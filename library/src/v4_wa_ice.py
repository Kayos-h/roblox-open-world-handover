"""wa ice module: A01 igloos, A02 ice-fishing shanties, A03 fishing holes.
Alpine village on a frozen lake. Snow, ice, warm lanterns. Fronts face -Y.
Only the headless runner (v4run.ps1) builds these; never the live Blender MCP tools.
"""
import math, random
from mathutils import Vector
import kitlib
from kitlib import (reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, flame)
from arch import F, faces, lbox, lbeam, beam3, slab, lslab, nm
from nature import blob, rock
import v4util

PAL = kitlib.PAL
# worker-prefixed palette keys (all start with wa_)
PAL['wa_snow']        = ((236, 242, 248), 'Snow',         0.00, 0.72, 0)
PAL['wa_snow_shade']  = ((206, 218, 232), 'Snow',         0.00, 0.78, 0)
PAL['wa_snow_pack']   = ((222, 230, 240), 'Snow',         0.00, 0.75, 0)
PAL['wa_ice_block']   = ((196, 222, 236), 'Ice',          0.00, 0.30, 0)
PAL['wa_ice_blue']    = ((168, 206, 230), 'Ice',          0.00, 0.28, 0)
PAL['wa_ice_clear']   = ((210, 234, 244), 'Ice',          0.00, 0.22, 0)
PAL['wa_water_dark']  = ((20, 34, 42),    'Slate',        0.10, 0.25, 0)
PAL['wa_soot']        = ((54, 50, 48),    'Slate',        0.00, 0.95, 0)
PAL['wa_fur']         = ((150, 120, 86),  'Fabric',       0.00, 1.00, 0)
PAL['wa_fur_dark']    = ((104, 82, 60),   'Fabric',       0.00, 1.00, 0)
PAL['wa_bone']        = ((224, 216, 196), 'Limestone',    0.00, 0.80, 0)
PAL['wa_board_red']   = ((150, 68, 54),   'WoodPlanks',   0.00, 0.85, 0)
PAL['wa_board_blue']  = ((92, 108, 126),  'WoodPlanks',   0.00, 0.85, 0)
PAL['wa_board_green'] = ((82, 110, 84),   'WoodPlanks',   0.00, 0.85, 0)
PAL['wa_board_grey']  = ((132, 122, 108), 'WoodPlanks',   0.00, 0.92, 0)
PAL['wa_board_trim']  = ((78, 58, 44),    'Wood',         0.00, 0.88, 0)
PAL['wa_tin']         = ((120, 118, 112), 'CorrodedMetal',0.55, 0.70, 0)
PAL['wa_lantern']     = ((248, 192, 110), 'Glass',        0.00, 0.20, 0.5)
PAL['wa_rope']        = ((176, 150, 104), 'Fabric',       0.00, 1.00, 0)
PAL['wa_frost']       = ((206, 224, 232), 'SmoothPlastic', 0.00, 0.55, 0)

LANT = 'wa_lantern'


# ----------------------------------------------------------------- shared bits
def _lantern(x, y, z, s=1.0):
    """Small warm wall/post lantern, bottom at z."""
    cyl(nm('ltp'), 0.09 * s, 0.14 * s, loc=(x, y, z), key='iron_dark', verts=8)
    lathe(nm('ltc'), [(0.0, 0.0), (0.30 * s, 0.0), (0.26 * s, 0.1 * s), (0.0, 0.1 * s)],
          loc=(x, y, z + 0.12 * s), key='iron_dark', segs=8)
    lathe(nm('ltg'), [(0.0, 0.0), (0.24 * s, 0.0), (0.24 * s, 0.5 * s), (0.0, 0.5 * s)],
          loc=(x, y, z + 0.2 * s), key=LANT, segs=8)
    lathe(nm('ltt'), [(0.0, 0.0), (0.34 * s, 0.0), (0.12 * s, 0.28 * s), (0.0, 0.3 * s)],
          loc=(x, y, z + 0.7 * s), key='iron_dark', segs=8)
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        tube(nm('ltr'), [(x + math.cos(a) * 0.22 * s, y + math.sin(a) * 0.22 * s, z + 0.22 * s),
                         (x + math.cos(a) * 0.26 * s, y + math.sin(a) * 0.26 * s, z + 0.66 * s)], 0.03 * s, 'iron_dark', res=4)


