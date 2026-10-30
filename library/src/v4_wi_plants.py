"""wi F05 - undergrowth (12 models) -> v4_plants.
Bushes, hedge pieces, reeds, tall meadow grass, coastal grass.
Placed in the thousands: small tri counts, strong silhouettes, natural colour
variation inside each model, slightly irregular shapes. No neon.
Technique follows D06 (v4_d06.py) and v4_elf helpers. 1 unit = 1 stud, Z up,
front = -Y, origin bottom-centre (kitlib.finalize).
"""
import math, random
from mathutils import Vector
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, _obj_from_bm, top_paint
from v4_d06 import ribbon, blade, tuft, leafy_bush, blossom, moss_skirt
from v4_elf import nm
from nature import blob, rock

PI = math.pi
PAL = kitlib.PAL
# wi palette: a few straw/seedhead and shell tones not in the base set
PAL['wi_straw']      = ((196, 176, 108), 'Grass',        0.00, 1.00, 0)
PAL['wi_straw_pale'] = ((214, 200, 142), 'Grass',        0.00, 1.00, 0)
PAL['wi_seed']       = ((168, 142, 86),  'Grass',        0.00, 1.00, 0)
PAL['wi_cattail']    = ((110, 74, 44),   'SmoothPlastic',0.00, 0.80, 0)
PAL['wi_reed_green'] = ((96, 134, 72),   'Grass',        0.00, 1.00, 0)
PAL['wi_sand']       = ((214, 196, 150), 'Sand',         0.00, 1.00, 0)
PAL['wi_sea_oat']    = ((198, 182, 120), 'Grass',        0.00, 1.00, 0)
PAL['wi_shell']      = ((228, 214, 196), 'SmoothPlastic',0.00, 0.55, 0)
PAL['wi_shell_pink'] = ((224, 190, 182), 'SmoothPlastic',0.00, 0.55, 0)
PAL['wi_juniper']    = ((70, 104, 84),   'LeafyGrass',   0.00, 0.90, 0)
PAL['wi_juniper_b']  = ((92, 122, 96),   'LeafyGrass',   0.00, 0.90, 0)
PAL['wi_berry_red']  = ((168, 46, 44),   'SmoothPlastic',0.00, 0.45, 0)

LEAFK = ('ev_leaf_a', 'ev_leaf_b', 'ev_leaf_c', 'ev_leaf_d')
GRASSK = ('ev_leaf_a', 'ev_leaf_c', 'ev_leaf_d', 'ev_fern')
STRAWK = ('wi_straw', 'wi_straw_pale', 'wi_seed', 'ev_leaf_d')


# ---------------------------------------------------------------- shared
def grass_blade(x, y, z, h, ang, bend, w, key, tipkey=None):
    """Tapered blade that leans and arcs over, optional seed head at the tip."""
    d = Vector((math.cos(ang), math.sin(ang), 0))
    side = Vector((-d.y, d.x, 0))
    pts = [Vector((x, y, z)) + d * bend * t * t * h + Vector((0, 0, h * t * (1 - 0.12 * t))) for t in (0, 0.33, 0.66, 1.0)]
    ribbon(nm('gb'), pts, [w, w * 0.9, w * 0.55, 0.015], [side] * 4, key, 1.0, 0.025)
    if tipkey:
        ball(nm('sh'), w * 1.7, loc=tuple(pts[-1]), key=tipkey, segs=5, rings=4, scale=(1.0, 1.0, 2.6))


def grass_clump(x, y, z, rnd, n, hrange, keys, w=0.13, bend=(0.3, 0.7), seedkey=None, seedprob=0.0):
    for i in range(n):
        k = rnd.choice(keys)
        tk = seedkey if (seedkey and rnd.random() < seedprob) else None
        grass_blade(x + rnd.uniform(-0.35, 0.35), y + rnd.uniform(-0.35, 0.35), z,
                    rnd.uniform(*hrange), rnd.uniform(0, 2 * PI), rnd.uniform(*bend), w, k, tk)


