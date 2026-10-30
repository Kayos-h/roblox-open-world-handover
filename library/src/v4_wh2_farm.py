"""wh2 E08 barns and E09 windmills. 1 unit = 1 stud, front -Y, origin bottom-centre.
My own module (predecessor had no v4_wh_farm.py). Reuses kitlib/arch/props/nature helpers.
Palette keys I add all start with 'wh2_'."""
import math, random
import bpy
from mathutils import Vector
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, top_paint, PAL
from arch import F, nm, lbox, lbeam, gable_roof, timber_frame, railing, slab, lslab, beam3
from props import wheel, cloth, plank_box
from nature import blob, rock
import v4util

# ---- palette additions (barn red, weathered boards, sail cloth) -----------
PAL['wh2_barnred']   = ((122, 44, 38),  'WoodPlanks', 0.0, 0.72, 0)
PAL['wh2_barnred_d'] = ((96, 34, 30),   'WoodPlanks', 0.0, 0.76, 0)
PAL['wh2_board']     = ((140, 112, 80), 'Wood',       0.0, 0.80, 0)
PAL['wh2_board_d']   = ((108, 84, 58),  'Wood',       0.0, 0.82, 0)
PAL['wh2_capwood']   = ((120, 92, 62),  'WoodPlanks', 0.0, 0.78, 0)
PAL['wh2_sail']      = ((214, 206, 188),'Fabric',     0.0, 0.85, 0)


# ---- shared helpers -------------------------------------------------------
def board_wall(f, w, z0, z1, key, keyd, seed, t=0.3, vgap=1.1):
    """A plank-boarded wall face in frame-local coords: vertical boards with seams and tone variation."""
    rnd = random.Random(seed)
    n = max(3, int(round(w / vgap)))
    bw = w / n
    for i in range(n):
        x = -w / 2 + bw * (i + 0.5)
        box(nm('bd'), (bw - 0.06, t, z1 - z0), loc=f.p(x, -t / 2, (z0 + z1) / 2),
            key=rnd.choice([key, key, keyd]), rot=f.r(), bev=0.02)


def batten_trim(f, w, z0, z1, key, n=6):
    for i in range(n + 1):
        x = -w / 2 + w * i / n
        lbox(f, (0.14, 0.12, z1 - z0), x, -0.32, (z0 + z1) / 2, key)


def hay_bale(x, y, z, rnd, w=2.2, d=1.4, h=1.3, key='thatch'):
    o = box(nm('bale'), (w, d, h), loc=(x, y, z + h / 2), key=key, bev=0.12, rot=(0, 0, rnd.uniform(-6, 6)))
    for k in range(2):
        box(nm('tie'), (w + 0.04, 0.08, h * 0.9), loc=(x, y - d / 2 + d * (0.3 + 0.4 * k), z + h / 2), key='rope')
    return o