def _snow_dome(cx, cy, r, h, key, inner_r, seed, segs=28, rings=11, blocks=True):
    """A snow-block dome shell: outer lathe + visible block seams, hollow inside (inner lathe)."""
    # outer shell
    prof = [(math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * h) for a in range(0, 91, 9)]
    prof[-1] = (0.0, h)
    lathe(nm('dome'), prof, loc=(cx, cy, 0), key=key, segs=segs)
    # inner hollow (slightly smaller, open bottom)
    iprof = [(math.cos(math.radians(a)) * inner_r, math.sin(math.radians(a)) * (h - 1.1)) for a in range(0, 91, 12)]
    iprof[-1] = (0.0, h - 1.1)
    io = lathe(nm('domein'), iprof, loc=(cx, cy, 0.05), key='wa_snow_shade', segs=max(16, segs - 6))
    io.scale = (-1, 1, 1)  # flip normals so inner face shows
    if blocks:
        rnd = random.Random(seed)
        courses = 6
        for c in range(courses):
            zt = (c + 0.5) / courses
            za = zt * 90
            rr = math.cos(math.radians(za)) * (r + 0.05)
            zz = math.sin(math.radians(za)) * h
            if rr < 0.6:
                continue
            n = max(6, int(2 * math.pi * rr / 1.8))
            for i in range(n):
                a = 2 * math.pi * (i + (c % 2) * 0.5) / n + rnd.uniform(-0.04, 0.04)
                bk = 'wa_ice_blue' if rnd.random() < 0.14 else (key if rnd.random() < 0.5 else 'wa_snow_pack')
                # block lies tangent to the dome: long axis (1.6) runs around the ring, thin axis points out
                box(nm('blk'), (1.6 + rnd.uniform(-0.2, 0.2), (h / courses) * 0.9, 0.3),
                    loc=(cx + math.cos(a) * rr, cy + math.sin(a) * rr, zz),
                    key=bk, rot=(0, 0, math.degrees(a) + 90), bev=0.04)


def _tunnel(cx, cy, r_out, r_in, length, h, key, face_y=-1):
    """Arched entrance tunnel along +/-Y, open at both ends, with a half-dome arch and side walls."""
    y0 = cy + face_y * r_out * 0.6
    y1 = y0 + face_y * length
    # arch tube over the opening
    pts = [(cx + math.cos(math.radians(a)) * (r_in + 0.4), y1, 0.1 + math.sin(math.radians(a)) * (h + 0.4))
           for a in range(0, 181, 20)]
    for yy in (y0, y1):
        tube(nm('arc'), [(cx + math.cos(math.radians(a)) * r_in, yy, math.sin(math.radians(a)) * h)
                         for a in range(10, 171, 16)], 0.4, key, res=4)
    # side walls
    for s in (-1, 1):
        lbox(F(cx, (y0 + y1) / 2, 0, 0), (0.45, abs(length), h), s * r_in, 0, h / 2, key)
    # top blocks
    seg = 5
    for i in range(seg):
        yy = y0 + (y1 - y0) * (i + 0.5) / seg
        a = 90
        box(nm('tt'), (r_in * 2.0, abs(length) / seg * 0.9, 0.42), loc=(cx, yy, h + 0.1), key=key, bev=0.04)
    return (cx, y1)  # threshold outer point


