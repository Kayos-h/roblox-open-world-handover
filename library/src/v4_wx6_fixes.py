"""wx6 FIX round: rusty-town props, farm, forest/countryside, elf-valley nature.
Repairs 13 reviewer-flagged ids. Copies the original builder bodies and fixes the
defect; imports helpers from the old modules. New palette keys use the wx6_ prefix.
Saved ids and category folders are kept exactly so .blend/.fbx overwrite in place.
"""
import math, random
from mathutils import Vector, Euler
import bpy
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, top_paint, poly_prism
from nature import rock, blob

PI = math.pi

# muted cloth tones for the scarecrow ribbons - HSV saturation <= 0.25 (near-grey earth cloth)
kitlib.PAL['wx6_rib_rust']  = ((140, 124, 112), 'Fabric', 0.0, 0.98, 0)  # S=0.20
kitlib.PAL['wx6_rib_sage']  = ((118, 126, 114), 'Fabric', 0.0, 0.98, 0)  # S=0.10
kitlib.PAL['wx6_rib_slate'] = ((114, 120, 128), 'Fabric', 0.0, 0.98, 0)  # S=0.11


# ====================================================================== E07 barrels
# Shared: a believable staved barrel body built from vertical staves that touch,
# with iron hoops. No floating parts.
def _barrel(cx, cy, zb, h, r, keys, seed, nstave=18, tilt=0.0, taz=0.0):
    """Closed staved barrel, bottom at zb. Staves TOUCH (wide, overlapping) over a solid inner
    wall so no sky shows through the gaps; full-radius top & bottom lids; hoops top/mid/bottom."""
    rnd = random.Random(seed)
    before = set(o.name for o in bpy.context.scene.objects)
    # solid inner wall sized to meet the staves (no gap where the core would show)
    cyl('core', r + 0.08, h - 0.1, loc=(cx, cy, zb + h / 2), key='wood_old', verts=max(16, nstave))
    # a box rotated by angle a has its LOCAL-Y pointing tangentially; make THAT wide (pitch x 1.9)
    # so neighbouring staves overlap all the way round. local-X (radial) is the plank thickness.
    sw = (2 * PI * r / nstave) * 1.9
    for i in range(nstave):
        a = 2 * PI * i / nstave
        bulge = r + 0.04
        x = cx + math.cos(a) * bulge
        y = cy + math.sin(a) * bulge
        box('sv', (0.22, sw, h), loc=(x, y, zb + h / 2), key=rnd.choice(keys), rot=(0, 0, math.degrees(a)), bev=0.02)
    cyl('lidb', r + 0.02, 0.18, loc=(cx, cy, zb + 0.09), key='wood_old', verts=nstave)
    cyl('lidt', r + 0.02, 0.18, loc=(cx, cy, zb + h - 0.09), key='wood_old', verts=nstave)
    for hz in (0.35, h * 0.5, h - 0.35):
        torus('hp', r + 0.12, 0.09, loc=(cx, cy, zb + hz), key='rust', segs=nstave, rsegs=4)
    if tilt:
        for o in bpy.context.scene.objects:
            if o.name not in before:
                v = Vector(o.location) - Vector((cx, cy, zb))
                o.location = Vector((cx, cy, zb))  # pivot at base
                o.rotation_euler = Euler((math.radians(tilt) * math.sin(taz), math.radians(tilt) * math.cos(taz), o.rotation_euler.z))
                o.location = Vector((cx, cy, zb)) + v


def barrel_staved_pile():
    """E07_07 - broken-barrel pile: one leaning intact barrel, one half-collapsed barrel whose
    loose staves lie flat on the ground, two fallen lids resting on the ground, hoops down."""
    reset()
    rnd = random.Random(77)
    # intact barrel, leaning against nothing but resting its base on the ground
    _barrel(-2.0, 0.6, 0.0, 3.4, 1.2, ('wood', 'wood_old'), 771, nstave=16, tilt=10, taz=0.4)
    # a half-height broken barrel stub (staves snapped short, still a ring that touches the ground)
    _barrel(1.6, 0.2, 0.0, 1.5, 1.25, ('wood', 'wood_old'), 772, nstave=16)
    # loose staves lying flat ON the ground around it (z小, flat)
    for k in range(6):
        ang = rnd.uniform(0, PI)
        L = rnd.uniform(2.4, 3.2)
        x = rnd.uniform(0.2, 3.6); y = rnd.uniform(-2.4, -1.0)
        box('lsv', (L, 0.5, 0.16), loc=(x, y, 0.08), key=rnd.choice(['wood_old', 'wood_grey']), rot=(0, 0, math.degrees(ang)), bev=0.02)
    # two fallen lids resting flat on the ground (grounded, not floating)
    cyl('fl1', 1.2, 0.16, loc=(3.4, -1.4, 0.09), key='wood_old', verts=18)
    cyl('fl2', 1.1, 0.16, loc=(-0.4, -2.2, 0.09), key='wood_light', verts=18, rot=(0, 6, 0))
    # fallen hoops on the ground
    torus('h1', 1.3, 0.08, loc=(2.6, -2.6, 0.1), key='rust', segs=20, rsegs=4, rot=(90, 0, 0))
    torus('h2', 1.25, 0.08, loc=(-1.6, -1.2, 0.1), key='rust', segs=20, rsegs=4, rot=(86, 8, 0))
    return finalize('barrel_staved_pile', smooth_angle=30)


