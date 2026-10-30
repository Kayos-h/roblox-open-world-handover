"""v4_elf2 - elven climbing and lighting set (ladders, stairs, lanterns). Natural woods, rope, bronze; warm glow only.
Front faces -Y. 1 unit = 1 stud. Ladder pieces record ladder_bottom / ladder_top markers.
"""
import math, random
import bmesh
from mathutils import Vector, noise
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, _obj_from_bm, mat
import v4util as U
from v4_elf import nm, lantern, roots

LIST_ROPE = 'rope'


def _rung(x0, y, z, length, r=0.1, key='ev_wood_light'):
    """Horizontal round rung along +X starting at x0."""
    return cyl(nm('rg'), r, length, loc=(x0, y, z), key=key, verts=8, rot=(0, 90, 0))


def _rope_ladder(H, spacing, width=2.2, name='rope_ladder'):
    reset()
    box(nm('bm'), (width + 1.8, 0.8, 0.65), loc=(0, 0, H + 0.33), key='ev_wood_dark', bev=0.07)
    for s in (-1, 1):
        x = s * width / 2
        tube(nm('rp'), [(x, 0, H), (x + 0.06 * s, 0, H * 0.5), (x, 0, 0.5)], 0.095, 'rope', res=4, ures=3)
        ball(nm('kn'), 0.2, loc=(x, 0, H - 0.05), key='rope_dark', segs=6, rings=4)
        box(nm('br'), (0.22, 0.5, 1.0), loc=(x * 1.28, 0, H + 0.05), key='iron', bev=0.03)
    n = int((H - 1.2) / spacing)
    for i in range(n + 1):
        z = 0.9 + i * spacing
        _rung(-width / 2 - 0.12, 0, z, width + 0.24)
        for s in (-1, 1):
            torus(nm('wr'), 0.14, 0.04, loc=(s * width / 2, 0, z), key='rope_dark', segs=8, rsegs=3, rot=(90, 0, 0))
    box(nm('ft'), (width + 0.6, 0.5, 0.35), loc=(0, 0, 0.22), key='ev_wood_dark', bev=0.05)
    U.marker('mk_lb', (0, -0.3, 0.3))
    U.marker('mk_lt', (0, -0.3, H))
    return finalize(name, smooth_angle=38)


def rope_ladder_short():
    return _rope_ladder(12.0, 1.05, name='rope_ladder_short')


def rope_ladder_tall():
    return _rope_ladder(28.0, 1.1, width=2.4, name='rope_ladder_tall')


def wood_ladder():
    """Vertical wooden tree ladder with wall brackets going back (+Y) to the trunk."""
    reset()
    H, width = 15.0, 2.4
    for s in (-1, 1):
        x = s * width / 2
        box(nm('lr'), (0.3, 0.38, H), loc=(x, 0, H / 2 + 0.2), key='ev_wood_dark', bev=0.045)
        cyl(nm('ft'), 0.22, 0.5, loc=(x, 0, -0.1), key='ev_stone_dark', verts=6)
        ball(nm('cap'), 0.2, loc=(x, 0, H + 0.2), key='ev_wood', segs=6, rings=4)
    n = int((H - 1.0) / 1.15)
    for i in range(n + 1):
        z = 0.9 + i * 1.15
        _rung(-width / 2 - 0.05, 0, z, width + 0.1, r=0.1)
    for z in (3.0, 7.5, 12.0):
        for s in (-1, 1):
            tube(nm('bk'), [(s * width / 2, 0.1, z), (s * width / 2, 0.9, z - 0.15), (s * width / 2, 1.9, z - 0.35)], 0.12, 'iron', res=4)
            box(nm('pl'), (0.5, 0.2, 0.5), loc=(s * width / 2, 1.95, z - 0.35), key='iron_dark', bev=0.03)
    U.marker('mk_lb', (0, -0.4, 0.3))
    U.marker('mk_lt', (0, -0.4, H))
    return finalize('wood_ladder', smooth_angle=38)


