# Harbour — area notes

**Area rectangle:** X -1000..-200, Z 2300..3100 (south coast). 20-stud inner margin kept.
**Heights:** sea surface Y 0; town slope ~Y 8; quay apron Y 4; sea carved south of z≈2900.
**North gate:** (-600, 2300, y 8) — a 24-wide cobbled main street runs straight south from it to the quays; the gate's 40-stud approach is kept clear.

## Layout idea (in plain words)
A lively working harbour on a south-facing bay. You enter at the **north gate** and walk down the **main street** (lamps alternating every ~40 studs) past two rows of harbour houses that face each other across the street. Partway down, a **side lane runs west and another east**, each lined with more harbour houses, and the main street widens into a small **town square** with a fountain, benches and greenery. The street then opens onto a **market plaza** (fish stall + fruit & cloth stalls) with the **tavern** on its east side and the **harbour master's office** on its west side — the two enterable buildings, both looking out over the water. West of the plaza runs the **warehouse row** backing onto the slope with their big doors to the quay.

The **quay apron** (Y 4) runs along the waterfront at z≈2885. Two **finger piers** reach south into the bay (east pier straight out to a deep berth; west pier with an L corner). The **cargo crane**, pallets, crate stacks, rope coils, anchor, net rack, lobster traps and barrels cluster on the apron; a **ship's bell** and **pier stairs** sit at the quay front, with **mooring bollards** and **piling clusters** along the piers and **gangplanks** bridging to the boats.

**Ships** are moored and floating at the piers: the **galleon** at the deep east berth, the **merchant ship** broadside to the west pier, two **fishing boats** and a **fishing boat 2** between the piers, and three **rowboats** near the shore and beach. Three **buoys** mark the channel out in the bay.

The **west end** is a raised **rocky headland**: the **small fort** (3 cannons along its seaward wall, flag, brazier) guards the bay mouth, and the **lighthouse** stands at the headland tip — visible straight down the quays from the east. A **breakwater** of four rock segments arcs from the west spur across the bay mouth to shelter the anchorage; a run of **seawall** segments armours the eastern shore. A **beach** of sand fills the east-centre shore where the rowboats are drawn up. Out on the east edge, a **stilt house** (G26) stands over the shallows on piling clusters with its own gangplank to shore.

## Coastline shaping (terrain ops, in order)
1. `plateau` — base town land at Y 8 sloping outward (Grass).
2. `ramp` — the slope band from the gate (Y 8) down toward the quay (Y 4), Ground.
3. `flatten` — quay apron at Y 4 along the waterfront (Cobblestone).
4. `water` — carves the curved bay south of z≈2900 down 22 studs, surface at Y 0.
5. `ramp` + `paint` — a Sand **beach** section on the east-centre shore running gently into the water.
6. `hill` + `paint` (Rock) — the **rocky headland** on the west for the fort + lighthouse.
7. `hill` (Rock) — a small west spur as the breakwater root.
8. `flatten` — the main-street cobble spine from the gate down to the quay.
9. `paint` (Grass) — town verges.

## Waterline / y_offset decisions (why each is what it is)
Model origin is bottom-centre and the coordinator snaps to the ground found under (x,z). Over the carved bay that "ground" is the seabed at Y≈-22, so floating objects get a positive `y_offset` to lift their hull bottom up near the Y 0 surface. Values chosen so roughly a quarter-to-third of each hull sits below the waterline:
- **Galleon (G06, h 60.9):** `y_offset 16` → hull bottom ≈ Y -6, deep draught, decks well clear.
- **Merchant ship (G07, h 41.7):** `y_offset 13` → hull bottom ≈ Y -9.
- **Fishing boats (G08/G09, h ~18):** `y_offset 13` → bottom ≈ Y -9, small shallow draught.
- **Rowboats (G10, h 2.5):** `y_offset 20.5` → bottom ≈ Y -1.5, sits barely in the water near the beach.
- **Buoys (G20, h 10.5):** `y_offset 18` → base ≈ Y -4, bobbing with the marker above water.
- **Breakwater (G29):** `y_offset -2` → settles slightly into the seabed rock so no gap under it.
- **Piling clusters (G05) at pier ends / stilt house:** `y_offset -4` → driven into the seabed.
- **Gangplanks at the quay edge:** `y_offset -1` → meet the apron and the deck.
- **Stilt house (G26) over the shallows:** `y_offset 26` → floor lifted from seabed to quay level (Y≈4) so it stands on its pilings over the water; its gangplank `y_offset 22` reaches the floor.

The piers themselves (G01–G04) include their own submerged pilings in their height, so they are placed at ground level at the quay edge with no offset; the coordinator snaps them to the apron/seabed transition.

