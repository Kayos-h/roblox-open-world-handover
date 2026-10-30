"""wi F06 - ground detail (21 models) -> v4_ground.
Logs, stumps, roots, pebbles, mossy rocks, flower patches, mushroom patches.
All small (2-8 studs), base flat at z=0, placed in the thousands: low tri counts
(<= 4k), strong silhouettes, natural colour variation, slightly irregular. No neon.
Technique follows D06 (v4_d06.py). 1 unit = 1 stud, Z up, front = -Y, origin bottom-centre.
"""
import math, random
from mathutils import Vector, Matrix
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, _obj_from_bm, top_paint
from v4_d06 import ribbon, blade, tuft, moss_skirt, daisy, polar_pts, shroom, blossom
from v4_elf import nm
from nature import blob, rock

PI = math.pi
PAL = kitlib.PAL
PAL['wi_log']        = ((120, 92, 62),  'Wood',          0.00, 0.95, 0)
PAL['wi_log_end']    = ((178, 146, 102),'Wood',          0.00, 0.85, 0)
PAL['wi_log_rot']    = ((96, 80, 60),   'Wood',          0.00, 1.00, 0)
PAL['wi_rings']      = ((158, 128, 88), 'Wood',          0.00, 0.88, 0)
PAL['wi_bracket']    = ((206, 176, 120),'SmoothPlastic', 0.00, 0.75, 0)
PAL['wi_bracket_b']  = ((164, 128, 80), 'SmoothPlastic', 0.00, 0.75, 0)
PAL['wi_pebble_a']   = ((150, 142, 130),'Rock',          0.00, 0.90, 0)
PAL['wi_pebble_b']   = ((122, 116, 108),'Rock',          0.00, 0.90, 0)
PAL['wi_pebble_c']   = ((172, 160, 142),'Rock',          0.00, 0.90, 0)
PAL['wi_pebble_d']   = ((110, 104, 100),'Slate',         0.00, 0.90, 0)
PAL['wi_gravel']     = ((140, 128, 110),'Ground',        0.00, 1.00, 0)
PAL['wi_lichen']     = ((168, 176, 140),'Grass',         0.00, 1.00, 0)
PAL['wi_poppy']      = ((188, 48, 44),  'SmoothPlastic', 0.00, 0.55, 0)
PAL['wi_corn_blue']  = ((96, 128, 196), 'SmoothPlastic', 0.00, 0.55, 0)
PAL['wi_buttercup']  = ((232, 196, 54), 'SmoothPlastic', 0.00, 0.60, 0)
PAL['wi_toadstool']  = ((190, 52, 50),  'SmoothPlastic', 0.00, 0.50, 0)

LEAFK = ('ev_leaf_a', 'ev_leaf_b', 'ev_leaf_c', 'ev_leaf_d')
GRASSK = ('ev_leaf_a', 'ev_leaf_c', 'ev_leaf_d', 'ev_fern')


# ---------------------------------------------------------------- helpers
def log_piece(cx, cy, length, r, ang, seed, mossy=True, broken=False):
    """A fallen log lying along `ang`: round bark cylinder with end caps, optional moss top & broken end."""
    rnd = random.Random(seed)
    d = Vector((math.cos(ang), math.sin(ang), 0))
    a0 = (cx - d.x * length / 2, cy - d.y * length / 2, r)
    a1 = (cx + d.x * length / 2, cy + d.y * length / 2, r)
    o = tube(nm('log'), [a0, a1], r, 'wi_log', res=6, ures=2)
    # pale sawn/broken ends
    end_prof = [(0, 0), (r * 0.9, 0), (r, 0.05), (r, 0.12), (0, 0.12)]
    for (ex, ey, sgn) in ((a0[0], a0[1], -1), (a1[0], a1[1], 1)):
        if broken and sgn == 1:
            # splintered broken end: a few jutting shards instead of a clean cap
            for s in range(5):
                aa = rnd.uniform(0, 2 * PI); rr = rnd.uniform(0.2, r * 0.9)
                tube(nm('shd'), [(ex, ey, r + math.sin(aa) * rr),
                                 (ex + d.x * rnd.uniform(0.4, 1.1), ey + d.y * rnd.uniform(0.4, 1.1), r + math.sin(aa) * rr + rnd.uniform(-0.2, 0.2))],
                     rnd.uniform(0.06, 0.14), 'wi_log_end', res=4, ures=2)
        else:
            c = lathe(nm('end'), end_prof, loc=(ex, ey, r), key='wi_log_end', segs=10,
                      rot=(0, 90 * sgn, math.degrees(ang)))
    # bark ridges
    for i in range(int(length / 0.8)):
        t = (i + 0.5) / max(1, int(length / 0.8))
        px = a0[0] + (a1[0] - a0[0]) * t
        py = a0[1] + (a1[1] - a0[1]) * t
        aa = rnd.uniform(0, 2 * PI)
        tube(nm('bk'), [(px, py, r + math.sin(aa) * r * 0.75),
                        (px + d.x * 0.5, py + d.y * 0.5, r + math.sin(aa + 0.2) * r * 0.75)],
             0.04, 'wi_log_rot', res=4, ures=2)
    if mossy:
        top_paint(o, 'ev_moss', 0.55, seed, noise_amt=0.35)
    return (a0, a1, d, r)


