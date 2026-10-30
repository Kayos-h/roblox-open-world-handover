# Town 1 (spawn town) — fixes plan notes

**Agent:** town1 (Town 1 fixes). **Files produced:** `town1.json` (plan) + this notes file.
**MCP note:** `robloxstudio-mcp` (`@Roblox_Studio`) was reported *failed to start / not configured* for this
session. It was not needed — this task only reads the build scripts and writes plan files; nothing touches
Studio. All work used the file tools and a local Python validator under `$KIROCREW_SCRATCH`.

Town 1 rectangle: **X -450..450, Z -560..345**, 20-stud inside margin. Gates: N (0,-560), E (450,-108),
W (-450,-108), S (0,345). Ground y ~1-3 in the flats, plateau top y≈18 at the skull site.

---

## How I reconstructed the town (from the Luau build scripts)

Read `b01_terrain.lua, b02v*_*.lua, b04_walls.lua, b05_plaza.lua, b06_residential.lua, b07_market.lua,
b08_landmarks.lua, b09_crafts.lua, b10_farm.lua, b11_magetower.lua, b12_nature.lua, b13_npcmarkers.lua,
b15_swapnature.lua, b16_north.lua, assets.lua, lib.lua`. Everything is under `workspace.SpawnTown`.

**Terrain / roads (b01, b16):** base grass; a river across the south at `z = 250 + 22*sin(x/90)`
(width ~34, water surface ~y-3). Main cobblestone **avenue** runs on x=0 from the south gate (z≈450) to the
plaza (z≈60), with a **bridge gap over the river (z≈228-272)**, then a north avenue (z -60..-150) up a ramp
to the skull plateau. **East road** z=0 x60..450 to the east gate; **west road** z=0 x-60..-450 to the west
gate. b16 extended the map north (wall to z=-760) and raised a big plateau (centre z≈-570, r≈165) with a
paved processional way and a forecourt at z≈-470 for the skull HQ.

**Folders / districts and reconstructed footprints (centre x,z — size w×d — front rot):**
- **Plaza** (0,0): fountain+statue (scaled 1.5×, basin r≈33), radial inlay out to r≈63, ring of benches
  (r≈54×1.5), planters (r≈61), lamps (r≈70), banner poles at the four road mouths. **Spawn** was a
  `SpawnLocation` at (0,18,63).
- **Residential** (west): houses line the x≈-150 spine (W side x-178, E side x-124, z -120..100), and the
  cross-streets z=-180 (x-200..-305), z=0 (x-200..-370), z=140 (x-205..-355), plus lane x-260. Sizes 16-28
  wide. **Pond** at (-300,-40) r≈30 with a dock and reeds.
- **Market** (east): shop row x≈124 (z±62) and x≈316 (z -72..78); **MarketHall** (222,-60, 48×28),
  **GrandEmporium** (222,66, 60×34 + arcade), **Warehouse** (372,-40, 46×28, faces -X). Two paved squares
  centred x≈222. Festival tents (TentL/TentR) flank the emporium.
- **Landmarks:** **Tavern** (110,-38, ~38×26 + wing + terrace), **GuildHall** (112,42, 40×30, enterable).
- **Crafts:** **Blacksmith** (380,64), **Chapel** (-205,-300, 26×52 + bell tower, a *second* church that
  already exists — left untouched), **TrainingYard** (centre 220,-290, ~104×72) full of AFK-pack tents,
  torches, flags, training dummies, targets and weapon racks (all Toolbox asset ids).
- **Farm** (SE, beyond the river): **Barn** (300,312), **Farmhouse** (180,304), **Windmill** (372,345),
  crop fields x166..334 z353..410.
- **MageTower** (-260,360): tower + arcane yard/garden. **This is actually north of the Z=345 border.**
- **SkullHQ6:** built by `b02v6_demonskull.lua` at **(0, G=18, Z0=-575)** — i.e. on the north plateau, on
  the map centreline, ~15 studs north of the town border. Its **mouth/jaw faces +Z (south)** toward the
  forecourt (NPC markers `HQGuard/Captain` sit at z≈-470..-490 facing +Z). So the HQ entrance already looks
  down the processional way toward the plaza — rot 0 keeps that.

