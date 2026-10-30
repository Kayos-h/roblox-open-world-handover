"""wg graveyard: E01 gravestones (8), E02 crypts (3), E03 weeping statues (3), E04 iron fence+gate (2).
Haunting, old, weathered. Fronts face -Y. 1 unit = 1 stud. Builds through v4run.ps1 only."""
import math, random
from mathutils import Vector, Euler
import kitlib
from kitlib import (reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, top_paint, scroll)
from arch import (F, faces, lbox, lbeam, beam3, slab, lslab, half_disc, band, nm, gable_roof, column_c,
                  pediment, lancet_pts, arc_pts)
from capital import plinth

# ---- wg palette additions (weathered graveyard stone, lichen, old iron) ----
kitlib.PAL['wg_granite']    = ((118, 116, 120), 'Granite',     0.00, 0.85, 0)
kitlib.PAL['wg_granite_d']  = ((92, 90, 96),    'Granite',     0.00, 0.90, 0)
kitlib.PAL['wg_marble']     = ((214, 210, 202), 'Marble',      0.00, 0.55, 0)
kitlib.PAL['wg_marble_d']   = ((176, 172, 164), 'Marble',      0.00, 0.65, 0)
kitlib.PAL['wg_stone']      = ((146, 140, 128), 'Limestone',   0.00, 0.88, 0)
kitlib.PAL['wg_stone_d']    = ((110, 104, 96),  'Slate',       0.00, 0.92, 0)
kitlib.PAL['wg_lichen']     = ((150, 158, 118), 'Grass',       0.00, 1.00, 0)
kitlib.PAL['wg_moss']       = ((88, 104, 56),   'Grass',       0.00, 1.00, 0)
kitlib.PAL['wg_iron']       = ((38, 36, 36),    'Metal',       0.80, 0.55, 0)
kitlib.PAL['wg_iron_rust']  = ((96, 58, 40),    'CorrodedMetal', 0.40, 0.85, 0)
kitlib.PAL['wg_dirt']       = ((104, 86, 64),   'Ground',      0.00, 1.00, 0)
kitlib.PAL['wg_ivy']        = ((54, 82, 40),    'LeafyGrass',  0.00, 0.95, 0)

GRAN = ['wg_granite', 'wg_granite_d']
STON = ['wg_stone', 'wg_stone_d']


def _lichen(o, amt=0.62, seed=0, key='wg_lichen'):
    top_paint(o, key, amt, seed)
    return o


def _mound(x0, y0, w, d, key='wg_dirt', seed=0):
    o = box(nm('gr'), (w, d, 0.4), loc=(x0, y0, 0.16), key=key, bev=0.18)
    return o


def _grass_tuft(x, y, rnd, n=5, h=0.7, key='wg_moss'):
    for _ in range(n):
        a = rnd.uniform(0, 6.28)
        tube(nm('tf'), [(x, y, 0.0), (x + math.cos(a) * 0.2, y + math.sin(a) * 0.2, h * rnd.uniform(0.6, 1.0))],
             0.05, key, res=4, taper=[1, 0.1])


def _ivy_face(x0, x1, y, z0, z1, n, seed, face=-1):
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.uniform(x0, x1)
        z = z0 + (z1 - z0) * rnd.random() ** 1.5
        ball(nm('iv'), rnd.uniform(0.22, 0.4), loc=(x, y + face * 0.12, z),
             key=rnd.choice(['wg_ivy', 'wg_moss']), segs=6, rings=4, scale=(1.3, 0.4, 1.1))


def _inscription(f, cx, cz, w, lines=3, key='wg_stone_d'):
    """Shallow carved lines standing in for an epitaph."""
    lbox(f, (w, 0.04, 0.22), cx, -0.05, cz + 0.5, key)          # name bar
    for i in range(lines):
        lbox(f, (w * (0.8 - i * 0.12), 0.04, 0.09), cx, -0.05, cz - 0.1 - i * 0.28, key)


# ============================================================ E01 gravestones
def gravestone_01():
    """E01_01 - rounded-top slab with inscription panel, mossy base, slight lean."""
    reset()
    W, H, T = 2.6, 4.6, 0.55
    pts = [(-W / 2, 0, 0), (W / 2, 0, 0), (W / 2, 0, H - W / 2)]
    pts += [(math.cos(math.radians(a)) * W / 2, 0, (H - W / 2) + math.sin(math.radians(a)) * W / 2)
            for a in range(15, 166, 15)]
    pts += [(-W / 2, 0, H - W / 2)]
    o = lslab(F(0, T / 2, 0, 0), pts, (0, -T, 0), 'wg_stone')
    o.rotation_euler = Euler((math.radians(4), math.radians(-3), 0))
    # sunk recessed panel look via darker inset frame + inscription
    f = F(0, -T / 2 - 0.0, 0, 0)
    lbox(f, (W - 0.8, 0.06, H - 1.9), 0, 0.02, (H - 1.9) / 2 + 0.3, 'wg_stone_d')
    _inscription(F(0, -T / 2 - 0.08, 0, 0), 0, H * 0.5, W - 1.0, lines=3)
    _lichen(o, 0.45, 1)
    _mound(0, -1.3, W + 0.8, 3.2, seed=1)
    rnd = random.Random(1)
    _grass_tuft(W / 2 - 0.2, 0.0, rnd)
    _grass_tuft(-W / 2 + 0.2, 0.1, rnd)
    return finalize('gravestone_01', smooth_angle=25)


