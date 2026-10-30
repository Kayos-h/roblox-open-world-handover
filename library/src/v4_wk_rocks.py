"""v4_wk_rocks - worker wk. Rock formations, coastal/sea cliffs, waterfall cliffs, canyon
walls and boulders (F07 x11, R04 x3, R05 x2, R06 x3, E15 x6) -> category v4_terrain.

Method follows worker wd (v4_wd_cliffs / v4_wd_peaks): free-standing landforms are a dense
noise-displaced revolved mesh (reuse wd._landform); tiling wall panels are a periodic-noise
height-field prism (reuse wd._front_panel) so left and right edge profiles match and panels
butt together seamlessly. Per-face materials from height / slope / noise. Flat base at z=0 with
a scree-and-boulder skirt. Rock must read as carved, layered, weathered - never smooth blobs or
stacked boxes. Reuse wd_ rock palette so everything sits together; new keys use the wk_ prefix.
Imports shared files only; edits none.
"""
import math, random, bmesh
from mathutils import Vector, noise as N
from kitlib import reset, finalize, PAL, _obj_from_bm, mat, cyl, tube, box, ball, lathe, poly_prism, top_paint
from nature import rock, blob
from v4_elf import nm
import v4util as U

# wd rock helpers + palette (import loads the wd_ keys into PAL)
from v4_wd_peaks import _landform, _paint, _scree_skirt, _mini_pine, _mini_oak, _grass_cap, _tree_cap
from v4_wd_cliffs import _front_panel, _paint_panel, _paint_sandstone, _scree, _tuft_on_ledges

PI = math.pi

# ------------------------------------------------------------------ palette (wk_ prefixed; reuse wd_ where possible)
for k, v in {
    'wk_guano':       ((214, 210, 196), 'Limestone', 0.00, 0.85, 0),   # white gull streaks on sea stacks
    'wk_kelp':        ((52, 60, 44),    'Grass',     0.00, 1.00, 0),    # dark wet foot / kelp
    'wk_wet_rock':    ((70, 74, 78),    'Rock',      0.00, 0.70, 0),    # wave-washed dark band
    'wk_chalk':       ((214, 212, 204), 'Limestone', 0.00, 0.85, 0),    # pale chalky sea cliff
    'wk_chalk_dk':    ((178, 176, 166), 'Limestone', 0.00, 0.88, 0),
    'wk_chalk_band':  ((150, 148, 138), 'Limestone', 0.00, 0.90, 0),
    'wk_cave_dark':   ((18, 16, 20),    'Slate',     0.00, 1.00, 0),    # cave/sea-cave interior black
    'wk_grass_cap':   ((92, 128, 60),   'Grass',     0.00, 1.00, 0),    # grass cap on coastal cliffs
    'wk_tree_pin':    ((48, 86, 56),    'LeafyGrass',0.00, 0.90, 0),
}.items():
    PAL[k] = v


# ================================================================== helpers
def _geo_paint(o, seed, H, keys, low=0.09, patch=0.09):
    """Geology colouring: assign at most 4 rock tones in LOW-FREQUENCY patches (~8-15 studs) so the
    face reads as bedded geology, not a per-face speckle or an even stripe. `patch` is the spatial
    frequency (smaller = bigger patches). keys = (dark, base, light[, extra]) tones."""
    me = o.data
    cols = list(keys)[:4]
    present = [m.name.split('|')[0] for m in me.materials]
    for k in cols:
        if k not in present:
            me.materials.append(mat(k)); present.append(k)
    idx = {m.name.split('|')[0]: i for i, m in enumerate(me.materials)}
    bm = bmesh.new(); bm.from_mesh(me)
    off = Vector((seed * 4.3, seed * 2.9, seed * 1.1))
    for f in bm.faces:
        c = f.calc_center_median()
        # two low-freq noise fields -> a few broad patches; a faint bedding bias by height
        n1 = N.noise(c * patch + off)
        n2 = N.noise(c * (patch * 0.55) + off * 1.7)
        bed = math.sin(c.z * 0.12 + n2 * 1.5)
        v = 0.6 * n1 + 0.4 * bed
        # base grey dominates; dark and light are minority accents (not half-and-half)
        if v < -0.42:
            pick = cols[0]                               # dark: patches
        elif v > 0.52 and len(cols) > 2:
            pick = cols[2]                               # light: small bright accents only
        elif v > 0.78 and len(cols) > 3:
            pick = cols[3]
        else:
            pick = cols[1]                               # base grey: most of the surface
        f.material_index = idx[pick]
    bm.to_mesh(me); bm.free(); me.update()
    return o


def _facet(bm, seed, amp=0.14, cell=0.5):
    """Push bmesh verts by cell-like + fbm noise so the surface breaks into angular plates with
    vertical fractures, instead of a smooth lump. Operates in place on a bmesh's verts."""
    off = Vector((seed * 3.1, seed * 1.7, seed * 0.9))
    for v in bm.verts:
        p = v.co
        # cell-ish: quantise a low-freq noise into steps -> flat plates with sharp edges
        base = N.noise(p * cell + off)
        plate = round(base * 3.0) / 3.0
        fbm = 0.5 * N.noise(p * cell * 2.3 + off) + 0.25 * N.noise(p * cell * 5.0 + off * 2)
        # vertical fracture grooves (sharp, periodic in angle around Z)
        ang = math.atan2(p.y, p.x)
        frac = max(0.0, math.sin(ang * (7 + seed % 4) + fbm * 2.0))
        d = amp * (0.6 * plate + 0.4 * fbm) - amp * 0.5 * (frac ** 3)
        r = math.hypot(p.x, p.y)
        if r > 1e-5:
            v.co.x += p.x / r * d * r
            v.co.y += p.y / r * d * r
        v.co.z += amp * 0.3 * fbm
    return bm


def _despeckle(o, light_key, base_key, keep=0.25, seed=0):
    """_paint_panel scatters the light tone as isolated bright flecks (reads as confetti/snow).
    Demote most light faces to base, keeping only ones that sit in a broad low-freq patch."""
    me = o.data
    names = [m.name.split('|')[0] for m in me.materials]
    if light_key not in names or base_key not in names:
        return o
    li = names.index(light_key); bi = names.index(base_key)
    bm = bmesh.new(); bm.from_mesh(me)
    off = Vector((seed * 2.7, seed * 1.3, 0))
    for f in bm.faces:
        if f.material_index == li:
            c = f.calc_center_median()
            if N.noise(c * 0.1 + off) < (1.0 - keep):   # keep only inside a broad patch
                f.material_index = bi
    bm.to_mesh(me); bm.free(); me.update()
    return o


