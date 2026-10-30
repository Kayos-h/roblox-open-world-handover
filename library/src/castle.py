"""C. Royal capital - Wizard King's castle (structure, throne room, grounds, noble district). Fronts face -Y."""
import math, random
from mathutils import Vector
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, top_paint
from arch import (F, faces, lbox, lbeam, beam3, slab, lslab, window, door, arrow_slit, quoins, band, corbels, battlements,
                  ring_battlements, gable_roof, roof_z, cone_roof, dormer, railing, wall_lantern, arc_pts, nm, lancet, rose_window,
                  column_c, pediment, dome, pinnacle, lancet_pts, flower_box)
from capital import (wall_run, round_tower, arch_block, stone_face, clock_face, pointed_portal, WT, WH, star_pts, crystal)

K, KD, KT = 'castle', 'ashlar', 'castle_trim'
ROOF = ('tile_a', 'tile_b')
CPAL = dict(key=K, dark=KD, trim=KT, faces_=(K, KT, 'ashlar'))


def bartizan(x, y, z, r=2.2, h=7.0, roof=ROOF, flag=None):
    """Corbelled corner turret starting at z."""
    lathe(nm('bz'), [(0.0, z - 3.0), (0.4, z - 3.0), (r * 0.7, z - 1.6), (r, z - 0.2), (r, z + h), (0.0, z + h)], loc=(x, y, 0), key=K, segs=16)
    for zz in (z, z + h - 0.3):
        lathe(nm('bzb'), [(0.0, zz - 0.2), (r + 0.25, zz - 0.2), (r + 0.25, zz + 0.25), (0.0, zz + 0.25)], loc=(x, y, 0), key=KT, segs=16)
    for k in range(3):
        a = 2 * math.pi * k / 3 + 0.5
        window(F(x + math.cos(a) * r, y + math.sin(a) * r, 0, math.degrees(a) + 90), 0, z + 1.5, w=0.9, h=2.6, arch=True, frame=KT, sill=None,
               panes=False, lit=(k == 0))
    return cone_roof(x, y, z + h, r, r * 3.2, keys=roof, rings=5, ov=0.4, finial='gold', segs=16, flag=flag)


def main_keep():
    """K1 - main keep: great hall block with royal balcony, corner turrets, central spire tower and blue roofs."""
    reset()
    W, D, H = 44.0, 30.0, 40.0
    box(nm('k'), (W, D, H), loc=(0, 0, H / 2), key=K)
    box(nm('kpl'), (W + 3, D + 3, 4.0), loc=(0, 0, 2.0), key=KD, bev=0.1)
    for zz in (4.0, 16.0, 30.0):
        band(0, 0, W, D, zz, 0.7, KT, out=0.3)
    fs = faces(0, 0, W, D)
    for k, (side, L) in enumerate((('front', W), ('back', W), ('left', D), ('right', D))):
        fr = fs[side]
        stone_face(fr, -L / 2, L / 2, 4.5, H - 1.0, int(L * 1.2), 300 + k, keys=(K, KT, 'ashlar'))
        n = int(L / 6.5)
        for i in range(n):
            x = -L / 2 + L * (i + 0.5) / n
            if side == 'front' and abs(x) < 8:
                continue
            lancet(fr, x, 6.0, w=2.4, h=7.5, glass='glass_dark', frame=KT, medallion=None)
            lancet(fr, x, 18.5, w=2.8, h=9.5, glass=('stained_b', 'stained_y')[i % 2], frame=KT, medallion='stained_r')
            window(fr, x, 32.0, w=2.0, h=4.6, arch=True, frame=KT, sill=KT, panes=True, lit=(i % 3 == 1))
        corbels(fr, -L / 2 + 0.6, L / 2 - 0.6, H - 2.0, KD, step=1.8, size=(0.7, 1.0, 1.4))
        battlements(fr, -L / 2, L / 2, H - 0.2, K, t=1.2, y=-0.8, cap=KT)
    fo = fs['front']
    pointed_portal(fo, 0, 7.0, 14.0, orders=3, trim=KT, tymp='gold')
    for k in range(6):
        box(nm('st'), (20.0 - k * 1.2, 1.6, 0.67), loc=(0, -D / 2 - 1.5 - 9.6 + k * 1.6 + 1.6, 0.33 + k * 0.67), key=KD if k % 2 else KT, bev=0.05)
    # royal balcony
    lbox(fo, (18.0, 4.0, 0.8), 0, -2.0, 16.4, KT, bev=0.08)
    for x in (-8.0, -3.0, 3.0, 8.0):
        lbeam(fo, (x, -0.2, 13.0), (x, -3.6, 16.0), 0.7, KT)
    for i in range(24):
        x = -8.6 + i * 0.75
        lathe(nm('bal'), [(0, 0), (0.22, 0), (0.15, 0.3), (0.28, 0.8), (0.14, 1.3), (0.22, 1.6), (0, 1.6)], loc=fo.p(x, -3.7, 16.8), key=KT, segs=8)
    lbox(fo, (18.0, 0.6, 0.35), 0, -3.7, 18.55, KT)
    for s in (-1, 1):
        lbox(fo, (0.6, 3.8, 0.35), s * 8.9, -1.9, 18.55, KT)
    door(fo.sub(0, 0, 17.2), 0, w=4.2, h=8.0, arch=True, key='glass_lit', surround=KT, step=None, studs=False)
    from props import cloth
    for s in (-1, 1):
        cloth(nm('kb'), 3.6, 11.0, fo.p(s * 6.5, -0.4, 29.6), 'fabric_blue', waves=0.5, amp=0.1, seed=s + 8)
        lbox(fo, (4.2, 0.3, 0.3), s * 6.5, -0.4, 29.7, 'gold')
        star = star_pts(0.4, 1.0, 4)
        lslab(fo.sub(s * 6.5, -0.65, 24.0), [(px, 0, pz) for px, pz in star], (0, -0.08, 0), 'gold')
    # roof
    gable_roof(F(), W - 4, D - 4, H + 1.4, 14.0, keys=ROOF, wall=K, ov=0.2, ovg=0.2, barge=KT, ridge='gold', crest='gold')
    for i in range(4):
        x = -15.0 + i * 10.0
        dormer(F(), x, -(D - 4) / 2 + 2.0, roof_z(H + 1.4, 14.0, D - 4, -(D - 4) / 2 + 2.0) - 0.4, w=3.6, h=4.4, depth=6.0, wall=K, keys=ROOF, frame=KT)
    # corner turrets
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * W / 2, sy * D / 2
            lathe(nm('ct'), [(0.0, 0.0), (5.4, 0.0), (5.4, 4.0), (4.6, 4.6), (4.6, H + 12.0), (0.0, H + 12.0)], loc=(x, y, 0), key=K, segs=24)
            for zz in (16.0, 30.0, H + 11.6):
                lathe(nm('ctb'), [(0.0, zz - 0.3), (4.9, zz - 0.3), (4.9, zz + 0.4), (0.0, zz + 0.4)], loc=(x, y, 0), key=KT, segs=24)
            for j in range(3):
                a = math.atan2(sy, sx) + (j - 1) * 0.9
                fr = F(x + math.cos(a) * 4.6, y + math.sin(a) * 4.6, 0, math.degrees(a) + 90)
                for zz in (20.0, 34.0, H + 5.0):
                    window(fr, 0, zz, w=1.6, h=3.6, arch=True, frame=KT, sill=KT, panes=False, lit=(j == 1 and zz > 30))
            ring_battlements(x, y, H + 12.0, 5.4, K, t=1.0, cap=KT, n=14)
            cone_roof(x, y, H + 14.6, 4.0, 16.0, keys=ROOF, rings=8, ov=0.8, flag='fabric_blue' if sx * sy > 0 else 'fabric_red')
            lathe(nm('ctr'), [(0.0, H + 12.0), (4.0, H + 12.0), (4.0, H + 14.6), (0.0, H + 14.6)], loc=(x, y, 0), key=K, segs=20)
    # central spire tower
    cz = H + 1.4
    box(nm('cs'), (12.0, 12.0, 24.0), loc=(0, 4.0, cz + 12.0), key=K)
    for zz in (cz + 11.0, cz + 23.6):
        band(0, 4.0, 12, 12, zz, 0.7, KT, out=0.3)
    for fr in faces(0, 4.0, 12, 12, cz).values():
        lancet(fr, 0, 13.0, w=2.6, h=9.0, glass='stained_b', frame=KT)
    clock_face(F(0, 4.0 - 6.0, cz, 0), 6.0, r=3.4)
    for sx in (-1, 1):
        for sy in (-1, 1):
            bartizan(sx * 6.0, 4.0 + sy * 6.0, cz + 20.0, r=1.6, h=5.0)
    lathe(nm('csp'), [(0.0, 0.0), (6.6, 0.0), (6.6, 0.8), (0.0, 0.8)], loc=(0, 4.0, cz + 24.0), key=KT, segs=8)
    cone_roof(0, 4.0, cz + 24.8, 6.0, 26.0, keys=ROOF, rings=10, ov=0.6, segs=8, flag='fabric_red')
    return finalize('main_keep', smooth_angle=25)


def castle_round_tower():
    """K2 - castle round tower, white stone, tall blue cone, corbelled lookout gallery."""
    reset()
    top = round_tower(0, 0, 8.0, 48.0, roof=ROOF, flag='fabric_blue', seed=22, doors=(0, 180), roof_h=26.0, **{k: v for k, v in CPAL.items() if k != 'faces_'})
    for k in range(4):
        a = 45 + 90 * k
        ar = math.radians(a)
        bartizan(math.cos(ar) * 8.6, math.sin(ar) * 8.6, 36.0, r=1.6, h=5.0)
    return finalize('castle_round_tower', smooth_angle=20)


def castle_square_tower():
    """K3 - square castle tower, corner bartizans, steep pyramid roof with dormers."""
    reset()
    s, H = 14.0, 46.0
    box(nm('sq'), (s, s, H), loc=(0, 0, H / 2), key=K)
    box(nm('sqp'), (s + 2.4, s + 2.4, 4.0), loc=(0, 0, 2.0), key=KD, bev=0.1)
    for zz in (4.0, 18.0, 32.0):
        band(0, 0, s, s, zz, 0.6, KT, out=0.3)
    for k, fr in enumerate(faces(0, 0, s, s).values()):
        stone_face(fr, -s / 2, s / 2, 4.5, H - 1, 40, 330 + k, keys=(K, KT, 'ashlar'))
        arrow_slit(fr, 0, 10.0, key=KD)
        lancet(fr, 0, 21.0, w=2.4, h=8.0, glass='stained_b', frame=KT, medallion=None)
        window(fr, -3.0, 35.0, w=2.0, h=4.6, arch=True, frame=KT, sill=KT, lit=(k == 0))
        window(fr, 3.0, 35.0, w=2.0, h=4.6, arch=True, frame=KT, sill=KT)
        corbels(fr, -s / 2 + 0.6, s / 2 - 0.6, H - 2.0, KD, step=1.6, size=(0.6, 0.9, 1.3))
        battlements(fr, -s / 2, s / 2, H - 0.2, K, t=1.0, y=-0.7, mw=1.4, gap=1.0, cap=KT)
    door(faces(0, 0, s, s)['front'], 0, w=3.6, h=7.0, surround=KT, lamp=True)
    lathe(nm('sr'), [(0.0, 0.0), (s / 2 * 1.414 - 1.0, 0.0), (s / 2 * 1.414 - 1.0, 2.0), (0.0, 2.0)], loc=(0, 0, H), key=K, segs=4)
    t = cone_roof(0, 0, H + 2.0, (s / 2 - 1.0) * 1.414, 22.0, keys=ROOF, rings=9, ov=0.6, segs=4, flag='fabric_blue')
    for fr in faces(0, 0, s - 2, s - 2, 0).values():
        dormer(fr.sub(0, 0, 0), 0, -0.6, H + 5.0, w=2.6, h=3.4, depth=3.0, wall=K, keys=ROOF, frame=KT)
    for sx in (-1, 1):
        for sy in (-1, 1):
            bartizan(sx * (s / 2 + 0.6), sy * (s / 2 + 0.6), H - 6.0, r=2.0, h=8.0)
    return finalize('castle_square_tower', smooth_angle=20)


def spire_tower():
    """K4 - very tall slender spire tower with a ring balcony, glowing windows and needle roof."""
    reset()
    r, H = 5.0, 66.0
    lathe(nm('sp'), [(0.0, 0.0), (r + 2.0, 0.0), (r + 2.0, 3.0), (r + 0.6, 4.0), (r, 5.0), (r, H), (0.0, H)], key=K, segs=24)
    for zz in (5.0, 18.0, 30.0, 42.0, H - 0.3):
        lathe(nm('spb'), [(0.0, zz - 0.3), (r + 0.3, zz - 0.3), (r + 0.3, zz + 0.4), (0.0, zz + 0.4)], key=KT, segs=24)
    for zz in (10.0, 22.0, 34.0, 46.0):
        for k in range(3):
            a = -90 + (k - 1) * 120 + zz * 3
            ar = math.radians(a)
            window(F(math.cos(ar) * r, math.sin(ar) * r, 0, a + 90), 0, zz, w=1.5, h=4.0, arch=True, frame=KT, sill=KT, panes=False,
                   lit=(zz > 40), glass='glass_dark')
    zb = 50.0
    lathe(nm('rb'), [(0.0, zb - 2.4), (r + 0.4, zb - 2.4), (r + 2.6, zb - 0.4), (r + 2.6, zb), (0.0, zb)], key=KT, segs=24)
    for i in range(30):
        a = 2 * math.pi * i / 30
        lathe(nm('rbb'), [(0, 0), (0.18, 0), (0.12, 0.4), (0.2, 0.9), (0.1, 1.4), (0, 1.4)], loc=(math.cos(a) * (r + 2.3), math.sin(a) * (r + 2.3), zb), key=KT, segs=6)
    torus(nm('rbt'), r + 2.3, 0.2, loc=(0, 0, zb + 1.5), key=KT, segs=36, rsegs=4)
    for k in range(4):
        a = 45 + 90 * k
        ar = math.radians(a)
        door(F(math.cos(ar) * r, math.sin(ar) * r, zb, a + 90), 0, w=2.0, h=4.6, arch=True, key='glass_lit', surround=KT, step=None, studs=False)
    for zz in (56.0, 61.0):
        for k in range(4):
            a = 90 * k + (zz - 56) * 9
            ar = math.radians(a)
            window(F(math.cos(ar) * r, math.sin(ar) * r, 0, a + 90), 0, zz, w=1.2, h=3.0, arch=True, frame=KT, sill=None, panes=False, lit=True)
    lathe(nm('st'), [(0.0, H), (r + 0.8, H), (r + 0.8, H + 1.0), (0.0, H + 1.0)], key=KT, segs=24)
    cone_roof(0, 0, H + 1.0, r + 0.3, 34.0, keys=ROOF, rings=12, ov=0.6, flag='fabric_red')
    door(F(0, -r - 2.0 + 0.6, 0, 0), 0, w=3.0, h=6.0, surround=KT)
    return finalize('spire_tower', smooth_angle=20)


