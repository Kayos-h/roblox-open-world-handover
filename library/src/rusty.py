"""D. Rusty run-down town with a beautiful church. Fronts face -Y."""
import math, random
from mathutils import Vector
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, top_paint, flame, chain, scroll
from arch import (F, faces, lbox, lbeam, beam3, slab, lslab, window, door, arrow_slit, quoins, band, corbels, battlements,
                  gable_roof, roof_z, cone_roof, chimney, dormer, railing, wall_lantern, arc_pts, nm, lancet, rose_window,
                  column_c, pediment, pinnacle, lancet_pts, flower_box, timber_frame)
from capital import stone_face, pointed_portal, star_pts, plinth
from nature import blob

S, SD, ST = 'sandstone', 'sandstone_dark', 'sandstone_trim'
CR = ('roof_red', 'roof_dark')
GL = ['stained_b', 'stained_r', 'stained_y', 'stained_g']


def ivy(x0, x1, y, z0, z1, n, seed, face_dir=-1):
    rnd = random.Random(seed)
    for i in range(n):
        x = rnd.uniform(x0, x1)
        z = z0 + (z1 - z0) * rnd.random() ** 1.6
        ball(nm('iv'), rnd.uniform(0.35, 0.6), loc=(x, y + face_dir * 0.15, z), key=rnd.choice(['ivy', 'leaf_dark']), segs=6, rings=4,
             scale=(1.2, 0.45, 1.0))


# ============================================================ church
def church():
    """D1 - the beautiful church: sandstone gothic nave, buttresses, rose window, apse and a tall bell tower with spire."""
    reset()
    NW, NL, NH = 18.0, 44.0, 22.0
    y0 = -NL / 2
    box(nm('nv'), (NW, NL, NH), loc=(0, 0, NH / 2), key=S)
    box(nm('pl'), (NW + 2, NL + 2, 1.4), loc=(0, 0, 0.7), key=SD, bev=0.08)
    band(0, 0, NW, NL, NH - 0.5, 0.8, ST, out=0.35)
    gable_roof(F(0, 0, 0, 90), NL, NW, NH, 12.0, keys=CR, wall=S, ov=0.9, ovg=0.6, barge=ST, ridge='roof_dark')
    for s in (-1, 1):
        fr = F(s * NW / 2, 0, 0, s * 90)
        stone_face(fr, -NL / 2, NL / 2, 1.5, NH - 1, 70, 400 + s, keys=(S, SD, ST))
        for i in range(5):
            yy = y0 + 6.0 + i * 8.0
            lancet(fr, yy * s, 5.0, w=2.8, h=12.0, glass=GL[(i + (s > 0)) % 4], frame=ST)
        for i in range(6):
            yy = y0 + 2.0 + i * 8.0
            x = s * (NW / 2 + 1.0)
            box(nm('bt'), (2.0, 2.2, 15.0), loc=(x, yy, 7.5), key=S, bev=0.08)
            lslab(F(), [(x - 1.0, yy - 1.1, 15.0), (x - 1.0, yy - 1.1, 15.0), (x + s * 0, yy - 1.1, 15.0)], (0, 0, 0), S) if False else None
            lslab(F(), [(s * NW / 2, yy - 1.1, 15.0), (x + s * 1.0, yy - 1.1, 15.0), (s * NW / 2, yy - 1.1, 19.0)], (0, 2.2, 0), SD)
            pinnacle(x, yy, 15.0, s=1.2, h=4.5, key=ST, tip=ST)
    ay = NL / 2
    lathe(nm('ap'), [(0.0, 0.0), (NW / 2, 0.0), (NW / 2, NH - 2), (0.0, NH - 2)], loc=(0, ay, 0), key=S, segs=12)
    lathe(nm('apr'), [(0.0, NH - 2.5), (NW / 2 + 0.9, NH - 2.5), (0.0, NH + 7)], loc=(0, ay, 0), key='roof_dark', segs=12)
    for i in range(3):
        a = math.radians(45 + 45 * i)
        fr = F(math.cos(a) * NW / 2 * 0.97, ay + math.sin(a) * NW / 2 * 0.97, 0, math.degrees(a) + 90)
        lancet(fr, 0, 5.0, w=2.2, h=11.0, glass=GL[i % 4], frame=ST)
    fw = F(0, y0, 0, 0)
    pointed_portal(fw, -4.2, 4.4, 10.0, orders=3, trim=ST, tymp='gold')
    rose_window(fw, -1.5, 16.5, 4.0, frame=ST)
    lbox(fw, (NW, 0.6, 0.6), 0, -0.3, 11.6, ST)
    gf = F(0, y0, NH, 0)
    lathe(nm('cr'), [(0, 0), (0.25, 0), (0.25, 3.0), (0, 3.0)], loc=gf.p(0, -0.3, 11.5), key='gold', segs=6)
    box(nm('crx'), (1.8, 0.3, 0.3), loc=gf.p(0, -0.3, 13.6), key='gold')
    # bell tower (front right)
    tx, ty, TW, TH = NW / 2 + 1.0, y0 + 4.0, 10.0, 40.0
    box(nm('tw'), (TW, TW, TH), loc=(tx, ty, TH / 2), key=S)
    box(nm('twp'), (TW + 1.2, TW + 1.2, 2.0), loc=(tx, ty, 1.0), key=SD, bev=0.08)
    for zz in (12.0, 26.0, TH - 0.5):
        band(tx, ty, TW, TW, zz, 0.6, ST, out=0.3)
    for k, fr in enumerate(faces(tx, ty, TW, TW).values()):
        stone_face(fr, -TW / 2, TW / 2, 2.0, TH - 1, 30, 420 + k, keys=(S, SD, ST))
        lancet(fr, 0, 15.0, w=2.0, h=8.0, glass=GL[k % 4], frame=ST, medallion=None)
        lslab(fr, [(px, 0.0, pz) for px, pz in lancet_pts(0, 28.0, 33.0, 3.6)], (0, -0.1, 0), 'hole')
        tube(nm('bf'), [fr.p(px, -0.25, pz) for px, pz in lancet_pts(0, 28.0, 33.0, 3.9)[1:-1]], 0.3, ST, res=4)
        for zz in (4.5,):
            if k == 0:
                door(fr, 0, w=3.0, h=6.5, arch=True, surround=ST, step=SD)
    lathe(nm('bell'), [(0.0, 0.0), (1.6, 0.0), (1.7, 0.2), (1.2, 0.7), (1.0, 1.8), (0.9, 2.6), (0.35, 2.8), (0.0, 2.8)], loc=(tx, ty, 29.5), key='bronze', segs=16)
    box(nm('yk'), (TW - 1.6, 0.5, 0.6), loc=(tx, ty, 32.6), key='timber')
    for sx in (-1, 1):
        for sy in (-1, 1):
            pinnacle(tx + sx * (TW / 2 - 0.5), ty + sy * (TW / 2 - 0.5), TH, s=1.2, h=5.0, key=ST, tip=ST)
    lathe(nm('sp'), [(0.0, 0.0), (TW / 2 - 0.6, 0.0), (0.0, 22.0)], loc=(tx, ty, TH), key='roof_dark', segs=8)
    for k in range(3):
        rr = (TW / 2 - 0.6) * (1 - (k * 6 + 4) / 22) + 0.2
        lathe(nm('spb'), [(0.0, 0.0), (rr, 0.0), (rr, 0.4), (0.0, 0.4)], loc=(tx, ty, TH + k * 6 + 4), key=ST, segs=8)
    lathe(nm('spf'), [(0, 0), (0.3, 0), (0.1, 1.6), (0, 1.8)], loc=(tx, ty, TH + 21.8), key='gold', segs=6)
    box(nm('spc'), (0.22, 0.22, 2.4), loc=(tx, ty, TH + 24.4), key='gold')
    box(nm('spx'), (1.4, 0.22, 0.22), loc=(tx, ty, TH + 25.0), key='gold')
    for k in range(3):
        box(nm('st'), (12.0 - k * 1.2, 1.4, 0.45), loc=(-4.2, y0 - 3.0 + k * 1.0, 0.22 + k * 0.45), key=SD if k % 2 else ST, bev=0.04)
    ivy(-NW / 2, -NW / 2 + 6, y0 - 0.1, 0.5, 9.0, 40, 1)
    return finalize('church', smooth_angle=25)


def church_bell():
    """D2 - church bell in a timber yoke frame with wheel and rope."""
    reset()
    lathe(nm('b'), [(0.0, 0.0), (2.6, 0.0), (2.75, 0.3), (2.0, 1.0), (1.65, 2.8), (1.5, 4.2), (0.6, 4.6), (0.0, 4.6)], loc=(0, 0, 1.4), key='bronze', segs=24)
    for zz in (1.7, 2.6, 5.4):
        torus(nm('r'), 2.05 if zz < 2 else (1.75 if zz < 3 else 0.95), 0.06, loc=(0, 0, zz), key='bronze', segs=24, rsegs=4)
    ball(nm('cl'), 0.45, loc=(0, 0, 1.1), key='iron_dark', segs=10, rings=7)
    cyl(nm('cls'), 0.08, 3.0, loc=(0, 0, 1.2), key='iron_dark', verts=6)
    box(nm('yk'), (1.2, 1.4, 1.0), loc=(0, 0, 6.4), key='timber')
    cyl(nm('ax'), 0.2, 9.0, loc=(-4.5, 0, 6.4), key='iron', verts=10, rot=(0, 90, 0))
    for s in (-1, 1):
        box(nm('fp'), (0.8, 0.8, 7.4), loc=(s * 4.0, 0, 3.7), key='timber')
        box(nm('ff'), (0.9, 3.0, 0.8), loc=(s * 4.0, 0, 0.4), key='timber')
        for d in (-1, 1):
            lbeam(F(), (s * 4.0, d * 1.4, 0.8), (s * 4.0, 0, 4.8), 0.4, 'timber')
    torus(nm('wh'), 2.2, 0.15, loc=(4.7, 0, 6.4), key='timber', segs=20, rsegs=4, rot=(0, 90, 0))
    for k in range(4):
        a = math.pi * k / 4
        lbeam(F(), (4.7, math.cos(a) * 2.2, 6.4 + math.sin(a) * 2.2), (4.7, -math.cos(a) * 2.2, 6.4 - math.sin(a) * 2.2), 0.14, 'timber')
    tube(nm('rope'), [(4.7, 2.2, 6.4), (4.7, 2.3, 3.0), (4.7, 2.3, 0.4)], 0.07, 'rope', res=4)
    return finalize('church_bell', smooth_angle=35)


def church_rose_window():
    """D3 - rose stained glass window panel, 12 across, sandstone tracery."""
    reset()
    f = F(0, 0, 0, 0)
    cyl(nm('bk'), 6.8, 1.2, loc=(0, 0.0, 7.0), key=S, verts=32, rot=(-90, 0, 0))
    rose_window(f, 0, 7.0, 5.6, keys=('stained_b', 'stained_r', 'stained_y', 'stained_g'), frame=ST, petals=16)
    torus(nm('or'), 6.4, 0.45, loc=(0, -0.4, 7.0), key=ST, segs=40, rsegs=6, rot=(90, 0, 0))
    for i in range(16):
        a = 2 * math.pi * (i + 0.5) / 16
        ball(nm('cu'), 0.35, loc=(math.cos(a) * 6.4, -0.6, 7.0 + math.sin(a) * 6.4), key=ST, segs=8, rings=6)
    return finalize('church_rose_window', smooth_angle=30)


