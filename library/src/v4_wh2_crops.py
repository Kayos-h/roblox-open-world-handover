"""wh2 E10 crop plots and E11 scarecrows. 1 unit = 1 stud, front -Y, origin bottom-centre.
Modest triangle counts via simple repeated plants with seeded variation. Palette keys prefixed 'wh2_'."""
import math, random
import bpy
from mathutils import Vector
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, top_paint, PAL
from arch import F, nm, beam3
from nature import blob, rock

# ---- palette additions (crops) -------------------------------------------
PAL['wh2_soil']      = ((74, 54, 38),   'Mud',   0.0, 0.92, 0)
PAL['wh2_soil_d']    = ((58, 42, 30),   'Mud',   0.0, 0.94, 0)
PAL['wh2_wheat']     = ((206, 174, 86), 'Grass', 0.0, 0.80, 0)
PAL['wh2_wheat_d']   = ((182, 148, 66), 'Grass', 0.0, 0.82, 0)
PAL['wh2_cornstalk'] = ((96, 132, 52),  'Grass', 0.0, 0.78, 0)
PAL['wh2_cornleaf']  = ((120, 158, 64), 'LeafyGrass', 0.0, 0.76, 0)
PAL['wh2_cob']       = ((214, 192, 96), 'Grass', 0.0, 0.70, 0)
PAL['wh2_cabbage']   = ((128, 170, 96), 'LeafyGrass', 0.0, 0.70, 0)
PAL['wh2_cabbage_i'] = ((170, 198, 128),'LeafyGrass', 0.0, 0.66, 0)
PAL['wh2_pumpkin']   = ((200, 112, 40), 'Grass', 0.0, 0.62, 0)
PAL['wh2_vine']      = ((88, 120, 54),  'LeafyGrass', 0.0, 0.76, 0)
PAL['wh2_grape']     = ((96, 70, 128),  'Grass', 0.0, 0.58, 0)
PAL['wh2_grapeleaf'] = ((108, 140, 66), 'LeafyGrass', 0.0, 0.74, 0)
PAL['wh2_lav']       = ((136, 112, 186),'Grass', 0.0, 0.66, 0)
PAL['wh2_lavstem']   = ((120, 138, 92), 'Grass', 0.0, 0.76, 0)
PAL['wh2_herb']      = ((108, 150, 80), 'LeafyGrass', 0.0, 0.72, 0)
PAL['wh2_straw']     = ((198, 168, 92), 'Grass', 0.0, 0.80, 0)
PAL['wh2_sack']      = ((176, 150, 110),'Fabric', 0.0, 0.86, 0)
PAL['wh2_rag_a']     = ((120, 96, 74),  'Fabric', 0.0, 0.88, 0)
PAL['wh2_rag_b']     = ((96, 108, 120), 'Fabric', 0.0, 0.88, 0)
PAL['wh2_turnip']    = ((214, 202, 170),'Grass', 0.0, 0.68, 0)
PAL['wh2_crow']      = ((26, 26, 30),   'SmoothPlastic', 0.0, 0.52, 0)


# ---- shared plot base -----------------------------------------------------
def _plot_base(size=16.0, rows=7, seed=0, ridged=True):
    """Tilled-soil square with raised furrow ridges running along +x. Returns row centre y-positions."""
    rnd = random.Random(seed)
    box(nm('plot'), (size, size, 0.6), loc=(0, 0, 0.3), key='wh2_soil', bev=0.05)
    # low plank border
    for s in (-1, 1):
        box(nm('bd'), (size + 0.4, 0.3, 0.7), loc=(0, s * size / 2, 0.45), key='wood_old')
        box(nm('bd'), (0.3, size + 0.4, 0.7), loc=(s * size / 2, 0, 0.45), key='wood_old')
    ys = []
    rp = size / rows
    for i in range(rows):
        y = -size / 2 + rp * (i + 0.5)
        ys.append(y)
        if ridged:
            box(nm('ridge'), (size - 0.8, rp * 0.6, 0.4), loc=(0, y, 0.75), key='wh2_soil_d', bev=0.06)
    return ys


