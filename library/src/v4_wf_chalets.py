"""v4_wf_chalets - C01: six distinct alpine chalets (wf).
Front faces -Y. 1 unit = 1 stud. Deep soft snow, overhanging eaves, varied icicles, warm glowing windows.
Each has a `door` marker at the threshold (not enterable). Reuses alpine.snow_roof / heart_shutters / carved_rail
and arch/kitlib helpers; improves on the flat parts of the older E-series. New palette keys use the wf_ prefix.
"""
import math, random
from mathutils import Vector
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, top_paint
from arch import F, faces, lbox, lbeam, beam3, slab, lslab, window, door, gable_roof, roof_z, cone_roof, chimney, nm
from capital import stone_face
from alpine import snow_roof, logs_face, carved_rail, heart_shutters, SH
from nature import blob, rock

# ---- winter palette additions (wf_ prefix; reuse base snow/ice/glass/glass_lit/wood/stone where they fit) ----
kitlib.PAL.setdefault('wf_timber',      ((96, 66, 44),   'Wood',       0.0, 0.85, 0))
kitlib.PAL.setdefault('wf_timber_dark', ((64, 44, 30),   'Wood',       0.0, 0.90, 0))
kitlib.PAL.setdefault('wf_plank',       ((140, 104, 68), 'WoodPlanks', 0.0, 0.80, 0))
kitlib.PAL.setdefault('wf_plank_light', ((176, 140, 96), 'WoodPlanks', 0.0, 0.78, 0))
kitlib.PAL.setdefault('wf_stone',       ((150, 146, 140),'Cobblestone',0.0, 0.92, 0))
kitlib.PAL.setdefault('wf_stone_dark',  ((112, 108, 104),'Slate',      0.0, 0.92, 0))
kitlib.PAL.setdefault('wf_shingle_a',   ((92, 72, 58),   'Slate',      0.0, 0.88, 0))
kitlib.PAL.setdefault('wf_shingle_b',   ((74, 58, 48),   'Slate',      0.0, 0.90, 0))
kitlib.PAL.setdefault('wf_shutter_g',   ((58, 96, 74),   'WoodPlanks', 0.0, 0.80, 0))
kitlib.PAL.setdefault('wf_shutter_r',   ((138, 58, 48),  'WoodPlanks', 0.0, 0.80, 0))
kitlib.PAL.setdefault('wf_shutter_b',   ((60, 86, 122),  'WoodPlanks', 0.0, 0.80, 0))
kitlib.PAL.setdefault('wf_glow',        ((248, 196, 112),'Glass',      0.0, 0.20, 0.5))
kitlib.PAL.setdefault('wf_turf',        ((96, 116, 70),  'Grass',      0.0, 1.0, 0))
kitlib.PAL.setdefault('wf_turf_snow',   ((206, 216, 210),'Grass',      0.0, 0.8, 0))

SNOW = 'snow'
ICE = 'glass'          # base translucent glass reads as clear ice for icicles
RSH = ('wf_shingle_a', 'wf_shingle_b')


# ---------------------------------------------------------------- shared detail helpers
def snow_cap_box(cx, cy, w, d, z, key=SNOW, bev=0.3, seed=0):
    """Soft rounded snow pillow sitting on a flat top (sill, beam, chimney cap)."""
    box(nm('scap'), (w, d, 0.55), loc=(cx, cy, z + 0.2), key=key, bev=bev)


def icicle_row(f, x0, x1, y, z, n=None, lo=0.4, hi=1.6, seed=0, prob=0.72):
    """A row of clear icicles of varied length hanging from an eave/ledge at local (x,z), outward at y."""
    rnd = random.Random(seed)
    n = n or max(3, int((x1 - x0) / 0.8))
    for i in range(n):
        if rnd.random() > prob:
            continue
        x = x0 + (x1 - x0) * i / max(1, n - 1)
        h = rnd.uniform(lo, hi)
        r = rnd.uniform(0.09, 0.17)
        lathe(nm('ic'), [(0, 0), (r, 0), (r * 0.55, -h * 0.45), (0, -h)], loc=f.p(x, y, z), key=ICE, segs=5)


