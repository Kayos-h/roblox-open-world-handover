"""v4_wk_landmarks - worker wk. Landmark trail set F11 x9 -> category v4_landmarks.
Lookouts x2, cave entrances x3, cliff-trail pieces x3, summit tower.

Stone/timber built with kitlib primitives; rocky crag bases reuse my rock helpers from
v4_wk_rocks (_pillar / _flat_scree / _roughen) and wd's palette. Caves have a closed dark back
(wk_cave_dark) so a viewer sees black, not through. Walkable trail surfaces are 6 wide with
tileable ends. Enterable pieces get a door marker at the threshold. New keys wk_ prefixed.
"""
import math, random, bmesh
from mathutils import Vector, noise as N
from kitlib import reset, finalize, PAL, box, cyl, ball, lathe, tube, torus, poly_prism, top_paint, _obj_from_bm, mat
from nature import rock, blob
from v4_elf import nm, lantern
import v4util as U
from v4_wk_rocks import _pillar, _flat_scree, _roughen, _mini_pine, _geo_paint, _facet
from v4_wd_peaks import _landform, _paint, _scree_skirt

PI = math.pi

for k, v in {
    'wk_timber':      ((104, 78, 52),   'Wood',       0.00, 0.90, 0),
    'wk_timber_dk':   ((74, 54, 38),    'Wood',       0.00, 0.92, 0),
    'wk_plank':       ((150, 118, 80),  'WoodPlanks', 0.00, 0.85, 0),
    'wk_plank_dk':    ((120, 92, 62),   'WoodPlanks', 0.00, 0.88, 0),
    'wk_rail':        ((132, 102, 70),  'Wood',       0.00, 0.88, 0),
    'wk_rope':        ((168, 142, 96),  'Fabric',     0.00, 1.00, 0),
    'wk_rail_roof':   ((96, 70, 56),    'Slate',      0.00, 0.90, 0),
    'wk_rust_rail':   ((96, 74, 54),    'CorrodedMetal', 0.5, 0.85, 0),
    'wk_cart':        ((110, 86, 62),   'Wood',       0.00, 0.90, 0),
    'wk_cart_metal':  ((80, 70, 64),    'CorrodedMetal', 0.5, 0.85, 0),
    'wk_flag':        ((150, 60, 52),   'Fabric',     0.00, 0.95, 0),
    'wk_brazier_fire':((255, 150, 60),  'Neon',       0.00, 0.50, 2.2),
    'wk_ember':       ((255, 110, 40),  'Neon',       0.00, 0.50, 2.0),
}.items():
    PAL[k] = v

ROCK = ('wd_rock_grey', 'wd_rock_dark', 'wd_rock_light')


def _crag(seed, R, H, cx=0.0, cy=0.0, key='wd_rock_grey'):
    """A rocky crag base (carved, stratified) for landmarks that sit on rock."""
    o = _pillar(seed, H, R, R * 0.8, 'crag%d' % seed, cx=cx, cy=cy)
    return o


def _stair_flight(x0, z0, x1, z1, w, steps, key, rise_key=None):
    """A straight run of stone/wood steps from (x0,z0) to (x1,z1), front faces -Y."""
    rise_key = rise_key or key
    for i in range(steps):
        t0 = i / steps
        sx = x0 + (x1 - x0) * t0
        sz = z0 + (z1 - z0) * t0
        dx = (x1 - x0) / steps
        dz = (z1 - z0) / steps
        box(nm('step'), (abs(dx) + 1.2, w, 0.5), loc=(sx + dx / 2, 0, sz + 0.25), key=key, bev=0.05, segs=1)
        box(nm('riser'), (0.5, w, abs(dz) + 0.6), loc=(sx, 0, sz), key=rise_key, bev=0.03, segs=1)


