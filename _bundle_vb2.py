def lab_bench():
    """WT07_01 - alchemy station 18 wide, 12 deep, 14 tall: long bench with glassware and a copper still, back shelf unit, hanging pots, stool."""
    reset()
    A = Acc()
    A.box((17.0, 6.4, 0.7), (0, 0, 3.65), K['timber'])
    for sx in (-7.8, 7.8):
        for sy in (-2.6, 2.6):
            A.box((0.9, 0.9, 3.3), (sx, sy, 1.65), K['timber'])
    A.box((16.4, 5.6, 0.35), (0, 0, 1.1), K['ochre'])
    for sx in (-8.4, 8.4):                                                                   # back shelf unit
        A.box((0.8, 2.2, 13.6), (sx, 4.8, 6.8), K['timber'])
    for z in (4.6, 7.8, 11.0, 13.3):
        A.box((17.6, 2.2, 0.45), (0, 4.8, z), K['ochre'])
    A.box((17.6, 0.4, 13.6), (0, 5.8, 6.8), K['timber'])
    rnd = random.Random(41)
    for z in (4.85, 8.05, 11.25):
        for k in range(10):
            _jar(A, -7.6 + k * 1.7, 4.8 + rnd.uniform(-0.4, 0.4), z, rnd.uniform(0.45, 0.65), rnd.uniform(1.0, 1.9), rnd.choice([K['glass'], K['parchment'], K['white'], K['glass']]))
    for k, x in enumerate((-6.0, -3.2, 0.6, 5.0)):                                           # flasks
        A.ball(0.95, (x, -1.0, 5.0), K['glass'], segs=10, rings=6)
        A.cyl(0.3, 1.5, (x, -1.0, 5.8), K['glass'], verts=8)
    A.cyl(1.2, 2.0, (-6.2, 1.4, 4.0), K['copper'], verts=12, r2=0.25)                        # copper still with a coil pipe
    A.cyl(0.22, 3.2, (-4.8, 1.4, 5.6), K['copper'], verts=6, rot=(0, 70, 0))
    A.cyl(0.6, 1.5, (2.2, 1.2, 4.0), K['brass'], verts=10)                                   # mortar
    A.beam((3.0, -0.6, 4.2), (5.4, 0.2, 4.2), 0.3, 0.3, K['brass'])                          # balance beam
    A.cyl(0.25, 2.2, (4.2, -0.2, 4.0), K['brass'], verts=6)
    A.box((6.0, 2.4, 0.14), (-1.0, -1.8, 4.1), K['parchment'])                               # recipe sheet
    A.beam((-8.4, 4.8, 13.9), (8.4, 4.8, 13.9), 0.3, 0.3, K['brass'])
    for k in range(5):                                                                       # hanging copper pots
        A.cyl(0.8, 1.1, (-6.4 + k * 3.2, 4.8, 12.4), K['copper'], verts=10, r2=0.65)
        A.box((0.08, 0.08, 0.6), (-6.4 + k * 3.2, 4.8, 13.6), K['timber'])
    A.cyl(1.5, 0.5, (4.0, -5.4, 2.4), K['ochre'], verts=12)                                  # stool
    for k in range(3):
        x, y, _ = polar(1.0, k * 120.0)
        A.box((0.4, 0.4, 2.4), (4.0 + x, -5.4 + y, 1.2), K['timber'])
    A.to_scene()
    return finalize('wizard_lab_bench', 25)


