"""v5_leadkit - hooks for the lead passes.  Wrap an existing builder so the geometry it has accumulated (the Acc) is reshaped, extended, cleaned and recoloured
right before it becomes scene objects.  No builder code has to be copied.

    LK.wrap(fn, deform=dict(lean=(0.1, 0), bend=(0, 0), twist=0, taper=0, scale=(1, 1, 1), mirror_x=False),
                post=callable(A),                 # add geometry with the normal Acc calls (box, chunk, cyl ...)
                prune=[dict(keys=[...], max_size=2.0, max_z=3.0, min_z=None)],     # delete small loose islands
                recolor=[dict(src=[keys], keys=[ramp bottom->top], wobble=0.05, zlim=None, trange=None)])

Order inside the hook: deform -> prune -> post -> normals -> de-z-fight -> recolor -> original to_scene.  Faces keep their winding when they move to another colour.
"""
import math
import random
import bmesh
from mathutils import Vector
import v5kit

if not hasattr(v5kit.Acc, '_lk_orig_to_scene'):
    v5kit.Acc._lk_orig_to_scene = v5kit.Acc.to_scene
_STACK = []


def _bounds(A):
    zs = [v.co.z for bm in A.bms.values() for v in bm.verts]
    return (min(zs), max(zs)) if zs else (0.0, 1.0)


def _deform(A, lean=(0.0, 0.0), bend=(0.0, 0.0), twist=0.0, taper=0.0, scale=(1.0, 1.0, 1.0), mirror_x=False, mirror_y=False, flare=0.0):
    z0, z1 = _bounds(A)
    H = max(z1 - z0, 1e-6)
    for bm in A.bms.values():
        for v in bm.verts:
            c = v.co
            t = (c.z - z0) / H
            x, y = c.x * scale[0], c.y * scale[1]
            z = z0 + (c.z - z0) * scale[2]
            if taper:
                s = 1.0 - taper * t
                x, y = x * s, y * s
            if flare:
                s = 1.0 + flare * t ** 3
                x, y = x * s, y * s
            if twist:
                a = math.radians(twist * t)
                x, y = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
            x += lean[0] * (c.z - z0) + bend[0] * H * t * t
            y += lean[1] * (c.z - z0) + bend[1] * H * t * t
            if mirror_x:
                x = -x
            if mirror_y:
                y = -y
            v.co = Vector((x, y, z))


def _islands(bm):
    seen = set()
    out = []
    for f in bm.faces:
        if f in seen:
            continue
        stack = [f]
        seen.add(f)
        isl = []
        while stack:
            g = stack.pop()
            isl.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h not in seen:
                        seen.add(h)
                        stack.append(h)
        out.append(isl)
    return out


def _prune(A, rule):
    keys = rule.get('keys') or list(A.bms.keys())
    for k in keys:
        bm = A.bms.get(k)
        if bm is None:
            continue
        kill = []
        for isl in _islands(bm):
            vs = {v for f in isl for v in f.verts}
            xs = [v.co.x for v in vs]
            ys = [v.co.y for v in vs]
            zs = [v.co.z for v in vs]
            size = max(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
            if size > rule.get('max_size', 2.0):
                continue
            if rule.get('thin') is not None and min(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)) > rule['thin']:
                continue
            if rule.get('max_z') is not None and min(zs) > rule['max_z']:
                continue
            if rule.get('min_z') is not None and max(zs) < rule['min_z']:
                continue
            kill.extend(isl)
        if kill:
            bmesh.ops.delete(bm, geom=kill, context='FACES')


def _recolor(A, rule):
    z0, z1 = _bounds(A)
    zl = rule.get('zlim')
    a, b = rule.get('trange') or (zl if zl else (z0, z1))
    span = max(b - a, 1e-6)
    keys = rule['keys']
    wob = rule.get('wobble', 0.05)
    srcs = rule['src'] if isinstance(rule['src'], (list, tuple)) else [rule['src']]
    for sk in srcs:
        bm = A.bms.get(sk)
        if bm is None:
            continue
        moves = []
        for f in bm.faces:
            c = f.calc_center_median()
            if zl and not (zl[0] <= c.z <= zl[1]):
                continue
            t = (c.z - a) / span
            if wob:
                t += random.Random(int(abs(c.x) * 37 + abs(c.y) * 91 + abs(c.z) * 53 + 7) & 0xFFFFFF).uniform(-wob, wob)
            k = keys[max(0, min(len(keys) - 1, int(t * len(keys))))]
            if k != sk:
                moves.append((f, k))
        for f, k in moves:
            tb = A._bm(k)
            vm = {v: tb.verts.new(v.co) for v in f.verts}
            tb.faces.new([vm[v] for v in f.verts])
        if moves:
            bmesh.ops.delete(bm, geom=[f for f, _ in moves], context='FACES')



