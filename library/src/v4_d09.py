"""D09 - water features and small bridges (5 models): two waterfall cliffs, stepping stones, two plank bridges.
Water uses the palette keys 'water' (body) and 'foam' (white water). No glow.
Bridges carry 'connect' markers at deck height. rot args of box/cyl are DEGREES.
"""
import math, random, bmesh
from mathutils import Vector
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism, top_paint, _obj_from_bm
import v4util as U
from v4_elf import nm, ivy_strand, lantern, mushrooms
from v4_d06 import tuft, mini_fern, moss_skirt, daisy
from nature import rock, blob

PI = math.pi
CLIFF = ('stone', 'ev_stone_dark', 'stone_dark', 'ev_stone_dark', 'stone')


# ------------------------------------------------------------------ shared helpers
def sheet(fn, w_fn, nu, ns, key='water', xc=0.0, thick=0.22, dy=0.0, ripple=0.1, u0=0.0, u1=1.0):
    """Water ribbon. fn(s) -> (y, z) centre line; w_fn(s) -> width; u0..u1 selects a lateral strip."""
    bm = bmesh.new()
    grid = []
    for j in range(ns + 1):
        s = j / ns
        y, z = fn(s)
        w = w_fn(s)
        row = []
        for i in range(nu + 1):
            u = u0 + (u1 - u0) * i / nu
            x = xc + (u - 0.5) * w
            rip = ripple * math.sin(u * 7.0 + s * 11.0 + xc) * (0.3 + s)
            row.append(bm.verts.new((x, y + rip + dy, z)))
        grid.append(row)
    for j in range(ns):
        for i in range(nu):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    o = _obj_from_bm(nm('wt'), bm, key)
    sol = o.modifiers.new('sol', 'SOLIDIFY')
    sol.thickness = thick
    return o


def fall_geometry(y_lip, z_top, z_bot, out):
    """Centre line of a falling sheet: leaves the lip, then arcs out and down."""
    H = z_top - z_bot
    return lambda s: (y_lip - 0.25 - out * s ** 2.2, z_top - H * s)


def waterfall(xc, y_lip, z_top, z_bot, width, out, rnd, ns=14, grow=0.12):
    fn = fall_geometry(y_lip, z_top, z_bot, out)
    wf = lambda s: width * (1 + grow * s)
    sheet(fn, wf, 8, ns, 'water', xc=xc, thick=0.3)
    for u in (0.16, 0.34, 0.52, 0.7, 0.86):
        u += rnd.uniform(-0.04, 0.04)
        sheet(fn, wf, 1, ns, 'foam', xc=xc, thick=0.12, dy=-0.14, ripple=0.0, u0=u, u1=u + 0.05)
    # foam and spray where it lands
    ylan = y_lip - 0.25 - out
    for k in range(7):
        a = rnd.uniform(0, 2 * PI)
        d = rnd.uniform(0.0, width * 0.45)
        r = rnd.uniform(0.7, 1.3)
        ball(nm('sp'), r, (xc + math.cos(a) * d, ylan - 0.4 + math.sin(a) * d * 0.5, z_bot + 0.2), 'foam', segs=7, rings=4, scale=(1.2, 1.0, 0.55))
    for R in (width * 0.6, width * 0.95):
        torus(nm('rg'), R, 0.09, loc=(xc, ylan - 0.6, z_bot + 0.1), key='foam', segs=22, rsegs=4)


def layer_poly(pts, z0, h, key, rnd, moss=True, seed=0):
    o = poly_prism(nm('ly'), pts, h, loc=(0, 0, z0), key=key)
    if moss:
        top_paint(o, 'ev_moss', 0.88, seed, noise_amt=0.15)
    return o


def rim_rocks(cx, cy, rx, ry, rnd, skip=None, n=18, r0=(0.9, 1.9), z=0.0):
    for i in range(n):
        a = 2 * PI * i / n + rnd.uniform(-0.1, 0.1)
        x, y = cx + math.cos(a) * rx, cy + math.sin(a) * ry
        if skip and skip(x, y):
            continue
        r = rnd.uniform(*r0)
        o = rock(nm('rr'), r, (x, y, z + r * 0.25), rnd.choice(CLIFF), seed=i + int(cx * 3), scale=(1.2, 1.0, 0.6), subdiv=3, amp=0.3)
        top_paint(o, 'ev_moss', 0.55, i)


