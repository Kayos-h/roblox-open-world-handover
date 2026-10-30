"""make_r4 - id lists for the review of the 91 models of fix round 2 (tag r4): the 91 rebuilt models + 12 blind controls (rated OK by the r3 panel, never rebuilt).
Writes library\\v5_work\\r4\\pack_ids.json (kind changed2 / control) and quad_ids.json (four-angle sheets for big or complex models)."""
import os
import json
import glob
import random

LIB = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
R4 = os.path.join(LIB, 'v5_work', 'r4')
os.makedirs(R4, exist_ok=True)
fix2 = json.load(open(os.path.join(LIB, 'v5_work', 'r2', 'fix2_ids.json')))
r3 = json.load(open(os.path.join(LIB, 'v5_work', 'r3', 'review_defects_r3.json')))
meta = {}
for f in glob.glob(os.path.join(LIB, 'v4_meta_v[a-j].json')):
    meta.update(json.load(open(f)))
ok3 = [r['id'] for r in r3 if r['verdict'] == 'OK']
rnd = random.Random(44)
seen, ctl = set(), []
rnd.shuffle(ok3)
for i in ok3:
    fam = i[:4]
    if fam in seen:
        continue
    seen.add(fam)
    ctl.append(i)
    if len(ctl) == 12:
        break
pack = [{'id': r['id'], 'category': r['category'], 'kind': 'changed2', 'row': r['row']} for r in fix2 if r['owner'] != 'A1'] + [{'id': i, 'category': meta[i]['category'], 'kind': 'control', 'row': i.split('_')[0]} for i in ctl]
random.Random(45).shuffle(pack)
json.dump(pack, open(os.path.join(R4, 'pack_ids.json'), 'w'), indent=1)
quad = [p['id'] for p in pack if p['kind'] == 'changed2' and (p['id'].startswith(('LM', 'WT', 'CP15', 'CP16', 'CP11', 'CP14', 'CP19', 'BR', 'FL', 'RW', 'VC02', 'CP02', 'CP05', 'CP12', 'CP18', 'SP', 'HL', 'FR01', 'VC04', 'DS08')) or (meta[p['id']].get('tris') or 0) >= 3500)]
json.dump(quad, open(os.path.join(R4, 'quad_ids.json'), 'w'))
print(f'r4 pack: {len(pack)} models = {sum(1 for p in pack if p["kind"] == "changed2")} rebuilt + {len(ctl)} blind controls; four-angle sheets for {len(quad)}')
print('controls:', ctl)
