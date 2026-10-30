"""F. Elf jungle city. Pale wood, white-green stone, leaf-shaped teal roofs, soft glowing magic."""
import math, random
import bmesh
from mathutils import Vector, Matrix
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, top_paint, _obj_from_bm, chain
from arch import F, faces, lbox, lbeam, beam3, slab, lslab, nm, arc_pts, lancet_pts, column_c
from nature import blob, rock, trunk_flare, branch_tree, foliage_at
from capital import star_pts, crystal

W_, WD, ST, STD = 'elf_wood', 'elf_wood_dark', 'elf_stone', 'elf_stone_dark'
LEAVES = ('jleaf_a', 'jleaf_b', 'jleaf_c', 'jleaf_d')


def leaf(p0, d, L, W, key, up=(0, 0, 1), bend=0.3, n=6, fold=0.18, thick=0.06):
    """Curved pointed leaf blade along direction d, drooping by `bend`, with a folded midrib."""
    d = Vector(d).normalized(); up = Vector(up)
    if abs(d.dot(up.normalized())) > 0.95:
        up = Vector((1, 0, 0))
    side = d.cross(up).normalized(); nrm = side.cross(d).normalized()
    bm = bmesh.new()
    rows = []
    for i in range(n + 1):
        t = i / n
        c = Vector(p0) + d * L * t - nrm * (bend * L * t * t)
        w = W * (math.sin(math.pi * min(1.0, t * 1.15)) ** 0.7) if t < 0.999 else 0.0
        rows.append([bm.verts.new(c - side * w + nrm * fold * w), bm.verts.new(c), bm.verts.new(c + side * w + nrm * fold * w)])
    for a, b in zip(rows, rows[1:]):
        bm.faces.new((a[0], a[1], b[1], b[0]))
        bm.faces.new((a[1], a[2], b[2], b[1]))
    o = _obj_from_bm(nm('lf'), bm, key)
    o.modifiers.new('s', 'SOLIDIFY').thickness = thick
    return o


def leaf_roof(cx, cy, z, r, h, keys=('elf_roof', 'elf_roof_b'), petals=8, tip='gold'):
    """Bud-shaped roof: dome with flared leaf-tip eaves and a curled spire."""
    lathe(nm('lr'), [(0.0, z - 0.4), (r + 0.6, z - 0.4), (r + 1.1, z + 0.2), (r * 0.95, z + h * 0.35), (r * 0.6, z + h * 0.7), (r * 0.2, z + h * 0.95), (0.0, z + h)],
          loc=(cx, cy, 0), key=keys[0], segs=petals * 2)
    for i in range(petals):
        a = 2 * math.pi * i / petals
        dvec = Vector((math.cos(a), math.sin(a), -0.35))
        leaf((cx + math.cos(a) * (r + 0.3), cy + math.sin(a) * (r + 0.3), z + 0.1), dvec, r * 0.55, r * 0.22, keys[i % 2], bend=-0.15, n=4)
        pts = [(cx + math.cos(a) * (r + 1.0), cy + math.sin(a) * (r + 1.0), z + 0.2), (cx + math.cos(a) * r * 0.75, cy + math.sin(a) * r * 0.75, z + h * 0.55),
               (cx + math.cos(a) * r * 0.15, cy + math.sin(a) * r * 0.15, z + h * 0.97)]
        tube(nm('rb'), pts, 0.12, 'gold', res=4)
    tube(nm('sp'), [(cx, cy, z + h - 0.2), (cx, cy, z + h + 1.6), (cx + 0.6, cy, z + h + 2.6), (cx + 0.2, cy, z + h + 3.0)], 0.22, tip, res=4, taper=[1, 0.7, 0.4, 0.2])
    ball(nm('gl'), 0.35, loc=(cx, cy, z + h + 1.0), key='glow_cyan', segs=8, rings=6)


def round_window(cx, cy, z, a, r=0.8, R=0.0, key='glow_gold'):
    fr = F(cx + math.cos(a) * R, cy + math.sin(a) * R, 0, math.degrees(a) + 90)
    cyl(nm('rw'), r, 0.12, loc=fr.p(0, -0.02, z), key=key, verts=12, rot=fr.r(90, 0, 0))
    torus(nm('rwf'), r + 0.1, 0.12, loc=fr.p(0, -0.15, z), key='gold', segs=14, rsegs=4, rot=fr.r(90, 0, 0))
    lbox(fr, (0.08, 0.1, r * 2), 0, -0.18, z, 'gold')


def elf_door(fr, x, w=2.6, h=5.0, key=WD):
    zs = h - w * 0.866
    lslab(fr, [(px, 0.05, pz) for px, pz in lancet_pts(x, 0, zs, w)], (0, -0.2, 0), key)
    tube(nm('df'), [fr.p(px, -0.25, pz) for px, pz in lancet_pts(x, 0, zs, w + 0.5)[1:-1]], 0.18, 'gold', res=4)
    ball(nm('dk'), 0.14, loc=fr.p(x + w * 0.3, -0.3, h * 0.42), key='gold', segs=6, rings=4)


def elf_railing(cx, cy, z, r, key=W_, gap=None, n=None):
    n = n or max(10, int(2 * math.pi * r / 1.4))
    pts = []
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        if gap and abs(((a - gap[0] + math.pi) % (2 * math.pi)) - math.pi) < gap[1]:
            if pts:
                tube(nm('rr'), pts, 0.12, key, res=4, ures=2)
                pts = []
            continue
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
        pts.append((x, y, z + 2.0))
        if i < n:
            tube(nm('rp'), [(x, y, z), (x, y, z + 1.0), (x, y, z + 2.0)], 0.07, key, res=4)
    if len(pts) > 1:
        tube(nm('rr'), pts, 0.12, key, res=4, ures=2)


def deck(cx, cy, z, r, inner=0.0, key=W_, gap=None, struts=True):
    if inner:
        lathe(nm('dk'), [(inner, z - 0.4), (r, z - 0.4), (r, z), (inner, z)], loc=(cx, cy, 0), key=key, segs=32)
    else:
        cyl(nm('dk'), r, 0.4, loc=(cx, cy, z - 0.4), key=key, verts=24)
    torus(nm('dke'), r, 0.16, loc=(cx, cy, z - 0.2), key='gold', segs=32, rsegs=4)
    elf_railing(cx, cy, z, r - 0.25, gap=gap)
    if struts:
        n = 6
        ri = inner if inner else r * 0.2
        dz = min(r * 0.9, 6.0)
        for i in range(n):
            a = 2 * math.pi * i / n + 0.3
            tube(nm('st'), [(cx + math.cos(a) * ri, cy + math.sin(a) * ri, z - dz), (cx + math.cos(a) * (ri + (r - ri) * 0.4), cy + math.sin(a) * (ri + (r - ri) * 0.4), z - dz * 0.6),
                            (cx + math.cos(a) * (r - 0.6), cy + math.sin(a) * (r - 0.6), z - 0.4)], 0.22, WD, res=4)


def pod_house(cx, cy, z, r=4.0, h=6.0, wall=W_, roof=('elf_roof', 'elf_roof_b'), door_a=-math.pi / 2, deck_r=None, gap=None):
    if deck_r:
        deck(cx, cy, z, deck_r, gap=gap)
    lathe(nm('pw'), [(0.0, z), (r * 0.85, z), (r, z + h * 0.35), (r * 0.95, z + h * 0.8), (r * 0.85, z + h), (0.0, z + h)], loc=(cx, cy, 0), key=wall, segs=16)
    for k in range(6):
        a = 2 * math.pi * k / 6
        tube(nm('pr'), [(cx + math.cos(a) * r * 0.86, cy + math.sin(a) * r * 0.86, z), (cx + math.cos(a) * r * 1.02, cy + math.sin(a) * r * 1.02, z + h * 0.35),
                        (cx + math.cos(a) * r * 0.87, cy + math.sin(a) * r * 0.87, z + h)], 0.14, WD, res=4)
    fr = F(cx + math.cos(door_a) * r * 0.9, cy + math.sin(door_a) * r * 0.9, z, math.degrees(door_a) + 90)
    elf_door(fr, 0, w=2.4, h=min(5.0, h * 0.8))
    for k in (1, 2, -1, -2):
        a = door_a + k * 1.1
        round_window(cx, cy, z + h * 0.55, a, r=0.65, R=r * 0.98)
    leaf_roof(cx, cy, z + h, r, r * 1.3, keys=roof)


