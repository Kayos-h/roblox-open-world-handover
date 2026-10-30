import json
p = r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\v4_pieces.json'
d = json.load(open(p, encoding='utf-8-sig'))
before = len(d['placements'])
d['placements'] = [q for q in d['placements'] if q.get('group') != 'SeaCliffs']
json.dump(d, open(p, 'w'))
import collections
print('v4_pieces plan: %d -> %d items' % (before, len(d['placements'])), dict(collections.Counter(q['group'] for q in d['placements'])))
