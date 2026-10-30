"""v5_fx_vf - FIX ROUND builders for assignment A6 (worker vf). Owner: builder A6.
Replaces round-1 vf builders for: LM22 colossal falls (REDO), LM03 frost fortress, LM30 ruined castle,
LM18 crater monolith ring, LM25 ruin gate, VC02 skull cliffs x2, CO01 coast cliffs (05 falls, 03 cave), VG03 flowering x2, VG01_02 tall narrow.
No glow, no emissive, no bright-white/cyan water slabs. Water is pale matte stepped with foam. Front faces -Y, pivot bottom centre.
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
import v5_vf as ORIG          # round-1 module: reuse its palette P and tree dicts; never edit it

OP = ORIG.P

# NEW palette keys only, prefix vf_f_. Pale matte water + foam (NO neon, NO cyan glare).
P = G.reg('vf_f', {
    'water':      ((150, 176, 190), 'SmoothPlastic', 0.0, 0.55),   # pale blue-grey, matte
    'water_dp':   ((120, 150, 168), 'SmoothPlastic', 0.0, 0.60),   # darker pool water
    'foam':       ((224, 230, 232), 'SmoothPlastic', 0.0, 0.70),   # off-white foam, not pure white
    'rock_a':     ((120, 116, 112), 'Rock', 0.0, 0.95),            # faceted cliff bands
    'rock_b':     ((98, 94, 90),    'Rock', 0.0, 0.95),
    'rock_c':     ((140, 136, 130), 'Rock', 0.0, 0.92),
    'rock_base':  ((80, 77, 74),    'Slate', 0.0, 0.95),           # dark wet base
    'moss':       ((96, 124, 72),   'Grass', 0.0, 1.0),
    'snowrock_a': ((176, 180, 186), 'Rock', 0.0, 0.9),             # grey snow-rock
    'snowrock_b': ((150, 154, 160), 'Rock', 0.0, 0.92),
    'snowcap':    ((236, 240, 246), 'Snow', 0.0, 0.7),
    'wall':       ((178, 170, 160), 'Limestone', 0.0, 0.88),       # weathered stone for castle
    'wall_b':     ((152, 144, 134), 'Cobblestone', 0.0, 0.92),
    'wall_c':     ((196, 188, 176), 'Limestone', 0.0, 0.85),
    'niche':      ((40, 36, 34),    'Slate', 0.0, 1.0),            # recessed dark void
    'sand':       ((206, 180, 140), 'Sandstone', 0.0, 0.9),
    'sand_d':     ((170, 144, 108), 'Sandstone', 0.0, 0.9),
    'sand_l':     ((228, 208, 172), 'Limestone', 0.0, 0.85),
    'red_in':     ((150, 86, 70),   'Sandstone', 0.0, 0.9),        # recessed niche stone, not sticker-bright
    'bark':       ((96, 74, 56),    'Wood', 0.0, 0.95),
    'blossom_a':  ((236, 188, 204), 'Grass', 0.0, 0.95),
    'blossom_b':  ((224, 166, 190), 'Grass', 0.0, 0.95),
    'leaf':       ((86, 134, 66),   'Grass', 0.0, 1.0),
    'leaf2':      ((112, 156, 80),  'Grass', 0.0, 1.0),
    'leafd':      ((60, 100, 54),   'Grass', 0.0, 1.0),
})

CLIFF = [P['rock_b'], P['rock_a'], P['rock_c']]        # dark base -> mid -> light top (graded)
SNOW = [P['snowrock_b'], P['snowrock_a'], P['snowcap']]


def _fin(A, name):
    A.to_scene()
    return finalize(name, 28)


# ------------------------------------------------------------------ shared: chunky faceted cliff (no thin stacked slabs)
def _faceted_cliff(A, rnd, w, d, h, keys, cx=0.0, cy=0.0, z0=0.0, cap=None, base_key=None, cols=None, lean=0.0, front=-1.0):
    """A cliff built from a FEW big masses plus many smaller facets, graded by height. Face toward -Y (front).
    Unlike the round-1 cliff this stacks chunky angular blocks of varied depth with no thin paper plates."""
    cols = cols or max(4, int(w / 16.0))
    cw = w / cols
    # dark wet base band of big chunks touching the ground
    if base_key:
        for c in range(cols + 1):
            x = cx - w / 2 + cw * c
            A.chunk((cw * rnd.uniform(1.1, 1.4), d * rnd.uniform(0.8, 1.05), h * rnd.uniform(0.1, 0.16)),
                    (x + rnd.uniform(-1, 1), cy + rnd.uniform(-d * 0.1, d * 0.1), z0 + h * 0.06),
                    base_key, (0, 0, rnd.uniform(-8, 8)), 0.12, rnd, (0.95, 0.95))
    for c in range(cols):
        x = cx - w / 2 + cw * (c + 0.5)
        hc = h * rnd.uniform(0.82, 1.0)
        z = z0 + h * 0.07
        while z < z0 + hc - h * 0.05:
            # chunky block: tall and deep, not a thin plate
            sh = min(rnd.uniform(0.14, 0.24) * h, z0 + hc - z)
            dep = d * rnd.uniform(0.72, 1.0)
            t = (z - z0) / max(h, 1e-6)
            key = band(keys, t, rnd, 0.1)
            A.chunk((cw * rnd.uniform(1.05, 1.35), dep, sh * 1.12),
                    (x + rnd.uniform(-cw * 0.2, cw * 0.2),
                     cy + front * (d - dep) * 0.22 + rnd.uniform(-1.2, 1.2) + lean * t * d,
                     z + sh * 0.5),
                    key, (0, rnd.uniform(-5, 5), rnd.uniform(-7, 7)), 0.13, rnd, (0.92, 0.9))
            z += sh * 0.84
        if cap:
            A.chunk((cw * 1.15, d * 0.7, h * 0.07), (x, cy, z0 + hc + h * 0.02), cap, (0, 0, rnd.uniform(-8, 8)), 0.14, rnd, (0.8, 0.8))
    # fallen rubble at the foot, touching the ground
    for k in range(int(cols * 2.2)):
        A.chunk((rnd.uniform(cw * 0.3, cw * 0.7), rnd.uniform(3, 7), rnd.uniform(2.5, 6.0)),
                (cx + rnd.uniform(-w * 0.5, w * 0.5), cy + front * (d * 0.5 + rnd.uniform(0, 6)), z0 + rnd.uniform(1.0, 3.0)),
                band(keys, 0.0, rnd), (0, 0, rnd.uniform(0, 90)), 0.18, rnd)


# ------------------------------------------------------------------ shared: pale stepped waterfall hugging the rock
def _falls(A, rnd, cx, cy_face, ztop, zbot, width, steps=6, pool_y=None, pool_w=None):
    """A believable waterfall: a stack of short pale-matte steps hugging the rock face (cy_face is the -Y rock surface),
    each step slightly proud of the one above, foam ridge at each lip, a plunge pool with foam at the base. No bright slabs."""
    n = steps
    dz = (ztop - zbot) / n
    for i in range(n):
        zt = ztop - i * dz
        zb = zt - dz
        w = width * (1.0 - 0.04 * i)
        # the water sheet set a little in front of the rock, tilted so it reads as falling, not a panel
        yf = cy_face - 0.8 - i * 0.55
        A.box((w, 1.1, dz * 1.14), (cx, yf, (zt + zb) / 2.0), P['water'], (6, 0, 0), bev=0)
        # broken vertical ribbons for relief (slightly varied widths, same pale colour)
        nb = max(2, int(w / 4.5))
        for b in range(nb):
            bx = cx - w / 2 + (b + 0.5) * w / nb + rnd.uniform(-0.6, 0.6)
            A.box((w / nb * 0.5, 0.5, dz * rnd.uniform(0.7, 1.05)), (bx, yf - 0.6, (zt + zb) / 2.0 + rnd.uniform(-0.5, 0.5)), P['water_dp'], bev=0)
        # foam ridge at the lip of each step
        A.box((w * 0.92, 1.4, dz * 0.22), (cx, yf - 0.7, zb + dz * 0.12), P['foam'], (10, 0, 0), bev=0)
        for k in range(max(3, int(w / 3))):
            A.ball(rnd.uniform(0.5, 1.0), (cx + rnd.uniform(-w / 2, w / 2), yf - 0.9, zb + rnd.uniform(0, dz * 0.3)), P['foam'], segs=6, rings=4, scale=(1.3, 1.0, 0.5))
    # plunge pool + foam ring
    py = pool_y if pool_y is not None else cy_face - 1.6 - n * 0.55 - 4.0
    pw = pool_w if pool_w is not None else width + 8.0
    A.chunk((pw + 6.0, 16.0, 3.0), (cx, py, zbot - 0.6), P['rock_base'], (0, 0, 0), 0.1, rnd)   # stone basin rim
    A.box((pw, 13.0, 1.0), (cx, py, zbot + 0.6), P['water_dp'], bev=0)
    for k in range(10):
        A.ball(rnd.uniform(0.8, 1.6), (cx + rnd.uniform(-pw / 2, pw / 2), py + rnd.uniform(-5, 5), zbot + 1.0), P['foam'], segs=6, rings=4, scale=(1.4, 1.2, 0.45))


# ------------------------------------------------------------------ shared: CONTINUOUS falling sheet (one unbroken column, not isolated panels)
def _sheet_falls(A, rnd, cx, cy_face, ztop, zbot, width, pool_y=None, pool_w=None, breaks=2):
    """A single continuous waterfall column hugging the rock: one tall gently-narrowing water face with many thin vertical
    ribbon grooves for relief, a faint lip crest at the top, a couple of foam aprons where the rock juts, and all the
    heavy foam gathered in the plunge pool at the base. Reads as a falling sheet, never as separate flat panels."""
    H = ztop - zbot
    nseg = max(6, int(H / 14.0))
    dz = H / nseg
    for i in range(nseg):
        zt = ztop - i * dz
        w = width * (1.0 - 0.06 * (i / nseg))                         # narrows very slightly toward the base
        yf = cy_face - 0.7 - 0.20 * i                                 # leans out as it falls
        A.box((w, 1.0, dz * 1.1), (cx, yf, zt - dz / 2.0), P['water'], (4, 0, 0), bev=0)   # the continuous sheet
    # vertical ribbon relief running the WHOLE height (unbroken streaks, darker water)
    nb = max(4, int(width / 3.2))
    for b in range(nb):
        bx = cx - width / 2 + (b + 0.5) * width / nb + rnd.uniform(-0.4, 0.4)
        bw = width / nb * rnd.uniform(0.3, 0.55)
        A.box((bw, 0.5, H * rnd.uniform(0.9, 1.0)), (bx, cy_face - 1.1, zbot + H / 2.0 + rnd.uniform(-2, 2)), P['water_dp'], (4, 0, 0), bev=0)
    # crest lip at the very top (thin foam line where it spills over)
    A.box((width * 1.02, 1.4, 1.2), (cx, cy_face - 0.5, ztop - 0.4), P['foam'], (0, 0, 0), bev=0)
    # a couple of mid foam aprons only where the rock juts (not a grid of panels)
    for q in range(breaks):
        zq = zbot + H * (0.35 + 0.3 * q)
        A.box((width * 0.85, 1.6, 1.4), (cx, cy_face - 1.0 - 0.2, zq), P['foam'], (8, 0, 0), bev=0)
        for k in range(4):
            A.ball(rnd.uniform(0.6, 1.1), (cx + rnd.uniform(-width / 2, width / 2), cy_face - 1.4, zq - rnd.uniform(0, 1.5)), P['foam'], segs=6, rings=4, scale=(1.3, 1.0, 0.5))
    # plunge pool with heavy foam at the base
    py = pool_y if pool_y is not None else cy_face - 2.0 - 4.0
    pw = pool_w if pool_w is not None else width + 10.0
    A.chunk((pw + 6.0, 16.0, 3.0), (cx, py, zbot - 0.6), P['rock_base'], (0, 0, 0), 0.1, rnd)
    A.box((pw, 13.0, 1.0), (cx, py, zbot + 0.6), P['water_dp'], bev=0)
    for k in range(14):
        A.ball(rnd.uniform(0.9, 1.8), (cx + rnd.uniform(-pw / 2, pw / 2), py + rnd.uniform(-6, 5), zbot + 1.0), P['foam'], segs=6, rings=4, scale=(1.5, 1.2, 0.5))
def colossal_falls():
    reset()
    A = Acc()
    rnd = random.Random(2202)
    # one chunky faceted massif, not stacked plates
    _faceted_cliff(A, rnd, 240.0, 110.0, 236.0, CLIFF, 0, 30.0, 0, cap=P['moss'], base_key=P['rock_base'], cols=11)
    # flanking gorge walls, angled in
    for sg in (-1, 1):
        _faceted_cliff(A, rnd, 70.0, 80.0, 210.0, CLIFF, sg * 108.0, -8.0, 0, cap=P['moss'], base_key=P['rock_base'], cols=4, lean=sg * 0.04)
    # one DOMINANT continuous falling sheet down the FRONT face of the massif, plus a shorter secondary
    for cx, w, zt, zb, br in ((-30.0, 46.0, 236.0, 36.0, 3), (48.0, 30.0, 196.0, 40.0, 2)):
        # cut a visible channel of darker rock into the front face (front of massif is ~ y=-25), water sits proud of it
        A.chunk((w + 10.0, 26.0, zt - zb), (cx, -26.0, (zt + zb) / 2.0), P['rock_base'], (0, 0, 0), 0.05, rnd, (0.95, 0.95))
        for sg in (-1, 1):                                                   # chunky channel walls framing the fall, proud of the face
            A.chunk((8.0, 20.0, zt - zb), (cx + sg * (w / 2 + 5.0), -32.0, (zt + zb) / 2.0), band(CLIFF, 0.5, rnd), (0, 0, 0), 0.12, rnd, (0.9, 0.9))
        _sheet_falls(A, rnd, cx, -36.0, zt, zb, w, pool_y=-62.0, pool_w=w + 14.0, breaks=br)
    # big calm pool at the foot with foam, then rubble, then a few trees on ledges
    A.box((150.0, 40.0, 1.0), (-10.0, -58.0, 0.6), P['water_dp'], bev=0)
    for k in range(22):
        A.chunk((rnd.uniform(4, 9), rnd.uniform(4, 8), rnd.uniform(2, 5)), (rnd.uniform(-72, 72), rnd.uniform(-74, -44), 1.8), band(CLIFF, rnd.random(), rnd), (0, 0, rnd.uniform(0, 90)), 0.16, rnd)
    for k in range(16):
        G.tree(A, rnd, rnd.uniform(14, 20), rnd.uniform(6, 9), ORIG.TKD, rnd.choice(('oak', 'conifer')), rnd.uniform(-110, 110), rnd.uniform(16, 60), rnd.uniform(196, 214))
    return _fin(A, 'colossal_falls')


# ================================================================== LM03 frost fortress hero (MAJOR: chunky snow-rock)
def fortress():
    reset()
    A = Acc()
    rnd = random.Random(2203)
    # chunky faceted snow-rock massif behind, no floating plates
    _faceted_cliff(A, rnd, 300.0, 120.0, 220.0, SNOW, 0, 70.0, 0, cap=P['snowcap'], base_key=P['snowrock_b'], cols=12)
    for sg in (-1, 1):
        _faceted_cliff(A, rnd, 56.0, 64.0, 150.0, SNOW, sg * 150.0, 28.0, 0, cap=P['snowcap'], base_key=P['snowrock_b'], cols=4)
    # snow drifts settling in pockets (on top only)
    FK = ORIG.FK
    levels = [(0.0, 230.0, -110.0), (46.0, 170.0, -66.0), (92.0, 112.0, -26.0)]
    for i, (z, L, y) in enumerate(levels):
        A.box((L + 12.0, 34.0, 4.0), (0, y + 12.0, z + 2.0), P['wall'], bev=0.4)
        n = int(L / 40.0)
        for k in range(n):
            wall_seg(A, rnd, 40.0, 18.0, 9.0, FK, -L / 2.0 + 20.0 + k * 40.0 * (L / (n * 40.0)), y, z + 4.0, 7.0, k % 2 == 0, False)
        for sg in (-1, 1):
            round_tower(A, rnd, 10.0 - i * 1.2, 40.0 + i * 8.0, FK, sg * (L / 2.0 + 2.0), y, z + 4.0, top='cone', slits=3, bands=3, roof_k=1.5, verts=22)
        for k in range(3):
            h_ = 22.0 + 6.0 * ((k + i) % 2)
            A.frustum((26.0, 20.0), (24.0, 18.0), h_, (-L / 2.0 * 0.5 + k * L * 0.28 - 10.0, y + 22.0, z + 4.0), P['wall'])
            A.gable(22.0, 28.0, 10.0, (-L / 2.0 * 0.5 + k * L * 0.28 - 10.0, y + 22.0, z + 4.0 + h_), ORIG.P['roof'], (0, 0, 90))
    A.frustum((50.0, 40.0), (44.0, 34.0), 62.0, (0, 10.0, 96.0), P['wall'])
    A.frustum((52.0, 42.0), (8.0, 8.0), 34.0, (0, 10.0, 158.0), ORIG.P['roof'])
    A.cyl(0.8, 14.0, (0, 10.0, 192.0), ORIG.P['iron'], verts=6)
    A.box((0.3, 7.0, 4.0), (0, 10.0, 203.0), ORIG.P['cloth'], bev=0)
    for sg in (-1, 1):
        round_tower(A, rnd, 8.0, 80.0, FK, sg * 30.0, -6.0, 96.0, top='cone', slits=4, bands=4, roof_k=1.6, verts=20, flag=True)
    for i in range(18):
        A.box((14.0, 3.0, 2.6 * (i + 1) * 0.3), (0, -118.0 + i * 3.2, 1.3 * (i + 1) * 0.3), P['wall_b'], bev=0.1)
    A.box((26.0, 40.0, 22.0), (0, -112.0, 11.0), P['snowrock_b'])
    A.box((12.0, 40.2, 14.0), (0, -112.0, 7.0), P['niche'], bev=0)
    # snow caps settled on the wall tops only
    for i, (z, L, y) in enumerate(levels):
        for k in range(int(L / 20.0)):
            A.chunk((rnd.uniform(5, 9), 6.0, 1.4), (-L / 2.0 + 10.0 + k * 20.0, y - 2.0, z + 13.0), P['snowcap'], (0, 0, rnd.uniform(0, 90)), 0.12, rnd)
    return _fin(A, 'frost_fortress_hero')


# ================================================================== LM30 ruined castle hero (MINOR: colour + recessed windows)
def ruined_castle():
    reset()
    A = Acc()
    rnd = random.Random(2230)
    CK = dict(ORIG.CK, wall=P['wall'], stone=P['wall_b'], trim=P['wall_c'], cap=P['moss'])
    A.chunk((130.0, 110.0, 4.0), (0, 0, 2.0), P['wall_b'], jit=0.03, rnd=rnd)
    courses = [P['wall'], P['wall_b'], P['wall_c']]
    for k in range(7):
        for sg in (-1, 1):
            h_ = rnd.uniform(6.0, 16.0)
            A.chunk((18.0, 7.0, h_), (-54.0 + k * 18.0, sg * 52.0, 4.0 + h_ / 2), band(courses, rnd.random(), rnd), (0, 0, 0), 0.1, rnd, (0.96, 0.9))
            A.chunk((7.0, 18.0, rnd.uniform(6.0, 14.0)), (sg * 62.0, -42.0 + k * 14.0, 8.0), band(courses, rnd.random(), rnd), (0, 0, 0), 0.1, rnd)
    round_tower(A, rnd, 9.0, 44.0, CK, -56.0, -48.0, 4.0, ruin=True, slits=3, bands=3)
    round_tower(A, rnd, 8.0, 30.0, CK, 58.0, -46.0, 4.0, ruin=True, slits=2, bands=2)
    round_tower(A, rnd, 8.5, 38.0, CK, 58.0, 48.0, 4.0, ruin=True, slits=3, bands=2)
    round_tower(A, rnd, 7.5, 24.0, CK, -58.0, 48.0, 4.0, ruin=True, slits=2, bands=2)
    for sx, sy, w_, d_, h_ in ((0, 6.0, 40.0, 34.0, 62.0), (-20, -20, 26, 18, 30.0), (24, -22, 20, 16, 24.0)):
        A.frustum((w_, d_), (w_ - 3.0, d_ - 3.0), h_, (sx, sy, 4.0), band(courses, 0.5, rnd))
        for k in range(12):
            a = rnd.uniform(0, 360)
            x, y, _ = polar(max(w_, d_) * 0.5, a)
            A.chunk((rnd.uniform(3, 8), rnd.uniform(3, 8), rnd.uniform(1.0, 7.0)), (sx + x * 0.9, sy + y * 0.8, 4.0 + h_ + rnd.uniform(-2, 2)), band(courses, rnd.random(), rnd), (0, 0, a), 0.2, rnd)
        # recessed windows: frame + real dark void set back
        for r_ in range(3):
            zz = 10.0 + r_ * 16.0
            if zz > h_ - 6:
                continue
            for i in range(max(1, int(w_ / 9))):
                wx = sx - w_ / 2.0 + 6.0 + i * 9.0
                A.box((2.8, 2.0, 5.0), (wx, sy - d_ / 2.0 + 0.4, zz), P['wall_c'], bev=0.1)   # frame
                A.box((1.8, 2.2, 3.8), (wx, sy - d_ / 2.0 - 0.3, zz), P['niche'], bev=0)      # recessed void
    A.chunk((22.0, 18.0, 28.0), (12.0, -10.0, 18.0), P['niche'], (0, 0, 0), 0.05, rnd)
    # tidy rubble: rest on the ground in small heaps
    for k in range(5):
        A.mound(rnd.uniform(-55, 55), rnd.uniform(-50, 50), rnd.uniform(8, 16), rnd.uniform(8, 14), rnd.uniform(3, 6), 5, [P['wall_b'], P['wall']], rnd, 5.0)
    for k in range(18):
        A.ball(rnd.uniform(2.0, 4.0), (rnd.uniform(-62, 62), rnd.uniform(-56, 56), rnd.uniform(6, 20)), P['moss'], segs=7, rings=4, scale=(1.3, 1.2, 1.0))
    return _fin(A, 'ruined_castle')


# ================================================================== LM18 crater monolith ring (MINOR: thicker, crater base)
def standing_stones():
    reset()
    A = Acc()
    rnd = random.Random(2218)
    # crater: raised broken rim with a lower centre, not a flat green disc
    A.mound(0, 0, 150.0, 150.0, 8.0, 44, [P['rock_b'], P['rock_a'], P['moss']], rnd, -2.0, 0.5, 1.0)
    A.cyl(58.0, 1.2, (0, 0, 0.0), P['rock_base'], verts=36, r2=54.0)   # sunken crater floor
    for k in range(44):   # scattered boulders/rubble breaking up the base
        x, y, _ = polar(rnd.uniform(18, 68), rnd.uniform(0, 360))
        A.chunk((rnd.uniform(3, 8), rnd.uniform(3, 7), rnd.uniform(1.5, 5)), (x, y, 1.0), band(CLIFF, rnd.random(), rnd), (0, 0, rnd.uniform(0, 90)), 0.18, rnd)
    n = 14
    for k in range(n):
        a = 360.0 / n * k + rnd.uniform(-4, 4)
        x, y, _ = polar(62.0, a)
        h = rnd.uniform(32.0, 48.0)
        # THICK faceted monolith (not thin spike): wide base chunk + tapering stack
        A.chunk((12.0, 9.0, 5.0), (x, y, 2.5), P['rock_base'], (0, 0, a + 90.0), 0.1, rnd)
        G.spire(A, rnd, 6.0, h, [P['rock_b'], P['rock_a'], P['rock_c']], x, y, 2.5, 8, lean=rnd.uniform(-0.03, 0.03), cap=P['rock_c'])
        for r_ in range(4):
            A.box((9.0, 0.6, 1.0), (x, y - 0.1, 9.0 + r_ * 9.0), P['niche'], (0, 0, a + 90.0), bev=0)   # carved band
    # a few lintel pairs (post and lintel, not an arch)
    for k in range(3):
        a = 120.0 * k + 30.0
        x, y, _ = polar(62.0, a + 360.0 / n / 2.0)
        A.chunk((22.0, 5.0, 4.0), (x, y, 30.0), P['rock_a'], (0, 0, a + 90.0 + 10), 0.06, rnd)
    A.chunk((10.0, 10.0, 3.0), (0, 0, 1.6), P['rock_c'], (0, 0, 0), 0.08, rnd)   # central altar
    for k in range(10):   # boulder heaps along the crater rim
        a = 360.0 / 10 * k + 18.0
        x, y, _ = polar(rnd.uniform(44, 56), a)
        A.mound(x, y, 12.0, 10.0, 7.0, 6, [P['rock_base'], P['rock_b'], P['rock_a']], rnd, 0.0, 0.4, 0.8)
    return _fin(A, 'crater_monolith_ring')


# ================================================================== LM25 ruin gate hero (MINOR: clearer lintel, recessed niches)
def ancient_gate():
    reset()
    A = Acc()
    rnd = random.Random(2225)
    for sg in (-1, 1):
        h = 58.0 if sg < 0 else 40.0
        A.frustum((24.0, 20.0), (19.0, 16.0), h, (sg * 32.0, 0, 0), P['sand_d'])
        for k in range(5):
            A.box((25.0 - k * 0.6, 21.0 - k * 0.6, 0.8), (sg * 32.0, 0, 4.0 + k * (h - 6.0) / 5.0), P['sand_l'], bev=0.1)
        # ashlar block relief on the outward faces
        for r_ in range(int(h / 6.0)):
            for cc in range(3):
                A.box((6.0, 1.0, 4.4), (sg * 32.0 + (cc - 1) * 7.5, -9.6, 7.0 + r_ * 6.0), P['sand'] if (r_ + cc) % 2 else P['sand_l'], bev=0.1)
                A.box((1.0, 1.0, 4.4), (sg * 43.6, -5.0 + (cc - 1) * 5.0, 7.0 + r_ * 6.0), P['sand'] if (r_ + cc) % 2 else P['sand_l'], bev=0.1)
        # recessed stone niches (frame + set-back panel), not flat red stickers
        for k in range(3):
            zz = (12.0 + k * 13.0) if h > 50 else (12.0 + k * 9.0)
            if zz > h - 8:
                continue
            A.box((13.0, 1.2, 10.0), (sg * 32.0, -9.0, zz), P['sand'], bev=0.1)         # surround
            A.box((9.5, 2.0, 7.5), (sg * 32.0, -8.4, zz), P['red_in'], bev=0)           # recessed panel, muted
            A.box((9.5, 0.6, 7.5), (sg * 32.0, -9.2, zz), P['niche'], bev=0)            # thin shadow gap
        if sg > 0:
            for k in range(12):
                A.chunk((rnd.uniform(3, 7), rnd.uniform(3, 7), rnd.uniform(1.5, 4)), (sg * 32.0 + rnd.uniform(-10, 10), rnd.uniform(-9, 4), rnd.uniform(36, 42)), P['sand_d'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    # clear, chunky lintel spanning both pylons (one solid beam reading as a gate head)
    A.box((52.0, 12.0, 9.0), (0, 0, 46.0), P['sand'], bev=0.3)
    A.box((54.0, 13.0, 2.0), (0, 0, 51.5), P['sand_l'], bev=0.2)        # cap course on the lintel
    for k in range(6):                                                  # corbels under the lintel so it reads supported
        A.box((3.0, 11.0, 3.0), (-20.0 + k * 8.0, 0, 40.5), P['sand_d'], bev=0.1)
    # the far half has slumped (broken end), seated on a grounded rubble skirt
    A.box((16.0, 10.0, 5.0), (30.0, -2.0, 4.0), P['sand'], (0, 8, 6), bev=0.2)
    A.chunk((22.0, 16.0, 4.0), (30.0, -4.0, 1.4), P['sand_d'], (0, 0, 4), 0.12, rnd, (0.95, 0.95))   # the slump rests on this grounded base
    # rubble gathered into a FEW grounded heaps at the pylon feet (welded, not scattered floating chips)
    for hx in (-32.0, 0.0, 30.0):
        A.mound(hx, -6.0, rnd.uniform(12, 18), rnd.uniform(8, 12), rnd.uniform(3.5, 5.0), 6, [P['wall_b'], P['sand_d'], P['sand']], rnd, 0.0, 0.4, 0.8)
    for k in range(8):                                                   # moss settled at the heap feet, on the ground
        A.ball(rnd.uniform(1.4, 2.2), (rnd.uniform(-36, 36), rnd.uniform(-10, 6), 1.0), P['moss'], segs=7, rings=4, scale=(1.3, 1.2, 0.4))
    return _fin(A, 'ruin_gate_hero')


# ================================================================== VC02 skull cliffs x2 (MINOR: faceted rock, seated jaw, differ)
def _skull(var):
    reset()
    A = Acc()
    rnd = random.Random(2210 + var)
    keys = [P['rock_base'], P['rock_b'], P['rock_a']]
    _faceted_cliff(A, rnd, 200.0, 120.0, 120.0, keys, 0, 36.0, 0, cap=None, base_key=P['rock_base'], cols=11)
    for k in range(60):   # extra surface facets so the dark cliff is not a bare stack
        x = rnd.uniform(-96, 96)
        z = rnd.uniform(6, 112)
        A.chunk((rnd.uniform(5, 11), rnd.uniform(3, 6), rnd.uniform(5, 11)), (x, 36.0 - 60.0 + rnd.uniform(-2, 3), z), band(keys, z / 120.0, rnd), (0, rnd.uniform(-6, 6), rnd.uniform(-8, 8)), 0.14, rnd, (0.9, 0.9))
    bone = P['wall_c']
    bone_d = P['wall_b']
    A.ball(46.0, (0, -10.0, 70.0), bone, segs=24, rings=16, scale=(1.18, 0.82, 1.0))
    A.ball(34.0, (0, -22.0, 36.0), bone, segs=18, rings=12, scale=(1.0, 0.8, 0.8))
    for sx in (-1, 1):
        A.ball(13.0, (sx * 22.0, -45.0, 72.0), P['niche'], segs=14, rings=10, scale=(1.0, 0.5, 1.15))
        A.ball(15.5, (sx * 22.0, -43.0, 72.0), bone_d, segs=12, rings=8, scale=(1.0, 0.4, 1.1))
        A.box((14.0, 6.0, 4.0), (sx * 22.0, -46.0, 87.0), bone, (0, 0, sx * 12.0), bev=0.3)
    A.prism([(-6.0, 0), (6.0, 0), (0, 16.0)], 6.0, (0, -44.0, 42.0), P['niche'], (90, 0, 0))
    A.box((52.0, 8.0, 5.0), (0, -50.0, 22.0), bone, bev=0.3)
    for k in range(10):
        A.box((4.2, 5.0, 8.0 if k % 2 == 0 else 6.5), (-22.0 + k * 4.9, -53.0, 17.0), bone, bev=0.25)
    for k in range(10):
        A.box((4.2, 5.0, 7.0 if k % 2 == 0 else 5.5), (-22.0 + k * 4.9, -53.0, 7.0), bone, bev=0.25)
    A.box((50.0, 4.0, 12.0), (0, -52.0, 12.0), P['niche'], bev=0)
    # lower jaw seated flush under the teeth (raised so it meets the upper teeth block)
    A.box((60.0, 10.0, 7.0), (0, -48.0, 3.0), bone, bev=0.3)
    A.box((50.0, 6.0, 3.0), (0, -52.0, 5.5), bone_d, bev=0.2)
    if var == 1:
        # design 1: smooth cranium, stair of dark treads to the mouth-cave
        for i in range(12):
            A.box((30.0 - i, 4.0, 1.6 * (i + 1)), (0, -62.0 - i * 3.6, 0.8 * (i + 1)), P['rock_base'], bev=0.1)
    else:
        # design 2: HORNED skull, clearly different silhouette (big curved horns, brow ridge, no stair)
        for sx in (-1, 1):
            for k in range(6):
                t = k / 5.0
                q = (sx * (40.0 + 26.0 * t), -6.0 - 8.0 * t * t, 98.0 + 60.0 * t)
                A.chunk((11.0 - k * 1.3, 11.0 - k * 1.3, 14.0), q, bone_d if k < 2 else P['rock_a'], (0, 20 * sx * t, 0), 0.08, rnd, (0.8, 0.8))
            A.chunk((10.0, 10.0, 8.0), (sx * 40.0, -6.0, 96.0), bone_d, (0, 0, 0), 0.1, rnd)
        A.box((56.0, 10.0, 5.0), (0, -40.0, 96.0), bone, bev=0.3)   # heavy brow ridge
    return _fin(A, 'skull_cliff')


def skull_1():
    return _skull(1)


def skull_2():
    return _skull(2)


# ================================================================== CO01 coast cliffs (05 falls, 03 cave)
def _coast_base(A, rnd):
    keys = [P['rock_b'], P['rock_a'], P['rock_c']]
    _faceted_cliff(A, rnd, 108.0, 42.0, 68.0, keys, 0, 8.0, 0, cap=P['moss'], base_key=P['rock_base'], cols=9)
    # extra surface facets so the face is not sparse
    for k in range(120):
        x = rnd.uniform(-52, 52)
        z = rnd.uniform(4, 64)
        A.chunk((rnd.uniform(3, 8), rnd.uniform(2, 5), rnd.uniform(3, 8)), (x, 8.0 - 21.0 + rnd.uniform(-1, 3), z), band(keys, z / 68.0, rnd), (0, rnd.uniform(-7, 7), rnd.uniform(-9, 9)), 0.14, rnd, (0.9, 0.9))
    return keys


def coast_03():
    """CO01_03 - cliff with a RECESSED sea cave (not a flat black square)."""
    reset()
    A = Acc()
    rnd = random.Random(2103)
    keys = _coast_base(A, rnd)
    # recessed cave: framed mouth + real depth (dark box set back, side walls, drooping lintel rock)
    cx, cy = 0.0, -12.0
    A.chunk((26.0, 8.0, 22.0), (cx, cy + 4.0, 11.0), P['rock_base'], (0, 0, 0), 0.05, rnd)       # darker rock around the mouth
    A.box((16.0, 16.0, 16.0), (cx, cy + 2.0, 9.0), P['niche'], bev=0)                            # recessed void going back
    for sg in (-1, 1):                                                                           # side walls of the mouth
        A.chunk((4.0, 10.0, 18.0), (cx + sg * 10.0, cy, 10.0), P['rock_b'], (0, 0, 0), 0.12, rnd)
    A.chunk((22.0, 9.0, 5.0), (cx, cy - 1.0, 19.0), P['rock_a'], (0, 0, 0), 0.12, rnd)           # overhang lintel
    for k in range(6):                                                                           # rubble at the cave foot
        A.chunk((rnd.uniform(2, 4), rnd.uniform(2, 4), rnd.uniform(1.2, 2.4)), (cx + rnd.uniform(-10, 10), cy - 4.0, 1.4), keys[k % 3], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(14):
        A.chunk((rnd.uniform(2, 6), rnd.uniform(2, 5), rnd.uniform(1.5, 3.5)), (rnd.uniform(-52, 52), rnd.uniform(-24, -10), 1.2), keys[k % 3], (0, 0, rnd.uniform(0, 90)), 0.18, rnd)
    return _fin(A, 'coast_cliff')


def coast_05():
    """CO01_05 - cliff with a PALE MATTE stepped waterfall (no cyan neon strip)."""
    reset()
    A = Acc()
    rnd = random.Random(2105)
    keys = _coast_base(A, rnd)
    # notch of dark rock, then the pale stepped fall hugging it
    A.chunk((12.0, 8.0, 64.0), (-14.0, -6.0, 34.0), P['rock_base'], (0, 0, 0), 0.06, rnd)
    _falls(A, rnd, -14.0, -10.0, 66.0, 6.0, 9.0, steps=6, pool_y=-22.0, pool_w=18.0)
    for k in range(14):
        A.chunk((rnd.uniform(2, 6), rnd.uniform(2, 5), rnd.uniform(1.5, 3.5)), (rnd.uniform(-52, 52), rnd.uniform(-24, -10), 1.2), keys[k % 3], (0, 0, rnd.uniform(0, 90)), 0.18, rnd)
    return _fin(A, 'coast_cliff')


# ================================================================== VG03 flowering trees x2 (MINOR: blended blossom), VG01_02 tall narrow
def _flowering(seed, h, crown, intermix):
    reset()
    A = Acc()
    rnd = random.Random(seed)
    # trunk + root flare + a few limbs
    tr = h * 0.045
    A.cyl(tr * 1.9, h * 0.06, (0, 0, 0), P['bark'], verts=8, r2=tr * 1.1)
    A.cyl(tr * 1.1, h * 0.55, (0, 0, h * 0.05), P['bark'], verts=8, r2=tr * 0.6)
    for k in range(4):
        a = 90 * k + rnd.uniform(-15, 15)
        x, y, _ = polar(tr * 1.6, a)
        A.beam((0, 0, h * 0.5), (x * 6, y * 6, h * 0.78), tr * 0.5, tr * 0.45, P['bark'])
    # canopy: MANY small clumps, ~45% pink blossom intermixed evenly with green (no big flat patch)
    n = intermix + 24
    for k in range(n):
        a = rnd.uniform(0, 360)
        rr = crown * (0.25 + 0.72 * (k / n)) * rnd.uniform(0.5, 1.0)
        x, y, _ = polar(rr, a)
        z = h * 0.6 + h * 0.36 * rnd.uniform(0, 1) + rnd.uniform(-1.5, 1.5)
        r = crown * rnd.uniform(0.18, 0.3)
        pink = (k * 7 % 20) < 9          # ~45% blossom, scattered by index not by region
        if pink:
            key = P['blossom_a'] if k % 2 else P['blossom_b']
        else:
            key = P['leaf'] if k % 2 else P['leaf2']
        A.ball(r, (x, y, z), key, segs=7, rings=5, scale=(1, 1, 0.9))
    # a crown cap of mixed clumps
    for k in range(6):
        key = (P['blossom_a'] if k % 2 else P['leaf2'])
        x, y, _ = polar(crown * 0.3, 60 * k)
        A.ball(crown * 0.28, (x, y, h * 0.95), key, segs=7, rings=5, scale=(1, 1, 0.85))
    return _fin(A, 'tree_flowering')


def flowering_1():
    return _flowering(2306, 27.0, 9.0, 26)


def flowering_2():
    return _flowering(2307, 26.0, 9.5, 30)


def tall_narrow_2():
    """VG01_02 - tall narrow tree, different foliage silhouette from 01 (fuller, wavier poplar-cypress with gold tips)."""
    reset()
    A = Acc()
    rnd = random.Random(2302)
    K = {'bark': P['bark'], 'leaf': P['leafd'], 'leaf2': P['leaf'], 'bloom': P['leaf2']}
    G.tree(A, rnd, 44.0, 6.4, K, 'cypress', 0, 0, 0, lean=0.4)
    # add irregular side tufts so the silhouette differs from the straight 01
    for k in range(10):
        t = (k + 0.5) / 10.0
        a = rnd.uniform(0, 360)
        r = 6.4 * (0.5 + 0.5 * math.sin(math.pi * t)) * rnd.uniform(0.7, 1.1)
        x, y, _ = polar(r, a)
        A.ball(rnd.uniform(1.4, 2.6), (x, y, 8.0 + 34.0 * t), P['leaf2'] if k % 2 else P['leaf'], segs=7, rings=5, scale=(1, 1, 1.2))
    return _fin(A, 'tree_tall_narrow')


def _stack2_post(A):
    G.spire(A, random.Random(5), 7.0, 52.0, [OP['rock'], OP['dark'], OP['rock2']], -13.0, 3.0, 6.0, 10, -0.1, None)


def _gate_post(A):
    for k in range(4):
        A.chunk((8.0 - k * 0.9, 9.0, 5.2), (16.0 + k * 1.1, 0.0, 36.5 + k * 4.4), OP['sand2'] if k % 2 else OP['sand'], (0, 0, 4 * k), 0.08, random.Random(40 + k), (0.95, 0.95))


def _old_oak2():
    reset()
    A = Acc()
    rnd = random.Random(2005)
    G.tree(A, rnd, 38.0, 12.0, ORIG.TKD, 'oak', 0, 0, 0, 1.0, True)
    return _fin(A, 'tree_oak_dead')


def co02_01():
    return LK.wrap(lambda: ORIG._stack(1), recolor=[LK.ramp([OP['moss']], [OP['rock2']])])()


def co02_02():
    return LK.wrap(lambda: ORIG._stack(2), post=_stack2_post, recolor=[LK.ramp([OP['moss']], [OP['sandl']]),
                                                                        LK.ramp([OP['rock'], OP['dark'], OP['rock2']], [OP['sand2'], OP['sand'], OP['sandl']], trange=(0.0, 80.0), wobble=0.05)])()


def co02_03():
    return LK.wrap(lambda: ORIG._stack(3), recolor=[LK.ramp([OP['moss']], [OP['rock2']]),
                                                     LK.ramp([OP['rock'], OP['dark'], OP['rock2']], [OP['rock2'], OP['red'], OP['sand2'], OP['rock2']], trange=(0.0, 80.0), wobble=0.05)])()


def lm25_01():
    return LK.wrap(ORIG.ancient_gate, post=_gate_post, prune=[dict(keys=None, max_size=6.5, max_z=2.0)])()


def vg02_02():
    return LK.wrap(_old_oak2)()


BATCHES = {
    'heroes': ('v5_landmarks', mk(list(zip(ids('LM22'), [colossal_falls])) +
                                  list(zip(ids('LM03'), [fortress])) +
                                  list(zip(ids('LM30'), [ruined_castle])) +
                                  list(zip(ids('LM18'), [standing_stones])) +
                                  list(zip(ids('LM25'), [ancient_gate])), 0.1)),
    'skull': ('v5_skull', mk(list(zip(ids('VC02'), [skull_1, skull_2])), 0.1)),
    'forest': ('v5_forest', mk([('VG03_01_tree_flowering_01', flowering_1), ('VG03_02_tree_flowering_02', flowering_2),
                                ('VG01_02_tree_tall_narrow_02', tall_narrow_2)], 0.1)),
    'coast': ('v5_coast', mk([('CO01_03_coastal_cliff_03', coast_03), ('CO01_05_coastal_cliff_05', coast_05)], 0.1)),
}


# --- lead4 registration ---
import v5_leadkit as LK
BATCHES['lead4_vf'] = ('v5_coast', mk([('CO02_01_sea_stack_01', co02_01), ('CO02_02_sea_stack_02', co02_02), ('CO02_03_sea_stack_03', co02_03)], 0.1))
BATCHES['lead4_vf_land'] = ('v5_landmarks', mk([('LM25_01_ruin_gate_hero', lm25_01)], 0.1))
BATCHES['lead4_vf_forest'] = ('v5_forest', mk([('VG02_02_tree_old_oak_02', vg02_02)], 0.1))
