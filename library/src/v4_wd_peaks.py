"""v4_wd_peaks - R01 islet, R02 snow_peak, R03 badlands_mesa (12 models). Worker wd.

Free-standing landforms. Core method: a dense bmesh dome/cone/ellipsoid, displaced by several
octaves of mathutils.noise, strata by banding height, overhangs and ledges, then materials per
face from height / slope / noise (rock bands, snow on up-slopes, moss, scree). Base kept flat at
z=0 with a scree-and-boulder skirt so it blends into terrain. Rock <= 40k tris. New palette keys
prefixed wd_. Do not edit shared files; import only.
"""
import math, random, bmesh
from mathutils import Vector, noise as N
from kitlib import reset, finalize, PAL, _obj_from_bm, mat, cyl, tube
from nature import rock, blob
from v4_elf import nm

# ------------------------------------------------------------------ palette (wd_ prefixed, reuse E13 where set)
for k, v in {
    'wd_rock_grey':   ((120, 122, 128), 'Rock', 0.00, 0.95, 0),
    'wd_rock_dark':   ((84, 86, 94),    'Rock', 0.00, 0.96, 0),
    'wd_rock_light':  ((160, 162, 170), 'Rock', 0.00, 0.92, 0),
    'wd_peak_snow':   ((240, 244, 250), 'Snow', 0.00, 0.68, 0),
    'wd_scree':       ((104, 104, 110), 'Rock', 0.00, 0.98, 0),
    'wd_grass':       ((96, 132, 62),   'Grass', 0.00, 1.00, 0),
    'wd_grass_dry':   ((150, 148, 92),  'Grass', 0.00, 1.00, 0),
    'wd_dirt':        ((110, 88, 62),   'Ground', 0.00, 1.00, 0),
    'wd_ice':         ((206, 228, 240), 'Glass', 0.00, 0.25, 0),
    # badlands reds/oranges/sand/cream
    'wd_bl_red':      ((158, 82, 54),   'Sandstone', 0.00, 0.92, 0),
    'wd_bl_orange':   ((192, 114, 62),  'Sandstone', 0.00, 0.90, 0),
    'wd_bl_sand':     ((198, 158, 104), 'Sandstone', 0.00, 0.90, 0),
    'wd_bl_cream':    ((222, 196, 150), 'Sandstone', 0.00, 0.88, 0),
    'wd_bl_dark':     ((124, 66, 44),   'Sandstone', 0.00, 0.93, 0),
    'wd_bl_talus':    ((176, 120, 74),  'Sandstone', 0.00, 0.95, 0),
    # island cliff + pine
    'wd_isle_rock':   ((132, 124, 110), 'Rock', 0.00, 0.95, 0),
    'wd_isle_dark':   ((98, 92, 82),    'Rock', 0.00, 0.96, 0),
    'wd_pine':        ((46, 86, 56),    'LeafyGrass', 0.00, 0.90, 0),
    'wd_pine_dark':   ((34, 68, 48),    'LeafyGrass', 0.00, 0.90, 0),
    'wd_oak':         ((78, 118, 58),   'LeafyGrass', 0.00, 0.90, 0),
    'wd_trunk':       ((88, 66, 48),    'Wood', 0.00, 0.95, 0),
}.items():
    PAL[k] = v


