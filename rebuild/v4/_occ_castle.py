import json, glob
V4 = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4'
big = []
for f in glob.glob(V4 + r'\occ_*.json'):
    try:
        for (x, z, hx, hz) in json.load(open(f)):
            if -230 < x < 230 and -2380 < z < -2000 and (hx > 24 or hz > 24):
                big.append((f.split('occ_')[1], x, z, hx, hz))
    except Exception as e:
        pass
for b in sorted(big, key=lambda t: -(t[3] * t[4])):
    print('%-22s centre (%.0f,%.0f) half-extents %.0f x %.0f' % b)
