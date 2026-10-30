# R2 Settlement Review — v4 (after terrain rebuild)

Art director: strict. Scope: settlements only (buildings not yet reworked). Studio overlays ignored.

---

## 1. Per-settlement scores & critique

### Town 1 (skull town) — 6/10
- **Layout/readability:** Good. Walled plaza, church+graveyard quarter, skull HQ on its plateau all read clearly. The half-timber house set is attractive and the plaza (c03) is the strongest street-level shot in the whole map — banners, lamps, benches, statue fountain, topiary all reading as a lived-in civic square.
- **Density/scale:** Plaza is well-dressed; church quarter (c01) is pleasingly tight. Skull HQ (c04) is a strong landmark but the apron around it is a bare tan disc with only 3 lamps + 2 braziers — under-dressed for the main icon of the town.
- **Terrain integration:** This is the weak point. Every wall, church and tower meets the grass as a hard flat seam — buildings still sit on a green tabletop (c01, c04). The blue cone towers are over-saturated cobalt and clash with the soft palette. Graveyard (c02) is a brown dirt rectangle with a crisp painted edge against green.
- **Props/life:** Plaza good; rest of town sparse.

Ranked fixes:
1. Skull apron (0,25,-402): add a low ring of 6–8 bushes/rocks and 2 banner poles around the tan disc; break the perfect circle edge with grass tufts.
2. Recolour all blue cone roofs (towers c01/c04) from cobalt to a muted slate/navy — knock saturation down ~40%.
3. Graveyard (-250,8,240): scatter 10–15 small rocks + 4 dead bushes over the dirt edge to feather the hard grass seam; add 2 lamp posts.
4. Add a few bushes/flower beds at the base of the church and wall towers to hide the flat ground seam.

### Capital city — 6.5/10
- **Layout/readability:** Excellent grid, clear main avenue to the cathedral/palace, strong curtain wall with gatehouses (c05). Avenue (c06) reads as a real street with bunting, lamps, mixed house fronts.
- **Density:** High and convincing from the air. Good roof-colour mix (red/blue/grey) now, less repetitive than the earlier pass.
- **Scale/integration:** The whole walled block sits on a dead-flat green pad (c05) — no grading, no skirt vegetation, the wall base is a razor line against grass. Interior block streets have almost no trees or plaza greenery; large green gaps between house rows read as empty lawn, not courtyards.
- **Colours:** Good. The one disused detached walled annex top-right of c05 is empty.

Ranked fixes:
1. Plant tree rows + hedges along the inside of the curtain wall and in the empty green gaps between house blocks (c05) — ~40–60 trees, breaks the lawn and hides the flat seam.
2. Add bushes/rock clusters along the OUTSIDE wall base all the way round to kill the tabletop seam.
3. Dress the empty avenue ends (c06) and the central round plaza with 4–6 market stalls + a well/statue.
4. Fill the empty annex (top-right c05) with a garden or barracks yard, or remove it.

### Castle compound — 5.5/10
- **Layout:** Reads as a castle — keep, curtain wall, corner towers, gatehouse ramp (c07). Keep building itself is nice.
- **Density/courtyard:** The courtyard is the problem the last reviewer flagged and it is still 80% empty — a vast grey slab with one cluster of banner poles and a couple of crates in the middle, one lonely red-roof shed against the wall. Dead zone.
- **Scale/integration:** Wall base meets grass flat; the rocky skirt on the left edge is the only grading and it's rough/unnatural (c07 bottom-left, blocky dark boulders stuck to the slope).
- **Colours:** Towers here are a deep slate-navy that works better than Town 1's cobalt — fine.

Ranked fixes:
1. Fill courtyard (0,100,-2200 area): add a central statue or fountain, 2 rows of market/armoury stalls, a training yard (dummies/racks), 6–10 trees along the inner wall, stacked crates/barrels in corners. This is the #1 castle fix.
2. Feather the left rocky skirt — replace the blocky dark boulders with the softer rock models and add grass/bushes between them.
3. Add banners down the gatehouse ramp and torches along the inner wall walk.
4. Place a few bushes/trees at the outer wall base to remove the flat seam.

