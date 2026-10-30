# Automatic checks (v5)

404 manifest rows, 385 clean, 19 with at least one flag.

- **SIZE depth**: 8 models (CP04_03_tower_round_cone_03, CP04_04_tower_round_cone_04, HM07_01_prayer_flag_string_01, HM07_02_prayer_flag_string_02, HM07_03_prayer_flag_string_03, NE01_02_village_sign_02, NE01_05_village_sign_05, NE01_06_village_sign_06)
- **MANY**: 8 models (LM03_01_frost_fortress_hero, WT05_01_wizard_round_map_table, HM03_03_tunnel_portal_03, RD04_01_trading_post_01, RD06_02_abandoned_house_02, FL01_01_floating_island_hero_01, FL01_02_floating_island_hero_02, FL01_03_floating_island_hero_03)
- **SIZE width**: 3 models (CP04_03_tower_round_cone_03, CP04_04_tower_round_cone_04, HM01_01_rope_suspension_bridge_01)
- **TRIS**: 2 models (CP16_04_townhouse_new_04, CP16_05_townhouse_new_05)
- **SIZE height**: 1 models (CP04_04_tower_round_cone_04)

## Flagged models

- `CP04_03_tower_round_cone_03` (2832 tris, [31.0, 31.0, 52.7]): SIZE width 31 vs 22; SIZE depth 31 vs 22
- `CP04_04_tower_round_cone_04` (2952 tris, [37.0, 37.0, 59.1]): SIZE width 37 vs 22; SIZE depth 37 vs 22; SIZE height 59.1 vs 48
- `CP16_04_townhouse_new_04` (12304 tris, [22.0, 22.0, 28.0]): TRIS 12304 > 11000
- `CP16_05_townhouse_new_05` (12304 tris, [22.0, 22.0, 28.0]): TRIS 12304 > 11000
- `LM03_01_frost_fortress_hero` (37720 tris, [300.0, 276.31, 220.0]): MANY MATERIALS 17
- `WT05_01_wizard_round_map_table` (20314 tris, [47.6, 47.6, 11.42]): MANY MATERIALS 17
- `HM01_01_rope_suspension_bridge_01` (5316 tris, [72.0, 9.6, 14.1]): SIZE width 72 vs 120
- `HM03_03_tunnel_portal_03` (1000 tris, [31.78, 20.03, 24.0]): MANY MATERIALS 15
- `HM07_01_prayer_flag_string_01` (500 tris, [39.93, 2.52, 12.47]): SIZE depth 2.52 vs 2
- `HM07_02_prayer_flag_string_02` (848 tris, [39.93, 2.35, 12.49]): SIZE depth 2.35 vs 2
- `HM07_03_prayer_flag_string_03` (596 tris, [39.93, 2.49, 12.48]): SIZE depth 2.49 vs 2
- `RD04_01_trading_post_01` (4948 tris, [30.0, 24.0, 21.16]): MANY MATERIALS 15
- `RD06_02_abandoned_house_02` (7176 tris, [22.0, 18.99, 20.0]): MANY MATERIALS 16
- `FL01_01_floating_island_hero_01` (18064 tris, [86.0, 86.0, 60.0]): MANY MATERIALS 17
- `FL01_02_floating_island_hero_02` (13052 tris, [86.0, 86.0, 59.81]): MANY MATERIALS 15
- `FL01_03_floating_island_hero_03` (9976 tris, [86.0, 86.0, 63.31]): MANY MATERIALS 18
- `NE01_02_village_sign_02` (388 tris, [10.34, 5.48, 17.6]): SIZE depth 5.48 vs 4
- `NE01_05_village_sign_05` (316 tris, [10.4, 2.91, 17.6]): SIZE depth 2.91 vs 4
- `NE01_06_village_sign_06` (244 tris, [10.4, 2.73, 17.6]): SIZE depth 2.73 vs 4