# ================================================================== F11_01..02 LOOKOUTS
def lookout_stone():
    """F11_01: stone lookout platform with a parapet and steps up to it."""
    reset()
    seed = 1101
    rnd = random.Random(seed)
    W, D, H = 16.0, 14.0, 5.0
    # rock plinth
    o = box(nm('plinth'), (W, D, H), loc=(0, 0, H / 2), key='wd_rock_grey', bev=0.3, segs=1)
    top_paint(o, 'wd_moss', 0.9, seed, noise_amt=0.1)
    # platform slab
    box(nm('deck'), (W - 1.0, D - 1.0, 0.6), loc=(0, 0, H + 0.3), key='ev_stone', bev=0.1, segs=1)
    # parapet on three sides (open toward -Y, the view side, with a low wall)
    pw, ph = 0.8, 2.2
    for (lx, ly, sx, sy) in ((0, D / 2 - 0.4, W - 1.0, pw), (-(W / 2 - 0.4), 0, pw, D - 1.0), (W / 2 - 0.4, 0, pw, D - 1.0)):
        box(nm('par'), (sx, sy, ph), loc=(lx, ly, H + 0.6 + ph / 2), key='ev_stone', bev=0.08, segs=1)
    # crenellations on the back parapet
    for x in range(-6, 7, 3):
        box(nm('cren'), (1.4, pw, 1.0), loc=(x, D / 2 - 0.4, H + 0.6 + ph + 0.5), key='ev_stone', bev=0.06, segs=1)
    # low front parapet (view side)
    box(nm('frontpar'), (W - 1.0, pw, 1.1), loc=(0, -(D / 2 - 0.4), H + 0.6 + 0.55), key='ev_stone', bev=0.08, segs=1)
    # steps up on the -Y front
    _stair_flight(0, 0.0, 0, 0.0, 5.0, 1, 'ev_stone')   # placeholder removed below
    for i in range(6):
        box(nm('step'), (5.0, 1.3, 0.55), loc=(0, -(D / 2) - 0.7 - i * 1.3, (H + 0.3) * (1 - i / 6)), key='ev_stone', bev=0.05, segs=1)
    U.marker('mk_door', (0, -(D / 2) - 0.7, 0.1))
    _flat_scree(seed, 0, 0, W * 0.7, ROCK, n=8)
    return finalize('landmark_trail_01', smooth_angle=30)


def lookout_timber():
    """F11_02: timber watch lookout on a cliff ledge, railing and a roof."""
    reset()
    seed = 1102
    rnd = random.Random(seed)
    # rock ledge it stands on
    led = box(nm('ledge'), (18.0, 12.0, 4.0), loc=(0, 2.0, 2.0), key='wd_rock_dark', bev=0.3, segs=1)
    top_paint(led, 'wd_moss', 0.85, seed)
    W, D = 12.0, 9.0
    deckz = 4.5
    # four posts + deck
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl(nm('post'), 0.4, deckz + 0.5, loc=(sx * (W / 2 - 0.6), sy * (D / 2 - 0.6) - 1.0, 0), key='wk_timber', verts=8)
    box(nm('deck'), (W, D, 0.5), loc=(0, -1.0, deckz), key='wk_plank', bev=0.05, segs=1)
    # railings on 3 sides (open at the back for access), with balusters
    for (lx, ly, sx, sy, horiz) in ((0, -1.0 - D / 2 + 0.3, W, 0.25, True),
                                    (-(W / 2 - 0.2), -1.0, 0.25, D, False),
                                    (W / 2 - 0.2, -1.0, 0.25, D, False)):
        box(nm('rail'), (sx, sy, 0.25), loc=(lx, ly, deckz + 2.0), key='wk_rail', bev=0.03, segs=1)
        n = int((sx if horiz else sy)) // 2
        for i in range(max(2, n)):
            if horiz:
                bx = -W / 2 + 0.5 + i * (W - 1) / max(1, n - 1)
                by = ly
            else:
                bx = lx
                by = -1.0 - D / 2 + 0.5 + i * (D - 1) / max(1, n - 1)
            cyl(nm('bal'), 0.1, 1.9, loc=(bx, by, deckz + 0.3), key='wk_rail', verts=5)
    # pitched roof on four corner posts
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl(nm('rpost'), 0.3, 4.0, loc=(sx * (W / 2 - 0.8), sy * (D / 2 - 0.8) - 1.0, deckz + 0.5), key='wk_timber', verts=6)
    rz = deckz + 4.5
    for s, sgn in ((0, -1), (1, 1)):
        box(nm('roof'), (W + 1.6, 0.4, 6.0), loc=(0, -1.0 + sgn * (D / 4), rz + 1.0), rot=(sgn * 32, 0, 0), key='wk_rail_roof', bev=0.05, segs=1)
    box(nm('ridge'), (W + 1.8, 0.5, 0.5), loc=(0, -1.0, rz + 2.6), key='wk_timber_dk', bev=0.05, segs=1)
    # ladder/step up at the back
    for i in range(5):
        box(nm('step'), (4.0, 1.1, 0.4), loc=(0, -1.0 + D / 2 + 0.6 + i * 1.1, deckz * (1 - i / 5)), key='wk_plank_dk', bev=0.04, segs=1)
    U.marker('mk_door', (0, -1.0 + D / 2 + 0.6, deckz + 0.3))
    return finalize('landmark_trail_02', smooth_angle=30)