def lit_window(f, x, z, w=2.0, h=3.0, shutter='wf_shutter_g', sill='wf_timber_dark', frame='wf_plank_light',
               hearts=True, glow=True, ledge_snow=True, seed=0):
    """Deep-set glowing shuttered window with a timber frame, snow on the sill and small icicles under it."""
    g = 'wf_glow' if glow else 'glass_dark'
    lbox(f, (w, 0.12, h), x, 0.0, z + h / 2, g)                       # glass pane, recessed
    lbox(f, (0.1, 0.2, h), x, -0.1, z + h / 2, frame)                 # mullion
    lbox(f, (w, 0.2, 0.1), x, -0.1, z + h * 0.6, frame)
    for s in (-1, 1):                                                 # frame posts
        lbox(f, (0.24, 0.26, h + 0.1), x + s * (w / 2 + 0.08), -0.12, z + h / 2, frame)
    lbox(f, (w + 0.5, 0.28, 0.22), x, -0.14, z + h + 0.1, frame)      # lintel
    lbox(f, (w + 0.8, 0.5, 0.2), x, -0.26, z - 0.08, sill, bev=0.04)  # sill
    if shutter:
        heart_shutters(f, x, z, w, h, shutter) if hearts else None
        if not hearts:
            for s in (-1, 1):
                lbox(f, (w / 2 + 0.06, 0.12, h), x + s * (w / 2 + 0.3 + w / 4), -0.08, z + h / 2, shutter)
    if ledge_snow:
        snow_cap_box(*f.p(x, -0.3, 0)[:2], w + 0.9, 0.7, z - 0.18, seed=seed)
        icicle_row(f, x - w / 2, x + w / 2, -0.35, z - 0.2, lo=0.3, hi=0.9, seed=seed + 1, prob=0.6)


def stone_base(cx, cy, w, d, h, key='wf_stone', dark='wf_stone_dark', seed=0):
    """Rubble-stone ground storey with slightly proud blocks and a plinth."""
    box(nm('sb'), (w, d, h), loc=(cx, cy, h / 2), key=key)
    box(nm('pl'), (w + 0.5, d + 0.5, 0.7), loc=(cx, cy, 0.35), key=dark, bev=0.06)
    for k, fr in enumerate(faces(cx, cy, w, d).values()):
        stone_face(fr, -w / 2 + 1, w / 2 - 1, 0.6, h - 0.5, int((w + d) * 0.6), seed + k, keys=(key, dark, 'wf_stone'))


def log_storey(cx, cy, w, d, z0, h, key='wf_timber', alt='wf_plank', corner=True):
    """Stacked-log upper storey: horizontal log courses on all four faces, with crossed corner ends."""
    box(nm('lg'), (w, d, h), loc=(cx, cy, z0 + h / 2), key=key)
    for side, L in (('front', w), ('back', w), ('left', d), ('right', d)):
        fr = faces(cx, cy, w, d, z0)[side]
        logs_face(fr, L, 0.1, h - 0.1, key=(key if side in ('front', 'back') else alt), step=0.95)
    if corner:
        for sx in (-1, 1):
            for sy in (-1, 1):
                nlog = int(h / 0.95)
                for i in range(nlog):
                    for ax in (0, 1):
                        ln = 1.3
                        if ax == 0:
                            box(nm('ce'), (ln, 0.5, 0.42), loc=(cx + sx * (w / 2 + 0.2), sy * (d / 2 + 0.1), z0 + 0.5 + i * 0.95), key='wf_timber_dark', bev=0.05)
                        else:
                            box(nm('ce'), (0.5, ln, 0.42), loc=(cx + sx * (w / 2 + 0.1), sy * (d / 2 + 0.2), z0 + 0.95 + i * 0.95), key='wf_timber_dark', bev=0.05)


def chimney_snow(x, y, zb, zt, w=2.0, key='wf_stone'):
    chimney(x, y, zb, zt, w=w, key=key)
    snow_cap_box(x, y, w + 0.6, w + 0.6, zt + 0.1, seed=int(x + y))
    icicle_row(F(x, y - (w / 2 + 0.3), 0, 0), -w / 2, w / 2, 0, zt - 0.3, lo=0.3, hi=0.8, seed=int(x))


def ground_snow(cx, cy, w, d, seed=0, extra=10):
    """Soft snow drifts banked against the walls and scattered on the ground."""
    rnd = random.Random(seed)
    for i in range(extra):
        side = rnd.choice(('front', 'back', 'left', 'right'))
        if side in ('front', 'back'):
            x = cx + rnd.uniform(-w / 2, w / 2); y = cy + (d / 2 + 0.6) * (1 if side == 'back' else -1)
            sc = (1.7, 0.9, 0.42)
        else:
            y = cy + rnd.uniform(-d / 2, d / 2); x = cx + (w / 2 + 0.6) * (1 if side == 'right' else -1)
            sc = (0.9, 1.7, 0.42)
        blob(nm('sd'), rnd.uniform(1.0, 1.8), (x, y, 0.0), SNOW, subdiv=2, amp=0.1, scale=sc, seed=seed + i)


