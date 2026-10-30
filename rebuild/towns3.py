"""Phase 1 town layouts v3. Writes mapplan/v3_<area>.json, rebuild/streets.json, rebuild/reserved.json, rebuild/parts_plan.json."""
import json, math
from layout_lib import Plan, Polyline, obb, norm, face_rot, catmull, CAT
import world as W

OUTDIR = r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan'
ALL_STREETS = []
RESERVED = {}          # part-built enterable buildings: name -> [cx, cz, half_len, half_wid, rot, y]
PARTS = {'huts': [], 'igloos': [], 'shanties': [], 'fishing_holes': []}   # part-built small structures

HOUSES_CAP = ['C05_townhouse_1', 'C06_townhouse_2', 'C07_townhouse_3', 'C08_townhouse_4', 'C09_corner_house', 'C10_terrace_row']
SHOPS_CAP = ['C12_bakery', 'C13_potion_shop', 'C14_magic_tool_shop']
TREES = ['A24_oak_1', 'A25_oak_2', 'A26_oak_3', 'A27_birch_1', 'A28_birch_2', 'A32_maple_autumn', 'A34_fruit_tree']
BUSHES = ['A38_bush_1', 'A39_bush_2', 'A40_bush_3']
FLOWERS = ['A43_flowers_red', 'A44_flowers_yellow', 'A45_flowers_purple', 'A46_flowers_white', 'A47_flowers_blue']
CRATES = ['A71_barrel', 'A72_barrel_open', 'A73_crate_small', 'A74_crate_large', 'A75_crate_stack', 'A76_sack', 'A77_sack_pile']


def pad(name):
    return [q for q in W.PADS if q['name'] == name][0]


def in_pad(name, need=0.97):
    p = pad(name)
    return lambda x, z: W.pad_mask(p, x, z) >= need


def reserve(P, name, cx, cz, half_l, half_w, rot, y=None, margin=3):
    y = W.ground_no_noise(cx, cz) if y is None else y
    RESERVED[name] = [round(cx, 1), round(cz, 1), half_l, half_w, round(rot % 360, 1), round(y, 2)]
    P.blocks.append(obb(cx, cz, half_w + margin, half_l + margin, rot))


def yard(P, inside, bbox, group, n_trees, n_bush, n_flower, extra=None):
    P.scatter(inside, TREES, n_trees, group, min_gap=4, scale=(0.75, 1.1), bbox=bbox)
    P.scatter(inside, BUSHES, n_bush, group, min_gap=1.5, scale=(0.8, 1.3), bbox=bbox)
    P.scatter(inside, FLOWERS, n_flower, group, min_gap=1.0, scale=(0.9, 1.3), bbox=bbox)
    for models, n in (extra or []):
        P.scatter(inside, models, n, group, min_gap=2.5, scale=None, bbox=bbox)