def gravestone_02():
    """E01_02 - Celtic ring cross on a two-step base, carved knot bands."""
    reset()
    for k in range(2):
        box(nm('b'), (3.0 - k * 0.8, 2.2 - k * 0.6, 0.55), loc=(0, 0, 0.27 + k * 0.55),
            key=GRAN[k % 2], bev=0.05)
    o = box(nm('v'), (0.78, 0.6, 5.2), loc=(0, 0, 1.1 + 2.6), key='wg_granite', bev=0.05)
    box(nm('h'), (2.9, 0.6, 0.78), loc=(0, 0, 1.1 + 3.9), key='wg_granite', bev=0.05)
    torus(nm('ring'), 1.15, 0.2, loc=(0, 0, 1.1 + 3.9), key='wg_granite', segs=24, rsegs=5, rot=(90, 0, 0))
    # knot bands on the shaft (front)
    for zz in (2.2, 3.1, 4.0):
        lbox(F(0, -0.31, 0, 0), (0.6, 0.06, 0.2), 0, 0, 1.1 + zz, 'wg_granite_d')
    cyl(nm('boss'), 0.38, 0.22, loc=(0, -0.3, 1.1 + 3.9), key='wg_granite_d', verts=12, rot=(90, 0, 0))
    o.rotation_euler = Euler((math.radians(3), math.radians(2), 0))
    _lichen(o, 0.4, 2)
    _mound(0, -1.0, 3.4, 3.0, seed=2)
    return finalize('gravestone_02', smooth_angle=25)


def gravestone_03():
    """E01_03 - broken headstone, missing top corner, the broken piece lying beside it."""
    reset()
    W, H, T = 2.4, 4.2, 0.5
    # jagged break across the upper third
    pts = [(-W / 2, 0, 0), (W / 2, 0, 0), (W / 2, 0, 2.4), (0.6, 0, 3.4), (0.15, 0, 2.7),
           (-0.3, 0, 3.6), (-W / 2, 0, 3.0)]
    o = lslab(F(0, T / 2, 0, 0), pts, (0, -T, 0), 'wg_stone')
    o.rotation_euler = Euler((math.radians(-5), math.radians(4), 0))
    _inscription(F(0, -T / 2 - 0.05, 0, 0), 0, 1.7, W - 0.9, lines=2)
    _lichen(o, 0.35, 3)
    # fallen broken corner on the ground
    frag = [(-0.55, 0, 0), (0.6, 0, 0), (0.25, 0, 0.5), (-0.4, 0, 0.45)]
    fo = lslab(F(1.6, -1.2, 0.0, 28), frag, (0, -T, 0), 'wg_stone')
    fo.rotation_euler = Euler((math.radians(72), 0, math.radians(28)))
    _lichen(fo, 0.5, 33)
    _mound(0, -1.2, W + 1.2, 3.4, seed=3)
    return finalize('gravestone_03', smooth_angle=25)


def gravestone_04():
    """E01_04 - slim pillar with a carved draped urn on top, stepped plinth."""
    reset()
    box(nm('b'), (1.9, 1.9, 0.6), loc=(0, 0, 0.3), key='wg_granite_d', bev=0.05)
    box(nm('b2'), (1.5, 1.5, 0.4), loc=(0, 0, 0.8), key='wg_granite', bev=0.04)
    o = lathe(nm('sh'), [(0, 1.0), (0.62, 1.0), (0.5, 4.8), (0.46, 5.0), (0.0, 5.0)], key='wg_marble', segs=4)
    # cap
    lathe(nm('cap'), [(0, 5.0), (0.62, 5.0), (0.62, 5.25), (0.46, 5.35), (0, 5.35)], key='wg_marble_d', segs=4)
    # draped urn
    lathe(nm('urn'), [(0, 5.35), (0.3, 5.35), (0.22, 5.55), (0.5, 6.0), (0.56, 6.5), (0.4, 6.95),
                      (0.2, 7.05), (0.26, 7.2), (0.1, 7.2), (0, 7.1)], key='wg_marble', segs=12)
    # drape cloth over the urn
    for s in (-1, 1):
        ball(nm('dr'), 0.26, loc=(s * 0.4, 0, 6.7), key='wg_marble_d', segs=8, rings=5,
             scale=(0.7, 1.1, 1.3))
    _lichen(o, 0.3, 4)
    _mound(0, -1.0, 2.6, 2.6, seed=4)
    return finalize('gravestone_04', smooth_angle=30)


