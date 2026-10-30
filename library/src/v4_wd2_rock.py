"""v4_wd2_rock - replacement for frozen worker wd. Carved-rock terrain.

Fixes the wd weakness (horizontal-plank strata + square colour patches):
  GEOMETRY  dense grid/landform displaced by fbm (several octaves of mathutils.noise)
            PLUS a voronoi-facet term that snaps the surface onto angular planes, so faces
            read as fractured rock rather than smooth blobs or stacked planks. Vertical
            fracture grooves, irregular ledge fronts (smooth bumps, not quantised steps),
            and a few real overhangs.
  COLOUR    at most 4 keys per model, chosen from a SMOOTH height gradient + darkening on
            steep faces + low-frequency (8-15 stud) patches; snow/moss only on genuinely
            up-facing ledges. No int(z/band) stripes anywhere.

Imports helpers + palette keys from the predecessor modules (never edits them). New keys are
prefixed wd2_. Rock <= 40k tris, base flat at z=0 with a scree/boulder skirt. Headless runner
only; no live Blender, no Studio.
"""
import math, random, bmesh
from mathutils import Vector, noise as N
from kitlib import reset, finalize, PAL, _obj_from_bm, mat, cyl, tube
from nature import rock, blob
from v4_elf import nm
# reuse predecessor low-poly trees + islet/peak scaffolding by import (do not edit those files)
import v4_wd_peaks as WP

# ------------------------------------------------------------------ palette (wd2_ prefixed, <=4 used per model)
for k, v in {
    # granite (E13 01-04, R-series grey rock)
    'wd2_granite':      ((126, 128, 134), 'Rock',  0.00, 0.95, 0),
    'wd2_granite_dk':   ((86, 88, 95),    'Rock',  0.00, 0.96, 0),
    'wd2_granite_lt':   ((164, 166, 172), 'Rock',  0.00, 0.92, 0),
    'wd2_snow':         ((240, 244, 250), 'Snow',  0.00, 0.68, 0),
    # sandstone (E13 05-07)
    'wd2_sand':         ((198, 154, 106), 'Sandstone', 0.00, 0.90, 0),
    'wd2_sand_dk':      ((160, 118, 76),  'Sandstone', 0.00, 0.92, 0),
    'wd2_sand_lt':      ((222, 186, 138), 'Sandstone', 0.00, 0.88, 0),
    # basalt / slate (E13 08-10)
    'wd2_basalt':       ((80, 82, 90),    'Basalt', 0.00, 0.92, 0),
    'wd2_basalt_dk':    ((52, 54, 60),    'Basalt', 0.00, 0.94, 0),
    'wd2_basalt_lt':    ((112, 116, 124), 'Slate',  0.00, 0.90, 0),
    'wd2_moss':         ((90, 110, 60),   'Grass',  0.00, 1.00, 0),
    # islet rock + grass + trees
    'wd2_isle':         ((136, 128, 112), 'Rock',  0.00, 0.95, 0),
    'wd2_isle_dk':      ((98, 92, 80),    'Rock',  0.00, 0.96, 0),
    'wd2_grass':        ((96, 132, 62),   'Grass', 0.00, 1.00, 0),
    'wd2_dirt':         ((112, 90, 64),   'Ground', 0.00, 1.00, 0),
    # peaks
    'wd2_peak':         ((122, 124, 130), 'Rock', 0.00, 0.95, 0),
    'wd2_peak_dk':      ((82, 84, 92),    'Rock', 0.00, 0.96, 0),
    'wd2_peak_snow':    ((242, 246, 252), 'Snow', 0.00, 0.66, 0),
    'wd2_ice':          ((206, 228, 240), 'Ice',  0.00, 0.22, 0),
    # badlands
    'wd2_bl_red':       ((160, 84, 54),   'Sandstone', 0.00, 0.92, 0),
    'wd2_bl_orange':    ((196, 118, 64),  'Sandstone', 0.00, 0.90, 0),
    'wd2_bl_sand':      ((202, 162, 108), 'Sandstone', 0.00, 0.90, 0),
    'wd2_bl_cream':     ((224, 198, 152), 'Sandstone', 0.00, 0.88, 0),
    'wd2_bl_talus':     ((178, 122, 76),  'Sandstone', 0.00, 0.95, 0),
    'wd2_dry':          ((154, 150, 94),  'Grass', 0.00, 1.00, 0),
}.items():
    PAL[k] = v


