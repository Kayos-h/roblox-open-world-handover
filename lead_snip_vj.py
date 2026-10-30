def natural_gate():
    """RW01_02 (round 3, lead) - natural entrance gateposts: two rough posts of stacked sandstone blocks in graded warm colours (no plain grey), tapering and leaning a little, rope band,
    moss crowns, base stones that touch the posts; NO lintel (no freestanding arch). A timber signpost with a plank and a cream plaque stands between them. 24 x 7 x 20."""
    reset()
    A = Acc()
    rnd = random.Random(11002)
    for sg in (-1, 1):
        for k in range(4):
            w = 5.4 - k * 0.55
            d = 4.8 - k * 0.45
            A.chunk((w, d, 5.4), (sg * (9.5 - 0.2 * k) + rnd.uniform(-0.25, 0.25), rnd.uniform(-0.3, 0.3), 2.6 + k * 4.5), BANDS[k], (0, 0, rnd.uniform(-8, 8)), 0.07, rnd, (0.95, 0.95))
        A.box((5.6, 5.0, 0.5), (sg * 9.3, 0, 6.2), M['rope'], bev=0.04)
        A.ball(1.5, (sg * 8.7, 0, 20.0), P['moss'], segs=7, rings=4, scale=(1.4, 1.2, 0.5))
        for k in range(2):
            A.chunk((rnd.uniform(3.0, 4.2), rnd.uniform(2.6, 3.6), rnd.uniform(1.8, 2.6)), (sg * (9.5 + (1 if k else -1) * 3.2), rnd.uniform(-1.2, 1.2), 1.0), BANDS[k], (0, 0, rnd.uniform(0, 90)), 0.1, rnd)
    A.cyl(0.4, 9.0, (0, 1.6, 0.0), M['plank'], verts=6)
    A.box((6.0, 0.5, 2.8), (0, 1.35, 6.4), M['plank'], bev=0.05)
    A.box((5.0, 0.12, 1.9), (0, 1.0, 6.4), P['cream'], bev=0)
    A.box((6.4, 0.5, 0.4), (0, 1.35, 8.1), M['plank'], bev=0)
    ob = _fin(A, 'natural_entrance_gateposts')
    return v5kit.fit(ob, w=24.3, d=7.0, h=19.8)


# --- lead3 registration ---
BATCHES['lead3'] = ('v5_rework', [('RW01_02_rework_existing_02', natural_gate)])