def gravestone_05():
    """E01_05 - headstone carved with an angel relief in a round-arched niche."""
    reset()
    W, H, T = 3.0, 5.2, 0.6
    # arched-top tablet
    pts = [(-W / 2, 0, 0), (W / 2, 0, 0), (W / 2, 0, H - W / 2)]
    pts += [(math.cos(math.radians(a)) * W / 2, 0, (H - W / 2) + math.sin(math.radians(a)) * W / 2)
            for a in range(12, 169, 12)]
    pts += [(-W / 2, 0, H - W / 2)]
    o = lslab(F(0, T / 2, 0, 0), pts, (0, -T, 0), 'wg_marble')
    o.rotation_euler = Euler((math.radians(3), 0, 0))
    f = F(0, -T / 2, 0, 0)
    # recessed niche
    lbox(f, (W - 1.0, 0.08, 2.8), 0, 0.03, H - 1.9, 'wg_marble_d')
    tube(nm('na'), arc_pts(f, 0, H - 1.9 + 1.4, (W - 1.0) / 2 + 0.05, y=-0.06, n=11), 0.1, 'wg_marble_d', res=4)
    # angel relief: wings first (behind), then gowned body, round haloed head
    z0 = H - 3.0
    yb = -T / 2 - 0.12
    for s in (-1, 1):
        wing = [(s * 0.18, 0, 1.1), (s * 0.7, 0, 1.5), (s * 1.05, 0, 2.3), (s * 1.0, 0, 3.0),
                (s * 0.7, 0, 2.7), (s * 0.5, 0, 2.0), (s * 0.3, 0, 1.3)]
        lslab(F(0, yb, z0, 0), wing, (0, -0.1, 0), 'wg_marble_d')
        for k in range(3):
            lbox(F(0, yb - 0.08, z0, 0), (0.06, 0.04, 0.5 + k * 0.2), s * (0.5 + k * 0.18), 0, 1.9 + k * 0.1,
                 'wg_marble')
    lathe(nm('body'), [(0, 0), (0.5, 0.05), (0.44, 0.9), (0.34, 1.9), (0.22, 2.3), (0, 2.35)],
          loc=(0, yb - 0.12, z0), key='wg_marble', segs=12, sy=0.5)
    for s in (-1, 1):
        tube(nm('arm'), [(s * 0.34, yb - 0.2, z0 + 1.8), (0, yb - 0.28, z0 + 1.4)], 0.09, 'wg_marble', res=4)
    ball(nm('head'), 0.32, loc=(0, yb - 0.3, z0 + 2.55), key='wg_marble', segs=10, rings=7, scale=(1, 0.6, 1))
    torus(nm('halo'), 0.42, 0.05, loc=(0, yb - 0.18, z0 + 2.75), key='wg_marble_d', segs=16, rsegs=4, rot=(90, 0, 0))
    _inscription(F(0, -T / 2 - 0.05, 0, 0), 0, 1.0, W - 1.2, lines=2)
    _lichen(o, 0.78, 5)
    _mound(0, -1.2, W + 0.8, 3.0, seed=5)
    return finalize('gravestone_05', smooth_angle=28)


def gravestone_06():
    """E01_06 - flat ledger slab on a low cracked stone box (table tomb)."""
    reset()
    L, Wd, H = 5.2, 2.8, 1.6
    rnd = random.Random(6)
    # low box with coursed, cracked stones
    for s in (-1, 1):
        box(nm('wl'), (L, 0.45, H), loc=(0, s * (Wd / 2 - 0.22), H / 2), key='wg_stone', bev=0.05)
        box(nm('we'), (0.45, Wd - 0.9, H), loc=(s * (L / 2 - 0.22), 0, H / 2), key='wg_stone', bev=0.05)
    # scattered course lines / cracks
    for s in (-1, 1):
        fr = F(0, s * (Wd / 2), 0, 0 if s < 0 else 180)
        for i in range(4):
            lbox(fr, (L * 0.22, 0.04, 0.08), -L / 2 + 0.7 + i * L * 0.25, -0.02, rnd.uniform(0.5, 1.1), 'wg_stone_d')
    # ledger slab on top, slightly cracked across the middle
    o = box(nm('led'), (L + 0.3, Wd + 0.3, 0.4), loc=(-0.15, 0, H + 0.2), key='wg_marble_d', bev=0.05)
    o.rotation_euler = Euler((0, math.radians(-1.5), 0))
    box(nm('crk'), (0.08, Wd + 0.3, 0.42), loc=(0.6, 0.2, H + 0.2), key='wg_stone_d')
    _inscription(F(0, 0, H + 0.41, 0), 0, 0, L - 1.6, lines=3)  # top face lines (flat)
    _lichen(o, 0.3, 6)
    for xx in (-L / 2, L / 2):
        _grass_tuft(xx, Wd / 2, rnd)
    return finalize('gravestone_06', smooth_angle=25)


