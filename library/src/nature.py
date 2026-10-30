# nature.py - trees, plants, rocks, ground clutter (A24-A70).
import math, random
import bmesh
from mathutils import Vector, noise, Matrix
from kitlib import *
from kitlib import _obj_from_bm


# ----------------------------------------------------------------- organic helpers
def blob(name, r, loc, key, subdiv=2, amp=0.22, freq=1.4, scale=(1, 1, 1), seed=0, flat_bottom=None, detail=0.0):
    """Lumpy organic mass (foliage clump / rock): noise-displaced icosphere."""
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=r)
    off = Vector((seed * 13.1, seed * 7.7, seed * 3.3))
    for v in bm.verts:
        n = noise.noise(v.co * (freq / r) + off)
        if detail:
            n += detail * noise.noise(v.co * (freq * 3.1 / r) + off * 1.7)
        v.co *= 1.0 + amp * n
        v.co.x *= scale[0]; v.co.y *= scale[1]; v.co.z *= scale[2]
        if flat_bottom is not None and v.co.z < flat_bottom:
            v.co.z = flat_bottom + (v.co.z - flat_bottom) * 0.15
    o = _obj_from_bm(name, bm, key)
    o.location = loc
    return o


def rock(name, r, loc, key='stone', seed=0, scale=(1, 1, 0.7), subdiv=2, amp=0.3, rot_z=0.0):
    """Faceted rock: noise blob, flattened, sunk slightly into the ground."""
    o = blob(name, r, loc, key, subdiv=subdiv, amp=amp, freq=1.1, scale=scale, seed=seed, flat_bottom=-r * scale[2] * 0.35,
             detail=0.45)
    o.rotation_euler.z = rot_z
    return o


def branch_tree(prefix, base, direction, length, radius, depth, rnd, key='bark', spread=32, kids=3, tips=None,
                droop=0.0, up_bias=0.35):
    """Recursive tapered branches. Collects tip positions (for foliage) in tips."""
    d = Vector(direction).normalized()
    mid = Vector(base) + d * length * 0.5 + Vector((rnd.uniform(-0.12, 0.12), rnd.uniform(-0.12, 0.12), 0)) * length
    end = Vector(base) + d * length + Vector((0, 0, -droop * length))
    tube(f'{prefix}', [tuple(base), tuple(mid), tuple(end)], radius, key, res=6 if depth > 1 else 4,
         taper=[1.0, 0.82, 0.62], ures=3)
    if tips is not None and depth <= 1:
        tips.append((end, radius))
    if depth <= 0:
        return
    for k in range(kids):
        az = rnd.uniform(0, 2 * math.pi)
        tilt = math.radians(rnd.uniform(spread * 0.6, spread * 1.3))
        # build child direction: rotate parent dir by tilt around a random perpendicular axis
        perp = d.cross(Vector((math.cos(az), math.sin(az), 0.3))).normalized()
        nd = (Matrix.Rotation(tilt, 3, perp) @ d)
        nd = (nd + Vector((0, 0, up_bias))).normalized()
        t = rnd.uniform(0.55, 0.95)
        start = Vector(base) + (end - Vector(base)) * t
        branch_tree(f'{prefix}_{k}', start, nd, length * rnd.uniform(0.55, 0.72), radius * 0.6, depth - 1, rnd, key,
                    spread, kids, tips, droop, up_bias)
    if tips is not None and depth > 1:
        tips.append((end, radius))


def trunk_flare(prefix, r, h, key='bark', roots=5, rnd=None, lean=(0, 0)):
    """Trunk base with root flare buttresses."""
    lathe(prefix, [(0.0, -0.2), (r * 1.6, -0.2), (r * 1.35, 0.25), (r * 1.08, 0.8), (r, h * 0.3), (r * 0.9, h), (0.0, h)],
          key=key, segs=12)
    rnd = rnd or random.Random(1)
    for i in range(roots):
        a = 2 * math.pi * i / roots + rnd.uniform(-0.3, 0.3)
        c, s = math.cos(a), math.sin(a)
        tube(f'{prefix}_root{i}', [(c * r * 0.55, s * r * 0.55, 1.1), (c * r * 1.15, s * r * 1.15, 0.45),
                                   (c * r * 1.7, s * r * 1.7, 0.15), (c * r * 2.0, s * r * 2.0, 0.02)], r * 0.3, key, res=4,
             taper=[1, 0.8, 0.6, 0.4], ures=3)


def foliage_at(prefix, tips, rnd, keys, rmin, rmax, extra=0, centre=None, cr=None, flat=0.82):
    for i, (p, rad) in enumerate(tips):
        r = rnd.uniform(rmin, rmax)
        blob(f'{prefix}{i}', r, (p.x, p.y, p.z + r * 0.15), rnd.choice(keys), subdiv=2, amp=0.25,
             scale=(1, 1, flat), seed=rnd.randint(0, 999))
    for i in range(extra):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, cr * 0.6)
        r = rnd.uniform(rmin, rmax) * 1.1
        blob(f'{prefix}x{i}', r, (centre[0] + math.cos(a) * d, centre[1] + math.sin(a) * d, centre[2] + rnd.uniform(-cr * 0.25, cr * 0.35)),
             rnd.choice(keys), subdiv=2, amp=0.25, scale=(1, 1, flat), seed=rnd.randint(0, 999))


# ----------------------------------------------------------------- trees
def _oak(seed, height, name, nb=4, crown=1.0, flat=0.82, keys=('leaf', 'leaf_dark', 'leaf_light', 'leaf')):
    reset()
    rnd = random.Random(seed)
    r = height * 0.075
    trunk_flare('trunk', r, height * 0.42, rnd=rnd)
    tips = []
    top = Vector((rnd.uniform(-0.4, 0.4), rnd.uniform(-0.4, 0.4), height * 0.4))
    for k in range(nb):
        az = 2 * math.pi * k / nb + rnd.uniform(-0.4, 0.4)
        d = Vector((math.cos(az), math.sin(az), rnd.uniform(0.9, 1.4) / crown))
        branch_tree(f'b{k}', top, d, height * rnd.uniform(0.3, 0.38) * crown, r * 0.62, 2, rnd, spread=34, kids=2, tips=tips)
    tube('leader', [(0, 0, height * 0.38), tuple(top + Vector((0, 0, height * 0.25)))], r * 0.55, 'bark', res=6, taper=[1, 0.5])
    tips.append((top + Vector((0, 0, height * 0.3)), 0.2))
    foliage_at('leaf', tips, rnd, list(keys), height * 0.13, height * 0.19,
               extra=5, centre=(0, 0, height * 0.72), cr=height * 0.35 * crown, flat=flat)
    return finalize(name, smooth_angle=50)


def oak_1():
    """A24 - broad old oak, 34 studs, wide spreading crown."""
    return _oak(24, 34, 'oak_1', nb=5, crown=1.15, flat=0.75)

