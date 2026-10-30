"""vi module - plains, ruins, coast extras, roads and sky: PL01-PL06 + VL01 farmland and church, LM19-LM21 crater, LM26-LM29 + LM31 ruins,
CO03-CO05 reefs/arches/islets, HB01 harbour towers, RD01-RD06 road life, BR01 viaduct, RV01 bank rocks, FL01-FL02 floating islands.
Original designs, no glow, ruined arches are allowed as ruins only. Front faces -Y. Sizes in briefs: (x, height, depth).
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v5kit
from v5kit import Acc, polar, tang, mk, ids
import v5gen as G
from v5gen import house, round_tower, wall_seg, column, cliff, spire, rock_arch, tree
import v4util

V = G.reg('vi', {
    'plaster': ((232, 222, 200), 'Concrete', 0.0, 0.9), 'wall': ((226, 214, 190), 'Concrete', 0.0, 0.9), 'timber': ((104, 78, 58), 'Wood', 0.0, 0.88),
    'roof': ((150, 84, 60), 'Brick', 0.0, 0.85), 'roof2': ((126, 66, 48), 'Brick', 0.0, 0.85), 'cap': ((110, 56, 42), 'Brick', 0.0, 0.85),
    'stone': ((148, 142, 134), 'Limestone', 0.0, 0.92), 'stone2': ((120, 116, 110), 'Slate', 0.0, 0.95), 'dark': ((38, 36, 40), 'Slate', 0.0, 0.95),
    'trim': ((220, 214, 204), 'Limestone', 0.0, 0.88), 'glass': ((86, 104, 128), 'SmoothPlastic', 0.0, 0.3), 'shutter': ((70, 100, 94), 'Wood', 0.0, 0.85),
    'door': ((92, 62, 46), 'Wood', 0.0, 0.85), 'iron': ((58, 58, 64), 'Metal', 0.6, 0.6), 'gold': ((196, 160, 84), 'Metal', 0.8, 0.35),
    'sign': ((184, 142, 72), 'WoodPlanks', 0.0, 0.85), 'flag': ((168, 52, 52), 'Fabric', 0.0, 1.0), 'deck': ((130, 98, 72), 'WoodPlanks', 0.0, 0.9),
    'hay': ((214, 182, 92), 'Grass', 0.0, 1.0), 'straw': ((190, 160, 84), 'Fabric', 0.0, 1.0), 'barn': ((150, 62, 54), 'Wood', 0.0, 0.88),
    'plank': ((150, 112, 76), 'WoodPlanks', 0.0, 0.9), 'canvas': ((226, 218, 196), 'Fabric', 0.0, 1.0), 'canvas2': ((176, 60, 52), 'Fabric', 0.0, 1.0),
    'canvas3': ((70, 96, 140), 'Fabric', 0.0, 1.0), 'water': ((84, 130, 160), 'SmoothPlastic', 0.0, 0.2), 'foam': ((236, 244, 248), 'SmoothPlastic', 0.0, 0.5),
    'moss': ((92, 124, 72), 'Grass', 0.0, 1.0), 'ivy': ((66, 102, 58), 'Grass', 0.0, 1.0), 'grass': ((100, 146, 72), 'Grass', 0.0, 1.0),
    'rock': ((128, 124, 120), 'Slate', 0.0, 0.95), 'rock2': ((150, 146, 140), 'Cobblestone', 0.0, 0.95), 'basalt': ((60, 60, 68), 'Basalt', 0.0, 0.9),
    'sand': ((214, 184, 140), 'Sandstone', 0.0, 0.95), 'char': ((46, 38, 34), 'Slate', 0.0, 0.95), 'ash': ((88, 82, 80), 'Slate', 0.0, 0.95),
    'cloth': ((196, 170, 120), 'Fabric', 0.0, 1.0), 'steel': ((150, 154, 160), 'Metal', 0.7, 0.45), 'coral': ((200, 120, 110), 'Sandstone', 0.0, 0.95),
    'white': ((240, 238, 232), 'Concrete', 0.0, 0.9), 'copper': ((92, 150, 128), 'Metal', 0.45, 0.55), 'cone': ((120, 54, 52), 'Slate', 0.0, 0.8),
    'dirt': ((118, 96, 70), 'Ground', 0.0, 1.0), 'rune': ((70, 84, 108), 'Slate', 0.0, 0.9), 'bark': ((96, 74, 56), 'Wood', 0.0, 0.95),
    'leaf': ((70, 120, 60), 'Grass', 0.0, 1.0), 'leaf2': ((104, 150, 80), 'Grass', 0.0, 1.0), 'rope': ((176, 150, 104), 'Fabric', 0.0, 1.0),
})
RK = {'stone': V['stone'], 'wall': V['wall'], 'trim': V['trim'], 'dark': V['dark'], 'door': V['door'], 'deck': V['deck'], 'roof': V['cone'], 'roof2': V['cap'],
      'gold': V['gold'], 'timber': V['timber'], 'flag': V['flag'], 'cap': V['trim'], 'glass': V['glass'], 'shutter': V['shutter'], 'iron': V['iron'], 'sign': V['sign']}
RUIN = dict(RK, wall=V['stone'], stone=V['stone2'], trim=V['moss'], cap=V['moss'])
ROCKS = [V['rock'], V['rock2'], V['stone2']]


def _fin(A, name):
    A.to_scene()
    return finalize(name, 28)


def _scatter(A, rnd, n, rx, ry, keys, size=(1.0, 3.0), z=0.5):
    for k in range(n):
        A.chunk((rnd.uniform(*size), rnd.uniform(*size), rnd.uniform(0.6, size[1] * 0.7)), (rnd.uniform(-rx, rx), rnd.uniform(-ry, ry), z), keys[k % len(keys)],
                (0, 0, rnd.uniform(0, 90)), 0.2, rnd)


def _L(fn, row):
    return [(m, (lambda j=j, f=fn: f(j))) for j, m in enumerate(ids(row))]


# ------------------------------------------------------------------ PL plains
def _farm(i):
    reset()
    A = Acc()
    rnd = random.Random(8000 + i)
    if i == 0:
        house(A, rnd, 16.0, 11.0, 2, RK, cx=-4.0, hs=5.4, jetty=0.4, pitch=0.8, dormers=1)
        A.box((10.0, 12.0, 8.0), (10.0, 4.0, 4.0), V['barn'], bev=0.2)
        A.gable(13.0, 12.0, 5.0, (10.0, 4.0, 8.0), V['roof2'], (0, 0, 90))
        A.box((4.0, 0.4, 5.4), (10.0, -2.1, 3.0), V['plank'], bev=0)
    elif i == 1:
        house(A, rnd, 22.0, 10.0, 1, RK, hs=6.0, jetty=0.0, pitch=0.9, chimney=True)
        A.box((7.0, 5.0, 4.0), (-12.0, 8.0, 2.0), V['plank'], bev=0.15)
        A.gable(8.0, 6.0, 2.4, (-12.0, 8.0, 4.0), V['roof2'], (0, 0, 90))
    elif i == 2:
        house(A, rnd, 14.0, 12.0, 2, RK, hs=5.6, jetty=0.6, pitch=0.75, balcony=True)
        for k in range(5):
            A.box((0.3, 0.3, 2.2), (-9.0 + k * 4.5, -9.0, 1.1), V['timber'], bev=0)
        A.box((20.0, 0.25, 0.25), (0, -9.0, 1.9), V['timber'], bev=0)
        A.box((20.0, 0.25, 0.25), (0, -9.0, 1.1), V['timber'], bev=0)
    else:
        house(A, rnd, 18.0, 14.0, 2, RK, hs=5.8, jetty=0.5, pitch=0.7, hip=True, dormers=2)
        house(A, rnd, 9.0, 8.0, 1, RK, cx=-13.0, cy=-1.0, hs=5.0, jetty=0.0, pitch=0.8, chimney=False, door=False)
        A.cyl(3.2, 12.0, (12.0, 2.0, 0), V['stone'], verts=12, r2=2.9)
        A.cyl(3.5, 3.0, (12.0, 2.0, 12.0), V['roof'], verts=12, r2=0.0)
    for k in range(4):                                                                           # fence and a hedge
        A.box((0.3, 0.3, 2.0), (-12.0 + k * 8.0, -11.0, 1.0), V['timber'], bev=0)
    A.box((26.0, 0.25, 0.25), (0, -11.0, 1.6), V['timber'], bev=0)
    for k in range(7):
        A.ball(rnd.uniform(1.0, 1.7), (rnd.uniform(-13, 13), rnd.uniform(9, 11), 1.0), V['ivy'], segs=7, rings=4, scale=(1.4, 1.0, 0.9))
    return _fin(A, 'farmhouse')


def _hay(i):
    reset()
    A = Acc()
    rnd = random.Random(8100 + i)
    if i == 0:
        for k in range(3):
            x = -3.6 + k * 3.6
            A.cyl(2.6, 6.0, (x, rnd.uniform(-1, 1), 0), V['hay'], verts=12, r2=2.4)
            A.cyl(2.7, 4.0, (x, 0, 6.0), V['straw'], verts=12, r2=0.0)
            A.sweep([(2.4, -0.1), (2.75, -0.1), (2.75, 0.1), (2.4, 0.1)], 0, 360, 12, V['timber'], loc=(x, 0, 2.5))
    elif i == 1:
        for r_ in range(3):
            for c in range(3 - r_):
                A.cyl(1.7, 3.0, (-3.5 + c * 3.4 + r_ * 1.7, 0, 1.7 + r_ * 3.0), V['hay'], verts=12, rot=(0, 90, 0))
        A.box((0.3, 0.3, 3.0), (5.5, 2.0, 1.5), V['timber'], bev=0)
        A.box((0.2, 0.3, 4.0), (6.0, 2.0, 2.0), V['iron'], bev=0)
    else:                                                                                        # grain silo
        A.cyl(4.6, 1.0, (0, 0, 0), V['stone'], verts=16)
        A.cyl(4.2, 18.0, (0, 0, 1.0), V['plaster'], verts=16, r2=4.0)
        for k in range(5):
            A.sweep([(4.0, -0.2), (4.6, -0.2), (4.6, 0.2), (4.0, 0.2)], 0, 360, 16, V['iron'], loc=(0, 0, 3.0 + k * 3.6))
        A.revolve([(4.2, 0.0), (3.8, 1.4), (2.6, 2.8), (1.2, 3.6), (0.0, 4.2)], (0, 0, 19.0), V['copper'], segs=16)
        A.box((1.6, 0.6, 3.2), (0, -4.3, 2.8), V['door'], bev=0.05)
        A.box((0.6, 0.6, 18.0), (4.6, 0, 9.0), V['iron'], bev=0.05)
    return _fin(A, 'hay_silo')


def _cart(i):
    reset()
    A = Acc()
    rnd = random.Random(8200 + i)
    A.box((9.0, 5.0, 0.5), (0, 0, 2.2), V['plank'], bev=0.04)
    for sg in (-1, 1):
        A.box((9.0, 0.3, 1.3), (0, sg * 2.4, 3.1), V['plank'], bev=0.03)
        A.cyl(2.0, 0.4, (0, sg * 2.9, 2.0), V['timber'], verts=14, rot=(90, 0, 0))
        A.cyl(0.4, 0.6, (0, sg * 2.9, 2.0), V['iron'], verts=8, rot=(90, 0, 0))
        for k in range(6):
            A.box((0.2, 0.3, 4.0), (0, sg * 2.9, 2.0), V['timber'], (k * 30.0, 0, 0), bev=0)
    A.box((0.3, 5.0, 1.3), (-4.4, 0, 3.1), V['plank'], bev=0.03)
    A.beam((4.4, 0, 2.2), (9.0, 0, 1.6), 0.3, 0.3, V['timber'])
    for k in range(5 if i == 0 else 3):
        A.cyl(0.8, 1.4, (-2.5 + k * 1.3, rnd.uniform(-1, 1), 2.5), V['hay'] if i == 0 else V['plank'], verts=8)
    return _fin(A, 'cart')


def watermill():
    reset()
    A = Acc()
    rnd = random.Random(8300)
    house(A, rnd, 17.0, 14.0, 2, RK, cx=-3.0, hs=6.0, jetty=0.5, pitch=0.75, door=True)
    A.box((6.0, 12.0, 14.0), (9.0, 0, 7.0), V['stone'], bev=0.2)
    A.box((1.0, 14.0, 1.0), (14.0, 0, 5.0), V['timber'], bev=0)
    A.cyl(8.0, 1.4, (14.0, -4.2, 8.0), V['timber'], verts=20, rot=(0, 90, 0)) if False else None
    for k in range(12):                                                                          # water wheel with paddles
        a = 30.0 * k
        x, y, z = polar(8.0, a, 0)
        A.box((1.0, 5.4, 1.6), (14.0 + z * 0.0, y * 0.0 - 0.0, 9.0 + math.sin(math.radians(a)) * 8.0) if False else (13.5, 0, 9.0), V['timber'], bev=0) if False else None
        px = 14.0 + 0.0
        A.box((0.9, 5.2, 1.8), (px, 0, 9.0 + math.cos(math.radians(a)) * 7.6), V['plank'], (0, a, 0), bev=0) if False else None
    for side in (-1, 1):
        A.sweep([(6.6, side * 2.2 - 0.3), (8.2, side * 2.2 - 0.3), (8.2, side * 2.2 + 0.3), (6.6, side * 2.2 + 0.3)], 0, 360, 20, V['timber'], loc=(14.0, 0, 9.0), rot=(0, 90, 0))
    for k in range(12):
        a = 30.0 * k
        A.box((0.5, 5.4, 1.9), (14.0 + math.sin(math.radians(a)) * 7.4, 0, 9.0 + math.cos(math.radians(a)) * 7.4), V['plank'], (0, -a, 0), bev=0)
        A.beam((14.0, 0, 9.0), (14.0 + math.sin(math.radians(a)) * 6.6, 0, 9.0 + math.cos(math.radians(a)) * 6.6), 0.35, 0.35, V['timber'])
    A.cyl(0.9, 6.4, (14.0, 0, 9.0), V['iron'], verts=8, rot=(90, 0, 0))
    A.box((10.0, 6.0, 0.5), (16.0, -10.0, 0.4), V['water'], bev=0)
    A.box((14.0, 3.0, 1.0), (7.0, -9.0, 1.2), V['plank'], (0, 0, 0), bev=0.05)
    for k in range(4):
        A.cyl(0.4, 1.4, (4.0 + k * 3.0, -10.6, 0.7), V['timber'], verts=6)
    for k in range(6):
        A.ball(rnd.uniform(0.7, 1.3), (16.0 + rnd.uniform(-4, 4), -10.0 + rnd.uniform(-2, 2), 0.9), V['foam'], segs=6, rings=4, scale=(1.4, 1.0, 0.5))
    return _fin(A, 'watermill')


def _stump_tower(i, ruin_level=1.0, height=40.0, r=6.0, seed=0, square=False):
    reset()
    A = Acc()
    rnd = random.Random(8400 + i + seed)
    if square:
        A.frustum((2 * r + 2.0, 2 * r + 2.0), (2 * r, 2 * r), 2.0, (0, 0, 0), V['stone2'])
        A.frustum((2 * r, 2 * r), (2 * r - 1.6, 2 * r - 1.6), height - 2.0, (0, 0, 2.0), V['wall'])
        for z in (0.3, 0.55, 0.8):
            G._window(A, 0, -r + 0.0, height * z, 270, RK, 1.4, 3.0, False, V['trim'])
        for k in range(8):
            a = rnd.uniform(0, 360)
            x, y, _ = polar(r * 0.9, a)
            A.chunk((rnd.uniform(2, 5), rnd.uniform(2, 5), rnd.uniform(1, 6) * ruin_level), (x, y, height + rnd.uniform(-1, 2)), V['wall'], (0, 0, a), 0.2, rnd)
    else:
        round_tower(A, rnd, r, height, RK, top='cone' if ruin_level == 0 else 'crenel', slits=3, bands=3, door=True, ruin=ruin_level > 0, roof_k=1.2)
    return _fin(A, 'watchtower')


def _watch(i):
    return _stump_tower(i, ruin_level=[1.0, 0.6, 0.0][i % 3], height=[34.0, 38.0, 40.0][i % 3], r=[5.4, 5.0, 6.0][i % 3], seed=i, square=(i == 1))


def _rock_bridge(i):
    reset()
    A = Acc()
    rnd = random.Random(8500 + i)
    G.rock_arch(A, rnd, 40.0 + i * 8.0, 26.0, 7.0, ROCKS, 0, 0, 0, 16.0, 13, V['moss'])
    A.mound(0, 0, 60.0, 24.0, 8.0, 14, ROCKS, rnd, 0.0, 0.4, 0.8)
    A.box((10.0, 18.0, 0.8), (0, 0, 28.0 if False else 24.5), V['dirt'], bev=0) if False else None
    for k in range(9):
        A.box((rnd.uniform(3, 6), rnd.uniform(5, 9), 0.6), (-16.0 + k * 4.0, 0, 26.0 + rnd.uniform(-0.3, 0.3)), V['dirt'], (0, 0, rnd.uniform(-8, 8)), bev=0)
    for k in range(10):
        A.ball(rnd.uniform(1.4, 2.6), (rnd.uniform(-22, 22), rnd.uniform(-8, 8), rnd.uniform(24.5, 27)), V['grass'], segs=7, rings=4, scale=(1.4, 1.2, 0.6))
    A.box((60.0, 5.0, 0.4), (0, -8.0, 0.2), V['water'], bev=0)
    v4util.marker('mk_enda', (-20.0, 0, 26.0))
    v4util.marker('mk_endb', (20.0, 0, 26.0))
    return _fin(A, 'rock_bridge')


def spired_church():
    reset()
    A = Acc()
    rnd = random.Random(8600)
    A.box((26.0, 18.0, 1.0), (0, 0, 0.5), V['stone'], bev=0.2)
    A.frustum((18.0, 10.0), (17.0, 9.0), 12.0, (0, 6.0, 1.0), V['wall'])
    A.gable(11.0, 20.0, 8.0, (0, 6.0, 13.0), V['cone'], (0, 0, 90))
    A.cyl(5.4, 11.0, (0, 12.0, 1.0), V['wall'], verts=10, r2=5.2)
    A.cyl(5.8, 6.0, (0, 12.0, 12.0), V['cone'], verts=10, r2=0.0)
    A.frustum((8.0, 8.0), (7.0, 7.0), 24.0, (0, -4.0, 1.0), V['wall'])                           # west tower
    A.frustum((8.4, 8.4), (7.4, 7.4), 2.0, (0, -4.0, 25.0), V['trim'])
    for sg in (-1, 1):
        A.box((1.4, 0.6, 5.0), (sg * 2.0, -8.2, 18.0), V['dark'], bev=0)
    A.frustum((8.0, 8.0), (0.6, 0.6), 38.0, (0, -4.0, 27.0), V['cone'])                         # spire
    for k in range(4):
        x, y, _ = polar(3.2, k * 90.0 + 45.0)
        A.frustum((2.0, 2.0), (0.4, 0.4), 6.0, (x, -4.0 + y, 25.0), V['cone'])
    A.cyl(0.25, 5.0, (0, -4.0, 65.0), V['gold'], verts=6)
    A.box((0.3, 0.3, 3.0), (0, -4.0, 69.0), V['gold'], bev=0)
    A.box((1.8, 0.3, 0.3), (0, -4.0, 70.0), V['gold'], bev=0)
    A.box((3.2, 0.5, 4.8), (0, -8.3, 3.4), V['door'], bev=0.05)
    A.box((4.4, 1.4, 0.7), (0, -8.3, 6.2), V['trim'], bev=0.08)
    for sg in (-1, 1):
        for z in (6.0, 9.0):
            for k in range(3):
                G._window(A, sg * 9.1, 1.0 + k * 5.0, z, 0 if sg > 0 else 180, RK, 1.4, 3.0, False, V['trim'])
        for k in range(3):
            A.box((1.4, 1.4, 11.0), (sg * 9.4, 1.0 + k * 5.0, 6.5), V['stone'], bev=0.1)
    A.cyl(0.9, 1.0, (0, -8.0, 22.0), V['trim'], verts=14, rot=(90, 0, 0))                       # clock disc on the tower
    for k in range(4):
        A.box((0.4, 0.4, 2.0), (6.0, 14.0, 1.4), V['timber'], bev=0) if False else None
    return _fin(A, 'spired_church')


# ------------------------------------------------------------------ crater + ruins
def _rim_rock(i):
    reset()
    A = Acc()
    rnd = random.Random(8700 + i)
    A.mound(0, 0, 60.0, 40.0, 40.0 + i * 3, 36, ROCKS + [V['basalt']], rnd, 0.0, 0.3, 0.7, 0.14)
    G.spire(A, rnd, 7.0, 46.0, ROCKS + [V['basalt']], rnd.uniform(-10, 10), rnd.uniform(-6, 6), 6.0, 8, rnd.uniform(-0.1, 0.1))
    _scatter(A, rnd, 14, 28.0, 18.0, ROCKS, (1.4, 4.0), 1.0)
    return _fin(A, 'rim_rock')


def _magic_ruin(i):
    reset()
    A = Acc()
    rnd = random.Random(8800 + i)
    A.cyl(18.0, 1.4, (0, 0, 0), V['stone2'], verts=24, r2=17.0)
    if i == 0:                                                                                   # broken ring of runestones
        for k in range(8):
            a = 45.0 * k
            x, y, _ = polar(14.0, a)
            h = rnd.uniform(8, 22) if k % 3 else rnd.uniform(3, 6)
            A.chunk((3.6, 2.6, h), (x, y, 1.4 + h / 2), V['stone'], (0, 0, a + 90.0), 0.1, rnd, (0.8, 0.8))
            A.box((3.8, 0.4, 1.4), (x, y, 5.0), V['rune'], (0, 0, a + 90.0), bev=0)
    elif i == 1:                                                                                 # fallen portal frame (post and lintel)
        for sx in (-1, 1):
            A.chunk((4.0, 4.0, 22.0), (sx * 9.0, 0, 12.0), V['stone'], (0, 0, 0), 0.06, rnd, (0.9, 0.9))
            A.box((4.4, 4.4, 1.0), (sx * 9.0, 0, 1.9), V['rune'], bev=0.05)
        A.chunk((26.0, 4.4, 4.0), (6.0, -8.0, 3.4), V['stone'], (0, 0, 14), 0.08, rnd)
        for k in range(8):
            A.chunk((rnd.uniform(2, 4), rnd.uniform(2, 4), rnd.uniform(1, 3)), (rnd.uniform(-12, 12), rnd.uniform(-10, 4), 2.0), V['stone2'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    else:                                                                                        # shattered obelisk and broken dais
        A.chunk((10.0, 10.0, 3.0), (0, 0, 2.9), V['stone'], jit=0.06, rnd=rnd)
        A.frustum((5.0, 5.0), (3.4, 3.4), 18.0, (0, 0, 4.4), V['stone'])
        for k in range(7):
            A.chunk((rnd.uniform(1.6, 3.4), rnd.uniform(1.6, 3.4), rnd.uniform(1.4, 4)), (rnd.uniform(-9, 9), rnd.uniform(-9, 9), 2.2), V['stone'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
        for r_ in range(4):
            A.box((3.6, 0.4, 0.6), (0, -1.8, 8.0 + r_ * 3.6), V['rune'], bev=0)
    _scatter(A, rnd, 8, 16.0, 16.0, [V['stone2'], V['moss']], (1.0, 2.6), 1.4)
    return _fin(A, 'magic_ruin')


def _drift_slab(i):
    reset()
    A = Acc()
    rnd = random.Random(8900 + i)
    A.chunk((34.0, 28.0, 5.0), (0, 0, 14.0), V['stone2'], (rnd.uniform(-4, 4), rnd.uniform(-4, 4), rnd.uniform(0, 60)), 0.07, rnd, (0.95, 0.95))
    A.chunk((30.0, 24.0, 3.0), (0, 0, 17.3), V['grass'], (0, 0, 0), 0.06, rnd)
    for k in range(7):
        A.chunk((rnd.uniform(5, 10), rnd.uniform(5, 10), rnd.uniform(5, 11)), (rnd.uniform(-9, 9), rnd.uniform(-8, 8), 8.0 - k * 0.8), ROCKS[k % 3], (0, 0, rnd.uniform(0, 90)), 0.16, rnd, (0.55, 0.55))
    A.chunk((9.0, 9.0, 8.0), (rnd.uniform(-4, 4), rnd.uniform(-4, 4), 3.0), V['basalt'], (0, 0, 20), 0.2, rnd, (0.2, 0.2))
    for k in range(5):
        A.ball(rnd.uniform(1.4, 2.6), (rnd.uniform(-12, 12), rnd.uniform(-10, 10), 19.5), V['ivy'], segs=7, rings=4, scale=(1.3, 1.1, 0.8))
    return _fin(A, 'drifting_slab')


def _arena(i):
    reset()
    A = Acc()
    rnd = random.Random(9000 + i)
    R = 40.0
    A.sweep([(R - 5.0, 0.0), (R + 5.0, 0.0), (R + 4.0, 26.0), (R - 4.0, 26.0)], -20, 20, 8, V['stone'], loc=(0, -R, 0))
    for k in range(5):                                                                           # tiers of arcade openings (ruined: allowed)
        a = -16.0 + k * 8.0
        x, y, _ = polar(R + 4.2, a + 90.0)
        for z in (5.0, 15.0):
            A.box((4.6, 0.8, 7.0), (math.cos(math.radians(a + 90)) * (R + 4.0), -R + math.sin(math.radians(a + 90)) * (R + 4.0), z + 3.5), V['dark'], (0, 0, a), bev=0) if False else None
    for k in range(5):
        a = -16.0 + k * 8.0
        px, py = math.sin(math.radians(a)) * (R + 4.1), -R + math.cos(math.radians(a)) * (R + 4.1)
        for z in (3.5, 13.5):
            A.box((4.4, 1.4, 6.0), (px, py, z + 3.0), V['dark'], (0, 0, -a), bev=0)
            A.box((5.2, 1.7, 0.8), (px, py, z + 6.4), V['trim'], (0, 0, -a), bev=0.1)
        A.box((1.6, 2.6, 25.0), (math.sin(math.radians(a + 4.0)) * (R + 4.6), -R + math.cos(math.radians(a + 4.0)) * (R + 4.6), 12.5), V['stone'], (0, 0, -a - 4.0), bev=0.1)
    for k in range(4 + i):
        a = rnd.uniform(-20, 20)
        A.chunk((rnd.uniform(5, 9), rnd.uniform(4, 8), rnd.uniform(1.0, 5.0 + i)), (math.sin(math.radians(a)) * (R + rnd.uniform(-2, 3)), -R + math.cos(math.radians(a)) * (R + rnd.uniform(-2, 3)), 26.0 + rnd.uniform(-1, 2)), V['stone'], (0, 0, -a), 0.22, rnd)
    _scatter(A, rnd, 12, 28.0, 14.0, [V['stone2'], V['moss']], (1.2, 3.4), 0.7)
    return _fin(A, 'arena_wall')


def _aqueduct(i):
    reset()
    A = Acc()
    rnd = random.Random(9100 + i)
    for k, x in enumerate((-14.0, 0.0, 14.0)):
        A.box((5.0, 8.0, 36.0), (x - 5.0 if False else x - 7.0, 0, 18.0), V['stone'], bev=0.25) if False else None
    for xp in (-18.0, -2.0, 14.0):
        A.box((5.0, 9.0, 38.0 - i * 6.0 * (xp > 0)), (xp, 0, (38.0 - i * 6.0 * (xp > 0)) / 2.0), V['stone'], bev=0.25)
    for xc in (-10.0, 6.0):
        A.sweep([(5.0, -4.5), (7.4, -4.5), (7.4, 4.5), (5.0, 4.5)], 0, 180, 10, V['trim'], loc=(xc, 0, 26.0), rot=(90, 0, 0))
        A.box((6.0, 9.0, 7.0), (xc, 0, 33.0 - 2.0), V['stone'], bev=0.2) if False else None
    A.box((46.0, 9.0, 4.0), (-2.0, 0, 38.0 - 4.0), V['stone'], bev=0.2) if i == 0 else A.box((30.0, 9.0, 4.0), (-8.0, 0, 34.0), V['stone'], bev=0.2)
    A.box((46.0, 6.0, 1.0), (-2.0, 0, 38.5 - 4.0 + 2.5), V['water'], bev=0) if i == 0 else None
    for k in range(5):
        A.chunk((rnd.uniform(2, 5), rnd.uniform(2, 5), rnd.uniform(1, 3)), (rnd.uniform(-22, 22), rnd.uniform(-6, 6), 1.0), V['stone2'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(6):
        A.ball(rnd.uniform(1.4, 2.4), (rnd.uniform(-22, 20), rnd.uniform(-5, 5), rnd.uniform(4, 36)), V['ivy'], segs=7, rings=4, scale=(1.3, 1.1, 0.8))
    return _fin(A, 'aqueduct_arches')


def _columns(i):
    reset()
    A = Acc()
    rnd = random.Random(9200 + i)
    A.cyl(12.0, 1.0, (0, 0, 0), V['stone2'], verts=14, r2=11.0)
    for k in range(3 + i % 2):
        a = k * 360.0 / (3 + i % 2) + rnd.uniform(-20, 20)
        x, y, _ = polar(6.0, a)
        column(A, x, y, 1.0, 1.8, rnd.uniform(14.0, 36.0), RUIN, rnd.uniform(0.2, 0.9), rnd)
    _scatter(A, rnd, 8, 10.0, 10.0, [V['stone2'], V['moss']], (1.0, 2.6), 1.2)
    return _fin(A, 'broken_columns')


def _stump(i):
    return _stump_tower(10 + i, 1.0, 30.0 + i * 5.0, 6.5 + i, i, i == 1)


def _wall_module(i):
    reset()
    A = Acc()
    rnd = random.Random(9300 + i)
    if i == 0:
        wall_seg(A, rnd, 40.0, 16.0, 7.0, RUIN, 0, 0, 0, 5.0, True, False, True)
        for k in range(8):
            A.chunk((rnd.uniform(3, 6), 4.0, rnd.uniform(1, 5)), (-18.0 + k * 5.0, 0, 20.0), V['stone'], (0, 0, rnd.uniform(-10, 10)), 0.2, rnd)
    elif i == 1:
        round_tower(A, rnd, 9.0, 30.0, RUIN, 0, 0, 0, ruin=True, slits=3, bands=3)
        wall_seg(A, rnd, 14.0, 12.0, 6.0, RUIN, 16.0, 0, 0, 4.0, False, False, True)
    else:
        for k in range(2):
            A.frustum((14.0, 14.0), (12.0, 12.0), 24.0 - k * 6.0, (-12.0 + k * 22.0, 0, 0), V['stone'])
            for j in range(6):
                A.chunk((rnd.uniform(2, 5), rnd.uniform(2, 5), rnd.uniform(1, 4)), (-12.0 + k * 22.0 + rnd.uniform(-5, 5), rnd.uniform(-5, 5), 24.0 - k * 6.0), V['stone'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
        wall_seg(A, rnd, 14.0, 10.0, 6.0, RUIN, 0, 0, 0, 4.0, False, False, True)
    for k in range(8):
        A.ball(rnd.uniform(1.2, 2.4), (rnd.uniform(-18, 18), rnd.uniform(-5, 5), rnd.uniform(2, 18)), V['ivy'], segs=7, rings=4, scale=(1.3, 1.1, 0.8))
    return _fin(A, 'ruin_module')


# ------------------------------------------------------------------ coast
def _reef(i):
    reset()
    A = Acc()
    rnd = random.Random(9400 + i)
    keys = [V['basalt'], V['rock'], V['rock2']]
    A.mound(0, 0, 30.0, 30.0, 6.0, 14, keys, rnd, 0.0, 0.35, 0.8)
    for k in range(10):
        x, y, _ = polar(rnd.uniform(3, 13), rnd.uniform(0, 360))
        A.ball(rnd.uniform(0.9, 1.6), (x, y, 1.0 + rnd.uniform(0, 2.5)), V['foam'], segs=6, rings=4, scale=(1.4, 1.1, 0.5)) if i % 2 == 0 else A.cyl(0.5, rnd.uniform(1.0, 2.4), (x, y, 1.0), V['coral'], verts=6, r2=0.3)
    return _fin(A, 'reef')


def _sea_arch(i):
    reset()
    A = Acc()
    rnd = random.Random(9500 + i)
    G.rock_arch(A, rnd, 40.0 + i * 8.0, 44.0, 9.0, ROCKS + [V['basalt']], 0, 0, 0, 16.0, 15, V['moss'])
    A.mound(0, 0, 70.0, 28.0, 10.0, 16, ROCKS, rnd, 0.0, 0.4, 0.8)
    return _fin(A, 'sea_arch')


def _islet(i):
    reset()
    A = Acc()
    rnd = random.Random(9600 + i)
    A.mound(0, 0, 58.0, 58.0, 16.0, 30, ROCKS + [V['sand']], rnd, 0.0, 0.3, 0.7)
    A.chunk((40.0, 40.0, 3.0), (0, 0, 16.0), V['grass'], jit=0.05, rnd=rnd)
    round_tower(A, rnd, 6.0, 26.0 - i * 4, RUIN, rnd.uniform(-8, 8), rnd.uniform(-8, 8), 16.5, ruin=True, slits=2, bands=2)
    for k in range(4):
        column(A, rnd.uniform(-16, 16), rnd.uniform(-16, 16), 16.5, 1.2, rnd.uniform(6, 14), RUIN, 0.4, rnd)
    for k in range(3):
        G.tree(A, rnd, rnd.uniform(12, 20), rnd.uniform(4, 6), {'bark': V['bark'], 'leaf': V['leaf'], 'leaf2': V['leaf2'], 'bloom': V['leaf2']}, 'oak', rnd.uniform(-16, 16), rnd.uniform(-16, 16), 16.5)
    return _fin(A, 'ruin_islet')


def _harbour_tower(i):
    reset()
    A = Acc()
    rnd = random.Random(9700 + i)
    K = dict(RK, wall=V['white'], stone=V['stone'], roof=V['roof'], roof2=V['cap'], trim=V['trim'])
    if i == 0:
        round_tower(A, rnd, 8.0, 34.0, K, top='cone', slits=2, bands=2, door=True, verts=20, roof_k=1.1, flag=True)
    elif i == 1:                                                                                 # lighthouse-like tower with a gallery (unlit lantern room)
        A.frustum((13.0, 13.0), (9.0, 9.0), 30.0, (0, 0, 0), V['white'])
        for k in range(3):
            A.box((9.6, 9.6, 3.0), (0, 0, 8.0 + k * 9.0), V['cone'], bev=0.1)
        A.box((13.0, 13.0, 1.0), (0, 0, 30.0), V['trim'])
        for sx in (-1, 1):
            for sy in (-1, 1):
                A.box((0.5, 0.5, 4.0), (sx * 6.0, sy * 6.0, 32.5), V['iron'], bev=0)
        A.cyl(4.4, 7.0, (0, 0, 31.0), V['glass'], verts=10, r2=3.8)
        A.cyl(5.4, 5.0, (0, 0, 38.0), V['cone'], verts=10, r2=0.0)
    else:                                                                                        # square watch tower with a hoarding
        A.frustum((12.0, 12.0), (10.0, 10.0), 28.0, (0, 0, 0), V['stone'])
        for z in (8.0, 16.0):
            G._window(A, 0, -5.9, z, 270, K, 1.6, 3.0, False, V['trim'])
        A.box((15.0, 15.0, 1.2), (0, 0, 28.0), V['timber'])
        A.box((13.0, 13.0, 5.0), (0, 0, 31.0), V['wall'] if False else V['white'])
        A.gable(14.0, 15.0, 6.0, (0, 0, 33.6), V['roof'], (0, 0, 90))
        for k in range(5):
            A.box((0.3, 0.3, 3.0), (-6.0 + k * 3.0, -7.0, 29.8), V['timber'], bev=0)
    return _fin(A, 'harbour_tower')


# ------------------------------------------------------------------ roads
def _road_tower(i):
    return _stump_tower(20 + i, 0.0 if i < 2 else 1.0, 46.0, 5.5 + (i % 2), i, i % 2 == 1)


def _camp(i):
    reset()
    A = Acc()
    rnd = random.Random(9800 + i)
    cols = [V['canvas'], V['canvas2'], V['canvas3']]
    if i < 3:                                                                                    # tents
        A.gable(10.0 + i, 12.0, 6.0 + i * 0.5, (0, 0, 0), cols[i], (0, 0, 90))
        A.box((3.0, 0.2, 4.4), (0, -6.1, 2.2), V['dark'], bev=0)
        for sg in (-1, 1):
            A.beam((sg * 7.0, -7.0, 0.0), (sg * 4.0, -5.5, 3.0), 0.12, 0.12, V['rope'])
            A.cyl(0.2, 1.6, (sg * 7.0, -7.0, 0.0), V['timber'], verts=5)
        A.cyl(0.18, 9.0 + i, (0, 6.0, 0), V['timber'], verts=6)
        A.box((3.4, 1.2, 0.3), (-3.0, -8.0, 0.2), V['plank'], bev=0)
    elif i == 3:                                                                                 # cooking rack
        for sg in (-1, 1):
            A.beam((sg * 5.0, 0, 0.0), (sg * 4.4, 0, 6.0), 0.36, 0.36, V['timber'])
        A.beam((-5.0, 0, 5.6), (5.0, 0, 5.6), 0.28, 0.28, V['iron'])
        A.cyl(1.5, 1.8, (0, 0, 2.6), V['iron'], verts=12, r2=1.8)
        A.beam((0, 0, 5.6), (0, 0, 4.4), 0.1, 0.1, V['iron'])
        for k in range(8):
            x, y, _ = polar(2.6, k * 45.0)
            A.chunk((1.0, 1.0, 0.8), (x, y, 0.4), V['rock'], jit=0.2, rnd=rnd)
        A.box((2.6, 1.6, 0.5), (4.5, -3.0, 0.4), V['plank'], bev=0.04)
    elif i == 4:                                                                                 # supply stack
        for (x, y, z, s) in ((-2.0, 0, 0, 2.6), (1.0, 0.4, 0, 2.4), (-0.6, 0.2, 2.6, 2.2), (3.2, -1.0, 0, 1.8)):
            A.box((s, s, s), (x, y, z + s / 2), V['plank'], (0, 0, rnd.uniform(-10, 10)), bev=0.08)
        for k in range(3):
            A.cyl(0.9, 1.6, (-4.0 + k * 1.1, 2.5, 0), V['timber'], verts=10)
        A.ball(1.2, (4.0, 2.0, 1.2), V['canvas'], segs=8, rings=5)
        A.cyl(0.9, 3.2, (0, -2.5, 0.9), V['canvas'], verts=10, rot=(0, 90, 0))
    else:                                                                                        # bedroll
        A.cyl(1.0, 7.0, (-3.5, 0, 0.9), V['canvas3'], verts=10, rot=(0, 90, 0))
        A.box((7.0, 2.4, 0.3), (0, 0, 0.2), V['canvas'], bev=0)
        A.ball(1.0, (3.8, 0, 0.9), V['canvas'], segs=8, rings=5, scale=(1.3, 1.0, 0.7))
        A.cyl(0.7, 1.2, (-5.0, 3.0, 0), V['timber'], verts=8)
        A.box((4.0, 2.0, 0.15), (0, 0, 0.1), V['moss'], bev=0)
    return _fin(A, 'camp_piece')


def _waystation(i):
    reset()
    A = Acc()
    rnd = random.Random(9900 + i)
    if i == 0:
        house(A, rnd, 18.0, 12.0, 1, RK, hs=6.4, jetty=0.0, pitch=0.8, sign=True)
        A.box((10.0, 5.0, 0.4), (0, -8.5, 6.0), V['canvas'], (-10, 0, 0), bev=0)
        for sx in (-4.5, 4.5):
            A.cyl(0.25, 6.0, (sx, -10.0, 0), V['timber'], verts=6)
        A.box((4.0, 1.6, 1.6), (9.0, -4.0, 0.8), V['plank'], bev=0.08)
    else:
        house(A, rnd, 20.0, 12.0, 2, RK, hs=5.6, jetty=0.7, pitch=0.7, balcony=True, sign=True)
        for k in range(4):
            A.box((2.4, 1.6, 1.6), (-8.0 + k * 2.8, -10.5, 0.8), V['plank'], bev=0.08)
            A.cyl(0.8, 1.4, (-8.0 + k * 2.8 + 0.0, -12.0, 0.7), V['timber'], verts=8)
        A.beam((-9.0, -9.0, 8.0), (-9.0, -12.0, 8.0), 0.2, 0.2, V['iron'])
    return _fin(A, 'waystation')


def _trading(i):
    reset()
    A = Acc()
    rnd = random.Random(10000 + i)
    house(A, rnd, 18.0, 11.0, 2, RK, hs=5.8, jetty=0.6, pitch=0.72, sign=True, arcade=(i == 1), door=(i == 0))
    for k in range(3):
        A.box((3.4, 1.8, 1.4), (-9.0 + k * 4.4, -9.0, 0.7), V['plank'], bev=0.08)
        A.box((3.8, 2.2, 0.2), (-9.0 + k * 4.4, -9.0, 4.2), (V['canvas'], V['canvas2'], V['canvas3'])[(k + i) % 3], bev=0)
        for sx in (-1.6, 1.6):
            A.cyl(0.12, 4.0, (-9.0 + k * 4.4 + sx, -9.0, 0), V['timber'], verts=5)
    for k in range(4):
        A.cyl(0.8, 1.5, (6.0 + k * 1.1, -8.5, 0), V['timber'], verts=8)
    A.box((3.0, 2.0, 2.0), (-12.0, -3.0, 1.0), V['plank'], bev=0.08)
    return _fin(A, 'trading_post')


def _military(i):
    reset()
    A = Acc()
    rnd = random.Random(10100 + i)
    if i == 0:                                                                                   # broken ballista
        A.box((6.0, 3.0, 0.7), (0, 0, 1.6), V['timber'], bev=0.05)
        for sx in (-2.4, 2.4):
            A.cyl(1.4, 0.4, (sx, 0, 1.4), V['timber'], verts=12, rot=(0, 90, 0))
        A.beam((-3.0, 0, 2.2), (4.0, 0, 3.6), 0.5, 0.5, V['timber'])
        A.beam((-1.6, -3.6, 3.6), (-0.4, 0, 3.0), 0.3, 0.3, V['timber'])
        A.beam((-1.6, 3.6, 3.6), (-0.4, 0, 3.0), 0.3, 0.3, V['timber'], up=(0, 1, 0))
        A.beam((-1.6, -3.6, 3.6), (-1.6, 1.0, 3.6), 0.08, 0.08, V['rope'])
        A.chunk((3.0, 0.6, 0.6), (3.0, 1.6, 0.5), V['timber'], (0, 0, 30), 0.2, rnd)
    elif i == 1:                                                                                 # wrecked cart
        A.box((7.0, 4.0, 0.4), (0, 0, 1.8), V['plank'], (0, 6, 4), bev=0.04)
        A.cyl(1.9, 0.3, (-2.0, 2.4, 1.9), V['timber'], verts=12, rot=(90, 0, 0))
        A.cyl(1.9, 0.3, (3.6, -3.4, 0.4), V['timber'], verts=12, rot=(10, 0, 0))
        for k in range(5):
            A.chunk((1.4, 0.5, 0.4), (rnd.uniform(-3, 3), rnd.uniform(-3, 3), 0.3), V['plank'], (0, 0, rnd.uniform(0, 180)), 0.2, rnd)
    elif i == 2:                                                                                 # banner
        A.cyl(0.3, 10.0, (0, 0, 0), V['timber'], verts=6)
        A.cyl(0.18, 4.8, (1.8, 0, 8.6), V['timber'], verts=6, rot=(0, 90, 0))
        A.box((0.1, 3.8, 6.0), (2.0, 0, 5.4), V['flag'], (0, 0, 0), bev=0)
        A.ball(0.45, (0, 0, 10.2), V['gold'], segs=6, rings=4)
        A.chunk((2.4, 2.4, 0.6), (0, 0, 0.3), V['rock'], jit=0.1, rnd=rnd)
    elif i == 3:                                                                                 # spear rack
        A.box((7.0, 1.0, 0.4), (0, 0, 0.2), V['timber'], bev=0)
        for sx in (-3.0, 3.0):
            A.cyl(0.18, 4.4, (sx, 0, 0), V['timber'], verts=6)
        A.box((6.4, 0.3, 0.3), (0, 0, 3.6), V['timber'], bev=0)
        for k in range(6):
            A.cyl(0.08, 6.0, (-2.5 + k * 1.0, 0, 0), V['timber'], verts=5, rot=(0, rnd.uniform(-4, 4), 0))
            A.frustum((0.5, 0.2), (0.1, 0.1), 1.0, (-2.5 + k * 1.0, 0, 6.0), V['steel'])
    else:                                                                                        # shield pile
        for k in range(7):
            x, y, _ = polar(rnd.uniform(0, 2.4), rnd.uniform(0, 360))
            A.cyl(1.7, 0.3, (x, y, 0.3 + k * 0.28), (V['canvas2'], V['canvas3'], V['timber'])[k % 3], verts=12, rot=(rnd.uniform(-8, 8), rnd.uniform(-8, 8), 0))
            A.ball(0.4, (x, y, 0.5 + k * 0.28), V['steel'], segs=6, rings=4, scale=(1, 1, 0.5))
        A.beam((-3.0, 1.0, 0.3), (1.0, 2.0, 2.2), 0.2, 0.2, V['timber'])
    return _fin(A, 'military_prop')


def _burnt_house(i):
    reset()
    A = Acc()
    rnd = random.Random(10200 + i)
    A.box((22.0, 20.0, 0.8), (0, 0, 0.4), V['ash'], bev=0.1)
    if i % 2 == 1:                                                                               # standing shell with a fallen roof
        BK = dict(RK, wall=V['char'] if i == 1 else V['stone2'], roof=V['char'], timber=V['char'], roof2=V['ash'], cap=V['ash'], shutter=V['char'], door=V['char'])
        house(A, rnd, 14.0, 11.0, 1 + (i == 3), BK, cx=-2.0, hs=5.4, jetty=0.0, pitch=0.7, shutters=False)
        A.gable(12.0, 11.0, 3.8, (5.0, 4.0, 0.8), V['char'], (22, -10, 24))
        for k in range(6):
            A.beam((-4.0 + k * 2.4, 6.0, 5.0), (-4.0 + k * 2.4 + rnd.uniform(-2, 2), 9.0, 0.9 + rnd.uniform(0, 2)), 0.45, 0.45, V['char'])
    else:
        w, d = 14.0, 11.0
        for (x, y, ww, dd, h) in ((0, 0, w, 0.9, 8.0), (-w / 2, d / 2, 0.9, d, 6.0), (w / 2, d / 2, 0.9, d, 3.5), (0, d, w * 0.6, 0.9, 5.0)):
            A.chunk((ww, dd, h * rnd.uniform(0.6, 1.0)), (x, y - d / 2 + (d / 2 if dd > 3 else 0.0), 0.8 + h / 2), V['char'] if i % 2 == 0 and i != 0 else V['stone2'], (0, 0, 0), 0.08, rnd, (0.96, 0.96))
        for k in range(4):
            A.box((1.8, 0.6, 2.6), (-w / 2 + 3.0 + k * (w - 5.0) / 3.0, -0.5 - d / 2 + d / 2, 4.4), V['dark'], bev=0)
        for k in range(8):
            A.beam((-w / 2 + k * 2.0, -d / 2, 5.0), (-w / 2 + k * 2.0 + rnd.uniform(-1, 1), d / 2, 5.0 + rnd.uniform(-2, 4)), 0.5, 0.5, V['char'])
        A.box((2.0, 2.0, 12.0), (w / 2 - 1.0, d / 2, 6.0), V['stone2'], bev=0.1)
    for k in range(22):
        A.chunk((rnd.uniform(1.0, 3.0), rnd.uniform(1.0, 3.0), rnd.uniform(0.4, 1.4)), (rnd.uniform(-10, 10), rnd.uniform(-9, 9), 1.0), V['char'] if k % 2 else V['ash'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(8):
        A.cyl(0.12, rnd.uniform(1.0, 2.6), (rnd.uniform(-8, 8), rnd.uniform(-6, 6), 0.8), V['char'], verts=5, r2=0.05)
    for k in range(5):
        A.cyl(0.4, rnd.uniform(1.4, 2.4), (rnd.uniform(-9, 9), rnd.uniform(-8, 0), 0.8), V['char'], verts=6, rot=(90, 0, rnd.uniform(0, 180)))
    return _fin(A, 'collapsed_house')


def _viaduct(i):
    reset()
    A = Acc()
    rnd = random.Random(10300 + i)
    n = 5
    span = 160.0 / n
    for k in range(n + 1):
        x = -80.0 + k * span
        A.box((6.0, 12.0, 28.0 - (6.0 if k in (0, n) else 0.0)), (x, 0, 14.0), V['stone'], bev=0.3)
        A.box((7.0, 13.0, 1.2), (x, 0, 28.6), V['trim'], bev=0.1)
    for k in range(n):
        xc = -80.0 + (k + 0.5) * span
        A.sweep([(span / 2.0 - 3.0, -6.0), (span / 2.0 - 0.6, -6.0), (span / 2.0 - 0.6, 6.0), (span / 2.0 - 3.0, 6.0)], 0, 180, 12, V['stone'], loc=(xc, 0, 14.0), rot=(90, 0, 0))
        A.box((span - 6.0, 12.0, 7.0), (xc, 0, 24.5), V['stone'], bev=0.2)
        for z in (10.0, 20.0):
            pass
    A.box((160.0, 12.0, 3.0), (0, 0, 29.8 - 0.0), V['stone2'], bev=0.2)
    for sg in (-1, 1):
        A.box((160.0, 1.0, 2.0), (0, sg * 5.6, 32.4), V['trim'], bev=0.1)
        for k in range(26):
            A.box((2.4, 1.2, 1.6), (-76.0 + k * 6.1, sg * 5.6, 34.0), V['stone'], bev=0.08)
    A.box((160.0, 7.0, 0.5), (0, 0, 31.5), V['dirt'], bev=0)
    v4util.marker('mk_enda', (-80.0, 0, 31.8))
    v4util.marker('mk_endb', (80.0, 0, 31.8))
    v4util.marker('mk_deck', (0, 0, 31.8))
    if i == 1:
        for k in range(3):
            A.chunk((rnd.uniform(5, 9), rnd.uniform(5, 9), rnd.uniform(4, 8)), (-24.0 + k * 22.0, rnd.uniform(-4, 4), 33.0), V['stone2'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd) if False else None
        A.chunk((18.0, 12.0, 9.0), (28.0, 0, 33.0), V['stone2'], (0, 0, 8), 0.25, rnd)
    return _fin(A, 'stone_viaduct')


def _bank(i):
    reset()
    A = Acc()
    rnd = random.Random(10400 + i)
    A.mound(0, 0, 30.0, 20.0, 9.0 + i, 12, ROCKS, rnd, 0.0, 0.35, 0.8)
    for k in range(6):
        A.ball(rnd.uniform(1.0, 2.0), (rnd.uniform(-12, 12), rnd.uniform(-8, 8), rnd.uniform(1, 6)), V['moss'], segs=6, rings=4, scale=(1.4, 1.2, 0.5))
    for k in range(7):
        A.cyl(0.08, rnd.uniform(1.4, 3.0), (rnd.uniform(-13, 13), rnd.uniform(-9, 9), 0.6), V['grass'], verts=4, r2=0.02)
    return _fin(A, 'bank_rocks')


# ------------------------------------------------------------------ sky
def _float_island(i):
    reset()
    A = Acc()
    rnd = random.Random(10500 + i)
    A.cyl(34.0, 5.0, (0, 0, 22.0), V['grass'], verts=22, r2=33.0)
    A.cyl(33.0, 12.0, (0, 0, 10.0), V['rock2'], verts=22, r2=34.0, rot=(180, 0, 0)) if False else None
    A.cyl(33.0, 4.0, (0, 0, 18.5), V['dirt'], verts=22, r2=33.0)
    for k in range(10):                                                                          # hanging rock cone, facets
        t = k / 9.0
        A.chunk((60.0 * (1.0 - 0.8 * t) + 6.0, 56.0 * (1.0 - 0.8 * t) + 6.0, 8.0), (rnd.uniform(-2, 2) * t, rnd.uniform(-2, 2) * t, 17.0 - k * 7.5), ROCKS[k % 3], (0, 0, rnd.uniform(0, 90)), 0.14, rnd, (0.82, 0.82))
    for k in range(7):
        a = k * 51.4
        x, y, _ = polar(rnd.uniform(16, 28), a)
        A.cyl(0.45, rnd.uniform(6, 16), (x, y, 14.0 if False else 18.0), V['moss'], verts=5, r2=0.1, rot=(180, 0, 0))
    round_tower(A, rnd, 6.5, 28.0 - i * 4, RUIN, rnd.uniform(-8, 8), rnd.uniform(-8, 8), 27.0, ruin=True, slits=2, bands=2)
    for k in range(5):
        column(A, rnd.uniform(-22, 22), rnd.uniform(-22, 22), 27.0, 1.2, rnd.uniform(6, 13), RUIN, 0.5, rnd)
    for k in range(5):
        G.tree(A, rnd, rnd.uniform(12, 20), rnd.uniform(4, 6), {'bark': V['bark'], 'leaf': V['leaf'], 'leaf2': V['leaf2'], 'bloom': V['leaf2']}, 'oak', rnd.uniform(-24, 24), rnd.uniform(-24, 24), 27.0)
    if i == 1:
        A.box((10.0, 10.0, 0.5), (14.0, -10.0, 27.4), V['water'], bev=0)
        A.box((2.4, 0.5, 10.0), (14.0, -15.2, 22.0), V['water'], bev=0)
    return _fin(A, 'floating_island')


def _float_rock(i):
    reset()
    A = Acc()
    rnd = random.Random(10600 + i)
    A.mound(0, 0, 36.0, 36.0, 14.0, 16, ROCKS, rnd, 8.0, 0.35, 0.8)
    A.chunk((24.0, 24.0, 2.4), (0, 0, 22.4), V['grass'], jit=0.06, rnd=rnd)
    for k in range(5):
        A.chunk((rnd.uniform(6, 12), rnd.uniform(6, 12), rnd.uniform(6, 10)), (rnd.uniform(-6, 6), rnd.uniform(-6, 6), 6.0 - k * 1.0), ROCKS[k % 3], (0, 0, rnd.uniform(0, 90)), 0.16, rnd, (0.5, 0.5))
    for k in range(5):
        A.ball(rnd.uniform(1.2, 2.2), (rnd.uniform(-9, 9), rnd.uniform(-9, 9), 24.0), V['ivy'], segs=7, rings=4, scale=(1.3, 1.1, 0.8))
    return _fin(A, 'floating_rock')


BATCHES = {
    'plains_set': ('v5_plains', mk(_L(_farm, 'PL01') + _L(_hay, 'PL02') + _L(_cart, 'PL03') + [(ids('PL04')[0], watermill)] + _L(_watch, 'PL05') + _L(_rock_bridge, 'PL06') +
                                  [(ids('VL01')[0], spired_church)], 0.1)),
    'ruins_crater': ('v5_landmarks', mk(_L(_rim_rock, 'LM19') + _L(_magic_ruin, 'LM20') + _L(_drift_slab, 'LM21') + _L(_arena, 'LM26') + _L(_aqueduct, 'LM27') +
                                       _L(_columns, 'LM28') + _L(_stump, 'LM29') + _L(_wall_module, 'LM31'), 0.1)),
    'coast_set': ('v5_coast', mk(_L(_reef, 'CO03') + _L(_sea_arch, 'CO04') + _L(_islet, 'CO05') + _L(_harbour_tower, 'HB01'), 0.1)),
    'road_life': ('v5_roads', mk(_L(_road_tower, 'RD01') + _L(_camp, 'RD02') + _L(_waystation, 'RD03') + _L(_trading, 'RD04') + _L(_military, 'RD05') +
                                _L(_burnt_house, 'RD06') + _L(_viaduct, 'BR01') + _L(_bank, 'RV01'), 0.1)),
    'sky': ('v5_coast', mk(_L(_float_island, 'FL01') + _L(_float_rock, 'FL02'), 0.1)),
}
