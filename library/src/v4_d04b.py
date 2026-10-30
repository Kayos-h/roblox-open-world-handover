"""v4_d04b - elven ground buildings, part 2: gate arches, market stalls, watch post, stone bridges, pavilion, moon pool, workshop.
Natural woods, mossy stone, green shingles, warm lanterns only (no neon). 1 unit = 1 stud. Front faces -Y.
"""
import math, random
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism
import v4util as U
from v4_elf import nm, lantern, ivy_strand, mushrooms, fern, cabin
from v4_d03 import _plat_ladder
from v4_d04 import (prism_xz, shell, lamp, steps, flagstones, wall_ivy, woodpile, chimney, LEAFS, rnd_key, bush, planter)
from nature import rock, blob

PI = math.pi
D = math.degrees


def sloped_roof(L, d, xc, yc, zr, pitch, keys, sg=1, rows=6, thick=0.14):
    """Half of a gable roof along X: ridge at y=yc, height zr, sloping toward sign sg in Y. Overlapping shingle boards."""
    p = math.radians(pitch)
    for r in range(rows):
        s = (r + 0.5) / rows * d
        box(nm('rof'), (L, d / rows * 1.4, thick), loc=(xc, yc + sg * s * math.cos(p), zr - s * math.sin(p)), key=keys[r % len(keys)], rot=(-sg * pitch, 0, 0), bev=0.02)


SHING = ('ev_shingle_a', 'ev_shingle_b', 'ev_shingle_a', 'ev_shingle_c')


def moss_cap(x, y, z, r, seed):
    blob(nm('mcp'), r, (x, y, z), 'ev_moss', subdiv=1, amp=0.3, scale=(1, 1, 0.4), seed=seed)


# ------------------------------------------------------------------ D04_06 gate arch a (timber gate with a green roof)
def gate_arch_a():
    reset()
    rnd = random.Random(81)
    for sd in (-1, 1):
        x = sd * 5.2
        box(nm('gft'), (3.2, 3.2, 1.0), loc=(x, 0, 0.5), key='ev_stone_dark', bev=0.1)
        box(nm('gpo'), (1.6, 1.6, 14.0), loc=(x, 0, 8.0), key='ev_wood_dark', bev=0.06)
        for zz in (3.0, 7.8, 12.4):
            box(nm('gbd'), (2.0, 2.0, 0.34), loc=(x, 0, zz), key='ev_wood', bev=0.05)
        box(nm('gcp'), (2.3, 2.3, 0.45), loc=(x, 0, 15.2), key='ev_wood_dark', bev=0.05)
        ball(nm('gfn'), 0.38, loc=(x, 0, 15.9), key='bronze', segs=8, rings=6)
        # curved knee braces
        for yy in (0,):
            tube(nm('knee'), [(x - sd * 0.8, 0, 8.6), (x - sd * 1.7, 0, 9.5), (x - sd * 2.9, 0, 10.0)], 0.28, 'ev_wood_dark', res=4, ures=3)
        wall_ivy_post(x, rnd)
    box(nm('gtb'), (11.8, 1.0, 0.8), loc=(0, 0, 10.2), key='ev_wood_dark', bev=0.05)
    tube(nm('glt'), [(-7.2, 0, 13.2), (-3.8, 0, 15.0), (0, 0, 15.7), (3.8, 0, 15.0), (7.2, 0, 13.2)], 0.58, 'ev_wood_dark', res=4, ures=4)
    for x in (-7.2, 7.2):
        ball(nm('gle'), 0.5, loc=(x, 0, 13.4), key='bronze', segs=8, rings=6)
    for x in (-3.0, 0.0, 3.0):
        tube(nm('gsp'), [(x, 0, 10.5), (x, 0, 15.2)], 0.2, 'ev_wood', res=4)
    for sg in (-1, 1):
        sloped_roof(16.4, 3.9, 0, 0, 18.2, 25, SHING, sg=sg, rows=7)
    tube(nm('rdg'), [(-8.4, 0, 18.35), (8.4, 0, 18.35)], 0.26, 'ev_wood_dark', res=4)
    for x in (-8.4, 8.4):
        ball(nm('rdb'), 0.42, loc=(x, 0, 18.45), key='bronze', segs=8, rings=6)
    box(nm('ban'), (3.2, 0.12, 6.4), loc=(0, 0, 6.8), key='ev_banner_green')
    box(nm('bag'), (3.2, 0.14, 0.5), loc=(0, 0, 9.7), key='ev_banner_gold')
    box(nm('bag2'), (3.2, 0.14, 0.4), loc=(0, 0, 4.0), key='ev_banner_gold')
    tube(nm('brd'), [(-1.8, 0, 9.85), (1.8, 0, 9.85)], 0.08, 'bronze', res=4)
    for x in (-3.4, 3.4):
        lantern(x, 0, 9.8 - 0.9 * 0.9, s=0.9, hang=True)
    for sd in (-1, 1):
        for k, wx in enumerate((10.6, 15.6)):
            x = sd * wx
            box(nm('gw'), (5.4, 1.8, 3.4), loc=(x, 0, 1.7), key='ev_stone', bev=0.1)
            box(nm('gwc'), (5.6, 2.1, 0.32), loc=(x, 0, 3.55), key='ev_stone_warm', bev=0.05)
            moss_cap(x, rnd.uniform(-0.5, 0.5), 3.7, 1.3, k + 3 * (sd + 2))
    for i in range(6):
        cyl(nm('pth'), 1.4, 0.14, loc=(rnd.uniform(-0.8, 0.8), -5.0 + i * 2.0, 0.0), key='ev_stone', verts=7, rot=(0, 0, rnd.uniform(0, 60)))
    for sd in (-1, 1):
        fern(sd * 4.2, -3.4, 0.0, n=7, L=1.6, seed=sd + 4)
        mushrooms(sd * 7.8, 2.0, 0.0, 3, seed=sd + 7, scale=0.8)
    U.marker('mk_deck', (0, 0, 0.5))
    return finalize('ev_gate_arch_a', smooth_angle=38)


def wall_ivy_post(x, rnd):
    for i in range(10):
        z = rnd.uniform(1.0, 9.0)
        ball(nm('ivp'), rnd.uniform(0.22, 0.34), loc=(x + rnd.uniform(-0.9, 0.9), -0.85 if i % 2 else 0.85, z), key=LEAFS[i % 3], segs=6, rings=4, scale=(1, 0.5, 1))
    ivy_strand((x, -0.85, 9.0), 6.0, seed=int(abs(x)))


