"""v4_wj_water - worker wj, F10 water and coast props (lily pads, small waterfalls, docks, beach props).
1 unit = 1 stud, Z up, front faces -Y. Water level is z=0 for floating pieces; finalize moves origin to bottom centre.
"""
import math, random
import bmesh
from mathutils import Vector
import kitlib
from kitlib import (reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, bevel,
                    top_paint, _obj_from_bm)
import v4util
from kitlib import flame
from nature import rock, blob
from arch import F, railing, nm

PAL = kitlib.PAL
PAL['wj_pad']      = ((62, 110, 58),   'LeafyGrass',  0.0, 0.90, 0)
PAL['wj_pad_d']    = ((44, 86, 48),    'LeafyGrass',  0.0, 0.90, 0)
PAL['wj_pad_r']    = ((88, 120, 52),   'LeafyGrass',  0.0, 0.90, 0)
PAL['wj_petal_w']  = ((238, 236, 228), 'SmoothPlastic', 0.0, 0.60, 0)
PAL['wj_petal_p']  = ((232, 160, 186), 'SmoothPlastic', 0.0, 0.60, 0)
PAL['wj_pollen']   = ((230, 196, 70),  'SmoothPlastic', 0.0, 0.55, 0)
PAL['wj_reed']     = ((96, 124, 58),   'LeafyGrass',  0.0, 0.90, 0)
PAL['wj_reed_d']   = ((150, 132, 78),  'Grass',       0.0, 1.00, 0)
PAL['wj_cattail']  = ((96, 66, 42),    'Wood',        0.0, 0.90, 0)
PAL['wj_water']    = ((64, 116, 132),  'Glass',       0.15, 0.06, 0)
PAL['wj_water_d']  = ((34, 62, 72),    'Glass',       0.10, 0.10, 0)
PAL['wj_water_fx'] = ((176, 214, 228), 'Glass',       0.10, 0.05, 0.12)
PAL['wj_foam']     = ((238, 246, 248), 'SmoothPlastic', 0.0, 0.55, 0)
PAL['wj_rock']     = ((120, 112, 102), 'Rock',        0.0, 0.95, 0)
PAL['wj_rock_d']   = ((92, 86, 78),    'Rock',        0.0, 0.95, 0)
PAL['wj_moss']     = ((86, 112, 50),   'Grass',       0.0, 1.00, 0)
PAL['wj_dock']     = ((138, 104, 72),  'WoodPlanks',  0.0, 0.85, 0)
PAL['wj_dock_b']   = ((118, 90, 66),   'WoodPlanks',  0.0, 0.90, 0)
PAL['wj_piling']   = ((80, 62, 48),    'Wood',        0.0, 0.95, 0)
PAL['wj_algae']    = ((58, 84, 50),    'Grass',       0.0, 1.00, 0)
PAL['wj_rope']     = ((178, 152, 104), 'Fabric',      0.0, 1.00, 0)
PAL['wj_iron']     = ((44, 42, 40),    'Metal',       0.80, 0.45, 0)
PAL['wj_glass_lit']= ((244, 186, 102), 'Glass',       0.0, 0.20, 0.42)
PAL['wj_sand']     = ((206, 186, 148), 'Sand',        0.0, 0.95, 0)
PAL['wj_sand_wet'] = ((168, 150, 118), 'Sand',        0.0, 0.95, 0)
PAL['wj_driftwood']= ((158, 146, 128), 'Wood',        0.0, 0.95, 0)
PAL['wj_shell']    = ((228, 214, 196), 'SmoothPlastic', 0.0, 0.55, 0)
PAL['wj_shell_p']  = ((226, 180, 170), 'SmoothPlastic', 0.0, 0.55, 0)
PAL['wj_starfish'] = ((214, 132, 72),  'SmoothPlastic', 0.0, 0.60, 0)
PAL['wj_crab']     = ((176, 70, 54),   'SmoothPlastic', 0.0, 0.55, 0)
PAL['wj_net']      = ((150, 128, 94),  'Fabric',      0.0, 1.00, 0)
PAL['wj_barrel']   = ((112, 84, 54),   'Wood',        0.0, 0.85, 0)


# ---------------------------------------------------------------- helpers
def lily_pad(name, x, y, r, rnd, key=None, notch=True):
    """Flat round leaf with a V notch, floating at z=0, slightly domed."""
    key = key or rnd.choice(['wj_pad', 'wj_pad_d', 'wj_pad_r'])
    pts = []
    n = 22
    gap = rnd.uniform(0.35, 0.6) if notch else 0.0
    for k in range(n):
        ang = gap / 2 + (2 * math.pi - gap) * k / (n - 1)
        rr = r * rnd.uniform(0.94, 1.0)
        pts.append((x + math.cos(ang) * rr, y + math.sin(ang) * rr))
    if notch:
        pts.append((x, y))
    o = poly_prism(name, pts, 0.08, loc=(0, 0, 0.02), key=key)
    return o


