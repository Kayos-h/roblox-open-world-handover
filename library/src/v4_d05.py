"""v4_d05 - elven trees: world tree (trunk / roots / canopy pieces), five ancient trees of different species,
canopy clusters, stumps, logs, a hollow tree and a sapling. Natural bark, moss and leaf greens only (no neon).
1 unit = 1 stud, Z up, origin at bottom centre. The world tree pieces stack: roots top ring r=21 at z=30 ->
trunk base r=21 at z=0 (height 150) -> canopy leader base r=12 at z=0.
"""
import math, random, bpy
from mathutils import Vector
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism
import v4util as U
from v4_elf import nm, bark_trunk, trunk_point, roots, limb, cluster, crown, ivy_strand, mushrooms, fern, lantern, LEAF
from v4_d04 import prism_xz, shell, steps
from nature import blob, rock

PI = math.pi
D = math.degrees
LEAF_BRIGHT = ('ev_leaf_c', 'ev_leaf_a', 'ev_leaf_gold', 'ev_leaf_c')
LEAF_DEEP = ('ev_leaf_b', 'ev_leaf_d', 'ev_leaf_b', 'ev_leaf_a')


# ------------------------------------------------------------------ shared pieces
def trunk_r(tr, H, z, top_r=0.62):
    t = max(0.0, min(1.0, z / H))
    return tr * (top_r + (1 - top_r) * (1 - t) ** 0.8)


def wcluster(cx, cy, z, r, seed, n=5, subdiv=2, flat=0.7, keys=LEAF):
    """Leaf mass: lumpy blobs, lighter on top, darker underneath. subdiv=1 for hidden interior clumps."""
    rnd = random.Random(seed * 7 + 3)
    for i in range(n):
        a = rnd.uniform(0, 2 * PI)
        d = r * 0.55 * math.sqrt(rnd.random())
        dz = rnd.uniform(-r * 0.25, r * 0.3)
        br = r * rnd.uniform(0.4, 0.62)
        k = rnd.choice(keys)
        if dz > r * 0.1:
            k = rnd.choice(('ev_leaf_c', 'ev_leaf_a', 'ev_leaf_c'))
        elif dz < -r * 0.1:
            k = rnd.choice(('ev_leaf_b', 'ev_leaf_d'))
        if rnd.random() < 0.012:
            k = 'ev_leaf_gold'
        blob(nm('wl'), br, (cx + math.cos(a) * d, cy + math.sin(a) * d, z + dz), k, subdiv=subdiv, amp=0.32, scale=(1, 1, flat), seed=rnd.randint(0, 999), detail=0.3)


def hang_strand(x, y, z, L, rnd, keys=('ev_leaf_a', 'ev_leaf_b', 'ev_leaf_c')):
    """Hanging leaf strand (willow-like): thin vine with a leaf ball about every 1.5 studs."""
    pts = [(x, y, z), (x + rnd.uniform(-0.5, 0.5), y + rnd.uniform(-0.5, 0.5), z - L * 0.4), (x + rnd.uniform(-0.8, 0.8), y + rnd.uniform(-0.8, 0.8), z - L)]
    tube(nm('hs'), pts, 0.07, 'ev_leaf_b', res=4, ures=2)
    n = max(3, int(L / 1.5))
    for i in range(n):
        t = (i + 0.6) / n
        px = x + (pts[2][0] - x) * t * t
        py = y + (pts[2][1] - y) * t * t
        ball(nm('hl'), rnd.uniform(0.32, 0.5), loc=(px, py, z - L * t), key=rnd.choice(keys), segs=6, rings=4, scale=(1, 1, 0.6))


def moss_on_trunk(tr, H, seed, n, rnd, sway=1.2, lean=(0.0, 0.0), zmin=1.0, zmax=None, ox=0.0, oy=0.0, top_r=0.62):
    zmax = zmax or H * 0.8
    for i in range(n):
        z = rnd.uniform(zmin, zmax)
        cx, cy = trunk_point(tr, H, seed, z, sway, lean)
        a = rnd.uniform(0, 2 * PI)
        rr = trunk_r(tr, H, z, top_r) * 0.97
        if i % 3 == 0:
            blob(nm('tm'), rnd.uniform(0.5, 1.1) * (tr / 3) ** 0.5, (ox + cx + math.cos(a) * rr, oy + cy + math.sin(a) * rr, z), 'ev_moss', subdiv=1, amp=0.3, scale=(0.7, 0.7, 1.3), seed=i)
        elif i % 3 == 1:
            o = ball(nm('sf'), rnd.uniform(0.45, 0.8) * (tr / 3) ** 0.5, loc=(ox + cx + math.cos(a) * (rr + 0.1), oy + cy + math.sin(a) * (rr + 0.1), z), key=rnd.choice(('ev_shroom_brown', 'ev_shroom_cream')), segs=8, rings=4, scale=(1, 1, 0.28))
        else:
            ivy_strand((ox + cx + math.cos(a) * (rr + 0.1), oy + cy + math.sin(a) * (rr + 0.1), z + 2.0), rnd.uniform(3.0, 7.0) * (tr / 3) ** 0.5, seed=i)


def ground_bits(tr, rnd, seed, ox=0.0, oy=0.0, nrock=4, scale=1.0):
    for i in range(nrock):
        a = rnd.uniform(0, 2 * PI)
        d = tr * rnd.uniform(2.4, 3.8)
        rock(nm('gr'), rnd.uniform(0.7, 1.3) * scale, (ox + math.cos(a) * d, oy + math.sin(a) * d, 0.0), 'ev_stone_dark', seed=i + seed)
    mushrooms(ox + tr * 1.5, oy - tr * 1.2, 0.0, 5, seed=seed, scale=scale)
    fern(ox - tr * 2.0, oy + tr * 1.4, 0.0, n=7, L=1.6 * scale, seed=seed)
    fern(ox + tr * 2.3, oy + tr * 0.7, 0.0, n=7, L=1.6 * scale, seed=seed + 1)


