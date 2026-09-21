"""Regression coverage for switching verified bases in the shared preview flow."""
import copy
from pathlib import Path
import tempfile
import unittest

from autopm.schema_memory import SchemaMemoryStore
from autopm.sync import apply_plan
from autopm.weekly_remark import read_weekly_remark
from autopm.workflow import prepare_preview
from test_sync import FakeClient, fixture


class ProfileClient(FakeClient):
    def __init__(self, snapshot):
        super().__init__(snapshot)
        self.base_id = snapshot["base_id"]

    def get_schema(self):
        return copy.deepcopy(self.data["schema"])

    def snapshot(self, overrides=None, **kwargs):
        return super().snapshot(overrides)


class StorageProfileWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = SchemaMemoryStore(Path(self.temp.name) / "memory")
        self.config = {
            "project_report_storage": "engineering_remark",
            "project_report_storage_base_id": "appCopy",
            "project_report_storage_by_base": {
                "appCopy": "engineering_remark", "appMain": "engineering_remark"},
            "field_mapping": {"projects": {
                "current_progress": "fld_projects_current_progress",
                "report_date": None, "update_this_week": "fld_projects_update_this_week"}},
        }

    def fixture(self, base="appMain"):
        snapshot, report = fixture()
        snapshot["base_id"] = base
        table = snapshot["schema"]["tables"][0]
        table["fields"] = [f for f in table["fields"] if f["id"] not in {
            "fld_projects_report_date"}]
        field = next(f for f in table["fields"] if f["id"] == "fld_projects_current_progress")
        field.update(name="Engineering remark(Manual)", type="richText")
        current = snapshot["records"]["tbl_projects"][0]["fields"]
        current.pop("fld_projects_report_date")
        current["fld_projects_current_progress"] = "Keep existing manual notes."
        report["projects"][0]["fields"].update(
            current_progress="EB2 completed", update_this_week="Ready for pilot", jira_total="0")
        return ProfileClient(snapshot), report, {**self.config, "base_id": base}

    def test_copy_main_copy_preview_write_and_repeat_use_each_base_memory(self):
        clients = {}
        for base in ("appCopy", "appMain", "appCopy"):
            with self.subTest(base=base):
                fresh, report, config = self.fixture(base)
                client = clients.setdefault(base, fresh)
                plan, effective = prepare_preview(client, report, config, self.store)
                self.assertFalse(plan["blockers"], plan["blockers"])
                self.assertEqual(effective["base_id"], base)
                if client.writes:
                    self.assertFalse(plan["changes"])
                    continue
                self.assertTrue(plan["changes"])
                self.assertEqual(plan["project_guards"][0]["date_storage"], "engineering_remark")
                result = apply_plan(client, plan, Path(self.temp.name) / base)
                self.assertEqual(result["status"], "completed")
                remark = client.data["records"]["tbl_projects"][0]["fields"]["fld_projects_current_progress"]
                self.assertTrue(remark.startswith("Keep existing manual notes."))
                stored = read_weekly_remark(remark)
                self.assertEqual(stored["report_date"], report["report_date"])
                cloud=client.data['records']['tbl_projects'][0]['fields']
                self.assertEqual(cloud['fld_projects_update_this_week'], "Ready for pilot")
                self.assertEqual(cloud['fld_projects_jira_summary'], "Total: 0")
                again, _ = prepare_preview(client, report, config, self.store)
                self.assertFalse(again["changes"])
        for base in clients:
            self.assertEqual(self.store.load(base)["base_id"], base)
        self.assertNotEqual(self.store.path("appCopy"), self.store.path("appMain"))

    def test_unknown_base_retains_missing_date_blocker_without_reading_records(self):
        client, report, config = self.fixture("appUnknown")
        plan, _ = prepare_preview(client, report, config, self.store)
        self.assertTrue(any("report_date" in item for item in plan["blockers"]))
        self.assertFalse(any("update_this_week" in item for item in plan["blockers"]))
        self.assertFalse(plan["changes"])
        self.assertEqual(client.snapshot_calls, 0)
        self.assertFalse(client.writes)

    def test_explicit_normal_profile_requires_separate_report_columns(self):
        client, report, config = self.fixture()
        config["project_report_storage_base_id"] = "appMain"
        config["project_report_storage_by_base"] = {"appMain": "normal"}
        plan, _ = prepare_preview(client, report, config, self.store)
        self.assertTrue(any("report_date" in item for item in plan["blockers"]))
        self.assertFalse(plan["changes"])
        self.assertEqual(client.snapshot_calls, 0)

    def test_storage_profiles_do_not_bypass_deleted_or_changed_binding_guards(self):
        for mutation in ("deleted", "type_changed"):
            with self.subTest(mutation=mutation):
                client, report, config = self.fixture()
                store = SchemaMemoryStore(Path(self.temp.name) / mutation)
                before, _ = prepare_preview(client, report, config, store)
                self.assertFalse(before["blockers"])
                memory = store.load("appMain")
                fields = client.data["schema"]["tables"][0]["fields"]
                if mutation == "deleted":
                    field = next(f for f in fields if f["id"] == "fld_projects_project_id")
                    field["id"] = "fld_recreated_same_name"
                else:
                    field = next(f for f in fields if f["id"] == "fld_projects_current_progress")
                    field["type"] = "multilineText"
                reads = client.snapshot_calls
                blocked, _ = prepare_preview(client, report, config, store)
                self.assertTrue(blocked["blockers"])
                self.assertFalse(blocked["changes"])
                self.assertEqual(client.snapshot_calls, reads)
                self.assertFalse(client.writes)
                self.assertEqual(store.load("appMain"), memory)


if __name__ == "__main__":
    unittest.main()
