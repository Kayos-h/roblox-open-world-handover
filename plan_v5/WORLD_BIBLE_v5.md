# World Bible v5: redesign plan for the Black Clover-inspired island

Written 30 Oct 2026, updated 11:55 after three corrections: remove only the plain arch (not every arch), roads must cross the mountains and the rivers need Himalayan-style bridges, and a giant enterable wizard tower stands on top of the Himalayan plateau. Sources: the MASTER_WORLD_REDESIGN_PROMPT, the three saved reference pictures (`../reference/`), the round 1-5 review reports, the stitched top-down view, and a scan of the exported terrain grid (`terrain_stats.json`, `sites_candidates.json`). Plan only: nothing is built, and nothing needs Blender or Studio until section 11 says so.

Working names come from your concept map and are placeholders. Every model is an original design; the "Black Clover" title art is not used in the game.

New plan files from this round: `world_v5_terrain.json` (the planned landforms as data), `terrain_v5.py`, `route_v5.py`, `roads_v5.json`, `ROADS_V5.md`, `WIZARD_TOWER_BRIEF.md`, `wizard_map_relief.obj`, `wizard_map_color.png`, `wizard_map_preview.jpg`, `topview_sketch_v5.jpg`, `concept_vs_sketch.jpg`.

## 0. Following your concept map

The concept map (`../reference/world_concept_topdown.png`) is the target composition. Every element is matched to a place on our island:

| Concept label | On the concept map | Plan (world coordinates) | Status |
|---|---|---|---|
| The Elden Tree (Ancient Forest) | NW, giant tree, waterfalls, ruins | Our world tree (-1560,-430) is the Elden Tree. The forest runs north to the NW corner (nw_tarn (-1350,-1900), peak (-1752,-1632)) with giant-tree groves, falls, ruins and caves. Natural, no glow | adapt |
| Frosthold Fortress (Snow Mountains) | NE, fortress on a jagged peak, glacier lake | Fortress on the NE massif (1632,-1608), h 511; jagged spires; frozen lake (exists) | match |
| Himalayan Roof Plateau and the wizard tower | not on the concept map (your addition) | High plateau (1380,-1400), level y 322, ringed by peaks; the giant enterable wizard tower on the pad at (1380,-1320) | **new, core** |
| The Castle Town (Royal Capital) | centre-north, spired castle city on a river-circled island with bridges | Capital kit per the castle-town picture; river horseshoe, 3 towered bridges; keep on the castle plateau | match |
| The Skull City (Forbidden Zone) | east, dark rock, red lava veins, giant carved skull | East coast: skull cliff (2208,-936) h 260; city floor around (2136,-576) to (2424,-288); basalt and cracked-lava terrain; dark ruins | **new, core** |
| The Sands of Elysium (Desert) | SE, red mesas, ring temple, ruins, oasis | SE desert: canyons, red mesa clusters, ring temple (1660,1130), buried temple (2160,1248), ruin blocks, oasis | match |
| Rusty Village (Starting Area) | west/south-west, farmland, church spire, stream | West farm village near (-1248,528): farmland, spired church, mill. Town 1 stays the spawn | **new, small** |
| The Harbor City (Trade Port) | south, walled port with ships, waterfall into a cove | Harbour (exists) gets walls, towers, a cove with a waterfall | adapt |
| River network, stone bridges, viaduct | rivers wind from the forest through the centre | Forest river, greenheart stream, trunk rivers either side of Town 1; 12 routed bridges plus 2 viaducts (section 7) | match |
| Coast, sea stacks, ruin islets, floating island | all around, NE corner | 6 cliff pieces, 3 stacks, 3 ruin islets, 6 floating islands | match |
| Clouds around the edges | all around | Clouds layer and haze set in Studio (no models) | note |

Not copied: the glow on the Elden Tree (your elf rule stays), the Black Clover title art, any existing game's designs.

## 1. How it should look from above, and the environment around it

Picture: `topview_sketch_v5.jpg` (a rough sketch drawn from the terrain data and the plan files, not a game render) next to the concept map in `concept_vs_sketch.jpg`.

