"""v5_tower_assembly - assemble the wizard tower from a placement list in a HEADLESS Blender, measure how every furnishing fits the interior,
(optionally) solve a corrected layout, and render plan sections and cutaway views. Writes only to library\\v5_work\\tower_check\\<tag>\\.
  blender -b --factory-startup --python v5_tower_assembly.py -- <mode: plan|solve|fixed> <outdir> <render: 0|1> [res]
plan  = the placements in mapplan\\v5_himalaya.json (groups WizardTower, WizardTowerInterior) exactly as they are
solve = search clear positions for every furnishing (wall bays between the windows, outside the stair), write <outdir>\\..\\placements_fixed.json, then measure it
fixed = measure and render library\\v5_work\\tower_check\\placements_fixed.json
Frame: tower-local Blender (centre = tower axis, front = -Y, z up, studs). Plan x/z (Roblox) -> x = X - 1380, y = -(Z + 1320); the plan's rot is the rotation about Z.
Per piece (all with a clearance): stair = vertices inside the helical stair treads (inflated 1.5), rail = inside the atrium rails, wall = how far its furthest vertex
reaches beyond the inner wall radius of its level, window = covers a window or the front door, floor = base centre not over a floor plate (levels 1 and up),
pair = overlaps a neighbouring bay on the same level.
"""
import sys
import os
import json
import math
import time
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
import numpy as np
import bpy
import bmesh
import kitlib
import v5liverun
from v5kit import TOWER, tower_openings

MODE, OUT, RENDER = argv[0], argv[1], argv[2] == '1'
STAIR_E = -0.3 if MODE == 'plan' else -2.5          # fixed/solve: every furnishing keeps 2.5 studs away from the stair treads (negative = inflate)
RES = int(argv[3]) if len(argv) > 3 else 700
LIB = kitlib.LIB
T_ = r"C:\Users\Nitro\.kiro\crew\workspace\town"
TX, TZ = 1380.0, -1320.0
F = TOWER['floors']
RIN = [d / 2.0 - TOWER['wall'] for d in TOWER['outer_d']]
os.makedirs(OUT, exist_ok=True)
FIXED = os.path.join(OUT, '..', 'placements_fixed.json')
WIN = {i: tower_openings(i) for i in range(8)}
boxes = json.load(open(os.path.join(LIB, 'v5_wizard', 'tower_collision.json')))['boxes']
bpy.ops.wm.read_factory_settings(use_empty=True)


def level_of(z):
    for i in range(7, -1, -1):
        if z >= F[i] - 0.5:
            return i
    return 0


# ---------------------------------------------------------------- models
_base, _loc = {}, {}


def base_obj(mid):
    if mid not in _base:
        with bpy.data.libraries.load(os.path.join(LIB, 'v5_wizard', mid + '.blend'), link=False) as (src, dst):
            dst.objects = list(src.objects)
        _base[mid] = [o for o in dst.objects if o is not None and o.type == 'MESH'][0]
    return _base[mid]


def local_verts(mid):
    if mid not in _loc:
        me = base_obj(mid).data
        a = np.empty(len(me.vertices) * 3)
        me.vertices.foreach_get('co', a)
        _loc[mid] = a.reshape(-1, 3)
    return _loc[mid]


def world(mid, x, y, z, rot, scale=1.0):
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    L = local_verts(mid) * scale
    return np.stack([L[:, 0] * c - L[:, 1] * s + x, L[:, 0] * s + L[:, 1] * c + y, L[:, 2] + z], axis=1)


# ---------------------------------------------------------------- collision sets
def boxset(pred):
    b = [x for x in boxes if pred(x['n'])]
    if not b:
        return None
    return np.array([x['p'] for x in b]), np.array([x['s'] for x in b]), np.cos(np.radians([x['yaw'] for x in b])), np.sin(np.radians([x['yaw'] for x in b]))


TREAD, RAIL = boxset(lambda n: n == 'tread'), boxset(lambda n: n.startswith('atrium_rail'))
FLOORS = {lv: boxset(lambda n, lv=lv: n == f'floor{lv}') for lv in range(1, 8)}


