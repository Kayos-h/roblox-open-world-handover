"""wh E07 rusty street props: crooked lamps, rusted carts, broken barrels. 1 unit = 1 stud, front -Y."""
import math, random
from mathutils import Vector
import bpy
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, scroll, flame, top_paint
from arch import F, lbox, lbeam, nm
from props import wheel, barrel_body, hoop, staves, plank_box
from nature import rock, blob


# ---- small shared helpers -------------------------------------------------
def rust_streaks(f, x0, x1, y, z0, z1, n, seed):
    rnd = random.Random(seed)
    for i in range(n):
        x = rnd.uniform(x0, x1)
        z = z0 + (z1 - z0) * rnd.random()
        box(nm('rs'), (0.1, 0.05, rnd.uniform(0.4, 1.1)), loc=(x, y, z), key=rnd.choice(['rust', 'tin_b']), rot=(0, 0, rnd.uniform(-8, 8)))


def crooked_lantern(x, y, z, s=1.0, dark_pane=None, lit=True, tilt=(0, 0)):
    """Four-pane iron lantern head centred at (x,y,z), base at its bottom."""
    glass = 'glass_lit' if lit else 'glass_dark'
    lathe(nm('lc'), [(0, 0), (0.42 * s, 0), (0.5 * s, 0.18 * s), (0, 0.18 * s)], loc=(x, y, z), key='rust', segs=4, rot=(tilt[0], tilt[1], 0))
    lathe(nm('lg'), [(0, 0.18 * s), (0.42 * s, 0.18 * s), (0.42 * s, 1.3 * s), (0, 1.3 * s)], loc=(x, y, z), key=glass, segs=4, rot=(tilt[0], tilt[1], 0))
    lathe(nm('lt'), [(0, 1.3 * s), (0.72 * s, 1.3 * s), (0.2 * s, 1.95 * s), (0, 2.05 * s)], loc=(x, y, z), key='rust', segs=4, rot=(tilt[0], tilt[1], 0))
    # corner mullions
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        tube(nm('mu'), [(x + math.cos(a) * 0.46 * s, y + math.sin(a) * 0.46 * s, z + 0.18 * s),
                        (x + math.cos(a) * 0.46 * s, y + math.sin(a) * 0.46 * s, z + 1.3 * s)], 0.05 * s, 'rust', res=4)
    if dark_pane is not None:
        a = dark_pane
        box(nm('dp'), (0.05 * s, 0.6 * s, 0.9 * s), loc=(x + math.cos(a) * 0.44 * s, y + math.sin(a) * 0.44 * s, z + 0.7 * s), key='hole', rot=(0, 0, math.degrees(a)))
    tube(nm('hk'), [(x, y, z + 1.9 * s), (x, y, z + 2.35 * s)], 0.05 * s, 'rust', res=4)


# ============================================================ E07 crooked lamps
def lamp_bent_post():
    """E07_01 - crooked street lamp: a bent, leaning iron post with a cracked lantern, one dark pane, rust streaks."""
    reset()
    lathe(nm('b'), [(0, 0), (1.1, 0), (0.95, 0.4), (0.45, 0.9), (0.4, 1.1), (0, 1.1)], key='rust', segs=10)
    # bent, S-curved post
    tube(nm('p'), [(0, 0, 1.0), (0.25, 0, 4.0), (0.1, 0, 7.0), (0.9, 0, 10.5), (2.2, 0, 13.4)], 0.24, 'rust', res=6, ures=4, taper=[1.1, 1.0, 0.95, 0.9, 0.8])
    # collar ring
    torus(nm('col'), 0.3, 0.07, loc=(2.2, 0, 13.4), key='iron', segs=12, rsegs=4, rot=(0, 20, 0))
    crooked_lantern(2.2, 0, 12.6, s=1.1, dark_pane=math.pi * 0.5, tilt=(0, 9))
    for k in range(3):
        box(nm('dent'), (0.1, 0.12, 0.5), loc=(0.2 + k * 0.1, 0, 3.0 + k * 2.3), key='tin_b', rot=(0, 0, 0))
    top_paint(rock(nm('g'), 1.2, (0, 0, 0.1), 'dirt', seed=71, scale=(1.3, 1.3, 0.25)), 'moss', 0.5, 71)
    return finalize('lamp_bent_post', smooth_angle=30)