def water_lily(name, x, y, rnd, pink=False):
    """Layered flower sitting on the water."""
    pk = 'wj_petal_p' if pink else 'wj_petal_w'
    for layer in range(3):
        nrp = 8 - layer
        pr = 0.34 - layer * 0.07
        lift = 0.14 + layer * 0.08
        for k in range(nrp):
            ang = 2 * math.pi * k / nrp + layer * 0.4
            o = ball('%s_p%d_%d' % (name, layer, k), pr, loc=(x + math.cos(ang) * (0.3 - layer * 0.07), y + math.sin(ang) * (0.3 - layer * 0.07), lift),
                     key=pk, segs=6, rings=4, scale=(1.0, 0.42, 0.3))
            o.rotation_euler = (0, math.radians(-40 - layer * 12), ang)
    ball('%s_c' % name, 0.16, loc=(x, y, 0.34), key='wj_pollen', segs=8, rings=5, scale=(1, 1, 0.7))


def reed_clump(name, x, y, rnd, n=8, h=(3.0, 5.0), cattails=True):
    for i in range(n):
        a = rnd.uniform(0, 6.28); d = math.sqrt(rnd.random()) * 1.1
        px, py = x + math.cos(a) * d, y + math.sin(a) * d
        hh = rnd.uniform(*h)
        lean = (rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3))
        tube('%s_r%d' % (name, i), [(px, py, 0), (px + lean[0] * 0.5, py + lean[1] * 0.5, hh * 0.6), (px + lean[0], py + lean[1], hh)],
             0.05, rnd.choice(['wj_reed', 'wj_reed', 'wj_reed_d']), res=4, taper=[1, 0.8, 0.2], ures=2)
        if cattails and i % 3 == 0:
            cyl('%s_ct%d' % (name, i), 0.15, 0.8, loc=(px + lean[0] * 0.85, py + lean[1] * 0.85, hh * 0.8), key='wj_cattail', verts=8)


