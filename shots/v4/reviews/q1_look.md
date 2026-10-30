# Q1 Look-Check — Island Environment Review

## Per-photo
- **q00_topdown**: Whole island readable; capital grid, skull-town, south farms, NE snow dome, SE badlands, elf area all present. Sea reads flat cyan-blue, no depth gradient. Bug: foliage sprites floating in open water far offshore (small green blobs ~(±2600,0,±1600)). Island reads as a flat green blanket — biomes not separated by value like the reference.
- **q01_overview_south**: Good biome layout, towns legible. Horizon sea is a hard flat band (pale cyan) with a visible seam where water meets skybox at ~Z −3000. Green is uniform and over-bright; no aerial haze on distant north ridge so depth is lost.
- **q05_ne_river_mouth**: NE cliffs/snow. Snow is pure flat white, no shading — reads as paper. Faceted low-poly cliff normals very harsh. Bug: floating grass-topped rock island hovering above sea at ~(2900,180,−1500); another floating islet right edge ~(3200,120,−1700). River mouth not visible as water feature.
- **q02_south_coast**: South beach + offshore islet. Beach sand band is clean; water near shore shows a flat darker blotch (no gradient, looks like a texture patch) ~(300,0,1500). Sky fog soft and pleasant here. Islet tree trunks look slightly rootless.
- **q03_se_beach**: Almost entirely open sea + one tiny rock stack ~(2900,10,1500). Sea surface tiles visibly (repeating speckle pattern), no depth darkening toward deep water. Confirms sea is the weakest element.
- **q04_west_cliffs**: Forest on cliffs. Bug: THREE large flat grey slab prisms in foreground (~(-2600,60,-300) and either side) — untextured placeholder/clipping mesh, z-fight flat shading. Trees good density. Distant peaks have no haze.
- **q06_country_mid**: Dense forest toward snow peak. Grass now nicely green/saturated; autumn (orange) trees read well. Mountain is flat grey faceted, no snow shading. Sky clear — atmosphere improved here.

## Scores (/10)
- **Sea colour & depth gradient — 4**: deep blue is better than before but totally uniform, no shallow→deep gradient, tiles visibly.
- **Shoreline (foam/beach) — 5**: beaches read; no foam/surf line at all, shore edge is a hard cut.
- **Fog & atmosphere — 6**: clearer and prettier than last pass; still NO aerial perspective on distant ridges, so depth is flat.
- **Grass & ground saturation — 7**: biggest win — greens and warm ground now read; slightly cartoon-bright but good.
- **Roads readable from above — 4**: faint tan lines only; capital grid reads, rural roads nearly invisible in q00/q01.
- **Overall resemblance to reference — 4**: layout matches, but finish is flat/toy-like vs reference's value-separated, hazy, deep-water painterly look.
- **Whole-island readable in q00/q01 — 6**: yes, all biomes present and none cut off; but hard sea seam at horizon and offshore floating sprites hurt it.

## Top 8 fixes (ranked)
1. Add sea depth gradient: WaterTransparency 0.74 -> 0.60 AND darken deep-water terrain water colour to ~(10,40,78); keeps shallows lighter for a gradient.
2. Remove floating objects: delete grass-rock islets ~(2900,180,-1500) & ~(3200,120,-1700), and offshore foliage sprites in q00.
3. Delete/retexture the 3 grey slab prisms at ~(-2600,60,-300) in q04 (placeholder meshes, flat grey z-fighting).
4. Add aerial haze for depth: Atmosphere.Density 0.20 -> 0.14, Haze 0.8 -> 1.6, Color tint toward (200,215,235) so distant ridges recede.
5. Shade the snow: snow Terrain colour (255,255,255) -> (224,230,238) and add subtle ambient occlusion / lower Studio AO; pure white reads as paper.
6. Strengthen roads from above: road colour -> (176,150,112) and widen 1.4x, or decal paths, so q00/q01 rural roads read.
7. Fix the horizon seam: raise skybox/ocean blend — Lighting FogEnd push + match skybox lower band to sea (14,62,104) so q01 band disappears.
8. Break grass uniformity: add 10-15% colour variation / darker Grass in shade (base (70,120,55), shaded (52,92,44)) to stop the flat-blanket look from above.

Unavailable this session: @Roblox_Studio MCP (not configured) — review done from photos only, no Studio tools used.
