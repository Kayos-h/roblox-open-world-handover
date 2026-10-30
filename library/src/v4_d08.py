"""D08 - statues, ruins, standing stones, markers and banners (12 models).
Original elven designs, natural stone and cloth colours. No glow. 1 unit = 1 stud, origin bottom-centre, front = -Y.
NOTE: kitlib box/cyl/lathe `rot` args are DEGREES; obj.rotation_euler is RADIANS.
"""
import math, random, bmesh
from mathutils import Vector
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, top_paint, _obj_from_bm
from v4_elf import nm, ivy_strand, mushrooms
from v4_d04 import prism_xz
from v4_d06 import tuft, mini_fern, moss_skirt, ribbon
from nature import rock, blob

PI = math.pi
STONE, WARM, DARK = 'ev_stone', 'ev_stone_warm', 'ev_stone_dark'


# ------------------------------------------------------------------ shared helpers
def fold_robe(profile, segs, key, loc=(0, 0, 0), folds=7, amp=0.07, phase=0.0, seed=0):
    """Revolved robe with vertical folds. profile = [(r, z), ...] starting and ending at r=0 poles."""
    bm = bmesh.new()
    rings = []
    ztop = profile[-1][1]
    for (r, z) in profile:
        if r < 1e-5:
            rings.append([bm.verts.new((0, 0, z))])
            continue
        ring = []
        fade = 1.0 if z < ztop * 0.8 else 0.25
        for i in range(segs):
            a = 2 * PI * i / segs
            k = 1 + amp * fade * (math.sin(a * folds + phase + z * 0.4) + 0.4 * math.sin(a * (folds + 3) + seed))
            ring.append(bm.verts.new((math.cos(a) * r * k, math.sin(a) * r * k, z)))
        rings.append(ring)
    for A, B in zip(rings, rings[1:]):
        if len(A) == 1 and len(B) == 1:
            continue
        if len(A) == 1:
            for i in range(segs):
                bm.faces.new((A[0], B[i], B[(i + 1) % segs]))
        elif len(B) == 1:
            for i in range(segs):
                bm.faces.new((A[i], B[0], A[(i + 1) % segs]))
        else:
            for i in range(segs):
                bm.faces.new((A[i], A[(i + 1) % segs], B[(i + 1) % segs], B[i]))
    if len(rings[0]) > 1:
        bm.faces.new(list(reversed(rings[0])))
    if len(rings[-1]) > 1:
        bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj_from_bm(nm('rb'), bm, key)
    o.location = loc
    return o


def limb(p0, p1, p2, r, taper, key=STONE):
    tube(nm('lm'), [p0, p1, p2], r, key, res=5, ures=3, taper=taper)


def head(x, y, z, s=1.0, key=STONE, hair=WARM):
    """Elf head: face, brow, nose, hair, circlet and long pointed ears."""
    ball(nm('hd'), 0.8 * s, (x, y, z), key, segs=12, rings=8, scale=(0.9, 0.95, 1.08))
    ball(nm('ns'), 0.13 * s, (x, y - 0.78 * s, z - 0.08 * s), key, segs=6, rings=4)
    ball(nm('br'), 0.5 * s, (x, y - 0.62 * s, z + 0.2 * s), key, segs=8, rings=4, scale=(1.35, 0.3, 0.16))
    ball(nm('hr'), 0.93 * s, (x, y + 0.3 * s, z + 0.12 * s), hair, segs=12, rings=8, scale=(1.0, 1.0, 1.06))
    ball(nm('hl'), 0.8 * s, (x, y + 0.7 * s, z - 1.6 * s), hair, segs=10, rings=6, scale=(0.95, 0.6, 2.3))
    for sx in (-1, 1):
        cyl(nm('ear'), 0.26 * s, 1.5 * s, loc=(x + sx * 0.76 * s, y + 0.05 * s, z + 0.05 * s), key=key, verts=5, rot=(-20, 55 * sx, 0), r2=0.02)
    torus(nm('cir'), 0.84 * s, 0.05 * s, loc=(x, y, z + 0.42 * s), key=WARM, segs=20, rsegs=4)


def plinth_round(r, h1=0.9, h2=1.7):
    a = cyl(nm('pl'), r, h1, loc=(0, 0, 0), key=DARK, verts=24, bev=0.08)
    b = cyl(nm('pl'), r * 0.82, h2, loc=(0, 0, h1), key=STONE, verts=24, bev=0.08)
    top_paint(a, 'ev_moss', 0.8, 1, noise_amt=0.2)
    return h1 + h2


def leaf_motif(x, y, z, h, s, key=WARM, face=-1):
    """Carved leaf: two flattened ellipsoids crossing; faces front (-Y) when face=-1."""
    for k in (-1, 1):
        o = ball(nm('lf'), s, (x, y, z), key, segs=7, rings=4, scale=(0.42, 0.14, 1.0))
        o.rotation_euler = (0, k * 0.5, 0)
    ball(nm('lv'), s * 0.14, (x, y - 0.02, z), key, segs=5, rings=3, scale=(0.5, 0.5, 1.9))


def dress_base(rnd, rad, seed, ferns=True):
    moss_skirt(rad, seed, sx=1.05, sy=1.0, h=0.35 / rad)
    if ferns:
        mini_fern(rad * 0.75, -rad * 0.4, 0.0, 6, 2.6, seed + 1)
        mini_fern(-rad * 0.7, rad * 0.45, 0.0, 5, 2.2, seed + 2)
    tuft(rad * 0.1, -rad * 0.85, 0.0, rnd, n=7)
    tuft(-rad * 0.9, -rad * 0.2, 0.0, rnd, n=6)