def inside(V, bs, e=0.15):
    if bs is None:
        return 0
    P, S, c, s = bs
    hit = np.zeros(len(V), dtype=bool)
    for k in range(len(P)):
        d = V - P[k]
        lx = d[:, 0] * c[k] + d[:, 1] * s[k]
        ly = -d[:, 0] * s[k] + d[:, 1] * c[k]
        hit |= (np.abs(lx) < S[k, 0] / 2 - e) & (np.abs(ly) < S[k, 1] / 2 - e) & (np.abs(d[:, 2]) < S[k, 2] / 2 - e)
    return int(hit.sum())


def over_floor(x, y, lv):
    bs = FLOORS.get(lv)
    if bs is None:
        return True
    P, S, c, s = bs
    d = np.array([x, y]) - P[:, :2]
    lx = d[:, 0] * c + d[:, 1] * s
    ly = -d[:, 0] * s + d[:, 1] * c
    return bool(((np.abs(lx) < S[:, 0] / 2) & (np.abs(ly) < S[:, 1] / 2)).any())


def measure(mid, x, y, z, rot, scale=1.0, lv=None):
    V = world(mid, x, y, z, rot, scale)
    lv = level_of(z + 0.5) if lv is None else lv
    r = np.hypot(V[:, 0], V[:, 1])
    ang = np.degrees(np.arctan2(V[:, 1], V[:, 0])) % 360
    ca = (math.degrees(math.atan2(y, x)) % 360) if math.hypot(x, y) > 1 else 0.0
    rel = ((ang - ca + 180) % 360) - 180
    zlo, zhi = float(V[:, 2].min()), float(V[:, 2].max())
    wmax = float(r.max()) - RIN[lv]
    ops, wins, tiers = WIN[lv]
    win = False
    for w in wins:
        hw = math.degrees(7.0 / (RIN[lv] + 3.0)) + 0.2
        dw = ((w - ca + 180) % 360) - 180
        if rel.min() - hw < dw < rel.max() + hw and any(not (zhi <= a or zlo >= b) for a, b in tiers) and wmax > -9:
            win = True
    if lv == 0:
        hd = math.degrees(5.5 / (RIN[0] + 3.0)) + 0.2
        dd = ((270.0 - ca + 180) % 360) - 180
        if rel.min() - hd < dd < rel.max() + hd and zlo < 13 and wmax > -9:
            win = True
    return dict(id=mid, lvl=lv, ca=round(ca, 1), r0=round(float(r.min()), 1), r1=round(float(r.max()), 1), wall=round(wmax, 2), zlo=round(zlo, 1), zhi=round(zhi, 1),
                half=round(float((rel.max() - rel.min()) / 2), 1), stair=inside(V, TREAD, STAIR_E), rail=inside(V, RAIL, -0.4), window=win,
                floor=over_floor(x, y, lv) if lv >= 1 and not mid.startswith(('WT09', 'WT10', 'WT11')) else True, x=round(x, 2), y=round(y, 2), z=z, rot=round(rot % 360, 1))


def clear(m, wall_ok=0.45):
    return m['stair'] == 0 and m['rail'] == 0 and not m['window'] and m['floor'] and m['wall'] <= wall_ok


def facing(x, y):
    return math.degrees(math.atan2(-x, y)) % 360          # rotation about Z that turns the model's front (-Y) toward the tower axis


# ---------------------------------------------------------------- the solver
FAILS = {}


def free_segments(lv):
    R = RIN[lv]
    ops, wins, tiers = WIN[lv]
    edges = []
    for w in wins:
        hw = math.degrees(7.0 / (R + 3.0)) + 0.2
        edges.append((w - hw, w + hw))
    if lv == 0:
        hd = math.degrees(5.5 / (R + 3.0)) + 0.2
        edges.append((270.0 - hd, 270.0 + hd))
    edges.sort()
    out = []
    for k in range(len(edges)):
        a = edges[k][1]
        b = edges[(k + 1) % len(edges)][0]
        if b <= a:
            b += 360.0
        out.append((((a + b) / 2.0) % 360.0, b - a))
    return out


