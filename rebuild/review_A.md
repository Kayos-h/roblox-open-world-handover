# Visual Review A — Phase 1 Map

Unavailable MCP servers this session: **@Roblox_Studio** (not configured). Review is image-only, read-only.

## Per-picture scores

| Shot | Score | What I literally see | Defects |
|---|---|---|---|
| r01_t1_church_air | 6/10 | Aerial over Town 1 SE. Red-roof church bottom-right, graveyard behind it as a bright-green lawn with a dozen pale crosses, a few bare trees, a short black fence, a blue-canopy stall. Half-timber houses, a small stream + wooden bridge, blue-cone wall towers. Pond top-left. | Graveyard reads as a **sunny green meadow**, not a cemetery — turf too vivid, graves sparse. Burn/scorch mark on wall left of graveyard. Stream ends abruptly. |
| r03_capital_air | 8/10 | Dense walled capital, hundreds of blue/red/half-timber houses, grid streets, blue-spire cathedral mid-left, white castle on far ridge, central fountain plaza, airship. | Roof palette repeats (same blue/red pairs tile across blocks). Castle compound reads small/pale vs the city mass. Bright uniform grass outside walls. |
| r04_capital_ave | 7/10 | Ground-level cobbled avenue, half-timber houses both sides, lamp posts, bunting, cathedral spire + plaza ahead. | House designs repeat (same 2–3 facades mirrored). Grass tufts poke through cobble at edges. A floating "Rock" label (watermark/gizmo) top-right. |
| r05_castle | 6/10 | Walled castle on a hilltop: white keep, many blue-cone spires, large empty bailey (dirt/grass), one tiny red-roof shed, sparse props. Rocky slopes. | **Bailey is large and empty** — one shed dwarfed by space. Props scattered, no composition. Rock terrain below walls is blocky. |
| r06_alpine_air | 8/10 | Alpine village on a ledge: ~15 snow-roof chalets, snow pines, frozen lake upslope with shanties + igloos, grey tower-mountain behind, market square. Good scale vs mountain. | Lake edge sits a touch high; some pines float slightly on the slope. Harsh terrain shadow line across the ledge. |
| r07_alpine_square | 8/10 | Market square: log chalet, bunting, striped stall canopies, fruit barrels/crates, stone planters. Snow pines, mountain backdrop. | Grass tufts very tall in foreground (clip camera). Stall goods a bit toy-bright for alpine. |
| r08_icelake | 7/10 | Huge Ice-material lake on the ledge, snow pines, igloos (2) and wooden shanties ON the ice, chalet left, mountain + floating rocks behind. | **Lake rim floats** — ice slab sits above grass with a visible vertical terrain cliff/seam at the near edge. Igloos sit on the rim edge, half off the ice. |
| s01_gy_inside | 7/10 | Inside graveyard: crosses, headstones, bench, hanging lanterns, candles, dead trees, boulder, poppies, black fence, blue-cone towers over the wall. Actually reads as a graveyard here. | Turf still bright sunny green (no desaturation/dirt). Spacing loose — gaps between graves read sparse. |
| s02_gy_high | 6/10 | Over-wall view: graveyard beyond battlement — crosses, lanterns, bare trees, blue fence, church roof right. | Same scorch/burn mark on wall. Graves thin; large empty green patches. Fence changes colour (black inside vs blue here). |
| s03_church_front | 7/10 | Church facade: pale stone, red spire, round stained-glass rose window, pointed arch door, flag tower left, houses right, bridge. Sun flare. | Door reads shut (good, not enterable). Very strong bloom/overexposed sun washes the top. Grass tufts tall at base. |
| s04_t1_gate_s | 7/10 | South gate: stone gatehouse, purple tree-sigil banners, torches, timber arch, skull HQ framed through the arch down a cobble path. | Interior of arch timber looks unfinished/raw. "Back" label gizmo floating. |
| s05_t1_corner_se | 5/10 | SE wall corner from outside: long grey battlement, blue-cone towers, skull head + houses peeking over, flat green field. | **Very empty** — huge blank lawn, repeated identical towers, flat lighting. Grass is one flat green. Reads unfinished outside the wall. |
| s06_t1_plaza_skull | 8/10 | Skull HQ: large horned white skull monument on a mound, cobble approach, trees, boulders, walls + mountain behind. Strong focal point. | Skull base blends into mound (no plinth). Boulders a bit flat-shaded. Good scale — keep. |
| s07_igloos | 6/10 | Alpine street: log + stone chalets, snow roofs with icicles, white igloo domes beside houses on grass, lamp. | Igloos sit on **green grass, not snow/ice** — looks out of place. Right chalet wall fills half the frame (camera too close). |
| s08_fishing_ice | 6/10 | On the frozen lake: blue + red shanties, a bucket (fishing hole), a small dock/bench, snow pines + igloos on far rim, mountain. | Only ~2 shanties + 1 hole for a "huge" lake — **under-populated**. Ice is a flat pale sheet, no cracks/holes texture. Far shanty tiny vs near one. |
| s09_icelake_edge | 6/10 | Lake edge: blue shanty, bucket, green + wood shanties, snow pines, floating rock islands, mountain cliff, sea horizon. | Floating rocks read as unfinished sky debris. Lake meets grass with a hard flat line. Sparse props. |
| s10_tower_scale | 4/10 | A single giant snow-pine fills the frame, chalets either side, mountain behind. | **Tree is wildly oversized** — dwarfs the houses, clips the ground, snow-cap texture blotchy/pixelated. Camera aimed at tower mountain but tree blocks it entirely. |
| s13_castle_close | 6/10 | Castle plaza close: white keep + blue spires, banners, fountain, lamps, benches, a blue royal cart, red-roof hall left. | Plaza **large and sparse** — props thinly scattered on a big pale apron. Keep looks flat/low-detail up close. |
| s14_capital_sq | 8/10 | Capital fountain square: tiered marble fountain with sun finial + water jets, ringed by cream/red half-timber houses, market stalls, bunting, lamps. Lively. | Fountain water is flat cyan (no transparency/flow). Good density — best capital shot. |

