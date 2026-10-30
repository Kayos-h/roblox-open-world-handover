"""D06 - understory plants (19 models): ferns, bushes, flowers, mossy rocks, ivy, hanging moss, mushrooms.
All natural elven colours (ev_* keys). No glow. 1 unit = 1 stud, origin bottom-centre, front = -Y.
"""
import math, random, bmesh
from mathutils import Vector
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, _obj_from_bm, top_paint
from v4_elf import nm, mushrooms, ivy_strand
from nature import blob, rock

PI = math.pi
FERN_KEYS = ('ev_fern', 'ev_leaf_a', 'ev_fern', 'ev_leaf_b', 'ev_leaf_d')
LEAFK = ('ev_leaf_a', 'ev_leaf_b', 'ev_leaf_c', 'ev_leaf_d')
GRASSK = ('ev_leaf_a', 'ev_leaf_c', 'ev_leaf_d', 'ev_fern')


# ------------------------------------------------------------------ shared helpers
def ribbon(name, centre, halfw, side, key, serr=1.0, thick=0.05):
    """Flat two-sided leaf strip along a centreline. serr<1 gives a zig-zag (serrated) edge."""
    bm = bmesh.new()
    L, M, R = [], [], []
    for k, (c, w, s) in enumerate(zip(centre, halfw, side)):
        f = 1.0 if (k % 2 == 0 or serr >= 1.0) else serr
        w = max(w, 0.012)
        M.append(bm.verts.new(c))
        drop = Vector((0, 0, -0.12 * w * f))
        L.append(bm.verts.new(c + s * w * f + drop))
        R.append(bm.verts.new(c - s * w * f + drop))
    for k in range(len(centre) - 1):
        bm.faces.new((L[k], L[k + 1], M[k + 1], M[k]))
        bm.faces.new((M[k], M[k + 1], R[k + 1], R[k]))
    o = _obj_from_bm(name, bm, key)
    sol = o.modifiers.new('sol', 'SOLIDIFY')
    sol.thickness = thick
    return o


def frond(cx, cy, z, ang, Lf, lift, wmax, key, n=18, droop=0.75, serr=0.5, spread=1.0, stem='ev_leaf_d'):
    d = Vector((math.cos(ang), math.sin(ang), 0))
    side = Vector((-d.y, d.x, 0))
    pts, ws = [], []
    for k in range(n + 1):
        t = k / n
        zz = Lf * lift * (0.9 * t - droop * t * t)
        pts.append(Vector((cx, cy, z)) + d * Lf * spread * t * (1 - 0.15 * t) + Vector((0, 0, zz + 0.1)))
        stalk = max(0.0, min(1.0, (t - 0.04) / 0.22))
        stalk = stalk * stalk * (3 - 2 * stalk)
        ws.append(wmax * stalk * math.sin(PI * t ** 0.8) ** 0.6 * (1 - 0.15 * t) + 0.03)
    ribbon(nm('fr'), pts, ws, [side] * (n + 1), key, serr)
    idx = list(range(0, n + 1, 3))
    if idx[-1] != n:
        idx.append(n)
    tube(nm('rc'), [tuple(pts[i]) for i in idx], 0.07, stem, res=4, ures=2)


def fiddlehead(x, y, z, h, ang, key='ev_fern'):
    d = Vector((math.cos(ang), math.sin(ang), 0))
    rr = h * 0.17
    pts = [(x, y, z), (x, y, z + h * 0.35), (x, y, z + h * 0.7)]
    cz = z + h * 0.7
    for i in range(1, 9):
        phi = i * (2.3 * PI / 8)
        r = rr * (1 - phi / (2.9 * PI))
        pos = Vector((x, y, cz)) + d * rr + (-d * math.cos(phi) + Vector((0, 0, 1)) * math.sin(phi)) * r
        pts.append(tuple(pos))
    tube(nm('fh'), pts, 0.085, key, res=4, ures=2)


def blade(x, y, z, h, ang, bend, w, key):
    d = Vector((math.cos(ang), math.sin(ang), 0))
    side = Vector((-d.y, d.x, 0))
    pts = [Vector((x, y, z)) + d * bend * t * t * h + Vector((0, 0, h * t * (1 - 0.1 * t))) for t in (0, 0.33, 0.66, 1.0)]
    ribbon(nm('bl'), pts, [w, w * 0.92, w * 0.6, 0.02], [side] * 4, key, 1.0, 0.03)


def tuft(x, y, z, rnd, n=7, h=(1.4, 2.7), keys=GRASSK, w=0.13):
    for i in range(n):
        blade(x + rnd.uniform(-0.3, 0.3), y + rnd.uniform(-0.3, 0.3), z, rnd.uniform(*h), rnd.uniform(0, 2 * PI), rnd.uniform(0.25, 0.6), w,
              rnd.choice(keys))


def mini_fern(x, y, z, n, L, seed, wmax=0.5):
    rnd = random.Random(seed)
    for i in range(n):
        a = 2 * PI * i / n + rnd.uniform(-0.25, 0.25)
        frond(x, y, z, a, L * rnd.uniform(0.85, 1.15), rnd.uniform(1.1, 1.6), wmax, rnd.choice(FERN_KEYS), n=12, spread=0.9)
    blob(nm('fc'), L * 0.14, (x, y, z + 0.05), 'ev_moss', subdiv=1, amp=0.2, scale=(1, 1, 0.55), seed=seed)


def moss_skirt(r, seed, sx=1.0, sy=0.85, key='ev_moss', loc=(0, 0, 0), h=0.16):
    blob(nm('sk'), r, loc, key, subdiv=2, amp=0.28, scale=(sx, sy, h), seed=seed)


