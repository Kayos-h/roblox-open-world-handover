"""vg module - highlands, forest and marsh extras: HL01 ice spires, HL02 ice arches, HL03 glacier tongues, HL04 ice caves, HL05 shrine, HL06 watchtower,
HL07 mine mouths, SP01 snow spires, LM04-LM08 fortress parts, FR01 giant trees, FR02 forest ruins, FR03 cave mouths, VG04 birch, LM23 gorge walls,
LM24 pool rocks, VG05 swamp cypress, VG06 hummocks, VG07 boardwalks. Original designs, no glow, front faces -Y.
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v5kit
from v5kit import Acc, polar, tang, mk, ids
import v5gen as G
from v5gen import round_tower, wall_seg, house, column, cliff, spire, rock_arch, tree
import v4util

P = G.reg('vg', {
    'rock': ((128, 124, 120), 'Slate', 0.0, 0.95), 'rock2': ((150, 146, 140), 'Cobblestone', 0.0, 0.95), 'dark': ((72, 72, 80), 'Granite', 0.0, 0.92),
    'snow': ((240, 244, 250), 'Snow', 0.0, 0.7), 'ice': ((196, 226, 242), 'Ice', 0.0, 0.3), 'ice2': ((160, 206, 232), 'Ice', 0.0, 0.28),
    'iceW': ((226, 240, 248), 'Ice', 0.0, 0.35), 'wall': ((172, 166, 172), 'Limestone', 0.0, 0.9), 'trim': ((214, 208, 210), 'Limestone', 0.0, 0.88),
    'roof': ((74, 94, 128), 'Slate', 0.0, 0.8), 'timber': ((112, 92, 70), 'Wood', 0.0, 0.9), 'plank': ((134, 108, 80), 'WoodPlanks', 0.0, 0.9),
    'moss': ((92, 124, 72), 'Grass', 0.0, 1.0), 'ivy': ((66, 102, 58), 'Grass', 0.0, 1.0), 'stoneM': ((140, 138, 126), 'Limestone', 0.0, 0.92),
    'shadow': ((26, 24, 30), 'Slate', 0.0, 0.95), 'iron': ((58, 58, 64), 'Metal', 0.6, 0.6), 'gold': ((196, 160, 84), 'Metal', 0.8, 0.35),
    'water': ((70, 110, 120), 'SmoothPlastic', 0.0, 0.2), 'foam': ((236, 244, 248), 'SmoothPlastic', 0.0, 0.5), 'bark': ((96, 74, 56), 'Wood', 0.0, 0.95),
    'barkW': ((226, 222, 212), 'Wood', 0.0, 0.95), 'leaf': ((70, 120, 60), 'Grass', 0.0, 1.0), 'leaf2': ((104, 150, 80), 'Grass', 0.0, 1.0),
    'leafd': ((50, 84, 48), 'Grass', 0.0, 1.0), 'leafy': ((176, 170, 70), 'Grass', 0.0, 1.0), 'bloom': ((236, 176, 196), 'Grass', 0.0, 1.0),
    'cloth': ((168, 52, 52), 'Fabric', 0.0, 1.0), 'glass': ((86, 104, 128), 'SmoothPlastic', 0.0, 0.3), 'rope': ((176, 150, 104), 'Fabric', 0.0, 1.0),
    'mud': ((84, 74, 58), 'Mud', 0.0, 1.0), 'reed': ((150, 140, 80), 'Grass', 0.0, 1.0), 'sand': ((214, 184, 140), 'Sandstone', 0.0, 0.95),
})
FK = {'stone': P['rock2'], 'wall': P['wall'], 'trim': P['trim'], 'dark': P['shadow'], 'door': P['timber'], 'deck': P['timber'], 'roof': P['roof'], 'roof2': P['rock'],
      'gold': P['gold'], 'timber': P['timber'], 'flag': P['cloth'], 'cap': P['snow'], 'glass': P['glass'], 'shutter': P['timber'], 'iron': P['iron'], 'sign': P['timber']}
ROCK = [P['rock'], P['rock2'], P['dark']]
ICE = [P['ice'], P['ice2'], P['iceW']]
TKS = {'bark': P['bark'], 'leaf': P['leaf'], 'leaf2': P['leaf2'], 'bloom': P['bloom']}
TKD = {'bark': P['bark'], 'leaf': P['leafd'], 'leaf2': P['leaf'], 'bloom': P['leaf']}
TKB = {'bark': P['barkW'], 'leaf': P['leafy'], 'leaf2': P['leaf2'], 'bloom': P['leaf']}
TKC = {'bark': P['mud'], 'leaf': P['leafd'], 'leaf2': P['moss'], 'bloom': P['leaf']}


def _fin(A, name):
    A.to_scene()
    return finalize(name, 28)


def _snowcap(A, rnd, z, r, n=6, w=None):
    for k in range(n):
        x, y, _ = polar(r * rnd.uniform(0.0, 0.55), rnd.uniform(0, 360))
        A.chunk(((w or r) * rnd.uniform(0.7, 1.1), (w or r) * rnd.uniform(0.7, 1.1), rnd.uniform(1.0, 2.2)), (x, y, z + rnd.uniform(-0.4, 0.6)), P['snow'], (0, 0, rnd.uniform(0, 90)), 0.12, rnd)


# ------------------------------------------------------------------ HL highlands
def _ice_spire(i):
    reset()
    A = Acc()
    rnd = random.Random(3000 + i)
    A.mound(0, 0, 24.0, 24.0, 10.0, 10, ICE[:2] + [P['snow']], rnd, 0.0, 0.5, 0.9)
    G.spire(A, rnd, 9.0 - i * 0.6, 62.0 + i * 3, ICE, 0, 0, 5.0, 9, lean=0.05 * (i - 1.5), cap=P['iceW'])
    for k in range(4 + i):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(4, 7), a)
        G.spire(A, rnd, rnd.uniform(2.5, 4.5), rnd.uniform(18, 36), ICE, x, y, 4.0, 5, lean=rnd.uniform(-0.1, 0.1))
    return _fin(A, 'ice_spire')


def _ice_arch(i):
    reset()
    A = Acc()
    rnd = random.Random(3100 + i)
    G.rock_arch(A, rnd, 30.0 + i * 4.0, 32.0, 6.0, ICE, 0, 0, 0, 12.0, 13, P['snow'])
    A.mound(0, 0, 50.0, 14.0, 6.0, 12, [P['snow'], P['ice']], rnd, 0.0, 0.3, 0.6)
    for k in range(12):
        x = rnd.uniform(-14, 14)
        A.cyl(0.25, rnd.uniform(1.0, 2.6), (x, rnd.uniform(-2, 2), 24.0 - abs(x) * 0.5), P['iceW'], verts=5, r2=0.0, rot=(180, 0, 0))
    return _fin(A, 'ice_arch')


def _glacier(i):
    reset()
    A = Acc()
    rnd = random.Random(3200 + i)
    for k in range(9):
        x = -38.0 + k * 9.5
        L = 44.0 - abs(x) * 0.25
        A.chunk((10.5, L, rnd.uniform(3.0, 5.5)), (x, -8.0 + (L - 40) * 0.0, 2.2 + rnd.uniform(0, 1.2)), ICE[k % 3], (0, 0, rnd.uniform(-6, 6)), 0.1, rnd, (0.9, 0.8))
        for j in range(3):
            A.chunk((rnd.uniform(3, 6), rnd.uniform(3, 8), rnd.uniform(2.5, 7.0)), (x + rnd.uniform(-3, 3), rnd.uniform(-22, 14), 4.0), ICE[(k + j) % 3], (0, 0, rnd.uniform(0, 90)), 0.16, rnd, (0.7, 0.7))
    for k in range(5 + i):                                                                       # crevasses: dark slots
        A.box((rnd.uniform(1.2, 2.0), rnd.uniform(10, 20), 0.4), (rnd.uniform(-36, 36), rnd.uniform(-10, 10), 5.4), P['shadow'], (0, 0, rnd.uniform(-20, 20)), bev=0)
    for sg in (-1, 1):
        A.mound(sg * 40.0, 16.0, 20.0, 20.0, 12.0, 8, ROCK, rnd, 0.0, 0.5, 0.9)
    _snowcap(A, rnd, 6.0, 30.0, 8, 12.0)
    return _fin(A, 'glacier_tongue')


def _ice_cave(i):
    reset()
    A = Acc()
    rnd = random.Random(3300 + i)
    for sg in (-1, 1):
        for k in range(6):
            A.chunk((7.5, 24.0, 5.5), (sg * 11.0 + rnd.uniform(-0.6, 0.6), 0, 2.6 + k * 4.4), ICE[(k + (sg > 0)) % 3], (0, 0, 0), 0.1, rnd, (0.94, 0.94))
    for k in range(5):
        A.chunk((9.0, 24.0, 5.0), (-12.0 + k * 6.0, 0, 22.0 + rnd.uniform(0, 1.0)), ICE[k % 3], (0, 0, 0), 0.08, rnd)
    A.box((10.0, 24.0, 0.4), (0, 0, 0.2), P['ice2'], bev=0)
    A.box((9.0, 20.0, 15.0), (0, 2.2, 7.5), P['shadow'], bev=0)
    for k in range(10):
        x = -4.0 + k * 0.9
        A.cyl(0.3, rnd.uniform(1.5, 4.0), (x, -11.0, 20.0), P['iceW'], verts=5, r2=0.0, rot=(180, 0, 0))
    A.mound(0, 0, 36.0, 24.0, 10.0, 10, [P['snow'], P['ice']], rnd, 17.0, 0.3, 0.6)
    for k in range(6):
        A.ball(rnd.uniform(0.9, 1.6), (rnd.choice((-1, 1)) * rnd.uniform(5, 14), rnd.uniform(-12, -6), 0.8), P['snow'], segs=7, rings=4, scale=(1.4, 1.2, 0.5))
    return _fin(A, 'ice_cave')


def hidden_shrine():
    reset()
    A = Acc()
    rnd = random.Random(3400)
    A.mound(0, 0, 26.0, 26.0, 7.0, 10, ROCK, rnd, 0.0, 0.45, 0.8)
    A.box((12.0, 10.0, 7.0), (0, 0, 10.5), P['stoneM'])
    A.gable(14.0, 12.0, 4.0, (0, 0, 14.0), P['roof'], (0, 0, 90))
    A.box((3.0, 0.5, 4.5), (0, -5.2, 10.0), P['shadow'], bev=0)
    A.box((1.8, 1.8, 1.4), (0, -3.0, 8.6), P['trim'], bev=0.1)
    A.ball(0.9, (0, -3.0, 9.8), P['gold'], segs=8, rings=5)
    for sg in (-1, 1):
        A.cyl(0.18, 9.0, (sg * 8.0, -6.0, 7.0), P['timber'], verts=6)
        for k in range(4):
            A.box((1.2, 0.05, 1.5), (sg * 8.0 + 0.7, -6.0, 15.0 - k * 1.2), (P['cloth'], P['snow'], P['ice2'], P['leaf'])[k], bev=0)
    for i in range(5):
        A.box((6.0 - i * 0.4, 2.0, 0.6 * (i + 1)), (0, -8.0 - i * 1.8 + 3.0, 7.0 + 0.3 * (i + 1) - 1.0), P['rock2'], bev=0.1)
    _snowcap(A, rnd, 17.5, 8.0, 5, 6.0)
    return _fin(A, 'hidden_shrine')


def mountain_watchtower():
    reset()
    A = Acc()
    rnd = random.Random(3500)
    A.mound(0, 0, 18.0, 18.0, 6.0, 8, ROCK, rnd, 0.0, 0.45, 0.8)
    G.round_tower(A, rnd, 6.0, 40.0, FK, 0, 0, 5.0, top='crenel', slits=3, bands=3, door=True, verts=18)
    A.cyl(7.0, 3.0, (0, 0, 44.0), P['timber'], verts=18, r2=8.0)
    A.cyl(8.2, 8.0, (0, 0, 47.0), P['roof'], verts=18, r2=0.0)
    for sg in (-1, 1):
        A.beam((sg * 6.0, 0, 38.0), (sg * 9.0, 0, 38.6), 0.3, 0.3, P['iron'])
    _snowcap(A, rnd, 6.5, 9.0, 4, 6.0)
    for k in range(6):
        A.box((0.4, 0.4, 1.6), (-4.0 + k * 1.6, -8.0, 6.0), P['timber'], bev=0)
    return _fin(A, 'mountain_watchtower')


def _mine(i):
    reset()
    A = Acc()
    rnd = random.Random(3600 + i)
    for sg in (-1, 1):
        for k in range(4):
            A.chunk((8.0, 22.0, 5.0), (sg * 11.0, 0, 2.5 + k * 4.5), ROCK[(k + i) % 3], (0, 0, 0), 0.1, rnd, (0.94, 0.94))
    for k in range(4):
        A.chunk((8.0, 22.0, 5.0), (-10.5 + k * 7.0, 0, 18.0), ROCK[k % 3], (0, 0, 0), 0.1, rnd)
    A.box((9.0, 22.0, 13.0), (0, 2.0, 6.5), P['shadow'], bev=0)
    for sg in (-1, 1):
        A.box((1.2, 1.2, 13.4), (sg * 5.0, -10.0, 6.7), P['timber'], bev=0.08)
        A.beam((sg * 5.0, -10.2, 10.0), (sg * 2.0, -10.2, 13.0), 0.5, 0.5, P['timber'])
    A.box((12.0, 1.4, 1.4), (0, -10.0, 13.4), P['timber'], bev=0.08)
    for k in range(18):                                                                          # rails and sleepers
        A.box((7.0, 0.5, 0.2), (0, -10.0 + k * 1.2, 0.2), P['timber'], bev=0)
    for sg in (-1, 1):
        A.box((0.2, 22.0, 0.3), (sg * 2.2, 1.0, 0.5), P['iron'], bev=0)
    if i == 1:
        A.box((4.0, 3.0, 2.0), (-4.5, -15.0, 1.4), P['plank'], bev=0.08)
        A.cyl(1.0, 0.6, (-5.6, -13.4, 0.9), P['iron'], verts=10, rot=(0, 90, 0))
        for k in range(5):
            A.chunk((1.4, 1.4, 1.0), (-4.5 + k * 0.4, -15.0, 2.6), P['dark'], (0, 0, 0), 0.2, rnd)
    A.beam((4.0, -10.4, 11.5), (4.0, -11.4, 11.5), 0.15, 0.15, P['iron'])
    A.cyl(0.5, 0.9, (4.0, -11.4, 10.6), P['gold'], verts=8)
    return _fin(A, 'mine_mouth')


def _snow_spire(i):
    reset()
    A = Acc()
    rnd = random.Random(3700 + i)
    A.mound(0, 0, 54.0, 54.0, 26.0, 24, [P['rock'], P['dark'], P['snow']], rnd, 0.0, 0.4, 0.9)
    G.spire(A, rnd, 15.0, 156.0, [P['rock'], P['dark'], P['rock2'], P['snow']], 0, 0, 14.0, 14, lean=0.05 * (i % 3 - 1), cap=P['snow'])
    for k in range(5):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(8, 14), a)
        G.spire(A, rnd, rnd.uniform(5, 9), rnd.uniform(60, 110), [P['rock'], P['dark'], P['snow']], x, y, 10.0, 8, lean=rnd.uniform(-0.1, 0.1), cap=P['snow'])
    _snowcap(A, rnd, 40.0, 24.0, 12, 10.0)
    return _fin(A, 'snow_spire')


# ------------------------------------------------------------------ LM04-LM08 fortress parts
def _rampart(i):
    reset()
    A = Acc()
    rnd = random.Random(3800 + i)
    steps = 3
    for s in range(steps):
        x0 = -20.0 + s * 20.0
        z = s * 5.5
        A.box((20.0, 12.0, z + 4.0), (x0, 0, (z + 4.0) / 2.0), P['rock2'], bev=0.2)
        wall_seg(A, rnd, 20.0, 12.0 - 2.0, 8.0, FK, x0, 0, z + 4.0, 6.0, (s + i) % 2 == 0, False)
    for sg in (-1, 1):
        round_tower(A, rnd, 4.2 + i * 0.4, 22.0 + i * 3.0, FK, sg * 28.0, 0, sg * 0 + (0 if sg < 0 else 11.0), top='cone', slits=2, bands=2, roof_k=1.4, verts=14)
    return _fin(A, 'stepped_rampart')


def _cliff_tower(i):
    reset()
    A = Acc()
    rnd = random.Random(3900 + i)
    A.mound(0, 8.0, 34.0, 20.0, 40.0, 22, ROCK, rnd, 0.0, 0.4, 0.8)
    if i == 0:
        round_tower(A, rnd, 7.5, 58.0, FK, 0, -2.0, 6.0, top='cone', slits=4, bands=4, roof_k=1.4, verts=18, flag=True)
    else:
        A.frustum((15.0, 15.0), (13.0, 13.0), 54.0, (0, -2.0, 6.0), P['wall'])
        for r_ in range(4):
            G._window(A, 0, -9.5, 18.0 + r_ * 11.0, 270, FK, 1.6, 3.2, False, P['trim'])
        A.frustum((18.0, 18.0), (2.0, 2.0), 22.0, (0, -2.0, 60.0), P['roof'])
        A.box((20.0, 2.0, 0.8), (0, -10.0, 40.0), P['timber'])
        for k in range(5):
            A.box((0.3, 0.3, 1.4), (-8.0 + k * 4.0, -11.0, 41.0), P['timber'], bev=0)
    _snowcap(A, rnd, 36.0, 12.0, 4, 8.0)
    return _fin(A, 'cliff_tower')


def gate_tunnel():
    reset()
    A = Acc()
    rnd = random.Random(4000)
    W, D, H = 60.0, 60.0, 50.0
    G.cliff(A, rnd, W, D, H, ROCK, 0, 0, 0, 8, P['snow'], True)
    A.box((16.0, D + 1.0, 18.0), (0, 0, 9.0), P['shadow'], bev=0)
    for sg in (-1, 1):
        A.box((2.4, 2.4, 19.0), (sg * 9.2, -D / 2.0 - 0.4, 9.5), P['timber'], bev=0.1)
        A.beam((sg * 9.2, -D / 2.0 - 0.6, 14.0), (sg * 5.0, -D / 2.0 - 0.6, 18.0), 0.9, 0.9, P['timber'])
        A.cyl(1.8, 24.0, (sg * 15.0, -D / 2.0 - 2.0, 0), P['wall'], verts=8, r2=1.4)
        A.ball(2.2, (sg * 15.0, -D / 2.0 - 2.0, 24.5), P['gold'], segs=8, rings=5)
    A.box((22.0, 2.4, 2.4), (0, -D / 2.0 - 0.4, 18.6), P['timber'], bev=0.1)
    A.box((18.0, 3.0, 4.0), (0, -D / 2.0 - 0.8, 24.0), P['wall'], bev=0.1)
    for k in range(7):
        A.box((18.0 - k, 2.0, 0.5 * (k + 1)), (0, -D / 2.0 - 4.0 - k * 1.6, 0.25 * (k + 1)), P['rock2'], bev=0.08)
    return _fin(A, 'gate_tunnel')


def _switch_stairs(i):
    reset()
    A = Acc()
    rnd = random.Random(4100 + i)
    n = 30
    z = 0.0
    x, y = -18.0, -22.0
    d = 1
    A.mound(0, 0, 60.0, 60.0, 62.0, 60, ROCK, rnd, 0.0, 0.3, 0.6)
    for s in range(n):
        A.box((8.0, 1.8, 2.0), (x, y, z + 1.0 + 20.0 * 0), P['rock2'], bev=0.08)
        if s % 10 == 9:
            d = -d
            y += 0.0
            A.box((10.0, 12.0, 2.0), (x, y + 3.0, z + 1.0), P['stoneM'], bev=0.1)
        x += d * 1.8
        z += 1.8
        if s % 10 == 9:
            y += 8.0
    for sg in (-1, 1):
        A.box((0.6, 40.0, 3.0), (sg * 20.0, 0, 12.0 + 0.0), P['rock'], (0, 0, 0), bev=0) if False else None
    return _fin(A, 'switchback_stairs')


def stone_span():
    reset()
    A = Acc()
    rnd = random.Random(4200)
    for sg in (-1, 1):
        A.mound(sg * 38.0, 0, 26.0, 18.0, 18.0, 14, ROCK, rnd, 0.0, 0.45, 0.85)
        A.box((10.0, 12.0, 2.0), (sg * 36.0, 0, 18.5), P['stoneM'], bev=0.2)
    n = 18
    for k in range(n):
        t = k / (n - 1.0)
        x = -34.0 + 68.0 * t
        z = 17.0 + math.sin(math.pi * t) * 3.0
        A.box((4.2, 9.0, 2.2 - 0.9 * math.sin(math.pi * t)), (x, 0, z), P['rock2'], (0, -math.degrees(math.cos(math.pi * t) * 0.14), 0), bev=0.15)
    for sg in (-1, 1):
        for k in range(9):
            t = k / 8.0
            A.box((1.2, 1.2, 1.6), (-34.0 + 68.0 * t, sg * 4.6, 20.0 + math.sin(math.pi * t) * 3.0), P['trim'], bev=0.1)
    for k in range(4):
        A.chunk((5.0 - k * 0.6, 8.0, 12.0 + k * 0.0), (-8.0 + k * 5.5, 0, 11.0 - abs(k - 1.5) * 2.5), ROCK[k % 3], (0, 0, 0), 0.1, rnd, (0.8, 0.9))
    v4util.marker('mk_enda', (-36.0, 0, 19.0))
    v4util.marker('mk_endb', (36.0, 0, 19.0))
    v4util.marker('mk_deck', (0, 0, 19.6))
    return _fin(A, 'stone_span')


# ------------------------------------------------------------------ FR forest
def _giant_tree(i):
    reset()
    A = Acc()
    rnd = random.Random(4300 + i)
    if i == 0:                                                                                   # leaning
        G.tree(A, rnd, 160.0, 38.0, TKD, 'oak', 0, 0, 0, 22.0)
        G.tree(A, rnd, 70.0, 20.0, TKD, 'oak', 26.0, -10.0, 0)
    elif i == 1:                                                                                 # twin trunk
        G.tree(A, rnd, 160.0, 30.0, TKD, 'oak', -12.0, 0, 0, -4.0)
        G.tree(A, rnd, 140.0, 28.0, TKS, 'oak', 14.0, 4.0, 0, 6.0)
        A.cyl(18.0, 18.0, (0, 2.0, 0), P['bark'], verts=14, r2=7.0)
    elif i == 2:                                                                                 # arched trunk
        prev = (-30.0, 0, 0.0)
        for s in range(1, 13):
            t = s / 12.0
            q = (-30.0 + 60.0 * t, 0, 112.0 * math.sin(math.pi * t) ** 0.8)
            A.beam(prev, q, 12.0 * (1.0 - 0.4 * t), 12.0 * (1.0 - 0.4 * t), P['bark'])
            if s % 2 == 0:
                A.ball(11.0, q, P['leaf'] if s % 4 else P['leaf2'], segs=9, rings=6, scale=(1, 1, 0.8))
            prev = q
        A.cyl(10.0, 8.0, (-30.0, 0, 0), P['bark'], verts=10, r2=7.0)
        A.cyl(10.0, 8.0, (30.0, 0, 0), P['bark'], verts=10, r2=7.0)
    else:                                                                                        # broken top
        G.tree(A, rnd, 150.0, 32.0, TKD, 'broken', 0, 0, 0, 0.0)
        for k in range(7):
            a = rnd.uniform(0, 360)
            x, y, _ = polar(12.0, a)
            A.chunk((5.0, 3.0, rnd.uniform(14, 30)), (x, y, 96.0 + rnd.uniform(0, 18)), P['bark'], (0, 0, a), 0.2, rnd, (0.5, 0.5))
    for k in range(10):
        x, y, _ = polar(rnd.uniform(16, 36), rnd.uniform(0, 360))
        A.beam((x * 1.6, y * 1.6, 0.4), (x * 0.5, y * 0.5, 7.0), 4.0, 3.0, P['bark'])
    A.mound(0, 0, 30.0, 30.0, 3.0, 8, [P['moss'], P['ivy']], rnd, 0.0, 0.3, 0.6)
    return _fin(A, 'giant_tree')


def _forest_ruin(i):
    reset()
    A = Acc()
    rnd = random.Random(4400 + i)
    st = [P['stoneM'], P['rock2'], P['rock']]
    if i == 0:                                                                                   # overgrown arch (a ruin, kept deep in the forest)
        G.rock_arch(A, rnd, 18.0, 26.0, 4.0, st, 0, 0, 0, 5.0, 11)
    elif i == 1:
        for k in range(10):
            A.box((24.0 - k * 1.2, 3.0, 1.1), (0, -8.0 + k * 1.8, 0.55 + k * 1.1), st[k % 3], (0, 0, rnd.uniform(-3, 3)), bev=0.1)
        for sg in (-1, 1):
            A.chunk((2.4, 16.0, 6.0), (sg * 12.0, 0, 3.0), P['stoneM'], (0, 0, 0), 0.1, rnd)
    elif i == 2:
        for k in range(8):
            for z in range(3):
                if rnd.random() < 0.8 - z * 0.2:
                    A.chunk((5.0, 3.6, 3.0), (-17.5 + k * 5.0 + rnd.uniform(-0.3, 0.3), 0, 1.5 + z * 3.0), st[(k + z) % 3], (0, 0, 0), 0.1, rnd)
    elif i == 3:                                                                                 # altar
        A.chunk((16.0, 16.0, 2.0), (0, 0, 1.0), P['rock2'], jit=0.05, rnd=rnd)
        A.chunk((11.0, 11.0, 2.0), (0, 0, 3.0), P['stoneM'], jit=0.05, rnd=rnd)
        A.chunk((8.0, 4.4, 4.6), (0, 0, 6.3), P['stoneM'], jit=0.04, rnd=rnd)
        A.ball(1.0, (0, 0, 9.4), P['gold'], segs=8, rings=5)
        for k in range(4):
            x, y, _ = polar(9.6, k * 90.0 + 45.0)
            A.chunk((1.8, 1.8, 7.0 - k), (x, y, 3.5), P['stoneM'], (0, 0, 0), 0.1, rnd)
    else:
        for sg in (-1, 1):
            column(A, sg * 8.0, 0, 0, 1.7, 22.0 if i == 4 else 15.0, FK, 0.7 if sg > 0 else 0.3, rnd)
    for k in range(16):                                                                          # ivy and moss
        A.ball(rnd.uniform(1.2, 2.6), (rnd.uniform(-16, 16), rnd.uniform(-8, 6), rnd.uniform(0.8, 12)), P['ivy'] if k % 2 else P['moss'], segs=7, rings=4, scale=(1.3, 1.2, 0.8))
    return _fin(A, 'forest_ruin')


def _cave(i):
    reset()
    A = Acc()
    rnd = random.Random(4500 + i)
    if i < 3:                                                                                    # cave mouths in a rock face
        G.cliff(A, rnd, 40.0, 30.0, 30.0, ROCK, 0, 0, 0, 5, P['moss'], False)
        A.box((10.0 + i * 2.0, 20.0, 11.0 + i), (0, -4.0, 5.5), P['shadow'], bev=0)
        for k in range(5 + i):
            a = 180.0 * k / (4.0 + i)
            A.chunk((3.4, 5.0, 3.0), (math.cos(math.radians(a)) * (6.0 + i) * -1.0, -14.0, 11.0 + math.sin(math.radians(a)) * (5.0 + i)), ROCK[k % 3], (0, 0, 0), 0.1, rnd)
        for k in range(6):
            A.ball(rnd.uniform(1.4, 2.6), (rnd.uniform(-16, 16), rnd.uniform(-14, -8), rnd.uniform(18, 30)), P['ivy'], segs=7, rings=4, scale=(1.3, 1.2, 0.8))
    else:                                                                                        # rock arches
        G.rock_arch(A, rnd, 24.0 + (i - 3) * 4.0, 24.0, 5.0, ROCK, 0, 0, 0, 12.0, 11, P['moss'])
        A.mound(0, 0, 40.0, 20.0, 5.0, 10, ROCK, rnd, 0.0, 0.3, 0.6)
    for k in range(8):
        A.chunk((rnd.uniform(1.5, 3.5), rnd.uniform(1.5, 3.0), rnd.uniform(1.0, 2.0)), (rnd.uniform(-18, 18), rnd.uniform(-16, -8), 0.8), ROCK[k % 3], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    return _fin(A, 'cave_mouth')


def _birch(i):
    reset()
    A = Acc()
    rnd = random.Random(4600 + i)
    G.tree(A, rnd, 34.0, 7.0 + i * 0.5, TKB, 'birch', 0, 0, 0, i * 0.4 - 0.4)
    for k in range(7):
        A.box((0.6, 0.14, 0.4), (rnd.uniform(-0.6, 0.6), -1.0 - 0.0, rnd.uniform(1.0, 11.0)), P['shadow'], (0, 0, rnd.uniform(0, 180)), bev=0)
    return _fin(A, 'birch')


def _gorge(i):
    reset()
    A = Acc()
    rnd = random.Random(4700 + i)
    G.cliff(A, rnd, 90.0, 28.0, 80.0, ROCK + [P['bark']], 0, 0, 0, 12, P['moss'], True, 0.0 if i != 1 else 0.2)
    for k in range(12):
        x = rnd.uniform(-40, 40)
        A.ball(rnd.uniform(2.0, 4.0), (x, rnd.uniform(-14, -6), rnd.uniform(20, 70)), P['ivy'] if k % 2 else P['moss'], segs=7, rings=4, scale=(1.3, 1.1, 0.8))
    if i == 2:
        A.box((10.0, 1.4, 60.0), (20.0, -14.2, 40.0), P['water'], bev=0)
        A.box((5.0, 0.6, 58.0), (20.0, -15.0, 38.0), P['foam'], bev=0)
    return _fin(A, 'gorge_wall')


def _pool_rock(i):
    reset()
    A = Acc()
    rnd = random.Random(4800 + i)
    A.mound(0, 0, 28.0, 28.0, 14.0, 12 + i * 2, ROCK, rnd, 0.0, 0.4, 0.8)
    for k in range(5):
        A.ball(rnd.uniform(1.0, 2.0), (rnd.uniform(-10, 10), rnd.uniform(-10, 6), rnd.uniform(3, 12)), P['moss'], segs=6, rings=4, scale=(1.4, 1.2, 0.5))
    A.box((14.0, 6.0, 0.5), (0, -9.0, 0.3), P['water'], bev=0)
    return _fin(A, 'pool_rocks')


# ------------------------------------------------------------------ marsh
def _cypress(i):
    reset()
    A = Acc()
    rnd = random.Random(4900 + i)
    G.tree(A, rnd, 38.0, 11.0, TKC, 'cypress', 0, 0, 0, i * 0.5 - 0.5)
    for k in range(9):                                                                           # cypress knees
        x, y, _ = polar(rnd.uniform(3.5, 8.0), rnd.uniform(0, 360))
        A.cyl(rnd.uniform(0.5, 0.9), rnd.uniform(1.4, 3.2), (x, y, 0), P['bark'], verts=6, r2=0.2)
    for k in range(8):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(4, 9), a)
        A.cyl(0.14, rnd.uniform(5.0, 9.0), (x, y, 12.0), P['moss'], verts=5, r2=0.04, rot=(180, 0, 0))
    return _fin(A, 'swamp_cypress')


def _hummock(i):
    reset()
    A = Acc()
    rnd = random.Random(5000 + i)
    A.mound(0, 0, 16.0, 16.0, 5.5, 8, [P['moss'], P['ivy']], rnd, 0.0, 0.5, 0.9, 0.12)
    for k in range(18):
        x, y, _ = polar(rnd.uniform(0, 6.5), rnd.uniform(0, 360))
        A.cyl(0.07, rnd.uniform(2.0, 4.5), (x, y, 2.0), P['reed'], verts=4, r2=0.02, rot=(rnd.uniform(-10, 10), rnd.uniform(-10, 10), 0))
    return _fin(A, 'grass_hummock')


def _board(i):
    reset()
    A = Acc()
    rnd = random.Random(5100 + i)
    for k in range(30):
        A.box((0.9, 5.2, 0.28), (-14.5 + k * 1.0, 0, 3.0), P['plank'], (0, 0, rnd.uniform(-1.5, 1.5)), bev=0)
    for sg in (-1, 1):
        for k in range(7):
            A.cyl(0.32, 4.0, (-14.0 + k * 4.7, sg * 2.4, 0), P['bark'], verts=6)
        A.box((30.0, 0.5, 0.45), (0, sg * 2.4, 2.7), P['timber'], bev=0)
    if i == 1:
        for k in range(5):
            A.box((0.2, 0.2, 3.0), (-10.0 + k * 5.0, 2.8, 4.6), P['timber'], bev=0)
        A.beam((-10.0, 2.8, 5.8), (10.0, 2.8, 5.8), 0.18, 0.18, P['rope'])
    return _fin(A, 'marsh_boardwalk')


def _seq(prefix, fn, n):
    return [(mid, (lambda j=j: fn(j))) for j, mid in enumerate(ids(prefix))]


BATCHES = {
    'highland_set': ('v5_himalaya', mk(
        [(m, (lambda j=j: _ice_spire(j))) for j, m in enumerate(ids('HL01'))] + [(m, (lambda j=j: _ice_arch(j))) for j, m in enumerate(ids('HL02'))] +
        [(m, (lambda j=j: _glacier(j))) for j, m in enumerate(ids('HL03'))] + [(m, (lambda j=j: _ice_cave(j))) for j, m in enumerate(ids('HL04'))] +
        [(ids('HL05')[0], hidden_shrine), (ids('HL06')[0], mountain_watchtower)] + [(m, (lambda j=j: _mine(j))) for j, m in enumerate(ids('HL07'))] +
        [(m, (lambda j=j: _snow_spire(j))) for j, m in enumerate(ids('SP01'))], 0.1)),
    'fortress_parts': ('v5_landmarks', mk(
        [(m, (lambda j=j: _rampart(j))) for j, m in enumerate(ids('LM04'))] + [(m, (lambda j=j: _cliff_tower(j))) for j, m in enumerate(ids('LM05'))] +
        [(ids('LM06')[0], gate_tunnel)] + [(m, (lambda j=j: _switch_stairs(j))) for j, m in enumerate(ids('LM07'))] + [(ids('LM08')[0], stone_span)], 0.1)),
    'forest_set': ('v5_forest', mk(
        [(m, (lambda j=j: _giant_tree(j))) for j, m in enumerate(ids('FR01'))] + [(m, (lambda j=j: _forest_ruin(j))) for j, m in enumerate(ids('FR02'))] +
        [(m, (lambda j=j: _cave(j))) for j, m in enumerate(ids('FR03'))] + [(m, (lambda j=j: _birch(j))) for j, m in enumerate(ids('VG04'))] +
        [(m, (lambda j=j: _gorge(j))) for j, m in enumerate(ids('LM23'))] + [(m, (lambda j=j: _pool_rock(j))) for j, m in enumerate(ids('LM24'))], 0.1)),
    'marsh_set': ('v5_forest', mk(
        [(m, (lambda j=j: _cypress(j))) for j, m in enumerate(ids('VG05'))] + [(m, (lambda j=j: _hummock(j))) for j, m in enumerate(ids('VG06'))] +
        [(m, (lambda j=j: _board(j))) for j, m in enumerate(ids('VG07'))], 0.1)),
}
