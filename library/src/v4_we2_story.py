"""Worker we2 - F09 story props (13), category v4_story.
Ruined, abandoned scenes that tell a story: broken carts with spilled cargo, camps,
ruined watchtowers, foundations, overgrown ruins. 8-22 wide. Original designs.
Base palette keys reused: stone/stone_dark/stone_light, moss, leaf/leaf_dark, ivy, dirt,
wood/wood_dark/wood_light, timber, rope, iron, rust, canvas, flame, brick.
"""
import math, random
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism
from arch import F, nm, lbox, lbeam, lslab, beam3
from nature import rock, blob, fern

P = kitlib.PAL
P['we2s_ash']    = ((60, 56, 52),    'Ground',     0.00, 1.00, 0)
P['we2s_sack']   = ((176, 150, 104), 'Fabric',     0.00, 1.00, 0)
P['we2s_ember']  = ((255, 120, 36),  'Neon',       0.00, 0.50, 1.6)
P['we2s_grain']  = ((206, 176, 108), 'Sand',       0.00, 1.00, 0)
P['we2s_tarp']   = ((150, 140, 110), 'Fabric',     0.00, 0.95, 0)
P['we2s_mud']    = ((92, 74, 54),    'Mud',        0.00, 1.00, 0)
P['we2s_bell']   = ((120, 86, 52),   'Metal',      0.90, 0.40, 0)


# --------------------------------------------------- shared ruin helpers
def _rubble(cx, cy, r, n, seed, z=0.0):
    rnd = random.Random(seed)
    for k in range(n):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, r)
        rock(nm('rb'), rnd.uniform(0.4, 1.2), (cx + math.cos(a) * d, cy + math.sin(a) * d, z + rnd.uniform(0, 0.3)),
             key=rnd.choice(('stone', 'stone_dark', 'stone_light')), seed=seed * 7 + k, scale=(1, 1, 0.7))


def _broken_wall(f, L, h, t, seed, crenel=True):
    """A stone wall from x=-L/2..L/2 with a jagged broken top profile."""
    rnd = random.Random(seed)
    n = max(3, int(L / 2.0))
    for i in range(n):
        x = -L / 2 + L * (i + 0.5) / n
        hh = h * rnd.uniform(0.35, 1.0) if crenel else h
        lbox(f, (L / n + 0.05, t, hh), x, 0, hh / 2, rnd.choice(('stone', 'stone_dark', 'stone_light')), bev=0.05)
    # moss on the base
    for k in range(int(L / 1.5)):
        x = -L / 2 + rnd.uniform(0, L)
        blob(nm('mo'), rnd.uniform(0.3, 0.6), f.p(x, -t / 2 - 0.1, rnd.uniform(0.1, 0.5)), 'moss', subdiv=1, amp=0.3, seed=seed + k)


def _ivy(f, x0, x1, z0, z1, seed, dens=0.5):
    rnd = random.Random(seed)
    n = int((x1 - x0) * (z1 - z0) * dens * 0.3) + 4
    for k in range(n):
        x = rnd.uniform(x0, x1); z = rnd.uniform(z0, z1)
        ball(nm('iv'), rnd.uniform(0.25, 0.5), f.p(x, -0.25, z), key=rnd.choice(('ivy', 'leaf_dark', 'leaf')), segs=6, rings=4, scale=(1, 0.5, 1))