def church_tall_window():
    """D4 - tall triple-lancet stained glass window, 9 wide x 20 tall."""
    reset()
    f = F()
    lslab(f, [(px, 0.0, pz) for px, pz in lancet_pts(0, 0.0, 14.0, 9.0)], (0, 1.2, 0), S)
    lancet(f, -2.7, 1.0, w=2.2, h=12.0, glass='stained_r', frame=ST, medallion='stained_y')
    lancet(f, 0.0, 1.0, w=2.4, h=15.0, glass='stained_b', frame=ST, medallion='stained_y')
    lancet(f, 2.7, 1.0, w=2.2, h=12.0, glass='stained_g', frame=ST, medallion='stained_y')
    for x in (-1.4, 1.4):
        cyl(nm('oc'), 0.9, 0.12, loc=f.p(x, -0.05, 15.2), key='stained_y', verts=12, rot=f.r(90, 0, 0))
        torus(nm('ocr'), 0.95, 0.15, loc=f.p(x, -0.2, 15.2), key=ST, segs=16, rsegs=4, rot=f.r(90, 0, 0))
    tube(nm('fr'), [f.p(px, -0.3, pz) for px, pz in lancet_pts(0, 0.0, 14.0, 8.4)[1:-1]], 0.35, ST, res=4)
    lbox(f, (10.0, 1.4, 0.6), 0, -0.3, -0.3, ST, bev=0.06)
    return finalize('church_tall_window', smooth_angle=25)


def pew():
    """D5 - church pew: 12-wide wooden bench with carved ends, backrest and kneeler."""
    reset()
    W = 12.0
    box(nm('seat'), (W, 2.0, 0.3), loc=(0, 0, 1.9), key='wood', bev=0.05)
    box(nm('back'), (W, 0.25, 2.2), loc=(0, 0.95, 3.2), key='wood', rot=(-8, 0, 0), bev=0.05)
    box(nm('rail'), (W, 0.4, 0.25), loc=(0, 1.1, 4.3), key='wood_dark', bev=0.05)
    box(nm('shelf'), (W, 0.8, 0.15), loc=(0, 1.5, 3.4), key='wood_dark')
    box(nm('kn'), (W - 1.0, 0.8, 0.4), loc=(0, -1.6, 0.4), key='velvet', bev=0.1)
    for s in (-1, 1):
        pts = [(0, -1.1, 0), (0, 1.3, 0), (0, 1.3, 4.6), (0, 0.6, 5.2), (0, 0.0, 4.9), (0, -0.4, 3.0), (0, -1.1, 2.4)]
        lslab(F(s * (W / 2 + 0.1), 0, 0, 0), [(p[0], p[1], p[2]) for p in pts], (-s * 0.3, 0, 0), 'wood_dark')
        cyl(nm('cv'), 0.4, 0.05, loc=(s * (W / 2 + 0.12), 0.4, 3.6), key='wood', verts=10, rot=(0, 90, 0))
    for x in (-W / 4, W / 4):
        box(nm('lg'), (0.3, 1.6, 1.8), loc=(x, 0, 0.9), key='wood_dark')
    return finalize('pew', smooth_angle=30)


def altar():
    """D6 - stone altar with embroidered cloth, gold cross, candlesticks and an open book."""
    reset()
    box(nm('st'), (12.0, 6.0, 0.8), loc=(0, 0, 0.4), key=ST, bev=0.06)
    box(nm('a'), (9.0, 3.6, 3.4), loc=(0, 0.4, 2.5), key='marble', bev=0.06)
    box(nm('at'), (9.6, 4.0, 0.4), loc=(0, 0.4, 4.4), key=ST, bev=0.05)
    box(nm('cl'), (9.8, 4.2, 0.08), loc=(0, 0.4, 4.64), key='fabric_cream')
    box(nm('clf'), (6.0, 0.08, 2.4), loc=(0, -1.75, 3.5), key='fabric_red')
    lbox(F(0, -1.82, 0, 0), (5.6, 0.04, 0.2), 0, 0, 2.5, 'gold')
    lbox(F(0, -1.82, 0, 0), (0.3, 0.04, 1.6), 0, 0, 3.6, 'gold')
    lbox(F(0, -1.82, 0, 0), (1.2, 0.04, 0.3), 0, 0, 4.0, 'gold')
    for i in range(3):
        column_c(-3.0 + i * 3.0, -1.4, 0.8, 3.4, 0.3, key=ST, base=ST) if False else None
    box(nm('cb'), (1.2, 0.8, 0.5), loc=(0, 1.6, 4.9), key='gold', bev=0.05)
    box(nm('cv'), (0.35, 0.35, 4.0), loc=(0, 1.6, 7.1), key='gold')
    box(nm('ch'), (2.4, 0.35, 0.35), loc=(0, 1.6, 8.0), key='gold')
    for s in (-1, 1):
        lathe(nm('cs'), [(0, 0), (0.45, 0), (0.2, 0.3), (0.12, 1.6), (0.3, 1.8), (0, 1.85)], loc=(s * 3.4, 1.4, 4.68), key='gold', segs=10)
        cyl(nm('cd'), 0.16, 1.4, loc=(s * 3.4, 1.4, 6.5), key='wax', verts=8)
        flame(nm('fl'), (s * 3.4, 1.4, 7.9), h=0.45, r=0.12, tongues=0)
    box(nm('bk1'), (1.2, 1.4, 0.15), loc=(-0.65, -0.6, 4.75), key='paper', rot=(0, -8, 0))
    box(nm('bk2'), (1.2, 1.4, 0.15), loc=(0.65, -0.6, 4.75), key='paper', rot=(0, 8, 0))
    box(nm('bkc'), (2.6, 1.5, 0.08), loc=(0, -0.6, 4.68), key='book_a')
    return finalize('altar', smooth_angle=30)


def pulpit():
    """D7 - carved wooden pulpit: octagonal box on a column, curved stair with rail and a sounding-board canopy."""
    reset()
    lathe(nm('bs'), [(0, 0), (1.8, 0), (1.8, 0.5), (0.8, 0.9), (0.6, 5.0), (1.6, 5.6), (0, 5.6)], key=ST, segs=8)
    lathe(nm('bx'), [(0, 5.6), (2.6, 5.6), (2.8, 6.0), (2.8, 9.0), (3.1, 9.3), (3.1, 9.6), (2.5, 9.6), (2.5, 6.0), (0, 6.0)], key='wood_dark', segs=8)
    for i in range(8):
        a = 2 * math.pi * (i + 0.5) / 8
        fr = F(math.cos(a) * 2.6, math.sin(a) * 2.6, 0, math.degrees(a) + 90)
        lslab(fr, [(px * 0.5, -0.12, pz * 0.5 + 6.6) for px, pz in lancet_pts(0, 0.0, 3.2, 1.6)], (0, -0.08, 0), 'wood')
    box(nm('bk'), (2.4, 0.2, 1.2), loc=(0, -2.6, 9.8), key='wood', rot=(30, 0, 0))
    box(nm('bko'), (2.0, 0.15, 1.4), loc=(0, -2.75, 9.95), key='paper', rot=(30, 0, 0))
    n = 10
    for i in range(n):
        a = math.radians(30 + i * 9)
        r = 4.2
        box(nm('stp'), (1.6, 1.0, 0.25), loc=(math.cos(a) * r, math.sin(a) * r, 0.6 * (i + 1)), key='wood', rot=(0, 0, math.degrees(a) + 90))
        box(nm('stc'), (0.2, 1.0, 0.6 * (i + 1)), loc=(math.cos(a) * (r + 0.8), math.sin(a) * (r + 0.8), 0.3 * (i + 1)), key='wood_dark', rot=(0, 0, math.degrees(a) + 90))
        cyl(nm('bal'), 0.08, 1.8, loc=(math.cos(a) * (r + 0.7), math.sin(a) * (r + 0.7), 0.6 * (i + 1)), key='wood_dark', verts=6)
    tube(nm('hr'), [(math.cos(math.radians(30 + i * 9)) * 4.9, math.sin(math.radians(30 + i * 9)) * 4.9, 0.6 * (i + 1) + 1.8) for i in range(n)], 0.1, 'wood_dark', res=4)
    cyl(nm('pp'), 0.3, 6.0, loc=(0, 2.7, 9.6), key='wood_dark', verts=8)
    lathe(nm('can'), [(0, 15.4), (3.4, 15.4), (3.4, 16.0), (2.0, 17.0), (0.6, 18.0), (0, 18.4)], loc=(0, 0.6, 0), key='wood_dark', segs=8)
    lathe(nm('canf'), [(0, 0), (0.3, 0), (0.1, 0.8), (0, 1.2)], loc=(0, 0.6, 18.3), key='gold', segs=6)
    return finalize('pulpit', smooth_angle=30)


def pipe_organ():
    """D8 - pipe organ: carved wood case, three towers of tin pipes and a two-keyboard console with bench."""
    reset()
    W, D = 16.0, 5.0
    box(nm('cs'), (W, D, 9.0), loc=(0, 1.0, 4.5), key='wood_dark', bev=0.06)
    box(nm('csc'), (W + 0.6, D + 0.6, 0.6), loc=(0, 1.0, 9.3), key='wood', bev=0.05)
    rnd = random.Random(8)
    for gx, n, hmax in ((-5.5, 7, 12.0), (0.0, 9, 18.0), (5.5, 7, 12.0)):
        for i in range(n):
            t = abs(i - (n - 1) / 2) / ((n - 1) / 2)
            h = hmax * (1 - t * 0.45)
            x = gx + (i - (n - 1) / 2) * 0.62
            r = 0.27 - t * 0.06
            cyl(nm('pp'), r, h, loc=(x, -0.9, 9.6), key='steel', verts=10)
            lathe(nm('mo'), [(0, 0), (r * 0.9, 0), (0, 0.8)], loc=(x, -0.9 - r, 9.6 + h * 0.18), key='hole', segs=4, rot=(90, 0, 0))
            lathe(nm('ft'), [(0, 0), (0.05, 0), (r, 0.9), (0, 0.9)], loc=(x, -0.9, 8.7 + 0.9), key='steel', segs=10, rot=(180, 0, 0))
        box(nm('tw'), (n * 0.62 + 0.6, 2.0, 0.5), loc=(gx, -0.6, 9.6 + hmax + 0.3), key='wood_dark', bev=0.05)
        pinnacle(gx, -0.6, 9.6 + hmax + 0.6, s=0.8, h=2.6, key='wood_dark', tip='gold')
    for i in range(14):
        x = -7.5 + i * 1.15
        if abs(x) < 2.4:
            continue
        cyl(nm('bp'), 0.2, 4.0 + rnd.uniform(0, 2), loc=(x, 1.8, 9.6), key='tin_b', verts=8)
    box(nm('con'), (6.0, 2.6, 3.6), loc=(0, -2.6, 1.8), key='wood', bev=0.05)
    for k in range(2):
        box(nm('kb'), (5.0, 0.8, 0.15), loc=(0, -3.6 + k * 0.4, 3.0 + k * 0.4), key='fabric_cream')
        for j in range(18):
            if j % 7 in (0, 3):
                continue
            box(nm('bkk'), (0.12, 0.45, 0.08), loc=(-2.3 + j * 0.27, -3.5 + k * 0.4, 3.1 + k * 0.4), key='iron_dark')
    box(nm('ms'), (3.0, 0.15, 1.6), loc=(0, -2.0, 4.6), key='wood_dark', rot=(-15, 0, 0))
    box(nm('sh'), (2.6, 0.08, 1.2), loc=(0, -2.12, 4.7), key='paper', rot=(-15, 0, 0))
    box(nm('bn'), (5.0, 1.4, 0.3), loc=(0, -5.4, 1.9), key='wood_dark', bev=0.05)
    for s in (-1, 1):
        box(nm('bnl'), (0.3, 1.2, 1.8), loc=(s * 2.2, -5.4, 0.9), key='wood_dark')
    for k in range(12):
        box(nm('pd'), (0.25, 1.4, 0.15), loc=(-1.6 + k * 0.3, -3.6, 0.2), key='wood_light', rot=(-12, 0, 0))
    return finalize('pipe_organ', smooth_angle=30)