# ============================================================ E08 barns
def barn_gambrel():
    """E08_01 - classic gambrel-roof red barn, big double doors, hay-loft door. ~30x22x24."""
    reset()
    rnd = random.Random(201)
    W, D, wallh = 30.0, 22.0, 15.0
    fl = {'front': F(0, -D / 2, 0, 0), 'back': F(0, D / 2, 0, 180),
          'left': F(-W / 2, 0, 0, -90), 'right': F(W / 2, 0, 0, 90)}
    # stone foundation band
    box(nm('found'), (W + 0.6, D + 0.6, 1.6), loc=(0, 0, 0.8), key='stone', bev=0.05)
    box(nm('slab'), (W - 1.0, D - 1.0, 0.4), loc=(0, 0, 1.0), key='dirt')
    # four boarded walls (hollow: walls are 0.3 thick boxes around the shell)
    board_wall(fl['front'], W, 1.4, wallh, 'wh2_barnred', 'wh2_barnred_d', 201)
    board_wall(fl['back'],  W, 1.4, wallh, 'wh2_barnred', 'wh2_barnred_d', 202)
    board_wall(fl['left'],  D, 1.4, wallh, 'wh2_barnred', 'wh2_barnred_d', 203)
    board_wall(fl['right'], D, 1.4, wallh, 'wh2_barnred', 'wh2_barnred_d', 204)
    # interior back wall + floor so doorway is not see-through
    box(nm('ceil'), (W - 1.2, D - 1.2, 0.4), loc=(0, 0, wallh - 0.3), key='wh2_board_d')
    # white corner + eave trim
    for fx in (fl['left'], fl['right']):
        batten_trim(fx, D, 1.4, wallh, 'whitewash', n=5)
    # big double doors on the front (white framed, X-braced)
    dw, dh = 10.0, 11.0
    for s in (-1, 1):
        cx = s * dw / 4
        lbox(fl['front'], (dw / 2 - 0.2, 0.25, dh), cx, -0.2, 1.4 + dh / 2, 'wh2_board')
        # X brace + edge frame
        lbeam(fl['front'], (cx - dw / 4 + 0.3, -0.42, 1.8), (cx + dw / 4 - 0.3, -0.42, 1.4 + dh - 0.4), 0.22, 'whitewash')
        lbeam(fl['front'], (cx + dw / 4 - 0.3, -0.42, 1.8), (cx - dw / 4 + 0.3, -0.42, 1.4 + dh - 0.4), 0.22, 'whitewash')
        for ex in (-1, 1):
            lbox(fl['front'], (0.22, 0.3, dh), cx + ex * (dw / 4 - 0.1), -0.4, 1.4 + dh / 2, 'whitewash')
    lbox(fl['front'], (dw + 1.2, 0.35, 0.5), 0, -0.4, 1.4 + dh + 0.3, 'whitewash')
    v4util.marker('mk_door', (0, -D / 2 - 0.3, 1.4))
    # hay-loft door high in the front gable with a hoist beam
    lbox(fl['front'], (4.0, 0.25, 4.0), 0, -0.2, wallh + 3.0, 'wh2_board')
    for ex in (-1, 1):
        lbox(fl['front'], (0.2, 0.3, 4.2), ex * 2.0, -0.4, wallh + 3.0, 'whitewash')
    lbeam(fl['front'], (0, -0.3, wallh + 5.4), (0, -2.6, wallh + 5.2), 0.3, 'wh2_capwood')
    tube(nm('pul'), [fl['front'].p(0, -2.4, wallh + 5.0), fl['front'].p(0, -2.4, wallh + 3.8)], 0.06, 'iron', res=4)
    # small windows down the sides
    for fx, span in ((fl['left'], D), (fl['right'], D)):
        for k in (-1, 1):
            lbox(fx, (2.0, 0.26, 2.4), k * span * 0.25, -0.1, 7.0, 'glass_dark')
            lbox(fx, (2.3, 0.32, 0.25), k * span * 0.25, -0.2, 8.3, 'whitewash')
            lbox(fx, (0.22, 0.3, 2.6), k * span * 0.25, -0.2, 7.0, 'whitewash')
    # gambrel roof: two-slope each side, built from four long tilted plank panels
    _gambrel_roof(W, D, wallh, rnd, keys=('wh2_barnred_d', 'wh2_barnred'))
    return finalize('barn_01', smooth_angle=30)