# ------------------------------------------------------------------ landform core
def _landform(nx, nz, radius_fn, seed, octs, strata_h=0.0, overhang=0.0, warp=1.0,
              taper_pow=1.6, flat_base=True, name_key='lf'):
    """Build a closed landform surface. For each ring at height parameter t in [0,1] the base
    radius is radius_fn(t); vertices are pushed out/in by multi-octave noise, banded into strata
    by z when strata_h>0, and given overhangs. Returns the object (not finalized), z from 0 up.
    H is encoded by radius_fn's own z (radius_fn returns (r, z))."""
    bm = bmesh.new()
    rings = []
    apex = None
    for iz in range(nz + 1):
        t = iz / nz
        r, z = radius_fn(t)
        if r < 0.25:
            apex = bm.verts.new((N.noise(Vector((seed, seed, z))) * 0.4, 0, z))
            rings.append([apex])
            continue
        ring = []
        for ix in range(nx):
            a = 2 * math.pi * ix / nx
            cx, cy = math.cos(a), math.sin(a)
            # multi-octave noise sampled on a cylinder (continuous around a)
            disp = 0.0
            asum = 0.0
            for (fr, amp) in octs:
                p = Vector((cx * fr + seed * 1.3, cy * fr + seed * 2.1, z * fr * 0.08 + seed * 0.7))
                disp += amp * N.noise(p)
                asum += amp
            disp /= asum
            rr = r * (1.0 + warp * 0.5 * disp)
            # strata: quantise radius by bed so beds step in/out -> layered rock
            if strata_h > 0:
                L = int(z / strata_h)
                bed = ((L * 73 + seed) % 5) / 4.0 - 0.5
                rr += bed * strata_h * 0.9
                fz = (z - L * strata_h) / strata_h
                rr += overhang * math.sin(math.pi * min(1.0, fz))   # protruding shelf lip
            # vertical fluting grooves
            fl = math.sin(a * (10 + (seed % 5)) + disp * 2.0)
            rr += 0.4 * warp * fl * (0.4 + 0.6 * t)
            ring.append(bm.verts.new((cx * rr, cy * rr, z)))
        rings.append(ring)
    # stitch rings
    for A, B in zip(rings, rings[1:]):
        if len(A) == 1 and len(B) == 1:
            continue
        if len(B) == 1:
            for i in range(len(A)):
                bm.faces.new((A[i], B[0], A[(i + 1) % len(A)]))
        elif len(A) == 1:
            for i in range(len(B)):
                bm.faces.new((A[0], B[i], B[(i + 1) % len(B)]))
        else:
            n = len(A)
            for i in range(n):
                bm.faces.new((A[i], A[(i + 1) % n], B[(i + 1) % n], B[i]))
    # flat base cap at z=0 (first ring)
    if flat_base and len(rings[0]) > 1:
        bm.faces.new(list(reversed(rings[0])))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj_from_bm(name_key + '_body', bm, 'wd_rock_grey')
    return o


def _paint(o, seed, rules, H):
    """rules: list of (key, predicate(center, nz, ny, t, noise)) evaluated in order; first True wins.
    Last rule should be a catch-all."""
    me = o.data
    keys = []
    for k, _ in rules:
        if k not in keys:
            keys.append(k)
    present = [m.name.split('|')[0] for m in me.materials]
    for k in keys:
        if k not in present:
            me.materials.append(mat(k)); present.append(k)
    idx = {m.name.split('|')[0]: i for i, m in enumerate(me.materials)}
    bm = bmesh.new(); bm.from_mesh(me)
    off = Vector((seed * 3.7, seed * 1.9, seed * 0.5))
    for f in bm.faces:
        c = f.calc_center_median()
        nrm = f.normal
        nz_ = nrm.z
        ny = nrm.y
        t = max(0.0, min(1.0, c.z / H))
        nv = N.noise(c * 0.2 + off)
        for k, pred in rules:
            if pred(c, nz_, ny, t, nv):
                f.material_index = idx[k]
                break
    bm.to_mesh(me); bm.free(); me.update()
    return o


def _scree_skirt(seed, R, keys, n=16, zmax=0.4, spread=1.25, scale=(1.3, 1.0, 0.6)):
    rnd = random.Random(seed + 700)
    for i in range(n):
        a = rnd.uniform(0, 2 * math.pi)
        d = R * rnd.uniform(0.85, spread)
        r = rnd.uniform(0.8, 2.6)
        rock(nm('scr'), r, (math.cos(a) * d, math.sin(a) * d, r * 0.25 + rnd.uniform(0, zmax)),
             rnd.choice(keys), seed=seed + i, scale=scale, subdiv=2, amp=0.34)