def curtain_wall_straight():
    """K5 - castle curtain wall, 40 long, white stone."""
    reset()
    wall_run(F(), -20, 20, seed=51, **CPAL)
    return finalize('curtain_wall_straight', smooth_angle=20)


def curtain_wall_corner():
    """K6 - castle curtain wall corner with a corbelled corner turret."""
    reset()
    wall_run(F(), -WT / 2, 24, seed=61, **CPAL)
    wall_run(F(0, 0, 0, -90), -24, WT / 2, seed=62, **CPAL)
    lbox(F(), (WT, WT, 0.3), 0, 0, WH + 0.1, 'stone_dark')
    bartizan(-WT / 2 - 0.4, -WT / 2 - 0.4, WH - 2.0, r=2.6, h=8.0, flag='fabric_blue')
    return finalize('curtain_wall_corner', smooth_angle=20)


def wall_stairs():
    """K7 - stone stairs up the inner face of a wall to the 28-stud walkway, on arched supports, with a parapet."""
    reset()
    n = 28
    rise, run, wd = WH / n, 1.4, 5.0
    L = n * run
    pts = [(0.0, 0.0, 0.0)]
    pts += [(run * i, 0.0, rise * i) for i in range(1, n + 1)]
    for i in range(n):
        x = run * i
        z = rise * (i + 1)
        box(nm('s'), (run + 0.05, wd, rise + 1.2), loc=(x + run / 2, 0, z - (rise + 1.2) / 2), key=KT if i % 2 else K, bev=0.04)
    prof = [(0.0, 0.0, 0.0)] + [(run * (i + 1), 0.0, rise * (i + 1) - 0.5) for i in range(n)] + [(L, 0.0, 0.0)]
    stx = []
    for k in range(3):
        ax = L * (k + 0.5) / 3.6 + 2.0
    lslab(F(0, -wd / 2, 0, 0), [(0, 0, 0), (L, 0, WH - 0.5), (L, 0, 0)], (0, wd, 0), K)
    for s in (-1, 1):
        fr = F(0, s * wd / 2, 0, 0 if s < 0 else 180)
        for k in range(3):
            ax = L * (k + 0.65) / 3.6
            zt = ax / L * WH
            r = min(3.4, zt * 0.45)
            if r < 1.0:
                continue
            xx = ax if s < 0 else -ax
            lslab(fr, [(xx + math.cos(math.pi * i / 12) * r, -0.05, zt * 0.42 + math.sin(math.pi * i / 12) * r) for i in range(13)] +
                  [(xx - r, -0.05, 0.0), (xx + r, -0.05, 0.0)][::-1][::-1], (0, -0.1, 0), 'glass_dark')
            tube(nm('sa'), arc_pts(fr, xx, zt * 0.42, r + 0.2, y=-0.15, n=11), 0.25, KT, res=4)
    for i in range(0, n, 2):
        x = run * i
        lbox(F(), (run * 2 + 0.1, 0.7, 1.4), x + run, -wd / 2 - 0.35, rise * (i + 1) + 0.7, K)
        lbox(F(), (run * 2 + 0.3, 0.9, 0.2), x + run, -wd / 2 - 0.35, rise * (i + 1) + 1.45, KT)
    box(nm('land'), (5.0, wd, 0.5), loc=(L + 2.5, 0, WH - 0.25), key=KT)
    box(nm('lands'), (5.0, wd, WH - 0.5), loc=(L + 2.5, 0, (WH - 0.5) / 2), key=K)
    wall_lantern(F(0, -wd / 2 - 0.7, 0, 0), 2.0, 3.5, s=1.2)
    return finalize('wall_stairs', smooth_angle=20)


def portcullis(f, w, h, z, depth_y):
    nx = int(w / 1.1)
    for k in range(nx + 1):
        xx = -w / 2 + w * k / nx
        lbox(f, (0.24, 0.24, h), xx, depth_y, z + h / 2, 'iron_dark')
        lathe(nm('pc'), [(0, 0), (0.17, 0), (0, 0.6)], loc=f.p(xx, depth_y, z + 0.05), key='iron_dark', segs=4, rot=(180, 0, 0))
    for j in range(int(h / 1.6)):
        lbox(f, (w, 0.2, 0.24), 0, depth_y - 0.05, z + 0.8 + j * 1.6, 'iron_dark')


def gatehouse():
    """K8 - castle gatehouse: arched passage with portcullis, flanking square towers with bartizans, royal crest."""
    reset()
    f = F()
    gw, gd, gh = 24.0, 18.0, 34.0
    arch_block(f, -gw / 2, gw / 2, -gd / 2, gd / 2, 0, gh, 0, 11.0, 5.5, K)
    for s in (-1, 1):
        fr = f.sub(0, s * gd / 2, 0, 0 if s < 0 else 180)
        tube(nm('va'), arc_pts(fr, 0, 11.0, 6.1, y=-0.3, n=21), 0.7, KT, res=4)
        lbox(fr, (1.4, 0.9, 2.0), 0, -0.4, 17.4, 'gold', bev=0.06)
        stone_face(fr, -gw / 2, gw / 2, 1.0, gh - 2, 60, 80 + s, keys=(K, KT, 'ashlar'))
        corbels(fr, -gw / 2 + 0.6, gw / 2 - 0.6, gh - 2.2, KD, step=1.8, size=(0.7, 1.0, 1.4))
        battlements(fr, -gw / 2, gw / 2, gh - 0.4, K, t=1.3, y=-0.9, cap=KT)
        for xx in (-7.5, 7.5):
            window(fr, xx, 21.0, w=2.2, h=4.8, arch=True, frame=KT, sill=KT, lit=(s < 0))
        for k in range(4):
            lbox(fr, (0.9, 0.5, 0.9), -3.0 + k * 2.0, -0.3, 19.5, KD)
    fo = f.sub(0, -gd / 2)
    portcullis(fo, 10.4, 9.0, 6.5, 1.4)
    for s in (-1, 1):
        lbox(fo, (0.8, 1.0, 13.0), s * 5.6, 1.4, 6.5, KD)
        tube(nm('pch'), [fo.p(s * 4.6, 1.4, 15.4), fo.p(s * 4.6, 1.4, 19.0)], 0.12, 'iron', res=4)
    lbox(fo, (7.4, 0.5, 8.0), 0, -0.25, 26.0, KT, bev=0.1)
    lslab(fo.sub(0, -0.5, 25.5), [(-2.6, 0, 3.4), (2.6, 0, 3.4), (2.6, 0, 0.6), (0, 0, -2.6), (-2.6, 0, 0.6)], (0, -0.35, 0), 'fabric_blue')
    lslab(fo.sub(0, -0.85, 25.8), [(px, 0, pz) for px, pz in star_pts(0.6, 1.6, 4)], (0, -0.1, 0), 'gold')
    for i, xx in enumerate((-1.8, 0, 1.8)):
        lathe(nm('cw'), [(0, 0), (0.45, 0), (0.12, 1.0 + (0.3 if i == 1 else 0)), (0, 1.1 + (0.3 if i == 1 else 0))], loc=fo.p(xx, -0.5, 29.6), key='gold', segs=6)
    for s in (-1, 1):
        lbox(f, (0.4, 5.6, 11.0), s * 5.2, -gd / 2 + 4.8, 5.5, 'wood_dark')
        for zz in (2.5, 8.5):
            lbox(f, (0.12, 5.2, 0.4), s * 5.0, -gd / 2 + 4.8, zz, 'iron')
        tx = s * (gw / 2 + 5.0)
        ts, th = 10.0, 44.0
        box(nm('gt'), (ts, ts + 2, th), loc=(tx, -1.0, th / 2), key=K)
        box(nm('gtp'), (ts + 2.0, ts + 4.0, 4.0), loc=(tx, -1.0, 2.0), key=KD, bev=0.1)
        for zz in (4.0, 20.0, 34.0):
            band(tx, -1.0, ts, ts + 2, zz, 0.6, KT, out=0.3)
        for k, (nmf, fr) in enumerate(faces(tx, -1.0, ts, ts + 2).items()):
            arrow_slit(fr, 0, 12.0, key=KD)
            lancet(fr, 0, 23.0, w=2.2, h=7.0, glass='stained_b', frame=KT, medallion=None)
            window(fr, 0, 36.0, w=2.0, h=4.0, arch=True, frame=KT, sill=KT, lit=(nmf == 'front'))
            L = ts if nmf in ('front', 'back') else ts + 2
            corbels(fr, -L / 2 + 0.5, L / 2 - 0.5, th - 2.0, KD, step=1.6, size=(0.6, 0.9, 1.3))
            battlements(fr, -L / 2, L / 2, th - 0.2, K, t=1.0, y=-0.7, mw=1.3, gap=1.0, cap=KT)
        lathe(nm('gtr'), [(0.0, 0.0), ((ts / 2 - 0.8) * 1.414, 0.0), ((ts / 2 - 0.8) * 1.414, 2.0), (0.0, 2.0)], loc=(tx, -1.0, th), key=K, segs=4)
        cone_roof(tx, -1.0, th + 2.0, (ts / 2 - 0.8) * 1.414, 16.0, keys=ROOF, rings=7, ov=0.5, segs=4, flag='fabric_blue')
        bartizan(tx + s * (ts / 2 + 0.4), -1.0 - (ts + 2) / 2 - 0.4, th - 8.0, r=1.8, h=6.0)
        from props import cloth
        fb = F(tx, -1.0 - (ts + 2) / 2, 0, 0)
        lbeam(fb, (0, -0.1, 31.0), (0, -1.4, 31.0), 0.25, 'gold')
        cloth(nm('ban'), 4.0, 12.0, fb.p(0, -1.4, 31.0), 'fabric_blue', waves=0.6, amp=0.15, seed=s + 9)
        lbox(fb, (0.6, 0.2, 12.0), 0, -1.55, 25.0, 'gold')
    lbox(f, (11.0, gd + 2, 0.25), 0, 0, 0.12, 'stone_dark')
    return finalize('gatehouse', smooth_angle=20)


def drawbridge():
    """K9 - lowered timber drawbridge, 12 wide x 26 long, iron straps, hinge beam and lifting chains."""
    reset()
    W, L, T = 12.0, 26.0, 1.0
    rnd = random.Random(9)
    n = 10
    for i in range(n):
        x = -W / 2 + W * (i + 0.5) / n
        box(nm('pl'), (W / n - 0.08, L, T), loc=(x, -L / 2, T / 2 + rnd.uniform(-0.03, 0.03)), key=rnd.choice(['wood', 'wood_dark', 'wood']))
    for y in (-2.0, -L / 2, -L + 2.0):
        box(nm('cr'), (W + 0.4, 1.2, 0.5), loc=(0, y, -0.25), key='wood_dark')
        box(nm('st'), (W + 0.2, 0.4, 0.08), loc=(0, y, T + 0.04), key='iron')
        for k in range(8):
            ball(nm('rv'), 0.08, loc=(-W / 2 + 0.6 + k * (W - 1.2) / 7, y, T + 0.1), key='iron', segs=6, rings=4)
    for s in (-1, 1):
        box(nm('ed'), (0.5, L, 0.6), loc=(s * (W / 2 - 0.25), -L / 2, T + 0.3), key='iron_dark')
        torus(nm('ey'), 0.4, 0.1, loc=(s * (W / 2 - 0.6), -L + 0.8, T + 0.6), key='iron', segs=12, rsegs=4, rot=(0, 90, 0))
        from kitlib import chain
        chain(nm('ch'), (s * (W / 2 - 0.6), -L + 0.8, T + 1.0), (s * (W / 2 - 0.6), 0.5, 20.0), link=0.7, thick=0.12)
        box(nm('hb'), (1.2, 1.4, 1.4), loc=(s * (W / 2 + 0.3), 0, 0.3), key='iron_dark', bev=0.05)
    cyl(nm('hinge'), 0.5, W + 1.6, loc=(-W / 2 - 0.8, 0, 0.3), key='iron_dark', verts=12, rot=(0, 90, 0))
    return finalize('drawbridge', smooth_angle=20)