def vine(p0, L, seed=0, leaves=True, key='jleaf_b', sway=0.8):
    rnd = random.Random(seed)
    pts = [Vector(p0)]
    for i in range(1, 6):
        pts.append(Vector((p0[0] + rnd.uniform(-sway, sway), p0[1] + rnd.uniform(-sway, sway), p0[2] - L * i / 5)))
    tube(nm('vn'), [tuple(p) for p in pts], 0.07, 'leaf_dark', res=4, ures=2)
    if leaves:
        for i in range(int(L / 0.9)):
            t = (i + 0.5) / int(L / 0.9)
            k = min(4, int(t * 5))
            p = pts[k].lerp(pts[k + 1], t * 5 - k)
            a = rnd.uniform(0, 6.28)
            leaf(tuple(p), (math.cos(a), math.sin(a), -0.6), rnd.uniform(0.5, 0.8), 0.22, rnd.choice(LEAVES), bend=0.2, n=3, thick=0.04)


def jungle_tree_body(seed, height, r, canopy=1.0, keys=LEAVES, vines=6, flat=0.55, roots=7, nb=5):
    rnd = random.Random(seed)
    trunk_flare(nm('tr'), r, height * 0.7, key='elf_bark', roots=roots, rnd=rnd)
    for i in range(roots):
        a = 2 * math.pi * i / roots + rnd.uniform(-0.2, 0.2)
        tube(nm('bu'), [(math.cos(a) * r * 0.6, math.sin(a) * r * 0.6, height * 0.16), (math.cos(a) * r * 1.4, math.sin(a) * r * 1.4, height * 0.06),
                        (math.cos(a) * r * 2.6, math.sin(a) * r * 2.6, 0.2)], r * 0.32, 'elf_bark_b', res=4, taper=[1, 0.7, 0.35], ures=3)
    tips = []
    top = Vector((0, 0, height * 0.68))
    for k in range(nb):
        az = 2 * math.pi * k / nb + rnd.uniform(-0.3, 0.3)
        d = Vector((math.cos(az), math.sin(az), rnd.uniform(0.35, 0.7)))
        branch_tree(nm('br'), top, d, height * 0.3 * canopy, r * 0.5, 2, rnd, key='elf_bark', spread=28, kids=2, tips=tips, up_bias=0.15)
    foliage_at(nm('fo'), tips, rnd, list(keys), height * 0.1 * canopy, height * 0.15 * canopy, extra=4, centre=(0, 0, height * 0.86),
               cr=height * 0.32 * canopy, flat=flat)
    for i in range(vines):
        p, _ = tips[rnd.randrange(len(tips))]
        vine((p.x, p.y, p.z - 1.0), rnd.uniform(height * 0.2, height * 0.45), seed=seed + i)
    return tips


# ============================================================ centrepiece and tree homes
def world_tree():
    """F1 - giant world tree: 150-stud trunk with buttress roots, glowing hollow door, huge layered canopy, platforms and lanterns."""
    reset()
    rnd = random.Random(1)
    H, R = 150.0, 13.0
    lathe(nm('wt'), [(0.0, -0.5), (R * 1.9, -0.5), (R * 1.45, 4.0), (R * 1.1, 14.0), (R, 40.0), (R * 0.82, 80.0), (R * 0.7, 110.0), (R * 0.55, H * 0.82), (0.0, H * 0.82)],
          key='elf_bark', segs=24)
    for i in range(14):
        a = 2 * math.pi * i / 14 + rnd.uniform(-0.1, 0.1)
        tube(nm('rib'), [(math.cos(a) * R * 1.5, math.sin(a) * R * 1.5, 3.0), (math.cos(a) * R * 1.05, math.sin(a) * R * 1.05, 30.0),
                         (math.cos(a + 0.5) * R * 0.85, math.sin(a + 0.5) * R * 0.85, 75.0), (math.cos(a + 0.9) * R * 0.62, math.sin(a + 0.9) * R * 0.62, 112.0)],
             R * 0.16, 'elf_bark_b', res=4, taper=[1, 0.9, 0.7, 0.5], ures=3)
    for i in range(9):
        a = 2 * math.pi * i / 9 + rnd.uniform(-0.2, 0.2)
        L = rnd.uniform(26, 38)
        tube(nm('rt'), [(math.cos(a) * R * 0.9, math.sin(a) * R * 0.9, 16.0), (math.cos(a) * R * 1.7, math.sin(a) * R * 1.7, 7.0),
                        (math.cos(a) * (R + L * 0.6), math.sin(a) * (R + L * 0.6), 2.2), (math.cos(a) * (R + L), math.sin(a) * (R + L), 0.3)],
             R * 0.28, 'elf_bark', res=6, taper=[1, 0.8, 0.5, 0.22], ures=3)
    fr = F(0, -R * 1.25, 0, 0)
    lslab(fr, [(px, -0.2, pz) for px, pz in lancet_pts(0, 0, 9.0, 8.0)], (0, -0.3, 0), 'glow_gold')
    tube(nm('hd'), [fr.p(px, -0.7, pz) for px, pz in lancet_pts(0, 0, 9.0, 9.4)[1:-1]], 0.6, 'gold', res=4)
    for k in range(6):
        box(nm('stp'), (12.0 - k * 1.2, 1.6, 0.5), loc=(0, -R * 1.25 - 9.0 + k * 1.4, 0.25 + k * 0.45), key=ST, bev=0.06)
    tips = []
    top = Vector((0, 0, H * 0.78))
    for k in range(7):
        az = 2 * math.pi * k / 7 + rnd.uniform(-0.2, 0.2)
        d = Vector((math.cos(az), math.sin(az), rnd.uniform(0.25, 0.55)))
        branch_tree(nm('mb'), top, d, rnd.uniform(48, 60), R * 0.42, 2, rnd, key='elf_bark', spread=26, kids=2, tips=tips, up_bias=0.12)
    tube(nm('ld'), [(0, 0, H * 0.78), (0, 0, H * 0.95)], R * 0.4, 'elf_bark', res=6, taper=[1, 0.5])
    tips.append((Vector((0, 0, H * 0.97)), 1))
    foliage_at(nm('cn'), tips, rnd, list(LEAVES), 13.0, 19.0, extra=10, centre=(0, 0, H * 0.9), cr=55.0, flat=0.5)
    for i in range(26):
        p, _ = tips[rnd.randrange(len(tips))]
        ball(nm('fl'), rnd.uniform(0.6, 1.1), loc=(p.x + rnd.uniform(-8, 8), p.y + rnd.uniform(-8, 8), p.z - rnd.uniform(4, 8)), key=rnd.choice(['glow_cyan', 'glow_green', 'glow_gold']),
             segs=8, rings=6)
    for i in range(14):
        p, _ = tips[rnd.randrange(len(tips))]
        vine((p.x, p.y, p.z - 6.0), rnd.uniform(18, 34), seed=i, leaves=(i % 2 == 0))
    deck(0, 0, 58.0, R * 0.9 + 7.0, inner=R * 0.84, gap=None)
    deck(0, 0, 96.0, R * 0.75 + 6.0, inner=R * 0.72)
    for zz, rr in ((58.0, R * 0.9 + 6.6), (96.0, R * 0.75 + 5.6)):
        for i in range(8):
            a = 2 * math.pi * i / 8
            hanging_lantern_at(math.cos(a) * rr, math.sin(a) * rr, zz + 6.5)
            cyl(nm('lp'), 0.12, 6.5, loc=(math.cos(a) * rr, math.sin(a) * rr, zz), key='gold', verts=6)
    return finalize('world_tree', smooth_angle=35)


def hanging_lantern_at(x, y, z, s=1.0):
    tube(nm('hk'), [(x, y, z), (x, y, z - 0.8 * s)], 0.05, 'gold', res=4)
    lathe(nm('hl'), [(0, 0), (0.3 * s, 0.3 * s), (0.5 * s, 0.9 * s), (0.4 * s, 1.4 * s), (0, 1.6 * s)], loc=(x, y, z - 2.4 * s), key='glow_cyan', segs=8)
    for k in range(4):
        a = math.pi / 2 * k
        tube(nm('hc'), [(x + math.cos(a) * 0.32 * s, y + math.sin(a) * 0.32 * s, z - 2.1 * s), (x + math.cos(a) * 0.55 * s, y + math.sin(a) * 0.55 * s, z - 1.5 * s),
                        (x, y, z - 0.8 * s)], 0.04 * s, 'gold', res=4)
    lathe(nm('ht'), [(0, 0), (0.2 * s, 0), (0, -0.6 * s)], loc=(x, y, z - 2.4 * s), key='gold', segs=6)