# ================================================================ F05_01..04 bushes
# Low-poly leaf mound: one smooth core + a shell of SMALL subdiv-1 leaf blobs.
# Placed in the thousands, so budget is <= 4k tris: subdiv-1 blob ~80 tris each.
def leaf_mound(seed, size, n=30, wide=1.15, tall=0.9, core_key='ev_leaf_b'):
    rnd = random.Random(seed)
    # smooth core gives the solid body with no see-through gaps
    blob(nm('core'), size * 0.47, (0, 0, size * 0.4), core_key, subdiv=2, amp=0.22,
         scale=(wide, wide, tall), seed=seed, flat_bottom=-size * 0.28)
    pts = []
    for i in range(n):
        t = (i + 0.5) / n
        el = math.asin(t * 0.97)
        az = i * 2.39996
        R = size * 0.5
        p = (math.cos(az) * math.cos(el) * R * wide, math.sin(az) * math.cos(el) * R * wide,
             size * 0.30 + math.sin(el) * R * tall * 1.15)
        r = size * rnd.uniform(0.12, 0.19)
        if el > 0.8:
            k = rnd.choice(('ev_leaf_c', 'ev_leaf_a'))
        elif el < 0.35:
            k = rnd.choice(('ev_leaf_b', 'ev_leaf_d'))
        else:
            k = rnd.choice(LEAFK)
        blob(nm('lc'), r, p, k, subdiv=1, amp=0.35, scale=(1, 1, 0.72), seed=rnd.randint(0, 999), detail=0.3)
        pts.append((p, el, az))
    return rnd, pts


def bush_round():
    """F05_01 round leafy shrub with grass and a stone at its foot."""
    reset()
    rnd, _ = leaf_mound(1101, 6.6, n=30, wide=1.15, tall=0.92)
    grass_clump(4.2, -1.0, 0.0, rnd, 5, (1.2, 2.2), GRASSK)
    grass_clump(-3.8, 2.2, 0.0, rnd, 5, (1.2, 2.2), GRASSK)
    rock(nm('rk'), 0.9, (3.6, 2.6, 0.0), 'ev_stone_dark', seed=2)
    return finalize('bush_round', smooth_angle=55)


def bush_flower():
    """F05_02 flowering bush: dense leaves with small white and pink blooms."""
    reset()
    size, wide, tall = 6.8, 1.12, 0.95
    rnd, _ = leaf_mound(1102, size, n=30, wide=wide, tall=tall)
    for i in range(26):
        az = rnd.uniform(0, 2 * PI)
        el = math.asin(rnd.uniform(0.1, 0.95))
        R = size * 0.5
        nrm = (math.cos(az) * math.cos(el), math.sin(az) * math.cos(el), math.sin(el))
        p = (nrm[0] * (R * wide + size * 0.08), nrm[1] * (R * wide + size * 0.08),
             size * 0.30 + nrm[2] * (R * tall * 1.15 + size * 0.07))
        blossom(p, nrm, size * 0.034, rnd.choice(('ev_petal_cream', 'ev_petal_cream', 'ev_petal_pink')), 'ev_petal_gold', n=4)
    grass_clump(4.3, 0.6, 0.0, rnd, 4, (1.0, 1.8), GRASSK)
    return finalize('bush_flower', smooth_angle=55)


def bush_berry():
    """F05_03 berry bush: leafy mound studded with small red berries."""
    reset()
    size, wide, tall = 6.4, 1.1, 0.9
    rnd, _ = leaf_mound(1103, size, n=30, wide=wide, tall=tall)
    for i in range(30):
        az = rnd.uniform(0, 2 * PI)
        el = math.asin(rnd.uniform(0.02, 0.9))
        R = size * 0.5
        nrm = (math.cos(az) * math.cos(el), math.sin(az) * math.cos(el), math.sin(el))
        p = (nrm[0] * (R * wide + size * 0.05), nrm[1] * (R * wide + size * 0.05),
             size * 0.28 + nrm[2] * (R * tall * 1.1 + size * 0.04))
        ball(nm('be'), size * rnd.uniform(0.026, 0.036),
             loc=(p[0], p[1], p[2]), key=rnd.choice(('wi_berry_red', 'wi_berry_red', 'ev_berry_red')), segs=6, rings=4)
    grass_clump(-4.0, -1.6, 0.0, rnd, 4, (1.0, 1.8), GRASSK)
    return finalize('bush_berry', smooth_angle=55)


