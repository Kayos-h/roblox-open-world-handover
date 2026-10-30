"""lead_verify - check the 31 models fixed in this pass in the LIBRARY: files exist and are new, category, triangles within budget, size within 10% of the manifest, every material key is in the palette."""
import os
import csv
import json
import glob
import time

LIB = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
import sys
fixed = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(LIB, 'v5_work', 'lead', 'fixed_ids.json')))
man = {r['id']: r for r in csv.DictReader(open(r"C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5\V5_MANIFEST.csv", encoding='utf-8-sig'))}
meta = {}
for f in glob.glob(os.path.join(LIB, 'v4_meta_v[a-j].json')):
    meta.update(json.load(open(f)))
pal = json.load(open(os.path.join(LIB, 'palette.json')))
now = time.time()
bad = 0
for i in fixed:
    m, r = meta[i], man[i]
    probs = []
    cat = m['category']
    for ext in ('.blend', '.fbx'):
        p = os.path.join(LIB, cat, i + ext)
        if not os.path.exists(p):
            probs.append('missing ' + ext)
        elif now - os.path.getmtime(p) > 3 * 3600:
            probs.append('old ' + ext)
    budget = int(float(r['tri_budget'] or 0))
    if budget and m['tris'] > budget:
        probs.append(f"tris {m['tris']} > {budget}")
    want = (float(r['size_x']), float(r['size_z']), float(r['size_y']))
    got = m['size']
    if all(w > 0 for w in want):
        for ax, (g, w) in zip('xyz', zip(got, want)):
            if abs(g - w) > 0.1 * w:
                probs.append(f'size {ax} {g:.1f} vs {w:.0f}')
    miss = [k for k in m['materials'] if k not in pal]
    if miss:
        probs.append('missing palette keys ' + str(miss[:3]))
    glow = [k for k in m['materials'] if pal.get(k, {}).get('glow')]
    if glow:
        probs.append('GLOW keys ' + str(glow))
    if probs:
        bad += 1
        print('PROBLEM', i[:38].ljust(38), '; '.join(probs))
print(f'{len(fixed)} models checked in the library: {len(fixed) - bad} pass every check, {bad} with a note')
