def _house5_post(A):
    W, D, H = 18.0, 16.0, 11.0
    z0 = 1.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            A.box((1.1, 1.1, H), (sx * (W / 2.0 + 0.1), sy * (D / 2.0 + 0.1), z0 + H / 2.0), P['sandd'], bev=0.1)
    for z in (z0 + H * 0.45, z0 + H * 0.78):
        A.box((W + 0.5, D + 0.5, 0.5), (0, 0, z), P['sand'], bev=0.05)
    A.box((W + 0.45, D + 0.45, 1.8), (0, 0, z0 + 0.9), P['sandl'], bev=0.08)
    for wx in (-5.5, 5.5):
        for s in (-1, 1):
            A.box((0.9, 0.35, 2.6), (wx + s * 1.7, -D / 2.0 - 0.15, 7.0), P['wood'], bev=0.04)


def _canyon2(i):
    reset()
    A = Acc()
    rnd = random.Random(6700 + i * 17)
    ramps = {1: STR, 2: [P['red2'], P['clay'], P['sandd'], P['red'], P['sand'], P['cream']]}
    rp = ramps[i]
    G.cliff(A, rnd, 120.0, 40.0, 45.0, rp, 0, 0, 0, 13 + i, P['sandl'], True, 0.1 if i == 1 else -0.12, 'strata' if i == 1 else 'grade')
    for k in range(7):
        A.box((124.0, 1.2, 1.4), (0, -20.5, 4.0 + k * 5.5), rp[(k + i) % len(rp)], bev=0)
    for k in range(8):
        A.mound(rnd.uniform(-56, 56), -20.0, 12.0, 8.0, rnd.uniform(2, 5), 4, rp, rnd, 0.0, 0.5, 0.9)
    return _fin(A, 'canyon_wall')


def _crown_post(A):
    r_ = random.Random(7)
    A.chunk((12.0, 9.5, 6.5), (0, 0, 55.0), P['sand'], (0, 0, 0), 0.08, r_, (0.9, 0.9))
    for sg in (-1, 1):
        A.chunk((6.0, 9.5, 6.0), (sg * 8.0, 0, 51.5), P['clay'], (0, 0, 0), 0.08, r_, (0.9, 0.9))


def _guard_post(A):
    A.box((15.0, 6.5, 4.0), (0, 0, 46.0), P['sand'], bev=0.25)
    for sg in (-1, 1):
        A.box((3.6, 4.6, 13.0), (sg * 7.8, -0.5, 39.5), P['sand'], bev=0.25)
        A.box((3.0, 3.6, 3.4), (sg * 7.8, -2.5, 32.5), P['sandl'], bev=0.2)
    A.cyl(0.7, 46.0, (-7.8, -3.4, 8.0), P['wood'], verts=8)
    A.frustum((3.0, 3.0), (0.5, 0.5), 5.0, (-7.8, -3.4, 54.0), P['sandd'])
    A.box((9.5, 6.2, 1.2), (0, 0, 43.4), P['clay'], bev=0.1)


def _palm_fan():
    reset()
    A = Acc()
    rnd = random.Random(8812)
    h = 42.0
    segs = 9
    prev = (0.0, 0.0, 0.0)
    A.cyl(2.2, 2.0, (0, 0, 0), P['bark'], verts=10, r2=1.9)
    for s in range(1, segs + 1):
        tt = s / float(segs)
        q = (1.4 * math.sin(tt * 3.0), 0.0, h * tt)
        r = 1.9 - 0.5 * tt
        A.beam((prev[0], prev[1], max(0.0, prev[2] - 0.8)), q, r * 2.0, r * 2.0, P['bark'])
        A.sweep([(r * 0.95, -0.24), (r * 1.65, -0.24), (r * 1.65, 0.24), (r * 0.95, 0.24)], 0, 360, 8, P['bark'], loc=q)
        prev = q
    top = prev
    A.cyl(2.0, 2.6, (top[0], top[1], top[2] - 1.3), P['bark'], verts=10, r2=1.6)
    nf = 11
    for k in range(nf):
        a = 360.0 / nf * k + rnd.uniform(-8, 8)
        pts = []
        for s in range(6):
            tt = s / 5.0
            x, y, _ = polar(tt * 8.5, a)
            pts.append((top[0] + x, top[1] + y, top[2] + 7.5 * math.sin(tt * 1.5) - 3.5 * tt * tt + 0.5))
        for p0, p1 in zip(pts, pts[1:]):
            A.beam(p0, p1, 0.55, 0.4, P['bark'])
        for j, pt in enumerate(pts[1:]):
            bl = 3.0 - j * 0.4
            for sg in (-1, 1):
                A.box((bl, 0.25, 0.9), (pt[0], pt[1], pt[2]), P['palm'] if (k + j) % 2 else P['palm2'], (0, 0, a + sg * 35.0), bev=0)
    for k in range(6):
        x, y, _ = polar(1.5, k * 60.0)
        A.ball(0.8, (top[0] + x, top[1] + y, top[2] - 0.9), P['clay'], segs=6, rings=4)
    return _fin(A, 'oasis_palm')


