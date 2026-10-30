"""C. Royal capital models. 1 unit = 1 stud. Fronts face -Y."""
import math, random
from mathutils import Vector
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, top_paint
from arch import (F, faces, lbox, lbeam, beam3, slab, lslab, half_disc, window, door, arrow_slit, quoins, band, corbels,
                  battlements, ring_battlements, timber_frame, gable_roof, roof_z, cone_roof, chimney, dormer, railing,
                  flower_box, wall_lantern, arc_pts, nm)


# ============================================================ townhouses
def hanging_sign(f, x, z, board='shutter_b', emblem='gold'):
    lbeam(f, (x, -0.1, z), (x, -2.6, z), 0.16, 'iron')
    tube(nm('sgc'), [f.p(x, -0.1, z - 1.0), f.p(x, -1.2, z - 0.5), f.p(x, -2.2, z)], 0.06, 'iron', res=4)
    lbox(f, (0.5, 0.2, 0.9), x, -0.1, z - 0.2, 'iron')
    for yy in (-1.0, -2.2):
        lbox(f, (0.06, 0.06, 0.5), x, yy, z - 0.3, 'iron')
    lbox(f, (0.16, 1.7, 1.25), x, -1.6, z - 1.2, board, bev=0.04)
    lbox(f, (0.2, 1.85, 0.12), x, -1.6, z - 0.55, 'wood_dark')
    lbox(f, (0.2, 1.85, 0.12), x, -1.6, z - 1.85, 'wood_dark')
    ball(nm('em'), 0.32, loc=f.p(x, -1.6, z - 1.2), key=emblem, segs=8, rings=6, scale=(1.4, 1, 1))


