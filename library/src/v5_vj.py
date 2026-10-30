"""vj module - the four RW01 reworks of existing models (same footprints so the export replaces the old mesh in place):
RW01_01 = R03_03 badlands mesa with a CLOSED flat top (old one had an open lip), 75.7 x 70.3 x 79.9
RW01_02 = F08_13 stone gate: NOT rebuilt as an arch (the plain entrance arch was removed by decision); replaced by a natural entrance of two separate stone posts + sign, 24.3 x 7 x 19.8
RW01_03 = D01_02 elf treehouse B under 50k triangles, 50.5 x 49.2 x 65.4
RW01_04 = D01_04 elf treehouse D under 50k triangles, 53.6 x 53.6 x 59.4
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v5kit
from v5kit import Acc, polar, tang, mk, ids
import v5gen as G
import v5_ve as VE
import v4util

E = VE.E
M = G.reg('vj', {
    'red': ((176, 92, 60), 'Sandstone', 0.0, 0.95), 'red2': ((150, 70, 48), 'Sandstone', 0.0, 0.95), 'sand': ((214, 184, 140), 'Sandstone', 0.0, 0.95),
    'cream': ((226, 208, 170), 'Sandstone', 0.0, 0.95), 'sandl': ((234, 210, 168), 'Sandstone', 0.0, 0.95), 'orange': ((200, 120, 70), 'Sandstone', 0.0, 0.95),
    'stone': ((128, 124, 120), 'Slate', 0.0, 0.95), 'stone2': ((150, 146, 140), 'Cobblestone', 0.0, 0.95), 'moss': ((92, 124, 72), 'Grass', 0.0, 1.0),
    'plank': ((134, 108, 80), 'WoodPlanks', 0.0, 0.9), 'rope': ((176, 150, 104), 'Fabric', 0.0, 1.0), 'cloth': ((168, 52, 52), 'Fabric', 0.0, 1.0),
})
BANDS = [M['red'], M['sand'], M['red2'], M['cream'], M['orange'], M['sand']]


def _fin(A, name):
    A.to_scene()
    return finalize(name, 28)


def mesa_closed():
    reset()
    A = Acc()
    rnd = random.Random(11000)
    A.mound(0, 0, 76.0, 70.0, 12.0, 30, [M['sand'], M['cream'], M['orange']], rnd, 0.0, 0.3, 0.55, 0.1)
    z, k = 6.0, 0
    while z < 70.0:
        sh = rnd.uniform(5.5, 8.5)
        t = z / 80.0
        A.chunk((62.0 * (1.0 - 0.1 * t) + rnd.uniform(-1, 1), 56.0 * (1.0 - 0.1 * t) + rnd.uniform(-1, 1), sh * 1.06), (rnd.uniform(-0.8, 0.8), rnd.uniform(-0.8, 0.8), z + sh / 2.0),
                BANDS[k % 6], (0, 0, rnd.uniform(-3, 3)), 0.05, rnd, (0.97, 0.97))
        z += sh * 0.95
        k += 1
    A.chunk((60.0, 54.0, 3.0), (0, 0, z + 0.2), M['sandl'], (0, 0, 0), 0.03, rnd)                # solid closed cap plate
    A.chunk((52.0, 46.0, 1.4), (0, 0, z + 2.1), M['cream'], (0, 0, 0), 0.04, rnd)
    for j in range(14):                                                                          # slumped talus and ledges so the edge reads as eroded, not as a lip
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(26, 34), a)
        A.chunk((rnd.uniform(6, 12), rnd.uniform(5, 10), rnd.uniform(8, 20)), (x, y * 0.9, rnd.uniform(6, 26)), BANDS[j % 6], (0, 0, a), 0.16, rnd, (0.8, 0.8))
    for j in range(10):
        A.ball(rnd.uniform(1.4, 2.6), (rnd.uniform(-20, 20), rnd.uniform(-18, 18), z + 2.9), M['moss'], segs=6, rings=4, scale=(1.5, 1.2, 0.35))
    ob = _fin(A, 'badlands_mesa_closed')
    return v5kit.fit(ob, w=75.7, d=70.3, h=79.9)


def natural_gate():
    reset()
    A = Acc()
    rnd = random.Random(11001)
    for sg in (-1, 1):                                                                           # two separate rough gateposts, NO lintel
        for k in range(4):
            A.chunk((5.0 - k * 0.6, 4.2 - k * 0.4, 5.2), (sg * 9.5 + rnd.uniform(-0.3, 0.3), rnd.uniform(-0.4, 0.4), 2.6 + k * 4.4), (M['stone'], M['stone2'])[k % 2], (0, 0, rnd.uniform(-8, 8)), 0.08, rnd, (0.93, 0.93))
        A.ball(1.4, (sg * 9.5, 0, 20.0), M['moss'], segs=7, rings=4, scale=(1.4, 1.2, 0.5))
    A.box((8.0, 0.6, 3.6), (0, 0, 13.0), M['plank'], bev=0.06)                                    # a carved sign hung between low posts
    for sx in (-4.2, 4.2):
        A.cyl(0.3, 7.6, (sx, 0, 6.0), M['plank'], verts=6)
    A.box((8.4, 0.5, 0.4), (0, 0, 15.0), M['plank'], bev=0)
    for sx in (-3.0, 3.0):
        A.beam((sx, 0, 15.0), (sx, 0, 14.8), 0.12, 0.12, M['rope'])
    for k in range(6):
        A.chunk((rnd.uniform(1.2, 2.6), rnd.uniform(1.2, 2.6), rnd.uniform(0.6, 1.4)), (rnd.uniform(-11, 11), rnd.uniform(-2.5, 2.5), 0.6), M['stone2'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    ob = _fin(A, 'natural_entrance_gateposts')
    return v5kit.fit(ob, w=24.3, d=7.0, h=19.8)


def treehouse(var):
    reset()
    A = Acc()
    rnd = random.Random(11100 + var)
    H = 40.0 if var == 0 else 36.0
    A.cyl(8.0, H + 6.0, (0, 0, 0), E['bark'], verts=16, r2=5.4)
    for k in range(6):
        x, y, _ = polar(7.0, k * 60.0 + 12.0)
        A.beam((x * 2.1, y * 2.1, 0.0), (x * 0.7, y * 0.7, 9.0), 3.0, 3.0, E['wood'])
    z1 = 22.0 if var == 0 else 20.0
    VE._deck(A, rnd, 0, 0, z1, 17.0, 0.8, True, 24, 270.0)
    VE._hut(A, rnd, 0, 0, z1 + 0.8, 9.0, 8.5, 4, True, 18, 0.85)
    for k in range(34):                                                                          # spiral stair around the trunk
        a = 200.0 + k * 13.0
        x, y, _ = polar(9.6, a)
        A.box((4.4, 2.4, 0.6), (x, y, 1.0 + k * (z1 - 1.0) / 34.0), E['plank'], (0, 0, a + 90.0), bev=0.04)
    a2 = 60.0 if var == 0 else 120.0
    x2, y2, _ = polar(15.0, a2)
    z2 = z1 + 13.0
    A.beam((0, 0, z2 - 1.5), (x2, y2, z2 - 0.8), 1.4, 1.4, E['wood'])
    VE._deck(A, rnd, x2, y2, z2, 8.5, 0.7, True, 18, a2 + 180.0)
    VE._hut(A, rnd, x2, y2, z2 + 0.7, 4.8, 4.8, 2, True, 14, 0.9)
    a3 = 250.0 + 40.0 * var
    x3, y3, _ = polar(24.0, a3)
    z3 = z1 + 4.0
    VE._deck(A, rnd, x3, y3, z3, 7.0, 0.7, True, 16, a3 + 180.0)
    VE._mushrooms(A, rnd, x3, y3, z3 + 0.7, 4.0, 3)
    px, py, _ = polar(16.5, a3)
    n = 22
    for s in range(n):                                                                           # rope bridge between the main deck and the third platform
        t = (s + 0.5) / n
        bx, by = px + (x3 - px) * t, py + (y3 - py) * t
        A.box((0.8, 2.2, 0.2), (bx, by, z1 + 0.8 + (z3 + 0.7 - z1 - 0.8) * t - 1.0 * 4 * t * (1 - t)), E['plank'], (0, 0, math.degrees(math.atan2(y3 - py, x3 - px))), bev=0)
    for sg in (-1, 1):
        prev = None
        for s in range(8):
            t = s / 7.0
            tx, ty = tang(a3)
            q = (px + (x3 - px) * t + tx * sg * 1.2, py + (y3 - py) * t + ty * sg * 1.2, z1 + 0.8 + (z3 + 0.7 - z1 - 0.8) * t - 1.0 * 4 * t * (1 - t) + 1.7)
            if prev:
                A.beam(prev, q, 0.12, 0.12, E['rope'])
            prev = q
    xl, yl, _ = polar(11.0, 90.0)
    VE._ladder(A, xl, yl, z1 + 0.8, z2, E['wood'], 90.0)
    for k in range(9):                                                                           # crown of the tree: foliage clumps and limbs
        a = 40.0 * k
        x, y, _ = polar(rnd.uniform(6, 15), a)
        zt = H + rnd.uniform(0, 14)
        A.beam((0, 0, H - 4.0), (x, y, zt), 2.6, 2.4, E['wood'])
        for j in range(3):
            A.ball(rnd.uniform(6.0, 10.5), (x + rnd.uniform(-3, 3), y + rnd.uniform(-3, 3), zt + j * 3.0), E['leaf1'] if (k + j) % 2 else E['leaf2'], segs=10, rings=7, scale=(1.0, 1.0, 0.8))
    for k in range(6):
        x, y, _ = polar(rnd.uniform(14, 22), rnd.uniform(0, 360))
        A.ball(rnd.uniform(1.6, 3.0), (x, y, 0.8), E['moss'], segs=7, rings=4, scale=(1.5, 1.2, 0.5))
    v4util.marker('mk_lb', (xl, yl, z1 + 0.8))
    v4util.marker('mk_lt', (xl, yl, z2))
    ob = _fin(A, 'elf_treehouse')
    return v5kit.fit(ob, w=50.5 if var == 0 else 53.6, d=49.2 if var == 0 else 53.6, h=65.4 if var == 0 else 59.4)


def _tree_b():
    return treehouse(0)


def _tree_d():
    return treehouse(1)


BATCHES = {
    'reworks': ('v5_rework', list(zip(ids('RW01'), [mesa_closed, natural_gate, _tree_b, _tree_d]))),
}