def _gambrel_roof(W, D, z0, rnd, keys):
    """Gambrel (two-pitch) roof as a closed shell. Ridge along x (length W), spans across y (width D).
    Four long sloped panels (lower steep + upper shallow, each side) built as flat slabs, plus gable-end
    pentagons and a shingle course overlay."""
    ov = 1.2
    LL = W / 2 + ov
    half = D / 2
    bx = half * 0.62          # y of the slope break
    zbreak = z0 + 6.5
    zridge = z0 + 11.0
    # eave point extended by overhang in y and down a touch
    eave_y = half + ov
    eave_z = z0 - 0.4
    # one slab per sloped panel (both gable ends share x = +-LL)
    def panel(ya, za, yb, zb, key, thick=0.3):
        # quad across the full roof length, from (ya,za) to (yb,zb) in the y-z section
        for sgn in (1,):
            pass
        n = Vector((0, (zb - za), -(yb - ya)))  # outward-ish normal (unused precise)
        pts = [(-LL, ya, za), (LL, ya, za), (LL, yb, zb), (-LL, yb, zb)]
        # give it thickness by extruding slightly downward along -z
        slab(pts, (0, 0, -thick), key)
    for s in (-1, 1):
        panel(s * eave_y, eave_z, s * bx, zbreak, keys[0])     # lower steep
        panel(s * bx, zbreak, 0.0, zridge, keys[1])            # upper shallow
    # shingle course lines on each panel (thin raised strips) for far-read detail
    for s in (-1, 1):
        for (ya, za, yb, zb) in [(s * eave_y, eave_z, s * bx, zbreak), (s * bx, zbreak, 0.0, zridge)]:
            seg = Vector((0, yb - ya, zb - za)); L = seg.length; seg = seg.normalized()
            nrm = Vector((0, seg.z, -seg.y)) if s > 0 else Vector((0, -seg.z, seg.y))
            ncourse = max(2, int(L / 1.3))
            for i in range(1, ncourse):
                t = i / ncourse
                cy = ya + (yb - ya) * t; cz = za + (zb - za) * t
                box(nm('crs'), (W + 2 * ov - 0.2, 0.3, 0.12),
                    loc=(0, cy + nrm.y * 0.16, cz + nrm.z * 0.16), key=keys[(i) % 2],
                    rot=(math.degrees(math.atan2(seg.z, seg.y)), 0, 0), bev=0.02)
    # gable-end pentagons (close the ends)
    for g in (-1, 1):
        pts = [(g * W / 2, -eave_y, eave_z), (g * W / 2, -bx, zbreak), (g * W / 2, 0, zridge),
               (g * W / 2, bx, zbreak), (g * W / 2, eave_y, eave_z)]
        slab(pts, (-g * 0.5, 0, 0), 'wh2_barnred')
    # barge boards along the gable rakes
    for g in (-1, 1):
        for (ya, za, yb, zb) in [(-eave_y, eave_z, -bx, zbreak), (-bx, zbreak, 0, zridge),
                                 (bx, zbreak, eave_y, eave_z), (0, zridge, bx, zbreak)]:
            beam3((g * (W / 2 + 0.1), ya, za), (g * (W / 2 + 0.1), yb, zb), 0.3, 0.5, 'whitewash')
    # ridge cap
    box(nm('ridge'), (W + 2 * ov + 0.2, 0.8, 0.5), loc=(0, 0, zridge + 0.15), key='wh2_capwood', bev=0.05)


