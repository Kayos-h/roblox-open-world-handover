import json, collections, os, math
MP = r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan'
def load(n):
    return json.load(open(MP + '\\' + n + '.json', encoding='utf-8-sig'))
def ext(pl):
    xs = [q['x'] for q in pl]; zs = [q['z'] for q in pl]
    return 'x %.0f..%.0f z %.0f..%.0f' % (min(xs), max(xs), min(zs), max(zs))
cap = [q for q in load('v3_capital')['placements'] if not q.get('skip')]
for g in ('Walls', 'Castle', 'CastleCourt', 'RoyalGarden', 'OuterRing', 'MarketSquare', 'Gardens'):
    pl = [q for q in cap if q.get('group') == g]
    if pl:
        print('capital', g, len(pl), ext(pl), collections.Counter(q['model'] for q in pl).most_common(5))
cf = [q for q in load('v3f_castle')['placements'] if not q.get('skip')]
for g in sorted(set(q.get('group') for q in cf)):
    pl = [q for q in cf if q.get('group') == g]
    print('castle_final', g, len(pl), ext(pl), collections.Counter(q['model'] for q in pl).most_common(4))
# walls in detail: north / south / east / west lines of the capital wall
walls = [q for q in cap if q.get('group') == 'Walls']
print('wall z values:', sorted(set(round(q['z']) for q in walls))[:12], '...')
print('wall x values:', sorted(set(round(q['x']) for q in walls))[:6], '...', sorted(set(round(q['x']) for q in walls))[-4:])
# castle walls (K05/K06/K02/K03)
kw = [q for q in cap if q['model'].startswith('K0')]
print('K models:', collections.Counter(q['model'] for q in kw).most_common(12))
print('K extents', ext(kw))
# gates
for q in cap:
    if 'gate' in q['model'].lower():
        print('gate', q['model'], round(q['x']), round(q['z']), q.get('rot'))
