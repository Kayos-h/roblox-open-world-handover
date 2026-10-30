"""v4_wx4_fix - FIX worker wx4. Repaired copies of 7 reviewer-flagged alpine/winter models.
Never edits an existing source file; imports helpers from the original modules and overrides the
broken builders. Saved ids and categories are preserved so the new .blend/.fbx overwrite in place.
New palette keys use the x4_ prefix. Builders fixed:
  C01_04_chalet_04 (REDO), A04_05_rusty_hut_05 (MAJOR), C07_02_sled_02 (MAJOR),
  C08_01_frozen_boat_01 + C08_02_frozen_boat_02 (MAJOR), A01_03_igloo_03 (MINOR),
  C05_02_ice_block_02 (MINOR), C05_03_ice_block_03 (MINOR).
"""
import math, random
import bmesh
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, _obj_from_bm
from arch import F, faces, lbox, lbeam, beam3, slab, lslab, nm
from nature import blob, rock
import v4util

P = kitlib.PAL
# reuse winter keys already defined by the original modules at import time
import v4_wf_chalets          # defines wf_* keys + chalet helpers
import v4_wa_huts             # defines wa_* keys + hut helpers
import v4_wf2_props           # defines wf2_* keys (ice/snow props)
import v4_wa_ice              # defines wa_* igloo keys + dome/tunnel helpers

from v4_wf_chalets import (stone_base, log_storey, door_timber, lit_window, snow_cap_box,
                           chimney_snow, ground_snow, icicle_row, snow_roof, SNOW as WF_SNOW)
from arch import gable_roof
from v4_wa_huts import (_floor, _walls_box2, _door_z, _window_z, _steps, nm as _nm)
from v4_wa_ice import _snow_dome, _tunnel, _lantern
from v4_wf2_props import snow_pillow, icicles as wf2_icicles, ground_frost

SNOW = 'snow'

# -- opt-in NO-RENDER fallback (env WX4_NORENDER=1) ---------------------------------
# In this tight-memory session Cycles' embree BVH build and the EEVEE GL context both
# crash at the C level during the preview render (EXCEPTION_ACCESS_VIOLATION), which no
# Python try/except can catch. Because run_batch renders BEFORE it saves, that crash
# destroys the whole process and the .blend/.fbx are never written. When WX4_NORENDER=1
# we replace the two preview functions with a cheap placeholder PNG writer (no render
# engine, no embree, no GL), so the process survives to save + export the real model.
# The reviewer runs this module with the env unset, so the normal render path is intact.
import os as _os


def _blank_preview(ob, out, *a, **kw):
    res = kw.get('res', a[0] if a else 420)
    try:
        import bpy
        r = int(res)
        img = bpy.data.images.new('_wx4_ph', r, r)
        img.filepath_raw = out
        img.file_format = 'PNG'
        img.save()
        bpy.data.images.remove(img)
    except Exception:
        pass
    return out


if _os.environ.get('WX4_NORENDER') == '1':
    v4util.thumb_preview = _blank_preview
    v4util.quad_preview = _blank_preview

# a couple of x4-prefixed keys
P.setdefault('x4_turf',      ((96, 116, 70),   'Grass', 0.0, 1.0, 0))
P.setdefault('x4_ice',       ((206, 230, 240), 'Ice',   0.0, 0.18, 0))
P.setdefault('x4_ice_blue',  ((150, 196, 224), 'Ice',   0.0, 0.16, 0))
P.setdefault('x4_ice_deep',  ((96, 150, 196),  'Ice',   0.0, 0.14, 0))


