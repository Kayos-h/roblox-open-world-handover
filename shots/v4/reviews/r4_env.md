# Round 4 review — ENVIRONMENT / TERRAIN (whole island)

Reviewer: terrain & environment. Scale matches r3 reviewers. MCP note: `@Roblox_Studio` server was not configured this session; review done from photos only, no Studio tools used (none were needed).

## Special checks (answered)
1. **Sea gradient & foam.** Deep blue — WORKED. The cyan is gone; near-shore reads a proper deep royal/navy. But there is still **no visible shallow-to-deep gradient**: the water is one flat blue slab right up to the sand (g_south_coast, g_se_beach, g_islet_shoal). The seabed ramp exists on paper but transparency 0.75 + flat lighting hides it, so shallows never turn turquoise. Foam: the wide soft translucent surf band is natural now (g_south_coast far shore) — WORKED — **except** the near islet in g_south_coast still wears the old hard faceted octagon foam outline around its beach. Partly fixed.
2. **Hovering islets / floating.** FIXED. 27 islets/stacks now have solid rock plinths down to the sea floor (g_islet_shoal, g_ne_river_mouth, h_overview_east). No hovering sand plates, no floating props found in any shot.
3. **Horizon seam.** NOT gone. The far-sea ring still reads as a flat lighter-blue plate with a hard straight edge: obvious in h_overview_south (top of frame, a ruled line sea-vs-sky and sea-vs-ring), and as a dark band across g_se_beach and g_ne_river_mouth. The 13000-stud ring extended the water but did not blend it — the seam just moved outward.
4. **Road web & rivers (quadrants).** Road web READABLE and matches the reference layout — tan trunk roads radiate from the Town-1 hub, capital grid (q_nw), harbour star-junction (q_sw), spurs to badlands & alpine (q_ne/q_se). Trunk roads are the right warm limestone; dirt ring roads are thinner and fainter but present. Rivers VISIBLE: blue ribbons in q_nw (north-central), q_sw (winding SW + lake chain), and the SE lake string (q_se). Good against reference, though the river network is thinner/shorter than the reference's long east-coast river.
5. **Forest & grass.** Forest variety GOOD now — deciduous rounds in three tints (dark green / yellow-green / autumn orange), spruces and pines mixed, random scale reads (g_country_mid, g_country_road). Grass height FIXED: short at ground level, no more chest-high tufts.
6. **Badlands mesas.** Variety still WEAK — see below.

## Scores
- **Sea & water — 6/10** (was 4). Colour fixed, foam softened, plinths fixed. Held back by the flat no-gradient shallows, the surviving octagon foam ring on some islets, and the horizon seam.
- **Landforms — 7/10** (was 7). Island silhouette is round and convincing; west craggy coast and NE snow range read well (h_overview_west/east). Badlands shape drags it; orange dirt scar-stripes on some mountains (g_country_mid bg) look painted-on.
- **Forest — 7/10** (was 5). Big jump: tint + scale + species variety now look like a real wood.
- **Rivers & lakes — 6/10** (was 5). Visible and blue, read from above; still sparse vs reference and some lakes are plain flat discs.
- **Readability from above — 7/10** (was 5). Quadrant resolution finally shows the road web and settlements clearly; biome borders ragged and legible.
- **Badlands — 5/10.** The 44 mesas are near-identical flat-topped circular layer-cake discs with red/white banding, same radius and tier count, tiled across the SE (q_se, h_overview_east, g_badlands). Reads cartoonish, not eroded rock. Tilt/sink helped the overview a little but ground level exposes the repetition.

## BUGS
- **Horizon seam** — far-sea ring edge, full perimeter ~13000 studs out; most visible north edge (0,0,-7000+) in h_overview_south and the dark band in g_se_beach / g_ne_river_mouth.
- **Faceted foam octagon** on the near islet ~ (300,0,1900) in g_south_coast — old hard polygon surf outline, not the new soft band.
- **No river at the "NE river mouth"** — g_ne_river_mouth (looking to ~2700,0,-1350) shows snow cliff meeting sea with no actual watercourse reaching the coast; the river in the reference's NE doesn't arrive at the shore here.
- **Snow reaches near sea level** on the NE seaward slope (g_ne_river_mouth, ~2700,100,-1200) — snowline dips almost to the beach, looks wrong beside green lowland just south.
- **Orange dirt scar stripes** banding mountain flanks (g_country_mid bg, ~ -200,250,-700) look like painted texture bands rather than erosion.
No black voids, z-fighting, terrain tears, or objects-inside-buildings found in the environment shots.

## KEEP
- Deep blue sea colour and soft wide surf band (g_south_coast far shore).
- Islet rock plinths — do not revert.
- Forest tint/scale/species mix (g_country_mid, g_country_road).
- Short ground grass.
- Trunk-road width/colour and trees-cleared-off-roads (g_country_road).
- Round island silhouette and NE snow range (h_overview_west/east).

## FIX LIST (ranked, highest payoff first)
1. **Kill the horizon seam.** Fade the far-sea ring into fog/sky at its outer edge or match its colour+material exactly to the near sea; better, extend the near-sea water plane itself instead of a separate ring. Cheap-ish (water/part edit), huge payoff — it's the one thing breaking every fog-off wide shot.
2. **Regenerate the badlands with varied mesas.** Replace the uniform discs with mixed-radius, mixed-height, non-circular eroded forms (buttes, fins, talus slopes); vary band count and break the flat tops. **Needs terrain regeneration.** Biggest ground-level quality gap.
3. **Make shallows read turquoise.** Add a true shallow water band (lower transparency / lighter colour over the sand shelf) so the sand→turquoise→blue ramp is actually visible from shore. **Terrain/seabed + water tweak.**
4. **Replace the faceted octagon foam rings** on islets with the new soft surf-band decal so every shoal matches g_south_coast's far shore. Cheap (prop/decal swap).
5. **Raise the NE snowline** so snow stops well above the coast; regrow green/forest on the lower NE seaward slope. **Needs terrain paint regeneration** (localized).
6. **Add the missing NE coastal river** (or re-route the existing NE river to reach the sea) to match the reference's prominent east-coast river. **Terrain carve + water.**
7. **Remove/soften the orange dirt scar stripes** on mountain flanks; blend with rock or thin them. Cheap terrain-paint edit.
8. **Thicken/extend the river & lake network** — longer rivers, a few irregular lake shapes instead of flat discs, reed rims. **Partly terrain.**
9. **Vary lake shapes** — the perfectly round blue discs (q_sw, q_se) look stamped; irregular edges. Cheap-ish terrain-paint.
10. **Dapple the open sea surface** — a subtle normal/colour break so the ocean isn't one flat sheet in ground shots (g_se_beach). Cheap water-material tweak.

Needs terrain regeneration: #2, #3 (seabed), #5, #6, and partly #8/#9. Cheap object/colour edits: #1 (water part), #4, #7, #10.

## Player verdict
A typical Roblox player would give the environment **7/10** today — the island reads lush, varied and believable at a glance, and the water finally looks like an ocean. The single change that would raise it most: **remove the horizon seam** in wide views; the badlands regen is the close second for anyone who walks the SE.

ROUND4 SCORES: sea 6, landforms 7, forest 7, rivers and lakes 6, readability from above 7 (player verdict 7/10)
