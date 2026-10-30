import sys, os
from PIL import Image
d = sys.argv[1]
def avg(im, cx, cy, r=14):
    w, h = im.size
    px = [im.getpixel((min(w - 1, max(0, cx + dx)), min(h - 1, max(0, cy + dy)))) for dx in range(-r, r + 1, 4) for dy in range(-r, r + 1, 4)]
    return tuple(round(sum(p[i] for p in px) / len(px)) for i in range(3))
for f in sorted(os.listdir(d)):
    if not f.endswith('.jpg') or not f.startswith('s'):
        continue
    im = Image.open(os.path.join(d, f)).convert('RGB')
    pts = [(480, 300), (200, 150), (760, 450), (480, 540), (480, 80)]
    print(f, ' '.join('%s' % (avg(im, x, y),) for x, y in pts))
