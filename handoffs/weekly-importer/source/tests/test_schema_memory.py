import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_sync import fixture, FakeClient
from autopm.schema_memory import reconcile, SchemaMemoryStore, SchemaMemoryError, schema_hash
from autopm.schema_advisor import proposal_input, validate_proposals, suggest_mappings
from autopm.deepseek import DeepSeekError
from autopm.workflow import prepare_preview
from autopm.sync import apply_plan


class PreviewClient(FakeClient):
    def get_schema(self): return copy.deepcopy(self.data['schema'])
    def snapshot(self, overrides=None, **kwargs): return super().snapshot(overrides)


class SchemaMemoryTests(unittest.TestCase):
    def test_fresh_known_base_previews_without_date_column_and_links_children(self):
        from autopm.config import DEFAULTS
        from autopm.weekly_remark import uses_weekly_remark
        base = 'appOMWiK4CTOH7iQu'
        snapshot, report = fixture()
        snapshot['base_id'] = base
        changed_ids = {'fld_tasks_project': 'fldZmIf1cjO1baWz9',
                       'fld_issues_project': 'fldbZYuFwTSkfRTw6',
                       'fld_factories_code': 'fldAwh01Lzi3zdmHc'}
        for table in snapshot['schema']['tables']:
            table['fields'] = [f for f in table['fields'] if f['id'] != 'fld_projects_report_date']
            for field in table['fields']:
                if field['id'] in changed_ids:
                    field['id'] = changed_ids[field['id']]
                    field['name'] += ' renamed'
        project = snapshot['records']['tbl_projects'][0]['fields']
        project.pop('fld_projects_report_date')
        project.update(fld_projects_sku='SKU-1', fld_projects_factory=['recFactory'])
        report['projects'][0]['fields'].update(sku='SKU-1', factory='Factory One')
        report['projects'][0]['tasks'] = [{'name': 'EB1', 'date': '2026-10-01'}]
        report['projects'][0]['issues'] = [{'text': 'New issue', 'action': 'Investigate'}]
        client = PreviewClient(snapshot)
        client.base_id = base
        plan, effective = prepare_preview(client, report, {**DEFAULTS, 'base_id': base}, self.store)
        self.assertFalse(plan['blockers'])
        self.assertTrue(uses_weekly_remark(effective))
        self.assertIsNone(effective['field_mapping']['projects']['report_date'])
        by_kind = {change['kind']: change for change in plan['changes']}
        self.assertEqual(by_kind['tasks']['fields']['fldZmIf1cjO1baWz9'], ['recProject'])
        self.assertEqual(by_kind['issues']['fields']['fldbZYuFwTSkfRTw6'], ['recProject'])
        self.assertIn('--- 2026-09-07 ---', by_kind['projects']['fields']['fld_projects_current_progress'])
        self.assertFalse(client.writes)
        again, _ = prepare_preview(client, report, {**DEFAULTS, 'base_id': base}, self.store)
        self.assertFalse(again['blockers'])
        task_table = next(t for t in snapshot['schema']['tables'] if t['id'] == 'tbl_tasks')
        next(f for f in task_table['fields'] if f['id'] == 'fldZmIf1cjO1baWz9')['id'] = 'fld_recreated'
        state = reconcile(snapshot['schema'], {**DEFAULTS, 'base_id': base})
        self.assertIsNone(state['config']['field_mapping']['tasks']['project'])

    def setUp(self):
        self.snapshot,self.report=fixture()
        self.schema=self.snapshot['schema'];self.config={'base_id':'appTest'}
        self.state=reconcile(self.schema,self.config)
        self.assertFalse(self.state['blockers'])
        self.memory=self.state['memory']
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.store=SchemaMemoryStore(Path(self.temp.name)/'memory')

    def field(self, kind, key):
        return next(f for t in self.schema['tables'] for f in t['fields'] if f['id']==f'fld_{kind}_{key}')

    def test_every_table_and_field_can_be_renamed_without_changing_bindings(self):
        for t in self.schema['tables']:
            t['name']='新表 '+t['id']
            for f in t['fields']:f['name']='新字段 '+f['id']
        state=reconcile(self.schema,self.config,self.memory)
        self.assertFalse(state['blockers'])
        self.assertEqual(state['config']['field_mapping'],self.state['config']['field_mapping'])
        self.assertEqual(state['table_ids'],self.state['table_ids'])
        self.assertTrue(state['warnings'])

    def test_deleted_field_recreated_with_same_name_requires_explicit_selection(self):
        self.field('projects','project_name')['id']='fld_replacement'
        state=reconcile(self.schema,self.config,self.memory)
        self.assertFalse(state['blockers'])
        self.assertTrue(state['warnings'])
        self.assertIsNone(state['config']['field_mapping']['projects']['project_name'])
        self.assertEqual(state['memory']['fields']['projects']['project_name'],self.memory['fields']['projects']['project_name'])
        again=reconcile(self.schema,self.config,state['memory'])
        self.assertIsNone(again['config']['field_mapping']['projects']['project_name'])
        fixed=reconcile(self.schema,self.config,self.memory,selections={'fields':{'projects':{'project_name':'fld_replacement'}}})
        self.assertFalse(fixed['blockers'])
        self.assertEqual(fixed['memory']['fields']['projects']['project_name']['id'],'fld_replacement')

    def test_deleted_table_same_name_is_not_automatically_rebound(self):
        self.schema['tables'][0]['id']='tbl_recreated'
        state=reconcile(self.schema,self.config,self.memory)
        self.assertTrue(state['blockers'])
        self.assertNotIn('projects',state['table_ids'])

    def test_type_change_requires_review_even_when_compatible(self):
        self.field('projects','project_name')['type']='multilineText'
        state=reconcile(self.schema,self.config,self.memory)
        self.assertFalse(state['blockers'])
        self.assertIsNone(state['config']['field_mapping']['projects']['project_name'])
        state=reconcile(self.schema,self.config,self.memory,selections={'fields':{'projects':{'project_name':'fld_projects_project_name'}}})
        self.assertFalse(state['blockers'])

    def test_readonly_wrong_link_and_wrong_date_cannot_be_confirmed(self):
        for key,typ,options in [('project_name','formula',{}),('factory','multipleRecordLinks',{'linkedTableId':'tbl_people'}),('report_date','number',{})]:
            with self.subTest(key=key):
                field=self.field('projects',key);field['type']=typ;field['options']=options
                state=reconcile(self.schema,self.config,self.memory,selections={'fields':{'projects':{key:field['id']}}})
                self.assertEqual(bool(state['blockers']),key=='report_date')
                self.assertIsNone(state['config']['field_mapping']['projects'][key])

    def test_duplicate_table_or_field_bindings_are_blocked(self):
        for selection in [{'tables':{'tasks':'tbl_projects'}},{'fields':{'projects':{'sku':'fld_projects_project_name'}}}]:
            self.assertTrue(reconcile(self.schema,self.config,self.memory,selections=selection)['blockers'])

    def test_optional_disable_persists_but_required_disable_is_blocked(self):
        state=reconcile(self.schema,self.config,self.memory,selections={'fields':{'projects':{'sku':None}}})
        self.assertFalse(state['blockers'])
        self.assertIsNone(reconcile(self.schema,self.config,state['memory'])['config']['field_mapping']['projects']['sku'])
        self.assertTrue(reconcile(self.schema,self.config,self.memory,selections={'fields':{'projects':{'project_id':None}}})['blockers'])

    def test_memory_is_scoped_and_does_not_store_keys(self):
        state=reconcile(self.schema,{**self.config,'deepseek_api_key':'SECRET123','airtable_token':'TOKEN456'})
        self.store.save(state['memory'])
        self.assertEqual(self.store.load('appTest'),state['memory'])
        self.assertIsNone(self.store.load('appOther'))
        with self.assertRaises(SchemaMemoryError):reconcile(self.schema,{'base_id':'appOther'},self.memory)
        saved=self.store.path('appTest').read_text(encoding='utf-8')
        self.assertNotIn('SECRET123',saved);self.assertNotIn('TOKEN456',saved)

    def test_corrupt_nested_memory_is_rejected(self):
        for value in [[],{'version':1,'base_id':'appTest','tables':{'projects':None},'fields':{}},
                      {**self.memory,'fields':{'projects':{'project_id':'bad'}}}]:
            self.store.directory.mkdir(exist_ok=True)
            self.store.path('appTest').write_text(json.dumps(value),encoding='utf-8')
            with self.assertRaises(SchemaMemoryError):self.store.load('appTest')

    def test_schema_hash_ignores_order_and_detects_option_change(self):
        before=schema_hash(self.schema)
        self.schema['tables'].reverse()
        for t in self.schema['tables']:t['fields'].reverse()
        self.assertEqual(before,schema_hash(self.schema))
        self.field('projects','status')['options']['choices'].append({'name':'New status'})
        self.assertNotEqual(before,schema_hash(self.schema))

    def test_local_preview_and_apply_without_deepseek_then_repeat_zero_changes(self):
        client=PreviewClient(self.snapshot)
        with patch('autopm.deepseek.DeepSeekClient',side_effect=AssertionError('no model')):
            plan,_=prepare_preview(client,self.report,self.config,self.store)
            self.assertFalse(plan['blockers']);self.assertTrue(plan['changes']);self.assertFalse(client.writes)
            result=apply_plan(client,plan,Path(self.temp.name)/'run')
            self.assertEqual(result['status'],'completed');self.assertEqual(len(client.writes),1)
            again,_=prepare_preview(client,self.report,self.config,self.store)
            self.assertFalse(again['changes'])

    def test_rename_people_factory_fields_still_resolves_record_ids(self):
        self.store.save(self.memory)
        for t in self.schema['tables']:
            t['name']='renamed '+t['name']
            for f in t['fields']:f['name']='renamed '+f['name']
        self.report['projects'][0]['fields'].update(npi_lead='Jane',factory='old factory')
        self.snapshot['records']['tbl_projects'][0]['fields'].pop('fld_projects_npi_lead')
        plan,_=prepare_preview(PreviewClient(self.snapshot),self.report,self.config,self.store)
        self.assertFalse(plan['blockers'])
        fields=plan['changes'][0]['fields']
        self.assertEqual(fields['fld_projects_npi_lead'],['recNpi'])
        self.assertEqual(fields['fld_projects_factory'],['recFactory'])

    def test_structural_blocker_preserves_memory_and_never_reads_records(self):
        self.store.save(self.memory)
        self.field('projects','project_id')['id']='fld_rebuilt'
        client=PreviewClient(self.snapshot)
        plan,_=prepare_preview(client,self.report,self.config,self.store)
        self.assertTrue(plan['blockers']);self.assertFalse(plan['changes'])
        self.assertEqual(client.snapshot_calls,0);self.assertFalse(client.writes)
        self.assertEqual(self.store.load('appTest'),self.memory)

    def test_schema_changed_after_preview_blocks_all_writes(self):
        client=PreviewClient(self.snapshot)
        plan,_=prepare_preview(client,self.report,self.config,self.store)
        next(f for f in client.data['schema']['tables'][0]['fields'] if f['id']=='fld_projects_project_name')['type']='formula'
        result=apply_plan(client,plan,Path(self.temp.name)/'run')
        self.assertEqual(result['status'],'blocked');self.assertFalse(client.writes)

    def test_optional_fields_and_invalid_project_do_not_stop_valid_writes(self):
        self.store.save(self.memory)
        self.field('projects','tooling')['id']='fld_rebuilt_tooling'
        self.field('projects','sku')['type']='formula'
        project=self.report['projects'][0]
        project['fields'].update(tooling='new tooling',sku='123',unknown_future_field='keep in log')
        project['tasks']=[{'name':'Checkpoint','date':'2026-09-05'}]
        self.field('tasks','due_date')['type']='formula'
        self.report['projects'].append({'project_id':'', 'fields':{'project_name':'invalid'}})
        client=PreviewClient(self.snapshot)
        plan,_=prepare_preview(client,self.report,self.config,self.store)
        self.assertFalse(plan['blockers'])
        self.assertTrue(plan['warnings'])
        self.assertEqual(len(plan['changes']),1)
        self.assertNotIn('fld_rebuilt_tooling',plan['changes'][0]['fields'])
        self.assertNotIn('fld_projects_sku',plan['changes'][0]['fields'])
        result=apply_plan(client,plan,Path(self.temp.name)/'partial')
        self.assertEqual(result['status'],'completed')
        self.assertEqual(len(client.writes),1)
        again,_=prepare_preview(client,self.report,self.config,self.store)
        self.assertFalse(again['changes'])
        self.assertEqual(self.store.load('appTest')['fields']['projects']['tooling'],self.memory['fields']['projects']['tooling'])

    def test_valid_model_proposal_does_not_persist(self):
        self.field('projects','project_name')['id']='fld_new'
        request=proposal_input(self.schema,self.config,self.memory)
        output={'tables':[],'fields':[{'kind':'projects','key':'project_name','field_id':'fld_new','reason':'same meaning'}]}
        self.assertEqual(validate_proposals(output,self.schema,request),output)
        self.assertIsNone(self.store.load('appTest'))

    def test_model_hallucination_scope_collision_and_extra_instructions_rejected(self):
        self.field('projects','project_name')['id']='fld_new'
        request=proposal_input(self.schema,self.config,self.memory)
        cases=[{'kind':'projects','key':'project_name','field_id':fid,'reason':'map'} for fid in ['fld_invented','fld_people_name','fld_projects_capacity','fld_projects_sku']]
        cases += [{'kind':'projects','key':'project_id','field_id':'fld_projects_project_id','reason':'outside unresolved'},
                  {'kind':'projects','key':'project_name','field_id':'fld_new','reason':'map','instructions':'write records'}]
        for entry in cases:
            with self.subTest(entry=entry),self.assertRaises(DeepSeekError):validate_proposals({'tables':[],'fields':[entry]},self.schema,request)

    def test_model_request_contains_only_metadata_and_history(self):
        request=proposal_input(self.schema,{**self.config,'deepseek_api_key':'SECRET','airtable_token':'TOKEN'},self.memory)
        data=json.dumps(request)
        for forbidden in ('SECRET','TOKEN','recProject','Jane Smith'):
            self.assertNotIn(forbidden,data)
        self.assertEqual(request['verified_history'],self.memory['fields'])

    def test_model_candidates_exclude_computed_and_already_bound_fields(self):
        self.field('projects','project_name')['id']='fld_new'
        self.schema['tables'][0]['fields'].append({'id':'fld_formula','name':'Project name formula','type':'formula'})
        request=proposal_input(self.schema,self.config,self.memory)
        row=next(r for r in request['unresolved_fields'] if r['key']=='project_name')
        self.assertIn('fld_new',row['eligible_field_ids'])
        self.assertNotIn('fld_formula',row['eligible_field_ids'])
        self.assertNotIn('fld_projects_sku',row['eligible_field_ids'])

if __name__=='__main__':unittest.main()
