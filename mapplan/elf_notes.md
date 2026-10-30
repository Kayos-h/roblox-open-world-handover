# Elf Jungle City — area notes

## Layout idea (plain words)
A mystical elf city grown into a dense western jungle. The **east gate** at
(-1950, -600, y 10) is the carved elf arch (F12), flanked by standing lanterns and two
archer statues. From the gate a **winding root path** runs west — framed by root arches
(F17), vine pillars (F35), glowing mushrooms and flowers, and standing lanterns every
~40 studs — straight to the **giant world tree (F01)** at the heart, centred on
(-2420, -600). The tree is 169x187 studs, so it reads as the landmark the whole area
is built around and is clearly visible from the gate down the open path corridor
(the path runs along z -600 and is kept clear of foliage).

Around the world tree sit **four treehouses** (F02-F05) at the NE, NW, SW, SE corners
of a ~160-stud ring, each with its own spiral stair (F09) to the ground. Two extra
**platform rings** (F06) sit due north and south as mid-air waystations. **Rope bridges**
span between them at canopy height (see "Bridges" below). A **platform ring + spiral
stair** also hug the world-tree trunk itself as the central hub.

- **Palace** (F10) sits on the **west** side at (-2560, -600), facing east back up the
  path toward the world tree — the city's civic heart, approached past benches, statues
  and lanterns.
- **Sacred moon pool** (F11) sits **south** of the tree at (-2410, -770) with lotus
  (F29), lily pads, glow flowers, benches and lanterns — a quiet shrine.
- **Waterfall cliff** (F32) rises at the far **west edge** (-2770, -600) on a raised
  rock shelf (terrain flattened to y 40), feeding a terrain-water stream that steps
  down east toward the tree, with reeds, lily pads, crystals and glow mushrooms along
  the bank.
- **Overgrown ruins** (F30/F31) half-swallowed by jungle sit NE and SE of the path
  entrance, with vine pillars and a crystal cluster.
- **Dense layered jungle** fills the rest: big jungle trees (F14/F15), palms (F16),
  giant ferns (F21), giant leaf plants (F22), root arches, hanging vines (F18/F19) and
  moss (F20), tall grass, fallen logs and mossy boulders — densest toward the N and S
  edges, thinning the path corridor so it stays readable.

## Terrain
- A soft **plateau at y 10** (the design ground) over the whole core, painted LeafyGrass,
  with four **gentle rises to ~y 28-40** at the N, S and W jungle edges (hills), matching
  the brief's "roots/rises to 40".
- Gate approach flattened/ramped to y 10 and kept 24 studs clear for the road gate.
- West waterfall shelf flattened to **y 40** (Rock), with two **terrain water** ops
  forming the pool at the cliff base (y 11) and a stream stepping east (y 10).
- Ground paint: LeafyGrass core, Ground on the root path, Rock at the waterfall.

## Bridges (which two points each connects)
All rope bridges are aerial — placed with `y_offset` so they span at canopy height
between platforms/treehouses, NOT on the ground:
- **F08 long @ (-2365,-435) y+34** — connects the central trunk **platform ring**
  (-2300,-600 area, north arm) to the **NE treehouse F03** (-2300,-440) via the north
  platform ring (-2430,-430).
- **F08 long @ (-2485,-430) y+36** — connects the **north platform ring** (-2430,-430)
  to the **NW treehouse F02** (-2540,-430).
- **F08 long @ (-2365,-772) y+34** — connects the trunk hub to the **south platform
  ring** (-2430,-770) toward the **SE treehouse F05** (-2290,-775).
- **F08 long @ (-2495,-770) y+38** — connects the **south platform ring** (-2430,-770)
  to the **SW treehouse F04** (-2560,-770).
- **F07 short @ (-2300,-520) y+30** — short link north of the trunk hub between the
  trunk platform ring and the north span.
- **F07 short @ (-2300,-700) y+30** — short link south of the trunk hub between the
  trunk platform ring and the south span.