def _flat_scree(seed, cx, cy, R, keys, n=10, zmax=0.4, scale=(1.3, 1.0, 0.6)):
    """Scree ring around a free-standing formation (like wd._scree_skirt but placeable)."""
    rnd = random.Random(seed + 700)
    for i in range(n):
        a = rnd.uniform(0, 2 * PI)
        d = R * rnd.uniform(0.85, 1.25)
        r = rnd.uniform(0.7, 2.2)
        rock(nm('scr'), r, (cx + math.cos(a) * d, cy + math.sin(a) * d, r * 0.25 + rnd.uniform(0, zmax)),
             rnd.choice(keys), seed=seed + i, scale=scale, subdiv=2, amp=0.34)


# ================================================================== F07_01..03 ROCK SPIRES
SPIRE_RULES = lambda H: [
    ('wd_rock_dark',  lambda c, nz, ny, t, nv: nv < -0.22 or t < 0.12),
    ('wd_rock_light', lambda c, nz, ny, t, nv: nv > 0.34),
    ('wd_moss',       lambda c, nz, ny, t, nv: nz > 0.74 and t < 0.4 and nv > -0.05),
    ('wd_rock_grey',  lambda c, nz, ny, t, nv: True),
]


def _spire(seed, H, Rbase, Rtop, name, lean=0.0, split=False, ledge_tree=False):
    """Slender carved monolith: a tall fast-tapering tower with CONTINUOUS vertical fluting
    (deep carved grooves running the full height) and only faint horizontal weathering, so it
    reads as a single eroded finger of rock, never a stack of discs. Built as a fine revolved
    mesh directly (not _landform's bedded path, which bulges into stacked bowls)."""
    reset()
    rnd = random.Random(seed)
    nx, nz = 36, 54
    flutes = 7 + (seed % 4)                 # number of vertical flutes carved around the shaft
    bm = bmesh.new()
    rings = []
    for iz in range(nz + 1):
        t = iz / nz
        z = H * t
        # fast concave taper -> a true spire silhouette (narrow, pointed)
        base_r = Rbase * (1 - t) ** 1.35 + Rtop
        # gentle, irregular bulges/pinches along the height (low frequency, small) - NOT bedded steps
        base_r *= 1.0 + 0.08 * N.noise(Vector((seed, seed, z * 0.08)))
        if base_r < Rtop * 0.5:
            rings.append([bm.verts.new((0, 0, z))]); continue
        ring = []
        for ix in range(nx):
            a = 2 * PI * ix / nx
            cx, cy = math.cos(a), math.sin(a)
            # deep vertical flutes: sinusoid in angle, slightly twisting with height
            flute = 0.5 + 0.5 * math.cos(a * flutes + t * 1.4 + seed)   # 0..1, 1 = ridge
            rr = base_r * (0.78 + 0.22 * flute)
            # multi-octave surface roughness so faces are carved, never smooth
            disp = 0.0
            for (fr, amp) in [(1.3, 1.0), (3.1, 0.4), (6.5, 0.2)]:
                disp += amp * N.noise(Vector((cx * fr + seed, cy * fr + seed * 2, z * fr * 0.12)))
            rr *= 1.0 + 0.10 * disp
            # faint horizontal weathering bands (small radial notch every few studs)
            rr *= 1.0 - 0.04 * max(0.0, math.sin(z * 0.9 + disp * 2.0))
            x = cx * rr + lean * H * (t ** 1.5)
            ring.append(bm.verts.new((x, cy * rr, z)))
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
    if len(rings[0]) > 1:
        bm.faces.new(list(reversed(rings[0])))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj_from_bm(name + '_body', bm, 'wd_rock_grey')
    if split:                                           # cleave the top third into two prongs
        me = o.data
        bm = bmesh.new(); bm.from_mesh(me)
        for v in bm.verts:
            if v.co.z > H * 0.62:
                up = (v.co.z - H * 0.62) / (H * 0.38)
                v.co.z -= 0.6 * H * 0.38 * math.exp(-((v.co.x - lean * H) / (Rtop * 1.2)) ** 2) * up
                if v.co.x > lean * H:
                    v.co.z *= 0.92
        bm.to_mesh(me); bm.free(); me.update()
    _paint(o, seed, SPIRE_RULES(H), H)
    _flat_scree(seed, lean * H * 0.9, 0, Rbase * 1.0, ('wd_rock_grey', 'wd_rock_dark', 'wd_scree'), n=10)
    if ledge_tree:
        lx = Rbase * 0.35 + lean * H * 0.5
        lz = H * 0.5
        o2 = rock(nm('ledge'), 2.2, (lx, -Rbase * 0.2, lz), 'wd_rock_dark', seed=seed + 3, scale=(1.6, 1.3, 0.4), subdiv=2, amp=0.3)
        top_paint(o2, 'wd_moss', 0.55, seed + 3)
        _mini_pine(lx, -Rbase * 0.2, lz + 0.5, 5.5, seed + 9)
    return finalize(name, smooth_angle=26)


def rock_spire_01():
    """Slender straight spire, 48 tall, fluted grey granite with a mossy top."""
    return _spire(101, 48.0, 7.5, 1.3, 'rock_spire_01')

def rock_spire_02():
    """Leaning spire, ~40 tall, tilts to one side like a toppling finger of rock."""
    return _spire(102, 40.0, 7.0, 1.4, 'rock_spire_02', lean=0.22)

def rock_spire_03():
    """Split-top spire, 44 tall, with a small ledge and a lone wind-bent pine."""
    return _spire(103, 44.0, 8.0, 1.6, 'rock_spire_03', split=True, ledge_tree=True)


