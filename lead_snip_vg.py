def _switch_stairs(i):
    """LM07_01/02 (round 3, lead) - a SOLID banded rock tower with a switchback stair bolted to its front face. 50 W x 60 D x 60 H.
    The mass is a closed stack of four blocks (nothing hollow, no black void). Each stair flight is a stepped wedge fixed INTO the face, so every part overlaps the mass.
    Siblings: i=1 is mirrored and has a different back outline."""
    reset()
    A = Acc()
    rnd = random.Random(7100 + i)
    flip = -1.0 if i else 1.0
    W, H = 50.0, 60.0
    Y0, Y1 = -30.0, 30.0
    SD = 6.0
    face = Y0 + SD - 0.8
    bands = [P['cliff1'], P['cliff2'], P['cliff3'], P['cliff4']]
    seg = H / 4.0
    for b in range(4):
        wb = W - 2.5 * b + rnd.uniform(-1.0, 1.0)
        y_front = face + 0.2 * b
        y_back = Y1 - (2.0 + 2.5 * i) * b + rnd.uniform(-1.0, 1.0)
        A.box((wb, y_back - y_front, seg + 0.5), (flip * rnd.uniform(-0.8, 0.8), (y_front + y_back) / 2.0, b * seg + seg / 2.0), bands[b], bev=0.5)
    for k in range(18):                                                            # faceted bosses on the sides and the back (rock is not a box)
        z = rnd.uniform(4.0, H - 6.0)
        key = band(bands, z / H, rnd)
        w_at = W - 2.5 * int(z / seg)
        sx, sy, sz = rnd.uniform(6.0, 10.0), rnd.uniform(8.0, 13.0), rnd.uniform(5.0, 9.0)
        if k % 3 == 2:
            A.chunk((sy, sx, sz), (rnd.uniform(-w_at / 2.0 + 7.0, w_at / 2.0 - 7.0), Y1 - 3.5 - 2.5 * i * int(z / seg), z), key, (0, 0, rnd.uniform(-20, 20)), 0.14, rnd, (0.9, 0.9))
        else:
            sg = -1.0 if k % 2 else 1.0
            A.chunk((sx, sy, sz), (sg * (w_at / 2.0 - 2.0), rnd.uniform(face + 8.0, Y1 - 10.0), z), key, (0, 0, rnd.uniform(-20, 20)), 0.14, rnd, (0.9, 0.9))
    flights, per = 5, 6
    rise = H / (flights * per)
    run = 3.4
    half = per * run / 2.0
    for fl in range(flights):
        d = 1.0 if fl % 2 == 0 else -1.0
        z0 = fl * per * rise
        x0 = -half if d > 0 else half
        for s in range(per):
            sx = flip * (x0 + d * (s * run + run / 2.0))
            hh = rise * (s + 1)
            A.box((run + 0.1, SD, hh), (sx, Y0 + SD / 2.0, z0 + hh / 2.0), P['stair_mid'], bev=0.1)
            A.box((run + 0.3, SD + 0.6, 0.8), (sx, Y0 + SD / 2.0 - 0.2, z0 + hh - 0.35 + 0.07), P['stair_hi'], bev=0.1)
        lx = flip * (x0 + d * (per * run + 3.5))
        A.box((7.0, SD, per * rise), (lx, Y0 + SD / 2.0, z0 + per * rise / 2.0), P['stair_mid'], bev=0.1)
        A.box((7.3, SD + 0.6, 0.8), (lx, Y0 + SD / 2.0 - 0.2, z0 + per * rise - 0.35 + 0.07), P['stair_hi'], bev=0.1)
    A.box((W - 9.5, Y1 - 8.0 - face, 0.8), (0, (face + Y1 - 8.0) / 2.0, H + 0.2), P['cliff4'], bev=0.1)      # summit cap, flush with the last landing
    for k in range(7):                                                                                        # lichen on the summit and ledges, embedded in the cap
        A.ball(rnd.uniform(1.2, 2.2), (rnd.uniform(-14, 14), rnd.uniform(face + 6.0, Y1 - 12.0), H + 0.5), P['lichen'], segs=6, rings=4, scale=(1.6, 1.4, 0.4))
    return _fin(A, 'carved_stair')