# ================================================================== F11_03..05 CAVE ENTRANCES
def _cave_mouth(seed, W, Hc, D, name, back_key='wk_cave_dark'):
    """A rock hillside with a recessed ARCHED dark opening facing -Y. Built as a solid faceted rock
    mound whose front has an arched tunnel bored into it; the tunnel interior (floor, ceiling, back,
    side walls) is all dark so a viewer sees black, not through. Opening ~0.42*W wide x ~0.72*Hc high.
    Returns the opening half-width/height for stalactite/prop placement."""
    rnd = random.Random(seed)
    ow = W * 0.42 / 2          # opening half-width
    oh = Hc * 0.72             # opening height
    # --- dark interior box set well back, so the recess reads black ---
    box(nm('iback'), (ow * 2 + 1.0, 1.5, oh + 2.0), loc=(0, D, oh / 2), key=back_key, bev=0, segs=1)
    box(nm('ifloor'), (ow * 2 + 1.0, D, 0.5), loc=(0, D / 2, 0.25), key=back_key, bev=0, segs=1)
    box(nm('iceil'), (ow * 2 + 1.0, D, 0.5), loc=(0, D / 2, oh), key=back_key, bev=0, segs=1)
    for sx in (-1, 1):
        box(nm('iside'), (0.6, D, oh), loc=(sx * ow, D / 2, oh / 2), key=back_key, bev=0, segs=1)
    # --- solid rock mound around the opening: a faceted dome, with the front-centre carved away ---
    nx, nz = 34, 20
    bm = bmesh.new(); rings = []
    Rm = W / 2
    for iz in range(nz + 1):
        t = iz / nz
        z = Hc * 1.05 * t
        rad = Rm * (1 - 0.55 * t) ** 0.9
        ring = []
        for ix in range(nx):
            a = 2 * PI * ix / nx
            cx, cy = math.cos(a), math.sin(a)
            disp = 0.0
            for (fr, amp) in [(1.2, 1.0), (2.8, 0.5), (6.0, 0.25)]:
                disp += amp * N.noise(Vector((cx * fr + seed, cy * fr + seed * 2, z * fr * 0.1)))
            rr = rad * (1.0 + 0.14 * disp)
            x, y = cx * rr, cy * rr * 0.85 + D * 0.55      # push mass toward +Y so front can be carved
            ring.append(bm.verts.new((x, y, z)))
        rings.append(ring)
    for A, B in zip(rings, rings[1:]):
        n = len(A)
        for i in range(n):
            bm.faces.new((A[i], A[(i + 1) % n], B[(i + 1) % n], B[i]))
    bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    # carve the arched mouth: delete faces whose centre is inside the arch tunnel volume (front, low)
    arch = []
    for f in bm.faces:
        c = f.calc_center_median()
        inside = (abs(c.x) < ow + 0.6) and (c.z < oh + 0.3) and (c.y < D * 0.6)
        # arched top: within an ellipse near the crown
        if abs(c.x) < ow and c.z > oh - ow:
            inside = inside and ((c.x / ow) ** 2 + ((c.z - (oh - ow)) / ow) ** 2 < 1.1 or c.z < oh - ow)
        if inside:
            arch.append(f)
    bmesh.ops.delete(bm, geom=arch, context='FACES')
    o = _obj_from_bm(name + '_mound', bm, 'wd_rock_grey')
    _geo_paint(o, seed, Hc * 1.05, ROCK)
    top_paint(o, 'wd_moss', 0.82, seed, noise_amt=0.4)     # patchy moss on upper faces
    # carved rock arch rim framing the mouth (a ring of dark rock chunks following the arch)
    for i in range(11):
        ang = PI * i / 10
        ax = math.cos(ang) * (ow + 0.8)
        az = max(0.4, (oh - ow) + math.sin(ang) * (ow + 0.8))
        rock(nm('rim'), rnd.uniform(1.0, 1.6), (ax, -0.2, az), 'wd_rock_dark', seed=seed + i, scale=(1.1, 1.3, 1.0), subdiv=2, amp=0.3)
    _flat_scree(seed, 0, -D * 0.2, W * 0.6, ROCK, n=7)
    return ow, oh


