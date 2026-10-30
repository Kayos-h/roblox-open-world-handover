"""Fix worker wx3 - castle masonry, throne hall, potion stall, gate arch, box ruins.
Repairs the reviewer defects: camouflage square colour patches, checkerboard curtain walls
with gaps, over-budget plain towers, neon throne-hall glass + no roof + toy floor, neon
potion bottles, saturated gate-arch panels, plain-box story ruins.

Overrides WORKER_BRIEF: never edits originals; copies the builders here and fixes the copies.
Keeps each saved id + category so new .blend/.fbx overwrite in place. New keys prefixed wx3_.
"""
import math, random
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism
from arch import (F, faces, nm, lbox, lbeam, lslab, slab, half_disc, window, door, arrow_slit,
                  quoins, band, corbels, battlements, ring_battlements, gable_roof, cone_roof,
                  column_c, pinnacle, arc_pts)
import v4util

P = kitlib.PAL
# ---- uniform masonry: ONE stone body tone + ONE darker course tone + trim. No per-block variation.
P['wx3_stone']   = ((198, 190, 172), 'Limestone', 0.0, 0.84, 0)   # body (single tone)
P['wx3_stone_d'] = ((170, 162, 146), 'Limestone', 0.0, 0.88, 0)   # one step darker - lit depth, never black
P['wx3_course']  = ((168, 160, 144), 'Limestone', 0.0, 0.90, 0)   # thin darker horizontal band
P['wx3_plinth']  = ((140, 134, 124), 'Cobblestone', 0.0, 0.90, 0)
P['wx3_trim']    = ((222, 214, 198), 'Marble',    0.0, 0.55, 0)    # cornice / quoin
P['wx3_warm']    = ((206, 196, 172), 'Sandstone', 0.0, 0.84, 0)    # keep/spire warm body (single tone)
P['wx3_warm_c']  = ((176, 166, 146), 'Sandstone', 0.0, 0.90, 0)
P['wx3_slate_a'] = ((70, 82, 108),   'Slate',     0.0, 0.72, 0)
P['wx3_slate_b'] = ((58, 68, 92),    'Slate',     0.0, 0.74, 0)
P['wx3_slate_d'] = ((44, 52, 70),    'Slate',     0.0, 0.78, 0)
P['wx3_floor_a'] = ((176, 168, 152), 'Slate',     0.0, 0.70, 0)    # throne slab floor, quiet two-tone
P['wx3_floor_b'] = ((150, 142, 128), 'Slate',     0.0, 0.78, 0)
# muted stained glass (indigo / wine / forest / ochre) - no pure primaries, no emission
P['wx3_glass_in'] = ((58, 66, 120),  'Glass', 0.0, 0.30, 0)
P['wx3_glass_wn'] = ((128, 46, 54),  'Glass', 0.0, 0.30, 0)
P['wx3_glass_fg'] = ((54, 96, 70),   'Glass', 0.0, 0.30, 0)
P['wx3_glass_oc'] = ((176, 142, 70), 'Glass', 0.0, 0.30, 0)
# muted potion liquids (no neon) + glass bottle body
P['wx3_pot_r']  = ((150, 58, 66),  'Glass', 0.0, 0.30, 0)
P['wx3_pot_b']  = ((58, 92, 150),  'Glass', 0.0, 0.30, 0)
P['wx3_pot_g']  = ((72, 132, 92),  'Glass', 0.0, 0.30, 0)
P['wx3_pot_p']  = ((120, 86, 150), 'Glass', 0.0, 0.30, 0)
# muted gate-arch banner panels
P['wx3_ban_r']  = ((150, 52, 50),  'Fabric', 0.0, 0.95, 0)
P['wx3_ban_b']  = ((56, 78, 128),  'Fabric', 0.0, 0.95, 0)

WH, WT, WALK = 31.0, 10.0, 26.0   # keep the original tiling profile: wall height, thickness, walkway z


def slit_stone(f, x, z, h=3.2, key='wx3_stone_d'):
    """A shallow slit rendered in a lit darker-STONE tone (never near-black glass), set just
    proud of the wall face so it reads as a recessed loophole without a black void."""
    lbox(f, (0.4, 0.12, h), x, -0.06, z, key)
    lbox(f, (1.2, 0.12, 0.34), x, -0.06, z + h * 0.15, key)


# ============================================================ masonry helpers (uniform tone)
def course_bands(f, w, z0, z1, y, course=2.7, depth=0.12, key='wx3_course'):
    """Thin recessed darker horizontal band every `course` studs on a flat wall face at local y.
    No per-block variation: the body stays one tone, only these slim lines break it up."""
    z = z0 + course
    while z < z1 - 0.3:
        lbox(f, (w - 0.1, depth, 0.35), 0, y - depth / 2, z, key)
        z += course


