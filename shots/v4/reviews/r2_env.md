# Terrain & Environment Review — v4 / r2_env

Reviewer role: senior Roblox environment artist / art director. Honest, demanding. Reference = top-down fantasy-island art (north up). 17 photos reviewed. Not penalised but noted: snow-peak/badlands mesa meshes, Town-1 farms, bridges, trail dressing, elf-valley rebuild.

**Overall environment score: 5.5 / 10** — a large, real jump from the ~3/10 version (genuine relief, tree variety, biomes, mountains), but dragged down hard by camera/fog-ruined establishing shots, flat pool-cyan sea with no depth, and several floating-object / terrain-tear bugs.

---

## 1. Category scores (out of 10)

**Overall resemblance to reference — 5/10.** The biome layout is recognisably the reference (green heartland core, snow range NE, badlands SE, west cliff coast, forest W, capital/castle N). But the reference reads as a lush, saturated, densely-wooded jewel island with a deep teal→navy sea; the build reads paler, hazier, with a flat bright-cyan sea and visible seams. The silhouette is close; the surface finish is not.

**Terrain shape and relief — 6.5/10.** Real improvement: rolling hills (b07, b11), ridges, ravines (b06), a proper snow massif (b10, b12), badlands bluffs (b04). Good. But many mid-ground hills are bare, faceted and low-poly-angular (b05 hill behind capital, b03 foreground slopes), and relief flattens out toward the coasts.

**Coastline and beaches — 5/10.** Sandy beaches exist and read correctly (b09, b13). But the coastline is still fairly smooth/rounded versus the reference's craggy inlets, and the west "cliffs" (b14) are flat dark slabs rather than cliff faces. SE (b15) is almost all open water.

**Sea and water colour — 3/10.** The weakest category. Flat, uniform, bright pool-cyan (b15, b16, b09) with no shallow→deep gradient, no darkening offshore, no foam at the shore. The reference sea is deep teal fading to navy with bright surf rings around every landmass. This alone reads as "unfinished Roblox".

**Lakes and rivers — 5.5/10.** The ravine river (b06) and heartland river (b07, b11) are decent and read as flowing water in a cut channel — better than the old "thin ribbon on flat grass". Still narrow and samey in colour (same cyan as sea), and I could not verify the twin lakes / Town-1 lakes due to fog (b00/b01).

**Vegetation density and variety — 7/10.** Strongest category. 13.6k trees with real species mix — round oaks, dark pines, orange/autumn crowns, birch trunks, alpine firs, dry badlands acacias (b03, b07, b08, b11, b13). Dense and convincing in the heartland and forest. Minor: a few areas border on uniform "broccoli" clumping (b03, b13) and undergrowth is hard to judge from altitude.

**Rocks, cliffs and mountains — 5.5/10.** The snow massif (b10) and NE range with natural arches (b12) are good faceted work. Sea-stack spires (b08) read well. But the west "cliffs" (b14) are flat monolithic grey slabs, and several mid-ground rock piles and the badlands mesas are blocky/placeholder.

**Ground colours / materials and transitions — 5.5/10.** Good variety across biomes (green grass, dirt, desert tan, snow, leafy patches). But transitions are often a hard line (b05 green hill meets forest abruptly; b13 green hill meets a RED patch) rather than a blended gradient, and there is an out-of-place red terrain patch below the capital walls (b13, b16).

**Roads and trails — 4/10.** A road/path is faintly visible (b11 right edge, b06) but roads are thin, pale and mostly unreadable from above — nothing like the reference's clear tan road network linking every settlement. Largely still "not done".

**Lighting, sky and atmosphere — 4/10.** Pretty sky and clouds, warm-ish light. But the fog/haze is far too strong: it completely destroys the top-down (b00 = near-blank cyan) and overview (b01 = washed-out blue), and hazes every distant hill into pale blue. Atmosphere is hiding the map instead of flattering it.

**Scale / readability from above — 3/10.** The two shots whose JOB is to prove the island reads from above (b00 top-down, b01 overview) are unusable — fog turns them into flat blue rectangles. From the ground the scale feels right, but you cannot currently confirm the island matches the reference plan from the one angle that matters.

---

## 2. Per-photo verdict (vs a typical "before": flat green, sparse trees)