def water_sheet(name, x0, x1, y, z_top, z_bot, rnd, key='wj_water_fx', segs=12, lip=True):
    """A falling water sheet: a slightly rippled vertical strip from a lip (z_top) to the pool (z_bot),
    widening a touch at the base. Top embeds up into the ledge and bottom dips below the pool so it connects."""
    bm = bmesh.new()
    rows = []
    zt = z_top + 0.6   # embed into the ledge lip
    zb = z_bot - 0.4   # dip below the pool surface
    cx = (x0 + x1) / 2
    for i in range(segs + 1):
        t = i / segs
        z = zt - (zt - zb) * t
        flare = 1.0 + 0.35 * t           # widen toward the base
        yy = y + math.sin(t * 3.0) * 0.1 + 0.25 * t  # bow outward as it falls
        ax = cx - (x1 - x0) / 2 * flare
        bx = cx + (x1 - x0) / 2 * flare
        rows.append([bm.verts.new((ax, yy, z)), bm.verts.new((bx, yy, z))])
    for A, B in zip(rows, rows[1:]):
        bm.faces.new((A[0], A[1], B[1], B[0]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj_from_bm(name, bm, key)
    sol = o.modifiers.new('sol', 'SOLIDIFY'); sol.thickness = 0.3
    # curled pour-lip over the top edge
    if lip:
        tube('%s_lip' % name, [(x0, y - 0.2, z_top + 0.5), (cx, y + 0.1, z_top + 0.8), (x1, y - 0.2, z_top + 0.5)],
             0.35, key, res=4, ures=2)
    return o


def splash_foam(name, x, y, z, r, rnd, n=8):
    for i in range(n):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, r)
        ball('%s%d' % (name, i), rnd.uniform(0.3, 0.6), loc=(x + math.cos(a) * d, y + math.sin(a) * d, z + rnd.uniform(-0.1, 0.25)),
             key='wj_foam', segs=8, rings=5, scale=(1.2, 1.2, 0.6))


def pool_rim(name, x, y, z, rin, rout, rnd, key='wj_rock'):
    nseg = 14
    for i in range(nseg):
        a = 2 * math.pi * i / nseg
        r = rnd.uniform(rin, rout)
        rock('%s%d' % (name, i), rnd.uniform(0.7, 1.3), (x + math.cos(a) * r, y + math.sin(a) * r, z),
             rnd.choice([key, 'wj_rock_d']), seed=hash((name, i)) % 999, scale=(1.2, 1.0, 0.7), subdiv=1)


def dock_piling(name, x, y, top, rnd, r=0.5, key='wj_piling'):
    tube(name, [(x + rnd.uniform(-0.12, 0.12), y + rnd.uniform(-0.12, 0.12), -3.0), (x, y, top)], r, key, res=4, taper=[1.1, 1.0])
    cyl('%s_alg' % name, r * 1.08, 1.6, loc=(x, y, -2.6), key='wj_algae', verts=10)
    cyl('%s_cap' % name, r * 1.02, 0.14, loc=(x, y, top), key='wj_iron', verts=10)


def deck_planks_x(name, x0, x1, y0, y1, z, rnd, pw=1.2, t=0.35):
    """Planks running along Y (down the dock length), rows stepped along X."""
    nx = max(1, int((x1 - x0) / pw)); dx = (x1 - x0) / nx
    for i in range(nx):
        x = x0 + dx * (i + 0.5)
        box('%s%d' % (name, i), (dx - 0.1, y1 - y0 + rnd.uniform(-0.2, 0.1), t),
            loc=(x + rnd.uniform(-0.05, 0.05), (y0 + y1) / 2, z - t / 2),
            key=rnd.choice(['wj_dock', 'wj_dock_b']), rot=(0, rnd.uniform(-0.4, 0.4), 0), bev=0.03)


# ---------------------------------------------------------------- F10_01..02 lily pads
def lily_pad_cluster():
    """F10_01 - lily pad cluster, 8 wide: a scatter of round pads at water level with two white and one pink bloom."""
    reset()
    rnd = random.Random(1001)
    for i in range(9):
        a = rnd.uniform(0, 6.28); d = math.sqrt(rnd.random()) * 3.4
        lily_pad('pad%d' % i, math.cos(a) * d, math.sin(a) * d, rnd.uniform(0.8, 1.5), rnd)
    water_lily('ly0', 0.6, 0.4, rnd, pink=False)
    water_lily('ly1', -1.8, -1.2, rnd, pink=False)
    water_lily('ly2', 1.6, -1.8, rnd, pink=True)
    # a few lily buds
    for i in range(3):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(1, 3)
        lathe('bud%d' % i, [(0.0, 0.0), (0.2, 0.1), (0.24, 0.4), (0.1, 0.7), (0.0, 0.75)],
              loc=(math.cos(a) * d, math.sin(a) * d, 0.05), key='wj_petal_p' if i % 2 else 'wj_petal_w', segs=8)
    return finalize('lily_pad_cluster', smooth_angle=50)


def lily_pad_spread():
    """F10_02 - larger lily pad spread with reeds, 14 wide: many pads, several blooms, and two reed clumps with cattails at the edge."""
    reset()
    rnd = random.Random(1002)
    for i in range(18):
        a = rnd.uniform(0, 6.28); d = math.sqrt(rnd.random()) * 6.2
        lily_pad('pad%d' % i, math.cos(a) * d, math.sin(a) * d, rnd.uniform(0.8, 1.6), rnd)
    for (x, y, pink) in ((1.0, 0.6, False), (-2.6, -1.0, True), (2.8, -2.4, False), (-1.0, 2.6, True), (3.4, 2.0, False)):
        water_lily('ly%.0f_%.0f' % (x, y), x, y, rnd, pink=pink)
    reed_clump('reedA', -5.5, 4.2, rnd, n=9, h=(3.5, 5.5))
    reed_clump('reedB', 5.0, -4.5, rnd, n=8, h=(3.0, 5.0))
    # floating leaves tilting up
    for i in range(4):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(2, 6)
        o = lily_pad('up%d' % i, math.cos(a) * d, math.sin(a) * d, rnd.uniform(0.7, 1.0), rnd, notch=False)
        o.rotation_euler = (math.radians(rnd.uniform(10, 25)), 0, rnd.uniform(0, 6.28))
    return finalize('lily_pad_spread', smooth_angle=50)


# ---------------------------------------------------------------- F10_03..05 small waterfalls
def waterfall_step():
    """F10_03 - rock step waterfall, 12 wide x 10 tall: a stacked rock ledge with water sheets pouring into a foamy splash pool with a rock rim."""
    reset()
    rnd = random.Random(1003)
    W, H = 12.0, 10.0
    from mathutils import noise as _noise
    # back rock wall in layered strata, front face near y=-0.5
    z = 0
    i = 0
    while z < H:
        sh = rnd.uniform(2.0, 2.8)
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=4, use_grid_fill=True)
        off = Vector((1003 + i * 3.1, i * 1.7, 0))
        inset = 0.6 * i  # upper strata step back so lower ledges catch water
        for v in bm.verts:
            v.co.x *= W * rnd.uniform(0.95, 1.0); v.co.y *= 4.0; v.co.z *= sh
            n = _noise.noise(v.co * 0.45 + off)
            v.co.y += n * 1.0 + (1.0 if v.co.y > 0 else 0)
        o = _obj_from_bm('strat%d' % i, bm, rnd.choice(['wj_rock', 'wj_rock_d', 'wj_rock']))
        o.location = (0, 1.5 + inset, z + sh / 2)
        top_paint(o, 'wj_moss', 0.8, 1003 + i, noise_amt=0.18)
        z += sh * 0.88; i += 1
    # one main wide sheet pouring the full height, plus a shorter side sheet from a mid ledge
    water_sheet('main', -3.5, -0.5, -0.6, H - 0.8, 0.0, rnd)
    water_sheet('side', 1.5, 3.8, -0.4, H * 0.58, 0.0, rnd)
    # a couple of thin trickles between
    water_sheet('trk', 0.0, 0.8, -0.3, H * 0.4, 0.0, rnd, lip=False)
    # splash pool rim + dark water + foam where each sheet lands
    pool_rim('rim', 0, -1.0, 0.3, 4.5, 6.0, rnd)
    cyl('pool', 5.0, 0.3, loc=(0, -1.0, 0.0), key='wj_water_d', verts=24)
    splash_foam('foamA', -2.0, -0.6, 0.5, 2.2, rnd, n=7)
    splash_foam('foamB', 2.6, -0.5, 0.5, 1.8, rnd, n=5)
    return finalize('waterfall_step', smooth_angle=25)


