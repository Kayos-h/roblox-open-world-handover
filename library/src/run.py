# run.py - helper executed inside Blender: build(module, func) -> object, preview render.
import sys, importlib
SRC = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\src"
if SRC not in sys.path:
    sys.path.insert(0, SRC)
import kitlib

def build(module, func, preview=True, res=700, save_cat=None, model_id=None):
    importlib.reload(kitlib)
    mod = importlib.import_module(module)
    importlib.reload(mod)
    ob = getattr(mod, func)()
    info = kitlib.stats(ob)
    if preview:
        kitlib.render(ob, r"C:\Users\Nitro\.kiro\crew\workspace\town\library\_wip.png", res=res)
    if save_cat:
        info = kitlib.save(ob, save_cat, model_id or func)
    return info


def batch(module, category, only=None, save=False, res=520, group='ITEMS'):
    importlib.reload(kitlib)
    mod = importlib.import_module(module)
    importlib.reload(mod)
    items = [it for it in getattr(mod, group) if (only is None or it[0] in only)]
    return kitlib.batch(items, category, save_files=save, res=res)