# ================================================================ F06_01..03 logs
def log_mossy():
    """F06_01 mossy fallen log with a broken end."""
    reset()
    rnd = random.Random(1201)
    log_piece(0, 0, 6.0, 0.9, 0.15, 1201, mossy=True, broken=True)
    moss_skirt(2.0, 1, sx=1.6, sy=0.7, loc=(0, 0, 0.0), h=0.1)
    tuft(2.4, 1.2, 0.0, rnd, n=5)
    for i in range(5):
        a = rnd.uniform(0, 2 * PI); d = rnd.uniform(1.5, 3.0)
        blob(nm('mo'), rnd.uniform(0.3, 0.5), (math.cos(a) * d, math.sin(a) * d, 0.1), 'ev_moss', subdiv=1, amp=0.3, scale=(1, 1, 0.3), seed=i)
    return finalize('log_mossy', smooth_angle=45)


def log_fungus():
    """F06_02 log with shelf (bracket) fungus growing up one side."""
    reset()
    rnd = random.Random(1202)
    a0, a1, d, r = log_piece(0, 0, 5.6, 0.85, -0.1, 1202, mossy=True, broken=False)
    side = Vector((-d.y, d.x, 0))
    if side.y > 0:          # make the shelf side face the camera (-Y)
        side = -side
    ang = math.atan2(side.y, side.x)
    for i in range(5):
        t = 0.2 + 0.6 * (i / 4) + rnd.uniform(-0.04, 0.04)
        cx = a0[0] + (a1[0] - a0[0]) * t
        cy = a0[1] + (a1[1] - a0[1]) * t
        pz = r * 0.55 + rnd.uniform(-0.1, 0.35)          # mid-height on the side, not the top
        px = cx + side.x * r * 0.85
        py = cy + side.y * r * 0.85
        br = rnd.uniform(1.0, 1.6)
        sh = ball(nm('br'), br, loc=(px + side.x * 0.25, py + side.y * 0.25, pz), key=rnd.choice(('wi_bracket', 'wi_bracket_b')), segs=8, rings=4, scale=(1.0, 0.75, 0.3))
        sh.rotation_euler = (0, math.radians(-30), ang)
        ball(nm('bru'), br * 0.92, loc=(px + side.x * 0.25, py + side.y * 0.25, pz - 0.12), key='ev_petal_cream', segs=8, rings=3, scale=(1.0, 0.72, 0.08)).rotation_euler = (0, math.radians(-30), ang)
    tuft(-2.2, -1.4, 0.0, rnd, n=5)
    return finalize('log_fungus', smooth_angle=45)


