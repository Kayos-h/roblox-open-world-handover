"""lead2_finish - after the second lead pass: merged notes, FINAL_VERDICTS (87 more FIXED), gallery generator reads both fixed lists, lead_verify takes an ids file."""
import json
import os
import glob
from collections import Counter

T = r"C:\Users\Nitro\.kiro\crew\workspace\town"
W = os.path.join(T, 'library', 'v5_work')
L2 = os.path.join(W, 'lead2')

# 1. merged notes
notes = json.load(open(os.path.join(W, 'lead', 'notes.json')))
for f in sorted(glob.glob(os.path.join(L2, 'notes_b*.json'))):
    notes.update(json.load(open(f)))
json.dump(notes, open(os.path.join(L2, 'notes_all.json'), 'w'), indent=1)
print('notes:', len(notes))

# 2. FINAL_VERDICTS
work = json.load(open(os.path.join(L2, 'worklist.json')))
fv = json.load(open(os.path.join(W, 'FINAL_VERDICTS_v5.json')))
n = 0
for e in fv:
    if e['id'] in work:
        e['previous_verdict'] = e['verdict']
        e['verdict'] = 'FIXED'
        e['source'] = 'lead pass 2 (rebuilt by the lead, checked by the lead, not judged by reviewers)'
        n += 1
json.dump(fv, open(os.path.join(W, 'FINAL_VERDICTS_v5.json'), 'w'), indent=1)
print('updated', n, '->', dict(Counter(e['verdict'] for e in fv)), 'total', len(fv))

# 3. gallery generator: both fixed lists, merged notes
p = os.path.join(T, 'make_gallery_final.py')
t = open(p, encoding='utf-8').read()
old1 = "_fixed = json.load(open(os.path.join(LIB, 'v5_work', 'lead', 'fixed_ids.json')))"
new1 = "_fixed = json.load(open(os.path.join(LIB, 'v5_work', 'lead', 'fixed_ids.json'))) + json.load(open(os.path.join(LIB, 'v5_work', 'lead2', 'worklist.json')))"
old2 = "_NOTE = json.load(open(os.path.join(LIB, 'v5_work', 'lead', 'notes.json')))"
new2 = "_NOTE = json.load(open(os.path.join(LIB, 'v5_work', 'lead2', 'notes_all.json')))"
assert t.count(old1) == 1 and t.count(old2) == 1
t = t.replace(old1, new1).replace(old2, new2)
t = t.replace("'FIXED IN THIS PASS: rebuilt and checked by the lead, waiting for YOUR review'", "'FIXED BY THE LEAD (two passes, 118 models): rebuilt and checked by the lead, waiting for YOUR review'")
open(p, 'w', encoding='utf-8').write(t)

# 4. lead_verify takes an ids file
p = os.path.join(T, 'lead_verify.py')
t = open(p, encoding='utf-8').read()
old = "fixed = json.load(open(os.path.join(LIB, 'v5_work', 'lead', 'fixed_ids.json')))"
new = "import sys\nfixed = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(LIB, 'v5_work', 'lead', 'fixed_ids.json')))"
assert t.count(old) == 1
open(p, 'w', encoding='utf-8').write(t.replace(old, new))
print('scripts updated')
