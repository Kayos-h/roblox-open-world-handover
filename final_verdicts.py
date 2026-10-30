"""final_verdicts - latest independent verdict per model across all review waves (r4 > r3 > r2 > r1) and the final counts.
Writes library\\v5_work\\FINAL_VERDICTS_v5.json. A model rebuilt in fix round 2 without an r4 verdict is 'UNREVIEWED' (the 13 models of builder A1)."""
import json
import os
import csv
from collections import Counter, defaultdict

W = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\v5_work"


def load(p):
    return {r['id']: r for r in json.load(open(os.path.join(W, p)))}


r1, r2, r3, r4 = load('review_defects_v5.json'), load(r'r2\review_defects_r2.json'), load(r'r3\review_defects_r3.json'), load(r'r4\review_defects_r4.json')
fix2 = {r['id']: r for r in json.load(open(os.path.join(W, r'r2\fix2_ids.json')))}
man = [r for r in csv.DictReader(open(r"C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5\V5_MANIFEST.csv", encoding='utf-8-sig'))]
out, src = {}, Counter()
for m in man:
    i = m['id']
    if i in r4:
        v, s = r4[i]['verdict'], 'r4'
    elif i in fix2:
        v, s = 'UNREVIEWED', 'rebuilt in fix round 2, no verdict'
    elif i in r3:
        v, s = r3[i]['verdict'], 'r3'
    elif i in r2:
        v, s = r2[i]['verdict'], 'r2'
    else:
        v, s = r1[i]['verdict'], 'r1'
    src[s] += 1
    out[i] = dict(id=i, verdict=v, source=s, row=m['row'], r1=r1.get(i, {}).get('verdict'), r2=r2.get(i, {}).get('verdict'), r3=r3.get(i, {}).get('verdict'), r4=r4.get(i, {}).get('verdict'))
json.dump(list(out.values()), open(os.path.join(W, 'FINAL_VERDICTS_v5.json'), 'w'), indent=1)
c = Counter(o['verdict'] for o in out.values())
print('MODELS', len(out), '| FINAL:', {k: c.get(k, 0) for k in ('OK', 'MINOR', 'MAJOR', 'REDO', 'UNREVIEWED')})
print('verdict source:', dict(src))
print('ROUND 1 for the same models:', dict(Counter(r1[i]['verdict'] for i in out)))
fam = defaultdict(Counter)
for o in out.values():
    fam[''.join(ch for ch in o['row'] if ch.isalpha())[:3] if False else o['row'][:2]][o['verdict']] += 1
print('NOT OK by family (OK/MINOR/MAJOR/REDO/UNREV):', '; '.join(f'{k} {c2["OK"]}/{c2["MINOR"]}/{c2["MAJOR"]}/{c2["REDO"]}/{c2["UNREVIEWED"]}' for k, c2 in sorted(fam.items()) if sum(c2.values()) - c2['OK'] > 0))
print('MAJOR/REDO now:', sorted(i[:24] for i, o in out.items() if o['verdict'] in ('MAJOR', 'REDO')))
print('UNREVIEWED:', sorted(i[:24] for i, o in out.items() if o['verdict'] == 'UNREVIEWED'))
