"""v5_fx_ve - FIX ROUND builders for assignment A6 (worker ve). Owner: builder A6.
Replaces round-1 ve builders for: LM02 world-tree falls (REDO), LM01 trunk door (MAJOR), EV03 path pieces 03/04/05/06 (MAJOR/MINOR),
EV01 elf houses 01/05 (MINOR), EV02_03 canopy (OK-note), TW01 statue (MINOR), TW02_06 street prop (MINOR), TW03_01/04 avenue (MINOR/OK-note).
Reuses ve palette E / T1 via ORIG. New keys only under ve_f_. No glow, pale matte stepped water, front -Y, pivot bottom centre.
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v4util
import v5kit
from v5kit import Acc, polar, tang, mk, ids, band, strata
import v5gen as G
from v5gen import house, round_tower, wall_seg, column, cliff, spire, rock_arch, tree
import v5_ve as ORIG          # round-1 module: reuse its E/T1 palettes and helpers; never edit it

E = ORIG.E
T1 = ORIG.T1

P = G.reg('ve_f', {
    'water':    ((150, 176, 190), 'SmoothPlastic', 0.0, 0.55),   # pale matte water (no neon/cyan)
    'water_dp': ((120, 150, 168), 'SmoothPlastic', 0.0, 0.60),
    'foam':     ((224, 230, 232), 'SmoothPlastic', 0.0, 0.70),
    'rock_a':   ((120, 116, 112), 'Rock', 0.0, 0.95),
    'rock_b':   ((98, 94, 90),    'Rock', 0.0, 0.95),
    'rock_c':   ((140, 136, 130), 'Rock', 0.0, 0.92),
    'rock_base':((80, 77, 74),    'Slate', 0.0, 0.95),
    'barkdk':   ((110, 86, 62),   'Wood', 0.0, 0.95),
    'barkmid':  ((150, 120, 86),  'Wood', 0.0, 0.92),
    'moss':     ((96, 124, 72),   'Grass', 0.0, 1.0),
    'deckwood': ((156, 124, 86),  'WoodPlanks', 0.0, 0.85),
    'niche':    ((40, 36, 34),    'Slate', 0.0, 1.0),
    'bone':     ((226, 218, 200), 'Limestone', 0.0, 0.85),
    'cloth_r':  ((150, 60, 54),   'Fabric', 0.0, 1.0),
    'cloth_b':  ((60, 84, 120),   'Fabric', 0.0, 1.0),
})

CLIFF = [P['rock_b'], P['rock_a'], P['rock_c']]


def _fin(A, name):
    A.to_scene()
    return finalize(name, 28)


# ------------------------------------------------------------------ shared pale stepped waterfall (hugs rock, no bright slabs)
def _falls(A, rnd, cx, cy_face, ztop, zbot, width, steps=6, pool_y=None, pool_w=None):
    n = steps
    dz = (ztop - zbot) / n
    for i in range(n):
        zt = ztop - i * dz
        zb = zt - dz
        w = width * (1.0 - 0.04 * i)
        yf = cy_face - 0.7 - i * 0.5
        A.box((w, 1.0, dz * 1.14), (cx, yf, (zt + zb) / 2.0), P['water'], (6, 0, 0), bev=0)
        nb = max(2, int(w / 4.0))
        for b in range(nb):
            bx = cx - w / 2 + (b + 0.5) * w / nb + rnd.uniform(-0.5, 0.5)
            A.box((w / nb * 0.5, 0.45, dz * rnd.uniform(0.7, 1.05)), (bx, yf - 0.55, (zt + zb) / 2.0 + rnd.uniform(-0.4, 0.4)), P['water_dp'], bev=0)
        A.box((w * 0.92, 1.3, dz * 0.22), (cx, yf - 0.6, zb + dz * 0.12), P['foam'], (10, 0, 0), bev=0)
        for k in range(max(3, int(w / 3))):
            A.ball(rnd.uniform(0.45, 0.9), (cx + rnd.uniform(-w / 2, w / 2), yf - 0.8, zb + rnd.uniform(0, dz * 0.3)), P['foam'], segs=6, rings=4, scale=(1.3, 1.0, 0.5))
    py = pool_y if pool_y is not None else cy_face - 1.5 - n * 0.5 - 4.0
    pw = pool_w if pool_w is not None else width + 8.0
    A.chunk((pw + 5.0, 14.0, 2.6), (cx, py, zbot - 0.5), P['rock_base'], (0, 0, 0), 0.1, rnd)
    A.box((pw, 11.0, 0.9), (cx, py, zbot + 0.6), P['water_dp'], bev=0)
    for k in range(9):
        A.ball(rnd.uniform(0.7, 1.4), (cx + rnd.uniform(-pw / 2, pw / 2), py + rnd.uniform(-4, 4), zbot + 0.9), P['foam'], segs=6, rings=4, scale=(1.4, 1.2, 0.45))


# ------------------------------------------------------------------ continuous falling sheet (one unbroken column, not window-like panels)
def _sheet_falls(A, rnd, cx, cy_face, ztop, zbot, width, pool_y=None, pool_w=None, breaks=2):
    H = ztop - zbot
    nseg = max(5, int(H / 12.0))
    dz = H / nseg
    for i in range(nseg):
        zt = ztop - i * dz
        w = width * (1.0 - 0.06 * (i / nseg))
        yf = cy_face - 0.6 - 0.18 * i
        A.box((w, 0.9, dz * 1.1), (cx, yf, zt - dz / 2.0), P['water'], (4, 0, 0), bev=0)
    nb = max(3, int(width / 3.0))
    for b in range(nb):
        bx = cx - width / 2 + (b + 0.5) * width / nb + rnd.uniform(-0.3, 0.3)
        bw = width / nb * rnd.uniform(0.3, 0.55)
        A.box((bw, 0.45, H * rnd.uniform(0.9, 1.0)), (bx, cy_face - 0.9, zbot + H / 2.0 + rnd.uniform(-1.5, 1.5)), P['water_dp'], (4, 0, 0), bev=0)
    A.box((width * 1.02, 1.2, 1.0), (cx, cy_face - 0.4, ztop - 0.4), P['foam'], bev=0)
    for q in range(breaks):
        zq = zbot + H * (0.35 + 0.3 * q)
        A.box((width * 0.85, 1.4, 1.2), (cx, cy_face - 0.9, zq), P['foam'], (8, 0, 0), bev=0)
    py = pool_y if pool_y is not None else cy_face - 2.0 - 4.0
    pw = pool_w if pool_w is not None else width + 10.0
    A.chunk((pw + 5.0, 14.0, 2.6), (cx, py, zbot - 0.5), P['rock_base'], (0, 0, 0), 0.1, rnd)
    A.box((pw, 11.0, 0.9), (cx, py, zbot + 0.6), P['water_dp'], bev=0)
    for k in range(12):
        A.ball(rnd.uniform(0.7, 1.4), (cx + rnd.uniform(-pw / 2, pw / 2), py + rnd.uniform(-4, 4), zbot + 0.9), P['foam'], segs=6, rings=4, scale=(1.4, 1.2, 0.45))
def tree_falls():
    """LM02_01 (round 3, lead) - a tree-trunk cliff with pale falls. 80 x 40 x 110. Same design as the round-2 version, but every bark rib now sits ON the tapering trunk
    (the old straight ribs hovered up to 5 studs off the narrow upper trunk and read as detached planks); no hanging roots, no scattered rubble."""
    reset()
    A = Acc()
    rnd = random.Random(1631)
    A.cyl(30.0, 110.0, (6.0, 10.0, 0.0), P['barkdk'], verts=20, r2=22.0)
    for k in range(34):
        zc = rnd.uniform(16.0, 92.0)
        L = rnd.uniform(22.0, 38.0)
        a = rnd.uniform(0, 360)
        r = 30.0 - 8.0 * (zc / 110.0) - 1.3
        x, y, _ = polar(r, a)
        A.chunk((3.2, 3.2, L), (6.0 + x, 10.0 + y, zc), P['barkmid'] if k % 2 else P['barkdk'], (0, 0, a), 0.1, rnd, (0.55, 0.8))
    for k in range(9):
        a = 360.0 / 9 * k + rnd.uniform(-6, 6)
        x, y, _ = polar(26.0, a)
        A.beam((6.0 + x * 1.7, 10.0 + y * 1.7, 0.4), (6.0 + x * 0.5, 10.0 + y * 0.5, 16.0), 6.0, 6.0, P['barkdk'])
    for cx, hc in ((-18.0, 96.0), (18.0, 84.0)):
        z = 0.0
        while z < hc:
            sh = min(rnd.uniform(6, 11), hc - z)
            t = z / 110.0
            A.chunk((rnd.uniform(14, 20), rnd.uniform(14, 20), sh * 1.1), (cx + rnd.uniform(-3, 3), -8.0 + rnd.uniform(-2, 2), z + sh / 2), band(CLIFF, t, rnd), (0, rnd.uniform(-5, 5), rnd.uniform(-7, 7)), 0.12, rnd, (0.9, 0.9))
            z += sh * 0.85
    for k in range(70):
        cx = rnd.uniform(-30, 30)
        z = rnd.uniform(6, 96)
        A.chunk((rnd.uniform(3, 7), rnd.uniform(2, 4), rnd.uniform(3, 7)), (cx, -14.0 + rnd.uniform(-1, 3), z), band(CLIFF, z / 110.0, rnd), (0, rnd.uniform(-7, 7), rnd.uniform(-9, 9)), 0.14, rnd, (0.9, 0.9))
    for k in range(10):
        A.chunk((rnd.uniform(6, 10), rnd.uniform(3, 5), rnd.uniform(1.2, 2.2)), (rnd.uniform(-24, 24), -14.0, rnd.uniform(12, 80)), P['moss'], (0, 0, rnd.uniform(-6, 6)), 0.14, rnd)
    _sheet_falls(A, rnd, -16.0, -16.0, 94.0, 10.0, 18.0, pool_y=-28.0, pool_w=26.0, breaks=2)
    _sheet_falls(A, rnd, 16.0, -14.0, 72.0, 8.0, 12.0, pool_y=-26.0, pool_w=20.0, breaks=1)
    for k in range(18):
        a = rnd.uniform(0, 360)
        r = rnd.uniform(0, 24)
        x, y, _ = polar(r, a)
        A.ball(rnd.uniform(7, 13), (6.0 + x, 10.0 + y, 103.0 + rnd.uniform(-4, 6)), E['leaf1'] if k % 2 else E['leaf2'], segs=9, rings=6, scale=(1.3, 1.2, 0.85))
    A.cyl(24.0, 4.0, (6.0, 10.0, 108.0), E['moss'], verts=20, r2=20.0)
    return v5kit.fit(_fin(A, 'world_tree_falls'), w=80.0, d=40.0, h=110.0)


# ================================================================== LM01 world tree trunk door (MAJOR)
def trunk_door():
    """LM01_01 - solid flared trunk, 36 x 36 x 50: merged root buttresses (no gaps), closed top, clear recessed door."""
    reset()
    A = Acc()
    rnd = random.Random(1621)
    ro, ri = 18.0, 12.0
    # SOLID trunk wall with a single real door opening (closed everywhere else)
    A.ring_wall(ri, ro, 0.0, 50.0, [(270.0, 9.0, [(0.0, 14.0)])], E['bark'])
    # merged flared root base: a continuous battered ring of fat roots, NO see-through gaps
    for k in range(24):
        a = 360.0 / 24 * k
        if abs(((a - 270 + 180) % 360) - 180) < 16:   # leave the doorway clear
            continue
        x, y, _ = polar(ro - 1.0, a)
        A.frustum((8.5, 8.5), (5.0, 5.0), rnd.uniform(13, 20), (x, y, 0.0), P['barkdk'] if k % 2 else P['barkmid'], (0, 0, a))
        xo, yo, _ = polar(ro + 3.0, a)                 # toe of the root on the ground
        A.beam((xo, yo, 0.4), (x, y, 11.0), 6.0, 5.0, P['barkdk'])
    A.cyl(ro + 4.5, 4.0, (0, 0, 0.0), P['barkdk'], verts=28, r2=ro + 0.5)   # solid plinth skirt closing the base
    # vertical bark ribs on the trunk body
    for k in range(18):
        a = 20.0 * k + rnd.uniform(-3, 3)
        if abs(((a - 270 + 180) % 360) - 180) < 16:
            continue
        x, y, _ = polar(ro + 0.1, a)
        A.chunk((2.4, 2.4, rnd.uniform(24, 40)), (x, y, rnd.uniform(16, 26)), P['barkmid'], (0, 0, a), 0.12, rnd, (0.7, 0.85))
    # clear recessed door: jambs + lintel ring the opening, deep dark void set well back
    x, y, _ = polar(ro, 270.0)
    for sg in (-1, 1):                                                                    # raised jambs either side of the opening
        A.box((1.6, 1.8, 15.0), (x + 0.4, y + sg * 4.6, 8.0), P['barkmid'], (0, 0, 270.0), bev=0.1)
    A.box((1.8, 11.5, 2.2), (x + 0.4, y, 15.0), P['barkmid'], (0, 0, 270.0), bev=0.1)     # lintel over the opening
    A.box((1.6, 11.5, 1.6), (x + 0.3, y, 16.6), P['barkdk'], (0, 0, 270.0), bev=0.08)     # arched hood
    A.box((4.0, 8.0, 13.5), (x - 2.2, y, 7.5), P['niche'], (0, 0, 270.0), bev=0)          # recessed void (set back, dark)
    A.box((4.0, 9.0, 1.0), (x - 1.0, y, 0.6), E['plank'], (0, 0, 270.0), bev=0.05)        # threshold step
    A.frustum((9.0, 2.0), (6.0, 1.4), 2.5, (x - 1.0, y - 2.0, 0.0), E['stone'])            # door stoop
    # inner floor + short spiral stair (visible through the door, reads inhabited)
    A.cyl(ri + 0.5, 0.8, (0, 0, 0.0), E['plank'], verts=20)
    for k in range(14):
        a = 250.0 + k * 11.0
        px, py, _ = polar(ri - 2.4, a)
        A.box((1.6, 3.4, 0.5), (px, py, 1.0 + k * 1.1), E['plank'], (0, 0, a + 90.0), bev=0.04)
    # CLOSED top: a solid bark cap + moss, no hollow rim
    A.cyl(ro + 0.5, 3.0, (0, 0, 47.0), P['barkdk'], verts=24, r2=ri - 1.0)
    A.cyl(ri + 2.0, 2.0, (0, 0, 49.5), E['moss'], verts=20, r2=2.0)
    return v5kit.fit(_fin(A, 'world_tree_trunk_door'), w=36.0, d=36.0, h=50.0)


# ================================================================== EV03 path pieces (04,05 MAJOR; 03,06 MINOR)
def _path04():
    """EV03_04 - continuous solid stepped deck seated on the ground, integrated moss (no floating planks)."""
    reset()
    A = Acc()
    rnd = random.Random(2704)
    # one solid ramped deck of merged steps, each resting on a solid riser to the ground
    for i in range(7):
        y = -9.0 + i * 3.0
        h = 0.5 + i * 0.42
        A.box((16.0, 3.2, h), (0, y, h / 2.0), P['deckwood'], bev=0.1)     # tread
        A.box((16.4, 3.4, 0.22), (0, y - 1.4, h + 0.08), P['barkmid'], bev=0)   # nosing lip
        A.box((16.0, 1.2, h + 0.45), (0, y + 1.5, (h + 0.45) / 2.0), P['barkdk'], bev=0.08)  # solid riser to next
    # side kerb logs running the whole length (seated on ground)
    for sg in (-1, 1):
        A.beam((sg * 8.0, -10.5, 0.0), (sg * 8.0, 11.0, 4.9), 1.4, 1.4, P['barkdk'])
    # integrated moss: low patches hugging the tread joints, not floating blobs
    for i in range(7):
        y = -9.0 + i * 3.0
        h = 0.6 + i * 0.5
        for sg in (-1, 1):
            A.ball(1.0, (sg * rnd.uniform(5.5, 7.0), y + rnd.uniform(-1, 1), h), E['moss'], segs=7, rings=4, scale=(1.6, 1.3, 0.35))
    return _fin(A, 'elf_path_piece')


def _path05():
    """EV03_05 - one connected walkable path surface, no floating gaps."""
    reset()
    A = Acc()
    rnd = random.Random(2705)
    # a single solid slab deck with a gentle crown, flagstone joints scored on top (not separate plates)
    A.box((16.0, 20.0, 1.4), (0, 0, 0.7), P['deckwood'], bev=0.1)
    A.box((14.0, 18.0, 0.4), (0, 0, 1.5), E['stone'], bev=0.06)            # paved top course, one piece
    for i in range(5):                                                    # scored joints (shallow dark grooves)
        A.box((14.2, 0.18, 0.1), (0, -7.2 + i * 3.6, 1.72), P['niche'], bev=0)
    for i in range(3):
        A.box((0.18, 18.2, 0.1), (-5.0 + i * 5.0, 0, 1.72), P['niche'], bev=0)
    for sg in (-1, 1):                                                    # kerb stones all along, resting on ground
        A.box((1.4, 20.0, 1.6), (sg * 7.8, 0, 0.8), E['stone'], bev=0.08)
    for k in range(6):                                                    # moss tufts in the kerb joints
        A.ball(0.8, (rnd.choice((-1, 1)) * 7.4, rnd.uniform(-9, 9), 1.4), E['moss'], segs=6, rings=4, scale=(1.4, 1.1, 0.4))
    return _fin(A, 'elf_path_piece')


def _path03():
    """EV03_03 - arched walkway with a SOLID filled underside, tiles on the ground."""
    reset()
    A = Acc()
    rnd = random.Random(2703)
    # solid arched ramp: fill the underside so there is no see-through gap
    n = 20
    for i in range(n):
        t = i / (n - 1.0)
        y = -8.0 + 16.0 * t
        z = 0.6 + math.sin(math.pi * t) * 2.2
        A.box((14.0, 16.0 / n + 0.3, z + 0.6), (0, y, (z + 0.6) / 2.0), E['plank'] if i % 2 else P['deckwood'], bev=0)   # deck + solid fill to ground
    A.box((14.4, 17.0, 0.8), (0, 0, 0.4), E['stone'], bev=0.06)   # ground footing slab (tiles flush)
    # scored plank joints across the deck (relief, not a bare ramp)
    for i in range(1, n):
        t = i / (n - 1.0)
        y = -8.0 + 16.0 * t
        z = 0.6 + math.sin(math.pi * t) * 2.2
        A.box((13.6, 0.16, 0.12), (0, y, z + 0.63), P['niche'], bev=0)
    for sg in (-1, 1):
        A.beam((sg * 7.0, -8.0, 0.6), (sg * 7.0, 8.0, 0.6), 0.8, 0.8, P['barkdk'])
        # carved handrail following the arch + balusters
        rpts = []
        for k in range(9):
            t = k / 8.0
            y = -8.0 + 16.0 * t
            z = 0.6 + math.sin(math.pi * t) * 2.2 + 2.6
            rpts.append((sg * 6.6, y, z))
        for p0, p1 in zip(rpts, rpts[1:]):
            A.beam(p0, p1, 0.4, 0.45, E['wood'])                                # top rail
        for k in range(9):                                                      # balusters down to the deck
            t = k / 8.0
            y = -8.0 + 16.0 * t
            zdeck = 0.6 + math.sin(math.pi * t) * 2.2 + 0.9
            ztop = 0.6 + math.sin(math.pi * t) * 2.2 + 2.5
            A.box((0.3, 0.3, ztop - zdeck), (sg * 6.6, y, (ztop + zdeck) / 2.0), E['wood'], bev=0)
        # carved newel posts at both ends with a leaf motif
        for yy in (-8.0, 8.0):
            A.box((0.9, 0.9, 4.2), (sg * 6.6, yy, 2.1), P['barkdk'], bev=0.1)
            A.ball(0.8, (sg * 6.6, yy, 4.4), E['leaf1'], segs=7, rings=5, scale=(1.1, 1.1, 0.8))
            A.ball(0.55, (sg * 6.6, yy, 4.9), E['leaf2'], segs=6, rings=4, scale=(1.0, 1.0, 0.8))
    for k in range(5):                                                          # moss tufts in the deck/kerb joints
        A.ball(0.6, (rnd.choice((-1, 1)) * 6.4, rnd.uniform(-7, 7), 1.2), E['moss'], segs=6, rings=4, scale=(1.4, 1.1, 0.4))
    return _fin(A, 'elf_path_piece')


def _path06():
    """EV03_06 - round planter ring with an even tree spacing and a raised lip."""
    reset()
    A = Acc()
    rnd = random.Random(2706)
    A.cyl(9.6, 0.7, (0, 0, 0), E['stone'], verts=32)                      # base pad
    A.sweep([(8.4, 0.7), (9.8, 0.7), (9.8, 2.2), (8.4, 2.2)], 0, 360, 36, E['stone'])   # raised lip
    A.cyl(8.2, 0.9, (0, 0, 0.7), E['moss'], verts=32)                    # soil bed
    for k in range(5):                                                   # evenly spaced small trees (light, under budget)
        a = 360.0 / 5 * k
        x, y, _ = polar(4.4, a)
        A.cyl(0.5, 5.0, (x, y, 1.6), E['wood'], verts=7, r2=0.35)
        A.ball(2.2, (x, y, 7.2), E['leaf1'] if k % 2 else E['leaf2'], segs=9, rings=6, scale=(1.0, 1.0, 0.95))
        A.ball(1.7, (x + 0.4, y, 8.6), E['leaf2'] if k % 2 else E['leaf1'], segs=8, rings=5, scale=(1.0, 1.0, 0.9))
    for k in range(10):                                                  # small flowers around the rim, evenly
        a = 36.0 * k
        x, y, _ = polar(6.6, a)
        A.ball(0.4, (x, y, 1.7), P['cloth_r'] if k % 2 else E['cream'], segs=5, rings=3)
    return _fin(A, 'elf_path_piece')


# ================================================================== EV01 houses 01/05 (MINOR)
def _house01():
    """EV01_01 - tower house, base rings cleanly stacked and ground planks flush."""
    reset()
    A = Acc()
    rnd = random.Random(2501)
    ORIG._hut  # reuse round-1 helpers
    A.cyl(8.0, 0.6, (0, 0, 0), E['stone'], verts=24, r2=8.6)             # flush ground pad (not offset)
    A.cyl(4.6, 8.0, (0, 0, 0.6), E['stone'], verts=14, r2=4.2)
    A.cyl(5.6, 0.7, (0, 0, 8.6), E['bark'], verts=14)
    ORIG._hut(A, rnd, 0, 0, 9.3, 4.4, 8.0, 3, True, 14)
    A.cyl(5.8, 0.7, (0, 0, 17.3), E['bark'], verts=14)
    ORIG._hut(A, rnd, 0, 0, 18.0, 3.5, 6.0, 2, False, 12, 1.1)
    # outside spiral stair, each tread seated on a cleanly aligned ring
    for k in range(20):
        a = 270.0 + k * 22.0
        x, y, _ = polar(5.2, a)
        A.box((2.4, 1.6, 0.4), (x, y, 1.2 + k * 0.74), E['plank'], (0, 0, a + 90.0), bev=0.04)
    ORIG._deck(A, rnd, 0, 0, 16.6, 6.4, 0.6, True, 18)
    # ground planks laid flush (flat on the pad, no gaps)
    for k in range(6):
        a = 300.0 + k * 20.0
        x, y, _ = polar(7.0, a)
        A.box((2.6, 1.4, 0.3), (x, y, 0.75), E['plank'], (0, 0, a + 90.0), bev=0)
    return _fin(A, 'elf_house_new')


def _house05():
    """EV01_05 - archery/pavilion type, but the interior behind the arch is CLOSED (no see-through gazebo gap)."""
    reset()
    A = Acc()
    rnd = random.Random(2505)
    A.cyl(10.0, 0.8, (0, 0, 0), E['plank'], verts=16)
    # closed back wall + side walls so the interior is not see-through
    A.cyl(9.0, 9.0, (0, 0, 0.8), E['wood'], verts=16, r2=8.6)            # solid drum body
    ORIG._rings(A, 9.0, 0.8, 9.0, 4, E['bark'], 0.45, 0.45, 16)
    # recessed front doorway (not an open hollow): frame + set-back door panel
    x, y, _ = polar(9.05, 270.0)
    A.box((0.8, 6.0, 7.0), (x, y, 4.3), E['bark'], (0, 0, 270.0), bev=0.06)       # frame
    A.box((0.5, 4.4, 5.6), (x - 0.5, y, 3.6), E['plank'], (0, 0, 270.0), bev=0.05)  # solid door panel (closed)
    A.box((0.5, 1.2, 5.0), (x - 0.4, y - 1.2, 3.6), E['dark'], bev=0)             # thin shadow gap only
    for i in range(2):                                                            # side round windows
        ORIG._roundwin(A, 210.0 + i * 120.0, 9.1, 5.0, 0.9, E['wood'], E['lantern'])
    ORIG._cone_roof(A, 0, 0, 9.8, 9.0, 6.5, 16, 1.6)
    xl, yl, _ = polar(9.2, 235.0)
    ORIG._lantern(A, xl, yl, 6.8, E['dark'], E['lantern'])
    return _fin(A, 'elf_house_new')


# ================================================================== EV02_03 canopy (OK-note: differ from 01)
def canopy_3():
    """EV02_03 - clearly distinct: a TWO-tier tall cluster (fewer, higher, bigger platforms) vs the 3-4 even spread of 01/02."""
    reset()
    A = Acc()
    rnd = random.Random(1603)
    A.cyl(3.6, 44.0, (0, 0, 0), E['bark'], verts=10, r2=2.4)
    for k in range(4):
        x, y, _ = polar(3.0, k * 90.0 + 20)
        A.beam((x * 2.4, y * 2.4, 0.0), (x * 0.6, y * 0.6, 8.0), 1.8, 1.8, E['wood'])
    # only TWO platforms, placed high and large, with a grand hut on the upper one
    spots = [(40.0, 24.0, 18.0, 9.0), (200.0, 28.0, 34.0, 10.5)]
    prev = None
    for a, dist, z, r in spots:
        x, y, _ = polar(dist, a)
        A.beam((0, 0, z - 2.0), (x, y, z - 0.6), 1.4, 1.4, E['wood'])
        ORIG._deck(A, rnd, x, y, z, r, 0.8, True, 20, a + 180.0)
        ORIG._hut(A, rnd, x, y, z + 0.8, r * 0.55, 5.2, 3, True, 14, 1.0)
        if prev is not None:
            px, py, pz, pr = prev
            L = math.hypot(x - px, y - py)
            d = ((x - px) / L, (y - py) / L)
            ang = math.degrees(math.atan2(d[1], d[0]))
            steps = int((L - pr - r) / 1.0)
            for s in range(steps):
                t = (s + 0.5) / steps
                bx = px + d[0] * pr + d[0] * (L - pr - r) * t
                by = py + d[1] * pr + d[1] * (L - pr - r) * t
                bz = pz + 0.8 + (z - pz) * t - 1.4 * 4 * t * (1 - t)
                A.box((0.8, 2.2, 0.2), (bx, by, bz), E['plank'], (0, 0, ang), bev=0)
        prev = (x, y, z, r)
    a0, d0, z0_, r0 = spots[0]
    xl, yl, _ = polar(d0 + r0 * 0.6, a0 + 180.0)
    ORIG._ladder(A, xl, yl, 0.0, z0_ + 0.6, E['wood'], a0)
    v4util.marker('mk_lb', (xl, yl, 0.4))
    v4util.marker('mk_lt', (xl, yl, z0_ + 0.9))
    return _fin(A, 'canopy_cluster')


# ================================================================== TW01 statue (MINOR: robe folds + thicker staff)
def statue():
    reset()
    A = Acc()
    for k in range(3):
        A.box((14.0 - k * 2.4, 14.0 - k * 2.4, 1.6), (0, 0, 0.8 + k * 1.6), T1['dstone'], bev=0.12)
    A.box((8.0, 8.0, 3.2), (0, 0, 6.4), T1['stone'], bev=0.12)
    A.box((8.8, 8.8, 0.7), (0, 0, 8.2), T1['dstone'], bev=0.08)
    z0 = 8.55
    for sx in (-1.4, 1.4):
        A.frustum((2.6, 2.8), (2.2, 2.4), 8.0, (sx, 0, z0), T1['stone'])
        A.box((2.8, 4.0, 1.0), (sx, -0.7, z0 + 0.5), T1['dstone'], bev=0.1)
    A.frustum((7.2, 4.6), (5.2, 3.6), 12.0, (0, 0, z0 + 7.0), T1['bone'])
    # carved robe folds: vertical pleats down the robe front
    for sx in range(-3, 4):
        A.box((0.5, 0.4, 11.0), (sx * 0.85, -2.1 + 0.0, z0 + 13.0), T1['stone'], bev=0)
    A.box((5.6, 3.8, 0.7), (0, 0, z0 + 12.8), T1['dstone'], bev=0.08)
    A.frustum((5.8, 3.6), (7.4, 3.0), 4.4, (0, 0.1, z0 + 12.9), T1['bone'])
    for sx in range(-3, 4):                                                     # pleats on the chest
        A.box((0.4, 0.35, 3.8), (sx * 0.85, -1.6, z0 + 15.0), T1['stone'], bev=0)
    A.box((8.0, 0.8, 11.0), (0, 2.8, z0 + 11.0), T1['dstone'], (-8, 0, 0), bev=0.1)
    for sg in (-1, 1):
        A.beam((sg * 3.8, 0, z0 + 16.0), (sg * 4.4, -1.8, z0 + 12.2), 1.3, 1.3, T1['bone'])
    A.beam((4.4, -1.8, z0 + 12.2), (4.6, -2.4, z0 + 11.6), 1.5, 1.5, T1['stone'])
    # THICKER staff (was thin): wrapped shaft + finial
    A.cyl(0.75, 28.0, (4.6, -2.4, z0 - 0.4), T1['wood'], verts=10)
    for k in range(5):
        A.sweep([(0.78, -0.2), (1.0, -0.2), (1.0, 0.2), (0.78, 0.2)], 0, 360, 8, T1['brass'], loc=(4.6, -2.4, z0 + 2.0 + k * 5.0))
    A.ball(1.3, (4.6, -2.4, z0 + 28.0), T1['brass'], segs=8, rings=5)
    A.box((2.4, 2.4, 0.4), (4.6, -2.4, z0 + 26.4), T1['brass'], (0, 0, 45), bev=0)
    zh = z0 + 18.4
    A.cyl(0.9, 1.2, (0, 0, zh - 1.0), T1['stone'], verts=10)
    A.ball(2.3, (0, -0.1, zh + 1.4), T1['bone'], segs=14, rings=10, scale=(0.92, 1.0, 1.12))
    A.box((3.6, 0.5, 0.55), (0, -2.2, zh + 2.1), T1['stone'], bev=0.04)
    A.box((0.7, 1.2, 1.7), (0, -2.45, zh + 1.2), T1['bone'], (-14, 0, 0), bev=0.04)
    for sx in (-0.95, 0.95):
        A.ball(0.42, (sx, -2.15, zh + 1.85), T1['dark'], segs=8, rings=5, scale=(1.2, 0.6, 0.8))
        A.box((1.0, 0.25, 0.18), (sx, -2.28, zh + 2.35), T1['stone'], (0, 0, sx * -6), bev=0)
    A.box((1.5, 0.35, 0.25), (0, -2.2, zh + 0.15), T1['dark'], bev=0)
    A.ball(0.7, (0, -1.9, zh - 0.65), T1['bone'], segs=8, rings=5, scale=(1.0, 0.9, 0.7))
    for sx in (-2.15, 2.15):
        A.ball(0.45, (sx, 0, zh + 1.2), T1['bone'], segs=6, rings=4, scale=(0.5, 0.7, 1.0))
    A.frustum((5.6, 5.2), (4.6, 4.4), 2.6, (0, 0.2, zh + 2.4), T1['dstone'])
    A.box((5.2, 0.5, 1.4), (0, 2.4, zh + 1.0), T1['dstone'], bev=0.05)
    return _fin(A, 'town1_hero_statue')


# ================================================================== TW02_06 street prop (MINOR: clarify + ground it)
def street_06():
    """TW02_06 - a village WELL (clear silhouette): round stone kerb, timber frame, roof, bucket on a rope. All grounded."""
    reset()
    A = Acc()
    rnd = random.Random(2806)
    A.cyl(3.2, 2.6, (0, 0, 0), T1['stone'], verts=16, r2=3.0)             # stone well kerb (grounded)
    A.sweep([(2.8, 2.6), (3.4, 2.6), (3.4, 3.1), (2.8, 3.1)], 0, 360, 16, T1['dstone'], loc=(0, 0, 0))
    A.cyl(2.6, 0.4, (0, 0, 2.2), T1['dark'], verts=16)                   # dark water surface recessed
    for sg in (-1, 1):                                                   # two timber uprights seated on the kerb
        A.box((0.8, 0.8, 7.0), (sg * 2.6, 0, 6.0), T1['wood'], bev=0.06)
    A.beam((-2.6, 0, 9.4), (2.6, 0, 9.4), 0.6, 0.6, T1['wood'])          # cross beam
    A.cyl(0.4, 5.6, (0, 0, 9.4), T1['wood'], verts=8, rot=(0, 90, 0))    # winch barrel
    A.beam((2.2, 0, 9.4), (3.2, 0.8, 9.4), 0.25, 0.25, T1['iron'])       # crank handle
    A.gable(7.0, 6.0, 2.6, (0, 0, 9.8), T1['plank'], (0, 0, 90))         # little roof
    G.roof_lines(A, 7.0, 6.0, 2.6, (0, 0, 9.8), T1['dstone'], 4)
    # bucket hanging on a rope from the barrel (grounded by the rope line, reads clearly)
    A.beam((0, 0, 9.2), (0, 0, 5.2), 0.1, 0.1, T1['rope'])
    A.cyl(0.9, 1.4, (0, 0, 3.8), T1['wood'], verts=10, r2=0.8)
    A.sweep([(0.72, -0.1), (0.95, -0.1), (0.95, 0.1), (0.72, 0.1)], 0, 360, 10, T1['iron'], loc=(0, 0, 4.4))
    return _fin(A, 'town1_street_life')


# ================================================================== TW03 avenue 01 (MINOR), 04 (OK-note differ from 03)
def _avenue01():
    """TW03_01 - skull-avenue brazier: tripod with a SKULL-motif bowl and thicker legs (ties to the avenue set)."""
    reset()
    A = Acc()
    rnd = random.Random(2901)
    A.cyl(3.4, 1.0, (0, 0, 0), T1['dstone'], verts=12)
    for k in range(3):                                                   # thick splayed legs
        a = k * 120.0
        x, y, _ = polar(2.6, a)
        A.box((1.2, 1.2, 7.4), (x * 0.6, y * 0.6, 3.6), T1['iron'], (0, 10, a), bev=0.1)
        A.box((2.0, 2.0, 1.0), (x, y, 0.6), T1['dstone'], bev=0.1)       # foot pad
    A.cyl(2.4, 1.8, (0, 0, 6.6), T1['iron'], verts=14, r2=3.6)           # bowl
    A.cyl(3.0, 0.3, (0, 0, 8.2), T1['coal'], verts=14)
    for k in range(7):
        x, y, _ = polar(1.6, k * 51.4)
        A.chunk((1.0, 1.0, 0.8), (x, y, 8.5), T1['coal'], jit=0.2, rnd=rnd)
    # skull motif on the front of the bowl (bone-white mini skull, matte)
    A.ball(1.1, (0, -3.4, 6.8), T1['bone'], segs=10, rings=7, scale=(1.0, 0.8, 1.0))
    for sx in (-0.4, 0.4):
        A.ball(0.3, (sx, -4.0, 7.0), T1['dark'], segs=6, rings=4, scale=(1.0, 0.6, 0.9))
    for k in range(4):
        A.box((0.25, 0.3, 0.5), (-0.4 + k * 0.27, -4.0, 6.0), T1['bone'], bev=0)
    return _fin(A, 'skull_avenue_set')


def _avenue04():
    """TW03_04 (round 3, lead) - banner standard with a swallowtail banner: the banner is ONE flat cloth shape (a prism), with a plain bone diamond on it. No letters, no
    stray angled slabs; thicker pole and braces. 14 x 14 x 14 footprint."""
    reset()
    A = Acc()
    A.cyl(2.8, 1.2, (0, 0, 0), T1['dstone'], verts=10)
    A.cyl(0.8, 20.0, (0, 0, 1.0), T1['wood'], verts=8, r2=0.6)
    A.ball(1.0, (0, 0, 21.2), T1['bone'], segs=10, rings=7, scale=(1.0, 0.85, 1.0))
    for sx in (-0.35, 0.35):
        A.ball(0.28, (sx, -0.7, 21.3), T1['dark'], segs=6, rings=4, scale=(1.0, 0.6, 0.9))
    A.beam((0, 0, 18.6), (5.6, 0, 18.6), 0.45, 0.45, T1['iron'])
    A.prism([(-2.1, 8.6), (2.1, 8.6), (2.1, 0.0), (0.0, 2.8), (-2.1, 0.0)], 0.45, (5.0, 0, 9.8), T1['green'], (90, 0, 90))
    A.prism([(0.0, 1.1), (0.9, 0.0), (0.0, -1.1), (-0.9, 0.0)], 0.12, (5.4, 0, 14.6), T1['bone'], (90, 0, 90))
    A.box((0.6, 4.6, 0.6), (5.0, 0, 18.5), T1['dstone'], bev=0.05)
    for sg in (-1, 1):
        A.beam((0, 0, 3.0), (sg * 3.2, 0, 1.0), 0.5, 0.5, T1['iron'])
    return _fin(A, 'skull_avenue_set')


PV = G.reg('ve_f', {
    'iron_m': ((92, 88, 86), 'Metal', 0.3, 0.72),
    'bronze': ((128, 96, 62), 'Metal', 0.3, 0.72),
    'coal2': ((76, 52, 42), 'Slate', 0.0, 0.95),
    'ash': ((128, 120, 110), 'Slate', 0.0, 0.95),
    'sack': ((190, 168, 124), 'Fabric', 0.0, 1.0),
})


def _path01():
    """EV03_01 (round 3, lead) - root-and-stone stair piece, 20 W x 6 H x 20 D: nine SOLID steps on the ground (closed underside), light wooden step edges proud of the treads,
    a solid back mass, root rails that touch the step sides, moss on the lower steps."""
    reset()
    A = Acc()
    rnd = random.Random(7001)
    n = 9
    for i in range(n):
        w = 17.5 - i * 0.55
        y = -9.0 + i * 2.1
        h = 0.62 * (i + 1)
        A.box((w, 2.3, h), (0, y, h / 2.0), E['stone'] if i % 2 else P['barkmid'], bev=0.08)
        A.box((w + 0.3, 2.6, 0.35), (0, y - 0.15, h - 0.175 + 0.07), E['plank'], bev=0.05)
    A.box((13.0, 3.0, 0.62 * n), (0, -9.0 + n * 2.1 + 0.5, 0.62 * n / 2.0), P['barkdk'], bev=0.1)
    for sg in (-1, 1):
        A.beam((sg * 9.0, -9.5, 0.9), (sg * 5.9, 9.5, 6.0), 1.4, 1.1, P['barkdk'])
        A.cyl(0.9, 1.6, (sg * 9.0, -9.5, 0.0), P['barkdk'], verts=8)
    for k in range(6):
        i = k
        A.ball(rnd.uniform(0.9, 1.5), (rnd.uniform(-6.5, 6.5), -9.0 + i * 2.1, 0.62 * (i + 1) + 0.05), P['moss'], segs=6, rings=4, scale=(1.5, 1.2, 0.4))
    return _fin(A, 'elf_path_piece')


def _stall():
    """TW02_03 (round 3, lead) - market stall, 12 W x 10 H x 10 D: four posts, a striped cloth awning, a counter with stacked crates, a barrel and two sacks beside it.
    Reads as street life from every side; everything is grounded."""
    reset()
    A = Acc()
    rnd = random.Random(7203)
    for sx in (-5.0, 5.0):
        for sy in (-3.5, 3.5):
            A.box((0.7, 0.7, 8.0), (sx, sy, 4.0), T1['wood'], bev=0.06)
    for k in range(6):
        x = -5.0 + k * 2.0 + 1.0
        A.box((1.96, 8.6, 0.5), (x, 0.0, 8.0 + (k % 1) * 0.0), T1['cloth'] if k % 2 else T1['cream'], (8, 0, 0), bev=0.02)
    A.box((11.0, 0.5, 1.6), (0, -4.1, 8.0 - 0.6), T1['cloth'], bev=0.04)
    A.box((9.0, 3.0, 3.0), (0, 0.2, 1.5), T1['plank'], bev=0.08)
    A.box((9.4, 3.4, 0.4), (0, 0.2, 3.2), T1['wood'], bev=0.05)
    for (x, z, s) in ((-2.6, 3.4, 1.8), (-0.4, 3.4, 1.8), (-1.5, 5.2, 1.6)):
        A.box((s, s, s), (x, 0.2, z + s / 2.0), T1['plank'], (0, 0, rnd.uniform(-8, 8)), bev=0.08)
        A.box((s + 0.08, 0.2, s + 0.08), (x, 0.2 - s / 2.0 - 0.02, z + s / 2.0), T1['wood'], bev=0)
    A.ball(0.9, (2.4, 0.2, 4.0), T1['green'], segs=8, rings=5)
    A.ball(0.8, (3.4, 0.0, 3.9), T1['cloth'], segs=8, rings=5)
    A.cyl(1.2, 2.8, (4.2, -3.4, 0.0), T1['plank'], verts=12, r2=1.2)
    A.cyl(1.3, 0.3, (4.2, -3.4, 1.0), T1['iron'], verts=12)
    for sx, sy in ((-4.2, -3.2), (-3.0, -3.6)):
        A.ball(1.3, (sx, sy, 1.0), PV['sack'], segs=8, rings=5, scale=(1.0, 0.9, 0.85))
    A.box((3.0, 0.3, 1.2), (0, -4.3, 6.4), T1['plank'], bev=0.04)
    A.box((2.6, 0.1, 0.8), (0, -4.5, 6.4), T1['cream'], bev=0)
    return _fin(A, 'town1_street_life')


def _sign_smith():
    """TW02_07 (round 3, lead) - smith's hanging sign, 12 W x 10 H x 10 D: stone footing, wooden post, bracket arm with a brace, a warm plank board on two chains with a
    cream plaque and a dark iron anvil emblem. Light and warm, only the small emblem is dark."""
    reset()
    A = Acc()
    A.box((4.0, 4.0, 1.2), (0, 0, 0.6), T1['stone'], bev=0.1)
    A.box((2.6, 2.6, 0.5), (0, 0, 1.4), T1['dstone'], bev=0.06)
    A.box((0.9, 0.9, 9.0), (0, 0, 1.2 + 4.5), T1['wood'], bev=0.08)
    A.beam((0.0, 0, 9.2), (6.0, 0, 9.2), 0.6, 0.6, T1['wood'])
    A.beam((0.2, 0, 6.2), (3.0, 0, 9.0), 0.4, 0.4, T1['wood'])
    for sx in (4.4, 5.8):
        A.box((0.12, 0.12, 1.4), (sx, 0, 8.4), T1['iron'], bev=0)
    A.box((3.4, 0.5, 3.2), (5.1, 0, 6.4), T1['plank'], bev=0.06)
    A.box((2.9, 0.12, 2.7), (5.1, -0.3, 6.4), T1['cream'], bev=0)
    A.box((2.0, 0.3, 0.7), (5.1, -0.46, 6.9), PV['iron_m'], bev=0.04)
    A.box((0.8, 0.3, 0.9), (5.1, -0.46, 6.3), PV['iron_m'], bev=0.04)
    A.box((1.7, 0.3, 0.5), (5.1, -0.46, 5.7), PV['iron_m'], bev=0.04)
    return _fin(A, 'town1_street_life')


def _brazier2():
    """TW03_02 (round 3, lead) - skull-avenue pedestal brazier, 14 x 14 x 14: stone pedestal, a dull iron bowl (not near-black), a dull bronze rim (no gold), and the bowl
    FILLED with a heap of dark coals and ash that rises above the rim, so it never reads as an empty hole. No glow."""
    reset()
    A = Acc()
    rnd = random.Random(7302)
    A.cyl(3.2, 0.8, (0, 0, 0), T1['dstone'], verts=12)
    A.cyl(1.4, 5.0, (0, 0, 0.8), T1['stone'], verts=8, r2=1.0)
    A.cyl(1.9, 0.6, (0, 0, 5.8), T1['dstone'], verts=8)
    A.cyl(3.6, 2.2, (0, 0, 6.4), PV['iron_m'], verts=16, r2=4.2)
    A.sweep([(3.9, 0.0), (4.7, 0.0), (4.7, 0.55), (3.9, 0.55)], 0, 360, 16, PV['bronze'], loc=(0, 0, 8.3))
    A.cyl(4.0, 0.9, (0, 0, 8.2), PV['ash'], verts=16)
    for k in range(16):
        r = rnd.uniform(0.0, 3.2)
        x, y, _ = polar(r, rnd.uniform(0, 360))
        A.chunk((rnd.uniform(1.2, 1.9), rnd.uniform(1.2, 1.9), rnd.uniform(1.0, 1.6)), (x, y, 9.2 + (1.0 - r / 3.4) * 0.9), PV['coal2'] if k % 3 else PV['ash'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(4):
        x, y, _ = polar(4.3, k * 90.0 + 45)
        A.ball(0.5, (x, y, 8.3), PV['bronze'], segs=6, rings=4)
    return _fin(A, 'skull_avenue_set')


def _canopy_post(seed, n):
    def post(A):
        rnd = random.Random(seed)
        spots = []
        for k in range(n):
            a = 360.0 * k / n + rnd.uniform(-20, 20)
            dist = rnd.uniform(22.0, 29.0)
            z = 10.0 + k * (22.0 / max(1, n - 1)) + rnd.uniform(-1, 1)
            r = rnd.uniform(6.5, 8.5)
            spots.append((a, dist, z, r))
        for (a0, d0, z0, r0), (a1, d1, z1, r1) in zip(spots, spots[1:]):
            x0, y0, _ = polar(d0, a0)
            x1, y1, _ = polar(d1, a1)
            L = math.hypot(x1 - x0, y1 - y0)
            ux, uy = (x1 - x0) / L, (y1 - y0) / L
            ang = math.degrees(math.atan2(uy, ux))
            Lw = L - r0 - r1
            steps = max(3, int(Lw / 1.3))
            for s in range(steps + 1):
                t = s / float(steps)
                px = x0 + ux * (r0 + Lw * t)
                py = y0 + uy * (r0 + Lw * t)
                pz = z0 + 0.8 + (z1 - z0) * t - 1.2 * 4 * t * (1 - t)
                A.box((1.5, 3.0, 0.5), (px, py, pz - 0.4), E['wood'], (0, 0, ang), bev=0.05)
                if s % 2 == 0:
                    for sg in (-1, 1):
                        A.box((0.3, 0.3, 2.0), (px - uy * sg * 1.35, py + ux * sg * 1.35, pz + 0.6), E['wood'], bev=0)
            for sg in (-1, 1):
                prev = None
                for s in range(steps + 1):
                    t = s / float(steps)
                    q = (x0 + ux * (r0 + Lw * t) - uy * sg * 1.35, y0 + uy * (r0 + Lw * t) + ux * sg * 1.35, z0 + 0.8 + (z1 - z0) * t - 1.2 * 4 * t * (1 - t) + 1.6)
                    if prev:
                        A.beam(prev, q, 0.32, 0.3, E['wood'])
                    prev = q
    return post


def _carved_post(A):
    for x in (-4.0, 0.0, 4.0):
        A.box((1.0, 0.7, 4.0), (x, 8.45, 2.2), E['bark'], bev=0.04)
    A.box((12.4, 0.5, 0.8), (0, 8.35, 0.4), E['wood'], bev=0.04)
    A.box((12.8, 1.0, 0.4), (0, 8.2, 4.55), E['wood'], bev=0.04)


def _roots_post(A):
    r_ = random.Random(612)
    A.cyl(56.0, 26.0, (0, 0, 3.0), E['bark'], verts=32, r2=38.0)
    A.ball(38.0, (0, 0, 28.0), E['bark'], segs=24, rings=10, scale=(1.0, 1.0, 0.22))
    for k in range(14):
        a = 360.0 / 14 * k
        x, y, _ = polar(47.0, a)
        A.chunk((7.0, 7.0, r_.uniform(16.0, 22.0)), (x, y, r_.uniform(12.0, 16.0)), P['barkdk'] if k % 2 else P['barkmid'], (0, 0, a), 0.1, r_, (0.55, 0.7))
    for k in range(8):
        x, y, _ = polar(r_.uniform(8.0, 34.0), r_.uniform(0, 360))
        A.ball(r_.uniform(3.0, 5.0), (x, y, 29.0), E['moss'], segs=7, rings=4, scale=(1.4, 1.3, 0.5))


def _statue_post(A):
    z0 = 8.55
    A.box((6.6, 4.4, 0.5), (0, 0, z0 + 10.5), T1['brass'], bev=0.05)
    A.cyl(0.9, 0.3, (0, -2.45, z0 + 14.4), T1['brass'], verts=12, rot=(90, 0, 0))
    for sg in (-1, 1):
        A.box((2.4, 3.4, 0.8), (sg * 3.7, 0, z0 + 16.4), T1['dstone'], bev=0.08)
    A.box((7.6, 4.8, 0.5), (0, 0, z0 + 7.2), T1['dstone'], bev=0.05)


def _cart_post(A):
    for (x, y, z) in ((-2.4, 0.5, 3.9), (-0.6, -0.7, 3.9), (1.4, 0.4, 3.9)):
        A.ball(1.25, (x, y, z), PV['sack'], segs=8, rings=5, scale=(1.0, 0.95, 0.85))
    A.cyl(1.0, 2.2, (2.6, -0.6, 2.9), T1['plank'], verts=10, r2=1.0)
    A.box((1.8, 1.8, 1.6), (-0.4, 0.1, 3.7), T1['plank'], (0, 0, 14), bev=0.06)


def _crates2_post(A):
    for k in range(3):
        A.ball(1.0, (4.2 + k * 0.6, 2.0 - k * 1.0, 1.0), T1['cream'], segs=10, rings=6, scale=(1.0, 1.0, 1.1))


def _banner_post(A):
    for j in range(4):
        A.box((0.3, 1.0, 9.0), (5.4 + (0.25 if j % 2 else -0.25), -1.5 + j * 1.0, 14.0), T1['cloth'], bev=0.02)
    for sy in (-1.6, 0.0, 1.6):
        A.box((0.3, 0.3, 0.7), (5.4, sy, 18.8), T1['rope'], bev=0)


def ev02_01():
    return LK.wrap(lambda: ORIG._canopy(601, 3), post=_canopy_post(601, 3))()


def ev02_02():
    return LK.wrap(lambda: ORIG._canopy(602, 4), post=_canopy_post(602, 4), recolor=[LK.ramp([E['shingle']], [E['red']])])()


def ev03_02():
    return LK.wrap(lambda: ORIG._path('carved'), post=_carved_post)()


def ev03_05():
    return LK.wrap(_path05, recolor=[LK.ramp([P['niche']], [E['bark']]), LK.ramp([P['deckwood']], [P['barkdk'], P['barkmid']], trange=(0.0, 1.5))])()


def rw02_01():
    return LK.wrap(ORIG.tree_roots, post=_roots_post)()


def tw01_01():
    return LK.wrap(statue, post=_statue_post)()


def tw02_01():
    return LK.wrap(lambda: ORIG._street('handcart'), prune=[dict(keys=[T1['cream'], T1['green']], max_size=2.6)], post=_cart_post)()


def tw02_04():
    return LK.wrap(lambda: ORIG._street('crates2'), prune=[dict(keys=[T1['cream']], max_size=2.6)], post=_crates2_post)()


def tw03_01():
    return LK.wrap(_avenue01, recolor=[LK.ramp([T1['iron']], [PV['iron_m']]), LK.ramp([T1['coal']], [PV['coal2']]), LK.ramp([T1['dark']], [PV['iron_m']])])()


def tw03_03():
    return LK.wrap(lambda: ORIG._avenue('banner1'), prune=[dict(keys=[T1['cloth']], max_size=10.0, thin=0.3)], post=_banner_post)()


BATCHES = {
    'elf': ('v5_elf', mk([
        ('LM02_01_world_tree_falls', tree_falls), ('LM01_01_world_tree_trunk_door', trunk_door),
        ('EV03_03_elf_path_piece_03', _path03), ('EV03_04_elf_path_piece_04', _path04),
        ('EV03_05_elf_path_piece_05', _path05), ('EV03_06_elf_path_piece_06', _path06),
        ('EV01_01_elf_house_new_01', _house01), ('EV01_05_elf_house_new_05', _house05),
        ('EV02_03_canopy_cluster_03', canopy_3)], 0.1)),
    'town1': ('v5_town1', mk([
        ('TW01_01_town1_hero_statue', statue), ('TW02_06_street_life_06', street_06),
        ('TW03_01_skull_avenue_set_01', _avenue01), ('TW03_04_skull_avenue_set_04', _avenue04)], 0.1)),
}


# --- lead3 registration ---
BATCHES['lead3'] = ('v5_elf', mk([('EV03_01_elf_path_piece_01', _path01), ('LM02_01_world_tree_falls', tree_falls)], 0.1))
BATCHES['lead3_town'] = ('v5_town1', mk([('TW02_03_street_life_03', _stall), ('TW02_07_street_life_07', _sign_smith), ('TW03_02_skull_avenue_set_02', _brazier2), ('TW03_04_skull_avenue_set_04', _avenue04)], 0.1))


# --- lead4 registration ---
import v5_leadkit as LK
BATCHES['lead4_elf'] = ('v5_elf', mk([('EV02_01_canopy_cluster_01', ev02_01), ('EV02_02_canopy_cluster_02', ev02_02), ('EV03_02_elf_path_piece_02', ev03_02),
                                      ('EV03_05_elf_path_piece_05', ev03_05), ('RW02_01_rework_world_tree_roots', rw02_01)], 0.1))
BATCHES['lead4_town'] = ('v5_town1', mk([('TW01_01_town1_hero_statue', tw01_01), ('TW02_01_street_life_01', tw02_01), ('TW02_04_street_life_04', tw02_04),
                                         ('TW03_01_skull_avenue_set_01', tw03_01), ('TW03_03_skull_avenue_set_03', tw03_03)], 0.1))
