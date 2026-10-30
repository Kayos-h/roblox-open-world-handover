"""v5liverun - run a v5 module's batches inside the OPEN Blender (through the add-on socket, via live_batch.ps1).
Same outputs as the headless v4worker: .blend + .fbx + per-colour Roblox FBX, v4_meta_<worker>.json, palette_<worker>.json, contact sheets.
Previews use Cycles on the CPU like the headless runner (so every thumbnail has the same look); the scene render engine is restored afterwards.
  v5liverun.run('v5_va', 'va', batches=['tower_shell'], only=None)
The last model built stays in the open scene so it can be looked at.
"""
import sys
import os
import json
import time
import importlib
import traceback
SRC = os.path.dirname(os.path.abspath(__file__))
if SRC not in sys.path:
    sys.path.insert(0, SRC)
import bpy
import kitlib
import v4util
import export_v2


def _patch_once():
    if getattr(kitlib, '_v5_patched', False):
        return
    orig = kitlib._setup_render

    def cpu(ob, res=900):
        r = orig(ob, res)
        sc = bpy.context.scene
        sc.render.engine = 'CYCLES'
        cy = sc.cycles
        for k, v in (('device', 'CPU'), ('samples', 24), ('use_adaptive_sampling', True), ('adaptive_threshold', 0.05),
                     ('use_denoising', os.environ.get('V4_NODENOISE') != '1'), ('denoiser', 'OPENIMAGEDENOISE'), ('denoising_use_gpu', False),
                     ('max_bounces', 4), ('diffuse_bounces', 2), ('glossy_bounces', 2), ('transmission_bounces', 2),
                     ('transparent_max_bounces', 4), ('volume_bounces', 0)):
            try:
                setattr(cy, k, v)
            except Exception:
                pass
        return r
    kitlib._setup_render = cpu

    def fail_safe(fn, label):
        def wrapped(ob, out, *a, **kw):
            res0 = kw.get('res', a[0] if a else 420)
            for attempt in range(3):
                try:
                    if attempt >= 1:
                        os.environ['V4_NODENOISE'] = '1'
                    if attempt == 2:
                        kw['res'] = max(240, int(res0 * 0.7))
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
            print('PREVIEW_FAILED', label, out)
            try:
                img = bpy.data.images.new('_ph', int(res0), int(res0))
                img.filepath_raw = out
                img.file_format = 'PNG'
                img.save()
                bpy.data.images.remove(img)
            except Exception:
                pass
            return out
        return wrapped
    v4util.thumb_preview = fail_safe(v4util.thumb_preview, 'thumb')
    kitlib._v5_patched = True


def _write_fragment(worker):
    pre = worker + '_'
    out = {}
    for k, v in kitlib.PAL.items():
        if not k.startswith(pre):
            continue
        rgb, rmat = v[0], v[1]
        emit = v[4] if len(v) > 4 else 0
        out[k] = {'rgb': [round(c, 4) for c in rgb], 'material': rmat, 'glow': bool(emit)}
    p = os.path.join(kitlib.LIB, f'palette_{worker}.json')
    old = {}
    if os.path.exists(p):
        try:
            old = json.load(open(p))
        except Exception:
            old = {}
    old.update(out)
    json.dump(old, open(p, 'w'), indent=1)
    return p


def frame_view():
    """Frame the newest model in every 3D viewport and show material colours (cosmetic; ignores any failure)."""
    try:
        for win in bpy.context.window_manager.windows:
            for area in win.screen.areas:
                if area.type != 'VIEW_3D':
                    continue
                reg = next((r for r in area.regions if r.type == 'WINDOW'), None)
                with bpy.context.temp_override(window=win, area=area, region=reg):
                    area.spaces[0].shading.type = 'SOLID'
                    area.spaces[0].shading.color_type = 'MATERIAL'
                    area.spaces[0].clip_end = max(area.spaces[0].clip_end, 2000.0)
                    bpy.ops.view3d.view_all(center=False)
    except Exception as e:
        print('frame_view skipped:', str(e)[:80])


def run(modname, worker, batches=None, only=None, res=420, chunk=12):
    _patch_once()
    lib = kitlib.LIB
    os.makedirs(os.path.join(lib, 'v4_work'), exist_ok=True)
    os.makedirs(os.path.join(lib, 'v4_sheets'), exist_ok=True)
    v4util.META_PATH = os.path.join(lib, f'v4_meta_{worker}.json')
    export_v2.write_palette = lambda: _write_fragment(worker)
    # reload order: kit, generators, every round-1 queue module already loaded (a fix module may import one), then the target.
    # Other builders' v5_fx_* modules are skipped on purpose: one of them may be half edited and must not break this build.
    others = sorted(n for n in sys.modules if n.startswith('v5_') and not n.startswith('v5_fx_') and n != modname)
    for n in ['v5kit', 'v5gen'] + others + [modname]:
        if n in sys.modules:
            importlib.reload(sys.modules[n])
        else:
            importlib.import_module(n)
    mod = sys.modules[modname]
    engine0 = bpy.context.scene.render.engine
    only = set(only or [])
    allrows = []
    try:
        for bn in (batches or list(mod.BATCHES)):
            if bn not in mod.BATCHES:
                print('NO_SUCH_BATCH', bn, list(mod.BATCHES))
                continue
            cat, items = mod.BATCHES[bn]
            if only:
                items = [it for it in items if it[0] in only]
            for k in range(0, len(items), chunk):
                part = items[k:k + chunk]
                t0 = time.time()
                sheet = f'{worker}_{bn}_{k // chunk + 1}'
                try:
                    rows = v4util.run_batch(part, cat, sheet, res=res)
                except Exception:
                    rows = [(part[0][0], 'ERROR', traceback.format_exc()[-700:])]
                dt = round(time.time() - t0, 1)
                json.dump({'worker': worker, 'batch': bn, 'chunk': k // chunk + 1, 'seconds': dt, 'sheet': sheet + '.png', 'rows': rows},
                          open(os.path.join(lib, 'v4_work', f'{worker}_{bn}_{k // chunk + 1}.json'), 'w'), indent=1, default=str)
                allrows.extend(rows)
                print(f'CHUNK {bn} #{k // chunk + 1}: {len(part)} models in {dt}s -> sheet {sheet}.png')
                for r in rows:
                    print('  ', r)
    finally:
        try:
            bpy.context.scene.render.engine = engine0
        except Exception:
            pass
    frame_view()
    print('LIVE_DONE', worker, 'models:', len(allrows), 'errors:', sum(1 for r in allrows if len(r) > 1 and r[1] == 'ERROR'))