# ------------------------------------------------------------------ D09_01 waterfall_cliff_a
def waterfall_cliff_a():
    """Tall single fall between two steep stratified cliffs, dropping into a rock-ringed pool with an outflow stream."""
    reset()
    rnd = random.Random(901)
    NL, LH, c, ych = 9, 3.2, 3.4, 3.5
    j = lambda a=0.5: rnd.uniform(-a, a)

    def fr(xa, xb, y, n):
        out = []
        for i in range(n + 1):
            x = xa + (xb - xa) * i / n + (j(0.5) if 0 < i < n else 0.0)
            out.append((x, y + j(0.9) - (0.8 if i % 2 else 0.0)))
        return out

    for k in range(NL):
        Wl = 17.5 - 0.45 * k + j(0.6)
        Wr = 17.5 - 0.5 * k + j(0.6)
        yf = -3.0 + 0.55 * k
        left = fr(-Wl, -c - 0.9, yf, 4)
        right = fr(c + 0.9, Wr, yf, 4)
        if k < NL - 1:
            pts = [(-Wl, 10.5)] + left + [(-c, ych + 0.2), (c, ych + 0.2)] + right + [(Wr, 10.5)]
            layer_poly(pts, k * LH, LH + 0.05, CLIFF[k % 5], rnd, seed=k)
        else:
            layer_poly([(-Wl, 10.5)] + left + [(-c, ych + 0.2), (-c, 10.5)], k * LH, LH + 0.05, CLIFF[k % 5], rnd, seed=k)
            layer_poly([(c, 10.5), (c, ych + 0.2)] + right + [(Wr, 10.5)], k * LH, LH + 0.05, CLIFF[k % 5], rnd, seed=k + 20)
    # boulders at the foot and on ledges break up the stepped outline
    for sx in (-1, 1):
        for i in range(6):
            x = sx * rnd.uniform(c + 3.0, 16.0)
            y = rnd.uniform(-5.5, -2.0)
            r = rnd.uniform(2.2, 4.0)
            o = rock(nm('bd'), r, (x, y, r * 0.4), rnd.choice(CLIFF), seed=i + sx * 7, scale=(1.2, 1.0, 0.75), subdiv=3, amp=0.34)
            top_paint(o, 'ev_moss', 0.5, i + 5)
        for k in (2, 4, 6):
            x = sx * rnd.uniform(c + 2.5, 11.0)
            r = rnd.uniform(1.6, 2.6)
            yf = -3.0 + 0.55 * k
            o = rock(nm('bd'), r, (x, yf + 0.6, (k) * LH + r * 0.2), rnd.choice(CLIFF), seed=k + sx, scale=(1.3, 1.0, 0.7), subdiv=3, amp=0.34)
            top_paint(o, 'ev_moss', 0.5, k)
    z_s = (NL - 1) * LH + 0.55
    # stream on top, then the main fall
    sheet(lambda s: (10.4 - (10.4 - (ych + 0.2)) * s, z_s), lambda s: 2 * c - 0.5, 8, 6, 'water', thick=0.3, ripple=0.06)
    for u in (0.3, 0.62):
        sheet(lambda s: (10.4 - (10.4 - (ych + 0.2)) * s, z_s), lambda s: 2 * c - 0.5, 1, 6, 'foam', thick=0.1, dy=0.0, ripple=0.0, u0=u, u1=u + 0.04)
    waterfall(0.0, ych + 0.2, z_s, 0.75, 2 * c - 0.5, 3.3, rnd)
    # pool and rim
    pool_c = (0.0, -5.0)
    ball(nm('pool'), 1.0, (pool_c[0], pool_c[1], 0.35), 'water', segs=28, rings=8, scale=(12.5, 11.0, 0.5))
    rim_rocks(pool_c[0], pool_c[1], 12.2, 10.8, rnd, skip=lambda x, y: (y > -1.0 and abs(x) < 9) or y > 0.5, n=22)
    # outflow stream: narrows and ends between stones
    sheet(lambda s: (-14.5 - 9.0 * s, 0.55), lambda s: 6.5 - 3.0 * s, 6, 8, 'water', xc=0.0, thick=0.25, ripple=0.08)
    for (x, y) in ((-3.3, -18.0), (3.0, -20.0), (-2.2, -23.5), (2.2, -24.5)):
        o = rock(nm('rk'), rnd.uniform(1.0, 1.7), (x, y, 0.4), rnd.choice(CLIFF), seed=int(y), scale=(1.2, 1.0, 0.65), subdiv=3, amp=0.3)
        top_paint(o, 'ev_moss', 0.55, int(y))
    # ledge dressing: moss, ferns and hanging ivy
    for k in (1, 2, 3, 4, 5, 6, 7):
        yf = -3.0 + 0.55 * k
        z = (k) * LH
        for sx in (-1, 1):
            x = sx * rnd.uniform(c + 2.0, 12.0 - 0.4 * k)
            blob(nm('lm'), rnd.uniform(1.2, 2.2), (x, yf + 1.6, z + 0.05), 'ev_moss', subdiv=2, amp=0.3, scale=(1.5, 1.0, 0.3), seed=k * 3 + sx)
            if k in (1, 3, 5, 7):
                mini_fern(x + rnd.uniform(-1, 1), yf + 1.4, z + 0.1, 6, 2.4, 110 + k * 2 + sx)
            if k in (2, 4, 6):
                ivy_strand((x, yf - 0.2, z), rnd.uniform(3.0, 6.5), seed=130 + k * 3 + sx)
    for sx in (-1, 1):
        for k in range(3):
            ivy_strand((sx * (c + 0.5 + k * 0.5), ych - 0.1, (NL - 1) * LH), rnd.uniform(4.0, 9.0), seed=170 + k * 2 + sx)
    mini_fern(-9.0, -6.0, 0.0, 7, 3.0, 181)
    mini_fern(9.5, -5.0, 0.0, 6, 2.6, 182)
    tuft(-11.0, -9.0, 0.0, rnd, n=8)
    tuft(11.0, -10.0, 0.0, rnd, n=8)
    return finalize('waterfall_cliff_a', smooth_angle=35)


