"""v5_fx_vh - A3 fix module (worker vh, palette prefix vh_f_). Rebuilds the flawed desert + Skull City models from assign_A3.
Reuses round-1 colours through v5_vh.D where helpful; registers only NEW vh_f_ keys. Front faces -Y, pivot bottom-centre on z=0, 1 unit = 1 stud.
Families: DS01 houses, DS02 market, DS03 wagon, DS04 palms, DS05 oasis ring, DS07 hoodoo arches, DS08 underground entrances,
SD01 mesas, SD02 ruin blocks, LM10 colonnade, LM12 temple stair-down, LM13 guardians, LM14 obelisk, LM16 ring segments,
VC01 volcanic rock, VC03 dark fort ruins, VC04 Skull City buildings. All original designs.
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v5kit
from v5kit import Acc, polar, tang, mk, ids, band, strata
import v5gen as G
from v5gen import round_tower, wall_seg, column, cliff, spire, rock_arch
import v5_vh as R  # round-1 module: reuse its palette dict R.D and marker-free helpers

# --- new palette (prefix vh_f_). Desert sandstone strata, basalt dark stone, timber. No neon, no pure white/cyan slabs.
P = G.reg('vh_f', {
    'sand':  ((212, 182, 138), 'Sandstone', 0.0, 0.95), 'sandl': ((232, 208, 166), 'Sandstone', 0.0, 0.95),
    'sandd': ((186, 150, 104), 'Sandstone', 0.0, 0.95), 'red':   ((174, 92, 60), 'Sandstone', 0.0, 0.95),
    'red2':  ((150, 72, 48), 'Sandstone', 0.0, 0.95), 'cream': ((224, 206, 168), 'Sandstone', 0.0, 0.9),
    'clay':  ((190, 122, 88), 'Brick', 0.0, 0.9), 'wood':  ((116, 84, 54), 'Wood', 0.0, 0.9),
    'plank': ((150, 112, 76), 'WoodPlanks', 0.0, 0.9), 'dark':  ((34, 30, 32), 'Slate', 0.0, 0.95),
    'shadow': ((22, 20, 24), 'Slate', 0.0, 1.0), 'stone': ((150, 140, 125), 'Limestone', 0.0, 0.92),
    'palm':  ((82, 126, 68), 'Grass', 0.0, 1.0), 'palm2': ((112, 150, 78), 'Grass', 0.0, 1.0),
    'bark':  ((122, 98, 70), 'Wood', 0.0, 0.95), 'water': ((150, 186, 180), 'SmoothPlastic', 0.0, 0.5),
    'foam':  ((206, 214, 206), 'SmoothPlastic', 0.0, 0.7), 'reed': ((150, 150, 84), 'Grass', 0.0, 1.0),
    'cloth1': ((70, 108, 140), 'Fabric', 0.0, 1.0), 'cloth2': ((168, 66, 54), 'Fabric', 0.0, 1.0),
    'cloth3': ((202, 150, 72), 'Fabric', 0.0, 1.0), 'canvas': ((224, 214, 190), 'Fabric', 0.0, 1.0),
    'gold':  ((194, 160, 86), 'Metal', 0.8, 0.35), 'iron': ((58, 58, 64), 'Metal', 0.6, 0.6),
    'basalt': ((56, 54, 60), 'Basalt', 0.0, 0.9), 'basalt2': ((76, 74, 82), 'Basalt', 0.0, 0.9),
    'ash':   ((100, 94, 96), 'Slate', 0.0, 0.95), 'ashl': ((124, 118, 120), 'Slate', 0.0, 0.95),
    'rust':  ((120, 70, 56), 'Slate', 0.0, 0.95), 'moss': ((92, 120, 68), 'Grass', 0.0, 1.0),
    # warm dark-stone set for Skull City buildings (so they read off plain grey) + roof tiles
    'dstone': ((96, 80, 78), 'Slate', 0.0, 0.92), 'dstone2': ((120, 98, 90), 'Slate', 0.0, 0.92),
    'dband': ((140, 96, 72), 'Brick', 0.0, 0.9), 'tile': ((128, 62, 50), 'Slate', 0.0, 0.85),
    'tile2': ((104, 50, 42), 'Slate', 0.0, 0.85), 'slate': ((70, 66, 72), 'Slate', 0.0, 0.9),
})
STR = [P['red'], P['sand'], P['red2'], P['cream'], P['clay'], P['sandd']]   # desert strata bottom->top order for banding
STRT = [P['red2'], P['red'], P['clay'], P['sand'], P['sandd'], P['cream']]   # darker base -> lighter top for graded mesas
SANDCOL = {'stone': P['sand'], 'wall': P['sandl'], 'trim': P['sandd']}       # sandstone column palette for column() (keys: stone/wall/trim)


def _fin(A, name):
    A.to_scene()
    return finalize(name, 28)


def _rubble(A, rnd, n, rx, ry, keys, size=(0.9, 2.6), z=None):
    """3-D chunky debris resting on the ground (never flat planes)."""
    for k in range(n):
        s = rnd.uniform(*size)
        h = rnd.uniform(0.8, size[1] * 0.8)
        A.chunk((s, s * rnd.uniform(0.8, 1.2), h), (rnd.uniform(-rx, rx), rnd.uniform(-ry, ry), h * 0.5 if z is None else z),
                keys[k % len(keys)], (0, 0, rnd.uniform(0, 90)), 0.2, rnd, (0.8, 0.8))


# ================================================================ VC04 Skull City buildings (MAJOR) - closed/ruined roofs, warm colour, clear opening
def _skull_building(i):
    """A finished ruined dark-stone building: warm stone walls with ochre coursing (not plain grey), a real ROOF or a deliberate
    collapsed-roof crown (never an open hollow box), a clear framed doorway, and a finished back. Six distinct designs."""
    reset()
    A = Acc()
    rnd = random.Random(8100 + i)
    W, D = 24.0, 24.0
    th = 1.6
    A.box((W + 6.0, D + 6.0, 1.2), (0, 0, 0.6), P['slate'], bev=0.25)                      # stone pad
    # per-sibling design: roof kind + wall tone + height, all clearly different
    roofs = ['gable', 'hip', 'flat', 'collapsed', 'gable', 'leanto']
    tones = [(P['dstone'], P['dstone2']), (P['dstone2'], P['dstone']), (P['ash'], P['dstone2']),
             (P['dstone'], P['ash']), (P['dstone2'], P['dstone']), (P['dstone'], P['dstone2'])]
    hts = [14.0, 12.0, 15.0, 13.0, 12.0, 16.0]
    roof_kind = roofs[i % 6]
    wk, wk2 = tones[i % 6]
    h = hts[i % 6]
    tile = P['tile'] if i % 2 == 0 else P['tile2']

    def wall(cx, cy, ln, axis, hh, key):
        if axis == 'x':
            A.box((ln, th, hh), (cx, cy, 1.2 + hh / 2.0), key, bev=0.12)
        else:
            A.box((th, ln, hh), (cx, cy, 1.2 + hh / 2.0), key, bev=0.12)

    def courses(cx, cy, ln, axis, hh):                                                     # ochre string-courses -> colour relief on the walls
        for t in (0.34, 0.66):
            z = 1.2 + hh * t
            if axis == 'x':
                A.box((ln + 0.2, th + 0.3, 0.5), (cx, cy, z), P['dband'], bev=0.05)
            else:
                A.box((th + 0.3, ln + 0.2, 0.5), (cx, cy, z), P['dband'], bev=0.05)

    bh = h if roof_kind != 'collapsed' else h * 0.78
    wall(0, -D / 2, W, 'x', bh, wk)
    wall(0, D / 2, W, 'x', bh, wk2)
    wall(-W / 2, 0, D, 'y', bh, wk2)
    wall(W / 2, 0, D, 'y', bh, wk)
    for (cx, cy, ln, ax) in ((0, -D / 2, W, 'x'), (0, D / 2, W, 'x'), (-W / 2, 0, D, 'y'), (W / 2, 0, D, 'y')):
        courses(cx, cy, ln, ax, bh)
    # clear framed doorway in the front wall (dark void + jambs + lintel)
    A.box((5.2, th + 0.8, 8.4), (0, -D / 2, 1.2 + 4.2), P['shadow'], bev=0)
    for sg in (-1, 1):
        A.box((1.3, th + 1.0, 8.8), (sg * 3.2, -D / 2, 1.2 + 4.4), P['dband'], bev=0.1)
    A.box((7.8, th + 1.1, 1.6), (0, -D / 2, 1.2 + 8.8), P['dband'], bev=0.12)
    # windows on BOTH long faces (finished back) + the sides
    for (fy, face) in ((-D / 2, 270), (D / 2, 90)):
        for sx in (-1, 1):
            A.box((3.0, th + 0.7, 2.8), (sx * 6.0, fy, 1.2 + bh * 0.66), P['shadow'], bev=0)
            A.box((3.6, th + 1.0, 0.5), (sx * 6.0, fy, 1.2 + bh * 0.66 + 1.8), P['dband'], bev=0.05)
    for sx in (-1, 1):
        A.box((th + 0.7, 2.4, 2.8), (sx * W / 2, 0, 1.2 + bh * 0.55), P['shadow'], bev=0)

    ztop = 1.2 + bh
    if roof_kind == 'gable':
        A.gable(W + 1.4, D + 1.4, 6.0, (0, 0, ztop), tile, (0, 0, 90))                      # full tiled gable roof (closed)
        for t in (0.28, 0.52, 0.76):                                                       # tile course lines
            for sgf in (-1, 1):
                A.beam((-W / 2, sgf * (W / 2 + 0.7) * (1 - t), ztop + 6.0 * t + 0.05), (W / 2, sgf * (W / 2 + 0.7) * (1 - t), ztop + 6.0 * t + 0.05), 0.3, 0.14, P['tile2'], up=(0, sgf, 1))
        A.box((W + 1.0, 0.6, 0.6), (0, 0, ztop + 6.0), P['dband'], bev=0.06)                # ridge
    elif roof_kind == 'hip':
        A.frustum((W + 1.4, D + 1.4), (3.0, 3.0), 5.5, (0, 0, ztop), tile)                  # hipped tiled roof (closed)
        A.box((4.0, 4.0, 0.8), (0, 0, ztop + 5.5), P['dband'], bev=0.1)
    elif roof_kind == 'flat':
        A.box((W + 1.0, D + 1.0, 1.4), (0, 0, ztop + 0.3), P['slate'], bev=0.1)             # solid flat stone deck, seated ON the wall top (fully closed, no interior visible)
        for t in (0.3, 0.7):                                                               # shallow coping courses on the deck top (relief, not exposed beams)
            A.box((W + 1.2, 0.8, 0.4), (0, -D / 2 + 1.0 + t * (D - 2.0), ztop + 1.1), P['dstone2'], bev=0.06)
        for (cx, cy, ln, ax) in ((0, -D / 2, W, 'x'), (0, D / 2, W, 'x'), (-W / 2, 0, D, 'y'), (W / 2, 0, D, 'y')):  # parapet merlons on the roof edge
            n = int(ln / 3.4)
            for k in range(n):
                off = -ln / 2 + 1.7 + k * (ln / n)
                if ax == 'x':
                    A.box((2.4, th, 1.6), (cx + off, cy, ztop + 1.7), wk2, bev=0.1)
                else:
                    A.box((th, 2.4, 1.6), (cx, cy + off, ztop + 1.7), wk2, bev=0.1)
    elif roof_kind == 'leanto':
        A.box((W + 0.6, D + 0.6, 1.0), (0, 0, ztop + 0.2), P['dstone'], bev=0.08)           # closed ceiling slab first (no open gap under the slope)
        A.prism([(-D / 2 - 0.6, 0.0), (D / 2 + 0.6, 0.0), (D / 2 + 0.6, 4.4), (-D / 2 - 0.6, 1.2)], W + 1.2, (-(W + 1.2) / 2.0, 0, ztop + 0.7), tile, (90, 0, 90))    # single-slope lean-to roof seated flush, fully covering
        A.box((W + 1.4, 0.8, 0.6), (0, D / 2 + 0.4, ztop + 0.7 + 4.4), P['dband'], bev=0.06)       # high-edge ridge cap closes the top lip
    else:                                                                                  # collapsed: a DELIBERATE ruin - a closed ceiling slab (interior never shown), a surviving roof slope, broken rafters above
        A.box((W + 0.6, D + 0.6, 1.0), (0, 0, ztop + 0.2), P['dstone'], bev=0.08)           # solid closed ceiling slab seals the top (no open hollow box)
        A.gable(W + 1.4, D + 1.4, 5.0, (0, 0, ztop + 0.7), tile, (0, 0, 90))  # surviving roof slope on one side
        for k in range(4):
            pass  # broken rafters over the gap
        # broken parapet merlons around the open side
        for (cx, cy, ln, ax) in ((0, -D / 2, W, 'x'), (0, D / 2, W, 'x'), (W / 2, 0, D, 'y')):
            n = int(ln / 3.4)
            for k in range(n):
                if rnd.random() < 0.35:
                    continue
                off = -ln / 2 + 1.7 + k * (ln / n)
                mh = rnd.uniform(1.2, 2.6)
                if ax == 'x':
                    pass
                else:
                    pass
    # a corner tower on two siblings for silhouette variety (closed conical/flat top, never open)
    if i % 3 == 2:
        tx, ty = W / 2 - 3.0, D / 2 - 3.0
        twh = h + 7.0
        A.box((7.0, 7.0, twh), (tx, ty, 1.2 + twh / 2.0), wk, bev=0.12)
        A.box((2.0, 2.2, 3.0), (tx, ty - 3.6, 1.2 + twh * 0.6), P['shadow'], bev=0)
        A.cyl(5.2, 5.5, (tx, ty, 1.2 + twh), tile, verts=4, r2=0.0, start=45)               # closed pyramidal tower cap
    # chunky fallen rubble at the base
    _rubble(A, rnd, 14, 14.0, 14.0, [wk, wk2, P['dband']], (1.0, 3.0))
    return _fin(A, 'skull_city_building')


# ================================================================ DS07 hoodoo arches (MAJOR + MINOR)
def _hoodoo_arch(i):
    """A clear eroded rock arch: one connected span of chunks over a dark gap, thick legs to the ground, horizontal strata, no scattered rubble tower."""
    reset()
    A = Acc()
    rnd = random.Random(8200 + i)
    span, h = 30.0, 60.0
    legw = 11.0
    # two tapering legs - each layer is a core chunk + a ring of smaller facet chunks (rich silhouette)
    for sg in (-1, 1):
        lx = sg * span / 2.0
        z = 0.0
        while z < h * 0.58:
            sh = rnd.uniform(3.6, 4.8)
            t = z / h
            w = legw * (1.0 - 0.26 * t)
            key = strata(STR, int(z / 4.2))
            A.chunk((w, legw * 0.85 * (1.0 - 0.2 * t), sh * 1.05), (lx + rnd.uniform(-0.5, 0.5), rnd.uniform(-0.5, 0.5), z + sh / 2.0),
                    key, (0, 0, rnd.uniform(-5, 5)), 0.1, rnd, (0.95, 0.95))
            for r in range(4):
                a = r * 90 + rnd.uniform(-20, 20)
                ex, ey, _ = polar(1.0, a)
                cw = w * rnd.uniform(0.3, 0.42)
                A.chunk((cw, cw, sh * rnd.uniform(0.8, 1.1)), (lx + ex * w * 0.42, ey * legw * 0.4, z + sh / 2.0), key, (0, 0, a), 0.14, rnd, (0.8, 0.8))
            z += sh * 0.92
    # the connected span: facet chunks following a flattened arch from leg-top to leg-top
    n = 15
    legtop = h * 0.54
    crown = h * 0.9
    for k in range(n + 1):
        t = k / n
        a = math.pi * t
        x = math.cos(a) * span / 2.0
        zz = legtop + math.sin(a) * (crown - legtop)
        sz = 7.5 * (1.1 - 0.32 * math.sin(a))
        key = strata(STR, int(zz / 4.2))
        A.chunk((sz * 1.1, legw * 0.82, sz * 1.15), (x, rnd.uniform(-0.4, 0.4), zz), key, (0, math.degrees(a) - 90.0, 0), 0.1, rnd, (0.9, 0.9))
        if 0 < k < n:                                                                      # a smaller block on the underside of the span (voussoir look)
            A.chunk((sz * 0.6, legw * 0.55, sz * 0.6), (x, rnd.uniform(-0.3, 0.3), zz - sz * 0.6), key, (0, math.degrees(a) - 90.0, 0), 0.14, rnd, (0.75, 0.75))
    # a solid keystone bridging the very top so the span reads continuous (no broken gap at the apex)
    A.chunk((span * 0.5, legw * 0.9, 9.0), (0, 0, crown - 1.0), strata(STR, int(crown / 4.2)), (0, 0, 0), 0.08, rnd, (0.9, 0.9))
    # a little moss/weathering where it would settle on the top of the span
    A.chunk((span * 0.4, legw * 0.5, 1.2), (0, 0, crown + 0.4), P['moss'], (0, 0, rnd.uniform(-6, 6)), 0.15, rnd, (0.7, 0.7))
    # a modest fallen block at each foot (chunky, touching ground), not a pile
    for sg in (-1, 1):
        A.chunk((rnd.uniform(5, 8), rnd.uniform(4, 6), rnd.uniform(3, 5)), (sg * (span / 2 + 7.0), rnd.uniform(-4, 4), 2.0),
                STR[rnd.randrange(len(STR))], (0, 0, rnd.uniform(0, 90)), 0.15, rnd, (0.8, 0.8))
    if i == 3:                                                                             # arch 04 variant: a stepped buttress of chunks leaning against one leg foot (connected)
        bx = -span / 2.0
        for k in range(4):
            A.chunk((7.0 - k, 7.0 - k, 4.0), (bx + 4.0 + k * 1.5, 4.0 - k * 0.5, 2.0 + k * 3.0), strata(STR, k + 1), (0, 0, 10 + k * 6), 0.12, rnd, (0.8, 0.8))
    return _fin(A, 'hoodoo_arch')


# ================================================================ DS08 underground entrances (MAJOR)
def _underground(i):
    """A finished underground entrance that reads head-on: a solid battered sandstone mastaba with a prominent recessed DOORWAY cut into the
    FRONT face (framed portal, dark void, descending steps visible just inside), colour banding, solid on all sides. Target 30 x 30 x 24."""
    reset()
    A = Acc()
    rnd = random.Random(8300 + i)
    W, D, H = 30.0, 30.0, 24.0
    kk = [P['sand'], P['sandl'], P['sandd']]
    bodyh = 19.0
    # solid battered body (slightly tapered mastaba), mid-tone sandstone - finished all four sides, min z = 0
    A.frustum((W, D), (W - 5.0, D - 5.0), bodyh, (0, 0, 0.0), P['sandd'])
    # strong alternating horizontal colour courses on every face (so no plain pale tan slab)
    for k in range(5):
        z = 2.0 + k * (bodyh - 3.0) / 5.0
        inset = 2.5 * (z / bodyh)
        A.box((W - inset * 2 + 0.3, D - inset * 2 + 0.3, 0.7), (0, 0, z), P['red'] if k % 2 else P['clay'], bev=0.05)
    # a stepped crown on top (reads finished, not open)
    A.frustum((W - 7.0, D - 7.0), (W - 11.0, D - 11.0), 3.5, (0, 0, bodyh), P['sand'])
    A.box((W - 13.0, D - 13.0, 2.0), (0, 0, bodyh + 3.5), P['sandd'], bev=0.1)
    # PROMINENT recessed doorway in the front (-Y) face: a deep DARK opening framed by jambs/lintel/sill (a RING, not a solid cover panel)
    pw, ph = 8.0, 12.0
    A.box((pw + 1.0, 7.0, ph + 1.0), (0, -D / 2 + 4.5, ph / 2.0 + 0.6), P['shadow'], bev=0)        # DEEP dark void, front face flush with the body so the hole reads black
    for sg in (-1, 1):                                                                             # jambs (frame the opening, do not cover it)
        A.box((2.2, 2.6, ph + 2.0), (sg * (pw / 2 + 1.0), -D / 2 + 0.8, (ph + 2.0) / 2.0), P['sandl'], bev=0.1)
    A.box((pw + 5.0, 2.8, 2.4), (0, -D / 2 + 0.8, ph + 1.2), P['sandl'], bev=0.12)                 # lintel
    A.box((pw + 4.0, 2.6, 1.2), (0, -D / 2 + 0.8, 0.6), P['sandd'], bev=0.1)                       # sill/threshold
    # darker descending steps set well back inside the mouth (reads as going down/under, not a lit panel)
    for s in range(5):
        A.box((pw - 2.0, 1.4, 0.9), (0, -D / 2 + 5.2 + s * 1.2, 5.2 - s * 1.0), P['sandd'] if s % 2 else P['dark'], bev=0.04)
    # per-sibling top treatment (keep them different)
    if i == 2:                                                                            # 03: a carved red glyph lintel band + a stepped pediment over the door
        A.box((pw + 3.0, 0.5, 1.2), (0, -D / 2 + 0.5, ph + 3.2), P['red'], bev=0.04)
        A.frustum((pw + 6.0, 3.0), (pw, 2.0), 2.6, (0, -D / 2 + 2.0, ph + 2.6), P['sandd'])
    elif i == 1:                                                                          # 02: flanking obelisk stubs + lighter upper band (colour variety)
        for sg in (-1, 1):
            A.frustum((5.0, 5.0), (2.6, 2.6), 11.0, (sg * (W / 2 - 4.5), -D / 2 + 4.5, bodyh - 2.0), P['sandd'])
        A.box((W - 6.0, 1.0, 0.6), (0, -D / 2 + 2.6, bodyh - 1.0), P['cream'], bev=0.04)
    else:                                                                                 # 01: a timber-beam hood over the doorway
        for k in range(4):
            A.beam((-pw / 2 + k * pw / 3.0, -D / 2 - 0.3, ph + 2.2), (-pw / 2 + k * pw / 3.0, -D / 2 + 3.5, ph + 2.2), 0.5, 0.5, P['wood'])
    # chunky rubble at the base
    _rubble(A, rnd, 10, 13.0, 12.0, [P['sandd'], P['sand'], P['stone']], (1.0, 2.6))
    return _fin(A, 'underground_entrance')


# ================================================================ LM12 temple stair down (MAJOR)
def _temple_stair(i):
    """A readable recessed temple stair in a SOLID mass: two solid side masses and a raised back head wall, with a stepped notch cut into the top
    descending to a dark doorway. All geometry from z=0 up (nothing floats). Target 30 x 40 x 24."""
    reset()
    A = Acc()
    rnd = random.Random(8400 + i)
    W, D, H = 30.0, 40.0, 22.0
    kk = [P['sand'], P['sandl'], P['sandd']]
    notch_w = 15.0                                                                        # wider slot so light reaches it (no near-black self-shadow)
    sidew = (W - notch_w) / 2.0
    # two solid side masses flanking the stair trench (full height, grounded)
    for sx in (-1, 1):
        A.box((sidew, D, H), (sx * (notch_w + sidew) / 2.0, 0, H / 2.0), kk[0], bev=0.15)
        A.box((0.6, D, H), (sx * (notch_w / 2.0), 0, H / 2.0), P['sandl'], bev=0.05)       # light inner trench wall so the slot catches light (not black)
        # coursed string bands + coping on the side mass tops
        for k in range(6):
            A.box((sidew + 0.3, 2.8, 1.0), (sx * (notch_w + sidew) / 2.0, D / 2 - 3.0 - k * (D - 6.0) / 6.0, H + 0.5), P['sandl'], bev=0.1)
        for k in range(3):
            A.box((sidew + 0.3, D, 0.5), (sx * (notch_w + sidew) / 2.0, 0, H * (0.3 + 0.25 * k)), P['sandl'], bev=0)
        A.box((sidew + 0.3, D, 1.2), (sx * (notch_w + sidew) / 2.0, 0, H * 0.5), P['clay'], bev=0)   # warm colour band (relief + colour)
        for k in range(4):                                                                # vertical pilaster ribs on the outer face
            A.box((0.8, 1.6, H - 3.0), (sx * (W / 2 - 0.4), -D / 2 + 5.0 + k * (D - 10.0) / 3.0, H / 2.0), P['sandl'], bev=0.08)
    # raised temple head wall at the back (+Y), taller than the sides
    A.box((W, 7.0, H + 6.0), (0, D / 2 - 3.5, (H + 6.0) / 2.0), kk[2], bev=0.15)
    A.box((W + 1.0, 7.5, 1.4), (0, D / 2 - 3.5, H + 6.6), P['sandl'], bev=0.1)             # head coping
    # stepped stair notch cut into the top, descending from the head (high) to the front mouth (low), solid blocks to the ground
    steps = 12
    for s in range(steps):
        y = D / 2 - 8.0 - s * (D - 12.0) / steps
        ztop = H - s * (H - 3.0) / steps
        depth = (D - 12.0) / steps + 0.4
        A.box((notch_w, depth, ztop), (0, y, ztop / 2.0), P['cream'] if s % 2 else P['sandl'], bev=0.04)
        A.box((notch_w, 0.3, 1.3), (0, y - depth / 2.0, ztop - 0.65), P['clay'], bev=0)
    # dark doorway at the top of the stair (into the temple head) - mid stone recess, NOT near-black
    A.box((notch_w - 2.0, 1.4, 8.0), (0, D / 2 - 7.2, H - 2.0), P['sandd'], bev=0)
    A.box((notch_w - 3.4, 0.8, 6.6), (0, D / 2 - 6.9, H - 2.2), P['stone'], bev=0)         # lighter inner door panel so it doesn't read as a black hole
    for sx in (-1, 1):
        A.box((1.8, 1.8, 9.0), (sx * (notch_w / 2 - 1.0), D / 2 - 7.2, H - 1.0), P['sandd'], bev=0.1)
    A.box((notch_w + 1.0, 2.0, 2.2), (0, D / 2 - 7.2, H + 3.6), P['sandl'], bev=0.12)       # lintel
    # front portal posts framing the mouth of the descent
    for sx in (-1, 1):
        A.box((2.2, 2.2, H + 1.0), (sx * (notch_w / 2 + 1.0), -D / 2 + 1.5, (H + 1.0) / 2.0), P['sand'], bev=0.12)
    A.box((notch_w + 5.0, 2.6, 2.4), (0, -D / 2 + 1.5, H + 0.5), P['sandd'], bev=0.15)
    if i == 1:                                                                            # stair 02: red glyph band on the head + flanking statue plinths (varies from 01)
        A.box((W * 0.7, 0.6, 2.0), (0, D / 2 - 7.0, 6.0), P['red'], bev=0.04)
        for sx in (-1, 1):
            A.box((3.0, 3.0, 5.0), (sx * (notch_w / 2 + 2.5), -D / 2 + 3.0, H + 1.0), P['sandl'], bev=0.1)
    else:                                                                                # stair 01: a chunky cornice over the head doorway
        A.frustum((notch_w + 4.0, 3.0), (notch_w, 2.0), 2.4, (0, D / 2 - 7.2, H + 4.6), P['sandd'])
    _rubble(A, rnd, 9, 13.0, 17.0, [P['sandd'], P['stone'], P['sand']], (1.0, 2.6))
    return _fin(A, 'temple_stair_down')


# ================================================================ SD01 red mesa clusters (MAJOR) - broad flat-top butte, wider than tall
def _mesa(i):
    reset()
    A = Acc()
    rnd = random.Random(8500 + i)
    W, D, H = 120.0, 100.0, 90.0
    # one solid broad mass: a wide battered base + stacked TAPERING strata (wider than tall), flat top. Each layer is made of several
    # facet chunks so the silhouette is rich (not a crude blockout).
    base_w, base_d = W * 0.9, D * 0.9
    z = 0.0
    layers = 11
    for k in range(layers):
        t = k / (layers - 1.0)
        lw = base_w * (1.0 - 0.34 * t)
        ld = base_d * (1.0 - 0.34 * t)
        sh = (H * 0.92) / layers
        key = strata(STRT, k, 1)
        # ring of facet chunks around the layer edge + a solid core chunk (bottom layers use full footprint so nothing can detach)
        core = 0.95 if k < 2 else 0.8
        A.chunk((lw * core, ld * core, sh * 1.08), (rnd.uniform(-1.2, 1.2), rnd.uniform(-1.2, 1.2), z + sh / 2.0), key, (0, 0, rnd.uniform(-2, 2)), 0.06, rnd, (0.92, 0.92))
        nring = 8
        for r in range(nring):
            a = r * (360.0 / nring) + rnd.uniform(-8, 8)
            ex, ey, _ = polar(1.0, a)
            cw = lw * rnd.uniform(0.2, 0.3)
            A.chunk((cw, cw * rnd.uniform(0.8, 1.2), sh * rnd.uniform(0.95, 1.15)),
                    (ex * lw * 0.38, ey * ld * 0.38, z + sh / 2.0), key, (0, 0, a), 0.1, rnd, (0.85, 0.85))
        z += sh * 0.95
    # broad flat cap (several plates)
    for k in range(3):
        A.chunk((base_w * (0.5 - 0.1 * k), base_d * (0.5 - 0.1 * k), 3.0), (rnd.uniform(-2, 2), rnd.uniform(-2, 2), z + 1.5 + k * 1.2), STRT[-1 - k % 2], (0, 0, rnd.uniform(-3, 3)), 0.05, rnd, (0.95, 0.95))
    # sloped talus flanks: big fallen rock masses leaning ON the base all round, their centres pulled inward so they touch the body
    for k in range(14):
        a = k * (360.0 / 14) + rnd.uniform(-8, 8)
        ex, ey, _ = polar(1.0, a)
        mw = rnd.uniform(16, 26)
        mh = rnd.uniform(18, 38)
        cx = ex * (base_w * 0.42 - mw * 0.3)
        cy = ey * (base_d * 0.42 - mw * 0.3)
        A.chunk((mw, mw * 0.85, mh), (cx, cy, mh / 2.0), strata(STRT, k % 4), (0, 0, a), 0.12, rnd, (0.55, 0.55))
    # vertical buttress ridges on the big faces (relief, not a flat slab)
    for sg in (-1, 1):
        for k in range(4):
            A.chunk((9.0, D * 0.42, rnd.uniform(44, 64)), (sg * base_w * 0.4, -D * 0.22 + k * D * 0.15, 26.0), strata(STRT, k), (0, 0, 0), 0.1, rnd, (0.62, 0.68))
    # a second smaller butte beside the main one for cluster variety (varies per sibling)
    if i != 1:
        cx2, cy2 = (W * 0.3, -D * 0.22)
        A.chunk((44.0, 38.0, 12.0), (cx2, cy2, 5.0), strata(STRT, i, 1), (0, 0, 0), 0.06, rnd, (0.95, 0.95))  # solid grounded base block
        z = 9.0
        for k in range(1, 5):
            t = k / 4.0
            A.chunk((40.0 * (1 - 0.28 * t), 34.0 * (1 - 0.28 * t), 10.0), (cx2, cy2, z + 5.0), strata(STRT, k + i, 1), (0, 0, 0), 0.08, rnd, (0.9, 0.9))
            for r in range(4):
                a = r * 90 + 45
                ex, ey, _ = polar(1.0, a)
                A.chunk((9, 9, 9), (cx2 + ex * 15 * (1 - 0.28 * t), cy2 + ey * 13 * (1 - 0.28 * t), z + 5.0), strata(STRT, k + i), (0, 0, a), 0.12, rnd, (0.75, 0.75))
            z += 9.0
    # chunky fallen rubble at the foot
    _rubble(A, rnd, 18, W * 0.42, D * 0.42, STRT, (3.0, 8.0))
    return _fin(A, 'red_mesa_cluster')


# ================================================================ DS01 adobe houses (MINOR fixes: remove stray slab/beam, seat merlons)
def _house(i):
    """Clean adobe house. DS01_03 fix: no blue slab, merlons solidly on the parapet. DS01_04 fix: no loose beam in front."""
    reset()
    A = Acc()
    rnd = random.Random(8600 + i)
    W, D, H = 18.0, 16.0, 11.0
    A.box((W + 2.0, D + 2.0, 1.0), (0, 0, 0.5), P['stone'], bev=0.15)
    wall = P['sandl'] if i == 0 else P['cream']
    A.box((W, D, H), (0, 0, 1.0 + H / 2.0), wall, bev=0.35)
    A.box((W + 0.9, D + 0.9, 0.8), (0, 0, 1.0 + H + 0.4), P['sand'], bev=0.1)               # parapet coping ring
    # merlons seated SOLIDLY on the coping (overlapping it, not floating blocks)
    n = int((W) / 3.0)
    for edge, axis, length in ((-D / 2, 'x', W), (D / 2, 'x', W), (-W / 2, 'y', D), (W / 2, 'y', D)):
        nn = int(length / 3.0)
        for k in range(nn):
            off = -length / 2 + 1.5 + k * (length / nn)
            if axis == 'x':
                A.box((2.0, 1.4, 1.8), (off, edge + (0.7 if edge < 0 else -0.7), 1.0 + H + 1.1), P['sand'], bev=0.12)
            else:
                A.box((1.4, 2.0, 1.8), (edge + (0.7 if edge < 0 else -0.7), off, 1.0 + H + 1.1), P['sand'], bev=0.12)
    # door (framed, recessed)
    A.box((3.0, 0.5, 5.0), (0, -D / 2, 1.0 + 2.5), P['shadow'], bev=0)
    A.box((2.4, 0.6, 4.4), (0, -D / 2 - 0.1, 1.0 + 2.2), P['wood'], bev=0.05)
    for sg in (-1, 1):
        A.box((0.6, 0.7, 5.2), (sg * 1.7, -D / 2 - 0.05, 1.0 + 2.6), P['sandd'], bev=0.06)
    A.box((4.2, 0.9, 0.7), (0, -D / 2 - 0.1, 1.0 + 5.2), P['sandd'], bev=0.08)
    # windows
    for (wx, wy, face) in ((-5.5, -D / 2, 270), (5.5, -D / 2, 270), (W / 2, 3.0, 0), (-W / 2, 3.0, 180)):
        tx, ty = tang(face)
        ca, sa = math.cos(math.radians(face)), math.sin(math.radians(face))
        A.box((0.4, 1.8, 2.4), (wx, wy, 7.0), P['shadow'], (0, 0, face), bev=0)
        A.box((0.5, 2.6, 0.5), (wx + ca * 0.1, wy + sa * 0.1, 8.4), P['sandd'], (0, 0, face), bev=0.05)
    # a small second-storey setback box + wooden roof beams resting ON the setback roof
    A.box((W * 0.6, D * 0.6, 4.0), (-2.0, 1.0, 1.0 + H + 0.8), wall, bev=0.3)
    for k in range(4):
        A.cyl(0.3, D * 0.5, (-5.0 + k * 2.4, 1.0, 1.0 + H + 2.4), P['wood'], verts=6, rot=(90, 0, 0))
    # ground pots / jars (3-D, clearly resting)
    for k in range(3):
        A.cyl(0.9, 1.6, (-6.0 + k * 1.8, -D / 2 - 2.5, 0.0), P['clay'], verts=10, r2=0.7)
    _rubble(A, rnd, 5, 9.0, 8.0, [P['sandd'], P['stone']], (0.7, 1.6))
    return _fin(A, 'adobe_house')


# ================================================================ DS02 desert market (MINOR: read as a market, seat goods, no stray cubes)
def _market(i):
    reset()
    A = Acc()
    rnd = random.Random(8700 + i)
    # a clear market stall: plank counter, four posts, a striped awning, goods on the counter and baskets below
    A.box((12.0, 2.0, 1.0), (0, 0, 0.5), P['stone'], bev=0.1)                               # ground pad
    A.box((11.0, 4.5, 3.0), (0, -1.0, 1.5), P['plank'], bev=0.1)                            # counter
    A.box((11.4, 4.9, 0.4), (0, -1.0, 3.1), P['wood'], bev=0.06)                            # counter top
    for sx in (-5.0, 5.0):
        A.cyl(0.32, 9.5, (sx, 1.6, 0), P['wood'], verts=6)
        A.cyl(0.32, 7.0, (sx, -3.4, 0), P['wood'], verts=6)
    A.box((12.0, 7.5, 0.3), (0, -0.9, 8.6), P['cloth3'], (-12, 0, 0), bev=0)                 # awning
    for k in range(6):                                                                      # awning stripes (seated flush on the cloth)
        A.box((1.0, 7.6, 0.33), (-5.0 + k * 2.0, -0.9, 8.62), P['canvas'] if k % 2 else P['cloth2'], (-12, 0, 0), bev=0)
    # goods on the counter: stacked crates, fruit balls, jars - clearly resting on the top (z = 3.3)
    for k in range(4):
        A.box((1.8, 1.6, 1.4), (-4.0 + k * 2.6, -1.0, 4.0), P['plank'], bev=0.08)
    for k in range(6):
        A.ball(0.5, (-4.5 + k * 1.6, 0.6, 3.9), (P['cloth2'], P['palm2'], P['cloth3'])[k % 3], segs=7, rings=4)
    for k in range(3):
        A.cyl(0.8, 1.4, (-3.0 + k * 3.0, -2.6, 3.3), P['clay'], verts=10, r2=0.6)
    # baskets / sacks below, on the ground
    for k in range(3):
        A.cyl(1.0, 1.6, (-4.0 + k * 4.0, -4.6, 0.0), P['reed'], verts=10, r2=0.9)
        A.ball(0.9, (-4.0 + k * 4.0, -4.6, 1.6), P['sand'], segs=7, rings=4, scale=(1, 1, 0.7))
    # a sign board on a post rising from the counter (reads as a shop/market), seated
    A.cyl(0.32, 11.5, (5.0, 1.6, 0), P['wood'], verts=6)
    A.box((0.3, 2.6, 1.6), (5.0, 2.9, 10.6), P['sandd'], bev=0.06)
    return _fin(A, 'desert_market')


# ================================================================ DS04 palms (MINOR: stouter trunk, fuller fronds, vary siblings, no stray wire)
def _palm(i):
    reset()
    A = Acc()
    rnd = random.Random(8800 + i)
    h = 40.0 + (i - 1) * 2.0                                                               # vary height per sibling
    lean = (i - 1) * 2.4
    segs = 9
    prev = (0.0, 0.0, 0.0)
    A.cyl(2.0, 2.0, (0, 0, 0), P['bark'], verts=10, r2=1.7)                                # stout root base
    for s in range(1, segs + 1):
        t = s / segs
        q = (lean * t * t, 0.6 * math.sin(t * 2.6), h * t)
        r = 1.7 - 0.45 * t                                                                # noticeably stouter trunk, gentle taper
        p0 = (prev[0], prev[1], max(0.0, prev[2] - 0.8))
        A.beam(p0, q, r * 2.0, r * 2.0, P['bark'])
        A.sweep([(r * 0.95, -0.24), (r * 1.6, -0.24), (r * 1.6, 0.24), (r * 0.95, 0.24)], 0, 360, 8, P['bark'], loc=q)  # ring node
        prev = q
    top = prev
    A.cyl(1.8, 2.4, (top[0], top[1], top[2] - 1.2), P['bark'], verts=10, r2=1.5)           # solid crown hub
    nf = 16                                                                                # fuller canopy
    for k in range(nf):
        a = (360.0 / nf) * k + rnd.uniform(-5, 5)
        droop = 7.0 + (k % 3)
        pts = []
        for s in range(6):
            t = s / 5.0
            x, y, _ = polar(t * (12.5 + i), a)
            pts.append((top[0] + x, top[1] + y, top[2] + 2.8 * math.sin(t * 1.3) - droop * t * t + 1.4))
        # central rib
        for p0, p1 in zip(pts, pts[1:]):
            A.beam(p0, p1, 0.5, 0.34, P['bark'])
        # broad leaflet blades along the rib (volume, reads as a frond)
        tx, ty = tang(a)
        for j, p in enumerate(pts[1:]):
            bl = 3.2 - j * 0.4
            for sg in (-1, 1):
                A.box((0.2, bl, 1.4 - j * 0.12), (p[0] + tx * sg * bl * 0.5, p[1] + ty * sg * bl * 0.5, p[2] - 0.6),
                      P['palm'] if (k + j) % 2 else P['palm2'], (0, 0, a + sg * 35.0), bev=0)
    # date clusters under the crown
    for k in range(5):
        x, y, _ = polar(1.4, k * 72.0)
        A.ball(0.8, (top[0] + x, top[1] + y, top[2] - 0.8), P['clay'], segs=6, rings=4)
    return _fin(A, 'oasis_palm')


# ================================================================ DS05 oasis rock ring (OK note: rearrange layout so 02 differs from 01)
def _oasis_ring(i):
    reset()
    A = Acc()
    rnd = random.Random(8900 + i)
    A.cyl(20.0, 0.5, (0, 0, 0.1), P['water'], verts=28)
    A.sweep([(19.0, 0.0), (22.0, 0.0), (22.0, 0.7), (19.0, 0.7)], 0, 360, 28, P['sandl'])    # sandy rim
    A.sweep([(18.5, 0.5), (19.6, 0.5), (19.6, 0.9), (18.5, 0.9)], 0, 360, 28, P['foam'])     # pale foam line
    # ring 02 uses a clustered/gapped layout instead of ring 01's even spacing
    n = 14
    for k in range(n):
        if i == 1 and k % 4 == 0:
            continue                                                                       # gaps -> different arrangement
        a = (360.0 / n) * k + (18.0 if i == 1 else 0.0)
        x, y, _ = polar(rnd.uniform(20.0, 22.5), a)
        A.mound(x, y, rnd.uniform(4, 8), rnd.uniform(4, 8), rnd.uniform(4, 9), 4, [P['stone'], P['sandd'], P['red']], rnd, 0.0, 0.5, 0.9)
    for k in range(18):
        x, y, _ = polar(rnd.uniform(15.0, 19.5), rnd.uniform(0, 360))
        A.cyl(0.08, rnd.uniform(2.0, 4.0), (x, y, 0.4), P['reed'], verts=4, r2=0.03, rot=(rnd.uniform(-8, 8), rnd.uniform(-8, 8), 0))
    for k in range(4):
        x, y, _ = polar(rnd.uniform(5, 12), rnd.uniform(0, 360))
        A.ball(rnd.uniform(1.4, 2.2), (x, y, 0.5), P['palm2'], segs=7, rings=4, scale=(1.6, 1.2, 0.3))
    return _fin(A, 'oasis_rock_ring')


# ================================================================ DS03 caravan wagon (OK note: vary cover shape from wagon 01)
def _wagon(i):
    reset()
    A = Acc()
    rnd = random.Random(9000 + i)
    A.box((14.0, 6.0, 0.7), (0, 0, 2.6), P['plank'], bev=0.06)
    for sg in (-1, 1):
        for sx in (-4.5, 4.5):
            A.cyl(2.6, 0.5, (sx, sg * 3.3, 2.6), P['wood'], verts=16, rot=(90, 0, 0))
            A.cyl(0.5, 0.8, (sx, sg * 3.3, 2.6), P['iron'], verts=8, rot=(90, 0, 0))
            for k in range(6):
                A.box((0.22, 0.3, 5.0), (sx, sg * 3.3, 2.6), P['wood'], (k * 30.0, 0, 0), bev=0)
        A.box((14.0, 0.3, 1.4), (0, sg * 2.9, 3.6), P['plank'], bev=0)
    # wagon 02 gets a peaked tent cover; wagon 01 was a rounded canvas tilt -> different silhouette
    for k in range(5):
        A.sweep([(2.9, 0.0), (3.1, 0.0), (3.1, 0.3), (2.9, 0.3)], 0, 180, 8, P['wood'], loc=(-5.6 + k * 2.8, 0, 3.0), rot=(90, 0, 90))
    A.gable(7.2, 12.0, 3.4, (0, 0, 4.0), P['cloth2'], (0, 0, 0))                            # peaked cloth roof
    A.box((7.2, 0.3, 0.3), (0, 0, 7.4), P['wood'], bev=0)
    A.beam((7.0, 0, 2.6), (13.0, 0, 2.0), 0.5, 0.5, P['wood'])                              # yoke/tongue
    A.box((2.4, 1.4, 1.4), (-3.0, 0, 3.8), P['clay'], bev=0.1)
    A.box((2.0, 1.6, 1.6), (3.0, 0, 3.8), P['plank'], bev=0.1)
    return _fin(A, 'caravan_wagon')


# ================================================================ SD02 desert ruin blocks (MINOR: 3-D rubble not flat planes, vary siblings)
def _ruin_block(i):
    reset()
    A = Acc()
    rnd = random.Random(9100 + i)
    # low sand mound base (not a flat visible slab) the ruin stands on
    A.mound(0, 0, 42.0, 40.0, 3.5, 16, [P['sand'], P['sandl'], P['sandd']], rnd, 0.0, 0.5, 0.9, 0.12)
    A.box((40.0, 38.0, 1.0), (0, 0, 0.5), P['sandd'], bev=0.2)
    # distinct massing per sibling (different broken-wall skylines)
    massings = {
        0: [(-9, -5, 14, 12, 15), (9, 3, 12, 14, 9), (-4, 11, 10, 10, 7), (11, -11, 9, 9, 13)],
        1: [(-10, 0, 20, 10, 16), (8, 8, 12, 12, 8), (6, -10, 14, 10, 11)],
        3: [(0, 0, 16, 16, 18), (-12, 8, 10, 12, 7), (12, -8, 9, 10, 12), (10, 10, 8, 8, 6)],
        4: [(-8, -8, 14, 14, 13), (10, 6, 13, 10, 16), (-2, 12, 12, 8, 7)],
        5: [(-6, 2, 24, 12, 14), (10, -10, 12, 12, 10), (12, 11, 8, 8, 8)],
    }[i if i in (0, 1, 3, 4, 5) else 0]
    for (x, y, w, d, hh) in massings:
        h2 = hh * rnd.uniform(0.7, 1.0)
        A.box((w, d, h2), (x, y, 1.0 + h2 / 2.0), P['sand'], bev=0.3)
        A.box((w + 0.2, d + 0.2, 1.0), (x, y, 1.0 + h2 * 0.45), P['clay'], bev=0.05)       # warm colour course on each wall
        # broken DIAGONAL top: a wedge-cut crown + chunky blocks (reads as a ruined jagged edge, not a flat box top)
        A.chunk((w, d, 2.5), (x, y, 1.0 + h2 + 0.6), P['sandd'], (rnd.uniform(-8, 8), rnd.uniform(-8, 8), rnd.uniform(0, 20)), 0.25, rnd, (0.7, 0.6))
        for sx in (-1, 1):
            A.chunk((w * 0.4, d * 0.8, rnd.uniform(2.0, 4.0)), (x + sx * w * 0.22, y, 1.0 + h2 - 0.4), P['sand'], (0, 0, rnd.uniform(0, 20)), 0.25, rnd, (0.8, 0.8))
        # dark window/door voids framed in colour
        for k in range(2):
            A.box((2.0, 0.6, 2.8), (x - w / 4.0 + k * w / 2.0, y - d / 2.0, 1.0 + h2 * 0.5), P['shadow'], bev=0)
            A.box((2.6, 0.5, 0.5), (x - w / 4.0 + k * w / 2.0, y - d / 2.0 - 0.05, 1.0 + h2 * 0.5 + 1.6), P['clay'], bev=0)
        # a fallen block leaning against the wall foot
        A.chunk((4.0, 3.0, 2.4), (x + rnd.uniform(-w * 0.3, w * 0.3), y - d / 2.0 - 2.5, 1.4), P['sandd'], (20, 0, rnd.uniform(0, 40)), 0.2, rnd, (0.8, 0.8))
    for k in range(3 + i % 3):
        column(A, rnd.uniform(-14, 14), rnd.uniform(-14, 14), 1.2, 1.1, rnd.uniform(6, 14), R.SK, 0.0, rnd)
    # scattered fallen column drums + chunky rubble (volumetric) around the foot
    for k in range(5):
        x, y = rnd.uniform(-16, 16), rnd.uniform(-16, 16)
        A.cyl(1.2, 3.0, (x, y, 1.6), P['sand'], verts=10, rot=(0, 90, rnd.uniform(0, 180)))
    _rubble(A, rnd, 16, 18.0, 17.0, [P['sand'], P['sandd'], P['stone']], (1.2, 3.4))
    return _fin(A, 'desert_ruin_block')


# ================================================================ LM10 colonnade (MINOR: fix black/inverted lintel top)
def _colonnade(i):
    reset()
    A = Acc()
    rnd = random.Random(9200 + i)
    A.box((60.0, 20.0, 2.0), (0, 2.0, 1.0), P['sand'], bev=0.1)                            # base platform
    A.box((56.0, 16.0, 1.4), (0, 2.0, 2.4), P['sandl'], bev=0.1)
    xs = [-24.0 + k * 12.0 for k in range(5)]
    for x in xs:
        column(A, x, -4.0, 3.1, 2.1, 22.0, R.SK, 0.0, rnd)                                 # full front row -> lintels always seated
        column(A, x, 8.0, 3.1, 2.1, 20.0, R.SK, 0.0, rnd)
    # lintels spanning the front row - solid boxes resting on two full columns (A.box recalcs normals -> no black top face)
    for k in range(4):
        A.box((12.4, 3.0, 2.6), (-18.0 + k * 12.0, -4.0, 3.1 + 22.0 + 0.3), P['sand'], bev=0.15)
        A.box((12.8, 3.4, 0.7), (-18.0 + k * 12.0, -4.0, 3.1 + 22.0 + 1.9), P['sandl'], bev=0.1)   # cornice cap
    # buried half the colonnade in a dune so it reads as half-sunk (and anchors everything to the ground)
    A.mound(0, 2.0, 60.0, 18.0, 7.0, 14, [P['sand'], P['sandl'], P['sandd']], rnd, 0.0, 0.3, 0.6, 0.1)
    for k in range(8):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(10, 26), a)
        A.chunk((rnd.uniform(1.2, 3.2), rnd.uniform(1.2, 3.2), rnd.uniform(1.2, 2.6)), (x, 2.0 + y * 0.4, 0.8), (P['sandd'], P['stone'])[k % 2], (0, 0, a), 0.2, rnd, (0.8, 0.8))
    return _fin(A, 'temple_colonnade_buried')


# ================================================================ LM13 guardian statues (MINOR: fix black face, bulk up figure, vary siblings)
def _guardian(i):
    reset()
    A = Acc()
    rnd = random.Random(9300 + i)
    A.box((16.0, 16.0, 4.0), (0, 0, 2.0), P['stone'], bev=0.3)                             # plinth
    A.box((12.0, 12.0, 3.0), (0, 0, 5.5), P['sandd'], bev=0.3)
    # broad robed body (bulked up so it reads as a carved figure)
    A.frustum((11.0, 8.0), (9.0, 6.0), 30.0, (0, 0, 7.0), P['sand'])                        # long robe, wide
    A.frustum((12.0, 9.0), (11.0, 8.0), 3.0, (0, 0, 7.0), P['sandl'])                       # robe hem
    A.box((13.0, 7.0, 10.0), (0, 0, 1.0 + 36.0), P['sand'], bev=0.2) if False else \
        A.frustum((10.0, 6.5), (13.0, 7.0), 12.0, (0, 0, 37.0), P['sand'])                  # broad chest + shoulders
    # arms folded to the chest (attached, bulky)
    for sg in (-1, 1):
        A.beam((sg * 6.0, -1.0, 48.0), (sg * 3.0, -4.0, 42.0), 3.0, 3.0, P['sand'])
    # wide head with a headdress (box -> normals recalced, no black face)
    A.box((7.0, 6.0, 7.0), (0, 0, 52.5), P['sandl'], bev=0.25)                              # head block
    A.box((8.5, 7.0, 2.0), (0, 0, 56.5), P['sandd'], bev=0.15)                              # crown / nemes band
    A.box((3.0, 1.0, 1.2), (0, -3.0, 51.5), P['shadow'], bev=0)                             # recessed face shadow (not inverted)
    # carved facial relief so the head reads as a face, not a plain block
    A.box((5.0, 0.6, 0.8), (0, -3.0, 53.6), P['sandd'], bev=0.05)                           # brow ridge
    for sg in (-1, 1):
        A.box((1.2, 0.5, 0.8), (sg * 1.5, -3.05, 52.8), P['shadow'], bev=0)                 # eye socket
    A.box((0.9, 1.0, 1.8), (0, -3.2, 51.6), P['sandl'], bev=0.1)                            # nose
    A.frustum((3.0, 1.2), (1.6, 0.8), 2.4, (0, -2.6, 48.6), P['sandd'])                     # chin / short beard
    # pectoral collar + kilt panel relief on the front (armour/dress)
    A.frustum((11.0, 4.0), (9.0, 3.0), 2.0, (0, -2.0, 44.0), P['sandl'])                    # broad collar
    for k in range(3):
        A.box((2.4, 0.5, 8.0), (-3.0 + k * 3.0, -3.3, 24.0), P['sandd'], bev=0.08)          # vertical kilt panels (front relief)
    A.box((9.0, 0.5, 1.0), (0, -3.4, 20.0), P['clay'], bev=0.05)                            # a warm banded belt
    # finished BACK: a carved spine pillar + a cartouche panel (no blank slab)
    A.box((2.0, 1.0, 26.0), (0, 3.3, 22.0), P['sandd'], bev=0.1)                            # spine relief down the back
    A.box((5.0, 0.6, 7.0), (0, 3.5, 30.0), P['sandl'], bev=0.1)                             # cartouche frame
    A.box((3.2, 0.5, 5.0), (0, 3.7, 30.0), P['red'], bev=0.04)                              # carved glyph panel
    for k in range(3):
        A.box((9.0, 0.5, 0.5), (0, 3.4, 12.0 + k * 5.0), P['sandd'], bev=0)                 # back robe folds
        A.beam((3.0, -3.0, 40.0), (6.0, -3.2, 40.0), 1.2, 1.2, P['sand'])                  # hand gripping the staff (connects staff to body)
        A.box((5.0, 0.8, 7.0), (0, -3.6, 30.0), P['red'], bev=0.05)                          # chest tablet
    else:                                                                                 # guardian 02: a shield against the chest + beard, broader shoulders
        A.frustum((15.0, 8.0), (13.0, 7.0), 6.0, (0, 0, 40.0), P['sand'])
        A.box((5.0, 1.2, 6.0), (-4.0, -3.4, 30.0), P['sandd'], bev=0.1)                       # shield flush on the chest
        A.frustum((4.0, 1.5), (2.0, 1.0), 4.0, (0, -2.6, 48.0), P['sandd'])                   # beard
    _rubble(A, rnd, 6, 7.0, 7.0, [P['sandd'], P['stone']], (0.8, 1.8))
    return _fin(A, 'guardian_statue')


# ================================================================ LM14 sand obelisk (MINOR: vary from obelisk 01/02)
def _obelisk(i):
    reset()
    A = Acc()
    rnd = random.Random(9400 + i)
    A.box((9.5, 9.5, 2.0), (0, 0, 1.0), P['stone'], bev=0.2)
    A.box((7.4, 7.4, 1.6), (0, 0, 2.8), P['sandd'], bev=0.2)
    # obelisk 03: a MORE eroded, leaning, chipped shaft with a broken tip (distinct from 01/02)
    A.frustum((5.4, 5.4), (2.8, 2.8), 46.0, (0, 0, 3.6), P['sand'], (0, 2.0, 0))             # slight lean
    A.frustum((3.0, 3.0), (1.8, 1.8), 4.0, (0.8, 0.0, 49.6), P['red'])                       # broken, offset tip (not a clean pyramidion)
    # weathered strata bands + a couple of shallow chipped corners (kept well inside the shaft so nothing detaches)
    for k in range(8):
        z = 7.0 + k * 5.0
        A.box((4.8 - k * 0.3, 4.8 - k * 0.3, 0.3), (0, 0, z - 2.0), P['sandd'], bev=0)         # strata band
    for k in range(2):                                                                    # a couple of eroded bites low on the shaft where it is widest (distinct from 01/02)
        z = 9.0 + k * 6.0
        A.box((1.0, 1.0, 2.0), (0.8 - k * 0.1, 0.8 - k * 0.1, z), P['sandd'], (0, 0, 20), bev=0.1)
    _rubble(A, rnd, 6, 4.5, 4.5, [P['sandd'], P['stone']], (0.8, 2.2))
    return _fin(A, 'sand_obelisk')


# ================================================================ LM16 ring temple segments (MINOR: add relief/carving, differ siblings)
def _ring_segment(i):
    """A readable curved ring-temple segment: a banded curved wall with ARCHED openings, a row of EVENLY SPACED free-standing sandstone columns
    in front carrying an entablature, relief courses on both faces, broken merlons. Nothing protrudes below the plinth. Two distinct silhouettes."""
    reset()
    A = Acc()
    rnd = random.Random(9500 + i)
    R0 = 30.0                                                                              # tight radius so the curve clearly READS as a ring segment (chord ~50, depth ~22)
    a0, a1 = -52.0, 52.0
    wall_top = 34.0 if i == 0 else 30.0
    CW = [P['sand'], P['sandl'], P['sandd']]                                               # column palette = sandstone (NOT the dark skull keys) so columns read light
    # grounded base plinth (two curved steps) - stays above z=0, nothing hangs below it
    A.sweep([(R0 - 6.0, 0.0), (R0 + 6.0, 0.0), (R0 + 6.0, 1.8), (R0 - 6.0, 1.8)], a0 - 2, a1 + 2, 22, P['sandd'])
    A.sweep([(R0 - 5.0, 1.8), (R0 + 5.0, 1.8), (R0 + 5.0, 3.0), (R0 - 5.0, 3.0)], a0 - 1, a1 + 1, 22, P['sandl'])
    # curved banded back wall carrying arched window openings (relief on BOTH faces via courses)
    A.sweep([(R0 - 3.2, 3.0), (R0 - 1.0, 3.0), (R0 - 1.0, wall_top), (R0 - 3.2, wall_top)], a0, a1, 22, P['sand'])
    for t, key in ((0.5, P['sandd']),):               # colour string-courses on the wall (kills the blank flat slab)
        z = 3.0 + (wall_top - 3.0) * t
        A.sweep([(R0 - 3.4, z), (R0 - 0.8, z), (R0 - 0.8, z + 1.1), (R0 - 3.4, z + 1.1)], a0, a1, 22, key)
    ncol = 6                                                                               # evenly spaced across the whole arc
    for k in range(ncol):
        aw = a0 + (a1 - a0) * (k + 0.5) / ncol
        # arched dark opening in the wall behind each bay (reads as a window)
        if (i == 0) or (i == 1 and k % 2 == 0):
            x, y, _ = polar(R0 - 2.1, aw)
            A.box((1.4, 3.2, wall_top * 0.5), (x, y, 3.0 + wall_top * 0.28), P['shadow'], (0, 0, aw), bev=0)
        # free-standing sandstone column in front of the wall, evenly spaced
        cx, cy, _ = polar(R0 + 3.4, aw)
        broken = False                                                  # sibling 1: two columns snapped off (ruin) - a SOLID stub, no floating capital
        ch = wall_top * (0.42 if broken else 1.0)
        if broken:
            A.cyl(2.6, ch, (cx, cy, 3.0), CW[0], verts=12, r2=2.3)                         # plain broken drum stub, grounded on the plinth, nothing above it
            A.chunk((5.2, 5.2, 2.2), (cx, cy, 3.0 + ch), CW[2], (rnd.uniform(-8, 8), rnd.uniform(-8, 8), rnd.uniform(0, 30)), 0.3, rnd, (0.7, 0.6))  # jagged break seated on the stub
        else:
            column(A, cx, cy, 2.8, 1.6, ch, SANDCOL, 0.0, rnd)
    if i == 0:
        # entablature spanning the column tops (reads as a finished temple front)
        A.sweep([(R0 + 1.9, wall_top + 0.5), (R0 + 4.9, wall_top + 0.5), (R0 + 4.9, wall_top + 3.0), (R0 + 1.9, wall_top + 3.0)], a0, a1, 22, P['sandl'])
        A.sweep([(R0 + 1.6, wall_top + 3.0), (R0 + 5.2, wall_top + 3.0), (R0 + 5.2, wall_top + 4.0), (R0 + 1.6, wall_top + 4.0)], a0, a1, 22, P['sandd'])
        for k in range(9):                                                                # merlons on the wall top
            aw = a0 + (a1 - a0) * k / 8.0
            x, y, _ = polar(R0 - 2.1, aw)
            A.box((1.3, 2.8, 2.6), (x, y, wall_top + 1.3), P['sand'], (0, 0, aw), bev=0.12)
    else:
        # sibling 1: ruined - a short surviving entablature stub on one side + a collapsed gap, broken merlons
        A.sweep([(R0 + 1.9, wall_top + 0.5), (R0 + 4.9, wall_top + 0.5), (R0 + 4.9, wall_top + 2.6), (R0 + 1.9, wall_top + 2.6)], a0, a1, 22, P['sandl'])
        for k in range(9):
            if k % 3 == 1:
                continue
            aw = a0 + (a1 - a0) * k / 8.0
            x, y, _ = polar(R0 - 2.1, aw)
            A.box((1.3, 2.8, rnd.uniform(1.6, 2.8)), (x, y, wall_top + 0.9), P['sandd'], (0, 0, aw), bev=0.12)
    # a carved red glyph band low on the back wall
    for k in range(6):
        aw = a0 + (a1 - a0) * (k + 0.5) / 6.0
        x, y, _ = polar(R0 - 0.9, aw)
        A.box((0.4, 2.4, 1.3), (x, y, 7.5), P['red'], (0, 0, aw), bev=0)
    # chunky fallen column drums + rubble along the foot (seated on the plinth, nothing below z=0)
    for k in range(8):
        aw = a0 + (a1 - a0) * rnd.random()
        x, y, _ = polar(R0 + rnd.uniform(3.4, 4.6), aw)
        if k % 3 == 0:
            A.cyl(1.5, 3.2, (x, y, 4.5), P['sand'], verts=10, rot=(0, 90, aw))             # fallen drum
        else:
            s = rnd.uniform(1.4, 3.0)
            A.chunk((s, s, rnd.uniform(1.2, 2.4)), (x, y, 3.9), (P['sandd'], P['stone'])[k % 2], (0, 0, aw), 0.2, rnd, (0.8, 0.8))
    return _fin(A, 'ring_temple_segment')


# ================================================================ VC01 volcanic rock (MINOR: remove stray fragment, vary spire arrangement)
def _volcanic(i):
    reset()
    A = Acc()
    rnd = random.Random(9600 + i)
    keys = [P['basalt'], P['basalt2'], P['ash']]
    A.mound(0, 0, 56.0, 50.0, 22.0 + (i % 2) * 5.0, 26, keys, rnd, 0.0, 0.3, 0.7, 0.13)
    # basalt column clusters (varied arrangement per sibling so the set is not clones)
    layout = [(0, 0), (-12, 8), (10, -6), (6, 12)] if i == 0 else [(-8, -8), (8, 8), (14, -2), (-4, 10), (2, -12)]
    for (cx, cy) in layout:
        for j in range(5):
            xx, yy, _ = polar(1.6 * (j > 0), j * 72.0)
            hh = rnd.uniform(14.0, 42.0) * (1.0 - 0.01 * math.hypot(cx, cy))
            A.cyl(1.6, hh + 1.0, (cx + xx, cy + yy, 0.0), keys[(j + i) % 3], verts=6, r2=1.4)
    # a couple of leaning spires (different count/lean per sibling)
    for k in range(2 + i):
        G.spire(A, rnd, rnd.uniform(3.0, 6.0), rnd.uniform(26.0, 46.0), keys, rnd.uniform(-16, 16), rnd.uniform(-14, 14), 2.0, 6, rnd.uniform(-0.08, 0.08))
    # rubble bedded into the mound base (overlaps the body, no stray floating fragment)
    for k in range(16):
        s = rnd.uniform(1.4, 3.4)
        hh = rnd.uniform(1.2, 2.8)
        rx, ry = rnd.uniform(-22, 22), rnd.uniform(-20, 20)
        A.chunk((s, s * rnd.uniform(0.8, 1.2), hh), (rx, ry, 0.0), (keys + [P['rust']])[k % 4], (0, 0, rnd.uniform(0, 90)), 0.2, rnd, (0.8, 0.8))
    return _fin(A, 'volcanic_rock')


# ================================================================ VC03 dark fort ruins (MINOR: seat/remove loose base fragments)
def _dark_fort(i):
    reset()
    A = Acc()
    rnd = random.Random(9700 + i)
    DK = R.DK                                                                              # reuse round-1 dark-fort key dict
    z0 = 2.0
    A.box((60.0, 50.0, z0), (0, 0, z0 / 2.0), P['basalt2'], bev=0.15)                       # flat grounded base (generator scatter lands on this)
    for k in range(5):
        h = rnd.uniform(11.0, 22.0)
        wall_seg(A, rnd, 12.0, h, 6.0, DK, -24.0 + k * 12.0, -22.0, z0, 4.5, k % 2 == 0, False)
    for sg in (-1, 1):
        A.chunk((6.0, 40.0, rnd.uniform(9.0, 18.0)), (sg * 27.0, 0, z0 + 7.0), P['basalt2'], (0, 0, 0), 0.1, rnd)
    round_tower(A, rnd, 7.5, 50.0 - i * 2.0, DK, -26.0, -22.0, z0, ruin=True, slits=3, bands=3)
    round_tower(A, rnd, 6.5, 28.0, DK, 26.0, -22.0, z0, ruin=(i != 1), slits=2, bands=2, top='crenel')
    A.frustum((20.0, 16.0), (18.0, 14.0), 24.0, (0, 10.0, z0), P['ash'])
    for k in range(10):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(2.0, 7.0), a)
        A.chunk((rnd.uniform(2, 5), rnd.uniform(2, 5), rnd.uniform(1.5, 4.0)), (x, 10.0 + y, z0 + 23.0), P['ash'], (0, 0, a), 0.2, rnd)
    # a low rubble berm skirting the base (embeds the walls' and towers' own loose scatter so nothing reads as a detached fragment)
    A.mound(0, 0, 64.0, 54.0, 5.0, 24, [P['basalt2'], P['ash'], P['rust']], rnd, 0.0, 0.5, 0.95, 0.14)
    for sg in (-1, 1):                                                                     # extra rubble heaped around the two tower feet (where the generator scatter lands)
        A.mound(sg * 26.0, -22.0, 16.0, 16.0, 5.0, 8, [P['basalt2'], P['ash']], rnd, 0.0, 0.5, 0.95, 0.14)
    for k in range(14):
        s = rnd.uniform(1.6, 4.0)
        A.chunk((s, s * rnd.uniform(0.8, 1.2), rnd.uniform(1.8, 3.4)), (rnd.uniform(-28, 28), rnd.uniform(-24, 24), 1.0),
                P['basalt2'] if k % 4 else P['rust'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd, (0.8, 0.8))
    return _fin(A, 'dark_fort_ruin')


# ================================================================ batch wiring
# EXACT A3 assignment - only these 40 ids. The sibling index (position in its row) is kept so per-sibling variation lines up.
MINE = {
    'DS01_03_adobe_house_03', 'DS01_04_adobe_house_04',
    'DS02_01_desert_market_01',
    'DS03_02_caravan_wagon_02',
    'DS04_01_palm_01', 'DS04_02_palm_02', 'DS04_03_palm_03',
    'DS05_02_oasis_rock_ring_02',
    'DS07_01_hoodoo_arch_01', 'DS07_02_hoodoo_arch_02', 'DS07_04_hoodoo_arch_04',
    'DS08_01_underground_entrance_01', 'DS08_02_underground_entrance_02', 'DS08_03_underground_entrance_03',
    'SD01_04_red_mesa_cluster_04', 'SD01_05_red_mesa_cluster_05', 'SD01_06_red_mesa_cluster_06',
    'SD02_01_desert_ruin_block_01', 'SD02_02_desert_ruin_block_02', 'SD02_04_desert_ruin_block_04',
    'SD02_05_desert_ruin_block_05', 'SD02_06_desert_ruin_block_06',
    'LM10_02_temple_colonnade_buried_02',
    'LM12_01_temple_stair_down_01', 'LM12_02_temple_stair_down_02',
    'LM13_01_guardian_statue_01', 'LM13_02_guardian_statue_02',
    'LM14_03_sand_obelisk_03',
    'LM16_01_ring_temple_segment_01', 'LM16_02_ring_temple_segment_02',
    'VC01_07_volcanic_rock_07', 'VC01_08_volcanic_rock_08',
    'VC03_01_dark_fort_ruin_01', 'VC03_03_dark_fort_ruin_03',
    'VC04_01_skull_city_building_01', 'VC04_02_skull_city_building_02', 'VC04_03_skull_city_building_03',
    'VC04_04_skull_city_building_04', 'VC04_05_skull_city_building_05', 'VC04_06_skull_city_building_06',
}


def _L(fn, row):
    """(id, builder) for every id in `row` that is MINE, keeping the sibling index j = position within the row."""
    return [(m, (lambda j=j, f=fn: f(j))) for j, m in enumerate(ids(row)) if m in MINE]


# only the ids assigned to A3 appear, each in the SAME category folder as round 1
def _house5_post(A):
    W, D, H = 18.0, 16.0, 11.0
    z0 = 1.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            A.box((1.1, 1.1, H), (sx * (W / 2.0 + 0.1), sy * (D / 2.0 + 0.1), z0 + H / 2.0), P['sandd'], bev=0.1)
    for z in (z0 + H * 0.45, z0 + H * 0.78):
        A.box((W + 0.5, D + 0.5, 0.5), (0, 0, z), P['sand'], bev=0.05)
    A.box((W + 0.45, D + 0.45, 1.8), (0, 0, z0 + 0.9), P['sandl'], bev=0.08)
    for wx in (-5.5, 5.5):
        for s in (-1, 1):
            A.box((0.9, 0.35, 2.6), (wx + s * 1.7, -D / 2.0 - 0.15, 7.0), P['wood'], bev=0.04)


def _canyon2(i):
    reset()
    A = Acc()
    rnd = random.Random(6700 + i * 17)
    ramps = {1: STR, 2: [P['red2'], P['clay'], P['sandd'], P['red'], P['sand'], P['cream']]}
    rp = ramps[i]
    G.cliff(A, rnd, 120.0, 40.0, 45.0, rp, 0, 0, 0, 13 + i, P['sandl'], True, 0.1 if i == 1 else -0.12, 'strata' if i == 1 else 'grade')
    for k in range(7):
        A.box((124.0, 1.2, 1.4), (0, -20.5, 4.0 + k * 5.5), rp[(k + i) % len(rp)], bev=0)
    for k in range(8):
        A.mound(rnd.uniform(-56, 56), -20.0, 12.0, 8.0, rnd.uniform(2, 5), 4, rp, rnd, 0.0, 0.5, 0.9)
    return _fin(A, 'canyon_wall')


def _crown_post(A):
    r_ = random.Random(7)
    A.chunk((12.0, 9.5, 6.5), (0, 0, 55.0), P['sand'], (0, 0, 0), 0.08, r_, (0.9, 0.9))
    for sg in (-1, 1):
        A.chunk((6.0, 9.5, 6.0), (sg * 8.0, 0, 51.5), P['clay'], (0, 0, 0), 0.08, r_, (0.9, 0.9))


def _guard_post(A):
    A.box((15.0, 6.5, 4.0), (0, 0, 46.0), P['sand'], bev=0.25)
    for sg in (-1, 1):
        A.box((3.6, 4.6, 13.0), (sg * 7.8, -0.5, 39.5), P['sand'], bev=0.25)
        A.box((3.0, 3.6, 3.4), (sg * 7.8, -2.5, 32.5), P['sandl'], bev=0.2)
    A.cyl(0.7, 46.0, (-7.8, -3.4, 8.0), P['wood'], verts=8)
    A.frustum((3.0, 3.0), (0.5, 0.5), 5.0, (-7.8, -3.4, 54.0), P['sandd'])
    A.box((9.5, 6.2, 1.2), (0, 0, 43.4), P['clay'], bev=0.1)


def ds01_01():
    return LK.wrap(lambda: R._adobe(R.KINDS[0]), prune=[dict(keys=[R.D['cloth1']], max_size=25.0), dict(keys=None, max_size=1.9, max_z=1.5)])()


def ds01_05():
    return LK.wrap(lambda: _house(4), post=_house5_post)()


def ds04_01():
    return LK.wrap(lambda: _palm(0))()


def ds04_02():
    return LK.wrap(_palm_fan)()


def ds06_02():
    return LK.wrap(lambda: _canyon2(1), deform=dict(scale=(1.0, 1.0, 2.0)))()


def ds06_03():
    return LK.wrap(lambda: _canyon2(2), deform=dict(scale=(1.0, 1.0, 2.0), bend=(0.0, 0.0)))()


def ds07_03():
    return LK.wrap(lambda: _hoodoo_arch(2), post=_crown_post, recolor=[LK.ramp(STR, STRT, trange=(0.0, 62.0), wobble=0.02)])()


def ds08_02():
    return LK.wrap(lambda: _underground(1))()


def lm10_01():
    return LK.wrap(lambda: _colonnade(0))()


def lm12_01():
    return LK.wrap(lambda: _temple_stair(0))()


def lm12_02():
    return LK.wrap(lambda: _temple_stair(1))()


def lm13_01():
    return LK.wrap(lambda: _guardian(0), post=_guard_post, recolor=[LK.ramp([P['red']], [P['clay']])])()


def lm14_01():
    return LK.wrap(lambda: _obelisk(0), deform=dict(taper=0.12), recolor=[LK.ramp([P['sand']], [P['sandl'], P['sand'], P['clay']], trange=(3.0, 52.0), wobble=0.03)])()


def lm14_02():
    return LK.wrap(_obelisk_oct)()


def lm16_01():
    return LK.wrap(lambda: _ring_segment(0))()


def sd01_03():
    return LK.wrap(lambda: _mesa(2), prune=[dict(keys=None, max_size=9.0, max_z=4.0)])()


def sd02_05():
    return LK.wrap(lambda: _ruin_block(4), prune=[dict(keys=[P['sand'], P['sandl'], P['sandd']], max_size=24.0, thin=2.2, max_z=2.5)])()


VOLC = [P['basalt'], P['basalt2'], P['ash']]


def vc01_03():
    return LK.wrap(lambda: _volcanic(2), deform=dict(twist=18.0, bend=(0.1, -0.05), scale=(0.95, 1.0, 1.1)), prune=[dict(keys=None, max_size=3.8, max_z=1.5)])()


def vc01_04():
    return LK.wrap(lambda: _volcanic(3), recolor=[LK.ramp(VOLC, [P['basalt2'], P['basalt'], P['basalt2'], P['ash']], wobble=0.1), LK.ramp(VOLC, [P['rust']], zlim=(-1.0, 3.5))])()


def vc01_06():
    return LK.wrap(lambda: _volcanic(5), deform=dict(lean=(0.12, 0.0), scale=(1.2, 0.9, 0.85), mirror_x=True),
                   recolor=[LK.ramp(VOLC, [P['ash'], P['basalt2'], P['ash'], P['basalt']], wobble=0.1), LK.ramp(VOLC, [P['rust']], zlim=(-1.0, 3.0))])()


def _palm_fan():
    reset()
    A = Acc()
    rnd = random.Random(8812)
    h = 42.0
    segs = 9
    prev = (0.0, 0.0, 0.0)
    A.cyl(2.2, 2.0, (0, 0, 0), P['bark'], verts=10, r2=1.9)
    for s in range(1, segs + 1):
        tt = s / float(segs)
        q = (1.4 * math.sin(tt * 3.0), 0.0, h * tt)
        r = 1.9 - 0.5 * tt
        A.beam((prev[0], prev[1], max(0.0, prev[2] - 0.8)), q, r * 2.0, r * 2.0, P['bark'])
        A.sweep([(r * 0.95, -0.24), (r * 1.65, -0.24), (r * 1.65, 0.24), (r * 0.95, 0.24)], 0, 360, 8, P['bark'], loc=q)
        prev = q
    top = prev
    A.cyl(2.0, 2.6, (top[0], top[1], top[2] - 1.3), P['bark'], verts=10, r2=1.6)
    nf = 11
    for k in range(nf):
        a = 360.0 / nf * k + rnd.uniform(-8, 8)
        pts = []
        for s in range(6):
            tt = s / 5.0
            x, y, _ = polar(tt * 8.5, a)
            pts.append((top[0] + x, top[1] + y, top[2] + 7.5 * math.sin(tt * 1.5) - 3.5 * tt * tt + 0.5))
        for p0, p1 in zip(pts, pts[1:]):
            A.beam(p0, p1, 0.55, 0.4, P['bark'])
        for j, pt in enumerate(pts[1:]):
            bl = 3.0 - j * 0.4
            for sg in (-1, 1):
                A.box((bl, 0.25, 0.9), (pt[0], pt[1], pt[2]), P['palm'] if (k + j) % 2 else P['palm2'], (0, 0, a + sg * 35.0), bev=0)
    for k in range(6):
        x, y, _ = polar(1.5, k * 60.0)
        A.ball(0.8, (top[0] + x, top[1] + y, top[2] - 0.9), P['clay'], segs=6, rings=4)
    return _fin(A, 'oasis_palm')


def _obelisk_oct():
    reset()
    A = Acc()
    A.cyl(5.6, 2.2, (0, 0, 0), P['stone'], verts=8)
    A.cyl(4.6, 1.6, (0, 0, 2.2), P['sandd'], verts=8)
    A.cyl(3.4, 46.0, (0, 0, 3.8), P['sand'], verts=8, r2=2.0)
    for z, r in ((12.0, 3.15), (24.0, 2.85), (36.0, 2.55)):
        A.cyl(r + 0.45, 0.6, (0, 0, z), P['clay'], verts=8)
    for z in (18.0, 30.0, 42.0):
        A.cyl(2.6 - (z - 18.0) * 0.012, 3.0, (0, 0, z), P['sandl'], verts=8, r2=2.5 - (z - 18.0) * 0.012)
    A.cyl(2.2, 2.6, (0, 0, 49.8), P['sandl'], verts=8, r2=1.5)
    A.ball(1.7, (0, 0, 53.4), P['clay'], segs=10, rings=6)
    A.cyl(0.35, 3.0, (0, 0, 54.6), P['sandd'], verts=6, r2=0.05)
    return _fin(A, 'sand_obelisk')


BATCHES = {
    'vh_f_desert': ('v5_desert', mk(
        _L(_house, 'DS01') + _L(_market, 'DS02') + _L(_wagon, 'DS03') + _L(_palm, 'DS04') + _L(_oasis_ring, 'DS05') +
        _L(_hoodoo_arch, 'DS07') + _L(_underground, 'DS08') + _L(_mesa, 'SD01') + _L(_ruin_block, 'SD02'), 0.1)),
    'vh_f_landmarks': ('v5_landmarks', mk(
        _L(_colonnade, 'LM10') + _L(_temple_stair, 'LM12') + _L(_guardian, 'LM13') + _L(_obelisk, 'LM14') + _L(_ring_segment, 'LM16'), 0.1)),
    'vh_f_skull': ('v5_skull', mk(
        _L(_volcanic, 'VC01') + _L(_dark_fort, 'VC03') + _L(_skull_building, 'VC04'), 0.1)),
}


# --- lead4 registration ---
import v5_leadkit as LK
BATCHES['lead4_desert'] = ('v5_desert', mk([('DS01_01_adobe_house_01', ds01_01), ('DS01_05_adobe_house_05', ds01_05), ('DS04_01_palm_01', ds04_01), ('DS04_02_palm_02', ds04_02),
                                            ('DS06_02_canyon_wall_02', ds06_02), ('DS06_03_canyon_wall_03', ds06_03), ('DS07_03_hoodoo_arch_03', ds07_03),
                                            ('DS08_02_underground_entrance_02', ds08_02), ('SD01_03_red_mesa_cluster_03', sd01_03), ('SD02_05_desert_ruin_block_05', sd02_05)], 0.1))
BATCHES['lead4_land'] = ('v5_landmarks', mk([('LM10_01_temple_colonnade_buried_01', lm10_01), ('LM12_01_temple_stair_down_01', lm12_01), ('LM12_02_temple_stair_down_02', lm12_02),
                                             ('LM13_01_guardian_statue_01', lm13_01), ('LM14_01_sand_obelisk_01', lm14_01), ('LM14_02_sand_obelisk_02', lm14_02),
                                             ('LM16_01_ring_temple_segment_01', lm16_01)], 0.1))
BATCHES['lead4_skull'] = ('v5_skull', mk([('VC01_03_volcanic_rock_03', vc01_03), ('VC01_04_volcanic_rock_04', vc01_04), ('VC01_06_volcanic_rock_06', vc01_06)], 0.1))
