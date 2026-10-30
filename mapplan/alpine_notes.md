# Alpine village — notes

**Area:** X 2150..2850, Z -850..-150 (700×700). Design ground ~Y 70, rolling 60–95.
West gate at (2150, -500, 70). Built strictly inside a 20-stud margin.
The NE tower mountain (keep-out, north of z -1050) is outside this rectangle; the
north edge is treated as higher snowy ground sloping up toward it, nothing built past z -830.

## The idea (plain words)
A cosy snowy mountain village sitting on a tilted highland shelf. The land is **low
green alpine meadow in the west/south (Y ~62–70, Grass / LeafyGrass)** and **snowy
high ground in the east/north (Y ~84–95, Snow / Glacier)** with bare **Rock outcrops**
on the southern lip.

A single **main street climbs west→east** from the west gate, rising from Y 70 to Y 86,
and ends at the **stone chapel (E06)** — the landmark closes the street on a raised snowy
pad (Y 88) so it is framed dead-ahead the moment you walk through the gate (sightline
requirement). Just before the chapel the street opens into the paved **village square**
(well, benches, cheese cart, fruit stall, signpost, brazier) with the **lodge (E05)** on
its north side.

A **stream** (terrain water, surface Y 66) runs north→south through the west-centre at
x≈2408. The **covered bridge (E11)** carries the main street over it; just south, on a
small **mill pond**, the **sawmill (E07)** turns its water wheel. Below that, on the
south-west meadow, sit the **barn (E08)** and **goat pen (E09)** with hay, a trough and
rail fences, a little apiary of three **beehives (E24)**, and a dirt path linking the farm
up to the street. A **watchtower (E10)** stands on a snowy rise in the NE (Y ~94) with a
brazier and snowy rocks, overlooking the village and the mountain foot.

**Chalets** sit on four flattened **terraces** either side of the street, each fronted by
**stacked-stone terrace walls (E20)**, facing the street (north row faces south, south row
faces north so fronts face each other across the street). Snow drifts, icicle clusters,
planter boxes, a sled and firewood dress their doorsteps.

**Nature** thickens toward the snowy east/north: groves of snowy pines (E12/E13/E14) with
snowy rocks (E15/E16) half-buried on the slopes and snowy bushes (E17). The low meadows
carry **edelweiss (E18)** and **gentian (E19)** scattered in drifts, tall grass, and a
couple of ordinary pines to the far west that thin out into the countryside. Rustic wooden
lamp posts (A17) light the whole main street, alternating sides ~40 studs apart, plus
lamps at the gate, chapel steps and lodge.

## Decisions I made (inside my area)
- **Street line** fixed at z = -500 (the gate's z), 24 studs wide, so it leaves the gate
  exactly at (2150,-500,70) and the 40-stud gate zone is clear and 24 wide. Road kit
  A01 tiles run x 2192→2664, fading (A05) into the square.
- **Terrain heights:** meadow 62–70, street 70→86, square 86, chapel pad 88, watchtower
  rise ~94. Stream water surface Y 66, depth 5 (sits just below the meadow so it reads as a
  carved channel + mill pond).
- **Orientation:** chapel faces west (rot 270) down the street; lodge faces south (rot 0)
  onto the square; covered bridge spans the E–W street so it is rotated 90 (long axis along X);
  sawmill rot 90 with its wheel toward the pond; chalets face the street.
- **Materials:** Snow/Glacier high east & north, Grass/LeafyGrass low west & south, Rock
  outcrops on the south lip, Cobblestone on street/square, Mud round the mill pond.
- **Scatter is collision-checked:** every tree/rock with height > 6 is placed only if its
  footprint keeps a ≥2-stud gap from every building and every earlier tree/rock, and never
  on the street corridor or in the stream band.

## Enterable buildings (2, per the performance rule)
1. **E05_lodge** — interior at ~(2680,-600), floor Y ≈ 85: table, two chairs, a stool,
   firewood stack, hanging lantern (group `LodgeInterior`).
2. **E06_stone_chapel** — interior at ~(2790,-500), floor Y ≈ 88: two wooden benches as
   pews and two candle clusters (group `ChapelInterior`).

All other buildings (chalets, sawmill, barn, goat pen, watchtower) are solid exterior-only.

## Missing (things the area wants that the catalog lacks)
- **Animals** — goats for the pen, which the model list already flags as NOT AVAILABLE
  (need rigging). The pen, trough and hay are placed and ready for them.
- **Snow-covered evergreen hedge / snowy log-pile wall** — only the plain `A41/A42` hedge
  and `E21` log fence exist; a snowy hedge would suit terrace edges. Used E17 snowy bushes
  and E20 terrace walls instead.
- **Frozen pond / ice surface prop** — handled with terrain `Ice`/`Glacier` paint if the
  coordinator wants a skating pond later; no dedicated model.
- **Church bell / cross for the chapel exterior** — exist only in the rusty-church kit (D2,
  D16), not shared; left to the chapel model's own roof spire (visible in the contact sheet).

Nothing was faked with plain parts or Toolbox models.

## Validation report (final, clean)
Checker: `catalog.json` + `alpine.json` → unknown ids, out-of-rect (20-stud margin),
building-footprint overlaps (height > 6, rotated AABB, > 1 stud), gate-blocking within
12 studs, counts per model. Wall/top-mounted placements (those with `y_offset`) and
interior-group placements are excluded from the overlap check (a lantern on a wall / a
candle on an altar is meant to overlap its host).

```
=== ALPINE VALIDATION ===
placements: 269   unique models: 62
problems: 0
```

All 26 alpine models (E01–E26) are used, plus shared road/lighting/nature/prop kit.
Key counts: chalets E01–E04 ×1 each, lodge/chapel/sawmill/barn/goat pen/watchtower/covered
bridge ×1 each; snowy pines 12+14+10, snowy rocks 11+6, snowy bush ×14, edelweiss ×22,
gentian ×22, terrace wall ×6, log fence ×12, beehive ×3, snow drift ×6, icicle ×4, sled ×1,
cheese cart ×1; road straights ×20; rustic lamps ×13.
