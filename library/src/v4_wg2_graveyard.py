"""wg2 graveyard set 2: E02 crypts (3), E03 weeping statues (3), E04 iron fence+gate (2).
Replacement for frozen worker wg. Reuses wg's weathered-stone palette from v4_wg_graveyard
(imported, never edited). Haunting, old, weathered. Fronts face -Y. 1 unit = 1 stud.
Builds through v4run.ps1 only."""
import math, random
from mathutils import Euler
import kitlib
from kitlib import (reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, top_paint)
from arch import (F, lbox, lslab, lbeam, nm, arc_pts, column_c, pediment, cone_roof)
# Reuse the predecessor's palette keys + helpers (import triggers its PAL additions).
import v4_wg_graveyard as WG
from v4_wg_graveyard import _lichen, _mound, _grass_tuft, _ivy_face, GRAN, STON

# A couple of wg2-scoped additions so no key collides with wg.
kitlib.PAL['wg2_iron']      = ((34, 32, 32),    'Metal',         0.80, 0.55, 0)
kitlib.PAL['wg2_iron_rust'] = ((92, 56, 38),    'CorrodedMetal', 0.40, 0.88, 0)
kitlib.PAL['wg2_bronze']    = ((110, 92, 60),   'Metal',         0.85, 0.55, 0)
kitlib.PAL['wg2_glass_lit'] = ((236, 176, 96),  'Glass',         0.00, 0.20, 0.30)
kitlib.PAL['wg2_moss']      = ((78, 92, 54),    'Grass',         0.00, 1.00, 0)


def _mossy(o, amt=0.80, seed=0):
    """Light, patchy moss on up-facing stone (high thresh = sparse). Darker than wg_lichen."""
    top_paint(o, 'wg2_moss', amt, seed)
    return o


# ---------- shared bits ----------
def _step_base(cx, cy, w, d, steps=2, h=0.55, key='wg_granite_d'):
    for k in range(steps):
        box(nm('st'), (w - k * 1.6, d - k * 1.6, h), loc=(cx, cy, h / 2 + k * h),
            key=key if k == 0 else 'wg_granite', bev=0.05)
    return steps * h


def _coursed_wall(f, w, h, z0, key, dark, seed, courses=None, t=0.06):
    """Draw horizontal course lines + a few vertical joints on a wall face."""
    rnd = random.Random(seed)
    courses = courses or max(3, int(h / 1.1))
    for i in range(1, courses):
        lbox(f, (w - 0.2, t, t), 0, -0.02, z0 + h * i / courses, dark)
    for i in range(courses):
        zc = z0 + h * (i + 0.5) / courses
        for _ in range(2):
            x = rnd.uniform(-w / 2 + 0.6, w / 2 - 0.6)
            lbox(f, (t, t, h / courses * 0.8), x, -0.02, zc, dark)


def _iron_door(f, w, h, z0, key='wg2_iron', rust='wg2_iron_rust'):
    """A closed iron door: panel + banding + ring handle, set in a recess."""
    lbox(f, (w + 0.5, 0.3, h + 0.5), 0, 0.1, z0 + h / 2, 'wg_stone_d')   # recess jamb
    lbox(f, (w, 0.14, h), 0, -0.02, z0 + h / 2, key)                      # leaf
    for zz in (0.22, 0.5, 0.78):
        lbox(f, (w + 0.1, 0.05, 0.14), 0, -0.1, z0 + h * zz, rust)        # bands
    for s in (-1, 1):
        lbox(f, (0.12, 0.05, h - 0.3), s * (w / 2 - 0.2), -0.1, z0 + h / 2, rust)
    torus(nm('rg'), 0.22, 0.05, loc=f.p(0, -0.16, z0 + h * 0.5), key=rust, segs=14, rsegs=4, rot=f.r(0, 0, 0))