# ------------------------------------------------------------------ D06_01..03 ferns
def fern_a():
    """Lady fern: low arching fronds in three rings with fiddleheads in the middle."""
    reset()
    rnd = random.Random(101)
    for i in range(11):
        a = 2 * PI * i / 11 + rnd.uniform(-0.15, 0.15)
        frond(0, 0, 0.2, a, rnd.uniform(5.4, 6.6), rnd.uniform(1.6, 2.0), 1.15, rnd.choice(FERN_KEYS), n=24, serr=0.74)
    for i in range(6):
        a = 2 * PI * i / 6 + 0.4 + rnd.uniform(-0.2, 0.2)
        frond(0, 0, 0.3, a, rnd.uniform(4.2, 5.0), rnd.uniform(2.2, 2.6), 1.0, rnd.choice(FERN_KEYS), n=22, serr=0.74, spread=0.7)
    for i in range(4):
        a = 2 * PI * i / 4 + 0.9
        frond(0, 0, 0.4, a, rnd.uniform(3.2, 3.8), rnd.uniform(2.9, 3.3), 0.8, rnd.choice(('ev_leaf_c', 'ev_leaf_a')), n=18, serr=0.74, spread=0.45)
    for i in range(3):
        fiddlehead(math.cos(i * 2.1) * 0.5, math.sin(i * 2.1) * 0.5, 0.2, 2.2 + 0.4 * i, i * 2.1)
    blob(nm('crown'), 1.0, (0, 0, 0.25), 'ev_moss', subdiv=2, amp=0.2, scale=(1.2, 1.2, 0.6), seed=3)
    moss_skirt(2.6, 5)
    return finalize('fern_a', smooth_angle=42)


def fern_b():
    """Shield fern: tall upright vase of narrow fronds, with two young ferns beside it."""
    reset()
    rnd = random.Random(102)
    for i in range(12):
        a = 2 * PI * i / 12 + rnd.uniform(-0.12, 0.12)
        frond(0, 0, 0.2, a, rnd.uniform(8.6, 10.0), rnd.uniform(2.1, 2.5), 0.85, rnd.choice(FERN_KEYS), n=22, droop=0.8, spread=0.55)
    for i in range(5):
        a = 2 * PI * i / 5 + 0.3
        frond(0, 0, 0.3, a, rnd.uniform(6.0, 7.0), rnd.uniform(2.6, 3.0), 0.7, rnd.choice(('ev_leaf_a', 'ev_leaf_c')), n=18, droop=0.8, spread=0.35)
    for i in range(3):
        fiddlehead(math.cos(i * 2.1 + 0.5) * 0.6, math.sin(i * 2.1 + 0.5) * 0.6, 0.2, 3.0 + 0.5 * i, i * 2.1 + 0.5)
    blob(nm('crown'), 1.3, (0, 0, 0.3), 'ev_bark', subdiv=2, amp=0.25, scale=(1.1, 1.1, 0.7), seed=7)
    mini_fern(5.2, -2.6, 0.0, 6, 2.4, 11)
    mini_fern(-4.6, 3.6, 0.0, 5, 2.0, 12)
    moss_skirt(4.2, 9, sx=1.4, sy=1.1)
    rock(nm('rk'), 1.2, (3.2, 3.0, 0.0), 'ev_stone_dark', seed=4)
    return finalize('fern_b', smooth_angle=42)


def fern_c():
    """Bracken patch: three low clumps of small fronds on a moss mound, with a stone and a twig."""
    reset()
    rnd = random.Random(103)
    for (cx, cy, nn, L, sd) in ((0.0, 0.0, 9, 5.6, 1), (7.4, 2.8, 8, 4.8, 2), (-4.6, -5.0, 8, 5.0, 3)):
        for i in range(nn):
            a = 2 * PI * i / nn + rnd.uniform(-0.2, 0.2)
            frond(cx, cy, 0.25, a, L * rnd.uniform(0.85, 1.15), rnd.uniform(1.5, 1.9), 1.0, rnd.choice(FERN_KEYS), n=22, serr=0.74, spread=0.9)
        blob(nm('cr'), 0.8, (cx, cy, 0.2), 'ev_moss', subdiv=1, amp=0.2, scale=(1, 1, 0.5), seed=sd)
    moss_skirt(7.2, 21, sx=1.35, sy=1.0, loc=(1.2, -1.0, 0.0))
    rk = rock(nm('rk'), 1.6, (-5.8, 3.4, 0.0), 'ev_stone_dark', seed=8)
    top_paint(rk, 'ev_moss', 0.55, 8)
    tube(nm('tw'), [(4.6, 5.4, 0.3), (6.8, 6.0, 0.55), (9.2, 5.6, 0.35)], 0.17, 'ev_bark', res=5, ures=3)
    tuft(-1.4, 4.6, 0.0, rnd, n=6)
    tuft(8.6, -1.6, 0.0, rnd, n=6)
    return finalize('fern_c', smooth_angle=42)


# ------------------------------------------------------------------ bushes
def blossom(p, nrm, r, pk, ck, n=5):
    nrm = Vector(nrm).normalized()
    u = nrm.cross(Vector((0, 0, 1)))
    if u.length < 0.1:
        u = Vector((1, 0, 0))
    u.normalize()
    v = nrm.cross(u)
    for i in range(n):
        a = 2 * PI * i / n
        q = Vector(p) + (u * math.cos(a) + v * math.sin(a)) * r
        ball(nm('bp'), r * 0.72, loc=tuple(q), key=pk, segs=5, rings=3)
    ball(nm('bc'), r * 0.45, loc=tuple(Vector(p) + nrm * r * 0.25), key=ck, segs=5, rings=3)


def leafy_bush(seed, size, n=90, wide=1.2, tall=0.9):
    rnd = random.Random(seed)
    blob(nm('core'), size * 0.5, (0, 0, size * 0.42), 'ev_leaf_b', subdiv=2, amp=0.2, scale=(wide, wide, tall), seed=seed, flat_bottom=-size * 0.3)
    blob(nm('base'), size * 0.5, (0, 0, size * 0.1), 'ev_leaf_b', subdiv=2, amp=0.25, scale=(wide * 1.05, wide * 1.05, 0.4), seed=seed + 1)
    for i in range(n):
        t = (i + 0.5) / n
        el = math.asin(t * 0.97)
        az = i * 2.39996
        R = size * 0.5 * (1.0 if i % 3 else 0.78)
        p = (math.cos(az) * math.cos(el) * R * wide, math.sin(az) * math.cos(el) * R * wide, size * 0.30 + math.sin(el) * R * tall * 1.15)
        r = size * rnd.uniform(0.10, 0.165)
        k = rnd.choice(('ev_leaf_c', 'ev_leaf_a', 'ev_leaf_c')) if el > 0.8 else rnd.choice(('ev_leaf_b', 'ev_leaf_d', 'ev_leaf_a')) if el < 0.35 else rnd.choice(LEAFK)
        blob(nm('c'), r, p, k, subdiv=2, amp=0.3, scale=(1, 1, 0.72), seed=rnd.randint(0, 999))
    return rnd