def lamp_snapped_arm():
    """E07_02 - crooked lamp with a snapped crossarm: upright post, broken arm hanging the lantern crooked by one chain."""
    reset()
    lathe(nm('b'), [(0, 0), (1.0, 0), (0.85, 0.4), (0.4, 0.9), (0.35, 1.1), (0, 1.1)], key='rust', segs=10)
    tube(nm('p'), [(0, 0, 1.0), (0.05, 0, 6.0), (-0.05, 0, 11.0), (0.1, 0, 13.6)], 0.24, 'rust', res=6, ures=3)
    # crossarm, snapped: a stub plus a broken dangling end
    tube(nm('arm'), [(0.1, 0, 13.4), (1.0, 0, 13.9), (1.9, 0, 13.6)], 0.14, 'rust', res=4)
    for k in range(2):
        tube(nm('jag'), [(1.9, 0, 13.6), (2.1 + k * 0.1, 0, 13.4 - k * 0.1)], 0.06, 'rust', res=3)
    # lantern hangs crooked from a single chain
    from kitlib import chain as _chain
    _chain(nm('ch'), (1.85, 0, 13.4), (2.1, 0, 11.7), link=0.22, thick=0.04)
    crooked_lantern(2.05, 0, 10.8, s=1.0, dark_pane=math.pi * 1.5, tilt=(0, -14))
    scroll(nm('sc'), (0.5, 0, 12.4), 0.05, 0.4, 1.2, plane='XZ', key='rust', radius=0.05)
    top_paint(rock(nm('g'), 1.1, (0, 0, 0.1), 'dirt', seed=72, scale=(1.3, 1.3, 0.25)), 'moss', 0.5, 72)
    return finalize('lamp_snapped_arm', smooth_angle=30)


def lamp_wall_bracket():
    """E07_03 - lamp leaning on a wall bracket: a stub of broken wall with an iron scrolled bracket holding a tilted lantern."""
    reset()
    # broken wall stub it leans on
    w = box(nm('wall'), (4.0, 2.0, 9.0), loc=(0, 1.2, 4.5), key='stone')
    from capital import stone_face
    stone_face(F(0, 0.2, 0, 0), -1.9, 1.9, 0.5, 8.5, 18, 73, keys=('stone', 'stone_dark', 'stone_light'))
    # jagged broken top
    rnd = random.Random(73)
    for i in range(6):
        x = -1.8 + i * 0.7
        box(nm('br'), (0.7, 2.0, rnd.uniform(0.4, 1.4)), loc=(x, 1.2, 9.0 + rnd.uniform(0, 0.4)), key=rnd.choice(['stone', 'stone_dark']), rot=(rnd.uniform(-6, 6), 0, 0))
    top_paint(w, 'moss', 0.3, 73)
    # iron bracket on the front face
    f = F(0, 0.2, 0, 0)
    lbox(f, (0.5, 0.3, 1.0), 0.0, -0.1, 6.5, 'rust')
    tube(nm('arm'), [f.p(0, -0.1, 6.8), f.p(0, -1.4, 7.0), f.p(0, -2.4, 6.6)], 0.1, 'rust', res=4)
    scroll(nm('sc1'), (0, -0.8, 6.3), 0.05, 0.45, 1.3, plane='YZ', key='rust', radius=0.05, off=(0.2, 0, 0))
    scroll(nm('sc2'), (0, -1.6, 6.3), 0.05, 0.35, 1.2, plane='YZ', key='rust', radius=0.05, off=(0.2, 0, 0))
    from kitlib import chain as _chain
    _chain(nm('ch'), f.p(0, -2.3, 6.6), f.p(0, -2.3, 5.4), link=0.2, thick=0.04)
    crooked_lantern(0.0, -2.3, 4.4, s=1.0, dark_pane=0.0, tilt=(6, 0))
    return finalize('lamp_wall_bracket', smooth_angle=28)