def candle_stand():
    """D9 - iron votive candle stand: three curved tiers of small candles and a sand tray."""
    reset()
    lathe(nm('b'), [(0, 0), (1.4, 0), (1.2, 0.3), (0.3, 0.6), (0.2, 3.0), (0, 3.0)], key='iron_dark', segs=12)
    rnd = random.Random(9)
    for tier, (R, z, n) in enumerate(((2.6, 3.0, 11), (1.9, 3.8, 8), (1.2, 4.6, 5))):
        tube(nm('rl'), [(math.cos(math.radians(a)) * R, math.sin(math.radians(a)) * R - 0.5, z) for a in range(200, 341, 20)], 0.08, 'iron_dark', res=4)
        for i in range(n):
            a = math.radians(200 + 140 * i / (n - 1))
            x, y = math.cos(a) * R, math.sin(a) * R - 0.5
            lathe(nm('cup'), [(0, 0), (0.18, 0), (0.24, 0.3), (0, 0.3)], loc=(x, y, z), key='glass_lit', segs=8)
            h = rnd.uniform(0.2, 0.7)
            cyl(nm('cd'), 0.13, h, loc=(x, y, z + 0.1), key='wax', verts=8)
            if rnd.random() < 0.8:
                flame(nm('fl'), (x, y, z + 0.1 + h), h=0.3, r=0.08, tongues=0, seed=i)
        lbeam(F(), (0, 0, z - 0.2), (0, -0.5 - R * 0.9, z), 0.1, 'iron_dark')
    lathe(nm('tr'), [(0, 4.9), (0.8, 4.9), (0.9, 5.3), (0, 5.2)], key='brass', segs=12)
    return finalize('candle_stand', smooth_angle=35)


def church_pillar():
    """D10 - gothic interior pillar: clustered shafts with ring capitals, 24 tall, springing ribs."""
    reset()
    lathe(nm('b'), [(0, 0), (2.4, 0), (2.4, 0.8), (2.0, 1.2), (0, 1.2)], key=SD, segs=8)
    cyl(nm('c'), 1.2, 22.0, loc=(0, 0, 1.2), key=S, verts=16)
    for i in range(8):
        a = 2 * math.pi * i / 8
        r = 0.42 if i % 2 == 0 else 0.3
        cyl(nm('sh'), r, 21.0, loc=(math.cos(a) * 1.25, math.sin(a) * 1.25, 1.2), key=ST, verts=8)
    for zz in (11.0, 21.6):
        lathe(nm('rc'), [(0, zz), (1.9, zz), (2.1, zz + 0.4), (2.4, zz + 1.0), (0, zz + 1.0)], key=ST, segs=16)
    for i in range(4):
        a = 2 * math.pi * i / 4 + math.pi / 4
        tube(nm('rib'), [(math.cos(a) * 1.8, math.sin(a) * 1.8, 22.6), (math.cos(a) * 3.2, math.sin(a) * 3.2, 24.6), (math.cos(a) * 4.6, math.sin(a) * 4.6, 25.6)], 0.4, ST, res=4)
    return finalize('church_pillar', smooth_angle=30)


def church_door():
    """D11 - ornate church door: double pointed-arch oak doors with scrolled iron hinges and carved surround."""
    reset()
    f = F()
    w, h = 6.0, 11.0
    zs = h - w * 0.866
    for s in (-1, 1):
        pts = [p for p in lancet_pts(0, 0, zs, w)]
        half = [(px, 0.0, pz) for px, pz in pts if (px <= 0.001 if s < 0 else px >= -0.001)]
        if s < 0:
            half = [(0, 0, 0)] + [(px, 0.0, pz) for px, pz in pts if px <= 0.001][::-1] if False else [(px, 0.0, pz) for px, pz in pts if px <= 0.001] + [(0.0, 0.0, 0.0)]
        else:
            half = [(0.0, 0.0, 0.0)] + [(px, 0.0, pz) for px, pz in pts if px >= -0.001]
        lslab(f, [(px + s * 0.03, y, pz) for px, y, pz in half], (0, -0.4, 0), 'wood_dark')
        for zz in (1.4, 4.4, 7.4):
            tube(nm('hg'), [f.p(s * 2.8, -0.48, zz), f.p(s * 1.6, -0.5, zz), f.p(s * 0.6, -0.5, zz + 0.1)], 0.1, 'iron', res=4)
            scroll(nm('sc'), (s * 0.9, -0.5, zz + 0.45), 0.05, 0.4, 1.4, plane='XZ', key='iron', radius=0.06)
            scroll(nm('sc'), (s * 1.6, -0.5, zz - 0.45), 0.05, 0.35, 1.3, plane='XZ', key='iron', radius=0.06)
        torus(nm('rg'), 0.35, 0.07, loc=f.p(s * 0.6, -0.55, 4.4), key='iron', segs=12, rsegs=4, rot=f.r(90, 0, 0))
        for i in range(4):
            lbox(f, (0.05, 0.05, zs - 0.3), s * (0.5 + i * 0.65), -0.42, zs / 2, 'timber')
    lbox(f, (0.12, 0.5, zs + w * 0.8), 0, -0.2, (zs + w * 0.8) / 2, 'iron_dark')
    for k in range(2):
        ww = w + 1.0 + k * 1.2
        tube(nm('po'), [f.p(px, -0.3 - k * 0.5, pz) for px, pz in lancet_pts(0, 0, zs, ww)[1:-1]], 0.36, ST, res=4)
        for s in (-1, 1):
            cyl(nm('pc'), 0.34, zs, loc=f.p(s * ww / 2, -0.3 - k * 0.5, 0), key=ST, verts=8)
    lslab(f, [(px, 0.25, pz) for px, pz in lancet_pts(0, 0.0, zs, w + 3.6)] + [], (0, 0.6, 0), S)
    box(nm('st'), (w + 4.0, 2.0, 0.5), loc=(0, -1.0, 0.25), key=SD, bev=0.05)
    return finalize('church_door', smooth_angle=25)


# ============================================================ graveyard
def _moss(o, amt=0.6, seed=0):
    top_paint(o, 'moss', amt, seed)


def gravestone_1():
    """D12 - rounded-top headstone, slightly leaning, mossy."""
    reset()
    pts = [(-1.2, 0, 0), (1.2, 0, 0), (1.2, 0, 3.0)] + [(math.cos(math.radians(a)) * 1.2, 0, 3.0 + math.sin(math.radians(a)) * 1.0) for a in range(15, 166, 15)] + [(-1.2, 0, 3.0)]
    o = lslab(F(0, 0.25, 0, 0), pts, (0, -0.5, 0), 'stone')
    o.rotation_euler = (math.radians(5), math.radians(-3), 0)
    _moss(o, 0.5, 1)
    lbox(F(0, -0.27, 0, 0), (1.6, 0.04, 0.2), 0, 0, 2.6, 'stone_dark')
    lbox(F(0, -0.27, 0, 0), (1.0, 0.04, 0.15), 0, 0, 2.1, 'stone_dark')
    lbox(F(0, -0.27, 0, 0), (0.2, 0.04, 0.9), 0, 0, 3.3, 'stone_dark')
    lbox(F(0, -0.27, 0, 0), (0.7, 0.04, 0.18), 0, 0, 3.45, 'stone_dark')
    box(nm('gr'), (2.4, 4.2, 0.35), loc=(0, -2.3, 0.17), key='dirt', bev=0.15)
    ball(nm('fl'), 0.25, loc=(0.6, -1.0, 0.4), key='fl_white', segs=6, rings=4)
    return finalize('gravestone_1', smooth_angle=25)


def gravestone_2():
    """D13 - weathered wooden grave cross with rope binding, a stone ring border and a dirt mound."""
    reset()
    rnd = random.Random(13)
    box(nm('gr'), (2.2, 4.0, 0.4), loc=(0, -1.8, 0.2), key='dirt', bev=0.15)
    for i in range(12):
        t = i / 11
        x = -1.3 if i < 6 else 1.3
        y = 0.2 - (i % 6) * 0.8
        ball(nm('rs'), rnd.uniform(0.25, 0.35), loc=(x, y, 0.15), key=rnd.choice(['stone', 'stone_dark']), segs=6, rings=4, scale=(1.2, 1, 0.7))
    o = box(nm('v'), (0.4, 0.3, 4.6), loc=(0, 0.3, 2.1), key='wood_grey', rot=(0, 4, 0))
    box(nm('h'), (2.2, 0.3, 0.4), loc=(0.1, 0.25, 3.4), key='wood_grey', rot=(0, -6, 0))
    for k in range(3):
        torus(nm('rp'), 0.3, 0.05, loc=(0.1, 0.25, 3.4), key='rope', segs=10, rsegs=3, rot=(0, 45 + k * 30, 0))
    ball(nm('fl'), 0.2, loc=(0.3, -1.5, 0.45), key='fl_yellow', segs=6, rings=4)
    ball(nm('fl'), 0.2, loc=(-0.2, -1.9, 0.45), key='fl_white', segs=6, rings=4)
    return finalize('gravestone_2', smooth_angle=25)


def gravestone_3():
    """D14 - tall obelisk-style grave marker with an urn."""
    reset()
    box(nm('b'), (1.8, 1.8, 0.6), loc=(0, 0, 0.3), key='stone_dark', bev=0.05)
    o = lathe(nm('ob'), [(0, 0.6), (0.9, 0.6), (0.6, 4.6), (0, 4.6)], key='stone', segs=4)
    lathe(nm('urn'), [(0, 4.6), (0.4, 4.6), (0.25, 4.8), (0.55, 5.3), (0.4, 5.8), (0.2, 5.9), (0, 6.0)], key='stone_light', segs=10)
    from mathutils import noise
    lbox(F(0, -0.62, 0, 0), (0.6, 0.04, 0.6), 0, 0, 2.4, 'stone_dark')
    _moss(o, 0.6, 3)
    return finalize('gravestone_3', smooth_angle=25)


def gravestone_4():
    """D15 - broken, half-sunk old headstone with a crack and ivy."""
    reset()
    pts = [(-1.0, 0, 0), (1.0, 0, 0), (1.0, 0, 1.6), (0.4, 0, 2.2), (0.1, 0, 1.7), (-0.3, 0, 2.5), (-1.0, 0, 2.3)]
    o = lslab(F(0, 0.2, 0, 0), pts, (0, -0.4, 0), 'stone_dark')
    o.rotation_euler = (math.radians(-12), math.radians(8), 0)
    _moss(o, 0.2, 4)
    lslab(F(0.8, -0.8, 0.0, 30), [(-0.6, 0, 0), (0.5, 0, 0), (0.2, 0, 0.3), (-0.4, 0, 0.35)], (0, -0.35, 0), 'stone_dark')
    ivy(-1.0, 1.0, -0.25, 0.1, 1.6, 10, 5)
    box(nm('gr'), (2.2, 3.6, 0.25), loc=(0, -2.0, 0.12), key='dirt', bev=0.12)
    return finalize('gravestone_4', smooth_angle=25)


