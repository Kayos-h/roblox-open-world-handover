"""v5_backview - render ONE extra picture per model (3/4 view from behind, same lighting and size as the library thumbnails) so reviewers see both sides.
Opens the saved .blend of each id (any model, rebuilt or not), so rebuilt models and untouched models are rendered identically.
  blender -b --factory-startup --python v5_backview.py -- <ids.json> <outdir>
ids.json = list of {"id":..., "category":...}. Writes <outdir>\\<id>.png (420 px). Touches nothing else.
"""
import sys
import os
import json
import time
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
import bpy
import kitlib
import v4util
import v5liverun
v5liverun._patch_once()
rows = json.load(open(argv[0]))
out = argv[1]
os.makedirs(out, exist_ok=True)
t0 = time.time()
n = 0
for r in rows:
    mid = r['id']
    p = os.path.join(out, mid + '.png')
    if os.path.exists(p):
        continue
    try:
        bpy.ops.wm.open_mainfile(filepath=os.path.join(kitlib.LIB, r['category'], mid + '.blend'))
        ob = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
        v4util.thumb_preview(ob, p, 420, view=(-1.0, 1.1, 0.4), dist=1.85)
        n += 1
    except Exception as e:
        print('BACK_FAIL', mid, str(e)[:100])
    if n % 20 == 0 and n:
        print('BACK_PROGRESS', n, round(time.time() - t0))
print('BACK_DONE', n, round(time.time() - t0))