def ring_course_bands(cx, cy, r, z0, z1, course=2.7, key='wx3_course', segs=28):
    """Thin darker course rings on a round tower shaft - uniform tone, no patches."""
    z = z0 + course
    while z < z1 - 0.3:
        lathe(nm('rc'), [(r, z - 0.17), (r + 0.18, z - 0.17), (r + 0.18, z + 0.18), (r, z + 0.18)],
              loc=(cx, cy, 0), key=key, segs=segs)
        z += course


def wall_profile(f, length, key='wx3_stone', seed=0, quoin_ends=True):
    """One straight curtain-wall segment, fixed profile, flat watertight faces + recessed course
    lines (no protruding offset blocks, so NO gaps and it tiles). Walkway + crenellated parapet."""
    L = length
    # battered plinth (two steps)
    lbox(f, (L, WT + 1.8, 2.4), 0, 0, 1.2, 'wx3_plinth', bev=0.08)
    lbox(f, (L, WT + 1.0, 1.6), 0, 0, 3.0, 'wx3_plinth')
    # solid core - one uniform tone, full thickness, no gaps
    lbox(f, (L, WT, WH - 3.2), 0, 0, 3.2 + (WH - 3.2) / 2, key)
    # recessed course lines both faces
    course_bands(F(*f.p(0, -WT / 2, 0), f.rz), L, 3.6, WALK - 0.5, y=0.0)
    course_bands(F(*f.p(0, WT / 2, 0), f.rz + 180), L, 3.6, WALK - 0.5, y=0.0)
    # sparse quoins at the ends so segments read as dressed stone and butt cleanly
    if quoin_ends:
        for s in (-1, 1):
            quoins(F(*f.p(s * L / 2, -WT / 2, 0), f.rz), 3.6, WALK - 1.0, 'wx3_trim', sizes=(1.5, 0.9), course=2.7, t=0.16)
    # string course under the walkway
    lbox(f, (L, WT + 0.8, 0.6), 0, 0, WALK - 0.4, 'wx3_trim', bev=0.05)
    # walkway slab
    lbox(f, (L, WT - 1.2, 1.0), 0, 0, WALK + 0.5, 'wx3_floor_a')
    # machicolation corbels under the outer parapet
    corbels(F(*f.p(0, -WT / 2, 0), f.rz), -L / 2 + 1.0, L / 2 - 1.0, WALK - 1.0, 'wx3_stone', step=2.4, size=(0.7, 1.0, 1.1))
    # outer crenellated parapet (fixed rhythm), inner low parapet
    fo = F(*f.p(0, -WT / 2 + 0.5, WALK + 1.0), f.rz)
    battlements(fo, -L / 2, L / 2, 0, key, t=1.1, mw=2.0, gap=1.4, mh=2.6, ph=1.6, y=0.0, cap='wx3_trim')
    fi = F(*f.p(0, WT / 2 - 0.5, WALK + 1.0), f.rz + 180)
    lbox(fi, (L, 0.9, 2.0), 0, 0.45, 1.0, key)
    # fill the open walkway channel at both ends with a solid stone end-wall flush to BOTH parapet
    # faces, so there is no recessed pocket to read as a black void. Spans full thickness + merlon height.
    for s in (-1, 1):
        # Solid dressed end built with world-space box() (guaranteed outward normals - lbox here
        # produced inverted black faces). Placed at the frame's world end position + the frame angle.
        wx, wy, wz = f.p(s * (L / 2 - 2.0), 0, WALK + 1.0 + 2.6)
        box(nm('endfill'), (4.0, WT, 6.2), loc=(wx, wy, wz), key='wx3_stone', rot=(0, 0, f.rz), bev=0.05)
    # arrow slits spaced on the fixed rhythm (match wall/tower/gatehouse)
    for xx in [-L / 2 + 3.0 + i * 5.0 for i in range(max(1, int((L - 4) / 5.0)) + 1)]:
        if abs(xx) < L / 2 - 1.5:
            slit_stone(F(*f.p(0, -WT / 2, 0), f.rz), xx, 14.0, h=3.2)


# ============================================================ B02_05 curtain wall
def curtain_wall():
    reset()
    wall_profile(F(0, 0, 0, 0), 40.0, seed=5)
    return finalize('B02_05_curtain_wall', smooth_angle=30)


# ============================================================ B02_06 curtain corner
def curtain_corner():
    reset()
    arm = 16.0
    wall_profile(F(-arm / 2 - WT / 2, 0, 0, 0), arm, seed=6)
    wall_profile(F(0, -arm / 2 - WT / 2, 0, 90), arm, seed=7)
    cx, cy = -WT / 2, -WT / 2
    r = 7.5
    # round corner turret - uniform tone, course rings (no patches)
    lathe(nm('tp'), [(0.0, 0.0), (r + 1.0, 0.0), (r + 0.6, 2.4), (r, 4.0), (r, WH + 4.0), (0.0, WH + 4.0)],
          loc=(cx, cy, 0), key='wx3_stone', segs=28)
    ring_course_bands(cx, cy, r, 5.0, WH + 2.0, course=3.0)
    for zz in (8.0, 16.0, 24.0):
        lathe(nm('tb'), [(0.0, zz - 0.2), (r + 0.35, zz - 0.2), (r + 0.35, zz + 0.3), (0.0, zz + 0.3)],
              loc=(cx, cy, 0), key='wx3_trim', segs=28)
    for i in range(6):
        a = 60 * i
        fr = F(cx + math.cos(math.radians(a)) * r, cy + math.sin(math.radians(a)) * r, 0, a + 90)
        slit_stone(fr, 0, 14.0 + (4.0 if i % 2 else 0), h=3.0)
    ring_battlements(cx, cy, WH + 4.0, r, 'wx3_stone', t=1.1, mh=2.6, ph=1.6, cap='wx3_trim', machicolate=True)
    return finalize('B02_06_curtain_corner', smooth_angle=30)



