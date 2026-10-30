# Base Towns — Art Review (v4)

Reviewer stance: strict. Target is a "very, very high quality, proper Roblox game." Current state is competent kit-bashing with real problems in cohesion, terrain integration, scale discipline and material variety. Nothing here yet reads as top-tier Roblox production. Scores reflect that bar, not effort.

**MCP note:** `@Roblox_Studio` MCP server was NOT available this session, so this is a visual review only — no scene graph, no part counts, no live measurement. All coordinates below are inferred from the camera metadata and should be verified in Studio.

---

## 1. Settlement scorecard

### Town 1 — "Skull Town" — **5/10**
Layout reads as three disconnected set-pieces (walled church/graveyard NE, plaza S, skull HQ N) rather than one town; the castle-grade curtain wall wrapping a modest church+graveyard is a scale mismatch — those blue-cone towers belong to the capital, not a starter town. Density is thin: large flat green gaps between clusters, the graveyard (c02) is a few props on bare grass. Materials are the stock Roblox half-timber kit reused verbatim from the capital, so Town 1 has no identity of its own except the skull. The giant skull (c04) is the only real landmark but it floats/sits on a flat pink gravel pad with no base integration and no supporting theme around it. Terrain is flat and unnatural — buildings sit on a green tabletop.

### Capital (walled city) — **6.5/10**
Best large-scale layout: clear grid, curtain wall, radial avenues, a cathedral and keep anchoring the center (c05). The main avenue (c06) is genuinely good — lamp rhythm, bunting, framed vista to the keep. But it is monotonous: the entire city is red/blue-roof half-timber with almost no building-type variety (no market hall, no distinct guild/temple massing beyond the church), so from the air it's a texture of identical houses. Grid blocks are too empty inside — green courtyards with nothing in them. Wall towers are oversaturated cobalt blue; reads toy, not regal.

### Castle compound — **5.5/10**
Silhouette is strong from distance but the interior courtyard (c07) is a near-empty gravel lot with a scatter of props and one incongruous red-roof shack against the wall. For a capital's seat of power this is underbuilt — no keep interior staging, no gardens, no barracks massing, no paving pattern. The pure-white wall + cobalt cones is the same toy palette as everything else; a royal castle needs material and color separation from the common town. Terrain: walls meet the hillside abruptly with visible flat-cut benches (c07 left/foreground).

### Alpine village + ice lake — **6/10**
The village itself (c09) is the single most convincing street in the set: snow-dusted log cabins, market stalls with produce/barrels, bunting, warm interior light — good density and life. But the air view (c08, c10) exposes a hard, unnatural snow/grass border — the white zone is a flat-painted blob with a crisp edge against bright green, no transition. The "frozen lake" (c10) is a raised slab of ice sitting ABOVE the surrounding ground with vertical cliff sides — it reads as a floating table, not a lake, and the igloos on top make the scale confusing. Rock mountain behind is low-poly and flat-shaded.

### Elf valley (world tree) — **5.5/10** (layout only, per brief)
Layout is readable — world tree centered, radial dirt paths, ponds, a ring shrine (c11 lower-left). Good bones for a hub. But it is sparse and samey: endless identical bushy trees on flat green, white blob-mushrooms scattered like confetti (c11) with no clustering logic, and the ground is one flat grass plane. c12 path level shows the glow/crystal theme that is being removed — judging layout only, the path framing is decent but props (glowing stumps, crystal totems) are randomly placed, not composed. Terrain is flat tabletop again.

### Harbour — **6.5/10**
Strongest sense of place after the capital avenue. The pier + two tall sailing ships + buoys + rowboats (c13) give it real identity and life, and the house cluster has decent density. Weaknesses: the water is a flat cyan plane with no depth gradient or shoreline foam, so ships look pasted on; the headland fort (c13 right) is a tiny bare stub; the grass behind the houses is empty flat green with no docks-district clutter (crates, nets, fish barrels) spilling inland.

### Rusty desert town — **4.5/10**
Weakest settlement. The oversized grey/pink gothic church (c14) is wildly out of style and scale for a "rusty" shanty town — it looks imported from a different game and dwarfs everything. The huts are a monotonous grid of identical rust-roof boxes with no street hierarchy, and the ground-level shot (c15) shows crude untextured plank/plaster boxes with harsh seams and a rust roof that is a single flat stretched texture. Dead trees are repeated identically. The desert ground is flat and empty between structures — lots of dead zone.

---

## 2. Concrete fixes, ranked by impact

### Town 1 (~0,5,-60 plaza; ~-210,0,240 church; ~0,25,-402 skull)
1. Downgrade the curtain wall: replace the capital-grade white/cobalt towers around the church (~-210,0,240) with a low timber palisade or stone garden wall ~8–12 studs tall. Keep the town subordinate to the capital.
2. Build a skull plaza (~0,25,-402): give the skull a rock/bone base sunk ~4 studs into terrain, ring it with braziers, banners, a dark-stone pavement, and 4–6 themed stalls so it reads as the HQ, not a prop on gravel.
3. Fill the dead green between plaza (0,-60), church (-210,240) and skull (0,-402): add 8–15 houses + a connecting road so the three set-pieces become one town.
4. Flesh the graveyard (c02, ~-250,8,240): add 20–30 more headstones in rows, iron fencing, a gate, fog/dead-tree clusters; right now it's bare.

