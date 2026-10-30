"""Worker we2 - B03 throne hall + B06 market stalls, category v4_castle.
Ported from predecessor we's design (which never ran its B03/B06 after the B04 freeze),
with we2_ palette keys and the correct marker call marker('mk_door', ...).
"""
import math, random
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, scroll
from arch import (F, faces, nm, lbox, lbeam, lslab, beam3, half_disc, column_c, cone_roof, arc_pts)
import v4util

P = kitlib.PAL
P['we2_ashlar']     = ((206, 198, 180), 'Limestone',  0.00, 0.82, 0)
P['we2_trim']       = ((230, 224, 210), 'Marble',     0.00, 0.48, 0)
P['we2_plinth']     = ((132, 128, 120), 'Cobblestone', 0.00, 0.90, 0)
P['we2_floor_a']    = ((178, 170, 154), 'Marble',     0.00, 0.55, 0)
P['we2_floor_b']    = ((96, 92, 86),    'Slate',      0.00, 0.80, 0)
P['we2_carpet']     = ((140, 28, 36),   'Fabric',     0.00, 1.00, 0)
P['we2_carpet_t']   = ((198, 158, 72),  'Fabric',     0.00, 0.95, 0)
P['we2_banner_r']   = ((150, 36, 42),   'Fabric',     0.00, 0.95, 0)
P['we2_banner_b']   = ((44, 66, 128),   'Fabric',     0.00, 0.95, 0)
P['we2_banner_g']   = ((196, 158, 72),  'Fabric',     0.00, 0.95, 0)
P['we2_gold']       = ((214, 172, 72),  'Metal',      1.00, 0.25, 0)
P['we2_bronze']     = ((120, 86, 52),   'Metal',      0.90, 0.40, 0)
P['we2_iron']       = ((44, 42, 40),    'Metal',      0.85, 0.48, 0)
P['we2_wood']       = ((122, 84, 52),   'WoodPlanks', 0.00, 0.80, 0)
P['we2_wood_l']     = ((166, 126, 84),  'WoodPlanks', 0.00, 0.80, 0)
P['we2_timber']     = ((78, 54, 37),    'Wood',       0.00, 0.85, 0)
P['we2_hay']        = ((190, 160, 92),  'Fabric',     0.00, 1.00, 0)
P['we2_wax']        = ((238, 228, 200), 'SmoothPlastic', 0.00, 0.50, 0)
P['we2_rope']       = ((176, 150, 104), 'Fabric',     0.00, 1.00, 0)
P['we2_stain_r']    = ((190, 48, 56),   'Glass',      0.00, 0.10, 0.5)
P['we2_stain_b']    = ((56, 92, 190),   'Glass',      0.00, 0.10, 0.5)
P['we2_stain_y']    = ((232, 186, 60),  'Glass',      0.00, 0.10, 0.5)
P['we2_stain_g']    = ((60, 150, 90),   'Glass',      0.00, 0.10, 0.5)
P['we2_flame']      = ((255, 150, 40),  'Neon',       0.00, 0.50, 2.0)
P['we2_flame_c']    = ((255, 214, 120), 'Neon',       0.00, 0.50, 2.0)
P['we2_canopy_r']   = ((164, 54, 48),   'Fabric',     0.00, 0.95, 0)
P['we2_canopy_cr']  = ((230, 218, 188), 'Fabric',     0.00, 0.95, 0)
P['we2_canopy_bl']  = ((52, 86, 140),   'Fabric',     0.00, 0.95, 0)
P['we2_canopy_gr']  = ((60, 110, 72),   'Fabric',     0.00, 0.95, 0)
P['we2_canopy_gd']  = ((200, 160, 72),  'Fabric',     0.00, 0.95, 0)
P['we2_cloth_a']    = ((150, 46, 54),   'Fabric',     0.00, 0.95, 0)
P['we2_cloth_b']    = ((48, 78, 132),   'Fabric',     0.00, 0.95, 0)
P['we2_cloth_c']    = ((60, 108, 78),   'Fabric',     0.00, 0.95, 0)
P['we2_cloth_d']    = ((196, 170, 90),  'Fabric',     0.00, 0.95, 0)
P['we2_fruit_a']    = ((186, 36, 34),   'SmoothPlastic', 0.00, 0.45, 0)
P['we2_fruit_b']    = ((232, 160, 42),  'SmoothPlastic', 0.00, 0.50, 0)
P['we2_fruit_c']    = ((120, 172, 58),  'SmoothPlastic', 0.00, 0.55, 0)
P['we2_fruit_d']    = ((150, 70, 160),  'SmoothPlastic', 0.00, 0.50, 0)
P['we2_potion_r']   = ((198, 40, 70),   'Glass',      0.00, 0.10, 0.4)
P['we2_potion_b']   = ((60, 110, 220),  'Glass',      0.00, 0.10, 0.4)
P['we2_potion_g']   = ((80, 200, 110),  'Glass',      0.00, 0.10, 0.4)
P['we2_potion_p']   = ((170, 90, 220),  'Glass',      0.00, 0.10, 0.4)
P['we2_glass_lit']  = ((246, 196, 110), 'Glass',      0.00, 0.20, 0.45)


