"""Worker wb - B07 capital avenue townhouses (6, all different) + B08 Town-1 Gothic church.
Builds on capital.house() and arch.py. 1 unit = 1 stud. Fronts face -Y. Houses 15-22 wide,
14-18 deep, 30-40 tall, each a different composition and roof colour. Church 35x85x75, not enterable.
"""
import math, random
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, top_paint, dup
from arch import (F, faces, lbox, lbeam, beam3, slab, lslab, half_disc, window, door, arrow_slit, quoins, band,
                  corbels, battlements, ring_battlements, timber_frame, gable_roof, roof_z, cone_roof, chimney,
                  dormer, railing, lancet, rose_window, column_c, pinnacle, pediment, dome, arc_pts, nm)
import capital
from capital import house, hanging_sign

P = kitlib.PAL
# worker town palette (wb_ prefix)
P['wb_slate_blue']  = ((64, 80, 112),  'Slate',        0.0, 0.72, 0)
P['wb_terra']       = ((178, 92, 56),   'Brick',       0.0, 0.84, 0)
P['wb_terra_b']     = ((156, 78, 50),   'Brick',       0.0, 0.86, 0)
P['wb_copper']      = ((96, 150, 128),  'CorrodedMetal',0.4, 0.55, 0)
P['wb_copper_dk']   = ((72, 122, 104),  'CorrodedMetal',0.4, 0.6, 0)
P['wb_slate_grey']  = ((88, 92, 100),   'Slate',       0.0, 0.76, 0)
P['wb_brownshingle']= ((120, 86, 56),   'WoodPlanks',  0.0, 0.85, 0)
P['wb_brownshingle_b']=((102, 72, 48),  'WoodPlanks',  0.0, 0.85, 0)
P['wb_slate_purple']= ((96, 78, 116),   'Slate',       0.0, 0.74, 0)
P['wb_slate_purple_b']=((80, 64, 100),  'Slate',       0.0, 0.76, 0)
P['wb_plaster_warm']= ((228, 206, 168), 'Plaster',     0.0, 0.90, 0)
P['wb_plaster_rose']= ((226, 196, 182), 'Plaster',     0.0, 0.90, 0)
P['wb_awning_a']    = ((178, 60, 56),   'Fabric',      0.0, 0.95, 0)
P['wb_awning_b']    = ((224, 216, 196), 'Fabric',      0.0, 0.95, 0)
P['wb_clock']       = ((234, 224, 198), 'SmoothPlastic',0.0, 0.5, 0)
P['wb_clock_face']  = ((40, 44, 56),    'SmoothPlastic',0.0, 0.45, 0)
P['wb_clock_hand']  = ((232, 206, 120), 'Metal',        0.9, 0.35, 0)
P['wb_bell']        = ((150, 110, 58),  'Metal',       0.9, 0.4, 0)
P['wb_stone_c']     = ((176, 168, 150), 'Limestone',   0.0, 0.85, 0)


# ---- small shared extras ----
def oriel(f, x, z, w=3.2, h=5.0, proj=1.8, key='wb_plaster_warm', roofk='wb_slate_blue', frame='wood_paint'):
    """Projecting oriel bay window."""
    lbox(f, (w, proj, h), x, -proj / 2, z + h / 2, key)
    # corbel bracket under it
    for s in (-1, 1):
        lbeam(f, (x + s * w * 0.35, -0.1, z - 0.2), (x + s * w * 0.35, -proj, z + 0.6), 0.3, key)
    lbeam(f, (x, -0.1, z - 0.3), (x, -proj, z + 0.5), 0.3, key)
    for face_x, fr in ((0, F(*f.p(x, -proj, z), f.rz)),):
        window(fr, 0, 0.8, w=w * 0.6, h=h - 1.6, frame=frame, sill=frame, panes=True)
    for s in (-1, 1):
        frs = F(*f.p(x + s * w / 2, -proj / 2, z), f.rz + s * 90)
        window(frs, 0, 0.8, w=proj * 0.55, h=h - 1.8, frame=frame, sill=frame, panes=True)
    # little lead hip roof on the oriel
    lathe(nm('or'), [(0.0, 0.0), (w * 0.62, 0.0), (0.0, 2.0)], loc=f.p(x, -proj / 2, z + h), key=roofk, segs=4)


