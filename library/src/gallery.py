"""Build the GitHub photo gallery for the V4 Blender models.
Reads library\\v4_meta*.json + the manifest, converts preview PNGs to small JPEGs and writes README.md + one page per section.
Run:  python gallery.py   (safe to re-run; only changed images are re-encoded)
"""
import os, sys, json, glob, re, time, html
from PIL import Image

SRC = r'C:\Users\Nitro\.kiro\crew\workspace\town\library\src'
sys.path.insert(0, SRC)
import v4_manifest as M

LIB = M.LIB
SHEETS = os.path.join(LIB, 'v4_sheets')
OUT = r'C:\Users\Nitro\.kiro\crew\workspace\town\gallery_repo'
IMG = os.path.join(OUT, 'images')
PAGES = os.path.join(OUT, 'sections')
COLS = 3
THUMB_W = 330


def load_meta():
    meta = {}
    paths = [os.path.join(LIB, 'v4_meta.json')] + sorted(glob.glob(os.path.join(LIB, 'v4_meta_*.json')))
    for p in paths:
        try:
            meta.update(json.load(open(p)))
        except Exception:
            pass
    if 'D01_01_treehouse_a' not in meta and 'EV01_treehouse_a' in meta:
        meta['D01_01_treehouse_a'] = meta['EV01_treehouse_a']
    return meta


def jpg(src, dst, width, q=82):
    if not os.path.exists(src):
        return False
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        return True
    try:
        im = Image.open(src).convert('RGB')
    except Exception:
        return False
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, 'JPEG', quality=q, optimize=True)
    return True


def resolve(rows, meta):
    """manifest id -> actual saved id. Some workers used descriptive names (F05_01_bush_round): match by slot (F05_01)."""
    ok = {k: e for k, e in meta.items() if os.path.exists(os.path.join(LIB, e.get('category', ''), k + '.fbx'))}
    slot = {'_'.join(k.split('_')[:2]): k for k in ok}
    out = {}
    for r in rows:
        k = r['id'] if r['id'] in ok else slot.get('_'.join(r['id'].split('_')[:2]))
        if k:
            out[r['id']] = k
    return out


def fmt_tris(n):
    return f'{n / 1000:.1f}k' if isinstance(n, (int, float)) and n >= 1000 else str(n)


def size_txt(e):
    s = e.get('size') or []
    return ' x '.join(str(round(v)) for v in s) if s else '?'


