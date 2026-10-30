"""v4_wx5_fix - FIX worker wx5. Strata cliffs, mesas and a boulder speck/polish pass.

Repairs 16 reviewer-flagged models, all MINOR (geometry good, polish needed):
  R04_01/03, R05_01/02, R06_01/02/03, F07_09/10/11 : scattered white speck patches -> DESPECKLE
  R04_02                                            : near-black -> readable dark slate + normals check
  R03_01..04 badlands_mesa                          : loose-block gaps -> continuous faceted shell
  E15_02 boulder                                    : 108-tri flat wedge -> faceted boulder 250-500 tris

Method (never edits a shared file; copies builder bodies where a copy must change):
- Specks: the real cause is isolated bright faces that _paint_panel / _paint_sandstone / _paint_badlands
  scatter as single confetti faces. FIX_COMMON rule 6: a face whose colour is shared by NONE of its
  edge neighbours is demoted to the most common neighbour colour; repeat twice. _edge_despeckle does
  exactly this on the finished mesh, so it works regardless of which paint routine ran. The flagged
  cliffs are rebuilt by calling their original builder, then despeckled in place (material-index only,
  silhouette/size/strata untouched).
- R04_02: lighter wx5 basalt/slate keys so the dark volcanic cliff reads as dark slate, not black;
  finalize already recomputes outward normals so no inverted faces.
- R03 mesas: the chunk-pile version (v4_wd2_chunk) is what the reviewer saw; rebuild from the CONTINUOUS
  _landform shell in v4_wd2_rock (one closed mesh per mesa, strata as banded tint, no inter-block gaps).
- E15_02: a small faceted icosphere-derived boulder, flat shaded, same ~10x7x5 size class.
"""
import math, random, bmesh
import bpy
from mathutils import Vector, noise as N
from kitlib import reset, finalize, PAL, mat, _obj_from_bm

# cliff builders to re-run then despeckle
import v4_wk_rocks as WK
# continuous-shell mesa builders (FACET METHOD) + badlands paint
import v4_wd2_rock as WD2


def _safe_render_scene():
    """This host's EEVEE-Next render path crashes in embree4 (ray-traced BVH) under memory pressure.
    Turn ray tracing OFF and drop AA so the preview render never builds that BVH. Set on the scene
    (persists; kitlib._setup_render never re-enables raytracing). Called from every builder."""
    sc = bpy.context.scene
    try:
        sc.eevee.use_raytracing = False
    except Exception:
        pass
    for attr in ('taa_render_samples', 'taa_samples'):
        try:
            setattr(sc.eevee, attr, 8)
        except Exception:
            pass
    try:
        sc.eevee.use_shadows = False
    except Exception:
        pass


# ------------------------------------------------------------------ wx5 palette (lighter basalt for R04_02)
for k, v in {
    'wx5_slate':      ((104, 108, 118), 'Slate',  0.00, 0.88, 0),   # readable dark slate (was near-black basalt)
    'wx5_slate_dk':   ((78, 82, 92),    'Slate',  0.00, 0.90, 0),
    'wx5_slate_lt':   ((140, 144, 152), 'Slate',  0.00, 0.85, 0),
    'wx5_slate_stain':((70, 76, 84),    'Slate',  0.00, 0.92, 0),
    'wx5_gran':       ((128, 128, 132), 'Rock',   0.00, 0.95, 0),   # boulder
    'wx5_gran_dk':    ((96, 96, 100),   'Rock',   0.00, 0.96, 0),
    'wx5_moss':       ((96, 112, 64),   'Grass',  0.00, 1.00, 0),
}.items():
    PAL[k] = v

