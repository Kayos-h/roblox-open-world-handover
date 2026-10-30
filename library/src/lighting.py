# lighting.py - shared-kit lighting models (A15-A23).
import math
import bmesh
from kitlib import *
from kitlib import _obj_from_bm, _link


def lantern_head(px, py, pz, s=1.0, frame='iron', tag='L', hang=False):
    """Four-sided tapered lantern; bottom of the drip cup at pz - 0.95*s. Returns top z."""
    S = lambda v: v * s
    lathe(f'{tag}_cup', [(0.0, S(-0.95)), (S(0.16), S(-0.9)), (S(0.28), S(-0.6)), (S(0.5), S(-0.25)),
                         (S(0.92), S(-0.05)), (S(1.02), S(0.1)), (S(0.0), S(0.1))],
          loc=(px, py, pz), key=frame, segs=4)
    hb, ht, H = S(0.78), S(1.0), S(2.1)
    lathe(f'{tag}_glass', [(0.0, S(0.1)), (hb * 1.414, S(0.1)), (ht * 1.414, S(0.1) + H), (0.0, S(0.1) + H)],
          loc=(px, py, pz), key='glass_lit', segs=4)
    cyl(f'{tag}_glow', S(0.32), S(1.1), loc=(px, py, pz + S(0.45)), key='glow', verts=12, r2=S(0.22))
    cyl(f'{tag}_wick', S(0.36), S(0.35), loc=(px, py, pz + S(0.12)), key='brass', verts=12)
    for i in range(4):
        a = math.radians(45 + 90 * i)
        x0, y0 = math.cos(a) * hb * 1.414, math.sin(a) * hb * 1.414
        x1, y1 = math.cos(a) * ht * 1.414, math.sin(a) * ht * 1.414
        tube(f'{tag}_post{i}', [(px + x0, py + y0, pz + S(0.1)), (px + x1, py + y1, pz + S(0.1) + H)], S(0.07), frame, res=4)
    for j, (hh, r) in enumerate([(S(0.1), hb), (S(0.1) + H, ht), (S(0.1) + H * 0.62, hb + (ht - hb) * 0.62)]):
        R = r * 1.414
        ring = [(px + math.cos(math.radians(45 + 90 * k)) * R, py + math.sin(math.radians(45 + 90 * k)) * R, pz + hh)
                for k in range(4)]
        for k in range(4):
            tube(f'{tag}_band{j}_{k}', [ring[k], ring[(k + 1) % 4]], S(0.055 if j == 2 else 0.075), frame, res=4)
    top = pz + S(0.1) + H
    lathe(f'{tag}_roof', [(0.0, top), (S(1.55), top), (S(1.6), top + S(0.12)), (S(1.35), top + S(0.25)),
                          (S(0.55), top + S(0.95)), (S(0.4), top + S(1.05)), (0.0, top + S(1.05))],
          loc=(px, py, 0), key=frame, segs=4)
    lathe(f'{tag}_cap', [(0.0, top + S(1.0)), (S(0.42), top + S(1.0)), (S(0.46), top + S(1.12)),
                         (S(0.3), top + S(1.45)), (S(0.12), top + S(1.6)), (S(0.16), top + S(1.75)),
                         (S(0.06), top + S(1.85)), (S(0.0), top + S(2.3))],
          loc=(px, py, 0), key=frame, segs=12)
    ball(f'{tag}_fin', S(0.14), loc=(px, py, top + S(1.92)), key=frame, segs=10, rings=6)
    if hang:
        torus(f'{tag}_hring', S(0.22), S(0.06), loc=(px, py, top + S(2.4)), key=frame, segs=12, rsegs=6, rot=(90, 0, 0))
    return top + S(2.3)


def fluted(name, z0, z1, r0, r1, key='iron', n=24, depth=0.86):
    bm = bmesh.new()
    rings = []
    for z, rad in ((z0, r0), (z1, r1)):
        ring = []
        for i in range(n):
            a = 2 * math.pi * i / n
            rr = rad * (1.0 if i % 2 == 0 else depth)
            ring.append(bm.verts.new((math.cos(a) * rr, math.sin(a) * rr, z)))
        rings.append(ring)
    for i in range(n):
        bm.faces.new((rings[0][i], rings[0][(i + 1) % n], rings[1][(i + 1) % n], rings[1][i]))
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[1])
    return _obj_from_bm(name, bm, key)