def cut_arch(target, phi_deg, r_front, w, h, depth, z0=0.6):
    """Boolean-cut a round-topped doorway into a trunk. phi_deg = outward direction; r_front = radius where the cut starts."""
    ph = h - w
    pts = [(-w, z0), (w, z0), (w, z0 + ph)] + [(w * math.cos(PI * i / 14), z0 + ph + w * math.sin(PI * i / 14)) for i in range(1, 14)] + [(-w, z0 + ph)]
    cutter = prism_xz(pts, -(r_front + 4.0), -(r_front - depth), 'ev_bark')
    cutter.rotation_euler.z = math.radians(phi_deg + 90)
    bpy.context.view_layer.update()
    m = target.modifiers.new('doorcut', 'BOOLEAN')
    m.operation = 'DIFFERENCE'
    m.object = cutter
    m.solver = 'EXACT'
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(target.evaluated_get(dg))
    target.modifiers.clear()
    old = target.data
    target.data = me
    bpy.data.objects.remove(cutter, do_unlink=True)
    try:
        bpy.data.meshes.remove(old)
    except Exception:
        pass
    return target


def limb_tree(seed, tr, H, nlimb=7, z_lo=0.55, z_hi=0.8, len_rng=(12, 18), pitch=(0.3, 0.65), sway=1.2, key='ev_bark', top_r=0.62, flare=1.9,
              lean=(0.0, 0.0), root_n=8, rspan=2.6, limb_r=0.34, sub=True, ox=0.0, oy=0.0, segs=16):
    """Trunk with roots and forking limbs. Returns (rnd, tips, top_xy)."""
    rnd = random.Random(seed)
    t = bark_trunk(tr, H, seed=seed, sway=sway, flare=flare, key=key, segs=segs, ring_h=max(1.4, H / 30), top_r=top_r, lean=lean)
    t.location = (ox, oy, 0)
    roots(tr, n=root_n, seed=seed, key=key, span=rspan, ox=ox, oy=oy)
    tips = []
    for k in range(nlimb):
        az = 2 * PI * k / nlimb + rnd.uniform(-0.3, 0.3)
        z0 = H * rnd.uniform(z_lo, z_hi)
        p0 = trunk_point(tr, H, seed, z0, sway, lean)
        e = limb((ox + p0[0], oy + p0[1], z0), (math.cos(az), math.sin(az), rnd.uniform(*pitch)), rnd.uniform(*len_rng), tr * limb_r, key=key, seed=k)
        tips.append(e)
        if sub:
            az2 = az + rnd.uniform(-0.6, 0.6)
            e2 = limb((e.x, e.y, e.z), (math.cos(az2), math.sin(az2), rnd.uniform(0.4, 0.9)), rnd.uniform(len_rng[0] * 0.4, len_rng[1] * 0.5), tr * limb_r * 0.5, key=key, seed=k + 20)
            tips.append(e2)
    top = trunk_point(tr, H, seed, H, sway, lean)
    return rnd, tips, (ox + top[0], oy + top[1])


# ------------------------------------------------------------------ D05_01..03 world tree (stacking pieces)
def world_tree_trunk():
    reset()
    rnd = random.Random(201)
    tr, H = 21.0, 150.0
    bark_trunk(tr, H, seed=21, sway=0.0, flare=1.0, key='ev_bark', segs=28, ring_h=5.0, top_r=0.6)
    # big bark plates and buttress ridges up the trunk
    for i in range(14):
        a = 2 * PI * i / 14 + rnd.uniform(-0.1, 0.1)
        z0 = rnd.uniform(4, 60)
        L = rnd.uniform(40, 80)
        pts = []
        for k in range(5):
            z = z0 + L * k / 4
            rr = trunk_r(tr, H, z, 0.6) * 1.01
            aa = a + math.sin(z * 0.05 + i) * 0.08
            pts.append((math.cos(aa) * rr, math.sin(aa) * rr, z))
        tube(nm('rdg'), pts, 1.5 + rnd.random() * 0.8, 'ev_bark_light' if i % 3 == 0 else 'ev_bark', res=4, taper=[0.6, 1.0, 1.0, 0.8, 0.3], ures=3)
    # limb stubs near the top where the canopy attaches
    for k in range(8):
        az = 2 * PI * k / 8 + 0.2
        z = 118 + (k % 3) * 8
        rr = trunk_r(tr, H, z, 0.6)
        tube(nm('stub'), [(math.cos(az) * (rr - 1), math.sin(az) * (rr - 1), z - 2), (math.cos(az) * (rr + 7), math.sin(az) * (rr + 7), z + 3), (math.cos(az) * (rr + 14), math.sin(az) * (rr + 14), z + 10)], 4.6, 'ev_bark', res=4, taper=[1.2, 0.9, 0.6], ures=3)
    # warm round windows and small balconies
    for k, (z, az) in enumerate(((22, -1.1), (36, -0.4), (48, -1.7), (62, -0.9), (78, -1.4))):
        rr = trunk_r(tr, H, z, 0.6)
        x, y = math.cos(az) * rr, math.sin(az) * rr
        o = cyl(nm('win'), 2.1, 0.5, loc=(x * 0.99, y * 0.99, z), key='ev_lantern', verts=14)
        o.rotation_euler = Vector((math.cos(az), math.sin(az), 0)).to_track_quat('Z', 'Y').to_euler()
        wt = torus(nm('wfr'), 2.35, 0.35, loc=(x * 1.01, y * 1.01, z), key='ev_wood_dark', segs=16, rsegs=4)
        wt.rotation_euler = Vector((math.cos(az), math.sin(az), 0)).to_track_quat('Z', 'Y').to_euler()
        box(nm('wsl'), (5.2, 1.8, 0.5), loc=(x * 1.03, y * 1.03, z - 2.6), key='ev_wood', rot=(0, 0, D(az) + 90), bev=0.05)
    # moss, shelf fungi and long ivy
    moss_on_trunk(tr, H, 21, 60, rnd, sway=0.0, zmin=3, zmax=140, top_r=0.6)
    for i in range(10):
        a = rnd.uniform(0, 2 * PI)
        z = rnd.uniform(70, 140)
        rr = trunk_r(tr, H, z, 0.6)
        pts = [(math.cos(a) * (rr + 0.2), math.sin(a) * (rr + 0.2), z)]
        for k in range(1, 7):
            pts.append((math.cos(a + 0.03 * k) * (rr + 0.4), math.sin(a + 0.03 * k) * (rr + 0.4), z - 7 * k))
        tube(nm('vine'), pts, 0.28, 'ev_leaf_b', res=4, ures=2)
        for k in range(0, 7):
            for s in (-1, 1):
                ball(nm('vl'), rnd.uniform(0.7, 1.1), loc=(pts[k][0] + s * 0.6, pts[k][1], pts[k][2]), key=rnd.choice(('ev_leaf_a', 'ev_leaf_b', 'ev_leaf_c')), segs=6, rings=4, scale=(1, 0.6, 0.8))
    U.marker('mk_deck', (0, 0, 2.0))
    return finalize('ev_world_tree_trunk', smooth_angle=38)


