"""lead4_edit_ve2 - batch 5 corrections: a much bigger trunk boss for the world-tree roots, round pots instead of the open-topped jar cylinders."""
S = r"C:\Users\Nitro\.kiro\crew\workspace\town"
p = S + r"\lead4_snip_ve.py"
t = open(p, encoding='utf-8-sig').read()


def sub(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:80])
    t = t.replace(old, new)


sub("    A.cyl(20.0, 24.0, (0, 0, 3.0), E['bark'], verts=24, r2=13.5)\n    A.ball(13.5, (0, 0, 26.5), E['bark'], segs=16, rings=8, scale=(1.0, 1.0, 0.45))",
    "    A.cyl(34.0, 24.0, (0, 0, 3.0), E['bark'], verts=28, r2=24.0)\n    A.ball(24.0, (0, 0, 25.0), E['bark'], segs=20, rings=10, scale=(1.0, 1.0, 0.3))")
sub("        x, y, _ = polar(16.0, a)\n        A.chunk((3.0, 3.0, r_.uniform(14.0, 22.0)), (x, y, r_.uniform(10.0, 15.0)),",
    "        x, y, _ = polar(28.0, a)\n        A.chunk((4.5, 4.5, r_.uniform(14.0, 20.0)), (x, y, r_.uniform(10.0, 14.0)),")
sub("        x, y, _ = polar(r_.uniform(4.0, 11.0), r_.uniform(0, 360))\n        A.ball(r_.uniform(1.6, 2.6), (x, y, 28.0),",
    "        x, y, _ = polar(r_.uniform(6.0, 20.0), r_.uniform(0, 360))\n        A.ball(r_.uniform(2.0, 3.4), (x, y, 28.5 - 0.0),")
sub("def _crates2_post(A):\n    for k in range(3):\n        A.cyl(1.0, 0.3, (4.2 + k * 0.6, 2.0 - k * 1.0, 1.6), T1['wood'], verts=10)",
    "def _crates2_post(A):\n    for k in range(3):\n        A.ball(1.0, (4.2 + k * 0.6, 2.0 - k * 1.0, 1.0), T1['cream'], segs=10, rings=6, scale=(1.0, 1.0, 1.1))")
sub("    return LK.wrap(lambda: ORIG._street('crates2'), post=_crates2_post)()",
    "    return LK.wrap(lambda: ORIG._street('crates2'), prune=[dict(keys=[T1['cream']], max_size=2.6)], post=_crates2_post)()")
open(p, 'w', encoding='utf-8').write(t)
print('ok')
