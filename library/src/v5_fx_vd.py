"""v5_fx_vd - FIX ROUND builders for assignment A5 (the capital). Owner: builder A5. Replaces the round-1 builders of the vd ids in library\\v5_work\\fix\\assign_A5.md.
Same worker (vd) and same category folders as round 1, so the files and the vd_ fragments are overwritten in place after archiving.
NEW palette keys only, under the prefix vd_f_ (never re-register a round-1 key name with another colour).
No glow, no emissive, no freestanding entrance arch. Front faces -Y, pivot at the bottom centre.
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v4util
import v5kit
from v5kit import Acc, polar, tang, mk, ids, band, strata
import v5gen as G
from v5gen import house, round_tower, wall_seg, column
import v5_vd as ORIG          # round-1 module: reuse its palette dict K and helpers, never edit it

K = ORIG.K                    # round-1 capital palette (wall, stone, roof, trim, cone, ...)

# a few extra stone tones so rebuilt walls get real tonal variation (graded, never a checker)
P = G.reg('vd_f', {
    'stone_d': ((126, 120, 134), 'Slate', 0.0, 0.93),      # darker course stone (base / shadow bands)
    'stone_l': ((168, 160, 174), 'Slate', 0.0, 0.92),      # lighter course stone
    'coping': ((150, 142, 158), 'Slate', 0.0, 0.9),        # stone coping cap (replaces the grass-green strip)
    'brown': ((120, 86, 58), 'Wood', 0.0, 0.9),            # timber crate / tank body accent
})
STONES = [P['stone_d'], K['stone'], P['stone_l']]           # bottom -> top grade


def _fin(A, name):
    A.to_scene()
    return finalize(name, 25)


# ================================================================= CP02 corner (MAJOR: floating slit bars + gap)
def _corner(angle, seed):
    """Rebuild of ORIG._corner: wall_seg battlement=True on the free end only, no stray slits hanging past the join, tower seated into the arms."""
    reset()
    A = Acc()
    rnd = random.Random(seed)
    arm = Acc()
    wall_seg(arm, rnd, 16.0, 16.0, 9.0, K, 8.0, 0, 0, 7.0, False, False, battlement=False)   # slits=False; own merlons below
    arm.box((16.0, 3.2, 1.6), (8.0, -5.6, 15.6), K['wall'], bev=0.06)      # crest capstone bridges frustum top to merlons
    for k in range(4):                                                     # merlons embedded on the capstone
        x = 8.0 - 8.0 + 2.0 + k * 4.0
        arm.box((2.4, 1.8, 3.0), (x, -6.3, 16.0 + 1.2), K['wall'], bev=0.08)
        arm.box((2.7, 2.1, 0.4), (x, -6.3, 16.0 + 2.8), K['cap'], bev=0.06)
    A.append(arm)
    A.append(arm, rot=(0, 0, angle), scale=(1, -1, 1))
    # fill the inner wedge between the two arms so there is no gap to the tower
    A.cyl(8.2, 9.0, (0, 0, 0), K['stone'], verts=24, r2=7.4)
    t = Acc()
    round_tower(t, rnd, 7.4, 20.0, K, 0, 0, 0, top='crenel', slits=2, bands=2)
    A.append(t, (0, 0, 0))
    return _fin(A, 'ring_wall_corner')


def corner_2():
    return _corner(90, 12)


# ================================================================= CP01 straight wall (MINOR: clone of 01/03)
def wall_2():
    """Arrow-slit variant made genuinely different from 01/03: tighter merlon spacing, double string course, slits that sit flush in the face."""
    reset()
    A = Acc()
    rnd = random.Random(777)
    L, h, t = 40.0, 16.0, 9.0
    A.box((L + 0.6, t + 1.6, 1.8), (0, 0, 0.9), K['stone'])
    A.frustum((L, t), (L, t - 1.6), h - 1.8, (0, 0, 1.8), K['wall'])
    for k in range(4):                                                     # four graded string courses (01/03 have 3)
        zz = 1.8 + (h - 1.8) * (k + 1) / 5.0
        for sg in (-1, 1):
            A.box((L + 0.2, 0.4, 0.45), (0, sg * (t / 2 - 0.5), zz), band(STONES, k / 4.0), bev=0)
    for r in range(4):                                                     # proud ashlar blocks on the outer (-Y) face -> real masonry relief
        zz = 2.6 + r * 3.0
        for c in range(13):
            bx = -L / 2 + 1.5 + c * 3.0 + (1.5 if r % 2 else 0.0)
            if abs(bx) > L / 2 - 1.0:
                continue
            A.box((2.6, 0.5, 2.2), (bx, -t / 2 + 0.2, zz), band(STONES, (r + c) % 3 / 3.0, rnd), bev=0.1)
    A.box((L, 8.0, 0.7), (0, (t - 8.0) / 2, h + 0.15), K['deck'])
    A.box((L + 0.3, 1.0, 1.7), (0, t / 2 - 0.5, h + 1.15), K['wall'])
    A.box((L + 0.5, 1.3, 0.4), (0, t / 2 - 0.5, h + 2.15), P['coping'], bev=0.06)
    n = int(L / 3.2)                                                       # tighter merlon spacing (3.2 vs 4.0)
    for k in range(n):
        x = -L / 2 + 1.6 + k * 3.2
        A.box((1.9, 1.2, 2.2), (x, -t / 2 + 0.6, h + 1.55), K['wall'], bev=0.08)
        A.box((2.1, 1.5, 0.4), (x, -t / 2 + 0.6, h + 2.8), P['coping'], bev=0.06)
    for k in range(5):                                                     # arrow slits recessed into the outer face (flush, not protruding)
        x = -L / 2 + 6.0 + k * 8.0
        A.box((0.7, 0.9, 3.6), (x, -t / 2 + 0.6, h * 0.55), K['dark'], bev=0)
        A.box((1.5, 0.6, 0.5), (x, -t / 2 + 0.35, h * 0.55 + 2.0), K['trim'], bev=0)
    return _fin(A, 'ring_wall_straight')


# ================================================================= CP03 stair end (MINOR: stray bar on merlon)
def stair_end_2():
    """Copy of ORIG._stair_end(1) without the stray diagonal timber handrail beam that pokes past the merlons."""
    reset()
    A = Acc()
    rnd = random.Random(22)
    wall_seg(A, rnd, 20.0, 16.0, 9.0, K, 0, 0, 0, 7.0, False, False, battlement=False)
    for k in range(int(20.0 / 4.0)):                                       # merlons seated on the wall crest (z=16)
        x = -10.0 + 2.0 + k * 4.0
        A.box((2.4, 1.6, 2.6), (x, -3.6, 16.0 + 1.3), K['wall'], bev=0.08)
        A.box((2.7, 1.9, 0.4), (x, -3.6, 16.0 + 2.6), K['cap'], bev=0.06)
    s = -1
    for i in range(14):
        A.box((1.5, 3.4, 1.2 * (i + 1)), (s * (-9.0 + i * 1.3), 7.4, 0.6 * (i + 1)), K['stone'], bev=0.08)
    A.box((19.0, 0.6, 0.5), (0, 9.4, 1.0), K['trim'])
    for i in range(0, 14, 3):                                              # short vertical balusters seated on the steps
        A.beam((s * (-9.0 + i * 1.3), 7.6, 1.2 * (i + 1)), (s * (-9.0 + i * 1.3), 7.6, 1.2 * (i + 1) + 2.0), 0.4, 0.4, K['timber'])
    round_tower(A, rnd, 2.8, 22.0, K, s * 11.0, -0.5, 0, top='crenel', slits=1, bands=1, verts=14)
    return _fin(A, 'ring_wall_stair_end')


# ================================================================= CP05 turret (MAJOR: black spikes clip the cone)
def turret_2():
    """Crenellated turret with a cone roof: iron finials become short gold roof-ridge finials seated ON the cone, none clipping/floating."""
    reset()
    A = Acc()
    round_tower(A, random.Random(42), 6.5, 18.0, K, top='crenel', slits=2, bands=1, verts=16)
    # cone roof seated on the crenel ring
    A.cyl(7.6, 7.0, (0, 0, 19.0), K['cone'], verts=16, r2=0.0)
    for k in range(1, 5):                                                  # tile course rings on the cone
        t = k / 5.0
        A.sweep([(7.6 * (1 - t) - 0.2, -0.15), (7.6 * (1 - t) + 0.25, -0.15), (7.6 * (1 - t) + 0.25, 0.15), (7.6 * (1 - t) - 0.2, 0.15)],
                0, 360, 16, K['cap'], loc=(0, 0, 19.0 + 7.0 * t))
    A.revolve([(0.5, 0.0), (0.5, 1.2), (0.9, 1.5), (0.0, 2.4)], (0, 0, 26.0), K['gold'], segs=8)
    return v5kit.fit(_fin(A, 'turret_crenellated'), h=26.0)


# ================================================================= CP06 gate flank towers (MINOR: banner off wall)
def _flank(seed, cone):
    """Copy of ORIG._flank with the banner snapped flush to the tower wall face (no gap)."""
    reset()
    A = Acc()
    rnd = random.Random(seed)
    round_tower(A, rnd, 14.0, 40.0, K, top='cone' if cone else 'crenel', slits=3, bands=3, roof_k=0.9, flag=cone, verts=28)
    for sg in (-1, 1):
        x, y, _ = polar(14.0, 270 + sg * 24.0)                            # on the wall radius, not 1.25x out
        nx, ny, _ = polar(1.0, 270 + sg * 24.0)
        A.beam((x, y, 30.0), (x + nx * 0.6, y + ny * 0.6, 30.5), 0.4, 0.4, K['iron'])
        A.box((0.25, 3.0, 8.0), (x + nx * 0.35, y + ny * 0.35, 26.0), K['flag'], (0, 0, 270 + sg * 24.0), bev=0)
    return _fin(A, 'gate_flank_tower')


def flank_1():
    return _flank(51, True)


def flank_2():
    return _flank(52, False)


# ================================================================= CP11 great hall / chapel (MAJOR: floating gable)
def hall_1():
    """Rebuild of ORIG.hall_chapel(1): the louvred lantern stays, every roof/wall piece seated; no detached gable triangle above the ridge."""
    reset()
    A = Acc()
    rnd = random.Random(91)
    ORIG._stone_block(A, rnd, 60.0, 30.0, 26.0, 0, 0, 0, 2, True, True)
    A.gable(32.0, 62.0, 16.0, (0, 0, 26.0), K['roof'], (0, 0, 90))
    G.roof_lines(A, 32.0, 62.0, 16.0, (0, 0, 26.0), K['roof2'], n=5, rot_z=90.0)
    A.box((6.0, 6.0, 8.0), (0, 0, 39.5), K['wall'])                       # lantern box seated down into the ridge (36.5..43.5)
    A.cyl(4.6, 6.0, (0, 0, 43.4), K['cone'], verts=6, r2=0.0)             # cone base flush on the box top (no gap)
    for sg in (-30.0, 30.0):
        round_tower(A, rnd, 5.0, 34.0, K, sg, -15.0, 0, top='cone', roof_k=1.5, verts=16)
    A.box((12.0, 4.0, 9.0), (0, -17.0, 4.5), K['timber'], bev=0.1)
    return _fin(A, 'hall_chapel')


# ================================================================= CP12 terrace retaining walls (MAJOR/MINOR: camo + green cap)
def terrace_wall_s():
    """Straight retaining wall: one graded stone (strata), real block relief, stone coping (no green grass strip, no square camo)."""
    reset()
    A = Acc()
    rnd = random.Random(101)
    for k in range(10):
        for z in range(5):
            A.chunk((4.2, 7.0 - z * 0.4, 4.6), (-18.0 + k * 4.0, 0, 2.3 + z * 4.3),
                    strata(STONES, z, 1), (0, 0, 0), 0.06, rnd, (0.97, 0.93))   # strata grade, not (k+z)%3 checker
    A.box((41.0, 8.0, 0.9), (0, 0, 22.0), K['trim'])
    A.box((41.0, 7.2, 0.6), (0, 0, 22.9), P['coping'], bev=0.08)                # stone coping, not grass
    for k in range(9):                                                          # buttress ribs for relief
        A.box((1.6, 1.6, 6.0), (-18.0 + k * 4.5, -3.8, 12.0), K['stone'], bev=0.1)
    return _fin(A, 'terrace_retaining_wall')


def terrace_wall_c():
    """Curved retaining wall: graded strata, a chamfered course line for relief, stone coping (no green strip)."""
    reset()
    A = Acc()
    R = 24.0
    for z in range(5):
        A.sweep([(R - 4.0 + z * 0.3, z * 4.3), (R + 4.0 - z * 0.3, z * 4.3), (R + 4.0 - z * 0.3, z * 4.3 + 4.4), (R - 4.0 + z * 0.3, z * 4.3 + 4.4)],
                0, 90, 9, strata(STONES, z, 1))
        A.sweep([(R - 4.2 + z * 0.3, z * 4.3 + 2.1), (R + 4.2 - z * 0.3, z * 4.3 + 2.1), (R + 4.2 - z * 0.3, z * 4.3 + 2.4), (R - 4.2 + z * 0.3, z * 4.3 + 2.4)],
                0, 90, 9, K['trim'])                                            # course line relief
    A.sweep([(R - 4.0, 21.5), (R + 4.0, 21.5), (R + 4.0, 22.4), (R - 4.0, 22.4)], 0, 90, 9, K['trim'])
    A.sweep([(R - 3.4, 22.4), (R + 3.4, 22.4), (R + 3.4, 23.0), (R - 3.4, 23.0)], 0, 90, 9, P['coping'])
    for a in (8, 30, 52, 74):
        x, y, _ = polar(R + 4.4, a)
        A.box((1.6, 1.6, 17.0), (x, y, 9.0), K['stone'], (0, 0, a), bev=0.1)
    return _fin(A, 'terrace_retaining_wall')


# ================================================================= CP14 skyline towers (MINOR: stray rail / teal patch)
def sky_beacon():
    """Copy of ORIG.sky_beacon with the rooftop rail frame re-seated on the deck (closed box frame, nothing floating)."""
    reset()
    A = Acc()
    ORIG._shaft(A, 13.0, 84.0, 0.0, K['stone'], 6)
    A.box((18.0, 18.0, 1.2), (0, 0, 85.0), K['trim'])
    A.cyl(2.2, 12.0, (0, 0, 80.0), K['stone'], verts=8)                   # neck ties the deck to the shaft top
    for sx in (-1, 1):
        for sy in (-1, 1):
            A.box((0.9, 0.9, 6.4), (sx * 8.0, sy * 8.0, 88.2), K['iron'], bev=0.05)   # posts sit on the 85.6 deck top
    for z in (87.0, 91.0):                                                 # rails span post to post (shortened to 16, flush)
        for sg in (-1, 1):
            A.box((16.0, 0.4, 0.4), (0, sg * 8.0, z), K['iron'], bev=0)
            A.box((0.4, 16.0, 0.4), (sg * 8.0, 0, z), K['iron'], bev=0)
    A.cyl(3.0, 2.0, (0, 0, 86.2), K['iron'], verts=8, r2=4.4)              # brazier bowl, unlit
    for k in range(7):
        x, y, _ = polar(2.2, k * 51.4)
        A.cyl(0.4, 3.5 + (k % 3), (x, y, 88.0), K['dark'], verts=5, r2=0.1)
    A.frustum((18.0, 18.0), (6.0, 6.0), 3.0, (0, 0, 93.0), K['cone'])
    return _fin(A, 'skyline_tower_beacon')


def sky_water():
    """Copy of ORIG.sky_water with the tank body all one timber tone (no teal/copper patch on the tank itself)."""
    reset()
    A = Acc()
    for sx in (-1, 1):
        for sy in (-1, 1):
            A.beam((sx * 11.0, sy * 11.0, 0.0), (sx * 7.0, sy * 7.0, 56.0), 2.0, 2.0, K['timber'])
            A.cyl(2.2, 1.2, (sx * 11.0, sy * 11.0, 0.0), K['stone'], verts=8)
    for z in (14.0, 28.0, 42.0):
        for sg in (-1, 1):
            A.beam((-10.0, sg * (11.0 - 4.0 * z / 56.0), z), (10.0, sg * (11.0 - 4.0 * z / 56.0), z), 1.0, 1.0, K['timber'])
            A.beam((sg * (11.0 - 4.0 * z / 56.0), -10.0, z), (sg * (11.0 - 4.0 * z / 56.0), 10.0, z), 1.0, 1.0, K['timber'])
        A.beam((-9.5, -9.5, z - 14.0), (9.5, 9.5, z), 0.6, 0.6, K['iron'])
        A.beam((9.5, -9.5, z - 14.0), (-9.5, 9.5, z), 0.6, 0.6, K['iron'])
    A.cyl(13.0, 2.0, (0, 0, 56.0), K['timber'], verts=16)
    A.cyl(2.0, 58.0, (0, 0, 0.0), K['timber'], verts=8)                   # central mast grounds the tank to the base
    A.cyl(13.0, 22.0, (0, 0, 58.0), K['timber'], verts=20, r2=12.0)        # tank body: timber
    for k in range(5):
        A.sweep([(12.4, -0.3), (13.4, -0.3), (13.4, 0.3), (12.4, 0.3)], 0, 360, 20, K['iron'], loc=(0, 0, 60.0 + k * 4.5))  # iron bands
    A.cyl(14.5, 12.0, (0, 0, 80.0), K['cone'], verts=20, r2=0.0)
    A.cyl(0.4, 6.0, (0, 0, 91.5), K['iron'], verts=6)
    A.beam((13.0, 0, 62.0), (13.0, 0, 20.0), 1.4, 1.4, K['timber'])        # downpipe: timber, not copper patch
    A.beam((13.0, 0, 20.0), (14.5, 0, 18.0), 1.0, 1.0, K['timber'])
    return _fin(A, 'skyline_tower_water')


# ================================================================= CP15_03 order HQ (MAJOR: crude octagon + floating box)
def hq_3():
    """Rebuild to landmark detail (like CP15_01/02): octagonal reading hall with pilasters, window bays, a banded drum,
    a tiled lantern roof and a seated entrance porch + stair. No stray brown box in front."""
    reset()
    A = Acc()
    rnd = random.Random(133)
    R = 20.0
    A.cyl(R + 1.8, 2.4, (0, 0, 0), K['stone'], verts=8, r2=R + 1.4)        # battered plinth
    A.cyl(R, 24.0, (0, 0, 2.4), K['wall'], verts=8, r2=R - 1.2)            # main octagon body
    for z in (9.0, 17.0):                                                  # two string courses for relief
        A.cyl(R + 0.3, 0.7, (0, 0, z), K['trim'], verts=8)
    for k in range(8):
        a = 22.5 + 45.0 * k
        x, y, _ = polar(R - 1.2, a)
        if k != 5:                                                         # 7 window bays, one face is the entrance
            A.box((1.4, 5.0, 11.0), (x, y, 11.0), K['glass'], (0, 0, a), bev=0)   # deep enough to embed in the drum
            A.box((1.8, 6.2, 0.7), (x, y, 17.0), K['trim'], (0, 0, a), bev=0)     # lintel
            A.box((1.8, 6.2, 0.7), (x, y, 5.0), K['stone'], (0, 0, a), bev=0)     # sill
        px, py, _ = polar(R - 0.8, a - 22.5)                               # pilaster embedded on every corner
        A.box((2.0, 2.0, 24.0), (px, py, 14.4), K['stone'], (0, 0, a - 22.5), bev=0.08)
    A.cyl(R + 1.2, 1.4, (0, 0, 26.4), K['trim'], verts=8)                  # cornice
    A.cyl(R + 0.4, 10.0, (0, 0, 27.8), K['cone'], verts=8, r2=7.0)         # tiled octagon roof
    for k in range(1, 4):
        t = k / 4.0
        A.cyl((R + 0.4) * (1 - t) + 7.0 * t + 0.25, 0.4, (0, 0, 27.8 + 10.0 * t), K['cap'], verts=8)
    A.cyl(7.0, 2.0, (0, 0, 37.8), K['trim'], verts=8)                      # lantern
    A.cyl(6.0, 6.0, (0, 0, 39.8), K['wall'], verts=8, r2=5.5)
    for k in range(8):
        x, y, _ = polar(5.6, 22.5 + 45.0 * k)
        A.box((0.5, 2.0, 3.2), (x, y, 42.0), K['glass'], (0, 0, 22.5 + 45.0 * k), bev=0)
    A.cyl(6.6, 7.0, (0, 0, 45.8), K['cone'], verts=8, r2=0.0)
    A.revolve([(0.5, 0.0), (0.5, 1.4), (1.0, 1.8), (0.0, 3.2)], (0, 0, 52.8), K['gold'], segs=8)
    # seated entrance porch on the -Y face (k==5 -> a=22.5+225=247.5; front is 270, use the -Y bay)
    A.box((10.0, 6.0, 12.0), (0, -R - 1.5, 6.0), K['stone'], bev=0.1)      # porch block flush against the wall
    A.gable(11.0, 7.0, 4.0, (0, -R - 1.5, 12.0), K['roof'], (0, 0, 90))
    A.box((4.0, 1.0, 7.0), (0, -R - 4.6, 3.5), K['door'], bev=0.05)
    for i in range(5):                                                     # entrance stair, seated to the ground
        A.box((12.0 - i * 1.4, 1.6, 1.0), (0, -R - 5.0 - i * 1.2, 0.5 - i * 0.0 + i * 0.0), K['stone'], bev=0.08)
    # a flanking round tower like the other annexes (no floating box)
    round_tower(A, rnd, 6.0, 40.0, K, -R - 4.0, 8.0, 0, top='cone', roof_k=1.4, verts=16, flag=True)
    return _fin(A, 'order_hq')


# ================================================================= CP16_01 townhouse (MINOR: canopy off facade)
def town_corner():
    """Rebuild of ORIG._town('corner'): house() draws the entry hood flush; keep the corner L-plan, nothing floating."""
    reset()
    A = Acc()
    rnd = random.Random(200)
    house(A, rnd, 18.0, 13.0, 2, K, cx=0, cy=0, hs=6.2, jetty=0.9, pitch=0.7, sign=False, balcony=True)
    house(A, rnd, 12.0, 17.0, 2, K, cx=8.0, cy=12.0, hs=6.2, jetty=0.9, pitch=0.7, ridge_x=False, chimney=False, door=False)
    return _fin(A, 'townhouse_new')


# ================================================================= CP18 quay walls (MAJOR/MINOR: camo patches)
def _quay(kind):
    """Rebuilt quay walls: ONE graded stone (strata, no two-tone checker), relief from a coping course + real geometry (bollards, steps, chimney)."""
    reset()
    A = Acc()
    rnd = random.Random(300 + len(kind))
    if kind == 'curve':
        R = 22.0
        for z in range(3):
            A.sweep([(R - 3.0, z * 2.8), (R + 1.0, z * 2.8), (R + 1.0, z * 2.8 + 2.9), (R - 3.0, z * 2.8 + 2.9)], 0, 80, 8, strata(STONES, z, 1))
        for z in range(3):                                                 # proud course lips (sit OUTSIDE the face, no coplanar z-fight)
            A.sweep([(R + 1.0, z * 2.8 + 2.4), (R + 1.5, z * 2.8 + 2.4), (R + 1.5, z * 2.8 + 2.9), (R + 1.0, z * 2.8 + 2.9)], 0, 80, 8, P['coping'])
        A.sweep([(R - 3.4, 8.4), (R + 1.4, 8.4), (R + 1.4, 9.2), (R - 3.4, 9.2)], 0, 80, 8, P['coping'])
        for k in range(4):                                                 # bollards as relief
            x, y, _ = polar(R - 1.0, 12 + k * 18.0)
            A.cyl(0.6, 2.4, (x, y, 9.2), K['timber'], verts=8)
            A.ball(0.7, (x, y, 11.7), K['iron'], segs=6, rings=4)
    else:
        for k in range(10):
            for z in range(3):
                A.chunk((3.2, 4.0, 2.9), (-13.5 + k * 3.0, 0, 1.45 + z * 2.8), strata(STONES, z, 1), (0, 0, 0), 0.05, rnd)
        A.box((30.6, 4.8, 0.8), (0, 0, 8.8), K['trim'])
        A.box((30.8, 5.0, 0.5), (0, 0, 9.4), P['coping'], bev=0.06)        # coping course
        if kind == 'steps':
            for i in range(7):                                             # real risers + side cheeks
                A.box((8.0, 1.3, 1.2), (0, -2.8 - i * 1.0, 8.4 - 1.2 * (i + 1) + 0.6), K['stone'], bev=0.06)
            for sx in (-1, 1):
                A.box((0.8, 8.0, 8.4), (sx * 4.4, -5.0, 4.2), K['stone'], bev=0.08)
        if kind == 'posts':
            for k in range(5):
                A.cyl(0.55, 3.2, (-12.0 + k * 6.0, -1.4, 9.2), K['timber'], verts=8)
                A.ball(0.7, (-12.0 + k * 6.0, -1.4, 12.5), K['iron'], segs=6, rings=4)
        if kind == 'straight':
            A.box((6.0, 3.6, 6.0), (10.0, -0.2, 6.0), K['stone'], bev=0.1)   # chimney/bollard block as geometry
            A.box((6.6, 4.2, 0.6), (10.0, -0.2, 9.3), K['trim'])
            for k in range(4):                                             # mooring cleats
                A.cyl(0.35, 0.6, (-12.0 + k * 7.0, -2.5, 9.6), K['iron'], verts=8, rot=(90, 0, 0))
    return _fin(A, 'quay_wall')


# ================================================================= CP08 water gate (MAJOR never-rebuilt: flat white roof reads as a light panel)
def water_gate():
    """Rebuild of ORIG.water_gate: the flat bright-white trim roof slab is replaced by a muted tile-tone battlemented parapet roof
    with a ridge and stepped merlons; the vaulted gate (allowed on a CP gate) stays."""
    reset()
    A = Acc()
    rnd = random.Random(62)
    W, D, H, ow, oh = 40.0, 30.0, 30.0, 16.0, 9.0
    ORIG._portal_block(A, rnd, W, D, H, ow, oh, K)
    yf = -D / 2.0
    A.box((ow, D + 2.0, 1.0), (0, 0, 3.5), K['dark'])
    for k in range(9):                                                     # iron grille over the channel
        A.box((0.4, 0.4, oh + 6.0), (-6.4 + k * 1.6, yf + 2.0, 3.0 + (oh + 6.0) / 2.0), K['iron'], bev=0)
    for z in (6.0, 9.5, 13.0):
        A.box((ow, 0.4, 0.4), (0, yf + 2.0, z), K['iron'], bev=0)
    # --- muted tile roof (no flat white slab) ---
    A.box((W + 1.0, D + 1.0, 1.2), (0, 0, H + 0.6), K['roof'])             # tile-tone roof deck
    A.box((W + 1.4, D + 1.4, 0.5), (0, 0, H + 1.4), K['cap'], bev=0.1)     # darker tile coping lip
    A.gable(W - 6.0, D + 1.0, 3.0, (0, 0, H + 1.2), K['roof2'], (0, 0, 90))   # low central ridge breaks the flat top
    for k in range(int(W / 4.0)):                                          # stepped merlons on both long edges (relief)
        x = -W / 2.0 + 2.0 + k * 4.0
        for sy in (-1, 1):
            A.box((2.4, 1.3, 2.2), (x, sy * (D / 2.0 - 0.4), H + 2.3), K['wall'], bev=0.08)
            A.box((2.7, 1.6, 0.4), (x, sy * (D / 2.0 - 0.4), H + 3.5), K['cap'], bev=0.06)
    for k in range(int(W / 4.0)):                                          # machicolation corbels under the front parapet
        x = -W / 2.0 + 2.0 + k * 4.0
        A.box((1.4, 1.4, 1.4), (x, yf - 0.6, H - 0.6), K['stone'], bev=0.06)
    for sg in (-1, 1):
        A.box((3.0, 14.0, 2.0), (sg * (W / 2.0 + 2.0), 0, 1.0), K['stone'])
        round_tower(A, rnd, 3.4, H + 6.0, K, sg * (W / 2.0 - 3.0), yf + 3.0, 0, top='cone', slits=1, bands=1, verts=14, roof_k=1.3)
    v4util.marker('mk_door', (0, yf, 3.4))
    return _fin(A, 'water_gate')


def quay_1():
    return _quay('straight')


def quay_2():
    """CP18_02 (round 3, lead) - a curved harbour quay as plain masonry: ashlar blocks laid along the arc (no hull stripes), a wide paved deck with a low kerb,
    short square stone bollards (no tall posts that read as funnels). 30 W x 8 H x 10 D."""
    reset()
    A = Acc()
    rnd = random.Random(302)
    R, nseg, a0, a1 = 22.0, 14, 0.0, 80.0
    for z in range(3):
        for j in range(nseg):
            a = a0 + (a1 - a0) * (j + 0.5) / nseg
            ln = math.radians((a1 - a0) / nseg) * (R - 1.0) * 1.07
            x, y, _ = polar(R - 1.0, a)
            A.chunk((ln, 4.2, 2.9), (x, y, 1.45 + z * 2.8), strata(STONES, z, 1), (0, 0, a + 90.0), 0.04, rnd)
    A.sweep([(R - 3.4, 8.2), (R + 1.4, 8.2), (R + 1.4, 8.9), (R - 3.4, 8.9)], a0, a1, 8, P['coping'])
    A.sweep([(R + 0.5, 8.9), (R + 1.4, 8.9), (R + 1.4, 10.0), (R + 0.5, 10.0)], a0, a1, 8, K['trim'])
    for a in (14.0, 40.0, 66.0):
        x, y, _ = polar(R - 1.4, a)
        A.box((1.5, 1.5, 1.5), (x, y, 8.9 + 0.7), K['stone'], (0, 0, a), bev=0.1)
        A.box((1.9, 1.9, 0.3), (x, y, 8.9 + 1.6), K['trim'], (0, 0, a), bev=0.05)
    return _fin(A, 'quay_wall')


def quay_3():
    return _quay('steps')


def quay_4():
    return _quay('posts')


PB = G.reg('vd_f', {
    'bronze': ((128, 96, 62), 'Metal', 0.3, 0.72),
    'bronze_d': ((92, 70, 50), 'Metal', 0.3, 0.75),
})


def hq_1():
    """CP15_01 (round 3, lead) - copy of ORIG.order_hq(1) with the gold star crest replaced by a matte bronze ring with a small crenellated tower glyph
    (no star, no gold, nothing bright)."""
    reset()
    A = Acc()
    rnd = random.Random(131)
    ORIG._stone_block(A, rnd, 56.0, 34.0, 28.0, 0, 0, 0, 3, True, True)
    A.gable(36.0, 58.0, 18.0, (0, 0, 28.0), K['cone'], (0, 0, 90))
    round_tower(A, rnd, 9.0, 56.0, K, -32.0, 8.0, 0, top='cone', roof_k=1.5, verts=22, flag=True)
    ORIG._stone_block(A, rnd, 22.0, 22.0, 20.0, 34.0, -4.0, 0, 2, True, False)
    A.frustum((24.0, 24.0), (2.0, 2.0), 14.0, (34.0, -4.0, 20.0), K['cone'])
    for i in range(7):
        A.box((24.0 - i * 1.2, 2.0, 1.0), (0, -17.0 - i * 1.6, 8.0 - i), K['stone'], bev=0.1)
    A.cyl(5.4, 0.8, (0, -18.1, 22.0), K['trim'], verts=24, rot=(90, 0, 0))
    A.cyl(4.5, 0.55, (0, -18.7, 22.0), PB['bronze'], verts=24, rot=(90, 0, 0))
    A.cyl(3.7, 0.7, (0, -18.7, 22.0), P['stone_d'], verts=24, rot=(90, 0, 0))
    A.box((1.9, 0.6, 4.2), (0, -19.3, 21.4), PB['bronze_d'], bev=0.05)
    for sx in (-0.65, 0.0, 0.65):
        A.box((0.5, 0.6, 0.9), (sx, -19.3, 23.9), PB['bronze_d'], bev=0.03)
    A.box((0.55, 0.7, 1.3), (0, -19.4, 20.2), P['stone_d'], bev=0)
    return _fin(A, 'order_hq')


def plaza_monument():
    """CP17_01 (round 3, lead) - copy of ORIG.plaza_monument with the gold urn finial and the flat star replaced by a dull bronze urn topped by a plain orb."""
    reset()
    A = Acc()
    for k in range(4):
        A.cyl(14.0 - k * 1.8, 0.7, (0, 0, k * 0.7), K['stone'], verts=24)
    A.cyl(9.0, 1.2, (0, 0, 2.8), K['trim'], verts=24)
    A.cyl(8.0, 0.9, (0, 0, 4.0), K['water'], verts=24)
    A.cyl(2.8, 10.0, (0, 0, 4.0), K['stone'], verts=16, r2=2.0)
    A.cyl(3.6, 1.0, (0, 0, 14.0), K['trim'], verts=16)
    A.cyl(1.4, 10.0, (0, 0, 15.0), K['stone'], verts=12, r2=1.1)
    A.cyl(2.2, 1.0, (0, 0, 25.0), K['trim'], verts=12)
    A.revolve([(1.6, 0.0), (1.4, 2.4), (0.8, 4.4), (1.2, 5.6), (0.6, 6.4)], (0, 0, 26.0), PB['bronze'], segs=10)
    A.ball(1.5, (0, 0, 33.0), PB['bronze'], segs=10, rings=6)
    for k in range(4):
        x, y, _ = polar(11.0, k * 90.0 + 45.0)
        A.box((2.0, 2.0, 1.8), (x, y, 0.9), K['stone'], (0, 0, k * 90.0 + 45.0), bev=0.1)
        A.cyl(0.9, 1.6, (x, y, 1.8), PB['bronze'], verts=8, r2=0.4)
    return _fin(A, 'plaza_monument')


def _grand_stair2(width, steps):
    """CP13_01 (lead pass 2) - grand stair with ONE continuous side wall per side (a prism following the step profile) instead of 36 overlapping boxes whose coplanar
    side faces rendered as black stripes; the back mass is wider than the walls so no faces coincide."""
    reset()
    A = Acc()
    rise = 22.0 / steps
    run = 40.0 / steps
    for i in range(steps):
        A.box((width, run, rise * (i + 1)), (0, -20.0 + run * (i + 0.5), rise * (i + 1) / 2.0), K['stone'] if i % 6 else K['trim'], bev=0.06)
    pts = [(-20.0, 0.0)]
    for i in range(steps):
        pts.append((-20.0 + run * i, rise * (i + 1) + 1.6))
        pts.append((-20.0 + run * (i + 1), rise * (i + 1) + 1.6))
    pts.append((20.0, 0.0))
    for sg in (-1, 1):
        x0 = width / 2.0 if sg > 0 else -width / 2.0 - 2.6
        A.prism(pts, 2.6, (x0, 0, 0), K['wall'], (90, 0, 90))
        for i in range(0, steps, 6):
            A.box((3.0, 3.0, 1.0), (sg * (width / 2.0 + 1.3), -20.0 + run * (i + 0.5), rise * (i + 1) + 2.1), K['trim'])
            A.cyl(0.35, 2.4, (sg * (width / 2.0 + 1.3), -20.0 + run * (i + 0.5), rise * (i + 1) + 2.6), K['iron'], verts=6)
    A.box((width + 5.8, 4.4, 22.0), (0, 18.0, 11.0), K['stone'])
    return _fin(A, 'grand_stair')


def _gate_post(A):
    W, D, H = 60.0, 40.0, 44.0
    for sx in (-1, 1):
        for k in range(int(D / 4.0) - 1):
            y = -D / 2.0 + 4.0 + k * 4.0
            A.box((1.2, 2.4, 2.4), (sx * (W / 2.0 - 0.4), y, H + 2.1), K['wall'])
            A.box((1.5, 2.7, 0.4), (sx * (W / 2.0 - 0.4), y, H + 3.5), K['cap'])
        for y in (-13.0, 0.0, 13.0):
            A.box((1.8, 2.6, 33.0), (sx * (W / 2.0 + 0.6), y, 18.0), K['stone'], bev=0.1)
            A.box((2.4, 3.2, 0.7), (sx * (W / 2.0 + 0.6), y, 34.8), K['trim'], bev=0.05)
        for z in (20.0, 29.0):
            for y in (-6.5, 6.5):
                A.box((0.5, 2.2, 3.6), (sx * (W / 2.0 + 0.05), y, z), K['glass'], bev=0)
                A.box((0.8, 3.0, 0.5), (sx * (W / 2.0 + 0.1), y, z + 2.1), K['trim'], bev=0)
    A.gable(26.0, 30.0, 9.0, (0, 0, H + 1.0), K['roof'], (0, 0, 0))
    A.box((27.0, 0.8, 0.6), (0, 0, H + 10.2), K['trim'])


def corner_1b():
    return LK.wrap(lambda: _corner(135, 11))()


def corner_3b():
    return LK.wrap(lambda: _corner(150, 13))()


def gatehouse_b():
    return LK.wrap(ORIG.gatehouse, post=_gate_post)()


def stair_wide_b():
    return LK.wrap(lambda: _grand_stair2(20.0, 36))()


BATCHES = {
    'gates_keep': ('v5_capital', mk([
        ('CP08_01_water_gate', water_gate)], 0.12)),
    'walls_towers': ('v5_capital', mk([
        ('CP01_02_ring_wall_straight_02', wall_2),
        ('CP02_02_ring_wall_corner_02', corner_2),
        ('CP03_02_ring_wall_stair_end_02', stair_end_2),
        ('CP05_02_turret_crenellated_02', turret_2),
        ('CP06_01_gate_flank_tower_01', flank_1),
        ('CP06_02_gate_flank_tower_02', flank_2)], 0.1)),
    'terrace_skyline': ('v5_capital', mk([
        ('CP12_01_terrace_retaining_wall_01', terrace_wall_s),
        ('CP12_02_terrace_retaining_wall_02', terrace_wall_c),
        ('CP14_04_skyline_tower_04', sky_beacon),
        ('CP14_05_skyline_tower_05', sky_water),
        ('CP15_03_order_hq_03', hq_3)], 0.1)),
    'town_extras': ('v5_capital', mk([
        ('CP11_01_great_hall_chapel_01', hall_1),
        ('CP16_01_townhouse_new_01', town_corner),
        ('CP18_01_quay_wall_01', quay_1),
        ('CP18_02_quay_wall_02', quay_2),
        ('CP18_03_quay_wall_03', quay_3),
        ('CP18_04_quay_wall_04', quay_4)], 0.1)),
}


# --- lead3 registration ---
BATCHES['lead3'] = ('v5_capital', mk([('CP15_01_order_hq_01', hq_1), ('CP17_01_plaza_features_01', plaza_monument)], 0.1))


# --- lead4 registration ---
import v5_leadkit as LK
BATCHES['lead4'] = ('v5_capital', mk([('CP02_01_ring_wall_corner_01', corner_1b), ('CP02_03_ring_wall_corner_03', corner_3b), ('CP07_01_gatehouse_main', gatehouse_b),
                                      ('CP13_01_grand_stair_01', stair_wide_b)], 0.12))
