# V5 worker plan

Nine worker queues. Blender is parked; nothing here has run. When it is allowed: `v4run.ps1 -Module <module> -Worker <worker> -Batch <batch>` per batch (two Blender processes at a time), then `python v4_merge.py`, then `upload_v5.ps1`.

| Worker | Module (create in library/src) | Models | Est. worker-hours | Content |
|---|---|---|---|---|
| va | v5_va.py | 9 | 1.0 | Wizard tower exterior (do first, most review rounds) |
| vb | v5_vb.py | 18 | 1.5 | Wizard tower interior and the circular map |
| vc | v5_vc.py | 37 | 2.0 | Himalayan road kit and natural entrances |
| vd | v5_vd.py | 55 | 4.5 | Capital |
| ve | v5_ve.py | 33 | 2.1 | Elf valley and Town 1 |
| vf | v5_vf.py | 25 | 2.8 | Landmark heroes, trees and coast |
| vg | v5_vg.py | 62 | 4.4 | Highlands, forest and marsh extras |
| vh | v5_vh.py | 70 | 4.6 | Desert and Skull City |
| vi | v5_vi.py | 91 | 5.7 | Plains, ruins, coast extras, roads and sky |

Total models in the queues: 400; worker-hours 28.6 (about 13.3 hours of wall time with 3 active workers plus 40% for reviews and fixes). Rows not in any queue: none (RW01 reworks are done by hand on the old models).

## va: Wizard tower exterior (do first, most review rounds)

| Batch | Category folder | Rows | Models | Est. minutes |
|---|---|---|---|---|
| tower_shell | v5_wizard | WT01 | 1 | 28 |
| tower_porch | v5_wizard | WT12, WT11 | 2 | 12 |
| tower_terrace | v5_wizard | WT13 | 6 | 19 |

```
powershell -File library\src\v4run.ps1 -Module v5_va -Worker va -Batch tower_shell
powershell -File library\src\v4run.ps1 -Module v5_va -Worker va -Batch tower_porch
powershell -File library\src\v4run.ps1 -Module v5_va -Worker va -Batch tower_terrace
```

## vb: Wizard tower interior and the circular map

| Batch | Category folder | Rows | Models | Est. minutes |
|---|---|---|---|---|
| interior_shell | v5_wizard | WT02 | 1 | 17 |
| map_table | v5_wizard | WT05, WT06 | 2 | 16 |
| shelves | v5_wizard | WT03, WT04 | 5 | 20 |
| furniture | v5_wizard | WT07, WT08, WT09, WT10 | 10 | 37 |

```
powershell -File library\src\v4run.ps1 -Module v5_vb -Worker vb -Batch interior_shell
powershell -File library\src\v4run.ps1 -Module v5_vb -Worker vb -Batch map_table
powershell -File library\src\v4run.ps1 -Module v5_vb -Worker vb -Batch shelves
powershell -File library\src\v4run.ps1 -Module v5_vb -Worker vb -Batch furniture
```

## vc: Himalayan road kit and natural entrances

| Batch | Category folder | Rows | Models | Est. minutes |
|---|---|---|---|---|
| bridges | v5_himalaya | HM01 | 3 | 12 |
| tunnels | v5_himalaya | HM03, HM04 | 5 | 19 |
| signs | v5_entrances | NE01 | 6 | 18 |
| road_extras | v5_himalaya | HM02, HM05, HM06, HM07, HM08, HM09 | 19 | 62 |
| boulders | v5_entrances | NE02 | 4 | 11 |

```
powershell -File library\src\v4run.ps1 -Module v5_vc -Worker vc -Batch bridges
powershell -File library\src\v4run.ps1 -Module v5_vc -Worker vc -Batch tunnels
powershell -File library\src\v4run.ps1 -Module v5_vc -Worker vc -Batch signs
powershell -File library\src\v4run.ps1 -Module v5_vc -Worker vc -Batch road_extras
powershell -File library\src\v4run.ps1 -Module v5_vc -Worker vc -Batch boulders
```

## vd: Capital

| Batch | Category folder | Rows | Models | Est. minutes |
|---|---|---|---|---|
| walls_towers | v5_capital | CP01, CP02, CP03, CP04, CP05, CP06 | 16 | 63 |
| gates_keep | v5_capital | CP07, CP08, CP09, CP10 | 5 | 36 |
| terrace_skyline | v5_capital | CP12, CP13, CP14, CP15, CP19 | 14 | 89 |
| town_extras | v5_capital | CP11, CP16, CP17, CP18 | 20 | 81 |

```
powershell -File library\src\v4run.ps1 -Module v5_vd -Worker vd -Batch walls_towers
powershell -File library\src\v4run.ps1 -Module v5_vd -Worker vd -Batch gates_keep
powershell -File library\src\v4run.ps1 -Module v5_vd -Worker vd -Batch terrace_skyline
powershell -File library\src\v4run.ps1 -Module v5_vd -Worker vd -Batch town_extras
```

## ve: Elf valley and Town 1

