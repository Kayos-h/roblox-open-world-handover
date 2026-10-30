"""v5_fix_briefs - writes one assignment file per builder (library\\v5_work\\fix\\assign_<A>.md) and creates the empty fix-module skeletons
(library\\src\\v5_fx_<queue>.py) that the builders fill in. Existing fix modules are never overwritten.
"""
import os
import json

T = r"C:\Users\Nitro\.kiro\crew\workspace\town"
LIB = os.path.join(T, 'library')
FIX = os.path.join(LIB, 'v5_work', 'fix')
rows = json.load(open(os.path.join(FIX, 'fix_ids.json')))
ORDER = {'REDO': 0, 'MAJOR': 1, 'MINOR': 2, 'OK': 3}

# builder -> (label, [(fix module, worker, palette prefix, round-1 module)], row filter)
AGENTS = {
    'A1': ('plains, ruins and crater rocks', [('v5_fx_vi_a', 'vi', 'vi_fa', 'v5_vi')], lambda r: r['worker'] == 'vi' and r['batch'] in ('plains_set', 'ruins_crater', 'sky')),
    'A2': ('road life, bridges, coast and reefs', [('v5_fx_vi_b', 'vi', 'vi_fb', 'v5_vi')], lambda r: r['worker'] == 'vi' and r['batch'] in ('road_life', 'coast_set')),
    'A3': ('desert and Skull City', [('v5_fx_vh', 'vh', 'vh_f', 'v5_vh')], lambda r: r['worker'] == 'vh'),
    'A4': ('highlands, forest, fortress and marsh', [('v5_fx_vg', 'vg', 'vg_f', 'v5_vg')], lambda r: r['worker'] == 'vg'),
    'A5': ('Himalayan kit and the capital', [('v5_fx_vc', 'vc', 'vc_f', 'v5_vc'), ('v5_fx_vd', 'vd', 'vd_f', 'v5_vd')], lambda r: r['worker'] in ('vc', 'vd')),
    'A6': ('elf valley, Town 1, landmark heroes, tower pieces, reworks',
           [('v5_fx_ve', 've', 've_f', 'v5_ve'), ('v5_fx_vf', 'vf', 'vf_f', 'v5_vf'), ('v5_fx_va', 'va', 'va_f', 'v5_va'), ('v5_fx_vb', 'vb', 'vb_f', 'v5_vb'), ('v5_fx_vj', 'vj', 'vj_f', 'v5_vj')],
           lambda r: r['worker'] in ('ve', 'vf', 'va', 'vb', 'vj')),
}
LEAD = {'WT02_01_wizard_tower_interior'}      # kept by the lead: needs the shelves and the map assembled into it, not a rebuild by a builder
for _k, (_l, _m, _f) in list(AGENTS.items()):
    AGENTS[_k] = (_l, _m, (lambda f: (lambda r: f(r) and r['id'] not in LEAD))(_f))
SKEL = '''"""{mod} - FIX ROUND builders for assignment {A} ({label}). Owner: builder {A}. Replaces the round-1 builders of the ids in library\\\\v5_work\\\\fix\\\\assign_{A}.md.
Same worker ({worker}) and same category folders as round 1, so the files and the {worker}_ fragments are overwritten in place after archiving.
NEW palette keys only, under the prefix {pfx}_ (never re-register a round-1 key name with another colour: that would recolour models that are not rebuilt).
No glow, no emissive, no freestanding entrance arch. Front faces -Y, pivot at the bottom centre.
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v4util
import v5kit
from v5kit import Acc, polar, tang, mk, ids, band, strata
import v5gen as G
from v5gen import house, round_tower, wall_seg, column, cliff, spire, rock_arch, tree
import {orig} as ORIG          # round-1 module: read it, reuse its palette dict and helpers, never edit it

P = G.reg('{pfx}', {{
    # 'name': ((r, g, b), 'RobloxMaterial', metallic, roughness),   -> key '{pfx}_name'
}})

# builders go here: def _something(): reset(); A = Acc(); ...; A.to_scene(); return finalize('name', 25)

BATCHES = {{
    # 'batch_name': ('<category folder of round 1, see the assignment file>', mk([(manifest_id, builder), ...], 0.1)),
}}
'''
summary = {}
for A, (label, mods, flt) in AGENTS.items():
    mine = sorted([r for r in rows if flt(r)], key=lambda r: (ORDER[r['verdict']], r['row'], r['id']))
    from collections import Counter
    cv = Counter(r['verdict'] for r in mine)
    L = [f'# Assignment {A}: {label}', '',
         f'{len(mine)} models: REDO {cv["REDO"]}, MAJOR {cv["MAJOR"]}, MINOR {cv["MINOR"]}, OK-with-note {cv["OK"]}. Work in the order of the table (worst first).', '',
         '## Your modules (you own these files and nothing else)', '',
         '| fix module | worker | new palette prefix | round-1 module to read |', '|---|---|---|---|']
    for mod, w, pfx, orig in mods:
        L.append(f'| `library\\src\\{mod}.py` | {w} | `{pfx}_` | `library\\src\\{orig}.py` |')
    L += ['', 'Scratch build: `powershell -NoProfile -ExecutionPolicy Bypass -File "C:\\Users\\Nitro\\.kiro\\crew\\workspace\\town\\scratch.ps1" -Module <fix module> -Ids <id,id,...> -Tag ' + A + '`',
          'Sheets land in `library\\v5_work\\fix_scratch\\' + A + '\\<id>.png`. Target size is W x D x H in studs (X, Y, Z); the manifest autofit (`mk(..., 0.1)`) rescales a model that is more than 10% off, which distorts it, so design to size.', '']
    fam = Counter(r['row'] for r in mine)
    L += ['## Families in this assignment', '', ', '.join(f'{k} x{v}' for k, v in sorted(fam.items())), '', '## Models', '',
          '| id | verdict | category | target W x D x H | tri budget | tris now | what the reviewers saw | reviewer suggestion |', '|---|---|---|---|---|---|---|---|']
    for r in mine:
        d = '; '.join(r['defects']).replace('|', '/').replace('\n', ' ') or '(no flaw listed, sibling-variety note only)'
        L.append(f"| `{r['id']}` | {r['verdict']} | {r['category']} | {r['want_w']:g} x {r['want_d']:g} x {r['want_h']:g} | {r['tri_budget']} | {r['tris_now']} | {d} | {(r['fix'] or '').replace('|', '/').replace(chr(10), ' ')} |")
    open(os.path.join(FIX, f'assign_{A}.md'), 'w', encoding='utf-8').write('\n'.join(L))
    summary[A] = len(mine)
    for mod, w, pfx, orig in mods:
        p = os.path.join(LIB, 'src', mod + '.py')
        if not os.path.exists(p):
            open(p, 'w', encoding='utf-8').write(SKEL.format(mod=mod, A=A, label=label, worker=w, pfx=pfx, orig=orig))
print('assignments written:', summary, 'total', sum(summary.values()))
missing = [r['id'] for r in rows if not any(f(r) for _, (_, _, f) in AGENTS.items())]
print('models without a builder (lead keeps these):', missing)
