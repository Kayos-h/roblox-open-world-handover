"""wa shells module: A05-A08 enterable building shells (v4_shells).
Drop-in replacements for the part-built church/hall/lodge in Studio.
Shell = outer walls, roof, tower/spire, floor slab, door + window openings with
glass. NO interior furniture (placed separately). Walls >= 2 thick, hollow nave,
door marker, closed roof underside, a proper interior back wall.
Footprints/door end/tower position match town/rebuild/enterable.py.
Fronts face -Y (the door/tower end).
"""
import math, random
from mathutils import Vector
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus
from arch import (F, faces, lbox, lbeam, beam3, slab, lslab, half_disc, arc_pts, nm,
                  battlements, lancet, lancet_pts, rose_window, gable_roof)
import v4util

PAL = kitlib.PAL
# rusty church palette (weathered sandstone/plaster, dark timber, rust spire)
PAL['wa_rc_wall']   = ((176, 150, 116), 'Sandstone',   0.00, 0.90, 0)
PAL['wa_rc_wall_b'] = ((150, 128, 100), 'Sandstone',   0.00, 0.92, 0)
PAL['wa_rc_trim']   = ((158, 140, 116), 'Limestone',   0.00, 0.88, 0)
PAL['wa_rc_roof']   = ((78, 58, 44),    'Wood',        0.00, 0.88, 0)
PAL['wa_rc_spire']  = ((132, 78, 50),   'CorrodedMetal',0.50, 0.82, 0)
PAL['wa_rc_glass']  = ((150, 120, 70),  'Glass',       0.00, 0.20, 0.15)
PAL['wa_rc_broken'] = ((40, 44, 46),    'Slate',       0.00, 0.95, 0)
PAL['wa_rc_floor']  = ((104, 92, 80),   'Slate',       0.00, 0.95, 0)
# capital cathedral palette (clean pale limestone, blue slate, stained glass)
PAL['wa_cc_wall']   = ((226, 220, 204), 'Limestone',   0.00, 0.80, 0)
PAL['wa_cc_trim']   = ((238, 232, 220), 'Marble',      0.00, 0.50, 0)
PAL['wa_cc_roof']   = ((54, 72, 104),   'Slate',       0.00, 0.78, 0)
PAL['wa_cc_spire']  = ((60, 80, 116),   'Slate',       0.00, 0.78, 0)
PAL['wa_cc_floor']  = ((206, 198, 182), 'Marble',      0.00, 0.55, 0)
PAL['wa_cc_gold']   = ((222, 184, 74),  'Metal',       1.00, 0.30, 0)
# tavern palette (half-timber seaside)
PAL['wa_tv_base']   = ((120, 112, 102), 'Cobblestone', 0.00, 0.90, 0)
PAL['wa_tv_plaster']= ((224, 212, 186), 'Plaster',     0.00, 0.90, 0)
PAL['wa_tv_timber'] = ((84, 56, 38),    'Wood',        0.00, 0.88, 0)
PAL['wa_tv_roof']   = ((112, 54, 46),   'Slate',       0.00, 0.82, 0)
PAL['wa_tv_glass']  = ((230, 190, 120), 'Glass',       0.00, 0.20, 0.25)
PAL['wa_tv_floor']  = ((140, 100, 66),  'WoodPlanks',  0.00, 0.85, 0)
# lodge palette (timber on stone, snow)
PAL['wa_lo_base']   = ((132, 124, 114), 'Cobblestone', 0.00, 0.90, 0)
PAL['wa_lo_wall']   = ((128, 84, 50),   'Wood',        0.00, 0.88, 0)
PAL['wa_lo_timber'] = ((78, 52, 34),    'Wood',        0.00, 0.88, 0)
PAL['wa_lo_roof']   = ((86, 58, 40),    'WoodPlanks',  0.00, 0.90, 0)
PAL['wa_lo_snow']   = ((236, 242, 248), 'Snow',        0.00, 0.72, 0)
PAL['wa_lo_glass']  = ((240, 200, 130), 'Glass',       0.00, 0.20, 0.3)
PAL['wa_lo_floor']  = ((146, 104, 68),  'WoodPlanks',  0.00, 0.85, 0)
PAL['wa_ice']       = ((210, 234, 244), 'Ice',         0.00, 0.22, 0)


