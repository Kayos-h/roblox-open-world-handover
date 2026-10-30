"""v4_wd2_chunk - CHUNK-BASED carved rock (replaces the soft grid-displacement method).

Why: displacing one dense grid and painting individual faces gives pillowy clay walls with
stair-stepped colour edges. Instead we ASSEMBLE rock from many distinct ANGULAR CHUNKS -
flat-shaded low-poly blocks/slabs (distorted cubes or low icospheres, 12-60 faces). Each chunk
is ONE geology colour (sampled from a low-frequency noise at the chunk centre, <=4 colours),
laid in irregular courses with jittered offset, +-8 deg tilt, some blocks protruding to form
ledges/overhangs, slanted cap slabs on top, talus boulders at the base. Crisp edges + chunky
silhouette read as carved rock from 30-60 studs.

Reusable entry points (another worker can import these for sea stacks, cliffs, canyon walls):
    chunk_rock_face(W, D, H, seed, keys, snow=.., moss=.., tile=True)   -> builds in-scene
    chunk_peak(H, Rbase, seed, keys, snow_line=.., ridge_dir=None)      -> builds in-scene
    chunk_arch(span, H, seed, keys)                                     -> voussoir arch
Call reset() before, finalize(name, smooth_angle=12) after (low angle keeps chunk edges hard).

Imports palette keys from v4_wd2_rock (registers wd2_* on import). No shared files edited.
"""
import math, random, bmesh
from mathutils import Vector, Matrix, noise as N
from kitlib import reset, finalize, PAL, mat, _obj_from_bm, _link, cyl, tube
from nature import rock, blob
from v4_elf import nm
import bpy
import v4_wd2_rock as R   # registers wd2_* palette keys and _fbm


def _lowfreq_colour(center, seed, keys, scale=0.05):
    """Pick ONE key for a whole chunk from a low-frequency noise at its centre (<=4 keys).
    keys: ordered list dark..light; noise in [-1,1] maps across them with soft thresholds."""
    n = R._fbm(Vector(center) * scale + Vector((seed * 1.7, seed * 0.9, 0)), seed + 3, octaves=2)
    k = len(keys)
    # map n (-1..1) to an index, biased so the middle tone is most common
    t = (n + 1) * 0.5
    t = t * t * (3 - 2 * t)                 # smoothstep -> fewer extremes
    return keys[min(k - 1, int(t * k))]


def _chunk(name, size, loc, key, seed=0, tilt=8.0, rough=0.26, faceted=True):
    """One angular rock chunk: a distorted low-poly cube (optionally an icosphere for a boulder).
    Flat-shaded, crisp edges. size=(sx,sy,sz) studs, loc=centre, tilt=max deg random tilt."""
    rnd = random.Random(seed)
    bm = bmesh.new()
    if faceted:
        bmesh.ops.create_cube(bm, size=1.0)
        # one or two subdivisions so corners can be chamfered irregularly (still chunky)
        bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=1, use_grid_fill=True)
    else:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.5)
    off = Vector((seed * 3.1, seed * 1.3, seed * 2.7))
    for v in bm.verts:
        p = v.co
        # jitter each vertex outward/inward by noise -> irregular faceted block, NOT a smooth box
        d = R._fbm(p * 2.2 + off, seed + 5, octaves=2)
        v.co = p * (1.0 + rough * d)
        v.co.x *= size[0]; v.co.y *= size[1]; v.co.z *= size[2]
    # knock a couple of corners off for angular breaks
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj_from_bm(name, bm, key)
    o.location = loc
    o.rotation_euler = (math.radians(rnd.uniform(-tilt, tilt)),
                        math.radians(rnd.uniform(-tilt, tilt)),
                        math.radians(rnd.uniform(0, 360)))
    return o


