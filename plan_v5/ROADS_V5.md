# Roads v5: route table (offline search on the planned terrain)

Least-cost routes on the 24-stud grid after the planned landform changes. Grade-limited profile (max 0.16) gives the cuts (tunnel when the cut is deeper than 22 studs for 72+ studs) and the fills (viaduct when the road stands 14+ studs above the ground for 48+ studs).

| Road | From - to | Length | Top | Steepest 96 studs | Climb | Hairpins | Bridges | Tunnels | Cliff galleries | Viaduct fills |
|---|---|---|---|---|---|---|---|---|---|---|
| North road | town1_n - capital_s | 720 | 29 | 0.14 | 21 | 0 | 0 | 0 | 0 | 0 |
| South road | town1 - harbour | 1763 | 56 | 0.24 | 54 | 0 | 1 | 0 | 0 | 0 |
| Farm road | town1 - west_village | 2908 | 76 | 0.22 | 101 | 0 | 2 | 0 | 0 | 0 |
| Greenwood road | west_village - elf_e | 1281 | 66 | 0.10 | 6 | 0 | 0 | 0 | 0 | 0 |
| East road | town1 - alpine | 2167 | 128 | 0.20 | 128 | 1 | 1 | 0 | 0 | 0 |
| Gale Pass road | capital_s - low_pass | 1573 | 177 | 0.19 | 156 | 2 | 1 | 0 | 0 | 0 |
| Lake shore road | alpine - low_pass | 774 | 177 | 0.14 | 52 | 0 | 0 | 0 | 0 | 0 |
| Roof road | low_pass - wizard_tower | 997 | 325 | 0.32 | 147 | 4 | 0 | 1 | 0 | 0 |
| Tarn path | wizard_tower - tarn_shore | 253 | 324 | 0.05 | 0 | 0 | 1 | 0 | 0 | 0 |
| Cloud stair (carved switchback stair) | tarn_shore - dragon_a | 286 | 340 | 0.50 | 16 | 0 | 0 | 0 | 1 | 1 |
| Dragonback road (lower) | alpine - dragon_a | 901 | 292 | 0.53 | 113 | 3 | 0 | 1 | 1 | 0 |
| Dragonback road (terraces) | dragon_a - dragon_b | 517 | 295 | 0.49 | 0 | 1 | 0 | 1 | 0 | 1 |
| Dragonback road (east) | dragon_b - gorge_s | 902 | 264 | 0.32 | 76 | 2 | 0 | 1 | 1 | 0 |
| Gorge crossing | gorge_s - hidden_monastery | 230 | 208 | 1.13 | 0 | 0 | 1 | 0 | 1 | 1 |
| Highland descent | gorge_s - skull_city | 1130 | 212 | 0.27 | 2 | 2 | 0 | 0 | 1 | 0 |
| Ash road | alpine - skull_city | 1324 | 126 | 0.19 | 19 | 2 | 1 | 0 | 0 | 0 |
| Crater spur | town1 - crater_rim | 1247 | 90 | 0.19 | 85 | 0 | 1 | 0 | 0 | 0 |
| Old road | town1 - ruins_e | 1255 | 63 | 0.17 | 61 | 0 | 1 | 0 | 0 | 0 |
| Dune road | ruins_e - rusty | 918 | 62 | 0.22 | 3 | 0 | 0 | 0 | 0 | 0 |
| Temple road | rusty - ring_temple | 434 | 34 | 0.13 | 15 | 0 | 0 | 0 | 0 | 0 |
| Buried road | ring_temple - buried_temple | 705 | 36 | 0.20 | 12 | 0 | 0 | 0 | 0 | 0 |
| Ruin road | elf_e - ruined_castle | 1197 | 66 | 0.13 | 58 | 0 | 0 | 0 | 0 | 0 |
| West gate road | ruined_castle - capital_s | 955 | 65 | 0.11 | 1 | 0 | 1 | 0 | 0 | 0 |
| Coast road | harbour - west_village | 1377 | 74 | 0.10 | 54 | 0 | 1 | 0 | 0 | 0 |
| Ember road | skull_city - crater_rim | 1685 | 104 | 0.18 | 56 | 1 | 1 | 0 | 0 | 0 |
| Trade road | rusty - harbour | 2587 | 56 | 0.13 | 41 | 0 | 2 | 0 | 0 | 0 |

Total new and reused road length: 30086 studs. Unique bridges: 12 (rope_suspension 1, stone_arch 7, timber_cantilever 1, towered_stone 3). Tunnels: 3.

## Bridges

| Road | River | Kind | Span | Ground y | At (x, z) |
|---|---|---|---|---|---|
| Gorge crossing | ne_a_dn | rope_suspension | 116 | 94 | (2448, -1358) |
| Farm road | greenheart | stone_arch | 28 | 68 | (-1236, 660) |
| East road | trunk_east | stone_arch | 32 | 31 | (628, -103) |
| Gale Pass road | trunk_east | stone_arch | 32 | 88 | (355, -883) |
| Ash road | silverrun | stone_arch | 28 | 43 | (1935, -590) |
| Old road | trunk_east | stone_arch | 32 | 19 | (652, 264) |
| Coast road | greenheart | stone_arch | 28 | 65 | (-1216, 584) |
| Trade road | trunk_east | stone_arch | 32 | 42 | (654, 751) |
| Tarn path | meltwater | timber_cantilever | 28 | 318 | (1552, -1415) |
| South road | trunk_west | towered_stone | 32 | 18 | (-418, 1556) |
| Farm road | trunk_west | towered_stone | 32 | 27 | (-442, 1391) |
| West gate road | trunk_west | towered_stone | 32 | 55 | (-306, -1080) |

## Tunnels

| Road | From | To | Length | Depth |
|---|---|---|---|---|
| Roof road | (1003, -1148) | (1040, -1232) | 120 | 24 |
| Dragonback road (lower) | (1816, -1241) | (1800, -1290) | 216 | 57 |
| Dragonback road (east) | (2191, -1136) | (2226, -1169) | 72 | 26 |
