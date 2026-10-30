# Round 2 Visual Review — Reviewer A

MCP note: the `@Roblox_Studio` server was not configured/available this session. Review done read-only from the 9 jpgs; no Studio access.

## Per-picture

**t01 gy_inside — 8/10.** Dense graveyard: ~20+ Celtic crosses, headstones, two dead trees, a candelabra, lanterns, flower clusters, stone mist hanging low. Ground is now brown mud with patchy grass. Round-1 "sunny meadow, sparse graves" — **fixed**. New defects: grass patches still bright lime-green and read as untextured blobs between graves (center/foreground); a couple of headstones sit at slight tilts that look accidental not weathered; candles cluster a bit repetitively lower-left.

**t02 gy_high — 7/10.** From the wall the graveyard reads as a proper dense dark plot inside the bailey, mist visible. **Fixed.** New: the mud patch has a hard rectangular edge against surrounding green lawn (visible seam where mud zone stops ~x-186/z-204 side); graves crowd right up to the church wall with little spacing.

**t03 igloos — 6/10.** Alpine chalets with snow roofs, icicles, stone bases, snow ground. Round-1 "igloos on green grass" — **partly fixed** (ground is snow now) BUT a bright green grass tuft pokes through the snow bottom-center (clipping), and the chalets shown are log cabins, not igloos — if igloos were intended they aren't in frame. Camera is very close to one wall; hard to judge spread.

**t04 ice_camp — 7/10.** Good: colored shanties (red/blue/green), fishing holes ringed with ice blocks, sled, boat, boulders, snow spires, mist. **Fixed** under-population. New defects: the green shanty center has no snow cap while all others do — inconsistent; fishing holes bottom-right are a repeated identical ring stamp; one shanty (blue, left) has a visible icicle fringe floating slightly below its floor edge (hovering over ice).

**t05 ice_wide — 6/10.** Populated and varied. But serious defect: **large rock boulders are FLOATING** — several rocks hang in mid-air above the ice (center and the whole top band of 6–8 rocks floating against the sky). The big foreground boulders also sit on the ice with no snow skirt, looking pasted on. Repetitive snowy-pine instances. Fixed population, but floating rocks drop the score.

**t06 rim_wall — 7/10.** The 30-stud step now has a rock cliff face, snow shelf on top, pines framing, buildings/lantern at the lip. Round-1 "floating rim / cut" — **partly fixed**: it reads as a cliff rather than a floating slab now, but the transition from grey rock to the flat snow lip is abrupt and the rock face is a plain flat quad with little depth — still slightly cut-looking. Pines clip into frame edges heavily (foliage planes overlap).

**t07 castle_high — 8/10.** Strong: fountain, ring of lamps, blue banners on the axis, knight statues, striped market stalls, barrels, hedge gardens flanking. Round-1 "empty bailey" — **fixed**. New: banners stand as flat vertical slabs with no pole/cloth read (look like blue boards); a few lamp posts are very densely packed near the fountain (clutter); statues are a uniform bronze repeat.

**t08 castle_close — 7/10.** Barracks/stable yard: barrels, hay bales, benches, a blue+gold wagon, net/crates, obelisk, hedges. **Fixed.** New defects: hay bales are strewn in a scattered line that reads as random clutter blocking the open yard; wagon sits isolated mid-plaza; ground is bare sand with no path definition.

**t09 elf_tree — 7/10.** Base paths now sandstone (no blow-out), glow mushrooms/ferns/crystals, palms, distant crystal palace and an arch. Round-1 "stray white parts, blown paths" — **fixed**. New: a grey crate/box and a yellow wedge sit at the tree root foreground clipping into the trunk flare (left + center-low); white path-edge borders are still bright and a touch glowy; mushroom props repeat identically.

## Per-area scores & prioritised fixes

**Town 1 Graveyard — 7.5/10**
1. Soften mud/grass boundary: feather terrain paint from bright-green to mud over ~x -186..-260, z 204..288 (no hard rectangle).
2. Dim/retexture the lime grass tufts between graves to a muted dead-grass green.
3. Add 6–10 stud spacing between graves and the church wall (~x -200, z 240).
4. Reduce candle count lower-left (~x -205, z 250); vary placement.
5. Normalise headstone tilts to ±3°.

**Alpine (igloos + ice lake) — 6.5/10**
1. **Drop all floating rocks onto the ice** at y≈152 across the lake (~x 1440..1540, z -1000..-1100) — biggest issue.
2. Remove the green grass tuft clipping through snow near camera (~x 1500, z -810).
3. Give the floating/skirtless boulders a snow base ring (small white parts at contact y≈152).
4. Add a snow roof cap to the green shanty (~x 1490, z -1050) for consistency.
5. De-duplicate the stamped fishing-hole rings (~x 1500, z -1060); vary radius/rotation.

**Castle — 7.5/10**
1. Rebuild banners as pole + thin cloth instead of flat blue slabs (axis z ≈ -2150..-2300, x 0).
2. Thin the lamp cluster around the fountain (~x 0, z -2200) to even spacing.
3. Tidy hay bales in the stable yard into stacks against a wall (~x 120, z -2080), clear the center.
4. Paint a stone path from stairs to fountain (axis x 0).
5. Vary the 8 knight statues (pose/material) to break the bronze repeat.

**Elf — 7.5/10**
1. Remove/relocate the grey crate and yellow wedge clipping the trunk base (~x -1555, z -430).
2. Reduce glow/emissive on white path borders around the tree (~x -1560, z -430).
3. Randomise glow-mushroom scale/rotation to kill the repeat.
4. Add subtle root-to-ground blend parts where the trunk flare meets grass.
5. Space palms irregularly to avoid grid feel.