def world_tree_roots():
    reset()
    rnd = random.Random(203)
    r, h = 21.0, 30.0
    door_a = 260.0
    trunk = bark_trunk(r, h, seed=22, sway=0.0, flare=1.9, key='ev_bark', segs=28, ring_h=3.0, top_r=1.0)
    cut_arch(trunk, door_a, r * 1.55, 5.6, 13.0, 21.0)
    door = math.radians(door_a)
    n = 11
    for i in range(n):
        a = door + 0.62 + (2 * PI - 1.24) * i / (n - 1) + rnd.uniform(-0.06, 0.06)
        c, s = math.cos(a), math.sin(a)
        L = rnd.uniform(52, 84)
        rad = 6.8 + rnd.uniform(-0.8, 1.0)
        pts = [(c * r * 0.5, s * r * 0.5, r * 1.15), (c * r * 1.25, s * r * 1.25, r * 0.5), (c * (r + 0.55 * L), s * (r + 0.55 * L), 4.2), (c * (r + L), s * (r + L), -0.4)]
        tube(nm('root'), pts, rad, 'ev_bark', res=4, taper=[1.0, 0.8, 0.5, 0.2], ures=4)
        if i % 2 == 0:   # smaller secondary root
            a2 = a + rnd.uniform(-0.25, 0.25)
            c2, s2 = math.cos(a2), math.sin(a2)
            L2 = L * 0.55
            tube(nm('rt2'), [(c2 * (r + 8), s2 * (r + 8), 7.5), (c2 * (r + 8 + 0.5 * L2), s2 * (r + 8 + 0.5 * L2), 3.0), (c2 * (r + 8 + L2), s2 * (r + 8 + L2), -0.3)], 2.6, 'ev_bark', res=4, taper=[1, 0.6, 0.25], ures=3)
        for k in range(3):   # moss on top of the root
            d = r + L * rnd.uniform(0.2, 0.7)
            blob(nm('rm'), rnd.uniform(1.4, 2.6), (c * d, s * d, 6.5 * (1 - d / (r + L)) + 3.5), 'ev_moss', subdiv=1, amp=0.3, scale=(1.4, 1, 0.4), seed=i * 3 + k)
    # doorway: stone steps, stone floor, lanterns on posts and a hanging lantern inside
    steps(door, r * 1.5, 7.0, 4, 11.0, key='ev_stone', depth=2.0)
    for sd in (-1, 1):
        px = math.cos(door) * (r * 1.5 + 9.5) - math.sin(door) * sd * 9.0
        py = math.sin(door) * (r * 1.5 + 9.5) + math.cos(door) * sd * 9.0
        cyl(nm('lp'), 0.35, 8.0, loc=(px, py, 0.0), key='ev_wood_dark', verts=6)
        lantern(px, py, 8.0 + 1.12 * 1.6, s=1.6, hang=False)
    ix, iy = math.cos(door) * 20.0, math.sin(door) * 20.0
    lantern(ix, iy, 11.0 - 0.9 * 1.4, s=1.4, hang=True)
    for i in range(12):
        a = rnd.uniform(0, 2 * PI)
        d = rnd.uniform(36, 70)
        rock(nm('gr'), rnd.uniform(1.4, 3.0), (math.cos(a) * d, math.sin(a) * d, 0.0), 'ev_stone_dark', seed=i)
    for i in range(12):
        a = rnd.uniform(0, 2 * PI)
        d = rnd.uniform(26, 60)
        mushrooms(math.cos(a) * d, math.sin(a) * d, 0.0, 4, seed=i, scale=2.0)
        fern(math.cos(a + 0.5) * (d + 4), math.sin(a + 0.5) * (d + 4), 0.0, n=8, L=3.4, seed=i)
    U.marker('mk_door', (math.cos(door) * (r * 1.5 + 2.0), math.sin(door) * (r * 1.5 + 2.0), 2.0))
    U.marker('mk_deck', (0, 0, h + 0.5))
    return finalize('ev_world_tree_roots', smooth_angle=38)


def world_tree_canopy():
    reset()
    rnd = random.Random(205)
    tube(nm('lead'), [(0, 0, 0), (1.5, 0.5, 30), (0, 1.5, 62), (0, 0, 92)], 12.0, 'ev_bark', res=4, taper=[1.0, 0.75, 0.45, 0.15], ures=4)
    tips = []
    npri = 10
    for k in range(npri):
        az = 2 * PI * k / npri + rnd.uniform(-0.2, 0.2)
        z0 = rnd.uniform(0, 26)
        e = limb((math.cos(az) * 8, math.sin(az) * 8, z0), (math.cos(az), math.sin(az), rnd.uniform(0.3, 0.62)), rnd.uniform(48, 68), 5.0, seed=k, droop=0.06)
        tips.append(e)
        for s in range(2):
            az2 = az + rnd.uniform(-0.7, 0.7)
            e2 = limb((e.x, e.y, e.z), (math.cos(az2), math.sin(az2), rnd.uniform(0.35, 0.8)), rnd.uniform(22, 34), 2.3, seed=k * 3 + s, droop=0.05)
            tips.append(e2)
    for i, e in enumerate(tips):
        wcluster(e.x, e.y, e.z + 3, rnd.uniform(13, 19), 50 + i, n=5, subdiv=2)
    for ring, (rad, z, cnt, rr) in enumerate(((56, 42, 10, 16), (40, 52, 9, 17), (30, 64, 8, 17), (24, 74, 7, 16), (8, 92, 4, 15))):
        for j in range(cnt):
            a = 2 * PI * j / cnt + ring
            wcluster(math.cos(a) * rad, math.sin(a) * rad, z + rnd.uniform(-4, 4), rr * rnd.uniform(0.9, 1.15), 300 + ring * 20 + j, n=5, subdiv=1 if ring in (1, 2) else 2)
    wcluster(0, 0, 100, 24, 400, n=7, subdiv=2)
    for j in range(16):   # hanging leaf strands below the outer ring
        a = rnd.uniform(0, 2 * PI)
        d = rnd.uniform(34, 60)
        hang_strand(math.cos(a) * d, math.sin(a) * d, rnd.uniform(36, 48), rnd.uniform(16, 26), rnd)
    U.marker('mk_deck', (0, 0, 0.5))
    return finalize('ev_world_tree_canopy', smooth_angle=38)


