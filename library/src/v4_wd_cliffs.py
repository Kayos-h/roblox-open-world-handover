"""v4_wd_cliffs - E13 rock_face: 10 large modular cliff panels that tile sideways.

Worker wd. Each panel is ~80 wide (X) x ~30 deep (Y) x ~60 tall (Z), front face toward -Y.
The front surface is a height field y(x, z): its displacement is built from an x-PERIODIC
noise (period = panel width) so the left and right edge profiles are identical and two panels
placed side by side show no seam. Layered strata come from quantising the inward cut by z;
ledges are extra inward steps; scree boulders ring the base. Materials per face by z / slope /
noise. New palette keys all prefixed wd_. Rock <= 40k tris. Do not edit shared files.
"""
import math, random, bmesh
from mathutils import Vector, noise as N
from kitlib import reset, finalize, PAL, _obj_from_bm, mat
from nature import rock, blob
from v4_elf import nm

# ------------------------------------------------------------------ palette (wd_ prefixed)
PAL['wd_granite']       = ((118, 120, 128), 'Rock',      0.00, 0.95, 0)
PAL['wd_granite_dark']  = ((82, 84, 92),    'Rock',      0.00, 0.96, 0)
PAL['wd_granite_light'] = ((158, 160, 168), 'Rock',      0.00, 0.92, 0)
PAL['wd_snow']          = ((238, 242, 248), 'Snow',      0.00, 0.70, 0)
PAL['wd_scree_grey']    = ((100, 100, 106), 'Rock',      0.00, 0.98, 0)

PAL['wd_sandstone']     = ((196, 150, 104), 'Sandstone', 0.00, 0.90, 0)
PAL['wd_sandstone_dk']  = ((162, 118, 78),  'Sandstone', 0.00, 0.92, 0)
PAL['wd_sandstone_lt']  = ((220, 182, 134), 'Sandstone', 0.00, 0.88, 0)
PAL['wd_sand_band']     = ((176, 134, 92),  'Sandstone', 0.00, 0.92, 0)
PAL['wd_scree_sand']    = ((170, 132, 92),  'Sandstone', 0.00, 0.95, 0)

PAL['wd_basalt']        = ((78, 80, 86),    'Basalt',    0.00, 0.92, 0)
PAL['wd_basalt_dark']   = ((54, 56, 62),    'Basalt',    0.00, 0.94, 0)
PAL['wd_slate']         = ((92, 96, 104),   'Slate',     0.00, 0.90, 0)
PAL['wd_moss']          = ((94, 106, 70),   'Grass',     0.00, 1.00, 0)
PAL['wd_stain']         = ((60, 66, 64),    'Slate',     0.00, 0.95, 0)
PAL['wd_scree_dark']    = ((70, 72, 78),    'Basalt',    0.00, 0.96, 0)


def _periodic_noise(x, z, period, seed, oct_scales):
    """Noise that repeats every `period` in x (so x=0 and x=period match), several octaves.
    Built from two angle channels of x wrapped on a circle + a free z term."""
    ang = 2 * math.pi * x / period
    cx, sx = math.cos(ang), math.sin(ang)
    total, amp_sum = 0.0, 0.0
    for k, (fr, amp) in enumerate(oct_scales):
        # circle radius grows with octave so higher octaves are busier but still periodic in x
        r = 1.0 + k * 0.9
        p = Vector((cx * r * fr + seed * 3.1, sx * r * fr + seed * 1.7, z * fr + seed * 0.5))
        total += amp * N.noise(p)
        amp_sum += amp
    return total / amp_sum


