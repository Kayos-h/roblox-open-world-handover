"""wg2 shrine ruins: E12 shrine_ruin 01-04 -> v4_world. 14-24 wide, overgrown, haunting.
Replacement for frozen worker wg. Reuses wg's weathered-stone palette (imported). Builds through
v4run.ps1 only. Fronts face -Y, 1 unit = 1 stud."""
import math, random
from mathutils import Euler
import kitlib
from kitlib import (reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, top_paint)
from arch import F, lbox, lslab, lbeam, nm, arc_pts, column_c, pediment
import v4_wg_graveyard as WG
from v4_wg_graveyard import _lichen, _mound, _grass_tuft, _ivy_face

kitlib.PAL['wg2w_moss']  = ((78, 92, 54),   'Grass',      0.00, 1.00, 0)
kitlib.PAL['wg2w_ivy']   = ((54, 82, 40),   'LeafyGrass', 0.00, 0.95, 0)
kitlib.PAL['wg2w_bowl']  = ((70, 60, 52),   'Metal',      0.70, 0.60, 0)
kitlib.PAL['wg2w_flame'] = ((236, 128, 40), 'Neon',       0.00, 0.50, 1.8)
kitlib.PAL['wg2w_offer'] = ((180, 150, 92), 'SmoothPlastic', 0.00, 0.60, 0)


def _broken_col(cx, cy, h, r=0.55, key='wg_stone', seed=0):
    """A column broken off at height h with a jagged, mossy top."""
    rnd = random.Random(seed)
    lathe(nm('cb'), [(0, 0), (r * 1.3, 0), (r * 1.3, r * 0.3), (r, r * 0.5), (r, h)], loc=(cx, cy, 0), key=key, segs=14)
    for i in range(6):   # faint flutes
        a = 2 * math.pi * i / 6
        tube(nm('fl'), [(cx + math.cos(a) * r, cy + math.sin(a) * r, r * 0.6),
                        (cx + math.cos(a) * r, cy + math.sin(a) * r, h - 0.2)], 0.04, 'wg_stone_d', res=4)
    top_paint(box(nm('br'), (r * 2.1, r * 2.1, 0.4), loc=(cx, cy, h), key=key, rot=(rnd.uniform(-8, 8), rnd.uniform(-8, 8), 0), bev=0.1),
              'wg2w_moss', 0.72, seed)


def _fallen_col(cx, cy, a, L, r=0.55, key='wg_stone', seed=0, drums=4):
    """A toppled column lying in drum segments along angle a."""
    for i in range(drums):
        px = cx + math.cos(a) * (-L / 2 + L * i / (drums - 1))
        py = cy + math.sin(a) * (-L / 2 + L * i / (drums - 1))
        cyl(nm('dr'), r, L / drums * 0.9, loc=(px, py, r), key=key, verts=12, rot=(0, 90, math.degrees(a)))


def _vines(x0, x1, y, z0, z1, n, seed):
    _ivy_face(x0, x1, y, z0, z1, n, seed)