def stepped_gable(f, w, z0, hr, key='wb_stone_c', steps=5):
    """Crow-stepped gable on the front face (local)."""
    sh = hr / steps
    sw = w / (steps * 2 - 1)
    for i in range(steps):
        gw = w - 2 * sw * i
        lbox(f, (gw, 0.8, sh + 0.4), 0, -0.4, z0 + sh * i + sh / 2, key, bev=0.05)
        for s in (-1, 1):
            lbox(f, (sw, 1.0, 0.5), s * (gw / 2 - sw / 2), -0.5, z0 + sh * (i + 1), key, bev=0.05)


def awning(f, x, z, w, keys=('wb_awning_a', 'wb_awning_b')):
    seg = max(4, int(w / 1.1))
    for i in range(seg):
        xx = x - w / 2 + w * (i + 0.5) / seg
        lbox(f, (w / seg + 0.02, 2.2, 0.16), xx, -1.1, z, keys[i % 2], rot=(-26, 0, 0))
    lbox(f, (w + 0.3, 0.2, 0.3), x, -0.1, z + 0.5, 'wood_dark')
    # scalloped valance
    for i in range(seg):
        xx = x - w / 2 + w * (i + 0.5) / seg
        ball(nm('vl'), 0.28, loc=f.p(xx, -2.05, z - 0.95), key=keys[i % 2], segs=7, rings=4, scale=(1, 0.5, 1))


# ======================================================= B07 capital houses
def cap_house_1():
    """01 tall narrow 4-storey stone house, oriel window, stepped gable, blue slate."""
    reset()
    w, d = 15.0, 14.0
    top = house(w=w, d=d, floors=4, gh=8.0, fh=7.0, ground='ashlar', ground_trim='castle_trim', upper='wb_plaster_warm',
                timber=False, jetty=0.0, roof='front', rkeys=('wb_slate_blue', 'tile_b'), shutter='shutter_b',
                flowers=('fl_blue', 'fl_white'), dormers=0, seed=71, frame_key='wood_paint', pitch=0.5, chim=True)
    fc = faces(0, 0, w, d, 0)
    oriel(fc['front'], 0, 16.0, w=4.0, h=6.0, proj=2.0, key='wb_plaster_warm', roofk='wb_slate_blue')
    stepped_gable(F(0, -d / 2, top, 0), w + 0.4, 0, w * 0.5, key='ashlar', steps=5)
    stepped_gable(F(0, d / 2, top, 180), w + 0.4, 0, w * 0.5, key='ashlar', steps=5)
    return finalize('B07_01_capital_house_01', smooth_angle=30)


def cap_house_2():
    """02 wide merchant house, ground-floor arcade, three dormers, terracotta roof."""
    reset()
    w, d = 22.0, 15.0
    # custom ground arcade instead of plain shopfront
    gh = 8.5
    box(nm('g'), (w, d, gh), loc=(0, 0, gh / 2), key='ashlar')
    box(nm('pl'), (w + 0.4, d + 0.4, 1.0), loc=(0, 0, 0.5), key='stone_dark', bev=0.06)
    fc0 = faces(0, 0, w, d)
    narc = 4
    for i in range(narc):
        x = -w / 2 + w * (i + 0.5) / narc
        # arcade arch openings
        half_disc(fc0['front'], x, 5.0, w / narc / 2 - 0.6, 0.0, 0.8, 'hole')
        lbox(fc0['front'], (w / narc - 1.2, 0.8, 5.0), x, -0.1, 2.5, 'hole')
        column_c(x - w / narc / 2 + 0.4, -d / 2 + 0.3, 0, gh - 0.3, 0.6, key='castle_trim', base='castle_trim')
    column_c(w / 2 - 0.4, -d / 2 + 0.3, 0, gh - 0.3, 0.6, key='castle_trim', base='castle_trim')
    band(0, 0, w, d, gh - 0.2, 0.5, 'castle_trim', out=0.2)
    # upper storeys via house() stacked on top by building a 2-floor block manually
    top = gh
    for k in range(2):
        box(nm('u'), (w, d, 7.0), loc=(0, 0, top + 3.5), key='wb_plaster_rose')
        fk = faces(0, 0, w, d, top)
        band(0, 0, w, d, top - 0.05, 0.3, 'castle_trim', out=0.1)
        for i in range(5):
            x = -w / 2 + w * (i + 0.5) / 5
            for side in ('front', 'back'):
                window(fk[side], (x if side == 'front' else -x), 1.6, w=2.2, h=3.8, frame='wood_paint',
                       shutter='shutter_r', sill='castle_trim', lit=(k == 0 and i == 2 and side == 'front'))
        for side in ('left', 'right'):
            window(fk[side], 0, 1.6, w=2.0, h=3.6, frame='wood_paint', sill='castle_trim')
        top += 7.0
    box(nm('eave'), (w + 0.4, d + 0.4, 0.5), loc=(0, 0, top - 0.25), key='castle_trim')
    hr = d * 0.45
    gable_roof(F(0, 0, 0, 0), w, d, top, hr, keys=('wb_terra', 'wb_terra_b'), wall='wb_plaster_rose', ov=1.1, ovg=0.9)
    yf = -d / 2 + 2.2
    zb = roof_z(top, hr, d, yf) - 0.3
    slope = hr / (d / 2)
    for i in range(3):
        dx = -w / 2 + w * (i + 0.5) / 3
        dormer(F(0, 0, 0, 0), dx, yf, zb, w=3.2, h=3.4, depth=3.4 / slope + 1.2, wall='wb_plaster_rose', keys=('wb_terra', 'wb_terra_b'), frame='wood_paint')
    chimney(w / 2 - 2.4, d * 0.2, top, top + hr + 2.6, key='wb_terra_b')
    hanging_sign(fc0['front'], w / 2 - 3.0, gh - 1.2, board='shutter_r')
    return finalize('B07_02_capital_house_02', smooth_angle=30)


