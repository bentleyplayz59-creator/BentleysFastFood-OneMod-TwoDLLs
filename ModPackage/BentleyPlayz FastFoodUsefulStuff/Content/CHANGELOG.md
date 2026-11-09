# Changelog

## 3.13.6
- REVERTED: all Bus Stop terrain edits are gone (no canopy removal, no fence tiles set, no tile removals, no spawn-marker removals). The Bus Stop map is vanilla except for the restaurant itself.
- MOVED: the restaurant now stands on the lawn at tiles 30-37 x 10-16 (was 32-39 x 3-9 on the road). Front doors are 33-34,15, the exit puts you at 33-34,17. That leaves 2 free tiles on the right before the garden fence (x40) and 2 free rows below the exit before the lower fence (y20).
- NOT DONE: running `world_clear current everything` automatically. Content Patcher cannot run console commands and the compiled Code part has no source here. Run the command once yourself on the Bus Stop (see below).
- World map: the two Data/WorldMap patches are one patch (from 3.13.5). The welcome letter says Bus Stop (from 3.13.5).
- Version is 3.13.6 in both manifests. The DLL is unchanged.

## 3.13.4
- MOVED: Bentley's Fast Food now stands on the Bus Stop road (tiles 32-39 x 3-9, door at 35-36,8, exit at 35-36,10) instead of in Cindersap Forest. The Forest, Ice Festival and clearing patches are no longer used (data/forest_restaurant.json is kept in the folder but is not loaded; data/busstop_restaurant.json replaces it).
- CHANGE: the two tree canopies over the road beside the restaurant and the lawn tiles in front of the door are cleared. Fences, the road curb, the cliff and the fenced garden east of the door are left as in vanilla.
- CHANGE: tree and bush spawn markers on that lawn are removed (affects new saves only; trees and bushes already in a save must be chopped).
- Version is now plain 3.13.4 (no -dev). Because the version changed, the update announcement shows once more. The Code part (DLL) logic is unchanged.

## 3.13.3-dev
- DEV BUILD, visual polish only: no gameplay, item, shop, price or code change. The map file name is unchanged (FastFoodInterior_v4.tmx) and so are all Content Patcher targets. The Code part (DLL) is byte-identical to 3.13.2-dev; only its manifest version changed so both parts still match.
- CHANGE (Dessert Corner furniture): the two round bistro sets are replaced by small cafe tables in the dining room's own style (same dark-brown outline, cream rim, wood top and wood legs) with pink accents: a pink skirt, a pink placemat and a sundae on top. The chairs are redrawn as slim pink-cushioned chairs with the same wood frame, a little smaller than the dining chairs. Same tile positions as before (tables 3,6-7 and 3,10-11; chairs 2,7 / 4,7 / 2,11 / 4,11), so walking space and collision are unchanged.
- NEW: the dessert chairs can be sat on (added to Data/ChairTiles in data/seating.json), like every other chair in the restaurant.
- CHANGE (sign): the big Dessert Corner sign (art said SWEETS) now reads DESSERT. Lettering redrawn centred with a soft shadow; the pink frame is unchanged.
- CHANGE (kiosk entrance): the kiosk is now a full storefront. From the top: DESSERT sign, striped awning (moved up one tile, over the wall), a dark ORDER HERE menu board (new tiles on tile row 3), then the counter with a glass cake dome, a service bell, a cash register and a two-tier cake stand, and a pink floor mat with three up-arrows on tile row 5 in front of the counter. The counter is redrawn with a trimmed lip and recessed panels. Tiles 2-4,4 are still the only OpenShop {{ModId}}_DessertKiosk tiles (data/dessert_corner.json is unchanged except for its log text) and still sit on solid Buildings tiles; the player stands on the mat at 2-4,5 and faces up.
- CHANGE (arcade): the arcade sign (Front layer, 3 tiles, vanilla townInterior art) is moved up one tile, from row 2 to row 1 (tiles 27-29). It stays centred over the room (centre tile 28). Row 1 is plain wall (the wall tile at 26-30,1), so nothing overlaps; the cabinets, their Arcade_Prairie / Arcade_Minecart tiles (27 and 29, rows 3-4) and the lights are unchanged.
- ART: assets/maps/z_DessertCorner.png was redrawn in place (still 128x64, 8x4 tiles, same tile indices for everything that already existed). New tiles use previously empty slots 21-29. Tile slots 0, 1 and 11-16 (floors, posters, freezer, soft-serve machine) are untouched. source/build_dessert_corner.py regenerates the sheet from source/z_DessertCorner_3.13.2_original.png.
- MAP: exactly 12 tiles changed in the dessert room (3 Back, 3 Buildings, 6 Front) plus 3 Front tiles moved for the arcade sign. The previous map is kept as source/FastFoodInterior_v4_3.13.2_original.tmx.
- NOT TESTED IN GAME (see TEST_REPORT.md). The art was previewed in a map render made outside the game. The arcade sign's own tiles come from the vanilla townInterior sheet, which is not in this mod, so the new sign position could not be previewed with its real art.

## 3.13.2-dev
- DEV BUILD: same behaviour as 3.13.2, but the Code part logs everything it does to the SMAPI log with a [DEV] tag (startup and config values, events, every eat/drink with the item id, Windex detection and damage, health changes, door use, announcement, a heartbeat). Existing hidden log lines are raised to Info so they show in the console. New console command bentley_windex_test [cone] runs just the damage code. See DEV_LOGGING.md in the mod folder.