def logs_crossed():
    """F06_03 two small logs crossed over each other."""
    reset()
    rnd = random.Random(1203)
    log_piece(0, 0, 5.0, 0.7, 0.35, 1203, mossy=True, broken=True)
    # second log raised, lying across the first
    d = Vector((math.cos(-0.7), math.sin(-0.7), 0))
    length, r = 4.6, 0.6
    a0 = (-d.x * length / 2, -d.y * length / 2, 1.5)
    a1 = (d.x * length / 2, d.y * length / 2, 0.6)
    o = tube(nm('log2'), [a0, (0, 0, 1.75), a1], r, 'wi_log', res=6, ures=3)
    top_paint(o, 'ev_moss', 0.6, 23, noise_amt=0.3)
    for (ex, ey, ez, sgn) in ((a0[0], a0[1], a0[2], -1), (a1[0], a1[1], a1[2], 1)):
        lathe(nm('end'), [(0, 0), (r * 0.9, 0), (r, 0.05), (r, 0.12), (0, 0.12)], loc=(ex, ey, ez), key='wi_log_end', segs=10, rot=(0, 90 * sgn, math.degrees(-0.7)))
    tuft(2.0, 2.0, 0.0, rnd, n=5)
    return finalize('logs_crossed', smooth_angle=45)


# ================================================================ F06_04..06 stumps
def _stump(r, h, seed, rings=True, mossy=False):
    """A sawn stump: tapered bark cylinder with a ringed top face. Returns (r, h)."""
    rnd = random.Random(seed)
    o = tube(nm('st'), [(0, 0, 0.0), (0, 0, h * 0.5), (0, 0, h)], r, 'wi_log', res=8, ures=2, taper=[1.1, 1.0, 0.92])
    # bark ridges
    for i in range(int(2 * PI * r / 0.6)):
        a = 2 * PI * i / max(1, int(2 * PI * r / 0.6)) + rnd.uniform(-0.1, 0.1)
        c, s = math.cos(a), math.sin(a)
        tube(nm('bk'), [(c * r * 1.02, s * r * 1.02, 0.1), (c * r * 0.98, s * r * 0.98, h - 0.1)], 0.05, 'wi_log_rot', res=4, ures=2)
    if mossy:
        top_paint(o, 'ev_moss', 0.5, seed, noise_amt=0.35)
    # ring top
    if rings:
        for k in range(4):
            torus(nm('rg'), r * (0.85 - k * 0.2), 0.04, loc=(0, 0, h + 0.01), key='wi_rings', segs=18, rsegs=3)
        cyl(nm('tp'), r * 0.95, 0.06, loc=(0, 0, h - 0.02), key='wi_log_end', verts=16)
    # roots at the base
    for i in range(6):
        a = 2 * PI * i / 6 + rnd.uniform(-0.2, 0.2)
        c, s = math.cos(a), math.sin(a)
        tube(nm('rt'), [(c * r * 0.6, s * r * 0.6, 0.6), (c * r * 1.1, s * r * 1.1, 0.25), (c * r * 1.5, s * r * 1.5, 0.02)], r * 0.18, 'wi_log', res=4, taper=[1, 0.7, 0.4], ures=2)
    return rnd


def stump_sawn():
    """F06_04 sawn stump with growth rings and an axe-cut notch."""
    reset()
    rnd = _stump(1.9, 3.0, 1204, rings=True, mossy=False)
    # axe-cut wedge notch in the top rim
    box(nm('axe'), (0.9, 0.5, 0.9), loc=(1.5, 0, 3.0), key='wi_log_end', rot=(0, 30, 0), bev=0.02)
    tuft(2.6, 1.6, 0.0, rnd, n=5)
    return finalize('stump_sawn', smooth_angle=45)


def stump_rotten():
    """F06_05 rotten stump with moss and a soft broken top."""
    reset()
    rnd = random.Random(1205)
    o = tube(nm('st'), [(0, 0, 0.0), (0, 0, 1.4), (0.2, 0.1, 2.6)], 1.7, 'wi_log_rot', res=8, ures=3, taper=[1.15, 1.0, 0.78])
    # jagged soft top: a ring of uneven stubs
    for i in range(7):
        a = 2 * PI * i / 7 + rnd.uniform(-0.2, 0.2)
        c, s = math.cos(a), math.sin(a)
        tube(nm('stub'), [(c * 1.1, s * 1.1, 2.3), (c * 1.2, s * 1.2, 2.6 + rnd.uniform(0, 0.9))], rnd.uniform(0.15, 0.3), 'wi_log_rot', res=4, ures=2)
    top_paint(o, 'ev_moss', 0.42, 1205, noise_amt=0.4)
    moss_skirt(2.4, 5, sx=1.1, sy=1.0, h=0.14)
    for i in range(5):
        a = rnd.uniform(0, 2 * PI); d = rnd.uniform(0.3, 1.2)
        blob(nm('mo'), rnd.uniform(0.3, 0.55), (math.cos(a) * d, math.sin(a) * d, 2.4), 'ev_moss', subdiv=1, amp=0.3, scale=(1, 1, 0.4), seed=i)
    tuft(2.4, -1.4, 0.0, rnd, n=5)
    return finalize('stump_rotten', smooth_angle=42)


