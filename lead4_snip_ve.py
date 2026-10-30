def _canopy_post(seed, n):
    def post(A):
        rnd = random.Random(seed)
        spots = []
        for k in range(n):
            a = 360.0 * k / n + rnd.uniform(-20, 20)
            dist = rnd.uniform(22.0, 29.0)
            z = 10.0 + k * (22.0 / max(1, n - 1)) + rnd.uniform(-1, 1)
            r = rnd.uniform(6.5, 8.5)
            spots.append((a, dist, z, r))
        for (a0, d0, z0, r0), (a1, d1, z1, r1) in zip(spots, spots[1:]):
            x0, y0, _ = polar(d0, a0)
            x1, y1, _ = polar(d1, a1)
            L = math.hypot(x1 - x0, y1 - y0)
            ux, uy = (x1 - x0) / L, (y1 - y0) / L
            ang = math.degrees(math.atan2(uy, ux))
            Lw = L - r0 - r1
            steps = max(3, int(Lw / 1.3))
            for s in range(steps + 1):
                t = s / float(steps)
                px = x0 + ux * (r0 + Lw * t)
                py = y0 + uy * (r0 + Lw * t)
                pz = z0 + 0.8 + (z1 - z0) * t - 1.2 * 4 * t * (1 - t)
                A.box((1.5, 3.0, 0.5), (px, py, pz - 0.4), E['wood'], (0, 0, ang), bev=0.05)
                if s % 2 == 0:
                    for sg in (-1, 1):
                        A.box((0.3, 0.3, 2.0), (px - uy * sg * 1.35, py + ux * sg * 1.35, pz + 0.6), E['wood'], bev=0)
            for sg in (-1, 1):
                prev = None
                for s in range(steps + 1):
                    t = s / float(steps)
                    q = (x0 + ux * (r0 + Lw * t) - uy * sg * 1.35, y0 + uy * (r0 + Lw * t) + ux * sg * 1.35, z0 + 0.8 + (z1 - z0) * t - 1.2 * 4 * t * (1 - t) + 1.6)
                    if prev:
                        A.beam(prev, q, 0.32, 0.3, E['wood'])
                    prev = q
    return post


def _carved_post(A):
    for x in (-4.0, 0.0, 4.0):
        A.box((1.0, 0.7, 4.0), (x, 8.45, 2.2), E['bark'], bev=0.04)
    A.box((12.4, 0.5, 0.8), (0, 8.35, 0.4), E['wood'], bev=0.04)
    A.box((12.8, 1.0, 0.4), (0, 8.2, 4.55), E['wood'], bev=0.04)


def _roots_post(A):
    r_ = random.Random(612)
    A.cyl(56.0, 26.0, (0, 0, 3.0), E['bark'], verts=32, r2=38.0)
    A.ball(38.0, (0, 0, 28.0), E['bark'], segs=24, rings=10, scale=(1.0, 1.0, 0.22))
    for k in range(14):
        a = 360.0 / 14 * k
        x, y, _ = polar(47.0, a)
        A.chunk((7.0, 7.0, r_.uniform(16.0, 22.0)), (x, y, r_.uniform(12.0, 16.0)), P['barkdk'] if k % 2 else P['barkmid'], (0, 0, a), 0.1, r_, (0.55, 0.7))
    for k in range(8):
        x, y, _ = polar(r_.uniform(8.0, 34.0), r_.uniform(0, 360))
        A.ball(r_.uniform(3.0, 5.0), (x, y, 29.0), E['moss'], segs=7, rings=4, scale=(1.4, 1.3, 0.5))


def _statue_post(A):
    z0 = 8.55
    A.box((6.6, 4.4, 0.5), (0, 0, z0 + 10.5), T1['brass'], bev=0.05)
    A.cyl(0.9, 0.3, (0, -2.45, z0 + 14.4), T1['brass'], verts=12, rot=(90, 0, 0))
    for sg in (-1, 1):
        A.box((2.4, 3.4, 0.8), (sg * 3.7, 0, z0 + 16.4), T1['dstone'], bev=0.08)
    A.box((7.6, 4.8, 0.5), (0, 0, z0 + 7.2), T1['dstone'], bev=0.05)


