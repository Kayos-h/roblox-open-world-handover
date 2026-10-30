"""E. Alpine village. Fronts face -Y. Snow everywhere it would settle."""
import math, random
from mathutils import Vector
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, top_paint, flame, chain
from arch import (F, faces, lbox, lbeam, beam3, slab, lslab, window, door, quoins, band, gable_roof, roof_z, cone_roof, chimney,
                  railing, wall_lantern, arc_pts, nm, flower_box, timber_frame)
from capital import stone_face, hanging_sign
from nature import blob, rock, _pine, _bush

SH = ('roof_old', 'roof_old_b')


def snow_roof(f, L, D, z0, hr, ov=1.0, ovg=0.9, icicles=True, seed=0):
    """Snow blanket and icicles matching gable_roof(f, L, D, z0, hr, ov, ovg)."""
    rnd = random.Random(seed)
    a = math.atan2(hr, D / 2)
    hw = D / 2 + ov
    S = hw / math.cos(a)
    zr = z0 + hr
    LL = L + 2 * ovg
    for s in (-1, 1):
        nrm = Vector((0, s * math.sin(a), math.cos(a)))
        dirv = Vector((0, s * math.cos(a), -math.sin(a)))
        c = Vector((0, 0, zr)) + dirv * (S / 2 + 0.05) + nrm * 0.62
        lbox(f, (LL - 0.1, S + 0.1, 0.55), 0, c.y, c.z, 'snow', rot=(-s * math.degrees(a), 0, 0), bev=0.22)
        e = Vector((0, 0, zr)) + dirv * S + nrm * 0.45
        lbeam(f, (-LL / 2 + 0.2, e.y, e.z), (LL / 2 - 0.2, e.y, e.z), 0.7, 'snow', 0.55)
        if icicles:
            n = int(LL / 0.9)
            for i in range(n):
                if rnd.random() < 0.35:
                    continue
                x = -LL / 2 + 0.4 + (LL - 0.8) * i / max(1, n - 1)
                h = rnd.uniform(0.4, 1.4)
                p = f.p(x, e.y + s * 0.1, e.z - 0.45)
                lathe(nm('ic'), [(0, 0), (0.12, 0), (0, -h)], loc=p, key='glass', segs=5)
    lbeam(f, (-LL / 2, 0, zr + 0.85), (LL / 2, 0, zr + 0.85), 1.0, 'snow', 0.6)


def logs_face(f, L, z0, z1, key='wood', step=0.9):
    n = int((z1 - z0) / step)
    for i in range(n):
        z = z0 + step * (i + 0.5)
        tube(nm('lg'), [f.p(-L / 2 - 0.4, -0.15, z), f.p(L / 2 + 0.4, -0.15, z)], step * 0.48, key, res=4, ures=1)


def carved_rail(f, x0, x1, z, y, h=2.2, key='wood_light'):
    lbox(f, (x1 - x0, 0.3, 0.3), (x0 + x1) / 2, y, z + h, key)
    lbox(f, (x1 - x0, 0.25, 0.25), (x0 + x1) / 2, y, z + 0.2, key)
    n = int((x1 - x0) / 0.55)
    for i in range(n):
        x = x0 + (x1 - x0) * (i + 0.5) / n
        lbox(f, (0.42, 0.12, h - 0.3), x, y, z + h / 2 + 0.05, key)
        if i % 2 == 0:
            ball(nm('cut'), 0.11, loc=f.p(x, y - 0.08, z + h * 0.55), key='hole', segs=6, rings=4, scale=(1, 0.4, 1.4))


def heart_shutters(f, x, z, w, h, key):
    for s in (-1, 1):
        cx = x + s * (w / 2 + 0.75)
        lbox(f, (1.2, 0.14, h), cx, -0.1, z + h / 2, key)
        ball(nm('ht'), 0.16, loc=f.p(cx - 0.1, -0.2, z + h * 0.7), key='hole', segs=6, rings=4, scale=(1, 0.3, 1))
        ball(nm('ht'), 0.16, loc=f.p(cx + 0.1, -0.2, z + h * 0.7), key='hole', segs=6, rings=4, scale=(1, 0.3, 1))
        lathe(nm('hp'), [(0, 0), (0.2, 0), (0, -0.25)], loc=f.p(cx, -0.2, z + h * 0.66), key='hole', segs=4)