def treehouse(seed, name, height, r, pods, keys=LEAVES):
    reset()
    rnd = random.Random(seed)
    jungle_tree_body(seed, height, r, canopy=0.9, keys=keys, vines=5)
    for (a, zf, pr, ph) in pods:
        R = r * 0.9 + pr + 0.6
        cx, cy = math.cos(a) * R, math.sin(a) * R
        z = height * zf
        pod_house(cx, cy, z, r=pr, h=ph, door_a=a + math.pi * 0.5 if abs(math.sin(a)) > 0.5 else -math.pi / 2, deck_r=pr + 2.2)
        tube(nm('br'), [(math.cos(a) * r * 0.6, math.sin(a) * r * 0.6, z - 4.0), (math.cos(a) * (r + 1.0), math.sin(a) * (r + 1.0), z - 2.0), (cx, cy, z - 0.8)], 0.5, 'elf_bark', res=4)
    return finalize(name, smooth_angle=35)


def treehouse_1():
    """F2 - treehouse: one large pod house on a ring deck, 44-stud jungle tree."""
    return treehouse(2, 'treehouse_1', 44, 3.4, [(-math.pi / 2, 0.36, 5.4, 7.0)])


def treehouse_2():
    """F3 - treehouse: two pods at different heights."""
    return treehouse(3, 'treehouse_2', 52, 3.8, [(-math.pi / 2, 0.26, 5.0, 6.4), (math.pi * 0.25, 0.5, 4.2, 5.6)])


def treehouse_3():
    """F4 - treehouse: three pods stacked around a tall trunk."""
    return treehouse(4, 'treehouse_3', 60, 3.8, [(-math.pi / 2, 0.2, 4.4, 5.8), (math.pi * 0.15, 0.4, 4.0, 5.4), (math.pi * 0.85, 0.56, 3.8, 5.0)])


def treehouse_4():
    """F5 - treehouse: wide family pod low on a squat broad tree."""
    return treehouse(5, 'treehouse_4', 38, 4.4, [(-math.pi / 2, 0.3, 6.6, 7.6)], keys=('jleaf_c', 'jleaf_a', 'jleaf_d'))


def platform_ring():
    """F6 - platform ring that wraps a trunk (inner radius 6, outer 14), railing, struts and lanterns."""
    reset()
    deck(0, 0, 8.0, 14.0, inner=6.0, gap=(-math.pi / 2, 0.25))
    for i in range(6):
        a = 2 * math.pi * i / 6 + 0.5
        hanging_lantern_at(math.cos(a) * 13.6, math.sin(a) * 13.6, 14.0)
        cyl(nm('lp'), 0.12, 6.0, loc=(math.cos(a) * 13.6, math.sin(a) * 13.6, 8.0), key='gold', verts=6)
    rnd = random.Random(6)
    for i in range(8):
        a = rnd.uniform(0, 6.28)
        vine((math.cos(a) * 13.5, math.sin(a) * 13.5, 7.6), rnd.uniform(3, 6), seed=i, leaves=True)
    return finalize('platform_ring', smooth_angle=35)


def rope_bridge(name, L, sag, W=4.0):
    reset()
    rnd = random.Random(int(L))
    n = int(L / 0.8)
    def zf(t): return -sag * 4 * t * (1 - t)
    for i in range(n):
        t = (i + 0.5) / n
        x = -L / 2 + L * t
        box(nm('pl'), (0.62, W, 0.18), loc=(x, 0, zf(t)), key=rnd.choice([W_, WD, W_]), rot=(rnd.uniform(-2, 2), math.degrees(math.atan(sag * 4 * (1 - 2 * t) / L)), rnd.uniform(-2, 2)))
    for s in (-1, 1):
        y = s * (W / 2 + 0.1)
        tube(nm('rb'), [(-L / 2 + L * k / 10, y, zf(k / 10) - 0.15) for k in range(11)], 0.08, 'rope', res=4, ures=2)
        tube(nm('rt'), [(-L / 2 + L * k / 10, y, zf(k / 10) * 0.75 + 2.8) for k in range(11)], 0.1, 'rope', res=4, ures=2)
        for k in range(1, 20):
            t = k / 20
            x = -L / 2 + L * t
            tube(nm('rv'), [(x, y, zf(t) - 0.1), (x, y, zf(t) * 0.75 + 2.8)], 0.04, 'rope', res=4)
            if k % 4 == 0:
                leaf((x, y, zf(t) * 0.75 + 2.8), (rnd.uniform(-1, 1), s * 0.3, -0.8), 0.9, 0.25, rnd.choice(LEAVES), n=3, thick=0.04)
        for e in (-1, 1):
            cyl(nm('ps'), 0.3, 4.2, loc=(e * L / 2, y, -1.0), key=WD, verts=8)
            ball(nm('pb'), 0.38, loc=(e * L / 2, y, 3.3), key='gold', segs=8, rings=6)
    return finalize(name, smooth_angle=35)


def rope_bridge_short():
    """F7 - short rope bridge, 16 long, slight sag."""
    return rope_bridge('rope_bridge_short', 16.0, 0.8)


def rope_bridge_long():
    """F8 - long sagging rope bridge, 48 long."""
    return rope_bridge('rope_bridge_long', 48.0, 5.0)


def spiral_stair():
    """F9 - spiral stair that winds around a trunk (inner radius 5.5), one and a half turns, 30 tall, rail and lanterns."""
    reset()
    n, Rin, Rout, H = 48, 5.5, 9.0, 30.0
    rnd = random.Random(9)
    rail = []
    for i in range(n):
        t = i / n
        a = t * 3 * math.pi
        z = t * H
        rm = (Rin + Rout) / 2
        box(nm('st'), (Rout - Rin, 1.6, 0.35), loc=(math.cos(a) * rm, math.sin(a) * rm, z), key=rnd.choice([W_, W_, WD]), rot=(0, 0, math.degrees(a)))
        tube(nm('sb'), [(math.cos(a) * Rin, math.sin(a) * Rin, z - 1.6), (math.cos(a) * (Rin + 1.4), math.sin(a) * (Rin + 1.4), z - 0.4)], 0.14, WD, res=4)
        rail.append((math.cos(a) * (Rout - 0.2), math.sin(a) * (Rout - 0.2), z + 2.2))
        if i % 2 == 0:
            tube(nm('rp'), [(math.cos(a) * (Rout - 0.2), math.sin(a) * (Rout - 0.2), z), rail[-1]], 0.07, W_, res=4)
        if i % 12 == 6:
            hanging_lantern_at(rail[-1][0], rail[-1][1], z + 4.4, s=0.8)
            tube(nm('lpp'), [(rail[-1][0], rail[-1][1], z), (rail[-1][0], rail[-1][1], z + 4.4)], 0.08, 'gold', res=4)
    tube(nm('rl'), rail, 0.12, 'gold', res=4, ures=2)
    return finalize('spiral_stair', smooth_angle=35)


