# Review slice E (sheets 021-025)

Reviewer E of 7. Sheets review_021 to review_025 (60 models): forest ruins / buried temples, desert pieces, hoodoos, underground entrances, volcanic rock, skull-city / dark-fort ruins, red mesas. No wizard-tower ids in this slice. No hero four-angle sheet covers any id in this slice (the LM09/LM25/LM30 hero ids are on other reviewers' sheets); confirmed doubts with v4 close-ups instead.

## Verdict counts
- OK: 32
- MINOR: 18
- MAJOR: 6
- REDO: 4
- Total: 60

## Non-OK models

| id | verdict | what is wrong | how to fix |
|----|---------|---------------|------------|
| LM10_02_temple_colonnade_buried_02 | MINOR | black/inverted face on top of lintel | recalc lintel normals |
| LM13_01_guardian_statue_01 | MINOR | black face near head; thin crude figure | fix normal, bulk up figure |
| LM13_02_guardian_statue_02 | MINOR | black face near head; thin figure | fix normal, bulk up figure |
| LM14_03_sand_obelisk_03 | MINOR | near-identical recolour of 01/02 | vary height/carving/erosion |
| LM16_01_ring_temple_segment_01 | MINOR | plain curved slab, little relief | add carved panelling/weathering |
| LM16_02_ring_temple_segment_02 | MINOR | near-identical featureless curved slab | differentiate + add relief |
| LM12_01_temple_stair_down_01 | MAJOR | jumble of flat clipping slabs, no stair read; floating boxes | rebuild as legible recessed stair, remove floaters |
| LM12_02_temple_stair_down_02 | MAJOR | overlapping slabs, stair not legible | rebuild with distinct descending treads/pit |
| DS01_03_adobe_house_03 | MINOR | large blue slab on front wall; loose merlons | verify/remove slab, seat merlons |
| DS01_04_adobe_house_04 | MINOR | stray yellow beam on ground | remove/attach beam |
| DS02_01_desert_market_01 | MINOR | well reads generic, not a market; stray cubes | redress toward stall, remove cubes |
| DS03_02_caravan_wagon_02 | MINOR | near-recolour of wagon 01 | vary cover shape |
| DS04_01_palm_01 | MINOR | spindly trunk, sparse fronds, stray base wire | thicken trunk, fuller fronds, remove wire |
| DS04_02_palm_02 | MINOR | spindly, sparse, near-identical | fuller canopy, vary silhouette |
| DS04_03_palm_03 | MINOR | spindly, sparse, near-identical | fuller canopy, vary silhouette |
| DS05_02_oasis_rock_ring_02 | MINOR | near-recolour of ring 01 | rearrange rock layout |
| DS07_01_hoodoo_arch_01 | MINOR | camouflage square colour patches; reads as two spires not an arch | band strata, connect arch span |
| DS07_02_hoodoo_arch_02 | MINOR | patchy colour blocks; arch unclear | layered bands, clarify span |
| DS07_04_hoodoo_arch_04 | MAJOR | collapsed block pile, no legible arch; colour patches | rebuild as connected eroded arch |
| DS08_01_underground_entrance_01 | MAJOR | flat wall + face stair, clipping slab jumble, no entrance read | rebuild as sunken doorway/ramp with dark opening |
| DS08_02_underground_entrance_02 | MAJOR | same clipping-slab mass, no entrance | rebuild legible descending entrance |
| DS08_03_underground_entrance_03 | MAJOR | same illegible composition | rebuild, vary from 01/02 |
| VC01_07_volcanic_rock_07 | MINOR | tiny floating fragment at base | remove fragment |
| VC01_08_volcanic_rock_08 | MINOR | stray fragment; set feels like close variants | remove fragment, vary spires |
| VC03_01_dark_fort_ruin_01 | MINOR | loose detached blocks/poles at base | seat/remove fragments |
| VC03_03_dark_fort_ruin_03 | MINOR | small detached bits at base | clean up fragments |
| VC04_01_skull_city_building_01 | REDO | hollow open grey box, floating detached poles, no identity | rebuild as recognisable ruined building, attach beams |
| VC04_02_skull_city_building_02 | REDO | hollow box, floating poles | rebuild identifiable structure |
| VC04_03_skull_city_building_03 | MAJOR | hollow box + broken tower, poles float | attach beams, define box |
| VC04_04_skull_city_building_04 | REDO | hollow box, floating poles | rebuild with attached beams |
| VC04_05_skull_city_building_05 | REDO | hollow box, floating poles | rebuild identifiable structure |
| VC04_06_skull_city_building_06 | MAJOR | hollow box + tower stub, poles float | attach beams, define box |

## Systemic issues
1. **Floating / detached parts.** The whole VC04 skull-city set has timber poles floating above hollow boxes; VC01 volcanic rocks and VC03 forts leave loose fragments at the base. Fix: weld or seat every secondary part onto the main body; delete orphan geometry.
2. **"Entrance/stair cut into ground" pieces are illegible.** LM12 temple stairs and DS08 underground entrances both render as flat walls with clipping slabs and no readable opening. Fix: model these as an explicit recessed opening with framed, stepped treads and a dark void, instead of stacking flat planes on a wall face.
3. **Camouflage-style square colour patches on rock.** DS07 hoodoo arches show blocky red/cream patches that read as camo rather than strata. Fix: convert patchwork into horizontal eroded bands.
4. **Recolour siblings lacking variety.** DS04 palms, LM14 obelisks, LM16 ring segments, DS05 oasis rings and DS03 wagons each look like recolours/clones. Fix: vary silhouette, height and damage within each set.
5. **Minor black/inverted faces.** LM10 lintel and LM13 statue heads show black faces. Fix: recalculate normals.

## Could not judge
Nothing was unjudgeable — all 60 cells and the relevant close-ups were legible. No hero sheet exists for this slice, so hero pieces here (buried temples, dark forts) were judged from sheet + v4 close-up only, i.e. not from the close-up/front-elevation angles a hero sheet would add.
