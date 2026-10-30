"""Architecture helpers for buildings. 1 unit = 1 stud.
Convention: a building's front faces -Y. A Frame F places features on a wall:
local x runs along the wall, local -y points out of the wall, z is up."""
import bpy, bmesh, math, random
from mathutils import Vector, Euler
from kitlib import box, cyl, ball, lathe, tube, torus, poly_prism, _obj_from_bm, mat


class F:
    def __init__(s, x=0.0, y=0.0, z=0.0, rz=0.0):
        s.o = Vector((x, y, z)); s.rz = rz
        s.c, s.s = math.cos(math.radians(rz)), math.sin(math.radians(rz))

    def p(s, x, y, z):
        return (s.o.x + x * s.c - y * s.s, s.o.y + x * s.s + y * s.c, s.o.z + z)

    def r(s, rx=0.0, ry=0.0, rz=0.0):
        return (rx, ry, rz + s.rz)

    def sub(s, x, y, z=0.0, rz=0.0):
        return F(*s.p(x, y, z), s.rz + rz)


def faces(cx, cy, w, d, z=0.0):
    """Frames for the four outer faces of a w x d block (front = -y)."""
    return {'front': F(cx, cy - d / 2, z, 0), 'back': F(cx, cy + d / 2, z, 180),
            'left': F(cx - w / 2, cy, z, -90), 'right': F(cx + w / 2, cy, z, 90)}


_n = [0]
def nm(t):
    _n[0] += 1
    return f'{t}{_n[0]}'


def lbox(f, size, x, y, z, key, rot=(0, 0, 0), bev=0.0):
    """Box in frame-local coordinates (centre)."""
    return box(nm('b'), size, loc=f.p(x, y, z), key=key, rot=f.r(*rot), bev=bev)


def beam3(p0, p1, w, h, key, roll=0.0):
    v = Vector(p1) - Vector(p0)
    o = box(nm('bm'), (w, h, v.length), loc=(Vector(p0) + Vector(p1)) / 2, key=key)
    q = v.to_track_quat('Z', 'Y')
    e = q.to_euler()
    o.rotation_euler = e
    if roll:
        o.rotation_euler.rotate_axis('Z', math.radians(roll))
    return o


def lbeam(f, a, b, t, key, h=None):
    return beam3(f.p(*a), f.p(*b), t, h or t, key)


