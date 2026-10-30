"""v4_merge - fold the per-worker metadata and palette fragments into the main files (idempotent, never deletes).
  library\\v4_meta.json   <- every library\\v4_meta_<worker>.json  (newest file wins; test entries skipped)
  library\\palette.json   <- every library\\palette_<worker>.json  (existing keys are NEVER overwritten)
Also checks that every material key used by a built model exists in palette.json (otherwise it would import grey).
Run: python v4_merge.py
"""
import os, sys, json, glob, shutil, time

SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
LIB = r'C:\Users\Nitro\.kiro\crew\workspace\town\library'


def main():
    meta_p = os.path.join(LIB, 'v4_meta.json')
    pal_p = os.path.join(LIB, 'palette.json')
    for p in (meta_p, pal_p):
        bak = p + '.bak_pre_merge'
        if not os.path.exists(bak):
            shutil.copy2(p, bak)
    meta = json.load(open(meta_p))
    n0 = len(meta)
    # fix-round workers (v4_meta_wx*.json) are applied last, so their rebuilt models win whatever the file times are
    files = sorted(glob.glob(os.path.join(LIB, 'v4_meta_*.json')),
                   key=lambda f: (os.path.basename(f).startswith('v4_meta_wx'), os.path.getmtime(f)))
    added = upd = skipped = 0
    for f in files:
        try:
            d = json.load(open(f))
        except Exception as e:
            print('unreadable', f, e)
            continue
        for k, e in d.items():
            if k.startswith('ZZ_') or e.get('category') == 'v4_test':
                skipped += 1
                continue
            if not os.path.exists(os.path.join(LIB, e.get('category', ''), k + '.fbx')):
                skipped += 1
                continue
            if k in meta:
                upd += 1
            else:
                added += 1
            meta[k] = e
    json.dump(meta, open(meta_p, 'w'), indent=1)
    print(f'meta: {n0} -> {len(meta)} entries ({added} added, {upd} updated, {skipped} skipped) from {len(files)} worker files')

    pal = json.load(open(pal_p))
    p0 = len(pal)
    base_p = pal_p + '.bak_pre_merge'
    base = json.load(open(base_p)) if os.path.exists(base_p) else {}
    clash, refreshed = [], []
    # original base keys are never touched; worker keys: the newest fragment wins, fix-round fragments (palette_wx*) last
    for f in sorted(glob.glob(os.path.join(LIB, 'palette_*.json')),
                    key=lambda f: (os.path.basename(f).startswith('palette_wx'), os.path.getmtime(f))):
        try:
            d = json.load(open(f))
        except Exception:
            continue
        for k, v in d.items():
            if k.startswith('zz_'):
                continue
            if k in pal:
                if pal[k] != v:
                    if k in base:
                        clash.append(k)
                    else:
                        pal[k] = v
                        refreshed.append(k)
                continue
            pal[k] = v
    json.dump(pal, open(pal_p, 'w'), indent=1)
    print(f'palette: {p0} -> {len(pal)} keys; {len(set(refreshed))} worker keys refreshed to the newest value; {len(clash)} original keys kept as they were{": " + ", ".join(clash[:12]) if clash else ""}')

    used, missing = {}, {}
    for k, e in meta.items():
        for m in e.get('materials', []):
            key = m.split('|')[0].split('.')[0]
            used.setdefault(key, []).append(k)
            if key not in pal and not key.startswith('mk_'):
                missing.setdefault(key, []).append(k)
    print(f'material keys used by models: {len(used)}; missing from palette: {len(missing)}')
    for key, ids in sorted(missing.items()):
        print(f'   MISSING {key}: used by {len(ids)} model(s), e.g. {ids[0]}')


if __name__ == '__main__':
    main()