def _blade(x, y, z, h, key, lean, rz, w=0.12):
    o = box(nm('bl'), (w, w, h), loc=(x, y, z + h / 2), key=key, bev=0.02)
    o.rotation_euler = (math.radians(lean * math.sin(rz)), math.radians(lean * math.cos(rz)), math.radians(math.degrees(rz)))
    return o


# ============================================================ E10 crop plots
def crop_wheat():
    """E10_01 - wheat field: dense clumps of short golden stalks with bushy seed heads in furrow rows."""
    reset()
    rnd = random.Random(401)
    ys = _plot_base(16, 7, 401)
    for y in ys:
        nclump = 11
        for c in range(nclump):
            cx = -7.0 + 14.0 * c / (nclump - 1) + rnd.uniform(-0.2, 0.2)
            cy = y + rnd.uniform(-0.25, 0.25)
            key = rnd.choice(['wh2_wheat', 'wh2_wheat', 'wh2_wheat_d'])
            # a tight tuft of a few blades fanning up from one spot
            for b in range(4):
                a = rnd.uniform(0, 6.28); d = rnd.uniform(0, 0.18)
                h = rnd.uniform(1.8, 2.4)
                _blade(cx + math.cos(a) * d, cy + math.sin(a) * d, 0.9, h, key, rnd.uniform(4, 12), a, w=0.11)
            # one bushy seed head sitting on the tuft
            ball(nm('head'), 0.4, loc=(cx, cy, 0.9 + 2.3), key=key, segs=6, rings=4, scale=(0.75, 0.75, 1.6))
    return finalize('crop_plot_01', smooth_angle=35)


def crop_corn():
    """E10_02 - corn field: tall stalks with drooping leaves and a cob each, fewer plants (bigger)."""
    reset()
    rnd = random.Random(402)
    ys = _plot_base(16, 5, 402)
    for y in ys:
        n = 10
        for i in range(n):
            x = -6.8 + 13.6 * i / (n - 1) + rnd.uniform(-0.3, 0.3)
            h = rnd.uniform(5.0, 6.5)
            cyl(nm('stalk'), 0.16, h, loc=(x, y, 0.9 + h / 2), key='wh2_cornstalk', verts=6)
            for k in range(4):
                zz = 0.9 + h * (0.35 + 0.16 * k)
                a = k * 1.9
                tube(nm('leaf'), [(x, y, zz), (x + math.cos(a) * 1.3, y + math.sin(a) * 1.0, zz - 0.5)],
                     0.06, 'wh2_cornleaf', res=3)
            # cob
            cyl(nm('cob'), 0.28, 1.0, loc=(x + 0.3, y, 0.9 + h * 0.55), key='wh2_cob', verts=8, rot=(0, 18, 0))
            # tassel
            for t in range(3):
                tube(nm('tas'), [(x, y, 0.9 + h), (x + rnd.uniform(-0.3, 0.3), y + rnd.uniform(-0.3, 0.3), 0.9 + h + 0.6)], 0.04, 'wh2_wheat', res=2)
    return finalize('crop_plot_02', smooth_angle=35)


def crop_cabbage():
    """E10_03 - cabbage patch: rows of layered leafy spheres."""
    reset()
    rnd = random.Random(403)
    ys = _plot_base(16, 6, 403)
    for y in ys:
        n = 8
        for i in range(n):
            x = -6.5 + 13.0 * i / (n - 1) + rnd.uniform(-0.25, 0.25)
            r = rnd.uniform(0.75, 1.05)
            # outer leaves: a few blobs splayed out
            for k in range(5):
                a = 2 * math.pi * k / 5 + rnd.random()
                blob(nm('ol'), r * 0.7, (x + math.cos(a) * r * 0.5, y + math.sin(a) * r * 0.5, 0.95 + r * 0.2),
                     'wh2_cabbage', subdiv=1, amp=0.25, scale=(1.3, 1.3, 0.6), seed=403 + i * 7 + k)
            ball(nm('head'), r * 0.6, loc=(x, y, 0.95 + r * 0.45), key='wh2_cabbage_i', segs=7, rings=5, scale=(1, 1, 0.9))
    return finalize('crop_plot_03', smooth_angle=35)


