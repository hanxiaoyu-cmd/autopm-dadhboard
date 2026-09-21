"""Model provenance regression tests for the colored weekly-report fields."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from autopm.deepseek import DeepSeekClient, DeepSeekError, SYSTEM_PROMPT, validate_model_project
from autopm.workbook import SUPPLEMENTAL_FIELDS, supplemental_entries
from test_deepseek import evidence_fixture, response


def colored_evidence():
    evidence = evidence_fixture()
    block = evidence['projects'][0]
    block['cells'] = [c for c in block['cells'] if c['address'] != 'L10']
    next(c for c in block['cells'] if c['address'] == 'P2')['text'] = 'XPT Lead'
    next(c for c in block['cells'] if c['address'] == 'L9')['merged_range'] = 'L9:U9'
    for address, row, col, text, merged in [
        ('P3', 3, 16, 'NPD Lead', None), ('R3', 3, 18, 'Alex', None),
        ('P4', 4, 16, 'PMO', None), ('R4', 4, 18, 'Liz Wolf', None),
        ('L10', 10, 12, 'Total', 'L10:M10'), ('N10', 10, 14, 'Open', 'N10:O10'),
        ('P10', 10, 16, 'Verify', None), ('Q10', 10, 17, 'Ready to close', 'Q10:R10'),
        ('S10', 10, 19, 'Closed', None), ('T10', 10, 20, 'Jira Link', 'T10:U10'),
        ('L11', 11, 12, '10', 'L11:M11'), ('N11', 11, 14, '0', 'N11:O11'),
        ('P11', 11, 16, '2', None), ('Q11', 11, 17, '3', 'Q11:R11'),
        ('S11', 11, 19, '5', None), ('T11', 11, 20, 'https://jira.example/NXA0005', 'T11:U11'),
        ('L12', 12, 12, 'Next PLM', 'L12:O12'),
        ('P12', 12, 16, 'MP workflow to be released by Oct 15', 'P12:U12'),
    ]:
        block['cells'].append({'ref': f"'Report'!{address}", 'address': address,
                               'row': row, 'col': col, 'text': text, 'fill': {}, 'merged_range': merged})
    return evidence


def colored_output(block):
    fields = {
        'npi_lead': {'value': 'Levin', 'evidence': ["'Report'!P2", "'Report'!R2"]},
        'npd_lead': {'value': 'Alex', 'evidence': ["'Report'!P3", "'Report'!R3"]},
        'pmo': {'value': 'Liz Wolf', 'evidence': ["'Report'!P4", "'Report'!R4"]},
    }
    for entry in supplemental_entries(block):
        refs = [entry['heading']['ref'], entry['value']['ref']]
        if entry.get('context'):
            refs.insert(0, entry['context']['ref'])
        fields[entry['key']] = {'value': entry['value']['text'], 'evidence': refs}
    return {'project_id': 'NXA0005', 'fields': fields, 'tasks': [], 'issues': []}


class ColoredModelFieldTests(unittest.TestCase):
    def setUp(self):
        self.evidence = colored_evidence()
        self.block = self.evidence['projects'][0]

    def test_xpt_roles_jira_zero_and_next_plm_are_literal_fields(self):
        output = colored_output(self.block)
        self.assertEqual(set(output['fields']) & SUPPLEMENTAL_FIELDS, SUPPLEMENTAL_FIELDS)
        result = validate_model_project(output, self.block)
        self.assertEqual(result['fields']['npi_lead'], 'Levin')
        self.assertEqual(result['fields']['npd_lead'], 'Alex')
        self.assertEqual(result['fields']['pmo'], 'Liz Wolf')
        self.assertEqual(result['fields']['jira_open'], '0')
        self.assertEqual(result['fields']['jira_link'], 'https://jira.example/NXA0005')
        self.assertEqual(result['fields']['next_plm'], 'MP workflow to be released by Oct 15')
        self.assertEqual(result['tasks'], [])

    def test_model_input_contains_complete_coordinate_index_and_preserves_zero(self):
        client = DeepSeekClient('fixture-key', workers=1)
        with patch.object(client, '_request', return_value=response(colored_output(self.block))) as request:
            result = client.parse(self.evidence)
        payload = request.call_args.args[0]
        model_input = json.loads(payload['messages'][1]['content'].split('\n', 1)[1])
        self.assertEqual({entry['key'] for entry in model_input['supplemental_fields']}, SUPPLEMENTAL_FIELDS)
        self.assertTrue(SUPPLEMENTAL_FIELDS <= set(model_input['source_map']['fields']))
        self.assertEqual(model_input['source_map']['fields']['npi_lead'], ["'Report'!P2", "'Report'!R2"])
        supplied = {cell['ref']: cell['text'] for cell in model_input['cells']}
        self.assertEqual(supplied["'Report'!N11"], '0')
        self.assertNotIn("'Report'!F23", supplied)
        self.assertEqual(result['projects'][0]['fields']['jira_open'], '0')
        self.assertEqual(result['extraction_stats']['rejected_model_items'], 0)
        self.assertIn('XPT Lead or NPI Lead -> npi_lead', SYSTEM_PROMPT)
        self.assertIn('Never calculate totals', SYSTEM_PROMPT)

    def test_value_only_evidence_reconstructs_real_column_and_context(self):
        output = colored_output(self.block)
        output['fields']['jira_open']['evidence'] = ["'Report'!N11"]
        result = validate_model_project(output, self.block)
        self.assertEqual(set(result['evidence']['fields']['jira_open']),
                         {"'Report'!L9", "'Report'!N10", "'Report'!N11"})

    def test_equal_zeroes_do_not_allow_other_jira_column_evidence(self):
        next(c for c in self.block['cells'] if c['address'] == 'L11')['text'] = '0'
        output = colored_output(self.block)
        for refs in (["'Report'!L9", "'Report'!L10", "'Report'!L11"],
                     ["'Report'!L9", "'Report'!N10", "'Report'!N11", "'Report'!L11"]):
            with self.subTest(refs=refs):
                output['fields']['jira_open']['evidence'] = refs
                with self.assertRaises(DeepSeekError):
                    validate_model_project(output, self.block)

    def test_wrong_counts_and_cross_project_references_are_rejected(self):
        output = colored_output(self.block)
        for value, refs in [('9', ["'Report'!L10", "'Report'!L11"]),
                            ('0', ["'Other Project'!N10", "'Other Project'!N11"]),
                            ('0', ["'Report'!N10", "'Report'!N11"])]:
            with self.subTest(value=value, refs=refs):
                output['fields']['jira_total'] = {'value': value, 'evidence': refs}
                with self.assertRaises(DeepSeekError):
                    validate_model_project(output, self.block)

    def test_generic_open_and_total_outside_jira_cannot_be_used(self):
        for heading, target in [('Open', 'jira_open'), ('Total', 'jira_total')]:
            with self.subTest(heading=heading):
                block = deepcopy(self.block)
                block['cells'].extend([
                    {'ref': "'Report'!H2", 'row': 2, 'col': 8, 'text': heading, 'fill': {}},
                    {'ref': "'Report'!I2", 'row': 2, 'col': 9, 'text': '0', 'fill': {}},
                ])
                output = colored_output(block)
                output['fields'][target] = {'value': '0', 'evidence': ["'Report'!H2", "'Report'!I2"]}
                with self.assertRaises(DeepSeekError):
                    validate_model_project(output, block)

    def test_blank_or_invalid_jira_count_cannot_be_filled_from_another_cell(self):
        for text in ('', 'N/A', '-1', '1.5', '001', '=1+1'):
            with self.subTest(text=text):
                block = deepcopy(self.block)
                next(c for c in block['cells'] if c['address'] == 'N11')['text'] = text
                output = colored_output(block)
                output['fields']['jira_open'] = {'value': '2', 'evidence': ["'Report'!P10", "'Report'!P11"]}
                with self.assertRaises(DeepSeekError):
                    validate_model_project(output, block)

    def test_next_plm_cannot_be_converted_to_a_task_even_when_it_is_a_date(self):
        next(c for c in self.block['cells'] if c['address'] == 'P12')['text'] = '2026-10-15'
        output = colored_output(self.block)
        output['tasks'] = [{'name': 'Next PLM', 'date': '2026-10-15', 'completed': False,
                            'evidence': ["'Report'!L12", "'Report'!P12"]}]
        with self.assertRaisesRegex(DeepSeekError, '时间线'):
            validate_model_project(output, self.block)

    def test_xpt_cannot_replace_other_people_roles(self):
        for key in ('npd_lead', 'pmo', 'pm', 'tpm'):
            with self.subTest(key=key):
                output = colored_output(self.block)
                output['fields'][key] = {'value': 'Levin', 'evidence': ["'Report'!P2", "'Report'!R2"]}
                with self.assertRaises(DeepSeekError):
                    validate_model_project(output, self.block)

    def test_whitelist_and_prompt_changes_invalidate_cached_responses(self):
        with tempfile.TemporaryDirectory() as directory:
            client = DeepSeekClient('fixture-key', workers=1, cache_dir=Path(directory))
            indexed = {'supplemental_fields': [{'key': 'jira_open', 'value': "'Report'!N11"}]}
            current = client._cache_path(self.block, indexed)
            self.assertNotEqual(current, client._cache_path(self.block, {}))
            old_client = DeepSeekClient('fixture-key', workers=1, cache_dir=Path(directory),
                                        system_prompt='Jira/safety/third-party gray sections are excluded.')
            self.assertNotEqual(current, old_client._cache_path(self.block, indexed))


if __name__ == '__main__':
    unittest.main()