def oak_2():
    """A25 - medium oak, 28 studs, rounded crown."""
    return _oak(25, 28, 'oak_2', nb=4, crown=1.0, flat=0.9, keys=('leaf', 'leaf_light', 'leaf'))

def oak_3():
    """A26 - young upright oak, 22 studs, narrow tall crown."""
    return _oak(26, 22, 'oak_3', nb=3, crown=0.75, flat=1.15, keys=('leaf_light', 'leaf', 'birch_leaf'))


def _birch(seed, height, name):
    reset()
    rnd = random.Random(seed)
    r = height * 0.035
    lean = Vector((rnd.uniform(-0.08, 0.08), rnd.uniform(-0.08, 0.08), 1)).normalized()
    pts = [Vector((0, 0, 0)), lean * height * 0.35 + Vector((0.3, 0, 0)), lean * height * 0.7, lean * height * 0.95]
    tube('trunk', [tuple(p) for p in pts], r, 'birch', res=6, taper=[1.15, 0.9, 0.7, 0.4], ures=4)
    # bark marks: dark horizontal lenticels
    for i in range(26):
        z = rnd.uniform(0.6, height * 0.8)
        a = rnd.uniform(0, 6.28)
        p = lean * z
        box(f'mark{i}', (r * 1.3, 0.12, rnd.uniform(0.15, 0.4)),
            loc=(p.x + math.cos(a) * r * 0.8, p.y + math.sin(a) * r * 0.8, p.z), key='iron_dark', rot=(0, 0, math.degrees(a) + 90))
    tips = []
    for k in range(8):
        z = height * rnd.uniform(0.42, 0.85)
        az = 2 * math.pi * k / 8 + rnd.uniform(-0.3, 0.3)
        d = Vector((math.cos(az), math.sin(az), 0.9))
        branch_tree(f'b{k}', lean * z, d, height * 0.24, r * 0.45, 1, rnd, key='birch', spread=25, kids=2, tips=tips)
    tips.append((lean * height * 0.97, 0.1))
    foliage_at('leaf', tips, rnd, ['leaf_light', 'leaf', 'leaf_light', 'birch_leaf'], height * 0.085, height * 0.12, extra=7,
               centre=tuple(lean * height * 0.7), cr=height * 0.32, flat=1.0)
    return finalize(name, smooth_angle=50)


def birch_1():
    """A27 - slender birch, 30 studs."""
    return _birch(27, 30, 'birch_1')

def birch_2():
    """A28 - birch, 24 studs."""
    return _birch(28, 24, 'birch_2')


def _pine(seed, height, name, snow=False, tiers=6, width=0.27, keys=('pine', 'pine_dark'), droop=0.12):
    reset()
    rnd = random.Random(seed)
    r = height * 0.04
    trunk_flare('trunk', r, height * 0.9, rnd=rnd, roots=4)
    for i in range(tiers):
        t = i / (tiers - 1)
        z = height * (0.14 + 0.76 * t)
        R = height * (width * (1 - t) + 0.05) * rnd.uniform(0.92, 1.08)
        H = height * (1.3 / tiers) * (1 - t * 0.35)
        n = 14
        # star-profiled drooping skirt: points alternate radius, outer rim drops below
        bm = bmesh.new()
        top = bm.verts.new((rnd.uniform(-0.2, 0.2), rnd.uniform(-0.2, 0.2), z + H))
        rim, inner = [], []
        for j in range(n * 2):
            a = math.pi * j / n + rnd.uniform(-0.05, 0.05) + i * 0.4
            rr = R * (1.0 if j % 2 == 0 else 0.72) * rnd.uniform(0.9, 1.08)
            dz = -H * (droop if j % 2 == 0 else 0.0) + rnd.uniform(-0.15, 0.15)
            rim.append(bm.verts.new((math.cos(a) * rr, math.sin(a) * rr, z + dz)))
            inner.append(bm.verts.new((math.cos(a) * rr * 0.5, math.sin(a) * rr * 0.5, z + H * 0.12)))
        for j in range(n * 2):
            k = (j + 1) % (n * 2)
            bm.faces.new((rim[j], rim[k], top))
            bm.faces.new((rim[k], rim[j], inner[j], inner[k]))
        c = bm.verts.new((0, 0, z + H * 0.1))
        for j in range(n * 2):
            bm.faces.new((inner[k := (j + 1) % (n * 2)], inner[j], c))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        _obj_from_bm(f'tier{i}', bm, rnd.choice(keys))
        if snow:
            bm = bmesh.new()
            top2 = bm.verts.new((0, 0, z + H + 0.05))
            ring = []
            for j in range(n):
                a = 2 * math.pi * j / n + i * 0.4
                rr = R * 0.62 * rnd.uniform(0.85, 1.05)
                ring.append(bm.verts.new((math.cos(a) * rr, math.sin(a) * rr, z + H * 0.42 + rnd.uniform(-0.1, 0.1))))
            for j in range(n):
                bm.faces.new((ring[j], ring[(j + 1) % n], top2))
            bm.faces.new(list(reversed(ring)))
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            _obj_from_bm(f'snow{i}', bm, 'snow')
    return finalize(name, smooth_angle=20)


def pine_1():
    """A29 - tall narrow spruce, 42 studs, 9 tiers."""
    return _pine(29, 42, 'pine_1', tiers=9, width=0.2, keys=('pine_dark', 'pine_dark', 'pine'), droop=0.18)

def pine_2():
    """A30 - full round fir, 30 studs, 6 tiers."""
    return _pine(30, 30, 'pine_2', tiers=6, width=0.32, keys=('pine', 'pine_light'), droop=0.1)

def pine_3():
    """A31 - small bushy pine, 16 studs, 4 tiers."""
    return _pine(31, 16, 'pine_3', tiers=4, width=0.38, keys=('pine_light', 'pine'), droop=0.06)


def maple_autumn():
    """A32 - autumn maple: rounded canopy in orange/red/gold."""
    reset()
    rnd = random.Random(32)
    h = 28
    r = h * 0.07
    trunk_flare('trunk', r, h * 0.4, rnd=rnd)
    tips = []
    top = Vector((0, 0, h * 0.38))
    for k in range(5):
        az = 2 * math.pi * k / 5 + rnd.uniform(-0.3, 0.3)
        branch_tree(f'b{k}', top, (math.cos(az), math.sin(az), 1.5), h * 0.3, r * 0.55, 2, rnd, spread=30, kids=2, tips=tips)
    foliage_at('leaf', tips, rnd, ['autumn_a', 'autumn_b', 'autumn_c', 'autumn_a'], h * 0.11, h * 0.16,
               extra=6, centre=(0, 0, h * 0.72), cr=h * 0.32, flat=0.9)
    # fallen leaves on the ground
    for i in range(40):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(1, h * 0.4)
        box(f'fl{i}', (0.5, 0.35, 0.04), loc=(math.cos(a) * d, math.sin(a) * d, 0.03),
            key=rnd.choice(['autumn_a', 'autumn_b', 'autumn_c']), rot=(0, 0, rnd.uniform(0, 360)))
    return finalize('maple_autumn', smooth_angle=50)