def _dezfight(A, delta=0.04, min_area=0.02, min_overlap=0.08):
    """Find coplanar, same-direction faces of DIFFERENT islands (boxes) that overlap, and push the conflicting face of the smaller island outward along its normal."""
    isl_vol = []
    items = []
    for bm in A.bms.values():
        if not len(bm.faces):
            continue
        bm.normal_update()
        for isl in _islands(bm):
            vs = {v for f in isl for v in f.verts}
            xs = [v.co.x for v in vs]
            ys = [v.co.y for v in vs]
            zs = [v.co.z for v in vs]
            iid = len(isl_vol)
            isl_vol.append((max(xs) - min(xs) + 1e-3) * (max(ys) - min(ys) + 1e-3) * (max(zs) - min(zs) + 1e-3))
            for f in isl:
                items.append((f, iid))
    byn = {}
    for f, iid in items:
        n = f.normal
        if n.z < -0.9 or f.calc_area() < min_area:
            continue
        byn.setdefault((round(n.x, 2), round(n.y, 2), round(n.z, 2)), []).append((n.dot(f.calc_center_median()), f, iid, n.copy()))
    push = {}
    for lst in byn.values():
        lst.sort(key=lambda r: r[0])
        i0 = 0
        while i0 < len(lst):
            i1 = i0 + 1
            while i1 < len(lst) and lst[i1][0] - lst[i0][0] <= 0.015:
                i1 += 1
            cl = lst[i0:i1]
            i0 = i1
            if len({r[2] for r in cl}) < 2:
                continue
            n = cl[0][3]
            a_ = Vector((0, 0, 1)) if abs(n.z) < 0.9 else Vector((1, 0, 0))
            u = n.cross(a_).normalized()
            w = n.cross(u).normalized()
            bx = []
            for _, f, iid, _n in cl:
                us = [vt.co.dot(u) for vt in f.verts]
                ws = [vt.co.dot(w) for vt in f.verts]
                bx.append((min(us), max(us), min(ws), max(ws), iid, f))
            bx.sort(key=lambda b: b[0])
            for i in range(len(bx)):
                for j in range(i + 1, len(bx)):
                    if bx[j][0] >= bx[i][1] - min_overlap:
                        break
                    if bx[i][4] == bx[j][4] or min(bx[i][3], bx[j][3]) - max(bx[i][2], bx[j][2]) <= min_overlap:
                        continue
                    small = bx[i] if isl_vol[bx[i][4]] < isl_vol[bx[j][4]] else bx[j]
                    push[small[5]] = n
    for f, n in push.items():
        for v in f.verts:
            v.co += n * delta
    return len(push)


def _patched(self, keep_normals=()):
    if not _STACK:
        return v5kit.Acc._lk_orig_to_scene(self, keep_normals)
    cfg = _STACK[-1]
    if cfg.get('deform'):
        _deform(self, **cfg['deform'])
    for rule in cfg.get('prune') or []:
        _prune(self, rule)
    if cfg.get('post'):
        cfg['post'](self)
    for bm in self.bms.values():
        if len(bm.faces):
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if cfg.get('dezfight', True):
        _dezfight(self)
    for rule in cfg.get('recolor') or []:
        _recolor(self, rule)
    keep = tuple(set(keep_normals) | set(self.bms.keys()))
    return v5kit.Acc._lk_orig_to_scene(self, keep)


v5kit.Acc.to_scene = _patched


def wrap(fn, deform=None, post=None, prune=None, recolor=None, dezfight=True):
    cfg = dict(deform=deform, post=post, prune=prune, recolor=recolor, dezfight=dezfight)

    def run():
        _STACK.append(cfg)
        try:
            return fn()
        finally:
            _STACK.pop()
    run.__name__ = getattr(fn, '__name__', 'wrapped') + '_lk'
    return run


def ramp(src, keys, **kw):
    """shortcut for one recolor rule"""
    d = dict(src=src, keys=keys)
    d.update(kw)
    return d