def bush_juniper():
    """F05_04 low conifer shrub (juniper): dense spreading dusty blue-green mound."""
    reset()
    rnd = random.Random(1104)
    size = 7.0
    wide, tall = 1.15, 0.85   # a proper domed low shrub, not a splat
    blob(nm('core'), size * 0.48, (0, 0, size * 0.34), 'wi_juniper', subdiv=2, amp=0.24,
         scale=(wide, wide, tall), seed=4, flat_bottom=-size * 0.2)
    # shell of small rounded needled clumps
    n = 38
    for i in range(n):
        t = (i + 0.5) / n
        el = math.asin(t * 0.97)
        az = i * 2.39996
        R = size * 0.5
        p = (math.cos(az) * math.cos(el) * R * wide, math.sin(az) * math.cos(el) * R * wide,
             size * 0.30 + math.sin(el) * R * tall * 1.15)
        r = size * rnd.uniform(0.12, 0.18)
        k = rnd.choice(('wi_juniper', 'wi_juniper_b', 'wi_juniper'))
        blob(nm('spr'), r, p, k, subdiv=1, amp=0.4, scale=(1, 1, 0.72), seed=rnd.randint(0, 999), detail=0.4)
    # upright needle tips over the dome for a soft conifer silhouette
    for i in range(16):
        a = rnd.uniform(0, 2 * PI); d = rnd.uniform(0.6, size * 0.4)
        z0 = size * 0.3 + (1 - (d / (size * 0.5)) ** 2) * size * 0.3
        grass_blade(math.cos(a) * d, math.sin(a) * d, z0, rnd.uniform(0.8, 1.4), a, 0.2, 0.1,
                    rnd.choice(('wi_juniper', 'wi_juniper_b')))
    # a few pale juniper berries
    for i in range(10):
        a = rnd.uniform(0, 2 * PI); d = rnd.uniform(0.5, size * 0.4)
        ball(nm('jb'), 0.16, loc=(math.cos(a) * d, math.sin(a) * d, rnd.uniform(1.0, 2.2)), key='ev_berry', segs=5, rings=3)
    return finalize('bush_juniper', smooth_angle=50)