## 3.13.2
- NEW: separate config setting for the Windex Swirl Cone, WindexSwirlConeDamage (default 10), next to WindexDrinkDamage (default 10) in Code/config.json. Each item takes its own amount; 0 turns that one off; never below 1 health.

## 3.13.1
- FIX (Windex damage): the DLL only recognised raw Windex, so the Windex Swirl Cone never hurt. It now checks both (O)BentleyPlayz.FastFoodUsefulStuff_Windex and (O)BentleyPlayz.FastFoodUsefulStuff_WindexSwirlCone (new helper IsHarmfulItem in WindexDrinkController).
- FIX: Code/config.json now ships WindexDrinkDamage 10 (it was 0, which switched the DLL damage off). An old config.json with 0 keeps damage off, so replace it or set it to 10.
- CHANGE: Windex and the Windex Swirl Cone are back to Edibility 0, so the DLL is the only source of damage (one hit of 10, never below 1 health) and nothing stacks.
- The compiled DLL no longer carries its embedded debug symbols (smaller file; error traces just lack line numbers).

## 3.13.0
- CHANGE: the Furniture Corner is replaced by the Dessert Corner, the same left-hand room in the restaurant map (still part of the restaurant, no loading screen, doorway at 6,9). New pink-and-cream checker floor, SWEETS sign, two ice-cream posters, a dessert kiosk counter with a striped awning (tiles 2-4,4), a freezer and a soft-serve machine, and two bistro sets. New tileset: assets/maps/z_DessertCorner.png. Map file is now FastFoodInterior_v4.tmx.
- NEW: the kiosk sells 7 desserts, each with its own drawn icon: Ice Cream Sundae (200g), Soft Serve Cone (140g, Speed +1), Fudge Brownie (160g), Strawberry Cheesecake (220g, Defense +1), Glazed Donut (120g), Banana Split (260g, Luck +1) and the Windex Swirl Cone (60g): vanilla soft serve with a blue swirl. Shop id {{ModId}}_DessertKiosk. Bentley loves the six normal desserts as gifts.
- FIX (Windex damage): Windex had Edibility 0, which the game treats as "eat it, change nothing", so nothing could hurt you unless the DLL did. Windex now has Edibility -9, and the Windex Swirl Cone has -8. In Stardew a negative edibility takes health and energy away when you eat or drink it, by the game itself, no code needed (about 10 and 9 health, plus energy). The DLL's own damage is switched off in the shipped Code/config.json (WindexDrinkDamage 0) so you don't get hurt twice. If you keep your old config.json, set it to 0 there too.
- REMOVED: all furniture (the 8 pieces, their textures, the furniture shop and ATM). Those textures never displayed in game. If you bought any, they will show as error items. Remove them or ignore them.
- The DLL is unchanged since 3.12.1 (restaurant coordinate patch). I could not find why its damage never applied without the source.
- NOT TESTED IN GAME. Tip: save outside the restaurant before updating (see 3.12.1).

## 3.12.1
- CHANGE: the Furniture Corner is no longer a separate location with a loading screen. It is now a room built into the restaurant map itself, on the left side, the mirror image of the arcade on the right (5 tiles wide, same floor, wall, windows and lights). The map grew from 26x14 to 32x14 tiles. The doorway between the dining room and the new room is an open gap in the wall at tile 6,9, exactly like the arcade's doorway at 25,9. There is no warp and no second location any more (`{{ModId}}_FurnitureWing` was removed).
- NEW LAYOUT: ATM on the back wall (tile 3,4) between two windows, Coke Cooler (1,4) and Milkshake Lamp (5,4) beside it, Burger Rug and Burger Chair in the middle, Nugget Table and Diner Booth along the bottom. The ATM still opens the same furniture shop (same eight pieces and prices as 3.12.0).
- BIG CHANGE TO COORDINATES: because the new room is added on the LEFT, everything that was already in the restaurant moved 6 tiles to the right (old x + 6, y unchanged). Updated to match: the Forest front-door arrival (now 15,12), the restaurant's exit warps (15,13 and 16,13), the staff door tiles (22,3 and 23,3), the bedroom exits (arrive at 22,4 and 23,4), the NPC warp (24,4), the ordering counter shop tiles (14-18,5), the arcade cabinets (27 and 29, rows 3-4), the light sources, Bentley's 6:10 AM spot (16,4), the Restaurant Robot's counter tile (15,4) and the Milkshake lesson event positions. Bedroom coordinates did not change.
- CODE (DLL byte patch, not recompiled): the compiled Code part had the main-entrance arrival tile (9,12) and the staff door tiles (16,3 and 17,3) written into it. Six single-byte constants were changed to 15,12 / 22,3 / 23,3 so they match the new map. The DLL was not rebuilt from source; its size is unchanged.
- REMOVED: assets/maps/FurnitureWing.tmx and FurnitureWingDoor.tmx (and the door tile image), since the room is part of the restaurant now. The previous restaurant map is kept in Content/source as FastFoodInterior_v2_3.12.0_original.tmx.
- UPDATE ANNOUNCEMENT: text updated (Code/announcement.json). Both manifests are 3.12.1.
- NOT YET TESTED IN GAME. Checked outside the game only (see TEST_REPORT.md). Tip: before updating, save while standing OUTSIDE the restaurant. A save made inside would put you at the old tile position, which is now somewhere else in the bigger room.

