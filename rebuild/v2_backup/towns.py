"""Phase 1 town layouts (v2). Writes mapplan/v2_<area>.json plans and rebuild/streets.json."""
import json, math
from layout_lib import Plan, Polyline, obb, norm, face_rot, catmull, CAT
import world as W

OUTDIR = r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan'
ALL_STREETS = []
RESERVED = {}   # part-built buildings: name -> (cx, cz, half_len, half_wid, rot)

HOUSES_CAP = ['C05_townhouse_1', 'C06_townhouse_2', 'C07_townhouse_3', 'C08_townhouse_4', 'C09_corner_house', 'C10_terrace_row']
SHOPS_CAP = ['C12_bakery', 'C13_potion_shop', 'C14_magic_tool_shop']
TREES = ['A24_oak_1', 'A25_oak_2', 'A26_oak_3', 'A27_birch_1', 'A28_birch_2', 'A32_maple_autumn', 'A34_fruit_tree']
BUSHES = ['A38_bush_1', 'A39_bush_2', 'A40_bush_3']
FLOWERS = ['A43_flowers_red', 'A44_flowers_yellow', 'A45_flowers_purple', 'A46_flowers_white', 'A47_flowers_blue']
CRATES = ['A71_barrel', 'A72_barrel_open', 'A73_crate_small', 'A74_crate_large', 'A75_crate_stack', 'A76_sack', 'A77_sack_pile']


def in_pad(name, need=0.97):
    p = [q for q in W.PADS if q['name'] == name][0]
    return lambda x, z: W.pad_mask(p, x, z) >= need


def yard_dressing(P, inside, bbox, group, n_trees=40, n_bush=60, n_flower=50, extra=None):
    P.scatter(inside, TREES, n_trees, group, min_gap=4, scale=(0.75, 1.1), bbox=bbox)
    P.scatter(inside, BUSHES, n_bush, group, min_gap=1.5, scale=(0.8, 1.3), bbox=bbox)
    P.scatter(inside, FLOWERS, n_flower, group, min_gap=1.0, scale=(0.9, 1.3), bbox=bbox)
    if extra:
        for models, n in extra:
            P.scatter(inside, models, n, group, min_gap=2.5, scale=None, bbox=bbox)