# ================================================================== F07_04..06 SEA STACKS
def _sea_stack(seed, H, Rbase, Rtop, name, twin=False):
    """Weathered sea stack: an IRREGULAR faceted column - leaning axis, uneven elliptical section,
    uneven ledges and a wave-cut undercut - broken into angular plates with vertical fractures
    (_facet), coloured by geology in low-frequency patches (_geo_paint), with guano only as sparse
    pale drips under the upper ledges. Not a corrugated barrel and not evenly banded."""
    reset()
    rnd = random.Random(seed)
    nx, nz = 44, 40
    bm = bmesh.new(); rings = []
    # irregular section: an ellipse that rotates and changes aspect with height
    e_a, e_b = rnd.uniform(1.05, 1.25), rnd.uniform(0.78, 0.95)
    lean_x, lean_y = rnd.uniform(-0.12, 0.12), rnd.uniform(-0.08, 0.08)
    for iz in range(nz + 1):
        t = iz / nz
        z = H * t
        base_r = Rbase * (1 - 0.26 * t)
        # wave-cut UNDERCUT: pinch the lowest ~16%, strongest on one side (asymmetric)
        if t < 0.16:
            base_r *= 0.58 + 0.42 * (t / 0.16)
        # a couple of uneven ledges (broad, irregular - not a periodic groove)
        for zc, dp in ((H * 0.42, 0.1), (H * 0.68, 0.08)):
            base_r *= 1.0 - dp * math.exp(-((z - zc) / 3.5) ** 2)
        lx, ly = lean_x * z, lean_y * z
        ring = []
        for ix in range(nx):
            a = 2 * PI * ix / nx
            cx, cy = math.cos(a) * e_a, math.sin(a) * e_b
            disp = 0.0
            for (fr, amp) in [(1.0, 1.0), (2.3, 0.5), (4.8, 0.26), (9.0, 0.13)]:
                disp += amp * N.noise(Vector((cx * fr + seed, cy * fr + seed * 2, z * fr * 0.11)))
            rr = base_r * (1.0 + 0.12 * disp)
            ring.append(bm.verts.new((lx + cx * rr, ly + cy * rr, z)))
        rings.append(ring)
    for A, B in zip(rings, rings[1:]):
        n = len(A)
        for i in range(n):
            bm.faces.new((A[i], A[(i + 1) % n], B[(i + 1) % n], B[i]))
    bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    # break into angular plates + vertical fractures
    _facet(bm, seed, amp=0.1, cell=0.4)
    o = _obj_from_bm(name + '_body', bm, 'wd_rock_grey')
    if twin:                                            # cleave the top third into two uneven heads
        me = o.data
        bm = bmesh.new(); bm.from_mesh(me)
        for v in bm.verts:
            if v.co.z > H * 0.52:
                up = (v.co.z - H * 0.52) / (H * 0.48)
                v.co.z -= 0.6 * H * 0.48 * math.exp(-(v.co.x / (Rtop * 1.5)) ** 2) * up
                if v.co.x > 0:
                    v.co.z *= 0.82                      # one head clearly lower -> not a flat slab
        bm.to_mesh(me); bm.free(); me.update()
    # geology colour: two greys in big low-freq patches (no bright light tone -> no white band); wet foot added below
    _geo_paint(o, seed, H, ('wd_rock_dark', 'wd_rock_grey'), patch=0.13)
    # overpaint the wave-washed foot + sparse guano drips under the upper ledges
    me = o.data
    for k in ('wk_kelp', 'wk_wet_rock', 'wk_guano'):
        if k not in [m.name.split('|')[0] for m in me.materials]:
            me.materials.append(mat(k))
    idx = {m.name.split('|')[0]: i for i, m in enumerate(me.materials)}
    bm = bmesh.new(); bm.from_mesh(me)
    off = Vector((seed * 5.1, seed * 2.3, 0))
    guano = 0
    nfaces = len(bm.faces)
    for f in bm.faces:
        c = f.calc_center_median(); t = c.z / H; nz_ = f.normal.z
        if t < 0.06:
            f.material_index = idx['wk_kelp']
        elif t < 0.17:
            f.material_index = idx['wk_wet_rock']
        else:
            # guano: pale drips only just UNDER the two ledges, on steep faces, irregular, capped <15%
            under = math.exp(-((c.z - (H * 0.42 - 2.0)) / 2.0) ** 2) + math.exp(-((c.z - (H * 0.68 - 2.0)) / 2.0) ** 2)
            drip = N.noise(c * 0.5 + off)
            if nz_ < 0.4 and under > 0.5 and drip > 0.45 and guano < nfaces * 0.14:
                f.material_index = idx['wk_guano']; guano += 1
    bm.to_mesh(me); bm.free(); me.update()
    # irregular wave-cut rubble at the foot
    for i in range(6):
        a = rnd.uniform(0, 2 * PI); d = Rbase * rnd.uniform(0.85, 1.2)
        rock(nm('shelf'), rnd.uniform(1.4, 2.8), (math.cos(a) * d, math.sin(a) * d, 0.25),
             rnd.choice(('wk_wet_rock', 'wd_rock_dark', 'wk_kelp')), seed=seed + i, scale=(1.5, 1.2, 0.4), subdiv=2, amp=0.34)
    _flat_scree(seed, 0, 0, Rbase * 0.95, ('wk_wet_rock', 'wd_rock_dark', 'wk_kelp'), n=9)
    return finalize(name, smooth_angle=30)


def sea_stack_01():
    """Blocky sea stack, 44 tall, wave-cut notch, guano streaks, dark kelp foot, gull ledges."""
    return _sea_stack(104, 44.0, 16.0, 6.0, 'sea_stack_01')

def sea_stack_02():
    """Taller slimmer sea stack, 50 tall, deeper notch."""
    return _sea_stack(105, 50.0, 14.0, 5.0, 'sea_stack_02')

def sea_stack_03():
    """Twin-pinnacle sea stack, 40 tall, cleft into two heads above the notch."""
    return _sea_stack(106, 40.0, 18.0, 6.0, 'sea_stack_03', twin=True)


# ================================================================== F07_07..08 NATURAL ARCHES
def _pillar(seed, H, Rbase, Rtop, name_key, cx=0.0, cy=0.0):
    """A stubby carved rock pillar (arch leg / abutment): near-vertical fluted column with
    incised horizontal strata, built directly so it does not bulge like the bedded _landform path."""
    rnd = random.Random(seed)
    nx, nz = 32, 30
    bm = bmesh.new(); rings = []
    for iz in range(nz + 1):
        t = iz / nz
        z = H * t
        base_r = Rbase * (1 - (Rbase - Rtop) / Rbase * t)
        base_r *= 1.0 - 0.06 * (1.0 - max(0.0, math.sin(z / 3.0 * PI)))   # incised strata
        ring = []
        for ix in range(nx):
            a = 2 * PI * ix / nx
            cxx, cyy = math.cos(a), math.sin(a)
            disp = 0.0
            for (fr, amp) in [(1.2, 1.0), (2.8, 0.45), (5.8, 0.22)]:
                disp += amp * N.noise(Vector((cxx * fr + seed, cyy * fr + seed * 2, z * fr * 0.12)))
            rr = base_r * (1.0 + 0.10 * disp) * (1.0 + 0.05 * math.cos(a * 7 + seed))
            ring.append(bm.verts.new((cx + cxx * rr, cy + cyy * rr, z)))
        rings.append(ring)
    for A, B in zip(rings, rings[1:]):
        n = len(A)
        for i in range(n):
            bm.faces.new((A[i], A[(i + 1) % n], B[(i + 1) % n], B[i]))
    bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj_from_bm(name_key + '_body', bm, 'wd_rock_grey')
    _paint(o, seed, SPIRE_RULES(H), H)
    return o