def house(cx=0.0, w=18.0, d=16.0, floors=3, gh=8.0, fh=7.0, ground='ashlar', ground_trim='ashlar_dark', upper='plaster',
          timber=True, jetty=0.7, roof='side', rkeys=('tile_a', 'tile_b'), shutter='shutter_g', flowers=('fl_red', 'fl_white'),
          shop=False, dormers=2, balcony=False, seed=0, door_bay=None, sign=None, side_windows=(True, True), chim=True,
          frame_key='wood_paint', pitch=0.42, lit=(), upper_quoins=False):
    rnd = random.Random(seed)
    nb = max(2, round(w / 6.2))
    xs = [-w / 2 + w * (i + 0.5) / nb for i in range(nb)]
    db = door_bay if door_bay is not None else (nb // 2 if not shop else 0)
    # ---- ground storey
    box(nm('g'), (w, d, gh), loc=(cx, 0, gh / 2), key=ground)
    box(nm('pl'), (w + 0.3, d + 0.3, 0.9), loc=(cx, 0, 0.45), key='stone_dark', bev=0.05)
    band(cx, 0, w, d, gh - 0.1, 0.5, ground_trim, out=0.2)
    for fr in (F(cx - w / 2, -d / 2, 0, 0), F(cx + w / 2, -d / 2, 0, 90), F(cx + w / 2, d / 2, 0, 180), F(cx - w / 2, d / 2, 0, -90)):
        quoins(fr, 0.9, gh - 0.2, ground_trim, course=1.05)
    fc = faces(cx, 0, w, d)
    for i, x in enumerate(xs):
        if i == db:
            door(fc['front'], x, w=3.4, h=6.6, arch=True, surround=ground_trim, lamp=True)
        elif shop:
            sw = w / nb - 1.6
            window(fc['front'], x, 1.4, w=sw, h=4.6, arch=False, frame=frame_key, sill=ground_trim, lintel=ground_trim, lit=True)
            for k in range(1, 4):
                lbox(fc['front'], (0.1, 0.22, 4.6), x - sw / 2 + sw * k / 4, -0.14, 1.4 + 2.3, frame_key)
            lbox(fc['front'], (sw + 1.0, 1.6, 0.18), x, -0.9, 6.8, rnd.choice(['fabric_red', 'fabric_blue', 'fabric_green']), rot=(-18, 0, 0))
        else:
            window(fc['front'], x, 1.8, w=2.4, h=4.4, arch=True, frame=frame_key, sill=ground_trim, keystone=ground_trim,
                   flowers=flowers if rnd.random() < 0.6 else None)
        if i != db:
            window(fc['back'], -x, 1.8, w=2.2, h=4.0, arch=True, frame=frame_key, sill=ground_trim, keystone=ground_trim)
    if not shop or True:
        door(fc['back'], -xs[-1], w=3.0, h=6.0, arch=False, surround=ground_trim, step='stone_dark')
    if sign:
        hanging_sign(fc['front'], xs[db] + (2.6 if db < nb - 1 else -2.6), gh - 1.0, board=sign)
    # ---- upper storeys
    z = gh
    for k in range(floors - 1):
        jj = jetty * (k + 1)
        dk = d + 2 * jj
        box(nm('u'), (w, dk, fh), loc=(cx, 0, z + fh / 2), key=upper)
        if jetty:
            for s in (-1, 1):
                for i in range(int(w / 1.5) + 1):
                    xx = cx - w / 2 + 0.3 + (w - 0.6) * i / int(w / 1.5)
                    box(nm('jo'), (0.4, 0.8, 0.45), loc=(xx, s * (dk / 2 - 0.3), z + 0.05), key='timber')
        fk = faces(cx, 0, w, dk, z)
        posts = [-w / 2 + 0.21] + [-w / 2 + w * i / nb for i in range(1, nb)] + [w / 2 - 0.21]
        for side in ('front', 'back'):
            fr = fk[side]
            if timber:
                timber_frame(fr, w, 0, fh, posts, braces=not shutter)
                lbox(fr, (w, 0.36, 0.36), 0, -0.18, 1.2, 'timber')
            elif upper_quoins:
                pass
            for i, x in enumerate(xs):
                xx = x if side == 'front' else -x
                is_lit = (k, i) in lit and side == 'front'
                if balcony and side == 'front' and k == 0 and i == nb // 2:
                    door(fr, xx, w=2.6, h=5.2, arch=False, key='glass_dark', surround=frame_key, step=None, studs=False)
                    lbox(fr, (6.0, 2.4, 0.4), xx, -1.2, 0.0, ground_trim, bev=0.05)
                    for s in (-1, 1):
                        lbeam(fr, (xx + s * 2.4, -0.1, -1.6), (xx + s * 2.4, -2.1, -0.15), 0.35, ground_trim)
                    railing(fr.sub(0, 0, 0), xx - 2.9, xx + 2.9, 0.2, y=-2.3, h=1.8, key='iron')
                    for s in (-1, 1):
                        lbox(fr, (0.1, 2.3, 0.12), xx + s * 2.9, -1.2, 2.0, 'iron')
                    continue
                window(fr, xx, 1.6, w=2.2, h=3.7, frame=frame_key, shutter=shutter, sill=frame_key if timber else ground_trim,
                       flowers=flowers if (side == 'front' and rnd.random() < 0.55) else None, lit=is_lit,
                       lintel=None if timber else ground_trim)
        for side, on in zip(('left', 'right'), side_windows):
            fr = fk[side]
            if timber:
                timber_frame(fr, dk, 0, fh, [-dk / 2 + 0.21, 0, dk / 2 - 0.21], braces=True)
            if on:
                for x in ((-dk / 4, dk / 4) if dk > 13 else (0,)):
                    window(fr, x + (1.6 if timber and len((-dk / 4, dk / 4)) == 1 else 0), 1.6, w=2.0, h=3.4, frame=frame_key,
                           sill=frame_key if timber else ground_trim, lintel=None if timber else ground_trim)
        if not timber:
            band(cx, 0, w, dk, z - 0.05, 0.35, ground_trim, out=0.12)
        z += fh
    top = z
    dd = d + 2 * jetty * (floors - 1)
    box(nm('eave'), (w + 0.3, dd + 0.3, 0.5), loc=(cx, 0, top - 0.25), key='timber' if timber else ground_trim)
    # ---- roof
    if roof == 'side':
        hr = dd * pitch
        gable_roof(F(cx, 0, 0, 0), w, dd, top, hr, keys=rkeys, wall=upper, ov=1.1, ovg=0.8)
        for g in (-1, 1):
            fr = F(cx + g * w / 2, 0, top, g * 90)
            window(fr, 0, 1.0, w=1.6, h=2.4, arch=True, frame=frame_key, sill=frame_key)
        if dormers:
            yf = -dd / 2 + 2.2
            zb = roof_z(top, hr, dd, yf) - 0.3
            slope = hr / (dd / 2)
            for i in range(dormers):
                dx = cx - w / 2 + w * (i + 0.5) / dormers
                dormer(F(0, 0, 0, 0), dx, yf, zb, w=3.4, h=3.6, depth=3.6 / slope + 1.2, wall=upper, keys=rkeys, frame=frame_key)
        if chim:
            chimney(cx + w / 2 - 2.6, dd * 0.18, top, top + hr + 2.8)
    else:
        hr = w * pitch * 1.15
        gable_roof(F(cx, 0, 0, 90), dd, w, top, hr, keys=rkeys, wall=upper, ov=1.0, ovg=1.0, crest='iron')
        for side in ('front', 'back'):
            fr = faces(cx, 0, w, dd, top)[side]
            if timber:
                lbeam(fr, (0, -0.2, 0.3), (0, -0.2, hr - 0.4), 0.42, 'timber')
                for s in (-1, 1):
                    lbeam(fr, (s * w * 0.42, -0.2, 0.3), (s * w * 0.12, -0.2, hr * 0.7), 0.36, 'timber')
            window(fr, 0 if not timber else -1.9, 1.4, w=2.0, h=3.2, arch=True, frame=frame_key, sill=frame_key)
            if timber:
                window(fr, 1.9, 1.4, w=2.0, h=3.2, arch=True, frame=frame_key, sill=frame_key)
            window(fr, 0, hr * 0.62, w=1.1, h=1.5, arch=True, frame=frame_key, sill=None, panes=False)
        if chim:
            chimney(cx + w * 0.3, dd * 0.2, top, top + hr * 0.7 + 3.0)
    return top


def _townhouse(**kw):
    reset()
    name = kw.pop('name', 'townhouse')
    house(**kw)
    return finalize(name, smooth_angle=30)


def townhouse_1():
    """C5 - three-storey timber-framed house, blue slate roof, two dormers."""
    return _townhouse(name='townhouse_1', w=18, d=16, floors=3, upper='plaster', rkeys=('tile_a', 'tile_b'),
                      shutter='shutter_g', flowers=('fl_red', 'fl_white'), dormers=2, seed=5, lit={(0, 0), (1, 2)})


def townhouse_2():
    """C6 - tall narrow stone house, street-facing gable, balcony."""
    return _townhouse(name='townhouse_2', w=14, d=15, floors=4, ground='ashlar_dark', ground_trim='castle_trim', upper='plaster_b',
                      timber=False, jetty=0.0, roof='front', rkeys=('tile_red_a', 'tile_red_b'), shutter='shutter_b',
                      flowers=('fl_pink', 'fl_white', 'fl_yellow'), balcony=True, seed=6, frame_key='wood_paint', lit={(1, 0)})


def townhouse_3():
    """C7 - wide merchant house with shop front and three dormers."""
    return _townhouse(name='townhouse_3', w=21, d=15, floors=3, upper='plaster_c', rkeys=('tile_grey', 'tile_b'), shutter='shutter_r',
                      flowers=('fl_yellow', 'fl_orange'), shop=True, dormers=3, seed=7, sign='shutter_r', lit={(0, 1), (0, 2)})


def townhouse_4():
    """C8 - brick house with stone trims, front gable, balcony."""
    return _townhouse(name='townhouse_4', w=16, d=16, floors=3, ground='ashlar', ground_trim='castle_trim', upper='brick',
                      timber=False, jetty=0.0, roof='front', rkeys=('tile_a', 'tile_b'), shutter='shutter_g',
                      flowers=('fl_purple', 'fl_white'), balcony=True, seed=8, frame_key='wood_paint', gh=8.5)


def corner_house():
    """C9 - corner townhouse with a round turret on the street corner."""
    reset()
    w, d = 20.0, 20.0
    top = house(w=w, d=d, floors=3, upper='plaster_d', rkeys=('tile_red_a', 'tile_red_b'), shutter='shutter_b',
                flowers=('fl_red', 'fl_pink'), shop=True, dormers=2, seed=9, sign='shutter_g', jetty=0.0,
                side_windows=(True, True), lit={(0, 1)})
    cx, cy, r = -w / 2 - 0.6, -d / 2 - 0.6, 3.4
    lathe(nm('tc'), [(0.0, 5.0), (1.2, 5.0), (r - 0.2, 7.4), (r, 7.9), (r, top + 4.0), (0.0, top + 4.0)], loc=(cx, cy, 0), key='plaster_d', segs=20)
    for zz in (7.9, 8.0 + 7.0, top + 3.8):
        lathe(nm('tb'), [(0.0, zz - 0.2), (r + 0.25, zz - 0.2), (r + 0.25, zz + 0.25), (0.0, zz + 0.25)], loc=(cx, cy, 0), key='ashlar_dark', segs=20)
    for i in range(3):
        a = -135 + (i - 1) * 55
        fr = F(cx + math.cos(math.radians(a)) * r, cy + math.sin(math.radians(a)) * r, 0, a + 90)
        for zz in (9.4, 16.4):
            window(fr, 0, zz, w=1.5, h=3.2, arch=True, frame='wood_paint', sill='ashlar_dark', panes=False, lit=(i == 1 and zz > 10))
    cone_roof(cx, cy, top + 4.0, r, 8.5, keys=('tile_red_a', 'tile_red_b'), rings=6, ov=0.6, flag='fabric_red')
    return finalize('corner_house', smooth_angle=30)


def terrace_row():
    """C10 - row of four narrow terraced houses with varied heights, colours and roofs."""
    reset()
    specs = [
        dict(w=11, floors=3, upper='plaster', rkeys=('tile_a', 'tile_b'), shutter='shutter_g', roof='front', timber=True),
        dict(w=10, floors=4, upper='plaster_b', rkeys=('tile_red_a', 'tile_red_b'), shutter='shutter_b', roof='front', timber=False, jetty=0.0),
        dict(w=12, floors=3, upper='plaster_c', rkeys=('tile_grey', 'tile_b'), shutter='shutter_r', roof='front', timber=True),
        dict(w=10, floors=3, upper='plaster_d', rkeys=('tile_red_b', 'tile_red_a'), shutter='shutter_g', roof='front', timber=False, jetty=0.0, gh=9.0),
    ]
    total = sum(s['w'] for s in specs)
    x = -total / 2
    for i, s in enumerate(specs):
        w = s['w']
        kw = dict(d=14, dormers=0, seed=20 + i, side_windows=(False, False), flowers=('fl_red', 'fl_white', 'fl_pink'), pitch=0.5)
        kw.update(s)
        house(cx=x + w / 2, **kw)
        x += w
    return finalize('terrace_row', smooth_angle=30)


ITEMS_HOUSES = [
    ('C05_townhouse_1', townhouse_1), ('C06_townhouse_2', townhouse_2), ('C07_townhouse_3', townhouse_3),
    ('C08_townhouse_4', townhouse_4), ('C09_corner_house', corner_house), ('C10_terrace_row', terrace_row),
]



# ============================================================ city walls and gates
WT, WH = 9.0, 28.0   # wall thickness and walk height


def stone_face(f, x0, x1, z0, z1, n, seed, keys=('ashlar', 'ashlar_dark', 'castle'), out=0.14):
    """Scatter slightly proud ashlar blocks on a wall face so it reads as stone."""
    rnd = random.Random(seed)
    for i in range(n):
        bw, bh = rnd.choice([(2.4, 1.1), (1.8, 1.1), (3.0, 1.1), (1.4, 1.1)])
        z = z0 + 0.6 + round(rnd.uniform(0, (z1 - z0 - 1.2) / 1.1)) * 1.1
        x = rnd.uniform(x0 + bw / 2, x1 - bw / 2)
        lbox(f, (bw, out * 2, bh - 0.1), x, 0, z, rnd.choice(keys), bev=0.04)


def wall_run(f, x0, x1, seed=0, slits=True, butt=True, key='ashlar', dark='ashlar_dark', trim='castle_trim', faces_=('ashlar', 'ashlar_dark', 'castle')):
    """City wall section in frame f (centre line), outer face toward local -y."""
    L = x1 - x0
    xc = (x0 + x1) / 2
    lbox(f, (L, WT, WH), xc, 0, WH / 2, key)
    o = lslab(f, [(x0, -WT / 2 - 2.6, 0), (x0, -WT / 2, 0), (x0, -WT / 2, 7.0)], (L, 0, 0), dark)
    top_paint(o, 'moss', 0.5, seed)
    lbox(f, (L, 0.6, 0.6), xc, -WT / 2 - 0.2, 7.2, trim)
    lbox(f, (L, 0.5, 0.5), xc, -WT / 2 - 0.2, 20.0, trim)
    fo = f.sub(0, -WT / 2)
    fi = f.sub(0, WT / 2, 0, 180)
    stone_face(fo, x0, x1, 7.5, WH - 1, int(L * 1.6), seed, keys=faces_)
    stone_face(fi, -x1, -x0, 0.5, WH - 1, int(L * 1.0), seed + 1, keys=faces_)
    lbox(f, (L, WT - 1.6, 0.3), xc, 0.2, WH + 0.1, 'stone_dark')
    corbels(fo, x0 + 0.6, x1 - 0.6, WH - 2.2, dark, step=1.8, size=(0.7, 1.0, 1.4))
    battlements(fo, x0, x1, WH - 0.4, key, t=1.3, y=-0.9, mw=1.8, gap=1.1, cap=trim)
    lbox(f, (L, 0.9, 1.3), xc, WT / 2 - 0.45, WH + 0.6, key)
    lbox(f, (L, 1.1, 0.25), xc, WT / 2 - 0.45, WH + 1.35, trim)
    if slits:
        n = max(1, int(L / 8))
        for i in range(n):
            arrow_slit(fo, x0 + L * (i + 0.5) / n, 14.0, key=dark)
    if butt and L > 18:
        for bx in (x0 + L * 0.25, x0 + L * 0.75):
            lbox(f, (3.0, 2.4, 18.0), bx, -WT / 2 - 1.2, 9.0, key, bev=0.08)
            lslab(f, [(bx - 1.5, -WT / 2 - 2.4, 18.0), (bx - 1.5, -WT / 2, 18.0), (bx - 1.5, -WT / 2, 21.0)], (3.0, 0, 0), dark)
    # inner face: torch brackets and a few drain holes
    for i in range(max(1, int(L / 14))):
        wall_lantern(fi, -x1 + L * (i + 0.5) / max(1, int(L / 14)), 10.0, s=1.4)


def city_wall_straight():
    """C1 - outer city wall, 40 long, walkway at 28."""
    reset()
    wall_run(F(0, 0, 0, 0), -20, 20, seed=1)
    return finalize('city_wall_straight', smooth_angle=20)


def city_wall_corner():
    """C2 - outer city wall corner (two 24-stud arms)."""
    reset()
    wall_run(F(0, 0, 0, 0), -WT / 2, 24, seed=2)
    wall_run(F(0, 0, 0, -90), -24, WT / 2, seed=3)
    lbox(F(), (WT, WT, 0.3), 0, 0, WH + 0.1, 'stone_dark')
    return finalize('city_wall_corner', smooth_angle=20)


def round_tower(cx, cy, r, h, roof=('tile_a', 'tile_b'), flag='fabric_red', seed=0, doors=(0, 180), slit_rows=(10, 18, 26),
                key='ashlar', dark='ashlar_dark', trim='castle_trim', roof_h=None, gallery=False):
    lathe(nm('tw'), [(0.0, 0.0), (r + 2.2, 0.0), (r + 0.6, 6.0), (r, 7.0), (r, h), (0.0, h)], loc=(cx, cy, 0), key=key, segs=28)
    for zz, k in ((7.0, trim), (h * 0.62, trim)):
        lathe(nm('tb'), [(0.0, zz - 0.3), (r + 0.3, zz - 0.3), (r + 0.3, zz + 0.3), (0.0, zz + 0.3)], loc=(cx, cy, 0), key=k, segs=28)
    rnd = random.Random(seed)
    for i in range(int(r * 5)):
        a = rnd.uniform(0, 360)
        zz = 8 + round(rnd.uniform(0, (h - 10) / 1.1)) * 1.1
        ar = math.radians(a)
        box(nm('sb'), (0.3, rnd.choice([1.6, 2.2, 2.8]), 1.0), loc=(cx + math.cos(ar) * r, cy + math.sin(ar) * r, zz), key=rnd.choice([dark, trim]),
            rot=(0, 0, a), bev=0.04)
    for zz in slit_rows:
        for k in range(4):
            a = 45 + 90 * k + (zz % 3) * 15
            ar = math.radians(a)
            arrow_slit(F(cx + math.cos(ar) * r, cy + math.sin(ar) * r, 0, a + 90), 0, zz, key=dark)
    for k in range(3):
        a = -90 + (k - 1) * 70
        ar = math.radians(a)
        window(F(cx + math.cos(ar) * r, cy + math.sin(ar) * r, 0, a + 90), 0, h - 8.0, w=1.8, h=3.6, arch=True, frame=dark,
               sill=trim, panes=False, lit=(k == 1))
    ring_battlements(cx, cy, h, r + 1.0, key, t=1.2, cap=trim)
    lathe(nm('tf'), [(0.0, h - 0.6), (r + 1.0, h - 0.6), (r + 1.0, h), (0.0, h)], loc=(cx, cy, 0), key=dark, segs=28)
    lathe(nm('rr'), [(0.0, h + 2.0), (r - 1.0, h + 2.0), (r - 1.0, h + 4.5), (0.0, h + 4.5)], loc=(cx, cy, 0), key=key, segs=24)
    top = cone_roof(cx, cy, h + 4.5, r - 1.0, roof_h or (r - 1.0) * 2.0, keys=roof, rings=8, ov=1.0, flag=flag)
    for a in doors:
        ar = math.radians(a)
        door(F(cx + math.cos(ar) * r, cy + math.sin(ar) * r, WH, a + 90), 0, w=3.2, h=6.0, arch=True, surround='castle_trim', step=None)
    return top


def city_wall_tower():
    """C3 - round wall tower; wall sections join at +-X, doors at walk level."""
    reset()
    round_tower(0, 0, 9.0, 42.0, doors=(0, 180), seed=3)
    return finalize('city_wall_tower', smooth_angle=20)


def arch_block(f, x0, x1, y0, y1, z0, z1, ax, spring, r, key):
    """Solid block from x0..x1 (local) with a round-arched passage of radius r centred at ax, springing at z=spring."""
    pts = [(ax - r, y0, z0)]
    for i in range(17):
        a = math.pi - math.pi * i / 16
        pts.append((ax + math.cos(a) * r, y0, spring + math.sin(a) * r))
    pts += [(ax + r, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1), (x0, y0, z0)]
    return lslab(f, pts, (0, y1 - y0, 0), key)


def grand_gate():
    """C4 - grand city gate: twin towers, deep arched passage, portcullis, crest and banners."""
    reset()
    f = F()
    gw, gd, gh = 22.0, 16.0, 36.0
    arch_block(f, -gw / 2, gw / 2, -gd / 2, gd / 2, 0, gh, 0, 12.0, 5.5, 'ashlar')
    for s in (-1, 1):
        fr = f.sub(0, s * gd / 2, 0, 0 if s < 0 else 180)
        tube(nm('va'), arc_pts(fr, 0, 12.0, 6.1, y=-0.3, n=21), 0.7, 'castle_trim', res=4)
        lbox(fr, (1.4, 0.9, 2.0), 0, -0.4, 18.4, 'castle_trim', bev=0.06)
        for xx in (-5.9, 5.9):
            lbox(fr, (1.2, 0.8, 12.0), xx, -0.3, 6.0, 'castle_trim', bev=0.05)
        stone_face(fr, -gw / 2, gw / 2, 19.5, gh - 2, 50, 40 + s)
        lbox(fr, (gw, 0.6, 0.5), 0, -0.2, 20.0, 'castle_trim')
        corbels(fr, -gw / 2 + 0.6, gw / 2 - 0.6, gh - 2.2, 'ashlar_dark', step=1.8, size=(0.7, 1.0, 1.4))
        battlements(fr, -gw / 2, gw / 2, gh - 0.4, 'ashlar', t=1.3, y=-0.9, cap='castle_trim')
        for xx in (-7.5, 7.5):
            window(fr, xx, 24.0, w=2.2, h=4.4, arch=True, frame='ashlar_dark', sill='castle_trim', panes=True, lit=(s < 0))
    # royal crest over the outer arch
    fo = f.sub(0, -gd / 2)
    lbox(fo, (6.4, 0.5, 7.4), 0, -0.25, 27.5, 'castle_trim', bev=0.1)
    shield = [(-2.4, 0, 3.2), (2.4, 0, 3.2), (2.4, 0, 0.6), (0, 0, -2.4), (-2.4, 0, 0.6)]
    lslab(fo.sub(0, -0.5, 27.0), shield, (0, -0.35, 0), 'fabric_red')
    lslab(fo.sub(0, -0.85, 27.0), [(-0.5, 0, 2.6), (0.5, 0, 2.6), (0.5, 0, -1.4), (-0.5, 0, -1.4)], (0, -0.12, 0), 'gold')
    lslab(fo.sub(0, -0.85, 27.0), [(-1.8, 0, 1.4), (1.8, 0, 1.4), (1.8, 0, 0.6), (-1.8, 0, 0.6)], (0, -0.12, 0), 'gold')
    for i, xx in enumerate((-1.8, 0, 1.8)):
        lathe(nm('cw'), [(0, 0), (0.45, 0), (0.12, 1.0 + (0.3 if i == 1 else 0)), (0, 1.1 + (0.3 if i == 1 else 0))],
              loc=fo.p(xx, -0.5, 31.4), key='gold', segs=6)
    # portcullis (half raised) and open timber doors
    for k in range(9):
        xx = -4.8 + k * 1.2
        lbox(fo, (0.22, 0.22, 7.0), xx, 1.2, 13.8, 'iron_dark')
        lathe(nm('sp'), [(0, 0), (0.16, 0), (0, 0.6)], loc=fo.p(xx, 1.2, 9.7), key='iron_dark', segs=4, rot=(180, 0, 0))
    for zz in (11.0, 13.0, 15.0, 17.0):
        lbox(fo, (11.0, 0.18, 0.22), 0, 1.0, zz, 'iron_dark')
    for s in (-1, 1):
        lbox(f, (0.4, 5.2, 11.0), s * 5.2, -gd / 2 + 4.2, 5.5, 'wood_dark')
        for zz in (2.5, 8.5):
            lbox(f, (0.12, 4.8, 0.4), s * 5.0, -gd / 2 + 4.2, zz, 'iron')
    # flanking towers
    for s in (-1, 1):
        round_tower(s * (gw / 2 + 5.0), -1.5, 8.0, 44.0, doors=(), seed=50 + s, slit_rows=(12, 20, 28))
        fb = F(s * (gw / 2 + 5.0), -1.5 - 8.0, 0, 0)
        lbeam(fb, (0, -0.1, 33.0), (0, -1.6, 33.0), 0.25, 'gold')
        from props import cloth
        cloth(nm('ban'), 4.2, 13.0, fb.p(0, -1.6, 33.0), 'fabric_red', waves=0.6, amp=0.15, seed=s + 3)
        lbox(fb, (0.6, 0.2, 13.0), 0, -1.75, 26.5, 'gold')
    # paving through the passage
    lbox(f, (11.0, gd + 4, 0.25), 0, 0, 0.12, 'stone_dark')
    return finalize('grand_gate', smooth_angle=20)


ITEMS_WALLS = [
    ('C01_city_wall_straight', city_wall_straight), ('C02_city_wall_corner', city_wall_corner),
    ('C03_city_wall_tower', city_wall_tower), ('C04_grand_gate', grand_gate),
]


# ============================================================ grand market
def arcade(f, x0, x1, bays, t, spring, r, top, key='ashlar', trim='castle_trim'):
    """Row of round arches along local x (outer face at local y=0, depth t inward)."""
    bw = (x1 - x0) / bays
    for i in range(bays):
        a = x0 + bw * i
        arch_block(f, a, a + bw, 0, t, 0, top, a + bw / 2, spring, r, key)
        tube(nm('ar'), arc_pts(f, a + bw / 2, spring, r + 0.3, y=-0.15, n=13), 0.32, trim, res=4)
        lbox(f, (0.7, 0.5, 0.8), a + bw / 2, -0.2, spring + r + 0.3, trim, bev=0.05)
    for i in range(bays + 1):
        xx = x0 + bw * i
        lbox(f, (bw - 2 * r + 0.4, 0.4, 0.6), xx, -0.15, 0.3, 'stone_dark')
        lbox(f, (bw - 2 * r + 0.3, 0.35, 0.45), xx, -0.15, spring - 0.2, trim)


def oriel(f, x, z, w=5.0, h=5.6, dep=1.6, wall='plaster', keys=('tile_a', 'tile_b'), frame='wood_paint', glass='glass_dark', lit=False):
    lbox(f, (w, dep, h), x, -dep / 2, z + h / 2, wall)
    for k, (ww, zz) in enumerate(((w, 0.0), (w * 0.8, -0.5), (w * 0.55, -1.0))):
        lbox(f, (ww, dep * (1 - k * 0.25), 0.5), x, -dep * (1 - k * 0.25) / 2, z + zz - 0.25, 'timber')
    fo = f.sub(x, -dep, z)
    window(fo, 0, 1.0, w=w - 1.6, h=h - 2.0, frame=frame, sill=frame, lit=lit, glass=glass)
    for s in (-1, 1):
        window(f.sub(x + s * w / 2, -dep / 2, z, s * 90), 0, 1.0, w=dep * 0.55, h=h - 2.0, frame=frame, sill=None, panes=False, lit=lit, glass=glass)
    lslab(f, [(x - w / 2 - 0.2, 0, z + h + 1.8), (x - w / 2 - 0.2, -dep - 0.4, z + h - 0.1), (x - w / 2 - 0.2, 0, z + h - 0.1)], (w + 0.4, 0, 0), keys[0])


def market_hall():
    """C11 - covered market hall: open stone arcade below, timber hall above, roof cupola."""
    reset()
    W, D, sp, top = 32.0, 18.0, 6.0, 10.0
    fs = faces(0, 0, W, D)
    arcade(fs['front'], -W / 2, W / 2, 4, 1.6, sp, 2.9, top)
    arcade(fs['back'], -W / 2, W / 2, 4, 1.6, sp, 2.9, top)
    arcade(fs['left'], -D / 2, D / 2, 2, 1.6, sp, 2.9, top)
    arcade(fs['right'], -D / 2, D / 2, 2, 1.6, sp, 2.9, top)
    for x in (-8, 0, 8):
        cyl(nm('pi'), 0.8, top, loc=(x, 0, 0), key='ashlar', verts=12)
        cyl(nm('pc'), 1.1, 0.6, loc=(x, 0, top - 0.6), key='castle_trim', verts=12)
        cyl(nm('pb'), 1.1, 0.6, loc=(x, 0, 0), key='castle_trim', verts=12)
    rnd = random.Random(11)
    for i in range(30):
        box(nm('fl'), (rnd.uniform(2.5, 4), rnd.uniform(2.5, 4), 0.2), loc=(rnd.uniform(-14, 14), rnd.uniform(-7.5, 7.5), 0.1),
            key=rnd.choice(['cob_a', 'cob_b', 'cob_c', 'stone_light']), rot=(0, 0, rnd.uniform(0, 90)))
    box(nm('flr'), (W - 0.4, D - 0.4, 0.15), loc=(0, 0, 0.07), key='grout')
    for x, y in ((-10, -3), (-2, 3), (6, -3), (12, 3)):
        box(nm('tb'), (4.5, 2.4, 0.25), loc=(x, y, 3.0), key='wood_light')
        for s in (-1, 1):
            box(nm('tl'), (0.3, 2.0, 2.9), loc=(x + s * 1.9, y, 1.45), key='wood_dark')
        for k in range(3):
            box(nm('cr'), (1.2, 1.0, 0.7), loc=(x - 1.4 + k * 1.4, y, 3.45), key='wood', bev=0.03)
            for q in range(3):
                ball(nm('fr'), 0.24, loc=(x - 1.7 + k * 1.4 + q * 0.3, y + rnd.uniform(-0.2, 0.2), 3.95), key=rnd.choice(['fruit', 'fl_orange', 'leaf_light', 'fl_yellow']), segs=7, rings=5)
    band(0, 0, W, D, top - 0.1, 0.6, 'castle_trim', out=0.25)
    fh = 8.0
    box(nm('up'), (W, D, fh), loc=(0, 0, top + fh / 2), key='plaster')
    fu = faces(0, 0, W, D, top)
    for side, L in (('front', W), ('back', W), ('left', D), ('right', D)):
        n = 4 if L > 20 else 2
        posts = [-L / 2 + 0.21] + [-L / 2 + L * i / n for i in range(1, n)] + [L / 2 - 0.21]
        timber_frame(fu[side], L, 0, fh, posts, braces=True)
        for i in range(n):
            x = -L / 2 + L * (i + 0.5) / n
            window(fu[side], x, 2.0, w=3.0, h=4.0, arch=True, frame='wood_paint', sill='wood_paint', panes=True)
    hr = D * 0.45
    gable_roof(F(), W, D, top + fh, hr, keys=('tile_red_a', 'tile_red_b'), wall='plaster', ov=1.2, ovg=1.0)
    for g in (-1, 1):
        window(F(g * W / 2, 0, top + fh, g * 90), 0, 1.5, w=3.0, h=4.0, arch=True, frame='wood_paint', sill='wood_paint')
    zc = top + fh + hr - 1.5
    box(nm('cu'), (4.6, 4.6, 5.0), loc=(0, 0, zc + 2.5), key='plaster')
    for k, fr in enumerate(faces(0, 0, 4.6, 4.6, zc).values()):
        window(fr, 0, 1.4, w=2.0, h=3.0, arch=True, frame='wood_paint', sill=None, panes=False, lit=(k == 0))
    box(nm('cut'), (5.2, 5.2, 0.4), loc=(0, 0, zc + 5.2), key='timber')
    t = cone_roof(0, 0, zc + 5.4, 3.2, 5.0, keys=('tile_red_b', 'tile_red_a'), rings=4, ov=0.5, segs=4, finial='brass')
    # weather vane
    lbeam(F(), (-1.4, 0, t + 3.0), (1.4, 0, t + 3.0), 0.12, 'brass')
    lslab(F(), [(1.4, 0, t + 3.5), (2.2, 0, t + 3.0), (1.4, 0, t + 2.5)], (0, 0.08, 0), 'brass')
    lslab(F(), [(-1.4, 0, t + 3.5), (-0.6, 0, t + 3.0), (-1.4, 0, t + 2.5)], (0, 0.08, 0), 'brass')
    for s in (-1, 1):
        hanging_sign(fs['front'].sub(0, -0.3), s * 12.0, top + 0.5, board='fabric_green' if s < 0 else 'fabric_red')
    return finalize('market_hall', smooth_angle=30)


def loaf(name, loc, L=1.0, key='bread', rot=0.0):
    o = ball(name, L * 0.5, loc=loc, key=key, segs=10, rings=6, scale=(1.0, 0.55, 0.42))
    o.rotation_euler.z = math.radians(rot)
    for k in (-1, 0, 1):
        box(nm('sc'), (0.06, L * 0.4, 0.05), loc=(loc[0] + math.cos(math.radians(rot)) * k * L * 0.22, loc[1] + math.sin(math.radians(rot)) * k * L * 0.22, loc[2] + L * 0.2),
            key='bread_dark', rot=(0, 0, rot + 20))


def basket(x, y, z, r=0.9, h=0.8, n=4, seed=0):
    rnd = random.Random(seed)
    lathe(nm('bk'), [(0.0, 0.0), (r * 0.8, 0.0), (r, h), (r * 0.9, h), (r * 0.72, 0.12), (0.0, 0.12)], loc=(x, y, z), key='wicker', segs=14)
    torus(nm('bkr'), r * 0.95, 0.06, loc=(x, y, z + h), key='wood_light', segs=14, rsegs=4)
    for i in range(n):
        loaf(nm('lo'), (x + rnd.uniform(-r * 0.4, r * 0.4), y + rnd.uniform(-r * 0.4, r * 0.4), z + h * 0.8), L=rnd.uniform(0.8, 1.1), rot=rnd.uniform(0, 180))


def pretzel_sign(f, x, z):
    lbeam(f, (x, -0.1, z), (x, -2.4, z), 0.16, 'iron')
    lbox(f, (0.5, 0.2, 0.9), x, -0.1, z - 0.2, 'iron')
    c = f.sub(x, -1.6, z - 1.6, 90)
    tube(nm('pz'), [c.p(-1.0, 0, 0.0), c.p(-1.1, 0, 0.9), c.p(-0.5, 0, 1.3), c.p(0.3, 0, 0.3), c.p(0.6, 0, -0.6)], 0.2, 'bread', res=6)
    tube(nm('pz'), [c.p(1.0, 0, 0.0), c.p(1.1, 0, 0.9), c.p(0.5, 0, 1.3), c.p(-0.3, 0, 0.3), c.p(-0.6, 0, -0.6)], 0.2, 'bread', res=6)
    tube(nm('pz'), [c.p(-1.0, 0, 0.0), c.p(0.0, 0, -0.75), c.p(1.0, 0, 0.0)], 0.2, 'bread', res=6)
    lbox(f, (0.06, 0.06, 0.4), x, -1.6, z - 0.2, 'iron')


def bakery():
    """C12 - bakery: two-storey timber house, big oven chimney, bread display, baskets and pretzel sign."""
    reset()
    w, d = 15.0, 14.0
    top = house(w=w, d=d, floors=2, upper='plaster_d', rkeys=('tile_red_a', 'tile_red_b'), roof='front', shutter='shutter_g',
                flowers=('fl_red', 'fl_yellow'), shop=True, seed=12, chim=False, door_bay=1, lit={(0, 0)})
    fr = faces(0, 0, w, d)['front']
    pretzel_sign(fr, 2.5, 7.4)
    chimney(-w / 2 + 1.6, d * 0.25, 2.0, top + 10.0, w=3.0)
    lbox(fr, (6.0, 1.0, 0.25), -3.75, -0.6, 1.3, 'wood')
    for k in range(5):
        loaf(nm('lo'), fr.p(-6.0 + k * 1.1, -0.6, 1.7), L=0.95, rot=90)
    lbox(F(0, -d / 2 - 2.2, 0), (4.5, 1.8, 0.25), 3.8, 0, 2.8, 'wood_light')
    for s in (-1, 1):
        lbox(F(0, -d / 2 - 2.2, 0), (0.3, 1.5, 2.8), 3.8 + s * 1.9, 0, 1.4, 'wood_dark')
    basket(2.6, -d / 2 - 2.2, 2.92, seed=1)
    basket(4.9, -d / 2 - 2.2, 2.92, r=0.8, seed=2)
    for i, (x, y) in enumerate(((-6.5, -d / 2 - 1.4), (-5.2, -d / 2 - 1.8))):
        cyl(nm('sk'), 0.75, 1.6, loc=(x, y, 0), key='fabric_cream', verts=12, r2=0.55)
        lathe(nm('skt'), [(0.0, 1.55), (0.6, 1.55), (0.25, 1.9), (0.4, 2.1), (0.0, 2.2)], loc=(x, y, 0), key='fabric_cream', segs=10)
    return finalize('bakery', smooth_angle=30)


def bottle(x, y, z, key, s=1.0, kind=0):
    if kind == 0:
        prof = [(0, 0), (0.28, 0), (0.32, 0.25), (0.3, 0.5), (0.1, 0.7), (0.1, 0.9), (0, 0.9)]
    elif kind == 1:
        prof = [(0, 0), (0.18, 0), (0.36, 0.25), (0.36, 0.42), (0.1, 0.62), (0.1, 0.85), (0, 0.85)]
    else:
        prof = [(0, 0), (0.22, 0), (0.22, 0.6), (0.08, 0.72), (0.08, 0.95), (0, 0.95)]
    lathe(nm('bt'), [(r * s, zz * s) for r, zz in prof], loc=(x, y, z), key=key, segs=8)
    cyl(nm('cork'), 0.09 * s, 0.15 * s, loc=(x, y, z + prof[-1][1] * s), key='wood_light', verts=6)


def potion_shop():
    """C13 - potion shop: tall lilac house, bay window full of glowing bottles, hanging glow lanterns."""
    reset()
    w, d = 13.0, 13.0
    house(w=w, d=d, floors=3, upper='plaster_purple', ground='ashlar_dark', ground_trim='ashlar', timber=True,
          rkeys=('tile_grey', 'tile_b'), roof='front', shutter='shutter_b', flowers=('fl_purple', 'fl_blue', 'fl_white'),
          shop=True, seed=13, door_bay=1, sign='fabric_green', pitch=0.55, lit={(1, 0)})
    fr = faces(0, 0, w, d)['front']
    lbox(fr, (5.0, 1.2, 0.25), -3.25, -0.7, 1.35, 'wood_dark')
    lbox(fr, (5.0, 0.6, 0.2), -3.25, -0.4, 3.2, 'wood_dark')
    rnd = random.Random(13)
    keys = ['potion_red', 'potion_blue', 'potion_green', 'magic_purple']
    for k in range(9):
        bottle(fr.p(-5.4 + k * 0.55, -0.8, 1.48)[0], fr.p(0, -0.8, 0)[1], 1.48, rnd.choice(keys), s=rnd.uniform(0.7, 1.0), kind=k % 3)
    for k in range(8):
        bottle(fr.p(-5.2 + k * 0.6, -0.4, 3.3)[0], fr.p(0, -0.4, 0)[1], 3.3, rnd.choice(keys), s=0.65, kind=(k + 1) % 3)
    oriel(faces(0, 0, w, d + 1.4, 8.0)['front'], -3.25, 1.2, w=4.6, h=5.0, dep=1.5, wall='plaster_purple', keys=('tile_grey',), lit=True)
    for x in (-6.0, 5.6):
        f2 = fr.sub(0, 0, 0)
        lbeam(f2, (x, -0.1, 7.3), (x, -1.3, 7.3), 0.12, 'iron')
        chain_pts = [f2.p(x, -1.3, 7.3), f2.p(x, -1.3, 6.6)]
        tube(nm('ch'), chain_pts, 0.04, 'iron', res=4)
        ball(nm('orb'), 0.45, loc=f2.p(x, -1.3, 6.1), key='magic_purple' if x < 0 else 'magic', segs=10, rings=7)
        torus(nm('cage'), 0.48, 0.05, loc=f2.p(x, -1.3, 6.1), key='iron', segs=12, rsegs=4)
    for k, (x, y) in enumerate(((5.0, -d / 2 - 1.6), (6.2, -d / 2 - 2.6))):
        cyl(nm('cau'), 0.9 - k * 0.2, 1.2, loc=(x, y, 0), key='iron_dark', verts=14, r2=1.05 - k * 0.2)
        cyl(nm('cl'), 0.85 - k * 0.2, 0.05, loc=(x, y, 1.15), key='potion_green', verts=14)
    return finalize('potion_shop', smooth_angle=30)


def star_pts(r0, r1, n=5):
    return [((r1 if i % 2 == 0 else r0) * math.cos(math.pi / 2 + math.pi * i / n), (r1 if i % 2 == 0 else r0) * math.sin(math.pi / 2 + math.pi * i / n))
            for i in range(2 * n)]


def magic_tool_shop():
    """C14 - magic tool shop: blue-roofed house, oriel window, star sign, wand barrel and glowing orbs."""
    reset()
    w, d = 16.0, 14.0
    house(w=w, d=d, floors=3, upper='plaster_b', rkeys=('tile_a', 'tile_b'), roof='side', shutter='shutter_b',
          flowers=('fl_blue', 'fl_white'), shop=True, seed=14, dormers=1, door_bay=2, lit={(1, 1)})
    fr = faces(0, 0, w, d)['front']
    oriel(faces(0, 0, w, d + 1.4, 8.0)['front'], -2.7, 1.2, w=4.8, h=5.0, dep=1.6, wall='plaster_b', keys=('tile_a',), lit=True)
    lbeam(fr, (4.6, -0.1, 7.6), (4.6, -2.6, 7.6), 0.16, 'iron')
    lbox(fr, (0.5, 0.2, 0.9), 4.6, -0.1, 7.4, 'iron')
    fs = fr.sub(4.6, -1.8, 6.2, 90)
    pts = star_pts(0.5, 1.15)
    lslab(fs, [(px, 0, pz) for px, pz in pts], (0, 0.25, 0), 'gold')
    tube(nm('sgc'), [fr.p(4.6, -1.8, 7.6), fr.p(4.6, -1.8, 7.3)], 0.04, 'iron', res=4)
    ball(nm('so'), 0.3, loc=fs.p(0, -0.05, 0), key='magic', segs=8, rings=6)
    from props import barrel_body
    barrel_body('wb', loc=(6.0, -d / 2 - 1.8, 0), h=3.0, open_top=True)
    rnd = random.Random(14)
    for i in range(9):
        a = rnd.uniform(0, 6.28); rr = rnd.uniform(0, 0.7)
        x, y = 6.0 + math.cos(a) * rr, -d / 2 - 1.8 + math.sin(a) * rr
        tube(nm('wd'), [(x, y, 2.0), (x + rnd.uniform(-0.4, 0.4), y + rnd.uniform(-0.4, 0.4), 4.2)], 0.07, rnd.choice(['wood_dark', 'wood_light', 'bark']), res=4, taper=[1, 0.7])
        if i % 3 == 0:
            ball(nm('wt'), 0.12, loc=(x, y, 4.25), key=rnd.choice(['magic', 'magic_purple']), segs=6, rings=4)
    for x in (-7.2, 1.3):
        cyl(nm('op'), 0.25, 3.2, loc=fr.p(x, -1.3, 0), key='iron', verts=8)
        lathe(nm('oc'), [(0, 3.2), (0.5, 3.2), (0.2, 3.5), (0, 3.5)], loc=fr.p(x, -1.3, 0), key='iron', segs=8)
        ball(nm('oo'), 0.5, loc=fr.p(x, -1.3, 4.0), key='magic', segs=10, rings=7)
    return finalize('magic_tool_shop', smooth_angle=30)


def clock_face(f, z, r=3.6):
    o = cyl(nm('cf'), r, 0.3, loc=f.p(0, 0, z), key='marble', verts=32, rot=f.r(90, 0, 0))
    torus(nm('cr'), r, 0.25, loc=f.p(0, -0.3, z), key='gold', segs=32, rsegs=6, rot=f.r(90, 0, 0))
    for i in range(12):
        a = math.radians(90 - i * 30)
        big = i % 3 == 0
        lbox(f, (0.25 if not big else 0.4, 0.1, 0.7 if big else 0.45), math.cos(a) * r * 0.8, -0.35, z + math.sin(a) * r * 0.8, 'iron_dark',
             rot=(0, -math.degrees(a) + 90, 0))
    lbeam(f, (0, -0.4, z), (math.cos(math.radians(60)) * r * 0.5, -0.4, z + math.sin(math.radians(60)) * r * 0.5), 0.22, 'iron_dark')
    lbeam(f, (0, -0.5, z), (math.cos(math.radians(-30)) * r * 0.74, -0.5, z + math.sin(math.radians(-30)) * r * 0.74), 0.16, 'iron_dark')
    cyl(nm('hub'), 0.3, 0.3, loc=f.p(0, -0.3, z), key='gold', verts=10, rot=f.r(90, 0, 0))


def clock_tower():
    """C15 - square stone clock tower with four clock faces, open belfry with bell, spire and pinnacles."""
    reset()
    s, H = 12.0, 44.0
    box(nm('ct'), (s, s, H), loc=(0, 0, H / 2), key='ashlar')
    box(nm('cp'), (s + 1.2, s + 1.2, 2.4), loc=(0, 0, 1.2), key='ashlar_dark', bev=0.1)
    for zz in (14.0, 28.0, H - 0.5):
        band(0, 0, s, s, zz, 0.6, 'castle_trim', out=0.3)
    fs = faces(0, 0, s, s)
    for k, (nmf, fr) in enumerate(fs.items()):
        quoins(F(*fr.p(-s / 2, 0, 0), fr.rz), 2.4, H - 0.6, 'castle_trim', course=1.2)
        stone_face(fr, -s / 2, s / 2, 2.5, H - 1, 40, 150 + k)
        for zz in (9.0, 21.0):
            arrow_slit(fr, 0, zz, h=3.2) if zz < 15 else window(fr, 0, zz - 1.5, w=1.8, h=4.0, arch=True, frame='ashlar_dark', sill='castle_trim', panes=False)
        clock_face(fr, 36.0)
        lbox(fr, (9.4, 0.5, 9.4), 0, -0.1, 36.0, 'castle_trim', bev=0.1)
    door(fs['front'], 0, w=3.6, h=7.0, surround='castle_trim', lamp=True)
    # belfry
    zb, bh = H, 11.0
    for fr in faces(0, 0, s, s, zb).values():
        arch_block(fr, -s / 2, s / 2, 0, 1.4, 0, bh, 0, 6.0, 3.0, 'ashlar')
        tube(nm('ba'), arc_pts(fr, 0, 6.0, 3.3, y=-0.15, n=13), 0.3, 'castle_trim', res=4)
        railing(fr, -2.9, 2.9, 0.0, y=-0.2, h=1.6, key='iron')
    box(nm('bf'), (s, s, 0.6), loc=(0, 0, zb + 0.3), key='stone_dark')
    lathe(nm('bell'), [(0.0, 0.0), (2.1, 0.0), (2.2, 0.3), (1.6, 0.9), (1.35, 2.4), (1.2, 3.3), (0.5, 3.6), (0.0, 3.6)], loc=(0, 0, zb + 3.6), key='bronze', segs=20)
    box(nm('yoke'), (s - 2.6, 0.6, 0.8), loc=(0, 0, zb + 7.6), key='timber')
    ball(nm('clap'), 0.4, loc=(0, 0, zb + 3.4), key='iron_dark', segs=8, rings=6)
    zt = zb + bh
    box(nm('bt'), (s + 0.8, s + 0.8, 1.0), loc=(0, 0, zt + 0.5), key='castle_trim', bev=0.08)
    cone_roof(0, 0, zt + 1.0, s / 2 * 1.414, 18.0, keys=('tile_a', 'tile_b'), rings=8, ov=0.3, segs=4, flag='fabric_red')
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * (s / 2 - 0.2), sy * (s / 2 - 0.2)
            box(nm('pn'), (1.4, 1.4, 2.6), loc=(x, y, zt + 2.3), key='castle_trim', bev=0.08)
            cone_roof(x, y, zt + 3.6, 0.9, 4.0, keys=('tile_b',), rings=2, ov=0.2, segs=4, finial='gold')
    return finalize('clock_tower', smooth_angle=25)


ITEMS_MARKET = [
    ('C11_market_hall', market_hall), ('C12_bakery', bakery), ('C13_potion_shop', potion_shop),
    ('C14_magic_tool_shop', magic_tool_shop), ('C15_clock_tower', clock_tower),
]



# ============================================================ civic and magic buildings
from arch import lancet, rose_window, column_c, pediment, dome, pinnacle, lancet_pts

GLASS = ['stained_b', 'stained_r', 'stained_g', 'stained_y']


def pointed_portal(f, x, w, h, orders=3, door_key='door_paint', trim='castle_trim', tymp='gold'):
    zs = h - w * 0.866
    lslab(f, [(px, 0.05, pz) for px, pz in lancet_pts(x, 0, zs, w)], (0, -0.25, 0), door_key)
    lbox(f, (0.12, 0.3, zs + w * 0.8), x, -0.2, (zs + w * 0.8) / 2, 'iron')
    for k in range(orders):
        ww = w + 1.0 + k * 1.1
        pts = lancet_pts(x, 0, zs, ww)
        tube(nm('po'), [f.p(px, -0.4 - k * 0.5, pz) for px, pz in pts[1:-1]], 0.35, trim, res=4)
        for s in (-1, 1):
            cyl(nm('pc'), 0.32, zs, loc=f.p(x + s * ww / 2, -0.4 - k * 0.5, 0), key=trim, verts=8)
    cyl(nm('ty'), w * 0.22, 0.2, loc=f.p(x, -0.25, zs + w * 0.35), key=tymp, verts=16, rot=f.r(90, 0, 0))
    for zz in (zs * 0.3, zs * 0.7):
        lbox(f, (w * 0.9, 0.1, 0.25), x, -0.32, zz, 'iron')


def cathedral():
    """C16 - grand cathedral: twin-spired west front, rose window, flying buttresses, transept, apse."""
    reset()
    NW, NL, NH = 22.0, 60.0, 32.0
    y0 = -NL / 2
    box(nm('nave'), (NW, NL, NH), loc=(0, 0, NH / 2), key='castle')
    box(nm('plinth'), (NW + 18, NL + 4, 1.2), loc=(0, 2, 0.6), key='ashlar_dark')
    gable_roof(F(0, 0, 0, 90), NL, NW, NH, 15.0, keys=('tile_a', 'tile_b'), wall='castle', ov=0.8, ovg=0.6, barge='castle_trim', ridge='gold')
    for s in (-1, 1):
        ax = s * (NW / 2 + 4.0)
        box(nm('aisle'), (8.0, NL - 14, 17.0), loc=(ax, 5, 8.5), key='castle')
        lslab(F(), [(s * NW / 2, y0 + 12, 22.0), (s * (NW / 2 + 8.6), y0 + 12, 16.4), (s * (NW / 2 + 8.6), y0 + 12, 17.0), (s * NW / 2, y0 + 12, 17.0)],
              (0, NL - 14, 0), 'tile_b')
        fa = F(s * (NW / 2 + 8.0), 0, 0, s * 90)
        fn_ = F(s * NW / 2, 0, 17.0, s * 90)
        for i in range(5):
            yy = y0 + 16 + i * 9.0
            lx = yy * s
            if abs(yy - 10) < 6:
                continue
            lancet(fa, lx, 3.5, w=2.6, h=10.0, glass=GLASS[i % 4])
            lancet(fn_, lx, 6.5, w=2.4, h=7.5, glass=GLASS[(i + 1) % 4], medallion=None)
        for i in range(6):
            yy = y0 + 11.5 + i * 9.0
            if abs(yy - 10) < 7:
                continue
            px = s * (NW / 2 + 10.0)
            box(nm('bp'), (2.6, 2.6, 21.0), loc=(px, yy, 10.5), key='castle', bev=0.08)
            box(nm('bpb'), (3.4, 3.4, 2.0), loc=(px, yy, 1.0), key='ashlar_dark', bev=0.08)
            pinnacle(px, yy, 21.0, s=1.8, h=7.0)
            p0 = Vector((px - s * 1.3, yy, 20.0)); p1 = Vector((s * NW / 2, yy, 27.5))
            beam3(p0, p1, 1.2, 1.4, 'castle')
            tube(nm('fb'), [(px - s * 1.3, yy, 17.5), (s * (NW / 2 + 5.0), yy, 21.5), (s * NW / 2, yy, 25.0)], 0.5, 'castle_trim', res=4)
    # transept
    ty = 10.0
    box(nm('tr'), (NW + 26, 14.0, NH - 2), loc=(0, ty, (NH - 2) / 2), key='castle')
    gable_roof(F(0, ty, 0, 0), NW + 26, 14.0, NH - 2, 9.5, keys=('tile_a', 'tile_b'), wall='castle', ov=0.8, ovg=0.6, barge='castle_trim')
    for s in (-1, 1):
        ft = F(s * (NW / 2 + 13), ty, 0, s * 90)
        rose_window(ft, 0, 21.0, 4.2)
        lancet(ft, -3.0, 4.0, w=2.2, h=9.0, glass='stained_r')
        lancet(ft, 3.0, 4.0, w=2.2, h=9.0, glass='stained_b')
        door(ft, 0, w=3.4, h=7.0, surround='castle_trim', step='ashlar_dark')
        for g in (-1, 1):
            pinnacle(s * (NW / 2 + 13), ty + g * 6.6, NH - 2, s=1.4, h=6.0)
    # crossing fleche
    box(nm('cx'), (5, 5, 6), loc=(0, ty, NH + 13), key='castle_trim')
    for fr in faces(0, ty, 5, 5, NH + 13).values():
        lancet(fr, 0, 1.0, w=1.4, h=4.2, glass='stained_y', medallion=None, lead=False)
    lathe(nm('fl'), [(0.0, 0.0), (3.6, 0.0), (0.0, 16.0)], loc=(0, ty, NH + 19), key='tile_b', segs=8)
    lathe(nm('flf'), [(0, 0), (0.25, 0), (0.08, 3.0), (0, 3.2)], loc=(0, ty, NH + 35), key='gold', segs=6)
    # apse
    ay = NL / 2
    lathe(nm('ap'), [(0.0, 0.0), (NW / 2, 0.0), (NW / 2, NH - 2), (0.0, NH - 2)], loc=(0, ay, 0), key='castle', segs=16)
    lathe(nm('apr'), [(0.0, NH - 2.6), (NW / 2 + 1.0, NH - 2.6), (0.0, NH + 8)], loc=(0, ay, 0), key='tile_b', segs=16)
    for i in range(5):
        a = math.radians(-10 + 40 * i) if False else math.radians(20 + 35 * i)
        fr = F(math.cos(a) * NW / 2, ay + math.sin(a) * NW / 2, 0, math.degrees(a) + 90)
        lancet(fr, 0, 6.0, w=2.2, h=12.0, glass=GLASS[i % 4])
    # west towers
    TW, TH = 12.0, 56.0
    for s in (-1, 1):
        tx, ty_ = s * (NW / 2 + 5.0), y0 + 4.0
        box(nm('wt'), (TW, TW, TH), loc=(tx, ty_, TH / 2), key='castle')
        for zz in (16.0, 34.0, TH - 0.6):
            band(tx, ty_, TW, TW, zz, 0.6, 'castle_trim', out=0.3)
        for k, fr in enumerate(faces(tx, ty_, TW, TW).values()):
            lancet(fr, 0, 20.0, w=2.4, h=10.0, glass=GLASS[(k + (s > 0)) % 4])
            lancet(fr, -2.0, 38.0, w=2.2, h=14.0, glass='glass_dark', medallion=None)
            lancet(fr, 2.0, 38.0, w=2.2, h=14.0, glass='glass_dark', medallion=None)
            lancet(fr, 0, 5.0, w=2.0, h=7.0, glass=GLASS[k % 4], medallion=None)
        for gx in (-1, 1):
            for gy in (-1, 1):
                pinnacle(tx + gx * (TW / 2 - 0.6), ty_ + gy * (TW / 2 - 0.6), TH, s=1.6, h=8.0)
        battlements(F(tx, ty_ - TW / 2, 0, 0), -TW / 2, TW / 2, TH, 'castle_trim', t=0.6, mw=0.9, gap=0.9, mh=1.2, ph=0.8)
        lathe(nm('sp'), [(0.0, 0.0), (TW / 2 - 1.0, 0.0), (0.0, 30.0)], loc=(tx, ty_, TH), key='tile_a', segs=8)
        for k in range(4):
            lathe(nm('spb'), [(0.0, 0.0), ((TW / 2 - 1.0) * (1 - (k * 6 + 4) / 30) + 0.25, 0.0), ((TW / 2 - 1.0) * (1 - (k * 6 + 4) / 30) + 0.25, 0.5), (0.0, 0.5)],
                  loc=(tx, ty_, TH + k * 6 + 4), key='castle_trim', segs=8)
        lathe(nm('spf'), [(0, 0), (0.35, 0), (0.12, 2.0), (0.3, 2.5), (0.08, 4.0), (0, 4.4)], loc=(tx, ty_, TH + 29.5), key='gold', segs=6)
        box(nm('cr1'), (0.25, 0.25, 2.6), loc=(tx, ty_, TH + 35.0), key='gold')
        box(nm('cr2'), (1.6, 0.25, 0.25), loc=(tx, ty_, TH + 35.6), key='gold')
    # west facade
    fw = F(0, y0, 0, 0)
    pointed_portal(fw, 0, 6.0, 14.0, orders=3)
    for s in (-1, 1):
        pointed_portal(F(s * (NW / 2 + 5.0), y0 + 4 - TW / 2, 0, 0), 0, 3.6, 9.0, orders=2)
    lbox(fw, (NW, 0.7, 0.7), 0, -0.3, 15.6, 'castle_trim')
    for i in range(7):
        lancet(fw, -NW / 2 + 2 + i * (NW - 4) / 6, 16.2, w=1.4, h=3.6, glass='glass_dark', medallion=None, lead=False)
    rose_window(fw, 0, 25.5, 6.2)
    lbox(fw, (NW, 0.7, 0.7), 0, -0.3, 32.6, 'castle_trim')
    gf = F(0, y0, NH, 0)
    lathe(nm('gc'), [(0, 0), (0.3, 0), (0.3, 3.0), (0, 3.0)], loc=gf.p(0, -0.3, 15.0), key='gold', segs=6)
    box(nm('gcx'), (2.0, 0.3, 0.3), loc=gf.p(0, -0.3, 17.0), key='gold')
    # front steps
    for k in range(4):
        box(nm('stp'), (NW + 6 - k * 1.2, 2.0, 0.5), loc=(0, y0 - 6.5 + k * 1.6, 0.25 + k * 0.5), key='ashlar' if k % 2 else 'ashlar_dark', bev=0.05)
    return finalize('cathedral', smooth_angle=25)


def squad_flag(x, y, z, key, emblem, h=7.0):
    cyl(nm('fp'), 0.18, h + 3, loc=(x, y, z), key='iron', verts=8)
    ball(nm('fpb'), 0.32, loc=(x, y, z + h + 3.1), key='gold', segs=8, rings=6)
    from props import cloth
    cloth(nm('sf'), 2.6, h * 0.6, (x + 1.4, y, z + h + 2.6), key, waves=0.8, amp=0.15, seed=int(x) % 9)
    ball(nm('se'), 0.45, loc=(x + 1.4, y - 0.12, z + h + 2.6 - h * 0.3), key=emblem, segs=8, rings=6, scale=(1, 0.3, 1))


def knights_hq():
    """C17 - Magic Knights headquarters: columned portico, green copper dome, squad flags along the front."""
    reset()
    W, D, H = 46.0, 28.0, 22.0
    box(nm('hq'), (W, D, H), loc=(0, 0, H / 2), key='castle')
    box(nm('pl'), (W + 1.0, D + 1.0, 2.0), loc=(0, 0, 1.0), key='ashlar_dark', bev=0.08)
    band(0, 0, W, D, 10.5, 0.7, 'castle_trim', out=0.3)
    band(0, 0, W, D, H - 0.2, 1.2, 'castle_trim', out=0.5)
    fs = faces(0, 0, W, D)
    for side, L in (('front', W), ('back', W), ('left', D), ('right', D)):
        fr = fs[side]
        n = int(L / 5.5)
        for i in range(n):
            x = -L / 2 + L * (i + 0.5) / n
            if side == 'front' and abs(x) < 9:
                continue
            window(fr, x, 3.0, w=2.4, h=5.4, arch=True, frame='castle_trim', sill='castle_trim', keystone='gold', lit=(i % 4 == 1))
            window(fr, x, 12.6, w=2.2, h=5.6, frame='castle_trim', sill='castle_trim', lintel='castle_trim', lit=(i % 5 == 2))
            lbox(fr, (0.9, 0.35, H - 2.4), x - L / n / 2, -0.17, H / 2 + 1.0, 'castle_trim') if i else None
        battlements(fr, -L / 2, L / 2, H + 1.0, 'castle', t=0.8, mw=1.2, gap=1.4, mh=1.2, ph=1.2, cap='castle_trim')
    # portico
    PD = 9.0
    fo = fs['front']
    for k in range(6):
        x = -10.0 + k * 4.0
        column_c(x, -D / 2 - PD + 1.2, 2.0, 16.0, 0.9)
    box(nm('ent'), (24.0, PD, 2.4), loc=(0, -D / 2 - PD / 2 + 0.5, 19.2), key='castle_trim')
    pediment(F(0, -D / 2 - PD, 0, 0), 0, 20.4, 25.0, 7.0, PD, emblem='gold')
    for k in range(6):
        box(nm('ps'), (26.0 - k * 1.6, 1.6, 0.5), loc=(0, -D / 2 - PD - 2.0 - (5 - k) * 1.6 + 7.0, 0.25 + k * 0.4), key='ashlar' if k % 2 else 'ashlar_dark')
    box(nm('pfl'), (24.0, PD + 1, 2.0), loc=(0, -D / 2 - PD / 2 + 0.5, 1.0), key='ashlar')
    door(fo, 0, w=5.0, h=10.0, arch=True, key='door_paint', surround='castle_trim', step=None)
    for s in (-1, 1):
        door(fo, s * 6.0, w=2.6, h=6.5, arch=True, key='door_paint', surround='castle_trim', step=None)
        # big hanging banner of the Clover kingdom
        from props import cloth
        cloth(nm('bn'), 3.6, 9.0, fo.p(s * 6.0, -0.3, 18.6), 'fabric_red', waves=0.5, amp=0.1, seed=s + 5)
        lbox(fo, (4.2, 0.3, 0.3), s * 6.0, -0.3, 18.7, 'gold')
    # dome on drum
    dome(0, 2.0, H + 1.0, 9.0, key='patina', ribs='castle_trim', drum='castle', drum_h=5.0, nrib=12)
    # corner pavilions
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * (W / 2 - 3.5), sy * (D / 2 - 3.5)
            box(nm('cp'), (8.0, 8.0, 6.0), loc=(x, y, H + 3.0), key='castle')
            band(x, y, 8, 8, H + 5.6, 0.6, 'castle_trim', out=0.3)
            lathe(nm('cpr'), [(0.0, 0.0), (5.6, 0.0), (0.0, 6.0)], loc=(x, y, H + 6.0), key='patina', segs=4)
            for fr in faces(x, y, 8, 8, H).values():
                window(fr, 0, 1.4, w=1.8, h=3.6, arch=True, frame='castle_trim', sill=None, panes=False)
    # squad flags along the front
    squads = [('fabric_blue', 'gold'), ('fabric_red', 'gold'), ('fabric_green', 'fl_white'), ('iron_dark', 'fabric_red'),
              ('fl_purple', 'gold'), ('fl_yellow', 'fabric_red'), ('fabric_cream', 'fabric_blue'), ('fl_orange', 'iron_dark')]
    for i, (k, e) in enumerate(squads):
        x = -W / 2 + 2.0 + i * 2.6 if i < 4 else W / 2 - 2.0 - (7 - i) * 2.6 - 0.0
        squad_flag(x - 1.3, -D / 2 - 3.0, 0.0, k, e)
    return finalize('knights_hq', smooth_angle=25)


def stepped_gable(f, x, w, z0, steps, step_h, key, trim):
    for k in range(steps):
        ww = w * (1 - k / steps)
        lbox(f, (ww, 1.0, step_h), x, 0.5, z0 + step_h * (k + 0.5), key)
        lbox(f, (ww + 0.3, 1.3, 0.3), x, 0.5, z0 + step_h * (k + 1) + 0.15, trim)
        for s in (-1, 1):
            if k:
                ball(nm('sgb'), 0.3, loc=f.p(x + s * (ww / 2 + w / steps / 2 - 0.3), 0.5, z0 + step_h * k + 0.6), key=trim, segs=8, rings=6)
    return z0 + step_h * steps


def guild_hall():
    """C18 - city / guild hall: arcaded ground floor, balcony, three stepped gables and a central onion-domed tower."""
    reset()
    W, D, gh, uh = 38.0, 20.0, 9.0, 14.0
    fs = faces(0, 0, W, D)
    arcade(fs['front'], -W / 2, W / 2, 5, 3.0, 5.5, 2.7, gh)
    box(nm('gb'), (W - 1, D - 6, gh), loc=(0, 3.0, gh / 2), key='ashlar_dark')
    for fr in (fs['back'], fs['left'], fs['right']):
        pass
    box(nm('gback'), (W, 3.0, gh), loc=(0, D / 2 - 1.5, gh / 2), key='ashlar')
    for s in (-1, 1):
        box(nm('gside'), (3.0, D, gh), loc=(s * (W / 2 - 1.5), 0, gh / 2), key='ashlar')
    for i in range(5):
        x = -W / 2 + W * (i + 0.5) / 5
        door(F(0, -D / 2 + 3.0, 0, 0), x, w=3.2, h=6.4, arch=True, surround='castle_trim', step=None) if i == 2 else \
            window(F(0, -D / 2 + 3.0, 0, 0), x, 2.0, w=3.0, h=4.8, arch=True, frame='wood_paint', sill='castle_trim', lit=True)
        window(fs['back'], x, 2.4, w=2.4, h=4.4, arch=True, frame='wood_paint', sill='castle_trim')
    band(0, 0, W, D, gh - 0.2, 0.8, 'castle_trim', out=0.3)
    box(nm('up'), (W, D, uh), loc=(0, 0, gh + uh / 2), key='plaster_rose')
    for side, L in (('front', W), ('back', W), ('left', D), ('right', D)):
        fr = faces(0, 0, W, D, gh)[side]
        n = 6 if L > 30 else 3
        for i in range(n):
            x = -L / 2 + L * (i + 0.5) / n
            window(fr, x, 1.8, w=2.4, h=4.4, frame='wood_paint', sill='castle_trim', lintel='castle_trim', shutter='shutter_r' if side != 'front' else None,
                   lit=(i % 3 == 1))
            window(fr, x, 8.4, w=2.2, h=3.6, arch=True, frame='wood_paint', sill='castle_trim', keystone='castle_trim')
        quoins(F(*fr.p(-L / 2, 0, 0), fr.rz), 0.2, uh - 0.2, 'castle_trim', course=1.2)
    band(0, 0, W, D, gh + uh - 0.2, 0.7, 'castle_trim', out=0.35)
    fu = faces(0, 0, W, D, gh)['front']
    lbox(fu, (16.0, 2.6, 0.5), 0, -1.3, 0.0, 'castle_trim')
    railing(fu, -8.0, 8.0, 0.25, y=-2.5, h=1.8, key='iron')
    for s in (-1, 1):
        lbox(fu, (0.1, 2.5, 0.12), s * 8.0, -1.3, 2.05, 'iron')
    for i in range(4):
        lbeam(fu, (-6.0 + i * 4.0, -0.1, -2.0), (-6.0 + i * 4.0, -2.4, -0.2), 0.4, 'castle_trim')
    # roof + three stepped gables on the front
    z0 = gh + uh
    gable_roof(F(), W, D, z0, 9.0, keys=('tile_grey', 'tile_b'), wall='plaster_rose', ov=0.6, ovg=0.4, barge='castle_trim')
    for k, x in enumerate((-12.0, 12.0)):
        fr = F(x, -D / 2, 0, 0)
        top = stepped_gable(fr, 0, 10.0, z0, 5, 2.2, 'plaster_rose', 'castle_trim')
        gable_roof(F(x, -D / 4, 0, 90), D / 2, 10.0, z0, top - z0 - 1.0, keys=('tile_grey', 'tile_b'), wall='plaster_rose', ov=0.2, ovg=0.1, infill=False)
        window(fr, 0, z0 + 1.5, w=2.0, h=4.0, arch=True, frame='wood_paint', sill='castle_trim', lit=(k == 0))
    # central tower
    tz = z0
    box(nm('tw'), (8.0, 8.0, 16.0), loc=(0, -D / 2 + 4.0, tz + 8.0), key='plaster_rose')
    quoins(F(-4.0, -D / 2, tz, 0), 0.0, 16.0, 'castle_trim', course=1.2)
    quoins(F(4.0, -D / 2, tz, 90), 0.0, 16.0, 'castle_trim', course=1.2)
    for fr in faces(0, -D / 2 + 4.0, 8, 8, tz).values():
        window(fr, 0, 6.0, w=2.2, h=5.0, arch=True, frame='wood_paint', sill='castle_trim', panes=False)
    clock_face(F(0, -D / 2 - 0.05, tz, 0), 13.0, r=2.6)
    band(0, -D / 2 + 4.0, 8, 8, tz + 16.0, 0.6, 'castle_trim', out=0.3)
    lathe(nm('on'), [(0.0, 0.0), (4.6, 0.0), (5.3, 1.6), (4.6, 3.6), (2.0, 5.6), (0.8, 7.0), (0.5, 8.6), (0.0, 8.8)],
          loc=(0, -D / 2 + 4.0, tz + 16.6), key='patina', segs=8)
    lathe(nm('onf'), [(0, 0), (0.3, 0), (0.12, 0.6), (0.35, 1.0), (0.08, 1.5), (0.06, 3.0), (0, 3.3)], loc=(0, -D / 2 + 4.0, tz + 25.2), key='gold', segs=8)
    for s in (-1, 1):
        lslab(F(s * 9.0, -D / 2 - 0.5, 0, 0), [(-1.4, 0, gh + 10.0), (1.4, 0, gh + 10.0), (1.4, 0, gh + 7.6), (0, 0, gh + 6.2), (-1.4, 0, gh + 7.6)],
              (0, -0.3, 0), 'fabric_blue' if s < 0 else 'fabric_green')
    return finalize('guild_hall', smooth_angle=25)


def royal_library():
    """C19 - royal library: white classical hall, tall arched windows, rotunda dome, grand steps."""
    reset()
    W, D, H = 44.0, 26.0, 24.0
    box(nm('lb'), (W, D, H), loc=(0, 0, H / 2), key='castle_trim')
    box(nm('lpl'), (W + 1.2, D + 1.2, 3.0), loc=(0, 0, 1.5), key='ashlar', bev=0.08)
    band(0, 0, W, D, H - 2.0, 2.0, 'castle', out=0.4)
    band(0, 0, W, D, H - 0.2, 0.6, 'castle_trim', out=0.8)
    lbox(F(), (W + 0.6, D + 0.6, 1.2), 0, 0, H + 1.2, 'castle_trim')
    for side, L in (('front', W), ('back', W), ('left', D), ('right', D)):
        fr = faces(0, 0, W, D)[side]
        n = int(L / 5.5)
        for i in range(n + 1):
            x = -L / 2 + L * i / n
            lbox(fr, (1.2, 0.6, H - 5.0), x, -0.3, 3.0 + (H - 5.0) / 2, 'castle')
            lbox(fr, (1.6, 0.8, 0.8), x, -0.4, H - 2.4, 'castle_trim')
        for i in range(n):
            x = -L / 2 + L * (i + 0.5) / n
            if side == 'front' and abs(x) < 6:
                continue
            window(fr, x, 5.0, w=2.8, h=12.0, arch=True, frame='castle', sill='castle', keystone='gold', lit=(i % 3 == 0))
        for i in range(n):
            x = -L / 2 + L * (i + 0.5) / n
            lbox(fr, (2.0, 0.3, 0.6), x, -0.2, H - 1.0, 'castle')
    # entrance portico with 4 columns
    for k in range(4):
        column_c(-6.0 + k * 4.0, -D / 2 - 5.0, 3.0, 17.0, 0.85, key='castle_trim', base='castle')
    box(nm('ent'), (16.0, 6.2, 2.0), loc=(0, -D / 2 - 2.6, 21.0), key='castle')
    pediment(F(0, -D / 2 - 5.8, 0, 0), 0, 22.0, 17.0, 5.0, 6.0, key='castle', tymp='castle_trim', emblem='gold')
    box(nm('pf'), (16.0, 6.4, 3.0), loc=(0, -D / 2 - 2.6, 1.5), key='ashlar')
    for k in range(6):
        box(nm('st'), (20.0 - k * 0.8, 1.4, 0.5), loc=(0, -D / 2 - 6.0 - (5 - k) * 1.4, 0.25 + k * 0.5 - 0.0), key='castle' if k % 2 else 'ashlar')
    door(faces(0, 0, W, D)['front'], 0, w=4.4, h=10.0, key='door_paint', surround='castle', step=None)
    for s in (-1, 1):
        # stone book statues / lamp urns beside steps
        lathe(nm('urn'), [(0, 0), (1.2, 0), (1.2, 1.2), (0.6, 1.6), (1.0, 2.6), (1.2, 3.6), (0.4, 4.0), (0, 4.0)], loc=(s * 10.5, -D / 2 - 10.0, 0), key='castle', segs=12)
        ball(nm('urnf'), 0.7, loc=(s * 10.5, -D / 2 - 10.0, 4.4), key='magic', segs=10, rings=7)
    # rotunda
    lathe(nm('ro'), [(0.0, H), (11.0, H), (11.0, H + 8.0), (0.0, H + 8.0)], loc=(0, 1.0, 0), key='castle_trim', segs=32)
    for i in range(16):
        a = 2 * math.pi * i / 16
        column_c(math.cos(a) * 11.6, 1.0 + math.sin(a) * 11.6, H + 1.2, 6.8, 0.45, key='castle_trim', base='castle')
        if i % 2:
            window(F(math.cos(a) * 11.0, 1.0 + math.sin(a) * 11.0, 0, math.degrees(a) + 90), 0, H + 2.0, w=1.8, h=5.0, arch=True, frame='castle', sill=None, panes=False, lit=True)
    lathe(nm('roc'), [(0.0, H + 8.0), (12.6, H + 8.0), (12.6, H + 9.0), (0.0, H + 9.0)], loc=(0, 1.0, 0), key='castle', segs=32)
    dome(0, 1.0, H + 9.0, 10.5, key='tile_a', ribs='gold', nrib=16)
    return finalize('royal_library', smooth_angle=25)


def crystal(x, y, z, h, r, key='magic'):
    lathe(nm('cy'), [(0.0, 0.0), (r, h * 0.3), (r * 0.9, h * 0.7), (0.0, h)], loc=(x, y, z), key=key, segs=6)


def magic_academy():
    """C20 - magic academy: grand hall with slender pointed towers, observatory dome and floating crystals."""
    reset()
    W, D, H = 36.0, 22.0, 26.0
    box(nm('ma'), (W, D, H), loc=(0, 0, H / 2), key='castle')
    box(nm('mpl'), (W + 1, D + 1, 2.0), loc=(0, 0, 1.0), key='ashlar_dark', bev=0.08)
    for zz in (12.0, H - 0.4):
        band(0, 0, W, D, zz, 0.6, 'castle_trim', out=0.3)
    for side, L in (('front', W), ('back', W), ('left', D), ('right', D)):
        fr = faces(0, 0, W, D)[side]
        n = int(L / 6)
        for i in range(n):
            x = -L / 2 + L * (i + 0.5) / n
            if side == 'front' and abs(x) < 5:
                continue
            lancet(fr, x, 3.0, w=2.4, h=7.0, glass='stained_b' if i % 2 else 'stained_y', medallion=None)
            lancet(fr, x, 14.0, w=2.4, h=9.0, glass='magic_purple' if i % 3 == 0 else 'stained_b', medallion='stained_y')
    gable_roof(F(), W, D, H, 12.0, keys=('tile_b', 'tile_a'), wall='castle', ov=0.8, ovg=0.6, barge='castle_trim', ridge='gold')
    for i in range(3):
        dormer(F(), -10.0 + i * 10.0, -D / 2 + 2.0, roof_z(H, 12.0, D, -D / 2 + 2.0) - 0.4, w=4.0, h=4.4, depth=6.0, wall='castle', keys=('tile_b',), frame='castle_trim')
    fo = faces(0, 0, W, D)['front']
    pointed_portal(fo, 0, 5.0, 11.0, orders=2, tymp='magic')
    rose_window(fo, 0, 18.0, 3.6, keys=('magic_purple', 'stained_b', 'stained_y', 'magic'))
    # slender towers
    towers = [(-W / 2, -D / 2, 4.0, 46.0, 'tile_b'), (W / 2, -D / 2, 4.0, 52.0, 'tile_a'), (-W / 2, D / 2, 3.4, 40.0, 'tile_a'), (W / 2 + 2, D / 2 + 2, 5.0, 34.0, None)]
    for k, (x, y, r, h, rk) in enumerate(towers):
        lathe(nm('st'), [(0.0, 0.0), (r + 0.8, 0.0), (r + 0.8, 2.0), (r, 2.6), (r, h), (0.0, h)], loc=(x, y, 0), key='castle', segs=20)
        for zz in (12.0, H, h - 0.2):
            lathe(nm('stb'), [(0.0, zz - 0.3), (r + 0.3, zz - 0.3), (r + 0.3, zz + 0.3), (0.0, zz + 0.3)], loc=(x, y, 0), key='castle_trim', segs=20)
        for j in range(3):
            a = -90 + (j - 1) * 80 + (0 if y < 0 else 180)
            ar = math.radians(a)
            lancet(F(x + math.cos(ar) * r, y + math.sin(ar) * r, 0, a + 90), 0, h - 9.0, w=1.4, h=4.6, glass='magic_purple' if j == 1 else 'stained_b', medallion=None, lead=False)
            lancet(F(x + math.cos(ar) * r, y + math.sin(ar) * r, 0, a + 90), 0, h * 0.45, w=1.2, h=3.6, glass='glass_dark', medallion=None, lead=False)
        if rk:
            lathe(nm('sb'), [(0.0, h), (r + 1.0, h), (r + 1.0, h + 0.6), (0.0, h + 0.6)], loc=(x, y, 0), key='castle_trim', segs=20)
            cone_roof(x, y, h + 0.6, r + 0.4, (r + 0.4) * 3.4, keys=(rk, 'tile_b' if rk == 'tile_a' else 'tile_a'), rings=7, ov=0.4, finial='gold')
        else:
            # observatory
            dome(x, y, h, r + 0.6, key='patina', ribs='brass', nrib=10, lantern=False, finial=None)
            lbeam(F(), (x, y, h + r * 0.7), (x + 4.5, y - 3.2, h + r * 1.6 + 2.4), 1.1, 'brass')
            lbeam(F(), (x + 4.5, y - 3.2, h + r * 1.6 + 2.4), (x + 5.2, y - 3.7, h + r * 1.6 + 2.9), 1.5, 'iron_dark')
            ring_battlements(x, y, h - 0.6, r + 1.2, 'castle', t=0.6, mh=0.6, ph=1.0, machicolate=False, n=12)
    # floating crystals over the roof and before the door
    rnd = random.Random(20)
    for i in range(5):
        x, y = rnd.uniform(-12, 12), rnd.uniform(-2, 2)
        zc = H + 16 + rnd.uniform(0, 6)
        crystal(x, y, zc, rnd.uniform(2.5, 4.0), rnd.uniform(0.6, 1.0), key=rnd.choice(['magic', 'magic_purple']))
        torus(nm('cring'), 1.4, 0.06, loc=(x, y, zc + 1.2), key='magic', segs=16, rsegs=4, rot=(rnd.uniform(-30, 30), rnd.uniform(-30, 30), 0))
    for s in (-1, 1):
        lathe(nm('pd'), [(0, 0), (1.3, 0), (1.3, 0.6), (0.7, 0.9), (0.6, 3.2), (1.1, 3.6), (1.1, 4.0), (0, 4.0)], loc=(s * 6.0, -D / 2 - 4.0, 0), key='castle_trim', segs=8)
        crystal(s * 6.0, -D / 2 - 4.0, 5.0, 3.0, 0.7, key='magic_purple' if s < 0 else 'magic')
    return finalize('magic_academy', smooth_angle=25)


ITEMS_CIVIC = [
    ('C16_cathedral', cathedral), ('C17_knights_hq', knights_hq), ('C18_guild_hall', guild_hall),
    ('C19_royal_library', royal_library), ('C20_magic_academy', magic_academy),
]


# ============================================================ squares, streets and canal
def stream(p0, p1, sag=-1.0, r=0.14):
    m = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, max(p0[2], p1[2]) + sag * -0.4)
    tube(nm('ws'), [p0, m, p1], r, 'water_fx', res=6, taper=[1.0, 0.9, 0.6])


