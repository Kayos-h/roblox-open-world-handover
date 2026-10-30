import json
W = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\world.json'))
for L in W['lakes']:
    print('lake', L['name'], 'c=(%d,%d)' % (L['cx'], L['cz']), 'r=(%d,%d)' % (L['rx'], L['rz']), 'level', L['level'], 'frozen' if L.get('frozen') else '')
ex = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4\world_extra.json'))
print('islets', len(ex['islets']), ex['islets'][:4])
print('rivers', [(r['name'], len(r['pts'])) for r in ex['rivers']])