def chalet_body(cx=0.0, w=18.0, d=14.0, floors=2, sh=7.0, fh=7.0, wood='wood', shutter='shutter_g', flowers=('fl_red', 'fl_pink'),
                balcony=True, pitch=0.36, seed=0, lit=(), woodpile=True, door_x=None, sign=None):
    rnd = random.Random(seed)
    box(nm('gs'), (w, d, sh), loc=(cx, 0, sh / 2), key='stone')
    fs = faces(cx, 0, w, d)
    for k, fr in enumerate(fs.values()):
        stone_face(fr, -6, 6, 0.4, sh - 0.6, 18, seed + k, keys=('stone', 'stone_dark', 'stone_light'))
    dxp = door_x if door_x is not None else -w / 4
    door(fs['front'], dxp, w=3.2, h=6.0, arch=False, key='wood_dark', surround='wood_dark', step='stone_dark', lamp=True)
    for x in (w / 4,):
        window(fs['front'], x, 2.2, w=2.0, h=2.6, frame='wood_light', sill='wood_dark', lit=(0, 0) in lit)
        heart_shutters(fs['front'], x, 2.2, 2.0, 2.6, shutter)
    for side in ('left', 'right', 'back'):
        L = d if side in ('left', 'right') else w
        for x in ((-L / 4, L / 4) if L > 12 else (0,)):
            window(fs[side], x, 2.4, w=1.8, h=2.4, frame='wood_light', sill='wood_dark')
    z = sh
    for k in range(floors - 1):
        box(nm('up'), (w, d, fh), loc=(cx, 0, z + fh / 2), key=wood)
        fu = faces(cx, 0, w, d, z)
        for side in ('front', 'back', 'left', 'right'):
            L = w if side in ('front', 'back') else d
            logs_face(fu[side], L, 0.0, fh, key=wood if k % 2 == 0 else 'wood_light')
            for x in ((-L / 3, 0, L / 3) if L > 16 else ((-L / 4, L / 4) if L > 10 else (0,))):
                window(fu[side], x, 1.8, w=2.2, h=3.2, frame='wood_light', sill='wood_dark', lit=(side == 'front' and (k + 1, x) in lit) or (side == 'front' and rnd.random() < 0.3))
                heart_shutters(fu[side], x, 1.8, 2.2, 3.2, shutter)
                if side == 'front' and not balcony:
                    flower_box(fu[side], x, 1.55, 2.6, flowers)
        for sx in (-1, 1):
            for sy in (-1, 1):
                for i in range(int(fh / 0.9)):
                    box(nm('lx'), (0.9, 0.9, 0.86), loc=(cx + sx * (w / 2 + 0.25), sy * (d / 2 + 0.25), z + 0.45 + i * 0.9), key='wood_dark')
        z += fh
    top = z
    hr = w * pitch
    fr = F(cx, 0, 0, 90)
    gable_roof(fr, d, w, top, hr, keys=SH, wall=wood, ov=2.6, ovg=2.4, barge='wood_dark', infill=True)
    snow_roof(fr, d, w, top, hr, ov=2.6, ovg=2.4, seed=seed)
    for side in ('front', 'back'):
        fg = faces(cx, 0, w, d, top)[side]
        n = int(w / 0.8)
        for i in range(n):
            x = -w / 2 + w * (i + 0.5) / n
            hh = hr * (1 - abs(x) / (w / 2)) - 0.3
            if hh > 0.4:
                lbox(fg, (w / n - 0.06, 0.12, hh), x, -0.12, hh / 2, 'wood_light')
        window(fg, 0, 1.0, w=1.8, h=2.4, frame='wood_dark', sill='wood_dark', lit=(side == 'front'))
        heart_shutters(fg, 0, 1.0, 1.8, 2.4, shutter)
        for s in (-1, 1):
            pts = [fg.p(s * (w / 2 + 2.4) * t, -0.5, hr * (1 - t) - 0.9 + 2.4 * math.tan(math.atan2(hr, w / 2)) * 0) for t in (0.0, 0.25, 0.5, 0.75, 1.0)]
            for i, p in enumerate(pts[1:]):
                ball(nm('bb'), 0.22, loc=p, key='wood_dark', segs=6, rings=4)
    if balcony:
        fb = faces(cx, 0, w, d, sh)['front']
        lbox(fb, (w + 1.0, 2.6, 0.4), 0, -1.3, 0.0, 'wood_dark')
        for x in (-w / 2, -w / 6, w / 6, w / 2):
            lbeam(fb, (x, -0.1, -2.2), (x, -2.4, -0.2), 0.4, 'wood_dark')
        carved_rail(fb, -w / 2 - 0.4, w / 2 + 0.4, 0.2, -2.5, key='wood_light')
        for x in (-w / 3, 0, w / 3):
            flower_box(fb.sub(0, -2.0, 0), x, 2.6, 3.0, flowers)
        lbox(fb, (w + 1.2, 2.8, 0.5), 0, -1.3, 2.75, 'snow', bev=0.2) if False else None
    chimney(cx - w / 4, d * 0.2, top, top + hr + 3.0, w=2.0, key='stone')
    box(nm('chs'), (2.6, 2.6, 0.5), loc=(cx - w / 4, d * 0.2, top + hr + 3.5), key='snow', bev=0.2)
    if woodpile:
        for i in range(4):
            for j in range(int(d / 1.1) - 2):
                cyl(nm('fw'), 0.5, 2.2, loc=(cx + w / 2 + 0.3, -d / 2 + 1.6 + j * 1.05, 0.55 + i * 0.95), key=rnd.choice(['bark', 'wood_light']), verts=7,
                    rot=(0, 90, rnd.uniform(-5, 5)))
        box(nm('fwr'), (3.0, d - 2.4, 0.3), loc=(cx + w / 2 + 1.3, 0, 4.6), key='wood_dark', rot=(0, -12, 0))
        box(nm('fws'), (3.2, d - 2.2, 0.4), loc=(cx + w / 2 + 1.3, 0, 4.95), key='snow', rot=(0, -12, 0), bev=0.15)
    if sign:
        hanging_sign(faces(cx, 0, w, d)['front'], dxp + 3.0, sh - 0.6, board=sign)
    for i in range(8):
        blob(nm('sd'), rnd.uniform(0.8, 1.4), (cx + rnd.uniform(-w / 2, w / 2), rnd.choice((-1, 1)) * (d / 2 + 0.6), 0.0), 'snow', subdiv=2, amp=0.1,
             scale=(1.6, 0.8, 0.45), seed=seed + i)
    return top + hr


def _chalet(name, **kw):
    reset()
    chalet_body(**kw)
    return finalize(name, smooth_angle=30)


def chalet_1():
    """E1 - chalet: stone base, log upper floor, wraparound balcony with red flowers, green heart shutters, snowy roof."""
    return _chalet('chalet_1', seed=501)


def chalet_2():
    """E2 - tall chalet: three storeys, light wood, blue shutters, no balcony (flower boxes instead)."""
    return _chalet('chalet_2', w=14.0, d=13.0, floors=3, wood='wood_light', shutter='shutter_b', flowers=('fl_white', 'fl_purple'), balcony=False, seed=502, pitch=0.42)


def chalet_3():
    """E3 - wide farm chalet: dark wood, red shutters, balcony, bigger woodpile."""
    return _chalet('chalet_3', w=22.0, d=15.0, floors=2, wood='wood_dark', shutter='shutter_r', flowers=('fl_red', 'fl_yellow'), seed=503, pitch=0.32)


def chalet_4():
    """E4 - small cabin chalet: one log floor over a short stone base, steep snowy roof."""
    return _chalet('chalet_4', w=12.0, d=11.0, floors=2, sh=5.0, fh=6.0, wood='wood', shutter='shutter_g', flowers=('fl_pink', 'fl_white'),
                   balcony=False, seed=504, pitch=0.5, woodpile=True)