# ================================================================ F05_05..06 hedge
def _hedge_body(W, L, H, seed, wide=1.0):
    """Clipped hedge body: a boxy leaf mass with an uneven clipped top and stray twigs.
    Tileable: leaves fill the full W x L footprint so pieces butt end to end."""
    rnd = random.Random(seed)
    # dense dark core box (slightly inset) so no see-through gaps
    box(nm('core'), (W - 1.0, L - 1.0, H - 1.2), loc=(0, 0, (H - 1.2) / 2 + 0.3), key='ev_leaf_b', bev=0.25, segs=1)
    # dense leaf shell: walk the two long faces, two ends, and the rounded top in a fine grid
    step = 1.05
    def put(px, py, pz, top=False):
        k = rnd.choice(('ev_leaf_c', 'ev_leaf_a')) if top else rnd.choice(LEAFK)
        blob(nm('lb'), rnd.uniform(0.6, 0.85), (px + rnd.uniform(-0.2, 0.2), py + rnd.uniform(-0.2, 0.2), pz + rnd.uniform(-0.15, 0.15)),
             k, subdiv=1, amp=0.4, scale=(1, 1, 0.8), seed=rnd.randint(0, 999), detail=0.35)
    nx = max(2, int(W / step))
    ny = max(2, int(L / step))
    nz = max(2, int((H - 0.6) / step))
    # long faces (+/-Y)
    for ix in range(nx):
        px = -W / 2 + (ix + 0.5) * W / nx
        for iz in range(nz):
            pz = 0.5 + (iz + 0.5) * (H - 0.9) / nz
            put(px, L / 2 - 0.3, pz)
            put(px, -L / 2 + 0.3, pz)
    # ends (+/-X)
    for iy in range(ny):
        py = -L / 2 + (iy + 0.5) * L / ny
        for iz in range(nz):
            pz = 0.5 + (iz + 0.5) * (H - 0.9) / nz
            put(W / 2 - 0.3, py, pz)
            put(-W / 2 + 0.3, py, pz)
    # rounded, uneven clipped top
    for ix in range(nx):
        px = -W / 2 + (ix + 0.5) * W / nx
        for iy in range(ny):
            py = -L / 2 + (iy + 0.5) * L / ny
            drop = rnd.uniform(0, 0.7)
            put(px, py, H - 0.6 - drop, top=True)
    # a short woody base line showing between leaves
    box(nm('base'), (W - 0.2, L - 0.2, 0.5), loc=(0, 0, 0.25), key='ev_bark', bev=0.05)
    # a few stray twigs poking out of the top
    for i in range(int(W / 3)):
        x = rnd.uniform(-W / 2 + 0.5, W / 2 - 0.5)
        y = rnd.uniform(-L / 2 + 0.4, L / 2 - 0.4)
        a = rnd.uniform(0, 2 * PI)
        d = Vector((math.cos(a), math.sin(a), 0))
        tube(nm('tw'), [(x, y, H - 0.4), (x + d.x * 0.6, y + d.y * 0.6, H + rnd.uniform(0.3, 0.9))],
             0.05, 'ev_bark', res=4, ures=2)
    return rnd


def hedge_straight():
    """F05_05 straight hedge piece, 12 long x 4 wide x 5 tall, tileable end to end."""
    reset()
    _hedge_body(12.0, 4.0, 5.0, 1105)
    return finalize('hedge_straight', smooth_angle=55)


def hedge_corner():
    """F05_06 hedge corner (L-shape), same 4 x 5 cross-section, tiles with the straight piece."""
    reset()
    rnd = random.Random(1106)
    arm, W, H = 8.0, 4.0, 5.0
    c = arm / 2 - W / 2   # centreline offset of each arm
    # two dark cores (slightly inset) forming the L
    box(nm('cx'), (arm, W - 1.0, H - 1.2), loc=(c, -c, (H - 1.2) / 2 + 0.3), key='ev_leaf_b', bev=0.25, segs=1)
    box(nm('cy'), (W - 1.0, arm, H - 1.2), loc=(-c, c, (H - 1.2) / 2 + 0.3), key='ev_leaf_b', bev=0.25, segs=1)

    def put(px, py, pz, top=False):
        k = rnd.choice(('ev_leaf_c', 'ev_leaf_a')) if top else rnd.choice(LEAFK)
        blob(nm('lb'), rnd.uniform(0.6, 0.85), (px + rnd.uniform(-0.2, 0.2), py + rnd.uniform(-0.2, 0.2), pz + rnd.uniform(-0.15, 0.15)),
             k, subdiv=1, amp=0.4, scale=(1, 1, 0.8), seed=rnd.randint(0, 999), detail=0.35)

    step = 1.05
    nz = max(2, int((H - 0.6) / step))
    # shell each arm: sides (both long faces), top; the shared corner overlaps harmlessly
    for horiz in (True, False):
        nlen = int(arm / step)
        for i in range(nlen):
            t = (i + 0.5) / nlen
            run = -arm / 2 + t * arm + c   # position along the arm
            for side in (-1.3, 0.0, 1.3):  # near + far face and middle (top coverage)
                px, py = (run, -c + side) if horiz else (-c + side, run)
                for iz in range(nz):
                    pz = 0.5 + (iz + 0.5) * (H - 0.9) / nz
                    if abs(side) > 0.6 or pz > H - 1.4:   # faces and top only
                        put(px, py, pz, top=(pz > H - 1.4))
            # uneven top ridge
            px, py = (run, -c) if horiz else (-c, run)
            put(px, py, H - 0.6 - rnd.uniform(0, 0.7), top=True)
    # outer end caps of each arm
    for (ex, ey, horiz) in ((arm / 2 - W / 2 + arm / 2, -c, True), (-c, arm / 2 - W / 2 + arm / 2, False)):
        for off in (-1.2, 0.0, 1.2):
            for iz in range(nz):
                pz = 0.5 + (iz + 0.5) * (H - 0.9) / nz
                px, py = (ex, ey + off) if horiz else (ex + off, ey)
                put(px, py, pz)
    # base woody lines
    box(nm('bx'), (arm, W - 0.2, 0.5), loc=(c, -c, 0.25), key='ev_bark', bev=0.05)
    box(nm('by'), (W - 0.2, arm, 0.5), loc=(-c, c, 0.25), key='ev_bark', bev=0.05)
    for i in range(5):
        x = rnd.uniform(-arm / 2, arm / 2); y = rnd.uniform(-arm / 2, arm / 2)
        a = rnd.uniform(0, 2 * PI); d = Vector((math.cos(a), math.sin(a), 0))
        tube(nm('tw'), [(x, y, H - 0.4), (x + d.x * 0.6, y + d.y * 0.6, H + rnd.uniform(0.3, 0.8))], 0.05, 'ev_bark', res=4, ures=2)
    return finalize('hedge_corner', smooth_angle=55)