def moat_bridge():
    """K10 - grand stone moat bridge: three arches, balustrades, statue plinths with glowing orbs, 64 long."""
    reset()
    L, Wd, Hd = 64.0, 16.0, 14.0
    f = F(0, 0, 0, 90)
    pts = [(-L / 2, -Wd / 2, 0.0)]
    for (cx, r) in ((-20.0, 7.0), (0.0, 9.0), (20.0, 7.0)):
        spring = 3.0
        for i in range(17):
            a = math.pi - math.pi * i / 16
            pts.append((cx + math.cos(a) * r, -Wd / 2, spring + math.sin(a) * r * 0.9 if i not in (0, 16) else 0.0))
            if i == 0:
                pts[-1] = (cx - r, -Wd / 2, 0.0)
                pts.append((cx - r, -Wd / 2, spring))
            if i == 16:
                pts[-1] = (cx + r, -Wd / 2, spring)
                pts.append((cx + r, -Wd / 2, 0.0))
    pts += [(L / 2, -Wd / 2, 0.0), (L / 2, -Wd / 2, Hd), (-L / 2, -Wd / 2, Hd)]
    lslab(f, pts, (0, Wd, 0), K)
    for s in (-1, 1):
        fr = f.sub(0, s * Wd / 2, 0, 0 if s < 0 else 180)
        for (cx, r) in ((-20.0, 7.0), (0.0, 9.0), (20.0, 7.0)):
            xx = cx * (-1 if s > 0 else 1) * -1 if False else (cx if s < 0 else -cx)
            ar = [fr.p(xx + math.cos(math.pi * i / 16) * (r + 0.4), -0.3, 3.0 + math.sin(math.pi * i / 16) * (r * 0.9 + 0.4)) for i in range(17)]
            tube(nm('vo'), ar, 0.55, KT, res=4)
        for px in (-10.0, 10.0):
            lslab(fr, [(px - 2.0, 0.0, 0.0), (px + 2.0, 0.0, 0.0), (px + 2.0, 0.0, 9.0), (px, 0.0, 11.0), (px - 2.0, 0.0, 9.0)], (0, -2.4, 0), K)
        lbox(fr, (L, 0.6, 0.7), 0, -0.3, Hd - 0.4, KT)
        stone_face(fr, -L / 2, L / 2, 1.0, Hd - 1.2, 80, 100 + s, keys=(K, KT, 'ashlar'))
        lbox(fr, (L, 1.0, 0.6), 0, 0.5, Hd + 0.3, K)
        lbox(fr, (L, 1.1, 0.4), 0, 0.5, Hd + 2.8, KT)
        for i in range(56):
            x = -L / 2 + 1.0 + i * (L - 2.0) / 55
            lathe(nm('bal'), [(0, 0), (0.28, 0), (0.2, 0.4), (0.36, 1.0), (0.18, 1.6), (0.28, 1.9), (0, 1.9)], loc=fr.p(x, 0.5, Hd + 0.6), key=KT, segs=6)
        for x in (-L / 2 + 1.0, -10.0, 10.0, L / 2 - 1.0):
            box(nm('np'), (2.0, 2.0, 4.6), loc=fr.p(x, 0.5, Hd + 2.3), key=K, bev=0.06)
            box(nm('npc'), (2.4, 2.4, 0.4), loc=fr.p(x, 0.5, Hd + 4.8), key=KT, bev=0.05)
            lathe(nm('op'), [(0, 0), (0.6, 0), (0.3, 0.6), (0.5, 1.0), (0, 1.0)], loc=fr.p(x, 0.5, Hd + 5.0), key='gold', segs=10)
            ball(nm('orb'), 0.75, loc=fr.p(x, 0.5, Hd + 6.6), key='magic', segs=12, rings=8)
    rnd = random.Random(10)
    box(nm('dk'), (Wd - 2.0, L, 0.15), loc=(0, 0, Hd + 0.08), key='grout')
    for i in range(70):
        box(nm('cb'), (rnd.uniform(1.6, 2.6), rnd.uniform(1.6, 2.6), 0.12), loc=(rnd.uniform(-Wd / 2 + 2, Wd / 2 - 2), rnd.uniform(-L / 2 + 1, L / 2 - 1), Hd + 0.16),
            key=rnd.choice(['cob_a', 'cob_b', 'cob_c', 'stone_light']), rot=(0, 0, rnd.uniform(0, 90)))
    for s in (-1, 1):
        box(nm('cl'), (3.0, L, 0.2), loc=(0, 0, Hd + 0.26), key='castle_trim') if s < 0 else None
    return finalize('moat_bridge', smooth_angle=20)


ITEMS_STRUCT = [
    ('K01_main_keep', main_keep), ('K02_castle_round_tower', castle_round_tower), ('K03_castle_square_tower', castle_square_tower),
    ('K04_spire_tower', spire_tower), ('K05_curtain_wall_straight', curtain_wall_straight), ('K06_curtain_wall_corner', curtain_wall_corner),
    ('K07_wall_stairs', wall_stairs), ('K08_gatehouse', gatehouse), ('K09_drawbridge', drawbridge), ('K10_moat_bridge', moat_bridge),
]



# ============================================================ throne room interior
from kitlib import flame, chain


def throne():
    """K11 - the Wizard King's throne: tall gilded back with star crest, red velvet, on a three-step dais."""
    reset()
    for k in range(3):
        box(nm('d'), (14.0 - k * 2.4, 11.0 - k * 2.0, 0.8), loc=(0, 0.6 + k * 0.6, 0.4 + k * 0.8), key='marble' if k % 2 == 0 else KT, bev=0.06)
        box(nm('dc'), (13.0 - k * 2.4, 10.0 - k * 2.0, 0.04), loc=(0, 0.6 + k * 0.6, 0.82 + k * 0.8), key='carpet')
    z = 2.4
    box(nm('seat'), (5.2, 4.4, 1.2), loc=(0, 1.6, z + 1.6), key='gold', bev=0.12)
    box(nm('cush'), (4.4, 3.8, 0.6), loc=(0, 1.5, z + 2.5), key='velvet', bev=0.25, segs=3)
    for s in (-1, 1):
        box(nm('leg'), (0.8, 0.8, 1.2), loc=(s * 2.2, -0.2, z + 0.6), key='gold', bev=0.1)
        box(nm('leg'), (0.8, 0.8, 1.2), loc=(s * 2.2, 3.4, z + 0.6), key='gold', bev=0.1)
        box(nm('arm'), (0.9, 4.2, 0.6), loc=(s * 2.9, 1.6, z + 4.0), key='gold', bev=0.15)
        box(nm('armp'), (0.7, 3.6, 0.3), loc=(s * 2.9, 1.7, z + 4.4), key='velvet', bev=0.1)
        lbeam(F(), (s * 2.9, -0.2, z + 2.2), (s * 2.9, -0.4, z + 4.0), 0.6, 'gold')
        ball(nm('armb'), 0.5, loc=(s * 2.9, -0.4, z + 4.2), key='gold', segs=10, rings=7)
    back = [(-2.8, 0, 0.0), (2.8, 0, 0.0), (2.8, 0, 7.5), (2.0, 0, 9.0), (0.9, 0, 9.6), (0.0, 0, 11.2), (-0.9, 0, 9.6), (-2.0, 0, 9.0), (-2.8, 0, 7.5)]
    lslab(F(0, 3.8, z + 2.2, 0), back, (0, 0.8, 0), 'gold')
    inner = [(-2.1, 0, 0.6), (2.1, 0, 0.6), (2.1, 0, 7.0), (1.5, 0, 8.2), (0.0, 0, 9.4), (-1.5, 0, 8.2), (-2.1, 0, 7.0)]
    lslab(F(0, 3.75, z + 2.2, 0), inner, (0, 0.2, 0), 'velvet')
    for k in range(4):
        ball(nm('btn'), 0.12, loc=(-1.2 + k * 0.8, 3.5, z + 6.0), key='gold', segs=6, rings=4)
        ball(nm('btn'), 0.12, loc=(-0.8 + k * 0.53, 3.5, z + 7.6), key='gold', segs=6, rings=4)
    lslab(F(0, 3.7, z + 13.4, 0), [(px, 0, pz) for px, pz in star_pts(0.7, 1.8, 4)], (0, 0.5, 0), 'gold')
    ball(nm('gem'), 0.5, loc=(0, 3.6, z + 13.4), key='magic', segs=10, rings=7)
    for s in (-1, 1):
        lathe(nm('fin'), [(0, 0), (0.45, 0), (0.3, 0.6), (0.5, 1.1), (0.15, 1.6), (0, 2.0)], loc=(s * 2.8, 4.2, z + 9.7), key='gold', segs=10)
        tube(nm('scr'), [(s * 2.8, 3.7, z + 5.0), (s * 3.6, 3.6, z + 6.4), (s * 3.2, 3.6, z + 7.6), (s * 2.8, 3.8, z + 7.8)], 0.22, 'gold', res=6)
    return finalize('throne', smooth_angle=35)


def throne_pillar():
    """K12 - throne room pillar: 30-stud marble column, gold capital and base."""
    reset()
    box(nm('pb'), (5.0, 5.0, 1.0), loc=(0, 0, 0.5), key=KT, bev=0.08)
    lathe(nm('b'), [(0, 1.0), (2.3, 1.0), (2.3, 1.5), (2.0, 1.8), (2.1, 2.1), (1.8, 2.4), (0, 2.4)], key='gold', segs=24)
    lathe(nm('s'), [(0, 2.4), (1.7, 2.4), (1.55, 26.0), (0, 26.0)], key='marble', segs=24)
    for i in range(12):
        a = 2 * math.pi * i / 12
        tube(nm('fl'), [(math.cos(a) * 1.68, math.sin(a) * 1.68, 3.0), (math.cos(a) * 1.55, math.sin(a) * 1.55, 25.5)], 0.12, KT, res=4)
    for zz in (9.0, 18.0):
        torus(nm('band'), 1.68, 0.16, loc=(0, 0, zz), key='gold', segs=24, rsegs=5)
    lathe(nm('c'), [(0, 26.0), (1.6, 26.0), (1.9, 26.6), (2.4, 27.4), (2.9, 28.0), (0, 28.0)], key='gold', segs=24)
    for i in range(8):
        a = 2 * math.pi * i / 8
        scr = [(math.cos(a) * 2.0, math.sin(a) * 2.0, 26.6), (math.cos(a) * 2.8, math.sin(a) * 2.8, 27.0), (math.cos(a) * 2.6, math.sin(a) * 2.6, 27.7)]
        tube(nm('cs'), scr, 0.2, 'gold', res=4)
    box(nm('ab'), (6.2, 6.2, 1.2), loc=(0, 0, 28.6), key=KT, bev=0.08)
    box(nm('ab2'), (6.6, 6.6, 0.8), loc=(0, 0, 29.6), key='gold', bev=0.06)
    return finalize('throne_pillar', smooth_angle=35)


def chandelier():
    """K13 - three-tier gold chandelier with 24 candles on a hanging chain."""
    reset()
    zc = 4.0
    chain(nm('ch'), (0, 0, 14.0), (0, 0, zc + 4.2), link=0.5, thick=0.08, key='gold')
    torus(nm('hk'), 0.4, 0.1, loc=(0, 0, 14.3), key='gold', segs=12, rsegs=4, rot=(90, 0, 0))
    lathe(nm('st'), [(0, zc - 1.6), (0.3, zc - 1.6), (0.7, zc - 0.9), (0.3, zc), (0.25, zc + 3.0), (0.6, zc + 3.4), (0.2, zc + 4.2), (0, zc + 4.2)], key='gold', segs=12)
    ball(nm('drop'), 0.35, loc=(0, 0, zc - 1.9), key='magic', segs=10, rings=7)
    for tier, (R, z, n) in enumerate(((3.6, zc, 12), (2.5, zc + 1.5, 8), (1.5, zc + 2.8, 4))):
        torus(nm('r'), R, 0.12, loc=(0, 0, z), key='gold', segs=36, rsegs=5)
        for i in range(n):
            a = 2 * math.pi * (i + tier * 0.25) / n
            x, y = math.cos(a) * R, math.sin(a) * R
            tube(nm('arm'), [(math.cos(a) * 0.3, math.sin(a) * 0.3, z + 0.6), (x * 0.6, y * 0.6, z - 0.4), (x, y, z)], 0.07, 'gold', res=4)
            lathe(nm('cup'), [(0, 0), (0.25, 0), (0.32, 0.18), (0, 0.18)], loc=(x, y, z + 0.1), key='gold', segs=8)
            cyl(nm('cd'), 0.13, 0.9, loc=(x, y, z + 0.28), key='wax', verts=8)
            flame(nm('fl'), (x, y, z + 1.2), h=0.45, r=0.12, tongues=0, seed=i)
            if tier == 0:
                ball(nm('pr'), 0.13, loc=(x, y, z - 0.45), key='glass', segs=6, rings=4, scale=(1, 1, 1.6))
    return finalize('chandelier', smooth_angle=35)


def red_carpet():
    """K14 - red carpet runner, 10 x 60, gold borders and a star medallion pattern."""
    reset()
    W, L = 10.0, 60.0
    box(nm('c'), (W, L, 0.12), loc=(0, 0, 0.06), key='carpet')
    for s in (-1, 1):
        box(nm('bd'), (0.7, L, 0.14), loc=(s * (W / 2 - 0.6), 0, 0.07), key='gold')
        box(nm('bd2'), (0.2, L, 0.14), loc=(s * (W / 2 - 1.3), 0, 0.07), key='gold')
        box(nm('end'), (W, 0.7, 0.14), loc=(0, s * (L / 2 - 0.6), 0.07), key='gold')
        for i in range(int(W / 0.5)):
            box(nm('fr'), (0.12, 0.8, 0.04), loc=(-W / 2 + 0.25 + i * 0.5, s * (L / 2 + 0.35), 0.02), key='gold')
    for k in range(5):
        y = -L / 2 + L * (k + 0.5) / 5
        slab([(px, y + pz, 0.13) for px, pz in star_pts(0.9, 2.2, 4)], (0, 0, 0.02), 'gold')
        cyl(nm('md'), 0.7, 0.03, loc=(0, y, 0.14), key='velvet', verts=12)
    return finalize('red_carpet', smooth_angle=20)


def stained_window():
    """K15 - tall stained glass window insert (8 wide, 22 tall) with tracery and a rose top; set into a wall."""
    reset()
    f = F()
    w, h = 7.0, 20.0
    lslab(f, [(px, 0.0, pz) for px, pz in lancet_pts(0, 0.0, h - w * 0.866, w + 1.2)], (0, 1.4, 0), KT)
    lancet(f, -1.7, 1.0, w=2.8, h=12.0, glass='stained_b', frame='gold', medallion='stained_y')
    lancet(f, 1.7, 1.0, w=2.8, h=12.0, glass='stained_r', frame='gold', medallion='stained_g')
    rose_window(f, 0, 15.5, 2.2, keys=('stained_y', 'stained_b', 'stained_r', 'stained_g'), frame='gold', petals=8)
    lslab(f, [(px, -0.02, pz) for px, pz in lancet_pts(0, 0.0, h - w * 0.866, w)], (0, -0.05, 0), 'stained_b')
    tube(nm('fr'), [f.p(px, -0.3, pz) for px, pz in lancet_pts(0, 0.0, h - w * 0.866, w + 0.4)[1:-1]], 0.35, KT, res=4)
    lbox(f, (w + 2.0, 1.2, 0.6), 0, -0.4, -0.3, KT, bev=0.06)
    return finalize('stained_window', smooth_angle=25)