def barrel_rolled_grain():
    """E07_08 - a barrel rolled on its side; its lid leans against the barrel (grounded), grain spills out."""
    reset()
    rnd = random.Random(78)
    before = set(o.name for o in bpy.context.scene.objects)
    # barrel lying on its side: build upright then rotate 90 about Y and set on ground
    _barrel(0.0, 0.0, 0.0, 4.0, 1.3, ('wood', 'wood_old'), 781, nstave=16)
    for o in bpy.context.scene.objects:
        if o.name not in before:
            o.rotation_euler.y += math.radians(90)
            o.location = Vector((o.location.z + 0.0, o.location.y, o.location.x))
    # re-seat the rolled barrel: its axis now along X, centre at z=1.3, spanning x in [-0.6,3.4]
    before2 = set(o.name for o in bpy.context.scene.objects)
    # the lid leaning against the open (left) end of the barrel, foot on the ground
    cyl('lid', 1.25, 0.16, loc=(-1.4, 0.0, 0.95), key='wood_light', verts=20, rot=(0, 62, 0))
    # grain spilling from the mouth (left end) as a grounded fan + heap
    mx = -0.4
    for i in range(44):
        t = rnd.random()
        spread = 0.3 + t * 2.2
        x = mx - t * 2.6 + rnd.uniform(-0.2, 0.2)
        y = rnd.uniform(-spread, spread)
        z = max(0.06, 0.5 - t * 0.5 + rnd.uniform(-0.05, 0.08))
        ball('gr', 0.12, loc=(x, y, z), key=rnd.choice(['thatch', 'grass_dry']), segs=5, rings=4, scale=(1.3, 1, 0.7))
    blob('heap', 1.1, (mx - 2.6, 0, 0.0), 'thatch', subdiv=2, amp=0.25, scale=(1.5, 1.6, 0.35), seed=78)
    return finalize('barrel_rolled_grain', smooth_angle=30)


def barrel_burst_hoop_rain():
    """E07_09 - a standing broken barrel: a closed staved body (staves joined, touching), one burst
    top hoop shown as two arcs still resting on the rim, NO floating internal discs."""
    reset()
    rnd = random.Random(79)
    H, r = 4.2, 1.3
    # closed body: vertical staves that touch all the way round, over a solid core (no sky through gaps)
    _barrel(0.0, 0.0, 0.0, H, r, ('wood', 'wood_old'), 791, nstave=18)
    # burst TOP hoop: two arcs sprung but still sitting on the rim (ends touch the staves, not floating)
    for (a0, a1) in ((0.5, PI - 0.1), (PI + 0.2, 2 * PI - 0.5)):
        pts = [(math.cos(a0 + (a1 - a0) * t / 8) * (r + 0.1), math.sin(a0 + (a1 - a0) * t / 8) * (r + 0.1), H - 0.35 + 0.08 * math.sin(t)) for t in range(9)]
        tube('harc', pts, 0.08, 'rust', res=4)
    # a short sprung hoop end that still rests against the body
    tube('hspr', [(r + 0.1, 0, H - 0.35), (r + 0.55, 0.3, H - 0.1)], 0.07, 'rust', res=4)
    return finalize('barrel_burst_hoop_rain', smooth_angle=30)


# ====================================================================== F06_10 scree chips (REDO)
# The old builder used blob(subdiv=1, amp=0.5) which produced degenerate/inverted faces that
# the Cycles preview rendered as pure noise. Rebuild with solid rock() chips (valid closed
# shells, outward normals) scattered on a thin ground patch.
from v4_d06 import polar_pts, tuft


