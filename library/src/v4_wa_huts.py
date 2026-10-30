"""wa rusty huts module: A04 six different frontier huts (v4_rusty).
Rusty, patched, lived-in. Sandstone, tin, scrap, canvas, weathered timber.
Each hut: 13-15 wide, hollow with floor, door >= 4 x 7, one or two shuttered
windows, wooden steps, an interior back wall, door marker. Fronts face -Y.
"""
import math, random
from mathutils import Vector
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus
from arch import F, faces, lbox, lbeam, beam3, slab, lslab, nm
from nature import rock
import v4util

PAL = kitlib.PAL
PAL['wa_plank']       = ((128, 98, 68),   'WoodPlanks',   0.00, 0.90, 0)
PAL['wa_plank_grey']  = ((132, 122, 108), 'WoodPlanks',   0.00, 0.92, 0)
PAL['wa_plank_dark']  = ((82, 62, 46),    'Wood',         0.00, 0.90, 0)
PAL['wa_sand']        = ((198, 168, 124), 'Sandstone',    0.00, 0.88, 0)
PAL['wa_sand_dark']   = ((166, 138, 100), 'Sandstone',    0.00, 0.90, 0)
PAL['wa_tin_rust']    = ((132, 78, 50),   'CorrodedMetal',0.50, 0.82, 0)
PAL['wa_tin_grey']    = ((112, 104, 96),  'CorrodedMetal',0.50, 0.80, 0)
PAL['wa_tarp']        = ((120, 104, 78),  'Fabric',       0.00, 1.00, 0)
PAL['wa_tarp_b']      = ((96, 86, 64),    'Fabric',       0.00, 1.00, 0)
PAL['wa_thatch']      = ((164, 138, 86),  'Fabric',       0.00, 1.00, 0)
PAL['wa_plaster']     = ((178, 162, 136), 'Plaster',      0.00, 0.95, 0)
PAL['wa_plaster_st']  = ((150, 134, 112), 'Plaster',      0.00, 0.95, 0)
PAL['wa_shutter']     = ((96, 72, 52),    'WoodPlanks',   0.00, 0.88, 0)
PAL['wa_glass']       = ((120, 128, 120), 'Glass',        0.10, 0.20, 0)
PAL['wa_iron']        = ((60, 52, 46),    'Metal',        0.70, 0.55, 0)
PAL['wa_clay']        = ((168, 104, 70),  'Brick',        0.00, 0.85, 0)


# ----------------------------------------------------------------- shared bits
def _floor(W, D, key='wa_plank_grey'):
    box(nm('floor'), (W - 0.4, D - 0.4, 0.3), loc=(0, 0, 0.15), key=key)


def _walls_box(W, D, H, t, wall_key, door_w=4.5, door_h=7.0, win=((1,), 3.5),
               plank_seams=False, seam_key='wa_plank_dark'):
    """Four solid walls from boxes, with a door gap in the -Y front wall and
    window gaps on the sides. Interior stays closed (back + side + lintel)."""
    # back + both sides (solid)
    box(nm('back'), (W, t, H), loc=(0, D / 2 - t / 2, H / 2), key=wall_key)
    for s in (-1, 1):
        box(nm('side'), (t, D, H), loc=(s * (W / 2 - t / 2), 0, H / 2), key=wall_key)
    # front with a door gap
    fy = -D / 2 + t / 2
    dw = door_w
    box(nm('fl'), ((W - dw) / 2, t, H), loc=(-(dw + (W - dw) / 2) / 2, fy, H / 2), key=wall_key)
    box(nm('fr'), ((W - dw) / 2, t, H), loc=((dw + (W - dw) / 2) / 2, fy, H / 2), key=wall_key)
    box(nm('flin'), (dw, t, H - door_h), loc=(0, fy, door_h + (H - door_h) / 2), key=wall_key)
    if plank_seams:
        for face in ('back', 'left', 'right'):
            fr = faces(0, 0, W, D)[face]
            L = W if face == 'back' else D
            for k in range(int(H / 1.2)):
                lbox(fr, (L, 0.06, 0.1), 0, -0.05, 0.6 + k * 1.2, seam_key)
    return fy, dw


