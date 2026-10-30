"""v4_wf2_props - alpine village props C02-C09 (worker wf2, replacing wf).
Front faces -Y. 1 unit = 1 stud. Origin = bottom centre (kitlib.finalize).
Winter palette: soft thick snow (rounded drifts, overhanging caps, icicles), clear/blue ice,
weathered timber, grey stone, warm lantern glow. New keys use the wf2_ prefix; base keys reused where they fit.
Reuses kitlib shapes, arch F/faces/lbox/lbeam, nature.blob/rock. Does not edit any existing file.
"""
import math, random
from mathutils import Vector
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, flame
from arch import F, faces, nm, lbox, lbeam
from nature import blob, rock
import v4util as U

# ---- winter palette (wf2_ prefix) -------------------------------------------------
P = kitlib.PAL
P.setdefault('wf2_timber',      ((98, 68, 46),   'Wood',       0.0, 0.85, 0))
P.setdefault('wf2_timber_dark', ((64, 44, 30),   'Wood',       0.0, 0.90, 0))
P.setdefault('wf2_plank',       ((146, 110, 72),  'WoodPlanks', 0.0, 0.80, 0))
P.setdefault('wf2_plank_light', ((182, 146, 100), 'WoodPlanks', 0.0, 0.78, 0))
P.setdefault('wf2_plank_grey',  ((132, 124, 112), 'WoodPlanks', 0.0, 0.92, 0))
P.setdefault('wf2_stone',       ((150, 146, 140), 'Cobblestone', 0.0, 0.92, 0))
P.setdefault('wf2_stone_dark',  ((112, 108, 104), 'Slate',      0.0, 0.92, 0))
P.setdefault('wf2_glow',        ((248, 196, 112), 'Glass',      0.0, 0.20, 0.55))
P.setdefault('wf2_ice',         ((206, 230, 240), 'Ice',        0.0, 0.18, 0))
P.setdefault('wf2_ice_blue',    ((150, 196, 224), 'Ice',        0.0, 0.16, 0))
P.setdefault('wf2_ice_deep',    ((96, 150, 196),  'Ice',        0.0, 0.14, 0))
P.setdefault('wf2_awn_red',     ((176, 64, 56),   'Fabric',     0.0, 0.95, 0))
P.setdefault('wf2_awn_cream',   ((234, 222, 198), 'Fabric',     0.0, 0.95, 0))
P.setdefault('wf2_awn_green',   ((70, 110, 82),   'Fabric',     0.0, 0.95, 0))
P.setdefault('wf2_awn_blue',    ((70, 100, 150),  'Fabric',     0.0, 0.95, 0))
P.setdefault('wf2_wool_red',    ((178, 72, 66),   'Fabric',     0.0, 1.0, 0))
P.setdefault('wf2_wool_mustard',((214, 168, 70),  'Fabric',     0.0, 1.0, 0))
P.setdefault('wf2_wool_teal',   ((68, 138, 134),  'Fabric',     0.0, 1.0, 0))
P.setdefault('wf2_coal',        ((40, 36, 34),    'Slate',      0.0, 0.95, 0))
P.setdefault('wf2_ember',       ((248, 120, 48),  'Neon',       0.0, 0.5, 2.0))
P.setdefault('wf2_fur',         ((150, 120, 92),  'Fabric',     0.0, 1.0, 0))
P.setdefault('wf2_fur_dark',    ((104, 82, 62),   'Fabric',     0.0, 1.0, 0))
P.setdefault('wf2_carrot',      ((220, 120, 40),  'SmoothPlastic', 0.0, 0.6, 0))
P.setdefault('wf2_bark',        ((86, 64, 46),    'Wood',       0.0, 0.95, 0))
P.setdefault('wf2_fish',        ((150, 164, 176), 'SmoothPlastic', 0.3, 0.4, 0))

SNOW = 'snow'


# ---- shared detail helpers --------------------------------------------------------
def snow_pillow(cx, cy, w, d, z, h=0.5, key=SNOW, bev=None, seed=0):
    """Soft rounded snow cushion on a flat top (cap, sill, beam)."""
    box(nm('sp'), (w, d, h), loc=(cx, cy, z + h * 0.4), key=key, bev=(bev if bev is not None else min(w, d) * 0.28))


def snow_drift(cx, cy, r, key=SNOW, seed=0, scale=(1.5, 1.2, 0.5)):
    blob(nm('dr'), r, (cx, cy, 0.0), key, subdiv=2, amp=0.12, scale=scale, seed=seed)


def icicles(x0, x1, y, z, n=None, lo=0.4, hi=1.4, seed=0, prob=0.72, key='wf2_ice'):
    """Row of clear icicles of varied length hanging down from z, along x at depth y."""
    rnd = random.Random(seed)
    n = n or max(3, int((x1 - x0) / 0.7))
    for i in range(n):
        if rnd.random() > prob:
            continue
        x = x0 + (x1 - x0) * i / max(1, n - 1)
        h = rnd.uniform(lo, hi)
        r = rnd.uniform(0.07, 0.15)
        lathe(nm('ic'), [(0, 0), (r, 0), (r * 0.5, -h * 0.45), (0, -h)], loc=(x, y, z), key=key, segs=5)


def ground_frost(cx, cy, rx, ry, n=10, seed=0):
    """Scattered low snow lumps banked at the base — no hard slab (reads as a floating tray)."""
    rnd = random.Random(seed)
    for i in range(n):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0.5, 1.05)
        snow_drift(cx + math.cos(a) * rx * d, cy + math.sin(a) * ry * d,
                   rnd.uniform(0.6, 1.2), seed=seed + i, scale=(1.5, 1.2, 0.32))


def plank_floor(cx, cy, w, d, z, h=0.3, key='wf2_plank', n=None):
    n = n or max(3, int(w / 1.1))
    for i in range(n):
        x = cx - w / 2 + w * (i + 0.5) / n
        box(nm('pf'), (w / n - 0.06, d, h), loc=(x, cy, z), key=key if i % 2 else 'wf2_plank_light')


