"""v4_wx2_facet - FIX worker wx2. Solid FACETED rock the classic low-poly way.

Repairs (reviewer MAJOR/REDO/MINOR):
  R02_01..04 snow_peak  - were cube/cairn piles -> solid jagged snow mountains, four silhouettes.
  F07_01..08 rock_formation - were smooth cones with square camo patches -> faceted spires,
                               stacks and arches, ONE tone family per piece, colour by slope/height.
  R01_01/03 islet (MINOR) + R01_04 islet (REDO, exploded) -> single steep sea-stack shell,
                               one grass top + the existing tree tops, no detached part.

Method (FIX_COMMON.md FACET METHOD): ONE closed bmesh shell per piece, flat shading
(finalize smooth_angle<=12). A revolved lattice (ring per height), every vertex jittered in its
plane, radius pushed by a large-scale profile + ridged noise + ridge spurs. Colour BY RULE
(snow on gentle high up-faces, 3 rock tones by slope, moss low), then DESPECKLE twice. A QA line
prints islands / floating / specks so the mechanical checks are visible.

Never edits shared files. New palette keys use the wx2_ prefix (grey snow-rock reused where the
existing wd2_peak_* keys already fit, to stay in one tone family). Headless runner only; no live
Blender, no Studio.
"""
import math, random, bmesh
from mathutils import Vector, noise as N
from kitlib import reset, finalize, PAL, _obj_from_bm, _link, mat, cyl
from nature import blob
from v4_elf import nm
import bpy

PI = math.pi

# ------------------------------------------------------------------ palette (wx2_ prefix; one tone family per rock)
for k, v in {
    # grey granite snow-mountain family
    'wx2_rock_dk':   ((74, 78, 86),    'Rock', 0.00, 0.95, 0),
    'wx2_rock':      ((110, 114, 122), 'Rock', 0.00, 0.94, 0),
    'wx2_rock_lt':   ((150, 154, 162), 'Rock', 0.00, 0.92, 0),
    'wx2_snow':      ((240, 244, 250), 'Snow', 0.00, 0.66, 0),
    'wx2_snow_sh':   ((206, 216, 230), 'Snow', 0.00, 0.70, 0),   # faint blue snow shadow for relief
    'wx2_ice':       ((196, 220, 236), 'Ice',  0.00, 0.22, 0),
    # warm coastal rock family (spires / sea stacks / arches)
    'wx2_tan_dk':    ((104, 94, 78),   'Rock', 0.00, 0.95, 0),
    'wx2_tan':       ((146, 134, 112), 'Rock', 0.00, 0.94, 0),
    'wx2_tan_lt':    ((182, 170, 146), 'Rock', 0.00, 0.92, 0),
    'wx2_kelp':      ((60, 66, 50),    'Grass', 0.00, 1.00, 0),   # dark wet foot
    'wx2_moss':      ((92, 116, 58),   'Grass', 0.00, 1.00, 0),
    # islet rock + grass + mini trees
    'wx2_isle_dk':   ((96, 90, 80),    'Rock',  0.00, 0.95, 0),
    'wx2_isle':      ((134, 126, 112), 'Rock',  0.00, 0.94, 0),
    'wx2_isle_lt':   ((168, 160, 144), 'Rock',  0.00, 0.92, 0),
    'wx2_grass':     ((96, 134, 62),   'Grass', 0.00, 1.00, 0),
    'wx2_grass_dk':  ((74, 110, 50),   'Grass', 0.00, 1.00, 0),
    'wx2_dirt':      ((110, 88, 62),   'Ground', 0.00, 1.00, 0),
    'wx2_trunk':     ((96, 70, 46),    'Wood', 0.00, 0.90, 0),
    'wx2_pine':      ((46, 92, 58),    'LeafyGrass', 0.00, 0.90, 0),
    'wx2_pine_dk':   ((34, 72, 48),    'LeafyGrass', 0.00, 0.90, 0),
}.items():
    PAL[k] = v


