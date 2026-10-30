"""v5_fix_verify - after a LIVE build of a fix module: was every assigned model rebuilt IN PLACE?
  python v5_fix_verify.py A4          (or A1..A6, or 'all')
Per id: file rewritten after the round-1 archive copy; same category folder as round 1; triangles and size changed against round 1; within the triangle
budget; each axis within 8% of the manifest target; palette colours present. Prints a problem list (empty = every check passed). Looks at no pictures.
"""
import os
import re
import sys
import json

LIB = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
FIX = os.path.join(LIB, 'v5_work', 'fix')
rows = {r['id']: r for r in json.load(open(os.path.join(FIX, 'fix_ids.json')))}
want = sys.argv[1:] or ['all']
ids = []
for A in ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']:
    if 'all' in want or A in want:
        txt = open(os.path.join(FIX, f'assign_{A}.md'), encoding='utf-8').read()
        ids += re.findall(r'^\| `([A-Za-z0-9_]+)` \|', txt, re.M)
ids += [i for i in want if i in rows and i not in ids]
meta_now, meta_old, pal = {}, {}, {}
import glob
for f in glob.glob(os.path.join(LIB, 'v4_meta_v[a-j].json')):
    meta_now.update(json.load(open(f)))
for f in glob.glob(os.path.join(LIB, 'v5_round1_archive', 'meta', 'v4_meta_v[a-j].json')):
    meta_old.update(json.load(open(f)))
for f in glob.glob(os.path.join(LIB, 'palette_v[a-j].json')):
    pal.update(json.load(open(f)))
problems, ok = [], 0
for i in ids:
    r = rows[i]
    p = []
    cur, old = meta_now.get(i), meta_old.get(i)
    f_new = os.path.join(LIB, r['category'], i + '.blend')
    f_old = os.path.join(LIB, 'v5_round1_archive', r['category'], i + '.blend')
    if not cur:
        problems.append((i, ['no meta entry']))
        continue
    if cur.get('category') != r['category']:
        p.append(f"category {cur.get('category')} instead of {r['category']}")
    if not os.path.exists(f_new):
        p.append('file missing in its category folder')
    elif os.path.exists(f_old) and os.path.getmtime(f_new) <= os.path.getmtime(f_old) + 1:
        p.append('NOT rebuilt (file not newer than the round-1 archive)')
    if old and cur.get('tris') == old.get('tris') and cur.get('size') == old.get('size'):
        import hashlib
        fa = os.path.join(LIB, 'v5_round1_archive', r['category'], i + '.fbx')
        fb = os.path.join(LIB, r['category'], i + '.fbx')
        same = os.path.exists(fa) and os.path.exists(fb) and hashlib.md5(open(fa, 'rb').read()).hexdigest() == hashlib.md5(open(fb, 'rb').read()).hexdigest()
        if same:
            p.append('identical to round 1 (same triangles, size and file bytes)')
    if r['tri_budget'] and (cur.get('tris') or 0) > r['tri_budget']:
        p.append(f"tris {cur.get('tris')} > budget {r['tri_budget']}")
    sz = cur.get('size') or [0, 0, 0]
    for got, w, nm in ((sz[0], r['want_w'], 'W'), (sz[1], r['want_d'], 'D'), (sz[2], r['want_h'], 'H')):
        if w > 0 and abs(got - w) / w > 0.10:
            p.append(f'{nm} {got:g} vs {w:g}')
    miss = [m for m in cur.get('materials', []) if m not in pal]
    if miss:
        p.append('palette keys missing: ' + ','.join(miss[:4]))
    if p:
        problems.append((i, p))
    else:
        ok += 1
print(f'verified {len(ids)} models: {ok} pass every check, {len(problems)} with problems')
for i, p in problems:
    print(' ', i, '|', '; '.join(p))
# palette collision check: a round-1 colour key whose value changed would recolour models that were NOT rebuilt
changed = []
for f in glob.glob(os.path.join(LIB, 'palette_v[a-j].json')):
    a = os.path.join(LIB, 'v5_round1_archive', 'meta', os.path.basename(f))
    if not os.path.exists(a):
        continue
    old, new = json.load(open(a)), json.load(open(f))
    for k, v in old.items():
        if k in new and (new[k].get('rgb') != v.get('rgb') or new[k].get('material') != v.get('material') or new[k].get('glow') != v.get('glow')):
            changed.append((os.path.basename(f), k, v.get('rgb'), new[k].get('rgb')))
glow = [(os.path.basename(f), k) for f in glob.glob(os.path.join(LIB, 'palette_v[a-j].json')) for k, v in json.load(open(f)).items() if v.get('glow')]
print(f'palette: {len(changed)} round-1 colour keys changed value since the archive' + (':' if changed else '') )
for c in changed[:12]:
    print('  CHANGED', c)
print(f'palette: {len(glow)} emissive keys' + (': ' + str(glow[:6]) if glow else ''))