# ================================================================== CLIFF FACE (tiling)
def chunk_rock_face(W, D, H, seed, keys, snow=False, moss=False, snow_line=0.66,
                    course_h=6.5, name='face'):
    """Build a tiling cliff panel ~W wide x D deep x H tall, front toward -Y, from stacked
    courses of angular chunks. Left/right ends are mirrored to the same X so panels tile.
    keys: list of 2-4 geology colours (dark..light). snow/moss add a 4th/extra key on tops."""
    rnd = random.Random(seed)
    ncourse = max(3, int(H / course_h))
    snow_key = (keys[-1] if not snow else 'wd2_snow')
    # SOLID BACKING SLAB so no daylight shows through the chunk courses (viewer sees rock, not sky)
    from kitlib import box
    box(nm('back'), (W, D * 0.5, H), loc=(0, D * 0.28, H / 2), key=keys[0])
    for ci in range(ncourse):
        z0 = H * ci / ncourse
        ch = course_h * rnd.uniform(0.85, 1.2)
        zc = z0 + ch / 2
        t = zc / H
        # slight inward lean toward the top; each course recedes a touch
        back_lean = (t ** 1.1) * (D * 0.18)
        nblk = max(5, int(W / rnd.uniform(9, 12)))
        # jittered course offset so vertical joints never align (staggered like masonry)
        xs = [-W / 2 + W * (j + rnd.uniform(-0.15, 0.15)) / nblk for j in range(nblk + 1)]
        xs[0] = -W / 2; xs[-1] = W / 2                      # lock ends for tiling + width
        for j in range(nblk):
            cx = (xs[j] + xs[j + 1]) / 2
            bw = (xs[j + 1] - xs[j]) * rnd.uniform(1.25, 1.5)   # OVERLAP neighbours -> no gaps
            protrude = rnd.random() < 0.32
            by = -D / 2 * (0.5 + rnd.uniform(0, 0.3)) + back_lean - (rnd.uniform(1.4, 3.2) if protrude else 0)
            bz = zc + rnd.uniform(-0.4, 0.4)
            sz = (bw, D * rnd.uniform(0.6, 0.85), ch * rnd.uniform(1.05, 1.35))   # taller: courses overlap in z
            key = _lowfreq_colour((cx, 0, bz), seed, keys)
            # snow/moss: only on an up-facing protruding ledge top
            if snow and protrude and t > snow_line:
                key = 'wd2_snow'
            elif moss and protrude and t < 0.4 and rnd.random() < 0.4:
                key = 'wd2_moss'
            c = _chunk(nm('cf'), sz, (cx, by, bz), key, seed=seed + ci * 40 + j, tilt=6.0)
            # clamp the END blocks so the silhouette stays within +-W/2 for clean tiling
            if j == 0:
                c.location.x = -W / 2 + bw * 0.4
            elif j == nblk - 1:
                c.location.x = W / 2 - bw * 0.4
    # slanted cap slabs on the crown
    for j in range(max(3, int(W / 14))):
        cx = -W / 2 + W * (j + 0.5) / max(3, int(W / 14))
        key = 'wd2_snow' if snow else _lowfreq_colour((cx, 0, H), seed, keys)
        cap = _chunk(nm('cap'), (W / max(3, int(W / 14)) * 1.1, D * 0.5, H * 0.08),
                     (cx, -D * 0.1 + rnd.uniform(-1, 1), H - 1.0), key, seed=seed + 200 + j, tilt=10.0)
    # talus boulders at the base
    for j in range(int(W / 7)):
        x = rnd.uniform(-W / 2 + 2, W / 2 - 2)
        r = rnd.uniform(1.4, 3.2)
        rock(nm('tal'), r, (x, -D / 2 - rnd.uniform(0, 4), r * 0.3),
             _lowfreq_colour((x, 0, 0), seed, keys), seed=seed + 300 + j, scale=(1.3, 1.0, 0.7), subdiv=1, amp=0.4)