def _gate_tunnel():
    """LM06_01 (round 3, lead) - fortress tunnel gate, 60 W x 60 D x 50 H: two grounded rock piers built as four thick stepped tiers with faceted bosses (no thin slabs),
    a three-tier lintel mass over a PASSABLE tunnel (mid-dark ceiling, paved floor), timber frame with braces, a stone sign block, warm banded colours, moss caps."""
    reset()
    A = Acc()
    rnd = random.Random(7600)
    W, D, H = 60.0, 60.0, 50.0
    ow, oh = 11.0, 22.0
    pw = W / 2.0 - ow
    fy = -25.5
    cols = [P['cliff1'], P['cliff2'], P['cliff3'], P['cliff4']]
    tiers = [(0.0, 14.0, 2.0, 51.0), (13.0, 13.0, 0.0, 49.0), (25.0, 12.5, -2.5, 46.0), (36.0, 12.0, -5.5, 42.0)]
    for sg in (-1, 1):
        for t, (zb, th, dw, dep) in enumerate(tiers):
            w = pw + dw
            A.box((w, dep, th + 0.6), (sg * (ow + w / 2.0), fy + 0.15 * t + dep / 2.0, zb + th / 2.0), cols[t], bev=0.6)
        A.box((pw - 7.0, 36.0, 2.0), (sg * (ow + (pw - 7.0) / 2.0 + 1.0), fy + 20.0, H - 0.2), P['moss'], bev=0.4)
    for t, (zb, ht, wx, dep) in enumerate(((oh, 9.0, 2.0, 49.0), (oh + 8.0, 9.5, 3.0, 47.0), (oh + 16.0, 12.0, 4.0, 42.0))):
        A.box((2 * ow + 2 * wx, dep, ht + 0.6), (0, fy + 0.2 * t + 0.07 + dep / 2.0, zb + ht / 2.0), cols[t + 1], bev=0.6)
    A.box((2 * ow + 10.0, 36.0, 2.0), (0, fy + 20.0, H - 0.2), P['moss'], bev=0.4)
    A.box((2 * ow + 0.4, D - 12.0, 0.8), (0, 0, oh - 0.1), P['recess'], bev=0)
    A.box((2 * ow + 0.4, D - 10.0, 0.5), (0, 0, 0.25), P['tread'], bev=0)
    for k in range(18):
        z = rnd.uniform(5.0, H - 9.0)
        key = band(cols, z / H, rnd)
        sx, sy, sz = rnd.uniform(5.0, 9.0), rnd.uniform(4.0, 7.0), rnd.uniform(4.0, 8.0)
        face = k % 4
        if face == 0:
            x, y = rnd.choice((-1, 1)) * rnd.uniform(ow + 6.0, W / 2.0 - 5.0), fy + 0.6
        elif face == 1:
            x, y = rnd.uniform(-W / 2.0 + 6.0, W / 2.0 - 6.0), fy + 49.0 - 1.2
        else:
            x, y = rnd.choice((-1, 1)) * (W / 2.0 - 1.2), rnd.uniform(fy + 8.0, fy + 40.0)
        if abs(x) < ow + 5.0 and z < oh + 4.0:
            z += oh + 4.0
        A.chunk((sx, sy, sz), (x, y, z), key, (0, 0, rnd.uniform(-25, 25)), 0.15, rnd, (0.9, 0.9))
    for sg in (-1, 1):
        A.box((2.4, 2.4, oh + 1.0), (sg * (ow + 0.5), fy + 0.2, (oh + 1.0) / 2.0), R.P['timber'], bev=0.1)
        A.beam((sg * (ow + 0.5), fy - 0.9, oh - 3.5), (sg * (ow - 3.5), fy - 0.9, oh + 0.4), 0.9, 0.9, R.P['timber'])
        A.box((3.4, 3.4, 1.0), (sg * (ow + 0.5), fy + 0.2, 0.5), P['cliff3'], bev=0.1)
    A.box((2 * ow + 4.0, 2.4, 2.4), (0, fy + 0.2, oh + 1.4), R.P['timber'], bev=0.1)
    A.box((13.0, 3.0, 4.0), (0, fy + 0.6, oh + 5.2), P['wall'], bev=0.12)
    A.box((9.0, 0.6, 1.4), (0, fy - 1.1, oh + 5.2), P['cliff1'], bev=0)
    A.box((2 * ow + 8.0, 6.0, 0.6), (0, fy - 3.0, 0.3), P['tread'], bev=0.1)
    return _fin(A, 'gate_tunnel')


