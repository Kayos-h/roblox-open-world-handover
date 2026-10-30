"""v5_fix_plan - the list of models the fix round must touch, with everything a builder needs per model.
Scope: every model whose first-review verdict is not OK (MINOR, MAJOR, REDO = 192) plus 7 OK models that carry a sibling-variety fix note.
Writes library\\v5_work\\fix\\fix_ids.json and prints counts per queue / batch / verdict.
"""
import os
import re
import csv
import json
import glob
from collections import defaultdict, Counter

T = r"C:\Users\Nitro\.kiro\crew\workspace\town"
LIB = os.path.join(T, 'library')
OUT = os.path.join(LIB, 'v5_work', 'fix')
os.makedirs(OUT, exist_ok=True)
EXTRA = ['LM04_02_fortress_rampart_step_02', 'LM04_03_fortress_rampart_step_03', 'VG01_02_tree_tall_narrow_02', 'EV02_03_canopy_cluster_03',
         'TW03_04_skull_avenue_set_04', 'DS03_02_caravan_wagon_02', 'DS05_02_oasis_rock_ring_02']
man = {r['id']: r for r in csv.DictReader(open(os.path.join(T, 'plan_v5', 'V5_MANIFEST.csv'), encoding='utf-8-sig'))}
rev = {e['id']: e for e in json.load(open(os.path.join(LIB, 'v5_work', 'review_defects_v5.json')))}
meta, worker_of = {}, {}
for f in sorted(glob.glob(os.path.join(LIB, 'v4_meta_v[a-j].json'))):
    w = os.path.basename(f)[8:-5]
    for k, v in json.load(open(f)).items():
        meta[k] = v
        worker_of[k] = w
batch_of = {}
for f in glob.glob(os.path.join(LIB, 'v4_work', 'v[a-j]_*_*.json')):
    m = re.match(r'(v[a-j])_(.+)_(\d+)\.json$', os.path.basename(f))
    try:
        rep = json.load(open(f))
    except Exception:
        continue
    for r in rep.get('rows', []):
        if r and isinstance(r[0], str) and r[0] in man:
            batch_of[r[0]] = (m.group(1), m.group(2))
ids = [i for i in man if i in rev and (rev[i]['verdict'] != 'OK' or i in EXTRA)]
rows = []
for i in ids:
    r, e, m = man[i], rev[i], meta[i]
    rows.append({
        'id': i, 'row': r['row'], 'worker': worker_of[i], 'batch': batch_of.get(i, (worker_of[i], '?'))[1], 'category': m['category'],
        'verdict': e['verdict'], 'defects': e['defects'], 'fix': e['fix'],
        'want_w': float(r['size_x']), 'want_h': float(r['size_y']), 'want_d': float(r['size_z']), 'tri_budget': int(float(r['tri_budget'])),
        'tris_now': m.get('tris'), 'size_now': m.get('size'), 'note': r.get('note', '')[:300],
    })
json.dump(rows, open(os.path.join(OUT, 'fix_ids.json'), 'w'), indent=1)
print('models in the fix round:', len(rows), dict(Counter(r['verdict'] for r in rows)), '(plus', sum(1 for r in rows if r['id'] in EXTRA), 'OK-with-note)')
by = defaultdict(lambda: Counter())
for r in rows:
    by[(r['worker'], r['batch'])][r['verdict']] += 1
for k in sorted(by):
    c = by[k]
    print(f'{k[0]} {k[1]:14} n={sum(c.values()):3}  REDO {c["REDO"]} MAJOR {c["MAJOR"]} MINOR {c["MINOR"]} OK {c["OK"]}')
w = Counter(r['worker'] for r in rows)
print('per queue:', dict(sorted(w.items())))
print('categories:', dict(Counter(r['category'] for r in rows)))