def spiral_stair():
    """Trunk-hugging spiral stair: central post, wedge steps, outer railing."""
    reset()
    H, R, r0, n, turns = 15.0, 4.6, 0.55, 26, 1.35
    cyl(nm('post'), 0.62, H + 3.4, loc=(0, 0, 0), key='ev_bark', verts=12)
    cyl(nm('base'), 1.1, 0.5, loc=(0, 0, 0), key='ev_stone', verts=10)
    rise = H / n
    pts_rail = []
    for i in range(n):
        a = 2 * math.pi * turns * i / n
        z = rise * (i + 1)
        mid = (r0 + R) / 2
        dth = 2 * math.pi * turns / n
        box(nm('st'), (R - r0, mid * dth * 1.1, 0.26), loc=(math.cos(a) * mid, math.sin(a) * mid, z - 0.13), key=('ev_wood' if i % 2 else 'ev_wood_light'), rot=(0, 0, math.degrees(a)), bev=0.03)
        box(nm('rs'), (0.16, mid * dth, rise), loc=(math.cos(a) * (R - 0.15 - 0.08), math.sin(a) * (R - 0.15 - 0.08), z - rise / 2 - 0.1), key='ev_wood_dark', rot=(0, 0, math.degrees(a)))
        if i % 2 == 0:
            cyl(nm('rp'), 0.1, 3.1, loc=(math.cos(a) * (R - 0.2), math.sin(a) * (R - 0.2), z - 0.1), key='ev_wood', verts=6)
        pts_rail.append((math.cos(a) * (R - 0.2), math.sin(a) * (R - 0.2), z + 3.0))
    tube(nm('hr'), pts_rail, 0.14, 'ev_wood_light', res=4, ures=2)
    tube(nm('hr2'), [(p[0], p[1], p[2] - 1.5) for p in pts_rail], 0.08, 'ev_wood', res=4, ures=2)
    ang_end = 2 * math.pi * turns * (n - 1) / n
    box(nm('top'), (3.4, 3.4, 0.3), loc=(0, 0, H + 0.1), key='ev_wood', bev=0.04)
    U.marker('mk_lb', (R * 0.7, 0.0, 0.3))
    U.marker('mk_lt', (math.cos(ang_end) * R * 0.7, math.sin(ang_end) * R * 0.7, H + 0.3))
    return finalize('spiral_stair', smooth_angle=38)


def switchback_stair():
    """Two straight flights with a landing between them, railings and posts."""
    reset()
    run, rise, steps, w = 1.0, 0.6, 10, 3.4
    H = rise * steps * 2
    def flight(x0, dirx, y0, z0, tag):
        for i in range(steps):
            x = x0 + dirx * (i + 0.5) * run
            z = z0 + (i + 1) * rise
            box(nm('st'), (run - 0.04, w, 0.3), loc=(x, y0 + w / 2, z - 0.15), key=('ev_wood' if i % 2 else 'ev_wood_light'), bev=0.03)
        L = math.hypot(run * steps, rise * steps)
        ang = math.degrees(math.atan2(rise * steps, run * steps)) * (-dirx)
        xm = x0 + dirx * run * steps / 2
        for y in (y0 + 0.12, y0 + w - 0.12):
            box(nm('sg'), (L, 0.3, 0.7), loc=(xm, y, z0 + rise * steps / 2 - 0.2), key='ev_wood_dark', rot=(0, ang, 0), bev=0.04)
            for k in range(0, steps + 1, 2):
                x = x0 + dirx * k * run
                z = z0 + k * rise
                cyl(nm('pp'), 0.11, 3.0, loc=(x, y, z), key='ev_wood', verts=6)
            tube(nm('hd'), [(x0, y, z0 + 3.0), (x0 + dirx * run * steps, y, z0 + rise * steps + 3.0)], 0.13, 'ev_wood_light', res=4)
            tube(nm('hd2'), [(x0, y, z0 + 1.5), (x0 + dirx * run * steps, y, z0 + rise * steps + 1.5)], 0.08, 'ev_wood', res=4)
    flight(-6.0, 1, 0.0, 0.0, 'a')
    flight(6.0, -1, w + 0.5, rise * steps, 'b')
    # landing at the right end
    box(nm('ld'), (4.6, 2 * w + 0.5, 0.35), loc=(8.3, w + 0.25, rise * steps - 0.18), key='ev_wood', bev=0.04)
    for (x, y) in ((6.4, 0.1), (10.2, 0.1), (6.4, 2 * w + 0.4), (10.2, 2 * w + 0.4)):
        cyl(nm('lp'), 0.28, rise * steps, loc=(x, y, 0.0), key='ev_bark', verts=8)
        cyl(nm('lr'), 0.1, 3.0, loc=(x, y, rise * steps), key='ev_wood', verts=6)
    for y in (0.1, 2 * w + 0.4):
        tube(nm('lh'), [(6.4, y, rise * steps + 3.0), (10.2, y, rise * steps + 3.0)], 0.13, 'ev_wood_light', res=4)
    tube(nm('lh2'), [(10.2, 0.1, rise * steps + 3.0), (10.2, 2 * w + 0.4, rise * steps + 3.0)], 0.13, 'ev_wood_light', res=4)
    # top landing at the left end of flight b
    box(nm('tl'), (3.6, w, 0.35), loc=(-6.0 - 1.8, w + 0.5 + w / 2, H - 0.18), key='ev_wood', bev=0.04)
    for (x, y) in ((-9.4, w + 0.6), (-9.4, 2 * w + 0.4)):
        cyl(nm('tp'), 0.26, H, loc=(x, y, 0.0), key='ev_bark', verts=8)
    # mid supports under flights
    for x in (-1.0, 3.0):
        for y in (0.1, w - 0.1):
            cyl(nm('ms'), 0.22, rise * ((x + 6) / run), loc=(x, y, 0.0), key='ev_bark', verts=6)
    U.marker('mk_lb', (-6.5, w / 2, 0.3))
    U.marker('mk_lt', (-8.2, w * 1.5 + 0.5, H + 0.3))
    return finalize('switchback_stair', smooth_angle=38)


