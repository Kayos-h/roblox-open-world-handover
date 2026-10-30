# Blender model list, v3 map

Written 29 Oct 2026. The v2 list is in `rebuild\v2_backup\BLENDER_NEEDS.v2.md`. Blender stays off for now, so everything below is a placeholder built from Roblox parts or an existing catalog model. Counts are what the map uses today.

**Workflow when Blender is on:** build every model here, export with `town\library\src\export_v2.py` (scale ÷100, one piece per colour, writes `palette.json`), you close Blender, then I finish the Studio build. Upload with `town\upload_all.ps1 -only <name>` or the Desktop `.bat` files (your "memory freeer" app killed earlier uploads with exit code 15; running the `.bat` yourself works).

Rule for all models: original designs, never direct Black Clover copies. Sizes are in studs (1 stud = 1 unit before the ÷100 export). Pivot at the bottom centre, front facing +Z.

## A. Replace part-built placeholders (highest priority)

| # | Model | Count in map now | Variants | Notes |
|---|---|---|---|---|
| A1 | Igloo | 17 | 3 (diameter 14, 16, 18) | Snow block seams, tunnel entrance, dark doorway with a back wall, optional hollow interior. Currently half-buried balls. |
| A2 | Ice-fishing shanty | 13 | 4 colours | Pitched roof with snow cap, door, stovepipe, plank walls. About 8x9x7 studs. |
| A3 | Fishing hole with ice rim | 30 | 3 | Ragged ice rim, cracks, shallow dark water. About 4 studs across. |
| A4 | Rusty hut | 46 | 5 or 6 | Flat-roof timber, gabled sandstone, scrap-roof. Doors, windows with shutters, steps, interior back wall. 13-15 studs wide. Break the straight-row look. |
| A5 | Enterable shell: rusty church | 1 | 1 | 60x124 footprint at (1406,1244). Hollow nave, door, windows with light. |
| A6 | Enterable shell: capital cathedral | 1 | 1 | At (-186,-1628), 362 parts now. |
| A7 | Enterable shell: harbour tavern | 1 | 1 | At (-428,1764), 92 parts now. |
| A8 | Enterable shell: alpine lodge | 1 | 1 | At (1585,-880), 92 parts now. |
| A9 | Enterable shell: elf temple | 1 | 1 | At (-1490,-170). Decide first whether it stays enterable (see report, point 7). |
| A10 | Enterable shell: elf round house | 2 | 2 | At (-1730,-300) and (-1390,-560). Round, pink, green roof. |

## B. Key set pieces

| # | Model | Count | Notes |
|---|---|---|---|
| B1 | Skull HQ | 1 | Separate colour pieces, hollow inside, entrance through the jaw. Same size as now (220x148x265). |
| B2 | Castle keep, towers and walls | 1 set | You like the capital layout, so improve the buildings, not the plan. Round, square and spire towers, curtain wall straight and corner pieces, gatehouse. |
| B3 | Castle throne hall interior | 1 | Throne pillars (K12), banners, stairs. |
| B4 | Barracks and stables | 1 each | Currently catalog K40 and K41. |
| B5 | Royal courtyard set | 1 set | Fountain, knight statues (8 in map), obelisks (2), ornate lamps (14), banners (16), gazebo, rose arches. |
| B6 | Castle market stalls | 12 | 3 designs (fruit, cloth, potion), 15x5x8 studs. |
| B7 | Capital houses | 4 to 6 new designs | Break up the repeated townhouses (about 180 copies of 4 townhouse designs, plus 6 other shop and house designs repeated 30-40 times each). Include 6+ roof colours and 4 facade variants for the main avenue. |
| B8 | Town 1 church | 1 | Gothic church, 35x85x75, door and rose window facing east. Not enterable. |
| B9 | Harbour ships | 2 | Galleon 88x28x60 and merchant ship 61x20x41, with rigging and rope detail. Plus 4 fishing boats and 5 rowboats. |
| B10 | Harbour lighthouse, cranes, warehouses | 1 set | Lighthouse 27x27x45, cargo crane, two warehouses. |