def cave_natural():
    """F11_03: natural cavern mouth with stalactites and darkness inside."""
    reset()
    seed = 1103
    rnd = random.Random(seed)
    W, Hc, D = 28.0, 15.0, 12.0
    ow, oh = _cave_mouth(seed, W, Hc, D, 'cave_natural')
    # stalactites from the arch ceiling, stalagmites from the floor (within the opening)
    for i in range(8):
        x = rnd.uniform(-ow + 0.6, ow - 0.6)
        h = rnd.uniform(2.0, 4.5)
        cyl(nm('stalac'), rnd.uniform(0.4, 0.8), h, loc=(x, rnd.uniform(1.5, 4), oh - h + 0.3), key='wk_cave_dark', verts=6, r2=0.05)
        if i % 2 == 0:
            hh = rnd.uniform(1.2, 2.6)
            cyl(nm('stalag'), rnd.uniform(0.4, 0.8), hh, loc=(x + rnd.uniform(-1, 1), rnd.uniform(2, 5), 0.2), key='wk_cave_dark', verts=6, r2=0.1)
    U.marker('mk_door', (0, -0.5, 0.2))
    return finalize('landmark_trail_03', smooth_angle=26)


def cave_mine():
    """F11_04: mine entrance with timber supports, rails and a cart."""
    reset()
    seed = 1104
    rnd = random.Random(seed)
    W, Hc, D = 26.0, 13.0, 12.0
    ow, oh = _cave_mouth(seed, W, Hc, D, 'cave_mine')
    # timber portal frame at the opening edges: two posts + a lintel + angle braces
    for sx in (-1, 1):
        box(nm('post'), (1.2, 1.2, oh), loc=(sx * (ow + 0.3), -0.5, oh / 2), key='wk_timber', bev=0.06, segs=1)
        box(nm('brace'), (0.8, 0.8, 4.0), loc=(sx * (ow - 0.8), -0.5, oh - 2.2), rot=(0, sx * 30, 0), key='wk_timber_dk', bev=0.05, segs=1)
    box(nm('lintel'), (ow * 2 + 2.4, 1.4, 1.4), loc=(0, -0.5, oh + 0.3), key='wk_timber', bev=0.08, segs=1)
    box(nm('lintel2'), (ow * 2 + 3.2, 1.0, 0.8), loc=(0, -0.5, oh + 1.3), key='wk_timber_dk', bev=0.06, segs=1)
    # rails running out of the mouth (two steel rails + sleepers)
    for i in range(10):
        box(nm('sleeper'), (ow * 1.4, 0.5, 0.3), loc=(0, -0.5 - i * 1.4, 0.15), key='wk_timber_dk', bev=0.03, segs=1)
    for sx in (-1, 1):
        box(nm('rail'), (0.3, 14.0, 0.3), loc=(sx * 2.0, -7.0, 0.35), key='wk_cart_metal', bev=0.02, segs=1)
    # ore cart at the mouth
    cx, cy = 0, -9.0
    box(nm('cartbody'), (3.6, 3.0, 2.2), loc=(cx, cy, 1.6), key='wk_cart', bev=0.08, segs=1)
    box(nm('cartin'), (3.0, 2.3, 1.6), loc=(cx, cy, 2.0), key='wk_cave_dark', bev=0.02, segs=1)
    for sx in (-1, 1):
        for sy in (-1, 1):
            torus(nm('wheel'), 0.8, 0.22, loc=(cx + sx * 1.6, cy + sy * 1.3, 0.8), key='wk_cart_metal', segs=12, rsegs=5, rot=(0, 90, 0))
    for i in range(5):
        a = rnd.uniform(0, 6.28)
        rock(nm('ore'), rnd.uniform(0.4, 0.7), (cx + math.cos(a), cy + math.sin(a) * 0.6, 2.4), 'wd_rock_dark', seed=seed + i, scale=(1.1, 1, 0.8), subdiv=2, amp=0.3)
    U.marker('mk_door', (0, -0.5, 0.2))
    return finalize('landmark_trail_04', smooth_angle=28)


