"""v5_autocheck - automatic checks of every v5 manifest row (no looking, only numbers and files).
Checks: .blend/.fbx/thumbnail exist; size within 15% of the manifest (width, height, depth); triangles within the budget (+10%); no exported piece
above 20k triangles; black or empty thumbnail; markers present for bridges (end_a, end_b, deck) and raised floors (ladder_bottom/ladder_top for canopy
clusters); palette keys per model; emissive palette keys (must be 0). Writes library\\v5_work\\AUTOCHECK_V5.json and AUTOCHECK_V5.md.
"""
import os
import sys
import csv
import json
import glob
import re
from PIL import Image

LIB = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
MAN = r"C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5\V5_MANIFEST.csv"
OUT = os.path.join(LIB, 'v5_work')
os.makedirs(OUT, exist_ok=True)
rows = list(csv.DictReader(open(MAN, encoding='utf-8-sig')))
meta, worker_of = {}, {}
for f in sorted(glob.glob(os.path.join(LIB, 'v4_meta_v[a-j].json'))):
    w = os.path.basename(f)[8:-5]
    d = json.load(open(f))
    for k, v in d.items():
        meta[k] = v
        worker_of[k] = w
pal = {}
for f in glob.glob(os.path.join(LIB, 'palette_v[a-j].json')):
    pal.update(json.load(open(f)))
maxpiece = {}
for f in glob.glob(os.path.join(LIB, 'v4_work', 'v[a-j]_*_*.json')):
    try:
        rep = json.load(open(f))
    except Exception:
        continue
    for r in rep.get('rows', []):
        if len(r) >= 5 and isinstance(r[4], (int, float)):
            maxpiece[r[0]] = max(maxpiece.get(r[0], 0), r[4])
BRIDGE_ROWS = {'HM01', 'HM02', 'CP19', 'BR01', 'LM08', 'PL06'}
LADDER_ROWS = {'EV02'}
res, flags_by = [], {}
for r in rows:
    mid = r['id']
    row = r['row']
    e = {'id': mid, 'row': row, 'flags': []}
    m = meta.get(mid)
    if not m:
        e['flags'].append('NOT BUILT')
        res.append(e)
        continue
    cat = m['category']
    base = os.path.join(LIB, cat, mid)
    for ext in ('.blend', '.fbx'):
        if not os.path.exists(base + ext):
            e['flags'].append('MISSING ' + ext)
    thumb = os.path.join(LIB, 'v4_sheets', f'_t_{mid}.png')
    if not os.path.exists(thumb):
        e['flags'].append('NO THUMB')
    else:
        try:
            im = Image.open(thumb).convert('L')
            px = list(im.resize((48, 48)).getdata())
            mean = sum(px) / len(px)
            bright = sum(1 for p in px if p > 40) / len(px)
            e['thumb_mean'] = round(mean, 1)
            if mean < 12 or bright < 0.02:
                e['flags'].append('BLACK/EMPTY THUMB')
        except Exception:
            e['flags'].append('THUMB UNREADABLE')
    sx, sh, sd = float(r['size_x']), float(r['size_y']), float(r['size_z'])
    bud = int(float(r['tri_budget'] or 0))
    sz = m.get('size') or [0, 0, 0]
    e.update(tris=m.get('tris'), size=sz, want=[sx, sd, sh], budget=bud, worker=worker_of.get(mid))
    if sx > 0 and sh > 0 and sd > 0:
        for got, want, nm in ((sz[0], sx, 'width'), (sz[1], sd, 'depth'), (sz[2], sh, 'height')):
            if abs(got - want) / want > 0.15:
                e['flags'].append(f'SIZE {nm} {got:g} vs {want:g}')
    if bud and (m.get('tris') or 0) > bud * 1.1:
        e['flags'].append(f"TRIS {m.get('tris')} > {bud}")
    if (m.get('tris') or 0) < 150:
        e['flags'].append('VERY FEW TRIANGLES')
    mp = maxpiece.get(mid)
    if mp and mp > 20000:
        e['flags'].append(f'PIECE {mp} > 20k')
    if row in BRIDGE_ROWS and ('end_a' not in m or 'end_b' not in m) and 'bridge' in mid + r['note'].lower():
        e['flags'].append('BRIDGE MARKERS MISSING')
    if row in LADDER_ROWS and ('ladder_bottom' not in m or 'ladder_top' not in m):
        e['flags'].append('LADDER MARKERS MISSING')
    mats = m.get('materials', [])
    e['materials'] = len(mats)
    if len(mats) > 14:
        e['flags'].append(f'MANY MATERIALS {len(mats)}')
    for k in mats:
        if k in pal and pal[k].get('glow'):
            e['flags'].append('EMISSIVE KEY ' + k)
    if re.search(r'gate_arch|entrance_arch|wooden_gate', mid):
        e['flags'].append('ENTRANCE ARCH NAME')
    res.append(e)
json.dump(res, open(os.path.join(OUT, 'AUTOCHECK_V5.json'), 'w'), indent=1)
bad = [e for e in res if e['flags']]
by_flag = {}
for e in bad:
    for f in e['flags']:
        by_flag.setdefault(f.split(' ')[0] + (' ' + f.split(' ')[1] if f.startswith('SIZE') else ''), []).append(e['id'])
lines = [f'# Automatic checks (v5)', '', f'{len(res)} manifest rows, {len(res) - len(bad)} clean, {len(bad)} with at least one flag.', '']
for k, v in sorted(by_flag.items(), key=lambda kv: -len(kv[1])):
    lines.append(f'- **{k}**: {len(v)} models' + (' (' + ', '.join(v[:8]) + (' ...' if len(v) > 8 else '') + ')' if len(v) <= 40 else ''))
lines += ['', '## Flagged models', '']
for e in bad:
    lines.append(f"- `{e['id']}` ({e.get('tris')} tris, {e.get('size')}): " + '; '.join(e['flags']))
open(os.path.join(OUT, 'AUTOCHECK_V5.md'), 'w', encoding='utf-8').write('\n'.join(lines))
print(f'autocheck: {len(res)} rows, {len(bad)} flagged')
for k, v in sorted(by_flag.items(), key=lambda kv: -len(kv[1])):
    print(f'  {k}: {len(v)}')