def slab(pts, vec, key):
    """Prism from a planar polygon (world points) extruded by vec."""
    bm = bmesh.new()
    A = [bm.verts.new(p) for p in pts]
    B = [bm.verts.new(Vector(p) + Vector(vec)) for p in pts]
    n = len(pts)
    bm.faces.new(A); bm.faces.new(list(reversed(B)))
    for i in range(n):
        bm.faces.new((A[i], B[i], B[(i + 1) % n], A[(i + 1) % n]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj_from_bm(nm('sl'), bm, key)


def lslab(f, pts, vec, key):
    return slab([f.p(*p) for p in pts], Vector(f.p(*vec)) - Vector(f.p(0, 0, 0)), key)


def arc_pts(f, x, z, r, y=0.0, n=9, a0=0.0, a1=180.0):
    return [f.p(x + math.cos(math.radians(a)) * r, y, z + math.sin(math.radians(a)) * r)
            for a in [a0 + (a1 - a0) * i / (n - 1) for i in range(n)]]


def half_disc(f, x, z, r, y0, t, key, n=10, extra=0.0):
    """Vertical semicircle (plus a rectangle `extra` tall below) in the wall plane."""
    pts = [(x + math.cos(math.pi * i / n) * r, y0, z + math.sin(math.pi * i / n) * r) for i in range(n + 1)]
    if extra:
        pts = [(x - r, y0, z - extra)] + list(reversed(pts)) + [(x + r, y0, z - extra)]
        pts = list(reversed(pts))
    return lslab(f, pts, (0, -t, 0), key)


# ------------------------------------------------------------- openings
def window(f, x, z, w=2.2, h=3.4, arch=False, frame='wood_paint', glass='glass_dark', shutter=None,
           sill='ashlar', lintel=None, flowers=None, panes=True, lit=False, keystone=None):
    """z = bottom of the opening. Built on the wall plane y=0, sticking out toward -y."""
    g = 'glass_lit' if lit else glass
    hr = h - (w / 2 if arch else 0)
    lbox(f, (w, 0.12, hr), x, -0.06, z + hr / 2, g)
    if arch:
        half_disc(f, x, z + hr, w / 2, 0.0, 0.12, g)
        tube(nm('af'), arc_pts(f, x, z + hr, w / 2 + 0.12, y=-0.2, n=11), 0.17, frame, res=4)
        if keystone:
            lbox(f, (0.5, 0.35, 0.8), x, -0.25, z + hr + w / 2 + 0.15, keystone)
    for s in (-1, 1):
        lbox(f, (0.26, 0.34, hr), x + s * (w / 2 + 0.05), -0.17, z + hr / 2, frame)
    if not arch:
        lbox(f, (w + 0.36, 0.34, 0.26), x, -0.17, z + h + 0.05, frame)
    if panes:
        lbox(f, (0.12, 0.24, hr + (w / 2 if arch else 0) - 0.1), x, -0.14, z + (hr + (w / 2 if arch else 0)) / 2, frame)
        lbox(f, (w, 0.24, 0.12), x, -0.14, z + hr * 0.62, frame)
    if lintel:
        lbox(f, (w + 0.9, 0.36, 0.5), x, -0.18, z + h + 0.35, lintel, bev=0.05)
    if sill:
        lbox(f, (w + 0.7, 0.6, 0.24), x, -0.3, z - 0.12, sill, bev=0.04)
    if shutter:
        sw = w / 2 + 0.1
        for s in (-1, 1):
            cx = x + s * (w / 2 + 0.25 + sw / 2)
            lbox(f, (sw, 0.14, hr), cx, -0.1, z + hr / 2, shutter)
            for zz in (0.22, 0.5, 0.78):
                lbox(f, (sw - 0.1, 0.06, 0.1), cx, -0.2, z + hr * zz, 'timber')
    if flowers:
        flower_box(f, x, z - 0.25, w + 0.4, flowers)


def flower_box(f, x, z, w, colours, seed=None):
    rnd = random.Random(seed if seed is not None else int(abs(x * 13 + z * 7)))
    lbox(f, (w, 0.75, 0.6), x, -0.55, z - 0.3, 'wood', bev=0.04)
    lbox(f, (w - 0.15, 0.6, 0.05), x, -0.55, z + 0.0, 'dirt')
    n = max(3, int(w / 0.45))
    for i in range(n):
        xx = x - w / 2 + 0.25 + (w - 0.5) * i / (n - 1)
        ball(nm('lf'), rnd.uniform(0.28, 0.38), loc=f.p(xx, -0.55 + rnd.uniform(-0.15, 0.15), z + 0.15), key=rnd.choice(['leaf', 'leaf_dark']),
             segs=7, rings=5, scale=(1, 1, 0.8))
        if rnd.random() < 0.75:
            ball(nm('fl'), rnd.uniform(0.13, 0.18), loc=f.p(xx + rnd.uniform(-0.1, 0.1), -0.75, z + rnd.uniform(0.35, 0.55)), key=rnd.choice(colours),
                 segs=6, rings=4)


def door(f, x, w=3.4, h=6.4, arch=True, key='door_paint', surround='ashlar', step='stone', lamp=False, studs=True):
    hr = h - (w / 2 if arch else 0)
    lbox(f, (w, 0.2, hr), x, -0.05, hr / 2, key)
    if arch:
        half_disc(f, x, hr, w / 2, 0.05, 0.2, key)
    n = int(w / 0.8)
    for i in range(1, n):
        xx = x - w / 2 + w * i / n
        top = hr + (math.sqrt(max(0.0, (w / 2) ** 2 - (xx - x) ** 2)) if arch else 0)
        lbox(f, (0.06, 0.06, top - 0.1), xx, -0.17, top / 2, 'timber')
    for zz in (hr * 0.22, hr * 0.78):
        lbox(f, (w * 0.82, 0.08, 0.2), x - w * 0.05, -0.2, zz, 'iron')
        if studs:
            for k in range(4):
                ball(nm('st'), 0.07, loc=f.p(x - w * 0.42 + k * w * 0.22, -0.25, zz), key='iron', segs=6, rings=4)
    torus(nm('ring'), 0.22, 0.05, loc=f.p(x + w * 0.3, -0.25, hr * 0.5), key='brass', segs=12, rsegs=4, rot=f.r(90, 0, 0))
    if surround:
        for s in (-1, 1):
            lbox(f, (0.6, 0.45, hr), x + s * (w / 2 + 0.3), -0.2, hr / 2, surround, bev=0.05)
        if arch:
            tube(nm('ds'), arc_pts(f, x, hr, w / 2 + 0.3, y=-0.22, n=13), 0.32, surround, res=4)
            lbox(f, (0.6, 0.5, 0.9), x, -0.3, hr + w / 2 + 0.25, surround, bev=0.05)
        else:
            lbox(f, (w + 1.4, 0.45, 0.6), x, -0.2, hr + 0.3, surround, bev=0.05)
    if step:
        lbox(f, (w + 1.8, 1.4, 0.5), x, -0.7, 0.25, step, bev=0.06)
    if lamp:
        wall_lantern(f, x + w / 2 + 1.3, h - 0.4)


def wall_lantern(f, x, z, s=1.0):
    lbox(f, (0.5 * s, 0.15, 0.9 * s), x, -0.08, z, 'iron')
    lbeam(f, (x, -0.1, z + 0.2 * s), (x, -1.0 * s, z + 0.2 * s), 0.1 * s, 'iron')
    tube(nm('wlc'), [f.p(x, -0.1, z - 0.3 * s), f.p(x, -0.6 * s, z - 0.1 * s), f.p(x, -1.0 * s, z + 0.2 * s)], 0.05 * s, 'iron', res=4)
    c = f.p(x, -1.0 * s, z - 0.55 * s)
    lathe(nm('wl'), [(0.0, 0.0), (0.24, 0.0), (0.32, 0.12), (0.0, 0.12)], loc=(c[0], c[1], c[2] - 0.2 * s), key='iron', segs=6, sx=s, sy=s)
    lathe(nm('wlt'), [(0.0, 0.64), (0.42, 0.64), (0.42, 0.72), (0.15, 0.95), (0.0, 1.0)], loc=(c[0], c[1], c[2] - 0.2 * s), key='iron', segs=6, sx=s, sy=s)
    lathe(nm('wlg'), [(0.0, 0.12), (0.3, 0.12), (0.3, 0.64), (0.0, 0.64)], loc=(c[0], c[1], c[2] - 0.2 * s), key='glass_lit', segs=6, sx=s, sy=s)


def arrow_slit(f, x, z, h=2.6, key='stone_dark'):
    lbox(f, (0.35, 0.1, h), x, -0.03, z, 'glass_dark')
    lbox(f, (1.2, 0.1, 0.32), x, -0.03, z + h * 0.15, 'glass_dark')
    lbox(f, (0.95, 0.3, 0.3), x, -0.12, z - h / 2 - 0.15, key)
    lbox(f, (0.95, 0.3, 0.3), x, -0.12, z + h / 2 + 0.15, key)


# ------------------------------------------------------------- walls & trim
def quoins(f, z0, z1, key, sizes=(1.6, 1.0), course=1.1, t=0.18):
    """Corner stones at frame origin: the corner where this face meets the face to its left (local -x side)."""
    k = 0
    z = z0
    while z + course <= z1 + 0.01:
        a, b = (sizes if k % 2 == 0 else sizes[::-1])
        lbox(f, (a, t, course - 0.12), a / 2 - 0.02, -t / 2, z + course / 2, key, bev=0.04)
        lbox(f, (t, b, course - 0.12), -t / 2, b / 2 - 0.02 - t, z + course / 2, key, bev=0.04)
        z += course; k += 1


def band(cx, cy, w, d, z, h, key, out=0.25, bev=0.05):
    return box(nm('band'), (w + 2 * out, d + 2 * out, h), loc=(cx, cy, z + h / 2), key=key, bev=bev)


def corbels(f, x0, x1, z, key, step=1.6, size=(0.6, 0.8, 0.9)):
    n = max(1, int((x1 - x0) / step))
    for i in range(n + 1):
        xx = x0 + (x1 - x0) * i / n
        lbox(f, (size[0], size[1], size[2] * 0.5), xx, -size[1] / 2, z + size[2] * 0.75, key)
        lbox(f, (size[0], size[1] * 0.6, size[2] * 0.5), xx, -size[1] * 0.3, z + size[2] * 0.25, key)


def battlements(f, x0, x1, z, key, t=1.0, mw=1.6, gap=1.1, mh=1.8, ph=1.3, y=0.0, cap=None):
    """Parapet + merlons along the frame's local x from x0 to x1, outer face at local y."""
    L = x1 - x0
    lbox(f, (L, t, ph), (x0 + x1) / 2, y + t / 2, z + ph / 2, key)
    n = max(1, int((L + gap) / (mw + gap)))
    pitch = L / n
    for i in range(n):
        xx = x0 + pitch * (i + 0.5)
        lbox(f, (pitch - gap, t, mh), xx, y + t / 2, z + ph + mh / 2, key, bev=0.05)
        if cap:
            lbox(f, (pitch - gap + 0.2, t + 0.2, 0.25), xx, y + t / 2, z + ph + mh + 0.1, cap)


def ring_battlements(cx, cy, z, r, key, t=1.0, n=None, mh=1.8, ph=1.3, cap=None, machicolate=True):
    circ = 2 * math.pi * r
    n = n or max(8, int(circ / 2.8))
    lathe(nm('par'), [(r - t, z), (r, z), (r, z + ph), (r - t, z + ph)], loc=(cx, cy, 0), key=key, segs=max(16, n * 2))
    for i in range(n):
        a = 360 * (i + 0.5) / n
        ar = math.radians(a)
        box(nm('mer'), (t, circ / n * 0.55, mh), loc=(cx + math.cos(ar) * (r - t / 2), cy + math.sin(ar) * (r - t / 2), z + ph + mh / 2),
            key=key, rot=(0, 0, a), bev=0.05)
        if cap:
            box(nm('mc'), (t + 0.2, circ / n * 0.55 + 0.2, 0.25), loc=(cx + math.cos(ar) * (r - t / 2), cy + math.sin(ar) * (r - t / 2), z + ph + mh + 0.1),
                key=cap, rot=(0, 0, a))
        if machicolate:
            ar2 = math.radians(360 * i / n)
            for zz, dd, hh in ((z - 0.45, 0.5, 0.9), (z - 1.25, 0.25, 0.7)):
                box(nm('mac'), (dd + 0.4, 0.7, hh), loc=(cx + math.cos(ar2) * (r - 0.6 + dd), cy + math.sin(ar2) * (r - 0.6 + dd), zz),
                    key=key, rot=(0, 0, math.degrees(ar2)))


def timber_frame(f, w, z0, z1, posts, key='timber', t=0.42, braces=True, skip=()):
    """Exposed beams on a plastered face. posts = local x positions."""
    lbox(f, (w + 0.1, t, t), 0, -t / 2, z0 + t / 2, key)
    lbox(f, (w + 0.1, t, t), 0, -t / 2, z1 - t / 2, key)
    for px in posts:
        lbox(f, (t, t, z1 - z0), px, -t / 2, (z0 + z1) / 2, key)
    if braces:
        for i, (a, b) in enumerate(zip(posts, posts[1:])):
            if i in skip:
                continue
            m = (b - a) * 0.28
            lbeam(f, (a + t / 2, -t / 2, z0 + t), (a + m, -t / 2, z0 + (z1 - z0) * 0.42), t * 0.8, key)
            lbeam(f, (b - t / 2, -t / 2, z0 + t), (b - m, -t / 2, z0 + (z1 - z0) * 0.42), t * 0.8, key)


# ------------------------------------------------------------- roofs
def gable_roof(f, L, D, z0, hr, keys=('tile_a', 'tile_b'), ov=1.0, ovg=0.9, wall='plaster', barge='timber',
               ridge=None, row=1.15, infill=True, crest=None):
    """Ridge along frame-local x (length L), spanning D across local y, eaves at z0, rise hr."""
    a = math.atan2(hr, D / 2)
    hw = D / 2 + ov
    S = hw / math.cos(a)
    zr = z0 + hr
    n = max(3, round(S / row))
    rl = S / n
    LL = L + 2 * ovg
    for s in (-1, 1):
        nrm = Vector((0, s * math.sin(a), math.cos(a)))
        dirv = Vector((0, s * math.cos(a), -math.sin(a)))
        c = Vector((0, 0, zr)) + dirv * (S / 2) - nrm * 0.12
        lbox(f, (LL, S, 0.24), 0, c.y, c.z, barge, rot=(-s * math.degrees(a), 0, 0))
        for i in range(n):
            cc = Vector((0, 0, zr)) + dirv * (rl * (i + 0.55)) + nrm * (0.12 + 0.02 * (i % 2))
            lbox(f, (LL + (0.12 if i % 2 else 0), rl * 1.18, 0.26), (0.06 if i % 2 else 0), cc.y, cc.z, keys[i % len(keys)],
                 rot=(-s * (math.degrees(a) + 3.5), 0, 0))
        for g in (-1, 1):
            p0 = (g * (LL / 2 + 0.05), s * hw, zr - S * math.sin(a) + 0.15)
            p1 = (g * (LL / 2 + 0.05), 0, zr + 0.3)
            lbeam(f, p0, p1, 0.3, barge, 0.7)
    lbeam(f, (-LL / 2 - 0.1, 0, zr + 0.3), (LL / 2 + 0.1, 0, zr + 0.3), 0.75, ridge or keys[-1], 0.55)
    if infill:
        for g in (-1, 1):
            pts = [(g * L / 2, -D / 2, z0), (g * L / 2, D / 2, z0), (g * L / 2, 0, zr - 0.1)]
            lslab(f, pts, (-g * 0.6, 0, 0), wall)
    if crest:
        for g in (-1, 1):
            lathe(nm('fin'), [(0, 0), (0.2, 0), (0.12, 0.6), (0.3, 0.9), (0.06, 1.3), (0, 1.8)], loc=f.p(g * (LL / 2 - 0.2), 0, zr + 0.5), key=crest, segs=8)
    return zr


def roof_z(z0, hr, D, y):
    """Roof surface height at local y for a gable_roof."""
    return z0 + hr * (1 - abs(y) / (D / 2))


def cone_roof(cx, cy, z, r, h, keys=('tile_a', 'tile_b'), rings=7, ov=0.8, finial='gold', segs=24, flag=None):
    R = r + ov
    zz = z - ov * (h / r)
    for k in range(rings):
        t0, t1 = k / rings, (k + 1) / rings
        ra, rb = R * (1 - t0), R * (1 - t1)
        za, zb = zz + (h + ov * h / r) * t0, zz + (h + ov * h / r) * t1
        prof = [(ra + 0.18, za - 0.25), (ra + 0.18, za), (rb + 0.05, zb + 0.08), (0.0, zb + 0.08)] if k < rings - 1 else \
               [(ra + 0.18, za - 0.25), (ra + 0.18, za), (0.0, zb)]
        lathe(nm('cr'), prof, loc=(cx, cy, 0), key=keys[k % len(keys)], segs=segs)
    lathe(nm('soff'), [(0.0, zz - 0.25), (R + 0.18, zz - 0.25), (R + 0.18, zz - 0.1), (0.0, zz - 0.1)], loc=(cx, cy, 0), key='timber', segs=segs)
    top = zz + h + ov * h / r
    if finial:
        lathe(nm('fn'), [(0, 0), (0.35, 0), (0.2, 0.5), (0.45, 1.0), (0.4, 1.3), (0.12, 1.5), (0.1, 3.2), (0, 3.6)],
              loc=(cx, cy, top - 0.2), key=finial, segs=10)
        ball(nm('fb'), 0.42, loc=(cx, cy, top + 1.1), key=finial, segs=10, rings=6)
    if flag:
        cyl(nm('fp'), 0.12, 6.0, loc=(cx, cy, top + 2.5), key='iron', verts=8)
        from props import cloth
        cloth(nm('fl'), 3.2, 1.9, (cx + 1.7, cy, top + 7.8), flag, waves=1.0, amp=0.25, seed=int(cx + cy) % 7)
    return top


def chimney(x, y, zb, zt, w=1.8, key='brick'):
    box(nm('ch'), (w, w, zt - zb), loc=(x, y, (zb + zt) / 2), key=key)
    box(nm('chc'), (w + 0.4, w + 0.4, 0.4), loc=(x, y, zt - 0.6), key='stone_dark', bev=0.05)
    box(nm('chc'), (w + 0.25, w + 0.25, 0.3), loc=(x, y, zt + 0.05), key='stone_dark', bev=0.05)
    for s in (-1, 1):
        cyl(nm('pot'), 0.28, 0.9, loc=(x + s * w * 0.22, y, zt + 0.2), key='terracotta', verts=10, r2=0.22)


def dormer(f, x, y, zbase, w=3.4, h=3.6, depth=5.0, wall='plaster', keys=('tile_a', 'tile_b'), frame='wood_paint', flowers=None):
    """Small gabled dormer; front face at local y, built back into the roof (+y)."""
    lbox(f, (w, depth, h), x, y + depth / 2, zbase + h / 2, wall)
    window(f.sub(x, y, zbase), 0, 0.6, w=w * 0.52, h=h - 1.2, frame=frame, sill=frame, panes=True, flowers=flowers)
    gable_roof(f.sub(x, y + depth / 2, 0, 90), depth + 0.4, w, zbase + h, w * 0.55, keys=keys, ov=0.4, ovg=0.3, wall=wall, row=0.9)


def railing(f, x0, x1, z, y=0.0, h=1.6, key='iron', step=0.4):
    lbox(f, (x1 - x0, 0.12, 0.12), (x0 + x1) / 2, y, z + h, key)
    lbox(f, (x1 - x0, 0.1, 0.1), (x0 + x1) / 2, y, z + 0.2, key)
    n = max(2, int((x1 - x0) / step))
    for i in range(n + 1):
        xx = x0 + (x1 - x0) * i / n
        lbox(f, (0.07, 0.07, h), xx, y, z + h / 2, key)



# ------------------------------------------------------------- gothic & classical
def lancet_pts(x, z0, zs, w, n=7):
    """Outline of a pointed arch opening (local x,z). zs = springing height."""
    pts = [(x - w / 2, z0)]
    for i in range(n):
        a = math.radians(180 - 60 * i / (n - 1))
        pts.append((x + w / 2 + math.cos(a) * w, zs + math.sin(a) * w))
    for i in range(1, n):
        a = math.radians(60 - 60 * i / (n - 1))
        pts.append((x - w / 2 + math.cos(a) * w, zs + math.sin(a) * w))
    pts.append((x + w / 2, z0))
    return pts


def lancet(f, x, z, w=2.4, h=8.0, glass='stained_b', frame='castle_trim', medallion='stained_y', lead=True, t=0.12):
    zs = z + h - w * 0.866
    pts = lancet_pts(x, z, zs, w)
    lslab(f, [(px, 0.0, pz) for px, pz in pts], (0, -t, 0), glass)
    tube(nm('lf'), [f.p(px, -0.2, pz) for px, pz in pts[1:-1]], 0.2, frame, res=4)
    for s in (-1, 1):
        lbox(f, (0.4, 0.4, zs - z), x + s * (w / 2 + 0.05), -0.2, (z + zs) / 2, frame)
    lbox(f, (w + 0.8, 0.6, 0.3), x, -0.3, z - 0.15, frame)
    if lead:
        lbox(f, (0.1, 0.2, zs - z + w * 0.7), x, -0.16, (z + zs + w * 0.7) / 2, 'iron_dark')
        k = int((zs - z) / 1.6)
        for i in range(1, k + 1):
            lbox(f, (w, 0.18, 0.08), x, -0.15, z + (zs - z) * i / (k + 1), 'iron_dark')
    if medallion:
        cyl(nm('md'), w * 0.26, 0.05, loc=f.p(x, -0.14, zs + w * 0.3), key=medallion, verts=12, rot=f.r(90, 0, 0))


def rose_window(f, x, z, r, keys=('stained_b', 'stained_r', 'stained_y', 'stained_g'), frame='castle_trim', petals=12):
    cyl(nm('rw'), r, 0.1, loc=f.p(x, 0.02, z), key=keys[0], verts=32, rot=f.r(90, 0, 0))
    for i in range(petals):
        a0 = 2 * math.pi * i / petals
        a1 = 2 * math.pi * (i + 1) / petals
        pts = [(x + math.cos(a0) * r * 0.38, -0.0, z + math.sin(a0) * r * 0.38), (x + math.cos(a0) * r * 0.92, 0, z + math.sin(a0) * r * 0.92),
               (x + math.cos((a0 + a1) / 2) * r * 0.97, 0, z + math.sin((a0 + a1) / 2) * r * 0.97), (x + math.cos(a1) * r * 0.92, 0, z + math.sin(a1) * r * 0.92),
               (x + math.cos(a1) * r * 0.38, 0, z + math.sin(a1) * r * 0.38)]
        lslab(f, pts, (0, -0.14, 0), keys[1 + i % (len(keys) - 1)])
        lbeam(f, (x + math.cos(a0) * r * 0.36, -0.22, z + math.sin(a0) * r * 0.36), (x + math.cos(a0) * r, -0.22, z + math.sin(a0) * r), 0.22, frame)
    cyl(nm('rc'), r * 0.36, 0.2, loc=f.p(x, -0.05, z), key=keys[2], verts=16, rot=f.r(90, 0, 0))
    for rr, th in ((r + 0.25, 0.42), (r * 0.37, 0.18)):
        torus(nm('rr'), rr, th, loc=f.p(x, -0.25, z), key=frame, segs=36, rsegs=6, rot=f.r(90, 0, 0))


def column_c(x, y, z, h, r, key='castle_trim', base='castle_trim', fluted=False):
    lathe(nm('cb'), [(0.0, 0.0), (r * 1.45, 0.0), (r * 1.45, r * 0.4), (r * 1.25, r * 0.55), (r * 1.15, r * 0.8), (0.0, r * 0.8)], loc=(x, y, z), key=base, segs=16)
    lathe(nm('cs'), [(0.0, r * 0.8), (r, r * 0.8), (r * 0.88, h - r * 0.9), (0.0, h - r * 0.9)], loc=(x, y, z), key=key, segs=16)
    lathe(nm('cc'), [(0.0, h - r * 0.9), (r * 1.0, h - r * 0.9), (r * 1.25, h - r * 0.5), (r * 1.5, h - r * 0.4), (r * 1.5, h), (0.0, h)], loc=(x, y, z), key=base, segs=4 if not fluted else 16, sx=1.0, sy=1.0)


def pediment(f, x, z, w, h, d, key='castle_trim', tymp='ashlar', emblem=None):
    lslab(f, [(x - w / 2, 0, z), (x + w / 2, 0, z), (x, 0, z + h)], (0, d, 0), tymp)
    for s in (-1, 1):
        lbeam(f, (x + s * (w / 2 + 0.4), -0.3, z + 0.1), (x, -0.3, z + h + 0.45), 0.8, key, 0.7)
    lbox(f, (w + 1.2, 0.9, 0.8), x, -0.1, z - 0.2, key)
    if emblem:
        cyl(nm('pe'), h * 0.28, 0.3, loc=f.p(x, -0.1, z + h * 0.38), key=emblem, verts=16, rot=f.r(90, 0, 0))


def dome(cx, cy, z, r, key='patina', ribs='castle_trim', drum=None, drum_h=4.0, lantern=True, nrib=12, finial='gold'):
    if drum:
        lathe(nm('dr'), [(0.0, z), (r + 0.4, z), (r + 0.4, z + drum_h), (0.0, z + drum_h)], loc=(cx, cy, 0), key=drum, segs=32)
        lathe(nm('drc'), [(0.0, z + drum_h - 0.4), (r + 0.8, z + drum_h - 0.4), (r + 0.8, z + drum_h + 0.2), (0.0, z + drum_h + 0.2)], loc=(cx, cy, 0), key=ribs, segs=32)
        for i in range(nrib):
            a = 2 * math.pi * (i + 0.5) / nrib
            fr = F(cx + math.cos(a) * (r + 0.4), cy + math.sin(a) * (r + 0.4), 0, math.degrees(a) + 90)
            window(fr, 0, z + 0.8, w=1.2, h=drum_h - 1.6, arch=True, frame=ribs, sill=None, panes=False)
        z += drum_h + 0.2
    prof = [(math.cos(math.radians(a)) * r, z + math.sin(math.radians(a)) * r * 1.05) for a in range(0, 91, 10)]
    prof[-1] = (0.0, prof[-1][1])
    lathe(nm('dm'), prof, loc=(cx, cy, 0), key=key, segs=32)
    for i in range(nrib):
        a = 2 * math.pi * i / nrib
        pts = [(cx + math.cos(a) * math.cos(math.radians(t)) * (r + 0.08), cy + math.sin(a) * math.cos(math.radians(t)) * (r + 0.08),
                z + math.sin(math.radians(t)) * (r * 1.05 + 0.08)) for t in range(0, 85, 12)]
        tube(nm('rb'), pts, 0.18, ribs, res=4)
    top = z + r * 1.05
    if lantern:
        lr = max(1.0, r * 0.2)
        cyl(nm('ln'), lr, lr * 2.0, loc=(cx, cy, top - 0.3), key=ribs, verts=12)
        for i in range(6):
            a = 2 * math.pi * i / 6
            fr = F(cx + math.cos(a) * lr, cy + math.sin(a) * lr, 0, math.degrees(a) + 90)
            window(fr, 0, top + lr * 0.3, w=lr * 0.6, h=lr * 1.2, arch=True, frame=ribs, sill=None, panes=False, lit=True)
        lathe(nm('lc'), [(0.0, top + lr * 1.7), (lr * 1.2, top + lr * 1.7), (lr * 0.2, top + lr * 2.9), (0.0, top + lr * 3.0)], loc=(cx, cy, 0), key=key, segs=12)
        top += lr * 3.0
    if finial:
        lathe(nm('df'), [(0, 0), (0.3, 0), (0.12, 0.6), (0.35, 1.0), (0.08, 1.5), (0.06, 3.0), (0, 3.3)], loc=(cx, cy, top - 0.1), key=finial, segs=8)
    return top


def pinnacle(x, y, z, s=1.2, h=5.0, key='castle_trim', tip='castle_trim'):
    box(nm('pn'), (s, s, h * 0.45), loc=(x, y, z + h * 0.225), key=key, bev=0.05)
    lathe(nm('pt'), [(0.0, 0.0), (s * 0.75, 0.0), (0.0, h * 0.55)], loc=(x, y, z + h * 0.45), key=tip, segs=4)
    for k in range(3):
        box(nm('cro'), (s * 0.3, s * 0.3, s * 0.3), loc=(x, y, z + h * 0.45 + h * 0.55 * (k + 1) / 4 + 0.15), key=tip, rot=(45, 45, 0))
    ball(nm('pb'), s * 0.22, loc=(x, y, z + h + 0.05), key=tip, segs=6, rings=4)