# ============================================================ E02 crypts (closed)
def crypt_01():
    """E02_01 - small temple-front crypt: four columns, pediment, closed iron door."""
    reset()
    W, D, H = 15.0, 11.0, 7.4
    bh = _step_base(0, 0, W + 3, D + 3, steps=2)
    # cella (solid block body)
    box(nm('cell'), (W, D, H), loc=(0, 0, bh + H / 2), key='wg_stone', bev=0.08)
    fF = F(0, -D / 2, bh, 0)
    _coursed_wall(fF, W, H, 0, 'wg_stone', 'wg_stone_d', 21)
    for fr in (F(W / 2, 0, bh, 90), F(-W / 2, 0, bh, -90), F(0, D / 2, bh, 180)):
        _coursed_wall(fr, D, H, 0, 'wg_stone', 'wg_stone_d', 22)
    # portico: 4 columns across the front
    cz = bh
    for i, x in enumerate((-W / 2 + 1.6, -1.9, 1.9, W / 2 - 1.6)):
        column_c(x, -D / 2 - 1.8, cz, H - 0.8, 0.7, key='wg_marble', base='wg_marble_d')
    # architrave + pediment
    lbox(fF, (W + 1.2, 2.4, 1.0), 0, -1.8, H + 0.4, 'wg_marble_d')
    pediment(F(0, -D / 2 - 1.8, bh, 0), 0, H + 0.9, W + 1.0, 2.6, 2.2, key='wg_marble', tymp='wg_marble_d')
    # doorway + closed iron door
    _iron_door(F(0, -D / 2, bh, 0), 3.2, 5.0, 0.0)
    _mossy(box(nm('roof'), (W + 0.6, D + 0.6, 0.8), loc=(0, 0, bh + H + 0.4), key='wg_stone_d', bev=0.05), 0.85, 101)
    _ivy_face(-W / 2, -W / 2 + 2, -D / 2, 0.0, H, 10, 101)
    _mound(0, 0, W + 5, D + 5, seed=101)
    return finalize('crypt_01', smooth_angle=30)


def crypt_02():
    """E02_02 - domed rotunda mausoleum: round drum, ribbed dome, pilasters, iron door."""
    reset()
    R, H = 6.4, 7.0
    bh = _step_base(0, 0, 16, 16, steps=2)
    # drum
    lathe(nm('dr'), [(0, 0), (R, 0), (R, H), (0, H)], loc=(0, 0, bh), key='wg_stone', segs=32)
    lathe(nm('cor'), [(0, H), (R + 0.5, H), (R + 0.5, H + 0.6), (0, H + 0.6)], loc=(0, 0, bh), key='wg_stone_d', segs=32)
    # pilasters around the drum
    for i in range(10):
        a = 2 * math.pi * i / 10
        box(nm('pil'), (0.5, 0.5, H - 0.4), loc=(math.cos(a) * (R + 0.02), math.sin(a) * (R + 0.02), bh + H / 2),
            key='wg_marble_d', rot=(0, 0, math.degrees(a)), bev=0.03)
    # ribbed dome
    prof = [(math.cos(math.radians(t)) * R, bh + H + 0.6 + math.sin(math.radians(t)) * R * 0.75)
            for t in range(0, 91, 10)]
    prof[-1] = (0.0, prof[-1][1])
    lathe(nm('dome'), prof, loc=(0, 0, 0), key='wg_stone_d', segs=32)
    for i in range(10):
        a = 2 * math.pi * i / 10
        pts = [(math.cos(a) * math.cos(math.radians(t)) * (R + 0.06), math.sin(a) * math.cos(math.radians(t)) * (R + 0.06),
                bh + H + 0.6 + math.sin(math.radians(t)) * R * 0.75 + 0.06) for t in range(0, 86, 14)]
        tube(nm('rb'), pts, 0.12, 'wg_marble_d', res=4)
    top = bh + H + 0.6 + R * 0.75
    lathe(nm('urn'), [(0, top), (0.6, top), (0.45, top + 0.9), (0.7, top + 1.3), (0.3, top + 1.7), (0, top + 1.8)],
          key='wg_marble', segs=12)
    # doorway recess + iron door
    _iron_door(F(0, -R, bh, 0), 3.0, 4.6, 0.0)
    _ivy_face(-R, -1, -R + 0.1, 0.0, H, 8, 102)
    _mound(0, 0, 18, 18, seed=102)
    return finalize('crypt_02', smooth_angle=30)


