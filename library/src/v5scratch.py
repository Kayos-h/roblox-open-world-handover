"""v5scratch - SCRATCH build of v5 models in a HEADLESS Blender: builds the requested ids from a module, prints a numbers check, and renders a
four-angle sheet per model to library\\v5_work\\fix_scratch\\<tag>\\<id>.png. Writes NOTHING to the model library, the metas or the palette files,
and never touches the open Blender.
  blender -b --factory-startup --python v5scratch.py -- <module> <id,id|-> <outdir> <res> <views 1-4> <samples>
Numbers printed per model (line starts with SCRATCH):
  tris, size vs manifest, flags (SIZE, TRIS, LOW, EMPTY), FLOAT = clusters of parts that touch neither the ground nor the main body (what the reviewers call
  'floating or detached parts'), INV = closed parts with inverted faces (render black), build seconds, markers.
"""
import sys
import os
import time
import math
import traceback
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
import numpy as np
import bpy
import kitlib
import v4util
import v5live
import v5liverun

MOD, IDS, OUT = argv[0], [i for i in argv[1].split(',') if i and i not in ('-', 'ALL')], argv[2]
RES = int(argv[3]) if len(argv) > 3 else 360
VIEWS = max(1, min(4, int(argv[4]))) if len(argv) > 4 else 4
SAMPLES = int(argv[5]) if len(argv) > 5 else 10
os.makedirs(OUT, exist_ok=True)
v5liverun._patch_once()
_orig_setup = kitlib._setup_render


def _setup(ob, res=900):
    r = _orig_setup(ob, res)
    try:
        bpy.context.scene.cycles.samples = SAMPLES
    except Exception:
        pass
    return r


kitlib._setup_render = _setup


def _uf(n, pairs):
    p = np.arange(n)

    def find(a):
        while p[a] != a:
            p[a] = p[p[a]]
            a = p[a]
        return a
    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            p[max(ra, rb)] = min(ra, rb)
    return np.array([find(i) for i in range(n)])


SKIPPED = 0