def stump_splintered():
    """F06_06 tall splintered stump: snapped trunk with jagged vertical shards."""
    reset()
    rnd = random.Random(1206)
    _stump(1.5, 3.6, 1206, rings=False, mossy=True)
    # tall splinters shooting up from the break
    for i in range(8):
        a = rnd.uniform(0, 2 * PI); d = rnd.uniform(0.2, 1.2)
        x, y = math.cos(a) * d, math.sin(a) * d
        h = rnd.uniform(1.5, 4.2)
        lean = Vector((rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3), 0))
        tube(nm('sp'), [(x, y, 3.4), (x + lean.x, y + lean.y, 3.6 + h)], rnd.uniform(0.08, 0.2), 'wi_log', res=4, ures=2, taper=[1, 0.25])
    tuft(-2.2, 1.6, 0.0, rnd, n=5)
    return finalize('stump_splintered', smooth_angle=42)


# ================================================================ F06_07..08 roots
def root_arch():
    """F06_07 exposed tree-root arch: a couple of big roots forming a gateway you look through."""
    reset()
    rnd = random.Random(1207)
    # two main roots arcing from one side, over, and down the other - like croquet hoops side by side
    for k, span in enumerate((0.0, 0.9)):
        y = -0.8 + span
        apex = 3.0 - k * 0.4
        pts = [(-3.6, y + rnd.uniform(-0.2, 0.2), 0.02),
               (-2.2, y, apex * 0.55),
               (0.0, y + rnd.uniform(-0.3, 0.3), apex),
               (2.2, y, apex * 0.55),
               (3.6, y + rnd.uniform(-0.2, 0.2), 0.02)]
        o = tube(nm('rt'), pts, 0.42 - k * 0.06, 'wi_log', res=5, ures=4, taper=[0.5, 0.9, 1.0, 0.9, 0.5])
        top_paint(o, 'ev_moss', 0.6, k, noise_amt=0.3)
    # a couple of smaller side roots branching off near the ground
    for (sx, sy, dx) in ((-3.4, -0.6, -1.4), (3.4, 0.4, 1.4)):
        pts = [(sx, sy, 0.6), (sx + dx * 0.5, sy + rnd.uniform(-0.6, 0.6), 0.3), (sx + dx, sy + rnd.uniform(-0.8, 0.8), 0.02)]
        o = tube(nm('sr'), pts, 0.22, 'wi_log', res=4, ures=2, taper=[1, 0.7, 0.4])
        top_paint(o, 'ev_moss', 0.65, 9, noise_amt=0.3)
    # a little soil mound where the roots dive in
    for (mx, my) in ((-3.5, -0.2), (3.5, 0.2)):
        blob(nm('soil'), 1.0, (mx, my, 0.0), 'wi_log_rot', subdiv=1, amp=0.3, scale=(1.1, 1.3, 0.4), seed=int(mx))
    moss_skirt(2.4, 7, sx=1.4, sy=1.0, h=0.08)
    tuft(0.0, 2.2, 0.0, rnd, n=5)
    tuft(-1.6, -2.4, 0.0, rnd, n=4)
    return finalize('root_arch', smooth_angle=40)