def iron_post(top=12.2, K='iron'):
    """Shared ornate cast-iron base + pedestal + fluted shaft + collars. Returns capital top z."""
    lathe('base', [(0.0, 0.0), (1.55, 0.0), (1.55, 0.25), (1.42, 0.32), (1.35, 0.55), (1.15, 0.62),
                   (1.05, 0.95), (0.95, 1.05), (0.75, 1.15), (0.0, 1.15)], key=K, segs=8)
    for i in range(4):
        a = math.radians(45 + 90 * i)
        cx, cy = math.cos(a), math.sin(a)
        tube(f'foot{i}', [(cx * 0.9, cy * 0.9, 1.05), (cx * 1.25, cy * 1.25, 0.8), (cx * 1.45, cy * 1.45, 0.45),
                          (cx * 1.3, cy * 1.3, 0.3)], 0.13, K, res=6)
    lathe('pedestal', [(0.0, 1.1), (0.78, 1.1), (0.82, 1.25), (0.68, 1.4), (0.72, 1.6), (0.88, 2.0),
                       (0.9, 2.5), (0.78, 2.9), (0.58, 3.15), (0.5, 3.35), (0.58, 3.5), (0.58, 3.65),
                       (0.42, 3.8), (0.0, 3.8)], key=K, segs=16)
    fluted('shaft', 3.75, top, 0.36, 0.28, K)
    for z, r, h in ((5.2, 0.46, 0.22), (3.75 + (top - 3.75) * 0.58, 0.42, 0.18), (top - 0.1, 0.42, 0.25)):
        lathe(f'collar{z:.1f}', [(0.0, z), (r * 0.85, z), (r, z + h * 0.3), (r, z + h * 0.7), (r * 0.85, z + h), (0.0, z + h)],
              key=K, segs=16)
    lathe('capital', [(0.0, top + 0.1), (0.32, top + 0.1), (0.5, top + 0.35), (0.62, top + 0.6), (0.55, top + 0.75),
                      (0.35, top + 0.85), (0.3, top + 1.0), (0.38, top + 1.1), (0.0, top + 1.1)], key=K, segs=16)
    return top + 1.1


def lamp_iron_city():
    """A15 - ornate cast-iron city lamp post, ~18.6 studs."""
    reset()
    K = 'iron'
    cap = iron_post(12.2, K)
    cyl('spike', 0.16, 0.5, loc=(0, 0, cap), key=K, verts=12)
    lantern_head(0, 0, cap + 0.8, s=1.0, frame=K, tag='LT')
    for i, side in enumerate((1, -1)):
        tube(f'brk{i}', [(side * 0.3, 0, 11.6), (side * 0.85, 0, 11.9), (side * 1.25, 0, 12.6), (side * 1.05, 0, 13.3),
                         (side * 0.6, 0, 13.6), (side * 0.25, 0, 13.55)], 0.1, K, res=6)
        scroll(f'brkcurl{i}', (side * 0.95, 0, 11.75), 0.05, 0.32, 1.1, 'XZ', K, 0.085,
               start_ang=(math.pi if side > 0 else 0), n=30)
        tube(f'brkY{i}', [(0, side * 0.3, 11.6), (0, side * 0.85, 11.9), (0, side * 1.25, 12.6), (0, side * 1.05, 13.3),
                          (0, side * 0.6, 13.6), (0, side * 0.25, 13.55)], 0.1, K, res=6)
    box('ladderbar', (2.6, 0.14, 0.14), loc=(0, 0, 12.85), key=K, bev=0.03)
    for side in (1, -1):
        ball(f'barknob{side}', 0.12, loc=(side * 1.33, 0, 12.85), key=K, segs=10, rings=6)
    return finalize('lamp_iron_city')


