"""Project-local issue revision matching, enabled only for DeepSeek extraction.

Source row numbers, owners, dates and risk are not identities. Never infer that
the only issue in a project must be the same issue. Ambiguities are held back.
"""
from collections import Counter
from difflib import SequenceMatcher
import re
import unicodedata


def text_key(value):
    text = unicodedata.normalize('NFKC', str(value or '')).casefold()
    return re.sub(r'[^\w]+', ' ', text).strip()


def similarity(a, b):
    a, b = text_key(a), text_key(b)
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b, autojunk=False).ratio()


def _contains(a, b):
    # Whole phrase only: "motor" must not match "motorcycle".
    return bool(a and b and ((' ' + a + ' ') in (' ' + b + ' ') or
                             (' ' + b + ' ') in (' ' + a + ' ')))


def _score(item, values, fields):
    old = values.get(fields['text']['id'], '')
    a, b = text_key(item.get('text')), text_key(old)
    # Short generic fragments offer too little evidence for a fuzzy update.
    score = similarity(a, b) if min(len(a), len(b)) >= 20 else 0.0
    # Nearly identical wording can describe different SKUs or regional failures.
    def scope(text):
        return set(re.findall(r'\b(?:cn|vn|th|us|uk|eu|left|right|upper|lower)\b', text))
    def codes(text):
        return {word for word in text.split() if re.search('[a-z]', word) and re.search('[0-9]', word)}
    conflict = any(x and y and x != y for x, y in ((scope(a), scope(b)), (codes(a), codes(b))))
    action_field = fields.get('action', {}).get('id')
    action = text_key(item.get('action'))
    old_action = text_key(values.get(action_field))
    same_action = min(len(action), len(old_action)) >= 24 and action == old_action
    continued_action = min(len(action), len(old_action)) >= 24 and _contains(action, old_action)
    continued_text = _contains(a, b)
    if a and a == b:
        return 1.0, True
    substantial = min(len(a), len(b)) >= 32
    strong = (score >= .86 or (same_action and score >= .50)
              or (continued_text and (substantial or continued_action)))
    possible = score >= .60 or same_action or (continued_text and min(len(a), len(b)) >= 8)
    confidence = max(score, .90) if strong else score
    return (min(confidence, .85) if conflict else confidence), possible


def match_revisions(items, records, project_id, fields, normalize):
    """Return index -> decision, reserving exact matches before fuzzy matching.

    A candidate must be unique on both sides; list order never breaks a tie.
    None is a genuinely new issue. A reason means withhold the item.
    """
    pool = [r for r in records if project_id in
            (r.get('fields', {}).get(fields['project']['id']) or [])]
    result, reserved, proposals = {}, set(), {}
    counts = Counter(normalize(i.get('text')) for i in items)
    for index, item in enumerate(items):
        title = normalize(item.get('text'))
        exact = [r for r in pool if normalize(r['fields'].get(fields['text']['id'])) == title]
        if exact:
            reserved.update(r['id'] for r in exact)
        if not title or counts[title] > 1:
            result[index] = {'reason': '周报中的问题正文为空或重复'}
        elif len(exact) > 1:
            result[index] = {'reason': 'Airtable 存在多个相同问题'}
        elif exact:
            result[index] = {'record': exact[0], 'method': 'exact_issue_text'}
    for index, item in enumerate(items):
        if index in result:
            continue
        candidates = []
        for record in pool:
            score, possible = _score(item, record['fields'], fields)
            if possible:
                candidates.append((record, score))
        if not candidates:
            result[index] = None
        elif (len(candidates) == 1 and candidates[0][1] >= .86
              and candidates[0][0]['id'] not in reserved
              and candidates[0][0]['fields'].get(fields['project']['id']) == [project_id]):
            proposals[index] = candidates[0]
        else:
            result[index] = {'reason': '可能是已有问题的改写，但匹配不唯一或证据不足',
                             'candidates': [r['id'] for r, _ in candidates]}
    targets = Counter(record['id'] for record, _ in proposals.values())
    for index, (record, score) in proposals.items():
        # Also reserve candidates of held-back source rows. Otherwise one of two
        # revisions could silently win merely because it has a higher score.
        contested = any(record['id'] in (d or {}).get('candidates', []) for d in result.values())
        if targets[record['id']] != 1 or contested:
            result[index] = {'reason': '多条周报问题可能对应同一条旧问题'}
        else:
            result[index] = {'record': record, 'method': 'unique_issue_revision', 'score': round(score, 4)}
    return result, pool
