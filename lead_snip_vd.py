PB = G.reg('vd_f', {
    'bronze': ((128, 96, 62), 'Metal', 0.3, 0.72),
    'bronze_d': ((92, 70, 50), 'Metal', 0.3, 0.75),
})


def hq_1():
    """CP15_01 (round 3, lead) - copy of ORIG.order_hq(1) with the gold star crest replaced by a matte bronze ring with a small crenellated tower glyph
    (no star, no gold, nothing bright)."""
    reset()
    A = Acc()
    rnd = random.Random(131)
    ORIG._stone_block(A, rnd, 56.0, 34.0, 28.0, 0, 0, 0, 3, True, True)
    A.gable(36.0, 58.0, 18.0, (0, 0, 28.0), K['cone'], (0, 0, 90))
    round_tower(A, rnd, 9.0, 56.0, K, -32.0, 8.0, 0, top='cone', roof_k=1.5, verts=22, flag=True)
    ORIG._stone_block(A, rnd, 22.0, 22.0, 20.0, 34.0, -4.0, 0, 2, True, False)
    A.frustum((24.0, 24.0), (2.0, 2.0), 14.0, (34.0, -4.0, 20.0), K['cone'])
    for i in range(7):
        A.box((24.0 - i * 1.2, 2.0, 1.0), (0, -17.0 - i * 1.6, 8.0 - i), K['stone'], bev=0.1)
    A.cyl(5.4, 0.8, (0, -18.1, 22.0), K['trim'], verts=24, rot=(90, 0, 0))
    A.cyl(4.5, 0.55, (0, -18.7, 22.0), PB['bronze'], verts=24, rot=(90, 0, 0))
    A.cyl(3.7, 0.7, (0, -18.7, 22.0), P['stone_d'], verts=24, rot=(90, 0, 0))
    A.box((1.9, 0.6, 4.2), (0, -19.3, 21.4), PB['bronze_d'], bev=0.05)
    for sx in (-0.65, 0.0, 0.65):
        A.box((0.5, 0.6, 0.9), (sx, -19.3, 23.9), PB['bronze_d'], bev=0.03)
    A.box((0.55, 0.7, 1.3), (0, -19.4, 20.2), P['stone_d'], bev=0)
    return _fin(A, 'order_hq')


def plaza_monument():
    """CP17_01 (round 3, lead) - copy of ORIG.plaza_monument with the gold urn finial and the flat star replaced by a dull bronze urn topped by a plain orb."""
    reset()
    A = Acc()
    for k in range(4):
        A.cyl(14.0 - k * 1.8, 0.7, (0, 0, k * 0.7), K['stone'], verts=24)
    A.cyl(9.0, 1.2, (0, 0, 2.8), K['trim'], verts=24)
    A.cyl(8.0, 0.9, (0, 0, 4.0), K['water'], verts=24)
    A.cyl(2.8, 10.0, (0, 0, 4.0), K['stone'], verts=16, r2=2.0)
    A.cyl(3.6, 1.0, (0, 0, 14.0), K['trim'], verts=16)
    A.cyl(1.4, 10.0, (0, 0, 15.0), K['stone'], verts=12, r2=1.1)
    A.cyl(2.2, 1.0, (0, 0, 25.0), K['trim'], verts=12)
    A.revolve([(1.6, 0.0), (1.4, 2.4), (0.8, 4.4), (1.2, 5.6), (0.6, 6.4)], (0, 0, 26.0), PB['bronze'], segs=10)
    A.ball(1.5, (0, 0, 33.0), PB['bronze'], segs=10, rings=6)
    for k in range(4):
        x, y, _ = polar(11.0, k * 90.0 + 45.0)
        A.box((2.0, 2.0, 1.8), (x, y, 0.9), K['stone'], (0, 0, k * 90.0 + 45.0), bev=0.1)
        A.cyl(0.9, 1.6, (x, y, 1.8), PB['bronze'], verts=8, r2=0.4)
    return _fin(A, 'plaza_monument')


def quay_2():
    """CP18_02 (round 3, lead) - a curved harbour quay as plain masonry: ashlar blocks laid along the arc (no hull stripes), a wide paved deck with a low kerb,
    short square stone bollards (no tall posts that read as funnels). 30 W x 8 H x 10 D."""
    reset()
    A = Acc()
    rnd = random.Random(302)
    R, nseg, a0, a1 = 22.0, 14, 0.0, 80.0
    for z in range(3):
        for j in range(nseg):
            a = a0 + (a1 - a0) * (j + 0.5) / nseg
            ln = math.radians((a1 - a0) / nseg) * (R - 1.0) * 1.07
            x, y, _ = polar(R - 1.0, a)
            A.chunk((ln, 4.2, 2.9), (x, y, 1.45 + z * 2.8), strata(STONES, z, 1), (0, 0, a + 90.0), 0.04, rnd)
    A.sweep([(R - 3.4, 8.2), (R + 1.4, 8.2), (R + 1.4, 8.9), (R - 3.4, 8.9)], a0, a1, 8, P['coping'])
    A.sweep([(R + 0.5, 8.9), (R + 1.4, 8.9), (R + 1.4, 10.0), (R + 0.5, 10.0)], a0, a1, 8, K['trim'])
    for a in (14.0, 40.0, 66.0):
        x, y, _ = polar(R - 1.4, a)
        A.box((1.5, 1.5, 1.5), (x, y, 8.9 + 0.7), K['stone'], (0, 0, a), bev=0.1)
        A.box((1.9, 1.9, 0.3), (x, y, 8.9 + 1.6), K['trim'], (0, 0, a), bev=0.05)
    return _fin(A, 'quay_wall')


# --- lead3 registration ---
BATCHES['lead3'] = ('v5_capital', mk([('CP15_01_order_hq_01', hq_1), ('CP17_01_plaza_features_01', plaza_monument)], 0.1))