### Alpine village + ice lake — 6/10
- **Layout:** Cosy cluster of A-frame chalets with snow roofs under a good craggy peak (c08). Square (c09) is well-dressed — market stalls, bunting, barrels, fruit crates; genuinely nice.
- **Snow border — still the biggest issue:** The snow/grass transition is a HARD painted line (c08, c10). The village sits half on bright green grass, half on snow, so the chalets on green (c08 foreground, c09) look like they teleported out of the biome. The square (c09) is on vivid green grass with snowy pines around it — jarring.
- **Ice lake (c10):** Lowering into a bowl helped — it now reads as a recessed frozen surface rather than a raised slab. But the ice is a flat pale-blue sheet with a hard edge; igloos and huts sit right at its rim.
- **Integration:** Igloos/huts generally sit flat on snow OK; a few props near the lake rim look like they float at the hard ice edge.

Ranked fixes:
1. Widen the snow→grass transition into a 20–40 stud dithered band: paint a mixed snow/rock/sparse-grass ring around the whole village so no chalet sits on pure green (c08/c09). Highest priority.
2. Pull the square (c09) fully onto snow or a snow-dusted cobble pad — it must not sit on bright green.
3. Ice lake rim (1450,152,-1100): add a snow-bank lip + a few rocks around the edge so the ice doesn't meet snow as a clean cut; add 2–3 cracked-ice detail decals or a small dock.
4. Dark GPU/denoiser patch on the peak face right of centre (c08/c10) — the near-black cliff band looks like a lighting void; re-check that rock's material/vertex colour.

### Elf valley terrain — 7/10
- **Layout/readability:** Best-reading natural area. The giant world-tree is a genuine landmark (c11), paths radiate well, rope bridge and stream with plank crossing (c11 right) integrate nicely. No glow now, as intended — good call, it looks more natural.
- **Density/detail:** Rich — layered canopy trees, glowing mushroom props, small pools, a gazebo/shrine bottom-left. Ground-level (c12) is atmospheric with crystal totems and mushrooms, though c12 is the old to-be-replaced village so judged lightly.
- **Scale/integration:** Terrain grading is the most natural of any area — rolling, with real relief and tree cover feathering the edges. Pools sit in the ground properly.
- **Note:** The two blue pools (c11 bottom-centre and bottom-left) have a slightly hard rim; minor.

Ranked fixes (terrain/surroundings only):
1. Feather the two pool rims (c11) with reeds/rocks — currently a clean circle edge.
2. The sandy clearings around the world-tree base and lower-left read a touch bare — add a few ferns/bushes.
3. Minor: one small bright sand patch mid-right could get undergrowth.
(Village rebuild itself out of scope.)

### Harbour — 6.5/10
- **Layout:** Reads clearly as a coastal town — waterfront road, piers, ships, buoys, anchors, a windmill/ruin on the headland (c13). Good mix of house styles.
- **Density:** Decent near the water; thins fast inland into plain green lawn with scattered houses and few trees (c13 right/foreground).
- **Scale/integration:** Houses sit flat on a green pad again — no grading toward the beach, hard grass/sand line. The waterfront is nicely busy (crates, anchors, striped stalls); inland is bare.
- **Colours:** Good — navy/red/cream roofs, warm sand, blue sea. Palette is cohesive.

Ranked fixes:
1. Add trees + hedges + garden plots through the inland green gaps (c13 right) — ~25–35 trees to break the empty lawn.
2. Feather the beach→grass line with dune grass, driftwood and rocks along the whole shore.
3. Add nets, barrels, fish-drying racks and 2–3 small rowboats along the piers to push the fishing-village life.
4. Dress the headland windmill/ruin with a path and a couple of trees so it reads as a destination.