# ================================================================ F05_07..08 reeds
def _reed(x, y, z, h, ang, rnd, cattail=False):
    d = Vector((math.cos(ang), math.sin(ang), 0))
    side = Vector((-d.y, d.x, 0))
    pts = [Vector((x, y, z)) + d * 0.35 * t * t * h + Vector((0, 0, h * t)) for t in (0, 0.4, 0.75, 1.0)]
    k = rnd.choice(('wi_reed_green', 'wi_reed_green', 'wi_straw'))
    ribbon(nm('rd'), pts, [0.1, 0.1, 0.07, 0.02], [side] * 4, k, 1.0, 0.03)
    if cattail:
        # brown sausage cattail head near the top
        top = pts[-1]
        mid = pts[-1].lerp(pts[-2], 0.4)
        lathe(nm('ct'), [(0, 0), (0.22, 0.1), (0.24, 0.9), (0.2, 1.3), (0, 1.45)],
              loc=(mid.x, mid.y, mid.z), key='wi_cattail', segs=7)
        # thin spike above
        tube(nm('sp'), [(top.x, top.y, top.z), (top.x + d.x * 0.1, top.y + d.y * 0.1, top.z + 1.0)], 0.03, 'wi_straw', res=4, ures=2)


def reed_clump():
    """F05_07 small reed clump, a dozen slim reeds from a muddy base."""
    reset()
    rnd = random.Random(1107)
    moss_skirt(1.6, 7, sx=1.1, sy=1.0, key='ev_bark', h=0.12)
    for i in range(14):
        a = rnd.uniform(0, 2 * PI)
        d = rnd.uniform(0.0, 1.0)
        _reed(math.cos(a) * d, math.sin(a) * d, -0.2, rnd.uniform(5.0, 7.5), a + rnd.uniform(-0.3, 0.3), rnd,
              cattail=(i % 5 == 0))
    return finalize('reed_clump', smooth_angle=45)


