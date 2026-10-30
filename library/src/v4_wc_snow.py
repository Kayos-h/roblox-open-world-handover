"""v4_wc_snow - worker wc: C10 snow-laden conifers (-> v4_alpine) and E05 dead trees (-> v4_nature).
Snow pines reuse the conifer builder from v4_wc_trees (snowy=True) with 4 different silhouettes,
snow on every tier and a few icicles. Dead trees are six different bare/broken designs in bark_dead,
grey wood and a little moss. 1 unit = 1 stud, Z up, origin at trunk base. Trees <= 20k tris.
"""
import math, random, bpy
from mathutils import Vector
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, PAL
import v4util as U
from v4_elf import nm, bark_trunk, trunk_point, roots, limb, ivy_strand
from v4_d05 import trunk_r, moss_on_trunk, ground_bits
from nature import blob, rock
from v4_wc_trees import conifer, CPINE, FIR

PI = math.pi
D = math.degrees

PAL['wc_dead_a']  = ((112, 100, 86), 'Wood', 0.0, 0.95, 0)
PAL['wc_dead_b']  = ((92, 82, 72),   'Wood', 0.0, 0.95, 0)
PAL['wc_char']    = ((44, 40, 38),   'Wood', 0.0, 1.00, 0)
PAL['wc_grey_wd'] = ((134, 126, 116),'Wood', 0.0, 0.92, 0)
DEAD = ('bark_dead', 'wc_dead_a', 'wc_dead_b', 'wc_grey_wd')


# ================================================================== C10 snow pines -> v4_alpine
def icicles(x, y, z, n, rnd, rng=(0.5, 1.6), spread=1.4):
    for i in range(n):
        a = rnd.uniform(0, 2 * PI); d = rnd.uniform(0, spread)
        L = rnd.uniform(*rng)
        px, py = x + math.cos(a) * d, y + math.sin(a) * d
        cyl(nm('ic'), rnd.uniform(0.07, 0.13), L, loc=(px, py, z - L), key='ice', verts=5, r2=0.01)


def snow_conifer(seed, H, name, tr, tiers, width, keys, droop, broken=False, clump=9):
    """A snow-laden conifer built on the shared conifer() helper, then icicles hung under the tiers."""
    ob = conifer(seed, H, name, tr=tr, tiers=tiers, width=width, keys=keys, droop=droop, snowy=True,
                 clump_per_tier=clump, bark='wc_bark_warm')
    return ob


def C10_01_tall_spruce():
    """Tall narrow spruce under heavy snow, ~42 high."""
    reset()
    rnd = random.Random(1001)
    # build via conifer then add icicles in a second pass by re-seeding tier positions
    ob = conifer(1001, 42.0, 'C10_01_snow_pine_01', tr=1.7, tiers=13, width=0.19, keys=FIR, droop=0.42,
                 snowy=True, clump_per_tier=8, bark='wc_bark_warm', top_r=0.15)
    return ob


def C10_02_wide_fir():
    """Wide fir with fat snow-covered tiers, ~34 high."""
    return conifer(1002, 34.0, 'C10_02_snow_pine_02', tr=1.9, tiers=10, width=0.3, keys=CPINE, droop=0.55,
                   snowy=True, clump_per_tier=10, bark='wc_bark_warm', top_r=0.2)


