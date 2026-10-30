# Slice A review (R4) — reviewer A

Sheets review_001 to review_003 (36 models). Pictures only; MCP server `@Roblox_Studio` was not configured and was not used.

## Verdict counts
- OK: 18
- MINOR: 10
- MAJOR: 6
- REDO: 2
- Total: 36

## Non-OK models

| id | verdict | what is wrong | how to fix |
|---|---|---|---|
| LM07_02_carved_stair_switchback_02 | REDO | hollow open box, black see-through interior, stairs float in a void, inverted/missing faces | rebuild as a solid rock mass with the switchback carved into a filled face |
| LM07_01_carved_stair_switchback_01 | REDO | same defect as _02: hollow black interior, floating stairs, no solid mass | rebuild as a solid rock mass, no open hollow or black interior |
| HM08_03_cairn_shrine_03 | MAJOR | roof on thin posts with a wide open gap to the drum; reads as floating roof | close the gap / add brackets so roof connects to body |
| RD06_05_abandoned_house_05 | MAJOR | roof planks jumbled, some detached/floating above the frame (front) | reseat planks as a connected collapsed roof, remove floating tiles |
| VC04_06_skull_city_building_06 | MAJOR | roof plank overhangs far past the wall as a detached floating slab (back) | trim the overhang and seat the roof on the walls |
| TW02_03_street_life_03 | MAJOR | just a stack of plain tan boxes, no props; does not read as street life | add street props (crates, barrels, stall, signage) |
| WT13_05_plateau_terrace_set_05 | MAJOR | only tiny scattered rock cairns, under-scaled, unlike its WT13 siblings | rebuild as a proper stepped plateau terrace matching the set |
| VC04_04_skull_city_building_04 | MAJOR | roof open with exposed rafters, reads as roofless box; floating base block | close the roof into a solid lid; remove floating block |
| HM01_03_rope_suspension_bridge_03 | MINOR | deck very thin/spindly for a 129-stud span | thicken deck and railings |
| HM06_03_switchback_wall_03 | MINOR | reads as loose stacked blocks, no clear switchback path | tie blocks into a continuous stepped wall |
| SP01_04_snow_spire_cluster_04 | MINOR | spire very thin for 168-stud height | widen spire base and rock cluster |
| WT13_02_plateau_terrace_set_02 | MINOR | dark hollow void under the back; thin black gap at base | close the underside into a solid mass |
| LM05_02_fortress_cliff_tower_02 | MINOR | thin splayed flaps at cliff base; tiny stray green speck | tidy base into solid rock, remove fleck |
| WT13_01_plateau_terrace_set_01 | MINOR | open grid deck reads as a grate with holes | fill the grid into a solid paved deck |
| WT13_06_plateau_terrace_set_06 | MINOR | central lantern reads as emissive/glowing (no-glow rule) | darken lantern glass to a flat tone |
| SD02_05_desert_ruin_block_05 | MINOR | thin splayed flaps around the rubble base | tidy base into solid chunky rocks |
| LM16_01_ring_temple_segment_01 | MINOR | stray base pieces; columns read as flat slabs | remove loose pieces, add column depth |
| SP01_06_snow_spire_cluster_06 | MINOR | spire very thin for 164-stud height | broaden spire and base |

## Repeating patterns
1. **Carved-stair switchbacks (LM07 family) are broken the same way both times**: hollow open boxes with black interiors and stairs floating in a void — the most serious defect in the slice, needs rebuilding, not patching.
2. **Roofs on the skull-city / shrine / ruin houses**: a recurring class of defect — overhanging detached roof planks, open/roofless tops with exposed rafters, and roofs floating off the walls (VC04_06, VC04_04, HM08_03, RD06_05).
3. **Thin splayed "flaps" at the bases of rock/cliff/ruin pieces** (LM05_02, SD02_05) — base geometry flares into thin shards instead of solid rock.
4. **Thin needle spires** (SP01_04, SP01_06) read unstable for their height.
5. **WT13 plateau-terrace set is inconsistent**: WT13_05 is tiny scattered rubble while its siblings are full terraces; WT13_01/02/06 each have a separate issue (grid-holes, hollow underside, glowing lantern).

## Worst 10 (most to least)
1. LM07_02_carved_stair_switchback_02 (REDO)
2. LM07_01_carved_stair_switchback_01 (REDO)
3. WT13_05_plateau_terrace_set_05 (MAJOR)
4. VC04_04_skull_city_building_04 (MAJOR)
5. TW02_03_street_life_03 (MAJOR)
6. HM08_03_cairn_shrine_03 (MAJOR)
7. RD06_05_abandoned_house_05 (MAJOR)
8. VC04_06_skull_city_building_06 (MAJOR)
9. WT13_02_plateau_terrace_set_02 (MINOR, hollow base)
10. WT13_06_plateau_terrace_set_06 (MINOR, glowing lantern)

## Originality
No external-franchise copies found. The Black Clover themed world concept art is the project's own supplied reference, and the skull-city / elden-tree / frosthold motifs are generic fantasy forms — no model reproduces a recognisable named emblem, character or building.

## Could not judge
Nothing was unjudgeable — all 36 models had a clear front/back sheet, and every id with a four-angle hero sheet was cross-checked. I did not need the larger single views to settle any verdict.