def lodge():
    """E5 - mountain lodge / inn: big three-storey chalet with two balconies, hanging inn sign and lit windows."""
    reset()
    top = chalet_body(w=26.0, d=18.0, floors=3, wood='wood', shutter='shutter_r', flowers=('fl_red', 'fl_pink', 'fl_white'), seed=505, pitch=0.34,
                      sign='shutter_r', door_x=0.0)
    fb = faces(0, 0, 26.0, 18.0, 14.0)['front']
    lbox(fb, (27.0, 2.6, 0.4), 0, -1.3, 0.0, 'wood_dark')
    carved_rail(fb, -13.4, 13.4, 0.2, -2.5, key='wood_light')
    for x in (-8.0, 0.0, 8.0):
        flower_box(fb.sub(0, -2.0, 0), x, 2.6, 3.0, ('fl_red', 'fl_white'))
    for x in (-13.0, -4.3, 4.3, 13.0):
        lbeam(fb, (x, -0.1, -2.2), (x, -2.4, -0.2), 0.4, 'wood_dark')
    from props import barrel_body
    barrel_body(nm('br'), loc=(-6.0, -11.0, 0), h=3.0)
    box(nm('bn'), (5.0, 1.2, 0.3), loc=(5.0, -11.0, 2.0), key='wood')
    for s in (-1, 1):
        box(nm('bnl'), (0.3, 1.0, 2.0), loc=(5.0 + s * 2.0, -11.0, 1.0), key='wood_dark')
    box(nm('bns'), (5.0, 1.2, 0.3), loc=(5.0, -11.0, 2.3), key='snow', bev=0.12)
    return finalize('lodge', smooth_angle=30)


def stone_chapel():
    """E6 - small alpine chapel: white plaster over stone, arched windows, bell tower with green onion dome, snowy roof."""
    reset()
    w, d, h = 12.0, 20.0, 10.0
    box(nm('nv'), (w, d, h), loc=(0, 0, h / 2), key='plaster')
    box(nm('pl'), (w + 0.6, d + 0.6, 1.4), loc=(0, 0, 0.7), key='stone', bev=0.06)
    fs = faces(0, 0, w, d)
    for side in ('left', 'right'):
        for x in (-6.0, 0.0, 6.0):
            window(fs[side], x, 3.5, w=1.8, h=4.4, arch=True, frame='stone_light', sill='stone_light', panes=True, glass='stained_b' if x == 0 else 'glass_dark')
    for k, fr in enumerate((F(-w / 2, -d / 2, 0, 0), F(w / 2, -d / 2, 0, 90), F(w / 2, d / 2, 0, 180), F(-w / 2, d / 2, 0, -90))):
        quoins(fr, 1.4, h - 0.2, 'stone_light', course=1.1)
    door(fs['front'], 0, w=3.0, h=6.0, arch=True, key='wood_dark', surround='stone_light', step='stone')
    window(fs['front'], 0, 7.4, w=1.4, h=1.4, arch=True, frame='stone_light', sill=None, panes=False, glass='stained_y')
    hr = w * 0.6
    fr = F(0, 0, 0, 90)
    gable_roof(fr, d, w, h, hr, keys=SH, wall='plaster', ov=1.0, ovg=0.8, barge='wood_dark')
    snow_roof(fr, d, w, h, hr, ov=1.0, ovg=0.8, seed=6)
    tx, ty, ts, th = 0.0, d / 2 + 2.5, 5.0, 22.0
    box(nm('tw'), (ts, ts, th), loc=(tx, ty, th / 2), key='plaster')
    for k, f2 in enumerate(faces(tx, ty, ts, ts).values()):
        lslab(f2, [(-1.0, 0, 15.5), (1.0, 0, 15.5), (1.0, 0, 18.0)] + [(math.cos(math.radians(a)) * 1.0, 0, 18.0 + math.sin(math.radians(a)) * 1.0) for a in range(20, 161, 20)] + [(-1.0, 0, 18.0)],
              (0, -0.1, 0), 'hole')
        from capital import clock_face
        if k == 0:
            clock_face(f2, 12.0, r=1.4)
    for zz in (h, th - 0.3):
        band(tx, ty, ts, ts, zz, 0.4, 'stone_light', out=0.2)
    lathe(nm('on'), [(0.0, th), (2.9, th), (3.3, th + 1.4), (2.6, th + 3.2), (1.0, th + 4.6), (0.4, th + 5.6), (0.35, th + 6.6), (0.0, th + 6.8)],
          loc=(tx, ty, 0), key='patina', segs=8)
    lathe(nm('ons'), [(0.0, th + 1.3), (3.0, th + 1.3), (2.7, th + 2.2), (1.4, th + 3.6), (0.0, th + 3.7)], loc=(tx, ty, 0), key='snow', segs=8)
    box(nm('cv'), (0.2, 0.2, 2.4), loc=(tx, ty, th + 7.8), key='gold')
    box(nm('ch'), (1.2, 0.2, 0.2), loc=(tx, ty, th + 8.4), key='gold')
    rnd = random.Random(6)
    for i in range(8):
        blob(nm('sd'), rnd.uniform(0.8, 1.4), (rnd.uniform(-w / 2, w / 2), rnd.choice((-1, 1)) * (d / 2 + 0.5), 0.0), 'snow', subdiv=2, amp=0.1, scale=(1.6, 0.8, 0.45), seed=i)
    return finalize('stone_chapel', smooth_angle=30)


def water_wheel(cx, cy, cz, R=6.0, W=2.6, n=12):
    for s in (-1, 1):
        torus(nm('wr'), R, 0.22, loc=(cx, cy + s * W / 2, cz), key='wood_dark', segs=28, rsegs=4, rot=(90, 0, 0))
        torus(nm('wr2'), R * 0.35, 0.18, loc=(cx, cy + s * W / 2, cz), key='wood_dark', segs=14, rsegs=4, rot=(90, 0, 0))
        for k in range(8):
            a = 2 * math.pi * k / 8
            beam3((cx, cy + s * W / 2, cz), (cx + math.cos(a) * R, cy + s * W / 2, cz + math.sin(a) * R), 0.25, 0.25, 'wood_dark')
    for k in range(n * 2):
        a = 2 * math.pi * k / (n * 2)
        c = (cx + math.cos(a) * (R - 0.6), cy, cz + math.sin(a) * (R - 0.6))
        box(nm('pd'), (1.2, W, 0.18), loc=c, key='wood', rot=(0, -math.degrees(a), 0))
    cyl(nm('ax'), 0.5, W + 4.0, loc=(cx, cy - W / 2 - 2.0, cz), key='iron_dark', verts=10, rot=(-90, 0, 0))


