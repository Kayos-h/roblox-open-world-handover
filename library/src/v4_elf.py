"""v4_elf - rebuilt elven village set: natural woods, moss, ivy-green leaves, warm lantern light only (no neon).
Front faces -Y. 1 unit = 1 stud. Treehouses have a real ladder: markers record ladder_bottom/ladder_top/door.
"""
import math, random
import bmesh
from mathutils import Vector, Matrix, noise
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, _obj_from_bm, mat
from nature import blob, rock, branch_tree
import v4util as U

N = [0]
def nm(t):
    N[0] += 1
    return f'{t}{N[0]}'

WOOD = ('ev_wood', 'ev_wood_light', 'ev_wood')
LEAF = ('ev_leaf_a', 'ev_leaf_b', 'ev_leaf_c', 'ev_leaf_d')


# ------------------------------------------------------------------ organic pieces
def bark_trunk(r, h, seed=0, sway=1.2, flare=1.9, key='ev_bark', segs=16, ring_h=1.4, top_r=0.62, lean=(0.0, 0.0)):
    """Irregular tapered trunk with a flared base, vertical bark ridges and a gentle sway."""
    rnd = random.Random(seed)
    off = Vector((seed * 3.1, seed * 1.7, 0))
    bm = bmesh.new()
    nr = max(4, int(h / ring_h))
    rings = []
    for i in range(nr + 1):
        t = i / nr
        z = -0.3 + (h + 0.3) * t
        cx = math.sin(t * 3.1 + seed) * sway * t + lean[0] * t * h
        cy = math.cos(t * 2.3 + seed * 0.7) * sway * t * 0.7 + lean[1] * t * h
        base = r * (top_r + (1 - top_r) * (1 - t) ** 0.8)
        fl = 1.0 + (flare - 1.0) * max(0.0, 1.0 - t * 7.0) ** 2
        ring = []
        for j in range(segs):
            a = 2 * math.pi * j / segs
            ridge = 1.0 + 0.09 * noise.noise(Vector((math.cos(a) * 2.2, math.sin(a) * 2.2, z * 0.35)) + off) + 0.04 * math.sin(a * 5 + z * 0.5)
            rr = base * fl * ridge
            ring.append(bm.verts.new((cx + math.cos(a) * rr, cy + math.sin(a) * rr, z)))
        rings.append(ring)
    for A, B in zip(rings, rings[1:]):
        for j in range(segs):
            k = (j + 1) % segs
            bm.faces.new((A[j], A[k], B[k], B[j]))
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj_from_bm(nm('trunk'), bm, key)


def trunk_point(r, h, seed, z, sway=1.2, lean=(0.0, 0.0)):
    t = z / h
    return (math.sin(t * 3.1 + seed) * sway * t + lean[0] * t * h, math.cos(t * 2.3 + seed * 0.7) * sway * t * 0.7 + lean[1] * t * h)


def roots(r, n=7, seed=0, key='ev_bark', span=2.6, ox=0.0, oy=0.0):
    rnd = random.Random(seed + 11)
    for i in range(n):
        a = 2 * math.pi * i / n + rnd.uniform(-0.25, 0.25)
        c, s = math.cos(a), math.sin(a)
        L = r * rnd.uniform(span * 0.8, span * 1.25)
        tube(nm('root'), [(ox + c * r * 0.5, oy + s * r * 0.5, r * 1.1), (ox + c * r * 1.2, oy + s * r * 1.2, r * 0.45), (ox + c * (r + L * 0.55), oy + s * (r + L * 0.55), r * 0.14), (ox + c * (r + L), oy + s * (r + L), -0.05)],
             r * 0.34, key, res=4, taper=[1, 0.75, 0.5, 0.25], ures=3)