def _mdoor(f, x, z=0.0):
    v4util.marker('mk_door', f.p(x, -0.1, z + 0.1))


def _flame(loc, h=1.1, r=0.4, seed=0):
    rnd = random.Random(seed)
    prof = [(0.0, 0.0), (r * 0.7, h * 0.08), (r, h * 0.24), (r * 0.85, h * 0.46), (r * 0.5, h * 0.7), (r * 0.2, h * 0.9), (0.0, h)]
    o = lathe(nm('fl'), prof, loc=loc, key='we2_flame', segs=8)
    o.rotation_euler.z = rnd.uniform(0, 6.28)
    lathe(nm('flc'), [(0.0, 0.0), (r * 0.5, h * 0.14), (r * 0.42, h * 0.4), (0.0, h * 0.58)],
          loc=(loc[0], loc[1], loc[2] + h * 0.03), key='we2_flame_c', segs=8)


def _brazier(x, y, h=4.2, r=1.5):
    lathe(nm('bz'), [(0.0, 0.0), (0.5, 0.0), (0.35, 0.3), (0.3, h - 1.6), (r, h - 0.3), (r, h), (r - 0.25, h), (r - 0.25, h - 0.25), (0.35, h - 1.4), (0.0, h - 1.4)],
          loc=(x, y, 0), key='we2_iron', segs=14)
    cyl(nm('coal'), r - 0.35, 0.2, loc=(x, y, h - 0.4), key='we2_iron', verts=14)
    for i in range(7):
        a = 2 * math.pi * i / 7
        _flame((x + math.cos(a) * (r - 0.6) * 0.5, y + math.sin(a) * (r - 0.6) * 0.5, h - 0.3), h=1.2 + 0.4 * (i % 2), r=0.4, seed=i)
    _flame((x, y, h - 0.2), h=1.8, r=0.5, seed=9)


def _wall_banner(f, x, z, w=3.4, h=10.0, key='we2_banner_r', seed=0):
    lbox(f, (w + 0.6, 0.35, 0.35), x, -0.4, z + 0.1, 'we2_bronze')
    for s in (-1, 1):
        ball(nm('fin'), 0.26, loc=f.p(x + s * (w / 2 + 0.3), -0.4, z + 0.1), key='we2_gold', segs=8, rings=6)
    lslab(f, [(x - w / 2, 0.0, z), (x + w / 2, 0.0, z), (x + w / 2, -0.12, z - h + 1.4), (x + w * 0.18, -0.12, z - h + 3.2),
              (x, -0.12, z - h), (x - w * 0.18, -0.12, z - h + 3.2), (x - w / 2, -0.12, z - h + 1.4)], (0, -0.14, 0), key)
    cyl(nm('em'), w * 0.26, 0.08, loc=f.p(x, -0.2, z - h * 0.42), key='we2_gold', verts=16, rot=f.r(90, 0, 0))
    cyl(nm('emi'), w * 0.14, 0.06, loc=f.p(x, -0.26, z - h * 0.42), key=key, verts=12, rot=f.r(90, 0, 0))