def sawmill():
    """E7 - sawmill: timber mill house on a stone base, big water wheel fed by a flume, saw bench and log stack."""
    reset()
    rnd = random.Random(7)
    w, d = 20.0, 14.0
    chalet_body(w=w, d=d, floors=2, sh=5.0, fh=6.0, wood='wood_dark', shutter='shutter_g', flowers=('fl_red',), balcony=False, seed=507, pitch=0.4, woodpile=False)
    water_wheel(w / 2 + 2.0, -1.0, 6.0, R=6.0)
    for s in (-1, 1):
        box(nm('wp'), (1.2, 1.2, 6.0), loc=(w / 2 + 2.0, -1.0 + s * 2.4, 3.0), key='stone', bev=0.06)
    lbeam(F(), (w / 2 + 2.0, -1.0, 13.0), (w / 2 + 14.0, -1.0, 15.0), 2.4, 'wood', 0.25)
    for s in (-1, 1):
        lbeam(F(), (w / 2 + 2.0, -1.0 + s * 1.2, 13.6), (w / 2 + 14.0, -1.0 + s * 1.2, 15.6), 0.25, 'wood_dark', 1.2)
    lbeam(F(), (w / 2 + 2.6, -1.0, 13.35), (w / 2 + 14.0, -1.0, 15.35), 2.0, 'water', 0.1)
    for x in (w / 2 + 6.0, w / 2 + 11.0):
        for s in (-1, 1):
            box(nm('fp'), (0.4, 0.4, 14.0 + (x - w / 2) * 0.16), loc=(x, -1.0 + s * 1.0, (14.0 + (x - w / 2) * 0.16) / 2), key='wood_dark')
    tube(nm('fall'), [(w / 2 + 2.6, -1.0, 13.2), (w / 2 + 1.8, -1.0, 12.4), (w / 2 - 0.2, -1.0, 9.0)], 0.6, 'water_fx', res=6)
    box(nm('pool'), (14.0, 8.0, 0.1), loc=(w / 2 + 3.0, -1.0, 0.05), key='water')
    box(nm('sb'), (12.0, 2.4, 0.4), loc=(-2.0, -d / 2 - 4.0, 2.4), key='wood')
    for x in (-7.0, 3.0):
        for s in (-1, 1):
            box(nm('sbl'), (0.4, 0.4, 2.4), loc=(x, -d / 2 - 4.0 + s * 1.0, 1.2), key='wood_dark')
    cyl(nm('saw'), 1.6, 0.08, loc=(-2.0, -d / 2 - 4.0, 2.6), key='steel', verts=24, rot=(90, 0, 0))
    cyl(nm('lg1'), 0.8, 9.0, loc=(-6.5, -d / 2 - 4.0, 3.4), key='bark', verts=10, rot=(0, 90, 0))
    for i in range(3):
        for j in range(3 - i):
            cyl(nm('lst'), 0.85, 10.0, loc=(-w / 2 - 6.0, -4.0 + j * 1.7 + i * 0.85, 0.85 + i * 1.5), key='bark', verts=10, rot=(90, 0, 0) if False else (0, 0, 0)) if False else \
                cyl(nm('lst'), 0.85, 10.0, loc=(-w / 2 - 1.5 - 10.0, -4.0 + j * 1.7 + i * 0.85, 0.85 + i * 1.5), key='bark', verts=10, rot=(0, 90, 0))
            cyl(nm('lse'), 0.7, 0.05, loc=(-w / 2 - 1.45, -4.0 + j * 1.7 + i * 0.85, 0.85 + i * 1.5), key='wood_light', verts=10, rot=(0, 90, 0))
    box(nm('lsn'), (10.4, 4.0, 0.5), loc=(-w / 2 - 6.5, -2.3, 4.4), key='snow', bev=0.2)
    return finalize('sawmill', smooth_angle=30)


def barn():
    """E8 - alpine barn: stone base, dark plank upper, big barn doors, hay loft, earth ramp, snowy roof."""
    reset()
    rnd = random.Random(8)
    w, d, sh, uh = 24.0, 16.0, 6.0, 9.0
    box(nm('bs'), (w, d, sh), loc=(0, 0, sh / 2), key='stone')
    for k, fr in enumerate(faces(0, 0, w, d).values()):
        stone_face(fr, -8, 8, 0.4, sh - 0.4, 22, 80 + k, keys=('stone', 'stone_dark', 'stone_light'))
    box(nm('up'), (w, d, uh), loc=(0, 0, sh + uh / 2), key='wood_dark')
    for side, L in (('front', w), ('back', w), ('left', d), ('right', d)):
        fr = faces(0, 0, w, d, sh)[side]
        n = int(L / 0.9)
        for i in range(n):
            x = -L / 2 + L * (i + 0.5) / n
            lbox(fr, (L / n - 0.06, 0.12, uh), x, -0.06, uh / 2, rnd.choice(['wood_dark', 'wood', 'wood_rot']))
    fo = faces(0, 0, w, d)['front']
    for s in (-1, 1):
        lbox(fo, (3.0, 0.3, 5.4), s * 1.55, -0.15, 2.7, 'wood')
        lbeam(fo, (s * 0.2, -0.32, 0.3), (s * 2.9, -0.32, 5.1), 0.3, 'wood_dark')
        lbox(fo, (3.0, 0.2, 0.3), s * 1.55, -0.32, 0.3, 'wood_dark')
        lbox(fo, (3.0, 0.2, 0.3), s * 1.55, -0.32, 5.1, 'wood_dark')
    for x in (-8.0, 8.0):
        window(fo, x, 2.2, w=1.6, h=1.6, frame='wood_dark', sill='stone_dark', panes=False)
    hr = d * 0.42
    gable_roof(F(), w, d, sh + uh, hr, keys=SH, wall='wood_dark', ov=1.6, ovg=1.0)
    snow_roof(F(), w, d, sh + uh, hr, ov=1.6, ovg=1.0, seed=8)
    fl = F(-w / 2, 0, sh, -90)
    lbox(fl, (5.0, 0.3, 6.0), 0, -0.15, 3.2, 'wood')
    lbox(fl, (5.6, 0.2, 0.3), 0, -0.32, 6.2, 'wood_dark')
    lslab(F(), [(-w / 2 - 12.0, -3.0, 0.0), (-w / 2, -3.0, 0.0), (-w / 2, -3.0, sh)], (0, 6.0, 0), 'dirt')
    lslab(F(), [(-w / 2 - 12.0, -3.0, 0.05), (-w / 2, -3.0, sh + 0.05), (-w / 2 - 0.0, -3.0, sh + 0.4), (-w / 2 - 12.0, -3.0, 0.4)], (0, 6.0, 0), 'snow')
    for k in range(3):
        box(nm('hb'), (3.4, 2.2, 2.2), loc=(w / 2 + 2.2, -4.0 + k * 2.6, 1.1), key='thatch', bev=0.25)
    box(nm('hbs'), (3.6, 7.6, 0.4), loc=(w / 2 + 2.2, -1.4, 2.4), key='snow', bev=0.18)
    return finalize('barn', smooth_angle=30)