# ================================================================== noise
def _fbm(p, seed, octaves=2, lac=2.0, gain=0.5):
    off = Vector((seed * 2.13, seed * 5.71, seed * 1.37))
    f, a, tot, amp = 1.0, 1.0, 0.0, 0.0
    for _ in range(octaves):
        tot += a * N.noise(p * f + off)
        amp += a
        f *= lac
        a *= gain
    return tot / amp


def _ridged(p, seed, octaves=2):
    """1 - |noise|, a couple of octaves -> sharp ridge lines (FIX_COMMON displacement term)."""
    off = Vector((seed * 1.7, seed * 3.1, seed * 0.9))
    f, a, tot, amp = 1.0, 1.0, 0.0, 0.0
    for _ in range(octaves):
        tot += a * (1.0 - abs(N.noise(p * f + off)))
        amp += a
        f *= 2.0
        a *= 0.5
    return tot / amp


# ================================================================== core faceted shell
def _facet_shell(profile, seed, H, Rmax, name, nseg=15, nz=24, jitter=0.33,
                 ridge_amp=0.09, spurs=None, flat_base=True, random_diag=True):
    """Build ONE closed low-poly shell as a revolved lattice.
      profile(t)   -> (radius, z) base silhouette (t in 0..1 up the height)
      spurs        -> list of (angle, width_rad, strength) ridge spurs added to the radius
      jitter       -> each vertex nudged in its own plane by up to this fraction of the cell size
      ridge_amp    -> ridged-noise displacement as a fraction of H
    Returns the object (single key); colour it afterwards with _paint_rules."""
    rnd = random.Random(seed)
    bm = bmesh.new()
    rings = []
    for iz in range(nz + 1):
        t = iz / nz
        r, z = profile(t)
        if r < 0.25:
            rings.append([bm.verts.new((0, 0, z))])
            continue
        ring = []
        for ia in range(nseg):
            a = 2 * PI * ia / nseg
            # spur: widen R near each spur angle, strongest low on the mountain
            rr = r
            if spurs:
                for (sa, sw, ss) in spurs:
                    da = (a - sa + PI) % (2 * PI) - PI
                    rr += r * ss * math.exp(-(da / sw) ** 2) * (1 - t) ** 0.6
            cx, cy = math.cos(a), math.sin(a)
            # ridged-noise displacement on the radius (sharp vertical ribs) + large profile wobble
            p = Vector((cx * rr, cy * rr, z))
            rib = (_ridged(p * 0.07, seed, 2) - 0.5) * ridge_amp * H
            lowf = _fbm(p * 0.03, seed + 4, 2) * ridge_amp * H * 0.7
            rr = max(0.3, rr + rib + lowf)
            # in-plane jitter: shift angle and height within the cell so facets are irregular
            cell_a = 2 * PI / nseg * rr
            cell_z = H / nz
            ja = rnd.uniform(-jitter, jitter) * (cell_a / max(rr, 0.5))
            jz = rnd.uniform(-jitter, jitter) * cell_z
            aa = a + ja
            vx = math.cos(aa) * rr + rnd.uniform(-jitter, jitter) * cell_a * 0.15
            vy = math.sin(aa) * rr + rnd.uniform(-jitter, jitter) * cell_a * 0.15
            ring.append(bm.verts.new((vx, vy, z + jz)))
        rings.append(ring)
    # bridge rings with quads, triangulated with alternating diagonals (done by triangulate op later)
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
    # ALWAYS close the TOP ring too, so nothing is hollow / no black interior shows from above.
    # A multi-vert top ring gets a fan to its centroid (a slightly domed broken-stone cap);
    # a single-apex top is already closed by the bridging above.
    top = rings[-1]
    if len(top) > 2:
        cz = sum(v.co.z for v in top) / len(top) + (H / nz) * 0.4
        cx0 = sum(v.co.x for v in top) / len(top)
        cy0 = sum(v.co.y for v in top) / len(top)
        apex = bm.verts.new((cx0, cy0, cz))
        n = len(top)
        for i in range(n):
            bm.faces.new((top[i], top[(i + 1) % n], apex))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    # triangulate with a mix of diagonals so facets look fractured, not gridded
    bmesh.ops.triangulate(bm, faces=bm.faces,
                          quad_method='ALTERNATE' if random_diag else 'BEAUTY')
    return _obj_from_bm(name + '_body', bm, 'wx2_rock')


