"""Small Airtable Web API client. All writes are explicit; schema is read-only."""
from __future__ import annotations

import json
import io
import math
import socket
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from .normalize import normalize_key
from .network import NetworkDiagnosis, diagnose_network_error, verified_tls_context


class AirtableError(RuntimeError):
    def __init__(self, message, *, report=None):
        super().__init__(message)
        self.report = report


class UncertainWriteError(AirtableError):
    """A create may have succeeded. Reconcile records; never blindly repeat it."""


class _TransportError(urllib.error.URLError):
    """Expose a classified diagnosis instead of raw transport exception text."""

    def __init__(self, diagnosis):
        super().__init__(diagnosis.error_type)
        self.diagnosis = diagnosis


class _HttpxOpener:
    """Persistent, verified HTTP transport adapting to the injected-opener contract.

    Keep retry policy entirely in AirtableClient: in particular the HTTP transport
    must never automatically replay a POST. Redirects are rejected without sending
    the Authorization header to another URL.
    """
    def __init__(self, timeout=40, *, client=None):
        try:
            import httpx
        except ImportError:
            raise AirtableError("Missing httpx dependency; run the application setup script") from None
        self._httpx = httpx
        self._client = client if client is not None else httpx.Client(
            timeout=timeout, verify=verified_tls_context(), trust_env=True, follow_redirects=False,
            limits=httpx.Limits(max_connections=4, max_keepalive_connections=4, keepalive_expiry=30),
        )

    def __call__(self, request, timeout):
        try:
            response = self._client.request(
                request.get_method(), request.full_url, content=request.data,
                headers=dict(request.header_items()), timeout=timeout, follow_redirects=False,
            )
        except self._httpx.RequestError as exc:
            # Classify the original DNS/TCP/TLS chain before discarding sensitive text.
            raise _TransportError(diagnose_network_error(exc)) from None
        try:
            if response.status_code >= 300:
                raise urllib.error.HTTPError(request.full_url, response.status_code,
                                             response.reason_phrase, response.headers, None)
            return io.BytesIO(response.content)
        finally:
            response.close()

    def close(self):
        self._client.close()


def resolve_tables(schema, overrides=None):
    """Resolve only unique normalized names, or explicitly configured table IDs."""
    result = {}
    overrides = overrides or {}
    for kind in ("projects", "tasks", "issues", "people", "factories"):
        wanted = overrides.get(kind) or overrides.get(kind + "_table_id") or kind
        hits = [t for t in schema.get("tables", [])
                if t["id"] == wanted or normalize_key(t["name"]) == normalize_key(wanted)]
        if len(hits) != 1:
            raise AirtableError(f"Table {kind}: expected one match for {wanted!r}, found {len(hits)}")
        result[kind] = hits[0]["id"]
    return result


