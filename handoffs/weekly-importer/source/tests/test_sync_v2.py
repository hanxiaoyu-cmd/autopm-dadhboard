"""End-to-end report storage migration using the v2 field changes."""
import tempfile
import unittest

from test_sync import fixture, FakeClient
from autopm.schema_memory import reconcile
from autopm.sync import build_plan, apply_plan, _equivalent
from autopm.weekly_remark import merge_weekly_remark, read_weekly_remark


def v2_fixture():
    snapshot, report = fixture()
    config = {"base_id": "appTest", "project_report_storage": "engineering_remark",
              "project_report_storage_base_id": "appTest", "field_mapping": {}}
    removed = {"projects": {"report_date", "capacity", "region", "sub_category"},
               "tasks": {"duration"}, "factories": {"old"}}
    renamed = {"projects": {"current_progress": "Engineering remark(Manual)",
                             "capacity": "LOA-13weeks plan(Manual)"},
               "tasks": {"project": "Projects(Link)"},
               "issues": {"project": "Projects(Link)", "text": "Issue description (Manual)",
                          "record_date": "Record Date (Auto)", "due_date": "Planned close Date (Manual)"},
               "factories": {"code": "Factory code (Manual)"}}
    for table in snapshot["schema"]["tables"]:
        kind = table["name"].lower()
        config["field_mapping"][kind] = {}
        keep = []
        for field in table["fields"]:
            key = field["id"].removeprefix("fld_" + kind + "_")
            if key in removed.get(kind, set()):
                config["field_mapping"][kind][key] = None
                continue
            if key in renamed.get(kind, {}):
                field["name"] = renamed[kind][key]
            if kind == "projects" and key == "current_progress":
                field["type"] = "richText"
            config["field_mapping"][kind][key] = field["id"]
            keep.append(field)
        table["fields"] = keep
    config["field_mapping"]["projects"]["capacity"] = None
    config["field_mapping"]["factories"]["old_name"] = None
    snapshot["records"]["tbl_projects"][0]["fields"].pop("fld_projects_report_date")
    snapshot["records"]["tbl_projects"][0]["fields"]["fld_projects_current_progress"] = "Manual note\n  Keep indentation."
    report["projects"][0]["fields"].update(current_progress="Build on track", update_this_week="Trial passed", capacity="30K per month")
    report["projects"][0]["tasks"] = [{"name": "MP Start", "date": "2026-10-01"}]
    report["projects"][0]["issues"] = [{"text": "Sample delay", "action": "Expedite", "due_date": "2026-09-20"}]
    return snapshot, report, config


