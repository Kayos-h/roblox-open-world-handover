"""v4_d03 - elven platforms, walkways, rope bridges, bridge anchor and railing set.
Natural woods, rope, moss-grey stone, warm lantern light only (no neon). Front faces -Y, 1 unit = 1 stud.
Modular rule: every deck in this group mates at DECK_Z (11 studs). 'connect' markers sit at deck height on the open ends.
"""
import math, random
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus
import v4util as U
from v4_elf import nm, lantern, plank_deck, ivy_strand, mushrooms, fern, ladder
from nature import rock

PI = math.pi
DECK_Z = 11.0
WOODS = ('ev_wood', 'ev_wood_light', 'ev_wood')


# ------------------------------------------------------------------ shared pieces
def _post(x, y, z0, z1, r=0.55, top=None, key='ev_wood_dark', foot=True):
    tx, ty = top if top else (x, y)
    tube(nm('pst'), [(x, y, z0), ((x + tx) / 2, (y + ty) / 2, (z0 + z1) / 2), (tx, ty, z1)], r, key, res=4, taper=[1.15, 1.0, 0.9], ures=2)
    if foot:
        cyl(nm('ftg'), r * 2.0, 0.55, loc=(x, y, z0 - 0.1), key='ev_stone_dark', verts=7)


def _gate_post(x, y, z, h=3.8, s=0.7):
    """Taller end post of a railing run, topped by a standing lantern (warm glow)."""
    cyl(nm('gp'), 0.2, h, loc=(x, y, z), key='ev_wood_dark', verts=6)
    lantern(x, y, z + h + 1.12 * s, s=s, hang=False)


def _rail_ring(cx, cy, z, R, gaps, post_h=3.0, inset=0.35):
    """Railing around a round deck with openings. gaps = [(centre_angle, half_width_angle)]. End posts of each run carry lanterns."""
    r = R - inset
    gl = sorted(((g % (2 * PI)), w) for g, w in gaps)
    for k, (g, w) in enumerate(gl):
        g2, w2 = gl[(k + 1) % len(gl)]
        a0 = g + w
        a1 = g2 - w2 + (2 * PI if k == len(gl) - 1 else 0.0)
        if a1 <= a0 + 0.05:
            continue
        m = max(2, int(round((a1 - a0) * r / 1.9)))
        pts = []
        for i in range(m + 1):
            a = a0 + (a1 - a0) * i / m
            x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
            pts.append((x, y))
            if i in (0, m):
                _gate_post(x, y, z)
            else:
                cyl(nm('post'), 0.13, post_h, loc=(x, y, z), key='ev_wood', verts=6)
                ball(nm('pc'), 0.17, loc=(x, y, z + post_h), key='ev_wood_light', segs=6, rings=4)
        tube(nm('rt'), [(p[0], p[1], z + post_h) for p in pts], 0.13, 'ev_wood_light', res=4, ures=3)
        tube(nm('rm'), [(p[0], p[1], z + post_h * 0.5) for p in pts], 0.08, 'ev_wood', res=4, ures=3)


def _stilted(R, zd, n, off_deg, splay, tiers, r_post=0.6):
    """Leaning stilts from the ground to under the deck, ring beams at each tier, rope-lashed X braces."""
    top_r = R - 1.6
    bot_r = top_r + splay
    h = zd - 0.55

    def at(i, z):
        a = math.radians(off_deg) + 2 * PI * i / n
        rr = bot_r + (top_r - bot_r) * (z / h)
        return (math.cos(a) * rr, math.sin(a) * rr, z)

    for i in range(n):
        p0, pm, p1 = at(i, 0.0), at(i, h / 2), at(i, h)
        tube(nm('stl'), [p0, pm, p1], r_post, 'ev_wood_dark', res=4, taper=[1.2, 1.0, 0.9], ures=2)
        cyl(nm('ftg'), r_post * 2.1, 0.7, loc=(p0[0], p0[1], -0.1), key='ev_stone_dark', verts=7)
        for z in tiers:
            q = at(i, z)
            torus(nm('lsh'), r_post + 0.1, 0.09, loc=q, key='rope_dark', segs=10, rsegs=3)
    for z in tiers:
        for i in range(n):
            tube(nm('rb'), [at(i, z), at((i + 1) % n, z)], 0.24, 'ev_wood', res=4)
    lo, hi = tiers[0], tiers[-1]
    for i in range(n):
        j = (i + 1) % n
        tube(nm('xb'), [at(i, lo), at(j, hi)], 0.13, 'rope_dark', res=4)
        tube(nm('xb'), [at(j, lo), at(i, hi)], 0.13, 'rope_dark', res=4)