def lantern(x, y, z, r=0.5, h=1.3, cage='iron', seed=0):
    """Small hanging lantern with warm glow."""
    cyl(nm('lt'), r, h, loc=(x, y, z), key=cage, verts=6)
    box(nm('lg'), (r * 1.1, r * 1.1, h * 0.7), loc=(x, y, z + h * 0.5), key='wf2_glow')
    cyl(nm('lc'), r * 1.25, 0.18, loc=(x, y, z + h), key=cage, verts=6)
    ball(nm('lr'), 0.12, loc=(x, y, z + h + 0.25), key=cage, segs=6, rings=4)


# ================================================================ C02 winter stalls
def _stall(seed, stripe_a, stripe_b, awn_shape, name, filling):
    reset()
    rnd = random.Random(seed)
    w, d, h = 10.0, 8.0, 5.0            # counter block; roof rises above
    # deck + four posts
    box(nm('dk'), (w, d, 0.3), loc=(0, 0, 0.15), key='wf2_timber_dark')
    plank_floor(0, 0, w, d, 0.32)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl(nm('po'), 0.32, h + 1.2, loc=(sx * (w / 2 - 0.5), sy * (d / 2 - 0.5), 0.3), key='wf2_timber', verts=8)
    # counter at the front (-Y): a low plank bar with a stone-slab top
    box(nm('ct'), (w - 0.6, 1.8, 3.0), loc=(0, -d / 2 + 1.0, 1.5), key='wf2_plank')
    box(nm('cts'), (w + 0.2, 2.1, 0.4), loc=(0, -d / 2 + 1.0, 3.1), key='wf2_stone', bev=0.08)
    # back wall so it is not see-through, with hanging boards
    box(nm('bw'), (w - 0.4, 0.4, h), loc=(0, d / 2 - 0.4, h / 2 + 0.3), key='wf2_plank_grey')
    # striped awning: a gable or shed over the top, built from alternating fabric strips
    rz = h + 1.3
    nst = int(w / 1.0)
    if awn_shape == 'gable':
        hr = 2.6
        for s in (-1, 1):
            for i in range(nst):
                x = -w / 2 + w * (i + 0.5) / nst
                box(nm('aw'), (w / nst - 0.05, (d / 2 + 1.3) / math.cos(0.5), 0.14),
                    loc=(x, s * (d / 4 + 0.3), rz + hr / 2 - 0.3), key=(stripe_a if i % 2 else stripe_b),
                    rot=(s * -28, 0, 0))
        box(nm('rdg'), (w + 0.6, 0.3, 0.3), loc=(0, 0, rz + hr), key='wf2_timber')
        snow_pillow(0, s * 0, w + 0.4, d + 1.4, rz + hr - 0.1, h=0.5, seed=seed)
        icicles(-w / 2, w / 2, -d / 2 - 1.2, rz - 0.2, lo=0.4, hi=1.2, seed=seed + 1)
    else:  # shed slope toward the front
        aa = 22
        for i in range(nst):
            x = -w / 2 + w * (i + 0.5) / nst
            box(nm('aw'), (w / nst - 0.05, d + 3.0, 0.14), loc=(x, -0.6, rz + 0.3), key=(stripe_a if i % 2 else stripe_b), rot=(-aa, 0, 0))
        snow_pillow(0, 0.2, w + 0.4, d + 3.0, rz + 0.55, h=0.5, seed=seed)
        icicles(-w / 2, w / 2, -d / 2 - 1.6, rz - 0.4, lo=0.4, hi=1.3, seed=seed + 1)
    # scalloped awning valance along the front edge
    for i in range(nst):
        x = -w / 2 + w * (i + 0.5) / nst
        lathe(nm('vl'), [(0, 0), (0.45, 0), (0.3, -0.5), (0, -0.7)], loc=(x, -d / 2 - 1.3, rz - 0.1),
              key=(stripe_a if i % 2 else stripe_b), segs=4, rot=(90, 0, 0))
    lantern(-w / 2 + 0.6, -d / 2 - 0.4, rz - 1.4, r=0.4, h=1.0, seed=seed)
    lantern(w / 2 - 0.6, -d / 2 - 0.4, rz - 1.4, r=0.4, h=1.0, seed=seed + 2)
    filling(rnd, w, d)
    ground_frost(0, 0, w / 2 + 0.5, d / 2 + 0.5, seed=seed)
    U.marker('mk_conn', (0, -d / 2 - 0.4, 0.3))
    return finalize(name, smooth_angle=35)


def winter_stall_01():
    """C02_01 mulled-wine stall: striped awning, a steaming cauldron on a brazier, mugs on the counter."""
    def fill(rnd, w, d):
        cy = -d / 2 + 1.0
        # cauldron on the counter
        lathe(nm('cau'), [(0, 0), (1.1, 0.1), (1.25, 0.7), (1.0, 1.3), (1.1, 1.5)], loc=(-2.2, cy, 3.3), key='iron', segs=14)
        lathe(nm('cauw'), [(0, 1.35), (1.0, 1.35)], loc=(-2.2, cy, 3.3), key='wf2_glow', segs=14)  # glowing wine surface
        torus(nm('cauh'), 1.25, 0.1, loc=(-2.2, cy, 4.7), key='iron', segs=14, rsegs=4, rot=(90, 0, 0))
        # steam
        for i in range(3):
            ball(nm('stm'), 0.5 - i * 0.1, (-2.2 + rnd.uniform(-0.3, 0.3), cy, 5.1 + i * 0.7), 'foam', segs=7, rings=4, scale=(1, 1, 1.3))
        # mugs
        for i in range(4):
            cyl(nm('mug'), 0.3, 0.6, loc=(1.0 + i * 0.9, cy - 0.3, 3.3), key='terracotta', verts=8)
    return _stall(2001, 'wf2_awn_red', 'wf2_awn_cream', 'gable', 'C02_01_winter_stall_01', fill)