# Matte clones of the grey rock keys the panels use. The reviewer's "bright white square patches"
# are NOT glint: they are faces of near-white rock keys (wk_chalk srgb 214, wd_rock_light srgb 160)
# that pop against the darker beds. The clone keeps the same Roblox material but (a) roughness 0.99
# and (b) a DARKENED colour for the light keys, so no rock face reads as a white block. Foam/water on
# the waterfalls are NOT in this map, so they stay bright. _mattify() remaps a panel's slots to these.
_DARKEN = {                      # near-white rock keys -> true mid-grey replacement sRGB
    'wk_chalk':       (150, 152, 150),
    'wk_chalk_dk':    (126, 128, 126),
    'wk_chalk_band':  (138, 140, 138),
    'wd_rock_light':  (138, 140, 146),
    'wx5_slate_lt':   (124, 128, 136),
}
_MATTE = {}
for src in ('wd_rock_grey', 'wd_rock_dark', 'wd_rock_light', 'wk_chalk', 'wk_chalk_dk', 'wk_chalk_band',
            'wd_basalt', 'wd_basalt_dark', 'wd_slate', 'wd_stain', 'wd_scree_grey', 'wd_scree_dark',
            'wx5_slate', 'wx5_slate_dk', 'wx5_slate_lt', 'wx5_slate_stain'):
    if src in PAL:
        rgb, rmat, met, rough, emit = PAL[src]
        rgb = _DARKEN.get(src, rgb)
        mk = 'wx5m_' + src
        PAL[mk] = (rgb, rmat, met, 0.99, emit)
        _MATTE[src] = mk


def _mattify(o):
    """Rename each of o's material slots from a glossy grey key to its matte wx5 clone (same colour
    and Roblox material), then ZERO the specular lobe on it. The reviewer's "white square patches" on
    the dark panels (R06_03, F07_11) are specular highlights where the sun hits a flat up-facing facet
    (confirmed: no near-white MATERIAL exists on them); killing specular removes them. Roblox ignores
    this preview-only setting, so the exported asset is unchanged."""
    me = o.data
    for slot in me.materials:
        if slot is None:
            continue
        key = slot.name.split('|')[0]
        mk = _MATTE.get(key)
        if mk:
            nmat = mat(mk)
            i = list(me.materials).index(slot)
            me.materials[i] = nmat
            slot = nmat
        # zero specular on ANY rock material (matte clone or not) to kill the facet glint
        try:
            b = slot.node_tree.nodes.get('Principled BSDF')
            for sp in ('Specular IOR Level', 'Specular'):
                if sp in b.inputs:
                    b.inputs[sp].default_value = 0.0
            if 'Roughness' in b.inputs:
                b.inputs['Roughness'].default_value = max(b.inputs['Roughness'].default_value, 0.99)
        except Exception:
            pass
    me.update()
    return o


# ================================================================== DESPECKLE (FIX_COMMON rule 6)
def _edge_despeckle(o, passes=3, protect=(), erode_keys=(), erode_passes=3):
    """A face whose material appears on NONE of its edge neighbours takes the most common neighbour
    material. Repeat `passes` times. This removes the scattered single-face white/light specks that
    read as confetti on the strata, without touching geometry. Materials in `protect` (e.g. water,
    foam, cave-dark, kelp) are never changed and never counted as the odd-one-out to demote.

    Then, for each key in `erode_keys` (the bright 'speckle' tones), run a majority-vote erosion:
    a face of that key whose edge-neighbours are MOSTLY (>= 60%) some other non-protected colour is
    reassigned to that majority colour. Repeated `erode_passes` times this eats away small 2-4 face
    bright patches (the "speck patches") while leaving a genuine broad light bed (where most
    neighbours are also light) intact."""
    me = o.data
    prot = set(protect)
    name_of = [m.name.split('|')[0] for m in me.materials]
    prot_idx = {i for i, nm_ in enumerate(name_of) if nm_ in prot}
    erode_idx = {i for i, nm_ in enumerate(name_of) if nm_ in set(erode_keys)}

    for _ in range(passes):
        bm = bmesh.new(); bm.from_mesh(me)
        bm.faces.ensure_lookup_table()
        changes = []
        for f in bm.faces:
            if f.material_index in prot_idx:
                continue
            counts = {}
            mine = 0
            for e in f.edges:
                for nf in e.link_faces:
                    if nf is f:
                        continue
                    mi = nf.material_index
                    counts[mi] = counts.get(mi, 0) + 1
                    if mi == f.material_index:
                        mine += 1
            if counts and mine == 0:
                best = max((c for c in counts.items() if c[0] not in prot_idx),
                           key=lambda kv: kv[1], default=None)
                if best is not None:
                    changes.append((f.index, best[0]))
        if not changes:
            bm.free(); break
        for fi, mi in changes:
            bm.faces[fi].material_index = mi
        bm.to_mesh(me); bm.free()

    # erosion of bright speckle keys
    if erode_idx:
        for _ in range(erode_passes):
            bm = bmesh.new(); bm.from_mesh(me)
            bm.faces.ensure_lookup_table()
            changes = []
            for f in bm.faces:
                if f.material_index not in erode_idx:
                    continue
                counts = {}
                tot = 0
                for e in f.edges:
                    for nf in e.link_faces:
                        if nf is f:
                            continue
                        mi = nf.material_index
                        if mi in prot_idx:
                            continue
                        counts[mi] = counts.get(mi, 0) + 1
                        tot += 1
                if not tot:
                    continue
                # majority neighbour colour that is NOT this bright key
                other = max((c for c in counts.items() if c[0] not in erode_idx),
                            key=lambda kv: kv[1], default=None)
                if other is not None and other[1] >= 0.45 * tot:
                    changes.append((f.index, other[0]))
            if not changes:
                bm.free(); break
            for fi, mi in changes:
                bm.faces[fi].material_index = mi
            bm.to_mesh(me); bm.free()
    me.update()
    return o