def _front_panel(W, D, H, seed, strata_h, bands, ledges, warp, name_key, slope_top=0.0):
    """Build one tiling cliff panel as a solid prism whose -Y front face is displaced.
    Returns the bmesh object (not finalized). z=0 base is flat.
    strata_h: thickness of each quantised stratum. bands: list of z where a bigger step sits.
    ledges: list of (z_center, depth) horizontal shelves. warp: amplitude of front displacement."""
    nx, nz = 60, 72
    bm = bmesh.new()
    rnd = random.Random(seed)
    oct_scales = [(1.0, 1.0), (2.0, 0.5), (4.0, 0.28), (8.0, 0.15)]
    hd = D / 2
    # per-stratum constant inward offset: makes each bed a real terrace with a lip, not a stripe.
    nlay = int(H / strata_h) + 2
    lay_off = []
    for L in range(nlay):
        base = ((L * 131 + seed) % 7) / 6.0            # 0..1
        lay_off.append(base * (warp * 1.4))            # how far this bed is recessed

    def surf_y(x, z):
        """Front y (more negative = further toward the viewer / protruding)."""
        n = _periodic_noise(x + W / 2, z, W, seed, oct_scales)
        L = int(z / strata_h)
        # within-bed parameter 0..1; a bed rounds out near its top edge forming an overhanging lip
        fz = (z - L * strata_h) / strata_h
        off = lay_off[min(L, nlay - 1)]
        lip = 1.1 * math.sin(math.pi * min(1.0, fz)) * (0.4 + 0.6 * ((L + seed) % 2))   # protruding shelf lip
        # ledges: a strong flat shelf (big recess just under zc, protruding lip at zc)
        ledge = 0.0
        for (zc, dp) in ledges:
            ledge += dp * 2.4 * math.exp(-((z - (zc + 1.0)) / 1.3) ** 2)   # recess above shelf
            lip += dp * 1.2 * math.exp(-((z - zc) / 0.9) ** 2)             # shelf front edge
        band = 0.0
        for zb in bands:
            band += 2.2 * math.exp(-((z - zb) / 1.0) ** 2)                 # deep horizontal groove
        lean = (z / H) * (2.2 + slope_top)
        y = -hd + warp * (0.6 + 0.5 * n) + off - lip + ledge + band + lean
        # vertical crack grooves cut inward
        cr = _periodic_noise((x + W / 2), z * 0.28, W, seed + 11, [(3.0, 1.0), (6.0, 0.5)])
        if cr > 0.70:
            y += 2.0 * (cr - 0.70)
        # fine roughness so faces are never perfectly coplanar
        y += 0.35 * _periodic_noise((x + W / 2) * 1.0, z * 1.3, W, seed + 23, [(6.0, 1.0), (12.0, 0.5)])
        return max(-hd - warp * 1.6, min(hd - 0.5, y))

    # front surface grid verts, indexed [iz][ix]
    front = []
    for iz in range(nz + 1):
        z = H * iz / nz
        row = [bm.verts.new((-W / 2 + W * ix / nx, surf_y(-W / 2 + W * ix / nx, z), z)) for ix in range(nx + 1)]
        front.append(row)
    # back wall (flat), top, bottom, sides
    backy = D / 2
    back = []
    for iz in range(nz + 1):
        z = H * iz / nz
        back.append([bm.verts.new((-W / 2 + W * ix / nx, backy, z)) for ix in range(nx + 1)])
    # front faces
    for iz in range(nz):
        for ix in range(nx):
            bm.faces.new((front[iz][ix], front[iz][ix + 1], front[iz + 1][ix + 1], front[iz + 1][ix]))
    # back faces (reversed)
    for iz in range(nz):
        for ix in range(nx):
            bm.faces.new((back[iz][ix + 1], back[iz][ix], back[iz + 1][ix], back[iz + 1][ix + 1]))
    # left / right side walls (use identical front edge profiles -> seamless tiling)
    for iz in range(nz):
        bm.faces.new((front[iz][0], front[iz + 1][0], back[iz + 1][0], back[iz][0]))
        bm.faces.new((back[iz][nx], back[iz + 1][nx], front[iz + 1][nx], front[iz][nx]))
    # bottom (flat z=0) and top
    for ix in range(nx):
        bm.faces.new((front[0][ix], back[0][ix], back[0][ix + 1], front[0][ix + 1]))
        bm.faces.new((front[nz][ix + 1], back[nz][ix + 1], back[nz][ix], front[nz][ix]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj_from_bm(name_key + '_body', bm, name_key + '_base')
    return o


def _paint_panel(o, seed, keyset, snow=False, snow_line=0.62, moss=False, stain=False, H=60.0):
    """Assign per-face material from height, up-slope and noise. keyset = dict with
    base, dark, light, cap-materials. Adds material slots as needed."""
    me = o.data
    # ensure all needed material slots present
    needed = [keyset[k] for k in keyset]
    present = [m.name.split('|')[0] for m in me.materials]
    for k in needed:
        if k not in present:
            me.materials.append(mat(k))
            present.append(k)
    idx = {m.name.split('|')[0]: i for i, m in enumerate(me.materials)}
    bm = bmesh.new(); bm.from_mesh(me)
    rot = o.rotation_euler.to_matrix()
    off = Vector((seed * 4.3, seed * 2.9, 0))
    for f in bm.faces:
        c = f.calc_center_median()
        nz_ = (rot @ f.normal).z
        ny = (rot @ f.normal).y
        t = c.z / H
        band = N.noise(c * 0.22 + off)
        # clean bedded strata: colour is constant within a bed, varies bed to bed (low-freq only)
        lay = int(c.z / 3.2)
        sel = (lay * 3 + seed) % 3
        pick = (keyset['dark'], keyset['base'], keyset['light'])[sel]
        if band > 0.5:                       # occasional whole-bed tone shift
            pick = keyset['light'] if sel != 2 else keyset['base']
        # moss only on genuinely up-facing shelf tops, low-to-mid height
        if moss and nz_ > 0.7 and t < 0.55 and band > -0.1:
            pick = keyset.get('moss', pick)
        # vertical trickle stain on steep front faces
        if stain and ny < -0.4 and nz_ < 0.3:
            cr = N.noise(Vector((c.x * 0.5 + off.x, 0, c.z * 0.12)))
            if cr > 0.45:
                pick = keyset.get('stain', pick)
        # snow: a clear white cap only on upward faces above the snow line (ledge tops + crown)
        if snow and nz_ > 0.55 and t > snow_line + 0.1 * band:
            pick = keyset.get('snow', pick)
        f.material_index = idx.get(pick, idx[keyset['base']])
    bm.to_mesh(me); bm.free()
    me.update()
    return o


def _scree(seed, W, keys, n=14, mossy=False):
    rnd = random.Random(seed + 500)
    for i in range(n):
        x = rnd.uniform(-W / 2 + 2, W / 2 - 2)
        y = -11 - rnd.uniform(0.0, 5.0)
        r = rnd.uniform(1.2, 3.2)
        o = rock(nm('scr'), r, (x, y, r * 0.3), rnd.choice(keys), seed=seed + i,
                 scale=(1.3, 1.0, 0.62), subdiv=2, amp=0.34)
    # a few on the lowest ledge too
    for i in range(5):
        x = rnd.uniform(-W / 2 + 4, W / 2 - 4)
        r = rnd.uniform(0.9, 1.8)
        rock(nm('scr2'), r, (x, -8.5, r * 0.3), rnd.choice(keys), seed=seed + 50 + i,
             scale=(1.2, 1.0, 0.6), subdiv=2, amp=0.3)


def _tuft_on_ledges(seed, W, ledges, color='wd_moss', n=6):
    """Small grass tufts only on ledges (shallow fans of blades)."""
    import bmesh as _bm
    rnd = random.Random(seed + 900)
    from kitlib import tube
    for i in range(n):
        zc = rnd.choice(ledges)[0]
        x = rnd.uniform(-W / 2 + 4, W / 2 - 4)
        y = -12.5
        for b in range(5):
            a = rnd.uniform(0, 6.28)
            h = rnd.uniform(0.8, 1.6)
            lean = 0.5
            tube(nm('gt'), [(x, y, zc), (x + math.cos(a) * lean * 0.4, y + math.sin(a) * lean * 0.4, zc + h * 0.6),
                            (x + math.cos(a) * lean, y + math.sin(a) * lean, zc + h)],
                 0.07, color, res=4, taper=[1, 0.6, 0.04], ures=2)


# ------------------------------------------------------------------ builders
def _granite_panel(seed, bands, ledges, name):
    reset()
    H = 60.0
    PAL[name + '_base'] = PAL['wd_granite']
    o = _front_panel(80.0, 28.0, H, seed, strata_h=3.4, bands=bands, ledges=ledges, warp=4.2, name_key=name)
    _paint_panel(o, seed, {'base': 'wd_granite', 'dark': 'wd_granite_dark', 'light': 'wd_granite_light',
                           'snow': 'wd_snow', 'moss': 'wd_moss'}, snow=True, snow_line=0.6, moss=True, H=H)
    _scree(seed, 80.0, ('wd_granite', 'wd_granite_dark', 'wd_scree_grey'))
    _tuft_on_ledges(seed, 80.0, ledges, 'wd_moss', n=5)
    return finalize(name, smooth_angle=30)


def rock_face_01():
    """Pale grey granite, broad strata, two wide ledges, snow dusting on ledges and crown."""
    return _granite_panel(1301, bands=[22, 40], ledges=[(16, 2.2), (34, 2.6)], name='rock_face_01')

def rock_face_02():
    """Granite with a deep mid cleft and a single high ledge; busier cracks."""
    return _granite_panel(1302, bands=[14, 30, 46], ledges=[(26, 3.0)], name='rock_face_02')

def rock_face_03():
    """Granite with three stacked ledges and a leaning crown."""
    return _granite_panel(1303, bands=[18, 36], ledges=[(12, 1.8), (24, 2.2), (42, 2.6)], name='rock_face_03')

def rock_face_04():
    """Granite buttressed face, few big bands, snow heavy on top."""
    return _granite_panel(1304, bands=[26, 44], ledges=[(20, 2.8)], name='rock_face_04')


def _sandstone_panel(seed, bands, ledges, name):
    reset()
    H = 58.0
    PAL[name + '_base'] = PAL['wd_sandstone']
    o = _front_panel(80.0, 28.0, H, seed, strata_h=2.6, bands=bands, ledges=ledges, warp=3.4, name_key=name)
    _paint_sandstone(o, seed, H)
    _scree(seed, 80.0, ('wd_sandstone', 'wd_sandstone_dk', 'wd_scree_sand'))
    _tuft_on_ledges(seed, 80.0, ledges, 'wd_moss', n=3)
    return finalize(name, smooth_angle=30)


def _paint_sandstone(o, seed, H):
    me = o.data
    for k in ('wd_sandstone', 'wd_sandstone_dk', 'wd_sandstone_lt', 'wd_sand_band'):
        if k not in [m.name.split('|')[0] for m in me.materials]:
            me.materials.append(mat(k))
    idx = {m.name.split('|')[0]: i for i, m in enumerate(me.materials)}
    bm = bmesh.new(); bm.from_mesh(me)
    off = Vector((seed * 2.1, seed * 3.3, 0))
    for f in bm.faces:
        c = f.calc_center_median()
        band = N.noise(c * 0.2 + off)
        # strong horizontal banding: pick colour from z in regular stripes
        stripe = math.floor(c.z / 1.8) % 4
        pick = ('wd_sandstone_dk', 'wd_sandstone', 'wd_sand_band', 'wd_sandstone_lt')[stripe]
        if band > 0.45:
            pick = 'wd_sandstone_lt'
        f.material_index = idx[pick]
    bm.to_mesh(me); bm.free(); me.update()
    return o


def rock_face_05():
    """Warm brown sandstone, strong even horizontal banding, one wide ledge."""
    return _sandstone_panel(1305, bands=[20, 38], ledges=[(28, 2.4)], name='rock_face_05')

def rock_face_06():
    """Sandstone with a recessed mid band and two ledges, fluted front."""
    return _sandstone_panel(1306, bands=[16, 32, 48], ledges=[(14, 1.8), (36, 2.2)], name='rock_face_06')

def rock_face_07():
    """Sandstone, thick alternating bands, deep single shelf near the top."""
    return _sandstone_panel(1307, bands=[24, 42], ledges=[(44, 3.0)], name='rock_face_07')


def _basalt_panel(seed, bands, ledges, name):
    reset()
    H = 60.0
    PAL[name + '_base'] = PAL['wd_basalt']
    o = _front_panel(80.0, 28.0, H, seed, strata_h=4.2, bands=bands, ledges=ledges, warp=4.6, name_key=name)
    _paint_panel(o, seed, {'base': 'wd_basalt', 'dark': 'wd_basalt_dark', 'light': 'wd_slate',
                           'moss': 'wd_moss', 'stain': 'wd_stain'}, snow=False, moss=True, stain=True, H=H)
    _scree(seed, 80.0, ('wd_basalt', 'wd_basalt_dark', 'wd_scree_dark'))
    _tuft_on_ledges(seed, 80.0, ledges, 'wd_moss', n=7)
    return finalize(name, smooth_angle=30)


def rock_face_08():
    """Dark basalt, columnar look, moss low down and a vertical trickle stain."""
    return _basalt_panel(1308, bands=[18, 34, 48], ledges=[(22, 2.2)], name='rock_face_08')

def rock_face_09():
    """Basalt/slate with two broad ledges, heavy moss, wet stains."""
    return _basalt_panel(1309, bands=[26, 44], ledges=[(16, 2.4), (36, 2.6)], name='rock_face_09')

def rock_face_10():
    """Basalt crag, jagged crown, deep central cleft, moss and stain."""
    return _basalt_panel(1310, bands=[14, 30, 46], ledges=[(28, 3.0)], name='rock_face_10')


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

BATCHES = {'e13': ('v4_terrain', BATCH_E13)}