def _paint_rules(o, seed, H, rules, despeckle_keys=None):
    """Colour each face by the first matching rule(center, up, t, patch). Then DESPECKLE twice:
    a face whose colour none of its edge-neighbours share takes the commonest neighbour colour."""
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
        patch = _fbm(Vector((c.x, c.y, c.z)) * 0.08 + off, seed + 5, 2)
        for k, pred in rules:
            if pred(c, up, t, patch):
                f.material_index = idx[k]; break
    # despeckle twice
    for _ in range(2):
        changes = []
        for f in bm.faces:
            neigh = {}
            for e in f.edges:
                for nf in e.link_faces:
                    if nf is not f:
                        neigh[nf.material_index] = neigh.get(nf.material_index, 0) + 1
            if neigh and f.material_index not in neigh:
                changes.append((f, max(neigh, key=neigh.get)))
        for f, mi in changes:
            f.material_index = mi
    bm.to_mesh(me); bm.free(); me.update()
    return o


# ================================================================== QA floating / speck check
def qa_check(obj_name, label):
    """Print QA <label> islands=N floating=N specks=N for the finished object (best effort)."""
    o = bpy.data.objects.get(obj_name)
    if not o or o.type != 'MESH':
        print("QA %s islands=? floating=? specks=? (no object)" % label); return
    bm = bmesh.new(); bm.from_mesh(o.data)
    # connected islands by vert
    seen = set(); islands = []
    vid = {v: i for i, v in enumerate(bm.verts)}
    for v in bm.verts:
        if vid[v] in seen:
            continue
        stack = [v]; comp = set()
        while stack:
            w = stack.pop()
            if vid[w] in comp:
                continue
            comp.add(vid[w]); seen.add(vid[w])
            for e in w.link_edges:
                ov = e.other_vert(w)
                if vid[ov] not in comp:
                    stack.append(ov)
        islands.append(comp)
    # bounding boxes per island
    boxes = []
    for comp in islands:
        verts = [bm.verts[i] for i in comp] if False else [v for v in bm.verts if vid[v] in comp]
        xs = [v.co.x for v in verts]; ys = [v.co.y for v in verts]; zs = [v.co.z for v in verts]
        boxes.append((min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))

    def overlap(a, b, tol=0.2):
        return (a[0] - tol <= b[1] and b[0] - tol <= a[1] and
                a[2] - tol <= b[3] and b[2] - tol <= a[3] and
                a[4] - tol <= b[5] and b[4] - tol <= a[5])
    floating = 0
    for i, bi in enumerate(boxes):
        if len(boxes) == 1:
            break
        if not any(j != i and overlap(bi, bj) for j, bj in enumerate(boxes)):
            floating += 1
    # specks: face whose colour no edge-neighbour shares
    specks = 0
    for f in bm.faces:
        nb = set()
        for e in f.edges:
            for nf in e.link_faces:
                if nf is not f:
                    nb.add(nf.material_index)
        if nb and f.material_index not in nb:
            specks += 1
    bm.free()
    print("QA %s islands=%d floating=%d specks=%d" % (label, len(islands), floating, specks))


# ================================================================== mini pine (overlaps grass cap)
def _mini_pine(x, y, z, h, seed):
    rnd = random.Random(seed)
    cyl(nm('tr'), max(0.42, h * 0.07), h * 0.34, loc=(x, y, z - 0.4), key='wx2_trunk', verts=6)
    for i in range(3):
        tt = i / 3
        r = max(0.9, h * 0.26 * (1 - tt))
        cyl(nm('pc'), r, h * 0.34, loc=(x, y, z + h * (0.18 + 0.24 * i)),
            key=rnd.choice(('wx2_pine', 'wx2_pine_dk')), verts=7, r2=max(0.3, r * 0.18))


def _grass_cap(cx, cy, ztop, r, seed):
    """Dirt rim + a single grass dome surface (one blob) sitting ON the rock top."""
    cyl(nm('rim'), r, 1.0, loc=(cx, cy, ztop - 0.5), key='wx2_dirt', verts=18)
    return blob(nm('gtop'), r * 0.99, (cx, cy, ztop + 0.1), 'wx2_grass', subdiv=2, amp=0.12,
                scale=(1.0, 1.0, 0.2), seed=seed, flat_bottom=-0.2)


