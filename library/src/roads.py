# roads.py - shared-kit roads, paths, stairs, bridges, signs (A1-A14).
# Road tiles are modular: 24 studs wide, 24 long, top surface at z = 0.6.
import math, random
import bmesh
from mathutils import Vector
from kitlib import *
from kitlib import _obj_from_bm

W = 24.0
TOP = 0.6
STONE_KEYS = ['cob_a', 'cob_a', 'cob_b', 'cob_c', 'cob_d']


def cobble(name, x, y, l, w, rnd, rot=0.0, key=None, h=None):
    """One cobblestone: bevelled box with jittered height/rotation, sits so its top ~ TOP."""
    hh = h if h else rnd.uniform(0.45, 0.6)
    k = key or rnd.choice(STONE_KEYS)
    o = box(name, (l * rnd.uniform(0.86, 0.94), w * rnd.uniform(0.84, 0.92), hh),
            loc=(x, y, TOP - hh / 2 + rnd.uniform(-0.04, 0.05)), key=k,
            rot=(rnd.uniform(-1.5, 1.5), rnd.uniform(-1.5, 1.5), rot + rnd.uniform(-3, 3)), bev=0.14, segs=1)
    return o


def grout_slab(name, pts2d, z0=0.0, z1=None, key='grout'):
    return poly_prism(name, pts2d, (z1 if z1 is not None else TOP - 0.2) - z0, loc=(0, 0, z0), key=key)


def road_straight():
    """A1 - straight cobblestone road tile, 24 x 24, running-bond courses across the road."""
    reset()
    rnd = random.Random(101)
    grout_slab('slab', [(-W / 2, -W / 2), (W / 2, -W / 2), (W / 2, W / 2), (-W / 2, W / 2)])
    rows = 14
    rl = W / rows
    for r in range(rows):
        y = -W / 2 + rl * (r + 0.5)
        off = (r % 2) * 0.5
        x = -W / 2 - off * 1.9
        while x < W / 2:
            L = rnd.uniform(1.6, 2.2)
            a, b = max(x, -W / 2), min(x + L, W / 2)
            if b - a > 0.5:
                cobble(f's{r}_{x:.1f}', (a + b) / 2, y, b - a, rl, rnd)
            x += L
    return finalize('road_straight')


def _arc_course(prefix, cx, cy, r_in, r_out, a0, a1, rnd, ring_w=1.7):
    """Lay stones in concentric rings between r_in and r_out over angle a0..a1 (degrees)."""
    rings = max(1, int((r_out - r_in) / ring_w))
    rw = (r_out - r_in) / rings
    for i in range(rings):
        r = r_in + rw * (i + 0.5)
        arc = math.radians(a1 - a0) * r
        n = max(1, int(arc / 1.9))
        da = (a1 - a0) / n
        start = a0 + (da * 0.5 if i % 2 else 0)
        for j in range(n + (1 if i % 2 else 0)):
            aa = start + da * j
            lo, hi = max(aa, a0), min(aa + da, a1)
            if hi - lo < da * 0.3:
                continue
            am = math.radians((lo + hi) / 2)
            L = math.radians(hi - lo) * r
            cobble(f'{prefix}{i}_{j}', cx + math.cos(am) * r, cy + math.sin(am) * r, rw, L, rnd,
                   rot=math.degrees(am))


def road_curve():
    """A2 - 90 degree curve; road centreline radius 18, inner edge r=6, outer r=30.
    Connects the -Y edge (x 6..30) to the -X edge... origin at curve centre corner."""
    reset()
    rnd = random.Random(202)
    pts = [(math.cos(math.radians(a)) * 30, math.sin(math.radians(a)) * 30) for a in range(0, 91, 6)]
    pts += [(math.cos(math.radians(a)) * 6, math.sin(math.radians(a)) * 6) for a in range(90, -1, -6)]
    grout_slab('slab', pts)
    _arc_course('c', 0, 0, 6, 30, 0, 90, rnd)
    return finalize('road_curve')


