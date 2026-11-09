namespace BentleyPlayz.FastFoodUsefulStuff.BusStopGuard
{
    public sealed class ModConfig
    {
        /// <summary>Master switch.</summary>
        public bool Enabled { get; set; } = true;

        /// <summary>Clear at most once per in-game day (a recovery always allows one more clear). Clearing removes only trees and bushes.</summary>
        public bool ClearOncePerDay { get; set; } = true;

        /// <summary>While in the Bus Stop, how often (ticks) the relocation state is re-checked.</summary>
        public int CheckIntervalTicks { get; set; } = 60;

        /// <summary>Safety cap on map reloads per in-game day, so a failing check can never loop.</summary>
        public int MaxRecoveryAttemptsPerDay { get; set; } = 3;

        /// <summary>Log extra detail.</summary>
        public bool VerboseLogging { get; set; } = false;
    }
}
