"""Worker wb - B02 royal castle set (+ P2 throne hall, barracks, stables, courtyard, market).
New set, richer than the old K01-K08: ashlar course relief, plinths, buttresses, machicolations,
arrow slits, crenellated parapets, banners, conical slate roofs with finials, balconies, stair turrets.
1 unit = 1 stud. Fronts face -Y. Pieces TILE: fixed wall profile height 31, thickness 10, walkway z=26.
"""
import math, random
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, top_paint, dup
from arch import (F, faces, lbox, lbeam, beam3, slab, lslab, half_disc, window, door, arrow_slit, quoins, band,
                  corbels, battlements, ring_battlements, timber_frame, gable_roof, roof_z, cone_roof, chimney,
                  dormer, railing, lancet, rose_window, column_c, pinnacle, arc_pts, nm)

# ---- worker palette keys (all start with wb_) : weathered royal limestone + heraldry ----
P = kitlib.PAL
P['wb_ashlar']      = ((206, 198, 180), 'Limestone',   0.0, 0.82, 0)
P['wb_ashlar_b']    = ((190, 182, 164), 'Limestone',   0.0, 0.85, 0)
P['wb_ashlar_c']    = ((176, 166, 148), 'Limestone',   0.0, 0.88, 0)
P['wb_ashlar_warm'] = ((214, 202, 176), 'Sandstone',   0.0, 0.84, 0)
P['wb_ashlar_stain']= ((150, 146, 132), 'Limestone',   0.0, 0.92, 0)
P['wb_plinth']      = ((132, 128, 120), 'Cobblestone',  0.0, 0.90, 0)
P['wb_trim']        = ((230, 224, 210), 'Marble',       0.0, 0.48, 0)
P['wb_slate_a']     = ((70, 82, 108),   'Slate',        0.0, 0.72, 0)
P['wb_slate_b']     = ((58, 68, 92),    'Slate',        0.0, 0.74, 0)
P['wb_slate_dark']  = ((44, 52, 70),    'Slate',        0.0, 0.78, 0)
P['wb_lead']        = ((96, 104, 112),  'Metal',        0.70, 0.55, 0)
P['wb_banner_red']  = ((150, 36, 42),   'Fabric',       0.0, 0.95, 0)
P['wb_banner_gold'] = ((196, 158, 72),  'Fabric',       0.0, 0.95, 0)
P['wb_banner_blue'] = ((44, 66, 128),   'Fabric',       0.0, 0.95, 0)
P['wb_portc']       = ((54, 50, 46),    'Metal',        0.80, 0.55, 0)
P['wb_floor']       = ((150, 142, 128), 'Slate',        0.0, 0.88, 0)

WH, WT, WALK = 31.0, 10.0, 26.0   # wall height, thickness, walkway top z


# --------------------------------------------------------- shared helpers
def ashlar_face(f, w, z0, z1, key='wb_ashlar', alt=('wb_ashlar_b', 'wb_ashlar_c'), course=2.6, out=0.14, y=0.0, seed=0, bev=0.0, block=3.4):
    """Raised ashlar blocks giving coursed-stone relief on a wall face (local x along w, outer face -y side at y)."""
    rnd = random.Random(seed)
    z = z0
    row = 0
    while z + 0.1 < z1:
        ch = min(course, z1 - z)
        nb = max(2, int(w / block))
        bw = w / nb
        offset = (bw / 2) if row % 2 else 0.0
        xx = -w / 2 - (bw if offset else 0)
        while xx < w / 2 - 0.1:
            x0 = max(-w / 2, xx)
            x1 = min(w / 2, xx + bw)
            if x1 - x0 > 0.4:
                k = key if rnd.random() < 0.55 else rnd.choice(alt)
                lbox(f, (x1 - x0 - 0.18, out, ch - 0.18), (x0 + x1) / 2, y - out / 2, z + ch / 2, k, bev=bev)
            xx += bw
        z += course
        row += 1


