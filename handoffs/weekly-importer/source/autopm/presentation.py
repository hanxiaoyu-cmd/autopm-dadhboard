"""Pure review-view helpers. Display strings are never Airtable write payloads.

``build_review_data(report, plan)`` expands changes into field rows and retains
independent, complete change payloads in ``changes``. Rows refer to those objects
by ``change_index``; the UI must apply its reviewed plan, not reconstruct writes
from table-cell text. This module does no I/O and has no GUI dependencies.
"""
from __future__ import annotations

import copy
import json
import re
from collections import Counter, defaultdict

from .normalize import clean_text, normalize_header, normalize_key, normalize_project_id


KIND_LABELS = {"projects": "项目", "tasks": "任务", "issues": "问题"}
ACTION_LABELS = {"create": "新增", "update": "更新", "read": "仅离线读取"}
SOURCE_FIELD_LABELS = {
    "project_id": "项目编号", "report_date": "周报更新日期", "project_name": "项目名称", "sku": "SKU",
    "brand": "品牌", "region": "地区", "type": "项目类型", "category": "品类", "sub_category": "子品类",
    "status": "项目状态", "npi_lead": "NPI 负责人", "npd_lead": "NPD 负责人", "pmo": "PMO 负责人",
    "pm": "PM", "epm": "EPM", "tpm": "TPM", "quality": "质量负责人", "factory": "工厂",
    "capacity": "产能 / 预测", "tooling": "模具", "current_progress": "当前进展", "update_this_week": "本周更新",
    "kick_off_date": "启动日期", "dqtp_finish_date": "DQTP 完成日期", "mp_aw_date": "MP AW 日期",
    "compliance_complete_date": "合规完成日期", "start_date": "开始日期", "mp_start_date": "量产开始日期",
    "name": "任务名称", "date": "任务日期", "completed": "来源完成标记", "owner": "负责人",
    "text": "问题内容", "action": "处理措施", "risk": "风险", "due_date": "到期日",
    "duration": "任务持续天数",
}
WARNING_LABELS = {
    "people_factory": "人员 / 工厂",
    "milestone": "里程碑映射",
    "dates": "日期核对",
    "identity": "重复 / 项目匹配",
    "completion": "完成状态",
    "model": "模型校验",
    "fields": "字段 / 选项",
    "other": "其他提示",
}


