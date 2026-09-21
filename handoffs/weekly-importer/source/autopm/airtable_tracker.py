"""Convert a fresh Airtable snapshot to a reviewable local tracker update.

Only values actually read from Airtable are candidates. Verified unit exports
may use a separate capture-date baseline for undated records; that baseline is
never written into the workbook's weekly-report date column.
"""

from collections import Counter, defaultdict
import math
import re

from .normalize import clean_text, normalize_header, normalize_project_id, parse_date
from .schema_memory import DEFAULT_FIELDS, LINKS, compatibility
from .sync import _field, _get, _mapping, _task_scope
from .tracker import TIMELINES, build_tracker_plan
from .weekly_remark import read_weekly_remark, uses_weekly_remark, REMARK_FIELDS
from .workbook import WorkbookError


_MILESTONES = {
    normalize_header(name): key
    for key, (_, names) in TIMELINES.items()
    for name in names
}
_MILESTONES.update(
    {
        normalize_header(name): key
        for name, key in {
            "TRA / ECN DD": "tra",
            "MPRA / ECN": "mpra",
            "Award": "start_date",
            "DQTP report": "dqtp_finish_date",
            "Compliance report": "compliance_complete_date",
            "MP AW release": "mp_aw_date",
        }.items()
    }
)


def _scope(project_ids):
    if project_ids is None:
        return None
    if isinstance(project_ids, str):
        project_ids = [project_ids]
    return {normalize_project_id(value) for value in project_ids if clean_text(value)}


def _location(base_id, table_id, record_id, field=None):
    path = f"Airtable/{base_id}/{table_id}/{record_id}"
    return path + (f"/{field['id']}" if field else "")


def _nonempty(value):
    return value is not None and value != "" and value != []


