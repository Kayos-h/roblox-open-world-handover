p = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4\dress_v4.py'
t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t
    assert t.count(a) == n, (t.count(a), a[:70])
    t = t.replace(a, b)
rep("    for (x, z) in ((-100, -2205), (-112, -2190), (-92, -2215), (-120, -2200)):",
    "    for (x, z) in ((105, -2200), (95, -2212), (120, -2195), (110, -2185)):")
rep("    # banners flanking the way to the keep\n",
    "    # training yard fence (rectangle x -141..-69, z -2222..-2172); east side keeps a gate gap in the middle\n"
    "    FX0, FX1, FZ0, FZ1 = -141.0, -69.0, -2222.0, -2172.0\n"
    "    for k in range(6):\n"
    "        x = FX0 + 6.0 + k * 12.0\n"
    "        for z in (FZ0, FZ1):\n"
    "            if put(P, 'A100_fence_picket', x, z, 0, 'CastleYardFence', scale=0.96, reg=False):\n"
    "                n['fence'] += 1\n"
    "    for k in range(4):\n"
    "        z = FZ0 + 6.25 + k * 12.5\n"
    "        if put(P, 'A100_fence_picket', FX0, z, 90, 'CastleYardFence', scale=1.0, reg=False):\n"
    "            n['fence'] += 1\n"
    "        if k not in (1, 2):\n"
    "            if put(P, 'A100_fence_picket', FX1, z, 90, 'CastleYardFence', scale=1.0, reg=False):\n"
    "                n['fence'] += 1\n"
    "    add_occ(-105, -2197, 38, 28)\n"
    "    # banners flanking the way to the keep\n")
open(p, 'w', encoding='utf-8').write(t)
print('castle recipe: well moved east, training yard fence added')