def ladder_landing():
    """Small landing platform on stilts with a railing, a ladder-down opening and a lantern."""
    reset()
    H = 10.0
    for (x, y) in ((-2.3, -1.8), (2.3, -1.8), (-2.3, 1.8), (2.3, 1.8)):
        cyl(nm('stilt'), 0.34, H, loc=(x, y, 0.0), key='ev_bark', verts=8)
        box(nm('foot'), (1.0, 1.0, 0.25), loc=(x, y, 0.12), key='ev_stone_dark', bev=0.05)
    for (x1, y1, x2, y2) in ((-2.3, -1.8, 2.3, 1.8), (2.3, -1.8, -2.3, 1.8)):
        tube(nm('brace'), [(x1, y1, 1.0), (x2, y2, H - 1.5)], 0.14, 'ev_wood_dark', res=4)
    for i in range(7):
        box(nm('pl'), (0.62, 4.9, 0.3), loc=(-2.0 + i * 0.67, 0, H - 0.15), key=('ev_wood' if i % 2 else 'ev_wood_light'), bev=0.03)
    for (x1, y1, x2, y2, gap) in ((-2.6, 2.4, 2.6, 2.4, False), (-2.6, -2.4, -2.6, 2.4, False), (2.6, -2.4, 2.6, 2.4, False)):
        n = max(3, int(math.hypot(x2 - x1, y2 - y1) / 1.3))
        for k in range(n + 1):
            t = k / n
            cyl(nm('rp'), 0.1, 3.0, loc=(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, H), key='ev_wood', verts=6)
        tube(nm('rh'), [(x1, y1, H + 3.0), (x2, y2, H + 3.0)], 0.13, 'ev_wood_light', res=4)
        tube(nm('rm'), [(x1, y1, H + 1.5), (x2, y2, H + 1.5)], 0.08, 'ev_wood', res=4)
    # front (-Y) rail with a ladder opening in the middle
    for (xa, xb) in ((-2.6, -1.3), (1.3, 2.6)):
        tube(nm('fh'), [(xa, -2.4, H + 3.0), (xb, -2.4, H + 3.0)], 0.13, 'ev_wood_light', res=4)
        for k in range(2):
            cyl(nm('fp'), 0.1, 3.0, loc=(xa + (xb - xa) * k, -2.4, H), key='ev_wood', verts=6)
    # ladder down the front
    for s in (-1, 1):
        box(nm('lr'), (0.28, 0.36, H + 3.2), loc=(s * 1.15, -2.7, (H + 3.2) / 2 + 0.1), key='ev_wood_dark', bev=0.04)
    for i in range(int((H + 1.0) / 1.15)):
        _rung(-1.2, -2.7, 0.9 + i * 1.15, 2.4, r=0.1)
    lantern(2.4, 2.2, H + 4.9, s=0.8, hang=False)
    cyl(nm('lps'), 0.1, 1.9, loc=(2.4, 2.2, H + 3.0), key='ev_wood_dark', verts=6)
    box(nm('crate'), (1.0, 1.0, 0.9), loc=(-1.2, 1.2, H + 0.45), key='ev_wood_aged', rot=(0, 0, 18), bev=0.04)
    U.marker('mk_lb', (0, -3.0, 0.3))
    U.marker('mk_lt', (0, -2.6, H + 0.2))
    return finalize('ladder_landing', smooth_angle=38)


