"""merge_reviews - merge all review_part_*.json of the v5 first review into review_defects_v5.json and print the counts.
Checks coverage against the 404-row manifest (every id exactly once), normalises verdict words, joins the automatic-check flags, and writes the data
tables of REVIEW_V5_FIRST.md (counts, per family, REDO and MAJOR lists with fixes, tower scores). Safe to re-run while reviewers are still writing.
"""
import os
import re
import csv
import json
import glob
from collections import Counter, defaultdict

W = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\v5_work"
MAN = r"C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5\V5_MANIFEST.csv"
rows = list(csv.DictReader(open(MAN, encoding='utf-8-sig')))
ids = [r['id'] for r in rows]
row_of = {r['id']: r['row'] for r in rows}
auto = {e['id']: e for e in json.load(open(os.path.join(W, 'AUTOCHECK_V5.json')))}
VERD = {'OK': 'OK', 'MINOR': 'MINOR', 'MAJOR': 'MAJOR', 'REDO': 'REDO', 'KEEP': 'OK', 'FIX': 'MAJOR', 'REBUILD': 'REDO'}
got, bad_format, dup, unknown = {}, [], [], []
parts_found = []
for f in sorted(glob.glob(os.path.join(W, 'review_part_*.json'))):
    parts_found.append(os.path.basename(f))
    try:
        data = json.load(open(f, encoding='utf-8'))
    except Exception as e:
        bad_format.append((os.path.basename(f), str(e)[:80]))
        continue
    if isinstance(data, dict):
        data = data.get('models') or data.get('items') or list(data.values())
    for o in data:
        if not isinstance(o, dict) or 'id' not in o:
            bad_format.append((os.path.basename(f), 'item without id'))
            continue
        v = VERD.get(str(o.get('verdict', '')).strip().upper())
        if not v:
            bad_format.append((os.path.basename(f), f"{o['id']}: verdict {o.get('verdict')!r}"))
            continue
        if o['id'] not in row_of:
            unknown.append(o['id'])
            continue
        if o['id'] in got:
            dup.append(o['id'])
        d = o.get('defects') or []
        if isinstance(d, str):
            d = [d]
        got[o['id']] = {'id': o['id'], 'verdict': v, 'defects': d, 'fix': o.get('fix', '') or '', 'scores': o.get('scores'), 'part': os.path.basename(f)}
missing = [i for i in ids if i not in got]
out = []
for i in ids:
    if i in got:
        e = dict(got[i])
        e['auto_flags'] = auto.get(i, {}).get('flags', [])
        e['tris'] = auto.get(i, {}).get('tris')
        e['worker'] = auto.get(i, {}).get('worker')
        out.append(e)
json.dump(out, open(os.path.join(W, 'review_defects_v5.json'), 'w'), indent=1)
cnt = Counter(e['verdict'] for e in out)
print(f'parts read: {len(parts_found)}   models with a verdict: {len(out)} of {len(ids)}   missing: {len(missing)}   duplicates: {len(dup)}   unknown ids: {len(unknown)}   bad items: {len(bad_format)}')
print('verdicts:', {k: cnt.get(k, 0) for k in ('OK', 'MINOR', 'MAJOR', 'REDO')})
if bad_format:
    print('BAD FORMAT:', bad_format[:8])
if missing:
    print('MISSING (first 40):', missing[:40])
fam = defaultdict(Counter)
for e in out:
    fam[re.match(r'[A-Z]+', row_of[e['id']]).group(0)][e['verdict']] += 1
print('family   n  OK MINOR MAJOR REDO')
for k, c in sorted(fam.items()):
    print(f'{k:6} {sum(c.values()):3} {c["OK"]:3} {c["MINOR"]:4} {c["MAJOR"]:4} {c["REDO"]:4}')
wk = defaultdict(Counter)
for e in out:
    wk[e['worker']][e['verdict']] += 1
print('queue    n  OK MINOR MAJOR REDO')
for k, c in sorted(wk.items(), key=lambda kv: str(kv[0])):
    print(f'{str(k):6} {sum(c.values()):3} {c["OK"]:3} {c["MINOR"]:4} {c["MAJOR"]:4} {c["REDO"]:4}')
both = [e['id'] for e in out if e['verdict'] in ('MAJOR', 'REDO') and e['auto_flags']]
print('MAJOR/REDO that the automatic checks also flagged:', len(both))
auto_only = [i for i, e in auto.items() if e['flags'] and i in got and got[i]['verdict'] == 'OK']
print('flagged by the automatic checks but rated OK by the reviewers:', len(auto_only), auto_only[:12])
md = ['# First v5 review: data tables', '', f'{len(out)} of {len(ids)} models have a verdict. OK {cnt.get("OK", 0)}, MINOR {cnt.get("MINOR", 0)}, MAJOR {cnt.get("MAJOR", 0)}, REDO {cnt.get("REDO", 0)}.', '']
md += ['## By family', '', '| family | models | OK | MINOR | MAJOR | REDO |', '|---|---|---|---|---|---|']
for k, c in sorted(fam.items()):
    md.append(f'| {k} | {sum(c.values())} | {c["OK"]} | {c["MINOR"]} | {c["MAJOR"]} | {c["REDO"]} |')
for title, vv in (('REDO', 'REDO'), ('MAJOR', 'MAJOR')):
    md += ['', f'## {title} ({cnt.get(vv, 0)})', '', '| id | what is wrong | fix |', '|---|---|---|']
    for e in out:
        if e['verdict'] == vv:
            md.append(f"| `{e['id']}` | {'; '.join(e['defects'])[:200]} | {e['fix'][:220]} |")
md += ['', f'## MINOR ({cnt.get("MINOR", 0)})', '']
for e in out:
    if e['verdict'] == 'MINOR':
        md.append(f"- `{e['id']}`: {'; '.join(e['defects'])[:160]}")
tw = [e for e in out if e.get('scores')]
if tw:
    md += ['', '## Tower scores', '', '| id | verdict | scores |', '|---|---|---|']
    for e in tw:
        md.append(f"| `{e['id']}` | {e['verdict']} | {json.dumps(e['scores'])} |")
open(os.path.join(W, 'REVIEW_V5_TABLES.md'), 'w', encoding='utf-8').write('\n'.join(md))