# ============================================================ B02_02 round tower (uniform tone)
def round_tower():
    reset()
    r, H = 10.0, 80.0
    lathe(nm('pl'), [(0.0, 0.0), (r + 2.0, 0.0), (r + 1.2, 3.0), (r, 5.0), (r, H), (0.0, H)],
          loc=(0, 0, 0), key='wx3_stone', segs=30)
    ring_course_bands(0, 0, r, 6.0, H - 2.0, course=3.0)
    for zz in (18.0, 34.0, 50.0, 66.0):
        lathe(nm('rb'), [(0.0, zz - 0.2), (r + 0.4, zz - 0.2), (r + 0.4, zz + 0.3), (0.0, zz + 0.3)],
              loc=(0, 0, 0), key='wx3_trim', segs=30)
    for k in range(5):
        a = 60 * k + 15 * k
        zz = 16.0 + k * 12.0
        fr = F(math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r, 0, a + 90)
        arrow_slit(fr, 0, zz, h=3.2, key='wx3_stone')
    for i in range(3):
        a = 120 * i + 40
        fr = F(math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r, 0, a + 90)
        window(fr, 0, H - 14.0, w=2.0, h=3.6, arch=True, frame='wx3_trim', sill='wx3_trim', panes=False, lit=(i == 0))
    ring_battlements(0, 0, H, r, 'wx3_stone', t=1.2, mh=2.8, ph=1.8, cap='wx3_trim', machicolate=True)
    cone_roof(0, 0, H + 4.0, r - 0.6, 12.0, keys=('wx3_slate_a', 'wx3_slate_b'), rings=8, ov=0.8, finial='gold', flag='wx3_ban_r')
    return finalize('B02_02_round_tower', smooth_angle=30)


# ============================================================ B02_03 square tower (<=45k, tapered, buttresses)
def square_tower():
    reset()
    s0, s1, H = 20.0, 17.0, 76.0   # slight batter (taper) top to bottom
    # tapered body as a single lathe-like box stack (few segments = low tris)
    poly_prism(nm('t'), [(-s0 / 2, -s0 / 2), (s0 / 2, -s0 / 2), (s0 / 2, s0 / 2), (-s0 / 2, s0 / 2)], H,
               loc=(0, 0, 0), key='wx3_stone')
    box(nm('pl'), (s0 + 2.4, s0 + 2.4, 3.0), loc=(0, 0, 1.5), key='wx3_plinth', bev=0.1)
    # real corner buttresses (projecting), with weathered pinnacles - gives relief, not a plain box
    for sx in (-1, 1):
        for sy in (-1, 1):
            lbox(F(sx * (s0 / 2 + 0.6), sy * (s0 / 2 + 0.6), 0, 0), (2.8, 2.8, H - 5.0), 0, 0, (H - 5.0) / 2 + 3.0, 'wx3_warm')
            pinnacle(sx * (s0 / 2 + 0.6), sy * (s0 / 2 + 0.6), H - 3.0, s=1.5, h=6.0, key='wx3_trim', tip='wx3_trim')
    # flat faces: recessed course lines + sparse tall windows + arrow slits (no bevelled block grid)
    for fr, L in ((F(0, -s0 / 2, 0, 0), s0), (F(0, s0 / 2, 0, 180), s0), (F(-s0 / 2, 0, 0, -90), s0), (F(s0 / 2, 0, 0, 90), s0)):
        course_bands(fr, L - 4.0, 5.0, H - 6.0, y=0.0, course=3.2)
        for k in range(3):
            arrow_slit(fr, 0, 16.0 + k * 18.0, h=3.0, key='wx3_stone')
        window(fr, 0, H - 13.0, w=2.2, h=4.4, arch=True, frame='wx3_trim', sill='wx3_trim', panes=False, lit=False)
    for zz in (22.0, 44.0, 62.0):
        band(0, 0, s0, s0, zz, 0.6, 'wx3_trim', out=0.28)
    lbox(F(0, 0, 0, 0), (s0 - 1.0, s0 - 1.0, 1.0), 0, 0, H + 0.5, 'wx3_floor_a')
    for fr in (F(0, -s0 / 2 + 0.6, H + 1.0, 0), F(0, s0 / 2 - 0.6, H + 1.0, 180), F(-s0 / 2 + 0.6, 0, H + 1.0, -90), F(s0 / 2 - 0.6, 0, H + 1.0, 90)):
        corbels(F(*fr.p(0, 0, -2.0), fr.rz), -s0 / 2 + 1, s0 / 2 - 1, 0, 'wx3_stone', step=2.6, size=(0.7, 1.0, 1.0))
        battlements(fr, -s0 / 2 + 0.5, s0 / 2 - 0.5, 0, 'wx3_stone', t=1.1, mw=2.0, gap=1.4, mh=2.8, ph=1.8, cap='wx3_trim')
    cyl(nm('fp'), 0.26, 11.0, loc=(0, 0, H + 3.5), key='wx3_slate_d', verts=8)
    lbox(F(2.2, 0, 0, 0), (4.0, 0.12, 6.0), 0, 0, H + 8.0, 'wx3_ban_b')
    return finalize('B02_03_square_tower', smooth_angle=30)