def stone_cross():
    """D16 - tall ringed stone cross on a three-step base, carved knot bands."""
    reset()
    for k in range(3):
        box(nm('b'), (4.0 - k * 1.0, 4.0 - k * 1.0, 0.6), loc=(0, 0, 0.3 + k * 0.6), key='stone_dark' if k % 2 == 0 else 'stone', bev=0.05)
    o = box(nm('v'), (0.9, 0.7, 9.0), loc=(0, 0, 6.3), key='stone_light', bev=0.06)
    box(nm('h'), (4.2, 0.7, 0.9), loc=(0, 0, 8.4), key='stone_light', bev=0.06)
    torus(nm('ring'), 1.5, 0.22, loc=(0, 0, 8.4), key='stone_light', segs=24, rsegs=5, rot=(90, 0, 0))
    for zz in (3.2, 4.6, 6.0):
        lbox(F(0, -0.36, 0, 0), (0.7, 0.06, 0.25), 0, 0, zz, 'stone')
    cyl(nm('boss'), 0.45, 0.25, loc=(0, -0.35, 8.4), key='stone', verts=12, rot=(90, 0, 0))
    _moss(o, 0.4, 6)
    return finalize('stone_cross', smooth_angle=25)


def mausoleum():
    """D17 - small classical crypt: columned porch, pediment, iron grille door, weathered stone and ivy."""
    reset()
    W, D, H = 12.0, 14.0, 9.0
    box(nm('m'), (W, D, H), loc=(0, 1.5, H / 2 + 1.0), key='stone_light')
    box(nm('mp'), (W + 3, D + 5, 1.0), loc=(0, 0.0, 0.5), key='stone_dark', bev=0.06)
    band(0, 1.5, W, D, H + 0.6, 0.8, 'stone', out=0.35)
    gable_roof(F(0, 1.5, 0, 90), D, W, H + 1.4, 3.2, keys=('stone', 'stone_dark'), wall='stone_light', ov=0.5, ovg=0.4, barge='stone', ridge='stone')
    for x in (-4.4, -1.5, 1.5, 4.4):
        if abs(x) < 2:
            continue
        column_c(x, -D / 2 - 1.4, 1.0, H, 0.5, key='stone_light', base='stone')
    for x in (-1.5, 1.5):
        column_c(x, -D / 2 - 1.4, 1.0, H, 0.5, key='stone_light', base='stone') if False else None
    fo = F(0, 1.5 - D / 2, 0, 0)
    lbox(fo, (4.0, 0.2, 6.0), 0, -0.05, 4.0, 'hole')
    for i in range(7):
        lbox(fo, (0.12, 0.12, 6.0), -1.8 + i * 0.6, -0.2, 4.0, 'iron_dark')
    for zz in (1.4, 4.0, 6.8):
        lbox(fo, (4.0, 0.12, 0.15), 0, -0.2, zz, 'iron_dark')
    for i in range(7):
        lathe(nm('sp'), [(0, 0), (0.12, 0), (0, 0.5)], loc=fo.p(-1.8 + i * 0.6, -0.2, 7.0), key='iron_dark', segs=4)
    lbox(fo, (5.0, 0.6, 0.8), 0, -0.3, 7.6, 'stone')
    lbox(fo, (3.6, 0.1, 0.6), 0, -0.65, 7.6, 'stone_dark')
    o = box(nm('por'), (W + 1.0, 3.0, 1.0), loc=(0, -D / 2 - 0.4, H + 1.5), key='stone')
    pediment(F(0, -D / 2 - 1.9, 0, 0), 0, H + 2.0, W + 1.0, 3.2, 3.0, key='stone', tymp='stone_light', emblem=None)
    for k in range(3):
        box(nm('st'), (6.0, 1.0, 0.33), loc=(0, -D / 2 - 2.6 - (2 - k) * 0.8 + 0.8, 0.17 + k * 0.33 + 0.5), key='stone')
    _moss(o, 0.4, 7)
    ivy(W / 2 - 4, W / 2 + 0.5, 1.5 - D / 2 - 0.1, 1.0, 8.0, 30, 7)
    for s in (-1, 1):
        lathe(nm('urn'), [(0, 0), (0.5, 0), (0.3, 0.3), (0.7, 0.9), (0.5, 1.4), (0, 1.5)], loc=(s * (W / 2 + 0.2), -D / 2 - 1.6, H + 2.0), key='stone', segs=10)
    return finalize('mausoleum', smooth_angle=25)


def graveyard_gate():
    """D18 - graveyard iron gate: twin gates in stone pillars with a scrolled iron arch."""
    reset()
    W = 10.0
    for s in (-1, 1):
        o = box(nm('p'), (2.0, 2.0, 7.0), loc=(s * (W / 2 + 1.0), 0, 3.5), key='stone', bev=0.08)
        box(nm('pc'), (2.4, 2.4, 0.5), loc=(s * (W / 2 + 1.0), 0, 7.25), key='stone_light', bev=0.06)
        ball(nm('pb'), 0.7, loc=(s * (W / 2 + 1.0), 0, 8.1), key='stone_light', segs=10, rings=7)
        _moss(o, 0.5, 8 + s)
        f = F(s * W / 4, 0, 0, 0)
        hw = W / 2 - 0.2
        lbox(f, (hw, 0.15, 0.15), 0, 0, 0.6, 'iron_dark')
        lbox(f, (hw, 0.15, 0.15), 0, 0, 5.4, 'iron_dark')
        lbox(f, (hw, 0.12, 0.12), 0, 0, 2.0, 'iron_dark')
        for i in range(9):
            x = -hw / 2 + 0.2 + i * (hw - 0.4) / 8
            top = 5.4 + 0.8 * math.cos((x / hw) * math.pi * 0.9) * (1 if s < 0 else 1)
            lbox(f, (0.08, 0.08, top - 0.4), x, 0, (top + 0.4) / 2, 'iron_dark')
            lathe(nm('spk'), [(0, 0), (0.13, 0), (0, 0.5)], loc=f.p(x, 0, top), key='iron_dark', segs=4)
        for k in range(3):
            scroll(nm('sc'), f.p(-hw / 2 + 0.6 + k * (hw - 1.2) / 2, 0, 1.3), 0.05, 0.4, 1.4, plane='XZ', key='iron_dark', radius=0.05)
    tube(nm('arch'), [(-W / 2, 0, 7.0), (-W / 4, 0, 9.4), (0, 0, 10.0), (W / 4, 0, 9.4), (W / 2, 0, 7.0)], 0.12, 'iron_dark', res=4)
    tube(nm('arch2'), [(-W / 2, 0, 7.0), (-W / 4, 0, 8.6), (0, 0, 9.0), (W / 4, 0, 8.6), (W / 2, 0, 7.0)], 0.1, 'iron_dark', res=4)
    for k in range(5):
        scroll(nm('as'), (-2.0 + k * 1.0, 0, 9.0), 0.04, 0.3, 1.3, plane='XZ', key='iron_dark', radius=0.05)
    lbox(F(), (0.12, 0.12, 2.0), 0, 0, 10.8, 'iron_dark')
    lbox(F(), (0.9, 0.12, 0.12), 0, 0, 11.3, 'iron_dark')
    return finalize('graveyard_gate', smooth_angle=30)


def weeping_statue():
    """D19 - weeping statue (original design): hooded mourning figure, head bowed, hands to face, on a mossy plinth."""
    reset()
    plinth(4.0, w=4.4, plaque=True)
    Z = 4.0
    lathe(nm('rb'), [(0.0, Z), (1.7, Z), (1.55, Z + 1.0), (1.1, Z + 4.0), (0.95, Z + 5.6), (1.15, Z + 6.6), (0.6, Z + 7.2), (0.0, Z + 7.2)], key='stone_light', segs=16, sy=0.8)
    for k in range(10):
        a = 2 * math.pi * k / 10
        tube(nm('fd'), [(math.cos(a) * 1.65, math.sin(a) * 1.3, Z + 0.1), (math.cos(a) * 1.05, math.sin(a) * 0.85, Z + 4.4)], 0.13, 'stone_light', res=4, taper=[1, 0.3])
    lathe(nm('hd'), [(0.0, 0.0), (0.75, 0.1), (0.85, 0.7), (0.7, 1.4), (0.2, 1.75), (0.0, 1.8)], loc=(0, -0.45, Z + 6.6), key='stone_light', segs=12, rot=(28, 0, 0))
    ball(nm('face'), 0.5, loc=(0, -0.95, Z + 7.0), key='stone', segs=10, rings=7)
    for s in (-1, 1):
        tube(nm('arm'), [(s * 1.0, 0, Z + 6.4), (s * 0.9, -0.8, Z + 5.4), (s * 0.35, -1.25, Z + 6.8)], 0.26, 'stone_light', res=6, taper=[1.0, 1.0, 0.9])
        ball(nm('hand'), 0.24, loc=(s * 0.25, -1.3, Z + 7.0), key='stone_light', segs=8, rings=6)
    from props import cloth
    cloth(nm('veil'), 2.6, 6.0, (0, 0.6, Z + 7.6), 'stone_light', waves=1.4, amp=0.15, seed=19)
    o = box(nm('mossb'), (5.2, 5.2, 0.05), loc=(0, 0, Z + 0.02), key='moss')
    ivy(-2.2, 2.2, -2.3, 0.6, 3.6, 18, 19)
    return finalize('weeping_statue', smooth_angle=35)


ITEMS_CHURCH = [
    ('D01_church', church), ('D02_church_bell', church_bell), ('D03_church_rose_window', church_rose_window),
    ('D04_church_tall_window', church_tall_window), ('D05_pew', pew), ('D06_altar', altar), ('D07_pulpit', pulpit),
    ('D08_pipe_organ', pipe_organ), ('D09_candle_stand', candle_stand), ('D10_church_pillar', church_pillar), ('D11_church_door', church_door),
]
ITEMS_GRAVE = [
    ('D12_gravestone_1', gravestone_1), ('D13_gravestone_2', gravestone_2), ('D14_gravestone_3', gravestone_3), ('D15_gravestone_4', gravestone_4),
    ('D16_stone_cross', stone_cross), ('D17_mausoleum', mausoleum), ('D18_graveyard_gate', graveyard_gate), ('D19_weeping_statue', weeping_statue),
]



# ============================================================ run-down town
from capital import house


def on_slope(cx, top, hr, D, x, y, size, key, lift=0.32, rot_extra=(0, 0, 0)):
    """Place a box lying on a side-gable roof slope (front slope when y<0)."""
    a = math.degrees(math.atan2(hr, D / 2))
    z = top + hr * (1 - abs(y) / (D / 2)) + lift
    rx = a if y < 0 else -a
    return box(nm('rs'), size, loc=(cx + x, y, z), key=key, rot=(rx + rot_extra[0], rot_extra[1], rot_extra[2]))


def roof_hole(cx, top, hr, D, x, y, w=3.0, l=2.4):
    on_slope(cx, top, hr, D, x, y, (w, l, 0.12), 'hole', lift=0.42)
    for k in range(3):
        on_slope(cx, top, hr, D, x - w / 2 + 0.4 + k * (w - 0.8) / 2, y, (0.3, l + 0.6, 0.3), 'wood_rot', lift=0.55)
    for k in range(3):
        o = on_slope(cx, top, hr, D, x + random.Random(k + int(x * 7)).uniform(-w / 2, w / 2), y + (l / 2 + 0.5) * (1 if y < 0 else -1) * (0.6 + 0.3 * k),
                     (1.4, 0.9, 0.18), random.choice(['roof_old', 'roof_old_b']), lift=0.6, rot_extra=(0, 0, 20 * k - 15))