def cave_carved():
    """F11_05: carved rock doorway with an ancient lintel (original design, not Black Clover)."""
    reset()
    seed = 1105
    rnd = random.Random(seed)
    W, Hc, D = 26.0, 14.0, 12.0
    ow, oh = _cave_mouth(seed, W, Hc, D, 'cave_carved')
    # carved stone door surround framing the opening: squared jambs + a stepped lintel + grooves
    for sx in (-1, 1):
        box(nm('jamb'), (2.2, 2.2, oh), loc=(sx * (ow + 1.1), -1.0, oh / 2), key='ev_stone', bev=0.1, segs=1)
        for g in range(3):
            box(nm('groove'), (0.3, 0.3, oh - 2), loc=(sx * (ow + 1.1) - 0.8 + g * 0.8, -2.1, oh / 2), key='ev_stone_dark', bev=0.02, segs=1)
    # stepped lintel above the opening
    for i, (wd, zz) in enumerate(((ow * 2 + 3.0, oh + 0.8), (ow * 2 + 1.6, oh + 1.8), (ow * 2 + 0.4, oh + 2.6))):
        box(nm('lint'), (wd, 2.5, 1.0), loc=(0, -1.0, zz), key='ev_stone', bev=0.08, segs=1)
    # a carved keystone emblem (original: a simple sunburst of wedges)
    cyl(nm('keystone'), 1.6, 1.2, loc=(0, -2.2, oh + 0.8), key='ev_stone_dark', verts=8)
    for i in range(8):
        a = 2 * PI * i / 8
        box(nm('ray'), (1.4, 0.5, 0.4), loc=(math.cos(a) * 2.2, -2.3, oh + 0.8 + math.sin(a) * 2.2), rot=(0, 0, math.degrees(a)), key='ev_stone_dark', bev=0.03, segs=1)
    U.marker('mk_door', (0, -1.0, 0.2))
    return finalize('landmark_trail_05', smooth_angle=28)


# ================================================================== F11_06..08 CLIFF-TRAIL PIECES (walkable 6 wide, tileable ends)
def trail_staircut():
    """F11_06: a stair-cut trail section along a cliff, 24 long, walkable 6 wide, tileable ends."""
    reset()
    seed = 1106
    rnd = random.Random(seed)
    L, w = 24.0, 6.0
    # cliff wall on +Y side
    wall = box(nm('wall'), (L, 6.0, 20.0), loc=(0, 6.0, 8.0), key='wd_rock_grey', bev=0.3, segs=1)
    top_paint(wall, 'wd_moss', 0.85, seed)
    # the cut steps climbing along the length (ends at matching heights for tiling: 0 and ~6)
    nst = 8
    for i in range(nst):
        x = -L / 2 + (i + 0.5) * L / nst
        z = i * 0.75
        box(nm('tread'), (L / nst + 0.3, w, 0.5), loc=(x, 0, z + 0.25), key='ev_stone', bev=0.04, segs=1)
        box(nm('riser'), (0.5, w, 1.0), loc=(x - L / nst / 2, 0, z), key='ev_stone_dark', bev=0.03, segs=1)
    # outer edge kerb + a few rocks
    box(nm('kerb'), (L, 0.5, 0.8), loc=(0, -w / 2, 3.2), key='ev_stone_dark', bev=0.05, segs=1)
    for i in range(5):
        rock(nm('rk'), rnd.uniform(0.8, 1.6), (rnd.uniform(-L / 2, L / 2), 2.5, rnd.uniform(0, 5)), rnd.choice(ROCK), seed=seed + i, scale=(1.2, 1, 0.7), subdiv=2, amp=0.3)
    U.marker('mk_conn', (-L / 2, 0, 0.3))
    U.marker('mk_conn', (L / 2, 0, nst * 0.75 * (nst - 1) / nst))
    return finalize('landmark_trail_06', smooth_angle=28)