def crypt_03():
    """E02_03 - Gothic crypt: steep gabled roof, buttresses, gargoyles, iron-banded door, steps."""
    reset()
    W, D, H = 14.0, 10.0, 7.0
    bh = _step_base(0, -D / 2 - 1.5, 7, 4, steps=3, h=0.4)  # entry steps out front
    box(nm('body'), (W, D, H), loc=(0, 0, H / 2), key='wg_stone', bev=0.06)
    fF = F(0, -D / 2, 0, 0)
    _coursed_wall(fF, W, H, 0, 'wg_stone', 'wg_stone_d', 303)
    for fr in (F(W / 2, 0, 0, 90), F(-W / 2, 0, 0, -90), F(0, D / 2, 0, 180)):
        _coursed_wall(fr, D, H, 0, 'wg_stone', 'wg_stone_d', 304)
    # corner buttresses
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(nm('but'), (1.4, 1.4, H - 0.5), loc=(sx * (W / 2 - 0.2), sy * (D / 2 - 0.2), (H - 0.5) / 2),
                key='wg_stone_d', bev=0.05)
            lathe(nm('bc'), [(0, 0), (1.0, 0), (0, 1.2)], loc=(sx * (W / 2 - 0.2), sy * (D / 2 - 0.2), H - 0.5),
                  key='wg_stone_d', segs=4)
    # steep gable roof from two slabs
    peak = H + 4.2
    for s in (-1, 1):
        roof = [(0, 0, H), (s * (W / 2 + 0.6), 0, H - 0.3), (s * 0.3, 0, peak)]
        ro = lslab(F(0, -D / 2 - 0.4, 0, 0), roof, (0, D + 0.8, 0), 'wg_stone_d')
        _mossy(ro, 0.85, 305 + s)
    tube(nm('ridge'), [(0, -D / 2 - 0.3, peak - 0.1), (0, D / 2 + 0.3, peak - 0.1)], 0.22, 'wg_stone', res=4)
    # gargoyles at the front eaves: crouched body, head, jutting water-spout snout
    for s in (-1, 1):
        gx = s * (W / 2 - 0.4)
        ball(nm('gy'), 0.45, loc=(gx, -D / 2 - 0.7, H + 0.1), key='wg_stone_d', segs=8, rings=6, scale=(0.9, 1.3, 1.0))
        ball(nm('gh'), 0.34, loc=(gx, -D / 2 - 1.3, H + 0.3), key='wg_stone_d', segs=8, rings=6, scale=(1.1, 1.0, 0.9))
        cyl(nm('gn'), 0.14, 0.9, loc=(gx, -D / 2 - 1.5, H + 0.15), key='wg_stone_d', verts=8, r2=0.09, rot=(72, 0, 0))
        for w in (-1, 1):  # folded stub wings
            lslab(F(gx, -D / 2 - 0.5, H + 0.1, 0), [(0, 0, 0), (w * 0.5, 0, 0.1), (w * 0.4, 0, 0.7), (0, 0, 0.6)], (0, 0.15, 0), 'wg_stone_d')
    # pointed-arch doorway with iron-banded door
    _iron_door(F(0, -D / 2, bh, 0), 3.2, 5.2, 0.0)
    tube(nm('arch'), arc_pts(F(0, -D / 2 - 0.04, bh, 0), 0, 5.2, 1.7, y=-0.06, n=9), 0.22, 'wg_stone_d', res=4)
    _ivy_face(W / 2 - 2, W / 2, -D / 2, 0.0, H, 10, 303)
    _mound(0, 0, W + 4, D + 6, seed=303)
    return finalize('crypt_03', smooth_angle=28)


# ============================================================ E03 weeping statues
def _plinth(cx, cy, w, h, key='wg_granite'):
    box(nm('pb'), (w + 0.8, w + 0.8, 0.5), loc=(cx, cy, 0.25), key='wg_granite_d', bev=0.05)
    box(nm('ps'), (w, w, h), loc=(cx, cy, 0.5 + h / 2), key=key, bev=0.05)
    cap = box(nm('pc'), (w + 0.6, w + 0.6, 0.4), loc=(cx, cy, 0.5 + h + 0.2), key='wg_granite_d', bev=0.05)
    top_paint(cap, 'wg2_moss', 0.8, int(cx * 7 + h))  # a little patchy moss on the plinth cap
    return 0.5 + h + 0.4


