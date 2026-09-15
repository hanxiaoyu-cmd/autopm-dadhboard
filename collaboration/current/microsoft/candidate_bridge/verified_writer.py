"""Reviewed Airtable writes with durable intent and independent read-back.

Single writer only: Airtable has no compare-and-swap or unique constraint for
these legacy tables. This module detects observed conflicts; it does not claim
to close the remote race window. An uncertain POST is NEVER automatically retried.
"""
from __future__ import annotations
from contextlib import contextmanager
from pathlib import Path
import hashlib
import json
import os
import tempfile


class ReconciliationRequired(RuntimeError):
    pass


def _save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name, suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def _lock(path):
    # Shared by jobs on this host, not just by one journal filename.
    path = Path(tempfile.gettempdir()) / ('autopm-' + hashlib.sha256(path.encode()).hexdigest() + '.lock')
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise ReconciliationRequired('Another writer or stale lock exists; reconcile before continuing.') from None
    try:
        os.write(fd, str(os.getpid()).encode())
        yield
    finally:
        os.close(fd)
        path.unlink()


def _equal(left, right):
    # Airtable omits empty fields and does not promise linked-record order.
    empty = (None, '', [])
    if left in empty and right in empty:
        return True
    if isinstance(left, list) and isinstance(right, list):
        return sorted(json.dumps(v, sort_keys=True) for v in left) == sorted(json.dumps(v, sort_keys=True) for v in right)
    return left == right


def _matches(record, fields):
    return all(_equal(record.get('fields', {}).get(key), value) for key, value in fields.items())


