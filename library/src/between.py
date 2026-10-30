"""Environment between areas (H1-H12). 1 unit = 1 stud, Z up, ground at z=0."""
import math, random
from mathutils import Vector
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, top_paint, flame, chain
from arch import (F, faces, lbox, lbeam, beam3, slab, lslab, window, door, band, gable_roof, cone_roof, railing, quoins, wall_lantern,
                  half_disc, arc_pts, nm)
from capital import stone_face, arch_block
from nature import rock, blob
from harbour import barrel_at, crate_at, line, sag, boards


def moss_rock(r, loc, seed, key='stone', scale=(1.2, 1.0, 0.7), moss=0.65):
    o = rock(nm('r'), r, loc, key, seed=seed, scale=scale)
    top_paint(o, 'moss', moss, seed)
    return o


def grass_tuft(x, y, rnd, h=0.9, key='leaf'):
    for k in range(5):
        a = rnd.uniform(0, 6.28)
        tube(nm('gt'), [(x, y, 0), (x + math.cos(a) * 0.3, y + math.sin(a) * 0.3, h * rnd.uniform(0.6, 1.0))], 0.06, key, res=2, taper=[1, 0.2])


def small_flowers(x, y, rnd, key, n=5):
    for k in range(n):
        px, py = x + rnd.uniform(-0.6, 0.6), y + rnd.uniform(-0.6, 0.6)
        h = rnd.uniform(0.5, 0.9)
        tube(nm('fs'), [(px, py, 0), (px, py, h)], 0.03, 'leaf', res=2)
        ball(nm('fh'), 0.13, loc=(px, py, h), key=key, segs=6, rings=4, scale=(1, 1, 0.6))


# ============================================================ H1 shrine
def roadside_shrine():
    """H1 - roadside shrine: stone niche on a stepped plinth with a little tiled roof, carved guardian statue, candles, offering bowl,
    a hanging lantern, wild flowers and a moss-covered base."""
    reset()
    rnd = random.Random(1)
    for k, (w, h) in enumerate(((5.2, 0.5), (4.4, 0.5))):
        box(nm('st'), (w, w * 0.8, h), loc=(0, 0, 0.25 + k * 0.5), key='stone_dark' if k == 0 else 'stone', bev=0.06)
    box(nm('bd'), (3.4, 2.6, 5.4), loc=(0, 0.2, 1.0 + 2.7), key='stone')
    fr = F(0, -1.1, 1.0, 0)
    stone_face(fr, -1.7, 1.7, 0.0, 5.4, 10, 11, keys=('stone', 'stone_light', 'stone_dark'))
    niche = [(-1.0, 0.0), (-1.0, 2.4)] + [(-math.cos(math.pi * i / 8), 2.4 + math.sin(math.pi * i / 8)) for i in range(1, 8)] + [(1.0, 2.4), (1.0, 0.0)]
    lslab(fr, [(px, -0.05, pz + 1.0) for px, pz in niche], (0, 0.9, 0), 'hole')
    lbox(fr, (2.6, 0.4, 0.3), 0, -0.2, 0.85, 'stone_light')
    # statue inside the niche
    sx, sy, sz = 0, -0.2, 1.2
    lathe(nm('rb'), [(0, 0), (0.6, 0), (0.55, 0.6), (0.42, 1.4), (0.34, 1.9), (0.2, 2.1), (0, 2.1)], loc=(sx, sy, sz), key='stone_light', segs=12)
    ball(nm('hd'), 0.26, loc=(sx, sy, sz + 2.35), key='stone_light', segs=10, rings=7)
    lathe(nm('hood'), [(0.32, 2.2), (0.36, 2.45), (0.22, 2.7), (0, 2.72)], loc=(sx, sy, sz), key='stone_light', segs=10)
    for s in (-1, 1):
        tube(nm('ar'), [(sx + s * 0.38, sy, sz + 1.8), (sx + s * 0.25, sy - 0.3, sz + 1.3), (sx, sy - 0.4, sz + 1.25)], 0.1, 'stone_light', res=4)
    ball(nm('orb'), 0.16, loc=(sx, sy - 0.48, sz + 1.32), key='glow_gold', segs=8, rings=6)
    # roof
    gable_roof(F(0, 0.2, 0, 0), 4.0, 3.4, 6.4, 1.5, keys=('tile_red_a', 'tile_red_b'), wall='stone', ov=0.4, ovg=0.3)
    ball(nm('fin'), 0.22, loc=(0, 0.2, 8.0), key='gold', segs=8, rings=6)
    # offerings
    for x in (-1.1, -0.6, 0.7, 1.15):
        h = rnd.uniform(0.3, 0.6)
        cyl(nm('cd'), 0.09, h, loc=(x, -1.3, 1.0), key='wax', verts=6)
        flame(nm('fl'), (x, -1.3, 1.0 + h), h=0.25, r=0.07, seed=int(x * 10))
    lathe(nm('bw'), [(0, 0), (0.25, 0), (0.4, 0.2), (0.38, 0.25), (0, 0.1)], loc=(0, -1.35, 1.0), key='bronze', segs=10)
    for k in range(3):
        ball(nm('fr'), 0.1, loc=(rnd.uniform(-0.15, 0.15), -1.35 + rnd.uniform(-0.15, 0.15), 1.25), key=('fruit', 'fl_yellow', 'fruit')[k], segs=6, rings=4)
    lbeam(fr, (1.7, 0.0, 5.0), (2.6, -0.1, 5.0), 0.12, 'iron')
    tube(nm('lh'), [(2.5, -1.0, 5.0), (2.5, -1.0, 4.4)], 0.03, 'iron', res=2)
    box(nm('lg'), (0.4, 0.4, 0.6), loc=(2.5, -1.0, 4.0), key='glass_lit')
    lathe(nm('lc'), [(0.34, 0), (0, 0.3)], loc=(2.5, -1.0, 4.3), key='iron', segs=4)
    for k, key in enumerate(('fl_white', 'fl_yellow', 'fl_purple', 'fl_red')):
        a = math.pi * 0.2 + k * 1.4
        small_flowers(math.cos(a) * 3.0, math.sin(a) * 2.6, rnd, key)
        grass_tuft(math.cos(a + 0.7) * 3.2, math.sin(a + 0.7) * 2.8, rnd)
    for k in range(3):
        moss_rock(0.5, (-2.6 + k * 0.4, 1.8 - k * 0.6, 0.2), 15 + k, scale=(1.3, 1.0, 0.6))
    return finalize('roadside_shrine', smooth_angle=35)