def _hollow_box(W, L, H, t, wall_key, floor_key, cz=0.0):
    """Four walls (thickness t) + floor slab, hollow interior. Centred at origin, front=-Y."""
    box(nm('floor'), (W, L, 0.8), loc=(0, 0, cz + 0.4), key=floor_key)
    box(nm('back'), (W, t, H), loc=(0, L / 2 - t / 2, cz + H / 2), key=wall_key)       # +Y wall
    for s in (-1, 1):
        box(nm('side'), (t, L, H), loc=(s * (W / 2 - t / 2), 0, cz + H / 2), key=wall_key)


def _gable_closed(W, L, z0, hr, outer_key, under_key, barge_key, overhang=1.0):
    """A closed gable roof spanning W across, ridge along L (front=-Y). Underside closed."""
    a = math.atan2(hr, W / 2)
    Lx = L + 2 * overhang
    for s in (-1, 1):
        ez = z0 - overhang * math.tan(a)
        # outer skin
        quad = [(0, -Lx / 2, z0 + hr), (s * (W / 2 + overhang), -Lx / 2, ez),
                (s * (W / 2 + overhang), Lx / 2, ez), (0, Lx / 2, z0 + hr)]
        slab(quad, (0, 0, 0.4), outer_key)
        # inner underside skin (slightly below, so a viewer inside sees roof not sky)
        iq = [(0, -L / 2, z0 + hr - 0.5), (s * (W / 2 - 0.3), -L / 2, z0 - 0.2),
              (s * (W / 2 - 0.3), L / 2, z0 - 0.2), (0, L / 2, z0 + hr - 0.5)]
        slab(iq, (0, 0, 0.2), under_key)
    # gable end infill triangles (front and back), closed
    for yy in (-L / 2, L / 2):
        slab([(-W / 2, yy, z0), (W / 2, yy, z0), (0, yy, z0 + hr)], (0, (0.5 if yy < 0 else -0.5), 0), outer_key)
    box(nm('ridge'), (0.8, Lx, 0.8), loc=(0, 0, z0 + hr), key=barge_key)
    return a


def _tower(cx, cy, tw, th, wall_key, trim_key, spire_key, spire_h, belfry_z,
           bands=3, spire_segs=4, finial='wa_cc_gold'):
    """Square tower centred at (cx,cy), tw wide, th tall, with belfry openings and a spire."""
    box(nm('tw'), (tw, tw, th), loc=(cx, cy, th / 2), key=wall_key)
    for k in range(bands):
        z = th * (k + 1) / (bands + 1)
        box(nm('twband'), (tw + 0.6, tw + 0.6, 0.6), loc=(cx, cy, z), key=trim_key)
    box(nm('twcap'), (tw + 1.0, tw + 1.0, 0.8), loc=(cx, cy, th - 0.4), key=trim_key)
    # belfry louver openings near the top on each face
    for a in (0, 90, 180, 270):
        ar = math.radians(a)
        fr = F(cx + math.cos(ar) * tw / 2, cy + math.sin(ar) * tw / 2, 0, a + 90)
        pts = lancet_pts(0, belfry_z, belfry_z + tw * 0.55, tw * 0.42)
        lslab(fr, [(px, 0.0, pz) for px, pz in pts], (0, 0.5, 0), 'wa_rc_broken')
        tube(nm('bel'), [fr.p(px, -0.25, pz) for px, pz in pts[1:-1]], 0.25, trim_key, res=4)
    # spire (pyramidal)
    lathe(nm('spire'), [(0.0, 0.0), (tw / 2 * 1.3, 0.0), (0.0, spire_h)], loc=(cx, cy, th + 0.4), key=spire_key, segs=spire_segs)
    if finial:
        lathe(nm('fin'), [(0, 0), (0.4, 0), (0.12, 1.2), (0, 1.6)], loc=(cx, cy, th + 0.4 + spire_h - 0.2), key=finial, segs=6)
        box(nm('finx'), (2.0, 0.3, 0.3), loc=(cx, cy, th + spire_h + 1.0), key=finial)
        box(nm('finv'), (0.3, 0.3, 2.0), loc=(cx, cy, th + spire_h + 1.0), key=finial)


