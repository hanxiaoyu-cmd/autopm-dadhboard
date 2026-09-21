from pathlib import Path
import tempfile
import unittest

from openpyxl import Workbook

from test_sync import fixture
from autopm.airtable_tracker import build_airtable_tracker_plan, snapshot_to_report
from autopm.schema_memory import reconcile
from autopm.weekly_remark import merge_weekly_remark
from autopm.workbook import WorkbookError


class AirtableTrackerV2Tests(unittest.TestCase):
    def setUp(self):
        self.snapshot, _ = fixture()
        self.snapshot['captured_at'] = '2026-09-20T12:00:00+00:00'
        self.config = reconcile(self.snapshot['schema'], {'base_id': 'appTest'})['config']
        self.config['project_report_storage'] = 'engineering_remark'
        project_mapping = self.config['field_mapping']['projects']
        project_mapping['report_date'] = None
        self.remark_id = project_mapping['current_progress']
        self.table = next(t for t in self.snapshot['schema']['tables'] if t['id'] == 'tbl_projects')
        self.table['fields'] = [f for f in self.table['fields']
                                if f['id'] not in {'fld_projects_report_date'}]
        self.remark_field = next(f for f in self.table['fields'] if f['id'] == self.remark_id)
        self.remark_field.update(name='Engineering remark(Manual)', type='richText')
        self.project = self.snapshot['records']['tbl_projects'][0]
        self.project['fields'].pop('fld_projects_report_date', None)
        self.remark_source = f'Airtable/appTest/tbl_projects/recProject/{self.remark_id}'

    def remark(self, date='2026-09-15', fields=None, existing='Original engineering notes'):
        incoming = fields if fields is not None else {'update_this_week':'This week update'}
        if incoming.get('update_this_week'):
            self.project['fields']['fld_projects_update_this_week']=incoming['update_this_week']
        text = merge_weekly_remark(existing, date, fields or {
            'current_progress': 'Current engineering progress', 'update_this_week': 'This week update'})
        self.project['fields'][self.remark_id] = text
        return text

    def report(self):
        return snapshot_to_report(self.snapshot, self.config)

    def test_latest_block_is_unpacked_with_exact_cloud_field_sources(self):
        older = self.remark('2026-09-10', {'current_progress': 'Old progress', 'update_this_week': 'Old update'})
        self.remark(existing=older)
        project = self.report()['projects'][0]
        self.assertEqual(project['report_date'], '2026-09-15')
        self.assertEqual(project['fields']['current_progress'], 'Current engineering progress')
        self.assertEqual(project['fields']['update_this_week'], 'This week update')
        self.assertNotIn('Original engineering notes', project['fields']['current_progress'])
        self.assertNotIn('Old progress', project['fields']['current_progress'])
        for key in ('report_date', 'current_progress'):
            self.assertEqual(project['field_sources'][key], self.remark_source)
        self.assertTrue(project['field_sources']['update_this_week'].endswith('/fld_projects_update_this_week'))
        self.assertEqual(project['fields']['npi_lead'], 'Jane Smith')

    def test_partial_update_reads_values_preserved_in_latest_block(self):
        older = self.remark('2026-09-10', {'current_progress': 'Old progress'})
        self.remark(fields={'update_this_week': 'Only the new update'}, existing=older)
        project = self.report()['projects'][0]
        self.assertEqual(project['fields']['current_progress'], 'Old progress')
        self.assertEqual(project['field_sources']['current_progress'], self.remark_source)
        self.assertEqual(project['report_date'], '2026-09-15')
        self.assertEqual(project['fields']['update_this_week'], 'Only the new update')

    def test_no_block_never_uses_capture_time_or_free_text_date(self):
        for text in (None, '', 'Engineering reviewed 2026-09-15; no weekly block.'):
            with self.subTest(text=text):
                self.project['fields'][self.remark_id] = text
                report = self.report()
                self.assertEqual(report['projects'], [])
                self.assertTrue(any('读取时间不能作为周报日期' in w for w in report['warnings']))

    def test_corrupt_block_skips_project_including_unrelated_field_updates(self):
        self.project['fields'][self.remark_id] = self.remark().replace('2026-09-15','2026-02-30')
        self.project['fields']['fld_projects_project_name'] = 'Should not update'
        report = self.report()
        self.assertEqual(report['projects'], [])
        self.assertTrue(any('周报块无效' in w for w in report['warnings']))

    def test_missing_remark_mapping_is_not_replaced_by_capture_time(self):
        self.config['field_mapping']['projects']['current_progress'] = None
        with self.assertRaisesRegex(WorkbookError, '缺少有效映射'):
            self.report()

    def test_readonly_remark_field_still_rejects_invalid_schema(self):
        self.remark_field['type'] = 'formula'
        with self.assertRaisesRegex(WorkbookError, '字段映射无效'):
            self.report()

    def test_tracker_plan_uses_block_date_and_remark_provenance(self):
        self.remark()
        with tempfile.TemporaryDirectory() as folder:
            tracker = Path(folder) / 'tracker.xlsx'
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = 'ALL PROJECTS'
            sheet.append(['PROJECT NUMBER', 'Current Progress', 'Update This Week', 'Report Date'])
            sheet.append(['AB-123', 'Local progress', 'Local update', '2026-09-14'])
            workbook.save(tracker)
            plan = build_airtable_tracker_plan(tracker, self.snapshot, self.config)
            changes = {change['semantic']: change for change in plan['changes']}
            self.assertEqual(set(changes), {'current_progress', 'update_this_week', 'report_date'})
            self.assertEqual(changes['report_date']['after'], '2026-09-15')
            self.assertEqual(changes['current_progress']['after'], 'Current engineering progress')
            self.assertEqual(changes['update_this_week']['after'], 'This week update')
            self.assertEqual(changes['current_progress']['source'],self.remark_source)
            self.assertTrue(changes['update_this_week']['source'].endswith('/fld_projects_update_this_week'))
            self.assertEqual(plan['versions']['AB-123'], '2026-09-15')
            sheet['D2'] = '2026-09-16'
            workbook.save(tracker)
            stale = build_airtable_tracker_plan(tracker, self.snapshot, self.config)
            self.assertEqual(stale['changes'], [])
            self.assertTrue(any('早于总表版本' in w for w in stale['warnings']))
            workbook.close()


if __name__ == '__main__':
    unittest.main()
