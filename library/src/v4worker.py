"""v4worker - headless Blender batch runner so several workers can build models in parallel without touching each other.

Run (always through v4run.ps1, which adds --factory-startup so the MCP addon is NOT loaded):
  blender -b --factory-startup --python v4worker.py -- <module> <worker> [--batch a,b] [--only ID,ID] [--res 420] [--chunk 12]

<module>  a file in library\\src (without .py). It must define
          BATCHES = {'batch_name': ('category_folder', [(manifest_id, builder_fn[, view]), ...])}
<worker>  short id, e.g. 'wa'. Every shared file is split per worker:
            library\\v4_meta_<worker>.json       model metadata (tris, size, markers)
            library\\palette_<worker>.json        palette keys added by this worker's module
            library\\v4_sheets\\<worker>_<batch>_<k>.png   contact sheets (<= --chunk models each)
            library\\v4_work\\<worker>_<batch>.json        build report (also printed)
Existing files in library\\src are never modified. New palette keys: kitlib.PAL['x_name'] = ((r,g,b), 'RobloxMaterial', metallic, roughness, emission)
"""
import sys, os, json, time, importlib, traceback

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
import bpy
import kitlib, v4util, export_v2

BASE_PAL = set(kitlib.PAL.keys())
LIB = kitlib.LIB
WORK = os.path.join(LIB, 'v4_work')
os.makedirs(WORK, exist_ok=True)
os.makedirs(os.path.join(LIB, 'v4_sheets'), exist_ok=True)


def opt(name, default=None):
    if name in argv:
        i = argv.index(name)
        return argv[i + 1] if i + 1 < len(argv) else default
    return default


modname, worker = argv[0], argv[1]
only = set(opt('--only', '').split(',')) - {''}
want = [b for b in opt('--batch', '').split(',') if b]
res = int(opt('--res', 420))
chunk = int(opt('--chunk', 12))

v4util.META_PATH = os.path.join(LIB, f'v4_meta_{worker}.json')
quad = '--quad' in argv


def _quad_preview_w(ob, out, res=460, focus=None):
    """Same as v4util.quad_preview but with worker-specific temp files, so parallel workers never overwrite each other."""
    from mathutils import Vector
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
        p = os.path.join(LIB, 'v4_sheets', f'_q_{worker}_{i}.png')
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        tmp.append(p)
    kitlib._cleanup_render()
    kitlib.contact_sheet(tmp, out=out, cols=2, cell=res)
    return out


v4util.quad_preview = _quad_preview_w

# ---- render previews on the CPU (Cycles). EEVEE needs a GPU GL context, and several Blender processes at once crashed the
# NVIDIA driver (nvoglv64.dll / nvwgf2umx.dll access violations). Set V4_EEVEE=1 in the environment to go back to EEVEE.
if os.environ.get('V4_EEVEE') != '1':
    _orig_setup_render = kitlib._setup_render

    def _setup_render_cpu(ob, res=900):
        r = _orig_setup_render(ob, res)
        sc = bpy.context.scene
        sc.render.engine = 'CYCLES'
        cy = sc.cycles
        for k, v in (('device', 'CPU'), ('samples', 24), ('use_adaptive_sampling', True), ('adaptive_threshold', 0.05),
                     ('use_denoising', os.environ.get('V4_NODENOISE') != '1'), ('denoiser', 'OPENIMAGEDENOISE'), ('denoising_use_gpu', False),
                     ('max_bounces', 4), ('diffuse_bounces', 2), ('glossy_bounces', 2),
                     ('transmission_bounces', 2), ('transparent_max_bounces', 4), ('volume_bounces', 0)):
            try:
                setattr(cy, k, v)
            except Exception:
                pass
        return r

    kitlib._setup_render = _setup_render_cpu


# ---- previews must never cost a model: run_batch renders BEFORE it saves, so a render error used to lose the whole model.
def _fail_safe(fn, label):
    def wrapped(ob, out, *a, **kw):
        res0 = kw.get('res', a[0] if a else 420)
        for attempt in range(3):
            try:
                if attempt >= 1:
                    os.environ['V4_NODENOISE'] = '1'          # retry without the denoiser (its memory use was the failure)
                if attempt == 2:
                    kw['res'] = max(240, int(res0 * 0.7))      # and smaller
                    a = a[1:] if a else a
                return fn(ob, out, *a, **kw)
            except Exception as e:
                print('PREVIEW_RETRY', label, attempt, str(e)[:100])
                try:
                    kitlib._cleanup_render()
                except Exception:
                    pass
            finally:
                os.environ.pop('V4_NODENOISE', None)
        print('PREVIEW_FAILED', label, out)                    # model files are still saved; the sheet shows a blank cell
        try:
            r = int(res0)
            img = bpy.data.images.new('_ph', r, r)
            img.filepath_raw = out
            img.file_format = 'PNG'
            img.save()
            bpy.data.images.remove(img)
        except Exception:
            pass
        return out
    return wrapped


v4util.thumb_preview = _fail_safe(v4util.thumb_preview, 'thumb')
v4util.quad_preview = _fail_safe(v4util.quad_preview, 'quad')


def write_fragment():
    out = {}
    for k, v in kitlib.PAL.items():
        if k in BASE_PAL:
            continue
        rgb, rmat = v[0], v[1]
        emit = v[4] if len(v) > 4 else 0
        out[k] = {'rgb': [round(c, 4) for c in rgb], 'material': rmat, 'glow': bool(emit)}
    p = os.path.join(LIB, f'palette_{worker}.json')
    old = {}
    if os.path.exists(p):
        try:
            old = json.load(open(p))
        except Exception:
            old = {}
    old.update(out)
    json.dump(old, open(p, 'w'), indent=1)
    return p


export_v2.write_palette = write_fragment

try:
    # make sure a stale module from a previous run in the same process is not used
    if modname in sys.modules:
        del sys.modules[modname]
    mod = importlib.import_module(modname)
except Exception:
    print('IMPORT_ERROR', traceback.format_exc()[-1500:])
    sys.exit(2)

batches = mod.BATCHES
names = want or list(batches)
allrows = []
for bn in names:
    if bn not in batches:
        print('NO_SUCH_BATCH', bn, 'available:', list(batches))
        continue
    cat, items = batches[bn]
    if only:
        items = [it for it in items if it[0] in only]
    for k in range(0, len(items), chunk):
        part = items[k:k + chunk]
        t0 = time.time()
        sheet = f'{worker}_{bn}_{k // chunk + 1}'
        try:
            rows = v4util.run_batch(part, cat, sheet, res=res, quad=quad)
        except Exception:
            rows = [(part[0][0], 'ERROR', traceback.format_exc()[-700:])]
        dt = round(time.time() - t0, 1)
        rep = {'worker': worker, 'batch': bn, 'chunk': k // chunk + 1, 'seconds': dt, 'sheet': sheet + '.png', 'rows': rows}
        json.dump(rep, open(os.path.join(WORK, f'{worker}_{bn}_{k // chunk + 1}.json'), 'w'), indent=1, default=str)
        allrows.extend(rows)
        print(f'CHUNK {bn} #{k // chunk + 1}: {len(part)} models in {dt}s -> sheet {sheet}.png (render engine: {bpy.context.scene.render.engine})')
        for r in rows:
            print('  ', r)
print('WORKER_DONE', worker, 'models:', len(allrows), 'errors:', sum(1 for r in allrows if len(r) > 1 and r[1] == 'ERROR'))