def _cart(x, y, rz, broken=True, seed=0):
    """A wooden cart; broken=True drops one wheel and tilts the bed."""
    rnd = random.Random(seed)
    f = F(x, y, 0, rz)
    tilt = rnd.uniform(6, 14) if broken else 0
    bedz = 2.2
    lbox(f, (7.0, 3.4, 0.5), 0, 0, bedz, 'wood', rot=(tilt, 0, 0))
    for s in (-1, 1):
        lbox(f, (7.0, 0.4, 1.2), 0, s * 1.5, bedz + 0.6, 'wood_dark', rot=(tilt, 0, 0))
    # shafts
    for s in (-1, 1):
        lbeam(f, (3.4, s * 1.0, bedz), (6.4, s * 0.7, bedz - 0.6), 0.3, 'timber')
    # wheels: 2 good, one off if broken
    def wheel(wx, wy, wz, rz2=0):
        torus(nm('wr'), 1.5, 0.3, loc=f.p(wx, wy, wz), key='wood_dark', segs=16, rsegs=5, rot=f.r(0, 90, rz2))
        torus(nm('wi'), 1.5, 0.12, loc=f.p(wx, wy, wz), key='rust', segs=16, rsegs=4, rot=f.r(0, 90, rz2))
        for k in range(8):
            a = 2 * math.pi * k / 8
            tube(nm('sp'), [f.p(wx, wy, wz), f.p(wx, wy + math.cos(a) * 1.4, wz + math.sin(a) * 1.4)], 0.1, 'wood', res=4)
    wheel(2.2, 1.9, 1.5)
    wheel(-2.2, 1.9, 1.5)
    wheel(2.2, -1.9, 1.5)
    if broken:
        # fourth wheel fallen flat beside the cart
        torus(nm('wf'), 1.5, 0.3, loc=f.p(-2.2, -3.4, 0.35), key='wood_dark', segs=16, rsegs=5, rot=f.r(90, 0, 0))
        lbox(f, (0.5, 0.5, 1.6), -2.2, -1.9, 0.8, 'timber', rot=(0, 20, 0))  # broken axle stub
    return f, bedz, tilt


def _tent(x, y, w, d, h, seed, collapsed=False):
    rnd = random.Random(seed)
    f = F(x, y, 0, 0)
    if collapsed:
        # draped tarp over a low mound
        for k in range(6):
            lslab(f, [(-w / 2 + k * w / 6, -d / 2, rnd.uniform(0.3, 1.0)), (-w / 2 + (k + 1) * w / 6, -d / 2, rnd.uniform(0.3, 1.0)),
                      (-w / 2 + (k + 1) * w / 6, d / 2, rnd.uniform(0.3, 1.2)), (-w / 2 + k * w / 6, d / 2, rnd.uniform(0.3, 1.0))], (0, 0, 0.08), 'we2s_tarp')
        box(nm('pole'), (0.3, 0.3, 2.2), loc=f.p(w * 0.2, 0, 1.0), key='timber', rot=(0, 40, 0))
    else:
        # A-frame tent
        tube(nm('rp'), [f.p(0, -d / 2, h + 0.5), f.p(0, d / 2, h + 0.5)], 0.12, 'timber', res=4)
        for s in (-1, 1):
            box(nm('tp'), (0.2, 0.2, h + 1.0), loc=f.p(0, s * d / 2, (h + 0.5) / 2), key='timber', rot=(0, 8 * s, 0))
            lslab(f, [(0, s * d / 2, h + 0.5), (0, -s * d / 2, h + 0.5), (s * w / 2, -s * d / 2, 0), (s * w / 2, s * d / 2, 0)] if False else
                  [(0, -d / 2, h + 0.5), (0, d / 2, h + 0.5), (s * w / 2, d / 2, 0.2), (s * w / 2, -d / 2, 0.2)], (0, 0, 0.1), 'canvas')
    return f


def _campfire(x, y, seed, lit=True):
    rnd = random.Random(seed)
    for k in range(7):
        a = 2 * math.pi * k / 7
        rock(nm('fs'), 0.4, (x + math.cos(a) * 1.3, y + math.sin(a) * 1.3, 0.2), key='stone_dark', seed=seed + k)
    for k in range(5):
        a = rnd.uniform(0, 6.28)
        tube(nm('log'), [(x - math.cos(a) * 0.9, y - math.sin(a) * 0.9, 0.3), (x + math.cos(a) * 0.9, y + math.sin(a) * 0.9, 0.5)], 0.22, 'wood_dark', res=5)
    cyl(nm('ash'), 1.1, 0.12, loc=(x, y, 0.15), key='we2s_ash', verts=12)
    if lit:
        for k in range(5):
            a = 2 * math.pi * k / 5
            lathe(nm('fl'), [(0, 0), (0.3, 0.3), (0.15, 0.8), (0, 1.1)], loc=(x + math.cos(a) * 0.3, y + math.sin(a) * 0.3, 0.4), key='flame', segs=6)
        ball(nm('em'), 0.5, loc=(x, y, 0.3), key='we2s_ember', segs=8, rings=5, scale=(1, 1, 0.4))