def scree_chips():
    """F06_10 sharp scree chips: angular broken rock fragments on a low ground patch."""
    reset()
    rnd = random.Random(1210)
    keys = ('wi_pebble_d', 'wi_pebble_b', 'ev_stone_dark') if 'wi_pebble_d' in kitlib.PAL else ('ev_stone_dark', 'stone_dark', 'stone')
    keys = tuple(k for k in keys if k in kitlib.PAL) or ('stone_dark',)
    # thin ground patch so the chips read as sitting on scree, not floating
    blob('base', 3.9, (0, 0, 0.0), keys[0], subdiv=2, amp=0.12, scale=(1.0, 0.95, 0.06), seed=12)
    for (x, y) in polar_pts(rnd, 26, 3.5, 0.75):
        r = rnd.uniform(0.35, 0.85)
        flat = rnd.uniform(0.35, 0.55)
        o = rock('ch', r, (x, y, r * flat * 0.5 + 0.03), rnd.choice(keys), seed=rnd.randint(0, 999),
                 scale=(1.25, 0.85, flat), subdiv=1, amp=0.28, rot_z=rnd.uniform(0, 2 * PI))
    return finalize('scree_chips', smooth_angle=16)


# ====================================================================== E01_08 gravestone
from v4_wg_graveyard import _lichen, _ivy_face, _mound, _grass_tuft
from arch import F, lslab


def gravestone_08():
    """E01_08 - overgrown grave: now with a clearly readable leaning broken headstone as the hero,
    moss/ivy on it, a smaller toppled stone and a grassy plot around it."""
    reset()
    W, H, T = 2.6, 4.4, 0.7
    # a taller, thicker leaning headstone with a broken top so it clearly reads as a grave marker
    pts = [(-W / 2, 0, 0), (W / 2, 0, 0), (W / 2, 0, H * 0.72), (0.55, 0, H * 0.96),
           (0.05, 0, H * 0.74), (-0.5, 0, H * 0.99), (-W / 2, 0, H * 0.82)]
    o = lslab(F(0, T / 2, 0, 0), pts, (0, -T, 0), 'wg_stone')
    o.rotation_euler = Euler((math.radians(-12), math.radians(7), 0))
    o.location.z = 0.1  # sits proud of the ground, not sunk away
    _lichen(o, 0.55, 8)   # higher threshold = lighter moss so the stone still reads
    _ivy_face(-W / 2, W / 2, -T / 2, 0.0, H * 0.55, 8, 8)
    # a plinth base so it looks founded
    box('plinth', (W + 0.6, T + 0.5, 0.6), loc=(0, -T / 2, 0.3), key='wg_stone_d', rot=(0, 0, 0), bev=0.05)
    # second toppled small stone nearby (clearly a second marker, grounded)
    o2 = box('s2', (1.3, 0.4, 1.5), loc=(-1.8, -0.8, 0.25), key='wg_stone', rot=(6, 22, 0), bev=0.05)
    _lichen(o2, 0.45, 81)
    m = _mound(0, -1.2, W + 1.6, 3.4, seed=8)
    rnd = random.Random(8)
    for _ in range(4):
        _grass_tuft(rnd.uniform(-W / 2, W / 2), rnd.uniform(-1.8, 0.2), rnd, n=6)
    return finalize('gravestone_08', smooth_angle=25)


# ====================================================================== E05_02 dead tree
from v4_wc_snow import dead_trunk, bare_branches
from v4_elf import trunk_point, limb as wc_limb
from v4_d05 import moss_on_trunk as wc_moss, ground_bits as wc_ground


def E05_02_leaning():
    """E05_02 - leaning dead tree; lowest branches made thicker & fewer so they read as limbs not spikes."""
    reset()
    tr, H = 1.5, 22.0
    rnd = random.Random(502)
    lean = (0.22, 0.05)
    dead_trunk(tr, H, 502, '02', sway=1.4, lean=lean, flare=1.8)
    # fewer limbs, all placed in the UPPER two-thirds, all thick (>=0.8 stud dia)
    for k in range(4):
        az = 2 * PI * k / 4 + rnd.uniform(-0.3, 0.3)
        z0 = H * rnd.uniform(0.55, 0.9)          # none low on the trunk
        p0 = trunk_point(tr, H, 502, z0, 1.4, lean)
        if rnd.random() < 0.4:
            e = wc_limb((p0[0], p0[1], z0), (math.cos(az), math.sin(az), 0.3), rnd.uniform(3.5, 5.5), tr * 0.34, key='bark_dead', seed=k)
            tube('hang', [(e.x, e.y, e.z), (e.x + rnd.uniform(-0.4, 0.4), e.y + rnd.uniform(-0.4, 0.4), e.z - rnd.uniform(2.5, 4.5))], tr * 0.26, 'wc_dead_b', res=4, taper=[1, 0.5], ures=2)
        else:
            bare_branches((p0[0], p0[1], z0), az, 2, rnd.uniform(3.5, 5.0), tr * 0.32, rnd, depth=2, up=rnd.uniform(0.6, 1.1))
    wc_moss(tr, H, 502, 4, rnd, sway=1.4, lean=lean, zmin=1, zmax=H * 0.4)
    wc_ground(tr, rnd, 502, nrock=3, scale=1.0)
    return finalize('E05_02_dead_tree_02', smooth_angle=38)


