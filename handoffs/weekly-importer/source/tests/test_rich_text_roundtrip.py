"""Regression for Airtable's ordered-list normalization, not business edits."""
import json
import re
import tempfile
import unittest
from pathlib import Path

from test_sync import fixture, FakeClient
from autopm.sync import _equivalent, build_plan, apply_plan
from autopm.weekly_remark import merge_weekly_remark


def airtable_list_format(text):
    # Observed server behavior: restart each contiguous ordered list at 1.
    number = 0
    lines = []
    for line in text.splitlines():
        match = re.match(r"^\d+\. (.*)$", line)
        number = number + 1 if match else 0
        lines.append(f"{number}. {match[1]}" if match else line)
    return '\n'.join(lines) + '\n'


class FormattingClient(FakeClient):
    def update_record(self, table_id, record_id, fields):
        types = {f['id']: f['type'] for t in self.data['schema']['tables'] for f in t['fields']}
        fields = {fid: airtable_list_format(value) if types[fid] == 'richText' else value
                  for fid, value in fields.items()}
        return super().update_record(table_id, record_id, fields)


class RichTextTests(unittest.TestCase):
    def test_only_markdown_numbering_is_equivalent(self):
        field = {'type': 'richText'}
        text = '--- 2026-09-17 ---\nIntro\n3. Ship 10 units by Sep 11\n4. On Hold'
        self.assertTrue(_equivalent(text, airtable_list_format(text), field))
        self.assertFalse(_equivalent(text, airtable_list_format(text).replace('10 units', '11 units'), field))
        for literal in ['```\n3. literal\n```', '~~~\n3. literal\n~~~', '3\\. literal', '    3. code', '3.No space']:
            self.assertFalse(_equivalent(literal, literal.replace('3', '1'), field))
        self.assertFalse(_equivalent(text, airtable_list_format(text), {'type':'multilineText'}))

    def test_reimport_preserves_history_without_appending_duplicate_progress(self):
        old = 'Manual note\n--- 2026-09-17 ---\nIntro\n1. Ship 10 units\n2. On Hold\n'
        result = merge_weekly_remark(old, '2026-09-17', {'current_progress':'Intro\n3. Ship 10 units\n4. On Hold'}, rich_text=True)
        self.assertEqual(result, old)

    def test_real_content_mismatch_keeps_record_id_and_written_evidence(self):
        snapshot, report = fixture()
        class ChangedByServer(FakeClient):
            def update_record(self, table, record, fields):
                return super().update_record(table, record, {fid:'Unexpected content' for fid in fields})
        client = ChangedByServer(snapshot)
        with tempfile.TemporaryDirectory() as folder:
            result = apply_plan(client, build_plan(report, snapshot), folder)
            journal = json.loads((Path(folder)/'write_journal.json').read_text(encoding='utf-8'))
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(result['written_unverified'], 1)
        self.assertEqual(result['applied'], 0)
        self.assertEqual(result['operations'][0]['record_id'], 'recProject')
        self.assertEqual(result['operations'][0]['reason'], 'verification_failed')
        self.assertIn('verification', journal['operations'][0])
        self.assertEqual(len(client.writes), 1)
