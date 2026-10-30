"""lead_targets - the models I fix myself in this pass: id, worker, row, the module files whose build table mentions the row, latest reviewer notes."""
import os
import re
import csv
import json
import glob

T = r"C:\Users\Nitro\.kiro\crew\workspace\town"
LIB = os.path.join(T, 'library')
W = os.path.join(LIB, 'v5_work')
fin = {e['id']: e for e in json.load(open(os.path.join(W, 'FINAL_VERDICTS_v5.json')))}
notes = {}
for p in ('review_defects_v5.json', r'r2\review_defects_r2.json', r'r3\review_defects_r3.json', r'r4\review_defects_r4.json'):
    for e in json.load(open(os.path.join(W, p))):
        notes[e['id']] = e
worker = {}
for f in glob.glob(os.path.join(LIB, 'v4_meta_v[a-j].json')):
    w = os.path.basename(f)[8:-5]
    for k in json.load(open(f)):
        worker[k] = w
man = {r['id']: r for r in csv.DictReader(open(os.path.join(T, 'plan_v5', 'V5_MANIFEST.csv'), encoding='utf-8-sig'))}
targets = [i for i, e in fin.items() if e['verdict'] in ('MAJOR', 'REDO', 'UNREVIEWED')] + ['CP15_01_order_hq_01', 'CP17_01_plaza_features_01', 'WT13_06_plateau_terrace_set_06']
targets = list(dict.fromkeys(targets))
mods = sorted(glob.glob(os.path.join(LIB, 'src', 'v5_*.py')))
text = {m: open(m, encoding='utf-8').read() for m in mods}
json.dump(targets, open(os.path.join(W, 'lead_targets.json'), 'w'), indent=1)
print(len(targets), 'targets')
for i in sorted(targets, key=lambda i: (fin[i]['verdict'], i)):
    row = man[i]['row']
    where = [os.path.basename(m)[:-3] for m, tx in text.items() if re.search(r"['\"]%s['\"]" % row, tx) and os.path.basename(m) not in ('v5_tower_assembly.py',)]
    n = notes.get(i, {})
    print(f"{i[:38].ljust(38)} {fin[i]['verdict'][:5].ljust(5)} w={worker.get(i)} row={row} modules={where}")
    if '--notes' in os.sys.argv:
        print('      saw:', '; '.join(n.get('defects') or [])[:260])
        print('      fix:', (n.get('fix') or '')[:260])