def wall_place(mid, lv, ang, z, curved, scale=1.0, tries=(0, 1.5, -1.5, 3, -3, 5, -5, 8, -8, 12, -12)):
    """Put a furnishing against the inner wall of level lv at polar angle ang (deg). The pivot of every model is the bottom centre of its bounding box,
    so the pivot radius is solved until the furthest vertex touches the wall (0.2 short of it); small angle offsets are tried until the place is clear."""
    R = RIN[lv]
    for off in tries:
        a = math.radians(ang + off)
        rad = R - 5.0
        m = None
        for _ in range(4):
            x, y = rad * math.cos(a), rad * math.sin(a)
            m = measure(mid, x, y, z, facing(x, y), scale, lv)
            rad += (R - 0.2) - m['r1']
        if clear(m) and m['wall'] <= 0.1:
            return m
        FAILS[(mid[:4], lv)] = FAILS.get((mid[:4], lv), []) + [(off, 'stair' if m['stair'] else '', 'rail' if m['rail'] else '', 'window' if m['window'] else '', 'floor' if not m['floor'] else '', f"wall{m['wall']}" if m['wall'] > 0.45 else '')]
    return None


def solve():
    placed = []

    def add(m, group='WizardTowerInterior', scale=None, note=None):
        p = dict(model=m['id'], x=m['x'], y=m['y'], z=m['z'], rot=m['rot'], group=group)
        if scale and scale != 1.0:
            p['scale'] = scale
        if note:
            p['note'] = note
        placed.append(p)

    # fixed centre pieces
    for mid, z, x, sc in (('WT05_01_wizard_round_map_table', 0.0, 0.0, 1.0), ('WT06_01_wizard_floor_medallion', 0.3, 0.0, 0.84), ('WT10_01_wizard_observatory_telescope', 232.0, 0.0, 1.0),
                          ('WT09_01_wizard_chandelier_ring_01', 30.0, -14.0, 1.0), ('WT09_02_wizard_chandelier_ring_02', 30.0, 14.0, 1.0), ('WT09_01_wizard_chandelier_ring_01', 222.0, 0.0, 0.8)):
        m = measure(mid, x, 0.0, z, 0.0, sc, level_of(z + 0.5))
        add(m, scale=sc, note='THE CIRCULAR MAP, Map Hall centre' if mid.startswith('WT05') else None)
    bays = ['WT03_01_wizard_bookshelf_curved_01', 'WT03_02_wizard_bookshelf_curved_02', 'WT03_03_wizard_bookshelf_curved_03']
    pref = {0: (0, 1), 1: (0, 1), 2: (1, 0), 3: (2, 1)}        # bay variant per level: the curvature (radius 38, 30, 22) closest to that level's wall
    k = 0
    stats = {}
    for lv, z in ((0, 0.1), (1, 40.0), (2, 72.0), (3, 104.0)):
        n = 0
        for gi, (ang, width) in enumerate(free_segments(lv)):
            order = [pref[lv][(gi + lv) % 2], pref[lv][(gi + lv + 1) % 2]] + [q for q in range(3) if q not in pref[lv]]
            m = None
            for q in order:
                m = wall_place(bays[q], lv, ang, z, True)
                if m:
                    break
            if m:
                add(m)
                n += 1
            k += 1
        stats[lv] = n
    print('SOLVE bays per level', stats)
    # four island shelves on the Map Hall floor, between the map and the wall bays, away from the stair sector (99 to 333 deg)
    for ang in (132.0, 177.0, 222.0, 297.0):
        best = None
        for rad in (31.0, 30.0, 32.0, 29.0):
            a = math.radians(ang)
            x, y = rad * math.cos(a), rad * math.sin(a)
            m = measure('WT04_02_wizard_bookshelf_straight_02', x, y, 0.1, (math.degrees(a) + 90.0) % 360, 1.0, 0)
            if m['stair'] == 0 and m['rail'] == 0:
                best = m
                break
        if best:
            add(best)
    # archive vault (level 3): straight shelves against the wall, one per free segment, level 2 gets two extra
    segs = free_segments(3)
    for ang, width in segs:
        m = wall_place('WT04_01_wizard_bookshelf_straight_01', 3, ang, 104.0, False)
        if m:
            add(m)
    # alchemy lab (level 4): four sets; study (level 5): three sets; star room (level 6): orrery and crystal ball
    for lv, z, mids in ((4, 136.0, ['WT07_01_wizard_lab_set_01', 'WT07_02_wizard_lab_set_02', 'WT07_03_wizard_lab_set_03', 'WT07_04_wizard_lab_set_04']),
                        (5, 168.0, ['WT08_01_wizard_study_set_01', 'WT08_02_wizard_study_set_02', 'WT08_03_wizard_study_set_03']),
                        (6, 200.0, ['WT07_04_wizard_lab_set_04', 'WT07_03_wizard_lab_set_03'])):
        segs = free_segments(lv)
        got = 0
        for i, mid in enumerate(mids):
            done = False
            for sc_try in (1.0, 0.85, 0.7):
                for s in range(len(segs)):
                    ang, width = segs[(i + s) % len(segs)]
                    m = wall_place(mid, lv, ang, z, False, sc_try)
                    if m and all(abs(((m['ca'] - q['ca'] + 180) % 360) - 180) > 14 for q in [measure(p['model'], p['x'], p['y'], p['z'], p['rot'], p.get('scale', 1.0)) for p in placed if p['z'] == z]):
                        add(m, scale=sc_try)
                        got += 1
                        done = True
                        break
                if done:
                    break
        print(f'SOLVE level {lv}: {got} of {len(mids)} furnishings placed ({len(segs)} wall segments)')
    # sparse upper floors: straight shelves on the free wall segments of the alchemy lab, the study and the star room (min 16 degrees from anything already there)
    extra = 0
    for lv, z, want in ((4, 136.0, 3), (5, 168.0, 3), (6, 200.0, 3)):
        segs = free_segments(lv)
        have = 0
        for gi in range(len(segs) * 2):
            if have >= want:
                break
            ang, width = segs[gi % len(segs)]
            ang = ang + (0 if gi < len(segs) else 11)
            mid = 'WT04_01_wizard_bookshelf_straight_01' if gi % 2 == 0 else 'WT04_02_wizard_bookshelf_straight_02'
            m = wall_place(mid, lv, ang, z, False, 0.85)
            if m and all(abs(((m['ca'] - q['ca'] + 180) % 360) - 180) > 16 for q in [measure(p['model'], p['x'], p['y'], p['z'], p['rot'], p.get('scale', 1.0)) for p in placed if p['z'] == z]):
                add(m, scale=0.85)
                have += 1
                extra += 1
        print(f'SOLVE level {lv}: {have} extra straight shelves')
    json.dump(placed, open(FIXED, 'w'), indent=1)
    for (fam_, lv_), lst in sorted(FAILS.items()):
        reasons = {}
        for t in lst:
            for r_ in t[1:]:
                if r_:
                    reasons[r_] = reasons.get(r_, 0) + 1
        print(f'SOLVE_FAIL {fam_} level {lv_}: {len(lst)} rejected tries; reasons {reasons}')
    return placed