def bush_a():
    """Round leafy bush with a few stones and grass at its foot."""
    reset()
    rnd = leafy_bush(201, 8.0, n=90)
    tuft(5.4, -1.2, 0.0, rnd, n=7)
    tuft(-4.9, 2.6, 0.0, rnd, n=7)
    rock(nm('rk'), 1.1, (4.6, 3.4, 0.0), 'ev_stone_dark', seed=2)
    return finalize('bush_a', smooth_angle=55)


def bush_b():
    """Flowering shrub: dense leaves covered in small cream blossoms (hawthorn-like)."""
    reset()
    rnd = leafy_bush(202, 9.0, n=96, wide=1.15, tall=0.95)
    size, wide, tall = 9.0, 1.15, 0.95
    for i in range(90):
        az = rnd.uniform(0, 2 * PI)
        el = math.asin(rnd.uniform(0.05, 0.95))
        R = size * 0.5
        nrm = (math.cos(az) * math.cos(el), math.sin(az) * math.cos(el), math.sin(el))
        p = (nrm[0] * (R * wide + size * 0.085), nrm[1] * (R * wide + size * 0.085), size * 0.30 + nrm[2] * (R * tall * 1.15 + size * 0.07))
        blossom(p, nrm, size * 0.036, rnd.choice(('ev_petal_cream', 'ev_petal_cream', 'ev_petal_pink')), 'ev_petal_gold')
    tuft(5.6, 0.4, 0.0, rnd, n=6)
    return finalize('bush_b', smooth_angle=55)


def bush_c():
    """Berry bush: arching woody canes with small leaf pads and dark berries hanging underneath."""
    reset()
    rnd = random.Random(203)
    moss_skirt(5.0, 3, sx=1.0, sy=1.0, key='ev_leaf_b', h=0.14)
    for i in range(11):
        a = 2 * PI * i / 11 + rnd.uniform(-0.2, 0.2)
        d = Vector((math.cos(a), math.sin(a), 0))
        reach = rnd.uniform(3.6, 5.2)
        top = rnd.uniform(5.2, 7.4)
        pts = [(d.x * 0.3, d.y * 0.3, 0.0), (d.x * reach * 0.35, d.y * reach * 0.35, top * 0.6), (d.x * reach * 0.72, d.y * reach * 0.72, top * 0.95),
               (d.x * reach, d.y * reach, top * 0.82)]
        tube(nm('cane'), pts, 0.22, 'ev_bark', res=5, ures=3)
        for k in (1, 2, 3):
            px, py, pz = pts[k]
            for m in range(2):
                ox, oy = rnd.uniform(-0.8, 0.8), rnd.uniform(-0.8, 0.8)
                blob(nm('lp'), rnd.uniform(0.7, 1.05), (px + ox, py + oy, pz + rnd.uniform(-0.1, 0.5)), rnd.choice(LEAFK), subdiv=2, amp=0.28,
                     scale=(1, 1, 0.55), seed=rnd.randint(0, 999))
            for b in range(rnd.randint(4, 6)):
                ball(nm('be'), 0.3, loc=(px + rnd.uniform(-1.0, 1.0), py + rnd.uniform(-1.0, 1.0), pz - rnd.uniform(0.35, 1.2)),
                     key=rnd.choice(('ev_berry', 'ev_berry', 'ev_berry_red')), segs=6, rings=4)
    tuft(5.8, 1.0, 0.0, rnd, n=6)
    tuft(-5.2, -2.4, 0.0, rnd, n=6)
    return finalize('bush_c', smooth_angle=55)


# ------------------------------------------------------------------ flowers
def daisy(x, y, z, h, rnd, pk='ev_petal_cream', ck='ev_petal_gold', npet=9, pr=0.62, pw=0.32):
    lean = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), 0)) * h * 0.09
    tube(nm('st'), [(x, y, z), (x + lean.x * 0.4, y + lean.y * 0.4, z + h * 0.55), (x + lean.x, y + lean.y, z + h)], 0.05, 'ev_leaf_b', res=4, ures=2)
    tx, ty, tz = x + lean.x, y + lean.y, z + h
    a0 = rnd.uniform(0, 2 * PI)
    for p in range(npet):
        a = a0 + 2 * PI * p / npet
        o = ball(nm('pt'), pr * 0.56, loc=(tx + math.cos(a) * pr * 0.58, ty + math.sin(a) * pr * 0.58, tz + 0.04), key=pk, segs=5, rings=3,
                 scale=(1.0, pw, 0.16))
        o.rotation_euler = (0, math.radians(-14), a)
    ball(nm('cn'), pr * 0.3, loc=(tx, ty, tz + 0.06), key=ck, segs=6, rings=4, scale=(1, 1, 0.7))
    if rnd.random() < 0.8:
        a = rnd.uniform(0, 2 * PI)
        o = ball(nm('lf'), 0.4, loc=(x + math.cos(a) * 0.35, y + math.sin(a) * 0.35, z + 0.3), key='ev_leaf_a', segs=5, rings=3, scale=(1.8, 0.5, 0.16))
        o.rotation_euler = (0, math.radians(-25), a)


def polar_pts(rnd, n, rad, min_d=1.3):
    pts = []
    tries = 0
    while len(pts) < n and tries < 600:
        tries += 1
        a = rnd.uniform(0, 2 * PI)
        d = math.sqrt(rnd.random()) * rad
        p = (math.cos(a) * d, math.sin(a) * d)
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > min_d ** 2 for q in pts):
            pts.append(p)
    return pts


def flower_a():
    """Meadow patch: white daisies and a few gold buttercups in grass."""
    reset()
    rnd = random.Random(301)
    blob(nm('mound'), 5.4, (0, 0, 0.0), 'ev_leaf_b', subdiv=2, amp=0.2, scale=(1.0, 0.9, 0.12), seed=71)
    for (x, y) in polar_pts(rnd, 8, 4.4, 1.7):
        tuft(x, y, 0.0, rnd, n=7)
    for i, (x, y) in enumerate(polar_pts(rnd, 15, 4.2, 1.35)):
        daisy(x, y, 0.0, rnd.uniform(2.0, 3.4), rnd)
    for (x, y) in polar_pts(rnd, 5, 4.4, 1.5):
        daisy(x, y, 0.0, rnd.uniform(1.6, 2.4), rnd, pk='ev_petal_gold', ck='ev_petal_cream', npet=5, pr=0.46, pw=0.85)
    return finalize('flower_a', smooth_angle=45)