def plaza_fountain():
    """C21 - grand plaza fountain: wide octagonal basin, three tiers, four urn spouts and a glowing star crown."""
    reset()
    R = 12.0
    lathe(nm('st'), [(0.0, 0.0), (R + 2.5, 0.0), (R + 2.5, 0.5), (R + 1.2, 0.5), (R + 1.2, 0.9), (0.0, 0.9)], loc=(0, 0, 0), key='ashlar_dark', segs=8)
    lathe(nm('bs'), [(0.0, 0.9), (R, 0.9), (R, 1.3), (R + 0.3, 1.5), (R + 0.3, 3.0), (R + 0.6, 3.3), (R + 0.6, 3.8), (R - 0.9, 3.8), (R - 0.9, 1.6), (0.0, 1.6)],
          key='castle_trim', segs=8)
    cyl(nm('pool'), R - 0.9, 0.05, loc=(0, 0, 3.2), key='water', verts=8, rot=(0, 0, 22.5))
    for i in range(8):
        a = math.radians(22.5 + 45 * i)
        fr = F(math.cos(a) * (R + 0.3) * 0.924, math.sin(a) * (R + 0.3) * 0.924, 0, math.degrees(a) + 90)
        lbox(fr, (4.8, 0.2, 1.1), 0, -0.05, 2.25, 'castle')
        cyl(nm('em'), 0.4, 0.2, loc=fr.p(0, -0.1, 2.25), key='gold', verts=10, rot=fr.r(90, 0, 0))
    lathe(nm('p1'), [(0.0, 1.6), (2.6, 1.6), (2.2, 2.6), (1.6, 3.4), (1.4, 7.0), (1.7, 7.4), (0.0, 7.4)], key='castle', segs=12)
    lathe(nm('b1'), [(0.0, 7.0), (1.4, 7.0), (4.6, 8.0), (5.6, 8.8), (5.8, 9.3), (5.3, 9.3), (4.4, 8.8), (0.0, 8.6)], key='castle_trim', segs=24)
    cyl(nm('w1'), 5.2, 0.05, loc=(0, 0, 9.1), key='water', verts=24)
    lathe(nm('p2'), [(0.0, 8.6), (1.0, 8.6), (0.8, 12.5), (1.0, 12.8), (0.0, 12.8)], key='castle', segs=12)
    lathe(nm('b2'), [(0.0, 12.5), (1.0, 12.5), (2.6, 13.2), (3.1, 13.8), (2.8, 13.8), (2.4, 13.5), (0.0, 13.4)], key='castle_trim', segs=20)
    cyl(nm('w2'), 2.7, 0.05, loc=(0, 0, 13.65), key='water', verts=20)
    lathe(nm('p3'), [(0.0, 13.4), (0.6, 13.4), (0.45, 15.6), (0.8, 16.0), (0.0, 16.2)], key='castle', segs=10)
    pts = star_pts(0.55, 1.4, 8)
    o = lslab(F(0, 0, 16.6, 0), [(px, 0.25, pz + 1.4) for px, pz in pts], (0, -0.5, 0), 'gold')
    ball(nm('so'), 0.6, loc=(0, 0, 18.0), key='magic', segs=12, rings=8)
    for i in range(12):
        a = 2 * math.pi * i / 12
        stream((math.cos(a) * 5.75, math.sin(a) * 5.75, 9.2), (math.cos(a) * 7.6, math.sin(a) * 7.6, 3.2), r=0.13)
    for i in range(8):
        a = 2 * math.pi * i / 8
        stream((math.cos(a) * 3.05, math.sin(a) * 3.05, 13.7), (math.cos(a) * 4.3, math.sin(a) * 4.3, 9.1), r=0.1)
    for i in range(4):
        a = math.radians(45 + 90 * i)
        x, y = math.cos(a) * (R - 3.0), math.sin(a) * (R - 3.0)
        lathe(nm('ub'), [(0, 1.6), (1.0, 1.6), (0.8, 3.0), (0.0, 3.0)], loc=(x, y, 0), key='castle', segs=10)
        lathe(nm('urn'), [(0, 3.0), (0.5, 3.0), (0.4, 3.4), (1.0, 4.2), (1.0, 4.9), (0.6, 5.3), (0.7, 5.6), (0.0, 5.5)], loc=(x, y, 0), key='castle_trim', segs=12)
        stream((x - math.cos(a) * 0.7, y - math.sin(a) * 0.7, 5.4), (x - math.cos(a) * 2.8, y - math.sin(a) * 2.8, 3.2), r=0.16)
        for k in range(3):
            torus(nm('rp'), 0.4 + k * 0.4, 0.04, loc=(x - math.cos(a) * 2.8, y - math.sin(a) * 2.8, 3.25), key='foam', segs=14, rsegs=3)
    return finalize('plaza_fountain', smooth_angle=35)


