import copy
import json
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from autopm.airtable import UncertainWriteError
from autopm.sync import build_plan, apply_plan, PROJECT_FIELDS, TASK_FIELDS, ISSUE_FIELDS, _atomic_json


def fixture():
    tables = []
    ids = {kind: "tbl_" + kind for kind in ("projects", "tasks", "issues", "people", "factories")}
    mappings = {"projects": {**PROJECT_FIELDS, 'capacity':'Capacity / Forecast (Manual)', 'region':'Region (Manual)'}, "tasks": TASK_FIELDS, "issues": ISSUE_FIELDS,
                "people": {"name": "Person Name (Manual)", "department": "Department (Manual)"},
                "factories": {"name": "Factory Full Name (Manual)", "code": "Factory code", "old": "Factory name (Old)"}}
    links = {("projects", "npi_lead"): "people", ("projects", "npd_lead"): "people", ("projects", "pmo"): "people",
             ("projects", "quality"): "people", ("projects", "factory"): "factories",
             ("tasks", "project"): "projects", ("issues", "project"): "projects",
             ("tasks", "owners"): "people", ("tasks", "completed_by"): "people", ("issues", "owner"): "people"}
    for kind, mapping in mappings.items():
        fs = []
        for key, name in mapping.items():
            typ = "singleLineText"
            opts = {}
            if key.endswith("_date"):
                typ = "date"
            if key in {"current_progress", "update_this_week", "action"}:
                typ = "multilineText"
            if (kind, key) in links:
                typ, opts = "multipleRecordLinks", {"linkedTableId": ids[links[kind, key]]}
            if key == "status":
                typ, opts = "singleSelect", {"choices": [{"name": "On Track"}, {"name": "At Risk"}]}
            if key == "milestone":
                typ, opts = "singleSelect", {"choices": [{"name": n} for n in ["Kick off", "Award", "MP Start", "DQTP report", "P1 BUILD DATE", "EB1", "Previous MP Date", "TRA / ECN DD", "MPRA / ECN"]]}
            if key == "risk":
                typ, opts = "singleSelect", {"choices": [{"name": n} for n in ["Critical", "High", "Medium", "Low"]]}
            if key in {"capacity", "duration"}:
                typ = "number"
            if key == "jira_link":
                typ = "url"
            f = {"id": "fld_" + kind + "_" + key, "name": name, "type": typ}
            if opts:
                f["options"] = opts
            fs.append(f)
        tables.append({"id": ids[kind], "name": kind.title(), "fields": fs})
    snapshot = {"base_id": "appTest", "schema": {"tables": tables}, "table_ids": ids,
                "records": {tid: [] for tid in ids.values()}}
    snapshot["records"][ids["projects"]] = [{"id": "recProject", "fields": {
        "fld_projects_project_id": "AB-123", "fld_projects_project_name": "Existing",
        "fld_projects_report_date": "2026-09-01", "fld_projects_npi_lead": ["recNpi"]}}]
    snapshot["records"][ids["people"]] = [
        {"id": "recNpi", "fields": {"fld_people_name": "Jane Smith", "fld_people_department": "NPI"}},
        {"id": "recOther", "fields": {"fld_people_name": "Jane Doe", "fld_people_department": "Quality"}}]
    snapshot["records"][ids["factories"]] = [
        {"id": "recFactory", "fields": {"fld_factories_name": "Factory One", "fld_factories_code": "F1", "fld_factories_old": "Old Factory"}}]
    report = {"report_date": "2026-09-07", "source": "weekly.xlsx", "projects": [
        {"project_id": " ab- 123 ", "fields": {"project_name": "New project"}, "tasks": [], "issues": [], "source": "Sheet!A4"}]}
    return snapshot, report


class FakeClient:
    base_id = "appTest"

    def __init__(self, snapshot):
        self.data = copy.deepcopy(snapshot)
        self.writes = []
        self.snapshot_calls = 0
        self.list_calls = 0
        self.uncertain = False
        self.mutate_on_read = None

    def snapshot(self, overrides=None):
        self.snapshot_calls += 1
        return copy.deepcopy(self.data)

    def list_records(self, table_id):
        self.list_calls += 1
        return copy.deepcopy(self.data["records"][table_id])

    def get_record(self, table_id, record_id):
        if self.mutate_on_read:
            self.mutate_on_read(self)
            self.mutate_on_read = None
        return copy.deepcopy(next(r for r in self.data["records"][table_id] if r["id"] == record_id))

    def update_record(self, table_id, record_id, fields):
        self.writes.append(("PATCH", table_id, fields))
        row = next(r for r in self.data["records"][table_id] if r["id"] == record_id)
        row["fields"].update(fields)
        return copy.deepcopy(row)

    def create_record(self, table_id, fields):
        self.writes.append(("POST", table_id, fields))
        if self.uncertain:
            raise UncertainWriteError("Unknown create result")
        row = {"id": "recCreated" + str(len(self.writes)), "fields": copy.deepcopy(fields)}
        self.data["records"][table_id].append(row)
        return copy.deepcopy(row)


