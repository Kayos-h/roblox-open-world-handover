"""vf module - landmark heroes, trees and coast: LM03 frost fortress, LM22 colossal falls, LM25 ancient gate, LM30 ruined castle,
LM09 half-buried desert temple, LM15 ring temple, LM18 standing stones, VC02 skull cliffs (two designs), VG01-VG03 trees, CO01 coast cliffs, CO02 sea stacks.
Original designs. No glow. Front faces -Y. Briefs list sizes as (x, height, depth) in Roblox axes.
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v5kit
from v5kit import Acc, polar, tang, mk
import v5gen as G
from v5gen import round_tower, wall_seg, house, column, cliff, spire, rock_arch, tree
import v4util

P = G.reg('vf', {
    'rock': ((128, 124, 120), 'Slate', 0.0, 0.95), 'rock2': ((150, 146, 140), 'Cobblestone', 0.0, 0.95), 'dark': ((70, 70, 78), 'Granite', 0.0, 0.92),
    'snow': ((240, 244, 250), 'Snow', 0.0, 0.7), 'ice': ((196, 226, 242), 'Ice', 0.0, 0.3), 'wall': ((172, 166, 172), 'Limestone', 0.0, 0.9),
    'trim': ((214, 208, 210), 'Limestone', 0.0, 0.88), 'roof': ((74, 94, 128), 'Slate', 0.0, 0.8), 'timber': ((112, 92, 70), 'Wood', 0.0, 0.9),
    'sand': ((214, 184, 140), 'Sandstone', 0.0, 0.95), 'sand2': ((194, 156, 108), 'Sandstone', 0.0, 0.95), 'sandl': ((234, 210, 168), 'Sandstone', 0.0, 0.95),
    'red': ((176, 92, 60), 'Sandstone', 0.0, 0.95), 'moss': ((92, 124, 72), 'Grass', 0.0, 1.0), 'ivy': ((66, 102, 58), 'Grass', 0.0, 1.0),
    'water': ((96, 150, 180), 'SmoothPlastic', 0.0, 0.2), 'foam': ((236, 244, 248), 'SmoothPlastic', 0.0, 0.5), 'basalt': ((48, 48, 56), 'Basalt', 0.0, 0.9),
    'bone': ((222, 214, 196), 'Limestone', 0.0, 0.85), 'gold': ((196, 160, 84), 'Metal', 0.8, 0.35), 'iron': ((58, 58, 64), 'Metal', 0.6, 0.6),
    'bark': ((96, 74, 56), 'Wood', 0.0, 0.95), 'leaf': ((70, 120, 60), 'Grass', 0.0, 1.0), 'leaf2': ((104, 150, 80), 'Grass', 0.0, 1.0),
    'leafd': ((50, 84, 48), 'Grass', 0.0, 1.0), 'bloom': ((236, 176, 196), 'Grass', 0.0, 1.0), 'cloth': ((168, 52, 52), 'Fabric', 0.0, 1.0),
    'glass': ((86, 104, 128), 'SmoothPlastic', 0.0, 0.3), 'dstone': ((96, 92, 98), 'Granite', 0.0, 0.92), 'shadow': ((26, 24, 30), 'Slate', 0.0, 0.95),
    'beach': ((206, 196, 170), 'Sand', 0.0, 1.0), 'poplar': ((96, 132, 62), 'Grass', 0.0, 1.0), 'copper': ((92, 150, 128), 'Metal', 0.45, 0.55),
})
FK = {'stone': P['rock2'], 'wall': P['wall'], 'trim': P['trim'], 'dark': P['basalt'], 'door': P['timber'], 'deck': P['timber'], 'roof': P['roof'], 'roof2': P['rock'],
      'gold': P['gold'], 'timber': P['timber'], 'flag': P['cloth'], 'cap': P['snow'], 'glass': P['glass'], 'shutter': P['timber'], 'iron': P['iron'], 'sign': P['timber']}
RK = dict(FK, wall=P['sand'], stone=P['sand2'], trim=P['sandl'], roof=P['red'], roof2=P['sand2'], cap=P['sandl'])
CK = dict(FK, wall=P['rock2'], stone=P['rock'], trim=P['moss'], roof=P['rock'], cap=P['moss'])
TK = {'bark': P['bark'], 'leaf': P['leaf'], 'leaf2': P['leaf2'], 'bloom': P['bloom']}
TKD = {'bark': P['bark'], 'leaf': P['leafd'], 'leaf2': P['leaf'], 'bloom': P['leaf']}
TKP = {'bark': P['bark'], 'leaf': P['poplar'], 'leaf2': P['leaf2'], 'bloom': P['leaf']}


def _fin(A, name):
    A.to_scene()
    return finalize(name, 28)


def _snow(A, rnd, n, bx, by, bz, size=(6, 14)):
    for k in range(n):
        s = rnd.uniform(*size)
        A.chunk((s, s * rnd.uniform(0.7, 1.2), rnd.uniform(1.2, 2.6)), (rnd.uniform(*bx), rnd.uniform(*by), rnd.uniform(*bz)), P['snow'], (0, 0, rnd.uniform(0, 90)), 0.12, rnd)


# ------------------------------------------------------------------ LM03 frost fortress
def fortress():
    reset()
    A = Acc()
    rnd = random.Random(1001)
    G.cliff(A, rnd, 300.0, 110.0, 220.0, [P['rock'], P['dark'], P['rock2']], 0, 75.0, 0, 15, P['snow'], True, 0.1)
    for sx in (-150.0, 150.0):                                                                 # flanking buttress spurs
        G.cliff(A, rnd, 50.0, 60.0, 150.0, [P['rock'], P['dark']], sx * 0.9, 30.0, 0, 4, P['snow'], True, 0.0)
    _snow(A, rnd, 46, (-140, 140), (20, 120), (30, 210))
    levels = [(0.0, 230.0, -110.0), (46.0, 170.0, -66.0), (92.0, 112.0, -26.0)]            # (z, wall length, y of the front wall)
    for i, (z, L, y) in enumerate(levels):
        A.box((L + 12.0, 34.0, 4.0), (0, y + 12.0, z + 2.0), P['rock2'], bev=0.4)
        n = int(L / 40.0)
        for k in range(n):
            wall_seg(A, rnd, 40.0, 18.0, 9.0, FK, -L / 2.0 + 20.0 + k * 40.0 * (L / (n * 40.0)), y, z + 4.0, 7.0, k % 2 == 0, False)
        for sg in (-1, 1):
            round_tower(A, rnd, 10.0 - i * 1.2, 40.0 + i * 8.0, FK, sg * (L / 2.0 + 2.0), y, z + 4.0, top='cone', slits=3, bands=3, roof_k=1.5, verts=22)
        for k in range(3):
            h_ = 22.0 + 6.0 * ((k + i) % 2)
            A.frustum((26.0, 20.0), (24.0, 18.0), h_, (-L / 2.0 * 0.5 + k * L * 0.28 - 10.0, y + 22.0, z + 4.0), P['wall'])
            A.gable(22.0, 28.0, 10.0, (-L / 2.0 * 0.5 + k * L * 0.28 - 10.0, y + 22.0, z + 4.0 + h_), P['roof'], (0, 0, 90))
    A.frustum((50.0, 40.0), (44.0, 34.0), 62.0, (0, 10.0, 96.0), P['wall'])                    # central keep on the top terrace
    A.frustum((52.0, 42.0), (8.0, 8.0), 34.0, (0, 10.0, 158.0), P['roof'])
    A.cyl(0.8, 14.0, (0, 10.0, 192.0), P['iron'], verts=6)
    A.box((0.3, 7.0, 4.0), (0, 10.0, 203.0), P['cloth'], bev=0)
    for sg in (-1, 1):
        round_tower(A, rnd, 8.0, 80.0, FK, sg * 30.0, -6.0, 96.0, top='cone', slits=4, bands=4, roof_k=1.6, verts=20, flag=True)
    for i in range(18):                                                                          # switchback stair between terraces
        A.box((14.0, 3.0, 2.6 * (i + 1) * 0.3), (-70.0 + (i % 6) * 0.0 + 58.0 * (i // 6 % 2) * 0.0, -118.0 + i * 3.2, 1.3 * (i + 1) * 0.3), P['rock2'], bev=0.1)
    A.box((26.0, 40.0, 22.0), (0, -112.0, 11.0), P['dark'])                                    # gate mass with an opening (portcullis slot)
    A.box((12.0, 40.2, 14.0), (0, -112.0, 7.0), P['shadow'], bev=0)
    return _fin(A, 'frost_fortress_hero')


# ------------------------------------------------------------------ LM22 colossal multi-fall cliff
def colossal_falls():
    reset()
    A = Acc()
    rnd = random.Random(1002)
    keys = [P['rock'], P['dark'], P['rock2'], P['bark']]
    G.cliff(A, rnd, 240.0, 90.0, 260.0, keys, 0, 25.0, 0, 16, P['moss'], True)
    for sg in (-1, 1):
        G.cliff(A, rnd, 40.0, 70.0, 200.0, keys, sg * 110.0, -15.0, 0, 5, P['moss'], True, 0.1)  # gorge walls
    for i, (cx, wd, ztop, zbot) in enumerate(((-60.0, 26.0, 250.0, 175.0), (30.0, 34.0, 205.0, 110.0), (-10.0, 30.0, 150.0, 30.0))):
        A.box((wd, 3.4, ztop - zbot + 2.0), (cx, -22.0 - i * 3.0, (ztop + zbot) / 2.0), P['water'], bev=0)
        A.box((wd * 0.62, 0.8, ztop - zbot), (cx, -24.2 - i * 3.0, (ztop + zbot) / 2.0 - 0.6), P['foam'], bev=0)
        A.box((wd + 10.0, 24.0, 4.0), (cx, -34.0 - i * 3.0, zbot - 0.8), P['rock2'], bev=0.3)
        A.box((wd + 6.0, 20.0, 1.2), (cx, -34.0 - i * 3.0, zbot + 1.4), P['water'], bev=0)
        for k in range(9):
            A.ball(rnd.uniform(1.4, 3.4), (cx + rnd.uniform(-wd / 2, wd / 2), -40.0 - i * 3.0 + rnd.uniform(-5, 5), zbot + 2.2), P['foam'], segs=7, rings=4, scale=(1.5, 1.2, 0.5))
    A.box((120.0, 50.0, 1.4), (-10.0, -56.0, 0.7), P['water'], bev=0)
    for k in range(26):
        A.chunk((rnd.uniform(4, 9), rnd.uniform(4, 8), rnd.uniform(2, 5)), (rnd.uniform(-70, 70), rnd.uniform(-78, -40), 1.8), keys[k % 4], (0, 0, rnd.uniform(0, 90)), 0.14, rnd)
    for k in range(22):
        G.tree(A, rnd, rnd.uniform(18, 30), rnd.uniform(6, 9), TKD, rnd.choice(('oak', 'conifer')), rnd.uniform(-110, 110), rnd.uniform(18, 62), rnd.choice((255.0, 262.0)) if False else rnd.uniform(246, 262))
    return _fin(A, 'colossal_falls')


# ------------------------------------------------------------------ LM25 ancient gate, LM30 ruined castle
def ancient_gate():
    reset()
    A = Acc()
    rnd = random.Random(1003)
    for sg in (-1, 1):                                                                         # two massive pylons, one broken
        h = 58.0 if sg < 0 else 34.0
        A.frustum((24.0, 24.0), (19.0, 19.0), h, (sg * 28.0, 0, 0), P['sand2'])
        for k in range(5):
            A.box((25.0 - k * 0.6, 25.0 - k * 0.6, 0.8), (sg * 28.0, 0, 4.0 + k * (h - 6.0) / 5.0), P['sandl'], bev=0.1)
        for k in range(3):                                                                      # carved panels
            A.box((12.0, 0.5, 9.0), (sg * 28.0, -11.2 + 0.0, 12.0 + k * 13.0 if h > 50 else 12.0 + k * 8.0), P['red'], bev=0.05)
        if sg > 0:
            for k in range(12):
                A.chunk((rnd.uniform(3, 7), rnd.uniform(3, 7), rnd.uniform(1.5, 4)), (sg * 28.0 + rnd.uniform(-12, 12), rnd.uniform(-14, 4), rnd.uniform(34, 40)), P['sand2'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    A.box((46.0, 10.0, 6.0), (-8.0, 0, 54.0), P['sand'], (0, 0, 0), bev=0.2)                  # broken lintel hanging from the tall pylon
    A.box((22.0, 9.0, 5.0), (14.0, -2.0, 7.0), P['sand'], (0, 8, 6), bev=0.2)                   # the other half fell
    for k in range(18):
        A.chunk((rnd.uniform(2, 6), rnd.uniform(2, 6), rnd.uniform(1.5, 3.5)), (rnd.uniform(-34, 34), rnd.uniform(-16, 10), 1.0), P['sand2'] if k % 2 else P['rock2'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for sg in (-1, 1):
        for k in range(3):
            column(A, sg * 10.0, -6.0 + k * 6.0, 0, 1.1, 14.0 - k * 3.0, RK, 0.2 + 0.4 * k, rnd)
    for k in range(10):
        A.ball(rnd.uniform(1.4, 2.4), (rnd.uniform(-38, 38), rnd.uniform(-14, 10), 1.0), P['moss'], segs=7, rings=4, scale=(1.3, 1.2, 0.5))
    return _fin(A, 'ancient_gate')


def ruined_castle():
    reset()
    A = Acc()
    rnd = random.Random(1004)
    A.chunk((130.0, 110.0, 4.0), (0, 0, 2.0), P['rock2'], jit=0.03, rnd=rnd)
    for k in range(7):                                                                          # broken curtain wall segments around the court
        for sg in (-1, 1):
            h_ = rnd.uniform(6.0, 16.0)
            A.chunk((18.0, 7.0, h_), (-54.0 + k * 18.0, sg * 52.0, 4.0 + h_ / 2), P['rock2'], (0, 0, 0), 0.1, rnd, (0.96, 0.9))
            A.chunk((7.0, 18.0, rnd.uniform(6.0, 14.0)), (sg * 62.0, -42.0 + k * 14.0, 8.0), P['rock2'], (0, 0, 0), 0.1, rnd)
    G.round_tower(A, rnd, 9.0, 44.0, CK, -56.0, -48.0, 4.0, ruin=True, slits=3, bands=3)
    G.round_tower(A, rnd, 8.0, 30.0, CK, 58.0, -46.0, 4.0, ruin=True, slits=2, bands=2)
    G.round_tower(A, rnd, 8.5, 38.0, CK, 58.0, 48.0, 4.0, ruin=True, slits=3, bands=2)
    G.round_tower(A, rnd, 7.5, 24.0, CK, -58.0, 48.0, 4.0, ruin=True, slits=2, bands=2)
    for sx, sy, w_, d_, h_ in ((0, 6.0, 40.0, 34.0, 62.0), (-20, -20, 26, 18, 30.0), (24, -22, 20, 16, 24.0)):                 # broken keep: jagged walls, missing corner
        A.frustum((w_, d_), (w_ - 3.0, d_ - 3.0), h_, (sx, sy, 4.0), P['rock2'])
        for k in range(12):
            a = rnd.uniform(0, 360)
            x, y, _ = polar(max(w_, d_) * 0.5, a)
            A.chunk((rnd.uniform(3, 8), rnd.uniform(3, 8), rnd.uniform(1.0, 7.0)), (sx + x * 0.9, sy + y * 0.8, 4.0 + h_ + rnd.uniform(-2, 2)), P['rock2'], (0, 0, a), 0.2, rnd)
        for r_ in range(3):
            for i in range(int(w_ / 8)):
                G._window(A, sx - w_ / 2.0 + 5.0 + i * 8.0, sy - d_ / 2.0, 10.0 + r_ * 16.0 if 10.0 + r_ * 16.0 < h_ - 4 else 8.0, 270, CK, 2.0, 4.0, False, P['trim'])
    A.chunk((22.0, 18.0, 28.0), (12.0, -10.0, 18.0), P['shadow'], (0, 0, 0), 0.05, rnd)       # collapsed corner hollow
    for k in range(60):
        A.chunk((rnd.uniform(1.5, 4.5), rnd.uniform(1.5, 4.5), rnd.uniform(1.0, 3.0)), (rnd.uniform(-62, 62), rnd.uniform(-58, 58), 5.0), P['rock2'] if k % 3 else P['moss'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(18):
        A.ball(rnd.uniform(2.0, 4.0), (rnd.uniform(-62, 62), rnd.uniform(-56, 56), rnd.uniform(6, 20)), P['ivy'], segs=7, rings=4, scale=(1.3, 1.2, 1.0))
    return _fin(A, 'ruined_castle')


# ------------------------------------------------------------------ LM09 buried temple, LM15 ring temple, LM18 standing stones
def desert_temple():
    reset()
    A = Acc()
    rnd = random.Random(1005)
    A.mound(0, 0, 175.0, 155.0, 52.0, 150, [P['sand'], P['sandl'], P['sand2']], rnd, 0.0, 0.25, 0.55, 0.12)   # dunes covering the base
    for i in range(5):                                                                          # stepped upper third
        w = 100.0 - i * 16.0
        A.box((w, w * 0.8, 9.0), (0, 14.0, 44.0 + i * 9.0), P['sand'] if i % 2 else P['sandl'], bev=0.4)
    A.box((26.0, 22.0, 10.0), (0, 14.0, 90.0), P['sand2'])
    A.frustum((28.0, 24.0), (4.0, 4.0), 18.0, (0, 14.0, 98.0), P['red'])
    for sg in (-1, 1):                                                                          # pylon gate showing above the sand
        A.frustum((26.0, 22.0), (22.0, 18.0), 46.0, (sg * 34.0, -52.0, 20.0), P['sand'])
        for k in range(4):
            A.box((27.0, 23.0, 0.8), (sg * 34.0, -52.0, 30.0 + k * 10.0), P['sandl'], bev=0.1)
        A.box((12.0, 0.5, 20.0), (sg * 34.0, -63.3, 44.0), P['red'], bev=0.05)
    A.box((92.0, 10.0, 8.0), (0, -52.0, 66.0 + 0.0), P['sand2'], bev=0.3)                      # lintel across the gate (post and lintel, not an arch)
    for sg in (-1, 1):
        for k in range(4):
            column(A, sg * (14.0 + k * 0.0), -40.0 + k * 11.0, 24.0 + k * 0.0, 2.0, 30.0 - k * 6.0, RK, 0.1 + 0.2 * k, rnd)
    for k in range(10):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(40, 80), a)
        A.chunk((rnd.uniform(4, 9), rnd.uniform(4, 9), rnd.uniform(3, 8)), (x, y, 24.0 + rnd.uniform(0, 12)), P['sand2'], (0, 0, a), 0.2, rnd)
    for sg in (-1, 1):
        G.spire(A, rnd, 3.4, 40.0, [P['sand'], P['sand2']], sg * 62.0, 44.0, 14.0, 6)
    return _fin(A, 'buried_desert_temple')


def ring_temple():
    reset()
    A = Acc()
    rnd = random.Random(1006)
    A.cyl(110.0, 2.0, (0, 0, 0), P['sand2'], verts=48)
    A.cyl(100.0, 1.2, (0, 0, 2.0), P['sandl'], verts=48)
    for k in range(24):                                                                          # outer ring: wall segments with broken crowns
        a = 15.0 * k
        if k % 6 == 3:
            continue
        x, y, _ = polar(100.0, a)
        h_ = rnd.uniform(10.0, 18.0) if k % 5 else rnd.uniform(4.0, 8.0)
        A.box((24.0, 5.0, h_), (x, y, 3.2 + h_ / 2), P['sand'] if k % 2 else P['sandl'], (0, 0, a + 90.0), bev=0.25)
        A.box((24.6, 5.6, 1.0), (x, y, 3.2 + h_), P['sand2'], (0, 0, a + 90.0), bev=0.1)
    for k in range(4):                                                                           # four gate piers (post and lintel)
        a = 90.0 * k + 45.0
        for sg in (-1, 1):
            x, y, _ = polar(100.0, a + sg * 4.2)
            A.frustum((7.0, 7.0), (5.6, 5.6), 28.0, (x, y, 3.2), P['sandl'], (0, 0, a))
        x, y, _ = polar(100.0, a)
        A.box((24.0, 5.5, 3.6), (x, y, 31.6), P['sand'], (0, 0, a + 90.0), bev=0.2)
    for k in range(16):                                                                          # inner colonnade
        a = 22.5 * k
        x, y, _ = polar(62.0, a)
        column(A, x, y, 3.2, 2.2, 24.0 if k % 3 else 12.0, RK, 0.0 if k % 3 else 0.6, rnd)
    A.sweep([(55.0, 26.0), (70.0, 26.0), (70.0, 28.0), (55.0, 28.0)], 0, 300, 24, P['sand2'], loc=(0, 0, 3.2))
    A.cyl(34.0, 26.0, (0, 0, 3.2), P['sand'], verts=24, r2=32.0)                                 # inner sanctum drum
    A.cyl(33.0, 4.0, (0, 0, 29.2), P['sandl'], verts=24)
    A.cyl(30.0, 14.0, (0, 0, 33.2), P['red'], verts=24, r2=0.0)
    for k in range(8):
        a = 45.0 * k + 22.5
        x, y, _ = polar(33.2, a)
        A.box((0.6, 4.4, 9.0), (x, y, 15.0), P['shadow'], (0, 0, a), bev=0)
    for k in range(4):
        a = 90.0 * k
        for i in range(10):
            x, y, _ = polar(36.0 + i * 5.4, a)
            A.box((4.8, 8.0, 0.5), (x, y, 3.7), P['sandl'], (0, 0, a), bev=0.05)
    for k in range(28):
        x, y, _ = polar(rnd.uniform(60, 108), rnd.uniform(0, 360))
        A.chunk((rnd.uniform(2, 5), rnd.uniform(2, 5), rnd.uniform(1, 3)), (x, y, 3.2), P['sand2'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    return _fin(A, 'ring_temple')


def standing_stones():
    reset()
    A = Acc()
    rnd = random.Random(1007)
    A.cyl(68.0, 1.6, (0, 0, 0), P['moss'], verts=32, r2=64.0)
    A.cyl(58.0, 0.6, (0, 0, 1.6), P['rock2'], verts=32)
    n = 14
    for k in range(n):
        a = 360.0 / n * k + rnd.uniform(-3, 3)
        x, y, _ = polar(60.0, a)
        h = rnd.uniform(26.0, 44.0)
        lean = rnd.uniform(-5.0, 5.0)
        G.spire(A, rnd, 3.5, h, [P['dark'] if k % 2 else P['rock'], P['rock']], x, y, 1.0, 5, lean=lean * 0.02)
        A.chunk((8.0, 5.6, 2.0), (x, y, 1.6), P['rock'], (0, 0, a + 90.0), 0.1, rnd)
        for r_ in range(3):                                                                      # carved bands (dark inlay, non-emissive)
            A.box((7.4, 0.5, 1.2), (x, y, 8.0 + r_ * 9.0), P['shadow'], (0, 0, a + 90.0), bev=0)
            A.box((3.0, 0.6, 3.0), (x, y, 11.5 + r_ * 9.0), P['shadow'], (0, 0, a + 90.0 + 45.0), bev=0)
        if k % 3 == 0:
            x2, y2, _ = polar(60.0, a + 360.0 / n / 2.0)
            A.chunk((20.0, 5.0, 4.0), (x2, y2, min(h, 26.0) + 2.0), P['rock'], (0, 0, a + 90.0 + 12), 0.06, rnd)
    for k in range(5):                                                                           # fallen stones
        x, y, _ = polar(rnd.uniform(30, 52), rnd.uniform(0, 360))
        A.chunk((22.0, 5.0, 5.0), (x, y, 3.5), P['rock'], (0, 0, rnd.uniform(0, 180)), 0.08, rnd)
    A.chunk((9.0, 9.0, 3.0), (0, 0, 2.5), P['dstone'], (0, 0, 0), 0.08, rnd)                     # central altar stone
    for k in range(6):
        x, y, _ = polar(rnd.uniform(66, 76), rnd.uniform(0, 360))
        A.mound(x, y, 8.0, 8.0, 5.0, 4, [P['rock'], P['moss']], rnd, 0.0, 0.4, 0.8)
    return _fin(A, 'standing_stones_ring')


# ------------------------------------------------------------------ VC02 skull cliffs
def _skull(var):
    reset()
    A = Acc()
    rnd = random.Random(1010 + var)
    keys = [P['basalt'], P['dark'], P['rock']]
    G.cliff(A, rnd, 200.0, 100.0, 120.0, keys, 0, 36.0, 0, 11, None, True)
    A.ball(46.0, (0, -10.0, 70.0), P['bone'], segs=24, rings=16, scale=(1.18, 0.82, 1.0))      # cranium
    A.ball(34.0, (0, -22.0, 36.0), P['bone'], segs=18, rings=12, scale=(1.0, 0.8, 0.8))        # face block
    for sx in (-1, 1):
        A.ball(13.0, (sx * 22.0, -45.0, 72.0), P['shadow'], segs=14, rings=10, scale=(1.0, 0.5, 1.15))     # eye sockets
        A.ball(15.5, (sx * 22.0, -43.0, 72.0), P['dstone'], segs=12, rings=8, scale=(1.0, 0.4, 1.1))
        A.box((14.0, 6.0, 4.0), (sx * 22.0, -46.0, 87.0), P['bone'], (0, 0, sx * 12.0), bev=0.3)          # brow
    A.prism([(-6.0, 0), (6.0, 0), (0, 16.0)], 6.0, (0, -44.0, 42.0), P['shadow'], (90, 0, 0))             # nose hollow
    A.box((52.0, 8.0, 5.0), (0, -50.0, 22.0), P['bone'], bev=0.3)                                          # upper teeth row base
    for k in range(10):
        A.box((4.2, 5.0, 8.0 if k % 2 == 0 else 6.5), (-22.0 + k * 4.9, -53.0, 17.0), P['bone'], bev=0.25)
    for k in range(10):
        A.box((4.2, 5.0, 7.0 if k % 2 == 0 else 5.5), (-22.0 + k * 4.9, -53.0, 7.0), P['bone'], bev=0.25)
    A.box((50.0, 4.0, 12.0), (0, -52.0, 12.0), P['shadow'], bev=0)                                         # open mouth (cave entrance)
    A.box((60.0, 10.0, 6.0), (0, -48.0, 1.5), P['bone'], bev=0.3)                                          # lower jaw
    if var == 2:
        for sx in (-1, 1):                                                                                  # horn spires and a terrace stair
            for k in range(5):
                A.chunk((12.0 - k * 2.0, 12.0 - k * 2.0, 14.0), (sx * (44.0 + k * 4.0), -6.0, 98.0 + k * 11.0), P['bone'], (0, 0, 0), 0.1, rnd, (0.78, 0.78))
        for i in range(12):
            A.box((30.0 - i, 4.0, 1.4 * (i + 1)), (0, -62.0 - i * 3.6, 0.7 * (i + 1)), P['dark'], bev=0.1)
        for sx in (-1, 1):
            A.cyl(2.0, 30.0, (sx * 22.0, -66.0, 0), P['dark'], verts=8, r2=1.4)
            A.cyl(3.2, 3.0, (sx * 22.0, -66.0, 30.0), P['iron'], verts=8, r2=4.0)
    return _fin(A, 'skull_cliff')


def skull_1():
    return _skull(1)


def skull_2():
    return _skull(2)


# ------------------------------------------------------------------ VG01-VG03 trees
def _tree(kind, h, crown, K, seed, lean=0.0):
    reset()
    A = Acc()
    rnd = random.Random(seed)
    G.tree(A, rnd, h, crown, K, kind, 0, 0, 0, lean)
    return _fin(A, 'tree_' + kind)


TREE_ROWS = [
    ('VG01_01_poplar_beech_01', 'poplar', 46.0, 5.6, TKP, 2001, 0.0), ('VG01_02_poplar_beech_02', 'poplar', 44.0, 5.0, TKP, 2002, 0.6),
    ('VG01_03_poplar_beech_03', 'beech', 42.0, 6.2, TK, 2003, 0.0), ('VG02_01_dark_old_oak_01', 'broken', 40.0, 13.0, TKD, 2004, 0.0),
    ('VG02_02_dark_old_oak_02', 'broken', 38.0, 12.0, TKD, 2005, 1.0), ('VG03_01_flowering_tree_01', 'cherry', 30.0, 9.0, TK, 2006, 0.0),
    ('VG03_02_flowering_tree_02', 'cherry', 28.0, 9.5, TK, 2007, 0.0)]


def _mk_tree(i):
    mid, kind, h, c, K, seed, lean = TREE_ROWS[i]
    return lambda: _tree(kind, h, c, K, seed, lean)


# ------------------------------------------------------------------ CO01 coast cliffs, CO02 sea stacks
def _coast(var):
    reset()
    A = Acc()
    rnd = random.Random(1100 + var)
    keys = [P['rock'], P['rock2'], P['dark']]
    if var == 1:                                                                                # straight cliff face
        G.cliff(A, rnd, 108.0, 40.0, 68.0, keys, 0, 8.0, 0, 11, P['moss'], True)
    elif var == 2:                                                                              # curved bay (two cliffs angled in)
        G.cliff(A, rnd, 60.0, 36.0, 66.0, keys, -22.0, 10.0, 0, 6, P['moss'], True, 0.1)
        G.cliff(A, rnd, 50.0, 36.0, 54.0, keys, 36.0, 4.0, 0, 5, P['moss'], True, 0.1)
    elif var == 3:                                                                              # cliff with a sea cave
        G.cliff(A, rnd, 108.0, 40.0, 64.0, keys, 0, 8.0, 0, 11, P['moss'], True)
        A.box((20.0, 24.0, 20.0), (0, -9.0, 10.0), P['shadow'], bev=0)
    elif var == 4:                                                                              # stepped terraces
        for i in range(3):
            G.cliff(A, rnd, 108.0 - i * 24.0, 22.0, 22.0 + i * 20.0, keys, 0, 14.0 - i * 5.0, 0, 8 - i, P['moss'] if i == 2 else None, True)
    elif var == 5:                                                                              # cliff with a waterfall trickle
        G.cliff(A, rnd, 108.0, 40.0, 70.0, keys, 0, 8.0, 0, 11, P['moss'], True)
        A.box((7.0, 1.6, 66.0), (-14.0, -13.2, 36.0), P['water'], bev=0)
        A.box((4.0, 0.5, 62.0), (-14.0, -14.2, 34.0), P['foam'], bev=0)
        A.box((16.0, 10.0, 1.0), (-14.0, -20.0, 2.0), P['water'], bev=0)
    else:                                                                                       # headland with talus slope
        G.cliff(A, rnd, 90.0, 40.0, 60.0, keys, 12.0, 8.0, 0, 9, P['moss'], True, -0.2)
        A.mound(-30.0, -10.0, 40.0, 30.0, 26.0, 18, keys, rnd, 0.0, 0.35, 0.7)
    for k in range(14):                                                                         # beach shingle and boulders at the foot
        A.chunk((rnd.uniform(2, 6), rnd.uniform(2, 5), rnd.uniform(1.5, 3.5)), (rnd.uniform(-52, 52), rnd.uniform(-22, -8), 1.2), keys[k % 3], (0, 0, rnd.uniform(0, 90)), 0.18, rnd)
    return _fin(A, 'coast_cliff')


def _mk_coast(i):
    return lambda: _coast(i + 1)


def _stack(var):
    reset()
    A = Acc()
    rnd = random.Random(1200 + var)
    keys = [P['rock'], P['dark'], P['rock2']]
    A.mound(0, 0, 40.0, 40.0, 20.0, 34, keys, rnd, 0.0, 0.4, 0.9)
    zt = G.spire(A, rnd, 11.0 - var, 78.0, keys, 0, 0, 8.0, 16, lean=(var - 2) * 0.05, cap=P['moss'])
    for k in range(16):                                                                          # side buttress chunks and ledges up the stack
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(5.0, 8.0), a)
        A.chunk((rnd.uniform(4, 8), rnd.uniform(4, 8), rnd.uniform(5, 11)), (x, y, rnd.uniform(10, 62)), keys[k % 3], (0, 0, a), 0.14, rnd, (0.8, 0.8))
    if var == 2:
        A.box((10.0, 8.0, 3.0), (6.0, -4.0, 56.0), P['rock2'], (0, 0, 0), bev=0.3)
        G.spire(A, rnd, 5.5, 34.0, keys, 12.0, 4.0, 6.0, 5)
    if var == 3:
        G.rock_arch(A, rnd, 18.0, 22.0, 4.0, keys, -10.0, -6.0, 0.0, 8.0, 9)
    for k in range(8):
        A.ball(rnd.uniform(0.8, 1.5), (rnd.uniform(-14, 14), rnd.uniform(-14, 14), rnd.uniform(20, 70)), P['foam'], segs=6, rings=4, scale=(1.4, 1.2, 0.5)) if False else None
    return _fin(A, 'sea_stack')


def _mk_stack(i):
    return lambda: _stack(i + 1)


BATCHES = {
    'heroes_a': ('v5_landmarks', mk(list(zip(v5kit.ids('LM03', 'LM22', 'LM25', 'LM30'), [fortress, colossal_falls, ancient_gate, ruined_castle])), 0.1)),
    'heroes_b': ('v5_landmarks', mk(list(zip(v5kit.ids('LM09', 'LM15', 'LM18'), [desert_temple, ring_temple, standing_stones])), 0.1)),
    'skull': ('v5_skull', mk(list(zip(v5kit.ids('VC02'), [skull_1, skull_2])), 0.1)),
    'trees': ('v5_forest', mk([(mid, _mk_tree(i)) for i, mid in enumerate(v5kit.ids('VG01', 'VG02', 'VG03'))], 0.1)),
    'coast': ('v5_coast', mk([(mid, _mk_coast(i)) for i, mid in enumerate(v5kit.ids('CO01'))] + [
        (mid, _mk_stack(i)) for i, mid in enumerate(v5kit.ids('CO02'))], 0.1)),
}
