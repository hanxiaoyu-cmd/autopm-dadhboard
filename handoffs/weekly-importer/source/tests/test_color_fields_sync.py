import tempfile
import unittest

from test_sync import FakeClient
from test_sync_v2 import v2_fixture
from autopm.airtable_tracker import snapshot_to_report
from autopm.schema_memory import reconcile
from autopm.sync import build_plan, apply_plan
from autopm.weekly_remark import JIRA_COUNT_FIELDS, merge_weekly_remark, read_weekly_remark


class ColorFieldSyncTests(unittest.TestCase):
    def test_jira_zero_and_next_plm_reach_existing_project_and_roundtrip(self):
        snapshot, report, config = v2_fixture()
        values = report['projects'][0]['fields']
        values.update({key: '0' for key in JIRA_COUNT_FIELDS})
        values.update(next_plm='MP workflow to be released by Oct 15',
                      jira_link='https://example.atlassian.net/browse/DEMO-1')
        state = reconcile(snapshot['schema'], config)
        self.assertFalse(state['blockers'], state['blockers'])
        plan = build_plan(report, snapshot, state['config'])
        self.assertFalse(plan['blockers'], plan['blockers'])
        project = next(c for c in plan['changes'] if c['kind'] == 'projects')
        self.assertEqual(project['fields']['fld_projects_next_plm'], values['next_plm'])
        self.assertEqual(project['fields']['fld_projects_jira_link'], values['jira_link'])
        self.assertEqual(project['fields']['fld_projects_jira_summary'],'Total: 0, Ready to close: 0, Verify: 0, Open: 0, Closed: 0')
        self.assertFalse(any('jira_' in w and 'unmapped' in w for w in plan['warnings']))
        client = FakeClient(snapshot)
        with tempfile.TemporaryDirectory() as folder:
            result = apply_plan(client, plan, folder)
        self.assertEqual(result['status'], 'completed', result)
        self.assertFalse(build_plan(report, client.data, state['config'])['changes'])
        readback = snapshot_to_report(client.data, state['config'])['projects'][0]
        for key in {'next_plm', 'jira_link'}:
            self.assertEqual(readback['fields'][key], values[key])
            self.assertIn('fld_projects_', readback['field_sources'][key])
        self.assertEqual(readback['fields']['jira_summary'],project['fields']['fld_projects_jira_summary'])

    def test_zero_overwrites_nonzero_count_without_clearing_missing_fields(self):
        snapshot,report,config=v2_fixture()
        snapshot['records']['tbl_projects'][0]['fields']['fld_projects_jira_summary']='Total: 5, Open: 3'
        report['projects'][0]['fields']['jira_total']='0'
        plan=build_plan(report,snapshot,config)
        project=next(c for c in plan['changes'] if c['kind']=='projects')
        self.assertEqual(project['fields']['fld_projects_jira_summary'],'Total: 0, Open: 3')
        client=FakeClient(snapshot)
        with tempfile.TemporaryDirectory() as folder:self.assertEqual(apply_plan(client,plan,folder)['status'],'completed')
        self.assertFalse(build_plan(report,client.data,config)['changes'])

    def test_invalid_counts_cannot_be_saved_or_parsed(self):
        for value in ('-1', '1.2', 'three', '1+2', '1e3'):
            with self.subTest(value=value):
                snapshot,report,config=v2_fixture()
                report['projects'][0]['fields']['jira_total']=value
                plan=build_plan(report,snapshot,config)
                self.assertTrue(any('不是非负整数' in w for w in plan['warnings']))
                self.assertFalse(any('fld_projects_jira_summary' in c['fields'] for c in plan['changes']))

    def test_new_field_types_and_empty_values_are_checked(self):
        snapshot, report, config = v2_fixture()
        project = snapshot['records']['tbl_projects'][0]['fields']
        project.update(fld_projects_next_plm='Preserve action', fld_projects_jira_link='https://example.com/existing')
        report['projects'][0]['fields'].update(next_plm='', jira_link='')
        change = next(c for c in build_plan(report, snapshot, config)['changes'] if c['kind']=='projects')
        self.assertNotIn('fld_projects_next_plm', change['fields'])
        self.assertNotIn('fld_projects_jira_link', change['fields'])
        field = next(f for t in snapshot['schema']['tables'] for f in t['fields'] if f['id']=='fld_projects_jira_link')
        field['type'] = 'formula'
        state = reconcile(snapshot['schema'], config)
        self.assertFalse(state['blockers'])
        self.assertIsNone(state['config']['field_mapping']['projects']['jira_link'])

    def test_old_report_cannot_overwrite_jira_or_next_plm(self):
        snapshot, report, config = v2_fixture()
        snapshot['records']['tbl_projects'][0]['fields']['fld_projects_current_progress'] = merge_weekly_remark(
            '', '2026-09-15', {'jira_total': '10'})
        report['projects'][0]['fields'].update(next_plm='Older action', jira_total='0')
        plan = build_plan(report, snapshot, config)
        self.assertFalse(plan['changes'])
        self.assertTrue(any('stale report' in w for w in plan['warnings']))