def _roughen(o, seed, amp=0.9, freq=0.25):
    """Push a smooth mesh's verts along their own normal by noise so a tube reads as carved rock."""
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    bm.normal_update()
    off = Vector((seed * 3.1, seed * 1.7, seed * 0.9))
    for v in bm.verts:
        n = N.noise(v.co * freq + off) + 0.4 * N.noise(v.co * freq * 2.3 + off)
        v.co += v.normal * amp * n
    bm.to_mesh(me); bm.free(); me.update()
    return o


def natural_arch_tall():
    """F07_07: tall narrow arch a player walks under (opening >= 8 wide x 10 high), grey rock."""
    reset()
    seed = 107
    rnd = random.Random(seed)
    span, H = 24.0, 32.0        # legs centred at +/-12 -> ~16 clear between the inner faces
    _pillar(seed, 26.0, 6.5, 4.0, 'arch_tall_L', cx=-span / 2)
    _pillar(seed + 5, 24.0, 6.0, 3.8, 'arch_tall_R', cx=span / 2)
    # thick bowed span leaving a clear >=10 high gap under the crown
    xs = [-span / 2, -span / 4, 0.0, span / 4, span / 2]
    zs = [22.0, 28.5, H, 27.5, 21.0]
    a1 = tube(nm('arch'), [(x, 0.0, z) for x, z in zip(xs, zs)], 3.6, 'wd_rock_grey', res=7, ures=5,
              taper=[0.85, 1.0, 1.05, 1.0, 0.85])
    _roughen(a1, seed, amp=0.8)
    a2 = tube(nm('arch2'), [(x, 4.4, z - 0.5) for x, z in zip(xs, zs)], 2.4, 'wd_rock_dark', res=6, ures=4,
              taper=[0.85, 1.0, 1.0, 1.0, 0.85])
    _roughen(a2, seed + 3, amp=0.6)
    _flat_scree(seed, -span / 2, 0, 7.0, ('wd_rock_grey', 'wd_rock_dark', 'wd_scree'), n=7)
    _flat_scree(seed + 5, span / 2, 0, 6.5, ('wd_rock_grey', 'wd_rock_dark', 'wd_scree'), n=7)
    return finalize('natural_arch_tall', smooth_angle=26)


def natural_arch_bridge():
    """F07_08: wide low arch bridge, 60 wide, a broad span of rock from bank to bank."""
    reset()
    seed = 108
    rnd = random.Random(seed)
    W = 60.0
    for sgn in (-1, 1):
        _pillar(seed + (0 if sgn < 0 else 6), 18.0, 12.0, 8.5, 'arch_bridge_%d' % sgn, cx=sgn * (W / 2 - 6))
    # broad low span: a wide ribbon of rock, thick, gentle rise, opening beneath for water/path
    xs = [-(W / 2 - 6), -W / 4, 0.0, W / 4, (W / 2 - 6)]
    zs = [15.0, 21.0, 23.0, 21.0, 15.0]
    for yi, (yoff, rad, key) in enumerate(((-4.0, 5.0, 'wd_rock_grey'), (0.0, 6.0, 'wd_rock_grey'), (4.0, 5.0, 'wd_rock_dark'))):
        sp = tube(nm('span'), [(x, yoff, z) for x, z in zip(xs, zs)], rad, key, res=7, ures=5,
                  taper=[0.85, 1.0, 1.05, 1.0, 0.85])
        _roughen(sp, seed + yi, amp=0.9)
    # grass + a couple of rocks on the crown deck
    deck = rock(nm('deck'), 9.0, (0, 0, 23.5), 'wd_rock_grey', seed=seed + 2, scale=(2.4, 0.9, 0.22), subdiv=3, amp=0.18)
    top_paint(deck, 'wk_grass_cap', 0.55, seed + 2)
    _flat_scree(seed, -(W / 2 - 6), 0, 12.0, ('wd_rock_grey', 'wd_rock_dark', 'wd_scree'), n=8)
    _flat_scree(seed + 6, (W / 2 - 6), 0, 12.0, ('wd_rock_grey', 'wd_rock_dark', 'wd_scree'), n=8)
    return finalize('natural_arch_bridge', smooth_angle=26)


# ================================================================== F07_09..11 COASTAL CLIFFS (tileable panels)
def _coastal_panel(seed, name, bands, ledges):
    """60 wide x 25 deep x 45 tall tiling coastal cliff: wave-cut notch low, strata, grass cap."""
    reset()
    H = 45.0
    PAL[name + '_base'] = PAL['wd_rock_grey']
    o = _front_panel(60.0, 25.0, H, seed, strata_h=3.2, bands=bands, ledges=ledges, warp=3.4, name_key=name)
    # carve a wave-cut notch: pull the lowest front band inward (toward +Y, i.e. recessed)
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts:
        if v.co.z < 7.0 and v.co.y < 0:                 # front face, low band
            rec = math.exp(-((v.co.z - 3.0) / 2.6) ** 2)
            v.co.y += 3.2 * rec                          # move toward back = undercut
    bm.to_mesh(me); bm.free(); me.update()
    # paint: grey rock strata (NO mid-cliff moss - coastal cliffs are wet rock, grass only on the cap)
    _paint_panel(o, seed, {'base': 'wd_rock_grey', 'dark': 'wd_rock_dark', 'light': 'wd_rock_light'},
                 snow=False, moss=False, H=H)
    _despeckle(o, 'wd_rock_light', 'wd_rock_grey', keep=0.3, seed=seed)
    # overpaint: dark wet/kelp band across the lower cliff, thin grass cap on the very top
    me = o.data
    for k in ('wk_wet_rock', 'wk_kelp', 'wk_grass_cap'):
        if k not in [m.name.split('|')[0] for m in me.materials]:
            me.materials.append(mat(k))
    idx = {m.name.split('|')[0]: i for i, m in enumerate(me.materials)}
    bm = bmesh.new(); bm.from_mesh(me)
    for f in bm.faces:
        c = f.calc_center_median()
        nz_ = f.normal.z
        if c.z < 3.0:
            f.material_index = idx['wk_kelp']            # dark kelp at the very foot
        elif c.z < 8.0:
            f.material_index = idx['wk_wet_rock']        # wave-washed wet band
        elif c.z > H - 2.4 and nz_ > 0.45:
            f.material_index = idx['wk_grass_cap']       # grass only on the cap
    bm.to_mesh(me); bm.free(); me.update()
    _scree(seed, 60.0, ('wk_wet_rock', 'wd_rock_dark', 'wk_kelp'))
    # a few grass tufts on the cap
    rnd = random.Random(seed + 40)
    for i in range(7):
        x = rnd.uniform(-26, 26)
        for b in range(4):
            a = rnd.uniform(0, 6.28)
            tube(nm('gt'), [(x, rnd.uniform(-2, 2), H), (x + math.cos(a) * 0.4, rnd.uniform(-2, 2), H + 1.1)],
                 0.07, 'wk_grass_cap', res=4, taper=[1, 0.05], ures=2)
    return finalize(name, smooth_angle=28)