def cap_house_3():
    """03 half-timber corner house with round turret and conical green copper roof."""
    reset()
    w, d = 18.0, 18.0
    top = house(w=w, d=d, floors=3, gh=8.0, fh=7.0, upper='wb_plaster_warm', timber=True, jetty=0.7,
                rkeys=('wb_copper', 'wb_copper_dk'), shutter='shutter_g', flowers=('fl_red', 'fl_white'),
                dormers=2, seed=73, roof='side')
    # round turret on the -x,-y street corner with copper cone
    cx, cy, r = -w / 2 - 0.6, -d / 2 - 0.6, 3.2
    lathe(nm('tc'), [(0.0, 4.0), (1.2, 4.0), (r - 0.2, 6.2), (r, 6.8), (r, top + 3.0), (0.0, top + 3.0)], loc=(cx, cy, 0), key='wb_plaster_warm', segs=20)
    for zz in (6.8, 15.0, top + 2.8):
        lathe(nm('tb'), [(0.0, zz - 0.2), (r + 0.3, zz - 0.2), (r + 0.3, zz + 0.25), (0.0, zz + 0.25)], loc=(cx, cy, 0), key='timber', segs=20)
    for i in range(3):
        a = -135 + (i - 1) * 50
        fr = F(cx + math.cos(math.radians(a)) * r, cy + math.sin(math.radians(a)) * r, 0, a + 90)
        for zz in (8.2, 15.5):
            window(fr, 0, zz, w=1.5, h=3.0, arch=True, frame='wood_paint', sill='timber', panes=True, lit=(i == 1 and zz > 10))
    cone_roof(cx, cy, top + 3.0, r, 7.5, keys=('wb_copper', 'wb_copper_dk'), rings=6, ov=0.6, finial='brass', flag='fabric_green')
    return finalize('B07_03_capital_house_03', smooth_angle=30)


