"""v4_wx1_rockwalls - FIX worker wx1. Rebuild the rock WALLS that the reviewer rejected.

E13_01..10 rock_face  -> v4_terrain  (was a loose-cube rubble wall with gaps, white/grey
                         two-tone and stray green blocks). Rebuilt as ONE solid continuous
                         faceted cliff panel (reuse the praised _front_panel from v4_wd_cliffs,
                         the same method as R06_01 canyon wall and the coastal cliffs), with
                         horizontal strata ledges + vertical cracks, uniform stone tone per
                         look, snow ONLY as a colour on gentle upper faces, and a mandatory
                         despeckle pass. No moss / green blocks anywhere.
E14_01..04 icelake_rim_wall -> v4_alpine  (was a noisy speckled/spiky striped surface).
                         Rebuilt with the same front-panel method at 60x25x30: pale blue-grey
                         rock, white snow on gentle upper faces, ICE as one or two blue bands
                         by rule (no painted vertical streaks, no thin spikes, no speckle).

Both side edge profiles come from _front_panel's periodic-x displacement, so panels tile
sideways. New palette keys use the wx1_ prefix. Edits no shared file; imports helpers from
v4_wd_cliffs. Rock face <= 40k tris.
"""
import math, random, bmesh
from mathutils import Vector, noise as N
from kitlib import reset, finalize, PAL, mat
# the praised tiling solid-prism panel + its scree/tuft helpers
from v4_wd_cliffs import _front_panel, _scree

# ------------------------------------------------------------------ palette (wx1_ prefixed)
# granite family (E13_01-04) - cool grey, three slope tones + snow colour
PAL['wx1_granite_dark']  = ((92, 96, 104),   'Rock',    0.00, 0.95, 0)
PAL['wx1_granite_mid']   = ((120, 124, 132), 'Rock',    0.00, 0.94, 0)
PAL['wx1_granite_light'] = ((142, 146, 154), 'Rock',    0.00, 0.92, 0)
PAL['wx1_snow']          = ((224, 228, 234), 'Snow',    0.00, 0.74, 0)
# sandstone / badlands family (E13_05-07) - warm tan
PAL['wx1_sand_dark']     = ((150, 110, 72),  'Sandstone', 0.00, 0.92, 0)
PAL['wx1_sand_mid']      = ((188, 144, 98),  'Sandstone', 0.00, 0.90, 0)
PAL['wx1_sand_light']    = ((214, 176, 128), 'Sandstone', 0.00, 0.88, 0)
PAL['wx1_sand_scree']    = ((168, 128, 86),  'Sandstone', 0.00, 0.95, 0)
PAL['wx1_sand_red']      = ((162, 92, 60),   'Sandstone', 0.00, 0.92, 0)   # red-brown bed
PAL['wx1_sand_umber']    = ((118, 78, 52),   'Sandstone', 0.00, 0.94, 0)   # dark umber bed
PAL['wx1_sand_crack']    = ((104, 70, 46),   'Sandstone', 0.00, 0.95, 0)   # shadowed vertical crack
# slate family (E13_08-10) - dark blue-grey
PAL['wx1_slate_dark']    = ((64, 68, 76),    'Slate',   0.00, 0.94, 0)
PAL['wx1_slate_mid']     = ((92, 98, 108),   'Slate',   0.00, 0.92, 0)
PAL['wx1_slate_light']   = ((116, 122, 132), 'Slate',   0.00, 0.90, 0)
PAL['wx1_slate_scree']   = ((78, 82, 90),    'Slate',   0.00, 0.96, 0)
# ice-lake rim family (E14) - pale blue-grey rock + ice bands
PAL['wx1_rimrock_dark']  = ((84, 96, 110),   'Rock',    0.00, 0.90, 0)
PAL['wx1_rimrock_mid']   = ((116, 130, 144),  'Rock',   0.00, 0.88, 0)
PAL['wx1_rimrock_light'] = ((144, 158, 172),  'Rock',   0.00, 0.86, 0)
PAL['wx1_ice_band']      = ((118, 176, 212),  'Ice',    0.00, 0.18, 0)
PAL['wx1_ice_pale']      = ((170, 210, 232),  'Ice',    0.00, 0.18, 0)
PAL['wx1_rim_snow']      = ((222, 228, 234),  'Snow',   0.00, 0.74, 0)
PAL['wx1_rim_scree']     = ((104, 116, 128),  'Rock',   0.00, 0.94, 0)