# ================================================================== PEAK (pile of tilted slabs)
def chunk_peak(H, Rbase, seed, keys, snow_line=0.5, ridge=None, name='peak'):
    """A mountain as a stack of tilted angular slabs narrowing upward to a sharp crest.
    ridge: optional (dx,dy) unit direction to stretch chunks along -> a serrated ridge.
    keys: 2-3 rock colours; snow added as white caps on up-facing chunk tops above snow_line."""
    rnd = random.Random(seed)
    nlayer = max(20, int(H / 4.0))
    for li in range(nlayer):
        t = li / nlayer
        z0 = H * t
        r = Rbase * (1 - t) ** 1.1 + 3.0
        # rings from the CENTRE outward (d = 0..r) at every height so the interior is packed with
        # chunks and no smooth surface is ever exposed - the whole mass is chunky rock.
        nrad = max(1, int(r / 9))
        for ri in range(nrad + 1):
            dfrac = ri / max(1, nrad)
            rad = r * dfrac
            nring = max(1, int(rad / 4.0)) if ri > 0 else 1
            for j in range(nring):
                a = 2 * math.pi * (j + rnd.uniform(-0.3, 0.3)) / nring
                rr = rad * rnd.uniform(0.85, 1.08)
                cx, cy = math.cos(a) * rr, math.sin(a) * rr
                if ridge and ri == nrad:               # only the OUTER ring follows the ridge line
                    cx = cx * 0.8 + ridge[0] * rr * 0.4
                    cy = cy * 0.8 + ridge[1] * rr * 0.4
                bz = z0 + rnd.uniform(-0.8, 0.8)
                slab_h = H / nlayer * rnd.uniform(2.0, 3.4)
                sw = max(5.0, (r / max(1, nrad)) * rnd.uniform(1.2, 1.8))
                sd = sw * rnd.uniform(0.8, 1.1)
                if ridge and ri == nrad:
                    sw *= 1.2; sd *= 0.9
                key = _lowfreq_colour((cx, cy, bz), seed, keys)
                c = _chunk(nm('pk'), (sw, sd, slab_h), (cx, cy, bz), key, seed=seed + li * 50 + ri * 7 + j, tilt=10.0)
                if t > snow_line and dfrac > 0.5 and rnd.random() < 0.85:   # snow on outer up-tops only
                    _chunk(nm('sn'), (sw * 0.98, sd * 0.98, slab_h * 0.3),
                           (cx, cy, bz + slab_h * 0.5), 'wd2_peak_snow', seed=seed + 500 + li * 50 + j, tilt=9.0)
    # sharp summit block(s)
    _chunk(nm('smt'), (6, 6, H * 0.08), (ridge[0] * 2 if ridge else 0, ridge[1] * 2 if ridge else 0, H - H * 0.03),
           'wd2_peak_snow' if snow_line < 0.9 else keys[-1], seed=seed + 900, tilt=14.0)
    # scree skirt
    for j in range(22):
        a = rnd.uniform(0, 2 * math.pi); d = Rbase * rnd.uniform(0.85, 1.3)
        rr = rnd.uniform(1.5, 3.5)
        rock(nm('scr'), rr, (math.cos(a) * d, math.sin(a) * d, rr * 0.25),
             _lowfreq_colour((math.cos(a) * d, math.sin(a) * d, 0), seed, keys),
             seed=seed + 600 + j, scale=(1.3, 1.0, 0.55), subdiv=1, amp=0.4)


# ================================================================== ARCH (voussoir wedges)
def chunk_arch(span, H, seed, keys, name='arch'):
    """A natural rock arch from wedge-shaped voussoir chunks over a clear opening."""
    rnd = random.Random(seed)
    n = 11
    for i in range(n):
        a = math.pi * i / (n - 1)
        x = -math.cos(a) * span / 2
        z = math.sin(a) * H + 2.0
        key = _lowfreq_colour((x, 0, z), seed, keys)
        w = span / n * 1.3
        # wedge: taller than wide, tilted to follow the arch tangent
        tangent = math.degrees(a) - 90
        c = _chunk(nm('vou'), (w, 6.0, 5.5 - math.sin(a) * 1.5), (x, 0, z), key, seed=seed + i, tilt=4.0)
        c.rotation_euler = (0, math.radians(tangent * 0.5), 0)
    # two piers
    for sgn in (-1, 1):
        for li in range(3):
            key = _lowfreq_colour((sgn * span / 2, 0, li * 3), seed, keys)
            _chunk(nm('pier'), (8, 7, 4), (sgn * span / 2, rnd.uniform(-0.5, 0.5), 1.5 + li * 3.2), key,
                   seed=seed + 50 + sgn * 10 + li, tilt=6.0)