def _church_shell(name, W, L, H, hr, tw, th, spire_h, style, broken=False):
    """Shared church/cathedral shell builder. Tower + door at the -Y (front) end."""
    reset()
    rnd = random.Random(hash(name) & 0xffff)
    wall = style['wall']; wallb = style.get('wall_b', style['wall'])
    trim = style['trim']; roof = style['roof']; spire = style['spire']
    glass = style['glass']; floor = style['floor']; gold = style['gold']
    t = 2.5
    _hollow_box(W, L, H, t, wall, floor)
    # front wall (-Y) is where the tower sits; cut a tall arched door in it
    fy = -L / 2 + t / 2
    dw, dh = 8.0, 14.0
    box(nm('fl'), ((W - dw) / 2, t, H), loc=(-(dw + (W - dw) / 2) / 2, fy, H / 2), key=wall)
    box(nm('fr'), ((W - dw) / 2, t, H), loc=((dw + (W - dw) / 2) / 2, fy, H / 2), key=wall)
    box(nm('flin'), (dw, t, H - dh), loc=(0, fy, dh + (H - dh) / 2), key=wall)
    # double door
    ffr = faces(0, 0, W, L)['front']
    for s in (-1, 1):
        lbox(ffr, (dw / 2 - 0.2, 1.0, dh - 0.4), s * dw / 4, -0.3, (dh - 0.4) / 2 + 0.2, roof)
        for k in range(3):
            lbox(ffr, (0.12, 0.2, dh - 0.8), s * (0.4 + k * (dw / 2 - 0.6) / 2), -0.85, dh / 2, 'wa_rc_roof' if broken else trim)
    lbox(ffr, (dw + 1.6, 1.0, 1.2), 0, -0.4, dh + 0.3, trim)   # door hood
    v4util.marker('mk_door', (0, fy - 0.2, 0.8))
    # clerestory windows along the nave sides (lancets), with glass; some broken
    for side in ('left', 'right'):
        fr = faces(0, 0, W, L)[side]
        n = int((L - 2 * tw) / 12)
        for i in range(n):
            yy = -L / 2 + tw + 6 + i * 12
            g = 'wa_rc_broken' if (broken and rnd.random() < 0.3) else glass
            lancet(fr, yy, H * 0.35, w=3.0, h=H * 0.5, glass=g, frame=trim, medallion=None, lead=not broken)
    # big window in the +Y (apse) end
    bfr = faces(0, 0, W, L)['back']
    if broken:
        lancet(bfr, -6, H * 0.3, w=3.4, h=H * 0.5, glass=glass, frame=trim, medallion=None)
        lancet(bfr, 6, H * 0.3, w=3.4, h=H * 0.5, glass='wa_rc_broken', frame=trim, medallion=None)
    else:
        rose_window(bfr, 0, H * 0.62, 7.0, keys=('stained_b', 'stained_r', 'stained_y', 'stained_g'), frame=trim)
        for s in (-1, 1):
            lancet(bfr, s * 10, H * 0.25, w=3.0, h=H * 0.4, glass='stained_b', frame=trim, medallion=None)
    # buttresses along the nave
    for side in (-1, 1):
        n = int((L - 2 * tw) / 12)
        for i in range(n + 1):
            yy = -L / 2 + tw + i * 12
            box(nm('butt'), (3.0, 3.0, H * 0.8), loc=(side * (W / 2 + 1.2), yy, H * 0.4), key=wallb, bev=0.1)
            lslab(F(), [(side * W / 2, yy, H * 0.8), (side * (W / 2 + 2.6), yy, H * 0.5), (side * (W / 2 + 2.6), yy, H * 0.58), (side * W / 2, yy, H * 0.88)],
                  (0, 2.0, 0), trim) if not broken else None
    # roof (closed)
    _gable_closed(W, L, H, hr, roof, roof, trim)
    # tower + spire at the -Y (front) end, centred on the front wall, projecting forward
    ty = -L / 2 - tw / 2 + t
    _tower(0, ty, tw, th, wall, trim, spire, spire_h, belfry_z=th - tw * 0.9,
           spire_segs=(4 if broken else 8), finial=gold)
    # tower door (main entrance through the tower base)
    tfr = F(0, ty - tw / 2, 0, 0)
    pts = lancet_pts(0, 0, dh - dw / 2, dw)
    lslab(tfr, [(px, 0.0, pz) for px, pz in pts], (0, 1.0, 0), roof)
    tube(nm('td'), [tfr.p(px, -0.3, pz) for px, pz in pts[1:-1]], 0.4, trim, res=4)
    v4util.marker('mk_door', (0, ty - tw / 2 - 0.2, 0.8))
    if broken:
        # a few rust streaks / missing roof patches
        for k in range(4):
            box(nm('rust'), (4.0, 6.0, 0.3), loc=(rnd.uniform(-W / 4, W / 4), rnd.uniform(-L / 4, L / 4), H + hr * 0.5),
                key='wa_rc_spire', rot=(0, rnd.uniform(-10, 10), 0))
    return finalize(name, smooth_angle=25)