# ============================================================ palace and sacred places
def elf_palace():
    """F10 - elf palace / temple: tiered white-green stone halls, crescent arches, slender spires with bud roofs and glowing water channels."""
    reset()
    rnd = random.Random(10)
    for k, (r, h) in enumerate(((26.0, 3.0), (21.0, 3.0), (17.0, 2.0))):
        lathe(nm('tr'), [(0.0, sum(x[1] for x in ((26.0, 3.0), (21.0, 3.0), (17.0, 2.0))[:k])), (r, sum(x[1] for x in ((26.0, 3.0), (21.0, 3.0), (17.0, 2.0))[:k])),
                         (r, sum(x[1] for x in ((26.0, 3.0), (21.0, 3.0), (17.0, 2.0))[:k + 1])), (0.0, sum(x[1] for x in ((26.0, 3.0), (21.0, 3.0), (17.0, 2.0))[:k + 1]))],
              key=ST if k % 2 == 0 else STD, segs=12)
        torus(nm('ch'), r - 1.0, 0.45, loc=(0, 0, sum(x[1] for x in ((26.0, 3.0), (21.0, 3.0), (17.0, 2.0))[:k + 1]) + 0.05), key='moon_water', segs=36, rsegs=4)
    z0 = 8.0
    lathe(nm('hall'), [(0.0, z0), (13.0, z0), (13.5, z0 + 2.0), (12.5, z0 + 16.0), (13.6, z0 + 17.0), (0.0, z0 + 17.0)], key=ST, segs=16)
    for i in range(16):
        a = 2 * math.pi * (i + 0.5) / 16
        fr = F(math.cos(a) * 12.9, math.sin(a) * 12.9, 0, math.degrees(a) + 90)
        lslab(fr, [(px, -0.02, pz) for px, pz in lancet_pts(0, z0 + 3.0, z0 + 10.5, 2.4)], (0, -0.12, 0), 'glow_cyan' if i % 4 == 0 else 'glass_dark')
        tube(nm('wf'), [fr.p(px, -0.2, pz) for px, pz in lancet_pts(0, z0 + 3.0, z0 + 10.5, 2.8)[1:-1]], 0.16, 'gold', res=4)
    for i in range(12):
        a = 2 * math.pi * i / 12
        column_c(math.cos(a) * 15.0, math.sin(a) * 15.0, z0, 15.0, 0.6, key=ST, base='gold')
        tube(nm('ca'), [(math.cos(a) * 15.0, math.sin(a) * 15.0, z0 + 15.0), (math.cos(a + math.pi / 12) * 15.6, math.sin(a + math.pi / 12) * 15.6, z0 + 13.6),
                        (math.cos(a + math.pi / 6) * 15.0, math.sin(a + math.pi / 6) * 15.0, z0 + 15.0)], 0.3, ST, res=4)
    lathe(nm('ent'), [(0.0, z0 + 15.0), (16.4, z0 + 15.0), (16.4, z0 + 17.4), (0.0, z0 + 17.4)], key=STD, segs=24)
    leaf_roof(0, 0, z0 + 17.4, 13.0, 18.0, petals=12)
    fr = F(0, -15.0, z0, 0)
    elf_door(fr, 0, w=5.0, h=10.0)
    for k in range(8):
        box(nm('stp'), (10.0, 1.6, 1.0), loc=(0, -27.0 + k * 1.6, 0.5 + k * 1.0), key=ST if k % 2 else STD, bev=0.05)
    for i in range(6):
        a = 2 * math.pi * i / 6 + math.pi / 6
        x, y = math.cos(a) * 21.0, math.sin(a) * 21.0
        sh = 26.0 + (i % 2) * 10.0
        lathe(nm('tw'), [(0.0, 6.0), (2.6, 6.0), (2.2, 8.0), (1.8, 6.0 + sh), (2.4, 6.0 + sh + 0.6), (0.0, 6.0 + sh + 0.6)], loc=(x, y, 0), key=ST, segs=12)
        for zz in (14.0, 22.0):
            torus(nm('twb'), 2.0, 0.15, loc=(x, y, zz), key='gold', segs=16, rsegs=4)
        round_window(x, y, 6.0 + sh - 3.0, math.atan2(y, x), r=0.6, R=1.85, key='glow_cyan')
        leaf_roof(x, y, 6.0 + sh + 0.6, 2.4, 6.0, petals=6)
        tube(nm('fl'), [(x, y, 6.0 + sh + 6.0), (x * 0.5, y * 0.5, z0 + 26.0)], 0.05, 'gold', res=4) if False else None
    for i in range(8):
        a = rnd.uniform(0, 6.28)
        vine((math.cos(a) * 12.6, math.sin(a) * 12.6, z0 + 16.5), rnd.uniform(5, 10), seed=100 + i)
    for i in range(14):
        a = rnd.uniform(0, 6.28)
        blob(nm('bush'), rnd.uniform(1.0, 1.8), (math.cos(a) * 24.0, math.sin(a) * 24.0, 3.0), rnd.choice(LEAVES), subdiv=2, amp=0.2, scale=(1.2, 1.2, 0.8), seed=i)
    return finalize('elf_palace', smooth_angle=30)


def moon_pool():
    """F11 - sacred moon pool: round glowing pool, carved stone rim, crescent-moon arch, lotus and standing stones."""
    reset()
    R = 10.0
    lathe(nm('rim'), [(0.0, 0.0), (R + 2.0, 0.0), (R + 2.0, 1.2), (R + 1.4, 1.6), (R, 1.6), (R, 0.6), (0.0, 0.6)], key=ST, segs=32)
    cyl(nm('w'), R, 0.05, loc=(0, 0, 1.2), key='moon_water', verts=32)
    for i in range(24):
        a = 2 * math.pi * i / 24
        box(nm('rs'), (1.2, 2.0, 0.3), loc=(math.cos(a) * (R + 1.0), math.sin(a) * (R + 1.0), 1.65), key=STD if i % 2 else ST, rot=(0, 0, math.degrees(a)), bev=0.05)
    pts = [(math.cos(math.radians(t)) * 7.0, R + 0.6, 1.6 + math.sin(math.radians(t)) * 9.0) for t in range(0, 181, 15)]
    pts_in = [(math.cos(math.radians(t)) * 5.0, R + 0.6, 2.6 + math.sin(math.radians(t)) * 7.0 + 1.0) for t in range(0, 181, 15)]
    lslab(F(), pts + list(reversed(pts_in)), (0, 1.0, 0), ST)
    tube(nm('mt'), [(x, y - 0.1, z) for x, y, z in pts], 0.18, 'gold', res=4)
    for i in range(9):
        t = math.radians(20 * i)
        ball(nm('ms'), 0.25, loc=(math.cos(t) * 6.0, R + 0.4, 2.6 + math.sin(t) * 8.0), key='glow_cyan', segs=8, rings=6)
    for i in range(5):
        a = math.radians(200 + i * 35)
        x, y = math.cos(a) * (R + 4.0), math.sin(a) * (R + 4.0)
        h = 6.0 + (i % 2) * 2.0
        lathe(nm('ss'), [(0, 0), (1.0, 0), (0.8, h * 0.7), (0.4, h), (0, h + 0.3)], loc=(x, y, 0), key=STD, segs=5)
        for k in range(3):
            box(nm('rn'), (0.5, 0.05, 0.2), loc=(x + math.cos(a) * 0.9 * (1 - k * 0.08), y + math.sin(a) * 0.9 * (1 - k * 0.08), 2.0 + k * 1.2), key='glow_cyan',
                rot=(0, 0, math.degrees(a) + 90))
    rnd = random.Random(11)
    for i in range(6):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(2, R - 2)
        lotus_at(math.cos(a) * d, math.sin(a) * d, 1.25, s=0.8, seed=i)
    return finalize('moon_pool', smooth_angle=35)


def lotus_at(x, y, z, s=1.0, seed=0, glow=True):
    rnd = random.Random(seed)
    cyl(nm('pad'), 1.4 * s, 0.06, loc=(x + 0.8 * s, y, z), key='jleaf_a', verts=16)
    for ring, (n, L, tilt) in enumerate(((8, 0.9, 0.5), (6, 0.7, 1.1))):
        for k in range(n):
            a = 2 * math.pi * k / n + ring * 0.3
            leaf((x, y, z + 0.1), (math.cos(a), math.sin(a), tilt), L * s, 0.32 * s, 'fl_pink' if ring == 0 else 'fl_white', bend=-0.2, n=3, thick=0.04)
    ball(nm('lc'), 0.2 * s, loc=(x, y, z + 0.35 * s), key='glow_gold' if glow else 'fl_yellow', segs=8, rings=6)
    bx, by = x - 1.1 * s, y + 0.7 * s
    tube(nm('bs'), [(bx, by, z), (bx + 0.1 * s, by, z + 0.6 * s)], 0.05 * s, 'jleaf_c', res=4)
    ball(nm('bd'), 0.22 * s, scale=(1, 1, 1.7), loc=(bx + 0.1 * s, by, z + 0.85 * s), key='fl_pink', segs=8, rings=6)