# ============================================================ E07 rusted carts
def _cart_bed(prefix, L, Wd, zb, tilt, plank_keys=('wood_old', 'wood_grey'), missing=()):
    """Tilted cart bed of planks with rusty iron side straps. Returns objs created."""
    rnd = random.Random(hash(prefix) & 255)
    before = set(o.name for o in bpy.context.scene.objects)
    n = 6
    for i in range(n):
        if i in missing:
            continue
        box(nm('pl'), (L, Wd / n - 0.05, 0.2), loc=(0, -Wd / 2 + Wd / n * (i + 0.5), zb), key=rnd.choice(plank_keys))
    for s in (-1, 1):
        box(nm('sd'), (L, 0.2, 0.9), loc=(0, s * Wd / 2, zb + 0.5), key='wood_old')
        box(nm('st'), (L, 0.25, 0.14), loc=(0, s * Wd / 2 + s * 0.03, zb + 0.9), key='rust')
        for k in range(3):
            box(nm('strap'), (0.14, 0.26, 0.9), loc=(-L / 2 + 0.4 + k * (L - 0.8) / 2, s * Wd / 2, zb + 0.5), key='rust')
    box(nm('ed'), (0.2, Wd, 1.0), loc=(L / 2, 0, zb + 0.4), key='wood_grey', rot=(0, 20, 0))
    for o in bpy.context.scene.objects:
        if o.name not in before:
            o.rotation_euler.x += math.radians(tilt)


def cart_handcart():
    """E07_04 - rusty two-wheel handcart: tipped forward on a broken strut, boards, long handles, rusted rims."""
    reset()
    _cart_bed('hc', 6.0, 3.6, 2.4, 10, missing=(4,))
    wheel(nm('w1'), 1.7, (0.6, -2.0, 1.6), axis='Y', key='wood_old', spokes=10)
    wheel(nm('w2'), 1.7, (0.6, 2.0, 1.5), axis='Y', key='wood_old', spokes=10)
    # rust the tyres
    for s in (-1, 1):
        torus(nm('ty'), 1.7, 0.08, loc=(0.6, s * 2.0, 1.55), key='rust', segs=24, rsegs=4, rot=(90, 0, 0))
    box(nm('ax'), (0.3, 4.4, 0.3), loc=(0.6, 0, 1.55), key='rust')
    for s in (-1, 1):
        lbeam(F(), (-2.9, s * 1.4, 2.1), (-6.4, s * 1.3, 0.6), 0.22, 'wood_old')
    # one broken front strut lying on the ground
    lbeam(F(), (2.9, -0.8, 0.3), (5.0, -1.4, 0.2), 0.2, 'wood_rot')
    rock(nm('r1'), 0.6, (3.2, 1.6, 0.2), 'stone', seed=74, scale=(1.3, 1, 0.6))
    return finalize('cart_handcart', smooth_angle=25)


