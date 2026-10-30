# Royal Capital + Castle — plan notes

**Area:** `capital` | **Rectangle:** X -800..800, Z -3300..-1700 (biggest area on the map).
**Design heights:** gate Y20 at the south, rising in terraces to the castle keep at ~Y150 at the north.
**Deliverable plan:** `C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\capital.json`
**Placements:** 490 | **Terrain ops:** 19 | **Unique models:** 119.

## The idea in plain words
The Wizard King's royal capital sits on a plateau. You enter through the **grand gate (C04)** at
the fixed south gate point (0, -1700). A single **grand avenue runs dead-straight north up the
centre**, climbing the hill in five terraces, and the **castle keep is visible straight up that
avenue from the gate** (everything on the X=0 axis is low or framing, nothing blocks the view).

Walking north you pass, in order:
1. **Outer city wall** (C01 straight / C02 corners / C03 towers) ringing the whole plateau foot,
   with the grand gate flanked by two towers and braziers.
2. **Common district** — four capital townhouse types (C05–C08) and terrace rows (C10) lining the
   avenue and a back side-street, fronts facing the street, mirrored across it, window flower
   boxes (C25), bunting (C31) strung overhead, a neighbourhood well/trough/laundry cluster, and
   oaks softening the back yards. An ornate street archway (C24) marks the way into the market.
3. **Grand market** — a paved plaza (C30) with the **plaza fountain (C21)** on axis, the
   **knight statue (C22)** in front of it, the **market hall (C11)** on the west and the
   **clock tower (C15)** landmark on the east, with bakery (C12), potion shop (C13) and magic
   tool shop (C14) around the edges, vendor carts (C26), market stalls (A105–A107), awning,
   crates/barrels/sacks in story clusters, benches facing the fountain, planters and double-arm
   lamps (A16).
4. **Canal** — an east-west water channel crossing the city, with canal walls on both banks
   (C27), the avenue **canal bridge (C28)** plus two side bridges, canal stairs down to the water
   (C29), reeds and lily pads.
5. **Noble district** — the two biggest civic landmarks flank the avenue: the **cathedral (C16,
   enterable)** on the west and the **magic academy (C20)** on the east, with the knights HQ
   (C17), guild hall (C18) and royal library (C19) further in, plus three noble mansions
   (K37–K39). An **obelisk (C23)** stands on the avenue axis. Two **formal gardens** (gazebo K30,
   topiary K25–K27, rose arches K31, ornate planters/benches/lamps, willows) sit east and west,
   with a **maze hedge** (K28/K29) in a corner. Royal banners (K35) and flag poles mark the
   civic doorways. A second archway marks the climb to the castle.
6. **Castle (top terrace, ~Y150)** — a **moat** with the **moat bridge (K10)** and **drawbridge
   (K09)** leading into the **gatehouse (K08)**, flanked by round towers (K02) and sentry boxes
   (K42). **Curtain walls (K05) with corner bastions (K06), wall stairs (K07), square towers
   (K03) and spire towers (K04)** enclose the bailey. At the high north centre stands the
   **main keep (K01, enterable)** reached by the **grand staircase (K18)**, braziers at its foot,
   tower flags (K36) flying. The courtyard holds the **royal fountain (K23)**, the **Wizard King
   statue (K24)** on axis (seen straight up the avenue), monument columns (K44), topiary, rose
   arches, a royal carriage (K43), and **barracks (K40)** + **stables (K41)** in the side baileys
   with hay, troughs, firewood and crates.

Nature thins toward the walls and edges (mixed oaks/pines/maples, bushes, flowers, rocks) so the
dense centre blends into countryside at the border.

## Enterable buildings (2, per the performance rule)
- **K01 main keep** — contains the **throne room** interior (group `KeepInterior`, inside the
  keep footprint centred at (0, -3110)): red carpet runner (K14) from the south entrance to the
  **throne (K11)** at the north end, flanking throne pillars (K12) and a colonnade down the hall,
  two chandeliers (K13) overhead, stained windows (K15) on the side walls, two tapestries
  (K16/K17) behind the throne, and a study corner — royal desk (K19), two bookshelves (K20),
  magic orb (K21) and candelabra (K22).
- **C16 cathedral** — the second enterable building (group `CathedralInterior`, inside the
  cathedral footprint at (-150, -2680)): candle clusters (A23) at the altar end and braziers
  toward the entrance. (The catalog has no cathedral-specific pews/altar/organ — those models
  live only in the `rusty` church kit, D05–D08, which belong to another area; see *missing*.)