# ================================================================== colouring (rule-based, uniform)
def _paint_rock(o, seed, H, keys, snow_key=None, snow_line=0.65, snow_amt=1.0):
    """Uniform faceted-rock colouring. keys = (dark, mid, light).
    Tone comes from SLOPE (steep=dark, gentle=light) plus one low-frequency tone shift - never
    a half-and-half two-tone or per-face speckle. Snow (if snow_key) only on gentle up-facing
    faces above the snow line, gated by a low-freq field so it forms continuous caps, not specks.
    NO moss / green anywhere."""
    dark, midk, light = keys
    me = o.data
    cols = [dark, midk, light] + ([snow_key] if snow_key else [])
    present = [m.name.split('|')[0] for m in me.materials]
    for k in cols:
        if k not in present:
            me.materials.append(mat(k)); present.append(k)
    idx = {m.name.split('|')[0]: i for i, m in enumerate(me.materials)}
    rot = o.rotation_euler.to_matrix()
    off = Vector((seed * 4.3, seed * 2.9, seed * 1.3))
    bm = bmesh.new(); bm.from_mesh(me)
    for f in bm.faces:
        c = f.calc_center_median()
        n = rot @ f.normal
        up = n.z                                   # 1 = flat-up, 0 = vertical, <0 = overhang
        t = c.z / H
        # slope decides the base tone: steep -> dark, medium -> mid, gentle -> light.
        # Low-FREQUENCY tone field (big patches) so beds read smooth, not pixel-like rectangles.
        g = N.noise(Vector((c.x * 0.018, 0.0, c.z * 0.02)) + off * 0.2)
        slope = up + 0.14 * g
        if slope < 0.15:
            key = dark
        elif slope < 0.62:
            key = midk
        else:
            key = light
        # SNOW: ONE continuous crown band. The snow line is a smooth undulation of x ONLY, so
        # every face in a given x-column flips at the same height -> no dashes. All faces above
        # it (risers included, bar deep overhangs) are snow, giving a single clean cap.
        if snow_key:
            wave = 0.04 * math.sin(c.x * 0.12 + seed) + 0.03 * N.noise(Vector((c.x * 0.03, seed, 0.0)))
            if t > (snow_line + wave) and up > -0.25:
                key = snow_key
        f.material_index = idx[key]
    bm.to_mesh(me); bm.free(); me.update()
    return o


def _paint_sandstone(o, seed, H, keys, scree_unused=None):
    """Badlands/sandstone: warm red-brown bedded strata - most beds tan, a few darker red/umber
    beds for geology, plus shadowed vertical cracks - so it reads as layered sandstone, not
    uniform wooden planks. Bedding is low-frequency (smooth beds, no pixel speckle)."""
    me = o.data
    cols = ['wx1_sand_umber', 'wx1_sand_dark', 'wx1_sand_mid', 'wx1_sand_light',
            'wx1_sand_red', 'wx1_sand_crack']
    present = [m.name.split('|')[0] for m in me.materials]
    for k in cols:
        if k not in present:
            me.materials.append(mat(k)); present.append(k)
    idx = {m.name.split('|')[0]: i for i, m in enumerate(me.materials)}
    rng = random.Random(seed)
    # assign each ~4-stud bed a tone up front: mostly tans, a few red/umber accent beds
    nbed = int(H / 4.0) + 2
    bedkey = []
    for b in range(nbed):
        r = rng.random()
        if r < 0.16:
            bedkey.append('wx1_sand_umber')
        elif r < 0.40:
            bedkey.append('wx1_sand_red')
        elif r < 0.68:
            bedkey.append('wx1_sand_mid')
        elif r < 0.86:
            bedkey.append('wx1_sand_light')
        else:
            bedkey.append('wx1_sand_dark')
    off = Vector((seed * 2.1, seed * 3.3, 0))
    bm = bmesh.new(); bm.from_mesh(me)
    for f in bm.faces:
        c = f.calc_center_median()
        b = int((c.z + 1.6 * N.noise(Vector((c.x * 0.05, 0, c.z * 0.04)) + off)) / 4.0)
        key = bedkey[max(0, min(nbed - 1, b))]
        # shadowed vertical cracks: a few narrow columns darken (erosion joints)
        crack = N.noise(Vector((c.x * 0.22 + seed, 0.0, 0.0)))
        if crack > 0.55 and f.normal.y < -0.2:
            key = 'wx1_sand_crack'
        f.material_index = idx[key]
    bm.to_mesh(me); bm.free(); me.update()
    return o