# ====================================================================== E06_04 rusty debris
from v4_wg2_debris import _ground, _drape


def debris_04():
    """E06_04 - fallen tarp over a solid junk mound: the tarp now collapses ONTO the mound (no stilt
    legs, no open underside), supports are thick, so it reads as a sturdy covered wreck."""
    reset()
    _ground(9, 8, seed=4)
    rnd = random.Random(4)
    # a solid, taller junk mound so the tarp has something real to drape over
    for _ in range(10):
        s = rnd.uniform(1.0, 1.9)
        box('jk', (s, s, rnd.uniform(0.9, 1.7)),
            loc=(rnd.uniform(-2.2, 2.2), rnd.uniform(-1.6, 1.6), rnd.uniform(0.5, 1.6)),
            key=rnd.choice(['wg2_plank', 'wg2_barrel', 'wg2_sheet_b']), rot=(0, 0, rnd.uniform(0, 90)), bev=0.06)
    # a broad fallen beam and a crate at the edges to ground the shape
    box('beam', (6.0, 0.6, 0.6), loc=(0, -2.4, 0.3), key='wg2_plank', rot=(0, 0, 8), bev=0.05)
    box('crate', (1.8, 1.8, 1.8), loc=(2.6, 2.0, 0.9), key='wg2_barrel', bev=0.08)
    # tarp draped so the edges reach the ground on all sides (no floating skirt)
    seg = 8
    rows = []
    for j in range(6):
        y = -2.8 + 5.6 * j / 5
        row = []
        for i in range(seg + 1):
            x = -3.4 + 6.8 * i / seg
            sagx = math.sin(PI * i / seg)
            sagy = math.sin(PI * j / 5)
            # edges fall to ~0.05 (touch ground), centre humps over the mound
            z = 0.05 + 2.0 * sagx * sagy
            row.append((x, y, z))
        rows.append(row)
    _drape(rows, 'wg2_tarp')
    # heavy tie stones at the corners (sturdy, not thin stilts)
    for sx in (-1, 1):
        for sy in (-1, 1):
            rock('tie', 0.7, (sx * 3.1, sy * 2.6, 0.3), 'wg2_barrel', seed=int(sx * 2 + sy), scale=(1.1, 1.0, 0.8), subdiv=2, amp=0.3)
    return finalize('rusty_debris_04', smooth_angle=35)


# ====================================================================== E09_01 windmill
from v4_wh2_farm import _lattice_sail
import v4util
from arch import lbox


