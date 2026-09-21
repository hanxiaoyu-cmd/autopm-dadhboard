"""Base-scoped, revalidated schema bindings. No record data, secrets or free-form instructions."""

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from .normalize import normalize_key
from .config import with_base_defaults
from .sync import (
    PROJECT_FIELDS,
    TASK_FIELDS,
    ISSUE_FIELDS,
    REQUIRED_PROJECT_TYPES,
    WRITABLE,
    _atomic_json,
    required_project_types,
    project_type_matches,
)

PEOPLE_FIELDS = {"name": "Person Name (Manual)", "department": "Department (Manual)"}
FACTORY_FIELDS = {
    "name": "Factory Full Name (Manual)",
    "factory_id": "Factory ID (Manual)",
    "code": "Factory code",
    "old_name": "Factory name (Old)",
}
DEFAULT_FIELDS = {
    "projects": PROJECT_FIELDS,
    "tasks": TASK_FIELDS,
    "issues": ISSUE_FIELDS,
    "people": PEOPLE_FIELDS,
    "factories": FACTORY_FIELDS,
}
LINKS = {("projects", k): "people" for k in ("npi_lead", "npd_lead", "pmo", "quality")}
LINKS.update(
    {
        ("projects", "factory"): "factories",
        ("tasks", "project"): "projects",
        ("issues", "project"): "projects",
        ("tasks", "owners"): "people",
        ("issues", "owner"): "people",
        ("tasks", "completed_by"): "people",
    }
)


class SchemaMemoryError(ValueError):
    pass


def compact_schema(schema):
    """Only metadata needed for matching, never formulas or record values."""
    return {
        "tables": [
            {
                "id": t["id"],
                "name": t["name"],
                "fields": [
                    {
                        "id": f["id"],
                        "name": f["name"],
                        "type": f["type"],
                        "options": {
                            **(
                                {"linkedTableId": f["options"]["linkedTableId"]}
                                if f.get("options", {}).get("linkedTableId")
                                else {}
                            ),
                            **(
                                {
                                    "choices": [
                                        {"id": c.get("id"), "name": c["name"]}
                                        for c in f["options"]["choices"]
                                    ]
                                }
                                if "choices" in f.get("options", {})
                                else {}
                            ),
                        },
                    }
                    for f in t.get("fields", [])
                ],
            }
            for t in schema.get("tables", [])
        ]
    }