def carved_arch():
    """F12 - carved archway gate: two living trunks bend into a pointed arch, carved leaf panels, gold crest and lanterns."""
    reset()
    rnd = random.Random(12)
    W, H = 14.0, 20.0
    for s in (-1, 1):
        pts = [(s * W / 2, 0, 0.0), (s * W / 2 * 1.02, 0, 6.0), (s * W / 2 * 0.9, 0, 12.0), (s * W / 4, 0, 17.5), (0, 0, H)]
        tube(nm('tk'), pts, 1.4, 'elf_bark', res=6, taper=[1.4, 1.0, 0.85, 0.6, 0.5], ures=4)
        tube(nm('tk2'), [(p[0] * 1.05, 0.9, p[2]) for p in pts[:4]], 0.5, 'elf_bark_b', res=4, taper=[1, 0.8, 0.6, 0.3], ures=3)
        for i in range(3):
            a = rnd.uniform(0, 6.28)
            tube(nm('rt'), [(s * W / 2, 0, 1.0), (s * W / 2 + math.cos(a) * 2.5, math.sin(a) * 2.5, 0.4), (s * W / 2 + math.cos(a) * 4.0, math.sin(a) * 4.0, 0.0)],
                 0.6, 'elf_bark', res=4, taper=[1, 0.6, 0.3])
        box(nm('pn'), (2.6, 1.0, 9.0), loc=(s * W / 2, -1.0, 5.5), key=ST, bev=0.1)
        for k in range(4):
            leaf((s * W / 2, -1.6, 2.5 + k * 2.0), (s * 0.3, -0.2, 1.0), 1.6, 0.6, 'gold', bend=0.2, n=4, thick=0.08)
        hanging_lantern_at(s * W * 0.3, -0.4, 15.0)
    lslab(F(0, -1.2, H - 1.4, 0), [(px * 0.9, 0, pz * 0.9 + 0.2) for px, pz in star_pts(0.6, 1.8, 6)], (0, -0.2, 0), 'gold')
    ball(nm('cg'), 0.6, loc=(0, -1.6, H - 1.2), key='glow_cyan', segs=10, rings=7)
    tips = [(Vector((s * 3.0, 0, H - 1.0)), 0.3) for s in (-1, 0, 1)] + [(Vector((s * 6.0, 0, 13.0)), 0.3) for s in (-1, 1)]
    foliage_at(nm('al'), tips, rnd, list(LEAVES), 2.0, 3.0, flat=0.7)
    for i in range(5):
        vine((rnd.uniform(-5, 5), rnd.uniform(-0.5, 0.5), rnd.uniform(14, 18)), rnd.uniform(4, 8), seed=i)
    return finalize('carved_arch', smooth_angle=35)


def elf_statue():
    """F13 - elf statue (original design): slender robed elf archer with long ears, drawn bow and leaf circlet, on a round plinth."""
    reset()
    lathe(nm('pl'), [(0.0, 0.0), (3.4, 0.0), (3.4, 0.8), (2.8, 1.2), (2.4, 3.6), (2.9, 4.0), (2.9, 4.5), (0.0, 4.5)], key=ST, segs=16)
    torus(nm('plb'), 2.6, 0.12, loc=(0, 0, 2.4), key='gold', segs=24, rsegs=4)
    Z, k = 4.5, 'elf_stone'
    lathe(nm('rb'), [(0.0, Z), (1.5, Z), (1.25, Z + 1.5), (0.9, Z + 4.5), (0.8, Z + 6.0), (1.05, Z + 7.6), (0.7, Z + 8.3), (0.0, Z + 8.4)], key=k, segs=16, sy=0.75)
    for i in range(8):
        a = 2 * math.pi * i / 8
        tube(nm('fd'), [(math.cos(a) * 1.45, math.sin(a) * 1.05, Z + 0.1), (math.cos(a) * 0.9, math.sin(a) * 0.65, Z + 4.6)], 0.1, k, res=4, taper=[1, 0.3])
    from props import cloth
    cloth(nm('cp'), 2.6, 7.4, (0, 0.85, Z + 8.0), k, waves=1.6, amp=0.2, seed=13)
    cyl(nm('nk'), 0.25, 0.5, loc=(0, 0, Z + 8.3), key=k, verts=10)
    ball(nm('hd'), 0.55, loc=(0, -0.05, Z + 9.3), key=k, segs=12, rings=8, scale=(0.9, 1.0, 1.15))
    for s in (-1, 1):
        lathe(nm('ear'), [(0, 0), (0.18, 0), (0.05, 0.9), (0, 1.0)], loc=(s * 0.48, 0.05, Z + 9.4), key=k, segs=5, rot=(0, s * 62, 0))
    tube(nm('hair'), [(0, 0.3, Z + 9.6), (0, 0.8, Z + 8.6), (0, 0.9, Z + 7.0)], 0.35, k, res=4, taper=[1, 0.8, 0.3])
    torus(nm('cir'), 0.55, 0.07, loc=(0, -0.05, Z + 9.7), key='gold', segs=16, rsegs=4)
    for i in range(5):
        a = math.radians(-60 + i * 30)
        leaf((math.sin(a) * 0.55, -math.cos(a) * 0.55, Z + 9.75), (math.sin(a) * 0.3, -math.cos(a) * 0.3, 1.0), 0.45, 0.14, 'gold', bend=0.2, n=3, thick=0.04)
    tube(nm('la'), [(-0.95, 0, Z + 7.6), (-1.9, -0.6, Z + 8.0), (-2.8, -1.0, Z + 8.3)], 0.22, k, res=6)
    tube(nm('ra'), [(0.95, 0, Z + 7.6), (0.9, -0.4, Z + 7.6), (-0.6, -0.8, Z + 8.3)], 0.22, k, res=6)
    bow = [(-2.9, -1.0 + 0.3 * math.sin(math.radians(t)) - 0.3, Z + 8.3 + 4.0 * math.cos(math.radians(t))) for t in range(-90 + 15, 91 - 15, 15)]
    bow = [(-2.9 - 1.4 * math.cos(math.radians(t)) * 0 , -1.0 - 1.2 * math.cos(math.radians(t)), Z + 8.3 + 3.6 * math.sin(math.radians(t))) for t in range(-80, 81, 20)]
    tube(nm('bow'), bow, 0.12, 'gold', res=4, ures=2)
    tube(nm('str'), [bow[0], (-0.6, -0.8, Z + 8.3), bow[-1]], 0.03, 'fl_white', res=4, ures=1)
    beam3((-0.6, -0.8, Z + 8.3), (-3.6, -1.15, Z + 8.3), 0.08, 0.08, 'elf_wood')
    lathe(nm('ah'), [(0, 0), (0.15, 0), (0, 0.5)], loc=(-3.6, -1.15, Z + 8.3), key='gold', segs=4, rot=(0, -90, 0))
    for i in range(6):
        a = 2 * math.pi * i / 6
        leaf((math.cos(a) * 3.0, math.sin(a) * 3.0, 0.0), (math.cos(a) * 0.5, math.sin(a) * 0.5, 1.0), 2.0, 0.6, LEAVES[i % 4], bend=0.4, n=4)
    return finalize('elf_statue', smooth_angle=40)


# ============================================================ jungle plants
def jungle_tree_1():
    """F14 - tall jungle tree: 70 studs, buttress roots, broad flat canopy and vines."""
    reset()
    jungle_tree_body(14, 70, 3.2, canopy=1.0, flat=0.5)
    return finalize('jungle_tree_1', smooth_angle=40)


def jungle_tree_2():
    """F15 - banyan jungle tree: 40 studs, wide low canopy held up by aerial prop roots dropping to the ground."""
    reset()
    rnd = random.Random(150)
    tips = jungle_tree_body(15, 40, 2.8, canopy=1.25, flat=0.8, keys=('jleaf_c', 'jleaf_a', 'jleaf_b'), vines=3, roots=5, nb=6)
    far = sorted(tips, key=lambda t: -(t[0].x ** 2 + t[0].y ** 2))[:10]
    for i, (p, _) in enumerate(far):
        base = (p.x * 0.85 + rnd.uniform(-1, 1), p.y * 0.85 + rnd.uniform(-1, 1), 0.0)
        tube(nm('pr'), [(p.x, p.y, p.z - 1.5), (p.x * 0.92, p.y * 0.92, p.z * 0.5), base], rnd.uniform(0.35, 0.6), 'elf_bark_b', res=5, taper=[0.6, 0.85, 1.2], ures=3)
        for k in range(3):
            a = rnd.uniform(0, 6.28)
            tube(nm('pf'), [(base[0], base[1], 1.2), (base[0] + math.cos(a) * 1.4, base[1] + math.sin(a) * 1.4, 0.0)], 0.22, 'elf_bark_b', res=4, taper=[1, 0.4])
        if i % 3 == 0:
            tube(nm('ar'), [(p.x + 0.6, p.y, p.z - 1.0), (p.x + 0.7, p.y + 0.2, p.z * 0.6)], 0.08, 'elf_bark_b', res=3, taper=[1, 0.3])
    return finalize('jungle_tree_2', smooth_angle=40)