# ------------------------------------------------------------------ D08_01..03 statues
def statue_a():
    """Elven sage in long robes: staff with a leaf finial in one hand, a glass-smooth orb in the other."""
    reset()
    rnd = random.Random(801)
    zb = plinth_round(4.4)
    prof = [(0, 0), (2.55, 0), (2.4, 0.8), (2.05, 2.6), (1.6, 4.6), (1.22, 6.0), (1.34, 7.1), (1.6, 8.1), (1.45, 8.9), (0.8, 9.35), (0.52, 9.65), (0, 9.75)]
    fold_robe(prof, 20, STONE, loc=(0, 0, zb), folds=7, amp=0.08, seed=1)
    torus(nm('belt'), 1.3, 0.12, loc=(0, 0, zb + 6.1), key=WARM, segs=20, rsegs=5)
    # hanging sash with ends
    tube(nm('sash'), [(0.2, -1.32, zb + 6.1), (0.5, -1.45, zb + 4.2), (0.35, -1.7, zb + 2.0)], 0.2, WARM, res=4, ures=3, taper=[1.0, 1.4, 1.0])
    ball(nm('sh'), 1.0, (0, 0.05, zb + 9.2), STONE, segs=12, rings=8, scale=(1.6, 0.9, 0.5))
    head(0, -0.05, zb + 10.6)
    # cloak edge falling behind
    tube(nm('clk'), [(-1.3, 0.8, zb + 9.0), (-1.6, 1.5, zb + 5.0), (-1.2, 1.9, zb + 0.8)], 0.55, WARM, res=5, ures=3, taper=[0.5, 1.2, 1.4])
    tube(nm('clk'), [(1.3, 0.8, zb + 9.0), (1.6, 1.5, zb + 5.0), (1.2, 1.9, zb + 0.8)], 0.55, WARM, res=5, ures=3, taper=[0.5, 1.2, 1.4])
    # right arm to staff
    limb((1.5, 0, zb + 9.0), (2.55, -0.3, zb + 7.6), (2.9, -1.0, zb + 6.6), 0.5, [0.9, 1.2, 1.5])
    ball(nm('hand'), 0.36, (2.9, -1.05, zb + 6.55), STONE, segs=8, rings=5)
    cyl(nm('stf'), 0.17, 15.5, loc=(2.9, -1.05, zb), key=WARM, verts=8)
    for k in range(3):
        torus(nm('stfr'), 0.26, 0.07, loc=(2.9, -1.05, zb + 12.0 + k * 0.4), key=STONE, segs=10, rsegs=4)
    for k in (-1, 1):
        o = ball(nm('fin'), 0.7, (2.9 + k * 0.3, -1.05, zb + 16.4), STONE, segs=8, rings=5, scale=(0.3, 0.14, 1.3))
        o.rotation_euler = (0, k * 0.35, 0)
    # left arm holding an orb
    limb((-1.5, 0, zb + 9.0), (-2.3, -0.6, zb + 7.2), (-2.1, -1.7, zb + 6.4), 0.5, [0.9, 1.2, 1.4])
    ball(nm('hand'), 0.36, (-2.1, -1.8, zb + 6.3), STONE, segs=8, rings=5)
    ball(nm('orb'), 0.62, (-2.1, -1.85, zb + 7.05), WARM, segs=12, rings=8)
    for k in range(4):
        ivy_strand((-1.7 + k * 1.1, -2.2, zb + 3.8 - 0.4 * k), rnd.uniform(2.0, 3.6), seed=80 + k)
    dress_base(rnd, 6.0, 82)
    return finalize('statue_a', smooth_angle=35)


def statue_b():
    """Elven ranger in a short tunic with a long bow, a quiver and a billowing cloak."""
    reset()
    rnd = random.Random(802)
    a = box(nm('pl'), (8.0, 8.0, 0.9), loc=(0, 0, 0.45), key=DARK, bev=0.08)
    b = box(nm('pl'), (6.2, 6.2, 1.5), loc=(0, 0, 1.65), key=STONE, bev=0.08)
    top_paint(a, 'ev_moss', 0.8, 2, noise_amt=0.2)
    for j in range(2):
        box(nm('stp'), (3.4, 1.0, 0.45 - 0.2 * j), loc=(0, -3.6 - j * 0.9, 0.22 - 0.1 * j), key=DARK, bev=0.05)
    zb = 2.4
    # legs: left straight, right stepping forward
    limb((-0.55, 0, zb + 5.6), (-0.6, 0.0, zb + 3.0), (-0.6, 0.1, zb + 0.6), 0.55, [1.0, 0.85, 0.72])
    limb((0.55, 0, zb + 5.6), (0.65, -1.0, zb + 3.2), (0.65, -1.9, zb + 0.6), 0.55, [1.0, 0.85, 0.72])
    ball(nm('ft'), 0.6, (-0.6, -0.2, zb + 0.35), DARK, segs=8, rings=5, scale=(0.8, 1.5, 0.6))
    ball(nm('ft'), 0.6, (0.65, -2.1, zb + 0.35), DARK, segs=8, rings=5, scale=(0.8, 1.5, 0.6))
    prof = [(0, 5.0), (1.6, 5.0), (1.5, 5.5), (1.15, 6.4), (1.05, 6.9), (1.25, 7.8), (1.38, 8.5), (1.1, 9.1), (0.55, 9.45), (0.46, 9.7), (0, 9.8)]
    fold_robe(prof, 18, STONE, loc=(0, 0, zb), folds=6, amp=0.05, seed=2)
    torus(nm('belt'), 1.1, 0.13, loc=(0, 0, zb + 6.7), key=WARM, segs=18, rsegs=5)
    ball(nm('bkl'), 0.28, (0, -1.1, zb + 6.7), WARM, segs=6, rings=4)
    ball(nm('sh'), 1.0, (0, 0.05, zb + 9.15), STONE, segs=12, rings=8, scale=(1.5, 0.85, 0.5))
    head(0, -0.1, zb + 10.55)
    # hooded cloak hanging from the shoulders
    cloth(3.6, 7.6, 8, 12, zb + 9.3, 1.0, 0.35, STONE, freq=1.0, phase=0.6)
    # left arm holds the bow out in front
    limb((-1.4, 0, zb + 9.0), (-1.9, -1.6, zb + 9.1), (-2.0, -3.0, zb + 9.0), 0.46, [1.0, 0.9, 0.9])
    ball(nm('hand'), 0.36, (-2.0, -3.05, zb + 9.0), STONE, segs=8, rings=5)
    bow = []
    for k in range(11):
        f = -1.2 + 2.4 * k / 10
        bow.append((-2.0, -3.0 + 1.7 * (1 - math.cos(f)) / (1 - math.cos(1.2)) * 1.0 - 0.0, zb + 9.0 + 5.4 * math.sin(f) / math.sin(1.2)))
    tube(nm('bow'), bow, 0.15, WARM, res=5, ures=3, taper=[0.5, 0.8, 1.0, 1.1, 1.2, 1.3, 1.2, 1.1, 1.0, 0.8, 0.5])
    tube(nm('str'), [bow[0], bow[-1]], 0.045, DARK, res=3)
    # right hand on the hip
    limb((1.4, 0, zb + 9.0), (2.2, 0.4, zb + 7.6), (1.25, -0.7, zb + 6.5), 0.46, [1.0, 0.95, 0.9])
    ball(nm('hand'), 0.34, (1.2, -0.75, zb + 6.45), STONE, segs=8, rings=5)
    # quiver with arrow fletching
    cyl(nm('qv'), 0.5, 3.2, loc=(0.9, 1.3, zb + 6.0), key=WARM, verts=8, rot=(0, 18, 8))
    for k in range(3):
        cyl(nm('arw'), 0.07, 1.6, loc=(0.75 + k * 0.18, 1.35, zb + 8.9), key=STONE, verts=4, rot=(0, 18, 8))
        cyl(nm('fl'), 0.2, 0.5, loc=(0.75 + k * 0.18 - 0.1, 1.35, zb + 10.2), key=WARM, verts=4, rot=(0, 18, 8), r2=0.02)
    for k in range(4):
        ivy_strand((-3.0 + k * 1.8, -3.9, 2.0), rnd.uniform(1.6, 2.4), seed=90 + k)
    dress_base(rnd, 6.2, 83)
    return finalize('statue_b', smooth_angle=35)


