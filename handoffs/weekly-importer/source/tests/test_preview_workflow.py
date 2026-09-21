"""Reject inconsistent or incomplete cloud inputs before producing a write plan."""
from copy import deepcopy
import unittest
from unittest.mock import Mock

from autopm.airtable import AirtableError
from autopm.workflow import prepare_preview
from test_sync import FakeClient, fixture


class PreviewClient(FakeClient):
    def __init__(self, snapshot):
        super().__init__(snapshot)
        self.base_id = snapshot["base_id"]
        self.schema_reads = 0
        self.snapshot_transform = lambda snapshot: snapshot

    def get_schema(self):
        self.schema_reads += 1
        return deepcopy(self.data["schema"])

    def snapshot(self, overrides=None, **kwargs):
        return self.snapshot_transform(super().snapshot(overrides))


class PreviewInputValidationTests(unittest.TestCase):
    def setUp(self):
        self.snapshot, self.report = fixture()
        self.client = PreviewClient(self.snapshot)
        self.config = {"base_id": self.client.base_id}
        self.store = Mock()
        self.store.load.return_value = None

    def test_wrong_or_missing_config_base_stops_before_schema_and_memory(self):
        for base_id in ("appOther", "", None):
            with self.subTest(base_id=base_id):
                with self.assertRaisesRegex(AirtableError, "数据库不一致"):
                    prepare_preview(self.client, self.report, {"base_id": base_id}, self.store)
        self.assertEqual(self.client.schema_reads, 0)
        self.assertEqual(self.client.snapshot_calls, 0)
        self.store.load.assert_not_called()
        self.store.save.assert_not_called()
        self.assertFalse(self.client.writes)

    def test_snapshot_base_table_ids_and_schema_must_match_reviewed_connection(self):
        variants = {}
        wrong_base = deepcopy(self.snapshot)
        wrong_base["base_id"] = "appOther"
        variants["base"] = wrong_base
        wrong_tables = deepcopy(self.snapshot)
        wrong_tables["table_ids"]["tasks"] = "tblOtherTasks"
        variants["table_ids"] = wrong_tables
        changed_schema = deepcopy(self.snapshot)
        changed_schema["schema"]["tables"][0]["fields"][0]["type"] = "number"
        variants["schema"] = changed_schema
        malformed_schema = deepcopy(self.snapshot)
        malformed_schema["schema"] = None
        variants["malformed_schema"] = malformed_schema
        variants["missing_snapshot"] = None
        for name, snapshot in variants.items():
            with self.subTest(name=name):
                self.client.snapshot_transform = lambda _, snapshot=snapshot: snapshot
                with self.assertRaisesRegex(AirtableError, "表结构不一致"):
                    prepare_preview(self.client, self.report, self.config, self.store)
        self.store.save.assert_not_called()
        self.assertFalse(self.client.writes)

    def test_each_missing_or_invalid_table_rejects_snapshot_instead_of_creating_records(self):
        # A missing child table must never look like an empty table and produce creates.
        self.report["projects"][0]["tasks"] = [{"name": "EB1", "date": "2026-09-11"}]
        self.report["projects"][0]["issues"] = [{"text": "Sample delay"}]
        for tid in self.snapshot["table_ids"].values():
            for value in (None, {}, "missing"):
                with self.subTest(table=tid, value=value):
                    snapshot = deepcopy(self.snapshot)
                    if value == "missing":
                        snapshot["records"].pop(tid)
                    else:
                        snapshot["records"][tid] = value
                    self.client.snapshot_transform = lambda _, snapshot=snapshot: snapshot
                    with self.assertRaisesRegex(AirtableError, "读取结果不完整"):
                        prepare_preview(self.client, self.report, self.config, self.store)
        for value in (None, [], "missing"):
            with self.subTest(records=value):
                snapshot = deepcopy(self.snapshot)
                if value == "missing":
                    snapshot.pop("records")
                else:
                    snapshot["records"] = value
                self.client.snapshot_transform = lambda _, snapshot=snapshot: snapshot
                with self.assertRaisesRegex(AirtableError, "读取结果不完整"):
                    prepare_preview(self.client, self.report, self.config, self.store)
        self.store.save.assert_not_called()
        self.assertFalse(self.client.writes)

    def test_valid_preview_still_learns_memory_and_accepts_empty_child_tables(self):
        plan, effective = prepare_preview(self.client, self.report, self.config, self.store)
        self.assertFalse(plan["blockers"], plan["blockers"])
        self.assertTrue(plan["changes"])
        self.assertEqual(plan["base_id"], self.config["base_id"])
        self.assertEqual(effective["base_id"], self.config["base_id"])
        self.assertEqual(self.client.snapshot_calls, 1)
        self.store.save.assert_called_once()
        self.assertEqual(self.store.save.call_args.args[0]["base_id"], self.config["base_id"])
        self.assertFalse(self.client.writes)

    def test_structural_blocker_retains_blocked_plan_without_snapshot_or_memory_save(self):
        table = self.client.data["schema"]["tables"][0]
        table["fields"] = [field for field in table["fields"]
                           if field["id"] != "fld_projects_report_date"]
        plan, _ = prepare_preview(self.client, self.report, self.config, self.store)
        self.assertTrue(any("report_date" in blocker for blocker in plan["blockers"]))
        self.assertFalse(plan["changes"])
        self.assertEqual(self.client.schema_reads, 1)
        self.assertEqual(self.client.snapshot_calls, 0)
        self.store.save.assert_not_called()
        self.assertFalse(self.client.writes)


if __name__ == "__main__":
    unittest.main()