def knight_figure(Z, metal='bronze', accent='patina'):
    for s, fwd in ((-1, -0.5), (1, 0.4)):
        tube(nm('lg'), [(s * 0.55, 0, Z + 4.4), (s * 0.7, fwd * 0.6, Z + 2.4), (s * 0.8, fwd, Z + 0.6)], 0.42, metal, res=6, taper=[1.0, 0.85, 0.8])
        box(nm('ft'), (0.7, 1.4, 0.5), loc=(s * 0.8, fwd - 0.25, Z + 0.25), key=metal, bev=0.12)
        ball(nm('kn'), 0.36, loc=(s * 0.7, fwd * 0.6 - 0.15, Z + 2.4), key=accent, segs=8, rings=6)
    lathe(nm('tas'), [(0.0, Z + 3.7), (1.3, Z + 3.7), (1.05, Z + 4.9), (0.0, Z + 4.9)], key=metal, segs=12, sx=1.0, sy=0.8)
    lathe(nm('tor'), [(0.0, Z + 4.8), (1.0, Z + 4.8), (1.15, Z + 5.6), (1.35, Z + 6.6), (1.1, Z + 7.3), (0.4, Z + 7.5), (0.0, Z + 7.5)], key=metal, segs=14, sx=1.0, sy=0.72)
    torus(nm('belt'), 1.05, 0.12, loc=(0, 0, Z + 4.9), key=accent, segs=16, rsegs=4)
    for s in (-1, 1):
        ball(nm('pa'), 0.7, loc=(s * 1.3, 0, Z + 7.0), key=accent, segs=12, rings=8, scale=(1.0, 0.9, 0.7))
    tube(nm('ra'), [(1.35, 0, Z + 6.8), (1.9, -0.3, Z + 7.9), (1.8, -0.4, Z + 9.2)], 0.32, metal, res=6)
    ball(nm('rh'), 0.32, loc=(1.8, -0.4, Z + 9.35), key=metal, segs=8, rings=6)
    beam3((1.8, -0.4, Z + 9.6), (1.75, -0.45, Z + 15.0), 0.42, 0.1, 'steel')
    beam3((1.6, -0.42, Z + 9.6), (2.0, -0.42, Z + 9.6), 1.6, 0.25, 'gold', roll=90)
    ball(nm('pm'), 0.2, loc=(1.8, -0.4, Z + 8.9), key='gold', segs=8, rings=6)
    tube(nm('la'), [(-1.35, 0, Z + 6.8), (-1.75, -0.5, Z + 5.9), (-1.3, -1.0, Z + 5.5)], 0.32, metal, res=6)
    sh = [(-1.0, 0, 1.4), (1.0, 0, 1.4), (1.0, 0, 0.0), (0.0, 0, -1.6), (-1.0, 0, 0.0)]
    lslab(F(-1.4, -1.25, Z + 5.6, 15), sh, (0, -0.25, 0), accent)
    lslab(F(-1.4, -1.5, Z + 5.6, 15), [(-0.15, 0, 1.1), (0.15, 0, 1.1), (0.15, 0, -1.2), (-0.15, 0, -1.2)], (0, -0.06, 0), 'gold')
    lslab(F(-1.4, -1.5, Z + 5.6, 15), [(-0.7, 0, 0.6), (0.7, 0, 0.6), (0.7, 0, 0.3), (-0.7, 0, 0.3)], (0, -0.06, 0), 'gold')
    cyl(nm('nk'), 0.35, 0.5, loc=(0, 0, Z + 7.4), key=metal, verts=10)
    lathe(nm('hm'), [(0.0, Z + 7.8), (0.62, Z + 7.8), (0.7, Z + 8.4), (0.62, Z + 8.9), (0.3, Z + 9.2), (0.0, Z + 9.25)], key=metal, segs=14)
    box(nm('vs'), (0.9, 0.2, 0.12), loc=(0, -0.65, Z + 8.45), key='iron_dark')
    tube(nm('pl'), [(0, -0.1, Z + 9.2), (0, 0.5, Z + 9.7), (0, 1.3, Z + 9.3), (0, 1.8, Z + 8.5)], 0.22, accent, res=6, taper=[1, 1.2, 0.8, 0.3])
    from props import cloth
    cloth(nm('cape'), 2.9, 5.0, (0, 0.85, Z + 7.3), accent, waves=1.6, amp=0.28, seed=4)