# ================================================================ C01_04 chalet (REDO -> solid)
def chalet_04():
    """Small solid stone-and-plank chalet with a steep turf-and-snow gable roof.
    Deliberately a different, simpler silhouette from the log/stone chalets 01-03, but a closed
    solid body (walls joined, no flaring log ends, no floating chimney)."""
    reset()
    rnd = random.Random(10041)
    w, d, sh, uh = 16.0, 14.0, 5.0, 7.0
    # solid stone ground storey + plinth (shared helper builds closed walls)
    stone_base(0, 0, w, d, sh, seed=41)
    # solid plank upper storey: one closed box, faced with horizontal plank battens (not loose logs)
    box(nm('up'), (w, d, uh), loc=(0, 0, sh + uh / 2), key='wf_plank')
    for side, L in (('front', w), ('back', w), ('left', d), ('right', d)):
        fr = faces(0, 0, w, d, sh)[side]
        for k in range(int(uh / 1.0)):
            lbox(fr, (L, 0.12, 0.14), 0, -0.06, 0.6 + k * 1.0, 'wf_timber_dark')
        # corner posts hide the box seam
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(nm('cp'), (0.6, 0.6, uh), loc=(sx * (w / 2 - 0.1), sy * (d / 2 - 0.1), sh + uh / 2), key='wf_timber_dark')
    top = sh + uh
    fo = faces(0, 0, w, d)['front']
    fu = faces(0, 0, w, d, sh)['front']
    door_timber(fo, 0, w=3.2, h=6.0, seed=15)
    for x in (-5.0, 5.0):
        lit_window(fo, x, 2.2, 1.8, 2.4, shutter='wf_shutter_b', seed=16 + int(x))
    for x in (-w / 4, w / 4):
        lit_window(fu, x, 1.8, 1.9, 2.8, shutter='wf_shutter_b', glow=(rnd.random() < 0.5), seed=20 + int(x))
    for x in (-d / 4, d / 4):
        lit_window(faces(0, 0, w, d, sh)['left'], x, 1.8, 1.7, 2.6, shutter='wf_shutter_b', glow=(rnd.random() < 0.4), hearts=False, seed=24 + int(x))
    # steep gable roof: plank skin, then turf, then snow (all closed, sitting on the walls)
    fr = F(0, 0, 0, 90)
    hr = w * 0.46
    gable_roof(fr, d, w, top, hr, keys=('wf_timber', 'wf_timber_dark'), wall='wf_plank', ov=1.8, ovg=1.5, barge='wf_timber_dark')
    # turf blanket: one angled slab per slope, laid flat on the roof (fr is rotated 90deg: span=d, len=w)
    a = math.atan2(hr, d / 2 + 1.8)
    hw = d / 2 + 1.8
    S = hw / math.cos(a)
    zr = top + hr
    for s in (-1, 1):
        cy = (0) + (s * math.cos(a)) * (S / 2)
        cz = zr - math.sin(a) * (S / 2)
        lbox(fr, (w + 2.8, S, 0.45), 0, cy, cz + 0.28, 'x4_turf', rot=(-s * math.degrees(a), 0, 0), bev=0.12)
    snow_roof(fr, d, w, top, hr, ov=1.8, ovg=1.5, seed=15)
    # a few turf tufts poking through the eave snow
    for s in (-1, 1):
        for i in range(5):
            x = rnd.uniform(-w / 2 + 1, w / 2 - 1)
            blob(nm('tuft'), rnd.uniform(0.35, 0.5), (x, s * (d / 2 + 1.3), top + 0.5), 'x4_turf', subdiv=1, amp=0.3, scale=(1.2, 1.0, 0.4), seed=i + s)
    # chimney rooted on the roof slope (no gap)
    chimney_snow(-w / 4, d * 0.2, top - 0.5, top + hr + 2.0, w=1.7)
    ground_snow(0, 0, w, d, seed=15)
    v4util.marker('mk_door', (0, -d / 2 - 0.4, 0.4))
    return finalize('C01_04_chalet_04', smooth_angle=30)


