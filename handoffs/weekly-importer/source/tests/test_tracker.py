from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from xml.sax.saxutils import escape
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from test_workbook import fixture_workbook
from autopm.tracker import build_tracker_plan,export_tracker,fingerprint,read_tracker
from autopm.workbook import WorkbookError


def tracker_fixture(path, *, duplicate=False, reordered=False, formula_name=False):
    fixture_workbook(path)
    with ZipFile(path) as z:parts={n:z.read(n) for n in z.namelist()}
    parts['xl/workbook.xml']=parts['xl/workbook.xml'].replace(b'name="Report"',b'name="ALL PROJECTS"')
    headers=['PROJECT NUMBER','Project Name , Description','Eng , OEM Kick Off','MP START','NPI Project Lead','Eng Status','Previous MP Start Date','Derived duration']
    data=['AB-123','Old name','2026-09-01','2026-09-15','Jane','On Track','2026-08-30','=SUM(D2-C2)/7']
    if reordered:headers[0],headers[1]=headers[1],headers[0];data[0],data[1]=data[1],data[0]
    if formula_name:data[1]='=A2'
    rows=[]
    for r,values in [(1,headers),(2,data)]+([(3,data)] if duplicate else []):
        cells=[]
        for i,v in enumerate(values):
            ref=f'{chr(65+i)}{r}'
            if v.startswith('='):cells.append(f'<c r="{ref}"><f>{escape(v[1:])}</f><v>2</v></c>')
            else:cells.append(f'<c r="{ref}" t="inlineStr"><is><t>{escape(v)}</t></is></c>')
        rows.append(f'<row r="{r}">'+''.join(cells)+'</row>')
    parts['xl/worksheets/sheet1.xml']=('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><dimension ref="A1:H3"/><sheetData>'+''.join(rows)+'</sheetData></worksheet>').encode()
    parts['customXML/item1.xml']=b'<original>preserve byte for byte</original>'
    with ZipFile(path,'w') as z:
        for n,v in parts.items():z.writestr(n,v)