### Capital (center ~0,40,-1650)
1. Add building-type variety: convert ~15% of houses into distinct types — a market hall, a 2-storey guild, an inn with sign, a temple annex, stables — varying footprint and roof height so the air view (c05) stops reading as one repeated house.
2. Populate the empty grid courtyards with wells, trees, market stalls, carts, washing lines.
3. Desaturate wall-tower cones from cobalt to a muted slate/steel-blue; the toy blue cheapens the whole city.
4. Vary roof color beyond the red/blue binary — add weathered green-copper, grey slate, thatch.

### Castle (center ~0,100,-2200)
1. Build the courtyard (c07): add paving pattern, a central fountain/statue, formal garden parterres, barracks/stable blocks against the inner walls, training dummies. Remove or re-skin the red-roof shack — it breaks the royal tone.
2. Separate the royal palette from the town: give walls a cream/gold stone and banners, distinct from common-town white.
3. Fix the wall-to-hill meeting (c07 foreground/left): blend terrain up to the wall base or add a stone plinth so walls don't sit on flat-cut benches.

### Alpine + ice lake (village ~1600,124,-900; lake ~1450,152,-1100)
1. Fix the snow/grass border (c08): add a 40–80 stud transition band — patchy snow over grass, more conifers, rock outcrops — instead of the crisp painted edge.
2. Rebuild the "frozen lake" (c10): sink the ice to ground level inside a carved basin with sloped snowy banks; right now it's a raised slab with cliff sides. Decide igloo vs lake — don't stack a village on top of the lake.
3. Keep the market stalls and cabin density of c09; extend that quality outward.

### Elf valley (world tree ~-1560,30,-430) — layout only
1. Cluster the mushrooms and props instead of confetti-scatter; group them along paths and pond edges, leave open glades.
2. Add tree-species and height variety; the uniform bushy canopy is monotonous.
3. Break the flat ground plane: gentle mounds, sunken pond basins, raised root buttresses at the world tree base.

### Harbour (center ~-420,10,1850)
1. Add shoreline treatment: foam line, a darker water depth gradient, wet-sand strip, so ships/piers sit IN the water.
2. Build out the headland fort (c13 right) — it's a stub; make it a small lighthouse or bastion as a landmark.
3. Spill dock clutter inland: crates, fishing nets, barrels, drying racks across the empty grass behind the houses.

### Rusty town (center ~1380,30,1220)
1. Replace or radically re-scale the gothic church (c14): it is the wrong style/era/scale. Swap for a weathered chapel or a rusted watchtower matching the shanty theme, ~40% of current height.
2. Re-skin the huts (c15): the plank/plaster boxes are untextured and seam harshly. Add proper wood/adobe materials, vary roof pitch and size, add lean-tos and awnings.
3. Fill the desert dead zones with rock clusters, cacti/scrub, broken carts, rusted debris, sand drifts; introduce a main street with hierarchy instead of a uniform grid.
4. Stop reusing the identical dead tree — vary or thin them.

---

## 3. Do NOT change (already good)
- **Capital main avenue (c06):** lamp rhythm, bunting, framing to the keep — keep this exact composition as the quality bar.
- **Alpine market stalls + cabin street (c09):** best density/life in the set; use as the template for other towns.
- **Harbour ships + pier + buoys (c13):** strong landmark identity; keep the ships and pier layout.
- **Capital overall grid + curtain-wall footprint (c05):** good large-scale readable plan.
- **Elf valley radial path + world-tree centering (c11):** sound hub layout; only props/terrain need work.

---

## 4. Visible bugs
- **Studio Move/Rotate gizmo and axis "Back/Right/Left" labels visible in c03, c04, c06, c07, c08, c10, c14, c15** — not part of the world; re-shoot without a selected part, or deselect before capture.
- **Floating "airship/kite" sprite in sky:** c04, c05, c07, c13 — a white diamond object hovering in the sky. Confirm it's intended; if not, it's a stray floating part.
- **Ice "lake" (c10):** raised slab floating above ground level with vertical cliff edges — reads as a floating table; z-level is wrong.
- **Skull HQ (c04):** giant skull sits on a flat pink gravel pad with a hard shadow seam and no base integration (possible slight float/sink at the grass line).
- **Snow/grass seam (c08, c10):** hard unnatural painted border, no blend.
- **Rusty huts (c15):** untextured faces and harsh plank/corner seams; the rust roof is one flat stretched texture (texture stretching).
- **Rusty church green windows (c14/c15):** flat solid-green glass reads as a material error, not stained glass.
- **General terrain:** most towns sit on flat green/sand tabletops — buildings meet ground with no foundation or grading (Town 1, elf valley, capital edges).
- No obvious z-fighting or black voids detected in these angles, but verify the skull pad and ice-slab undersides in-engine.

---

## 5. Overall top 10 improvements (ranked)
1. **Terrain integration pass across ALL towns** — ground buildings into graded terrain with foundations; kill the tabletop look. Highest-impact, most pervasive issue.
2. **Rescale/replace the rusty-town gothic church** — single worst style break in the map.
3. **Fix the ice "lake"** — sink it to ground level in a carved basin; stop it floating.
4. **Add building-type variety in the capital** — market/guild/inn/temple massing so the city isn't one repeated house.
5. **Re-skin rusty town huts** — real materials, varied roofs, kill texture stretching.
6. **Build out the castle courtyard** — paving, fountain, gardens, barracks; remove the red-roof shack.
7. **Downgrade Town 1's capital-grade walls** and unify its three set-pieces into one town.
8. **Fix the alpine snow/grass border** with a transition band.
9. **Desaturate the cobalt-blue tower cones** everywhere — they cheapen castle, capital and Town 1.
10. **Water + shoreline treatment at the harbour** (and ice lake) so ships and piers sit in the water, not on a cyan plane. Also: deselect parts before all future captures to remove Studio gizmos.