# ---------------------------------------------------------------- placements
if MODE == 'plan':
    items = [p for p in json.load(open(os.path.join(T_, 'mapplan', 'v5_himalaya.json')))['placements'] if p['group'] in ('WizardTower', 'WizardTowerInterior')]
    items = [dict(model=p['model'], x=p['x'] - TX, y=-(p['z'] - TZ), z=p.get('y_offset') or 0.0, rot=p['rot'], group=p['group'], scale=p.get('scale', 1.0)) for p in items]
else:
    if MODE == 'solve':
        solve()
    items = json.load(open(FIXED))
    plan_ext = [p for p in json.load(open(os.path.join(T_, 'mapplan', 'v5_himalaya.json')))['placements'] if p['group'] == 'WizardTower']
    items = [dict(model=p['model'], x=p['x'] - TX, y=-(p['z'] - TZ), z=p.get('y_offset') or 0.0, rot=p['rot'], group='WizardTower') for p in plan_ext] + \
            [dict(model='WT02_01_wizard_tower_interior', x=0.0, y=0.0, z=0.0, rot=0.0, group='WizardTowerInterior')] + items

rows = []
for it in items:
    mid = it['model']
    if mid.startswith(('WT01', 'WT02', 'WT11', 'WT12')):
        continue
    m = measure(mid, it['x'], it['y'], it['z'], it['rot'], it.get('scale', 1.0))
    rows.append(m)
