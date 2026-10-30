"""Worker we - B03-B06 castle interior, garrison, courtyard and market set (v4_castle).
Belongs to the same castle as worker wb's B02 keep/towers: matching ashlar, marble trim,
slate and heraldry colours. 1 unit = 1 stud. Fronts face -Y. Richer than the old castle.py
courtyard pieces: real relief, trims, variety, believable construction.
"""
import math, random
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, top_paint, dup
from arch import (F, faces, lbox, lbeam, beam3, slab, lslab, half_disc, window, door, arrow_slit, quoins, band,
                  corbels, battlements, ring_battlements, timber_frame, gable_roof, roof_z, cone_roof, chimney,
                  dormer, railing, column_c, pediment, dome, pinnacle, arc_pts, nm)

# ---------------------------------------------------------- worker palette (all start with we_)
# echoes worker wb's B02 castle colours so the pieces read as one castle
P = kitlib.PAL
P['we_ashlar']      = ((206, 198, 180), 'Limestone',    0.00, 0.82, 0)
P['we_ashlar_b']    = ((190, 182, 164), 'Limestone',    0.00, 0.85, 0)
P['we_ashlar_c']    = ((176, 166, 148), 'Limestone',    0.00, 0.88, 0)
P['we_plinth']      = ((132, 128, 120), 'Cobblestone',  0.00, 0.90, 0)
P['we_trim']        = ((230, 224, 210), 'Marble',       0.00, 0.48, 0)
P['we_trim_warm']   = ((224, 210, 180), 'Marble',       0.00, 0.50, 0)
P['we_slate_a']     = ((70, 82, 108),   'Slate',        0.00, 0.72, 0)
P['we_slate_b']     = ((58, 68, 92),    'Slate',        0.00, 0.74, 0)
P['we_floor_a']     = ((178, 170, 154), 'Marble',       0.00, 0.55, 0)
P['we_floor_b']     = ((96, 92, 86),    'Slate',        0.00, 0.80, 0)
P['we_carpet']      = ((140, 28, 36),   'Fabric',       0.00, 1.00, 0)
P['we_carpet_trim'] = ((198, 158, 72),  'Fabric',       0.00, 0.95, 0)
P['we_banner_red']  = ((150, 36, 42),   'Fabric',       0.00, 0.95, 0)
P['we_banner_gold'] = ((196, 158, 72),  'Fabric',       0.00, 0.95, 0)
P['we_banner_blue'] = ((44, 66, 128),   'Fabric',       0.00, 0.95, 0)
P['we_gold']        = ((214, 172, 72),  'Metal',        1.00, 0.25, 0)
P['we_bronze']      = ((120, 86, 52),   'Metal',        0.90, 0.40, 0)
P['we_iron']        = ((44, 42, 40),    'Metal',        0.85, 0.48, 0)
P['we_timber']      = ((78, 54, 37),    'Wood',         0.00, 0.85, 0)
P['we_plaster']     = ((222, 210, 188), 'Plaster',      0.00, 0.90, 0)
P['we_wood']        = ((122, 84, 52),   'WoodPlanks',   0.00, 0.80, 0)
P['we_wood_light']  = ((166, 126, 84),  'WoodPlanks',   0.00, 0.80, 0)
P['we_leather']     = ((96, 64, 42),    'Fabric',       0.00, 0.85, 0)
P['we_steel']       = ((150, 156, 164), 'Metal',        0.90, 0.32, 0)
P['we_hay']         = ((190, 160, 92),  'Fabric',       0.00, 1.00, 0)
P['we_canopy_r']    = ((164, 54, 48),   'Fabric',       0.00, 0.95, 0)
P['we_canopy_cream']= ((230, 218, 188), 'Fabric',       0.00, 0.95, 0)
P['we_canopy_blue'] = ((52, 86, 140),   'Fabric',       0.00, 0.95, 0)
P['we_canopy_green']= ((60, 110, 72),   'Fabric',       0.00, 0.95, 0)
P['we_canopy_gold'] = ((200, 160, 72),  'Fabric',       0.00, 0.95, 0)
P['we_cloth_a']     = ((150, 46, 54),   'Fabric',       0.00, 0.95, 0)
P['we_cloth_b']     = ((48, 78, 132),   'Fabric',       0.00, 0.95, 0)
P['we_cloth_c']     = ((60, 108, 78),   'Fabric',       0.00, 0.95, 0)
P['we_cloth_d']     = ((196, 170, 90),  'Fabric',       0.00, 0.95, 0)
P['we_fruit_a']     = ((186, 36, 34),   'SmoothPlastic', 0.00, 0.45, 0)
P['we_fruit_b']     = ((232, 160, 42),  'SmoothPlastic', 0.00, 0.50, 0)
P['we_fruit_c']     = ((120, 172, 58),  'SmoothPlastic', 0.00, 0.55, 0)
P['we_fruit_d']     = ((150, 70, 160),  'SmoothPlastic', 0.00, 0.50, 0)
P['we_potion_r']    = ((198, 40, 70),   'Glass',        0.00, 0.10, 0.4)
P['we_potion_b']    = ((60, 110, 220),  'Glass',        0.00, 0.10, 0.4)
P['we_potion_g']    = ((80, 200, 110),  'Glass',        0.00, 0.10, 0.4)
P['we_potion_p']    = ((170, 90, 220),  'Glass',        0.00, 0.10, 0.4)
P['we_glass_lit']   = ((246, 196, 110), 'Glass',        0.00, 0.20, 0.45)
P['we_stained_r']   = ((190, 48, 56),   'Glass',        0.00, 0.10, 0.5)
P['we_stained_b']   = ((56, 92, 190),   'Glass',        0.00, 0.10, 0.5)
P['we_stained_y']   = ((232, 186, 60),  'Glass',        0.00, 0.10, 0.5)
P['we_stained_g']   = ((60, 150, 90),   'Glass',        0.00, 0.10, 0.5)
P['we_flame']       = ((255, 150, 40),  'Neon',         0.00, 0.50, 2.0)
P['we_flame_core']  = ((255, 214, 120), 'Neon',         0.00, 0.50, 2.0)
P['we_wax']         = ((238, 228, 200), 'SmoothPlastic', 0.00, 0.50, 0)
P['we_rope']        = ((176, 150, 104), 'Fabric',       0.00, 1.00, 0)


def marker_door(f, x, z=0.0):
    import v4util
    v4util.marker('mk_door', f.p(x, -0.1, z + 0.1))


# ================================================================ shared bits
def flame(loc, h=1.1, r=0.4, seed=0):
    rnd = random.Random(seed)
    prof = [(0.0, 0.0), (r * 0.7, h * 0.08), (r, h * 0.24), (r * 0.85, h * 0.46), (r * 0.5, h * 0.7), (r * 0.2, h * 0.9), (0.0, h)]
    o = lathe(nm('fl'), prof, loc=loc, key='we_flame', segs=8)
    o.rotation_euler.z = rnd.uniform(0, 6.28)
    lathe(nm('flc'), [(0.0, 0.0), (r * 0.5, h * 0.14), (r * 0.42, h * 0.4), (0.0, h * 0.58)], loc=(loc[0], loc[1], loc[2] + h * 0.03), key='we_flame_core', segs=8)


def brazier(x, y, h=4.2, r=1.5):
    lathe(nm('bz'), [(0.0, 0.0), (0.5, 0.0), (0.35, 0.3), (0.3, h - 1.6), (r, h - 0.3), (r, h), (r - 0.25, h), (r - 0.25, h - 0.25), (0.35, h - 1.4), (0.0, h - 1.4)],
          loc=(x, y, 0), key='we_iron', segs=14)
    for i in range(3):
        a = 2 * math.pi * i / 3
        tube(nm('bzl'), [(x + math.cos(a) * 0.3, y + math.sin(a) * 0.3, 0.1), (x + math.cos(a) * 0.7, y + math.sin(a) * 0.7, 0.0)], 0.12, 'we_iron', res=4)
    cyl(nm('coal'), r - 0.35, 0.2, loc=(x, y, h - 0.4), key='we_iron', verts=14)
    for i in range(7):
        a = 2 * math.pi * i / 7
        flame((x + math.cos(a) * (r - 0.6) * 0.5, y + math.sin(a) * (r - 0.6) * 0.5, h - 0.3), h=1.2 + 0.4 * (i % 2), r=0.4, seed=i)
    flame((x, y, h - 0.2), h=1.8, r=0.5, seed=9)


