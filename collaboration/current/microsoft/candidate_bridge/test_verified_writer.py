import copy
import json
import pathlib
import tempfile
import unittest
import bridge
from verified_writer import ReconciliationRequired


class API:
    base='appTest'; table='tblProjects'; tasks='tblTasks'; issues='tblIssues'
    def __init__(self):
        self.data={self.tasks:{},self.table:{'recProject':{'id':'recProject','fields':{'name':'Old'}}}}
        self.posts=0;self.patches=0;self.reads=0;self.failure=None
    def schema(self):
        return {'tables':[{'id':self.tasks,'fields':[{'id':'name','type':'singleLineText'},{'id':'project','type':'multipleRecordLinks'}]},
            {'id':self.table,'fields':[{'id':'name','type':'singleLineText'}]}]}
    def records(self, table): return copy.deepcopy(list(self.data[table].values()))
    def request(self,path,method='GET',body=None):
        parts=path.split('?')[0].split('/');table=parts[1]
        if method=='POST':
            self.posts+=1
            rid='recNew'+str(self.posts)
            self.data[table][rid]={'id':rid,'fields':copy.deepcopy(body['records'][0]['fields'])}
            if self.failure=='timeout':raise TimeoutError('Response lost after accepted POST')
            if self.failure=='empty':return {'records':[]}
            return {'records':[{'id':rid}]}
        if method=='PATCH':
            self.patches+=1
            for row in body['records']:self.data[table][row['id']]['fields'].update(row['fields'])
            return {}
        self.reads+=1
        if self.failure=='read_timeout':raise TimeoutError('Read failed')
        row=copy.deepcopy(self.data[table][parts[2]])
        if self.failure=='wrong_value':row['fields']['name']='Wrong'
        return row


class WriterTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.temp.name)
        source=self.root/'source';source.write_text('fixture')
        self.journal=self.root/'journal.json';self.api=API()
        self.plan={'kind':'weekly_to_airtable','base':self.api.base,'table':self.api.table,
            'source':str(source),'source_sha256':bridge.digest(source),'changes':[
                {'op':'create','pid':'NXA0001','table':self.api.tasks,'new':{'name':'A','project':['recProject']},
                 'identity':{'name':'A','project':['recProject']}}]}
    def tearDown(self):self.temp.cleanup()
    def apply(self):return bridge.apply_airtable(self.plan,self.api,self.journal)
    def test_create_requires_independent_readback(self):
        result=self.apply();self.assertEqual(result['status'],'verified');self.assertEqual(self.api.reads,1)
        self.assertEqual(result['pending'],[]);self.assertEqual(result['created'][0]['record'],'recNew1')
    def test_wrong_readback_never_verified(self):
        self.api.failure='wrong_value'
        with self.assertRaises(ReconciliationRequired):self.apply()
        receipt=json.loads(self.journal.read_text())
        self.assertEqual(receipt['status'],'needs_reconciliation');self.assertEqual(len(receipt['pending']),1)
    def test_empty_create_response_never_verified(self):
        self.api.failure='empty'
        with self.assertRaises(ReconciliationRequired):self.apply()
        self.assertNotEqual(json.loads(self.journal.read_text())['status'],'verified')
    def test_timeout_after_create_does_not_repeat_post(self):
        self.api.failure='timeout'
        with self.assertRaises(TimeoutError):self.apply()
        self.api.failure=None
        with self.assertRaises(ReconciliationRequired):self.apply()
        self.assertEqual(self.api.posts,1)
    def test_failed_readback_can_resume_known_id_without_create(self):
        self.api.failure='read_timeout'
        with self.assertRaises(TimeoutError):self.apply()
        self.api.failure=None
        self.assertEqual(self.apply()['status'],'verified');self.assertEqual(self.api.posts,1)
    def test_receipt_replay_does_not_overwrite_later_change(self):
        self.apply();self.api.data[self.api.tasks]['recNew1']['fields']['name']='New legitimate value'
        self.assertEqual(self.apply()['status'],'verified')
        self.assertEqual(self.api.posts,1);self.assertEqual(self.api.patches,0)
    def test_new_batch_reconciles_existing_create(self):
        self.apply();self.journal=self.root/'second.json'
        receipt=self.apply();self.assertEqual(self.api.posts,1)
        self.assertEqual(receipt['created'][0]['origin'],'already_present')
    def test_existing_identity_with_different_values_blocks(self):
        self.api.data[self.api.tasks]['existing']={'id':'existing','fields':{'name':'A','project':['recProject'],'note':'Changed'}}
        self.plan['changes'][0]['new']['name']='B'
        with self.assertRaises(ValueError):self.apply()
        self.assertEqual(self.api.posts,0)
    def test_duplicate_creates_block_before_any_post(self):
        self.plan['changes']*=2
        with self.assertRaises(ValueError):self.apply()
        self.assertEqual(self.api.posts,0)
    def test_missing_updated_record_blocks(self):
        self.plan['changes']=[{'pid':'NXA0001','record':'deleted','field':'name','field_name':'Name','type':'singleLineText','old':None,'new':'New'}]
        with self.assertRaises(ValueError):self.apply()
        self.assertEqual(self.api.patches,0)
    def test_update_readback_and_before_image(self):
        self.plan['changes']=[{'pid':'NXA0001','record':'recProject','field':'name','field_name':'Name','type':'singleLineText','old':'Old','new':'New'}]
        receipt=self.apply();self.assertEqual(self.api.patches,1);self.assertEqual(receipt['status'],'verified')
        self.assertEqual(receipt['before'][0]['fields']['name'],'Old')
    def test_legacy_journal_is_not_destroyed(self):
        self.journal.write_text('{"status":"verified"}')
        with self.assertRaises(ReconciliationRequired):self.apply()
        self.assertEqual(json.loads(self.journal.read_text()),{'status':'verified'})

if __name__=='__main__':unittest.main()
