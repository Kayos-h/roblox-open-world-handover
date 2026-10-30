"""wg2 rusty debris: E06 rusty_debris 01-12 -> v4_rusty.
5 scrap piles, 3 tents, 4 collapsed walls. Rust, patches, stakes, ropes, bedrolls.
Replacement for frozen worker wg. Builds through v4run.ps1 only. Fronts face -Y, 1 unit = 1 stud."""
import math, random
from mathutils import Euler
import kitlib
from kitlib import (reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, top_paint)
from arch import F, lbox, lslab, lbeam, beam3, nm, arc_pts

# wg2 debris palette additions (all prefixed wg2_)
kitlib.PAL['wg2_sheet']    = ((120, 78, 52),  'CorrodedMetal', 0.45, 0.88, 0)
kitlib.PAL['wg2_sheet_b']  = ((96, 100, 92),  'CorrodedMetal', 0.45, 0.85, 0)
kitlib.PAL['wg2_barrel']   = ((108, 70, 48),  'CorrodedMetal', 0.40, 0.88, 0)
kitlib.PAL['wg2_barrel_b'] = ((78, 88, 96),   'CorrodedMetal', 0.45, 0.85, 0)
kitlib.PAL['wg2_cog']      = ((86, 64, 50),   'CorrodedMetal', 0.55, 0.80, 0)
kitlib.PAL['wg2_tarp']     = ((104, 96, 72),  'Fabric',        0.00, 1.00, 0)
kitlib.PAL['wg2_tarp_b']   = ((128, 70, 58),  'Fabric',        0.00, 1.00, 0)
kitlib.PAL['wg2_canvas']   = ((176, 160, 122),'Fabric',        0.00, 1.00, 0)
kitlib.PAL['wg2_canvas_p'] = ((150, 132, 98), 'Fabric',        0.00, 1.00, 0)
kitlib.PAL['wg2_bedroll']  = ((120, 70, 60),  'Fabric',        0.00, 1.00, 0)
kitlib.PAL['wg2_plank']    = ((104, 80, 56),  'WoodPlanks',    0.00, 0.92, 0)
kitlib.PAL['wg2_plank_d']  = ((74, 56, 42),   'Wood',          0.00, 0.95, 0)
kitlib.PAL['wg2_rope']     = ((150, 128, 90),  'Fabric',       0.00, 1.00, 0)
kitlib.PAL['wg2_sand']     = ((198, 172, 132),'Sandstone',     0.00, 0.88, 0)
kitlib.PAL['wg2_sand_d']   = ((164, 140, 104),'Sandstone',     0.00, 0.90, 0)
kitlib.PAL['wg2_plaster']  = ((178, 166, 142),'Plaster',       0.00, 0.95, 0)
kitlib.PAL['wg2_beam']     = ((82, 60, 42),   'Wood',          0.00, 0.95, 0)
kitlib.PAL['wg2_brick']    = ((148, 82, 60),  'Brick',         0.00, 0.90, 0)
kitlib.PAL['wg2_brick_d']  = ((112, 62, 46),  'Brick',         0.00, 0.92, 0)
kitlib.PAL['wg2_soot']     = ((46, 40, 38),   'Slate',         0.00, 1.00, 0)
kitlib.PAL['wg2_ash']      = ((60, 56, 52),   'Ground',        0.00, 1.00, 0)
kitlib.PAL['wg2_pot']      = ((54, 48, 44),   'Metal',         0.70, 0.60, 0)
kitlib.PAL['wg2_moss']     = ((78, 92, 54),   'Grass',         0.00, 1.00, 0)
kitlib.PAL['wg2_dirt']     = ((104, 86, 64),  'Ground',        0.00, 1.00, 0)
kitlib.PAL['wg2_ember']    = ((236, 120, 40), 'Neon',          0.00, 0.50, 1.6)


def _ground(w, d, key='wg2_dirt', seed=0, z=0.16):
    o = box(nm('gr'), (w, d, 0.32), loc=(0, 0, z), key=key, bev=0.15)
    return o


