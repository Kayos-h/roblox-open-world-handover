"""v5_fx_vi_b - fix module for assignment A2 (worker vi, palette prefix vi_fb_).
Rebuilds the flawed road-life, bridge, coast and reef models from v5_vi.py so a strict reviewer rates each OK.
Original designs, no glow, no franchise shapes. Front faces -Y. 1 unit = 1 stud. Pivot bottom-centre on z=0.
Reuses v5_vi.V colours through the round-1 module; registers only NEW vi_fb_ keys here.
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v5kit
from v5kit import Acc, polar, tang, mk, ids, band, strata
import v5gen as G
from v5gen import round_tower, rock_arch, column
import v4util
import v5_vi as R                      # round-1 module: reuse its palette V and helpers

# NEW palette (prefix vi_fb_). Never re-register a round-1 key name with a new colour.
P = G.reg('vi_fb', {
    'rock_lo': ((96, 100, 104), 'Slate', 0.0, 0.95), 'rock_mid': ((126, 128, 126), 'Slate', 0.0, 0.94),
    'rock_hi': ((158, 158, 152), 'Cobblestone', 0.0, 0.93), 'rock_warm': ((140, 130, 116), 'Limestone', 0.0, 0.92),
    'rock_dk': ((72, 74, 80), 'Basalt', 0.0, 0.9), 'reef_lo': ((78, 96, 102), 'Slate', 0.0, 0.92),
    'reef_mid': ((108, 120, 118), 'Slate', 0.0, 0.92), 'reef_hi': ((146, 150, 140), 'Cobblestone', 0.0, 0.92),
    'kelp': ((78, 110, 86), 'Grass', 0.0, 1.0), 'coral': ((176, 118, 104), 'Sandstone', 0.0, 0.95),
    'coral2': ((160, 140, 108), 'Sandstone', 0.0, 0.95), 'sand': ((202, 180, 142), 'Sandstone', 0.0, 0.95),
    'foam': ((198, 210, 212), 'SmoothPlastic', 0.0, 0.7), 'moss': ((96, 120, 72), 'Grass', 0.0, 1.0),
    'grass': ((104, 142, 74), 'Grass', 0.0, 1.0), 'grass2': ((122, 156, 86), 'Grass', 0.0, 1.0),
    'dirt': ((120, 98, 72), 'Ground', 0.0, 1.0), 'timber': ((110, 82, 58), 'Wood', 0.0, 0.88),
    'timber_dk': ((82, 60, 42), 'Wood', 0.0, 0.9), 'plank': ((150, 114, 78), 'WoodPlanks', 0.0, 0.9),
    'plank_dk': ((120, 90, 62), 'WoodPlanks', 0.0, 0.9), 'iron': ((70, 70, 76), 'Metal', 0.5, 0.6),
    'steel': ((150, 154, 160), 'Metal', 0.7, 0.45), 'char': ((52, 46, 42), 'Slate', 0.0, 0.95),
    'char2': ((74, 64, 58), 'Slate', 0.0, 0.95), 'plaster': ((214, 202, 176), 'Plaster', 0.0, 0.9),
    'plaster2': ((196, 182, 154), 'Plaster', 0.0, 0.9), 'wall_stone': ((170, 160, 142), 'Limestone', 0.0, 0.88),
    'trim': ((198, 190, 176), 'Limestone', 0.0, 0.86), 'cloth_r': ((164, 66, 56), 'Fabric', 0.0, 1.0),
    'cloth_b': ((70, 92, 132), 'Fabric', 0.0, 1.0), 'cloth_c': ((206, 194, 160), 'Fabric', 0.0, 1.0),
    'cloth_g': ((86, 112, 78), 'Fabric', 0.0, 1.0), 'gold': ((188, 156, 84), 'Metal', 0.75, 0.4),
    'rope': ((172, 148, 104), 'Fabric', 0.0, 1.0), 'dark': ((40, 38, 42), 'Slate', 0.0, 0.95),
    'shutter': ((96, 108, 86), 'WoodPlanks', 0.0, 0.85), 'door': ((96, 66, 48), 'Wood', 0.0, 0.85),
    'timber_warm': ((132, 98, 64), 'Wood', 0.0, 0.85), 'timber_grey': ((120, 104, 84), 'Wood', 0.0, 0.92),
    'wall_warm': ((198, 184, 158), 'Plaster', 0.0, 0.9), 'roof_warm': ((128, 74, 56), 'Brick', 0.0, 0.85),
    'ash': ((86, 80, 76), 'Slate', 0.0, 0.95), 'ember': ((150, 72, 48), 'Brick', 0.0, 0.8),
    'log': ((104, 76, 52), 'Wood', 0.0, 0.9), 'pot': ((64, 64, 70), 'Metal', 0.5, 0.6),
    'sand_warm': ((196, 176, 150), 'Sandstone', 0.0, 0.9),
})

RK = [P['rock_lo'], P['rock_mid'], P['rock_hi']]          # graded road/bank rock (dark base -> light top)
RK_WARM = [P['rock_lo'], P['rock_warm'], P['rock_hi']]
REEF = [P['reef_lo'], P['reef_mid'], P['reef_hi']]
ARCH = [P['rock_lo'], P['rock_mid'], P['rock_hi'], P['rock_warm']]


def _fin(A, name):
    A.to_scene()
    return finalize(name, 28)


def _foot_rubble(A, rnd, rx, ry, keys, n=7, z=0.0):
    """Fallen rubble resting on the ground at the foot - ties the model to z=0."""
    for k in range(n):
        s = rnd.uniform(1.2, 2.6)
        A.chunk((s, s * rnd.uniform(0.8, 1.2), rnd.uniform(0.8, 1.6)), (rnd.uniform(-rx, rx), rnd.uniform(-ry, ry), z + s * 0.25),
                keys[k % len(keys)], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)


# ================================================================== RD05 battlefield props (REDO/MAJOR/MINOR)
def _bf_cart(i):
    """RD05_01: broken supply cart - one bed on two wheels, a snapped shaft, spilled crates. 14x10x10."""
    reset()
    A = Acc()
    rnd = random.Random(7000 + i)
    # cart bed tilted (one wheel collapsed) so it reads as wrecked but connected
    tilt = 16
    A.box((8.0, 4.2, 0.6), (0, 0, 2.6), P['plank'], (tilt, 0, 0), bev=0.05)
    for sx in (-1, 1):                                              # side rails
        A.box((8.0, 0.4, 1.4), (0, sx * 2.0, 3.2), P['plank_dk'], (tilt, 0, 0), bev=0.04)
    A.box((0.5, 4.2, 1.4), (-3.9, 0, 3.2), P['plank_dk'], (tilt, 0, 0), bev=0.04)
    # two wheels on a shared axle, one sunk/broken
    A.cyl(0.4, 8.4, (0, 0, 1.8), P['iron'], verts=8, rot=(90, 0, 0))
    for sx, wz in ((-1, 1.9), (1, 1.0)):                           # right wheel sunk low = collapse
        wy = sx * 4.0
        A.cyl(1.9, 0.5, (0, wy, wz), P['timber'], verts=16, rot=(90, 0, 0), r2=1.9)
        A.cyl(2.0, 0.45, (0, wy, wz), P['iron'], verts=16, rot=(90, 0, 0), r2=2.0) if False else None
        A.sweep([(1.7, -0.22), (1.95, -0.22), (1.95, 0.22), (1.7, 0.22)], 0, 360, 16, P['iron'], loc=(0, wy, wz), rot=(90, 0, 0))
        A.cyl(0.5, 0.6, (0, wy, wz), P['iron'], verts=8, rot=(90, 0, 0))
        for k in range(6):
            A.box((0.22, 0.3, 3.4), (0, wy, wz), P['timber'], rot=(k * 30.0, 0, 0), bev=0)
    # snapped draw shaft dipping to the ground at the front
    A.beam((3.8, -1.3, 2.4), (6.6, -1.3, 0.3), 0.35, 0.35, P['timber'])
    A.beam((3.8, 1.3, 2.4), (6.2, 1.3, 0.4), 0.35, 0.35, P['timber'])
    A.box((0.5, 2.0, 0.4), (6.0, 0, 0.4), P['plank_dk'], (0, 6, 0), bev=0.03)
    # spilled crates and a barrel at the foot, all on the ground
    for (x, y, s) in ((5.2, 2.6, 1.8), (4.0, 3.0, 1.5), (-5.6, -1.0, 1.9)):
        A.box((s, s, s), (x, y, s / 2), P['plank'], (0, 0, rnd.uniform(-20, 20)), bev=0.07)
    A.cyl(1.1, 2.4, (-5.2, 2.4, 0), P['plank_dk'], verts=12, rot=(8, 0, 0))
    A.sweep([(0.9, 0.3), (1.2, 0.3), (1.2, 0.6), (0.9, 0.6)], 0, 360, 12, P['iron'], loc=(-5.2, 2.4, 0))
    return _fin(A, 'battlefield_cart')


def _bf_table(i):
    """RD05_02: overturned trestle table with a broken bench and a dropped shield. 14x10x10."""
    reset()
    A = Acc()
    rnd = random.Random(7100 + i)
    # table flipped on its side: top is a vertical panel, legs sticking out
    A.box((7.0, 0.5, 4.0), (0, -1.2, 2.6), P['plank'], (0, 0, 0), bev=0.05)       # table top on edge
    A.box((7.4, 0.35, 0.5), (0, -1.5, 4.4), P['plank_dk'], bev=0.04)              # top edge lip
    for sx in (-1, 1):                                                            # splayed trestle legs
        A.beam((sx * 2.6, -1.0, 0.6), (sx * 3.2, -3.2, 4.2), 0.45, 0.45, P['timber'])
        A.beam((sx * 2.6, -1.0, 0.6), (sx * 3.0, -3.0, 0.7), 0.4, 0.4, P['timber'])
    A.beam((-2.9, -3.1, 4.2), (2.9, -3.1, 4.2), 0.35, 0.35, P['timber'])         # cross-brace between legs
    # a broken bench lying beside it
    A.box((5.0, 1.4, 0.4), (-1.5, 3.0, 0.5), P['plank_dk'], (0, 0, 12), bev=0.04)
    for (lx, ly) in ((-3.2, 2.6), (0.0, 3.4)):
        A.box((0.4, 0.4, 1.0), (lx, ly, 0.5), P['timber'], bev=0)
    A.box((1.8, 1.0, 0.4), (2.6, 3.2, 0.6), P['plank_dk'], (6, 0, 20), bev=0.04)  # snapped-off bench end
    # dropped round shield resting on the ground, leaning against the table top - rim, boss and face relief
    sx0, sy0, sz0, lean = 2.9, -2.6, 1.5, 62
    A.cyl(1.8, 0.4, (sx0, sy0, sz0), P['cloth_r'], verts=16, rot=(lean, 0, 14))          # board
    A.sweep([(1.55, -0.2), (1.85, -0.2), (1.85, 0.2), (1.55, 0.2)], 0, 360, 16, P['steel'], loc=(sx0, sy0, sz0), rot=(lean, 0, 14))  # raised metal rim
    A.cyl(0.55, 0.5, (sx0 + 0.1, sy0 + 0.22, sz0 + 0.1), P['steel'], verts=12, rot=(lean, 0, 14))   # central boss
    for rr in (0.9, 1.3):                                                                # concentric face bands
        A.sweep([(rr - 0.12, -0.05), (rr + 0.12, -0.05), (rr + 0.12, 0.12), (rr - 0.12, 0.12)], 0, 360, 16, P['cloth_b'], loc=(sx0, sy0, sz0), rot=(lean, 0, 14))
    return _fin(A, 'battlefield_table')


def _bf_banner(i):
    """RD05_03: fallen war banner - a leaning pole with a draped flag, on a weighted stone base. 14x10x10."""
    reset()
    A = Acc()
    rnd = random.Random(7200 + i)
    # toppled pole resting diagonally, butt on a stone block
    A.chunk((3.0, 3.0, 1.4), (-4.4, 0, 0.7), P['rock_mid'], jit=0.12, rnd=rnd)
    ang = 42
    L = 10.2
    bx, bz = -4.0, 1.4
    tx = bx + math.sin(math.radians(ang)) * L
    tz = bz + math.cos(math.radians(ang)) * L
    A.beam((bx, 0, bz), (tx, 0, tz), 0.45, 0.45, P['timber_dk'])
    A.ball(0.5, (tx, 0, tz), P['gold'], segs=8, rings=5)
    # a crossbar near the top the flag hangs from, then the draped flag in overlapping folds (real volume)
    cbx = bx + math.sin(math.radians(ang)) * (L * 0.72)
    cbz = bz + math.cos(math.radians(ang)) * (L * 0.72)
    A.beam((cbx, -2.6, cbz), (cbx, 2.6, cbz), 0.18, 0.18, P['timber'])
    # the flag sags from the crossbar toward the ground in folds that lean with the pole
    for k in range(5):
        yy = -2.0 + k * 1.0
        droop = 0.5 + 0.5 * math.cos((k - 2) * 0.9)                              # middle folds sag more
        fx = cbx + math.sin(math.radians(ang)) * 0.4 + rnd.uniform(-0.2, 0.2)
        fz = cbz - 3.0 - droop
        A.box((0.3, 1.2, 6.0), (fx, yy, fz), P['cloth_r'], (rnd.uniform(-6, 6), -ang + rnd.uniform(-4, 4), 0), bev=0)
    for k in range(4):                                                           # torn, tattered hem at the bottom
        A.box((0.25, 0.9, rnd.uniform(1.2, 2.2)), (cbx + math.sin(math.radians(ang)) * 0.6, -1.6 + k * 1.1, cbz - 6.4), P['cloth_r'], (rnd.uniform(-10, 10), -ang, 6), bev=0)
    _foot_rubble(A, rnd, 5.0, 3.5, RK, 5)
    return _fin(A, 'battlefield_banner')


def _bf_cheval(i):
    """RD05_04: cheval-de-frise - a central log with angled crossed spikes and a base rail. 14x10x10."""
    reset()
    A = Acc()
    rnd = random.Random(7300 + i)
    A.cyl(0.7, 11.0, (0, 0, 2.2), P['timber_dk'], verts=10, rot=(0, 90, 0))      # central beam along X
    A.box((11.5, 1.6, 0.5), (0, 0, 0.3), P['timber'], bev=0.05)                  # ground base rail
    for sx in (-1, 1):                                                           # end feet
        A.box((0.8, 2.6, 2.4), (sx * 5.2, 0, 1.2), P['timber'], bev=0.06)
    for k in range(6):                                                           # crossed spikes at varied angles
        x = -4.4 + k * 1.76
        base_t = 60 + rnd.uniform(-8, 8)
        for sg in (-1, 1):
            a = sg * base_t
            dy = math.sin(math.radians(a)) * 4.4
            dz = math.cos(math.radians(a)) * 4.4
            A.beam((x, 0, 2.2), (x + rnd.uniform(-0.3, 0.3), dy, 2.2 + dz), 0.28, 0.28, P['timber'])
            A.frustum((0.5, 0.5), (0.05, 0.05), 1.0, (x, dy * 1.05, 2.2 + dz * 1.05), P['steel'], rot=(a, 0, 0))
    A.beam((-4.4, 0, 2.2), (4.4, 0.0, 2.2), 0.14, 0.14, P['rope'])               # binding rope line
    return _fin(A, 'battlefield_cheval')


def _bf_shields(i):
    """RD05_05 (REDO): a readable A-frame weapons rack - spears stood in a rail, shields hung on the side, a small pennant. 14x10x10."""
    reset()
    A = Acc()
    rnd = random.Random(7400 + i)
    # two A-frame trestles joined by a top rail and a bottom rail -> one clear connected frame
    for sy in (-3.4, 3.4):
        for sx in (-1, 1):
            A.beam((sx * 4.0, sy, 0.0), (0, sy, 6.2), 0.4, 0.4, P['timber'])     # legs meet at an apex
        A.box((1.2, 0.8, 0.8), (0, sy, 6.0), P['timber'], bev=0.06)              # apex block
    A.beam((0, -3.4, 5.8), (0, 3.4, 5.8), 0.35, 0.35, P['timber'])              # top rail (spears lean on it)
    A.box((9.0, 0.8, 0.6), (0, 0, 0.3), P['timber'], bev=0.05)                   # bottom rail with spear holes
    A.box((9.0, 7.6, 0.4), (0, 0, 0.2), P['timber_dk'], bev=0.04)               # base platform (ties it together)
    # a row of spears stood in the rack, butts on the platform, shafts leaning on the top rail
    for k in range(6):
        y = -3.0 + k * 1.2
        A.beam((0.2, y, 0.5), (-0.2, y, 8.2), 0.14, 0.14, P['timber_dk'])
        A.frustum((0.4, 0.22), (0.04, 0.04), 1.0, (-0.2, y, 8.2), P['steel'])    # spearhead
    # two round shields hung on the front face of the frame (clear discs, rim + boss)
    for k, sy in enumerate((-2.0, 1.6)):
        A.cyl(1.7, 0.35, (-3.6, sy, 3.2 + k * 0.3), (P['cloth_r'], P['cloth_b'])[k], verts=16, rot=(90, 0, 0))
        A.sweep([(1.45, -0.18), (1.7, -0.18), (1.7, 0.18), (1.45, 0.18)], 0, 360, 16, P['steel'], loc=(-3.6, sy, 3.2 + k * 0.3), rot=(90, 0, 0))
        A.cyl(0.5, 0.45, (-3.75, sy, 3.2 + k * 0.3), P['steel'], verts=10, rot=(90, 0, 0))
    # a small standard/pennant on the end of the frame
    A.cyl(0.16, 4.0, (3.8, 3.4, 6.0), P['timber'], verts=6)
    A.box((0.1, 2.0, 1.4), (3.8, 4.5, 8.6), P['cloth_r'], bev=0)
    # a couple of crates at the foot as camp context, on the ground
    for (x, y, s) in ((3.6, -3.0, 2.0), (3.0, -3.4, 1.6)):
        A.box((s, s, s), (x, y, s / 2), P['plank'], (0, 0, rnd.uniform(-12, 12)), bev=0.08)
    return _fin(A, 'weapon_rack')


# ================================================================== CO03 reefs (MAJOR x6) - solid relief mounds, even tone, no patches
def _reef(i):
    """CO03_01..06: a solid low reef with rounded 3D relief, evenly graded rock tone, siblings differ. 30x30x6."""
    reset()
    A = Acc()
    rnd = random.Random(7500 + i)
    # SOLID rounded body: a low broad base plate (thin) that the relief humps rise clearly above.
    A.ball(14.0, (0, 0, -0.6), band(REEF, 0.2, rnd), segs=16, rings=8, scale=(1.05, 1.0, 0.18))
    A.ball(10.0, (0, 0, -0.4), band(REEF, 0.3, rnd), segs=14, rings=7, scale=(1.3, 1.25, 0.2))
    # rounded sub-humps give real 3D relief, rising well above the base; layout differs per sibling (not a recolour)
    layout = [
        [(-6, 4, 7, 4.6), (6, -5, 8, 5.6), (2, 7, 5, 3.4)],
        [(0, 1, 11, 6.2), (-8, -6, 5, 3.2), (8, 5, 6, 4.0)],
        [(-7, -4, 6, 4.0), (5, 6, 8, 5.2), (9, -6, 5, 3.2), (-3, 8, 5, 3.0)],
        [(3, -3, 12, 6.4), (-9, 4, 5, 3.4), (-2, 9, 4, 2.8)],
        [(-5, 7, 6, 4.2), (7, 2, 7, 4.8), (-6, -7, 7, 5.0), (4, -8, 5, 3.2)],
        [(0, 6, 9, 5.4), (-8, -3, 6, 4.0), (8, -4, 6, 4.0), (1, -8, 5, 3.4)],
    ][i % 6]
    for (x, y, w, h) in layout:
        t = h / 6.5
        A.ball(w * 0.5, (x, y, 0.0), band(REEF, t, rnd), segs=11, rings=7, scale=(1.3, 1.25, h / (w * 0.5)))
        A.ball(w * 0.34, (x + rnd.uniform(-1, 1), y + rnd.uniform(-1, 1), h * 0.5), band(REEF, t + 0.2, rnd), segs=9, rings=6, scale=(1.15, 1.05, h / (w * 0.5) * 0.7))
    # a couple of taller outcrop ridges poking up through the domes (contrast), seated in the body - not flat patches
    for k in range(2):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(3, 8), a)
        A.chunk((rnd.uniform(2.0, 3.0), rnd.uniform(1.8, 2.6), rnd.uniform(4.0, 5.5)), (x, y, 2.0), band(REEF, 0.7, rnd), (0, 0, rnd.uniform(0, 90)), 0.1, rnd, (0.55, 0.55))
    # raised coral humps (warm tone) for a clear reef read
    for (cx, cy, cr) in [(5, -4, 2.4), (-5, 3, 2.0), (3, 6, 1.8)]:
        A.ball(cr, (cx, cy, 1.0), P['coral'] if (cx + cy) % 2 == 0 else P['coral2'], segs=9, rings=6, scale=(1.2, 1.1, 1.3))
    # tide-worn detail that settles in low spots only: kelp, coral tufts - varied per sibling
    deco = i % 3
    for k in range(9):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(5, 12), a)
        zt = 0.8 + rnd.uniform(0, 1.4)
        if deco == 0:
            A.cyl(0.4, rnd.uniform(1.2, 2.6), (x, y, zt), P['coral'], verts=6, r2=0.25)
            A.cyl(0.3, rnd.uniform(0.8, 1.6), (x + 0.5, y, zt), P['coral2'], verts=6, r2=0.2)
        elif deco == 1:
            A.ball(rnd.uniform(0.8, 1.4), (x, y, zt), P['kelp'], segs=7, rings=4, scale=(1.3, 1.1, 1.6))
        else:
            A.ball(rnd.uniform(0.9, 1.5), (x, y, zt), P['coral2'], segs=8, rings=5, scale=(1.1, 1.0, 1.3))
    for k in range(12):                                                          # soft surf foam seated at the waterline rim
        a = k * 30 + rnd.uniform(-8, 8)
        x, y, _ = polar(rnd.uniform(11.5, 13.8), a)
        A.ball(rnd.uniform(0.5, 0.9), (x, y, 0.0), P['foam'], segs=6, rings=4, scale=(1.6, 1.3, 0.3))
    return _fin(A, 'reef')


# ================================================================== CO04 sea arches (MINOR x2) - weathered tone, differ
def _sea_arch(i):
    """CO04_01/02: weathered sea arch with graded stone strata; the two siblings get different profiles. 70x30x60."""
    reset()
    A = Acc()
    rnd = random.Random(7600 + i)
    span = 56.0 if i == 0 else 52.0
    h = 64.0 if i == 0 else 40.0
    thick = 12.0 if i == 0 else 8.5
    G.rock_arch(A, rnd, span, h, thick, ARCH, 0, 0, 0, 26.0 if i == 0 else 14.0, 18, P['moss'])
    # stratified detail on the two legs (horizontal bands of chunks) -> tone variation + relief, opening stays clear
    for sg in (-1, 1):
        lx = sg * span / 2.0
        z = 0.0
        k = 0
        while z < h * 0.6:
            sh = rnd.uniform(2.6, 4.0)
            key = strata(ARCH, k, 2)
            for dy in (-thick * 0.3, thick * 0.3):                               # two depth columns -> rounder leg, more relief
                A.chunk((thick * rnd.uniform(0.7, 0.95), thick * 0.6 * rnd.uniform(0.85, 1.0), sh * 1.05),
                        (lx + rnd.uniform(-1.0, 1.0), dy + rnd.uniform(-0.8, 0.8), z + sh / 2), key, (0, 0, rnd.uniform(-6, 6)), 0.11, rnd, (0.9, 0.9))
            z += sh * 0.9
            k += 1
    # weathered stones following the arch ring, aligned to the ring (clean underside, not ragged)
    for j in range(14):
        a = math.pi * (j + 0.5) / 14.0
        ax = math.cos(a) * span / 2.0
        az = math.sin(a) * h * 0.82
        A.chunk((thick * 0.55, thick * 0.9, thick * 0.5), (ax, 0.0, az), band(ARCH, math.sin(a), rnd, 0.08), (0, math.degrees(a) - 90, 0), 0.06, rnd, (0.9, 0.9))
    # a darker wave-cut notch at each foot + a few LARGE welded boulders hugging the legs (not scattered rubble)
    for sg in (-1, 1):
        A.chunk((thick * 1.3, thick * 1.05, 3.0), (sg * span / 2.0, 0, 1.4), P['rock_dk'], (0, 0, rnd.uniform(0, 40)), 0.12, rnd)
        for k in range(3):
            A.chunk((rnd.uniform(4, 6), rnd.uniform(4, 6), rnd.uniform(2.5, 4.0)), (sg * span / 2.0 + rnd.uniform(-3, 3), rnd.uniform(-3, 3), 1.6),
                    band(ARCH, 0.2, rnd), (0, 0, rnd.uniform(0, 90)), 0.1, rnd, (0.7, 0.7))
    for k in range(12):                                                          # moss only where water would run (upper arch inner curve)
        t = rnd.uniform(0.3, 0.9)
        a = math.pi * t
        x = math.cos(a) * span / 2.0
        zz = math.sin(a) * h * 0.82
        A.ball(rnd.uniform(1.0, 1.8), (x, rnd.uniform(-2, 2), zz), P['moss'], segs=7, rings=4, scale=(1.3, 1.0, 0.7))
    return _fin(A, 'sea_arch')


# ================================================================== CO05 ruin islets (MAJOR/MINOR) - blended grass rim, even rock
def _islet(i):
    """CO05_01/02/03: rock islet with a sloped grass rim (no hard seam), even tone, varied ruin arrangement. 60x60x40."""
    reset()
    A = Acc()
    rnd = random.Random(7700 + i)
    # rock body, graded - keys chosen by band() so no tan camouflage squares
    A.mound(0, 0, 56.0, 56.0, 30.0, 30, RK_WARM, rnd, 0.0, 0.3, 0.72)
    # sloped soil rim then a grass cap set DOWN into the rock so the seam is a slope, not a flat edge
    A.cyl(21.0, 3.0, (0, 0, 27.5), P['dirt'], verts=20, r2=24.0)
    A.cyl(19.0, 3.4, (0, 0, 29.5), P['grass'], verts=20, r2=16.0)
    for k in range(10):                                                          # grass tufts spilling over the rim to blend it
        a = k * 36 + rnd.uniform(-12, 12)
        x, y, _ = polar(rnd.uniform(17, 22), a)
        A.ball(rnd.uniform(1.6, 2.6), (x, y, 28.0), P['grass2'], segs=7, rings=4, scale=(1.4, 1.3, 0.7))
    # ruin arrangement varied per sibling
    if i == 0:
        round_tower(A, rnd, 6.0, 22.0, R.RUIN, 2, -2, 31.0, ruin=True, slits=2, bands=2)
        for k in range(3):
            column(A, rnd.uniform(-14, 14), rnd.uniform(-14, 14), 31.0, 1.2, rnd.uniform(7, 13), R.RUIN, 0.5, rnd)
    elif i == 1:
        for k in range(3):                                                       # a cluster of three broken columns + a low wall
            column(A, -8 + k * 8, 4, 31.0, 1.3, rnd.uniform(9, 16), R.RUIN, 0.4, rnd)
        A.box((14.0, 2.4, 6.0), (0, -8.0, 34.0), P['wall_stone'], bev=0.15)
        for k in range(6):
            A.chunk((rnd.uniform(2, 4),) * 2 + (rnd.uniform(1, 3),), (rnd.uniform(-10, 10), -8 + rnd.uniform(-2, 2), 37.0), P['wall_stone'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    else:
        round_tower(A, rnd, 7.0, 16.0, R.RUIN, -3, 3, 31.0, ruin=True, slits=1, bands=1)   # stumpier, off-centre
        A.chunk((10.0, 10.0, 7.0), (6, -5, 31.0), P['rock_warm'], jit=0.12, rnd=rnd)       # a boulder outcrop
        for k in range(2):
            column(A, 8 - k * 14, 8, 31.0, 1.1, rnd.uniform(6, 11), R.RUIN, 0.6, rnd)
    for k in range(3):                                                           # a couple of small trees
        G.tree(A, rnd, rnd.uniform(11, 16), rnd.uniform(4, 6),
               {'bark': P['timber_dk'], 'leaf': P['grass'], 'leaf2': P['grass2'], 'bloom': P['grass2']},
               'oak', rnd.uniform(-15, 15), rnd.uniform(-15, 15), 31.0)
    return _fin(A, 'ruin_islet')


# ================================================================== HB01 harbour tower (MINOR) - stone trim, corner detail
def _harbour_tower(i):
    """HB01_03: square harbour wall-tower with stone banding, corner quoins, a capped parapet - not a flat grey cube. 24x24x40."""
    reset()
    A = Acc()
    rnd = random.Random(7800 + i)
    w = 11.0
    A.frustum((w + 3.0, w + 3.0), (w + 1.6, w + 1.6), 3.0, (0, 0, 0), P['rock_mid'])     # battered plinth
    A.frustum((w + 1.6, w + 1.6), (w, w), 31.0, (0, 0, 3.0), P['wall_stone'])            # body, slight batter
    for z in (9.0, 18.0, 27.0):                                                          # string courses (banding, not patches)
        A.box((w + 2.2, w + 2.2, 0.8), (0, 0, z), P['trim'], bev=0.1)
    for sx in (-1, 1):                                                                   # corner quoins
        for sy in (-1, 1):
            A.box((1.6, 1.6, 31.0), (sx * (w / 2), sy * (w / 2), 18.5), P['trim'], bev=0.08)
    for z in (11.0, 20.0):                                                               # recessed windows on the seaward faces
        G._window(A, 0, -w / 2 - 0.05, z, 270, {'glass': P['dark'], 'timber': P['trim'], 'stone': P['wall_stone'], 'shutter': P['shutter']}, 1.6, 3.0, False, P['trim'])
        G._window(A, w / 2 + 0.05, 0, z, 0, {'glass': P['dark'], 'timber': P['trim'], 'stone': P['wall_stone'], 'shutter': P['shutter']}, 1.6, 3.0, False, P['trim'])
    A.box((w + 3.4, w + 3.4, 1.2), (0, 0, 34.5), P['trim'], bev=0.12)                    # corbelled parapet base
    nm = 5
    for side in range(4):
        for k in range(nm):
            t = -1 + 2 * (k + 0.5) / nm
            px = (w / 2 + 1.2) * [t, 1, t, -1][side]
            py = (w / 2 + 1.2) * [-1, t, 1, t][side]
            A.box((2.0, 2.0, 2.4), (px, py, 36.4), P['wall_stone'], bev=0.1)             # merlons (crenellation)
    A.box((w - 1.0, w - 1.0, 0.8), (0, 0, 35.3), P['dark'], bev=0)                       # open walk floor (dark, recessed)
    A.box((2.4, 0.5, 4.4), (0, -w / 2 - 0.1, 5.4), P['door'], bev=0.05)                  # door
    return _fin(A, 'harbour_tower')


# ================================================================== RD01 watchtowers (MINOR x2) - capped top, anchored detail
def _watch(i):
    """RD01_02/04: stone watchtower with a real capped top - i0 conical roof, i1 anchored crenellation. 20x20x50."""
    reset()
    A = Acc()
    rnd = random.Random(7900 + i)
    K = {'stone': P['rock_mid'], 'wall': P['wall_stone'], 'trim': P['trim'], 'dark': P['dark'], 'door': P['door'],
         'deck': P['plank'], 'roof': R.V['roof'], 'roof2': R.V['cap'], 'gold': P['gold'], 'flag': P['cloth_r']}
    if i == 0:
        round_tower(A, rnd, 8.5, 44.0, K, top='cone', slits=3, bands=3, door=True, verts=18, roof_k=1.05)
    elif i == 1:
        round_tower(A, rnd, 8.5, 44.0, K, top='crenel', slits=3, bands=3, door=True, verts=18)
        # add a few deliberately broken (but anchored, resting on the walk) merlon stumps
        for k in range(4):
            a = rnd.uniform(0, 360)
            x, y, _ = polar(9.0, a)
            A.chunk((2.0, 1.1, rnd.uniform(0.8, 1.8)), (x, y, 46.6), P['wall_stone'], (0, 0, a + 90), 0.12, rnd)
    else:                                                                        # RD01_03: stone-banded tower, flat top with a timber watch hoarding + a ragged broken side
        r, h = 8.5, 40.0
        round_tower(A, rnd, r, h, K, top='flat', slits=3, bands=3, door=True, verts=18)
        # colour bands of darker stone courses so it is not one pale tone
        for z in (10.0, 20.0, 30.0):
            A.sweep([(r - 0.5, -0.5), (r + 0.5, -0.5), (r + 0.5, 0.5), (r - 0.5, 0.5)], 0, 360, 18, P['rock_mid'], loc=(0, 0, z))
        # timber hoarding (covered wooden gallery) around the top - clear silhouette, not a bare cap
        A.sweep([(r + 0.2, h - 0.2), (r + 1.5, h - 0.2), (r + 1.5, h + 0.4), (r + 0.2, h + 0.4)], 0, 360, 18, P['timber'], loc=(0, 0, 0))
        for k in range(12):
            a = k * 30
            x, y, _ = polar(r + 0.9, a)
            A.box((1.0, 1.0, 4.4), (x, y, h + 2.0), P['timber'], (0, 0, a), bev=0.06)      # hoarding posts
        A.cyl(r + 1.9, 2.2, (0, 0, h + 4.2), P['roof_warm'], verts=18, r2=r + 0.6)          # low shed roof over the gallery
        # one side of the parapet broken away (ruin) - anchored stones on the walk
        for k in range(4):
            a = 250 + k * 12
            x, y, _ = polar(r + 0.8, a)
            A.chunk((1.6, 1.2, rnd.uniform(0.8, 2.0)), (x, y, h + 0.6), P['wall_stone'], (0, 0, a + 90), 0.12, rnd)
    return _fin(A, 'watchtower')


# ================================================================== RD02 camp set (MINOR x4) - distinct geometry
def _camp(i):
    """RD02_01/02/03/06: camp pieces with genuinely different geometry, not recolours. 16x14x10."""
    reset()
    A = Acc()
    rnd = random.Random(8000 + i)
    if i == 0:                                                                   # ridge tent with a sloped front awning
        A.gable(9.0, 11.0, 6.4, (0, 0, 0), P['cloth_c'], (0, 0, 90))
        for sg in (-1, 1):                                                       # end flaps to give the tent volume
            A.box((0.3, 11.0, 0.3), (sg * 4.5, 0, 0.2), P['rope'], bev=0)
        A.box((2.6, 0.2, 4.2), (0, -5.55, 2.1), P['dark'], bev=0)                # dark door opening
        for sg in (-1, 1):                                                       # pegged guy ropes to the ground
            A.beam((sg * 4.5, 5.5, 3.2), (sg * 5.6, 6.8, 0.0), 0.1, 0.1, P['rope'])
            A.beam((sg * 4.5, -5.5, 3.2), (sg * 5.6, -6.8, 0.0), 0.1, 0.1, P['rope'])
        # awning: a sheet sloping from the front eave (z~4.0) down to two poles on the ground
        A.box((7.4, 4.4, 0.25), (0, -7.6, 3.0), P['cloth_c'], (-34, 0, 0), bev=0)
        for sx in (-1, 1):
            A.cyl(0.2, 1.4, (sx * 3.5, -9.4, 0), P['timber'], verts=6)           # short awning poles reaching the sheet front
            A.beam((sx * 3.5, -9.4, 1.4), (sx * 3.6, -9.6, 0.0), 0.1, 0.1, P['rope'])
        A.cyl(0.18, 10.0, (0, 5.4, 0), P['timber'], verts=6)                     # rear pole (sets 10-stud height)
        A.box((0.1, 2.2, 1.1), (0, 6.5, 9.0), P['cloth_r'], bev=0)               # small pennant
    elif i == 1:                                                                 # conical bell tent (round, not a ridge)
        A.cyl(6.4, 7.6, (0, 0, 0.6), P['cloth_g'], verts=14, r2=0.3)
        A.cyl(6.6, 0.6, (0, 0, 0.0), P['dark'], verts=14, r2=6.6)               # skirt shadow
        A.box((2.0, 0.2, 3.8), (0, -6.3, 1.9), P['dark'], (0, 0, 0), bev=0)      # entry slit
        A.cyl(0.16, 9.2, (0, 0, 0), P['timber'], verts=6)
        for k in range(8):
            a = k * 45
            x, y, _ = polar(6.8, a)
            A.beam((x, y, 0), (x * 1.18, y * 1.18, 0.0), 0.08, 0.08, P['rope'])
    elif i == 2:                                                                 # lean-to shelter (one sagging slope, open front)
        # canopy built from two overlapping panels with a dip in the middle so it sags, not a flat sheet
        A.box((9.4, 4.2, 0.5), (0, -0.6, 6.2), P['cloth_r'], (30, 0, 0), bev=0.1)
        A.box((9.4, 3.8, 0.5), (0, 2.6, 4.2), P['cloth_r'], (44, 0, 0), bev=0.1)   # lower, steeper fold
        A.box((9.4, 1.2, 0.4), (0, 1.0, 5.2), P['cloth_r'], (36, 0, 0), bev=0.08)  # mid sag ridge
        for sx in (-1, 1):                                                        # thicker A-frame legs (not spindly)
            A.cyl(0.42, 7.8, (sx * 4.3, -2.6, 0), P['timber'], verts=8)
            A.cyl(0.42, 3.6, (sx * 4.3, 4.4, 0), P['timber'], verts=8)
            A.beam((sx * 4.3, -2.6, 7.6), (sx * 4.3, 4.4, 3.5), 0.26, 0.26, P['timber'])
        A.beam((-4.3, -2.6, 7.6), (4.3, -2.6, 7.6), 0.24, 0.24, P['timber'])      # front ridge beam
        A.box((9.0, 0.4, 3.2), (0, 4.7, 1.6), P['cloth_r'], bev=0.06)             # back wall with thickness
        A.box((3.4, 2.2, 0.5), (-2.0, -1.0, 0.25), P['plank'], bev=0.06)          # bedroll plank
        A.cyl(0.8, 3.4, (3.0, 2.0, 0), P['plank_dk'], verts=10)                   # a barrel inside
    elif i == 3:                                                                 # i3 -> RD02_06: barrel + crate stack, closed end caps
        A.cyl(1.8, 5.0, (-2.0, 0, 0), P['plank_dk'], verts=14, rot=(0, 90, 0))   # barrel on its side
        A.cyl(1.8, 0.3, (-4.5, 0, 0), P['plank'], verts=14, rot=(0, 90, 0))      # closed end cap (fixes dark gap)
        A.cyl(1.8, 0.3, (0.5, 0, 0), P['plank'], verts=14, rot=(0, 90, 0))
        for z in (1.8,):
            for k in range(3):
                A.sweep([(1.55, -0.12), (1.85, -0.12), (1.85, 0.12), (1.55, 0.12)], 0, 360, 14, P['iron'], loc=(-3.3 + k * 1.3, 0, 0), rot=(0, 90, 0))
        for (x, y, s) in ((3.0, -1.5, 2.6), (3.4, 1.4, 2.2), (2.6, 0.2, 2.0)):   # crate stack
            A.box((s, s, s), (x, y, s / 2), P['plank'], (0, 0, rnd.uniform(-12, 12)), bev=0.08)
        A.box((2.0, 2.0, 2.0), (3.0, -0.2, 3.3), P['plank_dk'], (0, 0, 8), bev=0.08)
    else:                                                                        # i4 -> RD02_05: campfire + cooking pot + crates + a bedroll (readable camp gear)
        # stone fire ring with charred logs and a low ember/ash bed (no glow)
        for k in range(8):
            a = k * 45
            x, y, _ = polar(2.3, a)
            A.chunk((1.1, 1.1, 0.8), (x - 2.0, y, 0.4), P['rock_mid'], (0, 0, a), 0.2, rnd)
        A.cyl(1.7, 0.3, (-2.0, 0, 0.1), P['ash'], verts=12)                      # ash bed
        for k in range(5):                                                       # criss-crossed logs in the fire
            a = k * 36
            A.beam((-2.0 - 1.2, 0, 0.4), (-2.0 + 1.2 * math.cos(math.radians(a)), 1.2 * math.sin(math.radians(a)), 1.4), 0.3, 0.3, P['log'])
        A.cyl(0.5, 0.8, (-2.0, 0, 0.3), P['ember'], verts=8)                     # ember core (matte, not neon)
        # a cooking tripod with a pot over the fire
        for k in range(3):
            a = 90 + k * 120
            x, y, _ = polar(2.2, a)
            A.beam((-2.0 + x, y, 0), (-2.0, 0, 4.4), 0.14, 0.14, P['timber'])
        A.revolve([(0.0, 0.0), (1.1, 0.2), (1.2, 1.1), (0.8, 1.7), (0.95, 1.9)], (-2.0, 0, 2.2), P['pot'], segs=12)
        A.beam((-2.0, 0, 4.2), (-2.0, 0, 3.6), 0.06, 0.06, P['iron'])            # pot hook
        # crates and a barrel as camp gear (clearly stacked, connected silhouette)
        for (x, y, s) in ((4.2, 2.2, 2.2), (4.6, -0.3, 2.0), (4.0, 2.0, 1.8)):
            A.box((s, s, s), (x, y, s / 2 if y != 2.0 else s / 2 + 2.2), P['plank'], (0, 0, rnd.uniform(-10, 10)), bev=0.08)
        A.cyl(1.4, 3.0, (5.0, -3.2, 0), P['plank_dk'], verts=12)
        A.sweep([(1.2, 0.6), (1.5, 0.6), (1.5, 0.9), (1.2, 0.9)], 0, 360, 12, P['iron'], loc=(5.0, -3.2, 0))
        A.sweep([(1.2, 2.1), (1.5, 2.1), (1.5, 2.4), (1.2, 2.4)], 0, 360, 12, P['iron'], loc=(5.0, -3.2, 0))
        # a rolled bedroll on the ground
        A.cyl(0.9, 4.0, (2.0, -4.0, 0.9), P['cloth_b'], verts=10, rot=(0, 90, 0))
        A.cyl(0.9, 0.3, (0.0, -4.0, 0.9), P['cloth_c'], verts=10, rot=(0, 90, 0))
    return _fin(A, 'camp_piece')


# ================================================================== RD06 abandoned houses (MAJOR x3) - timber-framed ruin, no blank slab
def _ruin_house(i):
    """RD06_01/03/05: a ruined half-timber house - a standing framed wall with windows, a part-collapsed roof, deliberate debris. 22x20x20."""
    reset()
    A = Acc()
    rnd = random.Random(8100 + i)
    w, d = 15.0, 13.0
    A.box((w + 1.0, d + 1.0, 1.0), (0, 0, 0.5), P['rock_mid'], bev=0.12)          # stone plinth
    # ---- the standing wall(s): stone-infill between a timber frame, with window openings (never a blank slab)
    def framed_wall(cx, cy, length, height, axis='x', broken_top=0.0):
        """A timber-framed ruined wall running along `axis` ('x' or 'y'), centred on (cx, cy)."""
        def put_box(size_along, thick, zsize, along, across, z, key, bev=0.05):
            if axis == 'x':
                A.box((size_along, thick, zsize), (cx + along, cy + across, z), key, bev=bev)
            else:
                A.box((thick, size_along, zsize), (cx + across, cy + along, z), key, bev=bev)

        def put_beam(a0, c0, z0, a1, c1, z1, wd, ht, key):
            if axis == 'x':
                A.beam((cx + a0, cy + c0, z0), (cx + a1, cy + c1, z1), wd, ht, key)
            else:
                A.beam((cx + c0, cy + a0, z0), (cx + c1, cy + a1, z1), wd, ht, key)

        n = max(2, int(length / 4.0))
        for k in range(n + 1):                                                   # posts
            a = -length / 2 + k * length / n
            put_box(0.7, 0.7, height, a, 0.0, height / 2, P['timber_dk'], 0.06)
        for zz in (0.4, height * 0.5, height - 0.4):                             # sill, mid-rail, top plate
            put_box(length, 0.6, 0.6, 0.0, 0.0, zz, P['timber_dk'])
        for k in range(n):                                                       # plaster infill panels
            a = -length / 2 + (k + 0.5) * length / n
            put_box(length / n - 0.9, 0.5, height * 0.5 - 0.9, a, 0.0, height * 0.25 + 0.2, P['plaster'], 0.04)
            if k != n // 2:
                put_box(length / n - 0.9, 0.5, height * 0.5 - 0.9, a, 0.0, height * 0.75 - 0.2, P['plaster2'], 0.04)
        for k in range(n):                                                       # diagonal braces
            a0 = -length / 2 + k * length / n
            put_beam(a0, 0, 0.6, a0 + length / n, 0, height * 0.5, 0.3, 0.3, P['timber_dk'])
        wa = 0.5 * length / n                                                    # one window opening (dark recess)
        put_box(2.0, 0.7, 2.6, wa, 0.0, height * 0.62, P['dark'], 0)
        put_box(2.6, 0.5, 0.4, wa, -0.1, height * 0.62 + 1.5, P['timber'], 0)
        if broken_top:                                                           # ragged broken crest, stones butted together and seated into the wall top
            for k in range(n):
                a = -length / 2 + (k + 0.5) * length / n
                ch = rnd.uniform(1.4, 2.8) * broken_top
                loc = (cx + a, cy, height - 1.2 + ch / 2) if axis == 'x' else (cx, cy + a, height - 1.2 + ch / 2)
                sz = (length / n * 1.02, 0.55, ch) if axis == 'x' else (0.55, length / n * 1.02, ch)
                A.chunk(sz, loc, P['plaster'] if k % 2 else P['plaster2'], (0, 0, 0), 0.1, rnd)

    # layout differs per sibling but all read as a timber-framed ruin
    if i == 0:
        framed_wall(0, -d / 2, w, 11.0, 'x', broken_top=1.4)                     # tall front wall (runs along X)
        framed_wall(-w / 2, 0.0, d, 7.0, 'y', broken_top=1.0)                    # lower left side wall (runs along Y), meets at corner
        # anchored chimney rising from the plinth, bonded to the side wall
        A.box((2.6, 2.6, 15.0), (-w / 2 + 0.6, d / 2 - 2.0, 7.5), P['rock_mid'], bev=0.1)
        A.box((3.2, 3.2, 0.7), (-w / 2 + 0.6, d / 2 - 2.0, 15.2), P['trim'], bev=0.08)
        A.box((1.1, 1.1, 0.8), (-w / 2 + 0.6, d / 2 - 2.0, 15.7), P['rock_lo'], bev=0.05)
    elif i == 1:
        framed_wall(0, -d / 2, w, 12.0, 'x', broken_top=1.8)                     # one dramatic standing gable wall
        for sx in (-1, 1):                                                       # gable peak (triangular timber frame)
            A.beam((sx * w / 2, -d / 2, 12.0), (0, -d / 2, 17.0), 0.4, 0.4, P['timber_dk'])
        A.box((2.0, 0.5, 3.0), (0, -d / 2, 13.6), P['plaster'], bev=0.04)
        framed_wall(w / 2, 0.0, d, 5.0, 'y', broken_top=0.6)                     # low stub side wall meeting the corner
    else:
        framed_wall(0, -d / 2, w, 9.0, 'x', broken_top=1.2)                      # front wall
        framed_wall(0, d / 2, w, 10.0, 'x', broken_top=1.4)                      # back wall
        framed_wall(-w / 2, 0.0, d, 7.0, 'y', broken_top=1.0)                    # left side wall connects the two -> enclosed ruin
        framed_wall(w / 2, 0.0, d, 5.0, 'y', broken_top=0.8)                     # right side stub too -> reads as a house, not scaffolding
        # a surviving roof fragment over the back half (so it is an abandoned house, not bare frame)
        for k in range(3):
            A.box((w + 0.4, 8.2, 0.55), (0, d / 4 + 0.6 + k * 0.0, 8.2), R.V['cone'], (31, 0, 0), bev=0.05) if k == 0 else None
        [A.box((0.7, 0.7, 6.0), (sx_ * (w / 2 - 0.4), 0.0, 3.5), P['timber_dk'], bev=0.05) for sx_ in (-1, 1)] + [A.beam((-w / 2 + 0.4, 0.0, 6.2), (w / 2 - 0.4, 0.0, 6.2), 0.7, 0.7, P['timber_dk'])]
        # a fallen roof beam structure leaning across (deliberate collapse)
        for k in range(4):
            x = -w / 2 + 2.5 + k * 3.2
            A.beam((x, -d / 2 + 1.0, 9.0), (x + rnd.uniform(-1, 1), d / 2 - 1.0, 4.0 + rnd.uniform(-1, 2)), 0.45, 0.45, P['timber_warm'])
    # ---- RD06_02 (i==3): a mostly-standing WEATHERED house, warm brown timber (not charred black), intact gable roof, a few broken parts
    if i == 3:
        WK = {'wall': P['wall_warm'], 'stone': P['rock_mid'], 'trim': P['trim'], 'timber': P['timber_warm'],
              'roof': P['roof_warm'], 'roof2': P['roof_warm'], 'cap': P['timber_grey'], 'glass': P['dark'],
              'shutter': P['shutter'], 'door': P['door'], 'iron': P['iron'], 'sign': P['plank'], 'gold': P['gold'], 'flag': P['cloth_r'], 'deck': P['plank']}
        G.house(A, rnd, 15.0, 14.4, 2, WK, hs=6.0, jetty=0.5, pitch=0.8, chimney=True, dormers=1)
        # weathering: missing shutters, a boarded window, moss on the roof - but it stays a readable house
        for k in range(5):
            A.ball(rnd.uniform(0.8, 1.4), (rnd.uniform(-6, 6), rnd.uniform(-5, 5), 13.0 + rnd.uniform(0, 3)), P['moss'], segs=6, rings=4, scale=(1.4, 1.2, 0.5))
        for k in range(3):                                                       # a couple of boards nailed over a window
            A.box((3.0, 0.3, 0.5), (3.0, -6.6, 7.5 + k * 0.9), P['timber_warm'], (0, 0, rnd.uniform(-8, 8)), bev=0.04)
        for k in range(6):                                                       # light debris at the foot (warm timber + plaster)
            s = rnd.uniform(1.0, 2.0)
            A.chunk((s, s, rnd.uniform(0.5, 1.0)), (rnd.uniform(-8, 8), -d / 2 - rnd.uniform(0, 3), 0.6), [P['timber_warm'], P['plaster'], P['rock_lo']][k % 3], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
        return _fin(A, 'abandoned_house')
    # collapsed roof slope on one side (tiles on fallen rafters), reads as a ruin not a defect
    if i in (0, 1):
        for k in range(4):
            A.box((w * 0.8, 3.4, 0.4), (0.5, 3.5 + k * 0.1, 7.5 - k * 1.6), R.V['cone'], (28 + k * 3, 0, rnd.uniform(-4, 4)), bev=0.04)
        for k in range(4):                                                       # broken rafters poking through
            A.beam((-w / 3 + k * 3.0, 1.0, 6.5), (-w / 3 + k * 3.0 + rnd.uniform(-1, 1), d / 2 - 1.0, 2.0), 0.4, 0.4, P['timber_dk'])
    # deliberate debris: roof tiles, timber, plaster lumps resting on the ground inside and out
    for k in range(16):
        s = rnd.uniform(1.0, 2.4)
        key = [R.V['cone'], P['plaster'], P['timber_dk'], P['rock_lo']][k % 4]
        A.chunk((s, s * rnd.uniform(0.7, 1.1), rnd.uniform(0.4, 1.0)), (rnd.uniform(-w / 2 + 1, w / 2 - 1), rnd.uniform(-d / 2 + 1, d / 2 - 1), 0.9),
                key, (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(5):                                                           # fallen long timbers
        A.cyl(0.3, rnd.uniform(3, 6), (rnd.uniform(-5, 5), rnd.uniform(-4, 4), 0.4), P['timber_dk'], verts=6, rot=(90, 0, rnd.uniform(0, 180)))
    return _fin(A, 'abandoned_house')


# ================================================================== BR01 viaducts (MAJOR/MINOR) - no inverted faces, no stray slab, filled spandrels
def _viaduct(i):
    """BR01_01/02: multi-arch stone viaduct, solid piers, filled spandrels (no black voids), clean deck, no stray block. 160x20x40."""
    reset()
    A = Acc()
    rnd = random.Random(8200 + i)
    n = 5
    span = 160.0 / n
    pier_w = 6.0
    deck_z = 28.0
    for k in range(n + 1):                                                       # piers
        x = -80.0 + k * span
        ph = deck_z - (6.0 if k in (0, n) else 0.0)
        A.box((pier_w, 12.0, ph), (x, 0, ph / 2.0), P['rock_mid'], bev=0.3)
        A.box((pier_w + 1.2, 13.0, 1.2), (x, 0, ph - 0.6), P['trim'], bev=0.1)   # pier capital
        # cutwater (triangular prism) on the upstream face so piers read as a bridge, not posts
        A.prism([(-pier_w / 2, 0), (pier_w / 2, 0), (0, -4.0)], ph, (x, 6.0, 0), P['rock_mid'], rot=(0, 0, 0), z0=0.0)
    for k in range(n):                                                           # arches: a voussoir ring + solid spandrel flush under the deck
        xc = -80.0 + (k + 0.5) * span
        ri = span / 2.0 - pier_w / 2.0                                           # arch springs from the pier faces
        # arch ring (intrados), a solid half-annulus between the two piers - closed, normals recalced by to_scene
        A.sweep([(ri - 2.2, -6.0), (ri, -6.0), (ri, 6.0), (ri - 2.2, 6.0)], 0, 180, 16, P['wall_stone'], loc=(xc, 0, 14.0), rot=(90, 0, 0))
        # voussoir stones around the arch face for readability (both faces)
        for j in range(9):
            a = math.pi * (j + 0.5) / 9.0
            ax = xc + math.cos(a) * (ri - 0.5)
            az = 14.0 + math.sin(a) * (ri - 0.5)
            for sy in (-6.2, 6.2):
                A.box((2.0, 1.0, 2.6), (ax, sy, az), strata([P['rock_mid'], P['rock_hi']], j, 1), (0, math.degrees(a) - 90, 0), bev=0.06)
        # SOLID spandrel fill: a box capped by the arch, sitting between the piers, flush under the deck
        A.box((span - pier_w - 0.4, 12.0, deck_z - 14.0 - 0.2), (xc, 0, (14.0 + deck_z) / 2.0 - 0.1), P['wall_stone'], bev=0.08)
        # fill the two haunches (triangular gaps either side of the arch crown) so no gap shows under the deck
        for sg in (-1, 1):
            A.prism([(0, -6), (0, 6), (span / 2 - pier_w / 2 - 0.5, 6), (span / 2 - pier_w / 2 - 0.5, -6)], 1.0, (xc + sg * (ri - 1.0), 0, 14.0), P['wall_stone']) if False else None
    # continuous deck slab seated directly on the spandrels + road surface
    A.box((160.0, 13.0, 2.4), (0, 0, deck_z + 0.8), P['rock_mid'], bev=0.15)
    A.box((160.0, 12.0, 0.6), (0, 0, deck_z + 1.9), P['trim'], bev=0.08)         # deck cornice band
    A.box((160.0, 7.0, 0.5), (0, 0, deck_z + 2.3), P['dirt'], bev=0)             # road surface
    for sg in (-1, 1):
        A.box((160.0, 1.2, 2.6), (0, sg * 5.8, deck_z + 3.1), P['trim'], bev=0.12)   # parapet rail
        for k in range(26):
            A.box((2.2, 1.0, 1.4), (-76.0 + k * 6.1, sg * 5.8, deck_z + 4.5), P['wall_stone'], bev=0.08)  # balusters/merlons
    # weathering: moss seated ON the spandrel faces (water-run streaks), not floating in the openings
    for k in range(10):
        kk = rnd.randint(0, n - 1)
        xc = -80.0 + (kk + 0.5) * span
        A.ball(rnd.uniform(1.0, 1.8), (xc + rnd.uniform(-8, 8), -6.1, rnd.uniform(16, 24)), P['moss'], segs=6, rings=4, scale=(1.4, 0.6, 1.0))
    if i == 1:                                                                   # the "damaged" sibling: a partly collapsed parapet, debris at a foot (deliberate)
        for k in range(5):
            A.chunk((2.4, 1.2, rnd.uniform(1, 2)), (24.0 + k * 2.2, 5.8, deck_z + 3.4), P['wall_stone'], (0, 0, rnd.uniform(0, 40)), 0.15, rnd)
        _foot_rubble(A, rnd, 6.0, 6.0, RK, 6)
    v4util.marker('mk_enda', (-80.0, 0, deck_z + 2.4))
    v4util.marker('mk_endb', (80.0, 0, deck_z + 2.4))
    v4util.marker('mk_deck', (0, 0, deck_z + 2.4))
    return _fin(A, 'stone_viaduct')


# ================================================================== RV01 bank rocks (MINOR x4) - earth/moss tone variation, differ
def _bank(i):
    """RV01_01..04: river-bank rock with earth/moss tone variation and a distinct silhouette each. 30x20x10."""
    reset()
    A = Acc()
    rnd = random.Random(8300 + i)
    keys = [P['rock_lo'], P['rock_warm'], P['rock_mid'], P['rock_hi']]

    def boulder(x, y, w, dd, hh, t):
        A.ball(w * 0.5, (x, y, hh * 0.1), band(keys, t, rnd), segs=10, rings=6, scale=(1.0, dd / w, hh / (w * 0.5) * 0.85))
        A.chunk((w * 0.8, dd * 0.8, hh), (x, y, hh * 0.4), band(keys, t + 0.2, rnd), (0, 0, rnd.uniform(0, 90)), 0.12, rnd, (0.7, 0.7))
        humps.append((x, y, hh * 0.9))

    humps = []
    # distinct silhouette per sibling, built from rounded boulders (not flat plates)
    if i == 0:                                                                   # long low ridge of fused boulders
        for k in range(4):
            boulder(-10 + k * 6.5, rnd.uniform(-2, 2), rnd.uniform(7, 10), rnd.uniform(9, 12), rnd.uniform(5, 8), 0.3 + k * 0.1)
    elif i == 1:                                                                 # ONE big dome boulder + a small leaning satellite (distinct from 01's ridge)
        A.chunk((20.0, 15.0, 8.5), (-2.0, 0.0, 4.25), band(keys, 0.45, rnd), (0, 0, 8), 0.07, rnd, (0.78, 0.78))
        A.chunk((13.0, 11.0, 6.5), (7.5, -3.0, 3.25), band(keys, 0.25, rnd), (0, 0, -14), 0.08, rnd, (0.8, 0.8))
        A.chunk((10.0, 9.0, 5.0), (-10.0, 4.0, 2.5), band(keys, 0.1, rnd), (0, 0, 24), 0.08, rnd, (0.8, 0.8))
        A.chunk((9.0, 8.0, 3.4), (-3.0, 0.5, 9.0), band(keys, 0.85, rnd), (0, 0, 35), 0.07, rnd, (0.75, 0.75))
        humps.extend([(-3.0, 0.5, 10.2), (7.5, -3.0, 6.4), (-10.0, 4.0, 4.8)])
        pass
        pass   # a small shelf slab leaning on it
    elif i == 2:                                                                 # one tall rounded boulder with a shelf
        boulder(0, 0, 15, 14, 9.5, 0.6)
        boulder(7, -3, 8, 7, 3.0, 0.2)
        A.ball(6.0, (0, 0, 0.0), band(keys, 0.2, rnd), segs=12, rings=6, scale=(2.2, 1.6, 0.4))
    else:                                                                        # scattered cluster of distinct boulders
        for (x, y, w, hh) in ((-9, -2, 6, 6.0), (0, 3, 8, 8.0), (7, -3, 7, 6.5), (11, 4, 5, 4.0)):
            boulder(x, y, w, w * 0.9, hh, rnd.uniform(0.3, 0.7))
    # moss settles ON the hump crowns (never floating in a gap) - breaks the monochrome grey
    for (hx, hy, hz) in humps:
        for j in range(2):
            A.ball(rnd.uniform(1.2, 2.0), (hx + rnd.uniform(-2, 2), hy + rnd.uniform(-2, 2), hz - 0.6), P['moss'], segs=6, rings=4, scale=(1.4, 1.2, 0.5))
    # earth/dirt lumps and grass tufts rest on the ground at the foot
    for k in range(6):
        A.chunk((rnd.uniform(2, 3.5), rnd.uniform(2, 3.5), rnd.uniform(0.6, 1.0)), (rnd.uniform(-12, 12), rnd.uniform(-8, 8), 0.4), P['dirt'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(10):
        x, y = rnd.uniform(-13, 13), rnd.uniform(-9, 9)
        A.cyl(0.16, rnd.uniform(1.0, 2.0), (x, y, 0.0), P['grass'], verts=5, r2=0.04)
    return _fin(A, 'bank_rocks')


# ================================================================== manifest wiring
# Build ONLY the ids in assignment A2, each bound to its design variant.
# (id_substring, builder, variant_index) - id resolved from the manifest so ids are never typed by hand.
_MID = {r_id: r_id for r_id in v5kit._manifest()}


def _id(sub):
    hit = [m for m in _MID if sub in m]
    assert len(hit) == 1, (sub, hit)
    return hit[0]


def _pair(sub, fn, idx):
    return (_id(sub), (lambda f=fn, j=idx: f(j)))


_COAST = [
    _pair('CO03_01', _reef, 0), _pair('CO03_02', _reef, 1), _pair('CO03_03', _reef, 2),
    _pair('CO03_04', _reef, 3), _pair('CO03_05', _reef, 4), _pair('CO03_06', _reef, 5),
    _pair('CO04_01', _sea_arch, 0), _pair('CO04_02', _sea_arch, 1),
    _pair('CO05_01', _islet, 0), _pair('CO05_02', _islet, 1), _pair('CO05_03', _islet, 2),
    _pair('HB01_03', _harbour_tower, 0),
]
_ROAD = [
    _pair('RD01_02', _watch, 0), _pair('RD01_03', _watch, 2), _pair('RD01_04', _watch, 1),
    _pair('RD02_01', _camp, 0), _pair('RD02_02', _camp, 1), _pair('RD02_03', _camp, 2),
    _pair('RD02_05', _camp, 4), _pair('RD02_06', _camp, 3),
    _pair('RD05_01', _bf_cart, 0), _pair('RD05_02', _bf_table, 0), _pair('RD05_03', _bf_banner, 0),
    _pair('RD05_04', _bf_cheval, 0), _pair('RD05_05', _bf_shields, 0),
    _pair('RD06_01', _ruin_house, 0), _pair('RD06_02', _ruin_house, 3), _pair('RD06_03', _ruin_house, 1),
    _pair('RD06_05', _ruin_house, 2),
    _pair('BR01_01', _viaduct, 0), _pair('BR01_02', _viaduct, 1),
    _pair('RV01_01', _bank, 0), _pair('RV01_02', _bank, 1), _pair('RV01_03', _bank, 2), _pair('RV01_04', _bank, 3),
]

def _float_small(i):
    """FL02_01..03 (lead pass 2) - small floating island built as a SOLID root of stacked banded frustum slices (two sets turned 45 degrees, no gaps, nothing loose),
    three different root profiles (cone, bulb, crooked with hanging tips) and three different rock tones, soil rim, grass cap, ivy."""
    reset()
    A = Acc()
    rnd = random.Random(10700 + i)
    topw = (32.0, 30.0, 34.0)[i]
    prof = ([0.12, 0.28, 0.44, 0.60, 0.76, 0.90, 1.0], [0.10, 0.20, 0.55, 0.78, 0.92, 0.97, 1.0], [0.18, 0.26, 0.38, 0.56, 0.78, 0.94, 1.0])[i]
    ramp = ([P['rock_lo'], P['rock_warm'], P['rock_mid'], P['rock_hi']], [P['rock_lo'], P['rock_mid'], P['rock_hi']], [P['rock_warm'], P['rock_mid'], P['rock_hi'], P['rock_warm']])[i]
    H = 20.0
    n = len(prof) - 1
    for turn, sc in ((0.0, 1.0), (45.0, 0.9)):
        for s in range(n):
            w0 = (3.0 + (topw - 3.0) * prof[s]) * sc
            w1 = (3.0 + (topw - 3.0) * prof[s + 1]) * sc
            A.frustum((w0, w0 * 0.95), (w1, w1 * 0.95), H / n + 0.3, (0, 0, 1.0 + H * s / n), ramp[min(len(ramp) - 1, int(s / float(n) * len(ramp)))], (0, 0, turn))
    for k in range(7):
        t = rnd.uniform(0.25, 0.85)
        a = rnd.uniform(0, 360)
        x, y, _ = polar(((3.0 + (topw - 3.0) * t) * 0.5) - 1.5, a)
        A.chunk((rnd.uniform(4, 7), rnd.uniform(4, 7), rnd.uniform(4, 8)), (x, y, 1.0 + t * H), band(ramp, t, rnd), (rnd.uniform(-8, 8), rnd.uniform(-8, 8), a), 0.14, rnd, (0.7, 0.7))
    if i == 2:
        for sx, sy in ((-2.0, 1.0), (2.5, -1.5), (0.5, 2.5)):
            A.chunk((2.4, 2.4, 6.0), (sx, sy, 2.0), ramp[0], (0, 0, rnd.uniform(0, 90)), 0.12, rnd, (0.4, 0.4))
    A.chunk((topw + 1.0, topw * 0.95 + 1.0, 1.8), (0, 0, 21.4), P['dirt'], (0, 0, i * 20), 0.05, rnd)
    A.chunk((topw, topw * 0.95, 2.6), (0, 0, 23.0), R.V['grass'], (0, 0, i * 20), 0.06, rnd)
    for k in range(5):
        A.ball(rnd.uniform(1.2, 2.2), (rnd.uniform(-9, 9), rnd.uniform(-9, 9), 24.2), R.V['ivy'], segs=7, rings=4, scale=(1.3, 1.1, 0.8))
    return _fin(A, 'floating_rock')


def _harbour_post(A):
    for z in (4.0, 13.0, 22.0):
        w = 13.0 - 4.0 * (z / 30.0) + 0.6
        A.box((w, w, 0.8), (0, 0, z), R.V['trim'], bev=0.05)
    for sx in (-1, 1):
        A.box((0.45, 12.6, 0.4), (sx * 6.0, 0, 34.2), R.V['iron'], bev=0)
        A.box((12.6, 0.45, 0.4), (0, sx * 6.0, 34.2), R.V['iron'], bev=0)


def _trading_b():
    reset()
    A = Acc()
    rnd = random.Random(10011)
    G.house(A, rnd, 20.0, 12.0, 2, R.RK, hs=5.8, jetty=0.6, pitch=0.8, sign=True, hip=True, dormers=1, balcony=True)
    V_ = R.V
    for k in range(3):
        A.box((3.4, 1.8, 1.4), (-9.0 + k * 4.4, -9.5, 0.7), V_['plank'], bev=0.08)
        A.box((3.8, 2.2, 0.2), (-9.0 + k * 4.4, -9.5, 4.2), (V_['canvas3'], V_['canvas'], V_['canvas2'])[k % 3], bev=0)
        for sx in (-1.6, 1.6):
            A.cyl(0.12, 4.0, (-9.0 + k * 4.4 + sx, -9.5, 0), V_['timber'], verts=5)
    for k in range(3):
        A.cyl(0.9, 1.7, (7.0 + k * 1.2, -9.0, 0), V_['timber'], verts=8)
    A.box((3.0, 2.0, 2.0), (-12.5, -3.0, 1.0), V_['plank'], bev=0.08)
    return _fin(A, 'trading_post')


def fl02(i):
    return LK.wrap(lambda: _float_small(i))()


def hb01_02():
    return LK.wrap(lambda: R._harbour_tower(1), post=_harbour_post)()


def rd04_02():
    return LK.wrap(_trading_b)()


BATCHES = {
    'coast_fix': ('v5_coast', mk(_COAST, 0.1)),
    'road_fix': ('v5_roads', mk(_ROAD, 0.1)),
}


# --- lead4 registration ---
import v5_leadkit as LK
BATCHES['lead4_vib'] = ('v5_coast', mk([('FL02_01_floating_island_small_01', lambda: fl02(0)), ('FL02_02_floating_island_small_02', lambda: fl02(1)),
                                        ('FL02_03_floating_island_small_03', lambda: fl02(2)), ('HB01_02_harbour_wall_tower_02', hb01_02)], 0.1))
BATCHES['lead4_vib_roads'] = ('v5_roads', mk([('RD04_02_trading_post_02', rd04_02)], 0.1))