def tapestry(name, field, border, design):
    reset()
    from props import cloth
    W, H = 7.0, 14.0
    cyl(nm('rod'), 0.18, W + 1.6, loc=(-W / 2 - 0.8, -0.4, H + 0.3), key='gold', verts=10, rot=(0, 90, 0))
    for s in (-1, 1):
        ball(nm('rf'), 0.35, loc=(s * (W / 2 + 0.9), -0.4, H + 0.3), key='gold', segs=8, rings=6)
        lbeam(F(), (s * (W / 2 + 0.3), 0, H + 0.3), (s * (W / 2 + 0.3), -0.4, H + 0.3), 0.3, 'iron')
    cloth(nm('t'), W, H, (0, -0.4, H), field, waves=0.8, amp=0.06, seed=3)
    f = F(0, -0.62, 0, 0)
    for s in (-1, 1):
        lbox(f, (0.5, 0.06, H - 0.8), s * (W / 2 - 0.5), 0, H / 2 + 0.4, border)
    lbox(f, (W - 0.6, 0.06, 0.5), 0, 0, H - 0.6, border)
    pts = [(-W / 2 + 0.3, 0, 1.8), (W / 2 - 0.3, 0, 1.8), (W / 2 - 0.3, 0, 0.9), (0, 0, -0.4), (-W / 2 + 0.3, 0, 0.9)]
    lslab(f, pts, (0, -0.05, 0), border)
    design(f, W, H)
    for i in range(7):
        x = -W / 2 + 0.6 + i * (W - 1.2) / 6
        tube(nm('tas'), [f.p(x, 0, -0.3 if abs(x) < 1 else 0.6), f.p(x, 0, -1.2 if abs(x) < 1 else -0.2)], 0.06, border, res=4)
    return finalize(name, smooth_angle=30)


def tapestry_1():
    """K16 - tapestry: royal blue with the gold four-pointed star of the Wizard King."""
    def d(f, W, H):
        lslab(f.sub(0, -0.02, H * 0.55), [(px, 0, pz) for px, pz in star_pts(0.9, 2.6, 4)], (0, -0.05, 0), 'gold')
        torus(nm('ring'), 2.0, 0.12, loc=f.p(0, -0.06, H * 0.55), key='gold', segs=24, rsegs=4, rot=(90, 0, 0))
        for k in range(3):
            cyl(nm('dot'), 0.25, 0.04, loc=f.p(-1.2 + k * 1.2, -0.04, 3.0), key='fabric_cream', verts=8, rot=(90, 0, 0))
    return tapestry('tapestry_1', 'fabric_blue', 'gold', d)


def tapestry_2():
    """K17 - tapestry: crimson with a three-leaf clover and crossed swords."""
    def d(f, W, H):
        for k, (dx, dz) in enumerate(((0, 1.0), (-0.9, 0), (0.9, 0))):
            cyl(nm('lf'), 1.0, 0.05, loc=f.p(dx, -0.04, H * 0.6 + dz), key='fabric_green', verts=14, rot=(90, 0, 0))
        lbox(f, (0.25, 0.05, 2.2), 0, -0.04, H * 0.6 - 1.6, 'fabric_green')
        for s in (-1, 1):
            beam3(f.p(s * 2.2, -0.08, H * 0.2), f.p(-s * 2.2, -0.08, H * 0.42), 0.25, 0.04, 'steel')
            beam3(f.p(s * 1.7, -0.1, H * 0.25 - 0.2), f.p(s * 2.3, -0.1, H * 0.25 + 0.5), 0.2, 0.05, 'gold')
    return tapestry('tapestry_2', 'fabric_red', 'gold', d)


def grand_staircase():
    """K18 - grand staircase: 20 wide, rising 12 over 18 runs, carpeted, marble balustrades and newel posts."""
    reset()
    n, rise, run, W = 18, 12.0 / 18, 1.3, 20.0
    for i in range(n):
        z = rise * (i + 1)
        y = run * i
        box(nm('s'), (W, run + 0.05, z), loc=(0, y + run / 2, z / 2), key='marble' if i % 2 else KT)
        box(nm('nos'), (W - 6.0, 0.25, 0.1), loc=(0, y + 0.1, z + 0.05), key='gold')
        box(nm('cp'), (W - 6.4, run, 0.06), loc=(0, y + run / 2 + 0.12, z + 0.03), key='carpet')
    box(nm('land'), (W, 6.0, 12.0), loc=(0, n * run + 3.0, 6.0), key='marble')
    box(nm('landc'), (W - 6.4, 6.0, 0.06), loc=(0, n * run + 3.0, 12.03), key='carpet')
    for s in (-1, 1):
        x = s * (W / 2 - 0.6)
        lslab(F(), [(x - 0.6, 0, 0), (x - 0.6, n * run, 12.0), (x - 0.6, n * run + 6, 12.0), (x - 0.6, n * run + 6, 0)], (1.2, 0, 0), KT)
        for i in range(0, n, 1):
            y = run * (i + 0.5)
            z = rise * (i + 1)
            lathe(nm('bal'), [(0, 0), (0.26, 0), (0.18, 0.4), (0.34, 1.2), (0.16, 2.0), (0.26, 2.4), (0, 2.4)], loc=(x, y, z), key=KT, segs=8)
        beam3((x, -0.5, rise + 2.6), (x, n * run, 12.0 + 2.6), 0.8, 0.5, 'marble')
        for (y, z) in ((-0.6, 0.0), (n * run, 12.0)):
            box(nm('nw'), (1.6, 1.6, 3.8), loc=(x, y, z + 1.9), key='marble', bev=0.08)
            box(nm('nwc'), (1.9, 1.9, 0.35), loc=(x, y, z + 3.95), key='gold', bev=0.05)
            ball(nm('nwb'), 0.55, loc=(x, y, z + 4.6), key='gold', segs=10, rings=7)
    return finalize('grand_staircase', smooth_angle=25)


def royal_desk():
    """K19 - royal desk: carved dark wood with gold trim, papers, a quill in an inkwell and books."""
    reset()
    rnd = random.Random(19)
    W, D, H = 8.0, 3.6, 3.0
    box(nm('top'), (W, D, 0.3), loc=(0, 0, H), key='wood_dark', bev=0.08)
    box(nm('tt'), (W - 0.6, D - 0.6, 0.04), loc=(0, 0, H + 0.17), key='fabric_green')
    for s in (-1, 1):
        box(nm('ped'), (2.4, D - 0.3, H - 0.3), loc=(s * (W / 2 - 1.3), 0, (H - 0.3) / 2 + 0.15), key='wood_dark', bev=0.05)
        for k in range(3):
            lbox(F(0, -D / 2 + 0.1, 0, 0), (2.0, 0.08, 0.7), s * (W / 2 - 1.3), -0.04, 0.6 + k * 0.85, 'wood')
            ball(nm('kn'), 0.1, loc=(s * (W / 2 - 1.3), -D / 2 - 0.08, 0.6 + k * 0.85), key='gold', segs=6, rings=4)
        box(nm('ft'), (2.6, D - 0.1, 0.3), loc=(s * (W / 2 - 1.3), 0, 0.15), key='gold', bev=0.04)
    box(nm('ap'), (W - 5.2, 0.15, 0.6), loc=(0, -D / 2 + 0.2, H - 0.45), key='wood')
    lbox(F(0, -D / 2 + 0.1, 0, 0), (W, 0.1, 0.12), 0, -0.05, H - 0.1, 'gold')
    for i in range(5):
        box(nm('pp'), (0.9, 1.2, 0.02), loc=(-1.5 + rnd.uniform(-0.3, 0.3), rnd.uniform(-0.6, 0.4), H + 0.2 + i * 0.02), key='paper', rot=(0, 0, rnd.uniform(-15, 15)))
    lathe(nm('ink'), [(0, 0), (0.3, 0), (0.3, 0.3), (0.12, 0.4), (0.12, 0.5), (0, 0.5)], loc=(1.2, 0.6, H + 0.15), key='iron_dark', segs=10)
    tube(nm('quill'), [(1.2, 0.6, H + 0.5), (1.4, 0.7, H + 1.4), (1.7, 0.85, H + 2.2)], 0.05, 'fabric_cream', res=4, taper=[0.5, 2.5, 1.0])
    for k in range(4):
        box(nm('bk'), (0.9, 1.3, 0.25), loc=(3.0, 0.5, H + 0.28 + k * 0.26), key=random.Random(k).choice(['book_a', 'book_b', 'book_c', 'book_d']), rot=(0, 0, rnd.uniform(-10, 10)))
    lathe(nm('cs'), [(0, 0), (0.35, 0), (0.1, 0.2), (0.08, 0.8), (0.25, 0.9), (0, 0.95)], loc=(-3.2, 0.9, H + 0.15), key='gold', segs=8)
    cyl(nm('cd'), 0.1, 0.6, loc=(-3.2, 0.9, H + 1.05), key='wax', verts=8)
    flame(nm('fl'), (-3.2, 0.9, H + 1.65), h=0.35, r=0.1, tongues=0)
    return finalize('royal_desk', smooth_angle=30)


def bookshelf():
    """K20 - tall bookshelf (8 wide, 12 tall) packed with varied books, scrolls and a small globe."""
    reset()
    rnd = random.Random(20)
    W, D, H = 8.0, 2.0, 12.0
    for s in (-1, 1):
        box(nm('sd'), (0.4, D, H), loc=(s * (W / 2 - 0.2), 0, H / 2), key='wood_dark')
    box(nm('bk'), (W, 0.2, H), loc=(0, D / 2 - 0.1, H / 2), key='wood')
    box(nm('cr'), (W + 0.6, D + 0.4, 0.6), loc=(0, -0.1, H + 0.3), key='wood_dark', bev=0.08)
    box(nm('pl'), (W + 0.3, D + 0.2, 0.6), loc=(0, 0, 0.3), key='wood_dark', bev=0.05)
    keys = ['book_a', 'book_b', 'book_c', 'book_d', 'fabric_red', 'wood_light']
    shelves = 5
    for k in range(shelves):
        z = 0.6 + k * (H - 0.6) / shelves
        box(nm('sh'), (W - 0.8, D - 0.2, 0.2), loc=(0, 0, z), key='wood')
        x = -W / 2 + 0.5
        while x < W / 2 - 0.7:
            t = rnd.uniform(0.25, 0.5)
            hh = rnd.uniform(1.2, 1.9)
            if rnd.random() < 0.08:
                for q in range(3):
                    cyl(nm('sc'), 0.15, 1.4, loc=(x + 0.2, -0.2 + q * 0.3, z + 0.25), key='paper', verts=8, rot=(0, 90, 0)) if False else \
                        cyl(nm('sc'), 0.16, 1.1, loc=(x + 0.1, 0.45, z + 0.26 + q * 0.33), key='paper', verts=8, rot=(90, 0, 0))
                x += 0.5
                continue
            lean = rnd.uniform(-8, 8) if rnd.random() < 0.15 else 0
            box(nm('b'), (t, D - 0.6, hh), loc=(x + t / 2, -0.1, z + 0.1 + hh / 2), key=rnd.choice(keys), rot=(0, lean, 0))
            box(nm('bb'), (t + 0.02, 0.05, 0.1), loc=(x + t / 2, -D / 2 + 0.18, z + 0.1 + hh * 0.75), key='gold')
            x += t + 0.03
    ball(nm('gl'), 0.6, loc=(W / 2 - 1.2, -0.2, H + 1.4), key='fabric_blue', segs=12, rings=8)
    torus(nm('glr'), 0.7, 0.05, loc=(W / 2 - 1.2, -0.2, H + 1.4), key='brass', segs=16, rsegs=4, rot=(90, 20, 0))
    cyl(nm('gls'), 0.4, 0.2, loc=(W / 2 - 1.2, -0.2, H + 0.6), key='brass', verts=10)
    return finalize('bookshelf', smooth_angle=30)


def magic_orb():
    """K21 - glowing magic orb on a carved marble pedestal with gold claws."""
    reset()
    lathe(nm('p'), [(0, 0), (1.8, 0), (1.8, 0.5), (1.3, 0.8), (0.8, 1.2), (0.65, 3.4), (1.0, 3.8), (1.4, 4.2), (1.4, 4.5), (0, 4.5)], key='marble', segs=16)
    torus(nm('pr'), 0.7, 0.12, loc=(0, 0, 2.3), key='gold', segs=16, rsegs=4)
    for i in range(4):
        a = 2 * math.pi * i / 4
        tube(nm('cl'), [(math.cos(a) * 0.9, math.sin(a) * 0.9, 4.5), (math.cos(a) * 1.25, math.sin(a) * 1.25, 5.2), (math.cos(a) * 0.9, math.sin(a) * 0.9, 6.1)], 0.12, 'gold', res=4,
             taper=[1, 0.8, 0.3])
    ball(nm('orb'), 1.2, loc=(0, 0, 5.5), key='magic', segs=16, rings=12)
    for k in range(3):
        torus(nm('rg'), 1.7 + k * 0.25, 0.05, loc=(0, 0, 5.5), key='magic_purple', segs=24, rsegs=3, rot=(30 + k * 50, k * 40, 0))
    return finalize('magic_orb', smooth_angle=35)


def candelabra():
    """K22 - standing gold candelabra, five arms, 8 tall."""
    reset()
    lathe(nm('b'), [(0, 0), (1.3, 0), (1.2, 0.2), (0.6, 0.5), (0.2, 0.9), (0.15, 6.0), (0.3, 6.2), (0, 6.3)], key='gold', segs=14)
    for i in range(3):
        a = 2 * math.pi * i / 3
        tube(nm('ft'), [(0, 0, 0.6), (math.cos(a) * 1.0, math.sin(a) * 1.0, 0.3), (math.cos(a) * 1.4, math.sin(a) * 1.4, 0.05)], 0.1, 'gold', res=4)
    for zz in (2.0, 4.0):
        ball(nm('kn'), 0.28, loc=(0, 0, zz), key='gold', segs=10, rings=6)
    for k, x in enumerate((-1.6, -0.8, 0, 0.8, 1.6)):
        z = 7.0 + (0.6 if x == 0 else (0.3 if abs(x) < 1 else 0))
        if x:
            tube(nm('arm'), [(0, 0, 6.2), (x * 0.6, 0, 6.0), (x, 0, z - 0.4)], 0.08, 'gold', res=4)
        lathe(nm('cup'), [(0, 0), (0.12, 0), (0.3, 0.3), (0.32, 0.4), (0, 0.4)], loc=(x, 0, z - 0.4), key='gold', segs=8)
        cyl(nm('cd'), 0.13, 1.0, loc=(x, 0, z), key='wax', verts=8)
        flame(nm('fl'), (x, 0, z + 1.0), h=0.45, r=0.12, tongues=0, seed=k)
    return finalize('candelabra', smooth_angle=35)