def waterfall_cascade():
    """F10_04 - three-step cascade, 11 wide x 9 tall: water tumbling down three mossy rock shelves, each with its own foam line, into a small pool."""
    reset()
    rnd = random.Random(1004)
    W = 11.0
    steps = [(0.0, 8.5), (1.2, 5.5), (-0.8, 2.8)]  # (x_centre, shelf_top_z)
    for si, (xc, zt) in enumerate(steps):
        # shelf slab of rocks (front lip at y ~ 0)
        for k in range(5):
            x = xc - 3.0 + 6.0 * k / 4 + rnd.uniform(-0.3, 0.3)
            o = rock('shelf%d_%d' % (si, k), rnd.uniform(1.5, 2.3), (x, 1.2 + rnd.uniform(-0.3, 0.3), zt),
                     rnd.choice(['wj_rock', 'wj_rock_d']), seed=1004 + si * 5 + k, scale=(1.3, 1.1, 0.7), subdiv=1)
            top_paint(o, 'wj_moss', 0.7, 1004 + si * 5 + k, noise_amt=0.2)
        # water sheet falling from this shelf lip to the next shelf top (connected, overlapping)
        next_z = steps[si + 1][1] if si + 1 < len(steps) else 0.0
        water_sheet('ws%d' % si, xc - 1.8, xc + 1.8, -0.2, zt - 0.4, next_z, rnd)
        splash_foam('f%d' % si, xc, 0.4, next_z + 0.1, 1.8, rnd, n=5)
    # base pool
    cyl('pool', 4.0, 0.3, loc=(0, -0.3, 0.0), key='wj_water_d', verts=20)
    pool_rim('rim', 0, -0.3, 0.25, 3.6, 4.6, rnd)
    return finalize('waterfall_cascade', smooth_angle=25)


def waterfall_trickle():
    """F10_05 - trickle over a mossy ledge, 8 wide x 6 tall: a single thin stream dribbling over a heavily mossed boulder lip into a tiny clear pool with pebbles."""
    reset()
    rnd = random.Random(1005)
    # mossy boulder ledge
    for i in range(5):
        a = rnd.uniform(0, 6.28)
        o = rock('ldg%d' % i, rnd.uniform(1.6, 2.6), (math.cos(a) * 1.8, 1.5 + math.sin(a) * 0.8, 2.0 + rnd.uniform(0, 1.5)),
                 rnd.choice(['wj_rock', 'wj_rock_d']), seed=1005 + i, scale=(1.3, 1.1, 0.9), subdiv=2)
        top_paint(o, 'wj_moss', 0.6, 1005 + i, noise_amt=0.2)
    # single thin trickle
    water_sheet('trk', -0.5, 0.5, -0.2, 5.2, 0.4, rnd, segs=12)
    # tiny clear pool + pebbles
    cyl('pool', 2.6, 0.25, loc=(0, -0.3, 0.0), key='wj_water', verts=20)
    for i in range(10):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, 2.4)
        rock('pb%d' % i, rnd.uniform(0.2, 0.45), (math.cos(a) * d, -0.3 + math.sin(a) * d, 0.1),
             rnd.choice(['wj_rock', 'wj_rock_d']), seed=1005 + 20 + i, scale=(1.2, 1.0, 0.5), subdiv=1)
    splash_foam('foam', 0, -0.1, 0.3, 1.0, rnd, n=4)
    return finalize('waterfall_trickle', smooth_angle=25)


