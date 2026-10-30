# Round 4 review — Towns B (ELF VILLAGE priority, harbour inland, rusty huts)

Reviewer B. MCP note: `@Roblox_Studio` server was NOT configured/available this session; review is from the supplied photos only, no Studio tool used.

## ELF VILLAGE — score 7.0 / 10 (was 5.5)

Big jump. It is no longer dark, dead or black. The valley is bright, the lawn is dressed, the trunk reads as wood. But the one feature that is supposed to define the whole area — the waterfall — is broken, and that caps the score hard.

### Round-3 fault checklist (fixed / partly / not)
- Too dark (mean brightness 70): **FIXED.** Daylight is clean and even; grass, bark and flowers all read. Arguably slightly over-corrected — the lawn is a flat uniform lime with no shadow grounding.
- World tree trunk crushed to black: **FIXED.** Bark is mid-brown (t_elf_tree_base), legible all the way up.
- Valley-wide canopy shadow: **FIXED.** No giant shadow disk; soft light everywhere.
- No waterfall visible: **NOT FIXED — regressed into a bug.** What stands at (-1655,-742) is a flat vertical dark-blue ROCK slab (t_elf_waterfall): a frozen cardboard cutout with zero motion, no white plunge, no spray, no stream feeding it, no pool churn. From the air and from the tree base (t_elf_air, t_elf_tree_base) the same slab reads as a missing-texture blue cube beside the trunk. It is the single worst thing in the valley.
- Bare lawn around tree: **FIXED.** ~180 ferns/flowers/mushrooms ring the trunk; good density near paths.
- Hard pool rims: **PARTLY.** The elf lake and moon pool now have reed/lily/rock rims (nice, t_elf_waterfall foreground), but the two round ponds in t_elf_air still have a hard geometric shoreline with a flat tan sand collar.
- Hard-edged dirt paths: **PARTLY.** Plants line the edges now, but the paths are still crisp uniform-width ribbons with a sharp dirt/grass seam (t_elf_tree_base, t_elf_air).
- Palace on a flat pad: **PARTLY.** Plaza is dressed (feathered markers, stalls) but still sits on an obvious flat white rectangular slab under the treehouse cluster (t_elf_treehouses_w).
- Loose village not a city: **PARTLY.** The west treehouse cluster now reads as a connected hamlet with bridges; the rest of the valley is still scattered single huts around a big empty lawn, not a city.

### Glow / neon / emissive audit: PASS
No glow mushrooms, no neon, no light beams, no particles, no emissive/lit glass anywhere in any of the 5 elf shots. The reference image shows a cyan glow at the tree; the build correctly omits it per the brief. Clean natural look confirmed.

### Is the waterfall a visible landmark? NO.
It is visible but reads as a glitch, not water. It is not a landmark — it actively hurts the area.

### Does the valley feel like a lush natural elf city between mountains?
Lush natural valley between mountains: YES. Elf CITY: not yet — it feels like a tree + a lawn + a few scattered houses, not a settlement.

### BUGS (elf)
- Flat dark-blue rock "waterfall" slab at ~(-1655,-742) — no water, reads as missing-texture cube from other angles.
- Same slab visible as a stray blue box at ~(-1620,-460) in t_elf_air / t_elf_tree_base.
- Hard flat tan-sand collar + geometric rim on the two round ponds, ~(-1620,-360) and ~(-1700,-520).

### KEEP (elf)
- Brightness/light balance; brown legible trunk and radial buttress roots.
- West treehouse cluster + rope bridges; the dense white/pink/blue flower beds; reed-and-lily lake rims.
- The no-glow restraint — do not add glow back.

### Top 10 remaining elf fixes (ranked)
1. Replace the flat slab with a REAL waterfall at (-1655,-742): 2-3 stacked thin white-to-pale-cyan water planes (transparency 0.3) falling down the cliff face, a white foam/spray cluster where it hits, and a visible stream running from the pool toward the tree. Highest payoff by far.
2. Delete/retexture the stray blue box near the trunk at ~(-1620,-460) — if it is the waterfall object seen edge-on, it must not be visible from the plaza.
3. Soften the two round pond rims (-1620,-360),(-1700,-520): remove the tan sand collar, feather the shoreline with reeds/rocks/moss like the elf lake already has.
4. Break the path edges: vary trail width 6-10 studs, add a 1-stud scatter of pebbles/grass tufts over the dirt/grass seam on the paths radiating from the trunk at (-1560,-430).
5. Sink the palace plaza slab into the terrain at ~(-1720,-540) or skirt it with grass/steps so it is not a floating white rectangle.
6. Add 6-10 more round houses between the tree and the palace (fill the empty lawn band around (-1560,-480)) to make it read as a city, not a clearing.
7. Vary the lawn: 2-3 darker green grass-colour patches + low ground-shadow decals under tree clusters so the flat lime plane gets depth.
8. Add canopy to the mid-valley: a few more large round trees around (-1500,-430) so the giant lawn does not feel empty from the air.
9. Dress the elf lake with a small dock/bridge or lanterns-free stone jetty at ~(-1560,-430) rim to give the pool a purpose.
10. Add a second tiny treehouse cluster on the east side ~(-1420,-450) to balance the west-heavy layout seen in t_elf_air.

All 10 are cheap object/colour edits EXCEPT #1 and #3 (waterfall + pond rims), which touch terrain/water and are medium cost. None need full terrain regen.

## HARBOUR (inland lawn) — score 8.0 / 10 (was 7.5)
Tidy, dense, convincingly a seaside town. Nine-hue roofs read well, half-timber houses are varied, lamp posts and benches give it life; lighthouse and ruined tower bracket the view nicely. Negatives: grass tufts are tall and a touch cartoonish against the neat houses; the main dirt path is a hard flat ribbon; houses sit slightly proud of the lawn in a few spots (near-foreground house at ~(-420,1560) has a visible base gap).
Three cheapest fixes:
1. Lower grass-tuft scale ~25% so blades stop swallowing door-sills.
2. Scatter cobble/pebble edge decals along the central path seam at ~(-420,1600).
3. Nudge the 2-3 proud foreground houses down ~0.5 stud to close base gaps.

## RUSTY HUTS (desert) — score 7.5 / 10 (was 7)
Clean, varied stone/plank huts with corrugated and gabled roofs; ochre church + rose window is a good anchor; banded mesas and dead trees sell the badlands. Negatives: a few huts have a noticeably pixelated/low-res wall-texture patch (green-grey hut, centre, ~(1200,1215)); hut bases meet flat sand with no sand drift or rubble skirt; roof palette is a bit samey (tan/brown only).
Three cheapest fixes:
1. Retexture the low-res green-grey hut wall at ~(1200,1215).
2. Add small sand-drift/rubble decals at 4-5 hut bases around (1180,1210) to ground them.
3. Introduce 2 more roof hues (faded teal, rust-red) across the hut cluster for variety.

## Player verdict
A typical Roblox player would give the map ~7/10 today. The single change that raises it most: make the elf waterfall a real cascading waterfall — it is the promised landmark and right now it is a blue glitch slab.

ROUND4 SCORES: elf village 7.0, harbour 8.0, rusty 7.5