# =================================================================== CAPITAL (70%)
def capital():
    P = Plan('v3_capital', seed=111)
    inside = in_pad('capital_city')
    ZS, ZN, XE = -1237.0, -1918.0, 490.0
    P.put('C04_grand_gate', 0, ZS, 0, 'Walls', check=False)
    P.put('C04_grand_gate', 0, ZN, 180, 'Walls', check=False)
    towers_x = [170, 330]
    towers_z = [-1410, -1580, -1750]
    for sx in (-1, 1):
        P.put('C02_city_wall_corner', sx * XE, ZS, 0, 'Walls', check=False)
        P.put('C02_city_wall_corner', sx * XE, ZN, 0, 'Walls', check=False)
        for tx in towers_x:
            P.put('C03_city_wall_tower', sx * tx, ZS, 0, 'Walls', check=False)
            P.put('C03_city_wall_tower', sx * tx, ZN, 180, 'Walls', check=False)
        for tz in towers_z:
            P.put('C03_city_wall_tower', sx * XE, tz, 90 if sx > 0 else 270, 'Walls', check=False)
    nodes = [26] + sum([[t - 11, t + 11] for t in towers_x], []) + [XE - 15.5]
    for sx in (-1, 1):
        for i in range(0, len(nodes) - 1, 2):
            a, b = nodes[i], nodes[i + 1]
            p0, p1 = (min(sx * a, sx * b), ZS), (max(sx * a, sx * b), ZS)
            P.line_of('C01_city_wall_straight', p0, p1, 'Walls')
            P.line_of('C01_city_wall_straight', (p1[0], ZN), (p0[0], ZN), 'Walls')
        zn = [ZS - 15.5] + sum([[t + 11, t - 11] for t in towers_z], []) + [ZN + 15.5]
        for i in range(0, len(zn) - 1, 2):
            a, b = zn[i], zn[i + 1]
            if sx > 0:
                P.line_of('C01_city_wall_straight', (XE, a), (XE, b), 'Walls')
            else:
                P.line_of('C01_city_wall_straight', (-XE, b), (-XE, a), 'Walls')
    for sx in (-1, 1):
        P.put('A21_brazier', sx * 34, ZS + 16, 0, 'GateSquare', block=False, streets=False)
        P.put('A95_flag_pole', sx * 46, ZS - 22, 0, 'GateSquare', block=False, streets=False)
        P.put('A21_brazier', sx * 34, ZN - 16, 180, 'Walls', block=False, streets=False)
    av = P.street([(0, -1222), (0, ZN + 8)], 12, 'Pavement', smooth=False, step=40)
    ramp = [(0, -1928, 59.5), (55, -1940, 62.0), (128, -1958, 68.0), (146, -1980, 74.5), (90, -1996, 82.0), (22, -2006, 89.5), (0, -2006, 92.0)]
    P.street([(p[0], p[1]) for p in ramp], 7, 'Cobblestone', smooth=False, y=[p[2] for p in ramp], bank=28)
    cross_z = [-1376, -1544, -1712, -1838]
    cross = {z: P.street([(-470, z), (470, z)], 6.5, 'Cobblestone', smooth=False, step=40) for z in cross_z}
    ns = {x: P.street([(x, -1262), (x, -1893)], 6.5, 'Cobblestone', smooth=False, step=40) for x in (-238, 238)}
    ring = [P.street([(x, -1262), (x, -1893)], 5.5, 'Cobblestone', smooth=False, step=40) for x in (-462, 462)]
    ring.append(P.street([(-470, -1262), (470, -1262)], 5.5, 'Cobblestone', smooth=False, step=40))
    ring.append(P.street([(-470, -1893), (470, -1893)], 5.5, 'Cobblestone', smooth=False, step=40))
    plazas = [(0, -1280, 56, 26), (0, -1460, 88, 54), (0, -1628, 94, 48), (0, -1776, 48, 34)]
    for (cx, cz, rx, rz) in plazas:
        P.plaza(cx, cz, rx, rz, 'Pavement')
        P.sblocks.append(obb(cx, cz, rx, rz, 0))
    P.put('C22_knight_statue', 0, -1284, 0, 'GateSquare', check=False)
    P.put('C21_plaza_fountain', 0, -1460, 0, 'MarketSquare', check=False)
    P.put('C23_obelisk', 0, -1628, 0, 'CathedralSquare', check=False)
    P.put('K44_monument_column', 0, -1776, 0, 'UpperPlaza', check=False)
    reserve(P, 'capital_cathedral', -186, -1628, 82, 36, 90)
    P.put('C19_royal_library', 132, -1628, 270, 'CathedralSquare', check=False)
    P.put('C15_clock_tower', 108, -1688, 270, 'CathedralSquare', check=False)
    P.put('C11_market_hall', 116, -1460, 270, 'MarketSquare', check=False)
    P.put('C18_guild_hall', -112, -1460, 90, 'MarketSquare', check=False)
    P.put('C20_magic_academy', 58, -1808, 270, 'UpperAvenue', check=False)
    P.put('C17_knights_hq', -64, -1808, 90, 'UpperAvenue', check=False)
    stalls = ['A105_market_stall_fruit', 'A106_market_stall_cloth', 'A107_market_stall_potion']
    for k, ang in enumerate(range(0, 360, 45)):
        a = math.radians(ang)
        P.put(stalls[k % 3], 48 * math.cos(a), -1460 + 32 * math.sin(a), face_rot(-math.cos(a), -math.sin(a)), 'MarketSquare', block=False, pad=0.5, streets=False)
    for (x, z) in ((-66, -1430), (66, -1490), (-46, -1500), (70, -1425)):
        P.put('C26_vendor_cart', x, z, P.rng.uniform(0, 360), 'MarketSquare', block=False, streets=False)
        P.cluster(x + 7, z + 4, CRATES, 'MarketSquare', n=4, radius=5)
    for z in (-1408, -1512):
        P.put('C31_bunting', 0, z, 0, 'MarketSquare', block=False, check=False, yo=16)
    for (cx, cz, rx, rz) in plazas:
        for ang in range(20, 360, 45):
            a = math.radians(ang)
            P.put('A15_lamp_iron_city', cx + (rx - 4) * math.cos(a), cz + (rz - 4) * math.sin(a), 0, 'Lamps', block=False, pad=0.2, streets=False)
        for ang in (45, 135, 225, 315):
            a = math.radians(ang)
            P.put('A83_bench_stone', cx + rx * 0.55 * math.cos(a), cz + rz * 0.55 * math.sin(a), face_rot(-math.cos(a), -math.sin(a)), 'Plazas', block=False, pad=0.5, streets=False)
    wts = {m: 1.0 for m in HOUSES_CAP}; wts['C10_terrace_row'] = 0.6; wts['C09_corner_house'] = 0.5
    shopw = dict(wts); shopw.update({m: 1.2 for m in SHOPS_CAP})
    allh = HOUSES_CAP + SHOPS_CAP
    for side in (1, -1):
        P.frontage(av, side, allh, 'Avenue', 12, setback=4, gap=(1.5, 3.5), weights=shopw)
    for z, ln in cross.items():
        for side in (1, -1):
            P.frontage(ln, side, allh, f'Street_{-z}', 6.5, setback=3, gap=(2, 4), weights=shopw if z in (-1376, -1544) else wts)
    for x, ln in ns.items():
        for side in (1, -1):
            P.frontage(ln, side, HOUSES_CAP, f'Lane_{x}', 6.5, setback=3, gap=(2, 4.5), weights=wts)
    noble = ['K37_mansion_1', 'K38_mansion_2', 'K39_mansion_3']
    for sx in (-1, 1):
        for i, x in enumerate((140, 330)):
            P.put(noble[(i + (sx > 0)) % 3], sx * x, -1866, 0, 'NobleQuarter', pad=1.5)
    for side in (1, -1):
        for ln in ring:
            P.frontage(ln, side, HOUSES_CAP, 'OuterRing', 5.5, setback=3, gap=(3, 8), weights=wts, max_items=40)
    for side in (1, -1):
        P.lamps(av, 'A16_lamp_iron_double', 'Lamps', 12, spacing=32, offset=1.6, s0=30, alternate=False, side=side)
    for ln in list(cross.values()) + list(ns.values()):
        P.lamps(ln, 'A15_lamp_iron_city', 'Lamps', 6.5, spacing=40, offset=1.4, s0=20)
    for ln in ring:
        P.lamps(ln, 'A15_lamp_iron_city', 'Lamps', 5.5, spacing=52, offset=1.3, s0=25)
    yard(P, inside, (-480, 480, -1908, -1250), 'Gardens', 120, 180, 140,
         [(['A98_well', 'A92_laundry_line', 'A82_bench_wood', 'A97_water_trough'], 22), (CRATES, 36), (['A48_planter_box', 'A109_fountain_small'], 18)])
    castle(P)
    P.save(f'{OUTDIR}\\v3_capital.json')
    ALL_STREETS.extend(P.streets)
    return P