def _paint_rim(o, seed, H, snow_amt, ice_bands):
    """Ice-lake rim wall: pale blue-grey rock by slope, white snow on gentle upper faces, and
    ICE as one or two blue horizontal bands (by z-rule, perturbed), never painted vertical
    streaks. ice_bands = list of (z_center, half_height)."""
    me = o.data
    cols = ['wx1_rimrock_dark', 'wx1_rimrock_mid', 'wx1_rimrock_light',
            'wx1_rim_snow', 'wx1_ice_band', 'wx1_ice_pale']
    present = [m.name.split('|')[0] for m in me.materials]
    for k in cols:
        if k not in present:
            me.materials.append(mat(k)); present.append(k)
    idx = {m.name.split('|')[0]: i for i, m in enumerate(me.materials)}
    rot = o.rotation_euler.to_matrix()
    off = Vector((seed * 3.7, seed * 2.1, seed * 1.1))
    bm = bmesh.new(); bm.from_mesh(me)
    for f in bm.faces:
        c = f.calc_center_median()
        n = rot @ f.normal
        up = n.z
        t = c.z / H
        g = N.noise(Vector((c.x * 0.02, 0.0, c.z * 0.03)) + off * 0.2)   # big smooth patches
        # base rock: MID dominates; light only on the most gentle faces, dark on steep/overhang.
        slope = up + 0.14 * g
        if slope < 0.2:
            key = 'wx1_rimrock_dark'
        elif slope < 0.72:
            key = 'wx1_rimrock_mid'
        else:
            key = 'wx1_rimrock_light'
        # ICE: one or two clean horizontal bands (all faces inside the perturbed band), pale on
        # the up-facing part of the band, deeper blue on the steep part - reads as a frozen seam.
        for (zc, hh) in ice_bands:
            if abs((c.z + 1.0 * g) - zc) < hh:
                key = 'wx1_ice_pale' if up > 0.4 else 'wx1_ice_band'
        # SNOW: ONE continuous crown band - snow line undulates with x ONLY so no dashed edge.
        if snow_amt > 0 and up > -0.25:
            wave = 0.04 * math.sin(c.x * 0.16 + seed) + 0.03 * N.noise(Vector((c.x * 0.04, seed, 0.0)))
            if t > (0.80 - 0.05 * snow_amt + wave):
                key = 'wx1_rim_snow'
        f.material_index = idx[key]
    bm.to_mesh(me); bm.free(); me.update()
    return o


def _smooth_snow_edge(o, snow_key, passes=2):
    """Smooth ONLY the lower edge of the snow cap: a boundary face (one that has BOTH snow and
    non-snow edge-neighbours) flips to whichever its neighbours mostly are. This erases single-
    face steps so the snow line reads as a gently wavy edge. Touches nothing away from the edge."""
    me = o.data
    names = [m.name.split('|')[0] for m in me.materials]
    if snow_key not in names:
        return o
    si = names.index(snow_key)
    for _ in range(passes):
        bm = bmesh.new(); bm.from_mesh(me)
        bm.faces.ensure_lookup_table()
        flips = []
        for f in bm.faces:
            snow_n = non_n = 0
            non_key = {}
            for e in f.edges:
                for nf in e.link_faces:
                    if nf is f:
                        continue
                    if nf.material_index == si:
                        snow_n += 1
                    else:
                        non_n += 1
                        non_key[nf.material_index] = non_key.get(nf.material_index, 0) + 1
            if snow_n == 0 and non_n == 0:
                continue
            on_edge = snow_n > 0 and non_n > 0
            if not on_edge:
                continue
            if f.material_index == si:
                # a snow boundary face: demote to the majority rock neighbour if rock dominates
                if non_n > snow_n and non_key:
                    flips.append((f.index, max(non_key.items(), key=lambda kv: kv[1])[0]))
            else:
                # a rock boundary face: promote to snow if snow neighbours dominate
                if snow_n > non_n:
                    flips.append((f.index, si))
        for fi, mi in flips:
            bm.faces[fi].material_index = mi
        bm.to_mesh(me); bm.free(); me.update()
        if not flips:
            break
    return o


