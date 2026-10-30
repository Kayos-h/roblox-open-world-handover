# Priority areas v5: natural entrances, capital, elf valley, Town 1

Your messages of 30 Oct: the elf valley is good but must look better; the plain arch at every entry goes and the place must feel natural; the capital and Town 1 must look better; think about each place from above and about the environment; follow the top-down concept map; roads must cross the mountains and rivers need Himalayan bridges; a giant enterable wizard tower stands on the Himalayan plateau; no decisions asked of you. The wizard tower comes first of all (`WIZARD_TOWER_BRIEF.md`), then these four areas, all P1 in Blender and first in Studio.

## 1. Natural entrances (only the plain arch goes)

Remove the plain arch that was placed at the entrances; other arches and gates stay when they are a real design. From the placement plans the plain arch family is: `H12_region_entrance_arch` (5 in the country plan), `A104_wooden_gate` (4), `D04_06_gate_arch_a` and `D04_07_gate_arch_b` at the elf valley (-1300,-406) and (-1885,-437), and `F08_13` / `F08_14` gate arches if any are live. A Studio scan lists what is really in the map. These stay: the capital's grand gates and gatehouses (rebuilt as part of the ring wall), the royal-garden rose arches, ruined arches deep in the forest, natural root and rock arches, graveyard gates, bridge arches. Alpine, harbour, rusty and Town 1 never had a gate.

How a settlement is entered instead:
- The road narrows or widens, bends once, and is framed by two large trees, a boulder pair (NE02), a hedge or a fence.
- One carved village sign (NE01) on a post or stone, in the settlement's own style and palette.
- A few details that belong there: stepping stones and ferns (elf), a trough and a signpost (Town 1), a log fence with snow (alpine), mooring posts and a lighthouse in view (harbour), clay jars (desert).
- The capital keeps its gatehouses because a wall needs a gate. They are built into the ring wall (CP07, CP06 flank towers, CP08 water gate) and replace C04, K08 and B02_07 as part of the capital rebuild, not because they are arches.
- Ruined arches stay as ruins deep in the forest; natural root and rock arches stay.

NE01 village_sign x6 (6k triangles each): Town 1 (stone slab, carved jaw motif, iron bracket), elf valley (living-wood board on a root post), alpine (log post with a snow cap and a small bell), rusty (salvage plate on sandstone), harbour (whitewashed board with an anchor and rope), desert village (painted clay slab on a beam). The west village reuses the rusty set.
NE02 entry_rock_pair x4: mossy, frosted, sandstone and basalt boulder pairs, 30 x 14 x 22 studs, 5k triangles each.

## 2. Capital (reference: the castle-town picture)

Layout recipe (all numbers inside the existing pad):
- Ring wall: ellipse centre (0,-1585), rx 490, rz 350, 12 corner towers (alternate CP04 large and medium), about 68 straight segments of 40 studs (CP01 in 3 variants), foreground turrets (CP05) on every second tower.
- Gates in the wall: south (0,-1237) CP07 plus two CP06 flank towers; north gate (0,-1918) with the grand stair (CP13) up to the plateau; water gate CP08 where the river leaves at the south-west, about (-330,-1260).
- Plateau (y 92, castle pad at (0,-2200)): keep CP09 with wings CP10, retaining walls CP12, great hall and chapel CP11.
- Plaza (0,-1560), 130 x 100, monument CP17. Order HQ CP15 east of the plaza (190,-1570). Skyline towers CP14: clock (0,-1700), bell (250,-1750), observatory (-260,-1740), beacon (440,-1585), water tower (-300,-1400).
- Districts: nobles north-west, merchants east, crafts west, homes south. 12 new townhouse types CP16 break the repetition.
- From above: grey-lilac ellipse, one orange-red roof mass, a lighter plaza, grey plateau and keep behind, a blue river loop with 3 bridges.
- Palette: plaster (232,214,188) and timber (112,80,60); roofs orange-red (198,88,52), (214,104,58), (178,72,46), accents (140,62,48); stone grey-lilac (150,142,158); cone roofs maroon (120,44,52); wall-walk deck (150,88,70); parapet cap (232,226,230).