## Key decisions (made here, as the contract allows)
- **Gate & walls kept inside the rectangle.** The fixed gate point is (0, -1700) on the border;
  the margin rule needs placements inside z ≥ -1720. The south wall line and gate are set at
  z = -1722 and the north wall at z = -3238, so the whole ring sits inside the 20-stud margin
  while the gate still reads as "at the south gate". The avenue runs from z -1722 up to the keep.
- **Avenue corridor** is kept clear (nothing within 12 studs of the gate point, and the central
  X=0 corridor carries only on-axis framing: archways, fountain+statue, bridges, obelisk,
  gatehouse, keep). This guarantees the castle sightline.
- **Terraces built with terrain ops**, not a flat grid: one big `plateau`, a castle `hill`,
  six `flatten` shelves at Y 24/42/62/76/104/150 south→north, and five avenue `ramp`s linking
  them. A `water` op makes the canal and another the castle moat. `paint` adds LeafyGrass to the
  gardens and castle mound.
- **Wall overlaps avoided by reserving slots**: tower positions are skipped in the straight-wall
  loops (city E/W walls and castle curtain walls), gate flank towers sit outside the gate
  footprint, and the city north wall skips the short stretch directly behind the castle (the
  castle's own rear curtain wall closes it and it is hidden behind the keep).
- **Facing convention** followed: rot 0 = +Z (south). Houses on the west side face east (rot 90),
  east side face west (rot 270), both fronting the avenue; the gate faces south toward the
  incoming road; the keep and gatehouse face south down the avenue; the Wizard King statue faces
  south (rot 180) so its face is seen coming up the avenue.
- **Interiors excluded from the building-overlap check** on purpose (they sit inside their keep /
  cathedral footprint), and so are wall-mounted / stacked items carrying a `y_offset` (flower
  boxes, bunting, tapestries, chandeliers, tower flags).
- **Density:** ~490 placements, dense at the avenue/market/castle, thinning to scattered trees,
  flowers and rocks at the edges. Avenue lit with city lamps (A15) alternating every ~42 studs,
  double-arm lamps (A16) in the market, ornate lamps (K34) in the noble district and courtyard.

## Missing (things this area really wants that the catalog lacks)
- **Cathedral interior furniture** — there is no capital-specific pew / altar / pulpit / organ.
  Those exist only as `rusty`-church models (D05 pew, D06 altar, D07 pulpit, D08 pipe organ,
  D09 candle stand, D10 pillar). If the coordinator is willing to borrow them cross-area, the
  cathedral interior could be furnished with D05/D06/D07/D08; otherwise it stays a lit shell with
  candle clusters and braziers. **Not faked.**
- **Portcullis / closed gate leaf** as a separate model — C04 and K08 include their own gate
  detail, so this is optional, not blocking.
- **Hanging/standing banners sized for the keep's great hall** beyond K16/K17 — adequate as is.

Everything placed uses only catalog ids; no Toolbox, no plain parts, no stand-ins.

## Validation (run from `$KIROCREW_SCRATCH\capital\validate_capital.py` against capital.json + catalog.json)

```
=== VALIDATION REPORT ===
placements: 490  terrain ops: 19  unique models: 119
problems: 0
```

Checks performed and all passing:
- **Unknown model ids:** none (all 119 ids exist in catalog.json).
- **Outside rectangle (minus 20 margin):** none — every placement is within X -780..780, Z -3280..-1720.
- **Overlapping building footprints** (rotated rectangles, >1 stud, for structures taller than
  6 studs — city walls/towers/gate, townhouses, shops, civic buildings, castle walls/towers/
  gatehouse/keep, mansions, barracks, stables): none. Interior props and `y_offset` stacked items
  are excluded by design.
- **Gate corridor:** nothing within 12 studs of the gate point except C04; the 24-wide avenue is
  kept clear for 40 studs north of the gate.
- **Counts per model:** recorded in `report.txt` (e.g. C01 city wall ×~120, C05–C08 townhouses
  ×5 each, C10 terrace ×6, A15 lamps ×13, K05 curtain wall ×14, plus the single landmark models).

Iteration history: first run flagged 55 issues (south wall sitting on the -1720 margin; walls
overlapping their towers/corners; castle curtain walls overlapping flank towers, corner bastions
and wall stairs). Each was fixed by moving the wall lines inside the margin and reserving tower/
corner/stair slots in the straight-wall loops; the final run reports **0 problems**.
