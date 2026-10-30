"""lead4_edit_vh4 - LM14_02 becomes an octagonal obelisk with collars and a ball finial (autofit undoes size changes, so the shape itself has to differ)."""
S = r"C:\Users\Nitro\.kiro\crew\workspace\town"
p = S + r"\lead4_snip_vh.py"
t = open(p, encoding='utf-8-sig').read()
new_fn = '''def _obelisk_oct():
    reset()
    A = Acc()
    A.cyl(5.6, 2.2, (0, 0, 0), P['stone'], verts=8)
    A.cyl(4.6, 1.6, (0, 0, 2.2), P['sandd'], verts=8)
    A.cyl(3.4, 46.0, (0, 0, 3.8), P['sand'], verts=8, r2=2.0)
    for z, r in ((12.0, 3.15), (24.0, 2.85), (36.0, 2.55)):
        A.cyl(r + 0.45, 0.6, (0, 0, z), P['clay'], verts=8)
    for z in (18.0, 30.0, 42.0):
        A.cyl(2.6 - (z - 18.0) * 0.012, 3.0, (0, 0, z), P['sandl'], verts=8, r2=2.5 - (z - 18.0) * 0.012)
    A.cyl(2.2, 2.6, (0, 0, 49.8), P['sandl'], verts=8, r2=1.5)
    A.ball(1.7, (0, 0, 53.4), P['clay'], segs=10, rings=6)
    A.cyl(0.35, 3.0, (0, 0, 54.6), P['sandd'], verts=6, r2=0.05)
    return _fin(A, 'sand_obelisk')


'''
a = t.index("def ds01_01():")
t = t[:a] + new_fn + t[a:]
a = t.index("def lm14_02():")
b = t.index("def lm16_01():")
t = t[:a] + "def lm14_02():\n    return LK.wrap(_obelisk_oct)()\n\n\n" + t[b:]
open(p, 'w', encoding='utf-8').write(t)
print('ok')
