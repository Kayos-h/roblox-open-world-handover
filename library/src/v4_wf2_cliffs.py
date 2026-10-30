"""v4_wf2_cliffs - E14 ice-lake rim walls (worker wf2, replacing wf).
A 30-stud cliff step on the ice-lake rim. Four 60w x 25d x 30h panels, front toward -Y,
left/right edge profiles identical so panels tile sideways.
NOT stacked horizontal strata with square colour patches: a finely subdivided front face displaced by
fbm + voronoi facets, vertical fracture grooves, irregular ledges and a few overhangs. Colour by geology
(smooth height gradient, darker on steep faces, low-frequency patches <=4 colours; snow/ice only on up-facing
ledges). Scree + snow at the base. New keys use the wf2c_ prefix.
"""
import math, random
import bmesh
from mathutils import Vector, noise
import kitlib
from kitlib import reset, finalize, box, cyl, ball, _obj_from_bm, mat
from arch import nm
from nature import rock, blob

P = kitlib.PAL
# four looks share these geology keys (reuse base rock/ice/snow; add dark-rock + seam keys)
P.setdefault('wf2c_rock_dark',  ((64, 66, 72),   'Basalt',  0.0, 0.95, 0))
P.setdefault('wf2c_rock_mid',   ((96, 98, 104),  'Rock',    0.0, 0.95, 0))
P.setdefault('wf2c_rock_pale',  ((150, 150, 156),'Rock',    0.0, 0.92, 0))
P.setdefault('wf2c_slate',      ((88, 94, 104),  'Slate',   0.0, 0.92, 0))
P.setdefault('wf2c_slate_pale', ((132, 140, 150),'Slate',   0.0, 0.90, 0))
P.setdefault('wf2c_ice_seam',   ((120, 176, 214),'Ice',     0.0, 0.16, 0))
P.setdefault('wf2c_ice_glaze',  ((176, 212, 232),'Ice',     0.0, 0.18, 0))
P.setdefault('wf2c_ice_pale',   ((206, 230, 242),'Ice',     0.0, 0.18, 0))


def _fbm(p, oct=4, lac=2.0, gain=0.5):
    a, f, s = 1.0, 1.0, 0.0
    for _ in range(oct):
        s += a * noise.noise(p * f)
        f *= lac; a *= gain
    return s


def _vor(p):
    """Cheap cellular/voronoi value in [0,1): distance to nearest jittered lattice point."""
    best = 9.9
    cx, cy, cz = math.floor(p.x), math.floor(p.y), math.floor(p.z)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                gx, gy, gz = cx + dx, cy + dy, cz + dz
                h = noise.noise(Vector((gx * 1.3, gy * 2.1, gz * 1.7)))
                h2 = noise.noise(Vector((gx * 2.7 + 5, gy * 1.1 + 3, gz * 2.3 + 7)))
                fx = gx + 0.5 + 0.5 * h
                fy = gy + 0.5 + 0.5 * h2
                fz = gz + 0.5 + 0.5 * noise.noise(Vector((gx + 9, gy + 2, gz + 4)))
                d = (Vector((fx, fy, fz)) - p).length
                if d < best:
                    best = d
    return min(0.999, best)


