"""v4_elf3 - treehouse variants B-F. Every one has a real way up (ladder, rope ladder or stairs) with markers.
Natural palette only; warm lanterns. Front -Y. 1 unit = 1 stud.
"""
import math, random
from mathutils import Vector
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus
import v4util as U
from v4_elf import (nm, bark_trunk, trunk_point, roots, limb, cluster, crown, plank_deck, deck_braces, railing,
                    ladder, cabin, lantern, ivy_strand, mushrooms, fern, LEAF)
from nature import rock


def _tree(seed, tr, H, spread=17.0, nlimb=7, crown_z=0.88):
    rnd = random.Random(seed)
    bark_trunk(tr, H, seed=seed)
    roots(tr, n=8, seed=seed)
    tips = []
    for k in range(nlimb):
        az = 2 * math.pi * k / nlimb + rnd.uniform(-0.3, 0.3)
        z0 = H * rnd.uniform(0.6, 0.78)
        p0 = trunk_point(tr, H, seed, z0)
        e = limb((p0[0], p0[1], z0), (math.cos(az), math.sin(az), rnd.uniform(0.3, 0.65)), rnd.uniform(12, 18), tr * 0.34, seed=k)
        tips.append(e)
        e2 = limb((e.x, e.y, e.z), (math.cos(az + rnd.uniform(-0.6, 0.6)), math.sin(az + rnd.uniform(-0.6, 0.6)), rnd.uniform(0.4, 0.9)), rnd.uniform(6, 9), tr * 0.16, seed=k + 20)
        tips.append(e2)
    top = trunk_point(tr, H, seed, H)
    tube(nm('lead'), [(top[0], top[1], H * 0.7), (top[0] + 0.5, top[1], H * 0.9), (top[0], top[1], H + 3)], tr * 0.4, 'ev_bark', res=4, taper=[1, 0.6, 0.25])
    crown(top[0], top[1], H * crown_z, spread, 12.0, seed=seed, count=30)
    for i, e in enumerate(tips):
        cluster(e.x, e.y, e.z + 1.5, rnd.uniform(4.6, 6.2), seed=seed * 50 + i, n=6)
    return rnd


def _ground_access(cx, cy, deck_z, deck_r, lad_a, lamps=True):
    """Vertical wooden ladder from the ground to just above the deck rim, tied to the rim, with lantern posts at the opening."""
    lx, ly = cx + math.cos(lad_a) * (deck_r + 0.55), cy + math.sin(lad_a) * (deck_r + 0.55)
    ladder(lx, ly, 0.0, deck_z + 3.2, lad_a)
    tx, ty = -math.sin(lad_a), math.cos(lad_a)
    for side in (-1, 1):
        px, py = lx + tx * side * 1.15, ly + ty * side * 1.15
        for zz in (deck_z - 0.9, deck_z * 0.5):
            tube(nm('tie'), [(px, py, zz), (cx + math.cos(lad_a) * (deck_r - 0.5) + tx * side * 1.15, cy + math.sin(lad_a) * (deck_r - 0.5) + ty * side * 1.15, zz + 0.35)], 0.13, 'ev_wood_dark', res=4)
    if lamps:
        for side in (-1, 1):
            a = lad_a + side * 0.2
            px, py = cx + math.cos(a) * (deck_r - 0.35), cy + math.sin(a) * (deck_r - 0.35)
            cyl(nm('lps'), 0.1, 1.3, loc=(px, py, deck_z + 3.0), key='ev_wood_dark', verts=6)
            lantern(px, py, deck_z + 4.3 + 0.9, s=0.8, hang=False)
    U.marker('mk_lb', (lx, ly, 0.3))
    U.marker('mk_lt', (lx, ly, deck_z + 3.0))
    return lx, ly


