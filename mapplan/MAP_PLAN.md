# Phase 1 map — shared plan (coordinator contract)

Every area agent reads this whole file. It is the single source of truth for borders,
heights, road gates and the plan format. If something you need is not here, decide it
yourself inside YOUR area and write the decision in your notes file. Never plan outside
your rectangle.

## World
- Roblox world units = studs. Map is 7000 x 7000, centred on (0, 0). X runs east (+) / west (-).
  **Z runs south (+) / north (-).** Y is up.
- Sea level (water surface) is **Y = 0**. Areas sit on land above it.
- Character is ~5.5 studs tall. Doors ~8-10 studs. City lamp 18.6 tall.
- Studio is the only build target. **Agents never touch Studio.** You write a plan file;
  the coordinator builds it, snaps every model to the ground, anchors it and tests it.

## Models
- `C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\catalog.json` lists all 330 models:
  `id, folder, size_x, height, size_z, pieces` (sizes in studs, before rotation).
  Use ONLY ids from this file. Use each model's real size when spacing things.
- Previews (to understand what a model looks like): `C:\Users\Nitro\.kiro\crew\workspace\town\library\<folder>\<id>.png`
  and contact sheets in `C:\Users\Nitro\.kiro\crew\workspace\town\library\_sheets\`. Look at the previews of the
  models you use most.
- Full model list with descriptions: `C:\Users\Nitro\.kiro\crew\workspace\town\MAP_MODEL_LIST.md`.
- Orientation: `rot` is the direction the model's FRONT (door, face, sign) faces:
  **rot 0 = faces +Z (south), 90 = faces +X (east), 180 = faces -Z (north), 270 = faces -X (west).**
  Any angle in between is fine for nature and props. The coordinator handles the conversion.
- Model origin is bottom-centre. Placement x,z = centre of the footprint.
- Shared kit (roads, lighting, nature, props folders) may be used everywhere.
  Area folders (capital, castle, rusty, alpine, elf, harbour, between) belong to their area,
  except the roads/countryside agent owns `between`.
- **No Toolbox, no plain Roblox parts as decoration, no stand-ins.** If the area needs
  something that is not in the catalog, do not fake it: list it under "missing" in your notes.

## Areas (rectangles are hard borders; leave a 20-stud margin inside them)
| Area | Agent | X range | Z range | Ground (design Y) | Road gate(s) (x, z, y) |
|---|---|---|---|---|---|
| Town 1 (exists, spawn) | town1 | -450 .. 450 | -560 .. 345 | ~1-3 (existing) | N (0,-560,2), E (450,-108,2), W (-450,-108,2), S (0,345,2) |
| Royal capital + castle | capital | -800 .. 800 | -3300 .. -1700 | gate 20, rises to 150 at castle | S grand gate (0,-1700,20) |
| Alpine village | alpine | 2150 .. 2850 | -850 .. -150 | 70 (rolling 60-95) | W (2150,-500,70) |
| Elf jungle city | elf | -2850 .. -1950 | -1050 .. -150 | 10 (roots/rises to 40) | E (-1950,-600,10) |
| Harbour | harbour | -1000 .. -200 | 2300 .. 3100 | 8 town, quays at 4, sea 0 south of z 2900 | N (-600,2300,8) |
| Rusty town + church | rusty | 1600 .. 2200 | 1400 .. 2000 | 14 (dry, cracked) | NW (1600,1500,14) |
| Roads + countryside | roads | everywhere outside the rectangles above | | links the gates | all gates |

- **Keep-out:** the NE tower mountain stays untouched. Treat X 1700..3300, Z -2700..-1050 as
  no-build for everyone (roads go around it). The coordinator will confirm its exact outline in Studio.
- **Gates are fixed.** Each area agent ends a main street exactly at its gate point at the gate height.
  The roads agent starts/ends each road exactly there. Inside 40 studs of a gate, area agents keep the
  street clear and 24 studs wide.

## Plan file format (one per agent)
Write `C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\<agent>.json`:

```json
{
  "area": "capital",
  "terrain": [
    {"op": "plateau", "cx": 0, "cz": -2600, "rx": 700, "rz": 650, "top_y": 120, "slope": 120, "material": "Grass"},
    {"op": "hill",    "cx": 300, "cz": -3000, "r": 150, "h": 40, "material": "Grass"},
    {"op": "flatten", "x0": -60, "z0": -2000, "x1": 60, "z1": -1900, "y": 22, "material": "Cobblestone"},
    {"op": "ramp",    "x0": 0, "z0": -1700, "y0": 20, "x1": 0, "z1": -2200, "y1": 60, "width": 30, "material": "Cobblestone"},
    {"op": "water",   "x0": -400, "z0": -2400, "x1": 400, "z1": -2380, "y": 18, "depth": 6},
    {"op": "paint",   "cx": 0, "cz": -2500, "r": 80, "material": "LeafyGrass"}
  ],
  "placements": [
    {"model": "C05_townhouse_1", "x": 40, "z": -1950, "rot": 270, "group": "MarketStreet"},
    {"model": "A24_oak_1", "x": 120, "z": -2100, "rot": 37, "scale": 1.1, "group": "Park"},
    {"model": "A18_wall_lantern", "x": 46, "z": -1950, "rot": 270, "y_offset": 7, "group": "MarketStreet"}
  ]
}
```
- terrain ops run in order. Materials are Roblox `Enum.Material` names valid for terrain
  (Grass, LeafyGrass, Ground, Mud, Sand, Sandstone, Rock, Slate, Basalt, Cobblestone, Pavement,
  Brick, Snow, Glacier, Ice, Limestone, CrackedLava, Salt, Asphalt, Concrete, WoodPlanks).
- `y_offset` (default 0) is height above the ground found under (x, z). Use it only for things
  mounted on walls or sitting on top of other models (lanterns on walls, candles on altars,
  bunting between houses). Ground models leave it out.
- `scale` only for nature (0.8-1.3) and small props (0.9-1.1). Buildings always 1.
- `group` = folder name inside the area in Studio (districts/streets). Keep groups meaningful.
- Interior models (throne room items, church pews/altar/organ, shop counters...) go INSIDE an
  interior-enabled building; give exact coordinates inside its footprint and say which building
  in notes. Only 1-2 buildings per settlement are enterable (game performance rule).

Also write `C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\<agent>_notes.md` with: the layout idea in plain
words (districts, streets, landmarks, views), every decision you made, which buildings are
enterable, a **missing** list (things the area really needs that the catalog lacks), and the
validation results.

## Quality bar (this is a showcase map — top Roblox game quality)
- Plan it like a real settlement: a clear main street from the gate to the landmark, side streets,
  a square/plaza, districts with a purpose. Buildings FACE streets (front toward the street) with
  backs to yards or walls. Rows of houses follow the street line with small 2-6 stud gaps and
  varied models (never 3 identical models side by side; mirror via rot 180 across the street).
- Landmarks get sightlines: the castle visible straight up the capital avenue, the church at the end
  of the rusty main street, the world tree visible from the elf gate, the lighthouse from the quays.
- Lamps along main streets every 35-45 studs, alternating sides; lanterns on taverns/shops; torches
  or braziers at gates and walls. Every street has light.
- Props tell stories: barrels/crates by taverns and warehouses, stalls and carts in markets, benches
  facing views or fountains, hay by stables, nets and rope on quays, flowers in planters and at
  doorsteps. Cluster props in natural groups of 2-6, not evenly spread.
- Nature: trees in groups with mixed species/rot/scale, never on streets or in doorways; bushes and
  flowers along building edges and paths; rocks half-buried at slopes. Leave open grass too.
- Density: dense in centres, thinning toward edges and blending into countryside.
- Nothing overlaps unless it is meant to (a lantern on a wall, a candle on an altar). Keep a
  >= 2 stud gap between building footprints (use rotated footprints: for rot 90/270 swap size_x and size_z).
- Nothing in water unless it belongs there (piers, boats, lily pads, pilings).
- Streets 16-24 studs wide for main streets, 10-14 side streets, 6-8 paths. Use the road kit models
  (A01-A07, A10 curbs, A08/A09 stairs, A11/A12 bridges) or terrain paint (Cobblestone/Pavement/Ground).

## Validation (do this before you finish)
Write and run a small Python (or PowerShell) check in your scratch folder that loads your plan and
catalog.json and reports: unknown model ids, placements outside your rectangle (minus margin),
overlapping building footprints (rotated rectangles, >1 stud overlap) for models taller than 6 studs,
anything within 12 studs of a gate point that blocks the street, and counts per model. Fix every
problem, re-run, and paste the final report into your notes.