# ----------------------------------------------------------------- A05 / A06
def shell_rusty_church():
    """A05_01 - 60x124, wall 44, roof rise 30, front tower 26 wide / 104 tall, 52 spire. Rusty, broken windows."""
    style = {'wall': 'wa_rc_wall', 'wall_b': 'wa_rc_wall_b', 'trim': 'wa_rc_trim', 'roof': 'wa_rc_roof',
             'spire': 'wa_rc_spire', 'glass': 'wa_rc_glass', 'floor': 'wa_rc_floor', 'gold': 'wa_rc_spire'}
    return _church_shell('shell_rusty_church', 60, 124, 44, 30, 26, 104, 52, style, broken=True)


def shell_capital_cathedral():
    """A06_01 - 56x116, wall 46, roof rise 30, front tower 24 wide / 112 tall, 58 spire. Grand, clean."""
    style = {'wall': 'wa_cc_wall', 'wall_b': 'wa_cc_wall', 'trim': 'wa_cc_trim', 'roof': 'wa_cc_roof',
             'spire': 'wa_cc_spire', 'glass': 'stained_b', 'floor': 'wa_cc_floor', 'gold': 'wa_cc_gold'}
    return _church_shell('shell_capital_cathedral', 56, 116, 46, 30, 24, 112, 58, style, broken=False)


# ----------------------------------------------------------------- A07 tavern
def shell_harbour_tavern():
    """A07_01 - 30x40, wall 14, roof rise 10. Half-timber seaside tavern, hanging sign, chimney, porch, shutters, lantern brackets."""
    reset()
    W, L, H, hr = 30.0, 40.0, 14.0, 10.0
    t = 2.0
    # stone base storey (lower 4) + plaster + timber frame
    box(nm('floor'), (W, L, 0.8), loc=(0, 0, 0.4), key='wa_tv_floor')
    box(nm('base'), (W, L, 4.0), loc=(0, 0, 2.0), key='wa_tv_base')
    box(nm('back'), (W, t, H), loc=(0, L / 2 - t / 2, H / 2), key='wa_tv_plaster')
    for s in (-1, 1):
        box(nm('side'), (t, L, H), loc=(s * (W / 2 - t / 2), 0, H / 2), key='wa_tv_plaster')
    fy = -L / 2 + t / 2
    dw, dh = 5.0, 9.0
    box(nm('fl'), ((W - dw) / 2, t, H), loc=(-(dw + (W - dw) / 2) / 2, fy, H / 2), key='wa_tv_plaster')
    box(nm('fr'), ((W - dw) / 2, t, H), loc=((dw + (W - dw) / 2) / 2, fy, H / 2), key='wa_tv_plaster')
    box(nm('flin'), (dw, t, H - dh), loc=(0, fy, dh + (H - dh) / 2), key='wa_tv_plaster')
    # door
    ffr = faces(0, 0, W, L)['front']
    lbox(ffr, (dw - 0.4, 0.8, dh - 0.3), 0, -0.3, (dh - 0.3) / 2 + 0.15, 'wa_tv_timber')
    v4util.marker('mk_door', (0, fy - 0.2, 0.6))
    # half-timber frame on the upper storey (exposed beams)
    for face in ('front', 'back', 'left', 'right'):
        fr = faces(0, 0, W, L)[face]
        Lf = W if face in ('front', 'back') else L
        for k in range(int(Lf / 4)):
            x = -Lf / 2 + 2 + k * 4
            lbox(fr, (0.5, 0.3, H - 4.5), x, -0.1, 4 + (H - 4.5) / 2, 'wa_tv_timber')
        lbox(fr, (Lf, 0.4, 0.5), 0, -0.1, 4.2, 'wa_tv_timber')
        lbox(fr, (Lf, 0.4, 0.5), 0, -0.1, H - 0.4, 'wa_tv_timber')
    # windows with shutters + glass
    for side in ('left', 'right'):
        fr = faces(0, 0, W, L)[side]
        for i in range(3):
            yy = -L / 2 + 8 + i * 12
            _win_glass(fr, yy, 6.0, 3.6, 4.0, 'wa_tv_glass', 'wa_tv_timber')
    for x in (-8, 8):
        _win_glass(ffr, x, 6.0, 3.6, 4.0, 'wa_tv_glass', 'wa_tv_timber')
    _win_glass(faces(0, 0, W, L)['back'], 0, 6.0, 4.0, 4.0, 'wa_tv_glass', 'wa_tv_timber')
    # gable roof (ridge along L)
    _gable_closed(W, L, H, hr, 'wa_tv_roof', 'wa_tv_roof', 'wa_tv_timber', overhang=1.4)
    # chimney
    box(nm('chim'), (3.0, 3.0, H + hr + 4), loc=(W / 2 - 4, L / 2 - 6, (H + hr + 4) / 2), key='wa_tv_base')
    box(nm('chimcap'), (3.6, 3.6, 0.6), loc=(W / 2 - 4, L / 2 - 6, H + hr + 4), key='wa_tv_timber')
    # covered porch over the door
    lslab(F(0, fy, 0, 0), [(-dw / 2 - 2, 0, dh + 1.5), (dw / 2 + 2, 0, dh + 1.5), (dw / 2 + 2, -5, dh - 0.5), (-dw / 2 - 2, -5, dh - 0.5)],
          (0, 0, 0.3), 'wa_tv_roof')
    for s in (-1, 1):
        cyl(nm('ppost'), 0.4, dh - 0.5, loc=(s * (dw / 2 + 1.5), fy - 4.6, 0), key='wa_tv_timber', verts=8)
    # hanging sign
    lbeam(ffr.sub(0, 0, 0), (dw / 2 + 4, -0.2, H - 2), (dw / 2 + 4, -4, H - 2), 0.3, 'wa_iron' if 'wa_iron' in PAL else 'iron')
    lbox(ffr, (0.3, 3.0, 2.4), dw / 2 + 4, -4, H - 4, 'wa_tv_timber')
    # lantern brackets
    for x in (-dw / 2 - 2, dw / 2 + 2):
        lbeam(ffr.sub(0, 0, 0), (x, -0.2, dh + 0.5), (x, -1.6, dh + 0.5), 0.15, 'iron')
        lathe(nm('lan'), [(0, 0), (0.5, 0), (0.5, 1.0), (0, 1.0)], loc=ffr.p(x, -1.6, dh - 0.5), key='wa_tv_glass', segs=6)
    return finalize('shell_harbour_tavern', smooth_angle=28)


