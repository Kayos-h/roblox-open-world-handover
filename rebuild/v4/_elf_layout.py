import json, collections, math
V4 = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4'
fp = json.load(open(V4 + r'\occ_v4_elf.json'))
big = [f for f in fp if max(f[2], f[3]) >= 12]
print('elf footprints', len(fp), 'large (>=24 wide):', len(big))
xs = [f[0] for f in fp]; zs = [f[1] for f in fp]
print('extent x %.0f..%.0f z %.0f..%.0f' % (min(xs), max(xs), min(zs), max(zs)))
cells = collections.Counter((round(f[0] / 100) * 100, round(f[1] / 100) * 100) for f in big)
print('large buildings per 100-stud cell:', sorted(cells.items(), key=lambda kv: -kv[1])[:10])
for f in sorted(big, key=lambda f: -(f[2] * f[3]))[:12]:
    print('  big at (%.0f,%.0f) half %.0fx%.0f' % tuple(f))
plan = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\v4_elf.json', encoding='utf-8-sig'))['placements']
cnt = collections.Counter(p['model'][:3] for p in plan)
print('v4_elf plan models by family:', dict(cnt.most_common(12)))
th = [p for p in plan if p['model'].startswith('D01_')]
print('treehouses:', [(round(p['x']), round(p['z'])) for p in th])
tr = [p for p in plan if p['model'].startswith('D04_')]
print('D04 buildings:', [(p['model'][:8], round(p['x']), round(p['z'])) for p in tr][:20])