# ------------------------------------------------------------------ D09_02 waterfall_cliff_b
def strata_block(x0, x1, y0, y1, ztop, rnd, nlay, seed0, mossy=True):
    """A stratified rock terrace with a scalloped front edge."""
    zs = 0.0
    hl = ztop / nlay
    for k in range(nlay):
        inset = 0.35 * k
        pts = [(x0 + inset + rnd.uniform(-0.6, 0.6), y1)]
        nf = 7
        for i in range(nf + 1):
            x = x0 + inset + (x1 - x0 - 2 * inset) * i / nf
            pts.append((x, y0 + inset * 0.6 + rnd.uniform(-0.9, 0.5) - (0.7 if i % 2 else 0.0)))
        pts.append((x1 - inset + rnd.uniform(-0.6, 0.6), y1))
        layer_poly(pts, zs, hl + 0.05, CLIFF[(k + seed0) % 5], rnd, moss=mossy, seed=seed0 + k)
        zs += hl


def waterfall_cliff_b():
    """Wide three-step cascade: each terrace holds a pond and spills over its lip into the next."""
    reset()
    rnd = random.Random(902)
    terr = [(-13.0, 13.0, 5.0, 14.0, 22.0, 4), (-14.0, 14.0, -5.0, 5.0, 14.5, 3), (-15.0, 15.0, -14.0, -4.0, 7.2, 2)]
    for i, (x0, x1, y0, y1, zt, nl) in enumerate(terr):
        strata_block(x0, x1, y0, y1, zt, rnd, nl, i * 2)
    falls = [[(-5.5, 5.0), (6.5, 3.5)], [(1.0, 7.0), (-10.0, 2.6)], [(-3.5, 4.8), (7.5, 3.4)]]
    z_after = [14.5, 7.2, 0.0]
    for i, (x0, x1, y0, y1, zt, nl) in enumerate(terr):
        # pond on the terrace top
        cy = (y0 + y1) / 2 + 1.0
        rx = (x1 - x0) / 2 - 3.2
        ry = (y1 - y0) / 2 - 2.2
        ball(nm('pond'), 1.0, ((x0 + x1) / 2, cy, zt + 0.02), 'water', segs=26, rings=7, scale=(rx, ry, 0.5))
        rim_rocks((x0 + x1) / 2, cy, rx + 0.5, ry + 0.4, rnd, skip=lambda x, y, yy=y0: y < yy + 3.4, n=16, r0=(0.7, 1.4), z=zt)
        for (fx, fw) in falls[i]:
            zb = z_after[i] + 0.55
            ylip = y0 - 1.6
            slab_ = box(nm('spill'), (fw + 1.8, 3.8, 0.9), loc=(fx, y0 - 0.1, zt - 0.45), key=CLIFF[(i + 2) % 5], bev=0.1, segs=1)
            top_paint(slab_, 'ev_moss', 0.97, i, noise_amt=0.0)
            sheet(lambda s, a=y0 + 2.4, b=ylip, z=zt + 0.38: (a + (b - a) * s, z), lambda s, w=fw * 0.92: w, 6, 4, 'water', xc=fx, thick=0.26, ripple=0.04)
            waterfall(fx, ylip, zt + 0.38, zb, fw * 0.92, 2.0 if i < 2 else 2.6, rnd, ns=10)
    # bottom pool
    ball(nm('pool'), 1.0, (0, -20.0, 0.35), 'water', segs=28, rings=8, scale=(16.0, 7.5, 0.5))
    rim_rocks(0, -20.0, 16.2, 7.8, rnd, skip=lambda x, y: y > -13.6, n=22, r0=(1.0, 2.0))
    # dressing
    for i, (x0, x1, y0, y1, zt, nl) in enumerate(terr):
        for sx in (-1, 1):
            xx = sx * (x1 - 1.6)
            mini_fern(xx, (y0 + y1) / 2 + 1.0, zt + 0.1, 6, 2.4, 200 + i * 3 + sx)
            blob(nm('lm'), 1.8, (xx + sx * 0.4, y0 + 1.0, zt + 0.05), 'ev_moss', subdiv=2, amp=0.3, scale=(1.5, 1.0, 0.3), seed=i + sx)
        for k in range(3):
            ivy_strand((-9.0 + k * 8.5 + rnd.uniform(-1, 1), y0 - 0.5, zt - 0.3), rnd.uniform(3.0, 6.0), seed=230 + i * 3 + k)
    for sx in (-1, 1):
        for i in range(4):
            x = sx * rnd.uniform(11.0, 18.0)
            y = rnd.uniform(-14.0, -3.0)
            r = rnd.uniform(2.0, 3.6)
            o = rock(nm('bd'), r, (x, y, r * 0.35), rnd.choice(CLIFF), seed=i + sx * 5, scale=(1.2, 1.0, 0.7), subdiv=3, amp=0.34)
            top_paint(o, 'ev_moss', 0.5, i)
    tuft(-17.0, -22.0, 0.0, rnd, n=8)
    tuft(17.5, -23.0, 0.0, rnd, n=8)
    mini_fern(-16.0, -17.0, 0.0, 6, 2.8, 251)
    mini_fern(16.5, -18.0, 0.0, 6, 2.8, 252)
    return finalize('waterfall_cliff_b', smooth_angle=35)