def barn_stone_timber():
    """E08_02 - stone-and-timber barn with a lean-to shed. Stone lower, timber-framed plaster upper."""
    reset()
    rnd = random.Random(210)
    W, D, lowh, uph = 24.0, 18.0, 6.5, 8.0
    wallh = lowh + uph
    fl = {'front': F(0, -D / 2, 0, 0), 'back': F(0, D / 2, 0, 180),
          'left': F(-W / 2, 0, 0, -90), 'right': F(W / 2, 0, 0, 90)}
    box(nm('slab'), (W, D, 0.5), loc=(0, 0, 0.25), key='stone')
    # stone lower storey (all four faces), rough coursing via nature import unused -> boxes
    from capital import stone_face
    for fx, span in ((fl['front'], W), (fl['back'], W), (fl['left'], D), (fl['right'], D)):
        box(nm('low'), (span, 0.5, lowh), loc=fx.p(0, -0.25, lowh / 2), key='stone', rot=fx.r())
        stone_face(fx, -span / 2 + 0.3, span / 2 - 0.3, 0.4, lowh - 0.2, int(span / 1.4), rnd.randint(1, 999),
                   keys=('stone', 'stone_dark', 'stone_light'))
    # timber-framed plaster upper storey
    for fx, span in ((fl['front'], W), (fl['back'], W), (fl['left'], D), (fl['right'], D)):
        box(nm('up'), (span, 0.4, uph), loc=fx.p(0, -0.2, lowh + uph / 2), key='plaster', rot=fx.r())
        posts = [-span / 2 + 0.4 + (span - 0.8) * i / 4 for i in range(5)]
        timber_frame(fx.sub(0, -0.2, 0), span, lowh, lowh + uph, posts, key='timber', t=0.4)
    box(nm('ceil'), (W - 1.0, D - 1.0, 0.4), loc=(0, 0, wallh - 0.3), key='timber')
    # arched cart entrance (stone) on the front
    dw, dh = 8.0, 6.0
    lbox(fl['front'], (dw, 0.6, dh), 0, 0.0, dh / 2 + 0.4, 'hole')  # opening (dark)
    for ex in (-1, 1):
        lbox(fl['front'], (0.8, 0.7, dh + 0.4), ex * (dw / 2 + 0.2), -0.25, (dh + 0.4) / 2, 'stone_dark', bev=0.05)
    # timber lintel
    lbox(fl['front'], (dw + 2.0, 0.7, 0.9), 0, -0.3, dh + 0.9, 'timber')
    # interior back behind door so not see-through
    box(nm('ib'), (dw + 1, 0.5, dh + 1), loc=(0, -D / 2 + 3.5, dh / 2 + 0.4), key='wh2_board_d')
    v4util.marker('mk_door', (0, -D / 2 - 0.4, 0.5))
    # windows upper
    for fx, span in ((fl['left'], D), (fl['right'], D)):
        for k in (-1, 1):
            lbox(fx, (1.8, 0.3, 2.2), k * span * 0.26, -0.1, lowh + uph * 0.5, 'glass_dark')
            lbox(fx, (0.18, 0.34, 2.4), k * span * 0.26, -0.22, lowh + uph * 0.5, 'timber')
    # gable roof (thatch-free wooden shingle) using arch.gable_roof
    gable_roof(fl['front'].sub(0, D / 2, 0, 0), W, D, wallh, 8.0,
               keys=('wh2_board_d', 'wh2_board'), ov=1.0, ovg=0.8, wall='plaster', barge='timber', row=1.1)
    # lean-to shed on the right side
    lx = W / 2
    shw, shd, shh = 7.0, D * 0.7, 4.5
    box(nm('shfl'), (shw, shd, 0.3), loc=(lx + shw / 2, 0, 0.15), key='dirt')
    for (yy) in (-shd / 2, shd / 2):
        box(nm('shp'), (0.3, 0.3, shh), loc=(lx + shw - 0.3, yy, shh / 2), key='timber')
    # mono-pitch roof sloping down away from the barn
    o = box(nm('shr'), (shw + 1.0, shd + 0.8, 0.3), loc=(lx + shw / 2, 0, lowh - 0.5), key='wh2_board')
    o.rotation_euler = (0, math.radians(18), 0)
    # a couple of hay bales under the lean-to
    for k in range(3):
        hay_bale(lx + 2.0 + (k % 2) * 2.4, -2.0 + k * 2.0, 0.3, rnd)
    return finalize('barn_02', smooth_angle=30)


