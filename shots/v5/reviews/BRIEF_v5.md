# V5 photo review brief (first round after the v5 build)

You judge photos only. The pictures are in `C:\Users\Nitro\.kiro\crew\workspace\town\shots\v5\<round>\` (names `f_*`). `f_over_*`, `f_quad_*`, `f_himalaya_*`, `f_plateau_down`, `f_skull_down` were taken from high altitude with fog OFF; all other `f_*` with game fog. Ignore the small 'Back' view-cube widget (Studio overlay). Read at most 4 images per read call. Camera lists are the CSV files next to the pictures.

References (look at these first): `town\reference\world_concept_topdown.png` (the target composition of the whole island), `town\reference\castle_town_reference.png` (the target look of the capital), `town\plan_v5\topview_sketch_v5.jpg` (the intended top view, a rough drawing), `town\plan_v5\WIZARD_TOWER_BRIEF.md`.

## What to judge, area by area (score each 1-10, then SHIP / NOT YET)
1. **Whole island from above** (`f_over_*`, `f_quad_*`): does it read like the concept map? Ragged coast, colour zones, white NE massif with a pale plateau, dark forest NW, orange desert SE, dark east coast with the Skull cliff, river loops round the capital, winding roads with bridges. Is the middle still a green carpet?
2. **Himalayas and the wizard tower** (`f_himalaya_*`, `f_plateau_down`, `f_tw_*`): peaks and plateau shape, the tower as a landmark from far (`f_tw_far_*`), tower exterior (orbit, porch, crown), then interior: Map Hall with the circular map, curved bookshelves, library galleries, lab, study, observatory. Walkable? Awesome? Anything glowing or floating?
3. **Roads through the mountains** (`f_roof_*`, `f_gale_*`, `f_dragon_*`, `f_descent_*`, `f_tunnel_*`, `f_bridge_*`): do roads climb in believable hairpins, cut through ridges at tunnels, hug cliffs, cross rivers at proper bridges? Do the rope bridge and tunnel mouths look Himalayan and fit the rock? Any road that ends in nothing, floats or is buried?
4. **Capital** (`f_cap_*`): polygon ring wall with cone-roofed towers, red-brown wall-walk, gatehouse in the wall, one orange roof family, skyline towers, plaza and order hall, keep on its terrace, river loop and bridges. Compare with the castle-town reference.
5. **Elf valley** (`f_elf_*`): second house ring, canopy villages with ladders, waterfall width and mist, ground dapple, still NO glow of any kind.
6. **Town 1** (`f_t1_*`): statue with a face, avenue, street life, no gate, ground ring round the houses.
7. **Entrances** (`f_entry_*`): the plain arch must be gone. Does each settlement feel naturally entered (bend, framing trees or boulders, one sign)? Anything that still looks like a plain arch?
8. **Defects** to list: floating pieces, buried pieces, pieces in water, z-fighting, stretched textures, hard blue cut-out water, flat green carpet areas, repeated identical models in a row.

## Deliverables
Report in the same format as the round-5 reports: scores per area, `ROUND V5 SCORES:` line, a verdict `SHIP` or `NOT YET` for the whole map, and the five cheapest changes (30 minutes) that would raise the weakest scores. Give coordinates for every defect (the photo name tells the camera).