# ------------------------------------------------------------------ low-poly trees (for islets, tiny)
def _mini_pine(x, y, z, h, seed):
    rnd = random.Random(seed)
    cyl(nm('tr'), h * 0.05, h * 0.3, loc=(x, y, z), key='wd_trunk', verts=5)
    tiers = 3
    for i in range(tiers):
        tt = i / tiers
        r = h * 0.22 * (1 - tt)
        cyl(nm('pc'), r, h * 0.32, loc=(x, y, z + h * (0.22 + 0.24 * i)), key=rnd.choice(('wd_pine', 'wd_pine_dark')), verts=6, r2=r * 0.15)


def _mini_oak(x, y, z, h, seed):
    rnd = random.Random(seed)
    cyl(nm('tr'), h * 0.07, h * 0.4, loc=(x, y, z), key='wd_trunk', verts=5)
    blob(nm('cr'), h * 0.3, (x, y, z + h * 0.6), rnd.choice(('wd_oak', 'wd_pine')), subdiv=1, amp=0.28, scale=(1, 1, 0.9), seed=seed)


def _tree_cap(cx, cy, ztop, rtop, n, seed, kinds=('pine',)):
    """Scatter n small trees on a flattish top disc of radius rtop at height ztop. Deterministic."""
    rnd = random.Random(seed + 300)
    for i in range(n):
        a = rnd.uniform(0, 2 * math.pi)
        d = rtop * math.sqrt(rnd.random()) * 0.85
        x, y = cx + math.cos(a) * d, cy + math.sin(a) * d
        h = rnd.uniform(5.0, 8.0)
        kind = rnd.choice(kinds)
        if kind == 'pine':
            _mini_pine(x, y, ztop - 0.3, h, seed + i)
        else:
            _mini_oak(x, y, ztop - 0.3, h, seed + i)


# ================================================================== R01 ISLETS
ISLE_RULES = lambda H: [
    ('wd_grass', lambda c, nz, ny, t, nv: nz > 0.6 and t > 0.82),
    ('wd_dirt', lambda c, nz, ny, t, nv: nz > 0.45 and t > 0.72),
    ('wd_isle_dark', lambda c, nz, ny, t, nv: nv < -0.15 or t < 0.18),
    ('wd_isle_rock', lambda c, nz, ny, t, nv: True),
]


def _grass_cap(cx, cy, ztop, r, seed):
    """A flat-ish grassy top disc (dirt rim under) so trees sit on grass, not bare rock."""
    cyl(nm('cap'), r, 0.9, loc=(cx, cy, ztop - 0.45), key='wd_dirt', verts=18)
    return blob(nm('gtop'), r * 0.98, (cx, cy, ztop + 0.1), 'wd_grass', subdiv=2, amp=0.12,
                scale=(1.0, 1.0, 0.18), seed=seed, flat_bottom=-0.1)


def _islet(seed, H, Rbase, Rtop, ntrees, kinds, shape='stack', name='islet'):
    reset()
    rnd = random.Random(seed)

    def rfn(t):
        z = H * t
        if shape == 'stack':           # steep near-vertical sides, slight inward taper
            r = Rbase * (1 - 0.5 * t) ** 1.15 + Rtop * t
        elif shape == 'mesa':          # wide, flat top
            r = Rbase * (1 - 0.12 * t) if t < 0.85 else Rbase * 0.88 * (1 - (t - 0.85) / 0.15) + Rtop
        else:
            r = Rbase * (1 - 0.5 * t) ** 1.1 + Rtop * t
        return (max(r, Rtop * 0.9), z)

    o = _landform(44, 30, rfn, seed, [(1.0, 1.0), (2.3, 0.45), (4.6, 0.24), (9.0, 0.12)],
                  strata_h=6.5, overhang=0.45, warp=0.8, name_key=name)
    _paint(o, seed, ISLE_RULES(H), H)
    _scree_skirt(seed, Rbase * 0.92, ('wd_isle_rock', 'wd_isle_dark', 'wd_scree'), n=14, spread=1.3)
    for i in range(8):
        a = rnd.uniform(0, 2 * math.pi)
        rock(nm('wb'), rnd.uniform(1.2, 2.4), (math.cos(a) * Rbase * 1.02, math.sin(a) * Rbase * 1.02, 0.3),
             rnd.choice(('wd_isle_dark', 'wd_isle_rock')), seed=seed + 40 + i, scale=(1.3, 1.1, 0.55), subdiv=2, amp=0.3)
    _grass_cap(0, 0, H * 0.985, Rtop * 1.1, seed)
    _tree_cap(0, 0, H * 1.03, Rtop, ntrees, seed, kinds)
    return finalize(name, smooth_angle=22)