def _scree(seed, cx, cy, R, keys, n=12):
    from nature import rock
    rnd = random.Random(seed + 700)
    for i in range(n):
        a = rnd.uniform(0, 2 * PI); d = R * rnd.uniform(0.7, 1.0)   # overlap the base -> never floating
        r = rnd.uniform(1.2, 2.6)
        rock(nm('scr'), r, (cx + math.cos(a) * d, cy + math.sin(a) * d, r * 0.28),
             rnd.choice(keys), seed=seed + i, scale=(1.35, 1.05, 0.55), subdiv=1, amp=0.4)


# ================================================================== R02 SNOW PEAKS
def _peak_rules(H, snow_line):
    # Snow covers the upper mountain by HEIGHT (classic snow-cap). Above the ragged snow line,
    # any face that is not near-vertical-and-downward gets snow; the patch noise wobbles the
    # line so its edge zig-zags along the facets. Steep rock ridges (up<0.2) poke through bare.
    return [
        ('wx2_rock_dk', lambda c, up, t, pv: (up < 0.18 and t < snow_line + 0.25) or pv < -0.34),
        ('wx2_snow',    lambda c, up, t, pv: t > snow_line + 0.10 * pv and up > -0.1),
        ('wx2_snow_sh', lambda c, up, t, pv: t > snow_line - 0.12 + 0.10 * pv and up > 0.0),
        ('wx2_rock_lt', lambda c, up, t, pv: up > 0.5 and pv > 0.35),
        ('wx2_rock',    lambda c, up, t, pv: True),                         # bare rock low down
    ]


def _snow_peak(seed, H, Rbase, profile, snow_line, name, spurs, carve=None):
    reset()
    o = _facet_shell(profile, seed, H, Rbase, name, nseg=15, nz=26, jitter=0.34,
                     ridge_amp=0.10, spurs=spurs)
    if carve:
        me = o.data; bm = bmesh.new(); bm.from_mesh(me); carve(bm, H, seed); bm.to_mesh(me); bm.free(); me.update()
    _paint_rules(o, seed, H, _peak_rules(H, snow_line))
    _scree(seed, 0, 0, Rbase * 0.9, ('wx2_rock', 'wx2_rock_dk'), n=18)
    fo = finalize(name, smooth_angle=11)
    qa_check(fo.name, name)
    return fo


def snow_peak_01():
    """Sharp HORN: single pointed pyramid summit, steep faces, snow above a ragged line."""
    H, Rb = 165.0, 58.0
    spurs = [(0.4, 0.6, 0.18), (2.3, 0.5, 0.15), (4.3, 0.55, 0.16)]
    return _snow_peak(3511, H, Rb, lambda t: (Rb * (1 - t ** 1.0) ** 1.7 + 1.5, H * t),
                      0.40, 'snow_peak_01', spurs)


def snow_peak_02():
    """RIDGE: elongated serrated crest with several points along one axis."""
    H, Rb = 150.0, 60.0
    spurs = [(0.0, 0.7, 0.22), (PI, 0.7, 0.22), (0.5, 0.4, 0.12), (PI + 0.5, 0.4, 0.12)]

    def carve(bm, H, seed):
        for v in bm.verts:
            v.co.y *= 1.22                                  # stretch into a ridge (width stays in spec)
            if v.co.z > H * 0.45 and abs(v.co.x) < 14:
                v.co.z *= 0.82 + 0.18 * (0.5 + 0.5 * math.sin(v.co.y * 0.2 + seed))  # serrations
    return _snow_peak(3512, H, Rb, lambda t: (Rb * (1 - t ** 1.0) ** 1.45 + 2.0, H * t),
                      0.42, 'snow_peak_02', spurs, carve)


