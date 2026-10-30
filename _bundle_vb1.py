def floor_medallion():
    """WT06_01 - 80 wide round inlay: granite field, limestone and brass rings, 16-point star ring, compass rose, indigo centre."""
    reset()
    A = Acc()
    ring = lambda r0, r1, z0, z1, key, n=72: A.sweep([(r0, z0), (r1, z0), (r1, z1), (r0, z1)], 0, 360, n, key)
    ring(0.4, 40.0, 0.0, 0.5, K['granite'])
    ring(36.5, 39.0, 0.5, 0.8, K['limestone'])
    ring(35.4, 36.2, 0.5, 0.85, K['brass'])
    ring(29.0, 29.7, 0.5, 0.85, K['brass'])
    ring(22.0, 28.4, 0.5, 0.75, K['white'])
    ring(21.0, 21.8, 0.5, 0.85, K['brass'])
    A.cyl(20.2, 0.7, (0, 0, 0.5), K['indigo'], verts=48)
    for k in range(16):
        a = k * 22.5
        r_in, r_out = 22.0, 34.0 if k % 2 == 0 else 29.0
        A.prism([(-1.2, 0.0), (1.2, 0.0), (0.0, r_out - r_in)], 0.3, polar(r_in, a), K['ochre'] if k % 2 == 0 else K['limestone'], (0, 0, a - 90.0), z0=0.5)
    for k in range(8):
        a = k * 45.0
        long = 19.0 if k % 2 == 0 else 12.0
        A.prism([(-2.0, 0.0), (2.0, 0.0), (0.0, long)], 0.35, (0, 0, 0), K['brass'] if k % 2 == 0 else K['limestone'], (0, 0, a - 90.0), z0=0.85)
    A.cyl(3.0, 0.4, (0, 0, 0.85), K['timber'], verts=24)
    A.cyl(1.2, 0.5, (0, 0, 1.25), K['brass'], verts=16)
    for k in range(72):
        x, y, _ = polar(37.8, k * 5.0)
        A.box((1.8 if k % 6 == 0 else 0.9, 0.22, 0.12), (x, y, 0.86), K['timber'], (0, 0, k * 5.0))
    A.to_scene()
    ob = finalize('wizard_floor_medallion', 30)
    for v in ob.data.vertices:                                                               # a flat inlay: 1 stud thick in total
        v.co.z *= 0.57
    ob.data.update()
    return ob


