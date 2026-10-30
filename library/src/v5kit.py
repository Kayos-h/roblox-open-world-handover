"""v5kit - helpers for the v5 modules.
Acc builds geometry straight into one bmesh per palette key (no scene objects), so a model with thousands of parts builds in
well under a second. A builder does:  reset(); A = Acc(); A.box(...); ...; A.to_scene(); return finalize('name').
kitlib primitives (box, cyl, lathe, tube ...) can be mixed in: finalize() joins every mesh object in the scene.
Never modifies kitlib / v4util files; the marker table is extended at runtime only.
"""
import math
import bmesh
import bpy
from mathutils import Vector, Matrix, Euler
import kitlib
import v4util

# ---- extra marker names (material key -> metadata key); registered at runtime
for _k, _m in (('mk_enda', 'end_a'), ('mk_endb', 'end_b'), ('mk_hingel', 'hinge_l'), ('mk_hinger', 'hinge_r'), ('mk_spawn', 'spawn')):
    kitlib.PAL[_k] = ((255, 0, 255), 'SmoothPlastic', 0.0, 1.0, 0)
    v4util.MARKS[_k] = _m


def polar(r, deg, z=0.0):
    a = math.radians(deg)
    return (r * math.cos(a), r * math.sin(a), z)


AUTO_BEVEL = True
DETAIL = 1.9        # multiplies chunk counts of piles, spires, cliffs and arches (more, smaller facets = a richer rock silhouette)
_MAN = {}