def crop_pumpkin():
    """E10_04 - pumpkin patch: trailing vines with big ribbed orange pumpkins and leaves."""
    reset()
    rnd = random.Random(404)
    _plot_base(16, 4, 404, ridged=False)
    # winding vines
    for v in range(5):
        y0 = -6 + v * 3.0
        pts = [(-7, y0, 0.75)]
        for k in range(1, 8):
            pts.append((-7 + 14 * k / 7, y0 + math.sin(k * 1.1 + v) * 1.6, 0.75))
        tube(nm('vine'), pts, 0.12, 'wh2_vine', res=4)
        # leaves along the vine
        for k in range(6):
            px = -7 + 14 * (k + 0.5) / 7
            py = y0 + math.sin((k + 0.5) * 1.1 + v) * 1.6
            box(nm('lf'), (1.1, 1.1, 0.08), loc=(px, py, 0.82), key='wh2_vine', rot=(0, 0, rnd.uniform(0, 180)), bev=0.3)
    # pumpkins (ribbed via a squashed lathe)
    for p in range(9):
        x = rnd.uniform(-6, 6); y = rnd.uniform(-6, 6)
        r = rnd.uniform(0.9, 1.5)
        lathe(nm('pk'), [(0, 0), (r * 0.9, 0), (r, r * 0.5), (r * 0.9, r), (0, r * 1.05)], loc=(x, y, 0.8), key='wh2_pumpkin', segs=10)
        # ribs
        for k in range(8):
            a = 2 * math.pi * k / 8
            tube(nm('rib'), [(x + math.cos(a) * r * 0.1, y + math.sin(a) * r * 0.1, 0.82),
                             (x + math.cos(a) * r * 0.92, y + math.sin(a) * r * 0.92, 0.8 + r * 0.5)], 0.04, 'wh2_pumpkin', res=2)
        cyl(nm('stem'), 0.12, 0.5, loc=(x, y, 0.8 + r * 1.1), key='wh2_cornstalk', verts=6)
    return finalize('crop_plot_04', smooth_angle=35)


def crop_grapes():
    """E10_05 - grape vines trained on a wire trellis between posts, bunches hanging."""
    reset()
    rnd = random.Random(405)
    _plot_base(16, 1, 405, ridged=False)
    rows_y = [-5.0, 0.0, 5.0]
    for y in rows_y:
        # posts + top wire
        for i in range(5):
            x = -7 + 14 * i / 4
            box(nm('post'), (0.24, 0.24, 4.0), loc=(x, y, 2.0), key='wood_old')
        tube(nm('wire'), [(-7, y, 3.6), (7, y, 3.6)], 0.04, 'iron', res=2)
        tube(nm('wire2'), [(-7, y, 2.4), (7, y, 2.4)], 0.04, 'iron', res=2)
        # gnarled vine trunks + foliage mass along the wire
        for i in range(4):
            x = -5.5 + 11 * i / 3
            tube(nm('tr'), [(x, y, 0.75), (x + 0.2, y, 2.4), (x, y, 3.5)], 0.12, 'bark', res=4)
        for k in range(10):
            x = -6.5 + 13 * k / 9
            blob(nm('fol'), rnd.uniform(0.7, 1.0), (x, y, 3.4), 'wh2_grapeleaf', subdiv=1, amp=0.3, scale=(1.2, 0.8, 0.9), seed=405 + k)
            # hanging grape bunch
            if rnd.random() < 0.7:
                bz = 2.8
                for g in range(7):
                    ball(nm('gr'), 0.16, loc=(x + rnd.uniform(-0.25, 0.25), y + rnd.uniform(-0.2, 0.2), bz - g * 0.18 - (g % 2) * 0.06),
                         key='wh2_grape', segs=5, rings=4)
    return finalize('crop_plot_05', smooth_angle=35)