def buttress(f, x, z0, z1, w=2.4, proj=2.2, key='wb_ashlar_b', cap='wb_trim', setbacks=2):
    """Stepped buttress sticking out -y from a wall face, with sloped weatherings."""
    h = z1 - z0
    for i in range(setbacks):
        t = i / setbacks
        pw = w * (1 - 0.18 * i)
        pp = proj * (1 - 0.30 * i)
        zz0 = z0 + h * (t * 0.0)
        zz1 = z1 - h * 0.12 * i
        lbox(f, (pw, pp, zz1 - zz0), x, -pp / 2, (zz0 + zz1) / 2, key, bev=0.05)
        # sloped weathering cap between setbacks
        lbox(f, (pw + 0.2, pp * 0.5, 0.5), x, -pp + pp * 0.25, zz1, cap, rot=(-24, 0, 0))
    # small pinnacle on top
    pinnacle(*f.p(x, -proj * 0.35, z1), s=1.2, h=4.6, key=cap, tip=cap)


def banner(f, x, z, h=7.0, w=3.0, key='wb_banner_red', seed=0):
    """Hanging heraldic banner from a bracket on a wall."""
    rnd = random.Random(seed)
    lbox(f, (w + 0.5, 0.35, 0.35), x, -0.45, z + 0.2, 'iron')          # top bar bracket
    lbeam(f, (x - w / 2, -0.1, z), (x - w / 2, -0.5, z + 0.1), 0.12, 'iron')
    lbeam(f, (x + w / 2, -0.1, z), (x + w / 2, -0.5, z + 0.1), 0.12, 'iron')
    # cloth with a slight hanging sag and a pointed/forked bottom
    seg = 6
    for i in range(seg):
        xx = x - w / 2 + w * (i + 0.5) / seg
        sag = 0.25 * math.sin(math.pi * (i + 0.5) / seg)
        hh = h - (1.4 if (i in (0, seg - 1)) else 0) + rnd.uniform(-0.1, 0.1)
        lbox(f, (w / seg + 0.02, 0.1, hh), xx, -0.55 - sag * 0.1, z - hh / 2 + 0.1, key)
    # device: a pale stripe + emblem disc
    lbox(f, (w * 0.5, 0.06, h * 0.5), x, -0.62, z - h * 0.4, 'wb_banner_gold')
    cyl(nm('bem'), w * 0.16, 0.08, loc=f.p(x, -0.66, z - h * 0.4), key='wb_trim', verts=12, rot=f.r(90, 0, 0))


def wall_profile(f, length, key='wb_ashlar', seed=0, both_ends=True):
    """One straight curtain-wall segment of fixed profile, centred on frame f, running along local x.
    Core + plinth + ashlar relief both faces + walkway slab + crenellated parapet + machicolations."""
    L = length
    # plinth (battered base)
    lbox(f, (L, WT + 1.8, 2.4), 0, 0, 1.2, 'wb_plinth', bev=0.1)
    lbox(f, (L, WT + 1.0, 1.6), 0, 0, 3.0, 'wb_plinth', rot=(0, 0, 0))
    # main core
    lbox(f, (L, WT, WH - 3.2), 0, 0, 3.2 + (WH - 3.2) / 2, key)
    # ashlar relief, front (-y) and back (+y)
    ashlar_face(F(*f.p(0, -WT / 2, 0), f.rz), L, 3.6, WALK - 0.5, y=0.0, seed=seed)
    ashlar_face(F(*f.p(0, WT / 2, 0), f.rz + 180), L, 3.6, WALK - 0.5, y=0.0, seed=seed + 50)
    # string course under the walkway
    lbox(f, (L, WT + 0.8, 0.6), 0, 0, WALK - 0.4, 'wb_trim', bev=0.05)
    # walkway slab
    lbox(f, (L, WT - 1.2, 1.0), 0, 0, WALK + 0.5, 'wb_floor')
    # machicolation corbels on the outer (-y) edge just under the parapet
    corbels(F(*f.p(0, -WT / 2, 0), f.rz), -L / 2 + 1.0, L / 2 - 1.0, WALK - 1.0, 'wb_ashlar_b', step=2.2, size=(0.7, 1.0, 1.1))
    # outer parapet with merlons + arrow slits, inner low parapet
    fo = F(*f.p(0, -WT / 2 + 0.5, WALK + 1.0), f.rz)
    battlements(fo, -L / 2, L / 2, 0, key, t=1.1, mw=2.0, gap=1.4, mh=2.6, ph=1.6, y=0.0, cap='wb_trim')
    fi = F(*f.p(0, WT / 2 - 0.5, WALK + 1.0), f.rz + 180)
    lbox(fi, (L, 0.9, 2.0), 0, 0.45, 1.0, key)   # inner parapet (solid, lower)
    # arrow slits in the merlon band at intervals
    for xx in [-L / 2 + 3.0 + i * 5.0 for i in range(max(1, int((L - 4) / 5.0)) + 1)]:
        if abs(xx) < L / 2 - 1.5:
            arrow_slit(F(*f.p(0, -WT / 2, 0), f.rz), xx, 14.0, h=3.2, key=key)