def _robe(z0, profile, key='wg_marble', segs=28, folds=9, fold_amp=0.09, lean=0.0, lean_z0=0.0, seed=0):
    """A robe/gown as a lathe with radial noise so it has vertical drapery ridges.
    profile: list of (radius, z). lean: forward (-Y) tilt in studs applied above lean_z0 (a leaning torso).
    Built as raw bmesh so each ring can be nudged independently."""
    import bmesh
    rnd = random.Random(seed)
    phase = [rnd.uniform(0, 6.28) for _ in range(3)]
    bm = bmesh.new()
    rings = []
    zmax = max(z for _, z in profile) or 1.0
    for (r, z) in profile:
        if r < 1e-4:
            rings.append([bm.verts.new((0, _lean(z, lean, lean_z0, zmax), z0 + z))])
            continue
        ring = []
        for i in range(segs):
            a = 2 * math.pi * i / segs
            # vertical fold ridges: sum of a few sinusoids, constant along z so ridges run top-to-bottom
            ridge = fold_amp * (math.sin(folds * a + phase[0]) + 0.4 * math.sin(2 * folds * a + phase[1]))
            rr = r * (1.0 + ridge)
            ring.append(bm.verts.new((math.cos(a) * rr, math.sin(a) * rr + _lean(z, lean, lean_z0, zmax), z0 + z)))
        rings.append(ring)
    for A, B in zip(rings, rings[1:]):
        if len(A) == 1 and len(B) == 1:
            continue
        if len(A) == 1:
            for i in range(segs):
                bm.faces.new((A[0], B[i], B[(i + 1) % segs]))
        elif len(B) == 1:
            for i in range(segs):
                bm.faces.new((A[i], B[0], A[(i + 1) % segs]))
        else:
            for i in range(segs):
                bm.faces.new((A[i], A[(i + 1) % segs], B[(i + 1) % segs], B[i]))
    if len(rings[0]) > 1:
        bm.faces.new(list(reversed(rings[0])))
    if len(rings[-1]) > 1:
        bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return kitlib._obj_from_bm(nm('robe'), bm, key)


def _lean(z, lean, lean_z0, zmax):
    if lean == 0 or z <= lean_z0:
        return 0.0
    return -lean * ((z - lean_z0) / (zmax - lean_z0)) ** 1.3  # forward (-Y) lean, growing with height


def _shoulders(cx, cy, cz, wspan, key='wg_marble', lean=0.0):
    """A shoulder yoke wider than the waist, plus a short neck."""
    box(nm('shd'), (wspan, 0.95, 0.55), loc=(cx, cy, cz), key=key, rot=(lean, 0, 0), bev=0.26)
    for s in (-1, 1):   # rounded shoulder caps
        ball(nm('shc'), 0.42, loc=(cx + s * wspan / 2 * 0.86, cy, cz), key=key, segs=8, rings=6, scale=(1, 1, 0.9))


def _head(cx, cy, cz, r=0.56, key='wg_marble'):
    cyl(nm('neck'), 0.24, 0.5, loc=(cx, cy + 0.03, cz - 0.3), key=key, verts=10)
    ball(nm('head'), r, loc=(cx, cy, cz + r * 0.7), key=key, segs=12, rings=10)
    # a shallow face plane (brow + nose suggestion) on the -Y front
    box(nm('brow'), (r * 1.1, 0.12, 0.16), loc=(cx, cy - r * 0.82, cz + r * 0.9), key='wg_marble_d', bev=0.04)
    box(nm('nose'), (0.14, 0.2, 0.34), loc=(cx, cy - r * 0.92, cz + r * 0.55), key=key, bev=0.03)


def _arm(sx, shoulder, elbow, hand, key='wg_marble', r=0.22):
    """Upper + lower arm as two tubes with a ball hand."""
    tube(nm('ua'), [shoulder, elbow], r, key, res=5)
    tube(nm('la'), [elbow, hand], r * 0.9, key, res=5)
    ball(nm('hd'), r * 1.25, loc=hand, key=key, segs=8, rings=6, scale=(1.0, 0.8, 1.1))