def statue_c():
    """Stag guardian: a stone deer with branching antlers on a mossy rock."""
    reset()
    rnd = random.Random(803)
    ped = rock(nm('ped'), 5.8, (0, 0.2, 1.3), DARK, seed=81, scale=(1.05, 1.45, 0.45), subdiv=4, amp=0.3)
    top_paint(ped, 'ev_moss', 0.5, 81)
    zb = 2.0
    ball(nm('bd'), 1.0, (0, 0.2, zb + 5.6), STONE, segs=14, rings=9, scale=(1.35, 3.1, 1.45))
    ball(nm('ch'), 1.0, (0, -1.8, zb + 6.1), STONE, segs=12, rings=8, scale=(1.3, 1.5, 1.6))
    ball(nm('hn'), 1.0, (0, 2.2, zb + 5.5), STONE, segs=12, rings=8, scale=(1.4, 1.6, 1.5))
    ball(nm('tl'), 0.5, (0, 3.9, zb + 6.3), STONE, segs=8, rings=5, scale=(0.5, 0.8, 1.0))
    tube(nm('nk'), [(0, -2.4, zb + 6.4), (0, -3.5, zb + 8.1), (0, -3.95, zb + 9.4)], 1.0, STONE, res=6, ures=4, taper=[1.4, 1.0, 0.78])
    ball(nm('hd'), 1.0, (0, -4.7, zb + 9.6), STONE, segs=12, rings=8, scale=(0.8, 1.5, 0.78))
    ball(nm('mz'), 0.55, (0, -6.05, zb + 9.2), STONE, segs=8, rings=5, scale=(0.78, 1.1, 0.68))
    ball(nm('ns'), 0.26, (0, -7.0, zb + 9.3), DARK, segs=6, rings=4)
    for sx in (-1, 1):
        o = ball(nm('ear'), 0.5, (sx * 0.95, -4.1, zb + 10.4), STONE, segs=7, rings=4, scale=(0.22, 0.6, 1.2))
        o.rotation_euler = (0, sx * 0.6, 0)
        ball(nm('eye'), 0.14, (sx * 0.62, -5.2, zb + 9.95), DARK, segs=5, rings=3)
        for (y, ys, leg) in ((-1.9, -2.2, 'f'), (2.3, 2.7, 'h')):
            if leg == 'f':
                pts = [(sx * 0.85, y, zb + 5.0), (sx * 0.85, y - 0.1, zb + 2.6), (sx * 0.85, ys, zb + 0.5)]
            else:
                pts = [(sx * 0.85, y, zb + 5.0), (sx * 0.85, y + 0.8, zb + 2.9), (sx * 0.85, ys - 0.1, zb + 0.5)]
            limb(pts[0], pts[1], pts[2], 0.52, [1.1, 0.7, 0.55])
            cyl(nm('hv'), 0.4, 0.55, loc=(sx * 0.85, ys, zb), key=DARK, verts=8)
        # antlers
        base = Vector((sx * 0.45, -4.1, zb + 10.4))
        rel = [(0, 0, 0), (sx * 0.6, 0.3, 1.4), (sx * 1.3, 0.9, 2.7), (sx * 1.8, 1.8, 3.9), (sx * 1.6, 2.7, 5.0)]
        beam = [tuple(base + Vector(p)) for p in rel]
        tube(nm('ant'), beam, 0.19, WARM, res=5, ures=3, taper=[1.3, 1.1, 0.95, 0.8, 0.55])
        for k in (1, 2, 3):
            P = Vector(beam[k])
            tube(nm('tin'), [tuple(P), tuple(P + Vector((sx * 0.25, -0.6, 0.9))), tuple(P + Vector((sx * 0.1, -0.95, 2.0 - 0.3 * k)))], 0.11, WARM, res=4, ures=2,
                 taper=[1.2, 1.0, 0.5])
        P = Vector(beam[0])
        tube(nm('brw'), [tuple(P + Vector((0, 0, 0.2))), tuple(P + Vector((sx * 0.2, -0.8, 0.6))), tuple(P + Vector((sx * 0.3, -1.3, 1.5)))], 0.11, WARM, res=4, ures=2,
             taper=[1.2, 1.0, 0.5])
    for k in range(4):
        ivy_strand((-1.2 + k * 0.8, 0.5, zb + 6.4 - 0.3 * k), rnd.uniform(1.5, 2.8), seed=70 + k)
    mini_fern(4.8, -2.6, 0.0, 6, 2.6, 85)
    mini_fern(-4.6, 2.8, 0.0, 5, 2.2, 86)
    tuft(-2.5, -5.4, 0.0, rnd, n=7)
    mushrooms(4.2, 3.0, 0.8, 5, seed=4, scale=1.4)
    return finalize('statue_c', smooth_angle=35)