bays = [r for r in rows if r['id'].startswith('WT03')]
for a in bays:
    a['pair'] = 0
    for b in bays:
        if a is not b and a['lvl'] == b['lvl']:
            d = abs(((a['ca'] - b['ca'] + 180) % 360) - 180)
            if d < a['half'] + b['half'] - 0.5:
                a['pair'] += 1
os.makedirs(OUT, exist_ok=True)
json.dump(rows, open(os.path.join(OUT, 'metrics.json'), 'w'), indent=1)


def stair_headroom(items_):
    """Clear height above every stair tread (studs): lowest of any furnishing vertex inside the tread footprint above it and the underside of any floor plate above it."""
    if TREAD is None:
        return None
    Pt, St, ct, st = TREAD
    pts = [world(i['model'], i['x'], i['y'], i['z'], i['rot'], i.get('scale', 1.0)) for i in items_ if not i['model'].startswith(('WT01', 'WT02', 'WT11', 'WT12'))]
    V = np.concatenate(pts) if pts else np.zeros((0, 3))
    res = []
    for k in range(len(Pt)):
        top = Pt[k, 2] + St[k, 2] / 2.0
        head = 99.0
        if len(V):
            d = V - Pt[k]
            lx = d[:, 0] * ct[k] + d[:, 1] * st[k]
            ly = -d[:, 0] * st[k] + d[:, 1] * ct[k]
            m = (np.abs(lx) < St[k, 0] / 2) & (np.abs(ly) < St[k, 1] / 2) & (V[:, 2] > top + 0.4)
            if m.any():
                head = min(head, float(V[m, 2].min()) - top)
        for lv_, bs in FLOORS.items():
            if bs is None:
                continue
            Pf, Sf, cf, sf = bs
            d = Pt[k, :2] - Pf[:, :2]
            lx = d[:, 0] * cf + d[:, 1] * sf
            ly = -d[:, 0] * sf + d[:, 1] * cf
            hit = (np.abs(lx) < Sf[:, 0] / 2 + St[k, 0] / 2) & (np.abs(ly) < Sf[:, 1] / 2 + St[k, 1] / 2) & (Pf[:, 2] - Sf[:, 2] / 2 > top + 0.4)
            if hit.any():
                head = min(head, float((Pf[hit, 2] - Sf[hit, 2] / 2).min()) - top)
        res.append(head)
    return np.array(res)


HEAD = stair_headroom(items)
if HEAD is not None:
    print(f'TOWER stair headroom: {len(HEAD)} treads; lowest clear height {HEAD.min():.1f} studs; treads under 8.0 studs of headroom: {int((HEAD < 8.0).sum())}; under 7.0: {int((HEAD < 7.0).sum())}')
    bad_k = np.where(HEAD < 8.0)[0]
    if len(bad_k):
        Pt_ = TREAD[0]
        print('TOWER low headroom at (angle deg, height z, clear): ' + ', '.join(f'({math.degrees(math.atan2(Pt_[k, 1], Pt_[k, 0])) % 360:.0f}, {Pt_[k, 2]:.0f}, {HEAD[k]:.1f})' for k in bad_k[:8]))
print(f'TOWER pieces measured: {len(rows)} (mode {MODE})')
for f in sorted({r['id'][:4] for r in rows}):
    g = [r for r in rows if r['id'][:4] == f]
    print(f"TOWER {f}: n={len(g)} stair_hits={sum(1 for r in g if r['stair'])} rail_hits={sum(1 for r in g if r['rail'])} through_wall={sum(1 for r in g if r['wall'] > 0.45)} "
          f"on_window_or_door={sum(1 for r in g if r['window'])} not_over_floor={sum(1 for r in g if not r['floor'])} overlap_neighbour={sum(1 for r in g if r.get('pair'))}")