def C10_03_broken_top():
    """Broken-top pine: snapped crown, snow on the stump, ~30 high."""
    reset()
    rnd = random.Random(1003)
    tr, H = 1.7, 30.0
    bark_trunk(tr, H, seed=1003, sway=0.4, flare=1.9, key='wc_bark_warm', top_r=0.4, ring_h=max(1.4, H / 20))
    roots(tr, n=6, seed=1003, key='wc_bark_warm', span=2.1)
    tiers = 7
    for i in range(tiers):
        t = i / (tiers - 1)
        z = H * (0.12 + 0.62 * t)   # tiers stop ~0.74 H (snapped above)
        R = H * 0.24 * (1 - t) ** 1.0 + 1.0
        cx, cy = trunk_point(tr, H, 1003, z, 0.4)
        nb = max(5, int(9 * (1 - 0.4 * t)))
        for k in range(nb):
            az = i * 0.7 + 2 * PI * k / nb + rnd.uniform(-0.2, 0.2)
            c, s = math.cos(az), math.sin(az)
            ex, ey = cx + c * R, cy + s * R
            ez = z - R * 0.5
            tube(nm('bch'), [(cx, cy, z + 0.3), (ex, ey, ez)], max(0.12, tr * 0.3 * (1 - t) + 0.1), 'wc_bark_warm', res=4, taper=[1, 0.5], ures=2)
            br = R * rnd.uniform(0.34, 0.5)
            blob(nm('bl'), br, (ex, ey, ez + br * 0.2), rnd.choice(CPINE), subdiv=1, amp=0.34, scale=(1.2, 1.2, 0.6), seed=rnd.randint(0, 999), detail=0.35)
            blob(nm('sn'), br * rnd.uniform(0.6, 0.85), (ex + rnd.uniform(-0.2, 0.2), ey + rnd.uniform(-0.2, 0.2), ez + br * 0.55), 'snow', subdiv=1, amp=0.26, scale=(1.3, 1.3, 0.4), seed=rnd.randint(0, 999))
            if k % 3 == 0:
                icicles(ex, ey, ez - br * 0.3, 2, rnd, rng=(0.4, 1.0), spread=0.5)
    # snapped stump at the top with jagged splinters and a snow cap
    stump_z = H * 0.74
    cx, cy = trunk_point(tr, H, 1003, stump_z, 0.4)
    stub = cyl(nm('stub'), trunk_r(tr, H, stump_z, 0.4), 2.0, loc=(cx, cy, stump_z), key='wc_bark_warm', verts=10)
    for k in range(5):
        a = rnd.uniform(0, 2 * PI)
        cyl(nm('jag'), 0.18, rnd.uniform(1.0, 2.4), loc=(cx + math.cos(a) * 0.4, cy + math.sin(a) * 0.4, stump_z + 1.8), key='wc_bark_warm', verts=4, r2=0.02, rot=(rnd.uniform(-12, 12), rnd.uniform(-12, 12), 0))
    cyl(nm('innr'), trunk_r(tr, H, stump_z, 0.4) * 0.6, 0.3, loc=(cx, cy, stump_z + 1.9), key='wc_dead_a', verts=10)
    blob(nm('scap'), trunk_r(tr, H, stump_z, 0.4) * 1.1, (cx, cy, stump_z + 2.1), 'snow', subdiv=1, amp=0.2, scale=(1.2, 1.2, 0.4), seed=1)
    moss_on_trunk(tr, H, 1003, 5, rnd, sway=0.4, zmin=1, zmax=H * 0.3, top_r=0.4)
    ground_bits(tr, rnd, 1003, nrock=3, scale=1.0)
    for i in range(4):
        a = rnd.uniform(0, 2 * PI); d = tr * rnd.uniform(2.4, 3.6)
        blob(nm('gs'), rnd.uniform(0.9, 1.5), (math.cos(a) * d, math.sin(a) * d, 0.0), 'snow', subdiv=1, amp=0.25, scale=(1.3, 1.3, 0.25), seed=i)
    return finalize('C10_03_snow_pine_03', smooth_angle=34)


