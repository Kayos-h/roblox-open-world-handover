"""vb module - wizard tower INTERIOR and props: WT02 interior shell (+ tower_collision.json), WT05 circular map table,
WT06 floor medallion, WT03 curved bookshelves, WT04 straight/island shelves, WT07 lab sets, WT08 study sets,
WT09 chandeliers, WT10 telescope. Radii, floors and windows come from v5kit.TOWER (same numbers as WT01).
No glow anywhere: candles, lamps and glassware are plain meshes. Sizes in briefs are (x, height, depth) Roblox axes.
"""
import math
import random
import json
import os
import numpy as np
import bpy
import kitlib
from kitlib import reset, finalize
import v5kit
from v5kit import Acc, polar, tang, TOWER as T, tower_top, tower_openings
import v4util

v5kit.wiz_pal('vb')
K = {n: 'vb_' + n for n in v5kit.WIZ}
kitlib.PAL['vb_glass'] = ((176, 212, 226), 'SmoothPlastic', 0.0, 0.25, 0)
kitlib.PAL['vb_wax'] = ((236, 226, 200), 'SmoothPlastic', 0.0, 0.8, 0)
kitlib.PAL['vb_ring'] = ((184, 148, 70), 'Metal', 0.85, 0.30, 0)
K['glass'] = 'vb_glass'
K['wax'] = 'vb_wax'
K['ring'] = 'vb_ring'
BOOK = ['vb_bk_red', 'vb_bk_navy', 'vb_bk_green', 'vb_bk_brown', 'vb_bk_slate']
for _n, _rgb in zip(BOOK, ((128, 54, 52), (58, 72, 112), (62, 98, 78), (120, 88, 58), (96, 98, 110))):
    kitlib.PAL[_n] = (_rgb, 'Fabric', 0.0, 0.95, 0)
LIBDIR = os.path.join(kitlib.LIB, 'v5_wizard')


# ------------------------------------------------------------------ tower interior geometry shared by visuals and collision
def _rin(i):
    return T['outer_d'][i] / 2.0 - T['wall']


def _Rs(z):
    """Stair centre radius at height z: mid-level control points, linear in between (the stair spirals inward as the tower narrows)."""
    F = T['floors']
    mids = [(F[i] + tower_top(i)) / 2.0 for i in range(8)]
    rs = [_rin(i) - 9.5 for i in range(8)]
    if z <= mids[0]:
        return rs[0]
    for i in range(7):
        if z <= mids[i + 1]:
            t = (z - mids[i]) / (mids[i + 1] - mids[i])
            return rs[i] + (rs[i + 1] - rs[i]) * t
    return rs[7]


def _geometry():
    """Helical stair treads (rise <= 1.1, run 2.4, 7 wide, 10-deep landings at every floor) and the angular gap each floor plate needs."""
    F = T['floors']
    phi, z = 330.0, 0.0
    treads, gaps = [], {}
    for i in range(7):
        H = F[i + 1] - F[i]
        n = int(math.ceil(H / 1.1))
        rise = H / n
        g_start, g_end = None, None
        for s in range(n):
            z += rise
            R = _Rs(z - rise / 2.0)
            dphi = 137.5 / R
            phi += dphi
            treads.append(dict(z=z, R=R, phi=phi, rise=rise, kind='c'))
            if g_start is None and z > F[i + 1] - 11.5:
                g_start = phi - dphi * 1.5
            g_end = phi - dphi * 0.5
        gaps[i + 1] = (g_start, g_end)
        for s in range(4):
            R = _Rs(z)
            phi += 137.5 / R
            treads.append(dict(z=z, R=R, phi=phi, rise=0.6, kind='l'))
    return treads, gaps


def _wedges(col, name, r0, r1, a0, a1, z_top, thick, step=7.5):
    n = max(1, int(math.ceil((a1 - a0) / step)))
    for k in range(n):
        a = a0 + (a1 - a0) * (k + 0.5) / n
        da = math.radians((a1 - a0) / n)
        chord = (2.0 * r1 * math.sin(da / 2.0) + 0.4) if r1 > 1.0 else 1.0
        x, y, _ = polar((r0 + r1) / 2.0, a)
        col.append({'n': name, 'p': [round(x, 2), round(y, 2), round(z_top - thick / 2.0, 2)],
                    's': [round(chord, 2), round(r1 - r0, 2), round(thick, 2)], 'yaw': round(a + 90.0, 2)})


