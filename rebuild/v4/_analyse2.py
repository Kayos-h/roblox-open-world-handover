import json, math, collections
RB = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
TM = json.load(open(RB + r'\v4\terrain_map.json'))
W = json.load(open(RB + r'\world.json'))
X0, Z0, STEP = TM['x0'], TM['z0'], TM['step']
NAME = {'G': 'Grass', 'L': 'LeafyGrass', 'S': 'Sand', 'M': 'Mud', 'R': 'Rock', 'T': 'Slate', 'B': 'Basalt', 'N': 'Snow', 'I': 'Ice', 'D': 'Ground',
        'A': 'Sandstone', 'C': 'Cobblestone', 'P': 'Pavement', 'K': 'Limestone', 'H': 'Salt'}
rows = TM['rows']
cells = collections.defaultdict(list)
tot = collections.Counter()
for j, row in enumerate(rows):
    for i in range(len(row) // 5):
        c = row[i * 5:i * 5 + 5]
        h = int(c[0:2], 36) - 100
        if h < 3:
            continue
        ch = c[2]
        x, z = X0 + i * STEP, Z0 + j * STEP
        cells[ch].append((x, z, h))
        tot[NAME.get(ch, ch)] += 1
print('land cells (24-stud grid):', dict(tot.most_common()))
dry = [b for b in W['biomes'] if b[0] == 'dry']
def indry(x, z): return any(math.hypot(x - b[1], z - b[2]) < b[3] for b in dry)
for ch in ('D', 'A', 'H', 'M'):
    out = [(x, z, h) for (x, z, h) in cells[ch] if not indry(x, z)]
    bins = collections.Counter((round(x / 200) * 200, round(z / 200) * 200) for x, z, h in out)
    print(NAME[ch], 'cells outside dry biomes:', len(out), 'top bins', bins.most_common(8))
cx = [(NAME.get(ch), x, z, h) for ch in ('D', 'A', 'H', 'M', 'R', 'T') for (x, z, h) in cells[ch] if -250 < x < 450 and -2750 < z < -2330]
print('cells in the castle-back window by material:', collections.Counter(c[0] for c in cx))
for ch in ('D', 'A', 'H'):
    sub = [(x, z, h) for (x, z, h) in cells[ch] if -250 < x < 450 and -2750 < z < -2330]
    print(NAME[ch], 'in window:', sub[:8])
