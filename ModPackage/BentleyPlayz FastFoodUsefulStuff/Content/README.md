# Bentley Playz Fast Food & Useful Stuff (3.13.4)
Made by Bentley Playz. One mod: this Content part (Content Patcher) plus the Code part in the sibling `Code` folder (doors, Windex drinking damage, update announcement).

## Requirements
- Stardew Valley 1.6.15 (other 1.6.x builds untested)
- SMAPI 4.1.10+
- Content Patcher 2.6.0+
- The `Code` folder next to this one (it holds `BentleyPlayz.FastFoodUsefulStuff.Smapi.dll`; this pack will not load without it)
No other framework is needed.

## Install
1. Put the whole `BentleyPlayz FastFoodUsefulStuff` folder (with `Content` and `Code` inside) directly in `Mods`.
2. Keep only one copy (all versions use the same mod ID); delete older folders first.
3. Start the game with SMAPI.

## What it adds
- Items: Cheeseburger, French Fries, Coke, Windex (joke), Farmhand Snack Pack (all sold at Gus's Saloon and Bentley's counter), and Chicken Nuggets (Bentley's counter only), and Milkshake (cannot be bought; you cook it after Bentley teaches you the recipe at 4 hearts).
- Bentley's Fast Food, a walk-in restaurant in Cindersap Forest (top-left tile 65,20; door tiles 68-69,26). No building step. Also placed on the Ice Festival Forest maps.
- Bentley, the restaurant owner, with portraits and sprites, a winter outfit and a hazmat outfit for green rain. He works behind the counter from the early morning; after closing he goes to Gus's Saloon until about 23:30, then home.
- Arcade corner (3.11+): a small room on the right side of the dining room with Journey of the Prairie King and Junimo Kart.
- Dessert Corner (3.13.0, restyled in 3.13.3): a room on the left of the restaurant, the mirror image of the arcade, part of the same map (no loading screen), doorway at tile 6,9. A DESSERT sign, a striped awning, an ORDER HERE menu board and a pink floor mat lead to the kiosk counter (stand on the mat, tiles 2-4,5, and face the counter), which sells 7 desserts: Ice Cream Sundae, Soft Serve Cone, Fudge Brownie, Strawberry Cheesecake, Glazed Donut, Banana Split and the Windex Swirl Cone (vanilla with a blue swirl; it hurts).
- Seating: you can sit on every chair and booth in the restaurant, including the pink Dessert Corner chairs (tap / right-click / action button).
- Bentley's Bedroom: a private room behind the restaurant, through the staff door in the kitchen wall. The door is not locked. He sleeps there at night.
- Open 24 hours a day, every day: the front door, the counter shop and the poster next to the door never close.
- A welcome letter from Bentley arrives on the first day you load a save with this mod.
- The Town Pass has been removed (the restaurant is open 24/7). Any leftover Town Pass in an existing save is deleted once.

## Config (`config.json` after first run, or Generic Mod Config Menu)
- `EnableFestivals`: experimental, default off.

## Testing status
3.11.2 was tested in game by the author. 3.13.2 (Windex damage fix) and 3.13.3 (Dessert Corner / arcade visual polish) are not tested in game yet. See TEST_REPORT.md.

## Windex
Windex and the Windex Swirl Cone are joke items. When you finish consuming one, the Code part takes health: `WindexDrinkDamage` for Windex and `WindexSwirlConeDamage` for the Windex Swirl Cone (both default 10, set them in the Code folder's config.json; 0 = none; it never takes you below 1 health). Both items have Edibility 0, so the game adds no extra damage on top. If you copy an old config.json over this version, make sure Windex says 10, not 0 (the cone setting is added automatically). Windex has no spray attack.

## Notes
- Windex is a fictional joke item. Real glass cleaner is poisonous; never drink it.
- Bushes, weeds and twigs already in an existing save stay until removed by hand.