def _door(fy, dw, dh=7.0, key='wa_plank_dark', panel='wa_plank'):
    """A closed plank door in the gap, iron ledges, handle, frame; door marker."""
    for s in (-1, 1):
        box(nm('djamb'), (0.25, 0.9, dh), loc=(s * dw / 2, fy, dh / 2), key=key)
    box(nm('dlin'), (dw + 0.5, 0.9, 0.35), loc=(0, fy, dh + 0.15), key=key)
    box(nm('doorp'), (dw - 0.2, 0.2, dh - 0.2), loc=(0, fy - 0.12, (dh - 0.2) / 2 + 0.1), key=panel)
    for k in range(4):
        box(nm('dpl'), (0.07, 0.1, dh - 0.4), loc=(-dw / 2 + 0.35 + k * (dw - 0.7) / 3, fy - 0.22, dh / 2), key=key)
    for zz in (dh * 0.25, dh * 0.72):
        box(nm('dled'), (dw - 0.4, 0.08, 0.2), loc=(0, fy - 0.24, zz), key='wa_iron')
    ball(nm('dhandle'), 0.14, loc=(dw / 2 - 0.5, fy - 0.3, dh * 0.48), key='wa_iron', segs=6, rings=4)
    v4util.marker('mk_door', (0, fy - 0.1, 0.4))


def _window(fr, x, z, w=2.4, h=2.8, key='wa_glass', shutter='wa_shutter', frame='wa_plank_dark', boarded=False):
    """Shuttered window in a wall frame fr; z = bottom of opening."""
    lbox(fr, (w, 0.14, h), x, -0.02, z + h / 2, key)
    for s in (-1, 1):
        lbox(fr, (0.18, 0.3, h + 0.3), x + s * (w / 2 + 0.08), -0.12, z + h / 2, frame)
    lbox(fr, (w + 0.5, 0.3, 0.22), x, -0.12, z + h + 0.1, frame)
    lbox(fr, (w + 0.6, 0.4, 0.2), x, -0.2, z - 0.1, frame)   # sill
    # mullion + rail
    lbox(fr, (0.1, 0.18, h), x, -0.1, z + h / 2, frame)
    lbox(fr, (w, 0.18, 0.1), x, -0.1, z + h * 0.5, frame)
    if boarded:
        for k in range(3):
            lbox(fr, (w + 0.6, 0.12, 0.4), x, -0.3, z + h * (0.25 + 0.3 * k), 'wa_plank_grey', rot=(0, 0, 6 - k * 5))
    elif shutter:
        sw = w / 2 + 0.1
        for s in (-1, 1):
            lbox(fr, (sw, 0.12, h), x + s * (w / 2 + 0.2 + sw / 2), -0.06, z + h / 2, shutter, rot=(0, 0, s * 16))
            for zz in (0.25, 0.75):
                lbox(fr, (sw - 0.1, 0.06, 0.08), x + s * (w / 2 + 0.2 + sw / 2), -0.14, z + h * zz, frame, rot=(0, 0, s * 16))


def _steps(fy, dw, w=None):
    w = w or dw + 0.6
    for k in range(2):
        box(nm('step'), (w - k * 0.6, 1.2 - k * 0.3, 0.35), loc=(0, fy - 1.0 + k * 0.4, 0.17 + k * 0.35),
            key='wa_plank_dark', bev=0.03)


def _rubble(cx, cy, n, seed, keys=('wa_sand', 'wa_sand_dark', 'stone')):
    rnd = random.Random(seed)
    for i in range(n):
        rock(nm('rk'), rnd.uniform(0.4, 0.9), (cx + rnd.uniform(-2, 2), cy + rnd.uniform(-1.5, 1.5), 0.1),
             key=rnd.choice(keys), seed=seed + i, scale=(1.2, 1.0, 0.7))