def wall_banner(f, x, z, w=3.6, h=9.0, key='we_banner_red', emblem='we_gold', seed=0):
    lbox(f, (w + 0.6, 0.35, 0.35), x, -0.4, z + 0.1, 'we_bronze')
    for s in (-1, 1):
        ball(nm('fin'), 0.26, loc=f.p(x + s * (w / 2 + 0.3), -0.4, z + 0.1), key='we_gold', segs=8, rings=6)
    # cloth with forked bottom, slight billow
    n = 7
    pts_top = [(x - w / 2 + w * k / n, 0.0, z) for k in range(n + 1)]
    bm_pts = []
    for k in range(n + 1):
        xx = x - w / 2 + w * k / n
        billow = -0.12 * math.sin(math.pi * k / n)
        bm_pts.append((xx, billow, z))
    # fork: two tails
    verts = []
    verts += [(x - w / 2, 0.0, z)]
    for k in range(n + 1):
        verts.append((x - w / 2 + w * k / n, -0.1 * math.sin(math.pi * k / n), z - h + (1.6 if (k in (0, n)) else (0.0 if k == n // 2 else 0.8))))
    verts.append((x + w / 2, 0.0, z))
    lslab(f, [(x - w / 2, 0.0, z), (x + w / 2, 0.0, z), (x + w / 2, -0.12, z - h + 1.4), (x + w * 0.18, -0.12, z - h + 3.2),
              (x, -0.12, z - h), (x - w * 0.18, -0.12, z - h + 3.2), (x - w / 2, -0.12, z - h + 1.4)], (0, -0.14, 0), key)
    # emblem disc
    cyl(nm('em'), w * 0.26, 0.08, loc=f.p(x, -0.2, z - h * 0.42), key=emblem, verts=16, rot=f.r(90, 0, 0))
    cyl(nm('emi'), w * 0.14, 0.06, loc=f.p(x, -0.26, z - h * 0.42), key=key, verts=12, rot=f.r(90, 0, 0))


def tiled_floor(W, D, z=0.0, a='we_floor_a', b='we_floor_b', tile=4.0, border='we_trim'):
    nx = max(2, int(W / tile)); ny = max(2, int(D / tile))
    sx, sy = W / nx, D / ny
    for i in range(nx):
        for j in range(ny):
            k = a if (i + j) % 2 == 0 else b
            box(nm('ft'), (sx - 0.12, sy - 0.12, 0.3), loc=(-W / 2 + sx * (i + 0.5), -D / 2 + sy * (j + 0.5), z + 0.15), key=k, bev=0.03)
    box(nm('fb'), (W + 0.6, D + 0.6, 0.25), loc=(0, 0, z - 0.1), key=border)


def carpet(x0, x1, y, w=6.0, z=0.32, key='we_carpet', trim='we_carpet_trim'):
    L = x1 - x0
    box(nm('cp'), (L, w, 0.14), loc=((x0 + x1) / 2, y, z), key=key)
    for s in (-1, 1):
        box(nm('cpt'), (L, 0.5, 0.16), loc=((x0 + x1) / 2, y + s * (w / 2 - 0.3), z + 0.01), key=trim)
    # short fringe at the near end
    for k in range(int(w / 0.5)):
        box(nm('fr'), (0.5, 0.12, 0.1), loc=(x0 - 0.3, y - w / 2 + 0.3 + k * 0.5, z), key=trim)


def chandelier(x, y, z_ceiling, drop=5.0, r=2.2, candles=8):
    # chain
    tube(nm('ch'), [(x, y, z_ceiling), (x, y, z_ceiling - drop)], 0.08, 'we_iron', res=4)
    torus(nm('ring'), r, 0.14, loc=(x, y, z_ceiling - drop), key='we_iron', segs=20, rsegs=5)
    torus(nm('ring2'), r * 0.55, 0.12, loc=(x, y, z_ceiling - drop + 0.5), key='we_iron', segs=16, rsegs=4)
    for i in range(candles):
        a = 2 * math.pi * i / candles
        cx, cy = x + math.cos(a) * r, y + math.sin(a) * r
        tube(nm('arm'), [(x, y, z_ceiling - drop + 0.4), (cx, cy, z_ceiling - drop + 0.1)], 0.07, 'we_iron', res=4)
        cyl(nm('cup'), 0.22, 0.14, loc=(cx, cy, z_ceiling - drop + 0.1), key='we_bronze', verts=8)
        cyl(nm('cd'), 0.13, 0.7, loc=(cx, cy, z_ceiling - drop + 0.2), key='we_wax', verts=8)
        flame((cx, cy, z_ceiling - drop + 0.9), h=0.7, r=0.22, seed=i)
    for i in range(3):
        cx, cy = x, y
        cyl(nm('cd'), 0.14, 0.8, loc=(x + (i - 1) * 0.5, y, z_ceiling - drop + 0.7), key='we_wax', verts=8)
        flame((x + (i - 1) * 0.5, y, z_ceiling - drop + 1.5), h=0.7, r=0.22, seed=20 + i)


# ================================================================ B03 throne hall (interior kit)
def throne_hall():
    """B03_01 - throne-hall interior kit (no roof): tiled two-stone floor, long red carpet, 10 pillars with
    capitals, a low side wall carrying tall stained-glass bays with banners between, dais with wide steps,
    canopied throne, two braziers, big chandeliers on chains."""
    reset()
    W, D, H = 50.0, 80.0, 30.0
    tiled_floor(W, D, 0.0, tile=4.0)
    # long red carpet runner, raised clearly above the tiles, from the door to the dais foot
    carpet(-D / 2 + 2.0, D / 2 - 15.0, 0.0, w=9.0, z=0.55)
    px = 16.0                     # pillar x
    wx = W / 2                    # side-wall x
    zcap = H - 3.0
    pillar_ys = [-D / 2 + 10.0 + i * (D - 28.0) / 4 for i in range(5)]
    cols = ['we_stained_b', 'we_stained_r', 'we_stained_y', 'we_stained_g']
    bkeys = ['we_banner_red', 'we_banner_blue', 'we_banner_gold', 'we_banner_red']
    for s in (-1, 1):
        # continuous low ashlar side wall (dado) with a parapet band, so the hall has sides
        box(nm('wall'), (1.6, D - 6.0, H), loc=(s * wx, 0, H / 2), key='we_ashlar')
        band(s * wx, 0, 1.6, D - 6.0, 6.0, 0.6, 'we_trim', out=0.3)
        band(s * wx, 0, 1.6, D - 6.0, H - 0.6, 0.7, 'we_trim', out=0.3)
        for j, py in enumerate(pillar_ys):
            column_c(s * px, py, 0.0, zcap, 1.6, key='we_ashlar', base='we_trim')
            box(nm('pb'), (4.4, 4.4, 1.0), loc=(s * px, py, 0.5), key='we_plinth', bev=0.08)
        # architrave beam linking pillar tops
        lbeam(F(), (s * px, pillar_ys[0], zcap), (s * px, pillar_ys[-1], zcap), 1.2, 'we_trim')
        # stained-glass bays set INTO the side wall, with a banner between each pair
        fr = F(s * (wx - 0.8), 0, 0, -90 if s < 0 else 90)  # local x = +y world, faces inward
        for j, py in enumerate(pillar_ys):
            lx = (py if s < 0 else -py)   # frame-local x for this bay
            w2, zb, h2 = 4.4, 7.0, 15.0
            zs = zb + h2 - w2 * 0.6
            lbox(fr, (w2, 0.4, zs - zb), lx, -0.0, (zb + zs) / 2, cols[j % 4])
            half_disc(fr, lx, zs, w2 / 2, 0.0, 0.4, cols[(j + 1) % 4])
            for mx in (-w2 / 3, 0, w2 / 3):
                lbox(fr, (0.22, 0.5, zs - zb + 1.0), lx + mx, -0.05, (zb + zs) / 2, 'we_trim')
            for zz in (zb + (zs - zb) * 0.4, zb + (zs - zb) * 0.75):
                lbox(fr, (w2, 0.4, 0.22), lx, -0.05, zz, 'we_trim')
            tube(nm('wa'), arc_pts(fr, lx, zs, w2 / 2 + 0.25, y=-0.05, n=11), 0.3, 'we_trim', res=4)
            lbox(fr, (w2 + 1.2, 0.6, 0.6), lx, -0.1, zb - 0.3, 'we_trim')
        for j in range(len(pillar_ys) - 1):
            my = (pillar_ys[j] + pillar_ys[j + 1]) / 2
            bf = F(s * (wx - 0.9), my, zcap - 2.0, -90 if s < 0 else 90)
            wall_banner(bf, 0, 0, w=3.0, h=11.0, key=bkeys[j % 4], emblem='we_gold', seed=j + s)
    # dais with wide steps at the far (+y) end, facing the door
    dy = D / 2 - 11.0
    for k in range(5):
        box(nm('ds'), (30.0 - k * 3.4, 3.2, 1.1), loc=(0, dy - 7.0 + k * 3.2, 0.55 + k * 1.1), key='we_trim' if k % 2 else 'we_ashlar', bev=0.06)
    dz = 5.5
    box(nm('dtop'), (26.0, 11.0, 0.8), loc=(0, dy + 2.0, dz + 0.4), key='we_floor_a')
    # throne on the dais
    tx, ty = 0.0, dy + 3.0
    box(nm('thb'), (6.0, 4.2, 1.2), loc=(tx, ty, dz + 0.6), key='we_ashlar', bev=0.06)
    box(nm('ths'), (5.2, 3.4, 0.6), loc=(tx, ty, dz + 1.5), key='we_carpet')
    box(nm('thback'), (5.2, 0.7, 9.0), loc=(tx, ty + 1.8, dz + 5.7), key='we_wood')
    box(nm('thbp'), (5.6, 0.8, 1.0), loc=(tx, ty + 1.8, dz + 10.5), key='we_gold', bev=0.06)
    ball(nm('thorb'), 0.6, loc=(tx, ty + 1.8, dz + 11.3), key='we_gold', segs=10, rings=7)
    for s in (-1, 1):
        box(nm('tharm'), (0.6, 3.4, 2.4), loc=(tx + s * 2.6, ty, dz + 3.0), key='we_wood')
        lathe(nm('thf'), [(0, 0), (0.34, 0), (0.14, 0.9), (0.34, 1.4), (0, 1.9)], loc=(tx + s * 2.6, ty + 1.8, dz + 8.3), key='we_gold', segs=8)
    # canopy: four gold posts + a draped red valance
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl(nm('cnp'), 0.32, 14.0, loc=(tx + sx * 4.2, ty + 0.2 + sy * 2.4, dz + 1.2), key='we_gold', verts=10)
    box(nm('cnt'), (10.0, 6.0, 0.6), loc=(tx, ty + 0.2, dz + 15.0), key='we_wood')
    lslab(F(tx, ty - 3.0, dz + 14.8, 0), [(-5.0, 0, 0), (5.0, 0, 0), (5.0, 0, -2.2), (0, 0, -3.8), (-5.0, 0, -2.2)], (0, 6.0, 0), 'we_banner_red')
    for sx in (-1, 1):
        lslab(F(tx + sx * 5.0, ty - 3.0, dz + 14.8, 0), [(0, 0, 0), (0, 0, -2.2), (0, 6.0, -2.2), (0, 6.0, 0)], (sx * 0.1, 0, 0), 'we_banner_red')
    ball(nm('cfin'), 0.6, loc=(tx, ty + 0.2, dz + 15.6), key='we_gold', segs=10, rings=7)
    # two braziers flanking the dais foot
    for s in (-1, 1):
        brazier(s * 9.0, dy - 9.0)
    # three big chandeliers on chains down the centre
    for py in (-D / 2 + 20.0, -2.0, D / 2 - 28.0):
        chandelier(0, py, H - 0.6, drop=8.0, r=3.2, candles=10)
    marker_door(F(0, -D / 2, 0, 0), 0)
    return finalize('throne_hall', smooth_angle=30)


# ================================================================ B04 garrison
def barracks():
    """B04_01 - barracks: stone ground floor, timber-framed upper storey, crenellated roofline,
    weapon racks, shield wall, training dummy, stone stair to a raised door, chimney. ~42x23x28."""
    reset()
    W, D, gh, uh = 42.0, 23.0, 10.0, 9.0
    t = 1.8
    # ground stone box (hollow, closed interior)
    box(nm('g'), (W, D, gh), loc=(0, 0, gh / 2), key='we_ashlar')
    box(nm('plinth'), (W + 0.6, D + 0.6, 1.2), loc=(0, 0, 0.6), key='we_plinth', bev=0.06)
    box(nm('floor'), (W - 2 * t, D - 2 * t, 0.4), loc=(0, 0, 0.3), key='we_floor_b')
    # hollow out: build walls as boxes around the door/windows instead of solid
    # (use solid block; a viewer at the door sees the interior floor + opposite wall through opening)
    fc = faces(0, 0, W, D)
    for s in ('front', 'back', 'left', 'right'):
        L = W if s in ('front', 'back') else D
        quoins(fc[s], 0.9, gh - 0.3, 'we_trim', course=1.1)
    # raised door on the front, reached by a stone stair
    door_z = 2.4
    for k in range(4):
        box(nm('st'), (7.0, 2.0 + k * 0.0, 0.6), loc=(-W / 2 + 7.0, -D / 2 - 4.5 + k * 1.5, 0.3 + k * 0.6), key='we_ashlar_b', bev=0.05)
    # recess the doorway: cut a dark opening and a timber door
    lbox(fc['front'], (4.4, 0.4, 7.0), -W / 2 + 7.0, 0.1, door_z + 3.5, 'we_timber')
    door(fc['front'].sub(0, 0, door_z), -W / 2 + 7.0, w=4.0, h=7.0, arch=True, key='we_timber', surround='we_trim', step=None)
    marker_door(fc['front'].sub(0, 0, door_z), -W / 2 + 7.0)
    # ground windows (arrow-slit + arched)
    for x in (-6.0, 4.0, 14.0):
        window(fc['front'], x, 3.0, w=2.2, h=4.0, arch=True, frame='we_trim', sill='we_trim', glass='we_glass_lit', lit=True)
    for x in (-14.0, -4.0, 6.0, 15.0):
        window(fc['back'], x, 3.0, w=2.2, h=4.0, arch=True, frame='we_trim', sill='we_trim')
    for s in ('left', 'right'):
        window(fc[s], 0, 3.0, w=2.4, h=4.4, arch=True, frame='we_trim', sill='we_trim')
    band(0, 0, W, D, gh - 0.1, 0.6, 'we_trim', out=0.2)
    # timber-framed upper storey (jettied slightly)
    jj = 0.8
    dk = D + 2 * jj
    box(nm('u'), (W, dk, uh), loc=(0, 0, gh + uh / 2), key='we_plaster')
    for s in (-1, 1):
        for i in range(int(W / 2.4) + 1):
            xx = -W / 2 + 0.4 + (W - 0.8) * i / int(W / 2.4)
            box(nm('jo'), (0.45, 0.9, 0.5), loc=(xx, s * (dk / 2 - 0.3), gh + 0.1), key='we_timber')
    fu = faces(0, 0, W, dk, gh)
    for side, L in (('front', W), ('back', W), ('left', dk), ('right', dk)):
        np_ = max(2, int(L / 8))
        posts = [-L / 2 + 0.3] + [-L / 2 + L * i / np_ for i in range(1, np_)] + [L / 2 - 0.3]
        timber_frame(fu[side], L, 0, uh, posts, key='we_timber', braces=(side in ('front', 'back')))
        n = max(2, int(L / 9))
        for i in range(n):
            x = -L / 2 + L * (i + 0.5) / n
            window(fu[side], x, 2.2, w=2.4, h=4.0, frame='we_timber', shutter=None, sill='we_timber', glass='we_glass_lit',
                   panes=False, lit=((i % 3 == 1) and side == 'front'))
    # crenellated roofline (flat roof walk with battlements)
    box(nm('rf'), (W, dk, 0.6), loc=(0, 0, gh + uh + 0.3), key='we_floor_b')
    ft = faces(0, 0, W, dk, gh + uh + 0.6)
    for s, L in (('front', W), ('back', W), ('left', dk), ('right', dk)):
        battlements(ft[s], -L / 2, L / 2, 0, 'we_ashlar', t=1.0, mw=1.8, gap=1.4, mh=1.8, ph=1.3, cap='we_trim')
    chimney(W / 2 - 5.0, dk * 0.2, gh + uh, gh + uh + 8.0, w=2.2, key='we_ashlar_b')
    # yard furniture in front: a weapon rack, shield wall, training dummy
    _weapon_rack(-W / 2 + 18.0, -D / 2 - 3.0, 0)
    _shield_wall(6.0, -D / 2 - 3.2)
    _training_dummy(16.0, -D / 2 - 4.0)
    return finalize('barracks', smooth_angle=28)


def _weapon_rack(x, y, rz):
    f = F(x, y, 0, rz)
    lbox(f, (5.0, 0.6, 0.4), 0, 0, 0.2, 'we_wood')
    lbox(f, (5.0, 0.6, 0.5), 0, 0, 4.0, 'we_wood')
    for s in (-1, 1):
        lbox(f, (0.4, 0.4, 4.2), s * 2.3, 0, 2.1, 'we_wood')
    rnd = random.Random(int(x * 3 + y))
    for k in range(6):
        wx = -2.0 + k * 0.8
        kind = k % 3
        if kind == 0:  # spear
            lbox(f, (0.1, 0.1, 5.2), wx, 0, 2.6, 'we_timber')
            lathe(nm('sp'), [(0, 0), (0.14, 0), (0, 0.6)], loc=f.p(wx, 0, 5.0), key='we_steel', segs=6)
        elif kind == 1:  # sword
            lbox(f, (0.12, 0.08, 3.2), wx, 0.1, 2.0, 'we_steel')
            lbox(f, (0.5, 0.12, 0.14), wx, 0.1, 0.5, 'we_bronze')
            lbox(f, (0.12, 0.12, 0.5), wx, 0.1, 0.25, 'we_leather')
        else:  # axe
            lbox(f, (0.1, 0.1, 4.0), wx, 0, 2.2, 'we_timber')
            poly_prism(nm('ax'), [(0, 0), (0.7, 0.3), (0.7, -0.3)], 0.12, loc=f.p(wx + 0.1, 0.0, 3.6), key='we_steel', rot=f.r(90, 0, 0))


def _shield_wall(x, y):
    f = F(x, y, 0, 0)
    lbox(f, (9.0, 0.6, 5.0), 0, 0, 2.5, 'we_wood')
    for s in (-1, 1):
        lbox(f, (0.5, 0.6, 5.6), s * 4.5, 0, 2.8, 'we_wood')
    cols = ['we_banner_red', 'we_banner_blue', 'we_banner_gold']
    for i, (sx, sz) in enumerate(((-3.0, 1.6), (0.0, 1.6), (3.0, 1.6), (-1.5, 3.4), (1.5, 3.4))):
        poly_prism(nm('sh'), [(-1.0, 0), (1.0, 0), (1.0, 1.0), (0, -1.6), (-1.0, 1.0)] if False else
                   [(-1.0, 0.8), (1.0, 0.8), (1.0, -0.6), (0, -1.6), (-1.0, -0.6)], 0.18, loc=f.p(sx, -0.1, sz + 0.6), key=cols[i % 3], rot=f.r(90, 0, 0))
        cyl(nm('shb'), 0.3, 0.1, loc=f.p(sx, -0.25, sz), key='we_gold', verts=10, rot=f.r(90, 0, 0))


def _training_dummy(x, y):
    cyl(nm('tdp'), 0.3, 5.5, loc=(x, y, 0), key='we_timber', verts=8)
    ball(nm('tdb'), 1.1, loc=(x, y, 4.0), key='we_hay', segs=12, rings=8, scale=(1, 1, 1.3))
    for s in (-1, 1):
        lbox(F(x, y, 0, 0), (3.6, 0.5, 0.5), 0, 0, 4.2, 'we_timber')
        ball(nm('tdh'), 0.5, loc=(x + s * 1.5, y, 4.2), key='we_hay', segs=8, rings=6)
    ball(nm('tdhd'), 0.7, loc=(x, y, 5.6), key='we_hay', segs=10, rings=7)
    torus(nm('tdr'), 1.1, 0.08, loc=(x, y, 3.4), key='we_rope', segs=14, rsegs=4)
    box(nm('tdsh'), (1.6, 0.2, 1.8), loc=(x, y - 1.0, 4.0), key='we_wood', bev=0.04)


def stables():
    """B04_02 - stables: long low building with open stall fronts, half doors, hay, troughs,
    a hay-loft door with pulley beam, lanterns. ~41x20x18."""
    reset()
    W, D, wh = 41.0, 20.0, 10.0
    t = 1.6
    box(nm('plinth'), (W + 0.6, D + 0.6, 0.8), loc=(0, 0, 0.4), key='we_plinth', bev=0.05)
    box(nm('floor'), (W, D, 0.3), loc=(0, 0, 0.55), key='we_floor_b')
    # back and side walls stone; front is open stalls
    box(nm('back'), (W, t, wh), loc=(0, D / 2 - t / 2, wh / 2), key='we_ashlar')
    for s in (-1, 1):
        box(nm('side'), (t, D, wh), loc=(s * (W / 2 - t / 2), 0, wh / 2), key='we_ashlar')
    # open stall front: posts + a top beam + half doors
    nst = 5
    sw = (W - 2 * t) / nst
    lbeam(F(), (-W / 2 + t, -D / 2 + 1.0, wh - 0.5), (W / 2 - t, -D / 2 + 1.0, wh - 0.5), 0.7, 'we_timber')
    for i in range(nst + 1):
        x = -W / 2 + t + sw * i
        box(nm('post'), (0.7, 0.7, wh), loc=(x, -D / 2 + 1.0, wh / 2), key='we_timber')
    # interior partitions between stalls
    for i in range(1, nst):
        x = -W / 2 + t + sw * i
        box(nm('part'), (0.4, D - 2.0, 3.4), loc=(x, 0.5, 1.9), key='we_wood')
    rnd = random.Random(42)
    for i in range(nst):
        cx = -W / 2 + t + sw * (i + 0.5)
        # half door
        lbox(F(cx, -D / 2 + 1.0, 0, 0), (sw - 1.2, 0.3, 3.2), 0, -0.1, 1.9, 'we_wood')
        lbox(F(cx, -D / 2 + 1.0, 0, 0), (sw - 1.2, 0.34, 0.3), 0, -0.14, 3.4, 'we_timber')
        torus(nm('hdr'), 0.18, 0.05, loc=(cx + sw * 0.3, -D / 2 + 0.6, 2.0), key='we_iron', segs=10, rsegs=4, rot=(90, 0, 0))
        # hay + trough inside each stall
        for k in range(3):
            box(nm('hay'), (1.4, 1.0, 0.6), loc=(cx - 1.0 + k * 1.0, D / 2 - 3.0, 0.9 + (k % 2) * 0.3), key='we_hay', rot=(0, 0, rnd.uniform(0, 20)), bev=0.1)
        lbox(F(cx, D / 2 - 1.5, 0, 0), (sw - 1.4, 1.2, 0.8), 0, 0, 1.0, 'we_wood')
        box(nm('trw'), (sw - 1.8, 0.8, 0.1), loc=(cx, D / 2 - 1.5, 1.4), key='we_potion_b' if False else 'water' if 'water' in kitlib.PAL else 'we_floor_b')
    # loft above with a hay-loft door and pulley beam (gable roof)
    hr = D * 0.42
    gable_roof(F(), W, D, wh, hr, keys=('we_slate_a', 'we_slate_b'), wall='we_ashlar', ov=1.0, ovg=0.8, barge='we_timber')
    # loft door in the front gable? place a dormer-style loft door on the front roof
    fl = F(0, -D / 2 - 0.2, wh, 0)
    lbox(fl, (4.0, 0.4, 4.0), 0, 0.1, 2.5, 'we_ashlar')
    lbox(fl, (3.2, 0.3, 3.0), 0, -0.1, 2.3, 'we_wood')  # closed loft door
    # pulley beam jutting out over the loft door
    lbeam(fl, (0, -0.2, 5.4), (0, -3.6, 5.4), 0.4, 'we_timber')
    torus(nm('pul'), 0.4, 0.12, loc=fl.p(0, -3.3, 5.0), key='we_iron', segs=12, rsegs=4)
    tube(nm('pr'), [fl.p(0, -3.3, 4.7), fl.p(0, -3.3, 1.5)], 0.05, 'we_rope', res=4)
    lathe(nm('hk'), [(0, 0), (0.16, 0.1), (0.12, 0.5), (0, 0.6)], loc=fl.p(0, -3.3, 0.9), key='we_iron', segs=6)
    # lanterns on the front posts
    for i in (1, 3):
        x = -W / 2 + t + sw * i
        f = F(x, -D / 2 + 0.7, 0, 0)
        box(nm('lg'), (0.5, 0.5, 0.7), 0 if True else 0, -0.1, 0, 'we_glass_lit') if False else None
        lbox(f, (0.5, 0.5, 0.7), 0, -0.3, wh - 2.0, 'we_glass_lit')
        lathe(nm('lc'), [(0.35, 0), (0, 0.35)], loc=f.p(0, -0.3, wh - 1.6), key='we_iron', segs=6)
    marker_door(F(-W / 2 + t + sw * 2.5, -D / 2 + 1.0, 0, 0), 0)
    return finalize('stables', smooth_angle=28)


# ================================================================ B05 courtyard
def royal_fountain():
    """B05_01 - tiered marble fountain, ~24x24x18, with figures/finials and water."""
    reset()
    R = 11.0
    lathe(nm('step'), [(0, 0), (R + 1.5, 0), (R + 1.5, 0.5), (R + 0.5, 0.6), (0, 0.6)], loc=(0, 0, 0), key='we_plinth', segs=24)
    # octagonal basin wall
    lathe(nm('basin'), [(0, 0.6), (R, 0.6), (R, 1.0), (R + 0.3, 1.2), (R + 0.3, 3.0), (R + 0.6, 3.3), (R + 0.6, 3.8), (R - 0.8, 3.8), (R - 0.8, 1.4), (0, 1.4)],
          loc=(0, 0, 0), key='we_trim', segs=8)
    cyl(nm('pool'), R - 0.8, 0.06, loc=(0, 0, 3.4), key='water' if 'water' in kitlib.PAL else 'we_potion_b', verts=8, rot=(0, 0, 22.5))
    # pedestals around rim with finials
    for i in range(8):
        a = math.radians(22.5 + 45 * i)
        px, py = math.cos(a) * (R - 0.4) * 0.92, math.sin(a) * (R - 0.4) * 0.92
        lathe(nm('fin'), [(0, 0), (0.5, 0), (0.4, 0.4), (0.5, 1.2), (0.3, 2.0), (0.4, 2.3), (0, 2.5)], loc=(px, py, 3.8), key='we_trim', segs=10)
        ball(nm('finb'), 0.4, loc=(px, py, 6.4), key='we_gold', segs=8, rings=6)
    # tier 1
    lathe(nm('p1'), [(0, 1.4), (2.6, 1.4), (2.2, 2.6), (1.5, 3.2), (1.3, 7.0), (1.6, 7.4), (0, 7.4)], loc=(0, 0, 0), key='we_ashlar', segs=12)
    lathe(nm('b1'), [(0, 7.0), (1.3, 7.0), (4.4, 8.0), (5.4, 8.8), (5.6, 9.3), (5.1, 9.3), (4.2, 8.8), (0, 8.6)], loc=(0, 0, 0), key='we_trim', segs=24)
    cyl(nm('w1'), 5.0, 0.06, loc=(0, 0, 9.1), key='water' if 'water' in kitlib.PAL else 'we_potion_b', verts=24)
    # tier 2
    lathe(nm('p2'), [(0, 8.6), (1.0, 8.6), (0.8, 12.5), (1.0, 12.8), (0, 12.8)], loc=(0, 0, 0), key='we_ashlar', segs=12)
    lathe(nm('b2'), [(0, 12.5), (1.0, 12.5), (2.6, 13.2), (3.1, 13.8), (2.8, 13.8), (2.4, 13.5), (0, 13.4)], loc=(0, 0, 0), key='we_trim', segs=20)
    cyl(nm('w2'), 2.7, 0.06, loc=(0, 0, 13.65), key='water' if 'water' in kitlib.PAL else 'we_potion_b', verts=20)
    # crowning figure: an urn with lion-head spouts (simple finial figure)
    lathe(nm('p3'), [(0, 13.4), (0.7, 13.4), (0.5, 15.6), (0.9, 16.2), (0.6, 17.2), (0.0, 17.6)], loc=(0, 0, 0), key='we_trim', segs=12)
    ball(nm('top'), 0.7, loc=(0, 0, 18.0), key='we_gold', segs=12, rings=8)
    # water streams
    for i in range(12):
        a = 2 * math.pi * i / 12
        m = (math.cos(a) * 6.0, math.sin(a) * 6.0, 6.0)
        tube(nm('ws'), [(math.cos(a) * 5.4, math.sin(a) * 5.4, 9.1), m, (math.cos(a) * 7.6, math.sin(a) * 7.6, 3.5)], 0.12,
             'water_fx' if 'water_fx' in kitlib.PAL else 'we_potion_b', res=6, taper=[1.0, 0.9, 0.6])
    return finalize('royal_fountain', smooth_angle=35)


def _knight(Z, metal='we_bronze', accent='we_steel'):
    # plinth is built by the caller; this is the figure, origin at Z
    for s, fwd in ((-1, -0.45), (1, 0.4)):
        tube(nm('lg'), [(s * 0.55, 0, Z + 4.2), (s * 0.7, fwd * 0.6, Z + 2.3), (s * 0.8, fwd, Z + 0.5)], 0.42, metal, res=6, taper=[1.0, 0.85, 0.8])
        box(nm('ft'), (0.7, 1.4, 0.5), loc=(s * 0.8, fwd - 0.25, Z + 0.25), key=metal, bev=0.1)
        ball(nm('kn'), 0.34, loc=(s * 0.7, fwd * 0.6 - 0.15, Z + 2.3), key=accent, segs=8, rings=6)
    lathe(nm('skirt'), [(0, Z + 3.5), (1.3, Z + 3.5), (1.05, Z + 4.8), (0, Z + 4.8)], loc=(0, 0, 0), key=metal, segs=12, sx=1.0, sy=0.8)
    lathe(nm('tor'), [(0, Z + 4.7), (1.0, Z + 4.7), (1.15, Z + 5.5), (1.35, Z + 6.5), (1.1, Z + 7.2), (0.4, Z + 7.4), (0, Z + 7.4)], loc=(0, 0, 0), key=metal, segs=14, sx=1.0, sy=0.72)
    torus(nm('belt'), 1.05, 0.12, loc=(0, 0, Z + 4.8), key=accent, segs=16, rsegs=4)
    for s in (-1, 1):
        ball(nm('pa'), 0.7, loc=(s * 1.3, 0, Z + 6.9), key=accent, segs=12, rings=8, scale=(1.0, 0.9, 0.7))
    # raised sword arm
    tube(nm('ra'), [(1.35, 0, Z + 6.7), (1.9, -0.3, Z + 7.8), (1.8, -0.4, Z + 9.1)], 0.32, metal, res=6)
    ball(nm('rh'), 0.32, loc=(1.8, -0.4, Z + 9.25), key=metal, segs=8, rings=6)
    beam3((1.8, -0.4, Z + 9.5), (1.75, -0.45, Z + 14.8), 0.42, 0.1, accent)
    beam3((1.6, -0.42, Z + 9.5), (2.0, -0.42, Z + 9.5), 1.6, 0.25, 'we_gold', roll=90)
    # shield arm
    tube(nm('la'), [(-1.35, 0, Z + 6.7), (-1.75, -0.5, Z + 5.8), (-1.3, -1.0, Z + 5.4)], 0.32, metal, res=6)
    sh = [(-1.0, 0, 1.4), (1.0, 0, 1.4), (1.0, 0, 0.0), (0.0, 0, -1.6), (-1.0, 0, 0.0)]
    lslab(F(-1.4, -1.25, Z + 5.5, 15), sh, (0, -0.25, 0), accent)
    lslab(F(-1.4, -1.5, Z + 5.5, 15), [(-0.15, 0, 1.1), (0.15, 0, 1.1), (0.15, 0, -1.2), (-0.15, 0, -1.2)], (0, -0.06, 0), 'we_gold')
    # head/helm with plume
    cyl(nm('nk'), 0.35, 0.5, loc=(0, 0, Z + 7.3), key=metal, verts=10)
    lathe(nm('hm'), [(0, Z + 7.7), (0.62, Z + 7.7), (0.7, Z + 8.3), (0.62, Z + 8.8), (0.3, Z + 9.1), (0, Z + 9.15)], loc=(0, 0, 0), key=metal, segs=14)
    box(nm('vs'), (0.9, 0.2, 0.12), loc=(0, -0.65, Z + 8.35), key='we_iron')
    tube(nm('pl'), [(0, -0.1, Z + 9.1), (0, 0.5, Z + 9.6), (0, 1.3, Z + 9.2), (0, 1.8, Z + 8.4)], 0.22, 'we_banner_red', res=6, taper=[1, 1.2, 0.8, 0.3])


def knight_statue():
    """B05_02 - plinth + armoured knight with raised sword, ~24 high."""
    reset()
    Z = 7.0
    box(nm('pb'), (6.4, 6.4, 1.0), loc=(0, 0, 0.5), key='we_plinth', bev=0.08)
    box(nm('pb2'), (5.4, 5.4, 0.6), loc=(0, 0, 1.3), key='we_ashlar', bev=0.06)
    box(nm('pd'), (4.4, 4.4, Z - 2.6), loc=(0, 0, 1.6 + (Z - 2.6) / 2), key='we_trim')
    box(nm('pc'), (5.0, 5.0, 0.5), loc=(0, 0, Z - 0.75), key='we_ashlar', bev=0.06)
    box(nm('pc2'), (4.6, 4.6, 0.5), loc=(0, 0, Z - 0.25), key='we_trim', bev=0.04)
    lbox(F(0, -2.2, 0, 0), (2.8, 0.15, 1.4), 0, -0.07, (Z + 1.6) / 2, 'we_gold', bev=0.04)
    _knight(Z)
    return finalize('knight_statue', smooth_angle=40)


def obelisk():
    """B05_03 - obelisk ~32 high on a stepped base with carved gold bands."""
    reset()
    for k in range(3):
        box(nm('ob'), (8.0 - k * 1.6, 8.0 - k * 1.6, 0.8), loc=(0, 0, 0.4 + k * 0.8), key='we_ashlar' if k % 2 == 0 else 'we_trim', bev=0.06)
    box(nm('od'), (3.8, 3.8, 3.0), loc=(0, 0, 3.9), key='we_trim', bev=0.05)
    box(nm('odc'), (4.3, 4.3, 0.4), loc=(0, 0, 5.6), key='we_ashlar', bev=0.04)
    lathe(nm('sh'), [(0, 5.8), (2.2, 5.8), (1.3, 30.0), (0, 30.0)], loc=(0, 0, 0), key='we_trim', segs=4)
    lathe(nm('pyr'), [(0, 30.0), (1.36, 30.0), (0, 32.4)], loc=(0, 0, 0), key='we_gold', segs=4)
    for zz in (9.0, 16.0, 23.0):
        rr = 2.2 - (zz - 5.8) / 24.2 * 0.9
        lathe(nm('bd'), [(0, zz), (rr + 0.12, zz), (rr + 0.12, zz + 0.5), (0, zz + 0.5)], loc=(0, 0, 0), key='we_gold', segs=4)
    for k in range(4):
        fr = faces(0, 0, 3.8, 3.8)[('front', 'back', 'left', 'right')[k]]
        cyl(nm('oe'), 0.9, 0.12, loc=fr.p(0, 0, 3.9), key='we_gold', verts=12, rot=fr.r(90, 0, 0))
    return finalize('obelisk', smooth_angle=20)


def ornate_lamp():
    """B05_04 - ~14 high wrought-iron lamp post with scrollwork and warm glass."""
    reset()
    from kitlib import scroll
    # stepped stone base
    box(nm('b0'), (2.6, 2.6, 0.6), loc=(0, 0, 0.3), key='we_plinth', bev=0.1)
    box(nm('b1'), (1.8, 1.8, 0.6), loc=(0, 0, 0.9), key='we_ashlar', bev=0.08)
    lathe(nm('col'), [(0, 1.2), (0.55, 1.2), (0.4, 1.8), (0.3, 10.5), (0.42, 11.0), (0.3, 11.4), (0, 11.4)], loc=(0, 0, 0), key='we_iron', segs=12)
    for z in (2.2, 3.6):
        torus(nm('ring'), 0.45, 0.07, loc=(0, 0, z), key='we_iron', segs=14, rsegs=4)
    # scroll brackets near the top
    for i in range(4):
        a = i * math.pi / 2
        scroll(nm('sc'), (math.cos(a) * 0.3, math.sin(a) * 0.3, 10.4), 0.05, 0.45, 1.1, 'XZ' if i % 2 == 0 else 'YZ', 'we_iron', 0.07, n=24)
    # lantern head: four-sided glass with iron frame and finial
    lathe(nm('lb'), [(0, 11.3), (0.85, 11.3), (0.85, 11.6), (0, 11.6)], loc=(0, 0, 0), key='we_iron', segs=4)
    lathe(nm('lg'), [(0, 11.6), (0.72, 11.6), (0.72, 13.4), (0, 13.4)], loc=(0, 0, 0), key='we_glass_lit', segs=4)
    for i in range(4):
        a = math.pi / 4 + i * math.pi / 2
        tube(nm('le'), [(math.cos(a) * 0.74, math.sin(a) * 0.74, 11.6), (math.cos(a) * 0.74, math.sin(a) * 0.74, 13.4)], 0.07, 'we_iron', res=4)
    lathe(nm('lc'), [(0, 13.4), (0.9, 13.4), (0.85, 13.6), (0.3, 14.3), (0, 14.4)], loc=(0, 0, 0), key='we_iron', segs=4)
    lathe(nm('lf'), [(0, 14.4), (0.2, 14.4), (0.1, 14.7), (0.18, 15.0), (0, 15.2)], loc=(0, 0, 0), key='we_gold', segs=8)
    return finalize('ornate_lamp', smooth_angle=30)


def royal_banner():
    """B05_05 - tall pole ~24 with a large heraldic banner on a cross-arm and a gold finial."""
    reset()
    box(nm('b0'), (3.0, 3.0, 0.8), loc=(0, 0, 0.4), key='we_plinth', bev=0.1)
    box(nm('b1'), (2.0, 2.0, 0.8), loc=(0, 0, 1.2), key='we_ashlar', bev=0.08)
    cyl(nm('pole'), 0.32, 23.0, loc=(0, 0, 1.6), key='we_timber', verts=12, r2=0.24)
    ball(nm('fin'), 0.5, loc=(0, 0, 24.8), key='we_gold', segs=12, rings=8)
    lathe(nm('finp'), [(0, 0), (0.22, 0), (0.1, 0.6), (0, 0.9)], loc=(0, 0, 25.1), key='we_gold', segs=8)
    # cross-arm the banner hangs from
    cyl(nm('arm'), 0.18, 7.0, loc=(0, 0, 21.0), key='we_timber', verts=8, rot=(90, 0, 0))
    for s in (-1, 1):
        ball(nm('ak'), 0.26, loc=(0, s * 3.5, 21.0), key='we_gold', segs=8, rings=6)
    # big banner cloth with slight billow and forked base, emblem
    f = F(0, 0, 21.0, 0)
    pts = [(-3.2, 0, 0), (3.2, 0, 0), (3.2, 0, -12.0), (1.4, 0, -10.0), (0, 0, -13.0), (-1.4, 0, -10.0), (-3.2, 0, -12.0)]
    lslab(f, pts, (0, -0.16, 0), 'we_banner_red')
    # subtle billow via a thin inner panel pushed out
    cyl(nm('em'), 1.6, 0.1, loc=f.p(0, -0.2, -6.0), key='we_gold', verts=5, rot=f.r(90, 0, 0))
    cyl(nm('emi'), 1.0, 0.08, loc=f.p(0, -0.28, -6.0), key='we_banner_red', verts=5, rot=f.r(90, 0, 0))
    return finalize('royal_banner', smooth_angle=30)


def gazebo():
    """B05_06 - ~18x20x25 open pavilion with columns, ironwork and a domed/conical roof."""
    reset()
    R = 8.5
    n = 8
    # stepped stone platform
    for k in range(3):
        cyl(nm('pf'), R + 2.2 - k * 0.8, 0.5, loc=(0, 0, k * 0.5), key='we_ashlar' if k % 2 else 'we_trim', verts=n, bev=0.05, rot=(0, 0, 22.5))
    box(nm('floor'), (1, 1, 1), loc=(0, 0, -5)) if False else None
    cyl(nm('fl'), R + 0.5, 0.2, loc=(0, 0, 1.5), key='we_floor_a', verts=n, rot=(0, 0, 22.5))
    colh = 15.0
    for i in range(n):
        a = math.radians(22.5 + 45 * i)
        cx, cy = math.cos(a) * R, math.sin(a) * R
        column_c(cx, cy, 1.5, colh, 0.55, key='we_trim', base='we_ashlar')
        # ironwork arch between columns
    for i in range(n):
        a0 = math.radians(22.5 + 45 * i)
        a1 = math.radians(22.5 + 45 * (i + 1))
        x0, y0 = math.cos(a0) * R, math.sin(a0) * R
        x1, y1 = math.cos(a1) * R, math.sin(a1) * R
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        tube(nm('arc'), [(x0, y0, 1.5 + colh - 1.0), (mx, my, 1.5 + colh + 1.2), (x1, y1, 1.5 + colh - 1.0)], 0.18, 'we_iron', res=4)
        from kitlib import scroll
        scroll(nm('iw'), (mx, my, 1.5 + colh - 2.0), 0.05, 0.6, 1.0, 'XZ', 'we_iron', 0.07, n=22)
    # entablature ring
    lathe(nm('ent'), [(R - 0.3, 1.5 + colh), (R + 0.8, 1.5 + colh), (R + 0.8, 1.5 + colh + 0.9), (R - 0.3, 1.5 + colh + 0.9)], loc=(0, 0, 0), key='we_trim', segs=n, rot=(0, 0, 22.5))
    # conical slate roof + finial
    cone_roof(0, 0, 1.5 + colh + 0.9, R + 0.8, 8.0, keys=('we_slate_a', 'we_slate_b'), rings=6, ov=0.9, segs=n, finial='we_gold')
    # central bench
    cyl(nm('bench'), 2.0, 1.8, loc=(0, 0, 1.7), key='we_ashlar', verts=12)
    cyl(nm('bencht'), 2.2, 0.3, loc=(0, 0, 3.4), key='we_trim', verts=12, bev=0.08)
    return finalize('gazebo', smooth_angle=28)


def rose_arch():
    """B05_07 - ~8 wide x 11 high iron/stone arch smothered in roses."""
    reset()
    rnd = random.Random(57)
    W, H = 8.0, 11.0
    for s in (-1, 1):
        # stone footing + iron post
        box(nm('ft'), (1.4, 1.4, 0.8), loc=(s * W / 2, 0, 0.4), key='we_ashlar', bev=0.1)
        cyl(nm('post'), 0.2, H - 1.0, loc=(s * W / 2, 0, 0.8), key='we_iron', verts=8)
    # arched top
    tube(nm('arch'), [(-W / 2, 0, H - 2.5), (-W / 2 + 0.5, 0, H - 0.6), (0, 0, H + 0.4), (W / 2 - 0.5, 0, H - 0.6), (W / 2, 0, H - 2.5)], 0.2, 'we_iron', res=4, ures=4)
    # lattice cross-bars
    for s in (-1, 1):
        for z in (3.0, 5.5, 8.0):
            tube(nm('lat'), [(s * W / 2, 0, z), (s * (W / 2 - 1.2), 0, z)], 0.07, 'we_iron', res=4)
    for x in (-W / 4, 0, W / 4):
        tube(nm('top'), [(x, 0, H - 0.2 - abs(x) / W * 2.0), (x, 0, H + 1.0)], 0.07, 'we_iron', res=4) if False else None
    # roses + leaves climbing all over (deterministic scatter)
    def rose(px, py, pz, s=1.0):
        for k in range(4):
            a = 2 * math.pi * k / 4 + rnd.uniform(0, 1)
            ball(nm('pet'), 0.22 * s, loc=(px + math.cos(a) * 0.18 * s, py, pz + math.sin(a) * 0.18 * s), key=rnd.choice(['fl_red', 'fl_pink']) if 'fl_red' in kitlib.PAL else 'we_banner_red', segs=6, rings=4, scale=(1, 0.6, 1))
        ball(nm('core'), 0.14 * s, loc=(px, py - 0.08, pz), key='we_fruit_b', segs=6, rings=4)
    # along the two posts
    for s in (-1, 1):
        for k in range(14):
            z = 1.0 + k * (H - 2.0) / 13
            off = rnd.uniform(-0.5, 0.5)
            ball(nm('lf'), rnd.uniform(0.3, 0.5), loc=(s * W / 2 + off, rnd.uniform(-0.3, 0.3), z), key='leaf_dark' if 'leaf_dark' in kitlib.PAL else 'we_cloth_c', segs=6, rings=4, scale=(1, 0.6, 1))
            if rnd.random() < 0.7:
                rose(s * W / 2 + off, -0.3, z, s=rnd.uniform(0.8, 1.2))
    # along the arch
    for k in range(18):
        t = k / 17
        a = math.pi * t
        x = -math.cos(a) * W / 2 * 0.95
        z = H - 2.5 + math.sin(a) * 3.0
        ball(nm('lf'), rnd.uniform(0.3, 0.5), loc=(x, rnd.uniform(-0.3, 0.3), z), key='leaf' if 'leaf' in kitlib.PAL else 'we_cloth_c', segs=6, rings=4, scale=(1, 0.6, 1))
        if rnd.random() < 0.75:
            rose(x, -0.3, z, s=rnd.uniform(0.7, 1.1))
    return finalize('rose_arch', smooth_angle=30)


# ================================================================ B06 market stalls
def _stall_base(seed, canopy_a, canopy_b, shape='flat'):
    """Common stall frame ~10x8x9: carved posts, counter, back shelf, hanging sign, striped canopy.
    shape: 'flat' sloped, 'peak' ridged, 'round' barrel-vault — three different canopy shapes."""
    rnd = random.Random(seed)
    L, D, Hc = 10.0, 8.0, 3.0
    # counter
    box(nm('ct'), (L, 2.4, Hc), loc=(0, -D / 2 + 1.2, Hc / 2), key='we_wood')
    box(nm('ctp'), (L + 0.4, 2.8, 0.3), loc=(0, -D / 2 + 1.2, Hc + 0.15), key='we_wood_light', bev=0.04)
    for k in range(5):
        lbox(F(0, -D / 2, 0, 0), (L / 5 - 0.1, 0.16, Hc - 0.2), -L / 2 + L / 5 * (k + 0.5), -0.05, Hc / 2, 'we_wood')
    # back shelf table
    box(nm('bt'), (L, 1.6, 0.25), loc=(0, D / 2 - 1.2, 2.2), key='we_wood')
    box(nm('bt2'), (L, 1.6, 0.25), loc=(0, D / 2 - 1.2, 3.6), key='we_wood')
    # carved posts (turned)
    for sx in (-1, 1):
        for sy in (-1, 1):
            h = 9.0 if sy < 0 else 8.0
            lathe(nm('post'), [(0, 0), (0.3, 0), (0.22, 0.4), (0.3, 0.8), (0.2, h - 1.2), (0.3, h - 0.9), (0.22, h - 0.5), (0.28, h), (0, h)],
                  loc=(sx * (L / 2 - 0.3), sy * (D / 2 - 0.3), 0), key='we_timber', segs=10)
            ball(nm('pk'), 0.26, loc=(sx * (L / 2 - 0.3), sy * (D / 2 - 0.3), h + 0.1), key='we_gold', segs=8, rings=6)
    # beams
    lbeam(F(), (-L / 2, -D / 2 + 0.3, 8.9), (L / 2, -D / 2 + 0.3, 8.9), 0.25, 'we_timber')
    lbeam(F(), (-L / 2, D / 2 - 0.3, 7.9), (L / 2, D / 2 - 0.3, 7.9), 0.25, 'we_timber')
    # striped canopy
    n = 8
    front_z, back_z = 8.9, 7.9
    if shape == 'flat':
        for i in range(n):
            x = -L / 2 + L / n * (i + 0.5)
            k = canopy_a if i % 2 == 0 else canopy_b
            o = box(nm('can'), (L / n + 0.02, D + 1.2, 0.1), loc=(x, 0.05, 8.4), key=k, rot=(-7, 0, 0))
    elif shape == 'peak':
        for i in range(n):
            x = -L / 2 + L / n * (i + 0.5)
            k = canopy_a if i % 2 == 0 else canopy_b
            for s in (-1, 1):
                lslab(F(), [(x - L / n / 2, s * (D / 2 + 0.6), 7.6), (x + L / n / 2, s * (D / 2 + 0.6), 7.6), (x + L / n / 2, 0, 9.8), (x - L / n / 2, 0, 9.8)], (0, 0, 0.1), k)
    else:  # round barrel vault
        for i in range(n):
            x = -L / 2 + L / n * (i + 0.5)
            k = canopy_a if i % 2 == 0 else canopy_b
            pts = []
            for j in range(9):
                a = math.pi * j / 8
                pts.append((x, -math.cos(a) * (D / 2 + 0.6), 7.4 + math.sin(a) * 2.6))
            for j in range(8):
                lslab(F(), [(x - L / n / 2, pts[j][1], pts[j][2]), (x + L / n / 2, pts[j][1], pts[j][2]),
                            (x + L / n / 2, pts[j + 1][1], pts[j + 1][2]), (x - L / n / 2, pts[j + 1][1], pts[j + 1][2])], (0, 0, 0.1), k)
    # scalloped valance at the front
    for i in range(n):
        x = -L / 2 + L / n * (i + 0.5)
        k = canopy_a if i % 2 == 0 else canopy_b
        poly_prism(nm('val'), [(-L / n / 2, 0), (L / n / 2, 0), (0, -0.7)], 0.05, loc=(x, -D / 2 - 0.6, 8.2), key=k, rot=(90, 0, 0))
    # hanging sign
    lbeam(F(), (-L / 2 - 0.1, -D / 2 + 0.3, 7.5), (-L / 2 - 1.8, -D / 2 + 0.3, 7.5), 0.14, 'we_iron')
    for y in (-0.0, 0.0):
        pass
    lbox(F(-L / 2 - 1.5, -D / 2 + 0.3, 0, 0), (0.18, 1.6, 1.3), 0, 0, 6.6, canopy_a, bev=0.04)
    for z in (7.3, 5.9):
        tube(nm('sgc'), [(-L / 2 - 1.5, -D / 2 + 0.3, z), (-L / 2 - 0.2, -D / 2 + 0.3, 7.5)], 0.04, 'we_iron', res=4)
    marker_door(F(0, -D / 2, 0, 0), 0)
    return rnd, L, D, Hc


def stall_fruit():
    """B06_01 - fruit stall: red/cream peaked canopy, crates of fruit on the counter and shelf."""
    reset()
    rnd, L, D, Hc = _stall_base(61, 'we_canopy_r', 'we_canopy_cream', shape='peak')
    cols = ['we_fruit_a', 'we_fruit_b', 'we_fruit_c', 'we_fruit_d']
    # crates on the counter with heaped fruit
    for cx in (-3.2, 0.0, 3.2):
        box(nm('cr'), (2.4, 1.8, 1.0), loc=(cx, -D / 2 + 1.2, Hc + 0.65), key='we_wood_light')
        for k in range(10):
            a = rnd.uniform(0, 6.28); r = rnd.uniform(0, 0.8)
            ball(nm('fr'), rnd.uniform(0.26, 0.36), loc=(cx + math.cos(a) * r, -D / 2 + 1.2 + math.sin(a) * r * 0.6, Hc + 1.3 + rnd.uniform(0, 0.2)), key=rnd.choice(cols), segs=8, rings=6)
    # back shelf baskets
    for cx in (-3.0, 0.0, 3.0):
        lathe(nm('bk'), [(0, 0), (0.8, 0), (0.95, 1.0), (0.85, 1.05), (0, 0.15)], loc=(cx, D / 2 - 1.2, 2.45), key='wicker' if 'wicker' in kitlib.PAL else 'we_hay', segs=12)
        for k in range(6):
            ball(nm('bf'), 0.26, loc=(cx + rnd.uniform(-0.4, 0.4), D / 2 - 1.2 + rnd.uniform(-0.4, 0.4), 3.7), key=rnd.choice(cols), segs=7, rings=5)
    # hanging strings of onions/garlic
    for x in (-4.0, 4.0):
        for k in range(3):
            tube(nm('on'), [(x + k * 0.3, -D / 2 + 0.4, 8.6), (x + k * 0.3, -D / 2 + 0.4, 6.8)], 0.04, 'we_rope', res=4)
            for j in range(4):
                ball(nm('onb'), 0.18, loc=(x + k * 0.3, -D / 2 + 0.4, 7.0 + j * 0.4), key='we_cloth_d', segs=6, rings=4)
    return finalize('stall_fruit', smooth_angle=30)


def stall_cloth():
    """B06_02 - cloth stall: blue/cream flat-sloped canopy, bolts of fabric, hanging cloth samples."""
    reset()
    rnd, L, D, Hc = _stall_base(62, 'we_canopy_blue', 'we_canopy_cream', shape='flat')
    cols = ['we_cloth_a', 'we_cloth_b', 'we_cloth_c', 'we_cloth_d']
    # rolls of cloth stacked on the counter
    for k in range(6):
        x = -4.0 + k * 1.6
        cyl(nm('roll'), 0.4, 2.0, loc=(x, -D / 2 + 1.2, Hc + 0.5), key=rnd.choice(cols), verts=12, rot=(90, 0, rnd.uniform(-10, 10)))
    # standing bolts on the back shelf
    for k in range(5):
        x = -3.6 + k * 1.8
        box(nm('bolt'), (1.2, 0.5, 2.4), loc=(x, D / 2 - 1.2, 3.4), key=rnd.choice(cols), rot=(0, rnd.uniform(-6, 6), 0), bev=0.05)
    # hanging cloth samples draped from the front beam
    for k in range(5):
        x = -4.0 + k * 2.0
        lslab(F(x, -D / 2 + 0.3, 8.9, 0), [(-0.7, 0, 0), (0.7, 0, 0), (0.7, 0.1, -3.0), (-0.7, 0.1, -3.0)], (0, -0.08, 0), cols[k % 4])
    return finalize('stall_cloth', smooth_angle=30)


def stall_potion():
    """B06_03 - potion stall: green/gold round barrel-vault canopy, shelves of glowing bottles and a cauldron."""
    reset()
    rnd, L, D, Hc = _stall_base(63, 'we_canopy_green', 'we_canopy_gold', shape='round')
    cols = ['we_potion_r', 'we_potion_b', 'we_potion_g', 'we_potion_p']

    def bottle(x, y, z, key, s=1.0, kind=0):
        if kind == 0:
            prof = [(0, 0), (0.28, 0), (0.32, 0.25), (0.3, 0.5), (0.1, 0.7), (0.1, 0.9), (0, 0.9)]
        elif kind == 1:
            prof = [(0, 0), (0.18, 0), (0.36, 0.25), (0.36, 0.42), (0.1, 0.62), (0.1, 0.85), (0, 0.85)]
        else:
            prof = [(0, 0), (0.22, 0), (0.22, 0.6), (0.08, 0.72), (0.08, 0.95), (0, 0.95)]
        lathe(nm('bt'), [(r * s, zz * s) for r, zz in prof], loc=(x, y, z), key=key, segs=8)
        cyl(nm('cork'), 0.08 * s, 0.14 * s, loc=(x, y, z + prof[-1][1] * s), key='we_wood_light', verts=6)
    # bottles on counter
    for k in range(10):
        x = -4.3 + k * 0.95
        bottle(x, -D / 2 + 1.2, Hc + 0.3, rnd.choice(cols), s=rnd.uniform(0.8, 1.1), kind=k % 3)
    # two rows on the back shelves
    for z in (2.45, 3.85):
        for k in range(9):
            x = -4.0 + k * 1.0
            bottle(x, D / 2 - 1.2, z, rnd.choice(cols), s=0.7, kind=(k + 1) % 3)
    # bubbling cauldron on the counter end
    cyl(nm('cau'), 1.1, 1.3, loc=(3.6, -D / 2 + 1.2, Hc + 0.2), key='we_iron', verts=16, r2=1.3)
    cyl(nm('caul'), 1.05, 0.06, loc=(3.6, -D / 2 + 1.2, Hc + 1.5), key='we_potion_g', verts=16)
    for k in range(3):
        ball(nm('bub'), 0.2 - k * 0.04, loc=(3.6 + (k - 1) * 0.3, -D / 2 + 1.2, Hc + 1.6 + k * 0.2), key='we_potion_g', segs=6, rings=4)
    # hanging dried herbs
    for x in (-4.5, -3.8):
        for k in range(3):
            tube(nm('hb'), [(x + k * 0.2, -D / 2 + 0.4, 8.4), (x + k * 0.2, -D / 2 + 0.4, 7.2)], 0.03, 'we_rope', res=4)
            ball(nm('hbl'), 0.2, loc=(x + k * 0.2, -D / 2 + 0.4, 7.0), key='we_cloth_c', segs=6, rings=4, scale=(0.6, 0.6, 1.4))
    return finalize('stall_potion', smooth_angle=30)


# ================================================================ batches
BATCHES = {
    'throne':   ('v4_castle', [('B03_01_throne_hall_01', throne_hall, (0.9, -1.1, 0.4))]),
    'garrison': ('v4_castle', [('B04_01_barracks', barracks, (1.0, -1.2, 0.42)),
                               ('B04_02_stables', stables, (1.0, -1.2, 0.42))]),
    'court':    ('v4_castle', [('B05_01_royal_fountain', royal_fountain),
                               ('B05_02_knight_statue', knight_statue),
                               ('B05_03_obelisk', obelisk),
                               ('B05_04_ornate_lamp', ornate_lamp),
                               ('B05_05_royal_banner', royal_banner),
                               ('B05_06_gazebo', gazebo, (1.0, -1.1, 0.35)),
                               ('B05_07_rose_arch', rose_arch)]),
    'market':   ('v4_castle', [('B06_01_stall_fruit', stall_fruit),
                               ('B06_02_stall_cloth', stall_cloth),
                               ('B06_03_stall_potion', stall_potion)]),
}
