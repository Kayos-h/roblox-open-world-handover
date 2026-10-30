def _grand_stair2(width, steps):
    """CP13_01 (lead pass 2) - grand stair with ONE continuous side wall per side (a prism following the step profile) instead of 36 overlapping boxes whose coplanar
    side faces rendered as black stripes; the back mass is wider than the walls so no faces coincide."""
    reset()
    A = Acc()
    rise = 22.0 / steps
    run = 40.0 / steps
    for i in range(steps):
        A.box((width, run, rise * (i + 1)), (0, -20.0 + run * (i + 0.5), rise * (i + 1) / 2.0), K['stone'] if i % 6 else K['trim'], bev=0.06)
    pts = [(-20.0, 0.0)]
    for i in range(steps):
        pts.append((-20.0 + run * i, rise * (i + 1) + 1.6))
        pts.append((-20.0 + run * (i + 1), rise * (i + 1) + 1.6))
    pts.append((20.0, 0.0))
    for sg in (-1, 1):
        x0 = width / 2.0 if sg > 0 else -width / 2.0 - 2.6
        A.prism(pts, 2.6, (x0, 0, 0), K['wall'], (90, 0, 90))
        for i in range(0, steps, 6):
            A.box((3.0, 3.0, 1.0), (sg * (width / 2.0 + 1.3), -20.0 + run * (i + 0.5), rise * (i + 1) + 2.1), K['trim'])
            A.cyl(0.35, 2.4, (sg * (width / 2.0 + 1.3), -20.0 + run * (i + 0.5), rise * (i + 1) + 2.6), K['iron'], verts=6)
    A.box((width + 5.8, 4.4, 22.0), (0, 18.0, 11.0), K['stone'])
    return _fin(A, 'grand_stair')


def _gate_post(A):
    W, D, H = 60.0, 40.0, 44.0
    for sx in (-1, 1):
        for k in range(int(D / 4.0) - 1):
            y = -D / 2.0 + 4.0 + k * 4.0
            A.box((1.2, 2.4, 2.4), (sx * (W / 2.0 - 0.4), y, H + 2.1), K['wall'])
            A.box((1.5, 2.7, 0.4), (sx * (W / 2.0 - 0.4), y, H + 3.5), K['cap'])
        for y in (-13.0, 0.0, 13.0):
            A.box((1.8, 2.6, 33.0), (sx * (W / 2.0 + 0.6), y, 18.0), K['stone'], bev=0.1)
            A.box((2.4, 3.2, 0.7), (sx * (W / 2.0 + 0.6), y, 34.8), K['trim'], bev=0.05)
        for z in (20.0, 29.0):
            for y in (-6.5, 6.5):
                A.box((0.5, 2.2, 3.6), (sx * (W / 2.0 + 0.05), y, z), K['glass'], bev=0)
                A.box((0.8, 3.0, 0.5), (sx * (W / 2.0 + 0.1), y, z + 2.1), K['trim'], bev=0)
    A.gable(26.0, 30.0, 9.0, (0, 0, H + 1.0), K['roof'], (0, 0, 0))
    A.box((27.0, 0.8, 0.6), (0, 0, H + 10.2), K['trim'])


def corner_1b():
    return LK.wrap(lambda: _corner(135, 11))()


def corner_3b():
    return LK.wrap(lambda: _corner(150, 13))()


def gatehouse_b():
    return LK.wrap(ORIG.gatehouse, post=_gate_post)()


def stair_wide_b():
    return LK.wrap(lambda: _grand_stair2(20.0, 36))()


# --- lead4 registration ---
import v5_leadkit as LK
BATCHES['lead4'] = ('v5_capital', mk([('CP02_01_ring_wall_corner_01', corner_1b), ('CP02_03_ring_wall_corner_03', corner_3b), ('CP07_01_gatehouse_main', gatehouse_b),
                                      ('CP13_01_grand_stair_01', stair_wide_b)], 0.12))