# ------------------------------------------------------------------ ruined arches
def voussoir(sx, cx, zs, R, t, a0, a1, depth, key, gap=0.025):
    """One wedge of a pointed/round arch ring (half on side sx). Angles in radians from the spring point."""
    def P(a, r):
        return (cx + sx * r * math.cos(a), zs + r * math.sin(a))
    a0 += gap
    a1 -= gap
    pts = [P(a0, R), P(a1, R), P(a1, R + t), P(a0, R + t)]
    if sx < 0:
        pts = list(reversed(pts))
    return prism_xz(pts, -depth / 2, depth / 2, key)


def ruin_arch_a():
    """Tall pointed (leaf-shaped) arch: left side whole, right side broken off, fallen stones and ivy."""
    reset()
    rnd = random.Random(804)
    S, t, dep, zs = 9.0, 1.8, 3.0, 10.0
    px = S / 2 + 0.8
    for sx in (-1, 1):
        h = zs
        box(nm('pb'), (t + 1.5, dep + 0.8, 0.9), loc=(sx * px, 0, 0.45), key=DARK, bev=0.07)
        pier = box(nm('pr'), (t + 1.1, dep, h - 0.9), loc=(sx * px, 0, 0.9 + (h - 0.9) / 2), key=STONE, bev=0.07)
        top_paint(pier, 'ev_moss', 0.97, sx + 5, noise_amt=0.0)
        box(nm('cap'), (t + 1.5, dep + 0.5, 0.8), loc=(sx * px, 0, zs - 0.4), key=WARM, bev=0.07)
        for k in range(int((h - 1.5) / 2.2)):
            leaf_motif(sx * px, -dep / 2 - 0.05, 2.3 + k * 2.2, 1.2, 0.55)
    R = S
    phimax = math.radians(60)
    nseg = 8
    for i in range(nseg):
        a0, a1 = phimax * i / nseg, phimax * (i + 1) / nseg
        if i < 7:
            o = voussoir(-1, S / 2, zs, R, t, a0, a1, dep, STONE)
            if i >= 5:
                top_paint(o, 'ev_moss', 0.6, i)
        if i < 3:
            voussoir(1, -S / 2, zs, R, t, a0, a1, dep, STONE)
    # fallen blocks
    for (x, y, yaw, sz) in ((7.5, -5.5, 25, (3.0, 1.8, 1.8)), (-1.5, -6.8, -35, (2.6, 1.8, 1.7)), (3.6, -3.4, 70, (2.2, 1.5, 1.5)), (-6.5, -5.4, 10, (2.4, 1.6, 1.6))):
        b = box(nm('fb'), sz, loc=(x, y, sz[2] / 2 - 0.05), key=STONE, rot=(0, 0, yaw), bev=0.08)
        top_paint(b, 'ev_moss', 0.8, int(x * 3))
    for k in range(7):
        a = rnd.uniform(0, 2 * PI)
        d = rnd.uniform(4.5, 9)
        rock(nm('rub'), rnd.uniform(0.5, 1.0), (math.cos(a) * d * 1.2, math.sin(a) * d - 3, 0.0), DARK, seed=k, scale=(1.2, 1.0, 0.7))
    for k in range(7):
        x = -S / 2 - t + rnd.uniform(0.0, 2 * t)
        ivy_strand((-S / 2 + 0.2 + k * 0.45, -dep / 2 - 0.3, zs + rnd.uniform(1.0, 5.0) - k * 0.2), rnd.uniform(4.0, 8.0), seed=100 + k)
    for k in range(5):
        ivy_strand((-px + rnd.uniform(-1, 1), -dep / 2 - 0.4, zs - 0.8), rnd.uniform(5.0, 9.0), seed=120 + k)
    moss_skirt(11.0, 41, sx=1.2, sy=0.7, loc=(0, -2.0, 0.0), h=0.4 / 11.0)
    mini_fern(-8.5, -4.8, 0.0, 7, 3.0, 42)
    mini_fern(8.2, 3.0, 0.0, 6, 2.6, 43)
    tuft(0.0, -8.0, 0.0, rnd, n=8)
    tuft(5.0, 5.5, 0.0, rnd, n=7)
    return finalize('ruin_arch_a', smooth_angle=30)


def wall_blocks(x0, x1, y, thick, hfn, rnd, keys=(STONE, STONE, WARM, DARK), ch=1.25, stagger=True):
    z = 0.0
    row = 0
    while z < 15:
        h = ch * rnd.uniform(0.93, 1.07)
        x = x0 + (rnd.uniform(0, 1.3) if (row % 2 and stagger) else 0.0)
        while x < x1:
            bl = rnd.uniform(1.8, 3.0)
            xe = min(x + bl, x1)
            top = hfn((x + xe) / 2)
            if z + h * 0.55 < top and xe - x > 0.5:
                hh = h if z + h <= top + 0.4 else max(0.6, top - z)
                o = box(nm('wb'), (xe - x - 0.08, thick * rnd.uniform(0.94, 1.0), hh - 0.07), loc=((x + xe) / 2, y + rnd.uniform(-0.05, 0.05), z + hh / 2),
                        key=rnd.choice(keys), bev=0.07, segs=1)
            x = xe
        z += h
        row += 1