def snow_peak_03():
    """BROAD MASSIF: wide, two unequal summits sharing one base, gentler upper snowfields."""
    H, Rb = 135.0, 70.0
    spurs = [(0.3, 0.8, 0.2), (3.5, 0.8, 0.2), (1.8, 0.5, 0.12)]

    def carve(bm, H, seed):
        for v in bm.verts:
            if v.co.z > H * 0.5:
                # two horns: dip the saddle between +x and -x
                v.co.z -= 0.30 * (H - v.co.z) * math.exp(-((v.co.x) / 10.0) ** 2)
                if v.co.x > 0:
                    v.co.z *= 0.93                           # the +x horn a touch lower
    return _snow_peak(3513, H, Rb, lambda t: (Rb * (1 - t ** 1.1) ** 1.25 + 3.0, H * t),
                      0.48, 'snow_peak_03', spurs, carve)


def snow_peak_04():
    """STEEP PYRAMID with a hanging ice shelf: pale-blue ice faces on one flank (NOT a float)."""
    H, Rb = 150.0, 60.0
    spurs = [(0.6, 0.55, 0.17), (2.6, 0.5, 0.14), (4.7, 0.55, 0.16)]
    seed = 3514
    reset()
    o = _facet_shell(lambda t: (Rb * (1 - t ** 1.0) ** 1.6 + 2.0, H * t), seed, H, Rb,
                     'snow_peak_04', nseg=15, nz=26, jitter=0.33, ridge_amp=0.10, spurs=spurs)
    # ice-shelf: bulge one flank outward over a height band, then colour those faces as ice
    me = o.data; bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts:
        if 0.38 * H < v.co.z < 0.52 * H and v.co.x < 0 and v.co.y < 0:
            v.co.x -= 3.0 * math.exp(-((v.co.z - 0.45 * H) / 6.0) ** 2)
    bm.to_mesh(me); bm.free(); me.update()
    rules = [
        ('wx2_ice',     lambda c, up, t, pv: c.x < -Rb * 0.25 and c.y < 0 and 0.35 < t < 0.55),
        # rock ridges poke through the snow only where the face is steep AND sits in a dark patch
        # (coherent spurs, not alternating facets). Everything else high is snow.
        ('wx2_rock_dk', lambda c, up, t, pv: up < 0.12 and pv < -0.10 and t < 0.80),
        ('wx2_rock',    lambda c, up, t, pv: up < 0.14 and t < 0.40),
        ('wx2_snow',    lambda c, up, t, pv: t > 0.42),
        ('wx2_snow_sh', lambda c, up, t, pv: t > 0.36 and up < 0.25),
        ('wx2_rock',    lambda c, up, t, pv: True),
    ]
    _paint_rules(o, seed, H, rules)
    _scree(seed, 0, 0, Rb * 0.9, ('wx2_rock', 'wx2_rock_dk'), n=18)
    fo = finalize('snow_peak_04', smooth_angle=11)
    qa_check(fo.name, 'snow_peak_04')
    return fo


# ================================================================== R01 ISLETS (steep sea stacks)
def _islet_rules():
    return [
        ('wx2_grass',   lambda c, up, t, pv: up > 0.55 and t > 0.80),
        ('wx2_dirt',    lambda c, up, t, pv: up > 0.4 and t > 0.72),
        ('wx2_isle_dk', lambda c, up, t, pv: up < 0.32 or pv < -0.24),
        ('wx2_isle_lt', lambda c, up, t, pv: up > 0.5 and pv > 0.3),
        ('wx2_isle',    lambda c, up, t, pv: True),
    ]