def castle(P):
    CZ0 = -2018.0
    XW, ZB = 200.0, -2350.0
    P.put('K08_gatehouse', 0, CZ0, 0, 'Castle', check=False)
    for sx in (-1, 1):
        P.put('K06_curtain_wall_corner', sx * XW, CZ0, 0, 'Castle', check=False)
        P.put('K06_curtain_wall_corner', sx * XW, ZB, 0, 'Castle', check=False)
        P.put('K02_castle_round_tower', sx * XW, (CZ0 + ZB) / 2, 0, 'Castle', check=False)
        P.put('K03_castle_square_tower', sx * 100, ZB, 0, 'Castle', check=False)
        P.put('K42_sentry_box', sx * 34, CZ0 + 16, 0, 'Castle', check=False)
        P.put('A21_brazier', sx * 30, CZ0 + 24, 0, 'Castle', block=False, check=False)
    mz = (CZ0 + ZB) / 2
    P.line_of('K05_curtain_wall_straight', (-XW + 16, CZ0), (-25, CZ0), 'Castle')
    P.line_of('K05_curtain_wall_straight', (25, CZ0), (XW - 16, CZ0), 'Castle')
    P.line_of('K05_curtain_wall_straight', (XW - 16, ZB), (110, ZB), 'Castle')
    P.line_of('K05_curtain_wall_straight', (90, ZB), (-90, ZB), 'Castle')
    P.line_of('K05_curtain_wall_straight', (-110, ZB), (-XW + 16, ZB), 'Castle')
    for (a, b) in ((CZ0 - 16, mz + 10), (mz - 10, ZB + 16)):
        P.line_of('K05_curtain_wall_straight', (XW, a), (XW, b), 'Castle')
        P.line_of('K05_curtain_wall_straight', (-XW, b), (-XW, a), 'Castle')
    P.put('K01_main_keep', 0, ZB + 75, 0, 'Castle', check=False)
    for sx in (-1, 1):
        P.put('K04_spire_tower', sx * 62, ZB + 50, 0, 'Castle', check=False)
    P.plaza(0, CZ0 - 122, 150, 95, 'Pavement')
    P.street([(0, CZ0 - 12), (0, ZB + 102)], 9, 'Pavement', smooth=False)
    P.put('K23_royal_fountain', 0, CZ0 - 122, 0, 'CastleCourt', check=False)
    P.put('K24_wizard_king_statue', 0, CZ0 - 192, 0, 'CastleCourt', check=False)
    P.put('K40_barracks', -150, CZ0 - 77, 90, 'CastleCourt', check=False)
    P.put('K41_stables', 150, CZ0 - 77, 270, 'CastleCourt', check=False)
    P.put('K43_royal_carriage', 118, CZ0 - 117, 0, 'CastleCourt', check=False)
    P.put('K30_gazebo', -125, ZB + 110, 90, 'RoyalGarden', check=False)
    for sx in (-1, 1):
        for dz in (-47, -87, -152, -202):
            P.put('K34_ornate_lamp', sx * 16, CZ0 + dz, 0, 'CastleCourt', block=False, check=False)
        for dz in (-62, -177):
            P.put('K35_royal_banner', sx * 40, CZ0 + dz, 90 if sx < 0 else 270, 'CastleCourt', block=False, check=False)
        for dz in (-162, -192, -222):
            P.put('K26_topiary_cone', sx * 34, CZ0 + dz, 0, 'RoyalGarden', block=False, check=False)
        P.put('K27_topiary_spiral', sx * 90, CZ0 - 192, 0, 'RoyalGarden', block=False, check=False)
        P.put('K33_ornate_bench', sx * 58, CZ0 - 132, 90 if sx < 0 else 270, 'RoyalGarden', block=False, check=False)
        P.put('K31_rose_arch', sx * 100, ZB + 90, 0, 'RoyalGarden', block=False, check=False)
        P.put('K32_ornate_planter', sx * 26, CZ0 - 32, 0, 'CastleCourt', block=False, check=False)
    garden = lambda x, z: abs(x) < 185 and ZB + 15 < z < CZ0 - 17
    P.scatter(garden, ['K25_topiary_ball', 'K26_topiary_cone', 'K32_ornate_planter'] + FLOWERS, 40, 'RoyalGarden', min_gap=2, scale=None, bbox=(-185, 185, ZB + 15, CZ0 - 17))