def road_tjunction():
    """A3 - T junction 24x24: fan-laid stones (segmental arcs) facing the side road, curb on the closed side."""
    reset()
    rnd = random.Random(303)
    grout_slab('slab', [(-W / 2, -W / 2), (W / 2, -W / 2), (W / 2, W / 2), (-W / 2, W / 2)])
    # fan arcs centred below the tile so arcs bow toward +Y (the stem side)
    cx, cy = 0, -W / 2 - 6
    for i in range(12):
        r = 6 + 1.75 * (i + 0.5) + 0.6
        if r - 6 > W + 6:
            break
        span = 70
        n = max(3, int(math.radians(span * 2) * r / 1.9))
        for j in range(n):
            a = 90 - span + (2 * span) * (j + 0.5 + (0.5 if i % 2 else 0)) / n
            x = cx + math.cos(math.radians(a)) * r
            y = cy + math.sin(math.radians(a)) * r
            if abs(x) > W / 2 - 0.6 or y > W / 2 - 0.6 or y < -W / 2 + 0.6:
                continue
            cobble(f'f{i}_{j}', x, y, 1.65, 1.85, rnd, rot=a)
    # straight band of setts along the closed side (-Y) as a kerb edge
    for k in range(12):
        x = -W / 2 + 1 + k * 2
        box(f'kerb{k}', (1.9, 0.9, 0.9), loc=(x, -W / 2 + 0.45, TOP + 0.15), key='stone_light',
            rot=(0, 0, rnd.uniform(-2, 2)), bev=0.18, segs=2)
    return finalize('road_tjunction')


def road_crossroads():
    """A4 - crossroads 24x24: concentric circular paving with a carved central medallion."""
    reset()
    rnd = random.Random(404)
    grout_slab('slab', [(-W / 2, -W / 2), (W / 2, -W / 2), (W / 2, W / 2), (-W / 2, W / 2)])
    # medallion
    lathe('med', [(0.0, 0.0), (2.4, 0.0), (2.4, TOP + 0.02), (2.2, TOP + 0.1), (0.0, TOP + 0.1)], key='stone_light', segs=24)
    torus('medring', 2.25, 0.12, loc=(0, 0, TOP + 0.08), key='stone_dark', segs=28, rsegs=5)
    for i in range(8):
        a = math.radians(i * 45)
        box(f'ray{i}', (1.6, 0.22, 0.1), loc=(math.cos(a) * 1.15, math.sin(a) * 1.15, TOP + 0.12),
            key='stone_dark', rot=(0, 0, i * 45), bev=0.04, segs=1)
    # rings out to the corners (clip to square)
    for i in range(10):
        r = 2.6 + 1.75 * (i + 0.5)
        n = max(6, int(2 * math.pi * r / 1.9))
        for j in range(n):
            a = 360.0 * (j + (0.5 if i % 2 else 0)) / n
            x, y = math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r
            if abs(x) > W / 2 - 0.7 or abs(y) > W / 2 - 0.7:
                continue
            cobble(f'r{i}_{j}', x, y, 1.65, 2 * math.pi * r / n, rnd, rot=a)
    return finalize('road_crossroads')


def road_end_fade():
    """A5 - road end that breaks up into grass: stones thin out and sink toward +Y."""
    reset()
    rnd = random.Random(505)
    # slab only under the first half
    grout_slab('slab', [(-W / 2, -W / 2), (W / 2, -W / 2), (W / 2, 1), (-W / 2, 1)])
    rows = 14
    rl = W / rows
    for r in range(rows):
        y = -W / 2 + rl * (r + 0.5)
        t = (y + W / 2) / W  # 0..1 along tile
        keep = 1.0 if t < 0.4 else max(0.0, 1.0 - (t - 0.4) / 0.6 * 1.15)
        edge = W / 2 - (0 if t < 0.4 else (t - 0.4) * 9.0)  # road narrows/ragged edge
        x = -W / 2 - (r % 2) * 0.95
        while x < W / 2:
            L = rnd.uniform(1.6, 2.2)
            cxs = x + L / 2
            if abs(cxs) < edge + rnd.uniform(-1.5, 1.0) and rnd.random() < keep:
                o = cobble(f's{r}_{x:.1f}', cxs, y, L, rl, rnd)
                o.location.z -= (t > 0.45) * rnd.uniform(0.0, 0.35) * t  # stones sinking
            x += L
    # dirt + grass patches between and beyond the stones
    for i in range(18):
        x = rnd.uniform(-W / 2 + 1, W / 2 - 1); y = rnd.uniform(-1, W / 2 - 1)
        ball(f'dirt{i}', rnd.uniform(1.0, 2.2), loc=(x, y, 0.15), key='dirt', segs=10, rings=5,
             scale=(1.3, 1.0, 0.12))
    for i in range(30):
        x = rnd.uniform(-W / 2 + 0.5, W / 2 - 0.5); y = rnd.uniform(-2, W / 2 - 0.5)
        tuft(f'tf{i}', x, y, 0.2, rnd)
    return finalize('road_end_fade')