def crop_lavender():
    """E10_06 - lavender and herb beds: low rounded bushes with purple spikes and green herb clumps."""
    reset()
    rnd = random.Random(406)
    ys = _plot_base(16, 6, 406)
    for ri, y in enumerate(ys):
        lav = ri % 2 == 0
        n = 7
        for i in range(n):
            x = -6.5 + 13 * i / (n - 1) + rnd.uniform(-0.2, 0.2)
            if lav:
                blob(nm('bush'), rnd.uniform(0.7, 0.95), (x, y, 0.95), 'wh2_lavstem', subdiv=1, amp=0.25, scale=(1.1, 1.1, 0.7), seed=406 + i + ri * 9)
                for s in range(10):
                    a = rnd.uniform(0, 6.28); d = rnd.uniform(0, 0.6)
                    sx, sy = x + math.cos(a) * d, y + math.sin(a) * d
                    _blade(sx, sy, 1.3, rnd.uniform(0.8, 1.2), 'wh2_lavstem', rnd.uniform(4, 10), a, w=0.05)
                    cyl(nm('sp'), 0.09, 0.5, loc=(sx, sy, 1.3 + 0.9), key='wh2_lav', verts=5)
            else:
                blob(nm('herb'), rnd.uniform(0.6, 0.85), (x, y, 0.95), 'wh2_herb', subdiv=1, amp=0.3, scale=(1.2, 1.2, 0.6), seed=416 + i + ri * 9)
    return finalize('crop_plot_06', smooth_angle=35)


# ============================================================ E11 scarecrows
def _straw_tufts(x, y, z, rnd, n, length, key='wh2_straw', spread=0.3):
    for i in range(n):
        a = rnd.uniform(0, 6.28)
        tube(nm('st'), [(x, y, z), (x + math.cos(a) * spread, y + math.sin(a) * spread, z + length * rnd.uniform(0.6, 1.1))],
             0.05, key, res=2)


def _post_cross(h=8.0, armz=5.8, armspan=5.0):
    """Wooden cross frame: vertical post + horizontal arm. Returns (armz, armspan)."""
    box(nm('post'), (0.4, 0.4, h), loc=(0, 0, h / 2), key='wood_old', bev=0.03)
    box(nm('arm'), (armspan, 0.3, 0.3), loc=(0, 0, armz), key='wood_old', bev=0.03)
    # ground stake mound
    rock(nm('md'), 0.9, (0, 0, 0.1), 'wh2_soil', seed=7, scale=(1.4, 1.4, 0.3))
    return armz, armspan


def scarecrow_classic():
    """E11_01 - classic straw-stuffed scarecrow: cross frame, stuffed shirt + trousers, burlap head, straw-poke tufts, hat."""
    reset()
    rnd = random.Random(501)
    armz, armspan = _post_cross(h=8.5, armz=6.2, armspan=5.2)
    # stuffed body: a plaid shirt torso
    blob(nm('torso'), 1.5, (0, -0.1, 4.6), 'wh2_rag_a', subdiv=1, amp=0.22, scale=(1.1, 0.8, 1.3), seed=501)
    # arms (sleeves) along the crossbar
    for s in (-1, 1):
        cyl(nm('sleeve'), 0.45, armspan * 0.46, loc=(s * armspan * 0.26, 0, armz), key='wh2_rag_b', verts=8, rot=(0, 90, 0))
        _straw_tufts(s * armspan * 0.5, 0, armz, rnd, 6, 1.0)
    # legs / stuffed trousers hanging
    for s in (-1, 1):
        cyl(nm('leg'), 0.4, 3.2, loc=(s * 0.6, 0, 2.2), key='wh2_rag_b', verts=8)
        _straw_tufts(s * 0.6, 0, 0.7, rnd, 5, 0.8)
    # burlap head
    ball(nm('head'), 1.0, loc=(0, -0.1, 6.6), key='wh2_sack', segs=9, rings=7, scale=(1, 0.95, 1.1))
    for (ex) in (-0.35, 0.35):
        ball(nm('eye'), 0.14, loc=(ex, -0.9, 6.7), key='wh2_crow', segs=5, rings=4)
    box(nm('mouth'), (0.6, 0.1, 0.1), loc=(0, -0.9, 6.3), key='wood_dark')
    _straw_tufts(0, 0, 7.4, rnd, 8, 0.7)  # straw hair
    # pointed straw hat
    cyl(nm('brim'), 1.5, 0.12, loc=(0, -0.1, 7.5), key='thatch', verts=16)
    lathe(nm('cone'), [(0, 0), (1.1, 0), (0, 1.6)], loc=(0, -0.1, 7.55), key='thatch', segs=12)
    return finalize('scarecrow_01', smooth_angle=30)


