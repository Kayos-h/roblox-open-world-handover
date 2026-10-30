"""Worker we2 - B04 garrison (barracks + stables), category v4_castle.
Replaces worker we's B04 which errored (a helper leaked key='door').
Belongs to the same castle as wb's B02 keep/towers and we's B05 courtyard:
matching ashlar / marble trim / slate / heraldry colours. 1 unit = 1 stud,
front faces -Y, origin bottom-centre via finalize. Uses only base palette keys
(all verified present) plus we2_ additions below.
"""
import math, random
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism
from arch import (F, faces, nm, lbox, lbeam, lslab, beam3, window, door, quoins, band,
                  battlements, timber_frame, gable_roof, chimney)
import v4util

P = kitlib.PAL
# echo the castle colours (names start with we2_)
P['we2_ashlar']    = ((206, 198, 180), 'Limestone',  0.00, 0.82, 0)
P['we2_ashlar_b']  = ((188, 180, 162), 'Limestone',  0.00, 0.86, 0)
P['we2_plinth']    = ((132, 128, 120), 'Cobblestone', 0.00, 0.90, 0)
P['we2_trim']      = ((230, 224, 210), 'Marble',     0.00, 0.48, 0)
P['we2_slate_a']   = ((70, 82, 108),   'Slate',      0.00, 0.72, 0)
P['we2_slate_b']   = ((58, 68, 92),    'Slate',      0.00, 0.74, 0)
P['we2_plaster']   = ((222, 210, 188), 'Plaster',    0.00, 0.90, 0)
P['we2_timber']    = ((78, 54, 37),    'Wood',       0.00, 0.85, 0)
P['we2_wood']      = ((122, 84, 52),   'WoodPlanks', 0.00, 0.80, 0)
P['we2_floor']     = ((96, 92, 86),    'Slate',      0.00, 0.80, 0)
P['we2_steel']     = ((150, 156, 164), 'Metal',      0.90, 0.32, 0)
P['we2_iron']      = ((44, 42, 40),    'Metal',      0.85, 0.48, 0)
P['we2_bronze']    = ((120, 86, 52),   'Metal',      0.90, 0.40, 0)
P['we2_gold']      = ((214, 172, 72),  'Metal',      1.00, 0.25, 0)
P['we2_leather']   = ((96, 64, 42),    'Fabric',     0.00, 0.85, 0)
P['we2_hay']       = ((190, 160, 92),  'Fabric',     0.00, 1.00, 0)
P['we2_rope']      = ((176, 150, 104), 'Fabric',     0.00, 1.00, 0)
P['we2_glass_lit'] = ((246, 196, 110), 'Glass',      0.00, 0.20, 0.45)
P['we2_banner_r']  = ((150, 36, 42),   'Fabric',     0.00, 0.95, 0)
P['we2_banner_b']  = ((44, 66, 128),   'Fabric',     0.00, 0.95, 0)
P['we2_banner_g']  = ((196, 158, 72),  'Fabric',     0.00, 0.95, 0)
P['we2_water']     = ((70, 110, 150),  'Glass',      0.00, 0.20, 0)


def _mdoor(f, x, z=0.0):
    # v4util.marker passes name_key straight through as the palette key, and the
    # registered marker key is 'mk_door' -> pass the prefixed form.
    v4util.marker('mk_door', f.p(x, -0.1, z + 0.1))


# ------------------------------------------------------- yard furniture
def _weapon_rack(x, y, rz):
    f = F(x, y, 0, rz)
    lbox(f, (5.0, 0.6, 0.4), 0, 0, 0.2, 'we2_wood')
    lbox(f, (5.0, 0.6, 0.5), 0, 0, 4.0, 'we2_wood')
    for s in (-1, 1):
        lbox(f, (0.4, 0.4, 4.2), s * 2.3, 0, 2.1, 'we2_timber')
    for k in range(6):
        wx = -2.0 + k * 0.8
        kind = k % 3
        if kind == 0:   # spear
            lbox(f, (0.1, 0.1, 5.2), wx, 0, 2.6, 'we2_timber')
            lathe(nm('sp'), [(0, 0), (0.14, 0), (0, 0.6)], loc=f.p(wx, 0, 5.0), key='we2_steel', segs=6)
        elif kind == 1:  # sword
            lbox(f, (0.12, 0.08, 3.2), wx, 0.1, 2.0, 'we2_steel')
            lbox(f, (0.5, 0.12, 0.14), wx, 0.1, 0.5, 'we2_bronze')
            lbox(f, (0.12, 0.12, 0.5), wx, 0.1, 0.25, 'we2_leather')
        else:            # axe
            lbox(f, (0.1, 0.1, 4.0), wx, 0, 2.2, 'we2_timber')
            poly_prism(nm('ax'), [(0, 0), (0.7, 0.3), (0.7, -0.3)], 0.12, loc=f.p(wx + 0.1, 0.0, 3.6), key='we2_steel', rot=f.r(90, 0, 0))


