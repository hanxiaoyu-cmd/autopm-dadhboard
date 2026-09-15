import unittest,tempfile,pathlib,zipfile,json,datetime as dt
import bridge as b

def workbook(path,rows,epoch=False):
    ns=b.NS
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('xl/workbook.xml',f'<workbook xmlns="{ns}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><workbookPr date1904="{int(epoch)}"/><sheets><sheet name="ALL PROJECTS" sheetId="1" r:id="rId1"/></sheets></workbook>')
        z.writestr('xl/_rels/workbook.xml.rels','<Relationships><Relationship Id="rId1" Target="worksheets/sheet1.xml"/></Relationships>')
        z.writestr('xl/worksheets/sheet1.xml',f'<worksheet xmlns="{ns}"><sheetData>{rows}</sheetData></worksheet>')
        z.writestr('xl/styles.xml',f'<styleSheet xmlns="{ns}"><fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills><cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs></styleSheet>')
        z.writestr('xl/media/image1.png',b'untouched-image-content')
        z.writestr('xl/worksheets/sheet2.xml',b'untouched-other-sheet')
def textcell(ref,value):return f'<c r="{ref}" t="inlineStr"><is><t>{value}</t></is></c>'
def snapshot(records):return {'base':'appTest','table':'tblTest','projects':records,'schema':{'tables':[{'id':'tblTest','fields':[{'id':fid,'name':key,'type':typ,'options':{'choices':[{'name':'Delayed'}]}} for key,(fid,typ) in b.FIELDS.items()]}]},'links':{}}

def operational_snapshot(project):
    project_fields=[{'id':fid,'name':name,'type':typ,'options':{'choices':[{'name':'Delayed'}]}} for name,(fid,typ) in b.FIELDS.items()]
    project_fields += [{'id':'fldWeekly','name':'Weekly Report Update Date (System)','type':'date'},
                       {'id':'fldProgress','name':'Current Progress (Manual)','type':'multilineText'},
                       {'id':'fldTooling','name':'Tooling (Manual)','type':'singleLineText'}]
    task_fields=[{'id':v,'name':k,'type':'multipleRecordLinks' if k in ('owners','completed_by','project') else 'singleSelect' if k=='milestone' else 'date' if k in ('start','due') else 'singleLineText','options':{'choices':[{'name':x} for x in list(b.CANONICAL_MILESTONE.values())+['FPO Release']]}} for k,v in b.TASK_FIELDS.items()]
    issue_fields=[{'id':v,'name':k,'type':'multipleRecordLinks' if k in ('owners','project') else 'date' if k in ('record_date','target_date') else 'singleSelect' if k in ('status','severity') else 'multilineText'} for k,v in b.ISSUE_FIELDS.items()]
    people=[{'id':'per1','fields':{b.PEOPLE_NAME:'Nick Name',b.PEOPLE_DEPARTMENT:'NPI'}}]
    return {'base':'appTest','table':'tblTest','tasks_table':'tblTasks','issues_table':'tblIssues','projects':[project],
            'tasks':[],'issues':[],'project_specs':{**b.FIELDS,'weekly_updated':('fldWeekly','date'),'current_progress':('fldProgress','multilineText'),'tooling':('fldTooling','singleLineText')},
            'schema':{'tables':[{'id':'tblTest','name':'Projects','fields':project_fields},{'id':'tblTasks','name':'Tasks','fields':task_fields},{'id':'tblIssues','name':'Issues','fields':issue_fields},{'id':'tblPeople','name':'People','primaryFieldId':b.PEOPLE_NAME,'fields':[{'id':b.PEOPLE_NAME,'name':'Name','type':'singleLineText'},{'id':b.PEOPLE_DEPARTMENT,'name':'Department','type':'singleSelect'}]}]},
            'links':{'tblPeople':people}}

