# Assignment A6: elf valley, Town 1, landmark heroes, tower pieces, reworks

28 models: REDO 2, MAJOR 6, MINOR 17, OK-with-note 3. Work in the order of the table (worst first).

## Your modules (you own these files and nothing else)

| fix module | worker | new palette prefix | round-1 module to read |
|---|---|---|---|
| `library\src\v5_fx_ve.py` | ve | `ve_f_` | `library\src\v5_ve.py` |
| `library\src\v5_fx_vf.py` | vf | `vf_f_` | `library\src\v5_vf.py` |
| `library\src\v5_fx_va.py` | va | `va_f_` | `library\src\v5_va.py` |
| `library\src\v5_fx_vb.py` | vb | `vb_f_` | `library\src\v5_vb.py` |
| `library\src\v5_fx_vj.py` | vj | `vj_f_` | `library\src\v5_vj.py` |

Scratch build: `powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Nitro\.kiro\crew\workspace\town\scratch.ps1" -Module <fix module> -Ids <id,id,...> -Tag A6`
Sheets land in `library\v5_work\fix_scratch\A6\<id>.png`. Target size is W x D x H in studs (X, Y, Z); the manifest autofit (`mk(..., 0.1)`) rescales a model that is more than 10% off, which distorts it, so design to size.

## Families in this assignment

CO01 x2, EV01 x2, EV02 x1, EV03 x4, LM01 x1, LM02 x1, LM03 x1, LM18 x1, LM22 x1, LM25 x1, LM30 x1, RW01 x1, TW01 x1, TW02 x1, TW03 x2, VC02 x2, VG01 x1, VG03 x2, WT08 x1, WT13 x1

## Models