def winter_stall_02():
    """C02_02 knitwear stall: green-striped shed awning, scarves and hats hanging from a rail."""
    def fill(rnd, w, d):
        rail_z = 5.6
        box(nm('rail'), (w - 1.6, 0.14, 0.14), loc=(0, -d / 2 + 1.8, rail_z), key='wf2_timber')
        cols = ['wf2_wool_red', 'wf2_wool_mustard', 'wf2_wool_teal', 'wf2_awn_cream']
        for i in range(6):
            x = -w / 2 + 1.2 + i * 1.4
            hh = rnd.uniform(2.0, 3.0)
            k = cols[i % len(cols)]
            box(nm('scf'), (0.7, 0.1, hh), loc=(x, -d / 2 + 1.8, rail_z - hh / 2), key=k)
            box(nm('fr1'), (0.7, 0.12, 0.3), loc=(x, -d / 2 + 1.8, rail_z - hh), key=k)
        # folded hats stacked on the counter
        for i in range(3):
            ball(nm('hat'), 0.5, (-3.0 + i * 1.5, -d / 2 + 1.0, 3.5), cols[i % 3], segs=8, rings=5, scale=(1, 1, 0.8))
            ball(nm('pom'), 0.22, (-3.0 + i * 1.5, -d / 2 + 1.0, 4.0), 'wf2_awn_cream', segs=6, rings=4)
    return _stall(2002, 'wf2_awn_green', 'wf2_awn_cream', 'shed', 'C02_02_winter_stall_02', fill)


def winter_stall_03():
    """C02_03 roast-chestnut stall: blue-striped gable awning, a glowing brazier of chestnuts."""
    def fill(rnd, w, d):
        cy = -d / 2 + 1.0
        # brazier drum on legs
        cyl(nm('brz'), 1.3, 1.6, loc=(0, cy, 3.3), key='wf2_coal', verts=12)
        for a in range(3):
            ar = math.radians(90 + a * 120)
            cyl(nm('leg'), 0.14, 1.4, loc=(math.cos(ar) * 1.0, cy + math.sin(ar) * 1.0, 1.9), key='iron', verts=5)
        # roasting pan with chestnuts + embers on top
        cyl(nm('pan'), 1.45, 0.4, loc=(0, cy, 4.9), key='iron', verts=14)
        for i in range(14):
            a = rnd.uniform(0, 6.28); dd = rnd.uniform(0, 1.0)
            ball(nm('ch'), 0.24, (math.cos(a) * dd, cy + math.sin(a) * dd, 5.15), rnd.choice(['wf2_bark', 'wf2_timber_dark']), segs=6, rings=4)
        for i in range(5):
            a = rnd.uniform(0, 6.28); dd = rnd.uniform(0, 0.8)
            ball(nm('em'), 0.12, (math.cos(a) * dd, cy + math.sin(a) * dd, 5.1), 'wf2_ember', segs=5, rings=3)
    return _stall(2003, 'wf2_awn_blue', 'wf2_awn_cream', 'gable', 'C02_03_winter_stall_03', fill)


# ================================================================ C03 ski rack
def ski_rack_01():
    """C03_01 ~10x4x6 wooden A-frame rack holding six skis and pairs of poles, with snow on top."""
    reset()
    rnd = random.Random(301)
    w, d, h = 10.0, 4.0, 6.0
    box(nm('base'), (w, d, 0.3), loc=(0, 0, 0.15), key='wf2_timber_dark')
    # two A-frame ends joined by a top rail
    for sx in (-1, 1):
        x = sx * (w / 2 - 0.6)
        for s in (-1, 1):
            cyl(nm('ag'), 0.2, h * 1.05, loc=(x, s * (d / 2 - 0.5), 0.3), key='wf2_timber', verts=6, rot=(s * 14, 0, 0))
    box(nm('tr'), (w - 0.4, 0.3, 0.3), loc=(0, 0, h - 0.4), key='wf2_timber')
    box(nm('mr'), (w - 0.4, 0.3, 0.26), loc=(0, 0, h * 0.5), key='wf2_timber')
    snow_pillow(0, 0, w - 0.2, 0.7, h - 0.2, h=0.4, seed=1)
    # six skis leaning in the rack, varied colours and tilt
    cols = ['wf2_wool_red', 'wf2_awn_blue', 'wf2_wool_mustard', 'wf2_awn_green', 'wf2_wool_teal', 'wf2_plank_light']
    for i in range(6):
        x = -w / 2 + 1.0 + i * 1.5
        tilt = rnd.uniform(-6, 6)
        sl = 5.6
        box(nm('ski'), (0.32, 0.12, sl), loc=(x, -0.2, sl / 2 + 0.3), key=cols[i], rot=(10, 0, tilt), bev=0.05)
        # upturned tip
        box(nm('tip'), (0.32, 0.5, 0.2), loc=(x, -0.2 - 0.25, sl + 0.4), key=cols[i], rot=(40, 0, tilt), bev=0.06)
        # pole beside it
        cyl(nm('pl'), 0.06, 5.0, loc=(x + 0.5, 0.4, 0.3), key='iron', verts=5, rot=(6, 0, tilt))
        torus(nm('bask'), 0.3, 0.05, loc=(x + 0.5, 0.4, 0.9), key='wf2_plank_grey', segs=8, rsegs=3, rot=(90, 0, 0))
    ground_frost(0, 0, w / 2 + 0.3, d / 2 + 0.3, seed=1)
    return finalize('C03_01_ski_rack_01', smooth_angle=35)


