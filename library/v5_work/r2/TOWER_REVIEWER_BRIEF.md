# Tower reviewer brief (round 2)

You are a FRESH reviewer. You judge pictures only. Do not read code, `fix`, `fix_scratch`, `v5_round1_archive`, `gallery` or any `REVIEW_*`, `review_*`, `assign_*` file. Be strict.

## What you are looking at
A giant enterable wizard tower for a Roblox fantasy game (chunky low-poly style, original design). The tower shell is a hollow tower with 8 floor levels, an open round atrium in the middle and a wide helical stair that spirals up around the atrium. Separate furnishing models were placed inside it by a layout program: curved bookshelf bays along the outer wall, straight shelves, a big round relief map of the island on a stone-and-brass table in the Map Hall (level 0), a round floor medallion, chandeliers, alchemy lab sets, study sets, and a brass telescope at the top. The grey ground and flat sky are only the photo studio.

The question: does the furnished interior look and function like the inside of an impressive wizard tower, and does everything fit?

Files (all in `C:\Users\Nitro\.kiro\crew\workspace\town\library\v5_work\tower_check\fixed\`):
- `cutaway_full.png`: the whole tower with its front half cut away, seen from the front.
- `cutaway_lower.png`, `cutaway_upper.png`: the same cutaway, closer, lower floors and upper floors.
- `plan_L0_map_hall.png`, `plan_L1_gallery.png`, `plan_L2_gallery.png`, `plan_L3_vault.png`: top-down sections at the floor levels 0 to 3 (the floor above is removed).
- `hall_view.png`, `hall_view_back.png`: eye-level views inside the Map Hall, looking toward the back and toward the front.
Open each once. Do not open anything else except `C:\Users\Nitro\.kiro\crew\workspace\town\reference\world_concept_topdown.png` (optional, once).

## Score 1 to 10 each (be harsh: 8 means you would be proud of it in a finished game)
1. BOOKSHELVES: floor-to-ceiling, packed books, curved to follow the round wall, a real library feel; do they sit against the wall, not overlapping each other, not blocking windows, the door or the stair?
2. CIRCULAR MAP: the relief map of an island in the middle of the Map Hall: does it read as a map (land, sea, rings, landmark tokens), is it a worthy centrepiece, is there walking room around it?
3. STAIR AND WALKABILITY: a player (5.5 studs tall) must be able to walk the helical stair and each floor without hitting furniture; is the stair clear of shelves and props? Is there headroom?
4. LAYOUT: balance, readability of each room (library, vault, alchemy lab, study, star room, observatory), no clutter that blocks routes, no gaps that look unfinished, no pieces that float or sink into walls or floors.
5. ATMOSPHERE: does the interior look like it belongs to a powerful archmage (materials, colour, scale of the hall), or does it look empty or generic?
Then list every concrete defect with the file you saw it in, and say what you would change (move, remove, add, resize) in plain words.

## Output
Write `C:\Users\Nitro\.kiro\crew\workspace\town\library\v5_work\r2\tower_review.md`: the five scores, the defects, the changes you want, and a verdict line `TOWER INTERIOR: PASS` (all scores 8 or more and no blocking defect) or `TOWER INTERIOR: FIX`. Do not modify anything else, do not run Blender or Studio. Final answer: at most 12 lines.