def tuft(name, x, y, z, rnd, h=None, key=None):
    """Small grass tuft: a few thin leaning blades (cones)."""
    hh = h or rnd.uniform(0.6, 1.1)
    k = key or rnd.choice(['leaf', 'leaf_light', 'leaf_dark'])
    for b in range(4):
        a = rnd.uniform(0, 360)
        o = cyl(f'{name}_{b}', 0.09, hh * rnd.uniform(0.7, 1.0), loc=(x + rnd.uniform(-0.15, 0.15), y + rnd.uniform(-0.15, 0.15), z),
                key=k, verts=4, r2=0.0)
        o.rotation_euler = (math.radians(rnd.uniform(-25, 25)), math.radians(rnd.uniform(-25, 25)), math.radians(a))


def _dirt_strip(name, centre_fn, n, width_fn, rnd, rut=True):
    """Build a dirt strip mesh from a centreline function t->(x,y,heading).
    Cross section 9 verts: grass-blend edge, shoulders, two wheel ruts, crown."""
    bm = bmesh.new()
    prof = [(-1.08, -0.05), (-0.95, 0.12), (-0.7, 0.2), (-0.45, 0.1), (-0.32, 0.18), (0.0, 0.24),
            (0.32, 0.18), (0.45, 0.1), (0.7, 0.2), (0.95, 0.12), (1.08, -0.05)]
    if not rut:
        prof = [(-1.08, -0.05), (-0.9, 0.12), (-0.5, 0.2), (0.0, 0.24), (0.5, 0.2), (0.9, 0.12), (1.08, -0.05)]
    rows = []
    for i in range(n + 1):
        t = i / n
        x, y, hd = centre_fn(t)
        hw = width_fn(t)
        nx, ny = -math.sin(hd), math.cos(hd)
        row = []
        for k, (u, z) in enumerate(prof):
            j = rnd.uniform(-0.25, 0.25) if k in (0, len(prof) - 1) else rnd.uniform(-0.05, 0.05)
            row.append(bm.verts.new((x + nx * (u * hw + j), y + ny * (u * hw + j), z + rnd.uniform(-0.02, 0.03))))
        rows.append(row)
    for a, b in zip(rows, rows[1:]):
        for k in range(len(prof) - 1):
            bm.faces.new((a[k], a[k + 1], b[k + 1], b[k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj_from_bm(name, bm, 'dirt')
    # make normals face up
    return o


def path_dirt_straight():
    """A6 - dirt path 12 wide x 24 long with wheel ruts, pebbles and grassy verges."""
    reset()
    rnd = random.Random(606)
    L = 24.0
    _dirt_strip('dirt', lambda t: (0, -L / 2 + L * t, math.pi / 2), 24,
                lambda t: 6.0 + math.sin(t * 9.0) * 0.35 + math.sin(t * 23) * 0.15, rnd)
    for i in range(22):
        ball(f'pb{i}', rnd.uniform(0.12, 0.28), loc=(rnd.uniform(-5, 5), rnd.uniform(-L / 2, L / 2), 0.2),
             key=rnd.choice(['stone', 'stone_light', 'stone_dark']), segs=8, rings=5,
             scale=(1.2, 1.0, 0.6))
    for i in range(34):
        side = rnd.choice((-1, 1))
        tuft(f'tf{i}', side * rnd.uniform(5.6, 6.8), rnd.uniform(-L / 2 + 0.3, L / 2 - 0.3), 0.0, rnd)
    for i in range(6):
        tuft(f'mid{i}', rnd.uniform(-0.6, 0.6), rnd.uniform(-L / 2, L / 2), 0.15, rnd, h=0.5)
    return finalize('path_dirt_straight')


def path_dirt_curve():
    """A7 - 90 degree dirt path curve, centreline radius 14."""
    reset()
    rnd = random.Random(707)
    R = 14.0
    _dirt_strip('dirt', lambda t: (math.cos(t * math.pi / 2) * R, math.sin(t * math.pi / 2) * R, t * math.pi / 2 + math.pi / 2),
                30, lambda t: 6.0 + math.sin(t * 11.0) * 0.35, rnd)
    for i in range(26):
        a = rnd.uniform(0, math.pi / 2); r = R + rnd.uniform(-5, 5)
        ball(f'pb{i}', rnd.uniform(0.12, 0.28), loc=(math.cos(a) * r, math.sin(a) * r, 0.2),
             key=rnd.choice(['stone', 'stone_light', 'stone_dark']), segs=8, rings=5, scale=(1.2, 1.0, 0.6))
    for i in range(40):
        a = rnd.uniform(0.02, math.pi / 2 - 0.02); r = R + rnd.choice((-1, 1)) * rnd.uniform(5.6, 6.8)
        tuft(f'tf{i}', math.cos(a) * r, math.sin(a) * r, 0.0, rnd)
    return finalize('path_dirt_curve')


def _stairs(steps, name):
    reset()
    rnd = random.Random(800 + steps)
    width, rise, run = 12.0, 1.0, 2.0
    for s in range(steps):
        z = rise * s
        y = run * s
        # each tread built from 3-4 dressed blocks for a hand-laid look
        x = -width / 2
        k = 0
        while x < width / 2 - 0.1:
            L = min(rnd.uniform(2.6, 4.2), width / 2 - x)
            box(f'st{s}_{k}', (L - 0.08, run + 0.25, rise), loc=(x + L / 2, y + run / 2, z + rise / 2),
                key=rnd.choice(['stone_light', 'stone', 'stone_light']),
                rot=(0, 0, rnd.uniform(-0.6, 0.6)), bev=0.16, segs=2)
            x += L; k += 1
        # fill under the tread
        if s:
            box(f'fill{s}', (width - 0.3, run, z), loc=(0, y + run / 2, z / 2), key='stone_dark')
    # side cheek walls: stepped masonry that follows each step, with a capstone per step
    for side in (-1, 1):
        cx = side * (width / 2 + 0.7)
        for c in range(steps):
            h = rise * (c + 1) + 0.5
            box(f'cheek{side}_{c}', (1.4, run, h), loc=(cx, run * c + run / 2, h / 2), key='stone', bev=0.1, segs=1)
            box(f'cap{side}_{c}', (1.7, run + 0.1, 0.4), loc=(cx, run * c + run / 2, h + 0.2),
                key='stone_light', bev=0.12, segs=2)
        box(f'post{side}', (1.8, 1.8, 2.4), loc=(cx, -0.5, 1.2), key='stone_light', bev=0.18)
        ball(f'postball{side}', 0.6, loc=(cx, -0.5, 2.85), key='stone_light', segs=14, rings=8)
    return finalize(name)


def stairs_3():
    """A8 - three-step dressed-stone stairs, 12 wide, with cheek walls and newel posts."""
    return _stairs(3, 'stairs_3')


def stairs_6():
    """A9 - six-step stairs."""
    return _stairs(6, 'stairs_6')


def curb_stones():
    """A10 - 24-stud run of kerb/edge stones with a gutter channel."""
    reset()
    rnd = random.Random(1010)
    x = -12.0
    i = 0
    while x < 12:
        L = min(rnd.uniform(2.2, 3.2), 12 - x)
        box(f'k{i}', (L - 0.1, 1.2, 1.3), loc=(x + L / 2, 0, 0.65), key=rnd.choice(['stone_light', 'stone']),
            rot=(0, 0, rnd.uniform(-0.8, 0.8)), bev=0.2, segs=2)
        x += L; i += 1
    # gutter setts in front
    x = -12.0
    while x < 12:
        box(f'g{x:.1f}', (0.95, 0.9, 0.3), loc=(x + 0.5, -1.1, 0.42), key='stone_dark',
            rot=(0, 0, rnd.uniform(-2, 2)), bev=0.1, segs=1)
        x += 1.0
    return finalize('curb_stones')


def bridge_footbridge():
    """A11 - small arched wooden footbridge, 20 long x 6 wide, plank deck and post-and-rail sides."""
    reset()
    rnd = random.Random(1111)
    L, Wd, rise = 20.0, 6.0, 2.2
    zf = lambda y: 0.9 + rise * (1 - (2 * y / L) ** 2)
    # two curved stringer beams
    for side in (-1, 1):
        pts = [(side * (Wd / 2 - 0.4), -L / 2 + L * t, zf(-L / 2 + L * t) - 0.45) for t in [i / 8 for i in range(9)]]
        tube(f'stringer{side}', pts, 0.35, 'wood_dark', res=4)
    # deck planks across
    n = 26
    for i in range(n):
        y = -L / 2 + L * (i + 0.5) / n
        slope = math.degrees(math.atan(-8 * rise * y / (L * L)))
        box(f'pl{i}', (Wd + rnd.uniform(-0.15, 0.2), L / n - 0.08, 0.26), loc=(rnd.uniform(-0.08, 0.08), y, zf(y)),
            key=rnd.choice(['wood', 'wood_light', 'wood']), rot=(slope, 0, rnd.uniform(-1.2, 1.2)), bev=0.05, segs=1)
    # railing posts and top rail
    for side in (-1, 1):
        ys = [-L / 2 + L * i / 6 for i in range(7)]
        for j, y in enumerate(ys):
            yy = max(-L / 2 + 0.3, min(L / 2 - 0.3, y))
            box(f'post{side}{j}', (0.4, 0.4, 3.0), loc=(side * (Wd / 2 - 0.1), yy, zf(yy) + 1.4), key='wood_dark', bev=0.06)
            lathe(f'pcap{side}{j}', [(0.0, 0), (0.3, 0), (0.25, 0.2), (0.0, 0.32)], loc=(side * (Wd / 2 - 0.1), yy, zf(yy) + 2.9),
                  key='wood_dark', segs=4)
        rail = [(side * (Wd / 2 - 0.1), -L / 2 + L * t, zf(-L / 2 + L * t) + 2.6) for t in [i / 8 for i in range(9)]]
        tube(f'rail{side}', rail, 0.16, 'wood', res=4)
        mid = [(side * (Wd / 2 - 0.1), -L / 2 + L * t, zf(-L / 2 + L * t) + 1.4) for t in [i / 8 for i in range(9)]]
        tube(f'mrail{side}', mid, 0.11, 'wood', res=4)
        # X braces between posts
        for j in range(6):
            y0 = -L / 2 + L * j / 6 + 0.3; y1 = -L / 2 + L * (j + 1) / 6 - 0.3
            tube(f'x{side}{j}a', [(side * (Wd / 2 - 0.05), y0, zf(y0) + 0.3), (side * (Wd / 2 - 0.05), y1, zf(y1) + 1.3)], 0.07, 'wood_dark', res=4)
    # end stone footings
    for e in (-1, 1):
        box(f'abut{e}', (Wd + 1.5, 2.0, 1.2), loc=(0, e * (L / 2 - 0.2), 0.45), key='stone', bev=0.2)
    return finalize('bridge_footbridge')


def bridge_stone_arch():
    """A12 - large stone arch bridge: 64 long, 16 wide, one main arch with voussoirs, parapets, cobbled deck."""
    reset()
    rnd = random.Random(1212)
    L, Wd, deck = 64.0, 16.0, 12.0
    span, ah = 34.0, 9.5  # arch opening and rise
    # spandrel walls (solid) built as extruded profiles with the arch cut: outline polygon on XZ plane
    def outline():
        pts = [(-L / 2, -2.0), (-span / 2, -2.0)]
        for i in range(25):
            a = math.pi - math.pi * i / 24
            pts.append((math.cos(a) * span / 2, -2.0 + 2.0 + math.sin(a) * ah + 0.0))
        pts += [(span / 2, -2.0), (L / 2, -2.0), (L / 2, deck * 0.72), (L * 0.32, deck), (-L * 0.32, deck), (-L / 2, deck * 0.72)]
        return pts
    o = outline()
    for side in (-1, 1):
        poly_prism(f'spandrel{side}', o, 2.0, loc=(0, side * (Wd / 2) + (-2.0 if side > 0 else 0), 0),
                   key='stone', rot=(90, 0, 0))
    # vault (underside of the arch) as a half tube between faces
    bm = bmesh.new()
    rows = []
    for i in range(25):
        a = math.pi * i / 24
        x = math.cos(a) * span / 2; z = math.sin(a) * ah
        rows.append([bm.verts.new((x, -Wd / 2, z)), bm.verts.new((x, Wd / 2, z))])
    for a, b in zip(rows, rows[1:]):
        bm.faces.new((a[0], b[0], b[1], a[1]))
    _obj_from_bm('vault', bm, 'stone_dark')
    # fill core of bridge (between spandrels) as deck block
    poly_prism('core', o, Wd - 3.8, loc=(0, Wd / 2 - 1.9, 0), key='stone_dark', rot=(90, 0, 0))
    # voussoirs ring on both faces
    nv = 27
    for side in (-1, 1):
        for i in range(nv):
            a = math.pi * (i + 0.5) / nv
            r = span / 2 + 0.9
            x = math.cos(a) * r; z = math.sin(a) * (ah + 0.9)
            box(f'v{side}{i}', (1.9, 2.3, 1.15), loc=(x, side * (Wd / 2 + 0.05), z), key=rnd.choice(['stone_light', 'stone_light', 'stone']),
                rot=(0, -math.degrees(a) + 90, 0), bev=0.15, segs=1)
        box(f'key{side}', (1.6, 2.5, 2.6), loc=(0, side * (Wd / 2 + 0.1), ah + 1.3), key='stone_light', bev=0.18)
    # string course + parapets with copings
    def deck_z(x):
        ax = abs(x)
        if ax < L * 0.32:
            return deck
        return deck - (ax - L * 0.32) / (L / 2 - L * 0.32) * deck * 0.28
    segs = 16
    for side in (-1, 1):
        for i in range(segs):
            x0 = -L / 2 + L * i / segs; x1 = x0 + L / segs
            xm = (x0 + x1) / 2
            z = deck_z(xm)
            ang = math.degrees(math.atan2(deck_z(x1) - deck_z(x0), x1 - x0))
            box(f'sc{side}{i}', (L / segs + 0.1, 0.5, 0.45), loc=(xm, side * (Wd / 2 + 0.25), z - 0.2), key='stone_light', rot=(0, -ang, 0), bev=0.08, segs=1)
            box(f'par{side}{i}', (L / segs + 0.05, 1.3, 3.0), loc=(xm, side * (Wd / 2 - 0.65), z + 1.5), key='stone', rot=(0, -ang, 0), bev=0.12, segs=1)
            box(f'cop{side}{i}', (L / segs + 0.15, 1.7, 0.5), loc=(xm, side * (Wd / 2 - 0.65), z + 3.2), key='stone_light', rot=(0, -ang, 0), bev=0.15, segs=2)
        # end piers / newel blocks with pyramidal caps
        for e in (-1, 1):
            x = e * (L / 2 - 1.0)
            z = deck_z(x)
            box(f'pier{side}{e}', (2.4, 2.4, 4.6), loc=(x, side * (Wd / 2 - 0.65), z + 2.1), key='stone_light', bev=0.2)
            cyl(f'piercap{side}{e}', 1.6, 1.0, loc=(x, side * (Wd / 2 - 0.65), z + 4.4), key='stone_light', verts=4, r2=0.2, rot=(0, 0, 45))
    # cobbled deck surface (strip of setts)
    nx = 30
    for i in range(nx):
        x = -L / 2 + 2 + (L - 4) * (i + 0.5) / nx
        z = deck_z(x)
        ang = math.degrees(math.atan2(deck_z(x + 0.5) - deck_z(x - 0.5), 1.0))
        for j in range(6):
            y = -Wd / 2 + 1.9 + (Wd - 3.8) * (j + 0.5) / 6
            box(f'd{i}_{j}', ((L - 4) / nx - 0.12, (Wd - 3.8) / 6 - 0.12, 0.35), loc=(x, y + rnd.uniform(-0.05, 0.05), z + 0.12),
                key=rnd.choice(STONE_KEYS), rot=(0, -ang, rnd.uniform(-2, 2)), bev=0.1, segs=1)
    # cutwaters (pointed piers in the water at arch springs)
    for e in (-1, 1):
        x = e * (span / 2 + 2.2)
        for side in (-1, 1):
            cyl(f'cut{e}{side}', 2.4, 5.0, loc=(x, side * (Wd / 2 + 0.8), -2.0), key='stone', verts=3, rot=(0, 0, 90 if side > 0 else -90))
    return finalize('bridge_stone_arch')


def signpost():
    """A13 - directional signpost: timber post, three carved arrow boards, small shingle cap."""
    reset()
    rnd = random.Random(1313)
    box('foot', (1.6, 1.6, 0.5), loc=(0, 0, 0.25), key='stone', bev=0.15)
    box('post', (0.6, 0.6, 11.0), loc=(0, 0, 5.8), key='wood_dark', bev=0.08)
    arrow = [(0.0, -0.6), (3.6, -0.6), (4.4, 0.0), (3.6, 0.6), (0.0, 0.6)]
    for i, (z, ang) in enumerate(((9.0, 25), (7.6, 160), (6.2, -70))):
        o = poly_prism(f'board{i}', arrow, 0.22, loc=(0, 0, 0), key=rnd.choice(['wood_light', 'wood']), rot=(90, 0, 0))
        o.rotation_euler = (math.radians(90), 0, math.radians(ang))
        o.location = (0, 0, z)
        # move board so it sits beside the post face
        o.location.x += math.cos(math.radians(ang)) * 0.3 - math.sin(math.radians(ang)) * 0.12
        o.location.y += math.sin(math.radians(ang)) * 0.3 + math.cos(math.radians(ang)) * 0.12
        # painted lettering band (inset dark strip) and nails
        b = box(f'band{i}', (2.4, 0.04, 0.4), loc=(0, 0, 0), key='wood_dark')
        b.rotation_euler = (0, 0, math.radians(ang))
        b.location = (math.cos(math.radians(ang)) * 2.2, math.sin(math.radians(ang)) * 2.2, z)
    # little roof cap
    poly_prism('roofL', [(-1.1, 0), (0, 0.75), (1.1, 0), (1.1, 0.12), (0, 0.9), (-1.1, 0.12)], 1.6,
               loc=(0, 0.8, 11.3), key='roof_red', rot=(90, 0, 0))
    box('capbeam', (1.0, 1.0, 0.25), loc=(0, 0, 11.35), key='wood', bev=0.04)
    return finalize('signpost')


def milestone():
    """A14 - roadside milestone: rounded-top dressed stone with a carved band, moss and grass at base."""
    reset()
    rnd = random.Random(1414)
    # body: profile extruded with rounded top
    pts = [(-1.1, 0.0), (1.1, 0.0), (1.05, 2.4)]
    for i in range(1, 12):
        a = math.pi * i / 12
        pts.append((math.cos(a) * 1.05, 2.4 + math.sin(a) * 0.9))
    pts.append((-1.05, 2.4))
    o = poly_prism('body', pts, 0.8, loc=(0, 0.4, 0), key='stone_light', rot=(90, 0, 0))
    bevel(o, 0.08, 2)
    box('plinth', (2.6, 1.3, 0.45), loc=(0, 0, 0.22), key='stone', bev=0.12)
    # carved recess panel + raised numeral bar shapes
    box('panel', (1.5, 0.08, 1.3), loc=(0, -0.42, 1.9), key='stone')
    for i, (x, w) in enumerate(((-0.35, 0.16), (0.0, 0.16), (0.35, 0.16))):
        box(f'mark{i}', (w, 0.08, 0.8), loc=(x, -0.46, 1.9), key='stone_dark')
    box('arrowbar', (0.9, 0.08, 0.14), loc=(0, -0.46, 1.3), key='stone_dark')
    # moss patches
    for i in range(6):
        sd = rnd.choice((-1, 1))
        ball(f'moss{i}', rnd.uniform(0.2, 0.32), loc=(rnd.uniform(-0.95, 0.95), sd * 0.41, rnd.uniform(0.45, 0.9)),
             key='moss', segs=10, rings=6, scale=(1.6, 0.18, 0.7))
    from roads import tuft as _t
    for i in range(12):
        a = rnd.uniform(0, 6.28)
        _t(f'tf{i}', math.cos(a) * 1.5, math.sin(a) * 0.9, 0.0, rnd)
    return finalize('milestone')


ITEMS = [
    ('A01_road_straight', road_straight),
    ('A02_road_curve', road_curve),
    ('A03_road_tjunction', road_tjunction),
    ('A04_road_crossroads', road_crossroads),
    ('A05_road_end_fade', road_end_fade),
    ('A06_path_dirt_straight', path_dirt_straight),
    ('A07_path_dirt_curve', path_dirt_curve),
    ('A08_stairs_3', stairs_3),
    ('A09_stairs_6', stairs_6),
    ('A10_curb_stones', curb_stones),
    ('A11_bridge_footbridge', bridge_footbridge),
    ('A12_bridge_stone_arch', bridge_stone_arch),
    ('A13_signpost', signpost),
    ('A14_milestone', milestone),
]