| Batch | Category folder | Rows | Models | Est. minutes |
|---|---|---|---|---|
| elf_houses | v5_elf | EV01 | 8 | 35 |
| canopy_roots | v5_elf | EV02, RW02 | 4 | 23 |
| elf_paths | v5_elf | EV03, LM01, LM02 | 8 | 31 |
| town1 | v5_town1 | TW01, TW02, TW03 | 13 | 36 |

```
powershell -File library\src\v4run.ps1 -Module v5_ve -Worker ve -Batch elf_houses
powershell -File library\src\v4run.ps1 -Module v5_ve -Worker ve -Batch canopy_roots
powershell -File library\src\v4run.ps1 -Module v5_ve -Worker ve -Batch elf_paths
powershell -File library\src\v4run.ps1 -Module v5_ve -Worker ve -Batch town1
```

## vf: Landmark heroes, trees and coast

| Batch | Category folder | Rows | Models | Est. minutes |
|---|---|---|---|---|
| heroes_a | v5_landmarks | LM03, LM22, LM25, LM30 | 4 | 44 |
| heroes_b | v5_landmarks | LM09, LM15, LM18 | 3 | 32 |
| skull | v5_skull | VC02 | 2 | 23 |
| trees | v5_forest | VG01, VG02, VG03 | 7 | 27 |
| coast | v5_coast | CO01, CO02 | 9 | 44 |

```
powershell -File library\src\v4run.ps1 -Module v5_vf -Worker vf -Batch heroes_a
powershell -File library\src\v4run.ps1 -Module v5_vf -Worker vf -Batch heroes_b
powershell -File library\src\v4run.ps1 -Module v5_vf -Worker vf -Batch skull
powershell -File library\src\v4run.ps1 -Module v5_vf -Worker vf -Batch trees
powershell -File library\src\v4run.ps1 -Module v5_vf -Worker vf -Batch coast
```

## vg: Highlands, forest and marsh extras

| Batch | Category folder | Rows | Models | Est. minutes |
|---|---|---|---|---|
| highland_set | v5_himalaya | HL01, HL02, HL03, HL04, HL05, HL06, HL07, SP01 | 21 | 82 |
| fortress_parts | v5_landmarks | LM04, LM05, LM06, LM07, LM08 | 9 | 43 |
| forest_set | v5_forest | FR01, FR02, FR03, VG04, LM23, LM24 | 25 | 115 |
| marsh_set | v5_forest | VG05, VG06, VG07 | 7 | 22 |

```
powershell -File library\src\v4run.ps1 -Module v5_vg -Worker vg -Batch highland_set
powershell -File library\src\v4run.ps1 -Module v5_vg -Worker vg -Batch fortress_parts
powershell -File library\src\v4run.ps1 -Module v5_vg -Worker vg -Batch forest_set
powershell -File library\src\v4run.ps1 -Module v5_vg -Worker vg -Batch marsh_set
```

## vh: Desert and Skull City

| Batch | Category folder | Rows | Models | Est. minutes |
|---|---|---|---|---|
| desert_village | v5_desert | DS01, DS02, DS03, DS04, DS05 | 16 | 51 |
| desert_land | v5_desert | DS06, DS07, DS08, SD01, SD02 | 23 | 99 |
| temple_parts | v5_landmarks | LM10, LM11, LM12, LM13, LM14, LM16, LM17 | 14 | 58 |
| skull_set | v5_skull | VC01, VC03, VC04 | 17 | 70 |

```
powershell -File library\src\v4run.ps1 -Module v5_vh -Worker vh -Batch desert_village
powershell -File library\src\v4run.ps1 -Module v5_vh -Worker vh -Batch desert_land
powershell -File library\src\v4run.ps1 -Module v5_vh -Worker vh -Batch temple_parts
powershell -File library\src\v4run.ps1 -Module v5_vh -Worker vh -Batch skull_set
```

## vi: Plains, ruins, coast extras, roads and sky

| Batch | Category folder | Rows | Models | Est. minutes |
|---|---|---|---|---|
| plains_set | v5_plains | PL01, PL02, PL03, PL04, PL05, PL06, VL01 | 16 | 57 |
| ruins_crater | v5_landmarks | LM19, LM20, LM21, LM26, LM27, LM28, LM29, LM31 | 25 | 99 |
| coast_set | v5_coast | CO03, CO04, CO05, HB01 | 14 | 52 |
| road_life | v5_roads | RD01, RD02, RD03, RD04, RD05, RD06, BR01, RV01 | 30 | 100 |
| sky | v5_coast | FL01, FL02 | 6 | 32 |

```
powershell -File library\src\v4run.ps1 -Module v5_vi -Worker vi -Batch plains_set
powershell -File library\src\v4run.ps1 -Module v5_vi -Worker vi -Batch ruins_crater
powershell -File library\src\v4run.ps1 -Module v5_vi -Worker vi -Batch coast_set
powershell -File library\src\v4run.ps1 -Module v5_vi -Worker vi -Batch road_life
powershell -File library\src\v4run.ps1 -Module v5_vi -Worker vi -Batch sky
```