## 3.12.0
- NEW: Furniture Corner, a new room to the left of the dining room. Walk through the doorway in the restaurant's left wall (tile 0,9); you arrive at 18,9 inside the new room, and the doorway on its right wall (19,9) brings you back to the restaurant at tile 1,9. It is its own location (`{{ModId}}_FurnitureWing`), so no existing restaurant tile, warp, schedule, event or door coordinate moved.
- NEW: an ATM on the back wall (tile 9,4) opens a furniture shop (shop id `{{ModId}}_FurnitureATMShop`). It sells the Burger Chair (400g), French Fry Window (600g), Milkshake Lamp (500g), Coke Cooler (800g), Nugget Table (700g), Diner Booth (1,200g), Burger Rug (450g) and Fries Painting (900g). All eight are real furniture you can place at home.
- NEW: one tile of the restaurant's left wall (0,9) became a walkable doorway (floor and mat art, `assets/maps/FurnitureWingDoor.tmx`). No other tile of the restaurant map changed.
- CHANGE: update announcement text (Code/announcement.json, no recompiling). Both manifests are now 3.12.0 so it shows once for this version. The DLL is unchanged.
- NOT YET TESTED IN GAME: the Furniture Corner is new in this version. The files were checked outside the game only (JSON parses, maps are well-formed, tile ids are inside their tilesets).

## 3.11.2
- HOUSEKEEPING: both manifests and the READMEs now say 3.11.2 (they had been left at 3.11.0 / 3.9.0). Everything in 3.11.0-3.11.2 has been tested in game by the author and works. The DLL code is unchanged; its internal file-version label still reads 3.9.0, which is cosmetic (SMAPI and the announcement use the manifest version).
- FIX (staff door): the door tiles (16,3 and 17,3) now warp the player into Bentley's bedroom (tiles 6,9 / 7,9) when walked into, so you can't stand inside the door art. The tap-to-open behaviour from the code part is unchanged.
- FIX (lighting): the restaurant's light sources are now evenly spaced (every 4 tiles, radius 4 across the dining room), replacing the sparse ones that left dark patches. Kitchen and arcade lights are unchanged.

## 3.11.1
- FIX: the Restaurant Robot only works the counter when Bentley is away. He now starts each day in Bentley's bedroom (tile 2,9) and walks to the counter tile (9,4) at 7 PM. Nothing else changed.
- FIX: the Robot's schedule now begins with an explicit 6 AM entry in Bentley's bedroom (2,9), so he goes there even if an older save still remembers him in the restaurant.

## 3.11.0
- NEW: slightly larger restaurant interior. A new arcade room (5 tiles wide) was added on the right side, behind the dining room, reached through a doorway in the right-hand wall at tile 19,9. The map grew from 20x14 to 26x14 tiles. Every original tile, piece of furniture, light, warp, shop tile, seat and NPC coordinate is unchanged (columns 0-19 are untouched except the doorway tile 19,9; the old right wall now stands at column 25).
- NEW: two vanilla arcade cabinets in the new room, drawn from Stardew's own townInterior tilesheet: Journey of the Prairie King (left, tiles 21,3-4, Action Arcade_Prairie) and Junimo Kart (right, tiles 23,3-4, Action Arcade_Minecart). The game runs the minigames itself; the mod adds no minigame code, save data or progress tracking. Also a vanilla ARCADE sign above them.
- NEW: one extra wall tile (assets/maps/z_BentleyArcadeWall.png), made from the plain stripe row of the restaurant's own cream wall tile, so the new room's wall matches.
- NEW: three extra light sources for the arcade room (map property Light).
- CHANGE: update announcement text replaced (Code/announcement.json). The announcement code (DLL) is unchanged. Both manifests are now 3.11.0 so the announcement shows once for this version.
- CHANGE: the Restaurant Robot's home and 6 AM schedule spot is the counter tile 9,4 (from 3.10.3).
- Exterior art, Forest placement, doors and warps are not touched.

## 3.10.3
- CHANGE: the Restaurant Robot now lives at the counter tile 9,4 (home and schedule), so he is there from the start of a save, all day.
- CHANGE: the Restaurant Robot now works the counter at tile 9,4 (his 7 PM schedule destination), matching the in-game tile readout.

## 3.10.2
- CHANGE: the Restaurant Robot now stands on Bentley's own counter tile (10,4) instead of 12,4.
- FIX (no walking through each other): the area behind the counter is a single one-tile corridor, so they must never be in it at the same time. Bentley now arrives at the Saloon at 6:00 PM (leaves the restaurant well before), and the robot only starts walking to the counter at about 6:50 PM to arrive at 7:00 PM. In the morning the robot starts in the bedroom and stays there while Bentley is at the counter. The counter shop switches to the robot's portrait at 6 PM.

## 3.10.0
- CHANGE: Bentley now arrives at the Saloon at 6:30 PM (so he leaves the restaurant around 6 PM), and the Restaurant Robot walks to the counter at 6:10 PM, right after he goes. The counter shop switches from Bentley's portrait to the robot's at 6:10 PM. Bentley still gets home to bed at 11:30 PM.
- The robot's schedule only starts the morning after he is first added to a save (see 3.9.9 note): sleep once before testing.

## 3.9.9
- CHANGE: the bedroom staff door is no longer locked. The 3-heart rule in the SMAPI component's DLL is switched off (one byte changed so the heart check always passes), and the solid-door overlay patch was removed from data/locations.json. Anyone can walk through it now.
- NOTE (Restaurant Robot): the log shows his schedule file was never loaded on the first day of a save, because he is created when the save loads. His 7 PM walk to the counter starts from the next morning on. Sleep once, then test.
- Not tested in-game.

