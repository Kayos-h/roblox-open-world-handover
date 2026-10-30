# v5 review — slice C (sheets 011–015)

Reviewer C of 7. 60 models reviewed (review_011–015). Covers the Elden/world-tree landmarks, Town 1 props & statue, the elf valley, and landmark hero pieces (frost fortress, buried/ring temples, colossal fall cliff, ruin gate, ruined castle, coastal cliffs, sea stacks, skull cliffs, fortress ramparts) plus village-greenery trees.

Hero four-angle sheets used: hero_007, hero_008, hero_009, hero_010, hero_011.

## Verdict counts
| Verdict | Count |
|---|---|
| OK | 41 |
| MINOR | 13 |
| MAJOR | 4 |
| REDO | 2 |
| **Total** | **60** |

## Non-OK models
| id | verdict | what is wrong | how to fix |
|---|---|---|---|
| LM02_01_world_tree_falls | REDO | Falls are flat bright white+cyan slabs reading as glowing light panels (no-glow violation); body reads as a rubble stone stack, not a tree trunk | Rebuild as a tree-trunk cliff; thin layered pale stepped water with foam, no emissive panels |
| LM22_01_colossal_fall_cliff_hero | REDO | Same bright white+cyan emissive-looking falls, floating detached from the cliff; cliff is thin stacked slabs | Matte stepped water hugging the rock; chunky faceted rock cliff |
| EV03_04_elf_path_piece_04 | MAJOR | Stepped planks detached/floating with gaps; moss as stuck-on blobs; won't tile | Join planks into a continuous solid grounded deck; integrate moss |
| EV03_05_elf_path_piece_05 | MAJOR | Loose floating slab plates with gaps, reads as debris not a path | Merge slabs into one connected walkable surface |
| LM03_01_frost_fortress_hero | MAJOR | Mountain backdrop is a chaotic thin-slab stack with floating/jutting plates and messy silhouette (castle itself is good) | Rebuild massif as chunky faceted snow-rock; settle slabs so none float |
| CO01_05_coastal_cliff_05 | MAJOR | Thin bright cyan waterfall strip reads as a glowing neon line (no-glow violation) | Replace with pale matte stepped water, or remove |
| TW01_01_town1_hero_statue | MINOR | Crude flat face, thin staff | Add robe folds, thicken staff |
| TW02_06_street_life_06 | MINOR | Ambiguous prop; cylinder looks detached | Ground the piece, clarify what it is |
| EV01_01_elf_house_new_01 | MINOR | Stacked base rings offset/clipping; loose ground planks | Align base rings, seat planks flush |
| EV01_05_elf_house_new_05 | MINOR | Big open dark doorway with see-through hollow interior; reads as a gazebo | Close/shallow the interior; add a door panel |
| EV02_03_canopy_cluster_03 | MINOR | Risks reading as a recolour of canopy_cluster_01 | Vary platform count/heights |
| EV03_03_elf_path_piece_03 | MINOR | See-through open underside of the arched deck | Fill the underside solid |
| EV03_06_elf_path_piece_06 | MINOR | Flat ring planter, random tree placement | Even spacing, add a lip |
| TW03_01_skull_avenue_set_01 | MINOR | Generic brazier, not skull-themed; thin legs | Add skull motif, thicken legs |
| TW03_04_skull_avenue_set_04 | MINOR | Near recolour of set_03 (red↔blue) | Different banner shape |
| LM18_01_crater_monolith_ring | MINOR | Thin spiky monoliths, sparse ring, flat green disc base | Thicken monoliths, break up the disc base |
| LM25_01_ruin_gate_hero | MINOR | Ambiguous L-overhang lintel; flat sticker-like red panels | Clarify lintel; recess red niches |
| LM30_01_ruined_castle_hero | MINOR | Mostly flat default grey, flat black window holes, loose rubble | Add stone colour variation, recess windows, tidy rubble |
| CO01_03_coastal_cliff_03 | MINOR | Flat black square cave hole reads as a void patch | Give the cave recess/depth |
| VG03_01_tree_flowering_01 | MINOR | Pink blossom and green sit as separate blotchy patches | Intermix small pink clumps through the canopy |
| VG03_02_tree_flowering_02 | MINOR | Same patchy pink-on-green blotching | Blend blossom into the canopy |
| VC02_01_skull_cliff_hero_01 | MINOR | Thin stacked-slab cliff (reads as paper); jaw floats slightly | Chunky faceted dark rock; seat the jaw flush |
| VC02_02_skull_cliff_hero_02 | MINOR | Same slab-cliff issue; near-variant of 01 | Solid faceted rock; differentiate from 01 |

## Systemic issues
1. **Glowing white/cyan "water" on every waterfall piece** (LM02_01, LM22_01, CO01_05). The falls are flat bright emissive-looking slabs — a direct no-glow violation and the single worst pattern in this slice. Fix: one shared matte stepped-water treatment (pale blue, foam at the base, hugging the rock), applied to all fall pieces, with zero emissive material.
2. **Thin "stacked paper slab" cliffs/mountains** (LM03_01 massif, LM22_01, CO-series caps, VC02 skull cliffs). Tall rock masses are built from many thin flat plates that float and read as stacked paper. Fix: build rock as chunky faceted solid masses; use slabs only as surface detail, fully seated.
3. **Elf path kit does not tile or stay solid** (EV03_03/04/05). Walkway pieces float, have gaps, or see-through undersides. Fix: make each path module one connected solid deck that rests on z=0 and tiles edge-to-edge.
4. **Recolour/near-duplicate siblings** (EV02_03↔01, TW03_04↔03, VG01_01↔02, LM04_01/02/03, VC02_01↔02). Several sets are the same design in another colour. Fix: vary silhouette/part count across siblings.
5. **Flat default-grey / flat-colour landmarks** (LM30_01, LM04 ramparts). Reads unfinished. Fix: add weathered stone colour relief and recess openings.

Nothing was un-judgeable: all 60 models were visible on their sheets, and the hero sheets gave close/back angles for every landmark piece in the slice.
