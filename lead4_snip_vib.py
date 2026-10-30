def _float_small(i):
    """FL02_01..03 (lead pass 2) - small floating island built as a SOLID root of stacked banded frustum slices (two sets turned 45 degrees, no gaps, nothing loose),
    three different root profiles (cone, bulb, crooked with hanging tips) and three different rock tones, soil rim, grass cap, ivy."""
    reset()
    A = Acc()
    rnd = random.Random(10700 + i)
    topw = (32.0, 30.0, 34.0)[i]
    prof = ([0.12, 0.28, 0.44, 0.60, 0.76, 0.90, 1.0], [0.10, 0.20, 0.55, 0.78, 0.92, 0.97, 1.0], [0.18, 0.26, 0.38, 0.56, 0.78, 0.94, 1.0])[i]
    ramp = ([P['rock_lo'], P['rock_warm'], P['rock_mid'], P['rock_hi']], [P['rock_lo'], P['rock_mid'], P['rock_hi']], [P['rock_warm'], P['rock_mid'], P['rock_hi'], P['rock_warm']])[i]
    H = 20.0
    n = len(prof) - 1
    for turn, sc in ((0.0, 1.0), (45.0, 0.9)):
        for s in range(n):
            w0 = (3.0 + (topw - 3.0) * prof[s]) * sc
            w1 = (3.0 + (topw - 3.0) * prof[s + 1]) * sc
            A.frustum((w0, w0 * 0.95), (w1, w1 * 0.95), H / n + 0.3, (0, 0, 1.0 + H * s / n), ramp[min(len(ramp) - 1, int(s / float(n) * len(ramp)))], (0, 0, turn))
    for k in range(7):
        t = rnd.uniform(0.25, 0.85)
        a = rnd.uniform(0, 360)
        x, y, _ = polar(((3.0 + (topw - 3.0) * t) * 0.5) - 1.5, a)
        A.chunk((rnd.uniform(4, 7), rnd.uniform(4, 7), rnd.uniform(4, 8)), (x, y, 1.0 + t * H), band(ramp, t, rnd), (rnd.uniform(-8, 8), rnd.uniform(-8, 8), a), 0.14, rnd, (0.7, 0.7))
    if i == 2:
        for sx, sy in ((-2.0, 1.0), (2.5, -1.5), (0.5, 2.5)):
            A.chunk((2.4, 2.4, 6.0), (sx, sy, 2.0), ramp[0], (0, 0, rnd.uniform(0, 90)), 0.12, rnd, (0.4, 0.4))
    A.chunk((topw + 1.0, topw * 0.95 + 1.0, 1.8), (0, 0, 21.4), P['dirt'], (0, 0, i * 20), 0.05, rnd)
    A.chunk((topw, topw * 0.95, 2.6), (0, 0, 23.0), R.V['grass'], (0, 0, i * 20), 0.06, rnd)
    for k in range(5):
        A.ball(rnd.uniform(1.2, 2.2), (rnd.uniform(-9, 9), rnd.uniform(-9, 9), 24.2), R.V['ivy'], segs=7, rings=4, scale=(1.3, 1.1, 0.8))
    return _fin(A, 'floating_rock')


def _harbour_post(A):
    for z in (4.0, 13.0, 22.0):
        w = 13.0 - 4.0 * (z / 30.0) + 0.6
        A.box((w, w, 0.8), (0, 0, z), R.V['trim'], bev=0.05)
    for sx in (-1, 1):
        A.box((0.45, 12.6, 0.4), (sx * 6.0, 0, 34.2), R.V['iron'], bev=0)
        A.box((12.6, 0.45, 0.4), (0, sx * 6.0, 34.2), R.V['iron'], bev=0)


def _trading_b():
    reset()
    A = Acc()
    rnd = random.Random(10011)
    G.house(A, rnd, 20.0, 12.0, 2, R.RK, hs=5.8, jetty=0.6, pitch=0.8, sign=True, hip=True, dormers=1, balcony=True)
    V_ = R.V
    for k in range(3):
        A.box((3.4, 1.8, 1.4), (-9.0 + k * 4.4, -9.5, 0.7), V_['plank'], bev=0.08)
        A.box((3.8, 2.2, 0.2), (-9.0 + k * 4.4, -9.5, 4.2), (V_['canvas3'], V_['canvas'], V_['canvas2'])[k % 3], bev=0)
        for sx in (-1.6, 1.6):
            A.cyl(0.12, 4.0, (-9.0 + k * 4.4 + sx, -9.5, 0), V_['timber'], verts=5)
    for k in range(3):
        A.cyl(0.9, 1.7, (7.0 + k * 1.2, -9.0, 0), V_['timber'], verts=8)
    A.box((3.0, 2.0, 2.0), (-12.5, -3.0, 1.0), V_['plank'], bev=0.08)
    return _fin(A, 'trading_post')


def fl02(i):
    return LK.wrap(lambda: _float_small(i))()


def hb01_02():
    return LK.wrap(lambda: R._harbour_tower(1), post=_harbour_post)()


def rd04_02():
    return LK.wrap(_trading_b)()


# --- lead4 registration ---
import v5_leadkit as LK
BATCHES['lead4_vib'] = ('v5_coast', mk([('FL02_01_floating_island_small_01', lambda: fl02(0)), ('FL02_02_floating_island_small_02', lambda: fl02(1)),
                                        ('FL02_03_floating_island_small_03', lambda: fl02(2)), ('HB01_02_harbour_wall_tower_02', hb01_02)], 0.1))
BATCHES['lead4_vib_roads'] = ('v5_roads', mk([('RD04_02_trading_post_02', rd04_02)], 0.1))
