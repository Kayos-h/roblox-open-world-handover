import os, sys
sys.path.insert(0, r'C:\Users\Nitro\.kiro\crew\workspace\town\library\src')
import v4_manifest as M
rows = {r['id']: r for r in M.expand()}
by_slot = {'_'.join(i.split('_')[:2]): i for i in rows}

PLAN = {
    'wd2': {'rebuild': [('E13', range(1, 11)), ('R01', [1, 4])], 'new': [('R02', range(1, 5)), ('R03', range(1, 5))]},
    'we2': {'rebuild': [], 'new': [('B03', [1]), ('B04', [1, 2]), ('B06', range(1, 4)), ('B09', range(1, 5)), ('B10', range(1, 5)), ('F09', range(1, 14))]},
    'wf2': {'rebuild': [], 'new': [('C02', range(1, 4)), ('C03', [1]), ('C04', range(1, 3)), ('C05', range(1, 4)), ('C06', [1]), ('C07', range(1, 3)), ('C08', range(1, 3)), ('C09', [1]), ('E14', range(1, 5))]},
    'wg2': {'rebuild': [], 'new': [('E02', range(1, 4)), ('E03', range(1, 4)), ('E04', range(1, 3)), ('E12', range(1, 5)), ('E06', range(1, 13))]},
    'wh2': {'rebuild': [], 'new': [('E07', range(4, 10)), ('E08', range(1, 4)), ('E09', range(1, 3)), ('E10', range(1, 7)), ('E11', range(1, 4))]},
}
out_dir = r'C:\Users\Nitro\.kiro\crew\workspace\town\library\v4_work'
tot = 0
for w, p in PLAN.items():
    lines = [f'# Exact manifest ids for worker {w}', '', 'Use these ids EXACTLY (they are the keys of the BATCHES lists, the file names and the metadata keys).', '']
    for kind in ('rebuild', 'new'):
        if not p[kind]:
            continue
        lines.append('## ' + ('REBUILD (already built but judged weak: rebuild with the better method, overwrite)' if kind == 'rebuild' else 'NEW (not built yet)'))
        for code, nums in p[kind]:
            ids = []
            for n in nums:
                slot = f'{code}_{n:02d}'
                ids.append(by_slot[slot])
            lines.append(f'- {code}: ' + ', '.join(ids))
            tot += len(ids)
        lines.append('')
    open(os.path.join(out_dir, f'IDS_{w}.md'), 'w').write('\n'.join(lines))
    print(w, sum(len(list(n)) for k in ('rebuild', 'new') for _, n in p[k]))
print('total', tot)