def _tin_roof(W, D, H, hr=2.0, key='wa_tin_rust', mono=True, seed=0):
    """Corrugated tin roof. Mono-pitch lean-to (high back) or gable."""
    import mathutils
    rnd = random.Random(seed)
    if mono:
        a = math.atan2(hr, D)
        quad = [(-W / 2 - 0.6, D / 2 + 0.6, H + hr), (W / 2 + 0.6, D / 2 + 0.6, H + hr),
                (W / 2 + 0.6, -D / 2 - 0.6, H), (-W / 2 - 0.6, -D / 2 - 0.6, H)]
        slab(quad, (0, 0, 0.22), key)
        for s in (-1, 1):   # side gable triangles
            slab([(s * W / 2, -D / 2, H), (s * W / 2, D / 2, H), (s * W / 2, D / 2, H + hr)], (s * -0.3, 0, 0), 'wa_plank_grey')
        # corrugation ribs
        nseg = int(W / 0.7)
        for i in range(nseg):
            x = -W / 2 + W * (i + 0.5) / nseg
            n = mathutils.Vector((0, math.sin(a), math.cos(a))) * 0.1
            slab([(x, D / 2 + 0.6 + n.y, H + hr + n.z), (x + 0.1, D / 2 + 0.6 + n.y, H + hr + n.z),
                  (x + 0.1, -D / 2 - 0.6 + n.y, H + n.z), (x, -D / 2 - 0.6 + n.y, H + n.z)], (0, 0, 0.06), 'wa_tin_grey')
    else:
        a = math.atan2(hr, W / 2)
        for s in (-1, 1):
            ez = H - 0.5 * math.tan(a)
            quad = [(0, -D / 2 - 0.6, H + hr), (s * (W / 2 + 0.5), -D / 2 - 0.6, ez),
                    (s * (W / 2 + 0.5), D / 2 + 0.6, ez), (0, D / 2 + 0.6, H + hr)]
            slab(quad, (0, 0, 0.22), key if s < 0 else 'wa_tin_grey')
        for yy in (-D / 2, D / 2):
            slab([(-W / 2, yy, H), (W / 2, yy, H), (0, yy, H + hr)], (0, (0.3 if yy < 0 else -0.3), 0), 'wa_plank_grey')
        box(nm('ridge'), (0.4, D + 1.0, 0.4), loc=(0, 0, H + hr), key='wa_plank_dark')


# ----------------------------------------------------------------- the six huts
def rusty_hut_1():
    """A04_01 - plank hut, lean-to corrugated tin roof (rust), crate stack by the door."""
    reset()
    W, D, H = 14.0, 11.0, 7.5
    _floor(W, D)
    fy, dw = _walls_box(W, D, H, 0.5, 'wa_plank', door_w=4.2, plank_seams=True)
    _door(fy, dw)
    fr = faces(0, 0, W, D)['front']
    _window(fr, -W / 2 + 2.6, 2.6)
    _window(faces(0, 0, W, D)['right'], 0, 2.6)
    _tin_roof(W, D, H, hr=2.2, key='wa_tin_rust', mono=True, seed=41)
    _steps(fy, dw)
    from props import plank_box
    rnd = random.Random(41)
    plank_box(nm('cr1'), (2.2, 2.2, 2.0), loc=(W / 2 - 2.0, -D / 2 - 1.8, 0.0), rnd=rnd)
    plank_box(nm('cr2'), (1.8, 1.8, 1.6), loc=(W / 2 - 2.0, -D / 2 - 1.8, 2.0), rnd=rnd)
    return finalize('rusty_hut_1', smooth_angle=30)


