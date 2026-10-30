import json, math, sys
sys.path.insert(0, r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild')
RB = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
W = json.load(open(RB + r'\world.json'))
rusty = [{'w': s['w'], 'pts': s['pts']} for s in W['streets'] if s['name'].startswith('v3_rusty')]
rusty += [{'w': r['w'], 'pts': r['pts']} for r in W['roads'] if any(900 < p[0] < 1900 and 560 < p[1] < 1600 for p in r['pts'])]
json.dump({'streets': rusty}, open(RB + r'\_rusty_streets.json', 'w'))
print('rusty street polylines', len(rusty), 'points', sum(len(r['pts']) for r in rusty))