def islet_01():
    """Tall single sea stack, steep cliffs, small grassy crown with a few pines."""
    return _islet(1, 44.0, 18.0, 7.0, 4, ('pine',), 'stack', 'islet_01')

def islet_02():
    """Wide mesa-like islet, broad flat grassy top with a mix of pines and oaks."""
    return _islet(2, 28.0, 28.0, 20.0, 7, ('pine', 'oak'), 'mesa', 'islet_02')


def islet_03():
    """Twin-peak islet: two distinct stacks on a shared base, a clear saddle between, pines on both."""
    reset()
    seed = 3
    rnd = random.Random(seed)
    H = 40.0

    def rfn(t):
        z = H * t
        r = 24.0 * (1 - 0.5 * t) ** 1.1 + 5.0 * t
        return (max(r, 5.0), z)
    o = _landform(48, 30, rfn, seed, [(1.0, 1.0), (2.0, 0.5), (4.0, 0.26), (8.0, 0.13)],
                  strata_h=6.5, overhang=0.5, warp=0.8, name_key='islet_03')
    # strong saddle: deeply drop the central x-band in the upper 60% -> two separate summits
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts:
        if v.co.z > H * 0.4:
            up = (v.co.z - H * 0.4) / (H * 0.6)
            v.co.z -= 0.85 * H * 0.5 * math.exp(-(v.co.x / 5.0) ** 2) * up
            if v.co.x > 0:
                v.co.z *= 0.88    # second summit a bit lower
    bm.to_mesh(me); bm.free(); me.update()
    _paint(o, seed, ISLE_RULES(H), H)
    _scree_skirt(seed, 22.0, ('wd_isle_rock', 'wd_isle_dark', 'wd_scree'), n=14, spread=1.3)
    for i in range(8):
        a = rnd.uniform(0, 2 * math.pi)
        rock(nm('wb'), rnd.uniform(1.2, 2.2), (math.cos(a) * 22.0, math.sin(a) * 22.0, 0.3),
             'wd_isle_dark', seed=seed + 40 + i, scale=(1.3, 1.1, 0.55), subdiv=2, amp=0.3)
    _grass_cap(-9.0, 0, H * 0.96, 4.5, seed)
    _grass_cap(9.0, 0, H * 0.845, 4.2, seed + 1)
    _tree_cap(-9.0, 0, H * 0.99, 4.0, 3, seed, ('pine',))
    _tree_cap(9.0, 0, H * 0.875, 3.6, 2, seed + 20, ('pine',))
    return finalize('islet_03', smooth_angle=22)