def format_value(value):
    """Human-readable full value, without truncation or mutation."""
    if value is None or value == "" or value == []:
        return "（空）"
    if isinstance(value, bool):
        return "是" if value else "否"
    if isinstance(value, list):
        return "、".join(format_value(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, indent=2)
    return str(value)


def _preview(text, limit=100):
    compact = re.sub(r"\s+", " ", str(text)).strip()
    return compact if len(compact) <= limit else compact[:limit - 1] + "…"


def _unique_title(items, key):
    titles = list(dict.fromkeys(clean_text(item.get(key)) for item in items if clean_text(item.get(key))))
    return titles[0] if len(titles) == 1 else None


def _source_item(change, projects):
    kind = change.get("kind")
    if kind not in {"tasks", "issues"}:
        return None
    title_key = "name" if kind == "tasks" else "text"
    items = [item for project in projects for item in project.get(kind, [])]
    source = clean_text(change.get("source"))
    identity_title = change.get("identity", {}).get("title")
    # Both location and normalized identity are available in current engine
    # plans. Use them together when possible; never choose the first ambiguous
    # source item just to obtain a prettier title.
    at_source = [item for item in items if source and clean_text(item.get("source")) == source]
    by_identity = [item for item in items if identity_title and normalize_key(item.get(title_key)) == identity_title]
    both = [item for item in at_source if item in by_identity]
    for candidates in (both, at_source, by_identity):
        if candidates and _unique_title(candidates, title_key):
            return candidates[0]
    return None


def _record_title(change, projects, source_item, schema_title_fields):
    for key in ("record_title", "title", "name"):
        if clean_text(change.get(key)):
            return clean_text(change[key])
    title_field = change.get("identity", {}).get("title_field")
    candidate_fields = [title_field] if title_field else []
    expected = {"tasks": "tasknamemanual", "issues": "issuerecordmanual", "projects": "projectnamemanual"}.get(change.get("kind"))
    candidate_fields.extend(schema_title_fields.get(change.get("kind"), []))
    candidate_fields.extend(fid for fid, name in change.get("field_names", {}).items() if expected and normalize_header(name) == expected)
    for fid in dict.fromkeys(candidate_fields):
        for values in (change.get("fields", {}), change.get("before", {})):
            if fid in values and clean_text(values[fid]):
                return clean_text(values[fid])
    if source_item:
        return clean_text(source_item.get("name") if change.get("kind") == "tasks" else source_item.get("text"))
    if change.get("kind") == "projects":
        title = _unique_title([p.get("fields", {}) for p in projects], "project_name")
        if title:
            return title
    # Serialized plans can outlive their source report. The stable identity is
    # still more useful than an empty title, and remains clearly a fallback.
    return (clean_text(change.get("identity", {}).get("title"))
            or clean_text(change.get("project_id"))
            or clean_text(change.get("record_id")) or "未命名记录")


def build_change_rows(report, plan):
    """Return one full-fidelity display row per changed field, in plan order.

    A malformed/empty change still receives one placeholder row so a review UI
    cannot silently hide a record. Each row links back through ``change_index``.
    """
    report = report or {}
    if plan is None:
        return build_offline_rows(report)
    project_index = defaultdict(list)
    for project in report.get("projects", []):
        project_index[normalize_project_id(project.get("project_id"))].append(project)
    schema_fields = {field["id"]: field for table in plan.get("schema", {}).get("tables", [])
                     for field in table.get("fields", [])}
    expected_titles = {"tasknamemanual": "tasks", "issuerecordmanual": "issues", "projectnamemanual": "projects"}
    schema_title_fields = defaultdict(list)
    for fid, field in schema_fields.items():
        kind = expected_titles.get(normalize_header(field.get("name")))
        if kind:
            schema_title_fields[kind].append(fid)
    rows = []
    for change_index, change in enumerate(plan.get("changes", [])):
        project_id = clean_text(change.get("project_id"))
        projects = project_index[normalize_project_id(project_id)]
        source_item = _source_item(change, projects)
        title = _record_title(change, projects, source_item, schema_title_fields)
        kind = change.get("kind", "")
        action = "update" if change.get("record_id") else "create"
        source = clean_text(change.get("source") or (source_item or {}).get("source") or report.get("source"))
        values = change.get("fields", {})
        # Display_* contains resolved linked-record names; false, zero, and empty
        # values are intentional and must not fall back through truthiness.
        for field_id in values or [None]:
            field_name = (change.get("field_names", {}).get(field_id)
                          or schema_fields.get(field_id, {}).get("name")
                          or field_id or "无字段变更")
            before_map, after_map = change.get("display_before", {}), change.get("display_after", {})
            before = before_map[field_id] if field_id in before_map else change.get("before", {}).get(field_id)
            after = after_map[field_id] if field_id in after_map else values.get(field_id)
            row = {
                "row_id": f"{change_index}:{field_id or '-'}", "change_index": change_index,
                "field_id": field_id, "record_id": change.get("record_id"), "table_id": change.get("table_id"),
                "project_id": project_id, "kind": kind, "kind_label": KIND_LABELS.get(kind, kind or "其他"),
                "record_title": title, "record_title_preview": _preview(title),
                "action": action, "action_label": "合并更新" if change.get("match_method") == "unique_issue_revision" else ACTION_LABELS[action], "field_name": field_name,
                "match_note": "同一问题修订，保留原记录 ID 和首次记录日期" if change.get("match_method") == "unique_issue_revision" else "",
                "before_text": format_value(before), "after_text": format_value(after), "source": source,
                "source_value_text": format_value(change["source_values"][field_id])
                    if field_id in change.get("source_values", {}) else "",
                "report_date": change.get("report_date", ""),
                "evidence": copy.deepcopy((source_item or {}).get("evidence", [])),
            }
            row["search_text"] = _search_text(" ".join(str(row[key]) for key in (
                "project_id", "kind_label", "record_title", "action_label", "field_name",
                "before_text", "after_text", "source", "source_value_text", "report_date")))
            rows.append(row)
    return rows


def build_offline_rows(report):
    """Display every source record without creating any Airtable operations.

    Rows have no record/table/field IDs or change indices. ``field_key`` is a
    source-data label only, and ``source_record_index`` keeps empty/duplicate
    source records visible without pretending they are database identities.
    """
    report = report or {}
    rows = []
    source_record_index = 0
    for project in report.get("projects", []):
        project_id = clean_text(project.get("project_id"))
        report_date = project.get("report_date") or report.get("report_date", "")
        project_values = {"project_id": project.get("project_id", "")}
        if report_date:
            project_values["report_date"] = report_date
        project_values.update(project.get("fields", {}))
        project_title = clean_text(project.get("fields", {}).get("project_name")) or project_id or "未命名项目"
        records = [("projects", project, project_values, project_title)]
        for kind, title_key, fallback in (("tasks", "name", "未命名任务"), ("issues", "text", "未命名问题")):
            for item in project.get(kind, []):
                values = {key: value for key, value in item.items() if key not in {"source", "evidence"}}
                if not values:
                    values = {title_key: ""}
                records.append((kind, item, values, clean_text(item.get(title_key)) or fallback))
        for kind, item, values, title in records:
            for field_index, (field_key, value) in enumerate(values.items()):
                evidence = item.get("evidence", [])
                if isinstance(evidence, dict):
                    evidence = evidence.get(field_key, evidence.get("fields", {}).get(field_key, []))
                evidence = copy.deepcopy(evidence or [])
                source = clean_text(item.get("source") or project.get("source") or report.get("source"))
                if kind == "projects" and isinstance(evidence, list) and evidence:
                    source = "、".join(str(reference) for reference in evidence)
                row = {
                    "row_id": f"offline:{source_record_index}:{field_index}", "change_index": None,
                    "source_record_index": source_record_index, "field_id": None, "field_key": field_key,
                    "record_id": None, "table_id": None, "project_id": project_id,
                    "kind": kind, "kind_label": KIND_LABELS[kind], "record_title": title,
                    "record_title_preview": _preview(title), "action": "read", "action_label": ACTION_LABELS["read"],
                    "field_name": SOURCE_FIELD_LABELS.get(field_key, field_key),
                    "before_text": "未对比 Airtable", "after_text": format_value(value), "source": source,
                    "source_value_text": format_value(value), "report_date": report_date, "evidence": evidence,
                }
                row["search_text"] = _search_text(" ".join(str(row[key]) for key in (
                    "project_id", "kind_label", "record_title", "action_label", "field_name", "field_key",
                    "before_text", "after_text", "source", "report_date")))
                rows.append(row)
            source_record_index += 1
    return rows


def _search_text(value):
    return re.sub(r"\s+", " ", clean_text(value)).casefold()


def _filter_value(value, labels):
    if value is None or value == "" or value in {"all", "全部"}:
        return None
    return next((key for key, label in labels.items() if value == label), value)


def filter_change_rows(rows, query="", *, kind=None, action=None, project_id=None, field=None):
    """Combine all filters with AND; search terms match full display values.

    ``kind`` / ``action`` accept either their canonical codes or Chinese labels.
    Filtering never changes or reconstructs the retained write payloads.
    """
    kind, action = _filter_value(kind, KIND_LABELS), _filter_value(action, ACTION_LABELS)
    project = normalize_project_id(project_id) if project_id else None
    field_key = normalize_key(field) if field else None
    terms = _search_text(query).split()
    return [row for row in rows
            if (not kind or row["kind"] == kind)
            and (not action or row["action"] == action)
            and (not project or normalize_project_id(row["project_id"]) == project)
            and (not field_key or normalize_key(row["field_id"]) == field_key or normalize_key(row["field_name"]) == field_key
                 or normalize_key(row.get("field_key")) == field_key)
            and all(term in row.get("search_text", "") for term in terms)]


def classify_warning(message):
    """Return a Chinese review label while keeping the original message separate."""
    text = str(message)
    lowered = text.casefold()
    if "表结构映射" in text:
        category, short = "fields", "表结构映射需核对"
        if "已沿用" in text or "已重新核对" in text:
            short = "表结构变化已核对"
    elif any(token in lowered for token in ("模型", "deepseek", "model ", "model_", "来源校验", "来源验证", "source validation")):
        category = "model"
        short = "模型修正后已通过校验" if "重新验证" in text else "模型来源或输出需核对"
    elif any(token in lowered for token in ("green completed", "completion retained", "完成状态", "完成标记", "绿色", "显式绿色")):
        category, short = "completion", "完成状态需核对"
        if "preview only" in lowered:
            short = "完成标记仅保留在预览"
    elif "existing milestone identity is ambiguous" in lowered:
        category, short = "identity", "现有里程碑任务存在歧义，已跳过"
    elif "duplicate milestone/source scope" in lowered:
        category, short = "identity", "同一里程碑存在重复来源，已跳过"
    elif "未新增或覆盖" in text:
        category, short = "identity", "问题修订匹配需核对，已跳过"
    elif any(token in lowered for token in ("里程碑", "milestone", "ordinary task")):
        category, short = "milestone", "里程碑尚未映射，任务未写入"
    elif any(token in lowered for token in ("duplicate", "重复", "expected one existing airtable project", "project identity", "project id changed", "shared across projects", "缺失项目", "缺少项目", "缺少 project")):
        category, short = "identity", "重复或项目身份需核对"
        if "found 0" in lowered:
            short = "项目尚未匹配，已跳过"
        elif "duplicate" in lowered or "重复" in text:
            short = "重复记录已跳过"
    elif any(token in lowered for token in ("people", "factory", "npi owner", "issue owner", "人员", "工厂", "负责人")):
        category, short = "people_factory", "人员或工厂未唯一匹配"
    elif any(token in lowered for token in ("日期", "删除线", "stale", "invalid date", "ambiguous date", "newer report", "date is missing", "report update date")):
        category, short = "dates", "日期或来源标记需核对"
        if "删除线" in text:
            short = "删除线日期已跳过"
        elif "stale" in lowered or "newer report" in lowered:
            short = "周报版本较旧，已跳过"
    elif any(token in lowered for token in ("option ", "unmapped/missing", "invalid number", "字段", "schema", "required setup", "read-only", "unsupported type")):
        category, short = "fields", "字段或选项需核对"
    else:
        category, short = "other", _preview(text, 90)
    return {"category": category, "category_label": WARNING_LABELS[category], "short_text": short}


def _warning_rows(messages, severity, project_ids):
    rows = []
    for index, message in enumerate(messages):
        text = str(message)
        first = re.match(r"^([^\s:\[：]+)", text)
        key = normalize_project_id(first[1]) if first else ""
        project_id = project_ids.get(key, "")
        row = {"warning_id": f"{severity}:{index}", "message": text, "severity": severity,
               "project_id": project_id, **classify_warning(text)}
        row["search_text"] = _search_text(" ".join((row["project_id"], row["category_label"], row["short_text"], text)))
        rows.append(row)
    return rows


def filter_warning_rows(rows, query="", *, category=None, project_id=None, severity=None):
    category = _filter_value(category, WARNING_LABELS)
    project = normalize_project_id(project_id) if project_id else None
    terms = _search_text(query).split()
    return [row for row in rows if (not category or row["category"] == category)
            and (not project or normalize_project_id(row["project_id"]) == project)
            and (not severity or row["severity"] == severity)
            and all(term in row["search_text"] for term in terms)]


def build_review_data(report, plan):
    """Build a complete review model without mutating report, plan, or payloads.

    Return keys: rows, changes (full independent payloads), warnings, blockers,
    warning_counts, warning_groups, summary. Warning counts exclude blockers;
    report warnings already contained in the plan are not counted twice.
    """
    report = report or {}
    offline = plan is None
    rows = build_change_rows(report, plan)
    plan = plan or {}
    changes = copy.deepcopy(plan.get("changes", []))
    messages = list(plan.get("warnings", []))
    seen = set(str(message) for message in messages)
    for message in report.get("warnings", []):
        if str(message) not in seen:
            messages.append(message)
            seen.add(str(message))
    project_ids = {normalize_project_id(p.get("project_id")): clean_text(p.get("project_id")) for p in report.get("projects", [])}
    project_ids.update({normalize_project_id(c.get("project_id")): clean_text(c.get("project_id")) for c in changes})
    warnings = _warning_rows(messages, "warning", project_ids)
    blockers = _warning_rows(plan.get("blockers", []), "blocker", project_ids)
    counts = dict(Counter(row["category"] for row in warnings))
    source_by_kind = {"projects": len(report.get("projects", [])),
                      "tasks": sum(len(project.get("tasks", [])) for project in report.get("projects", [])),
                      "issues": sum(len(project.get("issues", [])) for project in report.get("projects", []))}
    return {"mode": "offline" if offline else "comparison", "rows": rows, "changes": changes, "warnings": warnings, "blockers": blockers,
            "warning_counts": counts,
            "warning_groups": [{"category": category, "label": label, "count": counts.get(category, 0)}
                               for category, label in WARNING_LABELS.items()],
            "summary": {"change_count": len(changes), "row_count": len(rows),
                        "field_count": len(rows) if offline else sum(len(change.get("fields", {})) for change in changes),
                        "source_by_kind": source_by_kind, "source_record_count": sum(source_by_kind.values()),
                        "project_count": len({normalize_project_id(change.get("project_id")) for change in changes if change.get("project_id")}),
                        "create_count": sum(not bool(change.get("record_id")) for change in changes),
                        "update_count": sum(bool(change.get("record_id")) for change in changes),
                        "by_kind": dict(Counter(change.get("kind", "other") for change in changes)),
                        "warning_count": len(warnings), "blocker_count": len(blockers)}}
