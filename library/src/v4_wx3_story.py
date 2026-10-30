"""Fix worker wx3 - F09_08, F09_10, F09_13 story props (category v4_story).
Reviewer: ruin-diorama buildings are plain grey boxes / white box towers, low detail.
Fix: give the box ruins broken roofs, lintels, buttresses, stone courses and strata so they
read as ruined buildings, not blank cubes. Copies the helpers from v4_we2_story; never edits it.
"""
import math, random
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism
from arch import F, nm, lbox, lbeam, lslab, beam3
from nature import blob
# reuse the ruin helpers from the original story module
from v4_we2_story import _rubble, _broken_wall, _ivy, _foundation

P = kitlib.PAL
P['wx3s_slate']  = ((96, 104, 118), 'Slate',      0.0, 0.76, 0)   # broken roof slate
P['wx3s_slate2'] = ((78, 86, 100),  'Slate',      0.0, 0.80, 0)
P['wx3s_beam']   = ((78, 56, 38),   'Wood',       0.0, 0.88, 0)
P['wx3s_course'] = ((120, 114, 104), 'Cobblestone', 0.0, 0.92, 0)  # darker course line on grey stone


def _broken_roof(f, W, D, z0, h, seed, slate='wx3s_slate'):
    """A partly-collapsed gabled roof over a ruin: a few surviving slate rafter planes on one
    side, exposed broken beams on the other."""
    rnd = random.Random(seed)
    nr = max(3, int(W / 2.2))
    for i in range(nr):
        x = -W / 2 + W * (i + 0.5) / nr
        # one slope survives on the +y side, patchy
        if rnd.random() < 0.72:
            lslab(f, [(x - W / nr / 2, -0.3, z0 + 0.2), (x + W / nr / 2, -0.3, z0 + 0.2),
                      (x + W / nr / 2, D / 2, z0 + h), (x - W / nr / 2, D / 2, z0 + h)], (0, 0, 0.12),
                  slate if i % 2 else 'wx3s_slate2')
    # ridge beam + a couple of broken rafters sticking up on the collapsed -y side
    lbeam(f, (-W / 2, D / 2, z0 + h), (W / 2, D / 2, z0 + h), 0.4, 'wx3s_beam')
    for k in range(3):
        x = -W / 2 + W * (k + 0.5) / 3
        lbeam(f, (x, D / 2, z0 + h), (x + rnd.uniform(-1, 1), -D / 4, z0 + rnd.uniform(0.5, 2.0)), 0.3, 'wx3s_beam')


def _stone_courses(f, L, z0, z1, t, key='wx3s_course', course=2.4):
    """Thin darker course lines on a grey ruin wall (both faces)."""
    z = z0 + course
    while z < z1 - 0.2:
        for y in (-t / 2, t / 2):
            lbox(f, (L - 0.1, 0.12, 0.28), 0, y - math.copysign(0.06, y), z, key)
        z += course


# ===================================================== F09_08 foundation + hearth, now with a part roof
def story_08():
    """Stone footprint with partial walls, doorway, hearth; now ALSO a surviving broken roof over
    one bay, lintels and buttresses, stone course lines - reads as a ruined building not a box."""
    _foundation(8, with_hearth=True)
    rnd = random.Random(808)
    W, D = 16.0, 12.0
    # doorway lintel across the 's' gap
    box(nm('lint'), (6.0, 1.6, 1.2), loc=(0, -D / 2, 3.6), key='stone_light', bev=0.05)
    # buttresses on the long 'w' wall
    for yy in (-3.0, 3.0):
        lbox(F(-W / 2, yy, 0.5, 90), (2.2, 2.4, 4.0), 0, 0, 2.0, 'stone_dark', bev=0.05)
    # course lines on the standing walls
    _stone_courses(F(0, D / 2, 0.5, 0), W, 0.5, 4.0, 1.4)
    _stone_courses(F(-W / 2, 0, 0.5, 90), D, 0.5, 4.0, 1.4)
    # surviving broken roof over the hearth (n) bay
    _broken_roof(F(0, 0, 0, 0), W - 2.0, D, 4.6, 4.0, 808)
    return finalize('story_prop_08', smooth_angle=30)