# ================================================================== R04 / R05 / R06 / F07_09-11  (specks)
# protected materials: water / foam / dark cave / wet foot - these are meant to be isolated regions
_PROT = ('water', 'water_fx', 'foam', 'wk_cave_dark', 'wk_kelp', 'wk_wet_rock', 'wd2_ice')
# bright tones that _paint_* scatter as confetti and must be eroded off small patches
_SPECK = ('wd_rock_light', 'wd_sandstone_lt', 'wd_slate', 'wx5_slate_lt', 'wd_bl_cream', 'wk_chalk_dk')


def _collapse_light(o, bright_keys, base_key):
    """Last-resort: remap every face of a bright speckle key to the base tone. Removes all remaining
    bright flecks on a busy carved panel at the cost of a slightly flatter strata (still banded by the
    dark key). Used only on the three panels whose specks survive despeckle+erode+mattify."""
    me = o.data
    names = [m.name.split('|')[0] for m in me.materials]
    base = mat(base_key)
    if base_key not in names:
        me.materials.append(base); names.append(base_key)
    bi = names.index(base_key)
    bm = bmesh.new(); bm.from_mesh(me)
    bset = set(bright_keys)
    bidx = {i for i, n in enumerate(names) if n in bset}
    for f in bm.faces:
        if f.material_index in bidx:
            f.material_index = bi
    bm.to_mesh(me); bm.free(); me.update()
    return o


def _fix_speck(builder, collapse=None):
    def _inner():
        o = builder()                     # original builder already calls finalize()
        _edge_despeckle(o, passes=3, protect=_PROT, erode_keys=_SPECK, erode_passes=4)
        if collapse:
            _collapse_light(o, collapse[0], collapse[1])
        _mattify(o)
        _safe_render_scene()
        return o
    return _inner


sea_cliff_03            = _fix_speck(WK.sea_cliff_03)            # R04_03 sandstone + caves
waterfall_cliff_large_01= _fix_speck(WK.waterfall_cliff_large_01)  # R05_01
waterfall_cliff_large_02= _fix_speck(WK.waterfall_cliff_large_02)  # R05_02
canyon_wall_01          = _fix_speck(WK.canyon_wall_01)          # R06_01 red
canyon_wall_02          = _fix_speck(WK.canyon_wall_02)          # R06_02 limestone
canyon_wall_03          = _fix_speck(WK.canyon_wall_03)          # R06_03 basalt
coastal_cliff_01        = _fix_speck(WK.coastal_cliff_01)        # F07_09
coastal_cliff_02        = _fix_speck(WK.coastal_cliff_02)        # F07_10
coastal_cliff_03        = _fix_speck(WK.coastal_cliff_03, collapse=(('wd_rock_grey', 'wd_rock_light'), 'wd_rock_dark'))  # F07_11: mostly dark bed, demote the few light-grey patches

# R04_01 chalk: good layering, just despeckle the stray light flecks
sea_cliff_01 = _fix_speck(WK.sea_cliff_01)


