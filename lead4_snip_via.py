def _arcane_shards():
    """LM20_01 (lead pass 2) - arcane ruin of standing shards: nine tall pointed stone shards of different heights on a dais, footings, rune bands, grounded rubble."""
    reset()
    A = Acc()
    rnd = random.Random(5201)
    A.cyl(19.0, 1.6, (0, 0, 0), P['s_base'], verts=24, r2=18.0)
    A.cyl(15.0, 0.8, (0, 0, 1.6), P['s_mid'], verts=24, r2=14.0)
    zt = 2.4
    for k in range(9):
        a = k * 40.0 + rnd.uniform(-10, 10)
        rr = rnd.uniform(6.0, 14.0) if k else 0.0
        x, y, _ = polar(rr, a)
        h = rnd.uniform(14.0, 34.0) if k % 3 else 37.0
        w = rnd.uniform(3.4, 5.2)
        A.chunk((w, w * rnd.uniform(0.7, 1.0), h), (x, y, zt + h / 2.0), band(STON, 0.15 + 0.7 * (k % 4) / 3.0, rnd), (rnd.uniform(-5, 5), rnd.uniform(-5, 5), a), 0.1, rnd, (0.4, 0.4))
        A.box((w + 1.4, w + 1.4, 0.8), (x, y, zt + 0.4), P['s_warm'], (0, 0, a), bev=0.06)
        A.box((w * 0.8, 0.5, 1.5), (x - math.sin(math.radians(a)) * (w * 0.5), y + math.cos(math.radians(a)) * (w * 0.5), zt + h * 0.45), V['rune'], (0, 0, a), bev=0)
    for k in range(10):
        s = rnd.uniform(2, 3.8)
        hh = rnd.uniform(1.2, 2.4)
        x, y, _ = polar(rnd.uniform(4, 17), rnd.uniform(0, 360))
        A.chunk((s, s, hh), (x, y, zt + hh / 2.0 - 0.2), band(STON, rnd.uniform(0, 0.5), rnd), (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(3):
        _moss_patch(A, rnd, rnd.uniform(-12, 12), rnd.uniform(-12, 12), 2.4, rnd.uniform(1.4, 2.2))
    return _fin(A, 'magic_ruin')


def _arcane_monolith():
    """LM20_03 (lead pass 2) - arcane ruin with ONE great carved monolith on a three-step round dais, rune bands, four low corner posts, a fallen cap slab."""
    reset()
    A = Acc()
    rnd = random.Random(5203)
    A.cyl(19.0, 1.6, (0, 0, 0), P['s_base'], verts=24, r2=18.0)
    A.cyl(15.0, 1.2, (0, 0, 1.6), P['s_mid'], verts=24, r2=14.0)
    A.cyl(11.0, 1.2, (0, 0, 2.8), P['s_warm'], verts=24, r2=10.0)
    zt = 4.0
    A.chunk((8.0, 6.0, 31.0), (0, 0, zt + 15.5), band(STON, 0.5, rnd), (0, 0, 0), 0.04, rnd, (0.82, 0.82))
    A.frustum((6.6, 4.8), (0.6, 0.6), 5.0, (0, 0, zt + 31.0), P['s_hi'])
    for z in (9.0, 15.0, 21.0, 27.0):
        A.box((6.2, 0.7, 1.6), (0, -3.0 - (z - 9.0) * 0.004, zt + z), V['rune'], bev=0)
        A.box((0.7, 5.0, 1.6), (4.0 - (z - 9.0) * 0.012, 0, zt + z), V['rune'], bev=0)
    for k in range(4):
        x, y, _ = polar(13.5, 45 + k * 90.0)
        A.chunk((3.0, 3.0, 6.0 + k * 1.5), (x, y, 1.6 + (6.0 + k * 1.5) / 2.0), band(STON, 0.3, rnd), (0, 0, 45 + k * 90.0), 0.08, rnd, (0.8, 0.8))
        A.box((3.8, 3.8, 0.7), (x, y, 1.95), P['s_warm'], (0, 0, 45 + k * 90.0), bev=0.05)
    A.chunk((9.0, 4.0, 2.6), (6.5, -12.0, 3.0), band(STON, 0.7, rnd), (0, 0, 28), 0.08, rnd)
    for k in range(8):
        s = rnd.uniform(2, 3.6)
        hh = rnd.uniform(1.2, 2.4)
        x, y, _ = polar(rnd.uniform(6, 17), rnd.uniform(0, 360))
        A.chunk((s, s, hh), (x, y, 2.6 + hh / 2.0 - 0.2), band(STON, rnd.uniform(0, 0.5), rnd), (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(3):
        _moss_patch(A, rnd, rnd.uniform(-12, 12), rnd.uniform(-12, 12), 2.6, rnd.uniform(1.4, 2.2))
    return _fin(A, 'magic_ruin')


def _arena_bands(A):
    R_, wth, cy = 34.0, 4.0, 34.0
    a0, a1 = 54.0, 126.0
    for z in (8.0, 16.0, 24.0):
        A.sweep([(R_ - wth / 2 - 0.4, z), (R_ - wth / 2, z), (R_ - wth / 2, z + 0.8), (R_ - wth / 2 - 0.4, z + 0.8)], a0, a1, 22, P['s_dk'], loc=(0, cy, 0), rot=(0, 0, 180))


def _columns_post(A):
    for (cx, cy) in ((0.0, 0.0), (6.0, 3.0), (-6.0, -2.0)):
        A.cyl(3.5, 0.9, (cx, cy, 1.1), P['s_warm'], verts=14)
        A.cyl(3.1, 0.6, (cx, cy, 1.9), P['s_hi'], verts=14)


def _stump_post(i):
    def post(A):
        rt = 10.5 if i == 0 else 10.9
        for k, (a, z) in enumerate(((20.0, 14.0), (140.0, 22.0), (260.0, 10.0))):
            x, y, _ = polar(rt, a)
            A.box((1.6, 2.2, 4.0), (x, y, z), P['void'], (0, 0, a), bev=0)
            A.box((2.4, 2.4, 0.7), (x, y, z + 2.2), P['s_hi'], (0, 0, a), bev=0.05)
            A.box((2.4, 2.4, 0.6), (x, y, z - 2.2), P['s_hi'], (0, 0, a), bev=0.05)
        if i == 1:
            for k in range(5):
                x, y, _ = polar(13.5 + k * 0.8, 200 + k * 16.0)
                A.chunk((4.0 - k * 0.4, 3.0, 2.6), (x, y, 1.3), P['s_base'], (0, 0, 200 + k * 16.0), 0.15, random.Random(k + 3))
    return post


def _watch_post(i):
    def post(A):
        rt = 8.2 if i != 1 else 8.6
        for a, z in ((70.0, 18.0), (190.0, 26.0), (310.0, 12.0)):
            x, y, _ = polar(rt, a)
            A.box((1.4, 1.8, 3.4), (x, y, z), P['void'], (0, 0, a), bev=0)
            A.box((2.2, 2.2, 0.6), (x, y, z + 2.0), P['s_hi'], (0, 0, a), bev=0.05)
        for k in range(3):
            x, y, _ = polar(rt + 0.3, 30 + k * 120.0)
            A.box((1.4, 1.2, 14.0 + k * 3.0), (x, y, 7.0 + k * 1.5), P['s_dk'], (0, 0, 30 + k * 120.0), bev=0.08)
    return post


def lm20_01():
    return LK.wrap(_arcane_shards)()


def lm20_03():
    return LK.wrap(_arcane_monolith)()


def lm26_02():
    return LK.wrap(lambda: _arena(1), prune=[dict(keys=None, max_size=4.2, max_z=1.2)])()


def lm26_03():
    return LK.wrap(lambda: _arena(2), post=_arena_bands, recolor=[LK.ramp([STON[1], STON[2]], [P['s_dk'], P['s_base'], P['s_mid'], P['s_warm']], zlim=(2.0, 31.0), trange=(0.0, 31.0), wobble=0.05)])()


def lm28_02():
    return LK.wrap(lambda: _columns(1), prune=[dict(keys=None, max_size=5.4, max_z=3.5)], post=_columns_post)()


def lm29_01():
    return LK.wrap(lambda: _stump(0), post=_stump_post(0), recolor=[LK.ramp(STON, [P['s_dk'], P['s_base'], P['s_mid'], P['s_hi']], trange=(0.0, 36.0), wobble=0.06)])()


def lm29_02():
    return LK.wrap(lambda: _stump(1), post=_stump_post(1), recolor=[LK.ramp(STON, [P['s_dk'], P['s_warm'], P['s_base'], P['s_warm']], trange=(0.0, 34.0), wobble=0.06)])()


def pl02_01():
    return LK.wrap(lambda: _hay(0), recolor=[LK.ramp([P['straw'], P['straw2']], [PS['straw4'], PS['straw3'], PS['straw3'], PS['straw5']], trange=(0.0, 24.0), wobble=0.05)])()


def pl05(i):
    return LK.wrap(lambda: _watch(i), post=_watch_post(i), recolor=[LK.ramp(STON, [P['s_dk'], P['s_base'], P['s_mid'], P['s_warm']], trange=(0.0, 42.0), wobble=0.06)])()


# --- lead4 registration ---
import v5_leadkit as LK
PS = G.reg('vi_fa', {
    'straw3': ((196, 170, 108), 'Fabric', 0.0, 1.0),
    'straw4': ((170, 142, 88), 'Fabric', 0.0, 1.0),
    'straw5': ((214, 190, 128), 'Fabric', 0.0, 1.0),
})
BATCHES['lead4_via'] = ('v5_landmarks', mk([('LM20_01_crater_arcane_ruin_01', lm20_01), ('LM20_03_crater_arcane_ruin_03', lm20_03), ('LM26_02_ruin_arena_segment_02', lm26_02),
                                            ('LM26_03_ruin_arena_segment_03', lm26_03), ('LM28_02_ruin_column_set_02', lm28_02), ('LM29_01_ruin_tower_stump_01', lm29_01),
                                            ('LM29_02_ruin_tower_stump_02', lm29_02)], 0.1))
BATCHES['lead4_via_plains'] = ('v5_plains', mk([('PL02_01_hay_silo_01', pl02_01), ('PL05_01_ruined_watchtower_plains_01', lambda: pl05(0)),
                                                ('PL05_02_ruined_watchtower_plains_02', lambda: pl05(1)), ('PL05_03_ruined_watchtower_plains_03', lambda: pl05(2))], 0.1))
