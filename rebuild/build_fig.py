"""Build the 3D figure of the Phase 1 map from sampled Studio data.
Inputs  (rebuild\\fig): heights_1..4.txt, boxes.txt, boxes_town1.txt
Outputs (rebuild\\fig): phase1_map.obj/.mtl, phase1_map.glb, phase1_map_topdown.png, README.txt
Scale: 100 studs = 1 unit (1 metre). Axes as in Roblox: +X east, +Y up, -Z north.
"""
import math, json, struct, os, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FIG = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\fig'
S = 0.01
STEP = 24
X0, X1 = -2400, 2400

# ------------------------------------------------------------------ parse heights
rows = {}
mats = None
for i in range(1, 5):
    for line in open(f'{FIG}\\heights_{i}.txt', encoding='ascii', errors='ignore').read().splitlines():
        line = line.strip()
        if line.startswith('MATS '):
            mats = line[5:].split(',')
        elif '|' in line and line.split('|')[0].lstrip('-').isdigit():
            z, rest = line.split('|', 1)
            cells = rest.split(',')
            rows[int(z)] = [(int(c.split(':')[0]), int(c.split(':')[1])) for c in cells]
zs = sorted(rows)
NX = len(rows[zs[0]])
assert all(len(rows[z]) == NX for z in zs), 'ragged rows'
H = np.array([[c[0] for c in rows[z]] for z in zs], dtype=np.float32)
Mi = np.array([[c[1] for c in rows[z]] for z in zs], dtype=np.int32)
NZ = len(zs)
xs = [X0 + STEP * i for i in range(NX)]
print('grid', NX, 'x', NZ, 'height range', H.min(), H.max(), 'materials', mats[:16])

MATCOL = {
    'Grass': (0.36, 0.62, 0.25), 'LeafyGrass': (0.24, 0.50, 0.20), 'Ground': (0.62, 0.50, 0.35), 'Mud': (0.38, 0.30, 0.22),
    'Sand': (0.86, 0.79, 0.56), 'Sandstone': (0.78, 0.60, 0.40), 'Rock': (0.50, 0.50, 0.50), 'Slate': (0.38, 0.40, 0.43),
    'Basalt': (0.26, 0.26, 0.29), 'Cobblestone': (0.55, 0.52, 0.48), 'Pavement': (0.62, 0.62, 0.62), 'Snow': (0.95, 0.97, 1.0),
    'Glacier': (0.75, 0.88, 0.95), 'Ice': (0.70, 0.86, 0.95), 'Limestone': (0.80, 0.78, 0.68), 'Salt': (0.9, 0.88, 0.85),
    'Asphalt': (0.2, 0.2, 0.2), 'Brick': (0.6, 0.3, 0.25), 'Concrete': (0.65, 0.65, 0.65), 'WoodPlanks': (0.6, 0.45, 0.28),
    'Water': (0.1, 0.4, 0.7), 'Air': (0.5, 0.5, 0.5)}
col_of = np.array([MATCOL.get(n, (0.5, 0.5, 0.5)) for n in mats], dtype=np.float32)

# clamp the seabed for drawing
Hd = np.maximum(H, -12.0)

# ------------------------------------------------------------------ boxes
AREA_COL = [
    ('enterable', (1.0, 0.82, 0.15)), ('town1_extra', (0.97, 0.96, 0.9)), ('town1_graveyard', (0.28, 0.28, 0.3)), ('town1_Walls', (0.6, 0.6, 0.64)),
    ('town1_Residential', (0.88, 0.78, 0.56)), ('town1_Market', (0.92, 0.66, 0.34)), ('town1_Plaza', (0.75, 0.75, 0.8)), ('town1_Bridges', (0.5, 0.36, 0.22)),
    ('town1_Farm', (0.75, 0.65, 0.35)), ('town1_Landmarks', (0.72, 0.5, 0.42)), ('town1_Crafts', (0.65, 0.45, 0.35)), ('town1', (0.82, 0.32, 0.3)),
    ('v3f_castle', (0.62, 0.66, 0.85)), ('v3_capital', (0.8, 0.54, 0.4)),
    ('v3_harbour', (0.35, 0.5, 0.72)), ('v3f_harbour', (0.35, 0.5, 0.72)),
    ('partbuilt_RustyHuts', (0.72, 0.4, 0.25)), ('v3_rusty', (0.72, 0.4, 0.25)), ('v3f_rusty', (0.62, 0.34, 0.22)),
    ('partbuilt_Igloos', (0.97, 0.98, 1.0)), ('partbuilt_IceShanties', (0.9, 0.35, 0.3)), ('partbuilt_FishingHoles', (0.1, 0.2, 0.4)),
    ('v3_alpine', (0.85, 0.9, 0.97)), ('v3f_alpine', (0.85, 0.9, 0.97)),
    ('v3_elf', (0.35, 0.8, 0.55)), ('v3f_elf', (0.35, 0.8, 0.55)),
    ('v3_country', (0.72, 0.62, 0.36)), ('v3f_country', (0.72, 0.62, 0.36)), ('v3f_se', (0.72, 0.62, 0.36))]


