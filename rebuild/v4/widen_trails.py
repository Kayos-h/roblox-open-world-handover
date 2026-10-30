"""World tweaks for terrain v4d (materials and widths only, NO height changes, so placed objects stay valid).
 - rural main roads: Cobblestone -> Limestone (warm tan, readable from above); the two ring roads stay Ground
 - rural trails: half width 2.6 -> 4.5 (9 studs), bank 10
Idempotent: always starts from the v4c backup rebuild/v4/world_v4c.json.
"""
import json, os, shutil
RB = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
bak = RB + r'\v4\world_v4c.json'
if not os.path.exists(bak):
    shutil.copy(RB + r'\world.json', bak)
w = json.load(open(bak))
roads = 0
for r in w['roads']:
    if r['name'] in ('north', 'east', 'west', 'south', 'southeast', 'lake_path'):
        r['mat'] = 'Limestone'
        roads += 1
trails = 0
for s in w['streets']:
    if str(s.get('name', '')).startswith('trail_'):
        s['w'] = 4.5
        s['bank'] = 10
        trails += 1
json.dump(w, open(RB + r'\world.json', 'w'), separators=(',', ':'))
json.dump(w, open(RB + r'\v4\world_v4.json', 'w'), separators=(',', ':'))
print('roads -> Limestone:', roads, '| trails widened:', trails, '| streets total:', len(w['streets']), '| keep:', w['keep'])