def root_tangle():
    """F06_08 root tangle with a few stones caught in it."""
    reset()
    rnd = random.Random(1208)
    blob(nm('knot'), 1.2, (0, 0, 0.8), 'wi_log', subdiv=2, amp=0.35, scale=(1.2, 1.0, 0.7), seed=2)
    for i in range(9):
        a = rnd.uniform(0, 2 * PI)
        c, s = math.cos(a), math.sin(a)
        reach = rnd.uniform(2.0, 3.6)
        pts = [(c * 0.5, s * 0.5, 0.7)]
        for k in range(1, 4):
            t = k / 3
            pts.append((c * reach * t + rnd.uniform(-0.5, 0.5), s * reach * t + rnd.uniform(-0.5, 0.5), max(0.02, 0.7 - 0.7 * t) + rnd.uniform(-0.1, 0.3)))
        o = tube(nm('rt'), pts, rnd.uniform(0.18, 0.34), 'wi_log', res=4, ures=3, taper=[1, 0.8, 0.5, 0.3])
        if rnd.random() < 0.6:
            top_paint(o, 'ev_moss', 0.65, i, noise_amt=0.3)
    for (sx, sy, sr, sd) in ((1.8, -1.2, 0.8, 11), (-1.6, 1.4, 0.6, 12), (0.4, 2.0, 0.5, 13)):
        rr = rock(nm('rk'), sr, (sx, sy, 0.1), 'ev_stone_dark', seed=sd, scale=(1.2, 1.0, 0.7))
        top_paint(rr, 'ev_moss', 0.6, sd)
    tuft(-2.4, -1.8, 0.0, rnd, n=5)
    return finalize('root_tangle', smooth_angle=40)


# ================================================================ F06_09..12 pebbles
def _pebble(x, y, r, key, seed, flat=0.5):
    o = rock(nm('pb'), r, (x, y, r * flat * 0.5), key, seed=seed, scale=(1.2, 1.0, flat), subdiv=2, amp=0.28, rot_z=seed * 0.7)
    return o


def pebbles_river():
    """F06_09 smooth river pebbles: a flat scatter of rounded stones."""
    reset()
    rnd = random.Random(1209)
    keys = ('wi_pebble_a', 'wi_pebble_b', 'wi_pebble_c', 'wi_pebble_d')
    for (x, y) in polar_pts(rnd, 26, 3.6, 0.8):
        _pebble(x, y, rnd.uniform(0.35, 0.95), rnd.choice(keys), rnd.randint(0, 999), flat=rnd.uniform(0.4, 0.6))
    return finalize('pebbles_river', smooth_angle=35)


def scree_chips():
    """F06_10 sharp scree chips: angular broken rock fragments."""
    reset()
    rnd = random.Random(1210)
    keys = ('wi_pebble_d', 'wi_pebble_b', 'ev_stone_dark')
    for (x, y) in polar_pts(rnd, 30, 3.6, 0.7):
        r = rnd.uniform(0.3, 0.8)
        # angular chip: low-subdiv blob, less smoothing so it reads sharp
        o = blob(nm('ch'), r, (x, y, r * 0.3), rnd.choice(keys), subdiv=1, amp=0.5, scale=(1.3, 0.9, rnd.uniform(0.3, 0.55)), seed=rnd.randint(0, 999))
        o.rotation_euler = (rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3), rnd.uniform(0, 2 * PI))
    return finalize('scree_chips', smooth_angle=18)


def stepping_stones():
    """F06_11 flat stepping-stone cluster: a few broad low slabs."""
    reset()
    rnd = random.Random(1211)
    keys = ('wi_pebble_a', 'wi_pebble_c', 'ev_stone')
    for (x, y) in polar_pts(rnd, 7, 3.4, 1.7):
        r = rnd.uniform(1.0, 1.7)
        o = rock(nm('ss'), r, (x, y, 0.1), rnd.choice(keys), seed=rnd.randint(0, 999), scale=(1.1, 1.0, 0.22), subdiv=2, amp=0.2, rot_z=rnd.uniform(0, 6.28))
        if rnd.random() < 0.4:
            top_paint(o, 'wi_lichen', 0.8, rnd.randint(0, 99), noise_amt=0.2)
    return finalize('stepping_stones', smooth_angle=30)


def gravel_patch():
    """F06_12 mixed gravel patch with a few grass tufts."""
    reset()
    rnd = random.Random(1212)
    blob(nm('base'), 3.6, (0, 0, 0.0), 'wi_gravel', subdiv=2, amp=0.15, scale=(1.0, 0.9, 0.08), seed=12)
    keys = ('wi_pebble_a', 'wi_pebble_b', 'wi_pebble_c', 'wi_pebble_d', 'wi_gravel')
    for (x, y) in polar_pts(rnd, 34, 3.2, 0.52):
        _pebble(x, y, rnd.uniform(0.18, 0.5), rnd.choice(keys), rnd.randint(0, 999), flat=rnd.uniform(0.4, 0.6))
    for (x, y) in polar_pts(rnd, 4, 3.0, 1.6):
        tuft(x, y, 0.0, rnd, n=5)
    return finalize('gravel_patch', smooth_angle=32)


