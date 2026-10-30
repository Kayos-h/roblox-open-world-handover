from PIL import Image
import os
R3 = r'C:\Users\Nitro\.kiro\crew\workspace\town\shots\v4\r3'
R4 = r'C:\Users\Nitro\.kiro\crew\workspace\town\shots\v4\r4'
def col_profile(path, x, ys):
    im = Image.open(path).convert('RGB')
    out = []
    for y in ys:
        px = [im.getpixel((min(959, x + dx), y)) for dx in (-6, -3, 0, 3, 6)]
        out.append(tuple(round(sum(p[i] for p in px) / 5) for i in range(3)))
    return out
ys = list(range(60, 600, 36))
for label, p in (('R3 g02_se_beach', os.path.join(R3, 'g02_se_beach.jpg')), ('R4 g_se_beach', os.path.join(R4, 'g_se_beach.jpg')), ('R4 g_south_coast', os.path.join(R4, 'g_south_coast.jpg'))):
    prof = col_profile(p, 480, ys)
    print(label)
    for y, c in zip(ys, prof):
        print('   y=%3d %s' % (y, c))
# find the horizon row in R4 g_se_beach: biggest brightness jump going down
im = Image.open(os.path.join(R4, 'g_se_beach.jpg')).convert('RGB')
prev = None
best = (0, 0)
for y in range(20, 580):
    c = im.getpixel((480, y))
    b = sum(c) / 3
    if prev is not None and abs(b - prev) > best[0]:
        best = (abs(b - prev), y)
    prev = b
print('largest vertical brightness step at y=%d (%.0f)' % (best[1], best[0]))
for y in range(max(20, best[1] - 14), best[1] + 24, 4):
    print('   y=%d %s' % (y, im.getpixel((480, y))))