def map_table():
    """WT05_01 - the circular island map: coloured relief (from the planned terrain), granite pedestal and table, brass compass ring,
    outer scale ring (own palette key = own MeshPart) and tiny landmark tokens. About 13 studs tall, 47 across."""
    reset()
    M = _load_map()
    V, Fc, lab, remap, w, h = M['V'], M['F'], M['lab'], M['remap'], M['w'], M['h']
    A = Acc()
    DIAM, SC = 44.0, 40.0 / 44.0
    zmin = min(v[2] for v in V)
    Z0, ZS = 6.4, 0.7
    tz = lambda zz: Z0 + (zz - zmin) * ZS
    for a_, b_, c_ in Fc:
        pa, pb, pc = V[a_], V[b_], V[c_]
        cx, cy = (pa[0] + pb[0] + pc[0]) / 3.0, (pa[1] + pb[1] + pc[1]) / 3.0
        row = int(max(0, min(h - 1, (cy / DIAM + 0.5) * (h - 1))))
        colm = int(max(0, min(w - 1, (cx / DIAM + 0.5) * (w - 1))))
        key = remap[int(lab[row, colm])]
        bm = A._bm(key)
        bm.faces.new([bm.verts.new((p[0] * SC, p[1] * SC, tz(p[2]))) for p in (pa, pb, pc)])
    A.cyl(18.0, 1.0, (0, 0, 0), K['granite'], verts=32)
    A.cyl(13.5, 3.4, (0, 0, 1.0), K['granite'], verts=32, r2=11.5)
    for k in range(12):
        x, y, _ = polar(13.0, k * 30.0 + 15.0)
        A.box((1.6, 2.4, 3.4), (x, y, 2.9), K['limestone'], (0, 0, k * 30.0 + 15.0))
    A.cyl(23.0, 1.8, (0, 0, 4.6), K['limestone'], verts=48)
    A.sweep([(22.6, 4.6), (23.6, 4.6), (23.6, 6.4), (22.6, 6.4)], 0, 360, 48, K['brass'])
    A.sweep([(20.6, 6.3), (21.9, 6.3), (21.9, 6.9), (20.6, 6.9)], 0, 360, 48, K['brass'])
    A.sweep([(21.9, 6.4), (23.0, 6.4), (23.0, 6.9), (21.9, 6.9)], 0, 360, 72, 'vb_ring')
    for k in range(72):
        x, y, _ = polar(22.45, k * 5.0)
        A.box((0.9 if k % 6 else 1.4, 0.18, 0.12), (x, y, 6.96), K['timber'], (0, 0, k * 5.0))
    for k in range(4):
        x, y, _ = polar(22.0, k * 90.0)
        A.prism([(-0.7, 0), (0.7, 0), (0, 1.8)], 0.3, (x, y, 0), K['brass'], (0, 0, k * 90.0 - 90.0), z0=6.9)
    for k in range(24):
        x, y, _ = polar(23.2, k * 15.0)
        A.box((0.35, 0.35, 1.0), (x, y, 6.9), K['brass'])

    def disc(wx, wz):
        return ((wx + 3300.0) / 6600.0 - 0.5) * DIAM, -((wz + 3525.0) / 6600.0 - 0.5) * DIAM

    def ground(x, y):
        i = int(round(max(0, min(100, (x / DIAM + 0.5) * 100))))
        j = int(round(max(0, min(100, (-y / DIAM + 0.5) * 100))))
        return tz(V[j * 101 + i][2])
    marks = {'tower': (1380, -1320), 'capital': (0, -1585), 'tree': (-1700, -540), 'fortress': (1632, -1608),
             'skull': (2280, -1008), 'temple': (1660, 1130), 'town1': (0, 0), 'crater': (1368, -312)}
    for name, (wx, wz) in marks.items():
        x, y = disc(wx, wz)
        x, y = x * SC, y * SC
        z = ground(x / SC, y / SC)
        if name == 'tower':
            A.cyl(0.5, 2.2, (x, y, z), K['white'], verts=10)
            A.cyl(0.75, 0.8, (x, y, z + 2.2), K['copper'], verts=10, r2=0.0)
        elif name == 'capital':
            A.sweep([(1.7, z), (2.0, z), (2.0, z + 0.7), (1.7, z + 0.7)], 0, 360, 16, K['limestone'], loc=(x, y, 0))
            A.box((1.0, 1.0, 1.4), (x, y + 0.6, z + 0.7), K['granite'])
            A.cyl(0.6, 1.0, (x, y + 0.6, z + 1.4), K['copper'], verts=8, r2=0.0)
        elif name == 'tree':
            A.cyl(0.22, 1.1, (x, y, z), K['timber'], verts=8)
            A.ball(0.85, (x, y, z + 1.5), K['copper'], segs=8, rings=5)
        elif name == 'fortress':
            A.box((1.6, 1.0, 0.8), (x, y, z + 0.4), K['granite'])
            A.box((0.9, 0.8, 1.4), (x, y, z + 1.1), K['limestone'])
            A.cyl(0.45, 0.8, (x, y, z + 1.8), K['indigo'], verts=8, r2=0.0)
        elif name == 'skull':
            A.ball(0.55, (x, y, z + 0.5), K['white'], segs=8, rings=5)
        elif name == 'temple':
            for k in range(6):
                px, py, _ = polar(0.9, k * 60.0)
                A.cyl(0.14, 1.0, (x + px, y + py, z), K['limestone'], verts=6)
            A.sweep([(0.3, z + 1.0), (1.2, z + 1.0), (1.2, z + 1.2), (0.3, z + 1.2)], 0, 360, 12, K['ochre'], loc=(x, y, 0))
        elif name == 'town1':
            A.cyl(0.9, 0.3, (x, y, z), K['limestone'], verts=12)
            A.box((0.5, 0.5, 0.7), (x, y, z + 0.6), K['ochre'])
        else:
            A.cyl(0.8, 0.4, (x, y, z), K['granite'], verts=10, r2=0.4)
    A.to_scene(keep_normals=set(M['keys']))
    return finalize('wizard_round_map_table', 30)