def schema_hash(schema):
    data = compact_schema(schema)
    data["tables"].sort(key=lambda t: t["id"])
    for t in data["tables"]:
        t["fields"].sort(key=lambda f: f["id"])
        for f in t["fields"]:
            if "choices" in f["options"]:
                f["options"]["choices"].sort(
                    key=lambda c: (c.get("id") or "", c["name"])
                )
    return hashlib.sha256(
        json.dumps(data, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()


def _find(items, target):
    exact = [x for x in items if x["id"] == target]
    hits = exact or [
        x for x in items if normalize_key(x["name"]) == normalize_key(target)
    ]
    return hits[0] if len(hits) == 1 else None


def compatibility(kind, key, field, table_ids):
    # Allow read-only lookup/formula fields as sources for airtable_tracker export.
    if (
        field["type"] in ("formula", "lookup", "multipleSelects")
        and kind == "projects"
        and key
        in {
            "sub_category",
        }
    ):
        return None
    if field["type"] not in WRITABLE:
        return "字段只读或类型不受支持"
    target = LINKS.get((kind, key))
    if target:
        if field["type"] != "multipleRecordLinks" or field.get("options", {}).get(
            "linkedTableId"
        ) != table_ids.get(target):
            return f"须关联 {target} 表"
        return None
    required = REQUIRED_PROJECT_TYPES.get(key) if kind == "projects" else None
    if required and not project_type_matches(key, field["type"], required):
        return f"须为 {required}"
    if key.endswith("_date") and field["type"] != "date":
        return "须为 date"
    if key == "completed" and field["type"] != "checkbox":
        return "须为 checkbox"
    if kind == "tasks" and key == "duration" and field["type"] != "number":
        return "须为 number"
    if kind == "projects" and key == "jira_link" and field["type"] != "url":
        return "须为 url"
    if (
        kind == "projects"
        and key == "next_plm"
        and field["type"] not in {"multilineText", "richText", "singleLineText"}
    ):
        return "须为文本字段"
    if field["type"] == "multipleRecordLinks":
        return "此字段未定义关联语义"
    if kind in {"people", "factories"} or key in {
        "name",
        "text",
        "project_name",
        "sku",
        "tooling",
    }:
        if field["type"] not in {
            "singleLineText",
            "multilineText",
            "richText",
            "singleSelect",
        }:
            return "须为文本或单选字段"
    return None


def reconcile(schema, config, memory=None, *, selections=None, strict=False):
    """Use remembered IDs, never silently redirect deleted IDs to reused names.

    Explicit editor selections are reviewed local bindings. A selection of None
    disables an optional field. Initial exact-name bindings may be learned.
    """
    config = with_base_defaults(config)
    base = config.get("base_id", "")
    if memory and memory.get("base_id") != base:
        raise SchemaMemoryError("映射记忆属于其他 Base，不能复用。")
    memory = memory or {}
    selections = selections or {}
    tables = schema.get("tables", [])
    ids = {}
    table_bindings = {}
    bindings = {}
    rows = []
    warnings = []
    blockers = []
    effective = deepcopy(config)
    effective["field_mapping"] = deepcopy(config.get("field_mapping", {}))
    for kind in DEFAULT_FIELDS:
        prior = memory.get("tables", {}).get(kind)
        override = selections.get("tables", {}).get(kind)
        wanted = (
            override
            or (prior or {}).get("id")
            or config.get(kind + "_table_id")
            or kind
        )
        table = _find(tables, wanted)
        if prior and not override:
            table = next((t for t in tables if t["id"] == prior["id"]), None)
        if not table:
            blockers.append(
                f"表结构映射：{kind} 的表已删除、重建或无法唯一识别，请打开映射记忆核对。"
            )
            continue
        if table["id"] in ids.values():
            blockers.append(f"表结构映射：{kind} 与其他业务表指向同一张表，请核对。")
        ids[kind] = table["id"]
        table_bindings[kind] = {"id": table["id"], "name": table["name"]}
        if prior and prior["name"] != table["name"]:
            warnings.append(
                f"表结构映射：{kind} 改名为 {table['name']}，已沿用稳定表 ID。"
            )
        effective[kind + "_table_id"] = table["id"]
    for kind, defaults in DEFAULT_FIELDS.items():
        used_fields = {}
        table = next((t for t in tables if t["id"] == ids.get(kind)), None)
        bindings[kind] = {}
        effective["field_mapping"].setdefault(kind, {})
        mappings = {**defaults, **config.get("field_mapping", {}).get(kind, {})}
        if kind == "tasks" and memory.get("fields", {}).get(kind, {}).get("completed"):
            mappings.setdefault("completed", "Completed")
        for key, label in mappings.items():
            required = kind == "projects" and key in required_project_types(config)
            problems = blockers if required or strict else warnings
            prior = memory.get("fields", {}).get(kind, {}).get(key)
            selected = selections.get("fields", {}).get(kind, {})
            explicit = key in selected
            field = None
            disabled = False
            status = "尚未匹配"
            if table:
                if explicit:
                    disabled = selected[key] is None
                    field = next(
                        (f for f in table["fields"] if f["id"] == selected[key]), None
                    )
                    if not disabled and not field:
                        problems.append(
                            f"表结构映射：{kind}.{key} 选择的字段已不存在；跳过此字段。"
                        )
                elif prior:
                    disabled = prior.get("disabled", False)
                    field = next(
                        (f for f in table["fields"] if f["id"] == prior.get("id")), None
                    )
                else:
                    field = _find(table["fields"], label) if label else None
                    if not field and kind == "people" and key in {"name", "department"}:
                        field = _find(table["fields"], key.title())
            if disabled:
                bindings[kind][key] = {"disabled": True}
                effective["field_mapping"][kind][key] = None
                status = "已明确停用"
            elif field:
                error = compatibility(kind, key, field, ids)
                if field["id"] in used_fields:
                    error = f"与 {kind}.{used_fields[field['id']]} 重复映射同一字段"
                    blockers.append(f"表结构映射：{kind}.{key} {error}，请核对。")
                used_fields[field["id"]] = key
                changed = prior and (
                    prior.get("type") != field["type"]
                    or prior.get("linked_table_id")
                    != field.get("options", {}).get("linkedTableId")
                )
                if error or (changed and not explicit):
                    status = error or "类型或关联表变化，需重新确认"
                    problems.append(
                        f"表结构映射：{kind}.{key} → {field['name']}：{status}；跳过此字段。"
                    )
                    if prior:
                        bindings[kind][key] = deepcopy(prior)
                else:
                    status = "已确认映射" if explicit else "已匹配"
                    if prior and prior.get("name") != field["name"]:
                        status = "改名已适应（ID 未变）"
                        warnings.append(
                            f"表结构映射：{kind}.{key} 改名为 {field['name']}，已沿用字段 ID。"
                        )
                    bindings[kind][key] = {
                        "id": field["id"],
                        "name": field["name"],
                        "type": field["type"],
                        "linked_table_id": field.get("options", {}).get(
                            "linkedTableId"
                        ),
                    }
                effective["field_mapping"][kind][key] = (
                    None if error or (changed and not explicit) else field["id"]
                )
            elif prior and not explicit:
                status = "记忆中的字段已删除或重建"
                problems.append(
                    f"表结构映射：{kind}.{key} 记忆字段已不存在，不能自动改投同名新字段；跳过此字段。"
                )
                bindings[kind][key] = deepcopy(prior)
                effective["field_mapping"][kind][key] = None
            else:
                effective["field_mapping"][kind][key] = None
                if label:
                    warnings.append(
                        f"表结构映射：{kind}.{key} 尚未匹配；跳过此字段，原值保留在来源与日志。"
                    )
            if (
                kind == "projects"
                and key in required_project_types(config)
                and (not field or disabled)
            ):
                blockers.append(
                    f"表结构映射：Projects.{key} 为必需字段，尚未建立有效映射。"
                )
            rows.append(
                {
                    "kind": kind,
                    "key": key,
                    "label": label,
                    "table_id": ids.get(kind),
                    "field_id": field["id"] if field else None,
                    "field_name": field["name"] if field else "",
                    "type": field["type"] if field else "",
                    "status": status,
                }
            )
    next_memory = {
        "version": 1,
        "base_id": base,
        "tables": table_bindings,
        "fields": bindings,
        "schema_hash": schema_hash(schema),
        "schema": compact_schema(schema),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    old_hash = memory.get("schema_hash")
    if old_hash and old_hash != next_memory["schema_hash"]:
        warnings.insert(
            0,
            "表结构映射：检测到 Airtable 结构变化，已重新核对字段类型、关联目标与当前选项。",
        )
    return {
        "config": effective,
        "table_ids": ids,
        "memory": next_memory,
        "rows": rows,
        "warnings": list(dict.fromkeys(warnings)),
        "blockers": list(dict.fromkeys(blockers)),
    }


class SchemaMemoryStore:
    def __init__(self, directory):
        self.directory = Path(directory)

    def path(self, base_id):
        return self.directory / (hashlib.sha256(base_id.encode()).hexdigest() + ".json")

    def load(self, base_id):
        path = self.path(base_id)
        if not path.exists():
            return None
        try:
            if path.stat().st_size > 4 * 1024 * 1024:
                raise ValueError("oversize")
            value = json.loads(path.read_text(encoding="utf-8"))
            if value.get("version") != 1 or value.get("base_id") != base_id:
                raise ValueError("scope/version")
            if not isinstance(value.get("tables"), dict) or not isinstance(
                value.get("fields"), dict
            ):
                raise ValueError("shape")
            for kind, table in value["tables"].items():
                if kind not in DEFAULT_FIELDS or not isinstance(table, dict):
                    raise ValueError("table")
                if not all(
                    isinstance(table.get(k), str) and table[k] for k in ("id", "name")
                ):
                    raise ValueError("table identity")
            for kind, fields in value["fields"].items():
                if kind not in DEFAULT_FIELDS or not isinstance(fields, dict):
                    raise ValueError("fields")
                for key, binding in fields.items():
                    if not isinstance(key, str) or not isinstance(binding, dict):
                        raise ValueError("binding")
                    if binding == {"disabled": True}:
                        continue
                    if not all(
                        isinstance(binding.get(k), str) and binding[k]
                        for k in ("id", "name", "type")
                    ):
                        raise ValueError("field identity")
                    if binding.get("linked_table_id") is not None and not isinstance(
                        binding["linked_table_id"], str
                    ):
                        raise ValueError("link")
            return value
        except (OSError, ValueError, TypeError, AttributeError):
            raise SchemaMemoryError(
                "映射记忆损坏或版本不支持，已停止复用；请在映射记忆中重建。"
            ) from None

    def save(self, memory):
        # Only emit the structured record produced by reconcile, not caller config.
        allowed = {
            k: memory[k]
            for k in (
                "version",
                "base_id",
                "tables",
                "fields",
                "schema_hash",
                "schema",
                "updated_at",
            )
        }
        self.directory.mkdir(parents=True, exist_ok=True)
        _atomic_json(self.path(memory["base_id"]), allowed)