def _despeckle(o, passes=2):
    """Mandatory: any face whose colour appears on NONE of its edge neighbours takes the most
    common neighbour colour. Removes isolated specks (green blocks, white dots, stray flecks)."""
    me = o.data
    for _ in range(passes):
        bm = bmesh.new(); bm.from_mesh(me)
        bm.faces.ensure_lookup_table()
        changes = []
        for f in bm.faces:
            neigh = {}
            mine = f.material_index
            shared = False
            for e in f.edges:
                for nf in e.link_faces:
                    if nf is f:
                        continue
                    neigh[nf.material_index] = neigh.get(nf.material_index, 0) + 1
                    if nf.material_index == mine:
                        shared = True
            if not shared and neigh:
                best = max(neigh.items(), key=lambda kv: kv[1])[0]
                changes.append((f.index, best))
        for fi, mi in changes:
            bm.faces[fi].material_index = mi
        bm.to_mesh(me); bm.free(); me.update()
        if not changes:
            break
    return o


def _cap_colors(o, keep, base_idx=0):
    """Ensure <= `keep` colour keys per piece: any material slot used by too few faces is folded
    into the dominant slot. Guards the 'at most 5-6 colour keys' QA rule and kills rare specks
    the despeckle missed."""
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    counts = {}
    for f in bm.faces:
        counts[f.material_index] = counts.get(f.material_index, 0) + 1
    ordered = sorted(counts.items(), key=lambda kv: -kv[1])
    allowed = set(i for i, _ in ordered[:keep])
    dom = ordered[0][0] if ordered else 0
    if len(ordered) > keep:
        for f in bm.faces:
            if f.material_index not in allowed:
                # fold to nearest allowed by count (dominant)
                f.material_index = dom
    bm.to_mesh(me); bm.free(); me.update()
    return o


def _strip_nonrock(o, allowed_keys):
    """Hard guard against stray specks (e.g. a green moss/Grass face leaking from a shared
    helper): any face whose material key is NOT in allowed_keys is remapped to the dominant
    allowed key. Runs across the whole mesh, so it also catches a single isolated island face
    that _despeckle (edge-neighbour only) cannot reach."""
    me = o.data
    names = [m.name.split('|')[0] for m in me.materials]
    allow_idx = {i for i, nm_ in enumerate(names) if nm_ in allowed_keys}
    if not allow_idx:
        return o
    bm = bmesh.new(); bm.from_mesh(me)
    counts = {}
    for f in bm.faces:
        if f.material_index in allow_idx:
            counts[f.material_index] = counts.get(f.material_index, 0) + 1
    dom = max(counts.items(), key=lambda kv: kv[1])[0] if counts else next(iter(allow_idx))
    for f in bm.faces:
        if f.material_index not in allow_idx:
            f.material_index = dom
    bm.to_mesh(me); bm.free(); me.update()
    return o