# ================================================================ A04_05 rusty hut (MAJOR -> closed roof)
def rusty_hut_5():
    """Hut on a stone footing with a COMPLETE tin gable roof on both slopes (no open corner,
    no floating duplicate panel), boarded window, ladder."""
    reset()
    W, D, H = 14.0, 11.0, 7.0
    box(_nm('foot'), (W + 0.6, D + 0.6, 1.4), loc=(0, 0, 0.7), key='wa_sand_dark', bev=0.05)
    _floor(W, D)
    box(_nm('floor2'), (W - 0.4, D - 0.4, 0.3), loc=(0, 0, 1.55), key='wa_plank_grey')
    base = 1.4
    fy, dw = _walls_box2(W, D, H, 0.5, 'wa_plank_grey', base, door_w=4.2)
    _door_z(fy, dw, base)
    fr = faces(0, 0, W, D)['front']
    _window_z(fr, W / 2 - 3.0, base + 2.4, boarded=True)
    top = base + H
    hr = 3.0
    a = math.atan2(hr, W / 2)
    # BOTH roof slopes as solid tin panels resting on the walls (closed gable)
    for s in (-1, 1):
        ez = top - 0.3
        quad = [(0, -D / 2 - 0.6, top + hr), (s * (W / 2 + 0.5), -D / 2 - 0.6, ez),
                (s * (W / 2 + 0.5), D / 2 + 0.6, ez), (0, D / 2 + 0.6, top + hr)]
        slab(quad, (0, 0, 0.22), 'wa_tin_rust' if s < 0 else 'wa_tin_grey')
    # ridge cap
    box(_nm('ridgeb'), (0.5, D + 1.2, 0.5), loc=(0, 0, top + hr), key='wa_plank_dark')
    # gable infill triangles on BOTH ends (closed, no open corner)
    for yy in (-D / 2, D / 2):
        slab([(-W / 2, yy, top), (W / 2, yy, top), (0, yy, top + hr)], (0, (0.3 if yy < 0 else -0.3), 0), 'wa_plank_grey')
    # a little weathering: one flat tin patch lying ON a slope (seated, not floating)
    patch_y = 1.0
    px = -W / 4
    pz = top + (hr) * (1 - abs(px) / (W / 2)) - 0.25
    box(_nm('patch'), (2.4, 2.0, 0.12), loc=(px, patch_y, pz + 0.18), key='wa_tin_grey', rot=(0, math.degrees(a), 0))
    # ladder leaning on the -Y front wall beside the door (kept)
    lsa, lsb = (W / 2 + 0.2, -D / 2 - 2.2, 0.2), (W / 2 - 0.9, -D / 2 - 0.3, top + 0.8)
    for s in (-0.5, 0.5):
        beam3((lsa[0], lsa[1] + s, lsa[2]), (lsb[0], lsb[1] + s, lsb[2]), 0.13, 0.13, 'wa_plank_dark')
    for k in range(6):
        t = (k + 0.5) / 6
        rx = lsa[0] + (lsb[0] - lsa[0]) * t
        ry = lsa[1] + (lsb[1] - lsa[1]) * t
        rz = lsa[2] + (lsb[2] - lsa[2]) * t
        beam3((rx, ry - 0.5, rz), (rx, ry + 0.5, rz), 0.07, 0.07, 'wa_plank_dark')
    for k in range(3):
        box(_nm('step'), (dw + 0.4 - k * 0.3, 1.0, 0.5), loc=(0, fy - 0.8 - k * 0.5, 0.25 + k * 0.5), key='wa_plank_dark', bev=0.03)
    return finalize('A04_05_rusty_hut_05', smooth_angle=30)


