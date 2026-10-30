"""vc module - Himalayan road kit and natural entrances: HM01 rope bridges, HM02 cantilever bridges, HM03 tunnel portals, HM04 tunnel lining,
HM05 cliff galleries, HM06 switchback walls, HM07 prayer-flag strings, HM08 cairn shrines, HM09 monastery outposts, NE01 village signs, NE02 entry boulders.
Original designs. No arches at entrances: signs and boulders mark a natural entrance. No glow (lanterns are plain meshes).
Long axis along X for bridges/walls, passage along Y for tunnels. Sizes in briefs are (x, height, depth) in Roblox axes.
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v5kit
from v5kit import Acc, polar, tang
import v4util

VC = {}
for _n, (_rgb, _m, _met, _r) in {
    'stone': ((128, 124, 120), 'Slate', 0.0, 0.95), 'stone2': ((150, 146, 140), 'Cobblestone', 0.0, 0.95), 'slate': ((84, 86, 96), 'Slate', 0.0, 0.9),
    'snow': ((240, 244, 250), 'Snow', 0.0, 0.7), 'ice': ((196, 226, 242), 'Ice', 0.0, 0.3), 'timber': ((112, 92, 70), 'Wood', 0.0, 0.9),
    'plank': ((134, 108, 80), 'WoodPlanks', 0.0, 0.9), 'rope': ((176, 150, 104), 'Fabric', 0.0, 1.0),
    'f_blue': ((60, 120, 200), 'Fabric', 0.0, 1.0), 'f_white': ((250, 250, 250), 'Fabric', 0.0, 1.0), 'f_red': ((200, 60, 50), 'Fabric', 0.0, 1.0),
    'f_green': ((60, 160, 90), 'Fabric', 0.0, 1.0), 'f_yellow': ((240, 200, 60), 'Fabric', 0.0, 1.0),
    'white': ((236, 232, 224), 'Concrete', 0.0, 0.9), 'red': ((128, 56, 46), 'Wood', 0.0, 0.85), 'gold': ((200, 164, 84), 'Metal', 0.8, 0.35),
    'iron': ((58, 58, 64), 'Metal', 0.6, 0.6), 'moss': ((92, 124, 72), 'Grass', 0.0, 1.0), 'sand': ((214, 184, 140), 'Sandstone', 0.0, 0.95),
    'basalt': ((62, 62, 70), 'Basalt', 0.0, 0.9), 'clay': ((190, 122, 88), 'Brick', 0.0, 0.9), 'wood': ((118, 86, 56), 'Wood', 0.0, 0.9),
    'leaf': ((88, 128, 66), 'Grass', 0.0, 1.0), 'dstone': ((72, 72, 80), 'Granite', 0.0, 0.92), 'rust': ((150, 92, 62), 'CorrodedMetal', 0.4, 0.8),
}.items():
    kitlib.PAL['vc_' + _n] = (_rgb, _m, _met, _r, 0)
    VC[_n] = 'vc_' + _n
FLAGS = [VC[k] for k in ('f_blue', 'f_white', 'f_red', 'f_green', 'f_yellow')]
ROCKS = [VC['stone'], VC['stone2'], VC['slate']]


def _cable(A, x0, x1, y, zf, key, w=0.2, step=3.0):
    n = max(2, int(abs(x1 - x0) / step))
    prev = None
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        p = (x, y, zf(x))
        if prev:
            A.beam(prev, p, w, w, key)
        prev = p


def _flag_run(A, x0, x1, y, zf, every=2.6, seed=0, hang=1.0):
    rnd = random.Random(seed)
    n = int(abs(x1 - x0) / every)
    for k in range(1, n):
        x = x0 + (x1 - x0) * k / n
        A.box((1.2, 0.06, 1.6), (x, y, zf(x) - hang), FLAGS[k % 5], (rnd.uniform(-6, 6), 0, rnd.uniform(-5, 5)))


# ------------------------------------------------------------------ HM01 rope suspension bridges
def _rope_bridge(span, seed, snow=False):
    reset()
    A = Acc()
    rnd = random.Random(seed)
    half, anchor = span / 2.0, 6.0
    zd = lambda x: 5.0 - 2.4 * (1.0 - (x / half) ** 2)
    xe = half + 1.5
    zc = lambda x: (zd(0) + 3.6) + (11.8 - (zd(0) + 3.6)) * (x / xe) ** 2
    for sg in (-1, 1):                                                                       # stone anchor towers
        cx = sg * (half + anchor / 2.0)
        A.box((anchor, 9.6, 3.0), (cx, 0, 1.5), VC['stone'])
        A.box((anchor - 1.0, 8.6, 6.0), (cx, 0, 6.0), VC['stone2'])
        A.box((anchor, 9.4, 0.9), (cx, 0, 9.45), VC['slate'])
        for y in (-3.6, 3.6):
            A.box((1.2, 1.2, 2.4), (sg * (half + 1.5), y, 11.1), VC['timber'])
            A.box((1.6, 1.6, 0.3), (sg * (half + 1.5), y, 12.4), VC['slate'])
        A.cyl(0.16, 4.2, (cx + sg * 1.2, 0, 9.9), VC['timber'], verts=6)
        for k in range(4):
            A.box((0.04 + 1.1, 0.05, 0.9), (cx + sg * 1.2 + 0.6, 0, 13.0 - 0.0 - k * 0.0 - 0.0 + 0.0), FLAGS[k % 5]) if False else None
        if snow:
            A.chunk((anchor + 0.6, 10.0, 0.8), (cx, 0, 10.2), VC['snow'], jit=0.06, rnd=rnd)
            A.chunk((anchor - 0.4, 9.0, 0.6), (cx, 0, 3.2), VC['snow'], jit=0.06, rnd=rnd)
    x = -half
    prev = None
    while x <= half + 1e-6:                                                                  # plank deck, sagging in the middle
        slope = 4.8 * x / (half * half)
        A.box((0.92, 7.0, 0.34), (x, 0, zd(x) - 0.17), VC['plank'], (0, -math.degrees(math.atan(slope)), 0))
        if prev is not None:
            for y in (-3.2, 3.2):
                A.beam((prev, y, zd(prev) - 0.55), (x, y, zd(x) - 0.55), 0.45, 0.5, VC['timber'])
        prev = x
        x += 1.0
    for xx in range(int(-half), int(half) + 1, 4):                                           # cross beams, hangers, posts
        A.box((0.45, 7.8, 0.4), (xx, 0, zd(xx) - 0.55), VC['timber'])
        for y in (-3.6, 3.6):
            A.beam((xx, y, zd(xx)), (xx, y, zc(xx)), 0.13, 0.13, VC['rope'])
            A.box((0.3, 0.3, 2.0), (xx, y, zd(xx) + 1.0), VC['timber'])
    for y in (-3.6, 3.6):
        _cable(A, -xe, xe, y, zc, VC['rope'], 0.24)
        _cable(A, -half, half, y, lambda x: zd(x) + 2.0, VC['rope'], 0.16, 2.0)
        _flag_run(A, -half + 3, half - 3, y, zc, 2.8, seed + int(y * 10), 1.1)
    v4util.marker('mk_enda', (-half, 0, zd(-half) + 0.2))
    v4util.marker('mk_endb', (half, 0, zd(half) + 0.2))
    v4util.marker('mk_deck', (0, 0, zd(0) + 0.1))
    A.to_scene()
    return finalize('rope_suspension_bridge', 25)


def rope_bridge_1():
    return _rope_bridge(60.0, 1)


def rope_bridge_2():
    return _rope_bridge(90.0, 2, True)


def rope_bridge_3():
    return _rope_bridge(116.0, 3, True)


# ------------------------------------------------------------------ HM03 tunnel portals, HM04 tunnel lining
def _portal(var, seed):
    reset()
    A = Acc()
    rnd = random.Random(seed)
    W, D, H, ow, oh = 30.0, 17.0, 24.0, 14.0, 16.0
    for sg in (-1, 1):                                                                       # rock piers beside the opening
        for k in range(8):
            A.chunk((rnd.uniform(7.0, 8.4), D * rnd.uniform(0.85, 1.0), 3.4), (sg * (11.2 + rnd.uniform(-0.3, 0.4)), rnd.uniform(-0.8, 0.8), 1.6 + 3.0 * k),
                    ROCKS[rnd.randrange(3)], (0, 0, 0), 0.1, rnd, (0.94, 0.96))
    for k in range(6):                                                                       # rock mass over the opening
        A.chunk((5.8, D * rnd.uniform(0.9, 1.0), 7.4), (-12.5 + k * 5.0, rnd.uniform(-0.6, 0.6), oh + 4.3 + rnd.uniform(-0.2, 0.4)),
                ROCKS[rnd.randrange(3)], (0, 0, 0), 0.08, rnd, (0.95, 0.95))
    A.box((ow, D, 0.4), (0, 0, 0.2), VC['slate'])                                            # lined passage
    for sg in (-1, 1):
        A.box((0.7, D, oh), (sg * (ow / 2 + 0.35), 0, oh / 2), VC['slate'])
    A.box((ow + 1.4, D, 0.8), (0, 0, oh + 0.4), VC['slate'])
    yf = -D / 2 + 0.3
    for sg in (-1, 1):                                                                       # rectangular timber frame (no arch)
        A.box((1.5, 1.5, oh + 0.4), (sg * (ow / 2 + 0.75), yf, (oh + 0.4) / 2), VC['timber'])
        A.beam((sg * (ow / 2 + 0.75), yf - 0.2, oh - 3.6), (sg * (ow / 2 - 2.6), yf - 0.2, oh), 0.6, 0.6, VC['timber'])
    A.box((ow + 3.4, 1.7, 1.7), (0, yf, oh + 0.85), VC['timber'])
    if var == 2:                                                                             # snow-capped
        for k in range(6):
            A.chunk((5.6, D * 0.9, 1.4), (-12.5 + k * 5.0, 0, H + 0.3), VC['snow'], (0, 0, 0), 0.08, rnd)
        for sg in (-1, 1):
            A.chunk((7.0, D * 0.85, 1.0), (sg * 11.2, 0, 13.2), VC['snow'], (0, 0, 0), 0.08, rnd)
        for k in range(9):
            x = -ow / 2 + 1.0 + k * (ow - 2.0) / 8
            A.cyl(0.16, rnd.uniform(1.2, 2.6), (x, yf - 0.5, oh - 0.2), VC['ice'], verts=5, r2=0.0, rot=(180, 0, 0))
    if var == 3:                                                                             # heavy timber front with cross bracing and flags
        A.box((W - 3.0, 0.9, H - oh - 2.0), (0, yf - 0.6, (oh + 1.7 + H) / 2 - 0.2), VC['plank'])
        for sg in (-1, 1):
            A.beam((sg * (W / 2 - 2.5), yf - 1.2, oh + 2.0), (0, yf - 1.2, H - 0.5), 0.7, 0.7, VC['timber'])
        A.box((ow + 5.0, 1.2, 1.2), (0, yf - 0.8, oh + 2.4), VC['red'])
        for sg in (-1, 1):
            A.cyl(0.18, 4.0, (sg * (W / 2 - 1.5), yf - 0.4, H - 0.4), VC['timber'], verts=6)
        zf = lambda x: H + 3.0 - 1.6 * (1.0 - (x / (W / 2 - 1.5)) ** 2)
        _cable(A, -(W / 2 - 1.5), W / 2 - 1.5, yf - 0.4, zf, VC['rope'], 0.12, 2.0)
        _flag_run(A, -(W / 2 - 1.5), W / 2 - 1.5, yf - 0.4, zf, 2.0, seed, 0.9)
        for sg in (-1, 1):
            A.beam((sg * (ow / 2 + 1.6), yf - 0.4, 10.5), (sg * (ow / 2 + 1.6), yf - 1.8, 10.5), 0.2, 0.2, VC['iron'])
            A.cyl(0.45, 0.9, (sg * (ow / 2 + 1.6), yf - 1.8, 9.5), VC['gold'], verts=8)
    v4util.marker('mk_door', (0, -D / 2, 0.3))
    A.to_scene()
    return finalize('tunnel_portal', 25)


def portal_1():
    return _portal(1, 11)


def portal_2():
    return _portal(2, 12)


def portal_3():
    return _portal(3, 13)


def _lining(bend):
    reset()
    A = Acc()
    rnd = random.Random(21 + bend)
    ow, oh = 14.0, 16.0
    if not bend:
        L = 24.0
        for sg in (-1, 1):
            for k in range(6):
                A.chunk((4.6, L / 6.0 * 1.15, 19.5), (sg * 9.7, -L / 2 + (k + 0.5) * L / 6.0, 9.75), ROCKS[rnd.randrange(3)], (0, 0, 0), 0.07, rnd)
            A.box((0.7, L, oh), (sg * (ow / 2 + 0.35), 0, oh / 2), VC['slate'])
        for k in range(4):
            A.chunk((ow + 8.0, L / 4.0 * 1.15, 4.4), (0, -L / 2 + (k + 0.5) * L / 4.0, oh + 2.4), ROCKS[rnd.randrange(3)], (0, 0, 0), 0.06, rnd)
        A.box((ow + 1.4, L, 0.8), (0, 0, oh + 0.4), VC['slate'])
        A.box((ow, L, 0.4), (0, 0, 0.2), VC['slate'])
        for yy in (-8.0, 0.0, 8.0):                                                          # timber ribs every 8 studs
            for sg in (-1, 1):
                A.box((0.9, 0.9, oh), (sg * (ow / 2 - 0.3), yy, oh / 2), VC['timber'])
                A.beam((sg * (ow / 2 - 0.3), yy, oh - 3.0), (sg * (ow / 2 - 3.0), yy, oh), 0.5, 0.5, VC['timber'])
            A.box((ow, 0.9, 0.9), (0, yy, oh - 0.45), VC['timber'])
        for yy in (-4.0, 4.0):                                                               # lantern brackets (warm, unlit)
            for sg in (-1, 1):
                A.beam((sg * (ow / 2 - 0.2), yy, 11.0), (sg * (ow / 2 - 1.5), yy, 11.4), 0.18, 0.18, VC['iron'])
                A.cyl(0.5, 0.9, (sg * (ow / 2 - 1.5), yy, 10.2), VC['gold'], verts=8)
                A.cyl(0.62, 0.2, (sg * (ow / 2 - 1.5), yy, 11.1), VC['iron'], verts=8)
        v4util.marker('mk_door', (0, -L / 2, 0.3))
    else:
        R = 40.0
        loc = (-R, 0, 0)
        sw = lambda poly, key: A.sweep(poly, 0, 30, 5, key, loc=loc)
        sw([(R - 11.0, 0), (R - 7.0, 0), (R - 7.0, 19.6), (R - 11.0, 19.6)], VC['stone'])
        sw([(R + 7.0, 0), (R + 11.0, 0), (R + 11.0, 19.6), (R + 7.0, 19.6)], VC['stone2'])
        sw([(R - 11.0, oh), (R + 11.0, oh), (R + 11.0, 19.6), (R - 11.0, 19.6)], VC['stone'])
        sw([(R - 7.0, 0), (R + 7.0, 0), (R + 7.0, 0.4), (R - 7.0, 0.4)], VC['slate'])
        sw([(R - 7.7, 0.4), (R - 7.0, 0.4), (R - 7.0, oh), (R - 7.7, oh)], VC['slate'])
        sw([(R + 7.0, 0.4), (R + 7.7, 0.4), (R + 7.7, oh), (R + 7.0, oh)], VC['slate'])
        for a in (4.0, 15.0, 26.0):
            ar = math.radians(a)
            for sg in (-1, 1):
                r = R + sg * (ow / 2 - 0.3)
                A.box((0.9, 0.9, oh), (-R + r * math.cos(ar), r * math.sin(ar), oh / 2), VC['timber'], (0, 0, a))
            A.box((0.9, ow, 0.9), (-R + R * math.cos(ar), R * math.sin(ar), oh - 0.45), VC['timber'], (0, 0, a))
        for a in (9.0, 21.0):
            ar = math.radians(a)
            for sg in (-1, 1):
                r = R + sg * (ow / 2 - 1.4)
                A.cyl(0.5, 0.9, (-R + r * math.cos(ar), r * math.sin(ar), 10.2), VC['gold'], verts=8)
        v4util.marker('mk_door', (0, 0, 0.3))
    A.to_scene()
    return finalize('tunnel_lining', 25)


def lining_1():
    return _lining(0)


def lining_2():
    return _lining(1)


# ------------------------------------------------------------------ NE01 village signs (no arch, no gate)
def _sign(kind):
    reset()
    A = Acc()
    rnd = random.Random(40 + len(kind))
    if kind == 'town1':                                                                      # dark stone slab with a carved jaw and an iron bracket
        A.chunk((9.0, 3.4, 1.4), (0, 0, 0.7), VC['dstone'], jit=0.05, rnd=rnd)
        A.chunk((8.0, 2.6, 8.4), (0, 0, 5.6), VC['dstone'], jit=0.04, rnd=rnd, taper=(0.95, 0.9))
        A.box((6.4, 0.5, 3.4), (0, -1.45, 6.6), VC['stone'])
        for k in range(7):
            A.box((0.55, 0.3, 1.0 + (k % 2) * 0.35), (-3.0 + k, -1.8, 5.2), VC['white'])
            A.box((0.55, 0.3, 0.9 + ((k + 1) % 2) * 0.35), (-3.0 + k, -1.8, 4.1), VC['white'])
        A.box((8.0, 0.5, 0.45), (0, -1.9, 9.8), VC['iron'])
        for sx in (-3.2, 3.2):
            A.box((0.35, 0.35, 1.3), (sx, -1.9, 9.4), VC['iron'])
        A.beam((3.6, -1.6, 9.8), (6.0, -1.6, 13.0), 0.35, 0.35, VC['iron'])
        A.box((2.6, 0.3, 1.8), (6.0, -1.6, 12.0), VC['iron'])
    elif kind == 'elf':                                                                      # living-wood board on a root post
        for k in range(5):
            x, y, _ = polar(1.3, k * 72.0 + 20.0)
            A.beam((x * 1.9, y * 1.9, 0.2), (x * 0.3, y * 0.3, 4.0), 0.9 - 0.1 * (k % 2), 0.9, VC['wood'])
        A.cyl(1.1, 11.0, (0, 0, 2.0), VC['wood'], verts=10, r2=0.8)
        A.box((9.4, 0.9, 5.4), (0, -1.0, 11.0), VC['plank'])
        A.chunk((9.8, 1.2, 0.9), (0, -1.0, 13.9), VC['wood'], jit=0.06, rnd=rnd)
        A.box((9.8, 1.2, 0.9), (0, -1.0, 8.2), VC['wood'])
        for k in range(5):
            x = -3.2 + k * 1.6
            A.ball(0.55, (x, -1.65, 11.0 + (0.9 if k % 2 else -0.5)), VC['leaf'], segs=6, rings=4, scale=(1.0, 0.3, 1.5))
        A.beam((-3.6, -1.7, 11.0), (3.6, -1.7, 11.0), 0.2, 0.2, VC['leaf'])
    elif kind == 'alpine':                                                                   # log post, snow cap, board and a small bell
        A.cyl(0.9, 14.0, (0, 0, 0.0), VC['timber'], verts=10, r2=0.8)
        A.chunk((2.6, 2.6, 1.0), (0, 0, 14.4), VC['snow'], jit=0.08, rnd=rnd)
        A.box((9.0, 0.9, 4.6), (0, -1.1, 10.4), VC['plank'])
        A.chunk((9.4, 1.1, 0.9), (0, -1.1, 12.9), VC['snow'], jit=0.06, rnd=rnd)
        A.box((0.5, 0.5, 5.0), (-4.4, -1.1, 10.4), VC['timber'])
        A.box((0.5, 0.5, 5.0), (4.4, -1.1, 10.4), VC['timber'])
        A.beam((0, -0.4, 14.0), (3.8, -0.4, 14.0), 0.3, 0.3, VC['timber'])
        A.beam((3.8, -0.4, 14.0), (3.8, -0.4, 13.0), 0.1, 0.1, VC['rope'])
        A.cyl(0.55, 0.9, (3.8, -0.4, 12.3), VC['gold'], verts=8, r2=0.2, rot=(0, 0, 0))
        A.box((6.2, 0.3, 2.4), (0, -1.65, 10.4), VC['white'])
        for k in range(4):
            A.box((0.3, 0.2, 1.4), (-2.2 + k * 1.5, -1.8, 10.4), VC['slate'])
        A.chunk((4.6, 4.0, 1.2), (0, 0, 0.5), VC['snow'], jit=0.1, rnd=rnd)
    elif kind == 'rusty':                                                                    # salvage plate on a sandstone block
        A.chunk((8.6, 3.4, 8.0), (0, 0, 4.0), VC['sand'], jit=0.06, rnd=rnd, taper=(0.92, 0.9))
        A.chunk((6.6, 2.6, 5.0), (0, 0, 10.2), VC['sand'], jit=0.06, rnd=rnd, taper=(0.9, 0.9))
        A.box((6.8, 0.4, 4.6), (0, -1.5, 10.0), VC['rust'], (0, 0, 0))
        A.box((7.2, 0.3, 0.5), (0, -1.75, 12.4), VC['iron'])
        A.box((7.2, 0.3, 0.5), (0, -1.75, 7.6), VC['iron'])
        for sx in (-3.0, 3.0):
            for sz in (8.2, 11.8):
                A.ball(0.28, (sx, -1.8, sz), VC['iron'], segs=6, rings=4)
        A.box((4.2, 0.2, 2.2), (0, -1.78, 10.0), VC['stone2'])
        A.box((1.8, 0.2, 0.5), (-1.4, -1.9, 10.4), VC['rust'])
        A.chunk((1.6, 1.4, 0.9), (-3.4, -1.6, 0.4), VC['sand'], jit=0.1, rnd=rnd)
    elif kind == 'harbour':                                                                  # whitewashed board on two posts with an anchor and rope
        for sx in (-3.8, 3.8):
            A.cyl(0.55, 14.0, (sx, 0, 0), VC['timber'], verts=8)
            A.ball(0.62, (sx, 0, 14.3), VC['iron'], segs=6, rings=4)
        A.box((9.2, 0.8, 5.6), (0, -0.8, 10.0), VC['white'])
        A.box((9.6, 1.0, 0.5), (0, -0.8, 12.9), VC['timber'])
        A.box((9.6, 1.0, 0.5), (0, -0.8, 7.1), VC['timber'])
        A.box((0.45, 0.4, 4.2), (0, -1.3, 10.0), VC['iron'])                                 # anchor
        A.box((2.8, 0.4, 0.45), (0, -1.3, 11.3), VC['iron'])
        A.sweep([(1.1, -0.2), (1.6, -0.2), (1.6, 0.2), (1.1, 0.2)], 200, 340, 8, VC['iron'], loc=(0, -1.3, 8.6), rot=(90, 0, 0))
        for sx in (-6.0, 6.0):
            A.box((0.14, 0.14, 0.14), (sx, 0, 0), VC['rope']) if False else None
        A.beam((-3.8, -0.6, 7.6), (-1.6, -1.3, 8.2), 0.18, 0.18, VC['rope'])
        A.beam((-1.6, -1.3, 8.2), (1.6, -1.3, 8.2), 0.18, 0.18, VC['rope'])
        A.beam((1.6, -1.3, 8.2), (3.8, -0.6, 7.6), 0.18, 0.18, VC['rope'])
        A.chunk((2.6, 2.6, 0.8), (-3.8, 0, 0.4), VC['stone2'], jit=0.08, rnd=rnd)
        A.chunk((2.6, 2.6, 0.8), (3.8, 0, 0.4), VC['stone2'], jit=0.08, rnd=rnd)
    else:                                                                                    # desert: painted clay slab on a timber beam
        for sx in (-4.2, 4.2):
            A.cyl(0.6, 13.0, (sx, 0, 0), VC['timber'], verts=8)
        A.box((10.0, 1.0, 0.8), (0, 0, 13.4), VC['timber'])
        A.box((8.2, 1.4, 6.0), (0, 0, 9.4), VC['clay'])
        A.box((8.6, 1.6, 0.7), (0, 0, 12.6), VC['sand'])
        A.box((8.6, 1.6, 0.7), (0, 0, 6.4), VC['sand'])
        for k in range(5):
            A.box((1.3, 0.12, 1.3), (-3.2 + k * 1.6, -0.75, 9.4), (VC['f_blue'], VC['f_yellow'], VC['f_red'], VC['f_green'], VC['f_white'])[k])
        A.box((6.6, 0.12, 0.35), (0, -0.75, 11.4), VC['white'])
        A.box((6.6, 0.12, 0.35), (0, -0.75, 7.4), VC['white'])
        A.chunk((2.4, 2.4, 0.8), (-4.2, 0, 0.4), VC['sand'], jit=0.08, rnd=rnd)
        A.chunk((2.4, 2.4, 0.8), (4.2, 0, 0.4), VC['sand'], jit=0.08, rnd=rnd)
    A.to_scene()
    ob = finalize('village_sign', 25)
    return v5kit.fit(ob, w=10.4 if kind in ('town1', 'desert', 'harbour') else None, h=17.6)


def sign_1():
    return _sign('town1')


def sign_2():
    return _sign('elf')


def sign_3():
    return _sign('alpine')


def sign_4():
    return _sign('rusty')


def sign_5():
    return _sign('harbour')


def sign_6():
    return _sign('desert')


# ------------------------------------------------------------------ HM02 cantilever bridges
def _cantilever(span, seed):
    reset()
    A = Acc()
    rnd = random.Random(seed)
    half = span / 2.0
    zdk = 6.0
    for sg in (-1, 1):                                                                       # stone abutments
        A.chunk((8.0, 8.4, 6.0), (sg * (half + 3.2), 0, 3.0), VC['stone'], jit=0.05, rnd=rnd)
        A.chunk((6.0, 8.0, 1.2), (sg * (half + 3.0), 0, 6.4), VC['stone2'], jit=0.05, rnd=rnd)
    reach = [0.2, 0.34, 0.46]
    for sg in (-1, 1):                                                                       # three layers of projecting log beams
        for k, rch in enumerate(reach):
            xe = sg * (half - span * rch)
            xs = sg * (half + 2.0)
            for y in (-2.6, 2.6):
                A.beam((xs, y, zdk - 2.4 + k * 0.62), (xe, y, zdk - 2.4 + k * 0.62), 0.7, 0.55, VC['timber'])
        for y in (-2.6, 2.6):
            A.beam((sg * (half + 2.0), y, zdk - 0.5), (sg * (half - span * 0.46), y, zdk - 0.5), 0.8, 0.5, VC['timber'])
    for y in (-2.6, 2.6):                                                                    # central girders
        A.beam((-half + span * 0.46, y, zdk - 0.5), (half - span * 0.46, y, zdk - 0.5), 0.8, 0.6, VC['timber'])
    x = -half - 2.0
    while x <= half + 2.0:                                                                   # deck planks
        A.box((0.9, 6.4, 0.3), (x, 0, zdk), VC['plank'])
        x += 0.95
    for sg in (-1, 1):                                                                       # roof posts, rails and a shingle gable roof over the deck
        for k in range(int(span / 7.0) + 1):
            x = sg * (half - 1.0 - k * 6.0) if sg > 0 else -half + 1.0 + k * 6.0
            if abs(x) > half + 1.5:
                continue
            for y in (-2.9, 2.9):
                A.box((0.55, 0.55, 5.6), (x, y, zdk + 2.8), VC['timber'])
        A.beam((sg * (half + 1.8), -2.9, zdk + 1.1), (sg * (half - 3.0), -2.9, zdk + 1.1), 0.3, 0.3, VC['timber'])
    for y in (-2.9, 2.9):
        A.beam((-half - 1.5, y, zdk + 5.7), (half + 1.5, y, zdk + 5.7), 0.7, 0.5, VC['timber'])
        A.beam((-half - 1.5, y, zdk + 1.1), (half + 1.5, y, zdk + 1.1), 0.3, 0.3, VC['timber'])
    A.gable(8.4, span + 4.4, 3.0, (0, 0, zdk + 5.7), VC['slate'], (0, 0, 90))
    A.box((span + 4.6, 0.5, 0.4), (0, 0, zdk + 8.7), VC['timber'])
    for k in range(5):
        A.box((0.1, 0.1, 0.1), (0, 0, 0), VC['rope']) if False else None
    v4util.marker('mk_enda', (-half - 2.0, 0, zdk + 0.2))
    v4util.marker('mk_endb', (half + 2.0, 0, zdk + 0.2))
    v4util.marker('mk_deck', (0, 0, zdk + 0.2))
    A.to_scene()
    return finalize('timber_cantilever_bridge', 25)


def cantilever_1():
    return _cantilever(28.0, 61)


def cantilever_2():
    return _cantilever(40.0, 62)


# ------------------------------------------------------------------ HM05 cliff galleries, HM06 switchback walls
def _gallery(var):
    reset()
    A = Acc()
    rnd = random.Random(70 + var)
    L = 40.0
    A.box((L, 12.0, 1.0), (0, -1.0, 0.5), VC['stone2'])
    for k in range(8):                                                                       # cliff face behind
        A.chunk((6.0, 6.0, 22.0), (-17.5 + k * 5.0, 4.4 + rnd.uniform(-0.5, 0.5), 11.0), ROCKS[rnd.randrange(3)], (0, 0, 0), 0.09, rnd, (0.94, 0.94))
    for k in range(8):                                                                       # rock roof over the road
        A.chunk((5.8, 9.4, 4.6), (-17.5 + k * 5.0, 0.6, 14.2 + rnd.uniform(-0.2, 0.5)), ROCKS[rnd.randrange(3)], (0, 0, 0), 0.08, rnd, (0.93, 0.93))
    for k in range(5):                                                                       # timber props on the open side
        x = -17.0 + k * 8.5
        A.box((0.9, 0.9, 12.6), (x, -4.6, 7.3), VC['timber'])
        A.beam((x, -4.6, 9.0), (x, -0.8, 12.4), 0.55, 0.55, VC['timber'])
        A.box((1.6, 1.6, 0.5), (x, -4.6, 1.2), VC['stone'])
    A.box((L - 2.0, 1.0, 1.0), (0, -4.6, 13.2), VC['timber'])
    A.box((L - 2.0, 0.35, 0.35), (0, -4.6, 3.6), VC['timber'])
    A.box((L - 2.0, 0.35, 0.35), (0, -4.6, 5.2), VC['timber'])
    if var == 2:
        for k in range(8):
            A.chunk((5.6, 9.0, 1.2), (-17.5 + k * 5.0, 0.6, 16.9), VC['snow'], jit=0.07, rnd=rnd)
        for x in (-12.0, 12.0):
            A.beam((x, -4.9, 12.8), (x, -4.9, 10.8), 0.12, 0.12, VC['rope'])
            A.cyl(0.4, 0.8, (x, -4.9, 10.0), VC['gold'], verts=8)
    v4util.marker('mk_enda', (-L / 2, -1.0, 1.2))
    v4util.marker('mk_endb', (L / 2, -1.0, 1.2))
    v4util.marker('mk_deck', (0, -1.0, 1.2))
    A.to_scene()
    return finalize('cliff_gallery', 25)


def gallery_1():
    return _gallery(1)


def gallery_2():
    return _gallery(2)


def _switchback(var):
    reset()
    A = Acc()
    rnd = random.Random(80 + var)
    if var == 1:                                                                             # straight retaining wall, battered face
        for k in range(10):
            for z in range(4):
                A.chunk((3.2, 4.6 - z * 0.25, 2.1), (-13.5 + k * 3.0, 0, 1.0 + z * 2.0), ROCKS[(k + z) % 3], (0, 0, 0), 0.07, rnd, (0.97, 0.9))
        A.box((30.4, 5.0, 0.7), (0, 0, 9.0), VC['stone2'])
        for k in range(8):
            A.box((0.9, 0.9, 0.5), (-12.6 + k * 3.6, -2.2, 8.7), VC['timber'])
    elif var == 2:                                                                           # 180-degree hairpin wall
        R = 8.8
        for z in range(4):
            A.sweep([(R - 2.4 + z * 0.2, 1.8 + z * 2.0 - 1.0), (R + 2.4 - z * 0.2, 1.8 + z * 2.0 - 1.0), (R + 2.4 - z * 0.2, 1.8 + z * 2.0 + 1.0), (R - 2.4 + z * 0.2, 1.8 + z * 2.0 + 1.0)],
                    0, 180, 9, ROCKS[z % 3], loc=(0, 0, 0.0))
        A.sweep([(R - 2.9, 8.2), (R + 2.9, 8.2), (R + 2.9, 8.9), (R - 2.9, 8.9)], 0, 180, 9, VC['stone2'])
        for k in range(7):
            x, y, _ = polar(R + 3.0, k * 30.0)
            A.box((0.6, 0.6, 1.4), (x, y, 9.6), VC['timber'], (0, 0, k * 30.0))
        for a in (-1, 1):                                                                    # straight legs so the hairpin is 30 wide
            A.chunk((4.8, 8.0, 8.2), (a * R, -4.0, 4.1), VC['stone2'], jit=0.05, rnd=rnd)
            A.box((5.2, 8.0, 0.7), (a * R, -4.0, 8.55), VC['stone2'])
    else:                                                                                    # wall with a short stair and a parapet
        for k in range(10):
            for z in range(3):
                A.chunk((3.2, 4.4, 2.2), (-13.5 + k * 3.0, 0, 1.1 + z * 2.1), ROCKS[(k + z) % 3], (0, 0, 0), 0.07, rnd, (0.97, 0.92))
        for s in range(8):
            A.box((2.0, 4.0, 0.6 * (s + 1)), (-14.0 + s * 2.0, -2.4, 0.3 * (s + 1)), VC['stone2'])
        A.box((14.0, 0.7, 1.4), (7.0, 2.0, 8.0), VC['stone2'])
        for k in range(6):
            A.box((0.6, 0.6, 1.7), (1.5 + k * 2.1, 2.0, 7.3), VC['stone'])
        A.box((30.2, 4.6, 0.7), (0, 0, 6.6), VC['stone2'])
    v4util.marker('mk_enda', (-14.0, 0, 0.5))
    v4util.marker('mk_endb', (14.0, 0, 0.5))
    A.to_scene()
    return v5kit.fit(finalize('switchback_wall', 25), h=12.0, w=(28.0 if var == 2 else None))


def switchback_1():
    return _switchback(1)


def switchback_2():
    return _switchback(2)


def switchback_3():
    return _switchback(3)


# ------------------------------------------------------------------ HM07 prayer flag strings, HM08 cairn shrines
def _flag_string(var):
    reset()
    A = Acc()
    rnd = random.Random(90 + var)
    half = 18.5
    for sg in (-1, 1):
        A.chunk((2.6, 2.2, 1.0), (sg * half, 0, 0.5), VC['stone'], jit=0.08, rnd=rnd)
        A.cyl(0.32, 11.0, (sg * half, 0, 0.8), VC['timber'], verts=8, r2=0.24)
        A.ball(0.42, (sg * half, 0, 12.0), VC['gold'], segs=6, rings=4)
    nstr = 2 if var == 2 else 1
    for s in range(nstr):
        z_end = 10.4 - s * 1.7
        sag = 2.2 + 0.7 * s
        zf = lambda x, z_end=z_end, sag=sag: z_end - sag * (1.0 - (x / half) ** 2)
        _cable(A, -half, half, 0.0, zf, VC['rope'], 0.12, 2.5)
        every = 1.5 if var == 3 else 2.3
        n = int(2 * half / every)
        for k in range(1, n):
            x = -half + 2 * half * k / n
            col = FLAGS[(k + s * 2) % 5] if var != 4 else (VC['f_white'] if k % 3 else VC['ice'])
            A.box((1.1, 0.05, 1.5 if var != 3 else 1.1), (x, 0, zf(x) - 0.9), col, (rnd.uniform(-5, 5), 0, rnd.uniform(-4, 4)))
    if var == 4:
        for k in range(10):
            x = rnd.uniform(-half + 3, half - 3)
            A.cyl(0.1, rnd.uniform(0.8, 1.6), (x, 0, 8.6), VC['ice'], verts=5, r2=0.0, rot=(180, 0, 0))
    A.to_scene()
    return finalize('prayer_flag_string', 30)


def flags_1():
    return _flag_string(1)


def flags_2():
    return _flag_string(2)


def flags_3():
    return _flag_string(3)


def flags_4():
    return _flag_string(4)


def _shrine(var):
    reset()
    A = Acc()
    rnd = random.Random(100 + var)
    if var == 1:                                                                             # tall stacked cairn with flags
        z = 0.0
        for lv in range(14):
            r = 5.6 * (1.0 - lv / 16.0)
            for k in range(max(1, 5 - lv // 3)):
                x, y, _ = polar(r * 0.35 if lv else 0, rnd.uniform(0, 360))
                h = rnd.uniform(0.7, 1.0)
                A.chunk((rnd.uniform(2.4, 3.8) * (1 - lv * 0.045), rnd.uniform(2.2, 3.4) * (1 - lv * 0.045), h), (x, y, z + h / 2), ROCKS[rnd.randrange(3)], (0, 0, rnd.uniform(0, 90)), 0.1, rnd)
            z += 0.8
        A.cyl(0.14, 3.0, (0, 0, z), VC['timber'], verts=6)
        for k in range(4):
            A.box((1.6, 0.05, 1.1), (0.9, 0, z + 2.2 - k * 0.35), FLAGS[k % 5], (0, 0, 0))
    elif var == 2:                                                                           # small stone shrine with a niche, statue and timber roof
        A.chunk((9.0, 7.0, 1.0), (0, 0, 0.5), VC['stone2'], jit=0.04, rnd=rnd)
        A.box((6.0, 5.0, 5.6), (0, 0, 3.8), VC['stone'])
        A.box((3.0, 0.8, 3.0), (0, -2.55, 3.8), VC['slate'])
        A.cyl(0.55, 1.0, (0, -2.7, 2.7), VC['gold'], verts=8, r2=0.4)
        A.ball(0.42, (0, -2.7, 3.9), VC['gold'], segs=8, rings=5)
        A.gable(8.6, 7.0, 2.8, (0, 0, 6.6), VC['red'], (0, 0, 90))
        A.box((8.8, 0.5, 0.5), (0, 0, 6.6), VC['timber'])
        A.cyl(0.14, 2.0, (0, 0, 9.4), VC['gold'], verts=6, r2=0.0)
    elif var == 3:                                                                           # prayer wheel shrine
        A.chunk((8.0, 8.0, 1.0), (0, 0, 0.5), VC['stone2'], jit=0.04, rnd=rnd)
        for sx in (-3.2, 3.2):
            A.box((0.7, 0.7, 7.2), (sx, 0, 4.6), VC['red'])
        A.cyl(2.4, 5.0, (0, 0, 2.0), VC['red'], verts=16)
        A.sweep([(2.3, 0.0), (2.6, 0.0), (2.6, 0.6), (2.3, 0.6)], 0, 360, 16, VC['gold'], loc=(0, 0, 2.2))
        A.sweep([(2.3, 0.0), (2.6, 0.0), (2.6, 0.6), (2.3, 0.6)], 0, 360, 16, VC['gold'], loc=(0, 0, 6.2))
        A.cyl(0.3, 9.0, (0, 0, 1.2), VC['gold'], verts=6)
        A.gable(9.0, 8.0, 2.6, (0, 0, 8.2), VC['slate'], (0, 0, 90))
        for k in range(8):
            x, y, _ = polar(2.45, k * 45.0)
            A.box((0.12, 0.5, 2.4), (x, y, 4.6), VC['gold'], (0, 0, k * 45.0))
    else:                                                                                    # bell frame on a stone base
        A.chunk((10.0, 7.0, 1.4), (0, 0, 0.7), VC['stone2'], jit=0.04, rnd=rnd)
        for sx in (-3.6, 3.6):
            A.box((0.9, 0.9, 8.8), (sx, 0, 5.4), VC['red'])
            A.beam((sx, 0, 8.0), (sx * 0.4, 0, 10.4), 0.6, 0.6, VC['red'])
        A.box((8.4, 1.0, 1.0), (0, 0, 10.0), VC['red'])
        A.gable(5.0, 10.0, 2.4, (0, 0, 10.5), VC['slate'], (0, 0, 90))
        A.revolve([(0.0, 7.0), (1.2, 6.9), (1.7, 5.6), (2.0, 4.6), (2.2, 4.2), (0.0, 4.2)], (0, 0, 2.2), VC['gold'], segs=14)
        A.beam((0, 0, 9.5), (0, 0, 9.0), 0.2, 0.2, VC['iron'])
    A.to_scene()
    return v5kit.fit(finalize('cairn_shrine', 25), w=(11.0 if var == 1 else 12.8), d=(11.0 if var == 1 else 12.0), h=12.4)


def shrine_1():
    return _shrine(1)


def shrine_2():
    return _shrine(2)


def shrine_3():
    return _shrine(3)


def shrine_4():
    return _shrine(4)


# ------------------------------------------------------------------ HM09 monastery outposts
def _roof_ornaments(A, x, y, z, w):
    A.box((w, 0.9, 0.5), (x, y, z), VC['gold'])
    for sg in (-1, 1):
        A.revolve([(0.9, 0.0), (0.9, 0.8), (0.4, 1.3), (0.0, 1.9)], (x + sg * (w / 2 - 1.0), y, z + 0.25), VC['gold'], segs=8)
    A.cyl(0.35, 1.2, (x, y, z + 0.25), VC['gold'], verts=8)


def _hall(var):
    reset()
    A = Acc()
    rnd = random.Random(110 + var)
    if var == 1:                                                                             # hall: tapering whitewashed walls, red band, flat roof with gold ornaments, pillared porch
        A.box((38.0, 28.0, 1.2), (0, 0, 0.6), VC['stone2'])
        A.frustum((34.0, 22.0), (31.0, 20.0), 14.0, (0, 2.0, 1.2), VC['white'])
        A.frustum((35.0, 23.0), (32.0, 21.0), 3.2, (0, 2.0, 15.2), VC['red'])
        A.box((34.0, 22.6, 0.9), (0, 2.0, 18.9), VC['slate'])
        A.frustum((24.0, 15.0), (21.0, 13.0), 5.0, (0, 2.0, 19.3), VC['white'])
        A.frustum((25.0, 16.0), (22.0, 14.0), 1.8, (0, 2.0, 24.3), VC['red'])
        A.box((25.0, 16.6, 0.8), (0, 2.0, 26.1), VC['slate'])
        _roof_ornaments(A, 0, 2.0, 26.9, 12.0)
        for k in range(5):                                                                   # porch pillars
            A.box((1.2, 1.2, 9.0), (-12.0 + k * 6.0, -11.0, 5.7), VC['red'])
            A.box((1.8, 1.8, 0.7), (-12.0 + k * 6.0, -11.0, 10.4), VC['gold'])
        A.box((30.0, 3.0, 0.9), (0, -11.0, 11.0), VC['red'])
        A.box((32.0, 5.0, 0.5), (0, -10.5, 11.7), VC['slate'])
        A.box((6.0, 1.0, 9.0), (0, -9.0, 5.7), VC['timber'])
        for sx in (-12.0, 12.0):
            for z in (7.0, 12.5):
                A.box((3.0, 0.5, 2.4), (sx, -9.1, z), VC['slate'])
                A.box((3.4, 0.5, 0.4), (sx, -9.2, z + 1.4), VC['red'])
        for k in range(3):
            A.box((9.0 - k * 2.0, 3.0, 0.5), (0, -14.0 + k * 0.0 + 0.0, 0.7 + k * 0.5), VC['stone2']) if False else None
        for st in range(3):
            A.box((14.0 - st * 2.0, 1.6, 0.4 * (st + 1)), (0, -13.4 + st * 1.4, 1.2 + 0.2 * (st + 1)), VC['stone'])
    elif var == 2:                                                                           # prayer-wheel house: octagon with a big central wheel
        A.box((34.0, 30.0, 1.2), (0, 0, 0.6), VC['stone2'])
        A.cyl(14.0, 12.0, (0, 0, 1.2), VC['white'], verts=8, r2=13.0)
        A.cyl(14.6, 2.4, (0, 0, 13.2), VC['red'], verts=8, r2=14.2)
        A.cyl(15.6, 1.0, (0, 0, 15.6), VC['slate'], verts=8)
        A.cyl(14.0, 5.0, (0, 0, 16.6), VC['gold'], verts=8, r2=0.0)
        A.cyl(0.5, 3.2, (0, 0, 21.6), VC['gold'], verts=8)
        A.ball(0.9, (0, 0, 25.0), VC['gold'], segs=8, rings=5)
        for k in range(8):
            a = k * 45.0 + 22.5
            x, y, _ = polar(14.2, a)
            if k != 6:
                for sz in (4.8, 9.0):
                    A.box((0.5, 3.2, 2.6), (x, y, sz), VC['slate'], (0, 0, a))
                    A.box((0.6, 3.6, 0.4), (x, y, sz + 1.5), VC['red'], (0, 0, a))
        A.cyl(4.2, 9.0, (0, 0, 1.4), VC['red'], verts=16)
        A.sweep([(4.1, 0.0), (4.5, 0.0), (4.5, 0.8), (4.1, 0.8)], 0, 360, 16, VC['gold'], loc=(0, 0, 4.0))
        A.sweep([(4.1, 0.0), (4.5, 0.0), (4.5, 0.8), (4.1, 0.8)], 0, 360, 16, VC['gold'], loc=(0, 0, 8.4))
        A.cyl(0.5, 14.0, (0, 0, 1.2), VC['gold'], verts=6)
        for k in range(10):
            x, y, _ = polar(8.0, k * 36.0)
            A.cyl(0.6, 2.2, (x, y, 1.4), VC['red'], verts=8)
            A.cyl(0.65, 0.3, (x, y, 2.4), VC['gold'], verts=8)
    elif var == 3:                                                                           # guest house: two storeys, wooden balcony, flat roof with parapet
        A.box((38.0, 28.0, 1.2), (0, 0, 0.6), VC['stone2'])
        A.frustum((32.0, 18.0), (30.0, 17.0), 10.0, (0, 2.0, 1.2), VC['white'])
        A.box((30.5, 17.5, 0.5), (0, 2.0, 11.4), VC['red'])
        A.frustum((30.0, 17.0), (28.0, 16.0), 9.0, (0, 2.0, 11.6), VC['white'])
        A.box((29.0, 17.6, 1.2), (0, 2.0, 21.2), VC['slate'])
        A.box((29.6, 18.2, 0.5), (0, 2.0, 22.0), VC['white'])
        for k in range(12):
            A.box((1.4, 0.7, 1.1), (-13.0 + k * 2.4, -6.7, 22.8), VC['white'])
        A.box((32.0, 5.0, 0.7), (0, -9.4, 11.0), VC['timber'])
        for k in range(9):
            A.box((0.35, 0.35, 2.8), (-14.5 + k * 3.6, -11.7, 12.6), VC['red'])
        A.box((32.0, 0.5, 0.5), (0, -11.7, 14.0), VC['red'])
        for k in range(5):
            A.box((0.7, 0.7, 9.4), (-14.0 + k * 7.0, -11.6, 5.9), VC['red'])
        for r in range(2):
            for k in range(6):
                A.box((2.2, 0.5, 3.0), (-11.0 + k * 4.4, -6.55, 5.4 + r * 10.0), VC['slate'])
                A.box((2.8, 0.5, 0.4), (-11.0 + k * 4.4, -6.65, 7.1 + r * 10.0), VC['red'])
        A.box((4.0, 0.6, 6.0), (0, -6.5, 4.2), VC['timber'])
        for st in range(3):
            A.box((12.0 - st * 2.0, 1.6, 0.4 * (st + 1)), (0, -13.6 + st * 1.2, 1.2 + 0.2 * (st + 1)), VC['stone'])
        for k in range(3):
            A.cyl(0.7, 1.6, (-10.0 + k * 10.0, 4.0, 22.5), VC['stone2'], verts=8)
    else:                                                                                    # bell shelter: open timber pavilion with a pagoda roof
        A.box((34.0, 30.0, 1.2), (0, 0, 0.6), VC['stone2'])
        A.frustum((22.0, 22.0), (20.0, 20.0), 1.6, (0, 0, 1.2), VC['stone'])
        for sx in (-8.0, 8.0):
            for sy in (-8.0, 8.0):
                A.box((1.4, 1.4, 14.0), (sx, sy, 9.8), VC['red'])
                A.box((2.2, 2.2, 0.8), (sx, sy, 3.2), VC['stone'])
        for z in (11.0, 15.6):
            A.box((18.0, 1.0, 1.0), (0, -8.0, z), VC['timber'])
            A.box((18.0, 1.0, 1.0), (0, 8.0, z), VC['timber'])
            A.box((1.0, 18.0, 1.0), (-8.0, 0, z), VC['timber'])
            A.box((1.0, 18.0, 1.0), (8.0, 0, z), VC['timber'])
        A.frustum((28.0, 28.0), (12.0, 12.0), 6.0, (0, 0, 16.4), VC['slate'])
        A.frustum((13.0, 13.0), (4.0, 4.0), 5.0, (0, 0, 22.6), VC['slate'])
        A.cyl(0.35, 4.0, (0, 0, 27.4), VC['gold'], verts=8)
        A.ball(0.7, (0, 0, 31.2), VC['gold'], segs=8, rings=5)
        A.revolve([(0.0, 10.0), (1.3, 9.9), (2.0, 8.3), (2.6, 6.6), (3.0, 5.4), (3.2, 4.8), (0.0, 4.8)], (0, 0, 3.0), VC['gold'], segs=16)
        A.beam((0, 0, 17.0), (0, 0, 14.0), 0.5, 0.5, VC['iron'])
        A.beam((0, -2.0, 6.5), (0, -9.0, 9.5), 0.5, 0.5, VC['timber'])
        A.cyl(0.8, 3.0, (0, -9.0, 9.2), VC['timber'], verts=8, rot=(90, 0, 0))
        for k in range(6):
            A.box((1.0, 0.05, 1.4), (-6.0 + k * 2.4, -8.0, 14.0), FLAGS[k % 5])
    v4util.marker('mk_door', (0, -12.0, 1.3))
    A.to_scene()
    return finalize('monastery_outpost', 25)


def outpost_1():
    return _hall(1)


def outpost_2():
    return _hall(2)


def outpost_3():
    return _hall(3)


def outpost_4():
    return _hall(4)


# ------------------------------------------------------------------ NE02 entry boulder pairs
def _boulders(var):
    reset()
    A = Acc()
    rnd = random.Random(120 + var)
    main, accent = {1: (VC['stone'], VC['moss']), 2: (VC['stone2'], VC['snow']), 3: (VC['sand'], VC['clay']), 4: (VC['basalt'], VC['slate'])}[var]
    keys = [main, main, main, VC['stone'] if var != 4 else VC['dstone']]
    for sg in (-1, 1):
        cx = sg * 11.0
        h = 13.0 if sg < 0 else 11.0
        A.mound(cx, 0, 11.0, 11.0, h, 16, keys, rnd, 0.0, 0.42, 0.85, 0.14)
        A.chunk((8.0, 8.0, 2.0), (cx, 0, 0.9), main, jit=0.12, rnd=rnd)
        if var in (1, 2, 3):
            for k in range(5 if var != 3 else 4):
                x = cx + rnd.uniform(-3.2, 3.2)
                y = rnd.uniform(-3.4, 1.0)
                zt = h * rnd.uniform(0.5, 0.92)
                if var == 3:
                    A.chunk((3.4, 2.4, 0.5), (x, y, zt), accent, jit=0.08, rnd=rnd)
                else:
                    A.chunk((rnd.uniform(2.0, 3.6), rnd.uniform(1.6, 3.0), 0.7 if var == 1 else 0.9), (x, y, zt + 0.4), accent, jit=0.1, rnd=rnd)
        if var == 4:
            for k in range(6):                                                               # basalt columns at the foot
                x, y, _ = polar(3.4 + rnd.uniform(0, 1.6), rnd.uniform(0, 360))
                A.cyl(0.8, rnd.uniform(3.0, 5.4), (cx + x * 0.9, y * 0.9 - 3.0, 0.0), VC['dstone'], verts=6)
    for k in range(4):                                                                       # small stones scattered between, leaving the road clear
        A.chunk((rnd.uniform(1.0, 1.8), rnd.uniform(1.0, 1.8), rnd.uniform(0.6, 1.1)), (rnd.choice((-1, 1)) * rnd.uniform(5.4, 7.2), rnd.uniform(-5.0, 5.0), 0.4), main, jit=0.14, rnd=rnd)
    A.to_scene()
    return v5kit.fit(finalize('entry_rock_pair', 25), w=31.0, h=14.6)


def boulders_1():
    return _boulders(1)


def boulders_2():
    return _boulders(2)


def boulders_3():
    return _boulders(3)


def boulders_4():
    return _boulders(4)


BATCHES = {
    'bridges': ('v5_himalaya', [('HM01_01_rope_suspension_bridge_01', rope_bridge_1), ('HM01_02_rope_suspension_bridge_02', rope_bridge_2),
                                ('HM01_03_rope_suspension_bridge_03', rope_bridge_3)]),
    'tunnels': ('v5_himalaya', [('HM03_01_tunnel_portal_01', portal_1), ('HM03_02_tunnel_portal_02', portal_2), ('HM03_03_tunnel_portal_03', portal_3),
                                ('HM04_01_tunnel_lining_01', lining_1), ('HM04_02_tunnel_lining_02', lining_2)]),
    'signs': ('v5_entrances', [('NE01_01_village_sign_01', sign_1), ('NE01_02_village_sign_02', sign_2), ('NE01_03_village_sign_03', sign_3),
                               ('NE01_04_village_sign_04', sign_4), ('NE01_05_village_sign_05', sign_5), ('NE01_06_village_sign_06', sign_6)]),
    'road_extras': ('v5_himalaya', [
        ('HM02_01_timber_cantilever_bridge_01', cantilever_1), ('HM02_02_timber_cantilever_bridge_02', cantilever_2),
        ('HM05_01_cliff_gallery_01', gallery_1), ('HM05_02_cliff_gallery_02', gallery_2),
        ('HM06_01_switchback_wall_01', switchback_1), ('HM06_02_switchback_wall_02', switchback_2), ('HM06_03_switchback_wall_03', switchback_3),
        ('HM07_01_prayer_flag_string_01', flags_1), ('HM07_02_prayer_flag_string_02', flags_2), ('HM07_03_prayer_flag_string_03', flags_3),
        ('HM07_04_prayer_flag_string_04', flags_4), ('HM08_01_cairn_shrine_01', shrine_1), ('HM08_02_cairn_shrine_02', shrine_2),
        ('HM08_03_cairn_shrine_03', shrine_3), ('HM08_04_cairn_shrine_04', shrine_4), ('HM09_01_monastery_outpost_01', outpost_1),
        ('HM09_02_monastery_outpost_02', outpost_2), ('HM09_03_monastery_outpost_03', outpost_3), ('HM09_04_monastery_outpost_04', outpost_4)]),
    'boulders': ('v5_entrances', [('NE02_01_entry_rock_pair_01', boulders_1), ('NE02_02_entry_rock_pair_02', boulders_2),
                                  ('NE02_03_entry_rock_pair_03', boulders_3), ('NE02_04_entry_rock_pair_04', boulders_4)]),
}