def _altar_ruin():
    """FR02_04 (round 3, lead) - overgrown forest shrine ruin, 40 W x 30 D x 34 H: two-step plinth, altar with a stone urn (no gold), four columns of different heights
    (the two front ones carry a lintel), a fallen drum, moss. Warm banded stone only; nothing bright."""
    reset()
    A = Acc()
    rnd = random.Random(7403)
    KW = dict(FK, stone=P['cliff2'], wall=P['cliff3'], trim=P['cliff4'])
    A.chunk((40.0, 30.0, 3.0), (0, 0, 1.5), P['cliff2'], (0, 0, 0), 0.04, rnd)
    A.chunk((32.0, 22.0, 3.0), (0, 0, 4.5), P['cliff3'], (0, 0, 0), 0.04, rnd)
    A.chunk((12.0, 7.0, 5.0), (0, 0, 8.5), P['cliff4'], (0, 0, 0), 0.04, rnd)
    A.chunk((9.0, 5.0, 1.4), (0, 0, 11.7), P['cliff3'], (0, 0, 0), 0.04, rnd)
    A.cyl(1.2, 2.4, (0, 0, 12.4), P['cliff2'], verts=10, r2=0.9)
    A.ball(1.0, (0, 0, 15.0), P['cliff3'], segs=8, rings=5)
    for (x, y, h, br) in ((-13.0, -8.0, 26.0, 0.0), (13.0, -8.0, 26.0, 0.0), (-13.0, 8.0, 18.0, 0.55), (13.0, 8.0, 11.0, 0.7)):
        G.column(A, x, y, 6.0, 1.9, h, KW, br, rnd)
    A.box((30.0, 3.4, 2.6), (0, -8.0, 6.0 + 26.0 + 0.7), P['cliff3'], bev=0.15)
    A.cyl(1.8, 5.5, (-4.0, 9.0, 6.0 + 1.7), P['cliff3'], verts=10, rot=(0, 90, 25))
    for k in range(8):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(11.0, 16.0), a)
        A.chunk((rnd.uniform(2.4, 4.0), rnd.uniform(2.4, 3.6), rnd.uniform(1.6, 2.4)), (x * 1.2, y * 0.9, 3.4), band(CROCK, rnd.random(), rnd), (0, 0, rnd.uniform(0, 90)), 0.18, rnd)
    for k in range(12):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(8.0, 17.0), a)
        A.ball(rnd.uniform(1.0, 1.9), (x * 1.15, y * 0.85, rnd.uniform(2.8, 3.6)), P['moss'] if k % 2 else P['moss2'], segs=6, rings=4, scale=(1.4, 1.2, 0.5))
    return _fin(A, 'forest_ruin')