def reed_stand():
    """F05_08 large reed stand with cattails, 6-9 tall, base below water line is fine."""
    reset()
    rnd = random.Random(1108)
    moss_skirt(3.4, 8, sx=1.2, sy=1.1, key='ev_bark', h=0.14)
    for (cx, cy) in ((0, 0), (2.4, 1.4), (-2.0, 1.8), (1.2, -2.2), (-1.8, -1.6)):
        for i in range(rnd.randint(7, 11)):
            a = rnd.uniform(0, 2 * PI); d = rnd.uniform(0.0, 1.2)
            _reed(cx + math.cos(a) * d, cy + math.sin(a) * d, -0.3, rnd.uniform(6.0, 9.0),
                  a + rnd.uniform(-0.25, 0.25), rnd, cattail=(rnd.random() < 0.28))
    # a couple of broad base leaves
    for i in range(6):
        a = rnd.uniform(0, 2 * PI)
        grass_blade(math.cos(a) * 2.6, math.sin(a) * 2.6, -0.1, rnd.uniform(3.0, 4.5), a, 0.5, 0.2, 'wi_reed_green')
    return finalize('reed_stand', smooth_angle=45)


# ================================================================ F05_09..10 tall meadow grass
def meadow_grass(seed, nclump, hrange, keys, seedkey, base_r=3.2):
    reset()
    rnd = random.Random(seed)
    blob(nm('base'), base_r, (0, 0, 0.0), 'ev_moss', subdiv=1, amp=0.2, scale=(1.0, 0.92, 0.09), seed=seed)
    pts = []
    tries = 0
    while len(pts) < nclump and tries < 400:
        tries += 1
        a = rnd.uniform(0, 2 * PI); dd = math.sqrt(rnd.random()) * base_r * 0.82
        p = (math.cos(a) * dd, math.sin(a) * dd)
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > 0.9 ** 2 for q in pts):
            pts.append(p)
    for (x, y) in pts:
        # a small fan of blades leaning out from a shared base point
        base_ang = rnd.uniform(0, 2 * PI)
        for b in range(rnd.randint(4, 6)):
            tk = seedkey if rnd.random() < 0.45 else None
            grass_blade(x + rnd.uniform(-0.2, 0.2), y + rnd.uniform(-0.2, 0.2), 0.0,
                        rnd.uniform(*hrange), base_ang + rnd.uniform(-0.9, 0.9),
                        rnd.uniform(0.2, 0.5), 0.11, rnd.choice(keys), tk)
    return rnd


def grass_tall_a():
    """F05_09 tall meadow grass, dense green with straw seed heads, 3-5 tall."""
    rnd = meadow_grass(1109, 13, (3.0, 5.0), ('ev_leaf_a', 'ev_leaf_c', 'ev_leaf_d', 'ev_fern'), 'wi_seed', base_r=3.2)
    return finalize('grass_tall_a', smooth_angle=45)


def grass_tall_b():
    """F05_10 tall meadow grass, sparser, drier straw/green mix, 3-5 tall."""
    rnd = meadow_grass(1110, 11, (3.2, 5.0), ('wi_straw', 'wi_straw_pale', 'ev_leaf_d', 'ev_leaf_a'), 'wi_seed', base_r=3.4)
    return finalize('grass_tall_b', smooth_angle=45)


# ================================================================ F05_11..12 coastal grass
def sea_oats():
    """F05_11 sea oats on a sand mound: tall pale stems with drooping seed heads."""
    reset()
    rnd = random.Random(1111)
    blob(nm('sand'), 4.4, (0, 0, 0.0), 'wi_sand', subdiv=2, amp=0.22, scale=(1.0, 0.9, 0.3), seed=11)
    # scatter of tall oats with a nodding seed head
    for i in range(22):
        a = rnd.uniform(0, 2 * PI); d = math.sqrt(rnd.random()) * 3.0
        x, y = math.cos(a) * d, math.sin(a) * d
        h = rnd.uniform(4.0, 6.0)
        ang = rnd.uniform(0, 2 * PI)
        dd = Vector((math.cos(ang), math.sin(ang), 0))
        side = Vector((-dd.y, dd.x, 0))
        # stem leans then the seed head droops over
        pts = [Vector((x, y, 0.2)), Vector((x, y, 0.2)) + dd * 0.3 * h * 0.3 + Vector((0, 0, h * 0.6)),
               Vector((x, y, 0.2)) + dd * 0.9 + Vector((0, 0, h))]
        tube(nm('st'), [tuple(p) for p in pts], 0.05, 'wi_sea_oat', res=4, ures=2)
        head = pts[-1]
        # drooping flattened seed head
        hp = [head, head + dd * 0.5 + Vector((0, 0, -0.1)), head + dd * 1.1 + Vector((0, 0, -0.7))]
        ribbon(nm('oh'), hp, [0.18, 0.22, 0.03], [side] * 3, 'wi_straw_pale', 0.5, 0.03)
    # a few short base blades
    for i in range(10):
        a = rnd.uniform(0, 2 * PI); d = rnd.uniform(0.5, 3.2)
        grass_blade(math.cos(a) * d, math.sin(a) * d, 0.15, rnd.uniform(1.5, 2.6), a, 0.5, 0.11, rnd.choice(('wi_sea_oat', 'ev_leaf_d')))
    return finalize('sea_oats', smooth_angle=45)