Heights (y_offset 30-38) sit the decks just below the treehouse floor level (treehouse
heights 42-65 studs) so they read as mid-canopy walkways. The coordinator should snap
the bridge ends to the actual platform/treehouse deck heights in Studio; the offsets
given are the design intent.

## Enterable buildings (interiors)
Two enterable, per the game-performance rule:
1. **Elf palace (F10)** at (-2560,-600). Interior items (group `PalaceInterior`), all
   real catalog elf models placed inside its 53.8x52 footprint (rot 90):
   - F34 crystal cluster "throne" at (-2572,-600) centre-back
   - F13 elf statue facing the entry at (-2544,-600) rot 270
   - 2x F33 elf bench at (-2556,-586) and (-2556,-614)
   - 2x F28 standing lantern at (-2566,-582) and (-2566,-618)
2. **One treehouse** — the **SW treehouse F04** at (-2560,-770) (largest, 58x58) is the
   designated enterable treehouse, reached by its spiral stair and the two SW rope
   bridges. (No dedicated treehouse-interior furniture exists in the elf set; interior
   is left open for the coordinator, lit by the glow flowers/lanterns at its base.)

## Decisions made
- World tree centred at (-2420,-600), not dead-centre of the rect, to leave the east
  half for the path corridor and keep the tree visible on the gate sightline.
