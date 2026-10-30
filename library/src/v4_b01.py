"""B01 - demon-remains skull headquarters (1 model, 220 x 148 x 265).
Round cranium, two big eye sockets (open to the inside), a recessed third eye, curled ridged ram horns, side spikes and teeth.
Hollow interior with a floor, dais and a bone chandelier. The only walk-in entrance is through the lower jaw (mouth gap).
Built as: soft union of ellipsoids (voxel remesh) -> hollow shell (solidify) -> boolean cuts -> faces coloured by depth.
rot args of kitlib shape helpers are DEGREES.
"""
import math, random, bpy, bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, _obj_from_bm, mat
from v4_elf import nm, lantern
from v4_d04 import prism_xz
from nature import blob

PI = math.pi


# ------------------------------------------------------------------ mesh helpers
def _eval_mesh(obj):
    dg = bpy.context.evaluated_depsgraph_get()
    return bpy.data.meshes.new_from_object(obj.evaluated_get(dg))


def bake(obj):
    me = _eval_mesh(obj)
    old = obj.data
    obj.modifiers.clear()
    obj.data = me
    bpy.data.meshes.remove(old)
    return obj


def join(objs, name, keys):
    bm = bmesh.new()
    for o in objs:
        me = _eval_mesh(o)
        me.transform(o.matrix_world)
        bm.from_mesh(me)
        bpy.data.meshes.remove(me)
    for o in objs:
        bpy.data.objects.remove(o, do_unlink=True)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for k in keys:
        me.materials.append(mat(k))
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def _info(tag, o):
    vs = [v.co for v in o.data.vertices]
    if not vs:
        print(tag, 'EMPTY')
        return
    mn = [round(min(v[i] for v in vs), 1) for i in range(3)]
    mx = [round(max(v[i] for v in vs), 1) for i in range(3)]
    print(tag, len(o.data.vertices), len(o.data.polygons), mn, mx)


DEBUG = False
DEC = 0.2


def cut(obj, cutter):
    m = obj.modifiers.new('bool', 'BOOLEAN')
    m.operation = 'DIFFERENCE'
    m.operand_type = 'OBJECT'
    m.object = cutter
    m.solver = 'EXACT'
    m.use_self = True
    m.use_hole_tolerant = True
    bake(obj)
    bpy.data.objects.remove(cutter, do_unlink=True)
    if DEBUG:
        _info('  cut', obj)


def hide_cutter(o):
    return o


def ray(bvh, origin, direction):
    hit = bvh.ray_cast(Vector(origin), Vector(direction).normalized())
    return hit[0] if hit and hit[0] is not None else None


def catmull(pts, n):
    P = [Vector(p) for p in pts]
    P = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
    out = []
    segs = len(P) - 3
    for i in range(n):
        u = i / (n - 1) * segs
        s = min(int(u), segs - 1)
        t = u - s
        p0, p1, p2, p3 = P[s], P[s + 1], P[s + 2], P[s + 3]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    return out


