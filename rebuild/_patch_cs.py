s = open('countryside.py', encoding='utf-8').read()
rep = [
    ("P = Plan('v2_country', seed=77)", "P = Plan('v3_country', seed=77)"),
    ("    if abs(x) > 3300 or abs(z) > 3300:\n        return False\n    if -520 <= x <= 520 and -840 <= z <= 510:\n        return False",
     "    if abs(x) > 2300 or abs(z) > 2500:\n        return False\n    if -360 <= x <= 360 and -585 <= z <= 345:\n        return False"),
    ("def in_mtn(x, z):\n    return 1650 <= x <= 3350 and -2750 <= z <= -1000 and not (2340 <= x <= 2740 and -1490 <= z <= -1110)",
     "def in_mtn(x, z):\n    return W.ground_no_noise(x, z) > 235"),
    ("def ok(x, z, road_gap=8, allow_steep=0.45):", "def ok(x, z, road_gap=8, allow_steep=0.55):"),
    ("            if not ok(tx, tz, road_gap=9, allow_steep=0.6):", "            if not ok(tx, tz, road_gap=9, allow_steep=0.7):"),
    ("    for (x, z, r) in ((18, 745, 120), (14, -835, 0), (515, 14, 90), (-515, 14, 270), (14, 505, 180), (2348, -918, 290), (-1925, -540, 100), (2060, 1430, 330), (-640, 2268, 180)):",
     "    for (x, z, r) in ((22, 470, 120), (16, -575, 0), (345, -36, 90), (-345, -36, 270), (16, 345, 180), (1515, -540, 290), (-1545, -110, 100), (1390, 930, 330), (-460, 1392, 180)):"),
    ("""    spots = [
        ('H03_ruins_1', -700, -1250, 20), ('H04_ruins_2', -760, -1210, 110), ('H11_standing_stone_circle', 1300, 250, 0),
        ('H02_abandoned_watchtower', 1300, -950, 35), ('H05_traveller_campsite', -1300, -150, 200), ('H05_traveller_campsite', 2510, 240, 90),
        ('H06_wagon_wreck', 1180, 1330, 140), ('H01_roadside_shrine', -640, 110, 90), ('H01_roadside_shrine', 680, -150, 250),
        ('H01_roadside_shrine', 70, -1180, 180), ('H01_roadside_shrine', -120, 1350, 20), ('H03_ruins_1', 950, -1600, 300),
        ('H10_working_windmill', -980, 1600, 30), ('H02_abandoned_watchtower', -1500, -1650, 0), ('H11_standing_stone_circle', -2150, 300, 0),
        ('A65_rock_arch', -1600, 1100, 40), ('A65_rock_arch', 2200, 1100, 120), ('H06_wagon_wreck', -1650, 800, 60),
    ]""", """    spots = [
        ('H03_ruins_1', -760, -985, 20), ('H04_ruins_2', -720, -950, 110), ('H11_standing_stone_circle', 760, 470, 0),
        ('H02_abandoned_watchtower', 600, -700, 35), ('H05_traveller_campsite', -900, -170, 200), ('H05_traveller_campsite', 1640, 120, 90),
        ('H06_wagon_wreck', 760, 860, 140), ('H01_roadside_shrine', -470, -40, 90), ('H01_roadside_shrine', 520, -95, 250),
        ('H01_roadside_shrine', 40, -800, 180), ('H01_roadside_shrine', -90, 780, 20), ('H03_ruins_1', 520, -1150, 300),
        ('H10_working_windmill', -1000, 1350, 30), ('H02_abandoned_watchtower', -880, -1660, 0), ('H11_standing_stone_circle', -900, 300, 0),
        ('A65_rock_arch', -1050, 700, 40), ('A65_rock_arch', 1450, 1600, 120), ('H06_wagon_wreck', -1250, 600, 60),
        ('H02_abandoned_watchtower', 1700, 300, 10), ('H03_ruins_1', 120, 1450, 80), ('H11_standing_stone_circle', -330, -950, 0),
    ]"""),
    ("""    farm(-760, 780, 20, name='Farm_West')
    farm(720, 520, -15, name='Farm_East')
    farm(880, 1250, 25, cols=3, rows=3, name='Farm_South')
    farm(-420, -1050, 5, cols=3, rows=2, name='Farm_North')
    for name, s in (('north', 110), ('west', 90), ('south', 110), ('southeast', 110), ('east', 640)):
        arch(name, s)""", """    farm(-560, 620, 20, name='Farm_West')
    farm(270, 770, -10, name='Farm_East')
    farm(-560, 1010, 25, cols=3, rows=3, name='Farm_South')
    farm(-380, -760, 5, cols=3, rows=2, name='Farm_North')
    for name, s in (('north', 90), ('west', 70), ('south', 90), ('southeast', 90), ('east', 560)):
        arch(name, s)"""),
    ("    P.save(r'C:\\Users\\Nitro\\.kiro\\crew\\workspace\\town\\mapplan\\v2_country.json')", "    P.save(r'C:\\Users\\Nitro\\.kiro\\crew\\workspace\\town\\mapplan\\v3_country.json')"),
    ("        for rr in range(3300, 2400, -30):\n            x, z = math.cos(a) * rr, math.sin(a) * rr * (3390 / 3300 if math.sin(a) < 0 else 3040 / 3300)",
     "        for rr in range(2250, 1500, -25):\n            x, z = math.cos(a) * rr, math.sin(a) * rr * (2480 / 2200 if math.sin(a) < 0 else 2000 / 2200)"),
    ("    for k in range(260):", "    for k in range(200):"),
]
for a, b in rep:
    n = s.count(a)
    s = s.replace(a, b)
    print(n, a[:60].replace('\n', ' '))
open('countryside.py', 'w', encoding='utf-8').write(s)