def barn_open_hay():
    """E08_03 - long open-sided hay barn: post-and-beam frame, roof, stacked bales, no walls on the long sides."""
    reset()
    rnd = random.Random(220)
    W, D, posth = 34.0, 14.0, 11.0
    box(nm('slab'), (W, D, 0.4), loc=(0, 0, 0.2), key='dirt')
    # stone pads + timber posts in two rows
    nb = 6
    for i in range(nb):
        x = -W / 2 + 2.5 + (W - 5.0) * i / (nb - 1)
        for s in (-1, 1):
            y = s * (D / 2 - 1.0)
            box(nm('pad'), (1.4, 1.4, 0.8), loc=(x, y, 0.5), key='stone', bev=0.05)
            box(nm('post'), (0.7, 0.7, posth), loc=(x, y, 0.9 + posth / 2), key='timber', bev=0.03)
            # knee brace to the top beam
            lbeam(F(), (x, y, 0.9 + posth - 2.0), (x + (1.2 if i < nb - 1 else -1.2), y, 0.9 + posth - 0.3), 0.3, 'timber')
    # top plates (long beams) + cross ties
    for s in (-1, 1):
        y = s * (D / 2 - 1.0)
        box(nm('plate'), (W - 3.0, 0.5, 0.6), loc=(0, y, 0.9 + posth), key='wh2_capwood')
    for i in range(nb):
        x = -W / 2 + 2.5 + (W - 5.0) * i / (nb - 1)
        box(nm('tie'), (0.5, D - 2.0, 0.5), loc=(x, 0, 0.9 + posth), key='timber')
    wallh = 0.9 + posth
    # back wall boarded (one long side closed), front open
    board_wall(F(0, D / 2, 0, 180), W, 0.4, wallh, 'wh2_board', 'wh2_board_d', 221)
    # gable roof over the whole run
    gable_roof(F(0, 0, 0, 0), W, D, wallh, 6.0,
               keys=('wh2_board_d', 'wh2_board'), ov=1.4, ovg=1.0, wall='plaster', barge='timber', row=1.1, infill=False)
    # stacked hay bales in pyramids along the back half
    for i in range(nb - 1):
        bx = -W / 2 + 4.0 + (W - 8.0) * i / (nb - 1)
        base = rnd.randint(2, 3)
        for row in range(base):
            for j in range(base - row):
                hay_bale(bx + j * 2.4 - (base - row - 1) * 1.2, 2.2 + rnd.uniform(-0.3, 0.3),
                         0.4 + row * 1.35, rnd, w=2.2, d=1.4, h=1.3)
    # a loose pile + pitchfork
    blob(nm('loose'), 2.2, (-W / 2 + 4.0, -3.0, 0.3), 'thatch', subdiv=1, amp=0.3, scale=(1.6, 1.3, 0.6), seed=220)
    tube(nm('pf'), [(-W / 2 + 6.0, -3.5, 0.2), (-W / 2 + 6.4, -3.2, 3.2)], 0.08, 'wood_old', res=4)
    for k in range(3):
        tube(nm('pt'), [(-W / 2 + 6.4, -3.2, 3.2), (-W / 2 + 6.2 + k * 0.2, -3.2, 4.0)], 0.04, 'iron', res=3)
    return finalize('barn_03', smooth_angle=30)


# ============================================================ E09 windmills
def _lattice_sail(prefix, cx, cy, cz, length, width, angle_deg, key_frame='timber', key_sail='wh2_sail'):
    """One windmill sail arm pointing outward at angle_deg in the X-Z plane (mill faces -Y, sails on the front)."""
    a = math.radians(angle_deg)
    dx, dz = math.cos(a), math.sin(a)
    tip = (cx + dx * length, cy, cz + dz * length)
    base = (cx + dx * 0.8, cy, cz + dz * 0.8)
    # main spar
    beam3(base, tip, 0.3, 0.3, key_frame)
    # lattice: cross slats + a thin sail cloth strip on one side
    n = 8
    perp = (-dz, 0, dx)
    for i in range(1, n):
        t = i / n
        p = (base[0] + (tip[0] - base[0]) * t, cy, base[2] + (tip[2] - base[2]) * t)
        whalf = width * (1 - t * 0.3) / 2
        p0 = (p[0] - perp[0] * whalf, cy - 0.05, p[2] - perp[2] * whalf)
        p1 = (p[0] + perp[0] * 0.15 * width, cy - 0.05, p[2] + perp[2] * 0.15 * width)
        beam3(p0, p1, 0.12, 0.12, key_frame)
    # leading-edge rail (full width on the trailing side of the spar)
    lead = (base[0] - perp[0] * width, cy - 0.06, base[2] - perp[2] * width)
    leadt = (tip[0] - perp[0] * width * 0.8, cy - 0.06, tip[2] - perp[2] * width * 0.8)
    beam3(lead, leadt, 0.16, 0.16, key_frame)
    # canvas: a clear rectangular cloth from the spar out to the leading edge, offset toward -Y so it faces the viewer
    sailpts = [base, tip, leadt, lead]
    slab([(x, cy - 0.14, z) for (x, _, z) in sailpts], (0, -0.1, 0), key_sail)


