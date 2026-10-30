"""_audit - which model files changed after the review pack was built, and are their thumbnails fresh?
Run: python _audit.py [HH:MM]   (default cutoff 13:41 today)
"""
import os, sys, json, glob, datetime

LIB = r'C:\Users\Nitro\.kiro\crew\workspace\town\library'
hh, mm = (sys.argv[1] if len(sys.argv) > 1 else '13:41').split(':')
cut = datetime.datetime.now().replace(hour=int(hh), minute=int(mm), second=0, microsecond=0).timestamp()

defects = json.load(open(os.path.join(LIB, 'v4_work', 'review_defects.json'), encoding='utf-8'))
fix = {e['id'] for e in defects if e['verdict'] != 'OK'}
meta = json.load(open(os.path.join(LIB, 'v4_meta.json')))

changed = {}
for p in glob.glob(os.path.join(LIB, 'v4_*', '*.fbx')):
    folder = os.path.basename(os.path.dirname(p))
    if folder in ('backup_pre_fix', 'stale') or folder.startswith('v4_work') or folder == 'v4_sheets':
        continue
    t = os.path.getmtime(p)
    if t > cut:
        changed[os.path.splitext(os.path.basename(p))[0]] = t

print(f'fix list {len(fix)} ids; changed after {hh}:{mm}: {len(changed)} ids')
extra = sorted(set(changed) - fix)
missing = sorted(fix - set(changed))
print('UNEXPECTED changes (not in fix list):', extra or 'none')
print('fix-list ids NOT rebuilt:', missing or 'none')

stale = []
for i, t in sorted(changed.items()):
    th = os.path.join(LIB, 'v4_sheets', '_t_' + i + '.png')
    if not os.path.exists(th):
        stale.append((i, 'no thumb'))
    elif os.path.getmtime(th) < t - 3:
        stale.append((i, 'thumb older by %d s' % (t - os.path.getmtime(th))))
print('stale or missing thumbnails:', len(stale))
for i, why in stale:
    print('  ', i, why)

if len(sys.argv) > 3 and sys.argv[2] == '--write':
    open(sys.argv[3], 'w', encoding='utf-8').write('\n'.join(sorted(changed)) + '\n')
    print('wrote', len(changed), 'ids to', sys.argv[3])

# tri / size outliers among changed ids (from the newest merged meta; merge first)
for i in sorted(changed):
    e = meta.get(i)
    if e and e.get('tris', 0) > 50000:
        print('OVER 50k tris:', i, e.get('tris'))