# --------------------------------------------------------- B02_05 curtain wall (straight, 40 long)
def curtain_wall():
    reset()
    wall_profile(F(0, 0, 0, 0), 40.0, seed=5)
    # a banner mid-span on the inner face
    banner(F(0, WT / 2, 0, 180), 0, 22.0, h=6.5, w=2.8, key='wb_banner_blue', seed=3)
    return finalize('B02_05_curtain_wall', smooth_angle=30)


# --------------------------------------------------------- B02_06 curtain corner
def curtain_corner():
    reset()
    arm = 16.0
    # two arms meeting at origin corner; each arm profile identical to the straight wall end profile
    wall_profile(F(-arm / 2 - WT / 2, 0, 0, 0), arm, seed=6)                 # arm running along +x from corner
    wall_profile(F(0, -arm / 2 - WT / 2, 0, 90), arm, seed=7)               # arm running along +y from corner
    # round corner turret at the junction
    cx, cy = -WT / 2, -WT / 2
    r = 7.5
    lathe(nm('tp'), [(0.0, 0.0), (r + 1.0, 0.0), (r + 0.6, 2.4), (r, 4.0), (r, WH + 4.0), (0.0, WH + 4.0)], loc=(cx, cy, 0), key='wb_ashlar', segs=28)
    # coursed relief band rings
    for zz in (8.0, 16.0, 24.0):
        lathe(nm('tb'), [(0.0, zz - 0.2), (r + 0.35, zz - 0.2), (r + 0.35, zz + 0.3), (0.0, zz + 0.3)], loc=(cx, cy, 0), key='wb_trim', segs=28)
    # arrow slits around the turret
    for i in range(6):
        a = 60 * i
        fr = F(cx + math.cos(math.radians(a)) * r, cy + math.sin(math.radians(a)) * r, 0, a + 90)
        arrow_slit(fr, 0, 14.0 + (4.0 if i % 2 else 0), h=3.0, key='wb_ashlar_b')
    # crenellated top ring with machicolations
    ring_battlements(cx, cy, WH + 4.0, r, 'wb_ashlar', t=1.1, mh=2.6, ph=1.6, cap='wb_trim', machicolate=True)
    # banner pole on the turret
    cyl(nm('fp'), 0.22, 9.0, loc=(cx, cy, WH + 4.0 + 1.7), key='iron', verts=8)
    lbox(F(cx + 1.8, cy, 0, 0), (3.4, 0.12, 5.0), 0, 0, WH + 4.0 + 6.0, 'wb_banner_red')
    return finalize('B02_06_curtain_corner', smooth_angle=30)