# ============================================================ H2 abandoned watchtower
def abandoned_watchtower():
    """H2 - abandoned watchtower, 26 studs: grey timber legs with cross bracing, sagging platform with missing planks, broken rail,
    torn shingle roof, snapped ladder, ivy climbing a leg and grass at the feet."""
    reset()
    rnd = random.Random(2)
    S, T, P = 4.0, 2.6, 17.0
    legs = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            b = (sx * S, sy * S, 0.0); t = (sx * T, sy * T, P + 5.5)
            tube(nm('lg'), [b, t], 0.4, 'wood_grey', res=4, taper=[1.15, 0.9])
            legs.append((Vector(b), Vector(t)))
    def at(i, z):
        b, t = legs[i]; return tuple(b.lerp(t, z / (P + 5.5)))
    order = [0, 1, 3, 2]
    for z0, z1 in ((1.0, 8.0), (8.0, 15.5)):
        for k in range(4):
            i, j = order[k], order[(k + 1) % 4]
            if (k, z0) == (2, 8.0):
                beam3(at(i, z0), tuple(Vector(at(i, z0)).lerp(Vector(at(j, z1)), 0.45)), 0.25, 0.35, 'wood_grey')
                continue
            beam3(at(i, z0), at(j, z1), 0.25, 0.35, 'wood_grey')
            beam3(at(i, z0 + 0.1), at(j, z0 + 0.1), 0.3, 0.35, 'wood_grey')
    # platform
    for k in range(9):
        if k in (2, 6):
            continue
        y = -3.3 + k * 0.82
        drop = 0.35 if k == 7 else 0.0
        box(nm('pk'), (6.6 if k != 5 else 4.2, 0.74, 0.25), loc=(0 if k != 5 else -1.2, y, P - drop), key=rnd.choice(('wood_grey', 'wood_old')), rot=(0, 4 if k == 7 else 0, rnd.uniform(-2, 2)))
    for s in (-1, 1):
        box(nm('jo'), (7.2, 0.4, 0.5), loc=(0, s * 3.0, P - 0.4), key='wood_grey')
        box(nm('jo'), (0.4, 7.2, 0.5), loc=(s * 3.0, 0, P - 0.4), key='wood_grey')
    fr = F(0, -3.2, P, 0)
    lbox(fr, (6.8, 0.2, 0.2), 0, 0, 1.6, 'wood_old')
    lbox(fr, (3.0, 0.2, 0.2), 1.6, 0, 3.4 - 2.6, 'wood_old', rot=(0, 18, 0))
    for x in (-3.0, -1.0, 2.4):
        lbox(fr, (0.18, 0.18, 1.6), x, 0, 0.8, 'wood_old')
    for s in (-1, 1):
        f2 = F(s * 3.2, 0, P, s * 90)
        lbox(f2, (6.8, 0.2, 0.2), 0, 0, 1.6, 'wood_old')
        for x in (-2.6, 0.0, 2.6):
            lbox(f2, (0.18, 0.18, 1.6), x, 0, 0.8, 'wood_old')
    # roof, partly torn
    for sx in (-1, 1):
        for sy in (-1, 1):
            if (sx, sy) == (1, 1):
                tube(nm('rpb'), [(sx * 2.8, sy * 2.8, P), (sx * 2.7, sy * 2.7, P + 2.4)], 0.2, 'wood_grey', res=4)
                continue
            tube(nm('rp'), [(sx * 2.8, sy * 2.8, P), (sx * 2.7, sy * 2.7, P + 5.0)], 0.2, 'wood_grey', res=4)
    zr = P + 5.0
    for k, (a0, keep) in enumerate(((0, 1.0), (90, 1.0), (180, 0.55), (270, 1.0))):
        a = math.radians(a0)
        c, s = math.cos(a), math.sin(a)
        p1 = (c * 4.0 - s * 4.0, s * 4.0 + c * 4.0, zr)
        p2 = (c * 4.0 + s * 4.0, s * 4.0 - c * 4.0, zr)
        top = (0, 0, zr + 3.4)
        if keep < 1:
            p2 = tuple(Vector(p1).lerp(Vector(p2), keep))
            top2 = tuple(Vector(p1).lerp(Vector(top), 0.9))
            slab([p1, p2, top2], (0, 0, 0.25), 'roof_old_b')
            for j in range(4):
                tube(nm('rr'), [Vector(p1).lerp(Vector((c * 4.0 + s * 4.0, s * 4.0 - c * 4.0, zr)), 0.6 + j * 0.1).to_tuple(), top], 0.08, 'wood_grey', res=2)
        else:
            slab([p1, p2, top], (0, 0, 0.25), 'roof_old' if k % 2 else 'roof_old_b')
    # ladder, snapped
    lx, ly = 0.0, -S - 0.4
    for s in (-0.6, 0.6):
        tube(nm('ld'), [(lx + s, ly, 0.0), (lx + s, ly + 0.7, 9.0 if s < 0 else 11.0)], 0.1, 'wood_grey', res=2)
    tube(nm('ldt'), [(lx - 0.6, ly + 1.4, 13.0), (lx - 0.6, ly + 1.9, P)], 0.1, 'wood_grey', res=2)
    tube(nm('ldt'), [(lx + 0.6, ly + 1.4, 12.5), (lx + 0.6, ly + 1.9, P)], 0.1, 'wood_grey', res=2)
    for k in range(13):
        z = 0.8 + k * 1.3
        if 9.0 < z < 13.2 or k in (3,):
            continue
        f = z / P
        tube(nm('lr'), [(lx - 0.6, ly + 1.9 * f * 0.95, z), (lx + 0.6, ly + 1.9 * f * 0.95, z)], 0.07, 'wood_grey', res=2)
    tube(nm('lf'), [(lx + 1.4, ly - 0.6, 0.15), (lx + 3.4, ly - 1.0, 0.15)], 0.1, 'wood_grey', res=2)
    # ivy up one leg
    b, t = legs[0]
    pts = []
    for k in range(10):
        p = b.lerp(t, k / 14)
        a = k * 1.3
        pts.append((p.x + math.cos(a) * 0.5, p.y + math.sin(a) * 0.5, p.z))
    tube(nm('iv'), pts, 0.06, 'ivy', res=2, ures=2)
    for p in pts[1:]:
        for j in range(3):
            ball(nm('il'), 0.32, loc=(p[0] + rnd.uniform(-0.3, 0.3), p[1] + rnd.uniform(-0.3, 0.3), p[2] + rnd.uniform(-0.4, 0.4)), key=rnd.choice(('ivy', 'leaf_dark')),
                 segs=6, rings=4, scale=(1, 1, 0.45))
    for k in range(8):
        a = rnd.uniform(0, 6.28); r = rnd.uniform(3.0, 6.0)
        grass_tuft(math.cos(a) * r, math.sin(a) * r, rnd, h=1.2, key=rnd.choice(('leaf', 'grass_dry')))
    return finalize('abandoned_watchtower', smooth_angle=30)


# ============================================================ H3-H4 ruins
def ruined_block(x, y, z, w, d, h, rnd, key='stone_light', rz=0.0, moss=0.6):
    o = box(nm('rb'), (w, d, h), loc=(x, y, z + h / 2), key=key, rot=(rnd.uniform(-4, 4), rnd.uniform(-4, 4), rz), bev=0.12)
    top_paint(o, 'moss', moss, int(abs(x * 7 + y * 3)))
    return o


def broken_column(x, y, h, r, rnd, key='stone_light', capital=False):
    cyl(nm('cb'), r * 1.35, 0.6, loc=(x, y, 0), key=key, verts=12, bev=0.06)
    lathe(nm('cs'), [(0, 0.6), (r, 0.6)] + [(r * (0.97 + 0.04 * (k % 2)), 0.6 + h * k / 8) for k in range(1, 8)] + [(r * 0.9, 0.6 + h), (0, 0.6 + h - 0.3)],
          loc=(x, y, 0), key=key, segs=12)
    for k in range(8):
        a = 2 * math.pi * k / 8
        box(nm('fl'), (0.12, 0.12, h * 0.9), loc=(x + math.cos(a) * r, y + math.sin(a) * r, 0.6 + h * 0.45), key='stone', rot=(0, 0, math.degrees(a)))
    if capital:
        box(nm('cap'), (r * 2.8, r * 2.8, 0.6), loc=(x, y, 0.9 + h), key=key, bev=0.08)
    top_paint(ball(nm('cm'), r * 0.9, loc=(x, y, 0.6 + h - 0.1), key='moss', segs=8, rings=4, scale=(1, 1, 0.25)), 'moss', 0.2, 1)