def area_color(a):
    for k, c in AREA_COL:
        if a == k:
            return k, c
    return 'other', (0.7, 0.7, 0.7)


boxes = []
for fn in ('boxes.txt', 'boxes_town1.txt'):
    for line in open(f'{FIG}\\{fn}', encoding='ascii', errors='ignore').read().splitlines():
        p = line.strip().split('|')
        if len(p) == 9:
            try:
                boxes.append((p[0], p[1], *[float(v) for v in p[2:]]))
            except ValueError:
                pass
print('boxes', len(boxes))


def ground_at(x, z):
    i = int(round((x - X0) / STEP)); j = int(round((z - zs[0]) / STEP))
    i = max(0, min(NX - 1, i)); j = max(0, min(NZ - 1, j))
    return float(Hd[j, i])


LANDMARKS = [
    ('Town 1 (skull town)', 0, 0, (1.0, 0.2, 0.2)), ('Capital', 0, -1500, (1.0, 0.5, 0.0)), ('Castle', 0, -2140, (0.6, 0.4, 1.0)),
    ('Harbour', -390, 1750, (0.1, 0.6, 1.0)), ('Rusty town', 1300, 1180, (0.9, 0.4, 0.1)), ('Elf valley (world tree)', -1560, -430, (0.1, 0.9, 0.4)),
    ('Alpine village', 1600, -880, (0.9, 0.95, 1.0)), ('Frozen lake', 1490, -1080, (0.4, 0.9, 1.0)), ('Tower mountain summit', 1380, -1300, (1.0, 1.0, 0.2))]

# ------------------------------------------------------------------ geometry builders
def box_corners(x, y, z, sx, sy, sz, rot):
    t = math.radians(rot)
    c, s = math.cos(t), math.sin(t)
    pts = []
    for ly in (-sy / 2, sy / 2):
        for lx, lz in ((-sx / 2, -sz / 2), (sx / 2, -sz / 2), (sx / 2, sz / 2), (-sx / 2, sz / 2)):
            pts.append((x + c * lx + s * lz, y + ly, z - s * lx + c * lz))
    return pts  # 0-3 bottom, 4-7 top


BOX_QUADS = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]  # outward-facing (right-handed)

solids = []   # (name, color, corners)
for a, n, x, y, z, sx, sy, sz, rot in boxes:
    k, c = area_color(a)
    sy = max(sy, 1.5)
    solids.append((k, c, box_corners(x, y, z, sx, sy, sz, rot)))
for name, x, z, c in LANDMARKS:
    g = ground_at(x, z)
    solids.append(('pillar', c, box_corners(x, g + 100, z, 14, 200, 14, 0)))
print('solids', len(solids))

# ------------------------------------------------------------------ terrain normals
dzdx = np.gradient(Hd, STEP, axis=1)
dzdz = np.gradient(Hd, STEP, axis=0)
nrm = np.stack([-dzdx, np.ones_like(Hd), -dzdz], axis=-1)
nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True)

SEA = dict(x0=-2700, x1=2700, z0=-2900, z1=2500)

# ------------------------------------------------------------------ OBJ + MTL
used_mats = sorted(set(Mi.flatten().tolist()))
mtl = []
for m in used_mats:
    c = MATCOL.get(mats[m], (0.5, 0.5, 0.5))
    mtl.append(f'newmtl t_{mats[m]}\nKd {c[0]:.3f} {c[1]:.3f} {c[2]:.3f}\nKa 0.2 0.2 0.2\nKs 0 0 0\nd 1\n')