# ----------------------------------------------------------------- A01 igloos
def igloo_1():
    """A01_01 - 14-wide snow-block igloo, arched tunnel, furnished hollow interior."""
    reset()
    R, H = 7.0, 6.2
    box(nm('floor'), (R * 2.2, R * 2.2, 0.3), loc=(0, 0, 0.15), key='wa_snow_pack')
    _snow_dome(0, 0, R, H, 'wa_snow', R - 1.3, seed=1)
    # tunnel entrance facing -Y
    thr = _tunnel(0, -R + 0.6, 2.6, 2.3, 5.0, 3.3, 'wa_snow', face_y=-1)
    # interior: fur rug + ice bench, visible from the door
    cyl(nm('rug'), 2.6, 0.08, loc=(0, 0.6, 0.32), key='wa_fur', verts=16)
    cyl(nm('rug2'), 1.6, 0.06, loc=(0, 0.6, 0.4), key='wa_fur_dark', verts=14)
    box(nm('bench'), (4.0, 1.4, 1.0), loc=(0, 3.0, 0.8), key='wa_ice_block', bev=0.1)
    box(nm('benchtop'), (4.2, 1.6, 0.25), loc=(0, 3.0, 1.35), key='wa_fur', bev=0.05)
    _lantern(2.4, -R + 0.2, 2.2)
    v4util.marker('mk_door', (0, thr[1] + 0.3, 0.5))
    return finalize('igloo_1', smooth_angle=30)


def igloo_2():
    """A01_02 - 16-wide igloo with storage dome, drift ramp, smoke hole with soot."""
    reset()
    R, H = 8.0, 6.8
    box(nm('floor'), (R * 2.4, R * 2.4, 0.3), loc=(0, 0, 0.15), key='wa_snow_pack')
    _snow_dome(0, 0, R, H, 'wa_snow', R - 1.3, seed=2)
    thr = _tunnel(0, -R + 0.6, 2.6, 2.3, 5.2, 3.3, 'wa_snow', face_y=-1)
    # small storage dome on the +X side, joined by a short passage
    sx = R + 2.6
    _snow_dome(sx, 1.0, 4.2, 4.0, 'wa_snow_pack', 3.0, seed=12, segs=20)
    # passage
    for s in (-1, 1):
        lbox(F(), (abs(sx - R) + 1.0, 0.4, 3.0), (R + sx) / 2 - 0.5, 1.0 + s * 1.6, 1.5, 'wa_snow')
    box(nm('ptop'), (abs(sx - R) + 1.0, 3.4, 0.4), loc=((R + sx) / 2 - 0.5, 1.0, 3.1), key='wa_snow')
    # drift ramp at the entrance
    for k in range(5):
        box(nm('drift'), (6.0 - k * 0.9, 1.6, 0.5), loc=(0, -R - 1.6 - k * 0.5, 0.25 + k * 0.28), key='wa_snow',
            rot=(18, 0, 0), bev=0.1)
    # smoke hole with soot stain on top
    cyl(nm('hole'), 0.9, 0.5, loc=(0, 0, H - 0.4), key='wa_water_dark', verts=12)
    lathe(nm('soot'), [(0.9, H - 0.4), (1.7, H - 0.9), (1.7, H - 0.8), (0.9, H - 0.3)], loc=(0, 0, 0), key='wa_soot', segs=16)
    # interior
    cyl(nm('rug'), 2.4, 0.08, loc=(0, 0.6, 0.32), key='wa_fur', verts=16)
    box(nm('bench'), (3.6, 1.3, 1.0), loc=(0, 3.4, 0.8), key='wa_ice_block', bev=0.1)
    _lantern(2.4, -R + 0.2, 2.2)
    v4util.marker('mk_door', (0, thr[1] + 0.3, 0.5))
    return finalize('igloo_2', smooth_angle=30)