def _sheet(cx, cy, cz, w, h, rx, ry, rz, key, bend=0.0):
    """A thin rusted sheet, optionally slightly dished."""
    o = box(nm('sh'), (w, h, 0.08), loc=(cx, cy, cz), key=key, rot=(rx, ry, rz), bev=0.02)
    return o


# ============================================================ E06_01..05 scrap piles
def debris_01():
    """E06_01 - heap of rusted corrugated sheet metal, leaning and stacked."""
    reset()
    _ground(10, 8, seed=1)
    rnd = random.Random(1)
    keys = ['wg2_sheet', 'wg2_sheet_b', 'tin', 'tin_b']
    for i in range(14):
        w = rnd.uniform(2.2, 4.0); h = rnd.uniform(1.6, 3.0)
        cx = rnd.uniform(-2.8, 2.8); cy = rnd.uniform(-2.2, 2.2)
        cz = 0.4 + rnd.uniform(0, 1.8)
        o = _sheet(cx, cy, cz, w, h, rnd.uniform(-70, 70), rnd.uniform(-30, 30), rnd.uniform(0, 180),
                   rnd.choice(keys))
        # corrugation ridges
        for r in range(int(w / 0.4)):
            lbox(F(cx, cy, cz, math.degrees(0)), (0.08, h * 0.9, 0.14), -w / 2 + 0.3 + r * 0.4, 0, 0, rnd.choice(keys))
    for _ in range(5):
        cyl(nm('bolt'), 0.12, 0.3, loc=(rnd.uniform(-2, 2), rnd.uniform(-1.5, 1.5), 0.2), key='wg2_cog', verts=6,
            rot=(rnd.uniform(0, 90), 0, 0))
    return finalize('rusty_debris_01', smooth_angle=35)