def lab_orrery():
    reset()
    A = Acc()
    zc = 11.0
    A.cyl(3.6, 0.9, (-3.0, 0, 0), K['granite'], verts=16)
    A.cyl(1.2, 2.2, (-3.0, 0, 0.9), K['timber'], verts=10, r2=0.9)
    A.cyl(0.8, 7.2, (-3.0, 0, 3.0), K['brass'], verts=10)
    A.ball(1.1, (-3.0, 0, zc), K['brass'], segs=10, rings=6)
    for k, (R, sz, key) in enumerate(((2.0, 0.35, K['copper']), (3.3, 0.45, K['white']), (4.6, 0.6, K['ochre']), (5.8, 0.4, K['indigo']))):
        A.sweep([(R - 0.08, -0.08), (R + 0.08, -0.08), (R + 0.08, 0.08), (R - 0.08, 0.08)], 0, 360, 32, K['brass'], loc=(-3.0, 0, zc))
        x, y, _ = polar(R, 40.0 + k * 85.0)
        A.ball(sz, (-3.0 + x, y, zc), key, segs=8, rings=5)
        A.beam((-3.0, 0, zc), (-3.0 + x, y, zc), 0.1, 0.1, K['brass'])
    for k in range(3):
        x, y, _ = polar(2.2, k * 120.0 + 30.0)
        A.beam((6.5 + x, y, 0.0), (6.5, 0, 9.0), 0.4, 0.4, K['timber'])
    A.cyl(0.35, 2.4, (6.5, 0, 9.0), K['brass'], verts=8)
    A.sweep([(2.2, -0.14), (3.2, -0.14), (3.2, 0.14), (2.2, 0.14)], 0, 360, 36, K['brass'], loc=(6.5, 0, 12.2), rot=(80, 0, 0))
    A.sweep([(0.3, -0.1), (2.2, -0.1), (2.2, 0.1), (0.3, 0.1)], 0, 360, 36, K['copper'], loc=(6.5, 0, 12.2), rot=(80, 0, 0))
    A.box((0.3, 0.2, 3.6), (6.5, 0.1, 12.2), K['brass'], (0, 0, 0))
    A.to_scene()
    return finalize('wizard_lab_orrery', 30)


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
    A.box((5.0, 2.6, 2.4), (11.0, -2.0, 1.2), K['timber'])
    A.box((5.2, 2.8, 0.4), (11.0, -2.0, 2.6), K['ochre'])
    A.to_scene()
    return finalize('wizard_study_bed', 25)


