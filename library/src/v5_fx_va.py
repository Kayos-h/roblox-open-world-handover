"""v5_fx_va - FIX ROUND builders for assignment A6 (worker va). Owner: builder A6.
Rebuilds the whole WT13 plateau terrace set (01-06) for v5_wizard.
Round-2 complaints: open hollow boxes, bright flat pale ramps/decks that read as light panels, blank/flat backs.
Fix: muted matte stone (not pale whitewash), every visible face coursed (front, back, both sides), moulded coping,
steps with real risers and a recessed dark throat, closed solid bodies, deep paving joints. No glow. Front -Y, pivot bottom centre.
Reuses the round-1 wizard palette via ORIG import. New keys only under va_f_.
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v4util
import v5kit
from v5kit import Acc, polar, tang, mk, ids, band, strata
import v5gen as G
from v5gen import house, round_tower, wall_seg, column, cliff, spire, rock_arch, tree
import v5_va as ORIG          # round-1 module: registers the va_ wizard palette and holds _courses; never edit it

K = ORIG.K                     # {'granite':'va_granite', 'limestone':'va_limestone', ...}

# muted, matte mid-tone stone (NOT pale whitewash) so big faces never read as lit panels; darker base, graded up
P = G.reg('va_f', {
    'stone_d':  ((118, 114, 108), 'Rock', 0.0, 0.95),      # dark base course
    'stone_m':  ((146, 142, 134), 'Rock', 0.0, 0.93),      # mid course
    'stone_l':  ((170, 165, 155), 'Cobblestone', 0.0, 0.9),# lighter upper course (still mid-tone, matte)
    'stone_a':  ((132, 126, 118), 'Slate', 0.0, 0.94),     # alt block for running-bond variety
    'trim':     ((158, 150, 138), 'Limestone', 0.0, 0.85), # coping (mid, not cream-white)
    'riser':    ((150, 144, 134), 'Limestone', 0.0, 0.88),
    'tread':    ((160, 154, 144), 'Cobblestone', 0.0, 0.9),
    'joint':    ((92, 88, 80),    'Slate', 0.0, 0.98),     # recessed dark paving/mortar joint
    'throat':   ((44, 42, 40),    'Slate', 0.0, 1.0),      # deep dark recess under lintels / stair sides
    'moss':     ((104, 122, 74),  'Grass', 0.0, 1.0),
    'wood':     ((110, 80, 54),   'Wood', 0.0, 0.9),
})

COURSE = [P['stone_d'], P['stone_m'], P['stone_l']]


def _fin(A, name):
    A.to_scene()
    return finalize(name, 25)


# ------------------------------------------------------------------ coursed ashlar skin on ONE straight vertical face
def _face_courses(A, rnd, cx, cy, length, z0, z1, thick, axis='x', depth_out=0.0, seed=0, bev=0.07, bw=(2.6, 4.6), rh=(1.4, 1.9)):
    """Lay running-bond ashlar blocks over a straight wall face. axis='x' -> wall runs along X at depth cy (face toward -Y side if cy<0).
    axis='y' -> wall runs along Y at cx. Blocks graded dark->light bottom to top. thick = block depth proud of the body."""
    r = random.Random(seed or (int(cx) * 13 + int(cy) * 7 + 1))
    z, row = z0, 0
    while z < z1 - 0.1:
        h = min(r.uniform(rh[0], rh[1]), z1 - z)
        off = (r.uniform(0.6, 1.8) if row % 2 else 0.0)
        t = (z - z0) / max(z1 - z0, 1e-6)
        s = -length / 2.0 + off
        while s < length / 2.0:
            w = r.uniform(bw[0], bw[1])
            sa, sb = max(s, -length / 2.0), min(s + w, length / 2.0)
            if sb - sa > 0.5:
                key = band(COURSE, t, r) if r.random() > 0.2 else P['stone_a']
                if axis == 'x':
                    A.box((sb - sa - 0.18, thick, h - 0.14), ((sa + sb) / 2.0, cy, z + h / 2.0), key, bev=bev)
                else:
                    A.box((thick, sb - sa - 0.18, h - 0.14), (cx, (sa + sb) / 2.0, z + h / 2.0), key, bev=bev)
            s += w
        z += h
        row += 1


def _wrap_body(A, rnd, w, d, cy, z0, z1, seed, bev=0.0, bw=(3.4, 5.6), rh=(1.7, 2.3)):
    """Course all four vertical faces of a rectangular terrace body centred on (0, cy). Faces proud of the solid core.
    Default sharp (bev=0) large blocks to keep the tri count down while still reading as coursed ashlar."""
    _face_courses(A, rnd, 0, cy - d / 2.0 + 0.05, w, z0, z1, 1.4, 'x', seed=seed + 1, bev=bev, bw=bw, rh=rh)        # front -Y
    _face_courses(A, rnd, 0, cy + d / 2.0 - 0.05, w, z0, z1, 1.4, 'x', seed=seed + 2, bev=bev, bw=bw, rh=rh)        # back +Y
    for sg in (-1, 1):
        _face_courses(A, rnd, sg * (w / 2.0 - 0.05), cy, d, z0, z1, 1.4, 'y', seed=seed + 10 + sg, bev=bev, bw=bw, rh=rh)


def _coping(A, w, d, cy, z, key=None):
    key = key or P['trim']
    A.box((w + 0.8, 1.6, 1.3), (0, cy - d / 2.0, z), key, bev=0.12)       # front
    A.box((w + 0.8, 1.6, 1.3), (0, cy + d / 2.0, z), key, bev=0.12)       # back
    for sg in (-1, 1):
        A.box((1.6, d + 0.8, 1.3), (sg * w / 2.0, cy, z), key, bev=0.12)  # sides


def _paved_deck(A, w, d, cy, ztop):
    """Paved deck with DEEP recessed joints (reads as flagstones, not a blank lid)."""
    A.box((w - 1.2, d - 1.2, 0.9), (0, cy, ztop - 0.45), P['stone_m'])
    for k in range(1, 6):
        A.box((0.45, d - 1.2, 0.5), (-w / 2.0 + k * w / 6.0, cy, ztop - 0.05), P['joint'], bev=0)
    for k in range(1, 5):
        A.box((w - 1.2, 0.45, 0.5), (0, cy - d / 2.0 + k * d / 5.0, ztop - 0.05), P['joint'], bev=0)
    # a few raised flag stones for relief
    r = random.Random(7)
    for _ in range(3):
        A.box((r.uniform(2.2, 3.6), r.uniform(2.2, 3.6), 0.22), (r.uniform(-w / 2 + 3, w / 2 - 3), cy + r.uniform(-d / 2 + 3, d / 2 - 3), ztop + 0.1), P['stone_l'], bev=0.08)


# ================================================================== WT13_01 straight retaining terrace (MAJOR fix)
def terrace_wall_straight():
    """WT13_01 - 30 x 30 x 10: solid coursed body on ALL four sides, moulded coping, a real recessed entry stair, paved deck. Closed underside."""
    reset()
    A = Acc()
    rnd = random.Random(2401)
    w, d = 30.0, 26.0
    cy = 1.0
    # solid core (closed box, no hollow underside) + ground footing
    A.box((w, d, 1.2), (0, cy, 0.6), P['stone_d'])
    A.box((w - 1.6, d - 1.6, 9.0), (0, cy, 4.8), P['stone_m'])
    _wrap_body(A, rnd, w, d, cy, 1.0, 9.2, seed=2401)
    # buttress pilasters on the front + sides
    for x in (-12, -4, 4, 12):
        A.box((2.2, 1.6, 8.4), (x, cy - d / 2.0 - 0.3, 5.1), P['stone_d'], bev=0.12)
        A.box((2.8, 2.2, 0.8), (x, cy - d / 2.0 - 0.4, 9.4), P['trim'], bev=0.1)
    _coping(A, w, d, cy, 9.7)
    _paved_deck(A, w, d, cy, 9.5)
    # a real recessed entry stair cut into the front: side cheek walls + treads + dark throat behind
    sw = 9.0
    A.box((sw + 2.4, 6.0, 0.5), (0, cy - d / 2.0 - 4.0, 0.25), P['stone_d'])     # landing pad on ground
    for i in range(6):
        zc = 1.4 + i * 1.3
        yy = cy - d / 2.0 - 4.4 + i * 0.75
        A.box((sw, 1.5, 1.2), (0, yy, zc - 0.6), P['tread'], bev=0.08)           # tread
        A.box((sw + 0.3, 0.4, 0.28), (0, yy - 0.75, zc + 0.1), P['trim'], bev=0) # nosing
        A.box((sw, 1.3, 1.3), (0, yy + 0.9, zc), P['throat'], bev=0)             # dark riser gap behind each tread
    for sg in (-1, 1):                                                           # cheek walls either side of the stair
        A.box((1.6, 7.0, 9.2), (sg * (sw / 2.0 + 0.8), cy - d / 2.0 - 3.6, 4.6), P['stone_m'], bev=0.1)
        A.box((2.0, 7.4, 0.7), (sg * (sw / 2.0 + 0.8), cy - d / 2.0 - 3.6, 9.2), P['trim'], bev=0.08)
    for k in range(7):
        A.ball(0.7, (rnd.uniform(-14, 14), cy - d / 2.0 - 0.2, 1.0), P['moss'], segs=6, rings=4, scale=(1.5, 1.0, 0.35))
    return _fin(A, 'terrace_wall_straight')


# ================================================================== WT13_02 curved retaining terrace (MAJOR fix)
def terrace_wall_curved():
    """WT13_02 - a quarter-round coursed retaining terrace: curved ashlar face AND curved back face, coping, broken paved top (no flat pale slab)."""
    reset()
    A = Acc()
    rnd = random.Random(2402)
    R = 24.0
    z0, z1 = 0.0, 9.0
    # solid curved body between inner and outer radius (closed)
    A.sweep([(R - 6.0, z0), (R + 1.4, z0), (R + 1.4, z1), (R - 6.0, z1)], 0, 90, 16, P['stone_m'])
    A.sweep([(R - 6.4, z0), (R - 5.6, z0), (R - 5.6, z1), (R - 6.4, z1)], 0, 90, 16, P['stone_d'])   # inner skin
    # coursed ashlar on the OUTER curved face (front), graded by height, running bond
    r2 = random.Random(2412)
    z, row = z0, 0
    while z < z1 - 0.1:
        h = min(r2.uniform(1.4, 1.9), z1 - z)
        t = (z - z0) / (z1 - z0)
        a = (r2.uniform(0, 6) if row % 2 else 0.0)
        while a < 90:
            wdeg = r2.uniform(7, 12)
            a0, a1 = max(a, 0.0), min(a + wdeg, 90.0)
            if a1 - a0 > 1.8:
                key = band(COURSE, t, r2) if r2.random() > 0.2 else P['stone_a']
                A.sweep([(R + 0.2, z + 0.08), (R + 1.7, z + 0.08), (R + 1.7, z + h - 0.12), (R + 0.2, z + h - 0.12)], a0 + 0.4, a1 - 0.4, 1, key)
            a += wdeg
        z += h
        row += 1
    # coursed inner (back) curved face too, so the back is finished
    r3 = random.Random(2422)
    z, row = z0, 0
    while z < z1 - 0.1:
        h = min(r3.uniform(1.4, 1.9), z1 - z)
        t = (z - z0) / (z1 - z0)
        a = (r3.uniform(0, 6) if row % 2 else 0.0)
        while a < 90:
            wdeg = r3.uniform(8, 13)
            a0, a1 = max(a, 0.0), min(a + wdeg, 90.0)
            if a1 - a0 > 1.8:
                A.sweep([(R - 6.3, z + 0.08), (R - 5.1, z + 0.08), (R - 5.1, z + h - 0.12), (R - 6.3, z + h - 0.12)], a0 + 0.4, a1 - 0.4, 1, band(COURSE, t, r3))
            a += wdeg
        z += h
        row += 1
    # moulded coping follows the curve
    A.sweep([(R - 6.6, z1), (R + 2.0, z1), (R + 2.0, z1 + 1.2), (R - 6.6, z1 + 1.2)], -2, 92, 18, P['trim'])
    # broken paved walk on top (flagstones with gaps + dark joints, NOT one flat slab)
    for k in range(7):
        a = 4 + k * 12.5
        x, y, _ = polar(R - 2.4, a)
        A.box((4.4, 3.4, 0.6), (x, y, z1 + 1.1), P['stone_l'] if k % 2 else P['stone_m'], (0, 0, a), bev=0.08)
        A.box((0.4, 3.6, 0.5), (*polar(R - 2.4, a + 6.2)[:2], z1 + 1.2), P['joint'], (0, 0, a + 6.2), bev=0)
    # a short flight of curved steps down the open end
    for i in range(5):
        A.sweep([(R - 1.5, 0), (R + 1.6, 0), (R + 1.6, 1.0 + i * 1.5), (R - 1.5, 1.0 + i * 1.5)], 90 - 2, 90 + 10 + i * 3, 3, P['tread'])
    for k in range(6):
        x, y, _ = polar(R + 1.0, 4 + k * 15)
        A.ball(0.7, (x, y, 0.8), P['moss'], segs=6, rings=4, scale=(1.4, 1.2, 0.35))
    return _fin(A, 'terrace_wall_curved')


# ================================================================== WT13_03 terrace stair (MAJOR fix - was a bright flat ramp)
def terrace_stair():
    """WT13_03 - a monumental stair that READS as steps, not a lit ramp: deep treads+risers in muted stone, dark riser throats,
    coursed cheek walls on both sides, a finished coursed underside/back, and newel posts. 30 x 30 x 10."""
    reset()
    A = Acc()
    rnd = random.Random(2403)
    nsteps = 11
    rise = 9.0 / nsteps
    run = 22.0 / nsteps
    y0 = -13.0
    # solid wedge core under the steps (closed, coursed on the back and sides so no hollow/flat underside)
    # back wall of the stair (the +Y top end) - coursed
    A.box((24.0, 2.2, 10.0), (0, 13.0, 5.0), P['stone_m'])
    _face_courses(A, rnd, 0, 14.1, 24.0, 0.0, 10.0, 1.3, 'x', seed=2433)         # finished back face
    A.box((24.4, 2.6, 1.3), (0, 13.0, 10.3), P['trim'], bev=0.1)                 # back coping
    for i in range(nsteps):
        zc = rise * (i + 1)
        yy = y0 + run * (i + 0.5)
        # tread (muted matte, slight tonal variation per step so it is not one flat pale sheet)
        tk = P['tread'] if i % 2 else P['stone_l']
        A.box((22.0, run + 0.25, rise), (0, yy, zc - rise / 2.0), tk, bev=0.06)
        A.box((22.3, 0.35, 0.22), (0, yy - run / 2.0, zc + 0.05), P['trim'], bev=0)   # nosing lip catches light = reads as a step edge
        A.box((22.0, 0.6, rise * 0.9), (0, yy - run / 2.0 - 0.2, zc - rise * 0.55), P['throat'], bev=0)  # dark shadow line under each nosing
        # solid riser down to the previous tread (closes the underside, no see-through)
        A.box((22.0, run, zc), (0, yy, zc / 2.0), P['stone_d'] if i == 0 else P['stone_m'], bev=0)
    # coursed cheek walls both sides, with a moulded rake coping and newel posts
    for sg in (-1, 1):
        for i in range(nsteps):
            zc = rise * (i + 1)
            yy = y0 + run * (i + 0.5)
            A.box((2.4, run + 0.3, zc + 1.6), (sg * 12.6, yy, (zc + 1.6) / 2.0), band(COURSE, i / nsteps, rnd), bev=0.1)
        # rake coping riding the stair line
        for i in range(nsteps):
            zc = rise * (i + 1)
            yy = y0 + run * (i + 0.5)
            A.box((3.0, run + 0.3, 0.6), (sg * 12.6, yy, zc + 1.7), P['trim'], bev=0.08)
        # newel posts bottom and top
        A.box((3.2, 3.2, 3.4), (sg * 12.6, y0 - 0.4, 1.7), P['stone_d'], bev=0.12)
        A.box((3.6, 3.6, 0.8), (sg * 12.6, y0 - 0.4, 3.6), P['trim'], bev=0.1)
        A.box((3.2, 3.2, 12.0), (sg * 12.6, 13.0, 6.0), P['stone_m'], bev=0.12)
        A.box((3.6, 3.6, 0.8), (sg * 12.6, 13.0, 12.2), P['trim'], bev=0.1)
    # bottom landing pad on the ground + a dark threshold
    A.box((26.0, 3.0, 0.6), (0, y0 - 1.6, 0.3), P['stone_d'])
    for k in range(6):
        A.ball(0.7, (rnd.uniform(-12, 12), y0 - 1.0, 0.7), P['moss'], segs=6, rings=4, scale=(1.4, 1.1, 0.35))
    return _fin(A, 'terrace_stair')


# ================================================================== WT13_04 prayer-flag pole (keep character, darker footing, finished)
def prayer_flag_pole():
    """WT13_04 - timber pole on a coursed stone footing drum with prayer-flag strings. Footing darkened + coursed; flags muted. Grounded."""
    reset()
    A = Acc()
    rnd = random.Random(2404)
    # coursed stone footing drum (not a loose ring of pale blocks)
    A.cyl(4.6, 1.0, (0, 0, 0), P['stone_d'], verts=20, r2=4.2)
    for row in range(3):
        z = 1.0 + row * 1.2
        n = 14
        for k in range(n):
            a = 360.0 / n * k + (12 if row % 2 else 0)
            x, y, _ = polar(3.9, a)
            A.box((1.5, 1.2, 1.1), (x, y, z + 0.55), band(COURSE, row / 3.0, rnd), (0, 0, a), bev=0.08)
    A.cyl(4.2, 0.6, (0, 0, 4.5), P['trim'], verts=20, r2=3.8)       # coping ring
    A.cyl(0.6, 10.5, (0, 0, 0.4), P['wood'], verts=10)
    for k in range(4):                                             # carved rings on the pole
        A.sweep([(0.62, -0.2), (0.85, -0.2), (0.85, 0.2), (0.62, 0.2)], 0, 360, 10, K['brass'], loc=(0, 0, 2.5 + k * 2.4))
    A.ball(0.8, (0, 0, 11.2), K['brass'], segs=8, rings=5)
    # four prayer-flag strings sagging to corner posts (muted fabric, not neon)
    fk = [K['indigo'], K['ochre'], K['copper'], P['moss'], K['timber']]
    for s, ang in enumerate((25, 115, 205, 295)):
        x1, y1, _ = polar(14.0, ang)
        A.box((1.4, 1.4, 2.4), (x1, y1, 1.2), P['stone_m'], (0, 0, ang), bev=0.1)   # anchor post on ground
        A.box((1.8, 1.8, 0.5), (x1, y1, 2.5), P['trim'], (0, 0, ang), bev=0.06)
        prev = (0, 0, 10.4)
        for t in (0.2, 0.4, 0.6, 0.8, 1.0):
            q = (x1 * t, y1 * t, 10.4 + (2.6 - 10.4) * t - 1.6 * 4 * t * (1 - t))
            A.beam(prev, q, 0.1, 0.1, K['timber'])
            if t < 1.0:
                yaw = math.degrees(math.atan2(y1, x1))
                A.box((1.9, 0.14, 1.5), (q[0], q[1], q[2] - 0.9), fk[(s * 4 + int(t * 5)) % 5], (0, 0, yaw), bev=0)
            prev = q
    return _fin(A, 'prayer_flag_pole')


# ================================================================== WT13_05 cairn (keep character, muted stones, grounded, finished)
def cairn():
    """WT13_05 (round 3, lead) - a stepped plateau terrace with a cairn on top, 30 x 30 x 10 like its WT13 siblings: two coursed tiers (solid cores, ashlar faces, coping, paved decks),
    a front stair in solid steps to each tier, and a tapering cairn of stacked stones with two small satellites on the upper deck. No bright finial."""
    reset()
    A = Acc()
    rnd = random.Random(2405)
    w, d = 30.0, 26.0
    A.box((w, d, 1.0), (0, 0, 0.5), P['stone_d'])
    A.box((w - 1.6, d - 1.6, 2.4), (0, 0, 2.2), P['stone_m'])
    _wrap_body(A, rnd, w, d, 0.0, 1.0, 3.4, seed=2405)
    _coping(A, w, d, 0.0, 3.7)
    _paved_deck(A, w, d, 0.0, 3.6)
    w2, d2 = 20.0, 18.0
    A.box((w2 - 1.2, d2 - 1.2, 2.0), (0, 0, 4.6), P['stone_m'])
    _wrap_body(A, rnd, w2, d2, 0.0, 3.6, 5.6, seed=2415)
    _coping(A, w2, d2, 0.0, 5.9)
    _paved_deck(A, w2, d2, 0.0, 5.8)
    for i in range(4):
        h = 0.9 + (i + 1) * 0.7
        A.box((8.0, 1.5, h), (0, -d / 2 - 0.6 - (3 - i) * 1.4, h / 2.0), P['tread'], bev=0.06)
        A.box((8.3, 0.4, 0.25), (0, -d / 2 - 0.6 - (3 - i) * 1.4 - 0.75, h + 0.05), P['trim'], bev=0)
    for i in range(3):
        h = 3.6 + (i + 1) * 0.7
        A.box((6.0, 1.4, h - 3.0), (0, -d2 / 2 - 0.4 - (2 - i) * 1.3, 3.0 + (h - 3.0) / 2.0), P['tread'], bev=0.06)
        A.box((6.3, 0.4, 0.25), (0, -d2 / 2 - 0.4 - (2 - i) * 1.3 - 0.7, h + 0.05), P['trim'], bev=0)
    z0 = 6.0
    A.cyl(3.8, 0.5, (0, 0, z0 - 0.3), P['stone_d'], verts=16, r2=3.5)
    z = z0 + 0.2
    for lv in range(5):
        r = 3.0 * (1.0 - lv / 7.0)
        n = max(1, 4 - lv // 2)
        for k in range(n):
            a_ = rnd.uniform(0, 360) if n > 1 else 0
            x, y, _ = polar(r * 0.45 if n > 1 else 0.0, a_)
            h = rnd.uniform(0.7, 0.95)
            A.chunk((rnd.uniform(1.9, 2.9) * (1 - lv * 0.06), rnd.uniform(1.7, 2.6) * (1 - lv * 0.06), h), (x, y, z + h / 2),
                    band(COURSE, lv / 5.0, rnd), (0, 0, rnd.uniform(0, 90)), 0.12, rnd)
        z += 0.6
    A.chunk((1.5, 1.5, 0.9), (0, 0, z + 0.3), P['stone_l'], (0, 0, 20), 0.12, rnd)
    for dx, dy in ((6.0, 5.0), (-6.0, 4.5)):
        zz = z0
        A.cyl(1.8, 0.4, (dx, dy, zz - 0.2), P['stone_d'], verts=10)
        for lv in range(4):
            h = rnd.uniform(0.6, 0.8)
            A.chunk((1.9 - lv * 0.3, 1.7 - lv * 0.28, h), (dx + rnd.uniform(-0.2, 0.2), dy + rnd.uniform(-0.2, 0.2), zz + h / 2),
                    band(COURSE, lv / 4.0, rnd), (0, 0, rnd.uniform(0, 90)), 0.12, rnd)
            zz += h * 0.95
    for k in range(6):
        A.ball(0.7, (rnd.uniform(-13, 13), -d / 2 - 0.3, 1.2), P['moss'], segs=6, rings=4, scale=(1.5, 1.0, 0.35))
    return _fin(A, 'cairn')


# ================================================================== WT13_06 lantern post + benches (coursed pad, not a pale disc)
def lantern_post():
    """WT13_06 (round 3, lead) - same plaza as before, but the lantern no longer reads as glowing: a stone lantern house in muted stone with four dark openings (no parchment
    yellow), dull bronze posts and finial."""
    reset()
    A = Acc()
    rnd = random.Random(2406)
    A.cyl(14.5, 0.6, (0, 0, 0), P['stone_d'], verts=36)
    A.cyl(13.4, 0.4, (0, 0, 0.6), P['stone_m'], verts=36)
    for k in range(16):
        a = 22.5 * k
        A.box((13.2, 0.35, 0.4), (0, 0, 0.9), P['joint'], (0, 0, a), bev=0)
    for rr in (5.0, 9.5):
        A.sweep([(rr - 0.18, 0.7), (rr + 0.18, 0.7), (rr + 0.18, 1.0), (rr - 0.18, 1.0)], 0, 360, 40, P['joint'])
    for k in range(28):
        a = 360.0 / 28 * k
        x, y, _ = polar(13.9, a)
        A.box((3.2, 1.4, 1.1), (x, y, 0.95), band(COURSE, 0.3 + 0.4 * (k % 2), rnd), (0, 0, a + 90), bev=0.08)
    A.sweep([(13.2, 1.5), (14.6, 1.5), (14.6, 2.0), (13.2, 2.0)], 0, 360, 40, P['trim'])
    A.cyl(2.6, 1.0, (0, 0, 1.0), P['stone_d'], verts=12)
    A.box((1.6, 1.6, 4.4), (0, 0, 3.6), P['stone_m'], bev=0.1)
    for z in (2.6, 4.4):
        A.box((2.0, 2.0, 0.4), (0, 0, z), P['trim'], bev=0.08)
    A.box((2.4, 2.4, 0.5), (0, 0, 6.0), P['trim'], bev=0.08)
    A.box((1.9, 1.9, 2.0), (0, 0, 7.2), P['stone_a'], bev=0.06)
    for sx, sy in ((1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0)):
        A.box((0.1, 0.9, 1.1) if sx else (0.9, 0.1, 1.1), (sx * 0.95, sy * 0.95, 7.2), P['throat'], bev=0)
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        A.box((0.18, 0.18, 2.1), (sx * 0.85, sy * 0.85, 7.2), PBZ['bronze'])
    A.cyl(1.7, 1.3, (0, 0, 8.2), P['stone_d'], verts=8, r2=0.2)
    A.ball(0.35, (0, 0, 9.6), PBZ['bronze'], segs=6, rings=4)
    for k in (60, 150, 240, 330):
        x, y, _ = polar(9.4, k)
        A.box((6.6, 1.8, 1.0), (x, y, 1.4), P['stone_m'], (0, 0, k + 90), bev=0.1)
        A.box((6.8, 2.0, 0.3), (x, y, 2.0), P['trim'], (0, 0, k + 90), bev=0.06)
        for e in (-1, 1):
            ox = math.cos(math.radians(k + 90)) * e * 2.6
            oy = math.sin(math.radians(k + 90)) * e * 2.6
            A.box((1.0, 1.4, 1.2), (x + ox, y + oy, 0.9), P['stone_d'], (0, 0, k + 90), bev=0.08)
    return _fin(A, 'lantern_post')


PBZ = G.reg('va_f', {
    'bronze': ((112, 88, 62), 'Metal', 0.3, 0.75),
})


def _curved_post(A):
    R = 24.0
    for a0, a1 in ((-2.0, 0.0), (90.0, 92.0)):
        A.sweep([(R - 6.4, 0.0), (R + 1.4, 0.0), (R + 1.4, 9.0), (R - 6.4, 9.0)], a0, a1, 2, P['stone_m'])
    A.sweep([(R - 6.8, 0.0), (R + 2.0, 0.0), (R + 2.0, 0.8), (R - 6.8, 0.8)], -2, 92, 18, P['stone_d'])


def wt13_01():
    return LK.wrap(terrace_wall_straight, prune=[dict(keys=[P['joint']], max_size=30.0)])()


def wt13_02():
    return LK.wrap(terrace_wall_curved, post=_curved_post)()


def wt13_03():
    return LK.wrap(terrace_stair, recolor=[LK.ramp([P['throat']], [P['stone_d']])])()


BATCHES = {
    'tower_terrace': ('v5_wizard', mk([
        ('WT13_01_plateau_terrace_set_01', terrace_wall_straight),
        ('WT13_02_plateau_terrace_set_02', terrace_wall_curved),
        ('WT13_03_plateau_terrace_set_03', terrace_stair),
        ('WT13_04_plateau_terrace_set_04', prayer_flag_pole),
        ('WT13_05_plateau_terrace_set_05', cairn),
        ('WT13_06_plateau_terrace_set_06', lantern_post)], 0.1)),
}


# --- lead4 registration ---
import v5_leadkit as LK
BATCHES['lead4_va'] = ('v5_wizard', mk([('WT13_01_plateau_terrace_set_01', wt13_01), ('WT13_02_plateau_terrace_set_02', wt13_02), ('WT13_03_plateau_terrace_set_03', wt13_03)], 0.1))
