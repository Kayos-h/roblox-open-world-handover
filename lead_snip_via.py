ROCKL = [P['r_base'], P['r_low'], P['r_rust'], P['r_mid'], P['r_hi']]


def _magic_ruin(i):
    """LM20_02 (round 3, lead) - arcane ruin, 40 x 40 x 40, built at full size (the old pillars were 24 high and got stretched to 40, which made them look thin):
    a broken dais, two tall rune pillars at the back with a fallen lintel in front, six standing stones with two trilithon lintels, a central stepped rune altar with an obelisk shard,
    a rune inlay ring, rubble that rests ON the dais."""
    reset()
    A = Acc()
    rnd = random.Random(5300 + i)
    A.cyl(19.4, 1.6, (0, 0, 0), P['s_base'], verts=24, r2=18.4)
    A.cyl(16.0, 0.8, (0, 0, 1.6), P['s_mid'], verts=24, r2=15.0)
    zt = 2.4
    for sx in (-1, 1):
        A.chunk((5.0, 5.0, 35.0), (sx * 11.0, 9.0, zt + 17.5), band(STON, 0.5, rnd), (0, 0, 0), 0.04, rnd, (0.85, 0.85))
        A.box((6.4, 6.4, 1.4), (sx * 11.0, 9.0, zt + 0.7), P['s_warm'], bev=0.1)
        for z in (9.0, 16.0, 23.0, 30.0):
            A.box((4.8, 0.7, 1.5), (sx * 11.0, 9.0 - 2.6, z), V['rune'], bev=0)
    A.chunk((26.0, 4.6, 4.2), (-3.0, -9.0, zt + 2.1), band(STON, 0.6, rnd), (0, 0, 12), 0.06, rnd)
    pair_h = (11.0, 11.0, 9.0, 7.0, 12.0, 12.0)
    angs = (190.0, 226.0, 262.0, 298.0, 334.0, 10.0)
    pts = []
    for k, (a, hh) in enumerate(zip(angs, pair_h)):
        x, y, _ = polar(13.0, a)
        pts.append((x, y, hh))
        A.chunk((3.4, 2.8, hh), (x, y, zt + hh / 2.0), band(STON, 0.35 + 0.1 * (k % 3), rnd), (0, 0, a + 90.0), 0.06, rnd, (0.9, 0.9))
        A.box((4.0, 3.4, 0.6), (x, y, zt + 0.3), P['s_warm'], (0, 0, a + 90.0), bev=0.06)
        A.box((3.0, 0.5, 1.2), (x + math.cos(math.radians(a + 270.0)) * 1.55, y + math.sin(math.radians(a + 270.0)) * 1.55, zt + hh * 0.55), V['rune'], (0, 0, a + 90.0), bev=0)
    for (p, q) in ((pts[0], pts[1]), (pts[4], pts[5])):
        mx, my = (p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0
        ln = math.hypot(q[0] - p[0], q[1] - p[1]) + 3.0
        ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
        A.chunk((ln, 2.8, 1.8), (mx, my, zt + p[2] + 0.8), band(STON, 0.8, rnd), (0, 0, ang), 0.05, rnd)
    A.cyl(4.8, 0.8, (0, -1.0, zt), P['s_base'], verts=16, r2=4.4)
    A.cyl(3.5, 0.8, (0, -1.0, zt + 0.8), P['s_mid'], verts=16, r2=3.2)
    A.box((3.4, 3.4, 2.2), (0, -1.0, zt + 1.6 + 1.1), band(STON, 0.55, rnd), bev=0.1)
    A.box((3.6, 0.5, 0.7), (0, -1.0 - 1.72, zt + 3.0), V['rune'], bev=0)
    A.chunk((2.4, 2.4, 6.0), (2.2, -3.0, zt + 1.6 + 3.0), band(STON, 0.8, rnd), (0, 0, 20), 0.08, rnd, (0.45, 0.45))
    for k in range(10):
        a = k * 36.0
        x, y, _ = polar(9.0, a)
        A.box((1.6, 0.6, 0.3), (x, y, zt + 0.05), V['rune'], (0, 0, a + 90), bev=0)
    for k in range(11):
        s = rnd.uniform(2, 3.8)
        hh = rnd.uniform(1.2, 2.6)
        x, y, _ = polar(rnd.uniform(5, 16.5), rnd.uniform(0, 360))
        A.chunk((s, s, hh), (x, y, zt + hh / 2.0 - 0.2), band(STON, rnd.uniform(0, 0.5), rnd), (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(3):
        _moss_patch(A, rnd, rnd.uniform(-12, 12), rnd.uniform(-14, 4), 2.4, rnd.uniform(1.4, 2.4))
    return _fin(A, 'magic_ruin')


def _float_rock(i):
    """LM21 floating rocks (round 3, lead) - built at the manifest size (40 x 30 x 40) so nothing is stretched: a SOLID root of stacked banded frustum slices (two sets turned 45 degrees,
    so the root is eight-sided with no gaps and no wafers), faceted bosses that sit in the root, a soil rim and a grass cap with moss."""
    reset()
    A = Acc()
    rnd = random.Random(5400 + i)
    topw, topd = (38.0, 36.0) if i == 0 else (34.0, 38.0)
    ramp = ROCKC if i == 0 else ROCKW
    H = 23.0
    nsl = 6
    for turn, sc in ((0.0, 1.0), (45.0, 0.9)):
        for s in range(nsl):
            t0, t1 = s / float(nsl), (s + 1) / float(nsl)
            w0, w1 = (4.0 + (topw - 4.0) * t0) * sc, (4.0 + (topw - 4.0) * t1) * sc
            d0, d1 = (4.0 + (topd - 4.0) * t0) * sc, (4.0 + (topd - 4.0) * t1) * sc
            A.frustum((w0, d0), (w1, d1), H / nsl + 0.4, (0, 0, 1.0 + t0 * H), ramp[min(len(ramp) - 1, int((t0 + 0.08 * turn / 45.0) * len(ramp)))], (0, 0, turn))
    for k in range(10):
        t = rnd.uniform(0.2, 0.85)
        a = rnd.uniform(0, 360)
        r = (4.0 + (min(topw, topd) - 4.0) * t) * 0.5 - 1.6
        x, y, _ = polar(r, a)
        A.chunk((rnd.uniform(6, 9), rnd.uniform(6, 9), rnd.uniform(6, 10)), (x, y, 1.0 + t * H), band(ramp, t, rnd), (rnd.uniform(-8, 8), rnd.uniform(-8, 8), a), 0.14, rnd, (0.7, 0.7))
    A.chunk((topw + 1.0, topd + 1.0, 1.8), (0, 0, 24.0), P['dirt'], (0, 0, i * 20), 0.05, rnd)
    A.chunk((topw, topd, 3.0), (0, 0, 25.6), P['grass'], (0, 0, i * 20), 0.06, rnd)
    for k in range(5):
        x, y, _ = polar(rnd.uniform(3, topw * 0.35), rnd.uniform(0, 360))
        _moss_patch(A, rnd, x, y, 26.9, rnd.uniform(1.2, 2.0))
    return _fin(A, 'floating_rock')