def plinth(Z=5.6, w=5.6, plaque=True):
    box(nm('pb'), (w + 2.0, w + 2.0, 1.0), loc=(0, 0, 0.5), key='ashlar_dark', bev=0.08)
    box(nm('pb2'), (w + 1.0, w + 1.0, 0.6), loc=(0, 0, 1.3), key='castle', bev=0.06)
    box(nm('pd'), (w, w, Z - 2.6), loc=(0, 0, 1.6 + (Z - 2.6) / 2), key='marble')
    box(nm('pc'), (w + 0.8, w + 0.8, 0.5), loc=(0, 0, Z - 0.75), key='castle', bev=0.06)
    box(nm('pc2'), (w + 0.4, w + 0.4, 0.5), loc=(0, 0, Z - 0.25), key='marble', bev=0.04)
    if plaque:
        lbox(F(0, -w / 2, 0, 0), (2.8, 0.15, 1.4), 0, -0.07, (Z + 1.6) / 2, 'gold', bev=0.04)
        for k in range(3):
            lbox(F(0, -w / 2, 0, 0), (2.0 - k * 0.4, 0.06, 0.12), 0, -0.17, (Z + 1.6) / 2 + 0.35 - k * 0.35, 'bronze')


def knight_statue():
    """C22 - hero knight statue (original): raised sword, kite shield, plumed helm and cape, on a marble plinth."""
    reset()
    plinth(5.6)
    knight_figure(5.6)
    return finalize('knight_statue', smooth_angle=40)


