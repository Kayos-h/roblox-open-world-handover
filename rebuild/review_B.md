# Visual Review B — Phase 1 Map

Reviewer B. 13 assigned shots (r09–r15 partial, s11, s12, s15–s18). Unavailable MCP server this session: **@Roblox_Studio** (not configured). Review done read-only from JPGs; no Studio access.

## Per-picture

| Shot | Score | What I literally see | Defects |
|---|---|---|---|
| **r09_elf_air** | 7/10 | Elf valley from NE air. Giant world tree center, sprawling jungle, four grey mountain ridges framing it, two blue lakes (one by a white domed building bottom-left, one mid-right), sandy glowing paths radiating out, a bridge/arch over a stream mid-right, domed temple right, sea beyond. Dense, readable, atmospheric. | Trees fairly repetitive/sparse in gaps; paths very bright white (overblown); no visible rope bridges between treehouses; canopy not truly "dense" — lots of open grass. |
| **r10_elf_path** | 6/10 | Ground path leading to world tree. Flanked by two white crowned-figure statues on plinths, mushrooms (red/purple), a dark stone arch, glowing green crystals hanging in trees, grass tufts. Stylised and pretty. | Crystals in trees look like flat decals/sprites, slightly garish. Right-side "Right" nav cube overlay visible (harmless, Studio UI). Statues float slightly above plinth tops. Path again blown-out white. Very bright, washed highlights. |
| **r11_harbour** | 8/10 | Harbour from air. Two sailing ships at two wooden piers, small rowboats/buoys, dense blue/red/grey half-timbered houses on green hill, a ruined stone fort on a headland, anchor + lamp props foreground. Ships sit correctly at waterline. Looks good. | A tiny boat mid-water appears to float just above surface (center). Houses densely packed, slightly uniform. Sea is flat and very cyan. Foreground houses clip the grass edge sharply (hard terrain seam). |
| **r12_rusty** | 7/10 | Rusty town overview. Large stone church with pink spire + rose window, cluster of small clay/rust-roof huts around it, dead bare trees, scattered rubble/props, sand ground, sea behind. Convincingly rundown. | Ground is uniform flat sand — no relief, no graveyard clearly visible from here. Some huts repeat identically. Terrain abruptly meets sea with no beach. |
| **r13_rusty_huts** | 5/10 | Close view of rusty huts + church base. Huts have rust metal roofs, open doorways, some are **roofless/hollow shells** (front-left hut has no roof, you see straight into empty interior). Dead trees, lamps. | **Major:** several huts are open-topped empty boxes — no interior, no roof — looks unfinished. Church windows show bright green glow (odd placeholder). Hut textures stretched. No floors inside. |
| **r14_country** | 5/10 | Countryside from castle turret. Vast flat green field, grey snow-capped mountains left, scattered trees + a line of trees along a road right, a lake right, a wood watchtower left, two blue castle turret tops foreground. | **Floating rock slabs in sky** (two grey slabs hovering mid-left and above mountains). Terrain extremely flat and empty — huge bland green expanse, no farms visible, no biome variety. Trees sparse. |
| **r15_overview** | 6/10 | Whole-island top-down. Roughly round island, green with darker mountain patches, several round lakes/ponds, grid-plan town top (capital), central palace complex, large dark-water bay bottom-right with a structure, scattered settlements. Island reads as one landmass with relief. | Heavy blue atmospheric haze/fog washes everything pale — hard to read detail. Relief is modest; mountains read as flat dark blotches not peaks. Bottom-right bay water very dark vs cyan sea elsewhere (inconsistent). |
| **s11_elf_tree_close** | 7/10 | Base of world tree — big buttressed wooden trunk, root flares. Behind: white domed temple left, jungle, two mountain ridges, mushrooms, arch, grass. | White paper/scroll props clipping into ground at trunk base (2 stray white sheets, bottom-left & bottom-center). Trunk texture uniform. Yellow sign decal on trunk looks misplaced. |
| **s12_elf_house** | 7/10 | Round pink elf house, green conical roof, red trim, windows, white tulip flowers front, jungle + mountain behind, treehouse right, glowing arch left. Charming, on-brief for round elf house. | House sits on pinkish bare dirt patch — terrain recolour blotch (pink sand under green grass, looks accidental). Flowers float just above ground. Roof peak orb prop. |
| **s15_harbour_quay** | 6/10 | Quay path along sea: cob?/dirt road, lit lamp post, stone-walled tavern right (lit windows), cranes/market stall left, ruined fort on headland ahead, ships left. | **Grass overgrown/oversized** — huge grass blades dominate foreground, blocking the quay view (grass too tall for a paved harbour quay). Path reads dirt not stone quay. |
| **s16_harbour_sea** | 3/10 | Almost entirely enormous bright-green grass blades filling frame; a round stone tower (fort, with cross-slit window) upper-left, sky. | **Severe:** foreground grass is absurdly tall/dense — unplayable view, obscures the sea the shot was meant to show. Grass decoration height badly mis-scaled here. Effectively unusable as a scenic view. |
| **s17_rusty_street** | 6/10 | Rusty main street at ground level. Clay houses rust roofs, open doorways, a wooden cart, anvil + barrel (smithy), lamp post, cactus/aloe plant, bare trees, flat sand. | Flat featureless sand street, no cobbles/ruts. A house mid-right appears to **float** (gap under it / shadow offset). Cart wheels sink slightly. Sparse — large empty sand gaps. |
| **s18_rusty_church** | 7/10 | Interior: entry vestibule (rust/clay walls) opening to nave — red carpet aisle, wood pews both sides, white altar with crosses, candlesticks, chandelier, warm lit sanctuary. Enterable + furnished = on-brief. | Walls very brightly lit/orange (overblown lighting). Vestibule ceiling low, textures stretched. Altar area washed white. No windows letting light — lighting feels artificial. |

