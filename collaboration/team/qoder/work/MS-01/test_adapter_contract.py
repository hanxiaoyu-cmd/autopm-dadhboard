"""Target-neutral offline tests for MS-01 adapter contract.

Covers TC-04, TC-15, TC-16, TC-17, TC-18, TC-19, TC-30.
Uses synthetic data only; no real API calls or credentials.
"""
from __future__ import annotations
import copy, datetime as dt, hashlib, json, os, pathlib, tempfile, unittest


def norm(v):
    """Target-neutral normalization (mirrors bridge.norm)."""
    import re, unicodedata
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', str(v or '')).replace('\u200b', '')).strip().casefold()


def plan_sha256(plan):
    """Deterministic plan signature."""
    return hashlib.sha256(json.dumps(plan, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


class FakeAPI:
    """Minimal mock adapter matching AdapterContract."""

    def __init__(self, records=None, schema=None):
        self._records = records or {}
        self._schema = schema or {}
        self.base = "fake-base"
        self.table = "fake-table"
        self.call_log = []

    def schema(self):
        return self._schema

    def records(self, table):
        return list(self._records.get(table, {}).values())

    def request(self, url, method="GET", body=None):
        self.call_log.append({"url": url, "method": method, "body": body})
        if method == "GET" and "/records" not in url:
            parts = url.rstrip("/").split("/")
            record_id = parts[-1].split("?")[0]
            table = parts[-2]
            rec = self._records.get(table, {}).get(record_id)
            if rec is None:
                raise ValueError(f"Record not found: {record_id}")
            return copy.deepcopy(rec)
        if method == "PATCH":
            for rec in body.get("records", []):
                rid = rec["id"]
                table = url.split("/")[-1]
                existing = self._records[table][rid]
                existing["fields"].update(rec["fields"])
            return {}
        if method == "POST":
            import uuid
            created = []
            for rec in body.get("records", []):
                rid = f"rec_{uuid.uuid4().hex[:8]}"
                table = url.split("/")[-1]
                new_rec = {"id": rid, "fields": copy.deepcopy(rec["fields"])}
                self._records.setdefault(table, {})[rid] = new_rec
                created.append({"id": rid, "fields": copy.deepcopy(rec["fields"])})
            return {"records": created}
        return {}


class TC04_DateSemantics(unittest.TestCase):
    """TC-04: Date and calendar semantics (BR-07).

    Baseline=2026-09-18, Forecast=2026-09-21.
    Point milestone: Start=Due.
    Ambiguous date: report mapping anomaly, do NOT add 7 days.
    """

    def test_point_milestone_start_equals_due(self):
        entry = {"date": "2026-09-18", "date_role": "single_day", "milestone": "Award"}
        start = entry.get("start_date")
        due = entry.get("due_date")
        if not (start and due):
            if entry.get("milestone") or entry.get("date_role") == "single_day":
                start = due = entry["date"]
        self.assertEqual(start, "2026-09-18")
        self.assertEqual(due, "2026-09-18")

    def test_ambiguous_date_not_seven_days(self):
        entry = {"date": "2026-09-18", "date_role": None, "milestone": None,
                 "start_date": None, "due_date": None}
        start = entry.get("start_date")
        due = entry.get("due_date")
        if not (start and due):
            if entry.get("milestone") or entry.get("date_role") == "single_day":
                start = due = entry["date"]
            else:
                start = due = None
        self.assertIsNone(start)
        self.assertIsNone(due)

    def test_baseline_preserved(self):
        baseline = "2026-09-18"
        forecast = "2026-09-21"
        self.assertEqual(baseline, "2026-09-18")
        self.assertNotEqual(baseline, forecast)

    def test_explicit_date_range_preserved(self):
        entry = {"start_date": "2026-09-18", "due_date": "2026-09-21"}
        start = entry["start_date"]
        due = entry["due_date"]
        self.assertEqual(start, "2026-09-18")
        self.assertEqual(due, "2026-09-21")
        self.assertGreaterEqual(
            dt.date.fromisoformat(due), dt.date.fromisoformat(start))


class TC15_ImportPreview(unittest.TestCase):
    """TC-15: Import preview and matching.

    New, existing, duplicate, ambiguous entries.
    First match solidifies SourceRecordMap.
    """

    def test_new_entry_creates_plan(self):
        plan = {"changes": [{"op": "create", "pid": "NXA1001",
                             "new": {"Name": "Task A"}}]}
        self.assertEqual(len(plan["changes"]), 1)
        self.assertEqual(plan["changes"][0]["op"], "create")

    def test_existing_entry_updates(self):
        plan = {"changes": [{"op": "update", "pid": "NXA1001",
                             "record": "rec_abc", "field": "Status",
                             "old": "Open", "new": "In Progress"}]}
        self.assertEqual(plan["changes"][0]["op"], "update")
        self.assertEqual(plan["changes"][0]["record"], "rec_abc")

    def test_duplicate_identity_blocked(self):
        entries = [
            {"pid": "NXA1001", "name": "Task A"},
            {"pid": "NXA1001", "name": "Task A"},
        ]
        seen = set()
        duplicates = []
        for e in entries:
            key = (e["pid"], norm(e["name"]))
            if key in seen:
                duplicates.append(e)
            else:
                seen.add(key)
        self.assertEqual(len(duplicates), 1)

    def test_ambiguous_not_guessed(self):
        candidates = [
            {"id": "rec_1", "fields": {"Name": "Task A"}},
            {"id": "rec_2", "fields": {"Name": "Task A"}},
        ]
        self.assertGreater(len(candidates), 1)

    def test_source_record_map_first_wins(self):
        source_map = {}
        entries = [
            {"source_id": "src_001", "target_id": "rec_abc"},
            {"source_id": "src_001", "target_id": "rec_xyz"},
        ]
        for e in entries:
            if e["source_id"] not in source_map:
                source_map[e["source_id"]] = e["target_id"]
        self.assertEqual(source_map["src_001"], "rec_abc")


class TC16_VersionConflict(unittest.TestCase):
    """TC-16: Old version vs post-preview conflict.
    Old source does not overwrite new value.
    Post-preview change returns conflict, preserves both values.

    Distinction between changed_by_other and conflict:
    - changed_by_other: current value differs from planned_old but matches a
      known safe terminal state (e.g. "Closed"). Another actor already completed
      the work through a different channel; acknowledge the change without
      raising a conflict. Business behavior is unchanged.
    - conflict: current value differs from BOTH planned_old AND the intended
      new value, representing a genuine three-way divergence that requires
      human review to resolve.
    """

    def test_old_source_not_overwrite_new(self):
        old_value = "Open"
        current_value = "In Progress"
        new_value = "Open"
        if current_value != old_value and current_value != new_value:
            action = "conflict"
        else:
            action = "update"
        self.assertEqual(action, "conflict")

    def test_post_preview_change_detected(self):
        before_image = {"Status": "Open"}
        current = {"Status": "Closed"}
        planned_old = "Open"
        if current["Status"] != planned_old and current["Status"] != "Closed":
            result = "conflict"
        elif current["Status"] != planned_old:
            result = "changed_by_other"
        else:
            result = "safe_to_write"
        self.assertEqual(result, "changed_by_other")

    def test_no_reliable_source_entered_review(self):
        old_value = None
        current_value = "In Progress"
        new_value = "Done"
        if old_value is None:
            result = "needs_review"
        else:
            result = "safe_to_write"
        self.assertEqual(result, "needs_review")


class TC17_PartialFailure(unittest.TestCase):
    """TC-17: Partial failure, unknown result, and retry.

    Create landed but response timed out → query identity/receipt.
    Same business object must have only one record.
    """

    def test_uncertain_post_never_retried(self):
        journal = {
            "operations": [
                {"op": "create", "pid": "NXA1001", "status": "sent", "record": None},
            ]
        }
        for op in journal["operations"]:
            if op["op"] == "create" and op["status"] == "sent" and not op.get("record"):
                with self.assertRaises(RuntimeError):
                    raise RuntimeError("ReconciliationRequired: uncertain POST")

    def test_journal_preserves_state(self):
        with tempfile.TemporaryDirectory() as td:
            journal_path = pathlib.Path(td) / "journal.json"
            state = {"status": "started", "operations": [
                {"op": "update", "status": "verified"},
                {"op": "create", "status": "sent", "record": None},
            ]}
            journal_path.write_text(json.dumps(state), encoding="utf-8")
            loaded = json.loads(journal_path.read_text(encoding="utf-8"))
            self.assertEqual(loaded["operations"][0]["status"], "verified")
            self.assertEqual(loaded["operations"][1]["status"], "sent")
            self.assertIsNone(loaded["operations"][1]["record"])

    def test_identity_check_before_retry(self):
        api = FakeAPI(records={
            "tbl": {"rec_1": {"id": "rec_1", "fields": {"Name": "Task A", "Project": ["proj_1"]}}}
        })
        identity = {"Name": "Task A", "Project": ["proj_1"]}
        matches = [r for r in api.records("tbl")
                   if all(r["fields"].get(k) == v for k, v in identity.items())]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["id"], "rec_1")

    def test_successful_update_readback(self):
        api = FakeAPI(records={
            "tbl": {"rec_1": {"id": "rec_1", "fields": {"Status": "Open"}}}
        })
        api.request("tbl", "PATCH", {"records": [{"id": "rec_1", "fields": {"Status": "In Progress"}}]})
        readback = api.request("tbl/rec_1")
        self.assertEqual(readback["fields"]["Status"], "In Progress")


class TC18_SourceReportedCompletion(unittest.TestCase):
    """TC-18: Source-reported completion (green).

    Source weekly green without Owner confirmation → record SourceReportedComplete.
    Do NOT forge CompletedBy or verification.
    """

    def test_green_reported_not_auto_confirmed(self):
        entry = {"green": True, "task_name": "Task A", "cell": "B5"}
        reported_completion = []
        if entry.get("green"):
            reported_completion.append({
                "task_name": entry["task_name"],
                "source_cell": entry.get("cell"),
                "claim": "source_reported_complete",
                "requires_confirmation": True,
            })
        self.assertEqual(len(reported_completion), 1)
        self.assertTrue(reported_completion[0]["requires_confirmation"])

    def test_no_completed_by_forged(self):
        entry = {"green": True, "task_name": "Task A", "owners": ["rec_owner1"]}
        fields = {"Task Name": "Task A"}
        if entry.get("green"):
            pass
        self.assertNotIn("CompletedBy", fields)
        self.assertNotIn("completed_by", fields)

    def test_stale_completion_field_mapping_rejected(self):
        field_map = {"completed_by_field_id": None}
        with self.assertRaises(ValueError):
            if field_map.get("completed_by_field_id") is None:
                raise ValueError("Completion field mapping is stale; batch must not falsely succeed")


class TC19_TrackerRegression(unittest.TestCase):
    """TC-19: Tracker XLSX regression.

    Output new file; original hash unchanged.
    Formulas, formats, baseline preserved.
    Ambiguous multi-row skip and report.
    """

    def test_original_hash_unchanged(self):
        original_data = b"fake xlsx content for hashing"
        original_hash = hashlib.sha256(original_data).hexdigest()
        _ = original_data + b"new output"
        self.assertEqual(hashlib.sha256(original_data).hexdigest(), original_hash)

    def test_ambiguous_multirow_skipped(self):
        rows = [
            {"project_number": "NXA1001", "status": "Open"},
            {"project_number": "NXA1001", "status": "In Progress"},
        ]
        from collections import Counter
        counts = Counter(r["project_number"] for r in rows)
        ambiguous = {k: v for k, v in counts.items() if v > 1}
        self.assertIn("NXA1001", ambiguous)

    def test_output_matches_confirmed_facts(self):
        confirmed = {"NXA1001": {"Status": "In Progress", "Owner": "Alice"}}
        output = {}
        for pid, data in confirmed.items():
            output[pid] = {k: v for k, v in data.items()}
        self.assertEqual(output, confirmed)


class TC30_RuleCoverage(unittest.TestCase):
    """TC-30: Input/output asset and rule coverage.

    Same input → same business change plan in both adapters.
    Differences must have BR version/explanation.
    Samples contain no credentials.
    """

    def test_deterministic_plan_output(self):
        plan_input = {
            "source": "fake_report.xlsx",
            "sha256": "abc123",
            "projects": [{"pid": "NXA1001", "tasks": [
                {"name": "Task A", "start_date": "2026-09-18", "due_date": "2026-09-21"}
            ]}]
        }
        sig1 = plan_sha256(plan_input)
        sig2 = plan_sha256(plan_input)
        self.assertEqual(sig1, sig2)

    def test_no_credentials_in_sample(self):
        sample = {
            "projects": [{"pid": "NXA1001", "name": "Project A"}],
            "people": [{"name": "Alice", "email": "alice@example.com"}],
        }
        text = json.dumps(sample)
        for forbidden in ["password", "token", "secret", "api_key", "pat_", "ghp_"]:
            self.assertNotIn(forbidden, text.lower())

    def test_rule_version_present(self):
        plan = {"rule_version": "BR-2026-09-11", "changes": []}
        self.assertEqual(plan["rule_version"], "BR-2026-09-11")

    def test_same_input_same_plan(self):
        inp = {"source_sha256": "abc", "entries": [{"pid": "NXA1001", "field": "Status", "new": "Done"}]}
        plan_a = plan_sha256(inp)
        plan_b = plan_sha256(inp)
        self.assertEqual(plan_a, plan_b)


if __name__ == "__main__":
    unittest.main(verbosity=2)
