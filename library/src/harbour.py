"""Harbour (G1-G33). 1 unit = 1 stud, Z up.
Pier pieces: seabed z=0, water about z=4, deck top z=8 (finalize moves origin to the bottom centre).
Ships: keel at z=0, waterline about 40% of hull depth."""
import math, random
import bmesh
from mathutils import Vector
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, top_paint, chain, _obj_from_bm
from arch import (F, faces, lbox, lbeam, beam3, slab, lslab, window, door, band, battlements, ring_battlements, gable_roof,
                  roof_z, cone_roof, chimney, railing, quoins, wall_lantern, nm)
from capital import house, hanging_sign, stone_face
from nature import rock, blob

DECK = 8.0
WL = 4.0


# ============================================================ small shared pieces
def sag(p0, p1, s=0.5, r=0.06, key='rope'):
    m = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, (p0[2] + p1[2]) / 2 - s)
    tube(nm('rp'), [p0, m, p1], r, key, res=2, ures=4)


def line(p0, p1, r=0.05, key='rope'):
    tube(nm('ln'), [p0, p1], r, key, res=2)


def solidify(o, t, off=0.0):
    m = o.modifiers.new('sol', 'SOLIDIFY')
    m.thickness = t
    m.offset = off
    return o


def piling(x, y, top=DECK - 0.4, r=0.55, seed=0, cap=True):
    rnd = random.Random(seed)
    lx, ly = rnd.uniform(-0.18, 0.18), rnd.uniform(-0.18, 0.18)
    tube(nm('pl'), [(x + lx, y + ly, 0.0), (x, y, top)], r, 'piling', res=4, taper=[1.1, 1.0])
    cyl(nm('alg'), r * 1.08, 1.9, loc=(x + lx * 0.6, y + ly * 0.6, WL - 1.7), key='algae', verts=10)
    for k in range(5):
        a = rnd.uniform(0, 6.28)
        z = rnd.uniform(0.5, WL - 1.9)
        f = 1 - z / top
        ball(nm('bn'), rnd.uniform(0.12, 0.2), loc=(x + lx * f + math.cos(a) * r * 1.05, y + ly * f + math.sin(a) * r * 1.05, z), key='barnacle', segs=6, rings=4)
    if cap:
        cyl(nm('pc'), r * 1.03, 0.14, loc=(x, y, top), key='tar', verts=10)


def deck_planks(x0, x1, y0, y1, z=DECK, t=0.45, pw=1.1, seed=0, across=True):
    """Planks laid side by side. across=True: each plank spans x, rows step along y."""
    rnd = random.Random(seed)
    if across:
        n = max(1, round((y1 - y0) / pw)); s = (y1 - y0) / n
        for i in range(n):
            box(nm('dk'), (x1 - x0 + rnd.uniform(-0.2, 0.1), s - 0.1, t), loc=((x0 + x1) / 2 + rnd.uniform(-0.1, 0.1), y0 + (i + 0.5) * s, z - t / 2 + rnd.uniform(-0.05, 0.02)),
                key=rnd.choice(('dock', 'dock', 'dock_b')), rot=(rnd.uniform(-0.5, 0.5), 0, 0))
    else:
        n = max(1, round((x1 - x0) / pw)); s = (x1 - x0) / n
        for i in range(n):
            box(nm('dk'), (s - 0.1, y1 - y0 + rnd.uniform(-0.2, 0.1), t), loc=(x0 + (i + 0.5) * s, (y0 + y1) / 2 + rnd.uniform(-0.1, 0.1), z - t / 2 + rnd.uniform(-0.05, 0.02)),
                key=rnd.choice(('dock', 'dock', 'dock_b')), rot=(0, rnd.uniform(-0.5, 0.5), 0))


def pier_frame(xs, ys, seed=0, tall=()):
    """Pilings on an xs * ys grid with stringers, cap beams and X bracing on the outer rows.
    tall: which outer x rows ('l', 'r') have pilings rising above the deck as posts."""
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            up = (i == 0 and 'l' in tall) or (i == len(xs) - 1 and 'r' in tall)
            piling(x, y, top=DECK + 1.6 if up else DECK - 0.45, seed=seed * 31 + i * 7 + j)
    for x in xs:
        box(nm('sg'), (0.9, ys[-1] - ys[0] + 1.4, 1.0), loc=(x, (ys[0] + ys[-1]) / 2, DECK - 0.95), key='piling')
    for y in ys:
        box(nm('cb'), (xs[-1] - xs[0] + 1.4, 1.0, 0.9), loc=((xs[0] + xs[-1]) / 2, y, DECK - 1.9), key='piling')
    for x in (xs[0], xs[-1]):
        for y0, y1 in zip(ys, ys[1:]):
            beam3((x, y0, WL + 0.3), (x, y1, DECK - 2.4), 0.32, 0.5, 'piling')
            beam3((x, y1, WL + 0.3), (x, y0, DECK - 2.4), 0.32, 0.5, 'piling')


def curb(x0, y0, x1, y1):
    L = math.hypot(x1 - x0, y1 - y0)
    a = math.degrees(math.atan2(y1 - y0, x1 - x0))
    box(nm('cu'), (L, 0.6, 0.5), loc=((x0 + x1) / 2, (y0 + y1) / 2, DECK + 0.25), key='dock_b', rot=(0, 0, a), bev=0.05)


def bollard_at(x, y, z, s=1.0, rope=False):
    lathe(nm('bo'), [(0, 0), (0.6 * s, 0), (0.55 * s, 0.22 * s), (0.4 * s, 0.45 * s), (0.34 * s, 1.1 * s), (0.5 * s, 1.32 * s), (0.54 * s, 1.48 * s),
                     (0.3 * s, 1.62 * s), (0, 1.66 * s)], loc=(x, y, z), key='iron', segs=14)
    if rope:
        torus(nm('bl'), 0.48 * s, 0.11 * s, loc=(x, y, z + 0.9 * s), key='rope', segs=14, rsegs=6)


def cleat_at(x, y, z, rz=0.0):
    a = math.radians(rz); c, s = math.cos(a), math.sin(a)
    box(nm('clb'), (0.5, 0.3, 0.3), loc=(x, y, z + 0.15), key='iron', rot=(0, 0, rz))
    tube(nm('clh'), [(x - c * 0.7, y - s * 0.7, z + 0.42), (x, y, z + 0.3), (x + c * 0.7, y + s * 0.7, z + 0.42)], 0.1, 'iron', res=4, taper=[0.7, 1, 0.7])


def lantern_post(x, y, z, h=7.0, arm=1.0):
    cyl(nm('lpb'), 0.32, h, loc=(x, y, z), key='piling', verts=8)
    tube(nm('la'), [(x, y, z + h - 0.4), (x + arm * 0.5, y, z + h + 0.05), (x + arm * 1.2, y, z + h - 0.15)], 0.07, 'iron', res=2)
    lx, lz = x + arm * 1.2, z + h - 1.9
    tube(nm('lh'), [(lx, y, z + h - 0.15), (lx, y, lz + 1.3)], 0.04, 'iron', res=2)
    box(nm('lb'), (0.6, 0.6, 0.14), loc=(lx, y, lz), key='iron')
    box(nm('lg'), (0.46, 0.46, 0.8), loc=(lx, y, lz + 0.5), key='glass_lit')
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(nm('lc'), (0.06, 0.06, 0.82), loc=(lx + sx * 0.24, y + sy * 0.24, lz + 0.5), key='iron')
    lathe(nm('lr'), [(0.42, 0), (0.1, 0.4), (0, 0.5)], loc=(lx, y, lz + 0.9), key='iron', segs=4)


def coil_at(x, y, z, R=1.3, turns=3, key='rope', flat=True, r=0.15):
    pts = []
    n = turns * 14
    for i in range(n + 1):
        a = 2 * math.pi * i / 14
        rr = (0.35 + (R - 0.35) * i / n) if flat else R
        zz = z + r if flat else z + r + i / 14 * r * 2
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr, zz))
    tube(nm('co'), pts, r, key, res=4, ures=2)
    return pts[-1]


def barrel_at(x, y, z, s=1.0, key='wood'):
    lathe(nm('ba'), [(0, 0), (0.62 * s, 0), (0.74 * s, 0.4 * s), (0.8 * s, 0.85 * s), (0.74 * s, 1.3 * s), (0.62 * s, 1.7 * s), (0, 1.7 * s)], loc=(x, y, z), key=key, segs=14)
    for zz, rr in ((0.2, 0.68), (0.6, 0.79), (1.1, 0.79), (1.5, 0.68)):
        lathe(nm('bh'), [(rr * s, (zz - 0.06) * s), (rr * s + 0.04, (zz - 0.06) * s), (rr * s + 0.04, (zz + 0.06) * s), (rr * s, (zz + 0.06) * s)], loc=(x, y, z), key='iron', segs=14)


def crate_at(x, y, z, s=1.0, rz=0.0, key='wood_light'):
    box(nm('cr'), (2.0 * s, 2.0 * s, 2.0 * s), loc=(x, y, z + s), key=key, rot=(0, 0, rz))
    a = math.radians(rz); c, sn = math.cos(a), math.sin(a)
    for k in (-1, 1):
        for zz in (0.15, 1.85):
            box(nm('cs'), (2.08 * s, 0.25 * s, 0.25 * s), loc=(x - sn * k * 0.9 * s, y + c * k * 0.9 * s, z + zz * s), key='wood_dark', rot=(0, 0, rz))
        box(nm('cd'), (2.06 * s, 0.22 * s, 0.3 * s), loc=(x - sn * k * 1.0 * s, y + c * k * 1.0 * s, z + s), key='wood_dark', rot=(45 * k, 0, rz))


def fender_at(x, y, z, side=1):
    """Rope fender hanging off a deck edge (side = +1 toward +y)."""
    tube(nm('fr'), [(x, y, z + 0.4), (x, y + side * 0.5, z + 0.2), (x, y + side * 0.6, z - 1.2)], 0.07, 'rope', res=2)
    ball(nm('fb'), 0.55, loc=(x, y + side * 0.65, z - 1.9), key='rope_dark', segs=10, rings=8, scale=(1, 1, 1.35))
    for dz in (-0.35, 0.35):
        torus(nm('fbr'), 0.5, 0.07, loc=(x, y + side * 0.65, z - 1.9 + dz), key='rope', segs=10, rsegs=4)


# ============================================================ G1-G5 piers
def pier_straight():
    """G1 - straight pier, 24 long x 12 wide: tarred pilings with algae and barnacles, X bracing, plank deck, curbs, bollard and cleats."""
    reset()
    pier_frame((-5.4, 0.0, 5.4), (-11.0, -5.5, 0.0, 5.5, 11.0), seed=1)
    deck_planks(-6.0, 6.0, -12.0, 12.0, seed=1)
    for s in (-1, 1):
        curb(s * 5.7, -12.0, s * 5.7, 12.0)
    bollard_at(4.6, 2.0, DECK, rope=True)
    cleat_at(-4.9, -6.0, DECK, 90)
    cleat_at(-4.9, 6.0, DECK, 90)
    coil_at(3.6, -7.0, DECK, R=1.0)
    for y in (-8.0, 8.0):
        tube(nm('fr'), [(6.1, y, DECK + 0.3), (6.5, y, DECK - 0.2), (6.6, y, DECK - 1.4)], 0.07, 'rope', res=2)
        ball(nm('fb'), 0.55, loc=(6.7, y, DECK - 2.1), key='rope_dark', segs=10, rings=8, scale=(1, 1, 1.35))
    return finalize('pier_straight', smooth_angle=30)


def pier_corner():
    """G2 - pier corner, 12 x 12: joins two straight piers at 90 degrees, outer curbs and a lantern post on the corner."""
    reset()
    pier_frame((-5.4, 0.0, 5.4), (-5.4, 0.0, 5.4), seed=2)
    deck_planks(-6.0, 6.0, -6.0, 6.0, seed=2)
    curb(5.7, -6.0, 5.7, 6.0)
    curb(-6.0, 5.7, 6.0, 5.7)
    box(nm('cp'), (1.2, 1.2, 0.6), loc=(5.6, 5.6, DECK + 0.3), key='dock_b')
    lantern_post(5.2, 5.2, DECK + 0.6, h=7.5, arm=-1.0)
    bollard_at(-3.0, 4.6, DECK)
    return finalize('pier_corner', smooth_angle=30)


def pier_end():
    """G3 - pier end, 12 x 14: three-side curb, tall corner posts, two bollards with rope, rope fenders and a lantern."""
    reset()
    pier_frame((-5.4, 0.0, 5.4), (-6.5, 0.0, 6.5), seed=3, tall=('l', 'r'))
    deck_planks(-6.0, 6.0, -7.0, 7.0, seed=3)
    curb(-5.7, -7.0, -5.7, 7.0)
    curb(5.7, -7.0, 5.7, 7.0)
    curb(-6.0, 6.7, 6.0, 6.7)
    for x in (-3.6, 3.6):
        bollard_at(x, 5.4, DECK, rope=True)
    lantern_post(0.0, 6.2, DECK + 0.5, h=8.0)
    for x in (-4.0, 0.0, 4.0):
        tube(nm('fr'), [(x, 7.0, DECK + 0.4), (x, 7.4, DECK - 0.1), (x, 7.6, DECK - 1.3)], 0.07, 'rope', res=2)
        ball(nm('fb'), 0.55, loc=(x, 7.7, DECK - 2.0), key='rope_dark', segs=10, rings=8, scale=(1, 1, 1.35))
        for dz in (-0.35, 0.35):
            torus(nm('fbr'), 0.5, 0.07, loc=(x, 7.7, DECK - 2.0 + dz), key='rope', segs=10, rsegs=4)
    crate_at(-3.4, -4.0, DECK, s=0.9, rz=12)
    barrel_at(-1.4, -4.6, DECK)
    return finalize('pier_end', smooth_angle=30)


def pier_stairs():
    """G4 - pier stairs and ladder: wooden flight from deck height down to a floating landing, handrail, iron ladder beside."""
    reset()
    rnd = random.Random(4)
    W = 5.0
    n = 9
    z0, z1 = DECK, WL + 1.0
    for i in range(n):
        f = (i + 0.5) / n
        z = z0 - (z0 - z1) * f
        box(nm('st'), (W, 1.2, 0.3), loc=(0, -f * 9.0, z), key=rnd.choice(('dock', 'dock_b')), bev=0.03)
    for s in (-1, 1):
        beam3((s * (W / 2 + 0.2), 0.4, z0 - 0.2), (s * (W / 2 + 0.2), -9.4, z1 - 0.4), 0.4, 1.0, 'piling')
        for k in range(4):
            f = k / 3
            x, y, z = s * (W / 2 + 0.2), -f * 9.0, z0 - (z0 - z1) * f
            box(nm('hp'), (0.3, 0.3, 3.4), loc=(x, y, z + 1.6), key='dock_b')
        tube(nm('hr'), [(s * (W / 2 + 0.2), 0.0, z0 + 3.2), (s * (W / 2 + 0.2), -9.0, z1 + 3.2)], 0.14, 'dock_b', res=4)
        piling(s * (W / 2 + 0.2), -4.5, top=z0 - (z0 - z1) * 0.5 - 0.8, r=0.45, seed=40 + s)
    # floating landing on barrels
    deck_planks(-3.2, 3.2, -15.0, -9.4, z=z1 + 0.1, seed=41, across=False)
    for x in (-2.2, 2.2):
        for y in (-13.8, -10.6):
            lathe(nm('fl'), [(0, -0.8), (0.9, -0.8), (1.0, 0.0), (0.9, 0.7), (0, 0.7)], loc=(x, y, z1 - 0.9), key='hull_dark', segs=12, rot=(0, 90, 0))
    for x in (-3.2, 3.2):
        piling(x, -15.4, top=z1 + 3.0, r=0.4, seed=43 + int(x))
        torus(nm('ri'), 0.65, 0.12, loc=(x, -15.4, z1 + 0.5), key='iron', segs=12, rsegs=4)
    cleat_at(0.0, -14.6, z1 + 0.1)
    # iron ladder on the pier face beside the stairs
    lx = W / 2 + 2.4
    for s in (-0.6, 0.6):
        tube(nm('lr'), [(lx + s, -0.35, WL - 1.0), (lx + s, -0.35, DECK + 1.4)], 0.09, 'iron', res=4)
    for k in range(10):
        z = WL - 0.6 + k * (DECK - WL + 0.4) / 9
        tube(nm('lg'), [(lx - 0.6, -0.35, z), (lx + 0.6, -0.35, z)], 0.06, 'iron', res=2)
    tube(nm('lt'), [(lx - 0.6, -0.35, DECK + 1.4), (lx - 0.6, 0.6, DECK + 0.6)], 0.09, 'iron', res=4)
    tube(nm('lt'), [(lx + 0.6, -0.35, DECK + 1.4), (lx + 0.6, 0.6, DECK + 0.6)], 0.09, 'iron', res=4)
    box(nm('top'), (W + 6.0, 1.6, 0.45), loc=(1.5, 0.8, DECK - 0.22), key='dock')
    return finalize('pier_stairs', smooth_angle=30)