def _tiled_floor(W, D, z=0.0, tile=4.0):
    nx = max(2, int(W / tile)); ny = max(2, int(D / tile))
    sx, sy = W / nx, D / ny
    for i in range(nx):
        for j in range(ny):
            k = 'we2_floor_a' if (i + j) % 2 == 0 else 'we2_floor_b'
            box(nm('ft'), (sx - 0.12, sy - 0.12, 0.3), loc=(-W / 2 + sx * (i + 0.5), -D / 2 + sy * (j + 0.5), z + 0.15), key=k, bev=0.03)
    box(nm('fb'), (W + 0.6, D + 0.6, 0.25), loc=(0, 0, z - 0.1), key='we2_trim')


def _carpet(x0, x1, y, w=7.0, z=0.32):
    L = x1 - x0
    box(nm('cp'), (L, w, 0.14), loc=((x0 + x1) / 2, y, z), key='we2_carpet')
    for s in (-1, 1):
        box(nm('cpt'), (L, 0.5, 0.16), loc=((x0 + x1) / 2, y + s * (w / 2 - 0.3), z + 0.01), key='we2_carpet_t')


def _chandelier(x, y, zc, drop=6.0, r=2.4, candles=8):
    tube(nm('ch'), [(x, y, zc), (x, y, zc - drop)], 0.08, 'we2_iron', res=4)
    torus(nm('ring'), r, 0.14, loc=(x, y, zc - drop), key='we2_iron', segs=20, rsegs=5)
    for i in range(candles):
        a = 2 * math.pi * i / candles
        cx, cy = x + math.cos(a) * r, y + math.sin(a) * r
        tube(nm('arm'), [(x, y, zc - drop + 0.4), (cx, cy, zc - drop + 0.1)], 0.07, 'we2_iron', res=4)
        cyl(nm('cd'), 0.13, 0.7, loc=(cx, cy, zc - drop + 0.2), key='we2_wax', verts=8)
        _flame((cx, cy, zc - drop + 0.9), h=0.7, r=0.22, seed=i)