# ================================================================== E13 builders
def _face(seed, keys, snow, moss, snow_line, name):
    reset()
    chunk_rock_face(70.0, 24.0, 58.0, seed, keys, snow=snow, moss=moss, snow_line=snow_line, name=name)
    return finalize(name, smooth_angle=12)

GRAN = ['wd2_granite_dk', 'wd2_granite', 'wd2_granite_lt']
SAND = ['wd2_sand_dk', 'wd2_sand', 'wd2_sand_lt']
BAS = ['wd2_basalt_dk', 'wd2_basalt', 'wd2_basalt_lt']

def rock_face_01(): return _face(3301, GRAN, True, True, 0.66, 'rock_face_01')
def rock_face_02(): return _face(3302, GRAN, True, True, 0.68, 'rock_face_02')
def rock_face_03(): return _face(3303, GRAN, True, True, 0.64, 'rock_face_03')
def rock_face_04(): return _face(3304, GRAN, True, True, 0.70, 'rock_face_04')
def rock_face_05(): return _face(3305, SAND, False, False, 0.9, 'rock_face_05')
def rock_face_06(): return _face(3306, SAND, False, False, 0.9, 'rock_face_06')
def rock_face_07(): return _face(3307, SAND, False, False, 0.9, 'rock_face_07')
def rock_face_08(): return _face(3308, BAS, False, True, 0.9, 'rock_face_08')
def rock_face_09(): return _face(3309, BAS, False, True, 0.9, 'rock_face_09')
def rock_face_10(): return _face(3310, BAS, False, True, 0.9, 'rock_face_10')


# ================================================================== R02 peaks
PEAK = ['wd2_peak_dk', 'wd2_peak', 'wd2_peak_dk']

def snow_peak_01():
    reset(); chunk_peak(165.0, 46.0, 3411, PEAK, snow_line=0.42, name='snow_peak_01')
    return finalize('snow_peak_01', smooth_angle=12)

def snow_peak_02():
    reset(); chunk_peak(150.0, 50.0, 3412, PEAK, snow_line=0.46, ridge=(1.0, 0.0), name='snow_peak_02')
    return finalize('snow_peak_02', smooth_angle=12)

def snow_peak_03():
    reset(); chunk_peak(140.0, 54.0, 3413, PEAK, snow_line=0.5, ridge=(0.3, 1.0), name='snow_peak_03')
    return finalize('snow_peak_03', smooth_angle=12)

def snow_peak_04():
    reset()
    chunk_peak(135.0, 58.0, 3414, PEAK, snow_line=0.5, name='snow_peak_04')
    # hanging glacier shelf: a flat tilted ice slab part-way up one flank
    rnd = random.Random(3414)
    for j in range(5):
        _chunk(nm('ice'), (rnd.uniform(8, 14), rnd.uniform(8, 12), 2.2),
               (-28 + rnd.uniform(-4, 4), -30 + rnd.uniform(-4, 4), 60 + rnd.uniform(-3, 3)),
               'wd2_ice', seed=3414 + 700 + j, tilt=8.0)
    return finalize('snow_peak_04', smooth_angle=12)


# ================================================================== R01 islets (chunk)
def islet_01():
    reset()
    chunk_peak(44.0, 17.0, 3401, ['wd2_isle_dk', 'wd2_isle', 'wd2_isle_dk'], snow_line=2.0, name='islet_01')
    # grassy crown + pines
    cyl(nm('cap'), 7.5, 1.0, loc=(0, 0, 43.0), key='wd2_dirt', verts=16)
    blob(nm('g'), 7.4, (0, 0, 43.8), 'wd2_grass', subdiv=2, amp=0.12, scale=(1, 1, 0.18), seed=3401, flat_bottom=-0.1)
    rnd = random.Random(3401)
    for i in range(4):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, 5)
        R2 = __import__('v4_wd2_rock')
        x, y = math.cos(a) * d, math.sin(a) * d
        h = rnd.uniform(5, 8)
        cyl(nm('tr'), h * 0.05, h * 0.3, loc=(x, y, 44.0), key='wd_trunk', verts=5)
        for k in range(3):
            rr = h * 0.22 * (1 - k / 3)
            cyl(nm('pc'), rr, h * 0.32, loc=(x, y, 44.0 + h * (0.22 + 0.24 * k)), key='wd_pine', verts=6, r2=rr * 0.15)
    return finalize('islet_01', smooth_angle=14)