def lab_herbs():
    """WT07_02 - herb rack with jars and hanging bundles plus a front work table (18 wide, 12 deep, 13 tall)."""
    reset()
    A = Acc()
    for sx in (-8.0, 8.0):
        A.box((0.9, 4.4, 13.0), (sx, 3.6, 6.5), K['timber'])
    for z in (0.5, 3.6, 6.7, 9.8):
        A.box((16.9, 4.4, 0.5), (0, 3.6, z + 0.25), K['ochre'])
    A.box((17.0, 0.5, 13.0), (0, 5.9, 6.5), K['timber'])
    rnd = random.Random(21)
    for z in (0.75, 3.85, 6.95):
        for k in range(10):
            _jar(A, -7.2 + k * 1.6, 3.6 + rnd.uniform(-0.8, 0.8), z, rnd.uniform(0.45, 0.6), rnd.uniform(0.9, 1.6), rnd.choice([K['glass'], K['parchment'], K['white']]))
    A.beam((-8.0, 3.6, 12.6), (8.0, 3.6, 12.6), 0.3, 0.3, K['timber'])
    for k in range(8):
        x = -7.0 + k * 2.0
        A.cyl(0.5, 2.2, (x, 3.6, 10.2), K['copper'] if k % 2 else K['ochre'], verts=8, r2=0.1, rot=(180, 0, 0))
        A.box((0.08, 0.08, 0.9), (x, 3.6, 12.4), K['timber'])
    A.box((12.0, 4.2, 0.6), (0, -3.4, 3.4), K['timber'])                                     # work table
    for sx in (-5.4, 5.4):
        for sy in (-4.8, -2.0):
            A.box((0.7, 0.7, 3.1), (sx, sy, 1.55), K['timber'])
    A.cyl(0.8, 1.2, (-3.0, -3.2, 3.7), K['brass'], verts=10)
    for k in range(4):
        A.cyl(0.4, 2.4, (1.0 + k * 0.7, -3.6, 3.7), K['copper'] if k % 2 else K['ochre'], verts=6, rot=(80, 0, 10.0 * k))
    A.cyl(1.5, 1.4, (4.2, -3.2, 3.7), K['ochre'], verts=12, r2=1.2)
    A.to_scene()
    return finalize('wizard_lab_herbs', 25)


def lab_specimens():
    """WT07_03 - specimen shelf with jars, plus a display table with a glass bell jar (17 wide, 12 deep, 13 tall)."""
    reset()
    A = Acc()
    A.box((16.0, 4.6, 1.0), (0, 3.6, 0.5), K['granite'])
    A.box((16.0, 0.7, 12.0), (0, 5.7, 7.0), K['timber'])
    for sx in (-7.6, 7.6):
        A.box((0.8, 4.6, 12.0), (sx, 3.6, 7.0), K['timber'])
    for z in (1.0, 4.4, 7.8, 11.2):
        A.box((15.0, 4.4, 0.5), (0, 3.6, z + 0.25), K['ochre'])
    for z in (1.5, 4.9, 8.3):
        for k in range(5):
            x = -6.0 + k * 3.0
            A.cyl(0.9, 2.2, (x, 3.6, z), K['glass'], verts=10)
            A.cyl(0.75, 0.3, (x, 3.6, z + 2.2), K['brass'], verts=10)
            if k % 3 == 0:
                A.ball(0.55, (x, 3.6, z + 1.1), K['white'], segs=8, rings=5)
            elif k % 3 == 1:
                A.cyl(0.25, 1.4, (x, 3.6, z + 0.4), K['copper'], verts=6)
            else:
                A.ball(0.45, (x, 3.6, z + 0.9), K['bk_red'] if 'bk_red' in K else BOOK[0], segs=8, rings=5)
    A.cyl(3.6, 0.8, (0, -3.2, 2.2), K['granite'], verts=20)                                  # display table
    A.cyl(0.9, 2.2, (0, -3.2, 0), K['timber'], verts=10)
    A.cyl(2.6, 0.3, (0, -3.2, 3.0), K['brass'], verts=20)
    A.ball(2.4, (0, -3.2, 5.2), K['glass'], segs=16, rings=8, scale=(1, 1, 1.15))            # bell jar
    A.ball(0.9, (0, -3.2, 3.8), K['white'], segs=8, rings=5)
    for sx in (-5.8, 5.8):
        A.cyl(0.7, 2.6, (sx, -4.4, 0), K['timber'], verts=8)
        A.ball(1.2, (sx, -4.4, 3.4), K['copper'], segs=8, rings=5)
    A.to_scene()
    return finalize('wizard_lab_specimens', 25)