def _cart_post(A):
    for (x, y, z) in ((-2.4, 0.5, 3.9), (-0.6, -0.7, 3.9), (1.4, 0.4, 3.9)):
        A.ball(1.25, (x, y, z), PV['sack'], segs=8, rings=5, scale=(1.0, 0.95, 0.85))
    A.cyl(1.0, 2.2, (2.6, -0.6, 2.9), T1['plank'], verts=10, r2=1.0)
    A.box((1.8, 1.8, 1.6), (-0.4, 0.1, 3.7), T1['plank'], (0, 0, 14), bev=0.06)


def _crates2_post(A):
    for k in range(3):
        A.ball(1.0, (4.2 + k * 0.6, 2.0 - k * 1.0, 1.0), T1['cream'], segs=10, rings=6, scale=(1.0, 1.0, 1.1))


def _banner_post(A):
    for j in range(4):
        A.box((0.3, 1.0, 9.0), (5.4 + (0.25 if j % 2 else -0.25), -1.5 + j * 1.0, 14.0), T1['cloth'], bev=0.02)
    for sy in (-1.6, 0.0, 1.6):
        A.box((0.3, 0.3, 0.7), (5.4, sy, 18.8), T1['rope'], bev=0)


def ev02_01():
    return LK.wrap(lambda: ORIG._canopy(601, 3), post=_canopy_post(601, 3))()


def ev02_02():
    return LK.wrap(lambda: ORIG._canopy(602, 4), post=_canopy_post(602, 4), recolor=[LK.ramp([E['shingle']], [E['red']])])()


def ev03_02():
    return LK.wrap(lambda: ORIG._path('carved'), post=_carved_post)()


def ev03_05():
    return LK.wrap(_path05, recolor=[LK.ramp([P['niche']], [E['bark']]), LK.ramp([P['deckwood']], [P['barkdk'], P['barkmid']], trange=(0.0, 1.5))])()


def rw02_01():
    return LK.wrap(ORIG.tree_roots, post=_roots_post)()


def tw01_01():
    return LK.wrap(statue, post=_statue_post)()


def tw02_01():
    return LK.wrap(lambda: ORIG._street('handcart'), prune=[dict(keys=[T1['cream'], T1['green']], max_size=2.6)], post=_cart_post)()


def tw02_04():
    return LK.wrap(lambda: ORIG._street('crates2'), prune=[dict(keys=[T1['cream']], max_size=2.6)], post=_crates2_post)()


def tw03_01():
    return LK.wrap(_avenue01, recolor=[LK.ramp([T1['iron']], [PV['iron_m']]), LK.ramp([T1['coal']], [PV['coal2']]), LK.ramp([T1['dark']], [PV['iron_m']])])()


def tw03_03():
    return LK.wrap(lambda: ORIG._avenue('banner1'), prune=[dict(keys=[T1['cloth']], max_size=10.0, thin=0.3)], post=_banner_post)()


# --- lead4 registration ---
import v5_leadkit as LK
BATCHES['lead4_elf'] = ('v5_elf', mk([('EV02_01_canopy_cluster_01', ev02_01), ('EV02_02_canopy_cluster_02', ev02_02), ('EV03_02_elf_path_piece_02', ev03_02),
                                      ('EV03_05_elf_path_piece_05', ev03_05), ('RW02_01_rework_world_tree_roots', rw02_01)], 0.1))
BATCHES['lead4_town'] = ('v5_town1', mk([('TW01_01_town1_hero_statue', tw01_01), ('TW02_01_street_life_01', tw02_01), ('TW02_04_street_life_04', tw02_04),
                                         ('TW03_01_skull_avenue_set_01', tw03_01), ('TW03_03_skull_avenue_set_03', tw03_03)], 0.1))