def islet_04():
    reset()
    # two piers + voussoir arch between them
    chunk_arch(26.0, 30.0, 3404, ['wd2_isle_dk', 'wd2_isle', 'wd2_isle_dk'], name='islet_04')
    # taller left leg with a grassy cap + pines
    rnd = random.Random(3404)
    for li in range(5):
        _chunk(nm('leg'), (9, 8, 5), (-13, rnd.uniform(-1, 1), 2.5 + li * 5.2),
               _lowfreq_colour((-13, 0, li * 5), 3404, ['wd2_isle_dk', 'wd2_isle']), seed=3404 + li, tilt=7.0)
    cyl(nm('cap'), 5.0, 0.9, loc=(-13, 0, 29.0), key='wd2_dirt', verts=14)
    blob(nm('g'), 4.8, (-13, 0, 29.7), 'wd2_grass', subdiv=2, amp=0.12, scale=(1, 1, 0.2), seed=3404, flat_bottom=-0.1)
    for i in range(3):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, 3)
        x, y = -13 + math.cos(a) * d, math.sin(a) * d
        h = rnd.uniform(5, 7)
        cyl(nm('tr'), h * 0.05, h * 0.3, loc=(x, y, 29.5), key='wd_trunk', verts=5)
        for k in range(3):
            rr = h * 0.22 * (1 - k / 3)
            cyl(nm('pc'), rr, h * 0.32, loc=(x, y, 29.5 + h * (0.22 + 0.24 * k)), key='wd_pine', verts=6, r2=rr * 0.15)
    return finalize('islet_04', smooth_angle=14)


# ================================================================== R03 mesas (chunk, banded)
BL = ['wd2_bl_red', 'wd2_bl_orange', 'wd2_bl_sand', 'wd2_bl_cream']

def _mesa(seed, H, Rbase, Rtop, name, butte=False):
    reset()
    rnd = random.Random(seed)
    ncourse = max(5, int(H / 5.5))
    for ci in range(ncourse):
        t = ci / ncourse
        z0 = H * t
        ch = H / ncourse
        r = (Rbase * (1 - 0.45 * t) if butte else Rbase * (1 - 0.14 * t))
        if t > 0.86:
            r = (Rbase * 0.58 if butte else Rbase * 0.86)
        # a whole course shares ONE band colour (crisp horizontal strata, not pixel rows)
        band = BL[ci % 4]
        nring = max(6, int(2 * math.pi * r / 8))
        for j in range(nring):
            a = 2 * math.pi * j / nring + rnd.uniform(-0.1, 0.1)
            rr = r * rnd.uniform(0.95, 1.05)
            cx, cy = math.cos(a) * rr, math.sin(a) * rr
            sw = 2 * math.pi * r / nring * rnd.uniform(1.0, 1.3)
            _chunk(nm('me'), (sw, sw * 0.8, ch * rnd.uniform(1.0, 1.25)), (cx, cy, z0 + ch / 2),
                   band, seed=seed + ci * 40 + j, tilt=5.0)
    # flat cap
    rtop = (Rbase * 0.58 if butte else Rbase * 0.86)
    cyl(nm('cap'), rtop, 2.0, loc=(0, 0, H - 1.0), key='wd2_bl_cream', verts=max(8, int(rtop)))
    # talus
    for j in range(int(Rbase / 3)):
        a = rnd.uniform(0, 6.28); d = Rbase * rnd.uniform(0.9, 1.25)
        rr = rnd.uniform(1.5, 3.2)
        rock(nm('tal'), rr, (math.cos(a) * d, math.sin(a) * d, rr * 0.25), 'wd2_bl_talus',
             seed=seed + 300 + j, scale=(1.4, 1.0, 0.5), subdiv=1, amp=0.4)
    return finalize(name, smooth_angle=12)

def badlands_mesa_01(): return _mesa(3421, 52.0, 44.0, 20.0, 'badlands_mesa_01')
def badlands_mesa_02(): return _mesa(3422, 78.0, 24.0, 10.0, 'badlands_mesa_02', butte=True)

