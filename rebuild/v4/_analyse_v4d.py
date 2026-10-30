"""analysis for terrain v4d: material usage, warm ground outside the dry biome, part counts per species. Read-only."""
import json, re, glob, os, collections, math

RB = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
V4 = RB + r'\v4'
TOWN = r'C:\Users\Nitro\.kiro\crew\workspace\town'

# 1. where do my scripts use these terrain materials?
mats = ['Basalt', 'Asphalt', 'Mud', 'Limestone', 'Concrete', 'Brick', 'WoodPlanks', 'Glacier', 'Salt']
hits = collections.defaultdict(list)
for root in (RB, TOWN + r'\tools_v3', TOWN + r'\mapplan'):
    for p in glob.glob(root + r'\**\*', recursive=True):
        if os.path.isfile(p) and p.endswith(('.luau', '.lua', '.py', '.ps1')) and 'world_v3' not in p and '__pycache__' not in p:
            try:
                t = open(p, encoding='utf-8', errors='ignore').read()
            except Exception:
                continue
            for m in mats:
                n = len(re.findall(r'\b' + m + r'\b', t))
                if n:
                    hits[m].append((os.path.basename(p), n))
for m in mats:
    print(m, '->', ', '.join('%s x%d' % h for h in hits[m][:9]) or '(unused)')

# 2. terrain map char legend + warm ground
export = open(V4 + r'\export_map.luau', encoding='utf-8').read()
leg = re.findall(r"\[Enum\.Material\.(\w+)\]\s*=\s*'(.)'", export)
print('legend', leg)
TM = json.load(open(V4 + r'\terrain_map.json'))
X0, Z0, STEP = TM['x0'], TM['z0'], TM['step']
rows = TM['rows']
W = json.load(open(RB + r'\world.json'))
code2mat = {c: m for m, c in leg}
warm = collections.Counter()
cells = collections.defaultdict(list)
for j, row in enumerate(rows):
    for i in range(len(row) // 5):
        c = row[i * 5:i * 5 + 5]
        ch = c[2]
        mname = code2mat.get(ch, ch)
        if mname in ('Ground', 'Sandstone', 'Salt', 'Mud'):
            x, z = X0 + i * STEP, Z0 + j * STEP
            h = int(c[0:2], 36) - 100
            if h > 3:
                cells[mname].append((x, z))
for k, v in cells.items():
    print(k, 'cells above water:', len(v))
# warm cells outside every dry biome centre region (distance > 0.9 r)
dry = [b for b in W['biomes'] if b[0] == 'dry']
out = []
for k in ('Ground', 'Sandstone', 'Salt'):
    for (x, z) in cells[k]:
        if not any(math.hypot(x - b[1], z - b[2]) < b[3] * 1.0 for b in dry):
            out.append((k, x, z))
print('warm cells outside dry biomes:', len(out))
bins = collections.Counter((k, round(x / 300) * 300, round(z / 300) * 300) for k, x, z in out)
for key, n in bins.most_common(14):
    print('  ', key, n)
near_castle = [(k, x, z) for k, x, z in out if -300 < x < 400 and -2700 < z < -2300]
print('warm cells near castle back:', len(near_castle), near_castle[:6])

# 3. part counts per species
cat = {}
try:
    for c in json.load(open(TOWN + r'\mapplan\catalog.json', encoding='utf-8-sig')):
        cat[c['id']] = len(c.get('pieces') or [])
except Exception as e:
    print('catalog err', e)
meta = json.load(open(TOWN + r'\library\v4_meta.json'))
for k, v in meta.items():
    cat[k] = len(v.get('materials') or [])
cnt = collections.Counter()
for plan in ('v4_forest', 'v4_under', 'v4_rocks'):
    d = json.load(open(TOWN + r'\mapplan\%s.json' % plan))
    cnt2 = collections.Counter(p['model'] for p in d['placements'])
    for m, n in cnt2.items():
        cnt[(plan, m)] = n
tot = collections.defaultdict(int)
for (plan, m), n in cnt.most_common(40):
    print('%-10s %-34s models %5d  pieces/model %s' % (plan, m, n, cat.get(m, '?')))