def goat_pen():
    """E9 - goat shelter and pen: small open-front shed, hay rack, water trough and a split-rail paddock."""
    reset()
    rnd = random.Random(9)
    w, d, h = 10.0, 7.0, 6.0
    for side, L in (('back', w), ('left', d), ('right', d)):
        fr = faces(0, d / 2, w, d)[side]
        n = int(L / 0.9)
        for i in range(n):
            x = -L / 2 + L * (i + 0.5) / n
            lbox(fr, (L / n - 0.05, 0.25, h), x, 0.12, h / 2, rnd.choice(['wood', 'wood_dark']))
    for x in (-w / 2 + 0.2, w / 2 - 0.2):
        box(nm('fp'), (0.4, 0.4, h + 0.5), loc=(x, 0.2, (h + 0.5) / 2), key='wood_dark')
    a = math.degrees(math.atan2(1.6, d + 1.4))
    box(nm('rf'), (w + 1.6, d + 2.4, 0.3), loc=(0, d / 2 - 0.4, h + 1.2), key='roof_old', rot=(a, 0, 0))
    box(nm('rfs'), (w + 1.4, d + 2.2, 0.5), loc=(0, d / 2 - 0.4, h + 1.6), key='snow', rot=(a, 0, 0), bev=0.2)
    box(nm('hr'), (4.0, 0.3, 2.0), loc=(0, d - 0.6, 2.6), key='wood_dark')
    for i in range(8):
        lbeam(F(), (-1.8 + i * 0.5, d - 0.6, 1.6), (-1.8 + i * 0.5, d - 1.6, 3.6), 0.1, 'wood_dark')
    blob(nm('hay'), 1.2, (0, d - 1.2, 3.0), 'thatch', subdiv=2, amp=0.25, scale=(1.6, 0.7, 0.8), seed=9)
    box(nm('st'), (w - 0.6, d - 0.6, 0.3), loc=(0, d / 2, 0.15), key='thatch')
    box(nm('tr'), (4.0, 1.4, 1.0), loc=(3.0, -4.0, 0.5), key='wood', bev=0.05)
    box(nm('tw'), (3.6, 1.0, 0.05), loc=(3.0, -4.0, 0.95), key='water')
    pts = [(-w / 2 - 6, -10), (w / 2 + 6, -10), (w / 2 + 6, 0.0)]
    pts2 = [(-w / 2 - 6, 0.0), (-w / 2 - 6, -10)]
    for seq in (pts, pts2):
        for (x0, y0), (x1, y1) in zip(seq, seq[1:]):
            L = math.hypot(x1 - x0, y1 - y0)
            n = max(1, int(L / 4))
            for i in range(n + 1):
                x = x0 + (x1 - x0) * i / n; y = y0 + (y1 - y0) * i / n
                if abs(x) < 2.0 and y < -9:
                    continue
                cyl(nm('fp'), 0.25, 3.4, loc=(x, y, 0), key='wood_dark', verts=7)
                cyl(nm('fps'), 0.3, 0.25, loc=(x, y, 3.4), key='snow', verts=7)
            for z in (1.2, 2.6):
                if y0 == y1 and y0 < -9:
                    lbeam(F(), (x0, y0, z), (-2.0, y1, z), 0.25, 'wood')
                    lbeam(F(), (2.0, y0, z), (x1, y1, z), 0.25, 'wood')
                else:
                    lbeam(F(), (x0, y0, z), (x1, y1, z), 0.25, 'wood')
    return finalize('goat_pen', smooth_angle=30)


def watchtower():
    """E10 - wooden watchtower: four log legs with cross bracing, ladder, railed lookout and a snowy pyramid roof."""
    reset()
    H, s0, s1 = 20.0, 4.0, 2.8
    for sx in (-1, 1):
        for sy in (-1, 1):
            beam3((sx * s0, sy * s0, 0), (sx * s1, sy * s1, H + 6.0), 0.7, 0.7, 'bark')
            cyl(nm('ft'), 0.8, 0.8, loc=(sx * s0, sy * s0, 0), key='stone', verts=8)
    for z0, z1 in ((1.0, 7.0), (7.0, 13.0), (13.0, 19.0)):
        def r(z): return s0 - (s0 - s1) * z / (H + 6.0)
        for (a, b) in (((-1, -1), (1, -1)), ((1, -1), (1, 1)), ((1, 1), (-1, 1)), ((-1, 1), (-1, -1))):
            beam3((a[0] * r(z0), a[1] * r(z0), z0), (b[0] * r(z1), b[1] * r(z1), z1), 0.3, 0.3, 'wood')
            beam3((a[0] * r(z1), a[1] * r(z1), z1), (b[0] * r(z1), b[1] * r(z1), z1), 0.35, 0.35, 'wood')
    box(nm('pl'), (8.0, 8.0, 0.5), loc=(0, 0, H), key='wood_dark')
    for side in ('front', 'back', 'left', 'right'):
        fr = faces(0, 0, 8.0, 8.0, H)[side]
        for i in range(10):
            lbox(fr, (0.7, 0.15, 2.2), -3.6 + i * 0.8, -0.1, 1.4, 'wood')
        lbox(fr, (8.4, 0.3, 0.3), 0, -0.1, 2.6, 'wood_dark')
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(nm('rp'), (0.4, 0.4, 5.6), loc=(sx * 3.8, sy * 3.8, H + 2.8), key='wood_dark')
    lathe(nm('rf'), [(0.0, 0.0), (7.2, 0.0), (0.0, 4.6)], loc=(0, 0, H + 5.6), key='roof_old', segs=4)
    lathe(nm('rfs'), [(0.0, 0.5), (6.6, 0.5), (0.0, 5.0)], loc=(0, 0, H + 5.6), key='snow', segs=4)
    for k in range(3):
        lathe(nm('ic'), [(0, 0), (0.12, 0), (0, -0.9)], loc=(-3.0 + k * 3.0, -5.0, H + 5.5), key='glass', segs=5)
    for x in (-0.7, 0.7):
        lbeam(F(), (x, -s0 - 1.6, 0.0), (x, -4.05, H), 0.18, 'wood')
    for k in range(18):
        t = (k + 0.5) / 18
        lbeam(F(), (-0.7, -s0 - 1.6 + t * (s0 + 1.6 - 4.05), t * H), (0.7, -s0 - 1.6 + t * (s0 + 1.6 - 4.05), t * H), 0.12, 'wood_light')
    wall_lantern(F(0, -4.0, H, 0), 2.6, 2.4)
    return finalize('watchtower', smooth_angle=30)