def _log_seat(x, y, rz):
    cyl(nm('ls'), 0.8, 3.2, loc=(x, y, 0.8), key='wood', verts=12, rot=(90, 0, rz))


def _crate(x, y, z, s=1.0, rz=0, key='wood_light'):
    box(nm('cr'), (2.0 * s, 2.0 * s, 2.0 * s), loc=(x, y, z + s), key=key, rot=(0, 0, rz), bev=0.04)
    for zz in (0.2, 1.8):
        box(nm('cs'), (2.06 * s, 2.06 * s, 0.2 * s), loc=(x, y, z + zz * s), key='wood_dark', rot=(0, 0, rz))


def _sack(x, y, z, s=1.0, key='we2s_sack'):
    lathe(nm('sk'), [(0, 0), (0.7 * s, 0.1 * s), (0.8 * s, 0.9 * s), (0.5 * s, 1.5 * s), (0.25 * s, 1.7 * s), (0.3 * s, 1.85 * s), (0, 1.9 * s)], loc=(x, y, z), key=key, segs=10)


def _barrel(x, y, z, s=1.0, key='wood'):
    lathe(nm('ba'), [(0, 0), (0.62 * s, 0), (0.78 * s, 0.85 * s), (0.62 * s, 1.7 * s), (0, 1.7 * s)], loc=(x, y, z), key=key, segs=12)
    for zz in (0.2, 1.5):
        torus(nm('bh'), 0.72 * s, 0.06 * s, loc=(x, y, z + zz * s), key='rust', segs=12, rsegs=4)


# ===================================================== F09_01..02 broken carts
def story_01():
    """Broken cart, a wheel off, spilled crates and grain sacks, scattered on a muddy rut."""
    reset()
    cyl(nm('gr'), 7.0, 0.2, loc=(0, 0, 0.1), key='we2s_mud', verts=24)
    f, bedz, tilt = _cart(0, 0, 10, broken=True, seed=1)
    _crate(4.5, 1.0, 0.0, s=0.9, rz=18)
    _crate(5.6, -0.8, 0.0, s=0.8, rz=-24)
    _crate(3.6, 2.4, 0.0, s=0.7, rz=40)
    for sx in (-1, 0, 1):
        _sack(5.0 + sx * 0.9, 2.6 + sx * 0.3, 0.0, s=0.9)
    cyl(nm('spill'), 1.6, 0.08, loc=(5.6, 2.0, 0.12), key='we2s_grain', verts=14)
    _rubble(-5, -4, 3, 6, 11)
    return finalize('story_prop_01', smooth_angle=30)