# ------------------------------------------------------------------ D05_04..08 ancient trees, five species
def ancient_a():
    """Great oak: massive trunk, broad flat-topped crown."""
    reset()
    tr, H = 6.4, 60.0
    rnd, tips, top = limb_tree(11, tr, H, nlimb=9, z_lo=0.45, z_hi=0.72, len_rng=(20, 30), pitch=(0.2, 0.5), sway=1.4, root_n=9, rspan=3.0)
    tube(nm('lead'), [(top[0], top[1], H * 0.7), (top[0] + 0.5, top[1], H * 0.9), (top[0], top[1], H + 3)], tr * 0.42, 'ev_bark', res=4, taper=[1, 0.6, 0.25])
    crown(top[0], top[1], H * 0.82, 34.0, 15.0, seed=11, count=44)
    for i, e in enumerate(tips):
        cluster(e.x, e.y, e.z + 2.0, rnd.uniform(6.4, 8.6), seed=100 + i, n=6)
    moss_on_trunk(tr, H, 11, 22, rnd, sway=1.4, zmin=1, zmax=36)
    ground_bits(tr, rnd, 11, nrock=5, scale=1.4)
    return finalize('ev_ancient_tree_a', smooth_angle=38)


def ancient_b():
    """Silverbark beech: tall, slim, pale trunk, narrow oval crown of bright leaves."""
    reset()
    tr, H = 3.2, 74.0
    rnd, tips, top = limb_tree(23, tr, H, nlimb=11, z_lo=0.4, z_hi=0.86, len_rng=(8, 13), pitch=(0.5, 1.1), sway=0.7, key='ev_bark_silver', top_r=0.45, flare=1.6, root_n=7, rspan=2.2, limb_r=0.3)
    crown(top[0], top[1], H * 0.72, 18.0, 34.0, seed=23, count=46, keys=LEAF_BRIGHT)
    for i, e in enumerate(tips):
        cluster(e.x, e.y, e.z + 1.5, rnd.uniform(4.4, 6.4), seed=200 + i, n=6, keys=LEAF_BRIGHT)
    moss_on_trunk(tr, H, 23, 10, rnd, sway=0.7, zmin=1, zmax=14, top_r=0.45)
    ground_bits(tr, rnd, 23, nrock=3, scale=1.1)
    return finalize('ev_ancient_tree_b', smooth_angle=38)


def ancient_c():
    """Mournwood: leaning trunk, low dome crown, long hanging curtains of leaves."""
    reset()
    tr, H = 4.0, 40.0
    rnd, tips, top = limb_tree(37, tr, H, nlimb=8, z_lo=0.55, z_hi=0.82, len_rng=(12, 17), pitch=(0.5, 0.95), sway=2.4, lean=(0.07, 0.03), root_n=8, rspan=2.8, limb_r=0.32)
    crown(top[0], top[1], H * 0.8, 20.0, 10.0, seed=37, count=26, keys=LEAF_DEEP)
    for i, e in enumerate(tips):
        cluster(e.x, e.y, e.z + 1.0, rnd.uniform(4.6, 6.0), seed=300 + i, n=5, keys=LEAF_DEEP)
        if i % 2 == 0:
            for j in range(2):
                hang_strand(e.x + rnd.uniform(-2.5, 2.5), e.y + rnd.uniform(-2.5, 2.5), e.z + 0.3, rnd.uniform(14, 23), rnd)
    for j in range(10):
        a = 2 * PI * j / 10
        hang_strand(top[0] + math.cos(a) * 15, top[1] + math.sin(a) * 15, H * 0.78, rnd.uniform(15, 24), rnd)
    moss_on_trunk(tr, H, 37, 14, rnd, sway=2.4, lean=(0.07, 0.03), zmin=1, zmax=22)
    ground_bits(tr, rnd, 37, nrock=4, scale=1.2)
    return finalize('ev_ancient_tree_c', smooth_angle=38)


def ancient_d():
    """Layered elder cedar: straight trunk, tiers of flat foliage pads shrinking toward the top."""
    reset()
    rnd = random.Random(53)
    tr, H = 3.8, 72.0
    bark_trunk(tr, H, seed=53, sway=0.3, flare=1.8, key='ev_bark', top_r=0.3, ring_h=2.6)
    roots(tr, n=8, seed=53, key='ev_bark', span=2.4)
    nt = 10
    for t in range(nt):
        f = t / (nt - 1)
        z = H * (0.2 + 0.74 * f)
        Rt = 21.0 * (1 - f) ** 0.9 + 3.2
        nb = 6 if t < nt - 2 else 4
        c0 = trunk_point(tr, H, 53, z, 0.3)
        for k in range(nb):
            az = t * 0.55 + 2 * PI * k / nb + rnd.uniform(-0.15, 0.15)
            ex, ey, ez = c0[0] + math.cos(az) * Rt, c0[1] + math.sin(az) * Rt, z - Rt * 0.07
            tube(nm('bch'), [(c0[0], c0[1], z), (c0[0] + math.cos(az) * Rt * 0.5, c0[1] + math.sin(az) * Rt * 0.5, z + 0.5), (ex, ey, ez)], max(0.3, 0.8 * (1 - f) + 0.25), 'ev_bark', res=4, taper=[1, 0.7, 0.4], ures=2)
            for s, frac in enumerate((0.5, 0.78, 1.0)):
                px, py = c0[0] + math.cos(az) * Rt * frac, c0[1] + math.sin(az) * Rt * frac
                keyset = ('ev_leaf_b', 'ev_leaf_d', 'ev_leaf_b') if t < 7 else ('ev_leaf_d', 'ev_leaf_a', 'ev_leaf_d')
                blob(nm('pad'), max(1.6, Rt * 0.3), (px, py, z + 0.6 + s * 0.15), keyset[(k + s) % 3], subdiv=1, amp=0.32, scale=(1.15, 1.15, 0.3), seed=t * 11 + k * 3 + s)
        blob(nm('tp'), Rt * 0.45 + 1.2, (c0[0], c0[1], z + 1.0), 'ev_leaf_a' if t > 4 else 'ev_leaf_b', subdiv=1, amp=0.3, scale=(1, 1, 0.34), seed=t)
    top = trunk_point(tr, H, 53, H, 0.3)
    tube(nm('lead'), [(top[0], top[1], H * 0.92), (top[0], top[1], H + 5)], 0.8, 'ev_bark', res=4, taper=[1, 0.2])
    blob(nm('tip'), 2.4, (top[0], top[1], H + 1.0), 'ev_leaf_c', subdiv=1, amp=0.3, scale=(0.8, 0.8, 1.4), seed=5)
    moss_on_trunk(tr, H, 53, 14, rnd, sway=0.3, zmin=1, zmax=16, top_r=0.3)
    ground_bits(tr, rnd, 53, nrock=4, scale=1.2)
    return finalize('ev_ancient_tree_d', smooth_angle=38)