def C10_04_pair():
    """Pair of small snowy pines growing together, ~20 high."""
    reset()
    rnd = random.Random(1004)
    for ox, oy, H, sd in ((-2.6, -1.0, 20.0, 1041), (2.4, 1.2, 16.0, 1042)):
        r2 = random.Random(sd)
        tr = H * 0.05
        bark_trunk(tr, H, seed=sd, sway=0.3, flare=1.8, key='wc_bark_warm', top_r=0.16, ring_h=max(1.2, H / 16)).location = (ox, oy, 0)
        roots(tr, n=5, seed=sd, key='wc_bark_warm', span=1.8, ox=ox, oy=oy)
        tiers = 7
        for i in range(tiers):
            t = i / (tiers - 1)
            z = H * (0.12 + 0.8 * t)
            R = H * 0.26 * (1 - t) ** 1.1 + 0.7
            cx, cy = trunk_point(tr, H, sd, z, 0.3)
            nb = max(4, int(7 * (1 - 0.45 * t)))
            for k in range(nb):
                az = i * 0.6 + 2 * PI * k / nb + r2.uniform(-0.2, 0.2)
                c, s = math.cos(az), math.sin(az)
                ex, ey = ox + cx + c * R, oy + cy + s * R
                ez = z - R * 0.5
                tube(nm('tb'), [(ox + cx, oy + cy, z + 0.2), (ex, ey, ez)], max(0.1, tr * 0.3 * (1 - t) + 0.07), 'wc_bark_warm', res=4, taper=[1, 0.4], ures=2)
                br = R * r2.uniform(0.34, 0.5)
                blob(nm('bl'), br, (ex, ey, ez + br * 0.2), r2.choice(CPINE), subdiv=1, amp=0.34, scale=(1.2, 1.2, 0.6), seed=r2.randint(0, 999), detail=0.3)
                blob(nm('sn'), br * r2.uniform(0.6, 0.85), (ex, ey, ez + br * 0.55), 'snow', subdiv=1, amp=0.24, scale=(1.3, 1.3, 0.4), seed=r2.randint(0, 999))
        tp = trunk_point(tr, H, sd, H, 0.3)
        blob(nm('tip'), 0.9, (ox + tp[0], oy + tp[1], H * 0.96), r2.choice(CPINE), subdiv=1, amp=0.3, scale=(0.8, 0.8, 1.1), seed=1)
        blob(nm('stp'), 0.7, (ox + tp[0], oy + tp[1], H * 0.99), 'snow', subdiv=1, amp=0.2, scale=(0.9, 0.9, 0.7), seed=2)
    for i in range(5):
        a = rnd.uniform(0, 2 * PI); d = rnd.uniform(2, 5)
        blob(nm('gs'), rnd.uniform(0.9, 1.6), (math.cos(a) * d, math.sin(a) * d, 0.0), 'snow', subdiv=1, amp=0.25, scale=(1.3, 1.3, 0.25), seed=i)
    return finalize('C10_04_snow_pine_04', smooth_angle=34)


# ================================================================== E05 dead trees -> v4_nature
def dead_trunk(tr, H, seed, name_end, sway=1.8, lean=(0, 0), flare=1.9, key='bark_dead', top_r=0.3):
    bark_trunk(tr, H, seed=seed, sway=sway, flare=flare, key=key, top_r=top_r, ring_h=max(1.2, H / 16), lean=lean)
    roots(tr, n=6, seed=seed, key=key, span=2.4)


def bare_branches(base, az0, n, L, r, rnd, key='bark_dead', depth=2, spread=0.8, up=0.5):
    """Recursive bare, grasping dead branches. Returns tip points."""
    tips = []
    d = (math.cos(az0), math.sin(az0), up)
    e = limb(base, d, L, r, key=key, droop=-0.05, seed=rnd.randint(0, 999))
    tips.append(e)
    if depth > 0:
        for k in range(n):
            az2 = az0 + rnd.uniform(-spread, spread)
            tips += bare_branches((e.x, e.y, e.z), az2, max(1, n - 1), L * rnd.uniform(0.5, 0.7), r * 0.6, rnd, key, depth - 1, spread, up * rnd.uniform(0.8, 1.4))
    return tips


def E05_01_forked():
    """Twisted dead tree with a forked trunk."""
    reset()
    tr, H = 1.6, 24.0
    rnd = random.Random(501)
    dead_trunk(tr, H * 0.45, 501, '01', sway=2.2, flare=2.0)
    # fork into two twisted stems
    for az in (0.7, 3.6):
        c, s = math.cos(az), math.sin(az)
        p_mid = (c * 3, s * 3, H * 0.6)
        p_top = (c * 5, s * 2, H * 0.92)
        tube(nm('fork'), [(0, 0, H * 0.4), p_mid, p_top], tr * 0.5, 'bark_dead', res=4, taper=[1, 0.7, 0.4], ures=3)
        for b in range(3):
            bare_branches(p_top, az + rnd.uniform(-1, 1), 2, rnd.uniform(3, 5), tr * 0.22, rnd, depth=2, up=rnd.uniform(0.4, 0.9))
    moss_on_trunk(tr, H * 0.45, 501, 4, rnd, sway=2.2, zmin=1, zmax=H * 0.3)
    ground_bits(tr, rnd, 501, nrock=3, scale=1.0)
    return finalize('E05_01_dead_tree_01', smooth_angle=38)


