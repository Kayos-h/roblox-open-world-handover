# Roads + Countryside — plan notes (`roads` agent)

Covers the whole 7000×7000 map **outside every area rectangle** and outside the
NE mountain keep-out (X 1700..3300, Z −2700..−1050). Deliverables:
`roads.json` + this file. Terrain ops are applied before the area agents' own
ops, so this is a sensible **base** that meets every gate height smoothly.

## 1. Base terrain (79 ops total — well under the ~150 cap)

A few large ops shape the whole map rather than thousands of tiny ones:

- **Central plains** around Town 1 — one big `plateau` at (0,−108), top_y 2,
  rolling gently (slope 300).
- **North → capital plateau** — large `plateau` at (0,−2500) top_y 22, with a
  wide `ramp` grading the plains up from y4 at z−1150 to **y20 at the capital S
  gate** (0,−1700). Meets the capital gate height exactly.
- **East → alpine highland** — stepped plateaus (y40 then **y70**) plus two Rock
  hills, reaching **70 at the alpine W gate** (2150,−500). Snowy paint on the
  approach.
- **West → elf forest floor** — `plateau` at (−1600,−500) top_y **10** painted
  `LeafyGrass`, matching the elf E gate (−1950,−600,10).
- **South-east → rusty** — dry `Ground` plateau at (1700,1500) top_y **14**,
  matching the rusty NW gate.
- **South → harbour & sea** — plateau at (−600,1800) top_y 8, a `ramp` down to
  the shore, a big `Sand` paint, and a single large **sea** `water` op (y0)
  spanning the south edge south of z≈3050.
- **River** — a polyline of `water` ops (y1, depth 7, ~55 wide) from the NW
  hills (−1700,−1200) down to the south coast (−430,3050). It **crosses the W→elf
  road, the S→harbour road and ring roads** — 6 bridges were auto-placed where
  roads meet it.
- **Lake** — a scenic `water` op (y1) at ~(850,535) in the east-central meadow,
  ringed with `Mud` paint, reeds and lily pads.
- **Natural border** — beyond ~3200 from centre, 13 big Rock `hill` ops ring the
  map (mountains/forest) on every edge except the south, which fades to sea.

Materials used are all valid terrain enums (Grass, LeafyGrass, Ground, Mud,
Sand, Rock, Snow, Cobblestone).

## 2. Main roads (graded with `ramp` ops, 20 wide)

Every road begins and ends **exactly on its gate point at the gate height**
(verified — 9/9 gates have a road ramp endpoint). Road surface is **Cobblestone
near towns** (within ~650 of any gate) and **Ground (dirt)** in open country.

- **N**: Town1 N (0,−560,2) → capital S (0,−1700,20) — straight royal approach.
- **E**: Town1 E (450,−108,2) → alpine W (2150,−500,70) — climbs the highland and
  **routes south of the keep-out** (the gate sits just below it).
- **W**: Town1 W (−450,−108,2) → elf E (−1950,−600,10) — through the forest floor.
- **S**: Town1 S (0,345,2) → harbour N (−600,2300,8) — down to the coast.
- **SE**: branches from Town1 E gate → rusty NW (1600,1500,14).
- **Ring road**: a full loop linking neighbouring areas —
  capital↔alpine↔rusty↔harbour↔elf↔capital — five gate-to-gate arcs routed
  through countryside and around the keep-out.

Along the roads: **milestones** (A14) every ~500 studs, **signposts** (A13) at
the five Town-1 junctions, **stone arch bridges** (A12) at every river crossing,
**rustic lamps** (A17) only near towns (alternating sides), and a light sprinkle
of roadside bushes.

## 3. Countryside

- **Region entrance arches** (H12) ~150 studs before each of the 5 area gates,
  facing the gate.
- **Farms near Town 1** — two belts (east and south of the rectangle) of wheat
  (H07) and vegetable (H08) crop rows, scarecrows (H09), hay bales, rail fences.
- **Landmarks (H models)** placed at scenic road-adjacent spots: 2 roadside
  shrines, 2 abandoned watchtowers, ancient ruins (H03/H04), 2 traveller
  campsites (with campfires), 2 wagon wrecks, a working windmill near the farm
  belt, a standing stone circle in the south-west meadow.
- **Forests** — 9 big natural clusters with mixed species, rot and scale
  (0.85–1.25): temperate oak/birch/maple/fruit toward the elf west and around
  the plains; snowy + normal pines on the eastern highland; dead/dry trees in
  the SE. ~700 trees total, none on roads or in the river, footprints
  non-overlapping.
- **Rocks / boulders / cliffs** on the highland slopes and along the map
  borders.
- **Flowers & tall grass** in four meadows (dense), plus reeds and lily pads
  around the lake.

Density is high near roads and points of interest and thins toward the edges,
blending into the natural border.

## Decisions I made (inside my area, per contract)
- **Road width 20** (contract range 18–22), graded entirely with `ramp`/`flatten`
  + `A01`-style surfaces are left to the coordinator's snapping; I supply the
  graded bed and the kit markers (bridges, signposts, milestones, lamps).
- The **SE road shares the Town-1 E gate** as its start, since the contract's
  five roads come from only four gates; the E gate therefore forks to alpine and
  to rusty.
- River kept at **y1 (depth 7)** rather than y0 so it reads as a river above sea
  level and the arch bridges sit correctly.
- All placements keep a **30-stud pad** outside every area rectangle and the
  keep-out (the validator confirms zero intrusions).

## Missing (catalog lacks, per contract — not faked)
- **Nothing blocking** this area. Optional nice-to-haves the catalog does not
  have: a dedicated dirt/gravel *road* surface mesh (I use `A06` dirt path + the
  Ground/Mud terrain paint instead), and a *river-ford* piece (handled by the
  stone arch bridge A12). Animals, NPCs, skybox and sounds are already listed as
  out-of-scope in `MAP_MODEL_LIST.md`.

## Validation (run in scratch, final report — CLEAN)

```
[info] water ops: 9, bridges: 6
=== ROADS.JSON VALIDATION REPORT ===
terrain ops: 79
placements: 1334
distinct models: 57
overlapping tall pairs: 0
gate ramp endpoints present: 9/9

NO PROBLEMS FOUND. CLEAN.
```

Checks performed and passing:
- no unknown model ids (all 57 are in `catalog.json`);
- **0 placements inside any area rectangle**;
- **0 placements inside the NE keep-out**;
- 0 placements outside the 7000×7000 bounds;
- terrain op count 79 ≤ 150; all terrain materials valid;
- **every road begins & ends exactly on its gate** (9/9 gate ramp endpoints);
- nothing taller than 6 studs within 12 studs of a gate (streets kept clear);
- **0 overlapping tall-model footprints** (>1 stud), rotation-aware;
- river crosses multiple roads with 6 bridges placed at the crossings.