# ================================================================== E13 rock faces
def _rock_wall(seed, name, look, bands, ledges, snow_line=0.65, snow_amt=1.0):
    """One solid tiling rock cliff panel, ~83w x 36d x 64h. look in granite|sandstone|slate.
    Gentle displacement + smooth_angle 26 (as R06_01/coastal cliffs that read well) so the
    front reads as a continuous stratified cliff, not stacked plates. No separate scree
    boulders (those read as the 'loose blocks with gaps' defect) - the panel is self-contained."""
    reset()
    W, D, H = 83.0, 36.0, 64.0
    if look == 'granite':
        keys = ('wx1_granite_dark', 'wx1_granite_mid', 'wx1_granite_light')
        allowed = set(keys) | {'wx1_snow'}
        strata_h, warp = 4.4, 2.9
    elif look == 'sandstone':
        keys = ('wx1_sand_dark', 'wx1_sand_mid', 'wx1_sand_light')
        allowed = {'wx1_sand_dark', 'wx1_sand_mid', 'wx1_sand_light',
                   'wx1_sand_red', 'wx1_sand_umber', 'wx1_sand_crack'}
        strata_h, warp = 3.4, 2.5
    else:  # slate
        keys = ('wx1_slate_dark', 'wx1_slate_mid', 'wx1_slate_light')
        allowed = set(keys) | {'wx1_snow'}
        strata_h, warp = 4.2, 2.8
    PAL[name + '_base'] = PAL[keys[1]]
    o = _front_panel(W, D, H, seed, strata_h=strata_h, bands=bands, ledges=ledges,
                     warp=warp, name_key=name)
    if look == 'sandstone':
        _paint_sandstone(o, seed, H, keys)
    else:
        _paint_rock(o, seed, H, keys, snow_key='wx1_snow', snow_line=snow_line, snow_amt=snow_amt)
    _despeckle(o, passes=2)
    _strip_nonrock(o, allowed)
    if look != 'sandstone':
        _smooth_snow_edge(o, 'wx1_snow', passes=2)
    return finalize(name, smooth_angle=26)


# granite 01-04, snow as a clean crown cap (snowline = top fraction, varies per sibling)
def rock_face_01():
    """E13_01: pale granite, broad strata, two low ledges, thin snow crown."""
    return _rock_wall(1301, 'E13_01_rock_face_01', 'granite',
                      bands=[24, 44], ledges=[(16, 2.2), (36, 2.6)], snow_line=0.82, snow_amt=0.7)

def rock_face_02():
    """E13_02: granite, deep mid cleft, one high ledge, busier cracks, a little more snow."""
    return _rock_wall(1302, 'E13_02_rock_face_02', 'granite',
                      bands=[16, 32, 50], ledges=[(28, 3.0)], snow_line=0.78, snow_amt=0.9)

def rock_face_03():
    """E13_03: granite, three stacked ledges, higher snow line (barely any snow)."""
    return _rock_wall(1303, 'E13_03_rock_face_03', 'granite',
                      bands=[20, 40], ledges=[(12, 1.8), (26, 2.2), (46, 2.6)], snow_line=0.86, snow_amt=0.6)

def rock_face_04():
    """E13_04: granite buttress, few big bands, deeper snow cap (lower snow line)."""
    return _rock_wall(1304, 'E13_04_rock_face_04', 'granite',
                      bands=[28, 48], ledges=[(22, 2.8)], snow_line=0.74, snow_amt=1.0)

# sandstone / badlands 05-07, warm tan, no snow
def rock_face_05():
    """E13_05: warm sandstone, even bedding, one wide ledge."""
    return _rock_wall(1305, 'E13_05_rock_face_05', 'sandstone',
                      bands=[22, 42], ledges=[(30, 2.4)])

def rock_face_06():
    """E13_06: badlands tan, recessed mid band, two ledges, fluted front."""
    return _rock_wall(1306, 'E13_06_rock_face_06', 'sandstone',
                      bands=[18, 34, 52], ledges=[(16, 1.8), (38, 2.2)])

def rock_face_07():
    """E13_07: sandstone, thick beds, deep single shelf near the top."""
    return _rock_wall(1307, 'E13_07_rock_face_07', 'sandstone',
                      bands=[26, 46], ledges=[(46, 3.0)])

# slate 08-10, dark blue-grey, light snow only on top ledges
def rock_face_08():
    """E13_08: dark slate, columnar look, three bands, snow only on the crown."""
    return _rock_wall(1308, 'E13_08_rock_face_08', 'slate',
                      bands=[20, 36, 52], ledges=[(24, 2.2)], snow_line=0.80, snow_amt=0.4)

def rock_face_09():
    """E13_09: slate, two broad ledges, high snow line."""
    return _rock_wall(1309, 'E13_09_rock_face_09', 'slate',
                      bands=[28, 48], ledges=[(18, 2.4), (38, 2.6)], snow_line=0.78, snow_amt=0.4)