def obelisk():
    """C23 - obelisk with stepped base, carved bands and a gold cap."""
    reset()
    for k in range(3):
        box(nm('ob'), (8.0 - k * 1.6, 8.0 - k * 1.6, 0.8), loc=(0, 0, 0.4 + k * 0.8), key='ashlar_dark' if k % 2 == 0 else 'castle', bev=0.06)
    box(nm('od'), (3.8, 3.8, 3.0), loc=(0, 0, 3.9), key='marble', bev=0.05)
    box(nm('odc'), (4.3, 4.3, 0.4), loc=(0, 0, 5.6), key='castle', bev=0.04)
    lathe(nm('sh'), [(0.0, 5.8), (2.2, 5.8), (1.3, 30.0), (0.0, 30.0)], key='castle_trim', segs=4)
    lathe(nm('pyr'), [(0.0, 30.0), (1.36, 30.0), (0.0, 32.4)], key='gold', segs=4)
    for zz in (9.0, 16.0, 23.0):
        rr = 2.2 - (zz - 5.8) / 24.2 * 0.9
        lathe(nm('bd'), [(0.0, zz), (rr + 0.12, zz), (rr + 0.12, zz + 0.5), (0.0, zz + 0.5)], key='gold', segs=4)
    for k in range(4):
        fr = faces(0, 0, 3.8, 3.8)[('front', 'back', 'left', 'right')[k]]
        cyl(nm('oe'), 0.9, 0.12, loc=fr.p(0, 0, 3.9), key='gold', verts=12, rot=fr.r(90, 0, 0))
    return finalize('obelisk', smooth_angle=20)


