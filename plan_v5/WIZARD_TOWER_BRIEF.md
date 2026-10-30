# Wizard tower brief (Blender): the giant enterable tower on the Roof Plateau

Written 30 Oct 2026, 11:40. Your words: "on top of the Himalayan plateau there is room for a giant enterable wizard tower; give this one special attention while making the Blender file; it should look awesome with a bookshelf on the side and a circular map; give extra effort." This is the most important single build in v5. Rows WT01 to WT13 in `V5_MANIFEST.md` (21 P1 models + 6 P2 terrace pieces). Original design: no Black Clover names, shapes or title art. No glow or emissive anywhere; warm candle and lantern light comes from Roblox lights in Studio, not from the meshes.

Working name: **The Star Spire** (placeholder). Emblem: a white star over an open book on indigo.

## 1. Where it stands (terrain is planned, see `world_v5_terrain.json`)

- Roof Plateau: ellipse centre (1380,-1400), 560 x 380 studs, level y 322, with a gentle roll. Peaks stand around it: Spire of Dawn (west, h 640+), Twin Fangs (north), East Horn. A frozen tarn on the east side drains over the south edge as the 190-stud Roof Falls into the alpine ice lake.
- Tower pad: centre (1380,-1320), floor y 324. Shell radius 55, terrace radius 95, courtyard radius 140.
- The tower faces +Z (south): the Roof road arrives from the south-west and reaches the porch over the courtyard. Pivot = centre of the shell at floor level. Build at 1 Blender unit = 1 stud.

## 2. What it looks like from outside (from the plateau and from far away)

- **Height 300 studs above the terrace** (a player is 5 studs tall, so it is 60 players high). It must read as a tower from 2,000+ studs away: a strong vertical stack, light bands, a dark roof, a bright finial.
- **Plinth:** stepped stone terrace 150 studs wide and 12 high, with a broad 40-step stair up to the porch.
- **Base (levels 0 and 1, diameter 110):** a Himalayan monastery drum. Whitewashed walls, a deep red-brown timber band, tapered window frames (narrower at the top), small copper-green eaves, angled stone buttresses.
- **Shaft (levels 2 to 5, diameter 96 narrowing to 70):** pale stone drums. Each level is turned 6 to 8 degrees against the one below and has a ledge or balcony, so the silhouette twists slightly. Corner turrets with copper-green cone roofs. Prayer-flag strings between balcony posts.
- **Upper (levels 6 and 7, diameter 64 to 52):** the star room and the observatory, with an open ring balcony around the top level.
- **Crown:** copper dome with a slit (WT11 armillary rings around it) and a spire with a gold star finial. A long indigo banner streams from the top (separate mesh).
- **Palette:** granite (176,172,180), limestone band (226,214,190), whitewash (238,234,226), ochre trim (196,150,76), red-brown timber (112,60,48), indigo slate roof (52,60,96), copper-green (92,150,128), brass (200,164,84). Light dusting of snow on ledges, icicles on balconies.
- **Entrance (WT12):** a porch with big carved double doors in a RECTANGULAR frame (no arch), steps, two lantern posts. Doors are separate meshes with their pivot at the hinge, so Studio can open them.
- Shell walls are 6 studs thick with real window openings (14 x 8 studs, with glass panes as separate transparent parts in Studio). Interior must be fully enterable.

## 3. The inside (the part that must look awesome)

Inner diameter 98 at the bottom, 58 at the top. Floor to floor 32 studs, clear height 28. Door openings 8 wide, 12 high. Nothing narrower than 7 studs on a walking route.

| Level | Floor y (above terrace) | Room | Contents |
|---|---|---|---|
| 0 | 0 | **Map Hall** (double height 40) | **The circular map** (WT05) in the centre on a stone-and-brass table, 44 studs across, with a brass walkway rail around it. Round floor medallion (WT06). Along the outer wall between the windows: **curved bookshelf bays** (WT03, 12 of them) and two reading alcoves. Ring chandeliers (WT09) hang over the map. |
| 1 | 40 | Library gallery | Ring gallery 14 studs wide around the open atrium (railing). Two-storey curved bookshelves (WT03) on the outer wall with rolling ladders. Island shelves and reading tables (WT04). |
| 2 | 72 | Library gallery | Same ring, other shelf variants: scroll racks, glass-fronted cabinet, map-chest drawers. |
| 3 | 104 | Archive vault | Straight shelves (WT04), writing desks, scroll vault. |
| 4 | 136 | Alchemy lab | Four lab sets (WT07): bench with glassware, herb rack and jars, specimen shelf, orrery. Big cauldron. |
| 5 | 168 | Archmage study | Desk with open books and quill, bed alcove with drapes, globe and sea-chart stand (WT08). Door to the outer balcony. |
| 6 | 200 | Star room | Painted star chart on the ceiling (texture or vertex colour), armillary sphere, orrery. |
| 7 | 232 | Observatory | The giant brass telescope (WT10) under the dome slit, ring balcony outside. |
| top | 264 to 300 | Crown | Dome, armillary rings, spire, finial. |

