"""v5_quad - render the four-angle review sheet of chosen models in a HEADLESS Blender (CPU Cycles, same look as the thumbnails).
  blender -b --factory-startup --python v5_quad.py -- id1,id2,id3
Writes library\\v4_sheets\\<id>.png (2 x 2 views) for each id. Opens the saved .blend files; changes nothing else.
"""
import sys
import os
import json
import glob
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
import bpy
import kitlib
import v4util
import v5liverun
v5liverun._patch_once()
LIB = kitlib.LIB
PID = os.getpid()
OUTDIR = argv[1] if len(argv) > 1 else None


def quad_pid(ob, out, res=460, focus=None):
    """Same four views as v4util.quad_preview, but with temp files named after this process so parallel Blenders never mix their pictures."""
    from mathutils import Vector
    sc = bpy.context.scene
    kitlib._setup_render(ob, res)
    try:
        sc.cycles.samples = int(os.environ.get('QUAD_SAMPLES', '12'))
    except Exception:
        pass
    cam = sc.camera
    d = ob.dimensions
    size = max(d.x, d.y, d.z)
    ctr = Vector((0, 0, d.z / 2))
    fpt = Vector((0.0, 0.0, d.z * 0.55))
    views = [(ctr, (1.0, -1.25, 0.45), size * 1.85), (ctr, (-1.0, 1.1, 0.4), size * 1.85), (fpt, (0.9, -1.1, 0.35), size * 0.9), (ctr, (0.0, -1.0, 0.08), size * 2.0)]
    tmp = []
    for i, (tgt, v, dist) in enumerate(views):
        dirv = Vector(v).normalized()
        cam.location = tgt + dirv * dist
        cam.rotation_euler = (tgt - cam.location).to_track_quat('-Z', 'Y').to_euler()
        p = os.path.join(LIB, 'v4_sheets', f'_q_{PID}_{i}.png')
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        tmp.append(p)
    kitlib._cleanup_render()
    kitlib.contact_sheet(tmp, out=out, cols=2, cell=res)
    for p in tmp:
        try:
            os.remove(p)
        except Exception:
            pass
    return out


v4util.quad_preview = quad_pid
meta = {}
for f in glob.glob(os.path.join(LIB, 'v4_meta_v*.json')):
    try:
        meta.update(json.load(open(f)))
    except Exception:
        pass
for mid in [i for i in (argv[0].split(',') if argv else []) if i]:
    try:
        cat = meta[mid]['category']
        bpy.ops.wm.open_mainfile(filepath=os.path.join(LIB, cat, mid + '.blend'))
        obs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
        out_png = os.path.join(OUTDIR, mid + '.png') if OUTDIR else os.path.join(LIB, 'v4_sheets', mid + '.png')
        os.makedirs(os.path.dirname(out_png), exist_ok=True)
        v4util.quad_preview(obs[0], out_png)
        print('QUAD_OK', mid)
    except Exception as e:
        print('QUAD_FAIL', mid, str(e)[:120])
print('QUAD_DONE')