# =================================================================== CAPITAL
def capital():
    P = Plan('v2_capital', seed=11)
    inside = in_pad('capital_city')
    Y = lambda z: min(71.0, max(22.0, 22 + 0.048 * (-1760 - z)))
    ZS, ZN, XE = -1762.0, -2735.0, 700.0
    # ---- walls
    P.put('C04_grand_gate', 0, ZS, 0, 'Walls', check=False)
    P.put('C04_grand_gate', 0, ZN, 180, 'Walls', check=False)
    for sx in (-1, 1):
        P.put('C02_city_wall_corner', sx * XE, ZS, 0, 'Walls', check=False)
        P.put('C02_city_wall_corner', sx * XE, ZN, 0, 'Walls', check=False)
        for tx in (240, 470):
            P.put('C03_city_wall_tower', sx * tx, ZS, 0, 'Walls', check=False)
            P.put('C03_city_wall_tower', sx * tx, ZN, 180, 'Walls', check=False)
        for tz in (-2000, -2250, -2500):
            P.put('C03_city_wall_tower', sx * XE, tz, 90 if sx > 0 else 270, 'Walls', check=False)
    nodes = [26, 229, 251, 459, 481, 684.5]
    for sx in (-1, 1):
        for i in range(0, len(nodes) - 1, 2):
            a, b = nodes[i], nodes[i + 1]
            # south wall faces south: draw west->east
            p0, p1 = (min(sx * a, sx * b), ZS), (max(sx * a, sx * b), ZS)
            P.line_of('C01_city_wall_straight', p0, p1, 'Walls')
            P.line_of('C01_city_wall_straight', (p1[0], ZN), (p0[0], ZN), 'Walls')
        zn = [ZS - 15.5, -1989, -2011, -2239, -2261, -2489, -2511, ZN + 15.5]
        for i in range(0, len(zn) - 1, 2):
            a, b = zn[i], zn[i + 1]
            if sx > 0:
                P.line_of('C01_city_wall_straight', (XE, a), (XE, b), 'Walls')
            else:
                P.line_of('C01_city_wall_straight', (-XE, b), (-XE, a), 'Walls')
    # gate dressing
    for sx in (-1, 1):
        P.put('A21_brazier', sx * 34, ZS + 16, 0, 'GateSquare', block=False, streets=False)
        P.put('A95_flag_pole', sx * 46, ZS - 22, 0, 'GateSquare', block=False, streets=False)
        P.put('A21_brazier', sx * 34, ZN - 16, 180, 'Walls', block=False)
    # ---- streets
    av = P.street([(0, -1745), (0, ZN + 8)], 13, 'Pavement', smooth=False, step=40)
    P.street([(0, ZN - 8), (0, ZN - 20)], 8, 'Pavement', smooth=False)
    ramp_pts = [(0, -2748, 70.2), (60, -2763, 72.5), (140, -2786, 78.5), (158, -2812, 84.0), (96, -2838, 91.0), (20, -2853, 98.5), (0, -2858, 100.0)]
    P.street([(p[0], p[1]) for p in ramp_pts], 8, 'Cobblestone', smooth=False, y=[p[2] for p in ramp_pts], bank=30)
    cross_z = [-1960, -2200, -2440, -2620]
    cross = {}
    for z in cross_z:
        cross[z] = P.street([(-672, z), (672, z)], 7, 'Cobblestone', smooth=False, step=40)
    ns = {}
    for x in (-340, 340):
        ns[x] = P.street([(x, -1790), (x, -2708)], 7, 'Cobblestone', smooth=False, step=40)
    ring = []
    for x in (-664, 664):
        ring.append(P.street([(x, -1790), (x, -2708)], 6, 'Cobblestone', smooth=False, step=40))
    ring.append(P.street([(-672, -1790), (672, -1790)], 6, 'Cobblestone', smooth=False, step=40))
    ring.append(P.street([(-672, -2708), (672, -2708)], 6, 'Cobblestone', smooth=False, step=40))
    # ---- plazas (reserve as blocks)
    plazas = [(0, -1820, 75, 34), (0, -2080, 115, 70), (0, -2320, 125, 62), (0, -2530, 62, 46)]
    for (cx, cz, rx, rz) in plazas:
        P.plaza(cx, cz, rx, rz, 'Pavement')
        P.sblocks.append(obb(cx, cz, rx, rz, 0))
    # landmarks
    P.put('C22_knight_statue', 0, -1826, 0, 'GateSquare', check=False)
    P.put('C21_plaza_fountain', 0, -2080, 0, 'MarketSquare', check=False)
    P.put('C23_obelisk', 0, -2320, 0, 'CathedralSquare', check=False)
    P.put('K44_monument_column', 0, -2530, 0, 'UpperPlaza', check=False)
    # cathedral (part-built, enterable) west of cathedral square, door facing east
    RESERVED['capital_cathedral'] = (-232, -2320, 82, 36, 90, Y(-2320))
    P.blocks.append(obb(-232, -2320, 36 + 3, 82 + 3, 90))
    P.put('C19_royal_library', 172, -2320, 270, 'CathedralSquare', check=False)
    P.put('C15_clock_tower', 140, -2392, 270, 'CathedralSquare', check=False)
    P.put('C11_market_hall', 150, -2080, 270, 'MarketSquare', check=False)
    P.put('C18_guild_hall', -146, -2080, 90, 'MarketSquare', check=False)
    P.put('C20_magic_academy', 70, -2585, 270, 'UpperAvenue', check=False)
    P.put('C17_knights_hq', -76, -2585, 90, 'UpperAvenue', check=False)
    # market stalls around the fountain
    stalls = ['A105_market_stall_fruit', 'A106_market_stall_cloth', 'A107_market_stall_potion']
    k = 0
    for ang in range(0, 360, 40):
        a = math.radians(ang)
        x, z = 62 * math.cos(a), -2080 + 40 * math.sin(a)
        P.put(stalls[k % 3], x, z, face_rot(-math.cos(a), -math.sin(a)), 'MarketSquare', block=False, pad=0.5, streets=False)
        k += 1
    for (x, z) in ((-90, -2040), (88, -2120), (-60, -2135), (95, -2030)):
        P.put('C26_vendor_cart', x, z, P.rng.uniform(0, 360), 'MarketSquare', block=False, streets=False)
        P.cluster(x + 8, z + 4, CRATES, 'MarketSquare', n=4, radius=5)
    for z in (-1995, -2165):
        P.put('C31_bunting', 0, z, 0, 'MarketSquare', block=False, check=False, yo=17)
    # benches + lamps around plazas
    for (cx, cz, rx, rz) in plazas:
        for ang in range(20, 360, 45):
            a = math.radians(ang)
            P.put('A15_lamp_iron_city', cx + (rx - 4) * math.cos(a), cz + (rz - 4) * math.sin(a), 0, 'Lamps', block=False, pad=0.2, streets=False)
        for ang in (0, 90, 180, 270):
            a = math.radians(ang + 45)
            P.put('A83_bench_stone', cx + (rx * 0.55) * math.cos(a), cz + (rz * 0.55) * math.sin(a), face_rot(-math.cos(a), -math.sin(a)), 'Plazas', block=False, pad=0.5, streets=False)
    # ---- frontage
    wts = {m: 1.0 for m in HOUSES_CAP}
    wts['C10_terrace_row'] = 0.6; wts['C09_corner_house'] = 0.5
    shopw = dict(wts); shopw.update({m: 1.2 for m in SHOPS_CAP})
    allh = HOUSES_CAP + SHOPS_CAP
    for side in (1, -1):
        P.frontage(av, side, allh, 'Avenue', 13, setback=4, gap=(1.5, 3.5), weights=shopw)
    for z, ln in cross.items():
        for side in (1, -1):
            P.frontage(ln, side, allh, f'Street_{-z}', 7, setback=3, gap=(2, 4), weights=shopw if z in (-1960, -2200) else wts)
    for x, ln in ns.items():
        for side in (1, -1):
            P.frontage(ln, side, HOUSES_CAP, f'Lane_{x}', 7, setback=3, gap=(2, 4.5), weights=wts)
    # mansions in the noble quarter (upper city, outer blocks) facing the noble row
    noble = ['K37_mansion_1', 'K38_mansion_2', 'K39_mansion_3']
    for sx in (-1, 1):
        for i, x in enumerate((180, 260, 470, 560)):
            P.put(noble[(i + (sx > 0)) % 3], sx * x, -2662, 0, 'NobleQuarter', pad=1.5)
    for side in (1, -1):
        for ln in ring:
            P.frontage(ln, side, HOUSES_CAP, 'OuterRing', 6, setback=3, gap=(3, 8), weights=wts, max_items=60)
    # ---- lamps
    for side in (1, -1):
        P.lamps(av, 'A16_lamp_iron_double', 'Lamps', 13, spacing=34, offset=1.6, s0=30, alternate=False, side=side)
    for ln in list(cross.values()) + list(ns.values()):
        P.lamps(ln, 'A15_lamp_iron_city', 'Lamps', 7, spacing=42, offset=1.4, s0=20)
    for ln in ring:
        P.lamps(ln, 'A15_lamp_iron_city', 'Lamps', 6, spacing=55, offset=1.3, s0=25)
    # ---- block interiors: gardens, wells, trees
    bb = (-690, 690, -2725, -1775)
    yard_dressing(P, inside, bb, 'Gardens', n_trees=170, n_bush=260, n_flower=200,
                  extra=[(['A98_well', 'A92_laundry_line', 'A82_bench_wood', 'A97_water_trough'], 30), (CRATES, 50), (['A48_planter_box', 'A109_fountain_small'], 25)])
    # ---- castle on the hill
    castle(P)
    P.save(f'{OUTDIR}\\v2_capital.json')
    ALL_STREETS.extend(P.streets)
    return P