# ===================================================== F09_10 hall foundation + columns + roofed bay
def story_10():
    """Large hall foundation, long wall with window gaps, hearth, column stumps; now a surviving
    roofed bay on the standing columns, column capitals, and stone course lines."""
    _foundation(10, with_hearth=True)
    rnd = random.Random(810)
    W, D = 16.0, 12.0
    cols_x = (-5, 0, 5)
    heights = {}
    for x in cols_x:
        hh = rnd.uniform(3.5, 5.5)
        heights[x] = hh
        cyl(nm('col'), 1.0, hh, loc=(x, 2.0, 0.5), key='stone_light', verts=12)
        # fluting course rings
        for zz in (1.5, 3.0):
            if zz < hh:
                torus(nm('cr'), 1.05, 0.08, loc=(x, 2.0, 0.5 + zz), key='wx3s_course', segs=12, rsegs=4)
        cyl(nm('colc'), 1.25, 0.5, loc=(x, 2.0, 0.5 + hh), key='stone', verts=12)
    # an architrave beam spanning the two tallest adjacent columns + a small roof patch on it
    xa, xb = cols_x[0], cols_x[1]
    za = 0.5 + min(heights[xa], heights[xb]) + 0.5
    box(nm('arch'), (abs(xb - xa) + 2.4, 1.6, 0.8), loc=((xa + xb) / 2, 2.0, za), key='stone', bev=0.05)
    for i in range(4):
        xx = xa - 1 + (abs(xb - xa) + 2) * i / 3
        lslab(F((xa + xb) / 2, 2.0, 0, 0), [(xx - (xa + xb) / 2 - 0.8, -1.2, za + 0.4), (xx - (xa + xb) / 2 + 0.8, -1.2, za + 0.4),
              (xx - (xa + xb) / 2 + 0.8, 1.2, za + 2.0), (xx - (xa + xb) / 2 - 0.8, 1.2, za + 2.0)], (0, 0, 0.12), 'wx3s_slate' if i % 2 else 'wx3s_slate2')
    # course lines on the standing perimeter walls
    _stone_courses(F(0, D / 2, 0.5, 0), W, 0.5, 4.0, 1.4)
    return finalize('story_prop_10', smooth_angle=30)


# ===================================================== F09_13 ruined bell-tower stump (strata detail)
def story_13():
    """Ruined bell-tower stump: square tower, two walls tall two broken low, now with strata
    course lines, a belfry lintel, buttresses and a broken-off slate roof cap; the cracked bell
    at its foot. Grey weathered stone, not a plain white box."""
    reset()
    rnd = random.Random(1313)
    W, Hh, t = 8.0, 16.0, 1.6
    walls = ((0, -W / 2, 0, 0.95), (-W / 2, 0, 90, 0.9), (0, W / 2, 0, 0.5), (W / 2, 0, 90, 0.45))
    for (cx, cy, rz, frac) in walls:
        f = F(cx, cy, 0, rz)
        _broken_wall(f, W, Hh * frac, t, 130 + int(cx + cy + rz), crenel=(frac < 0.6))
        _stone_courses(f, W, 1.0, Hh * frac - 0.5, t, course=2.6)
    # corner buttresses on the two tall corners
    for (bx, by) in ((-W / 2, -W / 2), (W / 2, -W / 2)):
        box(nm('but'), (1.8, 1.8, Hh * 0.7), loc=(bx, by, Hh * 0.35), key='stone_dark', bev=0.05)
    # belfry opening lintel on a tall wall
    box(nm('lint'), (W - 1, t, 1.0), loc=(0, -W / 2, Hh * 0.85), key='stone_light')
    # a broken-off slate roof cap clinging to the tall corner
    for i in range(4):
        x = -W / 2 + 1.0 + i * 2.0
        lslab(F(0, 0, 0, 0), [(x - 1.0, -W / 2, Hh * 0.9), (x + 1.0, -W / 2, Hh * 0.9),
              (x + 1.0, -W / 6, Hh * 0.9 + 2.2), (x - 1.0, -W / 6, Hh * 0.9 + 2.2)], (0, 0, 0.12),
              'wx3s_slate' if i % 2 else 'wx3s_slate2') if i < 3 else None
    # fallen cracked bell at the foot
    lathe(nm('bell'), [(0, 0), (1.6, 0.1), (1.5, 0.6), (1.2, 1.4), (1.3, 2.2), (0.9, 2.7), (0.5, 2.9), (0, 2.95)],
          loc=(W / 2 + 2.0, 2.0, 0.0), key='we2s_bell', segs=14, rot=(80, 0, 20))
    torus(nm('by'), 0.4, 0.12, loc=(W / 2 + 2.0, 2.0, 2.9), key='we2s_bell', segs=10, rsegs=4)
    box(nm('crk'), (0.2, 1.4, 1.8), loc=(W / 2 + 2.9, 2.0, 1.2), key='stone_dark', rot=(80, 0, 20))
    for side in ((0, -W / 2, 0), (-W / 2, 0, 90)):
        _ivy(F(side[0], side[1], 0, side[2]), -W / 2, W / 2, 1, Hh * 0.8, 133 + int(side[0]), dens=0.9)
    _rubble(0, 0, 5, 10, 1333)
    return finalize('story_prop_13', smooth_angle=30)


BATCHES = {
    'ruins': ('v4_story', [('F09_08_story_prop_08', story_08, (0.6, -1.2, 0.35)),
                           ('F09_10_story_prop_10', story_10, (0.6, -1.2, 0.35)),
                           ('F09_13_story_prop_13', story_13, (0.9, -1.1, 0.4))]),
}
