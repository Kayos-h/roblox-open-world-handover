# Placement plans v5 (drafts, written by make_v5_plans.py)

Built on the exported terrain plus the planned landforms. Format is the one `rebuild/v4/build_v4.ps1` reads. The new models do not exist yet, so a first run counts them as "waiting for upload" and places nothing; once a model is uploaded and listed in asset_ids.csv it is placed. Re-seat on the live ground (reseat_env.luau) and verify (verify_folders.luau) after every area.

| Plan file (area) | Placements | Groups | Build command |
|---|---|---|---|
| v5_himalaya | 115 | Himalaya, WizardTower, WizardTowerInterior | `build_v4.ps1 -area v5_himalaya -batch 30 -nocollide Himalaya` |
| v5_roads | 88 | Bridges, RoadLife, RoadWorks, Tunnels | `build_v4.ps1 -area v5_roads -batch 30 -nocollide RoadLife` |
| v5_entrances | 10 | Entrances | `build_v4.ps1 -area v5_entrances -batch 30 -nocollide Entrances` |
| v5_capital | 214 | CapitalGate, CapitalHouses, CapitalPlateau, CapitalPlaza, CapitalSkyline, CapitalWall | `build_v4.ps1 -area v5_capital -batch 30` |
| v5_elf | 17 | ElfCanopy, ElfHouses, ElfPaths | `build_v4.ps1 -area v5_elf -batch 30 -nocollide ElfPaths` |
| town1_v5 | 13 | town1_avenue, town1_life, town1_statue | `build_v4.ps1 -area town1_v5 -batch 30 -nocollide town1_life` |
| v5_landmarks | 53 | Landmarks | `build_v4.ps1 -area v5_landmarks -batch 30` |
| v5_regions | 424 | Coast, Desert, Forest, Plains, Rivers, SkullCity, Sky, VegBirch, VegFlowering, VegMarsh, VegOak, VegPoplar | `build_v4.ps1 -area v5_regions -batch 30 -nocollide VegMarsh` |

Models placed: 396 of 404 new models (rows without a site yet: see below). Total placements: 934.

## New models with no placement yet

- PL05 (1): PL05_01_ruined_watchtower_plains_01
- DS06 (1): DS06_03_canyon_wall_03
- CO05 (1): CO05_02_ruin_islet_02
- RW01 (4): RW01_01_rework_existing_01, RW01_02_rework_existing_02, RW01_03_rework_existing_03, RW01_04_rework_existing_04
- RW02 (1): RW02_01_rework_world_tree_roots

## Misses (no valid free spot was found; fix the site or move the rule)

- v5_regions | PL05_01_ruined_watchtower_plains_01 | only 2 of 3 | 
- v5_regions | DS06_03_canyon_wall_03 | 1885 | 1720 | {'ground': 95, 'busy': 10}

## Exterior placements on wet, steep or off-grid ground (check in Studio)

- v5_himalaya: SP01_03_snow_spire_cluster_03 at (1700.0, -1860.0)
- v5_himalaya: LM03_01_frost_fortress_hero at (1632.0, -1608.0)
- v5_himalaya: LM04_01_fortress_rampart_step_01 at (1600.0, -1560.0)
- v5_himalaya: LM06_01_fortress_tunnel_gate at (1628.0, -1568.0)

Rows meant to be reworks (RW01, RW02) are not placed: they change existing models.
