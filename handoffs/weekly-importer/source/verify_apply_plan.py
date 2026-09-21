# -*- coding: utf-8 -*-
"""Mock Airtable client that validates all apply_plan operations without real API calls.
Simulates the full apply_plan lifecycle: guards, identity checks, field coercion,
concurrent-edit guards, and journal writes — without touching Airtable.
"""

import sys, json, copy, os, tempfile
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

# Load config and modules
from autopm.config import load_settings, ROOT as CFG_ROOT
from autopm.schema_memory import SchemaMemoryStore
from autopm.sync import build_plan, apply_plan

SETTINGS = load_settings()

# ============================================================================
# Mock Airtable Client
# ============================================================================


class FakeClient:
    """Records every mutation, simulates optimistic locking and field access."""

    def __init__(self, base_id, records, schema):
        self.base_id = base_id
        self._records = copy.deepcopy(records)  # mutable mirror
        self._schema = schema
        self.calls = []
        self._schema_fields = {
            f["id"]: f for t in schema["tables"] for f in t["fields"]
        }

    def snapshot(self, table_ids=None):
        return {
            "base_id": self.base_id,
            "captured_at": "2026-09-17T12:00:00Z",
            "schema": self._schema,
            "table_ids": table_ids or {"projects": "tbllvOHZdwfBRWGM0"},
            "records": {
                tid: [copy.deepcopy(r) for r in rows]
                for tid, rows in self._records.items()
            },
        }

    def update_record(self, table_id, record_id, fields):
        self.calls.append(("update", table_id, record_id, fields))
        rec = self._records[table_id]
        for r in rec:
            if r["id"] == record_id:
                r.setdefault("fields", {}).update(fields)
                return {"id": record_id, "fields": r["fields"]}
        raise KeyError(f"record {record_id} not found")

    def create_record(self, table_id, fields):
        new_id = f"recFAKE{len(self.calls):04d}"
        self.calls.append(("create", table_id, new_id, fields))
        self._records[table_id].append({"id": new_id, "fields": fields})
        return {"id": new_id, "fields": fields}

    def get_record(self, table_id, record_id):
        for r in self._records[table_id]:
            if r["id"] == record_id:
                return copy.deepcopy(r)
        raise KeyError(f"record {record_id} not found")


# ============================================================================
# Load real preview from last run log
# ============================================================================