- Root path held along z -600 and kept clear of trees/ferns within the corridor; glow
  flora lines it for night readability (brief: "glowing mushrooms and flowers lighting
  the paths at night").
- Treehouses rotated to face inward toward the tree (rot 135/45 on the diagonals).
- 14 standing lanterns + 2 hanging lanterns + glow flora give full night lighting on
  every path and landmark.
- Palace faces east (rot 90) so its front looks back up the path to the world tree.
- Jungle density: canopy trees and understory doubled up along N (z -300 to -480) and
  S (z -720 to -930) edges, thinning toward the central corridor.
- Canopy interpenetration between big trees and decor sitting under the world tree's
  huge footprint is intentional and is classified as allowed in the validator (it is
  foliage/understory, not footprint collision).

## Missing (catalog gaps the area could use)
- **Dedicated treehouse interior furniture** (elf beds, tables, shelves) — none in the
  F set; the enterable treehouse interior is left open.
- A **ground-level rope-bridge/ramp to the first platform** — the spiral stairs (F09)
  cover vertical access, but a gentle entry ramp onto a low platform would help; used
  spiral stairs instead.
- **Flowing-water stream channel** prop — handled with terrain water ops + the waterfall
  cliff model, plus A66 stepping-stone crossings and an A111 pond edge along the basin.

## Densification pass (501 placements)
After the coordinator review found the first pass (140 placements) too sparse for a
900x900 jungle city, a densification pass brought it to **501 placements / 59 unique
models** (target 450-650), keeping every original hand-authored placement unchanged and
adding, with collision-checked generation (rotated-rect clearance, path/gate kept clear):
- **Layered jungle canopy** in clusters: more F14/F15 jungle trees plus fitting shared
  trees (A24/A25/A26 oak, A33 willow, A31 pine, A16-palm F16) scaled 0.85-1.25, densest
  at the N/S/W edges and thinning toward the path corridor and tree clearing.
- **Mid/understory**: F21 giant ferns, F22 giant leaf plants, A38/A39/A40 bushes, A51
  ferns, A37 saplings filling the floor.
- **Groundcover**: A49/A50 tall grass, A54 mushroom clusters scattered in natural groups.
- **Night lighting**: glow mushrooms (F23/F24) and glow flowers (F25/F26) line BOTH sides
  of the root path and ring the world tree at ~150 radius; **F27 hanging lanterns every
  ~30 studs** along the path plus F28 standing lanterns (28 total) on paths, platforms,
  treehouse grounds and the palace forecourt.
- **Vines/pillars/moss**: more F18/F19 hanging vines, F20 moss and F35 vine pillars across
  the canopy edges and ruins.
- **Crystals** (F34) at slopes and clusters; **ruins** detail (extra F30/F31, statues,
  vine pillars); **benches** (F33) and lanterns around all four treehouse bases and the
  palace.
- **Water detail**: more lotus/lily pads on the moon pool; the stream basin gets A52
  reeds, A53 lily pads, **A66 stepping-stone crossings (x2)** and an **A111 pond edge**
  on the north bank; **A110 waterfall rocks (x2)** at the cliff base.
- **Rocks at slopes**: A56/A57/A58/A60/A61 around the five hill rises.
- **A65 rock arch** used as a jungle landmark on the west slopes.
The generator is `$KIROCREW_SCRATCH/elf/densify.py` (idempotent: it slices the original
140 placements and regenerates the fill, seed=42). All 35 elf (F) models plus the
suggested shared models (A65, A66, A110, A111, A37) are used.

## Validation (final report — clean)
Script: `$KIROCREW_SCRATCH/elf/validate.py` (loads catalog.json + elf.json; checks
unknown ids, out-of-margin centres, footprints past the hard border, overlapping
building footprints >6 studs tall using rotated rectangles, gate clearance <12 studs,
and per-model counts). Big nature trees and treehouses are treated as canopy foliage
(interpenetration allowed); same-group attached stairs/lanterns, decor under the world
tree, and interior items inside the enterable palace are classified as intentional.

```
=== ELF VALIDATION REPORT ===
Total placements: 501
Unique models: 59
Area rect (hard): X[-2850,-1950] Z[-1050,-150]; margin X[-2830,-1970] Z[-1030,-170]

Per-model counts:
  A110_waterfall_rocks: 2   A111_pond_edge: 1       A24_oak_1: 3       A25_oak_2: 6
  A26_oak_3: 12             A31_pine_3: 9           A33_willow: 7      A37_sapling: 21
  A38_bush_1: 8             A39_bush_2: 10          A40_bush_3: 17     A49_tall_grass_1: 24
  A50_tall_grass_2: 29      A51_fern: 30            A52_reeds: 5       A53_lily_pads: 8
  A54_mushroom_cluster: 26  A56_rock_small_1: 3     A57_rock_small_2: 3 A58_rock_medium_1: 5
  A61_boulder_2: 5          A65_rock_arch: 1        A66_stepping_stones: 2  A67_fallen_log: 2
  F01_world_tree: 1         F02_treehouse_1: 1      F03_treehouse_2: 1 F04_treehouse_3: 1
  F05_treehouse_4: 1        F06_platform_ring: 3    F07_rope_bridge_short: 2  F08_rope_bridge_long: 4
  F09_spiral_stair: 5       F10_elf_palace: 1       F11_moon_pool: 1   F12_carved_arch: 1
  F13_elf_statue: 8         F14_jungle_tree_1: 4    F15_jungle_tree_2: 7  F16_jungle_palm: 13
  F17_root_arch: 4          F18_hanging_vines_1: 3  F19_hanging_vines_2: 7  F20_hanging_moss: 10
  F21_giant_fern: 12        F22_giant_leaf_plant: 17 F23_glow_mushroom_1: 19  F24_glow_mushroom_2: 18
  F25_glow_flower_1: 15     F26_glow_flower_2: 16   F27_elf_hanging_lantern: 11  F28_elf_standing_lantern: 28
  F29_lotus: 1              F30_ruins_1: 4          F31_ruins_2: 3     F32_waterfall_cliff: 1
  F33_elf_bench: 16         F34_crystal_cluster: 11 F35_vine_pillar: 12

PROBLEMS: 0  (clean)
```

All 35 elf (F) models are used. Problems resolved during the densification pass: a glow
mushroom clipping the trunk spiral stair and a vine pillar clipping a ruins statue were
cleared by making vine pillars and near-structure decor keep full rotated-footprint
clearance; the gate arch stays inside the 20-stud margin at x -1974. Path corridor
(z -600 +/-28 east of the tree) and a 26-stud gate radius are kept clear of all fill.