def _plat_ladder(cx, cy, zd, R, a):
    """Ground ladder hanging from the deck rim, facing the deck, tied to the rim. Records ladder markers."""
    lx, ly = cx + math.cos(a) * (R + 0.55), cy + math.sin(a) * (R + 0.55)
    ladder(lx, ly, 0.0, zd + 3.2, a)
    tx, ty = -math.sin(a), math.cos(a)
    for side in (-1, 1):
        px, py = lx + tx * side * 1.15, ly + ty * side * 1.15
        tube(nm('tie'), [(px, py, zd - 0.9), (cx + math.cos(a) * (R - 0.5) + tx * side * 1.15, cy + math.sin(a) * (R - 0.5) + ty * side * 1.15, zd - 0.5)], 0.13, 'ev_wood_dark', res=4)
    U.marker('mk_lb', (lx, ly, 0.3))
    U.marker('mk_lt', (lx, ly, zd + 3.0))


def _crate(x, y, z, s=1.3, rot=0.0):
    box(nm('crt'), (s, s, s * 0.9), loc=(x, y, z + s * 0.45), key='ev_wood_aged', rot=(0, 0, rot), bev=0.05)


def _barrel(x, y, z):
    cyl(nm('brl'), 0.75, 1.6, loc=(x, y, z), key='ev_wood_dark', verts=10)
    for zz in (0.4, 1.2):
        torus(nm('brb'), 0.77, 0.05, loc=(x, y, z + zz), key='iron', segs=12, rsegs=3)


def _coil(x, y, z):
    torus(nm('coil'), 0.5, 0.15, loc=(x, y, z + 0.15), key='rope', segs=14, rsegs=4)
    torus(nm('coil'), 0.34, 0.14, loc=(x, y, z + 0.4), key='rope', segs=12, rsegs=4)


def _ivy_ring(cx, cy, z, R, rnd, avoid, n=8):
    for i in range(n):
        a = rnd.uniform(0, 2 * PI)
        if any(abs(((a - g + PI) % (2 * PI)) - PI) < w + 0.3 for g, w in avoid):
            continue
        ivy_strand((cx + math.cos(a) * (R - 0.1), cy + math.sin(a) * (R - 0.1), z - 0.6), rnd.uniform(2.5, 5.5), seed=i)


def _foot_plants(pts, seed):
    for i, (x, y) in enumerate(pts):
        fern(x * 1.1, y * 1.1, 0.0, n=6, L=1.4, seed=seed + i)
        if i % 2 == 0:
            mushrooms(x * 0.9 + 0.9, y * 0.9 + 0.5, 0.0, 3, seed=seed + i, scale=0.8)


# ------------------------------------------------------------------ D03_01 / 02 platforms
def platform_small():
    reset()
    rnd = random.Random(11)
    R, zd = 7.0, DECK_Z
    r = R - 0.35
    wg = math.asin(2.6 / r)         # walkway opening, half width 2.6 studs
    wl = math.asin(1.75 / r)        # ladder opening
    plank_deck(0, 0, zd, R, seed=11)
    _stilted(R, zd, 4, 45, 1.6, [3.2, 6.8, zd - 1.4])
    gaps = [(0.0, wg), (PI, wg), (PI / 2, wl)]
    _rail_ring(0, 0, zd, R, gaps)
    _plat_ladder(0, 0, zd, R, PI / 2)
    _crate(math.cos(math.radians(255)) * 4.2, math.sin(math.radians(255)) * 4.2, zd, 1.3, 20)
    _barrel(math.cos(math.radians(292)) * 4.4, math.sin(math.radians(292)) * 4.4, zd)
    _coil(math.cos(math.radians(215)) * 4.0, math.sin(math.radians(215)) * 4.0, zd)
    _ivy_ring(0, 0, zd, R, rnd, gaps, 8)
    top_r, bot_r = R - 1.6, R - 1.6 + 1.6
    _foot_plants([(math.cos(math.radians(a)) * bot_r, math.sin(math.radians(a)) * bot_r) for a in (45, 225)], 3)
    U.marker('mk_deck', (0, 0, zd + 0.4))
    U.marker('mk_conn', (R, 0, zd))
    U.marker('mk_conn', (-R, 0, zd))
    return finalize('ev_platform_small', smooth_angle=38)