class BridgeTests(unittest.TestCase):
    def test_dates(self):
        self.assertEqual(b.read_date({'active':'1','type':None},dt.datetime(1904,1,1))[0],'1904-01-02')
        self.assertEqual(b.read_date({'active':'30-Jul','type':'s'},dt.datetime(1899,12,30))[1],'ambiguous_or_yearless_date')
        self.assertEqual(b.read_date({'active':'9-Feb-26\n3-Feb-26','type':'s'},dt.datetime(1899,12,30))[0],'2026-02-03')
        self.assertEqual(b.read_date({'active':'Sep 7','type':'s'},dt.datetime(1899,12,30),2026)[0],'2026-09-07')
        self.assertEqual(b.read_date({'active':'12-Spe-26','type':'s'},dt.datetime(1899,12,30))[0],'2026-09-12')
        self.assertEqual(b.read_date({'active':'Jiul -14-26\nJul-3-26','type':'s'},dt.datetime(1899,12,30))[0],'2026-07-03')
        self.assertEqual(b.read_date({'active':'2026-02-30','type':'s'},dt.datetime(1899,12,30))[0],None)
        self.assertEqual(b.read_date({'active':'0','type':None},dt.datetime(1899,12,30))[0],None)
    def test_rich_text_strike(self):
        e=b.ET.fromstring(f'<si xmlns="{b.NS}"><r><rPr><strike/></rPr><t>9-Feb-26</t></r><r><t>3-Feb-26</t></r></si>')
        self.assertEqual(b.rich_text(e)[1],'3-Feb-26')
        old=b.ET.fromstring(f'<si xmlns="{b.NS}"><r><rPr><strike/></rPr><t>9-Feb-26</t></r></si>')
        full,active=b.rich_text(old)
        self.assertEqual(b.read_date({'raw':full,'active':active,'type':'s'},dt.datetime(1899,12,30))[0],'2026-02-09')
    def test_sku_shorthand_normalization(self):
        self.assertEqual(b.normalize_skus('BW1001WH,GN2'),'BW1001WH, BW1001GN2')
        self.assertEqual(b.normalize_skus('BW1001WH/BW1001GN2'),'BW1001WH, BW1001GN2')
        self.assertEqual(b.normalize_skus('FS353A, ES300, ES300SD'),'FS353A, ES300, ES300SD')
    def test_fixed_and_ordinary_task_classification(self):
        self.assertEqual(b.classify_dated_task('DR release for MP')[1],'MP Start')
        self.assertEqual(b.classify_dated_task('DR Approval')[1],None)
        self.assertEqual(b.classify_dated_task('P1')[1],'P1 BUILD DATE')
        self.assertEqual(b.classify_dated_task('BIS Cert')[1],'Compliance report')
        self.assertEqual(b.classify_dated_task('MP start (IDN)')[1],'MP Start')
        self.assertEqual(b.classify_dated_task('TRA / ECN')[1],'TRA / ECN DD')
        self.assertEqual(b.classify_dated_task('AW file release')[1],'MP AW release')
        self.assertEqual(b.classify_dated_task('Cutting steel')[1],'Cut Steel')
        self.assertTrue(b.classify_dated_task('EB3.5 (CN)')[2])
        self.assertTrue(b.classify_dated_task('Sample PO Approval')[2])
    def test_task_issue_and_project_mapping(self):
        project={'id':'rec1','fields':{b.PID_FIELD:'NXA0001',b.FIELDS['npi'][0]:['per1']}}
        parsed={'projects':[{'pid':'NXA0001','row':1,'updated_on':'2026-09-04','values':{'current_progress':'Latest','tooling':'71 sets','capacity':'52k','weekly_updated':'2026-09-04'},'cells':{},'unmapped':{},'sections':[],
                 'dated_tasks':[{'date':'2026-09-10','task_name':'P1 BUILD DATE','milestone':'P1 BUILD DATE','green':False,'cell':'A1'},{'date':'2026-10-19','task_name':'MP Start','milestone':'MP Start','green':True,'cell':'B1'},{'date':'2026-09-12','task_name':'Factory Audit','milestone':None,'green':False,'cell':'C1'}],
                 'issues':[{'row':2,'values':{'key issues':'1. Housing risk','actions':'Fix it','risk (h/m/l)':'H','owner':'Nick Name','due date':'46273'},'cells':{'due date':{'raw':'46273','active':'46273','type':None}}}]}],
                'source':'x','sha256':'x','warnings':[]}
        plan=b.make_airtable_plan(parsed,operational_snapshot(project));creates=[x for x in plan['changes'] if x.get('op')=='create']
        tasks=[x for x in creates if x['table']=='tblTasks'];issues=[x for x in creates if x['table']=='tblIssues']
        self.assertEqual(len(tasks),2);self.assertEqual(len(issues),1)
        p1=next(x['new'] for x in tasks if x['display_new']=='P1 BUILD DATE');self.assertEqual(p1[b.TASK_FIELDS['due']],'2026-09-10')
        mp=next(x['new'] for x in tasks if x['display_new']=='MP Start');self.assertEqual(mp[b.TASK_FIELDS['due']],'2026-10-19');self.assertNotIn(b.TASK_FIELDS['completed_by'],mp)
        self.assertTrue(any(x['reason']=='task_date_range_requires_mapping' for x in plan['skipped']))
        self.assertEqual(plan['reported_completion'][0]['claim'],'source_reported_complete')
        self.assertEqual(issues[0]['new'][b.ISSUE_FIELDS['severity']],'High');self.assertEqual(issues[0]['new'][b.ISSUE_FIELDS['target_date']],'2026-09-08')
        project_changes={x['field_name']:x['new'] for x in plan['changes'] if x.get('table')=='tblTest'}
        self.assertEqual(project_changes['Capacity / Forecast (Manual)'],52000.0);self.assertEqual(project_changes['Current Progress (Manual)'],'Latest')
    def test_no_invented_milestone_alias(self):
        self.assertNotEqual(b.MS_INDEX['dqtp'],b.MS_INDEX['tra'])
        self.assertEqual(b.MS_INDEX[b.milestone_norm('MP Start\n(Eng Ready)\n(VN)')],'mp')
        self.assertNotIn('Original MP Ready [at KO]',b.TRACKER.values())
        self.assertEqual(b.TRACKER['status'],'Eng Status')
    def test_airtable_duplicates_and_rename(self):
        r={'id':'rec1','fields':{b.PID_FIELD:'NXA0001'}}
        parsed={'projects':[{'pid':'NXA0001','row':1,'values':{'name':'new'},'cells':{'name':'D2'},'unmapped':{},'issues':[]}],'source':'x','sha256':'x','warnings':[]}
        plan=b.make_airtable_plan(parsed,snapshot([r]))
        self.assertEqual(plan['changes'][0]['field'],b.FIELDS['name'][0])
        self.assertFalse(b.make_airtable_plan(parsed,snapshot([r,r]))['changes'])
        parsed['projects']*=2
        self.assertFalse(b.make_airtable_plan(parsed,snapshot([r]))['changes'])
    def test_zip_update_preserves_objects_formula_and_baseline(self):
        with tempfile.TemporaryDirectory() as td:
            source=pathlib.Path(td)/'in.xlsx';out=pathlib.Path(td)/'out.xlsx'
            rows='<row r="2">'+textcell('A2','Project Number')+textcell('B2','MP START')+textcell('C2','Previous MP Start Date')+textcell('D2','Original MP Ready [at KO]')+'</row>'
            rows+='<row r="3">'+textcell('A3','NXA0001')+'<c r="B3"><v>46000</v></c><c r="D3"><v>45000</v></c><c r="E3"><f>B3-D3</f><v>1000</v></c></row>'
            workbook(source,rows)
            ss=snapshot([{'id':'rec1','fields':{b.PID_FIELD:'NXA0001',b.FIELDS['mp'][0]:'2026-09-05',b.FIELDS['previous_mp'][0]:'2026-08-10'}}])
            plan=b.make_tracker_plan(ss,source);self.assertEqual(len(plan['changes']),2)
            before=b.digest(source);b.apply_tracker(plan,out);self.assertEqual(before,b.digest(source))
            with zipfile.ZipFile(out) as z:
                s=z.read('xl/worksheets/sheet1.xml').decode()
                self.assertIn('<c r="D3"><v>45000</v></c>',s);self.assertIn('<f>B3-D3</f>',s)
                self.assertEqual(z.read('xl/media/image1.png'),b'untouched-image-content')
                styles=z.read('xl/styles.xml').decode()
                self.assertIn('FFC6EFCE',styles)
                self.assertRegex(s,r'<c r="B3" s="1">')
            self.assertEqual(len(b.make_tracker_plan(ss,out)['changes']),0)
            with self.assertRaises(ValueError):b.apply_tracker(plan,source)
    def test_green_style_preserves_ignorable_namespace_prefixes(self):
        xml=(f'<styleSheet xmlns="{b.NS}" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
             'mc:Ignorable="x14ac xr" xmlns:x14ac="http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac" '
             'xmlns:xr="http://schemas.microsoft.com/office/spreadsheetml/2014/revision">'
             '<fills count="1"><fill><patternFill patternType="none"/></fill></fills>'
             '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellXfs></styleSheet>').encode()
        rendered,_=b._green_styles(xml,[0]);text=rendered.decode()
        self.assertIn('mc:Ignorable="x14ac xr"',text)
        self.assertIn('xmlns:x14ac=',text);self.assertIn('xmlns:xr=',text)
    def test_formula_and_tbc_are_not_overwritten(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/'in.xlsx'
            rows='<row r="2">'+textcell('A2','Project Number')+textcell('B2','MP START')+'</row><row r="3">'+textcell('A3','NXA0001')+textcell('B3','TBC')+'</row>'
            workbook(p,rows)
            ss=snapshot([{'id':'rec1','fields':{b.PID_FIELD:'NXA0001',b.FIELDS['mp'][0]:'2026-09-05'}}])
            self.assertFalse(b.make_tracker_plan(ss,p)['changes'])
            workbook(p,rows.replace(textcell('B3','TBC'),'<c r="B3"><f>TODAY()</f><v>46000</v></c>'))
            self.assertFalse(b.make_tracker_plan(ss,p)['changes'])
            workbook(p,rows.replace(textcell('B3','TBC'),'<c r="B3"><f t="shared" si="1"/><v>46000</v></c>'))
            self.assertFalse(b.make_tracker_plan(ss,p)['changes'])
    def test_project_key_is_not_model(self):
        self.assertEqual(b.pid('AF140PU'),'');self.assertEqual(b.pid(' NXA0025 '),'NXA0025')
    def test_apply_stale_no_writes(self):
        class API:
            base='appTest';table='tblTest'
            def records(self,t):return [{'id':'rec1','fields':{b.FIELDS['name'][0]:'changed elsewhere'}}]
            def schema(self):return snapshot([])['schema']
            def request(self,*a):raise AssertionError('No write allowed')
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/'source';p.write_text('test')
            plan={'kind':'weekly_to_airtable','base':'appTest','table':'tblTest','source':str(p),'source_sha256':b.digest(p),'changes':[{'pid':'NXA0001','record':'rec1','field':b.FIELDS['name'][0],'field_name':'name','type':'singleLineText','old':'old','new':'new'}]}
            with self.assertRaises(ValueError):b.apply_airtable(plan,API(),pathlib.Path(td)/'journal.json')

if __name__=='__main__':unittest.main(verbosity=2)
