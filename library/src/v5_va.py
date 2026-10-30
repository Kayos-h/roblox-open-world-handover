"""va module - the giant enterable wizard tower, EXTERIOR ('The Star Spire', original design).
WT01 shell, WT12 porch, WT11 armillary crown, WT13 terrace set (6 pieces). Front faces -Y. Floors, radii and window slots come from
v5kit.TOWER so the interior (WT02 in v5_vb) matches. No glow anywhere; warm light is placed in Studio.
Sizes in the briefs are (x, height, depth) in Roblox axes; in Blender that is X, Y=depth, Z=height.
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v5kit
from v5kit import Acc, polar, tang, TOWER as T, tower_top
import v4util

v5kit.wiz_pal('va')
K = {n: 'va_' + n for n in v5kit.WIZ}
kitlib.PAL['va_doorl'] = ((104, 56, 44), 'Wood', 0.0, 0.85, 0)
kitlib.PAL['va_doorr'] = ((104, 56, 44), 'Wood', 0.0, 0.85, 0)


# ------------------------------------------------------------------ helpers
def _frame(A, ro, ang, zlo, zhi, w, key, depth=1.8):
    """Tapered timber window frame on the outside of a wall opening (the jambs lean in at the top)."""
    tx, ty = tang(ang)
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))

    def at(off, z):
        return ((ro + 0.2) * c + tx * off, (ro + 0.2) * s + ty * off, z)
    h = zhi - zlo
    A.box((depth, w + 3.6, 1.2), at(0, zlo - 0.6), key, (0, 0, ang))
    A.box((depth, w + 2.4, 1.5), at(0, zhi + 0.75), key, (0, 0, ang))
    for sg in (-1, 1):
        A.box((depth, 1.3, h + 0.4), at(sg * (w / 2 + 0.55), (zlo + zhi) / 2.0), key, (sg * 4.0, 0, ang))


def _flags(A, rb, z, a_start, npost, keys):
    """Prayer-flag strings hung between the railing posts of a ring balcony."""
    pts = [polar(rb - 0.4, a_start + k * 360.0 / npost, z) for k in range(npost + 1)]
    for k in range(npost):
        p0, p1 = pts[k], pts[k + 1]
        prev = None
        for t in (0.0, 0.25, 0.5, 0.75, 1.0):
            q = (p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t, z - 1.1 * 4 * t * (1 - t))
            if prev is not None:
                A.beam(prev, q, 0.12, 0.12, K['timber'])
            prev = q
        yaw = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
        for fi, t in enumerate((0.25, 0.5, 0.75)):
            q = (p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t, z - 1.1 * 4 * t * (1 - t) - 1.0)
            A.box((1.6, 0.08, 1.8), q, keys[(k * 3 + fi) % len(keys)], (0, 0, yaw))


def _star(R, r, n=5):
    pts = []
    for k in range(2 * n):
        rr = R if k % 2 == 0 else r
        a = math.pi / 2 + math.pi * k / n
        pts.append((rr * math.cos(a), rr * math.sin(a)))
    return pts


def _courses(A, x0, x1, y, z0, z1, thick, key_main, key_alt, seed):
    """Dry-stone courses of blocks between x0 and x1 (running bond)."""
    rnd = random.Random(seed)
    z, row = z0, 0
    while z < z1 - 0.2:
        h = min(rnd.uniform(1.3, 1.8), z1 - z)
        x = x0 - (rnd.uniform(0, 2.0) if row % 2 else 0.0)
        while x < x1:
            w = rnd.uniform(2.2, 4.4)
            xa, xb = max(x, x0), min(x + w, x1)
            if xb - xa > 0.4:
                A.box((xb - xa - 0.12, thick + rnd.uniform(-0.15, 0.15), h - 0.1), ((xa + xb) / 2.0, y, z + h / 2.0),
                      key_alt if rnd.random() < 0.18 else key_main)
            x += w
        z += h
        row += 1


# ------------------------------------------------------------------ WT01 the tower shell
def tower_shell():
    """WT01_01 - 300 studs tall, 8 levels, round walls 6 thick with real 14 x 8 window openings, twisting upward."""
    reset()
    A = Acc()
    F, N, OD, W = T['floors'], T['slots'], T['outer_d'], T['wall']
    front, tw = T['front_deg'], T['twist']
    flagkeys = [K['indigo'], K['ochre'], K['copper'], K['white'], K['timber']]
    for i in range(8):
        z0, z1 = F[i], tower_top(i)
        ro = OD[i] / 2.0
        ri = ro - W
        rn = OD[i + 1] / 2.0 if i < 7 else ro
        base = front + tw * i
        step = 360.0 / N[i]
        tiers = [(10.0, 18.0), (26.0, 34.0)] if i == 0 else [(12.0, 20.0)]
        ops, wins = [], []
        if i == 0:
            ops.append((front, 11.0, [(0.0, 13.0)]))                     # the front door opening (11 wide, 13 high)
        for k in range(N[i]):
            if i == 0 and k == 0:
                continue
            ang = base + (k * step if i == 0 else (k + 0.5) * step)
            wins.append(ang)
            ops.append((ang, 14.0, [(z0 + a, z0 + b) for a, b in tiers]))
        A.ring_wall(ri, ro, z0, z1, ops, K['white'])
        if i == 0:
            A.ring_wall(ri, ro + 0.9, 0.0, 7.0, [(front, 11.0, [(0.0, 13.0)])], K['granite'])
        fk = K['timber'] if i <= 3 else K['ochre']
        for ang in wins:
            for a, b in tiers:
                _frame(A, ro, ang, z0 + a, z0 + b, 14.0, fk)
        if i > 0:                                                          # slender limestone pilasters between the windows
            for k in range(N[i]):
                x, y, _ = polar(ro + 0.35, base + k * step)
                zlo, zhi = z0 + 1.2, z1 - 5.4
                A.box((1.3, 3.0, zhi - zlo), (x, y, (zlo + zhi) / 2.0), K['limestone'], (0, 0, base + k * step))
                A.box((1.8, 3.8, 0.8), (x, y, zhi + 0.4), K['granite'], (0, 0, base + k * step))
                A.box((1.8, 3.8, 0.8), (x, y, zlo - 0.4), K['granite'], (0, 0, base + k * step))
        if i == 0:                                                         # extra whitewash/limestone courses on the monastery drum
            A.sweep([(ro - 0.2, 21.0), (ro + 0.5, 21.0), (ro + 0.5, 23.0), (ro - 0.2, 23.0)], 0, 360, 48, K['limestone'])
        if i == 1:
            A.sweep([(ro - 0.2, z0 + 3.0), (ro + 0.5, z0 + 3.0), (ro + 0.5, z0 + 5.0), (ro - 0.2, z0 + 5.0)], 0, 360, 48, K['limestone'])
        # limestone cornice band under the top of every level, timber band on levels 1 and 2
        A.sweep([(ro - 0.2, z1 - 5.0), (ro + 0.8, z1 - 5.0), (ro + 0.8, z1 - 2.6), (ro - 0.2, z1 - 2.6)], 0, 360, 48, K['limestone'])
        if i in (1, 2):
            A.sweep([(ro - 0.2, z0 + 22.5), (ro + 0.6, z0 + 22.5), (ro + 0.6, z0 + 25.5), (ro - 0.2, z0 + 25.5)], 0, 360, 48, K['timber'])
        # shoulder between this level and the next
        if i in (0, 2, 4, 6):                                              # copper-green pagoda eaves
            A.sweep([(rn - 0.5, z1 - 0.2), (rn - 0.5, z1 + 1.4), (ro + 4.6, z1 - 2.6), (ro + 4.6, z1 - 3.6), (ro + 0.4, z1 - 1.0)],
                    0, 360, 56, K['copper'])
        else:                                                              # ring balconies with railing, flags and corner turrets
            rb = ro + (5.5 if i == 7 else 3.4)
            A.sweep([(min(rn, ro) - 0.5, z1 - 1.8), (rb, z1 - 1.8), (rb, z1), (min(rn, ro) - 0.5, z1)], 0, 360, 56, K['limestone'])
            npost = 30
            for k in range(npost):
                x, y, _ = polar(rb - 0.4, base + 6.0 + k * 360.0 / npost)
                A.box((0.7, 0.7, 3.8), (x, y, z1 + 1.9), K['timber'])
            A.sweep([(rb - 0.8, z1 + 3.6), (rb, z1 + 3.6), (rb, z1 + 4.3), (rb - 0.8, z1 + 4.3)], 0, 360, 60, K['ochre'])
            if i in (1, 3, 5):
                _flags(A, rb, z1 + 3.6, base + 6.0, npost, flagkeys)
                for k in range(4):
                    x, y, _ = polar(ro + 1.0, base + 45.0 + 90.0 * k)
                    A.cyl(3.4, 15.0, (x, y, z1), K['limestone'], verts=16)
                    A.cyl(3.9, 1.2, (x, y, z1 + 15.0), K['granite'], verts=16)
                    A.cyl(4.5, 9.5, (x, y, z1 + 16.2), K['copper'], verts=16, r2=0.0)
    # emblem over the door: brass star on a limestone disc with an open book below (white star over an open book on indigo)
    y_face = -(OD[1] / 2.0 + 0.5)
    A.cyl(7.0, 0.7, (0, y_face, 51.0), K['limestone'], verts=24, rot=(90, 0, 0))
    A.cyl(5.8, 0.4, (0, y_face - 0.6, 51.0), K['indigo'], verts=24, rot=(90, 0, 0))
    A.prism(_star(4.6, 1.9), 0.5, (0, y_face - 1.0, 51.8), K['brass'], (90, 0, 0))
    A.box((5.0, 0.4, 1.2), (0, y_face - 1.1, 46.6), K['parchment'])
    A.box((0.25, 0.5, 1.4), (0, y_face - 1.1, 46.6), K['timber'])
    # angled granite buttresses around the monastery drum (between the windows)
    r0 = OD[0] / 2.0
    for k in range(N[0]):
        a = front + (k + 0.5) * 360.0 / N[0]
        x, y, _ = polar(r0 + 1.4, a)
        A.box((4.0, 5.2, 34.0), (x, y, 17.0), K['granite'], (0, -6.0, a))
        x2, y2, _ = polar(r0 + 0.2, a)
        A.box((3.0, 6.0, 1.6), (x2, y2, 34.4), K['limestone'], (0, 0, a))
    # crown: copper dome with an observatory slit toward the front, brass ring, spire, star finial, banner
    zd = float(T['top_deck'])
    rd, hd, th = OD[7] / 2.0 + 0.6, 25.0, 2.2
    outer = [(rd * math.cos(math.radians(t)), zd + hd * math.sin(math.radians(t))) for t in range(0, 81, 10)]
    inner = [((rd - th) * math.cos(math.radians(t)), zd + (hd - th) * math.sin(math.radians(t))) for t in range(80, -1, -10)]
    A.sweep(outer + [(1.2, zd + hd + 0.2)] + inner, front + 9.0, front - 9.0 + 360.0, 40, K['copper'])
    for side in (-9.0, 9.0):
        prev = None
        for t in range(0, 81, 10):
            q = polar(rd * math.cos(math.radians(t)) + 0.15, front + side, zd + hd * math.sin(math.radians(t)))
            if prev is not None:
                A.beam(prev, q, 0.5, 0.5, K['brass'])
            prev = q
    A.sweep([(rd - th - 0.3, zd), (rd + 0.7, zd), (rd + 0.7, zd + 1.4), (rd - th - 0.3, zd + 1.4)], 0, 360, 48, K['brass'])
    zt = zd + hd + 0.2
    A.revolve([(2.2, zt - 1.0), (2.2, zt + 1.0), (1.4, zt + 1.0), (1.1, zt + 2.0), (0.5, zt + 6.5), (0.0, zt + 7.2)], key=K['brass'], segs=12)
    A.prism(_star(2.4, 1.0), 0.5, (0, 0.25, 297.6), K['brass'], (90, 0, 0))
    A.prism(_star(2.4, 1.0), 0.5, (0.25, 0, 297.6), K['brass'], (90, 0, 90))
    for s in range(9):                                                     # long indigo banner streaming from the spire
        x0 = 1.0 + s * 3.6
        A.box((3.7, 0.25, 4.6 - 0.25 * s), (x0 + 1.8, math.sin(s * 0.9) * 1.6, 293.4 - 0.12 * s), K['indigo'],
              (0, 0, math.degrees(math.atan(math.cos(s * 0.9) * 0.9 / 3.6))))
    A.to_scene()
    return finalize('wizard_tower_shell', smooth_angle=25)


# ------------------------------------------------------------------ WT12 porch
def door_porch():
    """WT12_01 - 40 wide, 24 deep, 36 tall. Rectangular carved frame (no arch), separate door leaves, steps, lantern posts.
    Back plane y=+12 meets the tower wall. Door leaves have their own palette keys; hinge/door markers give Studio the pivots."""
    reset()
    A = Acc()
    A.box((40, 20, 1.5), (0, 2.0, 0.75), K['limestone'])                                    # platform, y -8 .. +12
    for i in range(2):                                                                       # two front steps, low one in front
        A.box((26 - 4 * i, 2.0, 0.5 * (i + 1)), (0, -11.0 + 2.0 * i, 0.25 * (i + 1)), K['limestone'])
    for sg in (-1, 1):                                                                       # granite cheek walls beside the steps
        A.box((1.6, 5.0, 1.4), (sg * 14.0, -9.5, 0.7), K['granite'])
        A.box((2.0, 5.4, 0.4), (sg * 14.0, -9.5, 1.6), K['limestone'])
    zf = 1.5
    for sg in (-1, 1):                                                                       # granite door frame
        A.box((3.0, 3.0, 14.8), (sg * 7.0, 10.4, zf + 7.4), K['granite'])
        A.box((3.6, 3.6, 1.2), (sg * 7.0, 10.4, zf + 15.4), K['limestone'])
    A.box((17.6, 3.4, 2.0), (0, 10.4, zf + 14.9), K['timber'])                               # carved lintel
    A.box((17.0, 0.4, 0.8), (0, 8.5, zf + 15.0), K['ochre'])
    A.box((17.6, 3.0, 9.0), (0, 10.4, zf + 20.4), K['timber'])                               # carved tympanum panel (rectangular)
    A.box((14.6, 0.3, 6.6), (0, 8.8, zf + 20.6), K['indigo'])
    A.prism(_star(2.6, 1.1), 0.4, (0, 8.55, zf + 21.0), K['brass'], (90, 0, 0))
    A.box((6.0, 0.35, 1.0), (0, 8.55, zf + 18.6), K['parchment'])                            # open-book emblem
    for sg in (-1, 1):
        A.box((0.6, 0.4, 6.4), (sg * 7.5, 8.7, zf + 20.5), K['ochre'])
    # door leaves (separate palette keys -> separate MeshParts), carved ochre panels, brass studs and rings
    for key, sg in ((K['doorl'] if 'doorl' in K else 'va_doorl', -1), ('va_doorr', 1)):
        A.box((5.4, 1.2, 12.8), (sg * 2.75, 10.8, zf + 6.4), key)
        for pz in (3.0, 9.6):
            A.box((3.6, 0.3, 4.6), (sg * 2.75, 10.1, zf + pz), K['ochre'])
        for pz in (1.0, 6.4, 11.8):
            for px in (-1.8, 1.8):
                A.ball(0.22, (sg * 2.75 + px, 10.1, zf + pz), K['brass'], segs=8, rings=5)
        A.cyl(0.55, 0.15, (sg * 0.9, 10.05, zf + 6.4), K['brass'], verts=10, rot=(90, 0, 0))
    v4util.marker('mk_hingel', (-5.5, 10.8, zf + 6.4))
    v4util.marker('mk_hinger', (5.5, 10.8, zf + 6.4))
    v4util.marker('mk_door', (0, 8.0, zf + 0.2))
    # porch roof on four timber posts: beams, indigo slate gable, copper ridge
    for px in (-17.5, 17.5):
        for py in (-7.5, 9.0):
            A.box((1.8, 1.8, 26.0), (px, py, zf + 13.0), K['timber'])
            A.box((2.6, 2.6, 0.8), (px, py, zf + 0.4), K['granite'])
            A.box((2.8, 2.8, 0.8), (px, py, zf + 26.4), K['ochre'])
        A.box((2.0, 18.6, 1.6), (px, 0.75, zf + 27.4), K['timber'])
    for py in (-7.5, 9.0):
        A.box((37.0, 1.8, 1.6), (0, py, zf + 27.4), K['timber'])
    A.gable(40.0, 24.0, 7.2, (0, 0.5, zf + 28.2), K['indigo'])
    A.box((0.9, 24.6, 0.7), (0, 0.5, zf + 35.5), K['copper'])
    for sg in (-1, 1):                                                                       # copper ridge finials
        A.cyl(0.8, 2.4, (0, 0.5 + sg * 12.4, zf + 35.1), K['copper'], verts=8, r2=0.0)
    for k in range(9):                                                                       # rafter ends along both eaves
        for sg in (-1, 1):
            A.box((1.6, 0.6, 0.6), (sg * 19.6, -10.6 + k * 2.8, zf + 28.4), K['timber'], (0, 0, 0))
    for sg in (-1, 1):                                                                       # lantern posts on the platform (no glow)
        A.box((1.4, 1.4, 7.0), (sg * 15.0, -6.5, zf + 3.5), K['granite'])
        A.box((2.0, 2.0, 0.6), (sg * 15.0, -6.5, zf + 7.2), K['brass'])
        A.box((1.5, 1.5, 2.0), (sg * 15.0, -6.5, zf + 8.5), K['parchment'])
        A.cyl(1.4, 1.2, (sg * 15.0, -6.5, zf + 9.5), K['copper'], verts=8, r2=0.0)
    A.to_scene()
    return finalize('wizard_door_porch', smooth_angle=25)


# ------------------------------------------------------------------ WT11 armillary crown
def armillary_crown():
    """WT11_01 - static brass armillary rings (70 x 70 wide, 50 tall) that sit around the crown."""
    reset()
    A = Acc()
    zc = 25.0
    sq = 0.72

    def ring(R, r, tilt, yaw, key, segs=48):
        # torus built as a sweep of a small square section, tilted/yawed, squashed to the oblate sphere
        poly = [(R - r, -r), (R + r, -r), (R + r, r), (R - r, r)]
        A.sweep(poly, 0, 360, segs, key, loc=(0, 0, zc), rot=(tilt, 0, yaw))
    ring(34.0, 0.9, 0, 0, K['brass'])
    ring(32.0, 0.8, 90, 0, K['brass'])
    ring(32.0, 0.8, 90, 90, K['brass'])
    ring(30.0, 0.8, 23.5, 0, K['copper'])
    ring(26.0, 0.7, 66.5, 45, K['brass'])
    A.cyl(0.7, 50.0, (0, 0, 0), K['brass'], verts=8)                                         # polar axis
    A.ball(2.4, (0, 0, zc), K['copper'], segs=12, rings=8)                                   # core
    for k in range(36):                                                                      # degree ticks on the equator ring
        x, y, _ = polar(34.9, k * 10.0)
        A.box((0.7, 0.5, 2.2 if k % 3 == 0 else 1.2), (x, y, zc), K['white'], (0, 0, k * 10.0))
    for k in range(8):                                                                       # beads at the ring crossings
        x, y, z = polar(32.0, k * 45.0, zc)
        A.ball(1.0, (x, y, z), K['brass'], segs=8, rings=5)
    for sg in (-1, 1):                                                                       # axis caps
        A.ball(1.2, (0, 0, 25.0 + sg * 24.5), K['brass'], segs=8, rings=5)
    A.to_scene()
    ob = finalize('wizard_armillary_crown', smooth_angle=30)
    for v in ob.data.vertices:                                                               # oblate sphere: 70 wide, 50 tall
        v.co.z *= 0.762
    ob.data.update()
    return ob


# ------------------------------------------------------------------ WT13 terrace set
def terrace_wall_straight():
    """30 x 30 x 10 terrace module: coursed retaining-wall face toward -Y, solid backing, paved deck on top, low coping."""
    reset()
    A = Acc()
    A.box((30, 30, 1.0), (0, 0, 0.5), K['granite'])
    A.box((30, 26.0, 8.0), (0, 2.0, 5.0), K['granite'])
    A.box((30, 4.4, 8.0), (0, -13.0, 5.0), K['granite'])
    _courses(A, -15, 15, -13.0, 1.0, 9.0, 3.6, K['granite'], K['limestone'], 1)
    A.box((30.4, 30.4, 1.0), (0, 0, 9.5), K['limestone'])
    A.box((30.4, 1.3, 0.8), (0, -14.3, 10.4), K['granite'])
    for x in (-13, -4.5, 4.5, 13):
        A.box((2.2, 1.4, 8.6), (x, -15.0, 5.3), K['granite'])
        A.box((2.8, 1.8, 0.7), (x, -15.0, 9.7), K['limestone'])
    for k in range(1, 6):                                                                    # paving joints on the deck
        A.box((0.18, 30.0, 0.06), (-15 + k * 5.0, 0, 10.03), K['granite'])
    A.to_scene()
    return finalize('terrace_wall_straight', 25)


def terrace_wall_curved():
    reset()
    A = Acc()
    R = 26.0
    A.sweep([(R - 3.0, 0), (R + 3.0, 0), (R + 3.0, 1.0), (R - 3.0, 1.0)], 0, 90, 12, K['granite'])
    rnd = random.Random(2)
    z, row = 1.0, 0
    while z < 9.0:
        h = min(rnd.uniform(1.3, 1.8), 9.0 - z)
        a = -(rnd.uniform(0, 7) if row % 2 else 0.0)
        while a < 90:
            w = rnd.uniform(5, 10)
            a0, a1 = max(a, 0.0), min(a + w, 90.0)
            if a1 - a0 > 1.5:
                A.sweep([(R - 1.8 + rnd.uniform(-0.1, 0.1), z), (R + 1.8 + rnd.uniform(-0.1, 0.1), z), (R + 1.8, z + h - 0.1), (R - 1.8, z + h - 0.1)],
                        a0 + 0.3, a1 - 0.3, 1, K['limestone'] if rnd.random() < 0.18 else K['granite'])
            a += w
        z += h
        row += 1
    A.sweep([(R - 2.6, 9.0), (R + 2.6, 9.0), (R + 2.6, 10.0), (R - 2.6, 10.0)], 0, 90, 12, K['limestone'])
    for a in (6, 30, 54, 78):
        x, y, _ = polar(R + 2.0, a)
        A.box((2.2, 1.4, 8.6), (x, y, 5.3), K['granite'], (0, 0, a))
    A.to_scene()
    return finalize('terrace_wall_curved', 25)


def terrace_stair():
    """40 broad steps (rise 0.25, run 0.7), cheek walls and two lantern posts; climbed toward +Y."""
    reset()
    A = Acc()
    for i in range(40):
        A.box((24.0, 0.7 + 0.05, 0.25 * (i + 1)), (0, -14.0 + 0.7 * (i + 0.5), 0.125 * (i + 1)), K['limestone'] if i % 8 else K['granite'])
    for sg in (-1, 1):
        for i in range(0, 40, 4):
            hh = 0.25 * (i + 4) + 0.5
            A.box((2.6, 2.8 + 0.02, hh), (sg * 13.3, -14.0 + 0.7 * (i + 2), hh / 2.0), K['granite'])
        A.box((3.0, 3.0, 0.5), (sg * 13.3, 12.0, 10.25), K['limestone'])
    A.box((30.0, 2.0, 10.0), (0, 14.0, 5.0), K['granite'])                                   # landing at the top
    A.box((30.4, 2.4, 0.5), (0, 14.0, 10.25), K['limestone'])
    A.to_scene()
    return finalize('terrace_stair', 25)


def prayer_flag_pole():
    reset()
    A = Acc()
    rnd = random.Random(4)
    for k in range(9):                                                                       # stone footing ring
        x, y, _ = polar(2.6, k * 40.0)
        A.box((2.2, 2.0, 1.6 + rnd.uniform(0, 0.8)), (x, y, 0.9), K['granite'], (0, 0, k * 40.0))
    A.cyl(0.55, 9.2, (0, 0, 0.3), K['timber'], verts=8)
    A.ball(0.7, (0, 0, 9.8), K['brass'], segs=8, rings=5)
    keys = [K['indigo'], K['white'], K['timber'], K['copper'], K['ochre']]
    for s, ang in enumerate((20, 110, 200, 290)):
        x1, y1, _ = polar(14.6, ang)
        A.box((0.5, 0.5, 2.0), (x1, y1, 1.0), K['timber'])
        prev = (0, 0, 9.0)
        for t in (0.2, 0.4, 0.6, 0.8, 1.0):
            q = (x1 * t, y1 * t, 9.0 + (2.0 - 9.0) * t - 1.4 * 4 * t * (1 - t))
            A.beam(prev, q, 0.1, 0.1, K['timber'])
            if t < 1.0:
                yaw = math.degrees(math.atan2(y1, x1))
                A.box((2.0, 0.08, 1.7), (q[0], q[1], q[2] - 0.95), keys[(s * 4 + int(t * 5)) % 5], (0, 0, yaw))
            prev = q
    A.to_scene()
    return finalize('prayer_flag_pole', 30)


def cairn():
    reset()
    A = Acc()
    rnd = random.Random(7)
    z = 0.0
    for lv in range(11):
        r = 4.2 * (1.0 - lv / 13.0)
        n = max(1, 5 - lv // 3)
        for k in range(n):
            a = rnd.uniform(0, 360) if n > 1 else 0
            d = r * 0.5 if n > 1 else 0.0
            x, y, _ = polar(d, a)
            h = rnd.uniform(0.7, 1.0)
            A.box((rnd.uniform(2.0, 3.2) * (1 - lv * 0.05), rnd.uniform(1.8, 2.8) * (1 - lv * 0.05), h), (x, y, z + h / 2), K['granite'] if rnd.random() < 0.7 else K['limestone'], (0, 0, rnd.uniform(0, 90)))
        z += 0.82
    A.ball(0.6, (0, 0, z + 0.4), K['white'], segs=8, rings=5, scale=(1, 1, 0.7))
    for dx, dy in ((13.5, 3.0), (-12.5, 13.0), (4.0, -13.5)):                                 # three small satellite cairns
        zz = 0.0
        for lv in range(4):
            h = rnd.uniform(0.6, 0.9)
            A.box((2.0 - lv * 0.35, 1.8 - lv * 0.3, h), (dx + rnd.uniform(-0.2, 0.2), dy + rnd.uniform(-0.2, 0.2), zz + h / 2), K['granite'], (0, 0, rnd.uniform(0, 90)))
            zz += h * 0.95
    A.to_scene()
    return finalize('cairn', 30)


def lantern_post():
    """29-wide round paved pad, a granite lantern post (warm lantern, no glow) and four benches."""
    reset()
    A = Acc()
    A.cyl(14.5, 0.5, (0, 0, 0), K['granite'], verts=32)
    A.cyl(12.8, 0.3, (0, 0, 0.5), K['limestone'], verts=32)
    for k in range(12):
        x, y, _ = polar(13.6, k * 30.0)
        A.box((2.4, 1.1, 0.35), (x, y, 0.68), K['granite'], (0, 0, k * 30.0))
    A.cyl(2.8, 0.9, (0, 0, 0.8), K['granite'], verts=12)
    A.box((1.4, 1.4, 4.4), (0, 0, 3.4), K['granite'])
    A.box((2.2, 2.2, 0.5), (0, 0, 5.85), K['brass'])
    A.box((1.7, 1.7, 2.0), (0, 0, 7.1), K['parchment'])
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        A.box((0.16, 0.16, 2.2), (sx * 0.85, sy * 0.85, 7.1), K['brass'])
    A.cyl(1.6, 1.2, (0, 0, 8.2), K['copper'], verts=8, r2=0.0)
    A.ball(0.3, (0, 0, 9.5), K['brass'], segs=6, rings=4)
    for k in (60, 120, 240, 300):
        x, y, _ = polar(10.0, k)
        A.box((7.0, 1.8, 0.9), (x, y, 1.25, ), K['granite'], (0, 0, k + 90))
        A.box((7.4, 2.2, 0.4), (x, y, 1.9), K['limestone'], (0, 0, k + 90))
    A.to_scene()
    return finalize('lantern_post', 30)


BATCHES = {
    'tower_shell': ('v5_wizard', [('WT01_01_wizard_tower_shell', tower_shell)]),
    'tower_porch': ('v5_wizard', [('WT12_01_wizard_door_porch', door_porch), ('WT11_01_wizard_armillary_crown', armillary_crown)]),
    'tower_terrace': ('v5_wizard', [
        ('WT13_01_plateau_terrace_set_01', terrace_wall_straight), ('WT13_02_plateau_terrace_set_02', terrace_wall_curved),
        ('WT13_03_plateau_terrace_set_03', terrace_stair), ('WT13_04_plateau_terrace_set_04', prayer_flag_pole),
        ('WT13_05_plateau_terrace_set_05', cairn), ('WT13_06_plateau_terrace_set_06', lantern_post)]),
}