# =================================================================== RUSTY (70%, huts)
def rusty():
    P = Plan('v3_rusty', seed=123)
    pr = pad('rusty')
    inside = lambda x, z: W.pad_mask(pr, x, z) > 0.9
    main = P.street([(1032, 986), (1095, 1025), (1162, 1060), (1220, 1101), (1274, 1141), (1324, 1180)], 7, 'Ground', step=16)
    lane1 = P.street([(1214, 1110), (1190, 1165), (1162, 1225), (1140, 1270)], 5, 'Ground', step=16)
    lane2 = P.street([(1228, 1092), (1270, 1046), (1318, 1003), (1346, 975)], 5, 'Ground', step=16)
    P.plaza(1220, 1101, 32, 32, 'Ground')
    P.sblocks.append(obb(1220, 1101, 30, 30, 0))
    d = norm(1324 - 1274, 1180 - 1141)
    ccx, ccz = 1324 + d[0] * 104, 1180 + d[1] * 104
    rot = face_rot(-d[0], -d[1])
    reserve(P, 'rusty_church', ccx, ccz, 88, 42, rot, 14.0, margin=4)
    P.plaza(1310, 1170, 28, 28, 'Ground')
    P.put('D36_old_well_pump', 1220, 1101, 30, 'Square', check=False)
    P.put('D25_rundown_tavern', 1255, 1068, face_rot(-0.73, 0.68), 'Square')
    P.put('D28_rusty_water_tower', 1186, 1068, 0, 'Square')
    P.put('D26_blacksmith_shed', 1192, 1140, face_rot(0.6, -0.8), 'Square')
    P.put('A99_anvil', 1204, 1131, 20, 'Square', block=False, streets=False)
    P.put('A93_notice_board', 1240, 1082, face_rot(-0.6, 0.8), 'Square', block=False, streets=False)
    houses = ['D20_rundown_house_1', 'D21_rundown_house_2', 'D22_rundown_house_3', 'D23_rundown_house_4']
    for side in (1, -1):
        P.frontage(main, side, houses + ['D24_collapsed_ruin'], 'MainStreet', 7, setback=3, gap=(4, 10), weights={'D24_collapsed_ruin': 0.3})
    for ln in (main, lane1, lane2):
        P.lamps(ln, 'D37_crooked_lamp', 'Lamps', 6 if ln is main else 4, spacing=34, offset=1.3, s0=12)
    # huts along the lanes and in clusters (part-built later; reserve footprints here)
    def hut_row(line, side, group):
        s = 8
        while s < line.L - 8:
            (px, pz), dd = line.at(s)
            R = (-dd[1], dd[0])
            size = P.rng.choice([10, 11, 12, 13])
            off = 5 + 3 + size / 2
            cx, cz = px + R[0] * side * off, pz + R[1] * side * off
            rr = face_rot(-R[0] * side, -R[1] * side)
            box = obb(cx, cz, size / 2 + 1, size / 2 + 1, rr)
            if P.fits(box, 0.5, soft=True) and inside(cx, cz):
                P.blocks.append(box)
                PARTS['huts'].append({'x': round(cx, 1), 'z': round(cz, 1), 'rot': round(rr, 1), 'w': size, 'd': size + P.rng.choice([0, 2, 3]),
                                      'y': round(W.ground_no_noise(cx, cz), 2), 'v': P.rng.randint(1, 3)})
                s += size + P.rng.uniform(4, 9)
            else:
                s += 4
    for side in (1, -1):
        hut_row(lane1, side, 'Huts')
        hut_row(lane2, side, 'Huts')
    # hut clusters around campfires on the edges
    for (hx, hz) in ((1110, 1180), (1350, 1040), (1080, 1090), (1290, 990)):
        P.put('A22_campfire', hx, hz, 0, 'Camps', block=False)
        for k in range(5):
            a = math.radians(k * 72 + P.rng.uniform(-15, 15))
            rr = 20 + P.rng.uniform(-3, 4)
            cx, cz = hx + math.cos(a) * rr, hz + math.sin(a) * rr
            size = P.rng.choice([9, 10, 11])
            rot2 = face_rot(hx - cx, hz - cz)
            box = obb(cx, cz, size / 2 + 1, size / 2 + 1, rot2)
            if P.fits(box, 0.5, soft=True) and inside(cx, cz):
                P.blocks.append(box)
                PARTS['huts'].append({'x': round(cx, 1), 'z': round(cz, 1), 'rot': round(rot2, 1), 'w': size, 'd': size, 'y': round(W.ground_no_noise(cx, cz), 2), 'v': P.rng.randint(1, 3)})
        P.cluster(hx + 6, hz - 5, ['D32_broken_barrel', 'A90_firewood_stack', 'D31_rusted_cart', 'A76_sack'], 'Camps', n=4, radius=6)
    # graveyard beside the church
    nL = (d[1], -d[0])
    gcx, gcz = ccx + nL[0] * 95 - d[0] * 10, ccz + nL[1] * 95 - d[1] * 10
    graveyard(P, gcx, gcz, face_rot(-nL[0], -nL[1]), 46, 38, 'Graveyard', fence='D33_broken_fence', rows=5)
    P.put('D27_broken_windmill', 1300, 990, 230, 'Edges')
    junk = ['D30_scrap_pile', 'D31_rusted_cart', 'D32_broken_barrel', 'D35_collapsed_wall', 'A90_firewood_stack', 'A79_hand_cart', 'A78_hay_bale']
    bbox = (990, 1480, 885, 1325)
    P.scatter(inside, junk, 34, 'Clutter', min_gap=3, scale=None, bbox=bbox)
    P.scatter(inside, ['A35_dead_tree_1', 'A36_dead_tree_2', 'A68_stump_1', 'A69_stump_2'], 26, 'Clutter', min_gap=5, bbox=bbox)
    P.scatter(inside, ['A49_tall_grass_1', 'A50_tall_grass_2', 'A56_rock_small_1', 'A57_rock_small_2', 'A58_rock_medium_1'], 90, 'Clutter', min_gap=1, bbox=bbox)
    P.save(f'{OUTDIR}\\v3_rusty.json')
    ALL_STREETS.extend(P.streets)
    return P


def graveyard(P, gcx, gcz, grot, gw, gd, group, fence='A103_fence_iron', rows=6, mausoleums=1, density=0.85):
    t = math.radians(grot)
    ux, uz = (math.cos(t), -math.sin(t)), (math.sin(t), math.cos(t))
    def gpt(a, b):
        return (gcx + ux[0] * a + uz[0] * b, gcz + ux[1] * a + uz[1] * b)
    P.put('D18_graveyard_gate', *gpt(0, gd), grot, group, check=False)
    P.line_of('A103_fence_iron', gpt(-gw, gd), gpt(-8, gd), group, block=False)
    P.line_of('A103_fence_iron', gpt(8, gd), gpt(gw, gd), group, block=False)
    P.line_of(fence, gpt(gw, gd), gpt(gw, -gd), group, block=False)
    P.line_of(fence, gpt(gw, -gd), gpt(-gw, -gd), group, block=False)
    P.line_of('A103_fence_iron', gpt(-gw, -gd), gpt(-gw, gd), group, block=False)
    graves = ['D12_gravestone_1', 'D13_gravestone_2', 'D14_gravestone_3', 'D15_gravestone_4', 'D16_stone_cross']
    cols = int((gw - 6) / 6.2)
    for r in range(rows):
        for c in range(-cols, cols + 1):
            if abs(c) <= 1:
                continue
            if P.rng.random() < density:
                x, z = gpt(c * 6.2 + P.rng.uniform(-0.6, 0.6), gd - 10 - r * 9)
                P.put(P.rng.choice(graves), x, z, grot + P.rng.uniform(-8, 8), group, block=False, pad=0.1, check=False)
    for k in range(mausoleums):
        P.put('D17_mausoleum', *gpt(-gw * 0.6 + k * gw * 1.2, -gd + 14), grot, group, check=False)
    P.put('D19_weeping_statue', *gpt(0, -gd + 16), grot, group, check=False)
    for a, b in ((gw * 0.65, -gd * 0.7), (-gw * 0.85, gd * 0.2), (gw * 0.8, gd * 0.5)):
        P.put('A35_dead_tree_1' if a > 0 else 'A36_dead_tree_2', *gpt(a, b), P.rng.uniform(0, 360), group, block=False, check=False)
    for a in (-6, 6):
        P.put('A20_wall_torch', *gpt(a, gd + 1.5), grot, group, block=False, check=False, yo=7)
    P.blocks.append(obb(gcx, gcz, gw + 2, gd + 2, grot))