# --------------------------------------------------------- B02_07 gatehouse
def gatehouse():
    reset()
    arm = 16.0
    passage_w, passage_h = 12.0, 18.0
    # central block holding the passage
    cb_w = passage_w + 2 * 7.0   # flanking piers 7 wide each -> 26
    cb_d = 20.0
    box(nm('cb'), (cb_w, cb_d, WH + 6.0), loc=(0, 0, (WH + 6.0) / 2), key='wb_ashlar')
    box(nm('cbp'), (cb_w + 1.0, cb_d + 1.0, 2.6), loc=(0, 0, 1.3), key='wb_plinth', bev=0.1)
    # relief on the four faces of the central block
    for fr, L in ((F(0, -cb_d / 2, 0, 0), cb_w), (F(0, cb_d / 2, 0, 180), cb_w),
                  (F(-cb_w / 2, 0, 0, -90), cb_d), (F(cb_w / 2, 0, 0, 90), cb_d)):
        ashlar_face(fr, L, 3.0, WH - 2.0, seed=int(L))
    # carve the passage: build the block as side piers + a lintel instead of a solid cut
    # (we already made a solid block; add the dark passage void + portcullis slots as inset geometry)
    # passage void (dark) and vaulted top
    lbox(F(0, 0, 0, 0), (passage_w, cb_d + 0.6, passage_h), 0, 0, passage_h / 2, 'hole')
    # arch over the passage front & back
    for sgn in (-1, 1):
        fr = F(0, sgn * cb_d / 2, 0, 0 if sgn < 0 else 180)
        half_disc(fr, 0, passage_h - passage_w / 2, passage_w / 2, 0.0, 1.2, 'wb_ashlar_b')
        tube(nm('ga'), arc_pts(fr, 0, passage_h - passage_w / 2, passage_w / 2 + 0.6, y=-0.3, n=13), 0.6, 'wb_trim', res=4)
        lbox(fr, (2.0, 1.0, 2.2), 0, -0.4, passage_h + 0.6, 'wb_trim', bev=0.06)   # keystone
        # portcullis slots + a half-lowered portcullis grid on the front
        for s in (-1, 1):
            lbox(fr, (0.5, 0.6, passage_h), s * (passage_w / 2 - 0.1), -0.9, passage_h / 2, 'wb_portc')
    # a partly-lowered portcullis in the front opening
    frf = F(0, -cb_d / 2, 0, 0)
    for i in range(7):
        xx = -passage_w / 2 + 0.6 + (passage_w - 1.2) * i / 6
        lbox(frf, (0.3, 0.3, passage_h * 0.55), xx, -0.8, passage_h * 0.72, 'wb_portc')
    for j in range(3):
        lbox(frf, (passage_w - 1.0, 0.3, 0.3), 0, -0.8, passage_h * 0.55 + j * passage_h * 0.22, 'wb_portc')
    # murder hole (dark square in the vault, visible from below) - represent as dark recess on underside
    lbox(F(0, 0, 0, 0), (2.0, 2.0, 0.6), 0, 0, passage_h - 0.3, 'hole')
    # drawbridge chain slots above the arch on the front
    for s in (-1, 1):
        lbox(frf, (0.5, 0.4, 2.4), s * (passage_w / 2 + 1.4), -0.3, passage_h + 3.0, 'hole')
        cyl(nm('chw'), 0.5, 0.8, loc=frf.p(s * (passage_w / 2 + 1.4), -0.6, passage_h + 4.4), key='iron', verts=10, rot=frf.r(90, 0, 0))
    # walkway + crenellated parapet across the top of the central block
    lbox(F(0, 0, 0, 0), (cb_w, cb_d - 1.5, 1.0), 0, 0, WH + 6.0 + 0.5, 'wb_floor')
    corbels(F(0, -cb_d / 2, 0, 0), -cb_w / 2 + 1, cb_w / 2 - 1, WH + 5.0, 'wb_ashlar_b', step=2.4, size=(0.7, 1.0, 1.1))
    battlements(F(0, -cb_d / 2 + 0.6, WH + 7.0, 0), -cb_w / 2, cb_w / 2, 0, 'wb_ashlar', t=1.1, mw=2.0, gap=1.4, mh=2.6, ph=1.6, cap='wb_trim')
    battlements(F(0, cb_d / 2 - 0.6, WH + 7.0, 180), -cb_w / 2, cb_w / 2, 0, 'wb_ashlar', t=1.1, mw=2.0, gap=1.4, mh=2.6, ph=1.6, cap='wb_trim')
    # flanking round towers rising above the gate
    for s in (-1, 1):
        tx = s * (cb_w / 2 - 1.0)
        r = 6.0
        lathe(nm('ft'), [(0.0, 0.0), (r + 0.8, 0.0), (r, 3.0), (r, WH + 12.0), (0.0, WH + 12.0)], loc=(tx, 0, 0), key='wb_ashlar_warm', segs=22)
        for zz in (10.0, 20.0, 30.0):
            lathe(nm('ftb'), [(0.0, zz - 0.2), (r + 0.3, zz - 0.2), (r + 0.3, zz + 0.25), (0.0, zz + 0.25)], loc=(tx, 0, 0), key='wb_trim', segs=22)
        for i in range(5):
            a = 72 * i - 20
            fr = F(tx + math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r, 0, a + 90)
            arrow_slit(fr, 0, 16.0 + (6.0 if i % 2 else 0), h=3.0, key='wb_ashlar_b')
        ring_battlements(tx, 0, WH + 12.0, r, 'wb_ashlar_warm', t=1.0, mh=2.4, ph=1.5, cap='wb_trim', machicolate=True)
        # conical roof + banner on each flank tower
        cone_roof(tx, 0, WH + 12.0 + 3.6, r - 0.4, 9.0, keys=('wb_slate_a', 'wb_slate_b'), rings=7, ov=0.7, finial='gold', flag='wb_banner_red')
    # wall arms either side (same fixed profile)
    wall_profile(F(-cb_w / 2 - arm / 2, 0, 0, 0), arm, seed=70)
    wall_profile(F(cb_w / 2 + arm / 2, 0, 0, 0), arm, seed=71)
    # big heraldic banner over the gate
    banner(frf, 0, passage_h + 7.0, h=8.0, w=4.0, key='wb_banner_blue', seed=9)
    from v4util import marker
    marker('mk_door', (0, -cb_d / 2 - 0.4, 0.2))
    return finalize('B02_07_gatehouse', smooth_angle=30)


