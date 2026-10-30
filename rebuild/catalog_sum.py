import json, collections
cat = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\catalog.json', encoding='utf-8-sig'))
g = collections.defaultdict(list)
for m in cat:
    g[m['folder']].append(f"{m['id']} {m['size_x']:.0f}x{m['height']:.0f}x{m['size_z']:.0f}")
for f, items in g.items():
    print(f'## {f} ({len(items)})')
    print(' | '.join(items))