# ------------------------------------------------------------------ D09_03 stepping_stones
def mound_bank(sgn, rnd):
    """Low overlapping earth-and-moss mounds that frame the stream and blend into the terrain."""
    for i in range(6):
        y = -11.5 + i * 4.6 + rnd.uniform(-0.6, 0.6)
        r = rnd.uniform(4.0, 5.2)
        blob(nm('mb'), r, (sgn * (5.7 + r * 0.8), y, 0.35), 'ev_moss', subdiv=3, amp=0.28, scale=(1.0, 1.0, 0.3), seed=i + sgn * 4, flat_bottom=-0.2)
    for i in range(7):
        y = rnd.uniform(-13, 13)
        r = rnd.uniform(0.5, 1.0)
        o = rock(nm('pb'), r, (sgn * rnd.uniform(5.3, 6.2), y, 0.9), rnd.choice(CLIFF), seed=i, scale=(1.2, 1.0, 0.6), subdiv=3, amp=0.3)


def stepping_stones():
    """Seven flat stones across a shallow stream, with foam rings, low mossy banks, ferns and flowers."""
    reset()
    rnd = random.Random(903)
    zw = 0.9
    box(nm('bed'), (11.6, 28.0, 0.5), loc=(0, 0, 0.25), key='ev_stone_dark', bev=0.05, segs=1)
    sheet(lambda s: (-14.0 + 28.0 * s, zw), lambda s: 11.4, 10, 14, 'water', thick=0.3, ripple=0.07)
    for sx in (-1, 1):
        mound_bank(sx, rnd)
    xs = [-6.4 + 2.15 * i for i in range(7)]
    for i, x in enumerate(xs):
        y = 1.6 * math.sin(i * 1.3 + 0.4)
        r = rnd.uniform(1.15, 1.5) if 0 < i < 6 else 1.7
        o = rock(nm('st'), r, (x, y, zw + 0.1), rnd.choice(('stone', 'ev_stone', 'ev_stone_warm')), seed=i + 3, scale=(1.05, 0.95, 0.85), subdiv=3, amp=0.18, rot_z=rnd.uniform(0, 3))
        top_paint(o, 'ev_moss', 0.93, i, noise_amt=0.2)
        torus(nm('fr'), r * 1.2, 0.06, loc=(x, y, zw + 0.1), key='foam', segs=18, rsegs=4)
    for (x, y) in ((-3.2, 6.8), (3.4, -7.4), (-1.8, -8.6), (2.6, 8.2)):
        o = rock(nm('rk'), rnd.uniform(0.8, 1.3), (x, y, zw + 0.1), rnd.choice(CLIFF), seed=int(x * 7), scale=(1.2, 1.0, 0.6), subdiv=3, amp=0.3)
        top_paint(o, 'ev_moss', 0.55, int(y))
        torus(nm('fr'), 1.5, 0.05, loc=(x, y, zw + 0.1), key='foam', segs=14, rsegs=4)
    for sx in (-1, 1):
        for y in (-9.0, -3.0, 4.0, 10.0):
            tuft(sx * (8.2 + rnd.uniform(0, 3.0)), y + rnd.uniform(-1, 1), 1.4, rnd, n=7)
        mini_fern(sx * 8.4, 7.0, 1.4, 7, 2.8, 300 + sx)
        mini_fern(sx * 9.5, -6.5, 1.4, 6, 2.6, 302 + sx)
        for y in (-1.5, 2.0):
            daisy(sx * 8.0, y + 3.0, 1.4, rnd.uniform(1.8, 2.8), rnd)
        o = rock(nm('rk'), 1.6, (sx * 8.0, -11.0, 1.6), rnd.choice(CLIFF), seed=sx + 9, scale=(1.2, 1.0, 0.7), subdiv=3, amp=0.3)
        top_paint(o, 'ev_moss', 0.55, 9)
    mushrooms(8.4, 1.0, 1.4, 5, seed=3, scale=1.3)
    return finalize('stepping_stones', smooth_angle=35)


