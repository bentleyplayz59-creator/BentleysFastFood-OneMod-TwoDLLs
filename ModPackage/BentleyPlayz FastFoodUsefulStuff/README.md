# Bentley Playz Fast Food & Useful Stuff 3.13.4 (the Code part still writes extra [DEV] lines to the SMAPI log, see DEV_LOGGING.md)

One mod, one folder. Copy this whole folder into your game's `Mods` folder:

```
Mods/BentleyPlayz FastFoodUsefulStuff/
  Content/   items, maps, shop, Bentley, art      (loaded by Content Patcher)
  Code/      doors, Windex drinking damage, announcement   (compiled DLL, loaded by SMAPI)
             announcement.json = the update announcement text (edit it, no recompiling)
```
Stardew needs art/data and code to be loaded by two different loaders, so the folder holds two parts. They share one name, one version and one install step, and SMAPI loads both from this folder automatically.

## Install / update
1. DELETE the old folders first: `BentleyPlayz_FastFoodUsefulStuff` and `BentleyPlayz_FastFoodUsefulStuff_SMAPI` (and any older copy of this mod).
2. Unzip so that the folder `BentleyPlayz FastFoodUsefulStuff` sits directly inside your game's `Mods` folder.
3. Requirements: Stardew Valley 1.6.15, SMAPI 4.1.10+, Content Patcher 2.6.0+.

Saves keep working: the UniqueIDs are unchanged.

See `Content/CHANGELOG.md` and `Content/TEST_REPORT.md`. Version 3.11.2 was tested in game by the author; 3.13.2 (Dessert Corner, new desserts, Windex damage fix, restaurant coordinate shift) and 3.13.3 (Dessert Corner / arcade visual polish) have not been tested in game yet.