def _shield_wall(x, y):
    f = F(x, y, 0, 0)
    lbox(f, (9.0, 0.6, 5.0), 0, 0, 2.5, 'we2_wood')
    for s in (-1, 1):
        lbox(f, (0.5, 0.6, 5.6), s * 4.5, 0, 2.8, 'we2_timber')
    cols = ['we2_banner_r', 'we2_banner_b', 'we2_banner_g']
    for i, (sx, sz) in enumerate(((-3.0, 1.6), (0.0, 1.6), (3.0, 1.6), (-1.5, 3.4), (1.5, 3.4))):
        poly_prism(nm('sh'), [(-1.0, 0.8), (1.0, 0.8), (1.0, -0.6), (0, -1.6), (-1.0, -0.6)], 0.18,
                   loc=f.p(sx, -0.1, sz + 0.6), key=cols[i % 3], rot=f.r(90, 0, 0))
        cyl(nm('shb'), 0.3, 0.1, loc=f.p(sx, -0.25, sz), key='we2_gold', verts=10, rot=f.r(90, 0, 0))


def _training_dummy(x, y):
    cyl(nm('tdp'), 0.3, 5.5, loc=(x, y, 0), key='we2_timber', verts=8)
    ball(nm('tdb'), 1.1, loc=(x, y, 4.0), key='we2_hay', segs=12, rings=8, scale=(1, 1, 1.3))
    lbox(F(x, y, 0, 0), (3.6, 0.5, 0.5), 0, 0, 4.2, 'we2_timber')
    for s in (-1, 1):
        ball(nm('tdh'), 0.5, loc=(x + s * 1.5, y, 4.2), key='we2_hay', segs=8, rings=6)
    ball(nm('tdhd'), 0.7, loc=(x, y, 5.6), key='we2_hay', segs=10, rings=7)
    torus(nm('tdr'), 1.1, 0.08, loc=(x, y, 3.4), key='we2_rope', segs=14, rsegs=4, rot=(0, 0, 0))
    box(nm('tdsh'), (1.6, 0.2, 1.8), loc=(x, y - 1.0, 4.0), key='we2_wood', bev=0.04)


