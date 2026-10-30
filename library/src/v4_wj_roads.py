"""v4_wj_roads - worker wj, F08 road pieces (bridges, signposts, milestones, gate arches, shrines).
Improves on roads.py / between.py. 1 unit = 1 stud, Z up, front faces -Y.
Bridges span along X; deck crosses Y. finalize moves origin to bottom centre.
"""
import math, random
import bmesh
from mathutils import Vector
import kitlib
from kitlib import (reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, bevel,
                    top_paint, flame, _obj_from_bm)
import v4util
from arch import F, gable_roof, railing, wall_lantern, nm
from nature import rock, blob

PAL = kitlib.PAL
# worker palette keys (prefixed wj_)
PAL['wj_cob_a']   = ((150, 142, 130), 'Cobblestone', 0.0, 0.90, 0)
PAL['wj_cob_b']   = ((132, 126, 116), 'Cobblestone', 0.0, 0.90, 0)
PAL['wj_cob_c']   = ((166, 156, 140), 'Cobblestone', 0.0, 0.90, 0)
PAL['wj_ashlar']  = ((190, 182, 164), 'Limestone',   0.0, 0.85, 0)
PAL['wj_ashlar_d']= ((156, 148, 132), 'Limestone',   0.0, 0.88, 0)
PAL['wj_stone']   = ((140, 134, 124), 'Cobblestone', 0.0, 0.90, 0)
PAL['wj_stone_d'] = ((104, 100, 92),  'Slate',       0.0, 0.92, 0)
PAL['wj_plank']   = ((138, 100, 62),  'WoodPlanks',  0.0, 0.82, 0)
PAL['wj_plank_b'] = ((120, 86, 54),   'WoodPlanks',  0.0, 0.85, 0)
PAL['wj_timber']  = ((92, 64, 42),    'Wood',        0.0, 0.88, 0)
PAL['wj_timber_d']= ((70, 48, 32),    'Wood',        0.0, 0.92, 0)
PAL['wj_wood_old']= ((112, 96, 76),   'WoodPlanks',  0.0, 0.95, 0)
PAL['wj_rope']    = ((178, 152, 104), 'Fabric',      0.0, 1.00, 0)
PAL['wj_iron']    = ((44, 42, 40),    'Metal',       0.80, 0.45, 0)
PAL['wj_moss']    = ((88, 112, 52),   'Grass',       0.0, 1.00, 0)
PAL['wj_ivy']     = ((60, 92, 44),    'LeafyGrass',  0.0, 0.95, 0)
PAL['wj_banner_r']= ((150, 44, 42),   'Fabric',      0.0, 0.95, 0)
PAL['wj_banner_b']= ((48, 70, 128),   'Fabric',      0.0, 0.95, 0)
PAL['wj_glass_lit']=((244, 186, 102), 'Glass',       0.0, 0.20, 0.42)
PAL['wj_gold']    = ((206, 166, 78),  'Metal',       1.00, 0.30, 0)

STONE_KEYS = ['wj_cob_a', 'wj_cob_b', 'wj_cob_c', 'wj_stone']
PLANK_KEYS = ['wj_plank', 'wj_plank_b', 'wj_wood_old']


# ---------------------------------------------------------------- helpers
def setts(prefix, x0, x1, y0, y1, z, rnd, keys=None, sx=1.9, sy=1.7, t=0.3, slopefn=None):
    """Lay a grid of bevelled cobble setts over a deck area. slopefn(x)->(z,angle_deg)."""
    keys = keys or STONE_KEYS
    nx = max(1, int((x1 - x0) / sx)); ny = max(1, int((y1 - y0) / sy))
    dx = (x1 - x0) / nx; dy = (y1 - y0) / ny
    for i in range(nx):
        x = x0 + dx * (i + 0.5)
        zz, ang = (slopefn(x) if slopefn else (z, 0.0))
        for j in range(ny):
            y = y0 + dy * (j + 0.5) + ((dy * 0.5) if i % 2 else 0) * 0.0
            box(f'{prefix}{i}_{j}', (dx * rnd.uniform(0.82, 0.92), dy * rnd.uniform(0.82, 0.92), t),
                loc=(x, y + rnd.uniform(-0.05, 0.05), zz + t / 2 + rnd.uniform(-0.03, 0.03)),
                key=rnd.choice(keys), rot=(0, -ang, rnd.uniform(-2.5, 2.5)), bev=0.08, segs=1)


def planks_x(prefix, x0, x1, y0, y1, z, rnd, keys=None, pw=1.3, t=0.3, slopefn=None, gap=0.08):
    """Deck planks running along X (across the bridge), laid in rows along Y."""
    keys = keys or PLANK_KEYS
    ny = max(1, int((y1 - y0) / pw)); dy = (y1 - y0) / ny
    for j in range(ny):
        y = y0 + dy * (j + 0.5)
        box(f'{prefix}{j}', (x1 - x0 + rnd.uniform(-0.2, 0.1), dy - gap, t),
            loc=((x0 + x1) / 2, y, z + t / 2 + rnd.uniform(-0.03, 0.02)),
            key=rnd.choice(keys), rot=(rnd.uniform(-0.6, 0.6), 0, 0), bev=0.04, segs=1)


def parapet(prefix, x0, x1, side_y, z, rnd, key='wj_stone', cap='wj_ashlar', h=2.6, t=1.1, slopefn=None, coping=True):
    """Low stone parapet wall running along X at y=side_y, with a coping course."""
    n = max(4, int((x1 - x0) / 2.4)); dx = (x1 - x0) / n
    for i in range(n):
        x = x0 + dx * (i + 0.5)
        zz, ang = (slopefn(x) if slopefn else (z, 0.0))
        box(f'{prefix}w{i}', (dx + 0.06, t, h), loc=(x, side_y, zz + h / 2),
            key=rnd.choice([key, 'wj_stone_d', key]), rot=(0, -ang, 0), bev=0.06, segs=1)
        if coping:
            box(f'{prefix}c{i}', (dx + 0.14, t + 0.5, 0.42), loc=(x, side_y, zz + h + 0.18),
                key=cap, rot=(0, -ang, 0), bev=0.1, segs=2)


def lamp_post(prefix, x, y, z, h=5.2, key='wj_iron'):
    """Small iron lamp post with a glowing lantern."""
    cyl(f'{prefix}b', 0.34, 0.5, loc=(x, y, z), key='wj_ashlar', verts=12, bev=0.05)
    cyl(f'{prefix}p', 0.16, h, loc=(x, y, z + 0.4), key=key, verts=10)
    for k in range(3):
        a = math.radians(120 * k)
        tube(f'{prefix}s{k}', [(x, y, z + h * 0.78), (x + math.cos(a) * 0.5, y + math.sin(a) * 0.5, z + h + 0.1)],
             0.06, key, res=3)
    box(f'{prefix}cap', (0.7, 0.7, 0.14), loc=(x, y, z + h + 0.1), key=key)
    lathe(f'{prefix}g', [(0.0, 0.0), (0.42, 0.0), (0.42, 1.0), (0.2, 1.3), (0.0, 1.35)],
          loc=(x, y, z + h + 0.24), key='wj_glass_lit', segs=8)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f'{prefix}e{sx}{sy}', (0.06, 0.06, 1.05), loc=(x + sx * 0.3, y + sy * 0.3, z + h + 0.74), key=key)
    lathe(f'{prefix}t', [(0.5, 0.0), (0.1, 0.5), (0.0, 0.6)], loc=(x, y, z + h + 1.6), key=key, segs=8)