def lamp_iron_double():
    """A16 - taller double-arm boulevard lamp: two hanging lanterns on a scrolled crossarm + finial."""
    reset()
    K = 'iron'
    cap = iron_post(15.0, K)
    # crossarm: two graceful arcs from the capital outwards, ending in hooks
    for i, side in enumerate((1, -1)):
        tube(f'arm{i}', [(0, 0, cap - 0.2), (side * 1.4, 0, cap + 0.55), (side * 2.9, 0, cap + 0.75),
                         (side * 3.9, 0, cap + 0.45), (side * 4.1, 0, cap + 0.05)], 0.13, K, res=6)
        tube(f'armlow{i}', [(side * 0.3, 0, cap - 1.4), (side * 1.3, 0, cap - 0.9), (side * 2.4, 0, cap + 0.25),
                            (side * 2.9, 0, cap + 0.7)], 0.09, K, res=6)
        scroll(f'armcurl{i}', (side * 1.2, 0, cap - 0.55), 0.04, 0.42, 1.25, 'XZ', K, 0.08,
               start_ang=(0 if side > 0 else math.pi), n=34)
        scroll(f'tipcurl{i}', (side * 3.25, 0, cap + 0.95), 0.03, 0.26, 1.0, 'XZ', K, 0.07,
               start_ang=(math.pi * 1.5), n=26)
        # hook + short chain + lantern hanging below the arm tip
        hx = side * 4.1
        chain(f'ch{i}', (hx, 0, cap + 0.05), (hx, 0, cap - 1.0), link=0.32, thick=0.05, key=K)
        top_z = cap - 1.05
        lantern_head(hx, 0, top_z - 2.3 * 0.82 - 0.1 * 0.82, s=0.82, frame=K, tag=f'L{i}', hang=False)
    # central finial spire
    lathe('finial', [(0.0, cap), (0.34, cap), (0.4, cap + 0.25), (0.22, cap + 0.6), (0.3, cap + 0.9),
                     (0.12, cap + 1.3), (0.18, cap + 1.6), (0.05, cap + 1.9), (0.0, cap + 2.6)], key=K, segs=12)
    ball('finball', 0.2, loc=(0, 0, cap + 1.95), key='brass', segs=12, rings=8)
    return finalize('lamp_iron_double')


def lamp_wood_rustic():
    """A17 - rustic timber lamp post: stone footing, square post, angled brace, hanging iron lantern."""
    reset()
    # rough stone footing (stacked irregular stones)
    import random
    rnd = random.Random(7)
    box('foot_base', (2.8, 2.8, 0.7), loc=(0, 0, 0.35), key='stone', bev=0.18, segs=2)
    for i in range(6):
        a = math.radians(i * 60 + rnd.uniform(-10, 10))
        box(f'fstone{i}', (rnd.uniform(0.9, 1.3), rnd.uniform(0.7, 1.0), rnd.uniform(0.5, 0.75)),
            loc=(math.cos(a) * 1.15, math.sin(a) * 1.15, 0.85), key=rnd.choice(['stone', 'stone_dark']),
            rot=(rnd.uniform(-6, 6), rnd.uniform(-6, 6), math.degrees(a) + rnd.uniform(-15, 15)), bev=0.16)
    # main post with chamfered edges, slightly tapered via two stacked boxes
    box('post', (0.85, 0.85, 13.2), loc=(0, 0, 0.7 + 6.6), key='wood_dark', bev=0.12)
    # carved rings / iron straps on the post
    for z in (2.4, 7.5, 12.6):
        box(f'strap{z}', (0.95, 0.95, 0.26), loc=(0, 0, z), key='iron', bev=0.04)
        for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            ball(f'rivet{z}{sx}{sy}', 0.07, loc=(sx * 0.48, sy * 0.3, z), key='iron', segs=8, rings=5)
    # post cap
    box('postcap', (1.15, 1.15, 0.35), loc=(0, 0, 14.05), key='wood', bev=0.08)
    lathe('capknob', [(0.0, 14.2), (0.38, 14.2), (0.42, 14.4), (0.25, 14.7), (0.0, 14.9)], key='wood_dark', segs=8)
    # horizontal arm + diagonal brace
    box('arm', (3.9, 0.6, 0.6), loc=(1.75, 0, 13.0), key='wood_dark', bev=0.1)
    box('brace', (0.45, 0.45, 2.7), loc=(1.15, 0, 11.75), key='wood_dark', rot=(0, 45, 0), bev=0.08)
    box('armend', (0.75, 0.75, 0.25), loc=(3.55, 0, 12.6), key='iron', bev=0.05)
    # iron hook + chain + lantern
    tube('hook', [(3.4, 0, 12.55), (3.4, 0, 12.15), (3.62, 0, 11.98), (3.78, 0, 12.15)], 0.06, 'iron', res=4)
    chain('ch', (3.6, 0, 12.0), (3.6, 0, 11.0), link=0.3, thick=0.05, key='iron')
    lantern_head(3.6, 0, 11.0 - 2.3 * 0.75 - 0.1 * 0.75, s=0.75, frame='iron', tag='LW')
    return finalize('lamp_wood_rustic')


