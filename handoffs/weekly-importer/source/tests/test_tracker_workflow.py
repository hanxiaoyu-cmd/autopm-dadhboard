"""The workbook handoff must read cloud state after a successful sync."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from autopm.airtable import AirtableError
from autopm.schema_memory import SchemaMemoryError, SchemaMemoryStore, reconcile
from autopm.tracker import export_tracker, read_tracker
from autopm.workflow import prepare_airtable_tracker, prepare_preview
from autopm.sync import apply_plan
from autopm.workbook import WorkbookError
from test_schema_memory import PreviewClient
from test_sync import fixture
from test_tracker import tracker_fixture


class TrackerWorkflowTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.source = self.root / "tracker.xlsx"
        tracker_fixture(self.source)
        snapshot, self.report = fixture()
        self.client = PreviewClient(snapshot)
        self.config = {"base_id": "appTest", "airtable_token": "secret-pat", "deepseek_api_key": "secret-model"}
        self.store = SchemaMemoryStore(self.root / "memory")

    def test_after_cloud_apply_uses_reread_values_not_uploaded_candidates(self):
        plan, effective = prepare_preview(self.client, self.report, self.config, self.store)
        result = apply_plan(self.client, plan, self.root / "cloud-log")
        self.assertEqual(result["status"], "completed")
        # Represents a cloud automation / accepted value that differs from the upload.
        self.client.data["records"]["tbl_projects"][0]["fields"]["fld_projects_project_name"] = "Cloud final value"
        before_reads, before_writes = self.client.snapshot_calls, deepcopy(self.client.writes)
        local = prepare_airtable_tracker(self.client, self.source, effective, self.store, project_ids=["AB-123"])
        self.assertEqual(self.client.snapshot_calls, before_reads + 1)
        self.assertEqual(self.client.writes, before_writes)
        name = next(row for row in local["changes"] if row["semantic"] == "project_name")
        self.assertEqual(name["after"], "Cloud final value")
        self.assertNotEqual(name["after"], self.report["projects"][0]["fields"]["project_name"])
        output = self.root / "updated.xlsx"
        export_tracker(local, output)
        self.assertEqual(read_tracker(output)["cells"]["B2"], "Cloud final value")
        self.assertEqual(read_tracker(self.source)["cells"]["B2"], "Old name")
        saved = Path(str(output) + ".autopm.json").read_text(encoding="utf-8")
        self.assertNotIn("secret-pat", saved)
        self.assertNotIn("secret-model", saved)
        again = prepare_airtable_tracker(self.client, output, effective, self.store, project_ids=["AB-123"])
        self.assertFalse(again["changes"])

    def test_wrong_base_cannot_read_or_export(self):
        self.client.base_id = "appOther"
        with self.assertRaisesRegex(AirtableError, "数据库不一致"):
            prepare_airtable_tracker(self.client, self.source, self.config, self.store)
        self.assertEqual(self.client.snapshot_calls, 0)
        self.assertFalse(self.client.writes)

    def test_deleted_mapped_field_blocks_before_record_read_and_preserves_memory(self):
        memory = reconcile(self.client.data["schema"], self.config)["memory"]
        self.store.save(memory)
        field = next(f for f in self.client.data["schema"]["tables"][0]["fields"] if f["id"] == "fld_projects_project_name")
        field["id"] = "fld_recreated"
        with self.assertRaises(SchemaMemoryError):
            prepare_airtable_tracker(self.client, self.source, self.config, self.store)
        self.assertEqual(self.client.snapshot_calls, 0)
        self.assertEqual(self.store.load("appTest"), memory)

    def test_read_failure_cannot_fall_back_to_old_snapshot_or_change_workbook(self):
        before = self.source.read_bytes()
        with patch.object(self.client, "snapshot", side_effect=AirtableError("读取超时")):
            with self.assertRaises(AirtableError):
                prepare_airtable_tracker(self.client, self.source, self.config, self.store)
        self.assertEqual(self.source.read_bytes(), before)
        self.assertFalse(self.client.writes)
        self.assertIsNone(self.store.load("appTest"))

    def test_partial_or_cross_base_snapshot_is_rejected(self):
        for change in (lambda data: data.update(base_id="appWrong"),
                       lambda data: data["records"].pop("tbl_tasks")):
            with self.subTest(change=change):
                data = deepcopy(self.client.data)
                change(data)
                with patch.object(self.client, "snapshot", return_value=data), self.assertRaises(AirtableError):
                    prepare_airtable_tracker(self.client, self.source, self.config, self.store)

    def test_tracker_mutation_during_network_read_rejects_preview(self):
        original = self.client.snapshot
        def changed(*args, **kwargs):
            value = original(*args, **kwargs)
            tracker_fixture(self.source, reordered=True)
            return value
        with patch.object(self.client, "snapshot", side_effect=changed), self.assertRaisesRegex(WorkbookError, "变化"):
            prepare_airtable_tracker(self.client, self.source, self.config, self.store)

    def test_empty_scope_never_expands_to_all_projects(self):
        local = prepare_airtable_tracker(self.client, self.source, self.config, self.store, project_ids=[])
        self.assertFalse(local["changes"])
        self.assertEqual(local["source_projects"], 0)


if __name__ == "__main__":
    unittest.main()