def trail_switchback():
    """F11_07: a switchback trail piece (two ramps with a landing turn), walkable 6 wide."""
    reset()
    seed = 1107
    rnd = random.Random(seed)
    w = 6.0
    wall = box(nm('wall'), (26.0, 6.0, 24.0), loc=(0, 7.0, 10.0), key='wd_rock_dark', bev=0.3, segs=1)
    top_paint(wall, 'wd_moss', 0.85, seed)
    # switchback: lower ramp climbs L->R to a landing, upper ramp climbs R->L. Place each ramp at the
    # midpoint of its two endpoints with the matching slope so the runs actually meet the landing.
    def ramp(x0, z0, x1, z1, yc, tag):
        dx, dz = x1 - x0, z1 - z0
        length = math.hypot(dx, dz)
        ang = math.degrees(math.atan2(dz, dx))
        box(nm(tag), (length, w, 0.6), loc=((x0 + x1) / 2, yc, (z0 + z1) / 2 + 0.3), rot=(0, -ang, 0), key='ev_stone', bev=0.05, segs=1)
        box(nm(tag + 'k'), (length, 0.5, 1.0), loc=((x0 + x1) / 2, yc - w / 2, (z0 + z1) / 2 + 0.8), rot=(0, -ang, 0), key='ev_stone_dark', bev=0.05, segs=1)
    yL, yU = -w / 2 - 0.5, w / 2 + 0.5          # front run and back run, offset in Y so they never cross
    ramp(-10.0, 0.5, 8.0, 6.0, yL, 'lower')
    box(nm('landing'), (6.0, 2 * w + 2.0, 0.7), loc=(10.0, 0, 6.3), key='ev_stone', bev=0.06, segs=1)
    box(nm('landkerb'), (6.0, 0.5, 1.2), loc=(10.0, w + 0.9, 6.9), key='ev_stone_dark', bev=0.05, segs=1)
    ramp(8.0, 6.6, -10.0, 12.0, yU, 'upper')
    for i in range(4):
        rock(nm('rk'), rnd.uniform(0.8, 1.5), (rnd.uniform(-10, 10), 3.0, rnd.uniform(0, 9)), rnd.choice(ROCK), seed=seed + i, scale=(1.2, 1, 0.7), subdiv=2, amp=0.3)
    U.marker('mk_conn', (-10.0, yL, 0.8))
    U.marker('mk_conn', (-10.0, yU, 12.3))
    return finalize('landmark_trail_07', smooth_angle=28)