def wall_lantern():
    """A18 - wall-mounted lantern on a scrolled bracket. Origin bottom-centre; back plate at y=0."""
    reset()
    K = 'iron'
    # back plate (shield shape)
    poly_prism('plate', [(-0.55, 0), (0.55, 0), (0.7, 0.9), (0.55, 2.2), (0.0, 2.7), (-0.55, 2.2), (-0.7, 0.9)],
               0.14, loc=(0, 0, 0), key=K, rot=(90, 0, 0))
    for z in (0.5, 2.1):
        ball(f'bolt{z}', 0.09, loc=(0, -0.16, z), key='brass', segs=8, rings=5)
    # bracket arm sweeping out to the lantern
    tube('arm', [(0, -0.1, 1.9), (0, -0.7, 2.05), (0, -1.5, 1.95), (0, -2.0, 1.6)], 0.09, K, res=6)
    tube('armlow', [(0, -0.1, 0.8), (0, -0.6, 0.9), (0, -1.15, 1.35), (0, -1.45, 1.9)], 0.07, K, res=6)
    scroll('curl', (0, -0.75, 1.25), 0.03, 0.3, 1.2, 'YZ', K, 0.06, start_ang=0.0, n=30)
    # lantern standing on the arm end (small cup + lantern)
    lantern_head(0, -2.0, 1.6 + 0.95 * 0.6, s=0.6, frame=K, tag='WL')
    return finalize('wall_lantern')


def hanging_lantern():
    """A19 - lantern hanging from a ceiling hook on a chain (for porches, taverns, halls)."""
    reset()
    K = 'iron'
    lathe('ceilplate', [(0.0, 6.0), (0.55, 6.0), (0.5, 5.88), (0.32, 5.8), (0.0, 5.8)], key=K, segs=12)
    torus('hook', 0.18, 0.05, loc=(0, 0, 5.62), key=K, segs=12, rsegs=6, rot=(90, 0, 0))
    chain('ch', (0, 0, 5.45), (0, 0, 3.0), link=0.32, thick=0.05, key=K)
    lantern_head(0, 0, 3.0 - 2.4 * 0.9 - 0.1 * 0.9, s=0.9, frame=K, tag='HL', hang=True)
    return finalize('hanging_lantern')