def igloo_3():
    """A01_03 - 18-wide igloo with block porch, whale-bone arch, two lanterns, sled-runner rack."""
    reset()
    R, H = 9.0, 7.4
    box(nm('floor'), (R * 2.4, R * 2.4, 0.3), loc=(0, 0, 0.15), key='wa_snow_pack')
    _snow_dome(0, 0, R, H, 'wa_snow', R - 1.3, seed=3)
    thr = _tunnel(0, -R + 0.6, 2.9, 2.5, 4.2, 3.6, 'wa_snow', face_y=-1)
    # block-built porch around the tunnel mouth
    py = -R - 3.6
    for s in (-1, 1):
        for k in range(3):
            box(nm('porch'), (1.5, 1.4, 1.1 + k * 0.1), loc=(s * 3.3, py + 0.8 + k * 0.0, 0.6 + k * 1.1),
                key='wa_snow_pack' if k % 2 else 'wa_snow', bev=0.05)
    box(nm('porchtop'), (7.4, 3.4, 0.5), loc=(0, py + 0.8, 3.6), key='wa_snow', bev=0.06)
    # whale-bone arch over the door
    for s in (-1, 1):
        tube(nm('bone'), [(s * 3.0, py - 0.6, 0.2), (s * 3.4, py - 0.6, 3.2),
                          (s * 1.6, py - 0.6, 5.4), (0, py - 0.6, 5.9)], 0.42, 'wa_bone', res=6, taper=[1.3, 1.0, 0.7, 0.5])
    ball(nm('bonetip'), 0.5, loc=(0, py - 0.6, 5.9), key='wa_bone', segs=10, rings=7)
    # two warm lanterns by the door
    for s in (-1, 1):
        cyl(nm('lp'), 0.12, 2.6, loc=(s * 3.6, py - 0.9, 0), key='iron_dark', verts=8)
        _lantern(s * 3.6, py - 0.9, 2.6)
    # sled-runner rack leaning on the wall
    rx = R - 1.0
    for s in (-1, 1):
        beam3((rx, -0.5 + s * 0.1, 0.2), (rx - 1.6, -0.5 + s * 0.1, 4.6), 0.18, 0.18, 'wa_board_trim')
    for k in range(3):
        beam3((rx + 0.3, -1.6, 1.2 + k * 1.1), (rx - 0.9, -1.6, 1.2 + k * 1.1), 0.12, 0.12, 'wa_board_grey')
        beam3((rx + 0.3, 0.6, 1.2 + k * 1.1), (rx - 0.9, 0.6, 1.2 + k * 1.1), 0.12, 0.12, 'wa_board_grey')
    cyl(nm('rug'), 2.6, 0.08, loc=(0, 0.6, 0.32), key='wa_fur', verts=16)
    v4util.marker('mk_door', (0, thr[1] + 0.3, 0.5))
    return finalize('igloo_3', smooth_angle=30)