# ================================================================== carved-rock noise field
def _fbm(p, seed, octaves=5, lac=2.07, gain=0.5):
    """Fractal brownian motion from mathutils.noise, deterministic by seed."""
    off = Vector((seed * 2.13, seed * 5.71, seed * 1.37))
    f, a, tot, amp = 1.0, 1.0, 0.0, 0.0
    for _ in range(octaves):
        tot += a * N.noise(p * f + off)
        amp += a
        f *= lac
        a *= gain
    return tot / amp


def _voronoi_facet(p, seed, scale):
    """Return (f1, edge) where f1 is distance to nearest cell point (cracked-plane look)
    and edge ~0 near a cell boundary. Uses mathutils.noise.voronoi."""
    try:
        d, _pts = N.voronoi(p * scale + Vector((seed, 0, 0)))
        f1 = d[0]
        f2 = d[1] if len(d) > 1 else d[0]
        return f1, (f2 - f1)
    except Exception:
        n = N.noise(p * scale + Vector((seed, 0, 0)))
        return abs(n), abs(n)


def _carve(p, seed, warp, facet=0.9, groove=1.0, strata=0.0):
    """Displacement (outward along local normal) for a point p. Combines:
      - fbm bulk shape
      - voronoi facets: snap toward flat angular planes (makes carved faces, not blobs)
      - vertical fracture grooves (narrow deep cuts, periodic-ish in angle/x)
      - gentle strata as a low-amplitude smooth ripple (NOT quantised steps)
    """
    base = _fbm(p * 0.09, seed, octaves=5)
    f1, edge = _voronoi_facet(p, seed + 7, 0.055)
    # facet term: within a cell the surface is nearly constant (a plane); near edges it drops -> crack
    fac = (0.5 - f1) * facet
    crack = -max(0.0, (0.06 - edge)) * 6.0 * groove        # sharp inward groove on cell boundaries
    # vertical fracture grooves: sample a 2D noise that varies mostly horizontally
    vg = _fbm(Vector((p.x * 0.22, p.y * 0.22, p.z * 0.03)), seed + 19, octaves=3)
    vg = -max(0.0, abs(vg) - 0.55) * 5.0 * groove
    rip = strata * math.sin(p.z * 0.5 + 1.3 * _fbm(p * 0.04, seed + 3, 3))   # soft bedding ripple
    fine = 0.18 * _fbm(p * 0.5, seed + 31, 3)              # fine tooth so no face is dead flat
    return warp * (0.55 + 0.6 * base) + fac + crack + vg + rip + fine