def sweep(name, ctrl, rfn, key, n=64, sides=12, ridges=0, ridge_amp=0.0, flat=1.0):
    P = catmull(ctrl, n)
    bm = bmesh.new()
    rings = []
    Nv = None
    for i, p in enumerate(P):
        a = P[max(0, i - 1)]
        b = P[min(len(P) - 1, i + 1)]
        T = (b - a).normalized()
        if Nv is None:
            Nv = T.cross(Vector((0, 0, 1)))
            if Nv.length < 1e-3:
                Nv = T.cross(Vector((1, 0, 0)))
            Nv.normalize()
        else:
            Nv = (Nv - T * Nv.dot(T)).normalized()
        B = T.cross(Nv)
        t = i / (n - 1)
        r = rfn(t)
        if ridges:
            f = (t * ridges) % 1.0
            r *= 1 + ridge_amp * (1.0 - 2.0 * f) * (1.0 if t > 0.06 else 0.0)
        ring = []
        for k in range(sides):
            ang = 2 * PI * k / sides
            ring.append(bm.verts.new(p + (Nv * math.cos(ang) * flat + B * math.sin(ang)) * r))
        rings.append(ring)
    for A, B_ in zip(rings, rings[1:]):
        for k in range(sides):
            bm.faces.new((A[k], A[(k + 1) % sides], B_[(k + 1) % sides], B_[k]))
    c0 = bm.verts.new(P[0] - (P[1] - P[0]).normalized() * rfn(0) * 0.3)
    c1 = bm.verts.new(P[-1] + (P[-1] - P[-2]).normalized() * 0.5)
    for k in range(sides):
        bm.faces.new((rings[0][(k + 1) % sides], rings[0][k], c0))
        bm.faces.new((rings[-1][k], rings[-1][(k + 1) % sides], c1))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj_from_bm(name, bm, key)


def spike(base, direction, length, r, key, verts=8):
    o = cyl(nm('sp'), r, length, loc=tuple(base), key=key, verts=verts, r2=r * 0.06)
    o.rotation_euler = Vector(direction).normalized().to_track_quat('Z', 'Y').to_euler()
    return o


def tooth(base, direction, length, r, key='sk_tooth'):
    o = cyl(nm('th'), r, length, loc=tuple(base), key=key, verts=6, r2=r * 0.12)
    o.rotation_euler = Vector(direction).normalized().to_track_quat('Z', 'Y').to_euler()
    return o


def ell(c, r, seed, key='sk_bone', amp=0.025):
    return blob(nm('el'), 1.0, c, key, subdiv=4, amp=amp, freq=1.3, scale=r, seed=seed)



# ------------------------------------------------------------------ the skull
def surface_pt(bvh, x, y, z0=300.0, lift=0.5):
    h = ray(bvh, (x, y, z0), (0, 0, -1))
    return (x, y, h.z + lift) if h else None