# ------------------------------------------------------------------ D04_07 gate arch b (stone arch grown over with ivy)
def gate_arch_b():
    reset()
    rnd = random.Random(83)
    cz, rin, rout = 6.4, 4.6, 6.3
    for sd in (-1, 1):
        box(nm('pr'), (1.9, 3.0, cz), loc=(sd * (rin + 0.95), 0, cz / 2), key='ev_stone_warm', bev=0.1)
        box(nm('prf'), (2.5, 3.5, 1.0), loc=(sd * (rin + 0.95), 0, 0.5), key='ev_stone_dark', bev=0.1)
    n = 13
    for i in range(n):
        t0 = PI - PI * i / n + 0.012
        t1 = PI - PI * (i + 1) / n - 0.012
        pts = [(math.cos(t0) * rin, cz + math.sin(t0) * rin), (math.cos(t1) * rin, cz + math.sin(t1) * rin), (math.cos(t1) * rout, cz + math.sin(t1) * rout), (math.cos(t0) * rout, cz + math.sin(t0) * rout)]
        prism_xz(pts, -1.5, 1.5, 'ev_stone_warm' if i % 2 else 'ev_stone')
    # keystone and carved leaf band
    box(nm('key'), (1.5, 3.4, 2.3), loc=(0, 0, cz + rin + 0.9), key='ev_stone_warm', bev=0.1)
    ball(nm('klf'), 0.65, loc=(0, -1.75, cz + rin + 0.9), key='ev_leaf_c', segs=6, rings=4, scale=(1, 0.4, 1.4))
    box(nm('cap'), (rout * 2 + 1.0, 3.3, 0.9), loc=(0, 0, cz + rout + 0.45), key='ev_stone', bev=0.1)
    for i in range(7):
        box(nm('mer'), (1.3, 1.2, 1.0), loc=(-5.4 + i * 1.8, 0, cz + rout + 1.4), key='ev_stone_warm', bev=0.08)
    for sd in (-1, 1):
        for k, wx in enumerate((10.0, 14.4)):
            x = sd * wx
            box(nm('gw'), (4.8, 2.2, 5.0), loc=(x, 0, 2.5), key='ev_stone', bev=0.1)
            box(nm('gwc'), (5.0, 2.5, 0.4), loc=(x, 0, 5.15), key='ev_stone_warm', bev=0.06)
            moss_cap(x + rnd.uniform(-1, 1), 0, 5.3, 1.4, k + 5 * (sd + 2))
        lamp(sd * 6.2, -1.0, cz + rout + 0.9, 2.8, 0.8)
    lantern(0, -0.8, cz + rin - 0.85 - 0.9 * 0.9, s=0.9, hang=True)
    for i in range(46):
        side = rnd.choice((-1, 1))
        a = rnd.uniform(0, PI)
        r = rnd.uniform(rin + 0.1, rout + 0.2) if rnd.random() < 0.5 else None
        if r is None:
            x, z = side * rnd.uniform(rin, rin + 1.9), rnd.uniform(0.6, cz)
        else:
            x, z = math.cos(a) * r, cz + math.sin(a) * r
        o = ball(nm('ivy'), rnd.uniform(0.2, 0.36), loc=(x, rnd.choice((-1, 1)) * 1.55, z), key=LEAFS[i % 3], segs=6, rings=4, scale=(1, 0.5, 1))
    for i in range(7):
        ivy_strand((rnd.uniform(-rin + 0.4, rin - 0.4), rnd.choice((-1, 1)) * 1.4, cz + math.sqrt(max(0.1, rin * rin - 1)) - 0.6 if False else cz + rin - 0.3), rnd.uniform(1.8, 4.0), seed=i)
    for i in range(14):
        box(nm('blk'), (rnd.uniform(0.9, 1.5), 0.2, 0.5), loc=(rnd.choice((-1, 1)) * rnd.uniform(rin + 0.2, rin + 1.7), rnd.choice((-1, 1)) * 1.55, rnd.uniform(0.5, cz - 0.6)), key='ev_stone_dark')
    for i in range(6):
        cyl(nm('pth'), 1.4, 0.14, loc=(rnd.uniform(-0.8, 0.8), -5.0 + i * 2.0, 0.0), key='ev_stone', verts=7, rot=(0, 0, rnd.uniform(0, 60)))
    for sd in (-1, 1):
        fern(sd * 6.4, -2.6, 0.0, n=7, L=1.6, seed=sd + 9)
        mushrooms(sd * 11.2, 2.4, 0.0, 3, seed=sd + 2, scale=0.8)
    return finalize('ev_gate_arch_b', smooth_angle=38)


# ------------------------------------------------------------------ D04_08..10 market stalls
def _stall(w, d, keys, seed, awning_pitch=None):
    """Four posts, counter, back shelf and a striped canvas awning with a scalloped front. Front faces -Y."""
    rnd = random.Random(seed)
    hf, hb = 6.4, 8.0
    for sx in (-1, 1):
        cyl(nm('sp'), 0.18, hf, loc=(sx * w / 2, -d / 2, 0.0), key='ev_wood_dark', verts=6)
        cyl(nm('sp'), 0.18, hb, loc=(sx * w / 2, d / 2, 0.0), key='ev_wood_dark', verts=6)
        ball(nm('spc'), 0.24, loc=(sx * w / 2, -d / 2, hf + 0.05), key='bronze', segs=6, rings=4)
    # counter
    box(nm('ctr'), (w - 0.4, 1.4, 0.22), loc=(0, -d / 2 + 0.9, 3.3), key='ev_wood_light', bev=0.03)
    box(nm('cfr'), (w - 0.4, 1.3, 2.9), loc=(0, -d / 2 + 0.9, 1.5), key='ev_wood', bev=0.04)
    for k in range(5):
        box(nm('cpl'), (0.08, 0.06, 2.9), loc=(-w / 2 + 0.6 + k * (w - 1.2) / 4, -d / 2 + 0.2, 1.5), key='ev_wood_dark')
    # back shelves
    for zz in (2.4, 4.6):
        box(nm('shf'), (w - 0.5, 0.9, 0.18), loc=(0, d / 2 - 0.7, zz), key='ev_wood', bev=0.03)
    # awning
    pitch = awning_pitch or math.degrees(math.atan((hb - hf) / (d + 0.3)))
    ln = math.hypot(d + 1.8, hb - hf)
    n = 8
    sw = (w + 1.2) / n
    ym = 0.0
    for i in range(n):
        x = -(w + 1.2) / 2 + sw * (i + 0.5)
        k = keys[i % len(keys)]
        box(nm('awn'), (sw * 1.02, ln, 0.13), loc=(x, ym, (hf + hb) / 2 + 0.12), key=k, rot=(pitch, 0, 0), bev=0.015)
        box(nm('scl'), (sw * 0.92, 0.06, 0.55), loc=(x, -d / 2 - 0.95, hf - 0.12), key=k)
    tube(nm('frt'), [(-w / 2 - 0.6, -d / 2 - 0.9, hf + 0.15), (w / 2 + 0.6, -d / 2 - 0.9, hf + 0.15)], 0.06, 'rope_dark', res=4)
    for sx in (-1, 1):
        lantern(sx * (w / 2 - 0.7), -d / 2 - 0.4, hf - 0.2 - 0.9 * 0.7, s=0.7, hang=True)
    return rnd