# ------------------------------------------------------------------ D09_04/05 plank bridges
def abutment(sg, zd, rnd):
    xc = sg * 8.0
    b = box(nm('ab'), (4.2, 6.6, zd - 0.3), loc=(xc, 0, (zd - 0.3) / 2), key='ev_stone_dark', bev=0.08)
    top_paint(b, 'ev_moss', 0.97, sg + 4, noise_amt=0.0)
    for j in range(3):
        top = zd * (1 - (j + 1) / 4) - 0.1
        box(nm('stp'), (1.1, 4.4, top), loc=(sg * (10.6 + 1.05 * j), 0, top / 2), key='ev_stone', bev=0.05, segs=1)
    for s in (-1, 1):
        box(nm('wing'), (3.0, 1.0, zd - 0.9), loc=(xc + sg * 0.4, s * 3.5, (zd - 0.9) / 2), key='ev_stone_dark', bev=0.06)


def bridge_deck(L, W, zfn, slope, rnd, keys=('ev_wood', 'ev_wood_light', 'ev_wood')):
    n = int((L + 6.0) / 0.95)
    pw = (L + 6.0) / n
    for i in range(n):
        x = -(L + 6.0) / 2 + pw * (i + 0.5)
        key = keys[i % 3] if rnd.random() > 0.15 else 'ev_wood_aged'
        box(nm('pl'), (pw * 0.93, W, 0.22), loc=(x, 0, zfn(x) - 0.11), rot=(0, slope(x), 0), key=key, bev=0.02, segs=1)