def rock_face_10():
    """E13_10: slate crag, jagged crown, deep central cleft, light snow dusting."""
    return _rock_wall(1310, 'E13_10_rock_face_10', 'slate',
                      bands=[16, 32, 50], ledges=[(30, 3.0)], snow_line=0.76, snow_amt=0.5)


# ================================================================== E14 ice-lake rim walls (60x25x30)
def _rim_wall(seed, name, bands, ledges, ice_bands, snow_amt=0.9):
    reset()
    W, D, H = 60.0, 25.0, 30.0
    PAL[name + '_base'] = PAL['wx1_rimrock_mid']
    o = _front_panel(W, D, H, seed, strata_h=3.0, bands=bands, ledges=ledges,
                     warp=2.2, name_key=name)
    _paint_rim(o, seed, H, snow_amt=snow_amt, ice_bands=ice_bands)
    _despeckle(o, passes=2)
    _strip_nonrock(o, {'wx1_rimrock_dark', 'wx1_rimrock_mid', 'wx1_rimrock_light',
                       'wx1_rim_snow', 'wx1_ice_band', 'wx1_ice_pale'})
    _smooth_snow_edge(o, 'wx1_rim_snow', passes=2)
    return finalize(name, smooth_angle=26)


def rim_wall_01():
    """E14_01: pale blue-grey rock, one low ice band, snow on upper ledges."""
    return _rim_wall(1401, 'E14_01_icelake_rim_wall_01',
                     bands=[10, 20], ledges=[(14, 2.0)], ice_bands=[(8.0, 2.6)], snow_amt=0.8)

def rim_wall_02():
    """E14_02: rim wall, two ice bands low and mid, snow cap."""
    return _rim_wall(1402, 'E14_02_icelake_rim_wall_02',
                     bands=[8, 18, 26], ledges=[(12, 1.8), (22, 2.0)], ice_bands=[(7.0, 2.4), (17.0, 2.0)], snow_amt=1.0)

def rim_wall_03():
    """E14_03: rim wall, single broad ice band, deep snow ledges."""
    return _rim_wall(1403, 'E14_03_icelake_rim_wall_03',
                     bands=[12, 22], ledges=[(16, 2.4)], ice_bands=[(9.0, 3.0)], snow_amt=1.2)

def rim_wall_04():
    """E14_04: rim wall, one high ice band, lighter snow."""
    return _rim_wall(1404, 'E14_04_icelake_rim_wall_04',
                     bands=[10, 20, 26], ledges=[(14, 2.0), (24, 2.0)], ice_bands=[(15.0, 2.4)], snow_amt=0.6)


# ================================================================== batches
_V13 = (0.0, -1.0, 0.22)
_V14 = (0.25, -1.1, 0.30)
BATCHES = {
    'proto':  ('v4_terrain', [('E13_01_rock_face_01', rock_face_01, _V13)]),
    'proto14': ('v4_alpine', [('E14_02_icelake_rim_wall_02', rim_wall_02, _V14)]),
    'e13': ('v4_terrain', [
        ('E13_01_rock_face_01', rock_face_01, _V13),
        ('E13_02_rock_face_02', rock_face_02, _V13),
        ('E13_03_rock_face_03', rock_face_03, _V13),
        ('E13_04_rock_face_04', rock_face_04, _V13),
        ('E13_05_rock_face_05', rock_face_05, _V13),
        ('E13_06_rock_face_06', rock_face_06, _V13),
        ('E13_07_rock_face_07', rock_face_07, _V13),
        ('E13_08_rock_face_08', rock_face_08, _V13),
        ('E13_09_rock_face_09', rock_face_09, _V13),
        ('E13_10_rock_face_10', rock_face_10, _V13),
    ]),
    'e14': ('v4_alpine', [
        ('E14_01_icelake_rim_wall_01', rim_wall_01, _V14),
        ('E14_02_icelake_rim_wall_02', rim_wall_02, _V14),
        ('E14_03_icelake_rim_wall_03', rim_wall_03, _V14),
        ('E14_04_icelake_rim_wall_04', rim_wall_04, _V14),
    ]),
}