def ruin_arch_b():
    """Round-arched gateway set in a broken wall: left side tall, right side crumbled to a stub, with worn steps."""
    reset()
    rnd = random.Random(805)
    Ri, t, dep, zs = 3.3, 1.7, 2.6, 6.0
    xj = Ri + t

    def hfn(x):
        ax = abs(x)
        if ax < Ri - 0.05:
            return 0.0
        if ax < xj:
            return zs
        if x < 0:
            return 13.0 - 0.3 * (ax - xj) + 1.5 * math.sin(ax * 1.7) - 0.25 * max(0, ax - 9) ** 1.4
        return 7.2 - 0.62 * (ax - xj) + 1.4 * math.sin(ax * 2.1)

    wall_blocks(-15.0, -xj, 0.0, dep, hfn, rnd)
    wall_blocks(-xj, -Ri, 0.0, dep, hfn, rnd, stagger=False)
    wall_blocks(Ri, xj, 0.0, dep, hfn, rnd, stagger=False)
    wall_blocks(xj, 11.0, 0.0, dep, hfn, rnd)
    # round arch ring: 11 voussoirs, keystone slightly taller; the right-most three have fallen
    n = 11
    for i in range(n):
        if i < 3:
            continue
        a0, a1 = PI * i / n, PI * (i + 1) / n
        extra = 0.5 if i == 5 else 0.0

        def P(a, r):
            return (r * math.cos(a), zs + r * math.sin(a))
        pts = [P(a0 + 0.02, Ri), P(a1 - 0.02, Ri), P(a1 - 0.02, Ri + t + extra), P(a0 + 0.02, Ri + t + extra)]
        o = prism_xz(pts, -dep / 2 - 0.12, dep / 2 + 0.12, WARM if i == 5 else STONE)
        if i in (3, 4, 8, 9):
            top_paint(o, 'ev_moss', 0.65, i)
    # leaf boss on the keystone
    leaf_motif(0.0, -dep / 2 - 0.2, zs + Ri + 0.9, 1.2, 0.9)
    # steps and threshold
    for j in range(3):
        box(nm('stp'), (2 * Ri + 2.0 + j * 1.2, 1.15, 0.38 * (3 - j)), loc=(0, -dep / 2 - 0.6 - j * 1.1, 0.19 * (3 - j)), key=DARK, bev=0.05)
    box(nm('thr'), (2 * Ri, dep, 0.3), loc=(0, 0, 0.15), key=STONE, bev=0.05)
    # fallen column drum and blocks
    cyl(nm('drum'), 1.4, 3.2, loc=(7.5, -4.8, 1.4), key=STONE, verts=14, rot=(0, 90, 160))
    for (x, y, yaw, sz) in ((10.0, -3.2, 20, (2.6, 1.7, 1.6)), (4.8, -6.2, -30, (2.2, 1.5, 1.5)), (-9.4, -4.2, 35, (2.8, 1.8, 1.7))):
        b = box(nm('fb'), sz, loc=(x, y, sz[2] / 2 - 0.05), key=STONE, rot=(0, 0, yaw), bev=0.08)
        top_paint(b, 'ev_moss', 0.8, int(x * 3))
    # moss tufts on the wall tops, ivy running down the left wall
    for k in range(12):
        x = rnd.uniform(-14, -xj - 0.5) if k < 7 else rnd.uniform(xj + 0.3, 10.5)
        top = hfn(x)
        blob(nm('wm'), rnd.uniform(0.7, 1.2), (x, rnd.uniform(-0.3, 0.3), top + 0.05), 'ev_moss', subdiv=2, amp=0.3, scale=(1.5, 1.0, 0.4), seed=k)
    for k in range(9):
        x = rnd.uniform(-13.5, -xj - 0.3)
        ivy_strand((x, -dep / 2 - 0.15, hfn(x) - rnd.uniform(0.2, 1.5)), rnd.uniform(3.0, 7.0), seed=140 + k)
    for k in range(4):
        ivy_strand((xj - 0.3 + k * 0.3, -dep / 2 - 0.15, zs - 0.3), rnd.uniform(3.0, 5.0), seed=170 + k)
    moss_skirt(13.0, 51, sx=1.5, sy=0.5, loc=(-1.5, -2.5, 0.0), h=0.4 / 13.0)
    mini_fern(-12.0, -3.6, 0.0, 7, 3.0, 52)
    mini_fern(9.5, 2.8, 0.0, 6, 2.6, 53)
    tuft(-6.5, -6.2, 0.0, rnd, n=8)
    tuft(7.0, -7.0, 0.0, rnd, n=7)
    return finalize('ruin_arch_b', smooth_angle=30)


# ------------------------------------------------------------------ standing stones
def slab(w, h, thick, seed, taper=0.85, flat_top=False, key=STONE):
    """Cut menhir: tapered slab with a slightly rough outline, extruded along Y."""
    rnd = random.Random(seed)
    j = lambda: rnd.uniform(-0.1, 0.1)
    hw = w / 2
    if flat_top:
        pts = [(-hw + j(), 0), (hw + j(), 0), (hw * taper + j(), h * 0.5), (hw * taper * 0.96, h), (-hw * taper * 0.96, h), (-hw * taper + j(), h * 0.5)]
    else:
        pts = [(-hw + j(), 0), (hw + j(), 0), (hw * taper + j(), h * 0.45), (hw * taper * 0.8, h * 0.82), (hw * 0.3 + j(), h), (-hw * 0.35 + j(), h * 0.97),
               (-hw * taper * 0.85, h * 0.8), (-hw * taper + j(), h * 0.45)]
    return prism_xz(pts, -thick / 2, thick / 2, key)


def carved_tree(x, y, z0, z1, rnd, sgn=-1):
    """Carved 'tree of life' relief: trunk line, leaf pairs and a ring at the top."""
    tube(nm('cv'), [(x, y, z0), (x, y, (z0 + z1) / 2), (x, y, z1)], 0.11, WARM, res=4, ures=2)
    n = 5
    for i in range(n):
        z = z0 + (z1 - z0) * (0.28 + 0.14 * i)
        for k in (-1, 1):
            o = ball(nm('cl'), 0.46, (x + k * 0.34, y, z), WARM, segs=6, rings=4, scale=(1.0, 0.18, 0.4))
            o.rotation_euler = (0, k * -0.7, 0)
    torus(nm('cr'), 0.6, 0.07, loc=(x, y, z1 + 0.5), key=WARM, segs=16, rsegs=4, rot=(90, 0, 0))