def bell(p, a, s, pk):
    ax = Vector((math.sin(-0.9) * math.cos(a), math.sin(-0.9) * math.sin(a), math.cos(-0.9)))
    top = Vector(p)
    loc = top - ax * 0.55 * s
    prof = [(0, 0.55 * s), (0.15 * s, 0.52 * s), (0.28 * s, 0.3 * s), (0.34 * s, 0.0), (0.29 * s, -0.02 * s), (0.2 * s, 0.28 * s), (0.1 * s, 0.45 * s), (0, 0.46 * s)]
    lathe(nm('bl'), prof, loc=tuple(loc), key=pk, segs=6, rot=(0, math.degrees(-0.9), math.degrees(a)))


def foxglove(x, y, z, H, rnd, pk):
    lean = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), 0)) * H * 0.04
    tube(nm('fx'), [(x, y, z), (x + lean.x * 0.5, y + lean.y * 0.5, z + H * 0.5), (x + lean.x, y + lean.y, z + H)], 0.1, 'ev_leaf_b', res=5, ures=3)
    for i in range(5):
        a = 2 * PI * i / 5 + rnd.uniform(-0.3, 0.3)
        o = ball(nm('bl'), 0.9, loc=(x + math.cos(a) * 0.9, y + math.sin(a) * 0.9, z + 0.4), key=rnd.choice(('ev_leaf_a', 'ev_leaf_b')), segs=6, rings=4,
                 scale=(1.9, 0.5, 0.16))
        o.rotation_euler = (0, math.radians(-22), a)
    nb = int(H * 1.9)
    for k in range(nb):
        t = 0.36 + 0.62 * k / nb
        a = k * 2.4 + rnd.uniform(-0.3, 0.3)
        s = 0.8 * (1 - 0.5 * (t - 0.36) / 0.64)
        px = x + lean.x * t + math.cos(a) * 0.12
        py = y + lean.y * t + math.sin(a) * 0.12
        bell((px, py, z + H * t), a, s, pk)
    ball(nm('tip'), 0.14, loc=(x + lean.x, y + lean.y, z + H + 0.1), key=pk, segs=5, rings=3)


def flower_b():
    """Foxglove spikes: tall stems with hanging violet and rose bells, leaf rosettes at the base."""
    reset()
    rnd = random.Random(302)
    blob(nm('mound'), 4.6, (0, 0, 0.0), 'ev_leaf_b', subdiv=2, amp=0.2, scale=(1.0, 0.9, 0.12), seed=72)
    pts = polar_pts(rnd, 6, 3.2, 2.0)
    for i, (x, y) in enumerate(pts):
        foxglove(x, y, 0.0, rnd.uniform(5.0, 7.0), rnd, ('ev_petal_violet', 'ev_petal_rose', 'ev_petal_violet', 'ev_petal_pink')[i % 4])
    for (x, y) in polar_pts(rnd, 5, 4.6, 1.8):
        tuft(x, y, 0.0, rnd, n=6)
    return finalize('flower_b', smooth_angle=45)


def tulip(x, y, z, h, rnd, pk, open_=True):
    lean = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), 0)) * h * 0.05
    tube(nm('tl'), [(x, y, z), (x + lean.x * 0.5, y + lean.y * 0.5, z + h * 0.5), (x + lean.x, y + lean.y, z + h)], 0.07, 'ev_leaf_b', res=5, ures=3)
    for i in range(2):
        blade(x, y, z, h * rnd.uniform(0.55, 0.75), rnd.uniform(0, 2 * PI), 0.55, 0.3, rnd.choice(('ev_leaf_a', 'ev_leaf_d')))
    cx, cy, cz = x + lean.x, y + lean.y, z + h
    if open_:
        prof = [(0, 0), (0.2, 0.03), (0.46, 0.5), (0.52, 0.95), (0.42, 1.0), (0.37, 0.6), (0.14, 0.25), (0, 0.22)]
        lathe(nm('cup'), prof, loc=(cx, cy, cz), key=pk, segs=6, rot=(math.degrees(rnd.uniform(-0.15, 0.15)), math.degrees(rnd.uniform(-0.15, 0.15)), 0))
        ball(nm('ct'), 0.12, loc=(cx, cy, cz + 0.45), key='ev_petal_gold', segs=5, rings=3)
    else:
        ball(nm('bud'), 0.36, loc=(cx, cy, cz + 0.4), key=pk, segs=6, rings=4, scale=(1, 1, 1.6))


def flower_c():
    """Wild tulips and lilies: soft pink, cream and rose cups on slim stems, some still in bud."""
    reset()
    rnd = random.Random(303)
    blob(nm('mound'), 5.0, (0, 0, 0.0), 'ev_leaf_b', subdiv=2, amp=0.2, scale=(1.0, 0.95, 0.12), seed=73)
    keys = ('ev_petal_pink', 'ev_petal_cream', 'ev_petal_rose', 'ev_petal_pink', 'ev_petal_cream')
    for i, (x, y) in enumerate(polar_pts(rnd, 12, 4.0, 1.5)):
        tulip(x, y, 0.0, rnd.uniform(2.6, 4.2), rnd, keys[i % 5], open_=(i % 4 != 3))
    for (x, y) in polar_pts(rnd, 6, 4.6, 1.8):
        tuft(x, y, 0.0, rnd, n=6)
    return finalize('flower_c', smooth_angle=45)


# ------------------------------------------------------------------ mossy rocks
def _mossy(o, thr, seed):
    top_paint(o, 'ev_moss', thr, seed, noise_amt=0.3)
    return o


def moss_rock_a():
    """Large mossy boulder with a smaller companion, a fern and toadstools at its foot."""
    reset()
    rnd = random.Random(401)
    a = rock(nm('rk'), 5.4, (0, 0, 2.7), 'ev_stone_dark', seed=11, scale=(1.25, 1.0, 0.82), subdiv=4, amp=0.34)
    _mossy(a, 0.52, 11)
    b = rock(nm('rk'), 2.6, (6.0, -2.2, 1.0), 'ev_stone_dark', seed=12, scale=(1.2, 1.0, 0.72), subdiv=3, amp=0.32)
    _mossy(b, 0.5, 12)
    c = rock(nm('rk'), 1.5, (-5.4, -3.4, 0.5), 'ev_stone_dark', seed=13, scale=(1.2, 1.0, 0.7), subdiv=3, amp=0.3)
    _mossy(c, 0.55, 13)
    moss_skirt(9.5, 14, sx=1.1, sy=0.95)
    mini_fern(-3.4, -7.0, 0.0, 7, 3.0, 15)
    mini_fern(7.2, 3.2, 0.0, 6, 2.4, 16)
    mushrooms(-6.6, -5.0, 0.0, 6, seed=3, scale=1.6)
    tuft(2.0, -7.2, 0.0, rnd, n=7)
    tuft(-8.0, 1.6, 0.0, rnd, n=7)
    for k in range(3):
        ivy_strand((-3.6 + k * 1.2, -4.4 - k * 0.2, 4.2 - k * 0.6), rnd.uniform(2.5, 4.5), seed=k)
    return finalize('moss_rock_a', smooth_angle=22)