# ================================================================ C04 snowmen
def _snowman(seed, total_h, name, hat, has_broom, has_lantern):
    reset()
    rnd = random.Random(seed)
    # three stacked snowballs sized to total height
    r0 = total_h * 0.26
    r1 = total_h * 0.20
    r2 = total_h * 0.15
    z0 = r0
    z1 = z0 + r0 * 0.8 + r1
    z2 = z1 + r1 * 0.8 + r2
    ball(nm('b0'), r0, (0, 0, z0), SNOW, segs=16, rings=10, scale=(1, 1, 0.95))
    ball(nm('b1'), r1, (0, 0, z1), SNOW, segs=16, rings=10, scale=(1, 1, 0.95))
    ball(nm('b2'), r2, (0, 0, z2), SNOW, segs=16, rings=10)
    # face: coal eyes, carrot nose, coal-button smile
    for s in (-1, 1):
        ball(nm('eye'), 0.14, (s * r2 * 0.35, -r2 * 0.85, z2 + r2 * 0.25), 'wf2_coal', segs=6, rings=4)
    cyl(nm('nose'), 0.18, r2 * 0.9, loc=(0, -r2 * 0.8, z2), key='wf2_carrot', verts=7, rot=(-90, 0, 0), r2=0.02)
    for i in range(5):
        a = math.radians(-50 + i * 25)
        ball(nm('sm'), 0.08, (math.sin(a) * r2 * 0.5, -r2 * 0.9, z2 - r2 * 0.25 + (1 - math.cos(a)) * 0.1), 'wf2_coal', segs=5, rings=3)
    # coal buttons down the middle ball
    for i in range(3):
        ball(nm('bt'), 0.12, (0, -r1 * 0.95, z1 + r1 * 0.4 - i * r1 * 0.4), 'wf2_coal', segs=5, rings=3)
    # stick arms
    for s in (-1, 1):
        tube(nm('arm'), [(s * r1 * 0.8, 0, z1), (s * (r1 + 1.6), 0.1, z1 + 1.0), (s * (r1 + 2.4), 0.2, z1 + 1.6)], 0.09, 'wf2_bark', res=4)
        for k in range(2):
            tube(nm('tw'), [(s * (r1 + 1.6 + k * 0.4), 0.1, z1 + 1.0 + k * 0.3), (s * (r1 + 2.0 + k * 0.5), 0.3, z1 + 1.8 + k * 0.4)], 0.05, 'wf2_bark', res=4)
    # scarf
    sc = torus(nm('scf'), r2 * 0.95, 0.22, loc=(0, 0, z1 + r1 * 0.65), key='wf2_wool_red', segs=14, rsegs=5)
    sc.scale = (1, 1, 0.6)
    box(nm('scfend'), (0.5, 0.15, 1.6), loc=(r2 * 0.6, -r2 * 0.7, z1 - 0.2), key='wf2_wool_red', rot=(0, 10, 0))
    # hat
    if hat == 'top':
        cyl(nm('brim'), r2 * 1.15, 0.12, loc=(0, 0, z2 + r2 * 0.8), key='wf2_coal', verts=14)
        cyl(nm('top'), r2 * 0.7, r2 * 1.3, loc=(0, 0, z2 + r2 * 0.85), key='wf2_coal', verts=14)
        torus(nm('band'), r2 * 0.72, 0.08, loc=(0, 0, z2 + r2 * 1.0), key='wf2_wool_red', segs=12, rsegs=4)
    else:  # bobble beanie
        ball(nm('beanie'), r2 * 0.95, (0, 0, z2 + r2 * 0.55), 'wf2_wool_teal', segs=12, rings=7, scale=(1, 1, 0.8))
        box(nm('cuff'), (r2 * 1.9, r2 * 1.9, 0.4), loc=(0, 0, z2 + r2 * 0.45), key='wf2_awn_cream', bev=0.15)
        ball(nm('pom'), 0.3, (0, 0, z2 + r2 * 1.35), 'wf2_awn_cream', segs=7, rings=5)
    if has_broom:
        bx = r1 + 2.0
        cyl(nm('bh'), 0.1, 4.5, loc=(bx, 0.3, 0), key='wf2_timber', verts=6, rot=(14, 0, 0))
        for i in range(7):
            cyl(nm('br'), 0.04, 1.4, loc=(bx + 1.1 + (i - 3) * 0.08, 0.9, 0.1), key='grass_dry', verts=4, rot=(70, 0, (i - 3) * 6))
    if has_lantern:
        lantern(-(r1 + 2.4), 0.2, z1 + 0.6, r=0.35, h=0.9, seed=seed)
    ground_frost(0, 0, r0 + 0.6, r0 + 0.6, n=8, seed=seed)
    return finalize(name, smooth_angle=40)


def snowman_01():
    """C04_01 ~6 high small snowman, bobble beanie, broom."""
    return _snowman(401, 6.0, 'C04_01_snowman_01', 'beanie', True, False)


def snowman_02():
    """C04_02 ~12 high tall snowman, top hat, holding a lantern."""
    return _snowman(402, 12.0, 'C04_02_snowman_02', 'top', False, True)


# ================================================================ C05 ice blocks / sculptures
def ice_block_01():
    """C05_01 ~8 stack of cut ice blocks with frost edges, roped, a pick leaning on them."""
    reset()
    rnd = random.Random(501)
    bw = 2.6
    # pyramid stack of translucent blocks
    layout = [(-1, 0), (0, 0), (1, 0), (-0.5, 1), (0.5, 1), (0, 2)]
    for (gx, gz) in layout:
        x = gx * bw
        z = gz * bw + bw / 2
        k = rnd.choice(['wf2_ice', 'wf2_ice_blue', 'wf2_ice'])
        box(nm('ib'), (bw - 0.1, bw - 0.1, bw - 0.1), loc=(x, 0, z), key=k, bev=0.12)
        # frost rime edges
        box(nm('rm'), (bw + 0.08, bw + 0.08, 0.18), loc=(x, 0, z + bw / 2 - 0.1), key=SNOW, bev=0.05)
    # saw marks / grooves hinted by thin darker seams between layers handled by bevel gaps
    # rope lashing over the stack
    tube(nm('rope'), [(-bw * 1.4, 0, 1.0), (0, 0, bw * 2 + 0.4), (bw * 1.4, 0, 1.0)], 0.1, 'rope', res=5)
    # ice pick leaning
    cyl(nm('ph'), 0.08, 4.0, loc=(bw * 1.6, 0.6, 0), key='wf2_timber', verts=5, rot=(18, 0, 0))
    box(nm('pk'), (1.4, 0.18, 0.3), loc=(bw * 1.6 + 1.2, 0.0, 3.8), key='iron', rot=(0, 0, 20), bev=0.05)
    ground_frost(0, 0, bw * 2, bw, n=7, seed=5)
    return finalize('C05_01_ice_block_01', smooth_angle=30)


