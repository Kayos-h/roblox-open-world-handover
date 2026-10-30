"""Checks that every colour key used by the V4 models exists in library/palette.json; lists glow/Neon keys per model folder."""
import json, collections
LIB = r'C:\Users\Nitro\.kiro\crew\workspace\town\library'
meta = json.load(open(LIB + r'\v4_meta.json', encoding='utf-8'))
pal = json.load(open(LIB + r'\palette.json', encoding='utf-8'))
missing = collections.defaultdict(set)
glow_models = collections.defaultdict(list)
neon_models = collections.defaultdict(list)
n = 0
for mid, m in meta.items():
    if mid.startswith('ZZ_') or m.get('category') == 'v4_test':
        continue
    n += 1
    for k in m.get('materials', []):
        key = k.rsplit('_', 1)[0] if k.rsplit('_', 1)[-1].isdigit() else k
        if key not in pal:
            missing[key].add(mid)
        else:
            e = pal[key]
            if e.get('glow'):
                glow_models[m['category']].append(mid + ':' + key)
            if e.get('material') == 'Neon':
                neon_models[m['category']].append(mid + ':' + key)
print('models checked', n, ' palette keys', len(pal))
print('missing keys:', {k: sorted(v)[:3] for k, v in missing.items()} if missing else 'none')
for cat in sorted(set(list(glow_models) + list(neon_models))):
    print(cat, 'glow:', len(glow_models.get(cat, [])), 'neon:', len(neon_models.get(cat, [])), (glow_models.get(cat, []) + neon_models.get(cat, []))[:8])