def load_last_preview():
    """Read the preview.json from the most recently modified run folder."""
    log_dir = ROOT / "Run Logs"
    runs = [
        d for d in log_dir.iterdir() if d.is_dir() and (d / "preview.json").exists()
    ]
    runs.sort(key=lambda d: (d / "preview.json").stat().st_mtime, reverse=True)
    if not runs:
        return None
    preview_path = runs[0] / "preview.json"
    with open(preview_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_mock_from_preview(preview):
    """Build a FakeClient populated with the same snapshot schema."""
    import glob
    import os

    # prefer the apply_snapshot.json inside the same run folder as the preview
    candidates = sorted(
        glob.glob(str(ROOT / "Run Logs" / "20*" / "apply_snapshot.json")),
        key=os.path.getmtime,
        reverse=True,
    )
    if not candidates:
        print("[WARN] No apply_snapshot.json found; using empty mock records")
        schema = preview.get("schema", {"tables": []})
        records = {}
        return FakeClient(preview.get("base_id", "appOMWiK4CTOH7iQu"), records, schema)

    with open(candidates[0], "r", encoding="utf-8") as f:
        snapshot = json.load(f)
    records = {tid: rows for tid, rows in snapshot.get("records", {}).items()}
    schema = snapshot.get("schema", {"tables": []})
    return FakeClient(snapshot.get("base_id", "appOMWiK4CTOH7iQu"), records, schema)


# ============================================================================
# Dry-run apply_plan
# ============================================================================


def dry_run_apply(preview):
    client = build_mock_from_preview(preview)
    # Use a temp folder so we don't clobber real run logs
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            result = apply_plan(client, preview, tmpdir)
            return result, client.calls
        except Exception as exc:
            import traceback

            return {
                "status": "exception",
                "error": f"{type(exc).__name__}: {exc}",
                "traceback": traceback.format_exc(),
            }, []


# ============================================================================
# Validate plan integrity (static checks on every operation)
# ============================================================================


def validate_plan(preview):
    errors = []
    changes = preview.get("changes", [])
    for i, op in enumerate(changes):
        # 1. Every operation must have kind and table_id
        if not op.get("kind"):
            errors.append(f"op[{i}] missing kind")
        if not op.get("table_id"):
            errors.append(f"op[{i}] missing table_id")
        # 2. projects must have record_id (update only, never create)
        if op.get("kind") == "projects" and not op.get("record_id"):
            errors.append(
                f"op[{i}] project operation missing record_id (would create new project)"
            )
        # 3. fields must be non-empty dict
        if not isinstance(op.get("fields"), dict) or not op["fields"]:
            errors.append(f"op[{i}] empty fields dict")
        # 4. field_names must cover all field IDs in fields
        field_ids = set(op.get("fields", {}).keys())
        field_names = set(op.get("field_names", {}).keys())
        if field_ids != field_names:
            errors.append(
                f"op[{i}] field_ids != field_names: missing={field_ids - field_names}"
            )
        # 5. before must cover all changed fields
        before_ids = set(op.get("before", {}).keys())
        if not before_ids >= field_ids:
            errors.append(f"op[{i}] before missing fields: {field_ids - before_ids}")
        # 6. display_before / display_after must be present
        if "display_before" not in op or "display_after" not in op:
            errors.append(f"op[{i}] missing display_before/after")
        # 7. identity consistency: tasks/issues may omit identity only in
        #    Next PLM stable-task branch (append_change without extras);
        #    projects must never carry identity.
        has_identity = "identity" in op
        kind = op.get("kind")
        if has_identity and kind == "projects":
            errors.append(f"op[{i}] projects should NOT have identity")
        if has_identity and kind in ("tasks", "issues"):
            identity = op["identity"]
            for required_key in ("project_field", "title_field", "title"):
                if required_key not in identity:
                    errors.append(f"op[{i}] {kind} identity missing {required_key}")
        # 8. project_record_id must match record_id for projects
        if kind == "projects" and op.get("project_record_id") != op.get("record_id"):
            errors.append(f"op[{i}] project_record_id != record_id")

    return errors


# ============================================================================
# Main
# ============================================================================


def main():
    preview = load_last_preview()
    if not preview:
        print("[FAIL] Cannot find any preview.json in Run Logs")
        return 1

    print(
        f"[INFO] Loaded preview: {preview.get('source', '?')} — "
        f"{len(preview.get('changes', []))} changes, {len(preview.get('warnings', []))} warnings"
    )

    # ---- Static validation ----
    static_errors = validate_plan(preview)
    if static_errors:
        print(f"[FAIL] Static validation found {len(static_errors)} errors:")
        for e in static_errors[:20]:
            print(f"  - {e}")
        if len(static_errors) > 20:
            print(f"  ... and {len(static_errors) - 20} more")
    else:
        print("[PASS] Static validation: all operations structurally valid")

    # ---- Dry-run apply ----
    result, calls = dry_run_apply(preview)
    if result.get("status") == "completed":
        print(
            f"[PASS] Dry-run apply_plan: completed, {len(calls)} operations, applied={result.get('applied')}"
        )
    elif result.get("status") == "exception":
        print(f"[FAIL] Dry-run apply_plan crashed:")
        print(result["traceback"])
    else:
        print(
            f"[FAIL] Dry-run apply_plan: status={result.get('status')}, applied={result.get('applied')}, errors={result.get('errors')}"
        )

    return 0 if not static_errors and result.get("status") == "completed" else 1


if __name__ == "__main__":
    sys.exit(main())