def rusty_hut_2():
    """A04_02 - sandstone-block hut, flat parapet roof, timber awning on poles, round oven chimney."""
    reset()
    W, D, H = 15.0, 12.0, 7.5
    _floor(W, D, key='wa_sand_dark')
    fy, dw = _walls_box(W, D, H, 0.7, 'wa_sand', door_w=4.5)
    _door(fy, dw)
    fr = faces(0, 0, W, D)['front']
    _window(fr, W / 2 - 3.0, 2.8, key='wa_glass')
    _window(faces(0, 0, W, D)['left'], 0, 2.8)
    # sandstone block courses on the walls (proud blocks)
    rnd = random.Random(42)
    for face in ('front', 'back', 'left', 'right'):
        f2 = faces(0, 0, W, D)[face]
        L = W if face in ('front', 'back') else D
        for c in range(5):
            z = 0.8 + c * 1.3
            for i in range(int(L / 2.4)):
                x = -L / 2 + 1.0 + i * 2.4 + (1.2 if c % 2 else 0)
                if abs(x) < dw / 2 + 0.6 and face == 'front' and z < 7.0:
                    continue
                lbox(f2, (2.0 + rnd.uniform(-0.2, 0.2), 0.16, 1.1), x, -0.08, z,
                     rnd.choice(['wa_sand', 'wa_sand_dark']), bev=0.03)
    # flat roof with parapet
    box(nm('roof'), (W, D, 0.5), loc=(0, 0, H + 0.25), key='wa_sand_dark')
    for face in ('front', 'back', 'left', 'right'):
        f2 = faces(0, 0, W, D)[face]
        L = W if face in ('front', 'back') else D
        lbox(f2, (L, 0.6, 1.2), 0, -0.05, H + 1.1, 'wa_sand')
    # timber awning over the door on two poles
    lslab(F(0, fy, 0, 0), [(-dw / 2 - 1, 0, 6.6), (dw / 2 + 1, 0, 6.6), (dw / 2 + 1, -3.0, 5.6), (-dw / 2 - 1, -3.0, 5.6)],
          (0, 0, 0.2), 'wa_tarp')
    for s in (-1, 1):
        cyl(nm('pole'), 0.2, 5.8, loc=(s * (dw / 2 + 0.8), fy - 2.8, 0), key='wa_plank_dark', verts=8)
    # round oven chimney
    cyl(nm('oven'), 1.3, 3.0, loc=(W / 2 - 1.8, D / 2 - 2.0, H), key='wa_clay', verts=16, r2=0.9)
    lathe(nm('ovc'), [(0, 0), (1.0, 0), (0.7, 0.4), (0, 0.4)], loc=(W / 2 - 1.8, D / 2 - 2.0, H + 3.0), key='wa_clay', segs=12)
    _steps(fy, dw)
    return finalize('rusty_hut_2', smooth_angle=30)


def rusty_hut_3():
    """A04_03 - patchwork shack of mixed planks and scrap sheets, tarp roof weighted with stones, leaning stovepipe, crooked door."""
    reset()
    W, D, H = 13.0, 11.0, 7.0
    _floor(W, D)
    # patchwork walls: mixed plank/scrap panels
    t = 0.5
    box(nm('back'), (W, t, H), loc=(0, D / 2 - t / 2, H / 2), key='wa_plank_grey')
    for s in (-1, 1):
        box(nm('side'), (t, D, H), loc=(s * (W / 2 - t / 2), 0, H / 2), key='wa_plank')
    fy = -D / 2 + t / 2
    dw, dh = 4.2, 7.0
    box(nm('fl'), ((W - dw) / 2, t, H), loc=(-(dw + (W - dw) / 2) / 2, fy, H / 2), key='wa_plank')
    box(nm('fr'), ((W - dw) / 2, t, H), loc=((dw + (W - dw) / 2) / 2, fy, H / 2), key='wa_plank_grey')
    box(nm('flin'), (dw, t, H - dh), loc=(0, fy, dh + (H - dh) / 2), key='wa_tin_rust')
    rnd = random.Random(43)
    # scrap patches nailed on
    for face, L in (('front', W), ('back', W), ('left', D), ('right', D)):
        f2 = faces(0, 0, W, D)[face]
        for k in range(5):
            x = rnd.uniform(-L / 2 + 1, L / 2 - 1)
            if face == 'front' and abs(x) < dw / 2 + 1:
                continue
            lbox(f2, (rnd.uniform(1.4, 2.4), 0.1, rnd.uniform(1.2, 2.2)), x, -0.08, rnd.uniform(1.5, 5.5),
                 rnd.choice(['wa_tin_rust', 'wa_tin_grey', 'wa_plank_dark']), rot=(0, 0, rnd.uniform(-8, 8)))
    # crooked door
    for s in (-1, 1):
        box(nm('djamb'), (0.25, 0.9, dh), loc=(s * dw / 2, fy, dh / 2), key='wa_plank_dark')
    box(nm('doorp'), (dw - 0.3, 0.2, dh - 0.3), loc=(0.1, fy - 0.12, (dh - 0.3) / 2 + 0.1), key='wa_plank', rot=(0, 2, 0))
    for k in range(4):
        box(nm('dpl'), (0.07, 0.12, dh - 0.5), loc=(-dw / 2 + 0.4 + k * (dw - 0.8) / 3, fy - 0.24, dh / 2), key='wa_plank_dark', rot=(0, 2, 0))
    box(nm('dled'), (dw - 0.4, 0.08, 0.2), loc=(0.1, fy - 0.26, dh * 0.5), key='wa_iron', rot=(0, 2, 0))
    v4util.marker('mk_door', (0, fy - 0.1, 0.4))
    _window(faces(0, 0, W, D)['front'], W / 2 - 3.0, 2.6, boarded=True)
    # tarp roof weighted with stones (slightly sagged, mono-pitch)
    import mathutils
    hr = 1.8
    a = math.atan2(hr, D)
    quad = [(-W / 2 - 0.8, D / 2 + 0.8, H + hr), (W / 2 + 0.8, D / 2 + 0.8, H + hr),
            (W / 2 + 0.8, -D / 2 - 0.8, H), (-W / 2 - 0.8, -D / 2 - 0.8, H)]
    slab(quad, (0, 0, 0.16), 'wa_tarp')
    slab([(-W / 2 - 0.8, D / 2 + 0.8, H + hr + 0.3), (W / 2 + 0.8, D / 2 + 0.8, H + hr + 0.3),
          (W / 2 + 0.8, 0, (H + hr + H) / 2 - 0.1), (-W / 2 - 0.8, 0, (H + hr + H) / 2 - 0.1)], (0, 0, 0.14), 'wa_tarp_b')
    for i in range(6):
        x = rnd.uniform(-W / 2, W / 2); y = rnd.uniform(-D / 2, D / 2)
        z = H + hr * (1 - (y + D / 2) / D) * 0  # on the slope
        zz = H + (H + hr - H) * ((y + D / 2 + 0.8) / (D + 1.6))
        rock(nm('wt'), 0.4, (x, y, zz + 0.3), key='stone', seed=i)
    # leaning stovepipe
    tube(nm('pipe'), [(-W / 2 + 2.0, D / 2 - 2.0, H + 0.5), (-W / 2 + 2.6, D / 2 - 2.6, H + 3.5), (-W / 2 + 3.4, D / 2 - 2.8, H + 5.0)],
         0.3, 'wa_tin_grey', res=6)
    _steps(fy, dw)
    return finalize('rusty_hut_3', smooth_angle=30)