ITEMS_THRONE = [
    ('K11_throne', throne), ('K12_throne_pillar', throne_pillar), ('K13_chandelier', chandelier), ('K14_red_carpet', red_carpet),
    ('K15_stained_window', stained_window), ('K16_tapestry_1', tapestry_1), ('K17_tapestry_2', tapestry_2),
    ('K18_grand_staircase', grand_staircase), ('K19_royal_desk', royal_desk), ('K20_bookshelf', bookshelf),
    ('K21_magic_orb', magic_orb), ('K22_candelabra', candelabra),
]


# ============================================================ royal grounds
from nature import blob


def robed_figure(Z, key='marble', accent='gold', hand_item='orb', crown=True, s=1.0):
    """Robed mage figure (original design) standing at height Z, about 10*s tall."""
    lathe(nm('rb'), [(0.0, Z), (1.9 * s, Z), (1.75 * s, Z + 1.0 * s), (1.35 * s, Z + 4.0 * s), (1.15 * s, Z + 6.0 * s), (1.35 * s, Z + 7.2 * s), (0.9 * s, Z + 7.9 * s), (0.0, Z + 8.0 * s)],
          key=key, segs=18, sy=0.82)
    for k in range(8):
        a = 2 * math.pi * k / 8
        tube(nm('fd'), [(math.cos(a) * 1.85 * s, math.sin(a) * 1.5 * s, Z + 0.1), (math.cos(a) * 1.3 * s, math.sin(a) * 1.05 * s, Z + 4.2 * s)], 0.14 * s, key, res=4,
             taper=[1.0, 0.4])
    from props import cloth
    cloth(nm('mn'), 3.4 * s, 7.2 * s, (0, 1.05 * s, Z + 7.6 * s), key, waves=1.4, amp=0.22 * s, seed=7)
    torus(nm('bl'), 1.18 * s, 0.12 * s, loc=(0, 0, Z + 5.4 * s), key=accent, segs=18, rsegs=4, rot=(0, 0, 0))
    lbox(F(0, -1.0 * s, 0, 0), (0.5 * s, 0.1, 5.2 * s), 0, -0.02, Z + 2.8 * s, accent)
    for sx in (-1, 1):
        ball(nm('sh'), 0.6 * s, loc=(sx * 1.15 * s, 0, Z + 7.5 * s), key=key, segs=10, rings=7, scale=(1, 0.9, 0.75))
    tube(nm('ra'), [(1.2 * s, 0, Z + 7.3 * s), (1.6 * s, -0.5 * s, Z + 6.3 * s), (1.5 * s, -1.2 * s, Z + 6.9 * s)], 0.32 * s, key, res=6, taper=[1.0, 1.1, 1.3])
    tube(nm('la'), [(-1.2 * s, 0, Z + 7.3 * s), (-1.7 * s, -0.3 * s, Z + 8.0 * s), (-1.6 * s, -0.4 * s, Z + 9.4 * s)], 0.3 * s, key, res=6, taper=[1.0, 1.0, 1.2])
    cyl(nm('nk'), 0.32 * s, 0.4 * s, loc=(0, 0, Z + 7.9 * s), key=key, verts=10)
    ball(nm('hd'), 0.62 * s, loc=(0, -0.05 * s, Z + 8.75 * s), key=key, segs=12, rings=8, scale=(1, 1, 1.1))
    ball(nm('br'), 0.45 * s, loc=(0, -0.42 * s, Z + 8.2 * s), key=key, segs=8, rings=6, scale=(1, 0.6, 1.2))
    if crown:
        lathe(nm('cr'), [(0.0, 0.0), (0.62 * s, 0.0), (0.66 * s, 0.35 * s), (0.0, 0.35 * s)], loc=(0, -0.05 * s, Z + 9.2 * s), key=accent, segs=14)
        for k in range(4):
            a = 2 * math.pi * k / 4 + math.pi / 4
            lathe(nm('cp'), [(0, 0), (0.15 * s, 0), (0, 0.6 * s)], loc=(math.cos(a) * 0.55 * s, -0.05 * s + math.sin(a) * 0.55 * s, Z + 9.5 * s), key=accent, segs=4)
        lslab(F(0, -0.66 * s, Z + 9.9 * s, 0), [(px * 0.35 * s, 0, pz * 0.35 * s) for px, pz in star_pts(0.6, 1.4, 4)], (0, -0.08, 0), accent)
    if hand_item == 'orb':
        ball(nm('orb'), 0.6 * s, loc=(-1.6 * s, -0.4 * s, Z + 10.1 * s), key='magic', segs=12, rings=8)
    else:
        box(nm('gm'), (1.6 * s, 0.5 * s, 2.0 * s), loc=(1.5 * s, -1.5 * s, Z + 7.0 * s), key='fabric_red', rot=(20, 0, 0), bev=0.05)
        lslab(F(1.5 * s, -1.78 * s, Z + 7.0 * s, 0), [(px * 0.3 * s, 0, pz * 0.3 * s) for px, pz in star_pts(0.6, 1.4, 4)], (0, -0.06, 0), 'gold')
        cyl(nm('stf'), 0.12 * s, 13.0 * s, loc=(-1.7 * s, -0.4 * s, Z), key='wood_dark', verts=8)
        crystal(-1.7 * s, -0.4 * s, Z + 13.0 * s, 1.6 * s, 0.4 * s, key='magic')


def royal_fountain():
    """K23 - royal fountain: round basin, carved column and a statue of a mage holding up a glowing orb, water from four spouts."""
    reset()
    R = 10.0
    lathe(nm('st'), [(0.0, 0.0), (R + 1.8, 0.0), (R + 1.8, 0.6), (0.0, 0.6)], key=KD, segs=32)
    lathe(nm('bs'), [(0.0, 0.6), (R, 0.6), (R, 1.0), (R + 0.4, 1.2), (R + 0.4, 2.6), (R + 0.8, 3.0), (R + 0.8, 3.4), (R - 0.8, 3.4), (R - 0.8, 1.3), (0.0, 1.3)],
          key='marble', segs=32)
    cyl(nm('pool'), R - 0.8, 0.05, loc=(0, 0, 2.8), key='water', verts=32)
    lathe(nm('col'), [(0.0, 1.3), (3.0, 1.3), (2.6, 2.4), (2.0, 3.0), (1.8, 7.0), (2.4, 7.6), (2.6, 8.2), (0.0, 8.2)], key=KT, segs=20)
    for k in range(4):
        a = 2 * math.pi * k / 4 + math.pi / 4
        lathe(nm('spt'), [(0, 0), (0.4, 0), (0.25, 0.9), (0, 1.0)], loc=(math.cos(a) * 2.2, math.sin(a) * 2.2, 5.6), key='gold', segs=8,
              rot=(math.degrees(-math.sin(a)) * 1.2, math.degrees(math.cos(a)) * 1.2, 0))
        stream((math.cos(a) * 2.7, math.sin(a) * 2.7, 6.1), (math.cos(a) * 6.5, math.sin(a) * 6.5, 2.8))
        for j in range(3):
            torus(nm('rp'), 0.4 + j * 0.45, 0.04, loc=(math.cos(a) * 6.5, math.sin(a) * 6.5, 2.85), key='foam', segs=14, rsegs=3)
    robed_figure(8.2, key='marble', accent='gold', hand_item='orb', s=0.9)
    for k in range(10):
        a = 2 * math.pi * k / 10
        cyl(nm('lp'), 0.6, 0.04, loc=(math.cos(a) * 7.8, math.sin(a) * 7.8, 2.85), key='leaf', verts=10)
    return finalize('royal_fountain', smooth_angle=35)


def stream(p0, p1, r=0.16):
    m = ((p0[0] * 0.4 + p1[0] * 0.6), (p0[1] * 0.4 + p1[1] * 0.6), p0[2] + 0.3)
    tube(nm('ws'), [p0, m, p1], r, 'water_fx', res=6, taper=[1.0, 0.9, 0.6])


def wizard_king_statue():
    """K24 - statue of a past Wizard King (original): crowned robed mage with grimoire and crystal staff, bronze on marble."""
    reset()
    from capital import plinth
    plinth(6.0, w=6.0)
    robed_figure(6.0, key='bronze', accent='gold', hand_item='book', s=1.0)
    return finalize('wizard_king_statue', smooth_angle=35)


def pot(r=1.6, h=2.0, key='terracotta'):
    lathe(nm('pt'), [(0.0, 0.0), (r * 0.75, 0.0), (r * 0.85, 0.2), (r, h * 0.85), (r * 1.1, h * 0.88), (r * 1.1, h), (r * 0.9, h), (0.0, h - 0.2)], key=key, segs=16)
    cyl(nm('soil'), r * 0.92, 0.05, loc=(0, 0, h - 0.15), key='dirt', verts=16)


def topiary_ball():
    """K25 - topiary: two clipped balls on a trunk in a stone pot."""
    reset()
    pot(1.8, 2.2, KT)
    cyl(nm('tr'), 0.22, 6.8, loc=(0, 0, 2.0), key='bark', verts=8)
    blob(nm('b1'), 2.4, (0, 0, 6.4), 'leaf_dark', subdiv=3, amp=0.06, freq=3.0, seed=1, detail=0.05)
    blob(nm('b2'), 1.4, (0, 0, 9.2), 'leaf_dark', subdiv=3, amp=0.07, freq=3.0, seed=2, detail=0.05)
    return finalize('topiary_ball', smooth_angle=60)


def topiary_cone():
    """K26 - topiary: tall clipped cone in a stone pot."""
    reset()
    pot(2.0, 2.2, KT)
    o = blob(nm('c'), 2.2, (0, 0, 2.3), 'leaf_dark', subdiv=3, amp=0.05, freq=3.0, seed=3, detail=0.04)
    import bmesh as _bm
    me = o.data
    for v in me.vertices:
        z = v.co.z + 2.2
        t = max(0.0, min(1.0, z / 4.4))
        v.co.x *= (1.0 - t * 0.92) * 1.0
        v.co.y *= (1.0 - t * 0.92) * 1.0
        v.co.z = (z / 4.4) * 9.0 - 2.2 + 0.0
    o.location.z = 2.3 + 2.2 - 2.2
    return finalize('topiary_cone', smooth_angle=60)


def topiary_spiral():
    """K27 - topiary: spiral clipped around a cone, in a stone pot."""
    reset()
    pot(2.0, 2.2, KT)
    cyl(nm('tr'), 0.25, 11.0, loc=(0, 0, 2.0), key='bark', verts=8)
    n = 26
    for i in range(n):
        t = i / (n - 1)
        a = t * 3.2 * 2 * math.pi
        r = 1.9 * (1 - t * 0.85)
        blob(nm('s'), 1.15 * (1 - t * 0.6), (math.cos(a) * r * 0.55, math.sin(a) * r * 0.55, 3.0 + t * 8.5), 'leaf_dark', subdiv=2, amp=0.08, freq=2.5, seed=i,
             scale=(1.3, 1.3, 0.9))
    return finalize('topiary_spiral', smooth_angle=60)


def hedge_mass(x0, x1, y, t, h, seed, axis='x'):
    from nature import _hedge_block
    rnd = random.Random(seed)
    L = x1 - x0
    if axis == 'x':
        _hedge_block(nm('hg'), (L, t, h), ((x0 + x1) / 2, y, h / 2), rnd)
    else:
        _hedge_block(nm('hg'), (t, L, h), (y, (x0 + x1) / 2, h / 2), rnd)
    for i in range(int(L / 4)):
        cyl(nm('tr'), 0.3, 1.0, loc=((x0 + 2 + i * 4) if axis == 'x' else y, y if axis == 'x' else (x0 + 2 + i * 4), 0), key='bark', verts=6)


def maze_hedge_straight():
    """K28 - tall maze hedge, straight, 16 long x 9 tall x 3 thick."""
    reset()
    hedge_mass(-8.0, 8.0, 0, 3.0, 9.0, 28)
    return finalize('maze_hedge_straight', smooth_angle=45)


def maze_hedge_corner():
    """K29 - tall maze hedge corner, two 10.5-long arms."""
    reset()
    hedge_mass(-1.5, 9.0, 0, 3.0, 9.0, 29)
    hedge_mass(1.5, 9.0, 0, 3.0, 9.0, 30, axis='y')
    return finalize('maze_hedge_corner', smooth_angle=45)