def analyse(ob):
    """(floating clusters, inverted closed parts). Parts = connected pieces of the mesh; touching = bounding boxes overlap within 0.06 studs."""
    me = ob.data
    nv, ne = len(me.vertices), len(me.edges)
    if nv == 0:
        return [], []
    co = np.empty(nv * 3)
    me.vertices.foreach_get('co', co)
    co = co.reshape(-1, 3)
    ed = np.empty(ne * 2, dtype=np.int64)
    me.edges.foreach_get('vertices', ed)
    ed = ed.reshape(-1, 2)
    root = _uf(nv, ed.tolist())
    uniq, inv = np.unique(root, return_inverse=True)
    k = len(uniq)
    lo = np.full((k, 3), 1e9)
    hi = np.full((k, 3), -1e9)
    np.minimum.at(lo, inv, co)
    np.maximum.at(hi, inv, co)
    # inverted closed parts
    me.calc_loop_triangles()
    nt = len(me.loop_triangles)
    vol = np.zeros(k)
    tv = np.zeros((0, 3), dtype=np.int64)
    if nt:
        tv = np.empty(nt * 3, dtype=np.int64)
        me.loop_triangles.foreach_get('vertices', tv)
        tv = tv.reshape(-1, 3)
        a, b, c = co[tv[:, 0]], co[tv[:, 1]], co[tv[:, 2]]
        v6 = np.einsum('ij,ij->i', a, np.cross(b, c)) / 6.0
        np.add.at(vol, inv[tv[:, 0]], v6)
    nl = len(me.loops)
    le = np.empty(nl, dtype=np.int64)
    me.loops.foreach_get('edge_index', le)
    cnt = np.bincount(le, minlength=ne)
    open_part = np.zeros(k, dtype=bool)
    bad_e = np.where(cnt != 2)[0]
    if len(bad_e):
        open_part[inv[ed[bad_e, 0]]] = True
    boxvol = np.prod(np.maximum(hi - lo, 0.01), axis=1)
    inverted = [int(i) for i in np.where((~open_part) & (vol < -0.02 * boxvol) & (boxvol > 0.5))[0]]
    mats = []
    if inverted and len(me.materials):
        pm = np.empty(len(me.polygons), dtype=np.int64)
        me.polygons.foreach_get('material_index', pm)
        pv = np.empty(len(me.polygons) * 0 + len(me.loops), dtype=np.int64)
        me.loops.foreach_get('vertex_index', pv)
        for p in me.polygons[:0]:
            pass
        first = {}
        for poly in me.polygons:
            r = int(inv[me.loops[poly.loop_start].vertex_index])
            first.setdefault(r, poly.material_index)
        mats = sorted({me.materials[first[i]].name if i in first and first[i] < len(me.materials) else '?' for i in inverted})
    # floating clusters: candidate pairs by bounding box, then an exact surface test (triangle overlap or any vertex within tol of the other surface).
    # ground = parts that reach z <= 0.25. A cluster that is not connected to the ground through touching parts is reported.
    from mathutils.bvhtree import BVHTree
    from mathutils import Vector
    global SKIPPED
    SKIPPED = 0
    if k > 2500:
        SKIPPED = k
        return [], (len(inverted), mats)
    tol = 0.25
    cell = 4.0
    grid = {}
    for i in range(k):
        for gx in range(int((lo[i, 0] - tol) // cell), int((hi[i, 0] + tol) // cell) + 1):
            for gy in range(int((lo[i, 1] - tol) // cell), int((hi[i, 1] + tol) // cell) + 1):
                for gz in range(int((lo[i, 2] - tol) // cell), int((hi[i, 2] + tol) // cell) + 1):
                    grid.setdefault((gx, gy, gz), []).append(i)
    cand = set()
    for lst in grid.values():
        if len(lst) < 2:
            continue
        for x in range(len(lst)):
            i = lst[x]
            for y in range(x + 1, len(lst)):
                j = lst[y]
                if i != j and (lo[i] <= hi[j] + tol).all() and (lo[j] <= hi[i] + tol).all():
                    cand.add((i, j) if i < j else (j, i))
    tri_of = {}
    if nt:
        for t in range(nt):
            tri_of.setdefault(int(inv[tv[t, 0]]), []).append(t)
    cache = {}

    def part(i):
        if i not in cache:
            ts = tri_of.get(i, [])
            if not ts:
                cache[i] = (None, [])
            else:
                vs = np.unique(tv[ts].ravel())
                loc = {int(v): n for n, v in enumerate(vs)}
                verts = [Vector(co[v].tolist()) for v in vs]
                polys = [tuple(loc[int(x)] for x in tv[t]) for t in ts]
                cache[i] = (BVHTree.FromPolygons(verts, polys), verts)
        return cache[i]

    def touching(i, j):
        bi, vi = part(i)
        bj, vj = part(j)
        if bi is None or bj is None:
            return True
        if bi.overlap(bj):
            return True
        for v in vi[::max(1, len(vi) // 48)]:
            if bj.find_nearest(v, tol)[0] is not None:
                return True
        for v in vj[::max(1, len(vj) // 48)]:
            if bi.find_nearest(v, tol)[0] is not None:
                return True
        return False
    pairs = [(i, j) for (i, j) in cand if touching(i, j)]
    comp = _uf(k, pairs)
    ground = {int(comp[i]) for i in range(k) if lo[i, 2] <= 0.25}
    clusters = {}
    for i in range(k):
        c = int(comp[i])
        if c in ground:
            continue
        d = clusters.setdefault(c, [np.full(3, 1e9), np.full(3, -1e9), 0])
        d[0] = np.minimum(d[0], lo[i])
        d[1] = np.maximum(d[1], hi[i])
        d[2] += 1
    floating = sorted(([tuple(round(float(a), 1) for a in (d[0] + d[1]) / 2), tuple(round(float(a), 1) for a in d[1] - d[0]), int(d[2])] for d in clusters.values()),
                      key=lambda t: -(t[1][0] * t[1][1] * t[1][2]))
    return floating, (len(inverted), mats)


def find_items():
    mod = v5live.load(MOD)
    found = {}
    for bn, (cat, items) in mod.BATCHES.items():
        for it in items:
            found[it[0]] = it[1]
    return found


items = find_items()
want = IDS or list(items)
for mid in want:
    if mid not in items:
        print('SCRATCH_NOT_FOUND', mid)
        continue
    t0 = time.time()
    try:
        ob = items[mid]()
        marks = v4util.extract_markers(ob)
        st = kitlib.stats(ob)
        dt = time.time() - t0
        fl, inv = analyse(ob)
        x, y, z = st['size_studs']
        row = v5live.manifest().get(mid)
        flags = []
        note = ''
        if st['tris'] < 12:
            flags.append('EMPTY')
        if row:
            sx, sh, sd = float(row['size_x']), float(row['size_y']), float(row['size_z'])
            bud = int(float(row['tri_budget']))
            note = f' want {sx:g}x{sd:g}x{sh:g} <={bud}'
            for got, w_, nm in ((x, sx, 'x'), (y, sd, 'y'), (z, sh, 'z')):
                if w_ > 0 and abs(got - w_) / w_ > 0.08:
                    flags.append('SIZE' + nm)
            if st['tris'] > bud:
                flags.append('TRIS')
            if st['tris'] < 0.12 * bud:
                flags.append('LOW')
        ftxt = 'FLOAT skipped (%d parts)' % SKIPPED if SKIPPED else ('FLOAT 0' if not fl else f'FLOAT {len(fl)} ' + ' '.join(f'[at {c} size {s} parts {n}]' for c, s, n in fl[:4]))
        itxt = 'INV 0' if not inv[0] else f'INV {inv[0]} ({",".join(inv[1][:4])})'
        out = os.path.join(OUT, mid + '.png')
        t1 = time.time()
        if VIEWS == 1:
            v4util.thumb_preview(ob, out, RES)
        else:
            d = ob.dimensions
            sz = max(d.x, d.y, d.z)
            from mathutils import Vector
            ctr = Vector((0, 0, d.z / 2))
            fpt = Vector((0, 0, d.z * 0.55))
            allv = [(ctr, (1.0, -1.25, 0.45), sz * 1.85), (ctr, (-1.0, 1.1, 0.4), sz * 1.85), (fpt, (0.9, -1.1, 0.35), sz * 0.9), (ctr, (0.0, -1.0, 0.08), sz * 2.0)]
            kitlib._setup_render(ob, RES)
            cam = bpy.context.scene.camera
            tmp = []
            for i, (tgt, v, dist) in enumerate(allv[:VIEWS]):
                dv = Vector(v).normalized()
                cam.location = tgt + dv * dist
                cam.rotation_euler = (tgt - cam.location).to_track_quat('-Z', 'Y').to_euler()
                p = os.path.join(OUT, f'_s{os.getpid()}_{i}.png')
                bpy.context.scene.render.filepath = p
                bpy.ops.render.render(write_still=True)
                tmp.append(p)
            kitlib._cleanup_render()
            kitlib.contact_sheet(tmp, out=out, cols=2, cell=RES)
            for p in tmp:
                try:
                    os.remove(p)
                except Exception:
                    pass
        print(f"SCRATCH {mid}: {st['tris']} tris, {x:g} x {y:g} x {z:g} (W x D x H){note} | {' '.join(flags) or 'ok'} | {ftxt} | {itxt} | build {dt:.1f}s render {time.time() - t1:.1f}s | mk={ {k_: len(v_) for k_, v_ in marks.items()} }")
    except Exception:
        print('SCRATCH_ERROR', mid, traceback.format_exc()[-700:].replace('\n', ' | '))
print('SCRATCH_DONE', len(want))