# --------------------------------------------------------- B02_02 round tower
def round_tower():
    reset()
    r = 10.0
    H = 80.0
    cx = cy = 0.0
    lathe(nm('pl'), [(0.0, 0.0), (r + 2.0, 0.0), (r + 1.2, 3.0), (r, 5.0), (r, H), (0.0, H)], loc=(cx, cy, 0), key='wb_ashlar', segs=30)
    ashlar_ring(cx, cy, r, 6.0, H - 6.0, 'wb_ashlar', seed=2)
    for zz in (18.0, 34.0, 50.0, 66.0):
        lathe(nm('rb'), [(0.0, zz - 0.2), (r + 0.4, zz - 0.2), (r + 0.4, zz + 0.3), (0.0, zz + 0.3)], loc=(cx, cy, 0), key='wb_trim', segs=30)
    # arrow slits up the shaft, spiralling
    for k in range(5):
        a = 60 * k + 15 * k
        zz = 16.0 + k * 12.0
        fr = F(math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r, 0, a + 90)
        arrow_slit(fr, 0, zz, h=3.2, key='wb_ashlar_b')
    # a couple of real windows near the top
    for i in range(3):
        a = 120 * i + 40
        fr = F(math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r, 0, a + 90)
        window(fr, 0, H - 14.0, w=2.0, h=3.6, arch=True, frame='wb_trim', sill='wb_trim', panes=False, lit=(i == 0))
    ring_battlements(cx, cy, H, r, 'wb_ashlar', t=1.2, mh=2.8, ph=1.8, cap='wb_trim', machicolate=True)
    cone_roof(cx, cy, H + 4.0, r - 0.6, 12.0, keys=('wb_slate_a', 'wb_slate_b'), rings=8, ov=0.8, finial='gold', flag='wb_banner_gold')
    return finalize('B02_02_round_tower', smooth_angle=30)


def ashlar_ring(cx, cy, r, z0, z1, key, seed=0, course=2.6, out=0.18):
    """Coursed-stone relief wrapped around a cylindrical tower shaft."""
    rnd = random.Random(seed)
    circ = 2 * math.pi * r
    nb = max(10, int(circ / 3.2))
    z = z0
    row = 0
    while z + 0.1 < z1:
        ch = min(course, z1 - z)
        off = (0.5 if row % 2 else 0.0)
        for i in range(nb):
            if rnd.random() < 0.5:
                continue
            a = 360 * (i + off) / nb
            ar = math.radians(a)
            box(nm('ar'), (circ / nb * 0.7, out, ch - 0.2),
                loc=(cx + math.cos(ar) * (r + out / 2), cy + math.sin(ar) * (r + out / 2), z + ch / 2),
                key=rnd.choice([key, 'wb_ashlar_b', 'wb_ashlar_c']), rot=(0, 0, a), bev=0.04)
        z += course
        row += 1


