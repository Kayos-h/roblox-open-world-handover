"""v5_fx_vg - A4 fix module (worker vg). Rebuilds the flawed highland/forest/fortress/marsh models
from assignment A4 so a strict reviewer rates each OK. New palette keys use the prefix vg_f_.
Reuses round-1 colours through v5_vg.P; never re-registers a round-1 key. Front faces -Y, pivot bottom-centre z=0.
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v5kit
from v5kit import Acc, polar, tang, mk, ids, band, strata
import v5gen as G
import v4util
import v5_vg as R                                   # round-1 module: reuse its palette dict R.P

# ---- NEW palette (prefix vg_f_). Register through G.reg so each key becomes 'vg_f_<name>'.
P = G.reg('vg_f', {
    # snow / ice graded for spires and glaciers (cool, coherent - no camo)
    'rkdark': ((86, 88, 96), 'Slate', 0.0, 0.92), 'rkmid': ((120, 122, 130), 'Slate', 0.0, 0.92),
    'rklit': ((150, 152, 160), 'Cobblestone', 0.0, 0.9), 'snow': ((238, 243, 250), 'Snow', 0.0, 0.62),
    'snowc': ((224, 232, 242), 'Snow', 0.0, 0.66), 'ice': ((176, 206, 226), 'Ice', 0.0, 0.32),
    'icelo': ((150, 186, 212), 'Ice', 0.0, 0.3),
    # ROUND 2: warmer, more varied cliff rock (visible colour spread so it never reads as flat default grey)
    'cliff1': ((88, 80, 74), 'Slate', 0.0, 0.94), 'cliff2': ((120, 104, 90), 'Rock', 0.0, 0.93),
    'cliff3': ((150, 132, 110), 'Cobblestone', 0.0, 0.9), 'cliff4': ((176, 160, 136), 'Sandstone', 0.0, 0.88),
    'lichen': ((132, 148, 104), 'Grass', 0.0, 1.0), 'recess': ((52, 48, 52), 'Slate', 0.0, 0.96),
    # ROUND 2: warm lit stair stone (surround mid-tone, treads light - no near-black)
    'stair_lo': ((126, 110, 92), 'Rock', 0.0, 0.92), 'stair_mid': ((158, 142, 120), 'Cobblestone', 0.0, 0.9),
    'stair_hi': ((196, 182, 158), 'Sandstone', 0.0, 0.86),
    # ROUND 2: muted matte water for the gorge chute (darker + rough so it never reads as a glowing panel)
    'chute': ((78, 98, 112), 'Slate', 0.0, 0.85), 'chuted': ((60, 78, 92), 'Slate', 0.0, 0.88),
    'foam2': ((170, 182, 186), 'SmoothPlastic', 0.0, 0.8),
    # warm forest rock for cave mouths / giant-tree base (graded, darker void)
    'crk1': ((96, 92, 84), 'Slate', 0.0, 0.94), 'crk2': ((124, 118, 106), 'Rock', 0.0, 0.93),
    'crk3': ((150, 142, 126), 'Cobblestone', 0.0, 0.92), 'void': ((18, 17, 22), 'Slate', 0.0, 0.98),
    'moss': ((88, 118, 70), 'Grass', 0.0, 1.0), 'moss2': ((70, 100, 58), 'Grass', 0.0, 1.0),
    # birch
    'bbark': ((224, 222, 214), 'Wood', 0.0, 0.9), 'blent': ((42, 42, 48), 'Wood', 0.0, 0.9),
    'bleaf': ((78, 128, 66), 'Grass', 0.0, 1.0), 'bleaf2': ((110, 156, 84), 'Grass', 0.0, 1.0),
    'bgold': ((190, 182, 96), 'Grass', 0.0, 1.0),
    # giant tree
    'tbark': ((92, 70, 52), 'Wood', 0.0, 0.95), 'tleaf': ((64, 110, 56), 'Grass', 0.0, 1.0),
    'tleaf2': ((92, 138, 72), 'Grass', 0.0, 1.0), 'tleafd': ((48, 82, 46), 'Grass', 0.0, 1.0),
    # cypress
    'cbark': ((96, 78, 60), 'Wood', 0.0, 0.95), 'cleaf': ((70, 104, 66), 'Grass', 0.0, 1.0),
    'cleaf2': ((54, 86, 54), 'Grass', 0.0, 1.0), 'cmoss': ((120, 134, 86), 'Grass', 0.0, 1.0),
    # marsh hummock
    'hgrass': ((96, 128, 72), 'Grass', 0.0, 1.0), 'hgrass2': ((120, 150, 86), 'Grass', 0.0, 1.0),
    'hmud': ((86, 72, 54), 'Mud', 0.0, 1.0), 'hreed': ((150, 146, 92), 'Grass', 0.0, 1.0),
    # water chute (muted, matte, stepped - no glow)
    'water': ((96, 140, 170), 'SmoothPlastic', 0.0, 0.28), 'waterd': ((72, 112, 142), 'SmoothPlastic', 0.0, 0.3),
    'foam': ((206, 222, 230), 'SmoothPlastic', 0.0, 0.55),
    # fortress stone
    'wall': ((176, 170, 174), 'Limestone', 0.0, 0.9), 'wall2': ((158, 152, 158), 'Limestone', 0.0, 0.9),
    'trim': ((210, 204, 206), 'Limestone', 0.0, 0.88), 'frock1': ((104, 104, 112), 'Slate', 0.0, 0.93),
    'frock2': ((134, 132, 138), 'Cobblestone', 0.0, 0.92), 'froof': ((78, 92, 122), 'Slate', 0.0, 0.8),
    'tread': ((150, 146, 140), 'Cobblestone', 0.0, 0.9), 'treadd': ((118, 114, 110), 'Slate', 0.0, 0.92),
    'cloth': ((162, 60, 58), 'Fabric', 0.0, 1.0), 'gold': ((194, 160, 86), 'Metal', 0.75, 0.38),
})
SNOWROCK = [P['rkdark'], P['rkmid'], P['rklit'], P['snowc'], P['snow']]       # bottom->top grade
CROCK = [P['cliff1'], P['cliff2'], P['cliff3'], P['cliff4']]           # warm, high-contrast forest rock
FROCK = [P['cliff1'], P['cliff2'], P['cliff3']]                        # warm fortress rock
FK = {'stone': P['cliff2'], 'wall': P['wall'], 'trim': P['trim'], 'dark': P['void'], 'door': R.P['timber'],
      'deck': R.P['timber'], 'roof': P['froof'], 'roof2': P['cliff1'], 'gold': P['gold'], 'timber': R.P['timber'],
      'flag': P['cloth'], 'cap': P['snow'], 'glass': R.P['glass'], 'shutter': R.P['timber'], 'iron': R.P['iron'], 'sign': R.P['timber']}


def _fin(A, name):
    A.to_scene()
    return finalize(name, 28)


# ================================================================= FR03 cave mouths (solid grounded arch + recessed void)
def _cave_mouth(i):
    """A solid rock buttress with a framed, recessed dark cave opening. i picks silhouette variant so siblings differ."""
    reset()
    A = Acc()
    rnd = random.Random(7400 + i)
    W, D, H = 40.0, 30.0, 30.0
    ow = 9.0 + (i % 3) * 1.4                                     # opening half-widths vary per sibling
    oh = 13.0 + (i % 2) * 2.0
    lean = (-0.12, 0.0, 0.1, 0.06)[i % 4]
    npier = (7, 7, 8, 6, 7, 8)[i]                                # pier chunk count -> different height/bulk per sibling
    arch_h = (4.5, 5.5, 3.5, 6.0, 4.0, 5.0)[i]                   # lintel curvature varies silhouette
    stagger = (0.0, 0.0, 0.0, 1.2, -1.0, 0.8)[i]                 # pier lean/offset
    # --- solid side piers (two tall grounded masses either side of the mouth), stacked chunks that touch
    for sg in (-1, 1):
        base_x = sg * (ow + 7.0)
        for k in range(npier):
            t = k / float(npier - 1)
            z = 1.0 + k * 4.2
            w = 13.0 - 3.0 * t
            dep = D * (0.9 - 0.12 * t)
            A.chunk((w, dep, 5.2), (base_x + (lean + stagger * 0.02) * z + rnd.uniform(-0.5, 0.5), rnd.uniform(-0.6, 0.6), z),
                    band(CROCK, t, rnd), (0, 0, rnd.uniform(-5, 5)), 0.11, rnd, (0.95, 0.94))
    # --- lintel span that connects the two piers into one arch (overlaps both piers, no gap)
    for k in range(5):
        t = k / 4.0
        x = -ow - 2.0 + (2 * ow + 4.0) * t
        z = H - 7.0 + math.sin(math.pi * t) * arch_h
        A.chunk((8.0, D * 0.85, 7.5), (x + lean * z, rnd.uniform(-0.5, 0.5), z),
                band(CROCK, 0.8 + 0.2 * math.sin(math.pi * t), rnd), (0, 0, rnd.uniform(-6, 6)), 0.11, rnd, (0.9, 0.9))
    # --- recessed dark void: a back wall set INTO the mass plus a dark inner shell so the opening reads hollow
    A.box((ow * 2.0, 2.0, oh), (0, 6.0, oh / 2.0 + 0.5), P['void'], bev=0)          # deep back wall
    A.box((ow * 2.0 - 1.0, 14.0, 0.6), (0, 0.0, 0.3), P['void'], bev=0)             # dark floor of the recess
    A.box((ow * 2.0 + 1.0, 3.0, oh + 1.0), (0, -D / 2.0 + 2.0, oh / 2.0 + 0.3), P['void'], bev=0)  # shadow just inside the lip
    # --- framed opening: chamfered jamb blocks and a keystone so the mouth reads as an entrance, not a hole
    for sg in (-1, 1):
        A.box((2.4, 4.0, oh + 1.0), (sg * (ow + 0.4), -D / 2.0 + 3.0, oh / 2.0 + 0.3), band(CROCK, 0.5, rnd), bev=0.15)
    A.box((ow * 2.0 + 3.0, 4.2, 3.0), (0, -D / 2.0 + 3.0, oh + 1.2), band(CROCK, 0.85, rnd), bev=0.15)
    A.chunk((4.0, 4.4, 3.4), (0, -D / 2.0 + 2.8, oh + 0.5), P['crk3'], (0, 0, 0), 0.08, rnd)       # keystone
    # --- fallen rubble banked against the pier feet (touches ground AND the pier mass, not stranded in the open)
    for sg in (-1, 1):
        for k in range(4):
            A.chunk((rnd.uniform(2.4, 4.0), rnd.uniform(2.4, 3.4), rnd.uniform(1.4, 2.6)),
                    (sg * (ow + 7.0) + rnd.uniform(-5, 5), -D / 2.0 + rnd.uniform(4.0, 9.0), 0.9),
                    band(CROCK, rnd.random() * 0.4, rnd), (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    # --- moss embedded in the pier body (well below the crown so it always overlaps solid rock, never floats)
    for sg in (-1, 1):
        for k in range(2):
            A.ball(rnd.uniform(1.4, 2.0), (sg * (ow + 7.0), rnd.uniform(-5, 1), 9.0 + k * 7.0),
                   P['moss'] if k % 2 else P['moss2'], segs=6, rings=4, scale=(1.6, 1.4, 0.5))
    return _fin(A, 'cave_mouth')


# ================================================================= SP01 snow spires (graded snow-over-rock, thick taper, seated base)
def _snow_spire(i):
    reset()
    A = Acc()
    rnd = random.Random(7700 + i)
    # base mass graded dark->snow, big and seated
    A.mound(0, 0, 56.0, 56.0, 30.0, 26, [P['rkdark'], P['rkmid'], P['rklit'], P['snowc']], rnd, 0.0, 0.42, 0.95)
    # main spire: THICK taper, coherent grade (band by height), snow cap. Vary silhouette per sibling.
    baseR = 18.0 + (i % 3) * 1.5
    if i == 5:
        baseR = 22.0                                                                           # SP01_06: stouter base, distinct from 05
    topFrac = (0.16, 0.22, 0.12, 0.2, 0.2, 0.3)[i]
    lean = (0.0, 0.08, -0.06, 0.04, -0.1, 0.16)[i]
    tiers = 16
    z = 10.0
    H = 150.0
    for k in range(tiers):
        t = k / (tiers - 1.0)
        thick = 1.0 + 0.5 * (1.0 - t) ** 2                                                     # extra girth low down so the needle looks solid, not fragile
        rr = baseR * thick * (1.0 - (1.0 - topFrac) * t) * rnd.uniform(0.97, 1.05)
        sh = H / tiers * rnd.uniform(1.0, 1.15)
        key = band(SNOWROCK, t * 0.92 + 0.06, rnd, 0.05)              # snow accumulates up high, coherent
        A.chunk((rr * 2.0, rr * 1.9, sh * 1.12),
                (lean * t * 40.0 + rnd.uniform(-rr * 0.04, rr * 0.04), rnd.uniform(-rr * 0.04, rr * 0.04), z + sh / 2.0),
                key, (0, 0, rnd.uniform(0, 90)), 0.06, rnd, (0.92, 0.92))
        z += sh * 0.9
    A.chunk((baseR * topFrac * 2.4, baseR * topFrac * 2.4, 6.0), (lean * 40.0, 0, z), P['snow'], (0, 0, rnd.uniform(0, 90)), 0.06, rnd, (0.5, 0.5))
    # secondary spires, seated INTO the base mound (overlap it), count/placement vary per sibling
    sub = [(2, 10), (3, 12), (2, 9), (4, 11), (3, 13), (2, 8)][i]
    for q in range(sub[0]):
        a = (i * 47 + q * 360.0 / sub[0]) % 360
        x, y, _ = polar(sub[1] + rnd.uniform(-1.5, 1.5), a)
        sz = 8.0 + rnd.uniform(-1.0, 2.0)
        sH = 44.0 + rnd.uniform(0, 30)
        if i == 5 and q == 0:                                                                  # SP01_06: one tall shoulder peak for a twin-summit silhouette
            sz = 12.0
            sH = 96.0
        st = 10
        zz = 8.0
        for k in range(st):
            t = k / (st - 1.0)
            rr = sz * (1.0 - 0.75 * t) * rnd.uniform(0.95, 1.05)
            sh = sH / st * rnd.uniform(1.0, 1.2)
            A.chunk((rr * 2.0, rr * 1.9, sh * 1.1), (x + rnd.uniform(-rr * 0.1, rr * 0.1), y + rnd.uniform(-rr * 0.1, rr * 0.1), zz + sh / 2.0),
                    band(SNOWROCK, t * 0.9 + 0.08, rnd, 0.05), (0, 0, rnd.uniform(0, 90)), 0.1, rnd, (0.88, 0.88))
            zz += sh * 0.9
        A.chunk((sz * 0.9, sz * 0.9, 3.0), (x, y, zz), P['snow'], (0, 0, 0), 0.08, rnd, (0.5, 0.5))
    # snow drift settled at the base, touching ground
    for k in range(14):
        x, y, _ = polar(rnd.uniform(8, 26), rnd.uniform(0, 360))
        A.ball(rnd.uniform(2.0, 4.5), (x, y, 1.5), P['snow'], segs=7, rings=4, scale=(1.5, 1.4, 0.4))
    return _fin(A, 'snow_spire')


# ================================================================= LM07 carved switchback stairs (visible flights, landings, side walls)
def _switch_stairs(i):
    """LM07_01/02 (round 3, lead) - a SOLID banded rock tower with a switchback stair bolted to its front face. 50 W x 60 D x 60 H.
    The mass is a closed stack of four blocks (nothing hollow, no black void). Each stair flight is a stepped wedge fixed INTO the face, so every part overlaps the mass.
    Siblings: i=1 is mirrored and has a different back outline."""
    reset()
    A = Acc()
    rnd = random.Random(7100 + i)
    flip = -1.0 if i else 1.0
    W, H = 50.0, 60.0
    Y0, Y1 = -30.0, 30.0
    SD = 6.0
    face = Y0 + SD - 0.8
    bands = [P['cliff1'], P['cliff2'], P['cliff3'], P['cliff4']]
    seg = H / 4.0
    for b in range(4):
        wb = W - 2.5 * b + rnd.uniform(-1.0, 1.0)
        y_front = face + 0.2 * b
        y_back = Y1 - (2.0 + 2.5 * i) * b + rnd.uniform(-1.0, 1.0)
        A.box((wb, y_back - y_front, seg + 0.5), (flip * rnd.uniform(-0.8, 0.8), (y_front + y_back) / 2.0, b * seg + seg / 2.0), bands[b], bev=0.5)
    for k in range(18):                                                            # faceted bosses on the sides and the back (rock is not a box)
        z = rnd.uniform(4.0, H - 6.0)
        key = band(bands, z / H, rnd)
        w_at = W - 2.5 * int(z / seg)
        sx, sy, sz = rnd.uniform(6.0, 10.0), rnd.uniform(8.0, 13.0), rnd.uniform(5.0, 9.0)
        if k % 3 == 2:
            A.chunk((sy, sx, sz), (rnd.uniform(-w_at / 2.0 + 7.0, w_at / 2.0 - 7.0), Y1 - 3.5 - 2.5 * i * int(z / seg), z), key, (0, 0, rnd.uniform(-20, 20)), 0.14, rnd, (0.9, 0.9))
        else:
            sg = -1.0 if k % 2 else 1.0
            A.chunk((sx, sy, sz), (sg * (w_at / 2.0 - 2.0), rnd.uniform(face + 8.0, Y1 - 10.0), z), key, (0, 0, rnd.uniform(-20, 20)), 0.14, rnd, (0.9, 0.9))
    flights, per = 5, 6
    rise = H / (flights * per)
    run = 3.4
    half = per * run / 2.0
    for fl in range(flights):
        d = 1.0 if fl % 2 == 0 else -1.0
        z0 = fl * per * rise
        x0 = -half if d > 0 else half
        for s in range(per):
            sx = flip * (x0 + d * (s * run + run / 2.0))
            hh = rise * (s + 1)
            A.box((run + 0.1, SD, hh), (sx, Y0 + SD / 2.0, z0 + hh / 2.0), P['stair_mid'], bev=0.1)
            A.box((run + 0.3, SD + 0.6, 0.8), (sx, Y0 + SD / 2.0 - 0.2, z0 + hh - 0.35 + 0.07), P['stair_hi'], bev=0.1)
        lx = flip * (x0 + d * (per * run + 3.5))
        A.box((7.0, SD, per * rise), (lx, Y0 + SD / 2.0, z0 + per * rise / 2.0), P['stair_mid'], bev=0.1)
        A.box((7.3, SD + 0.6, 0.8), (lx, Y0 + SD / 2.0 - 0.2, z0 + per * rise - 0.35 + 0.07), P['stair_hi'], bev=0.1)
    A.box((W - 9.5, Y1 - 8.0 - face, 0.8), (0, (face + Y1 - 8.0) / 2.0, H + 0.2), P['cliff4'], bev=0.1)      # summit cap, flush with the last landing
    for k in range(7):                                                                                        # lichen on the summit and ledges, embedded in the cap
        A.ball(rnd.uniform(1.2, 2.2), (rnd.uniform(-14, 14), rnd.uniform(face + 6.0, Y1 - 12.0), H + 0.5), P['lichen'], segs=6, rings=4, scale=(1.6, 1.4, 0.4))
    return _fin(A, 'carved_stair')


# ================================================================= LM08 mountain span bridge (continuous deck, rails, piers, markers)
def stone_span():
    reset()
    A = Acc()
    rnd = random.Random(7200)
    span = 84.0
    deckz = 18.0
    # abutment masses at each end (grounded rock the deck lands on)
    for sg in (-1, 1):
        A.mound(sg * 40.0, 0, 20.0, 18.0, 20.0, 14, FROCK, rnd, 0.0, 0.45, 0.85)
        A.box((12.0, 14.0, 3.0), (sg * 38.0, 0, deckz - 1.0), P['wall'], bev=0.2)
    # ONE continuous deck slab with a gentle arch (single box per segment, segments overlap - no gaps)
    n = 14
    prev_x = -span / 2.0
    for k in range(n):
        t0 = k / float(n)
        t1 = (k + 1) / float(n)
        x0 = -span / 2.0 + span * t0
        x1 = -span / 2.0 + span * t1
        xc = (x0 + x1) / 2.0
        z = deckz + math.sin(math.pi * (t0 + t1) / 2.0) * 3.0
        A.box((span / n + 2.0, 12.0, 3.4), (xc, 0, z), P['cliff3'], bev=0.12)
    # supporting piers down to ground under the span (connected, read as supports not debris)
    for px in (-24.0, 0.0, 24.0):
        t = (px + span / 2.0) / span
        topz = deckz + math.sin(math.pi * t) * 3.0
        A.box((5.0, 7.0, topz), (px, 0, topz / 2.0), P['cliff2'], bev=0.15)
        A.box((7.0, 9.0, 2.0), (px, 0, 1.0), P['cliff1'], bev=0.1)                           # pier footing on ground
    # continuous solid parapet both sides: overlapping segments (no black gaps) + flush coping
    for sg in (-1, 1):
        for k in range(n):
            t = (k + 0.5) / float(n)
            x = -span / 2.0 + span * t
            z = deckz + math.sin(math.pi * t) * 3.0
            A.box((span / n + 3.0, 1.4, 3.6), (x, sg * 5.3, z + 2.9), P['cliff3'], bev=0.1)   # wide overlap, no gaps
            A.box((span / n + 3.0, 1.8, 0.6), (x, sg * 5.3, z + 4.7), P['cliff4'], bev=0.08)  # coping cap
        for k in range(8):
            t = k / 7.0
            x = -span / 2.0 + span * t
            z = deckz + math.sin(math.pi * t) * 3.0
            A.box((1.8, 2.0, 2.2), (x, sg * 5.3, z + 5.4), P['cliff2'], bev=0.1)              # merlon posts on the coping
    # markers kept from round-1 stone_span
    v4util.marker('mk_enda', (-span / 2.0 + 2.0, 0, deckz + 1.4))
    v4util.marker('mk_endb', (span / 2.0 - 2.0, 0, deckz + 1.4))
    v4util.marker('mk_deck', (0, 0, deckz + 4.6))
    return _fin(A, 'stone_span')


# ================================================================= LM23_03 gorge wall with recessed stepped water chute (muted blue, no glow)
def _gorge(i):
    reset()
    A = Acc()
    rnd = random.Random(7470 + i)
    G.cliff(A, rnd, 90.0, 28.0, 80.0, [P['cliff1'], P['cliff2'], P['cliff3'], P['cliff4']], 0, 0, 0, 12, P['moss'], True, 0.0 if i != 1 else 0.2)
    for k in range(12):
        x = rnd.uniform(-40, 40)
        A.ball(rnd.uniform(2.0, 4.0), (x, rnd.uniform(-14, -6), rnd.uniform(20, 70)), P['moss'] if k % 2 else P['moss2'], segs=7, rings=4, scale=(1.3, 1.1, 0.8))
    if i == 2:
        # recessed chute cut into the face with a NARROW matte dark-blue water ribbon; nothing bright, foam only at the base
        cx = 20.0
        A.box((10.0, 7.0, 64.0), (cx, -7.0, 36.0), P['recess'], bev=0)                        # deep mid-dark recess (not glowing, not pure black)
        for sg in (-1, 1):                                                                    # warm rock lips framing the chute
            A.chunk((3.4, 11.0, 66.0), (cx + sg * 7.0, -9.0, 34.0), band([P['cliff1'], P['cliff2'], P['cliff3']], 0.5, rnd), (0, 0, 0), 0.1, rnd)
        steps = 9
        for s in range(steps):
            t = s / (steps - 1.0)
            z = 66.0 - t * 62.0
            w = 3.6 + t * 1.2                                                                 # NARROW ribbon, matte dark blue-grey
            A.box((w, 2.6, 7.0), (cx, -9.6 + t * 1.5, z), P['chute'] if s % 2 else P['chuted'], (12, 0, 0), bev=0)
        # foam only where the water lands at the foot (low, muted grey-white)
        A.box((7.0, 3.6, 0.8), (cx, -11.0, 1.6), P['foam2'], bev=0)
        for k in range(4):
            A.ball(rnd.uniform(0.8, 1.4), (cx + rnd.uniform(-3, 3), -11.0 + rnd.uniform(-1.5, 1.5), 1.8), P['foam2'], segs=6, rings=4, scale=(1.3, 1.2, 0.5))
    return _fin(A, 'gorge_wall')


# ================================================================= VG04 birch (slim white bole, lenticels, green canopy + light accents)
def _birch(i):
    reset()
    A = Acc()
    rnd = random.Random(7600 + i)
    H = 34.0
    lean = (0.0, 0.5, -0.4)[i % 3]
    tr = 1.5                                                                                   # thicker upright bole (not a pole)
    # straight white trunk with slight taper, standing upright (not splayed)
    A.cyl(tr * 1.5, 1.4, (0, 0, 0), P['bbark'], verts=10, r2=tr * 1.25)                        # root flare
    segs = 8
    for k in range(segs):
        z = 1.2 + k * (H * 0.7) / segs
        lx = lean * (k / float(segs))
        A.cyl(tr * (1.0 - 0.4 * k / segs), (H * 0.7) / segs + 0.1, (lx, 0, z), P['bbark'], verts=10, r2=tr * (1.0 - 0.4 * (k + 1) / segs))
    # dark lenticel marks (short horizontal dashes) on the bole
    for k in range(12):
        zz = rnd.uniform(2.0, H * 0.55)
        a = rnd.uniform(0, 360)
        x, y, _ = polar(tr * 1.0, a)
        A.box((0.7, 0.18, 0.26), (x + lean * zz / H, y, zz), P['blent'], (0, 0, a), bev=0)
    # fuller crown broken into several clumps, seated ONTO the trunk top (lowest balls overlap the bole, no gap)
    trunk_top = 1.2 + H * 0.7
    clumps = [(0, 0, 1.0), (-3.5, 0.5, 0.6), (3.2, -0.6, 0.62), (0.5, 2.8, 0.55), (-0.8, -2.6, 0.55)]
    if i == 2:
        clumps = [(0, 0, 0.95), (-4.0, 1.0, 0.68), (4.0, -1.0, 0.68), (0, 3.2, 0.6), (0, -3.0, 0.58), (-2.2, -1.5, 0.5)]
    for (cxl, cyl, cs) in clumps:
        cz = trunk_top - 4.0 + (H - trunk_top + 3.0) * (0.15 + 0.4 * rnd.random())
        for j in range(3):
            a = rnd.uniform(0, 360)
            x, y, _ = polar(3.0 * cs * 0.5, a)
            key = P['bgold'] if rnd.random() > 0.85 else (P['bleaf2'] if j % 2 else P['bleaf'])
            A.ball(4.4 * cs * rnd.uniform(0.6, 0.85), (cxl + lean * 3.0 + x, cyl + y, cz + j * 2.0), key, segs=9, rings=6, scale=(1, 1, 1.0))
    return _fin(A, 'birch')


# ================================================================= FR01 giant trees (full connected canopy, solid single trunk)
def _giant_tree(i):
    """i==1: MINOR, distinct canopy from 01. i==2: MAJOR, solid single trunk + full connected canopy."""
    reset()
    A = Acc()
    rnd = random.Random(7300 + i)
    H = 150.0
    if i == 2:
        spread = 42.0
        trunkR = 10.0
    else:
        spread = 36.0
        trunkR = 9.0
    # SOLID single trunk: tapered drum from ground, buttress roots that touch ground
    A.cyl(trunkR * 1.5, 6.0, (0, 0, 0), P['tbark'], verts=14, r2=trunkR * 1.2)
    A.cyl(trunkR * 1.2, H * 0.52, (0, 0, 6.0), P['tbark'], verts=14, r2=trunkR * 0.75)
    for k in range(6):
        a = 60 * k + rnd.uniform(-12, 12)
        x, y, _ = polar(trunkR * 1.5, a)
        A.beam((x * 2.0, y * 2.0, 0.2), (x * 0.4, y * 0.4, 14.0), trunkR * 0.5, trunkR * 0.5, P['tbark'])
    # main limbs radiating up and out from the crown base
    crownz = H * 0.52
    nb = 7 if i == 2 else 6
    tips = []
    for k in range(nb):
        a = 360.0 * k / nb + rnd.uniform(-14, 14)
        x, y, _ = polar(spread * rnd.uniform(0.75, 1.0), a)
        ztop = H * rnd.uniform(0.74, 0.92)
        A.beam((0, 0, crownz), (x, y, ztop), trunkR * 0.5, trunkR * 0.45, P['tbark'])
        tips.append((x, y, ztop))
    # FULL CONNECTED canopy: a dense dome of overlapping foliage balls spanning the whole crown, filling gaps
    # central mass
    for (bx, by, bz) in [(0, 0, crownz + (H - crownz) * f) for f in (0.3, 0.55, 0.78, 0.95)]:
        A.ball(spread * (0.62 if i == 2 else 0.55), (bx, by, bz), P['tleaf'], segs=11, rings=7, scale=(1, 1, 0.82))
    # fill around each limb tip and between them so there is no hole / wishbone gap
    for (x, y, ztop) in tips:
        for j in range(4):
            f = 0.55 + 0.15 * j
            key = (P['tleaf'], P['tleaf2'], P['tleafd'])[j % 3]
            A.ball(spread * rnd.uniform(0.3, 0.42), (x * f + rnd.uniform(-2, 2), y * f + rnd.uniform(-2, 2), crownz + (ztop - crownz) * f + j * 4.0),
                   key, segs=9, rings=6, scale=(1, 1, 0.85))
    # a ring of outer clumps to round the silhouette (distinguishes 01 vs 02 by density/spread)
    ring = 14 if i == 2 else 10
    for k in range(ring):
        a = 360.0 * k / ring + rnd.uniform(-10, 10)
        rr = spread * (0.85 if i == 2 else 0.95)
        x, y, _ = polar(rr, a)
        zz = crownz + (H - crownz) * rnd.uniform(0.35, 0.8)
        A.ball(spread * rnd.uniform(0.26, 0.36), (x, y, zz), P['tleaf2'] if k % 2 else P['tleaf'], segs=9, rings=6, scale=(1, 1, 0.8))
    # mossy root mat
    A.mound(0, 0, 32.0, 32.0, 3.5, 9, [P['moss2'], P['moss']], rnd, 0.0, 0.3, 0.6)
    return _fin(A, 'giant_tree')


# ================================================================= HL01_04 ice spire (vary from siblings; keep ICE look)
def _ice_spire4():
    reset()
    A = Acc()
    rnd = random.Random(7040)
    A.mound(0, 0, 24.0, 24.0, 11.0, 12, [P['icelo'], P['ice'], P['snow']], rnd, 0.0, 0.45, 0.9)
    # distinct: a twinned leaning spire pair rather than one central + scatter
    for sg, lean, hh, rr in ((-1, -0.12, 60.0, 6.5), (1, 0.14, 50.0, 5.0)):
        x0 = sg * 4.0
        tiers = 9
        z = 7.0
        for k in range(tiers):
            t = k / (tiers - 1.0)
            r = rr * (1.0 - 0.72 * t)
            sh = hh / tiers * rnd.uniform(1.0, 1.2)
            A.chunk((r * 2.0, r * 1.8, sh * 1.1), (x0 + lean * t * hh * 0.3, rnd.uniform(-0.4, 0.4), z + sh / 2.0),
                    band([P['icelo'], P['ice'], P['snow']], t * 0.85 + 0.1, rnd, 0.05), (0, 0, rnd.uniform(0, 90)), 0.1, rnd, (0.86, 0.86))
            z += sh * 0.9
        A.chunk((rr * 0.6, rr * 0.6, 2.0), (x0 + lean * hh * 0.3, 0, z), P['snow'], (0, 0, 0), 0.08, rnd, (0.5, 0.5))
    for k in range(3):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(5, 8), a)
        A.chunk((rnd.uniform(2, 3), rnd.uniform(2, 3), rnd.uniform(6, 14)), (x, y, rnd.uniform(3, 7)), P['ice'], (0, 0, a), 0.14, rnd, (0.7, 0.7))
    return _fin(A, 'ice_spire')


# ================================================================= HL02_02 ice arch (reshape + merge base chunks)
def _ice_arch2():
    reset()
    A = Acc()
    rnd = random.Random(7102)
    # a flatter, wider arch than HL02_01, feet seated into solid mounds (no loose debris)
    G.rock_arch(A, rnd, 42.0, 34.0, 7.0, [P['icelo'], P['ice'], P['snow']], 0, 0, 0, 12.0, 13, P['snow'])
    for sg in (-1, 1):                                                                         # solid grounded feet
        A.mound(sg * 21.0, 0, 16.0, 14.0, 10.0, 10, [P['icelo'], P['ice'], P['snow']], rnd, 0.0, 0.45, 0.9)
    A.mound(0, 0, 44.0, 12.0, 5.0, 10, [P['snow'], P['ice']], rnd, 0.0, 0.3, 0.6)
    return _fin(A, 'ice_arch')


# ================================================================= HL03 glacier tongues (cool coherent ice, no brown camo; vary silhouette)
def _glacier(i):
    reset()
    A = Acc()
    rnd = random.Random(7200 + i)
    ICEG = [P['icelo'], P['ice'], P['snowc'], P['snow']]
    nplate = 9 + i                                                                             # plate count varies per sibling
    for k in range(nplate):
        x = -38.0 + k * (76.0 / (nplate - 1))
        L = 44.0 - abs(x) * (0.22 + 0.04 * i)
        A.chunk((10.5, L, rnd.uniform(3.4, 6.0)), (x, rnd.uniform(-2, 2), 2.4 + rnd.uniform(0, 1.3)),
                band(ICEG, 0.25 + 0.7 * (k / float(nplate)), rnd, 0.05), (0, 0, rnd.uniform(-6, 6)), 0.1, rnd, (0.9, 0.82))
        for j in range(2):
            A.chunk((rnd.uniform(3, 6), rnd.uniform(3, 8), rnd.uniform(3.0, 7.0)), (x + rnd.uniform(-2, 2), rnd.uniform(-9, 7), 4.0),
                    band(ICEG, 0.3 + 0.6 * rnd.random(), rnd, 0.05), (0, 0, rnd.uniform(0, 90)), 0.14, rnd, (0.72, 0.72))
    for k in range(4 + i):                                                                     # crevasses: thin soft-shadow grooves (not black, not brown)
        A.box((rnd.uniform(0.9, 1.5), rnd.uniform(10, 18), 0.4), (rnd.uniform(-32, 32), rnd.uniform(-6, 8), 5.8), P['recess'], (0, 0, rnd.uniform(-16, 16)), bev=0)
    for sg in (-1, 1):                                                                          # grey rock valley walls kept to the SIDES, not blotched over the ice
        A.mound(sg * 42.0, 14.0, 18.0, 20.0, 13.0, 9, [P['rkmid'], P['rklit'], P['cliff3']], rnd, 0.0, 0.5, 0.9)
    for k in range(8):
        x, y, _ = polar(rnd.uniform(0, 26), rnd.uniform(0, 360))
        A.chunk((rnd.uniform(5, 9), rnd.uniform(5, 9), 1.4), (x, y, 6.0), P['snow'], (0, 0, rnd.uniform(0, 90)), 0.12, rnd)
    return _fin(A, 'glacier_tongue')


# ================================================================= HL04_02 ice cave (vary opening from HL04_01)
def _ice_cave2():
    reset()
    A = Acc()
    rnd = random.Random(7302)
    ICEG = [P['icelo'], P['ice'], P['snowc']]
    # wider, lower overhanging mouth (distinct from 01's tall stack)
    for sg in (-1, 1):
        for k in range(5):
            A.chunk((9.0, 24.0, 5.6), (sg * 12.0 + rnd.uniform(-0.5, 0.5), 0, 2.8 + k * 4.6), band(ICEG, k / 4.0, rnd, 0.05), (0, 0, 0), 0.1, rnd, (0.94, 0.94))
    for k in range(5):                                                                          # overhanging lintel sloping down at front
        A.chunk((10.0, 22.0, 5.2), (-12.0 + k * 6.0, -2.0, 24.0 - k * 0.4), band(ICEG, 0.8, rnd, 0.05), (0, 0, 0), 0.08, rnd)
    A.box((11.0, 24.0, 0.4), (0, 0, 0.2), P['icelo'], bev=0)
    A.box((10.0, 20.0, 15.0), (0, 3.0, 7.6), P['void'], bev=0)
    for k in range(8):
        x = -4.0 + k * 1.1
        A.cyl(0.32, rnd.uniform(1.6, 4.2), (x, -12.0, 20.0), P['snow'], verts=5, r2=0.0, rot=(180, 0, 0))
    A.mound(0, 0, 38.0, 24.0, 10.0, 11, [P['snow'], P['ice']], rnd, 17.0, 0.3, 0.6)
    return _fin(A, 'ice_cave')


# ================================================================= HL07_02 mine entrance (alter timber framing/rubble from 01)
def _mine2():
    reset()
    A = Acc()
    rnd = random.Random(7602)
    for sg in (-1, 1):
        for k in range(4):
            A.chunk((8.0, 22.0, 5.0), (sg * 11.0, 0, 2.5 + k * 4.5), band([P['rkdark'], P['rkmid'], P['rklit']], k / 3.0, rnd, 0.06), (0, 0, 0), 0.1, rnd, (0.94, 0.94))
    for k in range(4):
        A.chunk((8.0, 22.0, 5.0), (-10.5 + k * 7.0, 0, 18.0), band([P['rkdark'], P['rkmid'], P['rklit']], 0.8, rnd, 0.06), (0, 0, 0), 0.1, rnd)
    A.box((9.0, 22.0, 13.0), (0, 2.0, 6.5), P['void'], bev=0)
    # DOUBLE-A-frame timber portal (distinct from 01's square posts) + spoil heap on the other side
    for sg in (-1, 1):
        A.beam((sg * 5.5, -10.0, 0.0), (sg * 2.2, -10.0, 13.6), 0.7, 0.7, R.P['timber'])
        A.beam((sg * 5.5, -8.0, 0.0), (sg * 3.0, -8.0, 11.5), 0.5, 0.5, R.P['timber'])
    A.box((12.0, 1.4, 1.4), (0, -9.0, 13.4), R.P['timber'], bev=0.08)
    A.box((8.0, 1.2, 1.0), (0, -10.0, 11.5), R.P['timber'], bev=0.08)
    for k in range(16):
        A.box((7.0, 0.5, 0.2), (0, -10.0 + k * 1.3, 0.2), R.P['timber'], bev=0)
    for sg in (-1, 1):
        A.box((0.2, 22.0, 0.3), (sg * 2.2, 1.0, 0.5), R.P['iron'], bev=0)
    for k in range(7):                                                                          # spoil-rock heap to one side
        A.chunk((rnd.uniform(1.4, 2.6),) * 2 + (rnd.uniform(1.0, 2.0),), (5.5 + rnd.uniform(-1.5, 1.5), -14.0 + rnd.uniform(-2, 2), 1.2), P['rkmid'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    return _fin(A, 'mine_mouth')


# ================================================================= LM05_02 fortress cliff tower (no stray beam; faceted base)
def _cliff_tower2():
    reset()
    A = Acc()
    rnd = random.Random(7902)
    # warm, relieved rock base (graded cliff colour + lichen, not plain grey)
    A.mound(0, 8.0, 34.0, 20.0, 42.0, 24, [P['cliff1'], P['cliff2'], P['cliff3'], P['cliff4']], rnd, 0.0, 0.4, 0.85)
    for k in range(7):
        x, y, _ = polar(rnd.uniform(6, 14), rnd.uniform(0, 360))
        A.chunk((rnd.uniform(4, 7), rnd.uniform(4, 7), rnd.uniform(3, 6)), (x, 8 + y, rnd.uniform(8, 36)), band([P['cliff1'], P['cliff2'], P['cliff3'], P['cliff4']], rnd.random(), rnd), (0, 0, rnd.uniform(0, 90)), 0.12, rnd)
    for k in range(5):
        x, y, _ = polar(rnd.uniform(7, 13), rnd.uniform(0, 360))
        A.ball(rnd.uniform(1.2, 2.0), (x, 8 + y, rnd.uniform(10, 34)), P['lichen'] if k % 2 else P['moss'], segs=6, rings=4, scale=(1.5, 1.3, 0.5))
    G.round_tower(A, rnd, 7.5, 56.0, FK, 0, -2.0, 8.0, top='cone', slits=4, bands=4, roof_k=1.4, verts=18, flag=True)
    # snow cap only, NO stray side beam
    for k in range(4):
        x, y, _ = polar(rnd.uniform(0, 9), rnd.uniform(0, 360))
        A.chunk((rnd.uniform(3, 5), rnd.uniform(3, 5), 1.4), (x, 8 + y, 40.0), P['snow'], (0, 0, rnd.uniform(0, 90)), 0.12, rnd)
    return _fin(A, 'cliff_tower')


# ================================================================= LM04_02/03 fortress rampart steps (distinct module arrangements)
def _rampart(i):
    """i: 1 and 2 (steps 02, 03). Give each a distinct tower/wall arrangement so they are not recolours of 01."""
    reset()
    A = Acc()
    rnd = random.Random(7800 + i)
    steps = 3
    for s in range(steps):
        x0 = -20.0 + s * 20.0
        z = s * 5.5
        A.box((20.0, 12.0, z + 4.0), (x0, 0, (z + 4.0) / 2.0), band([P['cliff1'], P['cliff2'], P['cliff3']], s / 2.0, rnd), bev=0.2)
        G.wall_seg(A, rnd, 20.0, 12.0 - 2.0, 8.0, FK, x0, 0, z + 4.0, 6.0, (s % 2 == 0), (s == 1))
    if i == 1:
        # 02: a single tall square keep at the high end + a low round bastion at the low end
        A.frustum((12.0, 12.0), (10.0, 10.0), 30.0, (28.0, 0, 11.0), P['wall'])
        A.box((14.0, 14.0, 2.0), (28.0, 0, 41.0), P['trim'], bev=0.1)
        for k in range(4):
            A.box((2.4, 1.2, 2.2), (22.0 + k * 4.0, -5.0, 42.5), P['wall'], bev=0.08)
        G.round_tower(A, rnd, 5.0, 16.0, FK, -26.0, 0, 0, top='crenel', slits=1, bands=1, verts=14)
    else:
        # 03: twin slim round turrets at both ends + a gatehouse arch in the middle step
        for sg in (-1, 1):
            G.round_tower(A, rnd, 4.0, 26.0 + (sg > 0) * 6.0, FK, sg * 28.0, 0, (sg > 0) * 11.0, top='cone', slits=2, bands=2, roof_k=1.5, verts=14)
        A.box((7.0, 13.0, 9.0), (0, 0, 5.5 + 4.5), P['void'], bev=0)                           # gate void
        for sg in (-1, 1):
            A.box((2.0, 13.0, 14.0), (sg * 4.5, 0, 5.5 + 7.0), P['wall'], bev=0.12)
        A.box((11.0, 13.0, 2.4), (0, 0, 5.5 + 13.5), P['trim'], bev=0.12)
    return _fin(A, 'stepped_rampart')


# ================================================================= FR02_05/06 forest ruins (relief + base + anchored cap)
def _forest_ruin(i):
    """i==4 -> ruin_05 (tall column, add break detail + base); i==5 -> ruin_06 (column + anchored capstone + rubble)."""
    reset()
    A = Acc()
    rnd = random.Random(7400 + i)
    st = [P['cliff1'], P['cliff2'], P['cliff3'], P['cliff4']]
    # grounded plinth base both get
    A.chunk((16.0, 14.0, 2.8), (0, 0, 1.4), P['cliff2'], (0, 0, 0), 0.06, rnd)
    for k in range(6):                                                                         # rubble resting ON the plinth top (z~2.8)
        A.chunk((rnd.uniform(2, 4), rnd.uniform(2, 4), rnd.uniform(1.6, 2.4)), (rnd.uniform(-7, 7), rnd.uniform(-5, 5), 3.0), band(st, rnd.random(), rnd), (0, 0, rnd.uniform(0, 90)), 0.18, rnd)
    if i == 4:
        # fluted standing column, snapped at the top (jagged crown), recessed coursing grooves, a fallen drum leaning on the plinth
        shaft_h = 26.0
        G.column(A, 0, 0, 2.8, 2.2, shaft_h, FK, 0.0, rnd)
        shaft_top = 2.8 + shaft_h
        for k in range(4):                                                                     # recessed dark coursing grooves (relief, not proud plates)
            A.box((4.9, 4.9, 0.5), (0, 0, 8.0 + k * 4.2), P['crk1'], bev=0)
        for q in range(5):                                                                     # jagged snapped crown (chunks biting into the shaft top)
            a = q * 72 + rnd.uniform(-10, 10)
            x, y, _ = polar(1.6, a)
            A.chunk((2.2, 2.2, rnd.uniform(1.4, 3.2)), (x, y, shaft_top - 0.5), P['cliff2'], (0, 0, a), 0.2, rnd, (0.6, 0.6))
        A.cyl(2.0, 4.6, (7.5, 1.0, 2.0), P['cliff3'], verts=10, rot=(0, 72, 20))                  # fallen drum resting on the plinth
    else:
        # stout column with a capstone RESTING on it (overlaps the shaft top, not floating) + rubble
        G.column(A, 0, 0, 2.8, 2.6, 21.0, FK, 0.15, rnd)
        A.box((7.0, 6.0, 2.8), (0, 0, 22.4), P['cliff3'], bev=0.12)                               # capstone sits on shaft top (overlaps)
        A.chunk((4.2, 4.2, 2.2), (0, 0, 24.4), P['cliff2'], (0, 0, 15), 0.08, rnd)
        for k in range(4):
            A.chunk((rnd.uniform(2, 3.2), rnd.uniform(2, 3), rnd.uniform(1.6, 2.2)), (rnd.uniform(-6, 6), rnd.uniform(-4, 4), 3.0), band(st, rnd.random(), rnd), (0, 0, rnd.uniform(0, 90)), 0.18, rnd)
    for k in range(10):                                                                        # moss clinging low on the shaft and plinth
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(2.6, 4.0), a)
        A.ball(rnd.uniform(1.0, 1.7), (x, y, rnd.uniform(3.0, 11.0)), P['moss'] if k % 2 else P['moss2'], segs=6, rings=4, scale=(1.3, 1.1, 0.7))
    return _fin(A, 'forest_ruin')


# ================================================================= VG05 swamp cypress (vary canopy/roots per sibling)
def _cypress(i):
    reset()
    A = Acc()
    rnd = random.Random(7900 + i)
    H = 38.0
    lean = (0.0, 0.6, -0.5)[i]
    trR = 1.3 + 0.2 * i
    # buttressed swollen base (fluted cypress) then tapering bole
    A.cyl(trR * 2.4, 3.0, (0, 0, 0), P['cbark'], verts=12, r2=trR * 1.5)
    for k in range(7):
        a = 360.0 * k / 7
        x, y, _ = polar(trR * 2.0, a)
        A.beam((x, y, 0.0), (x * 0.3, y * 0.3, 5.0), trR * 0.6, trR * 0.6, P['cbark'])          # root buttress fins
    A.cyl(trR * 1.2, H * 0.5, (0, 0, 3.0), P['cbark'], verts=10, r2=trR * 0.7)
    # canopy: narrow conical crown; count/width varies per sibling so silhouettes differ
    n = (7, 9, 6)[i]
    topz = H * 0.42
    for k in range(n):
        t = (k + 0.5) / n
        zz = topz + (H - topz) * t
        rr = (5.5 + i * 0.6) * (math.sin(math.pi * (0.2 + 0.8 * t)) * 0.9 + 0.12)
        for j in range(2):
            a = rnd.uniform(0, 360)
            x, y, _ = polar(rr * 0.4, a)
            A.ball(rr * rnd.uniform(0.6, 0.9), (x + lean * t * 3.0, y, zz + rnd.uniform(-0.6, 0.6)), P['cleaf'] if (k + j) % 2 else P['cleaf2'], segs=8, rings=5, scale=(1, 1, 1.25))
    # cypress knees around the base (count varies)
    for k in range(7 + i * 2):
        x, y, _ = polar(rnd.uniform(3.5, 8.0), rnd.uniform(0, 360))
        A.cyl(rnd.uniform(0.5, 0.9), rnd.uniform(1.4, 3.2), (x, y, 0), P['cbark'], verts=6, r2=0.2)
    # hanging moss strands, rooted up inside the crown mass (start near canopy base, hang down)
    for k in range(6):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(3, 6), a)
        A.cyl(0.16, rnd.uniform(4.0, 7.0), (x, y, 20.0), P['cmoss'], verts=5, r2=0.05, rot=(180, 0, 0))
    return _fin(A, 'swamp_cypress')


# ================================================================= VG06 marsh hummocks (tufts, mud rim, height variation)
def _hummock(i):
    reset()
    A = Acc()
    rnd = random.Random(8000 + i)
    # muddy rim ring (reads as wet marsh edge)
    A.cyl(8.0, 0.8, (0, 0, 0), P['hmud'], verts=12, r2=7.2)
    # grassy mound with real height variation (several overlapping humps, not one flat shard)
    nh = 3 if i == 0 else 4
    for q in range(nh):
        a = (i * 60 + q * 360.0 / nh) % 360
        x, y, _ = polar(rnd.uniform(0, 3.5), a)
        A.mound(x, y, rnd.uniform(7, 10), rnd.uniform(7, 10), rnd.uniform(3.5, 5.5), 7, [P['hgrass'], P['hgrass2']], rnd, 0.6, 0.45, 0.9, 0.16)
    # grass tufts standing up (bases pushed down into the mound so they are not read as floating blades)
    for k in range(22):
        x, y, _ = polar(rnd.uniform(0, 6.5), rnd.uniform(0, 360))
        A.cyl(0.12, rnd.uniform(1.8, 3.2), (x, y, 0.8), P['hreed'] if k % 3 else P['hgrass2'], verts=4, r2=0.04, rot=(rnd.uniform(-10, 10), rnd.uniform(-10, 10), 0))
    # a few mud clumps on the near edge
    for k in range(4):
        x, y, _ = polar(rnd.uniform(5, 7.5), rnd.uniform(220, 320))
        A.ball(rnd.uniform(0.8, 1.4), (x, y, 0.6), P['hmud'], segs=6, rings=3, scale=(1.4, 1.2, 0.5))
    return _fin(A, 'grass_hummock')


# ================================================================= HL07_01 mine entrance (NEVER REBUILT: warm relieved rock, thicker timber)
def _mine1():
    reset()
    A = Acc()
    rnd = random.Random(7601)
    RK = [P['cliff1'], P['cliff2'], P['cliff3'], P['cliff4']]
    for sg in (-1, 1):
        for k in range(4):
            A.chunk((8.0, 22.0, 5.0), (sg * 11.0 + rnd.uniform(-0.4, 0.4), 0, 2.5 + k * 4.5), band(RK, k / 3.0, rnd, 0.06), (0, 0, 0), 0.12, rnd, (0.94, 0.94))
        for q in range(3):                                                                     # relief facets so it is not a plain grey slab
            A.chunk((rnd.uniform(3, 5), rnd.uniform(3, 5), rnd.uniform(3, 5)), (sg * 11.0 + rnd.uniform(-3, 3), -8 + rnd.uniform(-2, 4), rnd.uniform(5, 18)), band(RK, rnd.random(), rnd), (0, 0, rnd.uniform(0, 90)), 0.14, rnd)
    for k in range(4):
        A.chunk((8.0, 22.0, 5.0), (-10.5 + k * 7.0, 0, 18.0), band(RK, 0.8, rnd, 0.06), (0, 0, 0), 0.1, rnd)
    A.box((9.0, 22.0, 13.0), (0, 2.0, 6.5), P['recess'], bev=0)                                 # recessed opening (mid-dark, not black)
    # thick square timber portal
    for sg in (-1, 1):
        A.box((1.6, 1.6, 13.6), (sg * 5.0, -10.0, 6.8), R.P['timber'], bev=0.1)
        A.beam((sg * 5.0, -10.2, 10.5), (sg * 2.4, -10.2, 13.2), 0.7, 0.7, R.P['timber'])
    A.box((12.0, 1.8, 1.8), (0, -10.0, 13.6), R.P['timber'], bev=0.1)
    A.box((10.0, 1.4, 1.2), (0, -9.4, 11.0), R.P['timber'], bev=0.1)                            # lintel brace
    for k in range(16):                                                                        # rails + sleepers
        A.box((7.0, 0.5, 0.2), (0, -10.0 + k * 1.3, 0.2), R.P['timber'], bev=0)
    for sg in (-1, 1):
        A.box((0.2, 22.0, 0.3), (sg * 2.2, 1.0, 0.5), R.P['iron'], bev=0)
    for k in range(6):                                                                          # spoil heap to one side, seated on ground
        A.chunk((rnd.uniform(1.6, 2.8),) * 2 + (rnd.uniform(1.0, 2.0),), (6.0 + rnd.uniform(-1.5, 1.5), -14.0 + rnd.uniform(-2, 2), 1.1), band(RK, rnd.random(), rnd), (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
    for k in range(4):                                                                          # lichen on the rock face
        x, y, _ = polar(rnd.uniform(8, 13), rnd.uniform(0, 360))
        A.ball(rnd.uniform(1.0, 1.6), (x, y, rnd.uniform(6, 16)), P['lichen'], segs=6, rings=4, scale=(1.4, 1.2, 0.5))
    return _fin(A, 'mine_mouth')


# ================================================================= BATCHES (same category folders as round 1)
def _gate_tunnel():
    """LM06_01 (round 3, lead) - fortress tunnel gate, 60 W x 60 D x 50 H: two grounded rock piers built as four thick stepped tiers with faceted bosses (no thin slabs),
    a three-tier lintel mass over a PASSABLE tunnel (mid-dark ceiling, paved floor), timber frame with braces, a stone sign block, warm banded colours, moss caps."""
    reset()
    A = Acc()
    rnd = random.Random(7600)
    W, D, H = 60.0, 60.0, 50.0
    ow, oh = 11.0, 22.0
    pw = W / 2.0 - ow
    fy = -25.5
    cols = [P['cliff1'], P['cliff2'], P['cliff3'], P['cliff4']]
    tiers = [(0.0, 14.0, 2.0, 51.0), (13.0, 13.0, 0.0, 49.0), (25.0, 12.5, -2.5, 46.0), (36.0, 12.0, -5.5, 42.0)]
    for sg in (-1, 1):
        for t, (zb, th, dw, dep) in enumerate(tiers):
            w = pw + dw
            A.box((w, dep, th + 0.6), (sg * (ow + w / 2.0), fy + 0.15 * t + dep / 2.0, zb + th / 2.0), cols[t], bev=0.6)
        A.box((pw - 7.0, 36.0, 2.0), (sg * (ow + (pw - 7.0) / 2.0 + 1.0), fy + 20.0, H - 0.2), P['moss'], bev=0.4)
    for t, (zb, ht, wx, dep) in enumerate(((oh, 9.0, 2.0, 49.0), (oh + 8.0, 9.5, 3.0, 47.0), (oh + 16.0, 12.0, 4.0, 42.0))):
        A.box((2 * ow + 2 * wx, dep, ht + 0.6), (0, fy + 0.2 * t + 0.07 + dep / 2.0, zb + ht / 2.0), cols[t + 1], bev=0.6)
    A.box((2 * ow + 10.0, 36.0, 2.0), (0, fy + 20.0, H - 0.2), P['moss'], bev=0.4)
    A.box((2 * ow + 0.4, D - 12.0, 0.8), (0, 0, oh - 0.1), P['recess'], bev=0)
    A.box((2 * ow + 0.4, D - 10.0, 0.5), (0, 0, 0.25), P['tread'], bev=0)
    for k in range(18):
        z = rnd.uniform(5.0, H - 9.0)
        key = band(cols, z / H, rnd)
        sx, sy, sz = rnd.uniform(5.0, 9.0), rnd.uniform(4.0, 7.0), rnd.uniform(4.0, 8.0)
        face = k % 4
        if face == 0:
            x, y = rnd.choice((-1, 1)) * rnd.uniform(ow + 6.0, W / 2.0 - 5.0), fy + 0.6
        elif face == 1:
            x, y = rnd.uniform(-W / 2.0 + 6.0, W / 2.0 - 6.0), fy + 49.0 - 1.2
        else:
            x, y = rnd.choice((-1, 1)) * (W / 2.0 - 1.2), rnd.uniform(fy + 8.0, fy + 40.0)
        if abs(x) < ow + 5.0 and z < oh + 4.0:
            z += oh + 4.0
        A.chunk((sx, sy, sz), (x, y, z), key, (0, 0, rnd.uniform(-25, 25)), 0.15, rnd, (0.9, 0.9))
    for sg in (-1, 1):
        A.box((2.4, 2.4, oh + 1.0), (sg * (ow + 0.5), fy + 0.2, (oh + 1.0) / 2.0), R.P['timber'], bev=0.1)
        A.beam((sg * (ow + 0.5), fy - 0.9, oh - 3.5), (sg * (ow - 3.5), fy - 0.9, oh + 0.4), 0.9, 0.9, R.P['timber'])
        A.box((3.4, 3.4, 1.0), (sg * (ow + 0.5), fy + 0.2, 0.5), P['cliff3'], bev=0.1)
    A.box((2 * ow + 4.0, 2.4, 2.4), (0, fy + 0.2, oh + 1.4), R.P['timber'], bev=0.1)
    A.box((13.0, 3.0, 4.0), (0, fy + 0.6, oh + 5.2), P['wall'], bev=0.12)
    A.box((9.0, 0.6, 1.4), (0, fy - 1.1, oh + 5.2), P['cliff1'], bev=0)
    A.box((2 * ow + 8.0, 6.0, 0.6), (0, fy - 3.0, 0.3), P['tread'], bev=0.1)
    return _fin(A, 'gate_tunnel')


def _altar_ruin():
    """FR02_04 (round 3, lead) - overgrown forest shrine ruin, 40 W x 30 D x 34 H: two-step plinth, altar with a stone urn (no gold), four columns of different heights
    (the two front ones carry a lintel), a fallen drum, moss. Warm banded stone only; nothing bright."""
    reset()
    A = Acc()
    rnd = random.Random(7403)
    KW = dict(FK, stone=P['cliff2'], wall=P['cliff3'], trim=P['cliff4'])
    A.chunk((40.0, 30.0, 3.0), (0, 0, 1.5), P['cliff2'], (0, 0, 0), 0.04, rnd)
    A.chunk((32.0, 22.0, 3.0), (0, 0, 4.5), P['cliff3'], (0, 0, 0), 0.04, rnd)
    A.chunk((12.0, 7.0, 5.0), (0, 0, 8.5), P['cliff4'], (0, 0, 0), 0.04, rnd)
    A.chunk((9.0, 5.0, 1.4), (0, 0, 11.7), P['cliff3'], (0, 0, 0), 0.04, rnd)
    A.cyl(1.2, 2.4, (0, 0, 12.4), P['cliff2'], verts=10, r2=0.9)
    A.ball(1.0, (0, 0, 15.0), P['cliff3'], segs=8, rings=5)
    for (x, y, h, br) in ((-13.0, -8.0, 26.0, 0.0), (13.0, -8.0, 26.0, 0.0), (-13.0, 8.0, 18.0, 0.55), (13.0, 8.0, 11.0, 0.7)):
        G.column(A, x, y, 6.0, 1.9, h, KW, br, rnd)
    A.box((30.0, 3.4, 2.6), (0, -8.0, 6.0 + 26.0 + 0.7), P['cliff3'], bev=0.15)
    A.cyl(1.8, 5.5, (-4.0, 9.0, 6.0 + 1.7), P['cliff3'], verts=10, rot=(0, 90, 25))
    for k in range(8):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(11.0, 16.0), a)
        A.chunk((rnd.uniform(2.4, 4.0), rnd.uniform(2.4, 3.6), rnd.uniform(1.6, 2.4)), (x * 1.2, y * 0.9, 3.4), band(CROCK, rnd.random(), rnd), (0, 0, rnd.uniform(0, 90)), 0.18, rnd)
    for k in range(12):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(8.0, 17.0), a)
        A.ball(rnd.uniform(1.0, 1.9), (x * 1.15, y * 0.85, rnd.uniform(2.8, 3.6)), P['moss'] if k % 2 else P['moss2'], segs=6, rings=4, scale=(1.4, 1.2, 0.5))
    return _fin(A, 'forest_ruin')


def _pool_rock(i):
    """LM24_02/03 (round 3, lead) - rocks standing in the fall pool, 30 W x 30 D x 16 H. Warm banded stone, moss, a muted matte pool skirt.
    i=1 a broad low boulder cluster with a flat table stone; i=2 two leaning stone spires over a boulder ring (different shape, not only placement)."""
    reset()
    A = Acc()
    rnd = random.Random(7500 + i)
    A.box((29.0, 27.0, 0.5), (0, 0, 0.25), P['chuted'], bev=0)
    if i == 1:
        A.mound(0, 0, 26.0, 24.0, 10.0, 26, CROCK, rnd, 0.0, 0.32, 0.6)
        A.chunk((13.0, 10.0, 5.0), (-3.0, 1.0, 9.5), P['cliff3'], (0, 0, 14), 0.08, rnd)
        A.chunk((7.0, 6.0, 5.0), (8.0, -4.0, 8.0), P['cliff2'], (0, 0, -20), 0.12, rnd, (0.8, 0.8))
        A.chunk((8.0, 7.0, 6.0), (-9.0, -5.0, 6.0), P['cliff1'], (0, 0, 40), 0.12, rnd, (0.8, 0.8))
    else:
        A.mound(0, 0, 25.0, 23.0, 6.0, 18, CROCK, rnd, 0.0, 0.3, 0.55)
        G.spire(A, rnd, 6.0, 16.0, CROCK, -5.0, 3.0, 0.0, 6, 0.12, None)
        G.spire(A, rnd, 4.2, 11.0, CROCK, 7.0, -2.0, 0.0, 5, -0.15, None)
    for k in range(6):
        A.ball(rnd.uniform(1.0, 1.8), (rnd.uniform(-7, 7), rnd.uniform(-6, 6), rnd.uniform(3.0, 7.0)), P['moss'] if k % 2 else P['moss2'], segs=6, rings=4, scale=(1.5, 1.3, 0.5))
    return _fin(A, 'pool_rocks')


def _glacier_post(A):
    r_ = random.Random(3211)
    A.chunk((62.0, 46.0, 6.0), (0, -2.0, 3.0), R.ICE[0], (0, 0, 0), 0.05, r_, (0.96, 0.96))
    A.chunk((52.0, 34.0, 6.0), (0, 4.0, 8.5), R.ICE[1], (0, 0, 0), 0.05, r_, (0.94, 0.94))
    A.chunk((40.0, 22.0, 5.0), (0, 9.0, 13.0), R.ICE[2], (0, 0, 0), 0.05, r_, (0.9, 0.9))


def _span_post(A):
    n = 18
    for k in range(n - 1):
        t = (k + 0.5) / (n - 1.0)
        x = -34.0 + 68.0 * t
        z = 17.0 + math.sin(math.pi * t) * 3.0
        A.box((4.6, 8.6, 1.5), (x, 0, z - 1.35), R.P['stoneM'], bev=0.1)


def _board_post(A):
    for sg in (-1, 1):
        for k in range(7):
            A.cyl(0.24, 3.2, (-14.0 + k * 4.7, sg * 2.65, 3.15), R.P['bark'], verts=6)
        A.box((30.0, 0.36, 0.36), (0, sg * 2.65, 6.3), R.P['timber'], bev=0)
        A.box((30.0, 0.3, 0.3), (0, sg * 2.65, 4.8), R.P['timber'], bev=0)


def fr02_01():
    return LK.wrap(lambda: R._forest_ruin(0), recolor=[LK.ramp([R.P['stoneM'], R.P['rock2'], R.P['rock']], CROCK, wobble=0.07)])()


def fr02_02():
    return LK.wrap(lambda: R._forest_ruin(1), recolor=[LK.ramp([R.P['stoneM'], R.P['rock2'], R.P['rock']], [P['cliff2'], P['cliff3'], P['cliff4']], wobble=0.07)])()


def fr02_03():
    return LK.wrap(lambda: R._forest_ruin(2), recolor=[LK.ramp([R.P['stoneM'], R.P['rock2'], R.P['rock']], [P['cliff1'], P['cliff2'], P['cliff3']], wobble=0.07)])()


def fr03_01():
    return LK.wrap(lambda: _cave_mouth_big(0))()


def hl03_02():
    return LK.wrap(lambda: _glacier(1), prune=[dict(keys=None, max_size=8.5, max_z=9.0)], post=_glacier_post)()


def lm05_01():
    return LK.wrap(lambda: R._cliff_tower(0), recolor=[LK.ramp(R.ROCK, CROCK, trange=(0.0, 45.0), wobble=0.07)])()


def lm05_02():
    return LK.wrap(_cliff_tower2, prune=[dict(keys=None, max_size=16.0, thin=2.5, max_z=6.0), dict(keys=[P['moss'], P['lichen']], max_size=1.8)])()


def lm08_01():
    return LK.wrap(stone_span, post=_span_post)()


def lm24_01():
    return LK.wrap(lambda: R._pool_rock(0), recolor=[LK.ramp(R.ROCK, CROCK, trange=(0.0, 16.0), wobble=0.08)])()


def sp01_04():
    return LK.wrap(lambda: _snow_spire_wide(3))()


def sp01_06():
    return LK.wrap(lambda: _snow_spire_wide(5))()


def vg05_01():
    return LK.wrap(lambda: R._cypress(0), prune=[dict(keys=None, max_size=10.0, thin=0.6)])()


def vg07_02():
    return LK.wrap(lambda: R._board(1), post=_board_post)()


BATCHES = {
    'a4_forest': ('v5_forest', mk(
        [(ids('FR01')[1], (lambda: _giant_tree(1))), (ids('FR01')[2], (lambda: _giant_tree(2)))] +
        [(ids('FR02')[3], _altar_ruin), (ids('FR02')[4], (lambda: _forest_ruin(4))), (ids('FR02')[5], (lambda: _forest_ruin(5)))] +
        [(ids('FR03')[1], (lambda: _cave_mouth(1))), (ids('FR03')[2], (lambda: _cave_mouth(2))),
         (ids('FR03')[3], (lambda: _cave_mouth(3))), (ids('FR03')[4], (lambda: _cave_mouth(4))), (ids('FR03')[5], (lambda: _cave_mouth(5)))] +
        [(ids('VG04')[0], (lambda: _birch(0))), (ids('VG04')[1], (lambda: _birch(1))), (ids('VG04')[2], (lambda: _birch(2)))] +
        [(ids('LM23')[0], (lambda: _gorge(0))), (ids('LM23')[2], (lambda: _gorge(2)))] +
        [(ids('LM24')[1], (lambda: _pool_rock(1))), (ids('LM24')[2], (lambda: _pool_rock(2)))] +
        [(ids('VG05')[1], (lambda: _cypress(1))), (ids('VG05')[2], (lambda: _cypress(2)))] +
        [(ids('VG06')[0], (lambda: _hummock(0))), (ids('VG06')[1], (lambda: _hummock(1)))], 0.1)),
    'a4_himalaya': ('v5_himalaya', mk(
        [(ids('SP01')[j], (lambda j=j: _snow_spire(j))) for j in range(6)] +
        [(ids('HL01')[3], _ice_spire4), (ids('HL02')[1], _ice_arch2)] +
        [(ids('HL03')[0], (lambda: _glacier(0))), (ids('HL03')[1], (lambda: _glacier(1))), (ids('HL03')[2], (lambda: _glacier(2)))] +
        [(ids('HL04')[1], _ice_cave2), (ids('HL07')[0], _mine1), (ids('HL07')[1], _mine2)], 0.1)),
    'a4_landmarks': ('v5_landmarks', mk(
        [(ids('LM04')[1], (lambda: _rampart(1))), (ids('LM04')[2], (lambda: _rampart(2)))] +
        [(ids('LM05')[1], _cliff_tower2)] +
        [(ids('LM06')[0], _gate_tunnel)] +
        [(ids('LM07')[0], (lambda: _switch_stairs(0))), (ids('LM07')[1], (lambda: _switch_stairs(1)))] +
        [(ids('LM08')[0], stone_span)], 0.1)),
}


# --- lead4 registration ---
import inspect
import v5_leadkit as LK
exec(inspect.getsource(_cave_mouth).replace('def _cave_mouth(i):', 'def _cave_mouth_big(i):').replace('ow = 9.0 + (i % 3) * 1.4', 'ow = 12.5').replace('oh = 13.0 + (i % 2) * 2.0', 'oh = 17.0'))
exec(inspect.getsource(_snow_spire).replace('def _snow_spire(i):', 'def _snow_spire_wide(i):').replace('baseR = 18.0 + (i % 3) * 1.5', 'baseR = 25.0 + (i % 3) * 1.5').replace('baseR = 22.0 ', 'baseR = 29.0 ').replace('topFrac = (0.16, 0.22, 0.12, 0.2, 0.2, 0.3)[i]', 'topFrac = (0.16, 0.22, 0.12, 0.36, 0.2, 0.44)[i]'))
BATCHES['lead4_forest'] = ('v5_forest', mk([('FR02_01_forest_ruin_01', fr02_01), ('FR02_02_forest_ruin_02', fr02_02), ('FR02_03_forest_ruin_03', fr02_03), ('FR03_01_cave_mouth_01', fr03_01),
                                            ('LM24_01_fall_pool_rock_01', lm24_01), ('VG05_01_tree_cypress_swamp_01', vg05_01), ('VG07_02_boardwalk_02', vg07_02)], 0.1))
BATCHES['lead4_hima'] = ('v5_himalaya', mk([('HL03_02_glacier_tongue_02', hl03_02), ('SP01_04_snow_spire_cluster_04', sp01_04), ('SP01_06_snow_spire_cluster_06', sp01_06)], 0.1))
BATCHES['lead4_land'] = ('v5_landmarks', mk([('LM05_01_fortress_cliff_tower_01', lm05_01), ('LM05_02_fortress_cliff_tower_02', lm05_02), ('LM08_01_mountain_span_bridge', lm08_01)], 0.1))