def jungle_palm():
    """F16 - jungle palm: curved ringed trunk, crown of long drooping fronds, coconuts."""
    reset()
    rnd = random.Random(16)
    H = 34.0
    pts = [(0, 0, 0), (1.5, 0, H * 0.35), (4.0, 0, H * 0.7), (6.5, 0, H)]
    tube(nm('pt'), pts, 1.0, 'elf_bark', res=6, taper=[1.3, 1.0, 0.85, 0.7], ures=6)
    for i in range(18):
        t = i / 17
        p = Vector(pts[0]).lerp(Vector(pts[1]), min(1, t * 3)) if t < 0.33 else (Vector(pts[1]).lerp(Vector(pts[2]), min(1, (t - 0.33) * 3)) if t < 0.66 else Vector(pts[2]).lerp(Vector(pts[3]), (t - 0.66) * 3))
        torus(nm('ring'), 1.05 - t * 0.25, 0.12, loc=tuple(p), key='elf_bark_b', segs=12, rsegs=3)
    top = Vector(pts[-1])
    for k in range(12):
        a = 2 * math.pi * k / 12 + rnd.uniform(-0.1, 0.1)
        d = (math.cos(a), math.sin(a), rnd.uniform(0.0, 0.5))
        base = top + Vector((0, 0, 0.4))
        tube(nm('rc'), [tuple(base), tuple(base + Vector(d) * 6.0 + Vector((0, 0, -1.0))), tuple(base + Vector(d) * 11.0 + Vector((0, 0, -5.0)))], 0.12, 'jleaf_b', res=4)
        for j in range(9):
            t = (j + 1) / 10
            q = base + Vector(d) * 11.0 * t + Vector((0, 0, -5.0 * t * t))
            side = Vector(d).cross(Vector((0, 0, 1))).normalized()
            for s in (-1, 1):
                leaf(tuple(q), tuple(side * s + Vector((0, 0, -0.6)) + Vector(d) * 0.4), 2.6 * (1 - t * 0.5), 0.28, LEAVES[(k + j) % 4], bend=0.25, n=3, thick=0.04)
    for k in range(4):
        a = 2 * math.pi * k / 4
        ball(nm('cc'), 0.55, loc=(top.x + math.cos(a) * 0.8, top.y + math.sin(a) * 0.8, top.z - 0.4), key='elf_bark_b', segs=8, rings=6)
    return finalize('jungle_palm', smooth_angle=40)


def root_arch():
    """F17 - giant root arch: massive mossy roots looping overhead to form a natural gateway."""
    reset()
    rnd = random.Random(17)
    for k in range(4):
        y = -3.0 + k * 2.0
        span = 22.0 + rnd.uniform(-3, 3)
        h = 16.0 + rnd.uniform(-2, 3)
        pts = [(-span / 2 - 3, y, -0.3), (-span / 2, y + rnd.uniform(-1, 1), 6.0), (-span / 4, y, h * 0.9), (0, y + rnd.uniform(-1, 1), h), (span / 4, y, h * 0.85),
               (span / 2, y + rnd.uniform(-1, 1), 5.0), (span / 2 + 3, y, -0.3)]
        tube(nm('ra'), pts, rnd.uniform(1.2, 1.8), rnd.choice(['elf_bark', 'elf_bark_b']), res=6, taper=[1.6, 1.2, 0.9, 0.8, 0.9, 1.2, 1.6], ures=4)
    for i in range(10):
        x = rnd.uniform(-10, 10)
        blob(nm('ms'), rnd.uniform(1.0, 1.8), (x, rnd.uniform(-3, 3), 15.5 - abs(x) * 0.5), 'moss_bright', subdiv=2, amp=0.2, scale=(1.4, 1.0, 0.5), seed=i)
    for i in range(8):
        vine((rnd.uniform(-8, 8), rnd.uniform(-3, 3), 14.0), rnd.uniform(5, 10), seed=i + 20)
    for s in (-1, 1):
        rock(nm('rk'), 2.4, (s * 13.0, 0, 0.8), 'cliff_a', seed=17 + s, subdiv=3)
    return finalize('root_arch', smooth_angle=35)


def hanging_vines(name, n, L, seed):
    reset()
    rnd = random.Random(seed)
    box(nm('anchor'), (6.0, 1.2, 0.5), loc=(0, 0, L + 0.25), key='elf_bark')
    blob(nm('mb'), 1.6, (0, 0, L + 0.4), 'jleaf_b', subdiv=2, amp=0.2, scale=(2.2, 0.8, 0.5), seed=seed)
    for i in range(n):
        vine((rnd.uniform(-2.8, 2.8), rnd.uniform(-0.4, 0.4), L), L * rnd.uniform(0.6, 1.0), seed=seed + i, sway=0.5)
    for i in range(4):
        ball(nm('fl'), 0.22, loc=(rnd.uniform(-2.8, 2.8), rnd.uniform(-0.4, 0.4), rnd.uniform(L * 0.3, L)), key='glow_pink', segs=6, rings=4)
    return finalize(name, smooth_angle=40)


def hanging_vines_1():
    """F18 - hanging vine curtain, 12 long, leafy with a few glowing blossoms."""
    return hanging_vines('hanging_vines_1', 8, 12.0, 18)


def hanging_vines_2():
    """F19 - long hanging vines, 22 long, sparse."""
    return hanging_vines('hanging_vines_2', 5, 22.0, 19)


def hanging_moss():
    """F20 - hanging moss: soft grey-green strands draped from a branch, 8 long."""
    reset()
    rnd = random.Random(20)
    tube(nm('br'), [(-4, 0, 8.0), (0, 0.3, 8.4), (4, 0, 8.0)], 0.5, 'elf_bark', res=6)
    for i in range(22):
        x = rnd.uniform(-3.6, 3.6)
        L = rnd.uniform(3, 7.5)
        tube(nm('ms'), [(x, 0, 8.0), (x + rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3), 8.0 - L * 0.5), (x + rnd.uniform(-0.4, 0.4), rnd.uniform(-0.4, 0.4), 8.0 - L)],
             rnd.uniform(0.12, 0.22), rnd.choice(['birch_leaf', 'moss', 'grass_dry']), res=4, taper=[1, 0.7, 0.2])
    return finalize('hanging_moss', smooth_angle=40)


def giant_fern():
    """F21 - giant fern: 10 arching fronds, 9 studs long, made of many leaflets."""
    reset()
    rnd = random.Random(21)
    for k in range(10):
        a = 2 * math.pi * k / 10 + rnd.uniform(-0.15, 0.15)
        L = rnd.uniform(7.5, 9.5)
        d = Vector((math.cos(a), math.sin(a), 0))
        spine = [Vector((0, 0, 0.2)) + d * L * t + Vector((0, 0, 5.0 * math.sin(math.pi * t * 0.75) - 1.2 * t)) for t in (0, 0.25, 0.5, 0.75, 1.0)]
        tube(nm('sp'), [tuple(p) for p in spine], 0.09, 'jleaf_b', res=4, taper=[1, 0.8, 0.6, 0.4, 0.2], ures=2)
        side = d.cross(Vector((0, 0, 1))).normalized()
        for j in range(12):
            t = (j + 0.5) / 12
            i0 = min(3, int(t * 4)); q = spine[i0].lerp(spine[i0 + 1], t * 4 - i0)
            for s in (-1, 1):
                leaf(tuple(q), tuple(side * s * 1.0 + d * 0.4 + Vector((0, 0, -0.2))), 1.8 * (1 - t * 0.65), 0.25, LEAVES[k % 4], bend=0.2, n=3, thick=0.04)
    return finalize('giant_fern', smooth_angle=40)


def giant_leaf_plant():
    """F22 - giant leaf plant (elephant ear): huge heart-shaped leaves on long stalks, 10 tall."""
    reset()
    rnd = random.Random(22)
    for k in range(7):
        a = 2 * math.pi * k / 7 + rnd.uniform(-0.2, 0.2)
        h = rnd.uniform(5.0, 8.5)
        top = (math.cos(a) * 2.5, math.sin(a) * 2.5, h)
        tube(nm('st'), [(0, 0, 0), (math.cos(a) * 1.2, math.sin(a) * 1.2, h * 0.6), top], 0.14, 'jleaf_c', res=4, taper=[1.3, 1.0, 0.7])
        leaf(top, (math.cos(a), math.sin(a), -0.2), rnd.uniform(4.5, 6.0), rnd.uniform(1.8, 2.4), LEAVES[k % 4], bend=0.35, n=6, fold=0.25, thick=0.08)
    return finalize('giant_leaf_plant', smooth_angle=40)