def covered_bridge():
    """E11 - covered wooden bridge: 36-long truss bridge on stone abutments with plank sides, small windows and a snowy roof."""
    reset()
    L, W, H = 36.0, 9.0, 8.0
    rnd = random.Random(11)
    for s in (-1, 1):
        box(nm('ab'), (6.0, W + 3, 5.0), loc=(s * (L / 2 - 1.0), 0, 2.5), key='stone', bev=0.08)
    box(nm('dk'), (L, W, 0.6), loc=(0, 0, 5.3), key='wood_dark')
    for i in range(int(L / 1.0)):
        box(nm('pk'), (0.95, W - 0.6, 0.12), loc=(-L / 2 + 0.5 + i, 0, 5.66), key=rnd.choice(['wood', 'wood_light']))
    for s in (-1, 1):
        y = s * W / 2
        fr = F(0, y, 5.6, 0 if s < 0 else 180)
        n = int(L / 0.9)
        for i in range(n):
            x = -L / 2 + L * (i + 0.5) / n
            if abs(((x + L / 2) % 6.0) - 3.0) < 0.9 and abs(x) < L / 2 - 3:
                lbox(fr, (L / n - 0.05, 0.2, 2.0), x, 0.1, 0.9, rnd.choice(['wood', 'wood_dark']))
                lbox(fr, (L / n - 0.05, 0.2, 2.6), x, 0.1, H - 1.3, rnd.choice(['wood', 'wood_dark']))
                continue
            lbox(fr, (L / n - 0.05, 0.2, H), x, 0.1, H / 2, rnd.choice(['wood', 'wood_dark', 'wood']))
        for k in range(7):
            x = -L / 2 + 3.0 + k * 5.0
            lbeam(F(), (x, y * 0.92, 5.6), (x + 2.5, y * 0.92, 5.6 + H), 0.4, 'wood_dark')
    for x in (-L / 2, L / 2):
        for s in (-1, 1):
            box(nm('pp'), (0.6, 0.6, H), loc=(x, s * (W / 2 - 0.2), 5.6 + H / 2), key='wood_dark')
        box(nm('lt'), (0.6, W, 0.8), loc=(x, 0, 5.6 + H - 0.4), key='wood_dark')
    hr = 3.6
    fr = F(0, 0, 0, 0)
    gable_roof(fr, L, W, 5.6 + H, hr, keys=SH, wall='wood', ov=1.0, ovg=0.6)
    snow_roof(fr, L, W, 5.6 + H, hr, ov=1.0, ovg=0.6, seed=11)
    for s in (-1, 1):
        lslab(F(s * L / 2, 0, 0, 0), [(0, -W / 2, 5.6 + H), (0, W / 2, 5.6 + H), (0, 0, 5.6 + H + hr)], (-s * 0.3, 0, 0), 'wood_light')
    return finalize('covered_bridge', smooth_angle=30)


def _snowy_pine(seed, h, name, tiers, width, keys, droop):
    return _pine(seed, h, name, snow=True, tiers=tiers, width=width, keys=keys, droop=droop)


def snowy_pine_1():
    """E12 - tall snowy spruce, 40 studs."""
    return _snowy_pine(512, 40, 'snowy_pine_1', 9, 0.21, ('pine_dark', 'pine'), 0.18)


def snowy_pine_2():
    """E13 - full snowy fir, 28 studs."""
    return _snowy_pine(513, 28, 'snowy_pine_2', 6, 0.32, ('pine', 'pine_dark'), 0.12)


def snowy_pine_3():
    """E14 - small snowy pine, 14 studs."""
    return _snowy_pine(514, 14, 'snowy_pine_3', 4, 0.38, ('pine_light', 'pine'), 0.08)


def snowy_rock_1():
    """E15 - snowy boulder cluster."""
    reset()
    for i, (r, p) in enumerate(((4.0, (0, 0, 1.8)), (2.6, (3.6, 1.4, 0.8)), (1.6, (-3.2, -1.6, 0.4)))):
        o = rock(nm('r'), r, p, 'cliff_a' if i % 2 == 0 else 'cliff_b', seed=515 + i, subdiv=3)
        top_paint(o, 'snow', 0.45, i)
    return finalize('snowy_rock_1', smooth_angle=12)


def snowy_rock_2():
    """E16 - tall snowy rock spire."""
    reset()
    o = rock(nm('r'), 3.6, (0, 0, 4.0), 'cliff_b', seed=516, subdiv=3, scale=(0.9, 0.8, 1.8))
    top_paint(o, 'snow', 0.4, 2)
    o2 = rock(nm('r2'), 1.8, (2.6, -1.4, 0.6), 'cliff_a', seed=517, subdiv=3)
    top_paint(o2, 'snow', 0.4, 3)
    blob(nm('sd'), 2.2, (-1.0, -2.0, -0.4), 'snow', subdiv=2, amp=0.12, scale=(1.6, 1.0, 0.4), seed=516)
    return finalize('snowy_rock_2', smooth_angle=12)


def snowy_bush():
    """E17 - low evergreen bush with snow on top."""
    ob = _bush(517, 5.0, 'snowy_bush', keys=('pine', 'pine_dark', 'leaf_dark'))
    top_paint(ob, 'snow', 0.55, 7, noise_amt=0.3)
    return ob