# ===================================================== B03_01 throne hall
def throne_hall():
    """Interior kit, no outer walls/roof. ~48x80x30: tiled two-stone floor, long red carpet,
    10 pillars with capitals, banners between, tall stained-glass window bays both long sides,
    a dais with wide steps, a throne under a canopy, two braziers, chandeliers on chains."""
    reset()
    W, D, H = 48.0, 80.0, 30.0
    _tiled_floor(W, D, 0.0, tile=4.0)
    _carpet(-D / 2 + 3.0, D / 2 - 16.0, 0.0, w=7.0)
    px, zcap = W / 2 - 5.0, H - 3.0
    pillar_ys = [-D / 2 + 10.0 + i * (D - 28.0) / 4 for i in range(5)]
    for s in (-1, 1):
        for py in pillar_ys:
            column_c(s * px, py, 0.0, zcap, 1.5, key='we2_ashlar', base='we2_trim')
            box(nm('pb'), (4.2, 4.2, 1.0), loc=(s * px, py, 0.5), key='we2_plinth', bev=0.08)
        for j in range(len(pillar_ys) - 1):
            my = (pillar_ys[j] + pillar_ys[j + 1]) / 2
            fr = F(s * (W / 2 - 0.6), my, zcap - 1.0, -90 if s < 0 else 90)
            key = ['we2_banner_r', 'we2_banner_b', 'we2_banner_g', 'we2_banner_r'][j % 4]
            _wall_banner(fr, 0, 0, w=3.4, h=10.0, key=key, seed=j + s)
        lbeam(F(), (s * px, pillar_ys[0], zcap), (s * px, pillar_ys[-1], zcap), 1.0, 'we2_trim')
    # stained-glass window bays both long sides, between pillars
    cols = ['we2_stain_b', 'we2_stain_r', 'we2_stain_y', 'we2_stain_g']
    for s in (-1, 1):
        for j in range(len(pillar_ys) - 1):
            my = (pillar_ys[j] + pillar_ys[j + 1]) / 2
            fr = F(s * (W / 2 - 0.4), my, 0, -90 if s < 0 else 90)
            w2, zb, h2 = 5.0, 6.0, 15.0
            zs = zb + h2 - w2 * 0.6
            lbox(fr, (w2, 0.3, zs - zb), 0, -0.1, (zb + zs) / 2, cols[j % 4])
            half_disc(fr, 0, zs, w2 / 2, 0.0, 0.3, cols[(j + 1) % 4])
            for xx in (-w2 / 3, 0, w2 / 3):
                lbox(fr, (0.2, 0.34, zs - zb + 1.0), xx, -0.12, (zb + zs) / 2, 'we2_trim')
            for zz in (zb + (zs - zb) * 0.4, zb + (zs - zb) * 0.75):
                lbox(fr, (w2, 0.3, 0.2), 0, -0.12, zz, 'we2_trim')
            tube(nm('wa'), arc_pts(fr, 0, zs, w2 / 2 + 0.2, y=-0.2, n=11), 0.28, 'we2_trim', res=4)
            lbox(fr, (w2 + 1.0, 0.5, 0.5), 0, -0.2, zb - 0.2, 'we2_trim')
    # dais with wide steps at +y end
    dy = D / 2 - 10.0
    for k in range(4):
        box(nm('ds'), (24.0 - k * 3.0, 3.0, 1.0), loc=(0, dy - 6.0 + k * 3.0, 0.5 + k * 1.0), key='we2_ashlar' if k % 2 else 'we2_trim', bev=0.06)
    dz = 4.0
    box(nm('dtop'), (22.0, 10.0, 0.6), loc=(0, dy + 1.0, dz + 0.3), key='we2_floor_a')
    # throne
    tx, ty = 0.0, dy + 2.0
    box(nm('thb'), (5.0, 3.6, 1.0), loc=(tx, ty, dz + 0.5), key='we2_ashlar', bev=0.06)
    box(nm('ths'), (4.4, 3.0, 0.5), loc=(tx, ty, dz + 1.25), key='we2_carpet')
    box(nm('thback'), (4.4, 0.6, 7.0), loc=(tx, ty + 1.5, dz + 4.5), key='we2_wood')
    box(nm('thbp'), (4.8, 0.7, 0.8), loc=(tx, ty + 1.5, dz + 8.2), key='we2_gold', bev=0.06)
    for s in (-1, 1):
        box(nm('tharm'), (0.5, 3.0, 2.0), loc=(tx + s * 2.2, ty, dz + 2.5), key='we2_wood')
        lathe(nm('thf'), [(0, 0), (0.3, 0), (0.12, 0.8), (0.3, 1.2), (0, 1.6)], loc=(tx + s * 2.2, ty + 1.5, dz + 6.9), key='we2_gold', segs=8)
    for s in (-1, 1):
        cyl(nm('cnp'), 0.3, 11.0, loc=(tx + s * 3.4, ty + 1.2, dz + 1.0), key='we2_gold', verts=10)
    box(nm('cnt'), (9.0, 4.0, 0.5), loc=(tx, ty + 0.6, dz + 12.2), key='we2_wood')
    lslab(F(tx, ty - 2.0, dz + 12.0, 0), [(-4.5, 0, 0), (4.5, 0, 0), (4.5, 0, -2.0), (0, 0, -3.4), (-4.5, 0, -2.0)], (0, 3.6, 0), 'we2_banner_r')
    ball(nm('cfin'), 0.5, loc=(tx, ty + 0.6, dz + 12.7), key='we2_gold', segs=10, rings=7)
    for s in (-1, 1):
        _brazier(s * 8.0, dy - 8.0)
    for py in (-D / 2 + 20.0, 0.0, D / 2 - 26.0):
        _chandelier(0, py, H, drop=6.0, r=2.4, candles=8)
    _mdoor(F(0, -D / 2, 0, 0), 0)
    return finalize('throne_hall', smooth_angle=30)