def willow():
    """A33 - weeping willow with hanging strands."""
    reset()
    rnd = random.Random(33)
    h = 30
    r = h * 0.075
    trunk_flare('trunk', r, h * 0.35, rnd=rnd)
    tips = []
    top = Vector((0, 0, h * 0.33))
    for k in range(5):
        az = 2 * math.pi * k / 5 + rnd.uniform(-0.3, 0.3)
        branch_tree(f'b{k}', top, (math.cos(az), math.sin(az), 1.0), h * 0.32, r * 0.55, 1, rnd, spread=30, kids=2,
                    tips=tips, up_bias=0.5)
    # crown dome
    foliage_at('crown', tips, rnd, ['willow', 'leaf_light'], h * 0.1, h * 0.14, extra=4, centre=(0, 0, h * 0.62), cr=h * 0.3)
    # hanging strands around the crown edge
    for i in range(90):
        a = 2 * math.pi * i / 90 + rnd.uniform(-0.04, 0.04)
        R = h * rnd.uniform(0.26, 0.42)
        z0 = h * rnd.uniform(0.58, 0.74)
        z1 = rnd.uniform(1.5, h * 0.32)
        sway = rnd.uniform(-0.6, 0.6)
        pts = [(math.cos(a) * R * 0.9, math.sin(a) * R * 0.9, z0),
               (math.cos(a) * R * 1.04 - math.sin(a) * sway * 0.5, math.sin(a) * R * 1.04 + math.cos(a) * sway * 0.5, (z0 + z1) * 0.62),
               (math.cos(a) * R * 1.08 - math.sin(a) * sway, math.sin(a) * R * 1.08 + math.cos(a) * sway, z1)]
        tube(f'str{i}', pts, rnd.uniform(0.18, 0.32), rnd.choice(['willow', 'leaf_light', 'willow', 'birch_leaf']), res=4,
             taper=[1, 0.75, 0.2], ures=3)
    return finalize('willow', smooth_angle=50)


def fruit_tree():
    """A34 - apple/fruit tree: short trunk, round canopy, red fruit."""
    reset()
    rnd = random.Random(34)
    h = 20
    r = h * 0.07
    trunk_flare('trunk', r, h * 0.35, rnd=rnd, roots=4)
    tips = []
    top = Vector((0, 0, h * 0.33))
    for k in range(4):
        az = 2 * math.pi * k / 4 + 0.3
        branch_tree(f'b{k}', top, (math.cos(az), math.sin(az), 1.0), h * 0.3, r * 0.6, 2, rnd, spread=30, kids=2, tips=tips)
    foliage_at('leaf', tips, rnd, ['leaf', 'leaf_light'], h * 0.12, h * 0.17, extra=4, centre=(0, 0, h * 0.65), cr=h * 0.3)
    import bpy as _bpy
    leaves = [o for o in _bpy.context.scene.objects if o.name.startswith('leaf')]
    for i in range(30):
        lo = rnd.choice(leaves)
        bb = max(lo.dimensions) * 0.5
        a = rnd.uniform(0, 6.28); el = rnd.uniform(-0.6, 0.5)
        p = lo.location + Vector((math.cos(a) * math.cos(el), math.sin(a) * math.cos(el), math.sin(el))) * bb * 0.95
        ball(f'fruit{i}', 0.45, loc=tuple(p), key='fruit', segs=10, rings=7)
    for i in range(5):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(1.5, 6)
        ball(f'gfruit{i}', 0.42, loc=(math.cos(a) * d, math.sin(a) * d, 0.35), key='fruit', segs=10, rings=7)
    return finalize('fruit_tree', smooth_angle=50)


def _dead(seed, h, name, nb=4, depth=3, lean=0.0):
    reset()
    rnd = random.Random(seed)
    r = h * 0.07
    trunk_flare('trunk', r, h * 0.45, rnd=rnd)
    top = Vector((0.4 + lean * h, -0.3, h * 0.43))
    if lean:
        tube('leanpart', [(0, 0, h * 0.3), (lean * h * 0.5, -0.15, h * 0.37), tuple(top)], r * 0.85, 'bark_dead', res=6, taper=[1, 0.95, 0.85])
    for k in range(nb):
        az = 2 * math.pi * k / nb + rnd.uniform(-0.5, 0.5)
        branch_tree(f'b{k}', top, (math.cos(az), math.sin(az), rnd.uniform(0.6, 1.3)), h * rnd.uniform(0.28, 0.38), r * 0.55,
                    depth, rnd, key='bark_dead', spread=38, kids=2, up_bias=0.15)
    tube('snag', [tuple(top), (0.3, -0.25, h * 0.55)], r * 0.55, 'bark_dead', res=6, taper=[1, 0.8])
    for k in range(4):
        a = rnd.uniform(0, 6.28)
        cyl(f'jag{k}', r * 0.18, rnd.uniform(0.6, 1.4), loc=(0.3 + math.cos(a) * r * 0.3, -0.25 + math.sin(a) * r * 0.3, h * 0.55 - 0.1),
            key='bark_dead', verts=4, r2=0.02)
    # broken stub
    cyl('stub', r * 0.4, 1.5, loc=(r * 0.7, 0, h * 0.25), key='bark_dead', verts=8, rot=(0, 70, 0))
    return finalize(name, smooth_angle=50)


def dead_tree_1():
    """A35 - gnarled dead tree, 26 studs (rusty town, graveyards)."""
    return _dead(35, 26, 'dead_tree_1')

def dead_tree_2():
    """A36 - leaning dead tree with three heavy limbs, 18 studs."""
    return _dead(36, 18, 'dead_tree_2', nb=3, depth=2, lean=0.12)


def sapling():
    """A37 - young sapling with stake and tie."""
    reset()
    rnd = random.Random(37)
    tube('trunk', [(0, 0, 0), (0.1, 0, 3), (0, 0.1, 6.5)], 0.18, 'bark', res=4, taper=[1, 0.7, 0.4])
    tips = []
    for k in range(4):
        az = 2 * math.pi * k / 4 + 0.4
        branch_tree(f'b{k}', (0, 0.08, 5.2), (math.cos(az), math.sin(az), 1.2), 2.2, 0.09, 1, rnd, spread=25, kids=2, tips=tips)
    foliage_at('leaf', tips, rnd, ['leaf_light', 'leaf'], 0.9, 1.3, extra=2, centre=(0, 0, 6.8), cr=1.8)
    box('stake', (0.22, 0.22, 5.5), loc=(0.55, 0, 2.5), key='wood_light', rot=(0, -4, 0), bev=0.03)
    torus('tie', 0.45, 0.05, loc=(0.28, 0, 3.6), key='rope', segs=12, rsegs=4)
    lathe('mound', [(0.0, -0.1), (1.6, -0.1), (1.0, 0.15), (0.0, 0.25)], key='dirt', segs=14)
    return finalize('sapling', smooth_angle=50)


