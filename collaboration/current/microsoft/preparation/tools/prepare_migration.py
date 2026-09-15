"""Offline migration preparation. Never connects to or writes to any cloud system."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()


def build_package(data):
    """Keep every source row; ambiguity blocks readiness rather than guessing identities."""
    definitions = {'Programs': 'ProgramKey', 'Projects': 'ProjectKey', 'SKUs': 'SnapshotSkuKey'}
    errors = []
    indexes = {}
    for table, key in definitions.items():
        rows = data[table]
        counts = Counter(r.get(key, '') for r in rows)
        for value, count in counts.items():
            if not value or count > 1:
                errors.append({'type': 'invalid_identity', 'table': table, 'key': value, 'count': count})
        indexes[table] = {r[key]: r for r in rows if r.get(key) and counts[r[key]] == 1}

    links = []
    seen = set()
    for n, rel in enumerate(data['ProjectSKUs'], 1):
        pk, sk = rel.get('ProjectKey'), rel.get('SnapshotSkuKey')
        pair = (pk, sk)
        if pk not in indexes['Projects'] or sk not in indexes['SKUs']:
            errors.append({'type': 'orphan_project_sku', 'row': n, 'project': pk, 'sku': sk})
            continue
        if pair in seen:
            errors.append({'type': 'duplicate_project_sku', 'row': n, 'project': pk, 'sku': sk})
            continue
        seen.add(pair)
        links.append({'ProjectKey': pk, 'SnapshotSkuKey': sk,
                      'ExecutionStatus': None, 'OverrideDate': None,
                      'MigrationState': 'Pending source reconciliation'})

    derived = set()
    for rel in links:
        program = indexes['SKUs'][rel['SnapshotSkuKey']].get('ProgramKey')
        if program:
            if program not in indexes['Programs']:
                errors.append({'type': 'orphan_sku_program', 'sku': rel['SnapshotSkuKey'], 'program': program})
            else:
                derived.add((program, rel['ProjectKey']))
    # Also check SKU master relationships for SKUs without any Project.
    for row in data['SKUs']:
        program = row.get('ProgramKey')
        if program and program not in indexes['Programs']:
            errors.append({'type': 'invalid_master_program', 'sku': row.get('SnapshotSkuKey'), 'program': program})

    historical = set()
    for n, rel in enumerate(data['ProgramProjects'], 1):
        pair = (rel.get('ProgramKey'), rel.get('ProjectKey'))
        if pair in historical:
            errors.append({'type': 'duplicate_program_project', 'row': n, 'pair': pair})
        historical.add(pair)
        if pair[0] not in indexes['Programs'] or pair[1] not in indexes['Projects']:
            errors.append({'type': 'orphan_program_project', 'row': n, 'pair': pair})

    discrepancies = ([{'kind': 'historical_only', 'ProgramKey': p, 'ProjectKey': j}
                      for p, j in sorted(historical - derived, key=str)] +
                     [{'kind': 'derived_only', 'ProgramKey': p, 'ProjectKey': j}
                      for p, j in sorted(derived - historical, key=str)])
    assigned = {j for p, j in derived}
    payload = {
        'Programs': data['Programs'], 'Projects': data['Projects'], 'SKUs': data['SKUs'],
        'ProjectSKUsCandidate': links,
        'ProjectSKUsSource': data['ProjectSKUs'],
        'ProgramProjectsHistorical': data['ProgramProjects'],
        'ProgramProjectsDerived': [{'ProgramKey': p, 'ProjectKey': j} for p, j in sorted(derived)],
        'UnassignedProjects': [r['ProjectKey'] for r in data['Projects'] if r.get('ProjectKey') not in assigned],
    }
    manifest = {
        'format_version': 1, 'mode': 'offline_preparation', 'production_ready': False,
        'source_fingerprint': fingerprint(data), 'payload_fingerprint': fingerprint(payload),
        'counts': {k: len(v) for k, v in payload.items()},
        'integrity_errors': errors, 'relationship_discrepancies': discrepancies,
        'deployment_blockers': [
            'Dataverse custom table/solution development privilege not available in inspected environment.',
            'SKU snapshot keys are not permanent Airtable record identities; reconcile live source IDs.',
            'Normalized CSV snapshot is not a full field/history migration; retain original files.',
            'Reconcile current SharePoint edits before cutover.',
            'Import People, Factories, Tasks, Issues, templates and execution history from authoritative sources.',
            'Reconcile Project-SKU execution dates/status; do not copy SKU master status into each project.',
        ],
    }
    return payload, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    # An output directory must be new so an earlier review package cannot be overwritten.
    if args.output.exists():
        parser.error('Output already exists; choose a new review directory.')
    raw = args.source.read_bytes()
    payload, manifest = build_package(json.loads(raw.decode('utf-8-sig')))
    manifest['source_file_sha256'] = hashlib.sha256(raw).hexdigest()
    args.output.mkdir(parents=True)
    (args.output / 'source-snapshot.json').write_bytes(raw)
    for name, content in [('candidate-data.json', payload), ('manifest.json', manifest)]:
        (args.output / name).write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding='utf-8')
    with (args.output / 'relationship-review.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['kind', 'ProgramKey', 'ProjectKey'])
        writer.writeheader()
        writer.writerows(manifest['relationship_discrepancies'])
    print(json.dumps({'counts': manifest['counts'], 'integrity_errors': len(manifest['integrity_errors']),
                      'relationship_discrepancies': len(manifest['relationship_discrepancies']),
                      'production_ready': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