# ================================================================== R04_02  (lighten near-black)
def sea_cliff_02():
    """R04_02: dark volcanic sea cliff - re-paint with readable dark SLATE tones (not near-black),
    columnar fluting kept. Copy of WK._sea_cliff basalt path with the lighter wx5 palette."""
    reset()
    seed, name, H = 402, 'sea_cliff_02', 55.0
    PAL[name + '_base'] = PAL['wx5_slate']
    o = WK._front_panel(100.0, 40.0, H, seed, strata_h=4.6, bands=[16, 32, 46],
                        ledges=[(24, 2.6)], warp=5.0, name_key=name)
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts:
        if v.co.z < 9.0 and v.co.y < 0:                 # wave-cut notch
            rec = math.exp(-((v.co.z - 3.5) / 3.0) ** 2)
            v.co.y += 3.6 * rec
        if v.co.y < 0:                                  # columnar fluting on the front
            v.co.y += 0.6 * math.sin(v.co.x * 1.1 + seed)
    bm.to_mesh(me); bm.free(); me.update()
    WK._paint_panel(o, seed, {'base': 'wx5_slate', 'dark': 'wx5_slate_dk', 'light': 'wx5_slate_lt',
                              'stain': 'wx5_slate_stain'}, snow=False, moss=False, stain=True, H=H)
    # wet foot band (readable, not black)
    for k in ('wk_wet_rock', 'wk_kelp'):
        if k not in [m.name.split('|')[0] for m in me.materials]:
            me.materials.append(mat(k))
    idx = {m.name.split('|')[0]: i for i, m in enumerate(me.materials)}
    bm = bmesh.new(); bm.from_mesh(me)
    for f in bm.faces:
        c = f.calc_center_median()
        if c.z < 3.0:
            f.material_index = idx['wk_kelp']
        elif c.z < 9.0:
            f.material_index = idx['wk_wet_rock']
    bm.to_mesh(me); bm.free(); me.update()
    WK._scree(seed, 100.0, ('wx5_slate', 'wx5_slate_dk', 'wk_wet_rock'), n=18)
    o = finalize(name, smooth_angle=30)
    _edge_despeckle(o, passes=3, protect=_PROT, erode_keys=_SPECK, erode_passes=4)
    _mattify(o)
    _safe_render_scene()
    return o


# ================================================================== R03 badlands mesas (continuous shell)
# v4_wd2_rock._mesa / _03 / _04 build ONE continuous _landform shell with banded strata, but the
# TOP RING IS LEFT OPEN - so from above you see the inner wall and it reads as a hollow pot. Fill
# every high boundary edge-loop with a flat cap in the cream band colour, then despeckle.
def _cap_mesa_tops(o, cap_key='wd2_bl_cream', z_frac=0.40, max_span_frac=2.5):
    """Fill open top boundary loops with flat faces (a rock cap). Any boundary edge whose midpoint
    is above z_frac*height is part of an open top; fill those loops with bmesh contextual-create.
    A loop whose XY span exceeds max_span_frac*height is the outer/base boundary (or a stray flap) and
    is skipped."""
    import bmesh as _bm
    me = o.data
    names = [m.name.split('|')[0] for m in me.materials]
    cap = mat(cap_key)
    if cap_key not in names:
        me.materials.append(cap); names.append(cap_key)
    ci = names.index(cap_key)
    bm = _bm.new(); bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    zmax = max((v.co.z for v in bm.verts), default=0.0)
    thr = zmax * z_frac
    # collect boundary edges high on the model, then trace them into ordered loops
    be = [e for e in bm.edges if e.is_boundary and 0.5 * (e.verts[0].co.z + e.verts[1].co.z) > thr]
    adj = {}
    eset = set(be)
    for e in be:
        for v in e.verts:
            adj.setdefault(v, []).append(e)
    loops = []
    used = set()
    for start in list(adj.keys()):
        for e0 in adj[start]:
            if e0 in used:
                continue
            loop = [start]
            used.add(e0)
            cur = e0.other_vert(start)
            prev_e = e0
            guard = 0
            while cur is not start and guard < 4000:
                loop.append(cur)
                nxt = None
                for e in adj.get(cur, []):
                    if e is not prev_e and e not in used:
                        nxt = e; break
                if nxt is None:
                    break
                used.add(nxt)
                prev_e = nxt
                cur = nxt.other_vert(cur)
                guard += 1
            if len(loop) >= 3 and cur is start:
                loops.append(loop)
    new_faces = []
    for loop in loops:
        # skip a loop that is the whole outer silhouette (spans most of the model width) - that is not
        # an open top but the base/side boundary; a real open top loop is small in XY.
        xs = [v.co.x for v in loop]; ys = [v.co.y for v in loop]
        if (max(xs) - min(xs)) > zmax * max_span_frac or (max(ys) - min(ys)) > zmax * max_span_frac:
            continue
        c = _bm.geometry  # noqa
        cx = sum(xs) / len(loop); cy = sum(ys) / len(loop)
        cz = sum(v.co.z for v in loop) / len(loop)
        ctr = bm.verts.new((cx, cy, cz + 0.3))   # slight dome so the cap is a gentle rock lid
        n = len(loop)
        for i in range(n):
            try:
                f = bm.faces.new((loop[i], loop[(i + 1) % n], ctr))
                new_faces.append(f)
            except ValueError:
                pass
    for f in new_faces:
        if f.is_valid:
            f.material_index = ci
            f.smooth = False
    # fallback: any boundary edge loop still open up top -> holes_fill it (covers a loop the
    # tracer could not close, e.g. after the notch deform), then tag the new faces as cap.
    remaining = [e for e in bm.edges if e.is_boundary and 0.5 * (e.verts[0].co.z + e.verts[1].co.z) > thr]
    if remaining:
        before = set(f for f in bm.faces)
        try:
            _bm.ops.holes_fill(bm, edges=remaining, sides=0)
        except Exception:
            pass
        for f in bm.faces:
            if f not in before and f.is_valid and f.calc_area() < zmax * zmax:
                f.material_index = ci
                f.smooth = False
    _bm.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free(); me.update()
    return o