def ancient_e():
    """Gate tree: two old trunks lean together and fuse, leaving an arch you can walk through."""
    reset()
    tr, H1 = 4.6, 46.0
    sep = 14.6
    lean = 0.315
    rnd = random.Random(67)
    tips = []
    for sd in (-1, 1):
        ox = sd * sep
        t = bark_trunk(tr, H1, seed=67 + sd, sway=0.9, flare=1.7, key='ev_bark', top_r=0.78, lean=(-sd * lean, 0.0), ring_h=2.0)
        t.location = (ox, 0, 0)
        roots(tr, n=6, seed=67 + sd, key='ev_bark', span=2.4, ox=ox, oy=0.0)
        for k in range(3):
            z0 = H1 * rnd.uniform(0.45, 0.85)
            p0 = trunk_point(tr, H1, 67 + sd, z0, 0.9, (-sd * lean, 0.0))
            az = (PI if sd > 0 else 0.0) + rnd.uniform(-0.9, 0.9) if k == 0 else rnd.uniform(0, 2 * PI)
            e = limb((ox + p0[0], p0[1], z0), (math.cos(az), math.sin(az), rnd.uniform(0.4, 0.8)), rnd.uniform(11, 17), tr * 0.3, seed=k)
            tips.append(e)
    # fused upper trunk
    t2 = bark_trunk(4.8, 28.0, seed=69, sway=0.6, flare=1.0, key='ev_bark', top_r=0.55, ring_h=2.0)
    t2.location = (0, 0, H1 - 3.0)
    top = trunk_point(4.8, 28.0, 69, 28.0, 0.6)
    zt = H1 - 3.0 + 28.0
    for k in range(7):
        az = 2 * PI * k / 7 + rnd.uniform(-0.3, 0.3)
        z0 = H1 - 3.0 + rnd.uniform(8, 22)
        p0 = trunk_point(4.8, 28.0, 69, z0 - (H1 - 3.0), 0.6)
        e = limb((p0[0], p0[1], z0), (math.cos(az), math.sin(az), rnd.uniform(0.35, 0.7)), rnd.uniform(14, 20), 1.8, seed=k + 40)
        tips.append(e)
    crown(top[0], top[1], zt - 6, 26.0, 16.0, seed=67, count=34)
    for i, e in enumerate(tips):
        cluster(e.x, e.y, e.z + 1.8, rnd.uniform(5.6, 7.6), seed=400 + i, n=6)
    for sd in (-1, 1):   # moss and mushrooms along the arch
        moss_on_trunk(tr, H1, 67 + sd, 12, rnd, sway=0.9, lean=(-sd * lean, 0.0), zmin=1, zmax=30, ox=sd * sep, top_r=0.78)
    for i in range(4):
        ivy_strand((rnd.uniform(-4, 4), rnd.uniform(-2, 2), 33.0 + rnd.uniform(-1, 3)), rnd.uniform(5, 10), seed=i)
    for i in range(4):
        a = rnd.uniform(0, 2 * PI)
        rock(nm('gr'), rnd.uniform(0.9, 1.5), (math.cos(a) * rnd.uniform(14, 18), math.sin(a) * rnd.uniform(9, 13), 0.0), 'ev_stone_dark', seed=i)
    for i in range(6):
        cyl(nm('pth'), 1.4, 0.14, loc=(rnd.uniform(-1, 1), -7 + i * 2.8, 0.0), key='ev_stone', verts=7, rot=(0, 0, rnd.uniform(0, 60)))
    mushrooms(sep + 4.5, -3.0, 0.0, 5, seed=3, scale=1.1)
    fern(-sep - 4.5, 3.0, 0.0, n=7, L=1.7, seed=3)
    fern(sep + 3.8, 4.0, 0.0, n=7, L=1.7, seed=4)
    lantern(0, 0, 21.0, s=1.2, hang=True)
    tube(nm('lch'), [(0, 0, 25.0), (0, 0, 21.0 + 0.9 * 1.2)], 0.06, 'iron', res=4)
    U.marker('mk_deck', (0, -6.0, 0.4))
    return finalize('ev_ancient_tree_e', smooth_angle=38)


# ------------------------------------------------------------------ D05_09..11 canopy clusters
def canopy_a():
    """Dense round crown on a short branch stub."""
    reset()
    rnd = random.Random(71)
    cyl(nm('stub'), 1.3, 5.0, loc=(0, 0, 0), key='ev_bark', verts=8, r2=1.0)
    for k in range(4):
        az = 2 * PI * k / 4 + 0.4
        limb((0, 0, 4.0), (math.cos(az), math.sin(az), 0.8), 6.0, 0.7, seed=k)
    crown(0, 0, 11.0, 13.0, 11.0, seed=71, count=22)
    return finalize('ev_canopy_a', smooth_angle=38)


def canopy_b():
    """Wide flat-topped crown (umbrella shape)."""
    reset()
    rnd = random.Random(73)
    cyl(nm('stub'), 1.4, 6.0, loc=(0, 0, 0), key='ev_bark', verts=8, r2=1.0)
    for k in range(6):
        az = 2 * PI * k / 6 + 0.2
        e = limb((0, 0, 5.5), (math.cos(az), math.sin(az), 0.5), 12.0, 0.8, seed=k)
        cluster(e.x, e.y, e.z + 1.5, 5.4, seed=73 + k, n=6)
    crown(0, 0, 11.0, 22.0, 5.0, seed=73, count=26)
    return finalize('ev_canopy_b', smooth_angle=38)