# ----------------------------------------------------------------- A02 ice shanties
def _shanty(name, board_key, roof='gable', snow=True, seed=0,
            firewood=False, rods=False, net=False, canvas_roof=False, big_window=False):
    """Generic ice-fishing hut 8x9x7, hollow, floor, door 3.5x6, frosted window, stovepipe."""
    reset()
    rnd = random.Random(seed)
    W, D, H = 8.0, 9.0, 7.0
    t = 0.4
    # floor
    box(nm('floor'), (W, D, 0.3), loc=(0, 0, 0.15), key='wa_board_grey')
    # four walls from boxes around openings (front = -Y has door + window)
    # back + sides solid
    box(nm('back'), (W, t, H), loc=(0, D / 2 - t / 2, H / 2), key=board_key)
    for s in (-1, 1):
        box(nm('side'), (t, D, H), loc=(s * (W / 2 - t / 2), 0, H / 2), key=board_key)
    # front wall with a door gap (centre, 3.5 wide, 6 high) and a window hole
    fy = -D / 2 + t / 2
    dw, dh = 3.5, 6.0
    # left/right of door
    box(nm('fl'), ((W - dw) / 2, t, H), loc=(-(dw + (W - dw) / 2) / 2, fy, H / 2), key=board_key)
    box(nm('fr'), ((W - dw) / 2, t, H), loc=((dw + (W - dw) / 2) / 2, fy, H / 2), key=board_key)
    # lintel over door
    box(nm('flin'), (dw, t, H - dh), loc=(0, fy, dh + (H - dh) / 2), key=board_key)
    # plank seams on all walls (thin proud battens)
    for s in (-1, 1):
        for k in range(5):
            lbox(F(0, D / 2, 0, 180), (W, 0.06, 0.1), 0, -0.05, 0.8 + k * 1.3, 'wa_board_trim')
    # frosted window on +X side (or big shuttered window)
    wz = 3.6
    ww = 2.6 if big_window else 1.6
    box(nm('winhole'), (0.3, ww, 1.8), loc=(W / 2 - t / 2, 0.5, wz), key='wa_frost')
    for zz in (wz - 0.9, wz + 0.9):
        lbox(F(W / 2, 0, 0, 90), (ww + 0.4, 0.14, 0.14), 0.5, -0.1, zz, 'wa_board_trim')
    lbox(F(W / 2, 0, 0, 90), (0.14, 0.14, 1.9), 0.5, -0.1, wz, 'wa_board_trim')
    if big_window:
        for s in (-1, 1):
            box(nm('shut'), (0.14, ww * 0.6, 1.9), loc=(W / 2 + 0.1, 0.5 + s * (ww * 0.8), wz), key='wa_board_trim',
                rot=(0, 0, s * 20))
    # door frame + a closed plank door
    for s in (-1, 1):
        box(nm('djamb'), (0.2, t + 0.2, dh), loc=(s * dw / 2, fy, dh / 2), key='wa_board_trim')
    box(nm('dlin'), (dw + 0.4, t + 0.2, 0.3), loc=(0, fy, dh + 0.1), key='wa_board_trim')
    box(nm('door'), (dw - 0.2, 0.18, dh - 0.2), loc=(0, fy - 0.12, (dh - 0.2) / 2 + 0.1), key='wa_board_trim')
    for k in range(4):                                    # vertical plank seams on the door
        box(nm('dpl'), (0.06, 0.1, dh - 0.4), loc=(-dw / 2 + 0.3 + k * (dw - 0.6) / 3, fy - 0.22, dh / 2), key=board_key)
    for zz in (dh * 0.25, dh * 0.72):                     # iron ledges
        box(nm('dled'), (dw - 0.4, 0.08, 0.18), loc=(0, fy - 0.24, zz), key='iron_dark')
    ball(nm('dhandle'), 0.12, loc=(dw / 2 - 0.5, fy - 0.3, dh * 0.48), key='iron_dark', segs=6, rings=4)
    # roof
    if roof == 'gable':
        _gable_snow(W, D, H, rnd, snow=snow, canvas=canvas_roof)
    else:
        _monopitch_snow(W, D, H, rnd, snow=snow)
    # stovepipe with cap
    px, py2 = -W / 2 + 1.4, D / 2 - 2.2
    cyl(nm('pipe'), 0.32, 3.4, loc=(px, py2, H - 0.4), key='wa_tin', verts=10)
    lathe(nm('pcap'), [(0, 0), (0.5, 0), (0.55, 0.2), (0, 0.2)], loc=(px, py2, H + 3.0), key='wa_tin', segs=10)
    cyl(nm('pcol'), 0.4, 0.3, loc=(px, py2, H - 0.5), key='wa_tin', verts=10)
    # barrel + bucket by the door
    from props import barrel_body
    barrel_body(nm('br'), loc=(W / 2 - 1.2, -D / 2 - 1.6, 0.0), h=2.4)
    lathe(nm('buck'), [(0, 0), (0.5, 0), (0.6, 1.0), (0.54, 1.0), (0.44, 0.1), (0, 0.1)],
          loc=(-W / 2 + 1.0, -D / 2 - 1.4, 0.0), key='wa_tin', segs=12)
    if firewood:
        # stacked firewood lean-to on -X side
        for k in range(10):
            cyl(nm('log'), 0.35, 3.0, loc=(-W / 2 - 1.0, -2.5 + (k % 5) * 1.0, 0.4 + (k // 5) * 0.75), key='wa_board_trim',
                verts=8, rot=(0, 90, 0))
        box(nm('llroof'), (2.0, 6.0, 0.15), loc=(-W / 2 - 1.3, 0, 3.6), key='wa_tin', rot=(0, -24, 0))
    if rods:
        for k in range(3):
            beam3((-W / 2 - 0.1, -1.5 + k * 1.3, 2.0), (-W / 2 - 0.1, -1.5 + k * 1.3, 6.4), 0.05, 0.05, 'wa_board_trim')
    if net:
        # hanging net on the front
        for i in range(6):
            tube(nm('net'), [(-W / 2 + 0.5 + i * 0.5, -D / 2 - 0.3, 5.6), (-W / 2 + 0.5 + i * 0.5, -D / 2 - 0.5, 3.0)],
                 0.03, 'wa_rope', res=4)
        for j in range(4):
            tube(nm('neth'), [(-W / 2 + 0.5, -D / 2 - 0.4, 5.6 - j * 0.9), (-W / 2 + 3.0, -D / 2 - 0.4, 5.6 - j * 0.9)],
                 0.03, 'wa_rope', res=4)
    # step
    box(nm('step'), (dw + 0.6, 1.0, 0.3), loc=(0, -D / 2 - 0.5, 0.15), key='wa_board_grey', bev=0.04)
    v4util.marker('mk_door', (0, -D / 2 - 0.1, 0.4))
    return finalize(name, smooth_angle=30)


def _gable_snow(W, D, H, rnd, snow=True, canvas=False):
    import mathutils
    hr = 3.0
    rk = 'canvas' if canvas else 'wa_board_trim'
    ov = 0.6                      # eaves overhang
    ax = W / 2 + ov               # eave x (half-width incl overhang)
    L = D + 1.2                   # roof length (incl gable overhang)
    a = math.atan2(hr, W / 2)     # slope angle
    for s in (-1, 1):
        # roof plank slab from ridge (x=0,z=H+hr) down to eave (x=s*ax,z=H-ov*tan)
        ez = H - ov * math.tan(a)
        quad = [(0, -L / 2, H + hr), (s * ax, -L / 2, ez), (s * ax, L / 2, ez), (0, L / 2, H + hr)]
        slab(quad, (0, 0, 0.22), rk)
        if snow:
            # thin snow layer sitting just above the plank slab (same quad, lifted along normal)
            n = mathutils.Vector((-s * math.sin(a), 0, math.cos(a))) * 0.28
            sq = [(p[0] + n.x, p[1], p[2] + n.z) for p in quad]
            slab(sq, (0, 0, 0.22), 'wa_snow')
    # gable infill triangles (close the two ends)
    for yy in (-D / 2, D / 2):
        slab([(-W / 2, yy, H), (W / 2, yy, H), (0, yy, H + hr)], (0, (0.4 if yy < 0 else -0.4), 0), 'wa_board_grey')
    # ridge cap
    box(nm('ridge'), (0.5, L, 0.5), loc=(0, 0, H + hr), key='wa_board_trim')
    if snow:
        box(nm('snowridge'), (0.7, L, 0.3), loc=(0, 0, H + hr + 0.3), key='wa_snow', bev=0.06)
        for i in range(7):                           # icicles hanging off the front eave
            x = -W / 2 + W * (i + 0.5) / 7
            h = rnd.uniform(0.6, 1.3)
            lathe(nm('ice'), [(0.14, 0), (0.0, -h)], loc=(x, -D / 2 - ov, H - ov * math.tan(a) - 0.05),
                  key='wa_ice_clear', segs=6)


def _monopitch_snow(W, D, H, rnd, snow=True):
    import mathutils
    hr = 2.2
    a = math.atan2(hr, D)
    ov = 0.7
    # roof slab from back-high (y=+D/2, z=H+hr) to front-low (y=-D/2, z=H)
    quad = [(-W / 2 - 0.5, D / 2 + ov, H + hr), (W / 2 + 0.5, D / 2 + ov, H + hr),
            (W / 2 + 0.5, -D / 2 - ov, H), (-W / 2 - 0.5, -D / 2 - ov, H)]
    slab(quad, (0, 0, 0.3), 'wa_board_trim')
    # side gable triangles
    for s in (-1, 1):
        slab([(s * W / 2, -D / 2, H), (s * W / 2, D / 2, H), (s * W / 2, D / 2, H + hr)], (s * -0.35, 0, 0), 'wa_board_grey')
    if snow:
        n = mathutils.Vector((0, math.sin(a), math.cos(a))) * 0.3
        sq = [(p[0], p[1] + n.y, p[2] + n.z) for p in quad]
        slab(sq, (0, 0, 0.25), 'wa_snow')
        for i in range(7):
            x = -W / 2 + W * (i + 0.5) / 7
            h = rnd.uniform(0.5, 1.1)
            lathe(nm('ice'), [(0.12, 0), (0.0, -h)], loc=(x, -D / 2 - ov, H - 0.05), key='wa_ice_clear', segs=6)


def ice_shanty_1():
    """A02_01 - weathered red boards, gable roof with snow and icicles, stovepipe, frosted window."""
    return _shanty('ice_shanty_1', 'wa_board_red', roof='gable', snow=True, seed=21)


def ice_shanty_2():
    """A02_02 - blue-grey boards, mono-pitch snow roof, firewood lean-to, wall rods."""
    return _shanty('ice_shanty_2', 'wa_board_blue', roof='mono', snow=True, seed=22, firewood=True, rods=True)


def ice_shanty_3():
    """A02_03 - green planks, gable roof, big shuttered window, hanging net and rod rack."""
    return _shanty('ice_shanty_3', 'wa_board_green', roof='gable', snow=True, seed=23, net=True, rods=True, big_window=True)


def ice_shanty_4():
    """A02_04 - unpainted weathered wood patched with canvas, canvas-and-snow roof, sheet-metal chimney."""
    return _shanty('ice_shanty_4', 'wa_board_grey', roof='gable', snow=True, seed=24, canvas_roof=True)


# ----------------------------------------------------------------- A03 fishing holes
def _ice_plate(r, thick, seed, oval=1.0):
    rnd = random.Random(seed)
    o = cyl(nm('plate'), r, thick, loc=(0, 0, 0), key='wa_ice_clear', verts=20)
    o.scale = (oval, 1.0, 1.0)
    # radial dark cracks
    for i in range(7):
        a = 2 * math.pi * i / 7 + rnd.uniform(-0.2, 0.2)
        L = rnd.uniform(r * 0.4, r * 0.9)
        tube(nm('crack'), [(0, 0, thick + 0.01), (math.cos(a) * L * 0.5 * oval, math.sin(a) * L * 0.5, thick + 0.01),
                           (math.cos(a) * L * oval, math.sin(a) * L, thick + 0.01)], 0.04, 'wa_water_dark', res=4)
    return o


def fishing_hole_1():
    """A03_01 - thin ice plate with radial cracks, ragged raised rim, dark water, chipped chunks."""
    reset()
    r, thick = 3.2, 0.12
    box(nm('surf'), (6.4, 6.4, 0.12), loc=(0, 0, 0.06), key='wa_ice_block', bev=0.1)
    _ice_plate(r, thick, seed=31)
    rnd = random.Random(31)
    # dark water first (sunk centre), then the raised rim ring around it
    cyl(nm('water'), 1.3, 0.04, loc=(0, 0, 0.13), key='wa_water_dark', verts=18)
    # ragged raised rim ring (irregular blocks, 0.4 high)
    n = 16
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = 1.3 + rnd.uniform(-0.1, 0.15)
        box(nm('rim'), (0.6 + rnd.uniform(-0.1, 0.2), 0.5, 0.4 + rnd.uniform(-0.1, 0.2)),
            loc=(math.cos(a) * rr, math.sin(a) * rr, 0.2 + rnd.uniform(0, 0.1)),
            key='wa_ice_blue' if rnd.random() < 0.3 else 'wa_ice_clear', rot=(0, 0, math.degrees(a)), bev=0.03)
    # chipped chunks + slush around
    for i in range(10):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(1.6, 3.0)
        ball(nm('chunk'), rnd.uniform(0.2, 0.4), loc=(math.cos(a) * d, math.sin(a) * d, 0.18),
             key=rnd.choice(['wa_ice_clear', 'wa_ice_blue']), segs=6, rings=4, scale=(1.3, 1, 0.6))
    return finalize('fishing_hole_1', smooth_angle=25)


def fishing_hole_2():
    """A03_02 - oval hole with one ice slab leaning in, different crack pattern."""
    reset()
    r, thick = 3.2, 0.12
    box(nm('surf'), (7.4, 6.0, 0.12), loc=(0, 0, 0.06), key='wa_ice_block', bev=0.1)
    _ice_plate(r, thick, seed=32, oval=1.3)
    rnd = random.Random(32)
    cyl(nm('water'), 1.5, 0.04, loc=(0, 0, 0.13), key='wa_water_dark', verts=18)
    n = 14
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = 1.6 * (1.3 if abs(math.cos(a)) > 0.5 else 1.0) + rnd.uniform(-0.1, 0.15)
        box(nm('rim'), (0.6, 0.5, 0.4), loc=(math.cos(a) * rr, math.sin(a) * rr, 0.2),
            key='wa_ice_clear', rot=(0, 0, math.degrees(a)), bev=0.03)
    # one slab leaning into the hole
    box(nm('slab'), (2.2, 1.6, 0.18), loc=(0.6, 0.3, 0.7), key='wa_ice_blue', rot=(28, 0, 14), bev=0.04)
    for i in range(8):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(1.8, 3.2)
        ball(nm('chunk'), rnd.uniform(0.2, 0.4), loc=(math.cos(a) * d, math.sin(a) * d, 0.18),
             key=rnd.choice(['wa_ice_clear', 'wa_ice_blue']), segs=6, rings=4, scale=(1.3, 1, 0.6))
    return finalize('fishing_hole_2', smooth_angle=25)


def fishing_hole_3():
    """A03_03 - two joined holes with an ice saw and a bucket beside."""
    reset()
    thick = 0.12
    box(nm('surf'), (11, 9, 0.1), loc=(0, 0, 0.05), key='wa_ice_block')
    rnd = random.Random(33)
    thick = 0.12
    box(nm('surf'), (9.0, 6.0, 0.12), loc=(0, 0, 0.06), key='wa_ice_block', bev=0.1)
    rnd = random.Random(33)
    for cxp in (-2.2, 2.2):
        cyl(nm('pl'), 2.4, thick, loc=(cxp, 0, 0), key='wa_ice_clear', verts=18)
        cyl(nm('water'), 1.1, 0.04, loc=(cxp, 0, 0.13), key='wa_water_dark', verts=16)
        for i in range(5):
            a = 2 * math.pi * i / 5 + rnd.uniform(-0.2, 0.2)
            tube(nm('crack'), [(cxp, 0, thick + 0.01), (cxp + math.cos(a) * 2.0, math.sin(a) * 2.0, thick + 0.01)],
                 0.04, 'wa_water_dark', res=4)
        n = 12
        for i in range(n):
            a = 2 * math.pi * i / n
            box(nm('rim'), (0.55, 0.45, 0.38), loc=(cxp + math.cos(a) * 1.2, math.sin(a) * 1.2, 0.19),
                key='wa_ice_clear', rot=(0, 0, math.degrees(a)), bev=0.03)
    # ice saw lying beside
    box(nm('sawbl'), (3.2, 0.5, 0.08), loc=(0, 3.0, 0.2), key='steel', rot=(0, 0, 18))
    for k in range(10):
        box(nm('tooth'), (0.12, 0.2, 0.12), loc=(-1.4 + k * 0.32, 3.0 - 0.3 + k * 0.1, 0.22), key='steel', rot=(0, 0, 18))
    box(nm('sawhand'), (0.6, 0.9, 0.3), loc=(1.6, 3.5, 0.3), key='wa_board_trim', rot=(0, 0, 18))
    # bucket
    lathe(nm('buck'), [(0, 0), (0.5, 0), (0.6, 1.0), (0.54, 1.0), (0.44, 0.1), (0, 0.1)],
          loc=(-3.5, 2.8, 0.0), key='wa_tin', segs=12)
    return finalize('fishing_hole_3', smooth_angle=25)


BATCHES = {
    'igloos':   ('v4_alpine', [('A01_01_igloo_01', igloo_1), ('A01_02_igloo_02', igloo_2), ('A01_03_igloo_03', igloo_3)]),
    'shanties': ('v4_alpine', [('A02_01_ice_shanty_01', ice_shanty_1), ('A02_02_ice_shanty_02', ice_shanty_2),
                               ('A02_03_ice_shanty_03', ice_shanty_3), ('A02_04_ice_shanty_04', ice_shanty_4)]),
    'holes':    ('v4_alpine', [('A03_01_fishing_hole_01', fishing_hole_1), ('A03_02_fishing_hole_02', fishing_hole_2),
                               ('A03_03_fishing_hole_03', fishing_hole_3)]),
}