def trail_rope_ledge():
    """F11_08: a rope-and-plank ledge path on pegs driven into the cliff, walkable 6 wide, tileable."""
    reset()
    seed = 1108
    rnd = random.Random(seed)
    L, w = 24.0, 6.0
    wall = box(nm('wall'), (L, 5.0, 22.0), loc=(0, 5.0, 9.0), key='wd_rock_grey', bev=0.3, segs=1)
    top_paint(wall, 'wd_moss', 0.8, seed)
    deckz = 8.0
    # support pegs driven into the cliff, angled down-out
    for i in range(9):
        x = -L / 2 + i * L / 8
        box(nm('peg'), (0.5, 4.0, 0.5), loc=(x, 1.0, deckz - 0.4), rot=(18, 0, 0), key='wk_timber_dk', bev=0.03, segs=1)
    # plank deck (individual planks for seams)
    npl = int(L / 1.1)
    for i in range(npl):
        x = -L / 2 + (i + 0.5) * L / npl
        box(nm('plank'), (L / npl * 0.9, w, 0.2), loc=(x, 0.0, deckz), key=rnd.choice(('wk_plank', 'wk_plank_dk')), bev=0.02, segs=1)
    # rope handrail on the outer edge, on short posts, with a catenary sag between posts
    posts = [-L / 2 + i * L / 8 for i in range(9)]
    for x in posts:
        cyl(nm('rpost'), 0.14, 3.2, loc=(x, -w / 2 + 0.3, deckz), key='wk_timber', verts=5)
    for i in range(len(posts) - 1):
        x0, x1 = posts[i], posts[i + 1]
        xm = (x0 + x1) / 2
        tube(nm('rope'), [(x0, -w / 2 + 0.3, deckz + 3.0), (xm, -w / 2 + 0.3, deckz + 2.5), (x1, -w / 2 + 0.3, deckz + 3.0)], 0.1, 'wk_rope', res=4, ures=3)
        tube(nm('rope2'), [(x0, -w / 2 + 0.3, deckz + 1.6), (xm, -w / 2 + 0.3, deckz + 1.2), (x1, -w / 2 + 0.3, deckz + 1.6)], 0.08, 'wk_rope', res=4, ures=3)
    U.marker('mk_conn', (-L / 2, 0, deckz + 0.2))
    U.marker('mk_conn', (L / 2, 0, deckz + 0.2))
    return finalize('landmark_trail_08', smooth_angle=28)


