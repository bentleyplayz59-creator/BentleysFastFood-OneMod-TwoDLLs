# Test report - 3.13.3 (NOT tested in game) + 3.13.2 (NOT tested in game) + 3.11.2 (tested in game)

**3.13.3 note (Dessert Corner / arcade visual polish):** checked outside the game only. The game, SMAPI and Content Patcher were not available, so no SMAPI log was read.

## 3.13.3 checked outside the game
- [x] All JSON files parse (content.json, manifests, every data file, announcement.json).
- [x] Both manifests say 3.13.3-dev. The DLL is byte-identical to 3.13.2-dev.
- [x] FastFoodInterior_v4.tmx is well-formed XML, 32x14, every tile id is inside its tileset (z_DessertCorner 2530-2561). Content Patcher targets and FromFile paths are unchanged and every FromFile exists.
- [x] z_DessertCorner.png is 128x64, which matches the tileset entry in the TMX (tilecount 32, 8 columns). Tiles 0, 1 and 11-16 are pixel-identical to 3.13.2.
- [x] Only 12 tiles differ in the dessert room plus the 3 arcade sign tiles; everything else in the map is identical to the 3.13.2 map.
- [x] Collision: the Buildings layer is identical to 3.13.2 for every non-dessert tile; in the dessert room the only Buildings change is the three board tiles at 2-4,3 (still solid). Walkable area reachable from the dessert doorway (6,9) is the same as before.
- [x] Kiosk: OpenShop {{ModId}}_DessertKiosk is still on 2-4,4, all three on solid Buildings tiles; shop id {{ModId}}_DessertKiosk still exists in data/dessert_corner.json.
- [x] Arcade: Arcade_Prairie (27,3-4) and Arcade_Minecart (29,3-4) are untouched and still on non-empty Buildings tiles. The sign is on the Front layer at 27-29,1 over plain wall tiles; rows 0 and 2 of that column are not touched.
- [x] Seating: the two new Data/ChairTiles keys match the chair tiles' position in z_DessertCorner (tile 19 = 3/2, tile 20 = 4/2) and the direction convention of the dining-room chairs.
- [x] No new files are loaded by the game, no new dependency, no code change.

## 3.13.3 needs an in-game test
- [ ] Walk into the Dessert Corner: sign reads DESSERT, awning, ORDER HERE board, counter items and floor mat all draw correctly, nothing flickers or draws over the player.
- [ ] Stand on the mat (2,5 / 3,5 / 4,5), face up and use the action button / tap the counter: the dessert shop opens and buying works.
- [ ] Both tables are solid; walk between and around them; sit on all four dessert chairs and get up again.
- [ ] Arcade: the sign looks right one tile higher (against the vanilla art), and both cabinets still launch their games.
- [ ] Check on Android as well as PC (only PNG tile art and a TMX were changed, no code).
- [ ] SMAPI log has no new errors or warnings; run `patch summary` in the SMAPI console.

---- Older report below ----

**3.13.2 note:** Windex and cone damage each have their own config value.

**3.13.1 note:** the DLL was patched outside the game (IL checked, both item IDs present, JSON parses). Needs an in-game test: Windex and the Windex Swirl Cone each take 10 health once, never below 1 HP.

**3.13.0 note:** nothing in 3.12.1 or 3.13.0 has been run in game. Checked outside the game: JSON parses, the map is 32x14 with every tile id inside its tileset, no file refers to the removed furniture, desserts have sprites and shop entries. Needs an in-game test: dessert icons show in the shop, inventory and when held; kiosk opens from tiles 2-4,4; Windex and the Windex Swirl Cone really take health; plus every item from the 3.12.1 list below.

**3.12.1 note:** the left room was moved into the restaurant map and every restaurant coordinate shifted +6 tiles. The checks done outside the game are listed below; nothing about 3.12.1 has been run in game.

## 3.12.1 checked outside the game
- [x] All JSON files parse; the new map file is well-formed, 32x14, every tile id is inside its tileset (z_FurnitureWing placed after the arcade wall tileset).
- [x] No file still refers to the removed FurnitureWing location, map or door tile.
- [x] Every restaurant coordinate in the data files was moved +6 in x (list in CHANGELOG.md); a search for the old values finds none left.
- [x] DLL: the six hard-coded Point constants were listed before and after the byte patch; only the three restaurant ones changed (9,12 twice -> 15,12; 16,3 -> 22,3; 17,3 -> 23,3). The Forest door tiles (68,25 / 69,25) and the bedroom arrival points (6,9 / 7,9) are unchanged. File size unchanged.

## 3.12.1 needs an in-game test
- [ ] Walk in from the Forest: you arrive at the front door (15,12).
- [ ] Left doorway (6,9) is walkable both ways, no loading screen, and both rooms are lit.
- [ ] ATM (3,4) opens the furniture shop; you can walk to it; nothing blocks the corridor on row 9.
- [ ] Counter shop, arcade cabinets, seating, staff door and Bentley's bedroom still work.
- [ ] Bentley and the Robot appear at 16,4 / 15,4 and their schedules still run.
- [ ] The Milkshake lesson event starts with everybody in the right place.

## Known limits (3.12.1)
- The DLL was patched at byte level, not rebuilt from source. If you have the source, update the three constants there too.
- A save made inside the restaurant before updating loads you at the old tile coordinates.

---- Older report below (3.11.2) ----

**Tested in game by the author (Bentley Playz): everything works.** Stardew Valley 1.6.15, SMAPI 4.1.10+, Content Patcher 2.6.0+.

## Confirmed in game
- [x] The mod compiles and loads (Code part DLL + Content part), no SMAPI errors.
- [x] Main entrance / exit and bedroom entrance / exit, including the staff-door warp into Bentley's bedroom.
- [x] Doors: tap / action key / custom keybinding open and use doors.
- [x] Arcade room (doorway at 19,9; Journey of the Prairie King and Junimo Kart cabinets) and its lighting.
- [x] Restaurant lighting (evenly spaced lights across the dining room, kitchen and arcade).
- [x] Restaurant Robot and Bentley schedules (robot works the counter while Bentley is away; no walking through each other).
- [x] Counter shop, items, recipes, seating, Bentley events and dialogue.
- [x] Windex drinking damage.
- [x] Update announcement shows once per version and does not return on the next load.
- [x] `patch summary` shows no problems.

## Checked outside the game
- [x] All JSON files parse; the maps are well-formed; every tile id used is inside its tileset.
- [x] Exterior files are byte-identical to earlier versions.

## Version housekeeping (3.11.2)
- Both manifests and both READMEs now say 3.11.2.
- The compiled DLL's internal file-version label still reads 3.9.0. This is cosmetic: SMAPI and the announcement use the manifest version, and the DLL code has not changed since it was last built.

## Known limits
- Android / mobile with a custom DLL is not covered by this report.
- Exits and Bentley's NPC warps remain map warps (NPC pathfinding needs them).