def islet_04():
    """Arch islet: two rock legs bridged by a thick natural arch with a clear opening, grassy cap above."""
    reset()
    seed = 4
    rnd = random.Random(seed)
    H = 36.0
    # two steep legs straddling the -Y/+Y line, spaced along X, that the arch bridges
    for sgn, hh, rr in ((-1, 30.0, 8.0), (1, 26.0, 7.0)):
        def legr(t, hh=hh, rr=rr):
            return (max(rr * (1 - 0.45 * t), rr * 0.5), hh * t)
        leg = _landform(32, 22, legr, seed + (0 if sgn < 0 else 7),
                        [(1.0, 1.0), (2.3, 0.45), (4.6, 0.24)], strata_h=6.0, overhang=0.5, warp=0.8,
                        name_key='islet_04_%d' % sgn)
        leg.location = (sgn * 11.0, 0, 0)
        _paint(leg, seed + (0 if sgn < 0 else 7), ISLE_RULES(hh), hh)
    # the arch span: a thick bowed band from leg to leg, high enough to leave a clear gap beneath
    xs = [-11.0, -6.0, 0.0, 6.0, 11.0]
    zs = [27.0, 32.0, 35.0, 31.0, 24.0]
    pts = [(x, 0.0, z) for x, z in zip(xs, zs)]
    tube(nm('arch'), pts, 3.6, 'wd_isle_rock', res=7, ures=5, taper=[0.9, 1.0, 1.05, 1.0, 0.9])
    # a second thinner band behind for depth
    tube(nm('arch2'), [(x, 4.5, z - 0.6) for x, z in zip(xs, zs)], 2.6, 'wd_isle_dark', res=6, ures=4,
         taper=[0.9, 1.0, 1.0, 1.0, 0.9])
    _scree_skirt(seed, 20.0, ('wd_isle_rock', 'wd_isle_dark', 'wd_scree'), n=12, spread=1.25)
    for i in range(7):
        a = rnd.uniform(0, 2 * math.pi)
        rock(nm('wb'), rnd.uniform(1.2, 2.2), (math.cos(a) * 19.0, math.sin(a) * 19.0, 0.3),
             'wd_isle_dark', seed=seed + 40 + i, scale=(1.3, 1.1, 0.55), subdiv=2, amp=0.3)
    # grassy crown with pines on the taller (left) leg top
    _grass_cap(-11.0, 0, 29.5, 5.0, seed)
    _tree_cap(-11.0, 0, 30.5, 4.2, 3, seed, ('pine',))
    return finalize('islet_04', smooth_angle=22)


# ================================================================== R02 SNOW PEAKS
def _peak_rules(H, snow_line):
    return [
        ('wd_peak_snow', lambda c, nz, ny, t, nv: nz > 0.3 and t > snow_line + 0.08 * nv),
        ('wd_rock_dark', lambda c, nz, ny, t, nv: nz < 0.2 or nv < -0.2),
        ('wd_rock_light', lambda c, nz, ny, t, nv: nv > 0.35),
        ('wd_rock_grey', lambda c, nz, ny, t, nv: True),
    ]


def _snow_peak(seed, H, Rbase, rfn, snow_line, name, extra=None):
    reset()
    rnd = random.Random(seed)
    o = _landform(48, 40, rfn, seed, [(1.0, 1.0), (2.1, 0.6), (4.2, 0.34), (8.4, 0.2), (16.0, 0.1)],
                  strata_h=0.0, overhang=0.0, warp=1.35, taper_pow=1.8, name_key=name)
    _paint(o, seed, _peak_rules(H, snow_line), H)
    if extra:
        extra(rnd)
    _scree_skirt(seed, Rbase * 0.9, ('wd_rock_grey', 'wd_rock_dark', 'wd_scree'), n=20, spread=1.35, scale=(1.3, 1.0, 0.55))
    return finalize(name, smooth_angle=24)


def snow_peak_01():
    """Single sharp horn: a classic steep pyramidal summit, snow above a ragged line."""
    H, Rb = 170.0, 62.0
    rfn = lambda t: (Rb * (1 - t) ** 1.9 + 1.5, H * t)
    return _snow_peak(11, H, Rb, rfn, 0.5, 'snow_peak_01')


def snow_peak_02():
    """Double summit: two horns of unequal height sharing a massif."""
    H, Rb = 160.0, 66.0
    seed = 12

    def rfn(t):
        z = H * t
        r = Rb * (1 - t) ** 1.6 + 2.0
        return (r, z)

    def carve(rnd):
        pass
    reset()
    o = _landform(50, 40, rfn, seed, [(1.0, 1.0), (2.1, 0.6), (4.2, 0.34), (8.4, 0.2), (16.0, 0.1)],
                  warp=1.3, name_key='snow_peak_02')
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts:
        if v.co.z > H * 0.5:
            # split into two summits along x
            v.co.z *= 1.0 - 0.42 * math.exp(-(v.co.x / 9.0) ** 2) * ((v.co.z - H * 0.5) / (H * 0.5))
            if v.co.x > 0:
                v.co.z *= 0.9   # second summit lower
    bm.to_mesh(me); bm.free(); me.update()
    _paint(o, seed, _peak_rules(H, 0.46), H)
    _scree_skirt(seed, Rb * 0.9, ('wd_rock_grey', 'wd_rock_dark', 'wd_scree'), n=20, spread=1.35, scale=(1.3, 1.0, 0.55))
    return finalize('snow_peak_02', smooth_angle=24)


