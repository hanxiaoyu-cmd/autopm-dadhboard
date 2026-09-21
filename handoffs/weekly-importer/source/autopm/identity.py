"""Source project number first; SKU plus one resolved factory identifies a unit."""
from functools import lru_cache
from .normalize import clean_text, normalize_project_id
import re

MODE = 'number_sku_factory'


def sku_tokens(value):
    if not isinstance(value, str):
        return frozenset()
    return _sku_tokens(value)


@lru_cache(maxsize=8192)
def _sku_tokens(value):
    return frozenset(clean_text(v).upper() for v in re.split(r'[,;，；\n]+', value) if clean_text(v))


def official_number(record, fields):
    values = record.get('fields', {})
    number = normalize_project_id(values.get(fields.get('project_number')))
    legacy = normalize_project_id(values.get(fields.get('project_id')))
    return number if number and not number.startswith('X') else (legacy if not legacy.startswith('X') else '')


def match_units(number, sku, factory_ids, records, fields):
    """Return unique existing records and explicit unresolved SKU diagnostics.

    Artificial X IDs are not source project numbers. An unnumbered X record
    can be bound only by an exact unique SKU/factory pair. No name/fuzzy match.
    """
    number = normalize_project_id(number)
    tokens = sku_tokens(sku)
    if not number or number.startswith('X'):
        return [], ['来源缺少正式项目编号，不能用 X 自编编号代替。']
    if not tokens or len(factory_ids) != 1:
        return [], [f'{number}：需要明确 SKU 和唯一工厂，不能仅凭编号或名称匹配。']
    missing = {'project_id', 'sku', 'factory'} - {k for k, v in fields.items() if v}
    if missing:
        return [], [f'项目身份字段缺失：{", ".join(sorted(missing))}']
    factory_ids = sorted(factory_ids)
    resolved, warnings = {}, []
    for token in sorted(tokens):
        pair = [r for r in records if token in sku_tokens(r.get('fields', {}).get(fields['sku']))
                and sorted(r.get('fields', {}).get(fields['factory']) or []) == factory_ids]
        scoped = [r for r in pair if official_number(r, fields) == number]
        # Even a unique formal match must not conceal a duplicate unbound unit.
        unbound = [r for r in pair if not official_number(r, fields)
                   and normalize_project_id(r.get('fields', {}).get(fields['project_id'])).startswith('X')]
        candidates = scoped + unbound
        if len(candidates) != 1:
            warnings.append(f'{number} / {token}：SKU＋工厂匹配到 {len(candidates)} 条兼容记录，已跳过。')
            continue
        record = candidates[0]
        if len(sku_tokens(record.get('fields', {}).get(fields['sku']))) != 1:
            warnings.append(f'{number} / {token}：目标 {record["id"]} 合并了多个 SKU，需先拆成 SKU＋工厂记录，已跳过。')
            continue
        selected = resolved.setdefault(record['id'], {'record': record, 'skus': [],
            'method': 'number_sku_factory' if scoped else 'unbound_x_sku_factory'})
        selected['skus'].append(token)
    for item in resolved.values():
        item['guard'] = {'number': number, 'sku': ', '.join(item['skus']),
                         'factory_ids': factory_ids, 'fields': fields,
                         'record_id': item['record']['id'],
                         'before': {fid: item['record'].get('fields', {}).get(fid)
                                    for fid in fields.values() if fid}}
    return list(resolved.values()), warnings


def guard_matches(records, guard):
    matches, warnings = match_units(guard['number'], guard['sku'], guard['factory_ids'], records, guard['fields'])
    return not warnings and len(matches) == 1 and matches[0]['record']['id'] == guard['record_id']