# ================================================================== F11_09 SUMMIT TOWER
def summit_tower():
    """F11_09: weathered stone tower ~16x16x50 on a rocky crag, beacon brazier, flag, stair cut into rock."""
    reset()
    seed = 1109
    rnd = random.Random(seed)
    # rocky crag base
    crag = _landform(40, 20, lambda t: (max(16.0 * (1 - 0.4 * t), 9.0), 16.0 * t), seed,
                     [(1.0, 1.0), (2.2, 0.5), (4.4, 0.26), (8.8, 0.14)], strata_h=3.5, overhang=0.5, warp=1.0, name_key='crag')
    _paint(crag, seed, [('wd_rock_dark', lambda c, nz, ny, t, nv: nv < -0.2 or t < 0.15),
                        ('wd_moss', lambda c, nz, ny, t, nv: nz > 0.7 and t > 0.7),
                        ('wd_rock_light', lambda c, nz, ny, t, nv: nv > 0.35),
                        ('wd_rock_grey', lambda c, nz, ny, t, nv: True)], 16.0)
    _scree_skirt(seed, 15.0, ROCK, n=12)
    base_z = 14.0
    S, TH = 16.0, 50.0                                   # tower footprint / height
    # hollow-ish weathered stone tower: four walls (thick), battlements, narrow windows
    wall_t = 2.0
    for (lx, ly, sx, sy) in ((0, S / 2 - wall_t / 2, S, wall_t), (0, -(S / 2 - wall_t / 2), S, wall_t),
                             (-(S / 2 - wall_t / 2), 0, wall_t, S - 2 * wall_t), (S / 2 - wall_t / 2, 0, wall_t, S - 2 * wall_t)):
        w = box(nm('wall'), (sx, sy, TH), loc=(lx, ly, base_z + TH / 2), key='ev_stone', bev=0.15, segs=1)
        top_paint(w, 'wd_moss', 0.93, seed, noise_amt=0.1)
    # course lines (horizontal bands) for stonework read
    for i in range(1, int(TH / 6)):
        box(nm('course'), (S + 0.3, S + 0.3, 0.2), loc=(0, 0, base_z + i * 6), key='ev_stone_dark', bev=0, segs=1)
    # narrow lancet windows up one face
    for i in range(4):
        box(nm('win'), (1.4, 0.6, 3.2), loc=(0, -(S / 2) - 0.1, base_z + 10 + i * 10), key='wk_cave_dark', bev=0.05, segs=1)
    # battlements at the top
    topz = base_z + TH
    for x in range(-7, 8, 3):
        for (yy) in (-(S / 2 - 0.5), S / 2 - 0.5):
            box(nm('merlon'), (1.6, 1.4, 2.2), loc=(x, yy, topz + 1.1), key='ev_stone', bev=0.08, segs=1)
    for y in range(-6, 7, 3):
        for (xx) in (-(S / 2 - 0.5), S / 2 - 0.5):
            box(nm('merlon'), (1.4, 1.6, 2.2), loc=(xx, y, topz + 1.1), key='ev_stone', bev=0.08, segs=1)
    # roof deck
    box(nm('roofdeck'), (S - 1.0, S - 1.0, 0.5), loc=(0, 0, topz + 0.25), key='ev_stone_dark', bev=0.05, segs=1)
    # beacon brazier (lit) in the centre
    cyl(nm('brazbowl'), 2.0, 1.6, loc=(0, 0, topz + 0.5), key='wk_cart_metal', verts=10, r2=1.4)
    for i in range(3):
        cyl(nm('brazleg'), 0.25, 2.0, loc=(math.cos(i * 2.1) * 1.4, math.sin(i * 2.1) * 1.4, topz + 0.5), key='wk_cart_metal', verts=5)
    ball(nm('fire'), 1.3, (0, 0, topz + 2.2), 'wk_brazier_fire', segs=8, rings=6, scale=(1, 1, 1.3))
    ball(nm('ember'), 0.9, (0, 0, topz + 2.6), 'wk_ember', segs=7, rings=5, scale=(1, 1, 1.4))
    # flag on a pole at one corner
    cyl(nm('pole'), 0.25, 10.0, loc=(S / 2 - 1.5, -(S / 2 - 1.5), topz + 1.5), key='wk_timber_dk', verts=6)
    box(nm('flag'), (0.1, 4.0, 2.6), loc=(S / 2 - 1.5 - 2.0, -(S / 2 - 1.5), topz + 9.0), key='wk_flag', bev=0.02, segs=1)
    # stair spiral cut into the crag (a few steps wrapping the base up to the door)
    for i in range(10):
        a = -PI / 2 + i * 0.4
        r = 13.0
        box(nm('cutstep'), (3.0, 2.2, 0.5), loc=(math.cos(a) * r, math.sin(a) * r, 2.0 + i * 1.2), rot=(0, 0, math.degrees(a)), key='ev_stone', bev=0.04, segs=1)
    # tower doorway at base_z on the -Y face
    box(nm('doorhole'), (4.0, 1.0, 7.0), loc=(0, -(S / 2) - 0.2, base_z + 3.5), key='wk_cave_dark', bev=0, segs=1)
    U.marker('mk_door', (0, -(S / 2) - 0.2, base_z + 0.3))
    return finalize('landmark_trail_09', smooth_angle=30)


# ================================================================== batches
BATCH_LOOKOUTS = [
    ('F11_01_landmark_trail_01', lookout_stone, (0.5, -1.1, 0.4)),
    ('F11_02_landmark_trail_02', lookout_timber, (0.5, -1.1, 0.4)),
]
BATCH_CAVES = [
    ('F11_03_landmark_trail_03', cave_natural, (0.1, -1.0, 0.2)),
    ('F11_04_landmark_trail_04', cave_mine, (0.3, -1.0, 0.2)),
    ('F11_05_landmark_trail_05', cave_carved, (0.1, -1.0, 0.2)),
]
BATCH_TRAILS = [
    ('F11_06_landmark_trail_06', trail_staircut, (0.5, -1.0, 0.35)),
    ('F11_07_landmark_trail_07', trail_switchback, (0.5, -1.0, 0.35)),
    ('F11_08_landmark_trail_08', trail_rope_ledge, (0.5, -1.0, 0.35)),
]
BATCH_SUMMIT = [
    ('F11_09_landmark_trail_09', summit_tower, (0.5, -1.1, 0.4)),
]

BATCHES = {
    'lookouts': ('v4_landmarks', BATCH_LOOKOUTS),
    'caves':    ('v4_landmarks', BATCH_CAVES),
    'trails':   ('v4_landmarks', BATCH_TRAILS),
    'summit':   ('v4_landmarks', BATCH_SUMMIT),
}