# ===================================================== B06 market stalls
def _stall_base(seed, ca, cb, shape='flat'):
    rnd = random.Random(seed)
    L, D, Hc = 10.0, 8.0, 3.0
    box(nm('ct'), (L, 2.4, Hc), loc=(0, -D / 2 + 1.2, Hc / 2), key='we2_wood')
    box(nm('ctp'), (L + 0.4, 2.8, 0.3), loc=(0, -D / 2 + 1.2, Hc + 0.15), key='we2_wood_l', bev=0.04)
    box(nm('bt'), (L, 1.6, 0.25), loc=(0, D / 2 - 1.2, 2.2), key='we2_wood')
    box(nm('bt2'), (L, 1.6, 0.25), loc=(0, D / 2 - 1.2, 3.6), key='we2_wood')
    for sx in (-1, 1):
        for sy in (-1, 1):
            h = 9.0 if sy < 0 else 8.0
            lathe(nm('post'), [(0, 0), (0.3, 0), (0.22, 0.4), (0.3, 0.8), (0.2, h - 1.2), (0.3, h - 0.9), (0.22, h - 0.5), (0.28, h), (0, h)],
                  loc=(sx * (L / 2 - 0.3), sy * (D / 2 - 0.3), 0), key='we2_timber', segs=10)
            ball(nm('pk'), 0.26, loc=(sx * (L / 2 - 0.3), sy * (D / 2 - 0.3), h + 0.1), key='we2_gold', segs=8, rings=6)
    lbeam(F(), (-L / 2, -D / 2 + 0.3, 8.9), (L / 2, -D / 2 + 0.3, 8.9), 0.25, 'we2_timber')
    lbeam(F(), (-L / 2, D / 2 - 0.3, 7.9), (L / 2, D / 2 - 0.3, 7.9), 0.25, 'we2_timber')
    n = 8
    if shape == 'flat':
        for i in range(n):
            x = -L / 2 + L / n * (i + 0.5)
            k = ca if i % 2 == 0 else cb
            box(nm('can'), (L / n + 0.02, D + 1.2, 0.1), loc=(x, 0.05, 8.4), key=k, rot=(-7, 0, 0))
    elif shape == 'peak':
        for i in range(n):
            x = -L / 2 + L / n * (i + 0.5)
            k = ca if i % 2 == 0 else cb
            for s in (-1, 1):
                lslab(F(), [(x - L / n / 2, s * (D / 2 + 0.6), 7.6), (x + L / n / 2, s * (D / 2 + 0.6), 7.6), (x + L / n / 2, 0, 9.8), (x - L / n / 2, 0, 9.8)], (0, 0, 0.1), k)
    else:  # round barrel vault
        for i in range(n):
            x = -L / 2 + L / n * (i + 0.5)
            k = ca if i % 2 == 0 else cb
            pts = [(x, -math.cos(math.pi * j / 8) * (D / 2 + 0.6), 7.4 + math.sin(math.pi * j / 8) * 2.6) for j in range(9)]
            for j in range(8):
                lslab(F(), [(x - L / n / 2, pts[j][1], pts[j][2]), (x + L / n / 2, pts[j][1], pts[j][2]),
                            (x + L / n / 2, pts[j + 1][1], pts[j + 1][2]), (x - L / n / 2, pts[j + 1][1], pts[j + 1][2])], (0, 0, 0.1), k)
    for i in range(n):
        x = -L / 2 + L / n * (i + 0.5)
        k = ca if i % 2 == 0 else cb
        poly_prism(nm('val'), [(-L / n / 2, 0), (L / n / 2, 0), (0, -0.7)], 0.05, loc=(x, -D / 2 - 0.6, 8.2), key=k, rot=(90, 0, 0))
    lbeam(F(), (-L / 2 - 0.1, -D / 2 + 0.3, 7.5), (-L / 2 - 1.8, -D / 2 + 0.3, 7.5), 0.14, 'we2_iron')
    lbox(F(-L / 2 - 1.5, -D / 2 + 0.3, 0, 0), (0.18, 1.6, 1.3), 0, 0, 6.6, ca, bev=0.04)
    for z in (7.3, 5.9):
        tube(nm('sgc'), [(-L / 2 - 1.5, -D / 2 + 0.3, z), (-L / 2 - 0.2, -D / 2 + 0.3, 7.5)], 0.04, 'we2_iron', res=4)
    _mdoor(F(0, -D / 2, 0, 0), 0)
    return rnd, L, D, Hc


