import json
W = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\world.json'))
for r in W['rivers']:
    if r['name'].startswith('elf'):
        print(r['name'], 'w', r['w'], 'depth', r.get('depth'), 'pts', [(round(p[0]), round(p[1]), round(p[2], 1)) for p in r['pts']])
for s in W['streets']:
    if str(s['name']).startswith('v4_elf') or str(s['name']).startswith('elf'):
        print('street', s['name'], 'w', s['w'], s['mat'], len(s['pts']))