def tin_patch(cx, top, hr, D, x, y, w=3.2, l=2.6, key='tin'):
    on_slope(cx, top, hr, D, x, y, (w, l, 0.1), key, lift=0.58)
    for k in range(int(w / 0.5)):
        on_slope(cx, top, hr, D, x - w / 2 + 0.25 + k * 0.5, y, (0.08, l, 0.08), key, lift=0.66)


def boards(f, x, z, w, h, seed=0):
    rnd = random.Random(seed)
    lbox(f, (w, 0.1, h), x, -0.05, z + h / 2, 'hole')
    for k in range(3):
        zz = z + h * (0.2 + 0.3 * k) + rnd.uniform(-0.2, 0.2)
        lbox(f, (w + 0.8, 0.15, 0.55), x + rnd.uniform(-0.2, 0.2), -0.35 - k * 0.02, zz, rnd.choice(['wood_old', 'wood_grey', 'wood_rot']), rot=(0, rnd.uniform(-14, 14), 0))
    if rnd.random() < 0.5:
        lbeam(f, (x - w / 2 - 0.2, -0.45, z), (x + w / 2 + 0.2, -0.45, z + h), 0.4, 'wood_old', 0.14)


def broken_shutter(f, x, z, h, key='wood_grey', side=1):
    lbox(f, (1.2, 0.12, h), x + side * 2.2, -0.6, z + h / 2 - 0.4, key, rot=(0, side * 18, side * 30))


def rundown(name, w=16, d=14, floors=2, upper='plaster_dirty', ground='stone', gtrim='stone_dark', timber=True, roof='side',
            rkeys=('roof_old', 'roof_old_b'), seed=0, holes=((2, -3),), tins=((-4, -2),), board_list=((0, 0), (1, 1)), lean=0.0, ivy_side=-1, door_bay=None):
    reset()
    rnd = random.Random(seed)
    gh, fh = 8.0, 7.0
    top = house(w=w, d=d, floors=floors, gh=gh, fh=fh, ground=ground, ground_trim=gtrim, upper=upper, timber=timber, jetty=0.0, roof=roof,
                rkeys=rkeys, shutter=None, flowers=None, seed=seed, dormers=0 if roof == 'side' else 0, frame_key='wood_old', door_bay=door_bay, pitch=0.45)
    nb = max(2, round(w / 6.2))
    xs = [-w / 2 + w * (i + 0.5) / nb for i in range(nb)]
    fo = faces(0, 0, w, d)['front']
    for (k, i) in board_list:
        if i < len(xs):
            z = gh + (k - 1) * fh + 1.6 if k >= 1 else 1.8
            hh = 3.7 if k >= 1 else 4.4
            boards(fo, xs[i], z, 2.4, hh, seed + k * 3 + i)
    broken_shutter(fo, xs[-1], gh + 1.6, 3.7, side=1)
    if roof == 'side':
        hr = d * 0.45
        for (x, y) in holes:
            roof_hole(0, top, hr, d, x, y)
        for (x, y) in tins:
            tin_patch(0, top, hr, d, x, y, key=rnd.choice(['tin', 'tin_b']))
    else:
        hr = w * 0.45 * 1.15
        for (x, y) in tins:
            box(nm('tp'), (3.0, 0.1, 2.6), loc=(w * 0.25, y, top + hr * 0.5 + 0.5), key='tin', rot=(0, -math.degrees(math.atan2(hr, w / 2)) * 1, 0))
    ivy(-w / 2 + 0.5, -w / 2 + 5, -d / 2 - 0.05, 0.3, gh + 5, 45, seed)
    for k in range(9):
        ball(nm('st'), rnd.uniform(0.5, 0.9), loc=(rnd.uniform(-w / 2 + 0.6, w / 2 - 0.6), -d / 2 - 0.02, rnd.uniform(gh, top - 1.5)), key='wood_rot', segs=6, rings=6,
             scale=(0.7, 0.05, 2.6))
    if lean:
        lbeam(F(), (w / 2 + 3.0, -2.0, 0.0), (w / 2 + 0.2, -2.0, gh + 2.0), 0.6, 'wood_rot')
    return finalize(name, smooth_angle=30)


def rundown_house_1():
    """D20 - run-down two-storey timber house: roof hole, tin patch, boarded windows, ivy."""
    return rundown('rundown_house_1', seed=201)


def rundown_house_2():
    """D21 - run-down tall stone-and-plaster house with a street gable, boarded ground floor, prop beam."""
    return rundown('rundown_house_2', w=13, d=13, floors=3, upper='plaster_stain', timber=False, roof='front', rkeys=('roof_old_b', 'roof_old'),
                   seed=202, board_list=((0, 0), (1, 0), (2, 1)), tins=((0, -2),), lean=1.0)


def rundown_house_3():
    """D22 - run-down wide brick house with two roof holes and patched tin."""
    return rundown('rundown_house_3', w=20, d=14, floors=2, upper='brick', timber=False, ground='stone_dark', gtrim='stone',
                   seed=203, holes=((-5, -3), (5, 2.5)), tins=((1, -2.5), (-3, 3)), board_list=((1, 0), (1, 2), (0, 2)))


def rundown_house_4():
    """D23 - run-down small cottage, sagging timber, one-and-a-half storeys, mostly boarded."""
    return rundown('rundown_house_4', w=12, d=12, floors=2, upper='plaster_dirty', seed=204, holes=((-2, 2.0),), tins=((2, -2.0),),
                   board_list=((0, 1), (1, 0), (1, 1)))


def jagged_wall(f, x0, x1, h0, h1, t, key, seed, z0=0.0):
    rnd = random.Random(seed)
    n = 8
    pts = [(x0, 0, z0), (x1, 0, z0)]
    for i in range(n, -1, -1):
        x = x0 + (x1 - x0) * i / n
        hh = h0 + (h1 - h0) * i / n + rnd.uniform(-1.4, 1.0)
        pts.append((x, 0, z0 + max(0.8, hh)))
    o = lslab(f, pts, (0, t, 0), key)
    return o


def collapsed_ruin():
    """D24 - collapsed house ruin: broken stone walls, a fallen roof frame, rubble and weeds."""
    reset()
    rnd = random.Random(24)
    w, d = 16.0, 14.0
    fs = faces(0, 0, w, d)
    jagged_wall(fs['front'], -w / 2, w / 2, 9.0, 3.0, 1.0, 'stone', 1)
    jagged_wall(fs['left'], -d / 2, d / 2, 2.5, 11.0, 1.0, 'stone', 2)
    jagged_wall(fs['back'], -w / 2, w / 2, 12.0, 6.0, 1.0, 'stone', 3)
    jagged_wall(fs['right'], -d / 2, -1.0, 4.0, 2.0, 1.0, 'stone', 4)
    for fr, L in ((fs['front'], w), (fs['back'], w)):
        lslab(fr, [(px * 0.6, -0.02, pz * 0.6 + 1.5) for px, pz in lancet_pts(-L / 4 / 0.6, 0, 2.6, 2.4)], (0, -0.05, 0), 'hole') if False else \
            lbox(fr, (2.4, 1.2, 3.6), -L / 4, 0.5, 3.4, 'hole')
    for k, fr in enumerate(fs.values()):
        stone_face(fr, -6, 6, 0.5, 3.0, 12, 240 + k, keys=('stone', 'stone_dark', 'stone_light'))
    for i in range(5):
        y = -d / 2 + 2 + i * 2.6
        o = lbeam(F(), (-w / 2 + 0.5, y, 10.0 - i * 1.6 if i < 3 else 0.6), (w / 2 - 3.0, y + rnd.uniform(-1, 1), 0.4), 0.45, 'wood_rot')
    lbeam(F(), (-w / 2 + 0.5, -d / 2 + 1.0, 9.0), (-w / 2 + 0.5, d / 2 - 1.0, 11.0), 0.55, 'wood_rot')
    for i in range(40):
        x, y = rnd.uniform(-w / 2, w / 2 + 4), rnd.uniform(-d / 2, d / 2)
        ball(nm('rb'), rnd.uniform(0.3, 0.9), loc=(x, y, 0.2), key=rnd.choice(['stone', 'stone_dark', 'stone_light']), segs=6, rings=4, scale=(1.3, 1, 0.6))
    for i in range(14):
        box(nm('tl'), (1.0, 0.7, 0.1), loc=(rnd.uniform(-w / 2, w / 2), rnd.uniform(-d / 2, d / 2), 0.3), key=rnd.choice(['roof_old', 'roof_old_b']),
            rot=(rnd.uniform(-20, 20), rnd.uniform(-20, 20), rnd.uniform(0, 180)))
    from roads import tuft
    for i in range(20):
        tuft(nm('tf'), rnd.uniform(-w / 2, w / 2), rnd.uniform(-d / 2, d / 2), 0.0, rnd)
    ivy(-w / 2, -w / 2 + 6, -d / 2 - 0.05, 0.3, 7.0, 40, 24)
    return finalize('collapsed_ruin', smooth_angle=25)


def tankard_sign(f, x, z):
    lbeam(f, (x, -0.1, z), (x, -2.6, z), 0.16, 'rust')
    lbox(f, (0.16, 1.9, 1.4), x, -1.6, z - 1.3, 'wood_old', rot=(0, 0, 0))
    lathe(nm('tk'), [(0, 0), (0.45, 0), (0.45, 0.9), (0.5, 1.0), (0, 1.0)], loc=f.p(x, -1.6, z - 1.8), key='brass', segs=10)
    torus(nm('tkh'), 0.25, 0.06, loc=f.p(x, -1.1, z - 1.3), key='brass', segs=10, rsegs=4, rot=f.r(0, 90, 0))
    for yy in (-1.0, -2.2):
        lbox(f, (0.05, 0.05, 0.4), x, yy, z - 0.3, 'rust')


def rundown_tavern():
    """D25 - run-down tavern: big timber house, still lit, porch with barrels, tankard sign and a patched roof."""
    reset()
    w, d = 22.0, 16.0
    top = house(w=w, d=d, floors=2, gh=8.0, fh=7.5, ground='stone', ground_trim='stone_dark', upper='plaster_dirty', timber=True, jetty=0.5,
                roof='side', rkeys=('roof_old', 'roof_old_b'), shutter='wood_grey', flowers=None, seed=25, dormers=2, frame_key='wood_old',
                door_bay=1, lit={(0, 0), (0, 1), (0, 3)}, pitch=0.45)
    dd = d + 1.0
    tin_patch(0, top, dd * 0.45, dd, -6, -3.0)
    tin_patch(0, top, dd * 0.45, dd, 5, -2.0, key='tin_b')
    fo = faces(0, 0, w, d)['front']
    nb = 4
    xs = [-w / 2 + w * (i + 0.5) / nb for i in range(nb)]
    tankard_sign(fo, xs[1] + 2.8, 7.4)
    boards(fo, xs[3], 1.8, 2.4, 4.4, 25)
    lbox(fo, (14.0, 4.0, 0.4), -3.0, -2.0, 0.2, 'wood_old')
    for x in (-9.8, -3.0, 3.8):
        lbox(fo, (0.45, 0.45, 6.6), x, -3.8, 3.5, 'wood_rot')
    lslab(fo, [(-10.4, 0.0, 7.4), (4.4, 0.0, 7.4), (4.4, -4.4, 6.4), (-10.4, -4.4, 6.4)], (0, 0, 0.25), 'tin')
    from props import barrel_body
    for i, (x, y) in enumerate(((-8.0, -2.6), (-6.6, -2.4))):
        barrel_body(nm('br'), loc=fo.p(x, y, 0.4), h=3.0)
    box(nm('bn'), (4.0, 1.0, 0.25), loc=fo.p(-1.0, -2.8, 2.0), key='wood_old')
    for s in (-1, 1):
        box(nm('bl'), (0.25, 0.8, 1.6), loc=fo.p(-1.0 + s * 1.7, -2.8, 1.2), key='wood_rot')
    return finalize('rundown_tavern', smooth_angle=30)


