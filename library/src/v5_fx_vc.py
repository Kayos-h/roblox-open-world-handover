"""v5_fx_vc - FIX ROUND builders for assignment A5 (Himalayan kit + natural entrances). Owner: builder A5.
Replaces the round-1 builders of the vc ids in library\\v5_work\\fix\\assign_A5.md. Same worker (vc), same category folders.
NEW palette keys only under prefix vc_f_ (never re-register a round-1 key name). No glow, no freestanding arch. Front -Y.
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
import v5_vc as ORIG          # round-1 module: reuse its palette dict VC and helpers, never edit it

VC = ORIG.VC                  # round-1 himalaya/entrance palette (stone, stone2, slate, snow, timber, plank, ...)
ROCKS = ORIG.ROCKS

P = G.reg('vc_f', {
    'rock_d': ((96, 94, 100), 'Slate', 0.0, 0.93),         # dark base rock
    'rock_m': ((132, 128, 124), 'Slate', 0.0, 0.93),       # mid rock
    'rock_l': ((162, 158, 150), 'Cobblestone', 0.0, 0.92), # light rock
    'whitewash': ((236, 232, 222), 'Concrete', 0.0, 0.85), # chorten whitewash
    'band_r': ((150, 70, 58), 'Brick', 0.0, 0.85),         # ochre-red chorten band
    'board': ((180, 150, 104), 'WoodPlanks', 0.0, 0.88),   # sign board face
    'rock_w': ((150, 138, 122), 'Cobblestone', 0.0, 0.93), # warm natural stone (tonal variation on entry rocks)
    'fr_a': ((72, 128, 178), 'Fabric', 0.0, 1.0),          # extra flag colours (distinct string)
    'fr_b': ((214, 160, 60), 'Fabric', 0.0, 1.0),
    'fr_c': ((176, 70, 62), 'Fabric', 0.0, 1.0),
    'fr_d': ((78, 150, 96), 'Fabric', 0.0, 1.0),
})
GRADE = [P['rock_d'], P['rock_m'], P['rock_l']]            # bottom -> top rock grade (replaces random ROCKS patches)


def _fin(A, name):
    A.to_scene()
    return finalize(name, 25)


# ================================================================= HM04 tunnel lining (MAJOR inverted faces / MINOR dark bore)
def _lining(bend):
    """Rebuild of ORIG._lining: inner bore faces get a lit stone colour, the straight shell is solid boxes (no inverted/black faces)."""
    reset()
    A = Acc()
    rnd = random.Random(21 + bend)
    ow, oh = 14.0, 16.0
    if not bend:
        L = 24.0
        for sg in (-1, 1):                                                  # solid rock side masses, graded
            for k in range(6):
                A.chunk((4.6, L / 6.0 * 1.15, 19.5), (sg * 9.7, -L / 2 + (k + 0.5) * L / 6.0, 9.75),
                        strata(GRADE, k, 2), (0, 0, 0), 0.07, rnd)
            A.box((0.7, L, oh), (sg * (ow / 2 + 0.35), 0, oh / 2), VC['slate'])     # lit inner lining wall (not dark void)
        for k in range(4):
            A.chunk((ow + 8.0, L / 4.0 * 1.15, 4.4), (0, -L / 2 + (k + 0.5) * L / 4.0, oh + 2.4), strata([P['rock_m'], P['rock_l']], k, 1), (0, 0, 0), 0.06, rnd)
        A.box((ow + 1.4, L, 0.8), (0, 0, oh + 0.4), VC['stone'])            # lintel (stone, not near-black slate)
        A.box((ow, L, 0.4), (0, 0, 0.2), VC['stone2'])                     # floor
        A.box((ow - 0.6, L, 0.4), (0, 0, oh - 0.2), VC['stone'])           # lit ceiling plane facing down into the bore
        for yy in (-8.0, 0.0, 8.0):
            for sg in (-1, 1):
                A.box((0.9, 0.9, oh), (sg * (ow / 2 - 0.3), yy, oh / 2), VC['timber'])
                A.beam((sg * (ow / 2 - 0.3), yy, oh - 3.0), (sg * (ow / 2 - 3.0), yy, oh), 0.5, 0.5, VC['timber'])
            A.box((ow, 0.9, 0.9), (0, yy, oh - 0.45), VC['timber'])
        for yy in (-4.0, 4.0):                                             # lantern brackets (unlit meshes)
            for sg in (-1, 1):
                A.beam((sg * (ow / 2 - 0.2), yy, 11.0), (sg * (ow / 2 - 1.5), yy, 11.4), 0.18, 0.18, VC['iron'])
                A.cyl(0.5, 0.9, (sg * (ow / 2 - 1.5), yy, 10.2), VC['gold'], verts=8)
        v4util.marker('mk_door', (0, -L / 2, 0.3))
    else:
        R = 40.0
        loc = (-R, 0, 0)
        sw = lambda poly, key: A.sweep(poly, 0, 30, 5, key, loc=loc)
        sw([(R - 11.0, 0), (R - 7.0, 0), (R - 7.0, 19.6), (R - 11.0, 19.6)], P['rock_m'])
        sw([(R + 7.0, 0), (R + 11.0, 0), (R + 11.0, 19.6), (R + 7.0, 19.6)], P['rock_l'])
        sw([(R - 11.0, oh), (R + 11.0, oh), (R + 11.0, 19.6), (R - 11.0, 19.6)], P['rock_m'])
        sw([(R - 7.0, 0), (R + 7.0, 0), (R + 7.0, 0.4), (R - 7.0, 0.4)], VC['stone2'])        # floor
        sw([(R - 7.0, oh - 0.4), (R + 7.0, oh - 0.4), (R + 7.0, oh), (R - 7.0, oh)], VC['stone'])  # lit ceiling
        sw([(R - 7.7, 0.4), (R - 7.0, 0.4), (R - 7.0, oh), (R - 7.7, oh)], VC['stone'])
        sw([(R + 7.0, 0.4), (R + 7.7, 0.4), (R + 7.7, oh), (R + 7.0, oh)], VC['stone'])
        for a in (0.0, 30.0):                                              # lit stone portal frames close the dark end slots at both bore ends
            ar = math.radians(a)
            for sg in (-1, 1):
                r = R + sg * 10.0
                A.box((3.0, 2.8, 20.0), (-R + r * math.cos(ar), r * math.sin(ar), 10.0), VC['stone'], (0, 0, a), bev=0.1)
            # full-height lit stone lintel closes the top so no dark void shows between the post tops
            A.box((23.6, 2.9, 8.4), (-R + R * math.cos(ar), R * math.sin(ar), 15.8), VC['stone2'], (0, 0, a), bev=0.1)
            A.box((23.6, 3.0, 0.9), (-R + R * math.cos(ar), R * math.sin(ar), 20.3), P['rock_l'], (0, 0, a), bev=0.08)  # lit coping cap
        for a in (4.0, 15.0, 26.0):
            ar = math.radians(a)
            for sg in (-1, 1):
                r = R + sg * (ow / 2 - 0.3)
                A.box((0.9, 0.9, oh), (-R + r * math.cos(ar), r * math.sin(ar), oh / 2), VC['timber'], (0, 0, a))
            A.box((0.9, ow, 0.9), (-R + R * math.cos(ar), R * math.sin(ar), oh - 0.45), VC['timber'], (0, 0, a))
        for a in (9.0, 21.0):
            ar = math.radians(a)
            for sg in (-1, 1):
                rw = R + sg * (ow / 2 + 0.3)                              # into the lining wall
                r = R + sg * (ow / 2 - 1.4)                                # bowl radius (inset)
                A.beam((-R + rw * math.cos(ar), rw * math.sin(ar), 10.9), (-R + r * math.cos(ar), r * math.sin(ar), 10.6), 0.2, 0.2, VC['iron'])
                A.cyl(0.5, 0.9, (-R + r * math.cos(ar), r * math.sin(ar), 10.2), VC['gold'], verts=8)
        v4util.marker('mk_door', (0, 0, 0.3))
    return _fin(A, 'tunnel_lining')


def lining_1():
    return _lining(0)


def lining_2():
    return _lining(1)


# ================================================================= HM05 cliff galleries (MINOR: flat grey cliff / loose snow)
def _gallery(var):
    """Rebuild of ORIG._gallery using the graded cliff() generator so the rock is varied (not one flat grey mass); snow conforms to the top."""
    reset()
    A = Acc()
    rnd = random.Random(70 + var)
    L = 40.0
    A.box((L, 12.0, 1.0), (0, -1.0, 0.5), VC['stone2'])
    cliff(A, rnd, L, 7.0, 22.0, GRADE, cx=0.0, cy=4.4, z0=1.0, cols=(8 if var == 1 else 6), cap=(P['rock_m'] if var == 1 else VC['snow']), ledges=True, mode='grade')
    for k in range(8):                                                     # rock roof over the road: tidy graded rows, darker (not loose pale blocks)
        off = 0.0 if var == 1 else 2.5                                     # var 2 offsets the row rhythm -> different silhouette
        A.chunk((5.2, 9.4, 4.0), (-17.5 + off + k * 5.0, 0.6, 14.4), strata([P['rock_d'], P['rock_m'], P['rock_m']], k, 2), (0, 0, 0), 0.06, rnd, (0.92, 0.95))
    A.box((L - 1.0, 9.6, 1.2), (0, 0.6, 12.0), P['rock_d'])                # continuous rock soffit ties the roof together
    for k in range(5):                                                     # thicker timber props on the open side
        x = -17.0 + k * 8.5
        A.box((1.4, 1.4, 12.6), (x, -4.6, 7.3), VC['timber'])
        A.beam((x, -4.6, 9.0), (x, -0.8, 12.4), 0.7, 0.7, VC['timber'])
        A.box((2.2, 2.2, 0.6), (x, -4.6, 1.2), VC['stone'])
    A.box((L - 2.0, 1.0, 1.0), (0, -4.6, 13.2), VC['timber'])
    A.box((L - 2.0, 0.35, 0.35), (0, -4.6, 3.6), VC['timber'])
    A.box((L - 2.0, 0.35, 0.35), (0, -4.6, 5.2), VC['timber'])
    if var == 2:                                                           # snow conforming over the roof chunks (stepped, not one flat plane)
        for k in range(8):
            A.chunk((5.6, 9.0, 1.2), (-17.5 + k * 5.0, 0.6, 16.9 + rnd.uniform(-0.3, 0.3)), VC['snow'], jit=0.1, rnd=rnd, taper=(0.8, 0.8))
    v4util.marker('mk_enda', (-L / 2, -1.0, 1.2))
    v4util.marker('mk_endb', (L / 2, -1.0, 1.2))
    v4util.marker('mk_deck', (0, -1.0, 1.2))
    return _fin(A, 'cliff_gallery')


def gallery_1():
    return _gallery(1)


def gallery_2():
    return _gallery(2)


# ================================================================= HM06 switchback walls (MAJOR checker / MINOR bland)
def _switchback(var):
    """Rebuilt switchback walls: graded strata stone (no light/dark checker), real block relief and coursing."""
    reset()
    A = Acc()
    rnd = random.Random(80 + var)
    if var == 1:                                                           # straight battered wall
        for k in range(10):
            for z in range(4):
                A.chunk((3.2, 4.6 - z * 0.25, 2.1), (-13.5 + k * 3.0, 0, 1.0 + z * 2.0), strata(GRADE, z, 1), (0, 0, 0), 0.08, rnd, (0.97, 0.9))
        A.box((30.4, 5.0, 0.7), (0, 0, 8.1), P['rock_l'])
        for k in range(8):                                                 # coping blocks for relief
            A.box((2.4, 1.4, 0.8), (-12.6 + k * 3.6, -2.2, 8.7), P['rock_m'], bev=0.08)
    elif var == 2:                                                         # curved retaining section, coursed
        R = 12.0
        for z in range(4):
            A.sweep([(R - 2.4 + z * 0.2, 1.8 + z * 2.0 - 1.0), (R + 2.4 - z * 0.2, 1.8 + z * 2.0 - 1.0), (R + 2.4 - z * 0.2, 1.8 + z * 2.0 + 1.0), (R - 2.4 + z * 0.2, 1.8 + z * 2.0 + 1.0)],
                    0, 180, 9, strata(GRADE, z, 1), loc=(0, 0, 0.0))
        for z in range(4):                                                 # proud course lips OUTSIDE the face (no coplanar z-fight)
            A.sweep([(R + 2.4 - z * 0.2, 1.8 + z * 2.0 + 0.7), (R + 2.9 - z * 0.2, 1.8 + z * 2.0 + 0.7), (R + 2.9 - z * 0.2, 1.8 + z * 2.0 + 1.1), (R + 2.4 - z * 0.2, 1.8 + z * 2.0 + 1.1)],
                    0, 180, 9, P['rock_l'], loc=(0, 0, 0.0))
        for z in range(4):                                                 # proud ashlar blocks on the outer curved face -> real masonry relief
            rr = R + 2.4 - z * 0.2
            for k in range(11):
                a = 8.0 + k * 16.0 + (8.0 if z % 2 else 0.0)
                if a > 178.0:
                    continue
                x, y, _ = polar(rr + 0.25, a)
                A.box((2.2, 0.5, 1.5), (x, y, 1.8 + z * 2.0), band(GRADE, (z + k) % 3 / 3.0, rnd), (0, 0, a - 90.0), bev=0.08)
        A.sweep([(R - 2.9, 8.2), (R + 2.9, 8.2), (R + 2.9, 8.9), (R - 2.9, 8.9)], 0, 180, 9, P['rock_l'])
        for k in range(7):
            x, y, _ = polar(R + 3.0, k * 30.0)
            A.box((0.6, 0.6, 1.4), (x, y, 9.6), VC['timber'], (0, 0, k * 30.0))
        for a in (-1, 1):
            A.chunk((4.8, 8.0, 8.2), (a * R, -4.0, 4.1), P['rock_m'], jit=0.05, rnd=rnd)
            A.box((5.2, 8.0, 0.7), (a * R, -4.0, 8.55), P['rock_l'])
    else:                                                                  # wall with a short stair and a parapet
        for k in range(10):
            for z in range(3):
                A.chunk((3.2, 4.4, 2.2), (-13.5 + k * 3.0, 0, 1.1 + z * 2.1), strata(GRADE, z, 1), (0, 0, 0), 0.07, rnd, (0.97, 0.92))
        for s in range(8):                                                 # deeper treads: lit tread + dark recessed riser
            A.box((2.0, 4.0, 0.6 * (s + 1)), (-14.0 + s * 2.0, -2.4, 0.3 * (s + 1)), P['rock_l'], bev=0.06)
            A.box((2.0, 0.4, 0.6), (-14.0 + s * 2.0 + 1.0, -4.2, 0.6 * (s + 1)), VC['slate'], bev=0)
        for sx in (-15.0, -13.0):                                          # stair side cheeks so the steps read
            A.box((0.8, 4.6, 5.2), (sx, -2.4, 2.6), P['rock_m'], bev=0.08)
        A.box((14.0, 0.7, 1.4), (7.0, 2.0, 8.0), P['rock_l'])
        for k in range(6):
            A.box((0.6, 0.6, 1.7), (1.5 + k * 2.1, 2.0, 7.3), VC['stone'])
        for k in range(10):                                                # coping blocks instead of one flat slab
            A.box((2.6, 4.8, 0.8), (-13.5 + k * 3.0, 0, 6.7), band(GRADE, (k % 3) / 3.0), bev=0.1)
    v4util.marker('mk_enda', (-14.0, 0, 0.5))
    v4util.marker('mk_endb', (14.0, 0, 0.5))
    return v5kit.fit(_fin(A, 'switchback_wall'), h=12.0)


def switchback_1():
    return _switchback(1)


def switchback_2():
    return _switchback(2)


def switchback_3():
    return _switchback(3)


# ================================================================= HM07_04 prayer flags (MINOR: washed out)
def flags_4():
    """Distinct strongly-coloured flag string (rebuild of ORIG var 4 which was near-white/ice): uses the vc_f colour set."""
    reset()
    A = Acc()
    rnd = random.Random(94)
    half = 18.5
    cols = [P['fr_a'], P['fr_b'], P['fr_c'], P['fr_d'], VC['f_white']]
    for sg in (-1, 1):
        A.chunk((2.6, 2.2, 1.0), (sg * half, 0, 0.5), VC['stone'], jit=0.08, rnd=rnd)
        A.cyl(0.32, 11.0, (sg * half, 0, 0.8), VC['timber'], verts=8, r2=0.24)
        A.ball(0.42, (sg * half, 0, 12.0), VC['gold'], segs=6, rings=4)
    z_end, sag = 10.4, 2.2
    zf = lambda x: z_end - sag * (1.0 - (x / half) ** 2)
    ORIG._cable(A, -half, half, 0.0, zf, VC['rope'], 0.12, 2.5)
    n = int(2 * half / 2.3)
    for k in range(1, n):
        x = -half + 2 * half * k / n
        A.box((1.1, 0.05, 1.5), (x, 0, zf(x) - 0.9), cols[k % 5], (rnd.uniform(-5, 5), 0, rnd.uniform(-4, 4)))
    return _fin(A, 'prayer_flag_string')


# ================================================================= HM08_02 cairn shrine (MAJOR: looks like a hut)
def shrine_2():
    """Rebuild as a whitewashed chorten/stupa (not a red-roof hut): stepped stone base, bumpa dome, square harmika, tapered spire, no roof gable."""
    reset()
    A = Acc()
    rnd = random.Random(102)
    # stepped square base
    for k, (w, h) in enumerate(((10.0, 1.4), (8.4, 1.4), (6.8, 1.4))):
        A.box((w, w, h), (0, 0, 0.7 + k * 1.4), P['whitewash'], bev=0.1)
    zb = 4.2
    A.box((6.0, 6.0, 1.0), (0, 0, zb + 0.5), P['band_r'])                  # ochre-red plinth band
    # bumpa (dome) - stacked whitewashed drums tapering to a dome
    A.cyl(3.4, 2.2, (0, 0, zb + 1.0), P['whitewash'], verts=16, r2=3.0)
    A.ball(3.0, (0, 0, zb + 3.2), P['whitewash'], segs=16, rings=8, scale=(1, 1, 0.8))
    zt = zb + 5.6
    A.box((2.6, 2.6, 1.6), (0, 0, zt), P['whitewash'], bev=0.08)           # harmika (square box)
    A.box((2.8, 2.8, 0.3), (0, 0, zt + 0.9), P['band_r'])                  # painted band
    # thirteen-ring tapered spire
    A.cyl(1.2, 2.6, (0, 0, zt + 0.9), P['band_r'], verts=12, r2=0.5)
    for k in range(5):
        A.sweep([(0.5 + 0.5 * (1 - k / 5.0), -0.12), (0.8 + 0.5 * (1 - k / 5.0), -0.12), (0.8 + 0.5 * (1 - k / 5.0), 0.12), (0.5 + 0.5 * (1 - k / 5.0), 0.12)],
                0, 360, 12, VC['gold'], loc=(0, 0, zt + 1.3 + k * 0.5))
    A.revolve([(0.6, 0.0), (0.6, 0.5), (0.9, 0.8), (0.0, 1.6)], (0, 0, zt + 3.5), VC['gold'], segs=10)  # sun-moon finial
    return _fin(A, 'cairn_shrine')


# ================================================================= NE01 village signs (MAJOR town1 / MINOR sand plinth)
def _sign(kind):
    """Rebuilt signs that clearly read as a notice board on a post with a legible board face."""
    reset()
    A = Acc()
    rnd = random.Random(40 + len(kind))
    if kind == 'town1':                                                    # stone-framed notice board on twin posts (was an 'organ')
        for sx in (-3.4, 3.4):
            A.chunk((2.0, 2.0, 1.0), (sx, 0, 0.5), VC['dstone'], jit=0.08, rnd=rnd)   # footing
            A.box((1.0, 1.0, 12.0), (sx, 0, 6.0), VC['stone'], bev=0.1)               # stone post
            A.box((1.3, 1.3, 0.8), (sx, 0, 12.2), VC['slate'], bev=0.08)              # post cap
        for p in range(5):                                                           # board built from vertical planks (relief, not one flat panel)
            A.box((1.5, 0.7 + (p % 2) * 0.2, 6.4), (-3.2 + p * 1.6, 0.1, 9.0), band([P['board'], VC['timber'], P['board']], p / 5.0))
        for zb in (12.0, 6.0):                                                       # proud carved border rails
            A.box((9.0, 1.1, 0.8), (0, -0.2, zb), VC['timber'], bev=0.08)
        for sx in (-4.3, 4.3):
            A.box((0.7, 1.1, 7.4), (sx, -0.2, 9.0), VC['timber'], bev=0.08)          # proud side border
        for k in range(3):                                                           # carved text lines (recessed dark, proud frame above)
            A.box((5.4 - k * 0.8, 0.3, 0.5), (0, -0.7, 10.6 - k * 1.6), VC['dstone'])
        A.box((8.8, 1.4, 1.6), (0, 0, 13.2), VC['slate'], bev=0.08)                   # pediment cap
        A.gable(9.4, 1.8, 1.6, (0, 0, 14.0), VC['red'], (0, 0, 90))                   # small shelter roof
    else:                                                                  # NE01_04 rusty-style: slim POST instead of a dominating sand wedge plinth
        for sx in (-3.6, 3.6):
            A.cyl(0.5, 13.0, (sx, 0, 0), VC['timber'], verts=8)            # slim posts (plinth removed)
            A.chunk((1.6, 1.6, 0.8), (sx, 0, 0.4), VC['sand'], jit=0.08, rnd=rnd)     # small footing stone only
        A.box((8.6, 0.5, 5.0), (0, -0.3, 9.4), VC['rust'])                 # salvage plate board
        A.box((9.0, 0.7, 0.6), (0, -0.3, 12.1), VC['iron'])
        A.box((9.0, 0.7, 0.6), (0, -0.3, 6.7), VC['iron'])
        for sx in (-3.0, 3.0):
            for sz in (7.4, 11.4):
                A.ball(0.3, (sx, -0.6, sz), VC['iron'], segs=6, rings=4)   # rivets
        A.box((4.8, 0.3, 2.6), (0, -0.6, 9.4), P['board'])                 # inset parchment/wood plaque (not blank white)
        for k in range(3):                                                 # carved text lines
            A.box((3.6 - k * 0.5, 0.2, 0.3), (0, -0.8, 10.2 - k * 0.8), VC['timber'])
        A.box((9.4, 0.8, 0.8), (0, 0, 13.2), VC['timber'])                 # top beam linking posts
    A.to_scene()
    ob = finalize('village_sign', 25)
    return v5kit.fit(ob, w=10.4, h=17.6)


def sign_1():
    return _sign('town1')


def sign_4():
    return _sign('rusty')


# ================================================================= NE02 entry boulder pairs (MINOR: stray patch / dark)
def _boulders(var):
    """Rebuilt entry boulder pairs: graded rock, accent moss/snow only as small conforming caps, no stray flat patches; var4 lightened to grey."""
    reset()
    A = Acc()
    rnd = random.Random(120 + var)
    if var == 4:
        main, accent, keys = P['rock_m'], P['rock_l'], [P['rock_d'], P['rock_m'], P['rock_m'], P['rock_l']]  # natural grey (was near-black basalt)
    elif var == 1:
        main, accent, keys = VC['stone'], VC['moss'], [P['rock_d'], VC['stone'], P['rock_w'], P['rock_l']]   # warmer natural stone, more tonal spread
    else:
        main, accent, keys = VC['stone2'], P['rock_l'], [P['rock_d'], VC['stone'], P['rock_w'], P['rock_l']]  # light-stone weather caps (no green patch)
    sep = 10.5 if var == 2 else 11.0                                       # var 2: taller narrower peaks, clear central gap -> gateway reads
    for sg in (-1, 1):
        cx = sg * sep
        if var == 2:                                                       # two distinct flanking towers (not a low scattered pile)
            h = 14.6 if sg < 0 else 12.8
            A.mound(cx, 0, 8.6, 8.6, h, 16, keys, rnd, 0.0, 0.5, 0.92, 0.12)
            A.chunk((6.2, 6.6, h * 0.7), (cx, 0, h * 0.35), main, jit=0.1, rnd=rnd)     # tall grounded core bridges z=0 to the peak
            A.chunk((7.4, 7.4, 3.4), (cx, 0, 1.3), keys[0], jit=0.12, rnd=rnd)          # grounded base boulder
            A.box((8.8, 8.4, 2.2), (cx, 0, 1.1), keys[0], bev=0.25)                     # wide footing on z=0
        else:
            h = 13.0 if sg < 0 else 11.0                                                # taller, clearly two peaks
            A.mound(cx, 0, 11.0, 11.0, h, 16, keys, rnd, 0.0, 0.42, 0.85, 0.14)
            A.chunk((8.0, 8.0, 3.2), (cx, 0, 1.2), main, jit=0.1, rnd=rnd)              # tall base chunk bridges ground to mound
            A.box((11.5, 11.0, 2.8), (cx, 0, 1.4), keys[0], bev=0.2)                    # wide flat footing: covers the mound footprint, grounded on z=0
        if var in (1, 2):                                                  # accent caps conform to the top (chunks, not flat slivers)
            for k in range(4):
                x = cx + rnd.uniform(-2.4, 2.4)
                y = rnd.uniform(-3.0, 1.0)
                zt = h * rnd.uniform(0.6, 0.9)
                A.chunk((rnd.uniform(2.0, 3.2), rnd.uniform(1.6, 2.6), 0.8), (x, y, zt + 0.3), accent, jit=0.12, rnd=rnd, taper=(0.7, 0.7))
    for k in range(4):                                                     # small stones between, road left clear
        A.chunk((rnd.uniform(1.0, 1.8), rnd.uniform(1.0, 1.8), rnd.uniform(0.6, 1.1)),
                (rnd.choice((-1, 1)) * rnd.uniform(5.4, 7.2), rnd.uniform(-5.0, 5.0), 0.4), main, jit=0.14, rnd=rnd)
    return v5kit.fit(_fin(A, 'entry_rock_pair'), w=31.0, d=22.0, h=14.6)


def boulders_1():
    return _boulders(1)


def boulders_2():
    return _boulders(2)


def boulders_4():
    return _boulders(4)


PBR = G.reg('vc_f', {
    'bronze': ((128, 96, 62), 'Metal', 0.3, 0.72),
    'rock_b': ((118, 104, 92), 'Slate', 0.0, 0.93),
    'rock_c': ((146, 128, 108), 'Cobblestone', 0.0, 0.92),
})


WARM = [P['rock_d'], PBR['rock_b'], PBR['rock_c'], P['rock_w'], P['rock_l']]


def _portal2():
    """HM03_02 (round 3, lead) - snow-capped tunnel portal: copy of ORIG._portal(2) with warm banded rock (not plain grey), NO icicles (the thin hanging cones rendered as black
    stripes across the opening), thicker snow caps that sink into the rock instead of lying on it as flat white slabs."""
    reset()
    A = Acc()
    rnd = random.Random(12)
    W, D, H, ow, oh = 30.0, 17.0, 24.0, 14.0, 16.0
    for sg in (-1, 1):
        for k in range(8):
            A.chunk((rnd.uniform(7.0, 8.4), D * rnd.uniform(0.85, 1.0), 3.4), (sg * (11.2 + rnd.uniform(-0.3, 0.4)), rnd.uniform(-0.8, 0.8), 1.6 + 3.0 * k),
                    band(WARM, k / 8.0, rnd), (0, 0, 0), 0.1, rnd, (0.94, 0.96))
    for k in range(6):
        A.chunk((5.8, D * rnd.uniform(0.9, 1.0), 7.4), (-12.5 + k * 5.0, rnd.uniform(-0.6, 0.6), oh + 4.3 + rnd.uniform(-0.2, 0.4)),
                band(WARM, 0.55 + 0.1 * (k % 3), rnd), (0, 0, 0), 0.08, rnd, (0.95, 0.95))
    A.box((ow, D, 0.4), (0, 0, 0.2), VC['slate'])
    for sg in (-1, 1):
        A.box((0.7, D, oh), (sg * (ow / 2 + 0.35), 0, oh / 2), VC['slate'])
    A.box((ow + 1.4, D, 0.8), (0, 0, oh + 0.4), VC['slate'])
    yf = -D / 2 + 0.3
    for sg in (-1, 1):
        A.box((1.5, 1.5, oh + 0.4), (sg * (ow / 2 + 0.75), yf, (oh + 0.4) / 2), VC['timber'])
        A.beam((sg * (ow / 2 + 0.75), yf - 0.2, oh - 3.6), (sg * (ow / 2 - 2.6), yf - 0.2, oh), 0.6, 0.6, VC['timber'])
    A.box((ow + 3.4, 1.7, 1.7), (0, yf, oh + 0.85), VC['timber'])
    for k in range(6):
        A.chunk((5.9, D * 0.92, 2.6), (-12.5 + k * 5.0, 0, H - 0.4), VC['snow'], (0, rnd.uniform(-3, 3), 0), 0.12, rnd, (0.9, 0.9))
    for sg in (-1, 1):
        A.chunk((7.4, D * 0.88, 2.2), (sg * 11.2, 0, 13.4), VC['snow'], (0, 0, 0), 0.12, rnd, (0.9, 0.9))
    v4util.marker('mk_door', (0, -D / 2, 0.3))
    A.to_scene()
    return finalize('tunnel_portal', 25)


def _shrine3():
    """HM08_03 (round 3, lead) - prayer-wheel shrine: four red corner posts joined by tie beams under the roof, a hub block between the wheel and the roof (the old roof sat on two
    thin posts with a wide gap to the drum and looked like it floated), dull bronze bands instead of bright gold."""
    reset()
    A = Acc()
    A.chunk((9.4, 9.4, 1.0), (0, 0, 0.5), VC['stone2'], jit=0.03, rnd=random.Random(103))
    for sx in (-3.6, 3.6):
        for sy in (-3.6, 3.6):
            A.box((0.8, 0.8, 7.4), (sx, sy, 4.7), VC['red'])
    for sx in (-3.6, 3.6):
        A.box((0.6, 7.6, 0.6), (sx, 0, 7.0), VC['red'])
    for sy in (-3.6, 3.6):
        A.box((7.6, 0.6, 0.6), (0, sy, 7.0), VC['red'])
    A.cyl(2.4, 5.0, (0, 0, 1.5), VC['red'], verts=16)
    for z in (1.7, 5.9):
        A.sweep([(2.3, 0.0), (2.65, 0.0), (2.65, 0.6), (2.3, 0.6)], 0, 360, 16, PBR['bronze'], loc=(0, 0, z))
    A.cyl(0.35, 9.0, (0, 0, 1.2), PBR['bronze'], verts=6)
    A.box((2.6, 2.6, 1.8), (0, 0, 7.4), VC['stone'])
    A.box((7.2, 0.6, 0.5), (0, 0, 7.4), VC['timber'])
    A.box((0.6, 7.2, 0.5), (0, 0, 7.4), VC['timber'])
    A.gable(9.4, 8.6, 2.6, (0, 0, 8.2), VC['slate'], (0, 0, 90))
    for k in range(8):
        x, y, _ = polar(2.45, k * 45.0)
        A.box((0.12, 0.5, 2.4), (x, y, 4.0), PBR['bronze'], (0, 0, k * 45.0))
    A.to_scene()
    return v5kit.fit(finalize('cairn_shrine', 25), w=12.8, d=12.0, h=12.4)


def _rope3_post(A):
    half = 58.0
    zd = lambda x: 5.0 - 2.4 * (1.0 - (x / half) ** 2)
    x = -half
    while x < half - 0.1:
        x2 = min(half, x + 5.8)
        for y in (-3.45, 3.45):
            A.beam((x, y, zd(x) - 0.95), (x2, y, zd(x2) - 0.95), 0.95, 0.85, VC['timber'])
            A.beam((x, y, zd(x) + 1.95), (x2, y, zd(x2) + 1.95), 0.55, 0.5, VC['timber'])
        x = x2
    for xx in range(int(-half), int(half) + 1, 8):
        for y in (-3.45, 3.45):
            A.box((0.6, 0.6, 2.2), (xx, y, zd(xx) + 0.9), VC['timber'], bev=0.04)


def _hall3_back(A):
    for r in range(2):
        for k in range(6):
            yb = 10.75 - r * 0.45
            A.box((2.2, 0.5, 3.0), (-11.0 + k * 4.4, yb, 5.4 + r * 10.0), VC['slate'])
            A.box((2.8, 0.5, 0.4), (-11.0 + k * 4.4, yb + 0.1, 7.1 + r * 10.0), VC['red'])
    A.box((4.0, 0.6, 6.0), (0, 10.95, 4.2), VC['timber'])
    for k in range(12):
        A.box((1.4, 0.7, 1.1), (-13.0 + k * 2.4, 10.5, 22.8), VC['white'])
    for st in range(3):
        A.box((8.0 - st * 1.6, 1.6, 0.4 * (st + 1)), (0, 12.2 - st * 1.0 + 0.0, 1.2 + 0.2 * (st + 1)), VC['stone'])


def _switch3_post(A):
    A.box((30.2, 5.0, 0.6), (0, 0, 7.45), P['rock_l'])
    A.box((30.4, 1.2, 0.3), (0, -2.65, 7.4), P['rock_m'], bev=0.05)
    for z in (2.1, 4.2):
        A.box((30.4, 0.5, 0.45), (0, -2.45, z), P['rock_l'], bev=0.04)
    A.box((29.0, 2.6, 0.15), (0, 0.4, 7.82), VC['stone2'])


RAMP_A = [PBR['rock_b'], PBR['rock_c'], P['rock_w'], P['rock_l']]


RAMP_B = [PBR['rock_b'], PBR['rock_c'], P['rock_w'], P['rock_l'], P['rock_w']]


RAMP_C = [PBR['rock_b'], P['rock_m'], PBR['rock_c'], P['rock_w']]


STONE3 = [VC['stone'], VC['stone2'], VC['slate']]


def hm01_03():
    return LK.wrap(ORIG.rope_bridge_3, post=_rope3_post)()


def hm02_01():
    return LK.wrap(ORIG.cantilever_1, recolor=[LK.ramp([VC['stone'], VC['stone2']], RAMP_A, zlim=(-1.0, 7.4), trange=(0.0, 7.0), wobble=0.08)])()


def hm02_02():
    return LK.wrap(ORIG.cantilever_2, recolor=[LK.ramp([VC['stone'], VC['stone2']], RAMP_C, zlim=(-1.0, 7.4), trange=(0.0, 7.0), wobble=0.08),
                                               LK.ramp([VC['slate']], [P['band_r']], zlim=(9.0, 30.0))])()


def hm03_01():
    return LK.wrap(ORIG.portal_1, recolor=[LK.ramp(STONE3, RAMP_A, trange=(0.0, 24.0), wobble=0.07)])()


def hm03_03():
    return LK.wrap(ORIG.portal_3, recolor=[LK.ramp(STONE3, RAMP_B, trange=(0.0, 24.0), wobble=0.07)])()


def hm06_03():
    return LK.wrap(lambda: _switchback(3), post=_switch3_post)()


def hm08_01():
    return LK.wrap(ORIG.shrine_1, post=_flags1_post, prune=[dict(keys=[VC['f_blue'], VC['f_white'], VC['f_red'], VC['f_green'], VC['f_yellow']], max_size=3.0)],
                   recolor=[LK.ramp(STONE3, RAMP_A, zlim=(-1.0, 11.5), trange=(0.0, 11.0), wobble=0.08)])()


def hm09_03():
    return LK.wrap(ORIG.outpost_3, post=_hall3_back)()


def ne01_03():
    return LK.wrap(ORIG.sign_3, recolor=[LK.ramp([VC['white']], [P['board']]), LK.ramp([VC['snow']], [P['rock_m']], zlim=(-1.0, 1.4))])()


def ne02_03():
    return LK.wrap(lambda: _boulders(3), recolor=[LK.ramp([P['rock_d']], [PBR['rock_b'], PBR['rock_c']], trange=(0.0, 14.0), wobble=0.1)])()


def _flags1_post(A):
    for k, key in enumerate((VC['f_red'], VC['f_yellow'], VC['f_blue'])):
        A.box((1.5, 0.12, 0.7), (0.85, 0.0, 13.5 - k * 0.85), key, bev=0.02)


BATCHES = {
    'tunnels': ('v5_himalaya', mk([
        ('HM04_01_tunnel_lining_01', lining_1),
        ('HM04_02_tunnel_lining_02', lining_2)], 0.1)),
    'road_extras': ('v5_himalaya', mk([
        ('HM05_01_cliff_gallery_01', gallery_1),
        ('HM05_02_cliff_gallery_02', gallery_2),
        ('HM06_01_switchback_wall_01', switchback_1),
        ('HM06_02_switchback_wall_02', switchback_2),
        ('HM06_03_switchback_wall_03', switchback_3),
        ('HM07_04_prayer_flag_string_04', flags_4),
        ('HM08_02_cairn_shrine_02', shrine_2)], 0.1)),
    'signs': ('v5_entrances', mk([
        ('NE01_01_village_sign_01', sign_1),
        ('NE01_04_village_sign_04', sign_4)], 0.1)),
    'boulders': ('v5_entrances', mk([
        ('NE02_01_entry_rock_pair_01', boulders_1),
        ('NE02_02_entry_rock_pair_02', boulders_2),
        ('NE02_04_entry_rock_pair_04', boulders_4)], 0.1)),
}


# --- lead3 registration ---
BATCHES['lead3'] = ('v5_himalaya', mk([('HM03_02_tunnel_portal_02', _portal2), ('HM08_03_cairn_shrine_03', _shrine3)], 0.1))


# --- lead4 registration ---
import v5_leadkit as LK
BATCHES['lead4'] = ('v5_himalaya', mk([('HM01_03_rope_suspension_bridge_03', hm01_03), ('HM02_01_timber_cantilever_bridge_01', hm02_01), ('HM02_02_timber_cantilever_bridge_02', hm02_02),
                                       ('HM03_01_tunnel_portal_01', hm03_01), ('HM03_03_tunnel_portal_03', hm03_03), ('HM04_02_tunnel_lining_02', lining_2),
                                       ('HM06_03_switchback_wall_03', hm06_03), ('HM08_01_cairn_shrine_01', hm08_01), ('HM09_03_monastery_outpost_03', hm09_03)], 0.1))
BATCHES['lead4_ent'] = ('v5_entrances', mk([('NE01_03_village_sign_03', ne01_03), ('NE02_03_entry_rock_pair_03', ne02_03)], 0.1))