# =================================================================== HARBOUR (70%)
def harbour():
    P = Plan('v3_harbour', seed=137)
    hp = pad('harbour')
    inside = lambda x, z: W.pad_mask(hp, x, z) > 0.95 and z < 1786
    X = lambda x: -390 + (x + 600) * 0.7
    Z = lambda z: 1590 + (z - 2530) * 0.7
    main = P.street([(-390, 1392), (-390, 1798)], 8, 'Cobblestone', smooth=False, step=30)
    quay = P.street([(-625, 1808), (-155, 1808)], 10, 'Cobblestone', smooth=False, y=4.5, step=30)
    cross = [(z, P.street([(-640, z), (-140, z)], 6, 'Cobblestone', smooth=False, step=30)) for z in (1520, 1650)]
    lanes = [P.street([(x, 1470), (x, 1798)], 5, 'Cobblestone', smooth=False, step=30) for x in (-537, -243)]
    P.plaza(-390, 1597, 34, 28, 'Pavement')
    P.sblocks.append(obb(-390, 1597, 32, 26, 0))
    P.put('A109_fountain_small', -390, 1597, 0, 'Square', check=False)
    for ang in range(0, 360, 60):
        a = math.radians(ang)
        P.put('A82_bench_wood', -390 + 16 * math.cos(a), 1597 + 12 * math.sin(a), face_rot(-math.cos(a), -math.sin(a)), 'Square', block=False, streets=False)
    reserve(P, 'harbour_tavern', -428, 1764, 20, 15, 90)
    P.put('G14_harbour_master', -352, 1772, 270, 'Waterfront')
    for x in (-610, -570, -505, -465, -305, -265, -200, -160):
        P.put('G12_warehouse_1' if int(x) % 3 else 'G13_warehouse_2', x, 1780, 0, 'Waterfront', pad=1.0)
    P.line_of('G28_seawall', (-630, 1832), (-150, 1832), 'Waterfront', block=False)
    for it in P.items:
        if it['model'] == 'G28_seawall':
            it['y_offset'] = -8.5
    for px in (-530, -390, -250):
        for k in range(3):
            P.put('G01_pier_straight', px, 1850 + k * 24, 0, 'Piers', check=False, yo=-5.0)
        P.put('G03_pier_end', px, 1924, 0, 'Piers', check=False, yo=-5.0)
        for k in (0, 2):
            P.put('G31_mooring_bollard', px + 5, 1854 + k * 24, 90, 'Piers', block=False, check=False, yo=4.7)
    P.put('G06_galleon', -367, 1892, 90, 'Ships', check=False, yo=-7.0)
    P.put('G07_merchant_ship', -271, 1890, 270, 'Ships', check=False, yo=-6.0)
    P.put('G08_fishing_boat_1', -509, 1868, 90, 'Ships', check=False, yo=-2.5)
    P.put('G09_fishing_boat_2', -551, 1898, 270, 'Ships', check=False, yo=-2.5)
    for (x, z) in ((-460, 1850), (-320, 1855), (-180, 1848), (-600, 1850)):
        P.put('G10_rowboat', x, z, P.rng.uniform(0, 360), 'Ships', check=False, yo=-0.6)
    for (x, z) in ((-460, 1960), (-300, 1975), (-580, 1950), (-200, 1945)):
        P.put('G20_buoy', x, z, 0, 'Ships', check=False, yo=-2.0)
    P.put('G16_cargo_crane', -325, 1818, 180, 'Waterfront', check=False)
    P.put('G16_cargo_crane', -455, 1818, 180, 'Waterfront', check=False)
    for x in (-600, -560, -490, -300, -235, -190):
        P.put('G15_fish_market_stall' if int(x) % 2 else 'G17_net_rack', x, 1816, 0, 'Waterfront', block=False, streets=False)
    quayprops = ['G18_rope_coil', 'G19_anchor', 'G21_lobster_trap', 'G33_cargo_pallet', 'A71_barrel', 'A74_crate_large', 'A75_crate_stack']
    for x in range(-615, -160, 24):
        P.cluster(x + P.rng.uniform(-5, 5), 1822 + P.rng.uniform(-2, 2), quayprops, 'Waterfront', n=2, radius=3.5)
    for x in range(-620, -150, 52):
        P.put('A15_lamp_iron_city', x, 1826, 0, 'Lamps', block=False, streets=False)
    P.put('G11_lighthouse', -75, 1880, 200, 'Headlands', check=False)
    P.put('G23_harbour_fort', -700, 1870, 160, 'Headlands', check=False)
    for (x, z) in ((-715, 1905), (-685, 1910), (-728, 1890)):
        P.put('G22_cannon', x, z, 170, 'Headlands', block=False, check=False)
    houses = ['G24_harbour_house_1', 'G25_harbour_house_2', 'G26_harbour_house_3']
    for side in (1, -1):
        P.frontage(main, side, houses + ['G27_harbour_tavern'], 'MainStreet', 8, setback=3, gap=(1.5, 3.5), s0=8, s1=360, weights={'G27_harbour_tavern': 0.2})
        for z, ln in cross:
            P.frontage(ln, side, houses, f'Street_{z}', 6, setback=3, gap=(2, 4))
        for ln in lanes:
            P.frontage(ln, side, houses, 'Lanes', 5, setback=3, gap=(2, 5), s1=290)
    for ln in [main] + [c[1] for c in cross] + lanes:
        P.lamps(ln, 'A15_lamp_iron_city', 'Lamps', 6, spacing=38, offset=1.3, s0=14)
    yard(P, inside, (-690, -90, 1375, 1786), 'Gardens', 30, 60, 50,
         [(['A92_laundry_line', 'A98_well', 'A82_bench_wood', 'G17_net_rack'], 14), (CRATES, 24)])
    P.save(f'{OUTDIR}\\v3_harbour.json')
    ALL_STREETS.extend(P.streets)
    return P