def lift_winch():
    """Hand-cranked lift: two posts, crossbeam with pulley, rope, wooden basket."""
    reset()
    H = 12.0
    for x in (-2.6, 2.6):
        cyl(nm('post'), 0.42, H, loc=(x, 0, 0), key='ev_bark', verts=8)
        box(nm('foot'), (1.4, 1.4, 0.3), loc=(x, 0, 0.15), key='ev_stone_dark', bev=0.05)
        tube(nm('brace'), [(x, 0, 2.0), (x * 1.9, 2.4, 0.2)], 0.2, 'ev_wood_dark', res=4)
        tube(nm('brace2'), [(x, 0, 2.0), (x * 1.9, -2.4, 0.2)], 0.2, 'ev_wood_dark', res=4)
    box(nm('xb'), (6.6, 0.7, 0.7), loc=(0, 0, H), key='ev_wood_dark', bev=0.06)
    box(nm('xb2'), (6.0, 0.4, 0.4), loc=(0, 0, H - 1.6), key='ev_wood', bev=0.04)
    torus(nm('pu'), 0.65, 0.14, loc=(0, -0.5, H - 0.5), key='iron', segs=16, rsegs=5, rot=(90, 0, 0))
    cyl(nm('hub'), 0.2, 0.8, loc=(0, -0.9, H - 0.5), key='iron_dark', verts=8, rot=(-90, 0, 0))
    tube(nm('rope'), [(0.0, -0.5, H + 0.1), (0.1, -0.5, H * 0.5), (0.0, -0.5, 3.6)], 0.1, 'rope', res=4, ures=3)
    tube(nm('rope2'), [(0.65, -0.5, H - 0.5), (2.6, -0.1, H * 0.4), (2.6, 0.0, 2.2)], 0.1, 'rope', res=4, ures=3)
    cyl(nm('bk'), 1.45, 1.5, loc=(0.0, -0.5, 2.1), key='ev_wood', verts=12)
    torus(nm('bkr'), 1.45, 0.14, loc=(0.0, -0.5, 3.55), key='ev_wood_dark', segs=18, rsegs=4)
    torus(nm('bkb'), 1.46, 0.1, loc=(0.0, -0.5, 2.1), key='iron', segs=18, rsegs=3)
    torus(nm('bkb2'), 1.46, 0.1, loc=(0.0, -0.5, 3.0), key='iron', segs=18, rsegs=3)
    for k in range(3):
        a = 2 * math.pi * k / 3 + 0.4
        tube(nm('bch'), [(math.cos(a) * 1.4, -0.5 + math.sin(a) * 1.4, 3.6), (0.0, -0.5, 5.4)], 0.05, 'iron', res=4)
    cyl(nm('drum'), 0.55, 2.0, loc=(-2.6, 0.6, 4.2), key='ev_wood_dark', verts=10, rot=(0, 90, 0))
    tube(nm('crank'), [(-3.7, 0.6, 4.2), (-3.9, 0.6, 5.3), (-3.9, 1.5, 5.5)], 0.1, 'iron', res=4)
    cyl(nm('chd'), 0.14, 0.8, loc=(-3.9, 1.5, 5.5), key='ev_wood_light', verts=6, rot=(90, 0, 0))
    U.marker('mk_lb', (0, -0.5, 0.3))
    U.marker('mk_lt', (0, -0.5, 4.0))
    return finalize('lift_winch', smooth_angle=38)