def _islet(seed, H, Rbase, Rtop, ntrees, name):
    """One steep faceted sea-stack shell (undercut foot, flaring base), a single grass cap on top,
    a few mini pines overlapping the cap. No detached parts."""
    reset()
    rnd = random.Random(seed)

    def prof(t):
        z = H * t
        # steep sides: near-vertical, slight undercut at the waterline, small flat-ish top
        if t < 0.12:
            r = Rbase * (0.82 + 0.18 * (t / 0.12))        # undercut foot
        elif t > 0.86:
            r = (Rbase * 0.9) * (1 - 0.5 * (t - 0.86) / 0.14) + Rtop * 0.5
        else:
            r = Rbase * (0.9 - 0.32 * (t - 0.12))
        return (max(r, Rtop * 0.7), z)

    o = _facet_shell(prof, seed, H, Rbase, name, nseg=14, nz=22, jitter=0.33, ridge_amp=0.09)
    _paint_rules(o, seed, H, _islet_rules())
    _scree(seed, 0, 0, Rbase * 0.95, ('wx2_isle', 'wx2_isle_dk'), n=10)
    # grass cap sits on the rock top; trees overlap the cap (so they are not floating islands)
    rtop = max(Rtop, Rbase * 0.42)
    _grass_cap(0, 0, H * 0.985, rtop, seed)
    for i in range(ntrees):
        a = rnd.uniform(0, 2 * PI); d = rtop * math.sqrt(rnd.random()) * 0.78
        _mini_pine(math.cos(a) * d, math.sin(a) * d, H * 0.985 + 0.4, rnd.uniform(5.0, 7.5), seed + i)
    fo = finalize(name, smooth_angle=13)
    qa_check(fo.name, name)
    return fo


def islet_01():
    """Tall single sea stack with a small tree-topped crown (matches OK islet_02)."""
    return _islet(3501, 44.0, 18.0, 8.0, 4, 'islet_01')

def islet_03():
    """Lower, broader sea stack, a few more trees."""
    return _islet(3503, 36.0, 21.0, 10.0, 5, 'islet_03')

def islet_04():
    """Rebuilt from the exploded REDO: a single solid sea stack, grass cap, pines. No floats."""
    return _islet(3504, 40.0, 19.0, 9.0, 4, 'islet_04')


# ================================================================== F07 ROCK FORMATIONS
# spires / stacks / arches: warm tan family, colour by slope (dark steep, light gentle), moss low.
def _tan_rules(H, moss=True, kelp_foot=0.0):
    rules = [
        ('wx2_kelp',   lambda c, up, t, pv: kelp_foot > 0 and t < kelp_foot),
        ('wx2_tan_dk', lambda c, up, t, pv: up < 0.30 or pv < -0.26),
        ('wx2_tan_lt', lambda c, up, t, pv: up > 0.52 and pv > 0.22),
        ('wx2_tan',    lambda c, up, t, pv: True),
    ]
    if moss:
        rules.insert(1, ('wx2_moss', lambda c, up, t, pv: up > 0.55 and t < 0.22 and pv > 0.1))
    return rules


def _spire(seed, H, Rbase, Rtop, name, lean=0.0, split=False):
    """Slender faceted monolith: fast concave taper, strong vertical ribs, flat-shaded facets."""
    reset()

    def prof(t):
        return (Rbase * (1 - t) ** 1.4 + Rtop, H * t)
    o = _facet_shell(prof, seed, H, Rbase, name, nseg=13, nz=24, jitter=0.35, ridge_amp=0.11)
    me = o.data; bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts:
        v.co.x += lean * v.co.z * (v.co.z / H)            # lean the shaft
        if split and v.co.z > H * 0.62:                   # cleave the top into two prongs
            up = (v.co.z - H * 0.62) / (H * 0.38)
            v.co.z -= 0.55 * H * 0.38 * math.exp(-((v.co.x) / (Rtop * 1.4)) ** 2) * up
            if v.co.x > 0:
                v.co.z *= 0.9
    bm.to_mesh(me); bm.free(); me.update()
    _paint_rules(o, seed, H, _tan_rules(H, moss=False))
    _scree(seed, 0, 0, Rbase * 0.95, ('wx2_tan', 'wx2_tan_dk'), n=9)
    fo = finalize(name, smooth_angle=12)
    qa_check(fo.name, name)
    return fo


def rock_spire_01(): return _spire(3601, 48.0, 8.0, 1.4, 'rock_spire_01')
def rock_spire_02(): return _spire(3602, 42.0, 7.5, 1.5, 'rock_spire_02', lean=0.16)
def rock_spire_03(): return _spire(3603, 44.0, 9.0, 1.8, 'rock_spire_03', split=True)