def snow_peak_03():
    """Long serrated ridge: an elongated crest with several jagged points."""
    H, Rb = 150.0, 70.0
    seed = 13
    reset()

    def rfn(t):
        z = H * t
        r = Rb * (1 - t) ** 1.4 + 2.5
        return (r, z)
    o = _landform(56, 38, rfn, seed, [(1.0, 1.0), (2.1, 0.6), (4.2, 0.34), (8.4, 0.2), (16.0, 0.12)],
                  warp=1.3, name_key='snow_peak_03')
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts:
        # stretch along Y into a ridge, then serrate the crest in Y
        v.co.y *= 1.7
        if v.co.z > H * 0.4:
            serr = 0.82 + 0.18 * math.sin(v.co.y * 0.22 + seed)
            v.co.z *= serr if abs(v.co.x) < 12 else 1.0
    bm.to_mesh(me); bm.free(); me.update()
    _paint(o, seed, _peak_rules(H, 0.5), H)
    _scree_skirt(seed, Rb * 1.1, ('wd_rock_grey', 'wd_rock_dark', 'wd_scree'), n=24, spread=1.4, scale=(1.4, 1.0, 0.5))
    return finalize('snow_peak_03', smooth_angle=24)


def snow_peak_04():
    """Broad peak with a hanging glacier shelf: a wide summit and a flat ice bench on one flank."""
    H, Rb = 140.0, 78.0
    seed = 14
    reset()

    def rfn(t):
        z = H * t
        r = Rb * (1 - t) ** 1.3 + 3.0
        return (r, z)
    o = _landform(52, 40, rfn, seed, [(1.0, 1.0), (2.1, 0.6), (4.2, 0.34), (8.4, 0.2)],
                  warp=1.2, name_key='snow_peak_04')
    _paint(o, seed, _peak_rules(H, 0.5), H)

    # hanging glacier shelf: a flat-ish ice slab on the -Y flank, mid height
    def shelfr(t):
        return (26.0 * (1 - 0.2 * t), 18.0 * t)
    shelf = _landform(30, 10, shelfr, seed + 7, [(1.0, 0.6), (2.0, 0.3)], warp=0.5, name_key='snow_peak_04ice')
    shelf.location = (0, -40.0, H * 0.46)
    _paint(shelf, seed + 7, [('wd_ice', lambda c, nz, ny, t, nv: nz > 0.3),
                             ('wd_peak_snow', lambda c, nz, ny, t, nv: True)], 18.0)
    _scree_skirt(seed, Rb * 0.95, ('wd_rock_grey', 'wd_rock_dark', 'wd_scree'), n=22, spread=1.35, scale=(1.3, 1.0, 0.55))
    return finalize('snow_peak_04', smooth_angle=24)


# ================================================================== R03 BADLANDS MESAS
def _bl_rules(H):
    # horizontal strata bands in red / orange / sand / cream by height stripes; talus at base; dry top
    def stripe(c, nz, ny, t, nv):
        s = int((c.z / 3.0 + 0.4 * nv)) % 5
        return ('wd_bl_dark', 'wd_bl_red', 'wd_bl_orange', 'wd_bl_sand', 'wd_bl_cream')[s]
    return stripe