def debris_02():
    """E06_02 - pipes and barrels, some burst, stacked and rolled."""
    reset()
    _ground(10, 8, seed=2)
    rnd = random.Random(2)
    # barrels
    for i in range(5):
        cx = rnd.uniform(-3, 3); cy = rnd.uniform(-2, 2)
        lying = rnd.random() < 0.5
        key = rnd.choice(['wg2_barrel', 'wg2_barrel_b'])
        if lying:
            o = cyl(nm('bar'), 0.9, 2.4, loc=(cx, cy, 0.9), key=key, verts=16, rot=(0, 90, rnd.uniform(0, 180)))
        else:
            o = cyl(nm('bar'), 0.9, 2.6, loc=(cx, cy, 0.0), key=key, verts=16)
            for zz in (0.5, 1.3, 2.1):  # hoops
                torus(nm('hp'), 0.92, 0.07, loc=(cx, cy, zz), key='wg2_cog', segs=16, rsegs=4)
    # pipes bundled
    for i in range(7):
        a = i * 0.9
        px = -2.5 + (i % 4) * 0.5; py = 2.6 + (i // 4) * 0.5
        cyl(nm('pipe'), 0.3, rnd.uniform(3.0, 4.5), loc=(px, py, 0.3), key=rnd.choice(['wg2_barrel_b', 'tin_b']),
            verts=12, rot=(0, 92, rnd.uniform(-8, 8)))
    return finalize('rusty_debris_02', smooth_angle=35)


def debris_03():
    """E06_03 - broken wheels and cogs, cart axles, a pile of gears."""
    reset()
    _ground(9, 8, seed=3)
    rnd = random.Random(3)
    # cart wheels leaning
    for i in range(3):
        cx = -2.5 + i * 2.4; cy = rnd.uniform(-1, 1)
        torus(nm('rim'), 1.4, 0.18, loc=(cx, cy, 1.4), key='wg2_cog', segs=20, rsegs=5, rot=(0, rnd.uniform(-20, 20), 0))
        for sp in range(8):   # spokes
            a = 2 * math.pi * sp / 8
            tube(nm('spk'), [(cx, cy, 1.4), (cx + math.cos(a) * 1.3, cy, 1.4 + math.sin(a) * 1.3)], 0.07, 'wg2_plank_d', res=4)
        cyl(nm('hub'), 0.25, 0.4, loc=(cx, cy - 0.2, 1.4), key='wg2_cog', verts=10, rot=(90, 0, 0))
    # heap of cogs
    for _ in range(9):
        cx = rnd.uniform(-2, 2.5); cy = rnd.uniform(1.5, 3)
        R = rnd.uniform(0.4, 0.9)
        cyl(nm('cog'), R, 0.22, loc=(cx, cy, 0.2 + rnd.uniform(0, 0.6)), key='wg2_cog', verts=rnd.choice([8, 10, 12]),
            rot=(rnd.uniform(-40, 40), 0, 0))
        for t in range(10):   # teeth suggestion
            aa = 2 * math.pi * t / 10
            box(nm('tth'), (0.14, 0.14, 0.24), loc=(cx + math.cos(aa) * R, cy, 0.3 + math.sin(aa) * R), key='wg2_cog')
    return finalize('rusty_debris_03', smooth_angle=35)


def debris_04():
    """E06_04 - mixed junk under a sagging tarp: crates, metal, bottles."""
    reset()
    _ground(9, 8, seed=4)
    rnd = random.Random(4)
    # junk mound underneath
    for _ in range(8):
        box(nm('jk'), (rnd.uniform(0.8, 1.6), rnd.uniform(0.8, 1.6), rnd.uniform(0.8, 1.6)),
            loc=(rnd.uniform(-2, 2), rnd.uniform(-1.5, 1.5), rnd.uniform(0.4, 1.4)),
            key=rnd.choice(['wg2_plank', 'wg2_barrel', 'wg2_sheet_b']), rot=(0, 0, rnd.uniform(0, 90)), bev=0.05)
    # sagging tarp draped over the junk mound, with a dip in the middle
    seg = 8
    rows = []
    for j in range(5):
        y = -2.4 + 4.8 * j / 4
        row = []
        for i in range(seg + 1):
            x = -3.0 + 6.0 * i / seg
            sagx = math.sin(math.pi * i / seg)
            sagy = math.sin(math.pi * j / 4)
            z = 1.2 + 1.6 * sagx * sagy
            row.append((x, y, z))
        rows.append(row)
    _drape(rows, 'wg2_tarp')
    # tie-down ropes at corners
    for sx in (-1, 1):
        for sy in (-1, 1):
            tube(nm('rp'), [(sx * 2.8, sy * 2.2, 1.3), (sx * 3.3, sy * 2.6, 0.0)], 0.05, 'wg2_rope', res=4)
            cyl(nm('stk'), 0.08, 0.7, loc=(sx * 3.3, sy * 2.6, 0.0), key='wg2_plank_d', verts=6)
    return finalize('rusty_debris_04', smooth_angle=35)


def _drape(rows, key):
    """Build a thin quad-mesh cloth surface from a grid of 3D points (a draped tarp/tent)."""
    import bmesh
    bm = bmesh.new()
    verts = [[bm.verts.new(p) for p in row] for row in rows]
    for j in range(len(rows) - 1):
        for i in range(len(rows[0]) - 1):
            bm.faces.new((verts[j][i], verts[j][i + 1], verts[j + 1][i + 1], verts[j + 1][i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=-0.08)  # give the shell thickness
    return kitlib._obj_from_bm(nm('drape'), bm, key)


def debris_05():
    """E06_05 - collapsed scaffolding and planks, fallen poles and boards."""
    reset()
    _ground(11, 8, seed=5)
    rnd = random.Random(5)
    # a few upright broken scaffold poles
    for i in range(4):
        px = -3.5 + i * 2.2
        h = rnd.uniform(2.0, 4.2)
        cyl(nm('pole'), 0.14, h, loc=(px, rnd.uniform(-1, 1), 0.0), key='wg2_barrel_b', verts=8,
            rot=(rnd.uniform(-6, 6), rnd.uniform(-10, 10), 0))
    # collapsed poles lying across
    for _ in range(6):
        a = rnd.uniform(0, 3.14)
        L = rnd.uniform(3, 6)
        cx = rnd.uniform(-2, 2); cy = rnd.uniform(-2, 2); cz = 0.2 + rnd.uniform(0, 1.0)
        beam3((cx - math.cos(a) * L / 2, cy - math.sin(a) * L / 2, cz),
              (cx + math.cos(a) * L / 2, cy + math.sin(a) * L / 2, cz + rnd.uniform(-0.4, 0.8)),
              0.16, 0.16, rnd.choice(['wg2_barrel_b', 'tin_b']))
    # scattered planks
    for _ in range(8):
        a = rnd.uniform(0, 180)
        box(nm('pk'), (rnd.uniform(2, 3.6), 0.5, 0.12), loc=(rnd.uniform(-3, 3), rnd.uniform(-2.5, 2.5), 0.1 + rnd.uniform(0, 0.8)),
            key=rnd.choice(['wg2_plank', 'wg2_plank_d']), rot=(0, rnd.uniform(-20, 20), a), bev=0.02)
    # couplers
    for _ in range(4):
        cyl(nm('cp'), 0.2, 0.3, loc=(rnd.uniform(-3, 3), rnd.uniform(-2, 2), 0.2), key='wg2_cog', verts=8, rot=(90, 0, 0))
    return finalize('rusty_debris_05', smooth_angle=35)


# ============================================================ E06_06..08 tents
def _bedroll(cx, cy, a=0.0, key='wg2_bedroll'):
    o = cyl(nm('bed'), 0.4, 2.2, loc=(cx, cy, 0.4), key=key, verts=10, rot=(0, 90, a))
    box(nm('blk'), (2.0, 1.3, 0.12), loc=(cx + math.cos(math.radians(a)) * 0.2, cy, 0.18), key='wg2_tarp_b',
        rot=(0, 0, a), bev=0.03)
    return o


def _stake(cx, cy, key='wg2_plank_d'):
    cyl(nm('stk'), 0.08, 0.8, loc=(cx, cy, 0.0), key=key, verts=6, rot=(6, 4, 0))


def debris_06():
    """E06_06 - patched canvas A-frame tent, stakes, ropes, a bedroll inside."""
    reset()
    _ground(9, 8, seed=6, key='wg2_dirt')
    rnd = random.Random(6)
    L, W, Hh = 6.0, 4.0, 3.2
    # ridge pole on two end poles
    cyl(nm('ep1'), 0.1, Hh + 0.3, loc=(-L / 2, 0, 0), key='wg2_plank_d', verts=6)
    cyl(nm('ep2'), 0.1, Hh + 0.3, loc=(L / 2, 0, 0), key='wg2_plank_d', verts=6)
    tube(nm('ridge'), [(-L / 2, 0, Hh), (L / 2, 0, Hh)], 0.1, 'wg2_plank_d', res=4)
    # two canvas slopes as draped grids with a slight sag
    for s in (-1, 1):
        rows = []
        for j in range(4):
            x = -L / 2 + L * j / 3
            row = []
            for i in range(4):
                t = i / 3
                yy = s * (W / 2) * t
                zz = Hh * (1 - t) + 0.12 * math.sin(math.pi * j / 3) * math.sin(math.pi * t)
                row.append((x, yy, zz))
            rows.append(row)
        _drape(rows, rnd.choice(['wg2_canvas', 'wg2_canvas_p']))
    # patches (darker squares)
    for _ in range(6):
        s = rnd.choice([-1, 1]); t = rnd.uniform(0.2, 0.8)
        box(nm('ptc'), (0.8, 0.8, 0.06), loc=(rnd.uniform(-L / 2 + 0.6, L / 2 - 0.6), s * (W / 2) * t * 0.9, Hh * (1 - t)),
            key='wg2_canvas_p', rot=(math.degrees(math.atan2(s * W / 2, Hh)) * 0.6, 0, 0), bev=0.01)
    # guy ropes + stakes
    for s in (-1, 1):
        for ex in (-L / 2, L / 2):
            tube(nm('guy'), [(ex, 0, Hh + 0.2), (ex + (0.1 if ex < 0 else -0.1), s * (W / 2 + 1.2), 0.0)], 0.04, 'wg2_rope', res=4)
            _stake(ex, s * (W / 2 + 1.2))
    _bedroll(0, 0, a=0.0)
    return finalize('rusty_debris_06', smooth_angle=35)


def debris_07():
    """E06_07 - round tent (bell tent) with a centre pole, ropes, a bedroll."""
    reset()
    _ground(10, 10, seed=7, key='wg2_dirt')
    rnd = random.Random(7)
    R, Hh = 3.2, 3.6
    # centre pole
    cyl(nm('cp'), 0.12, Hh + 0.4, loc=(0, 0, 0), key='wg2_plank_d', verts=6)
    # conical roof as a lathe cloth with a scalloped hem
    lathe(nm('roof'), [(0, Hh + 0.3), (R * 0.5, Hh * 0.7), (R, 1.2), (R + 0.2, 1.1)], loc=(0, 0, 0),
          key='wg2_canvas', segs=14)
    # short cylindrical wall
    lathe(nm('wall'), [(R + 0.2, 1.1), (R + 0.2, 0.0)], loc=(0, 0, 0), key='wg2_canvas_p', segs=14)
    # door flap (gap) on the front
    box(nm('flap'), (0.1, 1.2, 1.4), loc=(0, -R - 0.1, 0.7), key='wg2_canvas', rot=(0, 0, 8))
    # patches
    for _ in range(7):
        a = rnd.uniform(0, 6.28); zz = rnd.uniform(1.4, 3.0); rr = R * (1 - (zz - 1.1) / (Hh))
        box(nm('ptc'), (0.7, 0.7, 0.06), loc=(math.cos(a) * rr, math.sin(a) * rr, zz), key='wg2_canvas_p',
            rot=(0, 0, math.degrees(a)))
    # guy ropes radiating
    for i in range(8):
        a = 2 * math.pi * i / 8
        ex = math.cos(a) * (R + 0.2); ey = math.sin(a) * (R + 0.2)
        tube(nm('guy'), [(ex, ey, 1.1), (ex * 1.5, ey * 1.5, 0.0)], 0.04, 'wg2_rope', res=4)
        _stake(ex * 1.5, ey * 1.5)
    _bedroll(0.8, 0.0, a=20)
    return finalize('rusty_debris_07', smooth_angle=35)


def debris_08():
    """E06_08 - lean-to tarp shelter against a frame, a cooking pot and embers."""
    reset()
    _ground(10, 8, seed=8, key='wg2_dirt')
    rnd = random.Random(8)
    L, W = 5.0, 4.0
    # back frame: two tall + two short poles
    for s in (-1, 1):
        cyl(nm('tp'), 0.1, 3.4, loc=(s * L / 2, W / 2, 0), key='wg2_plank_d', verts=6)
        cyl(nm('sp'), 0.1, 1.2, loc=(s * L / 2, -W / 2, 0), key='wg2_plank_d', verts=6)
    tube(nm('bt'), [(-L / 2, W / 2, 3.4), (L / 2, W / 2, 3.4)], 0.08, 'wg2_plank_d', res=4)
    tube(nm('ft'), [(-L / 2, -W / 2, 1.2), (L / 2, -W / 2, 1.2)], 0.08, 'wg2_plank_d', res=4)
    # sloping tarp roof as a draped grid
    rows = []
    for j in range(4):
        x = -L / 2 + L * j / 3
        row = []
        for i in range(4):
            t = i / 3
            yy = W / 2 - W * t
            zz = 3.4 - (3.4 - 1.2) * t + 0.1 * math.sin(math.pi * j / 3)
            row.append((x, yy, zz))
        rows.append(row)
    _drape(rows, 'wg2_tarp')
    for _ in range(4):
        box(nm('ptc'), (0.7, 0.7, 0.06), loc=(rnd.uniform(-L / 2 + 0.5, L / 2 - 0.5), rnd.uniform(-1, 1), rnd.uniform(1.6, 3.0)),
            key='wg2_tarp_b', rot=(45, 0, 0))
    # ropes from the front edge
    for ex in (-L / 2, L / 2):
        tube(nm('guy'), [(ex, -W / 2, 1.2), (ex, -W / 2 - 1.3, 0.0)], 0.04, 'wg2_rope', res=4)
        _stake(ex, -W / 2 - 1.3)
    _bedroll(0, 0.6, a=0)
    # cooking fire out front: ring of stones, pot on a tripod, embers
    for i in range(7):
        a = 2 * math.pi * i / 7
        ball(nm('fs'), 0.28, loc=(math.cos(a) * 0.9, -W / 2 - 1.2 + math.sin(a) * 0.9, 0.2), key='stone_dark', segs=6, rings=4)
    for i in range(3):
        a = 2 * math.pi * i / 3
        tube(nm('leg'), [(math.cos(a) * 0.7, -W / 2 - 1.2 + math.sin(a) * 0.7, 0.0), (0, -W / 2 - 1.2, 1.6)], 0.05, 'wg2_pot', res=4)
    lathe(nm('pot'), [(0, 0), (0.5, 0), (0.55, 0.5), (0.4, 0.8), (0.42, 0.9)], loc=(0, -W / 2 - 1.2, 0.7), key='wg2_pot', segs=12)
    ball(nm('emb'), 0.22, loc=(0, -W / 2 - 1.2, 0.15), key='wg2_ember', segs=6, rings=4)
    return finalize('rusty_debris_08', smooth_angle=35)


# ============================================================ E06_09..12 collapsed walls
def _rubble(cx, cy, n, spread, key, seed):
    rnd = random.Random(seed)
    for _ in range(n):
        s = rnd.uniform(0.4, 1.1)
        box(nm('rb'), (s, s * rnd.uniform(0.7, 1.1), s * rnd.uniform(0.6, 1.0)),
            loc=(cx + rnd.uniform(-spread, spread), cy + rnd.uniform(-spread * 0.6, spread * 0.6), s * 0.4),
            key=key, rot=(rnd.uniform(0, 40), rnd.uniform(0, 40), rnd.uniform(0, 90)), bev=0.04)


def _coursed(f, w, h, z0, key, dark, seed, t=0.06):
    rnd = random.Random(seed)
    for i in range(1, max(2, int(h / 0.9))):
        lbox(f, (w - 0.2, t, t), 0, -0.02, z0 + 0.9 * i, dark)
    for _ in range(int(w)):
        lbox(f, (t, t, 0.7), rnd.uniform(-w / 2 + 0.4, w / 2 - 0.4), -0.02, z0 + rnd.uniform(0.4, h - 0.4), dark)


def debris_09():
    """E06_09 - sandstone wall remains with a window gap, jagged broken top."""
    reset()
    _ground(12, 6, seed=9, key='wg2_sand_d')
    W, T = 9.0, 1.4
    # left section (tall) with a window opening
    box(nm('lw'), (3.4, T, 4.6), loc=(-3.0, 0, 2.3), key='wg2_sand', bev=0.06)
    box(nm('gap'), (1.4, T + 0.2, 1.6), loc=(-3.0, 0, 2.6), key='wg2_sand_d')  # darker reveal (window)
    lbox(F(-3.0, -T / 2, 0, 0), (1.5, 0.1, 0.25), 0, 0, 3.5, 'wg2_sand_d')  # lintel
    _coursed(F(-3.0, -T / 2, 0, 0), 3.4, 4.6, 0, 'wg2_sand', 'wg2_sand_d', 91)
    # right section (lower, broken diagonally)
    pts = [(-1.6, 0, 0), (2.2, 0, 0), (2.2, 0, 2.4), (0.8, 0, 3.1), (-0.4, 0, 2.0), (-1.6, 0, 2.6)]
    o = lslab(F(2.0, T / 2, 0, 0), pts, (0, -T, 0), 'wg2_sand')
    _coursed(F(2.0, -T / 2, 0, 0), 3.6, 2.4, 0, 'wg2_sand', 'wg2_sand_d', 92)
    # jagged top rubble + fallen blocks
    _rubble(-0.5, 0, 10, 3.5, 'wg2_sand', 93)
    top_paint(box(nm('cap'), (3.4, T, 0.3), loc=(-3.0, 0, 4.6), key='wg2_sand'), 'wg2_moss', 0.8, 9)
    return finalize('rusty_debris_09', smooth_angle=30)


def debris_10():
    """E06_10 - second sandstone wall remains, an arched window gap, leaning."""
    reset()
    _ground(12, 6, seed=10, key='wg2_sand_d')
    T = 1.4
    o = box(nm('w'), (7.0, T, 5.0), loc=(0, 0, 2.5), key='wg2_sand', bev=0.06)
    o.rotation_euler = Euler((0, math.radians(3), 0))
    # arched window gap: dark reveal + arch tube
    box(nm('gap'), (1.8, T + 0.2, 2.2), loc=(1.2, 0, 2.2), key='wg2_sand_d')
    tube(nm('arch'), arc_pts(F(1.2, -T / 2 - 0.02, 0, 0), 0, 3.3, 0.9, y=0, n=9), 0.18, 'wg2_sand_d', res=4)
    # broken-away right end (missing top corner)
    box(nm('brk'), (2.2, T + 0.1, 2.0), loc=(3.6, 0, 4.0), key='wg2_sand_d', rot=(0, 18, 0))
    _coursed(F(0, -T / 2, 0, 0), 7.0, 5.0, 0, 'wg2_sand', 'wg2_sand_d', 101)
    _rubble(-2.5, 0, 9, 2.8, 'wg2_sand', 102)
    top_paint(o, 'wg2_moss', 0.82, 10)
    return finalize('rusty_debris_10', smooth_angle=30)


def debris_11():
    """E06_11 - plaster-and-timber wall with exposed beams, broken laths."""
    reset()
    _ground(12, 6, seed=11, key='wg2_dirt')
    T = 1.0
    # plaster panel, broken on the right
    pts = [(-4.0, 0, 0), (2.0, 0, 0), (2.0, 0, 3.4), (0.6, 0, 4.2), (-1.2, 0, 3.0), (-2.6, 0, 4.4), (-4.0, 0, 3.8)]
    o = lslab(F(0, T / 2, 0, 0), pts, (0, -T, 0), 'wg2_plaster')
    # exposed timber frame (studs + braces) standing proud where plaster fell
    f = F(0, -T / 2 - 0.05, 0, 0)
    for x in (-3.4, -2.2, -1.0, 0.2, 1.4):
        lbox(f, (0.35, 0.3, 4.0), x, -0.1, 2.0, 'wg2_beam')
    lbox(f, (6.2, 0.3, 0.35), -1.0, -0.1, 0.4, 'wg2_beam')     # sill
    lbox(f, (6.2, 0.3, 0.35), -1.0, -0.1, 3.4, 'wg2_beam')     # top plate
    lbeam(f, (-3.4, -0.1, 0.5), (-1.0, -0.1, 3.3), 0.3, 'wg2_beam')  # diagonal brace
    # broken laths poking out on the damaged right side
    rnd = random.Random(11)
    for _ in range(6):
        lbox(f, (0.08, 0.3, rnd.uniform(0.6, 1.4)), rnd.uniform(0.6, 1.8), -0.15, rnd.uniform(2.6, 3.6), 'wg2_plank_d',
             rot=(rnd.uniform(-20, 20), 0, 0))
    _rubble(1.6, 0, 7, 2.0, 'wg2_plaster', 112)
    return finalize('rusty_debris_11', smooth_angle=30)


def debris_12():
    """E06_12 - brick chimney stub with a fireplace opening, sooted, crumbling top."""
    reset()
    _ground(9, 7, seed=12, key='wg2_dirt')
    # chimney breast
    box(nm('br'), (3.6, 2.4, 5.0), loc=(0, 0, 2.5), key='wg2_brick', bev=0.05)
    # crumbling top: stepped missing bricks
    rnd = random.Random(12)
    for _ in range(10):
        box(nm('tb'), (rnd.uniform(0.4, 0.7), rnd.uniform(0.4, 0.6), 0.4),
            loc=(rnd.uniform(-1.6, 1.6), rnd.uniform(-1.0, 1.0), 5.0 + rnd.uniform(0, 0.8)),
            key=rnd.choice(['wg2_brick', 'wg2_brick_d']), rot=(0, 0, rnd.uniform(0, 40)), bev=0.03)
    # fireplace opening (arched), sooted reveal
    box(nm('op'), (2.0, 2.6, 2.4), loc=(0, 0, 1.3), key='wg2_soot')
    tube(nm('arch'), arc_pts(F(0, -1.2 - 0.02, 0, 0), 0, 2.5, 1.0, y=0, n=9), 0.18, 'wg2_brick_d', res=4)
    # mantel beam
    lbox(F(0, -1.2, 0, 0), (2.6, 0.5, 0.4), 0, -0.1, 2.7, 'wg2_beam')
    # brick courses on the front
    for i in range(1, 9):
        lbox(F(0, -1.2, 0, 0), (3.6, 0.05, 0.05), 0, -0.02, 0.55 * i, 'wg2_brick_d')
    # ash bed + a couple of charred logs
    box(nm('ash'), (1.8, 1.4, 0.2), loc=(0, 0, 0.12), key='wg2_ash')
    for _ in range(3):
        cyl(nm('log'), 0.18, 1.2, loc=(rnd.uniform(-0.5, 0.5), rnd.uniform(-0.3, 0.3), 0.2), key='wg2_soot',
            verts=8, rot=(0, 90, rnd.uniform(0, 180)))
    ball(nm('emb'), 0.18, loc=(0, 0, 0.18), key='wg2_ember', segs=6, rings=4)
    _rubble(2.6, 0, 6, 1.6, 'wg2_brick', 122)
    return finalize('rusty_debris_12', smooth_angle=30)


BATCHES = {
    'scrap': ('v4_rusty', [
        ('E06_01_rusty_debris_01', debris_01, (1.0, -1.1, 0.5)),
        ('E06_02_rusty_debris_02', debris_02, (1.0, -1.1, 0.5)),
        ('E06_03_rusty_debris_03', debris_03, (1.0, -1.1, 0.5)),
        ('E06_04_rusty_debris_04', debris_04, (1.0, -1.1, 0.5)),
        ('E06_05_rusty_debris_05', debris_05, (1.0, -1.1, 0.5)),
    ]),
    'tents': ('v4_rusty', [
        ('E06_06_rusty_debris_06', debris_06, (1.0, -1.2, 0.4)),
        ('E06_07_rusty_debris_07', debris_07, (1.0, -1.2, 0.4)),
        ('E06_08_rusty_debris_08', debris_08, (1.0, -1.2, 0.4)),
    ]),
    'walls': ('v4_rusty', [
        ('E06_09_rusty_debris_09', debris_09, (0.9, -1.2, 0.4)),
        ('E06_10_rusty_debris_10', debris_10, (0.9, -1.2, 0.4)),
        ('E06_11_rusty_debris_11', debris_11, (0.9, -1.2, 0.4)),
        ('E06_12_rusty_debris_12', debris_12, (0.9, -1.2, 0.4)),
    ]),
}
