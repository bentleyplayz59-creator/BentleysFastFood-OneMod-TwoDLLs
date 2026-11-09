using System;
using StardewModdingAPI;

namespace BentleyPlayz.FastFoodUsefulStuff.BusStopGuard
{
    /// <summary>
    /// Public entry point of the BusStopGuard supporting library. This assembly is NOT a SMAPI mod (no Mod
    /// subclass, no manifest). The original Fast Food ModEntry.Entry calls Initialize(), so everything runs
    /// inside the one Fast Food mod.
    /// </summary>
    public static class BusStopGuardBootstrap
    {
        private static bool Started;

        /// <summary>Starts the guard using BusStopGuard.config.json for its settings.</summary>
        public static void Initialize(IModHelper helper, IMonitor monitor)
            => Initialize(helper, monitor, null);

        /// <summary>Starts the guard. <paramref name="config"/> may be null to read BusStopGuard.config.json.</summary>
        public static void Initialize(IModHelper helper, IMonitor monitor, ModConfig? config)
        {
            if (Started)
                return;
            Started = true;

            try
            {
                new BusStopGuardFeature(helper, monitor, config).Start();
                monitor.Log("Bus Stop guard started (part of Bentley's Fast Food).", LogLevel.Debug);
            }
            catch (Exception ex)
            {
                monitor.Log($"Bus Stop guard failed to start: {ex}", LogLevel.Error);
            }
        }
    }
}