mtl.append('newmtl sea\nKd 0.10 0.42 0.72\nKa 0.1 0.2 0.3\nKs 0.3 0.3 0.3\nd 0.55\nTr 0.45\n')
for k, c in sorted(set((k, c) for k, c, _ in solids)):
    mtl.append(f'newmtl b_{k}_{abs(hash(c)) % 997}\nKd {c[0]:.3f} {c[1]:.3f} {c[2]:.3f}\nKa 0.2 0.2 0.2\nKs 0 0 0\nd 1\n')
open(f'{FIG}\\phase1_map.mtl', 'w').write('\n'.join(mtl))

obj = ['# Phase 1 map (Black Clover-inspired Roblox game), 100 studs = 1 unit. +X east, +Y up, -Z north.', 'mtllib phase1_map.mtl']
for j in range(NZ):
    for i in range(NX):
        obj.append(f'v {xs[i] * S:.3f} {Hd[j, i] * S:.3f} {zs[j] * S:.3f}')
for j in range(NZ):
    for i in range(NX):
        n = nrm[j, i]
        obj.append(f'vn {n[0]:.3f} {n[1]:.3f} {n[2]:.3f}')
faces = {}
for j in range(NZ - 1):
    for i in range(NX - 1):
        a = j * NX + i + 1; b = a + 1; c = a + NX; d = c + 1
        m = int(Mi[j, i])
        faces.setdefault(m, []).extend([f'f {a}//{a} {c}//{c} {b}//{b}', f'f {b}//{b} {c}//{c} {d}//{d}'])
for m in used_mats:
    obj.append(f'usemtl t_{mats[m]}')
    obj.extend(faces.get(m, []))
base = NX * NZ
# sea
obj.append('usemtl sea')
sv = [(SEA['x0'], 0, SEA['z0']), (SEA['x1'], 0, SEA['z0']), (SEA['x1'], 0, SEA['z1']), (SEA['x0'], 0, SEA['z1'])]
for p in sv:
    obj.append(f'v {p[0] * S:.3f} {p[1]:.3f} {p[2] * S:.3f}')
obj.append(f'f {base + 1} {base + 4} {base + 3} {base + 2}')
base += 4
# solids
cur = None
for k, c, pts in solids:
    mname = f'b_{k}_{abs(hash(c)) % 997}'
    if mname != cur:
        obj.append(f'usemtl {mname}'); cur = mname
    for p in pts:
        obj.append(f'v {p[0] * S:.3f} {p[1] * S:.3f} {p[2] * S:.3f}')
    for q in BOX_QUADS:
        obj.append('f ' + ' '.join(str(base + v + 1) for v in q))
    base += 8
open(f'{FIG}\\phase1_map.obj', 'w').write('\n'.join(obj))
print('obj lines', len(obj))

# ------------------------------------------------------------------ GLB
def pack(arr, dtype):
    return np.ascontiguousarray(arr, dtype=dtype).tobytes()


prims = []
# terrain
pos = np.stack([np.repeat(np.array(xs)[None, :], NZ, 0) * S, Hd * S, np.repeat(np.array(zs)[:, None], NX, 1) * S], axis=-1).reshape(-1, 3)
col = col_of[Mi.reshape(-1)]
idx = []
for j in range(NZ - 1):
    for i in range(NX - 1):
        a = j * NX + i; b = a + 1; c = a + NX; d = c + 1
        idx.extend([a, c, b, b, c, d])
prims.append(dict(pos=pos, nrm=nrm.reshape(-1, 3), col=col, idx=np.array(idx, dtype=np.uint32), mat=0))
# sea
sp = np.array([[SEA['x0'] * S, 0, SEA['z0'] * S], [SEA['x1'] * S, 0, SEA['z0'] * S], [SEA['x1'] * S, 0, SEA['z1'] * S], [SEA['x0'] * S, 0, SEA['z1'] * S]], dtype=np.float32)
prims.append(dict(pos=sp, nrm=np.tile([0, 1, 0], (4, 1)).astype(np.float32), col=np.ones((4, 3), np.float32), idx=np.array([0, 3, 2, 0, 2, 1], dtype=np.uint32), mat=1))
# solids with flat normals
bp, bn, bc, bi = [], [], [], []
for k, c, pts in solids:
    for q in BOX_QUADS:
        p = [np.array(pts[v]) * S for v in q]
        n = np.cross(p[1] - p[0], p[2] - p[0]); ln = np.linalg.norm(n)
        n = n / ln if ln > 1e-12 else np.array([0, 1, 0])
        o = len(bp)
        for v in p:
            bp.append(v); bn.append(n); bc.append(c)
        bi.extend([o, o + 1, o + 2, o, o + 2, o + 3])