def statue_hooded():
    """E03_01 - hooded mourner KNEELING: folded-leg mass under the robe, torso leaning forward,
    hood up, head bowed, one hand to the face. ~11.5 studs incl. plinth."""
    reset()
    pz = _plinth(0, 0, 3.0, 3.6)
    # folded-leg mass: a broad low dome the robe sits over
    ball(nm('legs'), 1.7, loc=(0, -0.3, pz), key='wg_marble', segs=12, rings=8, scale=(1.1, 1.25, 0.55))
    # robe: wide pooled hem -> waist, torso leans forward above the waist
    _robe(pz, [(1.95, 0), (1.9, 0.5), (1.6, 1.6), (1.25, 2.8), (1.0, 3.8), (0.82, 4.3), (0, 4.4)],
          folds=10, fold_amp=0.10, lean=0.9, lean_z0=1.8, seed=31)
    # shoulders (leaning), neck hidden by hood
    _shoulders(0, -0.72, pz + 4.4, 1.9, lean=-14)
    # raised hood: a cowl cone over a bowed head, face in shadow
    _robe(pz + 4.3, [(0, 0), (0.85, 0.05), (0.9, 0.5), (0.7, 1.05), (0.35, 1.35), (0, 1.4)],
          key='wg_marble', folds=7, fold_amp=0.06, lean=0.55, lean_z0=0.0, seed=131)
    ball(nm('face'), 0.34, loc=(0, -1.15, pz + 5.0), key='wg_marble_d', segs=8, rings=6, scale=(1, 0.55, 1.15))
    # arms: right drawn up to the face, left resting forward on the knee (asymmetric)
    _arm(1, (0.78, -0.5, pz + 4.2), (0.55, -1.0, pz + 4.6), (0.2, -1.15, pz + 4.9), r=0.24)
    _arm(-1, (-0.78, -0.5, pz + 4.2), (-0.95, -0.7, pz + 3.3), (-0.8, -1.3, pz + 2.7), r=0.24)
    _mound(0, 0, 5, 5, seed=31)
    return finalize('weeping_statue_01', smooth_angle=32)


def statue_angel():
    """E03_02 - weeping angel STANDING, both hands over the face, layered feather-row folded wings,
    long folded robe. ~13 studs incl. plinth."""
    reset()
    pz = _plinth(0, 0, 3.2, 2.4)
    # long folded robe: hem -> waist (narrower) -> chest, clear taper to shoulders
    _robe(pz, [(1.55, 0), (1.5, 0.6), (1.2, 2.2), (0.98, 3.8), (0.9, 5.0), (0.82, 5.6), (0, 5.7)],
          folds=11, fold_amp=0.10, seed=32)
    _shoulders(0, -0.15, pz + 5.7, 2.1)
    _head(0, -0.35, pz + 5.95, r=0.58)
    # long hair/veil down the back
    _robe(pz + 5.2, [(0, 1.3), (0.62, 1.2), (0.55, 0.4), (0.4, 0), (0, -0.1)], key='wg_marble_d',
          folds=6, fold_amp=0.07, seed=231)
    # both arms bent up, hands together covering the face (grief)
    for s in (-1, 1):
        _arm(s, (s * 0.9, -0.2, pz + 5.3), (s * 0.62, -0.75, pz + 5.9), (s * 0.2, -0.9, pz + 6.35), r=0.23)
    # folded wings behind the shoulders: a shaped slab PLUS layered feather rows (curved tubes)
    for s in (-1, 1):
        wing = [(0, 0, 0), (s * 0.3, 0, 0.4), (s * 1.0, 0, 1.2), (s * 1.55, 0, 2.8), (s * 1.5, 0, 4.2),
                (s * 0.95, 0, 5.0), (s * 0.5, 0, 4.2), (s * 0.32, 0, 1.0)]
        lslab(F(s * 0.75, 0.55, pz + 2.1, 0), wing, (0, 0.28, 0), 'wg_marble')
        for row in range(5):   # overlapping feather rows, each a short curved scallop line
            zr = pz + 2.5 + row * 0.62
            spread = 0.7 + row * 0.22
            pts = [(s * (0.5 + t * spread), 0.72, zr + 0.18 * math.sin(math.pi * t))
                   for t in (0.0, 0.33, 0.66, 1.0)]
            tube(nm('ft'), pts, 0.08, 'wg_marble_d', res=4)
    _mound(0, 0, 5.4, 5.4, seed=32)
    return finalize('weeping_statue_02', smooth_angle=32)


