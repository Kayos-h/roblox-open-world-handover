# props.py - everyday props (A71-A108) and water features (A109-A111).
# Scale: character ~5.5 studs; table top 3.0; chair seat 1.9; door 8-9.
import math, random
import bmesh
from mathutils import Vector, noise
from kitlib import *
from kitlib import _obj_from_bm
from nature import blob


# ----------------------------------------------------------------- helpers
def staves(name, h, r_end, r_mid, loc=(0, 0, 0), key='wood', n=18, gap=0.88):
    """Barrel body built from staves: bulged lathe with alternating radius for stave grooves."""
    bm = bmesh.new()
    rows = []
    zs = [0, 0.12, 0.3, 0.5, 0.7, 0.88, 1.0]
    for t in zs:
        r = r_end + (r_mid - r_end) * math.sin(math.pi * t)
        ring = []
        for i in range(n * 2):
            a = math.pi * i / n
            rr = r * (1.0 if i % 2 == 0 else (1.0 - (1 - gap) * 0.25))
            ring.append(bm.verts.new((math.cos(a) * rr, math.sin(a) * rr, t * h)))
        rows.append(ring)
    m = n * 2
    for a, b in zip(rows, rows[1:]):
        for i in range(m):
            bm.faces.new((a[i], a[(i + 1) % m], b[(i + 1) % m], b[i]))
    bm.faces.new(list(reversed(rows[0])))
    top = bm.faces.new(rows[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj_from_bm(name, bm, key)
    o.location = loc
    return o


def hoop(name, r, z, loc=(0, 0, 0), key='iron', w=0.22, t=0.06):
    return lathe(name, [(0.0, z - w / 2), (r + t, z - w / 2), (r + t, z + w / 2), (0.0, z + w / 2)],
                 loc=loc, key=key, segs=36)


def barrel_body(prefix, loc=(0, 0, 0), h=4.0, open_top=False):
    x, y, z = loc
    staves(f'{prefix}_st', h, 1.25, 1.5, loc=(x, y, z), key='wood')
    for t in (0.1, 0.3, 0.7, 0.9):
        r = 1.25 + 0.25 * math.sin(math.pi * t)
        hoop(f'{prefix}_h{t}', r, z + t * h, loc=(x, y, 0))
    if open_top:
        cyl(f'{prefix}_inner', 1.2, 0.05, loc=(x, y, z + h * 0.93), key='wood_dark', verts=24)
    else:
        cyl(f'{prefix}_lid', 1.2, 0.08, loc=(x, y, z + h - 0.12), key='wood_light', verts=24)
        for i in range(-2, 3):
            box(f'{prefix}_lidline{i}', (0.04, 2.2 - abs(i) * 0.35, 0.02), loc=(x + i * 0.45, y, z + h - 0.03), key='wood_dark')
        cyl(f'{prefix}_bung', 0.14, 0.06, loc=(x + 0.6, y + 0.3, z + h - 0.04), key='wood_dark', verts=8)


def plank_box(prefix, size, loc=(0, 0, 0), rnd=None, key_pl=('wood', 'wood_light'), frame='wood_dark', planks=4, rot=0.0):
    """Crate made of planks with corner battens and an X brace on the front/back."""
    rnd = rnd or random.Random(0)
    sx, sy, sz = size
    x, y, z = loc
    objs = []
    ph = sz / planks
    for k in range(planks):
        zz = z + ph * (k + 0.5)
        for sgn in (-1, 1):
            objs.append(box(f'{prefix}_fy{sgn}{k}', (sx - 0.1, 0.12, ph - 0.06), loc=(x, y + sgn * (sy / 2 - 0.06), zz),
                            key=rnd.choice(key_pl), bev=0.02, segs=1))
            objs.append(box(f'{prefix}_fx{sgn}{k}', (0.12, sy - 0.3, ph - 0.06), loc=(x + sgn * (sx / 2 - 0.06), y, zz),
                            key=rnd.choice(key_pl), bev=0.02, segs=1))
    for k in range(planks):
        objs.append(box(f'{prefix}_top{k}', (sx - 0.1, sy / planks - 0.06, 0.12), loc=(x, y - sy / 2 + sy / planks * (k + 0.5), z + sz - 0.06),
                        key=rnd.choice(key_pl), bev=0.02, segs=1))
    objs.append(box(f'{prefix}_bot', (sx - 0.2, sy - 0.2, 0.12), loc=(x, y, z + 0.06), key=frame))
    for sx_ in (-1, 1):
        for sy_ in (-1, 1):
            objs.append(box(f'{prefix}_c{sx_}{sy_}', (0.22, 0.22, sz), loc=(x + sx_ * (sx / 2 - 0.05), y + sy_ * (sy / 2 - 0.05), z + sz / 2),
                            key=frame, bev=0.03, segs=1))
    for sgn in (-1, 1):
        L = math.hypot(sx - 0.4, sz - 0.4)
        ang = math.degrees(math.atan2(sz - 0.4, sx - 0.4))
        objs.append(box(f'{prefix}_x{sgn}', (L, 0.14, 0.24), loc=(x, y + sgn * (sy / 2 + 0.03), z + sz / 2), key=frame,
                        rot=(0, -ang * sgn, 0), bev=0.02, segs=1))
    if rot:
        for o in objs:
            o.location = Vector((x, y, 0)) + (Vector(o.location) - Vector((x, y, 0))).to_3d()
    return objs


def wheel(prefix, r, loc, axis='X', key='wood_dark', spokes=10, w=0.35, iron=True):
    rot = (0, 90, 0) if axis == 'X' else (90, 0, 0)
    torus(f'{prefix}_rim', r - 0.12, 0.17, loc=loc, key='wood', segs=28, rsegs=6, rot=rot)
    if iron:
        torus(f'{prefix}_tyre', r - 0.02, 0.07, loc=loc, key='iron', segs=28, rsegs=4, rot=rot)
    cyl(f'{prefix}_hub', r * 0.18, w * 1.6, loc=loc, key=key, verts=12, rot=rot)
    hub = Vector(loc)
    for i in range(spokes):
        a = 2 * math.pi * i / spokes
        if axis == 'X':
            d = Vector((0, math.cos(a), math.sin(a)))
        else:
            d = Vector((math.cos(a), 0, math.sin(a)))
        tube(f'{prefix}_sp{i}', [tuple(hub + d * r * 0.15), tuple(hub + d * (r - 0.2))], 0.07, key, res=4)
    # hub offset: cyl starts at loc along local Z; centre it
    o = bpy.data.objects[f'{prefix}_hub']
    if axis == 'X':
        o.location.x -= w * 0.8
    else:
        o.location.y += w * 0.8


def cloth(name, w, h, loc, key, waves=1.5, amp=0.25, rot=(90, 0, 0), sag=0.0, res=(14, 10), seed=0, hang_from_top=True):
    """Waving cloth panel (banner/awning). Built in XZ, then rotated."""
    bm = bmesh.new()
    nx, nz = res
    grid = []
    for j in range(nz + 1):
        row = []
        for i in range(nx + 1):
            u, v = i / nx, j / nz
            x = (u - 0.5) * w
            z = -v * h if hang_from_top else v * h
            dy = math.sin(u * math.pi * 2 * waves + v * 1.3 + seed) * amp * (v if hang_from_top else 1.0) - sag * math.sin(u * math.pi)
            row.append(bm.verts.new((x, dy, z)))
        grid.append(row)
    for j in range(nz):
        for i in range(nx):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    o = _obj_from_bm(name, bm, key)
    s = o.modifiers.new('sol', 'SOLIDIFY'); s.thickness = 0.06
    o.location = loc
    o.rotation_euler = [math.radians(a) for a in rot] if rot != (90, 0, 0) else (0, 0, 0)
    return o


# ----------------------------------------------------------------- A71-A78 containers
def barrel():
    """A71 - oak barrel with iron hoops and lid."""
    reset()
    barrel_body('b')
    return finalize('barrel', smooth_angle=40)


def barrel_open():
    """A72 - open barrel full of apples."""
    reset()
    rnd = random.Random(72)
    barrel_body('b', open_top=True)
    for i in range(40):
        a = rnd.uniform(0, 6.28); d = math.sqrt(rnd.random()) * 1.05
        zz = 3.75 + (1.05 - d) * 0.55 + rnd.uniform(0, 0.15)
        ball(f'ap{i}', 0.32, loc=(math.cos(a) * d, math.sin(a) * d, zz),
             key=rnd.choice(['fruit', 'fruit', 'leaf_light', 'fl_yellow']), segs=10, rings=7)
    return finalize('barrel_open', smooth_angle=40)


def crate_small():
    """A73 - small slatted crate, 3 studs."""
    reset()
    plank_box('c', (3, 3, 3), rnd=random.Random(73), planks=3)
    return finalize('crate_small', smooth_angle=30)


def crate_large():
    """A74 - large shipping crate, 5 x 4 x 4 with stencil band."""
    reset()
    plank_box('c', (5, 4, 4), rnd=random.Random(74), planks=4)
    box('stencil', (2.2, 0.03, 0.7), loc=(0, -2.1, 2.2), key='iron_dark')
    return finalize('crate_large', smooth_angle=30)


def crate_stack():
    """A75 - stack of crates and a barrel, ready to dress docks and markets."""
    reset()
    rnd = random.Random(75)
    plank_box('a', (4, 4, 4), loc=(0, 0, 0), rnd=rnd)
    plank_box('b', (3, 3, 3), loc=(4.2, 0.4, 0), rnd=rnd, planks=3)
    plank_box('c', (3, 3, 3), loc=(0.3, -0.2, 4.0), rnd=rnd, planks=3)
    barrel_body('br', loc=(-3.2, 1.0, 0))
    plank_box('d', (2.2, 2.2, 2.2), loc=(4.0, -2.8, 0), rnd=rnd, planks=2)
    return finalize('crate_stack', smooth_angle=30)


def _sack_shape(name, loc, h=2.6, r=1.0, rnd=None, key='fabric_cream', lean=0.0):
    rnd = rnd or random.Random(0)
    o = lathe(name, [(0.0, 0.0), (r * 1.05, 0.02), (r * 1.22, h * 0.18), (r * 1.18, h * 0.42), (r * 0.98, h * 0.66),
                     (r * 0.55, h * 0.8), (r * 0.24, h * 0.86), (r * 0.36, h * 0.95), (r * 0.42, h * 1.0), (r * 0.2, h * 0.98), (0.0, h * 0.96)],
              loc=loc, key=key, segs=16)
    me = o.data
    off = Vector((rnd.uniform(0, 50), rnd.uniform(0, 50), 0))
    for v in me.vertices:
        sl = max(0.0, 1.0 - v.co.z / h)
        v.co += Vector((noise.noise(v.co * 1.1 + off) * 0.22, noise.noise(v.co * 1.1 + off * 2) * 0.22, noise.noise(v.co * 1.6 + off) * 0.1 * sl))
    o.rotation_euler = (math.radians(lean), 0, rnd.uniform(0, 6.28))
    torus(name + '_tie', r * 0.27, 0.07, loc=(loc[0], loc[1], loc[2] + h * 0.86), key='rope', segs=12, rsegs=4)
    return o


def sack():
    """A76 - grain sack tied at the top."""
    reset()
    _sack_shape('s', (0, 0, 0), rnd=random.Random(76))
    return finalize('sack', smooth_angle=60)


def sack_pile():
    """A77 - pile of sacks, some lying, one spilling grain."""
    reset()
    rnd = random.Random(77)
    for i, (x, y, z, lean) in enumerate(((0, 0, 0, 0), (2.0, 0.3, 0, 8), (-1.9, 0.5, 0, -6), (0.9, 2.0, 0, 12), (0.2, 0.6, 1.9, 75))):
        _sack_shape(f's{i}', (x, y, z), rnd=rnd, lean=lean, key=rnd.choice(['fabric_cream', 'thatch', 'fabric_cream']))
    for i in range(30):
        a = rnd.uniform(-0.5, 0.8); d = rnd.uniform(1.4, 3.2)
        ball(f'gr{i}', 0.09, loc=(math.cos(a) * d, -1.4 - math.sin(a) * 0.5 * d, 0.05), key='thatch', segs=6, rings=4, scale=(1.4, 1, 0.6))
    return finalize('sack_pile', smooth_angle=60)


def hay_bale():
    """A78 - square hay bale with twine bands and loose straw."""
    reset()
    rnd = random.Random(78)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=6, use_grid_fill=True)
    sx, sy, sz = 5.0, 2.6, 2.4
    rad = 0.45
    for v in bm.verts:
        p = Vector((v.co.x * sx, v.co.y * sy, v.co.z * sz))
        inner = Vector((max(-sx / 2 + rad, min(sx / 2 - rad, p.x)), max(-sy / 2 + rad, min(sy / 2 - rad, p.y)), max(-sz / 2 + rad, min(sz / 2 - rad, p.z))))
        d = p - inner
        if d.length > 1e-6:
            p = inner + d.normalized() * rad
        p += Vector((noise.noise(p * 2.1) * 0.08, noise.noise(p * 2.3 + Vector((5, 0, 0))) * 0.08, noise.noise(p * 1.9) * 0.06))
        v.co = p
    o = _obj_from_bm('bale', bm, 'thatch')
    o.location = (0, 0, sz / 2)
    for x in (-1.2, 1.2):
        lathe(f'tw{x}', [(0, 0), (0, 0)], key='rope') if False else None
        box(f'twine{x}', (0.12, sy + 0.06, sz + 0.06), loc=(x, 0, sz / 2), key='rope_dark', bev=0.04, segs=1)
    for i in range(24):
        a = rnd.uniform(0, 6.28)
        x = rnd.uniform(-sx / 2, sx / 2); y = rnd.choice((-1, 1)) * (sy / 2 + rnd.uniform(0.0, 1.0))
        tube(f'straw{i}', [(x, y, 0.03), (x + math.cos(a) * 0.8, y + math.sin(a) * 0.8, 0.05)], 0.035, 'thatch', res=4)
    for i in range(14):
        x = rnd.uniform(-sx / 2 + 0.3, sx / 2 - 0.3)
        tube(f'tst{i}', [(x, rnd.uniform(-1, 1), sz + 0.02), (x + rnd.uniform(-0.6, 0.6), rnd.uniform(-1, 1), sz + rnd.uniform(0.15, 0.4))], 0.035, 'thatch', res=4)
    return finalize('hay_bale', smooth_angle=50)


# ----------------------------------------------------------------- A79-A81 carts
def hand_cart():
    """A79 - two-wheel hand cart with sideboards and long handles."""
    reset()
    rnd = random.Random(79)
    L, Wd = 6.0, 3.4
    zb = 2.2
    box('bed', (L, Wd, 0.25), loc=(0, 0, zb), key='wood', bev=0.03)
    for k in range(5):
        box(f'bp{k}', (L / 5 - 0.06, Wd, 0.06), loc=(-L / 2 + L / 5 * (k + 0.5), 0, zb + 0.15), key=rnd.choice(['wood', 'wood_light']))
    for s in (-1, 1):
        for k in range(2):
            box(f'side{s}{k}', (L, 0.14, 0.45), loc=(0, s * (Wd / 2 - 0.07), zb + 0.5 + k * 0.55), key=rnd.choice(['wood', 'wood_light']), bev=0.03, segs=1)
        for x in (-L / 2 + 0.2, 0, L / 2 - 0.2):
            box(f'stake{s}{x}', (0.2, 0.2, 1.5), loc=(x, s * (Wd / 2 - 0.05), zb + 0.75), key='wood_dark', bev=0.03, segs=1)
        box(f'handle{s}', (4.5, 0.25, 0.25), loc=(-L / 2 - 2.0, s * (Wd / 2 - 0.4), zb - 0.4), key='wood_dark', rot=(0, -12, 0), bev=0.05)
        wheel(f'w{s}', 2.0, (0.8, s * (Wd / 2 + 0.45), 2.0), axis='Y')
    for s in (-1, 1):
        box(f'leg{s}', (0.22, 0.22, 2.1), loc=(-L / 2 + 0.4, s * (Wd / 2 - 0.4), 1.05), key='wood_dark')
    box('axle', (0.25, Wd + 1.2, 0.25), loc=(0.8, 0, 2.0), key='iron')
    return finalize('hand_cart', smooth_angle=35)


def wagon():
    """A80 - four-wheel goods wagon (horseless), with draw pole, canvas bundle and barrels."""
    reset()
    rnd = random.Random(80)
    L, Wd, zb = 12.0, 5.0, 3.4
    box('bed', (L, Wd, 0.35), loc=(0, 0, zb), key='wood', bev=0.04)
    for s in (-1, 1):
        for k in range(3):
            box(f'side{s}{k}', (L, 0.16, 0.5), loc=(0, s * (Wd / 2 - 0.08), zb + 0.55 + k * 0.6), key=rnd.choice(['wood', 'wood_light']), bev=0.03, segs=1)
        for x in [-L / 2 + 0.2 + i * (L - 0.4) / 5 for i in range(6)]:
            box(f'stake{s}{x:.1f}', (0.24, 0.24, 2.2), loc=(x, s * (Wd / 2 - 0.05), zb + 1.0), key='wood_dark', bev=0.03, segs=1)
            box(f'iron{s}{x:.1f}', (0.28, 0.28, 0.12), loc=(x, s * (Wd / 2 - 0.05), zb + 1.9), key='iron')
        for x in (-L / 2 + 2.4, L / 2 - 2.4):
            wheel(f'w{s}{x}', 2.6 if x < 0 else 2.2, (x, s * (Wd / 2 + 0.5), 2.6 if x < 0 else 2.2), axis='Y', spokes=12)
    for e in (-1, 1):
        box(f'endboard{e}', (0.16, Wd, 1.6), loc=(e * (L / 2 - 0.08), 0, zb + 1.0), key='wood', bev=0.03)
    for x in (-L / 2 + 2.4, L / 2 - 2.4):
        box(f'axle{x}', (0.3, Wd + 1.4, 0.3), loc=(x, 0, 2.6 if x < 0 else 2.2), key='iron')
    tube('pole', [(L / 2, 0, 2.4), (L / 2 + 3.0, 0, 1.6), (L / 2 + 6.0, 0, 0.6)], 0.2, 'wood_dark', res=4)
    box('yoke', (0.3, 3.0, 0.3), loc=(L / 2 + 5.4, 0, 0.8), key='wood_dark')
    box('seat', (1.2, Wd - 0.6, 0.3), loc=(L / 2 - 1.0, 0, zb + 1.9), key='wood_light', bev=0.05)
    # cargo
    barrel_body('cb1', loc=(-2.5, -1.0, zb + 0.2), h=3.2)
    barrel_body('cb2', loc=(-2.5, 1.1, zb + 0.2), h=3.2)
    plank_box('cc', (3, 3, 2.6), loc=(1.4, 0, zb + 0.2), rnd=rnd, planks=3)
    blob('canvas', 2.0, (-0.6, 0, zb + 3.2), 'fabric_cream', subdiv=3, amp=0.12, scale=(1.6, 1.0, 0.6), seed=80) if False else None
    return finalize('wagon', smooth_angle=35)


def wheelbarrow():
    """A81 - wooden wheelbarrow with single front wheel."""
    reset()
    rnd = random.Random(81)
    # tray: trapezoid sides
    poly_prism('trayL', [(-1.6, 0), (1.4, 0), (2.2, 1.4), (-2.2, 1.4)], 0.14, loc=(0, -1.1, 1.6), key='wood', rot=(90, 0, 0))
    poly_prism('trayR', [(-1.6, 0), (1.4, 0), (2.2, 1.4), (-2.2, 1.4)], 0.14, loc=(0, 1.24, 1.6), key='wood', rot=(90, 0, 0))
    box('floor', (3.0, 2.2, 0.14), loc=(-0.1, 0, 1.65), key='wood_light', bev=0.02)
    box('front', (0.14, 2.6, 1.4), loc=(1.85, 0, 2.3), key='wood', rot=(0, -30, 0), bev=0.02)
    box('back', (0.14, 2.6, 1.4), loc=(-1.95, 0, 2.3), key='wood', rot=(0, 28, 0), bev=0.02)
    for s in (-1, 1):
        tube(f'handle{s}', [(2.4, s * 0.5, 1.0), (0, s * 0.9, 1.45), (-3.6, s * 1.0, 2.2), (-4.3, s * 1.0, 2.4)], 0.13, 'wood_dark', res=4)
        box(f'leg{s}', (0.2, 0.2, 1.4), loc=(-1.3, s * 0.95, 0.7), key='wood_dark')
    wheel('w', 1.0, (2.6, 0, 1.0), axis='Y', spokes=8, w=0.25)
    return finalize('wheelbarrow', smooth_angle=35)


# ----------------------------------------------------------------- A82-A86 furniture
def bench_wood():
    """A82 - wooden park/tavern bench, 8 studs, slatted seat and back on iron frames."""
    reset()
    rnd = random.Random(82)
    for k in range(4):
        box(f'seat{k}', (8.0, 0.55, 0.22), loc=(0, -0.95 + k * 0.62, 1.95), key=rnd.choice(['wood', 'wood_light']), bev=0.05, segs=1)
    for k in range(3):
        box(f'back{k}', (8.0, 0.18, 0.5), loc=(0, 1.2 + k * 0.1, 2.6 + k * 0.62), key=rnd.choice(['wood', 'wood_light']), rot=(-12, 0, 0), bev=0.05, segs=1)
    for x in (-3.3, 0, 3.3):
        tube(f'fr{x}', [(x, -1.1, 0), (x, -0.9, 1.0), (x, -1.0, 1.84)], 0.1, 'iron', res=4)
        tube(f'fb{x}', [(x, 1.1, 0), (x, 1.05, 1.84), (x, 1.35, 3.0), (x, 1.5, 4.0)], 0.1, 'iron', res=4)
        tube(f'fs{x}', [(x, -1.1, 1.84), (x, 1.1, 1.84)], 0.1, 'iron', res=4)
        if abs(x) > 1:
            tube(f'arm{x}', [(x * 1.06, -1.2, 2.9), (x * 1.06, 0.3, 3.0), (x * 1.06, 1.3, 2.95)], 0.1, 'iron', res=4)
            tube(f'armpost{x}', [(x * 1.06, -1.2, 1.84), (x * 1.06, -1.25, 2.9)], 0.09, 'iron', res=4)
            scroll(f'curl{x}', (x * 1.06, -0.4, 2.35), 0.03, 0.3, 1.0, 'YZ', 'iron', 0.06, n=24)
    return finalize('bench_wood', smooth_angle=35)


def bench_stone():
    """A83 - carved stone bench on two scrolled supports."""
    reset()
    box('slab', (8.0, 2.4, 0.6), loc=(0, 0, 1.9), key='stone_light', bev=0.15, segs=2)
    for x in (-2.9, 2.9):
        poly_prism(f'sup{x}', [(-1.1, 0), (1.1, 0), (0.8, 0.5), (0.55, 1.1), (0.75, 1.6), (-0.75, 1.6), (-0.55, 1.1), (-0.8, 0.5)],
                   1.4, loc=(x - 0.7, 0, 0), key='stone', rot=(90, 0, 90))
        bevel(bpy.data.objects[f'sup{x}'], 0.06, 1)
    return finalize('bench_stone', smooth_angle=35)


def table():
    """A84 - rustic plank table, 8 x 4, top at 3.0, turned legs and stretcher."""
    reset()
    rnd = random.Random(84)
    for k in range(4):
        box(f'top{k}', (8.0, 1.0 - 0.04, 0.3), loc=(0, -1.5 + k, 2.85), key=rnd.choice(['wood', 'wood_light']), bev=0.05, segs=1)
    box('apron', (7.2, 3.2, 0.5), loc=(0, 0, 2.45), key='wood_dark')
    for sx in (-1, 1):
        for sy in (-1, 1):
            lathe(f'leg{sx}{sy}', [(0.0, 0), (0.28, 0), (0.22, 0.25), (0.3, 0.5), (0.18, 0.9), (0.2, 1.6), (0.3, 1.9), (0.22, 2.2), (0.26, 2.7), (0.0, 2.7)],
                  loc=(sx * 3.4, sy * 1.4, 0), key='wood_dark', segs=10)
    box('stretch', (6.8, 0.25, 0.25), loc=(0, 0, 0.7), key='wood_dark')
    for sx in (-1, 1):
        box(f'stx{sx}', (0.25, 2.8, 0.25), loc=(sx * 3.4, 0, 0.7), key='wood_dark')
    return finalize('table', smooth_angle=35)


def chair():
    """A85 - ladder-back wooden chair, seat 1.9 high."""
    reset()
    box('seat', (1.9, 1.9, 0.2), loc=(0, 0, 1.9), key='wood', bev=0.05)
    for sx in (-1, 1):
        for sy in (-1, 1):
            h = 1.8 if sy < 0 else 4.4
            lathe(f'leg{sx}{sy}', [(0.0, 0), (0.13, 0), (0.11, h * 0.5), (0.13, h - 0.2), (0.17, h - 0.05), (0.0, h)],
                  loc=(sx * 0.82, sy * 0.82, 0), key='wood_dark', segs=8)
    for k in range(3):
        box(f'rung{k}', (1.6, 0.14, 0.34), loc=(0, 0.82, 2.6 + k * 0.6), key='wood', bev=0.04, segs=1)
    for sy in (-1, 1):
        box(f'str{sy}', (1.6, 0.1, 0.1), loc=(0, sy * 0.82, 0.6), key='wood_dark')
    box('cushion', (1.6, 1.6, 0.18), loc=(0, 0, 2.08), key='fabric_red', bev=0.07, segs=2)
    return finalize('chair', smooth_angle=35)


def stool():
    """A86 - three-legged round stool."""
    reset()
    cyl('seat', 0.95, 0.25, loc=(0, 0, 1.75), key='wood', verts=20, bev=0.06)
    for i in range(3):
        a = 2 * math.pi * i / 3
        tube(f'leg{i}', [(math.cos(a) * 0.55, math.sin(a) * 0.55, 1.75), (math.cos(a) * 0.85, math.sin(a) * 0.85, 0)], 0.1, 'wood_dark', res=4)
    torus('ring', 0.7, 0.06, loc=(0, 0, 0.65), key='wood_dark', segs=18, rsegs=4)
    return finalize('stool', smooth_angle=35)


# ----------------------------------------------------------------- A87-A99 small props
def bucket():
    """A87 - wooden bucket with iron hoops and rope handle."""
    reset()
    staves('b', 1.6, 0.75, 0.68, key='wood', n=12)
    for z in (0.25, 1.4):
        hoop(f'h{z}', 0.72, z, w=0.14, t=0.04)
    torus('rim', 0.7, 0.06, loc=(0, 0, 1.6), key='wood_dark', segs=24, rsegs=4)
    cyl('water', 0.64, 0.03, loc=(0, 0, 1.6), key='water', verts=20)
    tube('handle', [(-0.75, 0, 1.45), (-0.5, 0, 2.2), (0.5, 0, 2.2), (0.75, 0, 1.45)], 0.05, 'rope', res=4)
    return finalize('bucket', smooth_angle=40)


def clay_pot_1():
    """A88 - tall amphora-style clay jar with handles and painted band."""
    reset()
    lathe('pot', [(0.0, 0), (0.55, 0), (0.7, 0.2), (1.05, 0.9), (1.15, 1.6), (0.95, 2.4), (0.5, 2.9), (0.42, 3.3), (0.55, 3.45), (0.5, 3.55), (0.36, 3.5), (0.0, 3.4)],
          key='terracotta', segs=24)
    for z in (1.55, 1.8):
        torus(f'band{z}', 1.14, 0.05, loc=(0, 0, z), key='terracotta_dark', segs=28, rsegs=4)
    for s in (-1, 1):
        tube(f'handle{s}', [(s * 0.45, 0, 3.15), (s * 1.0, 0, 3.1), (s * 1.0, 0, 2.5), (s * 0.8, 0, 2.3)], 0.1, 'terracotta', res=4)
    return finalize('clay_pot_1', smooth_angle=45)


def clay_pot_2():
    """A89 - squat cooking/storage pot with lid."""
    reset()
    lathe('pot', [(0.0, 0), (0.7, 0), (1.1, 0.3), (1.25, 0.8), (1.05, 1.3), (0.9, 1.45), (0.95, 1.55), (0.0, 1.5)], key='terracotta_dark', segs=24)
    lathe('lid', [(0.0, 1.5), (0.92, 1.5), (0.6, 1.75), (0.15, 1.85), (0.2, 2.05), (0.0, 2.1)], key='terracotta', segs=24)
    return finalize('clay_pot_2', smooth_angle=45)


def firewood_stack():
    """A90 - stacked split firewood under a small lean-to roof."""
    reset()
    rnd = random.Random(90)
    for row in range(5):
        for k in range(8 - (row % 2)):
            y = -3.2 + k * 0.9 + (0.45 if row % 2 else 0)
            z = 0.42 + row * 0.78
            o = cyl(f'log{row}_{k}', rnd.uniform(0.36, 0.44), 3.0, loc=(-1.5, y, z), key='bark', verts=rnd.choice([6, 7, 8]),
                    rot=(rnd.uniform(0, 60), 90, rnd.uniform(-2, 2)))
            for ex in (1.52, -1.52):
                cyl(f'end{row}_{k}{ex}', 0.33, 0.04, loc=(ex if ex > 0 else ex - 0.04, y, z), key='wood_light', verts=7, rot=(0, 90, 0))
    for y in (-3.8, 3.8):
        box(f'post{y}', (0.3, 0.3, 4.8), loc=(-1.0, y, 2.4), key='wood_dark')
        box(f'postf{y}', (0.3, 0.3, 4.2), loc=(1.4, y, 2.1), key='wood_dark')
    box('roof', (3.4, 8.4, 0.2), loc=(0.2, 0, 4.6), key='roof_red', rot=(0, 10, 0), bev=0.04)
    return finalize('firewood_stack', smooth_angle=30)


def ladder():
    """A91 - wooden ladder, 12 studs, leaned use."""
    reset()
    for s in (-1, 1):
        box(f'rail{s}', (0.22, 0.22, 12), loc=(s * 0.8, 0, 6), key='wood', bev=0.03)
    for k in range(10):
        cyl(f'r{k}', 0.07, 1.8, loc=(-0.9, 0, 0.8 + k * 1.15), key='wood_dark', verts=8, rot=(0, 90, 0))
    return finalize('ladder', smooth_angle=35)


def laundry_line():
    """A92 - laundry line between two posts with hanging clothes."""
    reset()
    rnd = random.Random(92)
    for x in (-8, 8):
        box(f'post{x}', (0.35, 0.35, 8), loc=(x, 0, 4), key='wood_dark', bev=0.04)
        box(f'cross{x}', (0.25, 2.0, 0.25), loc=(x, 0, 7.6), key='wood_dark')
    for y in (-0.8, 0.8):
        tube(f'line{y}', [(-8, y, 7.55), (0, y, 7.0), (8, y, 7.55)], 0.03, 'rope', res=4)
    items = [(-5.5, 'fabric_cream', 2.0, 2.6), (-2.8, 'fabric_red', 1.6, 2.0), (0.0, 'fabric_blue', 2.2, 3.0), (3.0, 'fabric_cream', 1.4, 1.6), (5.6, 'fabric_green', 1.8, 2.4)]
    for i, (x, k, w, h) in enumerate(items):
        y = -0.8 if i % 2 else 0.8
        ztop = 7.0 + 0.55 * (abs(x) / 8) ** 2 - 0.05
        cloth(f'cl{i}', w, h, (x, y, ztop), k, waves=0.8, amp=0.15, seed=i)
        for px in (-w / 2 + 0.15, w / 2 - 0.15):
            box(f'peg{i}{px}', (0.08, 0.12, 0.3), loc=(x + px, y, ztop + 0.05), key='wood_light')
    return finalize('laundry_line', smooth_angle=40)


def notice_board():
    """A93 - covered notice board with pinned papers (quest board)."""
    reset()
    rnd = random.Random(93)
    for x in (-2.8, 2.8):
        box(f'post{x}', (0.45, 0.45, 8.5), loc=(x, 0, 4.25), key='wood_dark', bev=0.05)
    box('board', (5.4, 0.25, 3.6), loc=(0, 0, 5.0), key='wood', bev=0.04)
    box('frame_t', (5.8, 0.4, 0.3), loc=(0, -0.05, 6.9), key='wood_dark', bev=0.04)
    box('frame_b', (5.8, 0.4, 0.3), loc=(0, -0.05, 3.1), key='wood_dark', bev=0.04)
    poly_prism('roof', [(-3.6, 0), (0, 1.2), (3.6, 0), (3.6, 0.2), (0, 1.4), (-3.6, 0.2)], 1.8, loc=(0, 0.9, 8.3), key='roof_red', rot=(90, 0, 0))
    for i in range(9):
        x = rnd.uniform(-2.2, 2.2); z = rnd.uniform(3.8, 6.3)
        box(f'paper{i}', (rnd.uniform(0.7, 1.1), 0.03, rnd.uniform(0.8, 1.2)), loc=(x, -0.14, z), key=rnd.choice(['paper', 'paper', 'fabric_cream']),
            rot=(0, rnd.uniform(-8, 8), 0))
        ball(f'pin{i}', 0.06, loc=(x, -0.17, z + 0.4), key='fl_red', segs=6, rings=4)
    box('shelf', (5.0, 0.6, 0.12), loc=(0, -0.35, 2.9), key='wood_dark')
    return finalize('notice_board', smooth_angle=35)


def shop_sign():
    """A94 - hanging shop sign on a wall bracket (blank carved board with border)."""
    reset()
    box('wallplate', (0.6, 0.15, 1.2), loc=(0, 0, 4.0), key='iron', bev=0.03)
    tube('arm', [(0, -0.1, 4.3), (0, -2.0, 4.3), (0, -3.6, 4.35)], 0.07, 'iron', res=4)
    tube('brace', [(0, -0.1, 3.5), (0, -1.0, 3.8), (0, -2.0, 4.25)], 0.05, 'iron', res=4)
    scroll('curl', (0, -0.9, 3.95), 0.03, 0.25, 1.0, 'YZ', 'iron', 0.05, n=22)
    for y in (-1.0, -3.2):
        chain(f'ch{y}', (0, y, 4.3), (0, y, 3.55), link=0.16, thick=0.035)
    poly_prism('board', [(-1.3, 0), (1.3, 0), (1.3, 1.6), (0.9, 2.0), (-0.9, 2.0), (-1.3, 1.6)], 0.2, loc=(0, -2.1, 1.6), key='wood_light', rot=(90, 0, 90))
    poly_prism('inner', [(-1.05, 0.2), (1.05, 0.2), (1.05, 1.5), (0.75, 1.8), (-0.75, 1.8), (-1.05, 1.5)], 0.26, loc=(0, -2.1, 1.6), key='fabric_blue', rot=(90, 0, 90))
    return finalize('shop_sign', smooth_angle=35)


def flag_pole():
    """A95 - tall flag pole with stone base, finial and waving pennant banner."""
    reset()
    box('base', (2.4, 2.4, 1.2), loc=(0, 0, 0.6), key='stone_light', bev=0.15)
    cyl('pole', 0.22, 20, loc=(0, 0, 1.2), key='wood_dark', verts=12, r2=0.15)
    ball('finial', 0.32, loc=(0, 0, 21.4), key='gold', segs=12, rings=8)
    cyl('spike', 0.1, 0.8, loc=(0, 0, 21.6), key='gold', verts=8, r2=0.0)
    cloth('flag', 8.0, 5.0, (4.25, 0, 20.8), 'fabric_red', waves=1.2, amp=0.4, seed=1)
    box('hoist', (0.35, 0.3, 5.0), loc=(0.35, 0, 18.3), key='gold')
    for z in (20.6, 16.0):
        torus(f'ring{z}', 0.28, 0.05, loc=(0, 0, z), key='gold', segs=12, rsegs=4)
    return finalize('flag_pole', smooth_angle=40)


def wall_banner():
    """A96 - long wall banner on a rod with tassels and a swallow-tail end."""
    reset()
    cyl('rod', 0.12, 4.4, loc=(-2.2, 0, 10), key='gold', verts=10, rot=(0, 90, 0))
    for s in (-1, 1):
        ball(f'knob{s}', 0.22, loc=(s * 2.3, 0, 10), key='gold', segs=10, rings=6)
    bm = bmesh.new()
    nx, nz = 6, 16
    grid = []
    for j in range(nz + 1):
        row = []
        for i in range(nx + 1):
            u, v = i / nx, j / nz
            x = (u - 0.5) * 3.6
            z = 9.9 - v * 9.0
            if v > 0.85:
                z += abs(u - 0.5) * 2.0 * (v - 0.85) / 0.15 * 1.2 - 0.0
            y = math.sin(v * 5.5) * 0.08
            row.append(bm.verts.new((x, y, z)))
        grid.append(row)
    for j in range(nz):
        for i in range(nx):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    o = _obj_from_bm('cloth', bm, 'fabric_red')
    o.modifiers.new('sol', 'SOLIDIFY').thickness = 0.06
    # emblem: gold diamond and border stripes
    poly_prism('emblem', [(0, -1.0), (0.8, 0), (0, 1.0), (-0.8, 0)], 0.05, loc=(0, -0.08, 6.5), key='gold', rot=(90, 0, 0))
    for s in (-1, 1):
        box(f'border{s}', (0.18, 0.04, 8.0), loc=(s * 1.6, -0.08, 5.6), key='gold')
    for s in (-1, 1):
        tube(f'tassel{s}', [(s * 1.8, 0, 9.9), (s * 1.85, 0, 8.6)], 0.05, 'gold', res=4)
        cyl(f'tas{s}', 0.12, 0.6, loc=(s * 1.85, 0, 8.0), key='gold', verts=8, r2=0.2)
    return finalize('wall_banner', smooth_angle=40)


def water_trough():
    """A97 - stone water trough with water and an iron hand pump."""
    reset()
    L, Wd, H = 7.0, 2.6, 2.0
    rnd = random.Random(97)
    for s in (-1, 1):
        box(f'wl{s}', (L, 0.45, 1.5), loc=(0, s * (Wd / 2 - 0.22), 1.25), key='stone', bev=0.12, segs=2)
        box(f'we{s}', (0.45, Wd - 0.9, 1.5), loc=(s * (L / 2 - 0.22), 0, 1.25), key='stone', bev=0.12, segs=2)
        for x in (-L / 2 + 0.7, L / 2 - 0.7):
            box(f'foot{s}{x}', (0.9, 0.9, 0.55), loc=(x, s * (Wd / 2 - 0.5), 0.27), key='stone_dark', bev=0.1)
    box('floor', (L - 0.8, Wd - 0.8, 0.3), loc=(0, 0, 0.65), key='stone_dark')
    box('water', (L - 0.85, Wd - 0.85, 0.05), loc=(0, 0, 1.75), key='water')
    for s in (-1, 1):
        box(f'rimL{s}', (L + 0.1, 0.55, 0.22), loc=(0, s * (Wd / 2 - 0.22), 2.06), key='stone_light', bev=0.08)
        box(f'rimE{s}', (0.55, Wd - 0.9, 0.22), loc=(s * (L / 2 - 0.22), 0, 2.06), key='stone_light', bev=0.08)
    lathe('pump', [(0.0, 0), (0.4, 0), (0.32, 0.2), (0.28, 3.8), (0.36, 4.0), (0.25, 4.3), (0.0, 4.4)], loc=(L / 2 + 0.6, 0, 0), key='iron', segs=12)
    tube('spout', [(L / 2 + 0.6, 0, 3.4), (L / 2 - 0.2, 0, 3.35), (L / 2 - 0.6, 0, 3.0)], 0.12, 'iron', res=4)
    tube('lever', [(L / 2 + 0.6, 0, 4.2), (L / 2 + 1.4, 0, 4.7), (L / 2 + 2.5, 0, 4.4)], 0.07, 'iron', res=4)
    return finalize('water_trough', smooth_angle=35)


def well():
    """A98 - stone village well with timber roof, windlass, rope and bucket."""
    reset()
    rnd = random.Random(98)
    R = 3.0
    # stone ring: courses of blocks
    for c in range(4):
        n = 14
        for i in range(n):
            a = 2 * math.pi * (i + (0.5 if c % 2 else 0)) / n
            box(f'st{c}_{i}', (1.32, 0.9, 0.62), loc=(math.cos(a) * R, math.sin(a) * R, 0.31 + c * 0.64),
                key=rnd.choice(['stone', 'stone_light', 'cob_a']), rot=(0, 0, math.degrees(a) + 90), bev=0.12, segs=1)
    lathe('cap', [(R - 0.6, 2.6), (R + 0.6, 2.6), (R + 0.65, 2.8), (R + 0.55, 2.95), (R - 0.55, 2.95), (R - 0.6, 2.6)], key='stone_light', segs=28)
    cyl('dark', R - 0.5, 0.05, loc=(0, 0, 1.0), key='water_dark', verts=24)
    for s in (-1, 1):
        box(f'post{s}', (0.5, 0.5, 6.5), loc=(s * (R - 0.1), 0, 5.2), key='wood_dark', bev=0.05)
    box('beam', (2 * R + 0.8, 0.4, 0.4), loc=(0, 0, 8.3), key='wood_dark')
    cyl('windlass', 0.42, 2 * R - 0.8, loc=(-(R - 0.4), 0, 6.0), key='wood', verts=12, rot=(0, 90, 0))
    torus('rope_coil', 0.45, 0.1, loc=(0, 0, 6.0), key='rope', segs=14, rsegs=4, rot=(0, 90, 0))
    tube('crank', [(R + 0.1, 0, 6.0), (R + 0.6, 0, 6.0), (R + 0.6, 0, 6.9), (R + 1.1, 0, 6.9)], 0.07, 'iron', res=4)
    tube('rope', [(0, -0.4, 6.0), (0, -0.45, 4.4)], 0.05, 'rope', res=4)
    staves('bkt', 1.1, 0.5, 0.45, loc=(0, -0.45, 3.3), key='wood', n=10)
    hoop('bkth', 0.48, 3.9, loc=(0, -0.45, 0))
    for s in (-1, 1):
        o = box(f'roof{s}', (2 * R + 2.4, 2.8, 0.25), loc=(0, s * 1.15, 9.0), key='roof_red', rot=(s * -32, 0, 0), bev=0.05)
    for k in range(7):
        x = -R - 1.0 + k * (2 * R + 2) / 6
        for s in (-1, 1):
            box(f'shing{k}{s}', (0.06, 2.8, 0.12), loc=(x, s * 1.15, 9.15), key='roof_dark', rot=(s * -32, 0, 0))
    return finalize('well', smooth_angle=35)


def anvil():
    """A99 - blacksmith anvil on a banded stump, with hammer and tongs."""
    reset()
    lathe('stump', [(0.0, 0), (1.3, 0), (1.15, 0.3), (1.1, 2.0), (0.0, 2.0)], key='wood_dark', segs=14)
    for z in (0.6, 1.6):
        hoop(f'band{z}', 1.12, z)
    box('waist', (1.4, 1.0, 0.9), loc=(0, 0, 2.5), key='iron_dark', bev=0.1)
    box('foot', (2.2, 1.5, 0.45), loc=(0, 0, 2.2), key='iron_dark', bev=0.12)
    box('face', (2.6, 1.3, 0.7), loc=(-0.2, 0, 3.3), key='steel', bev=0.08)
    cyl('horn', 0.48, 2.0, loc=(1.05, 0, 3.4), key='steel', verts=12, r2=0.06, rot=(0, 90, 0))
    box('heel', (0.8, 1.0, 0.5), loc=(-1.75, 0, 3.4), key='steel', bev=0.06)
    box('hammer_head', (0.9, 0.4, 0.4), loc=(-0.4, 0.2, 3.85), key='iron_dark', bev=0.04)
    box('hammer_handle', (0.18, 2.0, 0.18), loc=(-0.4, 1.3, 3.8), key='wood', rot=(0, 0, 8))
    tube('tong1', [(0.6, -0.4, 3.7), (1.2, -1.2, 3.72), (2.4, -1.4, 3.7)], 0.05, 'iron_dark', res=4)
    tube('tong2', [(0.6, -0.25, 3.7), (1.2, -1.0, 3.72), (2.4, -1.15, 3.7)], 0.05, 'iron_dark', res=4)
    return finalize('anvil', smooth_angle=35)


# ----------------------------------------------------------------- A100-A104 fences & walls
def fence_picket():
    """A100 - white-painted picket fence section, 12 long, with posts."""
    reset()
    for x in (-6, 6):
        box(f'post{x}', (0.5, 0.5, 4.2), loc=(x, 0, 2.1), key='wood_paint', bev=0.05)
        cyl(f'cap{x}', 0.35, 0.4, loc=(x, 0, 4.2), key='wood_paint', verts=4, r2=0.02, rot=(0, 0, 45))
    for z in (1.0, 2.8):
        box(f'rail{z}', (12, 0.18, 0.35), loc=(0, 0.2, z), key='wood_paint', bev=0.03)
    for k in range(17):
        x = -5.4 + k * 0.675
        poly_prism(f'pk{k}', [(-0.25, 0), (0.25, 0), (0.25, 3.2), (0, 3.6), (-0.25, 3.2)], 0.12, loc=(x, 0.36, 0.2), key='wood_paint', rot=(90, 0, 0))
    return finalize('fence_picket', smooth_angle=35)


def fence_rail():
    """A101 - split-rail (zig-zag style) farm fence, 12 long."""
    reset()
    rnd = random.Random(101)
    for x in (-6, 0, 6):
        box(f'post{x}', (0.55, 0.55, 4.0), loc=(x, 0, 2.0), key='wood_dark', rot=(0, 0, rnd.uniform(-8, 8)), bev=0.08)
    for z in (1.2, 2.3, 3.4):
        for s in (-1, 1):
            tube(f'rail{z}{s}', [(s * 6.2, 0, z + rnd.uniform(-0.1, 0.1)), (s * 3, 0.1, z + rnd.uniform(-0.15, 0.1)), (0, 0, z)], rnd.uniform(0.2, 0.26),
                 rnd.choice(['wood', 'bark']), res=4, ures=2)
    return finalize('fence_rail', smooth_angle=40)


def stone_wall_low():
    """A102 - dry-stone low wall section, 12 long x 3.4 tall, with coping stones."""
    reset()
    rnd = random.Random(102)
    z = 0
    for c in range(4):
        x = -6.0 - (0.5 if c % 2 else 0)
        h = rnd.uniform(0.7, 0.85)
        while x < 6:
            L = rnd.uniform(1.1, 2.0)
            a, b = max(x, -6), min(x + L, 6)
            if b - a > 0.3:
                box(f'st{c}_{x:.1f}', (b - a - 0.08, rnd.uniform(1.6, 1.9), h - 0.06), loc=((a + b) / 2, rnd.uniform(-0.08, 0.08), z + h / 2),
                    key=rnd.choice(['stone', 'cob_a', 'cob_b', 'stone_light']), rot=(rnd.uniform(-2, 2), rnd.uniform(-2, 2), rnd.uniform(-2, 2)), bev=0.14, segs=1)
            x += L
        z += h
    x = -6.0
    while x < 6:
        L = rnd.uniform(0.6, 0.9)
        box(f'cope{x:.1f}', (L - 0.05, 2.0, 0.5), loc=(x + L / 2, 0, z + 0.25), key='stone_light', rot=(rnd.uniform(-6, 6), 0, 0), bev=0.12, segs=1)
        x += L
    for i in range(6):
        blob(f'moss{i}', rnd.uniform(0.3, 0.55), (rnd.uniform(-5.5, 5.5), rnd.choice((-1, 1)) * 0.95, rnd.uniform(0.3, z)), 'moss',
             subdiv=2, amp=0.25, scale=(1.4, 0.25, 0.9), seed=i)
    return finalize('stone_wall_low', smooth_angle=30)


def fence_iron():
    """A103 - wrought iron railing, 12 long, spear-top bars and stone plinth."""
    reset()
    box('plinth', (12.4, 1.2, 1.2), loc=(0, 0, 0.6), key='stone_light', bev=0.12)
    for x in (-6, 6):
        box(f'pier{x}', (1.6, 1.6, 5.2), loc=(x, 0, 2.6), key='stone_light', bev=0.15)
        cyl(f'piercap{x}', 1.1, 0.7, loc=(x, 0, 5.2), key='stone_light', verts=4, r2=0.3, rot=(0, 0, 45))
        ball(f'pierball{x}', 0.45, loc=(x, 0, 6.2), key='stone_light', segs=12, rings=8)
    for z in (1.6, 4.0):
        box(f'rail{z}', (10.6, 0.14, 0.14), loc=(0, 0, z), key='iron')
    for k in range(21):
        x = -5.0 + k * 0.5
        cyl(f'bar{k}', 0.06, 3.6, loc=(x, 0, 1.2), key='iron', verts=6)
        cyl(f'tip{k}', 0.14, 0.4, loc=(x, 0, 4.8), key='iron', verts=4, r2=0.0)
        if k % 4 == 2:
            scroll(f'sc{k}', (x + 0.25, 0, 2.6), 0.02, 0.25, 1.0, 'XZ', 'iron', 0.04, n=20)
    return finalize('fence_iron', smooth_angle=35)


def wooden_gate():
    """A104 - double wooden farm gate between two posts, Z-braced, iron hinges and latch."""
    reset()
    rnd = random.Random(104)
    for x in (-5.2, 5.2):
        box(f'post{x}', (0.8, 0.8, 6.0), loc=(x, 0, 3.0), key='wood_dark', bev=0.08)
        cyl(f'pcap{x}', 0.55, 0.5, loc=(x, 0, 6.0), key='wood_dark', verts=4, r2=0.05, rot=(0, 0, 45))
    for s in (-1, 1):
        cx = s * 2.4
        for k in range(5):
            box(f'pl{s}{k}', (0.85, 0.16, 4.2), loc=(cx - 1.8 + k * 0.9, 0, 2.6), key=rnd.choice(['wood', 'wood_light']), bev=0.03, segs=1)
        for z in (1.1, 4.1):
            box(f'rail{s}{z}', (4.6, 0.2, 0.45), loc=(cx, -0.18, z), key='wood_dark', bev=0.03)
        L = math.hypot(4.2, 3.0)
        box(f'brace{s}', (L, 0.2, 0.4), loc=(cx, -0.18, 2.6), key='wood_dark', rot=(0, s * math.degrees(math.atan2(3.0, 4.2)), 0), bev=0.03)
        for z in (1.1, 4.1):
            box(f'hinge{s}{z}', (1.4, 0.06, 0.2), loc=(s * 4.1, -0.3, z), key='iron')
    box('latch', (0.8, 0.1, 0.18), loc=(0, -0.32, 2.8), key='iron')
    return finalize('wooden_gate', smooth_angle=35)


# ----------------------------------------------------------------- A105-A108 market
def _stall(seed, name, canopy_key, stripe_key, goods):
    reset()
    rnd = random.Random(seed)
    L, D = 10.0, 5.0
    # counter
    box('counter', (L, 2.2, 0.3), loc=(0, -1.0, 3.2), key='wood_light', bev=0.05)
    for k in range(5):
        box(f'front{k}', (L / 5 - 0.06, 0.16, 3.0), loc=(-L / 2 + L / 5 * (k + 0.5), -2.05, 1.55), key=rnd.choice(['wood', 'wood_light']), bev=0.03, segs=1)
    box('back_table', (L, 1.6, 0.25), loc=(0, 1.6, 2.2), key='wood')
    for x in (-L / 2 + 0.2, L / 2 - 0.2):
        for y in (-2.1, 2.2):
            box(f'post{x}{y}', (0.35, 0.35, 8.0 if y < 0 else 7.2), loc=(x, y, (8.0 if y < 0 else 7.2) / 2), key='wood_dark', bev=0.04)
    # striped canopy: alternating cloth strips sloping back
    n = 8
    for i in range(n):
        x = -L / 2 + L / n * (i + 0.5)
        k = canopy_key if i % 2 == 0 else stripe_key
        o = box(f'can{i}', (L / n + 0.02, 5.4, 0.08), loc=(x, 0.05, 7.6), key=k, rot=(-9, 0, 0))
        # scalloped valance at the front
        cloth(f'val{i}', L / n, 0.9, (x, -2.6, 7.95), k, waves=0.5, amp=0.04, seed=i, res=(4, 3))
    # goods
    for i in range(goods['count']):
        x = rnd.uniform(-L / 2 + 0.8, L / 2 - 0.8)
        goods['fn'](f'g{i}', x, rnd.uniform(-1.8, -0.2), 3.35, rnd)
    for i in range(3):
        plank_box(f'cr{i}', (2.0, 2.0, 1.6), loc=(-L / 2 + 1.6 + i * 3.4, 1.6, 2.35), rnd=rnd, planks=2)
        for j in range(5):
            goods['fn'](f'cg{i}{j}', -L / 2 + 1.6 + i * 3.4 + rnd.uniform(-0.6, 0.6), 1.6 + rnd.uniform(-0.6, 0.6), 3.95, rnd)
    plank_box('side', (2.2, 2.2, 2.2), loc=(L / 2 + 1.6, -1.2, 0), rnd=rnd, planks=2)
    barrel_body('sb', loc=(-L / 2 - 1.6, -1.2, 0), h=3.4)
    return finalize(name, smooth_angle=35)


def _fruit(nm, x, y, z, rnd):
    k = rnd.choice(['fruit', 'fl_yellow', 'leaf_light', 'fl_orange', 'fruit'])
    ball(nm, rnd.uniform(0.25, 0.35), loc=(x, y, z + 0.25), key=k, segs=8, rings=6)


def _cloth_roll(nm, x, y, z, rnd):
    o = cyl(nm, 0.3, 1.6, loc=(x - 0.8, y, z + 0.3), key=rnd.choice(['fabric_red', 'fabric_blue', 'fabric_green', 'fabric_cream', 'fl_purple']),
            verts=10, rot=(0, 90, rnd.uniform(-20, 20)))


def _potion(nm, x, y, z, rnd):
    k = rnd.choice(['potion_red', 'potion_blue', 'potion_green', 'fl_purple'])
    lathe(nm, [(0.0, 0), (0.22, 0), (0.28, 0.25), (0.22, 0.55), (0.08, 0.65), (0.08, 0.85), (0.11, 0.9), (0.0, 0.92)], loc=(x, y, z), key=k, segs=10)
    cyl(nm + 'c', 0.07, 0.15, loc=(x, y, z + 0.9), key='wood_light', verts=6)


def market_stall_fruit():
    """A105 - fruit and veg stall, red/cream canopy."""
    return _stall(105, 'market_stall_fruit', 'fabric_red', 'fabric_cream', {'count': 40, 'fn': _fruit})


def market_stall_cloth():
    """A106 - cloth merchant stall, blue/cream canopy, fabric rolls."""
    return _stall(106, 'market_stall_cloth', 'fabric_blue', 'fabric_cream', {'count': 14, 'fn': _cloth_roll})


def market_stall_potion():
    """A107 - potion/magic stall, green/gold canopy, glass bottles."""
    return _stall(107, 'market_stall_potion', 'fabric_green', 'gold', {'count': 26, 'fn': _potion})


def awning():
    """A108 - wall-mounted striped cloth awning on iron brackets, 10 wide (for shopfronts)."""
    reset()
    L = 10.0
    n = 10
    for i in range(n):
        x = -L / 2 + L / n * (i + 0.5)
        k = 'fabric_red' if i % 2 == 0 else 'fabric_cream'
        bm = bmesh.new()
        rows = []
        for j in range(7):
            t = j / 6
            y = -t * 3.6
            z = 8.0 - t * 1.8 - math.sin(t * math.pi) * 0.25
            rows.append([bm.verts.new((x - L / n / 2, y, z)), bm.verts.new((x + L / n / 2, y, z))])
        for a, b in zip(rows, rows[1:]):
            bm.faces.new((a[0], a[1], b[1], b[0]))
        o = _obj_from_bm(f'strip{i}', bm, k)
        o.modifiers.new('sol', 'SOLIDIFY').thickness = 0.06
        cloth(f'val{i}', L / n, 0.8, (x, -3.6, 6.2), k, waves=0.5, amp=0.03, seed=i, res=(4, 3))
    box('rod', (L + 0.4, 0.2, 0.2), loc=(0, 0, 8.05), key='iron')
    box('frontrod', (L + 0.2, 0.12, 0.12), loc=(0, -3.6, 6.2), key='iron')
    for x in (-L / 2 + 0.2, 0, L / 2 - 0.2):
        tube(f'br{x}', [(x, 0, 6.2), (x, -1.8, 6.1), (x, -3.6, 6.2)], 0.06, 'iron', res=4)
        scroll(f'sc{x}', (x, -0.8, 6.7), 0.02, 0.35, 1.0, 'YZ', 'iron', 0.05, n=24)
    return finalize('awning', smooth_angle=35)


# ----------------------------------------------------------------- A109-A111 water
def fountain_small():
    """A109 - small village fountain: octagonal basin, column, bowl and water spill."""
    reset()
    lathe('basin', [(0.0, 0), (4.0, 0), (4.0, 0.3), (3.8, 0.4), (3.8, 1.6), (4.1, 1.75), (4.1, 2.0), (3.5, 2.0), (3.5, 0.5), (0.0, 0.5)],
          key='stone_light', segs=8)
    cyl('pool', 3.5, 0.05, loc=(0, 0, 1.55), key='water', verts=8, rot=(0, 0, 22.5))
    lathe('column', [(0.0, 0.5), (0.9, 0.5), (0.7, 0.9), (0.55, 1.5), (0.5, 3.2), (0.65, 3.5), (0.0, 3.5)], key='stone', segs=12)
    lathe('bowl', [(0.0, 3.4), (0.6, 3.4), (1.5, 3.7), (1.9, 4.2), (1.95, 4.35), (1.7, 4.35), (1.4, 4.05), (0.0, 3.9)], key='stone_light', segs=20)
    cyl('bowlwater', 1.65, 0.05, loc=(0, 0, 4.2), key='water', verts=20)
    lathe('spout', [(0.0, 4.0), (0.3, 4.0), (0.25, 4.9), (0.38, 5.1), (0.15, 5.4), (0.0, 5.5)], key='stone', segs=12)
    # water: central jet + spill curtain from bowl rim
    lathe('jet', [(0.0, 5.4), (0.12, 5.45), (0.18, 6.2), (0.05, 6.6), (0.0, 6.6)], key='water_fx', segs=8)
    for i in range(8):
        a = i * math.pi / 4 + math.pi / 8
        pts = [(math.cos(a) * r, math.sin(a) * r, z) for r, z in ((1.9, 4.3), (2.1, 3.9), (2.35, 3.0), (2.55, 1.6))]
        tube(f'stream{i}', pts, 0.09, 'water_fx', res=6, taper=[1.0, 0.7])
        lathe(f'ripple{i}', [(0.0, 1.57), (0.35, 1.57), (0.35, 1.6), (0.0, 1.6)], loc=(math.cos(a) * 2.55, math.sin(a) * 2.55, 0), key='foam', segs=10)
    lathe('jetripple', [(0.0, 4.22), (0.5, 4.22), (0.5, 4.25), (0.0, 4.25)], key='foam', segs=14)
    return finalize('fountain_small', smooth_angle=40)


def waterfall_rocks():
    """A110 - waterfall rock set: two cliff shoulders, a lip, the falling sheet and a splash pool rim."""
    reset()
    rnd = random.Random(110)
    from nature import rock
    for s in (-1, 1):
        for k in range(4):
            rock(f'sh{s}{k}', rnd.uniform(3.0, 4.0), (s * rnd.uniform(5.0, 6.5), rnd.uniform(-1, 1), 2.5 + k * 4.0), rnd.choice(['cliff_a', 'cliff_b']),
                 seed=110 + k + s * 10, scale=(1.0, 1.0, 1.1), subdiv=3, amp=0.3)
    for k in range(3):
        rock(f'lip{k}', 2.6, (-2.2 + k * 2.2, 1.5, 15.5), 'cliff_b', seed=130 + k, scale=(1.0, 1.2, 0.6), subdiv=3)
    # falling water sheet (curved)
    bm = bmesh.new()
    rows = []
    for j in range(10):
        t = j / 9
        z = 15.8 - t * 15.3
        y = -1.0 - math.sin(t * math.pi * 0.5) * 2.2
        rows.append([bm.verts.new((x, y + rnd.uniform(-0.1, 0.1), z)) for x in (-3.6, -1.8, 0, 1.8, 3.6)])
    for a, b in zip(rows, rows[1:]):
        for i in range(4):
            bm.faces.new((a[i], a[i + 1], b[i + 1], b[i]))
    o = _obj_from_bm('sheet', bm, 'water_fx')
    o.modifiers.new('sol', 'SOLIDIFY').thickness = 0.3
    # splash foam + pool rim stones
    for i in range(8):
        blob(f'foam{i}', rnd.uniform(0.7, 1.2), (rnd.uniform(-3.5, 3.5), rnd.uniform(-4.5, -2.5), 0.3), 'foam', subdiv=2, amp=0.3,
             scale=(1.3, 1.0, 0.5), seed=i)
    for i in range(12):
        a = math.pi + math.pi * i / 11
        rock(f'rim{i}', rnd.uniform(1.0, 1.6), (math.cos(a) * 8.0, -3.5 + math.sin(a) * 5.0, 0.3), rnd.choice(['stone', 'stone_dark']),
             seed=150 + i, subdiv=3)
    return finalize('waterfall_rocks', smooth_angle=12)


def pond_edge():
    """A111 - pond edge set: arc of mossy stones, reeds and a lily pad cluster (water itself = terrain water)."""
    reset()
    rnd = random.Random(111)
    from nature import rock
    from roads import tuft
    for i in range(16):
        a = math.pi * 0.1 + math.pi * 0.8 * i / 15
        o = rock(f'st{i}', rnd.uniform(0.9, 1.6), (math.cos(a) * 10, math.sin(a) * 6, 0.2), rnd.choice(['stone', 'stone_light', 'stone_dark']),
                 seed=200 + i, subdiv=3, scale=(1.3, 1.0, 0.55))
        top_paint(o, 'moss', 0.75, i)
    for i in range(30):
        a = math.pi * 0.1 + math.pi * 0.8 * rnd.random()
        tuft(f'tf{i}', math.cos(a) * rnd.uniform(10.5, 12), math.sin(a) * rnd.uniform(6.5, 7.5), 0.0, rnd)
    for i in range(14):
        a = rnd.uniform(0.3, 0.7) * math.pi
        x, y = math.cos(a) * 9.0, math.sin(a) * 5.0
        h = rnd.uniform(3, 5)
        tube(f'reed{i}', [(x, y, 0), (x + rnd.uniform(-0.3, 0.3), y, h)], 0.05, rnd.choice(['leaf', 'leaf_dark']), res=4, taper=[1, 0.2])
        if i % 3 == 0:
            cyl(f'cat{i}', 0.15, 0.8, loc=(x, y, h * 0.8), key='wood_dark', verts=8)
    bank = cyl('bank', 10.6, 0.12, loc=(0, 0, 0.0), key='dirt', verts=32)
    bank.scale = (1.0, 0.62, 1.0)
    water = cyl('water', 9.8, 0.06, loc=(0, 0, 0.1), key='water', verts=32)
    water.scale = (1.0, 0.6, 1.0)
    for i in range(6):
        r = rnd.uniform(0.7, 1.1)
        cyl(f'pad{i}', r, 0.05, loc=(rnd.uniform(-3, 3), rnd.uniform(1, 3), 0.16), key='leaf', verts=14)
        if i % 2 == 0:
            ball(f'bloom{i}', 0.22, loc=(rnd.uniform(-3, 3), rnd.uniform(1, 3), 0.3), key='fl_pink')
    return finalize('pond_edge', smooth_angle=30)


ITEMS_A = [
    ('A71_barrel', barrel), ('A72_barrel_open', barrel_open), ('A73_crate_small', crate_small), ('A74_crate_large', crate_large),
    ('A75_crate_stack', crate_stack), ('A76_sack', sack), ('A77_sack_pile', sack_pile), ('A78_hay_bale', hay_bale),
    ('A79_hand_cart', hand_cart), ('A80_wagon', wagon), ('A81_wheelbarrow', wheelbarrow), ('A82_bench_wood', bench_wood),
    ('A83_bench_stone', bench_stone), ('A84_table', table), ('A85_chair', chair), ('A86_stool', stool),
]
ITEMS_B = [
    ('A87_bucket', bucket), ('A88_clay_pot_1', clay_pot_1), ('A89_clay_pot_2', clay_pot_2), ('A90_firewood_stack', firewood_stack),
    ('A91_ladder', ladder), ('A92_laundry_line', laundry_line), ('A93_notice_board', notice_board), ('A94_shop_sign', shop_sign),
    ('A95_flag_pole', flag_pole), ('A96_wall_banner', wall_banner), ('A97_water_trough', water_trough), ('A98_well', well),
    ('A99_anvil', anvil),
]
ITEMS_C = [
    ('A100_fence_picket', fence_picket), ('A101_fence_rail', fence_rail), ('A102_stone_wall_low', stone_wall_low),
    ('A103_fence_iron', fence_iron), ('A104_wooden_gate', wooden_gate), ('A105_market_stall_fruit', market_stall_fruit),
    ('A106_market_stall_cloth', market_stall_cloth), ('A107_market_stall_potion', market_stall_potion), ('A108_awning', awning),
    ('A109_fountain_small', fountain_small), ('A110_waterfall_rocks', waterfall_rocks), ('A111_pond_edge', pond_edge),
]
ITEMS = ITEMS_A + ITEMS_B + ITEMS_C