def ruins_1():
    """H3 - ancient ruins 1: a broken stone gateway arch with keystone, stub walls running off each side, fallen voussoirs and blocks,
    moss on every top face, ivy and grass tufts."""
    reset()
    rnd = random.Random(3)
    W, H, T = 8.0, 9.0, 2.2
    for s in (-1, 1):
        box(nm('pr'), (2.6, T, H), loc=(s * (W / 2 + 1.3), 0, H / 2), key='stone_light', bev=0.08)
        box(nm('pb'), (3.2, T + 0.6, 1.0), loc=(s * (W / 2 + 1.3), 0, 0.5), key='stone', bev=0.06)
        box(nm('pi'), (3.0, T + 0.4, 0.6), loc=(s * (W / 2 + 1.3), 0, H + 0.3), key='stone', bev=0.06)
    n = 9
    for i in range(n):
        if i in (6, 7):
            continue
        a0, a1 = math.pi * i / n, math.pi * (i + 1) / n
        am = (a0 + a1) / 2
        r0, r1 = W / 2, W / 2 + 1.8
        pts = [(-math.cos(a0) * r0, -T / 2, H + 0.6 + math.sin(a0) * r0), (-math.cos(a0) * r1, -T / 2, H + 0.6 + math.sin(a0) * r1),
               (-math.cos(a1) * r1, -T / 2, H + 0.6 + math.sin(a1) * r1), (-math.cos(a1) * r0, -T / 2, H + 0.6 + math.sin(a1) * r0)]
        o = slab(pts, (0, T, 0), 'stone_light' if i != 4 else 'stone')
        top_paint(o, 'moss', 0.7, 30 + i)
    for (x, w, h) in ((-W / 2 - 5.6, 6.0, 4.5), (-W / 2 - 10.0, 3.0, 2.0), (W / 2 + 5.2, 5.0, 3.2), (W / 2 + 8.8, 2.4, 1.2)):
        o = box(nm('sw'), (w, T * 0.9, h), loc=(x, 0, h / 2), key='stone', bev=0.08)
        top_paint(o, 'moss', 0.6, int(x))
        fr = F(x, -T * 0.45, 0, 0)
        stone_face(fr, -w / 2 + 0.2, w / 2 - 0.2, 0, h, int(w * h / 3) + 1, int(abs(x)) + 3, keys=('stone', 'stone_light', 'stone_dark'))
    for k in range(7):
        ruined_block(rnd.uniform(-1.0, 5.0), rnd.uniform(-5.0, -1.6), 0.0, rnd.uniform(1.2, 2.2), rnd.uniform(0.9, 1.6), rnd.uniform(0.8, 1.3), rnd, rz=rnd.uniform(0, 90))
    for k in range(2):
        a = math.radians(rnd.uniform(0, 40))
        o = slab([(2.0 + k * 2, -3.0 - k, 0.2), (3.6 + k * 2, -3.2 - k, 0.2), (3.8 + k * 2, -3.0 - k, 1.6), (2.2 + k * 2, -2.8 - k, 1.4)], (0, 1.6, 0), 'stone_light')
        top_paint(o, 'moss', 0.6, 60 + k)
    for s in (-1, 1):
        for k in range(10):
            z = 0.6 + k * 0.85
            for j in range(2):
                ball(nm('iv'), 0.4, loc=(s * (W / 2 + 0.2 + rnd.uniform(0, 1.6)), -T / 2 - 0.15, z + rnd.uniform(-0.3, 0.3)), key=rnd.choice(('ivy', 'leaf_dark')),
                     segs=6, rings=4, scale=(1, 0.45, 1)) if (k < 7 or s < 0) and rnd.random() < 0.75 else None
    for k in range(10):
        grass_tuft(rnd.uniform(-12, 10), rnd.uniform(-5, 3), rnd, h=1.1, key=rnd.choice(('leaf', 'leaf_light', 'grass_dry')))
    return finalize('ruins_1', smooth_angle=30)


def ruins_2():
    """H4 - ancient ruins 2: circular temple of eight fluted columns at different broken heights, one surviving lintel span,
    cracked round floor, a fallen column in drums, toppled altar and wild flowers."""
    reset()
    rnd = random.Random(4)
    R = 8.0
    cyl(nm('fl'), R + 1.6, 0.8, loc=(0, 0, 0), key='stone', verts=24, bev=0.1)
    for k in range(10):
        a0 = 2 * math.pi * k / 10
        a1 = a0 + 2 * math.pi / 10 - 0.06
        rr = R + 1.55
        o = slab([(math.cos(a0) * 1.0, math.sin(a0) * 1.0, 0.8), (math.cos(a0) * rr, math.sin(a0) * rr, 0.8), (math.cos(a1) * rr, math.sin(a1) * rr, 0.8),
                  (math.cos(a1) * 1.0, math.sin(a1) * 1.0, 0.8)], (0, 0, 0.12 + 0.05 * (k % 3)), 'stone_light' if k % 2 else 'cob_c')
    heights = [9.0, 9.0, 5.5, 2.4, 0.0, 6.8, 9.0, 3.6]
    for k, h in enumerate(heights):
        a = 2 * math.pi * k / 8
        x, y = math.cos(a) * R, math.sin(a) * R
        if h == 0:
            cyl(nm('cb'), 1.1, 0.6, loc=(x, y, 0.8), key='stone_light', verts=12)
            continue
        cyl(nm('cb0'), 1.15, 0.6, loc=(x, y, 0.8), key='stone_light', verts=12)
        lathe(nm('cs'), [(0, 1.4), (0.82, 1.4)] + [(0.82 * (0.97 + 0.04 * (j % 2)), 1.4 + h * j / 8) for j in range(1, 9)] + [(0, 1.4 + h)], loc=(x, y, 0), key='stone_light', segs=12)
        if h >= 9.0:
            box(nm('cp'), (2.2, 2.2, 0.7), loc=(x, y, 1.4 + h + 0.35), key='stone_light', bev=0.08)
        else:
            ball(nm('cm'), 0.75, loc=(x, y, 1.4 + h), key='moss', segs=8, rings=4, scale=(1, 1, 0.3))
    a0, a1 = 0.0, 2 * math.pi / 8
    p0 = Vector((math.cos(a0) * R, math.sin(a0) * R, 11.6)); p1 = Vector((math.cos(a1) * R, math.sin(a1) * R, 11.6))
    o = box(nm('ln'), ((p1 - p0).length + 2.0, 1.8, 1.2), loc=tuple((p0 + p1) / 2 + Vector((0, 0, 0.0))), key='stone_light', rot=(0, 0, math.degrees(math.atan2(p1.y - p0.y, p1.x - p0.x))), bev=0.08)
    top_paint(o, 'moss', 0.6, 41)
    a6, a7 = 2 * math.pi * 6 / 8, 2 * math.pi * 7 / 8
    q0 = Vector((math.cos(a6) * R, math.sin(a6) * R, 11.6))
    half = q0.lerp(Vector((math.cos(a7) * R, math.sin(a7) * R, 11.6)), 0.45)
    o = box(nm('lnb'), ((half - q0).length + 1.0, 1.8, 1.2), loc=tuple((q0 + half) / 2), key='stone_light', rot=(0, -6, math.degrees(math.atan2(half.y - q0.y, half.x - q0.x))), bev=0.08)
    top_paint(o, 'moss', 0.6, 42)
    fx, fy = 3.0, -12.0
    for j in range(4):
        cyl(nm('dr'), 0.82, 2.0, loc=(fx + j * 2.15, fy + j * 0.25, 0.82), key='stone_light', verts=12, rot=(0, 90, rnd.uniform(-8, 8)))
    box(nm('alt'), (3.0, 1.8, 1.4), loc=(0.6, 0.3, 1.5), key='stone', rot=(0, 14, 25), bev=0.1)
    box(nm('alt2'), (2.4, 1.4, 1.2), loc=(-0.8, -0.6, 1.4), key='stone_light', rot=(0, 0, -10), bev=0.1)
    for k, key in enumerate(('fl_white', 'fl_yellow', 'fl_purple', 'fl_blue', 'fl_white')):
        a = k * 1.25 + 0.3
        small_flowers(math.cos(a) * (R + 2.6), math.sin(a) * (R + 2.6), rnd, key, n=6)
        grass_tuft(math.cos(a + 0.5) * (R + 2.4), math.sin(a + 0.5) * (R + 2.4), rnd, h=1.2)
    for k in range(5):
        ruined_block(rnd.uniform(-R, R), rnd.uniform(R + 1.8, R + 4.0) * (1 if k % 2 else -1), 0.0, rnd.uniform(1.0, 1.8), rnd.uniform(0.8, 1.4), 0.9, rnd,
                     rz=rnd.uniform(0, 90))
    return finalize('ruins_2', smooth_angle=30)


