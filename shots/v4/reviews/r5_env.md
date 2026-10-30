# Round 5 review — TERRAIN & ENVIRONMENT (whole island)

Senior art-director pass, strict. 10 photos read (4 fog-off overviews, north overview, 3 ground coast/islet, 2 badlands). Reference re-read. MCP note: the `@Roblox_Studio` server was declared but NOT configured, so no Studio tools were available — this review is from the photos only, as required.

## CHANGE VERIFICATION
1. GRASS (blade length 0.7→0.3): **WORKED.** Ground shots (f_south_coast, f_islet_shoal, f_badlands) show short, sensible turf. Islet trees, coastal pines, rocks, dummies and huts all stand clear of the grass now — the chest-high problem is gone. This is the single biggest quality jump of the round.
5. SEA (far-ring recolour, lighter shelf, transp 0.82, foam rebuilt): **PARTLY.** Horizon seam is GONE — far ocean now reads as one continuous body (f_over_south, f_over_west, f_over_north). Shallows read warmer and you can see seabed near shore (f_se_beach, f_islet_shoal). BUT the open sea is a flat, glassy, uniform navy "bathtub": no depth gradient visible from the ground (f_se_beach, f_islet_shoal), and the water plane is dead-level to a hard straight far edge against the sky wall (f_over_west, f_over_north). Foam is now soft and coast-only (good), but on the ground shots there is almost no foam at the actual waterline (f_south_coast, f_se_beach) — the surf rings of the reference are missing.
6a. SNOW LINE + SCAR STRIPES: **WORKED.** NE seaward slopes are rock, not stray snow (f_quad_nw, f_over_north); the snow cap now sits high and tidy on the NE range. The orange scar stripes on mountain flanks are gone — grey rock reads clean across the interior (f_over_south, f_over_west).
6b. MESA VARIETY: **WORKED, close up.** f_badlands and f_badlands_close show genuinely varied mesas now — tall drums, squat plinths, tilted stacks, thin spires, dark basalt blocks mixed with banded sandstone. Close read is strong and characterful. Far/top-down (f_quad_se) they still read as a field of similar pale discs, but the silhouette variety is real on the ground.

## SCORES (round 4 → round 5)
- **Sea 6 → 7.** Seam fixed, shallows readable, foam softened. Held back by the flat glassy open-water with no visible gradient and no shoreline surf.
- **Landforms 7 → 8.** Snow line and scars fixed; coastline cliffs and bays read natural; mesas varied. Clean, believable island form (f_over_west, f_over_north).
- **Forest 7 → 7.** Dense, tint-varied canopy with autumn flecks (f_over_west). Still slightly even/carpet-like from above and a touch too uniformly bright-green; no change needed but no gain.
- **Rivers & lakes 6 → 6.** East river and interior ponds read fine from above (f_quad_se, f_over_south). Lake water is the same flat blue as sea with hard edges; no bank/shallow treatment. Unchanged.
- **Readability from above 7 → 8.** Quadrant shots show a clear tan road web linking settlements, distinct biomes (green / snow / badlands) and legible town footprints. Very close to the reference's legibility.
- **Badlands 5 → 7.** Mesa variety and banding now genuinely good close up; biome edge against grass is ragged and natural (f_quad_se). Dragged down by the water bug below.

## BUGS
- **Floating rock**, badlands beach, approx **(1850, 95, 1050)** — a dark boulder hovers ~40 studs above the mesas (f_badlands_close, upper centre). Clear z-float.
- **Brown voids inside the water plane**, badlands south shore, approx **(1700–2000, 0, 1150)** — several dark brown holes ringed with white foam sit IN the blue water (f_badlands_close, foreground). These read as terrain holes / leftover seabed voxels showing through a too-dark shallow, or decals punched in the water. Looks broken; most eye-catching defect in the set.
- **Hard flat sea edge / sky wall seam**, whole far horizon, e.g. **(−4300…, 0, −200)** westward (f_over_west, f_over_north) — the ocean ends in a dead-straight line against the sky dome. Less jarring than before but still artificial from a distance.
- **Islet rock plinths read as stacked grey blocks**, e.g. SE islet approx **(469, 5, 2359)** and the stack right of it (f_islet_shoal) — plinths are solid now (good, not floating) but are blocky untextured columns, not rock.

## KEEP (do not touch)
- Grass length 0.3 — perfect, leave it.
- Snow cap placement and the de-scarred grey rock flanks.
- Mesa close-up variety and banding (f_badlands_close).
- Road web + biome legibility in the quadrant shots.
- Autumn/yellow-green leaf tint flecks in the canopy.
- Ragged badlands/grass biome border.

## RANKED FIX LIST (max 12; cheap unless noted)
1. **Fill the brown voids in the badlands shore water** near (1700–2000, 0, 1150): delete the leftover seabed voxels / holes under the shallow so the water reads solid. CHEAP terrain paint, high payoff — kills the worst bug. (small terrain edit)
2. **Delete the floating rock** at ~(1850, 95, 1050). Cheap object edit.
3. **Add shoreline surf foam** at the actual waterline on the main coasts (thin soft white band, follow the beach, ~15–25 studs). The reference's signature is surf rings; ground shots currently have none. Cheap decal/part edit.
4. **Give open water a visible depth gradient** from the ground: darker toward deep, lighter teal near shore (the top-down ramp isn't visible at eye level). Lower water transparency slightly offshore or add a subtle colour falloff. Cheap colour edit.
5. **Texture the islet/stack plinths** with rock material and taper them, so they stop reading as grey Lego columns (f_islet_shoal). Cheap material/colour edit.
6. **Break up the far-sea horizon line** with light far haze / a lower, softer sky-sea blend so the straight bathtub edge is less obvious from altitude. Cheap lighting/fog edit.
7. **Vary mesa top colour/size top-down** — add a few darker basalt caps and height spread so the badlands aren't a field of pale discs from above (f_quad_se). Cheap object recolour/scale.
8. **Soften lake edges** — add a thin sand/shallow collar to interior ponds and the east river so they aren't hard blue cut-outs. Cheap terrain paint.
9. Scatter a few more coastal rocks/driftwood on the long empty beaches (f_se_beach) to break the plain sand. Cheap object scatter.
10. Add faint snow dusting lower on the shaded NE faces so the snow-to-rock transition is a gradient, not a hard line (optional; EXPENSIVE if regen).

## PLAYER VERDICT
A typical Roblox player would give this map about **7.5/10** today — it reads as a real, lush, legible fantasy island with clear biomes and good ground-level scale. The single change that would raise it most: **fix the brown holes in the badlands shore water** (fix #1) — it's the one thing that currently looks plainly broken.

ROUND5 SCORES: sea 7, landforms 8, forest 7, rivers and lakes 6, readability from above 8, badlands 7

VERDICT: SHIP (first-playable quality — one real bug remains but it is localised and cheap).
Next 5 cheap changes (≤30 min): (1) paint out the brown water voids at ~(1700–2000,0,1150); (2) delete the floating rock at ~(1850,95,1050); (3) add a thin soft surf-foam band at the main shoreline waterline; (4) add a subtle offshore depth-colour falloff to the open water; (5) re-texture the islet/stack plinths to rock + taper.