## 3.9.8
- FIX (Bentley frozen): 3.9.7 put the NPC warps on tiles 16-17,4, which are also the tiles where the bedroom exits drop Bentley in the morning, so he arrived standing on a warp and stopped. The NPC warp is now a single tile, 18,4 (to bedroom tile 7,9), away from the arrival tiles. The old solid door tiles (16-17,3) are no longer used by NPCs.
- Not tested in-game.

## 3.9.7
- FIX (Restaurant Robot): he now starts every day in Bentley's bedroom at tile 2,9 (his home) and walks to the counter (12,4) at 7 PM, working it until the day ends. Before, his home was the counter, so he spawned there.
- FIX (shop): the counter shop no longer uses Bentley's face all day. Bentley's portrait and greeting show from 6 AM to 6:30 PM; otherwise the Restaurant Robot's portrait and greeting show. The counter shop tile row now also covers tile 12,5 in front of the robot. The unused ShopRequiresBentley config option was removed.
- FIX (walking back to bed): the NPC warps for the staff door moved from the door tiles (16-17,3, solid under 3 hearts) to the floor in front of them (16-17,4), so NPCs can path to them. This is what stopped Bentley (and the robot) from walking from the counter to the bedroom.
- Not tested in-game.

## 3.9.6
- RENAME (internal): the NPC id is now {{ModId}}_RestaurantRobot everywhere (character data, sprites, portraits, dialogue, schedule, gift tastes). Files renamed: data/restaurant_robot.json, assets/npc/RestaurantRobot_*.png. Gifting is disabled (CanReceiveGifts false, hidden from the social tab).

## 3.9.3
- FIX (Restaurant Robot): Restaurant Robot now has a real schedule and a visible start spot at the counter (tile 12,4) instead of 18,9. While Bentley works (6:10 AM-7 PM) Restaurant Robot stands in Bentley's bedroom at tile 2,9 (the coordinates logged in-game). Whenever Bentley is away (Saloon and bed, 7 PM onward) Restaurant Robot works the counter.
- CHANGE (Bentley): Bentley walks to Gus's Saloon again, arriving 7 PM at tile 21,17 and playing the smoking animation, then walks home and is in bed at 11:30 PM.
- Not tested in-game. If 21,17 in the Saloon is blocked he will stand near it.

## 3.9.2
- ART: Bentley's bedroom re-laid-out along the walls with the centre left open. Bed is now a complete 2x3 bed (headboard, pillows, mattress, footboard) flush against the upper wall with a nightstand and lamp on each side; TV and stand centred on the upper wall; desk upper-left; bookshelf and couch on the left wall; chair against the right wall facing right; dresser flush to the right wall; rug (now 4 tiles wide) centred on the door axis. Both plants moved (corner by the couch, and beside the TV stand).
- NEW FILE: assets/maps/z_BentleyBedroomFurniture.png, six tiles holding a horizontally mirrored copy of the vanilla red couch so it faces the room with its back to the left wall. The rest of the map still uses the game's own `townInterior` sheet.
- Same 14x11 map, exit warps (6,10 / 7,10) and NPC spot (9,6) unchanged; every floor tile except the enclosed tile (12,5) is reachable from the door. Not tested in-game (tile preview and walkability check only).

## 3.9.1
- ART: Bentley's bedroom interior is redesigned using the real vanilla Stardew `townInterior` tilesheet instead of the custom hand-drawn tiles. Same 14x11 map, same exit warps (6,10 / 7,10) and same NPC spot (9,6); nothing outside this one map was touched.
- Layout: sleeping area on the right (full 3-tile bed with headboard, pillows, blanket and footboard; a bedside table with lamp on each side; footlocker at the foot; plant; painting above), media area in the centre (dresser with the TV standing on it; painting above), work area on the left (desk with typewriter and book, chair pulled up to the desk, notice board, grandfather clock), reading corner at the bottom left (bookshelf, red armchair facing a red rug), wood-panelled walls on all sides.
- Every walkable floor tile is reachable from the door (checked with a path search), including the tile next to the bed where Bentley sleeps.
- The map references the game's own `townInterior` sheet by name (no copy shipped). `z_BentleyBedroom.png` stays because the restaurant interior still uses it for the staff door art.
- Not tested in-game (checked with a tile-by-tile preview and a walkability check only).