# ============================================================ H5 campsite
def traveller_campsite():
    """H5 - traveller campsite: patched canvas A-frame tent with guy ropes and pegs, stone-ringed campfire with flames and logs,
    cooking pot on a tripod, log seats, bedroll, backpack, lantern and firewood."""
    reset()
    rnd = random.Random(5)
    L, Wt, Ht = 7.0, 5.6, 4.4
    for x in (-L / 2, L / 2):
        tube(nm('tp'), [(x, 0, 0), (x, 0, Ht + 0.3)], 0.1, 'wood', res=2)
    tube(nm('rg'), [(-L / 2 - 0.3, 0, Ht), (L / 2 + 0.3, 0, Ht)], 0.08, 'wood', res=2)
    for s in (-1, 1):
        slab([(-L / 2, 0, Ht), (L / 2, 0, Ht), (L / 2, s * Wt / 2, 0.05), (-L / 2, s * Wt / 2, 0.05)], (0, 0, 0.08), 'canvas')
        box(nm('pt'), (1.4, 0.06, 1.0), loc=(1.2, s * Wt * 0.3, Ht * 0.42), key='canvas_b', rot=(-s * (90 - math.degrees(math.atan2(Ht, Wt / 2))), 0, 0))
    slab([(L / 2, -Wt / 2, 0.05), (L / 2, Wt / 2, 0.05), (L / 2, 0, Ht)], (0.08, 0, 0), 'canvas_b')
    slab([(-L / 2, -Wt / 2, 0.05), (-L / 2, -0.4, 0.05), (-L / 2, 0, Ht)], (-0.08, 0, 0), 'canvas')
    slab([(-L / 2, 0.4, 0.05), (-L / 2, Wt / 2, 0.05), (-L / 2, 0, Ht)], (-0.08, 0, 0), 'canvas')
    slab([(-L / 2, -0.4, 0.05), (-L / 2 - 1.2, -1.2, 0.05), (-L / 2, 0, Ht * 0.92)], (0, 0.08, 0), 'canvas')
    slab([(-L / 2, -Wt / 2 * 0.1, 0.06), (-L / 2, Wt / 2 * 0.1, 0.06), (-L / 2 + 0.05, 0, Ht * 0.6)], (0.02, 0, 0), 'hole')
    for x in (-L / 2 - 0.3, L / 2 + 0.3):
        line((x, 0, Ht), (x + (2.6 if x > 0 else -2.6), 0, 0.1), 0.04)
        box(nm('pg'), (0.15, 0.15, 0.6), loc=(x + (2.6 if x > 0 else -2.6), 0, 0.2), key='wood_light', rot=(0, 20 if x > 0 else -20, 0))
    for s in (-1, 1):
        for x in (-L / 2 + 0.3, L / 2 - 0.3):
            box(nm('pg'), (0.12, 0.12, 0.5), loc=(x, s * (Wt / 2 + 0.25), 0.15), key='wood_light')
    # campfire
    fx, fy = -L / 2 - 5.0, -2.0
    for k in range(10):
        a = 2 * math.pi * k / 10
        rock(nm('fs'), 0.42, (fx + math.cos(a) * 1.3, fy + math.sin(a) * 1.3, 0.2), rnd.choice(('stone', 'stone_dark')), seed=50 + k, scale=(1.2, 1.0, 0.75), subdiv=1)
    cyl(nm('as'), 1.0, 0.1, loc=(fx, fy, 0), key='grout', verts=12)
    for k in range(5):
        a = 2 * math.pi * k / 5
        tube(nm('lg'), [(fx + math.cos(a) * 0.9, fy + math.sin(a) * 0.9, 0.2), (fx + math.cos(a) * 0.15, fy + math.sin(a) * 0.15, 0.7)], 0.13, 'bark', res=4)
    flame(nm('fl'), (fx, fy, 0.3), h=1.6, r=0.55, tongues=4, seed=5)
    flame(nm('flc'), (fx, fy, 0.3), h=0.9, r=0.3, key='flame_core', tongues=3, seed=6)
    for k in range(3):
        a = 2 * math.pi * k / 3
        tube(nm('tr'), [(fx + math.cos(a) * 1.6, fy + math.sin(a) * 1.6, 0), (fx, fy, 3.6)], 0.07, 'wood', res=2)
    chain(nm('pc'), (fx, fy, 3.5), (fx, fy, 2.5), link=0.25, thick=0.04)
    lathe(nm('pot'), [(0, 1.4), (0.5, 1.45), (0.62, 1.8), (0.6, 2.3), (0.66, 2.38), (0, 2.38)], loc=(fx, fy, 0), key='iron', segs=12)
    tube(nm('ph'), [(fx - 0.62, fy, 2.35), (fx, fy, 2.6), (fx + 0.62, fy, 2.35)], 0.03, 'iron', res=2)
    for (x, y, rz) in ((fx - 3.0, fy, 90), (fx + 0.5, fy - 3.0, 10), (fx + 2.8, fy + 0.4, 80)):
        cyl(nm('ls'), 0.5, 2.6, loc=(x - math.cos(math.radians(rz)) * 1.3, y - math.sin(math.radians(rz)) * 1.3, 0.5), key='bark', verts=10, rot=(0, 90, rz))
    # bedroll, pack, lantern, firewood
    cyl(nm('br'), 0.45, 2.6, loc=(2.2, -Wt / 2 - 1.2, 0.45), key='fabric_red', verts=12, rot=(0, 90, 0))
    for x in (2.7, 4.2):
        torus(nm('bs'), 0.47, 0.05, loc=(x, -Wt / 2 - 1.2, 0.45), key='rope_dark', segs=10, rsegs=3, rot=(0, 90, 0))
    box(nm('bp'), (1.0, 0.7, 1.4), loc=(-0.8, -Wt / 2 - 1.0, 0.7), key='canvas_b', bev=0.15)
    box(nm('bpf'), (0.8, 0.3, 0.6), loc=(-0.8, -Wt / 2 - 1.4, 0.5), key='canvas', bev=0.1)
    cyl(nm('bpr'), 0.3, 1.0, loc=(-1.3, -Wt / 2 - 1.0, 1.6), key='fabric_green', verts=8, rot=(0, 90, 0))
    lx, ly = fx + 2.4, fy - 2.2
    box(nm('lb'), (0.5, 0.5, 0.12), loc=(lx, ly, 0.06), key='iron')
    box(nm('lgl'), (0.4, 0.4, 0.6), loc=(lx, ly, 0.42), key='glass_lit')
    lathe(nm('lcp'), [(0.36, 0.72), (0, 1.0)], loc=(lx, ly, 0), key='iron', segs=4)
    for k in range(6):
        cyl(nm('fw'), 0.22, 1.8, loc=(L / 2 + 1.0, -1.2 + (k % 3) * 0.46, 0.22 + (k // 3) * 0.42), key='bark', verts=7, rot=(0, 90, 0))
    for k in range(6):
        grass_tuft(rnd.uniform(-12, 6), rnd.uniform(-6, 5), rnd, h=1.0, key=rnd.choice(('leaf', 'grass_dry')))
    return finalize('traveller_campsite', smooth_angle=30)


# ============================================================ H6 wagon wreck
def wagon_wreck():
    """H6 - wagon wreck: four-wheel wagon tipped onto a broken axle, one wheel off and lying flat, snapped boards, ripped canvas on bare
    hoops, spilled crates, a split barrel and grass growing through."""
    reset()
    rnd = random.Random(6)
    L, W = 10.0, 4.4
    tilt = 12
    box(nm('bed'), (L, W, 0.35), loc=(0, 0, 1.6), key='wood_old', rot=(tilt, 4, 0))
    for s in (-1, 1):
        for k in range(3):
            if (s, k) == (1, 2):
                continue
            box(nm('sb'), (L if k != 1 else L * 0.6, 0.18, 0.4), loc=(0 if k != 1 else -L * 0.2, s * W / 2 * math.cos(math.radians(tilt)), 2.1 + k * 0.5 + s * 0.4 * 0.0 - s * W / 2 * math.sin(math.radians(tilt))),
                key=rnd.choice(('wood_old', 'wood_grey')), rot=(tilt, 4, 0))
    box(nm('eb'), (0.2, W, 1.4), loc=(-L / 2, 0, 2.3), key='wood_old', rot=(tilt, 4, 0))
    for x in (-3.2, -0.2, 2.8):
        pts = []
        for j in range(9):
            a = math.pi * j / 8
            if x > 2 and j > 5:
                break
            y = -math.cos(a) * W / 2
            z = 2.4 + math.sin(a) * 2.6
            yy = y * math.cos(math.radians(tilt)) - (z - 1.6) * math.sin(math.radians(tilt))
            zz = 1.6 + y * math.sin(math.radians(tilt)) + (z - 1.6) * math.cos(math.radians(tilt))
            pts.append((x, yy, zz))
        tube(nm('hp'), pts, 0.07, 'wood_grey', res=2, ures=2)
    hp = [(-3.2, 0.0), (-0.2, 0.0)]
    pts_a = []
    slab([(-3.6, -2.6, 3.2), (-0.6, -2.8, 3.6), (-0.4, -2.4, 4.8), (-3.0, -1.8, 5.2)], (0, 0.1, 0.05), 'canvas_b')
    slab([(-3.4, -2.4, 1.4), (-1.2, -2.6, 1.3), (-1.0, -2.9, 3.0), (-3.2, -2.7, 3.4)], (0, -0.08, 0), 'canvas_b')
    # wheels
    def wheel(x, y, z, rot, r=1.6, broken=False):
        torus(nm('wr'), r, 0.16, loc=(x, y, z), key='wood_dark', segs=18, rsegs=4, rot=rot)
        cyl(nm('wh'), 0.35, 0.6, loc=(x, y, z), key='wood_dark', verts=10, rot=rot)
        q = Vector(rot)
        for k in range(10 if not broken else 7):
            a = 2 * math.pi * k / 10
            if rot[0] == 90:
                p = (x + math.cos(a) * r, y, z + math.sin(a) * r)
            else:
                p = (x + math.cos(a) * r, y + math.sin(a) * r, z)
            tube(nm('sp'), [(x, y, z), p], 0.07, 'wood_dark', res=2)
    wheel(-3.4, -W / 2 - 0.4, 1.6, (90, 0, 0))
    wheel(3.4, -W / 2 - 0.4, 1.4, (90, 0, 0), broken=True)
    wheel(-3.4, W / 2 + 0.4, 1.2, (90, 0, 0))
    wheel(6.5, 4.6, 0.2, (0, 0, 0))
    tube(nm('ax'), [(3.4, -W / 2, 1.4), (3.2, 1.0, 0.4)], 0.18, 'wood_dark', res=4)
    tube(nm('dp'), [(L / 2, 0, 1.4), (L / 2 + 4.0, 0.6, 0.2)], 0.15, 'wood_old', res=4)
    tube(nm('dp2'), [(L / 2 + 4.4, 1.2, 0.15), (L / 2 + 6.4, 1.6, 0.15)], 0.15, 'wood_old', res=4)
    for k in range(4):
        crate_at(rnd.uniform(-3.0, 5.0), -W / 2 - rnd.uniform(1.6, 4.2), 0.0, rnd.uniform(0.6, 0.85), rnd.uniform(-40, 40), key=rnd.choice(('wood_light', 'wood_old')))
    o = box(nm('bc'), (1.4, 0.15, 1.3), loc=(1.0, -W / 2 - 2.0, 0.08), key='wood_light', rot=(90, 0, 25))
    for k in range(6):
        a = math.pi * k / 5 + 0.2
        box(nm('bst'), (0.3, 0.12, 1.7), loc=(-6.4 + math.cos(a) * 0.4, -1.5 + k * 0.05, 0.08), key='wood', rot=(90, 0, 70 + k * 6))
    torus(nm('bh'), 0.75, 0.05, loc=(-6.5, -1.5, 0.1), key='rust', segs=12, rsegs=3)
    for k in range(10):
        grass_tuft(rnd.uniform(-6, 7), rnd.uniform(-5, 5), rnd, h=rnd.uniform(1.0, 1.6), key=rnd.choice(('leaf', 'grass_dry', 'leaf_light')))
    return finalize('wagon_wreck', smooth_angle=30)


# ============================================================ H7-H8 crops
def wheat_crop_rows():
    """H7 - wheat crop rows, 16 x 12: six ploughed ridges of golden wheat, each clump a sheaf of stalks with drooping ears,
    a gap where the reaper stopped, poppies at the edge and a tied sheaf."""
    reset()
    rnd = random.Random(7)
    rows, L = 6, 16.0
    for r in range(rows):
        y = -5.0 + r * 2.0
        box(nm('rd'), (L, 1.4, 0.4), loc=(0, y, 0.2), key='dirt', bev=0.15)
        n = 11
        for k in range(n):
            x = -L / 2 + 0.7 + k * (L - 1.4) / (n - 1) + rnd.uniform(-0.2, 0.2)
            if r == 3 and 2 <= k <= 4:
                for j in range(4):
                    tube(nm('sb'), [(x + rnd.uniform(-0.3, 0.3), y + rnd.uniform(-0.3, 0.3), 0.4), (x, y, 0.65)], 0.04, 'grass_dry', res=2)
                continue
            h = rnd.uniform(3.0, 3.8)
            for j in range(5):
                a = rnd.uniform(0, 6.28); lean = rnd.uniform(0.15, 0.5)
                tx, ty = x + math.cos(a) * lean, y + math.sin(a) * lean
                hh = h * rnd.uniform(0.85, 1.0)
                tube(nm('ws'), [(x + math.cos(a) * 0.1, y + math.sin(a) * 0.1, 0.4), (tx, ty, hh)], 0.04, 'grass_dry', res=2)
                ball(nm('we'), 0.13, loc=(tx + math.cos(a) * 0.12, ty + math.sin(a) * 0.12, hh + 0.25), key='autumn_c', segs=6, rings=4, scale=(1.0, 1.0, 3.4))
            for j in range(2):
                a = rnd.uniform(0, 6.28)
                tube(nm('wl'), [(x, y, 0.5), (x + math.cos(a) * 0.6, y + math.sin(a) * 0.6, 1.4)], 0.05, 'birch_leaf', res=2, taper=[1, 0.2])
    for k in range(8):
        x = -L / 2 + 1.0 + k * 2.0 + rnd.uniform(-0.4, 0.4)
        y = -6.4 + rnd.uniform(-0.3, 0.3)
        tube(nm('ps'), [(x, y, 0), (x, y, rnd.uniform(1.2, 1.8))], 0.03, 'leaf', res=2)
        ball(nm('pp'), 0.2, loc=(x, y, 1.6), key='fl_red', segs=6, rings=4, scale=(1, 1, 0.5))
    sx, sy = -3.0, 1.0
    for j in range(16):
        a = 2 * math.pi * j / 16
        tube(nm('sh'), [(sx + math.cos(a) * 0.5, sy + math.sin(a) * 0.5, 0.4), (sx + math.cos(a) * 0.15, sy + math.sin(a) * 0.15, 1.5),
                        (sx + math.cos(a) * 0.4, sy + math.sin(a) * 0.4, 2.6)], 0.05, 'grass_dry', res=2, ures=2)
    torus(nm('sht'), 0.2, 0.06, loc=(sx, sy, 1.5), key='rope', segs=10, rsegs=3)
    ball(nm('she'), 0.55, loc=(sx, sy, 2.8), key='autumn_c', segs=8, rings=6, scale=(1, 1, 0.6))
    return finalize('wheat_crop_rows', smooth_angle=30)


def cabbage_at(x, y, z, s, rnd, key='leaf_light'):
    ball(nm('cg'), 0.55 * s, loc=(x, y, z + 0.45 * s), key=key, segs=10, rings=7)
    for k in range(6):
        a = 2 * math.pi * k / 6 + rnd.uniform(-0.2, 0.2)
        o = ball(nm('cl'), 0.5 * s, loc=(x + math.cos(a) * 0.45 * s, y + math.sin(a) * 0.45 * s, z + 0.3 * s), key='leaf' if k % 2 else key, segs=8, rings=5,
                 scale=(1.1, 0.8, 0.4))
        o.rotation_euler = (0, math.radians(-30), a)


def vegetable_crop_rows():
    """H8 - vegetable crop rows, 16 x 12: ridged soil beds of cabbages, carrot tops, a row of orange pumpkins on vines,
    bean poles with climbing beans, a wicker basket of picked vegetables and a hand hoe."""
    reset()
    rnd = random.Random(8)
    L = 16.0
    for r in range(5):
        y = -5.0 + r * 2.4
        box(nm('rd'), (L, 1.6, 0.45), loc=(0, y, 0.22), key='dirt', bev=0.15)
        n = 9
        for k in range(n):
            x = -L / 2 + 0.9 + k * (L - 1.8) / (n - 1)
            if r in (0, 3):
                cabbage_at(x, y, 0.45, rnd.uniform(0.8, 1.05), rnd, key='leaf_light' if r == 0 else 'fl_purple')
            elif r == 1:
                for j in range(5):
                    a = 2 * math.pi * j / 5
                    tube(nm('ct'), [(x, y, 0.45), (x + math.cos(a) * 0.35, y + math.sin(a) * 0.35, 1.3)], 0.05, 'leaf_light', res=2, taper=[1, 0.4])
                    ball(nm('ctl'), 0.16, loc=(x + math.cos(a) * 0.4, y + math.sin(a) * 0.4, 1.35), key='leaf_light', segs=6, rings=4, scale=(1, 1, 0.5))
                lathe(nm('cr'), [(0.14, 0.5), (0.08, 0.3), (0, 0.15)], loc=(x, y, 0), key='fl_orange', segs=6)
            elif r == 2:
                if k % 2 == 0:
                    lathe(nm('pk'), [(0, 0.45), (0.6, 0.5), (0.85, 0.85), (0.75, 1.25), (0.15, 1.35), (0, 1.3)], loc=(x, y, 0), key='fl_orange', segs=12, sx=1.15)
                    tube(nm('pks'), [(x, y, 1.3), (x + 0.1, y, 1.55)], 0.07, 'leaf_dark', res=2)
                tube(nm('pv'), [(x, y, 0.5), (x + 0.9, y + 0.4, 0.5), (x + 1.8, y, 0.5)], 0.05, 'leaf', res=2)
                o = ball(nm('pl'), 0.45, loc=(x + 0.9, y + 0.5, 0.6), key='leaf', segs=8, rings=4, scale=(1, 1, 0.3))
            else:
                if k % 2 == 0:
                    for j in range(3):
                        a = 2 * math.pi * j / 3
                        tube(nm('bp'), [(x + math.cos(a) * 0.5, y + math.sin(a) * 0.5, 0.4), (x, y, 5.0)], 0.06, 'wood', res=2)
                    pts = [(x + math.cos(t * 2.1) * 0.5 * (1 - t / 6.0), y + math.sin(t * 2.1) * 0.5 * (1 - t / 6.0), 0.5 + t * 0.75) for t in range(6)]
                    tube(nm('bv'), pts, 0.04, 'leaf', res=2, ures=2)
                    for p in pts[1:]:
                        ball(nm('bl'), 0.25, loc=p, key='leaf', segs=6, rings=4, scale=(1, 1, 0.5))
                        tube(nm('bn'), [p, (p[0], p[1], p[2] - 0.5)], 0.05, 'leaf_light', res=2)
    bx, by = L / 2 + 1.4, -2.0
    lathe(nm('bk'), [(0, 0), (0.7, 0), (0.85, 0.9), (0.8, 0.95), (0, 0.15)], loc=(bx, by, 0), key='wicker', segs=12)
    tube(nm('bkh'), [(bx - 0.8, by, 0.9), (bx, by, 1.8), (bx + 0.8, by, 0.9)], 0.05, 'wicker', res=2)
    cabbage_at(bx - 0.2, by, 0.6, 0.55, rnd)
    lathe(nm('bpk'), [(0, 0.6), (0.35, 0.62), (0.45, 0.85), (0.1, 1.05), (0, 1.0)], loc=(bx + 0.3, by + 0.2, 0), key='fl_orange', segs=10)
    tube(nm('ho'), [(bx + 1.6, by - 1.0, 0.1), (bx - 0.6, by - 2.6, 0.1)], 0.06, 'wood_light', res=2)
    box(nm('hb'), (0.5, 0.7, 0.06), loc=(bx + 1.7, by - 0.9, 0.12), key='iron', rot=(0, 0, 36))
    return finalize('vegetable_crop_rows', smooth_angle=30)


# ============================================================ H9 scarecrow
def scarecrow():
    """H9 - scarecrow: crossed poles, stitched burlap head with button eyes and a stitched smile, floppy straw hat, patched coat,
    straw bursting from cuffs and hem, rope belt and a tin can rattle."""
    reset()
    rnd = random.Random(9)
    tube(nm('po'), [(0, 0, 0), (0, 0, 8.4)], 0.18, 'wood_grey', res=4)
    tube(nm('ar'), [(-3.4, 0, 6.0), (3.4, 0, 6.2)], 0.14, 'wood_grey', res=4)
    ball(nm('hd'), 0.95, loc=(0, 0, 7.8), key='canvas', segs=12, rings=9, scale=(1, 0.95, 1.08))
    for s in (-1, 1):
        cyl(nm('ey'), 0.17, 0.08, loc=(s * 0.35, -0.86, 8.0), key='tar', verts=8, rot=(90, 0, 0))
        for k in range(2):
            box(nm('ex'), (0.04, 0.03, 0.14), loc=(s * 0.35 + (k - 0.5) * 0.06, -0.9, 8.0), key='paper')
    for k in range(7):
        a = math.pi * (0.15 + 0.7 * k / 6)
        box(nm('sm'), (0.05, 0.04, 0.22), loc=(-math.cos(a) * 0.45, -0.88, 7.55 - math.sin(a) * 0.12), key='tar', rot=(0, 30 if k % 2 else -30, 0))
    torus(nm('nk'), 0.42, 0.1, loc=(0, 0, 6.95), key='rope', segs=12, rsegs=4)
    for k in range(8):
        a = 2 * math.pi * k / 8
        tube(nm('ns'), [(math.cos(a) * 0.35, math.sin(a) * 0.35, 6.9), (math.cos(a) * 0.7, math.sin(a) * 0.7, 6.6)], 0.04, 'grass_dry', res=2)
    lathe(nm('ht'), [(0, 8.55), (1.9, 8.5), (2.0, 8.6), (1.85, 8.7), (0.85, 8.72), (0.8, 9.4), (0.6, 9.75), (0, 9.8)], key='thatch', segs=16)
    torus(nm('hb'), 0.82, 0.08, loc=(0, 0, 8.85), key='fabric_red', segs=14, rsegs=4)
    lathe(nm('ct'), [(0, 3.0), (1.3, 3.0), (1.15, 4.5), (1.0, 5.6), (0.6, 6.4), (0.3, 6.8), (0, 6.8)], key='fabric_blue', segs=12, sy=0.65)
    for s in (-1, 1):
        tube(nm('sl'), [(s * 0.6, 0, 6.2), (s * 1.8, 0, 6.15), (s * 2.9, 0, 6.2)], 0.38, 'fabric_blue', res=4, taper=[1.1, 1.0, 0.85])
        for k in range(6):
            a = rnd.uniform(0, 6.28)
            tube(nm('cs'), [(s * 3.0, 0, 6.2), (s * 3.6, math.cos(a) * 0.3, 6.2 + math.sin(a) * 0.35 - 0.1)], 0.035, 'grass_dry', res=2)
        box(nm('pa'), (0.7, 0.1, 0.6), loc=(s * 0.55, -0.7, 4.4 + s * 0.4), key='fabric_red' if s > 0 else 'fabric_green', rot=(8, 0, s * 8))
    for k in range(14):
        a = 2 * math.pi * k / 14
        tube(nm('hs'), [(math.cos(a) * 1.1, math.sin(a) * 0.72, 3.1), (math.cos(a) * 1.3, math.sin(a) * 0.85, 2.3 + rnd.uniform(-0.3, 0.3))], 0.04, 'grass_dry', res=2)
    torus(nm('bl'), 1.1, 0.09, loc=(0, 0, 4.2), key='rope', segs=14, rsegs=4)
    tube(nm('cr'), [(1.0, -0.4, 4.2), (1.2, -0.5, 3.4)], 0.03, 'rope', res=2)
    lathe(nm('can'), [(0, 0), (0.22, 0), (0.22, 0.5), (0, 0.5)], loc=(1.2, -0.5, 2.85), key='tin_b', segs=10)
    for s in (-1, 1):
        box(nm('bt'), (0.15, 0.15, 0.6), loc=(s * 0.5, 0, 0.3), key='wood_grey', rot=(0, s * 18, 0))
    return finalize('scarecrow', smooth_angle=30)


# ============================================================ H10 windmill
def working_windmill():
    """H10 - working tower windmill, 30 studs: tapered stone tower with door, windows and string courses, timber gallery,
    rotating-cap with tiled roof, four lattice sails with canvas, tail pole with wheel, sacks at the door."""
    reset()
    rnd = random.Random(10)
    R0, R1, H = 6.0, 4.4, 20.0
    lathe(nm('tw'), [(0, 0), (R0 + 0.4, 0), (R0 + 0.4, 1.0), (R0, 1.0), (R1, H), (0, H)], key='stone_light', segs=20)
    for z in (7.0, 13.5):
        r = R0 + (R1 - R0) * z / H
        lathe(nm('sc'), [(r - 0.1, z), (r + 0.25, z), (r + 0.25, z + 0.4), (r - 0.1, z + 0.4)], key='stone', segs=20)
    def on_wall(a, z):
        r = R0 + (R1 - R0) * z / H
        return F(math.cos(a) * r, math.sin(a) * r, z, math.degrees(a) + 90)
    door(on_wall(-math.pi / 2, 1.0), 0, w=2.6, h=4.4, arch=True, key='door_paint', surround='stone', step='stone_dark')
    for (a, z) in ((-math.pi / 2, 9.0), (0.6, 4.0), (2.4, 10.0), (-2.4, 15.0), (-math.pi / 2, 15.0)):
        window(on_wall(a, z), 0, 0, w=1.4, h=2.0, arch=True, frame='wood_paint', shutter='shutter_g', sill='stone')
    zg = H - 3.0
    cyl(nm('gl'), R1 + 2.0, 0.4, loc=(0, 0, zg), key='timber', verts=20)
    for k in range(10):
        a = 2 * math.pi * k / 10
        beam3((math.cos(a) * (R1 + 0.4), math.sin(a) * (R1 + 0.4), zg - 2.6), (math.cos(a) * (R1 + 1.8), math.sin(a) * (R1 + 1.8), zg), 0.25, 0.3, 'timber')
        tube(nm('gp'), [(math.cos(a) * (R1 + 1.9), math.sin(a) * (R1 + 1.9), zg + 0.4), (math.cos(a) * (R1 + 1.9), math.sin(a) * (R1 + 1.9), zg + 1.6)], 0.07, 'timber', res=2)
    torus(nm('gr'), R1 + 1.9, 0.09, loc=(0, 0, zg + 1.6), key='timber', segs=20, rsegs=4)
    # cap
    cyl(nm('cb'), R1 + 0.3, 0.6, loc=(0, 0, H), key='timber', verts=20)
    lathe(nm('cap'), [(R1 + 0.6, H + 0.6), (R1 + 0.3, H + 2.4), (R1 - 0.6, H + 4.4), (R1 - 2.2, H + 6.0), (0.4, H + 6.8), (0, H + 6.9)], key='tile_red_a', segs=20, sy=1.15)
    ball(nm('cf'), 0.35, loc=(0, 0, H + 7.0), key='gold', segs=8, rings=6)
    # windshaft and sails, facing -y
    hub = (0, -R1 - 1.6, H + 2.6)
    tube(nm('ws'), [(0, -1.0, H + 2.4), hub], 0.55, 'wood_dark', res=4)
    ball(nm('hb'), 0.8, loc=hub, key='iron', segs=10, rings=7)
    for k in range(4):
        a = math.radians(20 + k * 90)
        c, s = math.cos(a), math.sin(a)
        L = 14.0
        tube(nm('sw'), [hub, (hub[0] + c * L, hub[1] - 0.2, hub[2] + s * L)], 0.28, 'wood_dark', res=4, taper=[1.0, 0.7])
        px, pz = -s, c
        for j in range(8):
            t = 2.6 + j * (L - 2.8) / 7
            p0 = (hub[0] + c * t, hub[1] - 0.25, hub[2] + s * t)
            p1 = (p0[0] + px * 2.6, p0[1], p0[2] + pz * 2.6)
            tube(nm('sb'), [p0, p1], 0.07, 'wood', res=2)
        for off in (0.0, 2.6):
            q0 = (hub[0] + c * 2.6 + px * off, hub[1] - 0.25, hub[2] + s * 2.6 + pz * off)
            q1 = (hub[0] + c * L + px * off, hub[1] - 0.25, hub[2] + s * L + pz * off)
            tube(nm('se'), [q0, q1], 0.07, 'wood', res=2)
        cv = [(hub[0] + c * 3.0 + px * 0.2, hub[1] - 0.32, hub[2] + s * 3.0 + pz * 0.2), (hub[0] + c * (L - 0.4) + px * 0.2, hub[1] - 0.32, hub[2] + s * (L - 0.4) + pz * 0.2),
              (hub[0] + c * (L - 0.4) + px * 2.4, hub[1] - 0.32, hub[2] + s * (L - 0.4) + pz * 2.4), (hub[0] + c * 3.0 + px * 2.4, hub[1] - 0.32, hub[2] + s * 3.0 + pz * 2.4)]
        slab(cv, (0, -0.06, 0), 'sail' if k % 2 else 'sail_b')
    # tail pole and wheel at the back
    tube(nm('tp'), [(0, R1, H + 1.0), (0, R1 + 6.0, 3.0), (0, R1 + 8.6, 0.8)], 0.3, 'timber', res=4)
    torus(nm('tw'), 0.9, 0.12, loc=(0, R1 + 8.6, 0.9), key='wood_dark', segs=12, rsegs=4, rot=(0, 90, 0))
    for k in range(6):
        a = math.pi * k / 3
        tube(nm('tws'), [(0, R1 + 8.6, 0.9), (0, R1 + 8.6 + math.cos(a) * 0.9, 0.9 + math.sin(a) * 0.9)], 0.05, 'wood_dark', res=2)
    for k in range(5):
        blob(nm('sk'), 0.75, (-2.2 + rnd.uniform(-0.8, 0.8), -R0 - 1.6 + rnd.uniform(-0.6, 0.6), 0.55 + (k // 3) * 0.8), 'canvas' if k % 2 else 'fabric_cream',
             subdiv=2, amp=0.14, scale=(1.3, 0.95, 0.7), seed=100 + k)
    return finalize('working_windmill', smooth_angle=30)


# ============================================================ H11 stone circle
def standing_stone_circle():
    """H11 - standing stone circle, 26 across: twelve weathered monoliths of different heights, two trilithon lintels,
    one fallen stone, a central altar slab with faint glowing runes, moss and lichen tops, ring of grass tufts."""
    reset()
    rnd = random.Random(11)
    R = 11.0
    n = 12
    for k in range(n):
        a = 2 * math.pi * k / n
        x, y = math.cos(a) * R, math.sin(a) * R
        if k == 7:
            o = blob(nm('fs'), 1.0, (x + math.cos(a) * 1.5, y + math.sin(a) * 1.5, 0.7), 'stone', subdiv=2, amp=0.12, scale=(1.4, 1.0, 4.2), seed=110 + k)
            o.rotation_euler = (0, math.radians(86), a)
            top_paint(o, 'moss', 0.5, 110 + k)
            continue
        h = 6.5 if k in (0, 1, 4, 5) else rnd.uniform(3.6, 6.0)
        o = blob(nm('ms'), 1.0, (x, y, h / 2), rnd.choice(('stone', 'stone_light', 'cliff_a')), subdiv=2, amp=0.12, scale=(1.35, 0.85, h / 2), seed=110 + k,
                 flat_bottom=-h / 2 * 0.95)
        o.rotation_euler = (math.radians(rnd.uniform(-4, 4)), math.radians(rnd.uniform(-4, 4)), a + math.pi / 2)
        top_paint(o, 'moss', 0.6, 110 + k)
        for j in range(3):
            ball(nm('lc'), 0.3, loc=(x * 1.07 + rnd.uniform(-0.3, 0.3), y * 1.07 + rnd.uniform(-0.3, 0.3), rnd.uniform(1.0, h - 1.0)), key='birch_leaf', segs=6, rings=4,
                 scale=(1, 1, 0.5))
    for k0 in (0, 4):
        a0, a1 = 2 * math.pi * k0 / n, 2 * math.pi * (k0 + 1) / n
        p0 = Vector((math.cos(a0) * R, math.sin(a0) * R, 6.9)); p1 = Vector((math.cos(a1) * R, math.sin(a1) * R, 6.9))
        o = box(nm('li'), ((p1 - p0).length + 2.4, 1.6, 1.2), loc=tuple((p0 + p1) / 2), key='stone_light', rot=(rnd.uniform(-3, 3), 0, math.degrees(math.atan2(p1.y - p0.y, p1.x - p0.x))), bev=0.2)
        top_paint(o, 'moss', 0.5, 120 + k0)
    o = box(nm('al'), (4.4, 2.6, 1.1), loc=(0, 0, 0.55), key='stone', bev=0.2)
    top_paint(o, 'moss', 0.85, 130)
    for k in range(5):
        box(nm('rn'), (0.12, 0.8, 0.03), loc=(-1.6 + k * 0.8, 0, 1.115), key='magic', rot=(0, 0, 25 if k % 2 else -25))
        box(nm('rn2'), (0.5, 0.1, 0.03), loc=(-1.6 + k * 0.8, 0.2 - (k % 2) * 0.4, 1.115), key='magic')
    for k in range(18):
        a = 2 * math.pi * k / 18 + rnd.uniform(-0.1, 0.1)
        grass_tuft(math.cos(a) * (R + 2.0), math.sin(a) * (R + 2.0), rnd, h=1.0, key=rnd.choice(('leaf', 'leaf_light', 'grass_dry')))
    for k, key in enumerate(('fl_white', 'fl_purple', 'fl_white', 'fl_yellow')):
        a = k * 1.6 + 0.8
        small_flowers(math.cos(a) * 5.5, math.sin(a) * 5.5, rnd, key, n=5)
    return finalize('standing_stone_circle', smooth_angle=30)


# ============================================================ H12 region entrance arch
def region_entrance_arch():
    """H12 - region entrance arch, 22 wide: ashlar piers with plinths and quoins spanning a road, round arch with keystone crest,
    carved name board, crenellated top, twin banners, iron lanterns on brackets and flower planters at the feet."""
    reset()
    rnd = random.Random(12)
    W, Hs, T, P = 14.0, 10.0, 3.0, 4.0
    for s in (-1, 1):
        x = s * (W / 2 + P / 2)
        box(nm('pb'), (P + 1.0, T + 1.0, 1.4), loc=(x, 0, 0.7), key='stone', bev=0.08)
        box(nm('pr'), (P, T, Hs), loc=(x, 0, Hs / 2), key='ashlar')
        for fr in (F(x, -T / 2, 0, 0), F(x, T / 2, 0, 180)):
            stone_face(fr, -P / 2, P / 2, 1.4, Hs, 8, int(10 + s + fr.rz), keys=('ashlar', 'ashlar_dark', 'castle'))
        for fr in (F(x - P / 2, 0, 0, -90), F(x + P / 2, 0, 0, 90)):
            quoins(fr, 1.4, Hs + 3.0, 'ashlar_dark', course=1.1)
        box(nm('imp'), (P + 0.4, T + 0.4, 0.5), loc=(x, 0, Hs + 0.25), key='ashlar_dark')
    arch_block(F(0, 0, 0, 0), -W / 2 - P, W / 2 + P, -T / 2, T / 2, Hs + 0.5, Hs + 9.5, 0.0, Hs + 0.5, W / 2, 'ashlar')
    for i in range(13):
        a = math.pi * i / 12
        p = (-math.cos(a) * (W / 2 + 0.5), -T / 2 - 0.15, Hs + 0.5 + math.sin(a) * (W / 2 + 0.5))
        box(nm('vs'), (1.1, 0.3, 0.6), loc=p, key='ashlar_dark', rot=(0, math.degrees(a) - 90, 0))
    box(nm('ks'), (1.6, 0.6, 2.2), loc=(0, -T / 2 - 0.2, Hs + 0.5 + W / 2 + 0.4), key='castle_trim', bev=0.06)
    lathe(nm('cr'), [(0, 0), (1.3, 0), (1.3, 0.15), (0, 0.15)], loc=(0, -T / 2 - 0.55, Hs + W / 2 + 2.2), key='gold', segs=6, rot=(90, 0, 0))
    lathe(nm('crc'), [(0, 0), (0.8, 0), (0.8, 0.15), (0, 0.15)], loc=(0, -T / 2 - 0.7, Hs + W / 2 + 2.2), key='fabric_red', segs=6, rot=(90, 0, 0))
    ball(nm('crs'), 0.35, loc=(0, -T / 2 - 0.9, Hs + W / 2 + 2.2), key='gold', segs=8, rings=6)
    box(nm('nb'), (8.0, 0.4, 1.5), loc=(0, -T / 2 - 0.2, Hs + 7.9), key='wood_dark', bev=0.05)
    box(nm('nbi'), (7.4, 0.42, 1.0), loc=(0, -T / 2 - 0.22, Hs + 7.9), key='shutter_b')
    for k in range(6):
        box(nm('nl'), (0.5, 0.45, 0.12), loc=(-2.6 + k * 1.05, -T / 2 - 0.25, Hs + 7.9), key='gold')
    ztop = Hs + 9.5
    box(nm('cn'), (W + 2 * P + 0.6, T + 0.6, 0.5), loc=(0, 0, ztop + 0.25), key='ashlar_dark')
    for side in (F(0, -T / 2 - 0.3, ztop + 0.5, 0), F(0, T / 2 + 0.3, ztop + 0.5, 180)):
        from arch import battlements
        battlements(side, -(W / 2 + P), W / 2 + P, 0, 'ashlar', cap='ashlar_dark')
    for s in (-1, 1):
        x = s * (W / 2 + P / 2)
        tube(nm('br'), [(x, -T / 2, ztop - 1.0), (x, -T / 2 - 1.2, ztop - 0.8)], 0.1, 'iron', res=2)
        poly_prism(nm('bn'), [(-1.3, 0), (1.3, 0), (1.3, -6.0), (0, -7.0), (-1.3, -6.0)], 0.1, loc=(x, -T / 2 - 1.15, ztop - 0.9), key='fabric_red' if s < 0 else 'fabric_blue',
                   rot=(90, 0, 0))
        ball(nm('bne'), 0.6, loc=(x, -T / 2 - 1.25, ztop - 4.0), key='gold', segs=8, rings=6, scale=(1, 0.3, 1))
        wall_lantern(F(x, -T / 2, 0, 0), 0, 5.4, 1.2)
        px = s * (W / 2 + P + 2.4)
        box(nm('pl'), (2.4, 2.4, 1.6), loc=(px, -1.0, 0.8), key='stone', bev=0.08)
        box(nm('pls'), (2.0, 2.0, 0.2), loc=(px, -1.0, 1.55), key='dirt')
        for k in range(9):
            a = 2 * math.pi * k / 9
            rr = rnd.uniform(0.2, 0.75)
            tube(nm('ps'), [(px + math.cos(a) * rr, -1.0 + math.sin(a) * rr, 1.6), (px + math.cos(a) * rr * 1.3, -1.0 + math.sin(a) * rr * 1.3, 2.6)], 0.04, 'leaf', res=2)
            ball(nm('pf'), 0.24, loc=(px + math.cos(a) * rr * 1.3, -1.0 + math.sin(a) * rr * 1.3, 2.65), key=('fl_red', 'fl_yellow', 'fl_white')[k % 3], segs=6, rings=4,
                 scale=(1, 1, 0.6))
        ball(nm('pb'), 0.9, loc=(px, -1.0, 2.0), key='leaf', segs=8, rings=6, scale=(1, 1, 0.6))
    return finalize('region_entrance_arch', smooth_angle=30)


ITEMS = [
    ('H01_roadside_shrine', roadside_shrine), ('H02_abandoned_watchtower', abandoned_watchtower), ('H03_ruins_1', ruins_1), ('H04_ruins_2', ruins_2),
    ('H05_traveller_campsite', traveller_campsite), ('H06_wagon_wreck', wagon_wreck), ('H07_wheat_crop_rows', wheat_crop_rows),
    ('H08_vegetable_crop_rows', vegetable_crop_rows), ('H09_scarecrow', scarecrow), ('H10_working_windmill', working_windmill),
    ('H11_standing_stone_circle', standing_stone_circle), ('H12_region_entrance_arch', region_entrance_arch),
]
