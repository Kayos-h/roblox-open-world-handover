import sys, importlib, io, contextlib, traceback, json, os
p = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\src"
if p not in sys.path: sys.path.insert(0, p)
import kitlib, export_v2
importlib.reload(kitlib); importlib.reload(export_v2)
FOLDER = 'elf'
res = []
for cat, mid in export_v2.all_models():
    if cat != FOLDER:
        continue
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            info = export_v2.reexport(cat, mid)
    except Exception:
        info = {'id': mid, 'error': traceback.format_exc()[-400:]}
    res.append(info)
rep = os.path.join(export_v2.LIB, '_export_v2', FOLDER + '.json')
os.makedirs(os.path.dirname(rep), exist_ok=True)
with open(rep, 'w') as f:
    json.dump(res, f, indent=1)
bad = [r['id'] for r in res if 'error' in r or r.get('max_tris', 0) > 18000]
print(FOLDER, 'exported', len(res), 'bad', bad)