prims.append(dict(pos=np.array(bp, np.float32), nrm=np.array(bn, np.float32), col=np.array(bc, np.float32), idx=np.array(bi, dtype=np.uint32), mat=0))

bin_chunks, views, accs, gprims = [], [], [], []
off = 0
def add_view(data, target):
    global off
    pad = (-off) % 4
    if pad:
        bin_chunks.append(b'\x00' * pad); off += pad
    views.append({'buffer': 0, 'byteOffset': off, 'byteLength': len(data), 'target': target})
    bin_chunks.append(data); off += len(data)
    return len(views) - 1
for p in prims:
    pa = np.asarray(p['pos'], np.float32)
    accs.append({'bufferView': add_view(pack(pa, np.float32), 34962), 'componentType': 5126, 'count': len(pa), 'type': 'VEC3',
                 'min': pa.min(0).tolist(), 'max': pa.max(0).tolist()}); ap = len(accs) - 1
    na = np.asarray(p['nrm'], np.float32)
    accs.append({'bufferView': add_view(pack(na, np.float32), 34962), 'componentType': 5126, 'count': len(na), 'type': 'VEC3'}); an = len(accs) - 1
    ca = np.asarray(p['col'], np.float32)
    accs.append({'bufferView': add_view(pack(ca, np.float32), 34962), 'componentType': 5126, 'count': len(ca), 'type': 'VEC3'}); ac = len(accs) - 1
    ia = np.asarray(p['idx'], np.uint32)
    accs.append({'bufferView': add_view(pack(ia, np.uint32), 34963), 'componentType': 5125, 'count': len(ia), 'type': 'SCALAR'}); ai = len(accs) - 1
    gprims.append({'attributes': {'POSITION': ap, 'NORMAL': an, 'COLOR_0': ac}, 'indices': ai, 'material': p['mat'], 'mode': 4})
binblob = b''.join(bin_chunks)
binblob += b'\x00' * ((-len(binblob)) % 4)
gltf = {
    'asset': {'version': '2.0', 'generator': 'phase1 figure builder'},
    'scene': 0, 'scenes': [{'nodes': [0]}], 'nodes': [{'mesh': 0, 'name': 'Phase1Map'}],
    'meshes': [{'primitives': gprims, 'name': 'Phase1Map'}],
    'materials': [{'name': 'vertexcolor', 'pbrMetallicRoughness': {'baseColorFactor': [1, 1, 1, 1], 'metallicFactor': 0.0, 'roughnessFactor': 0.95}, 'doubleSided': True},
                  {'name': 'sea', 'pbrMetallicRoughness': {'baseColorFactor': [0.10, 0.42, 0.72, 0.55], 'metallicFactor': 0.0, 'roughnessFactor': 0.15}, 'alphaMode': 'BLEND', 'doubleSided': True}],
    'accessors': accs, 'bufferViews': views, 'buffers': [{'byteLength': len(binblob)}]}
js = json.dumps(gltf, separators=(',', ':')).encode()
js += b' ' * ((-len(js)) % 4)
with open(f'{FIG}\\phase1_map.glb', 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(js) + 8 + len(binblob)))
    f.write(struct.pack('<II', len(js), 0x4E4F534A)); f.write(js)
    f.write(struct.pack('<II', len(binblob), 0x004E4942)); f.write(binblob)
print('glb bytes', os.path.getsize(f'{FIG}\\phase1_map.glb'))

# ------------------------------------------------------------------ top-down labelled map
UP = 8
W_, H_ = NX * UP, NZ * UP
col_img = Image.fromarray((np.clip(col_of[Mi], 0, 1) * 255).astype(np.uint8), 'RGB').resize((W_, H_), Image.BICUBIC)
hi = np.array(Image.fromarray(Hd.astype(np.float32), 'F').resize((W_, H_), Image.BICUBIC), dtype=np.float32)
gy, gx = np.gradient(hi, STEP / UP)
shade = np.clip(0.62 + (-gx * 0.55 - gy * 0.55) * 0.9, 0.25, 1.35)
rgb = np.array(col_img, dtype=np.float32) / 255.0 * shade[..., None]
sea = hi < 0.2
depth = np.clip(-hi / 40.0, 0, 1)[..., None]
seacol = (1 - depth) * np.array([0.22, 0.58, 0.82]) + depth * np.array([0.05, 0.22, 0.48])
rgb = np.where(sea[..., None], seacol, rgb)
img = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), 'RGB')
dr = ImageDraw.Draw(img, 'RGBA')


