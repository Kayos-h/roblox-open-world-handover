PBZ = G.reg('va_f', {
    'bronze': ((112, 88, 62), 'Metal', 0.3, 0.75),
})


def cairn():
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


def lantern_post():
    """WT13_06 (round 3, lead) - same plaza as before, but the lantern no longer reads as glowing: a stone lantern house in muted stone with four dark openings (no parchment
    yellow), dull bronze posts and finial."""
    reset()
    A = Acc()
    rnd = random.Random(2406)
    A.cyl(14.5, 0.6, (0, 0, 0), P['stone_d'], verts=36)
    A.cyl(13.4, 0.4, (0, 0, 0.6), P['stone_m'], verts=36)
    for k in range(16):
        a = 22.5 * k
        A.box((13.2, 0.35, 0.4), (0, 0, 0.9), P['joint'], (0, 0, a), bev=0)
    for rr in (5.0, 9.5):
        A.sweep([(rr - 0.18, 0.7), (rr + 0.18, 0.7), (rr + 0.18, 1.0), (rr - 0.18, 1.0)], 0, 360, 40, P['joint'])
    for k in range(28):
        a = 360.0 / 28 * k
        x, y, _ = polar(13.9, a)
        A.box((3.2, 1.4, 1.1), (x, y, 0.95), band(COURSE, 0.3 + 0.4 * (k % 2), rnd), (0, 0, a + 90), bev=0.08)
    A.sweep([(13.2, 1.5), (14.6, 1.5), (14.6, 2.0), (13.2, 2.0)], 0, 360, 40, P['trim'])
    A.cyl(2.6, 1.0, (0, 0, 1.0), P['stone_d'], verts=12)
    A.box((1.6, 1.6, 4.4), (0, 0, 3.6), P['stone_m'], bev=0.1)
    for z in (2.6, 4.4):
        A.box((2.0, 2.0, 0.4), (0, 0, z), P['trim'], bev=0.08)
    A.box((2.4, 2.4, 0.5), (0, 0, 6.0), P['trim'], bev=0.08)
    A.box((1.9, 1.9, 2.0), (0, 0, 7.2), P['stone_a'], bev=0.06)
    for sx, sy in ((1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0)):
        A.box((0.1, 0.9, 1.1) if sx else (0.9, 0.1, 1.1), (sx * 0.95, sy * 0.95, 7.2), P['throat'], bev=0)
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        A.box((0.18, 0.18, 2.1), (sx * 0.85, sy * 0.85, 7.2), PBZ['bronze'])
    A.cyl(1.7, 1.3, (0, 0, 8.2), P['stone_d'], verts=8, r2=0.2)
    A.ball(0.35, (0, 0, 9.6), PBZ['bronze'], segs=6, rings=4)
    for k in (60, 150, 240, 330):
        x, y, _ = polar(9.4, k)
        A.box((6.6, 1.8, 1.0), (x, y, 1.4), P['stone_m'], (0, 0, k + 90), bev=0.1)
        A.box((6.8, 2.0, 0.3), (x, y, 2.0), P['trim'], (0, 0, k + 90), bev=0.06)
        for e in (-1, 1):
            ox = math.cos(math.radians(k + 90)) * e * 2.6
            oy = math.sin(math.radians(k + 90)) * e * 2.6
            A.box((1.0, 1.4, 1.2), (x + ox, y + oy, 0.9), P['stone_d'], (0, 0, k + 90), bev=0.08)
    return _fin(A, 'lantern_post')
