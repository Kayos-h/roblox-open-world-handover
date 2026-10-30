PV = G.reg('ve_f', {
    'iron_m': ((92, 88, 86), 'Metal', 0.3, 0.72),
    'bronze': ((128, 96, 62), 'Metal', 0.3, 0.72),
    'coal2': ((76, 52, 42), 'Slate', 0.0, 0.95),
    'ash': ((128, 120, 110), 'Slate', 0.0, 0.95),
    'sack': ((190, 168, 124), 'Fabric', 0.0, 1.0),
})


def _path01():
    """EV03_01 (round 3, lead) - root-and-stone stair piece, 20 W x 6 H x 20 D: nine SOLID steps on the ground (closed underside), light wooden step edges proud of the treads,
    a solid back mass, root rails that touch the step sides, moss on the lower steps."""
    reset()
    A = Acc()
    rnd = random.Random(7001)
    n = 9
    for i in range(n):
        w = 17.5 - i * 0.55
        y = -9.0 + i * 2.1
        h = 0.62 * (i + 1)
        A.box((w, 2.3, h), (0, y, h / 2.0), E['stone'] if i % 2 else P['barkmid'], bev=0.08)
        A.box((w + 0.3, 2.6, 0.35), (0, y - 0.15, h - 0.175 + 0.07), E['plank'], bev=0.05)
    A.box((13.0, 3.0, 0.62 * n), (0, -9.0 + n * 2.1 + 0.5, 0.62 * n / 2.0), P['barkdk'], bev=0.1)
    for sg in (-1, 1):
        A.beam((sg * 9.0, -9.5, 0.9), (sg * 5.9, 9.5, 6.0), 1.4, 1.1, P['barkdk'])
        A.cyl(0.9, 1.6, (sg * 9.0, -9.5, 0.0), P['barkdk'], verts=8)
    for k in range(6):
        i = k
        A.ball(rnd.uniform(0.9, 1.5), (rnd.uniform(-6.5, 6.5), -9.0 + i * 2.1, 0.62 * (i + 1) + 0.05), P['moss'], segs=6, rings=4, scale=(1.5, 1.2, 0.4))
    return _fin(A, 'elf_path_piece')


def tree_falls():
    """LM02_01 (round 3, lead) - a tree-trunk cliff with pale falls. 80 x 40 x 110. Same design as the round-2 version, but every bark rib now sits ON the tapering trunk
    (the old straight ribs hovered up to 5 studs off the narrow upper trunk and read as detached planks); no hanging roots, no scattered rubble."""
    reset()
    A = Acc()
    rnd = random.Random(1631)
    A.cyl(30.0, 110.0, (6.0, 10.0, 0.0), P['barkdk'], verts=20, r2=22.0)
    for k in range(34):
        zc = rnd.uniform(16.0, 92.0)
        L = rnd.uniform(22.0, 38.0)
        a = rnd.uniform(0, 360)
        r = 30.0 - 8.0 * (zc / 110.0) - 1.3
        x, y, _ = polar(r, a)
        A.chunk((3.2, 3.2, L), (6.0 + x, 10.0 + y, zc), P['barkmid'] if k % 2 else P['barkdk'], (0, 0, a), 0.1, rnd, (0.55, 0.8))
    for k in range(9):
        a = 360.0 / 9 * k + rnd.uniform(-6, 6)
        x, y, _ = polar(26.0, a)
        A.beam((6.0 + x * 1.7, 10.0 + y * 1.7, 0.4), (6.0 + x * 0.5, 10.0 + y * 0.5, 16.0), 6.0, 6.0, P['barkdk'])
    for cx, hc in ((-18.0, 96.0), (18.0, 84.0)):
        z = 0.0
        while z < hc:
            sh = min(rnd.uniform(6, 11), hc - z)
            t = z / 110.0
            A.chunk((rnd.uniform(14, 20), rnd.uniform(14, 20), sh * 1.1), (cx + rnd.uniform(-3, 3), -8.0 + rnd.uniform(-2, 2), z + sh / 2), band(CLIFF, t, rnd), (0, rnd.uniform(-5, 5), rnd.uniform(-7, 7)), 0.12, rnd, (0.9, 0.9))
            z += sh * 0.85
    for k in range(70):
        cx = rnd.uniform(-30, 30)
        z = rnd.uniform(6, 96)
        A.chunk((rnd.uniform(3, 7), rnd.uniform(2, 4), rnd.uniform(3, 7)), (cx, -14.0 + rnd.uniform(-1, 3), z), band(CLIFF, z / 110.0, rnd), (0, rnd.uniform(-7, 7), rnd.uniform(-9, 9)), 0.14, rnd, (0.9, 0.9))
    for k in range(10):
        A.chunk((rnd.uniform(6, 10), rnd.uniform(3, 5), rnd.uniform(1.2, 2.2)), (rnd.uniform(-24, 24), -14.0, rnd.uniform(12, 80)), P['moss'], (0, 0, rnd.uniform(-6, 6)), 0.14, rnd)
    _sheet_falls(A, rnd, -16.0, -16.0, 94.0, 10.0, 18.0, pool_y=-28.0, pool_w=26.0, breaks=2)
    _sheet_falls(A, rnd, 16.0, -14.0, 72.0, 8.0, 12.0, pool_y=-26.0, pool_w=20.0, breaks=1)
    for k in range(18):
        a = rnd.uniform(0, 360)
        r = rnd.uniform(0, 24)
        x, y, _ = polar(r, a)
        A.ball(rnd.uniform(7, 13), (6.0 + x, 10.0 + y, 103.0 + rnd.uniform(-4, 6)), E['leaf1'] if k % 2 else E['leaf2'], segs=9, rings=6, scale=(1.3, 1.2, 0.85))
    A.cyl(24.0, 4.0, (6.0, 10.0, 108.0), E['moss'], verts=20, r2=20.0)
    return v5kit.fit(_fin(A, 'world_tree_falls'), w=80.0, d=40.0, h=110.0)