def story_02():
    """Overturned ox-cart beside a ditch, barrels rolled out, one smashed, a snapped yoke."""
    reset()
    cyl(nm('gr'), 9.0, 0.2, loc=(0, 0, 0.1), key='we2s_mud', verts=24)
    # cart lying on its LEFT side: bed is a vertical slab, open box facing +y, wheels now vertical in the air
    f = F(0, -0.5, 0, 0)
    # bed floor (now a vertical wall) + three side boards fanning up
    lbox(f, (7.0, 0.5, 3.4), 0, 0, 1.9, 'wood')                       # cart floor, stood on edge
    lbox(f, (7.0, 2.4, 0.4), 0, 1.2, 0.3, 'wood_dark')               # one long side on the ground
    lbox(f, (7.0, 0.4, 2.0), 0, -0.2, 2.9, 'wood_dark')              # far side raised
    for s in (-1, 1):
        lbox(f, (0.4, 2.2, 2.0), s * 3.3, 0.1, 2.0, 'wood')          # end boards
    # axle + two wheels sticking up off the ground
    tube(nm('ax'), [f.p(-2.4, -0.4, 3.6), f.p(2.4, -0.4, 3.6)], 0.22, 'timber', res=6)
    for s in (-1, 1):
        wx = s * 2.4
        torus(nm('wr'), 1.5, 0.3, loc=f.p(wx, -0.4, 3.6), key='wood_dark', segs=16, rsegs=5, rot=f.r(90, 0, 0))
        torus(nm('wi'), 1.5, 0.12, loc=f.p(wx, -0.4, 3.6), key='rust', segs=16, rsegs=4, rot=f.r(90, 0, 0))
        for k in range(8):
            a = 2 * math.pi * k / 8
            tube(nm('sp'), [f.p(wx, -0.4, 3.6), f.p(wx + math.cos(a) * 1.4, -0.4, 3.6 + math.sin(a) * 1.4)], 0.09, 'wood', res=4)
    # snapped yoke shafts pointing up from one end
    lbeam(f, (3.3, 0.5, 2.6), (5.2, 1.2, 4.0), 0.3, 'timber')
    lbeam(f, (3.3, -0.3, 2.6), (4.6, -0.6, 3.2), 0.3, 'timber')      # the broken-off stub
    # barrels rolled out, one smashed
    _barrel(-4.0, 2.5, 0.0)
    _barrel(-2.6, 3.2, 0.0)
    rnd = random.Random(22)
    for k in range(7):
        a = 2 * math.pi * k / 7
        box(nm('st'), (0.3, 0.12, 1.6), loc=(3.2 + math.cos(a) * 0.7, 2.8 + math.sin(a) * 0.7, 0.3), key='wood', rot=(rnd.uniform(60, 88), 0, math.degrees(a)))
    cyl(nm('spill'), 1.3, 0.08, loc=(3.2, 2.8, 0.12), key='we2s_grain', verts=14)
    _rubble(0, -3, 3, 5, 23)
    return finalize('story_prop_02', smooth_angle=30)


# ===================================================== F09_03..05 camps
def story_03():
    """Campfire ring with log seats and an A-frame tent; a pot on a tripod over embers."""
    reset()
    cyl(nm('gr'), 7.0, 0.15, loc=(0, 0, 0.07), key='dirt', verts=24)
    _campfire(0, 0, 3, lit=True)
    for a in (0, 2.09, 4.19):
        _log_seat(math.cos(a) * 3.2, math.sin(a) * 3.2, math.degrees(a) + 90)
    # tripod + pot
    for k in range(3):
        a = 2 * math.pi * k / 3
        tube(nm('tri'), [(math.cos(a) * 1.4, math.sin(a) * 1.4, 0), (0, 0, 3.0)], 0.09, 'timber', res=4)
    lathe(nm('pot'), [(0, 0), (0.7, 0.1), (0.75, 0.8), (0.6, 1.0), (0, 1.0)], loc=(0, 0, 1.1), key='iron', segs=12)
    _tent(-5.5, 1.0, 5.0, 5.0, 3.5, 31, collapsed=False)
    _sack(4.5, -2.5, 0.0, s=0.8)
    return finalize('story_prop_03', smooth_angle=30)


def story_04():
    """Abandoned camp: a collapsed tarp over a cold fire, scattered cookware and a tipped stool."""
    reset()
    cyl(nm('gr'), 7.0, 0.15, loc=(0, 0, 0.07), key='dirt', verts=24)
    _campfire(1.0, 0, 4, lit=False)
    _tent(-4.0, 1.5, 6.0, 5.0, 2.0, 41, collapsed=True)
    # scattered cookware
    lathe(nm('pan'), [(0, 0), (0.9, 0.1), (0.9, 0.25), (0, 0.25)], loc=(3.0, -1.5, 0.1), key='iron', segs=12)
    tube(nm('ph'), [(3.0, -1.5, 0.2), (4.6, -2.2, 0.3)], 0.08, 'iron', res=4)
    lathe(nm('cup'), [(0, 0), (0.35, 0), (0.35, 0.5), (0, 0.5)], loc=(2.0, 1.8, 0.0), key='iron', segs=10, rot=(30, 0, 0))
    # tipped stool
    box(nm('ss'), (1.2, 1.2, 0.3), loc=(4.0, 2.0, 1.0), key='wood', rot=(70, 0, 20))
    for k in range(3):
        a = 2 * math.pi * k / 3
        box(nm('sl'), (0.2, 0.2, 1.4), loc=(4.0 + math.cos(a) * 0.4, 2.0 + math.sin(a) * 0.4, 1.4), key='wood', rot=(70, 0, 20))
    _rubble(-5, -3, 2, 3, 42)
    return finalize('story_prop_04', smooth_angle=30)