def wall_torch():
    """A20 - wall torch sconce: iron plate + ring holder + wrapped wooden torch with flame."""
    reset()
    K = 'iron_dark'
    box('plate', (0.9, 0.14, 1.8), loc=(0, -0.07, 0.9), key=K, bev=0.04)
    for z in (0.25, 1.55):
        ball(f'rv{z}', 0.08, loc=(0, -0.16, z), key=K, segs=8, rings=5)
    tube('arm', [(0, -0.12, 0.6), (0, -0.6, 0.62), (0, -0.95, 0.9)], 0.07, K, res=4)
    torus('ring', 0.24, 0.05, loc=(0, -0.95, 1.05), key=K, segs=14, rsegs=6)
    torus('ring2', 0.2, 0.045, loc=(0, -0.95, 0.55), key=K, segs=14, rsegs=6)
    tube('ring_link', [(0, -0.75, 1.05), (0, -0.75, 0.55)], 0.04, K, res=4)
    # torch: tilted outwards slightly
    t = box('_ref', (0.01, 0.01, 0.01), loc=(0, 0, 0))
    bpy.data.objects.remove(t, do_unlink=True)
    cyl('torch', 0.13, 2.0, loc=(0, -0.95, 0.0), key='wood_dark', verts=10, r2=0.17)
    for i, z in enumerate((1.45, 1.62, 1.79)):
        cyl(f'wrap{i}', 0.21 - i * 0.005, 0.16, loc=(0, -0.95, z), key='rope', verts=10)
    cyl('pitch', 0.2, 0.25, loc=(0, -0.95, 1.95), key='iron_dark', verts=10, r2=0.17)
    flame('fl', (0, -0.95, 2.1), h=1.25, r=0.3, tongues=3, seed=2)
    return finalize('wall_torch')


def brazier():
    """A21 - standing iron brazier: three curved legs, hammered bowl, coals and fire."""
    reset()
    K = 'iron'
    # bowl
    lathe('bowl', [(0.0, 3.0), (0.6, 3.0), (1.3, 3.25), (1.75, 3.7), (1.95, 4.2), (2.05, 4.3), (1.9, 4.32),
                   (1.75, 4.1), (1.55, 3.75), (1.1, 3.45), (0.0, 3.4)], key=K, segs=20)
    torus('rim', 2.0, 0.09, loc=(0, 0, 4.3), key=K, segs=28, rsegs=6)
    # decorative band with studs
    for i in range(12):
        a = 2 * math.pi * i / 12
        ball(f'stud{i}', 0.09, loc=(math.cos(a) * 1.78, math.sin(a) * 1.78, 3.85), key='brass', segs=8, rings=5)
    # legs: three S-curves to clawed feet
    for i in range(3):
        a = 2 * math.pi * i / 3
        c, s = math.cos(a), math.sin(a)
        tube(f'leg{i}', [(c * 1.2, s * 1.2, 3.5), (c * 1.6, s * 1.6, 2.6), (c * 1.25, s * 1.25, 1.4),
                         (c * 1.55, s * 1.55, 0.45), (c * 1.95, s * 1.95, 0.15)], 0.13, K, res=6)
        ball(f'foot{i}', 0.2, loc=(c * 1.98, s * 1.98, 0.14), key=K, segs=10, rings=6, scale=(1.3, 1.3, 0.7))
        scroll(f'lcurl{i}', (c * 1.75, s * 1.75, 2.4), 0.03, 0.25, 1.0, 'XZ', K, 0.06, n=24)
    # ring joining legs
    torus('legring', 1.38, 0.07, loc=(0, 0, 1.6), key=K, segs=24, rsegs=6)
    # coals
    import random
    rnd = random.Random(3)
    for i in range(16):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, 1.35)
        ball(f'coal{i}', rnd.uniform(0.18, 0.32), loc=(math.cos(a) * d, math.sin(a) * d, 4.0 + rnd.uniform(0, 0.15)),
             key=rnd.choice(['iron_dark', 'flame', 'iron_dark']), segs=6, rings=4, scale=(1, 1, 0.7))
    flame('fireA', (0, 0, 4.0), h=2.4, r=0.75, tongues=4, seed=5)
    flame('fireB', (0.55, 0.3, 4.0), h=1.5, r=0.42, tongues=2, seed=6)
    flame('fireC', (-0.5, -0.35, 4.0), h=1.7, r=0.45, tongues=2, seed=8)
    return finalize('brazier')


