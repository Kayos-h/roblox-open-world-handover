"""v5_fix2_prepare - build the second fix round from the round-2 review.
Scope: every rebuilt model that is still not OK (80) + the 7 untouched anchors the new panel rated not OK + the whole wizard terrace set WT13_01..06.
Writes library\\v5_work\\r2\\fix2_ids.json, library\\v5_work\\r2\\fix2_<A>.md (one file per builder A1..A6) and ROUND2_LESSONS.md, and appends the new ids to
library\\v5_work\\fix\\fix_ids.json so the archive script covers them (round-1 state is copied, never overwritten).
"""
import os
import re
import csv
import json
import glob
from collections import Counter, defaultdict

T = r"C:\Users\Nitro\.kiro\crew\workspace\town"
LIB = os.path.join(T, 'library')
R2 = os.path.join(LIB, 'v5_work', 'r2')
FIX = os.path.join(LIB, 'v5_work', 'fix')
r2 = {e['id']: e for e in json.load(open(os.path.join(R2, 'review_defects_r2.json')))}
r1 = {e['id']: e for e in json.load(open(os.path.join(LIB, 'v5_work', 'review_defects_v5.json')))}
man = {r['id']: r for r in csv.DictReader(open(os.path.join(T, 'plan_v5', 'V5_MANIFEST.csv'), encoding='utf-8-sig'))}
meta, worker_of = {}, {}
for f in glob.glob(os.path.join(LIB, 'v4_meta_v[a-j].json')):
    w = os.path.basename(f)[8:-5]
    for k, v in json.load(open(f)).items():
        meta[k] = v
        worker_of[k] = w
fixrows = json.load(open(os.path.join(FIX, 'fix_ids.json')))
fixed_ids = {r['id'] for r in fixrows}
owner_old = {}
for A in ('A1', 'A2', 'A3', 'A4', 'A5', 'A6'):
    for i in re.findall(r'^\| `([A-Za-z0-9_]+)` \|', open(os.path.join(FIX, f'assign_{A}.md'), encoding='utf-8').read(), re.M):
        owner_old[i] = A
A1_ROWS = ('PL01', 'PL02', 'PL03', 'PL04', 'PL05', 'PL06', 'VL01', 'LM19', 'LM20', 'LM21', 'LM26', 'LM27', 'LM28', 'LM29', 'LM31', 'FL01', 'FL02')
A2_ROWS = ('RD01', 'RD02', 'RD03', 'RD04', 'RD05', 'RD06', 'BR01', 'RV01', 'CO03', 'CO04', 'CO05', 'HB01')


def owner_of(i):
    if i in owner_old:
        return owner_old[i]
    w, row = worker_of[i], man[i]['row']
    if w == 'vi':
        return 'A1' if row in A1_ROWS else 'A2'
    return {'vh': 'A3', 'vg': 'A4', 'vc': 'A5', 'vd': 'A5', 've': 'A6', 'vf': 'A6', 'va': 'A6', 'vb': 'A6', 'vj': 'A6'}[w]


target = {}
for i, e in r2.items():
    if e['verdict'] != 'OK':
        target[i] = e
for i in ['WT13_01', 'WT13_02', 'WT13_03', 'WT13_04', 'WT13_05', 'WT13_06']:
    pass
for i in man:
    if man[i]['row'].startswith('WT13_') or man[i]['row'] == 'WT13':
        target.setdefault(i, None)
rows = []
for i, e in sorted(target.items()):
    r = man[i]
    if e is None:
        v2, d2, f2 = 'UNREVIEWED', ['same set as WT13_01 and WT13_03, which the new panel rated MAJOR: blank or hollow backs, bright flat ramps that read as light panels'], 'Make the whole terrace set finished from every side: coursed stone, coping, steps with risers, darker matte stone instead of pale flat slabs, no open hollow boxes.'
    else:
        v2, d2, f2 = e['verdict'], e['defects'], e['fix']
    rows.append(dict(id=i, row=r['row'], worker=worker_of[i], category=meta[i]['category'], owner=owner_of(i), r2_verdict=v2, r2_defects=d2, r2_fix=f2,
                     r1_verdict=r1[i]['verdict'], r1_defects=r1[i]['defects'], was_rebuilt=i in fixed_ids, tri_budget=int(float(r['tri_budget'])),
                     want_w=float(r['size_x']), want_h=float(r['size_y']), want_d=float(r['size_z']), tris_now=meta[i].get('tris'), size_now=meta[i].get('size')))
json.dump(rows, open(os.path.join(R2, 'fix2_ids.json'), 'w'), indent=1)
# extend the fix list used by the archive script
have = {r['id'] for r in fixrows}
added = 0
for r in rows:
    if r['id'] not in have:
        fixrows.append(dict(id=r['id'], row=r['row'], worker=r['worker'], batch='?', category=r['category'], verdict=r['r1_verdict'], defects=r['r1_defects'], fix='', want_w=r['want_w'], want_h=r['want_h'],
                            want_d=r['want_d'], tri_budget=r['tri_budget'], tris_now=r['tris_now'], size_now=r['size_now'], note=''))
        added += 1