## C. Alpine

| # | Model | Count | Notes |
|---|---|---|---|
| C1 | Chalets | 4 to 6 designs | Currently catalog E01-E05. Timber and stone, deep snow roofs, icicles. |
| C2 | Winter-market stalls | 6 | Striped awnings, lanterns. |
| C3 | Ski rack | 4 | |
| C4 | Snowman | 6 | 2 sizes. |
| C5 | Ice blocks and ice sculptures | 12 | |
| C6 | Frozen dock | 2 | For the lake edge. |
| C7 | Sleds | 6 | |
| C8 | Frozen boats | 5 | Boats stuck in the ice. |
| C9 | Frozen waterfall | 1 | At the cliff step on the lake's south rim, about (1520,-982). The step is 30 studs tall. |
| C10 | Snow pines | 4 designs | Currently E12-E14. |

## D. Elf valley

| # | Model | Count | Notes |
|---|---|---|---|
| D1 | Treehouse platforms | 4 | Only 2 of the 4 treehouses have a deck now (at y 35). All need a deck, ladders, railings. |
| D2 | Rope bridges | 3 sizes, 10 or more in the map | Short 16, long 48. Sagging ropes, wooden planks, lanterns. |
| D3 | Hanging vines and moss | 60+ | Currently catalog F18-F20. |
| D4 | Glow flowers, mushrooms, crystals | 90 + 70 + 14 | More variety in shape and colour. |
| D5 | World tree base, roots, canopy | 1 | 169x186x192 now. |
| D6 | Palace, moon pool, carved arches, root arches | 1 set | |
| D7 | Elf statues | 3 | |
| D8 | Elf lanterns | 62 | Standing and hanging. |
| D9 | Jungle trees and palms | 3 designs | |

## E. Graveyard, rusty town, farms, nature

| # | Model | Count | Notes |
|---|---|---|---|
| E1 | Gravestones | 8 designs | Currently catalog D12-D16. About 150 in the map (Town 1 and rusty town). Weathered, tilted, moss. |
| E2 | Crypts and mausoleums | 3 designs | 4 in the map. |
| E3 | Weeping statues | 3 | 5 in the map. |
| E4 | Graveyard iron fence and gate | 2 | |
| E5 | Dead trees | 6 | About 25 in the map. |
| E6 | Rusty scrap piles, tents, collapsed walls | 5 + 3 + 4 | |
| E7 | Crooked lamps, rusted carts, broken barrels | 3 + 3 + 3 | |
| E8 | Barn | 3 | One in the map at (580,-245). |
| E9 | Windmill | 2 | Two in the map. |
| E10 | Crop plots (wheat, vegetables) | 6 designs | About 20 plots. |
| E11 | Scarecrows | 3 | |
| E12 | Shrines and ruins | 4 | |
| E13 | Mountain rock faces and cliff pieces | 8 to 12 | Needs seamless tiling with the terrain. The tower massif needs 3 or 4 large faces. |
| E14 | Ice-lake rim wall | 4 | 30-stud cliff step. |
| E15 | Boulders and snowy rocks | 6 designs | Currently overscaled catalog rocks. |

## F. Known texture and material wishes

- A proper stone path set that blends into terrain (roads are terrain material now).
- Smaller, more varied grass blades near huts and the quay. The terrain grass decoration cannot be edited from scripts.

## G. Totals

The list above has 54 rows. Counting one model per design, with the design counts I chose for each row:

| Section | Models |
|---|---|
| A. Replace part-built placeholders | 23 |
| B. Key set pieces | 36 |
| C. Alpine | 25 |
| D. Elf valley | 28 |
| E. Graveyard, rusty, farms, nature | 81 |
| **Total** | **193** |

The 330 models already uploaded stay. The design counts are my estimate; a few rows say "4 to 6" and I used the upper number.