def rusty_hut_4():
    """A04_04 - two-room dirty-plaster hut, thatch roof patched with tin, canvas awning, water barrel and clay pots."""
    reset()
    W, D, H = 15.0, 12.0, 7.5
    _floor(W, D, key='wa_sand_dark')
    fy, dw = _walls_box(W, D, H, 0.6, 'wa_plaster', door_w=4.4)
    _door(fy, dw)
    # interior cross wall (two rooms) - visible through door
    box(nm('cross'), (0.5, D - 1.2, H - 1), loc=(1.5, 0, (H - 1) / 2), key='wa_plaster_st')
    fr = faces(0, 0, W, D)['front']
    _window(fr, W / 2 - 3.2, 2.8)
    _window(faces(0, 0, W, D)['left'], -D / 4, 2.8)
    _window(faces(0, 0, W, D)['right'], D / 4, 2.8)
    # plaster stains
    rnd = random.Random(44)
    for face, L in (('front', W), ('left', D), ('right', D)):
        f2 = faces(0, 0, W, D)[face]
        for k in range(4):
            lbox(f2, (rnd.uniform(1.5, 3.0), 0.04, rnd.uniform(1.5, 3.5)), rnd.uniform(-L / 2 + 2, L / 2 - 2), -0.03,
                 rnd.uniform(1.5, 5.5), 'wa_plaster_st')
    # thatch roof (gable) patched with tin
    import mathutils
    hr = 3.0
    a = math.atan2(hr, W / 2)
    for s in (-1, 1):
        quad = [(0, -D / 2 - 0.8, H + hr), (s * (W / 2 + 0.7), -D / 2 - 0.8, H - 0.3),
                (s * (W / 2 + 0.7), D / 2 + 0.8, H - 0.3), (0, D / 2 + 0.8, H + hr)]
        slab(quad, (0, 0, 0.4), 'wa_thatch')
        # tin patch on one slope
        if s < 0:
            box(nm('tinp'), (3.0, 3.0, 0.12), loc=(s * W / 4, 1.0, H + hr / 2 + 0.3), key='wa_tin_rust', rot=(0, -s * math.degrees(a), 0))
    for yy in (-D / 2, D / 2):
        slab([(-W / 2, yy, H), (W / 2, yy, H), (0, yy, H + hr)], (0, (0.3 if yy < 0 else -0.3), 0), 'wa_plaster')
    box(nm('ridge'), (0.5, D + 1.4, 0.6), loc=(0, 0, H + hr), key='wa_thatch')
    # canvas awning over the door
    lslab(F(0, fy, 0, 0), [(-dw / 2 - 1, 0, 6.6), (dw / 2 + 1, 0, 6.6), (dw / 2 + 1, -3.2, 5.4), (-dw / 2 - 1, -3.2, 5.4)],
          (0, 0, 0.16), 'wa_tarp')
    for s in (-1, 1):
        cyl(nm('pole'), 0.18, 5.6, loc=(s * (dw / 2 + 0.8), fy - 3.0, 0), key='wa_plank_dark', verts=8)
    # water barrel and clay pots
    from props import barrel_body
    barrel_body(nm('wb'), loc=(W / 2 - 1.6, -D / 2 - 1.8, 0.0), h=3.0, open_top=True)
    for k in range(3):
        lathe(nm('pot'), [(0, 0), (0.5, 0.1), (0.62, 0.6), (0.4, 1.0), (0.3, 1.1), (0.46, 1.2), (0, 1.2)],
              loc=(W / 2 - 3.6 - k * 0.9, -D / 2 - 1.4, 0.0), key='wa_clay', segs=12)
    _steps(fy, dw)
    return finalize('rusty_hut_4', smooth_angle=30)