def standing_stone_a():
    """Trilithon: two carved uprights bridged by a lintel, moss on top, rubble and ferns at the foot."""
    reset()
    rnd = random.Random(806)
    for sx in (-1, 1):
        s = slab(3.9, 11.4, 2.4, 20 + sx, taper=0.86, flat_top=True)
        s.location.x = sx * 4.5
        s.rotation_euler.z = sx * 0.03
        carved_tree(sx * 4.5, -1.28, 1.6, 8.4, rnd)
    lint = prism_xz([(-6.9, 0), (6.9, 0), (6.7, 1.5), (5.4, 1.75), (-5.2, 1.7), (-6.8, 1.5)], -1.35, 1.35, STONE)
    lint.location.z = 11.35
    top_paint(lint, 'ev_moss', 0.55, 3)
    sp = []
    for i in range(30):
        t = i / 29
        a = 0.6 + t * 4 * PI
        r = 0.2 + 0.9 * t
        sp.append((-2.0 + math.cos(a) * r, -1.42, 12.15 + math.sin(a) * r * 0.6))
    tube(nm('spl'), sp, 0.09, WARM, res=4, ures=2)
    sp = [(2.0 + (2.0 - (p[0] + 2.0)) * 1.0, p[1], p[2]) for p in sp]
    tube(nm('spl'), sp, 0.09, WARM, res=4, ures=2)
    for (x, y, r, sd) in ((-8.0, -3.4, 1.4, 5), (7.8, -3.0, 1.2, 6), (0.0, -5.0, 1.0, 7), (9.0, 2.4, 1.0, 8)):
        o = rock(nm('rk'), r, (x, y, r * 0.3), DARK, seed=sd, scale=(1.3, 1.0, 0.6), subdiv=3, amp=0.3)
        top_paint(o, 'ev_moss', 0.5, sd)
    ivy_strand((-5.8, -1.4, 9.0), 5.5, seed=7)
    ivy_strand((5.9, -1.4, 7.6), 4.0, seed=8)
    dress_base(rnd, 8.5, 61)
    return finalize('standing_stone_a', smooth_angle=30)


def standing_stone_b():
    """Stone circle: seven leaning menhirs round a flat altar slab, with flagstones and moss."""
    reset()
    rnd = random.Random(807)
    R = 9.5
    heights = (8.4, 6.2, 7.4, 5.4, 8.0, 6.6, 7.0)
    for i, h in enumerate(heights):
        a = 2 * PI * i / 7 + 0.2
        s = slab(rnd.uniform(2.6, 3.4), h, rnd.uniform(1.5, 2.0), 30 + i, taper=0.82)
        s.location = (math.cos(a) * R, math.sin(a) * R, -0.3)
        s.rotation_euler = (rnd.uniform(-0.05, 0.05), rnd.uniform(-0.07, 0.07), a + PI / 2 + rnd.uniform(-0.15, 0.15))
        top_paint(s, 'ev_moss', 0.55, i, noise_amt=0.3)
    # altar
    box(nm('alt'), (5.6, 3.4, 0.9), loc=(0, 0, 0.45), key=DARK, bev=0.08)
    alt = box(nm('alt'), (4.6, 2.6, 1.3), loc=(0, 0, 1.55), key=STONE, bev=0.08)
    top_paint(alt, 'ev_moss', 0.97, 1, noise_amt=0.0)
    carved_tree(0.0, -1.34, 1.0, 2.0, rnd)
    cyl(nm('bwl'), 0.9, 0.35, loc=(0, 0, 2.2), key=WARM, verts=12, r2=0.55)
    # flagstone path ring
    for i in range(18):
        a = 2 * PI * i / 18
        d = 5.4 + rnd.uniform(-0.3, 0.3)
        box(nm('fl'), (rnd.uniform(1.0, 1.7), rnd.uniform(1.0, 1.5), 0.2), loc=(math.cos(a) * d, math.sin(a) * d, 0.08), key=DARK, rot=(0, 0, math.degrees(a) + rnd.uniform(-20, 20)),
            bev=0.04, segs=1)
    moss_skirt(13.5, 71, h=0.4 / 13.5)
    for k in range(5):
        a = rnd.uniform(0, 2 * PI)
        mini_fern(math.cos(a) * 12.5, math.sin(a) * 12.5, 0.0, 6, 2.6, 72 + k)
    mushrooms(3.4, 5.6, 0.0, 6, seed=5, scale=1.6)
    return finalize('standing_stone_b', smooth_angle=30)


# ------------------------------------------------------------------ carved markers
def marker_a():
    """Waymarker: tapered stone pillar with two arrow-shaped direction stones and a carved leaf."""
    reset()
    rnd = random.Random(808)
    b = box(nm('bs'), (4.2, 4.2, 0.9), loc=(0, 0, 0.45), key=DARK, bev=0.07)
    top_paint(b, 'ev_moss', 0.8, 1, noise_amt=0.2)
    cyl(nm('pil'), 1.75, 5.4, loc=(0, 0, 0.9), key=STONE, verts=4, rot=(0, 0, 45), r2=1.25)
    cyl(nm('cap'), 1.45, 1.5, loc=(0, 0, 6.3), key=WARM, verts=4, rot=(0, 0, 45), r2=0.05)
    ball(nm('bl'), 0.28, (0, 0, 7.9), WARM, segs=6, rings=4)
    box(nm('bnd'), (3.0, 3.0, 0.3), loc=(0, 0, 3.3), key=WARM, bev=0.05, rot=(0, 0, 0))
    arrow = lambda L, sgn: [(0, 0.55), (sgn * L, 0.55), (sgn * (L + 1.3), 0.0), (sgn * L, -0.55), (0, -0.55)]
    s1 = prism_xz(arrow(4.6, 1), -0.4, 0.4, WARM)
    s1.location = (0.3, -1.2, 5.2)
    s2 = prism_xz(list(reversed(arrow(4.0, -1))), -0.4, 0.4, STONE)
    s2.location = (-0.3, -1.2, 4.2)
    s1.rotation_euler.z = 0.03
    leaf_motif(0.0, -1.17, 2.0, 1.2, 0.8)
    for (x, y, r, sd) in ((3.0, -2.2, 0.8, 1), (3.9, -1.4, 0.55, 2), (-3.2, -2.0, 0.7, 3), (-2.4, 2.6, 0.9, 4)):
        o = rock(nm('rk'), r, (x, y, r * 0.3), DARK, seed=sd, scale=(1.3, 1.0, 0.65), subdiv=3, amp=0.3)
        top_paint(o, 'ev_moss', 0.5, sd)
    ivy_strand((-1.0, -1.3, 5.4), 3.0, seed=3)
    dress_base(rnd, 5.4, 91, ferns=False)
    mini_fern(4.2, 2.2, 0.0, 6, 2.2, 92)
    return finalize('marker_a', smooth_angle=30)