def _bench(cx, cy, z, r, a, span=0.5):
    """Curved bench of seat boards on short legs, with a low back."""
    segs = 4
    for k in range(segs):
        aa = a - span / 2 + span * (k + 0.5) / segs
        w = r * span / segs * 1.02
        x, y = cx + math.cos(aa) * r, cy + math.sin(aa) * r
        box(nm('bs'), (0.95, w, 0.2), loc=(x, y, z + 1.05), key=WOODS[k % 3], rot=(0, 0, math.degrees(aa)), bev=0.03)
        x2, y2 = cx + math.cos(aa) * (r + 0.55), cy + math.sin(aa) * (r + 0.55)
        box(nm('bk'), (0.14, w, 0.5), loc=(x2, y2, z + 1.8), key='ev_wood_light', rot=(0, 0, math.degrees(aa)), bev=0.02)
    for s in (-1, 1):
        aa = a + s * span / 2 * 0.86
        x, y = cx + math.cos(aa) * r, cy + math.sin(aa) * r
        box(nm('bl'), (0.7, 0.22, 1.0), loc=(x, y, z + 0.5), key='ev_wood_dark', rot=(0, 0, math.degrees(aa)), bev=0.03)
        x2, y2 = cx + math.cos(aa) * (r + 0.55), cy + math.sin(aa) * (r + 0.55)
        box(nm('bp'), (0.16, 0.2, 1.6), loc=(x2, y2, z + 1.4), key='ev_wood_dark', rot=(0, 0, math.degrees(aa)), bev=0.02)


def platform_large():
    reset()
    rnd = random.Random(23)
    R, zd = 11.0, DECK_Z
    r = R - 0.35
    wg = math.asin(2.6 / r)
    wl = math.asin(1.75 / r)
    plank_deck(0, 0, zd, R, seed=23)
    _stilted(R, zd, 6, 30, 2.2, [3.4, 7.0, zd - 1.4], r_post=0.7)
    gaps = [(0.0, wg), (2 * PI / 3, wg), (4 * PI / 3, wg), (PI / 3, wl)]
    _rail_ring(0, 0, zd, R, gaps)
    _plat_ladder(0, 0, zd, R, PI / 3)
    # central lamp column: grows from the ground through the deck, three arms with hanging lanterns
    H = zd + 9.6
    tube(nm('col'), [(0, 0, 0), (0.05, 0, zd * 0.5), (0, 0.05, zd), (0, 0, H)], 0.8, 'ev_bark', res=4, taper=[1.7, 1.1, 0.9, 0.6], ures=3)
    cyl(nm('cft'), 2.3, 0.6, loc=(0, 0, -0.1), key='ev_stone_dark', verts=8)
    ball(nm('cap'), 0.45, loc=(0, 0, H + 0.1), key='bronze', segs=8, rings=6)
    torus(nm('hearth'), 2.0, 0.28, loc=(0, 0, zd + 0.28), key='ev_stone', segs=20, rsegs=5)
    for k in range(3):
        a = PI / 3 + 2 * PI * k / 3 + PI / 3
        c, s = math.cos(a), math.sin(a)
        az = zd + 8.4
        tube(nm('arm'), [(0, 0, az), (c * 1.6, s * 1.6, az + 0.55), (c * 3.3, s * 3.3, az + 0.1)], 0.12, 'bronze', res=4, taper=[1.0, 0.8, 0.7], ures=3)
        lantern(c * 3.3, s * 3.3, az + 0.1 - 0.9 * 0.9, s=0.9, hang=True)
    # benches in the arcs between the openings, props near the ladder
    _bench(0, 0, zd, 5.4, PI, 0.9)
    _bench(0, 0, zd, 5.4, 5 * PI / 3, 0.9)
    _barrel(math.cos(math.radians(32)) * 7.4, math.sin(math.radians(32)) * 7.4, zd)
    _barrel(math.cos(math.radians(26)) * 8.6, math.sin(math.radians(26)) * 8.6, zd)
    _crate(math.cos(math.radians(92)) * 7.5, math.sin(math.radians(92)) * 7.5, zd, 1.4, 35)
    _crate(math.cos(math.radians(98)) * 8.7, math.sin(math.radians(98)) * 8.7, zd, 1.1, 5)
    _coil(math.cos(math.radians(150)) * 6.5, math.sin(math.radians(150)) * 6.5, zd)
    _ivy_ring(0, 0, zd, R, rnd, gaps, 12)
    bot_r = R - 1.6 + 2.2
    _foot_plants([(math.cos(math.radians(a)) * bot_r, math.sin(math.radians(a)) * bot_r) for a in (30, 150, 270)], 9)
    U.marker('mk_deck', (0, 0, zd + 0.4))
    for g in (0.0, 2 * PI / 3, 4 * PI / 3):
        U.marker('mk_conn', (math.cos(g) * R, math.sin(g) * R, zd))
    return finalize('ev_platform_large', smooth_angle=38)