def gazebo():
    """K30 - octagonal garden gazebo: marble columns, ironwork railing, blue-and-gold domed roof, steps."""
    reset()
    R = 8.0
    lathe(nm('pl'), [(0.0, 0.0), (R + 0.6, 0.0), (R + 0.6, 1.6), (0.0, 1.6)], key=KT, segs=8)
    lathe(nm('plc'), [(0.0, 1.6), (R + 0.9, 1.6), (R + 0.9, 1.9), (0.0, 1.9)], key='marble', segs=8)
    for k in range(3):
        box(nm('st'), (5.0, 1.2, 0.55), loc=(0, -R - 1.0 - (2 - k) * 1.1 + 0.6, 0.27 + k * 0.53), key='marble' if k % 2 else KT)
    for i in range(8):
        a = 2 * math.pi * i / 8 + math.pi / 8
        x, y = math.cos(a) * (R - 0.4), math.sin(a) * (R - 0.4)
        column_c(x, y, 1.9, 11.0, 0.45, key='marble', base='gold')
        a2 = 2 * math.pi * (i + 1) / 8 + math.pi / 8
        x2, y2 = math.cos(a2) * (R - 0.4), math.sin(a2) * (R - 0.4)
        if i != 5:
            mid = ((x + x2) / 2, (y + y2) / 2)
            ang = math.degrees(math.atan2(y2 - y, x2 - x))
            fr = F(mid[0], mid[1], 1.9, ang)
            Lr = math.hypot(x2 - x, y2 - y) - 1.0
            railing(fr, -Lr / 2, Lr / 2, 0.0, y=0, h=2.6, key='iron', step=0.5)
            for k in range(3):
                torus(nm('rs'), 0.45, 0.05, loc=fr.p(-Lr / 3 + k * Lr / 3, 0, 1.5), key='iron', segs=12, rsegs=3, rot=fr.r(90, 0, 0))
        tube(nm('ar'), [(x, y, 12.6), ((x + x2) / 2 * 1.02, (y + y2) / 2 * 1.02, 11.6), (x2, y2, 12.6)], 0.22, 'gold', res=4)
    lathe(nm('ring'), [(0.0, 12.9), (R + 0.4, 12.9), (R + 0.4, 13.9), (0.0, 13.9)], key='marble', segs=8)
    lathe(nm('ring2'), [(0.0, 13.9), (R + 0.8, 13.9), (R + 0.8, 14.3), (0.0, 14.3)], key='gold', segs=8)
    lathe(nm('rf'), [(0.0, 14.3), (R + 1.4, 14.3), (R + 0.6, 15.0), (R - 1.0, 17.0), (R * 0.55, 19.4), (2.0, 21.0), (0.6, 21.8), (0.0, 22.0)], key='tile_a', segs=8)
    for i in range(8):
        a = 2 * math.pi * i / 8 + math.pi / 8
        pts = [(math.cos(a) * rr, math.sin(a) * rr, zz) for rr, zz in ((R + 1.45, 14.35), (R + 0.65, 15.05), (R - 0.95, 17.05), (R * 0.56, 19.45), (2.05, 21.05))]
        tube(nm('rib'), pts, 0.14, 'gold', res=4)
    lathe(nm('fn'), [(0, 0), (0.5, 0), (0.3, 0.6), (0.6, 1.2), (0.12, 1.8), (0.1, 3.0), (0, 3.4)], loc=(0, 0, 21.8), key='gold', segs=8)
    ball(nm('fb'), 0.45, loc=(0, 0, 23.5), key='magic', segs=10, rings=7)
    box(nm('flr'), (R * 1.4, R * 1.4, 0.05), loc=(0, 0, 1.92), key='marble', rot=(0, 0, 0))
    return finalize('gazebo', smooth_angle=30)


def rose_arch():
    """K31 - iron garden arch overgrown with climbing roses, 8 wide x 11 tall."""
    reset()
    rnd = random.Random(31)
    W, H, D = 8.0, 11.0, 2.0
    for y in (-D / 2, D / 2):
        for s in (-1, 1):
            cyl(nm('p'), 0.12, 7.0, loc=(s * W / 2, y, 0), key='iron', verts=8)
        tube(nm('ar'), [(-W / 2, y, 7.0), (-W / 2 + 0.6, y, 9.3), (0, y, H), (W / 2 - 0.6, y, 9.3), (W / 2, y, 7.0)], 0.12, 'iron', res=4)
    for k in range(9):
        a = math.pi * k / 8
        x, z = -math.cos(a) * W / 2, 7.0 + math.sin(a) * 4.0
        tube(nm('rg'), [(x, -D / 2, z), (x, D / 2, z)], 0.07, 'iron', res=4)
    for s in (-1, 1):
        for zz in (1.5, 3.5, 5.5):
            tube(nm('rh'), [(s * W / 2, -D / 2, zz), (s * W / 2, D / 2, zz)], 0.07, 'iron', res=4)
    for i in range(120):
        t = rnd.random()
        if t < 0.35:
            s = rnd.choice((-1, 1)); x = s * W / 2; z = rnd.uniform(0.6, 7.0)
        else:
            a = math.pi * (t - 0.35) / 0.65
            x, z = -math.cos(a) * W / 2, 7.0 + math.sin(a) * 4.0
        y = rnd.uniform(-D / 2 - 0.2, D / 2 + 0.2)
        ball(nm('lv'), rnd.uniform(0.32, 0.45), loc=(x + rnd.uniform(-0.35, 0.35), y, z + rnd.uniform(-0.2, 0.2)), key=rnd.choice(['leaf_dark', 'leaf', 'leaf_dark']),
             segs=7, rings=5, scale=(1.0, rnd.uniform(0.6, 1.0), 0.8))
        if rnd.random() < 0.4:
            ball(nm('rs'), rnd.uniform(0.2, 0.3), loc=(x + rnd.uniform(-0.5, 0.5), y + rnd.choice((-0.55, 0.55)), z + rnd.uniform(-0.3, 0.3)),
                 key=rnd.choice(['fl_red', 'fl_pink', 'fl_red', 'fl_white']), segs=7, rings=5)
    return finalize('rose_arch', smooth_angle=40)


def ornate_planter():
    """K32 - ornate stone urn planter on a square base, gold band, overflowing with flowers."""
    reset()
    rnd = random.Random(32)
    box(nm('b'), (3.2, 3.2, 1.6), loc=(0, 0, 0.8), key=KT, bev=0.08)
    box(nm('bc'), (3.6, 3.6, 0.3), loc=(0, 0, 1.75), key='marble', bev=0.05)
    lathe(nm('u'), [(0.0, 1.9), (0.9, 1.9), (0.5, 2.5), (0.6, 2.9), (1.8, 3.6), (2.2, 4.6), (2.4, 4.9), (2.0, 4.9), (0.0, 4.6)], key='marble', segs=20)
    torus(nm('gb'), 2.15, 0.1, loc=(0, 0, 4.5), key='gold', segs=24, rsegs=4)
    for i in range(26):
        a = rnd.uniform(0, 6.28); r = rnd.uniform(0, 1.8)
        blob(nm('lf'), rnd.uniform(0.4, 0.55), (math.cos(a) * r, math.sin(a) * r, 4.9 + rnd.uniform(0, 0.5)), rnd.choice(['leaf', 'leaf_dark']), subdiv=2, amp=0.12, seed=i)
    for i in range(18):
        a = rnd.uniform(0, 6.28); r = rnd.uniform(0, 1.9)
        ball(nm('fl'), rnd.uniform(0.2, 0.3), loc=(math.cos(a) * r, math.sin(a) * r, 5.3 + rnd.uniform(0, 0.6)), key=rnd.choice(['fl_purple', 'fl_white', 'fl_pink', 'fl_yellow']), segs=7, rings=5)
    for i in range(6):
        a = 2 * math.pi * i / 6
        tube(nm('tr'), [(math.cos(a) * 2.2, math.sin(a) * 2.2, 4.9), (math.cos(a) * 2.6, math.sin(a) * 2.6, 4.5), (math.cos(a) * 2.55, math.sin(a) * 2.55, 4.0)], 0.06, 'leaf', res=4)
        for q in range(3):
            ball(nm('tl'), 0.22, loc=(math.cos(a) * 2.55, math.sin(a) * 2.55, 4.0 + q * 0.35), key='leaf_dark', segs=6, rings=4, scale=(1, 0.6, 1))
    return finalize('ornate_planter', smooth_angle=40)


def ornate_bench():
    """K33 - ornate garden bench: marble seat and back on gold-scrolled iron frame, 8 wide."""
    reset()
    W = 8.0
    for k in range(4):
        box(nm('sl'), (W, 0.4, 0.18), loc=(0, -0.7 + k * 0.45, 1.95), key='wood_dark', bev=0.04)
    for k in range(3):
        box(nm('bk'), (W, 0.16, 0.4), loc=(0, 0.95 + k * 0.05, 2.6 + k * 0.6), key='wood_dark', rot=(-12, 0, 0), bev=0.04)
    for x in (-W / 2 + 0.4, 0.0, W / 2 - 0.4):
        lbeam(F(), (x, -0.8, 0.0), (x, -0.6, 1.85), 0.16, 'iron')
        lbeam(F(), (x, 0.9, 0.0), (x, 1.2, 4.2), 0.16, 'iron')
        lbeam(F(), (x, -0.8, 1.85), (x, 1.0, 1.85), 0.16, 'iron')
        if abs(x) > 1:
            tube(nm('am'), [(x, -1.0, 1.9), (x, -0.9, 3.0), (x, 0.0, 3.1), (x, 0.9, 3.2)], 0.1, 'iron', res=4)
            from kitlib import scroll
            scroll(nm('sc'), (x, -0.95, 2.6), 0.05, 0.42, 1.6, plane='YZ', key='gold', radius=0.06)
            scroll(nm('sc'), (x, 0.0, 1.0), 0.05, 0.5, 1.4, plane='YZ', key='gold', radius=0.06)
    lathe(nm('cr'), [(0, 0), (0.3, 0), (0.15, 0.4), (0, 0.6)], loc=(0, 1.3, 4.3), key='gold', segs=8)
    return finalize('ornate_bench', smooth_angle=30)


def ornate_lamp():
    """K34 - ornate royal lamp post: black fluted post, gold trims, three glowing lanterns, 17 tall."""
    reset()
    lathe(nm('b'), [(0, 0), (1.3, 0), (1.3, 0.5), (1.0, 0.8), (0.9, 2.2), (0.5, 2.6), (0.35, 3.0), (0.0, 3.0)], key='iron_dark', segs=8)
    torus(nm('g1'), 0.95, 0.08, loc=(0, 0, 2.3), key='gold', segs=16, rsegs=4)
    lathe(nm('s'), [(0, 3.0), (0.32, 3.0), (0.22, 12.6), (0, 12.6)], key='iron_dark', segs=8)
    for zz in (6.0, 12.4):
        torus(nm('g'), 0.3, 0.08, loc=(0, 0, zz), key='gold', segs=12, rsegs=4)
    for k in range(3):
        a = 2 * math.pi * k / 3
        x, y = math.cos(a) * 2.2, math.sin(a) * 2.2
        tube(nm('arm'), [(0, 0, 12.0), (x * 0.5, y * 0.5, 13.0), (x, y, 12.8)], 0.1, 'iron_dark', res=4)
        from kitlib import scroll
        tube(nm('arm2'), [(math.cos(a) * 0.2, math.sin(a) * 0.2, 11.0), (x * 0.4, y * 0.4, 11.4), (x * 0.7, y * 0.7, 12.4)], 0.06, 'gold', res=4)
        lathe(nm('lb'), [(0, 0), (0.25, 0), (0.42, 0.25), (0, 0.25)], loc=(x, y, 11.0), key='iron_dark', segs=6)
        lathe(nm('lg'), [(0, 0.25), (0.45, 0.25), (0.55, 1.5), (0, 1.5)], loc=(x, y, 11.0), key='glass_lit', segs=6)
        lathe(nm('lc'), [(0, 1.5), (0.75, 1.5), (0.2, 2.1), (0, 2.4)], loc=(x, y, 11.0), key='iron_dark', segs=6)
        ball(nm('lf'), 0.12, loc=(x, y, 13.45), key='gold', segs=6, rings=4)
    lathe(nm('top'), [(0, 0), (0.35, 0), (0.15, 0.8), (0.3, 1.2), (0, 1.8)], loc=(0, 0, 12.6), key='gold', segs=8)
    return finalize('ornate_lamp', smooth_angle=35)


def royal_banner():
    """K35 - freestanding royal banner: gold-capped pole with crossbar and blue banner with the Wizard King star."""
    reset()
    from props import cloth
    cyl(nm('b'), 1.4, 0.6, loc=(0, 0, 0), key=KT, verts=12)
    cyl(nm('p'), 0.2, 18.0, loc=(0, 0, 0.6), key='iron_dark', verts=10)
    ball(nm('pb'), 0.45, loc=(0, 0, 18.9), key='gold', segs=10, rings=7)
    lathe(nm('pt'), [(0, 0), (0.25, 0), (0, 1.2)], loc=(0, 0, 19.2), key='gold', segs=6)
    cyl(nm('cb'), 0.12, 5.6, loc=(-2.8, 0, 17.0), key='gold', verts=8, rot=(0, 90, 0))
    for s in (-1, 1):
        ball(nm('cbe'), 0.25, loc=(s * 2.9, 0, 17.0), key='gold', segs=8, rings=6)
    cloth(nm('bn'), 4.6, 11.0, (0, -0.25, 16.9), 'fabric_blue', waves=0.6, amp=0.12, seed=35)
    f = F(0, -0.45, 0, 0)
    for s in (-1, 1):
        lbox(f, (0.35, 0.05, 10.4), s * 2.05, 0, 11.6, 'gold')
    lslab(f.sub(0, 0, 12.0), [(px, 0, pz) for px, pz in star_pts(0.5, 1.5, 4)], (0, -0.05, 0), 'gold')
    lslab(f, [(-2.3, 0, 6.0), (2.3, 0, 6.0), (0, 0, 4.4)], (0, -0.05, 0), 'gold')
    return finalize('royal_banner', smooth_angle=30)


def tower_flag():
    """K36 - tower-top flag: tall pole with a large swallowtail pennant (place on roof finials)."""
    reset()
    from props import cloth
    cyl(nm('p'), 0.18, 14.0, loc=(0, 0, 0), key='iron_dark', verts=10)
    ball(nm('pb'), 0.4, loc=(0, 0, 14.2), key='gold', segs=10, rings=7)
    cloth(nm('fl'), 9.0, 3.6, (4.6, 0, 13.6), 'fabric_blue', waves=1.6, amp=0.45, seed=36)
    lslab(F(9.15, 0, 0, 0), [(0, 0.0, 13.6), (0, 0.0, 10.0), (-1.4, 0.0, 11.8)], (0, 0.06, 0), 'gold')
    lbox(F(0.35, 0, 0, 0), (0.3, 0.3, 3.6), 0, 0, 11.8, 'gold')
    for z in (13.4, 10.2):
        torus(nm('rg'), 0.26, 0.05, loc=(0, 0, z), key='gold', segs=10, rsegs=4)
    return finalize('tower_flag', smooth_angle=30)


ITEMS_GROUNDS = [
    ('K23_royal_fountain', royal_fountain), ('K24_wizard_king_statue', wizard_king_statue), ('K25_topiary_ball', topiary_ball),
    ('K26_topiary_cone', topiary_cone), ('K27_topiary_spiral', topiary_spiral), ('K28_maze_hedge_straight', maze_hedge_straight),
    ('K29_maze_hedge_corner', maze_hedge_corner), ('K30_gazebo', gazebo), ('K31_rose_arch', rose_arch), ('K32_ornate_planter', ornate_planter),
    ('K33_ornate_bench', ornate_bench), ('K34_ornate_lamp', ornate_lamp), ('K35_royal_banner', royal_banner), ('K36_tower_flag', tower_flag),
]


