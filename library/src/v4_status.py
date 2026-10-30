"""v4_status - what is really built (files on disk), per section / priority / worker, plus problems.
Run: python v4_status.py            (prints a compact report)
"""
import os, sys, json, glob, re, collections
SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
import v4_manifest as M

LIB = M.LIB
OWNER = {}
for code, w in [('A01', 'wa'), ('A02', 'wa'), ('A03', 'wa'), ('A04', 'wa'), ('A05', 'wa'), ('A06', 'wa'), ('A07', 'wa'), ('A08', 'wa'),
                ('B02', 'wb'), ('B07', 'wb'), ('B08', 'wb'),
                ('F01', 'wc'), ('F02', 'wc'), ('F03', 'wc'), ('F04', 'wc'), ('C10', 'wc'), ('E05', 'wc'),
                ('E13', 'wd'), ('R01', 'wd'), ('R02', 'wd'), ('R03', 'wd'),
                ('B03', 'we'), ('B04', 'we'), ('B05', 'we'), ('B06', 'we'), ('B09', 'we'), ('B10', 'we'),
                ('C01', 'wf'), ('C02', 'wf'), ('C03', 'wf'), ('C04', 'wf'), ('C05', 'wf'), ('C06', 'wf'), ('C07', 'wf'), ('C08', 'wf'), ('C09', 'wf'), ('E14', 'wf'),
                ('E01', 'wg'), ('E02', 'wg'), ('E03', 'wg'), ('E04', 'wg'), ('E06', 'wg'), ('E12', 'wg'),
                ('E07', 'wh'), ('E08', 'wh'), ('E09', 'wh'), ('E10', 'wh'), ('E11', 'wh'), ('F09', 'wh'),
                ('F05', 'wi'), ('F06', 'wi'), ('F08', 'wj'), ('F10', 'wj'),
                ('F07', 'wk'), ('F11', 'wk'), ('R04', 'wk'), ('R05', 'wk'), ('R06', 'wk'), ('E15', 'wk'), ('B01', 'old'), ('D01', 'old'), ('D02', 'old'), ('D03', 'old'),
                ('D04', 'old'), ('D05', 'old'), ('D06', 'old'), ('D07', 'old'), ('D08', 'old'), ('D09', 'old')]:
    OWNER[code] = w


def load_meta():
    meta = {}
    for p in [os.path.join(LIB, 'v4_meta.json')] + sorted(glob.glob(os.path.join(LIB, 'v4_meta_*.json'))):
        try:
            meta.update(json.load(open(p)))
        except Exception:
            pass
    if 'EV01_treehouse_a' in meta and 'D01_01_treehouse_a' not in meta:
        meta['D01_01_treehouse_a'] = meta['EV01_treehouse_a']
    return meta


def latest_rows():
    """latest (id -> row) from per-chunk reports; row = [id, tris, size, pieces, max_tris, markers] or [id,'ERROR',tb]"""
    out = {}
    files = sorted(glob.glob(os.path.join(LIB, 'v4_work', 'w?_*_*.json')), key=os.path.getmtime)
    for f in files:
        try:
            d = json.load(open(f))
        except Exception:
            continue
        for r in d.get('rows', []):
            if r and isinstance(r, list):
                out[r[0]] = r
    return out


def main():
    meta = load_meta()
    rows = M.expand()
    rep = latest_rows()
    built = {}
    slotmap = {}
    for k, e in meta.items():
        if os.path.exists(os.path.join(LIB, e.get('category', ''), k + '.fbx')) and os.path.exists(os.path.join(LIB, e.get('category', ''), k + '.blend')):
            slotmap['_'.join(k.split('_')[:2])] = k
    for r in rows:
        k = r['id'] if r['id'] in meta else slotmap.get('_'.join(r['id'].split('_')[:2]))
        if k and k in meta and os.path.exists(os.path.join(LIB, meta[k].get('category', ''), k + '.fbx')):
            built[r['id']] = meta[k]
            built[r['id']]['actual_id'] = k
    tot = len(rows)
    print(f'BUILT {len(built)} / {tot}   (remaining {tot - len(built)})')
    sec = collections.OrderedDict()
    pri = {'P1': [0, 0], 'P2': [0, 0], 'P3': [0, 0]}
    wk = collections.OrderedDict()
    miss = collections.defaultdict(list)
    for r in rows:
        s = sec.setdefault(r['section'], [0, 0]); s[1] += 1
        pri[r['priority']][1] += 1
        w = OWNER.get(r['row'], '?')
        k = wk.setdefault(w, [0, 0]); k[1] += 1
        if r['id'] in built:
            s[0] += 1; pri[r['priority']][0] += 1; k[0] += 1
        else:
            miss[(w, r['row'])].append(r['id'].split('_', 1)[0] + '_' + r['id'].split('_')[1])
    print('SECTIONS  ' + '   '.join(f'{k}:{v[0]}/{v[1]}' for k, v in sec.items()))
    print('PRIORITY  ' + '   '.join(f'{k}:{v[0]}/{v[1]}' for k, v in pri.items()))
    print('WORKERS   ' + '   '.join(f'{k}:{v[0]}/{v[1]}' for k, v in wk.items() if k != 'old'))
    print('NOT BUILT by worker/row (ids = row_nn):')
    for (w, code), ids in sorted(miss.items()):
        print(f'  {w} {code}: {len(ids)}  {",".join(i.split("_")[1] for i in ids)}')
    tris = [e['tris'] for e in built.values() if isinstance(e.get('tris'), (int, float))]
    print(f'TRIS total {sum(tris):,}  avg {sum(tris)//max(1,len(tris)):,}  max {max(tris):,}')
    big = sorted(((e['tris'], i) for i, e in built.items() if isinstance(e.get('tris'), (int, float)) and e['tris'] > 50000), reverse=True)
    print('OVER 50k tris:', ', '.join(f'{i}={t//1000}k' for t, i in big) or 'none')
    bad = [(i, r) for i, r in rep.items() if i in built and len(r) > 4 and isinstance(r[4], (int, float)) and r[4] > 18000]
    print('PIECES over 18k tris:', ', '.join(f'{i}={r[4]}' for i, r in bad) or 'none')
    errs = [i for i, r in rep.items() if len(r) > 1 and r[1] == 'ERROR' and i not in built]
    print('LAST RUN ERROR and not built:', ', '.join(errs) or 'none')
    odd = [(i, e['size']) for i, e in built.items() if e.get('size') and (max(e['size']) > 400 or max(e['size']) < 0.5)]
    print('ODD SIZES:', ', '.join(f'{i}={s}' for i, s in odd) or 'none')
    newcats = collections.Counter(e.get('category') for i, e in built.items() if OWNER.get(re.match(r'([A-Z]\d\d)', i).group(1)) not in (None, 'old'))
    print('NEW MODELS by folder:', dict(newcats))
    # new models only count
    new = [i for i in built if OWNER.get(re.match(r'([A-Z]\d\d)', i).group(1)) != 'old']
    print(f'NEW this session: {len(new)} models')


if __name__ == '__main__':
    main()
