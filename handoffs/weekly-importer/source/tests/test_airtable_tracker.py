from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from test_sync import fixture
from test_tracker import tracker_fixture
from autopm.airtable_tracker import build_airtable_tracker_plan, snapshot_to_report
from autopm.schema_memory import reconcile
from autopm.tracker import export_tracker, fingerprint, read_tracker
from autopm.workbook import WorkbookError


class AirtableTrackerTests(unittest.TestCase):
    def setUp(self):
        self.snapshot, _ = fixture()
        self.snapshot['captured_at'] = '2026-09-11T12:00:00+00:00'
        self.config = reconcile(self.snapshot['schema'], {'base_id': 'appTest'})['config']
        self.project = self.snapshot['records']['tbl_projects'][0]
        self.project['fields']['fld_projects_report_date'] = '2026-09-10'
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name) / 'tracker.xlsx'
        self.output = Path(self.temp.name) / 'updated.xlsx'
        tracker_fixture(self.source)

    def task(self, name='MP Start', milestone='MP Start', due_date='2026-09-20', record_id='recTask', **values):
        row = {'id': record_id, 'fields': {'fld_tasks_name': name,
               'fld_tasks_project': ['recProject'], 'fld_tasks_milestone': milestone,
               'fld_tasks_due_date': due_date, **values}}
        self.snapshot['records']['tbl_tasks'].append(row)
        return row

    def report(self, **kwargs):
        return snapshot_to_report(self.snapshot, self.config, **kwargs)

    def plan(self, **kwargs):
        return build_airtable_tracker_plan(self.source, self.snapshot, self.config, **kwargs)

    def test_cloud_values_links_and_sources_are_used_without_credentials(self):
        self.config['airtable_token'] = 'must-not-be-exported'
        self.config['deepseek_api_key'] = 'also-secret'
        self.project['fields'].update({'fld_projects_project_name': 'Actual cloud name',
                                      'fld_projects_factory': ['recFactory']})
        report = self.report(); project = report['projects'][0]
        self.assertEqual(project['fields']['project_name'], 'Actual cloud name')
        self.assertEqual(project['fields']['npi_lead'], 'Jane Smith')
        self.assertEqual(project['fields']['factory'], 'Factory One')
        plan = self.plan()
        change = next(change for change in plan['changes'] if change['semantic'] == 'project_name')
        self.assertEqual(change['source'], 'Airtable/appTest/tbl_projects/recProject/fld_projects_project_name')
        self.assertEqual(plan['source_kind'], 'airtable')
        self.assertEqual(plan['airtable_source']['captured_at'], self.snapshot['captured_at'])
        self.assertNotIn('must-not-be-exported', json.dumps(plan))
        self.assertNotIn('also-secret', json.dumps(plan))

    def test_only_real_due_date_maps_template_milestone(self):
        self.task(name='MP Start - Example project', **{
            'fld_tasks_start_date': '2025-01-01', 'fld_tasks_duration': 900})
        self.assertEqual(self.report()['projects'][0]['tasks'][0]['date'], '2026-09-20')
        change = next(change for change in self.plan()['changes'] if change['semantic'] == 'mp_start_date')
        self.assertEqual(change['after'], '2026-09-20')
        self.assertIn('tbl_tasks/recTask/fld_tasks_due_date', change['source'])

    def test_cloud_and_local_duplicates_are_not_selected(self):
        other = deepcopy(self.project); other['id'] = 'recDuplicate'
        other['fields']['fld_projects_project_id'] = ' ab- 123 '
        self.snapshot['records']['tbl_projects'].append(other)
        self.assertEqual(self.report()['projects'], [])
        self.assertTrue(any('重复' in warning for warning in self.report()['warnings']))
        self.snapshot['records']['tbl_projects'].pop()
        tracker_fixture(self.source, duplicate=True)
        self.assertFalse(self.plan()['changes'])

    def test_scope_none_empty_and_missing_are_distinct(self):
        other = deepcopy(self.project); other['id'] = 'recOther'; other['fields']['fld_projects_project_id'] = 'ZZ-1'
        self.snapshot['records']['tbl_projects'].append(other)
        self.assertEqual(len(self.report()['projects']), 2)
        self.assertEqual(self.report(project_ids=[])['projects'], [])
        self.assertEqual([p['project_id'] for p in self.report(project_ids=[' ab- 123 '])['projects']], ['AB-123'])
        self.assertTrue(any('未找到' in w for w in self.report(project_ids=['UNKNOWN'])['warnings']))

    def test_missing_invalid_report_date_never_uses_capture_date(self):
        for value in (None, '', 'invalid', 'September'):
            with self.subTest(value=value):
                self.project['fields']['fld_projects_report_date'] = value
                report = self.report()
                self.assertEqual(report['projects'], [])
                self.assertTrue(any('读取时间不能作为周报日期' in w for w in report['warnings']))

    def test_empty_cloud_values_never_clear_local_cells(self):
        self.project['fields'].update({'fld_projects_project_name': '', 'fld_projects_npi_lead': [],
                                      'fld_projects_mp_start_date': None})
        self.assertFalse(self.plan()['changes'])

    def test_unknown_or_ambiguous_person_link_skips_whole_field(self):
        self.project['fields']['fld_projects_npi_lead'] = ['recNpi', 'recMissing']
        report = self.report()
        self.assertNotIn('npi_lead', report['projects'][0]['fields'])
        self.assertTrue(any('关联记录不存在' in w for w in report['warnings']))
        self.project['fields']['fld_projects_npi_lead'] = ['recNpi']
        self.snapshot['records']['tbl_people'].append(deepcopy(self.snapshot['records']['tbl_people'][0]))
        self.assertNotIn('npi_lead', self.report()['projects'][0]['fields'])

    def test_project_date_task_conflict_preserves_local_date(self):
        self.project['fields']['fld_projects_mp_start_date'] = '2026-09-21'
        self.task(due_date='2026-09-20')
        plan = self.plan()
        self.assertFalse(any(c['semantic'] == 'mp_start_date' for c in plan['changes']))
        self.assertTrue(any('项目字段与任务' in w for w in plan['warnings']))

    def test_duplicate_milestones_do_not_collapse_even_when_dates_equal(self):
        for same_date in (True, False):
            with self.subTest(same_date=same_date):
                self.snapshot['records']['tbl_tasks'] = []
                self.task(record_id='recOne')
                self.task(record_id='recTwo', due_date='2026-09-20' if same_date else '2026-09-25')
                self.assertFalse(any(c['semantic'] == 'mp_start_date' for c in self.plan()['changes']))
                self.assertTrue(any('多个任务' in w for w in self.report()['warnings']))

    def test_regional_and_shared_tasks_cannot_overwrite_single_date(self):
        self.project['fields']['fld_projects_mp_start_date'] = '2026-09-20'
        for label in ('MP Start (CN)', 'MP Start (VN)', 'MP Start (IDN)', 'MP Start (MY)'):
            with self.subTest(label=label):
                self.snapshot['records']['tbl_tasks'] = []
                self.task(name=label)
                self.assertFalse(any(c['semantic'] == 'mp_start_date' for c in self.plan()['changes']))
                self.assertTrue(any('地区范围' in w for w in self.report()['warnings']))
        self.snapshot['records']['tbl_tasks'] = []
        task = self.task(); task['fields']['fld_tasks_project'].append('recAnotherProject')
        self.assertFalse(any(c['semantic'] == 'mp_start_date' for c in self.plan()['changes']))

    def test_duplicate_with_empty_due_date_still_prevents_selection(self):
        self.project['fields']['fld_projects_mp_start_date'] = '2026-09-20'
        self.task(record_id='recOne')
        self.task(record_id='recTwo', due_date=None)
        self.assertFalse(any(c['semantic'] == 'mp_start_date' for c in self.plan()['changes']))
        self.assertTrue(any('多个任务' in w for w in self.report()['warnings']))

    def test_no_milestone_does_not_guess_from_template_name(self):
        self.task(name='MP Start - Example project', milestone=None)
        report = self.report()
        self.assertFalse(report['projects'][0]['tasks'])
        self.assertEqual(len(report['projects'][0]['airtable_tasks']), 1)

    def test_explicit_project_timeline_mapping_keeps_date_semantics(self):
        table = next(t for t in self.snapshot['schema']['tables'] if t['id'] == 'tbl_projects')
        table['fields'].append({'id': 'fldPrevious', 'name': 'Reviewed previous MP', 'type': 'date'})
        self.config['field_mapping']['projects']['previous_mp'] = 'fldPrevious'
        self.project['fields']['fldPrevious'] = '2026-08-29'
        self.task(name='Previous MP Date - Example', milestone='Previous MP Date', due_date='2026-08-29')
        change = next(c for c in self.plan()['changes'] if c['semantic'] == 'previous_mp')
        self.assertTrue(change['is_date'])
        self.assertEqual(change['after'], '2026-08-29')

    def test_completion_only_retains_explicit_cloud_checkbox(self):
        self.task(due_date='2025-01-01')
        self.assertNotIn('completed', self.report()['projects'][0]['tasks'][0])
        table = next(t for t in self.snapshot['schema']['tables'] if t['id'] == 'tbl_tasks')
        table['fields'].append({'id': 'fldComplete', 'name': 'Reviewed Complete', 'type': 'checkbox'})
        self.config['field_mapping']['tasks']['completed'] = 'fldComplete'
        self.snapshot['records']['tbl_tasks'][0]['fields']['fldComplete'] = True
        self.assertIs(self.report()['projects'][0]['tasks'][0]['completed'], True)
        table['fields'][-1]['type'] = 'formula'
        with self.assertRaisesRegex(WorkbookError, '字段映射无效'):
            self.report()

    def test_issues_retained_in_audit_and_not_written_into_progress(self):
        self.snapshot['records']['tbl_issues'] = [{'id': 'recIssue', 'fields': {
            'fld_issues_project': ['recProject'], 'fld_issues_text': 'Cloud issue',
            'fld_issues_action': 'Cloud action', 'fld_issues_owner': ['recNpi']}}]
        plan = self.plan(); issue = plan['reports'][0]['projects'][0]['issues'][0]
        self.assertEqual(issue['action'], 'Cloud action')
        self.assertEqual(issue['owner'], 'Jane Smith')
        self.assertTrue(any('没有总表明细列' in w for w in plan['warnings']))
        self.assertFalse(any(c['after'] == 'Cloud issue' for c in plan['changes']))

    def test_id_mapping_survives_names_and_rejects_wrong_base_or_incomplete_snapshot(self):
        for table in self.snapshot['schema']['tables']:
            table['name'] = 'Changed ' + table['id']
            for field in table['fields']:
                field['name'] = 'Changed ' + field['id']
        self.assertEqual(self.report()['projects'][0]['fields']['project_name'], 'Existing')
        self.config['base_id'] = 'different'
        with self.assertRaisesRegex(WorkbookError, 'Base'):
            self.report()
        self.config['base_id'] = 'appTest'
        self.snapshot['records'].pop('tbl_tasks')
        with self.assertRaisesRegex(WorkbookError, '完整'):
            self.report()

    def test_export_is_native_copy_idempotent_and_stale_cloud_is_blocked(self):
        self.project['fields']['fld_projects_project_name'] = 'Cloud name'
        self.project['fields']['fld_projects_npi_lead'] = ['recOther', 'recNpi']
        self.task()
        before = fingerprint(self.source)
        export_tracker(self.plan(), self.output)
        self.assertEqual(fingerprint(self.source), before)
        plan = build_airtable_tracker_plan(self.output, self.snapshot, self.config)
        self.assertFalse(plan['changes'])
        self.project['fields']['fld_projects_npi_lead'].reverse()
        self.assertFalse(build_airtable_tracker_plan(self.output, self.snapshot, self.config)['changes'])
        self.project['fields']['fld_projects_report_date'] = '2026-09-01'
        self.project['fields']['fld_projects_project_name'] = 'Older cloud value'
        stale = build_airtable_tracker_plan(self.output, self.snapshot, self.config)
        self.assertFalse(stale['changes'])
        self.assertTrue(any('早于总表版本' in w for w in stale['warnings']))
        self.assertIn('H2', read_tracker(self.output)['formulas'])

    def test_invalid_task_date_does_not_fall_back_to_project_or_start(self):
        self.project['fields']['fld_projects_mp_start_date'] = '2026-09-21'
        self.task(due_date='not a date', **{'fld_tasks_start_date': '2026-09-20'})
        self.assertFalse(any(c['semantic'] == 'mp_start_date' for c in self.plan()['changes']))

    def test_multiple_selects_join_stably_and_formula_text_stays_literal(self):
        self.config['field_mapping']['projects']['region']='fld_projects_region'
        region = next(f for t in self.snapshot['schema']['tables'] for f in t['fields'] if f['id'] == 'fld_projects_region')
        region['type'] = 'multipleSelects'
        self.project['fields']['fld_projects_region'] = ['VN', 'CN']
        self.assertEqual(self.report()['projects'][0]['fields']['region'], 'CN; VN')
        self.project['fields']['fld_projects_project_name'] = '=HYPERLINK("https://example.invalid", "text")'
        export_tracker(self.plan(), self.output)
        self.assertNotIn('B2', read_tracker(self.output)['formulas'])


if __name__ == '__main__':
    unittest.main()
