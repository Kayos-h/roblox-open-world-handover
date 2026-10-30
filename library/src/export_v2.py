"""Roblox export v2.

Problems found on the first upload test:
  1. Models came in 100x too big (FBX written in centimetres, Roblox read the raw numbers as studs).
  2. Each model became ONE grey MeshPart (a Roblox MeshPart holds one colour/material).

Fix: for every saved .blend, load the model mesh, split it into one object per material
(object name = palette key), keep each piece under MAX_TRIS, and export with global_scale=0.01
so 1 Blender unit = 1 stud in Roblox. Studio then paints each MeshPart from palette.json.
Loads objects with bpy.data.libraries.load so the open file (and the MCP addon) is untouched.
"""
import bpy, bmesh, os, json
import kitlib

LIB = kitlib.LIB
FOLDERS = ['roads', 'lighting', 'nature', 'props', 'capital', 'castle', 'rusty', 'alpine', 'elf', 'harbour', 'between', 'town1']
MAX_TRIS = 18000
SCALE = 0.01


def write_palette():
    out = {}
    for k, v in kitlib.PAL.items():
        rgb, rmat = v[0], v[1]
        emit = v[4] if len(v) > 4 else 0
        out[k] = {'rgb': [round(c, 4) for c in rgb], 'material': rmat, 'glow': bool(emit)}
    path = os.path.join(LIB, 'palette.json')
    with open(path, 'w') as f:
        json.dump(out, f, indent=1)
    return path


def _clear_tmp():
    for o in list(bpy.data.objects):
        if o.name.startswith('RBX_'):
            bpy.data.objects.remove(o, do_unlink=True)
    for m in list(bpy.data.meshes):
        if m.users == 0:
            bpy.data.meshes.remove(m)


def _load_meshes(blend):
    with bpy.data.libraries.load(blend, link=False) as (src, dst):
        dst.objects = list(src.objects)
    obs = [o for o in dst.objects if o is not None and o.type == 'MESH']
    for o in dst.objects:
        if o is not None and o.type != 'MESH':
            bpy.data.objects.remove(o, do_unlink=True)
    for o in obs:
        bpy.context.scene.collection.objects.link(o)
    return obs


def _tri_count(me):
    return sum(len(p.vertices) - 2 for p in me.polygons)


def _split_by_material(obs, model_id):
    """Return new objects: one per palette key (further cut if over MAX_TRIS)."""
    faces = {}  # key -> list of (mesh_obj, poly_index)
    for o in obs:
        for p in o.data.polygons:
            mat = o.data.materials[p.material_index] if o.data.materials else None
            key = mat.name.split('|')[0] if mat else 'default'
            key = key.split('.')[0]
            faces.setdefault(key, []).append((o, p.index))
    pieces = []
    for key, flist in faces.items():
        bm_all = bmesh.new()
        by_obj = {}
        for o, i in flist:
            by_obj.setdefault(o, set()).add(i)
        for o, keep in by_obj.items():
            bm = bmesh.new(); bm.from_mesh(o.data)
            bm.transform(o.matrix_world)
            bm.faces.ensure_lookup_table()
            bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.index not in keep], context='FACES')
            tmp = bpy.data.meshes.new('RBX_tmp'); bm.to_mesh(tmp); bm.free()
            bm_all.from_mesh(tmp)
            bpy.data.meshes.remove(tmp)
        me = bpy.data.meshes.new(f'RBX_{key}')
        bm_all.to_mesh(me); bm_all.free()
        ob = bpy.data.objects.new(f'RBX_{key}', me)
        bpy.context.scene.collection.objects.link(ob)
        if _tri_count(me) > MAX_TRIS:
            parts = kitlib._split_pieces(ob, MAX_TRIS)
            for n, p in enumerate(parts):
                p.name = f'RBX_{key}_{n + 1}'
            bpy.data.objects.remove(ob, do_unlink=True)
            pieces.extend(parts)
        else:
            pieces.append(ob)
    return pieces


def reexport(category, model_id):
    base = os.path.join(LIB, category, model_id)
    _clear_tmp()
    obs = _load_meshes(base + '.blend')
    if not obs:
        return {'id': model_id, 'error': 'no mesh in blend'}
    pieces = _split_by_material(obs, model_id)
    for o in obs:
        bpy.data.objects.remove(o, do_unlink=True)
    for o in bpy.context.scene.objects:
        o.select_set(False)
    for p in pieces:
        p.name = p.name[4:]  # drop RBX_ so Roblox part name = palette key
        p.select_set(True)
    bpy.context.view_layer.objects.active = pieces[0]
    bpy.ops.export_scene.fbx(filepath=base + '.fbx', use_selection=True, global_scale=SCALE,
                             apply_unit_scale=True, apply_scale_options='FBX_SCALE_NONE',
                             axis_forward='-Z', axis_up='Y', mesh_smooth_type='EDGE',
                             bake_space_transform=True, object_types={'MESH'}, use_triangles=True)
    info = {'id': model_id, 'pieces': len(pieces), 'max_tris': max(_tri_count(p.data) for p in pieces),
            'names': sorted({p.name for p in pieces})}
    xs, ys, zs = [], [], []
    for p in pieces:
        for v in p.data.vertices:
            w = p.matrix_world @ v.co
            xs.append(w.x); ys.append(w.y); zs.append(w.z)
    info['size'] = [round(max(xs) - min(xs), 2), round(max(ys) - min(ys), 2), round(max(zs) - min(zs), 2)]
    info['min_z'] = round(min(zs), 2)
    for p in pieces:
        bpy.data.objects.remove(p, do_unlink=True)
    _clear_tmp()
    return info


def all_models():
    out = []
    for f in FOLDERS:
        d = os.path.join(LIB, f)
        if os.path.isdir(d):
            out += [(f, n[:-6]) for n in sorted(os.listdir(d)) if n.endswith('.blend')]
    return out