def _fix_mesa(builder, z_frac=0.40):
    def _inner():
        o = builder()
        _cap_mesa_tops(o, z_frac=z_frac)
        _edge_despeckle(o, passes=2)
        _safe_render_scene()
        return o
    return _inner

badlands_mesa_01 = _fix_mesa(WD2.badlands_mesa_01)
badlands_mesa_02 = _fix_mesa(WD2.badlands_mesa_02)


def badlands_mesa_03():
    """R03_03 rebuilt as ONE clean banded butte with a flat cap and a straight wedge notch cut into
    one side (clean vertical walls, no torn flaps). Continuous _landform shell, cream flat cap."""
    reset()
    seed, H, Rbase = 3423, 70.0, 34.0
    import math as _m

    def rfn(t):
        z = H * t
        r = Rbase * (1 - 0.30 * t) if t < 0.86 else Rbase * (1 - 0.30 * 0.86)
        return (max(r, 10.0), z)

    o = WD2._landform(48, 40, rfn, seed, warp=1.9, strata=1.0, facet=1.1, groove=1.6, name='badlands_mesa_03')
    # clean wedge notch: push verts inside an angular sector on the +Y/-X front straight inward,
    # then flatten them to a vertical plane so the cut walls are clean (no torn flaps).
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    a0, a1 = _m.radians(200), _m.radians(250)      # ~50deg wedge on one side
    for v in bm.verts:
        ang = _m.atan2(v.co.y, v.co.x) % (2 * _m.pi)
        if a0 < ang < a1 and v.co.z > H * 0.25:
            # collapse this sector's radius onto a straight chord -> a clean V notch
            depth = 0.55 * (v.co.z - H * 0.25) / (H * 0.75)
            v.co.x *= (1.0 - depth)
            v.co.y *= (1.0 - depth)
    bm.to_mesh(me); bm.free(); me.update()
    WD2._paint_badlands(o, seed, H)
    WD2.WP._scree_skirt(seed, Rbase * 0.96, ('wd2_bl_talus', 'wd2_bl_sand'), n=16, spread=1.3, scale=(1.4, 1.0, 0.5))
    o = finalize('badlands_mesa_03', smooth_angle=26)
    _cap_mesa_tops(o, z_frac=0.55, max_span_frac=1.6)
    _edge_despeckle(o, passes=2)
    _safe_render_scene()
    return o


def badlands_mesa_04():
    o = WD2.badlands_mesa_04()
    # strip any stray pale flap: a cap face far off the main rim is a mis-trace; cap with tight guard
    _cap_mesa_tops(o, z_frac=0.78, max_span_frac=1.3)
    _edge_despeckle(o, passes=2)
    _safe_render_scene()
    return o