# ------------------------------------------------------------------ D03_03 / 04 walkways
def _a_frame(x, y_half_deck, zd, ground_spread=1.8, axis='x', ang=0.0):
    """Pair of leaning legs under the deck edge (stringers) with a crossbar and rope X brace. Works across the walkway (Y) at position x."""
    ztop = zd - 1.0
    for s in (-1, 1):
        _post(x, s * (y_half_deck + ground_spread), 0.0, ztop, r=0.5, top=(x, s * y_half_deck))
    zb = 4.2
    t = zb / ztop
    yb = y_half_deck + ground_spread * (1 - t)
    tube(nm('xbar'), [(x, -yb, zb), (x, yb, zb)], 0.24, 'ev_wood', res=4)
    for s in (-1, 1):
        torus(nm('lsh'), 0.58, 0.09, loc=(x, s * yb, zb), key='rope_dark', segs=10, rsegs=3)
    za, zc = 1.8, 7.6
    ya = y_half_deck + ground_spread * (1 - za / ztop)
    yc = y_half_deck + ground_spread * (1 - zc / ztop)
    tube(nm('xb'), [(x, -ya, za), (x, yc, zc)], 0.12, 'rope_dark', res=4)
    tube(nm('xb'), [(x, ya, za), (x, -yc, zc)], 0.12, 'rope_dark', res=4)


def walkway_straight():
    reset()
    rnd = random.Random(5)
    L, W, zd = 24.0, 4.4, DECK_Z
    n = int(L / 0.96)
    pw = L / n
    for i in range(n):
        x = -L / 2 + pw * (i + 0.5)
        key = WOODS[i % 3] if rnd.random() > 0.12 else 'ev_wood_aged'
        box(nm('pl'), (pw - 0.07, W, 0.3), loc=(x, 0, zd - 0.15 + rnd.uniform(-0.015, 0.015)), key=key, bev=0.03)
    for s in (-1, 1):
        box(nm('str'), (L + 0.2, 0.5, 0.65), loc=(0, s * (W / 2 - 0.7), zd - 0.3 - 0.325), key='ev_wood_dark', bev=0.05)
        box(nm('fas'), (L, 0.16, 0.5), loc=(0, s * (W / 2 + 0.02), zd - 0.25), key='ev_wood_dark', bev=0.03)
    for x in (-L / 2 + 0.6, -7.5, 0.0, 7.5, L / 2 - 0.6):
        box(nm('xbm'), (0.55, W + 0.4, 0.4), loc=(x, 0, zd - 0.3 - 0.65 - 0.2), key='ev_wood_dark', bev=0.04)
    for x in (-7.5, 7.5):
        _a_frame(x, W / 2 - 0.7, zd)
    m = 8
    xs = [-L / 2 + 0.4 + (L - 0.8) * i / m for i in range(m + 1)]
    for s in (-1, 1):
        y = s * (W / 2 - 0.2)
        for i, x in enumerate(xs):
            if i in (0, m):
                _gate_post(x, y, zd)
            else:
                cyl(nm('post'), 0.13, 3.0, loc=(x, y, zd), key='ev_wood', verts=6)
                ball(nm('pc'), 0.17, loc=(x, y, zd + 3.0), key='ev_wood_light', segs=6, rings=4)
        tube(nm('rt'), [(xs[0], y, zd + 3.0), (xs[-1], y, zd + 3.0)], 0.13, 'ev_wood_light', res=4)
        tube(nm('rm'), [(xs[0], y, zd + 1.5), (xs[-1], y, zd + 1.5)], 0.08, 'ev_wood', res=4)
    for x, y in ((-7.5, -W / 2 - 1.8), (7.5, W / 2 + 1.8)):
        fern(x, y * 1.05, 0.0, n=6, L=1.4, seed=int(x))
        mushrooms(x + 1.1, y * 1.0, 0.0, 3, seed=int(x) + 4, scale=0.8)
    U.marker('mk_deck', (0, 0, zd + 0.4))
    U.marker('mk_conn', (-L / 2, 0, zd))
    U.marker('mk_conn', (L / 2, 0, zd))
    return finalize('ev_walkway_straight', smooth_angle=38)