def stall_fruit():
    """Red/cream peaked canopy, crates of heaped fruit, baskets, hanging onion strings."""
    reset()
    rnd, L, D, Hc = _stall_base(61, 'we2_canopy_r', 'we2_canopy_cr', shape='peak')
    cols = ['we2_fruit_a', 'we2_fruit_b', 'we2_fruit_c', 'we2_fruit_d']
    for cx in (-3.2, 0.0, 3.2):
        box(nm('cr'), (2.4, 1.8, 1.0), loc=(cx, -D / 2 + 1.2, Hc + 0.65), key='we2_wood_l')
        for k in range(10):
            a = rnd.uniform(0, 6.28); r = rnd.uniform(0, 0.8)
            ball(nm('fr'), rnd.uniform(0.26, 0.36), loc=(cx + math.cos(a) * r, -D / 2 + 1.2 + math.sin(a) * r * 0.6, Hc + 1.3 + rnd.uniform(0, 0.2)), key=rnd.choice(cols), segs=8, rings=6)
    for cx in (-3.0, 0.0, 3.0):
        lathe(nm('bk'), [(0, 0), (0.8, 0), (0.95, 1.0), (0.85, 1.05), (0, 0.15)], loc=(cx, D / 2 - 1.2, 2.45), key='we2_hay', segs=12)
        for k in range(6):
            ball(nm('bf'), 0.26, loc=(cx + rnd.uniform(-0.4, 0.4), D / 2 - 1.2 + rnd.uniform(-0.4, 0.4), 3.7), key=rnd.choice(cols), segs=7, rings=5)
    for x in (-4.0, 4.0):
        for k in range(3):
            tube(nm('on'), [(x + k * 0.3, -D / 2 + 0.4, 8.6), (x + k * 0.3, -D / 2 + 0.4, 6.8)], 0.04, 'we2_rope', res=4)
            for j in range(4):
                ball(nm('onb'), 0.18, loc=(x + k * 0.3, -D / 2 + 0.4, 7.0 + j * 0.4), key='we2_cloth_d', segs=6, rings=4)
    return finalize('stall_fruit', smooth_angle=30)


def stall_cloth():
    """Blue/cream flat-sloped canopy, rolls and standing bolts of fabric, hanging samples."""
    reset()
    rnd, L, D, Hc = _stall_base(62, 'we2_canopy_bl', 'we2_canopy_cr', shape='flat')
    cols = ['we2_cloth_a', 'we2_cloth_b', 'we2_cloth_c', 'we2_cloth_d']
    for k in range(6):
        x = -4.0 + k * 1.6
        cyl(nm('roll'), 0.4, 2.0, loc=(x, -D / 2 + 1.2, Hc + 0.5), key=rnd.choice(cols), verts=12, rot=(90, 0, rnd.uniform(-10, 10)))
    for k in range(5):
        x = -3.6 + k * 1.8
        box(nm('bolt'), (1.2, 0.5, 2.4), loc=(x, D / 2 - 1.2, 3.4), key=rnd.choice(cols), rot=(0, rnd.uniform(-6, 6), 0), bev=0.05)
    for k in range(5):
        x = -4.0 + k * 2.0
        lslab(F(x, -D / 2 + 0.3, 8.9, 0), [(-0.7, 0, 0), (0.7, 0, 0), (0.7, 0.1, -3.0), (-0.7, 0.1, -3.0)], (0, -0.08, 0), cols[k % 4])
    return finalize('stall_cloth', smooth_angle=30)