# --------------------------------------------------------- B02_03 square tower
def square_tower():
    reset()
    s = 20.0
    H = 76.0
    box(nm('t'), (s, s, H), loc=(0, 0, H / 2), key='wb_ashlar')
    box(nm('pl'), (s + 2.4, s + 2.4, 3.0), loc=(0, 0, 1.5), key='wb_plinth', bev=0.12)
    # corner buttresses
    for sx in (-1, 1):
        for sy in (-1, 1):
            fr = F(sx * s / 2, sy * s / 2, 0, 45 + (0 if (sx * sy > 0) else 90))
            lbox(F(sx * (s / 2 + 1.0), sy * (s / 2 + 1.0), 0, 0), (2.6, 2.6, H - 6.0), 0, 0, (H - 6.0) / 2 + 3.0, 'wb_ashlar_b', bev=0.06)
            pinnacle(sx * (s / 2 + 1.0), sy * (s / 2 + 1.0), H - 3.0, s=1.6, h=6.0, key='wb_trim', tip='wb_trim')
    for fr, L in ((F(0, -s / 2, 0, 0), s), (F(0, s / 2, 0, 180), s), (F(-s / 2, 0, 0, -90), s), (F(s / 2, 0, 0, 90), s)):
        ashlar_face(fr, L - 3.0, 4.0, H - 6.0, seed=int(L + fr.rz))
        for k in range(4):
            arrow_slit(fr, 0, 12.0 + k * 14.0, h=3.0, key='wb_ashlar_b')
    for zz in (20.0, 40.0, 60.0):
        band(0, 0, s, s, zz, 0.6, 'wb_trim', out=0.3)
    # top machicolated parapet (square)
    lbox(F(0, 0, 0, 0), (s - 1.0, s - 1.0, 1.0), 0, 0, H + 0.5, 'wb_floor')
    for fr in (F(0, -s / 2 + 0.6, H + 1.0, 0), F(0, s / 2 - 0.6, H + 1.0, 180), F(-s / 2 + 0.6, 0, H + 1.0, -90), F(s / 2 - 0.6, 0, H + 1.0, 90)):
        corbels(F(fr.o.x, fr.o.y, H - 1.0, fr.rz) if False else F(*fr.p(0, 0, -2.0), fr.rz), -s / 2 + 1, s / 2 - 1, 0, 'wb_ashlar_b', step=2.4, size=(0.7, 1.0, 1.0))
        battlements(fr, -s / 2 + 0.5, s / 2 - 0.5, 0, 'wb_ashlar', t=1.1, mw=2.0, gap=1.4, mh=2.8, ph=1.8, cap='wb_trim')
    cyl(nm('fp'), 0.26, 11.0, loc=(0, 0, H + 3.5), key='iron', verts=8)
    lbox(F(2.2, 0, 0, 0), (4.0, 0.12, 6.0), 0, 0, H + 8.0, 'wb_banner_gold')
    return finalize('B02_03_square_tower', smooth_angle=30)