def piling_cluster():
    """G5 - mooring dolphin: seven tarred pilings leaning together, rope lashings, iron hoop, algae and gull marks on the tops."""
    reset()
    rnd = random.Random(5)
    tops = []
    for i in range(7):
        if i == 6:
            bx, by, a = 0.0, 0.0, 0.0
        else:
            a = 2 * math.pi * i / 6
            bx, by = math.cos(a) * 1.9, math.sin(a) * 1.9
        top = rnd.uniform(9.0, 11.5) if i < 6 else 12.5
        tx, ty = bx * 0.45, by * 0.45
        tube(nm('pl'), [(bx, by, 0.0), (tx, ty, top)], 0.6, 'piling', res=4, taper=[1.1, 0.95])
        cyl(nm('pc'), 0.58, 0.12, loc=(tx, ty, top), key='tar', verts=10)
        ball(nm('gm'), 0.32, loc=(tx + 0.1, ty, top + 0.1), key='whitewash', segs=6, rings=4, scale=(1.3, 1, 0.3))
        tops.append((tx, ty, top))
    for z, r in ((WL - 1.0, 2.25), (WL + 0.2, 2.15)):
        cyl(nm('alg'), r, 1.4, loc=(0, 0, z), key='algae', verts=16)
    for z, r in ((7.4, 1.95), (9.0, 1.6)):
        torus(nm('lash'), r, 0.16, loc=(0, 0, z), key='rope', segs=20, rsegs=5)
        torus(nm('lash'), r, 0.16, loc=(0, 0, z + 0.32), key='rope', segs=20, rsegs=5)
    torus(nm('hoop'), 2.05, 0.14, loc=(0, 0, 5.6), key='rust', segs=20, rsegs=4)
    for k in range(10):
        a = rnd.uniform(0, 6.28); z = rnd.uniform(0.6, WL - 1.2)
        ball(nm('bn'), rnd.uniform(0.15, 0.24), loc=(math.cos(a) * 2.2, math.sin(a) * 2.2, z), key='barnacle', segs=6, rings=4)
    tube(nm('mr'), [(2.0, 0, 8.5), (3.2, 0.4, 7.4), (5.0, 0.6, 5.0)], 0.12, 'rope', res=4)
    return finalize('piling_cluster', smooth_angle=30)


# ============================================================ ship hulls
class Hull:
    """Lofted wooden hull. t runs 0 (stern) to 1 (bow); a runs 0 (keel) to 1 (rail)."""
    def __init__(s, L, B, D, bow=0.3, stern=0.7, sheer=1.4, keel_rise=0.45, flare=0.55, ns=30, nu=8, bulwark=1.2):
        s.L, s.B, s.D, s.bow, s.stern, s.sheer, s.kr, s.flare, s.ns, s.nu, s.bw = L, B, D, bow, stern, sheer, keel_rise, flare, ns, nu, bulwark

    def x(s, t):
        return -s.L / 2 + s.L * t

    def t_of(s, x):
        return (x + s.L / 2) / s.L

    def hb(s, t):
        b = 1.0
        if t > 1 - s.bow:
            k = (t - (1 - s.bow)) / s.bow
            b = math.sqrt(max(0.0, 1 - k * k))
        if t < 0.3:
            k = (0.3 - t) / 0.3
            b *= 1 - (1 - s.stern) * k * k
        return max(s.B / 2 * b, 0.06)

    def zk(s, t):
        z = 0.0
        if t > 1 - s.bow:
            k = (t - (1 - s.bow)) / s.bow
            z += s.kr * s.D * k * k
        if t < 0.12:
            k = (0.12 - t) / 0.12
            z += 0.18 * s.D * k * k
        return z

    def zd(s, t):
        u = 2 * t - 1
        return s.D + s.sheer * u * u * (1.0 if u < 0 else 0.85)

    def pt(s, t, a, side=1, out=0.0):
        hb = s.hb(t); ang = a * math.pi / 2
        y = side * (hb * math.sin(ang) ** s.flare + out * math.sin(ang))
        z = s.zk(t) + (s.zd(t) - s.zk(t)) * (1 - math.cos(ang)) - out * math.cos(ang)
        return (s.x(t), y, z)

    def deck_z(s, t):
        return s.zd(t) - s.bw

    def half_at(s, t, z):
        zk, zd = s.zk(t), s.zd(t)
        c = 1 - (z - zk) / max(zd - zk, 1e-4)
        c = min(1.0, max(-1.0, c))
        return max(0.05, s.hb(t) * math.sin(math.acos(c)) ** s.flare - 0.45)

    def build(s, key, thick=0.45):
        bm = bmesh.new()
        rows = []
        for i in range(s.ns + 1):
            t = i / s.ns
            rows.append([bm.verts.new(s.pt(t, abs(j) / s.nu, 1 if j >= 0 else -1)) for j in range(-s.nu, s.nu + 1)])
        for A, B in zip(rows, rows[1:]):
            for j in range(2 * s.nu):
                bm.faces.new((A[j], A[j + 1], B[j + 1], B[j]))
        f = bm.faces.new(rows[0])
        f.normal_update()
        if f.normal.x > 0:
            f.normal_flip()
        return solidify(_obj_from_bm(nm('hull'), bm, key), thick, -1.0)

    def deck(s, key='dock', t0=0.012, t1=0.97):
        bm = bmesh.new()
        rows = []
        n = s.ns
        for i in range(n + 1):
            t = t0 + (t1 - t0) * i / n
            z = s.deck_z(t)
            h = s.half_at(t, z)
            rows.append((bm.verts.new((s.x(t), -h, z)), bm.verts.new((s.x(t), h, z))))
        for A, B in zip(rows, rows[1:]):
            bm.faces.new((A[0], B[0], B[1], A[1]))
        return solidify(_obj_from_bm(nm('deck'), bm, key), 0.3, -1.0)

    def strip(s, a0, a1, key, out=0.05, t0=0.0, t1=1.0, n=2):
        for side in (-1, 1):
            bm = bmesh.new()
            rows = []
            for i in range(s.ns + 1):
                t = t0 + (t1 - t0) * i / s.ns
                rows.append([bm.verts.new(s.pt(t, a0 + (a1 - a0) * j / n, side, out)) for j in range(n + 1)])
            for A, B in zip(rows, rows[1:]):
                for j in range(n):
                    bm.faces.new((A[j], A[j + 1], B[j + 1], B[j]))
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.004)
            solidify(_obj_from_bm(nm('sp'), bm, key), 0.06, 0.0)

    def wale(s, a, key='tar', r=0.18, out=0.08, t0=0.01, t1=0.99, n=16):
        for side in (-1, 1):
            tube(nm('wl'), [s.pt(t0 + (t1 - t0) * i / n, a, side, out) for i in range(n + 1)], r, key, res=2, ures=3)

    def keel(s, key='hull_dark', r=0.35):
        pts = [s.pt(0.02 + 0.98 * i / 12, 0.0) for i in range(13)]
        pts += [s.pt(1.0, 0.0, 1, 0)[:2] + (s.zk(1.0) + (s.zd(1.0) - s.zk(1.0)) * k / 4,) for k in range(1, 5)]
        tube(nm('kl'), pts, r, key, res=4, ures=3)


def sail4(tl, tr, bl, br, bulge, key='sail', nu=7, nv=6, belly=0.62, reefs=()):
    bm = bmesh.new()
    V = Vector
    tl, tr, bl, br, bv = V(tl), V(tr), V(bl), V(br), V(bulge)
    g = []
    def P(u, v):
        L = tl.lerp(bl, v); R = tr.lerp(br, v)
        return L.lerp(R, u) + bv * (math.sin(math.pi * u) * math.sin(math.pi * belly * v))
    for i in range(nv + 1):
        g.append([bm.verts.new(P(j / nu, i / nv)) for j in range(nu + 1)])
    for A, B in zip(g, g[1:]):
        for j in range(nu):
            bm.faces.new((A[j], A[j + 1], B[j + 1], B[j]))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.01)
    solidify(_obj_from_bm(nm('sl'), bm, key), 0.12, 0.0)
    if bv.length:
        d = bv.normalized() * 0.08
        for v in reefs:
            tube(nm('rf'), [tuple(P(j / 6, v) + d) for j in range(7)], 0.05, 'sail_b', res=2, ures=2)


def tube_line(pts, r, key, taper=None):
    tube(nm('sp'), pts, r, key, res=4, taper=taper, ures=2)


def mast(x, z0, h, r, key='wood'):
    tube(nm('ms'), [(x, 0, z0), (x, 0, z0 + h)], r, key, res=4, taper=[1.0, 0.6])


def yard(x, z, w, r=0.35, key='wood'):
    tube(nm('yd'), [(x + 0.4, -w / 2, z), (x + 0.4, 0, z), (x + 0.4, w / 2, z)], r, key, res=4, taper=[0.55, 1.0, 0.55], ures=2)


def square_rig(x, z0, levels, top_at=None, sail_key='sail'):
    """levels: [(z, width, sail_height)]. Yards on the forward side, bellied sails, sheets, top platform."""
    for k, (z, w, hs) in enumerate(levels):
        yard(x, z, w)
        sail4((x + 0.5, -w * 0.46, z - 0.35), (x + 0.5, w * 0.46, z - 0.35), (x + 0.5, -w * 0.5, z - hs), (x + 0.5, w * 0.5, z - hs),
              (1.2 + 0.1 * w / 10, 0, 0), sail_key, reefs=(0.18, 0.36) if k == 0 else (0.22,))
        for s in (-1, 1):
            line((x + 0.4, s * w / 2, z), (x + 0.2, s * w * 0.15, z + 3.0), 0.04)
    if top_at:
        z, r = top_at
        cyl(nm('top'), r, 0.45, loc=(x, 0, z), key='hull_dark', verts=14)
        torus(nm('tr'), r, 0.08, loc=(x, 0, z + 1.1), key='hull_dark', segs=14, rsegs=4)
        for k in range(6):
            a = 2 * math.pi * k / 6
            line((x + math.cos(a) * r, math.sin(a) * r, z + 0.4), (x + math.cos(a) * r, math.sin(a) * r, z + 1.1), 0.05, 'hull_dark')


def shrouds(H, x, z_top, side_n=5, spread=0.07, rat=6, out=0.5):
    t = H.t_of(x)
    for side in (-1, 1):
        lines = []
        for k in range(side_n):
            tt = t - spread / 2 + spread * k / (side_n - 1)
            p0 = H.pt(tt, 1.0, side, out)
            p0 = (p0[0], p0[1], p0[2] - 0.3)
            p1 = (x, side * 0.5, z_top)
            line(p0, p1, 0.06, 'rope_dark')
            lines.append((Vector(p0), Vector(p1)))
        for j in range(1, rat + 1):
            f = j / (rat + 1) * 0.8
            a = lines[0][0].lerp(lines[0][1], f); b = lines[-1][0].lerp(lines[-1][1], f)
            line(tuple(a), tuple(b), 0.035, 'rope_dark')


def pennant(x, y, z, L=6.0, w=1.0, key='fabric_red'):
    poly_prism(nm('pn'), [(0, 0), (L, -w * 0.4), (L * 0.98, -w * 0.62), (0, -w)], 0.08, loc=(x, y + 0.04, z), key=key, rot=(90, 0, 0))


def flag(x, y, z, w=4.0, h=2.6, key='fabric_blue', emblem='gold'):
    poly_prism(nm('fg'), [(0, 0), (w, 0.15), (w, -h + 0.15), (0, -h)], 0.08, loc=(x, y + 0.04, z), key=key, rot=(90, 0, 0))
    ball(nm('fe'), h * 0.22, loc=(x + w * 0.5, y - 0.02, z - h * 0.5), key=emblem, segs=8, rings=6, scale=(1, 0.3, 1))


def ship_wheel(x, y, z, R=1.2):
    torus(nm('sw'), R, 0.1, loc=(x, y, z), key='wood_dark', segs=18, rsegs=4, rot=(0, 90, 0))
    for k in range(8):
        a = 2 * math.pi * k / 8
        tube(nm('sk'), [(x, y, z), (x, y + math.cos(a) * (R + 0.35), z + math.sin(a) * (R + 0.35))], 0.06, 'wood_dark', res=2)
    cyl(nm('sh'), 0.22, 0.3, loc=(x - 0.15, y, z), key='brass', verts=10, rot=(0, 90, 0))
    box(nm('sp'), (0.5, 0.5, z - 0.2), loc=(x + 0.4, y, (z - 0.2) / 2 + 0.0), key='wood_dark')


def anchor_parts(x, y, z, s=1.0, key='iron'):
    """Anchor standing in the XZ plane, crown at z, ring at the top."""
    H = 7.0 * s
    tube(nm('an'), [(x, y, z + 0.4 * s), (x, y, z + H)], 0.28 * s, key, res=4, taper=[1.1, 0.85])
    for sd in (-1, 1):
        pts = [(x, y, z + 0.4 * s), (x + sd * 1.4 * s, y, z + 0.55 * s), (x + sd * 2.5 * s, y, z + 1.4 * s), (x + sd * 2.9 * s, y, z + 2.6 * s)]
        tube(nm('aa'), pts, 0.24 * s, key, res=4, taper=[1.2, 1.0, 0.9, 0.7], ures=3)
        poly_prism(nm('af'), [(-0.6 * s, 0), (0.6 * s, 0), (0.0, 1.5 * s)], 0.22 * s, loc=(x + sd * 2.75 * s, y + 0.11 * s, z + 2.0 * s), key=key,
                   rot=(90, sd * -24, 0))
    ball(nm('ac'), 0.42 * s, loc=(x, y, z + 0.4 * s), key=key, segs=10, rings=7)
    box(nm('ast'), (0.5 * s, 4.8 * s, 0.5 * s), loc=(x, y, z + H - 1.1 * s), key='wood_dark', bev=0.05)
    for k in (-1, 1):
        box(nm('asb'), (0.56 * s, 0.14 * s, 0.56 * s), loc=(x, y + k * 1.6 * s, z + H - 1.1 * s), key=key)
    torus(nm('ar'), 0.6 * s, 0.13 * s, loc=(x, y, z + H + 0.5 * s), key=key, segs=14, rsegs=5, rot=(90, 0, 0))


def gunports(H, ts, a, guns=True, lid='hull_red'):
    for t in ts:
        for side in (-1, 1):
            x, y, z = H.pt(t, a, side, 0.04)
            box(nm('gp'), (1.5, 0.3, 1.25), loc=(x, y, z), key='tar')
            box(nm('gl'), (1.6, 0.16, 1.25), loc=(x, y + side * 0.55, z + 1.05), key=lid, rot=(side * -50, 0, 0))
            if guns:
                lathe(nm('gn'), [(0, 0), (0.36, 0), (0.32, 1.1), (0.4, 1.2), (0.3, 1.25), (0, 1.25)], loc=(x, y - side * 0.4, z), key='iron', segs=10,
                      rot=(-side * 90, 0, 0))


def hatch(x, y, z, w=4.0, d=3.0):
    box(nm('hc'), (w + 0.5, d + 0.5, 0.6), loc=(x, y, z + 0.3), key='hull_dark')
    for k in range(int(w / 0.8)):
        box(nm('hg'), (0.14, d, 0.14), loc=(x - w / 2 + 0.4 + k * 0.8, y, z + 0.65), key='wood_dark')
    for k in range(int(d / 0.8)):
        box(nm('hg'), (w, 0.14, 0.14), loc=(x, y - d / 2 + 0.4 + k * 0.8, z + 0.65), key='wood_dark')


def capstan(x, y, z):
    lathe(nm('cap'), [(0, 0), (1.0, 0), (0.7, 0.3), (0.55, 1.2), (0.8, 1.5), (0.8, 1.8), (0, 1.8)], loc=(x, y, z), key='wood_dark', segs=12)
    for k in range(6):
        a = 2 * math.pi * k / 6
        tube(nm('cb'), [(x + math.cos(a) * 0.7, y + math.sin(a) * 0.7, z + 1.65), (x + math.cos(a) * 2.2, y + math.sin(a) * 2.2, z + 1.65)], 0.08, 'wood', res=2)


def stern_lantern(x, y, z, s=1.0):
    lathe(nm('sl'), [(0, 0), (0.25 * s, 0), (0.55 * s, 0.5 * s), (0.6 * s, 1.0 * s), (0.5 * s, 1.5 * s), (0, 1.6 * s)], loc=(x, y, z), key='glass_lit', segs=8)
    lathe(nm('slc'), [(0.62 * s, 1.45 * s), (0.4 * s, 1.9 * s), (0.08 * s, 2.3 * s), (0, 2.5 * s)], loc=(x, y, z), key='gold', segs=8)
    lathe(nm('slb'), [(0.3 * s, -0.3 * s), (0.32 * s, 0.05 * s), (0, 0.05 * s)], loc=(x, y, z), key='gold', segs=8)