class AirtableClient:
    def __init__(self, token, base_id="", *, timeout=40, max_retries=3,
                 opener=None, sleep=None, clock=None, on_event=None):
        if not token:
            raise AirtableError("请填写完整的 Airtable Token，Token ID 不能用于连接。")
        if base_id.startswith("pat"):
            raise AirtableError("Base ID 中填写的是 Token ID。请在连接设置中点击“检测并选择数据库”。")
        self._token = token
        self.base_id = base_id
        self.timeout = timeout
        self.max_retries = max_retries
        self._on_event = on_event
        self._opener = opener if opener is not None else _HttpxOpener(timeout)
        self._owns_opener = opener is None
        self._sleep = sleep or time.sleep
        self._clock = clock or time.monotonic
        self._lock = threading.Lock()
        self._next_request = 0.0
        self._schema = None

    def _event(self, stage, method, path, attempt, started, *, diagnosis=None,
               retry_in=None, stop_reason=""):
        """Build reports exclusively from fixed labels and typed values, never URLs/data."""
        operation = ("检测数据库" if path == "meta/bases" else
                     "读取表结构" if path.startswith("meta/bases/") else
                     {"GET": "读取记录", "PATCH": "更新记录", "POST": "创建记录"}.get(method, "API 请求"))
        safe_method = method if method in {"GET", "PATCH", "POST"} else "API"
        maximum = self.max_retries + 1
        elapsed = round(max(0, self._clock() - started), 1)
        message = f"Airtable · {operation} · 第 {attempt}/{maximum} 次尝试"
        if stage == "retry":
            message = f"Airtable · {diagnosis.title}；{retry_in:g} 秒后第 {attempt + 1}/{maximum} 次尝试"
        elif stage == "recovered":
            message = f"Airtable · {operation}成功" + (f"（第 {attempt} 次尝试恢复）" if attempt > 1 else "")
        elif stage == "failed":
            message = f"Airtable · {operation}失败：{diagnosis.title}（已尝试 {attempt} 次）"
        event = {"stage": stage, "service": "Airtable", "host": "api.airtable.com",
                 "operation": operation, "method": safe_method, "attempt": attempt,
                 "max_attempts": maximum, "timeout": self.timeout, "elapsed": elapsed,
                 "at": datetime.now().astimezone().isoformat(timespec="seconds"), "message": message}
        lines = [message, f"时间：{event['at']}", f"目标：api.airtable.com · {safe_method} · {operation}",
                 f"请求尝试：{attempt}/{maximum}；累计用时：{elapsed:g} 秒；每个网络阶段超时：{self.timeout:g} 秒"]
        if diagnosis is not None:
            event["diagnosis"] = diagnosis.as_dict()
            lines.extend([f"故障类型：{diagnosis.title}（{diagnosis.error_type} / {diagnosis.code}）",
                          f"原因：{diagnosis.detail}", f"处理建议：{diagnosis.advice}"])
        if retry_in is not None:
            event["retry_in"] = retry_in
            lines.append(f"自动重试：等待 {retry_in:g} 秒后进行第 {attempt + 1} 次尝试。")
        if stop_reason:
            event["stop_reason"] = stop_reason
            lines.append("重试结果：" + stop_reason)
        event["report"] = "\n".join(lines)
        if self._on_event:
            try:
                # Observers cannot change whether a remote request is retried/replayed.
                self._on_event(dict(event, diagnosis=dict(event["diagnosis"])) if diagnosis else dict(event))
            except Exception:
                pass
        return event

    @staticmethod
    def _http_diagnosis(status):
        known = {
            401: ("Token 验证失败", "Airtable 已返回 HTTP 401，当前请求未通过身份验证。", "检查完整 Token 是否正确或已失效，然后重新检测连接。"),
            403: ("访问被拒绝", "Airtable 已返回 HTTP 403，当前操作没有被允许。", "检查 Token 的权限范围及目标数据库的 Access 授权。"),
            404: ("目标不存在或不可访问", "Airtable 已返回 HTTP 404，未能访问请求的目标。", "重新检测数据库，并核对数据库、表或记录是否仍存在及可访问。"),
            407: ("代理认证失败", "代理服务器要求身份验证（HTTP 407）。", "检查系统或环境代理的认证设置，然后重新检测连接。"),
            408: ("服务端请求超时", "服务端未能在规定时间内完成请求（HTTP 408）。", "检查网络连接稳定性，稍后重试。"),
            422: ("请求数据不符合要求", "Airtable 已返回 HTTP 422，请求内容未被接受。", "核对字段映射、字段类型和预览中的写入内容。"),
            429: ("请求过于频繁", "Airtable 已返回 HTTP 429，触发了请求限流。", "等待限流解除，避免同时运行多个同步任务。"),
        }
        if status in known:
            title, detail, advice = known[status]
        elif status >= 500:
            title, detail, advice = "服务端暂时异常", f"服务端返回 HTTP {status}。", "稍后重试；如持续发生，请检查 Airtable 服务状态。"
        elif 300 <= status < 400:
            title, detail, advice = "请求被重定向", f"收到 HTTP {status}；程序未向其他地址转发凭据。", "检查网络代理或网关是否改写了 API 请求。"
        else:
            title, detail, advice = "请求被拒绝", f"Airtable 已返回 HTTP {status}。", "检查连接配置和请求内容后重试。"
        return NetworkDiagnosis(code=f"http_{status}", title=title, detail=detail, advice=advice,
                                retryable=status in {408, 429, 500, 502, 503, 504}, error_type=f"HTTP {status}")

    @staticmethod
    def _rate_limit_wait(headers):
        value = (headers or {}).get("Retry-After", "30")
        try:
            delay = float(value)
        except (TypeError, ValueError, OverflowError):
            try:
                stamp = parsedate_to_datetime(value)
                if stamp.tzinfo is None:
                    stamp = stamp.replace(tzinfo=timezone.utc)
                delay = (stamp - datetime.now(timezone.utc)).total_seconds()
            except (TypeError, ValueError, OverflowError):
                delay = 30
        return max(30, delay) if math.isfinite(delay) else 30

    def close(self):
        """Release this client's persistent connection pool (injected openers stay caller-owned)."""
        if self._owns_opener:
            self._opener.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.close()

    def _throttle(self):
        with self._lock:
            delay = self._next_request - self._clock()
            if delay > 0:
                self._sleep(delay)
            # Slightly below four requests/second, including retries and pagination.
            self._next_request = self._clock() + 0.26

    def _request(self, method, path, payload=None, params=None):
        url = "https://api.airtable.com/v0/" + path
        if params:
            url += "?" + urllib.parse.urlencode(params, doseq=True)
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
        started = self._clock()
        for attempt in range(self.max_retries + 1):
            self._throttle()
            request = urllib.request.Request(url, data=encoded, method=method, headers={
                "Authorization": "Bearer " + self._token,
                "Content-Type": "application/json", "Accept": "application/json",
            })
            self._event("request", method, path, attempt + 1, started)
            try:
                with self._opener(request, timeout=self.timeout) as response:
                    result = json.load(response)
                self._event("recovered", method, path, attempt + 1, started)
                return result
            except urllib.error.HTTPError as exc:
                # Do not echo request headers, token, or arbitrary server response bodies.
                diagnosis = self._http_diagnosis(exc.code)
                if method == "POST" and (exc.code >= 500 or exc.code == 408):
                    report = self._event("failed", method, path, attempt + 1, started, diagnosis=diagnosis,
                                         stop_reason="新增记录的结果未知，未自动重发；请先核对 Airtable 和写入日志。")
                    raise UncertainWriteError(report["message"] + "；新增结果未知，请先核对记录，不能直接重试。", report=report) from None
                wait = self._rate_limit_wait(exc.headers) if exc.code == 429 else min(2 ** attempt, 8)
                if diagnosis.retryable and attempt < self.max_retries and wait <= 300:
                    self._event("retry", method, path, attempt + 1, started, diagnosis=diagnosis, retry_in=wait)
                    self._sleep(wait)
                    continue
                stop = ("服务要求等待超过 5 分钟，已停止自动重试；请稍后重新操作。" if wait > 300 else
                        "自动重试次数已用完。" if diagnosis.retryable else "此类错误需要修正配置或请求，未自动重试。")
                report = self._event("failed", method, path, attempt + 1, started, diagnosis=diagnosis, stop_reason=stop)
                raise AirtableError(f"Airtable {method} failed: HTTP {exc.code} · {diagnosis.title}；{diagnosis.advice}", report=report) from None
            except (urllib.error.URLError, TimeoutError, socket.timeout, ConnectionError, OSError) as exc:
                diagnosis = exc.diagnosis if isinstance(exc, _TransportError) else diagnose_network_error(exc)
                if method == "POST":
                    report = self._event("failed", method, path, attempt + 1, started, diagnosis=diagnosis,
                                         stop_reason="新增记录的结果未知，未自动重发；请先核对 Airtable 和写入日志。")
                    raise UncertainWriteError(report["message"] + "；新增结果未知，请先核对记录，不能直接重试。", report=report) from None
                if diagnosis.retryable and attempt < self.max_retries:
                    wait = min(2 ** attempt, 8)
                    self._event("retry", method, path, attempt + 1, started, diagnosis=diagnosis, retry_in=wait)
                    self._sleep(wait)
                    continue
                stop = "自动重试次数已用完。" if diagnosis.retryable else "此类错误需要修正网络配置，未自动重试。"
                report = self._event("failed", method, path, attempt + 1, started, diagnosis=diagnosis, stop_reason=stop)
                raise AirtableError(f"Airtable {method} connection failed ({diagnosis.error_type}) · {diagnosis.title}；{diagnosis.advice}", report=report) from None
            except (ValueError, UnicodeError):
                diagnosis = NetworkDiagnosis("invalid_json", "响应格式异常", "服务端响应不是有效 JSON，无法读取结果。",
                                             "检查代理或网关是否替换了响应；新增记录需先核对远端结果。", False, "InvalidJSON")
                report = self._event("failed", method, path, attempt + 1, started, diagnosis=diagnosis,
                                     stop_reason="响应不可读，已停止请求。" if method != "POST" else "新增记录的结果未知，未自动重发；请先核对 Airtable 和写入日志。")
                if method == "POST":
                    raise UncertainWriteError("Airtable 新增响应不可读，结果未知；请先核对记录，不能直接重试。", report=report) from None
                raise AirtableError("Airtable response was not valid JSON；请查看网络报告。", report=report) from None

    def list_bases(self):
        """List every authorized base without requiring a base ID."""
        bases, offset, seen = [], None, set()
        while True:
            data = self._request("GET", "meta/bases", params={"offset": offset} if offset else None)
            bases.extend(data.get("bases", []))
            offset = data.get("offset")
            if not offset:
                return bases
            if offset in seen:
                raise AirtableError("数据库列表分页异常，请重新检测。")
            seen.add(offset)

    def get_schema(self):
        if not self.base_id:
            raise AirtableError("请先检测并选择 Airtable 数据库。")
        self._schema = self._request("GET", "meta/bases/" + urllib.parse.quote(self.base_id, safe="") + "/tables")
        return self._schema

    def _path(self, table_id, record_id=None):
        if not self.base_id:
            raise AirtableError("请先检测并选择 Airtable 数据库。")
        parts = [self.base_id, table_id] + ([record_id] if record_id else [])
        return "/".join(urllib.parse.quote(str(p), safe="") for p in parts)

    def _by_id(self, table_id, record):
        """Normalize responses defensively; write endpoints may return field names."""
        if self._schema:
            table = next((t for t in self._schema["tables"] if t["id"] == table_id), None)
            if table:
                names = {f["name"]: f["id"] for f in table["fields"]}
                record = dict(record, fields={names.get(k, k): v for k, v in record.get("fields", {}).items()})
        return record

    def list_records(self, table_id, progress=None):
        """Read paginated records, optionally reporting cumulative page counts."""
        records, offset, seen, page_number = [], None, set(), 0
        while True:
            params = {"pageSize": 100, "returnFieldsByFieldId": "true"}
            if offset:
                params["offset"] = offset
            page = self._request("GET", self._path(table_id), params=params)
            records.extend(self._by_id(table_id, r) for r in page.get("records", []))
            page_number += 1
            if progress:
                progress({"stage": "page", "table_id": table_id, "page": page_number, "records": len(records)})
            offset = page.get("offset")
            if not offset:
                return records
            if offset in seen:
                raise AirtableError("Airtable returned a repeated pagination cursor")
            seen.add(offset)

    def get_record(self, table_id, record_id):
        record = self._request("GET", self._path(table_id, record_id), params={"returnFieldsByFieldId": "true"})
        return self._by_id(table_id, record)

    def update_record(self, table_id, record_id, fields):
        record = self._request("PATCH", self._path(table_id, record_id),
                               {"fields": fields, "typecast": False}, {"returnFieldsByFieldId": "true"})
        return self._by_id(table_id, record)

    def create_record(self, table_id, fields):
        record = self._request("POST", self._path(table_id),
                               {"fields": fields, "typecast": False}, {"returnFieldsByFieldId": "true"})
        return self._by_id(table_id, record)

    def snapshot(self, table_overrides=None, progress=None, *, schema=None):
        """Read one complete snapshot. Progress receives count-only event dictionaries.

        Stages are schema, table_start, page, table_done and done. Page events
        include table, table_id, page, records, tables_complete and tables_total.
        No record content or credentials are sent to the progress callback.
        """
        if progress:
            progress({"stage": "schema", "tables_complete": 0, "tables_total": 5})
        schema = self.get_schema() if schema is None else schema
        self._schema = schema
        table_ids = resolve_tables(schema, table_overrides)
        records = {}
        for index, (kind, tid) in enumerate(table_ids.items()):
            if progress:
                progress({"stage": "table_start", "table": kind, "table_id": tid,
                          "records": 0, "tables_complete": index, "tables_total": len(table_ids)})

                def page_progress(event, kind=kind, index=index):
                    progress({**event, "table": kind, "tables_complete": index, "tables_total": len(table_ids)})

                records[tid] = self.list_records(tid, progress=page_progress)
                progress({"stage": "table_done", "table": kind, "table_id": tid,
                          "records": len(records[tid]), "tables_complete": index + 1, "tables_total": len(table_ids)})
            else:
                records[tid] = self.list_records(tid)
        if progress:
            progress({"stage": "done", "records": sum(map(len, records.values())),
                      "tables_complete": len(table_ids), "tables_total": len(table_ids)})
        return {"base_id": self.base_id, "captured_at": datetime.now(timezone.utc).isoformat(),
                "schema": schema, "table_ids": table_ids, "records": records}