def cap_house_4():
    """04 stone townhouse, balcony with iron railings, grey slate mansard roof."""
    reset()
    w, d = 17.0, 16.0
    gh, fh = 8.5, 7.5
    # ground + 2 upper stone storeys
    box(nm('g'), (w, d, gh), loc=(0, 0, gh / 2), key='ashlar_dark')
    box(nm('pl'), (w + 0.4, d + 0.4, 1.0), loc=(0, 0, 0.5), key='stone_dark', bev=0.06)
    band(0, 0, w, d, gh - 0.2, 0.5, 'castle_trim', out=0.2)
    fc0 = faces(0, 0, w, d)
    door(fc0['front'], 0, w=3.6, h=6.8, arch=True, surround='castle_trim', lamp=True)
    window(fc0['front'], -5.5, 1.8, w=2.4, h=4.4, arch=True, frame='wood_paint', sill='castle_trim', keystone='castle_trim')
    window(fc0['front'], 5.5, 1.8, w=2.4, h=4.4, arch=True, frame='wood_paint', sill='castle_trim', keystone='castle_trim')
    door(fc0['back'], 0, w=3.0, h=6.0, arch=False, surround='castle_trim', step='stone_dark')
    top = gh
    for k in range(2):
        box(nm('u'), (w, d, fh), loc=(0, 0, top + fh / 2), key='ashlar')
        fk = faces(0, 0, w, d, top)
        band(0, 0, w, d, top - 0.05, 0.3, 'castle_trim', out=0.12)
        for fr in (F(*faces(0,0,w,d,top)['left'].p(0,0,0), -90), F(*faces(0,0,w,d,top)['right'].p(0,0,0), 90)):
            pass
        for x in (-5.5, 0, 5.5):
            if k == 0 and x == 0:
                # balcony door + projecting balcony with iron railing
                door(fk['front'], 0, w=2.6, h=5.2, arch=False, key='glass_dark', surround='castle_trim', step=None, studs=False)
                lbox(fk['front'], (6.4, 2.6, 0.5), 0, -1.3, 0.0, 'castle_trim', bev=0.05)
                for s in (-1, 1):
                    lbeam(fk['front'], (s * 2.6, -0.1, -1.8), (s * 2.6, -2.3, -0.2), 0.35, 'castle_trim')
                railing(F(*fk['front'].p(0, 0, 0), 0), -3.1, 3.1, 0.25, y=-2.5, h=1.8, key='iron')
                for s in (-1, 1):
                    lbox(fk['front'], (0.1, 2.5, 0.12), s * 3.1, -1.3, 2.0, 'iron')
            else:
                window(fk['front'], x, 1.6, w=2.2, h=3.9, frame='wood_paint', sill='castle_trim', shutter='shutter_b', lit=(k==1 and x==-5.5))
            window(fk['back'], -x, 1.6, w=2.2, h=3.7, frame='wood_paint', sill='castle_trim')
        for side in ('left', 'right'):
            window(fk[side], 0, 1.6, w=2.0, h=3.6, frame='wood_paint', sill='castle_trim')
        top += fh
    band(0, 0, w, d, top - 0.05, 0.5, 'castle_trim', out=0.25)
    # mansard roof: steep lower slope (grey slate) + shallow top, with dormers
    lower_h = 5.0
    lathe_profile = None
    for s in (-1, 1):   # steep sides front/back
        pass
    # steep mansard skirt on all four sides
    for fr, L, DD in ((F(0, 0, top, 0), w, d), (F(0, 0, top, 180), w, d), (F(0, 0, top, 90), d, w), (F(0, 0, top, -90), d, w)):
        p0 = fr.p(-L / 2 - 0.4, -DD / 2 - 0.4, 0)
        slab([fr.p(-L/2-0.4, -DD/2-0.4, 0), fr.p(L/2+0.4, -DD/2-0.4, 0), fr.p(L/2+0.4, -DD/2+2.2, lower_h), fr.p(-L/2-0.4, -DD/2+2.2, lower_h)], (0,0,0.0), 'wb_slate_grey')
    # simpler: build mansard as a frustum box ring
    for s, (L, DD, rz) in enumerate([(w, d, 0), (w, d, 180), (d, w, 90), (d, w, -90)]):
        fr = F(0, 0, top, rz)
        lbox(fr, (L + 0.8, 1.6, lower_h + 0.5), 0, -DD / 2 - 0.1, lower_h / 2, 'wb_slate_grey', rot=(-18, 0, 0))
    # flat-ish mansard deck top
    box(nm('deck'), (w - 3.0, d - 3.0, 3.5), loc=(0, 0, top + lower_h + 1.75), key='wb_slate_grey')
    box(nm('deckcap'), (w - 2.4, d - 2.4, 0.4), loc=(0, 0, top + lower_h + 3.6), key='castle_trim', bev=0.05)
    # dormers poking through the mansard skirt (front)
    for dx in (-5.0, 5.0):
        lbox(F(0, -d / 2 - 1.2, top, 0), (3.0, 2.0, 3.2), dx, -0.2, 1.4, 'ashlar')
        window(F(0, -d / 2 - 1.3, top + 1.4, 0), dx, 0.3, w=1.6, h=2.2, arch=True, frame='wood_paint', sill='wood_paint', panes=True)
        lathe(nm('dr'), [(0,0),(1.9,0),(0,1.6)], loc=(dx, -d/2-1.3, top+3.6), key='wb_slate_grey', segs=4)
    chimney(w / 2 - 3.0, d * 0.2, top + lower_h, top + lower_h + 6.0, key='brick')
    chimney(-w / 2 + 3.0, -d * 0.2, top + lower_h, top + lower_h + 6.0, key='brick')
    return finalize('B07_04_capital_house_04', smooth_angle=30)