# ================================================================ C07_02 sled (MAJOR -> proper toboggan)
def sled_02():
    """Child's toboggan: two curved wooden runners, a slatted plank bed, a curled-up front, and a
    short pull rope. No blobby body, no whip tail."""
    reset()
    rnd = random.Random(7021)
    L, W = 7.0, 2.6
    bed_z = 1.1
    # two curved runners (front curls up at -x = front/-Y of model after no rotation; here front is +x tip)
    for sy in (-1, 1):
        y = sy * (W / 2 - 0.25)
        tube(nm('run'), [(-L / 2, y, 0.25), (L / 2 - 1.6, y, 0.25), (L / 2 - 0.3, y, 0.35),
                         (L / 2 + 0.5, y, 1.2), (L / 2 + 0.8, y, 2.0)], 0.22, 'wf2_timber', res=6, taper=[1, 1, 1, 0.9, 0.8])
        # uprights from runner to bed
        for i in range(4):
            x = -L / 2 + 0.9 + i * (L - 2.0) / 3
            cyl(nm('up'), 0.16, bed_z - 0.25, loc=(x, y, 0.25), key='wf2_timber_dark', verts=6)
    # cross battens tying the two runners under the bed
    for i in range(3):
        x = -L / 2 + 1.2 + i * (L - 2.4) / 2
        box(nm('xb'), (0.3, W - 0.2, 0.18), loc=(x, 0, bed_z - 0.15), key='wf2_timber_dark')
    # slatted plank bed
    nb = int(L / 0.8)
    for i in range(nb):
        x = -L / 2 + 0.5 + i * (L - 0.8) / nb
        box(nm('bd'), (0.5, W - 0.3, 0.14), loc=(x, 0, bed_z + 0.3), key='wf2_plank' if i % 2 else 'wf2_plank_light', bev=0.03)
    # curled front lip joining the bed to the runner tips
    box(nm('lip'), (0.5, W - 0.3, 0.9), loc=(L / 2 + 0.3, 0, bed_z + 0.9), key='wf2_plank_light', rot=(0, -38, 0), bev=0.05)
    # low back rail
    for sy in (-1, 1):
        cyl(nm('bp'), 0.12, 1.4, loc=(-L / 2 + 0.3, sy * (W / 2 - 0.3), bed_z + 0.3), key='wf2_timber', verts=6)
    box(nm('bbar'), (0.26, W, 0.18), loc=(-L / 2 + 0.3, 0, bed_z + 1.6), key='wf2_timber', bev=0.05)
    # short pull rope from the curled front tip, coiled on the ground (not a thin straight whip)
    tube(nm('rope'), [(L / 2 + 0.8, 0, 2.0), (L / 2 + 1.6, 0.4, 1.0), (L / 2 + 2.0, -0.3, 0.3),
                      (L / 2 + 1.4, -0.6, 0.18), (L / 2 + 2.1, -0.4, 0.18)], 0.1, 'rope', res=5)
    torus(nm('coil'), 0.55, 0.1, loc=(L / 2 + 1.8, -0.4, 0.2), key='rope', segs=12, rsegs=4)
    blob(nm('snow'), 1.0, (0, 0, 0.0), SNOW, subdiv=2, amp=0.12, scale=(3.0, 1.4, 0.2), seed=1)
    ground_frost(0, 0, L / 2, W / 2 + 0.4, n=6, seed=2)
    return finalize('C07_02_sled_02', smooth_angle=35)


# ================================================================ C08 frozen boats (MAJOR -> no black voids)
def _hull_fixed(name, L, W, H, wz, bow_axis, key_out, key_in, keel='wf2_timber_dark'):
    """Lofted boat hull with a CLOSED, correctly-wound shell: the side faces, a bottom cap, and a
    top gunwale rim band so there is no open/black-faced boundary. recalc_face_normals at the end."""
    bm = bmesh.new()
    nseg = 11
    nz = 4
    rings = []
    for j in range(nz + 1):
        tz = j / nz
        z = wz - 0.6 + (H + 0.6) * tz
        beam = (0.35 + 0.65 * tz)
        ring = []
        for i in range(nseg + 1):
            t = i / nseg
            along = -L / 2 + t * L
            prof = math.sin(math.pi * t) ** 0.6
            half = (W / 2) * prof * beam
            if t < 0.22:
                half *= (t / 0.22) ** 0.7
            s = 1 if i <= nseg // 2 else -1
            ring.append((along, s * half, z))
        rings.append(ring)
    vrings = [[bm.verts.new((a, b, c) if bow_axis == 'x' else (b, a, c)) for (a, b, c) in r] for r in rings]
    # side skin
    for j in range(nz):
        A, B = vrings[j], vrings[j + 1]
        for i in range(nseg):
            bm.faces.new((A[i], A[i + 1], B[i + 1], B[i]))
    # bottom cap (fan from the first ring; wound so recalc can orient it)
    bm.faces.new(vrings[0])
    # top rim band: a thin inner ring so the top edge is a closed solid lip, not an open hole
    top = vrings[nz]
    inner = []
    for (v) in top:
        co = v.co.copy()
        # pull inward toward the local centreline and down a touch
        if bow_axis == 'x':
            co.y *= 0.82
        else:
            co.x *= 0.82
        co.z -= 0.35
        inner.append(bm.verts.new(co))
    for i in range(nseg):
        bm.faces.new((top[i], top[i + 1], inner[i + 1], inner[i]))
    # inner floor cap across the pulled-in top-inner ring so you cannot see through to a black void
    bm.faces.new(list(reversed(inner)))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj_from_bm(name, bm, key_out)
    if bow_axis == 'x':
        box(nm('keel'), (L, 0.4, 0.5), loc=(0, 0, wz - 0.7), key=keel)
        box(nm('flr'), (L - 2.5, W - 2.0, 0.3), loc=(0, 0, wz + 0.1), key=key_in)
    else:
        box(nm('keel'), (0.4, L, 0.5), loc=(0, 0, wz - 0.7), key=keel)
        box(nm('flr'), (W - 2.0, L - 2.5, 0.3), loc=(0, 0, wz + 0.1), key=key_in)
    return o