def mushroom_glow(name, specs, cap, gill, seed):
    reset()
    rnd = random.Random(seed)
    for (x, y, h, r) in specs:
        tube(nm('stm'), [(x, y, 0), (x + rnd.uniform(-0.3, 0.3), y + rnd.uniform(-0.3, 0.3), h * 0.5), (x, y, h)], r * 0.2, 'fl_white', res=8,
             taper=[1.5, 1.0, 0.85], ures=3)
        lathe(nm('sk'), [(r * 0.2, h * 0.78), (r * 0.42, h * 0.7), (r * 0.36, h * 0.67), (r * 0.18, h * 0.74)], loc=(x, y, 0), key=gill, segs=12)
        lathe(nm('bb'), [(0.0, 0.0), (r * 0.42, 0.0), (r * 0.36, r * 0.25), (0.0, r * 0.3)], loc=(x, y, 0), key='moss_bright', segs=10)
        lathe(nm('cap'), [(0.0, h - r * 0.1), (r * 0.95, h - r * 0.15), (r, h), (r * 0.8, h + r * 0.35), (r * 0.4, h + r * 0.55), (0.0, h + r * 0.6)], loc=(x, y, 0), key=cap, segs=14)
        lathe(nm('gl'), [(0.0, h - r * 0.1), (r * 0.93, h - r * 0.14), (0.0, h - r * 0.02)], loc=(x, y, 0), key=gill, segs=14)
        for k in range(5):
            a = rnd.uniform(0, 6.28); d = rnd.uniform(0.2, 0.7) * r
            ball(nm('sp'), r * 0.09, loc=(x + math.cos(a) * d, y + math.sin(a) * d, h + r * 0.5 - (d / r) * 0.35 * r), key='fl_white', segs=6, rings=4)
    return finalize(name, smooth_angle=40)


def glow_mushroom_1():
    """F23 - glowing mushroom cluster: cyan-glowing caps, tallest 6 studs."""
    return mushroom_glow('glow_mushroom_1', [(0, 0, 6.0, 2.2), (2.2, 0.8, 3.6, 1.4), (-1.6, 1.4, 2.4, 1.0), (0.8, -1.8, 1.6, 0.7)], 'glow_cyan', 'teal', 23)


def glow_mushroom_2():
    """F24 - glowing mushroom cluster: tall pink-glowing parasols."""
    return mushroom_glow('glow_mushroom_2', [(0, 0, 9.0, 2.8), (2.4, -0.6, 5.0, 1.6), (-2.0, 1.0, 3.2, 1.1)], 'glow_pink', 'fl_purple', 24)


def glow_flower(name, petal, centre, seed, n=5, h=4.0):
    reset()
    rnd = random.Random(seed)
    for k in range(6):
        a = 2 * math.pi * k / 6
        leaf((0, 0, 0.1), (math.cos(a), math.sin(a), 0.5), 1.8, 0.5, LEAVES[k % 4], bend=0.4, n=4)
    for i in range(n):
        a = 2 * math.pi * i / n + rnd.uniform(-0.3, 0.3)
        x, y = math.cos(a) * rnd.uniform(0.3, 1.0), math.sin(a) * rnd.uniform(0.3, 1.0)
        hh = h * rnd.uniform(0.7, 1.1)
        tube(nm('st'), [(0, 0, 0), (x * 0.6, y * 0.6, hh * 0.6), (x, y, hh)], 0.07, 'jleaf_c', res=4)
        for k in range(6):
            b = 2 * math.pi * k / 6
            leaf((x, y, hh), (math.cos(b), math.sin(b), 0.9), 0.9, 0.35, petal, bend=-0.25, n=3, thick=0.04)
        ball(nm('c'), 0.2, loc=(x, y, hh + 0.15), key=centre, segs=8, rings=6)
    return finalize(name, smooth_angle=40)


def glow_flower_1():
    """F25 - glowing flower: cyan cup blossoms with gold glowing centres."""
    return glow_flower('glow_flower_1', 'glow_cyan', 'glow_gold', 25)


def glow_flower_2():
    """F26 - glowing flower: tall pink star blossoms."""
    return glow_flower('glow_flower_2', 'glow_pink', 'glow_gold', 26, n=4, h=5.5)


# ============================================================ lights, water and furniture
def elf_hanging_lantern():
    """F27 - elven hanging lantern: gold leaf cage around a glowing cyan bud, on a curved hook."""
    reset()
    tube(nm('hk'), [(0, 0, 6.0), (0, 0, 5.0), (0.4, 0, 4.4), (0, 0, 4.0)], 0.07, 'gold', res=4)
    hanging_lantern_at(0, 0, 4.0, s=1.5)
    for k in range(4):
        a = math.pi / 2 * k + math.pi / 4
        leaf((math.cos(a) * 0.3, math.sin(a) * 0.3, 3.9), (math.cos(a), math.sin(a), 0.1), 0.9, 0.3, 'gold', bend=0.4, n=3, thick=0.05)
    return finalize('elf_hanging_lantern', smooth_angle=40)


def elf_standing_lantern():
    """F28 - elven standing lantern: curling pale-wood post ending in a glowing bud, 10 tall."""
    reset()
    lathe(nm('b'), [(0, 0), (1.0, 0), (0.8, 0.4), (0.3, 0.8), (0, 0.8)], key=ST, segs=10)
    pts = [(0, 0, 0.8), (0.2, 0, 4.0), (-0.3, 0, 7.0), (0.6, 0, 9.4), (1.6, 0, 9.8), (2.2, 0, 9.2)]
    tube(nm('p'), pts, 0.2, W_, res=4, taper=[1.2, 1.0, 0.9, 0.8, 0.6, 0.4], ures=3)
    tube(nm('pg'), [(p[0] + 0.15, 0.12, p[2]) for p in pts[:4]], 0.05, 'gold', res=4, ures=3)
    hanging_lantern_at(2.2, 0, 9.2, s=1.0)
    for k in range(3):
        leaf((0.0, 0.0, 3.0 + k * 2.0), (rnd_sign(k), 0.3, 0.6), 1.2, 0.35, LEAVES[k], bend=0.3, n=3)
    return finalize('elf_standing_lantern', smooth_angle=40)


def rnd_sign(k):
    return -1 if k % 2 else 1


def lotus():
    """F29 - lotus / water lily: big pad, layered pink-white petals, glowing heart, two side pads."""
    reset()
    lotus_at(0, 0, 0.1, s=2.0, seed=29)
    cyl(nm('p2'), 1.6, 0.06, loc=(3.6, 2.0, 0.05), key='jleaf_c', verts=16)
    cyl(nm('p3'), 1.2, 0.06, loc=(-2.6, 2.8, 0.05), key='jleaf_a', verts=16)
    return finalize('lotus', smooth_angle=40)


def ruins(name, seed):
    reset()
    rnd = random.Random(seed)
    for i in range(5):
        x = -12 + i * 6.0
        h = rnd.uniform(4, 13) if i != 2 else 2.5
        lathe(nm('col'), [(0, 0), (1.4, 0), (1.4, 0.6), (1.0, 0.9), (0.9, h), (0, h)], loc=(x, 0, 0), key=rnd.choice([ST, STD]), segs=10)
        if h > 9:
            lathe(nm('cap'), [(0, h), (1.2, h), (1.6, h + 0.8), (0, h + 0.8)], loc=(x, 0, 0), key=ST, segs=10)
        o = blob(nm('ms'), rnd.uniform(0.9, 1.4), (x, 0, h), 'moss_bright', subdiv=2, amp=0.25, scale=(1.3, 1.3, 0.6), seed=seed + i)
        vine((x + 0.9, 0.4, h), h * 0.8, seed=seed + i, sway=0.3)
    beam3((-12, 0, 13.6), (-6, 0, 13.6), 2.0, 1.6, ST)
    lslab(F(0, 3.0, 0, 0), [(-14, 0, 0), (-4, 0, 0), (-4, 0, 3.0), (-6, 0, 5.0), (-9, 0, 4.0), (-12, 0, 6.5), (-14, 0, 5.0)], (0, 1.2, 0), STD)
    for i in range(14):
        box(nm('rb'), (rnd.uniform(1.0, 2.2), rnd.uniform(0.8, 1.4), rnd.uniform(0.6, 1.0)), loc=(rnd.uniform(-14, 14), rnd.uniform(-4, 4), 0.4),
            key=rnd.choice([ST, STD]), rot=(rnd.uniform(-20, 20), rnd.uniform(-20, 20), rnd.uniform(0, 90)), bev=0.1)
    lathe(nm('fc'), [(0, 0), (1.0, 0), (1.0, 4.0), (0, 4.0)], loc=(8.0, -3.5, 0), key=ST, segs=10, rot=(0, 90, 20))
    for i in range(8):
        blob(nm('bu'), rnd.uniform(1.0, 1.8), (rnd.uniform(-14, 14), rnd.uniform(-4, 4), 0.4), rnd.choice(LEAVES), subdiv=2, amp=0.2, scale=(1.2, 1.2, 0.7), seed=seed + 30 + i)
    return finalize(name, smooth_angle=30)


