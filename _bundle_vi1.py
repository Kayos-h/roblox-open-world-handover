def _burnt_house(i):
    reset()
    A = Acc()
    rnd = random.Random(10200 + i)
    A.box((22.0, 20.0, 0.8), (0, 0, 0.4), V['ash'], bev=0.1)
    if i % 2 == 1:                                                                               # standing shell with a fallen roof
        BK = dict(RK, wall=V['char'] if i == 1 else V['stone2'], roof=V['char'], timber=V['char'], roof2=V['ash'], cap=V['ash'], shutter=V['char'], door=V['char'])
        house(A, rnd, 14.0, 11.0, 1 + (i == 3), BK, cx=-2.0, hs=5.4, jetty=0.0, pitch=0.7, shutters=False)
        A.gable(12.0, 11.0, 3.8, (5.0, 4.0, 0.8), V['char'], (22, -10, 24))
        for k in range(6):
            A.beam((-4.0 + k * 2.4, 6.0, 5.0), (-4.0 + k * 2.4 + rnd.uniform(-2, 2), 9.0, 0.9 + rnd.uniform(0, 2)), 0.45, 0.45, V['char'])
    else:
        w, d = 14.0, 11.0
        for (x, y, ww, dd, h) in ((0, 0, w, 0.9, 8.0), (-w / 2, d / 2, 0.9, d, 6.0), (w / 2, d / 2, 0.9, d, 3.5), (0, d, w * 0.6, 0.9, 5.0)):
            A.chunk((ww, dd, h * rnd.uniform(0.6, 1.0)), (x, y - d / 2 + (d / 2 if dd > 3 else 0.0), 0.8 + h / 2), V['char'] if i % 2 == 0 and i != 0 else V['stone2'], (0, 0, 0), 0.08, rnd, (0.96, 0.96))
        for k in range(4):
            A.box((1.8, 0.6, 2.6), (-w / 2 + 3.0 + k * (w - 5.0) / 3.0, -0.5 - d / 2 + d / 2, 4.4), V['dark'], bev=0)
        for k in range(8):
            A.beam((-w / 2 + k * 2.0, -d / 2, 5.0), (-w / 2 + k * 2.0 + rnd.uniform(-1, 1), d / 2, 5.0 + rnd.uniform(-2, 4)), 0.5, 0.5, V['char'])
        A.box((2.0, 2.0, 12.0), (w / 2 - 1.0, d / 2, 6.0), V['stone2'], bev=0.1)
    for k in range(22):
        A.chunk((rnd.uniform(1.0, 3.0), rnd.uniform(1.0, 3.0), rnd.uniform(0.4, 1.4)), (rnd.uniform(-10, 10), rnd.uniform(-9, 9), 1.0), V['char'] if k % 2 else V['ash'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(8):
        A.cyl(0.12, rnd.uniform(1.0, 2.6), (rnd.uniform(-8, 8), rnd.uniform(-6, 6), 0.8), V['char'], verts=5, r2=0.05)
    for k in range(5):
        A.cyl(0.4, rnd.uniform(1.4, 2.4), (rnd.uniform(-9, 9), rnd.uniform(-8, 0), 0.8), V['char'], verts=6, rot=(90, 0, rnd.uniform(0, 180)))
    return _fin(A, 'collapsed_house')