# ============================================================ B02_04 spire tower (widened, uniform tone)
def spire_tower():
    reset()
    r, H = 9.5, 86.0   # widened from 7.5 -> 9.5 for a believable proportion
    lathe(nm('pl'), [(0.0, 0.0), (r + 1.8, 0.0), (r + 1.1, 2.4), (r, 4.0), (r, H), (0.0, H)],
          loc=(0, 0, 0), key='wx3_warm', segs=26)
    ring_course_bands(0, 0, r, 5.0, H - 4.0, course=3.0, key='wx3_warm_c')
    for zz in (16.0, 32.0, 48.0, 64.0, 78.0):
        lathe(nm('rb'), [(0.0, zz - 0.2), (r + 0.35, zz - 0.2), (r + 0.35, zz + 0.3), (0.0, zz + 0.3)],
              loc=(0, 0, 0), key='wx3_trim', segs=26)
    for k in range(6):
        a = 60 * k + 12 * k
        zz = 14.0 + k * 11.0
        fr = F(math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r, 0, a + 90)
        arrow_slit(fr, 0, zz, h=2.8, key='wx3_warm')
    for i in range(2):
        a = 180 * i + 60
        fr = F(math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r, 0, a + 90)
        window(fr, 0, H - 12.0, w=1.8, h=3.4, arch=True, frame='wx3_trim', sill='wx3_trim', panes=False, lit=(i == 0))
    ring_battlements(0, 0, H, r, 'wx3_warm', t=1.0, mh=2.2, ph=1.4, cap='wx3_trim', machicolate=True)
    cone_roof(0, 0, H + 3.4, r - 0.8, 24.0, keys=('wx3_slate_a', 'wx3_slate_d'), rings=11, ov=0.6, finial='gold', flag='wx3_ban_b')
    return finalize('B02_04_spire_tower', smooth_angle=30)