def castle(P):
    CZ0 = -2868.0   # gatehouse line
    P.put('K08_gatehouse', 0, CZ0, 0, 'Castle', check=False)
    XW, ZB = 200.0, -3200.0
    for sx in (-1, 1):
        P.put('K06_curtain_wall_corner', sx * XW, CZ0, 0, 'Castle', check=False)
        P.put('K06_curtain_wall_corner', sx * XW, ZB, 0, 'Castle', check=False)
        P.put('K02_castle_round_tower', sx * XW, -3034, 0, 'Castle', check=False)
        P.put('K03_castle_square_tower', sx * 100, ZB, 0, 'Castle', check=False)
        P.put('K42_sentry_box', sx * 34, CZ0 + 16, 0, 'Castle', check=False)
        P.put('A21_brazier', sx * 30, CZ0 + 24, 0, 'Castle', block=False, check=False)
    # walls
    P.line_of('K05_curtain_wall_straight', (-XW + 16, CZ0), (-25, CZ0), 'Castle')
    P.line_of('K05_curtain_wall_straight', (25, CZ0), (XW - 16, CZ0), 'Castle')
    P.line_of('K05_curtain_wall_straight', (XW - 16, ZB), (110, ZB), 'Castle')
    P.line_of('K05_curtain_wall_straight', (90, ZB), (-90, ZB), 'Castle')
    P.line_of('K05_curtain_wall_straight', (-110, ZB), (-XW + 16, ZB), 'Castle')
    for (a, b) in ((CZ0 - 16, -3024), (-3044, ZB + 16)):
        P.line_of('K05_curtain_wall_straight', (XW, a), (XW, b), 'Castle')
        P.line_of('K05_curtain_wall_straight', (-XW, b), (-XW, a), 'Castle')
    P.put('K01_main_keep', 0, -3125, 0, 'Castle', check=False)
    for sx in (-1, 1):
        P.put('K04_spire_tower', sx * 62, -3150, 0, 'Castle', check=False)
    P.plaza(0, -2990, 150, 95, 'Pavement')
    P.street([(0, -2880), (0, -3098)], 9, 'Pavement', smooth=False)
    P.put('K23_royal_fountain', 0, -2990, 0, 'CastleCourt', check=False)
    P.put('K24_wizard_king_statue', 0, -3060, 0, 'CastleCourt', check=False)
    P.put('K40_barracks', -150, -2945, 90, 'CastleCourt', check=False)
    P.put('K41_stables', 150, -2945, 270, 'CastleCourt', check=False)
    P.put('K43_royal_carriage', 118, -2985, 0, 'CastleCourt', check=False)
    P.put('K30_gazebo', -125, -3090, 90, 'RoyalGarden', check=False)
    for sx in (-1, 1):
        for z in (-2915, -2955, -3020, -3070):
            P.put('K34_ornate_lamp', sx * 16, z, 0, 'CastleCourt', block=False, check=False)
        for z in (-2930, -3045):
            P.put('K35_royal_banner', sx * 40, z, 90 if sx < 0 else 270, 'CastleCourt', block=False, check=False)
        for z in (-3030, -3060, -3090):
            P.put('K26_topiary_cone', sx * 34, z, 0, 'RoyalGarden', block=False, check=False)
        for z in (-2930, -2960):
            P.put('K25_topiary_ball', sx * 60, z, 0, 'RoyalGarden', block=False, check=False)
        P.put('K27_topiary_spiral', sx * 90, -3060, 0, 'RoyalGarden', block=False, check=False)
        P.put('K33_ornate_bench', sx * 58, -3000, 90 if sx < 0 else 270, 'RoyalGarden', block=False, check=False)
        P.put('K31_rose_arch', sx * 100, -3110, 0, 'RoyalGarden', block=False, check=False)
        for z in (-3135, -3160):
            P.put('K28_maze_hedge_straight', sx * 130, z, 0, 'RoyalGarden', block=False, check=False)
        P.put('K32_ornate_planter', sx * 26, -2900, 0, 'CastleCourt', block=False, check=False)
    garden = lambda x, z: abs(x) < 185 and -3185 < z < -2885
    P.scatter(garden, ['K25_topiary_ball', 'K26_topiary_cone', 'K32_ornate_planter'] + FLOWERS, 40, 'RoyalGarden', min_gap=2, scale=None, bbox=(-185, 185, -3185, -2885))