def edelweiss():
    """E18 - clump of white alpine flowers (edelweiss): star petals on fuzzy grey-green leaves."""
    reset()
    rnd = random.Random(18)
    for i in range(10):
        a = rnd.uniform(0, 6.28)
        tube(nm('lf'), [(0, 0, 0.05), (math.cos(a) * 0.55, math.sin(a) * 0.55, 0.18)], 0.06, 'birch_leaf', res=4, taper=[1, 0.4])
    for i in range(6):
        x, y = rnd.uniform(-0.6, 0.6), rnd.uniform(-0.6, 0.6)
        h = rnd.uniform(0.8, 1.3)
        tube(nm('st'), [(x * 0.3, y * 0.3, 0), (x, y, h)], 0.04, 'leaf_light', res=4)
        for k in range(7):
            a = 2 * math.pi * k / 7 + rnd.uniform(0, 0.3)
            lathe(nm('pt'), [(0, 0), (0.07, 0), (0, 0.35)], loc=(x, y, h), key='fl_white', segs=4, rot=(90 - 10, 0, math.degrees(a) - 90))
        ball(nm('ce'), 0.08, loc=(x, y, h + 0.04), key='fl_yellow', segs=6, rings=4)
    return finalize('edelweiss', smooth_angle=40)


def gentian():
    """E19 - clump of blue alpine flowers (gentian): upright deep-blue trumpets on short stems."""
    reset()
    rnd = random.Random(19)
    for i in range(12):
        a = rnd.uniform(0, 6.28)
        tube(nm('lf'), [(0, 0, 0.05), (math.cos(a) * 0.6, math.sin(a) * 0.6, 0.25)], 0.1, 'leaf', res=4, taper=[1, 0.3])
    for i in range(7):
        x, y = rnd.uniform(-0.6, 0.6), rnd.uniform(-0.6, 0.6)
        h = rnd.uniform(0.4, 0.8)
        tube(nm('st'), [(x * 0.2, y * 0.2, 0), (x, y, h)], 0.04, 'leaf', res=4)
        lathe(nm('tp'), [(0, 0), (0.05, 0), (0.1, 0.25), (0.17, 0.4), (0.15, 0.43), (0, 0.28)], loc=(x, y, h), key='fl_blue', segs=8)
    return finalize('gentian', smooth_angle=40)


def terrace_wall():
    """E20 - stacked dry-stone terrace wall, 20 long x 5 tall, with a grassy snowy top."""
    reset()
    rnd = random.Random(20)
    L, H, T = 20.0, 5.0, 2.0
    z = 0.0
    k = 0
    while z < H:
        hh = rnd.uniform(0.6, 0.9)
        x = -L / 2 + (0.5 if k % 2 else 0)
        while x < L / 2:
            wv = rnd.uniform(1.0, 2.0)
            wv = min(wv, L / 2 - x)
            if wv > 0.3:
                box(nm('st'), (wv - 0.08, T - (z / H) * 0.6, hh - 0.06), loc=(x + wv / 2, (z / H) * 0.3, z + hh / 2), key=rnd.choice(['stone', 'stone_dark', 'stone_light', 'cliff_a']),
                    rot=(rnd.uniform(-3, 3), rnd.uniform(-3, 3), rnd.uniform(-2, 2)), bev=0.08)
            x += wv
        z += hh
        k += 1
    box(nm('top'), (L, 3.0, 0.4), loc=(0, 1.0, z + 0.1), key='grass_dry')
    for i in range(10):
        blob(nm('sn'), rnd.uniform(0.6, 1.0), (rnd.uniform(-L / 2, L / 2), rnd.uniform(0.0, 2.0), z + 0.3), 'snow', subdiv=2, amp=0.1, scale=(1.8, 1.0, 0.35), seed=i)
    return finalize('terrace_wall', smooth_angle=15)


def log_fence():
    """E21 - zig-zag split-log fence (snake fence), 20 long, snow on the top rails."""
    reset()
    rnd = random.Random(21)
    n = 5
    pts = [(-10 + 20 * i / n, (1.2 if i % 2 else -1.2)) for i in range(n + 1)]
    for i, (x, y) in enumerate(pts):
        for s in (-1, 1):
            cyl(nm('ps'), 0.22, 4.4, loc=(x + s * 0.35, y, 0), key='bark', verts=6, rot=(s * 8, 0, 0))
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for k in range(5):
            z = 0.5 + k * 0.75
            beam3((x0, y0, z), (x1, y1, z + 0.3), 0.42, 0.32, rnd.choice(['bark', 'wood']))
        beam3((x0, y0, 0.5 + 4 * 0.75 + 0.4), (x1, y1, 0.5 + 4 * 0.75 + 0.7), 0.5, 0.2, 'snow')
    return finalize('log_fence', smooth_angle=25)


def sled():
    """E22 - wooden sled with curled iron-shod runners and a rope pull."""
    reset()
    L = 6.0
    for s in (-1, 1):
        y = s * 1.1
        tube(nm('run'), [(L / 2, y, 0.15), (-L / 2 + 0.6, y, 0.15), (-L / 2 - 0.2, y, 0.6), (-L / 2 - 0.2, y, 1.4), (-L / 2 + 0.3, y, 1.5)], 0.12, 'iron', res=4)
        for x in (-1.8, 0.0, 1.8):
            lbeam(F(), (x, y, 0.2), (x, y, 1.1), 0.2, 'wood_dark')
        lbox(F(), (L - 0.4, 0.2, 0.3), 0.1, y, 1.2, 'wood')
    for i in range(7):
        box(nm('sl'), (0.6, 2.6, 0.12), loc=(-L / 2 + 0.8 + i * 0.75, 0, 1.4), key='wood_light')
    tube(nm('rope'), [(-L / 2 - 0.2, -1.1, 1.3), (-L / 2 - 1.6, 0, 0.8), (-L / 2 - 2.6, 0, 0.1)], 0.06, 'rope', res=4)
    tube(nm('rope2'), [(-L / 2 - 0.2, 1.1, 1.3), (-L / 2 - 1.6, 0, 0.8)], 0.06, 'rope', res=4)
    return finalize('sled', smooth_angle=30)