def door_timber(f, x, w=3.4, h=6.6, key='wf_timber_dark', surround='wf_timber', step='wf_stone_dark', seed=0):
    """Planked timber door with iron straps, stone step with snow, and a small gable canopy with icicles."""
    lbox(f, (w, 0.22, h), x, 0.0, h / 2, key)
    nplank = int(w / 0.7)
    for i in range(nplank):
        lbox(f, (w / nplank - 0.05, 0.08, h - 0.2), x - w / 2 + w * (i + 0.5) / nplank, -0.14, h / 2, 'wf_timber')
    for zz in (h * 0.22, h * 0.78):
        lbox(f, (w * 0.86, 0.06, 0.16), x, -0.2, zz, 'iron')
        for k in range(4):
            ball(nm('st'), 0.07, loc=f.p(x - w * 0.36 + k * w * 0.24, -0.24, zz), key='iron', segs=6, rings=4)
    torus(nm('ring'), 0.2, 0.05, loc=f.p(x + w * 0.28, -0.24, h * 0.48), key='brass', segs=12, rsegs=4, rot=f.r(90, 0, 0))
    for s in (-1, 1):
        lbox(f, (0.5, 0.42, h + 0.2), x + s * (w / 2 + 0.26), -0.18, h / 2, surround, bev=0.05)
    lbox(f, (w + 1.3, 0.46, 0.5), x, -0.2, h + 0.25, surround, bev=0.05)
    if step:
        lbox(f, (w + 1.6, 1.3, 0.5), x, -0.65, 0.25, step, bev=0.06)
        snow_cap_box(*f.p(x, -0.65, 0)[:2], w + 1.2, 1.1, 0.45, seed=seed)
    # little entrance canopy
    cz = h + 0.6
    for s in (-1, 1):
        lbeam(f, (x + s * (w / 2 + 0.3), -0.1, cz - 1.2), (x + s * (w / 2 + 0.3), -1.6, cz), 0.18, 'wf_timber')
    lbox(f, (w + 1.8, 1.9, 0.22), x, -0.9, cz, 'wf_plank', rot=(-20, 0, 0))
    snow_cap_box(*f.p(x, -0.9, 0)[:2], w + 1.9, 2.0, cz + 0.2, bev=0.22, seed=seed + 2)
    icicle_row(f, x - w / 2 - 0.4, x + w / 2 + 0.4, -1.7, cz - 0.35, lo=0.4, hi=1.2, seed=seed + 3, prob=0.7)


# ================================================================ C01_01 classic timber chalet
def chalet_01():
    """Classic alpine chalet: stone base, log upper floor, wide overhanging gable, carved balcony, deep snow roof."""
    reset()
    rnd = random.Random(1001)
    w, d, sh, uh = 22.0, 18.0, 6.5, 8.0
    stone_base(0, 0, w, d, sh, seed=1)
    log_storey(0, 0, w, d, sh, uh)
    top = sh + uh
    # front windows (glowing), door
    fo = faces(0, 0, w, d)['front']
    fu = faces(0, 0, w, d, sh)['front']
    door_timber(fo, -w / 4, seed=1)
    lit_window(fo, w / 4, 2.2, 2.2, 2.8, shutter='wf_shutter_g', seed=2)
    for x in (-w / 4, w / 4):
        lit_window(fu, x, 1.8, 2.4, 3.4, shutter='wf_shutter_g', seed=3 + int(x))
    for side in ('back', 'left', 'right'):
        L = w if side == 'back' else d
        fr = faces(0, 0, w, d, sh)[side]
        for x in ((-L / 4, L / 4) if L > 14 else (0,)):
            lit_window(fr, x, 1.8, 2.0, 3.0, shutter='wf_shutter_g', glow=(rnd.random() < 0.4), hearts=False, seed=10 + int(x))
    # gable roof + deep snow + icicles (wide overhang)
    fr = F(0, 0, 0, 90)
    hr = w * 0.4
    gable_roof(fr, d, w, top, hr, keys=RSH, wall='wf_timber', ov=3.0, ovg=2.6, barge='wf_timber_dark')
    snow_roof(fr, d, w, top, hr, ov=3.0, ovg=2.6, seed=1)
    # gable-end decorative truss + glowing loft window
    for side in ('front', 'back'):
        fg = faces(0, 0, w, d, top)[side]
        lbeam(fg, (0, -0.2, 0.2), (0, -0.2, hr - 0.4), 0.35, 'wf_timber')
        for s in (-1, 1):
            lbeam(fg, (s * w * 0.42, -0.2, 0.2), (0, -0.2, hr * 0.78), 0.3, 'wf_timber')
        lit_window(fg, 0, 1.2, 1.8, 2.3, shutter='wf_shutter_g', glow=(side == 'front'), ledge_snow=False, seed=20)
    # carved balcony across the front at the storey line
    fb = faces(0, 0, w, d, sh)['front']
    lbox(fb, (w + 1.4, 2.8, 0.4), 0, -1.4, 0.0, 'wf_timber_dark')
    for x in (-w / 2, -w / 6, w / 6, w / 2):
        lbeam(fb, (x, -0.1, -2.2), (x, -2.6, -0.2), 0.35, 'wf_timber')
    carved_rail(fb, -w / 2 - 0.5, w / 2 + 0.5, 0.2, -2.7, key='wf_plank_light')
    snow_cap_box(0, -(d / 2 + 2.6), w + 1.0, 0.5, 2.5, seed=4)
    chimney_snow(-w / 4, d * 0.22, top, top + hr + 2.6, w=2.0)
    ground_snow(0, 0, w, d, seed=1)
    kitlib.v4util_marker = None
    import v4util as U
    U.marker('mk_door', (-w / 4, -d / 2 - 0.4, 0.4))
    return finalize('C01_01_chalet_01', smooth_angle=30)