# ============================================================ noble district
def block(cx, cy, w, d, floors, fh=8.0, wall='castle', trim='castle_trim', base='ashlar', rkeys=ROOF, pitch=0.5, dormers=0,
          win='rect', shutter=None, lit=(), seed=0, front_skip=(), quoin=True, chim=True, roof=True, glass='glass_dark', balc=()):
    """Generic stately block with windows on every floor and side; returns top z."""
    H = floors * fh
    box(nm('bl'), (w, d, H), loc=(cx, cy, H / 2), key=wall)
    box(nm('bp'), (w + 0.6, d + 0.6, 1.6), loc=(cx, cy, 0.8), key=base, bev=0.06)
    for k in range(1, floors):
        band(cx, cy, w, d, k * fh - 0.2, 0.5, trim, out=0.2)
    band(cx, cy, w, d, H - 0.6, 0.8, trim, out=0.45)
    rnd = random.Random(seed)
    for side, L in (('front', w), ('back', w), ('left', d), ('right', d)):
        fr = faces(cx, cy, w, d)[side]
        if quoin:
            quoins(F(*fr.p(-L / 2, 0, 0), fr.rz), 1.6, H - 0.8, trim, course=1.2)
        n = max(1, int(L / 5.2))
        for f_ in range(floors):
            for i in range(n):
                x = -L / 2 + L * (i + 0.5) / n
                if side == 'front' and f_ == 0 and i in front_skip:
                    continue
                is_lit = (f_, i) in lit and side == 'front'
                z = f_ * fh + (2.2 if f_ == 0 else 1.6)
                hh = fh - 3.6
                if side == 'front' and (f_, i) in balc:
                    door(fr.sub(0, 0, f_ * fh), x, w=2.4, h=hh + 1.0, arch=(win == 'arch'), key=glass, surround=trim, step=None, studs=False)
                    lbox(fr, (3.8, 1.6, 0.3), x, -0.8, f_ * fh + 0.15, trim)
                    railing(fr, x - 1.8, x + 1.8, f_ * fh + 0.3, y=-1.55, h=1.6, key='iron', step=0.3)
                    for s in (-1, 1):
                        lbox(fr, (0.08, 1.5, 0.1), x + s * 1.8, -0.8, f_ * fh + 1.9, 'iron')
                    continue
                window(fr, x, z, w=2.2, h=hh, arch=(win == 'arch' or (win == 'mixed' and f_ == floors - 1)), frame=trim, sill=trim,
                       lintel=trim if win != 'arch' else None, keystone=trim if win != 'rect' else None, shutter=shutter, lit=is_lit, glass=glass)
    top = H
    if roof:
        hr = d * pitch
        gable_roof(F(cx, cy, 0, 0), w, d, H, hr, keys=rkeys, wall=wall, ov=0.8, ovg=0.6, barge=trim, crest='gold')
        for i in range(dormers):
            x = cx - w / 2 + w * (i + 0.5) / dormers
            yf = cy - d / 2 + 1.8
            dormer(F(), x, yf, roof_z(H, hr, d, yf - cy) - 0.4, w=3.2, h=4.0, depth=4.0 / (hr / (d / 2)) + 1.2, wall=wall, keys=rkeys, frame=trim)
        if chim:
            for s in (-1, 1):
                from arch import chimney
                chimney(cx + s * (w / 2 - 2.0), cy + d * 0.15, H, H + hr + 2.0, key=base if base != 'ashlar' else 'brick')
        top = H + hr
    return top


def mansion_1():
    """K37 - noble mansion: white classical villa, central columned portico with pediment, blue roof with dormers."""
    reset()
    w, d = 34.0, 20.0
    block(0, 0, w, d, 3, wall='castle', trim='castle_trim', rkeys=ROOF, pitch=0.42, dormers=5, win='mixed', lit={(1, 1), (2, 4)}, seed=37,
          front_skip=(2,), balc={(1, 2)})
    fo = faces(0, 0, w, d)['front']
    door(fo, 0, w=3.6, h=7.0, arch=True, surround='castle_trim', step=None, lamp=True)
    for x in (-5.4, -2.0, 2.0, 5.4):
        column_c(x, -d / 2 - 4.0, 1.6, 6.6, 0.55, key='marble', base='castle_trim')
    box(nm('pf'), (13.0, 4.8, 1.6), loc=(0, -d / 2 - 2.2, 0.8), key='ashlar')
    for k in range(3):
        box(nm('ps'), (8.0 - k * 0.6, 1.0, 0.53), loc=(0, -d / 2 - 5.2 - (2 - k) * 1.0, 0.27 + k * 0.53), key='marble' if k % 2 else 'castle_trim')
    box(nm('pent'), (13.0, 4.8, 1.2), loc=(0, -d / 2 - 2.2, 8.8), key='castle_trim')
    railing(F(0, -d / 2 - 4.5, 0, 0), -6.3, 6.3, 9.4, y=0, h=1.6, key='iron', step=0.35)
    pediment(F(0, -d / 2, 0, 0), 0, 24.6, 12.0, 4.8, 1.2, emblem='gold')
    for s in (-1, 1):
        lathe(nm('urn'), [(0, 0), (0.6, 0), (0.4, 0.4), (0.9, 1.2), (0.6, 1.8), (0, 1.9)], loc=(s * (w / 2 - 0.6), -d / 2 + 0.6, 24.8), key='castle_trim', segs=10)
    return finalize('mansion_1', smooth_angle=25)


def mansion_2():
    """K38 - noble mansion: brick and stone chateau, forward wings, round corner towers with tall cones."""
    reset()
    block(0, 2.0, 26.0, 18.0, 3, wall='brick', trim='castle_trim', base='ashlar', rkeys=('tile_grey', 'tile_b'), pitch=0.55, dormers=3, win='arch',
          lit={(0, 1), (2, 3)}, seed=38, front_skip=(2,))
    for s in (-1, 1):
        block(s * 17.0, -4.0, 10.0, 22.0, 3, wall='brick', trim='castle_trim', base='ashlar', rkeys=('tile_grey', 'tile_b'), pitch=0.5,
              win='arch', seed=39 + s, chim=False, lit={(1, 0)}, quoin=False)
        x, y = s * 22.0, -15.0
        lathe(nm('tw'), [(0.0, 0.0), (4.4, 0.0), (4.4, 1.6), (4.0, 1.8), (4.0, 28.0), (0.0, 28.0)], loc=(x, y, 0), key='brick', segs=20)
        for zz in (8.0, 16.0, 23.6):
            lathe(nm('twb'), [(0.0, zz - 0.25), (4.25, zz - 0.25), (4.25, zz + 0.3), (0.0, zz + 0.3)], loc=(x, y, 0), key='castle_trim', segs=20)
        for j in range(3):
            a = math.radians(-90 + (j - 1) * 65)
            fr = F(x + math.cos(a) * 4.0, y + math.sin(a) * 4.0, 0, math.degrees(a) + 90)
            for zz in (2.6, 10.2, 18.0):
                window(fr, 0, zz, w=1.8, h=4.2, arch=True, frame='castle_trim', sill='castle_trim', panes=True, lit=(j == 1 and zz > 15))
        cone_roof(x, y, 28.0, 4.0, 14.0, keys=('tile_grey', 'tile_b'), rings=8, ov=0.7, flag='fabric_green')
    fo = F(0, 2.0 - 9.0, 0, 0)
    door(fo, 0, w=3.8, h=7.4, arch=True, surround='castle_trim', step='marble', lamp=True)
    lbox(fo, (8.0, 3.0, 0.5), 0, -1.5, 8.2, 'castle_trim')
    railing(fo, -3.8, 3.8, 8.45, y=-2.9, h=1.6, key='iron', step=0.3)
    for x in (-3.4, 3.4):
        lbeam(fo, (x, -0.1, 5.6), (x, -2.6, 8.0), 0.5, 'castle_trim')
    return finalize('mansion_2', smooth_angle=25)


def mansion_3():
    """K39 - noble mansion: grand timber-framed manor on a stone base, bay windows, octagonal turret, red roof."""
    reset()
    from capital import house, oriel
    house(w=26.0, d=18.0, floors=3, gh=9.0, fh=8.0, ground='ashlar', ground_trim='castle_trim', upper='plaster_d', timber=True, jetty=0.0,
          rkeys=('tile_red_a', 'tile_red_b'), shutter='shutter_g', flowers=('fl_red', 'fl_white', 'fl_pink'), dormers=3, seed=393,
          lit={(0, 1), (1, 3)}, door_bay=2, pitch=0.5)
    fo = faces(0, 0, 26.0, 18.0, 9.0)['front']
    for x in (-8.0, 8.0):
        oriel(fo, x, 1.0, w=5.2, h=6.0, dep=1.8, wall='plaster_d', keys=('tile_red_a',), lit=(x > 0))
    x, y, r = 13.0 + 2.0, -9.0 - 2.0, 4.0
    lathe(nm('ot'), [(0.0, 0.0), (r + 0.6, 0.0), (r + 0.6, 1.4), (r, 1.6), (r, 31.0), (0.0, 31.0)], loc=(x, y, 0), key='ashlar', segs=8)
    lathe(nm('otu'), [(0.0, 9.0), (r + 0.05, 9.0), (r + 0.05, 31.0), (0.0, 31.0)], loc=(x, y, 0), key='plaster_d', segs=8)
    for zz in (9.0, 17.0, 25.0, 30.8):
        lathe(nm('otb'), [(0.0, zz - 0.25), (r + 0.3, zz - 0.25), (r + 0.3, zz + 0.25), (0.0, zz + 0.25)], loc=(x, y, 0), key='timber', segs=8)
    for j in range(4):
        a = math.radians(-90 + (j - 1.5) * 45)
        fr = F(x + math.cos(a) * r * 0.924, y + math.sin(a) * r * 0.924, 0, math.degrees(a) + 90)
        for zz in (3.0, 11.0, 19.0, 26.5):
            window(fr, 0, zz, w=1.5, h=3.6 if zz < 26 else 2.6, arch=True, frame='wood_paint', sill='wood_paint', panes=False, lit=(j == 1 and zz > 18))
    cone_roof(x, y, 31.0, r, 13.0, keys=('tile_red_a', 'tile_red_b'), rings=7, ov=0.6, segs=8, flag='fabric_red')
    return finalize('mansion_3', smooth_angle=25)


def weapon_rack(x, y, rz=0.0):
    f = F(x, y, 0, rz)
    for s in (-1, 1):
        lbox(f, (0.3, 0.3, 4.2), s * 2.0, 0, 2.1, 'wood_dark')
    for z in (1.0, 3.6):
        lbox(f, (4.4, 0.25, 0.25), 0, 0, z, 'wood')
    for k in range(4):
        xx = -1.5 + k * 1.0
        if k % 2 == 0:
            lbeam(f, (xx, -0.2, 0.2), (xx, -0.25, 5.4), 0.12, 'wood_light')
            lathe(nm('sp'), [(0, 0), (0.16, 0), (0, 0.8)], loc=f.p(xx, -0.25, 5.4), key='steel', segs=4)
        else:
            lbeam(f, (xx, -0.2, 0.5), (xx, -0.25, 3.9), 0.28, 'steel', 0.06)
            lbeam(f, (xx - 0.45, -0.25, 3.9), (xx + 0.45, -0.25, 3.9), 0.14, 'gold')
            lbeam(f, (xx, -0.25, 3.9), (xx, -0.25, 4.7), 0.14, 'wood_dark')


def barracks():
    """K40 - guard barracks: long two-storey stone hall, slit and arched windows, red roof, weapon racks and a target."""
    reset()
    w, d = 40.0, 16.0
    block(0, 0, w, d, 2, fh=9.0, wall='ashlar', trim='castle_trim', base='ashlar_dark', rkeys=('tile_red_a', 'tile_red_b'), pitch=0.45,
          dormers=0, win='arch', shutter='shutter_r', seed=40, front_skip=(3,), lit={(0, 1), (1, 5)}, quoin=True)
    fo = faces(0, 0, w, d)['front']
    door(fo, -w / 2 + w * 3.5 / 7, w=4.0, h=7.4, arch=True, surround='castle_trim', lamp=True)
    lslab(fo.sub(-w / 2 + w * 3.5 / 7, -0.4, 13.0), [(-2.0, 0, 3.2), (2.0, 0, 3.2), (2.0, 0, 0.8), (0, 0, -1.4), (-2.0, 0, 0.8)], (0, -0.3, 0), 'fabric_red')
    lslab(fo.sub(-w / 2 + w * 3.5 / 7, -0.75, 13.3), [(px * 0.8, 0, pz * 0.8) for px, pz in star_pts(0.6, 1.5, 4)], (0, -0.08, 0), 'gold')
    for x in (-12.0, 12.0):
        weapon_rack(x, -d / 2 - 2.5)
    lathe(nm('tg'), [(0, 0), (1.6, 0), (1.6, 0.3), (0, 0.3)], loc=(16.5, -d / 2 - 6.0, 3.0), key='fabric_cream', segs=20, rot=(90, 0, 0))
    for k, (rr, kk) in enumerate(((1.2, 'fabric_red'), (0.8, 'fabric_cream'), (0.4, 'fabric_red'))):
        cyl(nm('tr'), rr, 0.05, loc=(16.5, -d / 2 - 6.05 - 0.01 * k, 3.0), key=kk, verts=20, rot=(90, 0, 0))
    for s in (-1, 1):
        lbeam(F(), (16.5 + s * 1.0, -d / 2 - 5.6, 0), (16.5 + s * 0.6, -d / 2 - 5.75, 3.0), 0.2, 'wood_dark')
    lbeam(F(), (16.5, -d / 2 - 4.6, 0), (16.5, -d / 2 - 5.75, 2.2), 0.2, 'wood_dark')
    return finalize('barracks', smooth_angle=25)