# ============================================================ E12 shrine ruins
def shrine_01():
    """E12_01 - collapsed circular shrine: a ring of broken columns on a stepped base, rubble, overgrown."""
    reset()
    R = 7.0
    # two-step circular stylobate
    for k in range(2):
        lathe(nm('base'), [(0, 0), (R + 1.4 - k * 0.7, 0), (R + 1.4 - k * 0.7, 0.5), (0, 0.5)],
              loc=(0, 0, k * 0.5), key='wg_stone_d' if k == 0 else 'wg_stone', segs=28)
    rnd = random.Random(1)
    n = 10
    for i in range(n):
        a = 2 * math.pi * i / n
        cx, cy = math.cos(a) * R, math.sin(a) * R
        if rnd.random() < 0.45:          # some fallen
            _fallen_col(cx, cy, a + 1.57, rnd.uniform(4, 6), seed=10 + i)
        else:
            _broken_col(cx, cy, rnd.uniform(2.5, 6.0), seed=10 + i)
    # broken ring architrave fragments still bridging two uprights
    for _ in range(3):
        a = rnd.uniform(0, 6.28)
        cx, cy = math.cos(a) * R, math.sin(a) * R
        box(nm('arch'), (2.6, 0.7, 0.8), loc=(cx, cy, 5.6), key='wg_stone', rot=(0, 0, math.degrees(a) + 90), bev=0.05)
    # central altar + rubble + grass
    box(nm('alt'), (2.2, 2.2, 1.6), loc=(0, 0, 1.3), key='wg_stone', bev=0.08)
    top_paint(box(nm('altc'), (2.6, 2.6, 0.3), loc=(0, 0, 2.1), key='wg_stone'), 'wg2w_moss', 0.7, 1)
    for _ in range(14):
        s = rnd.uniform(0.4, 1.0)
        box(nm('rb'), (s, s, s * 0.8), loc=(rnd.uniform(-R, R), rnd.uniform(-R, R), s * 0.4),
            key=rnd.choice(['wg_stone', 'wg_stone_d']), rot=(rnd.uniform(0, 40), 0, rnd.uniform(0, 90)), bev=0.04)
    rndg = random.Random(101)
    for _ in range(10):
        _grass_tuft(rnd.uniform(-R, R), rnd.uniform(-R, R), rndg)
    return finalize('shrine_ruin_01', smooth_angle=30)


def shrine_02():
    """E12_02 - roadside stone shrine niche with a statue base and offerings, overgrown."""
    reset()
    rnd = random.Random(2)
    W, D, H = 7.0, 4.5, 8.5
    # chunky stone shrine block with a deep arched niche
    box(nm('body'), (W, D, H), loc=(0, 0, H / 2), key='wg_stone', bev=0.08)
    # deep niche recess (dark) open at the front + arch ring
    box(nm('niche'), (3.4, D + 0.6, 5.0), loc=(0, -0.9, 3.4), key='wg_stone_d')
    tube(nm('arch'), arc_pts(F(0, -D / 2 - 0.02, 0, 0), 0, 5.4, 1.7, y=0, n=11), 0.24, 'wg_stone_d', res=4)
    # weathered gabled cap
    for s in (-1, 1):
        lslab(F(0, -D / 2 - 0.4, 0, 0), [(0, 0, H), (s * (W / 2 + 0.6), 0, H - 0.4), (s * 0.2, 0, H + 2.4)], (0, D + 0.8, 0), 'wg_stone_d')
    # low flanking walls to widen the roadside footprint into spec
    for s in (-1, 1):
        lw = box(nm('fw'), (4.0, 1.3, 2.6), loc=(s * (W / 2 + 2.0), 0.4, 1.3), key='wg_stone', bev=0.06)
        top_paint(lw, 'wg2w_moss', 0.72, 20 + s)
        box(nm('fwc'), (4.2, 1.5, 0.3), loc=(s * (W / 2 + 2.0), 0.4, 2.6), key='wg_stone_d', bev=0.04)
    # statue base + a small weathered idol set INTO the deep niche
    box(nm('sb'), (1.8, 1.6, 1.2), loc=(0, -0.4, 2.0), key='wg_stone', bev=0.05)
    lathe(nm('idol'), [(0, 0), (0.6, 0), (0.5, 1.6), (0.35, 2.4), (0.2, 2.7), (0, 2.8)], loc=(0, -0.5, 2.6), key='wg_stone', segs=12)
    ball(nm('ih'), 0.34, loc=(0, -0.6, 5.4), key='wg_stone', segs=8, rings=6)
    # offerings at the foot: bowls, candles, flowers
    for ox in (-1.3, -0.4, 0.5, 1.3):
        lathe(nm('bowl'), [(0, 0), (0.3, 0), (0.34, 0.25), (0.22, 0.3)], loc=(ox, -D / 2 + 0.2, 0.0), key='wg2w_offer', segs=10)
    for ox in (-0.9, 0.9):
        cyl(nm('cndl'), 0.1, 0.5, loc=(ox, -D / 2 + 0.45, 0.0), key='wax', verts=8)
        ball(nm('fl'), 0.09, loc=(ox, -D / 2 + 0.45, 0.56), key='wg2w_flame', segs=6, rings=4)
    # overgrowth
    top_paint(box(nm('cap'), (W, D, 0.3), loc=(0, 0, H), key='wg_stone'), 'wg2w_moss', 0.66, 2)
    _vines(-W / 2, W / 2, -D / 2, 0.0, H, 12, 2)
    _mound(0, 0, W + 9, D + 4, seed=2)
    rndg = random.Random(22)
    for _ in range(6):
        _grass_tuft(rnd.uniform(-W / 2, W / 2), -D / 2 + rnd.uniform(0, 0.6), rndg)
    return finalize('shrine_ruin_02', smooth_angle=30)