# ================================================================ C01_02 stone+timber, big chimney
def chalet_02():
    """Stone ground floor with a timber upper floor, steep roof and a big external stone chimney."""
    reset()
    rnd = random.Random(1002)
    import v4util as U
    w, d, sh, uh = 20.0, 18.0, 8.5, 7.5
    stone_base(0, 0, w, d, sh, seed=5)
    # timber (plank + exposed frame) upper storey
    box(nm('up'), (w, d, uh), loc=(0, 0, sh + uh / 2), key='plaster')
    fu = faces(0, 0, w, d, sh)
    for side, L in (('front', w), ('back', w), ('left', d), ('right', d)):
        fr = fu[side]
        # exposed timber frame
        posts = [-L / 2 + 0.3, -L / 6, L / 6, L / 2 - 0.3]
        lbox(fr, (L, 0.4, 0.4), 0, -0.2, 0.3, 'wf_timber_dark')
        lbox(fr, (L, 0.4, 0.4), 0, -0.2, uh - 0.3, 'wf_timber_dark')
        for px in posts:
            lbox(fr, (0.4, 0.4, uh), px, -0.2, uh / 2, 'wf_timber_dark')
        for a, b in zip(posts, posts[1:]):
            lbeam(fr, (a + 0.2, -0.2, 0.5), ((a + b) / 2, -0.2, uh * 0.5), 0.3, 'wf_timber_dark')
            lbeam(fr, (b - 0.2, -0.2, 0.5), ((a + b) / 2, -0.2, uh * 0.5), 0.3, 'wf_timber_dark')
    door_timber(fu['front'].sub(0, 0, -sh), 0, seed=5) if False else None
    door_timber(faces(0, 0, w, d)['front'], w / 4, seed=5)
    lit_window(faces(0, 0, w, d)['front'], -w / 4, 2.4, 2.2, 3.0, shutter='wf_shutter_r', seed=6)
    for x in (-w / 3, w / 3):
        lit_window(fu['front'], x, 1.8, 2.0, 3.2, shutter='wf_shutter_r', seed=7 + int(x))
    for x in (-d / 4, d / 4):
        lit_window(fu['left'], x, 1.8, 1.8, 3.0, shutter='wf_shutter_r', glow=(rnd.random() < 0.4), hearts=False, seed=8 + int(x))
    top = sh + uh
    fr = F(0, 0, 0, 90)
    hr = w * 0.52
    gable_roof(fr, d, w, top, hr, keys=RSH, wall='plaster', ov=2.4, ovg=2.0, barge='wf_timber_dark')
    snow_roof(fr, d, w, top, hr, ov=2.4, ovg=2.0, seed=5)
    for side in ('front', 'back'):
        fg = faces(0, 0, w, d, top)[side]
        n = int(w / 0.9)
        for i in range(n):
            x = -w / 2 + w * (i + 0.5) / n
            lbox(fg, (w / n - 0.06, 0.1, 1.2), x, -0.1, hr * (1 - abs(x) / (w / 2)) * 0.5 + 0.6, 'wf_plank')
        lit_window(fg, 0, 1.2, 1.8, 2.2, glow=(side == 'front'), ledge_snow=False, shutter='wf_shutter_r', seed=22)
    # big external stone chimney on the gable end
    cx = w / 2 + 1.2
    box(nm('ch'), (3.2, 4.0, top + hr - 1.0), loc=(cx, 0, (top + hr - 1.0) / 2), key='wf_stone')
    for k, fr2 in enumerate(faces(cx, 0, 3.2, 4.0).values()):
        stone_face(fr2, -1.2, 1.2, 1.0, top + hr - 3.0, 14, 60 + k, keys=('wf_stone', 'wf_stone_dark'))
    box(nm('chc'), (3.8, 4.6, 0.6), loc=(cx, 0, top + hr - 0.7), key='wf_stone_dark', bev=0.08)
    snow_cap_box(cx, 0, 3.6, 4.4, top + hr - 0.3, seed=9)
    for s in (-1, 1):
        cyl(nm('pot'), 0.3, 1.0, loc=(cx, s * 1.0, top + hr - 0.4), key='terracotta', verts=10, r2=0.24)
    ground_snow(0, 0, w, d, seed=5)
    U.marker('mk_door', (w / 4, -d / 2 - 0.4, 0.4))
    return finalize('C01_02_chalet_02', smooth_angle=30)


