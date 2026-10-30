"""edit_snip_vg - round-3 edits to lead_snip_vg.py: nosing proud of the wedge (no coplanar faces), warm column colours, rewritten tunnel gate."""
p = r"C:\Users\Nitro\.kiro\crew\workspace\town\lead_snip_vg.py"
t = open(p, encoding='utf-8-sig').read()


def sub(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:70])
    t = t.replace(old, new)


sub("A.box((run + 0.1, SD + 0.5, 0.7), (sx, Y0 + SD / 2.0 - 0.15, z0 + hh - 0.35), P['stair_hi'], bev=0.1)",
    "A.box((run + 0.3, SD + 0.6, 0.8), (sx, Y0 + SD / 2.0 - 0.2, z0 + hh - 0.35 + 0.07), P['stair_hi'], bev=0.1)")
sub("A.box((7.0, SD + 0.5, 0.7), (lx, Y0 + SD / 2.0 - 0.15, z0 + per * rise - 0.35), P['stair_hi'], bev=0.1)",
    "A.box((7.3, SD + 0.6, 0.8), (lx, Y0 + SD / 2.0 - 0.2, z0 + per * rise - 0.35 + 0.07), P['stair_hi'], bev=0.1)")
sub("        G.column(A, x, y, 6.0, 1.9, h, FK, br, rnd)", "        G.column(A, x, y, 6.0, 1.9, h, KW, br, rnd)")
sub("    rnd = random.Random(7403)\n", "    rnd = random.Random(7403)\n    KW = dict(FK, stone=P['cliff2'], wall=P['cliff3'], trim=P['cliff4'])\n")
a = t.index('def _gate_tunnel():')
b = t.index('def _altar_ruin():')
new = '''def _gate_tunnel():
    """LM06_01 (round 3, lead) - fortress tunnel gate, 60 W x 60 D x 50 H: two grounded rock piers built as four thick stepped tiers with faceted bosses (no thin slabs),
    a three-tier lintel mass over a PASSABLE tunnel (mid-dark ceiling, paved floor), timber frame with braces, a stone sign block, warm banded colours, moss caps."""
    reset()
    A = Acc()
    rnd = random.Random(7600)
    W, D, H = 60.0, 60.0, 50.0
    ow, oh = 9.0, 18.0
    pw = W / 2.0 - ow
    fy = -25.5
    cols = [P['cliff1'], P['cliff2'], P['cliff3'], P['cliff4']]
    tiers = [(0.0, 14.0, 2.0, 51.0), (13.0, 13.0, 0.0, 49.0), (25.0, 12.5, -2.5, 46.0), (36.0, 12.0, -5.5, 42.0)]
    for sg in (-1, 1):
        for t, (zb, th, dw, dep) in enumerate(tiers):
            w = pw + dw
            A.box((w, dep, th + 0.6), (sg * (ow + w / 2.0), fy + dep / 2.0, zb + th / 2.0), cols[t], bev=0.6)
        A.box((pw - 7.0, 36.0, 2.0), (sg * (ow + (pw - 7.0) / 2.0 + 1.0), fy + 20.0, H - 0.2), P['moss'], bev=0.4)
    for t, (zb, ht, wx, dep) in enumerate(((oh, 10.5, 2.0, 49.0), (oh + 9.0, 11.5, 3.0, 47.0), (oh + 19.5, 11.5, 4.0, 42.0))):
        A.box((2 * ow + 2 * wx, dep, ht + 0.6), (0, fy + dep / 2.0 + 0.2 * t, zb + ht / 2.0), cols[t + 1], bev=0.6)
    A.box((2 * ow + 10.0, 36.0, 2.0), (0, fy + 20.0, H - 0.2), P['moss'], bev=0.4)
    A.box((2 * ow + 0.4, D - 12.0, 0.8), (0, 0, oh - 0.1), P['recess'], bev=0)
    A.box((2 * ow + 0.4, D - 10.0, 0.5), (0, 0, 0.25), P['tread'], bev=0)
    for k in range(18):
        z = rnd.uniform(5.0, H - 9.0)
        key = band(cols, z / H, rnd)
        sx, sy, sz = rnd.uniform(5.0, 9.0), rnd.uniform(4.0, 7.0), rnd.uniform(4.0, 8.0)
        face = k % 4
        if face == 0:
            x, y = rnd.choice((-1, 1)) * rnd.uniform(ow + 6.0, W / 2.0 - 5.0), fy + 0.6
        elif face == 1:
            x, y = rnd.uniform(-W / 2.0 + 6.0, W / 2.0 - 6.0), fy + 49.0 - 1.2
        else:
            x, y = rnd.choice((-1, 1)) * (W / 2.0 - 1.2), rnd.uniform(fy + 8.0, fy + 40.0)
        if abs(x) < ow + 5.0 and z < oh + 4.0:
            z += oh + 4.0
        A.chunk((sx, sy, sz), (x, y, z), key, (0, 0, rnd.uniform(-25, 25)), 0.15, rnd, (0.9, 0.9))
    for sg in (-1, 1):
        A.box((2.4, 2.4, oh + 1.0), (sg * (ow + 0.5), fy + 0.2, (oh + 1.0) / 2.0), R.P['timber'], bev=0.1)
        A.beam((sg * (ow + 0.5), fy - 0.9, oh - 3.5), (sg * (ow - 3.5), fy - 0.9, oh + 0.4), 0.9, 0.9, R.P['timber'])
        A.box((3.4, 3.4, 1.0), (sg * (ow + 0.5), fy + 0.2, 0.5), P['cliff3'], bev=0.1)
    A.box((2 * ow + 4.0, 2.4, 2.4), (0, fy + 0.2, oh + 1.4), R.P['timber'], bev=0.1)
    A.box((13.0, 3.0, 4.0), (0, fy + 0.6, oh + 5.2), P['wall'], bev=0.12)
    A.box((9.0, 0.6, 1.4), (0, fy - 1.1, oh + 5.2), P['cliff1'], bev=0)
    A.box((2 * ow + 8.0, 6.0, 0.6), (0, fy - 3.0, 0.3), P['tread'], bev=0.1)
    return _fin(A, 'gate_tunnel')


'''
t = t[:a] + new + t[b:]
open(p, 'w', encoding='utf-8').write(t)
print('snippet updated')