# ---------------------------------------------------------------- F10_06..07 docks
def dock_fishing():
    """F10_06 - small wooden fishing dock, 20 long x 6 wide: plank deck on pilings, a ladder to the water, a mooring post with rope, a bucket and a coiled line."""
    reset()
    rnd = random.Random(1006)
    L, Wd = 20.0, 6.0
    deck = 6.0
    y0, y1 = -L / 2, L / 2
    # pilings grid
    for x in (-Wd / 2 + 0.6, Wd / 2 - 0.6):
        for y in [y0 + 1 + (L - 2) * k / 5 for k in range(6)]:
            dock_piling('pl%.0f_%.0f' % (x, y), x, y, deck - 0.4, rnd)
    # cross bearers + stringers
    for y in [y0 + 1 + (L - 2) * k / 5 for k in range(6)]:
        box('bear%.0f' % y, (Wd + 0.4, 0.7, 0.7), loc=(0, y, deck - 0.75), key='wj_piling')
    for x in (-Wd / 2 + 0.6, Wd / 2 - 0.6):
        box('strg%.0f' % x, (0.6, L, 0.6), loc=(x, 0, deck - 0.45), key='wj_piling')
    # deck planks (run along Y, which is dock length)
    deck_planks_x('dk', -Wd / 2, Wd / 2, y0, y1, deck, rnd, pw=1.1)
    # mooring post with rope + cleat
    cyl('mpost', 0.4, 2.4, loc=(Wd / 2 - 0.8, y1 - 1.5, deck), key='wj_piling', verts=10)
    torus('mrope', 0.5, 0.1, loc=(Wd / 2 - 0.8, y1 - 1.5, deck + 1.3), key='wj_rope', segs=14, rsegs=5)
    tube('mrope2', [(Wd / 2 - 0.8, y1 - 1.5, deck + 1.0), (Wd / 2 + 0.5, y1 - 2.4, deck - 1.0), (Wd / 2 + 1.0, y1 - 3.5, -2.0)], 0.1, 'wj_rope', res=4, ures=3)
    # ladder down to water at the end
    lx = 0.0
    for sx in (-0.7, 0.7):
        tube('lr%.0f' % sx, [(lx + sx, y0 - 0.2, -2.5), (lx + sx, y0 - 0.2, deck + 0.2)], 0.09, 'wj_iron', res=4)
    for k in range(8):
        z = -2.0 + k * (deck + 1.5) / 7
        tube('lg%d' % k, [(lx - 0.7, y0 - 0.2, z), (lx + 0.7, y0 - 0.2, z)], 0.06, 'wj_iron', res=2)
    # bucket + coil
    lathe('bucket', [(0.0, 0.0), (0.4, 0.0), (0.46, 0.8), (0.4, 0.82), (0.0, 0.1)], loc=(-Wd / 2 + 1.2, y0 + 2.0, deck), key='wj_barrel', segs=10)
    # coil of rope flat on deck
    pts = []
    for i in range(44):
        a = 2 * math.pi * i / 12
        rr = 0.3 + (0.9 - 0.3) * i / 44
        pts.append((-Wd / 2 + 1.5 + math.cos(a) * rr, y0 + 4.0 + math.sin(a) * rr, deck + 0.14))
    tube('coil', pts, 0.13, 'wj_rope', res=4, ures=2)
    return finalize('dock_fishing', smooth_angle=30)