def ice_block_02():
    """C05_02 ~10 big clear ice block with a frozen fish suspended inside."""
    reset()
    rnd = random.Random(502)
    W, D, H = 5.0, 4.0, 9.0
    # plinth of snow/stone
    box(nm('pl'), (W + 1.2, D + 1.2, 1.0), loc=(0, 0, 0.5), key='wf2_stone', bev=0.1)
    snow_pillow(0, 0, W + 1.4, D + 1.4, 1.0, h=0.4, seed=1)
    # the clear block
    box(nm('blk'), (W, D, H), loc=(0, 0, 1.0 + H / 2), key='wf2_ice', bev=0.25)
    # internal cracks (thin blue slivers)
    for i in range(5):
        box(nm('cr'), (0.08, D * 0.7, rnd.uniform(2.0, 4.0)), loc=(rnd.uniform(-W / 3, W / 3), rnd.uniform(-0.5, 0.5), 1.0 + rnd.uniform(2, H - 2)), key='wf2_ice_blue', rot=(0, rnd.uniform(-20, 20), 0))
    # the fish, tilted, inside
    fz = 1.0 + H * 0.5
    ball(nm('fish'), 1.3, (0, 0, fz), 'wf2_fish', segs=10, rings=6, scale=(1.8, 0.5, 0.9))
    # tail
    box(nm('tail'), (0.1, 0.9, 1.3), loc=(-2.2, 0, fz), key='wf2_fish', rot=(0, 24, 0), bev=0.1)
    ball(nm('eye'), 0.16, (2.0, 0.35, fz + 0.3), 'wf2_coal', segs=6, rings=4)
    # frost on top
    snow_pillow(0, 0, W - 0.3, D - 0.3, 1.0 + H - 0.1, h=0.4, seed=2)
    icicles(-W / 2, W / 2, -D / 2 - 0.1, 1.0 + H - 0.2, lo=0.3, hi=0.8, seed=3, prob=0.6)
    ground_frost(0, 0, W, D, n=6, seed=6)
    return finalize('C05_02_ice_block_02', smooth_angle=28)


def ice_block_03():
    """C05_03 ~12 ice sculpture of a leaping stag on an ice plinth."""
    reset()
    rnd = random.Random(503)
    K = 'wf2_ice'
    KB = 'wf2_ice_blue'
    # octagonal ice plinth
    lathe(nm('pl'), [(0, 0), (2.6, 0), (2.6, 2.0), (2.2, 2.2), (2.2, 2.4)], loc=(0, 0, 0), key=KB, segs=8)
    snow_pillow(0, 0, 4.6, 4.6, 2.4, h=0.35, seed=1)
    bz = 2.6
    # body
    ball(nm('body'), 1.5, (0, 0, bz + 3.4), K, segs=10, rings=7, scale=(1.0, 2.1, 1.1))
    # chest/neck rising forward (-Y)
    tube(nm('neck'), [(0, -1.8, bz + 3.6), (0, -3.0, bz + 5.2), (0, -3.4, bz + 6.4)], 0.7, K, res=6, taper=[1.1, 0.8, 0.55])
    ball(nm('head'), 0.65, (0, -3.6, bz + 6.9), K, segs=8, rings=6, scale=(0.9, 1.4, 0.9))
    # antlers
    for s in (-1, 1):
        tube(nm('ant'), [(s * 0.3, -3.6, bz + 7.4), (s * 0.9, -3.3, bz + 8.6), (s * 1.4, -3.8, bz + 9.6)], 0.1, KB, res=4)
        for k in range(2):
            tube(nm('pr'), [(s * (0.6 + k * 0.3), -3.4, bz + 8.0 + k * 0.6), (s * (1.2 + k * 0.4), -3.0, bz + 8.8 + k * 0.7)], 0.07, KB, res=4)
    # legs: front reaching forward, back pushing off (leaping)
    for (lx, ly, ang) in ((-0.7, -1.4, -40), (0.7, -1.4, -40), (-0.7, 1.4, 35), (0.7, 1.4, 35)):
        tube(nm('leg'), [(lx, ly, bz + 3.0), (lx + 0, ly + math.sin(math.radians(ang)) * 1.5, bz + 0.6), (lx, ly + math.sin(math.radians(ang)) * 2.4, bz + 0.1)], 0.3, K, res=5, taper=[1.0, 0.7, 0.5])
    # tail
    tube(nm('tl'), [(0, 2.0, bz + 3.6), (0, 2.8, bz + 3.0)], 0.2, K, res=4, taper=[1, 0.4])
    ground_frost(0, 0, 3.0, 3.0, n=6, seed=7)
    return finalize('C05_03_ice_block_03', smooth_angle=34)


# ================================================================ C06 frozen dock
def frozen_dock_01():
    """C06_01 ~30x8x4 lake-edge wooden dock, frosted planks, pilings, rope, ice crust under and around it."""
    reset()
    rnd = random.Random(601)
    L, W = 30.0, 8.0
    deck_z = 3.2
    # ice sheet underneath / around the lake edge
    box(nm('ice'), (L + 10, W + 14, 0.6), loc=(0, 3.0, 0.3), key='wf2_ice', bev=0.2)
    for i in range(10):      # cracked ice facets
        box(nm('icf'), (rnd.uniform(3, 6), rnd.uniform(3, 6), 0.1), loc=(rnd.uniform(-L / 2, L / 2), rnd.uniform(-2, 8), 0.62), key=rnd.choice(['wf2_ice_blue', 'wf2_ice']), rot=(0, 0, rnd.uniform(0, 90)))
    # pilings
    for x in [i for i in range(int(-L / 2 + 1), int(L / 2), 5)]:
        for sy in (-1, 1):
            py = sy * (W / 2 - 0.8)
            cyl(nm('pil'), 0.5, deck_z + 1.4, loc=(x, py, 0.4), key='wf2_bark', verts=8)
            snow_pillow(x, py, 1.3, 1.3, deck_z + 1.4, h=0.3, seed=x)
            icicles(x - 0.5, x + 0.5, py, deck_z + 1.0, n=2, lo=0.4, hi=1.0, seed=x, prob=0.9)
    # deck beams + planks running along L
    for sy in (-1, 1):
        box(nm('str'), (L, 0.4, 0.5), loc=(0, sy * (W / 2 - 0.8), deck_z - 0.3), key='wf2_timber_dark')
    nplk = int(L / 1.1)
    for i in range(nplk):
        x = -L / 2 + L * (i + 0.5) / nplk
        gap = rnd.uniform(0, 0.05)
        box(nm('plk'), (L / nplk - 0.08, W - 1.0, 0.3), loc=(x, 0, deck_z), key=rnd.choice(['wf2_plank_grey', 'wf2_plank', 'wf2_plank_grey']))
    # thin snow dusting on the deck (patchy)
    for i in range(14):
        snow_drift(rnd.uniform(-L / 2, L / 2), rnd.uniform(-W / 2 + 1, W / 2 - 1), rnd.uniform(0.6, 1.3), seed=i, scale=(1.6, 1.3, 0.22))
    # a couple of bollards with coiled rope
    for x in (-L / 2 + 2, L / 2 - 2):
        cyl(nm('bol'), 0.6, 1.6, loc=(x, 0, deck_z + 0.15), key='wf2_timber', verts=8)
        torus(nm('co'), 0.8, 0.12, loc=(x, 0, deck_z + 0.5), key='rope', segs=14, rsegs=4)
    ground_frost(0, -W / 2 - 1, L / 2, 2.0, n=8, seed=6)
    U.marker('mk_conn', (0, -W / 2 + 0.5, deck_z + 0.3))
    return finalize('C06_01_frozen_dock_01', smooth_angle=35)