def report_fixture():
    return {'source':'weekly.xlsx','report_date':'2026-09-10','warnings':[], 'projects':[
        {'project_id':' ab- 123 ','report_date':'2026-09-10','fields':{'project_name':'New name','kick_off_date':'2026-09-10','mp_start_date':'2026-09-20'},
         'tasks':[{'name':'MP Start','date':'2026-09-20','source':"'Report'!D7"}],
         'issues':[{'text':'Needs review','action':'Review CAD'}],'source':"'Report'!D1:U25"}]}


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.folder=Path(self.temp.name);self.source=self.folder/'tracker.xlsx';self.output=self.folder/'updated.xlsx'
        tracker_fixture(self.source);self.report=report_fixture()

    def test_header_matching_survives_reordered_columns(self):
        tracker_fixture(self.source,reordered=True)
        plan=build_tracker_plan(self.source,[self.report])
        self.assertEqual(plan['matched_projects'],1)
        self.assertEqual(next(c['cell'] for c in plan['changes'] if c['semantic']=='project_name'),'A2')

    def test_export_preserves_source_native_parts_formula_and_recalculates_known_cache(self):
        original=fingerprint(self.source);plan=build_tracker_plan(self.source,[self.report])
        with patch('httpx.Client.send',side_effect=AssertionError('no network')):
            result=export_tracker(plan,self.output)
        self.assertEqual(result['changed_cells'],3);self.assertEqual(result['recalculated_caches'],1)
        self.assertEqual(fingerprint(self.source),original)
        ns='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
        with ZipFile(self.source) as src,ZipFile(self.output) as out:
            self.assertEqual(set(src.namelist()),set(out.namelist()))
            self.assertEqual(src.read('customXML/item1.xml'),out.read('customXML/item1.xml'))
            cells={c.get('r'):c for c in ET.fromstring(out.read('xl/worksheets/sheet1.xml')).iter(ns+'c')}
            self.assertEqual(cells['H2'].findtext(ns+'f'),'SUM(D2-C2)/7')
            self.assertAlmostEqual(float(cells['H2'].findtext(ns+'v')),10/7)
            self.assertEqual(cells['C2'].get('t'),'n')
        repeated=build_tracker_plan(self.output,[self.report]);self.assertFalse(repeated['changes'])

    def test_audit_versions_prevent_older_report_overwrite(self):
        export_tracker(build_tracker_plan(self.source,[self.report]),self.output)
        old=deepcopy(self.report);old['projects'][0]['report_date']='2026-09-01';old['projects'][0]['fields']['project_name']='Old report'
        plan=build_tracker_plan(self.output,[old]);self.assertFalse(plan['changes'])
        self.assertTrue(any('早于总表版本' in w for w in plan['warnings']))

    def test_resaving_metadata_or_formula_caches_keeps_valid_import_history(self):
        export_tracker(build_tracker_plan(self.source,[self.report]),self.output)
        with ZipFile(self.output) as z:parts={n:z.read(n) for n in z.namelist()}
        parts['customXML/item1.xml']=b'<original>saved by Excel</original>'
        with ZipFile(self.output,'w') as z:
            for n,v in parts.items():z.writestr(n,v)
        self.assertFalse(build_tracker_plan(self.output,[self.report])['changes'])

    def test_multiple_reports_choose_latest_independent_of_upload_order(self):
        old=deepcopy(self.report);old['projects'][0]['report_date']='2026-09-01';old['projects'][0]['fields']['project_name']='Obsolete'
        a=build_tracker_plan(self.source,[old,self.report]);b=build_tracker_plan(self.source,[self.report,old])
        self.assertEqual(a['changes'],b['changes'])

    def test_equal_date_conflicting_reports_skip_project(self):
        other=deepcopy(self.report);other['projects'][0]['fields']['project_name']='Conflict'
        plan=build_tracker_plan(self.source,[other,self.report]);self.assertFalse(plan['changes'])
        self.assertTrue(any('同日期' in w for w in plan['warnings']))

    def test_duplicate_or_missing_identity_does_not_write(self):
        tracker_fixture(self.source,duplicate=True)
        self.assertFalse(build_tracker_plan(self.source,[self.report])['changes'])
        self.report['projects'][0]['project_id']='MISSING'
        self.assertFalse(build_tracker_plan(self.source,[self.report])['changes'])

    def test_formula_target_and_conflicting_date_candidates_are_skipped(self):
        tracker_fixture(self.source,formula_name=True)
        self.report['projects'][0]['tasks'][0]['date']='2026-09-21'
        plan=build_tracker_plan(self.source,[self.report])
        self.assertEqual({c['cell'] for c in plan['changes']},{'C2'})
        self.assertTrue(any('是公式' in w for w in plan['warnings']))
        self.assertTrue(any('多个不同候选值' in w for w in plan['warnings']))

    def test_changed_source_or_report_rejects_export(self):
        weekly=self.folder/'weekly.xlsx';weekly.write_bytes(b'source one')
        plan=build_tracker_plan(self.source,[self.report]);plan['source_files']={str(weekly):fingerprint(weekly)}
        weekly.write_bytes(b'changed')
        with self.assertRaisesRegex(WorkbookError,'变化'):export_tracker(plan,self.output)
        self.assertFalse(self.output.exists())

    def test_original_and_existing_destination_cannot_be_overwritten(self):
        plan=build_tracker_plan(self.source,[self.report])
        with self.assertRaisesRegex(WorkbookError,'不能覆盖'):export_tracker(plan,self.source)
        self.output.write_bytes(b'keep')
        with self.assertRaisesRegex(WorkbookError,'已存在'):export_tracker(plan,self.output)
        self.assertEqual(self.output.read_bytes(),b'keep')

    def test_formula_looking_source_is_literal_text(self):
        self.report['projects'][0]['fields']['project_name']='=HYPERLINK("https://example.com","text")'
        export_tracker(build_tracker_plan(self.source,[self.report]),self.output)
        tracker=read_tracker(self.output)
        self.assertEqual(tracker['cells']['B2'],self.report['projects'][0]['fields']['project_name'])
        self.assertNotIn('B2',tracker['formulas'])

    def test_corrupt_or_mismatched_audit_fails_closed(self):
        Path(str(self.source)+'.autopm.json').write_text('{bad',encoding='utf-8')
        with self.assertRaisesRegex(WorkbookError,'同步记录'):build_tracker_plan(self.source,[self.report])

    def test_disabled_sheet_protection_metadata_is_preserved_without_blocking(self):
        with ZipFile(self.source) as z:parts={n:z.read(n) for n in z.namelist()}
        parts['xl/worksheets/sheet1.xml']=parts['xl/worksheets/sheet1.xml'].replace(b'</worksheet>',b'<sheetProtection formatCells="0"/></worksheet>')
        with ZipFile(self.source,'w') as z:
            for n,v in parts.items():z.writestr(n,v)
        export_tracker(build_tracker_plan(self.source,[self.report]),self.output)
        with ZipFile(self.output) as z:self.assertIn(b'<sheetProtection formatCells="0"/>',z.read('xl/worksheets/sheet1.xml'))

    def test_active_protection_rejects_export_without_output(self):
        with ZipFile(self.source) as z:parts={n:z.read(n) for n in z.namelist()}
        parts['xl/worksheets/sheet1.xml']=parts['xl/worksheets/sheet1.xml'].replace(b'</worksheet>',b'<sheetProtection sheet="1"/></worksheet>')
        with ZipFile(self.source,'w') as z:
            for n,v in parts.items():z.writestr(n,v)
        with self.assertRaisesRegex(WorkbookError,'已保护'):export_tracker(build_tracker_plan(self.source,[self.report]),self.output)
        self.assertFalse(self.output.exists())

    def test_unknown_affected_formula_cache_is_cleared_for_excel_recalculation(self):
        with ZipFile(self.source) as z:parts={n:z.read(n) for n in z.namelist()}
        parts['xl/worksheets/sheet1.xml']=parts['xl/worksheets/sheet1.xml'].replace(b'SUM(D2-C2)/7',b'SUM(D2,C2)')
        with ZipFile(self.source,'w') as z:
            for n,v in parts.items():z.writestr(n,v)
        result=export_tracker(build_tracker_plan(self.source,[self.report]),self.output)
        self.assertEqual(result['formula_caches_requiring_excel'],['H2'])
        with ZipFile(self.output) as z:
            ns='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
            c=next(c for c in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).iter(ns+'c') if c.get('r')=='H2')
            self.assertEqual(c.findtext(ns+'f'),'SUM(D2,C2)');self.assertIsNone(c.find(ns+'v'))

    def test_destination_race_preserves_existing_file_and_removes_own_audit(self):
        import os
        name='rename' if os.name=='nt' else 'link';publish=getattr(os,name)
        def race(src,dest):
            if Path(dest)==self.output:
                self.output.write_bytes(b'other application')
                raise FileExistsError('destination appeared')
            return publish(src,dest)
        with patch('autopm.native_xlsx.os.'+name,side_effect=race),self.assertRaises(FileExistsError):
            export_tracker(build_tracker_plan(self.source,[self.report]),self.output)
        self.assertEqual(self.output.read_bytes(),b'other application')
        self.assertFalse(Path(str(self.output)+'.autopm.json').exists())

    def test_unknown_columns_and_issues_remain_in_audit(self):
        self.report['projects'][0]['fields']['factory']='Development or manufacturing?'
        plan=build_tracker_plan(self.source,[self.report])
        result=export_tracker(plan,self.output)
        saved=json.loads(Path(result['audit']).read_text(encoding='utf-8'))
        self.assertEqual(saved['reports'][0]['projects'][0]['issues'],self.report['projects'][0]['issues'])
        self.assertTrue(any('factory' in w for w in plan['warnings']))

if __name__=='__main__':unittest.main()