def dock_boat_landing():
    """F10_07 - boat landing with stone steps, 16 long: a stone quay edge with steps down to the water, a lantern post, mooring rings and a barrel."""
    reset()
    rnd = random.Random(1007)
    L, Wd = 16.0, 8.0
    deck = 6.0
    # stone quay block
    box('quay', (Wd, L, deck), loc=(0, 0, deck / 2), key='wj_piling' if False else 'wj_rock', bev=0.1)
    # ashlar face courses on the front (-y not applicable; front is water side -x here) -> front faces -X
    # paved top
    nx = int(Wd / 1.8); ny = int(L / 1.8)
    for i in range(nx):
        for j in range(ny):
            box('pv%d_%d' % (i, j), (Wd / nx - 0.12, L / ny - 0.12, 0.25),
                loc=(-Wd / 2 + Wd / nx * (i + 0.5), -L / 2 + L / ny * (j + 0.5), deck + 0.12),
                key=rnd.choice(['wj_rock', 'wj_rock_d']), rot=(0, 0, rnd.uniform(-2, 2)), bev=0.06)
    # steps down to water on the -X (water) side
    for s in range(6):
        z = deck - 0.6 - s * 1.0
        box('step%d' % s, (1.6, L * 0.55, 1.0), loc=(-Wd / 2 - 0.8 - s * 1.2, 0, z - 0.5),
            key=rnd.choice(['wj_rock', 'wj_rock_d']), bev=0.08)
    # algae on lower steps
    for s in range(3, 6):
        box('alg%d' % s, (1.65, L * 0.55, 0.2), loc=(-Wd / 2 - 0.8 - s * 1.2, 0, deck - 0.6 - s * 1.0 - 1.0), key='wj_algae')
    # lantern post
    cyl('lpb', 0.4, 0.6, loc=(Wd / 2 - 1.0, L / 2 - 1.2, deck + 0.25), key='wj_rock', verts=12)
    cyl('lp', 0.18, 5.0, loc=(Wd / 2 - 1.0, L / 2 - 1.2, deck + 0.4), key='wj_iron', verts=10)
    lathe('lg', [(0.0, 0.0), (0.44, 0.0), (0.44, 1.1), (0.2, 1.4), (0.0, 1.45)], loc=(Wd / 2 - 1.0, L / 2 - 1.2, deck + 5.3), key='wj_glass_lit', segs=8)
    lathe('lt', [(0.52, 0.0), (0.1, 0.5), (0.0, 0.6)], loc=(Wd / 2 - 1.0, L / 2 - 1.2, deck + 6.75), key='wj_iron', segs=8)
    # mooring rings on the quay edge
    for y in (-L / 3, L / 3):
        box('rb%.0f' % y, (0.5, 0.5, 0.5), loc=(-Wd / 2 + 0.25, y, deck - 1.2), key='wj_iron')
        torus('rg%.0f' % y, 0.5, 0.1, loc=(-Wd / 2 - 0.1, y, deck - 1.7), key='wj_iron', segs=12, rsegs=4, rot=(0, 90, 0))
    # barrel + coil
    lathe('barrel', [(0.0, 0.0), (0.62, 0.0), (0.74, 0.5), (0.8, 1.0), (0.74, 1.5), (0.62, 1.9), (0.0, 1.9)], loc=(Wd / 2 - 1.5, -L / 2 + 1.8, deck + 0.25), key='wj_barrel', segs=14)
    for zz in (0.3, 1.5):
        torus('bh%.0f' % zz, 0.8, 0.05, loc=(Wd / 2 - 1.5, -L / 2 + 1.8, deck + 0.25 + zz), key='wj_iron', segs=14, rsegs=4)
    return finalize('dock_boat_landing', smooth_angle=30)


# ---------------------------------------------------------------- F10_08..10 beach props
def driftwood_pile():
    """F10_08 - driftwood pile on sand, ~8 wide: bleached logs and branches crossed in a heap with a sand mound, some dry seaweed."""
    reset()
    rnd = random.Random(1008)
    # sand mound
    blob('sand', 3.5, (0, 0, -0.1), 'wj_sand', subdiv=2, amp=0.2, scale=(1.4, 1.2, 0.18), seed=1008)
    # crossed driftwood logs
    for i in range(7):
        a = rnd.uniform(0, math.pi)
        L = rnd.uniform(4, 7)
        c = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), 0.3 + i * 0.12))
        d = Vector((math.cos(a), math.sin(a), rnd.uniform(-0.05, 0.1)))
        p0, p1 = c - d * L / 2, c + d * L / 2
        mid = (p0 + p1) / 2 + Vector((rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3), 0.1))
        tube('log%d' % i, [tuple(p0), tuple(mid), tuple(p1)], rnd.uniform(0.2, 0.42), 'wj_driftwood', res=6, taper=[1, 0.85, 0.55], ures=3)
        # pale cut ends
        cyl('end%d' % i, rnd.uniform(0.2, 0.4), 0.05, loc=tuple(p1), key='wj_driftwood', verts=10)
    # branches/twigs
    for i in range(8):
        a = rnd.uniform(0, math.pi); L = rnd.uniform(1.5, 3)
        c = Vector((rnd.uniform(-2, 2), rnd.uniform(-2, 2), 0.4 + rnd.uniform(0, 0.6)))
        d = Vector((math.cos(a), math.sin(a), rnd.uniform(-0.1, 0.2)))
        tube('tw%d' % i, [tuple(c - d * L / 2), tuple(c + d * L / 2)], rnd.uniform(0.07, 0.14), 'wj_driftwood', res=4, taper=[1, 0.4])
    # dry seaweed clumps
    for i in range(4):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(1.5, 3)
        blob('sw%d' % i, rnd.uniform(0.4, 0.7), (math.cos(a) * d, math.sin(a) * d, 0.2), rnd.choice(['wj_algae', 'wj_reed_d']),
             subdiv=1, amp=0.4, scale=(1.3, 1.0, 0.4), seed=1008 + i)
    return finalize('driftwood_pile', smooth_angle=35)