def _paint_badlands(o, seed, H):
    me = o.data
    for k in ('wd_bl_dark', 'wd_bl_red', 'wd_bl_orange', 'wd_bl_sand', 'wd_bl_cream', 'wd_grass_dry', 'wd_bl_talus'):
        if k not in [m.name.split('|')[0] for m in me.materials]:
            me.materials.append(mat(k))
    idx = {m.name.split('|')[0]: i for i, m in enumerate(me.materials)}
    bm = bmesh.new(); bm.from_mesh(me)
    off = Vector((seed * 2.3, seed * 1.1, 0))
    for f in bm.faces:
        c = f.calc_center_median()
        nz_ = f.normal.z
        t = c.z / H
        nv = N.noise(c * 0.18 + off)
        if nz_ > 0.78 and t > 0.8:
            pick = 'wd_grass_dry'           # sparse dry top
        elif t < 0.12:
            pick = 'wd_bl_talus'            # talus at the foot
        else:
            s = int(c.z / 3.2 + 0.5 * nv) % 5
            pick = ('wd_bl_dark', 'wd_bl_red', 'wd_bl_orange', 'wd_bl_sand', 'wd_bl_cream')[s]
        f.material_index = idx[pick]
    bm.to_mesh(me); bm.free(); me.update()
    return o


def _mesa(seed, H, Rbase, Rtop, name, shape='mesa', fluting=1.4):
    reset()
    rnd = random.Random(seed)

    def rfn(t):
        z = H * t
        if shape == 'mesa':
            if t < 0.78:
                r = Rbase * (1 - 0.18 * t)
            else:
                r = (Rbase * 0.85) * (1 - (t - 0.78) / 0.22 * 0.1)   # keep flat top, tiny cap
            return (max(r, Rtop), z)
        elif shape == 'butte':             # narrow tower
            r = Rbase * (1 - 0.5 * t) if t < 0.8 else Rbase * 0.6
            return (max(r, Rtop), z)
        return (Rbase * (1 - 0.2 * t), z)

    o = _landform(44, 36, rfn, seed, [(1.0, 1.0), (2.2, 0.45), (4.4, 0.22), (9.0, 0.1)],
                  strata_h=3.2, overhang=0.9, warp=0.55, name_key=name)
    # strong vertical fluting already added in _landform via fl term; add erosion gullies on top half
    _paint_badlands(o, seed, H)
    _scree_skirt(seed, Rbase * 0.96, ('wd_bl_talus', 'wd_bl_sand', 'wd_bl_orange'), n=18, spread=1.3, scale=(1.4, 1.0, 0.5))
    # sparse dry tufts on top
    rnd2 = random.Random(seed + 9)
    for i in range(6):
        a = rnd2.uniform(0, 2 * math.pi); d = Rtop * math.sqrt(rnd2.random()) * 0.8
        for b in range(4):
            aa = rnd2.uniform(0, 6.28)
            tube(nm('dt'), [(math.cos(a) * d, math.sin(a) * d, H * 0.97),
                            (math.cos(a) * d + math.cos(aa) * 0.4, math.sin(a) * d + math.sin(aa) * 0.4, H * 0.97 + 1.2)],
                 0.08, 'wd_grass_dry', res=4, taper=[1, 0.1], ures=2)
    return finalize(name, smooth_angle=24)


def badlands_mesa_01():
    """Wide flat-topped mesa, broad talus slopes, layered red-orange-sand-cream bands."""
    return _mesa(21, 52.0, 44.0, 20.0, 'badlands_mesa_01', 'mesa', fluting=1.3)

def badlands_mesa_02():
    """Narrow butte tower: tall and slim with strong vertical fluting and a small flat cap."""
    return _mesa(22, 78.0, 24.0, 10.0, 'badlands_mesa_02', 'butte', fluting=1.6)


def badlands_mesa_03():
    """Twin-butte pair: two towers of different heights sharing a talus base."""
    reset()
    seed = 23
    rnd = random.Random(seed)
    H = 70.0

    def rfn(t):
        z = H * t
        r = 34.0 * (1 - 0.45 * t) if t < 0.8 else 34.0 * 0.6
        return (max(r, 12.0), z)
    o = _landform(46, 34, rfn, seed, [(1.0, 1.0), (2.2, 0.45), (4.4, 0.22)], strata_h=3.2, overhang=0.9, warp=0.5, name_key='badlands_mesa_03')
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts:
        if v.co.z > H * 0.4:
            v.co.z *= 1.0 - 0.5 * math.exp(-(v.co.x / 8.0) ** 2) * ((v.co.z - H * 0.4) / (H * 0.6))
            if v.co.x > 0:
                v.co.z *= 0.82
    bm.to_mesh(me); bm.free(); me.update()
    _paint_badlands(o, seed, H)
    _scree_skirt(seed, 34.0, ('wd_bl_talus', 'wd_bl_sand', 'wd_bl_orange'), n=18, spread=1.3, scale=(1.4, 1.0, 0.5))
    return finalize('badlands_mesa_03', smooth_angle=24)


