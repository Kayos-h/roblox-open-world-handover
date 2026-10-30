"""_palcheck - why did palette.json shrink, and which clashing keys hold stale values?"""
import os, json, glob, datetime

LIB = r'C:\Users\Nitro\.kiro\crew\workspace\town\library'
cur = json.load(open(os.path.join(LIB, 'palette.json')))
bak_p = os.path.join(LIB, 'palette.json.bak_pre_merge')
bak = json.load(open(bak_p))
print('current palette.json keys:', len(cur), ' backup(original base) keys:', len(bak))
lost = [k for k in bak if k not in cur]
changed = [k for k in bak if k in cur and cur[k] != bak[k]]
print('base keys LOST:', len(lost), lost[:10])
print('base keys with CHANGED value:', len(changed), changed[:10])
frag = {}
for f in sorted(glob.glob(os.path.join(LIB, 'palette_*.json')), key=os.path.getmtime):
    d = json.load(open(f))
    frag[os.path.basename(f)] = (datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime('%H:%M'), d)
for k in ('wj_moss', 'wx3r_ban_r', 'wx3r_ban_b', 'sea_cliff_02_base'):
    print('KEY', k, '| in base backup:', k in bak, '| main file:', cur.get(k))
    for name, (t, d) in frag.items():
        if k in d:
            print('     fragment', name, t, d[k])
all_frag_keys = set()
for name, (t, d) in frag.items():
    all_frag_keys |= set(d)
print('fragment files:', len(frag), ' union of fragment keys:', len(all_frag_keys))
print('main-file keys that are in no fragment and not in base backup:', len([k for k in cur if k not in all_frag_keys and k not in bak]))
print('palette.json mtime', datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(LIB, 'palette.json'))).strftime('%H:%M:%S'))