# ===================================================== B04_01 barracks
def barracks():
    """Stone ground floor, timber-framed jettied upper storey, crenellated roof walk,
    raised front door up a stone stair, chimney; yard has weapon racks, a shield wall,
    a training dummy. ~42x23x28. Closed, hollow interior."""
    reset()
    W, D, gh, uh = 42.0, 23.0, 10.0, 9.0
    t = 1.8
    # plinth + floor slab
    box(nm('plinth'), (W + 0.8, D + 0.8, 1.2), loc=(0, 0, 0.6), key='we2_plinth', bev=0.06)
    box(nm('floor'), (W - 2 * t, D - 2 * t, 0.4), loc=(0, 1.2, 1.0), key='we2_floor')
    # hollow stone shell: four walls as boxes (so interior is closed but open through door)
    box(nm('w_back'),  (W, t, gh), loc=(0, D / 2 - t / 2, gh / 2 + 0.8), key='we2_ashlar')
    for s in (-1, 1):
        box(nm('w_side'), (t, D, gh), loc=(s * (W / 2 - t / 2), 0, gh / 2 + 0.8), key='we2_ashlar')
    # front wall in two spans leaving a central door gap (4 wide)
    dgx, dgw = -W / 2 + 8.0, 4.0
    box(nm('w_fl'), ((dgx - dgw / 2) - (-W / 2) , t, gh), loc=((-W / 2 + (dgx - dgw / 2)) / 2, -D / 2 + t / 2, gh / 2 + 0.8), key='we2_ashlar')
    box(nm('w_fr'), ((W / 2) - (dgx + dgw / 2), t, gh), loc=(((dgx + dgw / 2) + W / 2) / 2, -D / 2 + t / 2, gh / 2 + 0.8), key='we2_ashlar')
    # lintel over the door gap
    box(nm('lint'), (dgw + 1.4, t + 0.2, 1.2), loc=(dgx, -D / 2 + t / 2, 0.8 + 7.4), key='we2_trim')
    fc = faces(0, 1.2, W, D, 0.8)
    for s in ('front', 'back', 'left', 'right'):
        quoins(fc[s], 0.9, gh - 0.3, 'we2_trim', course=1.1)
    # stone stair up to the raised threshold
    for k in range(4):
        box(nm('st'), (dgw + 2.0, 2.0, 0.6), loc=(dgx, -D / 2 - 4.2 + k * 1.4, 0.3 + k * 0.6), key='we2_ashlar_b', bev=0.05)
    # the door itself (timber, iron bands) at threshold z=0.8
    fdoor = fc['front'].sub(dgx, 0, 0)
    door(fdoor, 0, w=3.8, h=7.0, arch=True, key='timber', surround='we2_trim', step=None, studs=True)
    _mdoor(fc['front'], dgx, z=0.8)
    # ground windows
    for x in (-6.0, 4.0, 14.0):
        window(fc['front'], x, 3.0, w=2.2, h=4.0, arch=True, frame='we2_trim', sill='we2_trim', glass='we2_glass_lit', lit=(x == 4.0))
    for x in (-14.0, -4.0, 6.0, 15.0):
        window(fc['back'], x, 3.0, w=2.2, h=4.0, arch=True, frame='we2_trim', sill='we2_trim')
    for s in ('left', 'right'):
        window(fc[s], 0, 3.0, w=2.4, h=4.4, arch=True, frame='we2_trim', sill='we2_trim')
    band(0, 1.2, W, D, 0.8 + gh - 0.1, 0.6, 'we2_trim', out=0.2)
    # jettied timber-framed upper storey
    jj, z1 = 0.8, 0.8 + gh
    dk = D + 2 * jj
    box(nm('u'), (W, dk, uh), loc=(0, 1.2, z1 + uh / 2), key='we2_plaster')
    for s in (-1, 1):
        for i in range(int(W / 1.6) + 1):
            xx = -W / 2 + 0.4 + (W - 0.8) * i / int(W / 1.6)
            box(nm('jo'), (0.45, 0.9, 0.5), loc=(xx, 1.2 + s * (dk / 2 - 0.3), z1 + 0.1), key='we2_timber')
    fu = faces(0, 1.2, W, dk, z1)
    for side, L in (('front', W), ('back', W), ('left', dk), ('right', dk)):
        posts = [-L / 2 + 0.3] + [-L / 2 + L * i / int(L / 6) for i in range(1, int(L / 6))] + [L / 2 - 0.3]
        timber_frame(fu[side], L, 0, uh, posts, key='we2_timber', braces=True)
        n = max(2, int(L / 7))
        for i in range(n):
            x = -L / 2 + L * (i + 0.5) / n
            window(fu[side], x, 2.2, w=2.4, h=4.0, frame='we2_timber', sill='we2_timber', glass='we2_glass_lit',
                   lit=((i % 3 == 1) and side == 'front'))
    # flat roof walk with battlements
    z2 = z1 + uh
    box(nm('rf'), (W, dk, 0.6), loc=(0, 1.2, z2 + 0.3), key='we2_floor')
    ft = faces(0, 1.2, W, dk, z2 + 0.6)
    for s, L in (('front', W), ('back', W), ('left', dk), ('right', dk)):
        battlements(ft[s], -L / 2, L / 2, 0, 'we2_ashlar', t=1.0, mw=1.6, gap=1.2, mh=1.8, ph=1.3, cap='we2_trim')
    chimney(W / 2 - 5.0, 1.2 + dk * 0.18, z2, z2 + 7.0, w=2.2, key='we2_ashlar_b')
    # yard furniture in front
    _weapon_rack(-W / 2 + 16.0, -D / 2 - 3.0, 0)
    _weapon_rack(-W / 2 + 22.0, -D / 2 - 3.0, 180)
    _shield_wall(6.0, -D / 2 - 3.2)
    _training_dummy(16.0, -D / 2 - 4.5)
    return finalize('barracks', smooth_angle=28)


