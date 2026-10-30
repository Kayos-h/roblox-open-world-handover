"""Build the independent-review pack: labelled contact sheets of EVERY built model, 12 per sheet, in manifest order
(siblings sit next to each other so repetition and variety are easy to judge), plus INDEX.md.
Run: python review_pack.py            -> library\\v4_work\\review_pack\\review_001.jpg ...  + INDEX.md
"""
import os, sys, json, glob
from PIL import Image, ImageDraw, ImageFont

SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
import v4_manifest as M
import v4_status as S

LIB = M.LIB
SHEETS = os.path.join(LIB, 'v4_sheets')
OUT = os.path.join(LIB, 'v4_work', 'review_pack')
COLS, ROWS, CELL, LABEL_H = 4, 3, 360, 34
PER = COLS * ROWS


def font(sz):
    for p in (r'C:\Windows\Fonts\segoeui.ttf', r'C:\Windows\Fonts\arial.ttf'):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def main():
    args = sys.argv[1:]   # optional: --only <file with one saved id per line>  --out <folder>
    only = None
    out = OUT
    if '--only' in args:
        only = {l.strip() for l in open(args[args.index('--only') + 1], encoding='utf-8') if l.strip()}
    if '--out' in args:
        out = args[args.index('--out') + 1]
    os.makedirs(out, exist_ok=True)
    for f in glob.glob(os.path.join(out, 'review_*.jpg')):
        os.remove(f)
    meta = S.load_meta()
    rows = M.expand()
    ok = {k: e for k, e in meta.items() if os.path.exists(os.path.join(LIB, e.get('category', ''), k + '.fbx'))}
    slot = {'_'.join(k.split('_')[:2]): k for k in ok}
    items = []
    for r in rows:
        k = r['id'] if r['id'] in ok else slot.get('_'.join(r['id'].split('_')[:2]))
        if k:
            items.append((r['id'], k, ok[k]))
    if only is not None:
        items = [it for it in items if it[1] in only]
    f1, f2 = font(15), font(12)
    idx = ['# Review pack index', '', f'{len(items)} built models, {PER} per sheet (4 columns x 3 rows, left to right, top to bottom). Cell caption = saved id, triangles, size in studs (x y z).', '']
    n_sheets = (len(items) + PER - 1) // PER
    missing = []
    for s in range(n_sheets):
        part = items[s * PER:(s + 1) * PER]
        W, H = COLS * CELL, ROWS * (CELL + LABEL_H)
        sheet = Image.new('RGB', (W, H), (24, 24, 28))
        d = ImageDraw.Draw(sheet)
        idx.append(f'## review_{s + 1:03d}.jpg')
        for i, (mid, aid, e) in enumerate(part):
            c, r = i % COLS, i // COLS
            x0, y0 = c * CELL, r * (CELL + LABEL_H)
            p = os.path.join(SHEETS, f'_t_{aid}.png')
            if os.path.exists(p):
                try:
                    im = Image.open(p).convert('RGB').resize((CELL, CELL), Image.LANCZOS)
                    sheet.paste(im, (x0, y0))
                except Exception:
                    missing.append(aid)
            else:
                missing.append(aid)
                d.text((x0 + 10, y0 + CELL // 2), 'NO PHOTO', fill=(255, 120, 120), font=f1)
            size = ' x '.join(str(round(v)) for v in (e.get('size') or []))
            tri = e.get('tris', '?')
            tri = f'{tri / 1000:.1f}k' if isinstance(tri, (int, float)) and tri >= 1000 else str(tri)
            d.rectangle([x0, y0 + CELL, x0 + CELL - 1, y0 + CELL + LABEL_H - 1], fill=(40, 40, 48))
            d.text((x0 + 6, y0 + CELL + 2), aid[:46], fill=(235, 235, 240), font=f1)
            d.text((x0 + 6, y0 + CELL + 19), f'{tri} tris   {size}', fill=(170, 200, 230), font=f2)
            idx.append(f'- {i + 1:>2}. {aid}  ({tri} tris, {size})')
        sheet.save(os.path.join(out, f'review_{s + 1:03d}.jpg'), 'JPEG', quality=86)
        idx.append('')
    if missing:
        idx += ['## Models without a photo', ''] + [f'- {m}' for m in missing]
    open(os.path.join(out, 'INDEX.md'), 'w', encoding='utf-8').write('\n'.join(idx))
    print(f'review pack: {len(items)} models on {n_sheets} sheets; no photo for {len(missing)}; out {out}')


if __name__ == '__main__':
    main()