def _sea_stack(seed, H, Rbase, Rtop, name, twin=False, lean=0.0, step=False):
    """Faceted sea stack: wave-cut undercut foot, real upward taper, uneven ledges, dark wet foot.
    lean  -> tilt the shaft sideways (toppling look). step -> a stacked/stepped silhouette.
    The top ring is tilted and roughened so it reads as a broken, irregular crown (not a barrel)."""
    reset()

    def prof(t):
        z = H * t
        if t < 0.15:
            r = Rbase * (0.55 + 0.45 * (t / 0.15))        # wave-cut notch at the foot
        else:
            # strong concave taper so the top is markedly narrower than the base (not a barrel)
            r = Rbase * (1 - 0.62 * ((t - 0.15) / 0.85) ** 1.2)
        if step:
            r *= 1.0 - 0.12 * (math.floor(t * 4) % 2)      # alternating stepped shoulders
        for zc, dp in ((0.42, 0.12), (0.68, 0.10)):        # irregular ledges
            r *= 1.0 - dp * math.exp(-((t - zc) / 0.06) ** 2)
        return (max(r, Rtop * 0.6), z)
    o = _facet_shell(prof, seed, H, Rbase, name, nseg=14, nz=24, jitter=0.34, ridge_amp=0.10)
    me = o.data; bm = bmesh.new(); bm.from_mesh(me)
    zmax = max(v.co.z for v in bm.verts)
    for v in bm.verts:
        v.co.x += lean * v.co.z * (v.co.z / H)             # lean the shaft
        # tilt + rough the crown so the top is a broken slanted cap, never a flat barrel lid
        if v.co.z > H * 0.82:
            up = (v.co.z - H * 0.82) / (H * 0.18)
            v.co.z += (0.12 * v.co.x + 0.08 * v.co.y) * up  # slant the top plane
    if twin:
        for v in bm.verts:
            if v.co.z > H * 0.55:
                up = (v.co.z - H * 0.55) / (H * 0.45)
                v.co.z -= 0.6 * H * 0.45 * math.exp(-((v.co.x) / (Rtop * 1.6)) ** 2) * up
                if v.co.x > 0:
                    v.co.z *= 0.82
    bm.to_mesh(me); bm.free(); me.update()
    _paint_rules(o, seed, H, _tan_rules(H, moss=False, kelp_foot=0.10))
    _scree(seed, 0, 0, Rbase * 0.95, ('wx2_tan_dk', 'wx2_kelp'), n=9)
    fo = finalize(name, smooth_angle=12)
    qa_check(fo.name, name)
    return fo


def sea_stack_01(): return _sea_stack(3604, 44.0, 16.0, 6.0, 'sea_stack_01')
def sea_stack_02(): return _sea_stack(3605, 50.0, 14.0, 5.0, 'sea_stack_02', lean=0.12)
def sea_stack_03(): return _sea_stack(3606, 40.0, 18.0, 6.0, 'sea_stack_03', twin=True, step=True)