**The island as one image.**
- Coast: ragged, with headlands, coves, cliffs on the west and south, beaches on the east and south-east, sea stacks and ruin islets, shallow turquoise water that fades to navy.
- Colour zones: dark ancient forest NW, white Himalayan massif NE with a pale plateau on top, orange-red desert SE, dark volcanic east coast, light green farmland and meadow in the middle and west, grey cliff bands where land meets sea.
- Reading order for the eye: the white NE massif with the plateau and the tower on it, then the capital's orange roof mass inside a grey ring wall under its castle plateau, then the dark canopy bowl of the Elden Tree, then the ring temple in the desert, then the harbour cove with its waterfall.
- Water: two trunk rivers either side of Town 1 that start at the capital's river loop; a forest river from the NW tarn to the elf lake; a greenheart stream through the west village to the west lake; meltwater from the plateau tarn over Roof Falls into the alpine ice lake; lakes with irregular outlines and reed margins, never round discs.
- Land: 11 low hills in the central band (20-42 studs high) so it stops being a carpet, a marsh around the west lake, two canyons in the desert, a crater east of centre, jagged ridge lines and 6 tall peaks in the NE.
- Roads: tan ribbons that follow valleys, climb in hairpins, pass through ridges and cross rivers at bridges. No straight runs.
- Edges between zones are gradients, not lines: forest to pine belt to scree to snow; forest to scrub to dry grass to sand; meadow to ash flats to black rock; grass to reeds to dunes to beach.

**Each settlement from above and in its environment.**

| Place | From above | Environment around it | How you arrive (natural entrance) |
|---|---|---|---|
| Capital | Grey ellipse ring wall, orange-roof mass, plaza, castle on the raised plateau behind, river loop with bridges | Orchards and meadows outside the wall, roads converging on the bridges | The road crosses a towered bridge and meets the capital's own gatehouse, built into the wall |
| Elf valley | Dark-green canopy bowl, lighter crown of the giant tree, houses under the canopy, waterfall at the west rim | Forest thickens toward the cliffs; ferns, moss rocks, giant trees | The path dissolves into forest; two large trees frame it; a carved signpost; stepping stones |
| Town 1 | Compact dark cluster with the skull HQ and an avenue to the plaza | Kitchen gardens, hedged fields, a river each side, hills at the edges | The road widens into the avenue; a sign and low stone markers; hedges |
| Alpine village | White roofs on a shelf around the frozen lake | Pine belt, snow meadow, scree | The road switchbacks up; log fence; sign |
| Wizard tower | A violet-grey drum with a gold star on a pale plateau, courtyard ring around it | Snow-dusted rock, prayer-flag poles, cairns, the tarn to the east | The Roof road arrives over the courtyard to the porch; terrace stair; lantern posts |
| Harbour | Curved quay, white and blue roofs, ships in the cove | Cliffs on both sides, terraced slope, waterfall into the cove | A gentle descent from the north road; sign; the lighthouse seen first |
| Rusty / desert village | Tan cluster on the desert edge near a canyon | Scrub, dry fields, dust | The road passes between two boulders; sign |
| West farm village | Patchwork fields, spired church, stream | Hedgerows, orchards | A lane between hedges |
| Skull City | Dark ruins at the foot of the skull cliff, red veins in black rock | Ash flats, scorched trees | A broken road with warning stones |

**Entrances: only the plain arch goes.** The plain arch that was placed at the entrances is removed and replaced by a natural entrance (the road narrows or widens, bends, and is framed by trees, boulders, hedges or a fence, with one sign). Other arches and gates stay when they are a real design: the capital's gates and gatehouses (rebuilt as part of the ring wall, CP06 to CP08), the royal-garden rose arches, ruined arches deep in the forest, natural root and rock arches, graveyard gates and bridge arches.
- Remove (from the placement plans; a Studio scan lists what is live): `H12_region_entrance_arch` (5 in the country plan, at the region entrances), `A104_wooden_gate` (4), `D04_06_gate_arch_a` and `D04_07_gate_arch_b` (elf valley, at (-1300,-406) and (-1885,-437)), and `F08_13` and `F08_14` gate arches if any are live.
- New: `village_sign` x6 and `entry_rock_pair` x4 (rows NE01, NE02). Hedges, fences, trees and signposts come from the existing library.