def px(x, z):
    return ((x - X0) / STEP * UP + UP / 2, (z - zs[0]) / STEP * UP + UP / 2)


for k, c, pts in solids:
    if k == 'pillar':
        continue
    poly = [px(p[0], p[2]) for p in pts[:4]]
    dr.polygon(poly, fill=tuple(int(v * 255) for v in c) + (235,), outline=(30, 30, 30, 200))
try:
    font = ImageFont.truetype('C:\\Windows\\Fonts\\arialbd.ttf', 34)
    small = ImageFont.truetype('C:\\Windows\\Fonts\\arial.ttf', 24)
except Exception:
    font = small = ImageFont.load_default()
for name, x, z, c in LANDMARKS:
    X, Z = px(x, z)
    dr.ellipse((X - 9, Z - 9, X + 9, Z + 9), fill=tuple(int(v * 255) for v in c) + (255,), outline=(0, 0, 0, 255), width=3)
    tx, ty = X + 16, Z - 18
    tw = dr.textlength(name, font=font)
    if tx + tw > W_ - 12:
        tx = X - 16 - tw
    for ox, oy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2)):
        dr.text((tx + ox, ty + oy), name, font=font, fill=(0, 0, 0, 255))
    dr.text((tx, ty), name, font=font, fill=(255, 255, 255, 255))
# scale bar and north arrow
bx, by = 70, H_ - 70
dr.rectangle((bx, by, bx + 500 / 3, by + 12), fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
dr.text((bx, by - 34), '500 studs', font=small, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
dr.polygon([(W_ - 90, 150), (W_ - 110, 210), (W_ - 70, 210)], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
dr.text((W_ - 102, 100), 'N', font=font, fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0, 255))
# legend
lx, ly = 40, 40
items = [('Enterable buildings', (1.0, 0.82, 0.15)), ('Town 1 houses', (0.88, 0.78, 0.56)), ('Capital / castle', (0.8, 0.54, 0.4)), ('Harbour', (0.35, 0.5, 0.72)),
         ('Rusty town', (0.72, 0.4, 0.25)), ('Alpine / igloos', (0.85, 0.9, 0.97)), ('Elf valley', (0.35, 0.8, 0.55)), ('Farms / country', (0.72, 0.62, 0.36))]
dr.rectangle((lx - 12, ly - 12, lx + 300, ly + 36 * len(items) + 8), fill=(0, 0, 0, 150))
for n, c in items:
    dr.rectangle((lx, ly, lx + 24, ly + 24), fill=tuple(int(v * 255) for v in c) + (255,), outline=(255, 255, 255, 255))
    dr.text((lx + 36, ly - 1), n, font=small, fill=(255, 255, 255, 255))
    ly += 36
img.save(f'{FIG}\\phase1_map_topdown.png')
print('png', img.size)

open(f'{FIG}\\README.txt', 'w').write(f"""Phase 1 map, 3D figure
Built {len(boxes)} building boxes + terrain ({NX}x{NZ} samples, {STEP}-stud spacing).

Files
  phase1_map.glb           terrain with smooth vertex colours, sea, buildings as coloured boxes, 9 tall marker pillars. Open in Windows 3D Viewer, Blender, https://gltf-viewer.donmccurdy.com
  phase1_map.obj + .mtl    same model as OBJ (keep both files in one folder). Terrain coloured per cell.
  phase1_map_topdown.png   labelled top-down map

Scale and axes: 100 studs = 1 unit. +X east, +Y up, -Z north (as in Roblox). Island is about 48 units across.
Boxes are bounding boxes of the real models, so they are rough. Gold boxes are the 7 enterable buildings.

Marker pillars (200 studs tall, 14 wide):
""" + '\n'.join(f'  {n:<28} x {x:>6}  z {z:>6}' for n, x, z, c in LANDMARKS) + '\n')
print('done')