def interior_shell():
    """WT02_01 - 7 floor plates + observatory disc, open atrium, helical stair with rails, wall linings, window reveals,
    star ceiling, dome ribs. Also writes tower_collision.json (boxes in tower-local Blender coordinates: x right, y back, z up)."""
    reset()
    A = Acc()
    col = []
    F, front = T['floors'], T['front_deg']
    treads, gaps = _geometry()
    # floor plates and atrium rails
    for f in range(1, 8):
        z = float(F[f])
        g0, g1 = gaps[f]
        rp = _rin(f - 1) + 0.3
        ra = _rin(f) - 14.0 if f < 7 else 0.4
        a_from, a_to = g1, g0 + 360.0
        n = int(math.ceil((a_to - a_from) / 6.0))
        A.sweep([(ra, z - 1.5), (rp, z - 1.5), (rp, z), (ra, z)], a_from, a_to, n, K['granite'] if f % 2 else K['limestone'])
        A.sweep([(ra + 0.5, z), (rp - 0.5, z), (rp - 0.5, z + 0.12), (ra + 0.5, z + 0.12)], a_from + 1, a_to - 1, n, K['white'])
        _wedges(col, f'floor{f}', ra if f < 7 else 0.0, rp, a_from, a_to, z, 1.5)
        if f < 7:
            a = a_from + 2.0
            while a < a_to - 2.0:
                x, y, _ = polar(ra + 0.35, a)
                A.box((0.5, 0.5, 3.6), (x, y, z + 1.8), K['timber'])
                a += 6.0
            A.sweep([(ra, z + 3.4), (ra + 0.7, z + 3.4), (ra + 0.7, z + 4.0), (ra, z + 4.0)], a_from + 1, a_to - 1, n, K['brass'])
            _wedges(col, f'atrium_rail{f}', ra, ra + 0.7, a_from + 1, a_to - 1, z + 4.0, 4.0)
    # star-chart ceiling under the observatory disc, with brass stars
    g0, g1 = gaps[7]
    A.sweep([(0.4, 230.25), (19.6, 230.25), (19.6, 230.5), (0.4, 230.5)], g1, g0 + 360.0, 48, K['indigo'])
    rnd = random.Random(11)
    for s in range(42):
        a = rnd.uniform(g1 + 4, g0 + 356)
        r = rnd.uniform(2.0, 18.5)
        x, y, _ = polar(r, a)
        A.box((rnd.uniform(0.35, 0.8),) * 2 + (0.06,), (x, y, 230.2), K['brass'], (0, 0, rnd.uniform(0, 90)))
    # helical stair with landings, rails and an under-ribbon
    prev = None
    for idx, t in enumerate(treads):
        z, R, ph, rs, kind = t['z'], t['R'], t['phi'], t['rise'], t['kind']
        th = rs + 0.7 if kind == 'c' else 0.8
        x, y, _ = polar(R, ph)
        A.box((2.55, 7.0, th), (x, y, z - th / 2.0), K['granite'] if kind == 'c' else K['limestone'], (0, 0, ph + 90.0))
        col.append({'n': 'tread', 'p': [round(x, 2), round(y, 2), round(z - th / 2.0, 2)], 's': [2.55, 7.0, round(th, 2)], 'yaw': round(ph + 90.0, 2)})
        xi, yi, _ = polar(R - 3.3, ph)
        xo, yo, _ = polar(R + 3.3, ph)
        pin, pout, pc = (xi, yi, z + 3.2), (xo, yo, z + 3.2), (x, y, z - th + 0.3)
        if prev is not None:
            A.beam(prev[0], pin, 0.32, 0.32, K['brass'])
            A.beam(prev[1], pout, 0.32, 0.32, K['timber'])
            A.beam(prev[2], pc, 5.6, 0.9, K['timber'], up=(0, 0, 1))
        if idx % 3 == 0:
            A.box((0.4, 0.4, 3.3), (xi, yi, z + 1.65), K['brass'])
            A.box((0.4, 0.4, 3.3), (xo, yo, z + 1.65), K['timber'])
        prev = (pin, pout, pc)
    # wall linings: timber wainscot, limestone picture rail, window reveals
    for i in range(8):
        z0, z1 = F[i], tower_top(i)
        ri = _rin(i)
        door = [(front, 11.0, [(0.0, 13.0)])] if i == 0 else []
        A.ring_wall(ri - 0.6, ri, z0, z0 + 6.0, door, K['timber'])
        A.sweep([(ri - 1.4, z1 - 3.2), (ri, z1 - 3.2), (ri, z1 - 1.8), (ri - 1.4, z1 - 1.8)], 0, 360, 48, K['limestone'])
        ops, wins, tiers = tower_openings(i)
        for ang in wins:
            tx, ty = tang(ang)
            c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            for lo, hi in tiers:
                for zz, key in ((lo - 0.35, K['limestone']), (hi + 0.35, K['timber'])):
                    A.box((2.4, 15.2, 0.7), ((ri - 0.3) * c, (ri - 0.3) * s, zz), key, (0, 0, ang))
                for sg in (-1, 1):
                    A.box((2.2, 0.5, hi - lo), ((ri - 0.2) * c + tx * sg * 7.25, (ri - 0.2) * s + ty * sg * 7.25, (lo + hi) / 2.0), K['timber'], (0, 0, ang))
        # wall collision: wall pieces between openings, sills, mid pieces and lintels
        rm = ri + 3.0
        ops_sorted = sorted(ops, key=lambda o: o[0] % 360.0)
        for k, (c, w, tl) in enumerate(ops_sorted):
            hw = math.degrees((w / 2.0) / ((ri + ri + 6) / 2.0))
            c %= 360.0
            nc, nw, _ = ops_sorted[(k + 1) % len(ops_sorted)]
            nc %= 360.0
            if k == len(ops_sorted) - 1:
                nc += 360.0
            nhw = math.degrees((nw / 2.0) / ((ri + ri + 6) / 2.0))
            if nc - nhw - (c + hw) > 0.1:
                _wedges(col, f'wall{i}', ri, ri + 6.0, c + hw, nc - nhw, z1, z1 - z0, 9.0)
            zs = [z0] + [q for pair in tl for q in pair] + [z1]
            for m in range(0, len(zs), 2):
                if zs[m + 1] - zs[m] > 0.05:
                    x, y, _ = polar(rm, c)
                    col.append({'n': f'wallcol{i}', 'p': [round(x, 2), round(y, 2), round((zs[m] + zs[m + 1]) / 2.0, 2)],
                                's': [round(w, 2), 6.0, round(zs[m + 1] - zs[m], 2)], 'yaw': round(c + 90.0, 2)})
    # dome ribs and a brass oculus ring inside the observatory dome
    zd = float(T['top_deck'])
    rdi, hdi = T['outer_d'][7] / 2.0 + 0.6 - 2.2 - 0.3, 22.8
    for m in range(12):
        a = front + 9.0 + 14.0 + m * 28.0
        pts = [polar(rdi * math.cos(math.radians(t)), a, zd + hdi * math.sin(math.radians(t))) for t in range(0, 81, 10)]
        for p0, p1 in zip(pts, pts[1:]):
            A.beam(p0, p1, 0.5, 0.5, K['brass'])
    A.to_scene()
    ob = finalize('wizard_tower_interior', smooth_angle=25)
    os.makedirs(LIBDIR, exist_ok=True)
    json.dump({'about': 'tower-local boxes, Blender axes (x right, y back, front is -y, z up), studs; p=centre, s=(tangent, radial, height) before yaw, yaw=degrees about Z; floors/tread/atrium_rail/wall*',
               'count': len(col), 'boxes': col}, open(os.path.join(LIBDIR, 'tower_collision.json'), 'w'))
    return ob


# ------------------------------------------------------------------ WT06 floor medallion
def floor_medallion():
    """WT06_01 - 80 wide round inlay: granite field, limestone and brass rings, 16-point star ring, compass rose, indigo centre."""
    reset()
    A = Acc()
    ring = lambda r0, r1, z0, z1, key, n=72: A.sweep([(r0, z0), (r1, z0), (r1, z1), (r0, z1)], 0, 360, n, key)
    ring(0.4, 40.0, 0.0, 0.5, K['granite'])
    ring(36.5, 39.0, 0.5, 0.8, K['limestone'])
    ring(35.4, 36.2, 0.5, 0.85, K['brass'])
    ring(29.0, 29.7, 0.5, 0.85, K['brass'])
    ring(22.0, 28.4, 0.5, 0.75, K['white'])
    ring(21.0, 21.8, 0.5, 0.85, K['brass'])
    A.cyl(20.2, 0.7, (0, 0, 0.5), K['indigo'], verts=48)
    for k in range(16):
        a = k * 22.5
        r_in, r_out = 22.0, 34.0 if k % 2 == 0 else 29.0
        A.prism([(-1.2, 0.0), (1.2, 0.0), (0.0, r_out - r_in)], 0.3, polar(r_in, a), K['ochre'] if k % 2 == 0 else K['limestone'], (0, 0, a - 90.0), z0=0.5)
    for k in range(8):
        a = k * 45.0
        long = 19.0 if k % 2 == 0 else 12.0
        A.prism([(-2.0, 0.0), (2.0, 0.0), (0.0, long)], 0.35, (0, 0, 0), K['brass'] if k % 2 == 0 else K['limestone'], (0, 0, a - 90.0), z0=0.85)
    A.cyl(3.0, 0.4, (0, 0, 0.85), K['timber'], verts=24)
    A.cyl(1.2, 0.5, (0, 0, 1.25), K['brass'], verts=16)
    for k in range(72):
        x, y, _ = polar(37.8, k * 5.0)
        A.box((1.8 if k % 6 == 0 else 0.9, 0.22, 0.12), (x, y, 0.86), K['timber'], (0, 0, k * 5.0))
    A.to_scene()
    ob = finalize('wizard_floor_medallion', 30)
    for v in ob.data.vertices:                                                               # a flat inlay: 1 stud thick in total
        v.co.z *= 0.57
    ob.data.update()
    return ob