def _rope_ladder(x, y, z0, z1, ang, width=2.0):
    c, s = math.cos(ang), math.sin(ang)
    tx, ty = -s, c
    for side in (-1, 1):
        px, py = x + tx * side * width / 2, y + ty * side * width / 2
        tube(nm('rp'), [(px, py, z1), (px + 0.05 * side, py, (z0 + z1) / 2), (px, py, z0 + 0.4)], 0.09, 'rope', res=4, ures=3)
        ball(nm('kn'), 0.19, loc=(px, py, z1 - 0.1), key='rope_dark', segs=6, rings=4)
    n = int((z1 - z0 - 1.0) / 1.0)
    for i in range(n + 1):
        zz = z0 + 0.8 + i * 1.0
        r = cyl(nm('rg'), 0.095, width + 0.24, loc=(x - tx * (width / 2 + 0.12), y - ty * (width / 2 + 0.12), zz), key='ev_wood_light', verts=8)
        r.rotation_euler = Vector((tx, ty, 0)).to_track_quat('Z', 'Y').to_euler()
    box(nm('ft'), (width + 0.6, 0.5, 0.3), loc=(x, y, z0 + 0.15), key='ev_wood_dark', rot=(0, 0, math.degrees(ang) + 90), bev=0.05)


def _door_toward(cx, cy, tx, ty):
    return math.atan2(ty - cy, tx - cx)


def _ground_bits(tr, rnd, seed):
    mushrooms(tr * 1.5, -tr * 1.2, 0.0, 5, seed=seed)
    fern(-tr * 2.0, tr * 1.4, 0.0, seed=seed)
    fern(tr * 2.4, tr * 0.8, 0.0, seed=seed + 1)
    for i in range(4):
        a = rnd.uniform(0, 6.28); d = tr * rnd.uniform(2.6, 3.8)
        rock(nm('gr'), rnd.uniform(0.6, 1.2), (math.cos(a) * d, math.sin(a) * d, 0.0), 'ev_stone_dark', seed=i)


def _ivy_rim(cx, cy, z, R, rnd, lad_a, n=10):
    for i in range(n):
        a = rnd.uniform(0, 6.28)
        if abs(((a - lad_a + math.pi) % (2 * math.pi)) - math.pi) < 0.5:
            continue
        ivy_strand((cx + math.cos(a) * (R - 0.1), cy + math.sin(a) * (R - 0.1), z - 0.6), rnd.uniform(2.5, 5.5), seed=i)


# ------------------------------------------------------------------ B: two decks, ladder between them
def treehouse_b():
    seed, tr, H = 5, 3.6, 62.0
    reset()
    rnd = _tree(seed, tr, H, spread=19.0)
    z1, r1 = 15.0, 13.5
    c1 = trunk_point(tr, H, seed, z1)
    plank_deck(c1[0], c1[1], z1, r1, seed=seed)
    deck_braces(c1[0], c1[1], z1, r1, tr * 1.05, seed=seed)
    lad1 = math.radians(25)
    railing(c1[0], c1[1], z1, r1, gap_a=lad1, gap_w=0.16)
    cab_a = lad1 + math.pi * 0.85
    cd = tr * 0.9 + 4.6 + 1.0
    cc = (c1[0] + math.cos(cab_a) * cd, c1[1] + math.sin(cab_a) * cd)
    lx, ly = _ground_access(c1[0], c1[1], z1, r1, lad1)
    d1 = _door_toward(cc[0], cc[1], lx, ly)
    cabin(cc[0], cc[1], z1, 4.6, 6.6, d1, seed=seed, windows=2)
    lantern_xy = (cc[0] + math.cos(d1) * 5.6 + math.sin(d1) * 2.2, cc[1] + math.sin(d1) * 5.6 - math.cos(d1) * 2.2)
    cyl(nm('dlp'), 0.13, 4.2, loc=(lantern_xy[0], lantern_xy[1], z1), key='ev_wood_dark', verts=6)
    lantern(lantern_xy[0], lantern_xy[1], z1 + 4.2 + 1.12, s=1.0, hang=False)
    U.marker('mk_door', (cc[0] + math.cos(d1) * 5.1, cc[1] + math.sin(d1) * 5.1, z1 + 2.0))
    # upper deck
    z2, r2 = 37.0, 9.2
    c2 = trunk_point(tr, H, seed, z2)
    plank_deck(c2[0], c2[1], z2, r2, seed=seed + 1)
    deck_braces(c2[0], c2[1], z2, r2, tr * 0.98, n=5, drop=5.5, seed=seed + 1)
    up_a = math.radians(160)
    railing(c2[0], c2[1], z2, r2, gap_a=up_a, gap_w=0.2)
    ux, uy = c2[0] + math.cos(up_a) * (r2 + 0.5), c2[1] + math.sin(up_a) * (r2 + 0.5)
    ladder(ux, uy, z1, z2 + 3.2, up_a)
    for side in (-1, 1):
        tx, ty = -math.sin(up_a), math.cos(up_a)
        px, py = ux + tx * side * 1.15, uy + ty * side * 1.15
        tube(nm('tie'), [(px, py, z2 - 0.9), (c2[0] + math.cos(up_a) * (r2 - 0.5) + tx * side * 1.15, c2[1] + math.sin(up_a) * (r2 - 0.5) + ty * side * 1.15, z2 - 0.5)], 0.13, 'ev_wood_dark', res=4)
    U.marker('mk_lb', (ux, uy, z1 + 0.3))
    U.marker('mk_lt', (ux, uy, z2 + 3.0))
    ca2 = up_a + math.pi * 0.9
    cc2 = (c2[0] + math.cos(ca2) * (tr * 0.9 + 3.4 + 0.8), c2[1] + math.sin(ca2) * (tr * 0.9 + 3.4 + 0.8))
    d2 = _door_toward(cc2[0], cc2[1], ux, uy)
    cabin(cc2[0], cc2[1], z2, 3.4, 5.6, d2, seed=seed + 2, windows=2)
    U.marker('mk_door', (cc2[0] + math.cos(d2) * 3.9, cc2[1] + math.sin(d2) * 3.9, z2 + 2.0))
    U.marker('mk_deck', (c1[0], c1[1], z1 + 0.4))
    U.marker('mk_deck', (c2[0], c2[1], z2 + 0.4))
    _ivy_rim(c1[0], c1[1], z1, r1, rnd, lad1, 9)
    _ground_bits(tr, rnd, seed)
    return finalize('ev_treehouse_b', smooth_angle=38)