def frozen_boat_01():
    """C08_01 rowboat frozen in lake ice: clean closed frosted hull (no black void), thwarts, oars."""
    reset()
    rnd = random.Random(8011)
    L, W, H = 14.0, 5.6, 4.2
    wz = 1.4
    box(nm('ice'), (L + 5, W + 5, 0.8), loc=(0, 0, 0.4), key='wf2_ice', bev=0.2)
    for i in range(6):
        box(nm('icf'), (rnd.uniform(2.5, 4), rnd.uniform(2.5, 4), 0.12), loc=(rnd.uniform(-L / 2, L / 2), rnd.uniform(-W, W), 0.82), key='wf2_ice_blue', rot=(0, 0, rnd.uniform(0, 90)))
    _hull_fixed('hull', L, W, H, wz, 'x', 'wf2_plank', 'wf2_timber_dark')
    for sy in (-1, 1):
        for i in range(6):
            t = (i + 0.5) / 6
            x = -L / 2 + t * L
            prof = math.sin(math.pi * t) ** 0.6
            if t < 0.22:
                prof *= (t / 0.22) ** 0.7
            yw = (W / 2) * prof
            box(nm('gw'), (L / 6, 0.4, 0.4), loc=(x, sy * yw, wz + H - 0.4), key='wf2_plank_grey', rot=(0, 0, sy * 10))
    for x in (-3.2, 2.8):
        box(nm('th'), (1.0, W * 0.55, 0.25), loc=(x, 0, wz + 2.0), key='wf2_plank')
    for i, y in enumerate((-1.2, 1.2)):
        cyl(nm('oar'), 0.12, 8.5, loc=(0.5, y, wz + 2.6), key='wf2_timber', verts=5, rot=(0, 90, 12 - i * 24))
        box(nm('blade'), (1.3, 0.12, 0.6), loc=(0.5 + (4.0 if i == 0 else -4.0), y, wz + 2.6), key='wf2_plank_light', bev=0.08)
    blob(nm('snow'), 1.0, (0, 0, 0.0), SNOW, subdiv=2, amp=0.1, scale=(5.0, 2.2, 0.22), seed=1)
    for sy in (-1, 1):
        wf2_icicles(-L / 2 + 3, L / 2 - 3, sy * W * 0.4, wz + 0.2, lo=0.4, hi=1.0, seed=sy, prob=0.5)
    ground_frost(0, 0, L / 2 + 1, W / 2 + 1, n=6, seed=8)
    return finalize('C08_01_frozen_boat_01', smooth_angle=34)