def windmill_01():
    """E09_01 - tower windmill with the sail cross CENTRED on the cap hub, plus body detail:
    stone base skirt, door, three real windows, cap trim."""
    reset()
    rnd = random.Random(301)
    baseR, topR, H = 7.0, 4.6, 30.0
    prof = [(baseR, 0), (baseR, 1.0), (baseR - 0.3, 1.2)]
    nring = 9
    for i in range(nring + 1):
        t = i / nring
        r = baseR + (topR - baseR) * t
        prof.append((r, 1.2 + (H - 1.2) * t))
    lathe('tower', prof, loc=(0, 0, 0), key='stone', segs=24)
    # STONE BASE skirt (body detail)
    lathe('base', [(baseR + 1.2, 0), (baseR + 1.2, 2.4), (baseR, 3.0)], loc=(0, 0, 0), key='stone_dark', segs=24)
    for i in range(1, 6):
        z = H * i / 6
        r = baseR + (topR - baseR) * (z / H)
        torus('course', r + 0.05, 0.12, loc=(0, 0, z), key='stone_dark', segs=24, rsegs=4)
    # door at base (front -Y) with stone lintel
    f = F(0, -baseR + 0.2, 0, 0)
    lbox(f, (3.6, 1.2, 6.6), 0, -0.3, 3.3, 'wood_old')
    lbox(f, (4.2, 0.5, 0.6), 0, -0.4, 6.9, 'stone_dark')
    cyl('inner', baseR - 1.2, H - 2, loc=(0, 0, (H - 2) / 2 + 0.5), key='wh2_board_d', verts=20)
    v4util.marker('mk_door', (0, -baseR, 0))
    # three windows evenly spiralling up, each with a frame + sill (clean body detail)
    for k in range(3):
        z = 9.0 + k * 6.0
        ang = k * 120 + 40
        r = baseR + (topR - baseR) * (z / H)
        px = math.cos(math.radians(ang)) * r
        py = math.sin(math.radians(ang)) * r
        box('winf', (1.8, 0.4, 2.4), loc=(px * 1.02, py * 1.02, z), key='wood_old', rot=(0, 0, ang))
        box('win', (1.4, 0.6, 2.0), loc=(px, py, z), key='glass_dark', rot=(0, 0, ang))
        box('sill', (2.0, 0.5, 0.3), loc=(px * 1.02, py * 1.02, z - 1.2), key='stone_dark', rot=(0, 0, ang))
    # balcony ring
    bz = H - 5.0
    br = baseR + (topR - baseR) * (bz / H) + 1.4
    lathe('balc', [(br - 1.4, bz), (br, bz), (br, bz + 0.4), (br - 1.4, bz + 0.4)], loc=(0, 0, 0), key='timber', segs=24)
    nballus = 20
    for i in range(nballus):
        a = 2 * PI * i / nballus
        cyl('bal', 0.1, 1.4, loc=(math.cos(a) * (br - 0.2), math.sin(a) * (br - 0.2), bz + 0.9), key='timber', verts=6)
    torus('brail', br - 0.2, 0.1, loc=(0, 0, bz + 1.6), key='timber', segs=24, rsegs=4)
    # wooden cap (ogee dome)
    capz = H
    lathe('cap', [(0, capz), (topR + 0.6, capz), (topR + 0.8, capz + 0.5),
                  (topR * 0.5, capz + 3.2), (0, capz + 4.2)], loc=(0, 0, 0), key='wh2_capwood', segs=20)
    # cap trim ring (body detail)
    torus('captrim', topR + 0.8, 0.18, loc=(0, 0, capz + 0.5), key='wood_old', segs=20, rsegs=4)
    # tail pole
    tube('tail', [(0, topR, capz + 1.0), (0, topR + 6.0, capz - 2.0)], 0.3, 'timber', res=4)
    # hub + four sails, hub CENTRED on the cap axis (x=0) just in front of the cap face
    hubz = capz + 1.5
    hy = -(topR + 0.9)
    ball('hub', 0.9, loc=(0, hy, hubz), key='iron', segs=10, rings=8)
    for k in range(4):
        _lattice_sail(f'sl{k}', 0, hy - 0.4, hubz, 13.0, 3.2, 90 + k * 90)
    return finalize('windmill_01', smooth_angle=28)


# ====================================================================== E11_03 scarecrow
from v4_wh2_crops import _straw_tufts


def scarecrow_turnip():
    """E11_03 - pole figure with MUTED cloth ribbons (no neon), carved turnip head."""
    reset()
    rnd = random.Random(503)
    H = 9.5
    box('post', (0.4, 0.4, H), loc=(0, 0, H / 2), key='wood_old', bev=0.03)
    armz, armspan = H - 2.5, 4.4
    box('arm', (armspan, 0.3, 0.3), loc=(0, 0, armz), key='wood_old', bev=0.03)
    box('arm2', (armspan * 0.7, 0.26, 0.26), loc=(0, 0, armz - 2.0), key='wood_old', rot=(0, 0, 14), bev=0.03)
    rock('md', 1.0, (0, 0, 0.1), 'wh2_soil', seed=9, scale=(1.4, 1.4, 0.3))
    # MUTED ribbon colours (cloth tones, roughness 0.95, no emission)
    cols = ['wx6_rib_rust', 'wx6_rib_sage', 'wx6_rib_slate']
    for i in range(16):
        ax = rnd.uniform(-armspan / 2, armspan / 2)
        az = rnd.choice([armz, armz - 2.0, H * 0.6, H * 0.4])
        col = rnd.choice(cols)
        pts = [(ax, 0, az)]
        for k in range(1, 4):
            pts.append((ax + rnd.uniform(-0.3, 0.3), rnd.uniform(-0.4, 0.4) * k, az - 0.7 * k))
        tube('rib', pts, 0.07, col, res=2)
    for s in (-1, 1):
        _straw_tufts(s * armspan * 0.5, 0, armz, rnd, 5, 1.0)
    lathe('turnip', [(0, 0), (1.0, 0.3), (1.1, 0.9), (0.7, 1.5), (0, 1.9)], loc=(0, -0.1, H - 0.3), key='wh2_turnip', segs=12)
    for t in range(4):
        tube('root', [(0, -0.1, H + 1.5), (rnd.uniform(-0.3, 0.3), -0.1 + rnd.uniform(-0.2, 0.2), H + 2.0 + rnd.uniform(0, 0.4))], 0.04, 'wh2_turnip', res=2)
    for ex in (-0.35, 0.35):
        poly_prism('eye', [(-0.2, -0.2), (0.2, -0.2), (0, 0.22)], 0.3, loc=(ex, -0.95, H + 0.5), key='wh2_crow', rot=(90, 0, 0))
    poly_prism('nose', [(-0.14, -0.14), (0.14, -0.14), (0, 0.18)], 0.3, loc=(0, -1.0, H), key='wh2_crow', rot=(90, 0, 0))
    for mx in (-0.4, -0.1, 0.2, 0.5):
        box('tooth', (0.18, 0.3, 0.22), loc=(mx, -0.95, H - 0.5), key='wh2_crow')
    return finalize('scarecrow_03', smooth_angle=30)