## 3.9.0
- REMOVED: the Town Pass. data/townpass.json and assets/town_pass.png are deleted and the pack no longer includes them, so it is no longer sold at Pierre's or Bentley's counter. A one-time DayStarted action removes any leftover Town Pass book from existing saves. (The restaurant has been open 24/7 since 3.8.0 hotfix, so it is not needed.)
- FIX (bedroom collision): the staff door (interior tiles 16-17,3) is solid again while Bentley is under 3 hearts, using the existing BedroomDoorLocked.tmx overlay with the Hearts token. At 3+ hearts it is walkable. NPC warps are unchanged, and the SMAPI component still decides whether the door opens.
- CHANGE: the ordering counter shop no longer has 9 AM-9 PM closed hours (always open). The welcome letter now says open 24 hours.
- ANNOUNCEMENT: new update notes (open 24/7, Town Pass removed, bedroom door collision fixed, shop hours). The announcement version is now 3.9.0, so it shows once for every save/player on the next load. `bentley_announcement reset` shows it again. The DLL is now rebuilt from source and the announcement text is no longer inside it: it lives in Code/announcement.json. To change it for a future update, edit that file (no recompiling) and change its Version so everyone sees it once more.
- ART: the hours poster next to the front door (assets/maps/z_BentleyRestaurantExterior.png, plus the unused duplicate assets/buildings/fast_food_restaurant.png) said "9AM / 9PM". It now reads "24H / 7D". Only the poster's 11x15 pixel area changed. source/build_exterior.py still copies the old poster from the 3.7.2 original, so re-running it would bring "9AM/9PM" back.
- NEW (seating): you can sit on the restaurant's chairs and booths. 4 chairs facing right (tile 223), 2 chairs facing left (tile 226) and the 2 red booths (tiles 220 and 229, 2 seats each, facing left) are registered in vanilla Data/ChairTiles via data/seating.json. Right-click / tap / action button on the chair. No DLL involved. Not tested in-game.
- Not tested in-game.

## 3.8.0 hotfix (doors)
- CHANGE: the restaurant is open 24/7 (no hours, no Town Pass needed). Entering is never automatic: walk up and tap the door (mobile), press the action button (PC / controller / mobile) or click it. The two front-door tiles (Forest 68-69,25) now carry the game's own `Action Warp` property, so it works on every platform; the DLL's front-door check is also always open.
- CHANGE: removed the player-usable NPC warps on the door step and the closed-hours patches. Bentley no longer walks to the Saloon (he stays inside: counter 6:10, bedroom 11:30 PM).
- The hours poster now says open 24 hours. Bedroom door unchanged (3 hearts). Not tested in-game.

## 3.8.0
- NEW: SMAPI component (`BentleyPlayz_FastFoodUsefulStuff_SMAPI`). Install it next to the Content Patcher pack; the pack now requires it.
- DOORS: the front door and the bedroom staff door are now decided by the DLL, with the same rules as 3.7.3 (front door closed 6:00-8:59 and from 8:50 PM unless you own the Town Pass; staff door needs 3 hearts with Bentley; same messages). The matching Content Patcher door patches and tokens were removed so only one system exists. NPC warps, exits and the hours poster are unchanged.
- DOORS: action button (E / custom binding / controller A) and click/tap on a door tile within 2 tiles use the door; walking in still works. A locked door is now a walkable tile that shows its message instead of a solid tile.
- WINDEX: holding Windex and pressing use-tool (left click / tap) sprays the tile area in front of you and damages enemies through the game's combat code (10-18 damage, 0.7 s cooldown, consumes one Windex per spray that hits; all configurable in the DLL's config.json). Never harms the farmer. Drinking it (action button) is unchanged. Name, 25g shop price and item data are unchanged.
- ANNOUNCEMENT: a Stardew-style window with the update notes appears once per save after loading into the world, closed with Continue (mouse, keyboard, controller, touch). Stored per save/player in the SMAPI component's global data; bump `AnnouncementVersion` to show a new one in a future update.
- LIGHTING: restaurant interior gets nine extra light sources (map property `Light`) and the darkest shadow pixels of the interior tilesheet are lifted slightly. Layout, furniture and decorations are unchanged.
- Exterior artwork, items, prices, recipes, Gus's stock, NPCs, schedules, shop, config: unchanged.
- Version 3.8.0 (Content Patcher pack and SMAPI component).

## 3.7.3
- EXTERIOR ONLY: redrew the restaurant's building art (assets/maps/z_BentleyRestaurantExterior.png) to match vanilla Stardew architecture, using Pierre's General Store as the reference.
  - Roof: deeper hip roof with a ridge cap, three staggered courses of big vanilla-style shingle blocks, a dark shaded left hip face and a mid-tone right hip face, hip-line creases, a thick lit eave lip and a shadow cast onto the wall below it. Colours now come from vanilla's roof palette (was a pinker terracotta). New stone chimney and a metal vent pipe sit on the roof face.
  - Walls: teal clerestory panels and flat cream brick replaced by horizontal clapboard with vanilla timber corner posts (dark outlined, lit edge).
  - Windows: two ground-floor windows rebuilt with a lintel, jambs, 4-pane mullions, a projecting sill, shadow and the flower box; two small 4-pane windows flank the sign.
  - Door: proper frame with lit/shaded jambs, golden transom bar, two glass leaves with wood kick panels and the golden handles.
  - Awning: kept the red/cream stripes, now with a sloped top plane, scalloped valance, dark outline and a cast shadow.
  - Base: flat grey slab replaced by a two-course fieldstone foundation that runs to the bottom of the tile row (the building now sits on the ground), plus a flagstone door step with the red mat.
- KEPT PIXEL-IDENTICAL: the "BENTLEY'S FAST FOOD" sign, the menu board and the 9AM-9PM poster.
- NOT CHANGED: tile grid, tile indices, ForestRestaurant.tmx / ForestDoorStep.tmx / ForestDoorClosed.tmx, every Content Patcher patch, warps, door hours, collision, interior, items, shop, NPCs, config. assets/buildings/fast_food_restaurant.png is an unused duplicate of the sheet and was updated to match.
- Source: source/build_exterior.py regenerates the sheet from the 3.7.2 original (also included in source/).