def windmill_tower():
    """E09_01 - tower windmill: stone tapered tower ~14 base x 38 tall, wooden cap, balcony, four lattice sails."""
    reset()
    rnd = random.Random(301)
    baseR, topR, H = 7.0, 4.6, 30.0
    # tapered stone tower (lathe) with coursing rings
    prof = [(baseR, 0), (baseR, 1.0), (baseR - 0.3, 1.2)]
    nring = 9
    for i in range(nring + 1):
        t = i / nring
        r = baseR + (topR - baseR) * t
        prof.append((r, 1.2 + (H - 1.2) * t))
    lathe(nm('tower'), prof, loc=(0, 0, 0), key='stone', segs=24)
    # coursing bands
    for i in range(1, 6):
        z = H * i / 6
        r = baseR + (topR - baseR) * (z / H)
        torus(nm('course'), r + 0.05, 0.12, loc=(0, 0, z), key='stone_dark', segs=24, rsegs=4)
    # door at base (front -Y)
    f = F(0, -baseR + 0.2, 0, 0)
    lbox(f, (3.6, 1.2, 6.6), 0, -0.3, 3.3, 'wood_old')
    lbox(f, (4.2, 0.5, 0.6), 0, -0.4, 6.9, 'stone_dark')
    # interior backing so door isn't see-through
    cyl(nm('inner'), baseR - 1.2, H - 2, loc=(0, 0, (H - 2) / 2 + 0.5), key='wh2_board_d', verts=20)
    v4util.marker('mk_door', (0, -baseR, 0))
    # small windows spiralling up
    for k in range(3):
        z = 9.0 + k * 6.0
        ang = k * 90 + 30
        fr = F(math.cos(math.radians(ang + 90)) * 0, 0, 0, ang)
        r = baseR + (topR - baseR) * (z / H)
        fw = F(math.sin(math.radians(ang)) * r * 0, 0, 0)
        px = math.cos(math.radians(ang)) * r
        py = math.sin(math.radians(ang)) * r
        o = box(nm('win'), (1.4, 0.6, 2.0), loc=(px, py, z), key='glass_dark', rot=(0, 0, ang))
        o2 = box(nm('winf'), (1.7, 0.4, 2.3), loc=(px * 1.02, py * 1.02, z), key='wood_old', rot=(0, 0, ang))
    # balcony ring near the top
    bz = H - 5.0
    br = baseR + (topR - baseR) * (bz / H) + 1.4
    lathe(nm('balc'), [(br - 1.4, bz), (br, bz), (br, bz + 0.4), (br - 1.4, bz + 0.4)], loc=(0, 0, 0), key='timber', segs=24)
    nballus = 20
    for i in range(nballus):
        a = 2 * math.pi * i / nballus
        cyl(nm('bal'), 0.1, 1.4, loc=(math.cos(a) * (br - 0.2), math.sin(a) * (br - 0.2), bz + 0.9), key='timber', verts=6)
    torus(nm('brail'), br - 0.2, 0.1, loc=(0, 0, bz + 1.6), key='timber', segs=24, rsegs=4)
    # wooden cap (ogee dome) on top
    capz = H
    lathe(nm('cap'), [(0, capz), (topR + 0.6, capz), (topR + 0.8, capz + 0.5),
                      (topR * 0.5, capz + 3.2), (0, capz + 4.2)], loc=(0, 0, 0), key='wh2_capwood', segs=20)
    # tail pole (fantail) sticking back
    tube(nm('tail'), [(0, topR, capz + 1.0), (0, topR + 6.0, capz - 2.0)], 0.3, 'timber', res=4)
    # hub + four lattice sails on the front face (-Y)
    hubz = capz + 1.5
    hy = -(topR + 0.9)
    ball(nm('hub'), 0.9, loc=(0, hy, hubz), key='iron', segs=10, rings=8)
    for k in range(4):
        _lattice_sail(f'sl{k}', 0, hy - 0.4, hubz, 13.0, 3.2, 90 + k * 90)
    return finalize('windmill_01', smooth_angle=28)