def blacksmith_shed():
    """D26 - rusty blacksmith shed: open timber lean-to with corrugated tin roof, glowing forge, chimney, anvil and tools."""
    reset()
    W, D = 16.0, 10.0
    box(nm('fl'), (W, D, 0.3), loc=(0, 0, 0.15), key='dirt')
    box(nm('bw'), (W, 0.6, 8.0), loc=(0, D / 2 - 0.3, 4.0), key='stone')
    stone_face(F(0, D / 2 - 0.6, 0, 0), -W / 2, W / 2, 0.5, 7.5, 30, 26, keys=('stone', 'stone_dark', 'stone_light'))
    for x in (-W / 2 + 0.3, 0, W / 2 - 0.3):
        box(nm('post'), (0.5, 0.5, 6.0), loc=(x, -D / 2 + 0.4, 3.0), key='wood_rot')
    box(nm('bm'), (W, 0.5, 0.5), loc=(0, -D / 2 + 0.4, 6.0), key='wood_rot')
    a = math.degrees(math.atan2(2.0, D))
    rnd = random.Random(26)
    for i in range(8):
        x = -W / 2 + W * (i + 0.5) / 8
        o = box(nm('tin'), (W / 8 + 0.2, D + 1.6, 0.1), loc=(x, 0, 7.15 + rnd.uniform(-0.05, 0.05)), key=rnd.choice(['tin', 'tin_b', 'tin']), rot=(-a, rnd.uniform(-1, 1), 0))
        for k in range(4):
            box(nm('cr'), (0.08, D + 1.6, 0.08), loc=(x - W / 16 + 0.25 + k * W / 32, 0, 7.22), key='tin_b', rot=(-a, 0, 0))
    box(nm('fg'), (5.0, 3.6, 3.0), loc=(-4.0, D / 2 - 2.4, 1.5), key='stone_dark', bev=0.08)
    box(nm('fgt'), (4.0, 2.6, 0.2), loc=(-4.0, D / 2 - 2.4, 3.05), key='hole')
    for i in range(14):
        ball(nm('co'), rnd.uniform(0.2, 0.35), loc=(-4.0 + rnd.uniform(-1.6, 1.6), D / 2 - 2.4 + rnd.uniform(-1.0, 1.0), 3.2), key=rnd.choice(['glow', 'flame', 'iron_dark']),
             segs=6, rings=4)
    box(nm('hood'), (4.6, 3.0, 2.0), loc=(-4.0, D / 2 - 2.0, 6.0), key='brick')
    box(nm('chm'), (2.0, 2.0, 10.0), loc=(-4.0, D / 2 - 1.4, 9.0), key='brick')
    box(nm('chc'), (2.4, 2.4, 0.4), loc=(-4.0, D / 2 - 1.4, 14.1), key='stone_dark')
    lathe(nm('bel'), [(0, 0), (0.9, 0), (1.2, 0.3), (0.2, 0.8), (0, 0.8)], loc=(-0.6, D / 2 - 2.4, 1.6), key='wood_old', segs=4, rot=(0, 90, 0))
    lathe(nm('st'), [(0, 0), (0.9, 0), (0.8, 2.0), (0, 2.0)], loc=(3.0, -0.5, 0.3), key='wood_rot', segs=10)
    box(nm('an'), (2.4, 1.0, 0.6), loc=(3.0, -0.5, 2.6), key='steel', bev=0.05)
    cyl(nm('ah'), 0.4, 1.6, loc=(4.2, -0.5, 2.7), key='steel', verts=10, r2=0.05, rot=(0, 90, 0))
    box(nm('aw'), (0.8, 0.7, 0.5), loc=(3.0, -0.5, 2.1), key='steel')
    for k in range(5):
        x = 2.0 + k * 1.0
        lbox(F(0, D / 2 - 0.6, 0, 180), (0.1, 0.1, 2.0), -x, -0.15, 4.5, 'wood_old')
        lbox(F(0, D / 2 - 0.6, 0, 180), (0.5 if k % 2 else 0.3, 0.15, 0.4), -x, -0.2, 3.5, 'iron')
    from props import barrel_body
    barrel_body(nm('wb'), loc=(6.4, -2.6, 0.3), h=2.6, open_top=True)
    for i in range(6):
        cyl(nm('bar'), 0.1, 3.0, loc=(W / 2 - 1.0, D / 2 - 1.0 - i * 0.3, 0.3), key='rust', verts=6, rot=(rnd.uniform(-15, 15), rnd.uniform(-20, -10), 0))
    return finalize('blacksmith_shed', smooth_angle=25)


def sail(cx, cz, ang, L=14.0, broken=False, torn=False, seed=0):
    rnd = random.Random(seed)
    a = math.radians(ang)
    d = Vector((math.cos(a), 0, math.sin(a)))
    p = Vector((math.cos(a + math.pi / 2), 0, math.sin(a + math.pi / 2)))
    hub = Vector((cx, -3.4, cz))
    L2 = L * (0.55 if broken else 1.0)
    beam3(hub, hub + d * L2, 0.4, 0.4, 'wood_rot')
    for k in range(1, int(L2 / 1.6) + 1):
        q = hub + d * (k * 1.6)
        beam3(q, q + p * 2.4, 0.15, 0.15, 'wood_old')
    beam3(hub + d * 1.6 + p * 2.4, hub + d * L2 + p * 2.4, 0.15, 0.15, 'wood_old')
    if not broken:
        for k in range(int(L2 / 1.6)):
            if torn and rnd.random() < 0.5:
                continue
            q = hub + d * (1.6 + k * 1.6) + p * 1.2
            o = box(nm('cv'), (1.5, 0.05, 2.2), loc=q + Vector((0, -0.05, 0)), key=rnd.choice(['canvas', 'canvas_b']), rot=(0, -ang, 0))
            if torn:
                o.scale = (1.0, 1.0, rnd.uniform(0.4, 0.9))
    else:
        beam3(hub + d * L2, hub + d * L2 + Vector((0.6, -0.4, -1.8)), 0.35, 0.35, 'wood_rot')


def broken_windmill():
    """D27 - broken windmill: tapered stone tower, crooked cap roof, one snapped sail, one torn, boarded door."""
    reset()
    H = 26.0
    lathe(nm('tw'), [(0.0, 0.0), (7.0, 0.0), (6.8, 1.0), (5.0, H), (0.0, H)], key='stone', segs=16)
    for zz in (1.0, 12.0):
        lathe(nm('bd'), [(0.0, zz - 0.25), (7.2 - zz * 0.075, zz - 0.25), (7.2 - zz * 0.075, zz + 0.25), (0.0, zz + 0.25)], key='stone_dark', segs=16)
    rnd = random.Random(27)
    for i in range(60):
        a = rnd.uniform(0, 2 * math.pi); z = rnd.uniform(1.5, H - 1)
        r = 7.0 - (z / H) * 2.0
        box(nm('sb'), (0.25, rnd.choice([1.2, 1.8]), 0.8), loc=(math.cos(a) * r, math.sin(a) * r, z), key=rnd.choice(['stone_dark', 'stone_light']), rot=(0, 0, math.degrees(a)))
    fo = F(0, -6.85, 0, 0)
    boards(fo, 0, 0.3, 2.8, 5.6, 27)
    for zz in (9.0, 17.0):
        window(F(0, -(7.0 - zz / H * 2.0) - 0.05, 0, 0), 0, zz, w=1.6, h=2.6, arch=True, frame='wood_old', sill='stone_dark', panes=False)
    o = lathe(nm('cap'), [(0.0, 0.0), (5.6, 0.0), (5.2, 2.0), (3.6, 4.6), (0.0, 6.0)], loc=(0, 0, H), key='wood_grey', segs=12, rot=(6, -4, 0), sy=1.2)
    roof_hole_pts = None
    box(nm('ch'), (2.4, 0.15, 1.6), loc=(1.8, -4.4, H + 2.4), key='hole', rot=(30, 0, 10))
    box(nm('ax'), (1.2, 4.0, 1.2), loc=(0, -3.0, H + 1.6), key='wood_rot')
    sail(0, H + 1.6, 40, seed=1)
    sail(0, H + 1.6, 130, broken=True, seed=2)
    sail(0, H + 1.6, 220, torn=True, seed=3)
    sail(0, H + 1.6, 310, torn=True, seed=4)
    lbeam(F(), (0.6, -6.0, 0.2), (5.0, -9.5, 0.4), 0.4, 'wood_rot')
    return finalize('broken_windmill', smooth_angle=25)


def rusty_water_tower():
    """D28 - rusty water tower: banded tin tank with a cone lid on braced timber legs, ladder and a leak."""
    reset()
    H, R = 16.0, 5.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            beam3((sx * 4.6, sy * 4.6, 0), (sx * 3.6, sy * 3.6, H), 0.7, 0.7, 'wood_rot')
            cyl(nm('ft'), 0.9, 0.6, loc=(sx * 4.6, sy * 4.6, 0), key='stone', verts=8)
    for z0, z1 in ((1.0, 8.0), (8.0, 15.0)):
        for (a, b) in (((-1, -1), (1, -1)), ((1, -1), (1, 1)), ((1, 1), (-1, 1)), ((-1, 1), (-1, -1))):
            t0 = z0 / H; t1 = z1 / H
            r0 = 4.6 - t0; r1 = 4.6 - t1
            beam3((a[0] * r0, a[1] * r0, z0), (b[0] * r1, b[1] * r1, z1), 0.3, 0.3, 'wood_old')
            beam3((a[0] * r0, a[1] * r0, z0), (a[0] * r0 + (b[0] - a[0]) * r0, a[1] * r0 + (b[1] - a[1]) * r0, z0), 0.35, 0.35, 'wood_old')
    box(nm('dk'), (9.0, 9.0, 0.5), loc=(0, 0, H + 0.25), key='wood_old')
    lathe(nm('tk'), [(0.0, H + 0.5), (R, H + 0.5), (R, H + 8.5), (0.0, H + 8.5)], key='tin', segs=24)
    for zz in (H + 1.2, H + 3.6, H + 6.0, H + 8.2):
        torus(nm('hp'), R + 0.06, 0.1, loc=(0, 0, zz), key='rust', segs=24, rsegs=4)
    rnd = random.Random(28)
    for i in range(10):
        a = rnd.uniform(0, 2 * math.pi)
        box(nm('rp'), (0.08, rnd.uniform(1, 2.4), rnd.uniform(0.8, 2.6)), loc=(math.cos(a) * (R + 0.02), math.sin(a) * (R + 0.02), H + rnd.uniform(1.5, 7.5)),
            key=rnd.choice(['rust', 'tin_b']), rot=(0, 0, math.degrees(a)))
    lathe(nm('lid'), [(0.0, H + 8.5), (R + 0.4, H + 8.5), (0.0, H + 11.5)], key='tin_b', segs=24)
    lbeam(F(), (0.0, -R - 0.6, 0.0), (0.0, -R - 0.6, H + 9.0), 0.15, 'rust')
    lbeam(F(), (1.2, -R - 0.6, 0.0), (1.2, -R - 0.6, H + 9.0), 0.15, 'rust')
    for k in range(int((H + 9) / 1.0)):
        lbeam(F(), (0.0, -R - 0.6, 0.5 + k), (1.2, -R - 0.6, 0.5 + k), 0.08, 'rust')
    cyl(nm('sp'), 0.3, 3.0, loc=(R - 0.4, 0, H - 2.5), key='rust', verts=8)
    tube(nm('drip'), [(R - 0.4, 0, H - 2.5), (R - 0.4, 0, 0.3)], 0.06, 'water_fx', res=4)
    cyl(nm('pd'), 1.2, 0.05, loc=(R - 0.4, 0, 0.02), key='water', verts=12)
    return finalize('rusty_water_tower', smooth_angle=25)