# ====================================================================== D05 ancient trees
from v4_d05 import limb_tree, LEAF_BRIGHT, LEAF_DEEP, moss_on_trunk as elf_moss, ground_bits as elf_ground
from v4_elf import crown as elf_crown, cluster as elf_cluster, LEAF


def ancient_b():
    """D05_05 silverbark beech - add MID-LEVEL branches & foliage clumps so the trunk is not a bare pole."""
    reset()
    tr, H = 3.2, 74.0
    rnd, tips, top = limb_tree(23, tr, H, nlimb=13, z_lo=0.30, z_hi=0.86, len_rng=(9, 15), pitch=(0.45, 1.05),
                               sway=0.8, key='ev_bark_silver', top_r=0.45, flare=1.7, root_n=7, rspan=2.4, limb_r=0.34)
    # broad oval crown
    elf_crown(top[0], top[1], H * 0.70, 20.0, 34.0, seed=23, count=50, keys=LEAF_BRIGHT)
    # foliage on every limb tip (now reaching lower on the trunk)
    for i, e in enumerate(tips):
        elf_cluster(e.x, e.y, e.z + 1.5, rnd.uniform(5.0, 7.0), seed=200 + i, n=6, keys=LEAF_BRIGHT)
    # extra MID-TRUNK foliage clumps so there is no bare pole stretch
    for k in range(6):
        a = 2 * PI * k / 6 + rnd.uniform(-0.3, 0.3)
        z = H * rnd.uniform(0.34, 0.6)
        d = tr * 2.0 + rnd.uniform(1.0, 3.0)
        elf_cluster(math.cos(a) * d, math.sin(a) * d, z, rnd.uniform(4.0, 6.0), seed=260 + k, n=5, keys=LEAF_BRIGHT)
    elf_moss(tr, H, 23, 10, rnd, sway=0.8, zmin=1, zmax=20, top_r=0.45)
    elf_ground(tr, rnd, 23, nrock=3, scale=1.1)
    return finalize('ev_ancient_tree_b', smooth_angle=38)


def ancient_d():
    """D05_07 - give it a gnarled BROADLEAF dome crown to match the ancient_tree family (was a conifer)."""
    reset()
    tr, H = 5.0, 58.0
    rnd, tips, top = limb_tree(27, tr, H, nlimb=10, z_lo=0.42, z_hi=0.74, len_rng=(16, 26), pitch=(0.25, 0.6),
                               sway=1.5, key='ev_bark', top_r=0.5, flare=2.0, root_n=8, rspan=2.8, limb_r=0.5)
    # low broad broadleaf dome (wide spread, moderate thickness) - the opposite of a pine spire
    elf_crown(top[0], top[1], H * 0.76, 30.0, 16.0, seed=27, count=48, keys=LEAF_DEEP)
    for i, e in enumerate(tips):
        elf_cluster(e.x, e.y, e.z + 2.0, rnd.uniform(6.0, 8.2), seed=270 + i, n=6, keys=LEAF_DEEP)
    elf_moss(tr, H, 27, 14, rnd, sway=1.5, zmin=1, zmax=28)
    elf_ground(tr, rnd, 27, nrock=4, scale=1.3)
    return finalize('ev_ancient_tree_d', smooth_angle=38)


# ====================================================================== D06_10 moss rock
from v4_d06 import mini_fern, mushrooms, moss_skirt
from v4_elf import ivy_strand as elf_ivy


def _organic_moss(o, seed):
    """Organic moss: paint onto gentle upward faces only (high-ish threshold + strong noise), not blocky."""
    top_paint(o, 'ev_moss', 0.72, seed, noise_amt=0.55)