# ------------------------------------------------------------------ WT05 circular map table
OBJ = r"C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5\wizard_map_relief.obj"
PNG = r"C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5\wizard_map_color.png"
_MAP = {}


def _load_map():
    """Read the relief OBJ and the colour map; cluster the map colours into 8 palette keys; label every face."""
    if _MAP:
        return _MAP
    V, Fc = [], []
    for line in open(OBJ):
        if line.startswith('v '):
            V.append(tuple(float(x) for x in line.split()[1:4]))
        elif line.startswith('f '):
            Fc.append(tuple(int(p.split('/')[0]) - 1 for p in line.split()[1:4]))
    img = bpy.data.images.load(PNG, check_existing=False)
    img.colorspace_settings.name = 'Non-Color'
    img.scale(256, 256)
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    px = px.reshape(h, w, 4)[:, :, :3]
    bpy.data.images.remove(img)
    pts = px.reshape(-1, 3)
    lum = pts @ np.array([0.3, 0.59, 0.11])
    cent = pts[np.argsort(lum)[(np.linspace(0.03, 0.97, 8) * (len(pts) - 1)).astype(int)]].copy()
    for _ in range(14):
        lab = ((pts[:, None, :] - cent[None, :, :]) ** 2).sum(-1).argmin(1)
        for c in range(8):
            m = lab == c
            if m.any():
                cent[c] = pts[m].mean(0)
    lab_img = ((pts[:, None, :] - cent[None, :, :]) ** 2).sum(-1).argmin(1).reshape(h, w)
    order = np.argsort(cent @ np.array([0.3, 0.59, 0.11]))
    keys = []
    for rank, c in enumerate(order):
        key = f'vb_map{rank}'
        rgb = tuple(int(max(0, min(255, round(float(v) * 255)))) for v in cent[c])
        kitlib.PAL[key] = (rgb, 'Concrete', 0.0, 0.9, 0)
        keys.append((c, key))
    remap = {c: key for c, key in keys}
    _MAP.update(V=V, F=Fc, lab=lab_img, remap=remap, w=w, h=h, keys=[k for _, k in keys])
    return _MAP


def map_table():
    """WT05_01 - the circular island map: coloured relief (from the planned terrain), granite pedestal and table, brass compass ring,
    outer scale ring (own palette key = own MeshPart) and tiny landmark tokens. About 13 studs tall, 47 across."""
    reset()
    M = _load_map()
    V, Fc, lab, remap, w, h = M['V'], M['F'], M['lab'], M['remap'], M['w'], M['h']
    A = Acc()
    DIAM, SC = 44.0, 40.0 / 44.0
    zmin = min(v[2] for v in V)
    Z0, ZS = 6.4, 0.7
    tz = lambda zz: Z0 + (zz - zmin) * ZS
    for a_, b_, c_ in Fc:
        pa, pb, pc = V[a_], V[b_], V[c_]
        cx, cy = (pa[0] + pb[0] + pc[0]) / 3.0, (pa[1] + pb[1] + pc[1]) / 3.0
        row = int(max(0, min(h - 1, (cy / DIAM + 0.5) * (h - 1))))
        colm = int(max(0, min(w - 1, (cx / DIAM + 0.5) * (w - 1))))
        key = remap[int(lab[row, colm])]
        bm = A._bm(key)
        bm.faces.new([bm.verts.new((p[0] * SC, p[1] * SC, tz(p[2]))) for p in (pa, pb, pc)])
    A.cyl(18.0, 1.0, (0, 0, 0), K['granite'], verts=32)
    A.cyl(13.5, 3.4, (0, 0, 1.0), K['granite'], verts=32, r2=11.5)
    for k in range(12):
        x, y, _ = polar(13.0, k * 30.0 + 15.0)
        A.box((1.6, 2.4, 3.4), (x, y, 2.9), K['limestone'], (0, 0, k * 30.0 + 15.0))
    A.cyl(23.0, 1.8, (0, 0, 4.6), K['limestone'], verts=48)
    A.sweep([(22.6, 4.6), (23.6, 4.6), (23.6, 6.4), (22.6, 6.4)], 0, 360, 48, K['brass'])
    A.sweep([(20.6, 6.3), (21.9, 6.3), (21.9, 6.9), (20.6, 6.9)], 0, 360, 48, K['brass'])
    A.sweep([(21.9, 6.4), (23.0, 6.4), (23.0, 6.9), (21.9, 6.9)], 0, 360, 72, 'vb_ring')
    for k in range(72):
        x, y, _ = polar(22.45, k * 5.0)
        A.box((0.9 if k % 6 else 1.4, 0.18, 0.12), (x, y, 6.96), K['timber'], (0, 0, k * 5.0))
    for k in range(4):
        x, y, _ = polar(22.0, k * 90.0)
        A.prism([(-0.7, 0), (0.7, 0), (0, 1.8)], 0.3, (x, y, 0), K['brass'], (0, 0, k * 90.0 - 90.0), z0=6.9)
    for k in range(24):
        x, y, _ = polar(23.2, k * 15.0)
        A.box((0.35, 0.35, 1.0), (x, y, 6.9), K['brass'])

    def disc(wx, wz):
        return ((wx + 3300.0) / 6600.0 - 0.5) * DIAM, -((wz + 3525.0) / 6600.0 - 0.5) * DIAM

    def ground(x, y):
        i = int(round(max(0, min(100, (x / DIAM + 0.5) * 100))))
        j = int(round(max(0, min(100, (-y / DIAM + 0.5) * 100))))
        return tz(V[j * 101 + i][2])
    marks = {'tower': (1380, -1320), 'capital': (0, -1585), 'tree': (-1700, -540), 'fortress': (1632, -1608),
             'skull': (2280, -1008), 'temple': (1660, 1130), 'town1': (0, 0), 'crater': (1368, -312)}
    for name, (wx, wz) in marks.items():
        x, y = disc(wx, wz)
        x, y = x * SC, y * SC
        z = ground(x / SC, y / SC)
        if name == 'tower':
            A.cyl(0.5, 2.2, (x, y, z), K['white'], verts=10)
            A.cyl(0.75, 0.8, (x, y, z + 2.2), K['copper'], verts=10, r2=0.0)
        elif name == 'capital':
            A.sweep([(1.7, z), (2.0, z), (2.0, z + 0.7), (1.7, z + 0.7)], 0, 360, 16, K['limestone'], loc=(x, y, 0))
            A.box((1.0, 1.0, 1.4), (x, y + 0.6, z + 0.7), K['granite'])
            A.cyl(0.6, 1.0, (x, y + 0.6, z + 1.4), K['copper'], verts=8, r2=0.0)
        elif name == 'tree':
            A.cyl(0.22, 1.1, (x, y, z), K['timber'], verts=8)
            A.ball(0.85, (x, y, z + 1.5), K['copper'], segs=8, rings=5)
        elif name == 'fortress':
            A.box((1.6, 1.0, 0.8), (x, y, z + 0.4), K['granite'])
            A.box((0.9, 0.8, 1.4), (x, y, z + 1.1), K['limestone'])
            A.cyl(0.45, 0.8, (x, y, z + 1.8), K['indigo'], verts=8, r2=0.0)
        elif name == 'skull':
            A.ball(0.55, (x, y, z + 0.5), K['white'], segs=8, rings=5)
        elif name == 'temple':
            for k in range(6):
                px, py, _ = polar(0.9, k * 60.0)
                A.cyl(0.14, 1.0, (x + px, y + py, z), K['limestone'], verts=6)
            A.sweep([(0.3, z + 1.0), (1.2, z + 1.0), (1.2, z + 1.2), (0.3, z + 1.2)], 0, 360, 12, K['ochre'], loc=(x, y, 0))
        elif name == 'town1':
            A.cyl(0.9, 0.3, (x, y, z), K['limestone'], verts=12)
            A.box((0.5, 0.5, 0.7), (x, y, z + 0.6), K['ochre'])
        else:
            A.cyl(0.8, 0.4, (x, y, z), K['granite'], verts=10, r2=0.4)
    A.to_scene(keep_normals=set(M['keys']))
    return finalize('wizard_round_map_table', 30)