def story_05():
    """Merchant camp: a wagon with a canvas cover, crates and barrels stacked, a lantern pole."""
    reset()
    cyl(nm('gr'), 8.0, 0.15, loc=(0, 0, 0.07), key='dirt', verts=24)
    f = F(-1.0, 0, 0, 0)
    lbox(f, (8.0, 4.0, 0.5), 0, 0, 2.4, 'wood')
    for s in (-1, 1):
        torus(nm('w'), 1.6, 0.32, loc=f.p(s * 2.6, 2.2, 1.6), key='wood_dark', segs=16, rsegs=5, rot=f.r(0, 90, 0))
        torus(nm('w'), 1.6, 0.32, loc=f.p(s * 2.6, -2.2, 1.6), key='wood_dark', segs=16, rsegs=5, rot=f.r(0, 90, 0))
    # canvas tilt cover (arched hoops)
    for i in range(5):
        x = -3.2 + i * 1.6
        pts = [f.p(x, -math.cos(math.pi * j / 8) * 2.2, 2.9 + math.sin(math.pi * j / 8) * 2.6) for j in range(9)]
        for j in range(8):
            lslab(F(), [(pts[j][0] - 0.8, pts[j][1], pts[j][2]), (pts[j][0] + 0.8, pts[j][1], pts[j][2]),
                        (pts[j + 1][0] + 0.8, pts[j + 1][1], pts[j + 1][2]), (pts[j + 1][0] - 0.8, pts[j + 1][1], pts[j + 1][2])], (0, 0, 0.08), 'canvas')
    _crate(4.5, 1.5, 0.0, s=1.0)
    _crate(4.5, -1.5, 0.0, s=0.9, rz=12)
    _crate(4.6, 0.0, 2.0, s=0.7)
    _barrel(5.8, 1.0, 0.0)
    # lantern pole
    cyl(nm('lp'), 0.2, 6.0, loc=(5.5, -2.5, 0), key='timber', verts=8)
    tube(nm('la'), [(5.5, -2.5, 5.6), (6.3, -2.5, 5.4)], 0.07, 'iron', res=4)
    box(nm('lg'), (0.5, 0.5, 0.7), loc=(6.3, -2.5, 4.9), key='flame')
    return finalize('story_prop_05', smooth_angle=30)