def rim_wall(name, W, D, H, seed, palette, ice_mode, snow_amt=1.0, overhangs=2):
    """Build one rim-wall panel. palette = (steep_dark, mid, pale) rock keys for geology bands.
    ice_mode: 'seams' | 'icicle_curtain' | 'snow_ledges' | 'glazed_drips'."""
    reset()
    rnd = random.Random(seed)
    steep, mid, pale = palette
    off = Vector((seed * 7.3, seed * 3.1, seed * 5.7))

    # ---- front face: a dense grid in the X-Z plane at y=0, displaced out (-Y) by fbm+voronoi ----
    nx, nz = 54, 30
    bm = bmesh.new()
    V = {}
    def groove(x, z):
        # a handful of irregular vertical fracture grooves: narrow low-Y dents
        g = 0.0
        for gx, depth, wdt in GROOVES:
            dx = abs(x - gx - 0.8 * math.sin(z * 0.18 + gx))
            g -= depth * math.exp(-(dx * dx) / (2 * wdt * wdt))
        return g
    GROOVES = []
    for _ in range(6):
        GROOVES.append((rnd.uniform(-W / 2 + 4, W / 2 - 4), rnd.uniform(0.8, 1.8), rnd.uniform(0.6, 1.4)))
    LEDGES = sorted(rnd.uniform(0.15, 0.9) * H for _ in range(5))

    for iz in range(nz + 1):
        z = H * iz / nz
        for ix in range(nx + 1):
            x = -W / 2 + W * ix / nx
            p = Vector((x * 0.12, 0.0, z * 0.14)) + off
            base = 1.6 * _fbm(p, oct=5)                 # broad relief
            fac = (0.5 - _vor(p * 1.6)) * 2.0            # voronoi facets (fracture planes)
            disp = base + 0.9 * fac + groove(x, z)
            # irregular ledges: just under a ledge height, push out a shelf; taper the very top back
            for lz in LEDGES:
                if 0 < (z - lz) < 1.4:
                    disp += 1.3 * (1 - (z - lz) / 1.4)
            if z > H - 2.5:
                disp -= (z - (H - 2.5)) * 0.6
            y = -(disp)                                  # out of the wall is -Y
            V[(ix, iz)] = bm.verts.new((x, y, z))
    for iz in range(nz):
        for ix in range(nx):
            bm.faces.new((V[(ix, iz)], V[(ix + 1, iz)], V[(ix + 1, iz + 1)], V[(ix, iz + 1)]))
    # ---- close the panel into a solid block: back wall at +D, sides, top, bottom ----
    # back + side skirt via a solidify-like shell: add a back grid and bridge the border
    back = {}
    for iz in range(nz + 1):
        z = H * iz / nz
        for ix in range(nx + 1):
            x = -W / 2 + W * ix / nx
            back[(ix, iz)] = bm.verts.new((x, D, z))
    for iz in range(nz):          # back face
        for ix in range(nx):
            bm.faces.new((back[(ix, iz)], back[(ix, iz + 1)], back[(ix + 1, iz + 1)], back[(ix + 1, iz)]))
    for ix in range(nx):          # top + bottom
        bm.faces.new((V[(ix, nz)], V[(ix + 1, nz)], back[(ix + 1, nz)], back[(ix, nz)]))
        bm.faces.new((V[(ix, 0)], back[(ix, 0)], back[(ix + 1, 0)], V[(ix + 1, 0)]))
    for iz in range(nz):          # left + right edges (IDENTICAL profiles so panels tile)
        bm.faces.new((V[(0, iz)], V[(0, iz + 1)], back[(0, iz + 1)], back[(0, iz)]))
        bm.faces.new((V[(nx, iz)], back[(nx, iz)], back[(nx, iz + 1)], V[(nx, iz + 1)]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    # ---- geology colouring: smooth, low-frequency; NO per-quad speckle, NO horizontal strata ----
    o = _obj_from_bm(name, bm, mid)
    for k in ('wf2c_rock_dark', steep, pale, 'snow'):
        if k not in [m.name.split('|')[0] for m in o.data.materials]:
            o.data.materials.append(mat(k))
    names = [m.name.split('|')[0] for m in o.data.materials]
    bm2 = bmesh.new(); bm2.from_mesh(o.data)
    bm2.faces.ensure_lookup_table()
    for f in bm2.faces:
        c = f.calc_center_median()
        up = f.normal.z
        hgt = c.z / H
        # 3D low-frequency field decides which of 3 rock tones -> big irregular blotches, not bands
        g = _fbm(Vector((c.x * 0.045, c.y * 0.05, c.z * 0.05)) + off * 0.3, oct=2)
        shade = hgt * 0.7 + g * 0.5                       # smooth gradient, perturbed
        if shade > 0.62:
            key = pale
        elif shade < 0.3:
            key = 'wf2c_rock_dark'
        else:
            key = mid
        if up < -0.4:                                     # steep / overhang faces read darker
            key = steep
        # SNOW only on genuinely near-horizontal, up-facing surfaces above the base (ledge tops),
        # gated by a low-freq field so it forms continuous caps rather than scattered squares.
        if snow_amt > 0 and up > 0.72 and c.z > 2.5 and (g + 0.3) > (1.0 - 0.55 * snow_amt):
            key = 'snow'
        f.material_index = names.index(key)
    bm2.to_mesh(o.data); bm2.free()

    # ---- overhang blocks + a few detached boulders on ledges (break the silhouette) ----
    for i in range(overhangs):
        lz = rnd.choice(LEDGES)
        bx = rnd.uniform(-W / 2 + 6, W / 2 - 6)
        r = rock(nm('ov'), rnd.uniform(2.2, 3.4), (bx, -2.0 - rnd.uniform(0, 1), lz + 1.2),
                 rnd.choice([steep, mid, 'wf2c_rock_dark']), seed=seed + i, scale=(1.4, 1.1, 0.8), subdiv=3, amp=0.34)
    for lz in LEDGES[::2]:
        for _ in range(rnd.randint(1, 2)):
            bx = rnd.uniform(-W / 2 + 4, W / 2 - 4)
            rock(nm('lb'), rnd.uniform(1.0, 1.8), (bx, -1.4, lz + 0.6), rnd.choice([mid, pale]), seed=seed + int(bx), scale=(1.3, 1.0, 0.7))

    # ---- ice feature by mode on the front ----
    if ice_mode == 'seams':
        # thin vertical ice ribbons running down the fracture grooves (geometry, not colour)
        for gx, depth, wdt in GROOVES:
            segs = int(H / 2.5)
            for s in range(segs):
                z = 1.5 + s * (H - 2) / segs
                jx = gx + 0.8 * math.sin(z * 0.18 + gx) + rnd.uniform(-0.3, 0.3)
                box(nm('seam'), (rnd.uniform(0.5, 1.1), 0.5, (H - 2) / segs + 0.4),
                    loc=(jx, -1.9 - rnd.uniform(0, 0.3), z), key=rnd.choice(['wf2c_ice_seam', 'wf2c_ice_glaze']), bev=0.08)
    if ice_mode == 'icicle_curtain':
        for lz in LEDGES:
            n = int(W / 1.3)
            for i in range(n):
                if rnd.random() > 0.6:
                    continue
                x = -W / 2 + W * i / n
                h = rnd.uniform(0.8, 3.0)
                r = rnd.uniform(0.1, 0.25)
                from kitlib import lathe
                lathe(nm('ic'), [(0, 0), (r, 0), (r * 0.5, -h * 0.45), (0, -h)], loc=(x, -2.2, lz), key=rnd.choice(['wf2c_ice_pale', 'wf2c_ice_glaze']), segs=5)
    if ice_mode == 'glazed_drips':
        for _ in range(int(W / 4)):
            x = rnd.uniform(-W / 2 + 3, W / 2 - 3)
            z0 = rnd.uniform(H * 0.4, H * 0.8)
            from kitlib import lathe
            lathe(nm('dr'), [(0, 0), (0.5, 0), (0.35, -z0 * 0.3), (0, -z0 * 0.6)], loc=(x, -2.4, z0), key='wf2c_ice_glaze', segs=6)

    # ---- scree + snow apron at the base (front, -Y) ----
    for i in range(16):
        x = rnd.uniform(-W / 2 + 1, W / 2 - 1)
        y = -2.5 - rnd.uniform(0, 3.5)
        r = rnd.uniform(0.6, 1.9)
        rock(nm('scr'), r, (x, y, r * 0.3), rnd.choice([steep, mid, 'wf2c_rock_dark']), seed=seed + i * 3, scale=(1.3, 1.1, 0.6), subdiv=2, amp=0.35)
    for i in range(14):
        x = rnd.uniform(-W / 2, W / 2)
        y = -2.0 - rnd.uniform(0, 4.0)
        blob(nm('sn'), rnd.uniform(1.0, 2.2), (x, y, 0.0), 'snow', subdiv=2, amp=0.12, scale=(1.6, 1.3, 0.35), seed=seed + i)

    return finalize(name, smooth_angle=30)


# -- four looks --------------------------------------------------------------------
def rim_wall_01():
    """E14_01 dark rock with blue ice seams threading the fracture planes."""
    return rim_wall('E14_01_icelake_rim_wall_01', 60, 25, 30, 1401,
                    ('wf2c_rock_dark', 'wf2c_rock_mid', 'wf2c_rock_pale'), 'seams', snow_amt=0.8, overhangs=3)


def rim_wall_02():
    """E14_02 pale rock with hanging icicle curtains off every ledge."""
    return rim_wall('E14_02_icelake_rim_wall_02', 60, 25, 30, 1402,
                    ('wf2c_rock_mid', 'wf2c_rock_pale', 'wf2c_rock_pale'), 'icicle_curtain', snow_amt=1.0, overhangs=2)


def rim_wall_03():
    """E14_03 layered slate with deep snow ledges."""
    return rim_wall('E14_03_icelake_rim_wall_03', 60, 25, 30, 1403,
                    ('wf2c_slate', 'wf2c_slate_pale', 'wf2c_rock_pale'), 'snow_ledges', snow_amt=1.4, overhangs=2)


def rim_wall_04():
    """E14_04 ice-glazed cliff with frozen drips sheeting down the rock."""
    return rim_wall('E14_04_icelake_rim_wall_04', 60, 25, 30, 1404,
                    ('wf2c_rock_dark', 'wf2c_rock_mid', 'wf2c_slate_pale'), 'glazed_drips', snow_amt=0.6, overhangs=2)


BATCHES = {
    'proto': ('v4_alpine', [('E14_01_icelake_rim_wall_01', rim_wall_01, (0.3, -1.3, 0.3))]),
    'walls': ('v4_alpine', [
        ('E14_01_icelake_rim_wall_01', rim_wall_01, (0.3, -1.3, 0.3)),
        ('E14_02_icelake_rim_wall_02', rim_wall_02, (0.3, -1.3, 0.3)),
        ('E14_03_icelake_rim_wall_03', rim_wall_03, (0.3, -1.3, 0.3)),
        ('E14_04_icelake_rim_wall_04', rim_wall_04, (0.3, -1.3, 0.3)),
    ]),
}
