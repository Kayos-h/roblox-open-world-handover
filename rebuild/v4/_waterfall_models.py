import json
m = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\library\v4_meta.json'))
for k in ('D09_01_waterfall_cliff_a', 'D09_02_waterfall_cliff_b', 'F10_03_waterfall_step', 'F10_04_waterfall_cascade', 'F10_05_waterfall_trickle', 'R05_01_waterfall_cliff_01', 'R05_02_waterfall_cliff_02', 'C09_01_frozen_waterfall_01'):
    e = m.get(k)
    print(k, e and (e['size'], e.get('tris'), e.get('materials')))
# elf plan: what is placed near the north rim and the lake
plan = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\v4_elf.json', encoding='utf-8-sig'))['placements']
near = [(p['model'][:22], round(p['x']), round(p['z'])) for p in plan if -1900 < p['x'] < -1560 and -800 < p['z'] < -640 and not p['model'].startswith(('A', 'F05', 'F06', 'D06'))]
print('structures near the north rim:', near)
pal = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\library\palette.json'))
for k in ('water', 'water_white', 'foam', 'wf_water', 'falls', 'ev_water'):
    print(k, pal.get(k))
