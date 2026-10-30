# Map Visual Review — Round 3

## Per-screenshot notes

### u01_overview (cam 0,1700,2300 → 0,0,-200) — 6/10
Whole island read much cleaner than round 1. Haze is gone; districts and the grey massif (NE) are now distinct. Capital walls (centre-north), windmill/stone tower (centre), rusty brown patch (SE), scattered villages (south/SW). Defects: the rusty town's ground is now mottled brown/tan but reads as one flat, oddly circular blob pasted on green — edge is a hard colour seam, not a terrain blend. Two perfectly round ponds (centre) look stamped. Island coastline is smooth and uniform. No floating rock seen at this range.

### u02_tower_south (cam 1380,210,-450 → 1380,200,-1300) — 7/10
Solid mountain mass, good snow caps, no floating slabs. Alpine village and pines sit believably. Defect: a large flat diagonal rock face mid-mountain still shows a gridded checker texture seam (around x1380–1480, y~260, z~-1000) — unnatural straight-edged panel. Lower-right cliff edge below the village is a hard straight drop.

### u03_ice_wide (cam 1440,175,-1010 → 1520,152,-1100) — 6.5/10
Ground-level: solid boulders with slate/basalt speckle sit well in snow. Defect: a small dark navy-blue blob on the snow (foreground, ~x1460,z-1080) looks like a stray mis-coloured part. A couple of tiny white part fragments scatter on the snow (lower-centre) — debris. Cliff behind is solid but very steep/straight.

### u04_rusty_huts (cam 1170,22,1130 → 1182,12,1165) — 6/10
Huts now have corner posts, plank courses, a small window gap and a tiled roof overhang — real improvement over flat boxes. Grass tufts and a sandstone wall patch add variety. Defects: huts are identical and lined in a rigid row (repetition); grass blades are huge/oversized relative to the hut; one dark doorway gap is a black void (no interior/backface). Roof overhangs float slightly on thin black posts.

### u05_alpine_air (cam 1950,320,-500 → 1600,130,-900) — 7.5/10
Best mountain shot. Massif reads solid, snow line natural, village nestled in a bowl with a frozen pond. Pines well distributed. Defect: one grey sphere/boulder embedded high on the peak (upper-right, ~x1700,y400,z-700) looks stuck-on; pond edge is a clean circle.

### u06_east_sea (cam 1800,250,-1400 → 2300,300,-1500) — n/a (5/10 as a shot)
Open sea only — nothing but water, sky and the view-cube. Water tiles show a faint repeating ripple seam near the bottom edge. Confirms no floating debris off the east coast, but the shot carries no content.

### u07_elf_air (cam -1250,260,-250 → -1560,30,-430) — 8/10
Still the strongest area. Giant central tree, varied foliage, dirt paths, ponds, white blossom scatter, ruins/gazebo. Defect: blossom/mushroom props are very dense and uniform, bordering on visual noise; two ponds are circular.

### u08_country (cam 200,120,-300 → 900,30,-300) — 7/10
Rolling green, orchard of orange/green trees, windmill, lamp posts, path. Reads pleasant. Defects: large empty grass expanses left and foreground; blue-roofed towers in extreme foreground are clipped by camera (framing, not a build fault); far-right a hard rocky plateau edge meets the sea abruptly.

### u09_capital_air (cam 300,320,-1050 → 0,40,-1650) — 8/10
Dense, convincing walled capital: half-timbered houses, red/blue roofs, cathedral, castle on the rise, towered curtain wall, central plaza. Strong. Defects: roof-colour pattern is slightly repetitive; grass outside the wall is flat and empty; wall meets terrain on a perfectly flat shelf.

### u10_harbour_air (cam -150,90,1700 → -420,10,1850) — 7.5/10
Lively harbour: tall ship, sailboats, piers, buoys, barrels, anchors, mixed houses. Defect: a few boats/buoys sit on the water a touch high (slight float); grass-to-beach transition is a hard line; houses repeat.

## Area verdicts & prioritised fixes

**Island overview — 6/10**
1. Break the rusty-town ground seam: feather sand↔grass over a 40–60 stud ring at x1100–1500,z900–1300 instead of a hard circular edge.
2. De-stamp the two round ponds near x0–200,z-150 and x400,z-300: irregularise shorelines ±15 studs.
3. Add light coastline variation (coves/rocks) around the island rim.

**Alpine + tower massif — 7/10**
1. Retexture the checkered flat rock panel ~x1380–1480,y260,z-1000 with slate/basalt; break the straight edge.
2. Remove/sink the stuck grey sphere on the peak ~x1700,y400,z-700.
3. Soften the straight cliff drop below the alpine village (z~-900).

**Rusty town — 6/10**
1. Fill black doorway voids (x1150–1250,z1120–1180) with a dark interior plane or a back wall.
2. Shrink grass-blade props ~50% here; vary hut yaw/spacing to kill the straight row.
3. Jitter hut positions ±3–5 studs and swap 2–3 roof tones.

**Elf valley — 8/10**
1. Thin blossom/mushroom scatter ~30%.
2. Irregularise the two ponds.

**Countryside — 7/10**
1. Fill empty grass left/foreground (x100–400,z-200..-400) with hedgerows, rocks, a few trees.
2. Soften the hard rock-plateau/sea edge far east.

**Capital — 8/10**
1. Add gardens/trees in the empty grass belt just outside the curtain wall.
2. Vary roof-colour clustering to reduce the repeat.

**Harbour — 7.5/10**
1. Lower floating boats/buoys ~1–2 studs to water level.
2. Feather the grass→beach line into a sand transition.

## Three biggest remaining problems (whole map)
1. Hard straight terrain/colour seams — the rusty-town ground ring, the checkered alpine rock panel, and several wall/cliff/beach edges all read as cut-not-blended.
2. Stamped-circle water bodies and smooth uniform coastline across the island.
3. Repetition & oversized props — identical lined-up rusty huts, giant grass blades, dense uniform elf-valley scatter.