**What matters most for the look.** Terrain pass first (hills, rivers, canyons, crater, Skull City grading, the Himalayan peaks and plateau, cliff coast), because it changes the top view the most and costs no models. Then the landscape kit (fields, hedges, woodlots, signs, boulders). Then the hero landmarks, the wizard tower first. Then settlement detail.

## 2. Diagnosis (phase 1 of the prompt, from data and reviewers)

Land share by region and what it looks like from above (24-stud grid, 168-stud window; "varied" = relief of 60+ studs):

| Region | Land | Green | Rock | Sand | Snow | Varied relief | Verdict |
|---|---|---|---|---|---|---|---|
| NW forest and elf valley | 21% | 67% | 30% | 1% | 0% | 58% | Already varied; needs landmarks, not terrain |
| NE frozen highlands | 15% | 24% | 56% | 1% | 17% | 77% | Dramatic; needs the plateau, tower, fortress, passes, glaciers, spires |
| North: capital and castle | 21% | 73% | 20% | 1% | 1% | 37% | Rectangular wall, no river, weak skyline |
| Centre: Town 1 | 9% | 92% | 4% | 0% | 0% | 5% | **Green carpet** |
| SW plains | 12% | 82% | 16% | 1% | 0% | 33% | Needs farms, marsh, rolling hills |
| South: harbour belt | 6% | 94% | 2% | 2% | 0% | 0% | **Flattest and greenest band** |
| SE desert and badlands | 10% | 20% | 4% | 22% | 0% | 28% | Flat; only 4% rock, so no canyons in the terrain |
| East coast | 8% | 69% | 15% | 6% | 1% | 33% | Rugged; becomes the Skull City |

Other findings:
- Reviewers (round 5): forest reads as an even carpet from above (7/10), rivers and lakes are hard blue cut-outs (6/10), sea is flat (7/10), roads have no bridges and junctions have no props.
- Landmarks: only 1 of the 7 types exists (the world tree). The colossal waterfall exists in small form (109 studs). The summit pad for a tower exists at (1380,-1320), y about 320, on a high shelf (the terrain around it is already 317 to 324 over 180 studs north to south).
- The capital is a rectangle (walls x +-490, z -1934..-1237) with the castle compound on a raised plateau behind it (keep at (0,-2275)). No river, weak skyline.

## 3. Principles

1. Keep the existing geography where it works: Town 1 zone (x +-318, z -545..311), the elf valley pad, harbour, alpine shelf, the capital pads. Archive, never delete. The terrain spec leaves the Town 1 zone untouched.
2. Change the world in this order: terrain forms, rivers, roads, landmarks, regional kits, small details.
3. All big landform changes go into ONE terrain regeneration (about 8 minutes plus replays of road paint, plinths, patches).
4. One dominant material and roof family per settlement, different from every other settlement.
5. No glow in the elf valley, and no emissive meshes anywhere. No Black Clover names or shapes. Everything anchored. At most 1-2 enterable buildings per settlement (the wizard tower is the one big landmark that is fully enterable).
6. Performance first: measure before adding (section 10).

## 4. Regions