# =================================================================== RUSTY
def rusty():
    P = Plan('v2_rusty', seed=23)
    inside = lambda x, z: W.pad_mask([q for q in W.PADS if q['name'] == 'rusty'][0], x, z) > 0.9
    main = P.street([(1610, 1530), (1700, 1586), (1795, 1636), (1880, 1695), (1958, 1752), (2028, 1808)], 8, 'Ground', step=18)
    lane1 = P.street([(1872, 1708), (1838, 1785), (1800, 1870), (1770, 1940)], 6, 'Ground', step=18)
    lane2 = P.street([(1892, 1688), (1952, 1622), (2020, 1560), (2060, 1520)], 6, 'Ground', step=18)
    P.plaza(1880, 1695, 44, 44, 'Ground')
    P.sblocks.append(obb(1880, 1695, 40, 40, 0))
    P.plaza(2010, 1796, 34, 34, 'Ground')
    # big part-built church: axis along main street direction, door facing back up the street (NW)
    d = norm(2028 - 1958, 1808 - 1752)
    ccx, ccz = 2028 + d[0] * 104, 1808 + d[1] * 104
    rot = face_rot(-d[0], -d[1])
    RESERVED['rusty_church'] = (round(ccx, 1), round(ccz, 1), 88, 42, round(rot, 1), 14.0)
    P.blocks.append(obb(ccx, ccz, 42 + 4, 88 + 4, rot))
    # square
    P.put('D36_old_well_pump', 1880, 1695, 30, 'Square', check=False)
    P.put('D25_rundown_tavern', 1880 + 50, 1695 - 46, face_rot(-0.73, 0.68), 'Square')
    P.put('D28_rusty_water_tower', 1830, 1650, 0, 'Square')
    P.put('D26_blacksmith_shed', 1838, 1748, face_rot(0.6, -0.8), 'Square')
    P.put('A99_anvil', 1850, 1736, 20, 'Square', block=False, streets=False)
    P.put('A93_notice_board', 1906, 1668, face_rot(-0.6, 0.8), 'Square', block=False, streets=False)
    houses = ['D20_rundown_house_1', 'D21_rundown_house_2', 'D22_rundown_house_3', 'D23_rundown_house_4', 'D34_boarded_shack']
    wts = {'D34_boarded_shack': 0.6}
    for side in (1, -1):
        P.frontage(main, side, houses + ['D24_collapsed_ruin'], 'MainStreet', 8, setback=3, gap=(3, 9), weights=dict(wts, D24_collapsed_ruin=0.3))
        P.frontage(lane1, side, houses, 'SouthLane', 6, setback=3, gap=(4, 10), weights=wts)
        P.frontage(lane2, side, houses, 'NorthLane', 6, setback=3, gap=(4, 10), weights=wts)
    for ln in (main, lane1, lane2):
        P.lamps(ln, 'D37_crooked_lamp', 'Lamps', 7 if ln is main else 5, spacing=36, offset=1.3, s0=15)
    # graveyard beside the church (to its left when walking up the street)
    nL = (d[1], -d[0])
    gcx, gcz = ccx + nL[0] * 92 - d[0] * 10, ccz + nL[1] * 92 - d[1] * 10
    grot = face_rot(-nL[0], -nL[1])
    gw, gd = 46, 38
    corners = []
    ux, uz = (math.cos(math.radians(grot)), -math.sin(math.radians(grot))), (math.sin(math.radians(grot)), math.cos(math.radians(grot)))
    def gpt(a, b):
        return (gcx + ux[0] * a + uz[0] * b, gcz + ux[1] * a + uz[1] * b)
    P.put('D18_graveyard_gate', *gpt(0, gd), grot, 'Graveyard', check=False)
    P.line_of('A103_fence_iron', gpt(-gw, gd), gpt(-8, gd), 'Graveyard', block=False)
    P.line_of('A103_fence_iron', gpt(8, gd), gpt(gw, gd), 'Graveyard', block=False)
    P.line_of('D33_broken_fence', gpt(gw, gd), gpt(gw, -gd), 'Graveyard', block=False)
    P.line_of('D33_broken_fence', gpt(gw, -gd), gpt(-gw, -gd), 'Graveyard', block=False)
    P.line_of('A103_fence_iron', gpt(-gw, -gd), gpt(-gw, gd), 'Graveyard', block=False)
    graves = ['D12_gravestone_1', 'D13_gravestone_2', 'D14_gravestone_3', 'D15_gravestone_4', 'D16_stone_cross']
    for r in range(5):
        for c in range(-6, 7):
            if abs(c) <= 1 and r >= 0:
                continue
            if P.rng.random() < 0.82:
                x, z = gpt(c * 6.2 + P.rng.uniform(-0.6, 0.6), gd - 10 - r * 9)
                P.put(P.rng.choice(graves), x, z, grot + P.rng.uniform(-8, 8), 'Graveyard', block=False, pad=0.1)
    P.put('D17_mausoleum', *gpt(-28, -24), grot, 'Graveyard', check=False)
    P.put('D19_weeping_statue', *gpt(0, -14), grot, 'Graveyard', check=False)
    for a, b in ((30, -28), (-40, 6), (38, 20)):
        P.put('A35_dead_tree_1' if a > 0 else 'A36_dead_tree_2', *gpt(a, b), P.rng.uniform(0, 360), 'Graveyard', block=False, check=False)
    P.blocks.append(obb(gcx, gcz, gw + 2, gd + 2, grot))
    # windmill on a rise north-east, tents and scrap on the edges
    P.put('D27_broken_windmill', 2085, 1585, 230, 'Edges')
    for (x, z) in ((1700, 1760), (1760, 1830), (2010, 1640), (1680, 1680)):
        P.put('D29_patched_tent', x, z, P.rng.uniform(0, 360), 'Edges')
        P.put('A22_campfire', x + 9, z + 6, 0, 'Edges', block=False)
    junk = ['D30_scrap_pile', 'D31_rusted_cart', 'D32_broken_barrel', 'D35_collapsed_wall', 'A90_firewood_stack', 'A79_hand_cart', 'A78_hay_bale']
    bbox = (1560, 2240, 1390, 2010)
    P.scatter(inside, junk, 45, 'Clutter', min_gap=3, scale=None, bbox=bbox)
    P.scatter(inside, ['A35_dead_tree_1', 'A36_dead_tree_2', 'A68_stump_1', 'A69_stump_2'], 35, 'Clutter', min_gap=5, bbox=bbox)
    P.scatter(inside, ['A49_tall_grass_1', 'A50_tall_grass_2', 'A56_rock_small_1', 'A57_rock_small_2', 'A58_rock_medium_1'], 120, 'Clutter', min_gap=1, bbox=bbox)
    P.scatter(inside, ['D33_broken_fence', 'A101_fence_rail'], 20, 'Clutter', min_gap=2, bbox=bbox)
    P.save(f'{OUTDIR}\\v2_rusty.json')
    ALL_STREETS.extend(P.streets)
    return P