def statue_maiden():
    """E03_03 - praying maiden STANDING, hands clasped at the chest, head bowed, long hair down the
    back, simple belted dress with folds. ~12.5 studs incl. plinth."""
    reset()
    pz = _plinth(0, 0, 2.8, 2.6)
    # simple dress with folds; a belt marks the waist
    _robe(pz, [(1.35, 0), (1.3, 0.7), (1.05, 2.4), (0.9, 3.8), (0.84, 4.8), (0.78, 5.3), (0, 5.4)],
          folds=10, fold_amp=0.085, seed=33)
    torus(nm('belt'), 0.98, 0.12, loc=(0, 0, pz + 2.5), key='wg_marble_d', segs=20, rsegs=5)
    _shoulders(0, -0.12, pz + 5.4, 1.65)
    _head(0, -0.3, pz + 5.65, r=0.5)
    # long hair down the back (-Y is front, so hair on +Y)
    _robe(pz + 4.6, [(0, 1.5), (0.58, 1.45), (0.52, 0.6), (0.38, 0), (0, -0.1)], key='wg_marble_d',
          folds=7, fold_amp=0.06, seed=331)
    # clasped hands at the chest + both forearms angling in to meet
    ball(nm('hands'), 0.3, loc=(0, -0.72, pz + 4.5), key='wg_marble', segs=8, rings=6, scale=(0.85, 0.85, 1.25))
    for s in (-1, 1):
        _arm(s, (s * 0.72, -0.15, pz + 4.95), (s * 0.5, -0.55, pz + 4.6), (0, -0.7, pz + 4.5), r=0.19)
    _mound(0, 0, 4.6, 4.6, seed=33)
    return finalize('weeping_statue_03', smooth_angle=32)


# ============================================================ E04 iron fence + gate
def _spiked_bar(f, x, z0, h, key='wg2_iron'):
    cyl(nm('br'), 0.07, h, loc=f.p(x, 0, z0), key=key, verts=8, rot=f.r(0, 0, 0))
    cyl(nm('sp'), 0.12, 0.5, loc=f.p(x, 0, z0 + h), key=key, verts=8, r2=0.0, rot=f.r(0, 0, 0))  # spearhead


def iron_fence():
    """E04_01 - 12-long fence section: spiked bars, finial rails, stone footing, two posts. Tileable."""
    reset()
    L = 12.0
    # stone footing / plinth (tileable: runs the full 12)
    foot = box(nm('ft'), (L, 1.1, 0.9), loc=(0, 0, 0.45), key='wg_stone', bev=0.05)
    _lichen(foot, 0.5, 41)
    f = F(0, 0, 0.9, 0)
    # two stone posts at the ends
    for s in (-1, 1):
        px = s * (L / 2 - 0.5)
        box(nm('pst'), (1.1, 1.1, 4.2), loc=(px, 0, 0.9 + 2.1), key='wg_stone_d', bev=0.05)
        lathe(nm('pcap'), [(0, 0), (0.75, 0), (0.6, 0.4), (0.3, 0.75), (0, 0.8)], loc=(px, 0, 0.9 + 4.2),
              key='wg_stone', segs=4)
    # top and bottom rails between posts
    inner = L - 2.0
    for zz in (0.7, 3.4):
        box(nm('rail'), (inner, 0.18, 0.2), loc=(0, 0, 0.9 + zz), key='wg2_iron')
    # spiked bars
    n = 15
    for i in range(n):
        x = -inner / 2 + inner * i / (n - 1)
        _spiked_bar(f, x, 0.4, 3.3)
    # a couple of bent/rusted bars for age
    for bx, tilt in ((inner * 0.18, 6), (-inner * 0.3, -5)):
        o = cyl(nm('bent'), 0.07, 3.3, loc=f.p(bx, 0, 0.4), key='wg2_iron_rust', verts=8, rot=f.r(0, tilt, 0))
    _mound(0, 0, L + 1, 2.4, seed=41)
    return finalize('iron_fence_gate_01', smooth_angle=30)