| id | verdict | category | target W x D x H | tri budget | tris now | what the reviewers saw | reviewer suggestion |
|---|---|---|---|---|---|---|---|
| `LM02_01_world_tree_falls` | REDO | v5_elf | 80 x 40 x 110 | 35000 | 5304 | waterfalls are flat bright white+cyan vertical slabs that read as glowing light panels, not water; no-glow rule violation; body reads as a random rubble stone stack, not a tree trunk with falls; window-like openings look like lit doors | Rebuild as a believable tree-trunk cliff; make the falls thin layered translucent/pale-blue stepped water with foam at the base and NO emissive bright panels. |
| `LM22_01_colossal_fall_cliff_hero` | REDO | v5_landmarks | 240 x 120 x 260 | 60000 | 51678 | waterfalls are bright white+cyan flat emissive-looking vertical slabs floating in front of the cliff; no-glow rule violation; falls float detached from the rock face; cliff is a thin stacked-slab stack like paper | Rebuild falls as thin pale stepped water hugging the rock with foam pools, no glowing slabs; make the cliff chunky faceted rock instead of stacked thin plates. |
| `CO01_05_coastal_cliff_05` | MAJOR | v5_coast | 110 x 50 x 70 | 18000 | 2616 | thin bright cyan vertical waterfall strip reads as a glowing neon line; no-glow rule violation | Replace the glowing cyan strip with a pale matte stepped waterfall, or remove it. |
| `EV03_04_elf_path_piece_04` | MAJOR | v5_elf | 20 x 20 x 6 | 4000 | 1080 | stepped bridge planks look detached/floating with gaps between them; green mossy patches look like loose stuck-on blobs; would not tile cleanly | Join the plank steps into a continuous solid deck seated on the ground and integrate the moss rather than floating blobs. |
| `EV03_05_elf_path_piece_05` | MAJOR | v5_elf | 20 x 20 x 6 | 4000 | 632 | loose thin slab plates float with visible gaps and do not connect; reads as scattered debris, not a path | Merge the slabs into one connected walkable path surface with no floating gaps. |
| `LM01_01_world_tree_trunk_door` | MAJOR | v5_elf | 36 x 36 x 50 | 30000 | 3004 | splayed root buttresses are thin spiky planks with large see-through gaps between them; trunk base reads hollow/holed; top is an open flat green rim (hollow trunk cap) | thicken and merge the roots into a solid flared base with no gaps, close the trunk top, and make the door a clear recessed opening rather than a hollow |
| `LM03_01_frost_fortress_hero` | MAJOR | v5_landmarks | 300 x 260 x 220 | 60000 | 48568 | mountain backdrop is a chaotic stack of thin flat slabs with floating/jutting plates and a messy broken silhouette; slabs read as stacked paper, not snow rock; castle itself is good but overwhelmed by the crude massif | Rebuild the mountain as chunky faceted snow-rock masses instead of thin stacked slabs; keep the castle and settle slabs so none float. |
| `RW01_01_rework_existing_01` | MAJOR | v5_rework | 0 x 0 x 0 | 0 | 1356 | crude stack of offset coloured slabs; silhouette does not read as a clear structure; slabs look loosely piled/unstable | Rebuild as a coherent tower/mesa with aligned, connected courses instead of randomly offset flat slabs. |
| `CO01_03_coastal_cliff_03` | MINOR | v5_coast | 110 x 50 x 70 | 18000 | 2304 | flat black square cave hole reads as a void/hole in the slab | Give the cave opening depth/recess so it is not a flat black square patch. |
| `EV01_01_elf_house_new_01` | MINOR | v5_elf | 26 x 26 x 30 | 14000 | 4040 | stacked ring tiers at base look slightly offset/clipping; loose plank segments at ground | Align the stacked base rings cleanly and seat the ground planks flush. |
| `EV01_05_elf_house_new_05` | MINOR | v5_elf | 26 x 26 x 30 | 14000 | 1576 | front is a big open dark round doorway with a see-through hollow interior behind the columns; reads as an open gazebo more than a house | Close or shallow the interior behind the arch so there is no see-through gap; add a door/wall panel. |
| `EV03_03_elf_path_piece_03` | MINOR | v5_elf | 20 x 20 x 6 | 4000 | 528 | arched deck has an open gap/see-through underside between the ramp and the deck | Fill the underside of the arched walkway so it is solid and tiles on the ground. |
| `EV03_06_elf_path_piece_06` | MINOR | v5_elf | 20 x 20 x 6 | 4000 | 2520 | flat ring planter, trees inside look placed a bit randomly | Even out tree spacing inside the ring and add a lip so it reads as a planter. |
| `LM18_01_crater_monolith_ring` | MINOR | v5_landmarks | 140 x 140 x 50 | 40000 | 2684 | dark monoliths are thin and spiky, ring reads sparse; flat green pad under it looks like a disc, not terrain | Thicken the monoliths and break up the flat green base so the ring reads as a crater, not a disc. |
| `LM25_01_ruin_gate_hero` | MINOR | v5_landmarks | 90 x 30 x 80 | 40000 | 3068 | the tall L-shaped overhang block reads ambiguous, almost like an unfinished arm; red inset panels look like flat stickers | Clarify the gate lintel form and recess/relieve the red panels so they read as stone niches. |
| `LM30_01_ruined_castle_hero` | MINOR | v5_landmarks | 140 x 120 x 70 | 50000 | 9628 | almost entirely flat default grey, reads unfinished/greyed-out; window holes are flat black rectangles; rubble cubes scattered loosely | Add weathered stone colour variation and recess the windows; tidy the rubble so cubes rest naturally. |
| `TW01_01_town1_hero_statue` | MINOR | v5_town1 | 14 x 14 x 40 | 16000 | 1314 | face is crude flat-boxy; staff reads thin | Add simple carved robe folds and a thicker staff so it reads as a hero statue up close. |
| `TW02_06_street_life_06` | MINOR | v5_town1 | 12 x 10 x 10 | 3000 | 184 | bracket+gong reads ambiguous as a street prop; cylinder on ground looks detached | Ground the fallen log/bell and clarify what the prop is; thicken the mount. |
| `TW03_01_skull_avenue_set_01` | MINOR | v5_town1 | 14 x 14 x 14 | 5000 | 268 | dark brazier bowl on a thin tripod reads generic, not skull-avenue themed | Add a skull/gothic motif to tie it to the avenue set and thicken the legs. |
| `VC02_01_skull_cliff_hero_01` | MINOR | v5_skull | 200 x 120 x 120 | 55000 | 6632 | white skull sits in front of a thin stacked-slab cliff; slabs read as stacked paper; skull jaw/teeth block floats slightly below | Make the cliff chunky faceted dark rock rather than thin stacked plates and seat the jaw flush to the skull. |
| `VC02_02_skull_cliff_hero_02` | MINOR | v5_skull | 200 x 120 x 120 | 55000 | 7464 | horned skull version, same thin stacked-slab cliff issue; near recolour/variant of 01 | Differentiate from 01 and rebuild the slab cliff as solid faceted rock. |
| `VG03_01_tree_flowering_01` | MINOR | v5_forest | 22 x 22 x 30 | 12000 | 2832 | pink blossom and green foliage sit as separate blotchy patches rather than blended blossom; reads as two colours slapped on | Intermix smaller pink blossom clumps through the green canopy so the blossom reads natural, not patchy. |
| `VG03_02_tree_flowering_02` | MINOR | v5_forest | 22 x 22 x 30 | 12000 | 2832 | same patchy pink-on-green blotching as flowering_01 | Blend the pink blossom clusters into the canopy rather than large flat patches. |
| `WT08_02_wizard_study_set_02` | MINOR | v5_wizard | 18 x 14 x 12 | 9000 | 592 | sparse: a bare blue canopy-bed/frame with little detail for the tri count, crudest of the study set | add bedding, pillows or drapery folds so it reads as a furnished study/bed, not an empty frame |
| `WT13_01_plateau_terrace_set_01` | MINOR | v5_wizard | 30 x 30 x 10 | 7000 | 2520 | plain flat cream slab deck with little relief | add an edge trim or a few steps so it reads as a built terrace, not a blank box lid |
| `EV02_03_canopy_cluster_03` | OK | v5_elf | 70 x 70 x 40 | 30000 | 6264 | very similar to canopy_cluster_01, risks reading as a recolour | Vary platform count/heights so the three canopy clusters are clearly distinct designs. |
| `TW03_04_skull_avenue_set_04` | OK | v5_town1 | 14 x 14 x 14 | 5000 | 260 | near-identical recolour of set_03 (red vs blue) | Give it a different banner shape/standard so it is not just a recolour of set_03. |
| `VG01_02_tree_tall_narrow_02` | OK | v5_forest | 14 x 14 x 46 | 9000 | 2084 | near-identical to tree_tall_narrow_01 | Vary the foliage silhouette so 01 and 02 are not recolour-identical. |