- **b00 topdown** — Near-blank cyan frame; fog has erased the entire island. UNUSABLE. (can't rate vs before — no content visible)
- **b01 overview_south** — Heavily fogged; island barely discernible as faint shapes. Better than before only in that structures exist, but WORSE as a usable shot.
- **b02 west_coast** — BETTER vegetation, but severe dark triangular z-fighting/clipping tears across the ground. Buggy.
- **b03 country_mid** — BETTER. Dense mixed forest, faceted mountain behind. Mountain is a bit blocky.
- **b04 east_badlands** — BETTER. Desert tan, grass-topped bluffs, dead trees, church set piece. Hazy and a touch sparse.
- **b05 north_ridge** — BETTER structures (excellent walled capital + castle) but the hill behind is bare/faceted with a hard biome edge.
- **b06 silverrun** — BETTER. River in a ravine through lush forest. Good.
- **b07 twin_lakes** — BETTER. Rolling hills, strong tree variety, river. One of the best.
- **b08 sw_forest** — BETTER (sea-stack spires + dense forest) but a floating terrain chunk at the left edge. Buggy.
- **b09 south_coast** — Mixed: nice beach/forest band, but a clearly FLOATING sea-stack islet above the water with a shadow beneath. Buggy.
- **b10 tower_massif** — Much BETTER. Faceted snow mountain + alpine village w/ igloos. A highlight.
- **b11 country_road** — BETTER. Lush forest, river, faint road. Good.
- **b12 ne_range** — BETTER. Snowy peaks, natural arches, sea stacks. Strong.
- **b13 north_cape** — BETTER forest + capital, but an out-of-place RED terrain patch below the walls (wrong colour).
- **b14 west_cliffs** — Mixed: good forest, but three flat dark monolithic rock slabs look like stretched boxes, not cliffs.
- **b15 se_beach** — WORSE-ish: mostly flat pool-cyan open sea, one isolated/floating rock, dark shadow artifact bottom-left.
- **b16 ne_river_mouth** — WORST. Camera clipping below/into terrain: upper half is detached terrain chunks, rocks and pines floating in the sky. Major bug.

Net: ~12 of 17 clearly better than "before"; 2 unusable (fog), 3 buggy.

---

## 3. Top 15 highest-impact fixes (ranked)

1. **Sea depth gradient & shore surf (whole coast, all water y=0).** Replace flat pool-cyan with a shallow→deep gradient (bright turquoise in the 0–30 stud shelf, mid-teal, then navy past ~150 studs offshore) and add white foam/surf rings at every shoreline. Biggest single readability + "AAA" win. Ref sea is deep teal→navy with surf.
2. **Fix the NE river-mouth floating/clipping cluster (~x 2300–2900, z −900 to −1400, b16).** Detached terrain chunks + floating rocks/pines. Reseat all objects to ground; close the terrain void. Currently reads as broken.
3. **Cut the fog / draw distance so the top-down reads (b00, b01).** Reduce FogEnd/atmosphere density dramatically (or raise FogEnd to several thousand studs) so a top-down at y≈4600 shows the actual island, not blue. Without this you cannot verify resemblance at all.
4. **Reseat floating set-piece islets (b09 south coast ~x300,z1700; b08 left edge; b15).** Several sea stacks / terrain chunks hover above water with gaps and shadows. Drop to seabed or raise water.
5. **Fix z-fighting / terrain tears on west-coast ground (b02, ~x −2150→−1500, z 350–500).** Dark triangular artifacts = overlapping coplanar surfaces. Rebuild/relevel that terrain slab.
6. **Remove the red terrain patch below the capital walls (b13/b16, ~x 0–200, z −2400 to −2500).** Wrong colour bleeding through; repaint to grass/dirt.
7. **Rebuild the west "cliffs" as real cliff faces (b14, ~x −3200→−2500, z −300).** Replace the 3 flat dark slabs with layered, stratified cliff geometry (reuse the good strata method) with varied height; they currently look like boxes.
8. **Soften hard biome borders with blended transition bands (b05 green↔forest ~z −1750; b04 desert↔grass; snow↔grass at b10).** Add 50–100 stud dirt/leafy/scree gradient strips instead of a hard line.
9. **Dress the road network so it reads from above (reference shows clear tan roads to every settlement).** Widen main roads to ~12–16 studs, use a warm packed-dirt material, add visible junctions linking Capital↔Town1↔Harbour↔Rusty town↔Alpine.
10. **De-facet / displace the bare mid-ground hills (b05 hill behind capital; b03 foreground; b13).** Add a subtle noise pass + scatter rocks/bushes so they stop reading as flat low-poly triangles.
11. **Vary tree clumping to kill the "broccoli field" look (b03, b13 heartland).** Introduce clearings, size variance, and a few hero/standout trees; thin the uniform round-oak mass by ~15–20%.
12. **Widen and vary the rivers (b06, b07, b11).** Some reach 20–40 studs, add bends, gravel banks, a couple of small rapids/waterfalls; tint river water slightly greener than the sea so it doesn't read as the same cyan.
13. **Richen & saturate the heartland grass; reduce the pale wash.** Reference grass is deep saturated green; build grass is lighter/greyer under haze. Boost grass colour saturation and use leafy-grass patches for mottling.
14. **Add shallow-shelf sand + submerged terrain around every islet (b09, b15, b16).** The islets sit in abruptly deep water; add a sand halo so they look rooted, not dropped in.
15. **Thicken coastline cragginess (whole perimeter).** Reference coast has inlets, points and small coves; current coast is smoother/rounder. Add a few bays and headlands, especially W and SE.

---

## 4. Regressions & bugs

- **FLOATING OBJECTS:** south-coast sea stack hovering with shadow (b09); floating terrain chunk left edge (b08); isolated floating rock (b15); large floating-chunk/rock/pine cluster at NE river mouth (b16). Highest priority — breaks immersion instantly.
- **CAMERA/TERRAIN CLIPPING or VOID:** b16 upper half = detached terrain/objects "in the sky" = camera below surface or a genuine terrain hole/void at the river mouth. Verify there is no black void / missing terrain there.
- **Z-FIGHTING / TERRAIN TEARS:** b02 dark triangular artifacts across the west-coast ground (coplanar overlap). Also faint dark shadow artifact bottom-left of b15.
- **WRONG COLOUR:** red terrain patch under the capital walls (b13, b16).
- **FOG TOO HEAVY (regression in readability):** b00 top-down is a near-blank cyan square; b01 overview washed out. The map is being hidden by atmosphere.
- **BLOCKY/PLACEHOLDER GEOMETRY:** west cliffs flat slabs (b14); some mid-ground mountains/mesas faceted and boxy (b03, b05); expected to improve once mesa/snow-peak meshes land.
- **TOO UNIFORM:** heartland tree clumping borders on repetitive "broccoli" (b03, b13).
- **PERFORMANCE WORRIES:** 13.6k trees + 11.4k undergrowth + 3.7k rocks is heavy; the dense heartland/forest (b03, b11, b13) is where FPS and streaming will hurt most on mid-range devices — budget LODs / StreamingEnabled and thin the densest clumps.
- **SEA HAS NO DEPTH (regression not fully fixed):** the old "pool-cyan, no depth" complaint largely persists on open water (b15, b16, b09).

---

## 5. Top-down vs reference, and the 5 changes that close the gap

Today's top-down (b00) literally cannot be compared — fog has erased it to a flat cyan rectangle — and even the overview (b01) is a pale blue wash, whereas the reference is a crisp, saturated, high-contrast island: deep teal→navy sea with bright surf, a dense dark-green forested landmass, clear tan roads webbing between every named settlement, a sharp snow range NE and tan badlands SE. The build's biome *placement* matches, but its *finish* (sea depth, saturation, road legibility, atmosphere) does not. The 5 changes that would close most of the gap: **(1)** slash the fog / extend draw distance so the island actually renders from above; **(2)** give the sea a shallow→deep colour gradient + shoreline surf; **(3)** build a clearly readable tan road network between settlements; **(4)** boost ground/vegetation saturation and soften biome borders into blended bands; **(5)** fix all floating objects and the NE river-mouth clipping/void so the perimeter reads clean. Do these and a fresh top-down should jump from unusable to a strong 7+.

File: `C:\Users\Nitro\.kiro\crew\workspace\town\shots\v4\reviews\r2_env.md`