| Region | Identity | Landmark | Key terrain change |
|---|---|---|---|
| NW Ancient Forest (Elden Tree) | Giant trees, hidden clearings, waterfalls, caves, overgrown ruins; natural | World tree (exists) plus the colossal waterfall on the west rim | Raise the rim near (-1800,-672) to about 290; 3-tier falls into the elf lake |
| NE Himalayan highlands (Frosthold) | Massive jagged silhouettes, a high plateau, glaciers, frozen lakes, gorges, dangerous passes | Frost fortress (1632,-1608); Roof Plateau with the wizard tower (1380,-1320) | Section 5 |
| North: Kingdom Capital (Castle Town) | Ring wall with cone-roofed towers, keep on a terrace, orange-roof town, river around it | The capital skyline (section 6) | Horseshoe river from the north pool (380,-2350) around both walls |
| Centre: crater and heartland | Rolling hills instead of a carpet, marsh by west_lake (-660,300) | Magical crater at (1368,-312) | 11 low hills, 2 shallow river valleys, crater bowl (radius 240, depth 46) |
| SW Greenheart Plains and west farm village | Farms, windmills, rolling grass, ruined watchtowers, natural rock bridges | Ruined civilization on plateau_e (760,470); ruined castle on plateau_nw (-760,-980) | Gentle hills, stream valleys, small marsh near sw_pond (-1150,1150), village terrace near (-1248,528) |
| SE Desert Wasteland (Sands of Elysium) | Sandstone canyons, red mesas, oasis village, buried temples | Buried temple (2160,1248); ring temple about (1660,1130) | Two canyon systems 34 deep, about 100 wide, about 900 long |
| South: Harbour coast | Cliff coves, sea stacks, reefs, ruin islets | Lighthouse and harbour (exist) | Add 4-6 headlands and coves, a cove waterfall |
| East coast: Skull City | Dark volcanic cliff with a giant carved skull, lava veins, ruined dark city | Skull cliff (2208,-936) | Grade a city floor near (2136,-576)..(2424,-288); basalt and cracked-lava paint |

Sites came from the grid scan and are good to about +-30 studs. Final siting is checked against the live terrain before anything is placed. The landforms are in `world_v5_terrain.json` and are applied by `terrain_v5.apply_spec`.

## 5. The Himalayan highlands and the wizard tower

**Landforms (all in `world_v5_terrain.json`).**
- **Roof Plateau:** ellipse centre (1380,-1400), 560 x 380 studs, level y 322 with a gentle roll (the live terrain is already about 320 there). Blend to the old terrain over 150 studs to the north and 110 to the sides, and a short cliff of about 50 studs on the south edge above the alpine ice lake (y 131).
- **Peaks:** Spire of Dawn (1140,-1790) h 640, Twin Fang North (1540,-1930) h 610, Twin Fang South (1700,-1860) h 575, Wall Peak (940,-1600) h 520, East Horn (1930,-1520) h 540, Snow Saddle Peak (1260,-2100) h 560. Anvil Ridge and Frost Spine run between them. The Frost fortress peak (1632,-1608) is kept (about 550).
- **Water:** frozen Roof Tarn (1580,-1500), meltwater down the plateau to Roof Falls (1480,-1205): three ribbons, 26 studs wide, a drop of 190 studs into the alpine ice lake. Meltwater Notch is a small gorge above the falls. Frost Gorge (depth 40, about 110 wide) cuts the east side from (2272,-1348) to the coast.
- **Tower pad:** centre (1380,-1320), floor y 324, shell radius 55, terrace radius 95, courtyard radius 140. The plateau leaves 150 studs of room on every side of the courtyard.

**The wizard tower** (`WIZARD_TOWER_BRIEF.md`, rows WT01-WT13): 300 studs tall, enterable, 8 levels. The Map Hall on the ground floor has THE CIRCULAR MAP in the middle (a 44-stud stone relief map of the whole island on a brass-ringed table; its mesh and colour map are already made from the plan: `wizard_map_relief.obj`, `wizard_map_color.png`) and curved bookshelf bays along the walls. Library galleries, an archive, an alchemy lab, the archmage's study, a star room and a telescope observatory above, joined by a wide helical stair. It gets the most review rounds of anything in v5.

**Other highland pieces:** hidden monastery pocket beyond Frost Gorge at (2450,-1480) reached only by the 116-stud rope bridge; carved Cloud stair from the tarn down to the terraces; mountain shrine, snow watchtower, ice spires, glacier tongues, mine mouths (rows HL01-HL07, HM09).

## 6. Capital and castle town (reference: the castle-town picture)