def apply_reviewed_plan(plan, api, journal, progress=None):
    import bridge
    if plan.get('kind') != 'weekly_to_airtable' or plan.get('blockers'):
        raise ValueError('A valid, unblocked weekly import preview is required.')
    if plan['base'] != api.base or plan['table'] != api.table:
        raise ValueError('Configuration does not match the reviewed preview.')
    if bridge.digest(plan['source']) != plan['source_sha256']:
        raise ValueError('The source file changed; generate a new preview.')
    signature = hashlib.sha256(json.dumps(plan, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    journal = Path(journal)
    with _lock(api.base):
        if journal.exists():
            result = json.loads(journal.read_text(encoding='utf-8'))
            if result.get('plan_sha256') != signature:
                raise ReconciliationRequired('Journal belongs to another or legacy preview; do not overwrite it.')
            if result.get('status') == 'verified':
                return result  # Immutable receipt: do not overwrite later legitimate edits.
            if any(op['status'] == 'sent' and op['op'] == 'create' and not op.get('record') for op in result['operations']):
                raise ReconciliationRequired('Create result is unknown. Reconcile record IDs before retrying; no POST was repeated.')
        else:
            grouped = {}
            creates = []
            for change in plan['changes']:
                table = change.get('table', plan['table'])
                if change.get('op') == 'create':
                    creates.append({'op': 'create', 'table': table, 'pid': change['pid'], 'fields': change['new'],
                                    'identity': change.get('identity'), 'status': 'planned'})
                else:
                    key = (table, change['record'])
                    op = grouped.setdefault(key, {'op': 'update', 'table': table, 'record': change['record'],
                        'pid': change['pid'], 'fields': {}, 'old': {}, 'types': {}, 'status': 'planned'})
                    fid = change['field']
                    if fid in op['fields'] and not _equal(op['fields'][fid], change['new']):
                        raise ValueError('Preview contains conflicting writes to the same field.')
                    op['fields'][fid], op['old'][fid], op['types'][fid] = change['new'], change['old'], change['type']
            operations = list(grouped.values()) + creates
            result = {'journal_version': 2, 'plan_sha256': signature, 'status': 'started', 'before': [],
                      'confirmed': [], 'created': [], 'pending': [], 'operations': operations}
            for index, op in enumerate(operations):
                op['key'] = f"{op['table']}:{op['op']}:{index}"
            _save(journal, result)

        schema = {t['id']: {f['id']: f for f in t['fields']} for t in api.schema()['tables']}
        current = {t: {r['id']: r for r in api.records(t)} for t in {op['table'] for op in result['operations']}}
        seen_creates = set()
        for op in result['operations']:
            table, fields = op['table'], op['fields']
            if any(f not in schema.get(table, {}) for f in fields):
                raise ValueError('Target schema changed after preview.')
            if any(schema[table][f]['type'] != typ for f, typ in op.get('types', {}).items()):
                raise ValueError('Target field type changed after preview.')
            if op['status'] == 'verified':
                continue
            if op['op'] == 'create' and not op.get('record'):
                identity = op.get('identity')
                if not identity:
                    spec = bridge.TASK_FIELDS if table == getattr(api, 'tasks', None) else bridge.ISSUE_FIELDS if table == getattr(api, 'issues', None) else None
                    if spec:
                        identity = {spec['project']: fields.get(spec['project']), spec.get('name', spec.get('record')): fields.get(spec.get('name', spec.get('record')))}
                if not identity or any(v in (None, '', []) for v in identity.values()):
                    raise ValueError('Create requires a reviewed identity before execution.')
                identity_key = table + json.dumps(identity, sort_keys=True)
                if identity_key in seen_creates:
                    raise ValueError('Duplicate create identity in preview.')
                seen_creates.add(identity_key)
                matches = [r for r in current[table].values() if _matches(r, identity)]
                if len(matches) > 1 or (matches and not _matches(matches[0], fields)):
                    raise ValueError('Create identity now exists or is ambiguous; generate a new preview.')
                if matches:
                    op['record'] = matches[0]['id']
                    op['origin'] = 'already_present'
            if op.get('record'):
                record = current[table].get(op['record'])
                if record is None:
                    raise ValueError('Target record was deleted after preview.')
                if op['op'] == 'update':
                    if not all(_equal(record['fields'].get(f), v) or _equal(record['fields'].get(f), fields[f]) for f, v in op['old'].items()):
                        raise ValueError('Target changed after preview; no writes were performed.')
                    if not any(r.get('id') == record['id'] for r in result['before']):
                        result['before'].append(record)
                elif not _matches(record, fields):
                    raise ReconciliationRequired('A created record differs from the reviewed values.')
        _save(journal, result)
        try:
            for op in result['operations']:
                if op['status'] == 'verified':
                    continue
                table, fields = op['table'], op['fields']
                if op['op'] == 'update':
                    # Re-read immediately before PATCH to narrow the remote race window.
                    latest = api.request(f"{api.base}/{table}/{op['record']}?returnFieldsByFieldId=true")
                    if not all(_equal(latest['fields'].get(f), v) or _equal(latest['fields'].get(f), fields[f]) for f, v in op['old'].items()):
                        raise ValueError('Concurrent modification detected before write.')
                    if not _matches(latest, fields):
                        op['status'] = 'sent'; _save(journal, result)
                        api.request(f'{api.base}/{table}', 'PATCH', {'records': [{'id': op['record'], 'fields': fields}], 'typecast': False})
                elif not op.get('record'):
                    op['status'] = 'sent'; _save(journal, result)
                    response = api.request(f'{api.base}/{table}', 'POST', {'records': [{'fields': fields}], 'typecast': False})
                    records = response.get('records', [])
                    if len(records) != 1 or not records[0].get('id'):
                        raise ReconciliationRequired('Create response has no single record ID; reconcile before retry.')
                    op['record'] = records[0]['id']
                    op['origin'] = 'created'
                    _save(journal, result)  # Preserve the ID even if the read-back fails.
                saved = api.request(f"{api.base}/{table}/{op['record']}?returnFieldsByFieldId=true")
                if not _matches(saved, fields):
                    raise ReconciliationRequired('Post-write verification failed: ' + op['record'])
                op['status'] = 'verified'
                _save(journal, result)
                if progress:
                    progress(sum(x['status'] == 'verified' for x in result['operations']), len(result['operations']))
        except Exception:
            result['status'] = 'needs_reconciliation'
            result['pending'] = [o['key'] for o in result['operations'] if o['status'] != 'verified']
            _save(journal, result)
            raise
        result['confirmed'] = [o['key'] for o in result['operations'] if o['op'] == 'update']
        result['created'] = [{'table': o['table'], 'record': o['record'], 'pid': o['pid'], 'origin': o.get('origin')} for o in result['operations'] if o['op'] == 'create']
        result['pending'] = [o['key'] for o in result['operations'] if o['status'] != 'verified']
        if result['pending']:
            raise ReconciliationRequired('Unverified operations remain.')
        result['status'] = 'verified'; _save(journal, result)
        return result
