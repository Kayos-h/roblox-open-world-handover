# Assignment A4: highlands, forest, fortress and marsh

36 models: REDO 0, MAJOR 17, MINOR 17, OK-with-note 2. Work in the order of the table (worst first).

## Your modules (you own these files and nothing else)

| fix module | worker | new palette prefix | round-1 module to read |
|---|---|---|---|
| `library\src\v5_fx_vg.py` | vg | `vg_f_` | `library\src\v5_vg.py` |

Scratch build: `powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Nitro\.kiro\crew\workspace\town\scratch.ps1" -Module <fix module> -Ids <id,id,...> -Tag A4`
Sheets land in `library\v5_work\fix_scratch\A4\<id>.png`. Target size is W x D x H in studs (X, Y, Z); the manifest autofit (`mk(..., 0.1)`) rescales a model that is more than 10% off, which distorts it, so design to size.

## Families in this assignment

FR01 x2, FR02 x2, FR03 x5, HL01 x1, HL02 x1, HL03 x3, HL04 x1, HL07 x1, LM04 x2, LM05 x1, LM07 x2, LM08 x1, LM23 x1, SP01 x6, VG04 x3, VG05 x2, VG06 x2

## Models

| id | verdict | category | target W x D x H | tri budget | tris now | what the reviewers saw | reviewer suggestion |
|---|---|---|---|---|---|---|---|
| `FR01_03_giant_tree_03` | MAJOR | v5_forest | 90 x 90 x 160 | 40000 | 1056 | canopy reduced to two ball blobs on splayed legs; reads as an arch/wishbone, not a giant tree; trunk splits into a bare inverted-V with a gap | Rebuild with a full connected canopy and a solid single trunk so it matches its giant-tree siblings. |
| `FR03_04_cave_mouth_04` | MAJOR | v5_forest | 40 x 30 x 30 | 10000 | 792 | rock arch collapsed into scattered loose blocks, many detached/floating; no solid cave mouth reads | Merge the loose chunks into a solid arched mass seated on the ground with a clear opening. |
| `FR03_05_cave_mouth_05` | MAJOR | v5_forest | 40 x 30 x 30 | 10000 | 792 | same scattered floating-debris problem as 04; silhouette does not read as a cave | Rebuild as one connected rock arch; remove free-floating blocks. |
| `FR03_06_cave_mouth_06` | MAJOR | v5_forest | 40 x 30 x 30 | 10000 | 792 | loose detached blocks, gaps, no solid opening | Consolidate into a solid grounded cave mouth with an actual recessed opening. |
| `LM07_01_carved_stair_switchback_01` | MAJOR | v5_landmarks | 50 x 60 x 60 | 16000 | 2820 | carved stair is not readable; looks like a plain rock mound; no visible steps or switchback | Cut clear stepped switchback flights into the rock face so the staircase reads from 30-60 studs. |
| `LM07_02_carved_stair_switchback_02` | MAJOR | v5_landmarks | 50 x 60 x 60 | 16000 | 2820 | steps barely readable, reads as a rough rock pile; silhouette does not say stair | Add defined step treads and a landing so the carved switchback is legible. |
| `LM08_01_mountain_span_bridge` | MAJOR | v5_landmarks | 90 x 16 x 24 | 14000 | 2368 | deck is broken/gappy, pieces look detached and floating; no continuous walkable span; tiny scattered posts read as debris | Rebuild a continuous solid deck with connected rails/supports so it reads as a crossable bridge. |
| `LM23_03_gorge_wall_03` | MAJOR | v5_forest | 90 x 30 x 80 | 20000 | 3456 | thin flat bright-white waterfall slab clips through the wall as a glowing vertical bar; slab is a single flat panel with no relief | Replace the flat white bar with a recessed stepped water chute in muted blue, seated into the rock, no flat glowing panel. |
| `SP01_01_snow_spire_cluster_01` | MAJOR | v5_himalaya | 60 x 60 x 160 | 15000 | 1416 | blocky black/grey/white square camouflage patches over the spire; very thin pencil-like spire reads as a pole, weak silhouette; base rocks look detached | Replace the camo patches with coherent snow-over-grey-rock shading, thicken the spire taper, and seat the base rocks into the mass. |
| `SP01_02_snow_spire_cluster_02` | MAJOR | v5_himalaya | 60 x 60 x 160 | 15000 | 1416 | identical camouflage-patch and thin-spire problem as 01 | Same fix as SP01_01; also vary silhouette so it is not a clone. |
| `SP01_03_snow_spire_cluster_03` | MAJOR | v5_himalaya | 60 x 60 x 160 | 15000 | 1416 | camo patches, thin spire, clone of the set | Recolour coherently, thicken, and differentiate shape. |
| `SP01_04_snow_spire_cluster_04` | MAJOR | v5_himalaya | 60 x 60 x 160 | 15000 | 1416 | camo patches, thin spire, clone | Recolour coherently, thicken, and differentiate shape. |
| `SP01_05_snow_spire_cluster_05` | MAJOR | v5_himalaya | 60 x 60 x 160 | 15000 | 1416 | camo patches, thin spire, clone | Recolour coherently, thicken, and differentiate shape. |
| `SP01_06_snow_spire_cluster_06` | MAJOR | v5_himalaya | 60 x 60 x 160 | 15000 | 1416 | camo patches, thin spire, clone | Recolour coherently, thicken, and differentiate shape. |
| `VG04_01_tree_birch_01` | MAJOR | v5_forest | 14 x 14 x 34 | 8000 | 2168 | canopy covered in flat yellow blotches, reads diseased not birch; splayed flat-white trunk looks like an open cone, not bark | Use a slim upright white-bark trunk with dark lenticel marks and a predominantly green canopy with light accents, not large yellow patches. |
| `VG04_02_tree_birch_02` | MAJOR | v5_forest | 14 x 14 x 34 | 8000 | 2168 | same yellow-blotch canopy and splayed cone trunk as 01 | Rebuild trunk as a thin upright birch bole and reduce yellow to subtle autumn accents. |
| `VG04_03_tree_birch_03` | MAJOR | v5_forest | 14 x 14 x 34 | 8000 | 2168 | clone of 01/02 with same trunk and blotch defects | Fix the trunk and canopy as above and vary the shape from its siblings. |
| `FR01_02_giant_tree_02` | MINOR | v5_forest | 90 x 90 x 160 | 40000 | 6016 | near-recolour of FR01_01 | Vary canopy mass and branch spread to distinguish from 01. |
| `FR02_05_forest_ruin_05` | MINOR | v5_forest | 40 x 30 x 34 | 10000 | 1304 | tall thin column looks like a floating plain slab with little relief | Add break detail and a base to the standing column so it reads as a ruin, not a blank post. |
| `FR02_06_forest_ruin_06` | MINOR | v5_forest | 40 x 30 x 34 | 10000 | 1196 | lone thin column with a floating cap block; sparse | Anchor the capstone to the column and add rubble so it reads as a ruin fragment. |
| `FR03_02_cave_mouth_02` | MINOR | v5_forest | 40 x 30 x 30 | 10000 | 948 | near-duplicate of FR03_01 | Vary the opening and rock stacking to differ from 01. |
| `FR03_03_cave_mouth_03` | MINOR | v5_forest | 40 x 30 x 30 | 10000 | 912 | recolour/clone of 01-02 | Change silhouette and cave opening shape. |
| `HL01_04_ice_spire_04` | MINOR | v5_himalaya | 24 x 24 x 70 | 8000 | 768 | near-identical recolour of the other three spires | Vary the taper and chunk placement so it is not a clone of HL01_01-03. |
| `HL02_02_ice_arch_02` | MINOR | v5_himalaya | 50 x 14 x 40 | 9000 | 864 | very close duplicate of HL02_01; scattered base blocks look like floating debris | Reshape the arch silhouette for variety and merge the loose base chunks into the mass. |
| `HL03_01_glacier_tongue_01` | MINOR | v5_himalaya | 90 x 50 x 24 | 12000 | 948 | brown/tan rock chunks mixed into ice read as dirty camouflage patches; flat scattered slabs | Reduce the brown rock blotches and give the ice plates more consistent cool tone and relief. |
| `HL03_02_glacier_tongue_02` | MINOR | v5_himalaya | 90 x 50 x 24 | 12000 | 960 | same brown-patch issue; near-copy of 01 | Tone down brown patches and differentiate the shape from siblings. |
| `HL03_03_glacier_tongue_03` | MINOR | v5_himalaya | 90 x 50 x 24 | 12000 | 972 | recolour of 01/02 with brown debris patches | Vary silhouette and cut the muddy brown blocks. |
| `HL04_02_ice_cave_mouth_02` | MINOR | v5_himalaya | 40 x 30 x 30 | 10000 | 788 | near-identical to HL04_01 | Change opening shape/overhang so it is not a clone. |
| `HL07_02_mine_entrance_02` | MINOR | v5_himalaya | 30 x 24 x 24 | 9000 | 732 | very close variant of HL07_01 | Alter timber framing or rubble arrangement for variety. |
| `LM05_02_fortress_cliff_tower_02` | MINOR | v5_landmarks | 34 x 34 x 80 | 18000 | 984 | thin stick-like flag/beam pokes out of side; rock base reads as plain grey slab | Remove or thicken the stray side beam and add facet variation to the base rock. |
| `VG05_02_tree_cypress_swamp_02` | MINOR | v5_forest | 22 x 22 x 38 | 11000 | 1852 | near-recolour of VG05_01 | Vary canopy mass and root spread. |
| `VG05_03_tree_cypress_swamp_03` | MINOR | v5_forest | 22 x 22 x 38 | 11000 | 1852 | near-clone of VG05_01/02 | Differentiate canopy silhouette and trunk from siblings. |
| `VG06_01_marsh_hummock_01` | MINOR | v5_forest | 16 x 16 x 6 | 3000 | 396 | single flat green faceted slab mound with no relief or detail; no texture of marsh grass/moss | Add tufts, mud rim and height variation so it reads as a marsh hummock, not a flat green shard. |
| `VG06_02_marsh_hummock_02` | MINOR | v5_forest | 16 x 16 x 6 | 3000 | 396 | near-duplicate of 01; flat untextured green | Vary the shape and add detail/mud edge. |
| `LM04_02_fortress_rampart_step_02` | OK | v5_landmarks | 60 x 20 x 34 | 14000 | 5432 | near-identical to rampart_step_01 | Give the three rampart steps distinct tower/wall arrangements so they are not recolours. |
| `LM04_03_fortress_rampart_step_03` | OK | v5_landmarks | 60 x 20 x 34 | 14000 | 5528 | near-identical to rampart_step_01 and 02 | See step_02: vary the three modules. |