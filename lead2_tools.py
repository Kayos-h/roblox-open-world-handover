"""lead2_tools - helpers for the second lead pass (87 models, batches).
  python lead2_tools.py archive                      copy (never overwrite) the current files of all 87 worklist models + metas + palettes + src into library\\v5_fix4_archive
  python lead2_tools.py pack <batch> <id,id,...>     writes lead2\\<batch>_ids.json and lead2\\<batch>_pack.json ({id, category}) for the back-view renderer
  python lead2_tools.py compare <batch> <notes.json> before / after-front / after-back sheets lead2\\<batch>_01.jpg ... (8 models per sheet)
"""
import os
import sys
import json
import glob
import shutil
from PIL import Image, ImageDraw, ImageFont

LIB = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
W = os.path.join(LIB, 'v5_work')
L2 = os.path.join(W, 'lead2')
AR = os.path.join(LIB, 'v5_fix4_archive')


def archive():
    ids = json.load(open(os.path.join(L2, 'worklist.json')))
    n = sk = 0

    def cp(src, dst):
        nonlocal n, sk
        if os.path.exists(dst):
            sk += 1
            return
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copytree(src, dst) if os.path.isdir(src) else shutil.copy2(src, dst)
        n += 1
    for i in ids:
        for p in glob.glob(os.path.join(LIB, 'v5_*', i + '*')) + glob.glob(os.path.join(LIB, 'v4_sheets', f'_t_{i}.png')):
            cp(p, os.path.join(AR, os.path.relpath(p, LIB)))
    for p in glob.glob(os.path.join(LIB, 'v4_meta_v*.json')) + glob.glob(os.path.join(LIB, 'palette_v*.json')) + [os.path.join(LIB, 'v4_meta.json'), os.path.join(LIB, 'palette.json')]:
        cp(p, os.path.join(AR, 'meta', os.path.basename(p)))
    for p in glob.glob(os.path.join(LIB, 'src', 'v5*.py')):
        cp(p, os.path.join(AR, 'src', os.path.basename(p)))
    print(f'archive {AR}: copied {n}, already there {sk}')


def pack(batch, ids):
    meta = {}
    for f in glob.glob(os.path.join(LIB, 'v4_meta_v[a-j].json')):
        meta.update(json.load(open(f)))
    full = []
    for want in ids:
        hit = [k for k in meta if k == want or k.startswith(want)]
        assert len(hit) == 1, (want, hit)
        full.append(hit[0])
    json.dump(full, open(os.path.join(L2, f'{batch}_ids.json'), 'w'), indent=1)
    json.dump([{'id': i, 'category': meta[i]['category']} for i in full], open(os.path.join(L2, f'{batch}_pack.json'), 'w'), indent=1)
    print(batch, len(full), 'ids')


def compare(batch, notes_path):
    ids = json.load(open(os.path.join(L2, f'{batch}_ids.json')))
    NOTE = json.load(open(notes_path))
    f = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 15)
    fs = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 13)
    CELL, GAP, HEAD, COLS, ROWS = 300, 6, 46, 2, 4
    PER = COLS * ROWS
    cw = 3 * CELL + 2 * GAP
    out = []
    for s in range(0, len(ids), PER):
        part = ids[s:s + PER]
        rows = (len(part) + COLS - 1) // COLS
        sheet = Image.new('RGB', (COLS * (cw + 14), rows * (CELL + HEAD + 8)), (24, 24, 28))
        d = ImageDraw.Draw(sheet)
        for k, mid in enumerate(part):
            c, r = k % COLS, k // COLS
            x0, y0 = c * (cw + 14), r * (CELL + HEAD + 8)
            d.text((x0 + 4, y0 + 2), mid[:60], fill=(240, 240, 244), font=f)
            d.text((x0 + 4, y0 + 22), NOTE.get(mid[:7], NOTE.get(mid, '')), fill=(170, 200, 180), font=fs)
            srcs = [os.path.join(AR, 'v4_sheets', f'_t_{mid}.png'), os.path.join(LIB, 'v4_sheets', f'_t_{mid}.png'), os.path.join(L2, 'back', f'{mid}.png')]
            for j, (p, lab) in enumerate(zip(srcs, ('BEFORE', 'AFTER front', 'AFTER back'))):
                xx = x0 + j * (CELL + GAP)
                if os.path.exists(p):
                    sheet.paste(Image.open(p).convert('RGB').resize((CELL, CELL), Image.LANCZOS), (xx, y0 + HEAD))
                d.rectangle([xx, y0 + HEAD, xx + 92, y0 + HEAD + 18], fill=(0, 0, 0))
                d.text((xx + 4, y0 + HEAD + 1), lab, fill=(255, 190, 150) if j == 0 else (190, 240, 200), font=fs)
        p = os.path.join(L2, f'{batch}_{s // PER + 1:02d}.jpg')
        sheet.save(p, 'JPEG', quality=84)
        out.append(p)
    print(len(ids), 'models on', len(out), 'sheets')
    for p in out:
        print(p)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'archive':
        archive()
    elif cmd == 'pack':
        pack(sys.argv[2], [x for x in sys.argv[3].split(',') if x])
    elif cmd == 'compare':
        compare(sys.argv[2], sys.argv[3])