def stall_a():
    reset()
    w, d = 8.0, 5.6
    rnd = _stall(w, d, ('ev_banner_green', 'canvas'), 91)
    zc = 3.41
    fruits = ('fruit', 'fl_orange', 'ev_leaf_gold', 'ev_leaf_c')
    for i, x in enumerate((-2.6, 0.0, 2.6)):
        cyl(nm('bsk'), 0.95, 0.7, loc=(x, -d / 2 + 0.9, zc), key='ev_thatch', verts=10, r2=0.8)
        torus(nm('bkr'), 0.95, 0.07, loc=(x, -d / 2 + 0.9, zc + 0.7), key='ev_wood_dark', segs=10, rsegs=3)
        for layer, (cnt, rr) in enumerate(((7, 0.55), (4, 0.3), (1, 0.0))):
            for k in range(cnt):
                a = 2 * PI * k / max(1, cnt) + layer
                ball(nm('frt'), 0.27, loc=(x + math.cos(a) * rr, -d / 2 + 0.9 + math.sin(a) * rr, zc + 0.78 + layer * 0.26), key=fruits[(i + layer) % 4], segs=6, rings=4)
    for i, x in enumerate((-2.8, 0.2)):
        box(nm('crt'), (2.0, 1.4, 0.9), loc=(x, d / 2 - 0.8, 0.45), key='ev_wood_aged', rot=(0, 0, rnd.uniform(-8, 8)), bev=0.04)
        for k in range(6):
            ball(nm('frt'), 0.27, loc=(x - 0.6 + (k % 3) * 0.6, d / 2 - 0.8 + (k // 3 - 0.5) * 0.5, 1.05), key=fruits[(i + k) % 4], segs=6, rings=4)
    for x in (2.8,):
        blob(nm('sck'), 0.95, (x, d / 2 - 0.9, 0.75), 'canvas', subdiv=1, amp=0.2, scale=(1, 1, 1.0), seed=2)
        blob(nm('sck'), 0.8, (x + 1.1, d / 2 - 1.5, 0.6), 'canvas_b', subdiv=1, amp=0.2, scale=(1, 1, 1.0), seed=3)
    for k in range(5):   # hanging garlic and onion braids
        x = -3.0 + k * 1.5
        tube(nm('brd'), [(x, d / 2 - 0.3, 6.6), (x, d / 2 - 0.3, 4.9)], 0.04, 'rope', res=4)
        for j in range(4):
            ball(nm('onn'), 0.2, loc=(x + (j % 2 - 0.5) * 0.15, d / 2 - 0.3, 5.0 + j * 0.36), key='canvas_b' if k % 2 else 'fl_white', segs=6, rings=4)
    box(nm('sgn'), (2.4, 0.12, 1.1), loc=(0, -d / 2 - 0.5, 4.5), key='ev_wood_dark')
    box(nm('sgi'), (2.0, 0.14, 0.7), loc=(0, -d / 2 - 0.52, 4.5), key='ev_wood_light')
    for z in (0.0,):
        cyl(nm('bar'), 0.7, 1.4, loc=(-w / 2 - 1.3, -d / 2 + 0.4, 0.0), key='ev_wood_dark', verts=10)
    mushrooms(w / 2 + 1.0, d / 2, 0.0, 3, seed=5, scale=0.8)
    U.marker('mk_deck', (0, -d / 2 - 1.2, 0.4))
    return finalize('ev_stall_a', smooth_angle=38)


def stall_b():
    reset()
    w, d = 8.0, 5.6
    rnd = _stall(w, d, ('ev_banner_gold', 'ev_banner_green', 'canvas'), 93)
    zc = 3.41
    # herb bundles hanging from the awning front rail
    for k in range(12):
        x = -w / 2 + 0.7 + k * (w - 1.4) / 11
        zt = 6.35 - rnd.uniform(0, 0.1)
        L = rnd.uniform(1.2, 2.0)
        tube(nm('hrb'), [(x, -d / 2 - 0.55, zt), (x, -d / 2 - 0.55, zt - 0.4)], 0.04, 'rope', res=4)
        lathe(nm('hbl'), [(0, 0), (0.26, 0.05), (0.3, L * 0.25), (0.2, L * 0.7), (0.06, L)], loc=(x, -d / 2 - 0.55, zt - 0.4 - L), key=('ev_fern', 'ev_leaf_c', 'ev_leaf_d', 'ev_moss')[k % 4], segs=6)
        if k % 3 == 0:
            ball(nm('hfl'), 0.14, loc=(x, -d / 2 - 0.55, zt - 0.4 - L * 0.1), key=('fl_purple', 'fl_white', 'fl_yellow')[k % 3], segs=6, rings=4)
    # counter: jars, mortar, scales, baskets of dried leaves
    for i, x in enumerate((-3.0, -2.0, -1.0)):
        cyl(nm('jar'), 0.38, 0.75, loc=(x, -d / 2 + 1.2, zc), key=('glass_dark', 'terracotta', 'glass_dark')[i], verts=8)
        cyl(nm('jlid'), 0.4, 0.14, loc=(x, -d / 2 + 1.2, zc + 0.75), key='ev_wood', verts=8)
    cyl(nm('mrt'), 0.55, 0.5, loc=(0.7, -d / 2 + 1.0, zc), key='ev_stone', verts=10, r2=0.4)
    cyl(nm('pst'), 0.1, 0.9, loc=(0.8, -d / 2 + 1.0, zc + 0.35), key='ev_wood_dark', verts=6, rot=(0, 18, 0))
    tube(nm('scl'), [(2.1, -d / 2 + 0.9, zc + 1.3), (2.1, -d / 2 + 0.9, zc)], 0.05, 'bronze', res=4)
    tube(nm('scb'), [(1.5, -d / 2 + 0.9, zc + 1.28), (2.7, -d / 2 + 0.9, zc + 1.28)], 0.04, 'bronze', res=4)
    for sx in (1.5, 2.7):
        cyl(nm('scp'), 0.28, 0.05, loc=(sx, -d / 2 + 0.9, zc + 0.75), key='bronze', verts=8)
    for i, x in enumerate((3.2,)):
        cyl(nm('bsk'), 0.7, 0.55, loc=(x, -d / 2 + 1.1, zc), key='ev_thatch', verts=10, r2=0.55)
        for k in range(5):
            blob(nm('drl'), 0.28, (x + rnd.uniform(-0.3, 0.3), -d / 2 + 1.1 + rnd.uniform(-0.3, 0.3), zc + 0.7), 'ev_leaf_gold', subdiv=1, amp=0.3, scale=(1, 1, 0.6), seed=k)
    # back shelves: jars and small pots
    for zz in (2.4 + 0.1, 4.6 + 0.1):
        for k in range(8):
            x = -w / 2 + 0.7 + k * (w - 1.4) / 7
            cyl(nm('shj'), 0.3, 0.7 + (k % 3) * 0.12, loc=(x, d / 2 - 0.7, zz), key=('terracotta', 'glass_dark', 'ev_stone_warm', 'terracotta_dark')[(k + int(zz)) % 4], verts=7)
    for k in range(3):   # drying racks with leaves
        tube(nm('rck'), [(-w / 2 + 0.3, d / 2 - 1.5 + k * 0.01, 5.8), (w / 2 - 0.3, d / 2 - 1.5, 5.8)], 0.05, 'ev_wood_dark', res=4)
        break
    for k in range(7):
        x = -w / 2 + 0.9 + k * 1.0
        blob(nm('dry'), 0.3, (x, d / 2 - 1.5, 5.4), 'ev_leaf_gold' if k % 2 else 'ev_moss', subdiv=1, amp=0.3, scale=(0.7, 0.7, 1.4), seed=k)
    cyl(nm('stl'), 0.5, 1.0, loc=(-w / 2 - 1.2, 0.0, 0.0), key='ev_wood_dark', verts=8)
    box(nm('sgn'), (2.6, 0.12, 1.1), loc=(0, -d / 2 - 0.5, 4.5), key='ev_wood_dark')
    box(nm('sgi'), (2.2, 0.14, 0.7), loc=(0, -d / 2 - 0.52, 4.5), key='ev_leaf_b')
    fern(w / 2 + 1.0, 1.0, 0.0, n=6, L=1.3, seed=3)
    U.marker('mk_deck', (0, -d / 2 - 1.2, 0.4))
    return finalize('ev_stall_b', smooth_angle=38)


def stall_c():
    reset()
    w, d = 8.0, 5.6
    rnd = _stall(w, d, ('ev_banner_green', 'ev_banner_gold'), 95)
    zc = 3.41
    cols = ('ev_banner_green', 'ev_banner_gold', 'canvas', 'plaster_purple', 'canvas_b', 'plaster_rose')
    # shelves of cloth bolts (horizontal rolls)
    for row, zz in enumerate((2.4, 4.6)):
        for k in range(6):
            x = -w / 2 + 0.9 + k * (w - 1.8) / 5
            cyl(nm('blt'), 0.34, 0.9, loc=(x, d / 2 - 0.9, zz + 0.38), key=cols[(k + row * 2) % 6], verts=8, rot=(90, 0, 0))
    # folded cloth stacks on the counter
    for i, x in enumerate((-2.9, -1.1, 0.7)):
        for j in range(4):
            box(nm('fld'), (1.3 - j * 0.05, 1.0, 0.18), loc=(x, -d / 2 + 1.15, zc + 0.1 + j * 0.18), key=cols[(i + j) % 6], bev=0.02)
    for k in range(3):   # yarn baskets
        x = 2.3 + k * 0.0
    cyl(nm('ybk'), 0.7, 0.5, loc=(2.8, -d / 2 + 1.1, zc), key='ev_thatch', verts=10, r2=0.55)
    for k in range(5):
        a = 2 * PI * k / 5
        ball(nm('yrn'), 0.26, loc=(2.8 + math.cos(a) * 0.3, -d / 2 + 1.1 + math.sin(a) * 0.3, zc + 0.62), key=cols[(k + 1) % 6], segs=6, rings=4)
    # hanging cloths from the front rail
    for k in range(7):
        x = -w / 2 + 0.8 + k * (w - 1.6) / 6
        L = 2.2 + (k % 3) * 0.6
        box(nm('hcl'), (0.9, 0.05, L), loc=(x, -d / 2 - 0.55, 6.25 - L / 2), key=cols[k % 6])
    # spinning wheel and small loom beside the stall
    xw = w / 2 + 2.0
    torus(nm('swh'), 1.0, 0.07, loc=(xw, 0.0, 1.4), key='ev_wood_dark', segs=16, rsegs=3, rot=(0, 90, 0))
    for k in range(6):
        a = PI * k / 6
        tube(nm('sps'), [(xw, math.cos(a) * 1.0, 1.4 + math.sin(a) * 1.0), (xw, -math.cos(a) * 1.0, 1.4 - math.sin(a) * 1.0)], 0.03, 'ev_wood', res=4)
    box(nm('swb'), (0.3, 2.6, 0.3), loc=(xw, 0.0, 0.5), key='ev_wood_dark', bev=0.03)
    for sd in (-1, 1):
        tube(nm('swl'), [(xw, sd * 1.0, 0.5), (xw, sd * 0.8, 2.6)], 0.09, 'ev_wood_dark', res=4)
    xl = -w / 2 - 2.6
    for sd in (-1, 1):
        cyl(nm('lmp'), 0.12, 4.2, loc=(xl, sd * 1.5, 0.0), key='ev_wood_dark', verts=6)
    for zz in (0.5, 4.5):
        box(nm('lmb'), (0.22, 3.3, 0.22), loc=(xl, 0.0, zz), key='ev_wood_dark')
    for k in range(11):
        y = -1.4 + k * 0.28
        tube(nm('lmt'), [(xl, y, 0.6), (xl, y, 4.4)], 0.015, 'canvas_b' if k % 3 else 'ev_banner_gold', res=4)
    box(nm('lmw'), (0.1, 3.0, 1.3), loc=(xl, 0.0, 1.6), key='ev_banner_green')
    box(nm('sgn'), (2.6, 0.12, 1.1), loc=(0, -d / 2 - 0.5, 4.5), key='ev_wood_dark')
    box(nm('sgi'), (2.2, 0.14, 0.7), loc=(0, -d / 2 - 0.52, 4.5), key='ev_banner_gold')
    U.marker('mk_deck', (0, -d / 2 - 1.2, 0.4))
    return finalize('ev_stall_c', smooth_angle=38)


# ------------------------------------------------------------------ D04_11 watch post
def watch_post():
    reset()
    rnd = random.Random(101)
    zd, hb, ht = 17.2, 3.4, 2.5

    def leg(i, z):
        sx, sy = (1, 1, -1, -1)[i], (1, -1, -1, 1)[i]
        t = z / zd
        rr = hb + (ht - hb) * t
        return (sx * rr, sy * rr, z)

    for i in range(4):
        tube(nm('leg'), [leg(i, 0.0), leg(i, zd / 2), leg(i, zd)], 0.5, 'ev_wood_dark', res=4, taper=[1.2, 1.0, 0.9], ures=2)
        cyl(nm('lft'), 1.0, 0.7, loc=(leg(i, 0)[0], leg(i, 0)[1], -0.1), key='ev_stone_dark', verts=7)
    for z in (4.8, 10.6):
        for i in range(4):
            tube(nm('rb'), [leg(i, z), leg((i + 1) % 4, z)], 0.24, 'ev_wood', res=4)
            torus(nm('lsh'), 0.62, 0.09, loc=leg(i, z), key='rope_dark', segs=10, rsegs=3)
    for lo, hi in ((0.5, 4.8), (4.8, 10.6), (10.6, zd - 0.8)):
        for i in range(4):
            j = (i + 1) % 4
            tube(nm('xb'), [leg(i, lo), leg(j, hi)], 0.12, 'rope_dark', res=4)
            tube(nm('xb'), [leg(j, lo), leg(i, hi)], 0.12, 'rope_dark', res=4)
    # platform
    hp = 3.9
    n = 8
    for k in range(n):
        y = -hp + 2 * hp * (k + 0.5) / n
        box(nm('plk'), (2 * hp, 2 * hp / n - 0.06, 0.3), loc=(0, y, zd - 0.15), key=('ev_wood', 'ev_wood_light', 'ev_wood')[k % 3], bev=0.03)
    for sd in (-1, 1):
        box(nm('pfb'), (2 * hp + 0.4, 0.5, 0.6), loc=(0, sd * (hp - 0.2), zd - 0.6), key='ev_wood_dark', bev=0.05)
        box(nm('pfc'), (0.5, 2 * hp + 0.4, 0.6), loc=(sd * (hp - 0.2), 0, zd - 0.6), key='ev_wood_dark', bev=0.05)
    # railings with an opening at the front for the ladder
    def rail_run(p0, p1, gap=None):
        pts = []
        m = 4
        for i in range(m + 1):
            t = i / m
            pts.append((p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t))
        return pts
    sides = [((-hp, hp), (hp, hp)), ((hp, hp), (hp, -hp)), ((-hp, hp), (-hp, -hp))]
    for p0, p1 in sides:
        pts = rail_run(p0, p1)
        for x, y in pts:
            cyl(nm('rp'), 0.13, 3.0, loc=(x, y, zd), key='ev_wood', verts=6)
        tube(nm('rt'), [(x, y, zd + 3.0) for x, y in pts], 0.12, 'ev_wood_light', res=4)
        tube(nm('rm'), [(x, y, zd + 1.5) for x, y in pts], 0.08, 'ev_wood', res=4)
    for sd, (a, b) in ((-1, ((-hp, -hp), (-1.7, -hp))), (1, ((1.7, -hp), (hp, -hp)))):
        pts = rail_run(a, b)
        for x, y in pts:
            cyl(nm('rp'), 0.13, 3.0, loc=(x, y, zd), key='ev_wood', verts=6)
        tube(nm('rt'), [(x, y, zd + 3.0) for x, y in pts], 0.12, 'ev_wood_light', res=4)
        tube(nm('rm'), [(x, y, zd + 1.5) for x, y in pts], 0.08, 'ev_wood', res=4)
    for x in (-1.7, 1.7):
        cyl(nm('gp'), 0.18, 3.7, loc=(x, -hp, zd), key='ev_wood_dark', verts=6)
        lantern(x, -hp, zd + 3.7 + 1.12 * 0.7, s=0.7, hang=False)
    _plat_ladder(0, 0, zd, hp, -PI / 2)
    # lookout roof on four posts, bell, banner
    zt = zd + 5.8
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl(nm('lpo'), 0.26, 5.8, loc=(sx * (hp - 0.5), sy * (hp - 0.5), zd), key='ev_wood_dark', verts=6)
    for sd in (-1, 1):
        box(nm('lbm'), (2 * hp, 0.45, 0.5), loc=(0, sd * (hp - 0.5), zt - 0.2), key='ev_wood_dark', bev=0.04)
        box(nm('lbm'), (0.45, 2 * hp, 0.5), loc=(sd * (hp - 0.5), 0, zt - 0.2), key='ev_wood_dark', bev=0.04)
    lathe(nm('roof'), [(0, zt + 4.4), (6.6, zt + 0.1), (6.6, zt - 0.2), (0, zt - 0.2)], key='ev_shingle_a', segs=4)
    for i in range(4):
        a = PI / 4 + PI / 2 * i
        tube(nm('rid'), [(math.cos(a) * 6.6, math.sin(a) * 6.6, zt + 0.15), (0, 0, zt + 4.45)], 0.14, 'ev_wood_dark', res=4)
    ball(nm('fin'), 0.36, loc=(0, 0, zt + 4.6), key='bronze', segs=8, rings=6)
    tube(nm('bel'), [(0, 0, zt - 0.2), (0, 0, zt - 1.2)], 0.05, 'iron', res=4)
    lathe(nm('bell'), [(0.62, 0), (0.55, 0.3), (0.38, 0.9), (0.18, 1.15), (0.0, 1.2)], loc=(0, 0, zt - 2.4), key='bronze', segs=10)
    box(nm('ban'), (0.12, 1.6, 4.0), loc=(hp - 0.5 + 0.35, 0.0, zd + 4.5), key='ev_banner_green')
    lantern(0, 2.4, zt - 0.5 - 0.9 * 0.8, s=0.8, hang=True)
    for i in range(2):
        mushrooms(5.0, 4.5 - i * 4, 0.0, 3, seed=i, scale=0.8)
    fern(-5.2, 3.2, 0.0, n=7, L=1.5, seed=2)
    fern(5.2, -4.8, 0.0, n=7, L=1.5, seed=4)
    U.marker('mk_deck', (0, 0, zd + 0.4))
    return finalize('ev_watch_post', smooth_angle=38)


# ------------------------------------------------------------------ D04_12 / 13 stone bridges
def _stone_bridge(arches, L_half, W, bank_z, hump, name, seed):
    reset()
    rnd = random.Random(seed)

    def ztop(x):
        return bank_z + hump * (1 - (x / L_half) ** 2)

    def slope_deg(x):
        return D(math.atan(2 * hump * x / (L_half ** 2)))

    pts = [(-L_half, 0.0)]
    ring = []
    for (cx, span, rise) in arches:
        r = span * span / (8 * rise) + rise / 2
        cz = rise - r
        th0 = math.asin(span / 2 / r)
        a0, a1 = PI / 2 + th0, PI / 2 - th0
        ring.append((cx, cz, r, a0, a1))
        n = 14
        pts.append((cx - span / 2, 0.0))
        for i in range(1, n):
            a = a0 + (a1 - a0) * i / n
            pts.append((cx + r * math.cos(a), cz + r * math.sin(a)))
        pts.append((cx + span / 2, 0.0))
    pts.append((L_half, 0.0))
    xs_top = [L_half - 2 * L_half * i / 24 for i in range(25)]
    for x in xs_top:
        pts.append((x, ztop(x)))
    prism_xz(pts, -W / 2, W / 2, 'ev_stone')
    # voussoir rings on both faces
    for (cx, cz, r, a0, a1) in ring:
        nv = 11
        for i in range(nv):
            t0 = a0 + (a1 - a0) * i / nv - 0.0
            t1 = a0 + (a1 - a0) * (i + 1) / nv
            t0, t1 = t0 - 0.006, t1 + 0.006
            q = [(cx + r * math.cos(t0), cz + r * math.sin(t0)), (cx + r * math.cos(t1), cz + r * math.sin(t1)), (cx + (r + 1.0) * math.cos(t1), cz + (r + 1.0) * math.sin(t1)), (cx + (r + 1.0) * math.cos(t0), cz + (r + 1.0) * math.sin(t0))]
            for y0, y1 in ((W / 2, W / 2 + 0.3), (-W / 2 - 0.3, -W / 2)):
                prism_xz(q, y0, y1, 'ev_stone_warm' if i % 2 else 'ev_stone')
            # soffit lining in the arch
        # keystone accent
        kx, kz = cx, cz + r + 0.5
        for yy in (W / 2 + 0.32, -W / 2 - 0.32):
            box(nm('kst'), (1.0, 0.16, 1.5), loc=(kx, yy, kz), key='ev_stone_warm', bev=0.04)
    # road paving and parapets
    m = int(2 * L_half / 2.0)
    for i in range(m):
        xm = -L_half + 2.0 * (i + 0.5)
        zt = ztop(xm)
        rot = (0, slope_deg(xm), 0)
        box(nm('rd'), (2.02, W - 2.4, 0.14), loc=(xm, 0, zt + 0.05), key='ev_stone_dark' if i % 2 else 'ev_stone', rot=rot, bev=0.02)
        for sd in (-1, 1):
            box(nm('par'), (2.05, 0.8, 1.5), loc=(xm, sd * (W / 2 - 0.45), zt + 0.75), key='ev_stone_warm', rot=rot, bev=0.05)
            box(nm('pcp'), (2.1, 1.05, 0.26), loc=(xm, sd * (W / 2 - 0.45), zt + 1.58), key='ev_stone', rot=rot, bev=0.04)
            if i % 4 == 1:
                moss_cap(xm, sd * (W / 2 - 0.45), zt + 1.75, 0.8, i + 7)
    # block texture and moss on the faces
    for i in range(110):
        x = rnd.uniform(-L_half + 1.0, L_half - 1.0)
        z = rnd.uniform(0.5, ztop(x) - 0.6)
        if any(math.hypot(x - cx, z - cz) < r + 1.2 for (cx, cz, r, a0, a1) in ring):
            continue
        sd = rnd.choice((-1, 1))
        if rnd.random() < 0.7:
            box(nm('blk'), (rnd.uniform(0.9, 1.7), 0.18, 0.55), loc=(x, sd * (W / 2 + 0.06), z), key=rnd.choice(('ev_stone_dark', 'ev_stone_warm', 'ev_stone_dark')), bev=0.02)
        else:
            blob(nm('mos'), rnd.uniform(0.35, 0.8), (x, sd * (W / 2 + 0.05), z), 'ev_moss', subdiv=1, amp=0.3, scale=(1, 0.3, 0.8), seed=i)
    # lamps, ivy, plants
    for sx in (-1, 1):
        for sd in (-1, 1):
            lamp(sx * (L_half - 1.8), sd * (W / 2 - 0.45), ztop(sx * (L_half - 1.8)) + 1.5, 2.6, 0.8)
    for sd in (-1, 1):
        lamp(0.0, sd * (W / 2 - 0.45), ztop(0.0) + 1.5, 2.6, 0.8)
    for i in range(8):
        x = rnd.uniform(-L_half * 0.8, L_half * 0.8)
        ivy_strand((x, rnd.choice((-1, 1)) * (W / 2 + 0.3), ztop(x) + 0.5), rnd.uniform(2.5, 4.5), seed=i)
    for sx in (-1, 1):
        fern(sx * (L_half + 0.2), W / 2 + 1.2, bank_z - 0.2, n=7, L=1.5, seed=sx + 3)
        fern(sx * (L_half - 1.0), -W / 2 - 1.2, bank_z - 0.2, n=7, L=1.5, seed=sx + 8)
    U.marker('mk_conn', (-L_half, 0, ztop(-L_half)))
    U.marker('mk_conn', (L_half, 0, ztop(L_half)))
    return finalize(name, smooth_angle=38)


def stone_bridge_a():
    return _stone_bridge([(0.0, 14.0, 4.6)], 17.0, 7.0, 5.2, 1.7, 'ev_stone_bridge_a', 111)


def stone_bridge_b():
    return _stone_bridge([(-9.5, 14.0, 4.8), (9.5, 14.0, 4.8)], 25.0, 7.0, 5.4, 2.2, 'ev_stone_bridge_b', 113)


# ------------------------------------------------------------------ D04_14 pavilion
def pavilion():
    reset()
    rnd = random.Random(121)
    R = 8.0
    cyl(nm('pb'), R + 1.2, 0.8, loc=(0, 0, 0), key='ev_stone', verts=8)
    cyl(nm('pb2'), R + 0.4, 0.4, loc=(0, 0, 0.8), key='ev_stone_warm', verts=8)
    cyl(nm('flr'), R, 0.2, loc=(0, 0, 1.2), key='ev_wood', verts=8)
    for k in range(4):
        a = PI / 8 + PI / 4 * k
        box(nm('inl'), (R * 1.9, 0.12, 0.05), loc=(0, 0, 1.42), key='ev_wood_light', rot=(0, 0, D(a)))
    zf = 1.4
    hc = 8.0
    rp = R - 0.7
    ents = (-PI / 2, PI / 2)
    for i in range(8):
        a = PI / 8 + PI / 4 * i - PI / 8 + PI / 8 * 0
        a = PI / 4 * i + PI / 8 + 0.0
    posts = []
    for i in range(8):
        a = PI / 4 * i
        x, y = math.cos(a) * rp, math.sin(a) * rp
        posts.append((a, x, y))
        cyl(nm('po'), 0.38, hc, loc=(x, y, zf), key='ev_wood_dark', verts=8)
        torus(nm('pbd'), 0.46, 0.08, loc=(x, y, zf + 0.9), key='ev_wood', segs=10, rsegs=3)
        torus(nm('pbd'), 0.46, 0.08, loc=(x, y, zf + hc - 0.9), key='ev_wood', segs=10, rsegs=3)
        box(nm('pfo'), (1.1, 1.1, 0.3), loc=(x, y, zf + 0.15), key='ev_stone', rot=(0, 0, D(a)), bev=0.05)
    zb = zf + hc
    for i, (a, x, y) in enumerate(posts):
        nx, ny = posts[(i + 1) % 8][1], posts[(i + 1) % 8][2]
        ln = math.hypot(nx - x, ny - y)
        am = math.atan2(ny - y, nx - x)
        box(nm('bm'), (ln, 0.6, 0.7), loc=((x + nx) / 2, (y + ny) / 2, zb + 0.3), key='ev_wood_dark', rot=(0, 0, D(am)), bev=0.05)
        # curved knee brace under the beam
        tube(nm('kn'), [(x + (nx - x) * 0.08, y + (ny - y) * 0.08, zb - 1.9), (x + (nx - x) * 0.14, y + (ny - y) * 0.14, zb - 0.7), (x + (nx - x) * 0.26, y + (ny - y) * 0.26, zb)], 0.18, 'ev_wood_dark', res=4, ures=2)
        tube(nm('kn'), [(nx - (nx - x) * 0.08, ny - (ny - y) * 0.08, zb - 1.9), (nx - (nx - x) * 0.14, ny - (ny - y) * 0.14, zb - 0.7), (nx - (nx - x) * 0.26, ny - (ny - y) * 0.26, zb)], 0.18, 'ev_wood_dark', res=4, ures=2)
        # low railing on every side except the two entrances
        mid = math.atan2((y + ny) / 2, (x + nx) / 2)
        is_ent = any(abs(((mid - e + PI) % (2 * PI)) - PI) < 0.3 for e in ents)
        if not is_ent:
            box(nm('rl'), (ln - 0.8, 0.14, 0.2), loc=((x + nx) / 2, (y + ny) / 2, zf + 3.0), key='ev_wood_light', rot=(0, 0, D(am)), bev=0.02)
            box(nm('rl'), (ln - 0.8, 0.12, 0.16), loc=((x + nx) / 2, (y + ny) / 2, zf + 1.9), key='ev_wood', rot=(0, 0, D(am)), bev=0.02)
            for k in range(1, 6):
                t = k / 6
                cyl(nm('bal'), 0.07, 1.7, loc=(x + (nx - x) * t, y + (ny - y) * t, zf + 1.4), key='ev_wood', verts=5)
            # bench under the railing
            box(nm('bnc'), (ln - 1.4, 0.8, 0.2), loc=((x + nx) / 2 * 0.86, (y + ny) / 2 * 0.86, zf + 1.1), key='ev_wood_light', rot=(0, 0, D(am)), bev=0.03)
    # roof: octagonal tiers with upswept eaves
    rmax = R + 2.6
    zr = zb + 1.0
    rs = [rmax, rmax * 0.78, rmax * 0.56, rmax * 0.36, rmax * 0.18]
    zs = [zr + 0.5, zr + 1.9, zr + 3.4, zr + 5.0, zr + 6.5]
    for k in range(4):
        sec = [(rs[k], zs[k]), (rs[k + 1] + 0.6, zs[k + 1] + 0.1), (rs[k + 1] + 0.6, zs[k + 1] - 0.4), (rs[k], zs[k] - 0.45)]
        shell(sec, 8, ('ev_shingle_a', 'ev_shingle_c', 'ev_shingle_a', 'ev_shingle_c')[k % 4], phase=PI / 8)
    lathe(nm('rtop'), [(0, zs[4] + 2.2), (rs[4] + 0.6, zs[4]), (0, zs[4])], loc=(0, 0, 0), key='ev_shingle_a', segs=8)
    cyl(nm('fin'), 0.1, 2.0, loc=(0, 0, zs[4] + 2.0), key='bronze', verts=6)
    ball(nm('finb'), 0.34, loc=(0, 0, zs[4] + 4.1), key='bronze', segs=8, rings=6)
    for i in range(8):
        a = PI / 8 + PI / 4 * i
        r0 = rmax * 1.0
        tube(nm('rib'), [(math.cos(a) * r0, math.sin(a) * r0, zs[0] - 0.1), (math.cos(a) * rs[2], math.sin(a) * rs[2], zs[2] + 0.3), (0, 0, zs[4] + 2.2)], 0.12, 'ev_wood_dark', res=4, ures=3)
        ball(nm('eav'), 0.26, loc=(math.cos(a) * (r0 + 0.1), math.sin(a) * (r0 + 0.1), zs[0] + 0.05), key='bronze', segs=6, rings=4)
    # interior: hanging lantern, round low table with stools
    tube(nm('hch'), [(0, 0, zs[3] - 0.6), (0, 0, zb - 1.3)], 0.05, 'iron', res=4)
    lantern(0, 0, zb - 2.2 - 0.0, s=1.0, hang=True)
    cyl(nm('tb'), 1.5, 0.15, loc=(0, 0, zf + 1.2), key='ev_wood_light', verts=12)
    cyl(nm('tbl'), 0.28, 1.2, loc=(0, 0, zf + 0.08), key='ev_wood_dark', verts=8)
    for k in range(4):
        a = PI / 4 + PI / 2 * k
        cyl(nm('stl'), 0.5, 0.15, loc=(math.cos(a) * 2.3, math.sin(a) * 2.3, zf + 0.95), key='ev_wood', verts=8)
        cyl(nm('stlg'), 0.15, 0.95, loc=(math.cos(a) * 2.3, math.sin(a) * 2.3, zf + 0.0), key='ev_wood_dark', verts=6)
    for e in ents:
        steps(e, R + 1.2, 0.8, 2, 4.2, depth=1.1)
        for sd in (-1, 1):
            lamp(math.cos(e) * (R + 1.0) - math.sin(e) * sd * 3.0, math.sin(e) * (R + 1.0) + math.cos(e) * sd * 3.0, 0.0, 3.0, 0.8)
    for i in range(6):
        a = rnd.uniform(0, 2 * PI)
        d = rnd.uniform(11.5, 14)
        bush(math.cos(a) * d, math.sin(a) * d, rnd.uniform(1.3, 2.0), i + 4)
        fern(math.cos(a + 0.4) * 11, math.sin(a + 0.4) * 11, 0.0, n=6, L=1.5, seed=i)
    U.marker('mk_deck', (0, 0, zf + 0.4))
    U.marker('mk_door', (0, -R - 1.2, 1.6))
    return finalize('ev_pavilion', smooth_angle=38)


# ------------------------------------------------------------------ D04_15 moon pool
def moon_pool():
    reset()
    rnd = random.Random(131)
    shell([(9.4, 0.0), (10.9, 0.0), (10.9, 1.3), (9.4, 1.3)], 36, 'ev_stone')
    shell([(10.9, 0.0), (12.6, 0.0), (12.6, 0.45), (10.9, 0.45)], 36, 'ev_stone_warm')
    shell([(9.15, 1.3), (11.1, 1.3), (11.1, 1.6), (9.15, 1.6)], 36, 'ev_stone_warm')
    cyl(nm('bed'), 9.5, 0.5, loc=(0, 0, 0), key='ev_stone_dark', verts=36)
    cyl(nm('wat'), 9.45, 0.12, loc=(0, 0, 0.55), key='water', verts=36)
    # islet with the crescent sculpture
    cyl(nm('isl'), 3.2, 0.9, loc=(0, 0, 0.45), key='ev_stone', verts=14)
    blob(nm('mos'), 2.6, (0, 0, 1.35), 'ev_moss', subdiv=2, amp=0.15, scale=(1, 1, 0.12), seed=1)
    box(nm('ped'), (1.8, 1.8, 1.3), loc=(0, 0, 2.0), key='ev_stone', bev=0.08)
    outer = [(2.0 * math.cos(math.radians(46.4 + (313.6 - 46.4) * i / 24)), 2.0 * math.sin(math.radians(46.4 + (313.6 - 46.4) * i / 24))) for i in range(25)]
    inner = [(0.7 + 1.6 * math.cos(math.radians(295.1 + (64.9 - 295.1) * i / 20)), 1.6 * math.sin(math.radians(295.1 + (64.9 - 295.1) * i / 20))) for i in range(1, 20)]
    poly_prism(nm('moon'), outer + inner, 0.7, loc=(0, 0.35, 4.8), key='ev_stone_warm', rot=(90, 0, 0))
    # stepping stones to the islet from the south
    for k in range(5):
        r = 8.4 - k * 1.05
        cyl(nm('stn'), 0.85 + rnd.uniform(-0.1, 0.1), 0.18, loc=(rnd.uniform(-0.3, 0.3), -r, 0.6), key='ev_stone', verts=8, rot=(0, 0, rnd.uniform(0, 45)))
    # standing stones
    for i in range(7):
        a = 2 * PI * i / 7 + 0.4
        hh = rnd.uniform(5.0, 8.0)
        x, y = math.cos(a) * 15.2, math.sin(a) * 15.2
        cyl(nm('mnh'), 1.5, hh, loc=(x, y, 0.0), key='ev_stone_dark', verts=6, r2=1.0, rot=(rnd.uniform(-4, 4), rnd.uniform(-4, 4), rnd.uniform(0, 60)))
        torus(nm('mrn'), 1.32, 0.07, loc=(x, y, hh * 0.55), key='ev_stone_warm', segs=10, rsegs=3)
        torus(nm('mrn'), 1.2, 0.07, loc=(x, y, hh * 0.7), key='ev_stone_warm', segs=10, rsegs=3)
        moss_cap(x, y, hh + 0.05, 0.9, i)
        blob(nm('mbs'), 0.8, (x + math.cos(a) * 1.1, y + math.sin(a) * 1.1, 0.4), 'ev_moss', subdiv=1, amp=0.3, scale=(1, 1, 0.6), seed=i)
    # lilies, lotus and reeds
    for i in range(10):
        a, d = rnd.uniform(0, 2 * PI), rnd.uniform(3.6, 8.2)
        ball(nm('pad'), rnd.uniform(0.6, 1.1), loc=(math.cos(a) * d, math.sin(a) * d, 0.7), key=('ev_leaf_a', 'ev_leaf_b')[i % 2], segs=10, rings=3, scale=(1, 1, 0.1))
        if i % 3 == 0:
            for p in range(8):
                pa = 2 * PI * p / 8
                o = ball(nm('pet'), 0.26, loc=(math.cos(a) * d + math.cos(pa) * 0.3, math.sin(a) * d + math.sin(pa) * 0.3, 0.9), key='fl_white', segs=6, rings=4, scale=(1, 0.45, 0.3))
                o.rotation_euler = (0, math.radians(-35), pa)
            ball(nm('lcn'), 0.14, loc=(math.cos(a) * d, math.sin(a) * d, 0.98), key='fl_yellow', segs=6, rings=4)
    for i in range(12):
        a = 2 * PI * i / 12 + rnd.uniform(-0.1, 0.1)
        for k in range(5):
            r0 = 12.8 + rnd.uniform(0, 0.6)
            h = rnd.uniform(2.0, 3.4)
            tube(nm('rd'), [(math.cos(a) * r0, math.sin(a) * r0, 0.3), (math.cos(a) * (r0 + 0.1) + rnd.uniform(-0.2, 0.2), math.sin(a) * (r0 + 0.1), h * 0.5), (math.cos(a) * (r0 + 0.3) + rnd.uniform(-0.3, 0.3), math.sin(a) * (r0 + 0.3) + rnd.uniform(-0.3, 0.3), h)], 0.045, 'ev_leaf_b', res=4, ures=2)
    for a in (PI / 4, 3 * PI / 4, 5 * PI / 4, 7 * PI / 4):
        lamp(math.cos(a) * 13.2, math.sin(a) * 13.2, 0.45, 3.2, 0.9)
    for k in range(3):
        a = PI * 0.9 + k * 1.1 - 1.0
        box(nm('bnc'), (4.0, 1.2, 0.5), loc=(math.cos(a) * 17.5, math.sin(a) * 17.5, 0.5), key='ev_stone_warm', rot=(0, 0, D(a) + 90), bev=0.06)
        for sd in (-1, 1):
            box(nm('bnl'), (0.5, 1.0, 0.5), loc=(math.cos(a) * 17.5 + math.cos(a + PI / 2) * sd * 1.6, math.sin(a) * 17.5 + math.sin(a + PI / 2) * sd * 1.6, 0.25), key='ev_stone', rot=(0, 0, D(a) + 90))
    for i in range(6):
        a = rnd.uniform(0, 2 * PI)
        fern(math.cos(a) * 20, math.sin(a) * 20, 0.0, n=6, L=1.5, seed=i)
    U.marker('mk_deck', (0, -14.0, 0.4))
    return finalize('ev_moon_pool', smooth_angle=38)


# ------------------------------------------------------------------ D04_16 workshop
def workshop():
    reset()
    rnd = random.Random(141)
    R, h, fh = 5.6, 7.2, 1.0
    cx, cy = -6.5, 0.0
    da = -PI / 2
    cyl(nm('fnd'), R + 0.8, fh, loc=(cx, cy, 0.0), key='ev_stone_dark', verts=26)
    torus(nm('fcr'), R + 0.8, 0.2, loc=(cx, cy, fh), key='ev_stone', segs=26, rsegs=5)
    for j in range(2):
        top = fh * (1 - (j + 1) / 3.0)
        r = R + 0.8 + 0.5 + j * 1.0
        box(nm('stp'), (1.0, 3.4, top), loc=(cx, cy - r, top / 2), key='ev_stone', bev=0.05)
    cabin(cx, cy, fh, R, h, da, seed=141, windows=2)
    # forge chimney on the far side
    chimney(cx, cy, PI + 0.4, R + 1.6, fh + h + 3.2)
    # open shed to the east: floor, posts, sloped shingle roof falling away from the cabin
    sx0, sx1, sy = cx + R + 0.2, cx + R + 13.0, 4.6
    nx = 12
    for k in range(nx):
        x = sx0 + (sx1 - sx0) * (k + 0.5) / nx
        box(nm('shf'), ((sx1 - sx0) / nx - 0.06, 2 * sy, 0.3), loc=(x, 0, 0.15), key=('ev_wood_aged', 'ev_wood', 'ev_wood_aged')[k % 3], bev=0.03)
    zhi, zlo = fh + h - 0.6, 5.0
    for sg in (-1, 1):
        for xx in (sx1 - 0.4, (sx0 + sx1) / 2):
            cyl(nm('shp'), 0.22, zlo - 0.3 + (zhi - zlo) * (1 - (xx - sx0) / (sx1 - sx0)), loc=(xx, sg * (sy - 0.3), 0.3), key='ev_wood_dark', verts=6)
    pitch = D(math.atan((zhi - zlo) / (sx1 - sx0)))
    rows = 9
    ln = (sx1 - sx0 + 1.4) / rows
    for r in range(rows):
        s = (r + 0.5) / rows * (sx1 - sx0 + 1.0)
        box(nm('sro'), (ln * 1.4, 2 * sy + 1.2, 0.14), loc=(sx0 - 0.2 + s * math.cos(math.radians(pitch)), 0, zhi + 0.2 - s * math.sin(math.radians(pitch))), key=SHING[r % 4], rot=(0, pitch, 0), bev=0.02)
    for sg in (-1, 1):
        tube(nm('srb'), [(sx0, sg * (sy - 0.3), zhi - 0.1), (sx1, sg * (sy - 0.3), zlo - 0.1)], 0.2, 'ev_wood_dark', res=4)
    # workbench with vise and a half-carved log, saw horses, grindstone, lumber, tool rack
    box(nm('wbt'), (5.6, 2.0, 0.3), loc=(sx0 + 4.2, -sy + 2.0, 3.2), key='ev_wood_light', bev=0.04)
    for sx in (-1, 1):
        for sy2 in (-1, 1):
            cyl(nm('wbl'), 0.18, 3.0, loc=(sx0 + 4.2 + sx * 2.5, -sy + 2.0 + sy2 * 0.8, 0.3), key='ev_wood_dark', verts=6)
    box(nm('vis'), (0.5, 0.8, 0.6), loc=(sx0 + 2.0, -sy + 2.0, 3.65), key='iron', bev=0.03)
    cyl(nm('lg'), 0.55, 2.2, loc=(sx0 + 4.8, -sy + 2.0, 3.35), key='ev_bark_light', verts=8, rot=(0, 90, 6))
    for k in range(5):
        a = rnd.uniform(0, 6.28)
        ball(nm('shv'), 0.18, loc=(sx0 + 4.8 + rnd.uniform(-1.2, 1.2), -sy + 2.0 + rnd.uniform(-0.6, 0.6), 3.4), key='ev_wood_light', segs=5, rings=3, scale=(1.4, 0.4, 0.2))
    for dx in (0.0, 1.9):
        box(nm('swh'), (0.3, 1.6, 0.3), loc=(sx0 + 9.0 + dx, 0.5, 1.9), key='ev_wood_dark', bev=0.03)
        for sg in (-1, 1):
            tube(nm('swl'), [(sx0 + 9.0 + dx, 0.5 + sg * 0.6, 1.9), (sx0 + 9.0 + dx + sg * 0.25, 0.5 + sg * 0.75, 0.3)], 0.12, 'ev_wood_dark', res=4)
            tube(nm('swl'), [(sx0 + 9.0 + dx, 0.5 + sg * 0.6, 1.9), (sx0 + 9.0 + dx - sg * 0.25, 0.5 + sg * 0.75, 0.3)], 0.12, 'ev_wood_dark', res=4)
    cyl(nm('sbm'), 0.4, 3.9, loc=(sx0 + 9.95, 0.5, 2.1), key='ev_wood', verts=8, rot=(0, 90, 0))
    cyl(nm('gst'), 1.05, 0.55, loc=(sx1 - 1.8, sy - 1.8, 1.6), key='ev_stone', verts=14, rot=(0, 90, 0))
    box(nm('gfr'), (0.3, 0.3, 1.6), loc=(sx1 - 1.8 - 0.2, sy - 1.8, 0.8), key='ev_wood_dark')
    box(nm('gfr'), (0.3, 0.3, 1.6), loc=(sx1 - 1.8 + 0.8, sy - 1.8, 0.8), key='ev_wood_dark')
    for i in range(7):
        box(nm('lbr'), (6.0, 0.9, 0.2), loc=(sx0 + 5.0, sy - 1.0, 0.45 + i * 0.22), key=('ev_wood', 'ev_wood_light')[i % 2], rot=(0, 0, rnd.uniform(-2.5, 2.5)), bev=0.02)
    for sg in (-1, 1):
        cyl(nm('lbs'), 0.14, 2.3, loc=(sx0 + 1.8 + (sg + 1) * 3.6, sy - 1.0, 0.3), key='ev_wood_dark', verts=5)
    box(nm('trk'), (0.18, 3.2, 1.6), loc=(cx + R + 0.35, -1.6, 4.4), key='ev_wood_dark')
    for k in range(5):
        box(nm('tol'), (0.12, 0.14, 1.0 + 0.15 * (k % 3)), loc=(cx + R + 0.5, -2.8 + k * 0.6, 4.3), key=('iron', 'ev_wood_light', 'iron')[k % 3])
    lantern(sx0 + 6.0, 0.0, zlo + 0.4 - 0.9 * 0.9, s=0.9, hang=True)
    lantern(sx0 + 2.0, -sy + 2.0, zhi - 0.2 - 0.9 * 0.8 - 1.4, s=0.8, hang=True)
    tube(nm('lch'), [(sx0 + 2.0, -sy + 2.0, zhi - 0.2), (sx0 + 2.0, -sy + 2.0, zhi - 0.2 - 1.4)], 0.05, 'iron', res=4)
    cyl(nm('brl'), 0.75, 1.6, loc=(sx1 + 1.4, -2.0, 0.0), key='ev_wood_dark', verts=10)
    cyl(nm('brl'), 0.75, 1.6, loc=(sx1 + 1.4, -0.4, 0.0), key='ev_wood_dark', verts=10)
    woodpile(cx - 0.5, cy + R + 3.0, 0.0, -PI / 2)
    # stack of carved figures drying outside
    for k in range(3):
        x = cx - 3.0 + k * 1.3
        cyl(nm('crv'), 0.35, 1.3 + k * 0.3, loc=(x, cy - R - 3.8, 0.0), key='ev_wood_light', verts=7, r2=0.28)
        ball(nm('crh'), 0.32, loc=(x, cy - R - 3.8, 1.5 + k * 0.3), key='ev_wood_light', segs=6, rings=4)
    for a in window_angles_ws(da):
        planter(cx, cy, fh + h * 0.58 - 1.0, R, a, rnd)
    wall_ivy(cx, cy, R, PI * 0.9, fh + 0.5, h - 0.8, 14, rnd, 0.6)
    flagstones(da, R + 4.8, 5, rnd) if False else None
    for i in range(5):
        cyl(nm('pth'), 1.2, 0.14, loc=(cx + rnd.uniform(-0.5, 0.5), -R - 3.0 - i * 1.6, 0.0), key='ev_stone', verts=7, rot=(0, 0, rnd.uniform(0, 60)))
    for i in range(4):
        bush(cx + rnd.uniform(-9, 3), cy + rnd.uniform(6.8, 9.2), rnd.uniform(1.3, 1.9), i + 14)
    fern(cx - 6.8, cy - 2.0, 0.0, n=7, L=1.5, seed=6)
    mushrooms(cx - 5.0, cy + 6.0, 0.0, 4, seed=9, scale=0.9)
    lamp(cx + 1.8, cy - R - 3.4, 0.0, 3.4, 0.8)
    lamp(cx - 1.8, cy - R - 3.4, 0.0, 3.4, 0.8)
    U.marker('mk_door', (cx, cy - R - 0.6, fh + 2.0))
    U.marker('mk_deck', (sx0 + 6.0, 0, 0.8))
    return finalize('ev_workshop', smooth_angle=38)


def window_angles_ws(da):
    return [da + 1.25, da - 1.25]


BATCH_D04 = [
    ('D04_06_gate_arch_a', gate_arch_a, (0.0, -1.3, 0.3)),
    ('D04_07_gate_arch_b', gate_arch_b, (0.0, -1.3, 0.3)),
    ('D04_08_stall_a', stall_a, (0.5, -1.2, 0.4)),
    ('D04_09_stall_b', stall_b, (0.5, -1.2, 0.4)),
    ('D04_10_stall_c', stall_c, (0.5, -1.2, 0.4)),
    ('D04_11_watch_post', watch_post),
    ('D04_12_stone_bridge_a', stone_bridge_a, (0.4, -1.3, 0.4)),
    ('D04_13_stone_bridge_b', stone_bridge_b, (0.4, -1.3, 0.35)),
    ('D04_14_pavilion', pavilion),
    ('D04_15_moon_pool', moon_pool, (0.6, -1.2, 0.7)),
    ('D04_16_workshop', workshop, (0.5, -1.2, 0.5)),
]