def stable_door(f, x, w=4.0, h=6.0):
    for zz, hh in ((0.0, h * 0.5), (h * 0.5 + 0.05, h * 0.5 - 0.05)):
        lbox(f, (w, 0.2, hh), x, -0.05, zz + hh / 2, 'wood')
        lbeam(f, (x - w / 2 + 0.2, -0.18, zz + 0.2), (x + w / 2 - 0.2, -0.18, zz + hh - 0.2), 0.22, 'wood_dark')
        lbox(f, (w, 0.15, 0.25), x, -0.18, zz + 0.15, 'wood_dark')
        lbox(f, (w, 0.15, 0.25), x, -0.18, zz + hh - 0.15, 'wood_dark')
    for s in (-1, 1):
        lbox(f, (0.45, 0.4, h + 0.5), x + s * (w / 2 + 0.2), -0.15, (h + 0.5) / 2, 'timber')
    lbox(f, (w + 1.0, 0.4, 0.45), x, -0.15, h + 0.4, 'timber')


def stables():
    """K41 - royal stables: timber-framed barn, six half-doors, hay loft with hoist beam, hay bales and a trough."""
    reset()
    w, d, h = 36.0, 16.0, 9.0
    box(nm('st'), (w, d, h), loc=(0, 0, h / 2), key='plaster')
    box(nm('sb'), (w + 0.4, d + 0.4, 1.6), loc=(0, 0, 0.8), key='ashlar', bev=0.05)
    fs = faces(0, 0, w, d)
    for side, L in (('front', w), ('back', w), ('left', d), ('right', d)):
        posts = [-L / 2 + 0.21] + [-L / 2 + L * i / 6 for i in range(1, 6)] + [L / 2 - 0.21] if L > 20 else [-L / 2 + 0.21, 0, L / 2 - 0.21]
        from arch import timber_frame
        timber_frame(fs[side], L, 1.6, h, posts, braces=(side != 'front'))
    for i in range(6):
        stable_door(fs['front'], -w / 2 + w * (i + 0.5) / 6)
    for i in range(6):
        window(fs['back'], -w / 2 + w * (i + 0.5) / 6, 4.0, w=2.0, h=2.4, frame='wood', sill='wood', panes=False)
    hr = 8.0
    gable_roof(F(), w, d, h, hr, keys=('tile_red_a', 'tile_red_b'), wall='plaster', ov=1.4, ovg=1.0)
    fl = F(w / 2, 0, h, 90)
    lbox(fl, (3.4, 0.2, 3.6), 0, -0.05, 1.8, 'wood_dark')
    for k in range(4):
        lbox(fl, (0.1, 0.3, 3.4), -1.2 + k * 0.8, -0.18, 1.8, 'timber')
    lbeam(F(), (w / 2 - 1.0, 0, h + hr * 0.62), (w / 2 + 3.0, 0, h + hr * 0.62), 0.5, 'timber')
    from kitlib import chain
    tube(nm('rope'), [(w / 2 + 2.6, 0, h + hr * 0.62 - 0.2), (w / 2 + 2.6, 0, h - 1.0)], 0.06, 'rope', res=4)
    lathe(nm('pul'), [(0, 0), (0.35, 0), (0.35, 0.2), (0, 0.2)], loc=(w / 2 + 2.6, -0.1, h + hr * 0.62 - 0.35), key='iron', segs=10, rot=(90, 0, 0))
    window(F(-w / 2, 0, h, -90), 0, 2.0, w=2.0, h=3.0, arch=True, frame='wood', sill='wood', panes=False)
    from props import hay_bale, water_trough
    rnd = random.Random(41)
    for k, (x, y, z) in enumerate(((w / 2 + 2.0, -3.0, 0), (w / 2 + 2.0, -0.3, 0), (w / 2 + 2.0, -1.6, 2.6))):
        cyl(nm('hb'), 1.3, 3.6, loc=(x - 1.8, y, z + 1.3), key='thatch', verts=12, rot=(0, 90, 0)) if False else \
            box(nm('hb'), (3.6, 2.4, 2.4), loc=(x, y, z + 1.2), key='thatch', bev=0.25, segs=2)
        for zz in (0.6, 1.8):
            box(nm('hbt'), (0.1, 2.5, 0.1), loc=(x - 0.8, y, z + zz + 0.0), key='rope_dark')
    box(nm('tr'), (6.0, 1.8, 1.4), loc=(-6.0, -d / 2 - 1.8, 0.7), key='wood', bev=0.05)
    box(nm('trw'), (5.6, 1.4, 0.05), loc=(-6.0, -d / 2 - 1.8, 1.3), key='water')
    box(nm('sign'), (5.0, 0.3, 1.4), loc=(0, -d / 2 - 0.2, h + 0.4), key='wood_dark', bev=0.05)
    torus(nm('shoe'), 0.45, 0.12, loc=(0, -d / 2 - 0.45, h + 0.4), key='iron', segs=12, rsegs=4, rot=(90, 0, 0))
    return finalize('stables', smooth_angle=25)


def sentry_box():
    """K42 - royal guard sentry box: striped blue-and-white booth with a pointed roof and lantern."""
    reset()
    W, D, H = 4.4, 4.0, 9.0
    box(nm('fl'), (W + 0.6, D + 0.6, 0.5), loc=(0, 0, 0.25), key='ashlar', bev=0.05)
    for s in (-1, 1):
        for k in range(6):
            box(nm('st'), (0.3, D, H / 6), loc=(s * (W / 2 - 0.15), 0, 0.5 + H / 12 + k * H / 6), key='fabric_blue' if k % 2 == 0 else 'wood_paint')
    for k in range(6):
        box(nm('bk'), (W, 0.3, H / 6), loc=(0, D / 2 - 0.15, 0.5 + H / 12 + k * H / 6), key='fabric_blue' if k % 2 == 0 else 'wood_paint')
    box(nm('top'), (W, D, 1.4), loc=(0, 0, H + 0.5 + 0.7 - 1.4 + 0.7), key='wood_paint')
    box(nm('lnt'), (W + 0.3, 0.4, 0.5), loc=(0, -D / 2 + 0.2, H + 0.3), key='gold')
    lathe(nm('rf'), [(0.0, 0.0), ((W / 2 + 0.6) * 1.414, 0.0), (0.0, 4.4)], loc=(0, 0, H + 1.6), key='tile_a', segs=4)
    lathe(nm('fn'), [(0, 0), (0.25, 0), (0.1, 0.8), (0.25, 1.1), (0, 1.6)], loc=(0, 0, H + 5.8), key='gold', segs=6)
    box(nm('seat'), (W - 0.8, 1.2, 0.3), loc=(0, D / 2 - 0.9, 2.6), key='wood')
    lslab(F(0, -D / 2, 0, 0), [(px * 0.5, 0, pz * 0.5 + H - 0.4) for px, pz in star_pts(0.5, 1.4, 4)], (0, -0.1, 0), 'gold')
    wall_lantern(F(W / 2, 0, 0, 90), 0, 6.5, s=1.0)
    return finalize('sentry_box', smooth_angle=30)


def royal_carriage():
    """K43 - royal carriage: curved gilded coach body, glass doors, crown on the roof, coach lamps and a driver's bench."""
    reset()
    from props import wheel
    L, Wd = 9.0, 5.0
    z0 = 3.0
    prof_y = Wd / 2
    pts = [(-L / 2 + 0.6, z0), (L / 2 - 0.6, z0), (L / 2 + 0.2, z0 + 1.6), (L / 2, z0 + 4.8), (L / 2 - 0.6, z0 + 5.4), (-L / 2 + 0.6, z0 + 5.4), (-L / 2, z0 + 4.8),
           (-L / 2 - 0.2, z0 + 1.6)]
    lslab(F(), [(x, -prof_y, z) for x, z in pts], (0, Wd, 0), 'fabric_blue')
    for s in (-1, 1):
        fr = F(0, s * prof_y, 0, 0 if s < 0 else 180)
        tube(nm('ed'), [fr.p(x * (1 if s < 0 else -1), -0.05, z) for x, z in pts + [pts[0]]], 0.14, 'gold', res=4, ures=1)
        window(fr, 0, z0 + 2.6, w=2.4, h=2.4, frame='gold', sill=None, panes=True, glass='glass')
        lbox(fr, (2.8, 0.1, 2.0), 0, -0.05, z0 + 1.2, 'fabric_blue')
        tube(nm('dr'), [fr.p(-1.5, -0.12, z0 + 0.2), fr.p(-1.5, -0.12, z0 + 5.2), fr.p(1.5, -0.12, z0 + 5.2), fr.p(1.5, -0.12, z0 + 0.2)], 0.08, 'gold', res=4, ures=1)
        lslab(fr.sub(0, -0.14, z0 + 1.2), [(px * 0.35, 0, pz * 0.35) for px, pz in star_pts(0.6, 1.5, 4)], (0, -0.06, 0), 'gold')
        for x in (-L / 2 + 0.2, L / 2 - 0.2):
            pass
    box(nm('rf'), (L - 0.6, Wd + 0.4, 0.4), loc=(0, 0, z0 + 5.6), key='gold', bev=0.1)
    box(nm('rf2'), (L - 1.6, Wd - 0.8, 0.5), loc=(0, 0, z0 + 6.05), key='fabric_blue', bev=0.15)
    lathe(nm('crn'), [(0.0, 0.0), (0.9, 0.0), (1.0, 0.6), (0.0, 0.6)], loc=(0, 0, z0 + 6.3), key='gold', segs=12)
    for k in range(5):
        a = 2 * math.pi * k / 5
        lathe(nm('cp'), [(0, 0), (0.2, 0), (0, 0.8)], loc=(math.cos(a) * 0.85, math.sin(a) * 0.85, z0 + 6.9), key='gold', segs=4)
    ball(nm('cb'), 0.35, loc=(0, 0, z0 + 7.2), key='fabric_red', segs=10, rings=7)
    for x in (-L / 2 + 0.6, L / 2 - 0.6):
        for s in (-1, 1):
            ball(nm('fin'), 0.25, loc=(x, s * (Wd / 2 + 0.1), z0 + 5.9), key='gold', segs=8, rings=6)
    box(nm('ch'), (L + 6.0, 0.5, 0.5), loc=(1.5, -1.6, 2.2), key='wood_dark')
    box(nm('ch2'), (L + 6.0, 0.5, 0.5), loc=(1.5, 1.6, 2.2), key='wood_dark')
    for x, r in ((-3.0, 2.2), (3.4, 1.6)):
        for s in (-1, 1):
            wheel(nm('wh'), r, (x, s * (Wd / 2 + 0.6), r), axis='Y', key='gold', spokes=12, iron=False)
        box(nm('ax'), (0.4, Wd + 1.4, 0.4), loc=(x, 0, r), key='iron_dark')
    for s in (-1, 1):
        tube(nm('sp'), [(-L / 2 - 0.5, s * 1.6, 2.2), (-L / 2 + 0.6, s * 1.6, 3.4)], 0.18, 'gold', res=4)
    box(nm('db'), (2.0, Wd - 0.6, 0.5), loc=(L / 2 + 1.6, 0, z0 + 3.2), key='fabric_red', bev=0.1)
    box(nm('dbb'), (2.2, Wd - 0.4, 3.2), loc=(L / 2 + 1.6, 0, z0 + 1.4), key='fabric_blue', bev=0.1)
    box(nm('fr'), (0.4, Wd - 0.4, 1.6), loc=(L / 2 + 2.6, 0, z0 + 3.6), key='gold', bev=0.08)
    for s in (-1, 1):
        f = F(L / 2 + 0.3, s * (Wd / 2 + 0.25), 0, 0)
        lathe(nm('ll'), [(0, 0), (0.3, 0), (0.35, 0.9), (0.45, 1.0), (0.15, 1.4), (0, 1.5)], loc=f.p(0, 0, z0 + 4.2), key='gold', segs=6)
        lathe(nm('lg'), [(0, 0.1), (0.3, 0.1), (0.33, 0.85), (0, 0.85)], loc=f.p(0, 0, z0 + 4.2), key='glass_lit', segs=6)
    lbeam(F(), (L / 2 + 2.6, 0, 2.2), (L / 2 + 10.0, 0, 3.6), 0.35, 'wood_dark')
    return finalize('royal_carriage', smooth_angle=30)


def monument_column():
    """K44 - plaza monument column: fluted marble column with spiral relief band, gold orb-and-star crown, 46 tall."""
    reset()
    from capital import plinth
    plinth(7.0, w=8.0)
    lathe(nm('cb'), [(0, 7.0), (3.2, 7.0), (3.2, 7.8), (2.8, 8.3), (2.6, 9.0), (0, 9.0)], key='castle_trim', segs=24)
    lathe(nm('cs'), [(0, 9.0), (2.3, 9.0), (2.0, 38.0), (0, 38.0)], key='marble', segs=24)
    n = 80
    pts = []
    for i in range(n + 1):
        t = i / n
        a = t * 6.5 * 2 * math.pi
        r = 2.3 - 0.3 * t + 0.12
        pts.append((math.cos(a) * r, math.sin(a) * r, 10.0 + t * 27.0))
    tube(nm('sp'), pts, 0.22, 'gold', res=4, ures=2)
    lathe(nm('cc'), [(0, 38.0), (2.2, 38.0), (2.8, 39.0), (3.4, 39.6), (3.4, 40.4), (0, 40.4)], key='castle_trim', segs=24)
    box(nm('ab'), (6.8, 6.8, 1.0), loc=(0, 0, 40.9), key='marble', bev=0.06)
    lathe(nm('ped'), [(0, 41.4), (1.4, 41.4), (1.0, 42.4), (0.7, 43.4), (1.1, 43.8), (0, 43.8)], key='gold', segs=16)
    ball(nm('orb'), 1.3, loc=(0, 0, 45.0), key='gold', segs=16, rings=10)
    torus(nm('ob'), 1.32, 0.1, loc=(0, 0, 45.0), key='castle_trim', segs=24, rsegs=4, rot=(90, 0, 0))
    lslab(F(0, 0.15, 46.0, 0), [(px, 0, pz + 1.6) for px, pz in star_pts(0.5, 1.6, 4)], (0, -0.3, 0), 'gold')
    return finalize('monument_column', smooth_angle=30)


ITEMS_NOBLE = [
    ('K37_mansion_1', mansion_1), ('K38_mansion_2', mansion_2), ('K39_mansion_3', mansion_3), ('K40_barracks', barracks),
    ('K41_stables', stables), ('K42_sentry_box', sentry_box), ('K43_royal_carriage', royal_carriage), ('K44_monument_column', monument_column),
]
