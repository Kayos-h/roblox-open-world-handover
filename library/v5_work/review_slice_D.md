# v5 review — slice D (reviewer D), sheets 016–020

Models reviewed: 60 (LM05–LM08, LM23, LM24, LM10_01; HL01–HL07; FR01–FR03; VG04–VG07; SP01).
No hero sheets exist for any model in this slice. MCP server `@Roblox_Studio` was not configured/unavailable; not needed for an image review.

## Verdict counts
- OK: 28
- MINOR: 17
- MAJOR: 15
- REDO: 0

## Non-OK models

| id | verdict | what is wrong | how to fix |
|----|---------|---------------|------------|
| LM05_02_fortress_cliff_tower_02 | MINOR | stray thin side beam; plain grey base rock | remove/thicken beam, facet the base |
| LM07_01_carved_stair_switchback_01 | MAJOR | no readable steps; reads as rock mound | cut clear stepped switchback flights |
| LM07_02_carved_stair_switchback_02 | MAJOR | steps barely legible, rough pile | add defined treads and a landing |
| LM08_01_mountain_span_bridge | MAJOR | broken gappy deck, floating pieces, debris posts | rebuild one continuous solid deck + rails |
| LM23_03_gorge_wall_03 | MAJOR | flat bright-white waterfall slab clips as a glowing bar | recessed stepped water chute, muted blue, seated |
| FR01_03_giant_tree_03 | MAJOR | canopy = 2 blobs on a split bare trunk; reads as an arch | full connected canopy + solid single trunk |
| FR03_04_cave_mouth_04 | MAJOR | scattered detached/floating blocks, no solid opening | merge into one grounded arch with a clear mouth |
| FR03_05_cave_mouth_05 | MAJOR | same floating-debris mass, not a cave | rebuild as one connected arch, remove floaters |
| FR03_06_cave_mouth_06 | MAJOR | loose detached blocks, gaps, no opening | consolidate into a solid grounded cave mouth |
| VG04_01_tree_birch_01 | MAJOR | yellow-blotch "diseased" canopy; splayed flat-white cone trunk | slim upright white bark + mostly-green canopy |
| VG04_02_tree_birch_02 | MAJOR | same trunk/canopy defect | thin upright bole, yellow only as accents |
| VG04_03_tree_birch_03 | MAJOR | clone of 01/02 with same defects | fix trunk/canopy and vary shape |
| SP01_01_snow_spire_cluster_01 | MAJOR | blocky B/W camo patches, pencil-thin spire, detached base | coherent snow-on-rock shading, thicken, seat base |
| SP01_02..06_snow_spire_cluster | MAJOR (×5) | identical camo-patch + thin-spire + clone problem | recolour coherently, thicken, differentiate each |
| HL01_04_ice_spire_04 | MINOR | near-clone of HL01_01–03 | vary taper/chunk placement |
| HL02_02_ice_arch_02 | MINOR | close dup of 01; floating base debris | reshape arch, merge base chunks |
| HL03_01/02/03_glacier_tongue | MINOR (×3) | brown rock blotches read as dirty camo; clones | cut brown patches, cool tone, vary shape |
| HL04_02_ice_cave_mouth_02 | MINOR | near-identical to 01 | change opening/overhang |
| HL07_02_mine_entrance_02 | MINOR | close variant of 01 | alter framing/rubble |
| FR01_02_giant_tree_02 | MINOR | near-recolour of 01 | vary canopy/branch spread |
| FR02_05_forest_ruin_05 | MINOR | thin blank floating column | add break detail + base |
| FR02_06_forest_ruin_06 | MINOR | floating cap on lone thin column | anchor cap, add rubble |
| FR03_02/03_cave_mouth | MINOR (×2) | clones of FR03_01 | vary opening/stacking |
| VG05_02/03_cypress_swamp | MINOR (×2) | near-recolours of VG05_01 | vary canopy/root spread |
| VG06_01/02_marsh_hummock | MINOR (×2) | flat untextured green shard, clones | add tufts/mud rim/height, vary shape |

## Systemic issues
1. **Scattered "exploded" rock constructions** (LM08 bridge, FR03_04–06 cave mouths) — formations are loose floating chunks with gaps instead of one solid grounded mass. Fix: weld/overlap pieces into a connected body seated on z=0 before adding surface chunks.
2. **Blocky square colour camouflage** (SP01 snow spires ×6, HL03 glacier tongues) — random black/grey/white or brown patches instead of coherent snow-over-rock shading. Fix: paint by region (snow caps lighter, rock body one grey) not per-face.
3. **Clone siblings / low variety** — many sets are recolours of model 01 (HL01, HL03, HL04, FR03, VG04, VG05, VG06, SP01). Fix: change silhouette/proportion per variant, not just color.
4. **Stair/landmark legibility** (LM07 switchbacks) — "carved stair" and "giant tree" (FR01_03) don't read at distance. Fix: exaggerate the defining feature (step treads, full canopy).
5. **Flat glowing/relief-less slabs** (LM23_03 waterfall bar, VG06 hummocks, thin ruin columns) — single flat panels, one a near-white glowing bar. Fix: recess/step them, add relief, muted tone, no flat bright panels.

## Could not judge
Nothing was unjudgeable — all 60 cells and three confirming close-ups were legible. No hero sheets apply to this slice.