def coastal_cliff_01():
    """Tiling coastal cliff, grey rock, broad strata, wave-cut notch, grass cap."""
    return _coastal_panel(109, 'coastal_cliff_01', bands=[16, 30], ledges=[(22, 2.2)])

def coastal_cliff_02():
    """Tiling coastal cliff, busier cracks, two notched ledges."""
    return _coastal_panel(110, 'coastal_cliff_02', bands=[12, 24, 36], ledges=[(18, 2.0), (30, 2.2)])

def coastal_cliff_03():
    """Tiling coastal cliff, tall clean beds, single high ledge."""
    return _coastal_panel(111, 'coastal_cliff_03', bands=[20, 34], ledges=[(28, 2.6)])


# ================================================================== R04_01..03 SEA CLIFFS (big tiling panels, 100x40x55)
def _sea_cliff(seed, name, look, bands, ledges):
    reset()
    H = 55.0
    PAL[name + '_base'] = PAL['wd_rock_grey'] if look != 'chalk' else PAL['wk_chalk']
    warp = 4.0 if look != 'basalt' else 5.0
    o = _front_panel(100.0, 40.0, H, seed, strata_h=3.4 if look != 'basalt' else 4.6,
                     bands=bands, ledges=ledges, warp=warp, name_key=name)
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts:
        if v.co.z < 9.0 and v.co.y < 0:                 # wave-cut notch at the sea line
            rec = math.exp(-((v.co.z - 3.5) / 3.0) ** 2)
            v.co.y += 3.6 * rec
        if look == 'basalt' and v.co.y < 0:             # vertical columns: fluting on the front
            v.co.y += 0.6 * math.sin(v.co.x * 1.1 + seed)
    bm.to_mesh(me); bm.free(); me.update()
    if look == 'chalk':
        keyset = {'base': 'wk_chalk', 'dark': 'wk_chalk_dk', 'light': 'wd_rock_light'}
        _paint_panel(o, seed, keyset, snow=False, moss=False, H=H)
        _despeckle(o, 'wd_rock_light', 'wk_chalk', keep=0.3, seed=seed)
    elif look == 'basalt':
        keyset = {'base': 'wd_basalt', 'dark': 'wd_basalt_dark', 'light': 'wd_slate', 'stain': 'wd_stain'}
        _paint_panel(o, seed, keyset, snow=False, moss=False, stain=True, H=H)
        _despeckle(o, 'wd_slate', 'wd_basalt', keep=0.3, seed=seed)
    else:  # sandstone with caves
        _paint_sandstone(o, seed, H)
    # wet notch band + sea caves for sandstone/chalk
    me = o.data
    for k in ('wk_wet_rock', 'wk_kelp', 'wk_cave_dark'):
        if k not in [m.name.split('|')[0] for m in me.materials]:
            me.materials.append(mat(k))
    idx = {m.name.split('|')[0]: i for i, m in enumerate(me.materials)}
    bm = bmesh.new(); bm.from_mesh(me)
    cave_xs = [-30.0, 14.0] if look != 'basalt' else []
    for f in bm.faces:
        c = f.calc_center_median()
        nz_ = f.normal.z
        if c.z < 3.0:
            f.material_index = idx['wk_kelp']            # dark kelp at the foot
        elif c.z < 9.0:
            f.material_index = idx['wk_wet_rock']        # wave-washed wet band, all low faces
        for cx in cave_xs:                               # dark cave mouths at the sea line
            if abs(c.x - cx) < 6.0 and c.z < 11.0 and c.y < 2.0 and nz_ < 0.5:
                f.material_index = idx['wk_cave_dark']
    bm.to_mesh(me); bm.free(); me.update()
    screekeys = {'chalk': ('wk_chalk', 'wk_chalk_dk', 'wk_wet_rock'),
                 'basalt': ('wd_basalt', 'wd_basalt_dark', 'wd_scree_dark'),
                 'sandstone': ('wd_sandstone', 'wd_sandstone_dk', 'wk_wet_rock')}[look]
    _scree(seed, 100.0, screekeys, n=18)
    return finalize(name, smooth_angle=30)


def sea_cliff_01():
    """R04_01: pale chalky layered sea cliff, 100x40x55, tiling, wave-cut notch."""
    return _sea_cliff(401, 'sea_cliff_01', 'chalk', bands=[18, 34, 48], ledges=[(26, 2.4)])

def sea_cliff_02():
    """R04_02: dark volcanic sea cliff with columnar fluting, 100x40x55, tiling."""
    return _sea_cliff(402, 'sea_cliff_02', 'basalt', bands=[16, 32, 46], ledges=[(24, 2.6)])

def sea_cliff_03():
    """R04_03: red-brown sandstone sea cliff with caves, 100x40x55, tiling."""
    return _sea_cliff(403, 'sea_cliff_03', 'sandstone', bands=[20, 36], ledges=[(14, 2.0), (40, 2.4)])