def scarecrow_ragged():
    """E11_02 - ragged scarecrow with crows perched on its arms and a tattered coat."""
    reset()
    rnd = random.Random(502)
    armz, armspan = _post_cross(h=8.0, armz=5.9, armspan=5.6)
    # tattered coat torso: layered ragged cloth slabs
    for k in range(4):
        box(nm('rag'), (2.2 - k * 0.2, 0.3, 1.1), loc=(rnd.uniform(-0.2, 0.2), -0.1, 4.6 - k * 0.5), key=rnd.choice(['wh2_rag_a', 'wh2_rag_b']),
            rot=(0, 0, rnd.uniform(-8, 8)), bev=0.1)
    # frayed strips hanging at the hem
    for i in range(8):
        x = -1.0 + 2.0 * i / 7
        box(nm('strip'), (0.22, 0.14, rnd.uniform(0.8, 1.6)), loc=(x, -0.2, 3.0), key=rnd.choice(['wh2_rag_a', 'wh2_rag_b']))
    # sleeves + straw
    for s in (-1, 1):
        cyl(nm('sleeve'), 0.42, armspan * 0.46, loc=(s * armspan * 0.26, 0, armz), key=rnd.choice(['wh2_rag_a', 'wh2_rag_b']), verts=8, rot=(0, 90, 0))
        _straw_tufts(s * armspan * 0.5, 0, armz, rnd, 5, 0.9)
    # head
    ball(nm('head'), 0.95, loc=(0, -0.1, 6.3), key='wh2_sack', segs=9, rings=7, scale=(1, 0.95, 1.1))
    for ex in (-0.33, 0.33):
        box(nm('eye'), (0.2, 0.1, 0.3), loc=(ex, -0.85, 6.4), key='wh2_crow', rot=(0, 0, 20 * (1 if ex > 0 else -1)))
    # crows perched on the arms + one on the hat
    def crow(x, y, z, facing):
        ball(nm('cb'), 0.4, loc=(x, y, z), key='wh2_crow', segs=7, rings=6, scale=(1.5, 0.8, 0.9))
        ball(nm('ch'), 0.26, loc=(x + facing * 0.5, y, z + 0.25), key='wh2_crow', segs=6, rings=5)
        poly_prism(nm('beak'), [(0, 0), (0.28, 0.06), (0, 0.12)], 0.06, loc=(x + facing * 0.78, y, z + 0.27), key='wh2_cob', rot=(90, 0, 90 if facing > 0 else -90))
        box(nm('tail'), (0.5, 0.12, 0.1), loc=(x - facing * 0.5, y, z), key='wh2_crow', rot=(0, 8 * facing, 0))
    crow(-armspan * 0.42, 0, armz + 0.5, 1)
    crow(armspan * 0.38, 0.1, armz + 0.5, -1)
    return finalize('scarecrow_02', smooth_angle=30)


