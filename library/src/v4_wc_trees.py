"""v4_wc_trees - worker wc: heartland, alpine, dry and coastal trees (F01-F04).
Technique from v4_d05 / v4_elf / nature: tapered flared bark_trunk with roots, forking limbs,
and canopies made of many small lumpy leaf clumps in 3-4 close greens (lighter on top, darker
underneath, sky gaps between). Natural colours only, no neon. 1 unit = 1 stud, Z up, front -Y,
origin at trunk base (finalize centres on the bounding box). Trees <= 20k tris.
"""
import math, random, bpy
from mathutils import Vector
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, PAL
import v4util as U
from v4_elf import nm, bark_trunk, trunk_point, roots, limb, cluster, crown
from v4_d05 import wcluster, hang_strand, moss_on_trunk, ground_bits, trunk_r, limb_tree
from nature import blob, rock

PI = math.pi
D = math.degrees

# ---- worker palette keys (all prefixed wc_) : heartland/dry/coastal leaf + bark greens not in base ----
PAL['wc_oak_a']     = ((86, 126, 54),  'LeafyGrass', 0.0, 0.90, 0)
PAL['wc_oak_b']     = ((60, 100, 44),  'LeafyGrass', 0.0, 0.90, 0)
PAL['wc_oak_c']     = ((112, 150, 66), 'LeafyGrass', 0.0, 0.90, 0)
PAL['wc_oak_d']     = ((74, 112, 40),  'LeafyGrass', 0.0, 0.90, 0)
PAL['wc_beech_a']   = ((120, 158, 72), 'LeafyGrass', 0.0, 0.90, 0)
PAL['wc_beech_b']   = ((92, 134, 56),  'LeafyGrass', 0.0, 0.90, 0)
PAL['wc_beech_c']   = ((146, 172, 86), 'LeafyGrass', 0.0, 0.90, 0)
PAL['wc_bark_pale'] = ((150, 134, 112),'Wood',       0.0, 0.88, 0)
PAL['wc_bark_warm'] = ((96, 70, 48),   'Wood',       0.0, 0.92, 0)
PAL['wc_bark_grey'] = ((122, 112, 100),'Wood',       0.0, 0.92, 0)
PAL['wc_apple_a']   = ((98, 140, 62),  'LeafyGrass', 0.0, 0.90, 0)
PAL['wc_apple_b']   = ((72, 116, 50),  'LeafyGrass', 0.0, 0.90, 0)
PAL['wc_apple_y']   = ((214, 196, 70), 'SmoothPlastic', 0.0, 0.45, 0)
PAL['wc_fir_a']     = ((40, 78, 56),   'LeafyGrass', 0.0, 0.90, 0)
PAL['wc_fir_b']     = ((30, 62, 48),   'LeafyGrass', 0.0, 0.90, 0)
PAL['wc_fir_c']     = ((52, 92, 64),   'LeafyGrass', 0.0, 0.90, 0)
PAL['wc_dry_a']     = ((120, 138, 78), 'LeafyGrass', 0.0, 0.92, 0)
PAL['wc_dry_b']     = ((98, 116, 64),  'LeafyGrass', 0.0, 0.92, 0)
PAL['wc_dry_c']     = ((142, 150, 94), 'LeafyGrass', 0.0, 0.92, 0)
PAL['wc_olive_a']   = ((140, 150, 118),'LeafyGrass', 0.0, 0.92, 0)
PAL['wc_olive_b']   = ((112, 126, 96), 'LeafyGrass', 0.0, 0.92, 0)
PAL['wc_pine_a']    = ((46, 86, 56),   'LeafyGrass', 0.0, 0.90, 0)
PAL['wc_pine_b']    = ((34, 70, 48),   'LeafyGrass', 0.0, 0.90, 0)
PAL['wc_pine_c']    = ((62, 100, 62),  'LeafyGrass', 0.0, 0.90, 0)
PAL['wc_cyp_a']     = ((44, 74, 50),   'LeafyGrass', 0.0, 0.90, 0)
PAL['wc_cyp_b']     = ((32, 58, 42),   'LeafyGrass', 0.0, 0.90, 0)

def wc_cluster(cx, cy, z, r, seed=0, n=6, keys=None, flat=0.72, light=None, dark=None, big=False):
    """Lighter leaf clump: small lumpy blobs (subdiv=1 to stay under the tree tri budget), lighter
    on top, darker underneath, using THIS worker's palette. big=True uses subdiv=2 for the few hero clumps."""
    keys = keys or OAK
    light = light or keys[2]
    dark = dark or keys[1]
    rnd = random.Random(seed * 7 + 3)
    for i in range(n):
        a = rnd.uniform(0, 6.283)
        d = r * 0.55 * math.sqrt(rnd.random())
        dz = rnd.uniform(-r * 0.25, r * 0.3)
        br = r * rnd.uniform(0.4, 0.64)
        k = rnd.choice(keys)
        if dz > r * 0.1:
            k = light
        elif dz < -r * 0.1:
            k = dark
        sd = 2 if (big and i == 0) else 1
        blob(nm('lc'), br, (cx + math.cos(a) * d, cy + math.sin(a) * d, z + dz), k, subdiv=sd, amp=0.34,
             scale=(1, 1, flat), seed=rnd.randint(0, 999), detail=0.35)