# ------------------------------------------------------------------ books and shelves
def _fill_books(A, rnd, place, length, z0, hmax=3.3, dep=(2.6, 3.6), keys=BOOK, gap_p=0.04):
    """Fill a shelf run with books. place(s, depth) -> (x, y, yaw) is the centre of a book at distance s along the run."""
    s = 0.0
    while s < length - 0.4:
        if rnd.random() < gap_p:
            s += rnd.uniform(0.8, 2.2)
            continue
        if rnd.random() < 0.05 and s + 2.6 < length:                                         # a small flat stack
            for q in range(3):
                x, y, yaw = place(s + 1.2, 3.0)
                A.box((3.0, 2.4, 0.6), (x, y, z0 + 0.3 + q * 0.62), rnd.choice(keys), (0, 0, yaw + rnd.uniform(-8, 8)))
            s += 2.6
            continue
        wb = min(rnd.uniform(0.45, 1.25), length - s)
        hb = rnd.uniform(2.3, hmax)
        db = rnd.uniform(*dep)
        x, y, yaw = place(s + wb / 2.0, db)
        A.box((db, wb, hb), (x, y, z0 + hb / 2.0), rnd.choice(keys), (0, 0, yaw))
        s += wb + 0.03


def _bay(R, chord, variant, seed):
    """Curved full-height bay hugging a round wall of radius R. Local frame: wall at y=0 (centre of bay), tower axis at (0,-R), front -Y."""
    reset()
    A = Acc()
    rnd = random.Random(seed)
    half = math.degrees(chord / 2.0 / R)
    a0, a1 = 90.0 - half, 90.0 + half
    depth, H = 3.4, 28.0
    loc = (0, -R, 0)
    P = lambda r, ang, z: (r * math.cos(math.radians(ang)), -R + r * math.sin(math.radians(ang)), z)
    n = max(4, int((a1 - a0) / 4.0))
    A.sweep([(R - 0.7, 0), (R, 0), (R, H), (R - 0.7, H)], a0, a1, n, K['timber'], loc=loc)
    A.sweep([(R - depth - 0.3, 0), (R + 0.2, 0), (R + 0.2, 1.3), (R - depth - 0.3, 1.3)], a0, a1, n, K['granite'], loc=loc)
    A.sweep([(R - depth - 0.7, H - 1.2), (R + 0.2, H - 1.2), (R + 0.2, H), (R - depth - 0.7, H)], a0, a1, n, K['limestone'], loc=loc)
    A.sweep([(R - depth - 1.1, H - 0.3), (R - depth - 0.4, H - 0.3), (R - depth - 0.4, H + 0.0), (R - depth - 1.1, H + 0.0)], a0, a1, n, K['ochre'], loc=loc)
    zs = [1.3 + k * 3.75 for k in range(7)]
    for z in zs:
        A.sweep([(R - depth, z), (R - 0.7, z), (R - 0.7, z + 0.5), (R - depth, z + 0.5)], a0, a1, n, K['ochre'], loc=loc)
    for ang in (a0, a1):                                                                     # carved end panels
        x, y, _ = P(R - depth / 2.0, ang, H / 2.0)
        A.box((depth, 0.8, H), (x, y, H / 2.0), K['timber'], (0, 0, ang))
        x, y, _ = P(R - depth - 0.1, ang, 0)
        A.box((0.4, 1.0, H - 3.0), (x, y, H / 2.0), K['ochre'], (0, 0, ang))
    length = math.radians(a1 - a0 - 2.4) * (R - 2.2)

    def place(s, db):
        return (*P(R - 0.9 - db / 2.0, a0 + 1.2 + math.degrees(s / (R - 2.2)), 0)[:2], a0 + 1.2 + math.degrees(s / (R - 2.2)))
    for k, z in enumerate(zs[:-1]):
        z0 = z + 0.5
        if variant == 1 and k < 3:                                                           # scroll racks: bundles of rolled parchment
            for q in range(int(length / 1.15)):
                ang = a0 + 1.4 + math.degrees((q * 1.15 + 0.6) / (R - 2.2))
                x, y, _ = P(R - 2.4, ang, z0)
                A.cyl(0.42, 3.0, (x, y, z0 + 0.1), K['parchment'], verts=8, rot=(0, 0, 0))
                A.cyl(0.46, 0.25, (x, y, z0 + 0.9), K['brass'], verts=8)
        elif variant == 1 and k >= 4:                                                        # glass-fronted cabinet: brass frame over the books
            _fill_books(A, rnd, place, length, z0, 3.2, (2.6, 3.4), BOOK, 0.08)
            for q in range(0, 7):
                ang = a0 + 1.2 + (a1 - a0 - 2.4) * q / 6.0
                x, y, _ = P(R - depth - 0.15, ang, z0 + 1.6)
                A.box((0.2, 0.28, 3.3), (x, y, z0 + 1.6), K['brass'], (0, 0, ang))
        else:
            _fill_books(A, rnd, place, length, z0, 3.3, (2.7, 3.7), BOOK, 0.05 if variant == 0 else 0.1)
    if variant == 0:                                                                         # rolling-ladder rail and ladder
        pts = [P(R - depth - 0.35, a0 + (a1 - a0) * t / 12.0, 25.2) for t in range(13)]
        for p0, p1 in zip(pts, pts[1:]):
            A.beam(p0, p1, 0.28, 0.28, K['brass'])
        la = a0 + (a1 - a0) * 0.35
        x1, y1, _ = P(R - depth - 0.6, la, 25.0)
        x2, y2, _ = P(R - depth - 3.2, la, 0.4)
        for off in (-0.9, 0.9):
            dx, dy = -math.sin(math.radians(la)) * off, math.cos(math.radians(la)) * off
            A.beam((x1 + dx, y1 + dy, 25.0), (x2 + dx, y2 + dy, 0.4), 0.26, 0.26, K['timber'])
        for q in range(1, 9):
            t = q / 9.0
            A.beam((x1 + (x2 - x1) * t - 0.9 * -math.sin(math.radians(la)), y1 + (y2 - y1) * t - 0.9 * math.cos(math.radians(la)), 25.0 - 24.6 * t),
                   (x1 + (x2 - x1) * t + 0.9 * -math.sin(math.radians(la)), y1 + (y2 - y1) * t + 0.9 * math.cos(math.radians(la)), 25.0 - 24.6 * t), 0.24, 0.24, K['ochre'])
    if variant == 2:                                                                         # fold-down reading ledge with a book and lantern hooks
        x, y, _ = P(R - depth - 1.2, 90.0, 12.0)
        A.box((chord * 0.5, 2.4, 0.4), (x, y, 12.0), K['timber'])
        A.box((2.2, 1.6, 0.3), (x, y, 12.3), K['bk_red'] if 'bk_red' in K else BOOK[0])
        for sg in (-1, 1):
            xx, yy, _ = P(R - depth - 0.4, 90.0 + sg * half * 0.8, 24.0)
            A.beam((xx, yy, 24.0), (xx, yy - 1.2, 24.0), 0.2, 0.2, K['brass'])
            A.cyl(0.35, 0.5, (xx, yy - 1.2, 23.4), K['brass'], verts=8)
    A.to_scene()
    return finalize('wizard_bookshelf_curved', 25)