def dune_tuft():
    """F05_12 low windswept dune-grass tuft with a few shells, all blades combed one way."""
    reset()
    rnd = random.Random(1112)
    blob(nm('sand'), 3.4, (0, 0, 0.0), 'wi_sand', subdiv=2, amp=0.2, scale=(1.0, 0.95, 0.22), seed=12)
    wind = rnd.uniform(0, 2 * PI)   # prevailing wind direction: all blades lean this way
    for i in range(34):
        a = rnd.uniform(0, 2 * PI); d = math.sqrt(rnd.random()) * 2.4
        x, y = math.cos(a) * d, math.sin(a) * d
        lean = wind + rnd.uniform(-0.35, 0.35)
        grass_blade(x, y, 0.15, rnd.uniform(2.0, 3.4), lean, rnd.uniform(0.7, 1.0), 0.1,
                    rnd.choice(('wi_sea_oat', 'wi_straw', 'ev_leaf_d')))
    # shells half-buried
    for (sx, sy, sk) in ((1.8, -1.2, 'wi_shell'), (-2.0, 0.8, 'wi_shell_pink'), (0.6, 2.2, 'wi_shell')):
        lathe(nm('sl'), [(0, 0), (0.3, 0.05), (0.45, 0.18), (0.4, 0.3), (0.2, 0.34), (0, 0.32)],
              loc=(sx, sy, 0.1), key=sk, segs=8, rot=(rnd.uniform(-20, 20), rnd.uniform(-15, 15), rnd.uniform(0, 360)))
    return finalize('dune_tuft', smooth_angle=45)


BATCHES = {
    'bushes': ('v4_plants', [
        ('F05_01_bush_round', bush_round, (0.9, -1.1, 0.5)),
        ('F05_02_bush_flower', bush_flower, (0.9, -1.1, 0.5)),
        ('F05_03_bush_berry', bush_berry, (0.9, -1.1, 0.5)),
        ('F05_04_bush_juniper', bush_juniper, (0.9, -1.1, 0.45)),
    ]),
    'hedges': ('v4_plants', [
        ('F05_05_hedge_straight', hedge_straight, (0.55, -1.0, 0.4)),
        ('F05_06_hedge_corner', hedge_corner, (0.9, -1.0, 0.5)),
    ]),
    'reeds_grass': ('v4_plants', [
        ('F05_07_reed_clump', reed_clump, (0.7, -1.0, 0.35)),
        ('F05_08_reed_stand', reed_stand, (0.7, -1.0, 0.3)),
        ('F05_09_grass_tall_a', grass_tall_a, (0.8, -1.0, 0.45)),
        ('F05_10_grass_tall_b', grass_tall_b, (0.8, -1.0, 0.45)),
        ('F05_11_sea_oats', sea_oats, (0.8, -1.0, 0.4)),
        ('F05_12_dune_tuft', dune_tuft, (0.8, -1.0, 0.45)),
    ]),
}