def _stall():
    """TW02_03 (round 3, lead) - market stall, 12 W x 10 H x 10 D: four posts, a striped cloth awning, a counter with stacked crates, a barrel and two sacks beside it.
    Reads as street life from every side; everything is grounded."""
    reset()
    A = Acc()
    rnd = random.Random(7203)
    for sx in (-5.0, 5.0):
        for sy in (-3.5, 3.5):
            A.box((0.7, 0.7, 8.0), (sx, sy, 4.0), T1['wood'], bev=0.06)
    for k in range(6):
        x = -5.0 + k * 2.0 + 1.0
        A.box((1.96, 8.6, 0.5), (x, 0.0, 8.0 + (k % 1) * 0.0), T1['cloth'] if k % 2 else T1['cream'], (8, 0, 0), bev=0.02)
    A.box((11.0, 0.5, 1.6), (0, -4.1, 8.0 - 0.6), T1['cloth'], bev=0.04)
    A.box((9.0, 3.0, 3.0), (0, 0.2, 1.5), T1['plank'], bev=0.08)
    A.box((9.4, 3.4, 0.4), (0, 0.2, 3.2), T1['wood'], bev=0.05)
    for (x, z, s) in ((-2.6, 3.4, 1.8), (-0.4, 3.4, 1.8), (-1.5, 5.2, 1.6)):
        A.box((s, s, s), (x, 0.2, z + s / 2.0), T1['plank'], (0, 0, rnd.uniform(-8, 8)), bev=0.08)
        A.box((s + 0.08, 0.2, s + 0.08), (x, 0.2 - s / 2.0 - 0.02, z + s / 2.0), T1['wood'], bev=0)
    A.ball(0.9, (2.4, 0.2, 4.0), T1['green'], segs=8, rings=5)
    A.ball(0.8, (3.4, 0.0, 3.9), T1['cloth'], segs=8, rings=5)
    A.cyl(1.2, 2.8, (4.2, -3.4, 0.0), T1['plank'], verts=12, r2=1.2)
    A.cyl(1.3, 0.3, (4.2, -3.4, 1.0), T1['iron'], verts=12)
    for sx, sy in ((-4.2, -3.2), (-3.0, -3.6)):
        A.ball(1.3, (sx, sy, 1.0), PV['sack'], segs=8, rings=5, scale=(1.0, 0.9, 0.85))
    A.box((3.0, 0.3, 1.2), (0, -4.3, 6.4), T1['plank'], bev=0.04)
    A.box((2.6, 0.1, 0.8), (0, -4.5, 6.4), T1['cream'], bev=0)
    return _fin(A, 'town1_street_life')


def _sign_smith():
    """TW02_07 (round 3, lead) - smith's hanging sign, 12 W x 10 H x 10 D: stone footing, wooden post, bracket arm with a brace, a warm plank board on two chains with a
    cream plaque and a dark iron anvil emblem. Light and warm, only the small emblem is dark."""
    reset()
    A = Acc()
    A.box((4.0, 4.0, 1.2), (0, 0, 0.6), T1['stone'], bev=0.1)
    A.box((2.6, 2.6, 0.5), (0, 0, 1.4), T1['dstone'], bev=0.06)
    A.box((0.9, 0.9, 9.0), (0, 0, 1.2 + 4.5), T1['wood'], bev=0.08)
    A.beam((0.0, 0, 9.2), (6.0, 0, 9.2), 0.6, 0.6, T1['wood'])
    A.beam((0.2, 0, 6.2), (3.0, 0, 9.0), 0.4, 0.4, T1['wood'])
    for sx in (4.4, 5.8):
        A.box((0.12, 0.12, 1.4), (sx, 0, 8.4), T1['iron'], bev=0)
    A.box((3.4, 0.5, 3.2), (5.1, 0, 6.4), T1['plank'], bev=0.06)
    A.box((2.9, 0.12, 2.7), (5.1, -0.3, 6.4), T1['cream'], bev=0)
    A.box((2.0, 0.3, 0.7), (5.1, -0.46, 6.9), PV['iron_m'], bev=0.04)
    A.box((0.8, 0.3, 0.9), (5.1, -0.46, 6.3), PV['iron_m'], bev=0.04)
    A.box((1.7, 0.3, 0.5), (5.1, -0.46, 5.7), PV['iron_m'], bev=0.04)
    return _fin(A, 'town1_street_life')