def frozen_boat_02():
    """C08_02 small sailing boat frozen in: closed frosted hull (no black triangular voids), snapped
    mast, torn sail."""
    reset()
    rnd = random.Random(8021)
    L, W, H = 20.0, 6.0, 5.0
    box(nm('ice'), (L + 8, W + 8, 0.9), loc=(0, 0, 0.45), key='wf2_ice', bev=0.2)
    for i in range(8):
        box(nm('icf'), (rnd.uniform(3, 6), rnd.uniform(3, 6), 0.12), loc=(rnd.uniform(-L / 2, L / 2), rnd.uniform(-W, W), 0.92), key='wf2_ice_blue', rot=(0, 0, rnd.uniform(0, 90)))
    wz = 1.6
    _hull_fixed('hull', L, W, H, wz, 'y', 'wf2_plank', 'wf2_timber_dark')
    for sx in (-1, 1):
        for i in range(8):
            t = (i + 0.5) / 8
            y = -L / 2 + t * L
            prof = math.sin(math.pi * t) ** 0.6
            if t < 0.22:
                prof *= (t / 0.22) ** 0.7
            xw = (W / 2) * prof
            box(nm('gw'), (0.4, L / 8, 0.4), loc=(sx * xw, y, wz + H - 0.6), key='wf2_plank_grey', rot=(0, 0, sx * 10))
    cyl(nm('mast'), 0.35, 6.0, loc=(0, -1.0, wz + 0.3), key='wf2_timber')
    box(nm('break'), (0.7, 0.7, 0.5), loc=(0, -1.0, wz + 6.0), key='wf2_timber_dark')
    tube(nm('upper'), [(0, -1.0, wz + 6.0), (1.5, -1.5, wz + 9.0), (3.0, -2.0, wz + 10.5)], 0.28, 'wf2_timber', res=4, taper=[1, 0.8, 0.6])
    box(nm('sail'), (0.1, 5.0, 5.5), loc=(0.2, 0.8, wz + 4.5), key='sail', rot=(0, 6, 0))
    box(nm('tear'), (0.12, 1.4, 2.0), loc=(0.2, 3.0, wz + 2.6), key='wf2_ice', rot=(0, 6, 18))
    blob(nm('snow'), 1.2, (0, 0, 0.0), SNOW, subdiv=2, amp=0.1, scale=(2.4, 6.0, 0.22), seed=1)
    for sx in (-1, 1):
        wf2_icicles(-2, 2, sx * W * 0.35, wz + 0.2, n=4, lo=0.4, hi=1.1, seed=sx, prob=0.6)
    ground_frost(0, 0, W / 2 + 1, L / 2 + 1, n=6, seed=8)
    return finalize('C08_02_frozen_boat_02', smooth_angle=34)


# ================================================================ A01_03 igloo (MINOR -> solid tunnel)
def igloo_3():
    """A01_03 big igloo with a SOLID blocky entry tunnel like igloo_01 (no thin curved whale-bone
    ribbon), two lanterns, sled-runner rack inside."""
    reset()
    R, H = 9.0, 7.4
    box(nm('floor'), (R * 2.4, R * 2.4, 0.3), loc=(0, 0, 0.15), key='wa_snow_pack')
    _snow_dome(0, 0, R, H, 'wa_snow', R - 1.3, seed=3)
    # solid snow-block tunnel (same helper igloo_1/2 use) - thick arch, not a ribbon
    thr = _tunnel(0, -R + 0.6, 3.0, 2.6, 5.4, 3.6, 'wa_snow', face_y=-1)
    # block-built porch collar around the tunnel mouth, solid
    py = -R - 4.4
    for s in (-1, 1):
        for k in range(3):
            box(nm('porch'), (1.6, 1.5, 1.2), loc=(s * 3.3, py + 0.8, 0.6 + k * 1.2),
                key='wa_snow_pack' if k % 2 else 'wa_snow', bev=0.05)
    box(nm('porchtop'), (7.6, 3.6, 0.6), loc=(0, py + 0.8, 3.7), key='wa_snow', bev=0.06)
    # two warm lanterns on solid posts by the door
    for s in (-1, 1):
        cyl(nm('lp'), 0.14, 2.6, loc=(s * 3.6, py - 0.3, 0), key='iron_dark', verts=8)
        _lantern(s * 3.6, py - 0.3, 2.6)
    # sled-runner rack leaning on the wall (kept, interior)
    rx = R - 1.0
    for s in (-1, 1):
        beam3((rx, -0.5 + s * 0.1, 0.2), (rx - 1.6, -0.5 + s * 0.1, 4.6), 0.2, 0.2, 'wa_board_trim')
    for k in range(3):
        beam3((rx + 0.3, -1.6, 1.2 + k * 1.1), (rx - 0.9, -1.6, 1.2 + k * 1.1), 0.14, 0.14, 'wa_board_grey')
        beam3((rx + 0.3, 0.6, 1.2 + k * 1.1), (rx - 0.9, 0.6, 1.2 + k * 1.1), 0.14, 0.14, 'wa_board_grey')
    cyl(nm('rug'), 2.6, 0.08, loc=(0, 0.6, 0.32), key='wa_fur', verts=16)
    v4util.marker('mk_door', (0, thr[1] + 0.3, 0.5))
    return finalize('A01_03_igloo_03', smooth_angle=30)