def rusty_hut_5():
    """A04_05 - hut on a stone footing, half-collapsed tin gable roof showing rafters, ladder, boarded window."""
    reset()
    W, D, H = 14.0, 11.0, 7.0
    # stone footing
    box(nm('foot'), (W + 0.6, D + 0.6, 1.4), loc=(0, 0, 0.7), key='wa_sand_dark', bev=0.05)
    rnd = random.Random(45)
    for i in range(int((W + D) * 0.6)):
        a = rnd.uniform(0, 1)
        # scatter footing stones around the base
        pass
    _floor(W, D)
    # lift floor to footing top
    box(nm('floor2'), (W - 0.4, D - 0.4, 0.3), loc=(0, 0, 1.55), key='wa_plank_grey')
    base = 1.4
    fy, dw = _walls_box2(W, D, H, 0.5, 'wa_plank_grey', base, door_w=4.2)
    _door_z(fy, dw, base)
    fr = faces(0, 0, W, D)['front']
    _window_z(fr, W / 2 - 3.0, base + 2.4, boarded=True)
    # rafters exposed (front slope collapsed -> open)
    import mathutils
    hr = 3.0
    a = math.atan2(hr, W / 2)
    top = base + H
    for i in range(7):
        y = -D / 2 + 1.0 + i * (D - 2.0) / 6
        for s in (-1, 1):
            beam3((0, y, top + hr), (s * (W / 2 + 0.4), y, top - 0.3), 0.3, 0.3, 'wa_plank_dark')
    box(nm('ridgeb'), (0.5, D + 0.6, 0.5), loc=(0, 0, top + hr), key='wa_plank_dark')
    # tin ONLY on the back (+X) slope; front slope left as open rafters
    quad = [(0, -D / 2 - 0.6, top + hr), (W / 2 + 0.5, -D / 2 - 0.6, top - 0.3),
            (W / 2 + 0.5, D / 2 + 0.6, top - 0.3), (0, D / 2 + 0.6, top + hr)]
    slab(quad, (0, 0, 0.2), 'wa_tin_rust')
    # a jagged half-sheet of tin still clinging to the front slope near the ridge
    box(nm('clingtin'), (W / 4, D - 2, 0.12), loc=(-W / 4 - 0.6, 0, top + hr * 0.55 + 0.2),
        key='wa_tin_grey', rot=(0, math.degrees(a), 0))
    # loose tin sheets fallen on the collapsed side
    for k in range(3):
        box(nm('looset'), (2.4, 2.0, 0.1), loc=(-W / 2 + 1.5 + k * 1.2, -D / 2 + 2 + k, top - 2.0 + k * 0.4),
            key=rnd.choice(['wa_tin_rust', 'wa_tin_grey']), rot=(rnd.uniform(-30, 30), rnd.uniform(-40, 40), rnd.uniform(0, 40)))
    for yy in (-D / 2, D / 2):   # gable infill (back slope side only)
        slab([(0, yy, top), (W / 2, yy, top), (0, yy, top + hr)], (0, (0.3 if yy < 0 else -0.3), 0), 'wa_plank_grey')
    # ladder leaning on the -Y front wall beside the door
    lx = W / 2 - 0.5
    for s in (-1, 1):
        beam3((lx, -D / 2 - 1.8 + s * 0.0, 0.2), (lx - 0.9, -D / 2 - 0.2, top + 0.6), 0.14, 0.14, 'wa_plank_dark') if False else None
    lsa, lsb = (W / 2 + 0.2, -D / 2 - 2.2, 0.2), (W / 2 - 0.9, -D / 2 - 0.3, top + 0.8)
    for s in (-0.5, 0.5):
        beam3((lsa[0], lsa[1] + s, lsa[2]), (lsb[0], lsb[1] + s, lsb[2]), 0.13, 0.13, 'wa_plank_dark')
    for k in range(6):
        t = (k + 0.5) / 6
        rx = lsa[0] + (lsb[0] - lsa[0]) * t
        ry = lsa[1] + (lsb[1] - lsa[1]) * t
        rz = lsa[2] + (lsb[2] - lsa[2]) * t
        beam3((rx, ry - 0.5, rz), (rx, ry + 0.5, rz), 0.07, 0.07, 'wa_plank_dark')
    # steps up to the raised floor
    for k in range(3):
        box(nm('step'), (dw + 0.4 - k * 0.3, 1.0, 0.5), loc=(0, fy - 0.8 - k * 0.5, 0.25 + k * 0.5), key='wa_plank_dark', bev=0.03)
    return finalize('rusty_hut_5', smooth_angle=30)


