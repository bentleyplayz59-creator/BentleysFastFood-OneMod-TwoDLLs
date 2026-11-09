# 3.13.4: what gets logged

This is a developer build. It behaves like 3.13.3, but the Code part writes a lot of extra lines to the SMAPI log, all tagged `[DEV]` (shown under the name "Bentley's Fast Food (code part)"). They appear in the SMAPI console and in the log file:
`%appdata%\StardewValley\ErrorLogs\SMAPI-latest.txt` (Windows). After testing, send that file.

## Logged at startup
- DEV BUILD loaded, the mod version, and the two loaded config values (WindexDrinkDamage, WindexSwirlConeDamage). If the config line says 0, damage is switched off by your config.json.
- Each event fired: GameLaunched (and whether the Content Patcher pack is loaded), SaveLoaded, ReturnedToTitle.
- Entry finished, with the console commands registered.

## Logged while playing
- World ready changes, and every change of the player's health ("player health changed: 100 -> 90"), whatever the cause.
- Every time you start or stop eating/drinking anything: `isEating changed`, the exact `itemToEat` id, and your health at that moment. This shows whether the mod can see the item at all.
- Windex detection: `DETECTED Windex/cone being consumed. is cone = true/false`.
- Damage: `finished consuming ... applying damage now`, `ApplyDamage called`, `damage setting used = N`, `health before -> after damage`, and the original "Windex drunk" line.
- Doors: action button near a door tile, too far away, `UseDoor` with the door id, hearts with Bentley for the bedroom, whether the door is unlocked, and the message shown if locked.
- Update announcement: when it is shown.
- A heartbeat line about every 30 seconds while a save is loaded, so you can tell the mod is alive.
- Any error in the damage code is logged as an error with the exception text.

## Expected lines when drinking Windex
```
[DEV] isEating changed -> true
[DEV] itemToEat = (O)BentleyPlayz.FastFoodUsefulStuff_Windex
[DEV] DETECTED Windex/cone being consumed. is cone = false
[DEV] isEating changed -> false
[DEV] finished consuming a Windex item, applying damage now
[DEV] ApplyDamage called. item is cone = false
[DEV] damage setting used = 10
[DEV] health before -> after damage: 100 -> 90
```
For the Windex Swirl Cone the id ends in `_WindexSwirlCone` and `is cone = true`.

## How to read a failure
- No `itemToEat` line at all: the mod cannot see eating (detection problem).
- `itemToEat` is the right id but no DETECTED line: the id check failed (send me the exact id).
- DETECTED but no `ApplyDamage called`: the "finished eating" step never happened.
- `damage setting used = 0`: your config.json has 0 for that item.
- ApplyDamage ran and health did not change in the next "player health changed" line: something restored it.
- Nothing `[DEV]` at all: the DLL did not load; look for red errors near the top of the log.

## Console commands (type in the SMAPI console)
- `bentley_windex_test` pretends you just drank Windex, `bentley_windex_test cone` pretends you ate the cone. This runs only the damage code, so it shows whether damage works even if eating detection does not. Needs a loaded save.
- `bentley_announcement show` / `reset` as before.