def _win_glass(fr, x, z, w, h, glass, frame, arch=False):
    """A simple glazed window opening in frame fr; z = bottom."""
    lbox(fr, (w, 0.3, h), x, -0.02, z + h / 2, glass)
    for s in (-1, 1):
        lbox(fr, (0.3, 0.4, h + 0.4), x + s * (w / 2 + 0.12), -0.14, z + h / 2, frame)
    lbox(fr, (w + 0.7, 0.4, 0.3), x, -0.14, z + h + 0.15, frame)
    lbox(fr, (w + 0.8, 0.5, 0.3), x, -0.2, z - 0.15, frame)
    lbox(fr, (0.14, 0.26, h), x, -0.1, z + h / 2, frame)
    lbox(fr, (w, 0.26, 0.14), x, -0.1, z + h / 2, frame)


# ----------------------------------------------------------------- A08 lodge
def shell_alpine_lodge():
    """A08_01 - 30x44, wall 15, roof rise 13. Big timber lodge on a stone base, deep snow roof + icicles, porch, stone chimney, warm glow."""
    reset()
    W, L, H, hr = 30.0, 44.0, 15.0, 13.0
    t = 2.0
    box(nm('floor'), (W, L, 0.8), loc=(0, 0, 0.4), key='wa_lo_floor')
    # stone base (lower 5)
    box(nm('base'), (W + 0.6, L + 0.6, 5.0), loc=(0, 0, 2.5), key='wa_lo_base')
    box(nm('back'), (W, t, H), loc=(0, L / 2 - t / 2, H / 2), key='wa_lo_wall')
    for s in (-1, 1):
        box(nm('side'), (t, L, H), loc=(s * (W / 2 - t / 2), 0, H / 2), key='wa_lo_wall')
    fy = -L / 2 + t / 2
    dw, dh = 5.0, 9.0
    box(nm('fl'), ((W - dw) / 2, t, H), loc=(-(dw + (W - dw) / 2) / 2, fy, H / 2), key='wa_lo_wall')
    box(nm('fr'), ((W - dw) / 2, t, H), loc=((dw + (W - dw) / 2) / 2, fy, H / 2), key='wa_lo_wall')
    box(nm('flin'), (dw, t, H - dh), loc=(0, fy, dh + (H - dh) / 2), key='wa_lo_wall')
    ffr = faces(0, 0, W, L)['front']
    lbox(ffr, (dw - 0.4, 0.8, dh - 0.3), 0, -0.3, (dh - 0.3) / 2 + 0.15, 'wa_lo_timber')
    v4util.marker('mk_door', (0, fy - 0.2, 0.6))
    # exposed log/timber courses on the walls
    for face in ('front', 'back', 'left', 'right'):
        fr = faces(0, 0, W, L)[face]
        Lf = W if face in ('front', 'back') else L
        for k in range(int((H - 5) / 1.5)):
            z = 5.3 + k * 1.5
            if face == 'front' and z < dh:
                continue
            lbox(fr, (Lf, 0.3, 0.2), 0, -0.1, z, 'wa_lo_timber')
    # windows with warm glow + glass
    for side in ('left', 'right'):
        fr = faces(0, 0, W, L)[side]
        for i in range(3):
            yy = -L / 2 + 9 + i * 13
            _win_glass(fr, yy, 7.0, 3.6, 4.4, 'wa_lo_glass', 'wa_lo_timber')
    for x in (-8, 8):
        _win_glass(ffr, x, 7.0, 3.4, 4.0, 'wa_lo_glass', 'wa_lo_timber')
    _win_glass(faces(0, 0, W, L)['back'], 0, 8.0, 5.0, 5.0, 'wa_lo_glass', 'wa_lo_timber')
    # deep snow gable roof
    a = _gable_closed(W, L, H, hr, 'wa_lo_roof', 'wa_lo_roof', 'wa_lo_timber', overhang=2.0)
    # snow layer on each slope
    import mathutils
    for s in (-1, 1):
        ez = H - 2.0 * math.tan(a)
        quad = [(0, -L / 2 - 2, H + hr), (s * (W / 2 + 2), -L / 2 - 2, ez),
                (s * (W / 2 + 2), L / 2 + 2, ez), (0, L / 2 + 2, H + hr)]
        n = mathutils.Vector((-s * math.sin(a), 0, math.cos(a))) * 0.7
        sq = [(p[0] + n.x, p[1], p[2] + n.z) for p in quad]
        slab(sq, (0, 0, 0.5), 'wa_lo_snow')
    box(nm('snowridge'), (1.4, L + 4, 0.6), loc=(0, 0, H + hr + 0.7), key='wa_lo_snow', bev=0.1)
    # icicles along the front eave
    for i in range(10):
        x = -W / 2 + W * (i + 0.5) / 10
        hh = random.Random(i + 80).uniform(1.0, 2.4)
        lathe(nm('ice'), [(0.25, 0), (0.0, -hh)], loc=(x, -L / 2 - 2, H - 2.0 * math.tan(a) - 0.1), key='wa_ice', segs=6)
    # covered porch
    lslab(F(0, fy, 0, 0), [(-dw / 2 - 3, 0, dh + 2), (dw / 2 + 3, 0, dh + 2), (dw / 2 + 3, -6, dh - 1), (-dw / 2 - 3, -6, dh - 1)],
          (0, 0, 0.4), 'wa_lo_roof')
    box(nm('porchsnow'), (dw + 6.5, 6.5, 0.4), loc=(0, fy - 3, dh + 2.2), key='wa_lo_snow', rot=(14, 0, 0))
    for s in (-1, 1):
        cyl(nm('ppost'), 0.5, dh - 1, loc=(s * (dw / 2 + 2.5), fy - 5.6, 0), key='wa_lo_timber', verts=8)
    # stone chimney
    box(nm('chim'), (4.0, 4.0, H + hr + 3), loc=(W / 2 - 5, L / 2 - 8, (H + hr + 3) / 2), key='wa_lo_base')
    box(nm('chimcap'), (4.6, 4.6, 0.7), loc=(W / 2 - 5, L / 2 - 8, H + hr + 3), key='wa_lo_timber')
    return finalize('shell_alpine_lodge', smooth_angle=28)


BATCHES = {
    'church':    ('v4_shells', [('A05_01_shell_rusty_church_01', shell_rusty_church)]),
    'cathedral': ('v4_shells', [('A06_01_shell_capital_cathedral_01', shell_capital_cathedral)]),
    'tavern':    ('v4_shells', [('A07_01_shell_harbour_tavern_01', shell_harbour_tavern)]),
    'lodge':     ('v4_shells', [('A08_01_shell_alpine_lodge_01', shell_alpine_lodge)]),
}