def plank_bridge_a():
    """Straight plank footbridge on two stone abutments with railings, lantern posts and ivy."""
    reset()
    rnd = random.Random(904)
    L, W, zd = 12.0, 4.0, 2.8
    zfn = lambda x: zd
    bridge_deck(L, W, zfn, lambda x: 0.0, rnd)
    for y in (-1.5, 0.0, 1.5):
        box(nm('str'), (L + 1.4, 0.55, 0.7), loc=(0, y, zd - 0.22 - 0.35), key='ev_wood_dark', bev=0.04, segs=1)
    for x in (-5.0, -2.5, 0.0, 2.5, 5.0):
        box(nm('slp'), (0.6, W + 0.6, 0.45), loc=(x, 0, zd - 0.22 - 0.95), key='ev_wood_dark', bev=0.04, segs=1)
    for sg in (-1, 1):
        abutment(sg, zd, rnd)
    for s in (-1, 1):
        ye = s * (W / 2 + 0.05)
        xs = [-9.0 + 3.0 * i for i in range(7)]
        for x in xs:
            cyl(nm('post'), 0.2, 3.3, loc=(x, ye, zd), key='ev_wood_dark', verts=6)
            ball(nm('kn'), 0.28, (x, ye, zd + 3.4), 'ev_wood_light', segs=6, rings=4)
        box(nm('rail'), (18.4, 0.3, 0.3), loc=(0, ye, zd + 3.1), key='ev_wood', bev=0.04, segs=1)
        box(nm('rail'), (18.4, 0.22, 0.22), loc=(0, ye, zd + 1.7), key='ev_wood', bev=0.03, segs=1)
        box(nm('toe'), (18.4, 0.2, 0.3), loc=(0, ye, zd + 0.15), key='ev_wood_dark', bev=0.03, segs=1)
    for (x, y) in ((-6.0, -2.05), (6.0, 2.05)):
        cyl(nm('lp'), 0.16, 1.2, loc=(x, y, zd + 3.4), key='ev_wood_dark', verts=6)
        lantern(x, y, zd + 4.6 + 1.12 * 0.8, 0.8, hang=False)
    for k in range(5):
        ivy_strand((rnd.uniform(-7, 7), rnd.choice((-1, 1)) * (W / 2 + 0.15), zd + 3.0), rnd.uniform(2.0, 3.6), seed=400 + k)
    for sg in (-1, 1):
        mini_fern(sg * 12.0, 3.0, 0.0, 6, 2.4, 410 + sg)
        tuft(sg * 12.5, -3.2, 0.0, rnd, n=7)
        blob(nm('mo'), 4.0, (sg * 12.0, 0, 0.0), 'ev_moss', subdiv=2, amp=0.3, scale=(1.2, 1.3, 0.1), seed=sg + 7)
        U.marker('mk_conn', (sg * 9.0, 0, zd))
    return finalize('plank_bridge_a', smooth_angle=35)