# ------------------------------------------------------------------ lights (warm only)
def lantern_post_a():
    reset()
    box(nm('bs'), (1.5, 1.5, 0.8), loc=(0, 0, 0.4), key='ev_stone', bev=0.08)
    cyl(nm('ps'), 0.26, 8.4, loc=(0, 0, 0.7), key='ev_wood_dark', verts=8)
    for k in range(4):
        a = math.pi / 2 * k + 0.4
        tube(nm('sb'), [(math.cos(a) * 0.3, math.sin(a) * 0.3, 1.2), (math.cos(a) * 0.75, math.sin(a) * 0.75, 0.55)], 0.1, 'ev_wood_dark', res=4)
    tube(nm('arm'), [(0, 0, 8.4), (0.7, 0, 9.0), (1.7, 0, 8.8)], 0.15, 'bronze', res=4)
    tube(nm('brace'), [(0, 0, 7.2), (0.9, 0, 8.4)], 0.1, 'bronze', res=4)
    torus(nm('curl'), 0.3, 0.05, loc=(0.9, 0, 7.9), key='bronze', segs=12, rsegs=3, rot=(90, 0, 0))
    lantern(1.7, 0, 8.8, s=1.1, hang=True)
    return finalize('lantern_post_a', smooth_angle=38)


def lantern_post_b():
    reset()
    lathe(nm('pil'), [(0.0, 0.0), (1.1, 0.0), (1.1, 0.5), (0.8, 0.7), (0.62, 1.2), (0.55, 4.6), (0.7, 5.0), (0.95, 5.2), (0.95, 5.5), (0.0, 5.5)], key='ev_stone', segs=8)
    for k in range(8):
        a = 2 * math.pi * k / 8
        box(nm('bnd'), (0.12, 0.9, 0.5), loc=(math.cos(a) * 0.6, math.sin(a) * 0.6, 2.9), key='ev_stone_dark', rot=(0, 0, math.degrees(a) + 90)) if k % 2 == 0 else None
    lantern(0, 0, 5.5 + 1.12 * 1.3, s=1.3, hang=False)
    return finalize('lantern_post_b', smooth_angle=38)


def lantern_hang_a():
    """Wall bracket with a hanging lantern (back plate on +Y, arm reaches toward -Y)."""
    reset()
    box(nm('bp'), (0.9, 0.22, 3.0), loc=(0, 0.11, 1.9), key='ev_wood_dark', bev=0.05)
    for z in (0.7, 3.1):
        ball(nm('rv'), 0.12, loc=(0, -0.02, z), key='bronze', segs=6, rings=4)
    tube(nm('arm'), [(0, 0.0, 2.4), (0, -1.1, 2.7), (0, -2.4, 2.45)], 0.13, 'bronze', res=4)
    tube(nm('brc'), [(0, 0.0, 1.0), (0, -1.4, 2.5)], 0.09, 'bronze', res=4)
    torus(nm('crl'), 0.34, 0.05, loc=(0, -0.7, 1.7), key='bronze', segs=12, rsegs=3, rot=(0, 90, 0))
    lantern(0, -2.4, 2.45 - 0.9, s=1.0, hang=True)
    return finalize('lantern_hang_a', smooth_angle=38)


def lantern_hang_b():
    """A rope of small lanterns strung between two short posts."""
    reset()
    L = 12.0
    for x in (-L / 2, L / 2):
        cyl(nm('pst'), 0.24, 6.0, loc=(x, 0, 0.3), key='ev_wood_dark', verts=8)
        box(nm('ft'), (1.2, 1.2, 0.3), loc=(x, 0, 0.15), key='ev_stone_dark', bev=0.05)
        ball(nm('cap'), 0.3, loc=(x, 0, 6.4), key='bronze', segs=8, rings=5)
    pts = [(-L / 2, 0, 6.0), (-L / 4, 0, 5.1), (0, 0, 4.8), (L / 4, 0, 5.1), (L / 2, 0, 6.0)]
    tube(nm('rope'), pts, 0.08, 'rope', res=4, ures=4)
    for x, z in ((-L / 4, 5.1), (0, 4.8), (L / 4, 5.1), (-L * 0.38, 5.55), (L * 0.38, 5.55)):
        lantern(x, 0, z - 0.1 - 0.5 * 0.9, s=0.5, hang=True)
    return finalize('lantern_hang_b', smooth_angle=38)