class V2SyncTests(unittest.TestCase):
    def test_new_schema_roundtrip_idempotence_and_no_deleted_field_writes(self):
        snapshot, report, config = v2_fixture()
        state = reconcile(snapshot["schema"], config)
        self.assertFalse(state["blockers"], state["blockers"])
        plan = build_plan(report, snapshot, state["config"])
        self.assertFalse(plan["blockers"], plan["blockers"])
        self.assertEqual({c["kind"] for c in plan["changes"]}, {"projects", "tasks", "issues"})
        legal = {f["id"] for t in snapshot["schema"]["tables"] for f in t["fields"]}
        for change in plan["changes"]:
            self.assertLessEqual(set(change["fields"]), legal)
            self.assertNotIn("fld_projects_capacity", change["fields"])
        client = FakeClient(snapshot)
        with tempfile.TemporaryDirectory() as folder:
            result = apply_plan(client, plan, folder)
        self.assertEqual(result["status"], "completed", result)
        remark = client.data["records"]["tbl_projects"][0]["fields"]["fld_projects_current_progress"]
        self.assertTrue(remark.startswith("Manual note\n  Keep indentation."))
        self.assertEqual(read_weekly_remark(remark)["report_date"], "2026-09-07")
        repeated = build_plan(report, client.data, config)
        self.assertFalse(repeated["changes"], repeated)
        report["report_date"] = "2026-09-01"
        stale = build_plan(report, client.data, config)
        self.assertFalse(stale["changes"])
        self.assertTrue(any("stale report" in w for w in stale["warnings"]))

    def test_preflight_blocks_newer_report_and_manual_edits(self):
        for value in ("A concurrent manual edit", merge_weekly_remark("", "2026-09-10", {})):
            with self.subTest(value=value):
                snapshot, report, config = v2_fixture()
                plan = build_plan(report, snapshot, config)
                client = FakeClient(snapshot)
                client.data["records"]["tbl_projects"][0]["fields"]["fld_projects_current_progress"] = value
                with tempfile.TemporaryDirectory() as folder:
                    result = apply_plan(client, plan, folder)
                self.assertEqual(result["status"], "blocked", result)
                self.assertFalse(client.writes)

    def test_remark_guard_rechecks_before_children(self):
        snapshot, report, config = v2_fixture()
        plan = build_plan(report, snapshot, config)
        class ConcurrentClient(FakeClient):
            def get_record(self, table_id, record_id):
                result = super().get_record(table_id, record_id)
                if self.writes and table_id == "tbl_projects":
                    self.mutate_on_read = lambda client: client.data["records"]["tbl_projects"][0]["fields"].update(
                        fld_projects_current_progress="Edited after project write")
                return result
        client = ConcurrentClient(snapshot)
        with tempfile.TemporaryDirectory() as folder:
            result = apply_plan(client, plan, folder)
        self.assertEqual(result["status"], "partial", result)
        self.assertEqual(len(client.writes), 1)

    def test_rollback_to_original_remark_after_project_write_blocks_children(self):
        snapshot, report, config = v2_fixture()
        original = snapshot["records"]["tbl_projects"][0]["fields"]["fld_projects_current_progress"]
        plan = build_plan(report, snapshot, config)
        class RollbackClient(FakeClient):
            def get_record(self, table_id, record_id):
                result = super().get_record(table_id, record_id)
                if self.writes and table_id == "tbl_projects":
                    self.mutate_on_read = lambda client: client.data["records"]["tbl_projects"][0]["fields"].update(
                        fld_projects_current_progress=original)
                return result
        client = RollbackClient(snapshot)
        with tempfile.TemporaryDirectory() as folder:
            result = apply_plan(client, plan, folder)
        self.assertEqual(result["status"], "partial", result)
        self.assertEqual(len(client.writes), 1)

    def test_richtext_newline_normalization_verifies_and_reimports_once(self):
        snapshot, report, config = v2_fixture()
        report["projects"][0]["fields"]["current_progress"] = "First line\nSecond line"
        plan = build_plan(report, snapshot, config)
        class CRLFClient(FakeClient):
            def update_record(self, table_id, record_id, fields):
                fields = dict(fields)
                if "fld_projects_current_progress" in fields:
                    fields["fld_projects_current_progress"] = fields["fld_projects_current_progress"].replace("\n", "\r\n")
                return super().update_record(table_id, record_id, fields)
        client = CRLFClient(snapshot)
        with tempfile.TemporaryDirectory() as folder:
            result = apply_plan(client, plan, folder)
        self.assertEqual(result["status"], "completed", result)
        self.assertFalse(build_plan(report, client.data, config)["changes"])

    def test_actual_richtext_marker_escape_and_terminal_newline_roundtrip(self):
        snapshot, report, config = v2_fixture()
        plan = build_plan(report, snapshot, config)
        class RichTextClient(FakeClient):
            def update_record(self, table_id, record_id, fields):
                fields = dict(fields)
                if "fld_projects_current_progress" in fields:
                    fields["fld_projects_current_progress"] = fields["fld_projects_current_progress"].replace(
                        "END_PROGRESS", r"END\_PROGRESS") + "\n"
                return super().update_record(table_id, record_id, fields)
        client = RichTextClient(snapshot)
        with tempfile.TemporaryDirectory() as folder:
            result = apply_plan(client, plan, folder)
            self.assertEqual(result["status"], "completed", result)
            write_count = len(client.writes)
            resumed = apply_plan(client, plan, folder)
            self.assertEqual(resumed["status"], "completed", resumed)
            self.assertEqual(len(client.writes), write_count)
        repeated = build_plan(report, client.data, config)
        self.assertFalse(repeated["blockers"], repeated)
        self.assertFalse(repeated["changes"], repeated)

    def test_richtext_comparison_still_detects_prose_history_and_date_edits(self):
        original = merge_weekly_remark("Manual A_B", "2026-09-07", {"current_progress": "Text A_B"})
        for altered in (original.replace("Text A_B", "Text A\\_B"),
                        original.replace("Manual A_B", "Manual A\\_B"),
                        original.replace("2026-09-07", "2026-09-08"),
                        original.replace("Text", "Edited"), original + "\n\n"):
            with self.subTest(altered=altered):
                self.assertFalse(_equivalent(original, altered, {"type": "richText"}))
        self.assertFalse(_equivalent("Manual", "Manual\n", {"type": "richText"}))
        self.assertFalse(_equivalent(original, original + "\n", {"type": "multilineText"}))
        unfenced = original + "\n```"
        self.assertTrue(_equivalent(unfenced, unfenced + "\n", {"type": "richText"}))

    def test_richtext_plan_writes_plain_source_and_verifies_terminal_lf(self):
        snapshot, report, config = v2_fixture()
        source = "1. A\n2. B\n2. C\n3. D\n4. E"
        report["projects"][0]["fields"]["current_progress"] = source
        plan = build_plan(report, snapshot, config)
        project = next(change for change in plan["changes"] if change["kind"] == "projects")
        value = project["fields"]["fld_projects_current_progress"]
        original = snapshot["records"]["tbl_projects"][0]["fields"]["fld_projects_current_progress"]
        self.assertTrue(value.startswith(original + "\n\n--- 2026-09-07 ---\n"))
        self.assertTrue(value.endswith(source))
        class TerminalLFClient(FakeClient):
            def update_record(self, table_id, record_id, fields):
                fields = dict(fields)
                if "fld_projects_current_progress" in fields:
                    fields["fld_projects_current_progress"] += "\n"
                return super().update_record(table_id, record_id, fields)
        client = TerminalLFClient(snapshot)
        with tempfile.TemporaryDirectory() as folder:
            result = apply_plan(client, plan, folder)
        self.assertEqual(result["status"], "completed", result)
        actual = client.data["records"]["tbl_projects"][0]["fields"]["fld_projects_current_progress"]
        self.assertEqual(read_weekly_remark(actual)["fields"]["current_progress"], source)
        self.assertFalse(build_plan(report, client.data, config)["changes"])
        self.assertFalse(_equivalent(value, actual + "\n", {"type": "richText"}))

    def test_legacy_requirements_and_base_scope_are_preserved(self):
        snapshot, report, config = v2_fixture()
        config["base_id"] = "anotherBase"
        self.assertTrue(reconcile(snapshot["schema"], config)["blockers"])
        self.assertTrue(build_plan(report, snapshot, config)["blockers"])

    def test_richtext_does_not_bypass_explicit_type_change_review(self):
        snapshot, _ = fixture()
        memory = reconcile(snapshot["schema"], {"base_id": "appTest"})["memory"]
        field = next(f for t in snapshot["schema"]["tables"] for f in t["fields"]
                     if f["id"] == "fld_projects_current_progress")
        field["type"] = "richText"
        state = reconcile(snapshot["schema"], {"base_id": "appTest"}, memory)
        self.assertFalse(state['blockers'])
        self.assertIsNone(state['config']['field_mapping']['projects']['current_progress'])
        state = reconcile(snapshot["schema"], {"base_id": "appTest"}, memory,
                          selections={"fields": {"projects": {"current_progress": field["id"]}}})
        self.assertFalse(state["blockers"], state["blockers"])
