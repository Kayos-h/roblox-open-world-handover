import json, math
W = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\world.json'))
for kind in ('streets', 'roads'):
    for s in W[kind]:
        inside = [p for p in s['pts'] if -230 < p[0] < 230 and -2380 < p[1] < -2000]
        if inside:
            print(kind, s['name'], 'w', s.get('w'), 'mat', s.get('mat'), 'pts inside', len(inside), 'of', len(s['pts']), 'e.g.', [(round(p[0]), round(p[1])) for p in inside[:4]])