def marker_b():
    """Memorial stone: arched slab with a carved tree, an offering bowl, small stones and wild flowers."""
    reset()
    rnd = random.Random(809)
    box(nm('bs'), (6.4, 3.2, 0.7), loc=(0, 0, 0.35), key=DARK, bev=0.07)
    box(nm('bs'), (5.4, 2.6, 0.6), loc=(0, 0, 1.0), key=STONE, bev=0.07)
    pts = [(2.1, 0), (2.0, 4.2)] + [(2.0 * math.cos(PI * i / 12), 4.2 + 2.2 * math.sin(PI * i / 12)) for i in range(1, 12)] + [(-2.0, 4.2), (-2.1, 0)]
    sl = prism_xz(pts, -0.65, 0.65, STONE)
    sl.location.z = 1.3
    top_paint(sl, 'ev_moss', 0.8, 5, noise_amt=0.2)
    # carved tree on the face
    carved_tree(0.0, -0.69, 1.9, 5.4, rnd)
    # offering bowl
    lathe(nm('bowl'), [(0, 0), (0.55, 0), (0.95, 0.35), (1.0, 0.55), (0.88, 0.55), (0.82, 0.38), (0.5, 0.12), (0, 0.12)], loc=(0, -2.9, 0.0), key=STONE, segs=12)
    ball(nm('fr'), 0.28, (0.15, -2.9, 0.45), 'ev_berry_red', segs=6, rings=4)
    ball(nm('fr'), 0.26, (-0.2, -2.8, 0.42), 'ev_berry', segs=6, rings=4)
    for (x, y, r, sd) in ((3.4, -2.0, 0.7, 1), (4.0, -1.1, 0.5, 2), (-3.6, -2.2, 0.8, 3), (-4.2, -1.3, 0.55, 4), (2.2, 2.6, 0.9, 5)):
        o = rock(nm('rk'), r, (x, y, r * 0.3), DARK, seed=sd, scale=(1.3, 1.0, 0.65), subdiv=3, amp=0.3)
        top_paint(o, 'ev_moss', 0.5, sd)
    from v4_d06 import daisy
    for (x, y) in ((-2.6, -3.4), (2.9, -3.5), (-3.6, 0.8), (3.8, 0.9)):
        daisy(x, y, 0.0, rnd.uniform(1.8, 2.8), rnd)
    dress_base(rnd, 5.8, 93, ferns=False)
    mini_fern(-4.6, 3.0, 0.0, 6, 2.4, 94)
    return finalize('marker_b', smooth_angle=30)


# ------------------------------------------------------------------ banners
def wave_y(u, t, y0, amp, freq, phase):
    return y0 + amp * math.sin(freq * u * 2 * PI + phase + t * 2.2) * (0.25 + 0.75 * t)


def cloth(w, H, nx, ny, z_top, y0, amp, key, x0=0.0, t0=0.0, t1=1.0, notch=0.0, taper=0.0, freq=1.0, phase=0.0, thick=0.08, dy=0.0):
    """Hanging cloth with a gentle wave; t0..t1 selects a horizontal band so trims share the same wave."""
    bm = bmesh.new()
    grid = []
    for j in range(ny + 1):
        t = t0 + (t1 - t0) * j / ny
        row = []
        for i in range(nx + 1):
            u = i / nx
            x = x0 + (u - 0.5) * w * (1 - taper * t)
            z = z_top - t * H
            if notch and t1 >= 0.999 and j == ny:
                z += notch * (1 - abs(2 * u - 1))
            row.append(bm.verts.new((x, wave_y(u, t, y0, amp, freq, phase) + dy, z)))
        grid.append(row)
    for j in range(ny):
        for i in range(nx):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    o = _obj_from_bm(nm('cl'), bm, key)
    sol = o.modifiers.new('sol', 'SOLIDIFY')
    sol.thickness = thick
    return o


def emblem(x, y, z, s, key='ev_banner_gold'):
    for k in (-1, 1):
        o = ball(nm('em'), s, (x, y, z), key, segs=7, rings=4, scale=(0.42, 0.12, 1.0))
        o.rotation_euler = (0, k * 0.5, 0)
    torus(nm('emr'), s * 0.95, s * 0.07, loc=(x, y - 0.02, z - s * 0.1), key=key, segs=16, rsegs=4, rot=(90, 0, 0))


def hang_banner(cx, z_bar, w, H, key, trim, y0, amp, phase, notch=1.6, with_emblem=True):
    z_top = z_bar - 0.15
    cloth(w, H, 8, 14, z_top, y0, amp, key, x0=cx, notch=notch, phase=phase)
    cloth(w, H, 8, 2, z_top, y0, amp, trim, x0=cx, t0=0.0, t1=0.09, phase=phase, dy=-0.05, thick=0.1)
    cloth(w, H, 8, 2, z_top, y0, amp, trim, x0=cx, t0=0.62, t1=0.66, phase=phase, dy=-0.05, thick=0.1)
    if with_emblem:
        t = 0.34
        emblem(cx, wave_y(0.5, t, y0, amp, 1.0, phase) - 0.14, z_top - t * H, 1.15, trim)
    for k in range(5):
        u = (k + 0.5) / 5
        box(nm('lp'), (0.26, 0.22, 0.7), loc=(cx + (u - 0.5) * w, y0 + 0.02, z_bar - 0.15), key='ev_wood_dark', segs=1)
    for sgn in (-1, 1):
        ball(nm('ts'), 0.22, (cx + sgn * w * 0.5, wave_y(0.5 + sgn * 0.5, 1.0, y0, amp, 1.0, phase), z_top - H + 0.1), trim, segs=6, rings=4, scale=(1, 1, 1.5))