def moss_rock_b():
    """Cairn-like cluster of four leaning rocks, heavily mossed, ivy running down the tallest."""
    reset()
    rnd = random.Random(402)
    spec = [(0, 0, 3.1, 3.4, (0.95, 0.9, 1.35), 21), (4.4, -1.8, 1.7, 2.4, (1.2, 1.0, 0.85), 22), (-3.9, -2.6, 1.4, 2.0, (1.1, 1.0, 0.8), 23),
            (1.2, 3.6, 1.3, 1.8, (1.2, 1.0, 0.75), 24)]
    for (x, y, z, r, sc, sd) in spec:
        o = rock(nm('rk'), r, (x, y, z), 'ev_stone_dark', seed=sd, scale=sc, subdiv=3, amp=0.34, rot_z=sd)
        _mossy(o, 0.38, sd)
    moss_skirt(8.2, 25, sx=1.15)
    for k in range(5):
        ivy_strand((-1.2 + k * 0.6, -2.3 + math.sin(k) * 0.2, 6.2 - (k % 2) * 0.8), rnd.uniform(4.0, 6.5), seed=10 + k)
    mini_fern(5.0, 4.4, 0.0, 6, 2.6, 26)
    mushrooms(-5.8, 2.0, 0.0, 5, seed=5, scale=1.5)
    tuft(-1.0, -6.0, 0.0, rnd, n=7)
    tuft(6.8, -4.2, 0.0, rnd, n=6)
    return finalize('moss_rock_b', smooth_angle=22)


def moss_rock_c():
    """Standing stone: a tall narrow slab with moss on its top and ferns round the base."""
    reset()
    rnd = random.Random(403)
    s = rock(nm('rk'), 3.2, (0, 0, 4.6), 'ev_stone_dark', seed=31, scale=(0.62, 0.92, 2.0), subdiv=4, amp=0.28)
    s.rotation_euler = (0.05, 0.06, 0.4)
    _mossy(s, 0.6, 31)
    for (x, y, r, sd) in ((3.0, -2.0, 1.5, 32), (-2.8, 1.8, 1.2, 33), (1.0, 3.2, 1.0, 34)):
        o = rock(nm('rk'), r, (x, y, r * 0.3), 'ev_stone_dark', seed=sd, scale=(1.3, 1.0, 0.6), subdiv=3, amp=0.3)
        _mossy(o, 0.5, sd)
    moss_skirt(6.2, 35)
    mini_fern(-4.2, -2.4, 0.0, 7, 2.8, 36)
    mini_fern(4.6, 2.2, 0.0, 6, 2.4, 37)
    for k in range(4):
        ivy_strand((-1.4 + k * 0.9, -2.0 + math.sin(k * 2) * 0.3, 7.0 - (k % 2) * 1.2), rnd.uniform(3.5, 6.0), seed=40 + k)
    tuft(0.5, -5.4, 0.0, rnd, n=7)
    return finalize('moss_rock_c', smooth_angle=22)


# ------------------------------------------------------------------ ivy
def ivy_leaf(p, r, rnd, plane='y', key=None):
    k = key or rnd.choice(('ev_leaf_a', 'ev_leaf_b', 'ev_leaf_c', 'ev_leaf_b', 'ev_leaf_d'))
    if plane == 'y':
        o = ball(nm('il'), r, loc=p, key=k, segs=5, rings=3, scale=(1.0, 0.16, 0.9))
        o.rotation_euler = (rnd.uniform(-0.35, 0.35), rnd.uniform(0, 2 * PI), rnd.uniform(-0.2, 0.2))
    else:
        o = ball(nm('il'), r, loc=p, key=k, segs=5, rings=3, scale=(1.0, 0.9, 0.16))
        o.rotation_euler = (rnd.uniform(-0.25, 0.25), rnd.uniform(-0.25, 0.25), rnd.uniform(0, 2 * PI))


def leaves_along(pts, rnd, step, rmin, rmax, plane='y', spread=0.5, ydepth=0.0):
    for a, b in zip(pts, pts[1:]):
        a, b = Vector(a), Vector(b)
        ln = (b - a).length
        m = max(1, int(ln / step))
        for i in range(m):
            p = a.lerp(b, (i + rnd.random()) / m)
            for s in (-1, 1):
                if rnd.random() < 0.85:
                    off = Vector((rnd.uniform(0.1, spread) * s, rnd.uniform(-ydepth, ydepth), rnd.uniform(-0.2, 0.2))) if plane == 'y' else \
                        Vector((rnd.uniform(0.1, spread) * s, rnd.uniform(-spread, spread), 0.0))
                    ivy_leaf(tuple(p + off), rnd.uniform(rmin, rmax), rnd, plane)


def ivy_a():
    """Climbing ivy mat for walls and trunks (faces -Y): vines climb unevenly with overlapping leaves."""
    reset()
    rnd = random.Random(501)
    blob(nm('soil'), 4.6, (0, 0.2, 0.0), 'ev_bark', subdiv=2, amp=0.25, scale=(1.0, 0.35, 0.18), seed=5)
    heights = [12.0, 9.5, 11.0, 7.5, 10.0, 6.5]
    xs = [-3.4, -1.9, -0.3, 1.2, 2.6, 3.8]
    for i, (x0, hmax) in enumerate(zip(xs, heights)):
        pts = []
        x = x0
        for j in range(10):
            t = j / 9
            x += rnd.uniform(-0.5, 0.5)
            pts.append((x, 0.2 + rnd.uniform(0.0, 0.15), 0.3 + (hmax - 0.3) * t))
        tube(nm('vn'), pts, 0.1, 'ev_bark', res=4, ures=2)
        leaves_along(pts, rnd, 0.42, 0.42, 0.62, 'y', spread=0.75, ydepth=0.25)
        for j in (3, 5, 7):
            if j >= len(pts):
                continue
            bx, by, bz = pts[j]
            sgn = rnd.choice((-1, 1))
            sub = [(bx, by, bz)]
            for q in range(1, 5):
                sub.append((bx + sgn * q * rnd.uniform(0.5, 0.9), 0.2 + rnd.uniform(0, 0.15), bz + q * rnd.uniform(0.5, 1.0)))
            tube(nm('vs'), sub, 0.06, 'ev_bark', res=4, ures=2)
            leaves_along(sub, rnd, 0.45, 0.4, 0.58, 'y', spread=0.6, ydepth=0.2)
    return finalize('ivy_a', smooth_angle=60)