def walkway_curved():
    reset()
    rnd = random.Random(9)
    Rc, W, zd = 14.0, 4.4, DECK_Z
    arc = PI / 2
    n = int(Rc * arc / 0.96)
    pw = Rc * arc / n

    def P(a, rr, z):
        return (math.cos(a) * rr, math.sin(a) * rr, z)

    for i in range(n):
        a = arc * (i + 0.5) / n
        key = WOODS[i % 3] if rnd.random() > 0.12 else 'ev_wood_aged'
        box(nm('pl'), (W, pw * 0.88, 0.3), loc=P(a, Rc, zd - 0.15 + rnd.uniform(-0.015, 0.015)), key=key, rot=(0, 0, math.degrees(a)), bev=0.03)
    k = 9
    for s in (-1, 1):
        tube(nm('str'), [P(arc * j / k, Rc + s * (W / 2 - 0.7), zd - 0.62) for j in range(k + 1)], 0.33, 'ev_wood_dark', res=4, ures=3)
        tube(nm('fas'), [P(arc * j / k, Rc + s * (W / 2 + 0.02), zd - 0.25) for j in range(k + 1)], 0.12, 'ev_wood_dark', res=4, ures=3)
    for j in range(0, 5):
        a = arc * j / 4
        box(nm('xbm'), (W + 0.4, 0.55, 0.4), loc=P(a, Rc, zd - 1.15), key='ev_wood_dark', rot=(0, 0, math.degrees(a)), bev=0.04)
    for j in (1, 3):
        a = arc * j / 4
        # legs lean outward along the radial direction
        c, s_ = math.cos(a), math.sin(a)
        ztop = zd - 1.0
        for s in (-1, 1):
            r_top = Rc + s * (W / 2 - 0.7)
            r_bot = r_top + s * 1.8
            _post(c * r_bot, s_ * r_bot, 0.0, ztop, r=0.5, top=(c * r_top, s_ * r_top))
        zb = 4.2
        tt = zb / ztop
        rb = [Rc + s * ((W / 2 - 0.7) + 1.8 * (1 - tt)) for s in (-1, 1)]
        tube(nm('xbar'), [(c * rb[0], s_ * rb[0], zb), (c * rb[1], s_ * rb[1], zb)], 0.24, 'ev_wood', res=4)
        for rr in rb:
            torus(nm('lsh'), 0.58, 0.09, loc=(c * rr, s_ * rr, zb), key='rope_dark', segs=10, rsegs=3)
        ra = [Rc + s * ((W / 2 - 0.7) + 1.8 * (1 - 1.8 / ztop)) for s in (-1, 1)]
        rc = [Rc + s * ((W / 2 - 0.7) + 1.8 * (1 - 7.6 / ztop)) for s in (-1, 1)]
        tube(nm('xb'), [(c * ra[0], s_ * ra[0], 1.8), (c * rc[1], s_ * rc[1], 7.6)], 0.12, 'rope_dark', res=4)
        tube(nm('xb'), [(c * ra[1], s_ * ra[1], 1.8), (c * rc[0], s_ * rc[0], 7.6)], 0.12, 'rope_dark', res=4)
    m = 10
    for s in (-1, 1):
        rr = Rc + s * (W / 2 - 0.2)
        pts = []
        for i in range(m + 1):
            a = arc * i / m
            x, y, _ = P(a, rr, 0)
            pts.append((x, y))
            if i in (0, m):
                _gate_post(x, y, zd)
            else:
                cyl(nm('post'), 0.13, 3.0, loc=(x, y, zd), key='ev_wood', verts=6)
                ball(nm('pc'), 0.17, loc=(x, y, zd + 3.0), key='ev_wood_light', segs=6, rings=4)
        tube(nm('rt'), [(p[0], p[1], zd + 3.0) for p in pts], 0.13, 'ev_wood_light', res=4, ures=3)
        tube(nm('rm'), [(p[0], p[1], zd + 1.5) for p in pts], 0.08, 'ev_wood', res=4, ures=3)
    for a, rr in ((arc * 0.25, Rc + W / 2 + 2.6), (arc * 0.75, Rc - W / 2 - 2.6)):
        x, y, _ = P(a, rr, 0)
        fern(x, y, 0.0, n=6, L=1.4, seed=int(a * 10))
        mushrooms(x + 0.9, y + 0.6, 0.0, 3, seed=int(a * 10) + 4, scale=0.8)
    U.marker('mk_deck', (Rc * math.cos(arc / 2), Rc * math.sin(arc / 2), zd + 0.4))
    U.marker('mk_conn', (Rc, 0, zd))
    U.marker('mk_conn', (0, Rc, zd))
    return finalize('ev_walkway_curved', smooth_angle=38)