# ------------------------------------------------------------------ C: small house, rope ladder
def treehouse_c():
    seed, tr, H = 7, 2.6, 40.0
    reset()
    rnd = _tree(seed, tr, H, spread=14.0, nlimb=6)
    zd, R = 17.0, 10.5
    c = trunk_point(tr, H, seed, zd)
    plank_deck(c[0], c[1], zd, R, seed=seed)
    deck_braces(c[0], c[1], zd, R, tr * 1.05, n=5, drop=5.5, seed=seed)
    lad = math.radians(200)
    railing(c[0], c[1], zd, R, gap_a=lad, gap_w=0.2)
    lx, ly = c[0] + math.cos(lad) * (R + 0.4), c[1] + math.sin(lad) * (R + 0.4)
    _rope_ladder(lx, ly, 0.0, zd + 2.8, lad)
    # rope ladder tied at two rail posts
    for side in (-1, 1):
        a = lad + side * 0.2
        px, py = c[0] + math.cos(a) * (R - 0.35), c[1] + math.sin(a) * (R - 0.35)
        cyl(nm('ps'), 0.13, 3.4, loc=(px, py, zd), key='ev_wood_dark', verts=6)
        lantern(px, py, zd + 3.4 + 1.0, s=0.7, hang=False)
    U.marker('mk_lb', (lx, ly, 0.3))
    U.marker('mk_lt', (lx, ly, zd + 2.6))
    ca = lad + math.pi * 0.8
    cr = 3.7
    cc = (c[0] + math.cos(ca) * (tr * 0.9 + cr + 0.9), c[1] + math.sin(ca) * (tr * 0.9 + cr + 0.9))
    d = _door_toward(cc[0], cc[1], lx, ly)
    cabin(cc[0], cc[1], zd, cr, 5.8, d, seed=seed, windows=2)
    U.marker('mk_door', (cc[0] + math.cos(d) * (cr + 0.5), cc[1] + math.sin(d) * (cr + 0.5), zd + 2.0))
    U.marker('mk_deck', (c[0], c[1], zd + 0.4))
    # drying herbs and a bucket on a hook
    for i in range(4):
        x = cc[0] + math.cos(d + 0.9) * (cr + 0.3) + i * 0.35 * math.cos(d + 1.57)
        y = cc[1] + math.sin(d + 0.9) * (cr + 0.3) + i * 0.35 * math.sin(d + 1.57)
        ball(nm('hb'), 0.24, loc=(x, y, zd + 4.2), key=rnd.choice(('ev_leaf_a', 'ev_leaf_c')), segs=6, rings=4, scale=(0.7, 0.7, 1.4))
    _ivy_rim(c[0], c[1], zd, R, rnd, lad, 8)
    _ground_bits(tr, rnd, seed)
    return finalize('ev_treehouse_c', smooth_angle=38)