def scarecrow_turnip():
    """E11_03 - tall pole figure with colourful ribbons and a carved turnip head (8-10 high)."""
    reset()
    rnd = random.Random(503)
    H = 9.5
    box(nm('post'), (0.4, 0.4, H), loc=(0, 0, H / 2), key='wood_old', bev=0.03)
    armz, armspan = H - 2.5, 4.4
    box(nm('arm'), (armspan, 0.3, 0.3), loc=(0, 0, armz), key='wood_old', bev=0.03)
    box(nm('arm2'), (armspan * 0.7, 0.26, 0.26), loc=(0, 0, armz - 2.0), key='wood_old', rot=(0, 0, 14), bev=0.03)
    rock(nm('md'), 1.0, (0, 0, 0.1), 'wh2_soil', seed=9, scale=(1.4, 1.4, 0.3))
    # colourful ribbons tied along the arms and post (thin wavy strips)
    cols = ['fabric_red', 'fabric_blue', 'fabric_green', 'fl_yellow', 'fl_pink']
    for i in range(16):
        ax = rnd.uniform(-armspan / 2, armspan / 2)
        az = rnd.choice([armz, armz - 2.0, H * 0.6, H * 0.4])
        col = rnd.choice(cols)
        pts = [(ax, 0, az)]
        for k in range(1, 4):
            pts.append((ax + rnd.uniform(-0.3, 0.3), rnd.uniform(-0.4, 0.4) * k, az - 0.7 * k))
        tube(nm('rib'), pts, 0.06, col, res=2)
    # a few straw tufts at the arm ends
    for s in (-1, 1):
        _straw_tufts(s * armspan * 0.5, 0, armz, rnd, 5, 1.0)
    # carved turnip head (pale, with a jack-o-face)
    lathe(nm('turnip'), [(0, 0), (1.0, 0.3), (1.1, 0.9), (0.7, 1.5), (0, 1.9)], loc=(0, -0.1, H - 0.3), key='wh2_turnip', segs=12)
    # root wisps on top
    for t in range(4):
        tube(nm('root'), [(0, -0.1, H + 1.5), (rnd.uniform(-0.3, 0.3), -0.1 + rnd.uniform(-0.2, 0.2), H + 2.0 + rnd.uniform(0, 0.4))], 0.04, 'wh2_turnip', res=2)
    # carved face (dark recesses)
    for ex in (-0.35, 0.35):
        poly_prism(nm('eye'), [(-0.2, -0.2), (0.2, -0.2), (0, 0.22)], 0.3, loc=(ex, -0.95, H + 0.5), key='wh2_crow', rot=(90, 0, 0))
    poly_prism(nm('nose'), [(-0.14, -0.14), (0.14, -0.14), (0, 0.18)], 0.3, loc=(0, -1.0, H), key='wh2_crow', rot=(90, 0, 0))
    for mx in (-0.4, -0.1, 0.2, 0.5):
        box(nm('tooth'), (0.18, 0.3, 0.22), loc=(mx, -0.95, H - 0.5), key='wh2_crow')
    return finalize('scarecrow_03', smooth_angle=30)


BATCHES = {
    'crops': ('v4_farm', [
        ('E10_01_crop_plot_01', crop_wheat, (1.0, -1.2, 0.5)),
        ('E10_02_crop_plot_02', crop_corn, (1.0, -1.2, 0.5)),
        ('E10_03_crop_plot_03', crop_cabbage, (1.0, -1.3, 0.55)),
        ('E10_04_crop_plot_04', crop_pumpkin, (1.0, -1.3, 0.6)),
        ('E10_05_crop_plot_05', crop_grapes, (1.0, -1.2, 0.5)),
        ('E10_06_crop_plot_06', crop_lavender, (1.0, -1.3, 0.55)),
    ]),
    'scarecrows': ('v4_farm', [
        ('E11_01_scarecrow_01', scarecrow_classic, (1.0, -1.15, 0.45)),
        ('E11_02_scarecrow_02', scarecrow_ragged, (1.0, -1.15, 0.45)),
        ('E11_03_scarecrow_03', scarecrow_turnip, (1.0, -1.15, 0.45)),
    ]),
}