def windmill_post():
    """E09_02 - smaller post windmill: boxy timber body on a central post + trestle, ladder tail, four sails."""
    reset()
    rnd = random.Random(310)
    # brick/stone trestle piers + cross timbers
    pierh = 4.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(nm('pier'), (1.6, 1.6, pierh), loc=(sx * 3.0, sy * 3.0, pierh / 2), key='stone', bev=0.05)
    # crossed trestle beams
    for (ax, ay, bx, by) in [(-3, -3, 3, 3), (-3, 3, 3, -3)]:
        beam3((ax, ay, pierh), (bx, by, pierh), 0.6, 0.6, 'timber')
    # central post
    box(nm('post'), (1.6, 1.6, 7.0), loc=(0, 0, pierh + 3.0), key='timber', bev=0.04)
    # the mill body (buck): a boarded box that sits on the post
    bodyz = pierh + 6.5
    bw, bd, bh = 9.0, 7.0, 9.0
    fl = {'front': F(0, -bd / 2, bodyz, 0), 'back': F(0, bd / 2, bodyz, 180),
          'left': F(-bw / 2, 0, bodyz, -90), 'right': F(bw / 2, 0, bodyz, 90)}
    for fx, span in ((fl['front'], bw), (fl['back'], bw), (fl['left'], bd), (fl['right'], bd)):
        board_wall(fx, span, 0, bh, 'wh2_board', 'wh2_board_d', rnd.randint(1, 999), t=0.3, vgap=0.9)
    box(nm('bceil'), (bw - 0.6, bd - 0.6, 0.4), loc=(0, 0, bodyz + bh - 0.3), key='wh2_board_d')
    box(nm('bfloor'), (bw - 0.4, bd - 0.4, 0.4), loc=(0, 0, bodyz + 0.2), key='wh2_board_d')
    # pitched little roof on the body
    gable_roof(F(0, 0, 0, 0), bw, bd, bodyz + bh, 3.0,
               keys=('wh2_board_d', 'wh2_board'), ov=0.6, ovg=0.5, wall='wh2_board', barge='timber', row=0.9)
    # ladder tail down to the ground at the back
    lz0 = bodyz + 1.0
    by0, by1 = bd / 2 + 0.5, bd / 2 + 7.0
    for s in (-1, 1):
        beam3((s * 0.8, by0, lz0), (s * 0.8, by1, 0.2), 0.16, 0.16, 'wood_old')
    for k in range(7):
        t = k / 7
        yy = by0 + (by1 - by0) * t
        zz = lz0 + (0.2 - lz0) * t
        box(nm('rung'), (1.9, 0.16, 0.16), loc=(0, yy, zz), key='wood_old')
    # hub + four sails on the front
    hy = -(bd / 2 + 1.0)
    hubz = bodyz + bh * 0.6
    ball(nm('hub'), 0.7, loc=(0, hy, hubz), key='iron', segs=10, rings=8)
    for k in range(4):
        _lattice_sail(f'ps{k}', 0, hy - 0.3, hubz, 9.5, 2.6, 45 + k * 90)
    return finalize('windmill_02', smooth_angle=28)


BATCHES = {
    'barns': ('v4_farm', [
        ('E08_01_barn_01', barn_gambrel, (1.0, -1.15, 0.4)),
        ('E08_02_barn_02', barn_stone_timber, (1.0, -1.15, 0.4)),
        ('E08_03_barn_03', barn_open_hay, (1.0, -1.1, 0.42)),
    ]),
    'windmills': ('v4_farm', [
        ('E09_01_windmill_01', windmill_tower, (1.0, -1.3, 0.55)),
        ('E09_02_windmill_02', windmill_post, (1.0, -1.25, 0.5)),
    ]),
}