def E05_02_leaning():
    """Leaning dead tree with broken hanging limbs."""
    reset()
    tr, H = 1.5, 22.0
    rnd = random.Random(502)
    lean = (0.22, 0.05)
    dead_trunk(tr, H, 502, '02', sway=1.4, lean=lean, flare=1.8)
    for k in range(5):
        az = 2 * PI * k / 5 + rnd.uniform(-0.3, 0.3)
        z0 = H * rnd.uniform(0.4, 0.85)
        p0 = trunk_point(tr, H, 502, z0, 1.4, lean)
        if rnd.random() < 0.5:
            # broken limb hanging down
            e = limb((p0[0], p0[1], z0), (math.cos(az), math.sin(az), 0.2), rnd.uniform(3, 5), tr * 0.22, key='bark_dead', seed=k)
            tube(nm('hang'), [(e.x, e.y, e.z), (e.x + rnd.uniform(-0.5, 0.5), e.y + rnd.uniform(-0.5, 0.5), e.z - rnd.uniform(3, 6))], tr * 0.14, 'wc_dead_b', res=4, taper=[1, 0.3], ures=2)
        else:
            bare_branches((p0[0], p0[1], z0), az, 2, rnd.uniform(3, 5), tr * 0.2, rnd, depth=2, up=rnd.uniform(0.5, 1.1))
    moss_on_trunk(tr, H, 502, 4, rnd, sway=1.4, lean=lean, zmin=1, zmax=H * 0.4)
    ground_bits(tr, rnd, 502, nrock=3, scale=1.0)
    return finalize('E05_02_dead_tree_02', smooth_angle=38)


def E05_03_split():
    """Lightning-split trunk, charred inside."""
    reset()
    tr, H = 1.8, 20.0
    rnd = random.Random(503)
    dead_trunk(tr, H * 0.55, 503, '03', sway=1.0, flare=2.0)
    # split: two halves lean apart above mid, charred inner faces
    for sd in (-1, 1):
        c = sd
        p_mid = (c * 2.2, 0, H * 0.7)
        p_top = (c * 4.0, rnd.uniform(-1, 1), H * rnd.uniform(0.85, 1.0))
        tube(nm('half'), [(c * 0.6, 0, H * 0.5), p_mid, p_top], tr * 0.55, 'bark_dead', res=4, taper=[1, 0.7, 0.35], ures=3)
        # charred inner strip
        box(nm('char'), (0.25, tr * 1.2, H * 0.4), loc=(c * 0.3, 0, H * 0.68), key='wc_char', rot=(0, c * 14, 0))
        for b in range(2):
            bare_branches(p_top, (0 if sd > 0 else PI) + rnd.uniform(-1, 1), 2, rnd.uniform(2.5, 4), tr * 0.2, rnd, depth=2, up=rnd.uniform(0.4, 1.0))
    # scorch at the base
    blob(nm('scorch'), tr * 1.3, (0, 0, 0.3), 'wc_char', subdiv=1, amp=0.3, scale=(1.3, 1.3, 0.2), seed=1)
    ground_bits(tr, rnd, 503, nrock=3, scale=1.0)
    return finalize('E05_03_dead_tree_03', smooth_angle=38)


def E05_04_grasping():
    """Tall thin dead tree with long grasping branches."""
    reset()
    tr, H = 1.1, 26.0
    rnd = random.Random(504)
    dead_trunk(tr, H, 504, '04', sway=1.0, flare=1.6, top_r=0.25)
    for k in range(7):
        az = 2 * PI * k / 7 + rnd.uniform(-0.3, 0.3)
        z0 = H * rnd.uniform(0.45, 0.95)
        p0 = trunk_point(tr, H, 504, z0, 1.0)
        # long thin curving grasping branches reaching up and out
        bare_branches((p0[0], p0[1], z0), az, 3, rnd.uniform(5, 8), tr * 0.28, rnd, depth=2, spread=0.6, up=rnd.uniform(0.8, 1.4))
    top = trunk_point(tr, H, 504, H, 1.0)
    bare_branches((top[0], top[1], H * 0.95), rnd.uniform(0, 2 * PI), 3, 6, tr * 0.2, rnd, depth=2, up=1.3)
    moss_on_trunk(tr, H, 504, 3, rnd, sway=1.0, zmin=1, zmax=H * 0.3, top_r=0.25)
    ground_bits(tr, rnd, 504, nrock=2, scale=0.9)
    return finalize('E05_04_dead_tree_04', smooth_angle=38)