def wc_crown(cx, cy, z, spread, thick, seed=0, count=26, keys=None, flat=0.72):
    """Natural canopy from many small subdiv=1 clumps in two loose layers; a sky-gapped lumpy dome."""
    keys = keys or OAK
    rnd = random.Random(seed + 5)
    nclu = max(6, count // 2)
    for i in range(nclu):
        layer = 0 if i % 3 else 1
        a = rnd.uniform(0, 6.283)
        d = spread * (0.35 + 0.65 * math.sqrt(rnd.random())) * (1.0 if layer == 0 else 0.62)
        zz = z + (-thick * 0.25 if layer == 0 else thick * 0.28) + rnd.uniform(-thick * 0.12, thick * 0.12)
        wc_cluster(cx + math.cos(a) * d, cy + math.sin(a) * d, zz, spread * rnd.uniform(0.2, 0.3),
                   seed=seed * 100 + i, n=rnd.randint(4, 6), keys=keys, flat=flat, big=(i < 3))
    wc_cluster(cx, cy, z + thick * 0.4, spread * 0.3, seed=seed + 77, n=6, keys=keys, flat=flat, big=True)


# use the light versions everywhere in this module (overrides the heavy v4_elf imports)
crown = wc_crown
cluster = wc_cluster


OAK = ('wc_oak_a', 'wc_oak_b', 'wc_oak_c', 'wc_oak_d')
BEECH = ('wc_beech_a', 'wc_beech_b', 'wc_beech_c', 'wc_oak_a')
AUTUMN = ('autumn_a', 'autumn_c', 'wc_oak_c', 'autumn_b')
APPLE = ('wc_apple_a', 'wc_apple_b', 'wc_oak_c', 'wc_apple_a')
FIR = ('wc_fir_a', 'wc_fir_b', 'wc_fir_c', 'wc_fir_a')
DRY = ('wc_dry_a', 'wc_dry_b', 'wc_dry_c', 'wc_dry_a')
OLIVE = ('wc_olive_a', 'wc_olive_b', 'wc_olive_a', 'wc_dry_b')
CPINE = ('wc_pine_a', 'wc_pine_b', 'wc_pine_c', 'wc_pine_a')
CYP = ('wc_cyp_a', 'wc_cyp_b', 'wc_cyp_a', 'wc_pine_b')


# ---------- shared conifer builder (spruce / fir with drooping tiered boughs) ----------
def conifer(seed, H, name, tr=None, tiers=11, width=0.26, keys=CPINE, bark='wc_bark_warm',
            droop=0.5, lean=(0.0, 0.0), clump_per_tier=9, top_r=0.18, snowy=False, flare=1.8):
    """Conical conifer: straight bark spire + rings of drooping bough clumps, wider at the base.
    Boughs are small lumpy clumps on short down-angled limbs so the silhouette is ragged, not a smooth cone."""
    reset()
    rnd = random.Random(seed)
    tr = tr or H * 0.045
    bark_trunk(tr, H, seed=seed, sway=0.3, flare=flare, key=bark, top_r=top_r, ring_h=max(1.4, H / 26), lean=lean, segs=14)
    roots(tr, n=7, seed=seed, key=bark, span=2.1)
    for i in range(tiers):
        t = i / (tiers - 1)
        z = H * (0.1 + 0.82 * t)
        R = H * width * (1 - t) ** 1.15 + H * 0.03
        cx, cy = trunk_point(tr, H, seed, z, 0.3, lean)
        nb = max(5, int(clump_per_tier * (1 - 0.5 * t)))
        for k in range(nb):
            az = i * 0.7 + 2 * PI * k / nb + rnd.uniform(-0.2, 0.2)
            c, s = math.cos(az), math.sin(az)
            ex, ey = cx + c * R, cy + s * R
            ez = z - R * droop * rnd.uniform(0.7, 1.1)
            tube(nm('bch'), [(cx, cy, z + 0.3), (cx + c * R * 0.5, cy + s * R * 0.5, z - R * droop * 0.3), (ex, ey, ez)],
                 max(0.14, tr * 0.35 * (1 - t) + 0.1), bark, res=4, taper=[1, 0.7, 0.4], ures=2)
            br = R * rnd.uniform(0.34, 0.5)
            k2 = rnd.choice(keys)
            blob(nm('bl'), br, (ex, ey, ez + br * 0.2), k2, subdiv=2, amp=0.34, scale=(1.15, 1.15, 0.62),
                 seed=rnd.randint(0, 999), detail=0.35)
            # a lighter tuft sitting on top of the bough
            if rnd.random() < 0.55:
                blob(nm('bt'), br * 0.6, (ex + rnd.uniform(-0.3, 0.3), ey + rnd.uniform(-0.3, 0.3), ez + br * 0.5),
                     keys[0] if keys[0].endswith('_c') else keys[-1], subdiv=1, amp=0.3, scale=(1, 1, 0.6), seed=rnd.randint(0, 999))
            if snowy:
                blob(nm('sn'), br * rnd.uniform(0.55, 0.8), (ex + rnd.uniform(-0.2, 0.2), ey + rnd.uniform(-0.2, 0.2), ez + br * 0.55),
                     'snow', subdiv=1, amp=0.26, scale=(1.25, 1.25, 0.4), seed=rnd.randint(0, 999))
    # spire tip
    top = trunk_point(tr, H, seed, H, 0.3, lean)
    for k in range(4):
        blob(nm('tip'), H * 0.03 + 0.5, (top[0] + rnd.uniform(-0.3, 0.3), top[1] + rnd.uniform(-0.3, 0.3), H * (0.9 + 0.03 * k)),
             rnd.choice(keys), subdiv=1, amp=0.3, scale=(0.8, 0.8, 1.1), seed=k)
    if snowy:
        blob(nm('sts'), 0.6, (top[0], top[1], H * 0.99), 'snow', subdiv=1, amp=0.25, scale=(0.9, 0.9, 0.7), seed=9)
    moss_on_trunk(tr, H, seed, 6, rnd, sway=0.3, zmin=1, zmax=H * 0.2, top_r=top_r)
    ground_bits(tr, rnd, seed, nrock=3, scale=1.0)
    return finalize(name, smooth_angle=34)


# ================================================================== F01 heartland
def F01_01_oak():
    """Great oak: thick trunk, broad round crown, ~38 high."""
    reset()
    tr, H = 3.0, 38.0
    rnd, tips, top = limb_tree(1101, tr, H, nlimb=8, z_lo=0.4, z_hi=0.72, len_rng=(11, 17), pitch=(0.25, 0.6),
                               sway=1.2, root_n=9, rspan=3.0, flare=2.1, key='wc_bark_warm')
    wc_crown(top[0], top[1], H * 0.78, 20.0, 12.0, seed=1101, count=40, keys=OAK)
    for i, e in enumerate(tips):
        wc_cluster(e.x, e.y, e.z + 1.6, rnd.uniform(4.4, 6.0), seed=1101 * 7 + i, n=6, keys=OAK)
    moss_on_trunk(tr, H, 1101, 10, rnd, sway=1.2, zmin=1, zmax=20)
    ground_bits(tr, rnd, 1101, nrock=4, scale=1.2)
    return finalize('F01_01_tree_heartland_01', smooth_angle=38)


def F01_02_beech():
    """Beech: smooth pale slim trunk, dense oval crown, ~34 high."""
    reset()
    tr, H = 2.0, 34.0
    rnd, tips, top = limb_tree(1102, tr, H, nlimb=10, z_lo=0.38, z_hi=0.82, len_rng=(7, 11), pitch=(0.55, 1.1),
                               sway=0.7, key='wc_bark_pale', top_r=0.5, flare=1.6, root_n=7, rspan=2.2, limb_r=0.3)
    crown(top[0], top[1], H * 0.68, 13.0, 20.0, seed=1102, count=42, keys=BEECH)
    for i, e in enumerate(tips):
        cluster(e.x, e.y, e.z + 1.3, rnd.uniform(3.6, 5.2), seed=1102 * 7 + i, n=6, keys=BEECH)
    moss_on_trunk(tr, H, 1102, 5, rnd, sway=0.7, zmin=1, zmax=10, top_r=0.5)
    ground_bits(tr, rnd, 1102, nrock=3, scale=1.0)
    return finalize('F01_02_tree_heartland_02', smooth_angle=38)


def F01_03_grove():
    """Grove: three mixed oaks of different heights growing close, ~30x30 footprint."""
    reset()
    rnd = random.Random(1103)
    spec = [(-6.5, -3.0, 2.4, 30.0, 1131, OAK), (6.0, 2.0, 2.8, 34.0, 1132, BEECH), (1.0, 7.5, 1.9, 24.0, 1133, OAK)]
    for ox, oy, tr, H, sd, keys in spec:
        r2 = random.Random(sd)
        bark_trunk(tr, H, seed=sd, sway=1.1, flare=2.0, key='wc_bark_warm', top_r=0.6, ring_h=max(1.4, H / 24)).location = (ox, oy, 0)
        roots(tr, n=7, seed=sd, key='wc_bark_warm', span=2.6, ox=ox, oy=oy)
        tips = []
        for k in range(7):
            az = 2 * PI * k / 7 + r2.uniform(-0.3, 0.3)
            z0 = H * r2.uniform(0.42, 0.72)
            p0 = trunk_point(tr, H, sd, z0, 1.1)
            e = limb((ox + p0[0], oy + p0[1], z0), (math.cos(az), math.sin(az), r2.uniform(0.3, 0.6)), r2.uniform(8, 13), tr * 0.32, key='wc_bark_warm', seed=k)
            tips.append(e)
        top = trunk_point(tr, H, sd, H, 1.1)
        crown(ox + top[0], oy + top[1], H * 0.78, 11.0, 9.0, seed=sd, count=24, keys=keys)
        for i, e in enumerate(tips):
            cluster(e.x, e.y, e.z + 1.4, r2.uniform(3.4, 4.8), seed=sd * 7 + i, n=5, keys=keys)
    ground_bits(2.4, rnd, 1103, ox=0.0, oy=0.0, nrock=5, scale=1.1)
    for i in range(3):
        a = rnd.uniform(0, 2 * PI); d = rnd.uniform(8, 13)
        from v4_elf import mushrooms
        mushrooms(math.cos(a) * d, math.sin(a) * d, 0.0, 4, seed=i, scale=0.9)
    return finalize('F01_03_tree_heartland_03', smooth_angle=38)


def F01_04_fruit():
    """Fruit tree (apple): short gnarled trunk, round crown with red and yellow fruit, ~18 high."""
    reset()
    tr, H = 1.9, 18.0
    rnd, tips, top = limb_tree(1104, tr, H, nlimb=6, z_lo=0.3, z_hi=0.58, len_rng=(5, 8), pitch=(0.3, 0.8),
                               sway=1.8, key='wc_bark_warm', top_r=0.6, flare=2.2, root_n=6, rspan=2.4, limb_r=0.34)
    crown(top[0], top[1], H * 0.72, 8.5, 7.5, seed=1104, count=22, keys=APPLE)
    for i, e in enumerate(tips):
        cluster(e.x, e.y, e.z + 1.0, rnd.uniform(2.8, 4.0), seed=1104 * 7 + i, n=5, keys=APPLE)
    # fruit on the canopy surface and a few windfalls on the ground
    for i in range(34):
        a = rnd.uniform(0, 2 * PI); el = rnd.uniform(-0.3, 0.7)
        d = rnd.uniform(4.5, 8.0)
        x, y = math.cos(a) * d * math.cos(el), math.sin(a) * d * math.cos(el)
        z = H * 0.72 + d * math.sin(el) * 0.7
        ball(nm('fr'), rnd.uniform(0.32, 0.42), loc=(x, y, z), key=rnd.choice(('fruit', 'fruit', 'wc_apple_y')), segs=8, rings=5)
    for i in range(6):
        a = rnd.uniform(0, 2 * PI); d = rnd.uniform(2, 6)
        ball(nm('wf'), 0.4, loc=(math.cos(a) * d, math.sin(a) * d, 0.3), key=rnd.choice(('fruit', 'wc_apple_y')), segs=8, rings=5)
    ground_bits(tr, rnd, 1104, nrock=3, scale=1.0)
    return finalize('F01_04_tree_heartland_04', smooth_angle=38)


def F01_05_elm():
    """Elm: vase-shaped (limbs sweep up and out), tall, ~40 high."""
    reset()
    tr, H = 2.6, 40.0
    rnd = random.Random(1105)
    bark_trunk(tr, H, seed=1105, sway=0.6, flare=1.9, key='wc_bark_grey', top_r=0.42, ring_h=max(1.4, H / 26))
    roots(tr, n=8, seed=1105, key='wc_bark_grey', span=2.6)
    # trunk splits low into a few main limbs that sweep up into a wide fan (vase)
    tips = []
    nmain = 5
    z_split = H * 0.4
    for k in range(nmain):
        az = 2 * PI * k / nmain + rnd.uniform(-0.2, 0.2)
        c, s = math.cos(az), math.sin(az)
        base = trunk_point(tr, H, 1105, z_split, 0.6)
        # sweep: out then strongly up
        p_mid = (base[0] + c * 6.0, base[1] + s * 6.0, z_split + 10.0)
        p_top = (base[0] + c * 11.0, base[1] + s * 11.0, H - 2.0)
        tube(nm('mn'), [(base[0], base[1], z_split), p_mid, p_top], tr * 0.5, 'wc_bark_grey', res=4, taper=[1, 0.7, 0.45], ures=3)
        tips.append(Vector(p_top))
        for j in range(2):
            az2 = az + rnd.uniform(-0.5, 0.5)
            e2 = limb(p_top, (math.cos(az2), math.sin(az2), rnd.uniform(0.6, 1.1)), rnd.uniform(5, 8), tr * 0.22, key='wc_bark_grey', seed=k * 3 + j)
            tips.append(e2)
    # broad fan crown across the top
    topc = trunk_point(tr, H, 1105, H, 0.6)
    for ring, (rad, zz, cnt) in enumerate(((13, H - 2, 8), (9, H - 5, 7), (5, H - 8, 5))):
        for j in range(cnt):
            a = 2 * PI * j / cnt + ring * 0.5
            cluster(topc[0] + math.cos(a) * rad, topc[1] + math.sin(a) * rad, zz, rnd.uniform(3.4, 4.6), seed=1105 * 9 + ring * 10 + j, n=6, keys=BEECH)
    for i, e in enumerate(tips):
        cluster(e.x, e.y, e.z + 1.0, rnd.uniform(3.0, 4.2), seed=1105 * 7 + i, n=5, keys=BEECH)
    moss_on_trunk(tr, H, 1105, 7, rnd, sway=0.6, zmin=1, zmax=16, top_r=0.42)
    ground_bits(tr, rnd, 1105, nrock=4, scale=1.1)
    return finalize('F01_05_tree_heartland_05', smooth_angle=38)


def F01_06_rowan():
    """Rowan / young maple with autumn-tinted leaves (orange/yellow/green mix), ~26 high."""
    reset()
    tr, H = 1.7, 26.0
    rnd, tips, top = limb_tree(1106, tr, H, nlimb=8, z_lo=0.4, z_hi=0.8, len_rng=(6, 9), pitch=(0.5, 1.0),
                               sway=0.9, key='wc_bark_pale', top_r=0.46, flare=1.7, root_n=6, rspan=2.2, limb_r=0.3)
    crown(top[0], top[1], H * 0.72, 11.0, 12.0, seed=1106, count=30, keys=AUTUMN)
    for i, e in enumerate(tips):
        cluster(e.x, e.y, e.z + 1.1, rnd.uniform(3.0, 4.4), seed=1106 * 7 + i, n=5, keys=AUTUMN)
    # a few berry clusters
    for i in range(14):
        a = rnd.uniform(0, 2 * PI); el = rnd.uniform(0.0, 0.7); d = rnd.uniform(5, 9)
        x, y = math.cos(a) * d * math.cos(el), math.sin(a) * d * math.cos(el)
        for k in range(4):
            ball(nm('be'), 0.14, loc=(x + rnd.uniform(-0.3, 0.3), y + rnd.uniform(-0.3, 0.3), H * 0.72 + d * math.sin(el) * 0.7 + rnd.uniform(-0.2, 0.2)), key='fl_red', segs=5, rings=3)
    ground_bits(tr, rnd, 1106, nrock=3, scale=1.0)
    return finalize('F01_06_tree_heartland_06', smooth_angle=38)


# ================================================================== F02 alpine
def F02_01_spruce():
    """Spruce, conical with drooping tiered boughs, ~36 high."""
    return conifer(1201, 36.0, 'F02_01_tree_alpine_01', tiers=12, width=0.24, keys=CPINE, droop=0.55, clump_per_tier=9)


def F02_02_fir():
    """Slim tall fir, ~44 high, dark blue-green."""
    return conifer(1202, 44.0, 'F02_02_tree_alpine_02', tr=1.7, tiers=14, width=0.17, keys=FIR, bark='wc_bark_grey', droop=0.42, clump_per_tier=8, top_r=0.14)


def F02_03_birch():
    """Bare birch in winter: white bark with dark marks, fine bare twigs, ~26 high."""
    reset()
    tr, H = 1.1, 26.0
    rnd = random.Random(1203)
    bark_trunk(tr, H, seed=1203, sway=0.9, flare=1.6, key='birch', top_r=0.4, ring_h=max(1.3, H / 24), segs=12)
    roots(tr, n=6, seed=1203, key='birch', span=1.9)
    # dark lenticel marks
    for i in range(30):
        z = rnd.uniform(1.5, H * 0.85)
        cx, cy = trunk_point(tr, H, 1203, z, 0.9)
        a = rnd.uniform(0, 2 * PI)
        rr = trunk_r(tr, H, z, 0.4) * 0.98
        box(nm('mk'), (0.5, 0.1, rnd.uniform(0.14, 0.34)), loc=(cx + math.cos(a) * rr, cy + math.sin(a) * rr, z), key='bark_dead', rot=(0, 0, D(a) + 90))
    # bare forking twigs, no foliage (winter)
    tips = []
    for k in range(9):
        az = 2 * PI * k / 9 + rnd.uniform(-0.3, 0.3)
        z0 = H * rnd.uniform(0.45, 0.85)
        p0 = trunk_point(tr, H, 1203, z0, 0.9)
        e = limb((p0[0], p0[1], z0), (math.cos(az), math.sin(az), rnd.uniform(0.7, 1.3)), rnd.uniform(5, 8), tr * 0.3, key='birch', seed=k)
        tips.append((e, az))
        for j in range(3):
            az2 = az + rnd.uniform(-0.6, 0.6)
            e2 = limb((e.x, e.y, e.z), (math.cos(az2), math.sin(az2), rnd.uniform(0.8, 1.4)), rnd.uniform(2.5, 4.5), tr * 0.15, key='birch', seed=k * 5 + j)
            # fine end twigs
            for t in range(2):
                az3 = az2 + rnd.uniform(-0.7, 0.7)
                limb((e2.x, e2.y, e2.z), (math.cos(az3), math.sin(az3), rnd.uniform(0.9, 1.5)), rnd.uniform(1.2, 2.2), tr * 0.08, key='birch', seed=k * 50 + j * 7 + t)
    top = trunk_point(tr, H, 1203, H, 0.9)
    tube(nm('lead'), [(top[0], top[1], H * 0.86), (top[0], top[1], H + 2.5)], tr * 0.2, 'birch', res=4, taper=[1, 0.2])
    # a little snow on the ground + a couple of twigs
    for i in range(4):
        a = rnd.uniform(0, 2 * PI); d = tr * rnd.uniform(2.5, 4.0)
        blob(nm('sng'), rnd.uniform(0.8, 1.4), (math.cos(a) * d, math.sin(a) * d, 0.0), 'snow', subdiv=1, amp=0.25, scale=(1.3, 1.3, 0.25), seed=i)
    ground_bits(tr, rnd, 1203, nrock=2, scale=0.9)
    return finalize('F02_03_tree_alpine_03', smooth_angle=38)


def F02_04_windpine():
    """Wind-bent mountain pine: leaning, boughs pushed to one side, ~22 high."""
    reset()
    tr, H = 1.5, 22.0
    rnd = random.Random(1204)
    lean = (0.12, 0.03)
    bark_trunk(tr, H, seed=1204, sway=0.7, flare=1.9, key='wc_bark_warm', top_r=0.3, ring_h=max(1.3, H / 20), lean=lean)
    roots(tr, n=6, seed=1204, key='wc_bark_warm', span=2.4)
    tiers = 9
    for i in range(tiers):
        t = i / (tiers - 1)
        z = H * (0.2 + 0.72 * t)
        cx, cy = trunk_point(tr, H, 1204, z, 0.7, lean)
        R = H * 0.2 * (1 - t) ** 0.9 + 1.0
        nb = max(4, int(7 * (1 - 0.4 * t)))
        for k in range(nb):
            # boughs all round the trunk but longer and lower on the leeward (+X) side
            az = 2 * PI * k / nb + rnd.uniform(-0.25, 0.25)
            c, s = math.cos(az), math.sin(az)
            lee = 1.25 if c > 0 else 0.75
            ex, ey = cx + c * R * lee * rnd.uniform(0.85, 1.15), cy + s * R * 0.8
            ez = z - R * (0.45 if c > 0 else 0.25)
            tube(nm('wb'), [(cx, cy, z + 0.2), (ex, ey, ez)], max(0.12, tr * 0.3 * (1 - t) + 0.08), 'wc_bark_warm', res=4, taper=[1, 0.5], ures=2)
            br = R * rnd.uniform(0.35, 0.52)
            blob(nm('wl'), br, (ex, ey, ez + br * 0.2), rnd.choice(CPINE), subdiv=2, amp=0.34, scale=(1.3, 1.0, 0.55), seed=rnd.randint(0, 999), detail=0.35)
    top = trunk_point(tr, H, 1204, H, 0.7, lean)
    blob(nm('tp'), 1.4, (top[0] + 0.8, top[1], H * 0.95), rnd.choice(CPINE), subdiv=1, amp=0.3, scale=(1.4, 1, 0.6), seed=3)
    for i in range(3):
        a = rnd.uniform(0, 2 * PI)
        rock(nm('gr'), rnd.uniform(0.9, 1.8), (math.cos(a) * tr * 3.0, math.sin(a) * tr * 2.6, 0.0), 'cliff_b', seed=i)
    ground_bits(tr, rnd, 1204, nrock=2, scale=1.0)
    return finalize('F02_04_tree_alpine_04', smooth_angle=36)


def F02_05_spruce_trio():
    """Cluster of three young spruces, ~14 high each."""
    reset()
    rnd = random.Random(1205)
    spec = [(-3.5, -1.5, 14.0, 1251), (3.0, 1.0, 12.5, 1252), (0.0, 4.0, 15.5, 1253)]
    for ox, oy, H, sd in spec:
        r2 = random.Random(sd)
        tr = H * 0.05
        bark_trunk(tr, H, seed=sd, sway=0.3, flare=1.7, key='wc_bark_warm', top_r=0.16, ring_h=max(1.2, H / 16)).location = (ox, oy, 0)
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
        tp = trunk_point(tr, H, sd, H, 0.3)
        blob(nm('tip'), 0.9, (ox + tp[0], oy + tp[1], H * 0.96), r2.choice(CPINE), subdiv=1, amp=0.3, scale=(0.8, 0.8, 1.1), seed=1)
    ground_bits(0.7, rnd, 1205, nrock=4, scale=0.9)
    return finalize('F02_05_tree_alpine_05', smooth_angle=34)


# ================================================================== F03 dry (scrub)
def F03_01_acacia():
    """Flat-topped acacia with a thin twisting trunk, sparse umbrella crown."""
    reset()
    tr, H = 1.4, 19.0
    rnd = random.Random(1301)
    bark_trunk(tr, H, seed=1301, sway=2.2, flare=1.8, key='wc_bark_grey', top_r=0.34, ring_h=max(1.3, H / 18))
    roots(tr, n=6, seed=1301, key='wc_bark_grey', span=2.4)
    # limbs branch near the top and spread wide, almost horizontal -> flat umbrella
    top = trunk_point(tr, H, 1301, H * 0.78, 2.2)
    tips = []
    for k in range(6):
        az = 2 * PI * k / 6 + rnd.uniform(-0.25, 0.25)
        c, s = math.cos(az), math.sin(az)
        p_mid = (top[0] + c * 5, top[1] + s * 5, H * 0.78 + 2.5)
        p_end = (top[0] + c * 11, top[1] + s * 11, H * 0.78 + 3.2)
        tube(nm('ac'), [(top[0], top[1], H * 0.78), p_mid, p_end], tr * 0.42, 'wc_bark_grey', res=4, taper=[1, 0.6, 0.3], ures=3)
        tips.append(Vector(p_end))
    # thin flat canopy pads across the top
    for i, e in enumerate(tips):
        for j in range(3):
            blob(nm('pad'), rnd.uniform(2.6, 3.6), (e.x + rnd.uniform(-2, 2), e.y + rnd.uniform(-2, 2), e.z + rnd.uniform(-0.3, 0.6)),
                 rnd.choice(DRY), subdiv=1, amp=0.3, scale=(1.25, 1.25, 0.22), seed=i * 5 + j)
    blob(nm('ctr'), 4.2, (top[0], top[1], H * 0.78 + 3.6), 'wc_dry_b', subdiv=1, amp=0.3, scale=(1.3, 1.3, 0.2), seed=9)
    # one dead snag
    tube(nm('snag'), [(trunk_point(tr, H, 1301, H*0.5, 2.2)[0], 0, H * 0.5), (3, 1, H * 0.55)], tr * 0.2, 'bark_dead', res=4, taper=[1, 0.3])
    ground_bits(tr, rnd, 1301, nrock=4, scale=1.0)
    return finalize('F03_01_tree_dry_01', smooth_angle=38)


def F03_02_juniper():
    """Gnarled juniper-like scrub tree with tufted foliage and dead branches."""
    reset()
    tr, H = 1.5, 15.0
    rnd, tips, top = limb_tree(1302, tr, H, nlimb=7, z_lo=0.3, z_hi=0.75, len_rng=(4, 7), pitch=(0.4, 1.0),
                               sway=2.4, key='wc_bark_warm', top_r=0.4, flare=2.0, root_n=7, rspan=2.6, limb_r=0.32)
    # irregular tufts of foliage, uneven
    for i, e in enumerate(tips):
        if rnd.random() < 0.75:
            for j in range(rnd.randint(2, 4)):
                blob(nm('tuf'), rnd.uniform(1.4, 2.4), (e.x + rnd.uniform(-1.2, 1.2), e.y + rnd.uniform(-1.2, 1.2), e.z + rnd.uniform(-0.5, 1.0)),
                     rnd.choice(DRY), subdiv=1, amp=0.4, scale=(1.1, 1.1, 0.7), seed=i * 7 + j, detail=0.4)
        else:
            # dead bare branch tip
            limb((e.x, e.y, e.z), (rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(0.3, 0.9)), rnd.uniform(1.5, 3), tr * 0.12, key='bark_dead', seed=i)
    moss_on_trunk(tr, H, 1302, 4, rnd, sway=2.4, zmin=1, zmax=8)
    ground_bits(tr, rnd, 1302, nrock=4, scale=1.0)
    return finalize('F03_02_tree_dry_02', smooth_angle=38)


def F03_03_olive():
    """Old olive-like tree: grey-green leaves, thick split trunk, ~17 high."""
    reset()
    tr, H = 2.2, 17.0
    rnd = random.Random(1303)
    roots(tr, n=8, seed=1303, key='wc_bark_grey', span=2.6)
    # trunk splits low into 2-3 gnarled stems
    tips = []
    z_split = 4.0
    bark_trunk(tr, z_split + 1.0, seed=1303, sway=0.6, flare=2.2, key='wc_bark_grey', top_r=0.9, ring_h=1.2)
    for k, az in enumerate((0.4, 2.5, 4.4)):
        c, s = math.cos(az), math.sin(az)
        p_mid = (c * 2.0, s * 2.0, z_split + 5.0)
        p_top = (c * 3.5, s * 3.5, H - 1.0)
        tube(nm('stem'), [(c * 0.6, s * 0.6, z_split), p_mid, p_top], tr * 0.55, 'wc_bark_grey', res=4, taper=[1, 0.75, 0.5], ures=3)
        tips.append(Vector(p_top))
        for j in range(2):
            az2 = az + rnd.uniform(-0.6, 0.6)
            e2 = limb(p_top, (math.cos(az2), math.sin(az2), rnd.uniform(0.5, 1.0)), rnd.uniform(3, 5), tr * 0.22, key='wc_bark_grey', seed=k * 3 + j)
            tips.append(e2)
    # soft grey-green rounded crown
    for i, e in enumerate(tips):
        for j in range(3):
            blob(nm('ol'), rnd.uniform(2.0, 3.0), (e.x + rnd.uniform(-1.5, 1.5), e.y + rnd.uniform(-1.5, 1.5), e.z + rnd.uniform(-0.5, 1.2)),
                 rnd.choice(OLIVE), subdiv=2, amp=0.32, scale=(1.1, 1.1, 0.75), seed=i * 5 + j, detail=0.3)
    blob(nm('crn'), 4.0, (0, 0, H - 0.5), 'wc_olive_a', subdiv=1, amp=0.3, scale=(1.2, 1.2, 0.7), seed=7)
    ground_bits(tr, rnd, 1303, nrock=4, scale=1.1)
    return finalize('F03_03_tree_dry_03', smooth_angle=38)


# ================================================================== F04 coastal (windswept pines)
def F04_01_lean_pine():
    """Tall pine leaning, crown pushed to one side."""
    reset()
    tr, H = 1.8, 32.0
    rnd = random.Random(1401)
    lean = (0.2, 0.04)
    bark_trunk(tr, H, seed=1401, sway=1.4, flare=1.9, key='wc_bark_warm', top_r=0.3, ring_h=max(1.4, H / 22), lean=lean)
    roots(tr, n=7, seed=1401, key='wc_bark_warm', span=2.6)
    # bare lower trunk, foliage pushed to the top and leeward (+X)
    tips = []
    for k in range(7):
        az = rnd.uniform(-1.0, 1.0)  # biased leeward
        z0 = H * rnd.uniform(0.6, 0.9)
        p0 = trunk_point(tr, H, 1401, z0, 1.4, lean)
        e = limb((p0[0], p0[1], z0), (math.cos(az), math.sin(az) * 0.6, rnd.uniform(0.25, 0.55)), rnd.uniform(6, 10), tr * 0.3, key='wc_bark_warm', seed=k)
        tips.append(e)
    top = trunk_point(tr, H, 1401, H, 1.4, lean)
    for i, e in enumerate(tips):
        blob(nm('cp'), rnd.uniform(3.0, 4.2), (e.x, e.y, e.z), rnd.choice(CPINE), subdiv=2, amp=0.34, scale=(1.3, 1.1, 0.5), seed=i, detail=0.35)
    blob(nm('ctop'), 4.5, (top[0] + 2, top[1], H * 0.92), 'wc_pine_a', subdiv=1, amp=0.3, scale=(1.4, 1.2, 0.45), seed=9)
    for i in range(3):
        rock(nm('gr'), rnd.uniform(1.0, 2.2), (rnd.uniform(-5, 5), rnd.uniform(-5, 5), 0.0), 'cliff_a', seed=i)
    ground_bits(tr, rnd, 1401, nrock=2, scale=1.0)
    return finalize('F04_01_tree_coastal_01', smooth_angle=36)


def F04_02_twin_pine():
    """Twin-trunk pine."""
    reset()
    tr, H = 1.5, 30.0
    rnd = random.Random(1402)
    roots(tr, n=7, seed=1402, key='wc_bark_warm', span=2.6)
    tips = []
    for sd, ox, hh, lean in ((1421, -1.4, 30.0, (-0.08, 0.03)), (1422, 1.4, 26.0, (0.1, -0.02))):
        bark_trunk(tr, hh, seed=sd, sway=1.0, flare=1.7, key='wc_bark_warm', top_r=0.3, ring_h=max(1.4, hh / 22), lean=lean).location = (ox, 0, 0)
        r2 = random.Random(sd)
        for k in range(6):
            az = 2 * PI * k / 6 + r2.uniform(-0.3, 0.3)
            z0 = hh * r2.uniform(0.55, 0.88)
            p0 = trunk_point(tr, hh, sd, z0, 1.0, lean)
            e = limb((ox + p0[0], p0[1], z0), (math.cos(az), math.sin(az), r2.uniform(0.3, 0.6)), r2.uniform(5, 9), tr * 0.3, key='wc_bark_warm', seed=k)
            tips.append(e)
        tp = trunk_point(tr, hh, sd, hh, 1.0, lean)
        for i in range(4):
            a = 2 * PI * i / 4
            blob(nm('ct'), 3.2, (ox + tp[0] + math.cos(a) * 3, tp[1] + math.sin(a) * 3, hh * 0.9), r2.choice(CPINE), subdiv=1, amp=0.32, scale=(1.3, 1.2, 0.5), seed=i)
    for i, e in enumerate(tips):
        blob(nm('cl'), rnd.uniform(2.6, 3.6), (e.x, e.y, e.z), rnd.choice(CPINE), subdiv=2, amp=0.34, scale=(1.3, 1.1, 0.5), seed=i, detail=0.35)
    ground_bits(tr, rnd, 1402, nrock=3, scale=1.0)
    return finalize('F04_02_tree_coastal_02', smooth_angle=36)


def F04_03_clipped_pine():
    """Short wind-clipped pine with a flat crown."""
    reset()
    tr, H = 1.6, 16.0
    rnd = random.Random(1403)
    lean = (0.12, 0.02)
    bark_trunk(tr, H, seed=1403, sway=1.8, flare=2.0, key='wc_bark_warm', top_r=0.38, ring_h=max(1.3, H / 14), lean=lean)
    roots(tr, n=6, seed=1403, key='wc_bark_warm', span=2.6)
    top = trunk_point(tr, H, 1403, H * 0.8, 1.8, lean)
    tips = []
    for k in range(6):
        az = 2 * PI * k / 6 + rnd.uniform(-0.3, 0.3)
        c, s = math.cos(az), math.sin(az)
        p_end = (top[0] + c * 7, top[1] + s * 7, H * 0.8 + 1.0)
        tube(nm('cl'), [(top[0], top[1], H * 0.8), (top[0] + c * 4, top[1] + s * 4, H * 0.8 + 1.5), p_end], tr * 0.35, 'wc_bark_warm', res=4, taper=[1, 0.6, 0.3], ures=2)
        tips.append(Vector(p_end))
    # dense flat wind-clipped canopy
    for i, e in enumerate(tips):
        for j in range(2):
            blob(nm('fc'), rnd.uniform(2.4, 3.2), (e.x + rnd.uniform(-1.5, 1.5), e.y + rnd.uniform(-1.5, 1.5), e.z + rnd.uniform(-0.2, 0.4)),
                 rnd.choice(CPINE), subdiv=1, amp=0.32, scale=(1.3, 1.3, 0.3), seed=i * 3 + j, detail=0.35)
    blob(nm('fctr'), 4.4, (top[0], top[1], H * 0.8 + 1.3), 'wc_pine_a', subdiv=1, amp=0.3, scale=(1.4, 1.4, 0.26), seed=7)
    for i in range(3):
        rock(nm('gr'), rnd.uniform(1.2, 2.4), (rnd.uniform(-5, 5), rnd.uniform(-5, 5), 0.0), 'cliff_a', seed=i)
    ground_bits(tr, rnd, 1403, nrock=2, scale=1.0)
    return finalize('F04_03_tree_coastal_03', smooth_angle=36)


def F04_04_cypress():
    """Tall dark cypress-like tree: narrow columnar, ~36 high."""
    reset()
    tr, H = 1.3, 36.0
    rnd = random.Random(1404)
    bark_trunk(tr, H, seed=1404, sway=0.3, flare=1.5, key='wc_bark_warm', top_r=0.22, ring_h=max(1.4, H / 26))
    roots(tr, n=5, seed=1404, key='wc_bark_warm', span=1.8)
    # tight columnar foliage: stacked narrow clumps hugging the trunk
    nz = 22
    for i in range(nz):
        t = i / (nz - 1)
        z = H * (0.1 + 0.85 * t)
        cx, cy = trunk_point(tr, H, 1404, z, 0.3)
        R = (H * 0.08) * (1 - abs(t - 0.45) * 0.8) + 0.8
        nb = 4
        for k in range(nb):
            az = i * 0.9 + 2 * PI * k / nb
            c, s = math.cos(az), math.sin(az)
            blob(nm('cy'), R * rnd.uniform(0.7, 1.0), (cx + c * R * 0.6, cy + s * R * 0.6, z), rnd.choice(CYP),
                 subdiv=1, amp=0.36, scale=(0.9, 0.9, 1.1), seed=i * 4 + k, detail=0.35)
    top = trunk_point(tr, H, 1404, H, 0.3)
    blob(nm('tip'), 1.3, (top[0], top[1], H * 0.97), 'wc_cyp_a', subdiv=1, amp=0.3, scale=(0.7, 0.7, 1.3), seed=3)
    ground_bits(tr, rnd, 1404, nrock=2, scale=0.9)
    return finalize('F04_04_tree_coastal_04', smooth_angle=36)


BATCHES = {
    'heartland': ('v4_trees', [
        ('F01_01_tree_heartland_01', F01_01_oak),
        ('F01_02_tree_heartland_02', F01_02_beech),
        ('F01_03_tree_heartland_03', F01_03_grove),
        ('F01_04_tree_heartland_04', F01_04_fruit),
        ('F01_05_tree_heartland_05', F01_05_elm),
        ('F01_06_tree_heartland_06', F01_06_rowan),
    ]),
    'alpine': ('v4_trees', [
        ('F02_01_tree_alpine_01', F02_01_spruce),
        ('F02_02_tree_alpine_02', F02_02_fir),
        ('F02_03_tree_alpine_03', F02_03_birch),
        ('F02_04_tree_alpine_04', F02_04_windpine),
        ('F02_05_tree_alpine_05', F02_05_spruce_trio),
    ]),
    'dry': ('v4_trees', [
        ('F03_01_tree_dry_01', F03_01_acacia),
        ('F03_02_tree_dry_02', F03_02_juniper),
        ('F03_03_tree_dry_03', F03_03_olive),
    ]),
    'coastal': ('v4_trees', [
        ('F04_01_tree_coastal_01', F04_01_lean_pine),
        ('F04_02_tree_coastal_02', F04_02_twin_pine),
        ('F04_03_tree_coastal_03', F04_03_clipped_pine),
        ('F04_04_tree_coastal_04', F04_04_cypress),
    ]),
}
