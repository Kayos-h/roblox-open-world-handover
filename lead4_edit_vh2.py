"""lead4_edit_vh2 - batch 3 corrections: kit flare, stronger palm differences, smaller hoodoo crown, remove the blue awning strip of DS01_01, drop the kit debug print."""
S = r"C:\Users\Nitro\.kiro\crew\workspace\town"


def edit(path, pairs):
    t = open(path, encoding='utf-8-sig').read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, t.count(old), old[:90])
        t = t.replace(old, new)
    open(path, 'w', encoding='utf-8').write(t)


edit(S + r"\library\src\v5_leadkit.py", [
    ("def _deform(A, lean=(0.0, 0.0), bend=(0.0, 0.0), twist=0.0, taper=0.0, scale=(1.0, 1.0, 1.0), mirror_x=False, mirror_y=False):",
     "def _deform(A, lean=(0.0, 0.0), bend=(0.0, 0.0), twist=0.0, taper=0.0, scale=(1.0, 1.0, 1.0), mirror_x=False, mirror_y=False, flare=0.0):"),
    ("            if taper:\n                s = 1.0 - taper * t\n                x, y = x * s, y * s\n",
     "            if taper:\n                s = 1.0 - taper * t\n                x, y = x * s, y * s\n            if flare:\n                s = 1.0 + flare * t ** 3\n                x, y = x * s, y * s\n"),
    ("    print('SCRATCH_DZ pushed', len(push), 'faces of', len(isl_vol), 'islands')\n", ""),
])
edit(S + r"\lead4_snip_vh.py", [
    ("deform=dict(bend=(-0.16, 0.05), twist=24.0))()", "deform=dict(bend=(-0.3, 0.1), twist=24.0, flare=-0.2))()"),
    ("deform=dict(bend=(0.2, -0.06), twist=-18.0, scale=(1.1, 1.0, 1.0)))()", "deform=dict(bend=(0.3, -0.1), twist=-18.0, scale=(1.1, 1.0, 1.0), flare=0.55))()"),
    ("    A.chunk((16.0, 10.5, 9.0), (0, 0, 54.0), P['sand'], (0, 0, 0), 0.08, r_, (0.9, 0.9))\n    for sg in (-1, 1):\n        A.chunk((8.0, 10.0, 8.0), (sg * 9.0, 0, 51.0), P['clay'], (0, 0, 0), 0.08, r_, (0.9, 0.9))",
     "    A.chunk((12.0, 9.5, 6.5), (0, 0, 55.0), P['sand'], (0, 0, 0), 0.08, r_, (0.9, 0.9))\n    for sg in (-1, 1):\n        A.chunk((6.0, 9.5, 6.0), (sg * 8.0, 0, 51.5), P['clay'], (0, 0, 0), 0.08, r_, (0.9, 0.9))"),
    ("prune=[dict(keys=None, max_size=1.9, max_z=1.5)])()\n\n\ndef ds01_05", "prune=[dict(keys=[R.D['cloth1']], max_size=25.0), dict(keys=None, max_size=1.9, max_z=1.5)])()\n\n\ndef ds01_05"),
])
print('ok')