def ruins_1():
    """F30 - overgrown stone ruins: broken colonnade with a fallen lintel, moss and vines."""
    return ruins('ruins_1', 30)


def ruins_2():
    """F31 - overgrown stone ruins: shattered colonnade variant with different heights and debris."""
    return ruins('ruins_2', 31)


def waterfall_cliff():
    """F32 - waterfall cliff: tall mossy cliff face, curved falling sheet, misty splash and a glowing pool."""
    reset()
    rnd = random.Random(32)
    for i in range(10):
        o = rock(nm('cl'), rnd.uniform(5, 8), (rnd.uniform(-14, 14), rnd.uniform(2, 6), rnd.uniform(3, 28)), rnd.choice(['cliff_a', 'cliff_b']), seed=320 + i, subdiv=3,
                 scale=(1.2, 0.8, 1.1))
        top_paint(o, 'moss_bright', 0.45, i)
    bm = bmesh.new()
    rows = []
    for j in range(12):
        t = j / 11
        z = 30.0 - t * 29.0
        y = -1.0 - math.sin(t * math.pi * 0.5) * 3.0
        rows.append([bm.verts.new((x, y + rnd.uniform(-0.1, 0.1), z)) for x in (-4.0, -2.0, 0.0, 2.0, 4.0)])
    for a, b in zip(rows, rows[1:]):
        for i in range(4):
            bm.faces.new((a[i], a[i + 1], b[i + 1], b[i]))
    o = _obj_from_bm(nm('wf'), bm, 'water_fx')
    o.modifiers.new('s', 'SOLIDIFY').thickness = 0.4
    cyl(nm('pool'), 10.0, 0.08, loc=(0, -6.0, 0.4), key='moon_water', verts=24)
    for i in range(10):
        blob(nm('fm'), rnd.uniform(0.8, 1.4), (rnd.uniform(-4, 4), rnd.uniform(-6, -3.5), 0.6), 'foam', subdiv=2, amp=0.3, scale=(1.3, 1.0, 0.5), seed=i)
    for i in range(12):
        a = math.pi + math.pi * i / 11
        rock(nm('rs'), rnd.uniform(1.0, 1.8), (math.cos(a) * 10.5, -6.0 + math.sin(a) * 6.0 * -1 + 0.0, 0.4), rnd.choice(['stone', 'cliff_b']), seed=340 + i, subdiv=2)
    for i in range(6):
        vine((rnd.uniform(-12, 12), 0.0, 30.0), rnd.uniform(8, 18), seed=i + 32)
    return finalize('waterfall_cliff', smooth_angle=15)


def elf_bench():
    """F33 - elven bench: curved pale-wood seat on leaf-shaped stone legs, gold inlay, 8 long."""
    reset()
    L = 8.0
    pts = [(-L / 2 + L * t / 8, 0.4 * math.sin(math.pi * t / 8) * 0, 1.9 + 0.25 * math.sin(math.pi * t / 8)) for t in range(9)]
    for k in range(4):
        tube(nm('sl'), [(x, -0.75 + k * 0.5, z) for x, _, z in pts], 0.2, W_, res=4, ures=2)
    for k in range(3):
        tube(nm('bk'), [(x, 0.95 + k * 0.08, z + 0.9 + k * 0.8) for x, _, z in pts[1:-1]], 0.18, W_, res=4, ures=2)
    for s in (-1, 1):
        leg = [(s * (L / 2 - 0.6), -1.0, 0), (s * (L / 2 - 0.6), 1.4, 0), (s * (L / 2 - 0.6), 1.4, 3.6), (s * (L / 2 - 0.6), 0.8, 4.4), (s * (L / 2 - 0.6), 0.0, 2.0),
               (s * (L / 2 - 0.6), -1.2, 1.4)]
        lslab(F(), leg, (s * 0.5, 0, 0), ST)
        tube(nm('gi'), [(s * (L / 2 - 0.6) + s * 0.52, -0.6, 0.4), (s * (L / 2 - 0.6) + s * 0.52, 0.6, 2.4), (s * (L / 2 - 0.6) + s * 0.52, 0.9, 3.8)], 0.06, 'gold', res=4)
    return finalize('elf_bench', smooth_angle=35)


def crystal_cluster():
    """F34 - magic crystal cluster: tall glowing cyan and purple crystals bursting from a mossy rock."""
    reset()
    rnd = random.Random(34)
    o = rock(nm('base'), 2.8, (0, 0, 0.6), 'cliff_b', seed=34, subdiv=3, scale=(1.3, 1.1, 0.6))
    top_paint(o, 'moss_bright', 0.6, 1)
    for i in range(9):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, 1.8)
        h = rnd.uniform(2.5, 8.0) * (1.2 if i == 0 else 1.0)
        r = h * 0.14
        tilt = (rnd.uniform(-25, 25), rnd.uniform(-25, 25), 0) if i else (0, 0, 0)
        o = lathe(nm('cr'), [(0.0, 0.0), (r, h * 0.1), (r * 0.95, h * 0.8), (0.0, h)], loc=(math.cos(a) * d, math.sin(a) * d, 1.0), key=rnd.choice(['magic', 'glow_cyan', 'magic_purple']),
                  segs=6, rot=tilt)
    return finalize('crystal_cluster', smooth_angle=20)


def vine_pillar():
    """F35 - vine-wrapped elven pillar: slender fluted stone column, spiral vines with leaves and glowing blossoms, 18 tall."""
    reset()
    rnd = random.Random(35)
    column_c(0, 0, 0, 18.0, 1.0, key=ST, base='gold')
    pts = [(math.cos(t * 0.6) * 1.15, math.sin(t * 0.6) * 1.15, 0.8 + t * 0.6) for t in range(0, 28)]
    tube(nm('vn'), pts, 0.12, 'leaf_dark', res=4, ures=2)
    pts2 = [(math.cos(t * 0.6 + 3.0) * 1.1, math.sin(t * 0.6 + 3.0) * 1.1, 1.5 + t * 0.55) for t in range(0, 26)]
    tube(nm('vn2'), pts2, 0.09, 'leaf_dark', res=4, ures=2)
    for p in pts[::2] + pts2[::3]:
        a = math.atan2(p[1], p[0])
        leaf(p, (math.cos(a), math.sin(a), rnd.uniform(-0.3, 0.6)), rnd.uniform(0.6, 1.0), 0.3, rnd.choice(LEAVES), bend=0.2, n=3, thick=0.04)
    for p in pts[3::6]:
        ball(nm('bl'), 0.22, loc=(p[0] * 1.2, p[1] * 1.2, p[2]), key='glow_pink', segs=6, rings=4)
    return finalize('vine_pillar', smooth_angle=35)


ITEMS_A = [
    ('F01_world_tree', world_tree), ('F02_treehouse_1', treehouse_1), ('F03_treehouse_2', treehouse_2), ('F04_treehouse_3', treehouse_3),
    ('F05_treehouse_4', treehouse_4), ('F06_platform_ring', platform_ring), ('F07_rope_bridge_short', rope_bridge_short),
    ('F08_rope_bridge_long', rope_bridge_long), ('F09_spiral_stair', spiral_stair), ('F10_elf_palace', elf_palace), ('F11_moon_pool', moon_pool),
    ('F12_carved_arch', carved_arch), ('F13_elf_statue', elf_statue),
]
ITEMS_B = [
    ('F14_jungle_tree_1', jungle_tree_1), ('F15_jungle_tree_2', jungle_tree_2), ('F16_jungle_palm', jungle_palm), ('F17_root_arch', root_arch),
    ('F18_hanging_vines_1', hanging_vines_1), ('F19_hanging_vines_2', hanging_vines_2), ('F20_hanging_moss', hanging_moss), ('F21_giant_fern', giant_fern),
    ('F22_giant_leaf_plant', giant_leaf_plant), ('F23_glow_mushroom_1', glow_mushroom_1), ('F24_glow_mushroom_2', glow_mushroom_2),
    ('F25_glow_flower_1', glow_flower_1), ('F26_glow_flower_2', glow_flower_2), ('F27_elf_hanging_lantern', elf_hanging_lantern),
    ('F28_elf_standing_lantern', elf_standing_lantern), ('F29_lotus', lotus), ('F30_ruins_1', ruins_1), ('F31_ruins_2', ruins_2),
    ('F32_waterfall_cliff', waterfall_cliff), ('F33_elf_bench', elf_bench), ('F34_crystal_cluster', crystal_cluster), ('F35_vine_pillar', vine_pillar),
]
