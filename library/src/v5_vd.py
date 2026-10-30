"""vd module - the capital and castle town (original design, one dominant orange-red roof family, grey-lilac stone, maroon cone roofs).
CP01 ring walls, CP02 corners, CP03 stair ends, CP04 towers, CP05 turrets, CP06 gate flank towers, CP07 gatehouse, CP08 water gate,
CP09 keep, CP10 wings, CP11 hall + chapel, CP12 terrace walls, CP13 stairs, CP14 skyline towers, CP15 order hall + annexes,
CP16 townhouses, CP17 plaza features, CP18 quay walls, CP19 bridges. Front faces -Y. No glow. Gatehouses stay (a wall needs a gate).
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v5kit
from v5kit import Acc, polar, tang, mk
import v5gen as G
from v5gen import house, round_tower, wall_seg, column
import v4util

K = G.reg('vd', {
    'wall': ((232, 214, 188), 'Concrete', 0.0, 0.9), 'timber': ((112, 80, 60), 'Wood', 0.0, 0.88), 'roof': ((198, 88, 52), 'Brick', 0.0, 0.85),
    'roof2': ((176, 72, 46), 'Brick', 0.0, 0.85), 'cap': ((140, 62, 48), 'Brick', 0.0, 0.85), 'stone': ((150, 142, 158), 'Slate', 0.0, 0.92),
    'cone': ((120, 44, 52), 'Slate', 0.0, 0.8), 'deck': ((150, 88, 70), 'Brick', 0.0, 0.85), 'trim': ((232, 226, 230), 'Limestone', 0.0, 0.88),
    'glass': ((86, 104, 128), 'SmoothPlastic', 0.0, 0.3), 'shutter': ((70, 100, 94), 'Wood', 0.0, 0.85), 'door': ((92, 62, 46), 'Wood', 0.0, 0.85),
    'iron': ((58, 58, 66), 'Metal', 0.6, 0.6), 'sign': ((184, 142, 72), 'WoodPlanks', 0.0, 0.85), 'gold': ((204, 168, 88), 'Metal', 0.8, 0.35),
    'dark': ((40, 36, 42), 'Slate', 0.0, 0.9), 'flag': ((168, 52, 52), 'Fabric', 0.0, 1.0), 'grass': ((96, 142, 70), 'Grass', 0.0, 1.0),
    'water': ((70, 120, 160), 'SmoothPlastic', 0.0, 0.2), 'copper': ((96, 150, 128), 'Metal', 0.45, 0.55),
})


def _fin(A, name):
    A.to_scene()
    return finalize(name, 25)


# ------------------------------------------------------------------ CP01-CP03 ring wall pieces
def _wall(slits=False, buttress=False):
    reset()
    A = Acc()
    wall_seg(A, random.Random(1 + slits * 2 + buttress * 3), 40.0, 16.0, 9.0, K, 0, 0, 0, 7.0, slits, buttress)
    return _fin(A, 'ring_wall_straight')


def wall_1():
    return _wall()


def wall_2():
    return _wall(slits=True)


def wall_3():
    return _wall(buttress=True)


def _corner(angle, seed):
    reset()
    A = Acc()
    rnd = random.Random(seed)
    arm = Acc()
    wall_seg(arm, rnd, 16.0, 16.0, 9.0, K, 8.0, 0, 0, 7.0, seed % 2 == 0, False)
    A.append(arm)
    A.append(arm, rot=(0, 0, angle), scale=(1, -1, 1))
    t = Acc()
    round_tower(t, rnd, 6.8, 20.0, K, 0, 0, 0, top='crenel', slits=2, bands=2)
    A.append(t, (0, 0, 0))
    return _fin(A, 'ring_wall_corner')


def corner_1():
    return _corner(135, 11)


def corner_2():
    return _corner(90, 12)


def corner_3():
    return _corner(150, 13)


def _stair_end(flip):
    reset()
    A = Acc()
    rnd = random.Random(21 + flip)
    wall_seg(A, rnd, 20.0, 16.0, 9.0, K, 0, 0, 0, 7.0, False, False)
    s = -1 if flip else 1
    for i in range(14):                                                                       # stair on the inner side up to the wall-walk
        A.box((1.5, 3.4, 1.2 * (i + 1)), (s * (-9.0 + i * 1.3), 7.4, 0.6 * (i + 1)), K['stone'], bev=0.08)
    A.box((19.0, 0.6, 0.5), (0, 9.4, 1.0), K['trim'])
    for i in range(0, 14, 3):
        A.beam((s * (-9.0 + i * 1.3), 9.2, 1.2 * (i + 1) + 0.8), (s * (-9.0 + i * 1.3), 9.2, 1.2 * (i + 1) + 3.0), 0.4, 0.4, K['timber'])
    A.beam((s * -9.0, 9.2, 2.8), (s * 9.2, 9.2, 19.5), 0.35, 0.35, K['timber'])
    round_tower(A, rnd, 2.8, 22.0, K, s * 11.0, -0.5, 0, top='crenel', slits=1, bands=1, verts=14)
    return _fin(A, 'ring_wall_stair_end')


def stair_end_1():
    return _stair_end(0)


def stair_end_2():
    return _stair_end(1)


# ------------------------------------------------------------------ CP04-CP06 towers
def _tower(r, h, seed, door, top='cone', roof_k=1.2, flag=False):
    reset()
    A = Acc()
    rnd = random.Random(seed)
    round_tower(A, rnd, r, h, K, 0, 0, 0, top=top, slits=3, bands=3, door=door, flag=flag, roof_k=roof_k)
    if top == 'crenel':
        for k in range(6):                                                                    # banner mounts
            pass
    return _fin(A, 'tower_round_cone')


def tower_1():
    return _tower(8.0, 29.0, 31, False)


def tower_2():
    return _tower(11.0, 31.0, 32, True, flag=True)


def tower_3():
    return _tower(14.0, 33.0, 33, False, roof_k=1.1)


def tower_4():
    return _tower(17.0, 34.0, 34, True, roof_k=1.0, flag=True)


def turret_1():
    reset()
    A = Acc()
    round_tower(A, random.Random(41), 7.0, 21.0, K, top='crenel', slits=2, bands=2, verts=16)
    return _fin(A, 'turret_crenellated')


def turret_2():
    reset()
    A = Acc()
    round_tower(A, random.Random(42), 6.5, 18.0, K, top='crenel', slits=2, bands=1, verts=16)
    for k in range(8):
        x, y, _ = polar(6.9, k * 45.0)
        A.box((0.5, 0.5, 5.0 if k % 2 else 4.0), (x, y, 21.2), K['iron'], bev=0)
    A.cyl(7.6, 5.0, (0, 0, 20.0), K['cone'], verts=16, r2=0.5) if False else A.cyl(7.6, 7.0, (0, 0, 19.0), K['cone'], verts=16, r2=0.0)
    return _fin(A, 'turret_crenellated')


def _flank(seed, cone):
    reset()
    A = Acc()
    rnd = random.Random(seed)
    round_tower(A, rnd, 14.0, 40.0, K, top='cone' if cone else 'crenel', slits=3, bands=3, roof_k=0.9, flag=cone, verts=28)
    for sg in (-1, 1):                                                                        # banner mount on the gate side
        x, y, _ = polar(14.4, 270 + sg * 24.0)
        A.beam((x, y, 30.0), (x * 1.25, y * 1.25, 30.5), 0.4, 0.4, K['iron'])
        A.box((0.2, 3.0, 8.0), (x * 1.25, y * 1.25, 26.0), K['flag'], (0, 0, 270 + sg * 24.0), bev=0)
    return _fin(A, 'gate_flank_tower')


def flank_1():
    return _flank(51, True)


def flank_2():
    return _flank(52, False)


# ------------------------------------------------------------------ CP07 gatehouse, CP08 water gate
def _portal_block(A, rnd, W, D, H, ow, oh, K, y=0.0):
    """Wall mass with a vaulted passage (ow wide, straight to oh then a half-round vault) running along Y."""
    rv = ow / 2.0
    A.box((W + 2.0, D + 2.0, 3.0), (0, y, 1.5), K['stone'])
    for sg in (-1, 1):
        xc = sg * ((W / 2.0 + ow / 2.0 + 1.0) / 2.0)
        wd = W / 2.0 - ow / 2.0 - 1.0
        A.frustum((wd * 2.0 + 0.0, D), (wd * 2.0 - 1.6, D - 1.6), H - 3.0, (sg * (ow / 2.0 + wd), y, 3.0), K['wall']) if False else \
            A.box((W / 2.0 - ow / 2.0, D, H - 3.0), (sg * (ow / 2.0 + (W / 2.0 - ow / 2.0) / 2.0), y, 3.0 + (H - 3.0) / 2.0), K['wall'])
    A.box((ow + 2.0, D, H - oh - rv - 3.0), (0, y, oh + rv + 3.0 + (H - oh - rv - 3.0) / 2.0 + 0.0), K['wall'])
    A.sweep([(rv, -D / 2.0), (rv + 2.4, -D / 2.0), (rv + 2.4, D / 2.0), (rv, D / 2.0)], 0, 180, 12, K['trim'], loc=(0, y, oh + 3.0), rot=(90, 0, 0))
    A.box((ow + 0.0, D, 0.6), (0, y, 3.3), K['deck'])
    for sg in (-1, 1):
        A.box((0.8, D, oh), (sg * (ow / 2.0 + 0.4), y, 3.0 + oh / 2.0), K['dark'])
        A.sweep([(rv - 0.8, -D / 2.0), (rv, -D / 2.0), (rv, D / 2.0), (rv - 0.8, D / 2.0)], 0, 180, 12, K['dark'], loc=(0, y, oh + 3.0), rot=(90, 0, 0)) if sg > 0 else None


def gatehouse():
    reset()
    A = Acc()
    rnd = random.Random(61)
    W, D, H, ow, oh = 60.0, 40.0, 44.0, 14.0, 12.0
    _portal_block(A, rnd, W, D, H, ow, oh, K)
    yf = -D / 2.0
    for k in range(9):                                                                        # portcullis, half raised
        A.box((0.45, 0.45, 12.0), (-5.6 + k * 1.4, yf + 3.0, oh + 3.0 + 3.0), K['iron'], bev=0)
    for z in (13.5, 16.5, 19.5):
        A.box((12.0, 0.45, 0.45), (0, yf + 3.0, z), K['iron'], bev=0)
    A.box((W + 1.0, D + 1.0, 1.0), (0, 0, H + 0.5), K['trim'])
    for k in range(int(W / 4.0)):                                                             # machicolation brackets and battlements
        x = -W / 2.0 + 2.0 + k * 4.0
        A.box((1.4, 1.6, 1.8), (x, yf - 0.8, H - 1.0), K['stone'])
        A.box((2.4, 1.2, 2.4), (x, yf + 0.4, H + 2.1), K['wall'])
        A.box((2.7, 1.5, 0.4), (x, yf + 0.4, H + 3.5), K['cap'])
        A.box((2.4, 1.2, 2.4), (x, -yf - 0.4, H + 2.1), K['wall'])
    A.box((W, 2.2, 0.8), (0, yf - 1.2, H - 2.2), K['trim'])
    for sg in (-1, 1):                                                                        # banner poles and banners
        A.cyl(0.25, 14.0, (sg * 22.0, yf - 0.5, H - 6.0), K['timber'], verts=6)
        A.box((0.2, 4.2, 9.0), (sg * 22.0, yf - 0.8, H - 1.5), K['flag'], (0, 0, 0), bev=0)
    for z in (22.0, 30.0):                                                                    # window rows
        for sg in (-1, 1):
            for xs in (-20.0, -12.0, 12.0, 20.0):
                A.box((2.0, 0.4, 3.4), (xs, yf - 0.1, z), K['glass'], bev=0)
                A.box((2.8, 0.5, 0.5), (xs, yf - 0.1, z + 2.0), K['trim'], bev=0)
            break
    for sg in (-1, 1):
        A.box((9.0, 0.9, 12.0), (sg * 15.0, yf - 0.4, 14.0), K['timber'], bev=0.1)
        A.box((7.0, 0.9, 1.0), (sg * 15.0, yf - 0.5, 20.4), K['gold'], bev=0)
    v4util.marker('mk_door', (0, yf, 3.4))
    return _fin(A, 'gatehouse_main')


def water_gate():
    reset()
    A = Acc()
    rnd = random.Random(62)
    W, D, H, ow, oh = 40.0, 30.0, 30.0, 16.0, 9.0
    _portal_block(A, rnd, W, D, H, ow, oh, K)
    yf = -D / 2.0
    A.box((ow, D + 2.0, 1.0), (0, 0, 3.5), K['dark'])
    for k in range(9):                                                                        # iron grille over the channel
        A.box((0.4, 0.4, oh + 6.0), (-6.4 + k * 1.6, yf + 2.0, 3.0 + (oh + 6.0) / 2.0), K['iron'], bev=0)
    for z in (6.0, 9.5, 13.0):
        A.box((ow, 0.4, 0.4), (0, yf + 2.0, z), K['iron'], bev=0)
    A.box((W + 1.0, D + 1.0, 1.0), (0, 0, H + 0.5), K['trim'])
    for k in range(int(W / 4.0)):
        x = -W / 2.0 + 2.0 + k * 4.0
        A.box((2.4, 1.2, 2.2), (x, yf + 0.4, H + 2.0), K['wall'])
    for sg in (-1, 1):
        for k in range(5):                                                                    # steps down to the water on each bank
            A.box((5.0, 3.0, 1.0), (sg * (ow / 2.0 + 6.0), yf - 1.5 - k * 0.0, 3.5 - k * 0.0), K['stone']) if False else None
        A.box((3.0, 14.0, 2.0), (sg * (W / 2.0 + 2.0), 0, 1.0), K['stone'])
        round_tower(A, rnd, 3.4, H + 6.0, K, sg * (W / 2.0 - 3.0), yf + 3.0, 0, top='cone', slits=1, bands=1, verts=14, roof_k=1.3)
    return _fin(A, 'water_gate')


# ------------------------------------------------------------------ CP09 keep, CP10 wings, CP11 hall + chapel
def _stone_block(A, rnd, w, d, h, cx=0.0, cy=0.0, z0=0.0, rows=3, crenel=True, buttress=True, roof=None):
    A.frustum((w, d), (w - 1.6, d - 1.6), h, (cx, cy, z0), K['stone'])
    for sy, face in ((-1, 270), (1, 90)):
        yy = cy + sy * (d / 2.0)
        for r_ in range(rows):
            zz = z0 + (r_ + 0.6) * h / (rows + 0.3)
            for i in range(int(w / 6.5)):
                x = cx - w / 2.0 + 4.0 + i * 6.5
                G._window(A, x, yy, zz, face, K, 1.8, 3.4, False, K['trim'])
    for sx, face in ((-1, 180), (1, 0)):
        for r_ in range(rows):
            zz = z0 + (r_ + 0.6) * h / (rows + 0.3)
            for i in range(int(d / 8.0)):
                G._window(A, cx + sx * (w / 2.0), cy - d / 2.0 + 4.0 + i * 8.0, zz, face, K, 1.8, 3.4, False, K['trim'])
    for r_ in range(1, 3):
        A.box((w + 0.6, d + 0.6, 0.5), (cx, cy, z0 + h * r_ / 3.0), K['trim'], bev=0)
    if buttress:
        for i in range(int(w / 9.0)):
            x = cx - w / 2.0 + 4.5 + i * 9.0
            A.box((2.2, 2.6, h * 0.8), (x, cy - d / 2.0 - 0.9, z0 + h * 0.4), K['stone'], bev=0.1)
    if crenel:
        A.box((w + 0.8, d + 0.8, 0.9), (cx, cy, z0 + h + 0.45), K['trim'])
        for i in range(int(w / 4.0)):
            x = cx - w / 2.0 + 2.0 + i * 4.0
            A.box((2.4, 1.2, 2.0), (x, cy - d / 2.0 - 0.2, z0 + h + 1.9), K['stone'], bev=0.08)
            A.box((2.4, 1.2, 2.0), (x, cy + d / 2.0 + 0.2, z0 + h + 1.9), K['stone'], bev=0.08)
    if roof:
        A.gable(d + 3.0, w + 3.0, (d + 3.0) * 0.5, (cx, cy, z0 + h), K['roof'], (0, 0, 90))


def keep():
    reset()
    A = Acc()
    rnd = random.Random(71)
    for i, (w, d) in enumerate(((130.0, 110.0), (122.0, 102.0), (114.0, 94.0))):             # raised grassy terrace, three tiers
        A.box((w, d, 3.0), (0, 0, 1.5 + i * 3.0), K['stone'], bev=0.3)
    A.box((106.0, 86.0, 0.8), (0, 0, 9.4), K['grass'], bev=0)
    for sg in (-1, 1):
        for k in range(14):
            A.box((2.0, 2.0, 2.4), (sg * 56.0, -45.0 + k * 6.5, 10.9), K['trim'], bev=0.08)
    _stone_block(A, rnd, 74.0, 46.0, 38.0, 0, 10.0, 9.8, 4, True, True)                       # great hall block
    A.gable(48.0, 76.0, 14.0, (0, 10.0, 47.8), K['roof'], (0, 0, 90))
    _stone_block(A, rnd, 34.0, 34.0, 62.0, 0, 28.0, 9.8, 6, True, False)                      # central keep tower
    A.frustum((38.0, 38.0), (4.0, 4.0), 34.0, (0, 28.0, 71.8 + 0.0), K['cone'])
    A.cyl(0.5, 10.0, (0, 28.0, 105.8), K['iron'], verts=6)
    A.box((0.2, 5.0, 3.0), (0, 28.0, 112.0), K['flag'], bev=0)
    corners = [(-40.0, -10.0, 9.0, 52.0), (40.0, -10.0, 9.0, 52.0), (-40.0, 30.0, 9.0, 52.0), (40.0, 30.0, 9.0, 52.0),
               (-18.0, -16.0, 6.0, 38.0), (18.0, -16.0, 6.0, 38.0), (-52.0, 10.0, 5.5, 34.0), (52.0, 10.0, 5.5, 34.0)]
    for i, (x, y, r, h) in enumerate(corners):
        round_tower(A, rnd, r, h, K, x, y, 9.8, top='cone', slits=3, bands=3, roof_k=1.6, verts=20, flag=(i < 4))
    for sg in (-1, 1):                                                                         # covered bridges between the towers
        A.box((20.0, 3.4, 4.2), (sg * 29.0, -10.0, 9.8 + 34.0), K['wall'])
        A.gable(5.0, 20.0, 2.0, (sg * 29.0, -10.0, 9.8 + 36.1), K['roof'], (0, 0, 90))
    A.box((16.0, 2.4, 8.0), (0, -13.4, 9.8 + 4.0), K['timber'], bev=0.1)                       # front porch and doors
    A.box((12.0, 0.6, 6.4), (0, -14.7, 9.8 + 3.4), K['door'])
    A.gable(18.0, 6.0, 5.0, (0, -13.4, 9.8 + 8.0), K['roof'], (0, 0, 90))
    for k in range(7):
        A.box((16.0 - k * 1.6, 1.6, 0.55), (0, -17.0 - k * 1.6 + 6.0, 9.4 - k * 0.0 + 0.0 - k * 0.0), K['stone']) if False else None
    for i in range(6):                                                                         # grand front stair down the terrace
        A.box((26.0 - i * 1.2, 2.4, 1.6), (0, -50.0 - i * 1.0, 9.0 - i * 1.5), K['stone'], bev=0.1)
    return _fin(A, 'keep_terrace_hero')


def _wing(var):
    reset()
    A = Acc()
    rnd = random.Random(80 + var)
    _stone_block(A, rnd, 46.0 if var == 1 else 40.0, 28.0, 30.0, 0, 0, 0, 3, True, True)
    A.gable(31.0, 48.0 if var == 1 else 42.0, 12.0, (0, 0, 30.0), K['roof'], (0, 0, 90))
    round_tower(A, rnd, 7.5, 44.0, K, -24.0 if var == 1 else -21.0, -10.0, 0, top='cone', slits=3, bands=2, roof_k=1.5, verts=20)
    round_tower(A, rnd, 5.5, 36.0, K, 24.0 if var == 1 else 21.0, 8.0, 0, top='cone', slits=2, bands=2, roof_k=1.5, verts=16, flag=True)
    if var == 2:                                                                               # chapel apse on the wing
        A.cyl(12.0, 24.0, (0, 20.0, 0), K['stone'], verts=14)
        A.cyl(13.0, 12.0, (0, 20.0, 24.0), K['cone'], verts=14, r2=0.0)
    return _fin(A, 'keep_wing')


def wing_1():
    return _wing(1)


def wing_2():
    return _wing(2)


def hall_chapel(var):
    reset()
    A = Acc()
    rnd = random.Random(90 + var)
    if var == 1:                                                                               # great hall: long block, tall windows, buttresses, louvred lantern
        _stone_block(A, rnd, 60.0, 30.0, 26.0, 0, 0, 0, 2, True, True)
        A.gable(32.0, 62.0, 16.0, (0, 0, 26.0), K['roof'], (0, 0, 90))
        for k in range(4):
            A.box((3.0, 3.0, 6.0), (-18.0 + k * 12.0, 0, 42.0 + 3.0), K['wall']) if False else None
        A.box((6.0, 6.0, 7.0), (0, 0, 40.0), K['wall'])
        A.cyl(4.6, 6.0, (0, 0, 47.0), K['cone'], verts=6, r2=0.0)
        round_tower(A, rnd, 5.0, 34.0, K, -30.0, -15.0, 0, top='cone', roof_k=1.5, verts=16)
        round_tower(A, rnd, 5.0, 34.0, K, 30.0, -15.0, 0, top='cone', roof_k=1.5, verts=16)
        A.box((12.0, 4.0, 9.0), (0, -17.0, 4.5), K['timber'], bev=0.1)
    else:                                                                                      # royal chapel: nave, apse, bell tower with a spire
        _stone_block(A, rnd, 40.0, 24.0, 22.0, 0, 6.0, 0, 2, True, True)
        A.gable(26.0, 42.0, 14.0, (0, 6.0, 22.0), K['cone'], (0, 0, 90))
        A.cyl(12.0, 22.0, (0, 30.0 - 6.0, 0), K['stone'], verts=14)
        A.cyl(13.0, 9.0, (0, 24.0, 22.0), K['cone'], verts=14, r2=0.0)
        round_tower(A, rnd, 6.0, 40.0, K, -22.0, -4.0, 0, top='cone', roof_k=2.4, verts=12, slits=3)
        A.box((7.0, 7.0, 3.0), (0, -9.0, 24.0 + 0.0), K['trim']) if False else None
        A.cyl(0.4, 4.0, (0, 6.0, 36.0), K['gold'], verts=6)
        A.box((0.4, 0.4, 2.4), (0, 6.0, 40.4), K['gold'], bev=0)
        A.box((1.6, 0.4, 0.4), (0, 6.0, 40.8), K['gold'], bev=0)
        A.box((9.0, 3.0, 8.0), (0, -8.0, 4.0), K['timber'], bev=0.1)
    return _fin(A, 'hall_chapel')


def hall_1():
    return hall_chapel(1)


def hall_2():
    return hall_chapel(2)


# ------------------------------------------------------------------ CP12 terrace walls, CP13 stairs
def terrace_wall_s():
    reset()
    A = Acc()
    rnd = random.Random(101)
    cliff_keys = [K['stone'], K['wall'], K['stone']]
    for k in range(10):
        for z in range(5):
            A.chunk((4.2, 7.0 - z * 0.4, 4.6), (-18.0 + k * 4.0, 0, 2.3 + z * 4.3), cliff_keys[(k + z) % 3], (0, 0, 0), 0.06, rnd, (0.97, 0.93))
    A.box((41.0, 8.0, 0.9), (0, 0, 22.0), K['trim'])
    A.box((41.0, 7.0, 0.6), (0, 0, 22.6), K['grass'], bev=0)
    for k in range(9):
        A.box((1.6, 1.6, 6.0), (-18.0 + k * 4.5, -3.8, 12.0), K['stone'], bev=0.1)
    return _fin(A, 'terrace_retaining_wall')


def terrace_wall_c():
    reset()
    A = Acc()
    rnd = random.Random(102)
    R = 24.0
    for z in range(5):
        A.sweep([(R - 4.0 + z * 0.3, z * 4.3), (R + 4.0 - z * 0.3, z * 4.3), (R + 4.0 - z * 0.3, z * 4.3 + 4.4), (R - 4.0 + z * 0.3, z * 4.3 + 4.4)], 0, 90, 9,
                K['stone'] if z % 2 else K['wall'])
    A.sweep([(R - 4.0, 21.5), (R + 4.0, 21.5), (R + 4.0, 22.4), (R - 4.0, 22.4)], 0, 90, 9, K['trim'])
    A.sweep([(R - 3.4, 22.4), (R + 3.4, 22.4), (R + 3.4, 23.0), (R - 3.4, 23.0)], 0, 90, 9, K['grass'])
    for a in (8, 30, 52, 74):
        x, y, _ = polar(R + 4.4, a)
        A.box((1.6, 1.6, 17.0), (x, y, 9.0), K['stone'], (0, 0, a), bev=0.1)
    return _fin(A, 'terrace_retaining_wall')


def _grand_stair(width, steps):
    reset()
    A = Acc()
    rise = 22.0 / steps
    run = 40.0 / steps
    for i in range(steps):
        A.box((width, run + 0.05, rise * (i + 1)), (0, -20.0 + run * (i + 0.5), rise * (i + 1) / 2.0), K['stone'] if i % 6 else K['trim'], bev=0.06)
    for sg in (-1, 1):
        for i in range(steps):
            A.box((2.6, run + 0.05, rise * (i + 1) + 1.6), (sg * (width / 2.0 + 1.3), -20.0 + run * (i + 0.5), (rise * (i + 1) + 1.6) / 2.0), K['wall'], bev=0.06)
        for i in range(0, steps, 6):
            A.box((3.0, 3.0, 1.0), (sg * (width / 2.0 + 1.3), -20.0 + run * (i + 0.5), rise * (i + 1) + 2.0), K['trim'])
            A.cyl(0.35, 2.4, (sg * (width / 2.0 + 1.3), -20.0 + run * (i + 0.5), rise * (i + 1) + 2.5), K['iron'], verts=6)
    A.box((width + 5.2, 4.0, 22.0), (0, 18.0, 11.0), K['stone'])
    return _fin(A, 'grand_stair')


def stair_wide():
    return _grand_stair(20.0, 36)


def stair_narrow():
    return _grand_stair(8.0, 40)


# ------------------------------------------------------------------ CP14 skyline towers
def _shaft(A, w, h, z0=0.0, key=None, bands=5):
    A.frustum((w + 2.0, w + 2.0), (w, w), 3.0, (0, 0, z0), K['stone'])
    A.frustum((w, w), (w - 1.6, w - 1.6), h - 3.0, (0, 0, z0 + 3.0), key or K['wall'])
    for k in range(bands):
        A.box((w + 0.4, w + 0.4, 0.55), (0, 0, z0 + 3.0 + (h - 3.0) * (k + 1) / (bands + 1)), K['trim'], bev=0.05)
    for z in (0.3, 0.55, 0.8):
        for face in (270, 0, 90, 180):
            x, y, _ = polar(w / 2.0 + 0.02, face)
            A.box((0.4, 1.0, 3.0), (x, y, z0 + h * z), K['dark'], (0, 0, face), bev=0)


def sky_clock():
    reset()
    A = Acc()
    _shaft(A, 14.0, 78.0)
    A.box((15.0, 15.0, 1.0), (0, 0, 79.5), K['trim'])
    A.box((13.0, 13.0, 14.0), (0, 0, 86.0), K['wall'])
    for face in (270, 0, 90, 180):                                                             # clock faces
        x, y, _ = polar(6.6, face)
        A.cyl(4.6, 0.6, (x, y, 86.0), K['trim'], verts=24, rot=(0, 90, face) if False else (90, 0, face - 90))
        A.cyl(4.0, 0.2, (x * 1.01, y * 1.01, 86.0), K['dark'], verts=24, rot=(90, 0, face - 90))
        for h_ in range(12):
            xa, ya, za = polar(3.4, h_ * 30.0)
            tx, ty = tang(face)
            A.box((0.2, 0.6, 0.6), (x * 1.04 + 0.0, y * 1.04, 86.0 + za), K['gold'], (0, 0, face), bev=0) if False else None
        A.box((0.2, 0.3, 3.2), (x * 1.06, y * 1.06, 87.4), K['gold'], (0, 0, face), bev=0)
        A.box((0.2, 2.6, 0.3), (x * 1.06, y * 1.06, 86.0), K['gold'], (0, 0, face), bev=0)
    A.frustum((15.0, 15.0), (2.0, 2.0), 17.0, (0, 0, 93.0), K['cone'])
    A.cyl(0.3, 9.0, (0, 0, 109.5), K['gold'], verts=6)
    A.ball(0.8, (0, 0, 118.5), K['gold'], segs=8, rings=5)
    return _fin(A, 'skyline_tower_clock')


def sky_bell():
    reset()
    A = Acc()
    r = 7.0
    A.cyl(r + 1.5, 3.0, (0, 0, 0), K['stone'], verts=20, r2=r + 0.3)
    A.cyl(r, 62.0, (0, 0, 3.0), K['wall'], verts=20, r2=r - 1.2)
    for k in range(4):
        A.sweep([(r - 1.8, -0.3), (r + 0.5, -0.3), (r + 0.5, 0.3), (r - 1.8, 0.3)], 0, 360, 20, K['trim'], loc=(0, 0, 3.0 + 15.0 * (k + 1)))
    A.cyl(r + 1.2, 1.0, (0, 0, 65.0), K['trim'], verts=20)
    for k in range(8):
        x, y, _ = polar(r - 0.4, k * 45.0)
        A.cyl(0.55, 12.0, (x, y, 66.0), K['stone'], verts=8)
        A.box((1.6, 1.6, 0.6), (x, y, 77.6), K['trim'], bev=0.05)
    A.cyl(r + 0.8, 1.0, (0, 0, 78.2), K['trim'], verts=20)
    A.revolve([(0.0, 14.0), (1.6, 13.8), (2.4, 11.6), (3.2, 8.8), (3.8, 6.4), (4.2, 5.2), (0.0, 5.2)], (0, 0, 68.0), K['gold'], segs=16)
    A.beam((0, -5, 82.0), (0, 5, 82.0), 0.5, 0.5, K['timber'])
    A.cyl(r + 1.6, 18.0, (0, 0, 79.2), K['cone'], verts=20, r2=0.0)
    A.revolve([(0.4, 0.0), (0.4, 3.2), (1.0, 3.6), (0.0, 5.5)], (0, 0, 96.6), K['gold'], segs=8)
    return _fin(A, 'skyline_tower_bell')


def sky_observatory():
    reset()
    A = Acc()
    r = 9.0
    A.cyl(r + 1.8, 3.0, (0, 0, 0), K['stone'], verts=24, r2=r + 0.4)
    A.cyl(r, 70.0, (0, 0, 3.0), K['wall'], verts=24, r2=r - 1.4)
    for k in range(5):
        A.sweep([(r - 2.4, -0.3), (r + 0.5, -0.3), (r + 0.5, 0.3), (r - 2.4, 0.3)], 0, 360, 24, K['trim'], loc=(0, 0, 3.0 + 11.5 * (k + 1)))
    A.cyl(r + 2.0, 1.4, (0, 0, 73.0), K['trim'], verts=24)
    A.sweep([(r + 1.9, 0.0), (r + 2.4, 0.0), (r + 2.4, 1.6), (r + 1.9, 1.6)], 0, 360, 24, K['iron'], loc=(0, 0, 74.4))
    rd = r + 0.6
    outer = [(rd * math.cos(math.radians(t)), 74.4 + 11.0 * math.sin(math.radians(t))) for t in range(0, 81, 10)]
    inner = [((rd - 1.2) * math.cos(math.radians(t)), 74.4 + 9.8 * math.sin(math.radians(t))) for t in range(80, -1, -10)]
    A.sweep(outer + [(0.8, 85.6)] + inner, 290.0, 610.0, 32, K['copper'])
    A.beam((0, -2.0, 74.6), (0, -9.0, 85.0), 1.0, 1.0, K['gold']) if False else None
    A.cyl(1.2, 11.0, (0, 1.0, 76.0), K['gold'], verts=10, r2=0.9, rot=(-52, 0, 0))
    A.revolve([(0.3, 0.0), (0.3, 3.0), (1.0, 3.4), (0.0, 5.0)], (0, 0, 85.4), K['gold'], segs=8)
    return _fin(A, 'skyline_tower_observatory')


def sky_beacon():
    reset()
    A = Acc()
    _shaft(A, 13.0, 84.0, 0.0, K['stone'], 6)
    A.box((18.0, 18.0, 1.2), (0, 0, 85.0), K['trim'])
    for sx in (-1, 1):
        for sy in (-1, 1):
            A.box((0.9, 0.9, 6.0), (sx * 8.0, sy * 8.0, 89.0), K['iron'], bev=0.05)
    for z in (87.0, 91.0):
        for sg in (-1, 1):
            A.box((16.0, 0.4, 0.4), (0, sg * 8.0, z), K['iron'], bev=0)
            A.box((0.4, 16.0, 0.4), (sg * 8.0, 0, z), K['iron'], bev=0)
    A.cyl(3.0, 2.0, (0, 0, 86.2), K['iron'], verts=8, r2=4.4)                                  # brazier bowl (unlit)
    for k in range(7):
        x, y, _ = polar(2.2, k * 51.4)
        A.cyl(0.3, 4.0, (x, y, 88.0), K['dark'], verts=5, r2=0.1, rot=(rnd_t := 0, 0, 0)) if False else A.cyl(0.4, 3.5 + (k % 3), (x, y, 88.0), K['dark'], verts=5, r2=0.1)
    A.frustum((18.0, 18.0), (6.0, 6.0), 3.0, (0, 0, 93.0), K['cone'])
    for k in range(10):
        A.box((10.0, 0.6, 1.0), (0, 0, 14.0 * k + 1.0 + 0.0), K['timber'], (0, 0, 45.0)) if False else None
    return _fin(A, 'skyline_tower_beacon')


def sky_water():
    reset()
    A = Acc()
    for sx in (-1, 1):
        for sy in (-1, 1):
            A.beam((sx * 11.0, sy * 11.0, 0.0), (sx * 7.0, sy * 7.0, 56.0), 2.0, 2.0, K['timber'])
            A.cyl(2.2, 1.2, (sx * 11.0, sy * 11.0, 0.0), K['stone'], verts=8)
    for z in (14.0, 28.0, 42.0):
        for sg in (-1, 1):
            A.beam((-10.0 + 3.0 * z / 56.0 * 0.0, sg * (11.0 - 4.0 * z / 56.0), z), (10.0, sg * (11.0 - 4.0 * z / 56.0), z), 1.0, 1.0, K['timber'])
            A.beam((sg * (11.0 - 4.0 * z / 56.0), -10.0, z), (sg * (11.0 - 4.0 * z / 56.0), 10.0, z), 1.0, 1.0, K['timber'])
        A.beam((-9.5, -9.5, z - 14.0), (9.5, 9.5, z), 0.6, 0.6, K['iron'])
        A.beam((9.5, -9.5, z - 14.0), (-9.5, 9.5, z), 0.6, 0.6, K['iron'])
    A.cyl(13.0, 2.0, (0, 0, 56.0), K['timber'], verts=16)
    A.cyl(12.0, 22.0, (0, 0, 58.0), K['timber'], verts=20, r2=11.0)
    for k in range(5):
        A.sweep([(11.4 - k * 0.0, -0.3), (12.4, -0.3), (12.4, 0.3), (11.4, 0.3)], 0, 360, 20, K['iron'], loc=(0, 0, 60.0 + k * 4.5))
    A.cyl(13.5, 12.0, (0, 0, 80.0), K['cone'], verts=20, r2=0.0)
    A.cyl(0.4, 6.0, (0, 0, 91.5), K['iron'], verts=6)
    A.beam((12.0, 0, 62.0), (12.0, 0, 20.0), 1.4, 1.4, K['copper'])
    A.beam((12.0, 0, 20.0), (16.0, 0, 18.0), 1.0, 1.0, K['copper'])
    return _fin(A, 'skyline_tower_water')


# ------------------------------------------------------------------ CP15 order hall + annexes
def order_hq(var):
    reset()
    A = Acc()
    rnd = random.Random(130 + var)
    if var == 1:                                                                               # main hall with a crest, stair and a round tower
        _stone_block(A, rnd, 56.0, 34.0, 28.0, 0, 0, 0, 3, True, True)
        A.gable(36.0, 58.0, 18.0, (0, 0, 28.0), K['cone'], (0, 0, 90))
        round_tower(A, rnd, 9.0, 56.0, K, -32.0, 8.0, 0, top='cone', roof_k=1.5, verts=22, flag=True)
        _stone_block(A, rnd, 22.0, 22.0, 20.0, 34.0, -4.0, 0, 2, True, False)
        A.frustum((24.0, 24.0), (2.0, 2.0), 14.0, (34.0, -4.0, 20.0), K['cone'])
        for i in range(8):
            A.box((24.0 - i * 1.2, 2.0, 1.0), (0, -17.0 - i * 1.6, 8.0 - i), K['stone'], bev=0.1) if i < 7 else None
        A.cyl(5.4, 0.8, (0, -18.1, 22.0), K['trim'], verts=24, rot=(90, 0, 0))                  # crest: disc, star and open book
        A.prism(G.__dict__.get('_star', lambda a, b: [(0, 0), (1, 0), (0, 1)])(3.6, 1.5) if hasattr(G, '_star') else [(0, 3.6), (1.0, 1.0), (3.6, 0.8), (1.5, -0.6), (2.4, -3.2), (0, -1.6), (-2.4, -3.2), (-1.5, -0.6), (-3.6, 0.8), (-1.0, 1.0)],
                0.5, (0, -18.6, 22.6), K['gold'], (90, 0, 0))
    elif var == 2:                                                                             # barracks annex: long hall, dormers, square tower
        house(A, rnd, 44.0, 22.0, 2, K, hs=7.5, jetty=0.0, pitch=0.62, dormers=3)
        round_tower(A, rnd, 6.0, 40.0, K, 28.0, 4.0, 0, top='cone', roof_k=1.4, verts=16)
    else:                                                                                      # library annex: octagonal reading hall with a lantern roof
        A.cyl(20.0, 24.0, (0, 0, 0), K['stone'], verts=8, r2=19.0)
        for k in range(8):
            a = 22.5 + 45.0 * k
            x, y, _ = polar(19.6, a)
            A.box((0.6, 6.0, 12.0), (x, y, 10.0), K['glass'], (0, 0, a), bev=0)
            A.box((0.9, 7.0, 0.8), (x, y, 16.4), K['trim'], (0, 0, a), bev=0)
        A.cyl(21.0, 1.2, (0, 0, 24.0), K['trim'], verts=8)
        A.cyl(21.0, 18.0, (0, 0, 25.0), K['cone'], verts=8, r2=5.0)
        A.cyl(5.0, 9.0, (0, 0, 43.0), K['stone'], verts=8)
        A.cyl(6.0, 8.0, (0, 0, 52.0), K['cone'], verts=8, r2=0.0)
        A.box((14.0, 6.0, 10.0), (0, -22.0, 5.0), K['timber'], bev=0.1)
        round_tower(A, rnd, 5.0, 34.0, K, -26.0, 10.0, 0, top='cone', roof_k=1.4, verts=14)
    return _fin(A, 'order_hq')


def hq_1():
    return order_hq(1)


def hq_2():
    return order_hq(2)


def hq_3():
    return order_hq(3)


# ------------------------------------------------------------------ CP16 townhouses (half-timbered, one orange-red roof family)
def _town(kind, seed):
    reset()
    A = Acc()
    rnd = random.Random(seed)
    if kind == 'corner':
        house(A, rnd, 18.0, 13.0, 2, K, cx=0, cy=0, hs=6.2, jetty=0.9, pitch=0.7, sign=False, balcony=True)
        house(A, rnd, 12.0, 17.0, 2, K, cx=8.0, cy=12.0, hs=6.2, jetty=0.9, pitch=0.7, ridge_x=False, chimney=False, door=False)
    elif kind == 'tall':
        house(A, rnd, 14.0, 14.0, 3, K, hs=6.4, jetty=1.0, pitch=0.85, dormers=1, sign=False)
    elif kind == 'courtyard':
        house(A, rnd, 22.0, 10.0, 2, K, cx=0, cy=8.0, hs=6.2, jetty=0.8, pitch=0.7)
        house(A, rnd, 9.0, 18.0, 2, K, cx=-12.0, cy=-4.0, hs=6.2, jetty=0.8, pitch=0.7, ridge_x=False, chimney=False, door=False)
        house(A, rnd, 9.0, 18.0, 2, K, cx=12.0, cy=-4.0, hs=6.2, jetty=0.8, pitch=0.7, ridge_x=False, door=False)
        A.box((8.0, 6.0, 0.4), (0, -8.0, 0.2), K['stone'])
    elif kind == 'arcade':
        house(A, rnd, 22.0, 13.0, 2, K, hs=6.6, jetty=0.9, pitch=0.68, arcade=True, dormers=1, shutters=True, door=False)
    elif kind == 'inn':
        house(A, rnd, 22.0, 15.0, 2, K, hs=6.4, jetty=1.0, pitch=0.72, dormers=2, balcony=True, sign=True)
    elif kind == 'guild':
        house(A, rnd, 22.0, 16.0, 2, K, hs=7.4, jetty=1.0, pitch=0.62, dormers=2, belfry=(seed % 2 == 0))
    elif kind == 'market':
        A.box((22.0, 20.0, 1.0), (0, 0, 0.5), K['stone'])
        for sx in (-1, 1):
            for sy in range(4):
                A.box((1.0, 1.0, 9.0), (sx * 10.0, -8.4 + sy * 5.6, 5.5), K['timber'], bev=0.1)
                A.box((2.0, 2.0, 0.6), (sx * 10.0, -8.4 + sy * 5.6, 1.3), K['stone'])
        A.box((22.4, 21.0, 0.9), (0, 0, 10.2), K['timber'])
        A.gable(23.0, 24.0, 10.0, (0, 0, 10.6), K['roof'], (0, 0, 90))
        for k in range(5):
            A.box((3.0, 1.6, 1.0), (-8.0 + k * 4.0, -6.0, 1.6), K['sign'], bev=0.05)
            A.box((2.4, 1.2, 0.9), (-8.0 + k * 4.0, 4.0, 1.6), K['wall'], bev=0.05)
        A.box((2.2, 2.2, 2.6), (0, 0, 20.8), K['wall'])
        A.cyl(1.9, 2.5, (0, 0, 23.4), K['cone'], verts=6, r2=0.0)
    return _fin(A, 'townhouse_new')


TOWN_ROWS = ['corner', 'tall', 'tall', 'courtyard', 'courtyard', 'arcade', 'arcade', 'inn', 'guild', 'guild', 'market', 'corner']


def _mk_town(i):
    return lambda: _town(TOWN_ROWS[i], 200 + i)


# ------------------------------------------------------------------ CP17 plaza features, CP18 quay walls, CP19 bridges
def plaza_monument():
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
    A.revolve([(1.6, 0.0), (1.4, 2.4), (0.8, 4.4), (1.2, 5.6), (0.0, 7.4)], (0, 0, 26.0), K['gold'], segs=10)
    A.prism([(0, 3.0), (0.8, 0.9), (3.0, 0.9), (1.2, -0.5), (1.8, -2.6), (0, -1.3), (-1.8, -2.6), (-1.2, -0.5), (-3.0, 0.9), (-0.8, 0.9)], 0.5, (0, 0.25, 34.0), K['gold'], (90, 0, 0))
    for k in range(4):
        x, y, _ = polar(11.0, k * 90.0 + 45.0)
        A.box((2.0, 2.0, 1.8), (x, y, 0.9), K['stone'], (0, 0, k * 90.0 + 45.0), bev=0.1)
        A.cyl(0.9, 1.6, (x, y, 1.8), K['gold'], verts=8, r2=0.2)
    return _fin(A, 'plaza_monument')


def plaza_well():
    reset()
    A = Acc()
    A.cyl(8.0, 1.0, (0, 0, 0), K['stone'], verts=20)
    A.cyl(5.4, 5.0, (0, 0, 1.0), K['stone'], verts=16, r2=5.0)
    A.cyl(4.2, 0.4, (0, 0, 5.8), K['water'], verts=16)
    A.sweep([(4.6, 0.0), (5.9, 0.0), (5.9, 0.7), (4.6, 0.7)], 0, 360, 16, K['trim'], loc=(0, 0, 6.0))
    for sg in (-1, 1):
        A.box((0.8, 0.8, 11.0), (sg * 5.6, 0, 11.5), K['timber'], bev=0.1)
        A.beam((sg * 5.6, 0, 14.0), (sg * 2.4, 0, 17.4), 0.5, 0.5, K['timber'])
    A.cyl(0.4, 12.0, (0, 0, 17.0), K['timber'], verts=6, rot=(0, 90, 0))
    A.gable(14.0, 14.0, 5.0, (0, 0, 17.0), K['roof'], (0, 0, 90))
    A.cyl(0.9, 1.6, (0, 0, 10.0), K['timber'], verts=10)
    A.beam((0, 0, 16.6), (0, 0, 11.6), 0.1, 0.1, K['iron'])
    for k in range(6):
        x, y, _ = polar(7.2, k * 60.0)
        A.box((1.6, 1.0, 0.8), (x, y, 1.4), K['stone'], (0, 0, k * 60.0), bev=0.08)
    return _fin(A, 'plaza_well')


def _quay(kind):
    reset()
    A = Acc()
    rnd = random.Random(300 + len(kind))
    if kind == 'curve':
        R = 22.0
        for z in range(3):
            A.sweep([(R - 3.0, z * 2.8), (R + 1.0, z * 2.8), (R + 1.0, z * 2.8 + 2.9), (R - 3.0, z * 2.8 + 2.9)], 0, 80, 8, K['stone'] if z % 2 else K['wall'])
        A.sweep([(R - 3.4, 8.4), (R + 1.4, 8.4), (R + 1.4, 9.2), (R - 3.4, 9.2)], 0, 80, 8, K['trim'])
    else:
        for k in range(10):
            for z in range(3):
                A.chunk((3.2, 4.0, 2.9), (-13.5 + k * 3.0, 0, 1.45 + z * 2.8), K['stone'] if (k + z) % 2 else K['wall'], (0, 0, 0), 0.05, rnd)
        A.box((30.6, 4.8, 0.8), (0, 0, 8.8), K['trim'])
        if kind == 'steps':
            for i in range(7):
                A.box((8.0, 1.3, 1.2), (0, -2.8 - i * 1.0, 8.4 - 1.2 * (i + 1) + 0.6), K['stone'], bev=0.06)
        if kind == 'posts':
            for k in range(5):
                A.cyl(0.55, 3.2, (-12.0 + k * 6.0, -1.4, 9.2), K['timber'], verts=8)
                A.torus_stub = None
                A.ball(0.7, (-12.0 + k * 6.0, -1.4, 12.5), K['iron'], segs=6, rings=4)
        if kind == 'straight':
            for k in range(3):
                A.box((0.25, 0.25, 4.0), (-9.0 + k * 9.0, -2.5, 6.0), K['iron'], bev=0)
                A.box((1.2, 0.25, 0.25), (-9.0 + k * 9.0 + 0.5, -2.5, 4.2), K['iron'], bev=0)
            for k in range(4):
                A.cyl(0.35, 0.5, (-12.0 + k * 8.0, -2.55, 7.6), K['iron'], verts=8, rot=(90, 0, 0))
    return _fin(A, 'quay_wall')


def quay_1():
    return _quay('straight')


def quay_2():
    return _quay('curve')


def quay_3():
    return _quay('steps')


def quay_4():
    return _quay('posts')


def _bridge_stone():
    reset()
    A = Acc()
    rnd = random.Random(401)
    L, Wd = 60.0, 14.0
    A.box((L, Wd, 3.0), (0, 0, 14.0 - 0.0), K['stone'])
    for sg in (-1, 1):
        A.box((L, 1.0, 2.0), (0, sg * (Wd / 2.0 - 0.5), 16.0), K['trim'])
        for k in range(10):
            A.box((2.4, 1.2, 1.6), (-27.0 + k * 6.0, sg * (Wd / 2.0 - 0.5), 17.6), K['wall'], bev=0.06)
    for i, xc in enumerate((-18.0, 0.0, 18.0)):                                                # three round arches under the deck
        A.sweep([(7.0, -Wd / 2.0), (9.0, -Wd / 2.0), (9.0, Wd / 2.0), (7.0, Wd / 2.0)], 0, 180, 12, K['trim'], loc=(xc, 0, 6.0), rot=(90, 0, 0))
        A.box((8.0, Wd, 6.0 - 0.0), (xc + 9.0 * 1.0, 0, 3.0), K['stone']) if False else None
    for xp in (-27.0, -9.0, 9.0, 27.0):
        A.box((4.0, Wd + 2.0, 12.0), (xp, 0, 6.0), K['stone'])
        A.box((5.0, Wd + 3.0, 1.0), (xp, 0, 12.5), K['trim'])
    for sg in (-1, 1):                                                                         # gate towers with cone roofs at both ends
        round_tower(A, rnd, 5.0, 22.0, K, sg * 27.0, 0, 8.0, top='cone', slits=2, bands=1, roof_k=1.3, verts=16)
        A.box((8.0, Wd + 2.0, 1.0), (sg * 27.0, 0, 7.5), K['trim'])
    v4util.marker('mk_enda', (-30.0, 0, 15.6))
    v4util.marker('mk_endb', (30.0, 0, 15.6))
    v4util.marker('mk_deck', (0, 0, 15.6))
    return _fin(A, 'grand_bridge')


def _drawbridge():
    reset()
    A = Acc()
    rnd = random.Random(402)
    A.box((60.0, 14.0, 3.0), (0, 0, 14.0), K['timber']) if False else None
    for sg in (-1, 1):
        A.box((10.0, 18.0, 16.0), (sg * 25.0, 0, 8.0), K['stone'])
        A.box((11.0, 19.0, 1.0), (sg * 25.0, 0, 16.5), K['trim'])
    for k in range(40):                                                                        # lowered plank deck between the abutments
        A.box((1.1, 12.0, 0.6), (-19.5 + k * 1.0, 0, 15.2), K['timber'], bev=0)
    for sg in (-1, 1):
        A.beam((-20.0, sg * 6.0, 14.6), (20.0, sg * 6.0, 14.6), 0.8, 0.8, K['timber'])
        for k in range(9):
            A.box((0.4, 0.4, 2.6), (-18.0 + k * 4.5, sg * 6.0, 16.4), K['timber'], bev=0)
        A.beam((-20.0, sg * 6.0, 17.6), (20.0, sg * 6.0, 17.6), 0.4, 0.4, K['timber'])
        round_tower(A, rnd, 4.6, 20.0, K, sg * 25.0, -8.0, 16.6, top='cone', slits=2, bands=1, roof_k=1.3, verts=14)
        A.beam((sg * 21.0, 0, 30.0), (sg * 13.0, sg * 5.0, 15.6), 0.35, 0.35, K['iron'])
        A.beam((sg * 21.0, 0, 30.0), (sg * 13.0, -sg * 5.0, 15.6), 0.35, 0.35, K['iron'])
    A.box((14.0, 18.0, 14.0), (0, 0, 7.0), K['stone']) if False else None
    A.box((14.0, 20.0, 4.0), (0, 0, 24.0 + 0.0), K['stone']) if False else None
    A.box((44.0, 2.0, 18.0), (0, -9.0, 25.0), K['timber'], bev=0.1) if False else None
    A.box((6.0, 20.0, 5.0), (-20.5, 0, 28.0 + 0.0), K['wall']) if False else None
    for sg in (-1, 1):
        A.box((4.0, 18.0, 18.0), (sg * 21.0, 0, 25.0), K['stone'])
        A.box((5.0, 19.0, 1.0), (sg * 21.0, 0, 34.5), K['trim'])
    v4util.marker('mk_enda', (-30.0, 0, 15.5))
    v4util.marker('mk_endb', (30.0, 0, 15.5))
    v4util.marker('mk_deck', (0, 0, 15.5))
    return _fin(A, 'drawbridge')


BATCHES = {
    'walls_towers': ('v5_capital', mk([
        ('CP01_01_ring_wall_straight_01', wall_1), ('CP01_02_ring_wall_straight_02', wall_2), ('CP01_03_ring_wall_straight_03', wall_3),
        ('CP02_01_ring_wall_corner_01', corner_1), ('CP02_02_ring_wall_corner_02', corner_2), ('CP02_03_ring_wall_corner_03', corner_3),
        ('CP03_01_ring_wall_stair_end_01', stair_end_1), ('CP03_02_ring_wall_stair_end_02', stair_end_2),
        ('CP05_01_turret_crenellated_01', turret_1), ('CP05_02_turret_crenellated_02', turret_2),
        ('CP06_01_gate_flank_tower_01', flank_1), ('CP06_02_gate_flank_tower_02', flank_2)]) + [
        ('CP04_01_tower_round_cone_01', tower_1), ('CP04_02_tower_round_cone_02', tower_2), ('CP04_03_tower_round_cone_03', tower_3),
        ('CP04_04_tower_round_cone_04', tower_4)]),
    'gates_keep': ('v5_capital', mk([
        ('CP07_01_gatehouse_main', gatehouse), ('CP08_01_water_gate', water_gate), ('CP09_01_keep_terrace_hero', keep),
        ('CP10_01_keep_wing_01', wing_1), ('CP10_02_keep_wing_02', wing_2)])),
    'terrace_skyline': ('v5_capital', mk([
        ('CP12_01_terrace_retaining_wall_01', terrace_wall_s), ('CP12_02_terrace_retaining_wall_02', terrace_wall_c),
        ('CP13_01_grand_stair_01', stair_wide), ('CP13_02_grand_stair_02', stair_narrow),
        ('CP14_01_skyline_tower_01', sky_clock), ('CP14_02_skyline_tower_02', sky_bell), ('CP14_03_skyline_tower_03', sky_observatory),
        ('CP14_04_skyline_tower_04', sky_beacon), ('CP14_05_skyline_tower_05', sky_water),
        ('CP15_01_order_hq_01', hq_1), ('CP15_02_order_hq_02', hq_2), ('CP15_03_order_hq_03', hq_3),
        ('CP19_01_grand_bridge_01', _bridge_stone), ('CP19_02_grand_bridge_02', _drawbridge)], 0.12)),
    'town_extras': ('v5_capital', mk([
        ('CP11_01_great_hall_chapel_01', hall_1), ('CP11_02_great_hall_chapel_02', hall_2)] + [
        (f'CP16_{i + 1:02d}_townhouse_new_{i + 1:02d}', _mk_town(i)) for i in range(12)] + [
        ('CP17_01_plaza_features_01', plaza_monument), ('CP17_02_plaza_features_02', plaza_well),
        ('CP18_01_quay_wall_01', quay_1), ('CP18_02_quay_wall_02', quay_2), ('CP18_03_quay_wall_03', quay_3), ('CP18_04_quay_wall_04', quay_4)])),
}