# ================================================================== R05_01..02 LARGE WATERFALL CLIFFS (80x50x75)
def _water_sheet(xc, y_lip, z_top, z_bot, width, out, rnd, ns=16):
    """Falling water sheet + foam streaks + splash rings (same recipe as d09.waterfall)."""
    H = z_top - z_bot
    fn = lambda s: (y_lip - 0.3 - out * s ** 2.2, z_top - H * s)
    # body
    bm = bmesh.new(); grid = []
    for j in range(ns + 1):
        s = j / ns
        y, z = fn(s)
        row = []
        for i in range(9):
            u = i / 8
            x = xc + (u - 0.5) * width * (1 + 0.1 * s)
            rip = 0.12 * math.sin(u * 7 + s * 11)
            row.append(bm.verts.new((x, y + rip, z)))
        grid.append(row)
    for j in range(ns):
        for i in range(8):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    o = _obj_from_bm(nm('wt'), bm, 'water_fx')
    o.modifiers.new('sol', 'SOLIDIFY').thickness = 0.35
    # foam streaks: broad, bright, placed slightly IN FRONT of the water so they read from the front
    for u in (0.12, 0.3, 0.5, 0.7, 0.88):
        u += rnd.uniform(-0.03, 0.03)
        bm = bmesh.new(); col = []
        for j in range(ns + 1):
            s = j / ns
            y, z = fn(s)
            x = xc + (u - 0.5) * width
            wobble = 0.25 * math.sin(s * 9 + u * 6)
            col.append((bm.verts.new((x - 0.6 + wobble, y - 0.5, z)), bm.verts.new((x + 0.6 + wobble, y - 0.5, z))))
        for j in range(ns):
            bm.faces.new((col[j][0], col[j][1], col[j + 1][1], col[j + 1][0]))
        fo = _obj_from_bm(nm('fm'), bm, 'foam')
        fo.modifiers.new('sol', 'SOLIDIFY').thickness = 0.12
    # splash basin foam
    ylan = y_lip - 0.3 - out
    for k in range(9):
        a = rnd.uniform(0, 2 * PI); d = rnd.uniform(0, width * 0.5)
        ball(nm('sp'), rnd.uniform(0.8, 1.6), (xc + math.cos(a) * d, ylan + math.sin(a) * d * 0.5, z_bot + 0.3),
             'foam', segs=7, rings=4, scale=(1.2, 1.0, 0.55))
    for R in (width * 0.6, width * 0.95):
        from kitlib import torus
        torus(nm('rg'), R, 0.1, loc=(xc, ylan - 0.4, z_bot + 0.15), key='foam', segs=22, rsegs=4)


def _waterfall_cliff(seed, name, twin=False):
    """80 wide x 50 deep x 75 tall rock headwall with a falling sheet, splash basin with boulders,
    mossy ledges, ferns and a few trees on top."""
    reset()
    rnd = random.Random(seed)
    H = 75.0
    PAL[name + '_base'] = PAL['wd_rock_grey']
    # headwall: a tiling-style front panel, but with a vertical slot carved for the fall
    o = _front_panel(80.0, 40.0, H, seed, strata_h=4.0, bands=[20, 40, 58], ledges=[(28, 2.6), (50, 2.2)],
                     warp=4.2, name_key=name)
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    slots = [(-14.0, 7.0), (14.0, 7.0)] if twin else [(0.0, 8.0)]
    for v in bm.verts:
        if v.co.y < 0:
            for (sx, sw) in slots:
                if abs(v.co.x - sx) < sw and v.co.z > 10.0:
                    rec = math.exp(-((v.co.x - sx) / (sw * 0.7)) ** 2)
                    v.co.y += 4.5 * rec                  # recess the channel behind the water
    bm.to_mesh(me); bm.free(); me.update()
    _paint_panel(o, seed, {'base': 'wd_rock_grey', 'dark': 'wd_rock_dark', 'light': 'wd_rock_light'},
                           snow=False, moss=False, H=H)
    # the fall(s)
    z_top = H - 3.0
    if twin:
        _water_sheet(-14.0, -17.0, z_top, 1.0, 5.5, 5.0, rnd)
        _water_sheet(14.0, -17.0, z_top, 1.0, 5.5, 5.0, rnd)
        # the dividing rock pillar between the two falls
        pil = rock(nm('pillar'), 6.0, (0, -14.0, H * 0.5), 'wd_rock_dark', seed=seed + 2, scale=(0.7, 0.8, 1.6), subdiv=3, amp=0.3)
        top_paint(pil, 'wd_moss', 0.5, seed + 2)
    else:
        _water_sheet(0.0, -17.0, z_top, 1.0, 7.0, 5.5, rnd)
    # splash basin: a shallow water disc + ring of boulders at the foot
    ball(nm('pool'), 1.0, (0, -22.0, 0.5), 'water', segs=26, rings=7, scale=(14.0, 8.0, 0.5))
    for i in range(14):
        a = rnd.uniform(0, 2 * PI)
        x = math.cos(a) * rnd.uniform(9, 15)
        y = -22.0 + math.sin(a) * rnd.uniform(5, 9)
        o2 = rock(nm('bd'), rnd.uniform(1.6, 3.4), (x, y, 0.5), rnd.choice(('wd_rock_grey', 'wd_rock_dark')),
                  seed=seed + 10 + i, scale=(1.3, 1.1, 0.7), subdiv=3, amp=0.34)
        top_paint(o2, 'wd_moss', 0.5, i)
    # mossy ledges with ferns, and a few pines/oaks on top
    for (zc, dp) in ((28, 2.6), (50, 2.2)):
        for sx in (-1, 1):
            x = sx * rnd.uniform(18, 34)
            blob(nm('lm'), rnd.uniform(1.5, 2.6), (x, -4.0, zc + 0.1), 'wd_moss', subdiv=2, amp=0.3, scale=(1.6, 1.0, 0.3), seed=int(zc) + sx)
            # ferns as small blade fans
            for b in range(5):
                a = rnd.uniform(0, 6.28)
                tube(nm('fn'), [(x, -4.0, zc), (x + math.cos(a) * 1.2, -5.0, zc + 1.8), (x + math.cos(a) * 1.6, -6.0, zc + 1.2)],
                     0.09, 'wd_moss', res=4, taper=[1, 0.6, 0.05], ures=2)
    _tree_cap(0, 6.0, H + 1.0, 30.0, 6, seed, ('pine', 'oak'))
    _scree(seed, 80.0, ('wd_rock_grey', 'wd_rock_dark', 'wd_scree'), n=14)
    return finalize(name, smooth_angle=30)


def waterfall_cliff_large_01():
    """R05_01: single-fall headwall, 80x50x75, splash basin, mossy ledges, trees on top."""
    return _waterfall_cliff(501, 'waterfall_cliff_large_01', twin=False)

def waterfall_cliff_large_02():
    """R05_02: twin falls splitting around a central rock pillar, 80x50x75."""
    return _waterfall_cliff(502, 'waterfall_cliff_large_02', twin=True)


