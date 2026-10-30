"""v4_d04 - elven ground buildings, part 1: shared helpers, round houses a/b/c, temple, palace.
Natural woods, mossy stone, green shingles, warm lanterns only (no neon). Front (door side) faces -Y. 1 unit = 1 stud.
"""
import math, random, bmesh
from mathutils import Vector
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, _obj_from_bm
import v4util as U
from v4_elf import nm, lantern, cabin, ivy_strand, mushrooms, fern, ladder
from nature import rock, blob

PI = math.pi
D = math.degrees
LEAFS = ('ev_leaf_a', 'ev_leaf_b', 'ev_leaf_c', 'ev_leaf_d')


# ------------------------------------------------------------------ geometry helpers
def prism_xz(pts, y0, y1, key):
    """Extrude a polygon given in (x, z) along Y from y0 to y1 (concave outlines allowed)."""
    bm = bmesh.new()
    f = [bm.verts.new((x, y0, z)) for x, z in pts]
    b = [bm.verts.new((x, y1, z)) for x, z in pts]
    n = len(pts)
    bm.faces.new(list(reversed(f)))
    bm.faces.new(b)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((f[i], f[j], b[j], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj_from_bm(nm('pz'), bm, key)


def shell(profile, segs, key, loc=(0, 0, 0), phase=0.0):
    """Revolve a CLOSED (r, z) cross-section around Z without end caps (roof tiers, rings)."""
    bm = bmesh.new()
    rings = [[bm.verts.new((math.cos(2 * PI * i / segs + phase) * r, math.sin(2 * PI * i / segs + phase) * r, z)) for i in range(segs)] for r, z in profile]
    for A, B in list(zip(rings, rings[1:])) + [(rings[-1], rings[0])]:
        for i in range(segs):
            j = (i + 1) % segs
            bm.faces.new((A[i], A[j], B[j], B[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj_from_bm(nm('shl'), bm, key)
    o.location = loc
    return o


def lamp(x, y, z, h=3.4, s=0.8):
    cyl(nm('lmp'), 0.12, h, loc=(x, y, z), key='ev_wood_dark', verts=6)
    lantern(x, y, z + h + 1.12 * s, s=s, hang=False)


def steps(a, r0, z_top, n, width, key='ev_stone', depth=1.05):
    """Stone steps leaving a round base toward angle a. Highest step nearest to the building."""
    for j in range(n):
        top = z_top * (1 - (j + 1) / (n + 1))
        r = r0 + depth * 0.5 + j * depth
        box(nm('stp'), (depth, width, top), loc=(math.cos(a) * r, math.sin(a) * r, top / 2), key=key, rot=(0, 0, D(a)), bev=0.06)


def house_base(R, fh, da, key='ev_stone_dark', nsteps=3, width=3.8):
    cyl(nm('fnd'), R + 0.9, fh, loc=(0, 0, 0), key=key, verts=30)
    torus(nm('fcr'), R + 0.9, 0.22, loc=(0, 0, fh), key='ev_stone', segs=30, rsegs=5)
    steps(da, R + 0.9, fh, nsteps, width)


def flagstones(a, r0, n, rnd, w=1.5):
    for i in range(n):
        r = r0 + i * 1.7 + rnd.uniform(-0.15, 0.15)
        off = rnd.uniform(-0.45, 0.45)
        tx, ty = -math.sin(a), math.cos(a)
        cyl(nm('fl'), w * rnd.uniform(0.7, 1.0), 0.14, loc=(math.cos(a) * r + tx * off, math.sin(a) * r + ty * off, 0.0), key='ev_stone', verts=7, rot=(0, 0, rnd.uniform(0, 60)))


def planter(cx, cy, z, R, a, rnd):
    x, y = cx + math.cos(a) * (R + 0.6), cy + math.sin(a) * (R + 0.6)
    box(nm('pln'), (0.6, 1.8, 0.55), loc=(x, y, z), key='ev_wood_dark', rot=(0, 0, D(a)), bev=0.04)
    tx, ty = -math.sin(a), math.cos(a)
    for k in range(5):
        t = (k - 2) * 0.34
        ball(nm('pl'), 0.22, loc=(x + tx * t, y + ty * t, z + 0.45 + rnd.uniform(0, 0.1)), key=rnd.choice(('ev_leaf_a', 'ev_leaf_c', 'ev_fern')), segs=6, rings=4)
        if k % 2 == 0:
            ball(nm('fw'), 0.13, loc=(x + tx * t, y + ty * t, z + 0.78), key=rnd.choice(('fl_white', 'fl_pink', 'fl_yellow')), segs=6, rings=4)


def wall_ivy(cx, cy, R, a0, z0, hmax, n, rnd, spread=0.3):
    for i in range(n):
        a = a0 + rnd.uniform(-spread, spread)
        zz = z0 + rnd.uniform(0.4, hmax) * rnd.random() ** 0.6
        o = ball(nm('ivw'), rnd.uniform(0.22, 0.38), loc=(cx + math.cos(a) * (R + 0.15), cy + math.sin(a) * (R + 0.15), zz), key=rnd.choice(LEAFS[:3]), segs=6, rings=4, scale=(0.5, 1, 1))
        o.rotation_euler = (0, 0, a)


def woodpile(x, y, z, ang):
    c, s = math.cos(ang), math.sin(ang)
    tx, ty = -s, c
    for row, n in enumerate((4, 3, 2)):
        for k in range(n):
            t = (k - (n - 1) / 2) * 0.5
            cyl(nm('log'), 0.23, 2.2, loc=(x + tx * t - c * 1.1, y + ty * t - s * 1.1, z + 0.25 + row * 0.42), key='ev_bark_light' if (k + row) % 2 else 'ev_wood_dark', verts=7, rot=(0, 90, D(ang)))
    for k in (-1.1, 1.1):
        cyl(nm('wps'), 0.1, 1.7, loc=(x + tx * k * 1.12, y + ty * k * 1.12, z), key='ev_wood_dark', verts=5)


def herb_bed(x, y, z, w, d, rnd, rot=0.0):
    box(nm('hbd'), (w, d, 0.5), loc=(x, y, z + 0.25), key='ev_wood_dark', rot=(0, 0, rot), bev=0.05)
    box(nm('hdt'), (w - 0.3, d - 0.3, 0.1), loc=(x, y, z + 0.52), key='dirt', rot=(0, 0, rot))
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    for i in range(int(w * d * 0.9)):
        u, v = rnd.uniform(-w / 2 + 0.3, w / 2 - 0.3), rnd.uniform(-d / 2 + 0.3, d / 2 - 0.3)
        ball(nm('hrb'), rnd.uniform(0.2, 0.34), loc=(x + c * u - s * v, y + s * u + c * v, z + 0.8), key=rnd.choice(('ev_leaf_a', 'ev_leaf_c', 'ev_fern', 'ev_leaf_d')), segs=6, rings=4, scale=(1, 1, 0.8))
        if i % 4 == 0:
            ball(nm('hfl'), 0.12, loc=(x + c * u - s * v, y + s * u + c * v, z + 1.12), key=rnd.choice(('fl_white', 'fl_yellow', 'fl_pink', 'fl_purple')), segs=6, rings=4)


def bush(x, y, r, seed):
    blob(nm('bsh'), r, (x, y, r * 0.6), rnd_key(seed), subdiv=1, amp=0.3, scale=(1, 1, 0.8), seed=seed)


def rnd_key(seed):
    return LEAFS[seed % 4]


def door_simple(cx, cy, z, R, a, w=2.4, h=4.6):
    """A decorative upper door (balcony) set against the wall."""
    c, s = math.cos(a), math.sin(a)
    tx, ty = -s, c
    px, py = cx + c * (R + 0.08), cy + s * (R + 0.08)
    for k in range(3):
        off = (k - 1) * w / 3
        box(nm('ud'), (w / 3 - 0.04, 0.2, h), loc=(px + tx * off, py + ty * off, z + h / 2), key='ev_wood_dark' if k % 2 else 'ev_wood', rot=(0, 0, D(a) + 90), bev=0.03)
    for sd in (-1, 1):
        box(nm('udf'), (0.3, 0.4, h + 0.3), loc=(px + c * 0.1 + tx * sd * (w / 2 + 0.12), py + s * 0.1 + ty * sd * (w / 2 + 0.12), z + (h + 0.3) / 2), key='ev_wood_dark', rot=(0, 0, D(a) + 90), bev=0.04)
    box(nm('udl'), (w + 0.8, 0.44, 0.32), loc=(px + c * 0.1, py + s * 0.1, z + h + 0.15), key='ev_wood_dark', rot=(0, 0, D(a) + 90), bev=0.05)


def chimney(cx, cy, a, r, ztop):
    c, s = math.cos(a), math.sin(a)
    x, y = cx + c * r, cy + s * r
    box(nm('chb'), (2.4, 2.2, ztop * 0.55), loc=(cx + c * (r - 0.6), cy + s * (r - 0.6), ztop * 0.275), key='ev_stone_dark', rot=(0, 0, D(a)), bev=0.08)
    box(nm('chm'), (1.7, 1.5, ztop * 0.5), loc=(x, y, ztop * 0.55 + ztop * 0.25 - 0.1), key='ev_stone', rot=(0, 0, D(a)), bev=0.08)
    box(nm('chc'), (2.1, 1.9, 0.4), loc=(x, y, ztop + 0.1), key='ev_stone_dark', rot=(0, 0, D(a)), bev=0.05)
    box(nm('cht'), (0.9, 0.8, 0.5), loc=(x, y, ztop + 0.5), key='iron', rot=(0, 0, D(a)))


def window_angles(da, n):
    return [da + off for off in (1.25, -1.25, 2.4, -2.4)[:n]]


# ------------------------------------------------------------------ D04_01 round house a
def round_house_a():
    reset()
    rnd = random.Random(41)
    R, h, fh = 6.0, 7.4, 1.4
    da = -PI / 2
    house_base(R, fh, da)
    cabin(0, 0, fh, R, h, da, seed=41, windows=3)
    chimney(0, 0, PI / 2 + 0.5, R + 1.7, fh + h + 3.4)
    for a in window_angles(da, 3):
        planter(0, 0, fh + h * 0.58 - 1.0, R, a, rnd)
    wall_ivy(0, 0, R, da + 2.0, fh + 0.5, h - 0.8, 16, rnd)
    flagstones(da, R + 4.8, 6, rnd)
    for sd in (-1, 1):
        lamp(math.cos(da) * (R + 3.3) + sd * 2.9, math.sin(da) * (R + 3.3), 0.0, 3.4, 0.8)
    herb_bed(-8.6, -7.2, 0.0, 4.2, 2.4, rnd, 15)
    woodpile(5.6, 6.6, 0.0, -0.3)
    cyl(nm('brl'), 0.75, 1.6, loc=(8.1, 3.2, 0.0), key='ev_wood_dark', verts=10)
    for zz in (0.4, 1.2):
        torus(nm('brb'), 0.77, 0.05, loc=(8.1, 3.2, zz), key='iron', segs=12, rsegs=3)
    for i, (x, y) in enumerate(((-7.6, 4.4), (7.8, -5.0), (-4.8, 7.8))):
        bush(x, y, 1.5 + 0.2 * i, 3 + i)
    fern(-7.0, -2.2, 0.0, n=7, L=1.5, seed=3)
    mushrooms(6.4, 5.6, 0.0, 4, seed=8, scale=0.9)
    U.marker('mk_door', (math.cos(da) * (R + 0.6), math.sin(da) * (R + 0.6), fh + 2.0))
    return finalize('ev_round_house_a', smooth_angle=38)


# ------------------------------------------------------------------ D04_02 round house b (tall, outer curved stair and balcony)
def round_house_b():
    reset()
    rnd = random.Random(47)
    R, h, fh = 5.2, 11.6, 1.2
    da = -PI / 2
    house_base(R, fh, da, nsteps=3, width=3.6)
    cabin(0, 0, fh, R, h, da, seed=47, windows=4, stave_n=24, roof_rise=R * 1.35)
    # outer curved stair winding around the wall, up to a balcony
    rs = R + 1.7
    ns = 12
    a_s = da + 0.9
    dth = 0.2
    zb = fh + 0.5 * ns
    for k in range(ns):
        a = a_s + dth * k
        top = fh + 0.5 * (k + 1)
        box(nm('str'), (2.1, rs * dth * 1.06, 0.3), loc=(math.cos(a) * rs, math.sin(a) * rs, top - 0.15), key='ev_wood_light' if k % 2 else 'ev_wood', rot=(0, 0, D(a)), bev=0.03)
        if k % 3 == 1:
            xo, yo = math.cos(a) * (rs + 0.9), math.sin(a) * (rs + 0.9)
            cyl(nm('stp'), 0.22, top, loc=(xo, yo, 0.0), key='ev_wood_dark', verts=6)
    pts_o = [(math.cos(a_s + dth * k) * (rs + 1.0), math.sin(a_s + dth * k) * (rs + 1.0), fh + 0.5 * (k + 1) + 2.8) for k in range(ns)]
    tube(nm('hrl'), pts_o, 0.1, 'ev_wood_light', res=4, ures=3)
    for k in range(0, ns, 2):
        p = pts_o[k]
        cyl(nm('hps'), 0.1, 2.8, loc=(p[0], p[1], p[2] - 2.8), key='ev_wood', verts=6)
    # balcony arc at the top of the stair
    ab0 = a_s + dth * (ns - 1)
    nb = 11
    ab1 = ab0 + 0.13 * nb
    for k in range(nb):
        a = ab0 + 0.13 * (k + 0.5)
        box(nm('bal'), (2.4, rs * 0.13 * 1.06, 0.3), loc=(math.cos(a) * (rs + 0.15), math.sin(a) * (rs + 0.15), zb - 0.15), key='ev_wood_light' if k % 2 else 'ev_wood', rot=(0, 0, D(a)), bev=0.03)
    tube(nm('brm'), [(math.cos(ab0 + 0.13 * k) * (rs + 1.3), math.sin(ab0 + 0.13 * k) * (rs + 1.3), zb - 0.5) for k in range(nb + 1)], 0.22, 'ev_wood_dark', res=4, ures=3)
    pts_b = [(math.cos(ab0 + 0.13 * k) * (rs + 1.25), math.sin(ab0 + 0.13 * k) * (rs + 1.25)) for k in range(nb + 1)]
    for i, (x, y) in enumerate(pts_b):
        cyl(nm('bps'), 0.12, 2.9, loc=(x, y, zb), key='ev_wood', verts=6)
        if i % 5 == 0:
            cyl(nm('bsp'), 0.28, zb - 0.4, loc=(x, y, 0.0), key='ev_wood_dark', verts=6)
    tube(nm('brt'), [(x, y, zb + 2.9) for x, y in pts_b], 0.12, 'ev_wood_light', res=4, ures=3)
    tube(nm('brm2'), [(x, y, zb + 1.5) for x, y in pts_b], 0.08, 'ev_wood', res=4, ures=3)
    amid = ab0 + 0.13 * nb / 2
    door_simple(0, 0, zb, R, amid)
    lx, ly = math.cos(amid) * (rs + 1.25), math.sin(amid) * (rs + 1.25)
    for sd, aa in ((0, pts_b[0]), (1, pts_b[-1])):
        cyl(nm('gp'), 0.18, 3.7, loc=(aa[0], aa[1], zb), key='ev_wood_dark', verts=6)
        lantern(aa[0], aa[1], zb + 3.7 + 1.12 * 0.7, s=0.7, hang=False)
    for a in window_angles(da, 4)[:2]:
        planter(0, 0, fh + h * 0.58 - 1.0, R, a, rnd)
    wall_ivy(0, 0, R, da + 3.1, fh + 0.5, h - 1.0, 18, rnd, 0.5)
    flagstones(da, R + 4.8, 5, rnd)
    for sd in (-1, 1):
        lamp(math.cos(da) * (R + 3.3) + sd * 2.7, math.sin(da) * (R + 3.3), 0.0, 3.4, 0.8)
    herb_bed(7.6, -6.4, 0.0, 3.8, 2.2, rnd, -20)
    woodpile(-5.0, 7.4, 0.0, 3.4)
    for i, (x, y) in enumerate(((-7.4, -3.6), (6.6, 6.6))):
        bush(x, y, 1.6, 6 + i)
    fern(-7.0, 1.0, 0.0, n=7, L=1.5, seed=6)
    mushrooms(-6.5, -5.3, 0.0, 4, seed=2, scale=0.9)
    U.marker('mk_door', (math.cos(da) * (R + 0.6), math.sin(da) * (R + 0.6), fh + 2.0))
    U.marker('mk_door', (math.cos(amid) * (R + 0.6), math.sin(amid) * (R + 0.6), zb + 2.0))
    return finalize('ev_round_house_b', smooth_angle=38)


# ------------------------------------------------------------------ D04_03 round house c (main house, annex, laundry line, well)
def well(x, y, rot=0.0):
    cyl(nm('wl'), 1.5, 1.3, loc=(x, y, 0.0), key='ev_stone', verts=12)
    torus(nm('wlr'), 1.5, 0.2, loc=(x, y, 1.3), key='ev_stone_warm', segs=12, rsegs=4)
    cyl(nm('wlw'), 1.1, 0.1, loc=(x, y, 1.1), key='water', verts=12)
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    for sd in (-1, 1):
        cyl(nm('wlp'), 0.16, 4.2, loc=(x + c * sd * 1.45, y + s * sd * 1.45, 0.4), key='ev_wood_dark', verts=6)
    tube(nm('wlb'), [(x - c * 1.6, y - s * 1.6, 4.4), (x + c * 1.6, y + s * 1.6, 4.4)], 0.13, 'ev_wood', res=4)
    for sd in (-1, 1):
        box(nm('wlr2'), (3.6, 0.2, 0.2), loc=(x + c * 0 - s * sd * 0.0, y, 4.1), key='ev_wood_dark')
    prism_xz([(-2.2, 4.3), (2.2, 4.3), (0.0, 6.1)], y - 1.3, y + 1.3, 'ev_shingle_a').location.x = x
    cyl(nm('wlk'), 0.09, 1.4, loc=(x, y, 2.9), key='rope')
    cyl(nm('wlbk'), 0.28, 0.5, loc=(x, y, 2.45), key='ev_wood_dark', verts=8)


def laundry(x0, y0, x1, y1, rnd):
    for (x, y) in ((x0, y0), (x1, y1)):
        cyl(nm('lp'), 0.14, 5.0, loc=(x, y, 0.0), key='ev_wood_dark', verts=6)
    n = 9
    pts = [(x0 + (x1 - x0) * t / n, y0 + (y1 - y0) * t / n, 4.7 - 0.5 * (1 - (2 * t / n - 1) ** 2)) for t in range(n + 1)]
    tube(nm('ll'), pts, 0.04, 'rope', res=4, ures=2)
    keys = ('ev_banner_green', 'ev_banner_gold', 'canvas', 'canvas_b', 'ev_banner_green')
    for k, t in enumerate((1.5, 3.0, 4.6, 6.2, 7.7)):
        p = pts[int(t)]
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        box(nm('cl'), (0.9 + 0.2 * (k % 2), 0.05, 1.6 - 0.2 * (k % 3)), loc=(p[0], p[1], p[2] - 0.85), key=keys[k], rot=(0, 0, ang))


def round_house_c():
    reset()
    rnd = random.Random(53)
    R, h, fh = 6.4, 7.8, 1.4
    da = -PI / 2
    house_base(R, fh, da)
    cabin(0, 0, fh, R, h, da, seed=53, windows=3, roof_rise=R * 1.05)
    # annex: smaller round house tucked against the main one
    aa = PI / 2 + 0.55
    ax, ay = math.cos(aa) * (R + 2.6), math.sin(aa) * (R + 2.6)
    ra, ha = 3.5, 5.0
    cyl(nm('afn'), ra + 0.7, fh, loc=(ax, ay, 0.0), key='ev_stone_dark', verts=22)
    torus(nm('acr'), ra + 0.7, 0.18, loc=(ax, ay, fh), key='ev_stone', segs=22, rsegs=5)
    ada = aa - PI / 2 + 0.2
    steps_a = ada
    for j in range(2):
        top = fh * (1 - (j + 1) / 3.0)
        r = ra + 0.7 + 0.5 + j * 0.95
        box(nm('astp'), (0.95, 2.8, top), loc=(ax + math.cos(steps_a) * r, ay + math.sin(steps_a) * r, top / 2), key='ev_stone', rot=(0, 0, D(steps_a)), bev=0.05)
    cabin(ax, ay, fh, ra, ha, ada, seed=54, windows=2, roof_rise=ra * 1.2, stave_n=16)
    chimney(0, 0, -0.45, R + 1.7, fh + h + 3.2)
    for a in window_angles(da, 3)[:2]:
        planter(0, 0, fh + h * 0.58 - 1.0, R, a, rnd)
    wall_ivy(0, 0, R, 0.2, fh + 0.5, h - 0.8, 14, rnd, 0.5)
    wall_ivy(ax, ay, ra, aa + 0.6, fh + 0.5, ha - 0.8, 8, rnd, 0.4)
    flagstones(da, R + 4.8, 6, rnd)
    for sd in (-1, 1):
        lamp(math.cos(da) * (R + 3.3) + sd * 2.9, math.sin(da) * (R + 3.3), 0.0, 3.4, 0.8)
    well(-10.0, -7.5, 20)
    laundry(9.5, -3.0, 9.8, 5.8, rnd)
    woodpile(-8.4, 3.0, 0.0, 3.1)
    herb_bed(9.0, -9.2, 0.0, 3.6, 2.2, rnd, 10)
    for i, (x, y) in enumerate(((-9.0, 7.8), (6.2, -9.8), (-4.0, -10.6))):
        bush(x, y, 1.5 + 0.15 * i, 9 + i)
    fern(8.4, 8.8, 0.0, n=7, L=1.5, seed=12)
    mushrooms(-8.6, 0.4, 0.0, 4, seed=4, scale=0.9)
    U.marker('mk_door', (math.cos(da) * (R + 0.6), math.sin(da) * (R + 0.6), fh + 2.0))
    U.marker('mk_door', (ax + math.cos(ada) * (ra + 0.6), ay + math.sin(ada) * (ra + 0.6), fh + 2.0))
    return finalize('ev_round_house_c', smooth_angle=38)


# ------------------------------------------------------------------ D04_04 temple (round colonnade with a tiered green roof)
def temple():
    reset()
    rnd = random.Random(61)
    Rc = 12.6
    for i, (r, z0, hh, k) in enumerate(((17.6, 0.0, 0.7, 'ev_stone'), (16.4, 0.7, 0.7, 'ev_stone_warm'), (15.2, 1.4, 0.7, 'ev_stone'))):
        cyl(nm('tb'), r, hh, loc=(0, 0, z0), key=k, verts=40)
    zf = 2.1
    cyl(nm('flr'), 14.2, 0.15, loc=(0, 0, zf), key='ev_stone_warm', verts=40)
    ent = -PI / 2
    steps(ent, 15.2, 2.1, 3, 8.0, depth=1.2)
    prof = [(0, 0), (1.15, 0), (1.15, 0.5), (0.86, 0.75), (0.78, 1.1), (0.74, 10.6), (0.84, 11.1), (1.15, 11.4), (1.35, 11.9), (1.35, 12.4), (0, 12.4)]
    nc = 10
    for i in range(nc):
        a = ent + (i + 0.5) * 2 * PI / nc
        x, y = math.cos(a) * Rc, math.sin(a) * Rc
        lathe(nm('col'), prof, loc=(x, y, zf + 0.15), key='ev_stone_warm', segs=12)
        blob(nm('cm'), 0.7, (x + math.cos(a) * 0.6, y + math.sin(a) * 0.6, zf + 0.35), 'ev_moss', subdiv=1, amp=0.3, scale=(1, 1, 0.45), seed=i)
        if i in (1, 4, 7):
            pts = []
            for k in range(18):
                t = k / 17
                pts.append((x + math.cos(a * 1 + t * 9) * 0.88, y + math.sin(a + t * 9) * 0.88, zf + 1.5 + t * 8.5))
            tube(nm('ivs'), pts, 0.05, 'ev_leaf_b', res=4, ures=1)
            for k in range(0, 18, 2):
                ball(nm('ivl'), 0.2, loc=pts[k], key=LEAFS[k % 3], segs=6, rings=4, scale=(1, 1, 0.6))
    zt = zf + 0.15 + 12.4
    torus(nm('arc'), Rc, 0.78, loc=(0, 0, zt + 0.5), key='ev_stone_warm', segs=40, rsegs=6)
    torus(nm('crn'), Rc + 0.35, 0.34, loc=(0, 0, zt + 1.35), key='ev_stone', segs=40, rsegs=5)
    # tiered roof, upswept eaves
    rmax, H, nt = 15.2, 10.2, 9
    zr = zt + 1.4

    def f(r):
        return zr + H * (1 - r / rmax) ** 1.35 + 0.55 * max(0.0, (r / rmax - 0.86) / 0.14) ** 2
    rs = [rmax * (1 - k / nt) ** 0.92 for k in range(nt + 1)]
    for k in range(nt):
        ro, ri = rs[k], rs[k + 1] + 0.7
        lift = 0.34 * k
        sec = [(ro, f(ro) + lift), (ri, f(ri) + lift + 0.12), (ri, f(ri) + lift + 0.12 - 0.5), (ro, f(ro) + lift - 0.5)]
        shell(sec, 40, ('ev_shingle_a', 'ev_shingle_c', 'ev_shingle_a', 'ev_shingle_a')[k % 4], phase=0.0)
    for i in range(nc):   # rafters under the eaves
        a = ent + (i + 0.5) * 2 * PI / nc
        tube(nm('raf'), [(math.cos(a) * 3.0, math.sin(a) * 3.0, f(3.0) - 0.7), (math.cos(a) * 9.5, math.sin(a) * 9.5, f(9.5) - 0.7), (math.cos(a) * 15.2, math.sin(a) * 15.2, f(15.2) - 0.55)], 0.26, 'ev_wood_dark', res=4, ures=3)
    ztop = f(rs[-1] + 0.7) + 0.34 * nt
    cyl(nm('cup'), 1.4, 1.6, loc=(0, 0, ztop - 0.3), key='ev_wood_dark', verts=10)
    lathe(nm('cap'), [(0, 0), (1.9, 0), (1.5, 0.5), (0.6, 1.8), (0, 2.6)], loc=(0, 0, ztop + 1.2), key='ev_shingle_a', segs=10)
    cyl(nm('fin'), 0.12, 2.2, loc=(0, 0, ztop + 3.7), key='bronze', verts=6)
    ball(nm('finb'), 0.38, loc=(0, 0, ztop + 5.9), key='bronze', segs=8, rings=6)
    # interior: sapling shrine in a stone planter, lanterns, benches
    cyl(nm('pln'), 3.3, 0.9, loc=(0, 0, zf + 0.15), key='ev_stone', verts=20)
    torus(nm('plr'), 3.3, 0.22, loc=(0, 0, zf + 1.05), key='ev_stone_warm', segs=20, rsegs=4)
    cyl(nm('pld'), 3.0, 0.1, loc=(0, 0, zf + 1.0), key='dirt', verts=20)
    tube(nm('str'), [(0, 0, zf + 1.0), (0.3, 0.1, zf + 3.0), (-0.1, 0.2, zf + 5.2), (0.2, 0, zf + 6.4)], 0.42, 'ev_bark', res=4, taper=[1.5, 1.0, 0.7, 0.4], ures=3)
    for k in range(6):
        a = 2 * PI * k / 6
        tube(nm('stb'), [(0, 0.1, zf + 4.8), (math.cos(a) * 1.2, math.sin(a) * 1.2, zf + 5.8), (math.cos(a) * 2.4, math.sin(a) * 2.4, zf + 6.4)], 0.13, 'ev_bark', res=4, ures=2)
    for k in range(7):
        a = 2 * PI * k / 7
        blob(nm('stl'), 1.3, (math.cos(a) * 2.2, math.sin(a) * 2.2, zf + 6.5 + (k % 2) * 0.4), LEAFS[k % 4], subdiv=1, amp=0.3, scale=(1, 1, 0.8), seed=k)
    blob(nm('stl'), 1.7, (0.2, 0, zf + 7.4), 'ev_leaf_c', subdiv=1, amp=0.3, scale=(1, 1, 0.8), seed=40)
    for k in range(5):
        a = 2 * PI * k / 5 + 0.3
        ball(nm('flw'), 0.22, loc=(math.cos(a) * 2.5, math.sin(a) * 2.5, zf + 1.2), key='fl_white', segs=6, rings=4)
    for i in range(nc):
        a = ent + (i + 0.5) * 2 * PI / nc
        x, y = math.cos(a) * 9.6, math.sin(a) * 9.6
        zl = zt - 1.0
        tube(nm('lch'), [(x, y, f(9.6) - 0.6), (x, y, zl + 1.0)], 0.05, 'iron', res=4)
        lantern(x, y, zl, s=0.85, hang=True)
    for k in range(2):
        a = ent + PI + (k - 0.5) * 1.0 + 0.5
        for sg in range(4):
            aa = a - 0.28 + 0.14 * sg
            box(nm('bch'), (1.1, 12.0 * 0.14 + 0.2, 0.25), loc=(math.cos(aa) * 9.0, math.sin(aa) * 9.0, zf + 1.1), key='ev_wood_light', rot=(0, 0, D(aa)), bev=0.03)
        for sg in (-0.34, 0.34):
            aa = a + sg
            box(nm('bcl'), (0.8, 0.3, 0.95), loc=(math.cos(aa) * 9.0, math.sin(aa) * 9.0, zf + 0.62), key='ev_wood_dark', rot=(0, 0, D(aa)))
    for sd in (-1, 1):   # banners on the entrance columns
        a = ent + sd * 0.3
        x, y = math.cos(a) * (Rc + 1.0), math.sin(a) * (Rc + 1.0)
        box(nm('ban'), (0.12, 1.9, 6.4), loc=(x, y, zt - 4.4), key='ev_banner_green', rot=(0, 0, D(a) + 90) if False else (0, 0, D(a)))
        box(nm('bag'), (0.14, 1.9, 0.5), loc=(x, y, zt - 1.45), key='ev_banner_gold', rot=(0, 0, D(a)))
    for i in range(6):
        a = rnd.uniform(0, 2 * PI)
        rock(nm('gr'), rnd.uniform(0.8, 1.6), (math.cos(a) * rnd.uniform(18.5, 21), math.sin(a) * rnd.uniform(18.5, 21), 0.0), 'ev_stone_dark', seed=i)
    for i in range(5):
        a = rnd.uniform(0, 2 * PI)
        fern(math.cos(a) * 18.4, math.sin(a) * 18.4, 0.0, n=6, L=1.5, seed=i)
    for sd in (-1, 1):
        lamp(sd * 5.2, -19.4, 0.0, 3.6, 0.9)
    U.marker('mk_door', (0, -Rc - 1.0, zf + 2.0))
    U.marker('mk_deck', (0, 0, zf + 0.4))
    return finalize('ev_temple', smooth_angle=38)


# ------------------------------------------------------------------ D04_05 palace (great round hall, two towers, galleries, porch)
def palace():
    reset()
    rnd = random.Random(71)
    z0 = 1.4
    box(nm('plinth'), (70.0, 44.0, z0), loc=(0, 0, z0 / 2), key='ev_stone', bev=0.2)
    box(nm('plint2'), (66.0, 40.0, 0.35), loc=(0, 0, z0 + 0.17), key='ev_stone_warm', bev=0.1)
    z0 += 0.35
    da = -PI / 2
    RH, hh = 12.0, 13.0
    cyl(nm('hfn'), RH + 0.8, 0.9, loc=(0, 0, z0 - 0.35), key='ev_stone_dark', verts=36)
    cabin(0, 0, z0 + 0.5, RH, hh, da, seed=71, windows=4, stave_n=36, roof_rise=15.0)
    for sd in (-1, 1):
        tx = sd * 22.0
        cyl(nm('tfn'), 6.3, 0.9, loc=(tx, -1.0, z0 - 0.35), key='ev_stone_dark', verts=24)
        cabin(tx, -1.0, z0 + 0.5, 5.5, 17.0, da + sd * 0.15, seed=72 + sd, windows=3, stave_n=22, roof_rise=9.5)
        # covered gallery between hall and tower
        gx0, gx1 = sd * 11.2, sd * 16.8
        xm = (gx0 + gx1) / 2
        L = abs(gx1 - gx0)
        box(nm('gfl'), (L, 3.2, 0.3), loc=(xm, -0.5, z0 + 0.65), key='ev_wood', bev=0.03)
        for yy in (-1.9, 0.9):
            for xx in (gx0 + sd * 0.4, gx1 - sd * 0.4):
                cyl(nm('gpo'), 0.2, 3.4, loc=(xx, yy, z0 + 0.8), key='ev_wood_dark', verts=6)
        for sg in (-1, 1):
            box(nm('grf'), (L + 0.8, 2.4, 0.2), loc=(xm, -0.5 + sg * 1.05, z0 + 4.6 + 0.35), key='ev_shingle_a', rot=(-sg * 28, 0, 0), bev=0.02)
        # tower banners
        box(nm('tbn'), (2.0, 0.12, 7.0), loc=(tx, -6.8, z0 + 12.0), key='ev_banner_green', rot=(0, 0, 0))
    # grand porch
    for sd in (-1, 1):
        cyl(nm('pco'), 0.7, 9.4, loc=(sd * 4.2, -15.2, z0 + 0.5), key='ev_wood_dark', verts=10)
        torus(nm('pcb'), 0.82, 0.14, loc=(sd * 4.2, -15.2, z0 + 1.2), key='bronze', segs=12, rsegs=3)
        torus(nm('pcb'), 0.82, 0.14, loc=(sd * 4.2, -15.2, z0 + 8.4), key='bronze', segs=12, rsegs=3)
        box(nm('pcf'), (1.8, 1.8, 0.7), loc=(sd * 4.2, -15.2, z0 + 0.85), key='ev_stone_dark', bev=0.05)
    box(nm('pbm'), (10.6, 1.1, 0.9), loc=(0, -15.2, z0 + 10.3), key='ev_wood_dark', bev=0.05)
    box(nm('pfl'), (10.6, 5.4, 0.3), loc=(0, -13.5, z0 + 0.7), key='ev_stone_warm', bev=0.04)
    prism_xz([(-5.6, z0 + 10.7), (5.6, z0 + 10.7), (0.0, z0 + 15.3)], -15.6, -15.2, 'ev_wood')
    for sg in (-1, 1):
        box(nm('prf'), (7.7, 5.6, 0.3), loc=(-sg * 2.9, -13.0, z0 + 13.0), key='ev_shingle_a', rot=(0, -sg * 38.5, 0), bev=0.02)
    ball(nm('pem'), 0.9, loc=(0, -15.65, z0 + 12.6), key='bronze', segs=10, rings=6)
    steps(da, 15.7, z0 + 0.7, 5, 16.0, depth=1.3)
    # path and banners and lamps
    for i in range(7):
        cyl(nm('pth'), 2.0, 0.14, loc=(rnd.uniform(-0.6, 0.6), -26.0 - i * 2.8, 0.0), key='ev_stone', verts=7, rot=(0, 0, rnd.uniform(0, 60)))
    for sd in (-1, 1):
        for yy in (-24.0, -31.0):
            x = sd * 6.0
            cyl(nm('bpo'), 0.2, 12.0, loc=(x, yy, 0.0), key='ev_wood_dark', verts=6)
            box(nm('bnr'), (2.2, 0.1, 6.2), loc=(x + 0.0, yy, 8.0), key='ev_banner_green')
            box(nm('bng'), (2.2, 0.12, 0.55), loc=(x, yy, 11.2), key='ev_banner_gold')
            ball(nm('bpt'), 0.3, loc=(x, yy, 12.1), key='bronze', segs=6, rings=4)
    for x in (-30.0, -20.0, 20.0, 30.0):
        lamp(x, -20.4, z0, 3.8, 0.9)
    for sd in (-1, 1):
        lamp(sd * 8.2, -19.0, z0, 3.8, 0.9)
    for i in range(10):
        x = rnd.choice((-1, 1)) * rnd.uniform(18, 32)
        blob(nm('hdg'), rnd.uniform(1.6, 2.4), (x, rnd.uniform(-19, -17), z0 + 1.2), LEAFS[i % 4], subdiv=1, amp=0.25, scale=(1.6, 1, 0.8), seed=i)
    for i in range(7):
        a = rnd.uniform(0, 2 * PI)
        fern(math.cos(a) * 36, math.sin(a) * 25, 0.0, n=6, L=1.5, seed=i)
    wall_ivy(0, 0, RH, 1.2, z0 + 1.0, hh - 1.0, 20, rnd, 0.9)
    U.marker('mk_door', (0, -RH - 0.6, z0 + 3.0))
    U.marker('mk_deck', (0, -22.0, z0 + 0.4))
    return finalize('ev_palace', smooth_angle=38)