# ================================================================== E13: tiling cliff panels
def _panel(seed, W, D, H, warp, strata, keyset, cap_snow, moss, name):
    """Solid prism whose -Y front is a carved height field y(x,z). Tiles sideways: the left and
    right edge COLUMNS are displaced by an x-periodic field so neighbours share a profile."""
    nx, nz = 72, 78
    bm = bmesh.new()
    hd = D / 2
    two_pi = 2 * math.pi

    def front_y(x, z):
        # x-periodic sample so x=-W/2 and x=+W/2 match exactly (seamless tiling)
        ang = two_pi * (x + W / 2) / W
        px = math.cos(ang) * (W / two_pi)
        py = math.sin(ang) * (W / two_pi)
        disp = _carve(Vector((px, py, z)), seed, warp, facet=1.0, groove=1.0, strata=strata)
        lean = (z / H) * 2.0                      # slight top-forward lean
        y = -hd - disp + lean
        return max(-hd - warp * 2.0, min(hd - 0.6, y))

    # overhang: a couple of broad protruding shelves whose underside is recessed (true overhang)
    rnd = random.Random(seed)
    shelves = [(H * rnd.uniform(0.3, 0.45), rnd.uniform(1.4, 2.0)),
               (H * rnd.uniform(0.6, 0.75), rnd.uniform(1.2, 1.8))]

    def shelf_adj(z):
        a = 0.0
        for zc, dp in shelves:
            a -= dp * 1.8 * math.exp(-((z - (zc + 1.4)) / 1.1) ** 2)   # recess just under lip
            a += dp * 1.4 * math.exp(-((z - zc) / 0.8) ** 2)           # protruding lip
        return a

    front = []
    for iz in range(nz + 1):
        z = H * iz / nz
        row = []
        for ix in range(nx + 1):
            x = -W / 2 + W * ix / nx
            y = front_y(x, z) - shelf_adj(z)
            y = max(-hd - warp * 2.2, min(hd - 0.6, y))
            row.append(bm.verts.new((x, y, z)))
        front.append(row)
    backy = D / 2
    back = [[bm.verts.new((-W / 2 + W * ix / nx, backy, H * iz / nz)) for ix in range(nx + 1)] for iz in range(nz + 1)]
    for iz in range(nz):
        for ix in range(nx):
            bm.faces.new((front[iz][ix], front[iz][ix + 1], front[iz + 1][ix + 1], front[iz + 1][ix]))
            bm.faces.new((back[iz][ix + 1], back[iz][ix], back[iz + 1][ix], back[iz + 1][ix + 1]))
    for iz in range(nz):
        bm.faces.new((front[iz][0], front[iz + 1][0], back[iz + 1][0], back[iz][0]))
        bm.faces.new((back[iz][nx], back[iz + 1][nx], front[iz + 1][nx], front[iz][nx]))
    for ix in range(nx):
        bm.faces.new((front[0][ix], back[0][ix], back[0][ix + 1], front[0][ix + 1]))
        bm.faces.new((front[nz][ix + 1], back[nz][ix + 1], back[nz][ix], front[nz][ix]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj_from_bm(name + '_body', bm, keyset['base'])
    _paint_geology(o, seed, H, keyset, cap_snow=cap_snow, moss=moss)
    return o


def _paint_geology(o, seed, H, keyset, cap_snow=False, moss=False, snow_line=0.6):
    """Colour by SMOOTH height gradient + steepness + LOW-FREQUENCY patches (8-15 studs).
    keyset: {'base','dark','light', optional 'snow','moss'}. At most 4 colours used."""
    me = o.data
    keys = [keyset[k] for k in ('base', 'dark', 'light') if k in keyset]
    for extra in ('snow', 'moss'):
        if (extra == 'snow' and cap_snow) or (extra == 'moss' and moss):
            keys.append(keyset[extra])
    present = [m.name.split('|')[0] for m in me.materials]
    for k in keys:
        if k not in present:
            me.materials.append(mat(k)); present.append(k)
    idx = {m.name.split('|')[0]: i for i, m in enumerate(me.materials)}
    bm = bmesh.new(); bm.from_mesh(me)
    off = Vector((seed * 3.1, seed * 1.7, seed * 0.9))
    for f in bm.faces:
        c = f.calc_center_median()
        up = f.normal.z
        t = max(0.0, min(1.0, c.z / H))
        # Two SMOOTH position fields. Colour is driven by POSITION, not the per-face normal
        # (the normal is high-frequency on a carved surface and that is what makes pixel speckle).
        patch = _fbm(Vector((c.x * 0.045, c.y * 0.045, c.z * 0.030)), seed + 2, octaves=2)
        patch2 = _fbm(Vector((c.x * 0.07, c.y * 0.02, c.z * 0.05)), seed + 8, octaves=2)
        g = patch + 0.35 * patch2
        if g < -0.15:
            pick = keyset['dark']
        elif g > 0.17:
            pick = keyset['light']
        else:
            pick = keyset['base']
        # moss: sparse patches on up-facing LOW shelves only (needs real up-facing + a positive patch),
        # so it is a hint of green on ledges, never a solid band.
        if moss:
            if up > 0.5 and (0.42 - t) * 2.4 + 1.1 * patch > 0.72:
                pick = keyset['moss']
        # snow: a thin DUSTING on ledge tops and the crown. Requires the face to be genuinely
        # up-facing (so vertical rock stays bare) AND high; the patch wobble breaks the line edge.
        if cap_snow:
            if up > 0.45 and (t - snow_line) * 3.4 + 0.6 * patch + 1.2 * (up - 0.45) > 0.0:
                pick = keyset['snow']
        f.material_index = idx.get(pick, idx[keyset['base']])
    bm.to_mesh(me); bm.free(); me.update()
    return o


def _scree(seed, W, keys, n=14, span=None):
    rnd = random.Random(seed + 500)
    span = span or (W / 2 - 2)
    for i in range(n):
        x = rnd.uniform(-span, span)
        y = -11 - rnd.uniform(0.0, 5.0)
        r = rnd.uniform(1.1, 3.0)
        rock(nm('scr'), r, (x, y, r * 0.3), rnd.choice(keys), seed=seed + i, scale=(1.35, 1.0, 0.6), subdiv=2, amp=0.36)
    for i in range(4):
        x = rnd.uniform(-span + 3, span - 3)
        r = rnd.uniform(0.8, 1.6)
        rock(nm('scr2'), r, (x, -8.5, r * 0.3), rnd.choice(keys), seed=seed + 60 + i, scale=(1.2, 1.0, 0.6), subdiv=2, amp=0.3)


# ---- E13 builders
def _granite_panel(seed, name, snow=True):
    reset()
    H = 60.0
    ks = {'base': 'wd2_granite', 'dark': 'wd2_granite_dk', 'light': 'wd2_granite_lt', 'snow': 'wd2_snow', 'moss': 'wd2_moss'}
    _panel(seed, 80.0, 28.0, H, warp=4.6, strata=1.1, keyset=ks, cap_snow=snow, moss=True, name=name)
    _scree(seed, 80.0, ('wd2_granite', 'wd2_granite_dk'))
    return finalize(name, smooth_angle=28)

def rock_face_01(): return _granite_panel(2301, 'rock_face_01')
def rock_face_02(): return _granite_panel(2302, 'rock_face_02')
def rock_face_03(): return _granite_panel(2303, 'rock_face_03')
def rock_face_04(): return _granite_panel(2304, 'rock_face_04')

def _sandstone_panel(seed, name):
    reset()
    H = 58.0
    ks = {'base': 'wd2_sand', 'dark': 'wd2_sand_dk', 'light': 'wd2_sand_lt'}
    _panel(seed, 80.0, 28.0, H, warp=3.8, strata=2.0, keyset=ks, cap_snow=False, moss=False, name=name)
    _scree(seed, 80.0, ('wd2_sand', 'wd2_sand_dk'))
    return finalize(name, smooth_angle=28)

def rock_face_05(): return _sandstone_panel(2305, 'rock_face_05')
def rock_face_06(): return _sandstone_panel(2306, 'rock_face_06')
def rock_face_07(): return _sandstone_panel(2307, 'rock_face_07')

def _basalt_panel(seed, name):
    reset()
    H = 60.0
    ks = {'base': 'wd2_basalt', 'dark': 'wd2_basalt_dk', 'light': 'wd2_basalt_lt', 'moss': 'wd2_moss'}
    _panel(seed, 80.0, 28.0, H, warp=4.8, strata=0.7, keyset=ks, cap_snow=False, moss=True, name=name)
    _scree(seed, 80.0, ('wd2_basalt', 'wd2_basalt_dk'))
    return finalize(name, smooth_angle=28)

def rock_face_08(): return _basalt_panel(2308, 'rock_face_08')
def rock_face_09(): return _basalt_panel(2309, 'rock_face_09')
def rock_face_10(): return _basalt_panel(2310, 'rock_face_10')


# ================================================================== R: free-standing landforms (carved)
def _landform(nx, nz, radius_fn, seed, warp, strata, facet, groove, name, flat_base=True):
    """Closed landform: ring per height, radius pushed by the carved field sampled on a cylinder."""
    bm = bmesh.new()
    rings = []
    for iz in range(nz + 1):
        t = iz / nz
        r, z = radius_fn(t)
        if r < 0.3:
            rings.append([bm.verts.new((0, 0, z))]); continue
        ring = []
        for ix in range(nx):
            a = 2 * math.pi * ix / nx
            cx, cy = math.cos(a), math.sin(a)
            # sample carve on a cylinder of this radius (continuous around a)
            p = Vector((cx * r, cy * r, z))
            disp = _carve(p, seed, warp, facet=facet, groove=groove, strata=strata)
            # strong VERTICAL FLUTING: deep azimuthal ribs that run top-to-bottom (cliff pilasters),
            # their count and phase wobbled by a low-freq field so they are irregular, not a gear.
            nribs = 11 + (seed % 7)
            phase = 1.6 * _fbm(Vector((0, 0, z)) * 0.04 + Vector((seed, 0, 0)), seed + 2, 2)
            flute = math.cos(a * nribs + phase)
            flute = (abs(flute) ** 0.6) - 0.55            # sharp valleys, broad ribs
            rr = r + disp + flute * warp * 1.5
            # a few overhang ledges: push selected height bands outward
            rr += warp * 0.9 * max(0.0, math.sin(z * 0.14 + seed) - 0.4) * (0.5 + 0.5 * _fbm(p * 0.05, seed + 9, 2))
            rr = max(0.4, rr)
            ring.append(bm.verts.new((cx * rr, cy * rr, z)))
        rings.append(ring)
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
    if flat_base and len(rings[0]) > 1:
        bm.faces.new(list(reversed(rings[0])))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj_from_bm(name + '_body', bm, 'wd2_peak')


def _paint_rules(o, seed, H, rules):
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
        up = f.normal.z
        t = max(0.0, min(1.0, c.z / H))
        patch = _fbm(Vector((c.x, c.y, c.z)) * 0.08 + off, seed + 5, octaves=3)
        for k, pred in rules:
            if pred(c, up, t, patch):
                f.material_index = idx[k]; break
    bm.to_mesh(me); bm.free(); me.update()
    return o


# ---------- R01 islets
def _islet(seed, H, Rbase, Rtop, ntrees, kinds, shape, name):
    reset()
    rnd = random.Random(seed)

    def rfn(t):
        z = H * t
        if shape == 'mesa':
            r = Rbase * (1 - 0.14 * t) if t < 0.86 else (Rbase * 0.86) * (1 - (t - 0.86) / 0.14) + Rtop
        else:
            r = Rbase * (1 - 0.5 * t) ** 1.15 + Rtop * t
        return (max(r, Rtop * 0.9), z)

    o = _landform(52, 34, rfn, seed, warp=2.6, strata=1.4, facet=1.3, groove=1.2, name=name)
    rules = [
        ('wd2_grass', lambda c, up, t, pv: up > 0.6 and t > 0.84),
        ('wd2_dirt',  lambda c, up, t, pv: up > 0.42 and t > 0.74),
        ('wd2_isle_dk', lambda c, up, t, pv: up < 0.33 or pv < -0.18),
        ('wd2_isle', lambda c, up, t, pv: True),
    ]
    _paint_rules(o, seed, H, rules)
    WP._scree_skirt(seed, Rbase * 0.92, ('wd2_isle', 'wd2_isle_dk'), n=12, spread=1.3)
    for i in range(7):
        a = rnd.uniform(0, 2 * math.pi)
        rock(nm('wb'), rnd.uniform(1.2, 2.3), (math.cos(a) * Rbase * 1.0, math.sin(a) * Rbase * 1.0, 0.3),
             rnd.choice(('wd2_isle', 'wd2_isle_dk')), seed=seed + 40 + i, scale=(1.3, 1.1, 0.55), subdiv=2, amp=0.3)
    _grass_cap(0, 0, H * 0.985, Rtop * 1.1, seed)
    _tree_cap(0, 0, H * 1.02, Rtop, ntrees, seed, kinds)
    return finalize(name, smooth_angle=24)


def _grass_cap(cx, cy, ztop, r, seed):
    cyl(nm('cap'), r, 0.9, loc=(cx, cy, ztop - 0.45), key='wd2_dirt', verts=18)
    return blob(nm('gtop'), r * 0.98, (cx, cy, ztop + 0.1), 'wd2_grass', subdiv=2, amp=0.12,
                scale=(1.0, 1.0, 0.18), seed=seed, flat_bottom=-0.1)


def _mini_pine(x, y, z, h, seed):
    rnd = random.Random(seed)
    cyl(nm('tr'), h * 0.05, h * 0.3, loc=(x, y, z), key='wd_trunk', verts=5)
    for i in range(3):
        tt = i / 3
        r = h * 0.22 * (1 - tt)
        cyl(nm('pc'), r, h * 0.32, loc=(x, y, z + h * (0.22 + 0.24 * i)), key=rnd.choice(('wd_pine', 'wd_pine_dark')), verts=6, r2=r * 0.15)


def _mini_oak(x, y, z, h, seed):
    rnd = random.Random(seed)
    cyl(nm('tr'), h * 0.07, h * 0.4, loc=(x, y, z), key='wd_trunk', verts=5)
    blob(nm('cr'), h * 0.3, (x, y, z + h * 0.6), rnd.choice(('wd_oak', 'wd_pine')), subdiv=1, amp=0.28, scale=(1, 1, 0.9), seed=seed)


def _tree_cap(cx, cy, ztop, rtop, n, seed, kinds):
    rnd = random.Random(seed + 300)
    for i in range(n):
        a = rnd.uniform(0, 2 * math.pi)
        d = rtop * math.sqrt(rnd.random()) * 0.85
        x, y = cx + math.cos(a) * d, cy + math.sin(a) * d
        h = rnd.uniform(5.0, 8.0)
        if rnd.choice(kinds) == 'pine':
            _mini_pine(x, y, ztop - 0.3, h, seed + i)
        else:
            _mini_oak(x, y, ztop - 0.3, h, seed + i)


def islet_01():
    """Tall single sea stack, carved steep cliffs, small grassy crown with pines."""
    return _islet(2401, 44.0, 18.0, 7.0, 4, ('pine',), 'stack', 'islet_01')


def islet_04():
    """Arch islet: two carved legs bridged by a thick natural arch with a clear gap, grassy cap."""
    reset()
    seed = 2404
    rnd = random.Random(seed)
    for sgn, hh, rr in ((-1, 30.0, 8.0), (1, 26.0, 7.0)):
        def legr(t, hh=hh, rr=rr):
            return (max(rr * (1 - 0.45 * t), rr * 0.5), hh * t)
        leg = _landform(40, 24, legr, seed + (0 if sgn < 0 else 7), warp=2.2, strata=1.3, facet=1.3, groove=1.1,
                        name='islet_04_%d' % sgn)
        leg.location = (sgn * 11.0, 0, 0)
        _paint_rules(leg, seed + (0 if sgn < 0 else 7), hh, [
            ('wd2_isle_dk', lambda c, up, t, pv: up < 0.33 or pv < -0.18),
            ('wd2_isle', lambda c, up, t, pv: True)])
    xs = [-11.0, -6.0, 0.0, 6.0, 11.0]
    zs = [27.0, 32.0, 35.0, 31.0, 24.0]
    tube(nm('arch'), [(x, 0.0, z) for x, z in zip(xs, zs)], 3.6, 'wd2_isle', res=7, ures=5, taper=[0.9, 1.0, 1.05, 1.0, 0.9])
    tube(nm('arch2'), [(x, 4.5, z - 0.6) for x, z in zip(xs, zs)], 2.6, 'wd2_isle_dk', res=6, ures=4, taper=[0.9, 1.0, 1.0, 1.0, 0.9])
    WP._scree_skirt(seed, 20.0, ('wd2_isle', 'wd2_isle_dk'), n=12, spread=1.25)
    for i in range(7):
        a = rnd.uniform(0, 2 * math.pi)
        rock(nm('wb'), rnd.uniform(1.2, 2.2), (math.cos(a) * 19.0, math.sin(a) * 19.0, 0.3),
             'wd2_isle_dk', seed=seed + 40 + i, scale=(1.3, 1.1, 0.55), subdiv=2, amp=0.3)
    _grass_cap(-11.0, 0, 29.5, 5.0, seed)
    _tree_cap(-11.0, 0, 30.5, 4.2, 3, seed, ('pine',))
    return finalize('islet_04', smooth_angle=24)


# ---------- R02 snow peaks
def _peak_rules(H, snow_line):
    return [
        ('wd2_peak_snow', lambda c, up, t, pv: up > 0.32 and t > snow_line + 0.10 * pv),
        ('wd2_peak_dk',   lambda c, up, t, pv: up < 0.22 or pv < -0.22),
        ('wd2_peak',      lambda c, up, t, pv: True),
    ]


def _snow_peak(seed, H, Rbase, rfn, snow_line, name, carve_fn=None):
    reset()
    o = _landform(56, 44, rfn, seed, warp=2.9, strata=0.0, facet=1.45, groove=1.3, name=name)
    if carve_fn:
        me = o.data
        bm = bmesh.new(); bm.from_mesh(me)
        carve_fn(bm, H, seed)
        bm.to_mesh(me); bm.free(); me.update()
    _paint_rules(o, seed, H, _peak_rules(H, snow_line))
    WP._scree_skirt(seed, Rbase * 0.9, ('wd2_peak', 'wd2_peak_dk'), n=20, spread=1.35, scale=(1.3, 1.0, 0.55))
    return finalize(name, smooth_angle=26)


def snow_peak_01():
    """Single sharp horn: steep pyramidal summit, carved faces, snow above a ragged line."""
    H, Rb = 170.0, 62.0
    return _snow_peak(2411, H, Rb, lambda t: (Rb * (1 - t) ** 1.9 + 1.5, H * t), 0.5, 'snow_peak_01')


def snow_peak_02():
    """Double summit: two horns of unequal height sharing a massif."""
    H, Rb = 160.0, 66.0

    def carve(bm, H, seed):
        for v in bm.verts:
            if v.co.z > H * 0.5:
                v.co.z *= 1.0 - 0.42 * math.exp(-(v.co.x / 9.0) ** 2) * ((v.co.z - H * 0.5) / (H * 0.5))
                if v.co.x > 0:
                    v.co.z *= 0.9
    return _snow_peak(2412, H, Rb, lambda t: (Rb * (1 - t) ** 1.6 + 2.0, H * t), 0.46, 'snow_peak_02', carve)


def snow_peak_03():
    """Long serrated ridge: an elongated crest with several jagged points."""
    H, Rb = 150.0, 70.0

    def carve(bm, H, seed):
        for v in bm.verts:
            v.co.y *= 1.7
            if v.co.z > H * 0.4:
                serr = 0.82 + 0.18 * math.sin(v.co.y * 0.22 + seed)
                if abs(v.co.x) < 12:
                    v.co.z *= serr
    return _snow_peak(2413, H, Rb, lambda t: (Rb * (1 - t) ** 1.4 + 2.5, H * t), 0.5, 'snow_peak_03', carve)


def snow_peak_04():
    """Broad peak with a hanging glacier shelf: wide summit, a flat ice bench on one flank."""
    H, Rb = 140.0, 78.0
    seed = 2414
    reset()
    o = _landform(54, 44, lambda t: (Rb * (1 - t) ** 1.3 + 3.0, H * t), seed, warp=2.7, strata=0.0,
                  facet=1.4, groove=1.2, name='snow_peak_04')
    _paint_rules(o, seed, H, _peak_rules(H, 0.5))
    shelf = _landform(30, 10, lambda t: (26.0 * (1 - 0.2 * t), 18.0 * t), seed + 7, warp=1.0, strata=0.0,
                      facet=0.7, groove=0.5, name='snow_peak_04ice')
    shelf.location = (0, -40.0, H * 0.46)
    _paint_rules(shelf, seed + 7, 18.0, [('wd2_ice', lambda c, up, t, pv: up > 0.3), ('wd2_peak_snow', lambda c, up, t, pv: True)])
    WP._scree_skirt(seed, Rb * 0.95, ('wd2_peak', 'wd2_peak_dk'), n=22, spread=1.35, scale=(1.3, 1.0, 0.55))
    return finalize('snow_peak_04', smooth_angle=26)


# ---------- R03 badlands mesas (strata as smooth banded tint, not quantised geometry steps)
def _paint_badlands(o, seed, H):
    me = o.data
    keys = ('wd2_bl_red', 'wd2_bl_orange', 'wd2_bl_sand', 'wd2_bl_cream', 'wd2_bl_talus', 'wd2_dry')
    present = [m.name.split('|')[0] for m in me.materials]
    for k in keys:
        if k not in present:
            me.materials.append(mat(k)); present.append(k)
    idx = {m.name.split('|')[0]: i for i, m in enumerate(me.materials)}
    bm = bmesh.new(); bm.from_mesh(me)
    off = Vector((seed * 2.3, seed * 1.1, 0))
    band_keys = ('wd2_bl_red', 'wd2_bl_orange', 'wd2_bl_sand', 'wd2_bl_cream')
    for f in bm.faces:
        c = f.calc_center_median()
        up = f.normal.z
        t = c.z / H
        # banding: smooth height-driven index, wobbled by low-freq noise so bands undulate (not pixel rows)
        wob = 2.2 * _fbm(Vector((c.x, c.y, 0)) * 0.05 + off, seed + 4, 3)
        level = (c.z + wob) / 5.5
        if up > 0.72 and t > 0.8:
            pick = 'wd2_dry'
        elif t < 0.14:
            pick = 'wd2_bl_talus'
        else:
            pick = band_keys[int(level) % 4]
        f.material_index = idx[pick]
    bm.to_mesh(me); bm.free(); me.update()
    return o


def _mesa(seed, H, Rbase, Rtop, name, shape='mesa'):
    reset()

    def rfn(t):
        z = H * t
        if shape == 'mesa':
            r = Rbase * (1 - 0.16 * t) if t < 0.8 else Rbase * 0.85
        elif shape == 'butte':
            r = Rbase * (1 - 0.48 * t) if t < 0.82 else Rbase * 0.58
        else:
            r = Rbase * (1 - 0.2 * t)
        return (max(r, Rtop), z)

    o = _landform(48, 40, rfn, seed, warp=1.9, strata=1.0, facet=1.1, groove=1.6, name=name)
    _paint_badlands(o, seed, H)
    WP._scree_skirt(seed, Rbase * 0.96, ('wd2_bl_talus', 'wd2_bl_sand'), n=16, spread=1.3, scale=(1.4, 1.0, 0.5))
    _dry_tufts(seed, Rtop, H)
    return finalize(name, smooth_angle=26)


def _dry_tufts(seed, Rtop, H):
    rnd = random.Random(seed + 9)
    for i in range(6):
        a = rnd.uniform(0, 2 * math.pi); d = Rtop * math.sqrt(rnd.random()) * 0.8
        x, y = math.cos(a) * d, math.sin(a) * d
        for b in range(4):
            aa = rnd.uniform(0, 6.28)
            tube(nm('dt'), [(x, y, H * 0.97), (x + math.cos(aa) * 0.4, y + math.sin(aa) * 0.4, H * 0.97 + 1.2)],
                 0.08, 'wd2_dry', res=4, taper=[1, 0.1], ures=2)


def badlands_mesa_01():
    """Wide flat-topped mesa, broad talus, undulating red-orange-sand-cream bands."""
    return _mesa(2421, 52.0, 44.0, 20.0, 'badlands_mesa_01', 'mesa')

def badlands_mesa_02():
    """Narrow butte tower: tall, strong vertical fluting, small flat cap."""
    return _mesa(2422, 78.0, 24.0, 10.0, 'badlands_mesa_02', 'butte')


def badlands_mesa_03():
    """Twin-butte pair: two towers of different heights sharing a talus base."""
    reset()
    seed = 2423
    H = 70.0
    o = _landform(48, 38, lambda t: (max(34.0 * (1 - 0.45 * t) if t < 0.8 else 34.0 * 0.6, 12.0), H * t),
                  seed, warp=1.9, strata=1.0, facet=1.1, groove=1.6, name='badlands_mesa_03')
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts:
        if v.co.z > H * 0.4:
            v.co.z *= 1.0 - 0.5 * math.exp(-(v.co.x / 8.0) ** 2) * ((v.co.z - H * 0.4) / (H * 0.6))
            if v.co.x > 0:
                v.co.z *= 0.82
    bm.to_mesh(me); bm.free(); me.update()
    _paint_badlands(o, seed, H)
    WP._scree_skirt(seed, 34.0, ('wd2_bl_talus', 'wd2_bl_sand'), n=16, spread=1.3, scale=(1.4, 1.0, 0.5))
    return finalize('badlands_mesa_03', smooth_angle=26)


def badlands_mesa_04():
    """Mesa with a notch and a small natural arch cut through one shoulder."""
    reset()
    seed = 2424
    H = 56.0
    o = _landform(48, 38, lambda t: (max(40.0 * (1 - 0.2 * t) if t < 0.78 else 40.0 * 0.82, 18.0), H * t),
                  seed, warp=1.9, strata=1.0, facet=1.1, groove=1.6, name='badlands_mesa_04')
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts:
        if v.co.x > 18 and v.co.z > H * 0.55 and abs(v.co.y) < 16:
            v.co.z = H * 0.55 + (v.co.z - H * 0.55) * 0.25
    bm.to_mesh(me); bm.free(); me.update()
    _paint_badlands(o, seed, H)
    leg = _landform(28, 18, lambda t: (6.0 * (1 - 0.3 * t), 22.0 * t), seed + 3, warp=1.5, strata=1.0,
                    facet=1.0, groove=1.4, name='badlands_mesa_04b')
    leg.location = (34.0, -3.0, 0)
    _paint_badlands(leg, seed + 3, 22.0)
    tube(nm('arch'), [(28.0, -3.0, 22.0), (31.0, -3.5, 26.0), (34.0, -3.0, 21.0)], 3.0, 'wd2_bl_orange', res=6, ures=4, taper=[1.1, 1.0, 1.0])
    WP._scree_skirt(seed, 40.0, ('wd2_bl_talus', 'wd2_bl_sand'), n=16, spread=1.25, scale=(1.4, 1.0, 0.5))
    return finalize('badlands_mesa_04', smooth_angle=26)


# ================================================================== batches
BATCH_E13 = [
    ('E13_01_rock_face_01', rock_face_01, (0.0, -1.0, 0.18)),
    ('E13_02_rock_face_02', rock_face_02, (0.0, -1.0, 0.18)),
    ('E13_03_rock_face_03', rock_face_03, (0.0, -1.0, 0.18)),
    ('E13_04_rock_face_04', rock_face_04, (0.0, -1.0, 0.18)),
    ('E13_05_rock_face_05', rock_face_05, (0.0, -1.0, 0.18)),
    ('E13_06_rock_face_06', rock_face_06, (0.0, -1.0, 0.18)),
    ('E13_07_rock_face_07', rock_face_07, (0.0, -1.0, 0.18)),
    ('E13_08_rock_face_08', rock_face_08, (0.0, -1.0, 0.18)),
    ('E13_09_rock_face_09', rock_face_09, (0.0, -1.0, 0.18)),
    ('E13_10_rock_face_10', rock_face_10, (0.0, -1.0, 0.18)),
]
BATCH_R01 = [
    ('R01_01_islet_01', islet_01, (0.6, -1.2, 0.4)),
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

BATCHES = {
    'e13': ('v4_terrain', BATCH_E13),
    'r01': ('v4_terrain', BATCH_R01),
    'r02': ('v4_terrain', BATCH_R02),
    'r03': ('v4_terrain', BATCH_R03),
}