# --------------------------------------------------------- B02_04 spire tower
def spire_tower():
    reset()
    r = 7.5
    H = 86.0
    lathe(nm('pl'), [(0.0, 0.0), (r + 1.6, 0.0), (r + 1.0, 2.4), (r, 4.0), (r, H), (0.0, H)], loc=(0, 0, 0), key='wb_ashlar_warm', segs=24)
    ashlar_ring(0, 0, r, 5.0, H - 4.0, 'wb_ashlar_warm', seed=4, course=2.4)
    for zz in (16.0, 32.0, 48.0, 64.0, 78.0):
        lathe(nm('rb'), [(0.0, zz - 0.2), (r + 0.35, zz - 0.2), (r + 0.35, zz + 0.3), (0.0, zz + 0.3)], loc=(0, 0, 0), key='wb_trim', segs=24)
    for k in range(6):
        a = 60 * k + 12 * k
        zz = 14.0 + k * 11.0
        fr = F(math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r, 0, a + 90)
        arrow_slit(fr, 0, zz, h=2.8, key='wb_ashlar_b')
    for i in range(2):
        a = 180 * i + 60
        fr = F(math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r, 0, a + 90)
        window(fr, 0, H - 12.0, w=1.6, h=3.2, arch=True, frame='wb_trim', sill='wb_trim', panes=False, lit=(i == 0))
    ring_battlements(0, 0, H, r, 'wb_ashlar_warm', t=1.0, mh=2.2, ph=1.4, cap='wb_trim', machicolate=True)
    # tall slim conical slate spire
    cone_roof(0, 0, H + 3.4, r - 0.8, 24.0, keys=('wb_slate_a', 'wb_slate_dark'), rings=11, ov=0.6, finial='gold', flag='wb_banner_blue')
    return finalize('B02_04_spire_tower', smooth_angle=30)


