# Round 4 review — Towns A (Capital, Castle, Alpine, Ice Lake, Town 1)

MCP note: `@Roblox_Studio` server was not configured this session; review done purely from the r4 photos. No Studio tool was needed.

Headline: the colour work on roofs and banners landed well, but the claimed grass rescale did NOT take at ground level — every ground shot still has chest-high blades. That is the single biggest drag on four of these five areas.

## CAPITAL — 7/10 (was 6)
Checkerboard navy-and-red is gone (special check 1: WORKED). Roofs now read as a warm, varied mix — terracotta, slate-blue, green, cream, plum — and the hue spread is pleasant, not chaotic; it genuinely looks like a lived-in medieval capital from the air. Blue spire church and the gold-domed rotunda give good landmarks. Still a touch too many dark navy half-timber facades on the south/east blocks, but nowhere near the old problem. Aerial shot has no floating plates.
Cheapest 3 fixes:
1. Thin ~20% of the navy-timber houses to brown/ochre timber so no block reads cold-blue — pure material swap.
2. Add 2-3 market-stall colour clusters along the main avenue for warmth — cheap object placement.
3. Nudge wall-base planting denser on the west curtain (bare at ~(-550,1450)) — cheap beds.

## CASTLE COURTYARD — 7/10 (was 7)
Clean, grand, well-dressed: lamp rows, central fountain, benches, stalls tucked at the flanks, amber-paned wings. Banner rows are NOT overly repetitive now (special check 4: FIXED) — only two large banners frame the avenue, rhythm is fine. Lamp posts are the one repetition risk: a long identical double row. Cobble plaza reads well.
Cheapest 3 fixes:
1. Break the lamp row — remove every 3rd lamp or swap some for braziers/bollards — cheap delete/swap.
2. Add a few figures/guards or a carriage for scale and life — cheap objects.
3. Tiny potted greenery between lamps to soften the stone expanse — cheap beds.

## CASTLE TRAINING YARD — 5/10 (was 5) — did NOT move
Dark-wood fence and pink/striped-stall removal DID land. But it still does NOT read as a drill ground (special check 3: NOT WORKED). The grass INSIDE the fenced pen is as tall as everywhere else, swallowing the dummies — only their heads poke out, so from here it looks like an overgrown garden plot with a gazebo, not a training yard. The gazebo + arbour + arch on the far edge read as a wedding garden, wrong tone for a drill yard.
Cheapest 3 fixes:
1. Paint the pen interior as dirt/packed-earth material and kill grass decoration inside the fence — this alone makes it read as a drill ground. Cheap.
2. Raise the dummies/targets or lower the grass so they clear the blades — cheap scale.
3. Swap the gazebo/floral arch for a weapon rack, hay bales and a sparring ring — cheap object swap.

## ALPINE VILLAGE — 7/10 (was 7)
Best-looking ground shot of the set. Snow cobble square, snow-capped cabins, bunting, two colourful stalls, snow pines, grey crags behind — cohesive winter-market mood, no tall-grass problem (snow floor). Stalls are a little clustered dead-centre; left side is emptier.
Cheapest 3 fixes:
1. Spread one stall + a barrel group to the left foreground to balance — cheap move.
2. Footprint/track decals in the snow around the stalls for wear — cheap decals.
3. A lamp or two lit (warm) to lift the cool palette — cheap.

## ICE LAKE — 6/10 (was 6) — did NOT move
Surface DOES read as ice now — pale blue-white Glacier mottling, believable (special check 5: partly WORKED). But two problems keep it flat: (a) no hard straight rim, good, yet the ice-to-snow boundary is mushy and the igloos/shanties sit ON the ice with no shore transition; (b) a clear BUG — a grey rock/wall slab FLOATS mid-air against the cliff at approx world (1600,205,-1020), upper-left of frame. Scene is also busy/scattered — pines, shanties, igloos, crates strewn without a centre.
Cheapest 3 fixes:
1. Delete/re-seat the floating grey slab at ~(1600,205,-1020) — cheap, it's the one real bug.
2. Add a ring of ice-chunk/snow-bank blocks where ice meets snow so the lake has a defined edge — cheap objects.
3. Cluster the fishing holes + shanties into one readable camp instead of scattering — cheap re-placement.

## TOWN 1 (skull town) — 7/10 (was 7) — judged lightly (user's original)
Plaza is characterful: hero statue, ornate red-and-gold banners, lamps, benches, café tables, half-timber houses, the big white skull landmark behind. Good identity. Only issue shared with the rest: foreground grass is chest-high in both shots, burying the low bushes and the skull-apron base. The skull itself reads well and sits on the ground cleanly (no float).
Cheapest 3 fixes:
1. Apply the ground-grass rescale here too (see global fix) — the plaza lawn is swallowing its own dressing.
2. A short dirt/paved path connecting the skull apron to the plaza (currently grass gap) — cheap path.
3. One or two hanging signs/market colour near the houses for depth — cheap objects.

## BUGS
- Floating grey slab at ice lake, approx world (1600,205,-1020) — hovers against the cliff face.
- GLOBAL: grass decoration scale did NOT apply at ground level (claimed 40-50% rescale not visible). Blades are chest-to-shoulder height in `t_capital_wall_west`, `t_castle_yard`, `t_t1_plaza`, `t_t1_skull`. This is the dominant flaw of the round.
- No terrain tears, black voids, z-fighting or wrong-colour roofs found in this area.

## KEEP
- Capital's new nine-hue roof mix — this is the round's best win, do not touch.
- Castle banner thinning (two framing banners, not rows).
- Alpine winter-market composition and palette.
- Ice surface material (Glacier mottling reads as ice).
- Town 1 plaza statue + red/gold banner identity.

## Special checks summary
(1) Capital checkerboard GONE, hue mix pleasant — WORKED. (2) Grass sensibly small at ground level — NOT WORKED, still chest-high in all ground shots. (3) Training yard reads as drill ground — NOT WORKED (grass buries dummies, floral props wrong tone). (4) Courtyard banner rows repetitive — FIXED. (5) Ice reads as ice — WORKED; no hard rim/plate, but one floating slab. (6) Town 1 judged lightly — solid, same grass issue.

Player verdict: a typical Roblox player would give this cluster ~7/10 today; the single highest-payoff change is to actually push the ground-grass decoration down to ~40% everywhere (one global decoration scale), which instantly fixes the training yard and lifts every ground-level town shot.

ROUND4 SCORES: Capital 7, castle 7, castle yard 5, alpine 7, ice lake 6, Town 1 7