- One polygonal ring wall (12 corner towers on an ellipse inside the existing pad: centre (0,-1585), about 490 by 350 studs), not a rectangle. 8-stud wide red-brown wall-walk, white-capped inner parapet, crenellated outer edge, round towers with maroon cone roofs. Gatehouses are part of the wall.
- The keep stands on the castle plateau (raised terrace, y 92) at the back, with a grand stair down to the town and retaining walls.
- A dense half-timbered town inside with ONE dominant roof family (orange-red) and value variation (replaces the nine hues).
- 5 distinct skyline towers (clock, bell, observatory, beacon, water tower), an order headquarters with its own name and shape, a plaza monument.
- Horseshoe river with a water gate, quay walls and 2 towered bridges.
- Keep the position. Moving 1,349 items is risky. The capital becomes the focal point through roads, rivers and skyline.

## 7. Roads, mountain passes, tunnels and bridges (routes in `ROADS_V5.md`)

Routing method: least-cost path on the 24-stud grid after the planned landforms. The cost rewards a grade near 0.16 (a road that climbs 190 studs needs about 1,200 studs of path, so it zigzags), forbids sea, lakes and cliffs, and prefers existing roads, so new roads merge into trunks. Result: 26 routes, about 30,000 studs, every region connected.

**The loop through the mountains.** Capital south gate, Gale Pass road (1,573 studs, 2 hairpins, top 177) to the low pass at (950,-1019). From there the **Roof road** climbs the south-west flank (997 studs, 4 hairpins, 147 studs of climb, a 120-stud rock-cut tunnel through a rib at (1003,-1148) to (1040,-1232)) to the tower porch at (1380,-1250). The Lake shore road joins the low pass to the alpine village. From the alpine village the **Dragonback road** climbs the east flank in hairpins to terraces at 290 studs, with a 216-stud tunnel and a 72-stud tunnel and cliff galleries, to a ledge above **Frost Gorge**. A **116-stud rope suspension bridge** crosses the gorge at (2448,-1358) to the hidden monastery pocket. The Highland descent runs down to Skull City. The Cloud stair (carved) links the plateau tarn to the Dragonback terraces. Capital, Town 1, alpine and the tower are one loop; Skull City, the crater, the desert temples, the west village, the elf valley, the ruined castle, the ruins and the harbour hang off it.

**Bridges (12 routed, plus 2 viaducts BR01 for big valleys).**

| Kind | Count | Where | Style |
|---|---|---|---|
| Rope suspension | 1 (116) | Frost Gorge (2448,-1358) | Himalayan: stone anchor towers, plank deck, prayer flags (HM01) |
| Timber cantilever | 1 (28) | Roof Tarn outlet (1552,-1415) | Himalayan, small roof (HM02) |
| Stone arch | 7 | Farm road, East road, Gale Pass, Ash road, Old road, Coast road, Trade road | Existing F08 bridge models, re-used |
| Towered stone | 3 | South road, Farm road (harbour side), West gate road (capital) | Next to the capital and harbour |

More rope bridges can be added where a story needs them; the kit has 3 spans (60, 90, 116).

**Mountain road kit:** 3 tunnel mouths and 2 lining pieces (rectangular timber frames in rock, no freestanding arches), 2 cliff galleries, 3 switchback retaining walls, prayer-flag strings, cairns (rows HM01-HM09). Targets for the rest of the map stay: 8 watchtowers, 12 camps, 6 waystations and trading posts.

## 8. Blender work

See `V5_MANIFEST.md` and `.csv`. Counts: P1 core 106, P2 region completion 289, P3 optional 4, total 399 new, plus 5 reworks. 20 hero models (40k+ triangles); the heaviest are the wizard tower shell (150k), its interior (90k) and the circular map (60k), which are the one allowed exception to the 60k hero limit. Style guide: chunky stylised shapes, warm saturated roofs per settlement, grey-lilac stone for the capital, indigo and copper-green for the wizard tower, no emissive parts. The 12 gate models were dropped when the plain arch was removed; 10 natural-entrance props took their place.

## 9. Environmental storytelling

Per region the placement plan lists what happened there (for example, a battlefield at the plains crossing, an abandoned village by the desert canyon, the wizard tower's archive of the island's history). No random scatter. The 13 story props and 9 trail landmarks already in the library are reused first.

## 10. Performance

