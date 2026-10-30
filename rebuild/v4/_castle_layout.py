import json, math, collections
MP = r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan'
RB = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
cap = [q for q in json.load(open(MP + r'\v3_capital.json', encoding='utf-8-sig'))['placements'] if not q.get('skip')]
for q in cap:
    if q['model'].startswith('K0') and q['model'][:3] in ('K01', 'K02', 'K03', 'K04', 'K08', 'K06'):
        print(q['model'], round(q['x']), round(q['z']), 'rot', q.get('rot'), 'scale', q.get('scale'))
walls = sorted([(round(q['x']), round(q['z']), q.get('rot')) for q in cap if q['model'].startswith('K05')])
print('K05 curtain walls:', walls)
W = json.load(open(RB + r'\world.json'))
for p in W['pads']:
    if p['name'] in ('capital_castle', 'capital_city'):
        print(p)
cf = [q for q in json.load(open(MP + r'\v3f_castle.json', encoding='utf-8-sig'))['placements'] if not q.get('skip')]
print('courtyard items (castle_final + court + royal):')
for q in cf:
    if q.get('group') in ('CastleMarket', 'Statues', 'Forecourt'):
        print('  ', q['group'], q['model'], round(q['x']), round(q['z']))
cc = [q for q in cap if q.get('group') == 'CastleCourt']
for q in cc:
    print('  court', q['model'], round(q['x']), round(q['z']), q.get('rot'))