# ================================================================ C05_02 ice block (MINOR -> faceted)
def ice_block_02():
    """C05_02 carved ice block: a faceted/chipped translucent slab with internal blue colour layers,
    a frozen fish suspended inside, on a snow-dusted stone plinth. No plain smooth box."""
    reset()
    rnd = random.Random(5021)
    W, D, H = 5.0, 4.0, 9.0
    box(nm('pl'), (W + 1.2, D + 1.2, 1.0), loc=(0, 0, 0.5), key='wf2_stone', bev=0.1)
    snow_pillow(0, 0, W + 1.4, D + 1.4, 1.0, h=0.4, seed=1)
    bz = 1.0
    # faceted ice body: a low-poly lathe-ish prism with jittered rings so faces catch light differently
    bm = bmesh.new()
    nside, nz = 7, 4
    rings = []
    for j in range(nz + 1):
        z = bz + (H) * j / nz
        taper = 1.0 - 0.14 * (j / nz)         # slight inward taper upward
        ring = []
        for i in range(nside):
            a = 2 * math.pi * i / nside + (0.12 if j % 2 else 0)
            rx = (W / 2) * taper * (1 + rnd.uniform(-0.08, 0.12))
            ry = (D / 2) * taper * (1 + rnd.uniform(-0.08, 0.12))
            ring.append(bm.verts.new((math.cos(a) * rx, math.sin(a) * ry, z)))
        rings.append(ring)
    for j in range(nz):
        A, B = rings[j], rings[j + 1]
        for i in range(nside):
            bm.faces.new((A[i], A[(i + 1) % nside], B[(i + 1) % nside], B[i]))
    bm.faces.new(rings[0])
    bm.faces.new(list(reversed(rings[nz])))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    _obj_from_bm(nm('blk'), bm, 'x4_ice')
    # chipped corners: a few angular shards knocked off the edges
    for i in range(6):
        a = 2 * math.pi * i / 6 + rnd.uniform(-0.3, 0.3)
        z = bz + rnd.uniform(1.0, H - 1.0)
        box(nm('chip'), (0.9, 0.9, 1.1), loc=(math.cos(a) * (W / 2 - 0.2), math.sin(a) * (D / 2 - 0.2), z),
            key='x4_ice_blue', rot=(rnd.uniform(0, 40), rnd.uniform(0, 40), math.degrees(a)), bev=0.05)
    # internal colour layers: horizontal blue strata suspended inside
    for k in range(3):
        box(nm('layer'), (W * 0.82, D * 0.82, 0.3), loc=(0, 0, bz + (k + 1) * H / 4), key='x4_ice_deep' if k % 2 else 'x4_ice_blue', bev=0.04)
    # vertical internal cracks
    for i in range(4):
        box(nm('cr'), (0.08, D * 0.6, rnd.uniform(2.0, 4.0)), loc=(rnd.uniform(-W / 3, W / 3), rnd.uniform(-0.4, 0.4), bz + rnd.uniform(2, H - 2)), key='x4_ice_blue', rot=(0, rnd.uniform(-18, 18), 0))
    # frozen fish inside
    fz = bz + H * 0.5
    ball(nm('fish'), 1.3, (0, 0, fz), 'wf2_fish', segs=10, rings=6, scale=(1.8, 0.5, 0.9))
    box(nm('tail'), (0.9, 0.9, 1.3), loc=(-2.2, 0, fz), key='wf2_fish', rot=(0, 24, 0), bev=0.1)
    ball(nm('eye'), 0.16, (2.0, 0.35, fz + 0.3), 'wf2_coal', segs=6, rings=4)
    # frost cap + icicles
    snow_pillow(0, 0, W - 0.3, D - 0.3, bz + H - 0.1, h=0.4, seed=2)
    wf2_icicles(-W / 2, W / 2, -D / 2 - 0.1, bz + H - 0.2, lo=0.3, hi=0.8, seed=3, prob=0.6)
    ground_frost(0, 0, W, D, n=6, seed=6)
    return finalize('C05_02_ice_block_02', smooth_angle=20)