def main():
    os.makedirs(IMG, exist_ok=True)
    os.makedirs(PAGES, exist_ok=True)
    meta = load_meta()
    rows = M.expand()
    by_row = {}
    for r in rows:
        by_row.setdefault(r['row'], []).append(r)
    actual = resolve(rows, meta)          # manifest id -> saved id
    built_ids = set(actual)
    total, nb = len(rows), len(built_ids)

    # images
    nthumb = nquad = 0
    for mid in built_ids:
        aid = actual[mid]
        if jpg(os.path.join(SHEETS, f'_t_{aid}.png'), os.path.join(IMG, 'thumbs', mid + '.jpg'), THUMB_W + 50):
            nthumb += 1
        if jpg(os.path.join(SHEETS, aid + '.png'), os.path.join(IMG, 'quads', mid + '.jpg'), 1100):
            nquad += 1
    sheets = []
    for p in sorted(glob.glob(os.path.join(SHEETS, '*.png')), key=os.path.getmtime):
        n = os.path.basename(p)[:-4]
        if re.match(r'^(w[a-z]_.+_\d+|batch.+)$', n):
            if jpg(p, os.path.join(IMG, 'sheets', n + '.jpg'), 1500, q=80):
                sheets.append((n, os.path.getmtime(p)))

    now = time.strftime('%Y-%m-%d %H:%M')
    sec_files = {}
    for sec, (title, defs) in M.SECTIONS.items():
        sb = sum(1 for r in rows if r['section'] == sec and r['id'] in built_ids)
        st = sum(1 for r in rows if r['section'] == sec)
        slug = f'{sec}_' + re.sub(r'[^a-z0-9]+', '_', title.lower()).strip('_')[:40]
        sec_files[sec] = (slug, title, sb, st)
        L = [f'# {sec}. {title}', '', f'**{sb} of {st} models built.** Updated {now}. [Back to overview](../README.md)', '']
        for d in defs:
            code, base, n, pr, desc = d[:5]
            grp = by_row.get(code, [])
            gb = sum(1 for r in grp if r['id'] in built_ids)
            L += [f'## {code} {base.replace("_", " ")} ({gb}/{len(grp)}, {pr})', '', f'_{desc or "no notes"}_', '', '<table>']
            for i in range(0, len(grp), COLS):
                L.append('<tr>')
                for r in grp[i:i + COLS]:
                    mid = r['id']
                    if mid in built_ids and os.path.exists(os.path.join(IMG, 'thumbs', mid + '.jpg')):
                        e = meta[actual[mid]]
                        cap = f'<b>{actual[mid]}</b><br>{fmt_tris(e.get("tris", "?"))} tris, {size_txt(e)}'
                        if e.get('door'):
                            cap += ', door marker'
                        if os.path.exists(os.path.join(IMG, 'quads', mid + '.jpg')):
                            cap += f'<br><a href="../images/quads/{mid}.jpg">4 angles</a>'
                        L.append(f'<td align="center" valign="top" width="{100 // COLS}%"><img src="../images/thumbs/{mid}.jpg" width="{THUMB_W}"><br><sub>{cap}</sub></td>')
                    else:
                        L.append(f'<td align="center" valign="top" width="{100 // COLS}%"><sub><b>{mid}</b><br>not built yet</sub></td>')
                for _ in range(COLS - len(grp[i:i + COLS])):
                    L.append('<td></td>')
                L.append('</tr>')
            L += ['</table>', '']
        open(os.path.join(PAGES, slug + '.md'), 'w', encoding='utf-8').write('\n'.join(L))

    # sheets page
    S = ['# Batch contact sheets', '', f'Every build batch as one sheet (up to 12 models each). Updated {now}. [Back to overview](README.md)', '']
    for n, mt in sheets:
        S += [f'### {n}', '', f'![{n}](images/sheets/{n}.jpg)', '']
    open(os.path.join(OUT, 'SHEETS.md'), 'w', encoding='utf-8').write('\n'.join(S))

    tris = sum(meta[actual[m]].get('tris', 0) for m in built_ids if isinstance(meta[actual[m]].get('tris', 0), (int, float)))
    p = {k: [0, 0] for k in ('P1', 'P2', 'P3')}
    for r in rows:
        p[r['priority']][1] += 1
        p[r['priority']][0] += r['id'] in built_ids
    R = ['# Roblox map: Blender model gallery (V4)', '',
         f'Photos of every model in the V4 list, one page per section. **{nb} of {total} models built.** Last updated {now}.', '',
         'Each picture is a 3/4 render straight from Blender. "4 angles" links open a front/back/detail/side view for the large pieces. '
         'The models are original designs for a Roblox game; units are studs (1 unit = 1 stud), models face -Y, origin at the bottom centre. '
         'This repo holds photos only; the .blend/.fbx files live on the author\'s PC.', '',
         '| Section | Title | Built | Page |', '|---|---|---|---|']
    for sec, (slug, title, sb, st) in sec_files.items():
        R.append(f'| {sec} | {title} | {sb} / {st} | [open](sections/{slug}.md) |')
    R += ['', f'**By priority:** P1 {p["P1"][0]}/{p["P1"][1]}, P2 {p["P2"][0]}/{p["P2"][1]}, P3 {p["P3"][0]}/{p["P3"][1]}.  ', f'**Total triangles of built models:** {tris:,}.', '',
          f'See also: [all batch contact sheets](SHEETS.md) ({len(sheets)} sheets).']
    open(os.path.join(OUT, 'README.md'), 'w', encoding='utf-8').write('\n'.join(R))
    print(f'gallery: built {nb}/{total}; thumbs updated {nthumb}, quads {nquad}, sheets {len(sheets)}; out {OUT}')


if __name__ == '__main__':
    main()