# ------------------------------------------------------------------ D03_05 / 06 rope bridges
def _rope_bridge(L, sag, W, tower_h, seed, long_span=False, name='ev_rope_bridge'):
    reset()
    rnd = random.Random(seed)
    zd, land = DECK_Z, 2.4
    TX = L / 2 + land

    def zc(x):
        return zd - sag * (1 - (2 * x / L) ** 2)

    def slope_deg(x):
        return -math.degrees(math.atan(8 * sag * x / (L * L)))

    n = int(L / 0.95)
    pw = L / n
    for i in range(n):
        x = -L / 2 + pw * (i + 0.5)
        key = WOODS[i % 3] if rnd.random() > 0.15 else 'ev_wood_aged'
        box(nm('pl'), (pw * 0.93, W, 0.22), loc=(x, 0, zc(x) - 0.11), rot=(0, slope_deg(x), 0), key=key, bev=0.02)
    # landings at both ends
    for sg in (-1, 1):
        xc = sg * (L / 2 + land / 2)
        for j in range(3):
            xx = xc + (j - 1) * land / 3
            box(nm('lp'), (land / 3 - 0.06, W + 0.5, 0.3), loc=(xx, 0, zd - 0.15), key=WOODS[j % 3], bev=0.03)
        for s in (-1, 1):
            box(nm('ls'), (land + 0.5, 0.5, 0.6), loc=(xc, s * (W / 2 - 0.4), zd - 0.6), key='ev_wood_dark', bev=0.05)
        box(nm('lx'), (0.6, W + 1.0, 0.5), loc=(sg * (L / 2 + 0.3), 0, zd - 0.9), key='ev_wood_dark', bev=0.04)
    # ropes: load cables under the deck edge, hand ropes and a mid rope on each side
    m = 14 if not long_span else 26
    xs = [-L / 2 + L * i / m for i in range(m + 1)]
    for s in (-1, 1):
        ye = s * (W / 2 + 0.1)
        tube(nm('cab'), [(-TX, s * (W / 2 + 0.3), zd - 0.4)] + [(x, ye, zc(x) - 0.3) for x in xs] + [(TX, s * (W / 2 + 0.3), zd - 0.4)], 0.17, 'rope_dark', res=4, ures=2)
        tube(nm('hand'), [(-TX, s * (W / 2 + 0.3), zd + 3.5)] + [(x, ye, zc(x) + 3.2) for x in xs] + [(TX, s * (W / 2 + 0.3), zd + 3.5)], 0.14, 'rope', res=4, ures=2)
        tube(nm('midr'), [(-TX, s * (W / 2 + 0.3), zd + 1.8)] + [(x, ye, zc(x) + 1.6) for x in xs] + [(TX, s * (W / 2 + 0.3), zd + 1.8)], 0.09, 'rope', res=4, ures=2)
        for i in range(1, n, 3):
            x = -L / 2 + pw * (i + 0.5)
            tube(nm('bal'), [(x, ye, zc(x) - 0.05), (x, ye, zc(x) + 3.2)], 0.06, 'rope_dark', res=4)
    # towers at both ends: leaning back, cross beam, stay ropes to anchor stones
    for sg in (-1, 1):
        x0 = sg * TX
        for s in (-1, 1):
            y = s * (W / 2 + 0.35)
            _post(x0, y, 0.0, zd + tower_h, r=0.62, top=(x0 + sg * 0.9, y))
            for zz in (zd - 0.4, zd + 1.8, zd + 3.5):
                torus(nm('lsh'), 0.7, 0.1, loc=(x0 + sg * 0.9 * zz / (zd + tower_h), y, zz), key='rope_dark', segs=10, rsegs=3)
            xa = x0 + sg * 4.6
            tube(nm('stay'), [(x0 + sg * 0.9, y, zd + tower_h - 0.4), (xa, y * 1.15, 0.9)], 0.12, 'rope_dark', res=4)
            tube(nm('bkb'), [(x0 + sg * 0.85, y, zd + 2.2), (xa - sg * 0.3, y * 1.15, 0.3)], 0.28, 'ev_wood_dark', res=4)
            box(nm('anc'), (1.9, 1.9, 1.0), loc=(xa, y * 1.15, 0.5), key='ev_stone_dark', rot=(0, 0, rnd.uniform(0, 30)), bev=0.1)
            lantern(x0 + sg * 0.9, y, zd + tower_h + 0.55 + 1.12 * 0.8, s=0.8, hang=False)
        box(nm('tcb'), (0.8, W + 1.9, 0.55), loc=(x0 + sg * 0.9, 0, zd + tower_h + 0.27), key='ev_wood_dark', bev=0.05)
        box(nm('tmb'), (0.6, W + 1.5, 0.45), loc=(x0 + sg * 0.5, 0, zd + tower_h * 0.5), key='ev_wood_dark', bev=0.04)
        fern(x0 + sg * 2.2, -W / 2 - 2.4, 0.0, n=6, L=1.4, seed=int(seed + sg))
        mushrooms(x0 + sg * 2.0, W / 2 + 2.2, 0.0, 3, seed=seed + 3, scale=0.8)
    if long_span:
        for sg in (-1, 1):
            for off in (7.0, 14.0):
                x = sg * (L / 2 - off)
                for s in (-1, 1):
                    tube(nm('stay'), [(sg * TX + sg * 0.9, s * (W / 2 + 0.35), zd + tower_h - 0.4), (x, s * (W / 2 + 0.1), zc(x) + 3.2)], 0.08, 'rope', res=4)
    U.marker('mk_deck', (0, 0, zc(0) + 0.4))
    U.marker('mk_conn', (-TX, 0, zd))
    U.marker('mk_conn', (TX, 0, zd))
    return finalize(name, smooth_angle=38)