# ------------------------------------------------------------------ D: wide hall deck, two cabins
def treehouse_d():
    seed, tr, H = 9, 4.2, 56.0
    reset()
    rnd = _tree(seed, tr, H, spread=21.0, nlimb=8)
    zd, R = 22.0, 18.5
    c = trunk_point(tr, H, seed, zd)
    plank_deck(c[0], c[1], zd, R, seed=seed)
    deck_braces(c[0], c[1], zd, R, tr * 1.05, n=8, drop=8.0, seed=seed)
    lad = math.radians(-100)
    railing(c[0], c[1], zd, R, gap_a=lad, gap_w=0.13)
    lx, ly = _ground_access(c[0], c[1], zd, R, lad)
    for k, (ca, cr, ch) in enumerate(((lad + math.pi * 0.62, 5.6, 7.4), (lad - math.pi * 0.62, 4.5, 6.4))):
        cd = tr * 0.9 + cr + 2.2
        cc = (c[0] + math.cos(ca) * cd, c[1] + math.sin(ca) * cd)
        d = _door_toward(cc[0], cc[1], c[0] + math.cos(lad) * 4, c[1] + math.sin(lad) * 4)
        cabin(cc[0], cc[1], zd, cr, ch, d, seed=seed + k, windows=3)
        U.marker('mk_door', (cc[0] + math.cos(d) * (cr + 0.5), cc[1] + math.sin(d) * (cr + 0.5), zd + 2.0))
    U.marker('mk_deck', (c[0], c[1], zd + 0.4))
    # long table and benches between the cabins (gathering hall deck)
    ta = lad + math.pi
    tx, ty = c[0] + math.cos(ta) * 9.5, c[1] + math.sin(ta) * 9.5
    box(nm('tbl'), (5.6, 1.7, 0.2), loc=(tx, ty, zd + 1.7), key='ev_wood_light', rot=(0, 0, math.degrees(ta) + 90), bev=0.04)
    for sx in (-2.2, 2.2):
        for sy in (-0.6, 0.6):
            cyl(nm('tl'), 0.1, 1.6, loc=(tx + math.cos(ta + 1.57) * sx + math.cos(ta) * sy, ty + math.sin(ta + 1.57) * sx + math.sin(ta) * sy, zd), key='ev_wood_dark', verts=6)
    for off in (-1.5, 1.5):
        bx, by = tx + math.cos(ta) * off, ty + math.sin(ta) * off
        box(nm('bn'), (5.0, 0.6, 0.18), loc=(bx, by, zd + 1.0), key='ev_wood', rot=(0, 0, math.degrees(ta) + 90), bev=0.03)
        for sx in (-2.0, 2.0):
            cyl(nm('bl'), 0.09, 0.95, loc=(bx + math.cos(ta + 1.57) * sx, by + math.sin(ta + 1.57) * sx, zd), key='ev_wood_dark', verts=6)
    # lantern string over the table
    pts = [(tx + math.cos(ta + 1.57) * -3.2, ty + math.sin(ta + 1.57) * -3.2, zd + 5.6), (tx, ty, zd + 5.0), (tx + math.cos(ta + 1.57) * 3.2, ty + math.sin(ta + 1.57) * 3.2, zd + 5.6)]
    for p in (pts[0], pts[2]):
        cyl(nm('sp'), 0.12, 5.6, loc=(p[0], p[1], zd), key='ev_wood_dark', verts=6)
    tube(nm('str'), pts, 0.07, 'rope', res=4, ures=4)
    for p in (pts[1], ((pts[0][0] + pts[1][0]) / 2, (pts[0][1] + pts[1][1]) / 2, zd + 5.2), ((pts[2][0] + pts[1][0]) / 2, (pts[2][1] + pts[1][1]) / 2, zd + 5.2)):
        lantern(p[0], p[1], p[2] - 0.4, s=0.55, hang=True)
    _ivy_rim(c[0], c[1], zd, R, rnd, lad, 12)
    _ground_bits(tr, rnd, seed)
    return finalize('ev_treehouse_d', smooth_angle=38)