## Enterable buildings (only two, per the performance rule)
- **Harbour tavern (G27)** at (-560, 2600), faces south over the harbour. Interior: table + chairs + stool + barrel + candle cluster + hanging lantern (group `TavernInterior`, coordinates inside the ~23×23 footprint). A terrace with two tables, chairs and a hanging lantern sits in front toward the water.
- **Harbour master's office (G14)** at (-660, 2640), faces south. Interior: desk/table + chair + notice board + candle cluster (group `HarbourMasterInterior`, inside the ~22×15 footprint). Flag pole and notice board outside by the door.

## Sightlines & quality notes
- The **lighthouse** at the west headland tip is on open rock, visible straight along the quay front from the east berths.
- Houses face the street in two rows with varied models (G24/G25/G26 mixed) and mirrored rotations across the street.
- Lamps: iron city lamps down the main street (alternating sides, ~40 studs); rustic wood lamps along the quay (~45 studs); wall lanterns on the two enterable buildings.
- Props clustered in natural working groups (cargo by the crane, nets/anchor/traps on the apron, barrels by the tavern) rather than spread evenly.

## Missing (things the area really wants that the catalog lacks)
- **Water plane / sea surface effect** — the catalog has no ocean material model; the sea is a terrain `water` op, so actual animated water + foam at the shoreline is the coordinator's/Studio's job. The G-kit has no wave or shoreline-foam prop.
- **Seagulls / fish / dock animals** — explicitly out of phase (need rigging); listed in MAP_MODEL_LIST "NOT AVAILABLE".
- **Hanging harbour sign for the tavern** — used A94-style props exist in `props` but no dedicated harbour shop sign; omitted rather than faked.
- No other true gaps: all 33 harbour models (G01–G33) were placed.

## Densification pass (coordinator review)
The first plan (139 placements) read too sparse for an 800×800 harbour town, so a densification pass brought it to **301 placements / 98 unique models** while keeping the original layout intact. Added:
- **More houses & lanes:** the two main-street rows extended further south, plus a **West Lane** and **East Lane** of harbour houses branching off the main street (eight more houses each side, varied G24/G25/G26, mirrored rotations, ≥2-stud gaps), with cobble T-junction + curb stones at the junctions.
- **Town square:** a small fountain (A109) with wood benches facing it, planters, flower patches, an oak and a bush, and a shop sign.
- **Upper-slope greenery:** oak/pine/fruit-tree groups, bushes, mixed flower patches, tall grass, low stone walls and a picket fence + gate marking garden yards behind the houses.
- **House details:** window/planter boxes and wall banners on the fronts, clay pots by the tavern.
- **Dense dockside story clusters** on the quay apron: a **fish-landing** (hand cart, fish crates, barrels, trap, bucket), a **cooperage** by the warehouses (barrels, sack pile, firewood, wheelbarrow, crate stacks, pallets), a **net-mending station** on the far west quay (net racks, rope coils, traps, stool, anchor), and a **general cargo staging** mid-quay (pallets, crates, sacks, bollards, rope).
- **Quay-wall detail:** ladders (A91) down the quay face at intervals, an iron railing (A103) along the back of the apron, and **benches facing the bay** along the quay front.
- **Lighting to 35–45 stud spacing:** a filled second quay-lamp row, lamps down both side lanes, a double lamp at the square, more wall lanterns on house fronts, a hanging lantern on the harbour master and a brazier at the quay head.
- **Shoreline dressing:** more headland/breakwater rocks and boulders, pebbles and reeds at the beach, a fallen log and rowboat gear on the sand.

Previously-unused models now placed per the review list: A100_fence_picket, A102_stone_wall_low, A103_fence_iron, A104_wooden_gate, A109_fountain_small, A87_bucket, A89_clay_pot_2, A91_ladder, A96_wall_banner, A81_wheelbarrow, A10_curb_stones, A03_road_tjunction (A09_stairs_6 was not needed — the slope is handled by the terrain ramp, so it was left out rather than forced in). Building clearance (≥2 studs), the gate approach and the quay walkways were all kept clear, and the ship hulls keep their documented waterline `y_offset`s.

## Validation results (final, clean)
```
=== HARBOUR PLAN VALIDATION ===
placements: 301   terrain ops: 11   unique models: 98
area rect X -1000..-200  Z 2300..3100  (margin 20)

NO PROBLEMS. Plan is clean.
```
Checks run: unknown model ids (none), placements outside the rectangle minus 20-stud margin (none), overlapping building footprints using rotated rectangles with >1-stud tolerance for models taller than 6 studs (none — lighting, wall-/float-mounted `y_offset` attachments and interior items are excluded as non-footprint), blockers within 12 studs of the north gate (none), and counts per model (all 33 G-models present; the full per-model tally is printed by the validator). Four overlaps found during the densification pass were fixed by removing an east-row house that stepped into the tavern, moving the town-square oak off a west-row house, and relocating a slope oak and bush clear of an east-lane house; re-run is clean.