# =================================================================== ELF (from scratch)
def elf():
    P = Plan('v3_elf', seed=151)
    ep = pad('elf')
    inside = lambda x, z: W.pad_mask(ep, x, z) > 0.55
    TX, TZ = -1560, -430
    P.put('F01_world_tree', TX, TZ, 90, 'WorldTree', check=False)
    P.blocks.append(obb(TX, TZ, 90, 90, 0))
    gate = P.street([(-1292, -404), (-1340, -408), (-1400, -414), (-1438, -420)], 4.5, 'Limestone', step=14)
    ring_pts = [(TX + 122 * math.cos(math.radians(a)), TZ + 122 * math.sin(math.radians(a))) for a in range(0, 361, 12)]
    ring = P.street(ring_pts, 3.5, 'Limestone', smooth=False)
    spokes = {
        'north': P.street([(TX, TZ - 124), (TX + 18, -640), (TX + 40, -700)], 4, 'Limestone', step=14),
        'south': P.street([(TX, TZ + 124), (TX - 14, -230), (TX, -150)], 4, 'Limestone', step=14),
        'west': P.street([(TX - 124, TZ), (-1760, -420), (-1840, -400)], 3.5, 'Limestone', step=14),
        'nw': P.street([(TX - 86, TZ - 86), (-1700, -560), (-1650, -600)], 3.5, 'Limestone', step=14),
        'se': P.street([(TX + 86, TZ + 86), (-1440, -260), (-1420, -230)], 3.5, 'Limestone', step=14),
        'sw': P.street([(TX - 86, TZ + 86), (-1720, -260), (-1780, -200)], 3.5, 'Limestone', step=14),
    }
    # palace by the lake (north), moon pool + shrine (south), houses
    P.put('F10_elf_palace', TX + 50, -735, 0, 'Palace', check=False)
    P.blocks.append(obb(TX + 50, -735, 30, 30, 0))
    for sx in (-1, 1):
        P.put('F13_elf_statue', TX + 50 + sx * 20, -700, 0, 'Palace', block=False, check=False)
        P.put('F28_elf_standing_lantern', TX + 40 + sx * 12, -690, 0, 'Palace', block=False, check=False)
    P.put('F11_moon_pool', TX, -150, 0, 'MoonPool', check=False)
    P.blocks.append(obb(TX, -150, 16, 16, 0))
    reserve(P, 'elf_temple', TX + 70, -170, 26, 26, 270)
    reserve(P, 'elf_house_1', -1730, -300, 15, 15, face_rot(TX - (-1730), TZ - (-300)))
    reserve(P, 'elf_house_2', -1390, -560, 15, 15, face_rot(TX - (-1390), TZ - (-560)))
    # treehouses in a ring around the tree
    ths = ['F02_treehouse_1', 'F03_treehouse_2', 'F04_treehouse_3', 'F05_treehouse_4']
    for k, ang in enumerate((200, 250, 300, 20, 70, 160)):
        a = math.radians(ang)
        x, z = TX + 230 * math.cos(a), TZ + 215 * math.sin(a)
        P.put(ths[k % 4], x, z, face_rot(TX - x, TZ - z), 'Treehouses', pad=3)
    P.put('F06_platform_ring', TX + 60, TZ - 96, 0, 'WorldTree', block=False, check=False, yo=24)
    P.put('F09_spiral_stair', TX + 92, TZ - 60, 0, 'WorldTree', check=False)
    P.put('F12_carved_arch', -1306, -405, 90, 'GatePath', check=False)
    P.put('F17_root_arch', -1390, -412, 90, 'GatePath', check=False)
    for (x, z) in ((-1330, -392), (-1330, -420), (-1420, -404), (-1420, -436)):
        P.put('F13_elf_statue', x, z, 90, 'GatePath', block=False)
    for k in range(4):
        a = math.radians(k * 90 + 45)
        P.put('F35_vine_pillar', TX + 140 * math.cos(a), TZ + 140 * math.sin(a), 0, 'WorldTree', block=False, check=False)
    paths = [gate] + list(spokes.values())
    for ln in paths:
        P.lamps(ln, 'F28_elf_standing_lantern', 'Lanterns', 4, spacing=24, offset=1.2, s0=8)
    for ln in paths + [ring]:
        for s in range(5, int(ln.L), 7):
            (px, pz), dd = ln.at(s)
            R = (-dd[1], dd[0])
            sd = 1 if (s // 7) % 2 else -1
            off = 5.5 + P.rng.uniform(0, 4)
            P.put(P.rng.choice(['F23_glow_mushroom_1', 'F24_glow_mushroom_2', 'F25_glow_flower_1', 'F26_glow_flower_2', 'A54_mushroom_cluster']),
                  px + R[0] * sd * off, pz + R[1] * sd * off, P.rng.uniform(0, 360), 'GlowPath', block=False, pad=0.2, scale=P.rng.uniform(0.8, 1.35))
    # lake: waterfall cliff from the NW mountain, lotus, rocks
    P.put('F32_waterfall_cliff', -1690, -712, 30, 'Lake', check=False)
    P.put('A110_waterfall_rocks', -1600, -690, 330, 'Lake', check=False)
    for k in range(10):
        a = P.rng.uniform(0, math.tau)
        P.put('F29_lotus', -1660 + 62 * math.cos(a) * P.rng.uniform(0.2, 0.9), -640 + 46 * math.sin(a) * P.rng.uniform(0.2, 0.9), P.rng.uniform(0, 360), 'Lake', block=False, check=False)
    for (x, z) in ((-1800, -505), (-1890, -444)):
        P.put('A66_stepping_stones', x, z, 30, 'River', block=False, check=False)
    for (x, z, r) in ((-1450, -700, 20), (-1830, -600, 0), (-1880, -260, 60), (-1300, -230, 200), (-1700, -130, 120)):
        P.put('F30_ruins_1' if x % 2 else 'F31_ruins_2', x, z, r, 'Ruins')
    for (x, z) in ((-1500, -310), (-1630, -300), (-1660, -540), (-1460, -545)):
        P.put('F33_elf_bench', x, z, face_rot(TX - x, TZ - z), 'WorldTree', block=False)
    for k in range(14):
        a = P.rng.uniform(0, math.tau); r = P.rng.uniform(150, 300)
        P.put('F34_crystal_cluster', TX + r * math.cos(a), TZ + r * math.sin(a), P.rng.uniform(0, 360), 'Crystals', block=False, scale=P.rng.uniform(0.8, 1.6))
    bbox = (-1900, -1220, -730, -70)
    far = lambda x, z: inside(x, z) and math.hypot(x - TX, z - TZ) > 160
    P.scatter(far, ['F14_jungle_tree_1', 'F15_jungle_tree_2'], 46, 'Jungle', min_gap=3, scale=(0.75, 1.1), bbox=bbox, block=True)
    P.scatter(far, ['F16_jungle_palm', 'A33_willow', 'A24_oak_1'], 70, 'Jungle', min_gap=2.5, scale=(0.8, 1.25), bbox=bbox, block=True,
              weights={'F16_jungle_palm': 3, 'A33_willow': 1.2, 'A24_oak_1': 0.8})
    P.scatter(inside, ['F21_giant_fern', 'F22_giant_leaf_plant', 'A51_fern', 'A38_bush_1', 'A39_bush_2'], 520, 'Undergrowth', min_gap=0.6, scale=(0.8, 1.35), bbox=bbox,
              weights={'F21_giant_fern': 3, 'F22_giant_leaf_plant': 3, 'A51_fern': 3, 'A38_bush_1': 1, 'A39_bush_2': 1})
    P.scatter(inside, ['F23_glow_mushroom_1', 'F24_glow_mushroom_2', 'A54_mushroom_cluster', 'F25_glow_flower_1', 'F26_glow_flower_2'], 240, 'Undergrowth', min_gap=0.4, scale=(0.8, 1.5), bbox=bbox)
    # hanging vines near big trees (raised)
    for it in [i for i in P.items if i['model'] in ('F14_jungle_tree_1', 'F15_jungle_tree_2')][:30]:
        for k in range(2):
            a = P.rng.uniform(0, math.tau)
            P.put(P.rng.choice(['F18_hanging_vines_1', 'F19_hanging_vines_2', 'F20_hanging_moss']), it['x'] + math.cos(a) * 14, it['z'] + math.sin(a) * 14,
                  P.rng.uniform(0, 360), 'Vines', block=False, check=False, yo=P.rng.uniform(18, 30))
    P.save(f'{OUTDIR}\\v3_elf.json')
    ALL_STREETS.extend(P.streets)
    return P


# =================================================================== ALPINE (bigger, igloos, ice lake camp)
def alpine():
    P = Plan('v3_alpine', seed=163)
    sp = pad('alpine_shelf')
    inside = lambda x, z: W.pad_mask(sp, x, z) > 0.97
    Y = 120.0
    main = P.street([(1585, -700), (1598, -760), (1618, -830), (1630, -872), (1606, -930), (1572, -962)], 6, 'Cobblestone', step=14, y=Y)
    east = P.street([(1640, -876), (1712, -862), (1780, -820), (1812, -790)], 5, 'Cobblestone', step=14, y=Y)
    west = P.street([(1620, -880), (1548, -890), (1480, -900), (1452, -930)], 5, 'Cobblestone', step=14, y=Y)
    south_lane = P.street([(1600, -780), (1530, -770), (1470, -790)], 4.5, 'Cobblestone', step=14, y=Y)
    P.plaza(1630, -872, 34, 30, 'Cobblestone', y=Y)
    P.sblocks.append(obb(1630, -872, 32, 28, 0))
    P.put('A98_well', 1630, -872, 0, 'Square', check=False)
    # winter market on the square
    for k, ang in enumerate(range(15, 360, 50)):
        a = math.radians(ang)
        P.put(['A105_market_stall_fruit', 'A106_market_stall_cloth', 'A107_market_stall_potion'][k % 3], 1630 + 25 * math.cos(a), -872 + 21 * math.sin(a),
              face_rot(-math.cos(a), -math.sin(a)), 'WinterMarket', block=False, pad=0.4, streets=False)
    P.put('C31_bunting', 1630, -872, 0, 'WinterMarket', block=False, check=False, yo=13)
    P.put('C31_bunting', 1630, -872, 90, 'WinterMarket', block=False, check=False, yo=13)
    reserve(P, 'alpine_lodge', 1585, -880, 22, 15, 90, Y)
    P.put('E06_stone_chapel', 1560, -985, 160, 'Chapel', check=False)
    P.put('E07_sawmill', 1785, -730, 200, 'Pond', pad=1.5)
    P.put('E08_barn', 1800, -900, 270, 'Farm', pad=1.5)
    P.put('E09_goat_pen', 1775, -935, 270, 'Farm', pad=1.0)
    P.put('E09_goat_pen', 1805, -955, 270, 'Farm', pad=1.0)
    P.put('E10_watchtower', 1845, -700, 230, 'Edge', check=False)
    P.put('E10_watchtower', 1440, -700, 140, 'Edge', check=False)
    chalets = ['E01_chalet_1', 'E02_chalet_2', 'E03_chalet_3', 'E04_chalet_4', 'E05_lodge']
    cw = {'E05_lodge': 0.35}
    for side in (1, -1):
        P.frontage(main, side, chalets, 'MainStreet', 6, setback=4, gap=(4, 8), weights=cw)
        P.frontage(east, side, chalets, 'EastLane', 5, setback=4, gap=(5, 9), weights=cw)
        P.frontage(west, side, chalets, 'WestLane', 5, setback=4, gap=(5, 9), weights=cw)
        P.frontage(south_lane, side, chalets, 'SouthLane', 4.5, setback=4, gap=(5, 9), weights=cw)
    for ln in (main, east, west, south_lane):
        P.lamps(ln, 'A17_lamp_wood_rustic', 'Lamps', 6, spacing=30, offset=1.3, s0=10)
    # igloos at the village edge (west) and an igloo camp on the ice-lake shore
    def igloo_ring(cx, cz, n, rr, base, group):
        P.put('A22_campfire', cx, cz, 0, group, block=False, check=False)
        for k in range(n):
            a = math.radians(k * 360 / n + P.rng.uniform(-10, 10))
            x, z = cx + math.cos(a) * rr, cz + math.sin(a) * rr
            dsz = P.rng.choice([14, 16, 18])
            box = obb(x, z, dsz / 2 + 1, dsz / 2 + 3, face_rot(cx - x, cz - z))
            if P.fits(box, 0.5, soft=True):
                P.blocks.append(box)
                PARTS['igloos'].append({'x': round(x, 1), 'z': round(z, 1), 'rot': round(face_rot(cx - x, cz - z), 1), 'd': dsz, 'y': base})
        P.cluster(cx + 5, cz + 5, ['E22_sled', 'A87_bucket', 'A90_firewood_stack', 'A74_crate_large'], group, n=4, radius=7)
    igloo_ring(1478, -820, 5, 26, Y, 'IglooCamp')
    igloo_ring(1395, -985, 6, 30, 151.0, 'IceCamp')
    igloo_ring(1620, -1010, 4, 24, 151.0, 'IceCamp')
    # ice fishing shanties and holes on the frozen lake
    for (x, z) in ((1460, -1080), (1530, -1120), (1590, -1060), (1420, -1130), (1500, -1030)):
        PARTS['shanties'].append({'x': x, 'z': z, 'rot': P.rng.uniform(0, 360), 'y': 150.0})
        PARTS['fishing_holes'].append({'x': x + 9, 'z': z + 4, 'y': 150.0})
    for (x, z) in ((1480, -1160), (1555, -1090), (1380, -1060)):
        PARTS['fishing_holes'].append({'x': x, 'z': z, 'y': 150.0})
    for (x, z) in ((1468, -1078), (1538, -1118), (1598, -1058)):
        P.put('E22_sled', x + 4, z - 9, P.rng.uniform(0, 360), 'IceLake', block=False, check=False)
        P.put('A87_bucket', x + 12, z + 6, 0, 'IceLake', block=False, check=False)
    bbox = (1420, 1860, -1025, -675)
    P.scatter(inside, ['E12_snowy_pine_1', 'E13_snowy_pine_2', 'E14_snowy_pine_3'], 70, 'Pines', min_gap=3, scale=(0.75, 1.2), bbox=bbox, block=True)
    P.scatter(inside, ['E15_snowy_rock_1', 'E16_snowy_rock_2', 'E17_snowy_bush', 'E25_snow_drift', 'E18_edelweiss', 'E19_gentian'], 190, 'Meadow', min_gap=0.8, scale=(0.9, 1.3), bbox=bbox,
              weights={'E18_edelweiss': 3, 'E19_gentian': 3, 'E17_snowy_bush': 2, 'E25_snow_drift': 1.5, 'E15_snowy_rock_1': 1, 'E16_snowy_rock_2': 1})
    P.scatter(inside, ['E22_sled', 'E23_cheese_cart', 'E24_beehive', 'A90_firewood_stack', 'A78_hay_bale', 'A81_wheelbarrow'], 30, 'Props', min_gap=2, scale=None, bbox=bbox)
    lp = pad('alpine_lake')
    shore = lambda x, z: W.pad_mask(lp, x, z) > 0.9 and math.hypot((x - 1490) / 170, (z + 1080) / 108) > 1.12
    P.scatter(shore, ['E12_snowy_pine_1', 'E13_snowy_pine_2', 'E14_snowy_pine_3', 'E15_snowy_rock_1', 'E16_snowy_rock_2', 'E25_snow_drift'], 80, 'LakeShore', min_gap=3, scale=(0.8, 1.3), bbox=(1260, 1720, -1230, -920))
    P.line_of('E21_log_fence', (1760, -915), (1760, -965), 'Farm', block=False)
    P.line_of('E21_log_fence', (1760, -965), (1830, -965), 'Farm', block=False)
    for (a, b) in (((1425, -680), (1520, -676)), ((1700, -676), (1855, -690))):
        P.line_of('E20_terrace_wall', a, b, 'Edge', block=False)
    P.save(f'{OUTDIR}\\v3_alpine.json')
    ALL_STREETS.extend(P.streets)
    return P


if __name__ == '__main__':
    stats = {}
    for fn in (capital, rusty, harbour, elf, alpine):
        p = fn()
        stats[p.area] = len(p.items)
    json.dump(ALL_STREETS, open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\streets.json', 'w'), separators=(',', ':'))
    json.dump(RESERVED, open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\reserved.json', 'w'), indent=1)
    json.dump(PARTS, open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\parts_plan.json', 'w'), indent=0)
    print(stats, 'streets', len(ALL_STREETS))
    print({k: len(v) for k, v in PARTS.items()})
    print(json.dumps(RESERVED))
