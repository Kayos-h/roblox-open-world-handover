"""ve module - elf valley and Town 1: EV01 eight elf house types, EV02 canopy clusters, EV03 path pieces, RW02 world tree roots rework,
LM01 trunk door, LM02 waterfall set, TW01 statue with a face, TW02 street props, TW03 skull-avenue braziers and banner poles.
Elf style: living wood, pale bark, moss, teal shingles, warm lantern hooks. No glow anywhere (lanterns are plain mesh). Front faces -Y.
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v5kit
from v5kit import Acc, polar, tang, mk
import v5gen as G
import v4util

E = G.reg('ve', {
    'wood': ((140, 104, 70), 'Wood', 0.0, 0.9), 'bark': ((176, 150, 112), 'Wood', 0.0, 0.95), 'moss': ((86, 130, 70), 'Grass', 0.0, 1.0),
    'leaf1': ((70, 120, 60), 'Grass', 0.0, 1.0), 'leaf2': ((104, 150, 80), 'Grass', 0.0, 1.0), 'stone': ((150, 140, 120), 'Limestone', 0.0, 0.92),
    'shingle': ((80, 120, 100), 'Slate', 0.0, 0.85), 'rope': ((176, 150, 104), 'Fabric', 0.0, 1.0), 'lantern': ((236, 206, 150), 'SmoothPlastic', 0.0, 0.5),
    'dark': ((38, 42, 40), 'Slate', 0.0, 0.9), 'water': ((96, 150, 180), 'SmoothPlastic', 0.0, 0.2), 'plank': ((156, 120, 82), 'WoodPlanks', 0.0, 0.9),
    'cloth': ((196, 170, 120), 'Fabric', 0.0, 1.0), 'red': ((150, 70, 60), 'Fabric', 0.0, 1.0), 'foam': ((236, 244, 248), 'SmoothPlastic', 0.0, 0.5),
    'shroom': ((176, 80, 64), 'Fabric', 0.0, 0.9), 'cream': ((234, 224, 196), 'Fabric', 0.0, 0.9),
})
T1 = G.reg('ve_t1', {
    'dstone': ((70, 70, 78), 'Granite', 0.0, 0.92), 'stone': ((128, 124, 120), 'Slate', 0.0, 0.95), 'iron': ((58, 58, 64), 'Metal', 0.6, 0.6),
    'bone': ((226, 218, 200), 'Limestone', 0.0, 0.85), 'wood': ((118, 86, 56), 'Wood', 0.0, 0.9), 'plank': ((150, 112, 76), 'WoodPlanks', 0.0, 0.9),
    'cloth': ((150, 50, 50), 'Fabric', 0.0, 1.0), 'coal': ((46, 34, 30), 'Slate', 0.0, 0.95), 'brass': ((190, 154, 84), 'Metal', 0.8, 0.35),
    'dark': ((30, 30, 34), 'Slate', 0.0, 0.9), 'rope': ((176, 150, 104), 'Fabric', 0.0, 1.0), 'cream': ((232, 222, 196), 'Fabric', 0.0, 1.0),
    'green': ((70, 100, 70), 'Fabric', 0.0, 1.0), 'blue': ((60, 84, 120), 'Fabric', 0.0, 1.0),
})
E['gold'] = E['lantern']


def _fin(A, name, tol=None):
    A.to_scene()
    return finalize(name, 28)


# ------------------------------------------------------------------ building blocks
def _rings(A, r, z0, h, n, key, w=0.5, d=0.5, verts=18):
    for k in range(1, n):
        A.sweep([(r - 0.3, -w / 2), (r + d, -w / 2), (r + d, w / 2), (r - 0.3, w / 2)], 0, 360, verts, key, loc=(0, 0, z0 + h * k / n))


def _roundwin(A, ang, r, z, rr, key_frame, key_glass):
    x, y, _ = polar(r, ang)
    A.cyl(rr + 0.35, 0.3, (x, y, z), key_frame, verts=12, rot=(0, 90, ang))
    A.cyl(rr, 0.5, (x * 1.003, y * 1.003, z), key_glass, verts=12, rot=(0, 90, ang))


def _lantern(A, x, y, z, key_arm, key_l):
    A.beam((x, y, z), (x + 0.0, y - 0.9, z + 0.3), 0.14, 0.14, key_arm)
    A.cyl(0.38, 0.8, (x, y - 0.9, z - 0.7), key_l, verts=8)
    A.cyl(0.46, 0.18, (x, y - 0.9, z + 0.1), key_arm, verts=8)


def _deck(A, rnd, cx, cy, z, r, h=0.7, rail=True, verts=20, gap_ang=270.0):
    A.cyl(r, h, (cx, cy, z), E['plank'], verts=verts)
    A.cyl(r + 0.4, 0.5, (cx, cy, z - 0.5), E['wood'], verts=verts, r2=r * 0.8)
    for k in range(verts):
        a = 360.0 * k / verts
        if rail and abs(((a - gap_ang + 180) % 360) - 180) > 22:
            x, y, _ = polar(r - 0.3, a)
            A.box((0.28, 0.28, 3.0), (cx + x, cy + y, z + h + 1.5), E['wood'], bev=0)
    if rail:
        A.sweep([(r - 0.55, 3.0), (r - 0.05, 3.0), (r - 0.05, 3.4), (r - 0.55, 3.4)], gap_ang + 22, gap_ang + 338, 18, E['wood'], loc=(cx, cy, z + h))


def _ladder(A, x, y, z0, z1, key, ang=270.0, w=1.6):
    tx, ty = tang(ang)
    for sg in (-1, 1):
        A.beam((x + tx * sg * w / 2, y + ty * sg * w / 2, z0), (x + tx * sg * w / 2, y + ty * sg * w / 2, z1), 0.22, 0.22, key)
    n = int((z1 - z0) / 0.9)
    for k in range(1, n):
        z = z0 + (z1 - z0) * k / n
        A.beam((x - tx * w / 2, y - ty * w / 2, z), (x + tx * w / 2, y + ty * w / 2, z), 0.18, 0.18, key)


def _cone_roof(A, x, y, z, r, h, verts=16, over=1.4, rings=6):
    A.cyl(r + over, h, (x, y, z), E['shingle'], verts=verts, r2=0.0)
    for k in range(1, rings):
        t = k / rings
        A.sweep([((r + over) * (1 - t) - 0.2, -0.16), ((r + over) * (1 - t) + 0.45, -0.16), ((r + over) * (1 - t) + 0.45, 0.16), ((r + over) * (1 - t) - 0.2, 0.16)],
                0, 360, verts, E['moss'] if k % 3 == 0 else E['shingle'], loc=(x, y, z + h * t))
    A.revolve([(0.4, 0.0), (0.3, 1.4), (0.9, 1.9), (0.0, 3.4)], (x, y, z + h), E['leaf2'], segs=6)


def _hut(A, rnd, cx, cy, z, r, h, n_win=3, door=True, verts=16, roof_k=0.9, windows_z=0.55):
    A.cyl(r, h, (cx, cy, z), E['wood'], verts=verts, r2=r * 0.96)
    _rings(A, r, z, h, 4, E['bark'], 0.45, 0.45, verts)
    for i in range(n_win):
        _roundwin(A, 270.0 + 360.0 * (i + 0.5) / (n_win + 1) + 20 * (i % 2), r + 0.05, z + h * windows_z, 0.9, E['wood'], E['lantern'])
    if door:
        x, y, _ = polar(r + 0.05, 270.0)
        A.box((0.5, 2.4, 4.2), (cx + x, cy + y, z + 2.1), E['plank'], (0, 0, 270.0), bev=0.04)
        A.box((0.8, 3.2, 0.5), (cx + x, cy + y - 0.1, z + 4.4), E['bark'], (0, 0, 270.0), bev=0.04)
    _cone_roof(A, cx, cy, z + h, r, h * roof_k, verts)
    xl, yl, _ = polar(r + 0.1, 235.0)
    _lantern(A, cx + xl, cy + yl, z + h * 0.7, E['dark'], E['lantern'])


def _mushrooms(A, rnd, cx, cy, z, r, n=4):
    for k in range(n):
        x, y, _ = polar(r * rnd.uniform(0.8, 1.2), rnd.uniform(0, 360))
        s = rnd.uniform(0.5, 1.0)
        A.cyl(0.35 * s, 1.2 * s, (cx + x, cy + y, z), E['cream'], verts=6)
        A.ball(0.9 * s, (cx + x, cy + y, z + 1.3 * s), E['shroom'], segs=8, rings=5, scale=(1, 1, 0.55))


# ------------------------------------------------------------------ EV01 eight elf house types
def _elf(kind):
    reset()
    A = Acc()
    rnd = random.Random(500 + len(kind))
    A.cyl(8.0, 0.8, (0, 0, 0), E['moss'], verts=16, r2=7.2) if False else None
    if kind == 'tower':                                                                        # tall tower house: two tiers, outside spiral stair
        A.cyl(4.6, 8.0, (0, 0, 0), E['stone'], verts=14, r2=4.2)
        A.cyl(5.6, 0.7, (0, 0, 8.0), E['bark'], verts=14)
        _hut(A, rnd, 0, 0, 8.7, 4.4, 8.0, 3, True, 14)
        A.cyl(5.8, 0.7, (0, 0, 16.7), E['bark'], verts=14)
        _hut(A, rnd, 0, 0, 17.4, 3.5, 6.0, 2, False, 12, 1.1)
        for k in range(20):
            a = 270.0 + k * 22.0
            x, y, _ = polar(5.2, a)
            A.box((2.4, 1.6, 0.5), (x, y, 0.6 + k * 0.74), E['plank'], (0, 0, a + 90.0), bev=0.04)
        _deck(A, rnd, 0, 0, 16.0, 6.4, 0.6, True, 18)
    elif kind == 'bridge':                                                                     # house on a stone-and-root bridge
        for sx in (-11.0, 11.0):
            A.chunk((5.0, 5.0, 5.0), (sx, 0, 2.5), E['stone'], jit=0.08)
            for k in range(3):
                A.beam((sx * 0.7 + (k - 1) * 1.2, (k - 1) * 1.4, 0.0), (sx * 0.5, 0, 5.2), 1.0, 1.0, E['wood'])
        A.box((24.0, 5.0, 1.0), (0, 0, 5.2), E['plank'])
        for sg in (-1, 1):
            A.box((24.0, 0.4, 0.4), (0, sg * 2.4, 7.0), E['wood'], bev=0)
            for k in range(7):
                A.box((0.3, 0.3, 1.8), (-10.5 + k * 3.5, sg * 2.4, 6.2), E['wood'], bev=0)
        A.box((10.0, 4.6, 5.0), (0, 0, 8.2), E['wood'])
        A.gable(6.2, 12.0, 4.4, (0, 0, 10.7), E['shingle'], (0, 0, 90))
        G.roof_lines(A, 6.2, 12.0, 4.4, (0, 0, 10.7), E['moss'], 5)
        for sg in (-1, 1):
            for k in range(4):                                                                 # eave brackets and round windows on the long sides
                A.beam((-4.5 + k * 3.0, sg * 2.5, 10.6), (-4.5 + k * 3.0, sg * 3.3, 10.0), 0.25, 0.25, E['wood'])
                A.cyl(0.8, 0.4, (-4.5 + k * 3.0, sg * 2.38, 8.6), E['lantern'], verts=10, rot=(90, 0, 0))
                A.cyl(1.15, 0.3, (-4.5 + k * 3.0, sg * 2.34, 8.6), E['wood'], verts=10, rot=(90, 0, 0))
        for k in range(6):
            A.ball(rnd.uniform(0.7, 1.1), (rnd.choice((-1, 1)) * rnd.uniform(9.5, 12.5), rnd.uniform(-2.5, 2.5), 5.0), E['moss'], segs=6, rings=4, scale=(1.3, 1.1, 0.6))
        for sg in (-1, 1):
            _roundwin(A, 270.0, 2.35, 8.4, 0.9, E['wood'], E['lantern']) if False else A.cyl(0.9, 0.4, (sg * 2.6, -2.35, 8.6), E['lantern'], verts=10, rot=(90, 0, 0))
        A.box((2.2, 0.4, 3.6), (0, -2.35, 7.4), E['plank'], bev=0.04)
        _lantern(A, 4.2, -2.5, 10.0, E['dark'], E['lantern'])
        _ladder(A, -11.0, -3.2, 0.0, 5.2, E['wood'], 270.0)
    elif kind == 'library':                                                                    # library: round, big round window, scroll rack, lean-to reading porch
        A.cyl(9.0, 0.9, (0, 0, 0), E['stone'], verts=18, r2=8.6)
        _hut(A, rnd, 0, 0, 0.9, 7.4, 9.0, 4, True, 18, 0.8)
        A.cyl(2.8, 0.4, (0, -7.5, 5.8), E['wood'], verts=16, rot=(90, 0, 0))
        A.cyl(2.3, 0.5, (0, -7.55, 5.8), E['lantern'], verts=16, rot=(90, 0, 0))
        for k in range(8):
            a = k * 45.0
            A.beam((0, -7.6, 5.8), (math.cos(math.radians(a)) * 2.3, -7.6, 5.8 + math.sin(math.radians(a)) * 2.3), 0.14, 0.14, E['wood'])
        A.box((8.0, 3.0, 0.5), (0, -9.5, 3.2), E['plank'])
        for sx in (-3.6, 3.6):
            A.box((0.4, 0.4, 3.2), (sx, -10.8, 1.6), E['wood'], bev=0)
        for k in range(5):
            A.cyl(0.35, 2.4, (-3.0 + k * 1.5, -9.4, 3.5), E['cloth'], verts=6, rot=(0, 90, 0))
        _mushrooms(A, rnd, 0, 0, 0.9, 9.6, 3)
    elif kind == 'healer':                                                                     # healer hut: small round hut, herb racks, mushrooms, ramp
        A.cyl(6.8, 0.9, (0, 0, 0), E['moss'], verts=16, r2=6.2)
        _hut(A, rnd, 0, 0, 0.9, 5.0, 6.0, 2, True, 14, 1.0)
        for sx in (-1, 1):
            A.box((0.3, 0.3, 4.0), (sx * 6.6, -2.0, 2.9), E['wood'], bev=0)
        A.box((14.0, 0.3, 0.3), (0, -2.0, 4.9), E['wood'], bev=0)
        for k in range(9):
            A.cyl(0.35, 1.8, (-5.6 + k * 1.4, -2.0, 3.7), E['leaf1'] if k % 2 else E['leaf2'], verts=5, r2=0.1)
        for k in range(6):
            x, y, _ = polar(7.4, 200.0 + k * 28.0)
            A.ball(0.9, (x, y, 1.2), E['leaf2'] if k % 2 else E['leaf1'], segs=7, rings=4, scale=(1, 1, 0.8))
        _mushrooms(A, rnd, 0, 0, 0.9, 7.0, 5)
        A.box((2.0, 5.0, 0.4), (0, -7.0, 0.8), E['plank'], (6, 0, 0))
    elif kind == 'archery':                                                                    # archery lodge: open pavilion, target, bow rack
        A.cyl(10.0, 0.8, (0, 0, 0), E['plank'], verts=16)
        for k in range(8):
            x, y, _ = polar(8.6, k * 45.0)
            A.cyl(0.55, 7.0, (x, y, 0.8), E['wood'], verts=8)
            A.beam((x, y, 6.0), (x * 0.6, y * 0.6, 7.8), 0.4, 0.4, E['wood'])
        A.sweep([(7.4, 7.6), (9.2, 7.6), (9.2, 8.3), (7.4, 8.3)], 0, 360, 16, E['wood'])
        _cone_roof(A, 0, 0, 7.8, 9.0, 6.5, 16, 1.6)
        A.cyl(0.25, 5.0, (-3.0, 3.0, 0.8), E['wood'], verts=6)
        for k in range(4):
            A.beam((-4.0 + k * 1.2, 3.4, 1.2), (-3.6 + k * 1.2, 3.4, 4.6), 0.12, 0.12, E['wood'])
        A.cyl(3.2, 0.5, (0, -16.0, 5.2), E['cloth'], verts=18, rot=(90, 0, 0))
        for rr, key in ((2.5, E['red']), (1.7, E['cream']), (0.9, E['red'])):
            A.cyl(rr, 0.55, (0, -16.05, 5.2), key, verts=18, rot=(90, 0, 0))
        A.beam((-1.5, -16.0, 0.4), (0, -16.0, 5.0), 0.4, 0.4, E['wood'])
        A.beam((1.5, -16.0, 0.4), (0, -16.0, 5.0), 0.4, 0.4, E['wood'])
    elif kind == 'bath':                                                                       # bathhouse: low wide house with a pool, steam stack
        A.box((20.0, 14.0, 1.0), (0, 0, 0.5), E['stone'])
        A.box((13.0, 12.0, 5.0), (3.0, 0, 3.5), E['wood'])
        A.gable(14.5, 14.0, 5.0, (3.0, 0, 6.0), E['shingle'], (0, 0, 90))
        G.roof_lines(A, 14.5, 14.0, 5.0, (3.0, 0, 6.0), E['moss'], 6)
        for k in range(5):
            A.cyl(0.35, 5.2, (-0.5 + k * 3.0, -6.1, 1.0), E['wood'], verts=6)
            A.box((2.0, 0.3, 2.0), (1.0 + k * 0.0 + (k - 2) * 2.4, -6.05, 5.0), E['lantern'], bev=0) if k % 2 == 0 else None
        for k in range(7):
            A.cyl(0.14, 1.4 + 0.2 * (k % 3), (-6.0 + k * 0.9, 4.8 + (k % 2) * 0.8, 2.6), E['foam'], verts=5, r2=0.04)
        A.box((13.4, 0.5, 0.5), (3.0, -6.2, 6.1), E['wood'], bev=0)
        A.box((13.4, 0.5, 0.5), (3.0, 6.2, 6.1), E['wood'], bev=0)
        A.cyl(1.0, 5.0, (6.0, 3.0, 8.0), E['stone'], verts=8, r2=0.8)
        A.cyl(1.4, 0.4, (6.0, 3.0, 13.0), E['stone'], verts=8)
        A.box((7.0, 12.0, 1.4), (-7.0, 0, 1.2), E['stone'])
        A.box((5.6, 10.6, 0.5), (-7.0, 0, 2.0), E['water'], bev=0)
        for k in range(6):
            A.ball(rnd.uniform(0.7, 1.2), (-9.5 + rnd.uniform(0, 5), rnd.uniform(-6, 6), 1.2), E['stone'], segs=6, rings=4, scale=(1, 1, 0.7))
        A.box((2.4, 0.4, 3.8), (3.0, -6.2, 3.4), E['plank'], bev=0.04)
        for k in range(6):
            A.box((0.2, 0.4, 2.4), (-0.8 + k * 0.0, -6.3, 4.6), E['wood'], bev=0) if False else None
        A.box((4.0, 2.0, 0.4), (3.0, -8.0, 0.9), E['plank'])
        _lantern(A, 8.6, -6.2, 5.6, E['dark'], E['lantern'])
        A.box((3.0, 0.2, 2.0), (-3.0, -6.1, 5.0), E['cloth'], bev=0)
    elif kind == 'council':                                                                    # council hall: big round hall on a platform, ring seats, banner pole
        A.cyl(12.0, 1.2, (0, 0, 0), E['stone'], verts=20, r2=11.4)
        _hut(A, rnd, 0, 0, 1.2, 10.0, 8.0, 5, True, 20, 0.75)
        for k in range(5):
            x, y, _ = polar(10.4, 270.0 + 360.0 * (k + 0.5) / 6 + 10)
            A.beam((x, y, 1.4), (x * 1.18, y * 1.18, 1.4), 0.5, 0.5, E['wood']) if False else None
        for k in range(10):
            x, y, _ = polar(11.5, 240.0 + k * 12.0)
            A.box((0.4, 0.4, 2.0), (x, y, 2.2), E['wood'], bev=0)
        A.cyl(0.25, 9.0, (0, 0, 9.2 + 7.4), E['wood'], verts=6)
        A.box((0.1, 3.2, 4.0), (0, 1.6, 9.2 + 14.2), E['red'], bev=0)
        for k in range(5):
            x, y, _ = polar(13.0, 200.0 + k * 35.0)
            A.chunk((1.8, 1.6, 0.8), (x, y, 0.4), E['stone'], jit=0.1)
        A.box((6.0, 3.0, 0.5), (0, -12.5, 0.7), E['plank'])
    else:                                                                                      # weavers hall: long house, loom frames, cloth hangings
        A.box((20.0, 12.0, 1.0), (0, 0, 0.5), E['stone'])
        A.box((18.0, 10.0, 6.0), (0, 0, 4.0), E['wood'])
        A.gable(11.6, 19.0, 5.6, (0, 0, 7.0), E['shingle'], (0, 0, 90))
        G.roof_lines(A, 11.6, 19.0, 5.6, (0, 0, 7.0), E['moss'], 6)
        for k in range(5):
            _roundwin(A, 90.0, 5.05, 4.2, 0.8, E['wood'], E['lantern']) if False else A.cyl(0.8, 0.4, (-6.5 + k * 3.2, 5.05, 4.4), E['lantern'], verts=10, rot=(90, 0, 0))
            A.cyl(1.1, 0.3, (-6.5 + k * 3.2, 5.0, 4.4), E['wood'], verts=10, rot=(90, 0, 0))
        for k in range(6):
            A.beam((-8.0 + k * 3.2, -5.1, 6.9), (-8.0 + k * 3.2, -6.0, 6.3), 0.25, 0.25, E['wood'])
        A.box((19.0, 0.5, 0.5), (0, -5.9, 6.3), E['wood'], bev=0)
        for k in range(4):
            A.cyl(0.45, 6.4, (-6.0 + k * 4.0, -5.4, 1.0), E['wood'], verts=6)
        A.box((18.0, 0.3, 0.3), (0, -5.4, 6.0), E['wood'], bev=0)
        cols = [E['red'], E['cloth'], E['leaf1'], E['shroom'], E['cream']]
        for k in range(14):
            A.box((1.2, 0.08, 4.2 - (k % 3) * 0.6), (-8.0 + k * 1.2, -5.45, 3.6), cols[k % 5], bev=0)
        for sx in (-6.0, 0.0, 6.0):
            A.box((0.3, 0.3, 4.0), (sx - 1.0, 4.0, 3.5), E['bark'], bev=0)
            A.box((0.3, 0.3, 4.0), (sx + 1.0, 4.0, 3.5), E['bark'], bev=0)
            A.box((2.4, 0.3, 0.3), (sx, 4.0, 5.5), E['bark'], bev=0)
            A.box((2.0, 0.1, 2.6), (sx, 3.95, 3.9), cols[(int(sx) + 2) % 5], bev=0)
        A.box((2.6, 0.5, 4.0), (0, -5.1, 3.2), E['plank'], bev=0.04)
        _lantern(A, 8.2, -5.2, 5.4, E['dark'], E['lantern'])
        _mushrooms(A, rnd, 0, 0, 1.0, 10.0, 3)
    return _fin(A, 'elf_house_new')


ELF_KINDS = ['tower', 'bridge', 'library', 'healer', 'archery', 'bath', 'council', 'weaver']


def _mk_elf(i):
    return lambda: _elf(ELF_KINDS[i])


# ------------------------------------------------------------------ EV02 canopy clusters, RW02 roots, LM01 trunk, LM02 falls
def _canopy(seed, n):
    reset()
    A = Acc()
    rnd = random.Random(seed)
    A.cyl(3.4, 40.0, (0, 0, 0), E['bark'], verts=10, r2=2.6)
    for k in range(4):
        x, y, _ = polar(3.0, k * 90.0 + 20)
        A.beam((x * 2.2, y * 2.2, 0.0), (x * 0.6, y * 0.6, 7.0), 1.6, 1.6, E['wood'])
    spots = []
    for k in range(n):
        a = 360.0 * k / n + rnd.uniform(-20, 20)
        dist = rnd.uniform(22.0, 29.0)
        spots.append((a, dist, 10.0 + k * (22.0 / max(1, n - 1)) + rnd.uniform(-1, 1), rnd.uniform(6.5, 8.5)))
    prev = None
    for a, dist, z, r in spots:
        x, y, _ = polar(dist, a)
        A.beam((0, 0, z - 1.5), (x, y, z - 0.6), 1.0, 1.0, E['wood'])                         # branch to the platform
        _deck(A, rnd, x, y, z, r, 0.7, True, 18, a + 180.0)
        _hut(A, rnd, x, y, z + 0.7, r * 0.52, 3.8, 2, True, 12, 1.0)
        for sg in (-1, 1):
            xb, yb, _ = polar(r * 0.9, a + 90.0 * sg)
        if prev is not None:                                                                   # rope bridge to the previous platform
            px, py, pz, pr = prev
            p0 = (px + (x - px) * pr / math.hypot(x - px, y - py), py + (y - py) * pr / math.hypot(x - px, y - py), pz + 0.8)
            L = math.hypot(x - px, y - py) - pr - r
            d = ((x - px) / math.hypot(x - px, y - py), (y - py) / math.hypot(x - px, y - py))
            ang = math.degrees(math.atan2(d[1], d[0]))
            steps = int(L / 1.0)
            for s in range(steps):
                t = (s + 0.5) / steps
                px2 = p0[0] + d[0] * L * t
                py2 = p0[1] + d[1] * L * t
                pz2 = p0[2] + (z + 0.8 - pz - 0.8) * t - 1.2 * 4 * t * (1 - t)
                A.box((0.8, 2.2, 0.2), (px2, py2, pz2), E['plank'], (0, 0, ang), bev=0)
            for sg in (-1, 1):
                prevp = None
                for s in range(7):
                    t = s / 6.0
                    q = (p0[0] + d[0] * L * t - d[1] * sg * 1.1, p0[1] + d[1] * 0 + d[1] * L * t + d[0] * sg * 1.1, p0[2] + (z - pz) * t - 1.2 * 4 * t * (1 - t) + 1.6)
                    if prevp:
                        A.beam(prevp, q, 0.12, 0.12, E['rope'])
                    prevp = q
        prev = (x, y, z, r)
    a0, d0, z0_, r0 = spots[0]
    xl, yl, _ = polar(d0 + r0 * 0.6, a0 + 180.0)
    _ladder(A, xl, yl, 0.0, z0_ + 0.6, E['wood'], a0)
    v4util.marker('mk_lb', (xl, yl, 0.4))
    v4util.marker('mk_lt', (xl, yl, z0_ + 0.9))
    return _fin(A, 'canopy_cluster')


def canopy_1():
    return _canopy(601, 3)


def canopy_2():
    return _canopy(602, 4)


def canopy_3():
    return _canopy(603, 3)


def tree_roots():
    """RW02_01 - rework of D05_02: 9 rounded buttress roots with a soft taper, bright bark, moss patches, footprint 198 x 187 x 32."""
    reset()
    A = Acc()
    rnd = random.Random(611)
    A.cyl(34.0, 6.0, (0, 0, 0), E['bark'], verts=28, r2=30.0)
    for k in range(9):
        a0 = 360.0 * k / 9 + rnd.uniform(-8, 8)
        L = rnd.uniform(78.0, 98.0)
        curve = rnd.uniform(-18.0, 18.0)
        n = 14
        for s in range(n):
            t = s / (n - 1)
            r_ = 28.0 + L * t
            a = a0 + curve * t * t
            x, y, _ = polar(r_, a)
            wd = 13.0 * (1.0 - 0.8 * t) + 1.6
            hh = 26.0 * (1.0 - t) ** 1.3 + 2.4
            A.ball(1.0, (x, y, hh * 0.28), E['bark'] if s % 3 else E['wood'], segs=10, rings=6, scale=(wd * 1.25, wd * 0.75, hh * 0.62))
        for s in range(3):
            t = rnd.uniform(0.15, 0.7)
            x, y, _ = polar(28.0 + L * t, a0 + curve * t * t + rnd.uniform(-4, 4))
            A.ball(1.0, (x, y, 5.5 * (1 - t) + 1.5), E['moss'], segs=8, rings=4, scale=(rnd.uniform(4, 7), rnd.uniform(3, 5), 1.4))
    for k in range(22):
        x, y, _ = polar(rnd.uniform(34.0, 92.0), rnd.uniform(0, 360))
        A.ball(rnd.uniform(1.2, 2.4), (x, y, 0.8), E['moss'], segs=7, rings=4, scale=(1.6, 1.3, 0.5))
    _mushrooms(A, rnd, 0, 0, 0.5, 46.0, 6)
    return v5kit.fit(_fin(A, 'world_tree_roots'), w=198.0, d=187.0, h=32.0)


def trunk_door():
    """LM01_01 - hollow trunk piece, 36 across, 50 tall: bark ribs, door, inner spiral stair, lantern niche."""
    reset()
    A = Acc()
    rnd = random.Random(621)
    ro, ri = 18.0, 13.0
    A.ring_wall(ri, ro, 0.0, 50.0, [(270.0, 9.0, [(0.0, 13.0)]), (30.0, 3.6, [(26.0, 31.0)]), (150.0, 3.6, [(30.0, 35.0)]), (90.0, 3.0, [(14.0, 19.0)])], E['bark'])
    for k in range(18):                                                                        # bark ribs and root flare
        a = 20.0 * k + rnd.uniform(-4, 4)
        x, y, _ = polar(ro + 0.2, a)
        if abs(((a - 270 + 180) % 360) - 180) < 14:
            continue
        A.chunk((1.6, 1.6, rnd.uniform(14, 40)), (x, y, rnd.uniform(8, 22)), E['wood'], (0, 0, a), 0.14, rnd, (0.6, 0.8))
        A.beam((x * 1.5, y * 1.5, 0.3), (x, y, 8.0), 1.8, 1.8, E['wood'])
    A.cyl(ro + 3.0, 1.0, (0, 0, 0), E['moss'], verts=24, r2=ro + 1.2) if False else None
    A.cyl(ri + 0.5, 0.8, (0, 0, 0), E['plank'], verts=20)
    for k in range(34):                                                                        # inner spiral stair
        a = 200.0 + k * 11.0
        x, y, _ = polar(ri - 2.4, a)
        A.box((1.6, 3.6, 0.5), (x, y, 1.0 + k * 1.3), E['plank'], (0, 0, a + 90.0), bev=0.04)
    A.cyl(0.6, 46.0, (0, 0, 0.8), E['wood'], verts=8)
    A.sweep([(ri - 0.4, 24.0), (ri + 0.2, 24.0), (ri + 0.2, 25.0), (ri - 0.4, 25.0)], 0, 360, 20, E['wood'])
    x, y, _ = polar(ri - 0.6, 90.0)
    A.box((3.6, 2.6, 4.6), (x, y, 15.6), E['dark'], (0, 0, 90.0), bev=0.04)                      # lantern niche
    A.cyl(0.5, 1.0, (x, y - 0.6, 14.8), E['lantern'], verts=8)
    for z in (27.0, 31.0):
        for a in (30.0, 150.0):
            x, y, _ = polar(ro + 0.2, a)
            A.box((0.5, 4.4, 5.6), (x, y, z + 1.0), E['wood'], (0, 0, a), bev=0) if False else None
    for k in range(6):
        x, y, _ = polar(ro - 0.1, 240.0 + k * 12.0)
        A.box((0.8, 1.0, 13.0), (x, y, 6.6), E['wood'], (0, 0, 240.0 + k * 12.0), bev=0) if abs(240.0 + k * 12.0 - 270.0) > 8 else None
    A.box((1.2, 11.0, 0.6), (0, -ro - 0.6, 13.6), E['wood'], bev=0.05)
    A.cyl(ri + 1.0, 4.0, (0, 0, 50.0), E['moss'], verts=20, r2=ri + 2.5)
    return _fin(A, 'world_tree_trunk_door')


def tree_falls():
    """LM02_01 - three-tier waterfall set: stepped rock cliff, water ribbons and plunge pools. 80 wide, 40 deep, 110 tall."""
    reset()
    A = Acc()
    rnd = random.Random(631)
    keys = [E['stone'], E['dark'], E['stone'], E['bark']]
    G.cliff(A, rnd, 80.0, 40.0, 110.0, keys, 0, 8.0, 0.0, cols=11, cap=E['moss'], ledges=True)
    tiers = [(100.0, 80.0), (74.0, 54.0), (48.0, 28.0)]
    for i, (zt, zb) in enumerate(tiers):
        wd = 22.0 - i * 3.0
        x0 = -4.0 + i * 5.0
        A.box((wd, 3.0, zt - zb + 2.0), (x0, -11.5 - i * 4.0, (zt + zb) / 2.0), E['water'], bev=0)
        A.box((wd * 0.6, 0.6, zt - zb), (x0, -13.2 - i * 4.0, (zt + zb) / 2.0 - 0.4), E['foam'], bev=0)
        A.box((wd + 4.0, 13.0, 2.4), (x0, -16.0 - i * 4.0, zb - 0.4), E['stone'], bev=0.1)      # basin rim
        A.box((wd + 1.6, 11.0, 0.8), (x0, -16.0 - i * 4.0, zb + 0.5), E['water'], bev=0)
        for k in range(7):
            A.ball(rnd.uniform(0.8, 1.6), (x0 + rnd.uniform(-wd / 2, wd / 2), -20.0 - i * 4.0 + rnd.uniform(-2, 2), zb + 1.1), E['foam'], segs=6, rings=4, scale=(1.4, 1.1, 0.5))
    A.box((30.0, 15.0, 0.8), (6.0, -29.0, 0.4), E['water'], bev=0)
    for k in range(10):
        A.chunk((rnd.uniform(2.0, 4.5), rnd.uniform(2.0, 4.0), rnd.uniform(1.2, 2.6)), (rnd.uniform(-24, 28), rnd.uniform(-34, -22), 1.0), keys[k % 4], (0, 0, rnd.uniform(0, 90)), 0.14, rnd)
    for k in range(8):
        G.tree(A, rnd, rnd.uniform(14, 22), 5.0, {'bark': E['wood'], 'leaf': E['leaf1'], 'leaf2': E['leaf2'], 'bloom': E['leaf2']}, 'oak', rnd.uniform(-38, 38), rnd.uniform(14, 18), 100.0 if False else rnd.uniform(60, 104)) if False else None
    for k in range(9):
        A.ball(rnd.uniform(2.0, 3.6), (rnd.uniform(-36, 36), rnd.uniform(12, 24), rnd.uniform(90, 108)), E['leaf1'] if k % 2 else E['leaf2'], segs=8, rings=5, scale=(1.3, 1.2, 0.8))
    return _fin(A, 'world_tree_falls')


# ------------------------------------------------------------------ EV03 elf path pieces
def _path(kind):
    reset()
    A = Acc()
    rnd = random.Random(700 + len(kind))
    if kind == 'rootstairs':
        for i in range(9):
            A.chunk((14.0 - i * 0.6, 2.4, 0.6 * (i + 1)), (0, -9.0 + i * 2.1, 0.3 * (i + 1)), E['bark'] if i % 2 else E['wood'], jit=0.06, rnd=rnd)
        for sg in (-1, 1):
            for k in range(4):
                A.beam((sg * (8.0 + rnd.uniform(0, 1.2)), -9.0 + k * 5.0, 0.2), (sg * 7.0, -7.0 + k * 5.0, 1.6 + k * 0.5), 1.2, 1.0, E['wood'])
        for k in range(5):
            A.ball(rnd.uniform(0.9, 1.5), (rnd.choice((-1, 1)) * rnd.uniform(5.5, 8.5), rnd.uniform(-8, 8), 0.5 + 0.0), E['moss'], segs=6, rings=4, scale=(1.5, 1.2, 0.5))
    elif kind == 'carved':
        for i in range(8):
            A.box((12.0, 2.4, 0.55 * (i + 1)), (0, -8.4 + i * 2.2, 0.275 * (i + 1)), E['stone'], bev=0.1)
            A.box((12.6, 0.3, 0.2), (0, -8.4 + i * 2.2 - 1.15, 0.55 * (i + 1) - 0.05), E['moss'], bev=0)
        for sg in (-1, 1):
            for i in range(0, 8, 2):
                A.cyl(0.3, 2.0, (sg * 6.8, -8.4 + i * 2.2, 0.55 * (i + 1) + 0.2), E['wood'], verts=6)
                A.cyl(0.46, 0.4, (sg * 6.8, -8.4 + i * 2.2, 0.55 * (i + 1) + 2.2), E['lantern'], verts=8)
    elif kind == 'bridge':
        for sx in (-8.5, 8.5):
            A.chunk((4.0, 7.0, 3.6), (sx, 0, 1.8), E['stone'], jit=0.08, rnd=rnd)
        for i in range(24):
            t = i / 23.0
            x = -8.0 + 16.0 * t
            z = 3.6 + math.sin(math.pi * t) * 1.8
            A.box((0.8, 5.6, 0.4), (x, 0, z), E['plank'], (0, -math.degrees(math.cos(math.pi * t) * 0.4), 0), bev=0)
        for sg in (-1, 1):
            for k in range(5):
                x = -8.0 + 4.0 * k
                t = (x + 8.0) / 16.0
                A.beam((x, sg * 2.8, 3.6 + math.sin(math.pi * t) * 1.8), (x, sg * 2.8, 5.4 + math.sin(math.pi * t) * 1.8), 0.3, 0.3, E['wood'])
            A.beam((-8.0, sg * 2.8, 5.4), (8.0, sg * 2.8, 5.4), 0.3, 0.3, E['wood'])
            for k in range(3):
                A.beam((-6.0 + k * 6.0, sg * 3.4, 0.0), (-6.0 + k * 6.0 + 1.0, sg * 2.4, 3.4), 0.9, 0.9, E['wood'])
        v4util.marker('mk_enda', (-9.0, 0, 4.0))
        v4util.marker('mk_endb', (9.0, 0, 4.0))
    elif kind == 'garden':                                                                     # garden trellis made of two roots meeting overhead (natural, inside the village)
        for sg in (-1, 1):
            prev = (sg * 6.0, 0, 0.0)
            for s in range(1, 9):
                t = s / 8.0
                q = (sg * 6.0 * (1 - t * t * 0.95) + 0.0, 0, 11.0 * math.sin(t * math.pi / 2.0))
                A.beam(prev, q, 1.4 - 0.8 * t, 1.4 - 0.8 * t, E['wood'])
                prev = q
            for k in range(7):
                z = 1.0 + k * 1.5
                x = sg * (6.0 - 5.0 * (z / 11.0) ** 2)
                A.ball(rnd.uniform(0.6, 1.0), (x + rnd.uniform(-0.5, 0.5), rnd.uniform(-0.6, 0.6), z), E['leaf1'] if k % 2 else E['leaf2'], segs=6, rings=4)
        for k in range(10):
            A.ball(rnd.uniform(0.8, 1.2), (rnd.uniform(-2.5, 2.5), rnd.uniform(-0.6, 0.6), rnd.uniform(9.0, 11.0)), E['leaf2'], segs=6, rings=4)
        A.chunk((3.0, 3.0, 0.8), (-6.0, 0, 0.4), E['stone'], jit=0.1, rnd=rnd)
        A.chunk((3.0, 3.0, 0.8), (6.0, 0, 0.4), E['stone'], jit=0.1, rnd=rnd)
    elif kind == 'posts':
        for k in range(4):
            x = -7.5 + k * 5.0
            A.cyl(0.55, 5.0, (x, 0, 0), E['wood'], verts=8, r2=0.45)
            A.ball(0.7, (x, 0, 5.3), E['wood'], segs=7, rings=4)
            A.beam((x, 0, 4.2), (x + 0.0, -1.0, 4.6), 0.14, 0.14, E['dark'])
            A.cyl(0.4, 0.8, (x, -1.0, 3.6), E['lantern'], verts=8)
            A.chunk((1.8, 1.8, 0.5), (x, 0, 0.25), E['stone'], jit=0.1, rnd=rnd)
            A.ball(0.45, (x + rnd.uniform(-0.5, 0.5), 0.9, 0.3), E['leaf2'], segs=6, rings=4)
    else:                                                                                      # plaza paving ring
        A.sweep([(3.6, 0.0), (9.4, 0.0), (9.4, 0.6), (3.6, 0.6)], 0, 360, 36, E['stone'])
        for k in range(36):
            a = k * 10.0
            for rr, w in ((4.6, 1.6), (6.2, 2.0), (7.8, 2.4), (9.0, 1.8)):
                x, y, _ = polar(rr, a + (5.0 if rr in (6.2, 9.0) else 0.0))
                A.box((w, 0.2, 0.2), (x, y, 0.65), E['moss'] if k % 7 == 0 else E['stone'], (0, 0, a + 90.0), bev=0)
        A.sweep([(9.4, 0.0), (10.0, 0.0), (10.0, 0.9), (9.4, 0.9)], 0, 360, 36, E['wood'])
        for k in range(6):
            x, y, _ = polar(5.0, k * 60.0)
            A.ball(1.0, (x, y, 0.9), E['leaf1'], segs=6, rings=4, scale=(1.2, 1.2, 0.5))
    return _fin(A, 'elf_path_piece')


PATH_KINDS = ['rootstairs', 'carved', 'bridge', 'garden', 'posts', 'plaza']


def _mk_path(i):
    return lambda: _path(PATH_KINDS[i])


# ------------------------------------------------------------------ TW01 statue, TW02 street life, TW03 avenue set
def statue():
    """TW01_01 - robed hero statue with a modelled face (brow, nose, eye hollows, mouth, chin), staff, cloak, stepped plinth. 14 x 14 x 40."""
    reset()
    A = Acc()
    for k in range(3):
        A.box((14.0 - k * 2.4, 14.0 - k * 2.4, 1.6), (0, 0, 0.8 + k * 1.6), T1['dstone'], bev=0.12)
    A.box((8.0, 8.0, 3.2), (0, 0, 6.4), T1['stone'], bev=0.12)
    A.box((8.8, 8.8, 0.7), (0, 0, 8.2), T1['dstone'], bev=0.08)
    z0 = 8.55
    for sx in (-1.4, 1.4):                                                                     # legs and feet
        A.frustum((2.6, 2.8), (2.2, 2.4), 8.0, (sx, 0, z0), T1['stone'])
        A.box((2.8, 4.0, 1.0), (sx, -0.7, z0 + 0.5), T1['dstone'], bev=0.1)
    A.frustum((7.2, 4.6), (5.2, 3.6), 12.0, (0, 0, z0 + 7.0), T1['bone'])                      # robe
    A.box((7.6, 5.0, 0.8), (0, 0, z0 + 12.6), T1['cloth'], bev=0.08) if False else A.box((5.6, 3.8, 0.7), (0, 0, z0 + 12.8), T1['dstone'], bev=0.08)
    A.frustum((5.8, 3.6), (7.4, 3.0), 4.4, (0, 0.1, z0 + 12.9), T1['bone'])                    # chest
    A.box((8.0, 0.8, 11.0), (0, 2.8, z0 + 11.0), T1['dstone'], (-8, 0, 0), bev=0.1)             # cloak
    for sg in (-1, 1):
        A.beam((sg * 3.8, 0, z0 + 16.0), (sg * 4.4, -1.8, z0 + 12.2), 1.2, 1.2, T1['bone'])    # arms
    A.beam((4.4, -1.8, z0 + 12.2), (4.6, -2.4, z0 + 11.6), 1.4, 1.4, T1['stone'])
    A.cyl(0.4, 28.0, (4.6, -2.4, z0 - 0.4), T1['wood'], verts=8)                              # staff in the right hand
    A.ball(1.0, (4.6, -2.4, z0 + 28.0), T1['brass'], segs=8, rings=5)
    A.box((2.0, 2.0, 0.3), (4.6, -2.4, z0 + 26.6), T1['brass'], (0, 0, 45), bev=0)
    zh = z0 + 18.4
    A.cyl(0.9, 1.2, (0, 0, zh - 1.0), T1['stone'], verts=10)                                   # neck
    A.ball(2.3, (0, -0.1, zh + 1.4), T1['bone'], segs=14, rings=10, scale=(0.92, 1.0, 1.12))   # head
    A.box((3.6, 0.5, 0.55), (0, -2.2, zh + 2.1), T1['stone'], bev=0.04)                       # brow ridge
    A.box((0.7, 1.2, 1.7), (0, -2.45, zh + 1.2), T1['bone'], (-14, 0, 0), bev=0.04)            # nose
    for sx in (-0.95, 0.95):
        A.ball(0.42, (sx, -2.15, zh + 1.85), T1['dark'], segs=8, rings=5, scale=(1.2, 0.6, 0.8))  # eye hollows
        A.box((1.0, 0.25, 0.18), (sx, -2.28, zh + 2.35), T1['stone'], (0, 0, sx * -6), bev=0)    # lids
    A.box((1.5, 0.35, 0.25), (0, -2.2, zh + 0.15), T1['dark'], bev=0)                          # mouth
    A.ball(0.7, (0, -1.9, zh - 0.65), T1['bone'], segs=8, rings=5, scale=(1.0, 0.9, 0.7))      # chin
    for sx in (-2.15, 2.15):
        A.ball(0.45, (sx, 0, zh + 1.2), T1['bone'], segs=6, rings=4, scale=(0.5, 0.7, 1.0))    # ears
    A.frustum((5.6, 5.2), (4.6, 4.4), 2.6, (0, 0.2, zh + 2.4), T1['dstone'])                  # hood
    A.box((5.2, 0.5, 1.4), (0, 2.4, zh + 1.0), T1['dstone'], bev=0.05)
    return _fin(A, 'town1_hero_statue')


def _street(kind):
    reset()
    A = Acc()
    rnd = random.Random(800 + len(kind))
    if kind == 'handcart':
        A.box((8.0, 5.0, 0.5), (0, 0, 2.6), T1['plank'], bev=0.05)
        for sg in (-1, 1):
            A.box((8.0, 0.4, 1.4), (0, sg * 2.4, 3.5), T1['plank'], bev=0.04)
            A.cyl(2.2, 0.5, (0, sg * 3.0, 2.2), T1['wood'], verts=14, rot=(90, 0, 0))
            A.cyl(0.4, 0.7, (0, sg * 3.0, 2.2), T1['iron'], verts=8, rot=(90, 0, 0))
            for k in range(6):
                a = k * 30.0
                A.box((0.2, 0.3, 4.2), (0, sg * 3.0, 2.2), T1['wood'], (a, 0, 0), bev=0)
            A.beam((4.0, sg * 1.9, 3.0), (9.5, sg * 0.9, 2.2), 0.3, 0.3, T1['wood'])
        A.box((0.4, 5.0, 1.4), (-4.0, 0, 3.5), T1['plank'], bev=0.04)
        for k in range(4):
            A.box((1.6, 1.6, 1.4), (-2.5 + k * 1.8, rnd.uniform(-1, 1), 3.6), T1['cream'] if k % 2 else T1['wood'], (0, 0, rnd.uniform(0, 40)), bev=0.08)
        A.ball(1.0, (1.5, 0, 4.0), T1['green'], segs=8, rings=5)
    elif kind == 'wagon':
        A.box((10.0, 5.6, 0.5), (0, 0, 3.0), T1['plank'], bev=0.05)
        for sg in (-1, 1):
            A.box((10.0, 0.4, 1.8), (0, sg * 2.7, 4.2), T1['plank'], bev=0.04)
            for sx in (-3.2, 3.2):
                A.cyl(2.6, 0.5, (sx, sg * 3.3, 2.6), T1['wood'], verts=16, rot=(90, 0, 0))
                A.cyl(0.5, 0.8, (sx, sg * 3.3, 2.6), T1['iron'], verts=8, rot=(90, 0, 0))
        A.box((10.4, 0.4, 1.8), (0, 2.9, 4.2), T1['plank'], bev=0.04) if False else None
        for k in range(5):
            A.beam((-4.5 + k * 2.25, -2.7, 4.1), (-4.5 + k * 2.25, -2.7, 7.0), 0.25, 0.25, T1['wood'])
            A.beam((-4.5 + k * 2.25, 2.7, 4.1), (-4.5 + k * 2.25, 2.7, 7.0), 0.25, 0.25, T1['wood'])
        A.frustum((10.4, 5.8), (9.0, 4.4), 2.2, (0, 0, 7.0), T1['cream'])
        A.beam((5.0, 0, 3.0), (11.0, 0, 2.4), 0.4, 0.4, T1['wood'])
    elif kind == 'crates':
        for (x, y, z, s) in ((-2.5, 0, 0, 3.2), (1.5, -0.5, 0, 3.0), (-1.0, 0.2, 3.2, 2.8), (2.5, 2.0, 0, 2.4), (-3.5, 2.6, 0, 2.2), (1.0, -0.6, 3.0, 2.2)):
            A.box((s, s, s), (x, y, z + s / 2), T1['plank'], (0, 0, rnd.uniform(-12, 12)), bev=0.1)
            A.box((s + 0.1, s * 0.12, s + 0.1), (x, y, z + s / 2), T1['wood'], (0, 0, 0), bev=0) if False else None
            for sg in (-1, 1):
                A.box((0.22, s + 0.06, s + 0.06), (x + sg * s * 0.36, y, z + s / 2), T1['wood'], (0, 0, 0), bev=0)
    elif kind == 'crates2':
        for r_ in range(3):
            for c in range(3 - r_):
                A.box((2.6, 2.6, 2.2), (-2.6 + c * 2.7 + r_ * 1.35, 0, 1.1 + r_ * 2.2), T1['plank'], (0, 0, rnd.uniform(-5, 5)), bev=0.08)
                A.box((2.7, 0.2, 2.3), (-2.6 + c * 2.7 + r_ * 1.35, -1.3, 1.1 + r_ * 2.2), T1['wood'], bev=0)
        for k in range(3):
            A.cyl(0.9, 1.6, (4.2 + k * 0.6, 2.0 - k * 1.0, 0), T1['cream'], verts=10)
        A.box((1.8, 1.8, 1.6), (5.4, -2.2, 0.8), T1['wood'], bev=0.08)
    elif kind == 'barrels':
        for (x, y, z) in ((-2.4, 0, 0), (0.2, 0, 0), (2.8, 0, 0), (-1.1, 0.2, 2.6), (1.5, 0.2, 2.6), (0.2, 0.3, 5.2)):
            A.cyl(1.25, 2.6, (x, y, z), T1['plank'], verts=12, r2=1.25)
            A.cyl(1.4, 1.2, (x, y, z + 0.7), T1['plank'], verts=12, r2=1.4)
            for hz in (0.35, 2.15):
                A.sweep([(1.2, -0.12), (1.46, -0.12), (1.46, 0.12), (1.2, 0.12)], 0, 360, 12, T1['iron'], loc=(x, y, z + hz))
            A.cyl(1.0, 0.1, (x, y, z + 2.6), T1['wood'], verts=12)
    elif kind == 'sign_inn':
        A.beam((0, 0, 9.0), (5.4, 0, 9.0), 0.4, 0.4, T1['iron'])
        A.beam((0, 0, 5.0), (0, 0, 9.4), 0.5, 0.5, T1['iron'])
        A.beam((0.3, 0, 6.0), (2.8, 0, 8.8), 0.28, 0.28, T1['iron'])
        for sx in (3.6, 5.0):
            A.beam((sx, 0, 9.0), (sx, 0, 8.3), 0.08, 0.08, T1['iron'])
        A.box((2.4, 0.4, 3.2), (4.3, 0, 6.8), T1['plank'], bev=0.05)
        A.cyl(0.9, 0.5, (4.3, -0.4, 7.2), T1['brass'], verts=12, rot=(90, 0, 0))              # tankard-and-mug emblem
        A.cyl(0.55, 0.9, (4.3, -0.5, 6.0), T1['cream'], verts=10, rot=(90, 0, 0))
    elif kind == 'sign_smith':
        A.beam((0, 0, 9.0), (5.4, 0, 9.0), 0.4, 0.4, T1['iron'])
        A.beam((0, 0, 5.0), (0, 0, 9.4), 0.5, 0.5, T1['iron'])
        for sx in (3.4, 5.0):
            A.beam((sx, 0, 9.0), (sx, 0, 8.3), 0.08, 0.08, T1['iron'])
        A.box((2.6, 0.35, 3.0), (4.2, 0, 6.8), T1['dstone'], bev=0.05)
        A.box((1.8, 0.6, 0.8), (4.2, -0.4, 7.2), T1['iron'], bev=0.05)                           # anvil emblem
        A.box((0.8, 0.6, 1.0), (4.2, -0.4, 6.6), T1['iron'], bev=0.05)
        A.box((1.8, 0.6, 0.4), (4.2, -0.4, 6.1), T1['iron'], bev=0.05)
    else:                                                                                       # bench
        A.box((9.0, 2.6, 0.5), (0, 0, 2.6), T1['plank'], bev=0.05)
        A.box((9.0, 0.5, 2.0), (0, 1.2, 4.0), T1['plank'], (-6, 0, 0), bev=0.05)
        for sx in (-3.8, 3.8):
            A.box((0.6, 2.4, 2.6), (sx, 0, 1.3), T1['dstone'], bev=0.06)
            A.box((0.5, 0.5, 4.2), (sx, 1.3, 3.2), T1['iron'], bev=0)
        A.box((9.4, 3.0, 0.3), (0, 0, 0.15), T1['stone'], bev=0)
    return _fin(A, 'town1_street_life')


STREET_KINDS = ['handcart', 'wagon', 'crates', 'crates2', 'barrels', 'sign_inn', 'sign_smith', 'bench']


def _mk_street(i):
    return lambda: _street(STREET_KINDS[i])


def _avenue(kind):
    reset()
    A = Acc()
    rnd = random.Random(900 + len(kind))
    if kind in ('brazier1', 'brazier2'):
        A.cyl(3.2, 0.8, (0, 0, 0), T1['dstone'], verts=12)
        if kind == 'brazier1':                                                                   # tripod brazier
            for k in range(3):
                x, y, _ = polar(2.2, k * 120.0)
                A.beam((x * 1.2, y * 1.2, 0.6), (0, 0, 6.8), 0.5, 0.5, T1['iron'])
            A.cyl(3.4, 1.6, (0, 0, 6.6), T1['iron'], verts=14, r2=2.4, rot=(180, 0, 0)) if False else A.cyl(2.4, 1.6, (0, 0, 6.6), T1['iron'], verts=14, r2=3.5)
            A.cyl(3.0, 0.3, (0, 0, 8.0), T1['coal'], verts=14)
            for k in range(7):
                x, y, _ = polar(1.7, k * 51.4)
                A.chunk((1.0, 1.0, 0.8), (x, y, 8.3), T1['coal'], jit=0.2, rnd=rnd)
        else:                                                                                    # pedestal brazier
            A.cyl(1.4, 5.0, (0, 0, 0.8), T1['stone'], verts=8, r2=1.0)
            A.cyl(1.9, 0.6, (0, 0, 5.8), T1['dstone'], verts=8)
            A.cyl(3.6, 2.2, (0, 0, 6.4), T1['iron'], verts=16, r2=4.2)
            A.sweep([(3.9, 0.0), (4.6, 0.0), (4.6, 0.5), (3.9, 0.5)], 0, 360, 16, T1['brass'], loc=(0, 0, 8.4))
            A.cyl(3.4, 0.3, (0, 0, 8.4), T1['coal'], verts=16)
            for k in range(8):
                x, y, _ = polar(2.0, k * 45.0)
                A.chunk((1.0, 1.0, 0.8), (x, y, 8.8), T1['coal'], jit=0.2, rnd=rnd)
            for k in range(4):
                A.ball(0.5, (polar(4.3, k * 90.0 + 45)[0], polar(4.3, k * 90.0 + 45)[1], 8.1), T1['brass'], segs=6, rings=4)
    else:
        A.cyl(2.8, 1.2, (0, 0, 0), T1['dstone'], verts=10)
        A.cyl(0.55, 20.0, (0, 0, 1.0), T1['wood'], verts=8, r2=0.4)
        A.ball(0.8, (0, 0, 21.3), T1['brass'], segs=8, rings=5)
        A.beam((0, 0, 19.0), (5.6, 0, 19.0), 0.28, 0.28, T1['iron'])
        col = T1['cloth'] if kind == 'banner1' else T1['blue']
        A.box((0.12, 4.0, 9.4), (5.4, 0, 14.0), col, bev=0)
        A.box((0.2, 4.4, 0.4), (5.4, 0, 9.2), T1['brass'], bev=0)
        A.box((0.13, 2.6, 1.1), (5.4 + 0.05, 0, 16.4), T1['bone'], bev=0)                       # bone-white jaw emblem
        for k in range(5):
            A.box((0.13, 0.26, 0.6), (5.45, -1.0 + k * 0.5, 15.5), T1['bone'], bev=0)
        for sg in (-1, 1):
            A.beam((0, 0, 3.0), (sg * 3.2, 0, 1.0), 0.3, 0.3, T1['iron'])
    return _fin(A, 'skull_avenue_set')


AVENUE_KINDS = ['brazier1', 'brazier2', 'banner1', 'banner2']


def _mk_avenue(i):
    return lambda: _avenue(AVENUE_KINDS[i])


BATCHES = {
    'elf_houses': ('v5_elf', mk([(f'EV01_{i + 1:02d}_elf_house_new_{i + 1:02d}', _mk_elf(i)) for i in range(8)])),
    'canopy_roots': ('v5_elf', mk([('EV02_01_canopy_cluster_01', canopy_1), ('EV02_02_canopy_cluster_02', canopy_2), ('EV02_03_canopy_cluster_03', canopy_3)], 0.1) + [
        ('RW02_01_rework_world_tree_roots', tree_roots)]),
    'elf_paths': ('v5_elf', mk([(f'EV03_{i + 1:02d}_elf_path_piece_{i + 1:02d}', _mk_path(i)) for i in range(6)] + [
        ('LM01_01_world_tree_trunk_door', trunk_door), ('LM02_01_world_tree_falls', tree_falls)])),
    'town1': ('v5_town1', mk([('TW01_01_town1_hero_statue', statue)] + [(f'TW02_{i + 1:02d}_street_life_{i + 1:02d}', _mk_street(i)) for i in range(8)] + [
        (f'TW03_{i + 1:02d}_skull_avenue_set_{i + 1:02d}', _mk_avenue(i)) for i in range(4)])),
}