def rope_bridge_short():
    return _rope_bridge(28.0, 1.8, 3.6, 5.0, 31, False, 'ev_rope_bridge_short')


def rope_bridge_long():
    return _rope_bridge(56.0, 3.8, 3.8, 6.4, 37, True, 'ev_rope_bridge_long')


# ------------------------------------------------------------------ D03_07 anchor
def bridge_anchor():
    reset()
    rnd = random.Random(17)
    zd = DECK_Z
    # stone footing slab with ballast boulders
    box(nm('slab'), (8.4, 8.6, 0.8), loc=(-1.2, 0, 0.4), key='ev_stone_dark', bev=0.12)
    box(nm('slab2'), (6.6, 6.8, 0.5), loc=(-0.6, 0, 1.0), key='ev_stone', bev=0.1)
    for i in range(7):
        a = rnd.uniform(0, 2 * PI)
        d = rnd.uniform(3.4, 4.6)
        rock(nm('bal'), rnd.uniform(0.9, 1.5), (-1.2 + math.cos(a) * d, math.sin(a) * d, 0.0), 'ev_stone_dark', seed=i)
    top_z = zd + 5.2
    for s in (-1, 1):
        y = s * 2.6
        _post(0.0, y, 1.2, top_z, r=0.8, top=(-1.0, y), foot=False)
        for zz in (3.0, 5.2, 8.5, 12.0):
            torus(nm('lsh'), 0.92, 0.12, loc=(-1.0 * zz / top_z, y, zz), key='rope_dark', segs=10, rsegs=3)
        # back braces down to the slab
        tube(nm('bkb'), [(-0.7, y, zd + 1.6), (-4.8, y * 1.05, 1.1)], 0.36, 'ev_wood_dark', res=4)
        cyl(nm('bfx'), 0.6, 0.4, loc=(-4.8, y * 1.05, 0.9), key='iron', verts=8)
        # rope stub that leaves toward the bridge, ending in an iron ring
        tube(nm('stub'), [(0.3, y, zd + 3.2), (2.2, y * 0.9, zd + 3.0), (4.2, y * 0.85, zd + 2.2)], 0.15, 'rope', res=4, ures=3)
        torus(nm('ring'), 0.38, 0.07, loc=(4.35, y * 0.85, zd + 2.0), key='iron', segs=10, rsegs=3, rot=(0, 90, 0))
    box(nm('tcb'), (0.9, 6.9, 0.7), loc=(-1.0, 0, top_z + 0.3), key='ev_wood_dark', bev=0.06)
    box(nm('mcb'), (0.7, 6.4, 0.55), loc=(-0.45, 0, zd - 0.1), key='ev_wood_dark', bev=0.05)
    # capstan drum between the posts with wound rope
    cyl(nm('cap'), 0.55, 4.6, loc=(0.2, -2.3, 5.0), key='ev_wood', verts=10, rot=(-90, 0, 0))
    for yy in (-1.4, -0.5, 0.4, 1.3):
        torus(nm('wrap'), 0.62, 0.15, loc=(0.2, yy, 5.0), key='rope', segs=12, rsegs=4, rot=(90, 0, 0))
    for yy in (-2.3, 2.3):
        cyl(nm('cpk'), 0.8, 0.18, loc=(0.2, yy, 5.0), key='ev_wood_dark', verts=10, rot=(-90, 0, 0))
    # lanterns on the post tops and a hanging one under the cross beam
    for s in (-1, 1):
        lantern(-1.0, s * 2.6, top_z + 0.65 + 1.12 * 0.9, s=0.9, hang=False)
    _coil(2.2, 0.0, 1.25)
    _barrel(-2.8, 0.0, 1.25)
    for i in range(2):
        ivy_strand((-1.0, (-1) ** i * 2.2, top_z - 0.2), 4.2, seed=i)
    fern(3.8, 3.9, 0.0, n=7, L=1.6, seed=1)
    fern(3.6, -3.9, 0.0, n=7, L=1.6, seed=2)
    mushrooms(-5.4, 3.2, 0.0, 4, seed=5, scale=0.9)
    U.marker('mk_conn', (4.35, -2.2, zd + 2.0))
    U.marker('mk_conn', (4.35, 2.2, zd + 2.0))
    U.marker('mk_deck', (0, 0, 1.4))
    return finalize('ev_bridge_anchor', smooth_angle=38)