# ================================================================ C01_03 long hall-chalet + woodshed
def chalet_03():
    """Long hall-chalet with a covered front porch and an attached woodshed stacked with logs."""
    reset()
    rnd = random.Random(1003)
    import v4util as U
    w, d, sh, uh = 24.0, 14.0, 5.5, 7.5
    stone_base(0, 0, w, d, sh, seed=11)
    log_storey(0, 0, w, d, sh, uh, key='wf_plank', alt='wf_timber')
    top = sh + uh
    fo = faces(0, 0, w, d)['front']
    fu = faces(0, 0, w, d, sh)['front']
    door_timber(fo, -4.0, seed=11)
    for x in (-10.0, 3.0, 9.0):
        lit_window(fo, x, 2.0, 2.0, 2.6, shutter='wf_shutter_g', seed=12 + int(x))
    for x in (-9.0, -3.0, 3.0, 9.0):
        lit_window(fu, x, 1.7, 1.9, 3.0, shutter='wf_shutter_g', glow=(rnd.random() < 0.5), seed=20 + int(x))
    fr = F(0, 0, 0, 90)
    hr = w * 0.32
    gable_roof(fr, d, w, top, hr, keys=RSH, wall='wf_plank', ov=2.6, ovg=2.2, barge='wf_timber_dark')
    snow_roof(fr, d, w, top, hr, ov=2.6, ovg=2.2, seed=11)
    chimney_snow(w / 4, d * 0.2, top, top + hr + 2.4, w=1.9)
    # covered porch along the front, its own lean-to snow roof
    py = -d / 2 - 4.0
    for x in (-w / 2 + 1, -w / 6, w / 6, w / 2 - 1):
        cyl(nm('pp'), 0.45, sh + 1.5, loc=(x, py, 0), key='wf_timber', verts=8)
        snow_cap_box(x, py, 1.0, 1.0, sh + 1.5, bev=0.3, seed=int(x))
    porch_h = sh + 1.8
    box(nm('pr'), (w + 0.6, 4.6, 0.3), loc=(0, py + 0.3, porch_h), key='wf_plank', rot=(-16, 0, 0))
    box(nm('prs'), (w + 0.8, 4.8, 0.5), loc=(0, py + 0.2, porch_h + 0.5), key=SNOW, rot=(-16, 0, 0), bev=0.2)
    icicle_row(F(0, py - 2.3, 0, 0), -w / 2, w / 2, 0, porch_h - 0.3, lo=0.4, hi=1.4, seed=13, prob=0.7)
    box(nm('pdk'), (w, 4.6, 0.3), loc=(0, py + 0.2, 0.15), key='wf_timber_dark')
    # attached woodshed on the right gable end: open-front lean-to, high at the back, low at the front (-Y)
    sx = w / 2 + 5.5
    swd, sdd = 11.0, 9.0
    box(nm('wsb'), (swd, sdd, 0.3), loc=(sx, 0, 0.15), key='wf_timber_dark')
    back_h, front_h = 7.2, 5.2
    for (px, py2, ph) in ((-swd / 2 + 0.6, sdd / 2 - 0.6, back_h), (swd / 2 - 0.6, sdd / 2 - 0.6, back_h),
                          (-swd / 2 + 0.6, -sdd / 2 + 0.6, front_h), (swd / 2 - 0.6, -sdd / 2 + 0.6, front_h), (0, -sdd / 2 + 0.6, front_h)):
        cyl(nm('wsp'), 0.38, ph, loc=(sx + px, py2, 0), key='wf_timber', verts=8)
    # back wall of stacked planks so the shed is not see-through
    lbox(F(sx, sdd / 2, 0, 180), (swd, 0.4, back_h), 0, -0.2, back_h / 2, 'wf_plank')
    # lean-to roof: single slope from back_h down to front_h (tilts about X toward -Y)
    rise = back_h - front_h
    aa = math.degrees(math.atan2(rise, sdd))
    mz = (back_h + front_h) / 2 + 0.3
    box(nm('wsr'), (swd + 1.4, sdd + 2.2, 0.3), loc=(sx, 0.2, mz), key='wf_plank', rot=(aa, 0, 0))
    box(nm('wsrs'), (swd + 1.2, sdd + 2.0, 0.5), loc=(sx, 0.2, mz + 0.45), key=SNOW, rot=(aa, 0, 0), bev=0.2)
    icicle_row(F(sx, -sdd / 2 - 1.2, 0, 0), -swd / 2, swd / 2, 0, front_h + 0.2, lo=0.4, hi=1.3, seed=14)
    # stacked logs filling the shed (log ends face the open -Y front), in two side-by-side piles
    for pile_y in (-2.4, 1.4):
        for row in range(5):
            cyl(nm('fw'), 0.48, swd - 2.0, loc=(sx, pile_y, 0.55 + row * 0.92),
                key=rnd.choice(['bark', 'wf_timber', 'wood_light']), verts=8, rot=(0, 90, rnd.uniform(-4, 4)))
            cyl(nm('fwe'), 0.4, 0.06, loc=(sx - (swd - 2.0) / 2 - 0.04, pile_y, 0.55 + row * 0.92), key='wood_light', verts=8, rot=(0, 90, 0))
    ground_snow(0, 0, w, d, seed=11)
    U.marker('mk_door', (-4.0, -d / 2 - 0.4, 0.4))
    return finalize('C01_03_chalet_03', smooth_angle=30)