def cap_house_5():
    """05 bakery: striped awning, hanging sign, window flower boxes, bright plaster, brown shingle roof."""
    reset()
    w, d = 18.0, 15.0
    top = house(w=w, d=d, floors=3, gh=8.5, fh=7.0, ground='wb_plaster_warm', ground_trim='wood_dark',
                upper='wb_plaster_warm', timber=False, jetty=0.0, roof='side', rkeys=('wb_brownshingle', 'wb_brownshingle_b'),
                shutter='shutter_r', flowers=('fl_red', 'fl_yellow', 'fl_white'), dormers=2, seed=75, shop=True, sign='shutter_r')
    fc0 = faces(0, 0, w, d, 0)
    awning(fc0['front'], 0, 7.0, w=w - 4.0)
    # extra flower boxes on upper windows front
    for x in (-5.5, 5.5):
        from arch import flower_box
        flower_box(F(0, -d / 2, 10.0, 0), x, 9.6, 2.6, ('fl_red', 'fl_pink', 'fl_white'))
    # big round bread sign emblem
    cyl(nm('be'), 1.4, 0.3, loc=fc0['front'].p(6.0, -2.0, 11.0), key='bread', verts=18, rot=fc0['front'].r(90, 0, 0))
    return finalize('B07_05_capital_house_05', smooth_angle=30)


def cap_house_6():
    """06 narrow tower house with a clock face and bell cupola on top, brick and stone, purple slate."""
    reset()
    w, d = 15.0, 15.0
    gh, fh = 8.0, 7.0
    floors = 4
    box(nm('pl'), (w + 0.6, d + 0.6, 1.2), loc=(0, 0, 0.6), key='stone_dark', bev=0.08)
    box(nm('g'), (w, d, gh), loc=(0, 0, gh / 2), key='ashlar')
    band(0, 0, w, d, gh - 0.2, 0.5, 'castle_trim', out=0.2)
    fc0 = faces(0, 0, w, d)
    door(fc0['front'], 0, w=3.4, h=6.6, arch=True, surround='castle_trim', lamp=True)
    window(fc0['front'], -5.0, 1.8, w=2.2, h=4.2, arch=True, frame='wood_paint', sill='castle_trim', keystone='castle_trim')
    window(fc0['front'], 5.0, 1.8, w=2.2, h=4.2, arch=True, frame='wood_paint', sill='castle_trim', keystone='castle_trim')
    door(fc0['back'], 0, w=3.0, h=6.0, arch=False, surround='castle_trim', step='stone_dark')
    top = gh
    for k in range(floors - 1):
        box(nm('u'), (w, d, fh), loc=(0, 0, top + fh / 2), key='brick')
        band(0, 0, w, d, top - 0.05, 0.35, 'castle_trim', out=0.14)
        for fr in (F(*faces(0,0,w,d,top)['front'].p(0,0,0), 0),):
            pass
        fk = faces(0, 0, w, d, top)
        for x in (-5.0, 5.0):
            window(fk['front'], x, 1.6, w=2.0, h=3.6, arch=True, frame='wood_paint', sill='castle_trim', shutter='shutter_b', lit=(k==1 and x==-5.0))
            window(fk['back'], -x, 1.6, w=2.0, h=3.4, arch=True, frame='wood_paint', sill='castle_trim')
        for side in ('left', 'right'):
            window(fk[side], 0, 1.6, w=1.8, h=3.4, arch=True, frame='wood_paint', sill='castle_trim')
        for sx in (-1,1):
            for sy in (-1,1):
                lbox(F(sx*w/2, sy*d/2, top, 45), (1.2,1.2,fh), 0,0,fh/2, 'castle_trim')
        top += fh
    band(0, 0, w, d, top - 0.05, 0.5, 'castle_trim', out=0.25)
    # clock stage with a clock face on the front
    cs = 6.0
    box(nm('cs'), (w - 1.0, d - 1.0, cs), loc=(0, 0, top + cs / 2), key='ashlar')
    for side, rz in (('front', 0), ('back', 180)):
        fr = F(0, (-d/2+0.5) if side=='front' else (d/2-0.5), top, rz)
        cyl(nm('cf'), 2.4, 0.4, loc=fr.p(0, -0.1, cs/2 + 0.5), key='wb_clock_face', verts=24, rot=fr.r(90,0,0))
        cyl(nm('cfr'), 2.55, 0.3, loc=fr.p(0, 0.0, cs/2 + 0.5), key='wb_clock', verts=24, rot=fr.r(90,0,0))
        torus(nm('cr'), 2.6, 0.35, loc=fr.p(0, -0.3, cs/2 + 0.5), key='castle_trim', segs=24, rsegs=6, rot=fr.r(90,0,0))
        for h12 in range(12):
            a = math.radians(90 - 30*h12)
            lbox(fr, (0.26,0.14,0.55), math.cos(a)*1.95, -0.35, cs/2+0.5+math.sin(a)*1.95, 'wb_clock_hand')
        lbox(fr, (0.22,0.16,1.9), 0.0, -0.4, cs/2+0.5+0.55, 'wb_clock_hand', rot=(0,-32,0))   # hour hand
        lbox(fr, (0.16,0.16,2.3), 0.0, -0.42, cs/2+0.5+0.1, 'wb_clock_hand', rot=(0,62,0))     # minute hand
        cyl(nm('ch'), 0.28, 0.3, loc=fr.p(0, -0.45, cs/2+0.5), key='wb_clock_hand', verts=12, rot=fr.r(90,0,0))
    top += cs
    band(0, 0, w-1, d-1, top-0.1, 0.5, 'castle_trim', out=0.3)
    # open bell cupola: 8 posts, roof, hanging bell
    cr = 3.4
    for i in range(8):
        a = math.radians(45*i)
        cyl(nm('bp'), 0.4, 6.0, loc=(math.cos(a)*cr, math.sin(a)*cr, top), key='castle_trim', verts=8)
    lbox(F(0,0,top+6.0,0), (cr*2+2, cr*2+2, 0.6), 0,0,0.3, 'castle_trim', bev=0.05)
    cone_roof(0, 0, top + 6.6, cr + 1.2, 6.0, keys=('wb_slate_purple', 'wb_slate_purple_b'), rings=6, ov=0.5, finial='gold')
    lathe(nm('bell'), [(0,0),(1.1,0),(1.2,1.0),(0.7,2.2),(0.3,2.6),(0,2.7)], loc=(0,0,top+1.2), key='wb_bell', segs=14)
    box(nm('byoke'), (cr*1.4, 0.4, 0.4), loc=(0,0,top+4.2), key='wood_dark')
    return finalize('B07_06_capital_house_06', smooth_angle=30)