# ------------------------------------------------------------------ D03_08 railing set (three fence styles, 12 studs each, side by side)
def railing_set():
    reset()
    L = 12.0
    xs = [-L / 2 + 3.0 * i for i in range(5)]

    def foot(x, y):
        box(nm('rft'), (0.9, 0.9, 0.4), loc=(x, y, 0.2), key='ev_stone_dark', bev=0.07)

    # a) plain post and rail (y = -6)
    y = -6.0
    for x in xs:
        foot(x, y)
        cyl(nm('pa'), 0.17, 3.3, loc=(x, y, 0.4), key='ev_wood', verts=6)
        ball(nm('pc'), 0.22, loc=(x, y, 3.7), key='ev_wood_light', segs=6, rings=4)
    for z, h, key in ((3.3, 0.3, 'ev_wood_light'), (2.1, 0.22, 'ev_wood'), (0.9, 0.22, 'ev_wood')):
        box(nm('ra'), (L, 0.2, h), loc=(0, y, z), key=key, bev=0.03)
    # b) lattice (y = 0)
    y = 0.0
    for x in xs:
        foot(x, y)
        cyl(nm('pb'), 0.2, 3.5, loc=(x, y, 0.4), key='ev_wood_dark', verts=6)
        box(nm('pbc'), (0.5, 0.5, 0.2), loc=(x, y, 4.0), key='ev_wood_light', bev=0.04)
    for z, h in ((3.5, 0.32), (0.8, 0.28)):
        box(nm('rb'), (L, 0.28, h), loc=(0, y, z), key='ev_wood_light' if z > 2 else 'ev_wood', bev=0.04)
    for i in range(4):
        x0, x1 = xs[i], xs[i + 1]
        w, h = 3.0 - 0.4, 3.5 - 0.8 - 0.2
        ln = math.hypot(w, h)
        ang = math.degrees(math.atan2(h, w))
        xm, zm = (x0 + x1) / 2, (0.9 + 3.4) / 2
        box(nm('lat'), (ln, 0.1, 0.13), loc=(xm, y, zm), key='ev_wood', rot=(0, -ang, 0), bev=0.015)
        box(nm('lat'), (ln, 0.12, 0.13), loc=(xm, y, zm), key='ev_wood_light', rot=(0, ang, 0), bev=0.015)
    # c) carved posts with sagging vine rails (y = +6)
    y = 6.0
    for x in xs:
        foot(x, y)
        cyl(nm('pc'), 0.22, 4.0, loc=(x, y, 0.4), key='ev_wood_dark', verts=8)
        for zz in (1.4, 2.8):
            torus(nm('band'), 0.24, 0.07, loc=(x, y, zz), key='ev_wood_light', segs=10, rsegs=3)
        lathe(nm('fin'), [(0, 0), (0.28, 0.12), (0.3, 0.5), (0.18, 0.95), (0, 1.35)], loc=(x, y, 4.4), key='bronze', segs=8)
    leaf_keys = ('ev_leaf_a', 'ev_leaf_b', 'ev_leaf_c')
    for i in range(4):
        x0, x1 = xs[i], xs[i + 1]
        for z0, dip in ((3.5, 1.1), (1.6, 0.7)):
            pts = [(x0, y, z0), ((x0 * 3 + x1) / 4, y, z0 - dip * 0.8), ((x0 + x1) / 2, y, z0 - dip), ((x0 + x1 * 3) / 4, y, z0 - dip * 0.8), (x1, y, z0)]
            tube(nm('vine'), pts, 0.1, 'ev_wood', res=4, ures=3)
            for j in range(5):
                t = (j + 0.5) / 5
                xx = x0 + (x1 - x0) * t
                zz = z0 - dip * (1 - (2 * t - 1) ** 2)
                ball(nm('lf'), 0.2, loc=(xx, y + (0.1 if j % 2 else -0.1), zz - 0.08), key=leaf_keys[(i + j) % 3], segs=6, rings=4, scale=(1, 0.5, 0.7))
    return finalize('ev_railing_set', smooth_angle=38)


# ------------------------------------------------------------------ batch list
BATCH_D03 = [
    ('D03_01_platform_small', platform_small),
    ('D03_02_platform_large', platform_large),
    ('D03_03_walkway_straight', walkway_straight, (0.5, -1.3, 0.55)),
    ('D03_04_walkway_curved', walkway_curved, (1.0, -1.3, 0.8)),
    ('D03_05_rope_bridge_short', rope_bridge_short, (0.5, -1.3, 0.4)),
    ('D03_06_rope_bridge_long', rope_bridge_long, (0.4, -1.3, 0.35)),
    ('D03_07_bridge_anchor', bridge_anchor, (1.0, -1.1, 0.4)),
    ('D03_08_railing_set', railing_set, (0.3, -1.3, 0.5)),
]