def bay_1():
    return _bay(38.0, 24.0, 0, 1)


def bay_2():
    return _bay(30.0, 22.0, 1, 2)


def bay_3():
    return _bay(22.0, 20.0, 2, 3)


def _shelf(width, H, depth, double, seed, ladder=False):
    reset()
    A = Acc()
    rnd = random.Random(seed)
    A.box((width, depth, 1.3), (0, 0, 0.65), K['granite'])
    A.box((width, depth + 0.4, 1.0), (0, 0, H - 0.5), K['limestone'])
    A.box((width, 0.7, H), (0, 0, H / 2.0), K['timber'])                                    # centre back / spine
    for sg in (-1, 1):
        A.box((0.8, depth, H), (sg * (width / 2.0 - 0.4), 0, H / 2.0), K['timber'])
        A.box((0.5, depth + 0.3, H - 2.5), (sg * (width / 2.0 + 0.1), 0, H / 2.0), K['ochre'])
    zs = [1.3 + k * 3.7 for k in range(6)]
    sides = (-1, 1) if double else (-1,)
    for sd in sides:
        yoff = sd * (depth / 4.0 + 0.2) if double else -0.3
        for z in zs:
            A.box((width - 1.6, depth / 2.0 + (0.2 if double else depth / 2.0), 0.5), (0, sd * depth / 4.0 if double else 0.0, z + 0.25), K['ochre'])
        length = width - 2.0
        for z in zs[:-1]:
            def place(s, db, sd=sd):
                return (-length / 2.0 + s + 0.0 - (0.0), sd * (depth / 2.0 - 0.9 - db / 2.0) if not double else sd * (depth / 2.0 - 0.3 - db / 2.0), 90.0)
            _fill_books(A, rnd, place, length, z + 0.5, 3.2, (2.0, 2.0 if double else 3.2), BOOK, 0.06)
    if ladder:
        for off in (-0.9, 0.9):
            A.beam((off - 3.0, -depth / 2.0 - 1.0, 1.0), (off - 3.0 + 0.0, -depth / 2.0 - 0.3, H - 3.0), 0.26, 0.26, K['timber'])
        for q in range(1, 9):
            t = q / 9.0
            A.beam((-3.9, -depth / 2.0 - 1.0 + 0.7 * t, 1.0 + (H - 4.0) * t), (-2.1, -depth / 2.0 - 1.0 + 0.7 * t, 1.0 + (H - 4.0) * t), 0.24, 0.24, K['ochre'])
        A.beam((-width / 2.0 + 0.5, -depth / 2.0 - 0.3, H - 2.6), (width / 2.0 - 0.5, -depth / 2.0 - 0.3, H - 2.6), 0.28, 0.28, K['brass'])
    A.to_scene()
    return finalize('wizard_bookshelf_straight', 25)


def shelf_1():
    return _shelf(14.0, 26.0, 4.6, False, 5)


def shelf_2():
    return _shelf(14.0, 26.0, 4.2, True, 6, True)


# ------------------------------------------------------------------ WT07 lab sets
def _jar(A, x, y, z, r=0.55, h=1.3, key=None, cork=True):
    A.cyl(r, h, (x, y, z), key or K['parchment'], verts=10)
    if cork:
        A.cyl(r * 0.8, 0.28, (x, y, z + h), K['timber'], verts=8)


def lab_bench():
    """WT07_01 - alchemy station 18 wide, 12 deep, 14 tall: long bench with glassware and a copper still, back shelf unit, hanging pots, stool."""
    reset()
    A = Acc()
    A.box((17.0, 6.4, 0.7), (0, 0, 3.65), K['timber'])
    for sx in (-7.8, 7.8):
        for sy in (-2.6, 2.6):
            A.box((0.9, 0.9, 3.3), (sx, sy, 1.65), K['timber'])
    A.box((16.4, 5.6, 0.35), (0, 0, 1.1), K['ochre'])
    for sx in (-8.4, 8.4):                                                                   # back shelf unit
        A.box((0.8, 2.2, 13.6), (sx, 4.8, 6.8), K['timber'])
    for z in (4.6, 7.8, 11.0, 13.3):
        A.box((17.6, 2.2, 0.45), (0, 4.8, z), K['ochre'])
    A.box((17.6, 0.4, 13.6), (0, 5.8, 6.8), K['timber'])
    rnd = random.Random(41)
    for z in (4.85, 8.05, 11.25):
        for k in range(10):
            _jar(A, -7.6 + k * 1.7, 4.8 + rnd.uniform(-0.4, 0.4), z, rnd.uniform(0.45, 0.65), rnd.uniform(1.0, 1.9), rnd.choice([K['glass'], K['parchment'], K['white'], K['glass']]))
    for k, x in enumerate((-6.0, -3.2, 0.6, 5.0)):                                           # flasks
        A.ball(0.95, (x, -1.0, 5.0), K['glass'], segs=10, rings=6)
        A.cyl(0.3, 1.5, (x, -1.0, 5.8), K['glass'], verts=8)
    A.cyl(1.2, 2.0, (-6.2, 1.4, 4.0), K['copper'], verts=12, r2=0.25)                        # copper still with a coil pipe
    A.cyl(0.22, 3.2, (-4.8, 1.4, 5.6), K['copper'], verts=6, rot=(0, 70, 0))
    A.cyl(0.6, 1.5, (2.2, 1.2, 4.0), K['brass'], verts=10)                                   # mortar
    A.beam((3.0, -0.6, 4.2), (5.4, 0.2, 4.2), 0.3, 0.3, K['brass'])                          # balance beam
    A.cyl(0.25, 2.2, (4.2, -0.2, 4.0), K['brass'], verts=6)
    A.box((6.0, 2.4, 0.14), (-1.0, -1.8, 4.1), K['parchment'])                               # recipe sheet
    A.beam((-8.4, 4.8, 13.9), (8.4, 4.8, 13.9), 0.3, 0.3, K['brass'])
    for k in range(5):                                                                       # hanging copper pots
        A.cyl(0.8, 1.1, (-6.4 + k * 3.2, 4.8, 12.4), K['copper'], verts=10, r2=0.65)
        A.box((0.08, 0.08, 0.6), (-6.4 + k * 3.2, 4.8, 13.6), K['timber'])
    A.cyl(1.5, 0.5, (4.0, -5.4, 2.4), K['ochre'], verts=12)                                  # stool
    for k in range(3):
        x, y, _ = polar(1.0, k * 120.0)
        A.box((0.4, 0.4, 2.4), (4.0 + x, -5.4 + y, 1.2), K['timber'])
    A.to_scene()
    return finalize('wizard_lab_bench', 25)