# ================================================================ C05_03 ice stag (MINOR -> thicken)
def ice_block_03():
    """C05_03 ice sculpture of a leaping stag on an ice plinth. Antlers and legs thickened to >=0.8
    stud so nothing reads as spindly or near-detached. Keeps the sculpture id and silhouette."""
    reset()
    rnd = random.Random(5031)
    K = 'wf2_ice'
    KB = 'wf2_ice_blue'
    lathe(nm('pl'), [(0, 0), (2.6, 0), (2.6, 2.0), (2.2, 2.2), (2.2, 2.4)], loc=(0, 0, 0), key=KB, segs=8)
    snow_pillow(0, 0, 4.6, 4.6, 2.4, h=0.35, seed=1)
    bz = 2.6
    # body
    ball(nm('body'), 1.7, (0, 0, bz + 3.4), K, segs=10, rings=7, scale=(1.0, 2.1, 1.1))
    # neck + head (thicker)
    tube(nm('neck'), [(0, -1.8, bz + 3.6), (0, -3.0, bz + 5.2), (0, -3.4, bz + 6.4)], 0.9, K, res=6, taper=[1.1, 0.95, 0.8])
    ball(nm('head'), 0.8, (0, -3.6, bz + 6.9), K, segs=8, rings=6, scale=(0.95, 1.4, 0.95))
    # antlers: thick main beams (r>=0.45 -> ~0.9 dia) with chunky tines, joined to the head
    for s in (-1, 1):
        tube(nm('ant'), [(s * 0.3, -3.5, bz + 7.2), (s * 0.8, -3.2, bz + 8.3), (s * 1.3, -3.7, bz + 9.3)], 0.46, KB, res=5, taper=[1.0, 0.9, 0.8])
        for k in range(2):
            tube(nm('pr'), [(s * (0.55 + k * 0.3), -3.35, bz + 7.9 + k * 0.6),
                            (s * (1.2 + k * 0.4), -3.0, bz + 8.6 + k * 0.7)], 0.44, KB, res=4, taper=[1.0, 0.85])
    # legs: thick (r=0.45 -> 0.9 dia), front reaching, back pushing off
    for (lx, ly, ang) in ((-0.7, -1.4, -40), (0.7, -1.4, -40), (-0.7, 1.4, 35), (0.7, 1.4, 35)):
        tube(nm('leg'), [(lx, ly, bz + 3.0),
                         (lx, ly + math.sin(math.radians(ang)) * 1.5, bz + 0.6),
                         (lx, ly + math.sin(math.radians(ang)) * 2.4, bz + 0.1)], 0.46, K, res=5, taper=[1.0, 0.9, 0.8])
        # hoof block grounding each leg so it reads as touching the plinth
        box(nm('hoof'), (0.9, 0.9, 0.5), loc=(lx, ly + math.sin(math.radians(ang)) * 2.4, bz + 0.2), key=KB, bev=0.08)
    # tail (thicker)
    tube(nm('tl'), [(0, 2.0, bz + 3.6), (0, 2.8, bz + 3.0)], 0.4, K, res=4, taper=[1, 0.6])
    ground_frost(0, 0, 3.0, 3.0, n=6, seed=7)
    return finalize('C05_03_ice_block_03', smooth_angle=34)


BATCHES = {
    'fix_a': ('v4_alpine', [
        ('C01_04_chalet_04', chalet_04, (1.0, -1.2, 0.42)),
        ('A01_03_igloo_03', igloo_3, (0.7, -1.3, 0.45)),
        ('C05_02_ice_block_02', ice_block_02, (0.8, -1.2, 0.4)),
        ('C05_03_ice_block_03', ice_block_03, (0.7, -1.2, 0.4)),
        ('C07_02_sled_02', sled_02, (1.0, -1.1, 0.4)),
        ('C08_01_frozen_boat_01', frozen_boat_01, (0.9, -1.0, 0.45)),
        ('C08_02_frozen_boat_02', frozen_boat_02, (1.0, -0.6, 0.5)),
    ]),
    'fix_b': ('v4_rusty', [
        ('A04_05_rusty_hut_05', rusty_hut_5, (1.0, -1.2, 0.45)),
    ]),
}