# ----------------------------------------------------------------- small plants
def _bush(seed, size, name, keys=('leaf', 'leaf_dark', 'leaf_light'), berries=None):
    reset()
    rnd = random.Random(seed)
    # inner core + many small leafy clumps on a dome surface = soft, full silhouette
    blob('core', size * 0.5, (0, 0, size * 0.42), keys[0], subdiv=3, amp=0.18, scale=(1.15, 1.15, 0.85), seed=seed,
         flat_bottom=-size * 0.3)
    n = 22
    for i in range(n):
        # golden-angle distribution on the upper hemisphere
        t = (i + 0.5) / n
        el = math.asin(t * 0.95)
        az = i * 2.39996
        R = size * 0.52
        p = (math.cos(az) * math.cos(el) * R * 1.15, math.sin(az) * math.cos(el) * R * 1.15, size * 0.38 + math.sin(el) * R * 0.85)
        r = size * rnd.uniform(0.18, 0.26)
        blob(f'c{i}', r, p, rnd.choice(keys), subdiv=2, amp=0.22, scale=(1, 1, 0.85), seed=rnd.randint(0, 999))
    if berries:
        for i in range(30 if berries == 'fl_white' else 18):
            a = rnd.uniform(0, 6.28); el = rnd.uniform(0.1, 1.0)
            ball(f'be{i}', size * (0.07 if berries == 'fl_white' else 0.045), loc=(math.cos(a) * size * 0.72 * math.cos(el), math.sin(a) * size * 0.72 * math.cos(el),
                                              size * 0.38 + size * 0.55 * math.sin(el)), key=berries, segs=6, rings=4)
    return finalize(name, smooth_angle=60)


def bush_1():
    """A38 - round leafy bush, 5 studs."""
    return _bush(38, 5.0, 'bush_1')

def bush_2():
    """A39 - larger dark bush with red berries, 7 studs."""
    return _bush(39, 7.0, 'bush_2', keys=('leaf_dark', 'leaf', 'leaf_dark'), berries='fl_red')

def bush_3():
    """A40 - low flowering bush (white blossom), 4 studs."""
    return _bush(40, 4.0, 'bush_3', keys=('leaf_light', 'leaf'), berries='fl_white')