def patched_tent():
    """D29 - patched canvas tent: A-frame with mismatched patches, guy ropes, stakes and a bedroll."""
    reset()
    L, W, H = 10.0, 7.0, 5.5
    rnd = random.Random(29)
    for s in (-1, 1):
        lslab(F(), [(-L / 2, s * W / 2, 0.0), (L / 2, s * W / 2, 0.0), (L / 2, 0, H), (-L / 2, 0, H)], (0, 0, 0.08), 'canvas')
        for i in range(4):
            x = rnd.uniform(-L / 2 + 1, L / 2 - 1); t = rnd.uniform(0.2, 0.8)
            y = s * W / 2 * (1 - t); z = H * t
            a = math.degrees(math.atan2(H, W / 2))
            box(nm('pt'), (rnd.uniform(1.0, 1.8), rnd.uniform(0.9, 1.4), 0.04), loc=(x, y + s * 0.06, z + 0.06), key=rnd.choice(['canvas_b', 'fabric_red', 'fabric_blue', 'wood_grey']),
                rot=(-s * a, 0, rnd.uniform(-10, 10)))
    lslab(F(), [(L / 2, -W / 2, 0), (L / 2, W / 2, 0), (L / 2, 0, H)], (0.08, 0, 0), 'canvas_b')
    lslab(F(), [(-L / 2, -W / 2, 0), (-L / 2, -0.4, 0), (-L / 2, 0, H)], (-0.08, 0, 0), 'canvas')
    lslab(F(), [(-L / 2 - 1.2, 0.4, 0), (-L / 2 - 1.2, W / 2 - 1.0, 0), (-L / 2, 0, H)], (0, 0, 0.06), 'canvas')
    lbox(F(), (-0.0 + 0.0001, 0, 0), 0, 0, 0, 'hole') if False else None
    lslab(F(), [(-L / 2 + 0.02, -0.4, 0), (-L / 2 + 0.02, W / 2 - 0.6, 0), (-L / 2 + 0.02, 0, H - 0.5)], (0.05, 0, 0), 'hole')
    for x in (-L / 2 - 0.1, L / 2 + 0.1):
        cyl(nm('pl'), 0.15, H + 0.8, loc=(x, 0, 0), key='wood_old', verts=6)
    cyl(nm('rp'), 0.12, L + 0.4, loc=(-L / 2 - 0.2, 0, H), key='wood_old', verts=6, rot=(0, 90, 0))
    for x in (-L / 2 - 0.1, L / 2 + 0.1):
        for s in (-1, 1):
            tube(nm('gy'), [(x, 0, H + 0.6), (x + (1.8 if x > 0 else -1.8), s * 1.0, 0.2)], 0.04, 'rope', res=4)
            cyl(nm('stk'), 0.08, 0.7, loc=(x + (1.8 if x > 0 else -1.8), s * 1.0, -0.2), key='wood_rot', verts=5)
    for x in (-2.0, 2.0):
        for s in (-1, 1):
            tube(nm('gs'), [(x, s * (W / 2 - 0.6), 0.9), (x, s * (W / 2 + 1.6), 0.1)], 0.04, 'rope', res=4)
    cyl(nm('roll'), 0.5, 2.6, loc=(-L / 2 - 1.0, -W / 2 - 0.4, 0.5), key='fabric_green', verts=10, rot=(0, 90, 0))
    for k in range(3):
        torus(nm('rt'), 0.52, 0.04, loc=(-L / 2 - 0.3 + k * 0.9 - 0.4, -W / 2 - 0.4, 0.5), key='rope', segs=10, rsegs=3, rot=(0, 90, 0))
    return finalize('patched_tent', smooth_angle=25)


def scrap_pile():
    """D30 - scrap pile: rusty plates, pipes, a cart wheel, gears, broken crates and a bucket."""
    reset()
    rnd = random.Random(30)
    blob(nm('mound'), 3.6, (0, 0, -1.2), 'dirt', subdiv=2, amp=0.2, scale=(1.4, 1.1, 0.6), seed=30)
    for i in range(18):
        box(nm('pl'), (rnd.uniform(1.2, 3.0), rnd.uniform(1.0, 2.4), 0.1), loc=(rnd.uniform(-3.5, 3.5), rnd.uniform(-2.6, 2.6), rnd.uniform(0.3, 2.2)),
            key=rnd.choice(['tin', 'tin_b', 'rust', 'iron']), rot=(rnd.uniform(-40, 40), rnd.uniform(-40, 40), rnd.uniform(0, 180)))
    for i in range(7):
        cyl(nm('pp'), rnd.uniform(0.15, 0.35), rnd.uniform(2.5, 5.0), loc=(rnd.uniform(-3, 3), rnd.uniform(-2, 2), rnd.uniform(0.5, 2.0)), key=rnd.choice(['rust', 'iron']), verts=10,
            rot=(rnd.uniform(60, 120), 0, rnd.uniform(0, 180)))
    from props import wheel
    import bpy
    before = set(o.name for o in bpy.context.scene.objects)
    wheel(nm('wh'), 1.6, (1.4, -1.6, 1.8), axis='Y', key='wood_rot', spokes=8)
    for o in bpy.context.scene.objects:
        if o.name not in before:
            o.rotation_euler.x += math.radians(35)
    for k in range(3):
        r = rnd.uniform(0.6, 1.0)
        cx, cy, cz = rnd.uniform(-2.5, 2.5), rnd.uniform(-1.8, 1.8), rnd.uniform(1.2, 2.6)
        rot = (rnd.uniform(-50, 50), rnd.uniform(-50, 50), 0)
        torus(nm('gr'), r, 0.18, loc=(cx, cy, cz), key='rust', segs=16, rsegs=4, rot=rot)
        for t in range(8):
            a = 2 * math.pi * t / 8
            o = box(nm('gt'), (0.3, 0.3, 0.25), loc=(cx, cy, cz), key='rust', rot=rot)
            from mathutils import Matrix
            M = o.rotation_euler.to_matrix()
            off = M @ Vector((math.cos(a) * (r + 0.2), math.sin(a) * (r + 0.2), 0))
            o.location = Vector((cx, cy, cz)) + off
    for k in range(2):
        box(nm('cr'), (1.6, 1.6, 1.4), loc=(rnd.uniform(-3, -1), rnd.uniform(-1.5, 1.5), 0.6 + k * 0.3), key='wood_old', rot=(rnd.uniform(-15, 15), rnd.uniform(-25, 25), rnd.uniform(0, 90)))
    lathe(nm('bk'), [(0, 0), (0.5, 0), (0.62, 1.0), (0.55, 1.0), (0.44, 0.08), (0, 0.08)], loc=(3.2, 1.2, 0.6), key='tin_b', segs=10, rot=(70, 0, 30))
    return finalize('scrap_pile', smooth_angle=25)


def rusted_cart():
    """D31 - abandoned rusted cart: tipped on a missing wheel, broken planks, rusty iron fittings."""
    reset()
    from props import wheel
    rnd = random.Random(31)
    import bpy
    tilt = 14.0
    objs_before = set(o.name for o in bpy.context.scene.objects)
    for i in range(6):
        if i == 4:
            continue
        box(nm('pl'), (0.8, 3.6, 0.2), loc=(-2.4 + i * 0.9, 0, 2.2), key=rnd.choice(['wood_old', 'wood_grey']))
    for s in (-1, 1):
        box(nm('sd'), (5.4, 0.2, 1.0), loc=(0, s * 1.8, 2.8), key='wood_old')
        box(nm('st'), (5.4, 0.25, 0.15), loc=(0, s * 1.85, 3.3), key='rust')
    box(nm('ed'), (0.2, 3.6, 1.0), loc=(2.7, 0, 2.8), key='wood_grey', rot=(0, 25, 0))
    box(nm('ax'), (0.3, 4.4, 0.3), loc=(0.4, 0, 1.6), key='rust')
    for o in bpy.context.scene.objects:
        if o.name not in objs_before:
            o.rotation_euler.x += math.radians(tilt)
            o.location = Vector(o.location) + Vector((0, 0, -0.4))
            o.location.z += o.location.y * math.sin(math.radians(tilt)) * 0.0
    wheel(nm('wh'), 1.6, (0.4, -2.3, 1.6), axis='Y', key='wood_old', spokes=10)
    wheel(nm('wl'), 1.6, (2.2, 3.4, 0.25), axis='Z', key='wood_rot', spokes=10)
    for s in (-1, 1):
        lbeam(F(), (-2.7, s * 1.0, 1.9), (-6.2, s * 0.9, 0.2), 0.25, 'wood_rot')
    return finalize('rusted_cart', smooth_angle=25)


def broken_barrel():
    """D32 - broken barrel: burst staves splayed outward, fallen hoops and spilled contents."""
    reset()
    from props import hoop
    rnd = random.Random(32)
    n = 14
    for i in range(n):
        a = 2 * math.pi * i / n
        h = rnd.uniform(1.6, 3.6)
        lean = rnd.uniform(5, 40) if rnd.random() < 0.6 else 2
        x, y = math.cos(a) * 1.25, math.sin(a) * 1.25
        o = box(nm('sv'), (0.62, 0.16, h), loc=(x, y, h / 2 * math.cos(math.radians(lean))), key=rnd.choice(['wood', 'wood_old']), rot=(0, lean, math.degrees(a)))
        o.rotation_euler = (0, math.radians(lean), a)
        o.location = (x + math.cos(a) * math.sin(math.radians(lean)) * h / 2, y + math.sin(a) * math.sin(math.radians(lean)) * h / 2, h / 2 * math.cos(math.radians(lean)))
    cyl(nm('bt'), 1.2, 0.2, loc=(0, 0, 0), key='wood_old', verts=14)
    torus(nm('h1'), 1.4, 0.08, loc=(0.6, 0.3, 0.1), key='rust', segs=20, rsegs=4, rot=(8, 0, 0))
    torus(nm('h2'), 1.35, 0.08, loc=(-1.4, -1.2, 0.5), key='rust', segs=20, rsegs=4, rot=(60, 10, 0))
    for i in range(10):
        ball(nm('ap'), 0.25, loc=(rnd.uniform(0.6, 3.0), rnd.uniform(-1.0, 1.4), 0.2), key=rnd.choice(['fruit', 'bark']), segs=7, rings=5)
    box(nm('sv2'), (0.6, 0.16, 3.2), loc=(2.4, -1.6, 0.1), key='wood_old', rot=(0, 90, 30))
    return finalize('broken_barrel', smooth_angle=30)


