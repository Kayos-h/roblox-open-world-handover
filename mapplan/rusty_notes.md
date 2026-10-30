# Rusty town + church — plan notes

**Area:** rusty · **Rectangle:** X 1600..2200, Z 1400..2000 (20-stud margin kept) · **Design ground Y:** 14 (dry, cracked) · **Road gate:** NW (1600, 1500, y 14).

## The idea in plain words
A poor, weather-beaten town in the dry south-east corner whose single treasure is a
beautiful old sandstone church. You enter at the **NW gate (1600,1500)**. A **crooked
main street** dog-legs away from the gate: it runs east along z≈1500 past the first,
saddest run-down houses, then bends south-east, lined on both sides with broken homes,
a collapsed ruin, boarded shacks and a tavern, until it opens onto a small **church
square** at ≈(2030,1790). The **church (D01)** stands at the end of the street as the
landmark — tallest thing in the area at 65.6 studs, its bell tower and rose window
visible straight up the street from the gate. The **graveyard** sits just east of the
church behind a broken iron/stone fence. The town is deliberately sad and weathered
around the street (dead trees, scrap, patched tents, rusted carts, a broken windmill on
a knoll, a leaning water tower) but the ground is cleaner and warm greenery (fruit tree,
oak, flowers, planters, benches) gathers only at the church — the one cared-for place.

### Districts / groups
- **MainStreet / ChurchSquare** — road-kit cobble tiles (A01/A02/A04), crooked from gate to square.
- **NorthRow / SouthRow** — run-down houses flanking the gate stretch, fronts to the street.
- **StreetEast / StreetWest** — houses down the diagonal, fronts to the street line.
- **Church / ChurchInterior / ChurchGarden** — the landmark, its fit-out, its warm garden.
- **Graveyard** — gravestones, cross, mausoleum, weeping statue, broken fence, gate.
- **Tavern / TavernInterior** — second enterable building off the diagonal.
- **Blacksmith, Windmill, WaterTower, TownCentre** — the town's working/industry bits.
- **Shanty / StreetClutter / DeadNature / Lighting** — poor clutter, dead nature, crooked lamps.

### Landmark sightline
The church is placed on the street's axis at the SE end (centre 2055,1870, **rot 180** so its
**door and rose window face back up the street, toward the gate**). Walking in from the NW
gate you look straight down the crooked street to the lit church front.

## Enterable buildings (2, per the performance rule)
1. **D01_church** (centre 2055,1870, rot 180). Interior laid inside the footprint
   (x 2055±13.3, z 1870±28.8): **altar** at the south end (2055,1894) facing the
   congregation, **pulpit** beside it, **pipe organ** against the west wall near the altar,
   **two columns of pews** (6 rows) down the nave facing the altar, **six interior pillars**
   in two rows, **two candle stands** + a candle cluster flanking the altar.
2. **D25_rundown_tavern** (centre 1912,1600, rot 270, front faces the street). Interior:
   two tables with chairs/stools, barrels, a candle cluster and a hanging lantern; exterior
   has barrels, a broken barrel, a wall lantern and a shop sign.

## Church fixtures (mounted on the shell — intentional "overlap" with D01)
- **D02_church_bell** on the tower (y_offset 44).
- **D03_church_rose_window** + **D11_church_door** on the front (north) facade.
- **D04_church_tall_window** ×6 — three per long (E/W) wall, y_offset 12, facing out.
- **A20_wall_torch** ×2 flanking the door for warm light.
These are the only deliberate overlaps with the church; the validator whitelists facade
fixtures, interior items and anything with a y_offset (wall/roof-mounted) and still reports
**zero** unintended building overlaps.

## Terrain
Base **plateau** at Y14 over the area, painted patchy with **Mud / Sandstone / Ground** dry
earth and two patches of dead **LeafyGrass**. A shallow **dry gully** (Sandstone, dipping to
Y10) runs roughly N→S through the east side. A **hill/knoll** (Y+22) in the NE carries the
broken windmill. The **church square** is a flattened Sandstone pad with a ring of LeafyGrass
(the kept, greener ground). A small Cobblestone pad flattens the gate mouth so the street
meets the gate clean and 24 studs wide.

## Gate handling
The street is kept clear and 24 wide at the NW gate: the first road tile centres at
(1632,1500) so its west edge sits on the x=1620 margin, and no model taller than 2 studs is
within 12 studs of the gate point (a brazier sits just off to light it). The road agent
takes the street out from (1600,1500,14).

## Decisions I made (not specified by the contract)
- Crooked street modelled as a dog-leg of A01 straights with A02 curves at the two bends
  (the catalog has no diagonal road tile; the coordinator paints/blends the ground beneath).
- Church faces **north (rot 180)** up the street rather than toward +Z, because the street
  approaches from the NW — this gives the door/rose-window the sightline.
- Graveyard placed **east** of the church (open ground there) rather than south (map edge).
- Warm greenery deliberately confined to the ChurchGarden group; everything else is dead/dry.
- Windmill on the NE knoll for the "broken windmill on a rise" beat.
- Non-cardinal rotations used only for nature, tents, carts and the diagonal houses; all
  checked with a rotated-rectangle (SAT) overlap test.

## Missing (things the area wants that the catalog lacks)
- **Diagonal / angled road tile** — the crooked street is approximated with straight tiles
  stepped SE; a true diagonal cobble piece would read cleaner. Coordinator can paint the
  ground between tiles to hide steps.
- **Rubble / debris ground scatter** (loose bricks, broken roof tiles) to dress the
  collapsed ruin and collapsed wall — only whole-prop pieces exist (D30 scrap pile, D32
  broken barrel used as stand-ins near the ruins).
- **Dry/dead bush** variant — used A38/A40 green bushes sparingly; a browned version would
  suit the scorched theme better.
Nothing was faked with plain parts; every placement is a catalog id.

## Validation results (final, clean)
Generator + validator: `gen_rusty.py`; rigorous overlap re-check: `sat_check.py`.

```
placements: 187   terrain ops: 13
ERRORS: 0
WARNINGS: 0
D-models NOT placed: []            # all of D01..D37 present
SAT building overlaps: 0  (59 tall buildings checked, arbitrary angles)
```

Checks performed and passed:
- **Unknown model ids:** none — every id is in catalog.json.
- **Out of rectangle (minus 20 margin):** none — footprint extents (rotated) all inside
  X 1620..2180, Z 1420..1980.
- **Overlapping building footprints (>6 tall, >1 stud):** none, confirmed by both an
  axis-aligned pass and a rotated-rectangle SAT pass; deliberate church-shell fixtures and
  interior items are whitelisted.
- **Within 12 studs of the gate blocking the street:** none (nearest tall object is clear;
  only a gate brazier for light).

### Model counts (187 placements)
All 37 rusty models (D01–D37) are used. Shared-kit support: roads A01/A02/A04; lighting
A18/A19/A20/A21/A23; nature A24/A34/A35/A36/A38/A39/A40/A43/A44/A46/A47/A48/A50/A52/A55/
A56/A57/A58/A59/A68/A69/A70; props A71/A72/A77/A79/A80/A82/A84/A85/A86/A90/A92/A94/A98/A99.
Full per-model tally is in the generator's printed report above.
