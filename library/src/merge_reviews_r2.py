"""merge_reviews_r2 - merge the second review (library\\v5_work\\r2\\part_*.json) and compare it with round 1.
Writes library\\v5_work\\r2\\review_defects_r2.json and prints:
  coverage (222 pack models: 198 rebuilt + 24 blind anchors), verdict counts for rebuilt models and for anchors,
  STRICTNESS CHECK: the anchors were OK in round 1 and untouched; the share the new reviewers do not rate OK shows how much stricter they are,
  transitions round 1 -> round 2 for the rebuilt models, originality flags, the models still failing (grouped by builder A1..A6) with the reviewers' fixes.
Safe to re-run while reviewers are still writing.
"""
import os
import re
import json
import glob
from collections import Counter, defaultdict

LIB = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
R2 = os.path.join(LIB, 'v5_work', 'r2')
pack = {p['id']: p for p in json.load(open(os.path.join(R2, 'pack_ids.json')))}
r1 = {e['id']: e for e in json.load(open(os.path.join(LIB, 'v5_work', 'review_defects_v5.json')))}
owner = {}
for A in ('A1', 'A2', 'A3', 'A4', 'A5', 'A6'):
    for i in re.findall(r'^\| `([A-Za-z0-9_]+)` \|', open(os.path.join(LIB, 'v5_work', 'fix', f'assign_{A}.md'), encoding='utf-8').read(), re.M):
        owner[i] = A
VERD = {'OK': 'OK', 'MINOR': 'MINOR', 'MAJOR': 'MAJOR', 'REDO': 'REDO', 'KEEP': 'OK', 'FIX': 'MAJOR', 'REBUILD': 'REDO'}
got, bad, dup, unknown, parts = {}, [], [], [], []
for f in sorted(glob.glob(os.path.join(R2, 'part_*.json'))):
    parts.append(os.path.basename(f))
    try:
        data = json.load(open(f, encoding='utf-8'))
    except Exception as e:
        bad.append((os.path.basename(f), str(e)[:80]))
        continue
    if isinstance(data, dict):
        data = data.get('models') or data.get('items') or list(data.values())
    for o in data:
        if not isinstance(o, dict) or 'id' not in o:
            bad.append((os.path.basename(f), 'item without id'))
            continue
        v = VERD.get(str(o.get('verdict', '')).strip().upper())
        if not v:
            bad.append((os.path.basename(f), f"{o['id']}: verdict {o.get('verdict')!r}"))
            continue
        if o['id'] not in pack:
            unknown.append(o['id'])
            continue
        if o['id'] in got:
            dup.append(o['id'])
        d = o.get('defects') or []
        got[o['id']] = dict(id=o['id'], verdict=v, defects=[d] if isinstance(d, str) else d, fix=o.get('fix', '') or '', original=str(o.get('original', 'OK')), kind=pack[o['id']]['kind'], part=os.path.basename(f))
missing = [i for i in pack if i not in got]
rows = list(got.values())
json.dump(rows, open(os.path.join(R2, 'review_defects_r2.json'), 'w'), indent=1)
ORDER = ('OK', 'MINOR', 'MAJOR', 'REDO')
print(f'parts read {len(parts)}; verdicts for {len(rows)} of {len(pack)} pack models; missing {len(missing)}; duplicates {len(dup)}; unknown {len(unknown)}; bad items {len(bad)}')
if bad:
    print('BAD FORMAT:', bad[:6])
ch = [r for r in rows if r['kind'] == 'changed']
an = [r for r in rows if r['kind'] == 'anchor']
cc, ca = Counter(r['verdict'] for r in ch), Counter(r['verdict'] for r in an)
print('REBUILT models (n=%d):' % len(ch), {k: cc.get(k, 0) for k in ORDER})
print('ANCHORS    (n=%d):' % len(an), {k: ca.get(k, 0) for k in ORDER}, ' <- were all OK in round 1 and were not touched')
if an:
    print('STRICTNESS: %d of %d untouched round-1 OK models are NOT rated OK now (%.0f%%)' % (len(an) - ca.get('OK', 0), len(an), 100.0 * (len(an) - ca.get('OK', 0)) / len(an)))
    for r in an:
        if r['verdict'] != 'OK':
            print('   anchor', r['id'][:40].ljust(40), r['verdict'], '|', '; '.join(r['defects'])[:90])
tr = Counter((r1[r['id']]['verdict'], r['verdict']) for r in ch)
print('TRANSITIONS round 1 -> round 2 (rebuilt models):')
for a in ('REDO', 'MAJOR', 'MINOR', 'OK'):
    line = {b: tr.get((a, b), 0) for b in ORDER if tr.get((a, b), 0)}
    if line:
        print(f'   {a:5} -> {line}')
orig = [r for r in rows if not str(r['original']).strip().upper().startswith('OK')]
print(f'ORIGINALITY flags: {len(orig)}')
for r in orig:
    print('   ', r['id'][:40].ljust(40), r['original'][:100])
fam = defaultdict(Counter)
bad_by = defaultdict(list)
for r in ch:
    if r['verdict'] != 'OK':
        bad_by[owner.get(r['id'], '?')].append(r)
print('STILL NOT OK among rebuilt models (%d), by builder:' % sum(len(v) for v in bad_by.values()))
for A in sorted(bad_by):
    c = Counter(r['verdict'] for r in bad_by[A])
    print(f'   {A}: {len(bad_by[A])}  ' + ', '.join(f'{k} {c[k]}' for k in ORDER if c.get(k)))
md = ['# Round 2 review: data', '', f'REBUILT {dict(cc)}   ANCHORS {dict(ca)}', '']
for A in sorted(bad_by):
    md += [f'## {A} ({len(bad_by[A])} not OK)', '', '| id | verdict | round 1 | what is wrong | fix |', '|---|---|---|---|---|']
    for r in sorted(bad_by[A], key=lambda r: (ORDER.index(r['verdict']) * -1, r['id'])):
        md.append(f"| `{r['id']}` | {r['verdict']} | {r1[r['id']]['verdict']} | {'; '.join(r['defects'])[:220]} | {r['fix'][:230]} |")
    md.append('')
open(os.path.join(R2, 'ROUND2_NOT_OK.md'), 'w', encoding='utf-8').write('\n'.join(md))
