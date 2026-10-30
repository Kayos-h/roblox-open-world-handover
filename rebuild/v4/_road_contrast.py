from PIL import Image
import math, json
D = r'C:\Users\Nitro\.kiro\crew\workspace\town\shots\v4\r3\h00_topdown.jpg'
im = Image.open(D).convert('RGB')
W, H = im.size
# the top-down camera: (0,4600,-190) looking straight down, FOV 70 vertical. Picture is the 1530x960 crop resampled to 960x602.
# vertical half-extent on the ground = 4600*tan(35deg) = 3221 studs; horizontal = 3221*(960/602) = 5136 studs.
HV = 4600 * math.tan(math.radians(35))
HH = HV * (W / H)
def px(x, z):
    u = (x - 0) / HH * (W / 2) + W / 2
    v = (z + 190) / HV * (H / 2) + H / 2
    return int(u), int(v)
def avg(x, z, r=2):
    u, v = px(x, z)
    pts = [im.getpixel((min(W - 1, max(0, u + dx)), min(H - 1, max(0, v + dy)))) for dx in range(-r, r + 1) for dy in range(-r, r + 1)]
    return tuple(round(sum(p[i] for p in pts) / len(pts)) for i in range(3))
# main south road centreline points (world.json roads 'south'), and nearby offset-grass points
W_ = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\world.json'))
for r in W_['roads'][:5]:
    pts = r['pts']
    print(r['name'], 'w', r['w'], 'mat', r['mat'])
    for k in range(0, len(pts), max(1, len(pts) // 5)):
        x, z = pts[k][0], pts[k][1]
        road = avg(x, z)
        side = avg(x + 90, z + 60)
        print('   (%.0f,%.0f) road px%s  grass px%s  delta %s' % (x, z, road, side, tuple(a - b for a, b in zip(road, side))))
print('pixels per 100 studs: %.2f' % (100 / HH * (W / 2)))
