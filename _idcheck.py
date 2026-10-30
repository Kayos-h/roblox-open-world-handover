import os, sys, json, glob, re, collections
SRC = r'C:\Users\Nitro\.kiro\crew\workspace\town\library\src'
sys.path.insert(0, SRC)
import v4_manifest as M
LIB = M.LIB
ids = {r['id'] for r in M.expand()}
ids.add('EV01_treehouse_a')
by = collections.OrderedDict()
for p in sorted(glob.glob(os.path.join(LIB, 'v4_meta_*.json'))):
    w = os.path.basename(p)[8:-5]
    try:
        d = json.load(open(p))
    except Exception as e:
        print(w, 'unreadable', e)
        continue
    bad = [k for k in d if k not in ids]
    ok = [k for k in d if k in ids]
    print(f'{w}: {len(d)} entries, {len(ok)} match manifest ids, {len(bad)} do NOT match')
    for k in bad:
        e = d[k]
        fb = os.path.exists(os.path.join(LIB, e.get('category', ''), k + '.fbx'))
        print(f'    {k}  cat={e.get("category")} tris={e.get("tris")} fbx={fb}')