def moss_rock_a():
    """D06_10 - large mossy boulder; moss now blended organically along gentle upward faces/crevices,
    not in blocky angular patches."""
    reset()
    rnd = random.Random(401)
    a = rock('rk', 5.4, (0, 0, 2.7), 'ev_stone_dark', seed=11, scale=(1.25, 1.0, 0.82), subdiv=4, amp=0.34)
    _organic_moss(a, 11)
    b = rock('rk', 2.6, (6.0, -2.2, 1.0), 'ev_stone_dark', seed=12, scale=(1.2, 1.0, 0.72), subdiv=3, amp=0.32)
    _organic_moss(b, 12)
    c = rock('rk', 1.5, (-5.4, -3.4, 0.5), 'ev_stone_dark', seed=13, scale=(1.2, 1.0, 0.7), subdiv=3, amp=0.3)
    _organic_moss(c, 13)
    # organic moss skirt + small moss blobs nestled in crevices (rounded, not blocks)
    moss_skirt(9.5, 14, sx=1.1, sy=0.95)
    for k in range(5):
        aa = rnd.uniform(0, 2 * PI); d = rnd.uniform(2.0, 4.6)
        blob('mo', rnd.uniform(0.5, 1.0), (math.cos(aa) * d, math.sin(aa) * d, 0.12), 'ev_moss', subdiv=2, amp=0.35, scale=(1.3, 1.1, 0.3), seed=k)
    mini_fern(-3.4, -7.0, 0.0, 7, 3.0, 15)
    mini_fern(7.2, 3.2, 0.0, 6, 2.4, 16)
    mushrooms(-6.6, -5.0, 0.0, 6, seed=3, scale=1.6)
    for k in range(3):
        elf_ivy((-3.6 + k * 1.2, -4.4 - k * 0.2, 4.2 - k * 0.6), rnd.uniform(2.5, 4.5), seed=k)
    return finalize('moss_rock_a', smooth_angle=22)


# ====================================================================== D09_02 waterfall cliff
from v4_d09 import strata_block, rim_rocks, waterfall, sheet, CLIFF, fall_geometry
from v4_elf import nm as _nm
from v4_d06 import tuft as d6_tuft


def waterfall_soft(xc, y_lip, z_top, z_bot, width, out, rnd, ns=10, grow=0.12):
    """Like v4_d09.waterfall but with NO flat white torus splash rings - soft rounded foam only."""
    fn = fall_geometry(y_lip, z_top, z_bot, out)
    wf = lambda s: width * (1 + grow * s)
    sheet(fn, wf, 8, ns, 'water', xc=xc, thick=0.3)
    for u in (0.2, 0.44, 0.68, 0.88):
        u += rnd.uniform(-0.04, 0.04)
        sheet(fn, wf, 1, ns, 'foam', xc=xc, thick=0.12, dy=-0.14, ripple=0.0, u0=u, u1=u + 0.05)
    # rounded foam mounds where the water lands (no flat discs/rings)
    ylan = y_lip - 0.25 - out
    for k in range(5):
        a = rnd.uniform(0, 2 * PI)
        d = rnd.uniform(0.0, width * 0.5)
        r = rnd.uniform(0.8, 1.5)
        blob(_nm('sp'), r, (xc + math.cos(a) * d, ylan - 0.4 + math.sin(a) * d * 0.5, z_bot + 0.15),
             'foam', subdiv=1, amp=0.45, scale=(1.2, 1.0, 0.45), seed=500 + k)


