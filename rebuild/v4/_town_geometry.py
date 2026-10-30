import json, collections, glob, os, math
MP = r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan'
for name in ('v3_capital', 'v3f_castle', 'v3_harbour', 'v3_rusty', 'v3_alpine', 'town1', 'v3_elf'):
    p = MP + '\\' + name + '.json'
    if not os.path.exists(p):
        print(name, 'missing'); continue
    d = json.load(open(p))
    pl = [q for q in d['placements'] if not q.get('skip')]
    xs = [q['x'] for q in pl]; zs = [q['z'] for q in pl]
    groups = collections.Counter(q.get('group') for q in pl)
    print('==', name, len(pl), 'x %.0f..%.0f z %.0f..%.0f' % (min(xs), max(xs), min(zs), max(zs)))
    print('   groups:', dict(groups.most_common(14)))
    walls = [q for q in pl if 'wall' in q['model'].lower() or 'gate' in q['model'].lower() or 'tower' in q['model'].lower()]
    if walls:
        wx = [q['x'] for q in walls]; wz = [q['z'] for q in walls]
        print('   wall/gate/tower models: %d  x %.0f..%.0f z %.0f..%.0f' % (len(walls), min(wx), max(wx), min(wz), max(wz)))
        names = collections.Counter(q['model'] for q in walls)
        print('   ', dict(names.most_common(8)))
