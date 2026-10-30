"""dress_v4.py - settlement dressing (round 3). Needs: terrain_map.json (fresh), world.json, occ_*.json, enterable_fp.json, foam_segments.json.
Writes mapplan/v4_dress_*.json plans (place each with rebuild/v4/build_v4.ps1 -area <plan>):
  v4_dress_castle  castle courtyard + outer wall base      v4_dress_capital capital interior trees + outer wall seam + avenue stalls
  v4_dress_harbour inland trees, beach, quay life          v4_dress_rusty   desert floor dressing
  v4_dress_alpine  ice lake rim                            v4_dress_elf     pool rims + clearings
  town1_dress      skull apron ring + graveyard feather    (Town 1 zone items must live in a plan named town1_*)
Replayable: python dress_v4.py
"""
import sys, json, math, random, collections, csv, os
V4 = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4'
TOWN = r'C:\Users\Nitro\.kiro\crew\workspace\town'
sys.path.insert(0, V4)
import env_plan as E

E.load_occupancy()
rng = random.Random(9031)
OBUCK = E.OBUCK


def add_occ(x, z, hx, hz):
    for bi in range(int((x - hx) // OBUCK), int((x + hx) // OBUCK) + 1):
        for bj in range(int((z - hz) // OBUCK), int((z + hz) // OBUCK) + 1):
            E.OCC.setdefault((bi, bj), []).append((x, z, hx, hz))


for (x, z, hx, hz, name) in json.load(open(V4 + r'\enterable_fp.json')):
    add_occ(x, z, hx + 6, hz + 6)

# sizes of models (footprint) for registering what we place
SZ = {}
for e in json.load(open(TOWN + r'\mapplan\catalog.json', encoding='utf-8-sig')):
    SZ[e['id']] = (e['size_x'], e['size_z'])
for k, v in json.load(open(TOWN + r'\library\v4_meta.json')).items():
    SZ[k] = (v['size'][0], v['size'][1])

REJ = collections.Counter()
PLACED = collections.Counter()


def put(plan, model, x, z, rot, group, scale=1.0, yo=None, reg=True):
    if model is None:
        return False
    ok = E.put(plan, model, x, z, rot, group, scale=scale, yo=yo)
    if not ok:
        REJ[model] += 1
        return False
    PLACED[plan] += 1
    if reg:
        sx, sz = SZ.get(model, (4.0, 4.0))
        r = max(sx, sz) * scale * 0.5
        add_occ(x, z, r * 0.8, r * 0.8)
    return True


def _free(x, z, margin=4.0, road=6.0, minh=2.0, river=3.0):
    if not E.in_map(x, z) or E.H(x, z) < minh:
        return False
    if E.has_water(x, z) or E.in_lake(x, z, 1.04):
        return False
    if E.ROADS.dist(x, z) < road or E.RIVERS.dist(x, z) < river:
        return False
    return not E.occupied(x, z, margin)


def free(x, z, margin=4.0, road=6.0, minh=2.0, river=3.0):
    return _free(x, z, margin, road, minh, river)


def W(*pairs):
    return list(pairs)


def choose(lst):
    names = [n for n, w in lst if n in E.IDS]
    wts = [w for n, w in lst if n in E.IDS]
    return rng.choices(names, wts)[0] if names else None


class Spacing:
    """dart throwing with a minimum distance between accepted points of this recipe"""
    def __init__(self, d):
        self.d, self.b = d, {}

    def ok(self, x, z):
        bx, bz = int(x // self.d), int(z // self.d)
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                for (px, pz) in self.b.get((bx + i, bz + j), ()):
                    if (px - x) ** 2 + (pz - z) ** 2 < self.d ** 2:
                        return False
        return True

    def add(self, x, z):
        self.b.setdefault((int(x // self.d), int(z // self.d)), []).append((x, z))


def scatter(n, region, sp, test, make, tries=60):
    """n points inside region (x0,x1,z0,z1) accepted by test(x,z) and spacing; make(x,z) places and returns True"""
    got = 0
    x0, x1, z0, z1 = region
    for _ in range(n * tries):
        if got >= n:
            break
        x, z = rng.uniform(x0, x1), rng.uniform(z0, z1)
        if not sp.ok(x, z) or not test(x, z):
            continue
        if make(x, z):
            sp.add(x, z)
            got += 1
    return got


TREES_TOWN = W(('A34_fruit_tree', 1.2), ('A27_birch_1', 1.0), ('A28_birch_2', 1.0), ('A24_oak_1', 0.7), ('A25_oak_2', 0.7), ('A32_maple_autumn', 0.9),
               ('F01_04_tree_heartland_04', 0.5), ('F01_06_tree_heartland_06', 0.5), ('A26_oak_3', 0.5))
BUSHES = W(('A38_bush_1', 1.0), ('A39_bush_2', 1.0), ('A40_bush_3', 0.9), ('F05_01_bush_round', 1.0), ('F05_04_bush_juniper', 0.7), ('F05_02_bush_flower', 0.6), ('F05_03_bush_berry', 0.4))
TUFTS = W(('A49_tall_grass_1', 1.0), ('A50_tall_grass_2', 1.0), ('F05_09_grass_tall_a', 0.6), ('F05_10_grass_tall_b', 0.6), ('A51_fern', 0.5))
ROCKS = W(('A56_rock_small_1', 1.0), ('A57_rock_small_2', 1.0), ('E15_01_boulder_01', 0.8), ('E15_02_boulder_02', 0.8), ('E15_03_boulder_03', 0.8), ('E15_04_boulder_04', 0.6), ('F06_13_boulder_mossy', 0.7), ('A58_rock_medium_1', 0.4))
FLOWERS = W(('F06_16_flowers_buttercup', 1.0), ('F06_17_flowers_cornflower', 1.0), ('F06_18_flowers_poppy', 0.8), ('F06_19_flowers_wild', 1.0), ('A46_flowers_white', 0.6), ('A44_flowers_yellow', 0.6))


def wall_ring(plan, rect, gap_xs, off_in, off_out, step, group_prefix, trees_every=7, bush_scale=(0.9, 1.35), gates=()):
    """clusters around the outside of a rectangular wall (x0,x1,z0,z1); gates = [(x,z,r)] kept clear"""
    x0, x1, z0, z1 = rect
    n = 0
    sides = [('N', x0, x1, z0, -1), ('S', x0, x1, z1, 1), ('W', z0, z1, x0, -1), ('E', z0, z1, x1, 1)]
    k = 0
    for name, a, b, c, sgn in sides:
        t = a + rng.uniform(0, step)
        while t < b:
            k += 1
            off = rng.uniform(off_in, off_out)
            if name in ('N', 'S'):
                x, z = t, c + sgn * off
            else:
                x, z = c + sgn * off, t
            t += step * rng.uniform(0.8, 1.25)
            if any(math.hypot(x - gx, z - gz) < gr for gx, gz, gr in gates):
                continue
            if not free(x, z, 3.0, 8.0):
                continue
            r = rng.random()
            if k % trees_every == 0:
                m, sc = choose(TREES_TOWN), rng.uniform(0.7, 1.05)
                g = 'Trees' + group_prefix
            elif r < 0.5:
                m, sc = choose(BUSHES), rng.uniform(*bush_scale)
                g = group_prefix + 'Bushes'
            elif r < 0.75:
                m, sc = choose(ROCKS), rng.uniform(0.9, 1.7)
                g = group_prefix + 'Rocks'
            else:
                m, sc = choose(TUFTS), rng.uniform(0.9, 1.5)
                g = group_prefix + 'Tufts'
            if put(plan, m, x, z, rng.uniform(0, 360), g, scale=sc):
                n += 1
    return n


# ============================================================ CASTLE
def castle():
    P = 'v4_dress_castle'
    n = collections.Counter()
    free = lambda x, z, margin=4.0, road=6.0, minh=2.0, river=3.0: _free(x, z, margin, -9e9, minh, river)
    # new buildings replace the old K40/K41 (archived by archive_dress.luau)
    for m, x, z, rot in (('B04_01_barracks', -163, -2102, 90), ('B04_02_stables', 163, -2102, 270)):
        if put(P, m, x, z, rot, 'CastleBuildings', scale=1.0, reg=False):
            n['buildings'] += 1
            add_occ(x, z, 18, 24)
    # trees and shrubs along the inner walls (west and east, plus the south wall west and east of the gatehouse)
    sp = Spacing(26)
    inner = [(-176, -2040, -2340), (176, -2040, -2340)]
    for (x, za, zb) in inner:
        z = za
        while z > zb:
            zz = z + rng.uniform(-6, 6)
            xx = x + rng.uniform(-5, 5)
            if abs(zz + 2184) > 34 and free(xx, zz, 5.0, 6.0) and sp.ok(xx, zz):
                if put(P, choose(TREES_TOWN), xx, zz, rng.uniform(0, 360), 'TreesCastle', scale=rng.uniform(0.75, 1.0)):
                    sp.add(xx, zz); n['trees'] += 1
            z -= 30
    for x0, x1 in ((-176, -72), (72, 176)):
        x = x0
        while x < x1:
            xx, zz = x + rng.uniform(-4, 4), -2036 + rng.uniform(-4, 4)
            if free(xx, zz, 5.0, 6.0) and sp.ok(xx, zz):
                if put(P, choose(TREES_TOWN), xx, zz, rng.uniform(0, 360), 'TreesCastle', scale=rng.uniform(0.7, 0.95)):
                    sp.add(xx, zz); n['trees'] += 1
            x += 32
    # undergrowth strips under the trees
    sp2 = Spacing(9)
    for (x0, x1, z0, z1) in ((-190, -166, -2345, -2036), (166, 190, -2345, -2036), (-190, -72, -2046, -2026), (72, 190, -2046, -2026)):
        n['bushes'] += scatter(18, (x0, x1, z0, z1), sp2, lambda x, z: free(x, z, 2.5, 5.0),
                               lambda x, z: put(P, choose(BUSHES if rng.random() < 0.6 else FLOWERS), x, z, rng.uniform(0, 360), 'CastleBeds', scale=rng.uniform(0.9, 1.3)))
    # well, benches around the fountain, crates and barrels near the new buildings, carts
    spc = Spacing(8)
    well_ok = False
    for (x, z) in ((105, -2200), (95, -2212), (120, -2195), (110, -2185)):
        if free(x, z, 3.0, 5.0):
            well_ok = put(P, 'A98_well', x, z, 0, 'CastleProps', scale=1.2); n['props'] += 1 if well_ok else 0
            if well_ok:
                break
    for (cx, cz, ang) in ((0, -2120, 180), (0, -2160, 0), (-24, -2140, 90), (24, -2140, 270)):
        if free(cx, cz, 2.0, 3.0):
            if put(P, choose(W(('A83_bench_stone', 1), ('K33_ornate_bench', 1))), cx, cz, ang, 'CastleProps', scale=1.0):
                n['props'] += 1
    for (cx, cz) in ((-186, -2045), (186, -2045), (-186, -2330), (186, -2330), (-150, -2060), (150, -2060), (-120, -2250), (120, -2250)):
        for k in range(rng.randint(2, 4)):
            x, z = cx + rng.uniform(-9, 9), cz + rng.uniform(-9, 9)
            if free(x, z, 1.5, 3.0):
                m = choose(W(('A71_barrel', 1.2), ('A74_crate_large', 1.0), ('A75_crate_stack', 0.5), ('A73_crate_small', 0.8), ('A78_hay_bale', 0.4)))
                if put(P, m, x, z, rng.uniform(0, 360), 'CastleProps', scale=rng.uniform(0.9, 1.15)):
                    n['props'] += 1
    for (x, z, m, rot) in ((100, -2175, 'A79_hand_cart', 20), (-46, -2215, 'A80_wagon', 80), (130, -2190, 'A97_water_trough', 0), (-128, -2065, 'A97_water_trough', 0)):
        if free(x, z, 2.0, 3.0):
            if put(P, m, x, z, rot, 'CastleProps'):
                n['props'] += 1
    # market stalls: V4 stalls in two short rows near the avenue
    for (x, z, rot) in ((-48, -2062, 180), (-72, -2062, 180), (48, -2062, 180), (72, -2062, 180), (-48, -2185, 0), (48, -2185, 0)):
        if free(x, z, 2.0, 3.0):
            if put(P, choose(W(('B06_01_stall_fruit', 1), ('B06_02_stall_cloth', 1), ('B06_03_stall_potion', 1))), x, z, rot, 'CastleStalls', scale=1.0):
                n['stalls'] += 1
    # training yard fence (rectangle x -141..-69, z -2222..-2172); east side keeps a gate gap in the middle
    FX0, FX1, FZ0, FZ1 = -141.0, -69.0, -2222.0, -2172.0
    for k in range(6):
        x = FX0 + 6.0 + k * 12.0
        for z in (FZ0, FZ1):
            if put(P, 'A100_fence_picket', x, z, 0, 'CastleYardFence', scale=0.96, reg=False):
                n['fence'] += 1
    for k in range(4):
        z = FZ0 + 6.25 + k * 12.5
        if put(P, 'A100_fence_picket', FX0, z, 90, 'CastleYardFence', scale=1.0, reg=False):
            n['fence'] += 1
        if k not in (1, 2):
            if put(P, 'A100_fence_picket', FX1, z, 90, 'CastleYardFence', scale=1.0, reg=False):
                n['fence'] += 1
    add_occ(-105, -2197, 38, 28)
    # banners flanking the way to the keep
    for sx in (-1, 1):
        for z in (-2075, -2120, -2165, -2215):
            x = sx * 23
            if free(x, z, 1.0, 1.0):
                if put(P, 'B05_05_royal_banner', x, z, 90 if sx < 0 else 270, 'CastleBanners', scale=0.85):
                    n['banners'] += 1
    # outside the walls
    n['outer'] += wall_ring(P, (-200, 200, -2350, -2018), (), 8, 22, 12, 'CastleOuter', trees_every=6, gates=[(0, -2018, 60)])
    return n


# ============================================================ CAPITAL
def capital():
    P = 'v4_dress_capital'
    n = collections.Counter()
    sp = Spacing(30)
    n['trees'] = scatter(80, (-470, 470, -1910, -1262), sp, lambda x, z: free(x, z, 7.0, 9.0) and abs(x) > 9,
                         lambda x, z: put(P, choose(TREES_TOWN), x, z, rng.uniform(0, 360), 'TreesCapital', scale=rng.uniform(0.6, 0.85)))
    sp2 = Spacing(14)
    n['beds'] = scatter(120, (-470, 470, -1910, -1262), sp2, lambda x, z: free(x, z, 3.0, 6.0),
                        lambda x, z: put(P, choose(FLOWERS if rng.random() < 0.5 else BUSHES), x, z, rng.uniform(0, 360), 'CapitalBeds', scale=rng.uniform(0.9, 1.3)))
    n['seam'] = wall_ring(P, (-490, 490, -1934, -1237), (), 7, 20, 11, 'CapitalWall', trees_every=8, gates=[(0, -1237, 55), (0, -1934, 55)])
    # stalls and a well on the two avenue plazas
    for (x, z, rot) in ((-46, -1275, 180), (46, -1275, 180), (-70, -1290, 180), (70, -1290, 180), (-46, -1895, 0), (46, -1895, 0)):
        if free(x, z, 2.0, 4.0):
            if put(P, choose(W(('B06_01_stall_fruit', 1), ('B06_02_stall_cloth', 1), ('B06_03_stall_potion', 1))), x, z, rot, 'CapitalStalls', scale=1.0):
                n['stalls'] += 1
    return n


# ============================================================ HARBOUR
def shoreline_points(box, spacing, inland_lo, inland_hi):
    """points just landward of the waterline inside box=(x0,x1,z0,z1)"""
    segs = json.load(open(V4 + r'\foam_segments.json'))['segments']
    pts = []
    for s in segs:
        mx, mz = (s[0] + s[2]) / 2, (s[1] + s[3]) / 2
        if not (box[0] <= mx <= box[1] and box[2] <= mz <= box[3]):
            continue
        dx, dz = s[2] - s[0], s[3] - s[1]
        L = math.hypot(dx, dz)
        if L < 1:
            continue
        nx, nz = -dz / L, dx / L
        if E.H(mx + nx * 12, mz + nz * 12) < E.H(mx - nx * 12, mz - nz * 12):
            nx, nz = -nx, -nz
        d = rng.uniform(inland_lo, inland_hi)
        pts.append((mx + nx * d, mz + nz * d, math.degrees(math.atan2(nx, nz))))
    rng.shuffle(pts)
    out, sp = [], Spacing(spacing)
    for (x, z, a) in pts:
        if sp.ok(x, z):
            sp.add(x, z)
            out.append((x, z, a))
    return out


def harbour():
    P = 'v4_dress_harbour'
    n = collections.Counter()
    sp = Spacing(28)
    n['trees'] = scatter(34, (-760, -40, 1380, 1650), sp, lambda x, z: free(x, z, 7.0, 8.0),
                         lambda x, z: put(P, choose(TREES_TOWN + W(('F04_01_tree_coastal_01', 1.0), ('F04_02_tree_coastal_02', 1.0))), x, z, rng.uniform(0, 360), 'TreesHarbour', scale=rng.uniform(0.7, 1.0)))
    sp2 = Spacing(13)
    n['beds'] = scatter(90, (-760, -40, 1380, 1700), sp2, lambda x, z: free(x, z, 3.0, 6.0),
                        lambda x, z: put(P, choose(BUSHES if rng.random() < 0.55 else FLOWERS), x, z, rng.uniform(0, 360), 'HarbourBeds', scale=rng.uniform(0.9, 1.3)))
    for (x, z, a) in shoreline_points((-1100, 380, 1650, 2150), 16, 3, 12):
        if not free(x, z, 3.0, 6.0, minh=0.8):
            continue
        m = choose(W(('F05_11_sea_oats', 1.4), ('F05_12_dune_tuft', 1.4), ('F10_08_driftwood_pile', 0.5), ('A55_pebbles', 0.7), ('A56_rock_small_1', 0.5), ('E15_01_boulder_01', 0.3), ('F10_10_beach_fishing_gear', 0.25)))
        if put(P, m, x, z, rng.uniform(0, 360), 'HarbourBeach', scale=rng.uniform(0.9, 1.5)):
            n['beach'] += 1
    # quay life: net racks, barrels, crates, fish stalls (quay centre around z=1808)
    for k in range(40):
        x, z = rng.uniform(-600, -180), rng.uniform(1780, 1815)
        if free(x, z, 2.0, 3.0, minh=1.0):
            m = choose(W(('A71_barrel', 1.4), ('A74_crate_large', 1.0), ('A75_crate_stack', 0.4), ('G17_net_rack', 0.5), ('G15_fish_market_stall', 0.25), ('A72_barrel_open', 0.4)))
            if put(P, m, x, z, rng.uniform(0, 360) if m not in ('G17_net_rack', 'G15_fish_market_stall') else 0, 'HarbourQuay', scale=rng.uniform(0.9, 1.1)):
                n['quay'] += 1
    return n


# ============================================================ RUSTY TOWN
def rusty():
    P = 'v4_dress_rusty'
    n = collections.Counter()
    sp = Spacing(15)
    MODELS = W(('E15_01_boulder_01', 0.6), ('E15_02_boulder_02', 0.6), ('A58_rock_medium_1', 0.5), ('A57_rock_small_2', 0.6), ('E05_01_dead_tree_01', 0.35), ('E05_03_dead_tree_03', 0.35),
               ('E05_05_dead_tree_05', 0.3), ('F03_01_tree_dry_01', 0.3), ('F03_02_tree_dry_02', 0.3), ('F05_12_dune_tuft', 1.0), ('E06_02_rusty_debris_02', 0.5), ('E06_05_rusty_debris_05', 0.5),
               ('E06_09_rusty_debris_09', 0.4), ('D29_patched_tent', 0.12), ('D31_rusted_cart', 0.12), ('D32_broken_barrel', 0.25), ('A74_crate_large', 0.2), ('A71_barrel', 0.3), ('E07_05_rusty_prop_05', 0.2),
               ('D33_broken_fence', 0.1), ('A78_hay_bale', 0.12))
    n['all'] = scatter(190, (1000, 1520, 880, 1330), sp, lambda x, z: free(x, z, 4.0, 7.0) and E.town_mask(x, z) > 0.0,
                       lambda x, z: put(P, choose(MODELS), x, z, rng.uniform(0, 360), 'RustyDressing', scale=rng.uniform(0.9, 1.5)))
    return n


# ============================================================ ALPINE ICE LAKE RIM
def alpine():
    P = 'v4_dress_alpine'
    n = collections.Counter()
    L = {'cx': 1490, 'cz': -1080, 'rx': 170, 'rz': 108}
    sp = Spacing(10)
    MODELS = W(('C05_01_ice_block_01', 0.6), ('C05_02_ice_block_02', 0.5), ('C05_03_ice_block_03', 0.5), ('E15_01_boulder_01', 0.7), ('E15_03_boulder_03', 0.7), ('F06_10_scree_chips', 0.6),
               ('C10_01_snow_pine_01', 0.45), ('C10_03_snow_pine_03', 0.45), ('C10_04_snow_pine_04', 0.5), ('A56_rock_small_1', 0.5))
    for k in range(240):
        a = rng.uniform(0, math.tau)
        rr = rng.uniform(1.03, 1.20)
        x, z = L['cx'] + math.cos(a) * L['rx'] * rr, L['cz'] + math.sin(a) * L['rz'] * rr
        if not sp.ok(x, z) or E.H(x, z) < 100:
            continue
        if E.occupied(x, z, 3.0) or E.ROADS.dist(x, z) < 5:
            continue
        if put(P, choose(MODELS), x, z, rng.uniform(0, 360), 'IceRim', scale=rng.uniform(0.9, 1.5)):
            sp.add(x, z); n['rim'] += 1
        if n['rim'] >= 110:
            break
    return n


# ============================================================ ELF POOLS
def elf():
    P = 'v4_dress_elf'
    n = collections.Counter()
    pools = [(-1660, -640, 80, 62), (-1440, -250, 40, 32)]
    sp = Spacing(7)
    RIM = W(('F05_07_reed_clump', 1.4), ('F05_08_reed_stand', 1.0), ('A52_reeds', 0.8), ('D06_01_fern_a', 1.0), ('D06_02_fern_b', 0.9), ('D06_10_moss_rock_a', 0.5), ('D06_11_moss_rock_b', 0.5),
            ('D06_04_bush_a', 0.7), ('D06_07_flower_a', 0.7), ('F06_09_pebbles_river', 0.6))
    for (cx, cz, rx, rz) in pools:
        want = int((rx + rz) / 3.4)
        got = 0
        for k in range(want * 12):
            if got >= want:
                break
            a = rng.uniform(0, math.tau)
            rr = rng.uniform(1.0, 1.22)
            x, z = cx + math.cos(a) * rx * rr, cz + math.sin(a) * rz * rr
            if not sp.ok(x, z) or E.occupied(x, z, 2.0) or E.ROADS.dist(x, z) < 3:
                continue
            if put(P, choose(RIM), x, z, rng.uniform(0, 360), 'ElfRim', scale=rng.uniform(0.9, 1.4)):
                sp.add(x, z); got += 1
        n['rim'] += got
        for k in range(int(rx / 8)):
            a = rng.uniform(0, math.tau)
            rr = rng.uniform(0.2, 0.8)
            x, z = cx + math.cos(a) * rx * rr, cz + math.sin(a) * rz * rr
            if put(P, choose(W(('F10_01_lily_pad_cluster', 1.2), ('F10_02_lily_pad_spread', 0.8))), x, z, rng.uniform(0, 360), 'ElfLily', scale=rng.uniform(0.9, 1.4), yo=0.15, reg=False):
                n['lily'] += 1
    # sandy clearings around the world tree: ferns, bushes, flowers
    sp2 = Spacing(11)
    FILL = W(('D06_01_fern_a', 1.2), ('D06_02_fern_b', 1.0), ('D06_03_fern_c', 0.7), ('D06_04_bush_a', 0.8), ('D06_05_bush_b', 0.8), ('D06_07_flower_a', 0.6), ('D06_08_flower_b', 0.6), ('D06_18_mushroom_a', 0.3))
    n['clear'] = scatter(70, (-1700, -1420, -560, -300), sp2, lambda x, z: free(x, z, 4.0, 4.0) and 55 < math.hypot(x + 1560, z + 430) < 150,
                         lambda x, z: put(P, choose(FILL), x, z, rng.uniform(0, 360), 'ElfClearing', scale=rng.uniform(0.9, 1.3)))
    return n


# ============================================================ TOWN 1 (light touch)
def town1():
    P = 'town1_dress'
    n = collections.Counter()
    # skull apron ring
    cx, cz = 0, -402
    for k in range(70):
        a = rng.uniform(0, math.tau)
        r = rng.uniform(112, 134)
        x, z = cx + math.sin(a) * r, cz + math.cos(a) * r
        # keep the southern approach (towards +z) and the cliff-free front clear
        if abs(a - 0.0) < 0.32 or abs(a - math.tau) < 0.32:
            continue
        if not free(x, z, 3.0, 6.0, minh=-5) or E.M(x, z) not in ('G', 'L', 'D', 'R'):
            continue
        r2 = rng.random()
        if r2 < 0.45:
            m, sc = choose(BUSHES), rng.uniform(1.1, 1.8)
        elif r2 < 0.75:
            m, sc = choose(ROCKS), rng.uniform(1.3, 2.4)
        else:
            m, sc = choose(TUFTS), rng.uniform(1.0, 1.6)
        if put(P, m, x, z, rng.uniform(0, 360), 'T1ApronRing', scale=sc):
            n['apron'] += 1
    # graveyard feather: bounding box of the graveyard footprints
    pts = []
    for f in ('occ_town1_graveyard.json', 'occ_town1_gy2.json'):
        pts += json.load(open(V4 + '\\' + f))
    if pts:
        x0 = min(p[0] - p[2] for p in pts); x1 = max(p[0] + p[2] for p in pts)
        z0 = min(p[1] - p[3] for p in pts); z1 = max(p[1] + p[3] for p in pts)
        n['gy_box'] = int(x1 - x0) * 10000 + int(z1 - z0)
        sp = Spacing(9)
        for k in range(500):
            side = rng.randint(0, 3)
            t = rng.random()
            off = rng.uniform(4, 13)
            if side == 0:
                x, z = x0 + t * (x1 - x0), z0 - off
            elif side == 1:
                x, z = x0 + t * (x1 - x0), z1 + off
            elif side == 2:
                x, z = x0 - off, z0 + t * (z1 - z0)
            else:
                x, z = x1 + off, z0 + t * (z1 - z0)
            if not sp.ok(x, z) or not free(x, z, 2.5, 5.0, minh=-5):
                continue
            m = choose(W(('A56_rock_small_1', 1.0), ('A57_rock_small_2', 1.0), ('E15_02_boulder_02', 0.6), ('A35_dead_tree_1', 0.3), ('A36_dead_tree_2', 0.3), ('F05_04_bush_juniper', 0.8), ('A49_tall_grass_1', 0.8), ('A50_tall_grass_2', 0.8)))
            if put(P, m, x, z, rng.uniform(0, 360), 'T1GraveyardEdge', scale=rng.uniform(0.9, 1.5)):
                sp.add(x, z); n['gy'] += 1
            if n['gy'] >= 60:
                break
    return n


if __name__ == '__main__':
    results = {}
    for name, fn in (('castle', castle), ('capital', capital), ('harbour', harbour), ('rusty', rusty), ('alpine', alpine), ('elf', elf), ('town1', town1)):
        results[name] = dict(fn())
        print(name, results[name])
    MP = TOWN + r'\mapplan'
    for plan, items in E.OUT.items():
        json.dump({'area': plan, 'terrain': [], 'placements': items}, open(MP + '\\' + plan + '.json', 'w'))
        print(plan, len(items), 'items;', 'groups:', dict(collections.Counter(i['group'] for i in items)))
    print('placed per plan:', dict(PLACED))
    print('REJECTED (model not uploaded / typo):', dict(REJ))