def cart_ox_broken_axle():
    """E07_05 - rusted ox-cart with a broken rear axle: four wheels, one collapsed, splintered axle, big tilt, draw pole."""
    reset()
    _cart_bed('ox', 9.0, 4.4, 3.0, 13, missing=(2,))
    # three standing wheels + one collapsed flat
    wheel(nm('w1'), 2.1, (3.0, -2.3, 2.0), axis='Y', key='wood_old', spokes=10)
    wheel(nm('w2'), 2.1, (3.0, 2.3, 1.9), axis='Y', key='wood_old', spokes=10)
    wheel(nm('w3'), 2.1, (-3.0, -2.3, 1.9), axis='Y', key='wood_old', spokes=10)
    wheel(nm('w4c'), 2.1, (-2.6, 3.8, 0.25), axis='Z', key='wood_rot', spokes=10)
    for (x, s) in ((3.0, -1), (3.0, 1), (-3.0, -1)):
        torus(nm('ty'), 2.1, 0.09, loc=(x, s * 2.3, 2.0 if x > 0 else 1.9), key='rust', segs=24, rsegs=4, rot=(90, 0, 0))
    # front axle intact, rear axle snapped with splinters
    box(nm('ax1'), (0.35, 5.0, 0.35), loc=(3.0, 0, 2.0), key='rust')
    tube(nm('ax2'), [(-3.0, -2.3, 1.9), (-3.0, 0.8, 1.3)], 0.3, 'rust', res=6)
    for k in range(3):
        tube(nm('jag'), [(-3.0, 0.8, 1.3), (-3.0 + (k - 1) * 0.2, 1.4 + k * 0.2, 1.0)], 0.08, 'wood_rot', res=3)
    tube(nm('pole'), [(4.5, 0, 2.2), (8.5, 0.5, 1.0), (11.0, 0.8, 0.5)], 0.22, 'wood_old', res=6)
    box(nm('yoke'), (0.35, 3.4, 0.35), loc=(10.4, 0.8, 0.7), key='wood_old')
    rock(nm('r1'), 0.7, (-4.0, -1.0, 0.2), 'stone', seed=75, scale=(1.3, 1, 0.6))
    return finalize('cart_ox_broken_axle', smooth_angle=25)


def cart_hay_wagon_wreck():
    """E07_06 - hay wagon wreck: tipped side with spilled hay, bare ladder racks, a wheel off, torn canvas strip."""
    reset()
    rnd = random.Random(76)
    _cart_bed('hw', 10.0, 4.6, 3.2, 16)
    # ladder racks (hay wagon uprights + rails) front and back
    for ex in (-1, 1):
        before = set(o.name for o in bpy.context.scene.objects)
        for k in range(4):
            box(nm('up'), (0.2, 0.2, 2.6), loc=(ex * 4.0, -1.8 + k * 1.2, 4.6), key='wood_old')
        box(nm('rl'), (0.2, 4.4, 0.18), loc=(ex * 4.0, 0, 5.7), key='wood_old')
        for o in bpy.context.scene.objects:
            if o.name not in before:
                o.rotation_euler.x += math.radians(16)
    wheel(nm('w1'), 2.0, (3.2, -2.4, 1.9), axis='Y', key='wood_old', spokes=10)
    wheel(nm('w2'), 2.0, (-3.2, -2.4, 1.8), axis='Y', key='wood_old', spokes=10)
    wheel(nm('w3'), 2.0, (3.2, 2.4, 1.8), axis='Y', key='wood_old', spokes=10)
    wheel(nm('w4'), 2.0, (-5.6, 4.2, 0.25), axis='Z', key='wood_rot', spokes=10)
    box(nm('ax'), (0.32, 5.0, 0.32), loc=(3.2, 0, 1.9), key='rust')
    box(nm('ax2'), (0.32, 5.0, 0.32), loc=(-3.2, 0, 1.8), key='rust')
    # spilled hay: clumps tumbling off the high side and on the ground
    for i in range(10):
        x = rnd.uniform(-4, 4)
        y = rnd.uniform(-3.4, -2.0)
        z = rnd.uniform(0.4, 4.2)
        blob(nm('hay'), rnd.uniform(0.9, 1.5), (x, y, z), rnd.choice(['thatch', 'grass_dry']), subdiv=1, amp=0.3, scale=(1.3, 1.1, 0.7), seed=76 + i)
    for i in range(14):
        x = rnd.uniform(-5, 5); y = rnd.uniform(-5.5, -3.0)
        tube(nm('straw'), [(x, y, 0.03), (x + rnd.uniform(-0.6, 0.6), y + rnd.uniform(-0.4, 0.4), 0.1)], 0.04, rnd.choice(['thatch', 'grass_dry']), res=2)
    # torn canvas strip over one rack
    from props import cloth
    cloth(nm('cv'), 3.0, 2.0, (1.5, -2.2, 5.8), 'canvas_b', waves=1.2, amp=0.2, seed=76, rot=(70, 0, 10))
    return finalize('cart_hay_wagon_wreck', smooth_angle=25)