def cheese_cart():
    """E23 - dairy cart: two-wheeled hand cart loaded with cheese wheels, milk churns and a striped cloth."""
    reset()
    from props import wheel
    rnd = random.Random(23)
    box(nm('bed'), (6.0, 3.2, 0.3), loc=(0, 0, 2.4), key='wood')
    for s in (-1, 1):
        box(nm('sd'), (6.0, 0.2, 0.8), loc=(0, s * 1.5, 2.9), key='wood_dark')
        wheel(nm('wh'), 1.3, (0.6, s * 1.9, 1.3), axis='Y', spokes=8)
        tube(nm('hd'), [(-3.0, s * 1.2, 2.4), (-5.6, s * 1.2, 2.0), (-6.6, s * 1.1, 2.1)], 0.12, 'wood_dark', res=4)
    box(nm('lg'), (0.3, 3.0, 2.4), loc=(-2.6, 0, 1.2), key='wood_dark')
    box(nm('cl'), (5.6, 3.0, 0.06), loc=(0, 0, 2.58), key='fabric_red')
    for i in range(3):
        for j in range(2):
            cyl(nm('ch'), 0.9, 0.6, loc=(-1.8 + i * 1.6, -0.7 + j * 1.4, 2.6), key='fl_yellow', verts=16, bev=0.1)
    cyl(nm('ch2'), 0.9, 0.6, loc=(-1.0, 0.0, 3.2), key='fl_yellow', verts=16, bev=0.1)
    box(nm('cw'), (0.8, 0.8, 0.6), loc=(0.2, 0.2, 3.5), key='fl_yellow', rot=(0, 0, 30))
    for k, x in enumerate((2.1, 2.1)):
        y = -0.7 + k * 1.4
        lathe(nm('mc'), [(0, 0), (0.55, 0), (0.6, 1.4), (0.35, 1.8), (0.3, 2.1), (0.4, 2.2), (0, 2.25)], loc=(x, y, 2.55), key='steel', segs=12)
        torus(nm('mch'), 0.3, 0.05, loc=(x, y, 4.8), key='steel', segs=10, rsegs=3, rot=(90, 0, 0))
    return finalize('cheese_cart', smooth_angle=30)


def beehive():
    """E24 - beehives: two straw skeps and a wooden box hive on a small roofed stand."""
    reset()
    box(nm('st'), (8.0, 3.0, 0.3), loc=(0, 0, 2.2), key='wood')
    for x in (-3.6, 3.6):
        for s in (-1, 1):
            box(nm('lg'), (0.3, 0.3, 6.6), loc=(x, s * 1.2, 3.3), key='wood_dark')
    a = math.degrees(math.atan2(1.0, 3.6))
    box(nm('rf'), (8.8, 4.4, 0.25), loc=(0, 0.2, 6.9), key='roof_old', rot=(a, 0, 0))
    box(nm('rfs'), (8.6, 4.2, 0.4), loc=(0, 0.2, 7.2), key='snow', rot=(a, 0, 0), bev=0.15)
    for x in (-2.4, 0.0):
        prof = [(0, 0), (1.0, 0)] + [(1.0 * math.cos(math.radians(t)), 1.9 * math.sin(math.radians(t))) for t in range(10, 91, 10)]
        lathe(nm('sk'), [(r, z + 2.35) for r, z in prof], loc=(x, 0, 0), key='thatch', segs=16)
        for k in range(5):
            zz = 2.5 + k * 0.35
            rr = 1.0 * math.cos(math.asin(min(0.99, (zz - 2.35) / 1.9)))
            torus(nm('skr'), rr + 0.02, 0.06, loc=(x, 0, zz), key='wicker', segs=16, rsegs=3)
        box(nm('en'), (0.5, 0.2, 0.25), loc=(x, -0.95, 2.5), key='hole')
    box(nm('bh'), (1.8, 1.8, 2.2), loc=(2.6, 0, 3.45), key='wood_paint', bev=0.04)
    box(nm('bhl'), (2.2, 2.2, 0.3), loc=(2.6, 0, 4.7), key='wood_light', bev=0.04)
    box(nm('bhe'), (1.0, 0.1, 0.2), loc=(2.6, -0.95, 2.6), key='hole')
    for zz in (3.0, 3.8):
        box(nm('bhb'), (1.85, 1.85, 0.06), loc=(2.6, 0, zz), key='wood')
    return finalize('beehive', smooth_angle=35)


def snow_drift():
    """E25 - soft snow drift piece, 16 x 8, to blend buildings and rocks into the snowy ground."""
    reset()
    rnd = random.Random(25)
    blob(nm('d'), 5.0, (0, 0, -2.6), 'snow', subdiv=4, amp=0.08, freq=0.8, scale=(1.6, 0.8, 0.7), seed=25, flat_bottom=0.0)
    for i in range(5):
        blob(nm('dd'), rnd.uniform(1.6, 2.6), (rnd.uniform(-6, 6), rnd.uniform(-2.5, 2.5), -0.6), 'snow', subdiv=3, amp=0.08, scale=(1.4, 1.0, 0.5), seed=i)
    return finalize('snow_drift', smooth_angle=50)


def icicle_cluster():
    """E26 - icicle cluster: a snow-capped ledge strip with hanging icicles, 8 wide (hang under eaves or rock overhangs)."""
    reset()
    rnd = random.Random(26)
    box(nm('ice'), (8.0, 1.2, 0.5), loc=(0, 0, 3.4), key='snow', bev=0.2)
    for i in range(16):
        x = -3.7 + i * 0.5 + rnd.uniform(-0.1, 0.1)
        h = rnd.uniform(0.8, 3.0) * (1.0 - abs(x) / 8.0)
        r = rnd.uniform(0.1, 0.22)
        lathe(nm('ic'), [(0, 0), (r, 0), (r * 0.6, -h * 0.4), (0, -h)], loc=(x, rnd.uniform(-0.3, 0.3), 3.2), key='glass', segs=6)
    return finalize('icicle_cluster', smooth_angle=40)


ITEMS_A = [
    ('E01_chalet_1', chalet_1), ('E02_chalet_2', chalet_2), ('E03_chalet_3', chalet_3), ('E04_chalet_4', chalet_4),
    ('E05_lodge', lodge), ('E06_stone_chapel', stone_chapel), ('E07_sawmill', sawmill), ('E08_barn', barn),
    ('E09_goat_pen', goat_pen), ('E10_watchtower', watchtower), ('E11_covered_bridge', covered_bridge),
]
ITEMS_B = [
    ('E12_snowy_pine_1', snowy_pine_1), ('E13_snowy_pine_2', snowy_pine_2), ('E14_snowy_pine_3', snowy_pine_3),
    ('E15_snowy_rock_1', snowy_rock_1), ('E16_snowy_rock_2', snowy_rock_2), ('E17_snowy_bush', snowy_bush),
    ('E18_edelweiss', edelweiss), ('E19_gentian', gentian), ('E20_terrace_wall', terrace_wall), ('E21_log_fence', log_fence),
    ('E22_sled', sled), ('E23_cheese_cart', cheese_cart), ('E24_beehive', beehive), ('E25_snow_drift', snow_drift),
]