# ============================================================ B02_01 keep (<=45k, uniform tone)
def keep():
    reset()
    W, D, Hbody = 60.0, 50.0, 78.0
    box(nm('pl'), (W + 3.0, D + 3.0, 4.0), loc=(0, 0, 2.0), key='wx3_plinth', bev=0.15)
    box(nm('pl2'), (W + 1.5, D + 1.5, 3.0), loc=(0, 0, 5.0), key='wx3_plinth')
    box(nm('b'), (W, D, Hbody), loc=(0, 0, Hbody / 2 + 6.0), key='wx3_warm')
    # flat faces with recessed course lines (NOT a bevelled block grid) -> far fewer tris, uniform tone
    for fr, L in ((F(0, -D / 2, 6.0, 0), W), (F(0, D / 2, 6.0, 180), W), (F(-W / 2, 0, 6.0, -90), D), (F(W / 2, 0, 6.0, 90), D)):
        course_bands(fr, L - 4.0, 8.0, Hbody - 2.0, y=0.0, course=6.0)
    # sparse quoins at the body corners
    for (cx, cy, rz) in ((-W / 2, -D / 2, 0), (W / 2, -D / 2, 0), (-W / 2, D / 2, 180), (W / 2, D / 2, 180)):
        quoins(F(cx, cy, 8.0, rz), 0, Hbody - 10.0, 'wx3_trim', sizes=(2.2, 1.2), course=6.0, t=0.18)
    for zz in (24.0, 42.0, 60.0):
        band(0, 0, W, D, zz, 0.7, 'wx3_trim', out=0.3)
    # great hall projection on the front with tall arched windows
    ghw, ghd, ghh = 26.0, 10.0, 34.0
    box(nm('gh'), (ghw, ghd, ghh), loc=(0, -D / 2 - ghd / 2, ghh / 2 + 6.0), key='wx3_warm')
    ghf = F(0, -D / 2 - ghd, 6.0, 0)
    for i in range(3):
        window(ghf, -ghw / 2 + 5.0 + i * 8.0, 10.0, w=3.4, h=14.0, arch=True, frame='wx3_trim', sill='wx3_trim', keystone='wx3_trim', lit=(i == 1))
    fbw = 10.0
    for i in range(8):
        box(nm('st'), (fbw, 2.0, 2.0), loc=(ghw / 2 + 4.0, -D / 2 - ghd - 1.5 - i * 1.8, 1.0 + i * 2.0), key='wx3_plinth', bev=0.04)
    box(nm('fbw'), (3.0, 16.0, 18.0), loc=(ghw / 2 + 4.0 + fbw / 2 + 1.0, -D / 2 - ghd - 8.0, 9.0 + 6.0), key='wx3_warm')
    door(F(ghw / 2 + 4.0, -D / 2 - ghd, 6.0 + 16.0, 0), 0, w=4.0, h=7.0, arch=True, surround='wx3_trim', step='wx3_plinth')
    v4util.marker('mk_door', (ghw / 2 + 4.0, -D / 2 - ghd - 0.3, 6.0 + 16.0))
    # sparser windows on the other faces
    fc = faces(0, 0, W, D, 6.0)
    for side in ('back', 'left', 'right'):
        fr = fc[side]
        LL = W if side == 'back' else D
        for zx in [-LL / 2 + 11 + i * 16 for i in range(max(1, int((LL - 14) / 16)) + 1)]:
            if abs(zx) < LL / 2 - 5:
                window(fr, zx, 40.0, w=2.4, h=4.6, arch=False, frame='wx3_trim', sill='wx3_trim', panes=False, lit=(zx == 0))
    # corner turrets (uniform tone, course rings)
    top = Hbody + 6.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            tx, ty, r = sx * (W / 2 - 1.0), sy * (D / 2 - 1.0), 6.5
            lathe(nm('ct'), [(0.0, 20.0), (r + 1.0, 20.0), (r, 23.0), (r, top + 10.0), (0.0, top + 10.0)], loc=(tx, ty, 0), key='wx3_warm', segs=18)
            ring_course_bands(tx, ty, r, 26.0, top + 8.0, course=7.0, key='wx3_warm_c', segs=16)
            for i in range(4):
                a = 90 * i + 45
                fr = F(tx + math.cos(math.radians(a)) * r, ty + math.sin(math.radians(a)) * r, 0, a + 90)
                arrow_slit(fr, 0, top - 14.0, h=3.0, key='wx3_warm')
            ring_battlements(tx, ty, top + 10.0, r, 'wx3_warm', t=1.0, mh=2.4, ph=1.5, cap='wx3_trim', machicolate=False)
            cone_roof(tx, ty, top + 10.0 + 3.4, r - 0.5, 10.0, keys=('wx3_slate_a', 'wx3_slate_b'), rings=4, ov=0.6, finial='gold', segs=18,
                      flag=('wx3_ban_r' if (sx * sy > 0) else 'wx3_ban_b'))
    lbox(F(0, 0, 0, 0), (W - 2.0, D - 2.0, 1.0), 0, 0, top + 0.5, 'wx3_floor_a')
    for fr in (F(0, -D / 2 + 0.6, top + 1.0, 0), F(0, D / 2 - 0.6, top + 1.0, 180)):
        corbels(F(*fr.p(0, 0, -2.0), fr.rz), -W / 2 + 2, W / 2 - 2, 0, 'wx3_warm', step=2.8, size=(0.8, 1.1, 1.2))
        battlements(fr, -W / 2 + 1, W / 2 - 1, 0, 'wx3_warm', t=1.2, mw=2.2, gap=1.5, mh=3.0, ph=2.0, cap='wx3_trim')
    for fr in (F(-W / 2 + 0.6, 0, top + 1.0, -90), F(W / 2 - 0.6, 0, top + 1.0, 90)):
        battlements(fr, -D / 2 + 1, D / 2 - 1, 0, 'wx3_warm', t=1.2, mw=2.2, gap=1.5, mh=3.0, ph=2.0, cap='wx3_trim')
    return finalize('B02_01_keep', smooth_angle=30)