# ================================================================ C01_04 round-log cabin, turf-and-snow roof
def chalet_04():
    """Small round-log cabin with crossed log corners and a thick turf-and-snow roof."""
    reset()
    rnd = random.Random(1004)
    import v4util as U
    w, d, h = 16.0, 14.0, 7.5
    box(nm('fl'), (w + 0.6, d + 0.6, 0.6), loc=(0, 0, 0.3), key='wf_stone_dark', bev=0.06)
    # body: a solid timber core wall (no sky gaps), faced with half-round logs on the four sides.
    box(nm('core'), (w - 0.6, d - 0.6, h), loc=(0, 0, h / 2), key='wf_timber_dark')
    nlog = int(h / 0.95)
    for i in range(nlog):
        z = 0.75 + i * 0.95
        k = ['wf_timber', 'wood_light', 'wf_plank'][i % 3]
        # front/back log courses run along x, their round ends crossing the corners
        cyl(nm('lf'), 0.5, w + 0.9, loc=(0, -d / 2, z), key=k, verts=10, rot=(0, 90, 0))
        cyl(nm('lb'), 0.5, w + 0.9, loc=(0, d / 2, z), key=k, verts=10, rot=(0, 90, 0))
        # side log courses run along y, offset half a course in z so corners interlock
        cyl(nm('ll'), 0.5, d - 0.1, loc=(-w / 2, 0, z + 0.48), key=k, verts=10, rot=(90, 0, 0))
        cyl(nm('lr'), 0.5, d - 0.1, loc=(w / 2, 0, z + 0.48), key=k, verts=10, rot=(90, 0, 0))
    fo = faces(0, 0, w, d)['front']
    door_timber(fo, 0, w=3.2, h=6.0, seed=15)
    for x in (-5.0, 5.0):
        lit_window(fo, x, 2.6, 1.8, 2.4, shutter='wf_shutter_b', seed=16 + int(x))
    for x in (-d / 4, d / 4):
        lit_window(faces(0, 0, w, d)['left'], x, 2.6, 1.6, 2.2, shutter='wf_shutter_b', glow=(rnd.random() < 0.4), hearts=False, seed=18 + int(x))
    # steep gable roof: timber planks, thick turf layer, then snow
    top = h
    fr = F(0, 0, 0, 90)
    hr = w * 0.46
    gable_roof(fr, d, w, top, hr, keys=('wf_timber', 'wf_timber_dark'), wall='wf_timber', ov=1.6, ovg=1.4, barge='wf_timber_dark')
    # thick turf blanket on each slope (one angled green slab per side), then a snow layer over it.
    # fr is rotated 90deg (ridge runs along the building's x); in fr-local coords the span is d, length w.
    aa = math.atan2(hr, d / 2 + 1.6)
    hw = d / 2 + 1.6
    S = hw / math.cos(aa)
    zr = top + hr
    for s in (-1, 1):
        nrm = Vector((0, s * math.sin(aa), math.cos(aa)))
        dirv = Vector((0, s * math.cos(aa), -math.sin(aa)))
        c = Vector((0, 0, zr)) + dirv * (S / 2) + nrm * 0.28
        lbox(fr, (w + 2.6, S + 0.1, 0.5), 0, c.y, c.z, 'wf_turf', rot=(-s * math.degrees(aa), 0, 0), bev=0.18)
    snow_roof(fr, d, w, top, hr, ov=1.6, ovg=1.4, seed=15)
    # a few turf tufts poking through the eave snow
    for s in (-1, 1):
        for i in range(6):
            x = rnd.uniform(-w / 2 + 1, w / 2 - 1)
            blob(nm('tuft'), rnd.uniform(0.35, 0.55), (x, s * (d / 2 + 1.3), top + 0.5), 'wf_turf', subdiv=1, amp=0.3, scale=(1.2, 1.0, 0.4), seed=i + s)
    chimney_snow(-w / 4, d * 0.2, top, top + hr + 2.0, w=1.7)
    ground_snow(0, 0, w, d, seed=15)
    U.marker('mk_door', (0, -d / 2 - 0.4, 0.4))
    return finalize('C01_04_chalet_04', smooth_angle=30)


