"""Shared online reconciliation for both local and model extraction."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from .airtable import AirtableError
from .schema_memory import reconcile, schema_hash
from .sync import build_plan, _finish_plan
from .preview import enrich_display


def prepare_preview(client,report,config,store,progress=None):
    base_id = config.get("base_id")
    if not base_id or client.base_id != base_id:
        raise AirtableError("Airtable 连接与本次预览的数据库不一致，请重新检测连接。")
    schema=client.get_schema()
    memory=store.load(config["base_id"])
    state=reconcile(schema,config,memory)
    if state["blockers"]:
        plan=_finish_plan({"version":1,"base_id":config["base_id"],"report_date":report.get("report_date"),
            "source":report.get("source",""),"schema":schema,"table_ids":state["table_ids"],"changes":[],
            "project_guards":[],"warnings":state["warnings"],"blockers":state["blockers"]})
    else:
        expected_schema_hash = schema_hash(schema)
        snapshot=client.snapshot(state["table_ids"],progress=progress,schema=schema)
        try:
            matches = (snapshot.get("base_id") == base_id
                       and snapshot.get("table_ids") == state["table_ids"]
                       and schema_hash(snapshot.get("schema", {})) == expected_schema_hash)
        except (AttributeError, KeyError, TypeError, ValueError):
            matches = False
        if not matches:
            raise AirtableError("Airtable 读取结果与已核对的数据库或表结构不一致，请重新生成预览。")
        records = snapshot.get("records")
        if not isinstance(records, dict) or any(not isinstance(records.get(tid), list)
                                                for tid in state["table_ids"].values()):
            raise AirtableError("Airtable 读取结果不完整，尚未生成可写入预览，请重新读取。")
        plan=build_plan(report,snapshot,state["config"])
        plan["warnings"]=list(dict.fromkeys(plan["warnings"]+state["warnings"]))
        plan=_finish_plan(plan)
        plan=enrich_display(plan,snapshot)
        # Unresolved bindings retain their previous IDs; other fields can proceed.
        store.save(state["memory"])
    plan["schema_memory"]={"schema_hash":state["memory"]["schema_hash"],"base_id":config["base_id"],"rows":state["rows"]}
    return plan,state["config"]


def prepare_airtable_tracker(client, tracker_path, config, store, *, project_ids=None, progress=None):
    """Read fresh cloud values, then prepare a local-only, reviewable workbook plan.

    This is a separate read-only phase after a completed cloud sync. It never
    calls apply_plan, reconstructs values from the upload, or replays a write.
    ``None`` explicitly selects all cloud projects; an empty scope selects none.
    """
    from .airtable import AirtableError
    from .airtable_tracker import build_airtable_tracker_plan
    from .schema_memory import SchemaMemoryError, schema_hash
    from .tracker import fingerprint, verify_sources
    from .workbook import WorkbookError

    base_id = config.get("base_id")
    if not base_id or client.base_id != base_id:
        raise AirtableError("Airtable 连接与本次本地总表任务的数据库不一致，请重新检测连接。")
    if isinstance(project_ids, (str, bytes)):
        raise ValueError("项目范围必须是项目编号列表，不能是一段文本。")
    scope = list(project_ids) if project_ids is not None else None
    source_path = Path(tracker_path).resolve()
    source_hash = fingerprint(source_path)
    sidecar = Path(str(source_path) + ".autopm.json")
    sidecar_hash = fingerprint(sidecar) if sidecar.exists() else None
    read_started = datetime.now(timezone.utc).isoformat()

    schema = client.get_schema()
    state = reconcile(schema, config, store.load(base_id), strict=True)
    if state["blockers"]:
        raise SchemaMemoryError("Airtable 表结构需要核对，本地总表尚未更新：" + "；".join(state["blockers"]))
    snapshot = client.snapshot(state["table_ids"], progress=progress, schema=schema)
    if (snapshot.get("base_id") != base_id or snapshot.get("table_ids") != state["table_ids"] or
            schema_hash(snapshot.get("schema", {})) != schema_hash(schema)):
        raise AirtableError("Airtable 读取结果与已核对的数据库或表结构不一致，本地总表尚未更新。")
    if any(not isinstance(snapshot.get("records", {}).get(tid), list) for tid in state["table_ids"].values()):
        raise AirtableError("Airtable 读取结果不完整，本地总表尚未更新，请重新读取。")
    snapshot = deepcopy(snapshot)
    snapshot.setdefault("captured_at", datetime.now(timezone.utc).isoformat())
    plan = build_airtable_tracker_plan(source_path, snapshot, state["config"], project_ids=scope)
    if plan["tracker_sha256"] != source_hash or (fingerprint(sidecar) if sidecar.exists() else None) != sidecar_hash:
        raise WorkbookError("读取 Airtable 期间，本地总表或同步记录已变化，请重新生成预览。")
    if sidecar_hash is not None:
        plan.setdefault("source_files", {})[str(sidecar)] = sidecar_hash
    verify_sources(plan)
    plan["warnings"] = list(dict.fromkeys(state["warnings"] + plan["warnings"]))
    plan.setdefault("airtable_source", {}).update(read_started_at=read_started)
    plan["schema_memory"] = {"base_id": base_id, "schema_hash": state["memory"]["schema_hash"]}
    store.save(state["memory"])
    return plan


def prepare_tracker_writeback(client, tracker_path, config, store, progress=None):
    from .tracker_roundtrip import writeback_plan
    from .schema_memory import SchemaMemoryError
    if config.get('project_identity_mode') != 'number_sku_factory':
        raise ValueError('回写需要启用正式编号＋SKU＋工厂匹配。')
    if client.base_id != config.get('base_id'):
        raise AirtableError('连接与数据库不一致。')
    schema = client.get_schema()
    state = reconcile(schema, config, store.load(client.base_id))
    if state['blockers']:
        raise SchemaMemoryError('；'.join(state['blockers']))
    snapshot = client.snapshot(state['table_ids'], progress=progress, schema=schema)
    if (snapshot.get('base_id') != client.base_id or snapshot.get('table_ids') != state['table_ids']
            or schema_hash(snapshot.get('schema', {})) != schema_hash(schema)
            or any(not isinstance(snapshot.get('records', {}).get(tid), list) for tid in state['table_ids'].values())):
        raise AirtableError('云端数据读取不完整或数据库不一致。')
    plan = writeback_plan(tracker_path, snapshot, state['config'])
    plan['warnings'] = list(dict.fromkeys(plan['warnings'] + state['warnings']))
    return enrich_display(_finish_plan(plan), snapshot), state['config']