# ============================================================ E07 broken barrels
def barrel_staved_pile():
    """E07_07 - a pile of staved barrels: two burst with splayed staves, fallen hoops, loose staves, scattered boards."""
    reset()
    rnd = random.Random(77)
    # one intact leaning barrel
    before = set(o.name for o in bpy.context.scene.objects)
    barrel_body(nm('b1'), loc=(-2.0, 0.6, 0), h=3.4)
    for o in bpy.context.scene.objects:
        if o.name not in before:
            o.rotation_euler.y += math.radians(72)
            o.location = Vector(o.location) + Vector((0, 0, 0.9))
    # one burst barrel: splayed staves from a base ring
    n = 13
    for i in range(n):
        a = 2 * math.pi * i / n
        h = rnd.uniform(1.8, 3.4)
        lean = rnd.uniform(10, 46)
        x, y = 1.6 + math.cos(a) * 1.25, 0.2 + math.sin(a) * 1.25
        o = box(nm('sv'), (0.6, 0.16, h), loc=(0, 0, 0), key=rnd.choice(['wood', 'wood_old']))
        o.rotation_euler = (0, math.radians(lean), a)
        o.location = (x + math.cos(a) * math.sin(math.radians(lean)) * h / 2, y + math.sin(a) * math.sin(math.radians(lean)) * h / 2, h / 2 * math.cos(math.radians(lean)))
    cyl(nm('bt'), 1.25, 0.2, loc=(1.6, 0.2, 0.0), key='wood_old', verts=14)
    # fallen hoops and loose staves
    torus(nm('h1'), 1.3, 0.08, loc=(3.4, -1.4, 0.1), key='rust', segs=20, rsegs=4, rot=(80, 0, 0))
    torus(nm('h2'), 1.25, 0.08, loc=(-0.4, -2.2, 0.4), key='rust', segs=20, rsegs=4, rot=(60, 20, 0))
    for k in range(4):
        box(nm('lsv'), (0.6, 0.16, rnd.uniform(2.0, 3.0)), loc=(rnd.uniform(-1, 3.5), rnd.uniform(-2.5, -1.2), 0.1), key=rnd.choice(['wood_old', 'wood_grey']),
            rot=(90, 0, rnd.uniform(0, 180)))
    return finalize('barrel_staved_pile', smooth_angle=30)


def barrel_rolled_grain():
    """E07_08 - a barrel rolled on its side with the lid out and spilled grain pouring from the mouth."""
    reset()
    rnd = random.Random(78)
    before = set(o.name for o in bpy.context.scene.objects)
    barrel_body(nm('b'), loc=(0, 0, 0), h=4.0, open_top=True)
    for o in bpy.context.scene.objects:
        if o.name not in before:
            o.rotation_euler.y += math.radians(90)
            o.location = Vector(o.location) + Vector((2.0, 0, 1.5))
    # the lid lying nearby
    cyl(nm('lid'), 1.2, 0.12, loc=(-2.4, 1.0, 0.2), key='wood_light', verts=20, rot=(4, 86, 0))
    # grain spilling out of the open (now sideways) mouth: a widening fan
    mx = -2.0  # open end of the rolled barrel
    for i in range(60):
        t = rnd.random()
        spread = 0.3 + t * 2.4
        x = mx - t * 2.6 + rnd.uniform(-0.2, 0.2)
        y = rnd.uniform(-spread, spread)
        z = max(0.05, 1.5 - t * 1.5 + rnd.uniform(-0.1, 0.1))
        ball(nm('gr'), 0.11, loc=(x, y, z), key=rnd.choice(['thatch', 'grass_dry']), segs=5, rings=4, scale=(1.3, 1, 0.7))
    # a small heap at the end
    blob(nm('heap'), 1.1, (mx - 2.6, 0, 0.0), 'thatch', subdiv=2, amp=0.25, scale=(1.5, 1.6, 0.3), seed=78)
    return finalize('barrel_rolled_grain', smooth_angle=30)