# ============================================================ G6-G10 ships
def galleon():
    """G6 - large three-masted galleon, 72 studs: lofted hull with red strake and gunports, stern castle with lit gallery windows,
    forecastle, square-rigged fore and main masts, lateen mizzen, jibs, shrouds and ratlines, figurehead, anchors, wheel and capstan."""
    reset()
    H = Hull(72, 18, 10.5, bow=0.32, stern=0.72, sheer=1.6, keel_rise=0.55)
    H.build('hull')
    H.deck('dock')
    H.strip(0.0, 0.56, 'hull_dark', out=0.04, t0=0.0, t1=0.995)
    H.strip(0.70, 0.84, 'hull_red', out=0.05, t0=0.02, t1=0.96)
    H.wale(0.62, 'tar', 0.22); H.wale(0.88, 'tar', 0.18); H.wale(1.0, 'hull_dark', 0.28, out=0.0)
    H.keel()
    gunports(H, [0.3 + 0.07 * i for i in range(7)], 0.77)
    # stern castle
    sx0, sx1 = -35.7, -20.0
    zc = H.deck_z(0.12)
    box(nm('sc'), (sx1 - sx0, 12.6, 6.0), loc=((sx0 + sx1) / 2, 0, zc + 3.0), key='hull')
    box(nm('sc2'), (8.8, 11.4, 3.6), loc=(sx0 + 4.4, 0, zc + 7.8), key='hull')
    for zz, ww, xx0, xx1 in ((zc + 6.0, 12.6, sx0, sx1), (zc + 9.6, 11.4, sx0, sx0 + 8.8)):
        box(nm('sct'), (xx1 - xx0 + 0.4, ww + 0.4, 0.4), loc=((xx0 + xx1) / 2, 0, zz + 0.2), key='hull_dark')
        for fr, L in ((F((xx0 + xx1) / 2, -ww / 2, zz + 0.4, 0), xx1 - xx0), (F((xx0 + xx1) / 2, ww / 2, zz + 0.4, 180), xx1 - xx0), (F(xx0, 0, zz + 0.4, -90), ww)):
            railing(fr, -L / 2 + 0.3, L / 2 - 0.3, 0, y=0.25, h=1.3, key='gold', step=0.9)
    box(nm('scb'), (0.5, 12.0, 4.0), loc=(sx1 + 0.2, 0, zc + 2.0), key='hull_dark')
    door(F(sx1 + 0.45, 0, zc, 90), 0, w=2.4, h=4.0, arch=True, key='door_paint', surround='gold', step=None, studs=False)
    for k, z in ((4, zc + 1.4), (3, zc + 6.6)):
        fr = F(sx0, 0, 0, -90)
        for i in range(k):
            x = -4.4 + 8.8 * (i + 0.5) / k
            window(fr, x, z, w=1.8, h=2.6, arch=True, frame='gold', glass='glass_lit', sill='hull_dark', lit=True, panes=True)
    box(nm('gal'), (1.6, 12.4, 0.35), loc=(sx0 - 0.7, 0, zc + 0.9), key='hull_dark')
    railing(F(sx0 - 1.45, 0, zc + 1.05, -90), -6.0, 6.0, 0, h=1.2, key='gold', step=0.7)
    for side in (-1, 1):
        fr = F(-27.8, side * 6.3, zc, 0 if side < 0 else 180)
        for x in (-5.0, 0.0, 5.0):
            window(fr, x, 1.6, w=1.5, h=2.2, arch=True, frame='gold', glass='glass_lit', sill='hull_dark', lit=True)
    for y in (-5.4, 0.0, 5.4):
        stern_lantern(sx0 + 0.4, y, zc + 10.0, s=1.0 if y else 1.3)
    ship_wheel(sx1 + 1.6, 0, zc + 2.0)
    # forecastle
    fx0, fx1 = 13.0, 23.5
    zf = H.deck_z(0.82)
    box(nm('fc'), (fx1 - fx0, 12.0, 4.0), loc=((fx0 + fx1) / 2, 0, zf + 2.0), key='hull')
    box(nm('fct'), (fx1 - fx0 + 0.4, 12.4, 0.4), loc=((fx0 + fx1) / 2, 0, zf + 4.2), key='hull_dark')
    for fr in (F((fx0 + fx1) / 2, -6.0, zf + 4.4, 0), F((fx0 + fx1) / 2, 6.0, zf + 4.4, 180), F(fx0, 0, zf + 4.4, -90)):
        railing(fr, -5.0, 5.0, 0, y=0.25, h=1.2, key='hull_dark', step=1.0)
    door(F(fx0 - 0.02, 0, zf, -90), 0, w=2.2, h=3.4, arch=False, key='door_paint', surround='hull_dark', step=None, studs=False)
    # masts and rigging
    mx_f, mx_m, mx_z = 15.0, -3.0, -27.0
    mast(mx_m, H.deck_z(0.45) - 1.0, 52.0, 0.95)
    mast(mx_f, zf + 3.0, 42.0, 0.8)
    mast(mx_z, zc + 9.5, 26.0, 0.55)
    square_rig(mx_m, 0, [(24.0, 28.0, 12.0), (38.0, 21.0, 11.0), (50.0, 14.0, 8.0)], top_at=(27.0, 2.6))
    square_rig(mx_f, 0, [(23.0, 24.0, 10.0), (35.0, 18.0, 9.5), (45.0, 12.0, 6.5)], top_at=(25.5, 2.2))
    tube_line([(mx_z - 9.0, 0, zc + 14.0), (mx_z, 0, zc + 22.0), (mx_z + 6.0, 0, zc + 28.5)], 0.25, 'wood', taper=[0.5, 1, 0.5])
    sail4((mx_z + 5.6, 0.4, zc + 28.0), (mx_z - 8.6, 0.4, zc + 14.4), (mx_z + 2.0, 0.4, zc + 11.0), (mx_z + 2.0, 0.4, zc + 11.0), (0, 1.3, 0), 'sail', belly=1.0)
    bx0 = (24.5, 0, H.zd(0.84) - 0.5); bx1 = (45.0, 0, H.zd(1.0) + 9.5)
    tube_line([bx0, bx1], 0.55, 'wood', taper=[1.0, 0.45])
    sail4((mx_f + 0.6, 0.3, 40.0), (42.5, 0.3, bx1[2] - 1.0), (27.0, 0.3, H.zd(0.9) + 3.0), (27.0, 0.3, H.zd(0.9) + 3.0), (0, 1.1, 0), 'sail', belly=1.0)
    sail4((mx_f + 0.6, 0.3, 31.0), (36.0, 0.3, bx1[2] - 3.4), (24.0, 0.3, zf + 5.6), (24.0, 0.3, zf + 5.6), (0, 0.9, 0), 'sail_b', belly=1.0)
    shrouds(H, mx_m, 27.0); shrouds(H, mx_f, 25.5)
    line((mx_m, 0, 55.0), (mx_f, 0, 30.0), 0.07, 'rope_dark')
    line((mx_f, 0, 47.0), bx1, 0.07, 'rope_dark')
    line((mx_z, 0, zc + 34.0), (mx_m, 0, 30.0), 0.06, 'rope_dark')
    pennant(mx_m, 0, 60.5, L=9.0, w=1.2)
    pennant(mx_f, 0, 50.5, L=7.0, w=1.0, key='fabric_blue')
    tube_line([(sx0 - 0.5, 0, zc + 9.8), (sx0 - 2.2, 0, zc + 17.0)], 0.12, 'wood')
    flag(sx0 - 2.2, 0, zc + 16.8, w=-5.0, h=3.4)
    # figurehead
    fp = H.pt(0.985, 0.85)
    lathe(nm('fh'), [(0, 0), (0.7, 0.2), (0.9, 1.4), (0.5, 2.6), (0, 2.8)], loc=(fp[0] + 0.8, 0, fp[2] - 2.6), key='gold', segs=10, rot=(0, -30, 0))
    ball(nm('fhh'), 0.6, loc=(fp[0] + 2.0, 0, fp[2] + 0.4), key='gold', segs=10, rings=7)
    torus(nm('fhm'), 0.6, 0.22, loc=(fp[0] + 1.85, 0, fp[2] + 0.4), key='gold', segs=12, rsegs=5, rot=(0, 90, 0))
    # deck furniture
    hatch(4.0, 0, H.deck_z(0.55), 5.0, 4.0)
    hatch(-12.0, 0, H.deck_z(0.33), 4.0, 3.0)
    capstan(-15.5, 0, H.deck_z(0.28))
    for x, y in ((7.0, 4.5), (8.4, 4.8), (7.6, -4.6)):
        barrel_at(x, y, H.deck_z(H.t_of(x)), 0.8)
    coil_at(9.0, -2.0, H.deck_z(0.62), R=1.0)
    for side in (-1, 1):
        p = H.pt(0.9, 0.9, side, 0.6)
        anchor_parts(p[0], p[1], p[2] - 6.0, s=0.75)
        p2 = H.pt(0.86, 1.0, side, 0.0)
        box(nm('cat'), (0.6, 2.4, 0.6), loc=(p2[0], p2[1] + side * 0.6, p2[2]), key='hull_dark')
    for side in (-1, 1):
        p = H.pt(0.5, 0.95, side, 0.4)
        stern_lantern(p[0], p[1], p[2] + 0.4, 0.45)
    return finalize('galleon', smooth_angle=30)


def merchant_ship():
    """G7 - two-masted merchant ship, 48 studs: broad cargo hull in blue and cream, raised aft cabin, deck cargo of crates, sacks and barrels."""
    reset()
    rnd = random.Random(7)
    H = Hull(48, 15, 7.5, bow=0.3, stern=0.78, sheer=1.4, keel_rise=0.5, flare=0.5)
    H.build('hull')
    H.deck('dock')
    H.strip(0.0, 0.56, 'hull_dark', out=0.04, t0=0.0, t1=0.995)
    H.strip(0.66, 0.82, 'hull_blue', out=0.05, t0=0.02, t1=0.96)
    H.strip(0.84, 0.92, 'hull_white', out=0.05, t0=0.03, t1=0.95)
    H.wale(0.62, 'tar', 0.2); H.wale(1.0, 'hull_dark', 0.26, out=0.0)
    H.keel()
    zc = H.deck_z(0.12)
    box(nm('ac'), (11.0, 10.4, 4.2), loc=(-17.6, 0, zc + 2.1), key='hull_white')
    gable_roof(F(-17.6, 0, 0, 0), 11.0, 10.4, zc + 4.2, 1.8, keys=('tile_red_a', 'tile_red_b'), wall='hull_white', ov=0.5, ovg=0.4)
    door(F(-12.1, 0, zc, 90), 0, w=2.2, h=3.4, arch=False, key='hull_blue', surround='hull_dark', step=None, studs=False)
    for side in (-1, 1):
        fr = F(-17.6, side * 5.2, zc, 0 if side < 0 else 180)
        for x in (-3.0, 0.0, 3.0):
            window(fr, x, 1.4, w=1.3, h=1.6, frame='hull_blue', glass='glass_lit', sill='hull_dark', lit=(x == 0))
    for x in (-2.5, 2.5):
        window(F(-23.1, 0, zc, -90), x, 1.4, w=1.4, h=1.8, arch=True, frame='hull_blue', glass='glass_lit', sill='hull_dark', lit=True)
    stern_lantern(-23.4, 0, zc + 5.4, 1.0)
    ship_wheel(-11.0, 0, zc + 1.8, R=1.0)
    # cargo
    hatch(2.0, 0, H.deck_z(0.54), 6.0, 4.6)
    for (x, y, s, rz) in ((-4.0, 3.6, 0.9, 5), (-4.0, 1.6, 0.9, -8), (-6.2, 3.2, 0.8, 20), (-4.6, 2.6, 0.75, 40)):
        crate_at(x, y, H.deck_z(H.t_of(x)) + (1.8 if s == 0.75 else 0), s, rz)
    for k in range(5):
        x, y = -6.0 + rnd.uniform(-1.4, 1.4), -3.2 + rnd.uniform(-1.4, 1.4)
        blob(nm('sk'), 0.9, (x, y, H.deck_z(H.t_of(x)) + 0.6), 'canvas', subdiv=2, amp=0.15, scale=(1.4, 1.0, 0.75), seed=70 + k)
    for x in (8.0, 9.6):
        barrel_at(x, -3.8, H.deck_z(H.t_of(x)), 0.8)
        barrel_at(x, 3.8, H.deck_z(H.t_of(x)), 0.8)
    mx_m, mx_f = -3.5, 11.5
    mast(mx_m, H.deck_z(0.43) - 1.0, 36.0, 0.75)
    mast(mx_f, H.deck_z(0.74) - 1.0, 30.0, 0.65)
    square_rig(mx_m, 0, [(18.0, 20.0, 9.0), (28.0, 14.5, 7.5)], top_at=(20.0, 1.8), sail_key='sail_b')
    square_rig(mx_f, 0, [(16.0, 17.0, 8.0), (25.0, 12.0, 6.5)], top_at=(18.0, 1.6), sail_key='sail_b')
    bx1 = (33.0, 0, H.zd(1.0) + 6.0)
    tube_line([(22.0, 0, H.zd(0.95) - 0.4), bx1], 0.4, 'wood', taper=[1.0, 0.5])
    sail4((mx_f + 0.5, 0.3, 28.0), (31.0, 0.3, bx1[2] - 0.6), (20.0, 0.3, H.zd(0.92) + 2.0), (20.0, 0.3, H.zd(0.92) + 2.0), (0, 0.9, 0), 'sail', belly=1.0)
    shrouds(H, mx_m, 20.0, side_n=4); shrouds(H, mx_f, 18.0, side_n=4)
    line((mx_m, 0, 35.0), (mx_f, 0, 22.0), 0.06, 'rope_dark')
    line((mx_f, 0, 30.0), bx1, 0.06, 'rope_dark')
    pennant(mx_m, 0, 40.0, L=6.0, w=0.9, key='fabric_green')
    tube_line([(-23.4, 0, zc + 4.0), (-25.0, 0, zc + 10.0)], 0.1, 'wood')
    flag(-25.0, 0, zc + 9.8, w=-3.4, h=2.2, key='fabric_green')
    for side in (-1, 1):
        p = H.pt(0.9, 0.9, side, 0.5)
        anchor_parts(p[0], p[1], p[2] - 4.6, s=0.55)
    return finalize('merchant_ship', smooth_angle=30)


def _fishing_boat(seed, name, L, keys, sail_key, cabin):
    reset()
    rnd = random.Random(seed)
    H = Hull(L, L * 0.34, L * 0.19, bow=0.36, stern=0.55, sheer=0.8, keel_rise=0.5, flare=0.5, ns=22, nu=7, bulwark=0.7)
    H.build('hull', thick=0.3)
    H.deck('dock_b')
    H.strip(0.0, 0.55, 'hull_dark', out=0.03, t0=0.0, t1=0.995)
    H.strip(0.62, 0.86, keys[0], out=0.04, t0=0.0, t1=0.99)
    H.strip(0.88, 1.0, keys[1], out=0.04, t0=0.0, t1=0.99)
    H.wale(0.6, 'tar', 0.12); H.wale(1.0, 'hull_dark', 0.16, out=0.0)
    H.keel(r=0.22)
    mx = H.x(0.62)
    dz = H.deck_z(0.62)
    mast(mx, dz - 0.5, L * 0.85, 0.32)
    # lateen sail on an angled yard
    top = (mx + L * 0.28, 0, dz + L * 0.88)
    low = (mx - L * 0.42, 0, dz + L * 0.18)
    tube_line([low, (mx, 0, dz + L * 0.55), top], 0.14, 'wood', taper=[0.5, 1, 0.5])
    sail4((top[0] - 0.3, 0.25, top[2] - 0.4), (low[0] + 0.3, 0.25, low[2] - 0.2), (mx + 0.2, 0.25, dz + 1.2), (mx + 0.2, 0.25, dz + 1.2), (0, 0.9, 0), sail_key, belly=1.0)
    line((mx, 0, dz + L * 0.85), H.pt(0.98, 1.0), 0.04, 'rope_dark')
    for side in (-1, 1):
        line((mx, side * 0.2, dz + L * 0.6), H.pt(0.55, 1.0, side), 0.04, 'rope_dark')
    if cabin:
        cx = H.x(0.25)
        zc = H.deck_z(0.25)
        hw = H.half_at(0.25, zc) * 0.8
        box(nm('cb'), (L * 0.2, hw * 2, 3.0), loc=(cx, 0, zc + 1.5), key='hull_white')
        lslab(F(cx, 0, 0, 0), [(-L * 0.11, -hw - 0.3, zc + 3.0), (-L * 0.11, hw + 0.3, zc + 3.0), (-L * 0.11, hw + 0.3, zc + 3.35), (-L * 0.11, -hw - 0.3, zc + 3.35)],
              (L * 0.22, 0, 0), 'roof_red')
        for side in (-1, 1):
            window(F(cx, side * hw, zc, 0 if side < 0 else 180), 0, 1.3, w=1.0, h=1.0, frame=keys[0], glass='glass_dark', sill='hull_dark')
        door(F(cx + L * 0.1, 0, zc, 90), 0, w=1.4, h=2.6, arch=False, key=keys[0], surround='hull_dark', step=None, studs=False)
        chimney(cx - 0.6, hw * 0.4, zc + 3.0, zc + 4.6, w=0.5, key='iron')
    # nets, baskets, oars, buoys
    nx = H.x(0.45); nz = H.deck_z(0.45)
    for k in range(3):
        blob(nm('nt'), 1.1, (nx + rnd.uniform(-0.8, 0.8), rnd.uniform(-0.6, 0.6), nz + 0.4), 'net', subdiv=2, amp=0.3, scale=(1.4, 1.0, 0.45), seed=seed + k)
    for k in range(4):
        ball(nm('cf'), 0.22, loc=(nx + rnd.uniform(-1.4, 1.4), rnd.uniform(-1.0, 1.0), nz + 0.85), key='fl_orange', segs=6, rings=4)
    for k in range(2):
        x = H.x(0.8) - k * 1.4
        lathe(nm('bk'), [(0, 0), (0.6, 0), (0.75, 0.9), (0.68, 0.95), (0, 0.95)], loc=(x, 0.8 - k * 1.6, H.deck_z(0.8)), key='wicker', segs=10)
        for j in range(4):
            ball(nm('fs'), 0.18, loc=(x + rnd.uniform(-0.3, 0.3), 0.8 - k * 1.6 + rnd.uniform(-0.3, 0.3), H.deck_z(0.8) + 0.95), key='fish', segs=6, rings=4, scale=(1.8, 0.6, 0.5))
    for side in (-1, 1):
        p = H.pt(0.4, 1.0, side, 0.1)
        tube_line([(p[0] - L * 0.25, p[1], p[2] + 0.2), (p[0] + L * 0.2, p[1], p[2] + 0.2)], 0.08, 'wood_light')
        box(nm('ob'), (1.2, 0.08, 0.35), loc=(p[0] + L * 0.22, p[1], p[2] + 0.2), key='wood_light')
    coil_at(H.x(0.9), 0.0, H.deck_z(0.9), R=0.6, turns=2, r=0.1)
    return finalize(name, smooth_angle=30)