# ===================================================== F09_06..07 ruined watchtowers
def _watchtower(seed, hbreak):
    reset()
    rnd = random.Random(seed)
    R, H, t = 4.5, 24.0, 1.8
    nseg = 24
    hi = H * hbreak          # broken height on the collapsed (low) side
    lo = H                   # intact height on the standing (tall) side
    # one continuous ring wall: each segment is a wide block, heights ramp smoothly from the
    # tall side (angles near 0) to the broken side (angles near pi) with only small jitter,
    # so it reads as a real broken cylinder, not loose spikes.
    seg_w = 2 * math.pi * R / nseg + 0.5
    for i in range(nseg):
        a = 2 * math.pi * i / nseg
        ramp = (1 + math.cos(a)) / 2          # 1 at the tall side, 0 at the broken side
        top = hi + (lo - hi) * ramp + rnd.uniform(-0.8, 0.8)
        x, y = math.cos(a) * R, math.sin(a) * R
        poly_prism(nm('tw'), [(-seg_w / 2, -t / 2), (seg_w / 2, -t / 2), (seg_w / 2, t / 2), (-seg_w / 2, t / 2)], top,
                   loc=(x, y, top / 2), key=rnd.choice(('stone', 'stone', 'stone_dark', 'stone_light')), rot=(0, 0, math.degrees(a) + 90))
    # inner skin so the wall reads as thick stone, not a shell
    lathe(nm('inner'), [(R - t, 0), (R - t, hi * 0.8)], loc=(0, 0, 0), key='stone_dark', segs=nseg) if False else None
    # battered base ring
    lathe(nm('base'), [(R + 1.4, 0), (R + 1.4, 2.0), (R + t / 2, 3.5), (R + t / 2, 0)], loc=(0, 0, 0), key='stone_dark', segs=nseg)
    box(nm('floor'), (2 * (R - t), 2 * (R - t), 0.5), loc=(0, 0, 0.25), key='stone')
    # exposed internal spiral stair up the standing side
    for k in range(int(lo * 0.7 / 1.7)):
        a = k * 0.8
        z = k * 1.7
        box(nm('st'), (2.6, 1.1, 0.4), loc=(math.cos(a) * (R - 1.9), math.sin(a) * (R - 1.9), z + 0.2), key='stone_light', rot=(0, 0, math.degrees(a) + 90))
    # a couple of surviving merlons on the very top of the tall side
    for da in (-0.5, 0.0, 0.5):
        x, y = math.cos(da) * R, math.sin(da) * R
        box(nm('mer'), (2.0, t, 1.8), loc=(x, y, lo + 0.9), key='stone', rot=(0, 0, math.degrees(da) + 90))
    # a narrow window slit on the standing wall
    box(nm('slit'), (0.5, t + 0.3, 2.4), loc=(R, 0, H * 0.6), key='stone_dark')
    # moss up the base, ivy climbing the standing side, rubble spilled on the broken side
    for k in range(12):
        a = rnd.uniform(-1.4, 1.4)
        blob(nm('mo'), rnd.uniform(0.4, 0.8), (math.cos(a) * R, math.sin(a) * R, rnd.uniform(1, 4)), 'moss', subdiv=1, amp=0.3, seed=seed + k)
    for k in range(16):
        a = rnd.uniform(-1.2, 1.2); z = rnd.uniform(1, lo * 0.8)
        ball(nm('iv'), rnd.uniform(0.3, 0.6), (math.cos(a) * (R + 0.3), math.sin(a) * (R + 0.3), z), key=rnd.choice(('ivy', 'leaf_dark')), segs=6, rings=4, scale=(1, 1, 0.6))
    _rubble(-(R + 3), 0, 4.5, 12, seed + 50)


def story_06():
    """Ruined round watchtower, broken off at two-thirds, exposed spiral stair, ivy and rubble."""
    _watchtower(6, 0.62)
    return finalize('story_prop_06', smooth_angle=30)


def story_07():
    """Half-collapsed watchtower, broken low with a split face, heavier rubble spill."""
    _watchtower(7, 0.42)
    return finalize('story_prop_07', smooth_angle=30)


# ===================================================== F09_08..10 foundations
def _foundation(seed, with_hearth=True):
    reset()
    rnd = random.Random(seed)
    W, D = 16.0, 12.0
    cyl(nm('gr'), 0, 0, loc=(0, 0, -5)) if False else None
    box(nm('slab'), (W + 1, D + 1, 0.5), loc=(0, 0, 0.25), key='stone_dark', bev=0.04)
    # partial perimeter walls (low, broken)
    for side, (cx, cy, L, rz) in (('s', (0, -D / 2, W, 0)), ('w', (-W / 2, 0, D, 90)), ('n', (0, D / 2, W, 0))):
        f = F(cx, cy, 0.5, rz)
        _broken_wall(f, L, rnd.uniform(2.5, 4.5), 1.4, seed + hash(side) % 50)
    # a doorway gap already left on the 's' wall via jaggedness; add jambs
    for s in (-1, 1):
        box(nm('jm'), (0.8, 1.4, 3.2), loc=(s * 2.0, -D / 2, 2.1), key='stone_light')
    if with_hearth:
        f = F(0, D / 2 - 0.5, 0.5, 0)
        box(nm('hb'), (3.6, 2.0, 1.0), loc=(0, D / 2 - 1.5, 1.0), key='stone')
        box(nm('hf'), (2.4, 1.2, 2.6), loc=(0, D / 2 - 0.9, 2.3), key='stone_dark')
        cyl(nm('ash'), 1.0, 0.1, loc=(0, D / 2 - 1.5, 1.55), key='we2s_ash', verts=10)
    # floor rubble + grass tufts
    _rubble(0, 0, 6, 10, seed + 70, z=0.5)
    for k in range(10):
        fern() if False else None
        blob(nm('gt'), 0.4, (rnd.uniform(-W / 2, W / 2), rnd.uniform(-D / 2, D / 2), 0.6), 'leaf', subdiv=1, amp=0.4, seed=seed + k)