# ------------------------------------------------------------------ E: cabin built around the trunk
def treehouse_e():
    seed, tr, H = 11, 3.4, 54.0
    reset()
    rnd = _tree(seed, tr, H, spread=18.0)
    zd, R = 20.0, 12.5
    c = trunk_point(tr, H, seed, zd)
    plank_deck(c[0], c[1], zd, R, seed=seed)
    deck_braces(c[0], c[1], zd, R, tr * 1.05, n=7, drop=7.0, seed=seed)
    lad = math.radians(70)
    railing(c[0], c[1], zd, R, gap_a=lad, gap_w=0.17)
    lx, ly = _ground_access(c[0], c[1], zd, R, lad)
    cr = tr + 3.6
    d = _door_toward(c[0], c[1], lx, ly)
    cabin(c[0], c[1], zd, cr, 7.0, d, seed=seed, windows=3, roof_rise=cr * 0.9)
    U.marker('mk_door', (c[0] + math.cos(d) * (cr + 0.5), c[1] + math.sin(d) * (cr + 0.5), zd + 2.0))
    U.marker('mk_deck', (c[0], c[1], zd + 0.4))
    # trunk pierces the roof: collar of bark and a few climbing roots over the stave wall
    for i in range(5):
        a = 2 * math.pi * i / 5 + 0.4
        tube(nm('cr'), [(c[0] + math.cos(a) * (cr + 0.05), c[1] + math.sin(a) * (cr + 0.05), zd + 0.4), (c[0] + math.cos(a + 0.3) * (cr + 0.35), c[1] + math.sin(a + 0.3) * (cr + 0.35), zd + 3.2),
                         (c[0] + math.cos(a + 0.2) * (cr + 0.1), c[1] + math.sin(a + 0.2) * (cr + 0.1), zd + 6.0)], 0.2, 'ev_bark', res=4, taper=[1, 0.7, 0.4], ures=3)
    # flower boxes under the windows
    for k, off in enumerate((1.25, -1.25, 2.4)):
        a = d + off + math.pi
        if abs(((a - d + math.pi) % (2 * math.pi)) - math.pi) < 0.8:
            continue
        fx, fy = c[0] + math.cos(a) * (cr + 0.45), c[1] + math.sin(a) * (cr + 0.45)
        box(nm('fb'), (1.9, 0.6, 0.55), loc=(fx, fy, zd + 2.3), key='ev_wood_dark', rot=(0, 0, math.degrees(a) + 90), bev=0.04)
        for j in range(4):
            ball(nm('fl'), 0.22, loc=(fx + math.cos(a + 1.57) * (j - 1.5) * 0.4, fy + math.sin(a + 1.57) * (j - 1.5) * 0.4, zd + 2.75), key=rnd.choice(('ev_leaf_a', 'ev_leaf_c', 'fl_white')), segs=6, rings=4)
    _ivy_rim(c[0], c[1], zd, R, rnd, lad, 10)
    _ground_bits(tr, rnd, seed)
    return finalize('ev_treehouse_e', smooth_angle=38)