def badlands_mesa_03():
    reset()
    rnd = random.Random(3423)
    for sgn, hh in ((-1, 70.0), (1, 56.0)):
        ncourse = int(hh / 5.5)
        for ci in range(ncourse):
            t = ci / ncourse; z0 = hh * t; ch = hh / ncourse
            r = 16.0 * (1 - 0.4 * t)
            band = BL[ci % 4]
            nring = max(5, int(2 * math.pi * r / 8))
            for j in range(nring):
                a = 2 * math.pi * j / nring
                rr = r * rnd.uniform(0.95, 1.05)
                _chunk(nm('tb'), (2 * math.pi * r / nring * 1.2, r * 0.5, ch * 1.1),
                       (sgn * 20 + math.cos(a) * rr, math.sin(a) * rr, z0 + ch / 2), band,
                       seed=3423 + int(sgn) * 100 + ci * 20 + j, tilt=5.0)
        cyl(nm('cap'), 16.0 * 0.6, 2.0, loc=(sgn * 20, 0, hh - 1.0), key='wd2_bl_cream', verts=12)
    for j in range(12):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(28, 42)
        rr = rnd.uniform(1.5, 3.0)
        rock(nm('tal'), rr, (math.cos(a) * d, math.sin(a) * d, rr * 0.25), 'wd2_bl_talus', seed=3423 + 400 + j,
             scale=(1.4, 1.0, 0.5), subdiv=1, amp=0.4)
    return finalize('badlands_mesa_03', smooth_angle=12)

def badlands_mesa_04():
    reset()
    _mesa_body = _mesa  # reuse via a notch cut
    rnd = random.Random(3424)
    H, Rbase = 56.0, 40.0
    ncourse = int(H / 5.5)
    for ci in range(ncourse):
        t = ci / ncourse; z0 = H * t; ch = H / ncourse
        r = Rbase * (1 - 0.18 * t)
        band = BL[ci % 4]
        nring = max(6, int(2 * math.pi * r / 8))
        for j in range(nring):
            a = 2 * math.pi * j / nring
            # notch: skip chunks on the +x shoulder in the upper half
            if t > 0.55 and -0.5 < a < 0.5:
                continue
            rr = r * rnd.uniform(0.95, 1.05)
            _chunk(nm('me'), (2 * math.pi * r / nring * 1.2, r * 0.45, ch * 1.1),
                   (math.cos(a) * rr, math.sin(a) * rr, z0 + ch / 2), band, seed=3424 + ci * 20 + j, tilt=5.0)
    cyl(nm('cap'), Rbase * 0.82, 2.0, loc=(0, 0, H - 1.0), key='wd2_bl_cream', verts=16)
    # small arch on the -Y front
    chunk_arch(16.0, 16.0, 3424 + 99, BL)
    for j in range(12):
        a = rnd.uniform(0, 6.28); d = Rbase * rnd.uniform(0.9, 1.2)
        rr = rnd.uniform(1.5, 3.0)
        rock(nm('tal'), rr, (math.cos(a) * d, math.sin(a) * d, rr * 0.25), 'wd2_bl_talus', seed=3424 + 400 + j,
             scale=(1.4, 1.0, 0.5), subdiv=1, amp=0.4)
    return finalize('badlands_mesa_04', smooth_angle=12)


# ================================================================== batches
BATCHES = {
    'e13': ('v4_terrain', [('E13_%02d_rock_face_%02d' % (i, i), globals()['rock_face_%02d' % i], (0.0, -1.0, 0.18)) for i in range(1, 11)]),
    'r01': ('v4_terrain', [('R01_01_islet_01', islet_01, (0.6, -1.2, 0.4)), ('R01_04_islet_04', islet_04, (0.6, -1.2, 0.4))]),
    'r02': ('v4_terrain', [('R02_%02d_snow_peak_%02d' % (i, i), globals()['snow_peak_%02d' % i], (0.5, -1.2, 0.3)) for i in range(1, 5)]),
    'r03': ('v4_terrain', [('R03_%02d_badlands_mesa_%02d' % (i, i), globals()['badlands_mesa_%02d' % i], (0.6, -1.2, 0.35)) for i in range(1, 5)]),
}
