"""_blackcheck - which of the changed models have an all-black or near-black thumbnail?
Run: python _blackcheck.py   (reads library\\v4_work\\recheck_ids.txt)
"""
import os
from PIL import Image, ImageStat

LIB = r'C:\Users\Nitro\.kiro\crew\workspace\town\library'
import sys
ids = sys.argv[1:] or [l.strip() for l in open(os.path.join(LIB, 'v4_work', 'recheck_ids.txt'), encoding='utf-8') if l.strip()]
bad = []
for i in ids:
    p = os.path.join(LIB, 'v4_sheets', '_t_' + i + '.png')
    if not os.path.exists(p):
        bad.append((i, 'missing', 0))
        continue
    im = Image.open(p).convert('RGB')
    st = ImageStat.Stat(im)
    mean = sum(st.mean) / 3.0
    # share of pixels that are almost black
    px = im.resize((64, 64)).getdata()
    dark = sum(1 for r, g, b in px if r + g + b < 30) / float(64 * 64)
    if mean < 40 or dark > 0.5:
        bad.append((i, 'dark', round(mean, 1), round(dark, 2)))
print('checked', len(ids), 'thumbnails; dark or missing:', len(bad))
for b in bad:
    print('  ', b)