# ===================================================== B04_02 stables
def stables():
    """Long low building, open stall fronts with half-doors, interior partitions, hay and
    water troughs, a gabled slate roof, a hay-loft door with a jutting pulley beam, lanterns.
    ~41x20x18. Closed back/sides, open front."""
    reset()
    W, D, wh = 41.0, 20.0, 10.0
    t = 1.6
    box(nm('plinth'), (W + 0.8, D + 0.8, 0.8), loc=(0, 0, 0.4), key='we2_plinth', bev=0.05)
    box(nm('floor'), (W, D, 0.3), loc=(0, 0, 0.75), key='we2_floor')
    # back + side stone walls
    box(nm('back'), (W, t, wh), loc=(0, D / 2 - t / 2, wh / 2 + 0.6), key='we2_ashlar')
    for s in (-1, 1):
        box(nm('side'), (t, D, wh), loc=(s * (W / 2 - t / 2), 0, wh / 2 + 0.6), key='we2_ashlar')
    # open stall front: posts + top beam
    nst = 5
    sw = (W - 2 * t) / nst
    lbeam(F(), (-W / 2 + t, -D / 2 + 1.0, 0.6 + wh - 0.5), (W / 2 - t, -D / 2 + 1.0, 0.6 + wh - 0.5), 0.7, 'we2_timber')
    for i in range(nst + 1):
        x = -W / 2 + t + sw * i
        box(nm('post'), (0.7, 0.7, wh), loc=(x, -D / 2 + 1.0, wh / 2 + 0.6), key='we2_timber')
    # interior partitions
    for i in range(1, nst):
        x = -W / 2 + t + sw * i
        box(nm('part'), (0.4, D - 2.0, 3.4), loc=(x, 0.5, 2.5), key='we2_wood')
    rnd = random.Random(42)
    for i in range(nst):
        cx = -W / 2 + t + sw * (i + 0.5)
        # half door
        lbox(F(cx, -D / 2 + 1.0, 0.6, 0), (sw - 1.2, 0.3, 3.2), 0, -0.1, 1.9, 'we2_wood')
        lbox(F(cx, -D / 2 + 1.0, 0.6, 0), (sw - 1.2, 0.34, 0.3), 0, -0.14, 3.4, 'we2_timber')
        torus(nm('hdr'), 0.18, 0.05, loc=(cx + sw * 0.3, -D / 2 + 0.6, 0.6 + 2.0), key='we2_iron', segs=10, rsegs=4, rot=(90, 0, 0))
        # hay + trough
        for k in range(3):
            box(nm('hay'), (1.4, 1.0, 0.6), loc=(cx - 1.0 + k * 1.0, D / 2 - 3.0, 0.6 + 0.6 + (k % 2) * 0.3),
                key='we2_hay', rot=(0, 0, rnd.uniform(0, 20)), bev=0.1)
        lbox(F(cx, D / 2 - 1.8, 0.6, 0), (sw - 1.4, 1.2, 0.8), 0, 0, 1.0, 'we2_wood')
        box(nm('trw'), (sw - 1.8, 0.8, 0.12), loc=(cx, D / 2 - 1.8, 0.6 + 1.3), key='we2_water')
    # gabled slate roof
    hr = D * 0.42
    gable_roof(F(0, 0, 0.6 + wh, 0), W, D, 0, hr, keys=('we2_slate_a', 'we2_slate_b'), wall='we2_ashlar', ov=1.0, ovg=0.8, barge='we2_timber')
    # hay-loft door in the front gable + jutting pulley beam
    fl = F(0, -D / 2 - 0.2, 0.6 + wh, 0)
    lbox(fl, (4.0, 0.4, 4.0), 0, 0.1, 2.5, 'we2_ashlar')
    lbox(fl, (3.2, 0.3, 3.0), 0, -0.1, 2.3, 'we2_wood')
    lbeam(fl, (0, -0.2, 5.4), (0, -3.6, 5.4), 0.4, 'we2_timber')
    torus(nm('pul'), 0.4, 0.12, loc=fl.p(0, -3.3, 5.0), key='we2_iron', segs=12, rsegs=4)
    tube(nm('pr'), [fl.p(0, -3.3, 4.7), fl.p(0, -3.3, 1.5)], 0.05, 'we2_rope', res=4)
    lathe(nm('hk'), [(0, 0), (0.16, 0.1), (0.12, 0.5), (0, 0.6)], loc=fl.p(0, -3.3, 0.9), key='we2_iron', segs=6)
    # lanterns on two front posts
    for i in (1, 3):
        x = -W / 2 + t + sw * i
        f = F(x, -D / 2 + 0.7, 0.6, 0)
        lbox(f, (0.5, 0.5, 0.7), 0, -0.3, wh - 2.0, 'we2_glass_lit')
        lathe(nm('lc'), [(0.35, 0), (0, 0.35)], loc=f.p(0, -0.3, wh - 1.6), key='we2_iron', segs=6)
    _mdoor(F(-W / 2 + t + sw * 2.5, -D / 2 + 1.0, 0.6, 0), 0)
    return finalize('stables', smooth_angle=28)


BATCHES = {
    'garrison': ('v4_castle', [('B04_01_barracks', barracks, (1.0, -1.2, 0.42)),
                               ('B04_02_stables', stables, (1.0, -1.2, 0.42))]),
}