# =================================================================== HARBOUR
def harbour():
    P = Plan('v2_harbour', seed=37)
    pad = [q for q in W.PADS if q['name'] == 'harbour'][0]
    inside = lambda x, z: W.pad_mask(pad, x, z) > 0.95 and z < 2826
    main = P.street([(-600, 2290), (-600, 2836)], 9, 'Cobblestone', smooth=False, step=30)
    quay = P.street([(-935, 2850), (-265, 2850)], 11, 'Cobblestone', smooth=False, y=4.5, step=30)
    cross = []
    for z, x0, x1 in ((2440, -960, -240), (2625, -970, -230)):
        cross.append((z, P.street([(x0, z), (x1, z)], 7, 'Cobblestone', smooth=False, step=30)))
    lanes = []
    for x in (-810, -390):
        lanes.append(P.street([(x, 2395), (x, 2836)], 6, 'Cobblestone', smooth=False, step=30))
    P.plaza(-600, 2540, 44, 36, 'Pavement')
    P.sblocks.append(obb(-600, 2540, 40, 32, 0))
    P.put('A109_fountain_small', -600, 2540, 0, 'Square', check=False)
    for ang in range(0, 360, 60):
        a = math.radians(ang)
        P.put('A82_bench_wood', -600 + 20 * math.cos(a), 2540 + 15 * math.sin(a), face_rot(-math.cos(a), -math.sin(a)), 'Square', block=False, streets=False)
    # enterable tavern (part-built) at the main street / quay corner, west side, door facing east onto the main street
    RESERVED['harbour_tavern'] = (-648, 2792, 22, 17, 90, W.ground_no_noise(-648, 2792))
    P.blocks.append(obb(-648, 2792, 17 + 2, 22 + 2, 90))
    P.put('G14_harbour_master', -560, 2800, 270, 'Waterfront', check=True)
    # warehouses facing the quay
    for x in (-900, -850, -760, -705, -480, -425, -330, -280):
        P.put('G12_warehouse_1' if x % 3 else 'G13_warehouse_2', x, 2814, 0, 'Waterfront', pad=1.0)
    # seawall + piers
    P.line_of('G28_seawall', (-940, 2878), (-260, 2878), 'Waterfront', block=False, streets=False)
    for i, it in enumerate(P.items):
        if it['model'] == 'G28_seawall':
            it['y_offset'] = -8.5
    for px in (-800, -600, -400):
        for k in range(4):
            P.put('G01_pier_straight', px, 2896 + k * 24, 0, 'Piers', check=False, yo=-5.0)
        P.put('G03_pier_end', px, 2994, 0, 'Piers', check=False, yo=-5.0)
        for k in range(0, 4, 2):
            P.put('G31_mooring_bollard', px + 5, 2900 + k * 24, 90, 'Piers', block=False, check=False, yo=4.7)
    P.put('G06_galleon', -577, 2942, 90, 'Ships', check=False, yo=-7.0)
    P.put('G07_merchant_ship', -421, 2940, 270, 'Ships', check=False, yo=-6.0)
    P.put('G08_fishing_boat_1', -779, 2918, 90, 'Ships', check=False, yo=-2.5)
    P.put('G09_fishing_boat_2', -821, 2948, 270, 'Ships', check=False, yo=-2.5)
    P.put('G08_fishing_boat_1', -821, 2914, 270, 'Ships', check=False, yo=-2.5)
    for (x, z) in ((-700, 2900), (-500, 2905), (-300, 2896), (-900, 2898)):
        P.put('G10_rowboat', x, z, P.rng.uniform(0, 360), 'Ships', check=False, yo=-0.6)
    for (x, z) in ((-700, 3010), (-480, 3030), (-880, 3000), (-330, 2990)):
        P.put('G20_buoy', x, z, 0, 'Ships', check=False, yo=-2.0)
    P.put('G16_cargo_crane', -520, 2864, 180, 'Waterfront', check=False)
    P.put('G16_cargo_crane', -700, 2864, 180, 'Waterfront', check=False)
    for x in (-880, -830, -740, -450, -360, -310):
        P.put('G15_fish_market_stall' if x % 2 else 'G17_net_rack', x, 2862, 0, 'Waterfront', block=False, streets=False)
    quayprops = ['G18_rope_coil', 'G19_anchor', 'G21_lobster_trap', 'G33_cargo_pallet', 'A71_barrel', 'A74_crate_large', 'A75_crate_stack']
    for x in range(-920, -260, 26):
        P.cluster(x + P.rng.uniform(-6, 6), 2868 + P.rng.uniform(-3, 3), quayprops, 'Waterfront', n=2, radius=4)
    for x in range(-930, -260, 60):
        P.put('A15_lamp_iron_city', x, 2872, 0, 'Lamps', block=False, streets=False)
    # lighthouse + fort on the headlands
    P.put('G11_lighthouse', -95, 2930, 200, 'Headlands', check=False)
    P.put('G23_harbour_fort', -1120, 2905, 160, 'Headlands', check=False)
    for k, (x, z) in enumerate(((-1140, 2945), (-1100, 2950), (-1160, 2925))):
        P.put('G22_cannon', x, z, 170, 'Headlands', block=False, check=False)
    # houses
    houses = ['G24_harbour_house_1', 'G25_harbour_house_2', 'G26_harbour_house_3']
    for side in (1, -1):
        P.frontage(main, side, houses + ['G27_harbour_tavern'], 'MainStreet', 9, setback=3, gap=(1.5, 3.5), s0=8, s1=470, weights={'G27_harbour_tavern': 0.25})
        for z, ln in cross:
            P.frontage(ln, side, houses, f'Street_{z}', 7, setback=3, gap=(2, 4))
        for ln in lanes:
            P.frontage(ln, side, houses, 'Lanes', 6, setback=3, gap=(2, 5), s1=380)
    for ln in [main] + [c[1] for c in cross] + lanes:
        P.lamps(ln, 'A15_lamp_iron_city', 'Lamps', 7, spacing=40, offset=1.3, s0=14)
    bbox = (-1020, -180, 2230, 2826)
    yard_dressing(P, inside, bbox, 'Gardens', n_trees=40, n_bush=80, n_flower=60,
                  extra=[(['A92_laundry_line', 'A98_well', 'A82_bench_wood', 'G17_net_rack'], 18), (CRATES, 30)])
    P.save(f'{OUTDIR}\\v2_harbour.json')
    ALL_STREETS.extend(P.streets)
    return P