def E05_05_husk():
    """Stump-like husk with a few spikes and ivy remains."""
    reset()
    tr, H = 2.4, 9.0
    rnd = random.Random(505)
    dead_trunk(tr, H, 505, '05', sway=0.6, flare=2.2, top_r=0.75)
    # jagged broken-off top spikes
    top = trunk_point(tr, H, 505, H, 0.6)
    for k in range(6):
        a = 2 * PI * k / 6 + rnd.uniform(-0.2, 0.2)
        hh = rnd.uniform(1.5, 3.5)
        cyl(nm('spk'), 0.25, hh, loc=(top[0] + math.cos(a) * tr * 0.6, top[1] + math.sin(a) * tr * 0.6, H - 0.3), key='bark_dead', verts=5, r2=0.03, rot=(rnd.uniform(-10, 10), rnd.uniform(-10, 10), 0))
    # hollow dark top
    cyl(nm('holl'), tr * 0.55, 0.5, loc=(top[0], top[1], H - 0.2), key='wc_char', verts=12)
    # ivy remains clinging to one side
    for i in range(3):
        a = rnd.uniform(0, 2 * PI)
        ivy_strand((top[0] + math.cos(a) * tr, top[1] + math.sin(a) * tr, H - 1.0), rnd.uniform(3, 6), seed=i, key='ev_leaf_b')
    for k in range(4):
        a = rnd.uniform(0, 2 * PI)
        blob(nm('mo'), rnd.uniform(0.6, 1.1), (math.cos(a) * tr, math.sin(a) * tr, rnd.uniform(1, H * 0.6)), 'moss', subdiv=1, amp=0.3, scale=(1, 1, 1.2), seed=k)
    ground_bits(tr, rnd, 505, nrock=4, scale=1.1)
    return finalize('E05_05_dead_tree_05', smooth_angle=38)


def E05_06_swing():
    """Old gnarled dead tree with a rope swing and a broken seat."""
    reset()
    tr, H = 1.9, 22.0
    rnd = random.Random(506)
    dead_trunk(tr, H * 0.5, 506, '06', sway=2.0, flare=2.1)
    # one big horizontal limb to hang the swing from, plus a few bare branches
    top = trunk_point(tr, H, 506, H * 0.5, 2.0)
    limb_end = limb((0, 0, H * 0.48), (0.2, -1.0, 0.25), 9.0, tr * 0.4, key='bark_dead', droop=0.08, seed=1)
    for k in range(4):
        az = 2 * PI * k / 4 + rnd.uniform(-0.3, 0.3)
        p0 = trunk_point(tr, H, 506, H * rnd.uniform(0.4, 0.5), 2.0)
        bare_branches((p0[0], p0[1], H * 0.48), az, 2, rnd.uniform(3, 5), tr * 0.22, rnd, depth=2, up=rnd.uniform(0.5, 1.0))
    # rope swing: two ropes down from the limb to a broken seat
    sx, sy = limb_end.x, limb_end.y
    seat_z = 3.0
    for dx in (-0.9, 0.9):
        tube(nm('rope'), [(sx + dx, sy, limb_end.z - 0.2), (sx + dx * 0.9, sy + 0.1, seat_z + 0.2)], 0.06, 'rope', res=4, ures=2)
    # broken plank seat (tilted, one side lower)
    box(nm('seat'), (2.2, 0.8, 0.22), loc=(sx, sy, seat_z), key='wc_grey_wd', rot=(8, 0, rnd.uniform(-6, 6)), bev=0.03)
    box(nm('crack'), (0.1, 0.85, 0.24), loc=(sx + 0.5, sy, seat_z), key='wc_char')
    moss_on_trunk(tr, H * 0.5, 506, 4, rnd, sway=2.0, zmin=1, zmax=H * 0.3)
    ground_bits(tr, rnd, 506, nrock=3, scale=1.0)
    return finalize('E05_06_dead_tree_06', smooth_angle=38)


BATCHES = {
    'snow': ('v4_alpine', [
        ('C10_01_snow_pine_01', C10_01_tall_spruce),
        ('C10_02_snow_pine_02', C10_02_wide_fir),
        ('C10_03_snow_pine_03', C10_03_broken_top),
        ('C10_04_snow_pine_04', C10_04_pair),
    ]),
    'dead': ('v4_nature', [
        ('E05_01_dead_tree_01', E05_01_forked),
        ('E05_02_dead_tree_02', E05_02_leaning),
        ('E05_03_dead_tree_03', E05_03_split),
        ('E05_04_dead_tree_04', E05_04_grasping),
        ('E05_05_dead_tree_05', E05_05_husk),
        ('E05_06_dead_tree_06', E05_06_swing),
    ]),
}