def ivy_b():
    """Broken stone column wrapped in a spiral of ivy, with a fallen drum at its foot."""
    reset()
    rnd = random.Random(502)
    box(nm('plinth'), (5.4, 5.4, 0.9), loc=(0, 0, 0.45), key='ev_stone_warm', bev=0.1)
    cyl(nm('col'), 1.8, 8.4, loc=(0, 0, 0.9), key='ev_stone', verts=14, bev=0.08)
    for k in range(3):
        cyl(nm('ring'), 1.95, 0.25, loc=(0, 0, 0.9 + k * 2.8), key='ev_stone_warm', verts=14)
    top = rock(nm('brk'), 2.1, (0.2, 0.1, 9.3), 'ev_stone', seed=51, scale=(0.95, 0.9, 0.5), subdiv=3, amp=0.4)
    cyl(nm('drum'), 1.7, 2.4, loc=(4.4, -2.6, 1.7), key='ev_stone', verts=14, rot=(0, 90, 20))
    moss_skirt(3.2, 52, loc=(5.4, -2.4, 0.0))
    spiral = []
    for i in range(48):
        t = i / 47
        a = t * 2 * PI * 2.4 + 0.5
        z = 0.7 + t * 8.3
        spiral.append((math.cos(a) * 1.92, math.sin(a) * 1.92, z))
    tube(nm('sp'), spiral, 0.1, 'ev_bark', res=4, ures=2)
    for i, p in enumerate(spiral):
        if i % 1 == 0:
            n = Vector((p[0], p[1], 0)).normalized()
            for s in (0, 1):
                q = Vector(p) + n * rnd.uniform(0.0, 0.25) + Vector((0, 0, rnd.uniform(-0.3, 0.3)))
                o = ball(nm('il'), rnd.uniform(0.38, 0.55), loc=tuple(q), key=rnd.choice(('ev_leaf_a', 'ev_leaf_b', 'ev_leaf_c', 'ev_leaf_b')), segs=5, rings=3,
                         scale=(1.0, 0.9, 0.16))
                ang = math.atan2(n.y, n.x)
                o.rotation_euler = (rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3) + 0.0, ang + rnd.uniform(-0.8, 0.8))
    for k in range(5):
        a = rnd.uniform(0, 2 * PI)
        ivy_strand((math.cos(a) * 1.95, math.sin(a) * 1.95, 9.0 - rnd.uniform(0, 1.0)), rnd.uniform(3.0, 6.0), seed=60 + k)
    mini_fern(-4.2, 3.6, 0.0, 6, 2.4, 53)
    tuft(3.4, 4.4, 0.0, rnd, n=6)
    return finalize('ivy_b', smooth_angle=50)


def ivy_c():
    """Ground ivy: a creeping carpet radiating from the middle, with two stones and tiny white flowers."""
    reset()
    rnd = random.Random(503)
    blob(nm('soil'), 5.6, (0, 0, 0.0), 'ev_bark', subdiv=2, amp=0.2, scale=(1.0, 0.9, 0.05), seed=54)
    for i in range(15):
        a = 2 * PI * i / 15 + rnd.uniform(-0.2, 0.2)
        L = rnd.uniform(4.6, 7.4)
        d = Vector((math.cos(a), math.sin(a), 0))
        side = Vector((-d.y, d.x, 0))
        pts = []
        for j in range(9):
            t = j / 8
            w = math.sin(t * 3 + i) * 0.9 * t
            pts.append(tuple(d * L * t + side * w + Vector((0, 0, 0.5 + 0.06 * math.sin(j + i)))))
        tube(nm('cr'), pts, 0.08, 'ev_bark', res=4, ures=2)
        leaves_along(pts, rnd, 0.34, 0.55, 0.82, 'z', spread=0.6)
    for (x, y, r, sd) in ((3.4, 2.6, 1.2, 55), (-3.0, -3.2, 0.95, 56)):
        o = rock(nm('rk'), r, (x, y, 0.2), 'ev_stone_dark', seed=sd, scale=(1.2, 1.0, 0.6), subdiv=3, amp=0.3)
        _mossy(o, 0.5, sd)
    for i in range(10):
        a = rnd.uniform(0, 2 * PI)
        d = rnd.uniform(1.0, 5.6)
        blossom((math.cos(a) * d, math.sin(a) * d, 0.8), (0, 0, 1), 0.22, 'ev_petal_cream', 'ev_petal_gold')
    mushrooms(-4.2, 3.4, 0.1, 4, seed=7, scale=1.0)
    return finalize('ivy_c', smooth_angle=60)


# ------------------------------------------------------------------ hanging moss
def moss_strand(x, y, z, L, rnd, w0=0.26, keys=('ev_lichen', 'ev_moss', 'ev_lichen', 'ev_leaf_d'), puffs=True):
    n = 6
    drift = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), 0)) * L * 0.1
    pts, ws = [], []
    for k in range(n + 1):
        t = k / n
        sw = math.sin(t * 3.0 + x) * L * 0.035
        pts.append(Vector((x + drift.x * t + sw, y + drift.y * t + sw * 0.5, z - L * t)))
        ws.append(w0 * (1 - 0.82 * t) + 0.02)
    a = rnd.uniform(0, PI)
    side = Vector((math.cos(a), math.sin(a), 0))
    key = rnd.choice(keys)
    ribbon(nm('ms'), pts, ws, [side] * (n + 1), key, 0.55, 0.05)
    if puffs:
        for k in range(1, n):
            if rnd.random() < 0.8:
                p = pts[k] + Vector((rnd.uniform(-0.25, 0.25), rnd.uniform(-0.25, 0.25), 0))
                ball(nm('mp'), rnd.uniform(0.26, 0.4), loc=tuple(p), key=rnd.choice(keys), segs=5, rings=3, scale=(1, 1, 0.7))


