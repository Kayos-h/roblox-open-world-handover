def _town(kind, seed):
    reset()
    A = Acc()
    rnd = random.Random(seed)
    if kind == 'corner':
        house(A, rnd, 18.0, 13.0, 2, K, cx=0, cy=0, hs=6.2, jetty=0.9, pitch=0.7, sign=False, balcony=True)
        house(A, rnd, 12.0, 17.0, 2, K, cx=8.0, cy=12.0, hs=6.2, jetty=0.9, pitch=0.7, ridge_x=False, chimney=False, door=False)
    elif kind == 'tall':
        house(A, rnd, 14.0, 14.0, 3, K, hs=6.4, jetty=1.0, pitch=0.85, dormers=1, sign=False)
    elif kind == 'courtyard':
        house(A, rnd, 22.0, 10.0, 2, K, cx=0, cy=8.0, hs=6.2, jetty=0.8, pitch=0.7)
        house(A, rnd, 9.0, 18.0, 2, K, cx=-12.0, cy=-4.0, hs=6.2, jetty=0.8, pitch=0.7, ridge_x=False, chimney=False, door=False)
        house(A, rnd, 9.0, 18.0, 2, K, cx=12.0, cy=-4.0, hs=6.2, jetty=0.8, pitch=0.7, ridge_x=False, door=False)
        A.box((8.0, 6.0, 0.4), (0, -8.0, 0.2), K['stone'])
    elif kind == 'arcade':
        house(A, rnd, 22.0, 13.0, 2, K, hs=6.6, jetty=0.9, pitch=0.68, arcade=True, dormers=1, shutters=True, door=False)
    elif kind == 'inn':
        house(A, rnd, 22.0, 15.0, 2, K, hs=6.4, jetty=1.0, pitch=0.72, dormers=2, balcony=True, sign=True)
    elif kind == 'guild':
        house(A, rnd, 22.0, 16.0, 2, K, hs=7.4, jetty=1.0, pitch=0.62, dormers=2, belfry=(seed % 2 == 0))
    elif kind == 'market':
        A.box((22.0, 20.0, 1.0), (0, 0, 0.5), K['stone'])
        for sx in (-1, 1):
            for sy in range(4):
                A.box((1.0, 1.0, 9.0), (sx * 10.0, -8.4 + sy * 5.6, 5.5), K['timber'], bev=0.1)
                A.box((2.0, 2.0, 0.6), (sx * 10.0, -8.4 + sy * 5.6, 1.3), K['stone'])
        A.box((22.4, 21.0, 0.9), (0, 0, 10.2), K['timber'])
        A.gable(23.0, 24.0, 10.0, (0, 0, 10.6), K['roof'], (0, 0, 90))
        for k in range(5):
            A.box((3.0, 1.6, 1.0), (-8.0 + k * 4.0, -6.0, 1.6), K['sign'], bev=0.05)
            A.box((2.4, 1.2, 0.9), (-8.0 + k * 4.0, 4.0, 1.6), K['wall'], bev=0.05)
        A.box((2.2, 2.2, 2.6), (0, 0, 20.8), K['wall'])
        A.cyl(1.9, 2.5, (0, 0, 23.4), K['cone'], verts=6, r2=0.0)
    return _fin(A, 'townhouse_new')