def study_desk():
    """WT08_01 - archmage study corner 17 wide, 13 deep, 12 tall: desk with open books and quill, chair, rug, bookcase, floor candlestick."""
    reset()
    A = Acc()
    A.box((16.0, 11.6, 0.12), (0, -0.2, 0.06), K['indigo'])                                  # rug with ochre border
    A.box((14.6, 10.2, 0.16), (0, -0.2, 0.1), K['ochre'])
    A.box((13.4, 9.0, 0.2), (0, -0.2, 0.12), K['indigo'])
    A.box((14.0, 6.0, 0.8), (0, 0, 4.2), K['timber'])
    for sx in (-6.3, 6.3):
        A.box((1.0, 5.0, 3.8), (sx, 0, 1.9), K['timber'])
        A.box((1.2, 5.4, 0.6), (sx, 0, 0.3), K['granite'])
    A.box((13.0, 0.4, 1.6), (0, 2.4, 5.0), K['ochre'])
    A.box((3.6, 2.6, 0.18), (-3.0, 0.2, 4.7), K['parchment'])
    A.box((3.6, 2.6, 0.18), (0.8, 0.2, 4.7), K['parchment'])
    A.box((0.2, 2.6, 0.3), (-1.1, 0.2, 4.75), BOOK[0])
    A.cyl(0.35, 1.0, (4.5, -0.8, 4.6), K['brass'], verts=8)
    A.beam((5.2, 0.4, 4.7), (6.2, 1.4, 6.4), 0.1, 0.1, K['white'])
    for k in range(4):
        A.box((2.4, 1.8, 0.45), (-5.2, 1.5, 4.8 + k * 0.46), BOOK[k % 5], (0, 0, k * 11.0))
    A.cyl(0.4, 0.7, (2.8, 1.8, 4.6), K['wax'], verts=8)
    A.box((4.0, 3.6, 0.6), (0, -4.2, 2.6), K['ochre'])                                       # chair
    A.box((4.0, 0.6, 3.6), (0, -5.8, 4.4), K['ochre'])
    for sx in (-1.6, 1.6):
        for sy in (-3.0, -5.4):
            A.box((0.5, 0.5, 2.3), (sx, sy, 1.15), K['timber'])
    for sx in (-8.4, 8.4):                                                                   # bookcase behind the desk
        A.box((0.7, 2.4, 12.0), (sx, 5.6, 6.0), K['timber'])
    for z in (0.3, 3.4, 6.5, 9.6, 11.8):
        A.box((17.0, 2.4, 0.5), (0, 5.6, z), K['ochre'])
    A.box((17.0, 0.4, 12.0), (0, 6.6, 6.0), K['timber'])
    rnd = random.Random(51)
    for z in (0.55, 3.65, 6.75, 9.85):
        _fill_books(A, rnd, lambda s, db: (-8.0 + s, 5.6, 90.0), 16.0, z, 2.6, (1.6, 2.0), BOOK, 0.07)
    A.cyl(0.9, 0.5, (-7.0, -3.4, 0), K['granite'], verts=10)                                 # floor candlestick (no glow)
    A.cyl(0.18, 6.4, (-7.0, -3.4, 0.5), K['brass'], verts=8)
    A.cyl(0.7, 0.4, (-7.0, -3.4, 6.9), K['brass'], verts=10)
    A.cyl(0.32, 1.2, (-7.0, -3.4, 7.3), K['wax'], verts=8)
    A.to_scene()
    return finalize('wizard_study_desk', 25)


def study_bed():
    reset()
    A = Acc()
    for sx in (-8.0, 8.0):
        for sy in (-6.0, 6.0):
            A.box((1.0, 1.0, 11.0), (sx, sy, 5.5), K['timber'])
            A.box((1.4, 1.4, 0.5), (sx, sy, 11.2), K['brass'])
    A.box((16.0, 12.6, 1.0), (0, 0, 2.4), K['timber'])
    A.box((15.0, 11.8, 1.3), (0, 0, 3.4), K['white'])
    A.box((15.2, 7.6, 0.5), (0.0, -2.2, 4.1), K['indigo'])
    for k in range(2):
        A.box((4.0, 2.4, 0.9), (-4.0 + k * 8.0, 4.4, 4.3), K['parchment'])
    A.box((16.6, 0.8, 8.0), (0, 6.6, 7.0), K['ochre'])
    for sg in (-1, 1):
        for k in range(5):
            A.box((1.1, 0.35, 8.4 - 0.15 * k), (sg * (6.5 - k * 0.8), -6.2 + (k % 2) * 0.5, 6.4), K['indigo'])
    A.beam((-8.0, -6.0, 10.8), (8.0, -6.0, 10.8), 0.3, 0.3, K['brass'])
    A.beam((-8.0, 6.0, 10.8), (8.0, 6.0, 10.8), 0.3, 0.3, K['brass'])
    A.box((16.0, 12.6, 0.5), (0, 0, 11.0), K['indigo'])
    A.box((14.0, 0.4, 0.4), (0, -6.4, 3.5), K['brass'])
    A.to_scene()
    return finalize('wizard_study_bed', 25)