# ================================================================ C01_05 two-storey, outside stair, bell gable
def chalet_05():
    """Two-storey chalet with an outside timber stair to the upper door, carved shutters and a little bell gable."""
    reset()
    rnd = random.Random(1005)
    import v4util as U
    w, d, sh, uh = 20.0, 16.0, 8.0, 8.0
    stone_base(0, 0, w, d, sh, seed=21)
    log_storey(0, 0, w, d, sh, uh)
    top = sh + uh
    fo = faces(0, 0, w, d)['front']
    fu = faces(0, 0, w, d, sh)['front']
    door_timber(fo, -w / 4, seed=21)
    lit_window(fo, w / 4, 2.4, 2.0, 2.8, shutter='wf_shutter_r', seed=22)
    # upper door reached by the outside stair, on the right half of the upper front
    door_timber(fu, w / 4, w=3.0, h=5.6, step=None, seed=23)
    lit_window(fu, -w / 4, 1.8, 2.2, 3.2, shutter='wf_shutter_r', seed=24)
    for x in (-d / 4, d / 4):
        lit_window(faces(0, 0, w, d, sh)['right'], x, 1.8, 1.9, 3.0, shutter='wf_shutter_r', glow=(rnd.random() < 0.4), hearts=False, seed=25 + int(x))
    fr = F(0, 0, 0, 90)
    hr = w * 0.42
    gable_roof(fr, d, w, top, hr, keys=RSH, wall='wf_timber', ov=2.4, ovg=2.0, barge='wf_timber_dark')
    snow_roof(fr, d, w, top, hr, ov=2.4, ovg=2.0, seed=21)
    for side in ('front', 'back'):
        fg = faces(0, 0, w, d, top)[side]
        lbeam(fg, (0, -0.2, 0.2), (0, -0.2, hr - 0.4), 0.32, 'wf_timber')
        for s in (-1, 1):
            lbeam(fg, (s * w * 0.4, -0.2, 0.2), (0, -0.2, hr * 0.78), 0.28, 'wf_timber')
        lit_window(fg, 0, 1.0, 1.6, 2.0, glow=(side == 'front'), ledge_snow=False, shutter='wf_shutter_r', seed=26)
    # outside stair: landing at the upper door + stringer of steps down to the ground
    lx = w / 4
    landing_z = sh + 0.2
    box(nm('land'), (5.0, 3.4, 0.4), loc=(lx, -d / 2 - 2.0, landing_z), key='wf_timber_dark')
    carved_rail(F(lx, -d / 2 - 2.0, landing_z, 0), -2.5, 2.5, 0.0, -1.7, h=1.6, key='wf_plank_light')
    nst = 9
    for i in range(nst):
        t = i / nst
        sx2 = lx - 5.0 - i * 1.3
        sz = landing_z * (1 - t)
        box(nm('step'), (1.4, 3.2, sz + 0.3), loc=(sx2, -d / 2 - 2.0, (sz + 0.3) / 2), key='wf_timber' if i % 2 else 'wf_plank')
        snow_cap_box(sx2 - 0.5, -d / 2 - 2.0, 0.6, 3.2, sz, bev=0.15, seed=i)
    for i in range(0, nst + 1, 2):
        sx2 = lx - 5.0 - i * 1.3
        sz = landing_z * (1 - i / nst)
        cyl(nm('sp'), 0.12, 1.8, loc=(sx2, -d / 2 - 3.6, sz + 0.3), key='wf_timber', verts=6)
    # bell gable on the roof ridge (front)
    bz = top + hr + 0.3
    for s in (-1, 1):
        cyl(nm('blp'), 0.2, 2.6, loc=(s * 1.2, -d / 2 + 2.0, bz), key='wf_timber', verts=6)
    box(nm('blr'), (3.4, 1.4, 0.3), loc=(0, -d / 2 + 2.0, bz + 2.6), key='wf_timber_dark')
    box(nm('blrs'), (3.6, 1.6, 0.4), loc=(0, -d / 2 + 2.0, bz + 2.8), key=SNOW, bev=0.15)
    lathe(nm('bell'), [(0, 0), (0.42, 0), (0.44, 0.1), (0.3, 0.5), (0.26, 0.7), (0, 0.72)], loc=(0, -d / 2 + 2.0, bz + 1.7), key='bronze', segs=12)
    chimney_snow(-w / 4, d * 0.22, top, top + hr + 2.4, w=1.9)
    ground_snow(0, 0, w, d, seed=21)
    U.marker('mk_door', (-w / 4, -d / 2 - 0.4, 0.4))
    return finalize('C01_05_chalet_05', smooth_angle=30)


