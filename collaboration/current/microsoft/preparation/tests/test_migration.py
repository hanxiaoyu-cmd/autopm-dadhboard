import copy
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from prepare_migration import build_package


def example():
    return {'Programs': [{'ProgramKey': 'P'}],
            'Projects': [{'ProjectKey': 'J1'}, {'ProjectKey': 'J2'}, {'ProjectKey': 'UNASSIGNED'}],
            'SKUs': [{'SnapshotSkuKey': 'S', 'ProgramKey': 'P', 'SKUStatus': 'Launched'}],
            'ProjectSKUs': [{'ProjectKey': 'J1', 'SnapshotSkuKey': 'S'},
                            {'ProjectKey': 'J2', 'SnapshotSkuKey': 'S'}],
            'ProgramProjects': [{'ProgramKey': 'P', 'ProjectKey': 'J1'}]}


class MigrationTests(unittest.TestCase):
    def test_many_to_many_does_not_copy_master_status(self):
        payload, report = build_package(example())
        self.assertEqual(len(payload['ProjectSKUsCandidate']), 2)
        self.assertTrue(all(r['ExecutionStatus'] is None for r in payload['ProjectSKUsCandidate']))
        self.assertEqual(len(payload['ProgramProjectsDerived']), 2)
        self.assertFalse(report['production_ready'])

    def test_unassigned_not_dropped(self):
        payload, _ = build_package(example())
        self.assertEqual(payload['UnassignedProjects'], ['UNASSIGNED'])
        self.assertEqual(len(payload['Projects']), 3)

    def test_duplicate_key_not_silently_overwritten(self):
        data = example()
        data['Projects'].append({'ProjectKey': 'J1', 'Title': 'Duplicate'})
        payload, report = build_package(data)
        self.assertEqual(len(payload['Projects']), 4)
        self.assertTrue(any(r['type'] == 'invalid_identity' for r in report['integrity_errors']))
        self.assertFalse(any(r['ProjectKey'] == 'J1' for r in payload['ProjectSKUsCandidate']))

    def test_orphan_relation_preserved_in_source(self):
        data = example()
        data['ProjectSKUs'].append({'ProjectKey': 'J1', 'SnapshotSkuKey': 'MISSING'})
        payload, report = build_package(data)
        self.assertEqual(len(payload['ProjectSKUsSource']), 3)
        self.assertTrue(any(r['type'] == 'orphan_project_sku' for r in report['integrity_errors']))

    def test_duplicates_do_not_inflate_counts(self):
        data = example()
        data['ProjectSKUs'].append(data['ProjectSKUs'][0].copy())
        payload, report = build_package(data)
        self.assertEqual(len(payload['ProgramProjectsDerived']), 2)
        self.assertEqual(len(payload['ProjectSKUsSource']), 3)
        self.assertTrue(any(r['type'] == 'duplicate_project_sku' for r in report['integrity_errors']))

    def test_historical_links_are_compared_not_discarded(self):
        data = example()
        data['ProgramProjects'].append({'ProgramKey': 'P', 'ProjectKey': 'UNASSIGNED'})
        _, report = build_package(data)
        self.assertEqual({r['kind'] for r in report['relationship_discrepancies']}, {'historical_only', 'derived_only'})

    def test_deterministic_and_no_source_mutation(self):
        data = example()
        before = copy.deepcopy(data)
        self.assertEqual(build_package(data), build_package(data))
        self.assertEqual(data, before)

    def test_unlinked_sku_orphan_is_reported(self):
        data = example()
        data['SKUs'].append({'SnapshotSkuKey': 'S2', 'ProgramKey': 'UNKNOWN'})
        _, report = build_package(data)
        self.assertTrue(any(r['type'] == 'invalid_master_program' for r in report['integrity_errors']))


if __name__ == '__main__':
    unittest.main()