# ------------------------------------------------------------------ F: spiral staircase around the outside
def treehouse_f():
    seed, tr, H = 13, 3.2, 52.0
    reset()
    rnd = _tree(seed, tr, H, spread=17.0)
    zd, R = 24.0, 11.0
    c = trunk_point(tr, H, seed, zd)
    plank_deck(c[0], c[1], zd, R, seed=seed)
    deck_braces(c[0], c[1], zd, R, tr * 1.05, n=6, drop=7.0, seed=seed)
    # spiral stair winding around the outside of the deck footprint, 1.1 turns
    turns, n = 1.1, 46
    r_in, r_out = R + 0.35, R + 3.5
    mid = (r_in + r_out) / 2
    rise = zd / n
    a0 = math.radians(215)
    pts_rail, pts_end = [], None
    for i in range(n):
        a = a0 - 2 * math.pi * turns * (i / (n - 1))   # climb clockwise
        z = rise * (i + 1)
        cc = trunk_point(tr, H, seed, min(z, zd))
        px, py = cc[0] + math.cos(a) * mid, cc[1] + math.sin(a) * mid
        dth = 2 * math.pi * turns / n
        box(nm('st'), (r_out - r_in, mid * dth * 1.15, 0.3), loc=(px, py, z - 0.15), key=('ev_wood' if i % 2 else 'ev_wood_light'), rot=(0, 0, math.degrees(a)), bev=0.03)
        if i % 3 == 0:
            ox, oy = cc[0] + math.cos(a) * (r_out - 0.15), cc[1] + math.sin(a) * (r_out - 0.15)
            cyl(nm('sp'), 0.11, 3.0, loc=(ox, oy, z), key='ev_wood', verts=6)
            if i % 6 == 0:
                cyl(nm('sk'), 0.2, z, loc=(ox, oy, 0.0), key='ev_bark', verts=6)
        pts_rail.append((cc[0] + math.cos(a) * (r_out - 0.15), cc[1] + math.sin(a) * (r_out - 0.15), z + 3.0))
        pts_end = (a, cc, z)
    tube(nm('hr'), pts_rail, 0.14, 'ev_wood_light', res=4, ures=2)
    tube(nm('hr2'), [(p[0], p[1], p[2] - 1.5) for p in pts_rail], 0.08, 'ev_wood', res=4, ures=2)
    a_end, c_end, z_end = pts_end
    # inner rail only on the upper part so the deck side stays open at the landing
    railing(c[0], c[1], zd, R, gap_a=a_end, gap_w=0.32)
    # landing slab bridging the last step to the deck
    lx, ly = c_end[0] + math.cos(a_end) * (R + 0.2), c_end[1] + math.sin(a_end) * (R + 0.2)
    box(nm('lnd'), (1.6, 3.4, 0.3), loc=(lx, ly, zd - 0.15), key='ev_wood', rot=(0, 0, math.degrees(a_end)), bev=0.03)
    # cabin
    ca = a_end + math.pi * 0.85
    cr = 4.4
    cd = tr * 0.9 + cr + 1.0
    cc = (c[0] + math.cos(ca) * cd, c[1] + math.sin(ca) * cd)
    d = _door_toward(cc[0], cc[1], lx, ly)
    cabin(cc[0], cc[1], zd, cr, 6.8, d, seed=seed, windows=2)
    U.marker('mk_door', (cc[0] + math.cos(d) * (cr + 0.5), cc[1] + math.sin(d) * (cr + 0.5), zd + 2.0))
    U.marker('mk_deck', (c[0], c[1], zd + 0.4))
    bx0 = c_end[0] + math.cos(a0) * mid
    by0 = c_end[1] + math.sin(a0) * mid
    # ground end of stair: marker and a small step-off stone
    c0 = trunk_point(tr, H, seed, 0.0)
    gx, gy = c0[0] + math.cos(a0) * mid, c0[1] + math.sin(a0) * mid
    U.marker('mk_lb', (gx, gy, 0.3))
    U.marker('mk_lt', (lx, ly, zd + 0.3))
    for side in (-1, 1):
        a = a_end + side * 0.28
        px, py = c[0] + math.cos(a) * (R - 0.35), c[1] + math.sin(a) * (R - 0.35)
        cyl(nm('lps'), 0.1, 1.3, loc=(px, py, zd + 3.0), key='ev_wood_dark', verts=6)
        lantern(px, py, zd + 4.3 + 0.9, s=0.8, hang=False)
    _ivy_rim(c[0], c[1], zd, R, rnd, a_end, 8)
    _ground_bits(tr, rnd, seed)
    return finalize('ev_treehouse_f', smooth_angle=38)


BATCH_TREEHOUSES = [
    ('D01_02_treehouse_b', treehouse_b),
    ('D01_03_treehouse_c', treehouse_c),
    ('D01_04_treehouse_d', treehouse_d),
    ('D01_05_treehouse_e', treehouse_e),
    ('D01_06_treehouse_f', treehouse_f),
]