def broken_fence():
    """D33 - broken fence section, 16 long: leaning posts, missing and snapped rails, weeds."""
    reset()
    rnd = random.Random(33)
    xs = [-8.0, -4.0, 0.0, 4.0, 8.0]
    tops = []
    for i, x in enumerate(xs):
        lean = (0, rnd.uniform(-12, 12), 0) if i in (1, 3) else (0, rnd.uniform(-3, 3), 0)
        h = 4.2 if i != 2 else 2.4
        o = box(nm('ps'), (0.45, 0.45, h), loc=(x, 0, h / 2), key=rnd.choice(['wood_old', 'wood_grey']), rot=lean)
        tops.append((x - math.sin(math.radians(lean[1])) * h * 0.5, h))
    for i in range(4):
        x0, x1 = xs[i], xs[i + 1]
        for z in (1.4, 3.2):
            r = rnd.random()
            if r < 0.25:
                continue
            if r < 0.5:
                box(nm('rb'), (2.2, 0.2, 0.35), loc=(x0 + 1.1, -0.3, z - 0.3), key='wood_grey', rot=(0, rnd.uniform(-25, 25), 0))
                box(nm('rf'), (2.0, 0.2, 0.35), loc=(x1 - 1.0 + rnd.uniform(-0.5, 0.5), -0.8, 0.15), key='wood_grey', rot=(0, 0, rnd.uniform(-30, 30)))
                continue
            box(nm('rl'), (4.2, 0.2, 0.35), loc=((x0 + x1) / 2, -0.3, z + rnd.uniform(-0.2, 0.2)), key=rnd.choice(['wood_old', 'wood_grey']), rot=(0, rnd.uniform(-4, 4), 0))
    from roads import tuft
    for i in range(12):
        tuft(nm('tf'), rnd.uniform(-8, 8), rnd.uniform(-0.8, 0.8), 0.0, rnd)
    return finalize('broken_fence', smooth_angle=25)


def boarded_shack():
    """D34 - boarded-up shack: grey plank walls, rusty tin lean-to roof, planks nailed over door and window."""
    reset()
    W, D, H = 10.0, 8.0, 7.0
    rnd = random.Random(34)
    box(nm('core'), (W - 0.4, D - 0.4, H), loc=(0, 0, H / 2), key='wood_rot')
    for side, L in (('front', W), ('back', W), ('left', D), ('right', D)):
        fr = faces(0, 0, W, D)[side]
        n = int(L / 0.9)
        for i in range(n):
            x = -L / 2 + L * (i + 0.5) / n
            hh = H - rnd.uniform(0, 0.4) + (0.8 if side == 'back' else 0) * 0
            lbox(fr, (L / n - 0.06, 0.2, hh), x, -0.1, hh / 2, rnd.choice(['wood_grey', 'wood_old', 'wood_grey']))
    fo = faces(0, 0, W, D)['front']
    boards(fo, -2.0, 0.2, 3.0, 6.0, 34)
    boards(fo, 2.6, 2.6, 2.2, 2.4, 35)
    for i in range(6):
        x = -W / 2 + W * (i + 0.5) / 6
        box(nm('tin'), (W / 6 + 0.25, D + 1.8, 0.1), loc=(x, 0, H + 0.7), key=rnd.choice(['tin', 'tin_b', 'rust']), rot=(-math.degrees(math.atan2(1.4, D)), rnd.uniform(-2, 2), 0))
    lbox(F(), (W + 0.4, 0.4, 0.4), 0, -D / 2 - 0.2, H + 1.3, 'wood_rot')
    cyl(nm('pipe'), 0.35, 4.0, loc=(W / 2 - 2.0, D / 4, H), key='rust', verts=10)
    lathe(nm('pc'), [(0, 0), (0.7, 0), (0, 0.6)], loc=(W / 2 - 2.0, D / 4, H + 4.0), key='rust', segs=10)
    ivy(-W / 2, -W / 2 + 3, -D / 2 - 0.25, 0.2, 4.0, 20, 34)
    return finalize('boarded_shack', smooth_angle=25)


def collapsed_wall():
    """D35 - collapsed wall section, 20 long: broken stone wall with a breach, rubble and moss."""
    reset()
    rnd = random.Random(35)
    f = F(0, -0.8, 0, 0)
    jagged_wall(f, -10.0, -2.5, 7.0, 3.0, 1.6, 'stone', 1)
    jagged_wall(f, 2.0, 10.0, 2.5, 6.5, 1.6, 'stone', 2)
    lbox(f, (4.5, 1.6, 0.8), 0, 0.8, 0.4, 'stone_dark')
    stone_face(F(0, -0.8, 0, 0), -10, -3, 0.3, 3.0, 14, 351, keys=('stone', 'stone_dark', 'stone_light'))
    stone_face(F(0, -0.8, 0, 0), 3, 10, 0.3, 2.5, 12, 352, keys=('stone', 'stone_dark', 'stone_light'))
    for i in range(36):
        x = rnd.gauss(0, 2.6); y = rnd.uniform(-3.5, 2.0)
        o = box(nm('rb'), (rnd.uniform(0.8, 1.6), rnd.uniform(0.6, 1.0), rnd.uniform(0.5, 0.9)), loc=(x, y, rnd.uniform(0.2, 0.8)), key=rnd.choice(['stone', 'stone_dark', 'stone_light']),
                rot=(rnd.uniform(-30, 30), rnd.uniform(-30, 30), rnd.uniform(0, 90)), bev=0.08)
    from roads import tuft
    for i in range(10):
        tuft(nm('tf'), rnd.uniform(-9, 9), rnd.uniform(-2.5, -1.2), 0.0, rnd)
    ivy(-10, -6, -0.85, 0.3, 4.5, 20, 35)
    return finalize('collapsed_wall', smooth_angle=25)


def old_well_pump():
    """D36 - old well with a rusty hand pump: cracked stone ring, broken little roof, rusty bucket."""
    reset()
    rnd = random.Random(36)
    R = 3.0
    for k in range(4):
        for i in range(14):
            if k == 3 and i in (3, 4):
                continue
            a = 2 * math.pi * (i + (k % 2) * 0.5) / 14
            box(nm('ws'), (1.3, 0.9, 0.85), loc=(math.cos(a) * R, math.sin(a) * R, 0.45 + k * 0.9), key=rnd.choice(['stone', 'stone_dark', 'stone_light']),
                rot=(0, rnd.uniform(-3, 3), math.degrees(a) + 90), bev=0.08)
    cyl(nm('wd'), R - 0.5, 0.05, loc=(0, 0, 1.2), key='water_dark', verts=16)
    lathe(nm('pb'), [(0, 0), (0.45, 0), (0.35, 0.4), (0.3, 3.4), (0.42, 3.6), (0.42, 4.0), (0, 4.0)], loc=(R + 1.4, 0, 0), key='rust', segs=10)
    tube(nm('sp'), [(R + 1.4, 0, 3.0), (R + 1.4, -0.9, 3.0), (R + 1.4, -1.1, 2.6)], 0.12, 'rust', res=4)
    tube(nm('hd'), [(R + 1.4, 0.2, 3.9), (R + 1.4, 1.2, 4.3), (R + 1.4, 2.4, 4.0)], 0.09, 'rust', res=4)
    lathe(nm('bk'), [(0, 0), (0.5, 0), (0.6, 1.0), (0.55, 1.0), (0.45, 0.1), (0, 0.1)], loc=(R + 1.4, -1.1, 0.0), key='tin_b', segs=12)
    for s in (-1, 1):
        lbox(F(), (0.4, 0.4, 7.0), s * (R - 0.2), 0, 3.5, 'wood_rot')
    lbox(F(), (2 * R + 0.4, 0.35, 0.35), 0, 0, 5.6, 'wood_rot')
    a = math.degrees(math.atan2(1.6, 2.4))
    box(nm('rf'), (2 * R + 1.6, 2.8, 0.15), loc=(0, -1.2, 7.4), key='roof_old', rot=(a, 0, 0))
    box(nm('rfb'), (3.0, 2.6, 0.15), loc=(-1.6, 1.3, 7.0), key='roof_old_b', rot=(-a + 10, -12, 4))
    box(nm('rff'), (2.4, 2.0, 0.15), loc=(R + 2.4, 2.2, 0.2), key='roof_old_b', rot=(4, 6, 30))
    lbox(F(), (0.25, 3.0, 0.25), 0.0, 0.0, 7.6, 'wood_rot')
    return finalize('old_well_pump', smooth_angle=25)


def crooked_lamp():
    """D37 - crooked old lamp post: bent leaning iron post, cracked lantern with one dark pane, flickering light."""
    reset()
    lathe(nm('b'), [(0, 0), (1.0, 0), (0.8, 0.5), (0.4, 1.0), (0, 1.0)], key='rust', segs=8)
    tube(nm('p'), [(0, 0, 1.0), (0.2, 0, 6.0), (0.9, 0, 11.0), (2.0, 0, 14.6)], 0.22, 'rust', res=4, ures=4)
    tube(nm('arm'), [(2.0, 0, 14.6), (2.7, 0, 15.2), (3.3, 0, 14.8)], 0.12, 'rust', res=4)
    x, z = 3.3, 13.0
    lathe(nm('lc'), [(0, 0), (0.4, 0), (0.5, 0.2), (0, 0.2)], loc=(x, 0, z), key='rust', segs=4)
    lathe(nm('lg'), [(0, 0.2), (0.5, 0.2), (0.6, 1.4), (0, 1.4)], loc=(x, 0, z), key='glass_lit', segs=4)
    lathe(nm('lt'), [(0, 1.4), (0.85, 1.4), (0.2, 2.0), (0, 2.2)], loc=(x, 0, z), key='rust', segs=4, rot=(0, 8, 0))
    box(nm('dp'), (0.05, 0.75, 1.1), loc=(x - 0.46, 0, z + 0.8), key='hole', rot=(0, 5, 45))
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        tube(nm('fr'), [(x + math.cos(a) * 0.48, math.sin(a) * 0.48, z + 0.2), (x + math.cos(a) * 0.58, math.sin(a) * 0.58, z + 1.4)], 0.05, 'rust', res=4)
    tube(nm('hk'), [(3.3, 0, 14.8), (3.3, 0, 15.2)], 0.05, 'rust', res=4)
    ivy(-0.6, 0.6, -0.3, 0.5, 4.0, 10, 37)
    return finalize('crooked_lamp', smooth_angle=30)


ITEMS_TOWN = [
    ('D20_rundown_house_1', rundown_house_1), ('D21_rundown_house_2', rundown_house_2), ('D22_rundown_house_3', rundown_house_3),
    ('D23_rundown_house_4', rundown_house_4), ('D24_collapsed_ruin', collapsed_ruin), ('D25_rundown_tavern', rundown_tavern),
    ('D26_blacksmith_shed', blacksmith_shed), ('D27_broken_windmill', broken_windmill), ('D28_rusty_water_tower', rusty_water_tower),
    ('D29_patched_tent', patched_tent), ('D30_scrap_pile', scrap_pile), ('D31_rusted_cart', rusted_cart), ('D32_broken_barrel', broken_barrel),
    ('D33_broken_fence', broken_fence), ('D34_boarded_shack', boarded_shack), ('D35_collapsed_wall', collapsed_wall),
    ('D36_old_well_pump', old_well_pump), ('D37_crooked_lamp', crooked_lamp),
]