def shrine_03():
    """E12_03 - ruined temple portico: three standing columns, a broken lintel, steps, overgrown."""
    reset()
    rnd = random.Random(3)
    W = 16.0
    # stepped stylobate (3 steps across the front)
    for k in range(3):
        box(nm('st'), (W - k * 1.4, 7.0 - k * 1.2, 0.5), loc=(0, 1.0 + k * 0.1, 0.25 + k * 0.5), key='wg_stone_d' if k == 0 else 'wg_stone', bev=0.04)
    sz = 1.6
    cols_x = [-6.0, -1.5, 5.0]   # irregular spacing: one is missing
    heights = [8.4, 8.4, 4.0]    # the third is broken short
    for x, h in zip(cols_x, heights):
        if h > 6:
            column_c(x, -1.8, sz, h, 0.75, key='wg_marble', base='wg_marble_d')
        else:
            _broken_col(x, -1.8, h, r=0.75, key='wg_marble', seed=int(x))
    # one fallen column lying across the steps
    _fallen_col(1.5, 2.5, 0.2, 7.0, r=0.72, key='wg_marble', seed=33, drums=5)
    # broken lintel: one span intact between cols 1-2, the rest fallen
    lbox(F(0, -1.8, sz + 8.4, 0), (5.0, 1.8, 1.2), -3.75, 0, 0.3, 'wg_marble_d')
    box(nm('ff'), (3.0, 1.6, 1.0), loc=(3.0, -3.0, 0.9), key='wg_marble_d', rot=(0, 12, 20), bev=0.05)
    # mossy caps + rubble + weeds
    for x, h in zip(cols_x, heights):
        if h > 6:
            top_paint(box(nm('cap'), (2.0, 2.0, 0.3), loc=(x, -1.8, sz + h), key='wg_marble'), 'wg2w_moss', 0.75, int(x) + 5)
    for _ in range(12):
        s = rnd.uniform(0.4, 1.0)
        box(nm('rb'), (s, s, s * 0.8), loc=(rnd.uniform(-7, 7), rnd.uniform(-2, 4), s * 0.4 + 1.0),
            key=rnd.choice(['wg_marble', 'wg_stone']), rot=(rnd.uniform(0, 40), 0, rnd.uniform(0, 90)), bev=0.04)
    rndg = random.Random(303)
    for _ in range(10):
        _grass_tuft(rnd.uniform(-7, 7), rnd.uniform(-2.5, 4), rndg)
    return finalize('shrine_ruin_03', smooth_angle=30)