def rusty_hut_6():
    """A04_06 - sandstone base with a timber loft, open lean-to porch with a cart wheel, barrels and a rope coil."""
    reset()
    W, D, H = 15.0, 12.0, 6.5
    _floor(W, D, key='wa_sand_dark')
    # sandstone ground storey
    fy, dw = _walls_box(W, D, H, 0.7, 'wa_sand', door_w=4.5)
    _door(fy, dw)
    fr = faces(0, 0, W, D)['front']
    _window(fr, W / 2 - 3.2, 2.6)
    rnd = random.Random(46)
    for face, L in (('back', W), ('left', D), ('right', D)):
        f2 = faces(0, 0, W, D)[face]
        for c in range(4):
            z = 0.8 + c * 1.3
            for i in range(int(L / 2.4)):
                x = -L / 2 + 1.0 + i * 2.4 + (1.2 if c % 2 else 0)
                lbox(f2, (2.0, 0.14, 1.1), x, -0.07, z, rnd.choice(['wa_sand', 'wa_sand_dark']), bev=0.03)
    # timber loft above
    loftH = 4.0
    box(nm('loft'), (W - 1.0, D - 1.0, loftH), loc=(0, 0.5, H + loftH / 2), key='wa_plank')
    lw, ld = W - 1.0, D - 1.0
    lfront = faces(0, 0.5, lw, ld, H)['front']
    for k in range(int(lw / 1.5)):
        lbox(lfront, (0.2, 0.3, loftH), -lw / 2 + 0.3 + k * 1.5, -0.1, loftH / 2, 'wa_plank_dark')
    _window(lfront, 0, 1.2, w=2.0, h=2.0)
    # loft gable roof
    import mathutils
    hr = 2.4
    a = math.atan2(hr, (W - 1) / 2)
    top = H + loftH
    for s in (-1, 1):
        quad = [(0, -D / 2 - 0.4, top + hr), (s * ((W - 1) / 2 + 0.5), -D / 2 - 0.4, top - 0.3),
                (s * ((W - 1) / 2 + 0.5), D / 2 + 0.4, top - 0.3), (0, D / 2 + 0.4, top + hr)]
        slab(quad, (0, 0, 0.2), 'wa_tin_rust' if s < 0 else 'wa_tin_grey')
    box(nm('ridge'), (0.4, D + 0.8, 0.4), loc=(0, 0, top + hr), key='wa_plank_dark')
    for yy in (-D / 2 + 0.5, D / 2 - 0.5):
        slab([(-(W - 1) / 2, yy, top), ((W - 1) / 2, yy, top), (0, yy, top + hr)], (0, (0.3 if yy < 0 else -0.3), 0), 'wa_plank')
    # open lean-to porch on the -X side
    px = -W / 2 - 3.0
    lslab(F(), [(px, -D / 2 + 1, 5.5), (-W / 2, -D / 2 + 1, 6.5), (-W / 2, D / 2 - 1, 6.5), (px, D / 2 - 1, 5.5)], (0, 0, 0.2), 'wa_tin_grey')
    for yy in (-D / 2 + 1.5, D / 2 - 1.5):
        cyl(nm('ppole'), 0.22, 5.5, loc=(px + 0.3, yy, 0), key='wa_plank_dark', verts=8)
    # cart wheel leaning on the porch
    from props import wheel
    import bpy
    before = set(o.name for o in bpy.context.scene.objects)
    wheel(nm('wh'), 1.8, (px + 0.8, -1.5, 1.8), axis='Y', key='wa_plank_dark', spokes=8)
    for o in bpy.context.scene.objects:
        if o.name not in before:
            o.rotation_euler.x += math.radians(12)
    # barrels + rope coil
    from props import barrel_body
    barrel_body(nm('b1'), loc=(px + 1.0, 1.5, 0.0), h=2.6)
    barrel_body(nm('b2'), loc=(px + 1.2, 3.0, 0.0), h=2.6)
    for k in range(4):
        torus(nm('rope'), 0.8 - k * 0.1, 0.12, loc=(px + 1.0, -3.2, 0.2 + k * 0.18), key='wa_tarp', segs=16, rsegs=4)
    _steps(fy, dw)
    return finalize('rusty_hut_6', smooth_angle=30)