def rock_pool():
    """F10_09 - shells, starfish and a rock pool, ~7 wide: a tide-pool ring of mossy rocks around clear water with shells, two starfish and pebbles on wet sand."""
    reset()
    rnd = random.Random(1009)
    # wet sand base
    blob('sand', 4.0, (0, 0, -0.08), 'wj_sand_wet', subdiv=2, amp=0.15, scale=(1.4, 1.3, 0.14), seed=1009)
    # rock pool rim
    nseg = 12
    for i in range(nseg):
        a = 2 * math.pi * i / nseg
        r = rnd.uniform(2.2, 2.8)
        o = rock('rim%d' % i, rnd.uniform(0.6, 1.1), (math.cos(a) * r, math.sin(a) * r, 0.2),
                 rnd.choice(['wj_rock', 'wj_rock_d']), seed=1009 + i, scale=(1.2, 1.1, 0.7), subdiv=1)
        if i % 2 == 0:
            top_paint(o, 'wj_algae', 0.6, 1009 + i)
    # clear pool water
    cyl('pool', 2.3, 0.2, loc=(0, 0, 0.05), key='wj_water', verts=22)
    # shells
    for i in range(6):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0.5, 3.2)
        x, y = math.cos(a) * d, math.sin(a) * d
        sh = lathe('shell%d' % i, [(0.0, 0.0), (0.3, 0.05), (0.38, 0.2), (0.28, 0.35), (0.0, 0.4)],
                   loc=(x, y, 0.1), key=rnd.choice(['wj_shell', 'wj_shell_p']), segs=10)
        sh.scale = (1.0, 0.7, 0.6)
        sh.rotation_euler = (rnd.uniform(0, 1), 0, rnd.uniform(0, 6.28))
    # two starfish
    for (sx, sy) in ((1.4, -1.0), (-1.6, 1.2)):
        for k in range(5):
            a = 2 * math.pi * k / 5
            o = ball('star%.0f_%d' % (sx, k), 0.4, loc=(sx + math.cos(a) * 0.3, sy + math.sin(a) * 0.3, 0.12),
                     key='wj_starfish', segs=6, rings=4, scale=(1.4, 0.4, 0.2))
            o.rotation_euler = (0, math.radians(-10), a)
        ball('starc%.0f' % sx, 0.22, loc=(sx, sy, 0.16), key='wj_starfish', segs=8, rings=5, scale=(1, 1, 0.4))
    # pebbles
    for i in range(10):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0.3, 3.4)
        rock('pb%d' % i, rnd.uniform(0.15, 0.35), (math.cos(a) * d, math.sin(a) * d, 0.08),
             rnd.choice(['wj_rock', 'wj_rock_d']), seed=1009 + 30 + i, scale=(1.2, 1.0, 0.5), subdiv=1)
    return finalize('rock_pool', smooth_angle=30)