def shrine_04():
    """E12_04 - altar stone with a fire bowl and a broken wall behind, overgrown."""
    reset()
    rnd = random.Random(4)
    # broken back wall with jagged top + a window gap
    pts = [(-7.0, 0, 0), (7.0, 0, 0), (7.0, 0, 3.0), (4.0, 0, 4.6), (1.5, 0, 3.4), (-1.5, 0, 5.2),
           (-4.0, 0, 3.6), (-7.0, 0, 4.4)]
    wall = lslab(F(0, 0.8, 5.5, 0), pts, (0, -1.6, 0), 'wg_stone')
    # coursed lines + a window gap
    f = F(0, 5.5 - 0.8, 0, 0)
    for i in range(1, 5):
        lbox(f, (13.6, 0.06, 0.08), 0, -0.02, 0.9 * i, 'wg_stone_d')
    box(nm('gap'), (1.8, 1.8, 2.0), loc=(2.5, 5.5, 2.4), key='wg_stone_d')
    tube(nm('ga'), arc_pts(F(2.5, 5.5 - 0.82, 0, 0), 0, 3.4, 0.9, y=0, n=9), 0.16, 'wg_stone_d', res=4)
    # low altar stone out front
    box(nm('altb'), (5.0, 2.6, 0.6), loc=(0, -1.0, 0.3), key='wg_stone_d', bev=0.05)
    alt = box(nm('alt'), (4.2, 2.0, 1.4), loc=(0, -1.0, 1.3), key='wg_stone', bev=0.08)
    top_paint(box(nm('altc'), (4.6, 2.4, 0.3), loc=(0, -1.0, 2.0), key='wg_stone'), 'wg2w_moss', 0.68, 4)
    # carved runnel lines on the altar top
    for xx in (-1.2, 0, 1.2):
        lbox(F(0, -1.0, 2.15, 0), (0.08, 1.6, 0.05), xx, 0, 0, 'wg_stone_d')
    # iron fire bowl on a tripod on the altar, with flame
    for i in range(3):
        a = 2 * math.pi * i / 3
        tube(nm('leg'), [(math.cos(a) * 0.8, -1.0 + math.sin(a) * 0.8, 2.15), (0, -1.0, 3.3)], 0.07, 'wg2w_bowl', res=4)
    lathe(nm('bowl'), [(0, 0), (0.9, 0), (1.0, 0.5), (0.7, 0.8), (0.75, 0.9)], loc=(0, -1.0, 3.2), key='wg2w_bowl', segs=14)
    for _ in range(5):
        ball(nm('fl'), rnd.uniform(0.2, 0.4), loc=(rnd.uniform(-0.4, 0.4), -1.0 + rnd.uniform(-0.3, 0.3), 3.9 + rnd.uniform(0, 0.4)),
             key='wg2w_flame', segs=6, rings=4, scale=(1, 1, 1.5))
    # ivy on the wall, rubble, weeds
    _vines(-7, 7, 0.0, 0.0, 5.0, 16, 4)
    for _ in range(10):
        s = rnd.uniform(0.4, 0.9)
        box(nm('rb'), (s, s, s * 0.8), loc=(rnd.uniform(-7, 7), rnd.uniform(-2, 2), s * 0.4),
            key=rnd.choice(['wg_stone', 'wg_stone_d']), rot=(rnd.uniform(0, 40), 0, rnd.uniform(0, 90)), bev=0.04)
    _mound(0, 1.0, 16, 6, seed=4)
    rndg = random.Random(404)
    for _ in range(10):
        _grass_tuft(rnd.uniform(-7, 7), rnd.uniform(-2, 2.5), rndg)
    return finalize('shrine_ruin_04', smooth_angle=30)


BATCHES = {
    'shrines': ('v4_world', [
        ('E12_01_shrine_ruin_01', shrine_01, (1.0, -1.1, 0.5)),
        ('E12_02_shrine_ruin_02', shrine_02, (1.0, -1.15, 0.45)),
        ('E12_03_shrine_ruin_03', shrine_03, (1.0, -1.1, 0.4)),
        ('E12_04_shrine_ruin_04', shrine_04, (1.0, -1.15, 0.45)),
    ]),
}
