from PIL import Image
import sys, os
D = r'C:\Users\Nitro\.kiro\crew\workspace\town\shots\v4\r3'
def patch(im, cx, cy, r=6):
    w, h = im.size
    px = [im.getpixel((min(w - 1, max(0, cx + dx)), min(h - 1, max(0, cy + dy)))) for dx in range(-r, r + 1, 3) for dy in range(-r, r + 1, 3)]
    n = len(px)
    return tuple(round(sum(p[i] for p in px) / n) for i in range(3))
for name, pts in (('h00_topdown', [(30, 30), (930, 30), (30, 570), (930, 570), (480, 20), (480, 585), (140, 300)]),
                  ('h01_overview_south', [(20, 400), (940, 400), (480, 580), (480, 300)]),
                  ('g02_se_beach', [(480, 100), (480, 300), (480, 500), (100, 500), (860, 500)]),
                  ('g05_islet_shoal', [(100, 300), (860, 300), (480, 560), (480, 150)]),
                  ('g01_south_coast', [(120, 520), (840, 520), (480, 560)])):
    im = Image.open(os.path.join(D, name + '.jpg')).convert('RGB')
    print(name, im.size, ' | '.join('(%d,%d)->%s' % (x, y, patch(im, x, y)) for x, y in pts))