def beach_fishing_gear():
    """F10_10 - fishing nets, crab pots and a half-buried oar on the sand, ~9 wide: a draped net with cork floats, two slatted crab pots, a crab, a buried rowing oar and shells."""
    reset()
    rnd = random.Random(1010)
    # sand mound
    blob('sand', 4.2, (0, 0, -0.1), 'wj_sand', subdiv=2, amp=0.18, scale=(1.5, 1.3, 0.16), seed=1010)
    # draped fishing net (sagging grid of thin tubes) over two short stakes
    for sx in (-1, 1):
        cyl('stake%d' % sx, 0.12, 2.4, loc=(sx * 2.5, 1.0, 0), key='wj_driftwood', verts=6)
    nx = 7
    for i in range(nx):
        x = -2.5 + 5.0 * i / (nx - 1)
        tube('nv%d' % i, [(x, 1.0, 2.2), (x * 0.9, 0.3, 1.1 - abs(x) * 0.1), (x * 0.8, -0.6, 0.2)], 0.025, 'wj_net', res=2, ures=3)
    for j in range(4):
        z = 2.0 - j * 0.5
        pts = []
        for i in range(nx):
            x = -2.5 + 5.0 * i / (nx - 1)
            sag = math.sin(math.pi * i / (nx - 1)) * 0.3
            pts.append((x, 1.0 - j * 0.35, z - sag))
        tube('nh%d' % j, pts, 0.025, 'wj_net', res=2, ures=2)
    # cork floats on the net
    for i in range(5):
        x = -2.3 + 4.6 * i / 4
        ball('cf%d' % i, 0.18, loc=(x, 1.0, 2.15), key='wj_starfish', segs=6, rings=4, scale=(1, 1, 1.3))
    # two crab pots (slatted domes)
    for (px, py) in ((-2.6, -2.2), (-1.2, -2.6)):
        for k in range(6):
            a = math.pi * (k + 0.5) / 6
            yy = py - math.cos(a) * 0.9
            zz = 0.1 + math.sin(a) * 0.9
            box('pot%.0f_%d' % (px, k), (1.8, 0.16, 0.08), loc=(px, yy, zz), key='wj_driftwood', rot=(math.degrees(a) - 90, 0, 0))
        for x in (px - 0.9, px + 0.9):
            for k in range(4):
                a = math.pi * (k + 1) / 5
                tube('potn%.0f_%d_%d' % (px, int(x), k), [(x, py, 0.1), (x, py - 0.9 * math.cos(a), 0.1 + 0.9 * math.sin(a))], 0.02, 'wj_net', res=2)
    # crab
    ball('crab', 0.45, loc=(1.6, -1.0, 0.25), key='wj_crab', segs=10, rings=6, scale=(1.3, 1.0, 0.45))
    for k in range(3):
        for sgn in (-1, 1):
            tube('leg%d%d' % (k, sgn), [(1.6 + sgn * 0.4, -1.0 + (k - 1) * 0.3, 0.2), (1.6 + sgn * 0.9, -1.0 + (k - 1) * 0.4, 0.05)], 0.05, 'wj_crab', res=3)
    for sgn in (-1, 1):
        ball('claw%d' % sgn, 0.18, loc=(1.6 + sgn * 0.6, -1.5, 0.25), key='wj_crab', segs=6, rings=4, scale=(1.4, 0.8, 0.6))
    # half-buried rowing oar
    o = tube('oar', [(2.0, 2.5, 0.0), (0.0, 1.5, 0.3), (-2.5, 0.5, -0.2)], 0.12, 'wj_driftwood', res=6, taper=[0.6, 1.0, 1.0], ures=3)
    box('blade', (1.0, 0.1, 0.5), loc=(2.6, 2.9, 0.1), key='wj_driftwood', rot=(0, 0, 25), bev=0.05)
    # scattered shells
    for i in range(6):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(1, 3.5)
        sh = lathe('shell%d' % i, [(0.0, 0.0), (0.26, 0.05), (0.32, 0.2), (0.2, 0.32), (0.0, 0.36)],
                   loc=(math.cos(a) * d, math.sin(a) * d, 0.08), key=rnd.choice(['wj_shell', 'wj_shell_p']), segs=10)
        sh.scale = (1.0, 0.7, 0.55); sh.rotation_euler = (rnd.uniform(0, 1), 0, rnd.uniform(0, 6.28))
    return finalize('beach_fishing_gear', smooth_angle=30)


BATCHES = {
    'lily': ('v4_water', [
        ('F10_01_lily_pad_cluster', lily_pad_cluster, (0.6, -1.0, 0.7)),
        ('F10_02_lily_pad_spread', lily_pad_spread, (0.6, -1.0, 0.75)),
    ]),
    'waterfalls': ('v4_water', [
        ('F10_03_waterfall_step', waterfall_step, (1.0, -1.2, 0.35)),
        ('F10_04_waterfall_cascade', waterfall_cascade, (1.0, -1.2, 0.35)),
        ('F10_05_waterfall_trickle', waterfall_trickle, (1.0, -1.2, 0.4)),
    ]),
    'docks_beach': ('v4_water', [
        ('F10_06_dock_fishing', dock_fishing, (1.0, -1.1, 0.4)),
        ('F10_07_dock_boat_landing', dock_boat_landing, (-1.1, -1.0, 0.4)),
        ('F10_08_driftwood_pile', driftwood_pile, (1.0, -1.2, 0.5)),
        ('F10_09_rock_pool', rock_pool, (0.8, -1.1, 0.6)),
        ('F10_10_beach_fishing_gear', beach_fishing_gear, (1.0, -1.1, 0.5)),
    ]),
}