# ================================================================== E15_02 boulder (faceted, 250-500 tris)
def boulder_slab():
    """E15_02: a faceted angular boulder (~10x7x5 studs), flat shaded, with a couple of broken
    facets and a small patchy moss cap - reads as a real rock, not a painted wedge."""
    reset()
    seed = 1502
    rnd = random.Random(seed)
    bm = bmesh.new()
    # icosphere subdiv 3 -> 1280 tris; the exporter splits per colour + welds, landing ~250-500 tris
    bmesh.ops.create_icosphere(bm, subdivisions=3, radius=3.0)
    off = Vector((seed * 3.1, seed * 1.3, seed * 2.7))
    for v in bm.verts:
        p = v.co
        d = 0.30 * N.noise(p * 1.3 + off) + 0.16 * N.noise(p * 3.1 + off * 2)
        v.co = p * (1.0 + d)
        # squash to a low wide boulder (~10 long x 7 wide x 5 tall) and knock one shoulder flat
        v.co.x *= 1.65
        v.co.y *= 1.15
        v.co.z *= 0.85
        if v.co.z > 2.4:
            v.co.z = 2.4 + (v.co.z - 2.4) * 0.45        # slight flat-ish crown
    # sit it on the ground
    minz = min(v.co.z for v in bm.verts)
    for v in bm.verts:
        v.co.z -= minz
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj_from_bm('boulder_slab_body', bm, 'wx5_gran')
    # colour: two rock tones in broad low-freq patches + patchy moss on the up-top
    me = o.data
    for k in ('wx5_gran', 'wx5_gran_dk', 'wx5_moss'):
        if k not in [m.name.split('|')[0] for m in me.materials]:
            me.materials.append(mat(k))
    idx = {m.name.split('|')[0]: i for i, m in enumerate(me.materials)}
    bm = bmesh.new(); bm.from_mesh(me)
    hi = max(v.co.z for v in bm.verts)
    for f in bm.faces:
        c = f.calc_center_median()
        up = f.normal.z
        patch = N.noise(c * 0.35 + off)
        pick = 'wx5_gran_dk' if patch < -0.12 else 'wx5_gran'
        if up > 0.45 and c.z > hi * 0.6 and N.noise(c * 0.5 + off * 1.5) > 0.0:
            pick = 'wx5_moss'                            # patchy moss only on the up-facing crown
        f.material_index = idx[pick]
    bm.to_mesh(me); bm.free(); me.update()
    o = finalize('boulder_slab', smooth_angle=16)        # low angle -> hard faceted edges
    _edge_despeckle(o, passes=2)
    _safe_render_scene()
    return o


# ================================================================== batches
BATCHES = {
    'r04': ('v4_terrain', [
        ('R04_01_sea_cliff_01', sea_cliff_01, (0.0, -1.0, 0.2)),
        ('R04_02_sea_cliff_02', sea_cliff_02, (0.0, -1.0, 0.2)),
        ('R04_03_sea_cliff_03', sea_cliff_03, (0.0, -1.0, 0.2)),
    ]),
    'r05': ('v4_terrain', [
        ('R05_01_waterfall_cliff_large_01', waterfall_cliff_large_01, (0.3, -1.1, 0.28)),
        ('R05_02_waterfall_cliff_large_02', waterfall_cliff_large_02, (0.3, -1.1, 0.28)),
    ]),
    'r06': ('v4_terrain', [
        ('R06_01_canyon_wall_01', canyon_wall_01, (0.0, -1.0, 0.25)),
        ('R06_02_canyon_wall_02', canyon_wall_02, (0.0, -1.0, 0.25)),
        ('R06_03_canyon_wall_03', canyon_wall_03, (0.0, -1.0, 0.25)),
    ]),
    'f07c': ('v4_terrain', [
        ('F07_09_rock_formation_09', coastal_cliff_01, (0.0, -1.0, 0.2)),
        ('F07_10_rock_formation_10', coastal_cliff_02, (0.0, -1.0, 0.2)),
        ('F07_11_rock_formation_11', coastal_cliff_03, (0.0, -1.0, 0.2)),
    ]),
    'r03': ('v4_terrain', [
        ('R03_01_badlands_mesa_01', badlands_mesa_01, (0.6, -1.2, 0.35)),
        ('R03_02_badlands_mesa_02', badlands_mesa_02, (0.5, -1.2, 0.3)),
        ('R03_03_badlands_mesa_03', badlands_mesa_03, (0.6, -1.2, 0.35)),
        ('R03_04_badlands_mesa_04', badlands_mesa_04, (0.6, -1.2, 0.35)),
    ]),
    'e15': ('v4_terrain', [
        ('E15_02_boulder_02', boulder_slab, (0.7, -1.1, 0.5)),
    ]),
}
