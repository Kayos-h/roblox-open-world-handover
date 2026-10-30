"""vh module - desert and Skull City: DS01 desert houses, DS02 well/awning/stall sets, DS03 caravan wagons, DS04 oasis palms, DS05 oasis rocks,
DS06 canyon walls, DS07 hoodoos and rock arches, DS08 stair-down entrances, SD01 mesa clusters, SD02 sand-worn ruined blocks,
LM10 colonnades, LM11 half-buried gate, LM12 stair into the sand, LM13 guardian figures, LM14 obelisks, LM16 ring wall segments, LM17 inner sanctum,
VC01 volcanic rock formations (no emissive; lava is terrain paint), VC03 dark fort ruins, VC04 ruined dark-stone houses. Original designs, front faces -Y.
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v5kit
from v5kit import Acc, polar, tang, mk, ids
import v5gen as G
from v5gen import round_tower, wall_seg, column, cliff, spire, rock_arch
import v4util

D = G.reg('vh', {
    'sand': ((214, 184, 140), 'Sandstone', 0.0, 0.95), 'sand2': ((194, 156, 108), 'Sandstone', 0.0, 0.95), 'sandl': ((234, 210, 168), 'Sandstone', 0.0, 0.95),
    'red': ((176, 92, 60), 'Sandstone', 0.0, 0.95), 'red2': ((150, 70, 48), 'Sandstone', 0.0, 0.95), 'cream': ((226, 208, 170), 'Sandstone', 0.0, 0.95),
    'lime': ((238, 230, 210), 'Concrete', 0.0, 0.9), 'clay': ((190, 122, 88), 'Brick', 0.0, 0.9), 'wood': ((118, 86, 56), 'Wood', 0.0, 0.9),
    'plank': ((150, 112, 76), 'WoodPlanks', 0.0, 0.9), 'cloth1': ((60, 100, 140), 'Fabric', 0.0, 1.0), 'cloth2': ((170, 60, 50), 'Fabric', 0.0, 1.0),
    'cloth3': ((204, 150, 70), 'Fabric', 0.0, 1.0), 'cloth4': ((70, 110, 80), 'Fabric', 0.0, 1.0), 'canvas': ((226, 218, 196), 'Fabric', 0.0, 1.0),
    'stone': ((150, 140, 125), 'Limestone', 0.0, 0.92), 'dark': ((46, 40, 38), 'Slate', 0.0, 0.95), 'palm': ((84, 128, 70), 'Grass', 0.0, 1.0),
    'palm2': ((112, 150, 78), 'Grass', 0.0, 1.0), 'bark': ((120, 96, 68), 'Wood', 0.0, 0.95), 'water': ((76, 150, 170), 'SmoothPlastic', 0.0, 0.2),
    'reed': ((150, 150, 84), 'Grass', 0.0, 1.0), 'iron': ((58, 58, 64), 'Metal', 0.6, 0.6), 'gold': ((196, 160, 84), 'Metal', 0.8, 0.35),
    'basalt': ((52, 52, 60), 'Basalt', 0.0, 0.9), 'basalt2': ((72, 70, 78), 'Basalt', 0.0, 0.9), 'ash': ((98, 92, 94), 'Slate', 0.0, 0.95),
    'rust': ((120, 70, 56), 'Slate', 0.0, 0.95), 'bone': ((222, 214, 196), 'Limestone', 0.0, 0.85), 'rope': ((176, 150, 104), 'Fabric', 0.0, 1.0),
    'glass': ((86, 104, 128), 'SmoothPlastic', 0.0, 0.3), 'shadow': ((26, 24, 30), 'Slate', 0.0, 0.95), 'moss': ((92, 124, 72), 'Grass', 0.0, 1.0),
})
DK = {'stone': D['basalt2'], 'wall': D['ash'], 'trim': D['rust'], 'dark': D['shadow'], 'door': D['wood'], 'deck': D['basalt'], 'roof': D['basalt'], 'roof2': D['basalt2'],
      'gold': D['iron'], 'timber': D['wood'], 'flag': D['cloth2'], 'cap': D['ash'], 'glass': D['shadow'], 'shutter': D['wood'], 'iron': D['iron'], 'sign': D['wood']}
SK = {'stone': D['sand2'], 'wall': D['sand'], 'trim': D['sandl'], 'dark': D['shadow'], 'door': D['wood'], 'deck': D['sand2'], 'roof': D['red'], 'roof2': D['sand2'],
      'gold': D['gold'], 'timber': D['wood'], 'flag': D['cloth2'], 'cap': D['sandl'], 'glass': D['glass'], 'shutter': D['wood'], 'iron': D['iron'], 'sign': D['wood']}
STR = [D['red'], D['sand'], D['red2'], D['cream'], D['clay'], D['sand2']]


def _fin(A, name):
    A.to_scene()
    return finalize(name, 28)


def _scatter(A, rnd, n, rx, ry, keys, size=(1.0, 3.0), z=0.5):
    for k in range(n):
        A.chunk((rnd.uniform(*size), rnd.uniform(*size), rnd.uniform(0.6, size[1] * 0.7)), (rnd.uniform(-rx, rx), rnd.uniform(-ry, ry), z), keys[k % len(keys)],
                (0, 0, rnd.uniform(0, 90)), 0.2, rnd)


def _dune(A, rnd, cx, cy, w, d, h, n=6):
    A.mound(cx, cy, w, d, h, n, [D['sand'], D['sandl'], D['sand2']], rnd, 0.0, 0.4, 0.8, 0.1)


# ------------------------------------------------------------------ DS01 desert houses
def _adobe(kind):
    reset()
    A = Acc()
    rnd = random.Random(6000 + len(kind))
    A.box((22.0, 20.0, 1.0), (0, 0, 0.5), D['stone'], bev=0.2)
    wall = D['sand'] if kind != 'merchant' else D['lime']

    def block(w, d, h, x=0.0, y=0.0, z=1.0, key=None):
        A.box((w, d, h), (x, y, z + h / 2.0), key or wall, bev=0.35)
        A.box((w + 0.8, d + 0.8, 0.7), (x, y, z + h + 0.35), D['sandl'], bev=0.15)
        for sx in (-1, 1):
            for sy in (-1, 1):
                A.box((0.9, 0.9, 0.9), (x + sx * w / 2.0, y + sy * d / 2.0, z + h + 1.0), D['sandl'], bev=0.12)
    def door(x, y, face, z=1.0):
        A.box((2.4, 0.5, 4.2), (x, y, z + 2.1), D['wood'], (0, 0, 0), bev=0.04)
        A.box((3.4, 0.9, 0.6), (x, y - 0.1, z + 4.5), D['stone'], bev=0.08)
        for sg in (-1, 1):
            A.box((0.5, 0.8, 4.4), (x + sg * 1.5, y - 0.1, z + 2.2), D['stone'], bev=0.08)
    def win(x, y, z, w=1.8, h=2.2):
        A.box((w, 0.4, h), (x, y, z), D['shadow'], bev=0)
        A.box((w + 0.8, 0.6, 0.45), (x, y - 0.1, z + h / 2.0 + 0.2), D['stone'], bev=0.04)
        A.box((w + 0.9, 0.9, 0.4), (x, y - 0.2, z - h / 2.0 - 0.2), D['stone'], bev=0.04)
    def dome(x, y, z, r, key=None):
        A.revolve([(r, 0.0), (r * 0.98, r * 0.2), (r * 0.85, r * 0.55), (r * 0.5, r * 0.85), (0.0, r * 1.05)], (x, y, z), key or D['lime'], segs=14)
        A.cyl(r * 1.05, 0.5, (x, y, z - 0.1), D['sandl'], verts=14)
        A.cyl(0.18, 1.8, (x, y, z + r * 1.0), D['gold'], verts=6)
    if kind == 'dome':
        block(14.0, 12.0, 7.0, 0, 0)
        dome(0, 0, 8.7, 5.2)
        door(0, -6.2, 270)
        win(-4.5, -6.15, 5.0)
        win(4.5, -6.15, 5.0)
        block(7.0, 6.0, 5.0, 8.0, -4.0, 1.0)
    elif kind == 'terrace':
        block(16.0, 13.0, 6.0, 0, 0)
        block(11.0, 9.0, 5.0, -2.0, 1.0, 7.7)
        for i in range(8):
            A.box((2.4, 1.8, 0.8 * (i + 1)), (8.5 + (i % 2) * 0.0, -6.0 + i * 1.8, 1.0 + 0.4 * (i + 1)), D['sand2'], bev=0.1)
        door(0, -6.7, 270)
        win(-5.0, -6.65, 4.5)
        win(5.0, -6.65, 4.5)
        win(-4.0, -4.7, 10.5)
        for k in range(6):
            A.cyl(0.25, 3.0, (-6.0 + k * 2.2, 4.0, 13.0), D['wood'], verts=6, rot=(0, 90, 0))
        dome(5.0, 2.0, 13.0, 2.4, D['sandl'])
    elif kind == 'court':
        for sx, sy, w, d in ((-6.0, 0.0, 6.0, 16.0), (6.0, 0.0, 6.0, 16.0), (0.0, 7.0, 18.0, 4.0)):
            block(w, d, 6.0, sx, sy)
        door(0, -8.0, 270)
        A.box((18.0, 0.8, 4.0), (0, -8.0, 3.0), D['sand'], bev=0.2)
        A.cyl(1.6, 0.8, (0, 0, 1.0), D['stone'], verts=10)
        A.cyl(0.9, 0.4, (0, 0, 1.8), D['water'], verts=10)
        for k in range(4):
            win(-6.0 + (k % 2) * 12.0, -8.2 + 0.0 + (k // 2) * 0.0 - 0.0, 4.5) if False else win(-6.0, -8.15, 4.5)
    elif kind == 'tower':
        block(9.0, 9.0, 16.0, 0, 0)
        block(6.0, 6.0, 5.0, 0, 0, 17.7)
        for z in (5.0, 10.0, 15.0):
            win(0, -4.65, z)
        door(0, -4.7, 270)
        A.frustum((7.0, 7.0), (0.5, 0.5), 5.0, (0, 0, 24.2), D['red'])
        A.box((2.0, 2.0, 6.0), (4.0, 3.0, 22.0), D['sand2'], bev=0.2)
        for z in (12.0, 20.0):
            for sx in (-1, 1):
                A.box((0.3, 0.3, 3.0), (sx * 4.6, -2.0, z), D['wood'], bev=0)
    elif kind == 'merchant':
        block(18.0, 14.0, 7.0, 0, 0, 1.0, D['lime'])
        A.box((20.0, 4.0, 0.4), (0, -9.0, 5.8), D['canvas'], (-10, 0, 0), bev=0)
        for sx in (-8.0, 8.0):
            A.cyl(0.3, 5.8, (sx, -10.5, 1.0), D['wood'], verts=6)
        door(0, -7.2, 270)
        for sx in (-6.0, 6.0):
            win(sx, -7.15, 4.5)
        A.box((3.0, 3.0, 9.0), (6.0, 3.0, 12.0), D['sand'], bev=0.2)                              # wind catcher
        for sx in (-1, 1):
            A.box((0.3, 3.1, 4.0), (6.0 + sx * 1.0, 3.0, 14.0), D['shadow'], bev=0)
        A.box((4.0, 4.0, 0.7), (6.0, 3.0, 16.8), D['sandl'], bev=0.1)
        for k in range(3):
            A.box((2.6, 1.4, 1.2), (-6.0 + k * 3.0, -10.0, 1.6), (D['cloth1'], D['cloth2'], D['cloth3'])[k], bev=0.08)
    else:                                                                                      # two-storey with a balcony
        block(15.0, 12.0, 6.0, 0, 0)
        block(15.0, 10.0, 5.0, 0, 1.0, 7.7)
        A.box((12.0, 3.0, 0.6), (0, -6.5, 7.4), D['plank'], bev=0.04)
        for k in range(9):
            A.box((0.25, 0.25, 1.4), (-5.5 + k * 1.4, -7.9, 8.4), D['wood'], bev=0)
        A.box((12.0, 0.3, 0.3), (0, -7.9, 9.1), D['wood'], bev=0)
        door(0, -6.2, 270)
        win(-4.5, -6.15, 4.5)
        win(4.5, -6.15, 4.5)
        win(-3.5, -4.15, 10.5)
        win(3.5, -4.15, 10.5)
        for k in range(3):
            A.cyl(0.25, 3.0, (-5.0 + k * 5.0, 4.0, 12.8), D['wood'], verts=6, rot=(0, 90, 0))
    A.box((20.0, 0.3, 4.0), (0, -9.4, 1.4), D['cloth1' if kind in ('dome', 'court') else 'cloth3'], (-8, 0, 0), bev=0) if kind in ('dome', 'court', 'tower') else None
    _scatter(A, rnd, 8, 10.0, 9.0, [D['sand2'], D['stone']], (0.8, 2.0), 0.7)
    return _fin(A, 'desert_house')


KINDS = ['dome', 'terrace', 'court', 'tower', 'merchant', 'balcony']


def _mk_house(i):
    return lambda: _adobe(KINDS[i % 6])


# ------------------------------------------------------------------ DS02-DS05 village sets
def _village_set(i):
    reset()
    A = Acc()
    rnd = random.Random(6100 + i)
    if i == 0:                                                                                   # well with a rope and a bucket
        A.cyl(6.0, 1.0, (0, 0, 0), D['stone'], verts=16)
        A.cyl(4.0, 4.0, (0, 0, 1.0), D['sand'], verts=14, r2=3.8)
        A.sweep([(2.6, 0.0), (4.4, 0.0), (4.4, 0.7), (2.6, 0.7)], 0, 360, 14, D['sandl'], loc=(0, 0, 5.0))
        A.cyl(2.6, 0.2, (0, 0, 4.2), D['water'], verts=14)
        for sx in (-1, 1):
            A.box((0.7, 0.7, 7.0), (sx * 3.6, 0, 5.0), D['wood'], bev=0.08)
            A.beam((sx * 3.6, 0, 7.6), (sx * 1.6, 0, 9.6), 0.5, 0.5, D['wood'])
        A.cyl(0.3, 8.0, (0, 0, 9.6), D['wood'], verts=6, rot=(0, 90, 0))
        A.beam((0.4, 0, 9.5), (0.4, 0, 6.5), 0.1, 0.1, D['rope'])
        A.cyl(0.7, 1.0, (0.4, 0, 5.4), D['wood'], verts=8)
        A.gable(10.0, 9.0, 2.0, (0, 0, 10.0), D['canvas'], (0, 0, 90)) if False else None
        A.box((12.0, 6.0, 0.3), (-5.0, -8.0, 0.9), D['plank'], bev=0)
        for k in range(3):
            A.cyl(1.0, 1.6, (-8.0 + k * 3.0, -8.0, 1.0), D['clay'], verts=10, r2=0.8)
    elif i == 1:                                                                                 # awning with rugs and cushions
        for sx in (-8.0, 8.0):
            for sy in (-4.0, 4.0):
                A.cyl(0.32, 10.0, (sx, sy, 0), D['wood'], verts=6)
        A.box((17.0, 9.6, 0.25), (0, 0, 10.0), D['cloth2'], (4, 0, 0), bev=0)
        for k in range(9):
            A.box((1.0, 9.8, 0.28), (-8.0 + k * 2.0, 0, 10.1), D['canvas'], (4, 0, 0), bev=0) if k % 2 == 0 else None
        for k, c in enumerate((D['cloth1'], D['cloth3'], D['cloth4'], D['cloth2'])):
            A.box((6.0, 4.0, 0.15), (-5.0 + (k % 2) * 9.0, -2.0 + (k // 2) * 4.0, 0.2), c, (0, 0, rnd.uniform(-8, 8)), bev=0)
            A.ball(1.0, (-5.0 + (k % 2) * 9.0 + 1.0, -2.0 + (k // 2) * 4.0, 0.9), c, segs=8, rings=5, scale=(1.3, 1.0, 0.6))
        A.box((4.0, 2.0, 2.0), (0, 5.0, 1.0), D['wood'], bev=0.08)
        A.cyl(0.8, 1.6, (-1.0, 5.0, 2.8), D['gold'], verts=8, r2=0.5)
    else:                                                                                        # market stall with goods
        A.box((10.0, 5.0, 3.0), (0, 0, 1.5), D['plank'], bev=0.1)
        for sx in (-5.0, 5.0):
            A.cyl(0.3, 9.0, (sx, 2.4, 0), D['wood'], verts=6)
            A.cyl(0.3, 7.0, (sx, -2.4, 0), D['wood'], verts=6)
        A.box((11.0, 7.0, 0.25), (0, 0, 8.4), D['cloth3'], (-14, 0, 0), bev=0)
        for k in range(5):
            A.box((1.1, 6.6, 0.28), (-4.8 + k * 2.4, 0, 8.5), D['canvas'], (-14, 0, 0), bev=0) if k % 2 == 0 else None
        for k in range(6):
            A.ball(rnd.uniform(0.6, 0.9), (-4.0 + k * 1.6, -0.5, 3.6), (D['cloth2'], D['cloth3'], D['palm2'])[k % 3], segs=7, rings=4)
        for k in range(3):
            A.cyl(0.9, 1.5, (-3.0 + k * 3.0, 1.2, 3.0), D['clay'], verts=10, r2=0.7)
    _scatter(A, rnd, 6, 10.0, 7.0, [D['sand2']], (0.6, 1.6), 0.5)
    return _fin(A, 'village_set')


def _wagon(i):
    reset()
    A = Acc()
    rnd = random.Random(6200 + i)
    A.box((14.0, 6.0, 0.6), (0, 0, 2.6), D['plank'], bev=0.06)
    for sg in (-1, 1):
        for sx in (-4.5, 4.5):
            A.cyl(2.6, 0.5, (sx, sg * 3.3, 2.6), D['wood'], verts=16, rot=(90, 0, 0))
            A.cyl(0.5, 0.8, (sx, sg * 3.3, 2.6), D['iron'], verts=8, rot=(90, 0, 0))
            for k in range(6):
                A.box((0.22, 0.3, 5.0), (sx, sg * 3.3, 2.6), D['wood'], (k * 30.0, 0, 0), bev=0)
        A.box((14.0, 0.3, 1.4), (0, sg * 2.9, 3.6), D['plank'], bev=0)
    for k in range(5):
        A.sweep([(2.9, 0.0), (3.1, 0.0), (3.1, 0.3), (2.9, 0.3)], 0, 180, 8, D['wood'], loc=(-5.6 + k * 2.8, 0, 3.0), rot=(90, 0, 90))
    A.cyl(3.1, 12.0, (-6.0, 0, 3.0), D['canvas'] if i == 0 else D['cloth2'], verts=10, r2=3.1, rot=(0, 90, 0)) if False else A.frustum((12.0, 6.4), (11.0, 3.0), 3.6, (0, 0, 4.0), D['canvas'] if i == 0 else D['cloth3'])
    A.beam((7.0, 0, 2.6), (13.0, 0, 2.0), 0.5, 0.5, D['wood'])
    A.box((2.4, 1.4, 1.4), (-3.0, 0, 3.8), D['clay'], bev=0.1)
    if i == 1:
        A.box((2.0, 1.6, 1.6), (3.0, 0, 3.8), D['plank'], bev=0.1)
        A.ball(1.0, (-1.0, 0, 3.8), D['cloth1'], segs=8, rings=5)
    return _fin(A, 'caravan_wagon')


def _palm(i):
    reset()
    A = Acc()
    rnd = random.Random(6300 + i)
    h = 40.0 - i * 2.0
    prev = (0, 0, 0.0)
    lean = (i - 1) * 3.0
    for s in range(1, 11):
        t = s / 10.0
        q = (lean * t * t, 0.8 * math.sin(t * 3.0), h * t)
        A.beam(prev, q, 1.5 - 0.7 * t, 1.5 - 0.7 * t, D['bark'])
        if s % 2 == 0:
            A.sweep([(0.6 - 0.3 * t, -0.18), (1.6 - 0.7 * t, -0.18), (1.6 - 0.7 * t, 0.18), (0.6 - 0.3 * t, 0.18)], 0, 360, 8, D['bark'], loc=q)
        prev = q
    top = prev
    for k in range(10):                                                                          # fronds: arched leaf strips with leaflets
        a = 36.0 * k + rnd.uniform(-6, 6)
        pts = []
        for s in range(6):
            t = s / 5.0
            x, y, _ = polar(t * 12.0, a)
            pts.append((top[0] + x, top[1] + y, top[2] + 3.0 * math.sin(t * 1.4) - 6.0 * t * t + 1.0))
        for p0, p1 in zip(pts, pts[1:]):
            A.beam(p0, p1, 0.3, 0.2, D['bark'])
        for j, p in enumerate(pts[1:]):
            for sg in (-1, 1):
                tx, ty = tang(a)
                A.beam(p, (p[0] + tx * sg * 2.4, p[1] + ty * sg * 2.4, p[2] - 1.3), 0.5 - j * 0.05, 0.1, D['palm'] if (k + j) % 2 else D['palm2'])
    for k in range(5):
        x, y, _ = polar(1.2, k * 72.0)
        A.ball(0.7, (top[0] + x, top[1] + y, top[2] - 0.6), D['clay'], segs=6, rings=4)
    return _fin(A, 'oasis_palm')


def _oasis_rocks(i):
    reset()
    A = Acc()
    rnd = random.Random(6400 + i)
    A.cyl(19.0, 0.6, (0, 0, 0), D['water'], verts=28)
    A.sweep([(18.0, 0.0), (21.5, 0.0), (21.5, 0.8), (18.0, 0.8)], 0, 360, 28, D['sandl'])
    for k in range(18):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(19.0, 24.0), a)
        A.mound(x, y, rnd.uniform(4, 8), rnd.uniform(4, 8), rnd.uniform(3, 8 + i * 2), 4, [D['stone'], D['sand2'], D['red']], rnd, 0.0, 0.5, 0.9)
    for k in range(22):
        x, y, _ = polar(rnd.uniform(15.0, 19.5), rnd.uniform(0, 360))
        A.cyl(0.07, rnd.uniform(2.0, 4.0), (x, y, 0.5), D['reed'], verts=4, r2=0.02, rot=(rnd.uniform(-8, 8), rnd.uniform(-8, 8), 0))
    for k in range(5):
        x, y, _ = polar(rnd.uniform(5, 13), rnd.uniform(0, 360))
        A.ball(rnd.uniform(1.4, 2.4), (x, y, 0.7), D['palm2'], segs=7, rings=4, scale=(1.6, 1.2, 0.3))
    return _fin(A, 'oasis_rocks')


# ------------------------------------------------------------------ DS06-DS08, SD01-SD02 land
def _canyon(i):
    reset()
    A = Acc()
    rnd = random.Random(6500 + i)
    G.cliff(A, rnd, 120.0, 40.0, 90.0, STR, 0, 0, 0, 14, D['sandl'], True, 0.0 if i % 2 else 0.12)
    for k in range(7):
        z = 8.0 + k * 11.0
        A.box((124.0, 1.2, 1.4), (0, -20.5, z), STR[(k + i) % 6], bev=0)
    for k in range(8):
        A.mound(rnd.uniform(-56, 56), -20.0, 12.0, 8.0, rnd.uniform(4, 10), 4, STR, rnd, 0.0, 0.5, 0.9)
    return _fin(A, 'canyon_wall')


def _hoodoo(i):
    reset()
    A = Acc()
    rnd = random.Random(6600 + i)
    if i < 2:
        A.mound(0, 0, 26.0, 22.0, 9.0, 10, STR[:4], rnd, 0.0, 0.5, 0.9)
        for k in range(1 + i):
            x = -8.0 + k * 14.0
            G.spire(A, rnd, 6.0 - k, 54.0 + k * 8, [D['red'], D['sand'], D['cream'], D['red2']], x, 0, 5.0, 8, 0.03 * k)
            A.chunk((12.0, 11.0, 5.0), (x, 0, 5.0 + 50.0 + k * 8 - 3.0), D['red2'], (0, 0, 20), 0.1, rnd, (1.0, 0.9))
        G.spire(A, rnd, 4.0, 36.0, STR[:3], 10.0, 6.0, 5.0, 6)
    else:
        G.rock_arch(A, rnd, 30.0, 40.0, 6.0, STR, 0, 0, 0, 12.0, 12, D['sandl'])
        A.mound(0, 0, 44.0, 20.0, 8.0, 10, STR, rnd, 0.0, 0.4, 0.8)
        if i == 3:
            G.spire(A, rnd, 4.0, 60.0, STR[:3], 18.0, 4.0, 5.0, 8)
    _scatter(A, rnd, 10, 18.0, 12.0, STR, (1.0, 2.4), 0.6)
    return _fin(A, 'hoodoo')


def _stair_down(i):
    reset()
    A = Acc()
    rnd = random.Random(6700 + i)
    _dune(A, rnd, 0, 8.0, 40.0, 22.0, 9.0, 10)
    n = 14
    for s in range(n):
        A.box((9.0, 1.6, 22.0 - s * 1.5), (0, -8.0 + s * 1.5 + 8.0, 11.0 - s * 0.75 + (s * 0.0)), D['sand2'], bev=0.04) if False else A.box((9.0, 1.6, 0.6), (0, -12.0 + s * 1.5, 14.0 - s * 1.0), D['sandl'], bev=0.06)
    for sg in (-1, 1):
        A.box((1.6, 22.0, 16.0), (sg * 5.6, 0, 8.0), D['sand'], bev=0.2)
        for s in range(0, n, 2):
            A.box((1.8, 1.6, 0.8), (sg * 5.6, -12.0 + s * 1.5, 14.8 - s * 1.0 + 0.4), D['sandl'], bev=0.08)
    A.box((11.0, 2.4, 2.4), (0, 3.0, 3.6), D['shadow'], bev=0)
    A.box((13.0, 3.0, 2.0), (0, 2.8, 5.4), D['sandl'], bev=0.2)
    for sg in (-1, 1):
        A.box((2.0, 3.0, 6.0), (sg * 5.8, 2.8, 3.0), D['sand'], bev=0.2)
    A.box((14.0, 0.5, 0.4), (0, -13.0, 14.6), D['canvas'], bev=0) if i == 2 else None
    _scatter(A, rnd, 10, 15.0, 12.0, [D['sand2'], D['stone']], (0.8, 2.0), 0.6)
    return _fin(A, 'stair_down')


def _mesa(i):
    reset()
    A = Acc()
    rnd = random.Random(6800 + i)
    A.mound(0, 0, 120.0, 100.0, 12.0, 26, [D['sand'], D['sandl'], D['sand2']], rnd, 0.0, 0.25, 0.5, 0.1)
    for b in range(3 + i % 2):
        cx = rnd.uniform(-34, 34)
        cy = rnd.uniform(-26, 26)
        w = rnd.uniform(26, 44)
        d = rnd.uniform(22, 36)
        h = rnd.uniform(56, 88) - b * 6.0
        z = 6.0
        k = 0
        while z < h:
            sh = rnd.uniform(5.0, 9.0)
            wd = w * (1.0 - 0.08 * k / 3.0)
            A.chunk((wd, d * (1.0 - 0.06 * k / 3.0), sh * 1.05), (cx + rnd.uniform(-0.8, 0.8), cy + rnd.uniform(-0.8, 0.8), z + sh / 2.0), STR[(k + b + i) % 6], (0, 0, rnd.uniform(-4, 4)), 0.07, rnd, (0.96, 0.96))
            z += sh * 0.95
            k += 1
        A.chunk((w * 0.92, d * 0.92, 3.0), (cx, cy, z + 0.6), D['sandl'], (0, 0, rnd.uniform(-5, 5)), 0.05, rnd)
        for j in range(8):
            a = rnd.uniform(0, 360)
            x, y, _ = polar(max(w, d) * 0.55, a)
            A.chunk((rnd.uniform(5, 10), rnd.uniform(4, 8), rnd.uniform(6, 14)), (cx + x, cy + y, rnd.uniform(5, 14)), STR[j % 6], (0, 0, a), 0.15, rnd, (0.8, 0.8))
    return _fin(A, 'mesa_cluster')


def _ruin_block(i):
    reset()
    A = Acc()
    rnd = random.Random(6900 + i)
    A.box((40.0, 38.0, 1.0), (0, 0, 0.5), D['sand2'], bev=0.2)
    for (x, y, w, d, h) in ((-9.0, -5.0, 14.0, 12.0, 14.0), (9.0, 3.0, 12.0, 14.0, 10.0), (-4.0, 11.0, 10.0, 10.0, 8.0), (11.0, -11.0, 9.0, 9.0, 12.0)):
        h2 = h * rnd.uniform(0.6, 1.0)
        A.box((w, d, h2), (x, y, 1.0 + h2 / 2.0), D['sand'], bev=0.3)
        for sx in (-1, 1):
            A.chunk((w * 0.4, d * 0.9, rnd.uniform(1.5, 4.5)), (x + sx * w * 0.3, y, 1.0 + h2 + 0.6), D['sand'], (0, 0, 0), 0.25, rnd)
        for k in range(2):
            A.box((2.0, 0.5, 2.6), (x - w / 4.0 + k * w / 2.0, y - d / 2.0 - 0.02, 1.0 + h2 * 0.55), D['shadow'], bev=0)
    for k in range(3 + i % 3):
        column(A, rnd.uniform(-14, 14), rnd.uniform(-14, 14), 1.0, 1.1, rnd.uniform(6, 14), SK, 0.5, rnd)
    A.mound(0, 0, 40.0, 38.0, 6.0, 12, [D['sand'], D['sandl']], rnd, 0.0, 0.3, 0.6)
    _scatter(A, rnd, 14, 18.0, 17.0, [D['sand2'], D['stone']], (0.8, 2.6), 1.0)
    return _fin(A, 'sand_ruin_block')


# ------------------------------------------------------------------ temple parts
def _colonnade(i):
    reset()
    A = Acc()
    rnd = random.Random(7000 + i)
    _dune(A, rnd, 0, 4.0, 62.0, 30.0, 9.0 + i * 2.0, 10)
    for k in range(5):
        column(A, -24.0 + k * 12.0, -6.0, 5.0, 2.1, 22.0 if k % (i + 2) else 11.0, SK, 0.0 if k % (i + 2) else 0.7, rnd)
        column(A, -24.0 + k * 12.0, 6.0, 5.0, 2.1, 18.0 if (k + i) % 3 else 8.0, SK, 0.0 if (k + i) % 3 else 0.8, rnd)
    for k in range(3):
        A.box((16.0, 5.0, 2.4), (-24.0 + k * 12.0 + 6.0, -6.0, 5.0 + 23.0 + 0.0), D['sand'], bev=0.2) if k < 2 and i < 2 else None
    _scatter(A, rnd, 12, 28.0, 14.0, [D['sand2'], D['stone']], (1.0, 3.4), 1.0)
    return _fin(A, 'colonnade')


def half_buried_gate():
    reset()
    A = Acc()
    rnd = random.Random(7100)
    for sg in (-1, 1):
        A.frustum((12.0, 10.0), (9.0, 8.0), 34.0, (sg * 14.0, 0, 12.0), D['sand'])
        for k in range(4):
            A.box((13.0, 11.0, 0.8), (sg * 14.0, 0, 16.0 + k * 7.0), D['sandl'], bev=0.1)
    A.box((44.0, 9.0, 5.0), (0, 0, 46.0), D['sand2'], bev=0.3)
    for k in range(4):
        A.box((8.0, 0.5, 4.0), (-12.0 + k * 8.0, -4.8, 46.0), D['red'], bev=0.05)
    _dune(A, rnd, 0, 0, 52.0, 24.0, 18.0, 14)
    A.chunk((20.0, 8.0, 4.0), (6.0, -4.0, 14.0), D['sand2'], (0, 8, 14), 0.15, rnd)
    return _fin(A, 'half_buried_gate')


def _sand_stair(i):
    reset()
    A = Acc()
    rnd = random.Random(7200 + i)
    _dune(A, rnd, 0, 4.0, 34.0, 38.0, 14.0, 12)
    for s in range(16):
        A.box((10.0, 1.8, 0.7), (0, -17.0 + s * 1.9, 22.0 - s * 1.35), D['sandl'], bev=0.06)
    for sg in (-1, 1):
        A.box((1.8, 32.0, 10.0), (sg * 6.2, -1.0, 14.0), D['sand'], bev=0.2)
    A.box((10.0, 2.0, 3.0), (0, 14.0, 4.0), D['shadow'], bev=0)
    column(A, -8.0, -16.0, 21.0, 1.1, 9.0, SK, 0.5 + 0.2 * i, rnd)
    return _fin(A, 'sand_stair')


def _guardian(i):
    reset()
    A = Acc()
    rnd = random.Random(7300 + i)
    A.box((14.0, 14.0, 4.0), (0, 0, 2.0), D['stone'], bev=0.3)
    A.box((10.0, 10.0, 3.0), (0, 0, 5.5), D['sand2'], bev=0.3)
    A.frustum((8.0, 6.0), (6.0, 4.6), 26.0, (0, 0, 7.0), D['sand'])                              # long robe
    A.frustum((9.0, 7.0), (8.0, 6.0), 3.0, (0, 0, 7.0), D['sandl'])
    A.frustum((7.4, 4.6), (9.6, 4.0), 14.0, (0, 0, 33.0), D['sand'])                              # chest and shoulders
    for sg in (-1, 1):
        A.beam((sg * 5.2, 0, 44.0), (sg * 6.0, -3.6, 37.0), 2.2, 2.2, D['sand'])
        A.beam((sg * 6.0, -3.6, 37.0), (sg * 4.0, -7.0, 36.0), 1.8, 1.8, D['sand'])
    A.cyl(0.4, 52.0, (6.0, -7.0, 6.0), D['wood'], verts=6)                                       # spear
    A.frustum((1.6, 0.8), (0.1, 0.1), 5.0, (6.0, -7.0, 57.0), D['iron'])
    A.cyl(2.0, 3.0, (0, 0, 46.5), D['sand'], verts=10)
    A.frustum((6.0, 6.6), (5.0, 5.4), 7.0, (0, -0.2, 49.0), D['sandl'])                          # hooded head
    A.box((3.8, 1.4, 1.2), (0, -3.1, 53.0), D['shadow'], bev=0)
    if i == 0:
        A.frustum((2.0, 2.0), (1.0, 4.0), 12.0, (-2.4, 0, 54.0), D['sandl'], (0, 0, 0), (0, 0)) if False else None
        for sg in (-1, 1):
            A.frustum((2.2, 2.0), (1.2, 1.4), 12.0, (sg * 2.6, 0.5, 55.6), D['sandl'])
    A.box((12.0, 0.6, 6.0), (0, -5.2, 12.0), D['red'], bev=0.05)
    for k in range(8):
        A.chunk((rnd.uniform(1.0, 2.4), rnd.uniform(1.0, 2.4), rnd.uniform(0.6, 1.6)), (rnd.uniform(-9, 9), rnd.uniform(-9, 9), 0.7), D['sand2'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    return _fin(A, 'guardian_figure')


def _obelisk(i):
    reset()
    A = Acc()
    rnd = random.Random(7400 + i)
    A.box((9.0, 9.0, 2.0), (0, 0, 1.0), D['stone'], bev=0.2)
    A.box((7.0, 7.0, 1.6), (0, 0, 2.8), D['sand2'], bev=0.2)
    A.frustum((5.2, 5.2), (3.2, 3.2), 50.0, (0, 0, 3.6), D['sand'])
    A.frustum((3.4, 3.4), (0.3, 0.3), 5.0, (0, 0, 53.6), D['red'])
    for k in range(7):
        z = 8.0 + k * 6.0
        for face in (270, 0, 90, 180):
            x, y, _ = polar(2.5 - k * 0.15, face)
            A.box((0.3, 1.8 - k * 0.1, 1.6), (x, y, z), D['red2'] if k % 2 else D['sandl'], (0, 0, face), bev=0)
        A.box((5.5 - k * 0.3, 5.5 - k * 0.3, 0.3), (0, 0, z - 2.2), D['sandl'], bev=0)
    for k in range(5):
        A.chunk((rnd.uniform(1.4, 3.0), rnd.uniform(1.4, 3.0), rnd.uniform(0.8, 2.0)), (rnd.uniform(-4.4, 4.4), rnd.uniform(-4.4, 4.4), 0.6), D['sand2'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    return _fin(A, 'obelisk')


def _ring_wall_seg(i):
    reset()
    A = Acc()
    rnd = random.Random(7500 + i)
    R = 80.0
    A.sweep([(R - 5.0, 0.0), (R + 5.0, 0.0), (R + 4.0, 24.0 - i * 4.0), (R - 4.0, 24.0 - i * 4.0)], -14, 14, 6, D['sand'])
    A.sweep([(R - 5.4, 24.0 - i * 4.0), (R + 5.4, 24.0 - i * 4.0), (R + 5.4, 25.2 - i * 4.0), (R - 5.4, 25.2 - i * 4.0)], -14, 14, 6, D['sandl'])
    for k in range(9):
        a = -12.0 + k * 3.0
        x, y, _ = polar(R + 4.6, a)
        if k % 3 != 1 or i == 0:
            A.box((2.4, 3.0, 2.6), (x, y, 26.4 - i * 4.0), D['sand'], (0, 0, a), bev=0.12)
    for k in range(4):
        x, y, _ = polar(R - 5.6, -10.0 + k * 6.5)
        A.box((2.2, 2.0, 18.0 - i * 3.0), (x, y, 9.0), D['sand2'], (0, 0, -10.0 + k * 6.5), bev=0.15)
    for k in range(5):
        A.box((0.3, 2.4, 3.6), (polar(R + 5.1, -10.0 + k * 5.0)[0], polar(R + 5.1, -10.0 + k * 5.0)[1], 14.0), D['red'], (0, 0, -10.0 + k * 5.0), bev=0)
    return _fin(A, 'ring_wall_segment')


def inner_sanctum():
    reset()
    A = Acc()
    rnd = random.Random(7600)
    A.box((60.0, 60.0, 4.0), (0, 0, 2.0), D['stone'], bev=0.4)
    A.box((50.0, 50.0, 3.0), (0, 0, 5.5), D['sand2'], bev=0.3)
    A.frustum((40.0, 40.0), (36.0, 36.0), 28.0, (0, 0, 7.0), D['sand'])
    for k in range(4):
        A.box((41.0, 41.0, 0.8), (0, 0, 14.0 + k * 6.0), D['sandl'], bev=0.1)
    A.frustum((42.0, 42.0), (4.0, 4.0), 22.0, (0, 0, 35.0), D['red'])
    for k in range(8):
        x = -17.5 + k * 5.0
        column(A, x, -24.0, 9.0, 1.6, 22.0, SK, 0.0, rnd)
    A.box((46.0, 4.0, 2.4), (0, -24.0, 32.0), D['sandl'], bev=0.2)
    A.box((10.0, 0.6, 12.0), (0, -20.2, 14.0), D['shadow'], bev=0)
    for sg in (-1, 1):
        A.box((2.0, 0.6, 12.4), (sg * 6.2, -20.1, 14.0), D['sandl'], bev=0.05)
    A.box((12.4, 0.6, 1.6), (0, -20.1, 20.4), D['sandl'], bev=0.05)
    for sx in (-1, 1):
        for sy in (-1, 1):
            A.frustum((6.0, 6.0), (3.0, 3.0), 12.0, (sx * 22.0, sy * 22.0, 7.0), D['sandl'])
    return _fin(A, 'inner_sanctum')


# ------------------------------------------------------------------ Skull City
def _volcanic(i):
    reset()
    A = Acc()
    rnd = random.Random(7700 + i)
    keys = [D['basalt'], D['basalt2'], D['ash']]
    A.mound(0, 0, 58.0, 56.0, 20.0 + (i % 3) * 4.0, 28, keys, rnd, 0.0, 0.3, 0.7, 0.13)
    for k in range(10 + i % 4):                                                                  # basalt column clusters
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(3.0, 20.0), a)
        for j in range(5):
            xx, yy, _ = polar(1.6 * (j > 0), j * 72.0)
            h = rnd.uniform(8.0, 30.0 + (i % 3) * 6.0) * (1.0 - 0.02 * math.hypot(x, y))
            A.cyl(1.5, h, (x + xx, y + yy, 2.0), keys[(j + k) % 3], verts=6, r2=1.35)
    for k in range(5):
        G.spire(A, rnd, rnd.uniform(3.0, 6.0), rnd.uniform(24.0, 46.0), keys, rnd.uniform(-18, 18), rnd.uniform(-16, 16), 4.0, 6, rnd.uniform(-0.1, 0.1))
    for k in range(18):
        A.chunk((rnd.uniform(1.4, 3.6), rnd.uniform(1.4, 3.6), rnd.uniform(0.8, 2.2)), (rnd.uniform(-28, 28), rnd.uniform(-26, 26), 1.0), D['rust'] if k % 5 == 0 else keys[k % 3], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    return _fin(A, 'volcanic_formation')


def _dark_fort(i):
    reset()
    A = Acc()
    rnd = random.Random(7800 + i)
    A.chunk((60.0, 50.0, 3.0), (0, 0, 1.5), D['basalt2'], jit=0.03, rnd=rnd)
    for k in range(5):
        h = rnd.uniform(10.0, 22.0)
        wall_seg(A, rnd, 12.0, h, 6.0, DK, -24.0 + k * 12.0, -22.0, 3.0, 4.5, k % 2 == 0, False)
    for sg in (-1, 1):
        A.chunk((6.0, 40.0, rnd.uniform(8.0, 18.0)), (sg * 27.0, 0, 3.0 + 7.0), D['basalt2'], (0, 0, 0), 0.1, rnd)
    round_tower(A, rnd, 7.5, 40.0 - i * 6.0, DK, -26.0, -22.0, 3.0, ruin=True, slits=3, bands=3)
    round_tower(A, rnd, 6.5, 28.0, DK, 26.0, -22.0, 3.0, ruin=(i != 1), slits=2, bands=2, top='crenel')
    A.frustum((20.0, 16.0), (18.0, 14.0), 22.0, (0, 10.0, 3.0), D['ash'])
    for k in range(10):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(9.0, a)
        A.chunk((rnd.uniform(2, 6), rnd.uniform(2, 6), rnd.uniform(1.0, 5.0)), (x, 10.0 + y * 0.8, 25.0 + rnd.uniform(-1, 3)), D['ash'], (0, 0, a), 0.2, rnd)
    for k in range(18):
        A.chunk((rnd.uniform(1.4, 4.0), rnd.uniform(1.4, 4.0), rnd.uniform(0.8, 2.4)), (rnd.uniform(-28, 28), rnd.uniform(-24, 24), 3.5), D['basalt2'] if k % 4 else D['rust'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    return _fin(A, 'dark_fort_ruin')


def _dark_house(i):
    reset()
    A = Acc()
    rnd = random.Random(7900 + i)
    A.box((26.0, 26.0, 1.0), (0, 0, 0.5), D['basalt2'], bev=0.2)
    w, d = (14.0, 12.0) if i % 2 == 0 else (18.0, 10.0)
    h = 8.0 + (i % 3) * 3.0
    for (x, y, ww, dd, hh) in ((0, 0, w, 0.9, h), (0, d, w, 0.9, h * 0.8), (-w / 2, d / 2, 0.9, d, h * 0.9), (w / 2, d / 2, 0.9, d, h * 0.6)):
        A.chunk((ww, dd, hh), (x, y - d / 2 + 0.0 + (d / 2 if dd > 3 else 0.0) * 0 + 0.0, 1.0 + hh / 2.0), D['ash'] if (x + y) % 2 else D['basalt2'], (0, 0, 0), 0.06, rnd, (0.96, 0.96))
    for k in range(4):
        A.box((1.8, 0.6, 2.6), (-w / 2 + 3.0 + k * (w - 5.0) / 3.0, -0.5, 1.0 + h * 0.55), D['shadow'], bev=0)
    A.box((2.6, 0.6, 4.2), (0, -0.5, 3.1), D['shadow'], bev=0)
    for k in range(5):                                                                           # broken roof beams
        A.beam((-w / 2 + k * w / 4.0, 0, 1.0 + h), (-w / 2 + k * w / 4.0 + rnd.uniform(-1, 1), d * 0.7, 1.0 + h + rnd.uniform(1.5, 5.0)), 0.5, 0.5, D['wood'])
    if i % 3 == 2:
        round_tower(A, rnd, 3.4, 20.0, DK, w / 2 + 3.0, 2.0, 1.0, ruin=True, slits=2, bands=1, verts=12)
    for k in range(10):
        A.chunk((rnd.uniform(1.0, 3.0), rnd.uniform(1.0, 3.0), rnd.uniform(0.6, 1.8)), (rnd.uniform(-11, 11), rnd.uniform(-11, 11), 1.2), D['basalt2'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    return _fin(A, 'dark_ruin_house')


def _L(fn, row):
    return [(m, (lambda j=j, f=fn: f(j))) for j, m in enumerate(ids(row))]


BATCHES = {
    'desert_village': ('v5_desert', mk(_L(_mk_house_wrap := (lambda j: _adobe(KINDS[j % 6])), 'DS01') + _L(_village_set, 'DS02') + _L(_wagon, 'DS03') + _L(_palm, 'DS04') +
                                      _L(_oasis_rocks, 'DS05'), 0.1)),
    'desert_land': ('v5_desert', mk(_L(_canyon, 'DS06') + _L(_hoodoo, 'DS07') + _L(_stair_down, 'DS08') + _L(_mesa, 'SD01') + _L(_ruin_block, 'SD02'), 0.1)),
    'temple_parts': ('v5_landmarks', mk(_L(_colonnade, 'LM10') + [(ids('LM11')[0], half_buried_gate)] + _L(_sand_stair, 'LM12') + _L(_guardian, 'LM13') +
                                       _L(_obelisk, 'LM14') + _L(_ring_wall_seg, 'LM16') + [(ids('LM17')[0], inner_sanctum)], 0.1)),
    'skull_set': ('v5_skull', mk(_L(_volcanic, 'VC01') + _L(_dark_fort, 'VC03') + _L(_dark_house, 'VC04'), 0.1)),
}