def street_archway():
    """C24 - ornate triumphal archway spanning a street (14-stud opening)."""
    reset()
    f = F()
    W, D, H = 26.0, 6.0, 24.0
    arch_block(f, -W / 2, W / 2, -D / 2, D / 2, 0, H, 0, 11.0, 7.0, 'castle')
    for s in (-1, 1):
        fr = f.sub(0, s * D / 2, 0, 0 if s < 0 else 180)
        tube(nm('av'), arc_pts(fr, 0, 11.0, 7.5, y=-0.25, n=21), 0.55, 'castle_trim', res=4)
        lbox(fr, (1.4, 0.8, 2.2), 0, -0.4, 18.6, 'gold', bev=0.06)
        for x in (-11.0, -8.6, 8.6, 11.0):
            column_c(x, fr.p(x, -0.9, 0)[1] if False else (s * (D / 2 + 0.9)), 1.6, 15.4, 0.6, key='castle_trim', base='castle')
            box(nm('cpl'), (2.0, 2.4, 1.6), loc=(x, s * (D / 2 + 0.6), 0.8), key='ashlar_dark', bev=0.06)
        lbox(fr, (W + 1.0, 1.4, 1.2), 0, -0.5, 17.6, 'castle_trim')
        lbox(fr, (W - 6.0, 0.4, 3.0), 0, -0.2, 20.4, 'marble')
        for k in range(5):
            lbox(fr, (2.0, 0.1, 0.9), -8.0 + k * 4.0, -0.42, 20.4, 'gold')
        for x in (-9.8, 9.8):
            window(fr, x, 6.0, w=1.8, h=4.0, arch=True, frame='castle_trim', sill='castle_trim', panes=False)
    box(nm('at'), (W + 1.2, D + 1.6, 1.0), loc=(0, 0, H + 0.5), key='castle_trim', bev=0.06)
    for s in (-1, 1):
        lathe(nm('au'), [(0, 0), (1.0, 0), (0.6, 0.6), (1.1, 1.8), (0.9, 2.6), (0, 2.8)], loc=(s * 11.0, 0, H + 1.0), key='castle_trim', segs=12)
        from props import cloth
        cyl(nm('fp'), 0.15, 9.0, loc=(s * 7.0, 0, H + 1.0), key='iron', verts=8)
        ball(nm('fpb'), 0.3, loc=(s * 7.0, 0, H + 10.1), key='gold', segs=8, rings=6)
        cloth(nm('af'), 4.0, 2.6, (s * 7.0 + 2.1, 0, H + 9.6), 'fabric_red', waves=1.0, amp=0.25, seed=s + 2)
    lslab(F(0, -D / 2 - 0.8, 0, 0), [(-2.2, 0, H + 1.0), (2.2, 0, H + 1.0), (2.2, 0, H + 3.0), (0, 0, H + 4.6), (-2.2, 0, H + 3.0)], (0, D + 1.6, 0), 'castle_trim')
    for s in (-1, 1):
        cyl(nm('cr'), 1.0, 0.2, loc=(0, s * (D / 2 + 0.8), H + 2.6), key='gold', verts=14, rot=(90, 0, 0))
    return finalize('street_archway', smooth_angle=25)


def window_flower_box():
    """C25 - window flower box on iron brackets (6 wide), mounts on any wall."""
    reset()
    f = F(0, 0.4, 0, 0)
    flower_box(f, 0, 1.6, 6.0, ('fl_red', 'fl_pink', 'fl_white', 'fl_yellow'), seed=25)
    for x in (-2.2, 2.2):
        lbox(f, (0.12, 0.12, 1.2), x, 0.0, 0.8, 'iron')
        lbeam(f, (x, 0.0, 0.4), (x, -0.9, 1.25), 0.1, 'iron')
        lbox(f, (0.12, 1.0, 0.1), x, -0.5, 1.25, 'iron')
    rnd = random.Random(25)
    for i in range(6):
        x = -2.5 + i
        tube(nm('vine'), [f.p(x, -0.9, 1.3), f.p(x + rnd.uniform(-0.2, 0.2), -1.0, 0.95), f.p(x + rnd.uniform(-0.3, 0.3), -0.95, rnd.uniform(0.45, 0.7))],
             0.05, 'leaf', res=4, taper=[1, 0.8, 0.4])
        ball(nm('vl'), 0.2, loc=f.p(x + 0.1, -1.0, 0.85), key='leaf_dark', segs=6, rings=4, scale=(1, 0.5, 1))
    return finalize('window_flower_box', smooth_angle=30)


def vendor_cart():
    """C26 - street vendor cart: two wheels, striped canopy, trays of goods and a hand bell."""
    reset()
    from props import wheel
    rnd = random.Random(26)
    box(nm('bed'), (6.0, 3.2, 0.3), loc=(0, 0, 2.6), key='wood_light')
    for s in (-1, 1):
        box(nm('sd'), (6.0, 0.2, 1.0), loc=(0, s * 1.5, 3.2), key='wood')
        box(nm('en'), (0.2, 3.2, 1.0), loc=(s * 2.9, 0, 3.2), key='wood')
        wheel(nm('wh'), 1.4, (0.8, s * 1.85, 1.4), axis='Y', spokes=8)
    box(nm('ax'), (0.3, 4.0, 0.3), loc=(0.8, 0, 1.4), key='wood_dark')
    for s in (-1, 1):
        tube(nm('hd'), [(-3.0, s * 1.2, 2.6), (-5.5, s * 1.2, 2.1), (-6.5, s * 1.1, 2.2)], 0.12, 'wood_dark', res=4)
        box(nm('lg'), (0.25, 0.25, 2.6), loc=(-2.6, s * 1.2, 1.3), key='wood_dark')
        for x in (-2.8, 2.8):
            cyl(nm('cp'), 0.1, 3.4, loc=(x, s * 1.45, 3.7), key='wood_dark', verts=6)
    for i in range(8):
        k = 'fabric_red' if i % 2 == 0 else 'fabric_cream'
        x0 = -3.3 + i * 0.825
        lslab(F(), [(x0, -2.0, 7.0), (x0 + 0.825, -2.0, 7.0), (x0 + 0.825, 0, 7.8), (x0, 0, 7.8)], (0, 0, 0.1), k)
        lslab(F(), [(x0, 2.0, 7.0), (x0 + 0.825, 2.0, 7.0), (x0 + 0.825, 0, 7.8), (x0, 0, 7.8)], (0, 0, 0.1), k)
        lslab(F(), [(x0, -2.0, 7.0), (x0 + 0.825, -2.0, 7.0), (x0 + 0.4125, -2.0, 6.4)], (0, 0.08, 0), k)
    for j, goods in enumerate(('fruit', 'fl_orange', 'leaf_light', 'fl_yellow')):
        x = -2.1 + j * 1.4
        box(nm('tray'), (1.3, 2.6, 0.3), loc=(x, 0, 3.6), key='wood_dark')
        for q in range(8):
            ball(nm('gd'), 0.22, loc=(x + rnd.uniform(-0.4, 0.4), rnd.uniform(-1.0, 1.0), 3.95), key=goods, segs=7, rings=5)
    lathe(nm('bell'), [(0, 0), (0.3, 0), (0.22, 0.35), (0.1, 0.45), (0, 0.5)], loc=(2.8, -1.45, 6.3), key='brass', segs=10, rot=(180, 0, 0))
    return finalize('vendor_cart', smooth_angle=30)