# ================================================================ C07 sleds
def sled_01():
    """C07_01 wooden dog sled piled with fur bundles and lashed rope, curved front runners."""
    reset()
    rnd = random.Random(701)
    L, W = 10.0, 3.2
    rz = 1.2
    # two curved runners
    for sy in (-1, 1):
        y = sy * (W / 2 - 0.3)
        tube(nm('run'), [(-L / 2, y, 0.3), (L / 2 - 1.5, y, 0.3), (L / 2, y, 0.3), (L / 2 + 0.8, y, 1.6)], 0.22, 'wf2_plank_light', res=5)
        # stanchions up to the bed
        for i in range(4):
            x = -L / 2 + 1.0 + i * (L - 2) / 3
            cyl(nm('st'), 0.14, rz, loc=(x, y, 0.3), key='wf2_timber', verts=5)
    # slatted bed
    nb = int(L / 0.9)
    for i in range(nb):
        x = -L / 2 + 0.6 + i * (L - 1.0) / nb
        box(nm('bd'), (0.5, W - 0.4, 0.14), loc=(x, 0, rz + 0.3), key='wf2_plank')
    # upright handlebar at the back
    for sy in (-1, 1):
        tube(nm('hb'), [(-L / 2 + 0.3, sy * (W / 2 - 0.3), rz + 0.3), (-L / 2 - 0.3, sy * (W / 2 - 0.3), rz + 2.4)], 0.12, 'wf2_timber', res=4)
    box(nm('hbar'), (0.3, W, 0.2), loc=(-L / 2 - 0.3, 0, rz + 2.4), key='wf2_timber', bev=0.06)
    # fur bundles as the load
    for i in range(3):
        ball(nm('fur'), 1.1, (-1.5 + i * 2.2, 0, rz + 1.1), rnd.choice(['wf2_fur', 'wf2_fur_dark']), segs=9, rings=6, scale=(1.4, 1.0, 0.8))
    # lashing rope over the load
    tube(nm('lr'), [(-3.0, -W / 2, rz + 0.4), (-2.0, 0, rz + 2.0), (-1.0, W / 2, rz + 0.4)], 0.07, 'rope', res=4)
    tube(nm('lr2'), [(2.0, -W / 2, rz + 0.4), (3.0, 0, rz + 2.0), (4.0, W / 2, rz + 0.4)], 0.07, 'rope', res=4)
    snow_drift(0, 0, 1.0, seed=1, scale=(3.0, 1.2, 0.2))
    ground_frost(0, 0, L / 2, W / 2 + 0.5, n=7, seed=7)
    return finalize('C07_01_sled_01', smooth_angle=35)


def sled_02():
    """C07_02 small child's toboggan: a single curved plank sled with a short pull rope."""
    reset()
    L, W = 6.0, 2.4
    # curved-up front plank body
    tube(nm('body'), [(-L / 2, 0, 0.5), (L / 2 - 1.2, 0, 0.5), (L / 2, 0, 0.6), (L / 2 + 0.7, 0, 1.5)], 1.0, 'wf2_plank_light', res=6, taper=[1, 1, 1, 0.9])
    # slat seams on top
    for i in range(5):
        x = -L / 2 + 0.6 + i * 1.0
        box(nm('sl'), (0.1, W, 0.06), loc=(x, 0, 1.02), key='wf2_timber')
    # two runner strips underneath
    for sy in (-1, 1):
        box(nm('ru'), (L - 0.5, 0.25, 0.14), loc=(-0.2, sy * (W / 2 - 0.3), 0.14), key='wf2_timber_dark')
    # pull rope from the front tip
    tube(nm('pr'), [(L / 2 + 0.7, 0, 1.5), (L / 2 + 2.2, 0.3, 0.8), (L / 2 + 3.2, -0.2, 0.3)], 0.07, 'rope', res=4)
    snow_drift(0, 0, 0.9, seed=1, scale=(2.6, 1.3, 0.2))
    ground_frost(0, 0, L / 2, W / 2 + 0.3, n=6, seed=2)
    return finalize('C07_02_sled_02', smooth_angle=36)


