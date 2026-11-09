# Bentley's Fast Food & Useful Stuff - build repo

Result: ONE SMAPI mod (`BentleyPlayz FastFoodUsefulStuff/`, original manifests unchanged), TWO DLLs in `Code/`:
- `BentleyPlayz.FastFoodUsefulStuff.Smapi.dll` - the original entry DLL (its `Entry()` now also calls the guard).
- `BentleyPlayz.FastFoodUsefulStuff.BusStopGuard.dll` - plain library (no Mod class, no manifest).

The original DLL has no source, so `Patcher/` (Mono.Cecil) adds one call at the start of `ModEntry.Entry`:
`BusStopGuardBootstrap.Initialize(helper, this.Monitor)`. The workflow then verifies the patch and the package.

- `lib/` original DLL (input) - `BusStopGuard/` library source - `Patcher/` build tool - `ModPackage/` original mod files, no DLLs.
- Run the workflow, download artifact `BentleysFastFood-FullMod-with-BusStopGuard`, unzip into `Mods/`.
- Guard settings: `Code/BusStopGuard.config.json` (created on first launch).