def badlands_mesa_04():
    """Mesa with a notch and a small natural arch cut through one shoulder."""
    reset()
    seed = 24
    rnd = random.Random(seed)
    H = 56.0

    def rfn(t):
        z = H * t
        r = 40.0 * (1 - 0.2 * t) if t < 0.78 else 40.0 * 0.82
        return (max(r, 18.0), z)
    o = _landform(44, 34, rfn, seed, [(1.0, 1.0), (2.2, 0.45), (4.4, 0.22), (9.0, 0.1)],
                  strata_h=3.2, overhang=0.9, warp=0.55, name_key='badlands_mesa_04')
    # cut a notch on the +x shoulder by lowering a column of verts
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts:
        if v.co.x > 18 and v.co.z > H * 0.55 and abs(v.co.y) < 16:
            v.co.z = H * 0.55 + (v.co.z - H * 0.55) * 0.25
    bm.to_mesh(me); bm.free(); me.update()
    _paint_badlands(o, seed, H)
    # a small arch leg + span on the -Y front
    legr = lambda t: (6.0 * (1 - 0.3 * t), 22.0 * t)
    leg = _landform(26, 16, legr, seed + 3, [(1.0, 1.0), (2.5, 0.45), (5.0, 0.2)], strata_h=3.0, overhang=0.8, warp=0.5, name_key='badlands_mesa_04b')
    leg.location = (34.0, -3.0, 0)
    _paint_badlands(leg, seed + 3, 22.0)
    tube(nm('arch'), [(28.0, -3.0, 22.0), (31.0, -3.5, 26.0), (34.0, -3.0, 21.0)], 3.0, 'wd_bl_orange', res=6, ures=4, taper=[1.1, 1.0, 1.0])
    _scree_skirt(seed, 40.0, ('wd_bl_talus', 'wd_bl_sand', 'wd_bl_orange'), n=18, spread=1.25, scale=(1.4, 1.0, 0.5))
    return finalize('badlands_mesa_04', smooth_angle=24)


# ------------------------------------------------------------------ batches
BATCH_R01 = [
    ('R01_01_islet_01', islet_01, (0.6, -1.2, 0.4)),
    ('R01_02_islet_02', islet_02, (0.6, -1.2, 0.5)),
    ('R01_03_islet_03', islet_03, (0.6, -1.2, 0.4)),
    ('R01_04_islet_04', islet_04, (0.6, -1.2, 0.4)),
]
BATCH_R02 = [
    ('R02_01_snow_peak_01', snow_peak_01, (0.5, -1.2, 0.3)),
    ('R02_02_snow_peak_02', snow_peak_02, (0.5, -1.2, 0.3)),
    ('R02_03_snow_peak_03', snow_peak_03, (0.7, -1.0, 0.3)),
    ('R02_04_snow_peak_04', snow_peak_04, (0.5, -1.2, 0.3)),
]
BATCH_R03 = [
    ('R03_01_badlands_mesa_01', badlands_mesa_01, (0.6, -1.2, 0.35)),
    ('R03_02_badlands_mesa_02', badlands_mesa_02, (0.5, -1.2, 0.3)),
    ('R03_03_badlands_mesa_03', badlands_mesa_03, (0.6, -1.2, 0.35)),
    ('R03_04_badlands_mesa_04', badlands_mesa_04, (0.6, -1.2, 0.35)),
]

BATCHES = {'r01': ('v4_terrain', BATCH_R01), 'r02': ('v4_terrain', BATCH_R02), 'r03': ('v4_terrain', BATCH_R03)}