def canopy_c():
    """Round crown with hanging leaf curtains."""
    reset()
    rnd = random.Random(75)
    cyl(nm('stub'), 1.3, 5.0, loc=(0, 0, 0), key='ev_bark', verts=8, r2=1.0)
    crown(0, 0, 18.0, 14.0, 8.0, seed=75, count=18, keys=LEAF_DEEP)
    for j in range(14):
        a = 2 * PI * j / 14 + rnd.uniform(-0.15, 0.15)
        d = rnd.uniform(6, 12)
        hang_strand(math.cos(a) * d, math.sin(a) * d, 16.0, rnd.uniform(11, 17), rnd)
    tube(nm('tr'), [(0, 0, 4.5), (0, 0, 15.0)], 0.9, 'ev_bark', res=4, taper=[1, 0.6])
    return finalize('ev_canopy_c', smooth_angle=38)


# ------------------------------------------------------------------ D05_12..14 stumps
def stump_a():
    """Big mossy stump with roots, shelf fungi and ferns."""
    reset()
    rnd = random.Random(81)
    r, h = 3.6, 3.6
    bark_trunk(r, h, seed=81, sway=0.15, flare=1.9, key='ev_bark', top_r=0.85, segs=14, ring_h=1.1)
    roots(r, n=7, seed=81, key='ev_bark', span=1.9)
    cyl(nm('top'), r * 0.8, 0.12, loc=(0, 0, h + 0.05), key='ev_wood_aged', verts=14)
    blob(nm('mt'), r * 0.9, (0.2, 0.1, h + 0.1), 'ev_moss', subdiv=2, amp=0.2, scale=(1, 1, 0.22), seed=3)
    for i in range(6):
        a = rnd.uniform(0, 2 * PI)
        ball(nm('sf'), rnd.uniform(0.5, 0.8), loc=(math.cos(a) * r * 0.95, math.sin(a) * r * 0.95, rnd.uniform(0.6, h)), key=rnd.choice(('ev_shroom_brown', 'ev_shroom_cream')), segs=8, rings=4, scale=(1, 1, 0.28))
    mushrooms(r * 1.3, -r * 0.9, 0.0, 6, seed=3, scale=0.9)
    fern(-r * 1.8, r * 1.0, 0.0, n=7, L=1.5, seed=4)
    fern(r * 1.6, r * 1.5, 0.0, n=6, L=1.4, seed=5)
    return finalize('ev_stump_a', smooth_angle=38)


def stump_b():
    """Cleanly cut stump with growth rings, chips and a new sprout."""
    reset()
    rnd = random.Random(83)
    r, h = 3.8, 2.4
    bark_trunk(r, h, seed=83, sway=0.1, flare=1.5, key='ev_bark', top_r=0.9, segs=16, ring_h=0.9)
    roots(r, n=6, seed=83, key='ev_bark', span=1.5)
    cyl(nm('cut'), r * 0.9, 0.14, loc=(0, 0, h - 0.02), key='ev_wood_light', verts=16)
    for k, rr in enumerate((0.7, 1.4, 2.1, 2.8)):
        torus(nm('ring'), rr, 0.045, loc=(0, 0, h + 0.14), key='ev_wood_dark', segs=20, rsegs=3)
    box(nm('kerf'), (1.4, 0.18, 0.08), loc=(1.6, -1.2, h + 0.16), key='ev_wood_dark', rot=(0, 0, 35))
    for i in range(9):
        a = rnd.uniform(0, 2 * PI)
        d = rnd.uniform(r * 1.5, r * 2.8)
        box(nm('chip'), (rnd.uniform(0.35, 0.7), rnd.uniform(0.15, 0.3), 0.1), loc=(math.cos(a) * d, math.sin(a) * d, 0.08), key='ev_wood_light', rot=(0, rnd.uniform(-10, 10), rnd.uniform(0, 180)))
    tube(nm('spr'), [(-3.0, 1.0, 0.8), (-3.2, 1.1, 2.6), (-3.1, 1.3, 4.2)], 0.12, 'ev_bark', res=4, taper=[1, 0.7, 0.4])
    for k in range(5):
        ball(nm('sl'), 0.36, loc=(-3.1 + rnd.uniform(-0.5, 0.5), 1.2 + rnd.uniform(-0.5, 0.5), 3.4 + k * 0.35), key=rnd.choice(('ev_leaf_a', 'ev_leaf_c')), segs=6, rings=4, scale=(1, 0.6, 0.5))
    mushrooms(r * 1.2, r * 1.5, 0.0, 4, seed=5, scale=0.8)
    return finalize('ev_stump_b', smooth_angle=38)


def stump_c():
    """Hollow rotten stump with jagged rim, a sapling growing inside, fungi and ferns."""
    reset()
    rnd = random.Random(85)
    shell([(1.9, 0.0), (3.3, 0.0), (3.0, 5.2), (2.0, 4.6)], 12, 'ev_bark_light')
    cyl(nm('flr'), 2.0, 0.5, loc=(0, 0, 0), key='dirt', verts=12)
    for k in range(7):
        a = 2 * PI * k / 7 + rnd.uniform(-0.2, 0.2)
        hh = rnd.uniform(1.0, 2.8)
        box(nm('jag'), (0.9, 0.5, hh), loc=(math.cos(a) * 2.6, math.sin(a) * 2.6, 4.9 + hh / 2 - 0.2), key='ev_bark_light', rot=(rnd.uniform(-8, 8), rnd.uniform(-8, 8), D(a)), bev=0.04)
    roots(3.0, n=5, seed=85, key='ev_bark', span=1.5)
    tube(nm('spr'), [(0, 0, 0.5), (0.1, 0, 3.0), (-0.1, 0.1, 6.0), (0.1, 0, 8.0)], 0.2, 'ev_bark', res=4, taper=[1.2, 0.8, 0.5, 0.3], ures=3)
    for k in range(7):
        a = 2 * PI * k / 7
        ball(nm('sl'), 0.62, loc=(math.cos(a) * 0.9, math.sin(a) * 0.9, 6.4 + (k % 3) * 0.7), key=rnd.choice(('ev_leaf_a', 'ev_leaf_c', 'ev_leaf_gold')), segs=6, rings=4, scale=(1, 0.7, 0.5))
    ball(nm('sl'), 0.9, loc=(0, 0, 8.4), key='ev_leaf_c', segs=6, rings=4, scale=(1, 1, 0.6))
    for i in range(5):
        a = rnd.uniform(0, 2 * PI)
        ball(nm('sf'), rnd.uniform(0.45, 0.8), loc=(math.cos(a) * 3.15, math.sin(a) * 3.15, rnd.uniform(0.7, 3.8)), key=rnd.choice(('ev_shroom_brown', 'ev_shroom_cream')), segs=8, rings=4, scale=(1, 1, 0.28))
    mushrooms(3.8, 1.5, 0.0, 6, seed=7, scale=1.0)
    fern(-3.6, 2.4, 0.0, n=7, L=1.5, seed=8)
    fern(2.6, -3.6, 0.0, n=6, L=1.4, seed=9)
    blob(nm('mo'), 1.2, (-2.8, -1.8, 0.2), 'ev_moss', subdiv=1, amp=0.3, scale=(1.4, 1, 0.4), seed=2)
    return finalize('ev_stump_c', smooth_angle=38)