def _manifest():
    if not _MAN:
        import csv
        with open(r"C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5\V5_MANIFEST.csv", encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                _MAN[r['id']] = r
    return _MAN


def ids(*rows):
    """Exact manifest ids of the given rows, in manifest order."""
    want = set(rows)
    return [r['id'] for r in _manifest().values() if r['row'] in want]


def autofit(ob, mid, tol=0.08):
    """Scale a finished model so each axis lands on its manifest size when it is off by more than tol (briefs: x, HEIGHT, depth)."""
    row = _manifest().get(mid)
    if not row:
        return ob
    sx, sh, sd = float(row['size_x']), float(row['size_y']), float(row['size_z'])
    if sx <= 0 or sh <= 0 or sd <= 0:
        return ob
    dm = ob.dimensions
    off = lambda got, want: abs(got - want) / want > tol
    return fit(ob, w=sx if off(dm.x, sx) else None, d=sd if off(dm.y, sd) else None, h=sh if off(dm.z, sh) else None)


def fitted(mid, fn, tol=0.08):
    """Wrap a builder so its result is autofitted to the manifest size of mid."""
    def run():
        return autofit(fn(), mid, tol)
    return run


def mk(rows, tol=0.08):
    """[(id, builder), ...] -> [(id, fitted builder), ...] for a BATCHES entry."""
    return [(mid, fitted(mid, fn, tol)) for mid, fn in rows]


def fit(ob, w=None, d=None, h=None):
    """Scale a finished model (origin at bottom centre) to a target width (x), depth (y) and height (z); None keeps that axis."""
    dm = ob.dimensions
    sx = (w / dm.x) if w and dm.x > 1e-6 else 1.0
    sy = (d / dm.y) if d and dm.y > 1e-6 else 1.0
    sz = (h / dm.z) if h and dm.z > 1e-6 else 1.0
    for v in ob.data.vertices:
        v.co.x *= sx
        v.co.y *= sy
        v.co.z *= sz
    ob.data.update()
    return ob


def tang(deg):
    a = math.radians(deg)
    return (-math.sin(a), math.cos(a))


def band(keys, t, rnd=None, wobble=0.06):
    """Colour key for a rock chunk at height fraction t (0 = bottom, 1 = top): graded bands instead of random patches.
    wobble shifts the band edge a little per chunk so the edge is not a ruler-straight line."""
    n = len(keys)
    if n == 1:
        return keys[0]
    if rnd is not None:
        t += rnd.uniform(-wobble, wobble)
    return keys[max(0, min(n - 1, int(t * n)))]


def strata(keys, k, thick=2):
    """Repeating horizontal strata: layer index k -> key, `thick` layers per band (every column gets the same band at the same height)."""
    return keys[(k // thick) % len(keys)]


class Acc:
    def __init__(self):
        self.bms = {}

    def _bm(self, key):
        bm = self.bms.get(key)
        if bm is None:
            bm = self.bms[key] = bmesh.new()
        return bm

    @staticmethod
    def M(loc=(0, 0, 0), rot=(0, 0, 0)):
        return Matrix.Translation(Vector(loc)) @ Euler([math.radians(a) for a in rot], 'XYZ').to_matrix().to_4x4()

    # ---------------------------------------------------------- solids
    def _box_m(self, size, M, key):
        sx, sy, sz = size[0] / 2.0, size[1] / 2.0, size[2] / 2.0
        bm = self._bm(key)
        v = [bm.verts.new(M @ Vector(p)) for p in (
            (-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz),
            (-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz))]
        for a, b, c, d in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
            bm.faces.new((v[a], v[b], v[c], v[d]))

    def box(self, size, loc=(0, 0, 0), key='stone', rot=(0, 0, 0), bev=None):
        """Box centred on loc. rot = Euler XYZ degrees (X first, then Y, then Z). Edges are chamfered automatically
        (bev=None -> 12% of the smallest side, at most 0.22; bev=0 -> sharp) so light catches the corners like the run-1 models."""
        M = self.M(loc, rot)
        m = min(size)
        if bev is None:
            bev = min(0.22, 0.12 * m) if m >= 0.9 else 0.0
        bev = min(bev, m * 0.45)
        if AUTO_BEVEL and bev > 0.02:
            self._box_bev(size, M, key, bev)
        else:
            self._box_m(size, M, key)

    def _box_bev(self, size, M, key, bev):
        tmp = bmesh.new()
        bmesh.ops.create_cube(tmp, size=1.0)
        bmesh.ops.scale(tmp, vec=Vector(size), verts=tmp.verts)
        bmesh.ops.bevel(tmp, geom=list(tmp.edges), offset=bev, offset_type='OFFSET', segments=1, profile=0.5, affect='EDGES')
        bmesh.ops.transform(tmp, matrix=M, verts=tmp.verts)
        bm = self._bm(key)
        vmap = {v: bm.verts.new(v.co) for v in tmp.verts}
        for f in tmp.faces:
            bm.faces.new([vmap[v] for v in f.verts])
        tmp.free()

    def beam(self, p0, p1, w, h, key, up=(0, 0, 1)):
        """Box of cross-section w x h running from p0 to p1 (w horizontal-ish, h along 'up')."""
        p0 = Vector(p0)
        p1 = Vector(p1)
        d = p1 - p0
        L = d.length
        if L < 1e-6:
            return
        x = d / L
        y = Vector(up).cross(x)
        if y.length < 1e-6:
            y = Vector((0, 1, 0)).cross(x)
        y.normalize()
        z = x.cross(y)
        R = Matrix(((x.x, y.x, z.x, 0), (x.y, y.y, z.y, 0), (x.z, y.z, z.z, 0), (0, 0, 0, 1)))
        self._box_m((L, w, h), Matrix.Translation((p0 + p1) / 2.0) @ R, key)

    def frustum(self, base, top, h, loc=(0, 0, 0), key='stone', rot=(0, 0, 0), off=(0.0, 0.0)):
        """Rectangular frustum standing on its base at loc: base=(w,d), top=(w,d), top centre shifted by off (pyramid: top=(0.02,0.02))."""
        M = self.M(loc, rot)
        bm = self._bm(key)
        bw, bd = base[0] / 2.0, base[1] / 2.0
        tw, td = max(top[0], 0.02) / 2.0, max(top[1], 0.02) / 2.0
        v = [bm.verts.new(M @ Vector(p)) for p in (
            (-bw, -bd, 0), (bw, -bd, 0), (bw, bd, 0), (-bw, bd, 0),
            (-tw + off[0], -td + off[1], h), (tw + off[0], -td + off[1], h), (tw + off[0], td + off[1], h), (-tw + off[0], td + off[1], h))]
        for a, b, c, d in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
            bm.faces.new((v[a], v[b], v[c], v[d]))

    def gable(self, w, d, h, loc=(0, 0, 0), key='roof', rot=(0, 0, 0), ridge_off=0.0):
        """Gable roof prism: eaves width w (x), depth d (y), ridge height h; standing on its base at loc, ridge along Y."""
        M = self.M(loc, rot)
        bm = self._bm(key)
        v = []
        for y in (-d / 2.0, d / 2.0):
            v.append([bm.verts.new(M @ Vector(p)) for p in ((-w / 2.0, y, 0), (w / 2.0, y, 0), (ridge_off, y, h))])
        f, b = v
        bm.faces.new((f[0], f[2], f[1]))
        bm.faces.new((b[0], b[1], b[2]))
        bm.faces.new((f[0], f[1], b[1], b[0]))
        bm.faces.new((f[1], f[2], b[2], b[1]))
        bm.faces.new((f[2], f[0], b[0], b[2]))

    def cyl(self, r, h, loc=(0, 0, 0), key='stone', verts=16, r2=None, rot=(0, 0, 0), start=0.0):
        """Cylinder or cone standing on its base at loc (r2=0 -> pointed cone)."""
        r2 = r if r2 is None else r2
        M = self.M(loc, rot)
        bm = self._bm(key)
        n = max(3, verts)
        bot, top = [], []
        for i in range(n):
            a = math.radians(start + 360.0 * i / n)
            c, s = math.cos(a), math.sin(a)
            bot.append(bm.verts.new(M @ Vector((r * c, r * s, 0))))
            if r2 > 1e-6:
                top.append(bm.verts.new(M @ Vector((r2 * c, r2 * s, h))))
        bm.faces.new(list(reversed(bot)))
        if r2 > 1e-6:
            bm.faces.new(top)
            for i in range(n):
                j = (i + 1) % n
                bm.faces.new((bot[i], bot[j], top[j], top[i]))
        else:
            apex = bm.verts.new(M @ Vector((0, 0, h)))
            for i in range(n):
                bm.faces.new((bot[i], bot[(i + 1) % n], apex))

    def ball(self, r, loc=(0, 0, 0), key='stone', segs=12, rings=8, scale=(1, 1, 1), rot=(0, 0, 0)):
        M = self.M(loc, rot)
        bm = self._bm(key)
        sx, sy, sz = scale
        top = bm.verts.new(M @ Vector((0, 0, r * sz)))
        bot = bm.verts.new(M @ Vector((0, 0, -r * sz)))
        rs = []
        for j in range(1, rings):
            ph = math.pi * j / rings
            sp, cp = math.sin(ph), math.cos(ph)
            rs.append([bm.verts.new(M @ Vector((r * sp * math.cos(2 * math.pi * i / segs) * sx,
                                                 r * sp * math.sin(2 * math.pi * i / segs) * sy, r * cp * sz))) for i in range(segs)])
        for i in range(segs):
            j = (i + 1) % segs
            bm.faces.new((top, rs[0][i], rs[0][j]))
            bm.faces.new((bot, rs[-1][j], rs[-1][i]))
            for k in range(len(rs) - 1):
                bm.faces.new((rs[k][i], rs[k + 1][i], rs[k + 1][j], rs[k][j]))

    def prism(self, pts2d, h, loc=(0, 0, 0), key='stone', rot=(0, 0, 0), z0=0.0):
        """Extrude a 2D outline (x, y) upward by h."""
        M = self.M(loc, rot)
        bm = self._bm(key)
        bot = [bm.verts.new(M @ Vector((x, y, z0))) for x, y in pts2d]
        top = [bm.verts.new(M @ Vector((x, y, z0 + h))) for x, y in pts2d]
        n = len(pts2d)
        bm.faces.new(list(reversed(bot)))
        bm.faces.new(top)
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new((bot[i], bot[j], top[j], top[i]))

    def revolve(self, profile, loc=(0, 0, 0), key='stone', segs=16, rot=(0, 0, 0), sx=1.0, sy=1.0, start=0.0):
        """Solid of revolution from a (radius, z) profile, bottom to top; radius 0 = pole."""
        M = self.M(loc, rot)
        bm = self._bm(key)
        rings = []
        for (r, z) in profile:
            if r < 1e-5:
                rings.append([bm.verts.new(M @ Vector((0, 0, z)))])
            else:
                rings.append([bm.verts.new(M @ Vector((math.cos(math.radians(start) + 2 * math.pi * i / segs) * r * sx,
                                                        math.sin(math.radians(start) + 2 * math.pi * i / segs) * r * sy, z)))
                              for i in range(segs)])
        for P, Q in zip(rings, rings[1:]):
            if len(P) == 1 and len(Q) == 1:
                continue
            if len(P) == 1:
                for i in range(segs):
                    bm.faces.new((P[0], Q[i], Q[(i + 1) % segs]))
            elif len(Q) == 1:
                for i in range(segs):
                    bm.faces.new((P[i], Q[0], P[(i + 1) % segs]))
            else:
                for i in range(segs):
                    bm.faces.new((P[i], P[(i + 1) % segs], Q[(i + 1) % segs], Q[i]))
        if len(rings[0]) > 1:
            bm.faces.new(list(reversed(rings[0])))
        if len(rings[-1]) > 1:
            bm.faces.new(rings[-1])

    def sweep(self, poly, a0=0.0, a1=360.0, n=None, key='stone', loc=(0, 0, 0), rot=(0, 0, 0)):
        """Sweep a closed (r, z) cross-section around Z from a0 to a1 degrees (360 = closed ring, else end caps)."""
        full = abs(a1 - a0) >= 359.99
        if n is None:
            n = max(1, int(math.ceil(abs(a1 - a0) / 7.5)))
        M = self.M(loc, rot)
        bm = self._bm(key)
        m = len(poly)
        cnt = n if full else n + 1
        rings = []
        for i in range(cnt):
            a = math.radians(a0 + (a1 - a0) * i / n)
            c, s = math.cos(a), math.sin(a)
            rings.append([bm.verts.new(M @ Vector((r * c, r * s, z))) for (r, z) in poly])
        for i in range(n):
            P = rings[i]
            Q = rings[(i + 1) % cnt]
            for j in range(m):
                bm.faces.new((P[j], P[(j + 1) % m], Q[(j + 1) % m], Q[j]))
        if not full:
            bm.faces.new(list(reversed(rings[0])))
            bm.faces.new(rings[-1])

    def ring_wall(self, r_in, r_out, z0, z1, openings, key, step_deg=6.0):
        """Round wall with real openings. openings = [(centre_deg, width_studs, [(z_lo, z_hi), ...]), ...] (tiers bottom to top)."""
        rm = (r_in + r_out) / 2.0
        poly = lambda za, zb: [(r_in, za), (r_out, za), (r_out, zb), (r_in, zb)]

        def seg(a0, a1, za, zb):
            if zb - za < 1e-4 or a1 - a0 < 1e-4:
                return
            n = max(1, int(math.ceil((a1 - a0) / step_deg)))
            self.sweep(poly(za, zb), a0, a1, n, key)

        ops = sorted(openings, key=lambda o: o[0] % 360.0)
        if not ops:
            self.sweep(poly(z0, z1), 0, 360, int(360 / step_deg), key)
            return
        for i, (c, w, tiers) in enumerate(ops):
            hw = math.degrees((w / 2.0) / rm)
            c = c % 360.0
            nc, nw, _ = ops[(i + 1) % len(ops)]
            nc = nc % 360.0
            if i == len(ops) - 1:
                nc += 360.0
            nhw = math.degrees((nw / 2.0) / rm)
            seg(c + hw, nc - nhw, z0, z1)
            zs = [z0] + [t for pair in tiers for t in pair] + [z1]
            for k in range(0, len(zs), 2):
                seg(c - hw, c + hw, zs[k], zs[k + 1])

    def chunk(self, size, loc=(0, 0, 0), key='stone', rot=(0, 0, 0), jit=0.16, rnd=None, taper=(1.0, 1.0)):
        """Angular rock chunk: a box with jittered corners (the 'facet' look). taper scales the top face."""
        import random as _r
        rnd = rnd or _r
        sx, sy, sz = size[0] / 2.0, size[1] / 2.0, size[2] / 2.0
        M = self.M(loc, rot)
        bm = self._bm(key)
        v = []
        for iz, z in enumerate((-sz, sz)):
            tx, ty = taper if iz else (1.0, 1.0)
            for (x, y) in ((-sx, -sy), (sx, -sy), (sx, sy), (-sx, sy)):
                v.append(bm.verts.new(M @ Vector((x * tx + rnd.uniform(-jit, jit) * size[0], y * ty + rnd.uniform(-jit, jit) * size[1],
                                                  z + rnd.uniform(-jit, jit) * size[2]))))
        for a, b, c, d in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
            bm.faces.new((v[a], v[b], v[c], v[d]))

    def mound(self, cx, cy, w, d, h, n, keys, rnd, z0=0.0, cmin=0.35, cmax=0.7, jit=0.16):
        """Heap of angular chunks over an area w x d up to height h: big chunks low, small high."""
        n = max(1, int(round(n * DETAIL)))
        for i in range(n):
            t = i / max(1, n - 1)
            s = rnd.uniform(cmin, cmax) * (1.0 - 0.45 * t)
            x = cx + rnd.uniform(-0.5, 0.5) * w * (1.0 - 0.6 * t)
            y = cy + rnd.uniform(-0.5, 0.5) * d * (1.0 - 0.6 * t)
            z = z0 + t * h * 0.82
            self.chunk((w * s, d * s * rnd.uniform(0.8, 1.2), h * s * 0.9), (x, y, z + h * s * 0.3), band(keys, t, rnd),
                       (0, 0, rnd.uniform(0, 90)), jit, rnd, (rnd.uniform(0.7, 1.0), rnd.uniform(0.7, 1.0)))

    def append(self, other, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        """Copy another Acc's geometry into this one, scaled (negative = mirrored), rotated by rot (Euler XYZ degrees) and moved by loc."""
        M = self.M(loc, rot) @ Matrix.Diagonal(Vector((scale[0], scale[1], scale[2], 1.0)))
        for key, obm in other.bms.items():
            bm = self._bm(key)
            vmap = {v: bm.verts.new(M @ v.co) for v in obm.verts}
            for f in obm.faces:
                bm.faces.new([vmap[v] for v in f.verts])

    # ---------------------------------------------------------- finish
    def to_scene(self, keep_normals=()):
        """Turn the accumulated meshes into scene objects (one per palette key); finalize() then joins them.
        keep_normals: palette keys whose faces are already wound correctly (open surfaces like terrain relief)."""
        for key, bm in self.bms.items():
            if len(bm.faces) == 0:
                bm.free()
                continue
            if key not in keep_normals:
                bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            kitlib._obj_from_bm('acc_' + key, bm, key)
        self.bms = {}


# ------------------------------------------------------------------ the wizard tower: numbers shared by WT01, WT02 and the collision file
TOWER = {
    'floors': [0, 40, 72, 104, 136, 168, 200, 232],      # floor height of level i (level 0 is the double-height Map Hall)
    'top_deck': 264,                                     # top of level 7 (the crown starts here)
    'height': 300.0,
    'outer_d': [110, 110, 96, 88, 80, 70, 64, 52],       # outer drum diameter per level (walls are 6 thick)
    'wall': 6.0,
    'slots': [8, 8, 6, 6, 5, 4, 4, 3],                   # window slots per level (level 0 slot 0 is the front door)
    'twist': 7.0,                                        # each level is turned this many degrees against the one below
    'front_deg': 270.0,                                  # front = -Y
}


def tower_top(i):
    f = TOWER['floors']
    return f[i + 1] if i + 1 < len(f) else TOWER['top_deck']


def tower_openings(i):
    """Window layout of level i, identical to WT01: (ops for ring_wall, window centre angles, absolute (z_lo, z_hi) tiers)."""
    F, N = TOWER['floors'], TOWER['slots']
    z0 = F[i]
    front = TOWER['front_deg']
    base = front + TOWER['twist'] * i
    step = 360.0 / N[i]
    tiers = [(z0 + 10.0, z0 + 18.0), (z0 + 26.0, z0 + 34.0)] if i == 0 else [(z0 + 12.0, z0 + 20.0)]
    ops, wins = [], []
    if i == 0:
        ops.append((front, 11.0, [(0.0, 13.0)]))
    for k in range(N[i]):
        if i == 0 and k == 0:
            continue
        ang = base + (k * step if i == 0 else (k + 0.5) * step)
        wins.append(ang)
        ops.append((ang, 14.0, list(tiers)))
    return ops, wins, tiers


WIZ = {
    'granite': ((176, 172, 180), 'Granite', 0.0, 0.92),
    'limestone': ((226, 214, 190), 'Limestone', 0.0, 0.88),
    'white': ((238, 234, 226), 'Concrete', 0.0, 0.90),
    'ochre': ((196, 150, 76), 'WoodPlanks', 0.0, 0.80),
    'timber': ((112, 60, 48), 'Wood', 0.0, 0.85),
    'indigo': ((52, 60, 96), 'Slate', 0.0, 0.75),
    'copper': ((92, 150, 128), 'Metal', 0.45, 0.55),
    'brass': ((200, 164, 84), 'Metal', 0.80, 0.35),
    'parchment': ((226, 208, 170), 'Fabric', 0.0, 0.95),
}


def wiz_pal(prefix):
    """Register the wizard palette under <prefix>_<name> (emission always 0)."""
    for k, (rgb, m, met, rough) in WIZ.items():
        kitlib.PAL[f'{prefix}_{k}'] = (rgb, m, met, rough, 0)