# ================================================================== R06_01..03 CANYON WALLS (100x40x90 tiling)
def _canyon_wall(seed, name, look, bands, ledges):
    reset()
    H = 90.0
    base = {'red': PAL['wd_bl_red'], 'limestone': PAL['wk_chalk'], 'basalt': PAL['wd_basalt']}[look]
    PAL[name + '_base'] = base
    warp = 3.6 if look != 'basalt' else 5.2
    o = _front_panel(100.0, 40.0, H, seed, strata_h=3.0 if look == 'red' else (3.6 if look == 'limestone' else 4.8),
                     bands=bands, ledges=ledges, warp=warp, name_key=name)
    if look == 'limestone':
        me = o.data                                      # deep vertical fissures on the front
        bm = bmesh.new(); bm.from_mesh(me)
        for v in bm.verts:
            if v.co.y < 0:
                fis = math.sin(v.co.x * 0.9 + seed)
                if fis > 0.6:
                    v.co.y += 2.4 * (fis - 0.6)
        bm.to_mesh(me); bm.free(); me.update()
    if look == 'basalt':
        me = o.data                                      # columnar fluting
        bm = bmesh.new(); bm.from_mesh(me)
        for v in bm.verts:
            if v.co.y < 0:
                v.co.y += 0.7 * math.sin(v.co.x * 1.2 + seed)
        bm.to_mesh(me); bm.free(); me.update()
    if look == 'red':
        _paint_badlands_wall(o, seed, H)
    elif look == 'limestone':
        _paint_panel(o, seed, {'base': 'wk_chalk', 'dark': 'wk_chalk_dk', 'light': 'wd_rock_light'},
                     snow=False, moss=False, H=H)
    else:
        _paint_panel(o, seed, {'base': 'wd_basalt', 'dark': 'wd_basalt_dark', 'light': 'wd_slate',
                               'stain': 'wd_stain'}, snow=False, moss=False, stain=True, H=H)
    screekeys = {'red': ('wd_bl_talus', 'wd_bl_sand', 'wd_bl_orange'),
                 'limestone': ('wk_chalk', 'wk_chalk_dk', 'wd_scree_grey'),
                 'basalt': ('wd_basalt', 'wd_basalt_dark', 'wd_scree_dark')}[look]
    _scree(seed, 100.0, screekeys, n=18)
    _tuft_on_ledges(seed, 100.0, ledges, 'wd_moss', n=5)
    return finalize(name, smooth_angle=30)


def _paint_badlands_wall(o, seed, H):
    """Red banded sandstone: horizontal red/orange/sand/cream stripes (reuse wd badlands palette)."""
    me = o.data
    for k in ('wd_bl_dark', 'wd_bl_red', 'wd_bl_orange', 'wd_bl_sand', 'wd_bl_cream', 'wd_bl_talus'):
        if k not in [m.name.split('|')[0] for m in me.materials]:
            me.materials.append(mat(k))
    idx = {m.name.split('|')[0]: i for i, m in enumerate(me.materials)}
    bm = bmesh.new(); bm.from_mesh(me)
    off = Vector((seed * 2.3, seed * 1.1, 0))
    for f in bm.faces:
        c = f.calc_center_median()
        if c.z < 6.0:
            pick = 'wd_bl_talus'
        else:
            nv = N.noise(c * 0.18 + off)
            s = int(c.z / 3.0 + 0.4 * nv) % 5
            pick = ('wd_bl_dark', 'wd_bl_red', 'wd_bl_orange', 'wd_bl_sand', 'wd_bl_cream')[s]
        f.material_index = idx[pick]
    bm.to_mesh(me); bm.free(); me.update()
    return o


def canyon_wall_01():
    """R06_01: red banded sandstone canyon wall, 100x40x90, tiling."""
    return _canyon_wall(601, 'canyon_wall_01', 'red', bands=[24, 44, 64], ledges=[(32, 2.4), (56, 2.6)])

def canyon_wall_02():
    """R06_02: grey limestone canyon wall with vertical fissures, 100x40x90, tiling."""
    return _canyon_wall(602, 'canyon_wall_02', 'limestone', bands=[20, 40, 60, 78], ledges=[(48, 2.8)])

def canyon_wall_03():
    """R06_03: dark basalt columnar canyon wall, 100x40x90, tiling."""
    return _canyon_wall(603, 'canyon_wall_03', 'basalt', bands=[28, 52, 72], ledges=[(38, 2.4), (62, 2.2)])


# ================================================================== E15_01..06 BOULDERS (3-10 studs)
def boulder_round():
    """E15_01: round granite boulder, ~7 studs, faceted and weathered."""
    reset()
    o = rock('b', 3.4, (0, 0, 2.4), 'wd_granite', seed=1501, scale=(1.1, 1.0, 0.95), subdiv=3, amp=0.3)
    o2 = rock('b2', 1.4, (3.0, -1.2, 0.8), 'wd_granite_dark', seed=1502, scale=(1.2, 1.0, 0.7), subdiv=3, amp=0.3)
    top_paint(o, 'wd_moss', 0.88, 1501, noise_amt=0.45)   # patchy, not a flat cap
    return finalize('boulder_round', smooth_angle=20)


def boulder_slab():
    """E15_02: angular slab boulder, ~9 studs long, sharp bedded edges."""
    reset()
    rnd = random.Random(1503)
    # angular bedded slab: an irregular polygon outline extruded, then tilted -> sharp flat facets
    pts = [(-4.5, -2.0), (-3.6, -2.6), (3.8, -2.2), (4.6, -0.4), (4.2, 1.8), (2.0, 2.7), (-2.8, 2.4), (-4.4, 0.8)]
    o = poly_prism('slab', pts, 2.6, loc=(0, 0, 0), key='wd_slate')
    # shear the top face so the slab is a tilted wedge (one end thicker), and jitter top verts for bedding
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts:
        if v.co.z > 1.3:
            v.co.z += 0.9 * (v.co.x / 4.5) + 0.25 * N.noise(Vector((v.co.x, v.co.y, 0)))   # bedded tilt
    bm.to_mesh(me); bm.free(); me.update()
    o.rotation_euler = (math.radians(4), math.radians(-10), math.radians(18))
    o2 = rock('chip', 1.1, (-4.0, 1.8, 0.6), 'wd_slate', seed=1504, scale=(1.4, 1.0, 0.35), subdiv=2, amp=0.25)
    top_paint(o, 'wd_moss', 0.9, 1503, noise_amt=0.4)
    return finalize('boulder_slab', smooth_angle=34)


def boulder_cracked():
    """E15_03: cracked boulder split into two halves with a gap between."""
    reset()
    a = rock('a', 2.8, (-1.8, 0, 2.0), 'wd_rock_grey', seed=1505, scale=(0.8, 1.1, 1.0), subdiv=3, amp=0.3)
    b = rock('b', 2.6, (2.0, 0.4, 1.8), 'wd_rock_grey', seed=1506, scale=(0.8, 1.1, 0.95), subdiv=3, amp=0.3)
    # dark crack faces hinted by a thin dark sliver between
    c = rock('c', 0.9, (0.1, -1.6, 0.6), 'wd_rock_dark', seed=1507, scale=(1.3, 1.0, 0.6), subdiv=2, amp=0.3)
    top_paint(a, 'wd_moss', 0.82, 1505); top_paint(b, 'wd_moss', 0.84, 1506)
    return finalize('boulder_cracked', smooth_angle=20)