def barrel_burst_hoop_rain():
    """E07_09 - a standing barrel with a burst hoop and bulging staves, full of dark rainwater with floating leaves."""
    reset()
    rnd = random.Random(79)
    # body: staves, some sprung outward near the burst
    n = 16
    H = 4.2
    for i in range(n):
        a = 2 * math.pi * i / n
        spr = 0.0
        # burst area around a = 0
        da = min(abs(a), abs(a - 2 * math.pi))
        if da < 1.1:
            spr = (1.1 - da) * 0.5
        bulge = 1.3 + 0.18 * math.sin(math.pi * 0.5) + spr
        x, y = math.cos(a) * (1.3 + spr), math.sin(a) * (1.3 + spr)
        o = box(nm('sv'), (0.56, 0.16, H), loc=(x, y, H / 2), key=rnd.choice(['wood', 'wood_old']), rot=(0, 0, math.degrees(a)))
        if spr > 0.05:
            o.rotation_euler = (math.radians(-spr * 30 * math.sin(a)), math.radians(spr * 30 * math.cos(a)), a)
    cyl(nm('bt'), 1.3, 0.25, loc=(0, 0, 0.12), key='wood_old', verts=16)
    # hoops: top one burst (two broken arcs), others intact
    hoop(nm('h_bot'), 1.34, 0.4, key='rust')
    hoop(nm('h_mid'), 1.34, 2.1, key='rust')
    # burst top hoop: two arcs sprung apart
    for (a0, a1, off) in ((1.0, math.pi, 0.1), (math.pi + 0.4, 2 * math.pi - 1.0, -0.1)):
        pts = [(math.cos(a0 + (a1 - a0) * t / 8) * 1.42, math.sin(a0 + (a1 - a0) * t / 8) * 1.42, 3.7 + off * math.sin(t)) for t in range(9)]
        tube(nm('harc'), pts, 0.08, 'rust', res=4)
    # a loose sprung hoop end sticking out
    tube(nm('hspr'), [(1.42, 0, 3.7), (2.1, 0.4, 3.9)], 0.07, 'rust', res=4)
    # dark rainwater surface near the top with floating leaves
    cyl(nm('water'), 1.22, 0.05, loc=(0, 0, 3.5), key='water_dark', verts=16)
    for i in range(6):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, 0.9)
        box(nm('leaf'), (0.4, 0.3, 0.03), loc=(math.cos(a) * d, math.sin(a) * d, 3.53), key=rnd.choice(['leaf_dark', 'autumn_b', 'autumn_a']), rot=(0, 0, rnd.uniform(0, 180)))
    return finalize('barrel_burst_hoop_rain', smooth_angle=30)


BATCHES = {
    'lamps': ('v4_rusty', [
        ('E07_01_rusty_prop_01', lamp_bent_post, (1.0, -1.1, 0.5)),
        ('E07_02_rusty_prop_02', lamp_snapped_arm, (1.0, -1.1, 0.5)),
        ('E07_03_rusty_prop_03', lamp_wall_bracket, (1.0, -1.3, 0.35)),
    ]),
    'carts': ('v4_rusty', [
        ('E07_04_rusty_prop_04', cart_handcart, (1.0, -1.1, 0.4)),
        ('E07_05_rusty_prop_05', cart_ox_broken_axle, (1.0, -1.2, 0.4)),
        ('E07_06_rusty_prop_06', cart_hay_wagon_wreck, (1.0, -1.1, 0.45)),
    ]),
    'barrels': ('v4_rusty', [
        ('E07_07_rusty_prop_07', barrel_staved_pile, (1.0, -1.1, 0.5)),
        ('E07_08_rusty_prop_08', barrel_rolled_grain, (1.0, -1.1, 0.4)),
        ('E07_09_rusty_prop_09', barrel_burst_hoop_rain, (1.0, -1.1, 0.5)),
    ]),
}
