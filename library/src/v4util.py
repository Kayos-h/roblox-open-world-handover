"""v4util - helpers for the v4 model batch: multi-angle previews, markers (ladders/doors), metadata, saving.
Runs inside Blender. Units: 1 unit = 1 Roblox stud. Z up in Blender. Front of a model faces -Y.
"""
import bpy, bmesh, math, os, json
import numpy as np
from mathutils import Vector
import kitlib

LIB = kitlib.LIB
META_PATH = os.path.join(LIB, 'v4_meta.json')
MARKS = {'mk_lb': 'ladder_bottom', 'mk_lt': 'ladder_top', 'mk_door': 'door', 'mk_deck': 'deck', 'mk_conn': 'connect'}


def marker(name_key, loc, size=0.3):
    """Place a tiny cube whose material encodes its meaning. Removed by extract_markers()."""
    return kitlib.box('mk_' + name_key, (size, size, size), loc=loc, key=name_key)


def extract_markers(ob):
    """Read marker positions from the finalized object, delete those faces, drop the slots.
    Returns {meaning: [(x, y, z), ...]} in the model's own coordinates (origin = bottom centre)."""
    me = ob.data
    idx_to_key = {}
    for i, m in enumerate(me.materials):
        k = m.name.split('|')[0]
        if k in MARKS:
            idx_to_key[i] = k
    out = {}
    if not idx_to_key:
        return out
    bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
    groups = {}
    for f in bm.faces:
        if f.material_index in idx_to_key:
            groups.setdefault(idx_to_key[f.material_index], []).append(f)
    for k, fl in groups.items():
        # cluster faces into cubes by connectivity of vertices
        verts = {}
        for f in fl:
            for v in f.verts:
                verts[v.index] = v
        seen, clusters = set(), []
        for vi, v in verts.items():
            if vi in seen:
                continue
            stack, comp = [v], []
            seen.add(vi)
            while stack:
                a = stack.pop(); comp.append(a)
                for e in a.link_edges:
                    b = e.other_vert(a)
                    if b.index in verts and b.index not in seen:
                        seen.add(b.index); stack.append(b)
            clusters.append(comp)
        pts = []
        for comp in clusters:
            c = sum((v.co for v in comp), Vector()) / len(comp)
            pts.append((round(c.x, 2), round(c.y, 2), round(c.z, 2)))
        out[MARKS[k]] = sorted(pts, key=lambda p: (p[2], p[0], p[1]))
    bmesh.ops.delete(bm, geom=[f for fl in groups.values() for f in fl], context='FACES')
    loose = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose, context='VERTS')
    bm.to_mesh(me); bm.free()
    # drop the marker material slots; Blender resets face material indices when slots are cleared,
    # so compute the new indices first and write them back after re-adding the slots
    keep = [i for i in range(len(me.materials)) if i not in idx_to_key]
    remap = {old: new for new, old in enumerate(keep)}
    new_idx = [remap.get(p.material_index, 0) for p in me.polygons]
    mats = [me.materials[i] for i in keep]
    me.materials.clear()
    for m in mats:
        me.materials.append(m)
    me.polygons.foreach_set('material_index', new_idx)
    me.update()
    return out


def quad_preview(ob, out, res=460, focus=None):
    """Render 4 angles into one 2x2 sheet: 3/4 front, 3/4 back, a close-up, and a side elevation.
    focus = (x, y, z, distance) aims the close-up at a detail (deck, door, ...). Default: upper-middle of the model."""
    sc = bpy.context.scene
    kitlib._setup_render(ob, res)
    cam = sc.camera
    d = ob.dimensions
    size = max(d.x, d.y, d.z)
    ctr = Vector((0, 0, d.z / 2))
    if focus is None:
        focus = (0.0, 0.0, d.z * 0.55, size * 0.9)
    fpt = Vector(focus[:3])
    views = [(ctr, (1.0, -1.25, 0.45), size * 1.85), (ctr, (-1.0, 1.1, 0.4), size * 1.85), (fpt, (0.9, -1.1, 0.35), focus[3]), (ctr, (0.0, -1.0, 0.08), size * 2.0)]
    tmp = []
    for i, (tgt, v, dist) in enumerate(views):
        dirv = Vector(v).normalized()
        cam.location = tgt + dirv * dist
        cam.rotation_euler = (tgt - cam.location).to_track_quat('-Z', 'Y').to_euler()
        p = os.path.join(LIB, 'v4_sheets', f'_q{i}.png')
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        tmp.append(p)
    kitlib._cleanup_render()
    kitlib.contact_sheet(tmp, out=out, cols=2, cell=res)
    return out