# ================================================================ F06_13..15 mossy rocks
def _mossy(o, thr, seed):
    top_paint(o, 'ev_moss', thr, seed, noise_amt=0.3)
    return o


def boulder_mossy():
    """F06_13 lumpy boulder with thick moss over the top."""
    reset()
    rnd = random.Random(1213)
    a = rock(nm('rk'), 3.2, (0, 0, 1.6), 'ev_stone_dark', seed=11, scale=(1.2, 1.0, 0.85), subdiv=3, amp=0.34)
    _mossy(a, 0.42, 11)
    moss_skirt(4.0, 14, sx=1.1, sy=0.95)
    for i in range(6):
        a2 = rnd.uniform(0, 2 * PI); d = rnd.uniform(1.0, 2.6)
        blob(nm('mo'), rnd.uniform(0.3, 0.6), (math.cos(a2) * d, math.sin(a2) * d, 0.1), 'ev_moss', subdiv=1, amp=0.3, scale=(1, 1, 0.3), seed=i)
    tuft(2.6, -1.8, 0.0, rnd, n=5)
    return finalize('boulder_mossy', smooth_angle=22)


def slab_lichen():
    """F06_14 flat slab with pale lichen blotches."""
    reset()
    rnd = random.Random(1214)
    o = rock(nm('rk'), 3.4, (0, 0, 0.5), 'ev_stone', seed=21, scale=(1.3, 1.0, 0.32), subdiv=3, amp=0.22)
    top_paint(o, 'wi_lichen', 0.55, 21, noise_amt=0.4)
    for i in range(3):
        a = rnd.uniform(0, 2 * PI); d = rnd.uniform(2.0, 3.0)
        rock(nm('rk2'), rnd.uniform(0.4, 0.8), (math.cos(a) * d, math.sin(a) * d, 0.1), 'ev_stone_dark', seed=30 + i, scale=(1.2, 1.0, 0.6))
    tuft(-2.6, 1.6, 0.0, rnd, n=5)
    return finalize('slab_lichen', smooth_angle=28)


def split_rock():
    """F06_15 split rock pair: one boulder cracked into two leaning halves."""
    reset()
    rnd = random.Random(1215)
    for (x, y, lean, sd) in ((-0.9, 0, -0.18, 41), (0.9, 0, 0.18, 42)):
        o = rock(nm('rk'), 2.4, (x, y, 1.4), 'ev_stone_dark', seed=sd, scale=(0.7, 1.1, 0.95), subdiv=3, amp=0.3)
        o.rotation_euler = (0, lean, rnd.uniform(-0.2, 0.2))
        _mossy(o, 0.5, sd)
    moss_skirt(3.6, 15, sx=1.0, sy=1.1)
    tuft(2.4, 2.0, 0.0, rnd, n=5)
    tuft(-2.4, -2.0, 0.0, rnd, n=5)
    return finalize('split_rock', smooth_angle=22)


# ================================================================ F06_16..19 flower patches
def _petal_flower(x, y, h, rnd, pk, ck, npet=6, pr=0.5, pw=0.5):
    tube(nm('st'), [(x, y, 0), (x, y, h)], 0.045, 'ev_leaf_b', res=3, ures=1)
    tz = h
    a0 = rnd.uniform(0, 2 * PI)
    for p in range(npet):
        a = a0 + 2 * PI * p / npet
        o = ball(nm('pt'), pr * 0.55, loc=(x + math.cos(a) * pr * 0.55, y + math.sin(a) * pr * 0.55, tz + 0.03), key=pk, segs=4, rings=3, scale=(1.0, pw, 0.18))
        o.rotation_euler = (0, math.radians(-12), a)
    ball(nm('cn'), pr * 0.28, loc=(x, y, tz + 0.05), key=ck, segs=5, rings=3, scale=(1, 1, 0.7))


