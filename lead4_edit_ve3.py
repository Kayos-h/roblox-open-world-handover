"""lead4_edit_ve3 - the world-tree root base gets a broad stump mound that dominates the middle."""
S = r"C:\Users\Nitro\.kiro\crew\workspace\town"
p = S + r"\lead4_snip_ve.py"
t = open(p, encoding='utf-8-sig').read()


def sub(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:80])
    t = t.replace(old, new)


sub("    A.cyl(34.0, 24.0, (0, 0, 3.0), E['bark'], verts=28, r2=24.0)\n    A.ball(24.0, (0, 0, 25.0), E['bark'], segs=20, rings=10, scale=(1.0, 1.0, 0.3))",
    "    A.cyl(56.0, 26.0, (0, 0, 3.0), E['bark'], verts=32, r2=38.0)\n    A.ball(38.0, (0, 0, 28.0), E['bark'], segs=24, rings=10, scale=(1.0, 1.0, 0.22))")
sub("        x, y, _ = polar(28.0, a)\n        A.chunk((4.5, 4.5, r_.uniform(14.0, 20.0)), (x, y, r_.uniform(10.0, 14.0)),",
    "        x, y, _ = polar(47.0, a)\n        A.chunk((7.0, 7.0, r_.uniform(16.0, 22.0)), (x, y, r_.uniform(12.0, 16.0)),")
sub("        x, y, _ = polar(r_.uniform(6.0, 20.0), r_.uniform(0, 360))\n        A.ball(r_.uniform(2.0, 3.4), (x, y, 28.5 - 0.0),",
    "        x, y, _ = polar(r_.uniform(8.0, 34.0), r_.uniform(0, 360))\n        A.ball(r_.uniform(3.0, 5.0), (x, y, 29.0),")
open(p, 'w', encoding='utf-8').write(t)
print('ok')