def story_08():
    """Stone building footprint with partial walls, a doorway and a hearth; rubble on the floor."""
    _foundation(8, with_hearth=True)
    return finalize('story_prop_08', smooth_angle=30)


def story_09():
    """Smaller foundation, two standing wall corners, a collapsed doorway lintel in the rubble."""
    reset()
    rnd = random.Random(9)
    W, D = 12.0, 10.0
    box(nm('slab'), (W + 1, D + 1, 0.5), loc=(0, 0, 0.25), key='stone_dark', bev=0.04)
    # two L-corners
    for (cx, cy, rzs) in ((-W / 2, -D / 2, (0, 90)), (W / 2, D / 2, (180, 270))):
        for rz in rzs:
            f = F(cx, cy, 0.5, rz)
            _broken_wall(f, 5.0, rnd.uniform(3.0, 4.5), 1.4, 90 + int(cx + cy + rz))
    # fallen lintel in rubble
    box(nm('lin'), (4.0, 1.0, 0.8), loc=(1.0, -1.0, 0.9), key='stone_light', rot=(0, 0, 18))
    _rubble(0, 0, 5, 9, 99, z=0.5)
    for k in range(8):
        a = rnd.uniform(0, 6.28)
        blob(nm('gt'), 0.4, (math.cos(a) * 4, math.sin(a) * 3, 0.6), 'leaf', subdiv=1, amp=0.4, seed=90 + k)
    return finalize('story_prop_09', smooth_angle=30)


def story_10():
    """Large hall foundation, a long wall with window gaps, a hearth and scattered column stumps."""
    _foundation(10, with_hearth=True)
    rnd = random.Random(101)
    for x in (-5, 0, 5):
        cyl(nm('col'), 1.0, rnd.uniform(1.5, 3.5), loc=(x, 2.0, 0.5), key='stone_light', verts=12)
        cyl(nm('colc'), 1.2, 0.4, loc=(x, 2.0, 0.5 + rnd.uniform(1.5, 3.5)), key='stone')
    return finalize('story_prop_10', smooth_angle=30)


# ===================================================== F09_11..13 overgrown ruins
def story_11():
    """Ivy-covered stone arch standing alone in rubble, moss at the base, a fallen keystone."""
    reset()
    rnd = random.Random(11)
    W, Hh, t = 10.0, 11.0, 1.6
    for s in (-1, 1):
        box(nm('pier'), (1.8, t, Hh - W / 2), loc=(s * W / 2, 0, (Hh - W / 2) / 2), key='stone')
    # arch voussoirs
    for k in range(9):
        a = math.pi * k / 8
        x = -math.cos(a) * W / 2
        z = (Hh - W / 2) + math.sin(a) * W / 2
        box(nm('vs'), (1.5, t, 1.4), loc=(x, 0, z), key=rnd.choice(('stone', 'stone_light')), rot=(0, math.degrees(a) - 90, 0))
    f = F(0, 0, 0, 0)
    _ivy(f, -W / 2 - 1, W / 2 + 1, 1, Hh, 11, dens=1.2)
    for k in range(12):
        blob(nm('mo'), rnd.uniform(0.3, 0.7), (rnd.uniform(-W / 2, W / 2), -t / 2, rnd.uniform(0.1, 1.0)), 'moss', subdiv=1, amp=0.3, seed=11 + k)
    box(nm('ks'), (1.6, 1.6, 1.2), loc=(2.0, 2.0, 0.6), key='stone_light', rot=(0, 20, 30))  # fallen keystone
    _rubble(0, 0, 5, 8, 111)
    return finalize('story_prop_11', smooth_angle=30)


