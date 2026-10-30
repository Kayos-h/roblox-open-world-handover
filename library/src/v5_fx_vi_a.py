"""v5_fx_vi_a - fix round, builder A1 (worker vi, palette prefix vi_fa_).
Rebuilds 31 flawed models: plains farm/ruin pieces, crater rim rocks, arcane ruins, floating rocks, arena and aqueduct
ruins, ruin columns, tower stumps, ruined castle modules, sky islands. Original designs, no glow, front faces -Y,
pivot bottom-centre on z=0, 1 unit = 1 stud. Only NEW palette keys registered, prefix vi_fa_.
Root fixes vs round 1: warm graded rock instead of near-black basalt/dark faces; no loose green balls or cyan/white
water-panel slabs; round/battered towers with eroded relief instead of flat cream boxes; moss as settled patches not
painted rings; underside rock as one tapered root; thicker colonnade geometry; grounded rubble.
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v5kit
from v5kit import Acc, polar, tang, mk, ids, band, strata
import v5gen as G
from v5gen import round_tower, wall_seg, column
import v4util
import v5_vi as R           # read-only: reuse round-1 palette colours and markers

V = R.V                      # round-1 palette dict (reuse colours, never re-register its keys)

# ---- new warm rock / matte palette, prefix vi_fa_ (emission always 0) -----------------------------------
P = G.reg('vi_fa', {
    'r_base':  ((96, 86, 78),  'Slate',       0.0, 0.95),   # dark warm base course
    'r_low':   ((122, 110, 98), 'Slate',       0.0, 0.95),
    'r_mid':   ((150, 136, 118), 'Cobblestone', 0.0, 0.94),
    'r_hi':    ((176, 162, 142), 'Limestone',   0.0, 0.92),  # sun-bleached top
    'r_warm':  ((162, 140, 112), 'Sandstone',   0.0, 0.93),  # warm ledge accent
    's_base':  ((132, 126, 116), 'Limestone',   0.0, 0.92),  # cut-stone dark course
    's_mid':   ((176, 168, 154), 'Limestone',   0.0, 0.90),
    's_hi':    ((206, 198, 182), 'Limestone',   0.0, 0.88),  # weathered cream stone
    's_warm':  ((190, 172, 144), 'Sandstone',   0.0, 0.90),
    'void':    ((54, 50, 48),   'Slate',        0.0, 0.98),  # recessed opening (never a flat outside face)
    'moss':    ((104, 120, 78),  'Grass',       0.0, 1.0),   # muted, patch only
    'dirt':    ((120, 100, 76),  'Ground',      0.0, 1.0),
    'grass':   ((108, 146, 80),  'Grass',       0.0, 1.0),
    'water':   ((150, 176, 182), 'SmoothPlastic', 0.0, 0.6), # pale matte, stepped, never a glow slab
    'foam':    ((214, 220, 214), 'SmoothPlastic', 0.0, 0.7),
    # round-2: wider tonal spread so rock/stone masses are not one flat tan
    'r_dk':    ((72, 66, 62),   'Basalt',       0.0, 0.95),   # deep shadow rock
    'r_cool':  ((118, 120, 120), 'Slate',       0.0, 0.94),   # cool grey band
    'r_rust':  ((150, 118, 88),  'Sandstone',   0.0, 0.93),   # rusty warm band
    's_dk':    ((104, 100, 92),  'Slate',        0.0, 0.93),   # dark stone course
    's_cool':  ((150, 150, 148), 'Granite',      0.0, 0.9),    # cool grey stone
    'lichen':  ((150, 158, 120), 'Grass',        0.0, 1.0),    # pale lichen patch
    'straw':   ((196, 170, 104), 'Fabric',       0.0, 1.0),    # natural straw (muted, not bright yellow)
    'straw2':  ((170, 144, 86),  'Fabric',       0.0, 1.0),    # shaded straw strands
})
ROCK = [P['r_dk'], P['r_base'], P['r_low'], P['r_rust'], P['r_mid'], P['r_hi']]   # bottom -> top, wide spread
ROCKW = [P['r_dk'], P['r_low'], P['r_rust'], P['r_warm'], P['r_hi']]
ROCKC = [P['r_dk'], P['r_cool'], P['r_low'], P['r_mid'], P['r_hi']]               # cooler variant for sibling variety
STON = [P['s_dk'], P['s_base'], P['s_cool'], P['s_mid'], P['s_hi']]               # cut stone, wider spread


def _fin(A, name):
    A.to_scene()
    return finalize(name, 28)


def _ground_rubble(A, rnd, n, rx, ry, keys, smin=1.2, smax=3.6):
    """Fallen rubble that rests ON the ground (z so the chunk bottom touches 0)."""
    for k in range(n):
        s = rnd.uniform(smin, smax)
        h = rnd.uniform(0.7, s * 0.8)
        A.chunk((s, s * rnd.uniform(0.8, 1.2), h), (rnd.uniform(-rx, rx), rnd.uniform(-ry, ry), h / 2.0 - 0.4),
                band(keys, rnd.uniform(0, 0.4), rnd), (0, 0, rnd.uniform(0, 90)), 0.2, rnd)


def _moss_patch(A, rnd, x, y, z, s=1.4):
    """A low settled moss clump (flat, hugging the surface), not a floating ball, ring or leaf."""
    A.chunk((s * 1.3, s * rnd.uniform(1.0, 1.3), s * 0.22), (x, y, z + s * 0.1), P['moss'], (0, 0, rnd.uniform(0, 90)), 0.14, rnd)


def _L(fn, row):
    return [(m, (lambda j=j, f=fn: f(j))) for j, m in enumerate(ids(row))]


# ================================================================ CRATER RIM ROCKS  LM19 (MAJOR 02/04/05, MINOR 01/03)
def _rim_rock(i):
    reset()
    A = Acc()
    rnd = random.Random(5200 + i)
    # one big graded mass + several medium masses, warm rock, colour by height (no basalt, no black faces)
    A.mound(0, 0, 54.0, 44.0, 36.0, 44, ROCKL, rnd, 0.0, 0.34, 0.74, 0.14)
    # a couple of bold tilted crag faces to break the pile, varied per sibling
    for k in range(3 + i % 2):
        a = (k * 70 + i * 40) % 360
        x, y, _ = polar(rnd.uniform(8, 18), a)
        A.chunk((rnd.uniform(10, 16), rnd.uniform(9, 14), rnd.uniform(14, 26)),
                (x * 0.5, y * 0.5, rnd.uniform(9, 16)),
                band(ROCKW, rnd.uniform(0.4, 0.95), rnd), (rnd.uniform(-8, 8), rnd.uniform(-8, 8), a),
                0.15, rnd, (rnd.uniform(0.55, 0.8), rnd.uniform(0.55, 0.8)))
    # a slender crag peak so the silhouette is not a dome
    px, py, _ = polar(rnd.uniform(3, 9), (i * 97) % 360)
    A.chunk((9.0, 8.0, 30.0 + i), (px, py, 24.0), P['r_hi'], (rnd.uniform(-6, 6), rnd.uniform(-6, 6), rnd.uniform(0, 90)), 0.16, rnd, (0.3, 0.3))
    # warm ledge shelves set INTO the mass (low radius, embedded so they rest on the body, not float off the side)
    for k in range(5):
        a = rnd.uniform(0, 360)
        rr = rnd.uniform(8, 15)
        x, y, _ = polar(rr, a)
        A.chunk((rnd.uniform(5, 9), rnd.uniform(4, 7), rnd.uniform(1.5, 3.5)), (x, y, rr * 0.55 + rnd.uniform(-2, 2)),
                P['r_warm'], (rnd.uniform(-10, 10), 0, a), 0.2, rnd)
    _ground_rubble(A, rnd, 13, 27.0, 20.0, ROCKL, 1.6, 4.2)
    for k in range(3):                                                  # a little moss low where it would settle
        x, y, _ = polar(rnd.uniform(12, 24), rnd.uniform(0, 360))
        _moss_patch(A, rnd, x, y, rnd.uniform(0.5, 3.5), rnd.uniform(1.6, 2.8))
    return _fin(A, 'rim_rock')


# ================================================================ CRATER ARCANE RUIN  LM20_02 (MINOR)
def _magic_ruin(i):
    """LM20_02 (round 3, lead) - arcane ruin, 40 x 40 x 40, built at full size (the old pillars were 24 high and got stretched to 40, which made them look thin):
    a broken dais, two tall rune pillars at the back with a fallen lintel in front, six standing stones with two trilithon lintels, a central stepped rune altar with an obelisk shard,
    a rune inlay ring, rubble that rests ON the dais."""
    reset()
    A = Acc()
    rnd = random.Random(5300 + i)
    A.cyl(19.4, 1.6, (0, 0, 0), P['s_base'], verts=24, r2=18.4)
    A.cyl(16.0, 0.8, (0, 0, 1.6), P['s_mid'], verts=24, r2=15.0)
    zt = 2.4
    for sx in (-1, 1):
        A.chunk((5.0, 5.0, 35.0), (sx * 11.0, 9.0, zt + 17.5), band(STON, 0.5, rnd), (0, 0, 0), 0.04, rnd, (0.85, 0.85))
        A.box((6.4, 6.4, 1.4), (sx * 11.0, 9.0, zt + 0.7), P['s_warm'], bev=0.1)
        for z in (9.0, 16.0, 23.0, 30.0):
            A.box((4.8, 0.7, 1.5), (sx * 11.0, 9.0 - 2.6, z), V['rune'], bev=0)
    A.chunk((26.0, 4.6, 4.2), (-3.0, -9.0, zt + 2.1), band(STON, 0.6, rnd), (0, 0, 12), 0.06, rnd)
    pair_h = (11.0, 11.0, 9.0, 7.0, 12.0, 12.0)
    angs = (190.0, 226.0, 262.0, 298.0, 334.0, 10.0)
    pts = []
    for k, (a, hh) in enumerate(zip(angs, pair_h)):
        x, y, _ = polar(13.0, a)
        pts.append((x, y, hh))
        A.chunk((3.4, 2.8, hh), (x, y, zt + hh / 2.0), band(STON, 0.35 + 0.1 * (k % 3), rnd), (0, 0, a + 90.0), 0.06, rnd, (0.9, 0.9))
        A.box((4.0, 3.4, 0.6), (x, y, zt + 0.3), P['s_warm'], (0, 0, a + 90.0), bev=0.06)
        A.box((3.0, 0.5, 1.2), (x + math.cos(math.radians(a + 270.0)) * 1.55, y + math.sin(math.radians(a + 270.0)) * 1.55, zt + hh * 0.55), V['rune'], (0, 0, a + 90.0), bev=0)
    for (p, q) in ((pts[0], pts[1]), (pts[4], pts[5])):
        mx, my = (p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0
        ln = math.hypot(q[0] - p[0], q[1] - p[1]) + 3.0
        ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
        A.chunk((ln, 2.8, 1.8), (mx, my, zt + p[2] + 0.8), band(STON, 0.8, rnd), (0, 0, ang), 0.05, rnd)
    A.cyl(4.8, 0.8, (0, -1.0, zt), P['s_base'], verts=16, r2=4.4)
    A.cyl(3.5, 0.8, (0, -1.0, zt + 0.8), P['s_mid'], verts=16, r2=3.2)
    A.box((3.4, 3.4, 2.2), (0, -1.0, zt + 1.6 + 1.1), band(STON, 0.55, rnd), bev=0.1)
    A.box((3.6, 0.5, 0.7), (0, -1.0 - 1.72, zt + 3.0), V['rune'], bev=0)
    A.chunk((2.4, 2.4, 6.0), (2.2, -3.0, zt + 1.6 + 3.0), band(STON, 0.8, rnd), (0, 0, 20), 0.08, rnd, (0.45, 0.45))
    for k in range(10):
        a = k * 36.0
        x, y, _ = polar(9.0, a)
        A.box((1.6, 0.6, 0.3), (x, y, zt + 0.05), V['rune'], (0, 0, a + 90), bev=0)
    for k in range(11):
        s = rnd.uniform(2, 3.8)
        hh = rnd.uniform(1.2, 2.6)
        x, y, _ = polar(rnd.uniform(5, 16.5), rnd.uniform(0, 360))
        A.chunk((s, s, hh), (x, y, zt + hh / 2.0 - 0.2), band(STON, rnd.uniform(0, 0.5), rnd), (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(3):
        _moss_patch(A, rnd, rnd.uniform(-12, 12), rnd.uniform(-14, 4), 2.4, rnd.uniform(1.4, 2.4))
    return _fin(A, 'magic_ruin')


# ================================================================ FLOATING ROCK  LM21_02 / LM21_04 (MINOR)
def _float_rock(i):
    """LM21 floating rocks (round 3, lead) - built at the manifest size (40 x 30 x 40) so nothing is stretched: a SOLID root of stacked banded frustum slices (two sets turned 45 degrees,
    so the root is eight-sided with no gaps and no wafers), faceted bosses that sit in the root, a soil rim and a grass cap with moss."""
    reset()
    A = Acc()
    rnd = random.Random(5400 + i)
    topw, topd = (38.0, 36.0) if i == 0 else (34.0, 38.0)
    ramp = ROCKC if i == 0 else ROCKW
    H = 23.0
    nsl = 6
    for turn, sc in ((0.0, 1.0), (45.0, 0.9)):
        for s in range(nsl):
            t0, t1 = s / float(nsl), (s + 1) / float(nsl)
            w0, w1 = (4.0 + (topw - 4.0) * t0) * sc, (4.0 + (topw - 4.0) * t1) * sc
            d0, d1 = (4.0 + (topd - 4.0) * t0) * sc, (4.0 + (topd - 4.0) * t1) * sc
            A.frustum((w0, d0), (w1, d1), H / nsl + 0.4, (0, 0, 1.0 + t0 * H), ramp[min(len(ramp) - 1, int((t0 + 0.08 * turn / 45.0) * len(ramp)))], (0, 0, turn))
    for k in range(10):
        t = rnd.uniform(0.2, 0.85)
        a = rnd.uniform(0, 360)
        r = (4.0 + (min(topw, topd) - 4.0) * t) * 0.5 - 1.6
        x, y, _ = polar(r, a)
        A.chunk((rnd.uniform(6, 9), rnd.uniform(6, 9), rnd.uniform(6, 10)), (x, y, 1.0 + t * H), band(ramp, t, rnd), (rnd.uniform(-8, 8), rnd.uniform(-8, 8), a), 0.14, rnd, (0.7, 0.7))
    A.chunk((topw + 1.0, topd + 1.0, 1.8), (0, 0, 24.0), P['dirt'], (0, 0, i * 20), 0.05, rnd)
    A.chunk((topw, topd, 3.0), (0, 0, 25.6), P['grass'], (0, 0, i * 20), 0.06, rnd)
    for k in range(5):
        x, y, _ = polar(rnd.uniform(3, topw * 0.35), rnd.uniform(0, 360))
        _moss_patch(A, rnd, x, y, 26.9, rnd.uniform(1.2, 2.0))
    return _fin(A, 'floating_rock')


# ================================================================ ARENA SEGMENT  LM26_01/02/03 (MINOR)
def _arena(i):
    reset()
    A = Acc()
    rnd = random.Random(5500 + i)
    R = 34.0                                         # wall centre-line radius; arc centre at +y so it bows toward -y (front)
    wth = 4.0
    span_deg = 72.0                                  # total arc sweep -> a clearly curved segment
    H = 30.0
    ncol = [5, 4, 6][i % 3]
    cy = R                                           # front of the arc sits near y=0
    a0, a1 = 90 - span_deg / 2, 90 + span_deg / 2    # centred so the arc faces -y
    # the curved back wall, grounded from z=0 (sweep an upright rectangle around the arc)
    A.sweep([(R - wth / 2, 0.0), (R + wth / 2, 0.0), (R + wth / 2, H), (R - wth / 2, H)],
            a0, a1, 22, band(STON, 0.4, rnd), loc=(0, cy, 0), rot=(0, 0, 180))
    # a continuous base course / plinth it rests on
    A.sweep([(R - wth / 2 - 1.2, 0.0), (R + wth / 2 + 1.2, 0.0), (R + wth / 2 + 1.0, 2.2), (R - wth / 2 - 1.0, 2.2)],
            a0 - 2, a1 + 2, 22, P['s_base'], loc=(0, cy, 0), rot=(0, 0, 180))
    def at(frac, rr, z):
        a = math.radians(180 + a0 + (a1 - a0) * frac)
        return (math.cos(a) * rr, cy + math.sin(a) * rr, z)
    # engaged round half-columns standing on the front face, from the ground up (relief, reads as colonnade)
    for k in range(ncol):
        f = k / (ncol - 1)
        x, y, _ = at(f, R - wth / 2, 0)
        ang = math.degrees(math.atan2(y - cy, x))
        colh = H * (1.0 if (k + i) % 4 else rnd.uniform(0.6, 0.85))
        A.cyl(2.5, colh, (x, y, 0.0), band(STON, 0.45, rnd), verts=14)
        for d in range(1, int(colh / 6)):
            A.cyl(2.65, 0.5, (x, y, d * 6.0), P['s_warm'], verts=14)
        A.box((5.6, 3.6, 1.6), (x, y, colh), P['s_hi'], (0, 0, ang), bev=0.12)   # capital
    # recessed arched bays between columns: a dark void set INTO the wall + an arch head (depth, not a flat black bar)
    for k in range(ncol - 1):
        f = (k + 0.5) / (ncol - 1)
        vx, vy, _ = at(f, R, 0)
        ang = math.degrees(math.atan2(vy - cy, vx))
        A.box((5.2, wth + 0.4, 12.0), (vx, vy, 7.0), P['void'], (0, 0, ang), bev=0)              # recessed bay
        A.sweep([(2.6, -wth / 2 - 0.2), (3.6, -wth / 2 - 0.2), (3.6, wth / 2 + 0.2), (2.6, wth / 2 + 0.2)],
                0, 180, 10, P['s_mid'], loc=(vx, vy, 13.0), rot=(90, 0, ang))                    # arch head
    # broken top edge: knock merlon-like notches out of the parapet, pattern per sibling
    broke = [{1, 3}, {0, 2}, {2, 4}][i % 3]
    for k in range(ncol + 2):
        f = k / (ncol + 1)
        bx, by, _ = at(f, R, H - 0.5)
        ang = math.degrees(math.atan2(by - cy, bx))
        if k in broke:
            A.chunk((5.0, wth, rnd.uniform(0.6, 2.0)), (bx, by, H), band(STON, 0.4, rnd), (0, 0, ang), 0.2, rnd)
        else:
            A.box((4.6, wth + 0.3, 3.0), (bx, by, H + 1.0), band(STON, 0.6, rnd), (0, 0, ang), bev=0.1)
    # fallen debris hugging the wall foot along the arc (seated on ground against the base, not scattered out front)
    for k in range(6 + i):
        f = rnd.random()
        bx, by, _ = at(f, R - wth / 2 + rnd.uniform(-1.5, 2.5), 0)
        s = rnd.uniform(1.6, 3.6)
        A.chunk((s, s * rnd.uniform(0.8, 1.2), rnd.uniform(0.8, s * 0.7)), (bx, by, s * 0.25 - 0.3),
                band(STON, rnd.uniform(0, 0.4), rnd), (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(3):
        bx, by, _ = at(rnd.random(), R - wth / 2, 0)
        _moss_patch(A, rnd, bx, by, rnd.uniform(0, 4), rnd.uniform(1.4, 2.2))
    return _fin(A, 'arena_wall')


# ================================================================ RUIN AQUEDUCT ARCH  LM27_01/02 (MAJOR)
def _aqueduct(i):
    reset()
    A = Acc()
    rnd = random.Random(5600 + i)
    piers = [-15.0, 0.0, 15.0]
    pierw = 7.0
    toph = [36.0, 34.0][i]
    for j, xp in enumerate(piers):
        h = toph - (6.0 if (i == 1 and j == 2) else 0.0)
        A.box((pierw, 8.0, h), (xp, 0, h / 2.0), band(STON, 0.4, rnd), bev=0.3)
        # stone courses so the pier is not a blank slab
        for z in range(6, int(h) - 2, 6):
            A.box((pierw + 0.5, 8.4, 0.6), (xp, 0, z), P['s_warm'], bev=0.1)
    # arches between piers: real sweep ring (stone) with recessed dark void behind, NOT a white underside
    for xc in (-7.5, 7.5):
        A.sweep([(6.5, -4.2), (8.4, -4.2), (8.4, 4.2), (6.5, 4.2)], 0, 180, 12, band(STON, 0.5, rnd), loc=(xc, 0, 24.0), rot=(90, 0, 0))
        A.box((9.0, 6.6, 0.6), (xc, 0, 24.0 + 6.0), P['void'], bev=0)                            # thin dark backing = depth, not a hole
    # parapet along the top: SOLID stone blocks with gaps that are real recessed openings (dark backed), not black outer faces
    toplen = 46.0
    nb = 11
    for k in range(nb):
        x = -toplen / 2 + k * toplen / (nb - 1)
        if rnd.random() < 0.28:                         # a broken-away merlon: leave a notch but back it with stone
            A.box((toplen / nb, 7.0, 1.2), (x, 0, toph - 3.0), band(STON, 0.4, rnd), bev=0.1)
            continue
        A.box((toplen / nb * 0.9, 7.2, 4.0), (x, 0, toph - 1.0), band(STON, 0.55, rnd), bev=0.12)
    A.box((toplen, 7.6, 2.2), (0, 0, toph - 4.0), band(STON, 0.45, rnd), bev=0.15)               # continuous parapet base course
    # the channel on top is a shallow matte pale trough (stepped), NOT a bright cyan slab; only on 01
    if i == 0:
        A.box((toplen, 3.2, 1.0), (0, 0, toph - 2.4), P['s_base'], bev=0)                        # trough floor (dark stone)
        A.box((toplen, 2.0, 0.5), (0, 0, toph - 1.9), P['water'], bev=0)                         # thin pale matte water, recessed
    _ground_rubble(A, rnd, 7, 22.0, 6.0, STON, 1.4, 3.4)
    for k in range(4):                               # moss as settled patches on piers, grounded-feel (sitting on a ledge)
        xp = rnd.choice(piers)
        _moss_patch(A, rnd, xp + rnd.uniform(-3, 3), 4.1, rnd.uniform(3, 14), rnd.uniform(1.2, 2.0))
    return _fin(A, 'aqueduct_arches')


# ================================================================ RUIN COLUMN SET  LM28_01/02/03 (MINOR)
def _columns(i):
    reset()
    A = Acc()
    rnd = random.Random(5700 + i)
    A.cyl(12.0, 1.4, (0, 0, 0), P['s_base'], verts=16, r2=11.0)
    A.cyl(10.5, 0.7, (0, 0, 1.4), P['s_mid'], verts=16, r2=9.5)
    # genuinely different column counts / heights / break pattern per sibling, soft colour (no high-contrast stripes)
    layouts = [[(5.0, 2.2, 36.0, 1.0), (-4.0, -3.0, 22.0, 0.55), (-2.0, 5.0, 14.0, 0.35)],
               [(0.0, 0.0, 30.0, 0.8), (6.0, 3.0, 38.0, 1.0), (-6.0, -2.0, 9.0, 0.3)],
               [(4.0, 4.0, 40.0, 1.0), (-5.0, 2.0, 18.0, 0.5)]][i % 3]
    for (cx, cy, ch, frac) in layouts:
        n = max(3, int(ch / 6.0))
        for d in range(n):                           # fluted drums, banded by course for clear tone variation
            if d / n > frac:
                break
            key = strata([P['s_dk'], P['s_mid'], P['s_hi']], d, 1)
            A.cyl(2.6, 6.0, (cx, cy, 1.0 + d * 6.0), key, verts=14, r2=2.5)   # thicker, embedded 0.4 into base
        topz = 1.0 + min(n, int(frac * n)) * 6.0
        if frac > 0.6:                               # a capital on tall survivors
            A.box((5.8, 5.8, 1.8), (cx, cy, topz), P['s_warm'], bev=0.12)
    # fallen drum segments LYING on the base disc (radius 1.9 -> centre at z=1.9 so they rest on the plinth top)
    for k in range(4):
        a = rnd.uniform(0, 180)
        A.cyl(1.9, rnd.uniform(4, 7), (rnd.uniform(-7, 7), rnd.uniform(-7, 7), 2.1 + 1.9), band(STON, 0.4, rnd), verts=12, rot=(90, 0, a))
    _ground_rubble(A, rnd, 6, 9.0, 9.0, STON, 1.2, 2.6)
    for k in range(2):
        _moss_patch(A, rnd, rnd.uniform(-8, 8), rnd.uniform(-8, 8), 2.1, rnd.uniform(1.2, 1.8))
    return _fin(A, 'broken_columns')


# ================================================================ battered round tower helper (stumps + watchtowers)
def _battered_tower(seed, r, height, ruin, roof=False, var_i=0, shape=0):
    """Round ruined tower with eroded broken top and masonry relief. shape 0 = battered taper, 1 = straighter blockier shaft. Pivot bottom-centre."""
    reset()
    A = Acc()
    rnd = random.Random(5800 + seed)
    verts = 16
    drums = max(4, int(height / 7.0))
    # body: stacked drums. shape 0 = battered taper; shape 1 = straighter shaft with a steeper batter and more blocks
    taper_k = 0.12 if shape == 0 else 0.05
    for d in range(drums):
        z = d * (height / drums)
        rr = r * (1.0 - taper_k * d / drums)
        key = strata(STON, d, 1)                      # banded by course -> clear tonal variation, not one tan
        A.cyl(rr, height / drums + 0.3, (0, 0, z), key, verts=verts, r2=rr * 0.985)
        A.cyl(rr + 0.3, 0.7, (0, 0, z), P['s_dk'], verts=verts, r2=rr + 0.3)       # recessed-look dark course line
        # protruding individual stone blocks ringing this course (real relief, reads as masonry)
        nbl = 8 if shape == 0 else 10
        for b in range(nbl):
            if (b + d) % 3 == 0:                      # skip some so it is irregular / weathered
                continue
            a = 360.0 * b / nbl + d * 9.0
            x, y, _ = polar(rr + 0.2, a)
            A.box((1.8, 1.1, height / drums * 0.6), (x, y, z + height / drums * 0.5),
                  band(STON, 0.3 + 0.5 * d / drums, rnd), (0, 0, a), bev=0.1)
    rtop = r * (1.0 - taper_k * (drums - 1) / drums)
    # vertical cracks (thin recessed dark lines) for ruin character
    for k in range(2 + shape):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rtop, a)
        A.box((0.4, 0.5, height * rnd.uniform(0.3, 0.6)), (x, y, height * rnd.uniform(0.3, 0.6)), P['void'], (0, 0, a), bev=0)
    # arrow slits recessed (dark void) around the body
    for k in range(3):
        a = k * 120 + var_i * 25
        x, y, _ = polar(rtop - 0.2, a)
        A.box((0.9, 1.4, 3.2), (x, y, height * (0.35 + 0.18 * k)), P['void'], (0, 0, a), bev=0)
    # a doorway at the front, recessed
    A.box((3.6, 2.0, 6.4), (0, -(rtop - 0.1), 3.2), P['void'], bev=0)
    A.sweep([(1.8, -1.0), (2.4, -1.0), (2.4, 1.0), (1.8, 1.0)], 0, 180, 8, P['s_hi'], loc=(0, -(rtop - 0.1), 6.0), rot=(90, 0, 0))
    if roof:
        A.cyl(rtop + 0.6, height * 0.22, (0, 0, height), P['r_warm'], verts=verts, r2=0.0)
        # break one side of the cone so it reads ruined
        A.chunk((rtop * 0.9, rtop * 0.5, height * 0.14), (rtop * 0.4, 0, height + height * 0.07), P['r_base'], (0, 20, 0), 0.25, rnd)
    else:
        # eroded broken crenellated rim: merlons ATTACHED to the rim. shape 1 collapses diagonally (different silhouette).
        nb = 10
        for k in range(nb):
            a = 360.0 * k / nb
            x, y, _ = polar(rtop - 0.4, a)
            if shape == 1:
                mh = max(0.0, 5.0 * (0.5 + 0.5 * math.cos(math.radians(a))) - rnd.uniform(0, 1.5))  # tall one side, gone the other
            else:
                mh = rnd.uniform(0.0, 4.5)
            if mh < 0.6:
                continue
            A.chunk((2.4, 2.0, mh), (x, y, height - 0.3 + mh / 2.0), band(STON, 0.7, rnd), (0, 0, a), 0.18, rnd)
        if shape == 1:                                 # a chunk of the wall sheared away near the top
            A.box((3.0, 4.0, 6.0), (rtop * 0.7, 0, height - 2.0), P['void'], (0, 0, 0), bev=0)
    # settled moss patches low on the wall and rubble at the foot
    for k in range(3):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(r - 0.3, a)
        _moss_patch(A, rnd, x, y, rnd.uniform(1, 5), rnd.uniform(1.2, 2.0))
    _ground_rubble(A, rnd, 7, r + 3.0, r + 3.0, STON, 1.2, 3.0)
    return _fin(A, 'watchtower')


# LM29 tower stumps: 01 battered taper, 02 straighter blockier shaft with a sheared top (different silhouette)
def _stump(i):
    return _battered_tower(10 + i, r=11.0, height=[36.0, 34.0][i % 2], ruin=True, roof=False, var_i=i, shape=i % 2)


# PL05 ruined watchtowers: 01 battered, 02 straight/sheared, 03 broken-roof
def _watch(i):
    if i == 2:                                      # 03: ruined with broken roof
        return _battered_tower(30 + i, r=9.0, height=40.0, ruin=True, roof=True, var_i=i, shape=0)
    return _battered_tower(30 + i, r=9.0, height=40.0, ruin=True, roof=False, var_i=i, shape=i % 2)


# ================================================================ RUINED CASTLE MODULE  LM31_01/02/03 (01/02 MINOR, 03 MAJOR)
def _castle(i):
    reset()
    A = Acc()
    rnd = random.Random(5900 + i)
    # a real ruined wall: two-faced with thickness, battlements, arrow slits, a corner tower - varied damage per sibling
    th = 4.0
    wlen = 34.0
    wh = [30.0, 34.0, 28.0][i % 3]
    # main curtain wall as a thick box with inner+outer faces (use two offset boxes so it has depth)
    A.box((wlen, th, wh), (0, 0, wh / 2.0), band(STON, 0.45, rnd), bev=0.15)
    for z in range(5, int(wh) - 2, 6):              # stone courses (relief, not blank)
        A.box((wlen + 0.4, th + 0.4, 0.6), (0, 0, z), P['s_warm'], bev=0.1)
    # arrow slits + a window, recessed dark voids
    for sx in (-10.0, 0.0, 11.0):
        A.box((0.9, th + 0.3, 4.0), (sx, 0, wh * 0.5), P['void'], bev=0)
    A.box((4.4, th + 0.3, 5.4), (6.0, 0, wh * 0.32), P['void'], bev=0)
    A.sweep([(2.2, -th / 2 - 0.1), (2.9, -th / 2 - 0.1), (2.9, th / 2 + 0.1), (2.2, th / 2 + 0.1)], 0, 180, 8, P['s_hi'], loc=(6.0, 0, wh * 0.32 + 2.7), rot=(90, 0, 0))
    # broken crenellations on top: merlons with gaps, some knocked away, damage pattern varies
    nb = 9
    broke = [{3, 4}, {1, 6}, {2, 5, 7}][i % 3]
    for k in range(nb):
        x = -wlen / 2 + 2.0 + k * (wlen - 4.0) / (nb - 1)
        if k in broke:
            A.chunk((2.6, th, rnd.uniform(0.6, 1.6)), (x, 0, wh + 0.4), band(STON, 0.4, rnd), (0, 0, rnd.uniform(-8, 8)), 0.2, rnd)
            continue
        A.box((2.6, th, 3.2), (x, 0, wh + 1.6), band(STON, 0.6, rnd), bev=0.1)
    # a square corner tower, taller, battered, different break per sibling
    tx = wlen / 2 - 2.0
    tth = wh + [8.0, 5.0, 9.0][i % 3]
    A.frustum((9.0, 9.0), (8.0, 8.0), tth, (tx, 2.0, 0), band(STON, 0.5, rnd))
    for z in range(6, int(tth) - 3, 7):
        A.box((9.4, 9.4, 0.6), (tx, 2.0, z), P['s_warm'], bev=0.1)
    A.box((1.0, 2.0, 4.0), (tx, 2.0 - 4.6, tth * 0.6), P['void'], bev=0)                          # slit
    for k in range(4):                               # broken tower-top merlons attached to rim
        a = k * 90 + 45
        x, y, _ = polar(3.4, a)
        mh = rnd.uniform(0.0, 2.6)
        if mh < 0.6:
            continue
        A.chunk((2.4, 2.4, mh), (tx + x, 2.0 + y, tth + mh / 2.0), band(STON, 0.6, rnd), (0, 0, a), 0.18, rnd)
    # moss as scattered PATCHES on the wall face (not continuous painted rings)
    for k in range(7):
        side = rnd.choice([-1, 1])
        _moss_patch(A, rnd, rnd.uniform(-wlen / 2 + 2, wlen / 2 - 2), side * (th / 2 + 0.2), rnd.uniform(2, wh - 4), rnd.uniform(1.0, 2.0))
    _ground_rubble(A, rnd, 10, 18.0, 6.0, STON, 1.4, 3.8)
    return _fin(A, 'ruin_module')


# ================================================================ FLOATING ISLAND HERO  FL01_01/02/03 (MINOR, v5_coast)
def _float_island(i):
    reset()
    A = Acc()
    rnd = random.Random(6000 + i)
    topr = 43.0
    # top disc of grass + soil
    A.cyl(topr, 4.0, (0, 0, 22.0), P['grass'], verts=24, r2=topr - 1.5)
    A.cyl(topr - 0.5, 3.0, (0, 0, 19.5), P['dirt'], verts=24, r2=topr - 2.0)
    # UNDERSIDE: one tapering natural rock+root mass (chunks shrinking to a point), warm graded - NOT stacked plates
    steps = 9
    for k in range(steps):
        t = k / (steps - 1.0)
        w = topr * 2 * (1.0 - 0.84 * t) + 5.0
        z = 17.0 - t * 27.0
        # several overlapping cubic chunks per layer (not one wide disc) so the mass reads as craggy rock, not plates
        nseg = max(1, int(4 * (1.0 - t)) + 1)
        for s in range(nseg):
            sa = rnd.uniform(0, 360)
            sr = rnd.uniform(0, w * 0.22)
            cw = w / (1.0 + 0.5 * (nseg - 1)) * rnd.uniform(0.8, 1.2)
            A.chunk((cw, cw * rnd.uniform(0.8, 1.15), 8.5),                     # tall overlap kills the plate look
                    (math.cos(math.radians(sa)) * sr, math.sin(math.radians(sa)) * sr, z + rnd.uniform(-2, 2)),
                    band(ROCK, 1.0 - t, rnd), (rnd.uniform(-10, 10), rnd.uniform(-10, 10), rnd.uniform(0, 90)),
                    0.13, rnd, (rnd.uniform(0.65, 0.88), rnd.uniform(0.65, 0.88)))
    # vertical spike crags plunging down the centre -> a pointed root, breaks any horizontal banding
    for k in range(5):
        a = k * 72 + i * 30
        x, y, _ = polar(topr * 0.28, a)
        A.chunk((rnd.uniform(6, 10), rnd.uniform(6, 10), rnd.uniform(14, 22)), (x * 0.6, y * 0.6, rnd.uniform(-2, 3)),
                band(ROCKW, 0.35, rnd), (rnd.uniform(-8, 8), rnd.uniform(-8, 8), a), 0.12, rnd, (0.3, 0.3))
    # dangling root crags clustered near the top of the mass (attached)
    for k in range(5):
        a = k * 72 + i * 30 + 36
        x, y, _ = polar(topr * 0.5, a)
        A.chunk((rnd.uniform(5, 9), rnd.uniform(5, 9), rnd.uniform(8, 16)), (x, y, 10.0 - rnd.uniform(0, 6)),
                band(ROCKW, 0.4, rnd), (rnd.uniform(-6, 6), rnd.uniform(-6, 6), a), 0.15, rnd, (0.35, 0.35))
    # --- distinct TOP composition per hero so the three differ clearly ---
    pal = {'bark': V['bark'], 'leaf': V['leaf'], 'leaf2': V['leaf2'], 'bloom': V['leaf2']}
    if i == 0:                                       # single central ruined tower, trees ringing the rim
        A.append(_tower_acc(rnd, 7.0, 26.0), (0, 0, 24.0))
        for k in range(6):
            a = k * 60
            x, y, _ = polar(topr * 0.66, a)
            G.tree(A, rnd, rnd.uniform(12, 18), rnd.uniform(4, 6), pal, 'oak', x, y, 24.0)
    elif i == 1:                                     # off-centre broken column cluster + a pond, trees to one side
        for k in range(4):
            x, y, _ = polar(rnd.uniform(4, 10), k * 90 + 20)
            column(A, x - 8, y, 24.0, 1.4, rnd.uniform(10, 20), R.RUIN, rnd.uniform(0.3, 0.8), rnd)
        A.cyl(7.0, 0.6, (12.0, -6.0, 24.2), P['water'], verts=16, r2=6.0)                        # pale matte pond, recessed
        A.cyl(7.6, 0.5, (12.0, -6.0, 23.9), P['dirt'], verts=16, r2=7.0)
        for k in range(4):
            x, y, _ = polar(topr * 0.7, k * 90 + 45)
            G.tree(A, rnd, rnd.uniform(14, 20), rnd.uniform(4, 6), pal, 'oak', x, y, 24.0)
    else:                                            # two towers (a broken gatehouse look) + sparse trees + rock outcrop
        A.append(_tower_acc(rnd, 5.5, 22.0), (-9.0, 4.0, 24.0))
        A.append(_tower_acc(rnd, 5.5, 18.0), (9.0, -4.0, 24.0))
        A.chunk((10.0, 8.0, 7.0), (0, 10.0, 24.0 + 3.0), band(ROCKW, 0.6, rnd), (0, 0, 20), 0.18, rnd)
        for k in range(3):
            x, y, _ = polar(topr * 0.6, k * 120 + 60)
            G.tree(A, rnd, rnd.uniform(13, 18), rnd.uniform(4, 6), pal, 'oak', x, y, 24.0)
    for k in range(5):
        x, y, _ = polar(rnd.uniform(6, topr * 0.7), rnd.uniform(0, 360))
        _moss_patch(A, rnd, x, y, 24.0, rnd.uniform(1.4, 2.4))
    return _fin(A, 'floating_island')


def _tower_acc(rnd, r, h):
    """A small ruined round tower as its own Acc (for append onto islands)."""
    T = Acc()
    drums = max(3, int(h / 7.0))
    for d in range(drums):
        z = d * (h / drums)
        rr = r * (1.0 - 0.1 * d / drums)
        T.cyl(rr, h / drums + 0.2, (0, 0, z), band(STON, 0.3 + 0.6 * d / drums, rnd), verts=14, r2=rr * 0.99)
        T.cyl(rr + 0.3, 0.5, (0, 0, z), P['s_warm'], verts=14, r2=rr + 0.3)
    T.box((2.4, 1.4, 4.4), (0, -(r - 0.2), 2.2), P['void'], bev=0)
    nb = 8
    for k in range(nb):
        a = 360.0 * k / nb
        x, y, _ = polar(r - 0.4, a)
        mh = rnd.uniform(0.0, 3.0)
        if mh < 0.5:
            continue
        T.chunk((1.8, 1.6, mh), (x, y, h - 0.3 + mh / 2.0), band(STON, 0.7, rnd), (0, 0, a), 0.18, rnd)
    return T


# ================================================================ ROCK ARCH NATURAL  PL06_01/02 (MINOR, v5_plains)
def _rock_arch(i):
    reset()
    A = Acc()
    rnd = random.Random(6100 + i)
    # a natural rock arch: two battered legs and a continuous arc of overlapping boulders spanning them, warm graded rock.
    span = [30.0, 32.0][i]                            # clear opening width, varied per sibling
    legw = 13.0
    top = 38.0
    springer = top * 0.5                              # height where the arc starts off each leg
    legx = span / 2.0 + legw * 0.35                   # centre of each leg
    # legs: stacked chunks from ground up to the springer, leaning slightly inward at the top
    for sx in (-1, 1):
        legs = 5
        for k in range(legs):
            t = k / (legs - 1.0)
            x = sx * legx - sx * t * (legw * 0.22)
            A.chunk((legw * (1.0 - 0.12 * t), legw * 0.92, springer / legs + 1.6),
                    (x, rnd.uniform(-1, 1), t * springer + springer / legs / 2),
                    band(ROCK, t * 0.55, rnd), (rnd.uniform(-5, 5), sx * 5 * t, rnd.uniform(0, 20)), 0.14, rnd, (0.84, 0.84))
    # the crown: a semicircular arc of overlapping boulders from one springer to the other (physically bridges the legs)
    ncrown = 9
    arc_r = (legx + legw * 0.3)                       # radius of the arc centre-line
    for k in range(ncrown):
        ang = math.radians(180.0 * k / (ncrown - 1))  # 0..180 across the top
        cx = -math.cos(ang) * arc_r
        cz = springer + math.sin(ang) * (top - springer)
        A.chunk((legw * 0.95, legw * 0.9, legw * 0.8), (cx, rnd.uniform(-1, 1), cz),
                band(ROCKW, 0.45 + 0.4 * math.sin(ang), rnd), (0, rnd.uniform(-5, 5), math.degrees(ang) - 90), 0.14, rnd, (0.8, 0.8))
    # boulders piled at the feet, grounded, touching the legs (no cyan sliver, no tree nubs)
    for sx in (-1, 1):
        for k in range(4):
            x = sx * legx + rnd.uniform(-5, 5)
            s = rnd.uniform(3, 7)
            A.chunk((s, s, rnd.uniform(2, 5)), (x, rnd.uniform(-7, 7), s * 0.4 - 0.3), band(ROCK, rnd.uniform(0, 0.4), rnd),
                    (0, 0, rnd.uniform(0, 90)), 0.18, rnd)
    _ground_rubble(A, rnd, 8, span, 9.0, ROCK, 1.4, 3.6)
    for k in range(4):                               # warm ledges SET AGAINST the legs (not floating in the opening)
        sx = -1 if k % 2 else 1
        x = sx * (legx - legw * 0.35) + rnd.uniform(-1.5, 1.5)
        A.chunk((rnd.uniform(4, 7), rnd.uniform(3, 6), rnd.uniform(1.5, 3.0)), (x, rnd.uniform(-5, 5), rnd.uniform(3, springer * 0.8)),
                P['r_warm'], (rnd.uniform(-8, 8), 0, rnd.uniform(0, 40)), 0.2, rnd)
    for k in range(3):
        _moss_patch(A, rnd, rnd.uniform(-span / 2, span / 2), rnd.uniform(-6, 6), rnd.uniform(0, 4), rnd.uniform(1.4, 2.2))
    return _fin(A, 'rock_arch')


# ================================================================ HAY SILO  PL02_01 (MINOR, keep as grain-sheaf prop, tidy)
def _hay(i):
    reset()
    A = Acc()
    rnd = random.Random(6200 + i)
    # grain sheaves bound at the waist - natural straw tone, strand relief (not a bright flat slab)
    for k in range(3):
        x = -3.4 + k * 3.4
        A.cyl(2.5, 6.0, (x, rnd.uniform(-0.6, 0.6), 0), P['straw'], verts=12, r2=2.3)
        A.cyl(2.6, 4.2, (x, 0, 6.0), P['straw2'], verts=12, r2=0.3)                              # flared top
        A.sweep([(2.3, -0.12), (2.7, -0.12), (2.7, 0.12), (2.3, 0.12)], 0, 360, 12, V['rope'], loc=(x, 0, 2.6))  # binding
        for s in range(8):                                                                       # raised vertical strands (relief)
            sa = s * 45.0 + k * 15
            sx, sy, _ = polar(2.45, sa)
            A.box((0.25, 0.25, 5.6), (x + sx, sy, 2.8), P['straw2'] if s % 2 else P['straw'], (0, 0, sa), bev=0)
        for s in range(7):                                                                       # splayed strands fanning off the top
            sa = s * 51.0
            sx, sy, _ = polar(1.6, sa)
            A.cyl(0.14, rnd.uniform(2.0, 3.4), (x + sx, sy, 8.0), P['straw2'], verts=5, r2=0.05, rot=(rnd.uniform(-22, 22), rnd.uniform(-22, 22), 0))
    A.box((0.3, 0.3, 3.4), (5.0, 1.6, 1.7), V['timber'], bev=0)                                  # a leaning fork
    A.box((0.2, 0.3, 2.0), (5.0, 1.6, 3.6), V['iron'], bev=0)
    return _fin(A, 'hay_silo')


# ================================================================ FARM CART  PL03_02 (MINOR, make distinct from cart_01)
def _cart(i):
    reset()
    A = Acc()
    rnd = random.Random(6300 + i)
    # cart_02: a two-wheeled covered/tipping cart with raised rails and crates - clearly different silhouette from cart_01
    A.box((9.0, 5.0, 0.5), (0, 0, 2.4), V['plank'], bev=0.04)
    # high slatted side rails (taller than cart_01's low sides)
    for sg in (-1, 1):
        A.box((9.0, 0.35, 2.4), (0, sg * 2.4, 3.6), V['plank'], bev=0.03)                        # solid side panel (no see-through gaps)
        for k in range(5):
            A.box((0.3, 0.3, 2.2), (-3.6 + k * 1.8, sg * 2.52, 3.6), V['sign'], bev=0.02)         # lighter batten ribs on the outside
    A.box((0.4, 5.0, 2.4), (-4.4, 0, 3.6), V['plank'], bev=0.03)                                 # tailboard
    # two big wheels (not four): a different axle layout
    for sg in (-1, 1):
        A.cyl(2.3, 0.4, (0, sg * 2.9, 2.3), V['timber'], verts=16, rot=(90, 0, 0))
        A.cyl(0.4, 0.6, (0, sg * 2.9, 2.3), V['iron'], verts=8, rot=(90, 0, 0))
        for k in range(8):
            A.box((0.2, 0.3, 4.4), (0, sg * 2.9, 2.3), V['iron'], (k * 22.5, 0, 0), bev=0)
    # a long single shaft (hand/ox cart) instead of cart_01's split poles
    A.beam((4.4, 0, 2.4), (9.2, 0, 1.4), 0.35, 0.35, V['timber'])
    A.beam((9.0, -0.6, 1.4), (9.0, 0.6, 1.4), 0.25, 0.25, V['timber'])                            # cross handle
    # distinct cargo: stacked crates, not loose hay
    for (cx, cy, cz, s) in ((-1.0, 0.8, 2.9, 2.0), (1.4, -0.6, 2.9, 1.8), (0.2, 0.4, 4.9, 1.6)):
        A.box((s, s, s), (cx, cy, cz + s / 2), V['plank'], (0, 0, rnd.uniform(-12, 12)), bev=0.08)
    return _fin(A, 'cart')


ROCKL = [P['r_base'], P['r_low'], P['r_rust'], P['r_mid'], P['r_hi']]


def _arcane_shards():
    """LM20_01 (lead pass 2) - arcane ruin of standing shards: nine tall pointed stone shards of different heights on a dais, footings, rune bands, grounded rubble."""
    reset()
    A = Acc()
    rnd = random.Random(5201)
    A.cyl(19.0, 1.6, (0, 0, 0), P['s_base'], verts=24, r2=18.0)
    A.cyl(15.0, 0.8, (0, 0, 1.6), P['s_mid'], verts=24, r2=14.0)
    zt = 2.4
    for k in range(9):
        a = k * 40.0 + rnd.uniform(-10, 10)
        rr = rnd.uniform(6.0, 14.0) if k else 0.0
        x, y, _ = polar(rr, a)
        h = rnd.uniform(14.0, 34.0) if k % 3 else 37.0
        w = rnd.uniform(3.4, 5.2)
        A.chunk((w, w * rnd.uniform(0.7, 1.0), h), (x, y, zt + h / 2.0), band(STON, 0.15 + 0.7 * (k % 4) / 3.0, rnd), (rnd.uniform(-5, 5), rnd.uniform(-5, 5), a), 0.1, rnd, (0.4, 0.4))
        A.box((w + 1.4, w + 1.4, 0.8), (x, y, zt + 0.4), P['s_warm'], (0, 0, a), bev=0.06)
        A.box((w * 0.8, 0.5, 1.5), (x - math.sin(math.radians(a)) * (w * 0.5), y + math.cos(math.radians(a)) * (w * 0.5), zt + h * 0.45), V['rune'], (0, 0, a), bev=0)
    for k in range(10):
        s = rnd.uniform(2, 3.8)
        hh = rnd.uniform(1.2, 2.4)
        x, y, _ = polar(rnd.uniform(4, 17), rnd.uniform(0, 360))
        A.chunk((s, s, hh), (x, y, zt + hh / 2.0 - 0.2), band(STON, rnd.uniform(0, 0.5), rnd), (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(3):
        _moss_patch(A, rnd, rnd.uniform(-12, 12), rnd.uniform(-12, 12), 2.4, rnd.uniform(1.4, 2.2))
    return _fin(A, 'magic_ruin')


def _arcane_monolith():
    """LM20_03 (lead pass 2) - arcane ruin with ONE great carved monolith on a three-step round dais, rune bands, four low corner posts, a fallen cap slab."""
    reset()
    A = Acc()
    rnd = random.Random(5203)
    A.cyl(19.0, 1.6, (0, 0, 0), P['s_base'], verts=24, r2=18.0)
    A.cyl(15.0, 1.2, (0, 0, 1.6), P['s_mid'], verts=24, r2=14.0)
    A.cyl(11.0, 1.2, (0, 0, 2.8), P['s_warm'], verts=24, r2=10.0)
    zt = 4.0
    A.chunk((8.0, 6.0, 31.0), (0, 0, zt + 15.5), band(STON, 0.5, rnd), (0, 0, 0), 0.04, rnd, (0.82, 0.82))
    A.frustum((6.6, 4.8), (0.6, 0.6), 5.0, (0, 0, zt + 31.0), P['s_hi'])
    for z in (9.0, 15.0, 21.0, 27.0):
        A.box((6.2, 0.7, 1.6), (0, -3.0 - (z - 9.0) * 0.004, zt + z), V['rune'], bev=0)
        A.box((0.7, 5.0, 1.6), (4.0 - (z - 9.0) * 0.012, 0, zt + z), V['rune'], bev=0)
    for k in range(4):
        x, y, _ = polar(13.5, 45 + k * 90.0)
        A.chunk((3.0, 3.0, 6.0 + k * 1.5), (x, y, 1.6 + (6.0 + k * 1.5) / 2.0), band(STON, 0.3, rnd), (0, 0, 45 + k * 90.0), 0.08, rnd, (0.8, 0.8))
        A.box((3.8, 3.8, 0.7), (x, y, 1.95), P['s_warm'], (0, 0, 45 + k * 90.0), bev=0.05)
    A.chunk((9.0, 4.0, 2.6), (6.5, -12.0, 3.0), band(STON, 0.7, rnd), (0, 0, 28), 0.08, rnd)
    for k in range(8):
        s = rnd.uniform(2, 3.6)
        hh = rnd.uniform(1.2, 2.4)
        x, y, _ = polar(rnd.uniform(6, 17), rnd.uniform(0, 360))
        A.chunk((s, s, hh), (x, y, 2.6 + hh / 2.0 - 0.2), band(STON, rnd.uniform(0, 0.5), rnd), (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(3):
        _moss_patch(A, rnd, rnd.uniform(-12, 12), rnd.uniform(-12, 12), 2.6, rnd.uniform(1.4, 2.2))
    return _fin(A, 'magic_ruin')


def _arena_bands(A):
    R_, wth, cy = 34.0, 4.0, 34.0
    a0, a1 = 54.0, 126.0
    for z in (8.0, 16.0, 24.0):
        A.sweep([(R_ - wth / 2 - 0.4, z), (R_ - wth / 2, z), (R_ - wth / 2, z + 0.8), (R_ - wth / 2 - 0.4, z + 0.8)], a0, a1, 22, P['s_dk'], loc=(0, cy, 0), rot=(0, 0, 180))


def _columns_post(A):
    for (cx, cy) in ((0.0, 0.0), (6.0, 3.0), (-6.0, -2.0)):
        A.cyl(3.5, 0.9, (cx, cy, 1.1), P['s_warm'], verts=14)
        A.cyl(3.1, 0.6, (cx, cy, 1.9), P['s_hi'], verts=14)


def _stump_post(i):
    def post(A):
        rt = 10.5 if i == 0 else 10.9
        for k, (a, z) in enumerate(((20.0, 14.0), (140.0, 22.0), (260.0, 10.0))):
            x, y, _ = polar(rt, a)
            A.box((1.6, 2.2, 4.0), (x, y, z), P['void'], (0, 0, a), bev=0)
            A.box((2.4, 2.4, 0.7), (x, y, z + 2.2), P['s_hi'], (0, 0, a), bev=0.05)
            A.box((2.4, 2.4, 0.6), (x, y, z - 2.2), P['s_hi'], (0, 0, a), bev=0.05)
        if i == 1:
            for k in range(5):
                x, y, _ = polar(13.5 + k * 0.8, 200 + k * 16.0)
                A.chunk((4.0 - k * 0.4, 3.0, 2.6), (x, y, 1.3), P['s_base'], (0, 0, 200 + k * 16.0), 0.15, random.Random(k + 3))
    return post


def _watch_post(i):
    def post(A):
        rt = 8.2 if i != 1 else 8.6
        for a, z in ((70.0, 18.0), (190.0, 26.0), (310.0, 12.0)):
            x, y, _ = polar(rt, a)
            A.box((1.4, 1.8, 3.4), (x, y, z), P['void'], (0, 0, a), bev=0)
            A.box((2.2, 2.2, 0.6), (x, y, z + 2.0), P['s_hi'], (0, 0, a), bev=0.05)
        for k in range(3):
            x, y, _ = polar(rt + 0.3, 30 + k * 120.0)
            A.box((1.4, 1.2, 14.0 + k * 3.0), (x, y, 7.0 + k * 1.5), P['s_dk'], (0, 0, 30 + k * 120.0), bev=0.08)
    return post


def lm20_01():
    return LK.wrap(_arcane_shards)()


def lm20_03():
    return LK.wrap(_arcane_monolith)()


def lm26_02():
    return LK.wrap(lambda: _arena(1), prune=[dict(keys=None, max_size=4.2, max_z=1.2)])()


def lm26_03():
    return LK.wrap(lambda: _arena(2), post=_arena_bands, recolor=[LK.ramp([STON[1], STON[2]], [P['s_dk'], P['s_base'], P['s_mid'], P['s_warm']], zlim=(2.0, 31.0), trange=(0.0, 31.0), wobble=0.05)])()


def lm28_02():
    return LK.wrap(lambda: _columns(1), prune=[dict(keys=None, max_size=5.4, max_z=3.5)], post=_columns_post)()


def lm29_01():
    return LK.wrap(lambda: _stump(0), post=_stump_post(0), recolor=[LK.ramp(STON, [P['s_dk'], P['s_base'], P['s_mid'], P['s_hi']], trange=(0.0, 36.0), wobble=0.06)])()


def lm29_02():
    return LK.wrap(lambda: _stump(1), post=_stump_post(1), recolor=[LK.ramp(STON, [P['s_dk'], P['s_warm'], P['s_base'], P['s_warm']], trange=(0.0, 34.0), wobble=0.06)])()


def pl02_01():
    return LK.wrap(lambda: _hay(0), recolor=[LK.ramp([P['straw'], P['straw2']], [PS['straw4'], PS['straw3'], PS['straw3'], PS['straw5']], trange=(0.0, 24.0), wobble=0.05)])()


def pl05(i):
    return LK.wrap(lambda: _watch(i), post=_watch_post(i), recolor=[LK.ramp(STON, [P['s_dk'], P['s_base'], P['s_mid'], P['s_warm']], trange=(0.0, 42.0), wobble=0.06)])()


BATCHES = {
    'A1_plains': ('v5_plains', mk([(ids('PL02')[0], (lambda: _hay(0))), (ids('PL03')[1], (lambda: _cart(1)))] +
                                  _L(_watch, 'PL05') + _L(_rock_arch, 'PL06'), 0.1)),
    'A1_landmarks': ('v5_landmarks', mk(_L(_rim_rock, 'LM19') + [(ids('LM20')[1], (lambda: _magic_ruin(1)))] +
                                        [(ids('LM21')[1], (lambda: _float_rock(0))), (ids('LM21')[3], (lambda: _float_rock(1)))] +
                                        _L(_arena, 'LM26') + _L(_aqueduct, 'LM27') + _L(_columns, 'LM28') +
                                        _L(_stump, 'LM29') + _L(_castle, 'LM31'), 0.1)),
    'A1_coast': ('v5_coast', mk(_L(_float_island, 'FL01'), 0.1)),
}


# --- lead4 registration ---
import v5_leadkit as LK
PS = G.reg('vi_fa', {
    'straw3': ((196, 170, 108), 'Fabric', 0.0, 1.0),
    'straw4': ((170, 142, 88), 'Fabric', 0.0, 1.0),
    'straw5': ((214, 190, 128), 'Fabric', 0.0, 1.0),
})
BATCHES['lead4_via'] = ('v5_landmarks', mk([('LM20_01_crater_arcane_ruin_01', lm20_01), ('LM20_03_crater_arcane_ruin_03', lm20_03), ('LM26_02_ruin_arena_segment_02', lm26_02),
                                            ('LM26_03_ruin_arena_segment_03', lm26_03), ('LM28_02_ruin_column_set_02', lm28_02), ('LM29_01_ruin_tower_stump_01', lm29_01),
                                            ('LM29_02_ruin_tower_stump_02', lm29_02)], 0.1))
BATCHES['lead4_via_plains'] = ('v5_plains', mk([('PL02_01_hay_silo_01', pl02_01), ('PL05_01_ruined_watchtower_plains_01', lambda: pl05(0)),
                                                ('PL05_02_ruined_watchtower_plains_02', lambda: pl05(1)), ('PL05_03_ruined_watchtower_plains_03', lambda: pl05(2))], 0.1))
