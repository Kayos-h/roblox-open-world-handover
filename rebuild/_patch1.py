s = open('towns.py', encoding='utf-8').read()
rep = [
    ("P.blocks.append(obb(cx, cz, rx, rz, 0))", "P.sblocks.append(obb(cx, cz, rx, rz, 0))"),
    ("P.blocks.append(obb(1880, 1695, 40, 40, 0))", "P.sblocks.append(obb(1880, 1695, 40, 40, 0))"),
    ("P.blocks.append(obb(-600, 2540, 40, 32, 0))", "P.sblocks.append(obb(-600, 2540, 40, 32, 0))"),
    ("P.blocks.append(obb(2502, -1300, 24, 24, 0))", "P.sblocks.append(obb(2502, -1300, 24, 24, 0))"),
    ("'MarketSquare', block=False, pad=0.5)", "'MarketSquare', block=False, pad=0.5, streets=False)"),
    ("P.put('C26_vendor_cart', x, z, P.rng.uniform(0, 360), 'MarketSquare', block=False)", "P.put('C26_vendor_cart', x, z, P.rng.uniform(0, 360), 'MarketSquare', block=False, streets=False)"),
    ("'Lamps', block=False, pad=0.2)", "'Lamps', block=False, pad=0.2, streets=False)"),
    ("'Plazas', block=False, pad=0.5)", "'Plazas', block=False, pad=0.5, streets=False)"),
    ("'Square', block=False)", "'Square', block=False, streets=False)"),
    ("P.put('A15_lamp_iron_city', x, 2872, 0, 'Lamps', block=False)", "P.put('A15_lamp_iron_city', x, 2872, 0, 'Lamps', block=False, streets=False)"),
    ("'Waterfront', block=False)", "'Waterfront', block=False, streets=False)"),
    ("'GateSquare', block=False)", "'GateSquare', block=False, streets=False)"),
]
for a, b in rep:
    n = s.count(a)
    s = s.replace(a, b)
    print(n, a[:50])
open('towns.py', 'w', encoding='utf-8').write(s)