# --------------------------------------------------------- B02_01 keep
def keep():
    reset()
    W, D, Hbody = 60.0, 50.0, 78.0
    # battered plinth
    box(nm('pl'), (W + 3.0, D + 3.0, 4.0), loc=(0, 0, 2.0), key='wb_plinth', bev=0.2)
    box(nm('pl2'), (W + 1.5, D + 1.5, 3.0), loc=(0, 0, 5.0), key='wb_plinth')
    # main body
    box(nm('b'), (W, D, Hbody), loc=(0, 0, Hbody / 2 + 6.0), key='wb_ashlar')
    # ashlar relief all four faces (coarse, bevel-free for triangle budget)
    for fr, L in ((F(0, -D / 2, 6.0, 0), W), (F(0, D / 2, 6.0, 180), W), (F(-W / 2, 0, 6.0, -90), D), (F(W / 2, 0, 6.0, 90), D)):
        ashlar_face(fr, L - 4.0, 2.0, Hbody - 8.0, seed=int(L + fr.rz), course=4.0, block=6.0, out=0.2)
    # string courses
    for zz in (24.0, 42.0, 60.0):
        band(0, 0, W, D, zz, 0.7, 'wb_trim', out=0.3)
    # great hall projection on the front (-y) with tall arched windows
    ghw, ghd, ghh = 26.0, 10.0, 34.0
    box(nm('gh'), (ghw, ghd, ghh), loc=(0, -D / 2 - ghd / 2, ghh / 2 + 6.0), key='wb_ashlar_warm')
    ghf = F(0, -D / 2 - ghd, 6.0, 0)
    for i in range(3):
        window(ghf, -ghw / 2 + 5.0 + i * 8.0, 10.0, w=3.4, h=14.0, arch=True, frame='wb_trim', sill='wb_trim', keystone='wb_trim', lit=(i == 1))
    # forebuilding stair up to a first-floor door on the great hall side (compact)
    fbw = 10.0
    for i in range(8):
        box(nm('st'), (fbw, 2.0, 2.0), loc=(ghw / 2 + 4.0, -D / 2 - ghd - 1.5 - i * 1.8, 1.0 + i * 2.0), key='wb_plinth', bev=0.05)
    box(nm('fbw'), (3.0, 16.0, 18.0), loc=(ghw / 2 + 4.0 + fbw / 2 + 1.0, -D / 2 - ghd - 8.0, 9.0 + 6.0), key='wb_ashlar_b')
    door(F(ghw / 2 + 4.0, -D / 2 - ghd, 6.0 + 16.0, 0), 0, w=4.0, h=7.0, arch=True, surround='wb_trim', step='wb_plinth')
    from v4util import marker
    marker('mk_door', (ghw / 2 + 4.0, -D / 2 - ghd - 0.3, 6.0 + 16.0))
    # windows up the body on the other faces (sparser)
    fc = faces(0, 0, W, D, 6.0)
    for side in ('back', 'left', 'right'):
        fr = fc[side]
        LL = W if side == 'back' else D
        for zx in [-LL / 2 + 11 + i * 16 for i in range(max(1, int((LL - 14) / 16)) + 1)]:
            if abs(zx) < LL / 2 - 5:
                for zz in (26.0, 54.0):
                    window(fr, zx, zz, w=2.4, h=4.6, arch=True, frame='wb_trim', sill='wb_trim', panes=False, lit=(zz == 26 and zx == 0))
    # corner turrets rising above the body
    top = Hbody + 6.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            tx, ty, r = sx * (W / 2 - 1.0), sy * (D / 2 - 1.0), 6.5
            lathe(nm('ct'), [(0.0, 20.0), (r + 1.0, 20.0), (r, 23.0), (r, top + 10.0), (0.0, top + 10.0)], loc=(tx, ty, 0), key='wb_ashlar_warm', segs=20)
            for zz in (40.0, 60.0, top + 2.0):
                lathe(nm('ctb'), [(0.0, zz - 0.2), (r + 0.3, zz - 0.2), (r + 0.3, zz + 0.25), (0.0, zz + 0.25)], loc=(tx, ty, 0), key='wb_trim', segs=20)
            for i in range(4):
                a = 90 * i + 45
                fr = F(tx + math.cos(math.radians(a)) * r, ty + math.sin(math.radians(a)) * r, 0, a + 90)
                arrow_slit(fr, 0, top - 14.0, h=3.0, key='wb_ashlar_b')
            ring_battlements(tx, ty, top + 10.0, r, 'wb_ashlar_warm', t=1.0, mh=2.4, ph=1.5, cap='wb_trim', machicolate=False)
            cone_roof(tx, ty, top + 10.0 + 3.4, r - 0.5, 10.0, keys=('wb_slate_a', 'wb_slate_b'), rings=5, ov=0.6, finial='gold',
                      flag=('wb_banner_red' if (sx * sy > 0) else 'wb_banner_blue'))
    # central walkway + machicolated parapet
    lbox(F(0, 0, 0, 0), (W - 2.0, D - 2.0, 1.0), 0, 0, top + 0.5, 'wb_floor')
    for fr in (F(0, -D / 2 + 0.6, top + 1.0, 0), F(0, D / 2 - 0.6, top + 1.0, 180)):
        corbels(F(*fr.p(0, 0, -2.0), fr.rz), -W / 2 + 2, W / 2 - 2, 0, 'wb_ashlar_b', step=2.6, size=(0.8, 1.1, 1.2))
        battlements(fr, -W / 2 + 1, W / 2 - 1, 0, 'wb_ashlar', t=1.2, mw=2.2, gap=1.5, mh=3.0, ph=2.0, cap='wb_trim')
    for fr in (F(-W / 2 + 0.6, 0, top + 1.0, -90), F(W / 2 - 0.6, 0, top + 1.0, 90)):
        battlements(fr, -D / 2 + 1, D / 2 - 1, 0, 'wb_ashlar', t=1.2, mw=2.2, gap=1.5, mh=3.0, ph=2.0, cap='wb_trim')
    # central banner on the great-hall face
    banner(ghf, 0, ghh + 2.0, h=9.0, w=4.2, key='wb_banner_red', seed=11)
    # two balconies on the sides
    for s in (-1, 1):
        bf = F(s * W / 2, 6.0, 6.0 + 44.0, s * 90)
        lbox(bf, (10.0, 3.0, 0.6), 0, -1.5, 0, 'wb_trim', bev=0.06)
        railing(bf, -5.0, 5.0, 0.3, y=-2.9, h=1.8, key='iron')
    return finalize('B02_01_keep', smooth_angle=30)


BATCHES = {
    'castle': ('v4_castle', [
        ('B02_01_keep', keep, (1.0, -1.3, 0.4)),
        ('B02_02_round_tower', round_tower, (1.0, -1.1, 0.35)),
        ('B02_03_square_tower', square_tower, (1.0, -1.1, 0.35)),
        ('B02_04_spire_tower', spire_tower, (1.0, -1.1, 0.4)),
        ('B02_05_curtain_wall', curtain_wall, (0.7, -1.3, 0.4)),
        ('B02_06_curtain_corner', curtain_corner, (1.0, -1.1, 0.4)),
        ('B02_07_gatehouse', gatehouse, (0.6, -1.3, 0.35)),
    ]),
}