# ======================================================= B08 Town-1 Gothic church
def town1_church():
    """Gothic church 35 wide x 85 long (nave along Y, front/door at -Y), 75 high. Spooky weathered stone,
    dark slate roof, buttresses with pinnacles, lancet stained-glass windows, bell tower + tall spire,
    gargoyles, porch with steps. Not enterable (recessed closed door)."""
    reset()
    W, L, body_h = 24.0, 85.0, 34.0
    SK = 'stone_dark'          # spooky weathered stone
    SKb = 'ev_stone_dark'
    TRIM = 'stone'
    ROOF = ('wb_slate_dark' if 'wb_slate_dark' in P else 'tile_grey', 'tile_grey')
    P.setdefault('wb_slate_dark', ((44, 52, 70), 'Slate', 0.0, 0.78, 0))
    ROOF = ('wb_slate_dark', 'tile_grey')
    # nave body centred, running along Y
    box(nm('nave'), (W, L - 18, body_h), loc=(0, 4.0, body_h / 2), key=SK)
    box(nm('plinth'), (W + 1.6, L - 16, 2.4), loc=(0, 4.0, 1.2), key='stone_dark', bev=0.1)
    # coursed relief faint on long walls
    for s in (-1, 1):
        fr = F(s * W / 2, 4.0, 0, s * 90)
        for zz in (10.0, 20.0, 30.0):
            band(s * W / 2, 4.0, 0.3, L - 18, zz, 0.5, TRIM, out=0.0)  # thin string course
    # side aisles (lower) with buttresses + lancet windows
    aisle_h = 18.0
    for s in (-1, 1):
        box(nm('aisle'), (6.0, L - 20, aisle_h), loc=(s * (W / 2 + 3.0), 4.0, aisle_h / 2), key=SK)
        fr = F(s * (W / 2 + 6.0), 4.0, 0, s * 90)
        ny = 6
        for i in range(ny):
            yy = -(L - 24) / 2 + (L - 24) * i / (ny - 1)
            lancet(F(s * (W / 2 + 6.0), 4.0 + yy, 0, s * 90), 0, 4.0, w=2.2, h=10.0,
                   glass=('stained_b','stained_r','stained_y','stained_g')[i % 4], frame=TRIM, medallion='stained_y')
            # buttress between windows
            if i < ny - 1:
                by = yy + (L - 24) / (ny - 1) / 2
                from_fr = F(s * (W / 2 + 6.0), 4.0 + by, 0, s * 90)
                lbox(from_fr, (2.0, 2.4, aisle_h + 2.0), 0, -1.2, (aisle_h + 2.0) / 2, SKb, bev=0.05)
                lbox(from_fr, (2.2, 1.2, 0.6), 0, -1.8, aisle_h + 2.0, TRIM, rot=(-26, 0, 0))
                pinnacle(*from_fr.p(0, -1.0, aisle_h + 2.0), s=1.2, h=4.6, key=TRIM, tip=TRIM)
        # aisle lean-to roof
        for yy in (0,):
            lbox(F(s * (W / 2 + 3.0), 4.0, aisle_h, s * 90), (L - 20, 7.0, 0.5), 0, -0.5, 2.6, ROOF[0], rot=(-s*0 - 32, 0, 0))
    # clerestory lancets on the upper nave
    for s in (-1, 1):
        fr = F(s * W / 2, 4.0, 0, s * 90)
        for i in range(7):
            yy = -(L - 26) / 2 + (L - 26) * i / 6
            lancet(F(s * W / 2, 4.0 + yy, 0, s * 90), 0, 22.0, w=1.8, h=9.0, glass=('stained_y','stained_b','stained_r')[i%3], frame=TRIM, medallion='stained_r')
    # steep gable roof over the nave
    hr = W * 0.62
    gable_roof(F(0, 4.0, 0, 90), L - 18, W, body_h, hr, keys=ROOF, wall=SK, ov=1.0, ovg=0.6, ridge='iron', crest='iron')
    # ---- front (-Y): porch, recessed closed door, rose window, two small turrets ----
    fy = -(L - 18) / 2 + 4.0
    ff = F(0, fy, 0, 0)
    # gable front wall is part of nave; add a projecting porch
    porch_w, porch_d, porch_h = 12.0, 6.0, 12.0
    box(nm('porch'), (porch_w, porch_d, porch_h), loc=(0, fy - porch_d / 2, porch_h / 2), key=SK)
    pf = F(0, fy - porch_d, 0, 0)
    # big pointed portal with a recessed CLOSED door (dark, set back)
    half_disc(pf, 0, 8.0, 3.2, 0.0, 1.0, SKb)
    lbox(pf, (6.4, 1.0, 8.0), 0, -0.1, 4.0, SKb)
    # recessed closed door
    lbox(pf, (4.4, 0.6, 7.0), 0, 0.5, 3.5, 'wood_dark')
    for xx in (-1.2, 0, 1.2):
        lbox(pf, (0.2, 0.7, 6.6), xx, 0.3, 3.5, 'timber')
    tube(nm('pa'), arc_pts(pf, 0, 8.0, 3.6, y=-0.3, n=13), 0.4, TRIM, res=4)
    # voussoir orders around the portal
    for k, rr in enumerate((3.9, 4.4, 4.9)):
        tube(nm('vo'), arc_pts(pf, 0, 8.0, rr, y=-0.2 - 0.2*k, n=13), 0.28, TRIM if k%2 else SKb, res=4)
    # porch steps
    for i in range(4):
        box(nm('ps'), (porch_w + 2 - i*0.8, 2.0, 1.0), loc=(0, fy - porch_d - 1.0 - i*1.4, 0.5 + (3-i)*0), key='stone_dark', bev=0.05)
    for i in range(4):
        box(nm('ps'), (porch_w + 3 - i, 2.2, 0.8), loc=(0, fy - porch_d - 0.5 - i*1.5, 0.4 + i*0.0), key='stone', bev=0.05)
    # gable roof on the porch
    gable_roof(F(0, fy - porch_d / 2, 0, 0), porch_w, porch_d, porch_h, porch_w*0.5, keys=ROOF, wall=SK, ov=0.6, ovg=0.4)
    # rose window above the porch in the nave gable
    rose_window(ff, 0, body_h - 4.0, 5.0, frame=TRIM)
    # gable-end pinnacles
    for s in (-1, 1):
        pinnacle(s * (W / 2 - 0.5), fy + 0.2, body_h + 1.0, s=1.6, h=6.0, key=TRIM, tip=TRIM)
    # ---- apse at the back (+Y): polygonal east end ----
    ay = (L - 18) / 2 + 4.0
    r_ap = W / 2
    lathe(nm('apse'), [(0.0, 0.0), (r_ap, 0.0), (r_ap, body_h*0.7), (r_ap*0.8, body_h*0.8), (0.0, body_h*0.82)], loc=(0, ay, 0), key=SK, segs=7)
    # ---- bell tower with tall spire at the front-left corner ----
    tx, ty = -(W / 2 + 6.0), fy + 2.0
    ts, tH = 14.0, 52.0
    box(nm('tower'), (ts, ts, tH), loc=(tx, ty, tH / 2), key=SK)
    box(nm('tpl'), (ts + 2, ts + 2, 3.0), loc=(tx, ty, 1.5), key='stone_dark', bev=0.1)
    for sx in (-1, 1):
        for sy in (-1, 1):
            lbox(F(tx + sx*ts/2, ty + sy*ts/2, 0, 0), (2.0, 2.0, tH - 8), 0, 0, (tH-8)/2 + 2, SKb, bev=0.05)
    for fr in (F(tx, ty - ts/2, 0, 0), F(tx, ty + ts/2, 0, 180), F(tx - ts/2, ty, 0, -90), F(tx + ts/2, ty, 0, 90)):
        lancet(fr, 0, tH - 18.0, w=2.4, h=12.0, glass='glass_dark', frame=TRIM, medallion=None)   # belfry openings
        lancet(fr, 0, 16.0, w=2.0, h=9.0, glass='stained_b', frame=TRIM, medallion='stained_y')
        for zz in (14.0, 28.0, 42.0):
            band(tx, ty, ts, ts, zz, 0.5, TRIM, out=0.15)
    # tower parapet + corner pinnacles + tall spire
    lbox(F(tx, ty, 0, 0), (ts, ts, 1.0), 0, 0, tH + 0.5, 'stone')
    for fr in (F(tx, ty - ts/2 + 0.6, tH + 1.0, 0), F(tx, ty + ts/2 - 0.6, tH + 1.0, 180), F(tx - ts/2 + 0.6, ty, tH + 1.0, -90), F(tx + ts/2 - 0.6, ty, tH + 1.0, 90)):
        battlements(fr, -ts/2 + 0.6, ts/2 - 0.6, 0, SK, t=0.9, mw=1.6, gap=1.1, mh=2.0, ph=1.4, cap=TRIM)
    for sx in (-1, 1):
        for sy in (-1, 1):
            pinnacle(tx + sx*(ts/2-0.6), ty + sy*(ts/2-0.6), tH + 1.0, s=1.6, h=8.0, key=TRIM, tip=TRIM)
    cone_roof(tx, ty, tH + 2.0, ts/2 - 1.0, 26.0, keys=('wb_slate_dark', 'tile_grey'), rings=10, ov=0.4, finial='iron')
    # ---- gargoyles projecting from the nave eaves ----
    for s in (-1, 1):
        for yy in (-18, 0, 18):
            gx, gy, gz = s * (W / 2 + 0.3), 4.0 + yy, body_h - 1.0
            box(nm('gg'), (1.2, 2.6, 1.0), loc=(gx + s*1.0, gy, gz), key=SKb, rot=(0, s*18, 0))
            ball(nm('ggh'), 0.7, loc=(gx + s*2.2, gy, gz - 0.3), key=SKb, segs=7, rings=5, scale=(1, 1.3, 0.9))
            lbox(F(gx + s*2.6, gy, 0, s*90), (0.4, 0.5, 0.5), 0, 0, gz - 0.3, SKb)   # snout
    return finalize('B08_01_town1_church_01', smooth_angle=28)


BATCHES = {
    'houses': ('v4_capital', [
        ('B07_01_capital_house_01', cap_house_1, (0.9, -1.2, 0.35)),
        ('B07_02_capital_house_02', cap_house_2, (0.9, -1.2, 0.35)),
        ('B07_03_capital_house_03', cap_house_3, (1.0, -1.1, 0.35)),
        ('B07_04_capital_house_04', cap_house_4, (0.9, -1.2, 0.35)),
        ('B07_05_capital_house_05', cap_house_5, (0.9, -1.2, 0.35)),
        ('B07_06_capital_house_06', cap_house_6, (0.9, -1.1, 0.4)),
    ]),
    'church': ('v4_town1', [
        ('B08_01_town1_church_01', town1_church, (0.8, -1.2, 0.3)),
    ]),
}