## H. Added 30 Oct 2026 (after the v4 map build; Blender is parked, nothing here blocks the map)

The 390 V4 models are all built, uploaded and placed (asset ids in `asset_ids.csv`, 720 rows). What is still open for Blender, ranked by visual payoff:

1. **Giant magic tower for the tower-mountain summit** (summit pad at about (1380,-1320), y 318). Not in the 390. Needs a tall (200 to 300 studs) original tower, enterable base optional.
2. **Fix list from the model reviews** (`library/v4_work/KNOWN_DEFECTS.md`): B02_05 curtain wall and B02_06 curtain corner (black recess at the wall-walk end, four failed attempts), R03_03 mesa (open lip top), F08_13 gate (thin dark seam). The elf treehouses D01_02 and D01_04 are 58k triangles (budget 50k).
3. **Castle courtyard and plaza paving as modular tiles.** The courtyard is a 190-stud-wide terrain Pavement strip; it reads as one flat tan slab. A set of paving decals or 3 to 4 low relief paving pieces with joints would fix the review note "flat single-tone paving".
4. **Road pieces:** crossings, T-junctions, bridges that carry the tan road web over rivers (the roads are terrain paint now and read well from above, but junctions have no props).
5. **More tree species for the heartland.** Reviewers call the round oak "broccoli". Wanted: 3 tall poplar or beech trees with a narrow crown, 2 dark old oaks with a broken crown, 2 flowering trees, all 25 to 45 studs.
6. **Hero rocks for the sea:** reefs and low sea rocks (6 designs, 6 to 20 studs) for the empty open water, and 3 larger sea stacks.
7. **Elf world tree and waterfall as one hero set:** a hollowed trunk with a door, a 3-tier waterfall, and a stone bridge across the stream. The current trunk is a plain column.
8. **Training yard kit** (built from parts tonight): 3 dummy designs, an archery butt, a weapon rack, a mounted-target. Models would look better than the part builds.
9. **Skull town cone roofs** need a second, less saturated roof material option.

## I. v5 world redesign: the full new-model list (30 Oct 2026, 11:55; Blender is off, nothing here is built)

The complete list is `town/plan_v5/V5_MANIFEST.md` (also `.csv` and `.json`; generated by `v5_manifest.py`). **Count: 399 new models** (P1 core 106, P2 region completion 289, P3 optional 4) **plus 5 reworks**. 20 hero models of 40k+ triangles. Triangle budget about 5.4M. Style and plan: `WORLD_BIBLE_v5.md`, `PRIORITY_AREAS_v5.md`.

Build order when Blender is allowed (launch it, build with parallel workers, review every model by render with independent reviewers, export with `library/src/export_v2.py`, user closes Blender, upload):

1. **The giant enterable wizard tower, first of all** (`WIZARD_TOWER_BRIEF.md`, rows WT01-WT12, 21 P1 models): shell, interior shell with helical stair, the circular map table (source data ready: `wizard_map_relief.obj`, `wizard_map_color.png`), curved and straight bookshelves, lab and study sets, chandeliers, telescope, armillary crown, door porch; plus `tower_collision.json`. Then WT13 terrace set (P2).
2. Himalayan road kit (HM01 rope bridges x3, HM03 tunnel portals x3, HM04 tunnel lining x2 are P1; HM02, HM05-HM09 are P2).
3. Capital (CP rows, 35 P1), elf valley (EV01 8 houses, EV02 3 canopy clusters, RW02 roots), Town 1 (TW rows), natural entrances (NE01 village signs x6 P1, NE02 boulder pairs x4).
4. Landmark heroes (frost fortress, skull cliff, crater ring, ring and buried temples, colossal fall cliff, ruined castle and gate).
5. Everything else by region (see the manifest).

Removed from the plan: GT01/GT02 gate models (12) after the plain arch was dropped; LM32-LM35 abandoned magic tower rows (replaced by the wizard tower).