def _scalar(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError("云端值不是可写入 Excel 的文本或数字")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("云端数值无效")
    return clean_text(value) if isinstance(value, str) else value


def snapshot_to_report(snapshot, config, *, project_ids=None, identities=None):
    """Read resolved schema fields, returning the tracker report-shaped input.

    The caller obtains the snapshot after a completed cloud sync and revalidates
    schema memory. No credentials or extraction output enter this report.
    """
    base_id = snapshot.get("base_id")
    if not base_id or (config.get("base_id") and config["base_id"] != base_id):
        raise WorkbookError("Airtable 数据快照与当前 Base 不一致，请重新读取。")
    remark_storage = uses_weekly_remark(config)
    scope = _scope(project_ids)
    ids = snapshot.get("table_ids", {})
    schema_tables = snapshot.get("schema", {}).get("tables", [])
    records = {}
    fields = {}
    warnings = []
    for kind, defaults in DEFAULT_FIELDS.items():
        tid = ids.get(kind)
        tables = [table for table in schema_tables if table.get("id") == tid]
        if not tid or len(tables) != 1 or tid not in snapshot.get("records", {}):
            raise WorkbookError(f"Airtable 快照缺少完整的 {kind} 表，请重新读取。")
        rows = snapshot["records"][tid]
        if not isinstance(rows, list) or any(
            not isinstance(row, dict)
            or not isinstance(row.get("id"), str)
            or not isinstance(row.get("fields"), dict)
            for row in rows
        ):
            raise WorkbookError(f"Airtable 快照的 {kind} 记录格式无效，请重新读取。")
        records[kind] = rows
        fields[kind] = {}
        for key, target in _mapping(config, kind, defaults).items():
            try:
                field = _field(tables[0], target)
            except ValueError as exc:
                raise WorkbookError(f"Airtable 字段映射不唯一：{kind}.{key}。") from exc
            if field:
                error = compatibility(kind, key, field, ids)
                if error:
                    raise WorkbookError(
                        f"Airtable 字段映射无效：{kind}.{key}：{error}。请核对映射记忆。"
                    )
            fields[kind][key] = field
    pf = fields["projects"]
    tf = fields["tasks"]
    issue_fields = fields["issues"]
    report_date_field = (
        pf.get("current_progress") if remark_storage else pf.get("report_date")
    )
    if not pf.get("project_id") or not report_date_field:
        date_label = "Engineering remark 周报字段" if remark_storage else "周报日期"
        raise WorkbookError(
            f"Airtable 项目编号或{date_label}缺少有效映射，请核对映射记忆。"
        )
    indexes = {kind: defaultdict(list) for kind in records}
    for kind, rows in records.items():
        for record in rows:
            indexes[kind][record["id"]].append(record)

    def linked_names(value, kind):
        if not isinstance(value, list) or not all(
            isinstance(item, str) for item in value
        ):
            raise ValueError("云端关联值格式无效")
        name_field = fields[kind].get("name")
        if not name_field:
            raise ValueError(f"{kind} 名称字段未映射")
        names = []
        for record_id in dict.fromkeys(value):
            matches = indexes[kind].get(record_id, [])
            if len(matches) != 1:
                raise ValueError(f"{kind} 关联记录不存在或不唯一（{record_id}）")
            name = _get(matches[0], name_field)
            if not isinstance(name, str) or not clean_text(name):
                raise ValueError(f"{kind} 关联记录名称为空或无效（{record_id}）")
            names.append(clean_text(name))
        return "; ".join(sorted(names, key=str.casefold))

    counts = Counter(
        normalize_project_id(_get(row, pf["project_id"])) for row in records["projects"]
    )
    projects = []
    found_ids = set()
    for record in records["projects"]:
        if identities is not None and record['id'] not in identities:
            continue
        raw_pid = _get(record, pf["project_id"])
        if identities is not None:
            raw_pid = identities[record['id']]
        pid = normalize_project_id(raw_pid)
        if scope is not None and pid not in scope:
            continue
        found_ids.add(pid)
        if (
            not isinstance(raw_pid, str)
            or not pid
            or (identities is None and counts[pid] != 1)
            or len(indexes["projects"][record["id"]]) != 1
        ):
            warnings.append(
                f"{pid or record['id']}：Airtable 项目编号为空、无效或重复，已跳过项目。"
            )
            continue
        remark_fields = {}
        if remark_storage:
            try:
                remark = read_weekly_remark(_get(record, report_date_field))
            except ValueError as exc:
                warnings.append(
                    f"{pid}：Engineering remark 周报块无效，已跳过项目：{exc}；读取时间不能作为周报日期。"
                )
                continue
            report_date = parse_date(remark["report_date"])
            remark_fields = remark["fields"]
        else:
            report_date = parse_date(_get(record, report_date_field))
        date_basis = 'weekly_report'
        if not report_date and identities is not None:
            # A cloud snapshot is usable even before the first weekly import.
            # This is a capture date, never a fabricated weekly-report date.
            report_date = parse_date(str(snapshot.get('captured_at', ''))[:10])
            date_basis = 'airtable_capture'
        if not report_date:
            reason = (
                "Engineering remark 尚无有效周报日期块"
                if remark_storage
                else "Airtable 周报日期缺失或无效"
            )
            warnings.append(f"{pid}：{reason}，已跳过项目；读取时间不能作为周报日期。")
            continue
        source = _location(base_id, ids["projects"], record["id"])
        project = {
            "project_id": pid,
            "report_date": report_date,
            "date_basis": date_basis,
            "fields": {},
            "tasks": [],
            "issues": [],
            "source": source,
            "airtable_record_id": record["id"],
            "field_sources": {},
            "airtable_tasks": [],
        }
        report_date_source = _location(
            base_id, ids["projects"], record["id"], report_date_field
        )
        project["field_sources"]["report_date"] = report_date_source
        for key, field in pf.items():
            if key in {"project_id", "report_date"} or not field:
                continue
            # current_progress: extract from Engineering remark(Manual) richText block
            # update_this_week: read directly from Current stage (text field)
            if key == "current_progress" and remark_storage:
                raw_remark = _get(record, field)
                if raw_remark:
                    try:
                        current_progress = read_weekly_remark(raw_remark)["fields"].get(
                            "current_progress"
                        )
                        if date_basis == 'airtable_capture' and not current_progress:
                            current_progress = raw_remark
                        if _nonempty(current_progress):
                            project["fields"][key] = _scalar(current_progress)
                            project["field_sources"][key] = report_date_source
                    except Exception:
                        pass  # ignore damaged remark blocks
                continue
            if key == "update_this_week" and remark_storage:
                # Current stage is now a text field (not singleSelect); read directly
                value = _get(record, field)
                if _nonempty(value):
                    try:
                        project["fields"][key] = _scalar(value)
                        project["field_sources"][key] = _location(
                            base_id, ids["projects"], record["id"], field
                        )
                    except ValueError:
                        pass  # skip invalid text values
                continue
            value = _get(record, field)
            if not _nonempty(value):
                continue
            try:
                linked_kind = LINKS.get(("projects", key))
                if linked_kind:
                    value = linked_names(value, linked_kind)
                elif field["type"] == "multipleSelects":
                    if not isinstance(value, list) or not all(
                        isinstance(v, str) for v in value
                    ):
                        raise ValueError("云端多选值格式无效")
                    value = "; ".join(
                        sorted(set(clean_text(v) for v in value), key=str.casefold)
                    )
                else:
                    value = _scalar(value)
                if key.endswith("_date") or key in TIMELINES:
                    value = parse_date(value)
                    if not value:
                        raise ValueError("云端日期无效")
                project["fields"][key] = value
                project["field_sources"][key] = _location(
                    base_id, ids["projects"], record["id"], field
                )
            except ValueError as exc:
                warnings.append(f"{pid}：{key}：{exc}，保留本地值。")

        for key in sorted(REMARK_FIELDS):
            value = remark_fields.get(key)
            if _nonempty(value):
                project["fields"][key] = value
                project["field_sources"][key] = report_date_source

        candidates = defaultdict(list)
        blocked = set()
        milestone_counts = Counter()
        if records["tasks"] and not all(
            tf.get(key) for key in ("project", "name", "milestone", "due_date")
        ):
            warnings.append(
                f"{pid}：Airtable 任务的项目关联、名称、里程碑或截止日期映射不完整，未更新任务日期。"
            )
        elif tf.get("project"):
            for task in records["tasks"]:
                links = _get(task, tf["project"])
                if not isinstance(links, list) or record["id"] not in links:
                    continue
                name = _get(task, tf.get("name"))
                milestone = _get(task, tf.get("milestone"))
                raw_date = _get(task, tf.get("due_date"))
                key = (
                    _MILESTONES.get(normalize_header(milestone))
                    if isinstance(milestone, str)
                    else None
                )
                task_source = _location(
                    base_id, ids["tasks"], task["id"], tf.get("due_date")
                )
                audit = {
                    "record_id": task["id"],
                    "name": name,
                    "milestone": milestone,
                    "due_date": raw_date,
                    "source": task_source,
                }
                completed = tf.get("completed")
                if completed:
                    raw_completed = _get(task, completed)
                    if raw_completed is None or isinstance(raw_completed, bool):
                        audit["completed"] = raw_completed is True
                        audit["completion_source"] = _location(
                            base_id, ids["tasks"], task["id"], completed
                        )
                    else:
                        warnings.append(
                            f"{pid}：任务 {task['id']} 完成标记无效，未推断完成状态。"
                        )
                project["airtable_tasks"].append(audit)
                if not key:
                    if _nonempty(raw_date):
                        warnings.append(
                            f"{pid}：任务 {clean_text(name) or task['id']} 的云端里程碑无明确总表列，保留在审计记录。"
                        )
                    continue
                milestone_counts[key] += 1
                if len(links) != 1 or len(indexes["tasks"][task["id"]]) != 1:
                    blocked.add(key)
                    warnings.append(
                        f"{pid}：{key} 任务关联多个项目或记录重复，保留本地日期。"
                    )
                    continue
                # Do not collapse a regional schedule into a single global column.
                scope_tokens = _task_scope(name) | set(
                    re.findall(
                        r"\b(?:ID|IDN|MY|KH)\b",
                        clean_text(name).split(" - ", 1)[0].upper(),
                    )
                )
                if scope_tokens:
                    blocked.add(key)
                    warnings.append(
                        f"{pid}：任务 {clean_text(name)} 含地区范围，不能合并到总表单一 {key} 列。"
                    )
                    continue
                due_date = parse_date(raw_date)
                if not due_date:
                    if _nonempty(raw_date):
                        blocked.add(key)
                        warnings.append(
                            f"{pid}：任务 {clean_text(name)} 的云端截止日期无效，保留本地日期。"
                        )
                    continue
                candidates[key].append((due_date, task_source, audit))
        for key, count in milestone_counts.items():
            if count > 1:
                blocked.add(key)
                warnings.append(
                    f"{pid}：Airtable 同一 {key} 里程碑有多个任务，保留本地日期；不合并任务范围。"
                )
        for key, values in candidates.items():
            existing = project["fields"].get(key)
            if existing and any(value[0] != existing for value in values):
                blocked.add(key)
                warnings.append(
                    f"{pid}：Airtable 项目字段与任务 {key} 日期冲突，保留本地日期。"
                )
        for key in blocked:
            project["fields"].pop(key, None)
            project["field_sources"].pop(key, None)
        for key, values in candidates.items():
            if key in blocked:
                continue
            due_date, task_source, audit = values[0]
            if key in TIMELINES:
                project["tasks"].append(
                    {
                        "name": TIMELINES[key][1][0],
                        "date": due_date,
                        "source": task_source,
                        "airtable_record_id": audit["record_id"],
                        "airtable_task_name": audit["name"],
                        **(
                            {"completed": audit["completed"]}
                            if "completed" in audit
                            else {}
                        ),
                    }
                )
            else:
                project["fields"][key] = due_date
            project["field_sources"][key] = task_source
        # Optional approved project mappings may use timeline semantics such as
        # "tra" whose canonical key does not end in "_date". Feed these through
        # the tracker's date-aware timeline path, preserving the cloud source.
        for key in list(project["fields"]):
            if key in TIMELINES and not key.endswith("_date"):
                project["tasks"].append(
                    {
                        "name": TIMELINES[key][1][0],
                        "date": project["fields"].pop(key),
                        "source": project["field_sources"][key],
                    }
                )

        if issue_fields.get("project"):
            for issue in records["issues"]:
                links = _get(issue, issue_fields["project"])
                if not isinstance(links, list) or record["id"] not in links:
                    continue
                item = {
                    "airtable_record_id": issue["id"],
                    "source": _location(base_id, ids["issues"], issue["id"]),
                }
                for key, field in issue_fields.items():
                    value = _get(issue, field)
                    if not field or key == "project" or not _nonempty(value):
                        continue
                    try:
                        item[key] = (
                            linked_names(value, "people")
                            if key == "owner"
                            else _scalar(value)
                        )
                    except ValueError as exc:
                        warnings.append(
                            f"{pid}：问题 {issue['id']} 的 {key}：{exc}，仅保留来源定位。"
                        )
                project["issues"].append(item)
        projects.append(project)
    if scope is not None:
        for pid in sorted(scope - found_ids):
            warnings.append(f"{pid}：Airtable 中未找到本次范围的项目，已跳过。")
    if any(project["airtable_tasks"] for project in projects):
        warnings.append(
            "Airtable 任务完成标记仅在有明确复选框映射时保留到审计；本次不改变 Excel 完成颜色，也不根据日期推断完成。"
        )
    return {
        "source": f"Airtable {base_id}",
        "report_date": None,
        "projects": projects,
        "warnings": list(dict.fromkeys(warnings)),
        "source_kind": "airtable",
        "airtable_source": {
            "base_id": base_id,
            "captured_at": snapshot.get("captured_at"),
            "scope_project_ids": sorted(
                scope if scope is not None else found_ids - {""}
            ),
            "scope": "selected_projects" if scope is not None else "all_projects",
            "project_record_ids": [
                project["airtable_record_id"] for project in projects
            ],
        },
    }


def build_airtable_tracker_plan(tracker_path, snapshot, config, *, project_ids=None):
    """Build a non-destructive, version-guarded plan for a new workbook copy."""
    if config.get('project_identity_mode') == 'number_sku_factory':
        from .tracker_roundtrip import export_plan
        return export_plan(tracker_path, snapshot, config, project_ids=project_ids)
    report = snapshot_to_report(snapshot, config, project_ids=project_ids)
    plan = build_tracker_plan(tracker_path, [report])
    projects = {project["project_id"]: project for project in report["projects"]}
    for change in plan["changes"]:
        change["source"] = projects[change["project_id"]]["field_sources"].get(
            change["semantic"], change["source"]
        )
    plan["source_kind"] = "airtable"
    plan["airtable_source"] = report["airtable_source"]
    return plan