def lab_herbs():
    """WT07_02 - herb rack with jars and hanging bundles plus a front work table (18 wide, 12 deep, 13 tall)."""
    reset()
    A = Acc()
    for sx in (-8.0, 8.0):
        A.box((0.9, 4.4, 13.0), (sx, 3.6, 6.5), K['timber'])
    for z in (0.5, 3.6, 6.7, 9.8):
        A.box((16.9, 4.4, 0.5), (0, 3.6, z + 0.25), K['ochre'])
    A.box((17.0, 0.5, 13.0), (0, 5.9, 6.5), K['timber'])
    rnd = random.Random(21)
    for z in (0.75, 3.85, 6.95):
        for k in range(10):
            _jar(A, -7.2 + k * 1.6, 3.6 + rnd.uniform(-0.8, 0.8), z, rnd.uniform(0.45, 0.6), rnd.uniform(0.9, 1.6), rnd.choice([K['glass'], K['parchment'], K['white']]))
    A.beam((-8.0, 3.6, 12.6), (8.0, 3.6, 12.6), 0.3, 0.3, K['timber'])
    for k in range(8):
        x = -7.0 + k * 2.0
        A.cyl(0.5, 2.2, (x, 3.6, 10.2), K['copper'] if k % 2 else K['ochre'], verts=8, r2=0.1, rot=(180, 0, 0))
        A.box((0.08, 0.08, 0.9), (x, 3.6, 12.4), K['timber'])
    A.box((12.0, 4.2, 0.6), (0, -3.4, 3.4), K['timber'])                                     # work table
    for sx in (-5.4, 5.4):
        for sy in (-4.8, -2.0):
            A.box((0.7, 0.7, 3.1), (sx, sy, 1.55), K['timber'])
    A.cyl(0.8, 1.2, (-3.0, -3.2, 3.7), K['brass'], verts=10)
    for k in range(4):
        A.cyl(0.4, 2.4, (1.0 + k * 0.7, -3.6, 3.7), K['copper'] if k % 2 else K['ochre'], verts=6, rot=(80, 0, 10.0 * k))
    A.cyl(1.5, 1.4, (4.2, -3.2, 3.7), K['ochre'], verts=12, r2=1.2)
    A.to_scene()
    return finalize('wizard_lab_herbs', 25)


def lab_specimens():
    """WT07_03 - specimen shelf with jars, plus a display table with a glass bell jar (17 wide, 12 deep, 13 tall)."""
    reset()
    A = Acc()
    A.box((16.0, 4.6, 1.0), (0, 3.6, 0.5), K['granite'])
    A.box((16.0, 0.7, 12.0), (0, 5.7, 7.0), K['timber'])
    for sx in (-7.6, 7.6):
        A.box((0.8, 4.6, 12.0), (sx, 3.6, 7.0), K['timber'])
    for z in (1.0, 4.4, 7.8, 11.2):
        A.box((15.0, 4.4, 0.5), (0, 3.6, z + 0.25), K['ochre'])
    for z in (1.5, 4.9, 8.3):
        for k in range(5):
            x = -6.0 + k * 3.0
            A.cyl(0.9, 2.2, (x, 3.6, z), K['glass'], verts=10)
            A.cyl(0.75, 0.3, (x, 3.6, z + 2.2), K['brass'], verts=10)
            if k % 3 == 0:
                A.ball(0.55, (x, 3.6, z + 1.1), K['white'], segs=8, rings=5)
            elif k % 3 == 1:
                A.cyl(0.25, 1.4, (x, 3.6, z + 0.4), K['copper'], verts=6)
            else:
                A.ball(0.45, (x, 3.6, z + 0.9), K['bk_red'] if 'bk_red' in K else BOOK[0], segs=8, rings=5)
    A.cyl(3.6, 0.8, (0, -3.2, 2.2), K['granite'], verts=20)                                  # display table
    A.cyl(0.9, 2.2, (0, -3.2, 0), K['timber'], verts=10)
    A.cyl(2.6, 0.3, (0, -3.2, 3.0), K['brass'], verts=20)
    A.ball(2.4, (0, -3.2, 5.2), K['glass'], segs=16, rings=8, scale=(1, 1, 1.15))            # bell jar
    A.ball(0.9, (0, -3.2, 3.8), K['white'], segs=8, rings=5)
    for sx in (-5.8, 5.8):
        A.cyl(0.7, 2.6, (sx, -4.4, 0), K['timber'], verts=8)
        A.ball(1.2, (sx, -4.4, 3.4), K['copper'], segs=8, rings=5)
    A.to_scene()
    return finalize('wizard_lab_specimens', 25)


def lab_orrery():
    reset()
    A = Acc()
    zc = 11.0
    A.cyl(3.6, 0.9, (-3.0, 0, 0), K['granite'], verts=16)
    A.cyl(1.2, 2.2, (-3.0, 0, 0.9), K['timber'], verts=10, r2=0.9)
    A.cyl(0.8, 7.2, (-3.0, 0, 3.0), K['brass'], verts=10)
    A.ball(1.1, (-3.0, 0, zc), K['brass'], segs=10, rings=6)
    for k, (R, sz, key) in enumerate(((2.0, 0.35, K['copper']), (3.3, 0.45, K['white']), (4.6, 0.6, K['ochre']), (5.8, 0.4, K['indigo']))):
        A.sweep([(R - 0.08, -0.08), (R + 0.08, -0.08), (R + 0.08, 0.08), (R - 0.08, 0.08)], 0, 360, 32, K['brass'], loc=(-3.0, 0, zc))
        x, y, _ = polar(R, 40.0 + k * 85.0)
        A.ball(sz, (-3.0 + x, y, zc), key, segs=8, rings=5)
        A.beam((-3.0, 0, zc), (-3.0 + x, y, zc), 0.1, 0.1, K['brass'])
    for k in range(3):
        x, y, _ = polar(2.2, k * 120.0 + 30.0)
        A.beam((6.5 + x, y, 0.0), (6.5, 0, 9.0), 0.4, 0.4, K['timber'])
    A.cyl(0.35, 2.4, (6.5, 0, 9.0), K['brass'], verts=8)
    A.sweep([(2.2, -0.14), (3.2, -0.14), (3.2, 0.14), (2.2, 0.14)], 0, 360, 36, K['brass'], loc=(6.5, 0, 12.2), rot=(80, 0, 0))
    A.sweep([(0.3, -0.1), (2.2, -0.1), (2.2, 0.1), (0.3, 0.1)], 0, 360, 36, K['copper'], loc=(6.5, 0, 12.2), rot=(80, 0, 0))
    A.box((0.3, 0.2, 3.6), (6.5, 0.1, 12.2), K['brass'], (0, 0, 0))
    A.to_scene()
    return finalize('wizard_lab_orrery', 30)