def load_meta():
    if os.path.exists(META_PATH):
        try:
            return json.load(open(META_PATH))
        except Exception:
            return {}
    return {}


def thumb_preview(ob, out, res=420, view=(1.0, -1.25, 0.45), dist=1.85):
    """One 3/4 render, used for contact sheets."""
    sc = bpy.context.scene
    kitlib._setup_render(ob, res)
    cam = sc.camera
    d = ob.dimensions
    size = max(d.x, d.y, d.z)
    ctr = Vector((0, 0, d.z / 2))
    dirv = Vector(view).normalized()
    cam.location = ctr + dirv * size * dist
    cam.rotation_euler = (ctr - cam.location).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    kitlib._cleanup_render()
    return out


def _drop_libs():
    """export_v2 loads each saved .blend as a library; release them so the file can be re-saved in the same session."""
    for lib in list(bpy.data.libraries):
        try:
            bpy.data.libraries.remove(lib)
        except Exception:
            pass
    for ob in list(bpy.data.objects):
        if ob.library is not None:
            bpy.data.objects.remove(ob, do_unlink=True)
    for me in list(bpy.data.meshes):
        if me.users == 0:
            bpy.data.meshes.remove(me)


def run_batch(items, category, sheet_name, res=420, quad=False):
    """items: list of (manifest_id, builder_fn[, view]). Builds, saves .blend/.fbx, exports per-colour FBX via export_v2,
    renders a thumb of each and writes ONE contact sheet LIB/v4_sheets/<sheet_name>.png. Returns summary rows."""
    import export_v2, traceback
    _drop_libs()
    rows, thumbs = [], []
    for it in items:
        mid, fn = it[0], it[1]
        view = it[2] if len(it) > 2 else (1.0, -1.25, 0.45)
        try:
            _drop_libs()
            ob = fn()
            marks = extract_markers(ob)
            if callable(view):   # view may be a function of the markers, e.g. aim at the ladder face
                view = view(marks)
            st = kitlib.stats(ob)
            th = thumb_preview(ob, os.path.join(LIB, 'v4_sheets', f'_t_{mid}.png'), res=res, view=view)
            if quad:
                quad_preview(ob, os.path.join(LIB, 'v4_sheets', mid + '.png'))
            kitlib.save(ob, category, mid, render_png=False)
            meta = load_meta()
            e = {'category': category, 'tris': st['tris'], 'size': list(st['size_studs']), 'materials': sorted({m.split('|')[0] for m in st['materials']})}
            e.update(marks)
            meta[mid] = e
            json.dump(meta, open(META_PATH, 'w'), indent=1)
            ex = export_v2.reexport(category, mid)
            _drop_libs()
            thumbs.append(th)
            rows.append((mid, st['tris'], tuple(st['size_studs']), ex.get('pieces'), ex.get('max_tris'), {k: len(v) for k, v in marks.items()}))
        except Exception:
            rows.append((mid, 'ERROR', traceback.format_exc()[-500:]))
    if thumbs:
        kitlib.contact_sheet(thumbs, out=os.path.join(LIB, 'v4_sheets', sheet_name + '.png'), cols=4, cell=res)
    export_v2.write_palette()
    return rows


def save_model(ob, category, model_id, extra=None, preview=True, focus=None):
    """Extract markers, render quad preview, save .blend/.fbx via kitlib.save, record metadata.
    The proper per-colour FBX is produced afterwards by export_v2.reexport."""
    marks = extract_markers(ob)
    st = kitlib.stats(ob)
    prev = None
    if preview:
        prev = quad_preview(ob, os.path.join(LIB, 'v4_sheets', model_id + '.png'), focus=focus)
    info = kitlib.save(ob, category, model_id, render_png=False)
    meta = load_meta()
    entry = {'category': category, 'tris': st['tris'], 'size': list(st['size_studs']), 'materials': sorted({m.split('|')[0] for m in st['materials']})}
    entry.update(marks)
    if extra:
        entry.update(extra)
    meta[model_id] = entry
    json.dump(meta, open(META_PATH, 'w'), indent=1)
    return {'id': model_id, 'tris': st['tris'], 'size': st['size_studs'], 'markers': {k: len(v) for k, v in marks.items()}, 'preview': prev}