def boulder_mossy():
    """E15_04: mossy boulder with a flat top (a natural seat/step)."""
    reset()
    o = blob('rock', 3.6, (0, 0, 2.0), 'wd_rock_dark', subdiv=3, amp=0.24, scale=(1.2, 1.1, 0.7), seed=1508, flat_bottom=-1.2)
    # flatten the very top so it reads as a flat-topped rock
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts:
        if v.co.z > 2.4:
            v.co.z = 2.4 + (v.co.z - 2.4) * 0.15
    bm.to_mesh(me); bm.free(); me.update()
    top_paint(o, 'wd_moss', 0.7, 1508, noise_amt=0.5)    # mossy but patchy (flat top mostly moss)
    o2 = rock('b2', 1.1, (2.8, -1.0, 0.7), 'wd_rock_dark', seed=1509, scale=(1.2, 1.0, 0.6), subdiv=2, amp=0.3)
    return finalize('boulder_mossy', smooth_angle=20)


def boulder_leaning_pair():
    """E15_05: a pair of leaning boulders resting against each other."""
    reset()
    a = rock('a', 2.6, (-1.4, 0, 2.2), 'wd_granite', seed=1510, scale=(0.85, 1.0, 1.1), subdiv=3, amp=0.3)
    a.rotation_euler = (0, math.radians(16), 0)
    b = rock('b', 2.4, (1.6, 0.3, 2.0), 'wd_granite_dark', seed=1511, scale=(0.85, 1.0, 1.05), subdiv=3, amp=0.3)
    b.rotation_euler = (0, math.radians(-18), 0)
    top_paint(a, 'wd_moss', 0.8, 1510); top_paint(b, 'wd_moss', 0.82, 1511)
    return finalize('boulder_leaning_pair', smooth_angle=20)


def boulder_flat_wide():
    """E15_06: low wide flat-topped rock (a natural platform), ~10 studs across."""
    reset()
    o = blob('rock', 5.0, (0, 0, 1.4), 'wd_rock_grey', subdiv=3, amp=0.18, scale=(1.3, 1.1, 0.4), seed=1512, flat_bottom=-0.8)
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts:
        if v.co.z > 1.6:
            v.co.z = 1.6 + (v.co.z - 1.6) * 0.12
    bm.to_mesh(me); bm.free(); me.update()
    top_paint(o, 'wd_moss', 0.78, 1512, noise_amt=0.4)
    for i in range(3):
        rock(nm('chip'), 0.8, (math.cos(i * 2) * 5.0, math.sin(i * 2) * 3.5, 0.4), 'wd_rock_dark', seed=1512 + i, scale=(1.2, 1.0, 0.5), subdiv=2, amp=0.3)
    return finalize('boulder_flat_wide', smooth_angle=20)


# ================================================================== batches
V = lambda: (0.0, -1.0, 0.2)
BATCH_F07_SPIRES = [
    ('F07_01_rock_formation_01', rock_spire_01, (0.45, -1.1, 0.35)),
    ('F07_02_rock_formation_02', rock_spire_02, (0.45, -1.1, 0.35)),
    ('F07_03_rock_formation_03', rock_spire_03, (0.45, -1.1, 0.35)),
]
BATCH_F07_STACKS = [
    ('F07_04_rock_formation_04', sea_stack_01, (0.45, -1.1, 0.35)),
    ('F07_05_rock_formation_05', sea_stack_02, (0.45, -1.1, 0.35)),
    ('F07_06_rock_formation_06', sea_stack_03, (0.45, -1.1, 0.35)),
]
BATCH_F07_ARCHES = [
    ('F07_07_rock_formation_07', natural_arch_tall, (0.3, -1.1, 0.25)),
    ('F07_08_rock_formation_08', natural_arch_bridge, (0.3, -1.1, 0.25)),
]
BATCH_F07_COAST = [
    ('F07_09_rock_formation_09', coastal_cliff_01, (0.0, -1.0, 0.2)),
    ('F07_10_rock_formation_10', coastal_cliff_02, (0.0, -1.0, 0.2)),
    ('F07_11_rock_formation_11', coastal_cliff_03, (0.0, -1.0, 0.2)),
]
BATCH_R04 = [
    ('R04_01_sea_cliff_01', sea_cliff_01, (0.0, -1.0, 0.2)),
    ('R04_02_sea_cliff_02', sea_cliff_02, (0.0, -1.0, 0.2)),
    ('R04_03_sea_cliff_03', sea_cliff_03, (0.0, -1.0, 0.2)),
]
BATCH_R05 = [
    ('R05_01_waterfall_cliff_large_01', waterfall_cliff_large_01, (0.3, -1.1, 0.28)),
    ('R05_02_waterfall_cliff_large_02', waterfall_cliff_large_02, (0.3, -1.1, 0.28)),
]
BATCH_R06 = [
    ('R06_01_canyon_wall_01', canyon_wall_01, (0.0, -1.0, 0.25)),
    ('R06_02_canyon_wall_02', canyon_wall_02, (0.0, -1.0, 0.25)),
    ('R06_03_canyon_wall_03', canyon_wall_03, (0.0, -1.0, 0.25)),
]
BATCH_E15 = [
    ('E15_01_boulder_01', boulder_round, (0.7, -1.1, 0.5)),
    ('E15_02_boulder_02', boulder_slab, (0.7, -1.1, 0.5)),
    ('E15_03_boulder_03', boulder_cracked, (0.7, -1.1, 0.5)),
    ('E15_04_boulder_04', boulder_mossy, (0.7, -1.1, 0.5)),
    ('E15_05_boulder_05', boulder_leaning_pair, (0.7, -1.1, 0.5)),
    ('E15_06_boulder_06', boulder_flat_wide, (0.7, -1.1, 0.7)),
]

BATCHES = {
    'f07_spires': ('v4_terrain', BATCH_F07_SPIRES),
    'f07_stacks': ('v4_terrain', BATCH_F07_STACKS),
    'f07_arches': ('v4_terrain', BATCH_F07_ARCHES),
    'f07_coast':  ('v4_terrain', BATCH_F07_COAST),
    'r04':        ('v4_terrain', BATCH_R04),
    'r05':        ('v4_terrain', BATCH_R05),
    'r06':        ('v4_terrain', BATCH_R06),
    'e15':        ('v4_terrain', BATCH_E15),
}