def campfire():
    """A22 - campfire: ring of fieldstones, crossed logs, embers, flames."""
    reset()
    import random
    rnd = random.Random(11)
    n = 11
    for i in range(n):
        a = 2 * math.pi * i / n + rnd.uniform(-0.08, 0.08)
        ball(f'st{i}', rnd.uniform(0.42, 0.58), loc=(math.cos(a) * 2.0, math.sin(a) * 2.0, 0.22),
             key=rnd.choice(['stone', 'stone_dark', 'stone_light']), segs=14, rings=9,
             scale=(rnd.uniform(1.1, 1.4), rnd.uniform(0.9, 1.1), rnd.uniform(0.6, 0.8)))
    box('ash', (2.6, 2.6, 0.08), loc=(0, 0, 0.04), key='iron_dark', rot=(0, 0, 20), bev=0.6, segs=3)
    # teepee logs
    for i in range(5):
        a = 2 * math.pi * i / 5 + 0.3
        c, s = math.cos(a), math.sin(a)
        tube(f'log{i}', [(c * 1.3, s * 1.3, 0.12), (c * 0.15, s * 0.15, 1.35)], 0.17, 'bark', res=6)
        cyl(f'logend{i}', 0.17, 0.02, loc=(c * 1.31, s * 1.31, 0.05), key='wood_light', verts=8,
            rot=(0, 0, 0))
    # two crossed lying logs
    tube('lie1', [(-1.4, -0.4, 0.2), (1.4, 0.4, 0.2)], 0.2, 'bark', res=6)
    tube('lie2', [(-0.5, 1.4, 0.2), (0.5, -1.4, 0.2)], 0.19, 'bark', res=6)
    for i in range(10):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, 0.9)
        ball(f'emb{i}', rnd.uniform(0.1, 0.18), loc=(math.cos(a) * d, math.sin(a) * d, 0.12),
             key=rnd.choice(['flame', 'iron_dark']), segs=6, rings=4, scale=(1, 1, 0.6))
    flame('fireA', (0, 0, 0.15), h=2.6, r=0.7, tongues=4, seed=1)
    flame('fireB', (0.35, -0.25, 0.15), h=1.6, r=0.4, tongues=2, seed=4)
    return finalize('campfire')


def candle_cluster():
    """A23 - cluster of church/tavern candles of different heights with wax drips and a wax pool."""
    reset()
    import random
    rnd = random.Random(21)
    lathe('pool', [(0.0, 0.0), (1.35, 0.0), (1.4, 0.06), (1.2, 0.14), (0.0, 0.16)], key='wax', segs=20)
    spots = [(0, 0, 3.0, 0.3), (0.62, 0.18, 2.1, 0.26), (-0.55, 0.32, 1.6, 0.25), (0.15, -0.62, 1.2, 0.23),
             (-0.35, -0.45, 2.45, 0.24), (0.75, -0.48, 0.8, 0.21)]
    for i, (x, y, h, r) in enumerate(spots):
        top = 0.12 + h
        # slightly uneven candle top
        lathe(f'c{i}', [(0.0, 0.12), (r, 0.12), (r * 1.02, top - 0.12), (r * 0.92, top - 0.02), (r * 0.55, top),
                        (r * 0.4, top - 0.06), (0.0, top - 0.06)], loc=(x, y, 0), key='wax', segs=14)
        # wax drips: thin bumps running down
        for d in range(3):
            a = rnd.uniform(0, 6.28)
            L = rnd.uniform(0.3, min(1.1, h * 0.6))
            tube(f'drip{i}_{d}', [(x + math.cos(a) * r * 0.98, y + math.sin(a) * r * 0.98, top - 0.05),
                                  (x + math.cos(a) * r * 1.03, y + math.sin(a) * r * 1.03, top - L)],
                 0.045, 'wax', res=4, taper=[1.0, 0.6])
        cyl(f'wick{i}', 0.025, 0.14, loc=(x, y, top - 0.06), key='iron_dark', verts=6)
        flame(f'fl{i}', (x, y, top + 0.05), h=0.42, r=0.09, tongues=0, seed=i)
    return finalize('candle_cluster')


ITEMS = [
    ('A15_lamp_iron_city', lamp_iron_city),
    ('A16_lamp_iron_double', lamp_iron_double),
    ('A17_lamp_wood_rustic', lamp_wood_rustic),
    ('A18_wall_lantern', wall_lantern),
    ('A19_hanging_lantern', hanging_lantern),
    ('A20_wall_torch', wall_torch),
    ('A21_brazier', brazier),
    ('A22_campfire', campfire),
    ('A23_candle_cluster', candle_cluster),
]
