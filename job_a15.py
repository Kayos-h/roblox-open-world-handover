import sys, importlib, io, contextlib, traceback
p = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\src"
if p not in sys.path: sys.path.insert(0, p)
import kitlib, export_v2
importlib.reload(kitlib); importlib.reload(export_v2)
try:
    with contextlib.redirect_stdout(io.StringIO()):
        pal = export_v2.write_palette()
        info = export_v2.reexport('lighting', 'A15_lamp_iron_city')
    print('palette:', pal)
    print('A15:', info)
except Exception:
    print('FAILED:', traceback.format_exc())
