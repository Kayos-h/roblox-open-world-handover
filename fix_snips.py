"""fix_snips - small corrections to the round-3 snippets (cairn proportions to the 30x30x10 manifest, lantern openings, shrine hub)."""
import re

T = r"C:\Users\Nitro\.kiro\crew\workspace\town"


def edit(path, pairs):
    t = open(path, encoding='utf-8-sig').read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, t.count(old), old[:80])
        t = t.replace(old, new)
    open(path, 'w', encoding='utf-8').write(t)


# ---- va: cairn terrace numbers and lantern openings
p = T + r"\lead_snip_va.py"
t = open(p, encoding='utf-8-sig').read()
a = t.index('def cairn():')
b = t.index('def lantern_post():')
cairn = '''def cairn():
    """WT13_05 (round 3, lead) - a stepped plateau terrace with a cairn on top, 30 x 30 x 10 like its WT13 siblings: two coursed tiers (solid cores, ashlar faces, coping, paved decks),
    a front stair in solid steps to each tier, and a tapering cairn of stacked stones with two small satellites on the upper deck. No bright finial."""
    reset()
    A = Acc()
    rnd = random.Random(2405)
    w, d = 30.0, 26.0
    A.box((w, d, 1.0), (0, 0, 0.5), P['stone_d'])
    A.box((w - 1.6, d - 1.6, 2.4), (0, 0, 2.2), P['stone_m'])
    _wrap_body(A, rnd, w, d, 0.0, 1.0, 3.4, seed=2405)
    _coping(A, w, d, 0.0, 3.7)
    _paved_deck(A, w, d, 0.0, 3.6)
    w2, d2 = 20.0, 18.0
    A.box((w2 - 1.2, d2 - 1.2, 2.0), (0, 0, 4.6), P['stone_m'])
    _wrap_body(A, rnd, w2, d2, 0.0, 3.6, 5.6, seed=2415)
    _coping(A, w2, d2, 0.0, 5.9)
    _paved_deck(A, w2, d2, 0.0, 5.8)
    for i in range(4):
        h = 0.9 + (i + 1) * 0.7
        A.box((8.0, 1.5, h), (0, -d / 2 - 0.6 - (3 - i) * 1.4, h / 2.0), P['tread'], bev=0.06)
        A.box((8.3, 0.4, 0.25), (0, -d / 2 - 0.6 - (3 - i) * 1.4 - 0.75, h + 0.05), P['trim'], bev=0)
    for i in range(3):
        h = 3.6 + (i + 1) * 0.7
        A.box((6.0, 1.4, h - 3.0), (0, -d2 / 2 - 0.4 - (2 - i) * 1.3, 3.0 + (h - 3.0) / 2.0), P['tread'], bev=0.06)
        A.box((6.3, 0.4, 0.25), (0, -d2 / 2 - 0.4 - (2 - i) * 1.3 - 0.7, h + 0.05), P['trim'], bev=0)
    z0 = 6.0
    A.cyl(3.8, 0.5, (0, 0, z0 - 0.3), P['stone_d'], verts=16, r2=3.5)
    z = z0 + 0.2
    for lv in range(5):
        r = 3.0 * (1.0 - lv / 7.0)
        n = max(1, 4 - lv // 2)
        for k in range(n):
            a_ = rnd.uniform(0, 360) if n > 1 else 0
            x, y, _ = polar(r * 0.45 if n > 1 else 0.0, a_)
            h = rnd.uniform(0.7, 0.95)
            A.chunk((rnd.uniform(1.9, 2.9) * (1 - lv * 0.06), rnd.uniform(1.7, 2.6) * (1 - lv * 0.06), h), (x, y, z + h / 2),
                    band(COURSE, lv / 5.0, rnd), (0, 0, rnd.uniform(0, 90)), 0.12, rnd)
        z += 0.6
    A.chunk((1.5, 1.5, 0.9), (0, 0, z + 0.3), P['stone_l'], (0, 0, 20), 0.12, rnd)
    for dx, dy in ((6.0, 5.0), (-6.0, 4.5)):
        zz = z0
        A.cyl(1.8, 0.4, (dx, dy, zz - 0.2), P['stone_d'], verts=10)
        for lv in range(4):
            h = rnd.uniform(0.6, 0.8)
            A.chunk((1.9 - lv * 0.3, 1.7 - lv * 0.28, h), (dx + rnd.uniform(-0.2, 0.2), dy + rnd.uniform(-0.2, 0.2), zz + h / 2),
                    band(COURSE, lv / 4.0, rnd), (0, 0, rnd.uniform(0, 90)), 0.12, rnd)
            zz += h * 0.95
    for k in range(6):
        A.ball(0.7, (rnd.uniform(-13, 13), -d / 2 - 0.3, 1.2), P['moss'], segs=6, rings=4, scale=(1.5, 1.0, 0.35))
    return _fin(A, 'cairn')


'''
t = t[:a] + cairn + t[b:]
old = """    for sx, sy in ((1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0)):
        A.box((0.12 + 0.0 * sx, 0.12 + 0.0 * sy, 1.0) if sx == 0 and sy == 0 else ((0.1, 0.9, 1.1) if sx else (0.9, 0.1, 1.1)), (sx * 0.95, sy * 0.95, 7.2), P['throat'], bev=0)
"""
new = """    for sx, sy in ((1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0)):
        A.box((0.1, 0.9, 1.1) if sx else (0.9, 0.1, 1.1), (sx * 0.95, sy * 0.95, 7.2), P['throat'], bev=0)
"""
assert t.count(old) == 1
t = t.replace(old, new)
open(p, 'w', encoding='utf-8').write(t)

# ---- vc: hub reaches the roof
edit(T + r"\lead_snip_vc.py", [("A.box((2.6, 2.6, 1.6), (0, 0, 7.4), VC['stone'])", "A.box((2.6, 2.6, 1.8), (0, 0, 7.4), VC['stone'])")])
print('snippets corrected')