## Area summaries & prioritised fixes
*(coords derived from CSV pos/look; +Z south)*

### Town 1 — overall 6.5/10
Skull, gate and church are strong; the graveyard still reads sunny/sparse and the outside walls are empty.
1. Graveyard turf recolour — around (-238,246), repaint the ~84×104 patch from bright grass to a desaturated olive/brown ground material (LeafyGrass/Ground mix), add scattered dirt decals. **Script-doable.**
2. Densify graves — add ~20–30 more headstones/crosses at (-238,246) to fill the 9 rows; tighten spacing to ~6-stud grid. Script-doable.
3. Remove/repair scorch mark on the west graveyard wall near (-290,240). Script-doable.
4. Darken graveyard lighting mood — add a couple more lanterns + lower local brightness around (-238,246). Script-doable.
5. Fill SE exterior field — add low hedgerows/path/farm plots across the lawn near (297,297) to (297,-100) so the outside isn't blank. Script-doable.
6. Extend/retexture the stream near (-80,250) so it doesn't end abruptly. Script-doable.
7. Add a plinth/base ring under the skull at (0,-402) so it doesn't melt into the mound. Script-doable.
8. Finish raw timber inside south gate arch at (0,297). Script-doable.
- **Blender later:** detailed headstone/mausoleum/statue meshes, a proper skull-monument mesh.

### Capital — overall 7.5/10
Dense and convincing from the square; roofs repeat and the castle compound reads small/empty.
1. Castle bailey fill — plaza centred ~(0,-2140): add ~8–12 props (tents, training dummies, carts, market rows, troops) spread across the bailey; it's one shed now. Script-doable.
2. Vary roof palette — across the housing blocks z -1300..-1900, introduce 3–4 more roof colours/pitches to break the blue/red tiling. Script-doable.
3. Add 2–3 new house facade variants and distribute along the main avenue (z -1300..-1600). Partly script, mesh variety is **Blender later.**
4. Castle plaza (~0,-2150) — cluster benches/lamps/banners nearer the keep; it's too sparse. Script-doable.
5. Give the fountain water at (0,-1480) transparency + a flow texture. Script-doable.
6. Trim grass tufts clipping cobble on the avenue (z ~-1300). Script-doable.
7. Add perimeter detail (gardens/stalls) outside walls near (300,-1050) to soften the flat lawn. Script-doable.
8. Remove the "Rock" gizmo/watermark visible near (0,-1600). Script-doable.
- **Blender later:** hero cathedral + keep meshes, varied house kits.

### Alpine — overall 6.5/10
Theme and mountain scale are good; the frozen lake floats and is under-populated, igloos sit on grass, and one pine is broken-scale.
1. Fix floating lake rim — lake centre (1490,-1080), y≈152: lower the Ice slab so it's flush with surrounding terrain; remove the vertical cliff/seam at the near edge (~1500,-1000). Script/terrain-doable.
2. Move igloos onto the ice/snow — the pair near (1480,-828) sit on green grass; relocate onto snow or add a snow apron under them. Script-doable.
3. Scale down the giant pine at ~(1380,-820) to match chalet height (~1/3 current); re-tile the snow-cap texture (it's blotchy). Script-doable.
4. Populate the lake — add ~4–6 more fishing shanties + ~6–8 fishing holes spread across (1490,-1080) ±70; it's nearly empty for a "huge" lake. Script-doable.
5. Add ice-surface detail — cracks/hole decals + a few snow drifts on the Ice material. Script-doable.
6. Remove or ground the floating rock islands above the lake near (1550,-1100). Script-doable.
7. Re-seat pines that float on the slope SW of the village (~1600,-900). Script-doable.
8. Soften the harsh terrain shadow seam across the ledge at ~(1600,-880). Lighting/terrain-doable.
- **Blender later:** proper igloo + shanty meshes, detailed chalet kit.

## Top cross-area priorities
1. Floating alpine ice lake (1490,-1080) — most visible defect.
2. Giant broken-scale pine (1380,-820).
3. Graveyard sunny-meadow look (-238,246).
4. Empty capital castle bailey (0,-2140).
5. Empty Town 1 exterior SE field (297,±).