# ------------------------------------------------------------------ WT08 study sets
def study_desk():
    """WT08_01 - archmage study corner 17 wide, 13 deep, 12 tall: desk with open books and quill, chair, rug, bookcase, floor candlestick."""
    reset()
    A = Acc()
    A.box((16.0, 11.6, 0.12), (0, -0.2, 0.06), K['indigo'])                                  # rug with ochre border
    A.box((14.6, 10.2, 0.16), (0, -0.2, 0.1), K['ochre'])
    A.box((13.4, 9.0, 0.2), (0, -0.2, 0.12), K['indigo'])
    A.box((14.0, 6.0, 0.8), (0, 0, 4.2), K['timber'])
    for sx in (-6.3, 6.3):
        A.box((1.0, 5.0, 3.8), (sx, 0, 1.9), K['timber'])
        A.box((1.2, 5.4, 0.6), (sx, 0, 0.3), K['granite'])
    A.box((13.0, 0.4, 1.6), (0, 2.4, 5.0), K['ochre'])
    A.box((3.6, 2.6, 0.18), (-3.0, 0.2, 4.7), K['parchment'])
    A.box((3.6, 2.6, 0.18), (0.8, 0.2, 4.7), K['parchment'])
    A.box((0.2, 2.6, 0.3), (-1.1, 0.2, 4.75), BOOK[0])
    A.cyl(0.35, 1.0, (4.5, -0.8, 4.6), K['brass'], verts=8)
    A.beam((5.2, 0.4, 4.7), (6.2, 1.4, 6.4), 0.1, 0.1, K['white'])
    for k in range(4):
        A.box((2.4, 1.8, 0.45), (-5.2, 1.5, 4.8 + k * 0.46), BOOK[k % 5], (0, 0, k * 11.0))
    A.cyl(0.4, 0.7, (2.8, 1.8, 4.6), K['wax'], verts=8)
    A.box((4.0, 3.6, 0.6), (0, -4.2, 2.6), K['ochre'])                                       # chair
    A.box((4.0, 0.6, 3.6), (0, -5.8, 4.4), K['ochre'])
    for sx in (-1.6, 1.6):
        for sy in (-3.0, -5.4):
            A.box((0.5, 0.5, 2.3), (sx, sy, 1.15), K['timber'])
    for sx in (-8.4, 8.4):                                                                   # bookcase behind the desk
        A.box((0.7, 2.4, 12.0), (sx, 5.6, 6.0), K['timber'])
    for z in (0.3, 3.4, 6.5, 9.6, 11.8):
        A.box((17.0, 2.4, 0.5), (0, 5.6, z), K['ochre'])
    A.box((17.0, 0.4, 12.0), (0, 6.6, 6.0), K['timber'])
    rnd = random.Random(51)
    for z in (0.55, 3.65, 6.75, 9.85):
        _fill_books(A, rnd, lambda s, db: (-8.0 + s, 5.6, 90.0), 16.0, z, 2.6, (1.6, 2.0), BOOK, 0.07)
    A.cyl(0.9, 0.5, (-7.0, -3.4, 0), K['granite'], verts=10)                                 # floor candlestick (no glow)
    A.cyl(0.18, 6.4, (-7.0, -3.4, 0.5), K['brass'], verts=8)
    A.cyl(0.7, 0.4, (-7.0, -3.4, 6.9), K['brass'], verts=10)
    A.cyl(0.32, 1.2, (-7.0, -3.4, 7.3), K['wax'], verts=8)
    A.to_scene()
    return finalize('wizard_study_desk', 25)


def study_bed():
    reset()
    A = Acc()
    for sx in (-8.0, 8.0):
        for sy in (-6.0, 6.0):
            A.box((1.0, 1.0, 11.0), (sx, sy, 5.5), K['timber'])
            A.box((1.4, 1.4, 0.5), (sx, sy, 11.2), K['brass'])
    A.box((16.0, 12.6, 1.0), (0, 0, 2.4), K['timber'])
    A.box((15.0, 11.8, 1.3), (0, 0, 3.4), K['white'])
    A.box((15.2, 7.6, 0.5), (0.0, -2.2, 4.1), K['indigo'])
    for k in range(2):
        A.box((4.0, 2.4, 0.9), (-4.0 + k * 8.0, 4.4, 4.3), K['parchment'])
    A.box((16.6, 0.8, 8.0), (0, 6.6, 7.0), K['ochre'])
    for sg in (-1, 1):
        for k in range(5):
            A.box((1.1, 0.35, 8.4 - 0.15 * k), (sg * (6.5 - k * 0.8), -6.2 + (k % 2) * 0.5, 6.4), K['indigo'])
    A.beam((-8.0, -6.0, 10.8), (8.0, -6.0, 10.8), 0.3, 0.3, K['brass'])
    A.beam((-8.0, 6.0, 10.8), (8.0, 6.0, 10.8), 0.3, 0.3, K['brass'])
    A.box((16.0, 12.6, 0.5), (0, 0, 11.0), K['indigo'])
    A.box((14.0, 0.4, 0.4), (0, -6.4, 3.5), K['brass'])
    A.to_scene()
    return finalize('wizard_study_bed', 25)


def study_globe():
    reset()
    A = Acc()
    A.cyl(3.2, 0.7, (-4.0, 0, 0), K['granite'], verts=16)
    A.cyl(0.6, 4.2, (-4.0, 0, 0.7), K['timber'], verts=8)
    A.sweep([(3.5, -0.18), (3.9, -0.18), (3.9, 0.18), (3.5, 0.18)], 0, 360, 36, K['brass'], loc=(-4.0, 0, 7.3), rot=(23.5, 0, 0))
    A.ball(3.3, (-4.0, 0, 7.3), K['indigo'], segs=18, rings=12)
    for k in range(7):
        a, b = 40.0 * k, 25.0 + 17.0 * (k % 4)
        r = 3.3 * 0.99
        A.ball(1.0, (-4.0 + r * math.cos(math.radians(b)) * math.cos(math.radians(a)), r * math.cos(math.radians(b)) * math.sin(math.radians(a)), 7.3 + r * math.sin(math.radians(b))),
               K['copper'] if k % 2 else K['ochre'], segs=8, rings=5, scale=(1.0, 1.0, 0.35))
    A.cyl(0.18, 8.4, (-4.0, 0, 3.1), K['brass'], verts=6, rot=(23.5, 0, 0))
    for k in range(3):
        x, y, _ = polar(1.9, k * 120.0 + 90.0)
        A.beam((6.0 + x, y, 0.0), (6.0, 0, 9.5), 0.4, 0.4, K['timber'])
    A.box((6.0, 0.3, 4.4), (6.0, -0.6, 8.5), K['parchment'], (-12, 0, 0))
    A.box((6.6, 0.4, 0.5), (6.0, -0.5, 6.3), K['timber'])
    for k in range(6):
        A.box((0.4, 0.05, 0.4), (4.0 + k * 0.9, -0.82, 8.0 + (k % 3) * 0.7), K['indigo'], (0, 0, 20.0 * k))
    A.box((8.0, 4.4, 3.6), (-3.0, -5.6, 1.8), K['timber'])                                   # sea chest in front
    A.box((8.2, 4.6, 0.5), (-3.0, -5.6, 3.8), K['ochre'])
    for sx in (-5.6, -0.4):
        A.box((0.5, 4.7, 3.7), (sx, -5.6, 1.85), K['brass'])
    A.box((2.6, 1.8, 0.35), (-3.0, -5.6, 4.15), K['parchment'])
    for k in range(3):                                                                       # rolled charts in a rack behind
        A.cyl(0.5, 5.0, (1.2 + k * 1.3, 6.2, 0.6), K['parchment'], verts=8, rot=(0, 15, 0))
    A.box((5.4, 1.6, 0.5), (2.8, 6.2, 0.3), K['timber'])
    A.to_scene()
    return finalize('wizard_study_globe', 30)