def fishing_boat_1():
    """G8 - fishing boat, 18 studs: red and cream hull, lateen sail, small wheelhouse cabin, nets, floats and fish baskets."""
    return _fishing_boat(8, 'fishing_boat_1', 18.0, ('hull_red', 'hull_white'), 'sail_b', True)


def fishing_boat_2():
    """G9 - open fishing boat, 16 studs: green and white hull, rust-red lateen sail, piled nets, no cabin."""
    return _fishing_boat(9, 'fishing_boat_2', 16.0, ('hull_green', 'hull_white'), 'sail_red', False)


def rowboat():
    """G10 - rowboat, 10 studs: lapstrake hull, three thwarts, oars in rowlocks, bow ring and painter rope."""
    reset()
    H = Hull(10.0, 3.8, 1.8, bow=0.4, stern=0.6, sheer=0.45, keel_rise=0.4, flare=0.6, ns=18, nu=6, bulwark=0.3)
    H.build('hull', thick=0.18)
    H.strip(0.0, 0.5, 'hull_dark', out=0.02, t0=0.0, t1=0.995)
    for a in (0.55, 0.72, 0.88):
        H.wale(a, 'hull_dark', 0.06, out=0.02, n=12)
    H.strip(0.9, 1.0, 'hull_blue', out=0.03, t0=0.0, t1=0.99)
    H.wale(1.0, 'wood_dark', 0.09, out=0.0, n=12)
    H.keel(r=0.12)
    for t in (0.25, 0.5, 0.75):
        z = H.zd(t) - 0.55
        h = H.half_at(t, z) + 0.3
        box(nm('th'), (0.7, h * 2, 0.14), loc=(H.x(t), 0, z), key='wood_light')
    bm = H.deck_z(0.5)
    box(nm('fb'), (6.0, 1.2, 0.08), loc=(0, 0, 0.45), key='wood_light')
    for side in (-1, 1):
        p = H.pt(0.5, 1.0, side, 0.0)
        tube(nm('rl'), [(p[0] - 0.12, p[1], p[2]), (p[0] - 0.12, p[1], p[2] + 0.35)], 0.04, 'iron', res=2)
        tube(nm('rl'), [(p[0] + 0.12, p[1], p[2]), (p[0] + 0.12, p[1], p[2] + 0.35)], 0.04, 'iron', res=2)
        tube(nm('oar'), [(p[0] + 0.6, -side * 0.6, p[2] + 0.5), (p[0], p[1], p[2] + 0.25), (p[0] - 1.6, p[1] + side * 3.0, p[2] - 0.5)], 0.07, 'wood_light', res=4)
        box(nm('bl'), (0.9, 0.06, 0.4), loc=(p[0] - 1.7, p[1] + side * 3.25, p[2] - 0.55), key='wood_light', rot=(0, 0, side * 58))
    bp = H.pt(1.0, 1.0)
    torus(nm('br'), 0.16, 0.04, loc=(bp[0] + 0.1, 0, bp[2] - 0.3), key='iron', segs=10, rsegs=4, rot=(90, 0, 0))
    tube(nm('pt'), [(bp[0] + 0.1, 0, bp[2] - 0.45), (bp[0] + 0.8, 0.3, bp[2] - 0.9), (bp[0] + 1.6, 0.2, 0.3)], 0.05, 'rope', res=2)
    return finalize('rowboat', smooth_angle=30)


ITEMS_A = [
    ('G01_pier_straight', pier_straight), ('G02_pier_corner', pier_corner), ('G03_pier_end', pier_end), ('G04_pier_stairs', pier_stairs),
    ('G05_piling_cluster', piling_cluster), ('G06_galleon', galleon), ('G07_merchant_ship', merchant_ship),
    ('G08_fishing_boat_1', fishing_boat_1), ('G09_fishing_boat_2', fishing_boat_2), ('G10_rowboat', rowboat),
]



# ============================================================ G11 lighthouse
def lighthouse():
    """G11 - lighthouse, 46 studs: red and white banded tower on a rock outcrop, keeper's cottage, corbelled gallery with railing,
    glazed lamp room with a lit lamp, red cap with gold vane."""
    reset()
    rnd = random.Random(11)
    for i in range(11):
        a = 2 * math.pi * i / 11 + rnd.uniform(-0.2, 0.2)
        rr = rnd.uniform(7.0, 10.0)
        o = rock(nm('rk'), rnd.uniform(3.0, 4.6), (math.cos(a) * rr, math.sin(a) * rr, 0.8), rnd.choice(('cliff_a', 'cliff_b')), seed=110 + i, scale=(1.3, 1.0, 0.65))
        top_paint(o, 'algae', 0.2, 110 + i) if i % 3 == 0 else None
    cyl(nm('pf'), 8.6, 2.4, loc=(0, 0, 0), key='stone', verts=24, bev=0.1)
    cyl(nm('pft'), 8.9, 0.4, loc=(0, 0, 2.4), key='stone_light', verts=24)
    R0, R1, z0, z1 = 4.8, 3.2, 2.8, 34.0
    def rad(z):
        return R0 + (R1 - R0) * (z - z0) / (z1 - z0)
    n = 6
    for k in range(n):
        za, zb = z0 + (z1 - z0) * k / n, z0 + (z1 - z0) * (k + 1) / n
        lathe(nm('tw'), [(0, za), (rad(za), za), (rad(zb), zb), (0, zb)], key='lh_red' if k % 2 else 'lh_white', segs=20)
    for k, (a, z) in enumerate(((0.6, 9.0), (2.4, 15.0), (4.3, 21.0), (6.0, 27.0))):
        r = rad(z)
        box(nm('tw_w'), (0.5, 1.1, 1.8), loc=(math.cos(a) * r, math.sin(a) * r, z), key='glass_dark', rot=(0, 0, math.degrees(a)))
        box(nm('tw_s'), (0.7, 1.5, 0.25), loc=(math.cos(a) * (r + 0.1), math.sin(a) * (r + 0.1), z - 1.0), key='stone_light', rot=(0, 0, math.degrees(a)))
        box(nm('tw_l'), (0.7, 1.5, 0.3), loc=(math.cos(a) * (r + 0.1), math.sin(a) * (r + 0.1), z + 1.05), key='stone_light', rot=(0, 0, math.degrees(a)))
    door(F(0, -R0 + 0.15, 2.8, 0), 0, w=2.2, h=4.0, arch=True, key='shutter_g', surround='stone_light', step='stone', lamp=False)
    # gallery
    for i in range(16):
        a = 2 * math.pi * i / 16
        box(nm('cb'), (1.6, 0.6, 1.0), loc=(math.cos(a) * (R1 + 0.5), math.sin(a) * (R1 + 0.5), z1 - 0.5), key='stone_light', rot=(0, 0, math.degrees(a)))
    cyl(nm('gl'), 4.9, 0.6, loc=(0, 0, z1), key='stone_light', verts=24, bev=0.08)
    torus(nm('gr'), 4.7, 0.09, loc=(0, 0, z1 + 2.0), key='iron', segs=24, rsegs=4)
    torus(nm('gr2'), 4.7, 0.06, loc=(0, 0, z1 + 1.1), key='iron', segs=24, rsegs=4)
    for i in range(20):
        a = 2 * math.pi * i / 20
        tube(nm('gp'), [(math.cos(a) * 4.7, math.sin(a) * 4.7, z1 + 0.6), (math.cos(a) * 4.7, math.sin(a) * 4.7, z1 + 2.0)], 0.06, 'iron', res=2)
    # lamp room
    zl = z1 + 0.6
    cyl(nm('lrb'), 2.9, 1.2, loc=(0, 0, zl), key='lh_red', verts=8)
    lathe(nm('lrg'), [(0, zl + 1.2), (2.6, zl + 1.2), (2.6, zl + 5.0), (0, zl + 5.0)], key='glass_lit', segs=8)
    for i in range(8):
        a = 2 * math.pi * i / 8 + math.pi / 8
        tube(nm('lm'), [(math.cos(a) * 2.68, math.sin(a) * 2.68, zl + 1.2), (math.cos(a) * 2.68, math.sin(a) * 2.68, zl + 5.0)], 0.1, 'iron', res=2)
    torus(nm('lmr'), 2.68, 0.1, loc=(0, 0, zl + 3.1), key='iron', segs=8, rsegs=4)
    ball(nm('lamp'), 1.2, loc=(0, 0, zl + 3.1), key='glow', segs=12, rings=8)
    lathe(nm('cap'), [(0, zl + 5.0), (3.1, zl + 5.0), (2.9, zl + 5.4), (2.2, zl + 6.6), (1.0, zl + 7.6), (0.3, zl + 8.0), (0, zl + 8.1)], key='lh_red', segs=16)
    ball(nm('vb'), 0.4, loc=(0, 0, zl + 8.4), key='gold', segs=8, rings=6)
    tube(nm('vr'), [(0, 0, zl + 8.0), (0, 0, zl + 10.6)], 0.07, 'iron', res=2)
    poly_prism(nm('vn'), [(0, 0), (1.8, 0.3), (1.8, -0.5), (0, -0.2)], 0.05, loc=(0, 0.03, zl + 10.2), key='gold', rot=(90, 0, 0))
    for d in range(4):
        a = d * math.pi / 2
        tube(nm('vc'), [(math.cos(a) * 0.1, math.sin(a) * 0.1, zl + 9.4), (math.cos(a) * 0.8, math.sin(a) * 0.8, zl + 9.4)], 0.04, 'iron', res=2)
    # keeper's cottage
    cx, cy = 0.0, -9.6
    box(nm('kc'), (9.0, 6.0, 5.0), loc=(cx, cy, 2.8 + 2.5), key='whitewash')
    fc = faces(cx, cy, 9.0, 6.0, 2.8)
    door(fc['front'], -2.0, w=2.2, h=3.8, arch=False, key='shutter_g', surround='stone_light', step='stone')
    window(fc['front'], 2.2, 1.4, w=1.8, h=2.0, frame='wood_paint', shutter='shutter_g', sill='stone_light', lit=True, flowers=('fl_red', 'fl_white'))
    for side in ('left', 'right'):
        window(fc[side], 0, 1.4, w=1.6, h=2.0, frame='wood_paint', shutter='shutter_g', sill='stone_light')
    gable_roof(F(cx, cy, 0, 0), 9.0, 6.0, 7.8, 2.6, keys=('tile_red_a', 'tile_red_b'), wall='whitewash', ov=0.6, ovg=0.5)
    chimney(cx + 3.0, cy + 1.0, 7.8, 11.4, w=1.2, key='stone')
    return finalize('lighthouse', smooth_angle=30)


# ============================================================ G12-G13 warehouses
def boards(fr, w, z0, z1, key, step=1.3):
    n = max(1, int(w / step))
    for i in range(n + 1):
        lbox(fr, (0.2, 0.14, z1 - z0), -w / 2 + 0.15 + i * (w - 0.3) / n, -0.07, (z0 + z1) / 2, key)


def hoist(fr, z, reach=3.6, hang=6.0, load='crate'):
    lbeam(fr, (0, 0.2, z), (0, -reach, z), 0.55, 'timber')
    lbeam(fr, (0, -0.1, z - 2.2), (0, -reach * 0.7, z - 0.2), 0.35, 'timber')
    p = fr.p(0, -reach + 0.3, z - 0.55)
    torus(nm('pu'), 0.35, 0.1, loc=p, key='iron', segs=10, rsegs=4, rot=(0, 0, 0))
    tube(nm('hr'), [(p[0], p[1], p[2] - 0.3), (p[0], p[1], p[2] - hang)], 0.06, 'rope', res=2)
    lathe(nm('hk'), [(0, 0), (0.18, 0.1), (0.14, 0.5), (0, 0.6)], loc=(p[0], p[1], p[2] - hang - 0.5), key='iron', segs=6)
    if load == 'crate':
        for k in range(4):
            a = math.pi / 4 + k * math.pi / 2
            line((p[0], p[1], p[2] - hang - 0.4), (p[0] + math.cos(a) * 0.95, p[1] + math.sin(a) * 0.95, p[2] - hang - 2.0), 0.04)
        crate_at(p[0], p[1], p[2] - hang - 4.0, s=1.0)


def warehouse_1():
    """G12 - timber warehouse, 22 x 14: stone ground floor with twin arched cargo doors, boarded upper store, loading door with hoist beam
    and hanging crate, shuttered windows, roof vent, sign and dock clutter."""
    reset()
    rnd = random.Random(12)
    w, d, g, h = 22.0, 14.0, 6.0, 13.5
    box(nm('pl'), (w + 0.5, d + 0.5, 0.8), loc=(0, 0, 0.4), key='stone_dark', bev=0.05)
    box(nm('gf'), (w, d, g), loc=(0, 0, g / 2), key='stone')
    box(nm('uf'), (w, d, h - g), loc=(0, 0, (g + h) / 2), key='wood_old')
    band(0, 0, w, d, g - 0.2, 0.5, 'stone_light', out=0.2)
    fc = faces(0, 0, w, d)
    for side in ('front', 'back', 'left', 'right'):
        L = w if side in ('front', 'back') else d
        stone_face(fc[side], -L / 2, L / 2, 0.6, g - 0.6, int(L * 1.3), 120 + len(side), keys=('stone', 'stone_dark', 'stone_light'))
        quoins(fc[side], 0.8, g - 0.3, 'stone_light', course=1.05)
        boards(fc[side], L, g + 0.1, h - 0.1, 'wood_dark')
    for x in (-5.5, 5.5):
        door(fc['front'], x, w=5.0, h=5.4, arch=True, key='door_paint', surround='stone_light', step='stone_dark', lamp=False)
    wall_lantern(fc['front'], 0, 4.2)
    lbox(fc['front'], (3.6, 0.3, 4.2), 0, -0.2, g + 2.6, 'timber')
    lbox(fc['front'], (3.0, 0.32, 3.6), 0, -0.28, g + 2.6, 'shutter_b')
    lbox(fc['front'], (3.2, 0.36, 0.3), 0, -0.3, g + 2.6, 'timber', rot=(0, 48, 0))
    hoist(fc['front'], h + 0.4, reach=4.0, hang=5.0)
    for x in (-8.0, 8.0):
        window(fc['front'], x, g + 2.0, w=1.8, h=2.6, frame='wood_paint', shutter='shutter_b', sill='timber')
    for x in (-7.0, 0.0, 7.0):
        window(fc['back'], x, g + 2.0, w=1.8, h=2.6, frame='wood_paint', shutter='shutter_b', sill='timber')
    for side in ('left', 'right'):
        window(fc[side], -3.0, g + 2.0, w=1.8, h=2.6, frame='wood_paint', shutter='shutter_b', sill='timber')
        window(fc[side], 3.0, 1.6, w=1.6, h=2.4, arch=True, frame='wood_paint', sill='stone_light', keystone='stone_light')
    gable_roof(F(0, 0, 0, 0), w, d, h, d * 0.36, keys=('tile_grey', 'tile_a'), wall='wood_old', ov=1.0, ovg=0.8)
    ridge = h + d * 0.36
    box(nm('vt'), (3.0, 2.0, 1.6), loc=(-4.0, 0, ridge + 0.4), key='wood_old')
    gable_roof(F(-4.0, 0, 0, 0), 3.0, 2.0, ridge + 1.2, 0.9, keys=('tile_grey', 'tile_a'), wall='wood_old', ov=0.3, ovg=0.3)
    for k in range(4):
        box(nm('vl'), (2.8, 0.12, 0.2), loc=(-4.0, -1.02, ridge - 0.1 + k * 0.35), key='timber', rot=(30, 0, 0))
    hanging_sign(fc['front'], -9.6, g - 1.0, board='shutter_b', emblem='gold')
    crate_at(-9.0, -d / 2 - 2.4, 0.0, 0.9, 10)
    crate_at(-7.0, -d / 2 - 2.0, 0.0, 0.9, -6)
    crate_at(-8.0, -d / 2 - 2.2, 1.8, 0.8, 30)
    for x in (8.0, 9.6, 8.8):
        barrel_at(x, -d / 2 - 1.6 - (0.0 if x != 8.8 else 1.4), 0.0)
    for k in range(4):
        blob(nm('sk'), 0.8, (3.4 + rnd.uniform(-1.0, 1.0), -d / 2 - 1.8 + rnd.uniform(-0.6, 0.6), 0.55), 'canvas', subdiv=2, amp=0.15, scale=(1.4, 1.0, 0.7), seed=120 + k)
    return finalize('warehouse_1', smooth_angle=30)