**Toolbox / marketplace asset ids** (found via `_G.loadAsset / _G.tpl / _G.place / _G.kit` in `assets.lua`,
`b07_market.lua`, `b09_crafts.lua`, and the `L.tree/L.bush/L.flowers` overrides in `assets.lua`):
- Tree pack **79689531752352**; flower-bush **1353190583**; single-flower packs **16428845157, 743377736,
  711333951, 16071638063, 136744769027061** — these are what `L.tree/L.bush/L.flowers` place, and
  `b15_swapnature.lua` swapped every primitive Tree/Bush/Flowers across **all districts** for them (each
  tagged with the `Store` attribute). The whole **Nature** folder (b12) is built from them too.
- AFK pack **121230482146932** (tents/torches/flags in Market + TrainingYard).
- Training dummies **92960550414449, 10140126732, 11900295788**; weapon racks **131782675995926, 698770549**
  (TrainingYard).
- Medieval Interior Kit **2129051912** (Guild Hall interior) — interior furniture, **left in place**.

---

## The five fixes

### (1) Demon skull HQ — now the uploaded model `T01_demon_skull_hq`
- The old HQ was an `EditableMesh` built client-side; it vanished. Replaced by the uploaded model
  `T01_demon_skull_hq` (≈220×265×148 studs).
- **Placed at the SkullHQ6 site: `skull = {x:0, z:-575, rot:0, base_drop:75}`.** `rot 0` = front faces +Z
  (south) so the **jaw faces the plaza/main approach** (the processional forecourt at z≈-470), exactly where
  the old skull faced and where the HQ-guard NPC markers already point.
- **`base_drop:75`** — the model's origin is bottom-centre but its base currently sits **75 studs below the
  origin**. **Coordinator must drop the model 75 studs** so its base meets the plateau top (y≈18): place the
  origin at y ≈ 18 + 75 = **93**, i.e. `CFrame` y = plateau_top + base_drop, then anchor. (Equivalently:
  snap by bringing the base up 75 after a naive origin-on-ground placement.)
- **Jaw = the only entrance.** The mesh can no longer be edited, so the coordinator must **block every other
  opening (eye sockets, nose, any gaps) and the sides with invisible walls**, and leave only the mouth/jaw
  cavity open as the doorway. Add invisible `Part` barriers (CanCollide true, Transparency 1) across the eye
  recesses and around the base perimeter except the jaw arch on the +Z face. A forecourt (2 braziers, 2
  lamps, 2 flag poles) is planned on the plateau in front of the jaw (group `SkullHQ*`, placed on the
  existing HQ site north of the border by design).

### (2) Better grass + more props
- **Grass:** terrain `paint` ops swap the town-core open grass to **LeafyGrass** (lusher) over the plaza,
  the west and east quarters and the church area; the skull forecourt stays plain Grass. Roads/plaza paving
  are untouched (material-only paint, no height change).
- **Props (all from the catalog):** a flower/bush/bench/lamp **ring around the plaza** (r≈90, outside the
  existing fountain furniture at r≈70); **street lamps** along the main avenue (kerb at x≈±18, every 40
  studs, alternating sides, skipping the bridge gap), the north avenue, and the east/west roads (every 45
  studs, on whichever kerb is clear); **flower planters** (`A48`) along the avenues and at the market-square
  corners; and **70 edge-nature clusters** (smaller trees `A26/A31/A34/A28/A32/A25`, bushes `A38-A40`, rocks
  `A56/A58`, flowers `A43/A45/A46`, mushrooms `A54`) scattered in open grass toward the walls, thinning
  outward. Every placement keeps **≥4 studs** from reconstructed building footprints and off the roads/plaza
  core/river; when unsure a spot was skipped (that is why edge-nature is 70 of ~1600 tries).

### (3) Mage tower removed
- **Archive** `SpawnTown.MageTower` → move to **ServerStorage** (not deleted).
- Its spot is north of the border (-260,360, out of the rectangle), so the replacement **small garden
  square** is planned just inside the border at **(-250,315)**: a small fountain (`A109`), a ring of benches
  and planters, flower beds and three small oaks (`MageGarden` group). This keeps a tidy green square where
  the tower stood without crossing the Z=345 border.

### (4) New church = the new spawn
- Best catalog fit: **`D01_church`** (26.6×57.6, h 65.6) — a large, high-quality standalone church.
  `C16_cathedral` (50.8×79.5, h 92.3) was rejected: at the target spot it would collide with the residential
  blocks and the new garden, and it reads as a capital-scale cathedral rather than a town church.
- Target was ~(-260,340); that is right on the border and overlaps the mage-tower footprint, so the church
  is placed at the **nearest open ground that fits inside the town: (-300,300)**, `rot 90` so the **doors
  face +X (east)** up the open approach toward the town core (clear sightline). Footprint after rotation
  ≈57.6 (X) × 26.6 (Z); clear of residential (ends at z≈166 / x≈-370) and the Chapel (z≈-300).
