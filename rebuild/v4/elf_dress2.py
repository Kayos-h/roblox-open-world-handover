"""elf_dress2.py - second dressing pass for the elf village (round-3 review: dark, bare core lawn, hard path edges, hard pool rims, flat palace pad, only 5.5/10).
Writes mapplan/v4_dress_elf2.json. Natural look only: no Neon, no lights, no particles. Place with build_v4.ps1 -area v4_dress_elf2 -nocollide ElfFill,ElfEdge,ElfRim2,ElfPlaza.
"""
import sys, json, math, random, collections
V4 = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4'
TOWN = r'C:\Users\Nitro\.kiro\crew\workspace\town'
sys.path.insert(0, V4)
import env_plan as E

E.load_occupancy()
rng = random.Random(1717)
OB = E.OBUCK


def add_occ(x, z, hx, hz):
    for bi in range(int((x - hx) // OB), int((x + hx) // OB) + 1):
        for bj in range(int((z - hz) // OB), int((z + hz) // OB) + 1):
            E.OCC.setdefault((bi, bj), []).append((x, z, hx, hz))


for (x, z, hx, hz, name) in json.load(open(V4 + r'\enterable_fp.json')):
    add_occ(x, z, hx + 6, hz + 6)
# the dress pass 1 items for the elf valley (already placed) block too
for it in json.load(open(TOWN + r'\mapplan\v4_dress_elf.json'))['placements']:
    add_occ(it['x'], it['z'], 2.5, 2.5)

SZ = {}
for k, v in json.load(open(TOWN + r'\library\v4_meta.json')).items():
    SZ[k] = (v['size'][0], v['size'][1])
for e in json.load(open(TOWN + r'\mapplan\catalog.json', encoding='utf-8-sig')):
    SZ[e['id']] = (e['size_x'], e['size_z'])
P = 'v4_dress_elf2'
cnt = collections.Counter()


def put(model, x, z, rot, group, scale=1.0, reg=True, yo=None):
    if model is None or model not in E.IDS:
        return False
    if not E.put(P, model, x, z, rot, group, scale=scale, yo=yo):
        return False
    cnt[group] += 1
    if reg:
        sx, sz = SZ.get(model, (4, 4))
        r = max(sx, sz) * scale * 0.4
        add_occ(x, z, r, r)
    return True


def ok(x, z, margin=3.0, road=2.5):
    return E.in_map(x, z) and E.H(x, z) > 3 and not E.has_water(x, z) and not E.in_lake(x, z, 1.02) and not E.occupied(x, z, margin) and E.ROADS.dist(x, z) > road


def choose(lst):
    names = [n for n, w in lst if n in E.IDS]
    wts = [w for n, w in lst if n in E.IDS]
    return rng.choices(names, wts)[0] if names else None


def W(*p):
    return list(p)


class Sp:
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


FILL = W(('D06_01_fern_a', 1.3), ('D06_02_fern_b', 1.1), ('D06_03_fern_c', 0.8), ('D06_04_bush_a', 0.9), ('D06_05_bush_b', 0.9), ('D06_06_bush_c', 0.8), ('D06_07_flower_a', 0.9),
         ('D06_08_flower_b', 0.8), ('D06_09_flower_c', 0.8), ('D06_18_mushroom_a', 0.35), ('D06_19_mushroom_b', 0.3), ('F06_19_flowers_wild', 0.8), ('F06_16_flowers_buttercup', 0.5))
STALLS = ['D04_08_stall_a', 'D04_09_stall_b', 'D04_10_stall_c']

# --- 1. the bare lawn around the world tree (65..175 studs): beds, bushes, ferns, benches of moss rock, a few saplings
sp = Sp(9)
want = 190
got = 0
for _ in range(want * 40):
    if got >= want:
        break
    a = rng.uniform(0, math.tau)
    r = rng.uniform(62, 175)
    x, z = -1560 + math.cos(a) * r, -430 + math.sin(a) * r * 0.9
    if not sp.ok(x, z) or not ok(x, z, 3.0, 4.5):
        continue
    if put(choose(FILL), x, z, rng.uniform(0, 360), 'ElfFill', scale=rng.uniform(0.9, 1.5)):
        sp.add(x, z); got += 1
# saplings and moss rocks: scattered accents
sp2 = Sp(26)
for _ in range(900):
    if cnt['ElfAccent'] >= 26:
        break
    a = rng.uniform(0, math.tau)
    r = rng.uniform(75, 180)
    x, z = -1560 + math.cos(a) * r, -430 + math.sin(a) * r * 0.9
    if sp2.ok(x, z) and ok(x, z, 4.0, 5.0):
        if put(choose(W(('D05_18_sapling', 1.2), ('D06_10_moss_rock_a', 0.8), ('D06_11_moss_rock_b', 0.8), ('D06_12_moss_rock_c', 0.6), ('D05_14_stump_c', 0.4), ('D05_15_log_a', 0.4))), x, z, rng.uniform(0, 360), 'ElfAccent', scale=rng.uniform(0.9, 1.3)):
            sp2.add(x, z)

# --- 2. edges of the dirt paths (soften the hard strips): small plants on both sides, 4-9 studs from the centre line
streets = json.load(open(V4 + r'\elf_streets.json'))
sp3 = Sp(6)
for s in streets:
    pts = s['pts']
    for i in range(len(pts) - 1):
        ax, az, bx, bz = pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]
        L = math.hypot(bx - ax, bz - az)
        if L < 1:
            continue
        nx, nz = -(bz - az) / L, (bx - ax) / L
        n = int(L / 6)
        for k in range(n + 1):
            t = k / max(1, n)
            for side in (-1, 1):
                off = s['w'] + rng.uniform(1.2, 5.5)
                x = ax + (bx - ax) * t + nx * off * side + rng.uniform(-1.5, 1.5)
                z = az + (bz - az) * t + nz * off * side + rng.uniform(-1.5, 1.5)
                if rng.random() < 0.55 and sp3.ok(x, z) and E.in_map(x, z) and not E.has_water(x, z) and not E.occupied(x, z, 1.6):
                    if put(choose(W(('D06_01_fern_a', 1.0), ('D06_02_fern_b', 1.0), ('D06_07_flower_a', 0.9), ('D06_08_flower_b', 0.9), ('D06_09_flower_c', 0.8), ('D06_05_bush_b', 0.5))), x, z, rng.uniform(0, 360), 'ElfEdge', scale=rng.uniform(0.8, 1.2), reg=False):
                        sp3.add(x, z)

# --- 3. pools: the elf lake (-1660,-640 r 80x62), the pond (-1440,-250 r 40x32), the moon pool (-1570,-615): reeds + ferns + stones around, 2 rings
sp4 = Sp(5)
for (cx, cz, rx, rz) in ((-1660, -640, 80, 62), (-1440, -250, 40, 32), (-1570, -615, 22, 22)):
    for ring in (1.08, 1.22, 1.38):
        n = int((rx + rz) * ring / 4.2)
        for k in range(n):
            a = rng.uniform(0, math.tau)
            x, z = cx + math.cos(a) * rx * ring, cz + math.sin(a) * rz * ring
            if not sp4.ok(x, z) or E.occupied(x, z, 1.8) or E.has_water(x, z) or E.ROADS.dist(x, z) < 2.0:
                continue
            pool = W(('F05_07_reed_clump', 1.4), ('F05_08_reed_stand', 1.0), ('D06_01_fern_a', 1.0), ('D06_03_fern_c', 0.7), ('D06_10_moss_rock_a', 0.6), ('D06_11_moss_rock_b', 0.6), ('F06_09_pebbles_river', 0.6), ('D06_05_bush_b', 0.5))
            if ring > 1.3:
                pool = W(('D06_01_fern_a', 1.0), ('D06_04_bush_a', 0.8), ('D06_07_flower_a', 0.7), ('D06_12_moss_rock_c', 0.6))
            if put(choose(pool), x, z, rng.uniform(0, 360), 'ElfRim2', scale=rng.uniform(0.9, 1.4), reg=False):
                sp4.add(x, z)

# --- 4. palace plaza (-1470,-655): feather the pad edge with beds, add benches (moss stone) and unlit braziers is NOT allowed (no glow) -> planters of ferns and 4 stone markers
sp5 = Sp(7)
for k in range(70):
    a = rng.uniform(0, math.tau)
    r = rng.uniform(52, 82)
    x, z = -1470 + math.cos(a) * r * 1.25, -655 + math.sin(a) * r
    if sp5.ok(x, z) and ok(x, z, 2.5, 3.0):
        if put(choose(W(('D06_04_bush_a', 1.0), ('D06_05_bush_b', 1.0), ('D06_01_fern_a', 1.0), ('D06_07_flower_a', 0.8), ('D06_10_moss_rock_a', 0.5))), x, z, rng.uniform(0, 360), 'ElfPlaza', scale=rng.uniform(1.0, 1.5)):
            sp5.add(x, z)
for k in range(4):
    a = k * math.pi / 2 + math.pi / 4
    x, z = -1470 + math.cos(a) * 46, -655 + math.sin(a) * 40
    if ok(x, z, 1.5, 2.0):
        put('D08_08_marker_a' if k % 2 == 0 else 'D08_09_marker_b', x, z, rng.uniform(0, 360), 'ElfPlaza', scale=1.2)

# --- 5. a small market on the east side of the tree ring, built from the V4 elf stalls
for (x, z, rot) in ((-1425, -455, 270), (-1425, -478, 270), (-1425, -402, 270), (-1425, -380, 270), (-1655, -380, 90), (-1655, -402, 90)):
    if ok(x, z, 2.0, 2.0):
        put(rng.choice(STALLS), x, z, rot, 'ElfPlaza', scale=1.0)

json.dump({'area': P, 'terrain': [], 'placements': E.OUT[P]}, open(TOWN + r'\mapplan\%s.json' % P, 'w'))
print(P, len(E.OUT[P]), 'items', dict(cnt))
