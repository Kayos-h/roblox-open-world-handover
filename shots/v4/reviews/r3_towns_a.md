# Round 3 review -- Capital, Castle, Alpine village + Ice lake, Town 1

Reviewer: senior art director. Tools unavailable this session: @Roblox_Studio (not configured) -- judged from photos only, as required.

## Capital -- 6/10
The tabletop seam is MOSTLY gone from the air (t01): the surrounding land now rolls and is wooded, no razor pad edge against the walls, and interior trees/beds break up the rooftops. Big remaining problem is colour: roofs are a near-uniform navy-and-red checkerboard with almost no roof-material or hue variety, so from the air it reads as repeated stamped houses rather than an organic medieval capital. The ground-level wall-base planting (t02) worked in principle -- bushes, grass and a rock sit against the west wall -- but the shot is swallowed by one giant foreground grass blade clump; the grass instances are far too tall (chest-high on a building) and too few/too sparse to read as a planted bed. The wall itself is clean white with blue cone turrets, matching the castle, good.

## Castle -- 7/10
Strongest area. Tabletop seam gone (t03): walls sit on sloped wooded ground with pines and boulders outside, terrain reads naturally. Courtyard is now ALIVE (t03/t04): lawns on both flanks of the paved central plaza, market stalls, banners (deep blue + one red), lamp posts, a central fountain, benches, trees, a gazebo. The gatehouse axis (t04) is a genuine processional view -- banners framing the paved avenue to the fountain and castle keep. The keep itself (blue conical spires, white stone) matches the target. Weaknesses: the double row of banners in t04 is over-dense and repetitive (same navy banner ~10x), and the paving is a flat single-tone tan with no wear/joint variation.

## Castle training yard -- 5/10
It reads, but only just (t05). Straw dummies, a weapon rack and what look like targets are present along the back fence, but they are pushed to the rear and half-hidden; a PINK picket fence and a green-and-yellow striped stall canopy dominate the foreground and fight the martial theme badly. Grass instances here are again far too tall -- they bury the dummies' legs and the fence. The gazebo and flower arch belong to a garden, not a training yard; the space reads more like a fete than a drill ground.

## Alpine village -- 7/10
Good improvement. Chalets no longer sit on bright green (t06/t07): there is a real snow band with a ragged lower edge bleeding into the green treeline, snow-laden pines, and the mountain wall behind reads as rock with snow pockets. Market square (t07) is characterful -- timber chalets, bunting, awned stalls, barrels, a stone well. Concerns: the snow is a very flat, pure near-white with little shading/ambient occlusion, so large areas look like blank paper; the transition rock/snow boulders are fine but the terrain mesh is visibly low-poly/faceted (t06, t08).

## Ice lake -- 6/10
The new rim worked partially (t08): ice blocks, boulders and snow pines ring a pale-blue frozen pool, and the V4 igloos (rounded white domes, lower right) are believable and clearly better than placeholders. But the lake surface is a flat uniform pale cyan slab with a hard straight edge in places -- it does not read as ice (no cracks, no translucency, no thickness) and sits slightly proud of the snow like a painted plate. The scattered shanties/huts are a bit sparse and randomly oriented.

## Town 1 (skull town) -- 7/10 (original town, touch lightly)
Tower roofs are FIXED (t17/t18/t19): the cobalt is clearly desaturated to a muted slate-blue; no longer the glowing over-saturated blue of prior rounds. Keep this. The skull apron ring of bushes and rocks (t18) is present and softens the tan plaza edge. The ochre church (t19) and half-timber houses read well. The plaza statue/fountain and banners (t17) are tidy. Main residual issue is the same over-tall grass instances swamping the foreground of t17 and t18.

## BUGS
- **Floating terrain block**, alpine, ~(1500,210,-1050): a detached grey rock cube hangs in mid-air against the mountain face in t08 (upper-left), clear black-shadowed void beneath it. Also a similar floating slab in t07 upper-right. Delete or ground these.
- **"Back" UI gizmo / move handle** visible in-world in t04, t05, t07, t08, t18, t19 (small labelled widget mid-sky). Editor selection artifact -- deselect before final renders; not a world bug but will spook players if shipped.
- **Grass instance scale bug** (all ground shots: t02, t05, t17, t18): grass blades are ~4-8 studs tall, taller than fences and burying props. Reduce grass model height to ~1-1.5 studs.
- **Ice lake edge z-seam**, ~(1450,139,-1120): lake surface meets snow in a hard straight line with a slight lip (t08), reads as a floating plate.
- No black voids, no objects-inside-buildings, no shoreline tears seen in these shots.

## KEEP
- Castle courtyard dressing and gatehouse processional axis (t03/t04).
- Alpine snow band with ragged treeline edge (t06).
- Town 1 desaturated tower roofs (t17/t18) -- do not re-saturate.
- V4 igloo domes at the ice lake (t08).
- Capital/castle natural wooded surround -- tabletop seam genuinely gone.

## FIX LIST (ranked, payoff per effort)
1. **Shrink grass instances** everywhere to ~1-1.5 studs tall (cheap, global material/model edit). Biggest single quality jump -- every ground shot is currently ruined by giant blades.
2. **Deselect editor gizmos** / hide the "Back" widget before renders (free).
3. **Vary capital roof colours** -- add 3-4 extra roof hues (terracotta, grey slate, weathered brown, teal) and break the navy/red checkerboard (cheap colour edit, high aerial payoff).
4. **Fix floating alpine rock cubes** at ~(1500,210,-1050) and ~(1750,250,-650) -- ground or delete (cheap object edit).
5. **Re-theme the training yard** (t05): remove pink fence + striped garden stall + gazebo + flower arch; bring dummies/targets/racks forward onto a dirt/sand pad, add a small weapon tent (cheap object moves).
6. **Shade the alpine snow** -- drop snow colour ~10% toward (225,232,240) and add subtle ambient occlusion so it stops reading as blank paper (cheap colour edit).
7. **Treat the ice lake surface** -- add a faint crack decal / slight transparency / tint banding so it reads as ice not a cyan slab, and soften the straight rim (cheap material/decal edit).
8. **Thin the castle gatehouse banner rows** (t04) from ~10 repeats to ~4 and alternate blue/red (cheap).
9. **Add paving joint/wear variation** to castle plaza and skull-town plaza so the tan isn't one flat tone (cheap texture/colour edit).
10. **Add more wall-base planting density** at the capital west wall (t02) -- current bed is too sparse once grass is shrunk (cheap object edit).
11. **Vary alpine shanty orientation/spacing** slightly at the ice lake so they don't read as randomly dropped (cheap).
12. None of my area's fixes need new terrain generation except the floating-cube cleanup, which is object-level.

## Player verdict
A typical Roblox player would rate my area ~7/10 today -- the castle and alpine village look finished and inviting. The single change that would raise it most is **shrinking the grass instances**: oversized grass currently wrecks every ground-level view and makes polished areas look buggy.
