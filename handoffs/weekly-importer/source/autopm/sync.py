"""Deterministic, reviewable weekly-report reconciliation with Airtable.

Language-model output is input data, never an authority for table IDs, field IDs,
select options, record identity, or arbitrary writes.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import re
import time
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from .airtable import AirtableError, UncertainWriteError, resolve_tables
from . import __version__
from .normalize import (
    clean_text,
    normalize_header,
    normalize_key,
    normalize_project_id,
    normalize_stage,
    normalize_task_title,
    parse_date,
)
from .weekly_remark import (
    uses_weekly_remark,
    read_weekly_remark,
    merge_weekly_remark,
    REMARK_FIELDS,
    JIRA_COUNT_FIELDS,
    remark_comparison_value,
)


PROJECT_FIELDS = {
    "project_id": "Project ID (Manual)",
    "project_number": "Project Number (Manual)",
    "project_name": "Project name (Manual)",
    "sku": "Project SKU (Manual)",
    "status": "Project Status (Manual)",
    "brand": "Brand (Manual)",
    "type": "Project Type (Manual)",
    "factory": "Factory (Manual)",
    "quality": "Quality Owner (Manual)",
    "npi_lead": "NPI Owner (Manual)",
    "npd_lead": "NPD Owner(Manual)",
    "pmo": "PMO Owner (Manual)",
    "current_progress": "Engineering remark(Manual)",
    "update_this_week": "Current stage",
    "jira_summary": "Jira summary (Manual)",
    "tooling": "Tooling (Manual)",
    "kick_off_date": "Kick Off Date (Manual)",
    "dqtp_finish_date": "DQTP Finish Date (Manual)",
    "mp_aw_date": "MP AW Date (Manual)",
    "compliance_complete_date": "Compliance Complete Date (Manual)",
    "start_date": "Start Date (Manual)",
    "mp_start_date": "MP Start Date (Manual)",
    "report_date": "Weekly Report Update Date (System)",
    "next_plm": "Next Action",
    "loa_13weeks_plan": "LOA-13weeks plan(Manual)",
    "jira_link": "Jira URL (Manual)",
}
TASK_FIELDS = {
    "name": "Task Name (Manual)",
    "project": "Projects (system manage)",
    "start_date": "Start Date (Manual)",
    "due_date": "Due Date (Manual)",
    "milestone": "Milestone (Manual)",
    "owners": "Tasks Owners (Manual)",
    "completed_by": "Completed By (Manual)",
    "latest_update": "Latest update (Manual)",
    "duration": "Duration for Start Date (Auto)",
}
ISSUE_FIELDS = {
    "text": "Issue description (Manual)",
    "project": "Projects (system manage)",
    "action": "Recovery Action (Manual)",
    "record_date": "Record Date (Auto)",
    "risk": "Severity (Manual)",
    "owner": "Recovery Owners (Manual)",
    "due_date": "Planned close Date (Manual)",
}
DEPARTMENTS = {"npi_lead": "NPI", "npd_lead": "NPD", "pmo": "PMO", "quality": "Quality"}
REQUIRED_PROJECT_TYPES = {
    "project_id": "singleLineText",
    # Active report version: weekly-remark storage uses current_progress;
    # legacy storage uses report_date. Either branch may be active, so both
    # keys must exist or required_project_types() raises KeyError before the
    # build_plan / reconcile guards can produce a readable blocker.
    "current_progress": "richText",
    "report_date": "date",
    "kick_off_date": "date",
    "dqtp_finish_date": "date",
    "mp_aw_date": "date",
    "compliance_complete_date": "date",
    "tooling": "singleLineText",
}


def required_project_types(config=None):
    """Only identity and the active report version protect the whole import."""
    version = "current_progress" if uses_weekly_remark(config or {}) else "report_date"
    return {key: REQUIRED_PROJECT_TYPES[key] for key in ("project_id", version)}


def project_type_matches(key, actual, expected):
    return actual == expected or (
        key in ("current_progress", "update_this_week")
        and actual in ("richText", "multilineText", "singleLineText")
    )


MILESTONE_ALIASES = {
    "kickoffdate": "Kick off",
    "kickoff": "Kick off",
    "award": "Award",
    "awarddate": "Award",
    "dqtpfinish": "DQTP report",
    "dqtpfinishdate": "DQTP report",
    "dqtp": "DQTP report",
    "compliancecomplete": "Compliance report",
    "compliancecompletedate": "Compliance report",
    "mpaw": "MP AW release",
    "mpawdate": "MP AW release",
    "mpstartdate": "MP Start",
    "newmpstart": "MP Start",
    "newmpstartdate": "MP Start",
    "previousmpstart": "Previous MP Date",
    "previousmpstartdate": "Previous MP Date",
    "oldmpstart": "Previous MP Date",
    "oldmpstartdate": "Previous MP Date",
    "ecndd": "TRA / ECN DD",
    "traecndd": "TRA / ECN DD",
    "mpraecn": "MPRA / ECN",
    "mpraecnimp": "MPRA / ECN",
    "p1": "P1 BUILD DATE",
    "p2": "P2 BUILD DATE",
    "p3": "P3 BUILD DATE",
    "fotdate": "FOT",
    "eb1date": "EB1",
    "eb2date": "EB2",
    "eb3date": "EB3",
    "cutsteeldate": "Cut Steel",
    "pilotdate": "Pilot",
    "mpra": "MPRA / ECN",
    "mpradate": "MPRA / ECN",
    "toolingtransferloaddate": "Tooling Transfer Load",
    "toolingtransferarrivaldate": "Tooling Transfer Arrival",
    "firstcrddate": "First CRD",
    "loa13wksplan": "LOA-13weeks",
    "loa": "LOA-13weeks",
    "p1caddrop": "P1 CAD DROP",
    "p2caddrop": "P2 CAD DROP",
    "p3caddrop": "P3 CAD DROP",
    "lastp": "Last P",
    "lastpbuilddate": "Last P BUILD DATE",
    "13weeksrelease": "13Weeks Release",
    "asrelease": "AS Release",
    "colorapproval": "Color approval",
    "fpo": "FPO",
    "mpawrelease": "MP AW release",
    "mpaw": "MP AW release",
}
WRITABLE = {
    "singleLineText",
    "multilineText",
    "richText",
    "email",
    "url",
    "phoneNumber",
    "singleSelect",
    "multipleSelects",
    "date",
    "dateTime",
    "number",
    "currency",
    "percent",
    "duration",
    "rating",
    "checkbox",
    "multipleRecordLinks",
}


def _now():
    return datetime.now(timezone.utc).isoformat()


def _field(table, target):
    if not target:
        return None
    hits = [
        f
        for f in table.get("fields", [])
        if f["id"] == target or normalize_key(f["name"]) == normalize_key(target)
    ]
    if len(hits) > 1:
        raise ValueError(f"Ambiguous field {table['name']}.{target}")
    return hits[0] if hits else None


def _mapping(config, kind, defaults):
    result = dict(defaults)
    custom = config.get("field_mapping", {}).get(kind, {})
    if isinstance(custom, dict):
        result.update(custom)
    return result


def _get(record, field):
    return (
        record.get("fields", {}).get(
            field["id"], record.get("fields", {}).get(field["name"])
        )
        if field
        else None
    )


def _empty(value):
    return (
        value is None
        or value == ""
        or value == []
        or (isinstance(value, str) and not value.strip())
    )


def _equivalent(left, right, field=None):
    if _empty(left) and _empty(right):
        return True
    if field and field.get("type") == "checkbox":
        return bool(left) == bool(right)
    if (
        field
        and field.get("type") == "richText"
        and isinstance(left, str)
        and isinstance(right, str)
    ):
        return remark_comparison_value(left) == remark_comparison_value(right)
    if isinstance(left, list) and isinstance(right, list):
        return sorted(left, key=str) == sorted(right, key=str)
    return left == right


def _coerce(field, value, context_date=None):
    kind = field["type"]
    if kind not in WRITABLE:
        raise ValueError(f"{field['name']}: read-only/unsupported type {kind}")
    if kind in {
        "singleLineText",
        "multilineText",
        "richText",
        "email",
        "url",
        "phoneNumber",
    }:
        if not isinstance(value, (str, int, float)) or isinstance(value, bool):
            raise ValueError(f"{field['name']}: expected text")
        return clean_text(value)
    if kind in {"singleSelect", "multipleSelects"}:
        options = [c["name"] for c in field.get("options", {}).get("choices", [])]

        def choose(raw):
            if raw in options:
                return raw
            hits = [
                name for name in options if normalize_key(name) == normalize_key(raw)
            ]
            if len(hits) != 1:
                raise ValueError(
                    f"{field['name']}: option {raw!r} has {len(hits)} matches; no option will be created"
                )
            return hits[0]

        if kind == "multipleSelects":
            values = value if isinstance(value, list) else [value]
            return list(dict.fromkeys(choose(v) for v in values))
        if not isinstance(value, str):
            raise ValueError(f"{field['name']}: expected one option")
        return choose(value)
    if kind == "date":
        value = parse_date(value, context_date)
        if not value:
            raise ValueError(f"{field['name']}: invalid/ambiguous date")
        return value
    if kind == "dateTime":
        raise ValueError(
            f"{field['name']}: dateTime requires explicit timezone mapping"
        )
    if kind == "checkbox":
        if not isinstance(value, bool):
            raise ValueError(f"{field['name']}: expected true/false")
        return value
    if kind == "multipleRecordLinks":
        if not isinstance(value, list) or not all(
            isinstance(v, str) and v.startswith("rec") for v in value
        ):
            raise ValueError(f"{field['name']}: expected resolved record IDs")
        return list(dict.fromkeys(value))
    if isinstance(value, bool):
        raise ValueError(f"{field['name']}: expected number")
    try:
        number = float(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        raise ValueError(f"{field['name']}: invalid number") from None
    if not math.isfinite(number):
        raise ValueError(f"{field['name']}: expected finite number")
    return int(number) if number.is_integer() else number


def _abbreviations(name):
    tokens = re.findall(r"[^\W_]+", clean_text(name), re.UNICODE)
    if not tokens:
        return set()
    result = {normalize_key(tokens[0]), normalize_key("".join(t[0] for t in tokens))}
    if len(tokens) > 1:
        result.add(normalize_key(tokens[0] + tokens[-1][0]))
        result.add(normalize_key(tokens[0][0] + tokens[-1]))
    return result


def _milestone_target(title, aliases):
    # Regional labels do not alter the fixed milestone meaning, but remain part
    # of task identity so CN and VN schedules cannot overwrite one another.
    label = normalize_task_title(title)
    key = normalize_header(label)
    configured = {normalize_header(k): v for k, v in aliases.items()}
    return configured.get(
        normalize_header(title), configured.get(key, MILESTONE_ALIASES.get(key, label))
    )


def _extract_narrative_date(text, context_date=None):
    """Extract a date from narrative text like 'Next PLM by Oct 15'.

    Returns ISO date string or None if unresolvable. Uses context_date year
    for yearless expressions when within half a year.
    """
    if not text or not isinstance(text, str):
        return None
    match = re.search(
        r"(?:by|due|before|target|on)\s+([A-Za-z]{3,9}\s*\d{1,2}(?:st|nd|rd|th)?(?:\s*,?\s*\d{4})?)",
        text,
        re.I,
    )
    if match:
        # Strip ordinal suffixes (1st, 2nd, 3rd, 4th) before parsing
        date_text = re.sub(r"(?<=\d)(st|nd|rd|th)\b", "", match[1], flags=re.I)
        return parse_date(date_text, context_date)
    return None


def _capacity_value(value):
    """Expand only a complete K amount with no period or an explicit month suffix.

    Year/day rates, mixed SKU amounts, descriptions, and forms such as 4K2 remain
    unchanged so ordinary numeric validation rejects them rather than guessing.
    """
    if not isinstance(value, str):
        return value
    match = re.fullmatch(
        r"(\d+(?:\.\d+)?)\s*k(?:\s*(?:/\s*month|per\s+month|monthly))?",
        clean_text(value),
        re.I,
    )
    if not match:
        return value
    number = float(match[1]) * 1000
    return int(number) if math.isfinite(number) and number.is_integer() else number


def _status_value(field, value):
    if not field or field["type"] != "singleSelect" or normalize_key(value) != "delay":
        return value
    choices = [choice["name"] for choice in field.get("options", {}).get("choices", [])]
    delayed = [name for name in choices if normalize_key(name) == "delayed"]
    if (
        not any(normalize_key(name) == "delay" for name in choices)
        and len(delayed) == 1
    ):
        return delayed[0]
    return value


def _resolve_person(value, table, records, department, aliases, mapping=None):
    mapping = mapping or {}
    name_field = _field(table, mapping.get("name", "Person Name (Manual)"))
    dept_field = _field(table, mapping.get("department", "Department (Manual)"))
    if "name" not in mapping:
        name_field = name_field or _field(table, "Name")
    if "department" not in mapping:
        dept_field = dept_field or _field(table, "Department")
    if not name_field:
        raise ValueError("People: Person Name field is missing")
    wanted = normalize_key(value)
    configured = {normalize_key(k): v for k, v in aliases.items()}.get(wanted)
    if configured:
        hits = [
            r
            for r in records
            if r["id"] == configured
            or normalize_key(_get(r, name_field)) == normalize_key(configured)
        ]
        if len(hits) != 1:
            raise ValueError(f"People alias {value!r} is not unique")
        return [hits[0]["id"]]
    dept = normalize_key(department)
    preferred = [
        r for r in records if dept and normalize_key(_get(r, dept_field)) == dept
    ]
    for pool in (preferred, records):
        exact = [r for r in pool if normalize_key(_get(r, name_field)) == wanted]
        hits = exact or [
            r for r in pool if wanted in _abbreviations(_get(r, name_field))
        ]
        if hits:
            if len(hits) == 1:
                return [hits[0]["id"]]
            raise ValueError(
                f"People {value!r}: ambiguous ({len(hits)} matches in {department or 'all departments'})"
            )
    raise ValueError(f"People {value!r}: no unique match")


def _resolve_people(value, table, records, department, aliases, mapping=None):
    names = (
        value if isinstance(value, list) else re.split(r"[\n;；]+", clean_text(value))
    )
    resolved = []
    for name in names:
        if clean_text(name):
            resolved.extend(
                _resolve_person(name, table, records, department, aliases, mapping)
            )
    if not resolved:
        raise ValueError("People: empty owner list")
    # All names must resolve before changing a linked owner list.
    return list(dict.fromkeys(resolved))


def _resolve_factory(value, table, records, aliases, mapping=None):
    candidates = (
        list(mapping.values())
        if mapping
        else [
            "Factory Full Name (Manual)",
            "Factory ID (Manual)",
            "Factory code",
            "Factory name (Old)",
        ]
    )
    fields = [f for name in candidates if (f := _field(table, name))]
    wanted = normalize_key(value)
    configured = {normalize_key(k): v for k, v in aliases.items()}.get(wanted)
    if configured:
        wanted = normalize_key(configured)
    name_field = _field(table, (mapping or {}).get('name', 'Factory Full Name (Manual)'))
    def names(record):
        values = [normalize_key(_get(record, f)) for f in fields if not _empty(_get(record, f))]
        name = normalize_key(_get(record, name_field))
        # Exact name + stored ID/code is a source spelling, not fuzzy matching.
        return values + [name + value for value in values if name and value != name]
    hits = [
        r
        for r in records
        if (configured and r["id"] == configured)
        or wanted in names(r)
    ]
    if len(hits) != 1:
        raise ValueError(
            f"Factory {value!r}: expected one name/code/alias match, found {len(hits)}"
        )
    return [hits[0]["id"]]


def _index_children(records, link_field, title_field):
    index = defaultdict(list)
    for record in records:
        title = normalize_key(_get(record, title_field))
        links = _get(record, link_field) or []
        if title and isinstance(links, list):
            for link in links:
                index[(link, title)].append(record)
    return index


def build_plan(report, snapshot, config=None):
    config = config or {}
    # Legacy/unknown reports default to exact identities. Merely configuring an
    # API key or changing the model name must not enable revision matching.
    merge_issue_revisions = report.get("extraction_mode") == "deepseek"
    plan = {
        "version": 1,
        "base_id": snapshot.get("base_id"),
        "created_at": _now(),
        "issue_matching_policy": "revisions" if merge_issue_revisions else "exact_only",
        "report_date": report.get("report_date"),
        "source": report.get("source", ""),
        "changes": [],
        "blockers": [],
        "warnings": list(report.get("warnings", [])),
        "project_guards": [],
        "schema": copy.deepcopy(snapshot.get("schema", {})),
    }
    warnings, blockers = plan["warnings"], plan["blockers"]
    schema = snapshot.get("schema", {})
    try:
        ids = snapshot.get("table_ids") or resolve_tables(
            schema, config.get("tables") or config.get("airtable_credentials")
        )
        plan["table_ids"] = ids
        tables = {
            kind: next(t for t in schema["tables"] if t["id"] == tid)
            for kind, tid in ids.items()
        }
    except (AirtableError, KeyError, StopIteration) as exc:
        blockers.append(f"Required setup: {exc}")
        return _finish_plan(plan)
    records = {
        kind: snapshot.get("records", {}).get(tid, []) for kind, tid in ids.items()
    }
    mappings = {
        "projects": _mapping(config, "projects", PROJECT_FIELDS),
        "tasks": _mapping(config, "tasks", TASK_FIELDS),
        "issues": _mapping(config, "issues", ISSUE_FIELDS),
    }
    try:
        fields = {
            kind: {k: _field(tables[kind], name) for k, name in mapping.items()}
            for kind, mapping in mappings.items()
        }
    except ValueError as exc:
        blockers.append(str(exc))
        return _finish_plan(plan)
    pf = fields["projects"]
    remark_storage = uses_weekly_remark(config)
    for key, expected in required_project_types(config).items():
        field = pf.get(key)
        if not field or not project_type_matches(key, field["type"], expected):
            blockers.append(
                f"Required setup: Projects.{mappings['projects'].get(key, key)} must be {expected}"
            )
    version_field = (
        pf.get("current_progress") if remark_storage else pf.get("report_date")
    )
    if not pf.get("project_id") or not version_field or blockers:
        return _finish_plan(plan)
    project_index = defaultdict(list)
    for record in records["projects"]:
        key = normalize_project_id(_get(record, pf["project_id"]))
        if key:
            project_index[key].append(record)
    strict_identity = config.get("project_identity_mode") == "number_sku_factory"
    source_projects = report.get("projects", [])
    if strict_identity:
        from .identity import match_units
        identity_fields = {k: (pf.get(k) or {}).get('id') for k in ('project_id', 'project_number', 'sku', 'factory')}
        if not all(identity_fields.values()):
            blockers.append('编号＋SKU＋工厂匹配需要完整的项目身份字段映射。')
            return _finish_plan(plan)
        source_projects = []
        plan['identity_review'] = []
        for source in report.get('projects', []):
            review = {'number':source.get('project_id'), 'sku':source.get('fields',{}).get('sku'),
                      'factory':source.get('fields',{}).get('factory'), 'source':source.get('source'),
                      'record_ids':[], 'reasons':[]}
            plan['identity_review'].append(review)
            try:
                factory_ids = _resolve_factory(source.get('fields', {}).get('factory'), tables['factories'],
                    records['factories'], config.get('factory_aliases', {}), config.get('field_mapping', {}).get('factories'))
            except (ValueError, TypeError) as exc:
                message = f"{source.get('project_id')}: {exc}; 无唯一工厂，项目未写入"
                warnings.append(message)
                review['reasons'].append(message)
                continue
            matches, notes = match_units(source.get('project_id'), source.get('fields', {}).get('sku'),
                                         factory_ids, records['projects'], identity_fields)
            warnings.extend(notes)
            review['reasons'].extend(notes)
            review['record_ids'] = [m['record']['id'] for m in matches]
            for match in matches:
                item = copy.deepcopy(source)
                item['_matched_record_id'] = match['record']['id']
                item['_unit_guard'] = match['guard']
                item['_match_method'] = match['method']
                # SKU/factory are identity inputs here, not a license to replace
                # a record's SKU list with the whole source project's SKU list.
                item['fields'].pop('sku', None)
                item['fields'].pop('factory', None)
                source_projects.append(item)
    project_counts = Counter(p.get('_matched_record_id') or normalize_project_id(p.get('project_id')) for p in source_projects)
    child_indexes = {}
    for kind, title in (("tasks", "name"), ("issues", "text")):
        child_indexes[kind] = _index_children(
            records[kind], fields[kind].get("project"), fields[kind].get(title)
        )

    def assign(target, key, value, out, context_date, project_id, linked=None):
        if _empty(value):
            return
        field = fields[target].get(key)
        if not field:
            warnings.append(
                f"{project_id}: {target}.{key} is unmapped/missing; retained in source only"
            )
            return
        try:
            if linked:
                actual = field.get("options", {}).get("linkedTableId")
                if field["type"] != "multipleRecordLinks" or actual != ids[linked]:
                    raise ValueError(f"{field['name']}: must link to {linked}")
            out[field["id"]] = _coerce(field, value, context_date)
        except (ValueError, TypeError) as exc:
            warnings.append(f"{project_id}: {exc}; value skipped")

    def append_change(
        kind, record, desired, project, project_record, context_date, source, **extras
    ):
        table = tables[kind]
        by_id = {f["id"]: f for f in table["fields"]}
        before = {fid: _get(record or {}, by_id[fid]) for fid in desired}
        changed = {
            fid: val
            for fid, val in desired.items()
            if not record or not _equivalent(before[fid], val, by_id[fid])
        }
        date_group = extras.get("date_group", {})
        if any(fid in changed for fid in date_group):
            # Airtable automations may recompute Due Date when Start Date changes.
            # Send and verify the full interval, including its stored duration.
            changed.update(date_group)
        if not changed:
            return
        plan["changes"].append(
            {
                "kind": kind,
                "table_id": table["id"],
                "record_id": record["id"] if record else None,
                "project_id": project,
                "project_record_id": project_record["id"],
                "report_date": context_date,
                "fields": changed,
                "before": {fid: before[fid] for fid in changed},
                "field_names": {fid: by_id[fid]["name"] for fid in changed},
                "source": source,
                **extras,
            }
        )

    for source_project in source_projects:
        project = copy.deepcopy(source_project)
        project_id = clean_text(project.get("project_id"))
        key = normalize_project_id(project_id)
        identity_key = project.get('_matched_record_id') or key
        if not key or project_counts[identity_key] != 1:
            warnings.append(
                f"Missing/duplicate report Project ID: {project_id!r}; project skipped"
            )
            continue
        matches = ([r for r in records['projects'] if r['id'] == project['_matched_record_id']]
                   if strict_identity else project_index.get(key, []))
        if len(matches) != 1:
            warnings.append(
                f"{project_id}: expected one existing Airtable project, found {len(matches)}; skipped"
            )
            continue
        current = matches[0]
        context_date = parse_date(
            project.get("report_date") or report.get("report_date")
        )
        if not context_date:
            warnings.append(
                f"{project_id}: report update date is missing/invalid; skipped"
            )
            continue
        try:
            old_date = (
                read_weekly_remark(_get(current, version_field))["report_date"]
                if remark_storage
                else parse_date(_get(current, version_field))
            )
        except ValueError as exc:
            warnings.append(
                f"{project_id}: invalid Engineering remark report metadata: {exc}; project skipped"
            )
            continue
        if old_date and old_date > context_date:
            warnings.append(
                f"{project_id}: stale report {context_date}; Airtable version {old_date}; entire project skipped"
            )
            continue
        guard = {
            "record_id": current["id"],
            "project_id": key,
            "id_field": pf["project_id"]["id"],
            "date_field": version_field["id"],
            "report_date": context_date,
        }
        if strict_identity:
            guard['unit_identity'] = project['_unit_guard']
        if remark_storage:
            guard.update(
                date_storage="engineering_remark",
                remark_before=_get(current, version_field),
            )
        desired, source_values = {}, {}
        if strict_identity:
            assign('projects', 'project_number', key, desired, context_date, project_id)
        values = project.get("fields", {})
        for canonical, value in values.items():
            if _empty(value) or canonical in {"project_id", "report_date"}:
                continue
            if remark_storage and canonical in REMARK_FIELDS | JIRA_COUNT_FIELDS:
                continue
            try:
                linked = None
                department = config.get("people_departments", {}).get(
                    canonical
                ) or DEPARTMENTS.get(canonical)
                field = pf.get(canonical)
                if canonical == "factory":
                    value = _resolve_factory(
                        value,
                        tables["factories"],
                        records["factories"],
                        config.get("factory_aliases", {}),
                        config.get("field_mapping", {}).get("factories"),
                    )
                    linked = "factories"
                elif department or (
                    field
                    and field["type"] == "multipleRecordLinks"
                    and field.get("options", {}).get("linkedTableId") == ids["people"]
                ):
                    value = _resolve_people(
                        value,
                        tables["people"],
                        records["people"],
                        department,
                        config.get("people_aliases", {}),
                        config.get("field_mapping", {}).get("people"),
                    )
                    linked = "people"
                elif canonical == "sku":
                    value = re.sub(r"\s*[,;，；\n]\s*", ", ", clean_text(value)).upper()
                elif canonical == "capacity" and field and field["type"] == "number":
                    mapped = _capacity_value(value)
                    if mapped != value:
                        source_values[field["id"]] = value
                    value = mapped
                elif canonical == "update_this_week" and field and field["type"] == "singleSelect":
                    stage = normalize_stage(value)
                    if stage and field:
                        source_values[field["id"]] = value
                        value = stage
                elif canonical == "status":
                    mapped = _status_value(field, value)
                    if field and mapped != value:
                        source_values[field["id"]] = value
                    value = mapped
                assign(
                    "projects",
                    canonical,
                    value,
                    desired,
                    context_date,
                    project_id,
                    linked,
                )
            except (ValueError, TypeError) as exc:
                warnings.append(f"{project_id}: {canonical}: {exc}; field skipped")
        if remark_storage:
            if not version_field:
                warnings.append(
                    f"{project_id}: Engineering remark storage enabled but current_progress field is unmapped; weekly remark skipped"
                )
            else:
                try:
                    remark = merge_weekly_remark(
                        _get(current, version_field),
                        context_date,
                        values,
                        rich_text=version_field["type"] == "richText",
                    )
                except (ValueError, TypeError) as exc:
                    warnings.append(
                        f"{project_id}: cannot merge Engineering remark: {exc}; project skipped"
                    )
                    continue
                # Preserve manual formatting and historic remarks exactly. _coerce's
                # text normalization must not rewrite the pre-existing note here.
                desired[version_field["id"]] = remark
                guard["remark_after"] = remark
            # Write Jira summary separately to Jira summary (Manual)
            jira_updates = {}
            jira_keys = [
                ("Total", "jira_total"),
                ("Ready to close", "jira_ready_to_close"),
                ("Verify", "jira_verify"),
                ("Open", "jira_open"),
                ("Closed", "jira_closed"),
            ]
            for label, key in jira_keys:
                val = values.get(key)
                if val is not None and str(val).strip():
                    if not re.fullmatch(r'\d+', str(val).strip()):
                        warnings.append(f'{project_id}: {key} 不是非负整数，未写入 Jira 汇总。')
                        continue
                    jira_updates[label.casefold()] = str(val).strip()
            jira_parts = []
            if jira_updates:
                previous = _get(current, pf.get('jira_summary')) or ''
                pattern = r'(Total|Ready to close|Verify|Open|Closed)\s*:\s*(\d+)'
                counts = {label.casefold():count for label,count in re.findall(pattern, previous, re.I)}
                if re.sub(pattern, '', previous, flags=re.I).strip(' ,;\r\n'):
                    warnings.append(f'{project_id}: 现有 Jira summary 含非标准文字，未覆盖，请核对预览来源。')
                else:
                    counts.update(jira_updates)
                    jira_parts = [f'{label}: {counts[label.casefold()]}' for label,_ in jira_keys if label.casefold() in counts]
            if jira_parts:
                assign(
                    "projects",
                    "jira_summary",
                    ", ".join(jira_parts),
                    desired,
                    context_date,
                    project_id,
                )
        else:
            assign(
                "projects",
                "report_date",
                context_date,
                desired,
                context_date,
                project_id,
            )
        plan["project_guards"].append(guard)
        append_change(
            "projects",
            current,
            desired,
            project_id,
            current,
            context_date,
            project.get("source", ""),
            source_values=source_values,
        )

        # Generate First CRD milestone task from project fields
        first_crd_date = values.get("first_crd_date")
        blocked_dates = project.get("blocked_fields", [])
        if _empty(first_crd_date) and not any(k in blocked_dates for k in ("first_crd_date", "mp_start_date")):
            mp_date = parse_date(values.get("mp_start_date"), context_date)
            if mp_date:
                first_crd_date = (date.fromisoformat(mp_date) - timedelta(days=45)).isoformat()
                warnings.append(f"{project_id}: First CRD 缺失/TBC，按 MP−45 个自然日推算为 {first_crd_date}。")
        if not _empty(first_crd_date) and not any(normalize_key(t.get('name')) in {'firstcrd', 'firstcrddate'} for t in project.get('tasks', [])):
            project.setdefault("tasks", []).append(
                {
                    "name": "First CRD",
                    "date": first_crd_date,
                }
            )

        # F7: Next PLM stable task — always update/create "Next PLM" task
        next_plm_text = values.get("next_plm")
        if next_plm_text and next_plm_text.strip().upper() not in ("N/A", "NA", ""):
            task_fields = fields["tasks"]
            due_date = _extract_narrative_date(next_plm_text, context_date)
            child = {}
            assign("tasks", "name", "Next PLM", child, context_date, project_id)
            if due_date:
                assign("tasks", "due_date", due_date, child, context_date, project_id)
            assign(
                "tasks", "latest_update", next_plm_text, child, context_date, project_id
            )
            if task_fields.get("project"):
                child[task_fields["project"]["id"]] = [current["id"]]
            existing_next_plm = [
                r
                for r in records["tasks"]
                if current["id"] in (_get(r, task_fields["project"]) or [])
                and normalize_key(_get(r, task_fields["name"])) == "nextplm"
            ]
            if len(existing_next_plm) > 1:
                warnings.append(
                    f"{project_id}: multiple existing 'Next PLM' tasks; no update performed"
                )
            else:
                existing = existing_next_plm[0] if existing_next_plm else None
                if not existing and pf.get('npi_lead'):
                    owner_ids = desired.get(pf['npi_lead']['id'], _get(current, pf['npi_lead']))
                    if owner_ids:
                        assign('tasks', 'owners', owner_ids, child, context_date, project_id, 'people')
                project_f = task_fields.get("project")
                name_f = task_fields.get("name")
                extras_f7 = (
                    {
                        "identity": {
                            "project_field": project_f["id"],
                            "title_field": name_f["id"],
                            "title": "nextplm",
                        }
                    }
                    if project_f and name_f
                    else {}
                )
                append_change(
                    "tasks",
                    existing,
                    child,
                    project_id,
                    current,
                    context_date,
                    project.get("source", ""),
                    **extras_f7,
                )
        for kind, title_key in (("tasks", "name"), ("issues", "text")):
            items = project.get(kind, [])
            kf = fields[kind]
            if not items:
                continue
            required = [title_key, "project"] + (
                ["due_date"] if kind == "tasks" else ["action", "record_date"]
            )
            missing = [name for name in required if not kf.get(name)]
            if missing:
                warnings.append(
                    f"{project_id}: {kind} missing fields {', '.join(missing)}; {kind} skipped"
                )
                continue
            expected_types = (
                {"name": {"singleLineText", "multilineText"}, "due_date": {"date"}}
                if kind == "tasks"
                else {
                    "text": {"singleLineText", "multilineText"},
                    "action": {"singleLineText", "multilineText"},
                    "record_date": {"date"},
                }
            )
            invalid = [
                name
                for name, allowed in expected_types.items()
                if kf[name]["type"] not in allowed
            ]
            if invalid:
                warnings.append(
                    f"{project_id}: {kind} incompatible field types: {', '.join(invalid)}; {kind} skipped"
                )
                continue
            if (
                kf["project"]["type"] != "multipleRecordLinks"
                or kf["project"].get("options", {}).get("linkedTableId")
                != ids["projects"]
            ):
                warnings.append(
                    f"{project_id}: {kind} project field must link to Projects; {kind} skipped"
                )
                continue
            if kind == 'tasks' and strict_identity:
                groups = defaultdict(list)
                for item in items:
                    target = _milestone_target(item.get('name',''), config.get('milestone_aliases',{}))
                    groups[target].append(item)
                normalized_items = []
                for target, group in groups.items():
                    if any(_task_scope(i.get('name')) for i in group) and kf.get('milestone'):
                        try:
                            canonical = _coerce(kf['milestone'], target, context_date)
                        except ValueError:
                            normalized_items.extend(group)
                            continue
                        dates = {parse_date(i.get('date'), context_date) for i in group}
                        if None in dates or len(dates) != 1:
                            warnings.append(f'{project_id}: {target} 地区日期冲突或缺失，未合并或写入。')
                            continue
                        normalized_items.append({**group[0], 'name':canonical,
                            'completed':all(i.get('completed') is True for i in group)})
                    else:
                        normalized_items.extend(group)
                items = normalized_items
            counts = Counter(normalize_key(item.get(title_key)) for item in items)
            issue_matches, issue_pool = ({}, [])
            if kind == "issues" and merge_issue_revisions:
                from .issue_matching import match_revisions

                issue_matches, issue_pool = match_revisions(
                    items, records[kind], current["id"], kf, normalize_key
                )
            for item_index, item in enumerate(items):
                title = clean_text(item.get(title_key))
                normalized = normalize_key(title)
                if not normalized or counts[normalized] > 1:
                    warnings.append(
                        f"{project_id}: duplicate/empty {kind} identity {title!r}; 该任务/问题未写入"
                    )
                    continue
                if kind == "tasks":
                    semantic_title = normalize_key(
                        _milestone_target(title, config.get("milestone_aliases", {}))
                    )
                    scope = _task_scope(title)
                    overlapping = [
                        i
                        for i in items
                        if normalize_key(
                            _milestone_target(
                                i.get("name", ""), config.get("milestone_aliases", {})
                            )
                        )
                        == semantic_title
                        and not (
                            scope
                            and _task_scope(i.get("name", ""))
                            and scope.isdisjoint(_task_scope(i.get("name", "")))
                        )
                    ]
                    if len(overlapping) > 1:
                        overlapping_dates = {
                            parse_date(i.get("date"), context_date) for i in overlapping
                        }
                        overlapping_dates.discard(None)
                        if len(overlapping_dates) == 1:
                            if item != overlapping[0]:
                                continue
                        else:
                            date_strs = ", ".join(
                                sorted(str(d) for d in overlapping_dates)
                            )
                            warnings.append(
                                f"{project_id}: duplicate milestone {title!r} with different dates ({date_strs}); 该任务未写入，请核对同一里程碑的多个来源"
                            )
                            continue
                hits = child_indexes[kind].get((current["id"], normalized), [])
                if len(hits) > 1:
                    warnings.append(
                        f"{project_id}: {kind} {title!r} has duplicate Airtable records; 该任务/问题未写入"
                    )
                    continue
                existing = hits[0] if hits else None
                issue_match = issue_matches.get(item_index)
                if kind == "issues" and issue_match:
                    if issue_match.get("reason"):
                        warnings.append(
                            f"{project_id}: issue {title!r}: {issue_match['reason']}；未新增或覆盖，请核对已有 issue"
                        )
                        continue
                    existing = issue_match["record"]
                if existing and len(_get(existing, kf["project"]) or []) != 1:
                    warnings.append(
                        f"{project_id}: {kind} {title!r} is shared across projects; 该任务/问题未写入"
                    )
                    continue
                child = {}
                assign(kind, title_key, title, child, context_date, project_id)
                assign(
                    kind,
                    "project",
                    [current["id"]],
                    child,
                    context_date,
                    project_id,
                    "projects",
                )
                extras = {
                    "identity": {
                        "project_field": kf["project"]["id"],
                        "title_field": kf[title_key]["id"],
                        "title": normalized,
                    }
                }
                if (
                    kind == "issues"
                    and issue_match
                    and issue_match["method"] == "unique_issue_revision"
                ):
                    extras["identity"]["title"] = normalize_key(
                        _get(existing, kf[title_key])
                    )
                    extras.update(
                        match_method="unique_issue_revision",
                        match_score=issue_match["score"],
                        source_title=title,
                    )
                    # Guard both the selected record and its candidate pool against
                    # concurrent edits. Keep original record_date and record ID.
                    guard_fields = [f["id"] for f in kf.values() if f]
                    extras["issue_match_guard"] = {
                        "fields": guard_fields,
                        "records": {
                            r["id"]: {
                                fid: r.get("fields", {}).get(fid)
                                for fid in guard_fields
                            }
                            for r in issue_pool
                        },
                    }
                if kind == "tasks":
                    task_date = parse_date(item.get("date"), context_date)
                    if not task_date:
                        warnings.append(
                            f"{project_id}: task {title!r} has no unambiguous date; skipped"
                        )
                        continue
                    milestone_target = _milestone_target(
                        title, config.get("milestone_aliases", {})
                    )
                    milestone = None
                    if kf.get("milestone"):
                        try:
                            milestone = _coerce(
                                kf["milestone"], milestone_target, context_date
                            )
                        except ValueError:
                            pass
                    if milestone:
                        assign(
                            kind,
                            "milestone",
                            milestone,
                            child,
                            context_date,
                            project_id,
                        )
                        if not existing:
                            scope = _task_scope(title)
                            candidates = [
                                r
                                for r in records[kind]
                                if current["id"] in (_get(r, kf["project"]) or [])
                                and _get(r, kf["milestone"]) == milestone
                                and not (
                                    scope
                                    and _task_scope(_get(r, kf[title_key]))
                                    and scope.isdisjoint(
                                        _task_scope(_get(r, kf[title_key]))
                                    )
                                )
                            ]
                            if candidates:
                                candidate = candidates[0]
                                prior_title = _get(candidate, kf[title_key])
                                prior_scope = _task_scope(prior_title)
                                source_count = sum(
                                    normalize_key(
                                        _milestone_target(
                                            i.get("name", ""),
                                            config.get("milestone_aliases", {}),
                                        )
                                    )
                                    == normalize_key(milestone_target)
                                    and not (
                                        prior_scope
                                        and _task_scope(i.get("name", ""))
                                        and prior_scope.isdisjoint(
                                            _task_scope(i.get("name", ""))
                                        )
                                    )
                                    for i in items
                                )
                                if (
                                    len(candidates) != 1
                                    or source_count != 1
                                    or not clean_text(prior_title)
                                    or len(_get(candidate, kf["project"]) or []) != 1
                                    or (
                                        scope
                                        and prior_scope
                                        and scope.isdisjoint(prior_scope)
                                    )
                                ):
                                    warnings.append(
                                        f"{project_id}: task {title!r}: existing milestone identity is ambiguous; 未新增重复任务，请核对现有任务名称/地区"
                                    )
                                    continue
                                # A template task often appends the project name.
                                # Preserve that name and ID; match only a unique
                                # milestone on both sides with compatible scope.
                                existing = candidate
                                child.pop(kf[title_key]["id"], None)
                                extras["identity"]["title"] = normalize_key(prior_title)
                                extras.update(
                                    match_method="unique_project_milestone",
                                    source_title=title,
                                )
                                extras["matched_milestone"] = {
                                    "field": kf["milestone"]["id"],
                                    "value": milestone,
                                }
                            else:
                                extras["milestone_guard"] = {
                                    "field": kf["milestone"]["id"],
                                    "value": milestone,
                                    "scope": sorted(scope),
                                }
                    else:
                        if config.get("require_milestone", False):
                            warnings.append(
                                f"{project_id}: {title!r}: 未配置里程碑映射，任务未写入 (no existing approved milestone option)"
                            )
                            continue
                        warnings.append(
                            f"{project_id}: {title!r} imported as ordinary task; no approved milestone option"
                        )
                    # Timeline dates are current milestone deadlines. Legacy saved
                    # +/-7 modes cannot override this source meaning. Preserve
                    # existing start/duration, which the report does not establish.
                    assign(kind, "due_date", task_date, child, context_date, project_id)
                    if not existing and pf.get("npi_lead"):
                        owner_ids = desired.get(
                            pf["npi_lead"]["id"], _get(current, pf["npi_lead"])
                        )
                        if owner_ids:
                            assign(
                                kind,
                                "owners",
                                owner_ids,
                                child,
                                context_date,
                                project_id,
                                "people",
                            )
                        else:
                            warnings.append(
                                f"{project_id}: task {title!r}: project NPI Owner is empty; task owner remains unassigned"
                            )
                    extras["completed"] = item.get("completed") is True
                    if item.get("completed") is True:
                        completed_field = kf.get("completed")
                        if completed_field and completed_field["type"] == "checkbox":
                            assign(
                                kind, "completed", True, child, context_date, project_id
                            )
                        else:
                            message = f"{project_id}: green completed task {title!r}; completion retained in preview only (no approved writable completion field)"
                            (
                                blockers
                                if config.get("require_completion_sync")
                                else warnings
                            ).append(message)
                        # F6: green completed -> Completed By (Manual) = union of existing + applicable owner
                        completed_by_field = kf.get("completed_by")
                        if completed_by_field:
                            if existing:
                                base_owners = _get(existing, kf.get("owners")) or []
                            else:
                                base_owners = (
                                    desired.get(
                                        pf["npi_lead"]["id"],
                                        _get(current, pf["npi_lead"]),
                                    )
                                    if pf.get("npi_lead")
                                    else []
                                )
                            if not isinstance(base_owners, list):
                                base_owners = [base_owners] if base_owners else []
                            existing_completed = (
                                _get(existing, completed_by_field) if existing else []
                            )
                            if not isinstance(existing_completed, list):
                                existing_completed = (
                                    [existing_completed] if existing_completed else []
                                )
                            merged = list(
                                dict.fromkeys(existing_completed + base_owners)
                            )
                            if merged:
                                assign(
                                    kind,
                                    "completed_by",
                                    merged,
                                    child,
                                    context_date,
                                    project_id,
                                    linked="people",
                                )
                else:
                    for name in ("action", "risk", "due_date"):
                        value = item.get(name)
                        if name == "risk" and isinstance(value, str):
                            value = {"h": "High", "m": "Medium", "l": "Low"}.get(
                                normalize_key(value), value
                            )
                        assign(kind, name, value, child, context_date, project_id)
                    if not existing:
                        assign(
                            kind,
                            "record_date",
                            context_date,
                            child,
                            context_date,
                            project_id,
                        )
                    if item.get("owner"):
                        try:
                            owners = _resolve_people(
                                item["owner"],
                                tables["people"],
                                records["people"],
                                None,
                                config.get("people_aliases", {}),
                                config.get("field_mapping", {}).get("people"),
                            )
                            assign(
                                kind,
                                "owner",
                                owners,
                                child,
                                context_date,
                                project_id,
                                "people",
                            )
                        except ValueError as exc:
                            warnings.append(
                                f"{project_id}: issue owner: {exc}; skipped"
                            )
                append_change(
                    kind,
                    existing,
                    child,
                    project_id,
                    current,
                    context_date,
                    item.get("source", ""),
                    **extras,
                )
    return _finish_plan(plan)


def _finish_plan(plan):
    plan["blockers"] = list(dict.fromkeys(plan["blockers"]))
    plan["warnings"] = list(dict.fromkeys(plan["warnings"]))
    plan["summary"] = dict(Counter(c["kind"] for c in plan["changes"]))
    digest = {k: v for k, v in plan.items() if k not in {"created_at", "plan_id"}}
    plan["plan_id"] = hashlib.sha256(
        json.dumps(digest, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()[:24]
    return plan


def _atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    # Windows scanners can briefly open the destination without delete sharing.
    # Retry only this local rename, never the remote record write it documents.
    for attempt in range(6):
        try:
            os.replace(temporary, path)
            break
        except OSError as exc:
            if getattr(exc, "winerror", None) not in {5, 32, 33} or attempt == 5:
                raise
            time.sleep(0.05 * 2**attempt)


def _record_fields_equal(record, expected, schema_fields):
    return all(
        _equivalent(record.get("fields", {}).get(fid), value, schema_fields.get(fid))
        for fid, value in expected.items()
    )


def _identity_hits(records, operation):
    if "identity" not in operation:
        return []
    identity = operation["identity"]
    titles = {identity["title"]}
    if operation.get("match_method") == "unique_issue_revision":
        titles.add(
            normalize_key(
                operation["fields"].get(identity["title_field"], identity["title"])
            )
        )
    return [
        r
        for r in records
        if operation["project_record_id"]
        in (r.get("fields", {}).get(identity["project_field"]) or [])
        and normalize_key(r.get("fields", {}).get(identity["title_field"])) in titles
    ]


def _check_issue_match(records, operation, changes, selected_only=False):
    guard = operation.get("issue_match_guard")
    if not guard:
        return
    project_field = operation["identity"]["project_field"]
    pool = {
        r["id"]: r
        for r in records
        if operation["project_record_id"]
        in (r.get("fields", {}).get(project_field) or [])
    }
    expected = guard["records"]
    if not selected_only and set(pool) != set(expected):
        raise AirtableError(
            "Issue candidates changed since preview; regenerate preview"
        )
    for rid, record in pool.items():
        before = expected.get(rid)
        if before is None:
            raise AirtableError(
                "Issue identity changed since preview; regenerate preview"
            )
        after = dict(before)
        for change in changes:
            if (
                change["table_id"] == operation["table_id"]
                and change.get("record_id") == rid
            ):
                after.update({k: v for k, v in change["fields"].items() if k in after})
        actual = {fid: record.get("fields", {}).get(fid) for fid in guard["fields"]}
        if actual != before and actual != after:
            raise AirtableError(
                "Issue matching evidence changed since preview; regenerate preview"
            )


def _task_scope(title):
    def countries(text):
        return set(re.findall(r"\b(?:CN|VN|TH|US|UK|EU|CA|JP|AU)\b", text.upper()))

    parts = re.split(r"\s+[-–—]\s+", clean_text(title), maxsplit=1)
    explicit = countries(parts[0])
    if explicit or len(parts) == 1:
        return explicit
    # Template suffixes describe the project, including its sales market.
    # Only an explicit factory location after "at" supplies a fallback scope.
    factory = re.split(r"\bat\b", parts[1], flags=re.I)
    return countries(factory[-1]) if len(factory) > 1 else set()


def _milestone_conflicts(records, operation):
    if "identity" not in operation:
        return []
    matched = operation.get("matched_milestone")
    if matched:
        target = next((r for r in records if r["id"] == operation["record_id"]), None)
        return (
            [target or {}]
            if not target
            or target.get("fields", {}).get(matched["field"]) != matched["value"]
            else []
        )
    guard = operation.get("milestone_guard")
    if not guard or operation.get("record_id"):
        return []
    identity = operation["identity"]
    scope = set(guard.get("scope", []))
    result = []
    for record in records:
        values = record.get("fields", {})
        if (
            operation["project_record_id"]
            not in (values.get(identity["project_field"]) or [])
            or values.get(guard["field"]) != guard["value"]
            or normalize_key(values.get(identity["title_field"])) == identity["title"]
        ):
            continue
        other_scope = _task_scope(values.get(identity["title_field"]))
        if not (scope and other_scope and scope.isdisjoint(other_scope)):
            result.append(record)
    return result


def apply_plan(client, plan, log_dir):
    """Apply an already reviewed plan, failing closed on conflicts and uncertainty.

    Airtable has no conditional PATCH/transaction API. Re-read immediately before
    every write and verify afterwards; another writer must not run concurrently.
    """
    if plan.get('source_kind') == 'tracker_writeback':
        from .tracker import fingerprint
        if not plan.get('source_files') or any(not Path(p).is_file() or fingerprint(p) != h for p, h in plan['source_files'].items()):
            raise AirtableError('All Tracker 或导出基线在预览后变化，请重新生成回写预览。')
    folder = Path(log_dir)
    folder.mkdir(parents=True, exist_ok=True)
    journal_path = folder / "write_journal.json"
    total_changes = len(plan.get("changes", []))
    result = {
        "status": "blocked",
        "applied": 0,
        "written_unverified": 0,
        "skipped": 0,
        "errors": [],
        "journal_path": str(journal_path),
        "version": __version__,
        "timestamp": _now(),
        "total": total_changes,
        "summary": {
            "projects": {"applied": 0, "skipped": 0, "failed": 0, "total": 0},
            "tasks": {"applied": 0, "skipped": 0, "failed": 0, "total": 0},
            "issues": {"applied": 0, "skipped": 0, "failed": 0, "total": 0},
        },
        "operations": [],
    }
    if plan.get("blockers"):
        result["errors"] = list(plan["blockers"])
        _atomic_json(folder / "result.json", result)
        return result
    if plan.get("base_id") and plan["base_id"] != client.base_id:
        result["errors"].append("Preview belongs to a different Airtable base")
        _atomic_json(folder / "result.json", result)
        return result
    lock_path = folder / "apply.lock"
    try:
        lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        result["errors"].append(
            "An apply is running or was interrupted; inspect apply.lock and the write journal before retrying"
        )
        return result
    os.close(lock_fd)
    journal = {"plan_id": plan.get("plan_id"), "started_at": _now(), "operations": []}
    try:
        if journal_path.exists():
            journal = json.loads(journal_path.read_text(encoding="utf-8"))
            if journal.get("plan_id") != plan.get("plan_id"):
                raise AirtableError(
                    "Run log folder contains another plan; use a new folder"
                )
        _atomic_json(folder / "preview.json", plan)
        fresh = client.snapshot(plan.get("table_ids"))
        _atomic_json(folder / "apply_snapshot.json", fresh)
        # One fresh scan per table is sufficient for deterministic identities.
        # Airtable has no atomic uniqueness/CAS operation; rescanning whole tables
        # before every create cannot remove that race and is prohibitively costly.
        # Keep this snapshot cache current with every reread and verified write.
        record_cache = {
            tid: {record["id"]: record for record in rows}
            for tid, rows in fresh["records"].items()
        }
        schema_fields = {
            f["id"]: f for t in fresh["schema"]["tables"] for f in t["fields"]
        }
        original_fields = {
            f["id"]: f
            for t in plan.get("schema", {}).get("tables", [])
            for f in t["fields"]
        }
        table_fields = {
            t["id"]: {f["id"] for f in t["fields"]} for t in fresh["schema"]["tables"]
        }
        for operation in plan.get("changes", []):
            for fid, value in operation["fields"].items():
                current_field = schema_fields.get(fid)
                if (
                    fid not in table_fields.get(operation["table_id"], set())
                    or not current_field
                ):
                    raise AirtableError(
                        f"Schema changed: missing field {fid}; regenerate preview"
                    )
                prior = original_fields.get(fid)
                if prior and (
                    prior["type"] != current_field["type"]
                    or prior.get("options") != current_field.get("options")
                ):
                    raise AirtableError(
                        f"Schema changed: {current_field['name']}; regenerate preview"
                    )
                _coerce(current_field, value, operation["report_date"])
        projects_id = plan["table_ids"]["projects"]
        guards = {g["record_id"]: g for g in plan.get("project_guards", [])}
        verified_project_versions = set()

        def guard_project(project_record, guard):
            values = project_record.get("fields", {})
            if guard.get('unit_identity'):
                identity = guard['unit_identity']
                allowed = dict(identity['before'])
                number_field = identity['fields']['project_number']
                if any(values.get(fid) != value and not (fid == number_field and normalize_project_id(values.get(fid)) == identity['number'])
                       for fid, value in allowed.items()):
                    raise AirtableError('项目编号、SKU 或工厂在预览后变化，请重新匹配。')
            elif (
                normalize_project_id(values.get(guard["id_field"]))
                != guard["project_id"]
            ):
                raise AirtableError(
                    "Project ID changed since preview; regenerate preview"
                )
            raw_version = values.get(guard["date_field"])
            if guard.get("date_storage") == "engineering_remark":
                current_date = read_weekly_remark(raw_version)["report_date"]
            else:
                current_date = parse_date(raw_version)
            if current_date and current_date > guard["report_date"]:
                raise AirtableError(
                    f"Project has a newer report ({current_date}); stale write blocked"
                )
            if guard.get("date_storage") == "engineering_remark":
                expected = (
                    [guard.get("remark_after")]
                    if guard["record_id"] in verified_project_versions
                    else [guard.get("remark_before"), guard.get("remark_after")]
                )
                if not any(
                    _equivalent(
                        raw_version, value, schema_fields.get(guard["date_field"])
                    )
                    for value in expected
                ):
                    raise AirtableError(
                        "Engineering remark changed since preview; regenerate preview"
                    )

        for guard in guards.values():
            if guard.get('unit_identity'):
                from .identity import guard_matches
                if not guard_matches(fresh['records'][projects_id], guard['unit_identity']):
                    raise AirtableError('编号＋SKU＋工厂匹配在预览后不再唯一，已停止写入。')
                hits = [r for r in fresh['records'][projects_id] if r['id'] == guard['record_id']]
            else:
                hits = [
                r
                for r in fresh["records"][projects_id]
                if normalize_project_id(r.get("fields", {}).get(guard["id_field"]))
                == guard["project_id"]
                ]
            if len(hits) != 1 or hits[0]["id"] != guard["record_id"]:
                raise AirtableError(
                    "Project identity is missing/duplicated since preview"
                )
            guard_project(hits[0], guard)
        # Validate every existing target before starting writes to reduce partial runs.
        for operation in plan.get("changes", []):
            pool = fresh["records"].get(operation["table_id"], [])
            _check_issue_match(pool, operation, plan["changes"])
            if _milestone_conflicts(pool, operation):
                raise AirtableError(
                    "An equivalent milestone task exists with another name; regenerate preview"
                )
            if operation.get("identity"):
                matches = _identity_hits(pool, operation)
                if len(matches) > 1:
                    raise AirtableError("Duplicate task/issue appeared since preview")
            if operation.get("record_id"):
                current = next(
                    (r for r in pool if r["id"] == operation["record_id"]), None
                )
                if not current:
                    raise AirtableError("A preview target no longer exists")
                if not _record_fields_equal(
                    current, operation["fields"], schema_fields
                ) and not _record_fields_equal(
                    current, operation["before"], schema_fields
                ):
                    raise AirtableError(
                        f"Concurrent edit: {operation['project_id']} {operation['kind']}; regenerate preview"
                    )
        for index, operation in enumerate(plan.get("changes", [])):
            guard = guards.get(operation["project_record_id"])
            if not guard:
                raise AirtableError("Preview is missing a project identity guard")
            guard_project(
                client.get_record(projects_id, operation["project_record_id"]), guard
            )
            if _milestone_conflicts(
                record_cache[operation["table_id"]].values(), operation
            ):
                raise AirtableError(
                    "An equivalent milestone task appeared; duplicate creation blocked"
                )
            entries = [
                entry for entry in journal["operations"] if entry["index"] == index
            ]
            entry = entries[-1] if entries else None
            current = None
            if operation.get("record_id"):
                current = client.get_record(
                    operation["table_id"], operation["record_id"]
                )
                _check_issue_match(
                    [current], operation, plan["changes"], selected_only=True
                )
                record_cache[operation["table_id"]][current["id"]] = current
                if _milestone_conflicts([current], operation):
                    raise AirtableError(
                        "Matched milestone changed immediately before write; regenerate preview"
                    )
                if operation.get("identity"):
                    hits = _identity_hits(
                        record_cache[operation["table_id"]].values(), operation
                    )
                    if (
                        len(hits) != 1
                        or hits[0]["id"] != current["id"]
                        or current.get("fields", {}).get(
                            operation["identity"]["project_field"]
                        )
                        != [operation["project_record_id"]]
                    ):
                        raise AirtableError(
                            "Task/issue identity changed or duplicated; write blocked"
                        )
            else:
                hits = _identity_hits(
                    record_cache[operation["table_id"]].values(), operation
                )
                if len(hits) > 1:
                    raise AirtableError(
                        "Duplicate task/issue appeared; creation blocked"
                    )
                if hits:
                    # A planned create may already exist after a prior partial
                    # run. Verify it directly instead of rescanning its table.
                    current = client.get_record(operation["table_id"], hits[0]["id"])
                    record_cache[operation["table_id"]][current["id"]] = current
                    if not _identity_hits([current], operation) or current.get(
                        "fields", {}
                    ).get(operation["identity"]["project_field"]) != [
                        operation["project_record_id"]
                    ]:
                        raise AirtableError(
                            "Task/issue identity changed since preflight; regenerate preview"
                        )
                if current and not _record_fields_equal(
                    current, operation["fields"], schema_fields
                ):
                    raise AirtableError(
                        "Task/issue was created since preview with different values; regenerate preview"
                    )
            if current and _record_fields_equal(
                current, operation["fields"], schema_fields
            ):
                if operation["kind"] == "projects":
                    verified_project_versions.add(operation["project_record_id"])
                result["skipped"] += 1
                result["summary"][operation["kind"]]["skipped"] += 1
                result["summary"][operation["kind"]]["total"] += 1
                result["operations"].append(
                    {
                        "index": index,
                        "kind": operation.get("kind", "unknown"),
                        "project_id": operation.get("project_id", ""),
                        "project_record_id": operation.get("project_record_id", ""),
                        "record_id": current["id"] if current else None,
                        "status": "skipped",
                        "reason": "already_applied",
                        "fields_changed": list(operation.get("fields", {}).keys()),
                    }
                )
                if not entry:
                    journal["operations"].append(
                        {
                            "index": index,
                            "state": "already_applied",
                            "record_id": current["id"],
                            "at": _now(),
                        }
                    )
                else:
                    entry.update(
                        state="verified", record_id=current["id"], verified_at=_now()
                    )
                _atomic_json(journal_path, journal)
                continue
            if current and not _record_fields_equal(
                current, operation["before"], schema_fields
            ):
                raise AirtableError(
                    "Concurrent edit immediately before write; regenerate preview"
                )
            if (
                not current
                and entry
                and entry.get("state")
                in {"started", "uncertain", "verified", "written"}
            ):
                raise AirtableError(
                    "Earlier create may have succeeded; journal requires reconciliation before retry"
                )
            entry = {
                "index": index,
                "state": "started",
                "at": _now(),
                "operation": copy.deepcopy(operation),
            }
            journal["operations"].append(entry)
            _atomic_json(
                journal_path, journal
            )  # Persist intent before sending a mutation.
            try:
                written = (
                    client.update_record(
                        operation["table_id"],
                        operation["record_id"],
                        operation["fields"],
                    )
                    if operation.get("record_id")
                    else client.create_record(
                        operation["table_id"], operation["fields"]
                    )
                )
                entry.update(
                    state="written", record_id=written["id"], written_at=_now()
                )
                _atomic_json(journal_path, journal)
                verified = client.get_record(operation["table_id"], written["id"])
                if not _record_fields_equal(
                    verified, operation["fields"], schema_fields
                ):
                    entry["verification"] = {
                        fid: {"name": schema_fields.get(fid, {}).get("name", fid),
                              "expected": value, "actual": verified.get("fields", {}).get(fid)}
                        for fid, value in operation["fields"].items()
                        if not _equivalent(verified.get("fields", {}).get(fid), value, schema_fields.get(fid))
                    }
                    raise AirtableError(
                        "写入已返回成功，但回读内容未通过校验；请核对写入日志中的字段差异，勿直接重复导入。"
                    )
                if operation["kind"] == "projects":
                    verified_project_versions.add(operation["project_record_id"])
                record_cache[operation["table_id"]][verified["id"]] = verified
                entry.update(state="verified", verified_at=_now())
                result["applied"] += 1
                result["summary"][operation["kind"]]["applied"] += 1
                result["summary"][operation["kind"]]["total"] += 1
                result["operations"].append(
                    {
                        "index": index,
                        "kind": operation.get("kind", "unknown"),
                        "project_id": operation.get("project_id", ""),
                        "project_record_id": operation.get("project_record_id", ""),
                        "record_id": verified["id"],
                        "status": "applied",
                        "action": "update" if operation.get("record_id") else "create",
                        "fields_changed": list(operation.get("fields", {}).keys()),
                    }
                )
                _atomic_json(journal_path, journal)
            except UncertainWriteError:
                entry.update(
                    state="uncertain", error="Create result unknown. No retry was sent."
                )
                result["summary"][operation["kind"]]["failed"] += 1
                result["summary"][operation["kind"]]["total"] += 1
                result["operations"].append(
                    {
                        "index": index,
                        "kind": operation.get("kind", "unknown"),
                        "project_id": operation.get("project_id", ""),
                        "project_record_id": operation.get("project_record_id", ""),
                        "record_id": None,
                        "status": "failed",
                        "reason": "uncertain_write",
                        "fields_changed": list(operation.get("fields", {}).keys()),
                    }
                )
                _atomic_json(journal_path, journal)
                raise
            except Exception as exc:
                written_unverified = entry.get("state") == "written"
                if written_unverified:
                    result["written_unverified"] += 1
                entry["error"] = (
                    f"Write or verification failed; {type(exc).__name__}: {exc}; "
                    "inspect remote state before retry"
                )
                result["summary"][operation["kind"]]["failed"] += 1
                result["summary"][operation["kind"]]["total"] += 1
                result["operations"].append(
                    {
                        "index": index,
                        "kind": operation.get("kind", "unknown"),
                        "project_id": operation.get("project_id", ""),
                        "project_record_id": operation.get("project_record_id", ""),
                        "record_id": entry.get("record_id"),
                        "status": "failed",
                        "reason": "verification_failed" if written_unverified else "write_error",
                        "error": f"{type(exc).__name__}: {exc}",
                        "fields_changed": list(operation.get("fields", {}).keys()),
                    }
                )
                _atomic_json(journal_path, journal)
                raise
        result["status"] = "completed"
    except (AirtableError, ValueError, OSError, KeyError) as exc:
        result["status"] = "partial" if result["applied"] or result["written_unverified"] else "blocked"
        result["errors"].append(str(exc))
    finally:
        _atomic_json(folder / "result.json", result)
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass
    return result