def gravestone_07():
    """E01_07 - double headstone: two joined rounded tablets sharing a base."""
    reset()
    base = box(nm('b'), (5.0, 1.6, 0.6), loc=(0, 0, 0.3), key='wg_granite_d', bev=0.05)
    for s, key in ((-1, 'wg_stone'), (1, 'wg_granite')):
        W, H, T = 2.2, 4.2 + (0.4 if s < 0 else 0), 0.5
        cx = s * 1.25
        pts = [(cx - W / 2, 0, 0), (cx + W / 2, 0, 0), (cx + W / 2, 0, H - W / 2)]
        pts += [(cx + math.cos(math.radians(a)) * W / 2, 0, (H - W / 2) + math.sin(math.radians(a)) * W / 2)
                for a in range(15, 166, 15)]
        pts += [(cx - W / 2, 0, H - W / 2)]
        o = lslab(F(0, T / 2, 0.6, 0), pts, (0, -T, 0), key)
        o.rotation_euler = Euler((math.radians(2 * s), 0, 0))
        _inscription(F(0, -T / 2, 0.6, 0), cx, H * 0.5, W - 0.8, lines=2)
        _lichen(o, 0.35, 70 + s)
    # a carved linked-heart / ring between them
    torus(nm('lk'), 0.4, 0.09, loc=(0, -0.3, 2.4), key='wg_granite_d', segs=16, rsegs=4, rot=(90, 0, 0))
    _mound(0, -1.2, 5.6, 3.2, seed=7)
    return finalize('gravestone_07', smooth_angle=25)


def gravestone_08():
    """E01_08 - old sunken stone, half buried and tilted, smothered in ivy and moss."""
    reset()
    W, H, T = 2.4, 3.6, 0.55
    pts = [(-W / 2, 0, 0), (W / 2, 0, 0), (W / 2, 0, 1.9), (0.5, 0, 2.6), (0.05, 0, 2.0),
           (-0.4, 0, 2.7), (-W / 2, 0, 2.3)]
    o = lslab(F(0, T / 2, 0, 0), pts, (0, -T, 0), 'wg_stone_d')
    o.rotation_euler = Euler((math.radians(-16), math.radians(10), 0))
    o.location.z = -0.25  # sunk partway into the ground, still clearly a headstone
    _lichen(o, 0.5, 8)    # patchy moss on the up-faces, stone still shows
    # a few thin ivy strands trailing down the face, not a bush
    rnd = random.Random(8)
    for i in range(4):
        x = -W / 2 + 0.3 + i * (W - 0.6) / 3
        pts = [(x, -T / 2 - 0.05, 1.9 - i * 0.2), (x + rnd.uniform(-0.2, 0.2), -T / 2 - 0.18, 1.1),
               (x + rnd.uniform(-0.3, 0.3), -T / 2 - 0.12, rnd.uniform(0.2, 0.5))]
        tube(nm('iv'), pts, 0.05, 'wg_ivy', res=4, taper=[1, 0.8, 0.3])
        for t in (0.4, 0.75):
            ball(nm('il'), 0.16, loc=(x + rnd.uniform(-0.15, 0.15), -T / 2 - 0.2, 1.9 - 1.5 * t - i * 0.15),
                 key='wg_ivy', segs=6, rings=4, scale=(1.2, 0.4, 1.0))
    # second toppled small stone nearby
    o2 = box(nm('s2'), (1.3, 0.4, 1.4), loc=(-1.7, -0.6, 0.2), key='wg_stone', rot=(8, 20, 0), bev=0.05)
    _lichen(o2, 0.45, 81)
    _mound(0, -1.2, W + 1.6, 3.4, seed=8)
    for _ in range(4):
        _grass_tuft(rnd.uniform(-W / 2, W / 2), rnd.uniform(-1.6, 0.3), rnd, n=5)
    return finalize('gravestone_08', smooth_angle=25)


BATCHES = {
    'e01': ('v4_graveyard', [
        ('E01_01_gravestone_01', gravestone_01),
        ('E01_02_gravestone_02', gravestone_02),
        ('E01_03_gravestone_03', gravestone_03),
        ('E01_04_gravestone_04', gravestone_04),
        ('E01_05_gravestone_05', gravestone_05),
        ('E01_06_gravestone_06', gravestone_06),
        ('E01_07_gravestone_07', gravestone_07),
        ('E01_08_gravestone_08', gravestone_08),
    ]),
}