def hanging_moss_a():
    """Branch with long pale-green moss tendrils hanging from it (Spanish-moss style)."""
    reset()
    rnd = random.Random(601)
    top = 14.0
    pts = [(-9.5, 0.0, top + 0.4), (-4.0, 0.2, top + 0.0), (2.0, -0.2, top + 0.15), (9.5, 0.1, top - 0.35)]
    tube(nm('lb'), pts, 0.85, 'ev_bark', res=7, ures=4)
    tube(nm('tw'), [(-1.0, 0.0, top + 0.1), (0.0, 1.8, top + 1.6), (0.8, 3.4, top + 2.0)], 0.35, 'ev_bark', res=5, ures=3)
    for (cx, z) in ((-9.5, top + 0.4), (9.5, top - 0.35)):
        blob(nm('lf'), 1.7, (cx, 0.0, z + 0.2), rnd.choice(LEAFK), subdiv=2, amp=0.3, scale=(1, 1, 0.7), seed=3)
    blob(nm('lf'), 1.5, (0.8, 3.4, top + 2.1), 'ev_leaf_c', subdiv=2, amp=0.3, scale=(1, 1, 0.7), seed=4)
    for i in range(30):
        t = (i + rnd.uniform(0, 0.8)) / 30
        x = -9.0 + 18.0 * t
        zb = top + 0.4 - 0.75 * t - 0.3
        moss_strand(x, rnd.uniform(-0.5, 0.5), zb, rnd.uniform(6.0, 13.0), rnd)
    return finalize('hanging_moss_a', smooth_angle=60)


def hanging_moss_b():
    """Curved limb with three curtains of leafy vines and small white star blossoms."""
    reset()
    rnd = random.Random(602)
    top = 15.0
    pts = [(-8.5, 0.0, top - 1.2), (-4.0, 0.3, top + 0.6), (1.0, 0.0, top + 0.9), (6.0, -0.3, top + 0.2), (9.5, 0.0, top - 0.9)]
    tube(nm('lb'), pts, 0.8, 'ev_bark', res=7, ures=4)
    for (cx, z) in ((-8.5, top - 1.0), (9.5, top - 0.7), (1.0, top + 1.5)):
        blob(nm('lf'), 1.8, (cx, 0.0, z), rnd.choice(LEAFK), subdiv=2, amp=0.3, scale=(1, 1, 0.7), seed=int(cx) + 9)
    for ci, cx in enumerate((-5.6, 0.8, 6.4)):
        for s in range(9):
            x = cx + rnd.uniform(-2.2, 2.2)
            y = rnd.uniform(-0.8, 0.8)
            zb = top + 0.4 - abs(x - 0.5) * 0.12 - 0.4
            L = rnd.uniform(8.0, 15.0)
            nseg = 6
            drift = Vector((rnd.uniform(-0.8, 0.8), rnd.uniform(-0.8, 0.8), 0))
            sp = [(x + drift.x * (k / nseg) ** 2, y + drift.y * (k / nseg) ** 2, zb - L * k / nseg) for k in range(nseg + 1)]
            tube(nm('vn'), sp, 0.06, 'ev_bark', res=4, ures=2)
            for k in range(nseg * 2):
                t = (k + 0.5) / (nseg * 2)
                kk = min(nseg - 1, int(t * nseg))
                a, b = Vector(sp[kk]), Vector(sp[kk + 1])
                p = a.lerp(b, t * nseg - kk)
                ivy_leaf((p.x + rnd.uniform(-0.3, 0.3), p.y + rnd.uniform(-0.3, 0.3), p.z), rnd.uniform(0.32, 0.5) * (1 - 0.3 * t), rnd, 'y')
            if rnd.random() < 0.7:
                for _ in range(2):
                    t = rnd.uniform(0.25, 0.95)
                    kk = min(nseg - 1, int(t * nseg))
                    p = Vector(sp[kk]).lerp(Vector(sp[kk + 1]), t * nseg - kk)
                    blossom((p.x, p.y - 0.3, p.z), (0, -1, 0), 0.2, 'ev_petal_cream', 'ev_petal_gold')
    return finalize('hanging_moss_b', smooth_angle=60)


# ------------------------------------------------------------------ mushrooms
def shroom(x, y, z, h, r, cap_key, stem_key='ev_shroom_cream', tilt=(0.0, 0.0), style='dome', spots=0, rnd=None):
    lathe(nm('ms'), [(0, 0), (r * 0.46, 0), (r * 0.4, h * 0.15), (r * 0.3, h * 0.6), (r * 0.26, h), (0, h)], loc=(x, y, z), key=stem_key, segs=8)
    c = r * (0.55 if style == 'dome' else 0.3 if style == 'flat' else 0.8)
    if style == 'dome':
        prof = [(0, 0.85 * c), (0.4 * r, 0.8 * c), (0.8 * r, 0.5 * c), (r, 0.1 * c), (0.97 * r, -0.05 * c), (0.55 * r, -0.02 * c), (0, 0.0)]
    elif style == 'flat':
        prof = [(0, 0.9 * c), (0.45 * r, 0.8 * c), (0.9 * r, 0.35 * c), (r, 0.0), (0.97 * r, -0.12 * c), (0.5 * r, -0.05 * c), (0, 0.0)]
    else:
        prof = [(0, 1.15 * c), (0.3 * r, 1.0 * c), (0.62 * r, 0.5 * c), (0.72 * r, 0.0), (0.64 * r, -0.05 * c), (0.3 * r, -0.02 * c), (0, 0.0)]
    lathe(nm('mc'), prof, loc=(x, y, z + h - 0.04), key=cap_key, segs=10, rot=(math.degrees(tilt[0]), math.degrees(tilt[1]), 0))
    if spots and rnd is not None and tilt == (0.0, 0.0):
        for s in range(spots):
            a = rnd.uniform(0, 2 * PI)
            rho = r * rnd.uniform(0.15, 0.78)
            hh = c * (0.85 - 0.75 * (rho / r) ** 2) + 0.03
            ball(nm('sp'), r * rnd.uniform(0.07, 0.12), loc=(x + math.cos(a) * rho, y + math.sin(a) * rho, z + h - 0.04 + hh), key='ev_petal_cream', segs=5,
                 rings=3, scale=(1, 1, 0.4))