def _flower_patch(seed, keys, ck, npet, pr, pw, hrange, grass_between=True, mound_r=3.4, n=11):
    reset()
    rnd = random.Random(seed)
    blob(nm('mound'), mound_r, (0, 0, 0.0), 'ev_moss', subdiv=1, amp=0.2, scale=(1.0, 0.92, 0.1), seed=seed)
    if grass_between:
        for (x, y) in polar_pts(rnd, 5, mound_r * 0.85, 1.5):
            tuft(x, y, 0.0, rnd, n=4)
    for i, (x, y) in enumerate(polar_pts(rnd, n, mound_r * 0.85, 1.1)):
        _petal_flower(x, y, rnd.uniform(*hrange), rnd, keys[i % len(keys)], ck, npet=npet, pr=pr, pw=pw)
    return rnd


def flowers_buttercup():
    """F06_16 yellow buttercups: small round golden five-petal flowers in grass."""
    rnd = _flower_patch(1216, ('wi_buttercup',), 'ev_petal_gold', 5, 0.42, 0.9, (1.6, 2.6), n=12)
    return finalize('flowers_buttercup', smooth_angle=45)


def flowers_cornflower():
    """F06_17 blue cornflowers with grass: ragged blue heads on slim stems."""
    rnd = _flower_patch(1217, ('wi_corn_blue', 'ev_petal_blue'), 'ev_berry', 7, 0.46, 0.4, (2.2, 3.4), n=10)
    return finalize('flowers_cornflower', smooth_angle=45)


def flowers_poppy():
    """F06_18 red poppies: broad red cupped petals with a dark centre."""
    rnd = _flower_patch(1218, ('wi_poppy',), 'ev_berry', 5, 0.62, 0.8, (2.4, 3.6), n=10)
    return finalize('flowers_poppy', smooth_angle=45)


def flowers_wild():
    """F06_19 mixed wildflower patch: soft natural petal colours, grass between."""
    reset()
    rnd = random.Random(1219)
    blob(nm('mound'), 3.6, (0, 0, 0.0), 'ev_moss', subdiv=1, amp=0.2, scale=(1.0, 0.92, 0.1), seed=19)
    for (x, y) in polar_pts(rnd, 5, 3.0, 1.5):
        tuft(x, y, 0.0, rnd, n=4)
    mix = (('wi_poppy', 'ev_berry', 5, 0.55, 0.8), ('wi_buttercup', 'ev_petal_gold', 5, 0.4, 0.9),
           ('wi_corn_blue', 'ev_berry', 7, 0.42, 0.4), ('ev_petal_pink', 'ev_petal_gold', 6, 0.46, 0.6),
           ('ev_petal_cream', 'ev_petal_gold', 7, 0.44, 0.45))
    for i, (x, y) in enumerate(polar_pts(rnd, 11, 3.0, 1.1)):
        pk, ck, npet, pr, pw = mix[i % len(mix)]
        _petal_flower(x, y, rnd.uniform(1.8, 3.2), rnd, pk, ck, npet=npet, pr=pr, pw=pw)
    return finalize('flowers_wild', smooth_angle=45)


# ================================================================ F06_20..21 mushroom patches
def shrooms_brown():
    """F06_20 brown-cap cluster at a log end."""
    reset()
    rnd = random.Random(1220)
    # short log end they grow against
    o = tube(nm('log'), [(-2.6, 0.4, 0.7), (-0.4, 0.2, 0.7)], 0.7, 'wi_log', res=6, ures=2)
    lathe(nm('end'), [(0, 0), (0.6, 0), (0.7, 0.05), (0.7, 0.12), (0, 0.12)], loc=(-0.4, 0.2, 0.7), key='wi_log_end', segs=10, rot=(0, 90, -5))
    top_paint(o, 'ev_moss', 0.6, 20, noise_amt=0.3)
    moss_skirt(2.4, 20, sx=1.3, sy=0.9, loc=(-0.6, 0.2, 0.0), h=0.12)
    caps = ('ev_shroom_brown', 'ev_shroom_tan', 'ev_shroom_umber', 'ev_shroom_brown')
    placed = []
    spec = [(2.6, 1.0), (2.2, 0.85), (1.8, 0.7), (1.6, 0.6), (1.2, 0.5), (1.0, 0.42), (0.8, 0.35)]
    for i, (h, r) in enumerate(spec):
        for _ in range(60):
            a = rnd.uniform(0, 2 * PI); d = math.sqrt(rnd.random()) * 1.8
            p = (0.6 + math.cos(a) * d, math.sin(a) * d)
            if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > (r + q[2] + 0.2) ** 2 for q in placed):
                break
        placed.append((p[0], p[1], r))
        shroom(p[0], p[1], 0.0, h, r, caps[i % 4], tilt=(rnd.uniform(-0.12, 0.12), rnd.uniform(-0.12, 0.12)), style='dome' if i % 2 else 'bell')
    tuft(2.6, -1.6, 0.0, rnd, n=5)
    return finalize('shrooms_brown', smooth_angle=50)