json.dump(fixrows, open(os.path.join(FIX, 'fix_ids.json'), 'w'), indent=1)
ORDER = {'MAJOR': 0, 'UNREVIEWED': 1, 'MINOR': 2}
by = defaultdict(list)
for r in rows:
    by[r['owner']].append(r)
LESSONS = """# Lessons from the round-2 review (read before you change anything)

Five fresh reviewers looked at BOTH sides (front and back) of every rebuilt model. They were stricter than round 1 and found things round 1 could not see. These patterns cost the most:

1. **Open-topped hollow grey boxes** (all VC04 skull-city buildings): a roof or a deliberate ruined crown is needed, not exposed beams over an empty box; the walls need colour variation and relief, not flat default grey.
2. **Pale or bright flat slabs read as glowing light panels**: bright white or cream roofs, ramps, terrace tops, waterfall panels (LM22_01, LM02_01, LM23_03), the CP08_01 roof, the WT13 ramps. Use mid-tone matte stone and break big flat faces into courses, coping, steps and slight tilts. Water: narrow stepped ribbons in muted blue-grey with foam only at the base.
3. **The back must be finished too**: flat solid back slabs (WT03_01 bookshelf back, WT13 terrace backs, quay and retaining walls) read as unfinished. Give every back a structure: coursing, buttresses, a rear frame, planks, windows.
4. **Plain pale cylinders and boxes** (watchtowers PL05, RD01_03, tower stumps LM29, CP01_02 wall): add courses, windows or slits, broken tops, colour bands, an entrance.
5. **Entrances and stairs must read** (DS08 underground entrances, LM07 carved stairs, LM12 temple stairs): a visible dark opening or descending treads with side walls. Black panels beside stairs read as inverted faces: avoid large near-black flat areas, keep the stair lit and the surround mid-tone.
6. **Siblings must differ in shape**, not only in colour or size (LM16 ring segments, SD02 ruin blocks, FR03 cave mouths, RV01 bank rocks, SP01 spires, LM28 columns).
7. **Flat single-tone rock and wall faces** read as the plain grey default: add colour bands, moss or lichen in the right places, ledges.
8. **Spindly verticals** (birch trunks, palms, spire tips): thicker trunks and fuller crowns.
9. **Props must read as one object** (camp RD02_05, battlefield RD05): a clear connected silhouette (tent with poles, fire ring, crates), no loose primitives.
10. **Near-black timber** (RD06_02) reads like the default dark grey: use warm brown.
The FLOAT check over-counts moss, rubble and merlons, but the reviewers did still call out several of them. Keep decorations visibly seated on a surface.
"""
open(os.path.join(R2, 'ROUND2_LESSONS.md'), 'w', encoding='utf-8').write(LESSONS)
for A, lst in sorted(by.items()):
    lst.sort(key=lambda r: (ORDER[r['r2_verdict']], r['row'], r['id']))
    cv = Counter(r['r2_verdict'] for r in lst)
    L = [f'# Fix round 2, builder {A}: {len(lst)} models', '', f'MAJOR {cv["MAJOR"]}, UNREVIEWED set members {cv["UNREVIEWED"]}, MINOR {cv["MINOR"]}. Worst first. Read `ROUND2_LESSONS.md` next to this file first.', '',
         'You own the same fix module(s) as before. Models marked "never rebuilt" are untouched round-1 models: write a new builder for them in your fix module (copy the round-1 code from the original queue module, then improve it) and add the id to `BATCHES` with the SAME category folder.', '',
         '| id | round 2 | round 1 | category | target W x D x H | tri budget | tris now | what the round-2 reviewers saw | reviewer suggestion | note |', '|---|---|---|---|---|---|---|---|---|---|']
    for r in lst:
        d = '; '.join(r['r2_defects']).replace('|', '/').replace('\n', ' ')
        L.append(f"| `{r['id']}` | {r['r2_verdict']} | {r['r1_verdict']} | {r['category']} | {r['want_w']:g} x {r['want_d']:g} x {r['want_h']:g} | {r['tri_budget']} | {r['tris_now']} | {d} | {(r['r2_fix'] or '').replace('|', '/')} | {'rebuilt in round 1' if r['was_rebuilt'] else 'never rebuilt'} |")
    open(os.path.join(R2, f'fix2_{A}.md'), 'w', encoding='utf-8').write('\n'.join(L))
print('fix round 2 models:', len(rows), {A: len(v) for A, v in sorted(by.items())}, '| added to fix_ids.json:', added)
print('by verdict:', dict(Counter(r['r2_verdict'] for r in rows)), '| never rebuilt:', sum(1 for r in rows if not r['was_rebuilt']))