Key briefs:
- CP09 keep (130 x 120 x 110): stepped massing with a central tower, 4 corner and 4 mid turrets with cone roofs, buttresses, arched windows, balconies, portcullis gate at the base. Must not look like B02_01.
- CP07 gatehouse (60 x 56 x 40): built into the wall, deep arch with portcullis, two machicolated bays, banner mounts, crenellated top, walkable passage.
- CP01 ring wall: 8-stud wall-walk with a red-brown deck, white-capped inner parapet, crenellated outer edge, slit windows in variant b, buttresses in variant c.
- CP04 towers: 16, 22, 28 and 34 studs wide; slit windows, a string course, maroon cone roof with a small finial.
- CP15 order HQ (90 x 60 x 70): wide hall with two wings and a banner tower; own name, own heraldry, no Black Clover shapes.

## 3. Elf valley: what makes it look better

From above it should read as a dark-green canopy bowl with a lighter giant-tree crown, houses tucked under the canopy, a waterfall at the west rim and a lake with a soft outline. Ranked, with the non-model work in Studio:
1. Structure: a moon-pool plaza with a main spoke path from the tree to the east side; a second ring of houses at 230-320 studs (EV01, 8 new types); 3 canopy clusters (EV02) at 90-140 studs up around the trunk, each with ladders to the ground.
2. Waterfall: parts version now (3-4 ribbons over 24-30 studs, 2-3 ledges with foam shelves, mist slab, stream to the lake, moss and ferns on the cliff); the colossal cliff hero (LM22) replaces it later at the west rim (-1800,-672).
3. Ground: dapple patches of 30-60 studs with higher contrast, base (86,142,70), light (120,170,96), dark (64,108,56), warm scuffs near paths, path-edge wear.
4. Tree: rounded buttress roots (RW02), trunk door and stair (LM01), 3-tier falls (LM02).
5. Entrances: the two arches are removed; the east and west paths simply enter the forest between large trees, with the elf sign (NE01) and stepping stones.
6. Forest layer: giant trees (FR01 x4), overgrown ruins (FR02 x6), cave mouths (FR03 x6), ferns and moss along paths.
7. Cleanups: the translucent slab near (-1500,65,-370), the orb, the tuft at the trunk base.
8. Light stays warm lantern only. No glow anywhere in the valley.

EV01 house types (22-40 studs, 14k triangles each, wood and stone, lantern hooks, no glow): tower house (stacked round rooms, outside spiral stair), bridge house (built across a stream), library (woven-branch dome, arched windows), healer hut (herb racks), archery lodge (open hall, target lane), bathhouse (stone pool, wooden screens), council hall (round, ring of carved posts), weavers hall (loft, hanging natural-dyed cloth).
EV02 clusters: ring village (4 platforms, 4 rope bridges, 2 huts, 2 ladders), branch hall (long platform with a hall), nest cluster (small round huts in the canopy).
RW02 roots: 8-10 rounded buttress roots, soft taper, bright bark, moss patches.

## 4. Town 1: what makes it look better

From above: a compact dark cluster with the skull HQ at the north end of an avenue to the plaza, kitchen gardens and hedged fields around it, a river on each side, low hills at the edges.
1. Paint a Ground ring where tall grass clips the house footing; find and remove the pale orb.
2. Finish or trim the dirt trail that ends abruptly; add the missing path from the skull apron to the plaza, with an avenue set (TW03 x4: braziers and banner poles).
3. Hero statue with a real face (TW01): founder figure, 14 x 40 x 14, brow, nose, cloak folds, plinth with an inscription band.
4. Street life (TW02 x8): carts, crate and barrel stacks, hanging smith and tavern signs, a bench.
5. Natural entrance: the road widens into the avenue between hedges, with the Town 1 sign (NE01) and low stone markers. No gate.
6. Hills and trees at the edges outside the protected zone (x +-318, z -545..311) to break the carpet. Inside the zone changes are additive only and named town1_*.

## 5. Order of work in Studio (after Blender)

Terrain pass, arch removal and natural entrances, capital rebuild, elf valley, Town 1, then the landmark heroes, the Skull City, the desert, roads and storytelling, then the rest.