def warehouse_2():
    """G13 - brick bonded warehouse, 26 x 16: four arched loading bays, arched upper windows, end gable to the quay with a wall crane wheel,
    stone dressings, roof dormer and stacked sacks."""
    reset()
    rnd = random.Random(13)
    w, d, h = 26.0, 16.0, 14.0
    box(nm('pl'), (w + 0.5, d + 0.5, 0.8), loc=(0, 0, 0.4), key='stone_dark', bev=0.05)
    box(nm('bd'), (w, d, h), loc=(0, 0, h / 2), key='brick')
    for z in (0.8, 7.0, h - 0.4):
        band(0, 0, w, d, z, 0.5, 'stone_light', out=0.2)
    fc = faces(0, 0, w, d)
    for side in fc:
        quoins(fc[side], 0.8, h - 0.4, 'stone_light', course=1.1)
    xs = [-w / 2 + w * (i + 0.5) / 4 for i in range(4)]
    for i, x in enumerate(xs):
        if i in (1, 2):
            door(fc['front'], x, w=4.4, h=5.8, arch=True, key='shutter_g', surround='stone_light', step='stone_dark')
        else:
            lbox(fc['front'], (4.4, 0.3, 3.6), x, -0.05, 2.8, 'hole')
            door(fc['front'], x, w=4.4, h=5.8, arch=True, key='hole', surround='stone_light', step='stone_dark', studs=False)
        window(fc['front'], x, 8.0, w=2.4, h=3.6, arch=True, frame='wood_paint', sill='stone_light', keystone='stone_light')
        window(fc['back'], x, 8.0, w=2.4, h=3.6, arch=True, frame='wood_paint', sill='stone_light', keystone='stone_light')
        window(fc['back'], x, 2.0, w=2.2, h=3.0, arch=True, frame='wood_paint', sill='stone_light', keystone='stone_light')
    hr = w * 0.0 + d * 0.42
    gable_roof(F(0, 0, 0, 0), w, d, h, hr, keys=('tile_red_a', 'tile_red_b'), wall='brick', ov=1.0, ovg=0.8)
    for side in ('left', 'right'):
        fr = faces(0, 0, w, d, h)[side]
        window(fr, 0, 1.4, w=2.0, h=3.0, arch=True, frame='wood_paint', sill='stone_light')
        window(fc[side], -4.0, 8.0, w=2.2, h=3.4, arch=True, frame='wood_paint', sill='stone_light', keystone='stone_light')
        window(fc[side], 4.0, 8.0, w=2.2, h=3.4, arch=True, frame='wood_paint', sill='stone_light', keystone='stone_light')
    door(fc['right'], 0, w=4.0, h=6.0, arch=True, key='door_paint', surround='stone_light', step='stone_dark', lamp=True)
    # wall crane on the quay end
    fr = fc['left']
    lbox(fr, (1.2, 1.2, 6.0), 0, -0.6, 10.0, 'timber')
    lbeam(fr, (0, -0.6, 12.8), (0, -5.6, 12.8), 0.6, 'timber')
    lbeam(fr, (0, -0.6, 8.0), (0, -4.6, 12.4), 0.45, 'timber')
    wp = fr.p(0, -1.6, 9.6)
    torus(nm('wh'), 1.4, 0.12, loc=wp, key='wood_dark', segs=16, rsegs=4, rot=(0, 90, 0))
    for k in range(6):
        a = math.pi * k / 3
        tube(nm('ws'), [wp, (wp[0], wp[1] + math.cos(a) * 1.4, wp[2] + math.sin(a) * 1.4)], 0.07, 'wood_dark', res=2)
    tip = fr.p(0, -5.3, 12.4)
    tube(nm('cr'), [tip, (tip[0], tip[1], 4.0)], 0.06, 'rope', res=2)
    lathe(nm('hk'), [(0, 0), (0.18, 0.1), (0.14, 0.5), (0, 0.6)], loc=(tip[0], tip[1], 3.4), key='iron', segs=6)
    blob(nm('nb'), 1.1, (tip[0], tip[1], 2.2), 'net', subdiv=2, amp=0.2, scale=(1.0, 1.0, 1.1), seed=131)
    for k in range(9):
        x = -6.0 + (k % 3) * 1.8 + rnd.uniform(-0.2, 0.2)
        y = -d / 2 - 1.6 - (k // 3 % 2) * 1.6
        z = 0.5 + (k // 6) * 1.0
        blob(nm('sk'), 0.8, (x, y, z), 'canvas' if k % 2 else 'canvas_b', subdiv=2, amp=0.14, scale=(1.4, 0.95, 0.65), seed=133 + k)
    crate_at(7.0, -d / 2 - 2.0, 0.0, 1.0, 8)
    barrel_at(9.4, -d / 2 - 1.6, 0.0)
    return finalize('warehouse_2', smooth_angle=30)


# ============================================================ G14 harbour master
def harbour_master():
    """G14 - harbour master's office: whitewashed stone house with blue shutters, lookout cupola with clock and lit windows,
    flag mast, bell bracket, notice board and tide marker post."""
    reset()
    top = house(cx=0.0, w=13.0, d=11.0, floors=2, gh=7.0, fh=6.5, ground='ashlar', ground_trim='stone_light', upper='whitewash', timber=False,
                jetty=0.0, roof='side', rkeys=('tile_a', 'tile_b'), shutter='shutter_b', flowers=('fl_blue', 'fl_white'), dormers=0, seed=14,
                sign='shutter_b', lit=((0, 1),))
    hr = 11.0 * 0.42
    cz = top + hr - 1.6
    box(nm('cu'), (3.4, 3.4, 4.0), loc=(0, 0, cz + 2.0), key='whitewash')
    cf = faces(0, 0, 3.4, 3.4, cz)
    for s in cf:
        window(cf[s], 0, 1.8, w=1.6, h=1.8, arch=True, frame='wood_paint', glass='glass_lit', sill='stone_light', lit=True)
    box(nm('cuc'), (3.8, 3.8, 0.35), loc=(0, 0, cz + 4.1), key='stone_light')
    cone_roof(0, 0, cz + 4.3, 2.6, 3.2, keys=('patina', 'patina'), rings=4, ov=0.3, finial='gold', segs=8)
    lathe(nm('ck'), [(0, 0), (1.1, 0), (1.1, 0.12), (0, 0.12)], loc=(0, -1.75, cz + 0.9), key='castle_trim', segs=16, rot=(90, 0, 0))
    lathe(nm('ckf'), [(0, 0), (0.95, 0), (0.95, 0.06), (0, 0.06)], loc=(0, -1.85, cz + 0.9), key='paper', segs=16, rot=(90, 0, 0))
    tube(nm('ch'), [(0, -1.95, cz + 0.9), (0, -1.95, cz + 1.6)], 0.06, 'iron', res=2)
    tube(nm('cm'), [(0, -1.95, cz + 0.9), (0.45, -1.95, cz + 0.7)], 0.06, 'iron', res=2)
    # flag mast with yard and pennants
    fx, fy = 9.0, -3.0
    cyl(nm('fb'), 1.2, 1.0, loc=(fx, fy, 0), key='stone', verts=10)
    tube(nm('fm'), [(fx, fy, 1.0), (fx, fy, 22.0)], 0.3, 'wood_paint', res=4, taper=[1.0, 0.5])
    tube(nm('fy'), [(fx, fy - 3.0, 17.0), (fx, fy + 3.0, 17.0)], 0.12, 'wood_paint', res=2)
    for s in (-1, 1):
        line((fx, fy + s * 3.0, 17.0), (fx, fy + s * 0.6, 1.2), 0.03)
    flag(fx + 0.1, fy, 21.6, w=4.2, h=2.6, key='fabric_blue')
    for k, key in enumerate(('fabric_red', 'fl_yellow', 'fabric_green')):
        poly_prism(nm('sg'), [(0, 0), (1.2, 0), (0.6, -1.4)], 0.06, loc=(fx + 0.05, fy - 2.6 + k * 0.05, 16.6 - k * 1.8), key=key, rot=(90, 0, 90))
    # bell bracket by the door
    fr = faces(0, 0, 13.0, 11.0)['front']
    lbeam(fr, (4.6, -0.1, 5.6), (4.6, -1.6, 5.6), 0.2, 'iron')
    bp = fr.p(4.6, -1.5, 5.4)
    lathe(nm('bl'), [(0, 0), (0.55, 0), (0.5, 0.15), (0.38, 0.7), (0.3, 1.0), (0.12, 1.1), (0, 1.1)], loc=(bp[0], bp[1], bp[2] - 1.1), key='brass', segs=12)
    tube(nm('bc'), [(bp[0], bp[1], bp[2] - 0.9), (bp[0], bp[1], bp[2] - 2.4)], 0.04, 'rope', res=2)
    # notice board
    nb = fr.p(-4.4, -0.2, 0)
    box(nm('nbb'), (3.0, 0.2, 2.2), loc=(nb[0], nb[1], 3.4), key='wood_dark')
    for k in range(4):
        box(nm('np'), (0.7, 0.05, 0.9), loc=(nb[0] - 1.0 + k * 0.65, nb[1] - 0.12, 3.4 + (0.3 if k % 2 else -0.2)), key='paper', rot=(0, (k - 1.5) * 6, 0))
    # tide post
    tx = -9.0
    cyl(nm('tp'), 0.3, 9.0, loc=(tx, -4.0, 0), key='wood_paint', verts=8)
    for k in range(8):
        box(nm('tm'), (0.66, 0.06, 0.12), loc=(tx, -4.32, 1.0 + k * 1.0), key='tar' if k % 2 else 'fabric_red')
    return finalize('harbour_master', smooth_angle=30)


# ============================================================ G15 fish stall
def fish_at(x, y, z, s=1.0, rz=0.0, key='fish'):
    o = ball(nm('fs'), 0.5 * s, loc=(x, y, z), key=key, segs=10, rings=6, scale=(1.9, 0.62, 0.4))
    o.rotation_euler.z = math.radians(rz)
    a = math.radians(rz); c, sn = math.cos(a), math.sin(a)
    poly_prism(nm('ft'), [(0, 0), (-0.65 * s, 0.42 * s), (-0.55 * s, 0), (-0.65 * s, -0.42 * s)], 0.07 * s, loc=(x - c * 0.85 * s, y - sn * 0.85 * s, z - 0.035 * s), key=key, rot=(0, 0, rz))
    ball(nm('fe'), 0.07 * s, loc=(x + c * 0.65 * s - sn * 0.12 * s, y + sn * 0.65 * s + c * 0.12 * s, z + 0.1 * s), key='tar', segs=6, rings=4)


def fish_market_stall():
    """G15 - fish market stall: plank counter with a sloped bed of ice, fish and a crab, striped blue canopy, hanging scale and fish string,
    chalk board, crates and a bucket."""
    reset()
    rnd = random.Random(15)
    W, D, Hc = 8.0, 3.2, 3.0
    box(nm('ct'), (W, D, Hc), loc=(0, 0, Hc / 2), key='wood')
    fr = F(0, -D / 2, 0, 0)
    boards(fr, W, 0.2, Hc - 0.2, 'wood_dark', step=1.0)
    box(nm('ctp'), (W + 0.3, D + 0.3, 0.25), loc=(0, 0, Hc + 0.12), key='wood_dark')
    box(nm('ice'), (W - 0.6, D - 0.4, 0.4), loc=(0, 0.1, Hc + 0.45), key='ice', rot=(-12, 0, 0))
    for k in range(13):
        x = -W / 2 + 0.9 + (k % 7) * (W - 1.8) / 6 + rnd.uniform(-0.15, 0.15)
        y = -0.6 if k < 7 else 0.6
        z = Hc + 0.72 + (0.0 if y < 0 else 0.25)
        fish_at(x, y, z, s=rnd.uniform(0.7, 1.0), rz=rnd.uniform(70, 110) + (180 if k % 2 else 0), key='fish' if k % 3 else 'fish_b')
    ball(nm('crb'), 0.55, loc=(W / 2 - 1.0, 0.3, Hc + 0.9), key='fish_b', segs=10, rings=6, scale=(1.2, 1, 0.45))
    for s in (-1, 1):
        for k in range(3):
            tube(nm('cl'), [(W / 2 - 1.0 + s * 0.4, 0.3 - 0.3 + k * 0.3, Hc + 0.85), (W / 2 - 1.0 + s * 0.9, 0.3 - 0.4 + k * 0.4, Hc + 0.75)], 0.05, 'fish_b', res=2)
        ball(nm('cw'), 0.2, loc=(W / 2 - 1.0 + s * 0.55, -0.35, Hc + 0.95), key='fish_b', segs=6, rings=4, scale=(1.4, 1, 0.7))
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl(nm('po'), 0.16, 7.2 if sy > 0 else 6.2, loc=(sx * (W / 2 - 0.1), sy * (D / 2 + 0.2), 0), key='wood_dark', verts=8)
    n = 8
    for k in range(n):
        x0 = -W / 2 - 0.3 + (W + 0.6) * k / n
        lslab(F(0, 0, 0, 0), [(x0, -D / 2 - 1.4, 6.0), (x0, D / 2 + 0.4, 7.4), (x0, D / 2 + 0.4, 7.55), (x0, -D / 2 - 1.4, 6.15)], ((W + 0.6) / n, 0, 0),
              'fabric_blue' if k % 2 else 'fabric_cream')
    for k in range(n):
        x0 = -W / 2 - 0.3 + (W + 0.6) * (k + 0.5) / n
        poly_prism(nm('vl'), [(-(W + 0.6) / n / 2, 0), ((W + 0.6) / n / 2, 0), (0, -0.7)], 0.05, loc=(x0, -D / 2 - 1.42, 6.05), key='fabric_blue' if k % 2 else 'fabric_cream', rot=(90, 0, 0))
    # hanging scale
    tube(nm('sch'), [(-2.2, -D / 2 - 0.6, 6.3), (-2.2, -D / 2 - 0.6, 5.2)], 0.04, 'iron', res=2)
    lathe(nm('scb'), [(0, 0), (0.25, 0), (0.25, 0.6), (0, 0.6)], loc=(-2.2, -D / 2 - 0.6, 4.6), key='brass', segs=10)
    for k in range(3):
        a = 2 * math.pi * k / 3
        line((-2.2, -D / 2 - 0.6, 4.6), (-2.2 + math.cos(a) * 0.6, -D / 2 - 0.6 + math.sin(a) * 0.6, 3.9), 0.025, 'iron')
    lathe(nm('scp'), [(0, 0.1), (0.65, 0.18), (0.68, 0.24), (0, 0.16)], loc=(-2.2, -D / 2 - 0.6, 3.75), key='brass', segs=12)
    # string of hanging fish
    line((1.0, -D / 2 - 0.9, 5.9), (3.6, -D / 2 - 0.9, 5.9), 0.03)
    for k in range(4):
        x = 1.3 + k * 0.7
        line((x, -D / 2 - 0.9, 5.9), (x, -D / 2 - 0.9, 5.4), 0.02)
        o = ball(nm('hf'), 0.32, loc=(x, -D / 2 - 0.9, 4.9), key='fish', segs=8, rings=6, scale=(0.4, 0.3, 1.6))
        poly_prism(nm('hft'), [(-0.3, 0), (0.3, 0), (0, 0.4)], 0.05, loc=(x, -D / 2 - 0.88, 4.2), key='fish', rot=(90, 180, 0))
    # chalk board, crates, bucket
    box(nm('cb'), (1.6, 0.12, 1.2), loc=(-W / 2 - 1.2, -D / 2 - 0.4, 1.5), key='tar', rot=(-12, 0, 0))
    box(nm('cbf'), (1.75, 0.1, 1.35), loc=(-W / 2 - 1.2, -D / 2 - 0.34, 1.5), key='wood_light', rot=(-12, 0, 0))
    for k in range(2):
        tube(nm('cbl'), [(-W / 2 - 1.9 + k * 1.4, -D / 2 - 0.2, 0), (-W / 2 - 1.9 + k * 1.4, -D / 2 - 0.5, 2.1)], 0.06, 'wood_light', res=2)
    for i, (x, y) in enumerate(((W / 2 + 1.4, -0.8), (W / 2 + 1.4, 1.2))):
        box(nm('fcr'), (1.8, 1.4, 1.0), loc=(x, y, 0.5), key='wood_light')
        for k in range(4):
            fish_at(x - 0.5 + (k % 2) * 0.9, y - 0.3 + (k // 2) * 0.6, 1.05, s=0.55, rz=rnd.uniform(-20, 20))
    lathe(nm('bk'), [(0, 0), (0.55, 0), (0.65, 1.1), (0.6, 1.1), (0, 0.15)], loc=(-W / 2 + 0.4, -D / 2 - 1.2, 0), key='wood', segs=12)
    return finalize('fish_market_stall', smooth_angle=30)


# ============================================================ G16 crane
def cargo_crane():
    """G16 - wooden treadwheel cargo crane: stone pad, braced mast, angled jib with pulley, rope to an iron hook carrying a net bundle,
    walk-in treadwheel with spokes and rungs."""
    reset()
    cyl(nm('pad'), 5.0, 1.4, loc=(0, 0, 0), key='stone', verts=16, bev=0.1)
    tube(nm('mst'), [(0, 0, 1.4), (0, 0, 17.0)], 0.75, 'timber', res=4, taper=[1.0, 0.8])
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        beam3((math.cos(a) * 3.6, math.sin(a) * 3.6, 1.4), (math.cos(a) * 0.5, math.sin(a) * 0.5, 7.0), 0.4, 0.5, 'timber')
    beam3((0, 0, 15.5), (11.0, 0, 21.0), 0.6, 0.7, 'timber')
    beam3((0, 0, 8.5), (7.6, 0, 19.3), 0.45, 0.5, 'timber')
    beam3((0, 0, 17.0), (11.0, 0, 21.0), 0.25, 0.25, 'iron')
    for zz in (8.5, 15.5):
        torus(nm('band'), 0.82, 0.1, loc=(0, 0, zz), key='iron', segs=12, rsegs=4)
    torus(nm('pu'), 0.6, 0.15, loc=(10.8, 0, 20.4), key='iron', segs=12, rsegs=4, rot=(90, 0, 0))
    tube(nm('rp'), [(10.8, 0, 19.8), (10.8, 0, 8.0)], 0.07, 'rope', res=2)
    lathe(nm('hk'), [(0, 0), (0.28, 0.15), (0.22, 0.8), (0, 0.95)], loc=(10.8, 0, 7.1), key='iron', segs=8)
    tube(nm('hkc'), [(10.8, 0, 7.15), (11.3, 0, 6.8), (11.2, 0, 7.4)], 0.09, 'iron', res=2)
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        line((10.8, 0, 7.0), (10.8 + math.cos(a) * 1.3, math.sin(a) * 1.3, 4.8), 0.04)
    blob(nm('nb'), 1.6, (10.8, 0, 3.6), 'net', subdiv=2, amp=0.2, scale=(1.0, 1.0, 1.0), seed=161)
    for k in range(3):
        crate_at(10.4 + k * 0.4 - 0.4, -0.3 + k * 0.3, 2.3 + k * 0.3, 0.4, k * 25)
    # treadwheel
    wx, wz, R = -5.5, 5.4, 4.0
    for y in (-1.6, 1.6):
        torus(nm('tw'), R, 0.18, loc=(wx, y, wz), key='wood_dark', segs=28, rsegs=4, rot=(90, 0, 0))
        for k in range(8):
            a = 2 * math.pi * k / 8
            tube(nm('sp'), [(wx, y, wz), (wx + math.cos(a) * R, y, wz + math.sin(a) * R)], 0.12, 'wood_dark', res=2)
        beam3((wx - 2.6, y * 1.25, 0.0), (wx, y * 1.25, wz), 0.35, 0.4, 'timber')
        beam3((wx + 2.6, y * 1.25, 0.0), (wx, y * 1.25, wz), 0.35, 0.4, 'timber')
    for k in range(18):
        a = 2 * math.pi * k / 18
        box(nm('rg'), (0.5, 3.4, 0.16), loc=(wx + math.cos(a) * R, 0, wz + math.sin(a) * R), key='wood', rot=(0, -math.degrees(a), 0))
    tube(nm('ax'), [(wx, -2.3, wz), (wx, 2.3, wz)], 0.25, 'iron', res=4)
    tube(nm('dr'), [(wx, 0.3, wz), (-0.6, 0.3, 16.0), (10.4, 0.2, 20.6)], 0.07, 'rope', res=2)
    return finalize('cargo_crane', smooth_angle=30)


# ============================================================ G17-G22 dock props
def net_rack():
    """G17 - net drying rack: three posts with cross rails, two sagging fishing nets with cork floats, a stool, basket and rope coil."""
    reset()
    rnd = random.Random(17)
    for x in (-7.0, 0.0, 7.0):
        for y in (-0.4, 0.4):
            tube(nm('po'), [(x, y, 0), (x + rnd.uniform(-0.1, 0.1), y, 7.0)], 0.2, 'wood_grey', res=4)
        box(nm('ct'), (0.4, 1.4, 0.3), loc=(x, 0, 7.0), key='wood_grey')
    tube(nm('tr'), [(-7.2, 0, 7.1), (7.2, 0, 7.1)], 0.13, 'wood_grey', res=4)
    tube(nm('mr'), [(-7.2, 0, 3.6), (7.2, 0, 3.6)], 0.1, 'wood_grey', res=4)
    for x0, x1 in ((-6.8, -0.2), (0.2, 6.8)):
        n = 9
        for k in range(n + 1):
            x = x0 + (x1 - x0) * k / n
            mid = math.sin(math.pi * k / n)
            tube(nm('nv'), [(x, 0.05, 7.0), (x, 0.25 + 0.35 * mid, 4.2), (x, 0.15 + 0.3 * mid, 1.6 + 0.6 * mid)], 0.03, 'net', res=2, ures=3)
        for j in range(6):
            z = 6.8 - j * 0.95
            pts = []
            for k in range(n + 1):
                mid = math.sin(math.pi * k / n)
                zz = z - mid * (0.25 + j * 0.12)
                pts.append((x0 + (x1 - x0) * k / n, 0.1 + 0.3 * mid, max(zz, 1.6 + 0.6 * mid)))
            tube(nm('nh'), pts, 0.03, 'net', res=2, ures=1)
        for k in range(7):
            ball(nm('cf'), 0.2, loc=(x0 + (x1 - x0) * (k + 0.5) / 7, 0.0, 6.85), key='fl_orange' if k % 2 else 'wood_light', segs=6, rings=4, scale=(1, 1, 1.3))
    lathe(nm('st'), [(0, 1.5), (0.7, 1.5), (0.7, 1.75), (0, 1.75)], loc=(-3.0, -2.0, 0), key='wood', segs=10)
    for k in range(3):
        a = 2 * math.pi * k / 3
        tube(nm('sl'), [(-3.0 + math.cos(a) * 0.5, -2.0 + math.sin(a) * 0.5, 1.5), (-3.0 + math.cos(a) * 0.7, -2.0 + math.sin(a) * 0.7, 0)], 0.07, 'wood', res=2)
    lathe(nm('bk'), [(0, 0), (0.7, 0), (0.85, 1.0), (0.78, 1.05), (0, 0.1)], loc=(2.6, -1.8, 0), key='wicker', segs=12)
    coil_at(5.0, -2.0, 0.0, R=1.0)
    return finalize('net_rack', smooth_angle=30)


def rope_coil():
    """G18 - big coil of mooring rope: stacked helix with a flemish spiral on top and a loose end trailing over the ground."""
    reset()
    end = coil_at(0, 0, 0, R=1.7, turns=4, flat=False, r=0.22)
    end2 = coil_at(0, 0, end[2] - 0.05, R=1.6, turns=3, flat=True, r=0.2)
    tube(nm('le'), [end2, (2.2, 0.4, end2[2] - 0.6), (3.4, 1.4, 0.25), (5.2, 1.0, 0.22), (6.4, 2.0, 0.22)], 0.2, 'rope', res=4, ures=3)
    torus(nm('wh'), 0.22, 0.08, loc=(6.4, 2.0, 0.24), key='rope_dark', segs=8, rsegs=4)
    return finalize('rope_coil', smooth_angle=30)


def anchor():
    """G19 - ship's anchor display, 7 studs tall: iron shank and curved arms with spade flukes, banded wooden stock, ring and draped chain,
    propped on oak chocks."""
    reset()
    anchor_parts(0, 0, 0.4, s=1.0)
    for x in (-1.6, 1.6):
        box(nm('ch'), (1.2, 1.4, 0.8), loc=(x, 0, 0.4), key='wood_dark', bev=0.06)
    chain(nm('chn'), (0, 0, 8.0), (2.2, 0.6, 0.3), link=0.4, thick=0.08)
    for k in range(10):
        a = k * 0.8
        torus(nm('cp'), 0.24, 0.08, loc=(2.6 + math.cos(a) * 0.6, 0.8 + math.sin(a) * 0.6, 0.15 + (k // 5) * 0.12), key='iron', segs=8, rsegs=4,
              rot=(0, 0, math.degrees(a)))
    return finalize('anchor', smooth_angle=30)


def buoy():
    """G20 - channel buoy: red and white float with algae waterline, iron cage holding a brass bell and a glowing lamp, mooring chain."""
    reset()
    lathe(nm('bb'), [(0, 0), (1.5, 0.2), (2.0, 1.2), (2.0, 2.6), (1.4, 3.2), (0, 3.3)], key='lh_red', segs=16)
    lathe(nm('bw'), [(0, 1.7), (2.04, 1.7), (2.04, 2.4), (0, 2.4)], key='lh_white', segs=16)
    lathe(nm('ba'), [(0, 0.4), (1.86, 0.6), (2.05, 1.1), (0, 1.1)], key='algae', segs=16)
    torus(nm('fr'), 2.05, 0.14, loc=(0, 0, 2.6), key='rope_dark', segs=16, rsegs=4)
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        tube(nm('cg'), [(math.cos(a) * 1.1, math.sin(a) * 1.1, 3.1), (math.cos(a) * 0.5, math.sin(a) * 0.5, 6.4)], 0.09, 'iron', res=2)
    torus(nm('cr'), 0.8, 0.07, loc=(0, 0, 4.8), key='iron', segs=12, rsegs=4)
    lathe(nm('bl'), [(0, 3.7), (0.45, 3.7), (0.4, 3.85), (0.3, 4.3), (0.12, 4.55), (0, 4.55)], key='brass', segs=12)
    ball(nm('blc'), 0.1, loc=(0, 0, 3.7), key='iron', segs=6, rings=4)
    cyl(nm('lb'), 0.6, 0.2, loc=(0, 0, 6.4), key='iron', verts=10)
    lathe(nm('lg'), [(0, 6.6), (0.4, 6.6), (0.45, 7.2), (0.35, 7.6), (0, 7.6)], key='glow', segs=8)
    lathe(nm('lc'), [(0.5, 7.6), (0.2, 8.0), (0, 8.1)], key='iron', segs=8)
    chain(nm('ch'), (0, 0, 0.1), (0.5, 0.0, -2.5), link=0.4, thick=0.08)
    return finalize('buoy', smooth_angle=30)


def lobster_trap():
    """G21 - lobster trap: plank base, bent hoops, slats, net ends, stone ballast, rope and a painted cork marker float."""
    reset()
    L, R = 3.4, 1.0
    box(nm('bs'), (L, 2.0, 0.15), loc=(0, 0, 0.075), key='wood_grey')
    for k in range(5):
        x = -L / 2 + 0.1 + (L - 0.2) * k / 4
        tube(nm('hp'), [(x, -R * math.cos(math.radians(a)), 0.15 + R * math.sin(math.radians(a))) for a in range(0, 181, 30)], 0.05, 'wood_old', res=2, ures=2)
    for k in range(7):
        a = math.pi * (k + 0.5) / 7
        y, z = -R * math.cos(a), 0.15 + R * math.sin(a)
        box(nm('sl'), (L, 0.18, 0.06), loc=(0, y, z), key='wood_grey', rot=(math.degrees(a) - 90, 0, 0))
    for x in (-L / 2 + 0.1, L / 2 - 0.1):
        for k in range(5):
            a = math.pi * (k + 1) / 6
            line((x, 0, 0.15), (x, -R * math.cos(a), 0.15 + R * math.sin(a)), 0.02, 'net')
        torus(nm('fn'), 0.25, 0.04, loc=(x, 0, 0.6), key='net', segs=8, rsegs=3, rot=(0, 90, 0))
    for k in range(2):
        rock(nm('bal'), 0.3, (-0.6 + k * 1.2, 0.3, 0.3), 'stone_dark', seed=210 + k, scale=(1.2, 1.0, 0.6), subdiv=1)
    tube(nm('rp'), [(L / 2, 0, 0.5), (L / 2 + 0.8, 0.4, 0.15), (L / 2 + 2.0, 0.6, 0.2), (L / 2 + 2.6, 1.6, 0.25)], 0.05, 'rope', res=2)
    lathe(nm('fl'), [(0, 0), (0.3, 0.05), (0.35, 0.4), (0.3, 0.75), (0, 0.8)], loc=(L / 2 + 2.9, 1.9, 0.0), key='fl_yellow', segs=10, rot=(0, 80, 20))
    lathe(nm('fl2'), [(0.36, 0.3), (0.36, 0.5), (0, 0.5), (0, 0.3)], loc=(L / 2 + 2.9, 1.9, 0.0), key='fabric_red', segs=10, rot=(0, 80, 20))
    return finalize('lobster_trap', smooth_angle=30)


def cannon_at(x, y, z, s=1.0, d=-1):
    wr = 0.7 * s
    for sx in (-1, 1):
        box(nm('ck'), (0.35 * s, 3.6 * s, 1.2 * s), loc=(x + sx * 0.75 * s, y, z + wr + 0.3 * s), key='wood', bev=0.04)
        box(nm('ck2'), (0.35 * s, 1.6 * s, 0.9 * s), loc=(x + sx * 0.75 * s, y - d * 1.0 * s, z + wr + 1.3 * s), key='wood', bev=0.04)
        for yy in (-1.2, 1.2):
            cyl(nm('wh'), wr, 0.3 * s, loc=(x + (0.95 if sx > 0 else -1.25) * s, y + yy * s, z + wr), key='wood_dark', verts=12, rot=(0, 90, 0))
            cyl(nm('whh'), 0.18 * s, 0.38 * s, loc=(x + (0.93 if sx > 0 else -1.31) * s, y + yy * s, z + wr), key='iron', verts=8, rot=(0, 90, 0))
    box(nm('bd'), (1.5 * s, 3.6 * s, 0.3 * s), loc=(x, y, z + wr), key='wood_dark')
    for yy in (-1.2, 1.2):
        tube(nm('ax'), [(x - 1.2 * s, y + yy * s, z + wr), (x + 1.2 * s, y + yy * s, z + wr)], 0.12 * s, 'iron', res=2)
    prof = [(0, 0), (0.36, 0), (0.5, 0.15), (0.62, 0.5), (0.6, 1.4), (0.68, 1.5), (0.56, 1.62), (0.5, 3.4), (0.58, 3.5), (0.44, 4.6), (0.54, 4.72), (0.54, 4.95),
            (0.3, 5.0), (0, 5.0)]
    bz = z + wr + 1.25 * s
    by = y - d * 1.9 * s
    lathe(nm('br'), [(r * s, zz * s) for r, zz in prof], loc=(x, by, bz), key='iron', segs=12, rot=(90 if d < 0 else -90, 0, 0))
    cyl(nm('bo'), 0.28 * s, 0.06 * s, loc=(x, by + d * 5.0 * s, bz), key='tar', verts=10, rot=(90 if d < 0 else -90, 0, 0))
    ball(nm('cs'), 0.25 * s, loc=(x, by - d * 0.25 * s, bz), key='iron', segs=8, rings=6)
    tube(nm('tn'), [(x - 0.95 * s, y - d * 0.2 * s, bz), (x + 0.95 * s, y - d * 0.2 * s, bz)], 0.16 * s, 'iron', res=4)


def ball_pyramid(x, y, z, r=0.32, n=3):
    for lvl in range(n):
        m = n - lvl
        for i in range(m):
            for j in range(m):
                ball(nm('cb'), r, loc=(x + (i - (m - 1) / 2) * 2 * r, y + (j - (m - 1) / 2) * 2 * r, z + r + lvl * r * 1.42), key='iron', segs=8, rings=6)


def cannon():
    """G22 - harbour cannon on a wooden truck carriage: cast barrel with reinforcing rings and cascabel, four iron-hubbed wheels,
    cannonball pyramid, rammer and powder keg."""
    reset()
    cannon_at(0, 0, 0, s=1.0, d=-1)
    ball_pyramid(2.6, 1.0, 0.0)
    tube(nm('rm'), [(-2.0, 2.4, 0.15), (-1.6, -2.6, 0.15)], 0.07, 'wood_light', res=2)
    cyl(nm('rmh'), 0.22, 0.6, loc=(-1.6, -2.6, 0.15), key='rope_dark', verts=8, rot=(90, 0, 0))
    barrel_at(2.6, -1.6, 0.0, s=0.7, key='wood_dark')
    return finalize('cannon', smooth_angle=30)


# ============================================================ G23 fort
def harbour_fort():
    """G23 - small harbour fort, 36 x 30: battered stone curtain walls with battlements, three corner turrets and a tall flag tower,
    seaward cannon battery on the wall walk, arched landward gate, inner stair, powder store and shot piles."""
    reset()
    rnd = random.Random(23)
    W, D, Hw, B = 36.0, 30.0, 9.0, 2.0
    box(nm('ap'), (W + 5, D + 5, B), loc=(0, 0, B / 2), key='stone_dark', bev=0.1)
    box(nm('apa'), (W + 5.2, D + 5.2, 1.0), loc=(0, 0, 0.5), key='algae')
    T = 4.0
    for (cx, cy, w, d) in ((0, -D / 2 + T / 2, W, T), (0, D / 2 - T / 2, W, T), (-W / 2 + T / 2, 0, T, D - 2 * T), (W / 2 - T / 2, 0, T, D - 2 * T)):
        box(nm('wl'), (w, d, Hw), loc=(cx, cy, B + Hw / 2), key='stone')
    box(nm('yd'), (W - 2 * T, D - 2 * T, 0.4), loc=(0, 0, B + 0.2), key='cob_a')
    fo = faces(0, 0, W, D, B)
    ft = faces(0, 0, W, D, B + Hw)
    for side in fo:
        L = W if side in ('front', 'back') else D
        stone_face(fo[side], -L / 2 + 4.5, L / 2 - 4.5, 0.3, Hw - 0.4, int(L * 1.4), 230 + len(side), keys=('stone', 'stone_dark', 'stone_light'))
        band(0, 0, W, D, B + Hw - 0.6, 0.6, 'stone_light', out=0.25)
        battlements(ft[side], -L / 2 + 4.5, L / 2 - 4.5, 0, 'stone', cap='stone_light')
    door(fo['back'], 0, w=5.0, h=7.0, arch=True, key='door_paint', surround='stone_light', step='stone_dark', lamp=True)
    for x in (-6.0, 6.0):
        cyl(nm('gp'), 0.6, Hw + 1.4, loc=(x, D / 2 + 0.4, B), key='stone_light', verts=10)
    for (cx, cy) in ((-W / 2, -D / 2), (W / 2, -D / 2), (W / 2, D / 2)):
        cyl(nm('tw'), 4.2, Hw + 3.0, loc=(cx, cy, B), key='stone', verts=20)
        lathe(nm('tc'), [(4.2, B + Hw + 2.4), (4.7, B + Hw + 3.0), (4.7, B + Hw + 3.2), (0, B + Hw + 3.2)], loc=(cx, cy, 0), key='stone_light', segs=20)
        ring_battlements(cx, cy, B + Hw + 3.2, 4.7, 'stone', cap='stone_light')
        for k in range(3):
            a = math.atan2(cy, cx) + (k - 1) * 0.9
            from arch import arrow_slit
            arrow_slit(F(cx + math.cos(a) * 4.2, cy + math.sin(a) * 4.2, B, math.degrees(a) + 90), 0, Hw * 0.55)
    cx, cy = -W / 2, D / 2
    cyl(nm('kt'), 4.6, Hw + 10.0, loc=(cx, cy, B), key='stone', verts=20)
    lathe(nm('ktc'), [(4.6, B + Hw + 9.4), (5.2, B + Hw + 10.0), (5.2, B + Hw + 10.2), (0, B + Hw + 10.2)], loc=(cx, cy, 0), key='stone_light', segs=20)
    ring_battlements(cx, cy, B + Hw + 10.2, 5.2, 'stone', cap='stone_light')
    for z in (B + 6.0, B + 12.0):
        window(F(cx + 3.25, cy - 3.25, z, 45 + 90 - 180), 0, 0, w=1.4, h=2.4, arch=True, frame='wood_dark', glass='glass_lit', sill='stone_light', lit=True)
    tube(nm('fp'), [(cx, cy, B + Hw + 10.2), (cx, cy, B + Hw + 22.0)], 0.22, 'wood_paint', res=4)
    flag(cx + 0.1, cy, B + Hw + 21.6, w=5.0, h=3.2, key='fabric_red', emblem='gold')
    # battery and inner works
    for x in (-9.0, 0.0, 9.0):
        cannon_at(x, -D / 2 + 2.4, B + Hw, s=0.75, d=-1)
    ball_pyramid(-4.5, -D / 2 + 2.6, B + Hw, r=0.26)
    ball_pyramid(4.5, -D / 2 + 2.6, B + Hw, r=0.26)
    for k in range(12):
        z = B + 0.4 + k * (Hw - 0.4) / 12
        box(nm('is'), (3.0, 1.0, z - B), loc=(W / 2 - T - 1.5, D / 2 - T - 3.0 - k * 1.0, B + (z - B) / 2), key='stone_light')
    px, py = -6.0, 4.0
    box(nm('ps'), (7.0, 5.0, 4.0), loc=(px, py, B + 2.0), key='stone_light')
    gable_roof(F(px, py, 0, 0), 7.0, 5.0, B + 4.0, 1.8, keys=('tile_grey', 'tile_a'), wall='stone_light', ov=0.4, ovg=0.4)
    door(faces(px, py, 7.0, 5.0, B)['front'], 0, w=1.8, h=3.0, arch=True, key='iron', surround='stone', step=None, studs=True)
    for k in range(3):
        barrel_at(px + 4.6, py - 1.4 + k * 1.5, B + 0.4, 0.75, 'wood_dark')
    ball_pyramid(4.0, 2.0, B + 0.4, r=0.3, n=4)
    return finalize('harbour_fort', smooth_angle=30)


# ============================================================ G24-G27 harbour houses and tavern
def wall_wheel(x, y, z, R=1.2):
    torus(nm('ww'), R, 0.1, loc=(x, y, z), key='wood_dark', segs=18, rsegs=4, rot=(90, 0, 0))
    for k in range(8):
        a = 2 * math.pi * k / 8
        tube(nm('wk'), [(x, y, z), (x + math.cos(a) * (R + 0.35), y, z + math.sin(a) * (R + 0.35))], 0.06, 'wood_dark', res=2)
    cyl(nm('wh'), 0.22, 0.3, loc=(x, y - 0.15, z), key='brass', verts=10, rot=(90, 0, 0))


def hung_net(fr, x, z, w=4.0, h=3.0, seed=0):
    rnd = random.Random(seed)
    for k in range(7):
        xx = x - w / 2 + w * k / 6
        tube(nm('hn'), [fr.p(xx, -0.15, z), fr.p(xx + rnd.uniform(-0.2, 0.2), -0.35, z - h * 0.6), fr.p(xx * 0.9 + x * 0.1, -0.3, z - h)], 0.03, 'net', res=2, ures=3)
    for j in range(5):
        zz = z - h * (j + 0.5) / 5
        tube(nm('hn'), [fr.p(x - w / 2 * (1 - j * 0.06), -0.25, zz + 0.1), fr.p(x, -0.38, zz - 0.15), fr.p(x + w / 2 * (1 - j * 0.06), -0.25, zz + 0.1)], 0.03, 'net', res=2, ures=3)
    for k in range(5):
        p = fr.p(x - w / 2 + w * k / 4, -0.2, z)
        ball(nm('nf'), 0.18, loc=p, key='fl_orange', segs=6, rings=4)


def harbour_house_1():
    """G24 - harbour house 1: whitewashed two-storey fisher's home, red tile roof, blue shutters and flower boxes,
    net hung on the wall, oars leaning, lobster traps and a drying-fish line."""
    reset()
    top = house(cx=0.0, w=12.0, d=10.0, floors=2, gh=7.0, fh=6.4, ground='whitewash', ground_trim='stone_light', upper='whitewash', timber=False,
                jetty=0.0, roof='side', rkeys=('tile_red_a', 'tile_red_b'), shutter='shutter_b', flowers=('fl_blue', 'fl_white'), dormers=1, seed=24)
    fc = faces(0, 0, 12.0, 10.0)
    hung_net(fc['right'], 0, 11.6, w=4.0, h=3.0, seed=241)
    for k in range(2):
        tube(nm('oar'), [fc['left'].p(-2.0 + k * 0.7, -0.5 - k * 0.2, 0.0), fc['left'].p(-1.6 + k * 0.7, -0.2, 7.0)], 0.08, 'wood_light', res=2)
        lbox(fc['left'], (0.5, 0.08, 1.4), -1.98 + k * 0.7, -0.48 - k * 0.2, 0.8, 'wood_light')
    for k in range(2):
        box(nm('lt'), (3.0, 1.8, 1.2), loc=(7.6, -2.0 + k * 0.4, 0.6 + k * 1.2), key='wood_grey', rot=(0, 0, k * 8))
        for j in range(3):
            tube(nm('lth'), [(6.2, -2.8 + k * 0.4, 1.0 + k * 1.2), (6.2, -2.0 + k * 0.4, 1.4 + k * 1.2), (6.2, -1.2 + k * 0.4, 1.0 + k * 1.2)], 0.04, 'wood_old', res=2)
    line(fc['front'].p(-5.8, -0.2, 6.4), (-9.0, -7.0, 6.0), 0.03)
    tube(nm('lp'), [(-9.0, -7.0, 0.0), (-9.0, -7.0, 6.4)], 0.15, 'wood_grey', res=4)
    for k in range(5):
        p = Vector(fc['front'].p(-5.8, -0.2, 6.4)).lerp(Vector((-9.0, -7.0, 6.0)), (k + 1) / 6)
        line(tuple(p), (p.x, p.y, p.z - 0.6), 0.02)
        ball(nm('df'), 0.25, loc=(p.x, p.y, p.z - 1.0), key='fish', segs=6, rings=4, scale=(0.4, 0.3, 1.6))
    return finalize('harbour_house_1', smooth_angle=30)


def harbour_house_2():
    """G25 - harbour house 2: narrow three-storey stone and green-plaster house, timber framing, grey slate gable to the street,
    red shutters, an anchor plaque and a wall lantern."""
    reset()
    house(cx=0.0, w=10.0, d=11.0, floors=3, gh=7.0, fh=6.2, ground='stone', ground_trim='stone_dark', upper='plaster_c', timber=True, jetty=0.5,
          roof='front', rkeys=('tile_grey', 'tile_a'), shutter='shutter_r', flowers=('fl_red', 'fl_yellow'), dormers=0, seed=25, chim=True)
    fc = faces(0, 0, 10.0, 11.0)
    anchor_parts(-3.2, -5.6, 3.0, s=0.32)
    lbox(fc['front'], (1.6, 0.12, 2.8), -3.2, -0.06, 4.2, 'shutter_g')
    return finalize('harbour_house_2', smooth_angle=30)


def harbour_house_3():
    """G26 - harbour house 3: weathered plank fisher's shack on pilings over the water, porch with railing, shuttered windows,
    old tile roof with stovepipe, ladder to the water, hung net, lantern and barrels."""
    reset()
    rnd = random.Random(26)
    w, d, Z = 10.0, 8.0, DECK
    for x in (-4.5, 0.0, 4.5):
        for y in (-7.0, -3.6, 0.0, 3.6):
            piling(x, y, top=Z - 0.45, r=0.45, seed=260 + int(x * 3 + y))
    for y in (-7.0, -3.6, 0.0, 3.6):
        box(nm('cb'), (10.6, 0.8, 0.8), loc=(0, y, Z - 0.85), key='piling')
    deck_planks(-5.4, 5.4, -7.8, 4.2, z=Z, seed=26)
    box(nm('hw'), (w, d, 6.0), loc=(0, 0, Z + 3.0), key='wood_grey')
    fc = faces(0, 0, w, d, Z)
    for s in fc:
        boards(fc[s], w if s in ('front', 'back') else d, 0.1, 5.9, 'wood_old', step=1.1)
    door(fc['front'], -2.2, w=2.2, h=4.0, arch=False, key='shutter_b', surround='wood_old', step=None, studs=False)
    window(fc['front'], 2.2, 1.6, w=1.8, h=1.8, frame='wood_paint', shutter='shutter_b', sill='wood_old', lit=True)
    for s in ('left', 'right', 'back'):
        window(fc[s], 0, 1.6, w=1.6, h=1.8, frame='wood_paint', shutter='shutter_b', sill='wood_old')
    gable_roof(F(0, 0, 0, 0), w, d, Z + 6.0, 3.2, keys=('roof_old', 'roof_old_b'), wall='wood_grey', ov=0.8, ovg=0.6)
    tube(nm('sp'), [(3.0, 1.6, Z + 6.5), (3.0, 1.6, Z + 11.0)], 0.25, 'iron', res=4)
    lathe(nm('spc'), [(0.6, 0), (0.1, 0.5), (0, 0.55)], loc=(3.0, 1.6, Z + 11.0), key='iron', segs=8)
    fr = F(0, -7.8, Z, 0)
    railing(fr, -5.4, 5.4, 0, y=0.1, h=1.6, key='wood_grey', step=1.0)
    lbox(fr, (0.3, 0.3, 4.6), -5.2, 0.1, 2.3, 'wood_grey')
    lbox(fr, (0.3, 0.3, 4.6), 5.2, 0.1, 2.3, 'wood_grey')
    for s in (-1, 1):
        tube(nm('pr'), [(s * 5.2, -7.6, Z + 4.6), (s * 5.2, -4.0, Z + 5.9)], 0.14, 'wood_grey', res=2)
    lslab(F(0, 0, 0, 0), [(-5.6, -8.2, Z + 4.6), (-5.6, -4.0, Z + 6.1), (-5.6, -4.0, Z + 6.3), (-5.6, -8.2, Z + 4.8)], (11.2, 0, 0), 'roof_old_b')
    for k in range(9):
        z = WL - 0.8 + k * (Z - WL + 0.8) / 8
        tube(nm('lr'), [(-1.0, -8.0, z), (1.0, -8.0, z)], 0.06, 'wood_grey', res=2)
    for s in (-1, 1):
        tube(nm('ls'), [(s * 1.0, -8.0, WL - 1.0), (s * 1.0, -8.0, Z + 0.1)], 0.1, 'wood_grey', res=2)
    hung_net(fc['right'], 0, 5.4, w=4.4, h=3.4, seed=262)
    tube(nm('lh'), [(3.6, -7.4, Z + 5.0), (3.6, -7.4, Z + 4.4)], 0.03, 'iron', res=2)
    box(nm('lg'), (0.5, 0.5, 0.7), loc=(3.6, -7.4, Z + 4.0), key='glass_lit')
    lathe(nm('lc'), [(0.4, 0), (0, 0.35)], loc=(3.6, -7.4, Z + 4.35), key='iron', segs=4)
    for k in range(2):
        barrel_at(-4.2 + k * 1.4, -6.6, Z, 0.75, 'wood_old')
    coil_at(1.8, -6.4, Z, R=0.8)
    return finalize('harbour_house_3', smooth_angle=30)


def harbour_tavern():
    """G27 - harbour tavern: big timber-framed inn with lit shop windows, red tile roof and dormers, carved sign, plank terrace with tables
    and barrel stools, porch lanterns, ship's wheel and anchor on the wall, stacked casks."""
    reset()
    rnd = random.Random(27)
    w, d = 20.0, 14.0
    house(cx=0.0, w=w, d=d, floors=2, gh=8.0, fh=7.0, ground='stone', ground_trim='stone_dark', upper='plaster_d', timber=True, jetty=0.7,
          roof='side', rkeys=('tile_red_a', 'tile_red_b'), shutter='shutter_g', flowers=('fl_red', 'fl_white'), shop=True, sign='shutter_r', seed=27,
          dormers=2, lit=((0, 0), (0, 1), (0, 2)))
    fc = faces(0, 0, w, d)
    wall_wheel(-7.0, -d / 2 - 1.0, 11.6, R=1.3)
    anchor_parts(7.0, -d / 2 - 1.0, 9.0, s=0.4)
    # terrace
    deck_planks(-w / 2, w / 2, -d / 2 - 7.0, -d / 2, z=0.5, seed=27, t=0.4)
    for x in (-w / 2 + 0.3, -3.5, 3.5, w / 2 - 0.3):
        cyl(nm('tp'), 0.22, 4.6, loc=(x, -d / 2 - 6.8, 0.5), key='timber', verts=8)
        tube(nm('tl'), [(x, -d / 2 - 6.8, 5.0), (x + 0.6, -d / 2 - 6.8, 5.3)], 0.05, 'iron', res=2)
        box(nm('tlg'), (0.45, 0.45, 0.65), loc=(x + 0.6, -d / 2 - 6.8, 4.6), key='glass_lit')
        lathe(nm('tlc'), [(0.38, 0), (0, 0.35)], loc=(x + 0.6, -d / 2 - 6.8, 4.92), key='iron', segs=4)
    tube(nm('tb'), [(-w / 2 + 0.3, -d / 2 - 6.8, 5.0), (w / 2 - 0.3, -d / 2 - 6.8, 5.0)], 0.18, 'timber', res=4)
    railing(F(0, -d / 2 - 7.0, 0.5, 0), -w / 2, -1.5, 0, y=0.1, h=1.4, key='timber', step=1.2)
    railing(F(0, -d / 2 - 7.0, 0.5, 0), 1.5, w / 2, 0, y=0.1, h=1.4, key='timber', step=1.2)
    for tx in (-6.0, 0.0, 6.0):
        ty = -d / 2 - 3.8
        box(nm('tt'), (2.8, 1.6, 0.18), loc=(tx, ty, 3.4), key='wood')
        box(nm('tleg'), (0.4, 0.4, 2.8), loc=(tx, ty, 1.9), key='wood_dark')
        for s in (-1, 1):
            barrel_at(tx + s * 2.0, ty, 0.5, 0.6)
        lathe(nm('mg'), [(0, 0), (0.18, 0), (0.2, 0.42), (0, 0.42)], loc=(tx - 0.6, ty + 0.2, 3.5), key='wood_light', segs=8)
        lathe(nm('mg'), [(0, 0), (0.18, 0), (0.2, 0.42), (0, 0.42)], loc=(tx + 0.7, ty - 0.2, 3.5), key='brass', segs=8)
        cyl(nm('cd'), 0.12, 0.35, loc=(tx, ty, 3.5), key='wax', verts=6)
    for k in range(5):
        x = w / 2 + 1.6 + (k % 3) * 0.0
        barrel_at(w / 2 + 1.4, -d / 2 + 1.4 + (k % 3) * 1.8, (k // 3) * 1.7, 0.85)
    return finalize('harbour_tavern', smooth_angle=30)


# ============================================================ G28-G33 waterfront pieces
def seawall():
    """G28 - seawall segment, 24 long x 11 tall: battered ashlar face with algae and barnacle band, coping stones, iron mooring rings,
    recessed iron ladder and a drain outlet with rust streak."""
    reset()
    rnd = random.Random(28)
    L, H, T = 24.0, 11.0, 5.0
    box(nm('core'), (L, T, H), loc=(0, 0, H / 2), key='stone')
    lslab(F(0, 0, 0, 0), [(-L / 2, -T / 2, 0), (-L / 2, -T / 2 - 1.6, 0), (-L / 2, -T / 2, H - 1.0)], (L, 0, 0), 'stone')
    fr = F(0, -T / 2, 0, 0)
    for k in range(int(H / 1.1)):
        z = 0.55 + k * 1.1
        lean = 1.6 * (1 - z / (H - 1.0)) if z < H - 1.0 else 0.0
        x = -L / 2 + rnd.uniform(0, 1.6)
        while x < L / 2 - 0.6:
            bw = rnd.choice((1.6, 2.2, 2.8, 1.2))
            bw = min(bw, L / 2 - x)
            box(nm('ash'), (bw - 0.12, 0.3, 1.0), loc=(x + bw / 2, -T / 2 - lean - 0.05, z), key=rnd.choice(('stone', 'stone_dark', 'stone_light', 'cliff_a')),
                rot=(-math.degrees(math.atan2(1.6, H - 1.0)) if z < H - 1.0 else 0, 0, 0), bev=0.04)
            x += bw
    for k in range(int(L / 1.2)):
        x = -L / 2 + 0.6 + k * 1.2
        z = rnd.uniform(1.8, 3.4)
        lean = 1.6 * (1 - z / (H - 1.0))
        box(nm('alg'), (1.25, 0.12, z), loc=(x, -T / 2 - 1.6 * (1 - z / 2 / (H - 1.0)) - 0.22, z / 2), key='algae', rot=(-9, 0, 0))
    for k in range(30):
        x = rnd.uniform(-L / 2 + 0.5, L / 2 - 0.5); z = rnd.uniform(0.3, 2.0)
        ball(nm('bn'), rnd.uniform(0.12, 0.2), loc=(x, -T / 2 - 1.6 * (1 - z / (H - 1.0)) - 0.35, z), key='barnacle', segs=6, rings=4)
    for k in range(8):
        box(nm('cp'), (L / 8 - 0.1, T + 0.8, 0.9), loc=(-L / 2 + L / 8 * (k + 0.5), -0.2, H + 0.45), key='stone_light', bev=0.08)
    for x in (-7.0, 7.0):
        box(nm('rb'), (0.6, 0.3, 0.6), loc=(x, -T / 2 - 0.25, H - 1.6), key='iron')
        torus(nm('rg'), 0.55, 0.11, loc=(x, -T / 2 - 0.45, H - 2.2), key='iron', segs=12, rsegs=4, rot=(90, 0, 0))
    lx = 2.0
    box(nm('lrc'), (2.2, 0.6, H - 1.4), loc=(lx, -T / 2 - 0.1, (H - 1.4) / 2 + 1.0), key='stone_dark')
    for s in (-0.7, 0.7):
        tube(nm('lrr'), [(lx + s, -T / 2 - 0.5, 0.5), (lx + s, -T / 2 - 0.5, H + 1.6)], 0.09, 'iron', res=4)
    for k in range(13):
        tube(nm('lrg'), [(lx - 0.7, -T / 2 - 0.5, 1.0 + k * 0.8), (lx + 0.7, -T / 2 - 0.5, 1.0 + k * 0.8)], 0.06, 'iron', res=2)
    cyl(nm('dr'), 0.6, 1.0, loc=(-3.0, -T / 2 - 0.4, 5.0), key='tar', verts=12, rot=(90, 0, 0))
    torus(nm('drr'), 0.65, 0.12, loc=(-3.0, -T / 2 - 0.9, 5.0), key='rust', segs=12, rsegs=4, rot=(90, 0, 0))
    box(nm('st'), (0.7, 0.08, 3.6), loc=(-3.0, -T / 2 - 0.85, 2.9), key='rust', rot=(-8, 0, 0))
    return finalize('seawall', smooth_angle=30)


def breakwater():
    """G29 - breakwater rock run, 32 long: heaped armour boulders, dark and algae-covered at the waterline, lighter on top,
    with a beacon post and red lamp at the end."""
    reset()
    rnd = random.Random(29)
    L = 32.0
    for i in range(14):
        x = -L / 2 + 1.5 + i * (L - 3.0) / 13
        for s in (-1, 1):
            o = rock(nm('rb'), rnd.uniform(2.6, 3.4), (x + rnd.uniform(-0.8, 0.8), s * rnd.uniform(3.2, 4.2), 1.2), rnd.choice(('stone_dark', 'cliff_b')),
                     seed=290 + i * 2 + (s > 0), scale=(1.2, 1.05, 1.05), rot_z=rnd.uniform(0, 3))
            top_paint(o, 'algae', 0.35, 290 + i) if rnd.random() < 0.5 else None
    for i in range(11):
        x = -L / 2 + 2.5 + i * (L - 5.0) / 10
        rock(nm('rt'), rnd.uniform(2.6, 3.2), (x + rnd.uniform(-0.6, 0.6), rnd.uniform(-1.0, 1.0), 4.4), rnd.choice(('cliff_a', 'stone', 'cliff_a')),
             seed=320 + i, scale=(1.2, 1.1, 1.05), rot_z=rnd.uniform(0, 3))
    for k in range(10):
        ball(nm('gm'), 0.3, loc=(rnd.uniform(-L / 2 + 3, L / 2 - 3), rnd.uniform(-1.0, 1.0), 7.0 + rnd.uniform(0, 0.4)), key='whitewash', segs=6, rings=4, scale=(1.4, 1, 0.3))
    bx = L / 2 - 2.0
    cyl(nm('bb'), 1.0, 1.2, loc=(bx, 0, 4.8), key='stone_light', verts=10)
    tube(nm('bp'), [(bx, 0, 6.0), (bx, 0, 12.0)], 0.3, 'piling', res=4)
    for k in range(3):
        box(nm('bs'), (0.68, 0.68, 0.5), loc=(bx, 0, 7.0 + k * 1.4), key='lh_red' if k % 2 == 0 else 'lh_white')
    cyl(nm('bl'), 0.55, 0.15, loc=(bx, 0, 12.0), key='iron', verts=8)
    lathe(nm('blg'), [(0, 12.15), (0.35, 12.15), (0.4, 12.8), (0, 12.9)], key='potion_red', segs=8)
    lathe(nm('blc'), [(0.5, 12.9), (0, 13.3)], key='iron', segs=8)
    return finalize('breakwater', smooth_angle=30)


def ship_bell():
    """G30 - dock bell: brass ship's bell under a little shingled roof on an oak post frame, clapper, bell rope and a name plate."""
    reset()
    for s in (-1, 1):
        box(nm('po'), (0.5, 0.5, 6.0), loc=(s * 1.6, 0, 3.0), key='timber', bev=0.04)
        beam3((s * 1.6, 0, 0.0), (s * 2.6, 0, 0.0), 0.5, 0.5, 'timber')
        beam3((s * 1.6, -0.9, 0.0), (s * 1.6, 0.9, 0.0), 0.5, 0.5, 'timber')
        beam3((s * 1.6, 0, 1.6), (s * 2.4, 0, 0.2), 0.3, 0.3, 'timber')
    box(nm('cb'), (4.2, 0.6, 0.5), loc=(0, 0, 6.0), key='timber')
    gable_roof(F(0, 0, 0, 0), 4.6, 1.8, 6.3, 1.2, keys=('roof_old', 'roof_old_b'), wall='timber', ov=0.4, ovg=0.3)
    lathe(nm('bl'), [(0, 3.3), (1.05, 3.3), (1.0, 3.45), (0.85, 3.9), (0.72, 4.7), (0.66, 5.2), (0.5, 5.45), (0.2, 5.55), (0, 5.55)], key='brass', segs=16)
    lathe(nm('blr'), [(1.06, 3.5), (1.1, 3.55), (1.06, 3.62)], key='brass', segs=16)
    torus(nm('bh'), 0.2, 0.06, loc=(0, 0, 5.72), key='iron', segs=8, rsegs=4, rot=(90, 0, 0))
    tube(nm('bk'), [(0, 0, 5.8), (0, 0, 6.0)], 0.06, 'iron', res=2)
    tube(nm('cl'), [(0, 0, 5.3), (0, 0, 3.6)], 0.05, 'iron', res=2)
    ball(nm('clb'), 0.2, loc=(0, 0, 3.6), key='iron', segs=8, rings=6)
    tube(nm('rp'), [(0, 0, 3.5), (0.2, -0.3, 2.4), (0.4, -0.5, 1.2)], 0.06, 'rope', res=2)
    torus(nm('rk'), 0.12, 0.08, loc=(0.4, -0.5, 1.1), key='rope_dark', segs=8, rsegs=4)
    box(nm('np'), (1.6, 0.1, 0.5), loc=(0, -0.32, 6.0), key='brass')
    return finalize('ship_bell', smooth_angle=30)


def mooring_bollard():
    """G31 - double mooring bollard on a dressed stone block, with a hawser looped in a figure eight around both posts."""
    reset()
    box(nm('bk'), (4.2, 2.4, 0.8), loc=(0, 0, 0.4), key='stone_light', bev=0.1)
    box(nm('bp'), (3.2, 1.6, 0.35), loc=(0, 0, 0.98), key='iron', bev=0.05)
    for x in (-0.95, 0.95):
        bollard_at(x, 0, 1.15, s=0.85)
    pts = []
    for i in range(33):
        a = 2 * math.pi * i / 32
        pts.append((0.95 * math.sin(a) * 1.25, 0.55 * math.sin(2 * a), 1.9 + 0.12 * math.cos(a)))
    tube(nm('f8'), pts, 0.13, 'rope', res=4, ures=2)
    tube(nm('hw'), [(1.3, 0.3, 1.95), (2.6, -0.4, 1.6), (4.4, -1.0, 0.9), (6.0, -1.2, 0.2)], 0.14, 'rope', res=4, ures=3)
    return finalize('mooring_bollard', smooth_angle=30)


def gangplank():
    """G32 - gangplank, 14 long: thick boards with grip battens, iron hooks at the ship end, rollers at the quay end, stanchions and sagging rope rails."""
    reset()
    L, W = 14.0, 2.6
    for k in range(3):
        box(nm('gb'), (L, W / 3 - 0.06, 0.35), loc=(0, -W / 2 + W / 3 * (k + 0.5), 0.6), key='dock' if k != 1 else 'dock_b', bev=0.03)
    for x in (-L / 2 + 1.0, 0.0, L / 2 - 1.0):
        box(nm('gu'), (0.4, W, 0.3), loc=(x, 0, 0.3), key='piling')
    for k in range(17):
        box(nm('bt'), (0.18, W - 0.2, 0.14), loc=(-L / 2 + 0.6 + k * (L - 1.2) / 16, 0, 0.84), key='wood_dark')
    for s in (-1, 1):
        tube(nm('hk'), [(L / 2 - 0.2, s * 0.8, 0.8), (L / 2 + 0.5, s * 0.8, 0.9), (L / 2 + 0.7, s * 0.8, 0.4)], 0.07, 'iron', res=2)
        cyl(nm('rl'), 0.3, 0.4, loc=(-L / 2 + 0.2, s * 1.1 - (0.4 if s > 0 else 0), 0.3), key='iron', verts=10, rot=(-90, 0, 0))
        xs = [-L / 2 + 0.6 + k * (L - 1.2) / 4 for k in range(5)]
        for x in xs:
            tube(nm('stn'), [(x, s * (W / 2 - 0.1), 0.8), (x, s * (W / 2 - 0.1), 3.4)], 0.07, 'iron', res=2)
            torus(nm('se'), 0.12, 0.04, loc=(x, s * (W / 2 - 0.1), 3.45), key='iron', segs=8, rsegs=3, rot=(0, 90, 0))
        for x0, x1 in zip(xs, xs[1:]):
            sag((x0, s * (W / 2 - 0.1), 3.4), (x1, s * (W / 2 - 0.1), 3.4), s=0.35, r=0.06)
    tube(nm('tg'), [(-L / 2 - 0.2, -W / 2, 0.45), (-L / 2 - 0.2, W / 2, 0.45)], 0.1, 'iron', res=2)
    return finalize('gangplank', smooth_angle=30)


def cargo_pallet():
    """G33 - cargo pallet ready for the crane: slatted pallet, sacks, crates and a cask under a rope cargo net gathered to a lifting ring."""
    reset()
    rnd = random.Random(33)
    for k in range(3):
        box(nm('pr'), (5.0, 0.6, 0.5), loc=(0, -1.8 + k * 1.8, 0.25), key='wood_dark')
    for k in range(9):
        box(nm('ps'), (0.48, 4.4, 0.18), loc=(-2.3 + k * 0.575, 0, 0.6), key='wood_light')
    crate_at(-1.2, -0.9, 0.7, 0.75, 5)
    crate_at(-1.2, 0.9, 0.7, 0.75, -4)
    crate_at(-1.2, 0.0, 2.2, 0.7, 20)
    barrel_at(1.2, -1.1, 0.7, 0.8)
    for k in range(5):
        blob(nm('sk'), 0.75, (1.0 + rnd.uniform(-0.6, 0.9), 0.9 + rnd.uniform(-0.5, 0.6), 1.2 + (k // 3) * 0.9), 'canvas' if k % 2 else 'canvas_b', subdiv=2, amp=0.14,
             scale=(1.35, 0.95, 0.65), seed=330 + k)
    ring = (0, 0, 7.0)
    for k in range(8):
        a = 2 * math.pi * k / 8
        bx, by = math.cos(a) * 2.6, math.sin(a) * 2.2
        tube(nm('nr'), [(bx, by, 0.7), (bx * 0.9, by * 0.9, 2.6), (bx * 0.55, by * 0.55, 3.9), (0, 0, 6.8)], 0.05, 'rope', res=2, ures=3)
    for z, f in ((1.6, 1.0), (2.8, 0.85), (3.8, 0.58)):
        torus(nm('nh'), 2.4 * f, 0.05, loc=(0, 0, z), key='rope', segs=20, rsegs=3)
    torus(nm('rg'), 0.4, 0.1, loc=ring, key='iron', segs=12, rsegs=4, rot=(90, 0, 0))
    return finalize('cargo_pallet', smooth_angle=30)


ITEMS_B = [
    ('G11_lighthouse', lighthouse), ('G12_warehouse_1', warehouse_1), ('G13_warehouse_2', warehouse_2), ('G14_harbour_master', harbour_master),
    ('G15_fish_market_stall', fish_market_stall), ('G16_cargo_crane', cargo_crane), ('G17_net_rack', net_rack), ('G18_rope_coil', rope_coil),
    ('G19_anchor', anchor), ('G20_buoy', buoy), ('G21_lobster_trap', lobster_trap), ('G22_cannon', cannon), ('G23_harbour_fort', harbour_fort),
    ('G24_harbour_house_1', harbour_house_1), ('G25_harbour_house_2', harbour_house_2), ('G26_harbour_house_3', harbour_house_3),
    ('G27_harbour_tavern', harbour_tavern), ('G28_seawall', seawall), ('G29_breakwater', breakwater), ('G30_ship_bell', ship_bell),
    ('G31_mooring_bollard', mooring_bollard), ('G32_gangplank', gangplank), ('G33_cargo_pallet', cargo_pallet),
]