def plank_bridge_b():
    """Humpback wooden bridge with a curved under-arch, curved rails and a lantern at each end."""
    reset()
    rnd = random.Random(905)
    L, W, zd, rise = 12.0, 4.0, 2.8, 2.3

    def zfn(x):
        if abs(x) >= L / 2:
            return zd
        return zd + rise * (1 - (2 * x / L) ** 2)

    def slope(x):
        if abs(x) >= L / 2:
            return 0.0
        return -math.degrees(math.atan(-rise * 8 * x / (L * L)))

    bridge_deck(L, W, zfn, slope, rnd)
    xs = [-L / 2 + L * i / 12 for i in range(13)]
    for y in (-1.5, 1.5):
        tube(nm('arch'), [(-L / 2 - 1.0, y, zd - 0.6)] + [(x, y, zfn(x) - 0.75) for x in xs] + [(L / 2 + 1.0, y, zd - 0.6)], 0.3, 'ev_wood_dark', res=5, ures=3)
    for y in (-0.75, 0.75):
        tube(nm('str'), [(x, y, zfn(x) - 0.4) for x in xs], 0.18, 'ev_wood_dark', res=4, ures=2)
    for x in (-4.0, -2.0, 0.0, 2.0, 4.0):
        box(nm('slp'), (0.5, W + 0.5, 0.35), loc=(x, 0, zfn(x) - 0.45), key='ev_wood_dark', bev=0.04, segs=1)
    for sg in (-1, 1):
        abutment(sg, zd, rnd)
    for s in (-1, 1):
        ye = s * (W / 2 + 0.05)
        px = [-L / 2 - 1.5, -4.0, -2.0, 0.0, 2.0, 4.0, L / 2 + 1.5]
        for x in px:
            z0 = zfn(x)
            cyl(nm('post'), 0.2, 3.2, loc=(x, ye, z0), key='ev_wood_dark', verts=6)
            ball(nm('kn'), 0.27, (x, ye, z0 + 3.3), 'ev_wood_light', segs=6, rings=4)
        top = [(x, ye, zfn(x) + 3.05) for x in [-L / 2 - 1.5] + xs + [L / 2 + 1.5]]
        mid = [(x, ye, zfn(x) + 1.65) for x in [-L / 2 - 1.5] + xs + [L / 2 + 1.5]]
        tube(nm('rail'), top, 0.16, 'ev_wood', res=5, ures=3)
        tube(nm('rail'), mid, 0.11, 'ev_wood', res=4, ures=3)
    for (x, y) in ((-L / 2 - 1.5, -2.05), (L / 2 + 1.5, 2.05)):
        cyl(nm('lp'), 0.16, 1.2, loc=(x, y, zd + 3.3), key='ev_wood_dark', verts=6)
        lantern(x, y, zd + 4.5 + 1.12 * 0.8, 0.8, hang=False)
    for k in range(5):
        x = rnd.uniform(-5, 5)
        ivy_strand((x, rnd.choice((-1, 1)) * (W / 2 + 0.15), zfn(x) + 2.9), rnd.uniform(2.0, 3.6), seed=420 + k)
    for sg in (-1, 1):
        mini_fern(sg * 12.0, 3.0, 0.0, 6, 2.4, 430 + sg)
        tuft(sg * 12.5, -3.2, 0.0, rnd, n=7)
        blob(nm('mo'), 4.0, (sg * 12.0, 0, 0.0), 'ev_moss', subdiv=2, amp=0.3, scale=(1.2, 1.3, 0.1), seed=sg + 9)
        U.marker('mk_conn', (sg * 9.0, 0, zd))
    return finalize('plank_bridge_b', smooth_angle=35)


BATCH_D09 = [
    ('D09_01_waterfall_cliff_a', waterfall_cliff_a, (0.5, -1.3, 0.35)),
    ('D09_02_waterfall_cliff_b', waterfall_cliff_b, (0.6, -1.2, 0.45)),
    ('D09_03_stepping_stones', stepping_stones, (0.8, -1.1, 0.7)),
    ('D09_04_plank_bridge_a', plank_bridge_a, (0.7, -1.2, 0.35)),
    ('D09_05_plank_bridge_b', plank_bridge_b, (0.7, -1.2, 0.35)),
]