class SyncTests(unittest.TestCase):
    def test_due_only_ignores_legacy_modes_and_does_not_require_start_field(self):
        for mode in (None, 'start_plus_7', 'due_minus_7', 'due_only'):
            snapshot, report = fixture()
            table = next(t for t in snapshot['schema']['tables'] if t['id'] == 'tbl_tasks')
            table['fields'] = [f for f in table['fields'] if f['id'] not in {'fld_tasks_start_date', 'fld_tasks_duration'}]
            report['projects'][0]['tasks'] = [{'name': 'EB1', 'date': '2026-09-11'}]
            plan = build_plan(report, snapshot, {'task_date_mode': mode})
            self.assertFalse(plan['blockers'], plan['blockers'])
            task = next(c for c in plan['changes'] if c['kind'] == 'tasks')
            self.assertEqual(task['fields']['fld_tasks_due_date'], '2026-09-11')
            self.assertNotIn('fld_tasks_start_date', task['fields'])
            self.assertNotIn('fld_tasks_duration', task['fields'])

    def test_due_update_preserves_start_and_duration_without_triggering_start_automation(self):
        snapshot,report=fixture()
        snapshot['records']['tbl_tasks']=[{'id':'recAward','fields':{
            'fld_tasks_name':'Award','fld_tasks_project':['recProject'],'fld_tasks_milestone':'Award',
            'fld_tasks_start_date':'2026-09-03','fld_tasks_due_date':'2026-09-10','fld_tasks_duration':8}}]
        report['projects'][0]['tasks']=[{'name':'Award','date':'2026-09-11'}]
        plan=build_plan(report,snapshot);op=next(c for c in plan['changes'] if c['kind']=='tasks')
        self.assertNotIn('fld_tasks_start_date',op['fields'])
        self.assertEqual(op['fields']['fld_tasks_due_date'],'2026-09-11')
        self.assertNotIn('fld_tasks_duration',op['fields'])
        class DateAutomationClient(FakeClient):
            def update_record(self,table_id,record_id,values):
                result=super().update_record(table_id,record_id,values)
                if table_id=='tbl_tasks' and 'fld_tasks_start_date' in values:
                    from datetime import date,timedelta
                    row=self.data['records'][table_id][0]
                    row['fields']['fld_tasks_due_date']=(date.fromisoformat(row['fields']['fld_tasks_start_date'])+timedelta(days=row['fields']['fld_tasks_duration']-1)).isoformat()
                return result
        client=DateAutomationClient(snapshot)
        with tempfile.TemporaryDirectory() as folder:result=apply_plan(client,plan,folder)
        self.assertEqual(result['status'],'completed')
        self.assertEqual(client.data['records']['tbl_tasks'][0]['fields']['fld_tasks_start_date'],'2026-09-03')
        self.assertEqual(client.data['records']['tbl_tasks'][0]['fields']['fld_tasks_duration'],8)
        self.assertEqual(build_plan(report,client.data)['changes'],[])
    def test_unique_template_milestone_reuses_record_and_preserves_name(self):
        snapshot, report = fixture()
        snapshot['records']['tbl_tasks'] = [{'id':'recTemplate','fields':{
            'fld_tasks_name':'EB1 - Existing', 'fld_tasks_project':['recProject'],
            'fld_tasks_milestone':'EB1','fld_tasks_start_date':'2026-09-01','fld_tasks_due_date':'2026-09-08'}}]
        report['projects'][0]['tasks']=[{'name':'EB1','date':'2026-09-10'}]
        plan=build_plan(report,snapshot)
        task=next(c for c in plan['changes'] if c['kind']=='tasks')
        self.assertEqual(task['record_id'],'recTemplate')
        self.assertNotIn('fld_tasks_name',task['fields'])
        self.assertEqual(task['fields']['fld_tasks_due_date'],'2026-09-10')
        self.assertNotIn('fld_tasks_start_date',task['fields'])
        client=FakeClient(snapshot)
        with tempfile.TemporaryDirectory() as folder:
            result=apply_plan(client,plan,folder)
        self.assertEqual(result['status'],'completed')
        self.assertEqual(build_plan(report,client.data)['changes'],[])
        self.assertEqual(len(client.data['records']['tbl_tasks']),1)
        changed=FakeClient(snapshot)
        changed.data['records']['tbl_tasks'][0]['fields']['fld_tasks_milestone']='Award'
        with tempfile.TemporaryDirectory() as folder:blocked=apply_plan(changed,plan,folder)
        self.assertEqual(blocked['status'],'blocked')
        self.assertFalse(changed.writes)

    def test_ambiguous_milestone_or_region_never_creates_another_task(self):
        for case in ('duplicate_existing','multiple_sources'):
            snapshot, report=fixture()
            snapshot['records']['tbl_tasks']=[{'id':'recTemplate','fields':{
                'fld_tasks_name':'EB1 (CN)' if case=='different_region' else 'EB1 - Existing',
                'fld_tasks_project':['recProject'],'fld_tasks_milestone':'EB1'}}]
            report['projects'][0]['tasks']=[{'name':'EB1 (VN)','date':'2026-09-10'}]
            if case=='duplicate_existing':
                snapshot['records']['tbl_tasks'].append({'id':'recOtherTask','fields':{
                    'fld_tasks_name':'Other EB1','fld_tasks_project':['recProject'],'fld_tasks_milestone':'EB1'}})
            if case=='multiple_sources':report['projects'][0]['tasks'].append({'name':'EB1 (CN)','date':'2026-09-10'})
            plan=build_plan(report,snapshot)
            self.assertFalse([c for c in plan['changes'] if c['kind']=='tasks'],case)
            self.assertTrue(any('identity is ambiguous' in w for w in plan['warnings']),case)

    def test_distinct_regional_task_can_be_added_and_repeated_without_duplicates(self):
        snapshot,report=fixture()
        snapshot['records']['tbl_tasks']=[{'id':'recCN','fields':{'fld_tasks_name':'EB1 (CN)',
            'fld_tasks_project':['recProject'],'fld_tasks_milestone':'EB1','fld_tasks_start_date':'2026-09-10','fld_tasks_due_date':'2026-09-10','fld_tasks_duration':8}}]
        report['projects'][0]['tasks']=[{'name':'EB1 (VN)','date':'2026-09-10'},{'name':'EB1 (CN)','date':'2026-09-10'}]
        plan=build_plan(report,snapshot);tasks=[c for c in plan['changes'] if c['kind']=='tasks']
        self.assertEqual(len(tasks),1)
        self.assertIsNone(tasks[0]['record_id'])
        client=FakeClient(snapshot)
        with tempfile.TemporaryDirectory() as folder:result=apply_plan(client,plan,folder)
        self.assertEqual(result['status'],'completed')
        self.assertEqual(build_plan(report,client.data)['changes'],[])

    def test_template_sales_market_does_not_invent_factory_scope(self):
        snapshot,report=fixture()
        snapshot['records']['tbl_tasks']=[{'id':'recTemplate','fields':{
            'fld_tasks_name':'EB1 - Dual Source product-US at Junxin V',
            'fld_tasks_project':['recProject'],'fld_tasks_milestone':'EB1'}}]
        report['projects'][0]['tasks']=[{'name':'EB1 (VN)','date':'2026-09-10'},
                                      {'name':'EB1 (CN)','date':'2026-09-11'}]
        plan=build_plan(report,snapshot)
        self.assertFalse([c for c in plan['changes'] if c['kind']=='tasks'])
        self.assertTrue(any('identity is ambiguous' in w for w in plan['warnings']))
        from autopm.sync import _task_scope
        self.assertEqual(_task_scope('EB1 - Product US at Factory VN'),{'VN'})
        self.assertEqual(_task_scope('EB1 (CN) - Product US at Factory VN'),{'CN'})

    def test_new_template_task_after_preview_blocks_duplicate_creation(self):
        snapshot, report=fixture()
        report['projects'][0]['tasks']=[{'name':'EB1','date':'2026-09-10'}]
        plan=build_plan(report,snapshot);client=FakeClient(snapshot)
        client.data['records']['tbl_tasks'].append({'id':'recConcurrentTemplate','fields':{
            'fld_tasks_name':'EB1 - Existing','fld_tasks_project':['recProject'],'fld_tasks_milestone':'EB1'}})
        with tempfile.TemporaryDirectory() as folder:result=apply_plan(client,plan,folder)
        self.assertEqual(result['status'],'blocked')
        self.assertFalse(client.writes)
        self.assertIn('equivalent milestone',result['errors'][0])

    def test_duplicate_source_aliases_are_skipped_before_any_task_write(self):
        snapshot,report=fixture()
        report['projects'][0]['tasks']=[{'name':'MP Start (CN)','date':'2026-09-10'},
                                      {'name':'New MP Start (CN)','date':'2026-09-11'}]
        plan=build_plan(report,snapshot)
        self.assertFalse([c for c in plan['changes'] if c['kind']=='tasks'])
        self.assertTrue(any('duplicate milestone' in w for w in plan['warnings']))

    def test_atomic_log_retries_transient_windows_rename_without_duplicate_write(self):
        import os
        snapshot, report = fixture()
        report["projects"][0]["fields"]["project_name"] = "Updated once"
        client = FakeClient(snapshot)
        rename = os.replace
        failures = []
        def locked_once(source, destination):
            if Path(destination).name == "write_journal.json" and not failures:
                failures.append(True)
                error = PermissionError("temporary scanner lock")
                error.winerror = 32
                raise error
            return rename(source, destination)
        with tempfile.TemporaryDirectory() as folder, patch("autopm.sync.os.replace", side_effect=locked_once), patch("autopm.sync.time.sleep") as sleep:
            result = apply_plan(client, build_plan(report, snapshot), folder)
            self.assertEqual(result["status"], "completed")
            self.assertEqual(len(client.writes), 1)
            sleep.assert_called_once_with(0.05)
            self.assertEqual(json.loads((Path(folder)/"result.json").read_text())["applied"], 1)

    def test_atomic_log_permanent_lock_preserves_old_file_and_fails_bounded(self):
        error = PermissionError("persistent access denied")
        error.winerror = 5
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/"journal.json"
            path.write_text('{"old":true}', encoding="utf-8")
            with patch("autopm.sync.os.replace", side_effect=error) as rename, patch("autopm.sync.time.sleep") as sleep:
                with self.assertRaises(PermissionError):
                    _atomic_json(path, {"new": True})
                self.assertEqual(rename.call_count, 6)
                self.assertEqual(sleep.call_count, 5)
            self.assertEqual(json.loads(path.read_text()), {"old": True})
            self.assertEqual(json.loads(path.with_suffix(".json.tmp").read_text()), {"new": True})

    def test_atomic_log_does_not_retry_unrelated_io_errors(self):
        with tempfile.TemporaryDirectory() as folder, patch("autopm.sync.os.replace", side_effect=OSError("disk failure")) as rename, patch("autopm.sync.time.sleep") as sleep:
            with self.assertRaises(OSError):
                _atomic_json(Path(folder)/"journal.json", {"new": True})
            self.assertEqual(rename.call_count, 1)
            sleep.assert_not_called()

    def test_exact_normalized_identity_nonblank_and_selection(self):
        snapshot, report = fixture()
        report["projects"][0]["fields"].update(region="", status=" on track ", sku=" ab1 ; ab2 ")
        plan = build_plan(report, snapshot)
        self.assertFalse(plan["blockers"])
        change = plan["changes"][0]
        self.assertEqual(change["record_id"], "recProject")
        self.assertEqual(change["fields"]["fld_projects_status"], "On Track")
        self.assertEqual(change["fields"]["fld_projects_sku"], "AB1, AB2")
        self.assertNotIn("fld_projects_region", change["fields"])
        report["projects"][0]["project_id"] = "AB123"
        self.assertEqual(build_plan(report, snapshot)["changes"], [])

    def test_duplicate_project_identity_is_not_guessed(self):
        snapshot, report = fixture()
        snapshot["records"]["tbl_projects"].append({"id": "recDuplicate", "fields": {"fld_projects_project_id": "ab -123"}})
        plan = build_plan(report, snapshot)
        self.assertFalse(plan["changes"])
        self.assertTrue(any("found 2" in w for w in plan["warnings"]))
        report["projects"].append(copy.deepcopy(report["projects"][0]))
        duplicate=build_plan(report, snapshot)
        self.assertFalse(duplicate['blockers'])
        self.assertFalse(duplicate['changes'])
        self.assertTrue(any('duplicate report Project ID' in w for w in duplicate['warnings']))

    def test_per_project_freshness(self):
        snapshot, report = fixture()
        report["projects"][0]["report_date"] = "2026-08-30"
        plan = build_plan(report, snapshot)
        self.assertFalse(plan["changes"])
        self.assertTrue(any("stale" in w for w in plan["warnings"]))

    def test_people_department_and_factory_alias(self):
        snapshot, report = fixture()
        report["projects"][0]["fields"].update(npi_lead="Jane", factory="old factory")
        snapshot["records"]["tbl_projects"][0]["fields"].pop("fld_projects_npi_lead")
        change = build_plan(report, snapshot)["changes"][0]
        self.assertEqual(change["fields"]["fld_projects_npi_lead"], ["recNpi"])
        self.assertEqual(change["fields"]["fld_projects_factory"], ["recFactory"])
        snapshot["records"]["tbl_people"].append({"id": "recAmbiguous", "fields": {"fld_people_name": "Jane Ellis", "fld_people_department": "NPI"}})
        plan = build_plan(report, snapshot)
        self.assertNotIn("fld_projects_npi_lead", plan["changes"][0]["fields"])
        self.assertTrue(any("ambiguous" in w for w in plan["warnings"]))

    def test_unknown_option_is_not_created(self):
        snapshot, report = fixture()
        report["projects"][0]["fields"]["status"] = "Magic new status"
        plan = build_plan(report, snapshot)
        self.assertNotIn("fld_projects_status", plan["changes"][0]["fields"])
        self.assertTrue(any("no option will be created" in w for w in plan["warnings"]))

    def test_missing_required_schema_blocks(self):
        snapshot, report = fixture()
        snapshot["schema"]["tables"][0]["fields"] = [f for f in snapshot["schema"]["tables"][0]["fields"] if f["id"] != "fld_projects_project_id"]
        self.assertTrue(build_plan(report, snapshot)["blockers"])

    def test_task_dates_milestones_owners_and_completion_evidence(self):
        snapshot, report = fixture()
        report["projects"][0]["tasks"] = [
            {"name": "Kick Off Date", "date": "2026-09-02", "completed": True, "source": "Sheet!B4"},
            {"name": "Award", "date": "2026-09-03", "completed": False},
            {"name": "Unusual checkpoint", "date": "2026-09-04", "completed": False}]
        plan = build_plan(report, snapshot, {"require_milestone": False})
        tasks = [c for c in plan["changes"] if c["kind"] == "tasks"]
        self.assertEqual(tasks[0]["fields"]["fld_tasks_due_date"], "2026-09-02")
        self.assertEqual(tasks[0]["fields"]["fld_tasks_milestone"], "Kick off")
        self.assertEqual(tasks[0]["fields"]["fld_tasks_owners"], ["recNpi"])
        self.assertTrue(tasks[0]["completed"])
        self.assertNotIn("fld_tasks_start_date", tasks[1]["fields"])
        self.assertEqual(tasks[1]["fields"]["fld_tasks_due_date"], "2026-09-03")
        self.assertNotIn("fld_tasks_milestone", tasks[2]["fields"])
        self.assertTrue(any("completion retained" in w for w in plan["warnings"]))
        alternative = build_plan(report, snapshot, {"task_date_mode": "due_minus_7"})
        task = next(c for c in alternative["changes"] if c["kind"] == "tasks")
        self.assertNotIn("fld_tasks_start_date", task["fields"])
        self.assertEqual(task["fields"]["fld_tasks_due_date"], "2026-09-02")
        self.assertTrue(build_plan(report, snapshot, {"require_completion_sync": True})["blockers"])

    def test_issues_are_separate_and_idempotent(self):
        snapshot, report = fixture()
        report["projects"][0]["issues"] = [{"text": "Battery delays", "action": "Expedite", "source": "Sheet!C4"}]
        client = FakeClient(snapshot)
        plan = build_plan(report, snapshot)
        self.assertEqual([c["kind"] for c in plan["changes"]], ["projects", "issues"])
        with tempfile.TemporaryDirectory() as folder:
            result = apply_plan(client, plan, folder)
            self.assertEqual(result["status"], "completed", result)
            self.assertTrue(all(op["state"] == "verified" for op in json.loads((Path(folder) / "write_journal.json").read_text())["operations"]))
            replay = apply_plan(client, plan, folder)
            self.assertEqual(replay["applied"], 0)
            self.assertEqual(replay["skipped"], 2)
        report["projects"][0]["issues"][0]["text"] = " battery  DELAYS "
        second = build_plan(report, client.snapshot())
        self.assertFalse(any(c["record_id"] is None for c in second["changes"]))

    def test_regional_mp_start_same_day_and_bare_p1_fixed_milestone(self):
        snapshot, report = fixture()
        report["projects"][0]["tasks"] = [{"name": name, "date": "2026-09-03"}
                                            for name in ["MP Start(CN)", "new MP Start (VN)", "P1", "EB1(CN)", "Previous MP Start Date", "EB3.5"]]
        tasks = [c for c in build_plan(report, snapshot, {"require_milestone": False})["changes"] if c["kind"] == "tasks"]
        self.assertEqual(len(tasks), 6)
        for task in tasks[:2]:
            self.assertEqual(task["fields"]["fld_tasks_milestone"], "MP Start")
            self.assertNotIn("fld_tasks_start_date", task["fields"])
            self.assertEqual(task["fields"]["fld_tasks_due_date"], "2026-09-03")
        self.assertNotEqual(tasks[0]["identity"]["title"], tasks[1]["identity"]["title"])
        self.assertEqual(tasks[2]["fields"]["fld_tasks_milestone"], "P1 BUILD DATE")
        self.assertEqual(tasks[3]["fields"]["fld_tasks_milestone"], "EB1")
        self.assertEqual(tasks[4]["fields"]["fld_tasks_milestone"], "Previous MP Date")
        self.assertNotIn("fld_tasks_milestone", tasks[5]["fields"])
        strict = build_plan(report, snapshot, {'require_milestone':True})
        self.assertEqual(len([c for c in strict["changes"] if c["kind"] == "tasks"]), 5)
        self.assertTrue(any("任务未写入" in w for w in strict["warnings"]))

    def test_multiline_issue_owners_resolve_all_or_none(self):
        snapshot, report = fixture()
        report["projects"][0]["issues"] = [{"text": "Delay", "action": "Investigate", "owner": "Jane Smith\nJane Doe", "risk": "M"}]
        issue = next(c for c in build_plan(report, snapshot)["changes"] if c["kind"] == "issues")
        self.assertEqual(issue["fields"]["fld_issues_owner"], ["recNpi", "recOther"])
        self.assertEqual(issue["fields"]["fld_issues_risk"], "Medium")
        report["projects"][0]["issues"][0]["risk"] = " H "
        high_issue = next(c for c in build_plan(report, snapshot)["changes"] if c["kind"] == "issues")
        self.assertEqual(high_issue["fields"]["fld_issues_risk"], "High")
        report["projects"][0]["issues"][0]["owner"] = "Jane Smith\nUnknown Person"
        plan = build_plan(report, snapshot)
        issue = next(c for c in plan["changes"] if c["kind"] == "issues")
        self.assertNotIn("fld_issues_owner", issue["fields"])
        self.assertTrue(any("Unknown Person" in w for w in plan["warnings"]))

    def test_stale_preview_concurrent_edit_writes_nothing(self):
        snapshot, report = fixture()
        plan = build_plan(report, snapshot)
        client = FakeClient(snapshot)
        client.data["records"]["tbl_projects"][0]["fields"]["fld_projects_project_name"] = "Someone edited"
        with tempfile.TemporaryDirectory() as folder:
            result = apply_plan(client, plan, folder)
        self.assertEqual(result["status"], "blocked")
        self.assertFalse(client.writes)

    def test_immediate_reread_detects_concurrent_edit(self):
        snapshot, report = fixture()
        plan = build_plan(report, snapshot)
        client = FakeClient(snapshot)
        client.mutate_on_read = lambda c: c.data["records"]["tbl_projects"][0]["fields"].update(fld_projects_project_name="Concurrent")
        with tempfile.TemporaryDirectory() as folder:
            result = apply_plan(client, plan, folder)
        self.assertEqual(result["status"], "blocked")
        self.assertFalse(client.writes)

    def test_uncertain_create_journal_prevents_blind_retry(self):
        snapshot, report = fixture()
        report["projects"][0]["issues"] = [{"text": "Delay", "action": "Investigate"}]
        client = FakeClient(snapshot)
        client.uncertain = True
        plan = build_plan(report, snapshot)
        with tempfile.TemporaryDirectory() as folder:
            first = apply_plan(client, plan, folder)
            self.assertEqual(first["status"], "partial")
            journal = json.loads((Path(folder) / "write_journal.json").read_text())
            self.assertEqual(journal["operations"][-1]["state"], "uncertain")
            count = len(client.writes)
            second = apply_plan(client, plan, folder)
            self.assertEqual(second["status"], "blocked")
            self.assertEqual(count, len(client.writes))

    def test_schema_change_blocks_without_write(self):
        snapshot, report = fixture()
        plan = build_plan(report, snapshot)
        client = FakeClient(snapshot)
        next(f for f in client.data['schema']['tables'][0]['fields'] if f['id']=='fld_projects_project_name')['type']='formula'
        with tempfile.TemporaryDirectory() as folder:
            result = apply_plan(client, plan, folder)
        self.assertFalse(client.writes)
        self.assertTrue(result["errors"])

    def test_multiple_creates_use_one_snapshot_without_repeated_table_scans(self):
        snapshot, report = fixture()
        report["projects"][0]["tasks"] = [{"name": name, "date": "2026-09-03"}
                                           for name in ["Award", "MP Start(CN)", "MP Start(VN)"]]
        report["projects"][0]["issues"] = [{"text": "Delay one", "action": "Expedite"},
                                             {"text": "Delay two", "action": "Investigate"}]
        plan = build_plan(report, snapshot)
        client = FakeClient(snapshot)
        with tempfile.TemporaryDirectory() as folder:
            result = apply_plan(client, plan, folder)
        self.assertEqual(result["status"], "completed", result)
        self.assertEqual(client.snapshot_calls, 1)
        self.assertEqual(client.list_calls, 0)
        self.assertEqual(len([write for write in client.writes if write[0] == "POST"]), 5)

    def test_duplicate_child_in_fresh_preflight_blocks_all_writes(self):
        snapshot, report = fixture()
        report["projects"][0]["tasks"] = [{"name": "Award", "date": "2026-09-03"}]
        plan = build_plan(report, snapshot)
        client = FakeClient(snapshot)
        for record_id in ("recDuplicate1", "recDuplicate2"):
            client.data["records"]["tbl_tasks"].append({"id": record_id, "fields": {
                "fld_tasks_name": " aWARD ", "fld_tasks_project": ["recProject"]}})
        with tempfile.TemporaryDirectory() as folder:
            result = apply_plan(client, plan, folder)
        self.assertEqual(result["status"], "blocked")
        self.assertFalse(client.writes)
        self.assertEqual(client.list_calls, 0)
        self.assertTrue(any("Duplicate" in error for error in result["errors"]))

    def test_ambiguous_children_skip_without_blocking_unrelated_reviewed_changes(self):
        snapshot, report = fixture()
        report["projects"][0]["tasks"] = [
            {"name": "Award", "date": "2026-09-03"},
            {"name": " aWard ", "date": "2026-09-04"},
            {"name": "", "date": "2026-09-04"},
            {"name": "MP Start", "date": "2026-09-10"},
            {"name": "Kick Off Date", "date": "2026-09-02"}]
        report["projects"][0]["issues"] = [{"text": "Historical duplicate", "action": "Do not guess"},
                                             {"text": "New issue", "action": "Investigate"}]
        for record_id in ("recOldIssue1", "recOldIssue2"):
            snapshot["records"]["tbl_issues"].append({"id": record_id, "fields": {
                "fld_issues_text": "Historical duplicate", "fld_issues_project": ["recProject"]}})
        snapshot["records"]["tbl_tasks"].append({"id": "recShared", "fields": {
            "fld_tasks_name": "Kick Off Date", "fld_tasks_project": ["recProject", "recOtherProject"]}})
        plan = build_plan(report, snapshot)
        self.assertFalse(plan["blockers"], plan["blockers"])
        self.assertEqual([change["kind"] for change in plan["changes"]], ["projects", "tasks", "issues"])
        self.assertEqual(plan["changes"][1]["fields"]["fld_tasks_name"], "MP Start")
        self.assertEqual(plan["changes"][2]["fields"]["fld_issues_text"], "New issue")
        self.assertTrue(any("duplicate/empty" in warning and "未写入" in warning for warning in plan["warnings"]))
        self.assertTrue(any("duplicate Airtable" in warning and "未写入" in warning for warning in plan["warnings"]))
        self.assertTrue(any("shared across" in warning and "未写入" in warning for warning in plan["warnings"]))
        client = FakeClient(snapshot)
        with tempfile.TemporaryDirectory() as folder:
            result = apply_plan(client, plan, folder)
        self.assertEqual(result["status"], "completed", result)
        self.assertEqual(result["applied"], 3)
        self.assertEqual(client.data["records"]["tbl_tasks"][0]["fields"]["fld_tasks_project"], ["recProject", "recOtherProject"])

    def test_capacity_k_formats_expand_and_preserve_source_evidence(self):
        for raw, expected in [("32K", 32000), ("31.2 K / Month", 31200),
                              ("6.3k per month", 6300), ("60K monthly", 60000)]:
            with self.subTest(raw=raw):
                snapshot, report = fixture()
                report["projects"][0]["fields"]["capacity"] = raw
                change = build_plan(report, snapshot, {'field_mapping':{'projects':{'capacity':'fld_projects_capacity'}}})["changes"][0]
                self.assertEqual(change["fields"]["fld_projects_capacity"], expected)
                self.assertEqual(change["source_values"]["fld_projects_capacity"], raw)
                self.assertEqual(report["projects"][0]["fields"]["capacity"], raw)

    def test_capacity_ambiguous_formats_are_not_extracted_or_converted(self):
        for raw in ["90K / Year", "100K/Y", "2200/day", "4K2", "Follow UZ815H",
                    "10K for SKU1\n5K for SKU2", "5K monthly from ALH", "46K sets"]:
            with self.subTest(raw=raw):
                snapshot, report = fixture()
                report["projects"][0]["fields"]["capacity"] = raw
                plan = build_plan(report, snapshot, {'field_mapping':{'projects':{'capacity':'fld_projects_capacity'}}})
                self.assertNotIn("fld_projects_capacity", plan["changes"][0]["fields"])
                self.assertTrue(any("invalid number" in warning for warning in plan["warnings"]))
        snapshot, report = fixture()
        report["projects"][0]["fields"]["capacity"] = "32K"
        field = next(f for f in snapshot["schema"]["tables"][0]["fields"] if f["id"] == "fld_projects_capacity")
        field["type"] = "singleLineText"
        change = build_plan(report, snapshot, {'field_mapping':{'projects':{'capacity':'fld_projects_capacity'}}})["changes"][0]
        self.assertEqual(change["fields"]["fld_projects_capacity"], "32K")

    def test_delay_alias_only_when_delayed_is_unique_and_delay_is_absent(self):
        for choices, expected in [(["On Track", "Delayed"], "Delayed"),
                                  (["Delay", "Delayed"], "Delay"),
                                  (["Delayed", " delayed "], None), (["On Track"], None)]:
            with self.subTest(choices=choices):
                snapshot, report = fixture()
                report["projects"][0]["fields"]["status"] = " delay "
                field = next(f for f in snapshot["schema"]["tables"][0]["fields"] if f["id"] == "fld_projects_status")
                field["options"]["choices"] = [{"name": name} for name in choices]
                change = build_plan(report, snapshot)["changes"][0]
                if expected is None:
                    self.assertNotIn("fld_projects_status", change["fields"])
                else:
                    self.assertEqual(change["fields"]["fld_projects_status"], expected)

    def test_evidenced_milestone_aliases_preserve_identity_and_reject_compound_title(self):
        snapshot, report = fixture()
        titles = ["ECN DD", "MPRA ,\nECN", "MPRA / ECN IMP", "Old MP Start", "Old MP Start Date",
                  "New MP Start / Eng Ready", "FPO", "DQTP (EB2)"]
        tasks, warnings = [], []
        # Test each alias independently. Multiple synonymous headings in one
        # project are now intentionally rejected as conflicting source identity.
        for title in titles:
            report["projects"][0]["tasks"] = [{"name": title, "date": "2026-09-03"}]
            plan = build_plan(report, snapshot)
            tasks.extend(change for change in plan["changes"] if change["kind"] == "tasks")
            warnings.extend(plan['warnings'])
        self.assertEqual([task["fields"]["fld_tasks_name"] for task in tasks], titles)
        self.assertEqual([task["fields"]["fld_tasks_milestone"] for task in tasks[:5]],
                         ["TRA / ECN DD", "MPRA / ECN", "MPRA / ECN", "Previous MP Date", "Previous MP Date"])
        self.assertTrue(all('fld_tasks_milestone' not in t['fields'] for t in tasks[5:]))
        self.assertEqual(len([warning for warning in warnings if 'ordinary task' in warning]), 3)

    def test_combined_tra_header_keeps_country_specific_task_identity(self):
        snapshot, report = fixture()
        titles = ["TRA/ ECN DD (CN)", "TRA /\nECN DD (VN)"]
        report["projects"][0]["tasks"] = [{"name": title, "date": "2026-09-03"} for title in titles]
        tasks = [change for change in build_plan(report, snapshot)["changes"] if change["kind"] == "tasks"]
        self.assertEqual(len(tasks), 2)
        self.assertTrue(all(task["fields"]["fld_tasks_milestone"] == "TRA / ECN DD" for task in tasks))
        self.assertEqual([task["fields"]["fld_tasks_name"] for task in tasks], titles)
        self.assertNotEqual(tasks[0]["identity"]["title"], tasks[1]["identity"]["title"])


if __name__ == "__main__":
    unittest.main()