# ================================================================ C01_06 chalet with stone tower annex
def chalet_06():
    """Chalet with a round stone tower annex capped by a conical snow-covered roof."""
    reset()
    rnd = random.Random(1006)
    import v4util as U
    w, d, sh, uh = 20.0, 16.0, 7.0, 8.0
    stone_base(-1.0, 0, w, d, sh, seed=31)
    log_storey(-1.0, 0, w, d, sh, uh)
    top = sh + uh
    fo = faces(-1.0, 0, w, d)['front']
    fu = faces(-1.0, 0, w, d, sh)['front']
    door_timber(fo, -w / 4 - 1.0, seed=31)
    lit_window(fo, w / 4 - 1.0, 2.2, 2.0, 2.8, shutter='wf_shutter_g', seed=32)
    for x in (-w / 4 - 1.0, w / 4 - 1.0):
        lit_window(fu, x, 1.8, 2.2, 3.2, shutter='wf_shutter_g', glow=(rnd.random() < 0.5), seed=33 + int(x))
    fr = F(-1.0, 0, 0, 90)
    hr = w * 0.4
    gable_roof(fr, d, w, top, hr, keys=RSH, wall='wf_timber', ov=2.4, ovg=2.0, barge='wf_timber_dark')
    snow_roof(fr, d, w, top, hr, ov=2.4, ovg=2.0, seed=31)
    chimney_snow(-w / 4 - 1.0, d * 0.2, top, top + hr + 2.2, w=1.8)
    # round stone tower on the right corner
    tx, ty, tr, th = w / 2 - 1.0 + 1.5, -d / 2 + 4.0, 4.2, top + 2.0
    lathe(nm('tw'), [(0, 0), (tr + 0.6, 0), (tr + 0.2, 1.2), (tr, 2.0), (tr, th), (0, th)], loc=(tx, ty, 0), key='wf_stone', segs=24)
    # stone texture on the tower
    for i in range(int(tr * 7)):
        a = rnd.uniform(0, 360); zz = 1.5 + round(rnd.uniform(0, (th - 3) / 1.1)) * 1.1
        ar = math.radians(a)
        box(nm('tsb'), (0.3, rnd.choice([1.6, 2.2]), 1.0), loc=(tx + math.cos(ar) * tr, ty + math.sin(ar) * tr, zz), key=rnd.choice(['wf_stone', 'wf_stone_dark']), rot=(0, 0, a), bev=0.04)
    for zz in (3.0, th - 3.0):
        lathe(nm('tb'), [(0, zz - 0.2), (tr + 0.25, zz - 0.2), (tr + 0.25, zz + 0.25), (0, zz + 0.25)], loc=(tx, ty, 0), key='wf_stone_dark', segs=24)
    for k in range(2):
        a = -90 + k * 70
        ar = math.radians(a)
        lit_window(F(tx + math.cos(ar) * tr, ty + math.sin(ar) * tr, 0, a + 90), 0, 5.0 + k * 5.0, 1.4, 2.6, shutter=None, glow=True, hearts=False, ledge_snow=False, seed=35 + k)
    # conical snow-capped roof
    lathe(nm('trf'), [(0, th), (tr + 1.0, th), (tr + 1.0, th + 0.5), (0, th + 0.5)], loc=(tx, ty, 0), key='wf_timber_dark', segs=24)
    cone_roof(tx, ty, th + 0.5, tr + 1.0, (tr + 1.0) * 1.8, keys=RSH, rings=7, ov=0.5, finial='bronze', segs=24)
    tipz = th + 0.5 + (tr + 1.0) * 1.8
    lathe(nm('tsnow'), [(0, th + 0.4), (tr + 1.2, th + 0.3), (tr * 0.5, th + (tr + 1) * 0.9), (0, tipz - 0.5)], loc=(tx, ty, 0), key=SNOW, segs=24)
    icicle_row(F(tx, ty - (tr + 1.1), 0, 0), -tr, tr, 0, th + 0.4, lo=0.4, hi=1.2, seed=36)
    ground_snow(-1.0, 0, w, d, seed=31)
    U.marker('mk_door', (-w / 4 - 1.0, -d / 2 - 0.4, 0.4))
    return finalize('C01_06_chalet_06', smooth_angle=30)


BATCHES = {
    'chalets': ('v4_alpine', [
        ('C01_01_chalet_01', chalet_01, (1.0, -1.2, 0.4)),
        ('C01_02_chalet_02', chalet_02, (1.0, -1.2, 0.42)),
        ('C01_03_chalet_03', chalet_03, (1.1, -1.0, 0.4)),
        ('C01_04_chalet_04', chalet_04, (1.0, -1.2, 0.45)),
        ('C01_05_chalet_05', chalet_05, (1.0, -1.15, 0.42)),
        ('C01_06_chalet_06', chalet_06, (1.0, -1.2, 0.45)),
    ]),
}