# ============================================================ B02_07 gatehouse (<=45k, uniform tone)
def gatehouse():
    reset()
    arm = 16.0
    passage_w, passage_h = 12.0, 18.0
    cb_w = passage_w + 2 * 7.0
    cb_d = 20.0
    box(nm('cb'), (cb_w, cb_d, WH + 6.0), loc=(0, 0, (WH + 6.0) / 2), key='wx3_stone')
    box(nm('cbp'), (cb_w + 1.0, cb_d + 1.0, 2.6), loc=(0, 0, 1.3), key='wx3_plinth', bev=0.08)
    # flat faces + recessed course lines (no block grid)
    for fr, L in ((F(0, -cb_d / 2, 0, 0), cb_w), (F(0, cb_d / 2, 0, 180), cb_w),
                  (F(-cb_w / 2, 0, 0, -90), cb_d), (F(cb_w / 2, 0, 0, 90), cb_d)):
        course_bands(fr, L - 3.0, 4.0, WH - 2.0, y=0.0, course=3.0)
    # passage void + arches
    lbox(F(0, 0, 0, 0), (passage_w, cb_d + 0.6, passage_h), 0, 0, passage_h / 2, 'hole')
    for sgn in (-1, 1):
        fr = F(0, sgn * cb_d / 2, 0, 0 if sgn < 0 else 180)
        half_disc(fr, 0, passage_h - passage_w / 2, passage_w / 2, 0.0, 1.2, 'wx3_stone')
        tube(nm('ga'), arc_pts(fr, 0, passage_h - passage_w / 2, passage_w / 2 + 0.6, y=-0.3, n=13), 0.6, 'wx3_trim', res=4)
        lbox(fr, (2.0, 1.0, 2.2), 0, -0.4, passage_h + 0.6, 'wx3_trim', bev=0.06)
        for s in (-1, 1):
            lbox(fr, (0.5, 0.6, passage_h), s * (passage_w / 2 - 0.1), -0.9, passage_h / 2, 'wx3_slate_d')
    frf = F(0, -cb_d / 2, 0, 0)
    for i in range(7):
        xx = -passage_w / 2 + 0.6 + (passage_w - 1.2) * i / 6
        lbox(frf, (0.3, 0.3, passage_h * 0.55), xx, -0.8, passage_h * 0.72, 'wx3_slate_d')
    for j in range(3):
        lbox(frf, (passage_w - 1.0, 0.3, 0.3), 0, -0.8, passage_h * 0.55 + j * passage_h * 0.22, 'wx3_slate_d')
    # walkway + crenellated parapet
    lbox(F(0, 0, 0, 0), (cb_w, cb_d - 1.5, 1.0), 0, 0, WH + 6.0 + 0.5, 'wx3_floor_a')
    corbels(F(0, -cb_d / 2, 0, 0), -cb_w / 2 + 1, cb_w / 2 - 1, WH + 5.0, 'wx3_stone', step=2.6, size=(0.7, 1.0, 1.1))
    battlements(F(0, -cb_d / 2 + 0.6, WH + 7.0, 0), -cb_w / 2, cb_w / 2, 0, 'wx3_stone', t=1.1, mw=2.0, gap=1.4, mh=2.6, ph=1.6, cap='wx3_trim')
    battlements(F(0, cb_d / 2 - 0.6, WH + 7.0, 180), -cb_w / 2, cb_w / 2, 0, 'wx3_stone', t=1.1, mw=2.0, gap=1.4, mh=2.6, ph=1.6, cap='wx3_trim')
    # flanking round towers (uniform, course rings)
    for s in (-1, 1):
        tx = s * (cb_w / 2 - 1.0)
        r = 6.0
        lathe(nm('ft'), [(0.0, 0.0), (r + 0.8, 0.0), (r, 3.0), (r, WH + 12.0), (0.0, WH + 12.0)], loc=(tx, 0, 0), key='wx3_warm', segs=20)
        ring_course_bands(tx, 0, r, 6.0, WH + 10.0, course=4.0, key='wx3_warm_c', segs=20)
        for i in range(5):
            a = 72 * i - 20
            fr = F(tx + math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r, 0, a + 90)
            arrow_slit(fr, 0, 16.0 + (6.0 if i % 2 else 0), h=3.0, key='wx3_warm')
        ring_battlements(tx, 0, WH + 12.0, r, 'wx3_warm', t=1.0, mh=2.4, ph=1.5, cap='wx3_trim', machicolate=True)
        cone_roof(tx, 0, WH + 12.0 + 3.6, r - 0.4, 9.0, keys=('wx3_slate_a', 'wx3_slate_b'), rings=7, ov=0.7, finial='gold', flag='wx3_ban_r')
    wall_profile(F(-cb_w / 2 - arm / 2, 0, 0, 0), arm, seed=70, quoin_ends=False)
    wall_profile(F(cb_w / 2 + arm / 2, 0, 0, 0), arm, seed=71, quoin_ends=False)
    v4util.marker('mk_door', (0, -cb_d / 2 - 0.4, 0.2))
    return finalize('B02_07_gatehouse', smooth_angle=30)



# ============================================================ B03_01 throne hall (muted glass, stone floor, roof)
def _stone_floor(W, D, z=0.0, tile=6.0):
    """Quiet two-tone slab floor (large slabs, low contrast) - not a toy checkerboard."""
    nx = max(2, int(W / tile)); ny = max(2, int(D / tile))
    sx, sy = W / nx, D / ny
    for i in range(nx):
        for j in range(ny):
            k = 'wx3_floor_a' if (i + j) % 2 == 0 else 'wx3_floor_b'
            box(nm('ft'), (sx - 0.1, sy - 0.1, 0.3), loc=(-W / 2 + sx * (i + 0.5), -D / 2 + sy * (j + 0.5), z + 0.15), key=k)
    box(nm('fb'), (W + 0.6, D + 0.6, 0.25), loc=(0, 0, z - 0.1), key='wx3_plinth')


