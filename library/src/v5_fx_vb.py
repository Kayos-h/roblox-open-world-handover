"""v5_fx_vb - FIX ROUND builder for assignment A6 (worker vb). Owner: builder A6.
Replaces round-1 vb WT08_02 wizard study bed (MINOR: bare frame -> furnished four-poster with bedding, pillows, drapery folds, rug, side table).
Reuses the round-1 wizard palette via v5kit.wiz_pal('vb') (registered by ORIG import). New keys only under vb_f_.
No glow. Front -Y, pivot bottom centre. 18 x 14 x 12.
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
import v5_vb as ORIG          # round-1 module: registers the vb_ wizard palette + books; never edit it

K = ORIG.K                     # includes 'glass','wax','ring' plus the WIZ keys under vb_

P = G.reg('vb_f', {
    'quilt':    ((72, 92, 150),  'Fabric', 0.0, 0.92),     # deep blue quilt
    'quilt_d':  ((54, 70, 120),  'Fabric', 0.0, 0.93),     # fold shadow
    'sheet':    ((230, 224, 206), 'Fabric', 0.0, 0.9),     # cream sheet turn-down
    'pillow':   ((236, 230, 214), 'Fabric', 0.0, 0.9),
    'drape':    ((96, 60, 120),  'Fabric', 0.0, 0.95),     # muted plum canopy drape
    'drape_d':  ((74, 46, 94),   'Fabric', 0.0, 0.96),
    'rug':      ((150, 70, 64),  'Fabric', 0.0, 1.0),
    'rug_trim': ((198, 170, 110),'Fabric', 0.0, 1.0),
    'wood':     ((96, 62, 44),   'Wood', 0.0, 0.85),
    'plank_a':  ((118, 80, 54),  'WoodPlanks', 0.0, 0.88),   # back planking (warm brown, not flat dark-red)
    'plank_b':  ((98, 66, 44),   'WoodPlanks', 0.0, 0.9),
    'frame':    ((80, 52, 36),   'Wood', 0.0, 0.9),          # rear frame rails / buttresses
    'peg':      ((150, 120, 70), 'Metal', 0.3, 0.5),         # iron pegs / brackets
})


def _fin(A, name):
    A.to_scene()
    return finalize(name, 25)


def study_bed():
    """WT08_02 - furnished four-poster: carved posts, canopy with draped valance, quilt with folds, turned-down sheet, pillows, bedside table and rug."""
    reset()
    A = Acc()
    rnd = random.Random(2802)
    # rug under the bed
    A.box((17.0, 13.0, 0.12), (0, 0, 0.06), P['rug'])
    A.box((15.2, 11.2, 0.16), (0, 0, 0.1), P['rug_trim'])
    A.box((13.6, 9.8, 0.2), (0, 0, 0.12), P['rug'])
    # four carved posts + finials
    for sx in (-8.0, 8.0):
        for sy in (-6.0, 6.0):
            A.cyl(0.6, 11.0, (sx, sy, 0.2), K['timber'], verts=10, r2=0.5)
            for z in (3.0, 6.0, 9.0):
                A.sweep([(0.6, -0.2), (0.85, -0.2), (0.85, 0.2), (0.6, 0.2)], 0, 360, 10, K['timber'], loc=(sx, sy, z))
            A.ball(0.8, (sx, sy, 11.4), K['brass'], segs=8, rings=5)
    # bed base, mattress
    A.box((16.0, 12.6, 1.6), (0, 0, 2.0), P['wood'])
    A.box((15.2, 11.8, 1.6), (0, 0, 3.4), P['sheet'])                       # mattress
    # quilt with modelled folds (rows of alternating depth, not a flat slab)
    for k in range(7):
        y = -5.2 + k * 1.6
        dz = 0.5 + 0.18 * (k % 2)
        A.box((15.4, 1.5, dz), (0, y, 4.3 + 0.1 * (k % 2)), P['quilt'] if k % 2 else P['quilt_d'], bev=0.12)
    # turned-down cream sheet at the head
    A.box((15.4, 2.6, 0.5), (0, 4.6, 4.5), P['sheet'], bev=0.1)
    A.box((15.4, 0.8, 0.3), (0, 3.4, 4.8), P['sheet'], bev=0.1)
    # two pillows
    for sx in (-3.8, 3.8):
        A.box((5.6, 3.0, 1.2), (sx, 4.6, 5.0), P['pillow'], bev=0.3)
    # headboard
    A.box((16.6, 0.8, 5.0), (0, 6.3, 5.5), K['timber'], bev=0.1)
    A.box((14.0, 0.5, 3.0), (0, 6.0, 5.5), P['wood'], bev=0.1)
    # canopy top frame + draped valance (folds) + corner swags
    for sg in (-1, 1):
        A.beam((-8.0, sg * 6.0, 11.0), (8.0, sg * 6.0, 11.0), 0.35, 0.35, K['timber'])
        A.beam((sg * 8.0, -6.0, 11.0), (sg * 8.0, 6.0, 11.0), 0.35, 0.35, K['timber'])
    A.box((16.8, 13.0, 0.5), (0, 0, 11.3), P['drape'])                      # canopy cloth
    # draped valance hanging from the frame, scalloped folds on all four sides
    for sg in (-1, 1):
        for k in range(8):
            x = -7.0 + k * 2.0
            A.box((1.4, 0.4, 2.2 - 0.3 * (k % 2)), (x, sg * 6.2, 9.9), P['drape'] if k % 2 else P['drape_d'], bev=0.08)
        for k in range(6):
            y = -5.0 + k * 2.0
            A.box((0.4, 1.4, 2.2 - 0.3 * (k % 2)), (sg * 8.2, y, 9.9), P['drape'] if k % 2 else P['drape_d'], bev=0.08)
    # tied-back corner curtains at the head posts
    for sx in (-8.0, 8.0):
        A.box((0.6, 1.4, 7.0), (sx, 5.4, 6.5), P['drape_d'], bev=0.1)
        A.sweep([(0.5, -0.1), (0.9, -0.1), (0.9, 0.1), (0.5, 0.1)], 0, 360, 8, K['brass'], loc=(sx, 5.4, 5.0))
    # bedside table with a candle (no glow) and a book
    A.box((3.4, 3.0, 0.4), (-10.6, -3.0, 4.2), P['wood'])
    for sx in (-11.8, -9.4):
        for sy in (-4.0, -2.0):
            A.box((0.4, 0.4, 4.0), (sx, sy, 2.0), P['wood'])
    A.cyl(0.3, 0.5, (-10.6, -3.0, 4.4), K['brass'], verts=8)
    A.cyl(0.18, 1.0, (-10.6, -3.0, 4.8), K['wax'], verts=8)
    A.box((1.6, 1.1, 0.4), (-10.2, -2.4, 4.4), ORIG.BOOK[1], (0, 0, 12))
    return _fin(A, 'wizard_study_bed')


def bay_1():
    """WT03_01 - curved full-height bookshelf hugging a round wall (R=38, chord 24). FRONT (toward tower axis) holds books;
    the BACK outer arc, previously a flat dark-red slab, is now finished: warm vertical plank boarding with rear frame
    rails, three buttress ribs and iron pegs, so the back view reads as built joinery, not a blank panel."""
    reset()
    A = Acc()
    rnd = random.Random(70)
    R, chord = 38.0, 24.0
    depth, H = 3.4, 28.0
    loc = (0, -R, 0)
    half = math.degrees(chord / 2.0 / R)
    a0, a1 = 90.0 - half, 90.0 + half
    n = max(6, int((a1 - a0) / 3.0))
    Pp = lambda r, ang, z: (r * math.cos(math.radians(ang)), -R + r * math.sin(math.radians(ang)), z)
    # carcase: inner book wall + base plinth + cornice (as round 1)
    A.sweep([(R - 0.7, 0), (R, 0), (R, H), (R - 0.7, H)], a0, a1, n, K['timber'], loc=loc)        # the thin inner backing (books lean on it)
    A.sweep([(R - depth - 0.3, 0), (R + 0.2, 0), (R + 0.2, 1.3), (R - depth - 0.3, 1.3)], a0, a1, n, K['granite'], loc=loc)
    A.sweep([(R - depth - 0.7, H - 1.2), (R + 0.2, H - 1.2), (R + 0.2, H), (R - depth - 0.7, H)], a0, a1, n, K['limestone'], loc=loc)
    zs = [1.3 + k * 3.75 for k in range(7)]
    for z in zs:                                                                                  # shelf boards
        A.sweep([(R - depth, z), (R - 0.7, z), (R - 0.7, z + 0.5), (R - depth, z + 0.5)], a0, a1, n, K['ochre'], loc=loc)
    for ang in (a0, a1):                                                                           # carved end panels
        x, y, _ = Pp(R - depth / 2.0, ang, H / 2.0)
        A.box((depth, 0.8, H), (x, y, H / 2.0), K['timber'], (0, 0, ang))
    # books on the shelves
    length = math.radians(a1 - a0 - 2.4) * (R - 2.2)
    def place(s, db):
        ang = a0 + 1.2 + math.degrees(s / (R - 2.2))
        return (*Pp(R - 0.9 - db / 2.0, ang, 0)[:2], ang)
    for z in zs[:-1]:
        ORIG._fill_books(A, rnd, place, length, z + 0.5, 3.3, (2.7, 3.7), ORIG.BOOK, 0.06)
    # rolling-ladder rail (keeps the WT03_01 marker character)
    pts = [Pp(R - depth - 0.35, a0 + (a1 - a0) * t / 12.0, 25.2) for t in range(13)]
    for p0, p1 in zip(pts, pts[1:]):
        A.beam(p0, p1, 0.28, 0.28, K['brass'])
    # ---- FINISHED BACK: the outer arc (radius ~R+0.2, facing +Y) gets plank boarding + frame, not a flat slab ----
    nb = 16
    for b in range(nb):
        ang = a0 + (a1 - a0) * (b + 0.5) / nb
        key = P['plank_a'] if b % 2 else P['plank_b']
        # a vertical plank board standing proud of the outer arc
        A.sweep([(R + 0.15, 0.6), (R + 0.9, 0.6), (R + 0.9, H - 0.6), (R + 0.15, H - 0.6)],
                ang - (a1 - a0) / nb * 0.44, ang + (a1 - a0) / nb * 0.44, 1, key, loc=loc)
    # three horizontal rear frame rails (top, middle, bottom) banding the planks
    for z in (1.6, H / 2.0, H - 2.0):
        A.sweep([(R + 0.1, z - 0.6), (R + 1.2, z - 0.6), (R + 1.2, z + 0.6), (R + 0.1, z + 0.6)], a0 - 0.5, a1 + 0.5, n, P['frame'], loc=loc)
    # two vertical buttress ribs + the two end stiles, with iron pegs
    for ang in (a0 + (a1 - a0) * 0.33, a0 + (a1 - a0) * 0.66, a0, a1):
        x, y, _ = Pp(R + 0.7, ang, H / 2.0)
        A.box((1.1, 1.4, H - 1.0), (x, y, H / 2.0), P['frame'], (0, 0, ang), bev=0.08)
        for z in (4.0, 12.0, 20.0, 25.0):
            px, py, _ = Pp(R + 1.3, ang, z)
            A.cyl(0.22, 0.5, (px, py, z), P['peg'], verts=6, rot=(90, 0, ang))
    # a slim skirting + cornice on the back so top and bottom edges read finished
    A.sweep([(R + 0.1, 0), (R + 1.4, 0), (R + 1.4, 1.1), (R + 0.1, 1.1)], a0 - 0.5, a1 + 0.5, n, P['frame'], loc=loc)
    A.sweep([(R + 0.1, H - 1.0), (R + 1.5, H - 1.0), (R + 1.5, H), (R + 0.1, H)], a0 - 0.5, a1 + 0.5, n, K['timber'], loc=loc)
    A.to_scene()
    return finalize('wizard_bookshelf_curved', 25)


def _bay_post(R, chord, H=28.0):
    def post(A):
        half = math.degrees(chord / 2.0 / R)
        a0, a1 = 90.0 - half, 90.0 + half
        for q in range(7):
            ang = a0 + (a1 - a0) * q / 6.0
            x = (R + 0.25) * math.cos(math.radians(ang))
            y = -R + (R + 0.25) * math.sin(math.radians(ang))
            A.box((0.5, 0.8, H - 3.0), (x, y, H / 2.0), VB.K['ochre'], (0, 0, ang), bev=0.05)
        n = max(4, int((a1 - a0) / 4.0))
        for z in (6.0, 14.0, 22.0):
            A.sweep([(R + 0.1, z), (R + 0.6, z), (R + 0.6, z + 0.7), (R + 0.1, z + 0.7)], a0, a1, n, VB.K['limestone'], loc=(0, -R, 0))
    return post


def _shelf1_post(A):
    width, H, depth = 14.0, 26.0, 4.6
    A.box((width - 0.4, 0.4, H - 2.2), (0, depth / 2.0 + 0.2, H / 2.0 + 0.2), VB.K['timber'], bev=0.05)
    for k in range(5):
        A.box((0.5, 0.3, H - 4.5), (-width / 2.0 + 2.0 + k * (width - 4.0) / 4.0, depth / 2.0 + 0.55, H / 2.0), VB.K['ochre'], bev=0.04)
    A.box((width + 0.4, 0.8, 0.7), (0, depth / 2.0 + 0.4, H - 1.0), VB.K['limestone'], bev=0.05)


def _shelf2_post(A):
    width, H = 14.0, 26.0
    for sx in (-1, 1):
        A.box((1.4, 1.4, 1.6), (sx * (width / 2.0 - 0.8), 0, H + 0.8), VB.K['limestone'], bev=0.08)
        A.cyl(0.5, 1.4, (sx * (width / 2.0 - 0.8), 0, H + 2.4), VB.K['brass'], verts=8, r2=0.1)


def wt03_02():
    return LK.wrap(VB.bay_2, post=_bay_post(30.0, 22.0))()


def wt03_03():
    return LK.wrap(VB.bay_3, post=_bay_post(22.0, 20.0))()


def wt04_01():
    return LK.wrap(VB.shelf_1, post=_shelf1_post)()


def wt04_02():
    return LK.wrap(VB.shelf_2, post=_shelf2_post)()


BATCHES = {
    'study': ('v5_wizard', mk([
        ('WT08_02_wizard_study_set_02', study_bed),
        ('WT03_01_wizard_bookshelf_curved_01', bay_1)], 0.1)),
}


# --- lead4 registration ---
import v5_leadkit as LK
import v5_vb as VB
BATCHES['lead4_vb'] = ('v5_wizard', mk([('WT03_02_wizard_bookshelf_curved_02', wt03_02), ('WT03_03_wizard_bookshelf_curved_03', wt03_03),
                                        ('WT04_01_wizard_bookshelf_straight_01', wt04_01), ('WT04_02_wizard_bookshelf_straight_02', wt04_02)], 0.1))