def banner_a():
    """Standard banner: tall pole, crossbar, a green swallow-tail banner with gold trim and a leaf emblem."""
    reset()
    rnd = random.Random(810)
    b = box(nm('bs'), (3.4, 3.4, 1.5), loc=(0, 0, 0.75), key=DARK, bev=0.07)
    top_paint(b, 'ev_moss', 0.8, 1, noise_amt=0.2)
    cyl(nm('pole'), 0.27, 17.0, loc=(0, 0, 1.4), key='ev_wood_dark', verts=8)
    ball(nm('fin'), 0.55, (0, 0, 18.7), 'bronze', segs=8, rings=5, scale=(1, 1, 1.3))
    cyl(nm('bar'), 0.17, 5.4, loc=(-2.7, 0, 16.0), key='ev_wood_dark', verts=6, rot=(0, 90, 0))
    for sgn in (-1, 1):
        ball(nm('bk'), 0.3, (sgn * 2.75, 0, 16.0), 'bronze', segs=6, rings=4)
    hang_banner(0.0, 16.0, 4.4, 10.0, 'ev_banner_green', 'ev_banner_gold', -0.5, 0.3, 0.4)
    for k in range(3):
        a = 2 * PI * k / 3 + 0.4
        box(nm('rk'), (0.9, 0.9, 0.5), loc=(math.cos(a) * 2.6, math.sin(a) * 2.6, 0.2), key=DARK, rot=(0, 0, math.degrees(a)), bev=0.05, segs=1)
    dress_base(rnd, 4.6, 101)
    return finalize('banner_a', smooth_angle=40)


def banner_b():
    """Gate banners: two posts joined by a beam, a gold and a green banner hanging side by side."""
    reset()
    rnd = random.Random(811)
    for sx in (-1, 1):
        b = box(nm('bs'), (2.8, 2.8, 1.2), loc=(sx * 4.6, 0, 0.6), key=DARK, bev=0.07)
        top_paint(b, 'ev_moss', 0.8, sx + 3, noise_amt=0.2)
        cyl(nm('post'), 0.34, 13.0, loc=(sx * 4.6, 0, 1.2), key='ev_wood_dark', verts=8)
        cyl(nm('pcap'), 0.5, 1.0, loc=(sx * 4.6, 0, 14.2), key='bronze', verts=8, r2=0.05)
    cyl(nm('beam'), 0.24, 9.8, loc=(-4.9, 0, 12.4), key='ev_wood_dark', verts=8, rot=(0, 90, 0))
    for sx in (-1, 1):
        cyl(nm('brc'), 0.12, 2.2, loc=(sx * 4.4, 0, 11.0), key='ev_wood_dark', verts=5, rot=(0, 40 * sx, 0))
    hang_banner(-2.1, 12.4, 3.6, 8.2, 'ev_banner_gold', 'ev_banner_green', -0.45, 0.28, 0.0, notch=1.3)
    hang_banner(2.1, 12.4, 3.6, 8.2, 'ev_banner_green', 'ev_banner_gold', -0.45, 0.28, 1.4, notch=1.3)
    dress_base(rnd, 8.0, 102)
    return finalize('banner_b', smooth_angle=40)


def banner_c():
    """Festival bunting: a rope between two posts hung with green and gold pennants."""
    reset()
    rnd = random.Random(812)
    span = 8.5
    for sx in (-1, 1):
        b = box(nm('bs'), (2.4, 2.4, 1.1), loc=(sx * span, 0, 0.55), key=DARK, bev=0.07)
        top_paint(b, 'ev_moss', 0.8, sx + 3, noise_amt=0.2)
        cyl(nm('post'), 0.3, 11.5, loc=(sx * span, 0, 1.1), key='ev_wood_dark', verts=8)
        ball(nm('fin'), 0.5, (sx * span, 0, 12.9), 'bronze', segs=8, rings=5, scale=(1, 1, 1.3))
    pts = []
    n = 12
    for i in range(n + 1):
        u = i / n
        x = -span + 2 * span * u
        pts.append((x, 0.0, 11.4 - 3.0 * 4 * u * (1 - u)))
    tube(nm('rope'), pts, 0.1, 'ev_thatch', res=4, ures=3)
    keys = (('ev_banner_green', 'ev_banner_gold'), ('ev_banner_gold', 'ev_banner_green'))
    for i in range(9):
        u = (i + 0.5) / 9
        x = -span + 2 * span * u
        z = 11.4 - 3.0 * 4 * u * (1 - u) - 0.1
        k, trim = keys[i % 2]
        cloth(2.0, 3.6, 4, 8, z, -0.1, 0.12, k, x0=x, taper=0.95, phase=i * 0.9, thick=0.07)
        cloth(2.0, 3.6, 4, 1, z, -0.1, 0.12, trim, x0=x, t0=0.0, t1=0.1, taper=0.95, phase=i * 0.9, thick=0.09, dy=-0.05)
    dress_base(rnd, 5.0, 103)
    return finalize('banner_c', smooth_angle=40)


BATCH_D08 = [
    ('D08_01_statue_a', statue_a, (0.8, -1.2, 0.35)),
    ('D08_02_statue_b', statue_b, (0.8, -1.2, 0.35)),
    ('D08_03_statue_c', statue_c, (-1.0, -1.1, 0.3)),
    ('D08_04_ruin_arch_a', ruin_arch_a, (0.7, -1.2, 0.3)),
    ('D08_05_ruin_arch_b', ruin_arch_b, (0.6, -1.2, 0.3)),
    ('D08_06_standing_stone_a', standing_stone_a, (0.6, -1.2, 0.3)),
    ('D08_07_standing_stone_b', standing_stone_b, (0.9, -1.1, 0.55)),
    ('D08_08_marker_a', marker_a, (0.9, -1.2, 0.3)),
    ('D08_09_marker_b', marker_b, (0.9, -1.2, 0.3)),
    ('D08_10_banner_a', banner_a, (0.5, -1.2, 0.2)),
    ('D08_11_banner_b', banner_b, (0.5, -1.2, 0.2)),
    ('D08_12_banner_c', banner_c, (0.5, -1.2, 0.2)),
]