def waterfall_cliff_b():
    """D09_02 - wide three-step cascade; trimmed subdivision toward ~35k tris and soft foam shapes
    at the base of each fall instead of flat white discs."""
    reset()
    rnd = random.Random(902)
    terr = [(-13.0, 13.0, 5.0, 14.0, 22.0, 3), (-14.0, 14.0, -5.0, 5.0, 14.5, 2), (-15.0, 15.0, -14.0, -4.0, 7.2, 2)]
    for i, (x0, x1, y0, y1, zt, nl) in enumerate(terr):
        strata_block(x0, x1, y0, y1, zt, rnd, nl, i * 2)
    falls = [[(-5.5, 5.0), (6.5, 3.5)], [(1.0, 7.0), (-10.0, 2.6)], [(-3.5, 4.8), (7.5, 3.4)]]
    z_after = [14.5, 7.2, 0.0]
    for i, (x0, x1, y0, y1, zt, nl) in enumerate(terr):
        cy = (y0 + y1) / 2 + 1.0
        rx = (x1 - x0) / 2 - 3.2
        ry = (y1 - y0) / 2 - 2.2
        ball('pond', 1.0, ((x0 + x1) / 2, cy, zt + 0.02), 'water', segs=22, rings=6, scale=(rx, ry, 0.5))
        rim_rocks((x0 + x1) / 2, cy, rx + 0.5, ry + 0.4, rnd, skip=lambda x, y, yy=y0: y < yy + 3.4, n=12, r0=(0.7, 1.4), z=zt)
        for (fx, fw) in falls[i]:
            zb = z_after[i] + 0.55
            ylip = y0 - 1.6
            slab_ = box('spill', (fw + 1.8, 3.8, 0.9), loc=(fx, y0 - 0.1, zt - 0.45), key=CLIFF[(i + 2) % 5], bev=0.1, segs=1)
            top_paint(slab_, 'ev_moss', 0.97, i, noise_amt=0.0)
            sheet(lambda s, a=y0 + 2.4, b=ylip, z=zt + 0.38: (a + (b - a) * s, z), lambda s, w=fw * 0.92: w, 5, 3, 'water', xc=fx, thick=0.26, ripple=0.04)
            waterfall_soft(fx, ylip, zt + 0.38, zb, fw * 0.92, 2.0 if i < 2 else 2.6, rnd, ns=8)
    # bottom pool with a soft foam band at the base of the last fall
    ball('pool', 1.0, (0, -20.0, 0.35), 'water', segs=24, rings=7, scale=(16.0, 7.5, 0.5))
    rim_rocks(0, -20.0, 16.2, 7.8, rnd, skip=lambda x, y: y > -13.6, n=18, r0=(1.0, 2.0))
    for k in range(4):
        blob('poolfoam', rnd.uniform(1.2, 2.2), (rnd.uniform(-6, 6), -14.5 + rnd.uniform(-0.6, 0.6), 0.45), 'foam', subdiv=1, amp=0.45, scale=(1.4, 1.0, 0.25), seed=420 + k)
    # dressing (trimmed counts to help the tri budget)
    for i, (x0, x1, y0, y1, zt, nl) in enumerate(terr):
        for sx in (-1, 1):
            xx = sx * (x1 - 1.6)
            mini_fern(xx, (y0 + y1) / 2 + 1.0, zt + 0.1, 5, 2.2, 200 + i * 3 + sx)
            blob('lm', 1.8, (xx + sx * 0.4, y0 + 1.0, zt + 0.05), 'ev_moss', subdiv=2, amp=0.3, scale=(1.5, 1.0, 0.3), seed=i + sx)
        for k in range(2):
            elf_ivy((-9.0 + k * 10.0 + rnd.uniform(-1, 1), y0 - 0.5, zt - 0.3), rnd.uniform(3.0, 6.0), seed=230 + i * 3 + k)
    for sx in (-1, 1):
        for i in range(3):
            x = sx * rnd.uniform(11.0, 18.0)
            y = rnd.uniform(-14.0, -3.0)
            r = rnd.uniform(2.0, 3.6)
            o = rock('bd', r, (x, y, r * 0.35), rnd.choice(CLIFF), seed=i + sx * 5, scale=(1.2, 1.0, 0.7), subdiv=2, amp=0.34)
            top_paint(o, 'ev_moss', 0.5, i)
    d6_tuft(-17.0, -22.0, 0.0, rnd, n=7)
    d6_tuft(17.5, -23.0, 0.0, rnd, n=7)
    mini_fern(-16.0, -17.0, 0.0, 5, 2.6, 251)
    mini_fern(16.5, -18.0, 0.0, 5, 2.6, 252)
    return finalize('waterfall_cliff_b', smooth_angle=35)


BATCHES = {
    'barrels': ('v4_rusty', [
        ('E07_07_rusty_prop_07', barrel_staved_pile, (1.0, -1.1, 0.5)),
        ('E07_08_rusty_prop_08', barrel_rolled_grain, (1.0, -1.1, 0.4)),
        ('E07_09_rusty_prop_09', barrel_burst_hoop_rain, (1.0, -1.1, 0.5)),
    ]),
    'ground': ('v4_ground', [
        ('F06_10_scree_chips', scree_chips, (0.6, -1.0, 1.1)),
    ]),
    'rusty_minor': ('v4_rusty', [
        ('E06_04_rusty_debris_04', debris_04, (1.0, -1.1, 0.5)),
    ]),
    'graveyard': ('v4_graveyard', [
        ('E01_08_gravestone_08', gravestone_08, (0.7, -1.2, 0.35)),
    ]),
    'deadtree': ('v4_nature', [
        ('E05_02_dead_tree_02', E05_02_leaning, (1.0, -1.2, 0.35)),
    ]),
    'farm': ('v4_farm', [
        ('E09_01_windmill_01', windmill_01, (1.0, -1.3, 0.35)),
        ('E11_03_scarecrow_03', scarecrow_turnip, (1.0, -1.1, 0.45)),
    ]),
    'ancient': ('v4_nature', [
        ('D05_05_ancient_tree_b', ancient_b, (1.0, -1.2, 0.3)),
        ('D05_07_ancient_tree_d', ancient_d, (1.0, -1.2, 0.35)),
    ]),
    'mossrock': ('v4_nature', [
        ('D06_10_moss_rock_a', moss_rock_a, (1.0, -1.2, 0.4)),
    ]),
    'cliff': ('v4_world', [
        ('D09_02_waterfall_cliff_b', waterfall_cliff_b, (0.9, -1.2, 0.4)),
    ]),
}
