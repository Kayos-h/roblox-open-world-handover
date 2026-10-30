"""emissive_keys - list palette keys flagged glow, grouped by prefix, and say whether any v5 manifest model uses them."""
import json
import os
import csv
import glob
from collections import defaultdict

LIB = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
pal = json.load(open(os.path.join(LIB, 'palette.json')))
glow = {k: v for k, v in pal.items() if v.get('glow')}
print(len(glow), 'glow keys of', len(pal))
by = defaultdict(list)
for k in glow:
    by[k.split('_')[0]].append(k)
for p, ks in sorted(by.items()):
    print(p, len(ks), ks[:6])
man = {r['id'] for r in csv.DictReader(open(r"C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5\V5_MANIFEST.csv", encoding='utf-8-sig'))}
meta = {}
for f in glob.glob(os.path.join(LIB, 'v4_meta_v[a-j].json')):
    meta.update(json.load(open(f)))
sample = next(iter(meta.values()))
print('meta fields:', list(sample.keys()))
hit = []
for mid in man:
    m = meta.get(mid, {})
    blob = json.dumps(m)
    for k in glow:
        if k in blob:
            hit.append((mid, k))
print('v5 models that mention a glow key:', len(hit), hit[:8])