def study_globe():
    reset()
    A = Acc()
    A.cyl(3.2, 0.7, (-4.0, 0, 0), K['granite'], verts=16)
    A.cyl(0.6, 4.2, (-4.0, 0, 0.7), K['timber'], verts=8)
    A.sweep([(3.5, -0.18), (3.9, -0.18), (3.9, 0.18), (3.5, 0.18)], 0, 360, 36, K['brass'], loc=(-4.0, 0, 7.3), rot=(23.5, 0, 0))
    A.ball(3.3, (-4.0, 0, 7.3), K['indigo'], segs=18, rings=12)
    for k in range(7):
        a, b = 40.0 * k, 25.0 + 17.0 * (k % 4)
        r = 3.3 * 0.99
        A.ball(1.0, (-4.0 + r * math.cos(math.radians(b)) * math.cos(math.radians(a)), r * math.cos(math.radians(b)) * math.sin(math.radians(a)), 7.3 + r * math.sin(math.radians(b))),
               K['copper'] if k % 2 else K['ochre'], segs=8, rings=5, scale=(1.0, 1.0, 0.35))
    A.cyl(0.18, 8.4, (-4.0, 0, 3.1), K['brass'], verts=6, rot=(23.5, 0, 0))
    for k in range(3):
        x, y, _ = polar(1.9, k * 120.0 + 90.0)
        A.beam((6.0 + x, y, 0.0), (6.0, 0, 9.5), 0.4, 0.4, K['timber'])
    A.box((6.0, 0.3, 4.4), (6.0, -0.6, 8.5), K['parchment'], (-12, 0, 0))
    A.box((6.6, 0.4, 0.5), (6.0, -0.5, 6.3), K['timber'])
    for k in range(6):
        A.box((0.4, 0.05, 0.4), (4.0 + k * 0.9, -0.82, 8.0 + (k % 3) * 0.7), K['indigo'], (0, 0, 20.0 * k))
    A.box((8.0, 4.4, 3.6), (-3.0, -5.6, 1.8), K['timber'])                                   # sea chest in front
    A.box((8.2, 4.6, 0.5), (-3.0, -5.6, 3.8), K['ochre'])
    for sx in (-5.6, -0.4):
        A.box((0.5, 4.7, 3.7), (sx, -5.6, 1.85), K['brass'])
    A.box((2.6, 1.8, 0.35), (-3.0, -5.6, 4.15), K['parchment'])
    for k in range(3):                                                                       # rolled charts in a rack behind
        A.cyl(0.5, 5.0, (1.2 + k * 1.3, 6.2, 0.6), K['parchment'], verts=8, rot=(0, 15, 0))
    A.box((5.4, 1.6, 0.5), (2.8, 6.2, 0.3), K['timber'])
    A.to_scene()
    return finalize('wizard_study_globe', 30)


def telescope():
    """WT10_01 - brass observatory telescope: stepped round pedestal, yoke, a long tube raised steeply, finder scope, eyepiece, counterweight."""
    reset()
    A = Acc()
    A.cyl(6.5, 1.0, (0, 0, 0), K['granite'], verts=24)
    A.cyl(4.8, 1.0, (0, 0, 1.0), K['limestone'], verts=24)
    A.cyl(1.8, 7.0, (0, 0, 2.0), K['brass'], verts=16, r2=1.4)
    for k in range(4):
        x, y, _ = polar(2.6, k * 90.0 + 45.0)
        A.beam((x, y, 2.2), (0, 0, 7.5), 0.5, 0.5, K['copper'])
    A.cyl(2.4, 1.4, (0, 0, 8.6), K['brass'], verts=16)
    for sx in (-1.9, 1.9):
        A.box((0.8, 2.4, 5.5), (sx, 0, 12.0), K['brass'])
    A.cyl(0.6, 4.8, (-2.4, 0, 12.0), K['copper'], verts=8, rot=(0, 90, 0))
    tilt, L = 22.0, 14.0
    d = math.radians(tilt)
    A.cyl(1.55, L, (0, 0, 12.0), K['brass'], verts=18, r2=1.2, rot=(tilt, 0, 0))
    for t in (3.0, 7.0, 11.0):
        A.cyl(1.7 - t * 0.02, 0.5, (0, -math.sin(d) * t, 12.0 + math.cos(d) * t), K['copper'], verts=18, rot=(tilt, 0, 0))
    A.cyl(1.9, 1.2, (0, -math.sin(d) * L, 12.0 + math.cos(d) * L), K['brass'], verts=18, rot=(tilt, 0, 0))
    A.cyl(0.4, 3.2, (0, math.sin(d) * 1.2, 12.0 - math.cos(d) * 1.2), K['copper'], verts=8, rot=(tilt + 180.0, 0, 0))
    A.cyl(0.35, 7.5, (1.6, -math.sin(d) * 3.0, 14.0 + math.cos(d) * 3.0), K['brass'], verts=8, rot=(tilt, 0, 0))
    A.ball(1.3, (0, math.sin(d) * 4.2, 12.0 - math.cos(d) * 4.2), K['copper'], segs=10, rings=6)
    for k in range(8):
        a = k * 45.0
        x, y, _ = polar(5.9, a)
        A.box((0.5, 0.3, 0.12), (x, y, 2.05), K['brass'], (0, 0, a))
    A.to_scene()
    return finalize('wizard_telescope', 30)