def shrooms_toadstool():
    """F06_21 small red-and-white toadstool ring (fairy ring)."""
    reset()
    rnd = random.Random(1221)
    moss_skirt(3.4, 21, sx=1.05, sy=1.0, h=0.14)
    ring_r = 2.4
    n = 7
    for i in range(n):
        a = 2 * PI * i / n + rnd.uniform(-0.12, 0.12)
        x, y = math.cos(a) * ring_r, math.sin(a) * ring_r
        h = rnd.uniform(1.4, 2.4); r = rnd.uniform(0.6, 0.95)
        shroom(x, y, 0.0, h, r, 'wi_toadstool', style='dome', spots=7, rnd=rnd)
    # one or two small ones in the middle
    for (x, y, h, r) in ((0.3, 0.2, 1.0, 0.45), (-0.5, -0.4, 0.7, 0.35)):
        shroom(x, y, 0.0, h, r, 'wi_toadstool', style='dome', spots=5, rnd=rnd)
    for i in range(4):
        a = rnd.uniform(0, 2 * PI)
        tuft(math.cos(a) * 3.0, math.sin(a) * 3.0, 0.0, rnd, n=4)
    return finalize('shrooms_toadstool', smooth_angle=50)


BATCHES = {
    'logs_stumps': ('v4_ground', [
        ('F06_01_log_mossy', log_mossy, (0.7, -1.0, 0.4)),
        ('F06_02_log_fungus', log_fungus, (0.7, -1.0, 0.4)),
        ('F06_03_logs_crossed', logs_crossed, (0.8, -1.0, 0.45)),
        ('F06_04_stump_sawn', stump_sawn, (0.8, -1.0, 0.5)),
        ('F06_05_stump_rotten', stump_rotten, (0.8, -1.0, 0.5)),
        ('F06_06_stump_splintered', stump_splintered, (0.8, -1.0, 0.5)),
        ('F06_07_root_arch', root_arch, (0.8, -1.0, 0.45)),
        ('F06_08_root_tangle', root_tangle, (0.8, -1.0, 0.5)),
    ]),
    'pebbles': ('v4_ground', [
        ('F06_09_pebbles_river', pebbles_river, (0.8, -1.0, 0.6)),
        ('F06_10_scree_chips', scree_chips, (0.8, -1.0, 0.6)),
        ('F06_11_stepping_stones', stepping_stones, (0.8, -1.0, 0.6)),
        ('F06_12_gravel_patch', gravel_patch, (0.8, -1.0, 0.6)),
    ]),
    'mossy_rocks': ('v4_ground', [
        ('F06_13_boulder_mossy', boulder_mossy, (0.9, -1.1, 0.45)),
        ('F06_14_slab_lichen', slab_lichen, (0.9, -1.1, 0.5)),
        ('F06_15_split_rock', split_rock, (0.9, -1.1, 0.45)),
    ]),
    'flowers': ('v4_ground', [
        ('F06_16_flowers_buttercup', flowers_buttercup, (0.8, -1.0, 0.5)),
        ('F06_17_flowers_cornflower', flowers_cornflower, (0.8, -1.0, 0.5)),
        ('F06_18_flowers_poppy', flowers_poppy, (0.8, -1.0, 0.5)),
        ('F06_19_flowers_wild', flowers_wild, (0.8, -1.0, 0.5)),
    ]),
    'mushrooms': ('v4_ground', [
        ('F06_20_shrooms_brown', shrooms_brown, (0.8, -1.0, 0.45)),
        ('F06_21_shrooms_toadstool', shrooms_toadstool, (0.8, -1.0, 0.5)),
    ]),
}