for lv in range(8):
    g = [r for r in rows if r['lvl'] == lv]
    if g:
        print(f"TOWER level {lv}: " + ', '.join(f"{k}x{sum(1 for r in g if r['id'][:4] == k)}" for k in sorted({r['id'][:4] for r in g})))

# ---------------------------------------------------------------- renders
if RENDER:
    v5liverun._patch_once()
    placed = []
    for it in items:
        ob = base_obj(it['model']).copy()
        ob.data = ob.data.copy()
        bpy.context.scene.collection.objects.link(ob)
        sc_ = it.get('scale', 1.0)
        ob.scale = (sc_, sc_, sc_)
        ob.location = (it['x'], it['y'], it['z'])
        ob.rotation_euler = (0, 0, math.radians(it['rot']))
        placed.append((it, ob))
    bpy.context.view_layer.update()
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = 14
    sc.cycles.use_denoising = False
    w = bpy.data.worlds.new('w')
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (0.62, 0.68, 0.76, 1)
    w.node_tree.nodes['Background'].inputs[1].default_value = 1.2
    sc.world = w
    sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN'))
    sun.data.energy = 3.4
    sun.rotation_euler = (math.radians(40), math.radians(10), math.radians(25))
    sc.collection.objects.link(sun)
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
    sc.collection.objects.link(cam)
    sc.camera = cam

    def shot(name, loc, rot, ortho=None, clip=0.1, fov=70, w_=RES, h_=RES):
        cam.location = loc
        cam.rotation_euler = tuple(math.radians(a) for a in rot)
        cd = cam.data
        if ortho:
            cd.type = 'ORTHO'
            cd.ortho_scale = ortho
        else:
            cd.type = 'PERSP'
            cd.lens_unit = 'FOV'
            cd.angle = math.radians(fov)
        cd.clip_start = clip
        cd.clip_end = 2000
        sc.render.resolution_x, sc.render.resolution_y = w_, h_
        sc.render.filepath = os.path.join(OUT, name + '.png')
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        print(f'RENDER {name} {time.time() - t0:.0f}s')

    shell = [ob for it, ob in placed if it['model'].startswith(('WT01', 'WT11', 'WT12'))]
    for ob in shell:
        ob.hide_render = True
    shot('plan_L0_map_hall', (0, 0, 250), (0, 0, 0), ortho=112, clip=250 - 38.5)
    shot('plan_L1_gallery', (0, 0, 250), (0, 0, 0), ortho=112, clip=250 - 70.5)
    shot('plan_L2_gallery', (0, 0, 250), (0, 0, 0), ortho=100, clip=250 - 102.5)
    shot('plan_L3_vault', (0, 0, 250), (0, 0, 0), ortho=92, clip=250 - 134.5)
    shot('hall_view', (0, -40, 9), (90, 0, 0), fov=95)
    shot('hall_view_back', (0, 40, 9), (90, 0, 180), fov=95)
    for ob in shell:
        ob.hide_render = False
    # cutaway: remove the front half (y < -2) of every mesh, then look from the front
    for it, ob in placed:
        me = ob.data
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.transform(bm, matrix=ob.matrix_world, verts=bm.verts)
        bmesh.ops.bisect_plane(bm, geom=list(bm.verts) + list(bm.edges) + list(bm.faces), dist=0.0001, plane_co=(0, -2, 0), plane_no=(0, 1, 0), clear_inner=True)
        bm.to_mesh(me)
        bm.free()
        ob.matrix_world = ob.matrix_world.__class__.Identity(4)
        ob.location, ob.rotation_euler, ob.scale = (0, 0, 0), (0, 0, 0), (1, 1, 1)
    bpy.context.view_layer.update()
    shot('cutaway_full', (0, -600, 150), (90, 0, 0), ortho=330, clip=300, w_=int(RES * 0.78), h_=int(RES * 1.2))
    shot('cutaway_lower', (0, -300, 62), (90, 0, 0), ortho=128, clip=200, w_=RES, h_=int(RES * 0.75))
    shot('cutaway_upper', (0, -300, 190), (90, 0, 0), ortho=128, clip=200, w_=RES, h_=int(RES * 0.75))
print('TOWER_DONE')