# ================================================================ C08 frozen boats
def _hull(name, L, W, H, wz, bow_axis, key_out, key_in, keel='wf2_timber_dark', rnd=None):
    """Clean lofted boat hull: a smooth tapered shell, pointed bow, open top, floor + ribs.
    bow_axis: 'x' (bow at -x) or 'y' (bow at -y, i.e. front -Y). Built around origin, floor at wz."""
    import bmesh
    from kitlib import _obj_from_bm
    bm = bmesh.new()
    nseg = 11
    nz = 4
    rings = []
    for j in range(nz + 1):
        tz = j / nz
        z = wz - 0.6 + (H + 0.6) * tz
        beam = (0.35 + 0.65 * tz)        # widens upward
        ring = []
        for i in range(nseg + 1):
            t = i / nseg                 # 0..1 along the length
            # length profile: full amidships, pointed at bow, square-ish at stern
            along = -L / 2 + t * L
            prof = math.sin(math.pi * t) ** 0.6
            half = (W / 2) * prof * beam
            # pointed bow: pinch the first 25%
            if t < 0.22:
                half *= (t / 0.22) ** 0.7
            s = 1 if i <= nseg // 2 else -1
            # one side then the other — build as a closed loop
            ring.append((along, s * half, z))
        rings.append(ring)
    # make verts
    vrings = [[bm.verts.new((a, b, c) if bow_axis == 'x' else (b, a, c)) for (a, b, c) in r] for r in rings]
    for j in range(nz):
        A, B = vrings[j], vrings[j + 1]
        for i in range(nseg):
            bm.faces.new((A[i], A[i + 1], B[i + 1], B[i]))
    # cap the bottom
    bm.faces.new(list(reversed(vrings[0])))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj_from_bm(name, bm, key_out)
    # keel strip
    if bow_axis == 'x':
        box(nm('keel'), (L, 0.4, 0.5), loc=(0, 0, wz - 0.7), key=keel)
        box(nm('flr'), (L - 2.5, W - 2.0, 0.3), loc=(0, 0, wz + 0.1), key=key_in)
    else:
        box(nm('keel'), (0.4, L, 0.5), loc=(0, 0, wz - 0.7), key=keel)
        box(nm('flr'), (W - 2.0, L - 2.5, 0.3), loc=(0, 0, wz + 0.1), key=key_in)
    return o


def frozen_boat_01():
    """C08_01 ~14x6 rowboat stuck in lake ice, clean frosted hull, two thwarts, oars, ice crust."""
    reset()
    rnd = random.Random(801)
    L, W, H = 14.0, 5.6, 4.2
    wz = 1.4
    box(nm('ice'), (L + 5, W + 5, 0.8), loc=(0, 0, 0.4), key='wf2_ice', bev=0.2)
    for i in range(6):
        box(nm('icf'), (rnd.uniform(2.5, 4), rnd.uniform(2.5, 4), 0.12), loc=(rnd.uniform(-L / 2, L / 2), rnd.uniform(-W, W), 0.82), key='wf2_ice_blue', rot=(0, 0, rnd.uniform(0, 90)))
    _hull('hull', L, W, H, wz, 'x', 'wf2_plank', 'wf2_timber_dark', rnd=rnd)
    # gunwale rail seated at the shell top
    for sy in (-1, 1):
        for i in range(6):
            t = (i + 0.5) / 6
            x = -L / 2 + t * L
            prof = math.sin(math.pi * t) ** 0.6
            if t < 0.22:
                prof *= (t / 0.22) ** 0.7
            yw = (W / 2) * prof
            box(nm('gw'), (L / 6, 0.4, 0.4), loc=(x, sy * yw, wz + H - 0.4), key='wf2_plank_grey', rot=(0, 0, sy * 10))
    # thwarts (benches) spanning the interior
    for x in (-3.2, 2.8):
        box(nm('th'), (1.0, W * 0.55, 0.25), loc=(x, 0, wz + 2.0), key='wf2_plank')
    # oars resting across the gunwale
    for i, y in enumerate((-1.2, 1.2)):
        cyl(nm('oar'), 0.12, 8.5, loc=(0.5, y, wz + 2.6), key='wf2_timber', verts=5, rot=(0, 90, 12 - i * 24))
        box(nm('blade'), (1.3, 0.12, 0.6), loc=(0.5 + (4.0 if i == 0 else -4.0), y, wz + 2.6), key='wf2_plank_light', bev=0.08)
    snow_drift(0, 0, 1.0, seed=1, scale=(5.0, 2.2, 0.22))
    for sy in (-1, 1):
        icicles(-L / 2 + 3, L / 2 - 3, sy * W * 0.4, wz + 0.2, lo=0.4, hi=1.0, seed=sy, prob=0.5)
    ground_frost(0, 0, L / 2 + 1, W / 2 + 1, n=6, seed=8)
    return finalize('C08_01_frozen_boat_01', smooth_angle=34)


def frozen_boat_02():
    """C08_02 ~20 small sailing boat frozen in with a snapped mast and a torn, frosted sail."""
    reset()
    rnd = random.Random(802)
    L, W, H = 20.0, 6.0, 5.0
    box(nm('ice'), (L + 8, W + 8, 0.9), loc=(0, 0, 0.45), key='wf2_ice', bev=0.2)
    for i in range(8):
        box(nm('icf'), (rnd.uniform(3, 6), rnd.uniform(3, 6), 0.12), loc=(rnd.uniform(-L / 2, L / 2), rnd.uniform(-W, W), 0.92), key='wf2_ice_blue', rot=(0, 0, rnd.uniform(0, 90)))
    wz = 1.6
    _hull('hull', L, W, H, wz, 'y', 'wf2_plank', 'wf2_timber_dark', rnd=rnd)
    # gunwale rail along the top edge
    for sx in (-1, 1):
        for i in range(8):
            t = (i + 0.5) / 8
            y = -L / 2 + t * L
            prof = math.sin(math.pi * t) ** 0.6
            if t < 0.22:
                prof *= (t / 0.22) ** 0.7
            xw = (W / 2) * prof
            box(nm('gw'), (0.4, L / 8, 0.4), loc=(sx * xw, y, wz + H - 0.6), key='wf2_plank_grey', rot=(0, 0, sx * 10))
    # mast, snapped: lower stub + broken upper leaning
    cyl(nm('mast'), 0.35, 6.0, loc=(0, -1.0, wz + 0.3), key='wf2_timber')
    box(nm('break'), (0.7, 0.7, 0.5), loc=(0, -1.0, wz + 6.0), key='wf2_timber_dark')
    tube(nm('upper'), [(0, -1.0, wz + 6.0), (1.5, -1.5, wz + 9.0), (3.0, -2.0, wz + 10.5)], 0.28, 'wf2_timber', res=4, taper=[1, 0.8, 0.6])
    # torn sail hanging off the broken mast (frosted canvas)
    box(nm('sail'), (0.1, 5.0, 5.5), loc=(0.2, 0.8, wz + 4.5), key='sail', rot=(0, 6, 0))
    box(nm('tear'), (0.12, 1.4, 2.0), loc=(0.2, 3.0, wz + 2.6), key='wf2_ice', rot=(0, 6, 18))  # frozen torn flap
    # frost + icicles along rails
    snow_drift(0, 0, 1.2, seed=1, scale=(2.4, 6.0, 0.22))
    for sx in (-1, 1):
        icicles(-2, 2, sx * W * 0.35, wz + 0.2, n=4, lo=0.4, hi=1.1, seed=sx, prob=0.6)
    ground_frost(0, 0, W / 2 + 1, L / 2 + 1, n=6, seed=8)
    return finalize('C08_02_frozen_boat_02', smooth_angle=34)