- Church **square**: stone **steps** (`A08`) at the doors, **lamps** (`A15`) and **benches** (`A82`)
  flanking the entrance, **flower** beds (`A46`), a small **graveyard** south of it (`D16_stone_cross`,
  `D12`, `D14`) and framing trees. **`spawn = {x:-258.2, z:300, rot:270}`** — on the square directly in
  front of the doors, facing west into the church. (Coordinator: replace the plaza `TownSpawn`
  `SpawnLocation` with one at this point, snapped to ground, `rot 270`.)

### (5) Replace old Toolbox trees/props with catalog models
- **Archive (→ ServerStorage)**: the whole **`SpawnTown.Nature`** folder (Toolbox tree-pack scatter), and
  **every `Tree` / `Bush` / `Flowers` model in any district** (the `b15_swapnature` store-model output,
  pattern `SpawnTown.*/Tree|Bush|Flowers`). The catalog **`Edge_Nature`**, **`Plaza_Edge`**, avenue and
  church/garden nature placements above **replace them at the same open-grass spots** with catalog ids
  (A24-A70 range).
- **Archive the Toolbox dressing in the TrainingYard and Market**: AFK-pack tents/torches/flags, training
  dummies, targets, weapon racks, and the AFK crate (patterns under
  `SpawnTown.Crafts.TrainingYard.*` and `SpawnTown.Market.TentL/TentR`). These were decorative stand-ins;
  the contract bans Toolbox decoration. The coordinator can re-dress the training yard from the catalog
  (e.g. `A93_notice_board`, `A95_flag_pole`, `A21_brazier`, `A78_hay_bale`, `A74_crate_large`,
  `A99_anvil`) — listed here under **missing** because the catalog has no training-dummy/target/weapon-rack
  model, so those gameplay props must be rebuilt from parts or sourced later.

The `archive` key is a list of Studio instance paths **or `*` name patterns** to move to ServerStorage.
The Guild Hall interior (Medieval Interior Kit 2129051912) and the interiors generally are **kept**.

---

## Decisions & assumptions
- Skull kept at its real build site (0,-575) rather than the MAP_PLAN "Town 1" border, because that is where
  `SkullHQ6` and its forecourt/NPC markers already exist; moving it would strand the processional way, the
  guards and the ramp. It is only ~15 studs north of the Z=-560 line and the plateau is part of Town 1 in
  practice. Flagged in the validator as an allowed exception.
- Church + mage-garden pulled inside the Z=345 border (the literal targets were on/над the line).
- Lamps are intentionally at the carriageway kerb (they border roads by design), so they are checked for
  rectangle + gate + building/prop clearance but allowed next to the road band.
- Scales: nature 0.9-1.25, props 0.9-1.1, buildings 1 (per contract).

## missing (catalog lacks these — coordinator to rebuild from parts or source later)
- Training dummies / combat targets / archery targets (TrainingYard gameplay props).
- Filled weapon rack / weapon rack models.
- A dedicated mage-tower replacement monument if a plain garden is not desired.
- Invisible-wall / barrier parts for the skull (these are coordinator-built parts, not catalog models).

---

## Validation (run against `town1.json` + `catalog.json`)
Script: `$KIROCREW_SCRATCH/validate_town1.py`. Checks: unknown model ids; placements outside the Town 1
rectangle (−20 margin, skull exempted); gate-blocking within 12 studs of a gate; building-footprint overlaps
(>1 stud) for models taller than 6 studs; **and ≥4-stud clearance of every reconstructed existing building
footprint**; plus skull.base_drop and spawn sanity.

Final report:
```
=== Town 1 validation ===
placements: 128   unique models: 27
skull: {'x': 0, 'z': -575, 'rot': 0, 'base_drop': 75}
spawn: {'x': -258.2, 'z': 300, 'rot': 270}
archive entries: 15
terrain ops: 5
counts per model: (A15_lamp_iron_city 23, A82_bench_wood 7, A48_planter_box 6, A46_flowers_white 13,
  edge trees A25/A26/A28/A31/A32/A34, bushes A38-A40, rocks A56/A58, A54 mushrooms, A21 brazier ×2,
  A95 flag pole ×2, A08 stairs, D01_church ×1, D12/D14/D16 graveyard ×1 each, T01_demon_skull_hq ×1)
CLEAN: no problems found.
```