def _carpet(x0, x1, y, w=7.0, z=0.32):
    L = x1 - x0
    box(nm('cp'), (w, L, 0.14), loc=(y, (x0 + x1) / 2, z), key='wx3_glass_wn')  # runs along Y (hall length), width w along X
    for s in (-1, 1):
        box(nm('cpt'), (0.5, L, 0.16), loc=(y + s * (w / 2 - 0.3), (x0 + x1) / 2, z + 0.01), key='wx3_glass_oc')


def throne_hall():
    reset()
    W, D, H = 48.0, 80.0, 30.0
    _stone_floor(W, D, 0.0, tile=6.0)
    _carpet(-D / 2 + 3.0, D / 2 - 16.0, 0.0, w=7.0)
    # outer walls (now enclosed so the roof reads) with recessed courses + buttresses between bays
    wt = 1.8
    for s in (-1, 1):
        lbox(F(s * (W / 2), 0, 0, 0), (wt, D, H), 0, 0, H / 2, 'wx3_stone')
        # thin darker course lines on the inner face, placed directly in world space (runs along Y)
        z = 4.0
        while z < H - 2.0:
            box(nm('wc'), (0.14, D - 0.4, 0.3), loc=(s * (W / 2 - wt / 2), 0, z), key='wx3_course')
            z += 3.4
    lbox(F(0, D / 2, 0, 0), (W, wt, H), 0, 0, H / 2, 'wx3_stone')   # back wall behind the dais
    px, zcap = W / 2 - 5.0, H - 3.0
    pillar_ys = [-D / 2 + 10.0 + i * (D - 28.0) / 4 for i in range(5)]
    glass = ['wx3_glass_in', 'wx3_glass_wn', 'wx3_glass_fg', 'wx3_glass_oc']
    for s in (-1, 1):
        for py in pillar_ys:
            column_c(s * px, py, 0.0, zcap, 1.5, key='wx3_stone', base='wx3_trim')
            box(nm('pb'), (4.2, 4.2, 1.0), loc=(s * px, py, 0.5), key='wx3_plinth', bev=0.06)
        lbeam(F(), (s * px, pillar_ys[0], zcap), (s * px, pillar_ys[-1], zcap), 1.0, 'wx3_trim')
        # muted stained-glass bays in the outer wall between pillars + banners
        for j in range(len(pillar_ys) - 1):
            my = (pillar_ys[j] + pillar_ys[j + 1]) / 2
            fr = F(s * (W / 2 - 0.4), my, 0, -90 if s < 0 else 90)
            w2, zb, h2 = 5.0, 6.0, 15.0
            zs = zb + h2 - w2 * 0.6
            lbox(fr, (w2, 0.3, zs - zb), 0, -0.1, (zb + zs) / 2, glass[j % 4])
            half_disc(fr, 0, zs, w2 / 2, 0.0, 0.3, glass[(j + 1) % 4])
            for xx in (-w2 / 3, 0, w2 / 3):
                lbox(fr, (0.2, 0.34, zs - zb + 1.0), xx, -0.12, (zb + zs) / 2, 'wx3_trim')
            tube(nm('wa'), arc_pts(fr, 0, zs, w2 / 2 + 0.2, y=-0.2, n=11), 0.28, 'wx3_trim', res=4)
            lbox(fr, (w2 + 1.0, 0.5, 0.5), 0, -0.2, zb - 0.2, 'wx3_trim')
            # hanging banner on the inner face between the pillars
            bk = ['wx3_ban_r', 'wx3_ban_b', 'wx3_glass_fg', 'wx3_ban_r'][j % 4]
            fb = F(s * (W / 2 - 1.2), my, zcap - 1.0, -90 if s < 0 else 90)
            lslab(fb, [(-1.7, 0.0, 0), (1.7, 0.0, 0), (1.7, -0.12, -9.0), (0.6, -0.12, -10.0),
                       (-0.6, -0.12, -10.0), (-1.7, -0.12, -9.0)], (0, -0.14, 0), bk)
    # ---- ROOF: gabled timber-and-slate roof over the hall (fixes the roofless defect) ----
    ridge = H + 10.0
    for s in (-1, 1):
        # two slate roof planes
        nrows = 8
        for r in range(nrows):
            t = (r + 0.5) / nrows
            yy = s * (W / 2 + 0.6) * (1 - t)
            zz = H + (ridge - H) * t
            box(nm('rf'), (1.6, D + 2.0, 0.4), loc=(yy, 0, zz), key=('wx3_slate_a' if r % 2 else 'wx3_slate_b'),
                rot=(0, s * 52, 0), bev=0.0)
    # gable end walls filling the triangle at both ends
    for sy in (-1, 1):
        for r in range(6):
            t = r / 6
            hw = (W / 2) * (1 - t)
            box(nm('gb'), (2 * hw, 1.2, (ridge - H) / 6 + 0.3), loc=(0, sy * (D / 2 + 0.3), H + (ridge - H) * (t + 0.5 / 6)), key='wx3_stone')
    box(nm('ridge'), (1.2, D + 2.0, 1.0), loc=(0, 0, ridge), key='wx3_slate_d', bev=0.1)
    # ---- dais + steps + throne (kept), muted tones ----
    dy = D / 2 - 10.0
    for k in range(4):
        box(nm('ds'), (24.0 - k * 3.0, 3.0, 1.0), loc=(0, dy - 6.0 + k * 3.0, 0.5 + k * 1.0), key='wx3_floor_b' if k % 2 else 'wx3_trim', bev=0.05)
    dz = 4.0
    box(nm('dtop'), (22.0, 10.0, 0.6), loc=(0, dy + 1.0, dz + 0.3), key='wx3_floor_a')
    tx, ty = 0.0, dy + 2.0
    box(nm('thb'), (5.0, 3.6, 1.0), loc=(tx, ty, dz + 0.5), key='wx3_stone', bev=0.05)
    box(nm('ths'), (4.4, 3.0, 0.5), loc=(tx, ty, dz + 1.25), key='wx3_glass_wn')
    box(nm('thback'), (4.4, 0.6, 7.0), loc=(tx, ty + 1.5, dz + 4.5), key='wx3_warm_c')
    box(nm('thbp'), (4.8, 0.7, 0.8), loc=(tx, ty + 1.5, dz + 8.2), key='wx3_trim', bev=0.05)
    for s in (-1, 1):
        box(nm('tharm'), (0.5, 3.0, 2.0), loc=(tx + s * 2.2, ty, dz + 2.5), key='wx3_warm_c')
        cyl(nm('cnp'), 0.3, 11.0, loc=(tx + s * 3.4, ty + 1.2, dz + 1.0), key='wx3_trim', verts=10)
    box(nm('cnt'), (9.0, 4.0, 0.5), loc=(tx, ty + 0.6, dz + 12.2), key='wx3_warm_c')
    lslab(F(tx, ty - 2.0, dz + 12.0, 0), [(-4.5, 0, 0), (4.5, 0, 0), (4.5, 0, -2.0), (0, 0, -3.4), (-4.5, 0, -2.0)], (0, 3.6, 0), 'wx3_ban_r')
    ball(nm('cfin'), 0.5, loc=(tx, ty + 0.6, dz + 12.7), key='wx3_trim', segs=10, rings=7)
    v4util.marker('mk_door', F(0, -D / 2, 0, 0).p(0, -0.1, 0.1))
    return finalize('throne_hall', smooth_angle=30)


