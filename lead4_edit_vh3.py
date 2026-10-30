"""lead4_edit_vh3 - DS04_02 becomes an upright vase-crown palm (a different silhouette from the umbrella palm DS04_01; autofit would normalise any lean or flare away)."""
S = r"C:\Users\Nitro\.kiro\crew\workspace\town"
p = S + r"\lead4_snip_vh.py"
t = open(p, encoding='utf-8-sig').read()
new_fn = '''def _palm_fan():
    reset()
    A = Acc()
    rnd = random.Random(8812)
    h = 42.0
    segs = 9
    prev = (0.0, 0.0, 0.0)
    A.cyl(2.2, 2.0, (0, 0, 0), P['bark'], verts=10, r2=1.9)
    for s in range(1, segs + 1):
        tt = s / float(segs)
        q = (1.4 * math.sin(tt * 3.0), 0.0, h * tt)
        r = 1.9 - 0.5 * tt
        A.beam((prev[0], prev[1], max(0.0, prev[2] - 0.8)), q, r * 2.0, r * 2.0, P['bark'])
        A.sweep([(r * 0.95, -0.24), (r * 1.65, -0.24), (r * 1.65, 0.24), (r * 0.95, 0.24)], 0, 360, 8, P['bark'], loc=q)
        prev = q
    top = prev
    A.cyl(2.0, 2.6, (top[0], top[1], top[2] - 1.3), P['bark'], verts=10, r2=1.6)
    nf = 11
    for k in range(nf):
        a = 360.0 / nf * k + rnd.uniform(-8, 8)
        pts = []
        for s in range(6):
            tt = s / 5.0
            x, y, _ = polar(tt * 8.5, a)
            pts.append((top[0] + x, top[1] + y, top[2] + 7.5 * math.sin(tt * 1.5) - 3.5 * tt * tt + 0.5))
        for p0, p1 in zip(pts, pts[1:]):
            A.beam(p0, p1, 0.55, 0.4, P['bark'])
        for j, pt in enumerate(pts[1:]):
            bl = 3.0 - j * 0.4
            for sg in (-1, 1):
                A.box((bl, 0.25, 0.9), (pt[0], pt[1], pt[2]), P['palm'] if (k + j) % 2 else P['palm2'], (0, 0, a + sg * 35.0), bev=0)
    for k in range(6):
        x, y, _ = polar(1.5, k * 60.0)
        A.ball(0.8, (top[0] + x, top[1] + y, top[2] - 0.9), P['clay'], segs=6, rings=4)
    return _fin(A, 'oasis_palm')


'''
a = t.index("def ds01_01():")
t = t[:a] + new_fn + t[a:]
old = "def ds04_02():\n    return LK.wrap(lambda: _palm(1), deform=dict(bend=(0.3, -0.1), twist=-18.0, scale=(1.1, 1.0, 1.0), flare=0.55))()"
assert t.count(old) == 1
t = t.replace(old, "def ds04_02():\n    return LK.wrap(_palm_fan)()")
old = "def ds04_01():\n    return LK.wrap(lambda: _palm(0), deform=dict(bend=(-0.3, 0.1), twist=24.0, flare=-0.2))()"
assert t.count(old) == 1
t = t.replace(old, "def ds04_01():\n    return LK.wrap(lambda: _palm(0))()")
open(p, 'w', encoding='utf-8').write(t)
print('ok')