def abutment(prefix, x, y0, y1, z_top, key='wj_stone', depth=4.0, sink=5.0):
    """Stone abutment block sinking into the ground at a bridge end."""
    box(f'{prefix}', (depth, y1 - y0, z_top + sink), loc=(x, (y0 + y1) / 2, (z_top - sink) / 2),
        key=key, bev=0.15, segs=1)
    box(f'{prefix}cap', (depth + 0.6, y1 - y0 + 0.6, 0.5), loc=(x, (y0 + y1) / 2, z_top - 0.25),
        key='wj_ashlar', bev=0.12, segs=2)


def arch_ring(prefix, cx, zspring, span, rise, side_y, t, rnd, nv=19, key='wj_ashlar', keystone=True):
    """Voussoir ring on one face: wedge blocks around a semi/segmental arch."""
    r = span / 2
    for i in range(nv):
        a = math.pi * (i + 0.5) / nv
        x = cx + math.cos(a) * (r + 0.5)
        z = zspring + math.sin(a) * (rise + 0.5)
        box(f'{prefix}{i}', (1.5, t, 1.4), loc=(x, side_y, z),
            key=rnd.choice([key, 'wj_ashlar_d', key]), rot=(0, -math.degrees(a) + 90, 0), bev=0.1, segs=1)
    if keystone:
        box(f'{prefix}key', (1.3, t + 0.3, 2.3), loc=(cx, side_y, zspring + rise + 0.4),
            key='wj_ashlar', bev=0.12, segs=2)