def brazier():
    """Bronze bowl on three legs with logs and a soft ember glow."""
    reset()
    for k in range(3):
        a = 2 * math.pi * k / 3 + 0.5
        tube(nm('lg'), [(math.cos(a) * 1.3, math.sin(a) * 1.3, 3.2), (math.cos(a) * 1.9, math.sin(a) * 1.9, 1.4), (math.cos(a) * 1.7, math.sin(a) * 1.7, 0.0)], 0.14, 'iron', res=4, taper=[1, 0.9, 0.7])
        ball(nm('ft'), 0.2, loc=(math.cos(a) * 1.7, math.sin(a) * 1.7, 0.1), key='iron_dark', segs=6, rings=4)
    lathe(nm('bowl'), [(0.0, 2.6), (0.9, 2.65), (1.9, 3.5), (2.1, 4.0), (2.0, 4.1), (0.0, 3.0)], key='iron_dark', segs=18)
    torus(nm('rim'), 2.05, 0.1, loc=(0, 0, 4.05), key='bronze', segs=24, rsegs=4)
    lathe(nm('embers'), [(0.0, 3.55), (1.6, 3.5), (1.8, 3.75), (0.0, 3.8)], key='rust', segs=14)
    for k in range(5):
        a = 2 * math.pi * k / 5 + 0.2
        cyl(nm('log'), 0.2, 1.9, loc=(math.cos(a) * 0.55, math.sin(a) * 0.55, 3.75), key='ev_wood_dark', verts=8, rot=(35 + 8 * (k % 2), 0, math.degrees(a) + 90))
    # soft flame: three small teardrops in the warm lantern glow colour
    for (x, y, hh, rr) in ((0.0, 0.0, 2.4, 0.5), (0.5, 0.2, 1.5, 0.34), (-0.45, -0.25, 1.7, 0.36)):
        lathe(nm('fl'), [(0.0, 0.0), (rr * 0.8, hh * 0.1), (rr, hh * 0.3), (rr * 0.7, hh * 0.6), (rr * 0.3, hh * 0.85), (0.0, hh)], loc=(x, y, 3.9), key='ev_lantern', segs=7)
    return finalize('brazier', smooth_angle=38)


def candle_cluster():
    reset()
    lathe(nm('base'), [(0.0, 0.0), (1.2, 0.0), (1.3, 0.2), (1.1, 0.45), (0.0, 0.45)], key='ev_stone', segs=14)
    rnd = random.Random(8)
    for i, (x, y, h) in enumerate(((0, 0, 2.3), (0.55, 0.3, 1.5), (-0.5, 0.4, 1.9), (0.1, -0.6, 1.1), (-0.55, -0.35, 0.8), (0.65, -0.35, 0.65))):
        r = rnd.uniform(0.13, 0.2)
        cyl(nm('cd'), r, h, loc=(x, y, 0.45), key='wax', verts=8)
        lathe(nm('drip'), [(0.0, h), (r * 1.12, h - 0.0), (r * 1.15, h - 0.35), (0.0, h - 0.35)], loc=(x, y, 0.45), key='wax', segs=8)
        lathe(nm('fl'), [(0.0, 0.0), (r * 0.55, 0.12), (r * 0.5, 0.32), (0.0, 0.5)], loc=(x, y, 0.45 + h), key='ev_lantern', segs=6)
    return finalize('candle_cluster', smooth_angle=38)


BATCH_LADDERS = [
    ('D02_01_rope_ladder_short', rope_ladder_short, (1.0, -1.1, 0.35)),
    ('D02_02_rope_ladder_tall', rope_ladder_tall, (1.0, -1.1, 0.3)),
    ('D02_03_wood_ladder', wood_ladder, (1.0, -1.1, 0.3)),
    ('D02_04_spiral_stair', spiral_stair),
    ('D02_05_switchback_stair', switchback_stair),
    ('D02_06_ladder_landing', ladder_landing),
    ('D02_07_lift_winch', lift_winch),
    ('D07_01_lantern_post_a', lantern_post_a, (1.0, -1.2, 0.3)),
    ('D07_02_lantern_post_b', lantern_post_b, (1.0, -1.2, 0.3)),
    ('D07_03_lantern_hang_a', lantern_hang_a, (1.0, -1.2, 0.3)),
    ('D07_04_lantern_hang_b', lantern_hang_b),
    ('D07_05_brazier', brazier),
    ('D07_06_candle_cluster', candle_cluster),
]
