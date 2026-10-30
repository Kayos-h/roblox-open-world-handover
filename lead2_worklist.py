"""lead2_worklist - the 87 models for the second lead pass: 9 never reviewed + 78 MINOR.  Writes library\\v5_work\\lead2\\worklist.json and prints them grouped by row with the latest reviewer notes and the module that builds them."""
import os
import re
import csv
import json
import glob
from collections import defaultdict

T = r"C:\Users\Nitro\.kiro\crew\workspace\town"
LIB = os.path.join(T, 'library')
W = os.path.join(LIB, 'v5_work')
fv = {e['id']: e for e in json.load(open(os.path.join(W, 'FINAL_VERDICTS_v5.json')))}
notes = {}
for p in ('review_defects_v5.json', r'r2\review_defects_r2.json', r'r3\review_defects_r3.json', r'r4\review_defects_r4.json'):
    for e in json.load(open(os.path.join(W, p))):
        notes[e['id']] = e
man = {r['id']: r for r in csv.DictReader(open(os.path.join(T, 'plan_v5', 'V5_MANIFEST.csv'), encoding='utf-8-sig'))}
worker = {}
for f in glob.glob(os.path.join(LIB, 'v4_meta_v[a-j].json')):
    w = os.path.basename(f)[8:-5]
    for k in json.load(open(f)):
        worker[k] = w
work = [i for i, e in fv.items() if e['verdict'] in ('MINOR', 'UNREVIEWED')]
os.makedirs(os.path.join(W, 'lead2'), exist_ok=True)
json.dump(work, open(os.path.join(W, 'lead2', 'worklist.json'), 'w'), indent=1)
by = defaultdict(list)
for i in work:
    by[man[i]['row']].append(i)
print(len(work), 'models in', len(by), 'rows')
for row in sorted(by):
    ids_ = by[row]
    print(f"\n[{row}] worker {worker[ids_[0]]}  ({len(ids_)})")
    for i in ids_:
        n = notes.get(i, {})
        print(f"  {i[:36].ljust(36)} {fv[i]['verdict'][:5]} saw: {'; '.join(n.get('defects') or [])[:170]}")
        if n.get('fix'):
            print(f"       fix: {n['fix'][:150]}")
