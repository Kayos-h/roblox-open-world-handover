"""archive_lead - copy (never move, never overwrite) the current files of the lead-fix target models, the metas, palettes and source modules
into library\\v5_fix3_archive before anything is rebuilt.  python archive_lead.py [extra ids...]"""
import os
import sys
import json
import glob
import shutil

LIB = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
AR = os.path.join(LIB, 'v5_fix3_archive')
ids = json.load(open(os.path.join(LIB, 'v5_work', 'lead_targets.json'))) + sys.argv[1:]
n = skipped = 0


def cp(src, dst):
    global n, skipped
    if os.path.exists(dst):
        skipped += 1
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
    n += 1


for i in ids:
    for p in glob.glob(os.path.join(LIB, 'v5_*', i + '*')) + glob.glob(os.path.join(LIB, 'v4_sheets', f'_t_{i}.png')):
        cp(p, os.path.join(AR, os.path.relpath(p, LIB)))
for p in glob.glob(os.path.join(LIB, 'v4_meta_v*.json')) + glob.glob(os.path.join(LIB, 'palette_v*.json')) + [os.path.join(LIB, 'v4_meta.json'), os.path.join(LIB, 'palette.json')]:
    cp(p, os.path.join(AR, 'meta', os.path.basename(p)))
for p in glob.glob(os.path.join(LIB, 'src', 'v5*.py')):
    cp(p, os.path.join(AR, 'src', os.path.basename(p)))
print(f'archive {AR}: copied {n}, already there {skipped}')