**Stairs:** a wide helical stair (7 studs wide) around the edge of the open atrium, rise at most 1.1 per step, run at least 2.2, landings 10 studs deep at every level, handrails both sides. Jump-friendly: no gaps wider than 4.

**The circular map (WT05).** A 44-stud round relief map of the whole island, carved in stone, on a round table with a brass ring and a rotating outer scale ring (separate mesh). Relief height 3 studs, sea sunk below the land, tiny landmark models on it (this tower, the capital walls, the Elden Tree, Frosthold, the Skull cliff, the ring temple, the harbour). Its source data is ready: `wizard_map_relief.obj` (the planned island as a 100 x 100 disc mesh, about 15k triangles) and `wizard_map_color.png` (2048 x 2048 colour map with rivers and roads), made from the same terrain plan as the world. Import them, build the table around them, add the landmark tokens. Split into 3 MeshParts: relief, landmarks, table and rings.

**Bookshelves.** They are the signature of the Map Hall and the library: floor-to-ceiling curved bays that follow the round wall, packed with books of many sizes and colours (spines, a few leaning, a few gaps), scroll racks, brass ladders on rails, carved end panels, lantern hooks. Build books as one merged mesh per bay with a shared colour atlas (do not model 200 separate books).

## 4. Budgets and structure

| Piece | Rows | Triangles | MeshParts (each at most 20k) |
|---|---|---|---|
| Exterior shell | WT01 | 150k | 10: plinth, 8 levels, crown |
| Interior shell | WT02 | 90k | 6 to 8: floors, atrium rails, stair, linings |
| Map table | WT05 | 60k | 3 |
| Porch and doors | WT12 | 24k | 3 |
| Crown rings and telescope | WT10, WT11 | 42k | 3 |
| Bookshelves | WT03, WT04 | 5 types x 10 to 12k | 1 each |
| Furniture | WT07, WT08, WT09 | 7 to 10k each | 1 each |

Roblox allows 20k triangles per MeshPart, so the shell is cut by level. Props are used many times (about 40 shelf bays and 30 other props in the final scene), so each is a separate small model. Use at most 3 shared material atlases for the whole tower. This tower is the one allowed exception to the hero limit of 60k triangles.

**Export extras:** `tower_collision.json`, a list of boxes in tower-local coordinates (name, position, size, yaw) for every floor, wall segment and stair tread. Studio builds invisible anchored collision parts from it; the visible meshes stay non-colliding except the big floors.

## 5. How to build it (order) and how it is checked

1. Block-out with simple drums at the right sizes, check the silhouette from 2,000 studs (render at 256 px wide: must still read as a tower).
2. Exterior detail level by level, then crown, then porch.
3. Interior shell and stair. Walk test: a 5-stud capsule must be able to go from the door to the observatory (check headroom 10 studs, tread rise).
4. Bookshelves and the map table (use the OBJ and the colour map).
5. Furniture sets.
6. Render 6 exterior views (front, back, two sides, three-quarter, from above), a cutaway section through the middle, and 4 interior views (Map Hall looking at the map, a library gallery, the lab, the observatory).
7. Independent reviewer scores the renders. Needs 8 or more in each of: silhouette, materials, interior, bookshelves, circular map. Anything below goes back for a fix.
8. Export with `library/src/export_v2.py`, name `WT_01_wizard_tower_shell` and so on, then upload.

## 6. Studio assembly (after upload)

Terrain plateau and pad first, then the shell and the interior floors, collision proxies from `tower_collision.json`, furniture at the listed ring positions, doors with hinges, warm PointLights (colour (255,190,120), brightness low, range 24, no Neon material), window panes, the Roof road arriving at the porch, prayer-flag strings, cairns and the terrace set (WT13). Then a photo round and a walk-through test.