# =================================================================== ELF
def elf():
    P = Plan('v2_elf', seed=41)
    pad = [q for q in W.PADS if q['name'] == 'elf'][0]
    inside = lambda x, z: W.pad_mask(pad, x, z) > 0.6
    TX, TZ = -2400, -640
    P.put('F01_world_tree', TX, TZ, 90, 'WorldTree', check=False)
    P.blocks.append(obb(TX, TZ, 92, 92, 0))
    gate = P.street([(-1935, -600), (-2050, -604), (-2170, -618), (-2300, -634)], 4.5, 'Limestone', step=16)
    ring_pts = [(TX + 128 * math.cos(math.radians(a)), TZ + 128 * math.sin(math.radians(a))) for a in range(0, 361, 15)]
    ring = P.street(ring_pts, 3.5, 'Limestone', smooth=False, block=False)
    north = P.street([(TX, TZ - 130), (TX + 10, -880), (TX, -955)], 4, 'Limestone', step=16)
    south = P.street([(TX, TZ + 130), (TX - 12, -410), (TX, -318)], 4, 'Limestone', step=16)
    west = P.street([(TX - 130, TZ), (-2650, -600), (-2780, -560)], 3.5, 'Limestone', step=16)
    ne = P.street([(-2310, -730), (-2220, -820), (-2165, -868)], 3.5, 'Limestone', step=16)
    P.put('F10_elf_palace', TX, -990, 0, 'Palace', check=False)
    P.blocks.append(obb(TX, -990, 30, 30, 0))
    P.put('F11_moon_pool', TX, -290, 0, 'MoonPool', check=False)
    P.blocks.append(obb(TX, -290, 16, 16, 0))
    RESERVED['elf_temple'] = (-2195, -440, 26, 26, 270, W.ground_no_noise(-2195, -440))
    P.blocks.append(obb(-2195, -440, 28, 28, 0))
    for (x, z, m, r) in ((-2650, -780, 'F02_treehouse_1', 60), (-2690, -460, 'F03_treehouse_2', 120), (-2560, -350, 'F04_treehouse_3', 160),
                         (-2240, -800, 'F05_treehouse_4', 300), (-2600, -930, 'F03_treehouse_2', 20), (-2790, -660, 'F04_treehouse_3', 90),
                         (-2160, -560, 'F02_treehouse_1', 270)):
        P.put(m, x, z, r, 'Treehouses', pad=2)
    P.put('F06_platform_ring', TX + 60, TZ - 96, 0, 'WorldTree', block=False, check=False, yo=24)
    P.put('F09_spiral_stair', TX + 92, TZ - 60, 0, 'WorldTree', check=False)
    P.put('F12_carved_arch', -1990, -601, 90, 'GatePath', check=False)
    P.put('F17_root_arch', -2120, -612, 90, 'GatePath', check=False)
    for (x, z) in ((-2040, -588), (-2040, -620), (-2210, -604), (-2210, -638)):
        P.put('F13_elf_statue', x, z, 90 if z > -610 else 90, 'GatePath', block=False)
    paths = [gate, north, south, west, ne]
    for ln in paths:
        P.lamps(ln, 'F28_elf_standing_lantern', 'Lanterns', 4, spacing=26, offset=1.2, s0=8)
    for ln in paths + [ring]:
        for s in range(6, int(ln.L), 9):
            (px, pz), d = ln.at(s)
            R = (-d[1], d[0])
            sd = 1 if (s // 9) % 2 else -1
            off = 6 + P.rng.uniform(0, 4)
            P.put(P.rng.choice(['F23_glow_mushroom_1', 'F24_glow_mushroom_2', 'F25_glow_flower_1', 'F26_glow_flower_2']),
                  px + R[0] * sd * off, pz + R[1] * sd * off, P.rng.uniform(0, 360), 'GlowPath', block=False, pad=0.2, scale=P.rng.uniform(0.8, 1.3))
    for (x, z, r) in ((-2290, -905, 20), (-2560, -1040, 0), (-2780, -880, 60), (-2600, -250, 200)):
        P.put('F30_ruins_1' if x % 2 else 'F31_ruins_2', x, z, r, 'Ruins')
    P.put('F32_waterfall_cliff', -2110, -1015, 0, 'Lake', check=False)
    for k in range(9):
        a = P.rng.uniform(0, math.tau)
        P.put('F29_lotus', -2120 + 70 * math.cos(a) * P.rng.uniform(0.2, 0.9), -930 + 50 * math.sin(a) * P.rng.uniform(0.2, 0.9), P.rng.uniform(0, 360), 'Lake', block=False, check=False)
    for (x, z) in ((-2215, -690), (-2205, -540), (-2150, -400)):
        P.put('A66_stepping_stones', x, z, 75, 'Stream', block=False, check=False)
    for (x, z) in ((-2330, -470), (-2470, -470), (-2520, -760), (-2290, -790)):
        P.put('F33_elf_bench', x, z, face_rot(TX - x, TZ - z), 'WorldTree', block=False)
    bbox = (-2900, -1900, -1090, -110)
    far = lambda x, z: inside(x, z) and math.hypot(x - TX, z - TZ) > 165
    P.scatter(far, ['F14_jungle_tree_1', 'F15_jungle_tree_2'], 55, 'Jungle', min_gap=4, scale=(0.75, 1.1), bbox=bbox, block=True)
    P.scatter(far, ['F16_jungle_palm', 'A33_willow', 'A24_oak_1', 'A29_pine_1'], 60, 'Jungle', min_gap=3, scale=(0.8, 1.2), bbox=bbox, block=True,
              weights={'F16_jungle_palm': 3, 'A33_willow': 1, 'A24_oak_1': 1, 'A29_pine_1': 0.3})
    P.scatter(inside, ['F21_giant_fern', 'F22_giant_leaf_plant', 'A51_fern', 'A38_bush_1', 'A39_bush_2', 'F35_vine_pillar', 'F34_crystal_cluster'], 420, 'Undergrowth', min_gap=0.8, scale=(0.8, 1.3), bbox=bbox,
              weights={'F21_giant_fern': 3, 'F22_giant_leaf_plant': 3, 'A51_fern': 3, 'A38_bush_1': 1, 'A39_bush_2': 1, 'F35_vine_pillar': 0.3, 'F34_crystal_cluster': 0.4})
    P.scatter(inside, ['F23_glow_mushroom_1', 'F24_glow_mushroom_2', 'A54_mushroom_cluster', 'F25_glow_flower_1', 'F26_glow_flower_2'], 220, 'Undergrowth', min_gap=0.5, scale=(0.8, 1.4), bbox=bbox)
    P.save(f'{OUTDIR}\\v2_elf.json')
    ALL_STREETS.extend(P.streets)
    return P


# =================================================================== ALPINE
def alpine():
    P = Plan('v2_alpine', seed=53)
    pad = [q for q in W.PADS if q['name'] == 'alpine_shelf'][0]
    inside = lambda x, z: W.pad_mask(pad, x, z) > 0.97
    main = P.street([(2640, -1166), (2585, -1198), (2528, -1238), (2502, -1300), (2484, -1362), (2470, -1408)], 6, 'Cobblestone', step=16, y=115.0)
    east = P.street([(2510, -1302), (2580, -1322), (2652, -1352)], 5, 'Cobblestone', step=16, y=115.0)
    west = P.street([(2524, -1242), (2450, -1232), (2398, -1262)], 5, 'Cobblestone', step=16, y=115.0)
    P.plaza(2502, -1300, 26, 26, 'Cobblestone', y=115.0)
    P.sblocks.append(obb(2502, -1300, 24, 24, 0))
    P.put('A98_well', 2502, -1300, 0, 'Square', check=False)
    P.put('E06_stone_chapel', 2470, -1436, 0, 'Chapel', check=False)
    P.blocks.append(obb(2470, -1436, 9, 15, 0))
    RESERVED['alpine_lodge'] = (2445, -1310, 24, 17, 90, 115.0)
    P.blocks.append(obb(2445, -1310, 17 + 2, 24 + 2, 90))
    P.put('E07_sawmill', 2655, -1418, 0, 'Pond', pad=1.5)
    P.put('E08_barn', 2668, -1250, 270, 'Farm', pad=1.5)
    P.put('E09_goat_pen', 2640, -1290, 270, 'Farm', pad=1.0)
    P.put('E10_watchtower', 2700, -1185, 230, 'Edge', check=False)
    chalets = ['E01_chalet_1', 'E02_chalet_2', 'E03_chalet_3', 'E04_chalet_4']
    for side in (1, -1):
        P.frontage(main, side, chalets, 'MainStreet', 6, setback=4, gap=(4, 9))
        P.frontage(east, side, chalets, 'EastLane', 5, setback=4, gap=(5, 10))
        P.frontage(west, side, chalets, 'WestLane', 5, setback=4, gap=(5, 10))
    for ln in (main, east, west):
        P.lamps(ln, 'A17_lamp_wood_rustic', 'Lamps', 6, spacing=34, offset=1.3, s0=12)
    bbox = (2370, 2710, -1460, -1140)
    P.scatter(inside, ['E12_snowy_pine_1', 'E13_snowy_pine_2', 'E14_snowy_pine_3'], 60, 'Pines', min_gap=3, scale=(0.75, 1.15), bbox=bbox, block=True)
    P.scatter(inside, ['E15_snowy_rock_1', 'E16_snowy_rock_2', 'E17_snowy_bush', 'E25_snow_drift', 'E18_edelweiss', 'E19_gentian'], 160, 'Meadow', min_gap=0.8, scale=(0.9, 1.3), bbox=bbox,
              weights={'E18_edelweiss': 3, 'E19_gentian': 3, 'E17_snowy_bush': 2, 'E25_snow_drift': 1, 'E15_snowy_rock_1': 1, 'E16_snowy_rock_2': 1})
    P.scatter(inside, ['E22_sled', 'E23_cheese_cart', 'E24_beehive', 'A90_firewood_stack', 'A78_hay_bale', 'A81_wheelbarrow'], 26, 'Props', min_gap=2, scale=None, bbox=bbox)
    P.line_of('E21_log_fence', (2620, -1270), (2620, -1312), 'Farm', block=False)
    P.line_of('E21_log_fence', (2620, -1312), (2662, -1312), 'Farm', block=False)
    P.save(f'{OUTDIR}\\v2_alpine.json')
    ALL_STREETS.extend(P.streets)
    return P


if __name__ == '__main__':
    stats = {}
    for fn in (capital, rusty, harbour, elf, alpine):
        p = fn()
        stats[p.area] = len(p.items)
    json.dump(ALL_STREETS, open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\streets.json', 'w'), separators=(',', ':'))
    json.dump(RESERVED, open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\reserved.json', 'w'), indent=1)
    print(stats, 'streets', len(ALL_STREETS))
    print(json.dumps(RESERVED))