def mushroom_a():
    """Woodland cluster of brown, tan and cream mushrooms on a moss mound with leaf litter."""
    reset()
    rnd = random.Random(701)
    moss_skirt(5.2, 61, sx=1.15, h=0.2)
    caps = ('ev_shroom_brown', 'ev_shroom_tan', 'ev_shroom_umber', 'ev_shroom_cream', 'ev_shroom_brown')
    spec = []
    for i in range(3):
        spec.append((rnd.uniform(2.9, 4.2), rnd.uniform(1.4, 1.9)))
    for i in range(5):
        spec.append((rnd.uniform(1.7, 2.6), rnd.uniform(0.9, 1.25)))
    for i in range(5):
        spec.append((rnd.uniform(0.8, 1.4), rnd.uniform(0.5, 0.75)))
    placed = []
    for i, (h, r) in enumerate(spec):
        for _ in range(80):
            a = rnd.uniform(0, 2 * PI)
            d = math.sqrt(rnd.random()) * 3.4
            p = (math.cos(a) * d, math.sin(a) * d)
            if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > (r + q[2] + 0.3) ** 2 for q in placed):
                break
        placed.append((p[0], p[1], r))
        style = 'dome' if i % 3 else 'bell'
        shroom(p[0], p[1], 0.0, h, r, caps[i % 5], tilt=(rnd.uniform(-0.14, 0.14), rnd.uniform(-0.14, 0.14)), style=style)
    for i in range(7):
        a = rnd.uniform(0, 2 * PI)
        d = rnd.uniform(3.6, 5.2)
        ball(nm('lit'), rnd.uniform(0.5, 0.8), loc=(math.cos(a) * d, math.sin(a) * d, 0.12), key=rnd.choice(('ev_bark_light', 'ev_leaf_gold', 'ev_bark')), segs=5,
             rings=3, scale=(1.5, 0.8, 0.08))
    rock(nm('rk'), 1.2, (-3.9, 3.3, 0.0), 'ev_stone_dark', seed=9)
    tuft(4.4, -2.6, 0.0, rnd, n=6)
    return finalize('mushroom_a', smooth_angle=50)


def mushroom_b():
    """Mossy stump with stacked shelf fungi, and a group of red-capped toadstools at its foot."""
    reset()
    rnd = random.Random(702)
    from v4_elf import bark_trunk, roots
    bark_trunk(2.5, 8.0, seed=5, sway=0.2, flare=1.7, key='ev_bark', segs=14, ring_h=1.6, top_r=0.82)
    roots(2.5, n=7, seed=4, key='ev_bark', span=1.45)
    blob(nm('cap'), 2.2, (0, 0, 8.0), 'ev_moss', subdiv=2, amp=0.25, scale=(1.0, 1.0, 0.35), seed=6)
    cyl(nm('top'), 1.5, 0.3, loc=(0, 0, 7.9), key='ev_bark_light', verts=12)
    shelf = ('ev_shroom_tan', 'ev_shroom_cream', 'ev_shroom_umber', 'ev_shroom_tan', 'ev_shroom_cream', 'ev_shroom_umber')
    for i in range(10):
        z = 1.6 + i * 0.62 + rnd.uniform(-0.1, 0.1)
        a = rnd.uniform(0, 2 * PI) + i * 0.9
        tr = 2.5 * (0.82 + (1 - 0.82) * (1 - z / 8.0) ** 0.8)
        rr = rnd.uniform(1.3, 2.0) * (1.2 if i in (2, 6) else 1.0)
        c = ball(nm('sh'), rr, loc=(math.cos(a) * (tr - 0.1), math.sin(a) * (tr - 0.1), z), key=shelf[i % 6], segs=8, rings=4, scale=(1.0, 0.9, 0.26))
        c.rotation_euler = (0, 0, a)
        ball(nm('shu'), rr * 0.92, loc=(math.cos(a) * (tr - 0.1), math.sin(a) * (tr - 0.1), z - 0.06), key='ev_petal_cream', segs=8, rings=3,
             scale=(1.0, 0.88, 0.07)).rotation_euler = (0, 0, a)
    for i, (x, y, h, r) in enumerate(((4.3, -1.6, 2.6, 1.25), (5.6, 0.2, 1.7, 0.85), (3.4, -3.2, 1.2, 0.7), (6.2, -2.4, 2.0, 0.95), (4.8, 1.8, 0.9, 0.55))):
        shroom(x, y, 0.0, h, r, 'ev_berry_red', style='dome', spots=7, rnd=rnd)
    for (x, y, h, r) in ((-4.0, -3.4, 1.6, 0.8), (-5.0, -2.6, 1.0, 0.55)):
        shroom(x, y, 0.0, h, r, 'ev_shroom_tan', tilt=(0.1, -0.08))
    moss_skirt(5.6, 62, loc=(3.0, -1.0, 0.0), sx=1.25)
    mini_fern(-3.6, 3.8, 0.0, 6, 2.4, 63)
    tuft(0.4, -5.4, 0.0, rnd, n=6)
    return finalize('mushroom_b', smooth_angle=50)


# (manifest_id, fn[, view]) - views chosen so each model shows its best side
BATCH_D06 = [
    ('D06_01_fern_a', fern_a, (0.9, -1.1, 0.75)),
    ('D06_02_fern_b', fern_b, (0.9, -1.1, 0.6)),
    ('D06_03_fern_c', fern_c, (0.9, -1.1, 0.85)),
    ('D06_04_bush_a', bush_a, (1.0, -1.25, 0.45)),
    ('D06_05_bush_b', bush_b, (1.0, -1.25, 0.45)),
    ('D06_06_bush_c', bush_c, (1.0, -1.25, 0.45)),
    ('D06_07_flower_a', flower_a, (0.9, -1.1, 0.7)),
    ('D06_08_flower_b', flower_b, (0.9, -1.1, 0.5)),
    ('D06_09_flower_c', flower_c, (0.9, -1.1, 0.6)),
    ('D06_10_moss_rock_a', moss_rock_a, (1.0, -1.2, 0.5)),
    ('D06_11_moss_rock_b', moss_rock_b, (1.0, -1.2, 0.5)),
    ('D06_12_moss_rock_c', moss_rock_c, (1.0, -1.2, 0.4)),
    ('D06_13_ivy_a', ivy_a, (0.35, -1.0, 0.15)),
    ('D06_14_ivy_b', ivy_b, (1.0, -1.2, 0.35)),
    ('D06_15_ivy_c', ivy_c, (0.9, -1.1, 0.95)),
    ('D06_16_hanging_moss_a', hanging_moss_a, (0.6, -1.0, 0.1)),
    ('D06_17_hanging_moss_b', hanging_moss_b, (0.6, -1.0, 0.1)),
    ('D06_18_mushroom_a', mushroom_a, (0.9, -1.1, 0.7)),
    ('D06_19_mushroom_b', mushroom_b, (1.0, -1.2, 0.4)),
]