def cluster(cx, cy, z, r, seed=0, n=7, keys=LEAF, flat=0.7):
    """One leaf clump: several small lumpy blobs around a centre, lighter on top, darker underneath."""
    rnd = random.Random(seed * 7 + 3)
    for i in range(n):
        a = rnd.uniform(0, 6.283)
        d = r * 0.55 * math.sqrt(rnd.random())
        dz = rnd.uniform(-r * 0.25, r * 0.3)
        br = r * rnd.uniform(0.38, 0.62)
        k = rnd.choice(keys)
        if dz > r * 0.1:
            k = rnd.choice(('ev_leaf_c', 'ev_leaf_a', 'ev_leaf_c'))
        elif dz < -r * 0.1:
            k = rnd.choice(('ev_leaf_b', 'ev_leaf_d'))
        if rnd.random() < 0.015:
            k = 'ev_leaf_gold'
        blob(nm('lc'), br, (cx + math.cos(a) * d, cy + math.sin(a) * d, z + dz), k, subdiv=2, amp=0.32, scale=(1, 1, flat), seed=rnd.randint(0, 999), detail=0.35)


def crown(cx, cy, z, spread, thick, seed=0, count=26, keys=LEAF, gold=0.08, low=0.0):
    """Natural canopy: many small clumps arranged in two loose layers (a wider lower one, a narrower upper one)."""
    rnd = random.Random(seed + 5)
    nclu = max(6, count // 2)
    for i in range(nclu):
        layer = 0 if i % 3 else 1
        a = rnd.uniform(0, 6.283)
        d = spread * (0.35 + 0.65 * math.sqrt(rnd.random())) * (1.0 if layer == 0 else 0.62)
        zz = z + (-thick * 0.25 if layer == 0 else thick * 0.28) + rnd.uniform(-thick * 0.12, thick * 0.12)
        cluster(cx + math.cos(a) * d, cy + math.sin(a) * d, zz, spread * rnd.uniform(0.2, 0.3), seed=seed * 100 + i, n=rnd.randint(5, 8), keys=keys)
    cluster(cx, cy, z + thick * 0.4, spread * 0.3, seed=seed + 77, n=8, keys=keys)


def limb(base, direction, length, radius, key='ev_bark', droop=0.1, seed=0):
    d = Vector(direction).normalized()
    b = Vector(base)
    mid = b + d * length * 0.5 + Vector((0, 0, length * 0.06))
    end = b + d * length + Vector((0, 0, -length * droop))
    tube(nm('limb'), [tuple(b), tuple(mid), tuple(end)], radius, key, res=4, taper=[1, 0.75, 0.45], ures=3)
    return end


def ivy_strand(p0, L, seed=0, key='ev_leaf_b'):
    rnd = random.Random(seed)
    pts = [Vector(p0)]
    for i in range(1, 5):
        pts.append(Vector((p0[0] + rnd.uniform(-0.4, 0.4), p0[1] + rnd.uniform(-0.4, 0.4), p0[2] - L * i / 4)))
    tube(nm('ivy'), [tuple(p) for p in pts], 0.05, 'ev_leaf_b', res=4, ures=2)
    for i in range(int(L / 0.8)):
        t = (i + 0.5) / max(1, int(L / 0.8))
        k = min(3, int(t * 4))
        p = pts[k].lerp(pts[k + 1], t * 4 - k)
        ball(nm('iv'), rnd.uniform(0.14, 0.24), loc=(p.x + rnd.uniform(-0.15, 0.15), p.y + rnd.uniform(-0.15, 0.15), p.z), key=rnd.choice(('ev_leaf_a', 'ev_leaf_b', 'ev_leaf_c')),
             segs=6, rings=4, scale=(1, 1, 0.55))


def mushrooms(cx, cy, z, n, seed=0, scale=1.0):
    rnd = random.Random(seed)
    for i in range(n):
        a = rnd.uniform(0, 6.283); d = rnd.uniform(0.0, 0.9) * scale
        h = rnd.uniform(0.35, 0.8) * scale
        x, y = cx + math.cos(a) * d, cy + math.sin(a) * d
        cyl(nm('mst'), 0.09 * scale, h, loc=(x, y, z), key='ev_shroom_cream', verts=6)
        lathe(nm('mcap'), [(0, h + 0.18 * scale), (0.2 * scale, h + 0.12 * scale), (0.34 * scale, h), (0.3 * scale, h - 0.05 * scale), (0, h - 0.02 * scale)],
              loc=(x, y, z), key=rnd.choice(('ev_shroom_brown', 'ev_shroom_brown', 'ev_shroom_cream')), segs=8)


def fern(cx, cy, z, n=7, L=1.6, seed=0, key='ev_fern'):
    rnd = random.Random(seed)
    for i in range(n):
        a = 2 * math.pi * i / n + rnd.uniform(-0.3, 0.3)
        d = Vector((math.cos(a), math.sin(a), 0.55 + rnd.uniform(0, 0.4)))
        pts = [(cx, cy, z), (cx + d.x * L * 0.5, cy + d.y * L * 0.5, z + L * 0.45), (cx + d.x * L, cy + d.y * L, z + L * 0.38)]
        tube(nm('fr'), pts, 0.045, key, res=4, ures=2)
        for k in range(5):
            t = 0.25 + 0.15 * k
            px = cx + d.x * L * t; py = cy + d.y * L * t; pz = z + L * (0.5 * t if t < 0.5 else 0.45) 
            for sdir in (-1, 1):
                side = Vector((-d.y, d.x, 0)) * sdir
                ball(nm('fl'), 0.11, loc=(px + side.x * 0.17, py + side.y * 0.17, pz), key=key, segs=5, rings=3, scale=(1, 0.5, 0.25))


# ------------------------------------------------------------------ construction pieces
def lantern(x, y, z, s=1.0, hang=True):
    """Warm candle lantern: brass cap and base, glass body with a gentle glow."""
    if hang:
        tube(nm('lh'), [(x, y, z + 0.9 * s), (x, y, z)], 0.04 * s, 'bronze', res=4)
    lathe(nm('lg'), [(0, 0), (0.26 * s, 0.05 * s), (0.34 * s, 0.4 * s), (0.34 * s, 0.9 * s), (0.22 * s, 1.1 * s), (0, 1.12 * s)], loc=(x, y, z - 1.12 * s), key='ev_lantern', segs=8)
    lathe(nm('lc'), [(0, 1.1 * s), (0.28 * s, 1.08 * s), (0.2 * s, 1.26 * s), (0.05 * s, 1.34 * s), (0, 1.38 * s)], loc=(x, y, z - 1.12 * s), key='bronze', segs=8)
    lathe(nm('lb'), [(0, -0.06 * s), (0.3 * s, -0.06 * s), (0.3 * s, 0.05 * s), (0, 0.05 * s)], loc=(x, y, z - 1.12 * s), key='bronze', segs=8)
    for k in range(4):
        a = math.pi / 2 * k + math.pi / 4
        cyl(nm('lr'), 0.025 * s, 0.9 * s, loc=(x + math.cos(a) * 0.33 * s, y + math.sin(a) * 0.33 * s, z - 1.0 * s), key='bronze', verts=4)


def plank_deck(cx, cy, z, R, thick=0.35, seed=0, hole_r=0.0):
    """Circular plank deck: parallel planks clipped to the circle, plus rim beam and joists."""
    rnd = random.Random(seed)
    w = 0.95
    n = int(2 * R / w)
    for i in range(n):
        x0 = -R + i * w + w / 2
        half = math.sqrt(max(0.01, R * R - x0 * x0))
        L = 2 * half - 0.1
        key = WOOD[i % 3] if rnd.random() > 0.15 else 'ev_wood_aged'
        box(nm('pl'), (w - 0.07, L, thick), loc=(cx + x0, cy, z - thick / 2 + rnd.uniform(-0.02, 0.02)), key=key, bev=0.03)
    torus(nm('rim'), R - 0.05, 0.3, loc=(cx, cy, z - thick * 0.6), key='ev_wood_dark', segs=40, rsegs=6)
    for i in range(10):
        a = 2 * math.pi * i / 10 + 0.15
        c, s = math.cos(a), math.sin(a)
        box(nm('jo'), (R * 0.82, 0.34, 0.4), loc=(cx + c * R * 0.5, cy + s * R * 0.5, z - thick - 0.2), key='ev_wood_dark', rot=(0, 0, math.degrees(a)), bev=0.04)


def deck_braces(cx, cy, z, R, tr, n=6, drop=7.0, seed=0):
    rnd = random.Random(seed)
    for i in range(n):
        a = 2 * math.pi * i / n + 0.3
        c, s = math.cos(a), math.sin(a)
        tube(nm('br'), [(cx + c * (tr + 0.4), cy + s * (tr + 0.4), z - drop), (cx + c * (tr + (R - tr) * 0.55), cy + s * (tr + (R - tr) * 0.55), z - drop * 0.4), (cx + c * (R - 0.5), cy + s * (R - 0.5), z - 0.7)],
             0.34, 'ev_wood_dark', res=4, taper=[1, 0.9, 0.8], ures=2)


def railing(cx, cy, z, R, gap_a=None, gap_w=0.5, post_h=3.0, n=None):
    """Posts around the deck edge with two rails; an opening of half-width gap_w (radians) at gap_a."""
    n = n or max(12, int(2 * math.pi * R / 1.9))
    top, mid, run = [], [], []
    def flush(run):
        if len(run) > 1:
            tube(nm('rt'), [(p[0], p[1], z + post_h) for p in run], 0.13, 'ev_wood_light', res=4, ures=3)
            tube(nm('rm'), [(p[0], p[1], z + post_h * 0.5) for p in run], 0.08, 'ev_wood', res=4, ures=3)
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        inside_gap = gap_a is not None and abs(((a - gap_a + math.pi) % (2 * math.pi)) - math.pi) < gap_w
        x, y = cx + math.cos(a) * (R - 0.35), cy + math.sin(a) * (R - 0.35)
        if inside_gap:
            flush(run); run = []
            continue
        run.append((x, y))
        if i < n:
            cyl(nm('post'), 0.13, post_h, loc=(x, y, z), key='ev_wood', verts=6)
            ball(nm('pc'), 0.17, loc=(x, y, z + post_h), key='ev_wood_light', segs=6, rings=4)
    flush(run)


def ladder(x, y, z0, z1, ang, width=2.3, key_rail='ev_wood_dark', key_rung='ev_wood_light', spacing=1.15, tie_z=None):
    """Vertical wooden ladder at (x, y) facing outward (angle `ang` radians). Rails run z0..z1."""
    c, s = math.cos(ang), math.sin(ang)
    tx, ty = -s, c   # tangent
    H = z1 - z0
    for side in (-1, 1):
        px, py = x + tx * side * width / 2, y + ty * side * width / 2
        box(nm('lr'), (0.28, 0.36, H), loc=(px, py, z0 + H / 2), key=key_rail, rot=(0, 0, math.degrees(ang)), bev=0.04)
        cyl(nm('lf'), 0.2, 0.5, loc=(px, py, z0 - 0.35), key='ev_stone_dark', verts=6)
    n = int((H - 1.0) / spacing)
    for i in range(n + 1):
        zz = z0 + 0.7 + i * spacing
        rung = cyl(nm('rg'), 0.095, width, loc=(x - tx * width / 2, y - ty * width / 2, zz), key=key_rung, verts=8)
        rung.rotation_euler = Matrix.Rotation(math.radians(90), 3, 'X').to_euler() if False else rung.rotation_euler
        # orient along tangent: rotate so local Z points along (tx, ty, 0)
        v = Vector((tx, ty, 0))
        rung.rotation_euler = v.to_track_quat('Z', 'Y').to_euler()
    return (x, y)


def cabin(cx, cy, z, R, h, door_a, seed=0, roof_rise=None, stave_n=20, windows=2, shutters=True):
    """Round cabin of vertical staves with timber bands, door, round windows and a shingled cone roof."""
    rnd = random.Random(seed)
    roof_rise = roof_rise or R * 1.15
    # floor plate and base band
    cyl(nm('cfl'), R + 0.12, 0.3, loc=(cx, cy, z), key='ev_wood_dark', verts=24)
    door_half = math.asin(min(0.95, 1.55 / R))
    for i in range(stave_n):
        a = 2 * math.pi * i / stave_n
        if abs(((a - door_a + math.pi) % (2 * math.pi)) - math.pi) < door_half + 0.02:
            continue
        key = WOOD[i % 3] if rnd.random() > 0.1 else 'ev_wood_aged'
        w = 2 * math.pi * R / stave_n * 0.97
        box(nm('sv'), (w, 0.34, h - 0.3), loc=(cx + math.cos(a) * R, cy + math.sin(a) * R, z + 0.3 + (h - 0.3) / 2), key=key, rot=(0, 0, math.degrees(a) + 90), bev=0.035)
    for zz, rr in ((z + 0.55, R + 0.22), (z + h * 0.52, R + 0.2), (z + h - 0.25, R + 0.24)):
        torus(nm('band'), rr, 0.16, loc=(cx, cy, zz), key='ev_wood_dark', segs=28, rsegs=5)
    # door
    dx, dy = math.cos(door_a), math.sin(door_a)
    fr = door_a
    dh = min(h - 0.9, 5.2)
    dw = 2.7
    c, s = math.cos(fr), math.sin(fr)
    tx, ty = -s, c
    px, py = cx + dx * (R + 0.06), cy + dy * (R + 0.06)
    # door panel (planks)
    for k in range(4):
        off = (k - 1.5) * dw / 4
        box(nm('dp'), (dw / 4 - 0.04, 0.22, dh), loc=(px + tx * off, py + ty * off, z + 0.3 + dh / 2), key=('ev_wood_dark' if k % 2 else 'ev_wood'), rot=(0, 0, math.degrees(fr) + 90), bev=0.03)
    # frame: posts and lintel arch
    for side in (-1, 1):
        box(nm('dfp'), (0.3, 0.42, dh + 0.3), loc=(px + dx * 0.1 + tx * side * (dw / 2 + 0.12), py + dy * 0.1 + ty * side * (dw / 2 + 0.12), z + 0.3 + (dh + 0.3) / 2), key='ev_wood_dark', rot=(0, 0, math.degrees(fr) + 90), bev=0.04)
    box(nm('dfl'), (dw + 0.8, 0.46, 0.34), loc=(px + dx * 0.1, py + dy * 0.1, z + 0.3 + dh + 0.15), key='ev_wood_dark', rot=(0, 0, math.degrees(fr) + 90), bev=0.05)
    # iron straps and handle
    for zz in (0.35, 0.75):
        box(nm('hg'), (dw * 0.85, 0.06, 0.16), loc=(px + dx * 0.14, py + dy * 0.14, z + 0.3 + dh * zz), key='iron', rot=(0, 0, math.degrees(fr) + 90))
    ball(nm('kn'), 0.11, loc=(px + dx * 0.2 + tx * dw * 0.3, py + dy * 0.2 + ty * dw * 0.3, z + 0.3 + dh * 0.48), key='bronze', segs=6, rings=4)
    # step stone
    box(nm('stp'), (dw + 0.6, 1.0, 0.2), loc=(px + dx * 0.7, py + dy * 0.7, z + 0.1), key='ev_stone', rot=(0, 0, math.degrees(fr) + 90), bev=0.05)
    # windows
    placed = 0
    for k, off in enumerate((1.25, -1.25, 2.4, -2.4)):
        if placed >= windows:
            break
        a = door_a + off
        wx, wy = cx + math.cos(a) * (R + 0.02), cy + math.sin(a) * (R + 0.02)
        wz = z + h * 0.58
        rot = math.degrees(a) + 90
        cyl(nm('wg'), 0.62, 0.18, loc=(wx, wy, wz), key='glass_dark', verts=14, rot=(0, 0, 0)).rotation_euler = Vector((math.cos(a), math.sin(a), 0)).to_track_quat('Z', 'Y').to_euler()
        wt = torus(nm('wf'), 0.72, 0.1, loc=(wx + math.cos(a) * 0.08, wy + math.sin(a) * 0.08, wz), key='ev_wood_dark', segs=16, rsegs=4)
        wt.rotation_euler = Vector((math.cos(a), math.sin(a), 0)).to_track_quat('Z', 'Y').to_euler()
        box(nm('wc'), (0.08, 0.1, 1.3), loc=(wx + math.cos(a) * 0.12, wy + math.sin(a) * 0.12, wz), key='ev_wood_dark', rot=(0, 0, math.degrees(a) + 90))
        if shutters:
            for sd in (-1, 1):
                tx2, ty2 = -math.sin(a), math.cos(a)
                box(nm('sh'), (0.55, 0.12, 1.45), loc=(wx + tx2 * sd * 0.98 + math.cos(a) * 0.06, wy + ty2 * sd * 0.98 + math.sin(a) * 0.06, wz), key=rnd.choice(('ev_shingle_a', 'ev_banner_green')), rot=(0, 0, math.degrees(a) + 90), bev=0.025)
        placed += 1
    # roof: dark underlay cone then shingle tiers
    zt = z + h
    lathe(nm('ru'), [(0.0, zt + roof_rise), (R + 0.95, zt - 0.1), (R + 0.95, zt - 0.3), (0.0, zt - 0.3)], loc=(cx, cy, 0), key='ev_wood_dark', segs=24)
    slope = math.atan2(roof_rise, R + 0.95)
    tiers = 7
    for i in range(tiers):
        t = i / tiers
        r_i = (R + 0.95) * (1 - t) + 0.25 * t
        z_i = zt - 0.1 + roof_rise * (1 - (1 - t) * 1.0) * ((R + 0.95 - r_i) / (R + 0.95 - 0.25 + 1e-6)) / max(t, 1e-6) * t if False else zt - 0.1 + roof_rise * ((R + 0.95) - r_i) / (R + 0.7)
        nsh = max(8, int(2 * math.pi * r_i / 0.85))
        L = (R + 0.95) / math.cos(slope) / tiers * 1.55
        for j in range(nsh):
            a = 2 * math.pi * j / nsh + (0.5 * math.pi / nsh if i % 2 else 0)
            tvec = Vector((-math.sin(a), math.cos(a), 0))
            u = Vector((-math.cos(a) * math.cos(slope), -math.sin(a) * math.cos(slope), math.sin(slope)))
            n = tvec.cross(u)
            M = Matrix(((tvec.x, u.x, n.x), (tvec.y, u.y, n.y), (tvec.z, u.z, n.z)))
            k = rnd.choice(('ev_shingle_a', 'ev_shingle_a', 'ev_shingle_a', 'ev_shingle_a', 'ev_shingle_b'))
            wsh = 2 * math.pi * r_i / nsh * 1.12
            base = Vector((cx + math.cos(a) * r_i, cy + math.sin(a) * r_i, z_i))
            nrm_out = Vector((math.cos(a) * math.sin(slope), math.sin(a) * math.sin(slope), math.cos(slope)))
            ctr = base + u * (L * 0.5) + nrm_out * 0.07
            sh = box(nm('shg'), (wsh, L, 0.13), loc=tuple(ctr), key=k)
            sh.rotation_euler = M.to_euler()
            # rounded tip: tiny bevel
    # eave rafter tails
    for i in range(12):
        a = 2 * math.pi * i / 12
        box(nm('raf'), (0.2, 0.9, 0.22), loc=(cx + math.cos(a) * (R + 0.7), cy + math.sin(a) * (R + 0.7), zt - 0.32), key='ev_wood_dark', rot=(0, 0, math.degrees(a) + 90))
    # finial
    cyl(nm('fin'), 0.12, 1.5, loc=(cx, cy, zt + roof_rise - 0.1), key='ev_wood_dark', verts=6)
    ball(nm('fib'), 0.26, loc=(cx, cy, zt + roof_rise + 1.5), key='bronze', segs=8, rings=6)
    # chimney-less: a few moss patches on the roof rim
    for i in range(5):
        a = rnd.uniform(0, 6.28); r_m = (R + 0.4) * rnd.uniform(0.7, 0.95)
        blob(nm('mo'), 0.7, (cx + math.cos(a) * r_m, cy + math.sin(a) * r_m, zt + roof_rise * (1 - r_m / (R + 0.95)) + 0.05), 'ev_moss', subdiv=1, amp=0.3, scale=(1, 1, 0.3), seed=i)


# ------------------------------------------------------------------ the pilot treehouse
def treehouse_a(seed=3, trunk_r=3.2, height=50.0, deck_z=21.0, deck_r=15.5, cab_r=5.3, cab_h=7.4):
    """Treehouse A: one round cabin on a plank deck wrapped around a big old tree, vertical ladder from the ground."""
    reset()
    rnd = random.Random(seed)
    bark_trunk(trunk_r, height, seed=seed)
    roots(trunk_r, n=8, seed=seed)
    tc = trunk_point(trunk_r, height, seed, deck_z)
    # big forking limbs reaching out, each ending in a leaf clump
    tips = []
    for k in range(7):
        az = 2 * math.pi * k / 7 + rnd.uniform(-0.3, 0.3)
        z0 = height * rnd.uniform(0.6, 0.78)
        p0 = trunk_point(trunk_r, height, seed, z0)
        e = limb((p0[0], p0[1], z0), (math.cos(az), math.sin(az), rnd.uniform(0.3, 0.65)), rnd.uniform(12, 18), trunk_r * 0.34, seed=k)
        tips.append(e)
        e2 = limb((e.x, e.y, e.z), (math.cos(az + rnd.uniform(-0.6, 0.6)), math.sin(az + rnd.uniform(-0.6, 0.6)), rnd.uniform(0.4, 0.9)), rnd.uniform(6, 9), trunk_r * 0.16, seed=k + 20)
        tips.append(e2)
    top = trunk_point(trunk_r, height, seed, height)
    tube(nm('lead'), [(top[0], top[1], height * 0.7), (top[0] + 0.5, top[1], height * 0.9), (top[0], top[1], height + 3)], trunk_r * 0.4, 'ev_bark', res=4, taper=[1, 0.6, 0.25])
    crown(top[0], top[1], height * 0.88, 17.0, 12.0, seed=seed, count=30)
    for i, e in enumerate(tips):
        cluster(e.x, e.y, e.z + 1.5, rnd.uniform(4.6, 6.2), seed=seed * 50 + i, n=6)
    # deck
    cx, cy = tc
    plank_deck(cx, cy, deck_z, deck_r, seed=seed)
    deck_braces(cx, cy, deck_z, deck_r, trunk_r * 1.05, seed=seed)
    lad_a = math.radians(-70)   # ladder side
    railing(cx, cy, deck_z, deck_r, gap_a=lad_a, gap_w=0.15)
    # cabin on the far side from the ladder, clear of the trunk
    cab_a = lad_a + math.pi * 0.82
    cab_d = trunk_r * 0.9 + cab_r + 1.0
    ccx, ccy = cx + math.cos(cab_a) * cab_d, cy + math.sin(cab_a) * cab_d
    lx, ly = cx + math.cos(lad_a) * (deck_r + 0.55), cy + math.sin(lad_a) * (deck_r + 0.55)
    door_a = math.atan2(ly - ccy, lx - ccx)
    cabin(ccx, ccy, deck_z, cab_r, cab_h, door_a, seed=seed, windows=3)
    # ladder (vertical, just outside the rim, rails stand 3.2 above the deck as grab handles)
    ladder(lx, ly, 0.0, deck_z + 3.2, lad_a)
    # ties from ladder rails to the deck rim
    for side in (-1, 1):
        tx, ty = -math.sin(lad_a), math.cos(lad_a)
        px, py = lx + tx * side * 1.15, ly + ty * side * 1.15
        for zz in (deck_z - 0.9, deck_z * 0.5):
            tube(nm('tie'), [(px, py, zz), (cx + math.cos(lad_a) * (deck_r - 0.5) + tx * side * 1.15, cy + math.sin(lad_a) * (deck_r - 0.5) + ty * side * 1.15, zz + 0.35)], 0.13, 'ev_wood_dark', res=4)
    # lanterns: one on a post by the cabin door, two on posts beside the ladder opening
    lpx = ccx + math.cos(door_a) * (cab_r + 1.0) + math.sin(door_a) * 2.2
    lpy = ccy + math.sin(door_a) * (cab_r + 1.0) - math.cos(door_a) * 2.2
    cyl(nm('dlp'), 0.13, 4.4, loc=(lpx, lpy, deck_z), key='ev_wood_dark', verts=6)
    lantern(lpx, lpy, deck_z + 4.4 + 1.12, s=1.0, hang=False)
    for side in (-1, 1):
        a = lad_a + side * 0.2
        px, py = cx + math.cos(a) * (deck_r - 0.35), cy + math.sin(a) * (deck_r - 0.35)
        cyl(nm('lps'), 0.1, 1.3, loc=(px, py, deck_z + 3.0), key='ev_wood_dark', verts=6)
        lantern(px, py, deck_z + 5.0, s=0.8, hang=False)
    # deck clutter: barrel, crate, rope coil
    box(nm('crt'), (1.4, 1.4, 1.2), loc=(cx + math.cos(cab_a + 1.1) * (deck_r - 2.4), cy + math.sin(cab_a + 1.1) * (deck_r - 2.4), deck_z + 0.6), key='ev_wood_aged', rot=(0, 0, 25), bev=0.05)
    bx, by = cx + math.cos(cab_a - 1.1) * (deck_r - 2.4), cy + math.sin(cab_a - 1.1) * (deck_r - 2.4)
    cyl(nm('brl'), 0.75, 1.6, loc=(bx, by, deck_z), key='ev_wood_dark', verts=10)
    for zz in (0.4, 1.2):
        torus(nm('brb'), 0.77, 0.05, loc=(bx, by, deck_z + zz), key='iron', segs=12, rsegs=3)
    # hanging ivy from deck rim
    for i in range(10):
        a = rnd.uniform(0, 6.28)
        if abs(((a - lad_a + math.pi) % (2 * math.pi)) - math.pi) < 0.5:
            continue
        ivy_strand((cx + math.cos(a) * (deck_r - 0.1), cy + math.sin(a) * (deck_r - 0.1), deck_z - 0.6), rnd.uniform(2.5, 5.5), seed=i)
    # ground details
    mushrooms(trunk_r * 1.5, -trunk_r * 1.2, 0.0, 5, seed=seed)
    fern(-trunk_r * 2.0, trunk_r * 1.4, 0.0, seed=seed)
    fern(trunk_r * 2.4, trunk_r * 0.8, 0.0, seed=seed + 1)
    for i in range(4):
        a = rnd.uniform(0, 6.28); d = trunk_r * rnd.uniform(2.6, 3.8)
        rock(nm('gr'), rnd.uniform(0.6, 1.2), (math.cos(a) * d, math.sin(a) * d, 0.0), 'ev_stone_dark', seed=i)
    # markers (removed on save): ladder start/end, cabin door, deck centre
    U.marker('mk_lb', (lx, ly, 0.3))
    U.marker('mk_lt', (lx, ly, deck_z + 3.0))
    U.marker('mk_door', (ccx + math.cos(door_a) * (cab_r + 0.5), ccy + math.sin(door_a) * (cab_r + 0.5), deck_z + 2.0))
    U.marker('mk_deck', (cx, cy, deck_z + 0.4))
    obj = finalize('ev_treehouse_a', smooth_angle=38)
    return obj