# ---- helpers for raised-floor huts (A04_05) and loft frames (A04_06) ----
def _walls_box2(W, D, H, t, wall_key, base, door_w=4.5, door_h=7.0):
    box(nm('back'), (W, t, H), loc=(0, D / 2 - t / 2, base + H / 2), key=wall_key)
    for s in (-1, 1):
        box(nm('side'), (t, D, H), loc=(s * (W / 2 - t / 2), 0, base + H / 2), key=wall_key)
    fy = -D / 2 + t / 2
    dw = door_w
    box(nm('fl'), ((W - dw) / 2, t, H), loc=(-(dw + (W - dw) / 2) / 2, fy, base + H / 2), key=wall_key)
    box(nm('fr'), ((W - dw) / 2, t, H), loc=((dw + (W - dw) / 2) / 2, fy, base + H / 2), key=wall_key)
    box(nm('flin'), (dw, t, H - door_h), loc=(0, fy, base + door_h + (H - door_h) / 2), key=wall_key)
    return fy, dw


def _door_z(fy, dw, base, dh=7.0):
    for s in (-1, 1):
        box(nm('djamb'), (0.25, 0.9, dh), loc=(s * dw / 2, fy, base + dh / 2), key='wa_plank_dark')
    box(nm('dlin'), (dw + 0.5, 0.9, 0.35), loc=(0, fy, base + dh + 0.15), key='wa_plank_dark')
    box(nm('doorp'), (dw - 0.2, 0.2, dh - 0.2), loc=(0, fy - 0.12, base + (dh - 0.2) / 2 + 0.1), key='wa_plank')
    for k in range(4):
        box(nm('dpl'), (0.07, 0.1, dh - 0.4), loc=(-dw / 2 + 0.35 + k * (dw - 0.7) / 3, fy - 0.22, base + dh / 2), key='wa_plank_dark')
    box(nm('dled'), (dw - 0.4, 0.08, 0.2), loc=(0, fy - 0.24, base + dh * 0.5), key='wa_iron')
    v4util.marker('mk_door', (0, fy - 0.1, base + 0.3))


def _window_z(fr, x, z, w=2.4, h=2.6, boarded=False):
    _window(fr, x, z, w=w, h=h, boarded=boarded)


BATCHES = {
    'huts': ('v4_rusty', [('A04_01_rusty_hut_01', rusty_hut_1), ('A04_02_rusty_hut_02', rusty_hut_2),
                          ('A04_03_rusty_hut_03', rusty_hut_3), ('A04_04_rusty_hut_04', rusty_hut_4),
                          ('A04_05_rusty_hut_05', rusty_hut_5), ('A04_06_rusty_hut_06', rusty_hut_6)]),
}
