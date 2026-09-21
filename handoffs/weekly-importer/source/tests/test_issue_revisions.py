import copy
import tempfile
import unittest
from test_sync import fixture, FakeClient
from autopm.sync import build_plan, apply_plan
from unittest.mock import patch


class IssueRevisionTests(unittest.TestCase):
    def setup_case(self):
        snapshot, report = fixture()
        report['extraction_mode'] = 'deepseek'
        old = 'Tooling transfer shipment delayed because injection parts are incomplete.'
        item = {'text': old.replace('are incomplete', 'remain incomplete; recovery expected next week'),
                'action': 'Supplier to finish injection and confirm revised shipment plan.',
                'risk': 'H', 'due_date': '2026-09-18', 'source': "'Report'!B112"}
        report['projects'][0]['issues'] = [item]
        snapshot['records']['tbl_issues'] = [{'id':'recIssue', 'fields':{
            'fld_issues_text':old, 'fld_issues_project':['recProject'],
            'fld_issues_action':item['action'], 'fld_issues_record_date':'2026-08-01',
            'fld_issues_due_date':'2026-09-10', 'fld_issues_risk':'Medium'}}]
        return snapshot, report

    def issues(self, plan):
        return [c for c in plan['changes'] if c['kind']=='issues']

    def test_rules_keep_similar_rows_separate_and_reimport_is_idempotent(self):
        snapshot, report = self.setup_case()
        report['extraction_mode'] = 'rules'
        second = copy.deepcopy(report['projects'][0]['issues'][0])
        second['text'] += ' A second shipment is affected.'
        report['projects'][0]['issues'].append(second)
        original = copy.deepcopy(snapshot['records']['tbl_issues'][0])
        with patch('autopm.issue_matching.match_revisions', side_effect=AssertionError('rules must not merge')):
            plan = build_plan(report, snapshot)
            self.assertEqual(plan['issue_matching_policy'], 'exact_only')
            ops = self.issues(plan)
            self.assertEqual(len(ops), 2)
            self.assertTrue(all(op['record_id'] is None for op in ops))
            self.assertTrue(all('issue_match_guard' not in op for op in ops))
            client = FakeClient(snapshot)
            with tempfile.TemporaryDirectory() as folder:
                result = apply_plan(client, plan, folder)
            self.assertEqual(result['status'], 'completed', result)
            self.assertEqual(len(client.data['records']['tbl_issues']), 3)
            self.assertEqual(client.data['records']['tbl_issues'][0], original)
            self.assertEqual(build_plan(report, client.data)['changes'], [])

    def test_rules_still_update_exact_issue_without_creating_duplicate(self):
        snapshot, report = self.setup_case()
        report['extraction_mode'] = 'rules'
        report['projects'][0]['issues'][0]['text'] = snapshot['records']['tbl_issues'][0]['fields']['fld_issues_text']
        op, = self.issues(build_plan(report, snapshot))
        self.assertEqual(op['record_id'], 'recIssue')
        self.assertNotIn('match_method', op)

    def test_missing_or_unknown_mode_does_not_enable_merging_from_model_name_or_config(self):
        for mode in (None, 'unknown'):
            snapshot, report = self.setup_case()
            report.pop('extraction_mode')
            if mode: report['extraction_mode'] = mode
            report['parser'] = 'deepseek-v4-flash'
            plan = build_plan(report, snapshot, {'deepseek_api_key': 'fixture-only', 'issue_matching_policy': 'revisions'})
            op, = self.issues(plan)
            self.assertIsNone(op['record_id'])
            self.assertEqual(plan['issue_matching_policy'], 'exact_only')

    def test_extractor_owns_mode_and_deepseek_path_enables_revision_matching(self):
        from test_deepseek import evidence_fixture, response
        from autopm.workbook import parse_local
        from autopm.deepseek import DeepSeekClient
        evidence = evidence_fixture()
        self.assertEqual(parse_local(evidence)['extraction_mode'], 'rules')
        with DeepSeekClient('fixture-only', workers=1) as client:
            with patch.object(client, '_request', return_value=response()) as request:
                parsed = client.parse(evidence)
        self.assertTrue(request.called)
        self.assertEqual(parsed['extraction_mode'], 'deepseek')
        snapshot, report = self.setup_case()
        report['extraction_mode'] = parsed['extraction_mode']
        plan = build_plan(report, snapshot)
        op, = self.issues(plan)
        self.assertEqual(plan['issue_matching_policy'], 'revisions')
        self.assertEqual(op['record_id'], 'recIssue')

    def test_revision_updates_id_preserves_created_date_and_reimport_is_idempotent(self):
        snapshot, report = self.setup_case()
        plan = build_plan(report, snapshot)
        issue, = self.issues(plan)
        self.assertEqual(issue['record_id'], 'recIssue')
        self.assertEqual(issue['match_method'], 'unique_issue_revision')
        self.assertNotIn('fld_issues_record_date', issue['fields'])
        client = FakeClient(snapshot)
        with tempfile.TemporaryDirectory() as d:
            result = apply_plan(client, plan, d)
            self.assertEqual(result['status'], 'completed', result)
        self.assertEqual(len(client.data['records']['tbl_issues']), 1)
        self.assertEqual(client.data['records']['tbl_issues'][0]['fields']['fld_issues_text'], report['projects'][0]['issues'][0]['text'])
        self.assertFalse(any(w[0]=='POST' for w in client.writes))
        self.assertEqual(build_plan(report,client.data)['changes'], [])
        with tempfile.TemporaryDirectory() as d:
            result = apply_plan(client, plan, d)
            self.assertEqual(result['status'], 'completed', result)
            self.assertEqual(result['applied'], 0)

    def test_multiple_similar_old_issues_hold_back_without_create(self):
        snapshot, report = self.setup_case()
        other = copy.deepcopy(snapshot['records']['tbl_issues'][0]);other['id']='recOtherIssue'
        other['fields']['fld_issues_text'] += ' Factory VN.'
        snapshot['records']['tbl_issues'].append(other)
        plan=build_plan(report,snapshot)
        self.assertEqual(self.issues(plan), [])
        self.assertTrue(any('未新增或覆盖' in w for w in plan['warnings']))

    def test_two_revisions_cannot_overwrite_one_record(self):
        snapshot, report = self.setup_case()
        item=copy.deepcopy(report['projects'][0]['issues'][0]);item['text']+=' Please expedite.'
        report['projects'][0]['issues'].append(item)
        self.assertEqual(self.issues(build_plan(report,snapshot)), [])

    def test_exact_match_reserved_before_modified_duplicate(self):
        snapshot, report = self.setup_case()
        item=copy.deepcopy(report['projects'][0]['issues'][0])
        item['text']=snapshot['records']['tbl_issues'][0]['fields']['fld_issues_text']
        report['projects'][0]['issues'].append(item)
        ops=self.issues(build_plan(report,snapshot))
        self.assertEqual(len(ops),1)
        self.assertNotIn('fld_issues_text',ops[0]['fields'])

    def test_unrelated_issue_is_new_not_forced_onto_only_record(self):
        snapshot, report = self.setup_case()
        report['projects'][0]['issues']=[{'text':'Battery safety certification failed the overcharge test.','action':'Run an independent electrical safety review.'}]
        op,=self.issues(build_plan(report,snapshot))
        self.assertIsNone(op['record_id'])

    def test_other_project_and_shared_record_never_merged(self):
        for links in (['recOtherProject'],['recProject','recOtherProject']):
            snapshot, report=self.setup_case()
            snapshot['records']['tbl_issues'][0]['fields']['fld_issues_project']=links
            ops=self.issues(build_plan(report,snapshot))
            self.assertTrue(not ops or ops[0]['record_id'] is None)

    def test_changed_matching_evidence_blocks_before_any_write(self):
        for mutation in ('action','new_candidate','title'):
            snapshot, report=self.setup_case();plan=build_plan(report,snapshot)
            client=FakeClient(snapshot)
            if mutation=='new_candidate':
                other=copy.deepcopy(client.data['records']['tbl_issues'][0]);other['id']='recNew'
                client.data['records']['tbl_issues'].append(other)
            else:
                field='fld_issues_action' if mutation=='action' else 'fld_issues_text'
                client.data['records']['tbl_issues'][0]['fields'][field]='Changed by another user'
            with tempfile.TemporaryDirectory() as d:result=apply_plan(client,plan,d)
            self.assertEqual(result['status'],'blocked',result)
            self.assertEqual(client.writes,[])

    def test_title_typo_and_chinese_revision(self):
        for old,new in [
            ('Injection mould validation remains delayed pending the supplier quality review.',
             'Injection mold validation remains delayed pending the supplier quality review.'),
            ('注塑模具验证进度延误，供应商仍未完成质量检查，需要尽快安排复测。',
             '注塑模具验证进度延误，供应商仍未完成质量检查，需要下周安排复测。')]:
            snapshot,report=self.setup_case()
            snapshot['records']['tbl_issues'][0]['fields']['fld_issues_text']=old
            report['projects'][0]['issues'][0]['text']=new
            op,=self.issues(build_plan(report,snapshot))
            self.assertEqual(op['record_id'],'recIssue')

    def test_similar_text_with_different_sku_or_region_is_held(self):
        for old,new in [('Model BU1620 failed the motor endurance quality test.',
                         'Model BU3620 failed the motor endurance quality test.'),
                        ('CN tooling transfer is delayed pending supplier validation.',
                         'VN tooling transfer is delayed pending supplier validation.')]:
            snapshot,report=self.setup_case()
            snapshot['records']['tbl_issues'][0]['fields']['fld_issues_text']=old
            report['projects'][0]['issues'][0]['text']=new
            self.assertEqual(self.issues(build_plan(report,snapshot)),[])

    def test_revision_visible_in_preview_and_retains_action_filter(self):
        from autopm.presentation import build_review_data,filter_change_rows
        snapshot,report=self.setup_case()
        view=build_review_data(report,build_plan(report,snapshot))
        rows=filter_change_rows(view['rows'],kind='issues',action='update')
        self.assertTrue(rows)
        self.assertTrue(all(r['action_label']=='合并更新' and r['match_note'] for r in rows))

    def test_appended_update_to_real_short_issue_never_creates_duplicate(self):
        snapshot,report=self.setup_case()
        snapshot['records']['tbl_issues'][0]['fields']['fld_issues_text']='DQTP failure'
        report['projects'][0]['issues'][0]['text']='DQTP failure Update: follow-up is still in progress.'
        report['projects'][0]['issues'][0]['action']+=' Reconfirm recovery plan.'
        ops=self.issues(build_plan(report,snapshot))
        self.assertEqual(ops[0]['record_id'],'recIssue')
        report['projects'][0]['issues'][0]['action']='An unrelated new action'
        self.assertEqual(self.issues(build_plan(report,snapshot)),[])

    def test_long_issue_continuation_merges_with_changed_action(self):
        snapshot,report=self.setup_case()
        old=snapshot['records']['tbl_issues'][0]['fields']['fld_issues_text']
        report['projects'][0]['issues'][0]['text']=old+' Update: follow-up is still in progress.'
        report['projects'][0]['issues'][0]['action']='Hold a new supplier review meeting.'
        op,=self.issues(build_plan(report,snapshot))
        self.assertEqual(op['record_id'],'recIssue')


if __name__=='__main__':unittest.main()