# ------------------------------------------------------------------ D05_15..16 logs
def log_a():
    """Fallen log, mossy, with shelf fungi and a snapped branch."""
    reset()
    rnd = random.Random(91)
    L, r = 16.0, 1.9
    cyl(nm('log'), r, L, loc=(-L / 2, 0, r), key='ev_bark', verts=10, rot=(0, 90, 0), r2=r * 0.88)
    for sx, rr in ((-L / 2, r), (L / 2, r * 0.88)):
        cyl(nm('end'), rr * 0.93, 0.14, loc=(sx - (0.07 if sx < 0 else -0.07), 0, r), key='ev_wood_light', verts=10, rot=(0, 90, 0))
        torus(nm('er'), rr * 0.55, 0.04, loc=(sx, 0, r), key='ev_wood_dark', segs=14, rsegs=3, rot=(0, 90, 0))
    for k in range(3):
        x = rnd.uniform(-5, 5)
        tube(nm('brk'), [(x, 0, r * 1.6), (x + rnd.uniform(-0.8, 0.8), rnd.choice((-1, 1)) * 1.3, r * 2.7), (x + rnd.uniform(-1, 1), rnd.choice((-1, 1)) * 2.0, r * 3.1)], 0.3, 'ev_bark', res=4, taper=[1, 0.7, 0.4])
    for i in range(7):
        x = -L / 2 + 1 + i * 2.2 + rnd.uniform(-0.4, 0.4)
        blob(nm('mo'), rnd.uniform(0.8, 1.5), (x, rnd.uniform(-0.5, 0.5), r * 1.9), 'ev_moss', subdiv=1, amp=0.3, scale=(1.5, 1, 0.4), seed=i)
    for i in range(5):
        x = rnd.uniform(-6, 6)
        sd = rnd.choice((-1, 1))
        o = ball(nm('sf'), rnd.uniform(0.5, 0.85), loc=(x, sd * r * 0.92, r * rnd.uniform(0.8, 1.5)), key=rnd.choice(('ev_shroom_brown', 'ev_shroom_cream')), segs=8, rings=4, scale=(1, 0.28, 1))
    mushrooms(-3.5, 2.8, 0.0, 5, seed=2, scale=0.9)
    fern(5.0, -2.8, 0.0, n=7, L=1.5, seed=3)
    fern(-6.5, -2.6, 0.0, n=6, L=1.4, seed=4)
    for i in range(3):
        rock(nm('gr'), rnd.uniform(0.5, 0.9), (rnd.uniform(-7, 7), rnd.choice((-1, 1)) * rnd.uniform(2.4, 3.4), 0.0), 'ev_stone_dark', seed=i)
    return finalize('ev_log_a', smooth_angle=38)


def log_b():
    """Hollow log with an open end, a smaller crossing log, ferns and ivy."""
    reset()
    rnd = random.Random(93)
    L, ro, ri = 13.0, 1.9, 1.0
    o = shell([(ri, 0.0), (ro, 0.0), (ro * 0.9, L), (ri * 0.95, L)], 10, 'ev_bark')
    o.rotation_euler = (0, math.radians(90), 0)
    o.location = (-L / 2, 0, ro)
    cyl(nm('log2'), 1.0, 9.0, loc=(2.5, -2.4, 1.0), key='ev_bark', verts=8, rot=(0, 90, 62), r2=0.85)
    for i in range(6):
        x = -L / 2 + 1 + i * 2.2
        blob(nm('mo'), rnd.uniform(0.8, 1.4), (x, rnd.uniform(-0.4, 0.4), ro * 1.9), 'ev_moss', subdiv=1, amp=0.3, scale=(1.5, 1, 0.4), seed=i)
    for i in range(4):
        sd = rnd.choice((-1, 1))
        ball(nm('sf'), rnd.uniform(0.5, 0.8), loc=(rnd.uniform(-5, 5), sd * ro * 0.93, ro * rnd.uniform(0.9, 1.5)), key=rnd.choice(('ev_shroom_brown', 'ev_shroom_cream')), segs=8, rings=4, scale=(1, 0.28, 1))
    ivy_strand((L / 2 - 1, 0.0, ro * 2.0), 3.0, seed=2)
    for pt in ((-L / 2 - 1.2, 1.4), (L / 2 + 1.2, -1.6), (0.0, 3.0)):
        fern(pt[0], pt[1], 0.0, n=7, L=1.6, seed=int(abs(pt[0] * 3)))
    mushrooms(-2.0, -3.0, 0.0, 6, seed=6, scale=0.9)
    for i in range(3):
        rock(nm('gr'), rnd.uniform(0.5, 0.9), (rnd.uniform(-7, 7), rnd.choice((-1, 1)) * rnd.uniform(3.2, 4.2), 0.0), 'ev_stone_dark', seed=i)
    return finalize('ev_log_b', smooth_angle=38)