def _arch(seed, span, H, name, pier_r, bridge=False):
    """Natural arch from a swept ring along a half-ellipse (closed shell), flared piers.
    No stray plates: everything is one swept tube welded to two pier shells."""
    reset()
    rnd = random.Random(seed)
    # two piers (faceted stubby shells)
    for sgn in (-1, 1):
        def pprof(t, sgn=sgn):
            return (pier_r * (1 - 0.18 * t), (H * 0.42) * t)
        po = _facet_shell(pprof, seed + (sgn + 1), H * 0.42, pier_r, name + ('_pier%d' % sgn),
                          nseg=11, nz=10, jitter=0.3, ridge_amp=0.08)
        me = po.data
        for v in me.vertices:
            v.co.x += sgn * span / 2
    # swept span: ring extruded along a half-ellipse arc
    steps = 18
    ring_n = 8
    tube_r = pier_r * (1.1 if bridge else 0.7)
    bm = bmesh.new()
    loops = []
    for s in range(steps + 1):
        u = s / steps
        ang = PI * u
        # centre of the arch tube on a half ellipse
        cxp = -math.cos(ang) * span / 2
        czp = (H * (0.5 if bridge else 0.95)) * math.sin(ang) + H * 0.42
        # tangent
        tx = math.sin(ang) * span / 2
        tz = (H * (0.5 if bridge else 0.95)) * math.cos(ang)
        tl = math.hypot(tx, tz) or 1.0
        tx, tz = tx / tl, tz / tl
        loop = []
        tr = tube_r * (1.25 if (u < 0.12 or u > 0.88) else 1.0)   # flared feet
        for j in range(ring_n):
            b = 2 * PI * j / ring_n
            # ring in plane perpendicular to tangent (tangent in x-z): normal n1 = (-tz,0,tx), n2 = (0,1,0)
            rr = tr * (1.0 + 0.12 * _fbm(Vector((cxp, 0, czp)) * 0.1 + Vector((b, s, seed)), seed, 2))
            ox = math.cos(b) * (-tz) * rr
            oz = math.cos(b) * (tx) * rr
            oy = math.sin(b) * rr
            loop.append(bm.verts.new((cxp + ox, oy, czp + oz)))
        loops.append(loop)
    for A, B in zip(loops, loops[1:]):
        for j in range(ring_n):
            bm.faces.new((A[j], A[(j + 1) % ring_n], B[(j + 1) % ring_n], B[j]))
    bm.faces.new(list(reversed(loops[0]))); bm.faces.new(loops[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh.ops.triangulate(bm, faces=bm.faces, quad_method='ALTERNATE')
    ao = _obj_from_bm(name + '_span', bm, 'wx2_tan')
    # colour span + piers by rule (height over full H)
    for ob in list(bpy.data.objects):
        if ob.type == 'MESH':
            _paint_rules(ob, seed, H, _tan_rules(H, moss=False))
    _scree(seed, -span / 2, 0, pier_r * 1.1, ('wx2_tan', 'wx2_tan_dk'), n=7)
    _scree(seed + 5, span / 2, 0, pier_r * 1.1, ('wx2_tan', 'wx2_tan_dk'), n=7)
    fo = finalize(name, smooth_angle=12)
    qa_check(fo.name, name)
    return fo


def natural_arch_tall():
    """F07_07: tall narrow arch, walk-under gap >= 8x10."""
    return _arch(3607, 26.0, 34.0, 'natural_arch_tall', pier_r=6.0, bridge=False)

def natural_arch_bridge():
    """F07_08: wide low arch bridge."""
    return _arch(3608, 56.0, 30.0, 'natural_arch_bridge', pier_r=9.0, bridge=True)


# ================================================================== batches (SAVED ids kept exactly)
BATCHES = {
    'r02': ('v4_terrain', [
        ('R02_01_snow_peak_01', snow_peak_01, (0.5, -1.2, 0.3)),
        ('R02_02_snow_peak_02', snow_peak_02, (0.5, -1.2, 0.3)),
        ('R02_03_snow_peak_03', snow_peak_03, (0.6, -1.1, 0.3)),
        ('R02_04_snow_peak_04', snow_peak_04, (0.6, -1.1, 0.3)),
    ]),
    'r01': ('v4_terrain', [
        ('R01_01_islet_01', islet_01, (0.6, -1.2, 0.4)),
        ('R01_03_islet_03', islet_03, (0.6, -1.2, 0.4)),
        ('R01_04_islet_04', islet_04, (0.6, -1.2, 0.4)),
    ]),
    'f07a': ('v4_terrain', [
        ('F07_01_rock_formation_01', rock_spire_01, (0.45, -1.1, 0.35)),
        ('F07_02_rock_formation_02', rock_spire_02, (0.45, -1.1, 0.35)),
        ('F07_03_rock_formation_03', rock_spire_03, (0.45, -1.1, 0.35)),
        ('F07_04_rock_formation_04', sea_stack_01, (0.45, -1.1, 0.35)),
    ]),
    'f07b': ('v4_terrain', [
        ('F07_05_rock_formation_05', sea_stack_02, (0.45, -1.1, 0.35)),
        ('F07_06_rock_formation_06', sea_stack_03, (0.45, -1.1, 0.35)),
        ('F07_07_rock_formation_07', natural_arch_tall, (0.3, -1.1, 0.25)),
        ('F07_08_rock_formation_08', natural_arch_bridge, (0.3, -1.1, 0.25)),
    ]),
}