def stall_potion():
    """Green/gold round barrel-vault canopy, shelves of glowing bottles, a bubbling cauldron."""
    reset()
    rnd, L, D, Hc = _stall_base(63, 'we2_canopy_gr', 'we2_canopy_gd', shape='round')
    cols = ['we2_potion_r', 'we2_potion_b', 'we2_potion_g', 'we2_potion_p']

    def bottle(x, y, z, key, s=1.0, kind=0):
        if kind == 0:
            prof = [(0, 0), (0.28, 0), (0.32, 0.25), (0.3, 0.5), (0.1, 0.7), (0.1, 0.9), (0, 0.9)]
        elif kind == 1:
            prof = [(0, 0), (0.18, 0), (0.36, 0.25), (0.36, 0.42), (0.1, 0.62), (0.1, 0.85), (0, 0.85)]
        else:
            prof = [(0, 0), (0.22, 0), (0.22, 0.6), (0.08, 0.72), (0.08, 0.95), (0, 0.95)]
        lathe(nm('bt'), [(r * s, zz * s) for r, zz in prof], loc=(x, y, z), key=key, segs=8)
        cyl(nm('cork'), 0.08 * s, 0.14 * s, loc=(x, y, z + prof[-1][1] * s), key='we2_wood_l', verts=6)
    for k in range(10):
        bottle(-4.3 + k * 0.95, -D / 2 + 1.2, Hc + 0.3, rnd.choice(cols), s=rnd.uniform(0.8, 1.1), kind=k % 3)
    for z in (2.45, 3.85):
        for k in range(9):
            bottle(-4.0 + k * 1.0, D / 2 - 1.2, z, rnd.choice(cols), s=0.7, kind=(k + 1) % 3)
    cyl(nm('cau'), 1.1, 1.3, loc=(3.6, -D / 2 + 1.2, Hc + 0.2), key='we2_iron', verts=16, r2=1.3)
    cyl(nm('caul'), 1.05, 0.06, loc=(3.6, -D / 2 + 1.2, Hc + 1.5), key='we2_potion_g', verts=16)
    for k in range(3):
        ball(nm('bub'), 0.2 - k * 0.04, loc=(3.6 + (k - 1) * 0.3, -D / 2 + 1.2, Hc + 1.6 + k * 0.2), key='we2_potion_g', segs=6, rings=4)
    for x in (-4.5, -3.8):
        for k in range(3):
            tube(nm('hb'), [(x + k * 0.2, -D / 2 + 0.4, 8.4), (x + k * 0.2, -D / 2 + 0.4, 7.2)], 0.03, 'we2_rope', res=4)
            ball(nm('hbl'), 0.2, loc=(x + k * 0.2, -D / 2 + 0.4, 7.0), key='we2_cloth_c', segs=6, rings=4, scale=(0.6, 0.6, 1.4))
    return finalize('stall_potion', smooth_angle=30)


BATCHES = {
    'throne':  ('v4_castle', [('B03_01_throne_hall_01', throne_hall, (0.9, -1.1, 0.4))]),
    'market':  ('v4_castle', [('B06_01_stall_fruit', stall_fruit),
                              ('B06_02_stall_cloth', stall_cloth),
                              ('B06_03_stall_potion', stall_potion)]),
}