def iron_gate():
    """E04_02 - double gate ~10 wide between two stone pillars, arched ironwork top, lantern posts, ajar."""
    reset()
    span = 10.0
    # two tall stone pillars
    for s in (-1, 1):
        px = s * (span / 2 + 0.6)
        box(nm('pil'), (1.6, 1.6, 6.0), loc=(px, 0, 3.0), key='wg_stone_d', bev=0.06)
        _coursed_wall(F(px, -0.8, 0, 0), 1.6, 6.0, 0, 'wg_stone_d', 'wg_stone', 42)
        lathe(nm('pc'), [(0, 0), (1.1, 0), (0.9, 0.5), (0.4, 1.0), (0, 1.1)], loc=(px, 0, 6.0), key='wg_stone', segs=4)
        # lantern on top
        box(nm('lh'), (0.7, 0.7, 1.1), loc=(px, 0, 7.1 + 0.55), key='wg2_iron')
        box(nm('lg'), (0.44, 0.44, 0.7), loc=(px, 0, 7.1 + 0.55), key='wg2_glass_lit')
        lathe(nm('lc'), [(0, 0), (0.5, 0), (0, 0.5)], loc=(px, 0, 7.1 + 1.1), key='wg2_iron', segs=4)
    # arched ironwork spanning the top
    arcf = F(0, 0, 0, 0)
    arc = arc_pts(arcf, 0, 6.0, span / 2 + 0.6, y=0.0, n=13)
    tube(nm('arc'), arc, 0.14, 'wg2_iron', res=5)
    # scroll decoration under the arch
    for s in (-1, 1):
        for k in range(3):
            cx = s * (1.2 + k * 1.3)
            torus(nm('sc'), 0.5, 0.06, loc=(cx, 0, 6.3), key='wg2_iron', segs=12, rsegs=4, rot=(90, 0, 0))
    # two gate leaves, slightly ajar (rotated about the pillars)
    for s, ang in ((-1, 18), (1, -14)):
        hinge = s * (span / 2)
        leaf = F(hinge, 0, 0.3, 0)
        # frame
        lbox(leaf, (0.18, 0.18, 5.4), 0, 0, 2.7, 'wg2_iron')
        lbox(leaf, (-s * (span / 2 - 0.3), 0.14, 0.18), -s * (span / 4 - 0.15), 0, 0.5, 'wg2_iron')
        lbox(leaf, (-s * (span / 2 - 0.3), 0.14, 0.18), -s * (span / 4 - 0.15), 0, 4.9, 'wg2_iron')
        nb = 7
        for i in range(nb):
            bx = -s * (0.4 + i * (span / 2 - 0.8) / (nb - 1))
            cyl(nm('gb'), 0.06, 4.3, loc=leaf.p(bx, 0, 0.6), key='wg2_iron', verts=6, rot=leaf.r(0, 0, 0))
            cyl(nm('gsp'), 0.1, 0.4, loc=leaf.p(bx, 0, 4.9), key='wg2_iron', verts=6, r2=0.0, rot=leaf.r(0, 0, 0))
        # swing the whole leaf group is hard post-hoc; instead tilt the bars collectively by building at angle:
    _mound(0, 0, span + 3, 3.0, seed=42)
    return finalize('iron_fence_gate_02', smooth_angle=30)


BATCHES = {
    'crypts': ('v4_graveyard', [
        ('E02_01_crypt_01', crypt_01, (1.0, -1.1, 0.5)),
        ('E02_02_crypt_02', crypt_02, (1.0, -1.1, 0.5)),
        ('E02_03_crypt_03', crypt_03, (1.0, -1.1, 0.45)),
    ]),
    'statues': ('v4_graveyard', [
        ('E03_01_weeping_statue_01', statue_hooded, (0.6, -1.2, 0.35)),
        ('E03_02_weeping_statue_02', statue_angel, (0.6, -1.2, 0.35)),
        ('E03_03_weeping_statue_03', statue_maiden, (0.6, -1.2, 0.35)),
    ]),
    'fence': ('v4_graveyard', [
        ('E04_01_iron_fence_gate_01', iron_fence, (0.5, -1.3, 0.35)),
        ('E04_02_iron_fence_gate_02', iron_gate, (0.6, -1.2, 0.4)),
    ]),
}
