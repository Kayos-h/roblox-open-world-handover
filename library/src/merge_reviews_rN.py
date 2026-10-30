"""merge_reviews_rN - merge one review wave (library\\v5_work\\<tag>\\part_*.json) and compare it with the earlier verdicts.
  python merge_reviews_rN.py r3        (the 177 never-rebuilt models, front + back)
  python merge_reviews_rN.py r4        (the 91 models of fix round 2, front + back)
Writes <tag>\\review_defects_<tag>.json and <tag>\\NOT_OK_<tag>.md (not-OK models grouped by the builder that owns that family) and prints counts,
transitions from the verdict each model had before (round 1 for r3; round 2 for r4), originality flags and the not-OK list per builder.
"""
import os
import re
import sys
import csv
import json
import glob
from collections import Counter, defaultdict

TAG = sys.argv[1]
T = r"C:\Users\Nitro\.kiro\crew\workspace\town"
LIB = os.path.join(T, 'library')
W = os.path.join(LIB, 'v5_work', TAG)
pack = {p['id']: p for p in json.load(open(os.path.join(W, 'pack_ids.json')))}
r1 = {e['id']: e for e in json.load(open(os.path.join(LIB, 'v5_work', 'review_defects_v5.json')))}
r2f = os.path.join(LIB, 'v5_work', 'r2', 'review_defects_r2.json')
r2 = {e['id']: e for e in json.load(open(r2f))} if os.path.exists(r2f) else {}
before = r2 if TAG == 'r4' else r1
man = {r['id']: r for r in csv.DictReader(open(os.path.join(T, 'plan_v5', 'V5_MANIFEST.csv'), encoding='utf-8-sig'))}
worker_of = {}
for f in glob.glob(os.path.join(LIB, 'v4_meta_v[a-j].json')):
    w = os.path.basename(f)[8:-5]
    for k in json.load(open(f)):
        worker_of[k] = w
A1_ROWS = ('PL01', 'PL02', 'PL03', 'PL04', 'PL05', 'PL06', 'VL01', 'LM19', 'LM20', 'LM21', 'LM26', 'LM27', 'LM28', 'LM29', 'LM31', 'FL01', 'FL02')


def owner_of(i):
    w, row = worker_of[i], man[i]['row']
    if w == 'vi':
        return 'A1' if row in A1_ROWS else 'A2'
    return {'vh': 'A3', 'vg': 'A4', 'vc': 'A5', 'vd': 'A5', 've': 'A6', 'vf': 'A6', 'va': 'A6', 'vb': 'A6', 'vj': 'A6'}[w]


VERD = {'OK': 'OK', 'MINOR': 'MINOR', 'MAJOR': 'MAJOR', 'REDO': 'REDO', 'KEEP': 'OK', 'FIX': 'MAJOR', 'REBUILD': 'REDO'}
got, bad, dup, unknown, parts = {}, [], [], [], []
for f in sorted(glob.glob(os.path.join(W, 'part_*.json'))):
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
        got[o['id']] = dict(id=o['id'], verdict=v, defects=[d] if isinstance(d, str) else d, fix=o.get('fix', '') or '', original=str(o.get('original', 'OK')), part=os.path.basename(f), owner=owner_of(o['id']), row=man[o['id']]['row'])
missing = [i for i in pack if i not in got]
rows = list(got.values())
json.dump(rows, open(os.path.join(W, f'review_defects_{TAG}.json'), 'w'), indent=1)
ORDER = ('OK', 'MINOR', 'MAJOR', 'REDO')
cc = Counter(r['verdict'] for r in rows)
print(f'{TAG}: parts read {len(parts)}; verdicts for {len(rows)} of {len(pack)}; missing {len(missing)} {missing[:5]}; duplicates {len(dup)}; unknown {len(unknown)}; bad {len(bad)}')
if bad:
    print('BAD FORMAT:', bad[:6])
print('VERDICTS:', {k: cc.get(k, 0) for k in ORDER}, f' ({100.0 * (len(rows) - cc.get("OK", 0)) / max(1, len(rows)):.0f}% not OK)')
tr = Counter((before[r['id']]['verdict'] if r['id'] in before else '?', r['verdict']) for r in rows)
print('TRANSITIONS (verdict before -> now):')
for a in ('REDO', 'MAJOR', 'MINOR', 'OK', '?'):
    line = {b: tr.get((a, b), 0) for b in ORDER if tr.get((a, b), 0)}
    if line:
        print(f'   {a:5} -> {line}')
orig = [r for r in rows if not str(r['original']).strip().upper().startswith('OK')]
print(f'ORIGINALITY flags: {len(orig)}')
for r in orig:
    print('   ', r['id'][:40].ljust(40), r['original'][:110])
fam = defaultdict(Counter)
for r in rows:
    fam[re.match(r'[A-Z]+', r['row']).group(0)][r['verdict']] += 1
print('FAMILIES with not-OK models (family: n, OK/MINOR/MAJOR/REDO):')
print('   ' + '; '.join(f'{k}: {sum(c.values())} ({c["OK"]}/{c["MINOR"]}/{c["MAJOR"]}/{c["REDO"]})' for k, c in sorted(fam.items()) if sum(c.values()) - c['OK'] > 0))
bad_by = defaultdict(list)
for r in rows:
    if r['verdict'] != 'OK':
        bad_by[r['owner']].append(r)
print('NOT OK by builder:', {A: len(v) for A, v in sorted(bad_by.items())})
md = [f'# {TAG}: not-OK models by builder', '', f'VERDICTS {dict(cc)}', '']
for A in sorted(bad_by):
    md += [f'## {A} ({len(bad_by[A])})', '', '| id | now | before | what the reviewers saw | fix |', '|---|---|---|---|---|']
    for r in sorted(bad_by[A], key=lambda r: (-ORDER.index(r['verdict']), r['id'])):
        md.append(f"| `{r['id']}` | {r['verdict']} | {before[r['id']]['verdict'] if r['id'] in before else '?'} | {'; '.join(r['defects'])[:220]} | {r['fix'][:230]} |")
    md.append('')
open(os.path.join(W, f'NOT_OK_{TAG}.md'), 'w', encoding='utf-8').write('\n'.join(md))