def _brazier2():
    """TW03_02 (round 3, lead) - skull-avenue pedestal brazier, 14 x 14 x 14: stone pedestal, a dull iron bowl (not near-black), a dull bronze rim (no gold), and the bowl
    FILLED with a heap of dark coals and ash that rises above the rim, so it never reads as an empty hole. No glow."""
    reset()
    A = Acc()
    rnd = random.Random(7302)
    A.cyl(3.2, 0.8, (0, 0, 0), T1['dstone'], verts=12)
    A.cyl(1.4, 5.0, (0, 0, 0.8), T1['stone'], verts=8, r2=1.0)
    A.cyl(1.9, 0.6, (0, 0, 5.8), T1['dstone'], verts=8)
    A.cyl(3.6, 2.2, (0, 0, 6.4), PV['iron_m'], verts=16, r2=4.2)
    A.sweep([(3.9, 0.0), (4.7, 0.0), (4.7, 0.55), (3.9, 0.55)], 0, 360, 16, PV['bronze'], loc=(0, 0, 8.3))
    A.cyl(4.0, 0.9, (0, 0, 8.2), PV['ash'], verts=16)
    for k in range(16):
        r = rnd.uniform(0.0, 3.2)
        x, y, _ = polar(r, rnd.uniform(0, 360))
        A.chunk((rnd.uniform(1.2, 1.9), rnd.uniform(1.2, 1.9), rnd.uniform(1.0, 1.6)), (x, y, 9.2 + (1.0 - r / 3.4) * 0.9), PV['coal2'] if k % 3 else PV['ash'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(4):
        x, y, _ = polar(4.3, k * 90.0 + 45)
        A.ball(0.5, (x, y, 8.3), PV['bronze'], segs=6, rings=4)
    return _fin(A, 'skull_avenue_set')


def _avenue04():
    """TW03_04 (round 3, lead) - banner standard with a swallowtail banner: the banner is ONE flat cloth shape (a prism), with a plain bone diamond on it. No letters, no
    stray angled slabs; thicker pole and braces. 14 x 14 x 14 footprint."""
    reset()
    A = Acc()
    A.cyl(2.8, 1.2, (0, 0, 0), T1['dstone'], verts=10)
    A.cyl(0.8, 20.0, (0, 0, 1.0), T1['wood'], verts=8, r2=0.6)
    A.ball(1.0, (0, 0, 21.2), T1['bone'], segs=10, rings=7, scale=(1.0, 0.85, 1.0))
    for sx in (-0.35, 0.35):
        A.ball(0.28, (sx, -0.7, 21.3), T1['dark'], segs=6, rings=4, scale=(1.0, 0.6, 0.9))
    A.beam((0, 0, 18.6), (5.6, 0, 18.6), 0.45, 0.45, T1['iron'])
    A.prism([(-2.1, 8.6), (2.1, 8.6), (2.1, 0.0), (0.0, 2.8), (-2.1, 0.0)], 0.45, (5.0, 0, 9.8), T1['green'], (90, 0, 90))
    A.prism([(0.0, 1.1), (0.9, 0.0), (0.0, -1.1), (-0.9, 0.0)], 0.12, (5.4, 0, 14.6), T1['bone'], (90, 0, 90))
    A.box((0.6, 4.6, 0.6), (5.0, 0, 18.5), T1['dstone'], bev=0.05)
    for sg in (-1, 1):
        A.beam((0, 0, 3.0), (sg * 3.2, 0, 1.0), 0.5, 0.5, T1['iron'])
    return _fin(A, 'skull_avenue_set')


# --- lead3 registration ---
BATCHES['lead3'] = ('v5_elf', mk([('EV03_01_elf_path_piece_01', _path01), ('LM02_01_world_tree_falls', tree_falls)], 0.1))
BATCHES['lead3_town'] = ('v5_town1', mk([('TW02_03_street_life_03', _stall), ('TW02_07_street_life_07', _sign_smith), ('TW03_02_skull_avenue_set_02', _brazier2), ('TW03_04_skull_avenue_set_04', _avenue04)], 0.1))