def _hedge_block(name, size, loc, rnd):
    """Clipped hedge: rounded-edge box (softened corners), leafy noise, plus small leaf clumps on top/sides."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=9, use_grid_fill=True)
    sx, sy, sz = size
    off = Vector((rnd.uniform(0, 99), rnd.uniform(0, 99), 0))
    rad = min(sx, sy, sz) * 0.28
    for v in bm.verts:
        p = Vector((v.co.x * sx, v.co.y * sy, v.co.z * sz))
        # rounded box: clamp to inner box then push out by radius
        inner = Vector((max(-sx / 2 + rad, min(sx / 2 - rad, p.x)), max(-sy / 2 + rad, min(sy / 2 - rad, p.y)),
                        max(-sz / 2 + rad, min(sz / 2 - rad, p.z))))
        d = p - inner
        if d.length > 1e-6:
            p = inner + d.normalized() * rad
        n = noise.noise(p * 0.8 + off) * 0.35 + noise.noise(p * 2.2 + off) * 0.12
        nrm = (p - inner).normalized() if (p - inner).length > 1e-6 else Vector((0, 0, 1))
        v.co = p + nrm * n
    o = _obj_from_bm(name, bm, 'leaf_dark')
    o.location = loc
    # leafy bumps
    for i in range(int(sx * sy / 3)):
        x = rnd.uniform(-sx / 2 + 0.5, sx / 2 - 0.5); y = rnd.uniform(-sy / 2 + 0.3, sy / 2 - 0.3)
        blob(f'{name}_b{i}', rnd.uniform(0.55, 0.85), (loc[0] + x, loc[1] + y, loc[2] + sz / 2 - 0.1), rnd.choice(['leaf_dark', 'leaf']),
             subdiv=1, amp=0.25, scale=(1, 1, 0.6), seed=i)
    for i in range(int(sx * 1.2)):
        x = rnd.uniform(-sx / 2 + 0.5, sx / 2 - 0.5); side = rnd.choice((-1, 1)); z = rnd.uniform(-sz / 2 + 0.6, sz / 2 - 0.6)
        blob(f'{name}_s{i}', rnd.uniform(0.45, 0.7), (loc[0] + x, loc[1] + side * (sy / 2 - 0.05), loc[2] + z), rnd.choice(['leaf_dark', 'leaf']),
             subdiv=1, amp=0.25, scale=(1, 0.55, 1), seed=i + 50)
    return o


def hedge_straight():
    """A41 - clipped hedge section, 12 long x 3 wide x 4.5 tall."""
    reset()
    rnd = random.Random(41)
    _hedge_block('hedge', (12.0, 3.0, 4.2), (0, 0, 2.1), rnd)
    return finalize('hedge_straight', smooth_angle=60)


def hedge_corner():
    """A42 - L-shaped hedge corner, 7.5 x 7.5."""
    reset()
    rnd = random.Random(42)
    _hedge_block('h1', (7.5, 3.0, 4.2), (0, 0, 2.1), rnd)
    _hedge_block('h2', (3.0, 4.5, 4.2), (2.25, 3.75, 2.1), rnd)
    return finalize('hedge_corner', smooth_angle=60)


def flower(prefix, x, y, z, h, rnd, petal_key, centre_key='fl_yellow', petals=6, pr=0.22):
    tube(f'{prefix}_st', [(x, y, z), (x + rnd.uniform(-0.15, 0.15), y + rnd.uniform(-0.15, 0.15), z + h * 0.6), (x, y, z + h)],
         0.035, 'leaf_dark', res=4, ures=2)
    # leaf
    lf = ball(f'{prefix}_lf', 0.18, loc=(x + 0.12, y, z + h * 0.35), key='leaf', segs=6, rings=4, scale=(1.6, 0.6, 0.25))
    lf.rotation_euler = (0, math.radians(-30), rnd.uniform(0, 6.28))
    for p in range(petals):
        a = 2 * math.pi * p / petals
        o = ball(f'{prefix}_p{p}', pr, loc=(x + math.cos(a) * pr, y + math.sin(a) * pr, z + h), key=petal_key, segs=6, rings=4,
                 scale=(1.0, 0.6, 0.25))
        o.rotation_euler = (0, math.radians(-15), a)
    ball(f'{prefix}_c', pr * 0.55, loc=(x, y, z + h + 0.03), key=centre_key, segs=8, rings=5, scale=(1, 1, 0.6))


def _flower_patch(seed, name, petal_key, centre='fl_yellow', count=14, h=(1.0, 1.6), petals=6, pr=0.22):
    reset()
    rnd = random.Random(seed)
    blob('soil', 2.0, (0, 0, -0.05), 'leaf_dark', subdiv=2, amp=0.25, scale=(1.2, 1.0, 0.12), seed=seed)
    for i in range(count):
        a = rnd.uniform(0, 6.28); d = math.sqrt(rnd.random()) * 1.9
        flower(f'f{i}', math.cos(a) * d * 1.2, math.sin(a) * d, 0.05, rnd.uniform(*h), rnd, petal_key, centre, petals, pr)
    for i in range(10):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0.3, 2.2)
        from roads import tuft
        tuft(f'g{i}', math.cos(a) * d * 1.2, math.sin(a) * d, 0.0, rnd, h=0.7)
    return finalize(name, smooth_angle=50)


def flowers_red():
    """A43 - red poppy patch."""
    return _flower_patch(43, 'flowers_red', 'fl_red', 'iron_dark', petals=5, pr=0.26)

def flowers_yellow():
    """A44 - yellow buttercup/daisy patch."""
    return _flower_patch(44, 'flowers_yellow', 'fl_yellow', 'fl_orange', petals=7)

def flowers_purple():
    """A45 - lavender-type spikes."""
    reset()
    rnd = random.Random(45)
    blob('soil', 2.0, (0, 0, -0.05), 'leaf_dark', subdiv=2, amp=0.25, scale=(1.2, 1.0, 0.12), seed=45)
    for i in range(22):
        a = rnd.uniform(0, 6.28); d = math.sqrt(rnd.random()) * 1.9
        x, y = math.cos(a) * d * 1.2, math.sin(a) * d
        h = rnd.uniform(1.2, 1.9)
        lean = (rnd.uniform(-0.25, 0.25), rnd.uniform(-0.25, 0.25))
        tube(f's{i}', [(x, y, 0), (x + lean[0], y + lean[1], h)], 0.035, 'leaf', res=4)
        for k in range(6):
            t = 0.6 + 0.4 * k / 5
            ball(f'b{i}_{k}', 0.11 * (1.1 - 0.4 * k / 5), loc=(x + lean[0] * t, y + lean[1] * t, h * t), key='fl_purple', segs=6, rings=4,
                 scale=(1, 1, 1.4))
    return finalize('flowers_purple', smooth_angle=50)

def flowers_white():
    """A46 - white daisy patch."""
    return _flower_patch(46, 'flowers_white', 'fl_white', 'fl_yellow', petals=8, pr=0.2)

def flowers_blue():
    """A47 - blue cornflower patch."""
    return _flower_patch(47, 'flowers_blue', 'fl_blue', 'fl_white', petals=6, pr=0.22)


def planter_box():
    """A48 - wooden planter box with soil, mixed flowers and trailing leaves."""
    reset()
    rnd = random.Random(48)
    L, Wd, H = 6.0, 2.4, 2.0
    for side in (-1, 1):
        for k in range(3):
            box(f'pl{side}{k}', (L, 0.25, 0.62), loc=(0, side * (Wd / 2 - 0.12), 0.35 + k * 0.64), key=rnd.choice(['wood', 'wood_light']), bev=0.04, segs=1)
            box(f'pe{side}{k}', (0.25, Wd - 0.5, 0.62), loc=(side * (L / 2 - 0.12), 0, 0.35 + k * 0.64), key=rnd.choice(['wood', 'wood_light']), bev=0.04, segs=1)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f'corner{sx}{sy}', (0.45, 0.45, H + 0.3), loc=(sx * (L / 2 - 0.1), sy * (Wd / 2 - 0.1), (H + 0.3) / 2), key='wood_dark', bev=0.05)
            box(f'band{sx}{sy}', (0.5, 0.5, 0.18), loc=(sx * (L / 2 - 0.1), sy * (Wd / 2 - 0.1), H - 0.2), key='iron')
    box('soil', (L - 0.5, Wd - 0.5, 0.3), loc=(0, 0, H - 0.25), key='dirt')
    keys = ['fl_red', 'fl_yellow', 'fl_white', 'fl_purple', 'fl_blue']
    for i in range(16):
        flower(f'f{i}', rnd.uniform(-L / 2 + 0.6, L / 2 - 0.6), rnd.uniform(-Wd / 2 + 0.5, Wd / 2 - 0.5), H - 0.1,
               rnd.uniform(0.7, 1.4), rnd, rnd.choice(keys), 'fl_yellow')
    for i in range(6):
        blob(f'lv{i}', 0.5, (rnd.uniform(-L / 2 + 0.6, L / 2 - 0.6), rnd.choice((-1, 1)) * (Wd / 2 - 0.1), H - 0.1), 'leaf',
             subdiv=1, amp=0.3, scale=(1.4, 0.7, 1.0), seed=i)
    return finalize('planter_box', smooth_angle=45)


def _grass_clump(seed, name, h, n, keys=('leaf', 'leaf_light', 'leaf_dark')):
    reset()
    rnd = random.Random(seed)
    for i in range(n):
        a = rnd.uniform(0, 6.28); d = math.sqrt(rnd.random()) * h * 0.25
        x, y = math.cos(a) * d, math.sin(a) * d
        hh = h * rnd.uniform(0.55, 1.0)
        lean = Vector((math.cos(a), math.sin(a), 0)) * hh * rnd.uniform(0.15, 0.45)
        tube(f'bl{i}', [(x, y, 0), (x + lean.x * 0.4, y + lean.y * 0.4, hh * 0.6), (x + lean.x, y + lean.y, hh)],
             rnd.uniform(0.07, 0.11), rnd.choice(keys), res=4, taper=[1, 0.7, 0.05], ures=2)
    return finalize(name, smooth_angle=60)


def tall_grass_1():
    """A49 - tall grass clump, 3 studs."""
    return _grass_clump(49, 'tall_grass_1', 3.0, 40)

def tall_grass_2():
    """A50 - dry/golden tall grass clump, 4 studs."""
    return _grass_clump(50, 'tall_grass_2', 4.0, 46, keys=('grass_dry', 'thatch', 'leaf_light'))


def fern():
    """A51 - fern: arching fronds built as tapered ribbons with serrated leaflet edges."""
    reset()
    rnd = random.Random(51)
    for f in range(13):
        a = 2 * math.pi * f / 13 + rnd.uniform(-0.15, 0.15)
        L = rnd.uniform(2.8, 3.6)
        lift = rnd.uniform(0.9, 1.2)
        d = Vector((math.cos(a), math.sin(a), 0))
        side = Vector((-d.y, d.x, 0))
        bm = bmesh.new()
        n = 16
        left, mid, right = [], [], []
        for k in range(n + 1):
            t = k / n
            # arching centreline: rises then droops
            c = d * L * t + Vector((0, 0, L * lift * (0.9 * t - 0.75 * t * t) + 0.1))
            w = 0.62 * math.sin(math.pi * min(1.0, t * 1.15)) * (1 - 0.5 * t) + 0.03
            serr = 1.0 if k % 2 == 0 else 0.55
            mid.append(bm.verts.new(c + Vector((0, 0, 0.05))))
            left.append(bm.verts.new(c + side * w * serr - Vector((0, 0, 0.08 * serr))))
            right.append(bm.verts.new(c - side * w * serr - Vector((0, 0, 0.08 * serr))))
        for k in range(n):
            bm.faces.new((left[k], left[k + 1], mid[k + 1], mid[k]))
            bm.faces.new((mid[k], mid[k + 1], right[k + 1], right[k]))
        # back faces so the frond is visible from below
        bmesh.ops.reverse_faces(bm, faces=list(bm.faces)) if False else None
        o = _obj_from_bm(f'frond{f}', bm, rnd.choice(['leaf', 'leaf_light', 'leaf']))
        sol = o.modifiers.new('sol', 'SOLIDIFY')
        sol.thickness = 0.04
    blob('crown', 0.45, (0, 0, 0.15), 'leaf_dark', subdiv=1, amp=0.2, scale=(1, 1, 0.6))
    return finalize('fern', smooth_angle=40)


def reeds():
    """A52 - reeds and cattails for pond/river edges."""
    reset()
    rnd = random.Random(52)
    for i in range(26):
        a = rnd.uniform(0, 6.28); d = math.sqrt(rnd.random()) * 1.4
        x, y = math.cos(a) * d, math.sin(a) * d
        h = rnd.uniform(3.0, 5.5)
        lean = (rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3))
        tube(f'r{i}', [(x, y, 0), (x + lean[0] * 0.5, y + lean[1] * 0.5, h * 0.6), (x + lean[0], y + lean[1], h)], 0.05,
             rnd.choice(['leaf', 'leaf_dark', 'grass_dry']), res=4, taper=[1, 0.8, 0.2], ures=2)
        if i % 3 == 0:
            cyl(f'cat{i}', 0.16, 0.85, loc=(x + lean[0] * 0.85, y + lean[1] * 0.85, h * 0.8), key='wood_dark', verts=8)
    for i in range(14):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0.2, 1.6)
        L = rnd.uniform(2, 3.5)
        tube(f'bl{i}', [(math.cos(a) * d, math.sin(a) * d, 0), (math.cos(a) * (d + 0.6), math.sin(a) * (d + 0.6), L * 0.7),
                        (math.cos(a) * (d + 1.2), math.sin(a) * (d + 1.2), L * 0.6)], 0.1, 'leaf', res=4, taper=[1, 0.6, 0.05], ures=2)
    return finalize('reeds', smooth_angle=60)


def lily_pads():
    """A53 - floating lily pads with two water lilies (place at water level)."""
    reset()
    rnd = random.Random(53)
    for i in range(7):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, 3.2)
        r = rnd.uniform(0.8, 1.4)
        pts = []
        notch = rnd.uniform(0, 6.28)
        for k in range(20):
            ang = notch + 0.3 + (2 * math.pi - 0.6) * k / 19
            pts.append((math.cos(ang) * r, math.sin(ang) * r))
        pts.append((0, 0))
        o = poly_prism(f'pad{i}', pts, 0.06, loc=(math.cos(a) * d, math.sin(a) * d, 0), key=rnd.choice(['leaf', 'leaf_dark']))
    for j, (x, y) in enumerate(((0.6, 0.4), (-1.5, -1.0))):
        for k in range(10):
            ang = 2 * math.pi * k / 10
            lay = 1 if k % 2 else 0
            o = ball(f'pet{j}_{k}', 0.32, loc=(x + math.cos(ang) * 0.28, y + math.sin(ang) * 0.28, 0.18 + lay * 0.08), key='fl_pink' if j == 0 else 'fl_white',
                     segs=6, rings=4, scale=(1.0, 0.45, 0.3))
            o.rotation_euler = (0, math.radians(-35 - lay * 15), ang)
        ball(f'lc{j}', 0.15, loc=(x, y, 0.3), key='fl_yellow', segs=8, rings=5)
    return finalize('lily_pads', smooth_angle=50)


def mushroom_cluster():
    """A54 - mushroom cluster: red spotted caps and tan caps on a mossy log stub."""
    reset()
    rnd = random.Random(54)
    spec = [(0, 0, 1.6, 0.85, 'fl_red'), (0.9, 0.35, 1.0, 0.55, 'fl_red'), (-0.7, 0.5, 0.8, 0.45, 'mush_tan'),
            (0.3, -0.8, 1.2, 0.6, 'mush_tan'), (-0.4, -0.4, 0.55, 0.3, 'fl_red')]
    for i, (x, y, h, r, k) in enumerate(spec):
        lathe(f'stem{i}', [(0.0, 0), (r * 0.42, 0), (r * 0.32, h * 0.4), (r * 0.28, h), (0.0, h)], loc=(x, y, 0), key='fl_white', segs=10)
        lathe(f'cap{i}', [(0.0, h - 0.05), (r * 0.35, h - 0.08), (r, h + r * 0.05), (r * 0.92, h + r * 0.35), (r * 0.55, h + r * 0.62), (0.0, h + r * 0.7)],
              loc=(x, y, 0), key=k, segs=16)
        if k == 'fl_red':
            for s in range(7):
                a = rnd.uniform(0, 6.28); el = rnd.uniform(0.25, 1.0)
                ball(f'spot{i}_{s}', r * 0.1, loc=(x + math.cos(a) * r * 0.85 * math.cos(el), y + math.sin(a) * r * 0.85 * math.cos(el),
                                                   h + r * 0.1 + r * 0.55 * math.sin(el)), key='fl_white', segs=6, rings=4, scale=(1, 1, 0.5))
    blob('moss', 1.6, (0, 0, 0), 'moss', subdiv=2, amp=0.3, scale=(1.3, 1.1, 0.12), seed=54)
    return finalize('mushroom_cluster', smooth_angle=50)


# ----------------------------------------------------------------- rocks & cliffs
def pebbles():
    """A55 - pebble cluster."""
    reset()
    rnd = random.Random(55)
    for i in range(18):
        a = rnd.uniform(0, 6.28); d = math.sqrt(rnd.random()) * 2.0
        rock(f'p{i}', rnd.uniform(0.18, 0.42), (math.cos(a) * d, math.sin(a) * d, 0.1), rnd.choice(['stone', 'stone_light', 'stone_dark']),
             seed=i, scale=(1.2, 1.0, 0.6), subdiv=1, amp=0.2)
    return finalize('pebbles', smooth_angle=12)


def _single_rock(seed, r, name, key='stone', moss=True, sc=(1.25, 1.0, 0.75)):
    reset()
    rnd = random.Random(seed)
    a = rock('rock', r, (0, 0, r * sc[2] * 0.55), key, seed=seed, scale=sc, subdiv=3 if r < 3 else 4, amp=0.32)
    b = rock('rock2', r * 0.45, (r * 0.9, -r * 0.4, r * 0.2), key, seed=seed + 1, scale=(1.2, 1, 0.7), subdiv=3, amp=0.3)
    if moss:
        top_paint(a, 'moss', 0.74, seed)
        top_paint(b, 'moss', 0.8, seed + 1)
    from roads import tuft
    for i in range(8):
        a = rnd.uniform(0, 6.28)
        tuft(f't{i}', math.cos(a) * r * 1.25, math.sin(a) * r * 1.0, 0.0, rnd)
    return finalize(name, smooth_angle=12)


def rock_small_1():
    """A56 - small rock 1.5 studs."""
    return _single_rock(56, 1.5, 'rock_small_1', moss=False)

def rock_small_2():
    """A57 - small mossy rock."""
    return _single_rock(57, 1.8, 'rock_small_2', key='stone_dark')

def rock_medium_1():
    """A58 - medium rock 3.5 studs."""
    return _single_rock(58, 3.5, 'rock_medium_1')

def rock_medium_2():
    """A59 - medium rock, light limestone."""
    return _single_rock(59, 3.0, 'rock_medium_2', key='stone_light', moss=False, sc=(1.4, 0.9, 0.6))

def boulder_1():
    """A60 - large boulder 7 studs."""
    return _single_rock(60, 7.0, 'boulder_1')

def boulder_2():
    """A61 - tall split boulder."""
    reset()
    rnd = random.Random(61)
    a = rock('a', 5.0, (-1.6, 0, 4.0), 'stone', seed=61, scale=(0.8, 1.0, 1.25), amp=0.3, subdiv=4)
    b = rock('b', 4.6, (2.0, 0.3, 3.4), 'stone', seed=62, scale=(0.8, 1.0, 1.1), amp=0.3, subdiv=4)
    rock('c', 2.0, (0.5, -4.0, 0.8), 'stone_dark', seed=63, scale=(1.3, 1.0, 0.7), subdiv=3)
    top_paint(a, 'moss', 0.7, 61); top_paint(b, 'moss', 0.74, 62)
    return finalize('boulder_2', smooth_angle=12)


def _cliff(seed, name, w, h, d):
    """Layered cliff face: stacked strata slabs with noise, overhang and moss/grass on top."""
    reset()
    rnd = random.Random(seed)
    z = 0
    i = 0
    while z < h:
        sh = rnd.uniform(2.5, 4.5)
        inset = rnd.uniform(-0.8, 0.8)
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=4, use_grid_fill=True)
        off = Vector((seed + i * 3.1, i * 1.7, 0))
        for v in bm.verts:
            v.co.x *= w * rnd.uniform(0.95, 1.0); v.co.y *= d; v.co.z *= sh
            n = noise.noise(v.co * 0.35 + off)
            v.co.y += n * 1.4 + (inset if v.co.y < 0 else 0)
            v.co.x += noise.noise(v.co * 0.5 + off * 2) * 0.6
        o = _obj_from_bm(f'stratum{i}', bm, rnd.choice(['cliff_a', 'cliff_b', 'cliff_a']))
        o.location = (0, 0, z + sh / 2)
        top_paint(o, 'moss', 0.8, seed + i, noise_amt=0.15)
        z += sh * 0.92
        i += 1
    z += sh * 0.04
    # grass tufts and hanging vines
    from roads import tuft
    for k in range(18):
        tuft(f'tf{k}', rnd.uniform(-w / 2, w / 2), rnd.uniform(-d / 2, d / 2), z + 0.2, rnd, h=1.0)
    for k in range(6):
        x = rnd.uniform(-w / 2 + 1, w / 2 - 1)
        tube(f'vine{k}', [(x, -d / 2 - 0.6, z), (x + 0.3, -d / 2 - 1.0, z - 2.5), (x - 0.2, -d / 2 - 0.9, z - rnd.uniform(4, 7))],
             0.18, 'leaf_dark', res=4, taper=[1, 0.8, 0.3], ures=3)
    # rubble at foot
    for k in range(6):
        rock(f'rub{k}', rnd.uniform(0.6, 1.5), (rnd.uniform(-w / 2, w / 2), -d / 2 - rnd.uniform(0.5, 2.5), 0.3),
             rnd.choice(['cliff_a', 'cliff_b']), seed=seed + k, subdiv=1)
    return finalize(name, smooth_angle=25)


def cliff_1():
    """A62 - cliff face, 20 wide x 18 tall."""
    return _cliff(62, 'cliff_1', 20, 18, 7)

def cliff_2():
    """A63 - cliff face, 28 wide x 26 tall."""
    return _cliff(63, 'cliff_2', 28, 26, 9)

def cliff_3():
    """A64 - low cliff ledge, 16 wide x 9 tall."""
    return _cliff(64, 'cliff_3', 16, 9, 6)


def rock_arch():
    """A65 - natural rock arch, 22 wide x 16 tall."""
    reset()
    rnd = random.Random(65)
    n = 13
    for i in range(n):
        a = math.pi * i / (n - 1)
        x = -math.cos(a) * 9.5; z = math.sin(a) * 11.5
        r = 3.4 - math.sin(a) * 1.0
        s = rock(f'seg{i}', r, (x, rnd.uniform(-0.3, 0.3), z + 1.8), rnd.choice(['cliff_a', 'cliff_b']), seed=65 + i,
                 scale=(1.1, 1.0, 1.0), amp=0.28)
        top_paint(s, 'moss', 0.7, 65 + i)
    for e in (-1, 1):
        rock(f'foot{e}', 4.2, (e * 10.5, 0, 1.5), 'cliff_b', seed=90 + e, scale=(1.1, 1.1, 0.7))
    return finalize('rock_arch', smooth_angle=12)


def stepping_stones():
    """A66 - stepping stones across a stream, 16 long."""
    reset()
    rnd = random.Random(66)
    for i in range(7):
        y = -8 + i * 2.6 + rnd.uniform(-0.3, 0.3)
        x = math.sin(i * 0.9) * 1.2
        rock(f's{i}', rnd.uniform(1.6, 2.0), (x, y, 0.2), rnd.choice(['stone', 'stone_light']), seed=66 + i,
             scale=(1.25, 1.05, 0.38), amp=0.18)
    return finalize('stepping_stones', smooth_angle=12)


# ----------------------------------------------------------------- ground clutter
def fallen_log():
    """A67 - fallen mossy log with broken branch stubs and pale cut ends."""
    reset()
    rnd = random.Random(67)
    L, r = 14.0, 1.1
    tube('log', [(-L / 2, 0, r * 0.9), (0, 0.3, r * 0.95), (L / 2, 0, r * 0.85)], r, 'bark', res=8, taper=[1.0, 0.95, 0.85], ures=4)
    for e, rr in ((-1, r), (1, r * 0.85)):
        cyl(f'end{e}', rr * 0.92, 0.05, loc=(e * (L / 2 + 0.02), 0, r * 0.9 if e < 0 else r * 0.85), key='wood_light', verts=16, rot=(0, 90, 0))
        torus(f'ring{e}', rr * 0.5, 0.05, loc=(e * (L / 2 + 0.05), 0, r * 0.9 if e < 0 else r * 0.85), key='wood', segs=14, rsegs=4, rot=(0, 90, 0))
    for i in range(4):
        x = rnd.uniform(-L / 2 + 1.5, L / 2 - 1.5)
        a = rnd.uniform(-1.2, 1.2)
        tube(f'stub{i}', [(x, math.sin(a) * r * 0.6, r + math.cos(a) * r * 0.6), (x + 0.4, math.sin(a) * 2.2, r + math.cos(a) * 1.8)], 0.2,
             'bark', res=4, taper=[1, 0.6])
    for i in range(6):
        x = rnd.uniform(-L / 2 + 1, L / 2 - 1)
        blob(f'moss{i}', rnd.uniform(0.9, 1.5), (x, rnd.uniform(-0.3, 0.3), r * 1.75), 'moss', subdiv=2, amp=0.3, scale=(1.4, 0.9, 0.22), seed=i)
    return finalize('fallen_log', smooth_angle=45)


def _stump(seed, r, h, name):
    reset()
    rnd = random.Random(seed)
    trunk_flare('stump', r, h, rnd=rnd, roots=6)
    cyl('top', r * 0.88, 0.06, loc=(0, 0, h - 0.02), key='wood_light', verts=16)
    for k in range(3):
        torus(f'ring{k}', r * (0.25 + k * 0.22), 0.04, loc=(0, 0, h + 0.03), key='wood', segs=16, rsegs=4)
    # jagged break on one side
    for k in range(4):
        a = rnd.uniform(-0.6, 0.6)
        cyl(f'splinter{k}', r * 0.18, rnd.uniform(0.4, 1.0), loc=(math.cos(a) * r * 0.7, math.sin(a) * r * 0.7, h - 0.05), key='bark',
            verts=4, r2=0.02)
    blob('moss', r * 0.8, (-r * 0.5, 0, h * 0.4), 'moss', subdiv=2, amp=0.3, scale=(0.6, 1.2, 0.8), seed=seed)
    return finalize(name, smooth_angle=45)


def stump_1():
    """A68 - wide old stump."""
    return _stump(68, 1.6, 2.2, 'stump_1')

def stump_2():
    """A69 - narrow axe-cut stump."""
    return _stump(69, 1.0, 1.4, 'stump_2')


def branch_pile():
    """A70 - pile of fallen branches and twigs."""
    reset()
    rnd = random.Random(70)
    for i in range(14):
        a = rnd.uniform(0, math.pi); L = rnd.uniform(3, 6)
        c = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), 0.2 + i * 0.05))
        d = Vector((math.cos(a), math.sin(a), rnd.uniform(-0.05, 0.08)))
        p0, p1 = c - d * L / 2, c + d * L / 2
        mid = (p0 + p1) / 2 + Vector((rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3), 0.15))
        tube(f'br{i}', [tuple(p0), tuple(mid), tuple(p1)], rnd.uniform(0.1, 0.22), rnd.choice(['bark', 'bark_dead']), res=4,
             taper=[1, 0.8, 0.4], ures=3)
        tw = mid + Vector((rnd.uniform(-0.8, 0.8), rnd.uniform(-0.8, 0.8), 0.6))
        tube(f'tw{i}', [tuple(mid), tuple(tw)], 0.06, 'bark_dead', res=4, taper=[1, 0.3])
    for i in range(10):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, 3)
        box(f'lf{i}', (0.45, 0.3, 0.04), loc=(math.cos(a) * d, math.sin(a) * d, 0.03), key=rnd.choice(['autumn_a', 'autumn_c', 'leaf_dark']),
            rot=(0, 0, rnd.uniform(0, 360)))
    return finalize('branch_pile', smooth_angle=50)


TREES = [
    ('A24_oak_1', oak_1), ('A25_oak_2', oak_2), ('A26_oak_3', oak_3), ('A27_birch_1', birch_1), ('A28_birch_2', birch_2),
    ('A29_pine_1', pine_1), ('A30_pine_2', pine_2), ('A31_pine_3', pine_3), ('A32_maple_autumn', maple_autumn),
    ('A33_willow', willow), ('A34_fruit_tree', fruit_tree), ('A35_dead_tree_1', dead_tree_1), ('A36_dead_tree_2', dead_tree_2),
    ('A37_sapling', sapling),
]
PLANTS = [
    ('A38_bush_1', bush_1), ('A39_bush_2', bush_2), ('A40_bush_3', bush_3), ('A41_hedge_straight', hedge_straight),
    ('A42_hedge_corner', hedge_corner), ('A43_flowers_red', flowers_red), ('A44_flowers_yellow', flowers_yellow),
    ('A45_flowers_purple', flowers_purple), ('A46_flowers_white', flowers_white), ('A47_flowers_blue', flowers_blue),
    ('A48_planter_box', planter_box), ('A49_tall_grass_1', tall_grass_1), ('A50_tall_grass_2', tall_grass_2),
    ('A51_fern', fern), ('A52_reeds', reeds), ('A53_lily_pads', lily_pads), ('A54_mushroom_cluster', mushroom_cluster),
]
ROCKS = [
    ('A55_pebbles', pebbles), ('A56_rock_small_1', rock_small_1), ('A57_rock_small_2', rock_small_2),
    ('A58_rock_medium_1', rock_medium_1), ('A59_rock_medium_2', rock_medium_2), ('A60_boulder_1', boulder_1),
    ('A61_boulder_2', boulder_2), ('A62_cliff_1', cliff_1), ('A63_cliff_2', cliff_2), ('A64_cliff_3', cliff_3),
    ('A65_rock_arch', rock_arch), ('A66_stepping_stones', stepping_stones),
    ('A67_fallen_log', fallen_log), ('A68_stump_1', stump_1), ('A69_stump_2', stump_2), ('A70_branch_pile', branch_pile),
]
ITEMS = TREES + PLANTS + ROCKS
