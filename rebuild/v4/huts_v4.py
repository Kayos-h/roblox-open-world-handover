"""Replaces the part-built placeholders (Phase1Map.PartBuilt: 46 rusty huts, 17 igloos, 13 ice shanties, 30 fishing holes) with the uploaded V4 models.
Writes mapplan/v4_huts.json (place with rebuild/v4/build_v4.ps1 -area v4_huts -nocollide FishingHoles). The placeholders are archived afterwards by archive_partbuilt.luau.
Replayable: python huts_v4.py
Orientation: rot 0 = door on +Z (south), same convention as the placeholders and the other V4 plans.
"""
import json, random, csv, os

TOWN = r'C:\Users\Nitro\.kiro\crew\workspace\town'
rng = random.Random(7071)
IDS = set()
for row in csv.DictReader(open(TOWN + r'\asset_ids.csv', encoding='utf-8-sig')):
    if row.get('asset_id'):
        IDS.add(row['name'])
pp = json.load(open(TOWN + r'\rebuild\parts_plan.json'))

HUTS = ['A04_01_rusty_hut_01', 'A04_02_rusty_hut_02', 'A04_03_rusty_hut_03', 'A04_04_rusty_hut_04', 'A04_05_rusty_hut_05', 'A04_06_rusty_hut_06']
IGLOOS = ['A01_01_igloo_01', 'A01_02_igloo_02', 'A01_03_igloo_03']
SHANTIES = ['A02_01_ice_shanty_01', 'A02_02_ice_shanty_02', 'A02_03_ice_shanty_03', 'A02_04_ice_shanty_04']
HOLES = ['A03_01_fishing_hole_01', 'A03_02_fishing_hole_02', 'A03_03_fishing_hole_03']
for lst in (HUTS, IGLOOS, SHANTIES, HOLES):
    for m in lst:
        assert m in IDS, ('not uploaded', m)

items = []


def cycle(models, n):
    """models in shuffled rounds so neighbours rarely repeat"""
    out = []
    while len(out) < n:
        r = models[:]
        rng.shuffle(r)
        if out and r[0] == out[-1]:
            r.append(r.pop(0))
        out.extend(r)
    return out[:n]


hut_models = cycle(HUTS, len(pp['huts']))
for h, m in zip(pp['huts'], hut_models):
    s = round(0.74 + max(0, h['w'] - 10) * 0.05 + rng.uniform(-0.03, 0.04), 2)
    items.append({'model': m, 'x': h['x'], 'z': h['z'], 'rot': round(h['rot'] + rng.uniform(-4, 4), 1), 'group': 'Huts', 'scale': s})

ig_models = cycle(IGLOOS, len(pp['igloos']))
for h, m in zip(pp['igloos'], ig_models):
    items.append({'model': m, 'x': h['x'], 'z': h['z'], 'rot': h['rot'], 'group': 'Igloos', 'scale': round(rng.uniform(0.95, 1.1), 2)})

sh_models = cycle(SHANTIES, len(pp['shanties']))
for h, m in zip(pp['shanties'], sh_models):
    items.append({'model': m, 'x': h['x'], 'z': h['z'], 'rot': round(h['rot'], 1), 'group': 'IceShanties', 'scale': 1.0})

fh_models = cycle(HOLES, len(pp['fishing_holes']))
for h, m in zip(pp['fishing_holes'], fh_models):
    items.append({'model': m, 'x': h['x'], 'z': h['z'], 'rot': round(rng.uniform(0, 360), 1), 'group': 'FishingHoles', 'scale': 1.0, 'y_offset': 0.05})

json.dump({'area': 'v4_huts', 'terrain': [], 'placements': items}, open(TOWN + r'\mapplan\v4_huts.json', 'w'))
print('v4_huts plan:', len(items), 'items', {g: sum(1 for i in items if i['group'] == g) for g in ('Huts', 'Igloos', 'IceShanties', 'FishingHoles')})