About 270,000 instances now and the place has never been play-tested. Before adding anything: play-test and measure frame time at 4 spots (capital, elf valley, alpine, desert). Budget: new content at most +30,000 instances, with matching cuts (thinner undergrowth, merged repeats). Heroes at most 60k triangles (the tower excepted), everything else at most 18k, each MeshPart at most 20k triangles. The tower interior is built from instanced props (about 40 shelf bays and 30 other props). Streaming stays on; the tower exterior is set to persist so it shows from far away.

## 11. Prep and order of work

| Step | Needs | Status |
|---|---|---|
| World bible, manifest (399), terrain scan, sites, plan picture, top-view sketch | nothing | **done** |
| Priority areas plan and Blender briefs (capital, elf, Town 1, natural entrances) | nothing | **done** |
| Wizard tower brief and the circular map source data | nothing | **done** |
| Terrain change spec as data (`world_v5_terrain.json`) with the Himalayan plateau | nothing | **done** (tuned on the live terrain later) |
| Road and river routing, bridge, tunnel and camp sites | nothing | **done** (bridges, tunnels, hairpins); camps and towers next |
| Placement plans for the new models (placeholder sizes) | nothing | **done** (934 draft placements in `mapplan\v5_*.json`, `PLACEMENT_V5.md`) |
| Blender style guide and one brief per row (V4 worker format), worker plan and prompts | nothing | **done** (`V5_BRIEFS.md`, `library\V5_STYLE_GUIDE.md`, `v5_worker_plan.md`, `worker_prompts\`) |
| Review briefs and camera lists for the new regions | nothing | **done** (121 cameras in `shots\v5`, `BRIEF_v5.md`, `MODEL_REVIEW_BRIEF.md`) |
| Performance scan and play-test probe (Luau), upload script for v5 names, placeholder builder | nothing | **done as drafts** (`rebuild\v5\`, `upload_v5.ps1`; the upload dry run is tested) |
| Runbook of the next steps | nothing | **done** (`RUNBOOK_v5.md`) |
| Terrain generator patch that applies `world_v5_terrain.json` (`patch_terrain_gen_v5.py`) | Studio to test | first Studio day |
| Studio plugins backed up, reinstall checklist | nothing | **done** |
| Model building (P1 first, the wizard tower first of all) and upload | Blender | blocked |
| Terrain regeneration, plain-arch removal, placement, photos, play-test, archive export | Studio | blocked |

Estimates (V4 ran about 40 models an hour with three workers including reviews; heavier models about 27 an hour): P1 core 106 about 5.5 hours (the tower alone takes about 2); P1 plus P2 (395) about 16 hours; all 399 about 16 hours. Studio part: terrain pass about 2 hours, placement about 5 hours, tower assembly about 1.5 hours, review loops about 25 minutes each.

## 12. Decisions taken (you said no decisions)

1. Scope: build in tiers, P1 first (the priority areas plus the hero landmarks, wizard tower first), then P2. Nothing waits for approval.
2. Skull City and floating islands are in the plan (they are on your concept map).
3. Elden Tree stays natural, no glow (your elf rule).
4. Capital stays where it is. Town 1 stays the spawn; the west farm village is a small early-game village.
5. Entrances: only the plain arch goes; villages get natural entrances, special gates stay.
6. The old "abandoned magic tower" is replaced by the enterable wizard tower; the pad at (1380,-1320) stays.
7. The Himalayan roads are built even where the lowland is easier, because you asked for roads through the mountains.

## 13. Studio reinstall checklist

1. Install Roblox Studio and sign in.
2. Plugins are still in `%LOCALAPPDATA%\Roblox\Plugins` (`MCPPlugin.rbxmx`, `RojoManagedPlugin.rbxm`, `VesperHeadlessRunner.rbxmx`). Copies are in `Desktop\roblox_backup\studio_plugins` and `town\plan_v5\studio_plugins`.
3. Start the bridge (`_start_bridge.ps1`), open place 103847533321973, click Connect on the MCP plugin, ping with `st.ps1`.
4. Check that GrassLength still reads 0.3 and that the place opens as the 06:05 save.