## Per-area scores + prioritised fixes

### Island / terrain — 6/10
Relief exists but mountains read flat and fog over-washes everything; countryside is a huge empty flat plain.
1. Delete **floating rock slabs** near (300,200,-500) and above mountains ~(700,160,-700) in r14 — remove 2–3 hovering parts.
2. Reduce atmospheric fog/haze (global Lighting FogEnd up / Atmosphere density down) so r15 overview reads.
3. Add real relief to countryside plain around (900,30,-300)→(200,-300): raise terrain into 3–4 rolling hills + 1 ridge, vary height ±20 studs over ~600x600.
4. Fix dark-water bay bottom-right in r15 (~(900,0,1200)) to match sea colour, or intentionally tint consistently.

### Elf valley — 7/10 (strongest area)
Atmospheric and on-brief, but "dense canopy / rope bridges / washed paths" need work.
1. Add **rope bridges** between treehouses around the world tree (-1560,-430) — 3–4 bridges spanning ~40–80 studs at y≈40–60. *(Blender/custom mesh likely later.)*
2. Tone down path brightness: recolour glowing path material near tree base and radiating paths (-1560,-430 outward) from near-white to warm sand/amber.
3. Remove **stray white scroll/paper parts** clipping ground at tree base ~(-1560,16,-430) (2 parts) and fix the yellow trunk decal.
4. Fix statue float on r10 path ~(-1500,30,-425): drop 2 crowned statues onto their plinths.
5. Densify canopy in open grass gaps across valley (-1990..-1150, -860..80): add ~40–60 jungle trees + vine decals. *(Denser vines may want Blender later.)*
6. Fix pink dirt blotch under elf house (-1730,20,-300): recolour terrain to grass or make it an intentional path.

### Harbour — 6/10
Ships/piers sit correctly; main problem is oversized grass ruining the scenic ground shots.
1. **Reduce grass decoration height/density** along quay (-430,6,1830) and sea edge (-400,12,1790) — this is the worst visual defect (s16 unusable, s15 blocked). Shorten grass ~70% over the quay strip.
2. Lift/seat the floating mid-water boat near (-420,0,1850) onto waterline (y≈0–2).
3. Convert quay path (-390,6,1808) from dirt to stone/cobble material to read as a real quay.
4. Soften hard terrain/grass seam under foreground houses ~(-250,10,1850).

### Rusty town — 6/10
Church exterior + interior good; the huts are the problem — several are roofless empty shells.
1. **Roof and floor the hollow huts** near (1185,16,1141)→(1147,1222): add rust roofs + interior floors to the ~6+ open-topped shells visible in r13. *(Highest priority — looks unfinished.)*
2. Fix floating house on s17 street ~(1160,16,1190): seat it on ground.
3. Add ground relief/ruts/cobbles to flat sand street (1160..1406, 1141..1244) so it isn't a blank sand plane.
4. Fix church bright-green window glow at church (1406,16,1244) — recolour to stained-glass or dim.
5. Add the requested **graveyard** clearly near church (~(1406,16,1300)): ~15–25 gravestones + fence.
6. Tone down overblown interior lighting in church nave (1406,25,1244); add window light sources.

### Countryside — 5/10 (weakest)
Mostly covered under Island. Empty, flat, lacks farms/biome variety/landmarks.
1. Add **farms** on the plain ~(500,30,-300): 3–5 fenced field plots + 1–2 barns.
2. Add biome tree clusters (not sparse singles) along road ~(600..900,-300).
3. Place 1–2 landmarks (shrine/ruin) to break the empty green at ~(400,30,-200).

### Needs a Blender model later (flagged)
Rope bridges, dense vines, detailed treehouses, ships' rigging detail, ornate statues, chandelier/altar fittings — current placeholders are Roblox-part/decal approximations and would benefit from real meshes.

**Unavailable this session:** @Roblox_Studio MCP (not configured) — review was image-only, as intended.