def arch_vault(prefix, cx, zspring, span, rise, y0, y1, key='wj_stone_d', nseg=19):
    """Underside vault surface of an arch spanning along X, extruded across Y."""
    bm = bmesh.new()
    r = span / 2
    rows = []
    for i in range(nseg + 1):
        a = math.pi * i / nseg
        x = cx + math.cos(a) * r
        z = zspring + math.sin(a) * rise
        rows.append([bm.verts.new((x, y0, z)), bm.verts.new((x, y1, z))])
    for A, B in zip(rows, rows[1:]):
        bm.faces.new((A[0], B[0], B[1], A[1]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj_from_bm(f'{prefix}', bm, key)


def spandrel(prefix, cx, zspring, span, rise, y0, y1, deck_z, key='wj_stone'):
    """Solid spandrel/deck block above an arch, cut by the arch opening, built from the arch top up to deck."""
    # a filled block from deck down to a bit above the arch crown, plus side wedges beside the arch
    poly = [(cx - span / 2 - 6, 0), (cx + span / 2 + 6, 0), (cx + span / 2 + 6, deck_z), (cx - span / 2 - 6, deck_z)]
    # build as a prism then we rely on vault+ring reading; instead fill only the haunches
    for sgn in (-1, 1):
        x0 = cx + sgn * (span / 2)
        x1 = cx + sgn * (span / 2 + 6)
        box(f'{prefix}h{sgn}', (abs(x1 - x0), y1 - y0, deck_z), loc=((x0 + x1) / 2, (y0 + y1) / 2, deck_z / 2),
            key=key, bev=0.0)
    # fill above crown
    crown = zspring + rise
    box(f'{prefix}top', (span, y1 - y0, max(0.4, deck_z - crown - 0.2)),
        loc=(cx, (y0 + y1) / 2, (crown + 0.2 + deck_z) / 2), key=key)


def ivy_patch(prefix, x, y, z, rnd, n=5, key='wj_ivy'):
    for i in range(n):
        blob(f'{prefix}{i}', rnd.uniform(0.5, 1.0),
             (x + rnd.uniform(-0.6, 0.6), y, z + rnd.uniform(-0.8, 0.8)), key,
             subdiv=1, amp=0.3, scale=(1.3, 0.25, 1.1), seed=rnd.randint(0, 999))


# ---------------------------------------------------------------- F08_01..03 stone bridges
def stone_bridge_arch():
    """F08_01 - single stone arch bridge, 30 long x 12 wide: one semicircular arch, voussoir ring, parapets, lamp posts, cobbled deck."""
    reset()
    rnd = random.Random(801)
    L, Wd = 30.0, 12.0
    span, rise = 16.0, 8.0
    zspring = 1.5
    deck = zspring + rise + 1.6  # ~11.1 crown just under deck
    y0, y1 = -Wd / 2, Wd / 2
    # arch vault underside + voussoir ring on both faces
    arch_vault('vault', 0, zspring, span, rise, y0 + 1.4, y1 - 1.4)
    for side in (-1, 1):
        arch_ring('vr%d' % side, 0, zspring, span, rise, side * (Wd / 2 - 0.5), 1.4, rnd)
    # haunch fill ONLY beside the arch (between arch spring and the ends), never over the opening
    for sgn in (-1, 1):
        x0 = sgn * (span / 2)
        x1 = sgn * (L / 2)
        box('haunch%d' % sgn, (abs(x1 - x0), Wd - 2.8, deck), loc=((x0 + x1) / 2, 0, deck / 2), key='wj_stone')
    # thin fill above the crown up to the deck (keeps the opening readable)
    crown = zspring + rise
    box('crownfill', (span, Wd - 2.8, max(0.4, deck - crown - 0.1)),
        loc=(0, 0, (crown + 0.1 + deck) / 2), key='wj_stone')
    # abutments sinking into ground
    for e in (-1, 1):
        abutment('ab%d' % e, e * (L / 2 - 1.0), y0, y1, deck, depth=4.0)
    # humped cobbled deck on top
    setts('dk', -L / 2 + 2.0, L / 2 - 2.0, y0 + 1.6, y1 - 1.6, deck, rnd)
    # parapets (low) + lamp posts on the four corners
    for side in (-1, 1):
        parapet('pp%d' % side, -L / 2 + 1.5, L / 2 - 1.5, side * (Wd / 2 - 0.6), deck, rnd, h=2.2, t=1.0)
        for e in (-1, 1):
            lamp_post('lp%d%d' % (side, e), e * (L / 2 - 2.5), side * (Wd / 2 - 0.6), deck + 2.5, h=4.6)
    return finalize('stone_bridge_arch', smooth_angle=30)


def stone_bridge_slab():
    """F08_02 - low flat slab bridge on stone piers, 24 long x 12 wide: stone beam deck on three pier bays, low kerb, no arch."""
    reset()
    rnd = random.Random(802)
    L, Wd = 24.0, 12.0
    deck = 7.0
    y0, y1 = -Wd / 2, Wd / 2
    # piers in the water
    for px in (-L / 2 + 1.0, -L / 6, L / 6, L / 2 - 1.0):
        # pointed cutwater pier
        poly_prism('pier%.0f' % px, [(-1.4, -2.0), (1.4, -2.0), (2.1, 0.0), (1.4, 2.2), (-1.4, 2.2), (-2.1, 0.0)],
                   deck - 0.6, loc=(px, 0, -2.5), key='wj_stone', rot=(0, 0, 0))
        box('piercap%.0f' % px, (4.6, Wd - 1.0, 0.6), loc=(px, 0, deck - 0.9), key='wj_ashlar', bev=0.1)
    # stone slab beams spanning
    for j in range(5):
        y = y0 + 1.2 + (Wd - 2.4) * (j + 0.5) / 5
        box('beam%d' % j, (L, (Wd - 2.4) / 5 - 0.1, 0.9), loc=(0, y, deck - 0.45), key=rnd.choice(['wj_stone', 'wj_stone_d']), bev=0.05)
    # cobbled deck
    setts('dk', -L / 2 + 0.5, L / 2 - 0.5, y0 + 0.8, y1 - 0.8, deck, rnd)
    # low kerb edges
    for side in (-1, 1):
        parapet('kb%d' % side, -L / 2, L / 2, side * (Wd / 2 - 0.5), deck, rnd, h=1.1, t=0.9, coping=True)
    # abutments
    for e in (-1, 1):
        abutment('ab%d' % e, e * (L / 2 + 0.5), y0, y1, deck, depth=3.0)
    return finalize('stone_bridge_slab', smooth_angle=30)


def stone_bridge_double():
    """F08_03 - grand double-arch bridge, 50 long x 14 wide: two semicircular arches, central cutwater pier, carved keystones, balustrade, lamp posts."""
    reset()
    rnd = random.Random(803)
    L, Wd = 50.0, 14.0
    span, rise = 18.0, 8.5
    zspring = 1.5
    deck = zspring + rise + 1.6
    y0, y1 = -Wd / 2, Wd / 2
    centres = (-L / 4, L / 4)
    for c in centres:
        arch_vault('vault%.0f' % c, c, zspring, span, rise, y0 + 1.4, y1 - 1.4)
        for side in (-1, 1):
            arch_ring('vr%.0f_%d' % (c, side), c, zspring, span, rise, side * (Wd / 2 - 0.5), 1.4, rnd)
    # central cutwater pier
    poly_prism('cpier', [(-2.5, -Wd / 2 - 1.0), (2.5, -Wd / 2 - 1.0), (4.0, 0), (2.5, Wd / 2 + 1.0), (-2.5, Wd / 2 + 1.0), (-4.0, 0)],
               deck, loc=(0, 0, -2.5), key='wj_stone')
    box('cpiercap', (6.0, Wd + 1.8, 0.6), loc=(0, 0, deck - 0.3), key='wj_ashlar', bev=0.1)
    # haunch fills + spandrel over each arch
    for c in centres:
        box('fill%.0f' % c, (span + 2, Wd - 2.8, deck), loc=(c, 0, deck / 2), key='wj_stone')
    box('fillmid', (L / 2 - span, Wd - 2.8, deck), loc=(0, 0, deck / 2), key='wj_stone')
    # re-carve: nothing (vault reads through); cobbled deck on top
    setts('dk', -L / 2 + 2.5, L / 2 - 2.5, y0 + 1.6, y1 - 1.6, deck, rnd)
    # balustrade (posts + rail) + lamp posts
    for side in (-1, 1):
        sy = side * (Wd / 2 - 0.6)
        box('rail%d' % side, (L - 4, 0.6, 0.5), loc=(0, sy, deck + 3.0), key='wj_ashlar', bev=0.08)
        box('base%d' % side, (L - 4, 0.9, 0.5), loc=(0, sy, deck + 0.3), key='wj_ashlar', bev=0.08)
        nb = int((L - 6) / 1.4)
        for i in range(nb + 1):
            x = -L / 2 + 3 + (L - 6) * i / nb
            lathe('bal%d_%d' % (side, i), [(0.0, 0.0), (0.28, 0.05), (0.18, 0.5), (0.3, 0.95), (0.16, 1.4), (0.26, 2.4), (0.0, 2.6)],
                  loc=(x, sy, deck + 0.5), key='wj_ashlar', segs=8)
        for e in (-1, 1):
            # end newel + lamp
            box('newel%d%d' % (side, e), (1.3, 1.3, 4.6), loc=(e * (L / 2 - 2.0), sy, deck + 2.3), key='wj_ashlar', bev=0.1)
            lamp_post('lp%d%d' % (side, e), e * (L / 2 - 2.0), sy, deck + 4.6, h=4.4)
    for e in (-1, 1):
        abutment('ab%d' % e, e * (L / 2 - 1.5), y0, y1, deck, depth=5.0)
    return finalize('stone_bridge_double', smooth_angle=30)


# ---------------------------------------------------------------- F08_04..06 wooden bridges
def wooden_footbridge():
    """F08_04 - plank footbridge with rope rails, 24 long x 7 wide: gently arched stringers, plank deck, posts and sagging rope handrails."""
    reset()
    rnd = random.Random(804)
    L, Wd = 24.0, 7.0
    base, hump = 6.0, 2.4
    zf = lambda x: base + hump * (1 - (2 * x / L) ** 2)
    # curved stringers
    for side in (-1, 1):
        pts = [(x, side * (Wd / 2 - 0.5), zf(x) - 0.5) for x in [-L / 2 + L * t / 10 for t in range(11)]]
        tube('str%d' % side, pts, 0.4, 'wj_timber', res=4, ures=3)
    tube('strc', [(x, 0, zf(x) - 0.55) for x in [-L / 2 + L * t / 10 for t in range(11)]], 0.35, 'wj_timber', res=4, ures=3)
    # deck planks
    n = 30
    for i in range(n):
        x = -L / 2 + L * (i + 0.5) / n
        slope = math.degrees(math.atan(-8 * hump * x / (L * L)))
        box('pl%d' % i, (L / n - 0.08, Wd, 0.28), loc=(x, rnd.uniform(-0.08, 0.08), zf(x)),
            key=rnd.choice(PLANK_KEYS), rot=(0, slope, rnd.uniform(-1.0, 1.0)), bev=0.04, segs=1)
    # posts + rope rails
    for side in (-1, 1):
        sy = side * (Wd / 2 - 0.2)
        xs = [-L / 2 + L * i / 8 for i in range(9)]
        for j, x in enumerate(xs):
            xx = max(-L / 2 + 0.3, min(L / 2 - 0.3, x))
            cyl('post%d%d' % (side, j), 0.22, 3.0, loc=(xx, sy, zf(xx)), key='wj_timber_d', verts=8)
            ball('postt%d%d' % (side, j), 0.28, loc=(xx, sy, zf(xx) + 3.0), key='wj_timber_d', segs=8, rings=6)
        # sagging top + mid rope between posts
        for j in range(8):
            x0, x1 = xs[j], xs[j + 1]
            xm = (x0 + x1) / 2
            for zoff, r in ((2.6, 0.08), (1.4, 0.06)):
                tube('rope%d%d_%.1f' % (side, j, zoff),
                     [(max(-L/2+0.3,min(L/2-0.3,x0)), sy, zf(x0) + zoff),
                      (xm, sy, zf(xm) + zoff - 0.35),
                      (max(-L/2+0.3,min(L/2-0.3,x1)), sy, zf(x1) + zoff)], r, 'wj_rope', res=4, ures=3)
    # stone footings
    for e in (-1, 1):
        box('foot%d' % e, (3.0, Wd + 1.5, 2.0), loc=(e * (L / 2 - 0.5), 0, zf(L / 2) - 0.6), key='wj_stone', bev=0.15)
    return finalize('wooden_footbridge', smooth_angle=35)


def wooden_trestle():
    """F08_05 - trestle bridge on timber piers, 32 long x 10 wide: braced timber bents, horizontal plank deck, post-and-rail sides."""
    reset()
    rnd = random.Random(805)
    L, Wd = 32.0, 10.0
    deck = 8.0
    # trestle bents
    bentxs = [-L / 2 + 3, -L / 6, L / 6, L / 2 - 3]
    for bx in bentxs:
        for side in (-1, 1):
            sy = side * (Wd / 2 - 0.8)
            # splayed legs
            tube('leg%.0f%d' % (bx, side), [(bx, sy * 1.35, 0), (bx, sy, deck - 0.6)], 0.42, 'wj_timber', res=4, taper=[1.1, 0.95])
        # cross cap
        box('cap%.0f' % bx, (1.0, Wd + 0.6, 0.7), loc=(bx, 0, deck - 0.6), key='wj_timber')
        # X brace
        tube('xa%.0f' % bx, [(bx, -(Wd / 2 - 0.8) * 1.35, 0.5), (bx, (Wd / 2 - 0.8), deck - 1.0)], 0.22, 'wj_timber_d', res=4)
        tube('xb%.0f' % bx, [(bx, (Wd / 2 - 0.8) * 1.35, 0.5), (bx, -(Wd / 2 - 0.8), deck - 1.0)], 0.22, 'wj_timber_d', res=4)
    # stringers along the bridge
    for side in (-1, 1):
        box('strg%d' % side, (L, 0.6, 0.8), loc=(0, side * (Wd / 2 - 0.9), deck - 0.4), key='wj_timber')
    box('strgc', (L, 0.6, 0.8), loc=(0, 0, deck - 0.4), key='wj_timber')
    # deck planks
    n = 40
    for i in range(n):
        x = -L / 2 + L * (i + 0.5) / n
        box('pl%d' % i, (L / n - 0.08, Wd, 0.3), loc=(x, rnd.uniform(-0.08, 0.08), deck),
            key=rnd.choice(PLANK_KEYS), rot=(0, 0, rnd.uniform(-1.0, 1.0)), bev=0.04, segs=1)
    # post and rail sides
    for side in (-1, 1):
        sy = side * (Wd / 2 - 0.3)
        xs = [-L / 2 + L * i / 10 for i in range(11)]
        for j, x in enumerate(xs):
            cyl('rp%d%d' % (side, j), 0.2, 3.2, loc=(x, sy, deck + 0.15), key='wj_timber_d', verts=8)
        for zoff in (2.9, 1.6):
            box('rl%d_%.1f' % (side, zoff), (L, 0.2, 0.2), loc=(0, sy, deck + zoff), key='wj_timber')
    # abutments
    for e in (-1, 1):
        abutment('ab%d' % e, e * (L / 2 + 0.5), -Wd / 2, Wd / 2, deck, depth=3.0)
    return finalize('wooden_trestle', smooth_angle=35)


def wooden_covered():
    """F08_06 - covered timber bridge, 28 long x 10 wide: enclosed with plank walls, window openings, shingled gable roof, portals at each end."""
    reset()
    rnd = random.Random(806)
    L, Wd = 28.0, 10.0
    deck = 7.5
    wallh = 6.5
    # stone abutments + plank deck
    for e in (-1, 1):
        abutment('ab%d' % e, e * (L / 2 + 0.3), -Wd / 2, Wd / 2, deck, depth=3.5)
    # deck beams
    for side in (-1, 1):
        box('strg%d' % side, (L, 0.7, 1.0), loc=(0, side * (Wd / 2 - 0.8), deck - 0.6), key='wj_timber')
    box('strgc', (L, 0.7, 1.0), loc=(0, 0, deck - 0.6), key='wj_timber')
    planks_x('pl', -L / 2, L / 2, -Wd / 2, Wd / 2, deck - 0.3, rnd, pw=1.2)
    # side walls (planked), with gaps as windows
    for side in (-1, 1):
        sy = side * (Wd / 2 - 0.2)
        # sill + top plate
        box('sill%d' % side, (L, 0.35, 0.9), loc=(0, sy, deck + 0.45), key='wj_timber')
        box('plate%d' % side, (L, 0.35, 0.5), loc=(0, sy, deck + wallh), key='wj_timber')
        # vertical board siding lower + upper, leaving a window band in the middle third
        nb = int(L / 1.1)
        for i in range(nb):
            x = -L / 2 + 0.6 + (L - 1.2) * i / (nb - 1)
            # lower boards
            box('bl%d_%d' % (side, i), (1.0, 0.18, 2.2), loc=(x, sy, deck + 1.9),
                key=rnd.choice(PLANK_KEYS), rot=(0, 0, rnd.uniform(-0.8, 0.8)), bev=0.03)
            # upper boards (window head to plate)
            box('bu%d_%d' % (side, i), (1.0, 0.18, 1.6), loc=(x, sy, deck + wallh - 1.1),
                key=rnd.choice(PLANK_KEYS), rot=(0, 0, rnd.uniform(-0.8, 0.8)), bev=0.03)
        # window mullions in the open band
        for x in [-L / 2 + 3 + k * 3.0 for k in range(int((L - 6) / 3.0) + 1)]:
            box('mul%d_%.0f' % (side, x), (0.22, 0.3, 2.0), loc=(x, sy, deck + 3.9), key='wj_timber_d')
        box('wh%d' % side, (L, 0.3, 0.3), loc=(0, sy, deck + 4.95), key='wj_timber')
    # corner posts
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl('cp%d%d' % (sx, sy), 0.35, wallh + 0.4, loc=(sx * (L / 2 - 0.4), sy * (Wd / 2 - 0.3), deck + 0.3),
                key='wj_timber_d', verts=8)
    # portal trim boards at the ends (frame the entrance)
    for e in (-1, 1):
        box('port%d' % e, (0.5, Wd + 0.8, wallh), loc=(e * (L / 2 + 0.1), 0, deck + 0.5 + wallh / 2), key='wj_timber')
        # arched portal cut look: two side blocks
        for sy in (-1, 1):
            box('portj%d%d' % (e, sy), (0.6, 1.6, wallh), loc=(e * (L / 2 + 0.05), sy * (Wd / 2 - 1.2), deck + 0.5 + wallh / 2),
                key='wj_timber_d')
    # shingled gable roof
    gable_roof(F(0, 0, 0, 0), L + 1.0, Wd + 1.4, deck + wallh + 0.5, Wd * 0.42,
               keys=('wj_plank_b', 'wj_wood_old'), wall='wj_timber', barge='wj_timber_d', ov=0.8, ovg=0.7, row=1.0)
    return finalize('wooden_covered', smooth_angle=30)


# ---------------------------------------------------------------- F08_07 ruined bridge
def ruined_bridge():
    """F08_07 - broken stone arch bridge, 30 long: a collapsed middle span, jagged broken parapets, rubble in the gap, ivy and moss."""
    reset()
    rnd = random.Random(807)
    L, Wd = 30.0, 12.0
    span, rise = 15.0, 7.0
    zspring = 1.5
    deck = zspring + rise + 1.3
    y0, y1 = -Wd / 2, Wd / 2
    # Build only the two end stubs of the arch (springing up part-way, then broken)
    for sgn in (-1, 1):
        # partial vault from the spring on each side up toward (but not reaching) the crown
        bm = bmesh.new()
        r = span / 2
        rows = []
        amax = 0.62  # fraction of the half-arch that survives on this side
        steps = 12
        for i in range(steps + 1):
            a = (math.pi / 2) * amax * i / steps  # from 0 (spring, outer) ... toward crown
            ang = (math.pi if sgn < 0 else 0.0) + sgn * a
            x = math.cos(ang) * r
            z = zspring + math.sin(abs(a)) * rise if False else zspring + math.sin(a) * rise
            # correct: param by a along the arch; use ang for x
            x = r * math.cos((math.pi if sgn < 0 else 0.0) + sgn * a)
            z = zspring + rise * math.sin(a)
            rows.append([bm.verts.new((x, y0 + 1.2, z)), bm.verts.new((x, y1 - 1.2, z))])
        for A, B in zip(rows, rows[1:]):
            bm.faces.new((A[0], B[0], B[1], A[1]))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        _obj_from_bm('vault%d' % sgn, bm, 'wj_stone_d')
        # voussoir stubs on faces with a jagged broken top
        for side in (-1, 1):
            nv = 11
            for i in range(nv):
                a = (math.pi / 2) * 0.62 * (i + 0.5) / nv
                ang = (math.pi if sgn < 0 else 0.0) + sgn * a
                x = (span / 2 + 0.5) * math.cos(ang)
                z = zspring + (rise + 0.5) * math.sin(a)
                box('vr%d%d_%d' % (sgn, side, i), (1.4, 1.2, 1.3), loc=(x, side * (Wd / 2 - 0.5), z),
                    key=rnd.choice(['wj_ashlar', 'wj_ashlar_d', 'wj_stone']),
                    rot=(0, -math.degrees(a) * sgn + (90 if sgn > 0 else 90), rnd.uniform(-3, 3)), bev=0.1)
        # haunch fill behind the stub up to deck, outer side only
        x0 = sgn * (span / 2)
        x1 = sgn * (L / 2)
        box('fill%d' % sgn, (abs(x1 - x0), Wd - 2.4, deck), loc=((x0 + x1) / 2, 0, deck / 2), key='wj_stone')
        # broken deck edge: setts thinning toward the gap
        xa, xb = (sgn * (span / 2 * 0.2), sgn * (L / 2 - 2.5))
        lo, hi = sorted((xa, xb))
        setts('dk%d' % sgn, lo, hi, y0 + 1.6, y1 - 1.6, deck, rnd)
        # jagged parapet stubs
        for side in (-1, 1):
            n = 7
            for i in range(n):
                frac = i / n
                x = sgn * (L / 2 - 1.5 - frac * (L / 2 - span / 2 - 1.0))
                h = 2.6 * (1 - frac * 0.9) + rnd.uniform(-0.3, 0.3)
                if h < 0.4:
                    continue
                box('pp%d%d_%d' % (sgn, side, i), (2.0, 1.1, h), loc=(x, side * (Wd / 2 - 0.6), deck + h / 2),
                    key=rnd.choice(['wj_stone', 'wj_stone_d']), rot=(0, 0, rnd.uniform(-4, 4)), bev=0.08)
        abutment('ab%d' % sgn, sgn * (L / 2 - 1.0), y0, y1, deck, depth=4.0)
    # rubble in the gap and below
    for i in range(14):
        x = rnd.uniform(-span / 2, span / 2)
        rock('rub%d' % i, rnd.uniform(0.8, 2.0), (x, rnd.uniform(y0 + 1, y1 - 1), rnd.uniform(-2.5, 1.0)),
             rnd.choice(['wj_stone', 'wj_stone_d', 'wj_ashlar_d']), seed=807 + i, scale=(1.2, 1.0, 0.8), subdiv=1)
    # ivy + moss on the stubs
    for sgn in (-1, 1):
        ivy_patch('ivy%d' % sgn, sgn * (span / 2 + 1), -(Wd / 2 - 0.3), deck - 2, rnd, n=6)
    return finalize('ruined_bridge', smooth_angle=30)


# ---------------------------------------------------------------- F08_08..10 signposts
def signpost_crossroads():
    """F08_08 - three-arm wooden crossroads post, 10 tall: squared timber post on a stone base, three carved arrow boards, a little shingle cap."""
    reset()
    rnd = random.Random(808)
    # stone base
    lathe('base', [(0.0, 0.0), (1.4, 0.0), (1.2, 0.5), (1.0, 0.6), (0.0, 0.6)], key='wj_stone', segs=8)
    box('post', (0.7, 0.7, 9.4), loc=(0, 0, 0.6 + 4.7), key='wj_timber', bev=0.06)
    # three arrow boards at different heights/angles
    arrow = [(0.0, -0.65), (3.4, -0.65), (4.3, 0.0), (3.4, 0.65), (0.0, 0.65)]
    for i, (z, ang) in enumerate(((8.6, 20), (7.3, 150), (6.0, -75))):
        o = poly_prism('board%d' % i, arrow, 0.22, loc=(0, 0, 0), key=rnd.choice(['wj_plank', 'wj_wood_old']), rot=(90, 0, 0))
        o.rotation_euler = (math.radians(90), 0, math.radians(ang))
        o.location = (math.cos(math.radians(ang)) * 0.42, math.sin(math.radians(ang)) * 0.42, z)
        # carved text groove band
        b = box('band%d' % i, (2.6, 0.05, 0.42), loc=(0, 0, 0), key='wj_timber_d')
        b.rotation_euler = (0, 0, math.radians(ang))
        b.location = (math.cos(math.radians(ang)) * 2.3, math.sin(math.radians(ang)) * 2.3, z)
        # pointer nub
        ball('nub%d' % i, 0.14, loc=(math.cos(math.radians(ang)) * 4.0, math.sin(math.radians(ang)) * 4.0, z), key='wj_iron', segs=6, rings=4)
    # shingle cap
    poly_prism('capL', [(-1.1, 0), (0, 0.8), (1.1, 0), (1.1, 0.14), (0, 0.94), (-1.1, 0.14)], 1.5,
               loc=(0, 0.75, 10.0), key='wj_plank_b', rot=(90, 0, 0))
    box('capbeam', (1.0, 1.0, 0.25), loc=(0, 0, 10.05), key='wj_timber', bev=0.04)
    return finalize('signpost_crossroads', smooth_angle=35)


def signpost_stone():
    """F08_09 - tall stone signpost, 11 tall: a dressed stone pillar with a chamfered cap and three iron directional plaques with embossed arrows."""
    reset()
    rnd = random.Random(809)
    box('plinth', (2.4, 2.4, 0.8), loc=(0, 0, 0.4), key='wj_stone', bev=0.12)
    box('plinth2', (1.9, 1.9, 0.5), loc=(0, 0, 0.9), key='wj_ashlar', bev=0.1)
    # tapered dressed shaft (built from courses so it reads as stone)
    for c in range(8):
        z = 1.2 + c * 1.18
        w = 1.4 - c * 0.05
        box('course%d' % c, (w, w, 1.12), loc=(0, 0, z + 0.56), key='wj_ashlar' if c % 2 == 0 else 'wj_ashlar_d', bev=0.05)
    # stepped square cornice cap
    box('cap1', (1.6, 1.6, 0.4), loc=(0, 0, 10.8), key='wj_ashlar', bev=0.06)
    box('cap2', (1.9, 1.9, 0.35), loc=(0, 0, 11.15), key='wj_ashlar', bev=0.06)
    lathe('capf', [(0.9, 0.0), (0.9, 0.2), (0.4, 0.75), (0.0, 0.9)], loc=(0, 0, 11.35), key='wj_ashlar', segs=12)
    # iron plaques
    for i, (z, ang) in enumerate(((8.4, 0), (7.0, 120), (5.6, 240))):
        a = math.radians(ang)
        c = (math.cos(a) * 0.72, math.sin(a) * 0.72, z)
        pl = poly_prism('plaq%d' % i, [(0, -0.5), (2.6, -0.5), (3.2, 0), (2.6, 0.5), (0, 0.5)], 0.12, loc=(0, 0, 0), key='wj_iron', rot=(90, 0, 0))
        pl.rotation_euler = (math.radians(90), 0, a)
        pl.location = c
        # embossed arrow + rivets
        for k in range(3):
            ball('riv%d_%d' % (i, k), 0.08, loc=(math.cos(a) * (0.9 + k * 0.6) - math.sin(a) * 0.0,
                 math.sin(a) * (0.9 + k * 0.6), z), key='wj_gold', segs=6, rings=4)
    return finalize('signpost_stone', smooth_angle=30)


def signpost_leaning():
    """F08_10 - leaning weathered signpost, 9 tall: an old grey post tilted off vertical, one hanging board, a small iron lantern bracket with a lit lantern."""
    reset()
    rnd = random.Random(810)
    lean = 8.0
    # weathered leaning post
    tube('post', [(0, 0, 0), (math.sin(math.radians(lean)) * 4.5, 0, 4.5),
                  (math.sin(math.radians(lean)) * 8.5, 0, 8.3)], 0.32, 'wj_wood_old', res=6, taper=[1.1, 1.0, 0.9], ures=3)
    tx = math.sin(math.radians(lean)) * 8.0
    # cross arm
    box('arm', (0.35, 4.2, 0.35), loc=(tx - 0.6, 0, 7.0), key='wj_wood_old', rot=(0, -lean, 0), bev=0.04)
    # hanging board on two short chains/ropes
    bx, bz = tx - 2.0, 5.7
    for sy in (-1, 1):
        tube('hr%d' % sy, [(tx - 0.6, sy * 1.6, 7.0), (bx, sy * 1.6, bz + 0.9)], 0.05, 'wj_rope', res=3)
    o = box('hboard', (3.0, 0.22, 1.6), loc=(bx, 0, bz), key='wj_plank_b', rot=(0, rnd.uniform(-3, 3), 0), bev=0.05)
    box('hbands', (3.0, 0.26, 0.2), loc=(bx, 0, bz + 0.4), key='wj_timber_d')
    # iron lantern bracket + lit lantern on the other arm side
    lxr = tx - 0.6
    tube('brk', [(lxr, 0, 6.6), (lxr + 1.0, 0, 6.9), (lxr + 1.4, 0, 6.5)], 0.06, 'wj_iron', res=3)
    tube('brkh', [(lxr + 1.4, 0, 6.6), (lxr + 1.4, 0, 6.0)], 0.04, 'wj_iron', res=3)
    lathe('lg', [(0.0, 0.0), (0.38, 0.0), (0.38, 0.9), (0.18, 1.15), (0.0, 1.2)], loc=(lxr + 1.4, 0, 4.9), key='wj_glass_lit', segs=6)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box('le%d%d' % (sx, sy), (0.05, 0.05, 0.95), loc=(lxr + 1.4 + sx * 0.28, sy * 0.28, 5.35), key='wj_iron')
    lathe('lt', [(0.46, 0.0), (0.1, 0.42), (0.0, 0.5)], loc=(lxr + 1.4, 0, 6.1), key='wj_iron', segs=6)
    # grass + a rock at the base
    rock('br', 1.0, (0.6, 0.8, 0.2), 'wj_stone', seed=810, scale=(1.2, 1.0, 0.6), subdiv=1)
    return finalize('signpost_leaning', smooth_angle=35)


# ---------------------------------------------------------------- F08_11..12 milestones
def milestone_carved():
    """F08_11 - carved stone milestone, 4 tall: a dressed rounded-top marker with a recessed panel, raised numerals and a flat cap."""
    reset()
    rnd = random.Random(811)
    pts = [(-1.1, 0.0), (1.1, 0.0), (1.05, 2.8)]
    for i in range(1, 12):
        a = math.pi * i / 12
        pts.append((math.cos(a) * 1.05, 2.8 + math.sin(a) * 0.95))
    pts.append((-1.05, 2.8))
    o = poly_prism('body', pts, 0.9, loc=(0, 0.45, 0), key='wj_ashlar', rot=(90, 0, 0))
    bevel(o, 0.08, 2)
    box('plinth', (2.8, 1.5, 0.5), loc=(0, 0, 0.25), key='wj_stone', bev=0.12)
    box('cap', (2.1, 1.1, 0.3), loc=(0, 0, 3.85), key='wj_ashlar', bev=0.08)
    # recessed panel + raised numerals (bars) + arrow
    box('panel', (1.5, 0.08, 1.5), loc=(0, -0.46, 2.1), key='wj_ashlar_d')
    for i, (x, h) in enumerate(((-0.4, 1.0), (0.0, 1.0), (0.4, 0.7))):
        box('num%d' % i, (0.16, 0.08, h), loc=(x, -0.5, 2.2), key='wj_stone_d')
    box('arrow', (0.9, 0.08, 0.16), loc=(0, -0.5, 1.4), key='wj_stone_d')
    return finalize('milestone_carved', smooth_angle=30)


def milestone_mossy():
    """F08_12 - rounded mossy milestone, 3 tall: a weathered boulder-like marker sunk slightly into the ground, moss on the north face, faint carved number."""
    reset()
    rnd = random.Random(812)
    # rocky weathered body: noise-displaced rounded marker
    body = blob('body', 1.5, (0, 0, 1.5), 'wj_stone', subdiv=3, amp=0.22, freq=1.3,
                scale=(0.85, 0.7, 1.05), seed=812, flat_bottom=-0.3, detail=0.4)
    box('plinth', (2.4, 1.8, 0.5), loc=(0, 0, 0.25), key='wj_stone_d', bev=0.1)
    # dressed flat front face for the carved panel (faces -Y)
    box('face', (1.3, 0.3, 1.8), loc=(0, -0.85, 1.7), key='wj_stone', bev=0.06)
    box('panel', (0.95, 0.12, 1.1), loc=(0, -1.0, 1.7), key='wj_stone_d')
    # carved numeral (two bars) in the recess
    for i, x in enumerate((-0.18, 0.18)):
        box('num%d' % i, (0.13, 0.08, 0.65), loc=(x, -1.05, 1.7), key='wj_ashlar_d')
    # heavy moss on top and the +Y (shaded) face, lighter dusting on front edges
    body = top_paint(body, 'wj_moss', 0.55, 812, noise_amt=0.22)
    for i in range(8):
        ball('moss%d' % i, rnd.uniform(0.28, 0.5),
             loc=(rnd.uniform(-0.8, 0.8), rnd.uniform(0.2, 0.75), rnd.uniform(1.4, 2.7)),
             key='wj_moss', segs=8, rings=5, scale=(1.4, 0.3, 0.9))
    for i in range(4):
        ball('mosst%d' % i, rnd.uniform(0.3, 0.46), loc=(rnd.uniform(-0.5, 0.5), rnd.uniform(-0.3, 0.5), 2.75),
             key='wj_moss', segs=8, rings=5, scale=(1.3, 1.0, 0.3))
    # a couple of small rocks at the base
    for i in range(3):
        a = rnd.uniform(0, 6.28)
        rock('br%d' % i, rnd.uniform(0.3, 0.5), (math.cos(a) * 1.1, math.sin(a) * 0.8, 0.15), 'wj_stone_d', seed=812 + i, scale=(1.2, 1.0, 0.6), subdiv=1)
    return finalize('milestone_mossy', smooth_angle=35)


# ---------------------------------------------------------------- F08_13..14 road gate arches
def gate_arch_stone():
    """F08_13 - stone region gateway, 24 wide x 22 tall: two battered piers, a round arch with a carved keystone, banners, lantern brackets; passage 14 x 14."""
    reset()
    rnd = random.Random(813)
    passage, ph = 14.0, 14.0
    pierw = 5.0
    totalw = passage + 2 * pierw  # 24
    zspring = ph - passage / 2   # arch springs at ~7 so crown ~14
    # piers
    for sgn in (-1, 1):
        px = sgn * (passage / 2 + pierw / 2)
        # battered pier (slightly tapering) built from courses
        nc = 9
        for c in range(nc):
            z = 1.0 + c * 2.2
            w = pierw - c * 0.12
            box('pier%d_%d' % (sgn, c), (w, w, 2.1), loc=(px, 0, z + 1.05),
                key=rnd.choice(['wj_stone', 'wj_stone_d', 'wj_ashlar']), rot=(0, 0, rnd.uniform(-0.6, 0.6)), bev=0.06)
        # cap cornice
        box('piercap%d' % sgn, (pierw + 0.8, pierw + 0.8, 0.8), loc=(px, 0, zspring + 0.0), key='wj_ashlar', bev=0.12)
        # lantern bracket on inner face
        tube('brk%d' % sgn, [(px - sgn * pierw / 2, 0, 9.0), (px - sgn * 1.0, 0, 9.3)], 0.14, 'wj_iron', res=3)
        lathe('lg%d' % sgn, [(0.0, 0.0), (0.5, 0.0), (0.5, 1.2), (0.0, 1.3)], loc=(px - sgn * 1.0, 0, 8.0), key='wj_glass_lit', segs=6)
    # arch over passage
    arch_vault('vault', 0, zspring, passage, passage / 2, -2.5, 2.5)
    for side in (-1, 1):
        arch_ring('vr%d' % side, 0, zspring, passage, passage / 2, side * 2.5, 2.0, rnd)
    # top lintel beam + battlement cap across
    box('lintel', (totalw, 5.0, 1.0), loc=(0, 0, zspring + passage / 2 + 0.6), key='wj_ashlar', bev=0.1)
    # merlons on top
    nm_ = 7
    for i in range(nm_):
        x = -totalw / 2 + totalw * (i + 0.5) / nm_
        box('mer%d' % i, (totalw / nm_ - 0.8, 4.0, 1.8), loc=(x, 0, zspring + passage / 2 + 2.0),
            key=rnd.choice(['wj_stone', 'wj_ashlar']), bev=0.08)
    # carved keystone
    box('keystone', (1.6, 5.2, 3.0), loc=(0, 0, zspring + passage / 2 - 0.5), key='wj_ashlar', bev=0.12)
    ball('keycarve', 0.6, loc=(0, -2.6, zspring + passage / 2 - 0.5), key='wj_gold', segs=10, rings=7, scale=(1, 0.3, 1))
    # hanging banners from the lintel
    for sgn in (-1, 1):
        bx = sgn * 4.0
        poly_prism('ban%d' % sgn, [(-1.4, 0), (1.4, 0), (1.4, -5.5), (0.8, -6.5), (-0.8, -6.5), (-1.4, -5.5)], 0.1,
                   loc=(bx, -2.7, zspring + passage / 2 - 0.5), key='wj_banner_r' if sgn < 0 else 'wj_banner_b', rot=(90, 0, 0))
        ball('bane%d' % sgn, 0.5, loc=(bx, -2.85, zspring + passage / 2 - 3.5), key='wj_gold', segs=8, rings=6, scale=(1, 0.3, 1))
    return finalize('gate_arch_stone', smooth_angle=30)


def gate_arch_timber():
    """F08_14 - timber frontier gate (original torii-like), passage 14 x 14: two tapered timber posts on stone footings, a double crossbeam with struts, hanging name-boards and a small peaked cap."""
    reset()
    rnd = random.Random(814)
    passage, ph = 14.0, 14.0
    postx = passage / 2 + 1.2
    # stone footings + posts
    for sgn in (-1, 1):
        px = sgn * postx
        lathe('foot%d' % sgn, [(0.0, 0.0), (1.9, 0.0), (1.7, 0.8), (1.4, 1.0), (0.0, 1.0)], loc=(px, 0, 0), key='wj_stone', segs=10)
        cyl('post%d' % sgn, 1.1, ph, loc=(px, 0, 1.0), key='wj_timber', verts=12, r2=0.9)
        # iron bands
        for z in (3.0, 9.0):
            torus('band%d_%.0f' % (sgn, z), 1.05, 0.14, loc=(px, 0, z), key='wj_iron', segs=14, rsegs=5, rot=(0, 90, 0) if False else (0, 0, 0))
    # top double crossbeam (upper curved, lower straight) - torii-like, original
    topz = ph + 0.5
    # upper beam with slight upward sweep at ends (built from segments)
    nseg = 9
    beamw = passage + 2 * postx - passage + 2 * 3.2  # overhang
    span = postx + 3.2
    for i in range(nseg):
        t = (i + 0.5) / nseg - 0.5
        x = t * 2 * span
        z = topz + 1.0 + (abs(t * 2) ** 2) * 1.4  # lift at ends
        box('ub%d' % i, (2 * span / nseg + 0.1, 2.4, 1.2), loc=(x, 0, z),
            key='wj_timber', rot=(0, -math.degrees(math.atan2((abs(t) * 2) * 1.0, 1.0)) * (1 if t > 0 else -1) * 0.0, 0), bev=0.06)
    # lower straight tie beam
    box('lb', (2 * postx + 2.4, 1.8, 1.1), loc=(0, 0, ph - 1.5), key='wj_timber_d', bev=0.06)
    # struts between the two beams
    for sgn in (-1, 1):
        box('strut%d' % sgn, (1.0, 1.0, topz + 1.0 - (ph - 1.0)), loc=(sgn * postx * 0.5, 0, (topz + 1.0 + ph - 1.0) / 2), key='wj_timber')
    # small peaked shingle cap on the upper beam
    poly_prism('capL', [(-span - 1, 0), (0, 1.6), (span + 1, 0), (span + 1, 0.2), (0, 1.8), (-span - 1, 0.2)], 3.0,
               loc=(0, 1.5, topz + 2.2), key='wj_plank_b', rot=(90, 0, 0))
    # hanging name boards
    for sgn in (-1, 1):
        bx = sgn * 3.6
        for sy in (-1, 1):
            tube('hr%d%d' % (sgn, sy), [(bx + sy * 0.0, 0, ph - 2.0), (bx, 0, ph - 2.5 + 0.0)], 0.04, 'wj_rope', res=2)
        box('nb%d' % sgn, (2.6, 0.2, 3.2), loc=(bx, 0, ph - 4.2), key='wj_plank', rot=(0, rnd.uniform(-2, 2), 0), bev=0.05)
        box('nbt%d' % sgn, (2.6, 0.24, 0.25), loc=(bx, 0, ph - 2.8), key='wj_timber_d')
    return finalize('gate_arch_timber', smooth_angle=30)


# ---------------------------------------------------------------- F08_15..17 roadside shrines
def shrine_stone():
    """F08_15 - small stone roadside shrine, 8 tall: a pedestal with a pitched roof over a niche holding two lit candles and an offering bowl."""
    reset()
    rnd = random.Random(815)
    # stepped base
    box('step1', (4.0, 3.4, 0.6), loc=(0, 0, 0.3), key='wj_stone', bev=0.08)
    box('step2', (3.2, 2.8, 0.6), loc=(0, 0, 0.9), key='wj_stone', bev=0.08)
    # body with a niche
    box('body', (3.0, 2.6, 4.0), loc=(0, 0, 1.2 + 2.0), key='wj_ashlar', bev=0.06)
    # niche opening (recessed dark box), wider and open at the front
    box('niche', (2.0, 1.2, 2.6), loc=(0, -0.7, 1.2 + 2.2), key='wj_stone_d')
    # side pilasters framing the niche
    for sgn in (-1, 1):
        box('pil%d' % sgn, (0.4, 0.6, 2.8), loc=(sgn * 1.3, -1.3, 1.2 + 2.2), key='wj_ashlar')
    box('nlintel', (2.8, 0.6, 0.4), loc=(0, -1.3, 1.2 + 3.7), key='wj_ashlar')
    # candle ledge + two tall candles with flames near the front so they read
    box('ledge', (2.0, 0.9, 0.3), loc=(0, -0.8, 1.2 + 1.1), key='wj_ashlar')
    for sgn in (-1, 1):
        cyl('candle%d' % sgn, 0.16, 1.0, loc=(sgn * 0.6, -1.0, 1.2 + 1.25), key='wj_ashlar', verts=8)
        flame('fl%d' % sgn, (sgn * 0.6, -1.0, 1.2 + 2.25), h=0.6, r=0.16, seed=815 + sgn)
    lathe('bowl', [(0.0, 0.0), (0.45, 0.0), (0.5, 0.3), (0.3, 0.34), (0.0, 0.12)], loc=(0, -1.1, 1.2 + 1.25), key='wj_iron', segs=10)
    # pitched roof
    poly_prism('roofL', [(-2.0, 0), (0, 1.6), (2.0, 0), (2.0, 0.2), (0, 1.8), (-2.0, 0.2)], 3.2,
               loc=(0, 1.6, 1.2 + 4.0), key='wj_plank_b', rot=(90, 0, 0))
    box('ridge', (0.4, 3.4, 0.3), loc=(0, 0, 1.2 + 5.75), key='wj_timber_d')
    ball('finial', 0.3, loc=(0, 0, 1.2 + 6.0), key='wj_gold', segs=8, rings=6)
    return finalize('shrine_stone', smooth_angle=30)


def shrine_cross():
    """F08_16 - wooden wayside cross, 10 tall: a weathered timber cross on a cairn base under a tiny peaked roof, with a wreath and offerings at the foot."""
    reset()
    rnd = random.Random(816)
    # cairn base of stacked rocks (broader, chunkier)
    for i in range(10):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, 1.9)
        rock('cairn%d' % i, rnd.uniform(0.8, 1.5), (math.cos(a) * d, math.sin(a) * d, 0.15 + i * 0.14),
             rnd.choice(['wj_stone', 'wj_stone_d']), seed=816 + i, scale=(1.2, 1.1, 0.85), subdiv=1)
    # timber cross (sturdier)
    box('upright', (0.75, 0.75, 7.2), loc=(0, 0, 1.8 + 3.6), key='wj_wood_old', bev=0.05)
    box('arm', (4.0, 0.72, 0.72), loc=(0, 0, 1.8 + 5.2), key='wj_wood_old', bev=0.05)
    # iron joint plate + bolts
    box('plate', (1.1, 0.8, 1.1), loc=(0, -0.3, 1.8 + 5.2), key='wj_iron')
    for sx in (-1, 1):
        for sz in (-1, 1):
            ball('bolt%d%d' % (sx, sz), 0.1, loc=(sx * 0.35, -0.42, 1.8 + 5.2 + sz * 0.35), key='wj_iron', segs=6, rings=4)
    # small peaked roof sitting just above the cross top
    poly_prism('capL', [(-1.6, 0), (0, 1.1), (1.6, 0), (1.6, 0.16), (0, 1.26), (-1.6, 0.16)], 1.6,
               loc=(0, 0.8, 1.8 + 7.4), key='wj_plank_b', rot=(90, 0, 0))
    box('ridge', (0.3, 1.6, 0.25), loc=(0, 0, 1.8 + 8.5), key='wj_timber_d')
    # wreath on the cross
    torus('wreath', 0.85, 0.22, loc=(0, -0.4, 1.8 + 4.4), key='wj_ivy', segs=16, rsegs=6, rot=(90, 0, 0))
    for i in range(7):
        a = math.radians(360 / 7 * i)
        ball('fl%d' % i, 0.17, loc=(math.cos(a) * 0.85, -0.45, 1.8 + 4.4 + math.sin(a) * 0.85),
             key=rnd.choice(['wj_banner_r', 'wj_gold']), segs=6, rings=4)
    # offerings: bowl + flowers at foot
    lathe('bowl', [(0.0, 0.0), (0.5, 0.0), (0.56, 0.4), (0.0, 0.12)], loc=(1.0, -1.0, 1.3), key='wj_iron', segs=10)
    for i in range(6):
        a = rnd.uniform(0, 6.28)
        ball('off%d' % i, 0.16, loc=(math.cos(a) * 1.2, -1.2 + math.sin(a) * 0.4, 1.4), key=rnd.choice(['wj_banner_r', 'wj_gold']), segs=6, rings=4)
    return finalize('shrine_cross', smooth_angle=35)


def shrine_niche():
    """F08_17 - stone niche shrine with a statue, 9 tall: an arched niche on a plinth sheltering a small robed figure, flower offerings and a candle ledge."""
    reset()
    rnd = random.Random(817)
    # plinth + body
    box('plinth', (4.2, 3.4, 0.8), loc=(0, 0, 0.4), key='wj_stone', bev=0.1)
    box('body', (3.4, 2.8, 6.4), loc=(0, 0, 0.8 + 3.2), key='wj_ashlar', bev=0.05)
    # arched niche recess
    box('niche', (2.0, 1.4, 3.2), loc=(0, -0.7, 0.8 + 2.6), key='wj_stone_d')
    # arch top of niche
    nf = F(0, -1.4, 0.8 + 4.2, 0)
    half = [(-1.0, 0.0), (1.0, 0.0)]
    tube('archtop', [(math.cos(math.radians(a)) * 1.0, -1.4, 0.8 + 4.2 + math.sin(math.radians(a)) * 1.0) for a in range(0, 181, 20)],
         0.18, 'wj_ashlar', res=4)
    # robed figure (simple lathe body + head)
    lathe('robe', [(0.0, 0.0), (0.7, 0.0), (0.75, 1.6), (0.55, 2.4), (0.4, 2.7), (0.0, 2.8)], loc=(0, -0.6, 0.8 + 1.4), key='wj_ashlar_d', segs=12)
    ball('head', 0.4, loc=(0, -0.6, 0.8 + 4.3), key='wj_ashlar_d', segs=10, rings=8)
    # hood arc
    lathe('hood', [(0.42, 0.0), (0.5, 0.3), (0.3, 0.6), (0.0, 0.7)], loc=(0, -0.6, 0.8 + 4.2), key='wj_ashlar_d', segs=10)
    # pediment roof
    poly_prism('ped', [(-2.0, 0), (0, 1.3), (2.0, 0), (2.0, 0.2), (0, 1.5), (-2.0, 0.2)], 0.4,
               loc=(0, -1.5, 0.8 + 6.4), key='wj_ashlar', rot=(90, 0, 0))
    box('cornice', (3.8, 3.2, 0.5), loc=(0, 0, 0.8 + 6.4), key='wj_ashlar', bev=0.06)
    # candle ledge + candles + flower offerings
    box('ledge', (2.4, 0.6, 0.3), loc=(0, -1.6, 0.8 + 1.2), key='wj_ashlar')
    for sgn in (-1, 1):
        cyl('candle%d' % sgn, 0.13, 0.6, loc=(sgn * 0.7, -1.7, 0.8 + 1.35), key='wj_ashlar', verts=8)
        flame('fl%d' % sgn, (sgn * 0.7, -1.7, 0.8 + 1.95), h=0.45, r=0.13, seed=817 + sgn)
    for i in range(6):
        a = rnd.uniform(-1.4, 1.4)
        ball('off%d' % i, 0.13, loc=(a, -1.7 + rnd.uniform(-0.1, 0.1), 0.8 + 1.35 + 0.05), key=rnd.choice(['wj_banner_r', 'wj_gold']), segs=6, rings=4)
    return finalize('shrine_niche', smooth_angle=30)


BATCHES = {
    'bridges': ('v4_roads', [
        ('F08_01_stone_bridge_arch', stone_bridge_arch, (1.0, -1.1, 0.4)),
        ('F08_02_stone_bridge_slab', stone_bridge_slab, (1.0, -1.1, 0.4)),
        ('F08_03_stone_bridge_double', stone_bridge_double, (1.0, -1.0, 0.35)),
        ('F08_04_wooden_footbridge', wooden_footbridge, (1.0, -1.1, 0.4)),
        ('F08_05_wooden_trestle', wooden_trestle, (1.0, -1.0, 0.4)),
        ('F08_06_wooden_covered', wooden_covered, (1.0, -1.0, 0.35)),
        ('F08_07_ruined_bridge', ruined_bridge, (1.0, -1.1, 0.4)),
    ]),
    'markers': ('v4_roads', [
        ('F08_08_signpost_crossroads', signpost_crossroads, (1.0, -1.25, 0.3)),
        ('F08_09_signpost_stone', signpost_stone, (1.0, -1.25, 0.3)),
        ('F08_10_signpost_leaning', signpost_leaning, (1.0, -1.25, 0.3)),
        ('F08_11_milestone_carved', milestone_carved, (1.0, -1.25, 0.35)),
        ('F08_12_milestone_mossy', milestone_mossy, (1.0, -1.25, 0.35)),
    ]),
    'gates_shrines': ('v4_roads', [
        ('F08_13_gate_arch_stone', gate_arch_stone, (1.0, -1.1, 0.35)),
        ('F08_14_gate_arch_timber', gate_arch_timber, (1.0, -1.1, 0.35)),
        ('F08_15_shrine_stone', shrine_stone, (1.0, -1.2, 0.35)),
        ('F08_16_shrine_cross', shrine_cross, (1.0, -1.2, 0.35)),
        ('F08_17_shrine_niche', shrine_niche, (1.0, -1.2, 0.35)),
    ]),
}