# ------------------------------------------------------------------ WT09 chandeliers, WT10 telescope
def _chandelier(rings, seed):
    reset()
    A = Acc()
    top = 7.6
    A.sweep([(0.0 + 0.3, top), (0.8, top), (0.8, top + 0.4), (0.3, top + 0.4)], 0, 360, 12, K['brass'])
    A.ball(0.9, (0, 0, top - 0.2), K['brass'], segs=8, rings=5)
    for R, ncan, z in rings:
        A.sweep([(R - 0.28, z - 0.28), (R + 0.28, z - 0.28), (R + 0.28, z + 0.28), (R - 0.28, z + 0.28)], 0, 360, 36, K['brass'])
        for k in range(ncan):
            a = 360.0 * k / ncan
            x, y, _ = polar(R, a)
            A.cyl(0.42, 0.5, (x, y, z + 0.28), K['brass'], verts=8)
            A.cyl(0.26, 1.5, (x, y, z + 0.78), K['wax'], verts=8)
            A.cyl(0.1, 0.35, (x, y, z + 2.28), K['timber'], verts=6)                         # wick only: no flame, no glow
            A.box((0.08, 0.08, 0.5), (x, y, z - 0.28 - 0.25), K['brass'])
        for k in range(3):
            a = 120.0 * k + 15.0
            x, y, _ = polar(R, a)
            A.beam((x, y, z), (0, 0, top - 0.2), 0.12, 0.12, K['brass'])
        for k in range(6):
            x, y, _ = polar(R * 0.98, k * 60.0 + 30.0)
            A.ball(0.32, (x, y, z - 0.9), K['glass'], segs=6, rings=4)
    A.to_scene()
    return finalize('wizard_chandelier', 30)


def chandelier_1():
    return _chandelier([(9.5, 12, 2.4)], 1)


def chandelier_2():
    return _chandelier([(9.6, 14, 1.6), (5.2, 8, 3.8)], 2)


def telescope():
    """WT10_01 - brass observatory telescope: stepped round pedestal, yoke, a long tube raised steeply, finder scope, eyepiece, counterweight."""
    reset()
    A = Acc()
    A.cyl(6.5, 1.0, (0, 0, 0), K['granite'], verts=24)
    A.cyl(4.8, 1.0, (0, 0, 1.0), K['limestone'], verts=24)
    A.cyl(1.8, 7.0, (0, 0, 2.0), K['brass'], verts=16, r2=1.4)
    for k in range(4):
        x, y, _ = polar(2.6, k * 90.0 + 45.0)
        A.beam((x, y, 2.2), (0, 0, 7.5), 0.5, 0.5, K['copper'])
    A.cyl(2.4, 1.4, (0, 0, 8.6), K['brass'], verts=16)
    for sx in (-1.9, 1.9):
        A.box((0.8, 2.4, 5.5), (sx, 0, 12.0), K['brass'])
    A.cyl(0.6, 4.8, (-2.4, 0, 12.0), K['copper'], verts=8, rot=(0, 90, 0))
    tilt, L = 22.0, 14.0
    d = math.radians(tilt)
    A.cyl(1.55, L, (0, 0, 12.0), K['brass'], verts=18, r2=1.2, rot=(tilt, 0, 0))
    for t in (3.0, 7.0, 11.0):
        A.cyl(1.7 - t * 0.02, 0.5, (0, -math.sin(d) * t, 12.0 + math.cos(d) * t), K['copper'], verts=18, rot=(tilt, 0, 0))
    A.cyl(1.9, 1.2, (0, -math.sin(d) * L, 12.0 + math.cos(d) * L), K['brass'], verts=18, rot=(tilt, 0, 0))
    A.cyl(0.4, 3.2, (0, math.sin(d) * 1.2, 12.0 - math.cos(d) * 1.2), K['copper'], verts=8, rot=(tilt + 180.0, 0, 0))
    A.cyl(0.35, 7.5, (1.6, -math.sin(d) * 3.0, 14.0 + math.cos(d) * 3.0), K['brass'], verts=8, rot=(tilt, 0, 0))
    A.ball(1.3, (0, math.sin(d) * 4.2, 12.0 - math.cos(d) * 4.2), K['copper'], segs=10, rings=6)
    for k in range(8):
        a = k * 45.0
        x, y, _ = polar(5.9, a)
        A.box((0.5, 0.3, 0.12), (x, y, 2.05), K['brass'], (0, 0, a))
    A.to_scene()
    return finalize('wizard_telescope', 30)


BATCHES = {
    'interior_shell': ('v5_wizard', [('WT02_01_wizard_tower_interior', interior_shell)]),
    'map_table': ('v5_wizard', [('WT05_01_wizard_round_map_table', map_table), ('WT06_01_wizard_floor_medallion', floor_medallion)]),
    'shelves': ('v5_wizard', [
        ('WT03_01_wizard_bookshelf_curved_01', bay_1), ('WT03_02_wizard_bookshelf_curved_02', bay_2), ('WT03_03_wizard_bookshelf_curved_03', bay_3),
        ('WT04_01_wizard_bookshelf_straight_01', shelf_1), ('WT04_02_wizard_bookshelf_straight_02', shelf_2)]),
    'furniture': ('v5_wizard', [
        ('WT07_01_wizard_lab_set_01', lab_bench), ('WT07_02_wizard_lab_set_02', lab_herbs), ('WT07_03_wizard_lab_set_03', lab_specimens),
        ('WT07_04_wizard_lab_set_04', lab_orrery), ('WT08_01_wizard_study_set_01', study_desk), ('WT08_02_wizard_study_set_02', study_bed),
        ('WT08_03_wizard_study_set_03', study_globe), ('WT09_01_wizard_chandelier_ring_01', chandelier_1),
        ('WT09_02_wizard_chandelier_ring_02', chandelier_2), ('WT10_01_wizard_observatory_telescope', telescope)]),
}