CW_H = 9.0


def canal_wall():
    """C27 - canal quay wall, 24 long: water side faces -Y, top at street level (z=9 above canal bed)."""
    reset()
    f = F()
    L = 24.0
    box(nm('cw'), (L, 4.0, CW_H), loc=(0, 2.0, CW_H / 2), key='ashlar')
    stone_face(F(0, 0, 0, 0), -L / 2, L / 2, 0.3, CW_H - 0.6, 70, 27, keys=('ashlar', 'ashlar_dark', 'stone'))
    o = box(nm('wl'), (L, 0.3, 2.6), loc=(0, -0.1, 1.3), key='stone_dark', bev=0.05)
    top_paint(o, 'moss', 0.3, 27)
    rnd = random.Random(270)
    for i in range(10):
        lbox(F(), (rnd.uniform(0.8, 2.0), 0.12, rnd.uniform(0.2, 0.5)), rnd.uniform(-L / 2 + 1, L / 2 - 1), -0.3, rnd.uniform(2.4, 2.8), 'moss')
    box(nm('cp'), (L, 2.0, 0.6), loc=(0, 0.6, CW_H + 0.3), key='castle_trim', bev=0.08)
    for x in (-6.0, 6.0):
        torus(nm('mr'), 0.5, 0.09, loc=(x, -0.35, CW_H - 2.0), key='iron', segs=14, rsegs=5, rot=(90, 0, 0))
        box(nm('mrp'), (0.5, 0.2, 0.5), loc=(x, -0.1, CW_H - 1.5), key='iron')
        cyl(nm('bol'), 0.45, 1.3, loc=(x + 2.0, 0.8, CW_H + 0.6), key='iron_dark', verts=10, r2=0.35)
        torus(nm('bolr'), 0.5, 0.1, loc=(x + 2.0, 0.8, CW_H + 1.7), key='iron_dark', segs=10, rsegs=4)
    for x in (-10.0, 0.0, 10.0):
        lathe(nm('dr'), [(0.0, 0.0), (0.6, 0.0), (0.6, 0.6), (0.0, 0.6)], loc=(x, 0.1, CW_H - 3.6), key='iron_dark', segs=10, rot=(90, 0, 0))
    railing(F(0, 0.1, CW_H + 0.6, 0), -L / 2, L / 2, 0.0, y=0.0, h=2.2, key='iron', step=1.0)
    for x in (-L / 2 + 0.2, 0.0, L / 2 - 0.2):
        box(nm('rp'), (0.35, 0.35, 2.6), loc=(x, 0.1, CW_H + 1.9), key='iron')
        ball(nm('rpb'), 0.28, loc=(x, 0.1, CW_H + 3.3), key='iron', segs=8, rings=6)
    return finalize('canal_wall', smooth_angle=20)


def canal_bridge():
    """C28 - small stone canal bridge: 18-stud arch span, balustrades and lamp posts on the ends."""
    reset()
    span, Wd = 18.0, 10.0
    f = F(0, 0, 0, 90)
    pts = [(-span / 2 - 6, -Wd / 2, CW_H - 0.5)]
    for i in range(17):
        a = math.pi - math.pi * i / 16
        pts.append((math.cos(a) * span / 2, -Wd / 2, 2.0 + math.sin(a) * (span / 2) * 0.62))
    pts += [(span / 2 + 6, -Wd / 2, CW_H - 0.5), (span / 2 + 6, -Wd / 2, CW_H + 0.4), (0, -Wd / 2, CW_H + 1.2), (-span / 2 - 6, -Wd / 2, CW_H + 0.4)]
    lslab(f, pts, (0, Wd, 0), 'ashlar')
    for s in (-1, 1):
        fr = f.sub(0, s * Wd / 2, 0, 0 if s < 0 else 180)
        ar = [fr.p(math.cos(math.pi - math.pi * i / 16) * (span / 2 + 0.4), -0.25, 2.0 + math.sin(math.pi - math.pi * i / 16) * (span / 2 * 0.62 + 0.4)) for i in range(17)]
        tube(nm('vo'), ar, 0.45, 'castle_trim', res=4)
        lbox(fr, (1.0, 0.6, 1.4), 0, -0.3, 2.0 + span / 2 * 0.62 + 0.9, 'castle_trim')
        for x0 in (-span / 2 - 6, 0):
            x1 = x0 + span / 2 + 6
            zc = lambda x: CW_H + 1.2 - abs(x) / (span / 2 + 6) * 0.8
            lbeam(fr, (x0, -0.45, zc(x0) + 2.4), (x1, -0.45, zc(x1) + 2.4), 0.8, 'castle_trim', 0.4)
            lbeam(fr, (x0, -0.45, zc(x0) + 0.2), (x1, -0.45, zc(x1) + 0.2), 0.8, 'castle', 0.4)
            n = 9
            for i in range(n):
                x = x0 + (x1 - x0) * (i + 0.5) / n
                lathe(nm('bal'), [(0, 0), (0.3, 0), (0.22, 0.4), (0.38, 1.1), (0.2, 1.7), (0.3, 2.0), (0, 2.0)], loc=fr.p(x, -0.45, zc(x) + 0.3), key='castle_trim', segs=8)
        for x in (-span / 2 - 6, span / 2 + 6):
            box(nm('np'), (1.4, 1.4, 3.4), loc=fr.p(x, -0.45, CW_H + 1.6), key='castle', bev=0.06)
    for s in (-1, 1):
        for e in (-1, 1):
            x, y = s * (Wd / 2 - 0.45), e * (span / 2 + 6)
            cyl(nm('lp'), 0.2, 6.0, loc=(x, y, CW_H + 3.3), key='iron', verts=8)
            lathe(nm('lh'), [(0, 0), (0.45, 0), (0.55, 0.2), (0.0, 0.2)], loc=(x, y, CW_H + 9.3), key='iron', segs=6)
            lathe(nm('lg'), [(0, 0.2), (0.45, 0.2), (0.5, 1.2), (0, 1.2)], loc=(x, y, CW_H + 9.3), key='glass_lit', segs=6)
            lathe(nm('lc'), [(0, 1.2), (0.65, 1.2), (0.0, 1.9)], loc=(x, y, CW_H + 9.3), key='iron', segs=6)
    rnd = random.Random(28)
    for i in range(14):
        x = rnd.uniform(-Wd / 2 + 1, Wd / 2 - 1)
        y = rnd.uniform(-span / 2 - 5, span / 2 + 5)
        box(nm('cb'), (rnd.uniform(1.2, 2), rnd.uniform(1.2, 2), 0.1), loc=(x, y, CW_H + 1.2 - abs(y) / (span / 2 + 6) * 0.8 + 0.02), key=rnd.choice(['cob_a', 'cob_b', 'cob_c']),
            rot=(0, 0, rnd.uniform(0, 90)))
    return finalize('canal_bridge', smooth_angle=25)


def canal_stairs():
    """C29 - stone stairs from street level down to the canal water, with side wall and iron handrail."""
    reset()
    n, rise, run, wd = 14, CW_H / 14, 1.4, 5.0
    box(nm('bk'), (n * run + 2, 4.0, CW_H), loc=(-(n * run) / 2 + 1.0, 4.0 + 2.0, CW_H / 2), key='ashlar')
    for i in range(n):
        z = CW_H - rise * (i + 1)
        x = -i * run
        box(nm('stp'), (run + 0.1, wd, z + rise), loc=(x, 1.5, (z + rise) / 2), key='ashlar' if i % 2 else 'castle', bev=0.05)
        box(nm('nos'), (0.3, wd + 0.1, 0.15), loc=(x - run / 2 + 0.1, 1.5, z + rise - 0.05), key='castle_trim')
    box(nm('ld'), (4.0, wd, 0.5), loc=(-n * run - 1.3, 1.5, 0.25), key='ashlar_dark')
    for i in range(n):
        x = -i * run
        z = CW_H - rise * (i + 1)
        lbox(F(), (run + 0.1, 0.6, 0.5), x, -1.25, z + rise + 0.25, 'castle_trim')
    tube(nm('hr'), [(1.0, -1.25, CW_H + 2.6), (-n * run * 0.5, -1.25, CW_H * 0.5 + 2.6), (-n * run, -1.25, 2.6)], 0.1, 'iron', res=4, ures=1)
    for i in range(0, n + 1, 3):
        x = -i * run
        z = CW_H - rise * i
        cyl(nm('hp'), 0.08, 2.2, loc=(x, -1.25, z + 0.4), key='iron', verts=6)
    box(nm('pst'), (0.6, 0.6, 4.0), loc=(-n * run - 2.6, 3.8, 2.0), key='wood_dark')
    torus(nm('mr'), 0.4, 0.08, loc=(-n * run - 2.6, 3.45, 3.0), key='iron', segs=12, rsegs=4, rot=(90, 0, 0))
    o = box(nm('mw'), (n * run + 6, 4.4, 1.6), loc=(-(n * run) / 2 - 1.0, 1.5, 0.8), key='ashlar_dark')
    return finalize('canal_stairs', smooth_angle=20)


def plaza_paving():
    """C30 - patterned grand-plaza paving tile, 32 x 32: compass rose of light and dark stone rings."""
    reset()
    S = 32.0
    box(nm('base'), (S, S, 0.3), loc=(0, 0, 0.15), key='grout')
    rnd = random.Random(30)
    n = 16
    step = S / n
    for i in range(n):
        for j in range(n):
            x, y = -S / 2 + step * (i + 0.5), -S / 2 + step * (j + 0.5)
            if math.hypot(x, y) < 12.3:
                continue
            box(nm('fl'), (step - 0.12, step - 0.12, 0.2), loc=(x, y, 0.4), key=rnd.choice(['cob_a', 'cob_c', 'stone_light']), bev=0.03)
    for k, (r0, r1, key) in enumerate(((10.5, 12.2, 'ashlar_dark'), (8.2, 10.4, 'castle_trim'), (2.4, 8.1, 'ashlar'))):
        segs = 24 + k * 8
        for i in range(segs):
            a0, a1 = 2 * math.pi * i / segs, 2 * math.pi * (i + 1) / segs
            g = 0.03
            pts = [(math.cos(a0 + g / r0 * 3) * r0, math.sin(a0 + g / r0 * 3) * r0, 0.3), (math.cos(a0 + g / r1 * 3) * r1, math.sin(a0 + g / r1 * 3) * r1, 0.3),
                   (math.cos(a1 - g / r1 * 3) * r1, math.sin(a1 - g / r1 * 3) * r1, 0.3), (math.cos(a1 - g / r0 * 3) * r0, math.sin(a1 - g / r0 * 3) * r0, 0.3)]
            kk = key if k != 2 else ('ashlar' if i % 2 else 'stone_light')
            slab(pts, (0, 0, 0.22), kk)
    for i in range(8):
        a = math.pi / 4 * i
        L = 9.6 if i % 2 == 0 else 6.4
        pts = [(math.cos(a) * L, math.sin(a) * L, 0.55), (math.cos(a + 0.5) * 1.6, math.sin(a + 0.5) * 1.6, 0.55), (math.cos(a - 0.5) * 1.6, math.sin(a - 0.5) * 1.6, 0.55)]
        slab(pts, (0, 0, 0.06), 'gold' if i % 2 == 0 else 'marble')
    cyl(nm('ctr'), 2.0, 0.3, loc=(0, 0, 0.4), key='marble', verts=24)
    cyl(nm('ctr2'), 1.0, 0.1, loc=(0, 0, 0.7), key='fabric_red', verts=16)
    return finalize('plaza_paving', smooth_angle=20)


def bunting():
    """C31 - bunting: 40-stud sagging rope of triangular flags, eye hooks at both ends (hang between buildings)."""
    reset()
    L, sag, z = 40.0, 4.0, 0.0
    cols = ['fabric_red', 'fl_yellow', 'fabric_blue', 'fabric_cream', 'fabric_green', 'fl_pink']
    pts = []
    for i in range(21):
        t = i / 20
        x = -L / 2 + L * t
        pts.append((x, 0, z + sag * (4 * (t - 0.5) ** 2) - sag + sag))
    tube(nm('rope'), pts, 0.06, 'rope', res=4)
    n = 26
    for i in range(n):
        t = (i + 0.5) / n
        x = -L / 2 + L * t
        zz = z + sag * (4 * (t - 0.5) ** 2)
        tw = L / n * 0.42
        slab([(x - tw, 0, zz), (x + tw, 0, zz), (x + 0.1 * math.sin(i), 0, zz - 1.7)], (0, 0.06, 0), cols[i % len(cols)])
    for s in (-1, 1):
        box(nm('pl'), (0.2, 0.6, 0.6), loc=(s * (L / 2 + 0.1), 0, sag), key='iron')
        torus(nm('hk'), 0.2, 0.05, loc=(s * L / 2, 0, sag), key='iron', segs=10, rsegs=4, rot=(90, 0, 0))
    return finalize('bunting', smooth_angle=30)


ITEMS_SQUARES = [
    ('C21_plaza_fountain', plaza_fountain), ('C22_knight_statue', knight_statue), ('C23_obelisk', obelisk),
    ('C24_street_archway', street_archway), ('C25_window_flower_box', window_flower_box), ('C26_vendor_cart', vendor_cart),
    ('C27_canal_wall', canal_wall), ('C28_canal_bridge', canal_bridge), ('C29_canal_stairs', canal_stairs),
    ('C30_plaza_paving', plaza_paving), ('C31_bunting', bunting),
]
