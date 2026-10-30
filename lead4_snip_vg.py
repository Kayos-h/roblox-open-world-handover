def _glacier_post(A):
    r_ = random.Random(3211)
    A.chunk((62.0, 46.0, 6.0), (0, -2.0, 3.0), R.ICE[0], (0, 0, 0), 0.05, r_, (0.96, 0.96))
    A.chunk((52.0, 34.0, 6.0), (0, 4.0, 8.5), R.ICE[1], (0, 0, 0), 0.05, r_, (0.94, 0.94))
    A.chunk((40.0, 22.0, 5.0), (0, 9.0, 13.0), R.ICE[2], (0, 0, 0), 0.05, r_, (0.9, 0.9))


def _span_post(A):
    n = 18
    for k in range(n - 1):
        t = (k + 0.5) / (n - 1.0)
        x = -34.0 + 68.0 * t
        z = 17.0 + math.sin(math.pi * t) * 3.0
        A.box((4.6, 8.6, 1.5), (x, 0, z - 1.35), R.P['stoneM'], bev=0.1)


def _board_post(A):
    for sg in (-1, 1):
        for k in range(7):
            A.cyl(0.24, 3.2, (-14.0 + k * 4.7, sg * 2.65, 3.15), R.P['bark'], verts=6)
        A.box((30.0, 0.36, 0.36), (0, sg * 2.65, 6.3), R.P['timber'], bev=0)
        A.box((30.0, 0.3, 0.3), (0, sg * 2.65, 4.8), R.P['timber'], bev=0)


def fr02_01():
    return LK.wrap(lambda: R._forest_ruin(0), recolor=[LK.ramp([R.P['stoneM'], R.P['rock2'], R.P['rock']], CROCK, wobble=0.07)])()


def fr02_02():
    return LK.wrap(lambda: R._forest_ruin(1), recolor=[LK.ramp([R.P['stoneM'], R.P['rock2'], R.P['rock']], [P['cliff2'], P['cliff3'], P['cliff4']], wobble=0.07)])()


def fr02_03():
    return LK.wrap(lambda: R._forest_ruin(2), recolor=[LK.ramp([R.P['stoneM'], R.P['rock2'], R.P['rock']], [P['cliff1'], P['cliff2'], P['cliff3']], wobble=0.07)])()


def fr03_01():
    return LK.wrap(lambda: _cave_mouth_big(0))()


def hl03_02():
    return LK.wrap(lambda: _glacier(1), prune=[dict(keys=None, max_size=8.5, max_z=9.0)], post=_glacier_post)()


def lm05_01():
    return LK.wrap(lambda: R._cliff_tower(0), recolor=[LK.ramp(R.ROCK, CROCK, trange=(0.0, 45.0), wobble=0.07)])()


def lm05_02():
    return LK.wrap(_cliff_tower2, prune=[dict(keys=None, max_size=16.0, thin=2.5, max_z=6.0), dict(keys=[P['moss'], P['lichen']], max_size=1.8)])()


def lm08_01():
    return LK.wrap(stone_span, post=_span_post)()


def lm24_01():
    return LK.wrap(lambda: R._pool_rock(0), recolor=[LK.ramp(R.ROCK, CROCK, trange=(0.0, 16.0), wobble=0.08)])()


def sp01_04():
    return LK.wrap(lambda: _snow_spire_wide(3))()


def sp01_06():
    return LK.wrap(lambda: _snow_spire_wide(5))()


def vg05_01():
    return LK.wrap(lambda: R._cypress(0), prune=[dict(keys=None, max_size=10.0, thin=0.6)])()


def vg07_02():
    return LK.wrap(lambda: R._board(1), post=_board_post)()


# --- lead4 registration ---
import inspect
import v5_leadkit as LK
exec(inspect.getsource(_cave_mouth).replace('def _cave_mouth(i):', 'def _cave_mouth_big(i):').replace('ow = 9.0 + (i % 3) * 1.4', 'ow = 12.5').replace('oh = 13.0 + (i % 2) * 2.0', 'oh = 17.0'))
exec(inspect.getsource(_snow_spire).replace('def _snow_spire(i):', 'def _snow_spire_wide(i):').replace('baseR = 18.0 + (i % 3) * 1.5', 'baseR = 25.0 + (i % 3) * 1.5').replace('baseR = 22.0 ', 'baseR = 29.0 ').replace('topFrac = (0.16, 0.22, 0.12, 0.2, 0.2, 0.3)[i]', 'topFrac = (0.16, 0.22, 0.12, 0.36, 0.2, 0.44)[i]'))
BATCHES['lead4_forest'] = ('v5_forest', mk([('FR02_01_forest_ruin_01', fr02_01), ('FR02_02_forest_ruin_02', fr02_02), ('FR02_03_forest_ruin_03', fr02_03), ('FR03_01_cave_mouth_01', fr03_01),
                                            ('LM24_01_fall_pool_rock_01', lm24_01), ('VG05_01_tree_cypress_swamp_01', vg05_01), ('VG07_02_boardwalk_02', vg07_02)], 0.1))
BATCHES['lead4_hima'] = ('v5_himalaya', mk([('HL03_02_glacier_tongue_02', hl03_02), ('SP01_04_snow_spire_cluster_04', sp01_04), ('SP01_06_snow_spire_cluster_06', sp01_06)], 0.1))
BATCHES['lead4_land'] = ('v5_landmarks', mk([('LM05_01_fortress_cliff_tower_01', lm05_01), ('LM05_02_fortress_cliff_tower_02', lm05_02), ('LM08_01_mountain_span_bridge', lm08_01)], 0.1))