def _obelisk_oct():
    reset()
    A = Acc()
    A.cyl(5.6, 2.2, (0, 0, 0), P['stone'], verts=8)
    A.cyl(4.6, 1.6, (0, 0, 2.2), P['sandd'], verts=8)
    A.cyl(3.4, 46.0, (0, 0, 3.8), P['sand'], verts=8, r2=2.0)
    for z, r in ((12.0, 3.15), (24.0, 2.85), (36.0, 2.55)):
        A.cyl(r + 0.45, 0.6, (0, 0, z), P['clay'], verts=8)
    for z in (18.0, 30.0, 42.0):
        A.cyl(2.6 - (z - 18.0) * 0.012, 3.0, (0, 0, z), P['sandl'], verts=8, r2=2.5 - (z - 18.0) * 0.012)
    A.cyl(2.2, 2.6, (0, 0, 49.8), P['sandl'], verts=8, r2=1.5)
    A.ball(1.7, (0, 0, 53.4), P['clay'], segs=10, rings=6)
    A.cyl(0.35, 3.0, (0, 0, 54.6), P['sandd'], verts=6, r2=0.05)
    return _fin(A, 'sand_obelisk')


def ds01_01():
    return LK.wrap(lambda: R._adobe(R.KINDS[0]), prune=[dict(keys=[R.D['cloth1']], max_size=25.0), dict(keys=None, max_size=1.9, max_z=1.5)])()


def ds01_05():
    return LK.wrap(lambda: _house(4), post=_house5_post)()


def ds04_01():
    return LK.wrap(lambda: _palm(0))()


def ds04_02():
    return LK.wrap(_palm_fan)()


def ds06_02():
    return LK.wrap(lambda: _canyon2(1), deform=dict(scale=(1.0, 1.0, 2.0)))()


def ds06_03():
    return LK.wrap(lambda: _canyon2(2), deform=dict(scale=(1.0, 1.0, 2.0), bend=(0.0, 0.0)))()


def ds07_03():
    return LK.wrap(lambda: _hoodoo_arch(2), post=_crown_post, recolor=[LK.ramp(STR, STRT, trange=(0.0, 62.0), wobble=0.02)])()


def ds08_02():
    return LK.wrap(lambda: _underground(1))()


def lm10_01():
    return LK.wrap(lambda: _colonnade(0))()


def lm12_01():
    return LK.wrap(lambda: _temple_stair(0))()


def lm12_02():
    return LK.wrap(lambda: _temple_stair(1))()


def lm13_01():
    return LK.wrap(lambda: _guardian(0), post=_guard_post, recolor=[LK.ramp([P['red']], [P['clay']])])()


def lm14_01():
    return LK.wrap(lambda: _obelisk(0), deform=dict(taper=0.12), recolor=[LK.ramp([P['sand']], [P['sandl'], P['sand'], P['clay']], trange=(3.0, 52.0), wobble=0.03)])()


def lm14_02():
    return LK.wrap(_obelisk_oct)()


def lm16_01():
    return LK.wrap(lambda: _ring_segment(0))()


def sd01_03():
    return LK.wrap(lambda: _mesa(2), prune=[dict(keys=None, max_size=9.0, max_z=4.0)])()


def sd02_05():
    return LK.wrap(lambda: _ruin_block(4), prune=[dict(keys=[P['sand'], P['sandl'], P['sandd']], max_size=24.0, thin=2.2, max_z=2.5)])()


VOLC = [P['basalt'], P['basalt2'], P['ash']]


def vc01_03():
    return LK.wrap(lambda: _volcanic(2), deform=dict(twist=18.0, bend=(0.1, -0.05), scale=(0.95, 1.0, 1.1)), prune=[dict(keys=None, max_size=3.8, max_z=1.5)])()


def vc01_04():
    return LK.wrap(lambda: _volcanic(3), recolor=[LK.ramp(VOLC, [P['basalt2'], P['basalt'], P['basalt2'], P['ash']], wobble=0.1), LK.ramp(VOLC, [P['rust']], zlim=(-1.0, 3.5))])()


def vc01_06():
    return LK.wrap(lambda: _volcanic(5), deform=dict(lean=(0.12, 0.0), scale=(1.2, 0.9, 0.85), mirror_x=True),
                   recolor=[LK.ramp(VOLC, [P['ash'], P['basalt2'], P['ash'], P['basalt']], wobble=0.1), LK.ramp(VOLC, [P['rust']], zlim=(-1.0, 3.0))])()


# --- lead4 registration ---
import v5_leadkit as LK
BATCHES['lead4_desert'] = ('v5_desert', mk([('DS01_01_adobe_house_01', ds01_01), ('DS01_05_adobe_house_05', ds01_05), ('DS04_01_palm_01', ds04_01), ('DS04_02_palm_02', ds04_02),
                                            ('DS06_02_canyon_wall_02', ds06_02), ('DS06_03_canyon_wall_03', ds06_03), ('DS07_03_hoodoo_arch_03', ds07_03),
                                            ('DS08_02_underground_entrance_02', ds08_02), ('SD01_03_red_mesa_cluster_03', sd01_03), ('SD02_05_desert_ruin_block_05', sd02_05)], 0.1))
BATCHES['lead4_land'] = ('v5_landmarks', mk([('LM10_01_temple_colonnade_buried_01', lm10_01), ('LM12_01_temple_stair_down_01', lm12_01), ('LM12_02_temple_stair_down_02', lm12_02),
                                             ('LM13_01_guardian_statue_01', lm13_01), ('LM14_01_sand_obelisk_01', lm14_01), ('LM14_02_sand_obelisk_02', lm14_02),
                                             ('LM16_01_ring_temple_segment_01', lm16_01)], 0.1))
BATCHES['lead4_skull'] = ('v5_skull', mk([('VC01_03_volcanic_rock_03', vc01_03), ('VC01_04_volcanic_rock_04', vc01_04), ('VC01_06_volcanic_rock_06', vc01_06)], 0.1))