## 3.7.2
- FIX (walk to the front door but cannot enter): the player warp on the door step only existed while a time/flag condition was true, and the condition failed closed, so a bad Time match left a walkable step with no warp. The warp (Forest 68-69,26, all three Forest maps) is now always present. Opening hours are enforced only by the solid closed-door overlay (still shows the closed message), so if anything goes wrong the door fails OPEN.
- FIX: RestaurantDoorOpen now defaults to true and turns false only during closed hours (6:00-8:50 and 20:50 onward), with both padded and unpadded Time ranges; Town Pass still keeps it open 24/7.

## 3.7.1
- FIX (head hidden under the building): the restaurant's door step (Forest 68-69,26) and the staff door's lower half (interior 16-17,3) were drawn on the Front layer, which draws over the player, so standing right below either one hid your head. Both are now on the Back layer: still walkable, but the player always draws on top. New file assets/maps/ForestDoorStep.tmx; ForestRestaurant.tmx and FastFoodInterior_v2.tmx edited.
- FIX (doors never locked): the SMAPI log showed Content Patcher ignoring every door condition ("Can't parse ... as a math expression"), because `Query:` only takes math, not game state queries. The conditions now use real Content Patcher tokens (Time, HasFlag, Hearts) through two dynamic tokens in content.json: RestaurantDoorOpen and BedroomDoorOpen. This fixes the locked bedroom door, its solid collision and locked message, and the front door's opening hours on all three Forest maps.
- CHANGE: Bentley's bedroom now unlocks at 3 hearts (was 2).
- The Town Pass is now checked by its mail flag only (the book itself was always just a keepsake).
- Known leftover: the two Data/WorldMap warnings in the log are harmless (the map marker just isn't added).

## 3.7.0
- NEW: Bentley's Bedroom, a small private room behind the restaurant (14x11 tiles): bed, nightstand with lamp, desk with monitor and game console, chair, dresser with mirror, window, burger poster, plant and a red rug. New art in assets/maps/z_BentleyBedroom.png, map in assets/maps/BentleyBedroom.tmx.
- NEW: a brown double staff door in the restaurant's back kitchen wall (tiles 16-17,3, just behind the counter gap). It is locked until you have 2 hearts (500 points) with Bentley, like vanilla bedroom doors. At 2+ hearts you simply walk into it. Below that, the door is solid and clicking it shows a "locked" message. It re-checks every 10 game minutes and when you change location.
- CHANGE: Bentley now sleeps there. His home is the bedroom (tile 9,6, next to the bed); he walks out to the counter at 6:10 AM and goes back to bed at 11:30 PM after the Saloon. NPC warps through the door always work, so he can use it even when it is locked to you.
- Exiting the bedroom puts you back in the kitchen at 16,4 / 17,4. The world map marker is shared with the restaurant.
- The restaurant interior map now uses a second tileset (z_BentleyBedroom) for the door art.
- Nothing else changed: items, shop, prices, hours, front door, events and dialogue are identical to 3.6.1.

## 3.6.1
- FIX (door hitbox): the two door tiles (Forest 68,26 and 69,26) were solid building tiles with a click-only door action, so walking at the doors just bumped an invisible wall. The door step is now a walkable tile (drawn on the Front layer) with a real warp, so you walk into the doors and go inside. The glass door tiles above it stay solid.
- Opening hours kept: the walk-in warp only exists 9:00 AM to 8:50 PM, or any time with a Town Pass. When closed, the step turns solid again and clicking it shows a closed message. Applies to all three Forest maps (normal and both Ice Festival). Bentley's own NPC warps are unchanged.
- CHANGE: Milkshake is now sold at Bentley's ordering counter for 180g (it was unbuyable). The cooking recipe from Bentley's 4-heart event is unchanged.
- New file assets/maps/ForestDoorClosed.tmx (the closed-door overlay).

## 3.6.0
- NEW ITEM: Milkshake (drink, sells for 90g, edibility 35, short Defense +1 / Speed +1 buff). It cannot be bought anywhere. You learn the cooking recipe (Milk + Sugar + Strawberry) only from Bentley.
- NEW EVENT: at 4 hearts with Bentley, walking into the restaurant between 9:00 AM and 8:00 PM can start a short scene where he teaches you the Milkshake recipe. Bentley also loves Milkshakes as a gift.
- NEW LETTER: a welcome letter from Bentley arrives in the mailbox the first day a save is loaded with this mod (once per player), inviting the farmer to the restaurant near Leah's cottage and Marnie's Ranch.
- MAP: the world map (menu map tab) used to put you on the Farm whenever you were inside the restaurant, because the interior had no world-map entry. Added a Data/WorldMap area so the marker shows in Cindersap Forest. The exact pixel is estimated (100,120 on the valley map) and needs an in-game check.
- Nothing else changed: existing items, IDs, prices, Gus's stock, doors, hours, warps, schedule, art and dialogue are identical to 3.5.4.


## 3.5.4
- NEW ITEM: Chicken Nuggets (cooking item, sells for 70g, edibility 25). Sold ONLY at Bentley's ordering counter for 140g, not at Gus's Saloon and no crafting recipe. Bentley loves them as a gift. New sprite assets/nuggets.png.
- Town Pass: its sell price is now 0g (was 500g, which let you ship it for a profit) and its description says you can drop it. Buying it still opens the door 24/7 permanently through the mail flag. Each purchase now also runs RemoveItem so the book should vanish from your inventory right after buying (untested: if the game adds the book after that action, the book simply stays and you can drop it).
- Friendship: Bentley's CanSocialize is now explicitly "TRUE" (was left unset) so talking and gifting are guaranteed to raise hearts. CanReceiveGifts was already true and CanBeRomanced is still false (non-romanceable NPCs can reach 10 hearts).
- README refreshed (it still described 3.4.1, the old building spot and Content Patcher 2.0.0).
- Nothing else changed: existing items, IDs, prices, Gus's stock, art, doors, hours, warps, schedule and dialogue are identical to 3.5.3.

## 3.5.3
- FIX: the restaurant's roof rows (top 3 tile rows, Forest y 20-22) were only on the Front layer, which draws over the player but has no collision, so you could walk in behind the building with your head hidden in the roof. Those rows are now on the Buildings layer, so the whole 8x7 footprint is solid. The two fully transparent roof corner tiles stay walkable. Applies to all three Forest maps (normal, Ice Festival, Ice Festival 2) since they share one map file.
- Nothing else changed: door tiles, hours, warps, clearing zone, items, art and Bentley are identical to 3.5.2.

## 3.5.2
- Moved the restaurant 10 tiles west (left) so it sits on the open grass left of the bushes: building top-left is now Forest tile 65,20 (door tiles 68-69,26; hours poster 70,25). Interior exit now lands at Forest 68,27 / 69,27. The NPC warps and the clearing zone (tiles 60-77 across, 15-31 down) moved with it. Estimated from a screenshot; verify in-game.

## 3.5.1
- Moved the whole restaurant 5 tiles north: building top-left is now Forest tile 75,20 (door tiles 78-79,26; hours poster 80,25). The interior exit now lands at Forest 78,27 / 79,27, and the NPC warps and the 5-tile clearing zone (tiles 70-87 across, 15-31 down) moved with it. The spot is unverified; check it in-game.

## 3.5.0
- Clears a 5-tile margin around the restaurant (Forest tiles 70-87 across, 20-36 down): the map's Paths layer markers (bushes, weeds, twigs, stumps) are removed there on all three Forest maps. Only the Paths layer is cleared in the margin, so vanilla walls, trees and action tiles nearby are untouched.
- Only affects new saves and locations not yet generated: bushes, weeds and twigs already placed in an existing save stay until removed by hand (axe for bushes, scythe for weeds).

## 3.4.4
- FIX (from a real SMAPI log): the whole Forest restaurant file was ignored because AddNpcWarps needs Content Patcher Format 2.6.0; content.json said 2.0.0. Format raised to 2.6.0 (CP 2.6.0+ required).
- FIX (from the same log): Bentley failed to spawn because TextureName was written as a full path ("Characters/..."), so the game looked for "Portraits/Characters/...". It is now just "BentleyPlayz.FastFoodUsefulStuff_Bentley", so the game loads Characters/ and Portraits/ of that name.

## 3.4.3
- Forest placement split into one patch per map (Forest, Ice Festival, Ice Festival 2) instead of one comma-separated target, so a problem on one map cannot hide the others and `patch summary` names each separately. Same tiles and rules as 3.4.2.

## 3.4.2
- BUG FIX: since 3.0.0 nothing loaded the restaurant interior map (the load lived in the deleted buildings.json). Without it the interior location could not be created, Bentley had no valid home so he never appeared, and the shop/door warps pointed nowhere. Added the missing Load in data/locations.json.
- Forest patch now uses ReplaceByLayer so the vanilla ground tiles stay under the building (Replace also wiped the ground layer).

## 3.4.1
- Town Pass now costs 200g (was 20,000g) and is also sold at Bentley's ordering counter, as well as Pierre's. Still one per player.

## 3.4.0
- Smoking animation redone: he holds an unlit cigarette for a while, puts it in his mouth, lights it with a lighter flame, then loops lit drags, exhales and smoke. Eight frames (16-23) on the normal and winter sheets. The hazmat sheet has no smoking frames, so he just stands there in the suit.
- The Town Pass is back: Pierre sells it for 20,000g (one per player). Owning it, or carrying it, keeps Bentley's front door open 24/7, including while he is out. Without it the door is locked outside 9:00-21:00, which covers the hours he is at the Saloon.
- Pass data is in data/townpass.json; the door override is in data/forest_restaurant.json.

## 3.3.0
- The Saloon animation is now smoking instead of drinking: he holds a cigarette, takes a drag, exhales a puff of smoke and lets it drift up. Frames 16-19 of the normal and winter sheets were redrawn; the hazmat sheet has plain idle frames in 16-19 (no smoking in a respirator). Animation key renamed to Bentley_Smoke.
- Schedule unchanged (Saloon 21,17 from 21:00 to 23:30).

## 3.2.0
- After closing, Bentley now goes to Gus's Stardrop Saloon and stands at tile 21,17 from 21:00 until 23:30, then walks home to the restaurant. Replaces the Marnie/Leah walk from 3.1.0.
- New drinking animation: he raises a beer mug and sips while at the Saloon. Added four frames (16-19) to the bottom of all three sprite sheets (normal, winter, hazmat) and an entry in Data/animationDescriptions.
- The Saloon tile 21,17 came from your screenshot and is unverified; if it is blocked he will stand near it.

## 3.1.0
- Bentley now walks around after closing. Schedule (every day): behind the counter 06:10, leaves at 21:00 for Marnie's Ranch door (Forest 90,16), then Leah's cottage door (104,33) around 21:40, back outside the restaurant (79,32) by 22:30, and inside the kitchen at 23:00. All waypoints are the game's own arrival tiles, which are walkable.
- Added NPC-only warps on the Forest door tiles so he can walk back in (the timed door still applies to players).
- The restaurant is now also placed on the Ice Festival Forest maps (Forest-IceFestival, Forest-IceFestival2). The Flower Dance maps are small overlays whose position I could not confirm, so they are not patched.

## 3.0.0
- The restaurant is no longer a Robin building on the Farm. It now stands in Cindersap Forest (Maps/Forest), top-left tile 75,25 (door tiles 78-79,31), using the same art and the same interior. Removed data/buildings.json; added data/forest_restaurant.json and assets/maps/ForestRestaurant.tmx plus its tilesheet.
- Why: the Forest is a normal NPC route, so Bentley can finally leave the restaurant later without Farm routing problems. His schedule is unchanged for now (he stays inside).
- Opening hours (9:00-21:00) use the same LockedDoorWarp rule on the Forest door tiles; the hours poster and the counter shop are unchanged.
- The interior exit now warps to Forest 78,32 / 79,32.
- Saves that already built the old Farm restaurant: demolish it first or expect an error about a missing building type.

## 2.4.0
- Removed everything Ginger Island: the day-28 trip, the island outfit and its art, and the day-28 Home.
- Removed the Town Pass book (item, Pierre's shop entry, door override, art) and the TownDoorX/TownDoorY config.
- Hazmat and winter outfits, and all other content, are unchanged.

## 2.3.1
- Replaced the NPC-only warps with a day-28 Home: on the 28th the game starts Bentley at a Town tile (TownDoorX/TownDoorY) instead of inside the restaurant, so he joins the island trip without needing to path out of the farm building. Warps removed. All other days unchanged.

## 2.3.0
- Bentley can now leave the restaurant: NPC-only warps (interior <-> Town) so the game's pathfinding never needs the Farm. Config TownDoorX/TownDoorY (default 43,58, an unverified guess) picks the Town tile.
- Monthly Ginger Island trip: Bentley is only allowed to visit the island on day 28 (last day of every season). The game runs the resort routine itself (10:20 AM walk to the docks, arrive ~11:00, swimwear, change back ~5:30 PM, leave ~6:00 PM) and uses his existing island outfit. The game picks resort visitors randomly, so a mod cannot force the visit on a given day.
- New item: Town Pass (20,000g at Pierre's, one per player). Buying it sets a permanent mail flag; the restaurant door then stays open 24/7. Holding the item also works.

## 2.2.0
- Bentley now has outfits: a hazmat suit with respirator (worn during green rain), a winter outfit (winter season), and an island outfit (Ginger Island trips). New files in assets/npc/. data/bentley.json gains six Load patches and an Appearance list. Everything else is unchanged.
- Green rain uses the condition `WEATHER Here GreenRain`. Not yet tested in-game.

## 2.1.0
Goal: let Bentley actually work inside the restaurant, and add real opening hours, without a DLL. Every change below fixes a verified problem or adds a documented feature.

Changed
- Bentley's home is now the restaurant interior (was a Town tile). Why: NPCs cannot path through the Farm, so a schedule cannot walk anyone into a farm building; living inside the interior needs no pathfinding. Removed the `HangoutX`/`HangoutY` config (no longer used).
- Bentley's schedule (`spring`, `default`, `rain`) now starts at 06:10 behind the counter (10,4) and moves to the kitchen (4,4) at 21:00. Start time 06:10 because the schedule docs warn that 06:00 may not trigger.
- The restaurant interior is now a registered global location (`BentleyPlayz.FastFoodUsefulStuff_BentleysRestaurant`, new `data/locations.json`) and the building uses it through `NonInstancedIndoorLocation`. The same interior map is still the building's `IndoorMap` fallback.
- Front door tile (3,3) now has a `LockedDoorWarp` tile action for 9:00-21:00. `HumanDoor` is kept (the game needs it to place the exit).
- Poster right of the door (tile 5,2) shows the opening hours when clicked.
- Counter shop now has an owner list: closed outside 9:00-20:50 with a message. New config `ShopRequiresBentley` (default false): when true the counter opens only while Bentley is inside.
- Only one restaurant can be built (`BuildCondition`), because only one building can use the global interior.
- Interior exit warp fallback changed from `Farm 0 0` to `Farm 64 15` so a player can never be dropped at the map corner. The game normally rewrites it to the building door.
- Building description mentions hours and the one-building limit.

Unchanged
- All items, IDs, sprites, descriptions, recipes, prices, Gus's stock, Robin's free 2-day build, building and interior art, the counter's items and prices, Bentley's dialogue, gift tastes, portraits, sprites, festival option.

## 2.0.2
See previous package.

## Phase 2D - Bentley NPC art redesign
- Redrew assets/npc/Bentley_portraits.png (128x192, six 64x64 expressions) and assets/npc/Bentley_sprites.png (64x128, 16x32 frames).
- No changes to content.json, data/*.json, maps, items, shop or building files. Originals backed up separately.

## 3.8.0 packaging note
- The compiled DLL is now included and both parts ship in one folder, `BentleyPlayz FastFoodUsefulStuff` (`Content/` and `Code/`). Delete the old two folders before installing.

## 3.8.0 Door patch
- Walking onto a door tile no longer enters it. Doors open only when you tap/click them or press the action button, and the closed/locked rules still apply to that.