# ------------------------------------------------------------------ D05_17 hollow tree (living tree with a doorway)
def hollow_tree():
    reset()
    tr, H = 7.0, 44.0
    seed = 97
    rnd = random.Random(seed)
    trunk = bark_trunk(tr, H, seed=seed, sway=0.5, flare=1.7, key='ev_bark', top_r=0.6, ring_h=1.6)
    door_a = 258.0
    cut_arch(trunk, door_a, tr * 1.45, 2.7, 8.0, 8.5)
    door = math.radians(door_a)
    n = 8
    for i in range(n):
        a = door + 0.7 + (2 * PI - 1.4) * i / (n - 1) + rnd.uniform(-0.05, 0.05)
        c, s = math.cos(a), math.sin(a)
        L = tr * rnd.uniform(2.2, 3.0)
        tube(nm('root'), [(c * tr * 0.5, s * tr * 0.5, tr * 1.1), (c * tr * 1.2, s * tr * 1.2, tr * 0.45), (c * (tr + L * 0.55), s * (tr + L * 0.55), tr * 0.14), (c * (tr + L), s * (tr + L), -0.05)], tr * 0.34, 'ev_bark', res=4, taper=[1, 0.75, 0.5, 0.25], ures=3)
    tips = []
    for k in range(7):
        az = 2 * PI * k / 7 + rnd.uniform(-0.3, 0.3)
        z0 = H * rnd.uniform(0.55, 0.8)
        p0 = trunk_point(tr, H, seed, z0, 0.5)
        e = limb((p0[0], p0[1], z0), (math.cos(az), math.sin(az), rnd.uniform(0.35, 0.7)), rnd.uniform(11, 16), tr * 0.32, seed=k)
        tips.append(e)
    top = trunk_point(tr, H, seed, H, 0.5)
    crown(top[0], top[1], H * 0.86, 17.0, 11.0, seed=seed, count=28)
    for i, e in enumerate(tips):
        cluster(e.x, e.y, e.z + 1.5, rnd.uniform(4.6, 6.2), seed=500 + i, n=6)
    # doorway dressing: stone steps, floor slab, lanterns, hanging lantern inside
    steps(door, tr * 1.4, 1.5, 3, 3.6, key='ev_stone', depth=1.2)
    for sd in (-1, 1):
        px = math.cos(door) * (tr * 1.4 + 4.2) - math.sin(door) * sd * 3.6
        py = math.sin(door) * (tr * 1.4 + 4.2) + math.cos(door) * sd * 3.6
        cyl(nm('lp'), 0.14, 3.4, loc=(px, py, 0.0), key='ev_wood_dark', verts=6)
        lantern(px, py, 3.4 + 1.12 * 0.8, s=0.8, hang=False)
    lantern(math.cos(door) * 4.5, math.sin(door) * 4.5, 7.2 - 0.9 * 0.9, s=0.9, hang=True)
    moss_on_trunk(tr, H, seed, 18, rnd, sway=0.5, zmin=1, zmax=30)
    for i in range(5):
        a = rnd.uniform(0, 2 * PI)
        ball(nm('sf'), rnd.uniform(0.6, 0.95), loc=(math.cos(a) * (tr * 0.95), math.sin(a) * (tr * 0.95), rnd.uniform(9, 24)), key='ev_shroom_cream', segs=8, rings=4, scale=(1, 1, 0.28))
    ground_bits(tr, rnd, seed, nrock=4, scale=1.2)
    U.marker('mk_door', (math.cos(door) * (tr * 1.4 + 1.5), math.sin(door) * (tr * 1.4 + 1.5), 1.8))
    return finalize('ev_hollow_tree', smooth_angle=38)


# ------------------------------------------------------------------ D05_18 sapling
def sapling():
    reset()
    rnd = random.Random(99)
    tube(nm('trk'), [(0, 0, 0), (0.15, 0.05, 3.0), (-0.1, 0.1, 6.0), (0.05, 0, 9.0)], 0.26, 'ev_bark', res=4, taper=[1.5, 1.0, 0.7, 0.4], ures=3)
    tips = []
    for k in range(5):
        az = 2 * PI * k / 5 + rnd.uniform(-0.3, 0.3)
        z = 4.0 + k * 1.1
        e = limb((0, 0, z), (math.cos(az), math.sin(az), 0.8), rnd.uniform(2.4, 3.6), 0.13, seed=k)
        tips.append(e)
    for i, e in enumerate(tips):
        wcluster(e.x, e.y, e.z + 0.3, 1.9, 600 + i, n=3, subdiv=1)
    wcluster(0.05, 0, 9.2, 2.6, 650, n=4, subdiv=1)
    cyl(nm('stk'), 0.09, 7.0, loc=(1.1, 0.6, 0.0), key='ev_wood_aged', verts=5)
    tube(nm('tie'), [(0.15, 0.05, 4.6), (1.1, 0.6, 4.8)], 0.03, 'rope', res=4)
    blob(nm('mnd'), 1.6, (0, 0, 0.0), 'dirt', subdiv=1, amp=0.2, scale=(1, 1, 0.3), seed=1)
    for i in range(7):
        a = 2 * PI * i / 7
        rock(nm('ring'), 0.28, (math.cos(a) * 1.6, math.sin(a) * 1.6, 0.0), 'ev_stone_dark', seed=i)
    fern(-1.8, 1.2, 0.0, n=6, L=1.1, seed=2)
    mushrooms(1.9, -1.2, 0.0, 3, seed=3, scale=0.6)
    return finalize('ev_sapling', smooth_angle=38)


BATCH_D05 = [
    ('D05_04_ancient_tree_a', ancient_a),
    ('D05_05_ancient_tree_b', ancient_b),
    ('D05_06_ancient_tree_c', ancient_c),
    ('D05_07_ancient_tree_d', ancient_d),
    ('D05_08_ancient_tree_e', ancient_e, (0.0, -1.3, 0.25)),
    ('D05_09_canopy_a', canopy_a),
    ('D05_10_canopy_b', canopy_b),
    ('D05_11_canopy_c', canopy_c),
    ('D05_12_stump_a', stump_a),
    ('D05_13_stump_b', stump_b),
    ('D05_14_stump_c', stump_c),
    ('D05_15_log_a', log_a, (0.4, -1.2, 0.5)),
    ('D05_16_log_b', log_b, (0.4, -1.2, 0.5)),
    ('D05_17_hollow_tree', hollow_tree, (-0.3, -1.3, 0.2)),
    ('D05_18_sapling', sapling),
]
BATCH_WORLD = [
    ('D05_01_world_tree_trunk', world_tree_trunk),
    ('D05_02_world_tree_roots', world_tree_roots, (-0.3, -1.3, 0.55)),
    ('D05_03_world_tree_canopy', world_tree_canopy, (0.5, -1.2, 0.2)),
]