# ============================================================ B06_03 stall potion (muted bottles)
def stall_potion():
    """Copied from v4_we2_castle.stall_potion; potion liquids desaturated (no neon magenta/lime)."""
    from v4_we2_castle import _stall_base
    reset()
    rnd, L, D, Hc = _stall_base(63, 'we2_canopy_gr', 'we2_canopy_gd', shape='round')
    cols = ['wx3_pot_r', 'wx3_pot_b', 'wx3_pot_g', 'wx3_pot_p']

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
    cyl(nm('caul'), 1.05, 0.06, loc=(3.6, -D / 2 + 1.2, Hc + 1.5), key='wx3_pot_g', verts=16)
    for k in range(3):
        ball(nm('bub'), 0.2 - k * 0.04, loc=(3.6 + (k - 1) * 0.3, -D / 2 + 1.2, Hc + 1.6 + k * 0.2), key='wx3_pot_g', segs=6, rings=4)
    for x in (-4.5, -3.8):
        for k in range(3):
            tube(nm('hb'), [(x + k * 0.2, -D / 2 + 0.4, 8.4), (x + k * 0.2, -D / 2 + 0.4, 7.2)], 0.03, 'we2_rope', res=4)
            ball(nm('hbl'), 0.2, loc=(x + k * 0.2, -D / 2 + 0.4, 7.0), key='we2_cloth_c', segs=6, rings=4, scale=(0.6, 0.6, 1.4))
    return finalize('stall_potion', smooth_angle=30)


BATCHES = {
    'cwall':  ('v4_castle', [('B02_05_curtain_wall', curtain_wall, (0.7, -1.3, 0.4)),
                             ('B02_06_curtain_corner', curtain_corner, (1.0, -1.1, 0.4))]),
    'towers': ('v4_castle', [('B02_03_square_tower', square_tower, (1.0, -1.1, 0.35)),
                             ('B02_02_round_tower', round_tower, (1.0, -1.1, 0.35)),
                             ('B02_04_spire_tower', spire_tower, (1.0, -1.1, 0.4))]),
    'throne': ('v4_castle', [('B03_01_throne_hall_01', throne_hall, (0.9, -1.1, 0.4))]),
    'big':    ('v4_castle', [('B02_01_keep', keep, (1.0, -1.3, 0.4)),
                             ('B02_07_gatehouse', gatehouse, (0.6, -1.3, 0.35))]),
    'stall':  ('v4_castle', [('B06_03_stall_potion', stall_potion, (0.6, -1.2, 0.4))]),
}