def skull_hq():
    reset()
    rnd = random.Random(1101)
    T = 6.0  # wall thickness
    CY = -20.0  # interior centre (y) for the floor and dais
    # 1. soft union of ellipsoids
    parts = [
        ell((0, 38, 20), (30, 26, 40), 1),            # neck stump under the skull
        ell((0, 14, 108), (68, 62, 62), 2),           # cranium
        ell((0, -14, 124), (56, 40, 46), 3),          # forehead
        ell((-27, -38, 128), (26, 14, 8), 4),         # brow ridges, one over each eye
        ell((27, -38, 128), (26, 14, 8), 16),
        ell((0, -42, 120), (14, 11, 11), 17),         # glabella
        ell((-46, -38, 88), (17, 20, 13), 5),         # cheekbones
        ell((46, -38, 88), (17, 20, 13), 6),
        ell((-56, -18, 94), (7, 26, 8), 11),          # zygomatic arches
        ell((56, -18, 94), (7, 26, 8), 12),
        ell((0, -34, 78), (46, 36, 34), 7),           # maxilla
        ell((0, -26, 50), (42, 30, 16), 18),          # mid face, joins jaw and maxilla
        ell((0, -20, 14), (54, 44, 28), 8),           # lower jaw
        ell((0, -54, 8), (28, 16, 16), 9),            # chin
    ]
    body = join(parts, 'skull_body', ['sk_bone', 'sk_inner', 'sk_bone_dark', 'sk_void'])
    rm = body.modifiers.new('rm', 'REMESH')
    rm.mode = 'VOXEL'
    rm.voxel_size = 1.9
    rm.adaptivity = 0.0
    bake(body)
    sm = body.modifiers.new('sm', 'SMOOTH')
    sm.factor = 0.5
    sm.iterations = 10
    bake(body)
    dc = body.modifiers.new('dc', 'DECIMATE')
    dc.decimate_type = 'COLLAPSE'
    dc.ratio = DEC
    dc.use_collapse_triangulate = True
    bake(body)
    groove = box(nm('gv'), (96, 40, 5.5), loc=(0, -70, 40.5), key='sk_bone')
    cut(body, groove)
    bm_ref = bmesh.new()
    bm_ref.from_mesh(body.data)
    bvh = BVHTree.FromBMesh(bm_ref)
    # 2. hollow shell
    so = body.modifiers.new('so', 'SOLIDIFY')
    so.thickness = T
    so.offset = -1.0
    so.use_even_offset = True
    so.use_quality_normals = True
    bake(body)
    # 3. cuts: flat base, doorway, eye sockets, nose, third eye recess
    cut(body, box(nm('cb'), (400, 400, 60), loc=(0, 0, -30), key='sk_bone'))
    W = 22.0
    door_pts = [(-W, 0), (W, 0), (W, 20)] + [(W * math.cos(PI * i / 14), 20 + 20 * math.sin(PI * i / 14)) for i in range(1, 14)] + [(-W, 20)]
    cut(body, prism_xz(door_pts, -110, -28, 'sk_bone'))
    for sx in (-1, 1):
        cut(body, cyl(nm('eye'), 17.5, 90, loc=(sx * 28, -100, 106), key='sk_bone', verts=26, rot=(-90, 0, 0), r2=14.0))
    cut(body, prism_xz([(0, 106), (-13, 76), (-5, 72), (5, 72), (13, 76)], -110, -28, 'sk_bone'))
    hit = ray(bvh, (0, -140, 152), (0, 1, 0))
    third = hit + Vector((0, -6.5, 0)) if hit else Vector((0, -55, 152))
    cut(body, ball(nm('t3'), 11.0, tuple(third), 'sk_bone', segs=20, rings=12))
    # 4. colour faces by depth below the outer surface: outside / inside / cut faces
    me = body.data
    for p in me.polygons:
        loc, n, idx, d = bvh.find_nearest(p.center)
        p.material_index = 0 if d < 0.9 else (1 if d > T - 0.9 else 2)
        c = p.center
        if p.material_index == 0 and abs(c.x) < 48.5 and c.y < -44.0 and 37.4 < c.z < 43.6:
            p.material_index = 3  # dark mouth slot
    me.update()
    # 5. sutures along the cranium, projected onto the surface
    def seam(pts, r=0.8):
        P = [surface_pt(bvh, x, y) for (x, y) in pts]
        P = [p for p in P if p]
        if len(P) > 3:
            tube(nm('sut'), P, r, 'sk_bone_dark', res=4, ures=1)
    seam([(x, -6 + 5 * math.sin(x * 0.42)) for x in range(-56, 57, 4)])
    seam([(2.5 * math.sin(y * 0.45), y) for y in range(-6, 70, 3)])
    seam([(x, 52 + 5 * math.sin(x * 0.38 + 1.0)) for x in range(-44, 45, 4)])
    bm_ref.free()
    # 6. horns (ridged, curled), collars and side spikes
    for sx in (-1, 1):
        ctrl = [(sx * 56, 22, 134), (sx * 80, 20, 137), (sx * 98, 14, 160), (sx * 102, 6, 196), (sx * 93, 0, 232), (sx * 77, -4, 256), (sx * 66, -5, 263)]
        sweep(nm('horn'), ctrl, lambda t: 13.0 * (1 - t) ** 0.85 + 0.7, 'sk_horn', n=84, sides=14, ridges=11, ridge_amp=0.075)
        sweep(nm('hornt'), ctrl[3:], lambda t: (4.8 * (1 - t) ** 0.9 + 0.4) * 1.02, 'sk_horn_light', n=40, sides=12, ridges=4, ridge_amp=0.06)
        ball(nm('hc'), 16.0, (sx * 59, 21, 135), 'sk_bone_dark', segs=18, rings=10, scale=(0.8, 1.0, 1.0))
    # 7. teeth and spikes: ray-cast onto the outer surface
    bm2 = bmesh.new()
    me_body = _eval_mesh(body)
    bm2.from_mesh(me_body)
    bpy.data.meshes.remove(me_body)
    bvh2 = BVHTree.FromBMesh(bm2)
    for sx in (-1, 1):
        for z0, yy, ln, rr, back in ((66, 26, 64, 7.0, 0.7), (84, 24, 54, 6.2, 0.6), (102, 22, 44, 5.4, 0.5)):
            h = ray(bvh2, (sx * 220, yy, z0), (-sx, 0, 0))
            if h:
                spike(Vector((h.x - sx * 3.0, h.y, h.z)), (sx * 0.8, back, 0.16), ln, rr, 'sk_bone_dark')
    for z0, upper, xs in ((44.0, True, (38.5, 45.0)), (37.0, False, (26.5, 35.0, 43.0))):
        for ax in xs:
            for sx in (-1, 1):
                x = sx * ax
                h = ray(bvh2, (x, -240, z0), (0, 1, 0))
                if not h:
                    continue
                ln = rnd.uniform(15, 22)
                rr = rnd.uniform(3.6, 4.8)
                if upper:
                    tooth(Vector((h.x, h.y + 1.5, z0 - 0.5)), (0, -0.08, -1), ln, rr)
                else:
                    tooth(Vector((h.x, h.y + 1.5, z0 + 0.5)), (0, -0.05, 1), ln * 0.85, rr * 0.95)
    for sx in (-1, 1):  # two big fangs flanking the doorway
        h = ray(bvh2, (sx * (W + 8.0), -240, 44.0), (0, 1, 0))
        if h:
            tooth(Vector((h.x, h.y + 1.5, 43.5)), (0, -0.05, -1), 38.0, 6.0)
    bm2.free()
    # 8. third eye pupil and brow ring
    ball(nm('pup'), 7.2, tuple(third + Vector((0, 3.6, 0))), 'sk_void', segs=16, rings=10)
    torus(nm('tring'), 11.0, 1.9, loc=tuple(third + Vector((0, 1.0, 0))), key='sk_bone_dark', segs=24, rsegs=6, rot=(90, 0, 0))
    # 9. interior: floor, dais with rune rings, bone chandelier hanging in the cranium
    ball(nm('flr'), 1.0, (0, CY, 0), 'sk_floor', segs=40, rings=8, scale=(38, 30, 1.6))
    cyl(nm('dais'), 17, 3.2, loc=(0, CY, 1.2), key='sk_floor', verts=28, bev=0.3)
    torus(nm('rn1'), 21.0, 0.6, loc=(0, CY, 1.6), key='sk_rune', segs=40, rsegs=4)
    torus(nm('rn2'), 12.0, 0.5, loc=(0, CY, 4.5), key='sk_rune', segs=32, rsegs=4)
    ring_z = 112.0
    CC = -2.0
    torus(nm('chd'), 11.0, 0.8, loc=(0, CC, ring_z), key='bronze', segs=32, rsegs=5)
    for k in range(3):
        a = 2 * PI * k / 3 + 0.4
        tube(nm('chn'), [(math.cos(a) * 11, CC + math.sin(a) * 11, ring_z), (math.cos(a) * 7, CC + math.sin(a) * 7, ring_z + 12), (0, CC, ring_z + 22)], 0.3, 'bronze', res=4, ures=2)
    for k in range(6):
        a = 2 * PI * k / 6
        lantern(math.cos(a) * 11, CC + math.sin(a) * 11, ring_z - 0.9 * 1.7, 1.7, hang=True)
    return finalize('skull_hq', smooth_angle=38)


BATCH_B01 = [
    ('B01_01_skull_hq_01', skull_hq, (0.6, -1.3, 0.3)),
]
