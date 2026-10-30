"""v5_archive_round1 - copy the round-1 state of every model in the fix round into library\\v5_round1_archive (COPY ONLY, nothing is deleted or moved).
Per id: <category>\\<id>.blend, .fbx, v4_sheets\\_t_<id>.png and v4_sheets\\<id>.png (hero four-angle sheet, if any).
Also: the per-worker meta and palette fragments, the merged v4_meta.json / palette.json, the round-1 review files and every v5*.py source file.
An archive file that already exists is never overwritten (so a re-run cannot replace round 1 with a later version). Verifies every copy by size.
"""
import os
import json
import glob
import shutil
import time

T = r"C:\Users\Nitro\.kiro\crew\workspace\town"
LIB = os.path.join(T, 'library')
ARC = os.path.join(LIB, 'v5_round1_archive')
rows = json.load(open(os.path.join(LIB, 'v5_work', 'fix', 'fix_ids.json')))
done, kept, bad, missing = 0, 0, [], []


def put(src, dst):
    global done, kept
    if not os.path.exists(src):
        return False
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        kept += 1
        return True
    shutil.copy2(src, dst)
    if os.path.getsize(src) != os.path.getsize(dst):
        bad.append(dst)
    done += 1
    return True


for r in rows:
    i, c = r['id'], r['category']
    for ext in ('.blend', '.fbx'):
        if not put(os.path.join(LIB, c, i + ext), os.path.join(ARC, c, i + ext)):
            missing.append(i + ext)
    if not put(os.path.join(LIB, 'v4_sheets', f'_t_{i}.png'), os.path.join(ARC, 'v4_sheets', f'_t_{i}.png')):
        missing.append(f'_t_{i}.png')
    put(os.path.join(LIB, 'v4_sheets', i + '.png'), os.path.join(ARC, 'v4_sheets', i + '.png'))
for f in glob.glob(os.path.join(LIB, 'v4_meta_v[a-j].json')) + glob.glob(os.path.join(LIB, 'palette_v[a-j].json')) + [os.path.join(LIB, 'v4_meta.json'), os.path.join(LIB, 'palette.json')]:
    put(f, os.path.join(ARC, 'meta', os.path.basename(f)))
for f in glob.glob(os.path.join(LIB, 'v5_work', 'review_defects_v5.json')) + glob.glob(os.path.join(LIB, 'v5_work', 'REVIEW_V5_*.md')) + glob.glob(os.path.join(LIB, 'v5_work', 'AUTOCHECK_V5.*')):
    put(f, os.path.join(ARC, 'review_round1', os.path.basename(f)))
for f in glob.glob(os.path.join(LIB, 'src', 'v5*.py')) + glob.glob(os.path.join(LIB, 'src', 'kitlib.py')) + glob.glob(os.path.join(LIB, 'src', 'v4util.py')):
    put(f, os.path.join(ARC, 'src', os.path.basename(f)))
n_files = sum(len(fs) for _, _, fs in os.walk(ARC))
json.dump({'created': time.strftime('%Y-%m-%d %H:%M:%S'), 'ids': len(rows), 'copied_now': done, 'already_there': kept, 'files_in_archive': n_files,
           'missing_sources': missing, 'size_mismatch': bad}, open(os.path.join(ARC, 'ARCHIVE_INFO.json'), 'w'), indent=1)
print(f'archive: {len(rows)} models; copied {done}, already archived {kept}; files in archive {n_files}; missing sources {len(missing)} {missing[:6]}; size mismatches {len(bad)}')
