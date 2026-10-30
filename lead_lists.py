"""lead_lists - id lists of the models fixed in this pass: lead\\fixed_ids.json (31 ids), lead\\pack_ids.json ({id, category}) for the back-view renderer."""
import json
import os
import glob

LIB = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
W = os.path.join(LIB, 'v5_work')
tg = json.load(open(os.path.join(W, 'lead_targets.json')))
untouched = ('LM26', 'LM28', 'LM29', 'PL02', 'PL05', 'WT02')
fixed = [i for i in tg if not i.startswith(untouched)]
meta = {}
for f in glob.glob(os.path.join(LIB, 'v4_meta_v[a-j].json')):
    meta.update(json.load(open(f)))
os.makedirs(os.path.join(W, 'lead'), exist_ok=True)
json.dump(fixed, open(os.path.join(W, 'lead', 'fixed_ids.json'), 'w'), indent=1)
json.dump([{'id': i, 'category': meta[i]['category']} for i in fixed], open(os.path.join(W, 'lead', 'pack_ids.json'), 'w'), indent=1)
print(len(fixed), 'fixed ids;', 'untouched from the target list:', [i for i in tg if i.startswith(untouched)])