def story_12():
    """Ruined hall corner with a fallen roof beam leaning across, ivy and moss over broken walls."""
    reset()
    rnd = random.Random(12)
    for (cx, cy, rz) in ((0, -6, 0), (-8, 0, 90)):
        f = F(cx, cy, 0, rz)
        _broken_wall(f, 14.0 if rz == 0 else 12.0, rnd.uniform(5.0, 8.0), 1.6, 120 + int(cx + cy))
        _ivy(f, -6, 6, 1, 7, 120 + int(cx), dens=0.8)
    # fallen roof beam
    beam3((-8, -6, 7.5), (3, 2, 0.5), 0.6, 0.8, 'wood_dark')
    beam3((-6, -6, 6.5), (4, 3, 0.5), 0.5, 0.6, 'timber')
    # broken rafters
    for k in range(4):
        beam3((-7 + k * 1.5, -6, rnd.uniform(4, 7)), (-5 + k * 1.5, -2, 0.5), 0.3, 0.3, 'timber')
    _rubble(-3, -2, 5, 10, 122, z=0.3)
    return finalize('story_prop_12', smooth_angle=30)


def story_13():
    """Ruined bell-tower stump: a broken square tower with the cracked bell fallen at its foot, ivy."""
    reset()
    rnd = random.Random(13)
    W, Hh, t = 8.0, 16.0, 1.6
    # square tower, two walls tall, two broken low
    for (cx, cy, rz, frac) in ((0, -W / 2, 0, 0.95), (-W / 2, 0, 90, 0.9), (0, W / 2, 0, 0.5), (W / 2, 0, 90, 0.45)):
        f = F(cx, cy, 0, rz)
        _broken_wall(f, W, Hh * frac, t, 130 + int(cx + cy + rz), crenel=(frac < 0.6))
    # belfry opening lintel on a tall wall
    box(nm('lint'), (W - 1, t, 1.0), loc=(0, -W / 2, Hh * 0.85), key='stone_light')
    # fallen cracked bell at the foot
    lathe(nm('bell'), [(0, 0), (1.6, 0.1), (1.5, 0.6), (1.2, 1.4), (1.3, 2.2), (0.9, 2.7), (0.5, 2.9), (0, 2.95)], loc=(W / 2 + 2.0, 2.0, 0.0), key='we2s_bell', segs=14, rot=(80, 0, 20))
    torus(nm('by'), 0.4, 0.12, loc=(W / 2 + 2.0, 2.0, 2.9), key='we2s_bell', segs=10, rsegs=4)
    # crack: a wedge cut-out faked by a dark gap box
    box(nm('crk'), (0.2, 1.4, 1.8), loc=(W / 2 + 2.9, 2.0, 1.2), key='stone_dark', rot=(80, 0, 20))
    f = F(0, 0, 0, 0)
    for side in ((0, -W / 2, 0), (-W / 2, 0, 90)):
        _ivy(F(side[0], side[1], 0, side[2]), -W / 2, W / 2, 1, Hh * 0.8, 133 + int(side[0]), dens=0.9)
    _rubble(0, 0, 5, 10, 133)
    return finalize('story_prop_13', smooth_angle=30)


def _item(i, fn):
    return (f'F09_{i:02d}_story_prop_{i:02d}', fn)


BATCHES = {
    'story_a': ('v4_story', [_item(1, story_01), _item(2, story_02), _item(3, story_03),
                             _item(4, story_04), _item(5, story_05), _item(6, story_06),
                             _item(7, story_07)]),
    'story_b': ('v4_story', [_item(8, story_08), _item(9, story_09), _item(10, story_10),
                             _item(11, story_11), _item(12, story_12), _item(13, story_13)]),
}