### Rusty desert town — 4.5/10
- **Layout:** Weakest settlement. Church-on-a-mound centrepiece with shanties clustered below reads OK as a layout, but the execution is rough (c14).
- **Church — still wrong:** The big pink/salmon stone church with a tall spire (c14/c15) is out of style and too large/clean for a rusty desert shanty town — exactly the prior complaint, unaddressed. It looks like it was imported from the capital and repainted.
- **Density/materials:** Huts are plain tan/wood boxes with rusty metal roofs. Several are **open-topped / missing roofs or walls** (c15 — the left hut is a hollow box you can see straight into; gaps between wall and roof on the right huts). Textures on the huts are flat and stretched. The desert floor is a vast bare tan plane with sparse dead trees and a hard coast line — reads empty and unfinished.
- **Integration:** Flat ground, huts sit on a dead plane; mesas in the background are blocky.

Ranked fixes:
1. Fix the open/broken huts (c15, ~1200,16,1220): every hut needs a closed roof and 4 walls — several are hollow boxes. #1 bug.
2. Church: recolour from pink to weathered sand/ochre stone, add rust/wear, and shrink it ~25%; or swap the spire for a squat adobe tower so it fits the biome.
3. Dress the empty desert floor: add rock clusters, dead bushes, broken carts, tent awnings and barrels between huts and out to ~80 studs; cluster the shanties tighter so the dead tan gaps shrink.
4. Vary hut materials — mix adobe, canvas, scrap-metal and timber instead of near-identical tan boxes; recolour some roofs to varied rust tones.
5. Feather the desert→sea edge with rocks and a small beach.

---

## 2. Must-NOT-change (already good)
- Town 1 **plaza** (c03) — statue fountain, banners, lamps, benches, topiary. Best street scene on the map.
- Town 1 **skull HQ** sculpt itself (c04) — strong landmark, keep as-is (only dress the apron).
- Capital **main avenue** (c06) — bunting, lamps, mixed fronts; reads great.
- Capital **grid + curtain wall** structure (c05) — excellent bones.
- Castle **keep + wall/tower silhouette** (c07) — fine; only the courtyard needs filling.
- Alpine **square dressing** (c09) — stalls/bunting/crates are lovely (just move it off green).
- Elf **world-tree + bridges + stream** (c11) — flagship landmark, keep.
- Harbour **waterfront props + ships** (c13).
- The new **surrounding vegetation and relief** everywhere — a big step up; the problem is only the flat pads directly under the settlements.

## 3. Visible bugs
- **Rusty town huts open/hollow** — several have no roof or a missing wall (c15). Clear bug.
- **Hard biome seams** — snow/grass painted line at alpine (c08/c10); grass/sand lines at harbour and rusty town; every town-core pad meets grass as a razor-flat seam (c01, c05, c07, c13).
- **Dark cliff void** on the alpine peak (c08/c10) — near-black band that looks like a lighting/denoiser artefact, not rock.
- **Over-saturated cobalt cone roofs** at Town 1 (c01/c04) — colour clash.
- **Stretched/flat textures** on rusty huts (c15).
- **Hard circular rims** on elf pools and ice lake edge (c10/c11) — minor.
- No floating buildings or trees-inside-buildings seen; no z-fighting or black-void geometry beyond the alpine cliff patch.

## 4. Overall top 10 improvements (ranked)
1. **Fix the broken/open rusty-town huts** — close all roofs and walls (c15). Functional bug.
2. **Kill the flat tabletop seam under every settlement** — add bushes/rocks/trees around all wall and building bases (capital, castle, Town 1, harbour).
3. **Widen the alpine snow→grass border** into a dithered 20–40 stud band; move the square off bright green (c08/c09).
4. **Fill the castle courtyard** — statue, stalls, training yard, corner crates, inner-wall trees (c07).
5. **Rework the rusty-town church** — recolour to weathered sand, shrink ~25%, de-"capital" it (c14).
6. **Dress the empty desert floor** — rocks, dead brush, carts, tents; cluster huts tighter (c14).
7. **Recolour over-saturated cobalt cone roofs** to muted slate at Town 1 (c01/c04).
8. **Green the capital interior & harbour inland** — tree rows and hedges in the empty lawn gaps (c05/c13).
9. **Dress the skull-HQ apron** — ring of bushes/rocks/banners around the bare tan disc (c04).
10. **Fix the dark alpine cliff void** and feather the ice-lake rim with a snow lip + rocks (c08/c10).
