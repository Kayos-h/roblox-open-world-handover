"""elf_city.py - more elf houses so the valley reads as a city, plus planting around the pavilion. Writes mapplan/v4_dress_elf3.json.
Houses face the world tree (-1560,-430) (rot 0 = door on +Z). No glow of any kind.
"""
import sys, json, math, random, collections
V4 = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4'
TOWN = r'C:\Users\Nitro\.kiro\crew\workspace\town'
sys.path.insert(0, V4)
sys.path.insert(0, TOWN + r'\rebuild')
import env_plan as E
from layout_lib import face_rot

E.load_occupancy()
rng = random.Random(4711)
OB = E.OBUCK


def add_occ(x, z, hx, hz):
    for bi in range(int((x - hx) // OB), int((x + hx) // OB) + 1):
        for bj in range(int((z - hz) // OB), int((z + hz) // OB) + 1):
            E.OCC.setdefault((bi, bj), []).append((x, z, hx, hz))


for (x, z, hx, hz, name) in json.load(open(V4 + r'\enterable_fp.json')):
    add_occ(x, z, hx + 6, hz + 6)
for plan in ('v4_dress_elf', 'v4_dress_elf2'):
    for it in json.load(open(TOWN + r'\mapplan\%s.json' % plan))['placements']:
        add_occ(it['x'], it['z'], 2.0, 2.0)

SZ = {}
for k, v in json.load(open(TOWN + r'\library\v4_meta.json')).items():
    SZ[k] = (v['size'][0], v['size'][1])
P = 'v4_dress_elf3'
cnt = collections.Counter()
CX, CZ = -1560.0, -430.0


def place(model, x, z, rot, group, scale):
    if model not in E.IDS:
        return False
    if not E.put(P, model, x, z, rot, group, scale=scale):
        return False
    sx, sz = SZ.get(model, (20, 20))
    r = max(sx, sz) * scale * 0.52
    add_occ(x, z, r, r)
    cnt[group] += 1
    return True


def slope_ok(x, z, lim=0.28):
    return E.slope(x, z) < lim


def free(x, z, margin):
    # the world tree canopy and roots (two huge footprints at the trunk) are ignored: only the trunk disc itself (radius 34) blocks
    if math.hypot(x - CX, z - CZ) < 40:
        return False
    if not (E.in_map(x, z) and E.H(x, z) > 3 and not E.has_water(x, z) and not E.in_lake(x, z, 1.15) and E.ROADS.dist(x, z) > 5.5):
        return False
    for (cx, cz, hx, hz) in E.OCC.get((int(x // OB), int(z // OB)), ()):
        if hx > 60 or hz > 60:
            continue
        if abs(x - cx) <= hx + margin and abs(z - cz) <= hz + margin:
            return False
    return True


HOUSES = ['D04_01_round_house_a', 'D04_02_round_house_b', 'D04_03_round_house_c']
# ring of houses around the world tree: radius 92..140, angle sweep every ~22 degrees with jitter
tries = 0
for k in range(30):
    ang = math.radians(k * 12 + rng.uniform(-4, 4))
    for attempt in range(16):
        r = rng.uniform(112, 230)
        x, z = CX + math.cos(ang) * r, CZ + math.sin(ang) * r * 0.92
        if free(x, z, 10.0) and slope_ok(x, z):
            rot = face_rot(CX - x, CZ - z) + rng.uniform(-8, 8)
            if place(rng.choice(HOUSES), x, z, rot, 'ElfHouses', rng.uniform(0.92, 1.12)):
                break
        tries += 1
# second tiny treehouse cluster on the east side (the layout was west-heavy)
TH = ['D01_03_treehouse_c', 'D01_05_treehouse_e', 'D01_01_treehouse_a']
placed_th = 0
for (x, z) in ((-1405, -470), (-1385, -395), (-1430, -520), (-1380, -440), (-1420, -355)):
    if placed_th >= 3:
        break
    if free(x, z, 14.0) and slope_ok(x, z, 0.35):
        if place(TH[placed_th % 3], x, z, face_rot(CX - x, CZ - z) + rng.uniform(-12, 12), 'ElfTreehouses', rng.uniform(0.9, 1.05)):
            placed_th += 1
# planting around the pavilion at (-1722,-528)
FILL = ['D06_04_bush_a', 'D06_05_bush_b', 'D06_01_fern_a', 'D06_02_fern_b', 'D06_07_flower_a', 'D06_08_flower_b', 'D06_10_moss_rock_a']
for k in range(34):
    a = rng.uniform(0, math.tau)
    r = rng.uniform(26, 46)
    x, z = -1722 + math.cos(a) * r, -528 + math.sin(a) * r
    if free(x, z, 3.0):
        place(rng.choice(FILL), x, z, rng.uniform(0, 360), 'ElfPavilionBeds', rng.uniform(1.0, 1.5))
json.dump({'area': P, 'terrain': [], 'placements': E.OUT[P]}, open(TOWN + r'\mapplan\%s.json' % P, 'w'))
print(P, len(E.OUT[P]), 'items', dict(cnt), '| house attempts that missed:', tries)