def _pool_rock(i):
    """LM24_02/03 (round 3, lead) - rocks standing in the fall pool, 30 W x 30 D x 16 H. Warm banded stone, moss, a muted matte pool skirt.
    i=1 a broad low boulder cluster with a flat table stone; i=2 two leaning stone spires over a boulder ring (different shape, not only placement)."""
    reset()
    A = Acc()
    rnd = random.Random(7500 + i)
    A.box((29.0, 27.0, 0.5), (0, 0, 0.25), P['chuted'], bev=0)
    if i == 1:
        A.mound(0, 0, 26.0, 24.0, 10.0, 26, CROCK, rnd, 0.0, 0.32, 0.6)
        A.chunk((13.0, 10.0, 5.0), (-3.0, 1.0, 9.5), P['cliff3'], (0, 0, 14), 0.08, rnd)
        A.chunk((7.0, 6.0, 5.0), (8.0, -4.0, 8.0), P['cliff2'], (0, 0, -20), 0.12, rnd, (0.8, 0.8))
        A.chunk((8.0, 7.0, 6.0), (-9.0, -5.0, 6.0), P['cliff1'], (0, 0, 40), 0.12, rnd, (0.8, 0.8))
    else:
        A.mound(0, 0, 25.0, 23.0, 6.0, 18, CROCK, rnd, 0.0, 0.3, 0.55)
        G.spire(A, rnd, 6.0, 16.0, CROCK, -5.0, 3.0, 0.0, 6, 0.12, None)
        G.spire(A, rnd, 4.2, 11.0, CROCK, 7.0, -2.0, 0.0, 5, -0.15, None)
    for k in range(6):
        A.ball(rnd.uniform(1.0, 1.8), (rnd.uniform(-7, 7), rnd.uniform(-6, 6), rnd.uniform(3.0, 7.0)), P['moss'] if k % 2 else P['moss2'], segs=6, rings=4, scale=(1.5, 1.3, 0.5))
    return _fin(A, 'pool_rocks')


BATCHES = {
    'a4_forest': ('v5_forest', mk(
        [(ids('FR01')[1], (lambda: _giant_tree(1))), (ids('FR01')[2], (lambda: _giant_tree(2)))] +
        [(ids('FR02')[3], _altar_ruin), (ids('FR02')[4], (lambda: _forest_ruin(4))), (ids('FR02')[5], (lambda: _forest_ruin(5)))] +
        [(ids('FR03')[1], (lambda: _cave_mouth(1))), (ids('FR03')[2], (lambda: _cave_mouth(2))),
         (ids('FR03')[3], (lambda: _cave_mouth(3))), (ids('FR03')[4], (lambda: _cave_mouth(4))), (ids('FR03')[5], (lambda: _cave_mouth(5)))] +
        [(ids('VG04')[0], (lambda: _birch(0))), (ids('VG04')[1], (lambda: _birch(1))), (ids('VG04')[2], (lambda: _birch(2)))] +
        [(ids('LM23')[0], (lambda: _gorge(0))), (ids('LM23')[2], (lambda: _gorge(2)))] +
        [(ids('LM24')[1], (lambda: _pool_rock(1))), (ids('LM24')[2], (lambda: _pool_rock(2)))] +
        [(ids('VG05')[1], (lambda: _cypress(1))), (ids('VG05')[2], (lambda: _cypress(2)))] +
        [(ids('VG06')[0], (lambda: _hummock(0))), (ids('VG06')[1], (lambda: _hummock(1)))], 0.1)),
    'a4_himalaya': ('v5_himalaya', mk(
        [(ids('SP01')[j], (lambda j=j: _snow_spire(j))) for j in range(6)] +
        [(ids('HL01')[3], _ice_spire4), (ids('HL02')[1], _ice_arch2)] +
        [(ids('HL03')[0], (lambda: _glacier(0))), (ids('HL03')[1], (lambda: _glacier(1))), (ids('HL03')[2], (lambda: _glacier(2)))] +
        [(ids('HL04')[1], _ice_cave2), (ids('HL07')[0], _mine1), (ids('HL07')[1], _mine2)], 0.1)),
    'a4_landmarks': ('v5_landmarks', mk(
        [(ids('LM04')[1], (lambda: _rampart(1))), (ids('LM04')[2], (lambda: _rampart(2)))] +
        [(ids('LM05')[1], _cliff_tower2)] +
        [(ids('LM06')[0], _gate_tunnel)] +
        [(ids('LM07')[0], (lambda: _switch_stairs(0))), (ids('LM07')[1], (lambda: _switch_stairs(1)))] +
        [(ids('LM08')[0], stone_span)], 0.1)),
}

