"""analyze_r4 - split the r4 verdicts into the 78 rebuilt models and the 12 blind controls; transitions; the worst models."""
import json
import os
from collections import Counter

W = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\v5_work"
d = {r['id']: r for r in json.load(open(os.path.join(W, 'r4', 'review_defects_r4.json')))}
pk = {p['id']: p for p in json.load(open(os.path.join(W, 'r4', 'pack_ids.json')))}
r2 = {r['id']: r for r in json.load(open(os.path.join(W, 'r2', 'review_defects_r2.json')))}
r3 = {r['id']: r for r in json.load(open(os.path.join(W, 'r3', 'review_defects_r3.json')))}
ORDER = ('OK', 'MINOR', 'MAJOR', 'REDO')
ctl = [d[i] for i in d if pk[i]['kind'] == 'control']
chg = [d[i] for i in d if pk[i]['kind'] == 'changed2']
c = Counter(r['verdict'] for r in ctl)
print('CONTROLS (12; all were OK in the r3 panel):', {k: c.get(k, 0) for k in ORDER})
for r in ctl:
    if r['verdict'] != 'OK':
        print('   ', r['id'][:36].ljust(36), r['verdict'], '|', '; '.join(r['defects'])[:140])
c = Counter(r['verdict'] for r in chg)
print(f'\nREBUILT IN FIX ROUND 2 ({len(chg)}):', {k: c.get(k, 0) for k in ORDER})
tr = Counter((r2[r['id']]['verdict'] if r['id'] in r2 else 'new', r['verdict']) for r in chg)
for a in ('REDO', 'MAJOR', 'MINOR', 'OK', 'new'):
    line = {b: tr.get((a, b), 0) for b in ORDER if tr.get((a, b), 0)}
    if line:
        print(f'   was {a:5} in r2 -> {line}')
print('\nREDO / MAJOR among the rebuilt:')
for r in sorted(chg, key=lambda r: (-ORDER.index(r['verdict']), r['id'])):
    if r['verdict'] in ('MAJOR', 'REDO'):
        print('   ', r['verdict'].ljust(5), r['id'][:36].ljust(36), r['owner'], '|', '; '.join(r['defects'])[:150])
print('\nnot OK by builder (rebuilt only):', dict(sorted(Counter(r['owner'] for r in chg if r['verdict'] != 'OK').items())))
print('worse than before:', [(r['id'][:22], r2[r['id']]['verdict'], r['verdict']) for r in chg if r['id'] in r2 and ORDER.index(r['verdict']) > ORDER.index(r2[r['id']]['verdict'])])