# ================================================================ C09 frozen waterfall
def frozen_waterfall_01():
    """C09_01 ~30 wide x 30 tall: rock backing with columns of frozen cascade, blue-white translucent ice,
    snow on the ledges, icicle curtains; base at z=0."""
    reset()
    rnd = random.Random(901)
    W, H = 30.0, 30.0
    ICE = ('wf2_ice', 'wf2_ice_blue', 'wf2_ice', 'wf2_ice_deep')
    ROCK = ('stone_dark', 'cliff_b', 'stone_dark')
    # rock back wall, stepped ledges
    for k in range(6):
        z0 = k * 5.0
        depth = 5.0 - k * 0.5
        wd = W - k * 1.0
        box(nm('rk'), (wd, depth, 5.2), loc=(0, 3.0 - k * 0.6, z0 + 2.6), key=ROCK[k % 3], bev=0.2)
        # rock facets
        for i in range(int(wd / 3)):
            x = -wd / 2 + rnd.uniform(0, wd)
            box(nm('fac'), (rnd.uniform(1.5, 3.0), 0.6, rnd.uniform(2, 4)), loc=(x, 3.0 - k * 0.6 - depth / 2 - 0.3, z0 + rnd.uniform(1, 4)), key=rnd.choice(ROCK), rot=(0, rnd.uniform(-15, 15), 0))
        # snow on each ledge front
        snow_pillow(0, 3.0 - k * 0.6 - depth / 2, wd - 1, 1.6, z0 + 5.2, h=0.6, seed=k)
    # frozen cascade: several big ice columns of varied width, bulging, from top to base
    cols = [(-10, 7), (-3, 9), (4, 8), (11, 6)]
    for ci, (cx, cw) in enumerate(cols):
        for seg in range(6):
            z = seg * 5.0
            bulge = cw * (0.55 + 0.12 * math.sin(seg * 1.3 + ci))
            yy = -2.5 - seg * 0.15
            lathe(nm('col'), [(0, 0), (bulge * 0.5, 0), (bulge * 0.6, 2.5), (bulge * 0.5, 5.0)], loc=(cx + rnd.uniform(-0.4, 0.4), yy, z), key=ICE[(seg + ci) % 4], segs=7, sy=0.5)
        # smooth frozen sheet over the column front
        box(nm('sheet'), (cw, 0.8, H), loc=(cx, -3.2, H / 2), key=ICE[ci % 4], bev=0.4)
    # icicle curtains hanging from each ledge
    for k in range(6):
        z0 = k * 5.0 + 5.0
        icicles(-W / 2 + 2, W / 2 - 2, -3.6, z0, lo=0.8, hi=3.0, seed=k, prob=0.7, key=rnd.choice(['wf2_ice', 'wf2_ice_blue']))
    # frozen plunge pool / mounded ice at the base
    lathe(nm('pool'), [(0, 0), (12, 0.2), (10, 1.4), (6, 2.2), (0, 2.5)], loc=(0, -6.0, 0), key='wf2_ice', segs=20, sy=0.6)
    for i in range(10):
        a = rnd.uniform(0, 6.28); dd = rnd.uniform(3, 10)
        ball(nm('chunk'), rnd.uniform(0.8, 1.8), (math.cos(a) * dd, -6.0 + math.sin(a) * dd * 0.5, 0.6), rnd.choice(ICE), segs=7, rings=4, scale=(1.3, 1.0, 0.7))
    # base snow apron
    for i in range(16):
        snow_drift(rnd.uniform(-W / 2, W / 2), rnd.uniform(-9, -1), rnd.uniform(1.2, 2.5), seed=i, scale=(1.6, 1.3, 0.4))
    return finalize('C09_01_frozen_waterfall_01', smooth_angle=30)


# ---- batches ----------------------------------------------------------------------
BATCHES = {
    'props_a': ('v4_alpine', [
        ('C02_01_winter_stall_01', winter_stall_01, (1.0, -1.2, 0.4)),
        ('C02_02_winter_stall_02', winter_stall_02, (1.0, -1.2, 0.4)),
        ('C02_03_winter_stall_03', winter_stall_03, (1.0, -1.2, 0.4)),
        ('C03_01_ski_rack_01', ski_rack_01, (1.0, -1.1, 0.4)),
        ('C04_01_snowman_01', snowman_01, (0.6, -1.2, 0.35)),
        ('C04_02_snowman_02', snowman_02, (0.6, -1.2, 0.35)),
        ('C05_01_ice_block_01', ice_block_01, (1.0, -1.1, 0.4)),
        ('C05_02_ice_block_02', ice_block_02, (0.8, -1.2, 0.4)),
        ('C05_03_ice_block_03', ice_block_03, (0.7, -1.2, 0.4)),
    ]),
    'props_b': ('v4_alpine', [
        ('C06_01_frozen_dock_01', frozen_dock_01, (0.8, -1.0, 0.5)),
        ('C07_01_sled_01', sled_01, (1.0, -1.1, 0.4)),
        ('C07_02_sled_02', sled_02, (1.0, -1.1, 0.4)),
        ('C08_01_frozen_boat_01', frozen_boat_01, (0.9, -1.0, 0.45)),
        ('C08_02_frozen_boat_02', frozen_boat_02, (1.0, -0.6, 0.5)),
        ('C09_01_frozen_waterfall_01', frozen_waterfall_01, (0.4, -1.3, 0.45)),
    ]),
}
