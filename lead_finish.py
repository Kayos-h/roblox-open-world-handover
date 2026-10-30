"""lead_finish - after the lead pass: notes.json for the gallery, FINAL_VERDICTS with the 31 FIXED models, and the patched gallery generator (new group F first)."""
import json
import os
import re

T = r"C:\Users\Nitro\.kiro\crew\workspace\town"
W = os.path.join(T, 'library', 'v5_work')

# 1. notes.json from lead_compare.py's NOTE dict
src = open(os.path.join(T, 'lead_compare.py'), encoding='utf-8').read()
ns = {}
exec(src[src.index('NOTE = {'):src.index('f = ImageFont')], ns)
json.dump(ns['NOTE'], open(os.path.join(W, 'lead', 'notes.json'), 'w'), indent=1)

# 2. FINAL_VERDICTS: the 31 fixed models
fixed = json.load(open(os.path.join(W, 'lead', 'fixed_ids.json')))
fv = json.load(open(os.path.join(W, 'FINAL_VERDICTS_v5.json')))
for e in fv:
    if e['id'] in fixed:
        e['previous_verdict'] = e['verdict']
        e['verdict'] = 'FIXED'
        e['source'] = 'lead pass (rebuilt by the lead, checked by the lead, not judged by reviewers)'
json.dump(fv, open(os.path.join(W, 'FINAL_VERDICTS_v5.json'), 'w'), indent=1)
from collections import Counter
print('FINAL:', dict(Counter(e['verdict'] for e in fv)), 'total', len(fv))

# 3. gallery generator: add the FIXED group
p = os.path.join(T, 'make_gallery_final.py')
t = open(p, encoding='utf-8').read()


def sub(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:70])
    t = t.replace(old, new)


sub("sub(\"COL = {'REDO': (176, 28, 44),\", \"COL = {'UNREVIEWED': (96, 104, 120), 'REDO': (176, 28, 44),\")",
    "sub(\"COL = {'REDO': (176, 28, 44),\", \"COL = {'FIXED': (46, 112, 196), 'UNREVIEWED': (96, 104, 120), 'REDO': (176, 28, 44),\")")
sub("    rev[_i] = _e'''\nsub(old_rev, new_rev)",
    "    rev[_i] = _e\n_fixed = json.load(open(os.path.join(LIB, 'v5_work', 'lead', 'fixed_ids.json')))\n_NOTE = json.load(open(os.path.join(LIB, 'v5_work', 'lead', 'notes.json')))\nfor _i in _fixed:\n    rev[_i] = dict(id=_i, verdict='FIXED', defects=[_NOTE.get(_i[:7], 'rebuilt in this pass')], fix='')'''\nsub(old_rev, new_rev)")
sub("sub(\"    ('C', 'C_good',", "sub(\"groups = [\\n    ('A', 'A_defective',\", \"groups = [\\n    ('F', 'F_fixed_now', 'FIXED IN THIS PASS: rebuilt and checked by the lead, waiting for YOUR review', [i for i in order if rev[i]['verdict'] == 'FIXED']),\\n    ('A', 'A_defective',\")\nsub(\"    ('C', 'C_good',")
sub("(('UNREVIEWED', 'rebuilt in round 2, no verdict yet'),", "(('FIXED', 'rebuilt in this pass, for your review'), ('UNREVIEWED', 'rebuilt in round 2, no verdict yet'),")
open(p, 'w', encoding='utf-8').write(t)
print('gallery generator patched')
