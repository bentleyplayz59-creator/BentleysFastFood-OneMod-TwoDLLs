using System;
using StardewModdingAPI;
using StardewModdingAPI.Events;
using StardewValley;

namespace BentleyPlayz.FastFoodUsefulStuff.BusStopGuard
{
    /// <summary>
    /// Bus Stop guard feature (a supporting library, started by the original Fast Food ModEntry.Entry via BusStopGuardBootstrap.Initialize). The relocation itself is a Content Patcher
    /// patch of Maps/BusStop (Content/data/busstop_restaurant.json); this mod never re-implements it. It
    /// only checks that the patched tiles are present and, if not, invalidates Maps/BusStop so Content
    /// Patcher re-applies its own patch.
    /// </summary>
    internal sealed class BusStopGuardFeature
    {
        private const string BusStopName = "BusStop";
        private const string BusStopAsset = "Maps/BusStop";
        private const string MainModId = "BentleyPlayz.FastFoodUsefulStuff";

        // Probe tiles taken from Content/data/busstop_restaurant.json (Buildings layer "Action" properties).
        private static readonly (int X, int Y, string Contains)[] Probes =
        {
            (33, 15, "BentleysRestaurant"),
            (34, 15, "BentleysRestaurant"),
            (37, 15, "Bentley's Fast Food"),
        };

        private readonly IModHelper Helper;
        private readonly IMonitor Monitor;
        private readonly ModConfig? SuppliedConfig;
        private ModConfig Config = new();

        private int PendingVerifyTicks = -1;
        private bool ClearedThisVisit;
        private int LastClearDay = -1;
        private bool ForceClear;
        private int AttemptDay = -1;
        private int AttemptsToday;
        private bool WarnedCap;
        private bool WarnedNoCommand;

        public BusStopGuardFeature(IModHelper helper, IMonitor monitor, ModConfig? config)
        {
            this.Helper = helper;
            this.Monitor = monitor;
            this.SuppliedConfig = config;
        }

        public void Start()
        {
            this.Config = this.SuppliedConfig ?? this.LoadConfig();
            IModHelper helper = this.Helper;
            helper.Events.GameLoop.SaveLoaded += this.OnSaveLoaded;
            helper.Events.GameLoop.ReturnedToTitle += (_, _) => this.ResetState();
            helper.Events.GameLoop.DayStarted += this.OnDayStarted;
            helper.Events.GameLoop.UpdateTicked += this.OnUpdateTicked;
            helper.Events.Player.Warped += this.OnWarped;
            helper.Events.Content.AssetReady += this.OnAssetReady;
        }

        /// <summary>Reads BusStopGuard.config.json (separate from the original mod's config.json so the two never overwrite each other).</summary>
        private ModConfig LoadConfig()
        {
            const string file = "BusStopGuard.config.json";
            try
            {
                ModConfig? config = this.Helper.Data.ReadJsonFile<ModConfig>(file);
                if (config == null)
                {
                    // First run: adopt any guard settings someone already put in config.json, then create our own file.
                    config = this.Helper.Data.ReadJsonFile<ModConfig>("config.json") ?? new ModConfig();
                    this.Helper.Data.WriteJsonFile(file, config);
                }
                return config;
            }
            catch (Exception ex)
            {
                this.Monitor.Log($"Could not read {file}, using defaults: {ex.Message}", LogLevel.Warn);
                return new ModConfig();
            }
        }

        private void ResetState()
        {
            this.PendingVerifyTicks = -1;
            this.ClearedThisVisit = false;
            this.LastClearDay = -1;
            this.ForceClear = false;
            this.AttemptDay = -1;
            this.AttemptsToday = 0;
            this.WarnedCap = false;
        }

        private bool Active => this.Config.Enabled && Context.IsWorldReady && this.Helper.ModRegistry.IsLoaded(MainModId);

        private void OnSaveLoaded(object? sender, SaveLoadedEventArgs e)
        {
            this.ResetState();
            this.PendingVerifyTicks = 120;
        }

        private void OnDayStarted(object? sender, DayStartedEventArgs e)
        {
            if (!this.Active)
                return;

            this.AttemptsToday = 0;
            this.WarnedCap = false;
            bool newYear = Game1.year > 1 && Game1.season == Season.Spring && Game1.dayOfMonth == 1;
            if (newYear)
                this.Monitor.Log("New in-game year detected: will verify the Bus Stop relocation.", LogLevel.Info);

            // Wait a moment so Content Patcher finishes its own day-start update before checking.
            this.PendingVerifyTicks = 120;
        }

        private void OnAssetReady(object? sender, AssetReadyEventArgs e)
        {
            if (e.NameWithoutLocale.IsEquivalentTo(BusStopAsset) && this.Active)
                this.PendingVerifyTicks = Math.Max(this.PendingVerifyTicks, 10);
        }

        private void OnWarped(object? sender, WarpedEventArgs e)
        {
            if (!e.IsLocalPlayer || !this.Active)
                return;

            if (e.NewLocation?.NameOrUniqueName == BusStopName)
            {
                this.ClearedThisVisit = false;
                this.PendingVerifyTicks = Math.Max(this.PendingVerifyTicks, 5);
            }
        }

        private void OnUpdateTicked(object? sender, UpdateTickedEventArgs e)
        {
            if (!this.Active)
                return;

            // Scheduled verification (day start, save load, map reload, entering the Bus Stop).
            if (this.PendingVerifyTicks >= 0 && --this.PendingVerifyTicks < 0)
                this.VerifyAndRecover("scheduled check");

            if (!this.InBusStop() || !e.IsMultipleOf((uint)Math.Max(10, this.Config.CheckIntervalTicks)))
                return;

            // Mid-session reset detection while standing in the Bus Stop.
            if (this.PendingVerifyTicks < 0 && !this.IsRelocationApplied())
            {
                this.VerifyAndRecover("relocation missing while in Bus Stop");
                return;
            }

            this.TryClear();
        }

        private bool InBusStop() => Game1.currentLocation?.NameOrUniqueName == BusStopName;

        /// <summary>True when the Content Patcher relocation edits are present in the live Bus Stop map.</summary>
        private bool IsRelocationApplied()
        {
            GameLocation? loc = Game1.getLocationFromName(BusStopName);
            if (loc?.Map == null)
                return false;

            foreach (var (x, y, contains) in Probes)
            {
                string? value = loc.doesTileHaveProperty(x, y, "Action", "Buildings");
                if (value == null || !value.Contains(contains))
                    return false;
            }
            return true;
        }

        private void VerifyAndRecover(string reason)
        {
            if (this.IsRelocationApplied())
            {
                if (this.Config.VerboseLogging)
                    this.Monitor.Log($"Relocation intact ({reason}).", LogLevel.Debug);
                return;
            }

            int day = Game1.Date.TotalDays;
            if (this.AttemptDay != day)
            {
                this.AttemptDay = day;
                this.AttemptsToday = 0;
            }

            if (this.AttemptsToday >= this.Config.MaxRecoveryAttemptsPerDay)
            {
                if (!this.WarnedCap)
                {
                    this.Monitor.Log($"Relocation still missing after {this.AttemptsToday} reload attempts today; giving up until tomorrow.", LogLevel.Warn);
                    this.WarnedCap = true;
                }
                return;
            }

            this.AttemptsToday++;
            this.Monitor.Log($"Bus Stop relocation missing ({reason}). Reloading {BusStopAsset} so Content Patcher re-applies it (attempt {this.AttemptsToday}).", LogLevel.Warn);
            this.Helper.GameContent.InvalidateCache(BusStopAsset);
            this.ForceClear = true;
            this.PendingVerifyTicks = 45; // check again after the reload has propagated
        }

        private void TryClear()
        {
            if (!Context.IsMainPlayer || !Context.IsPlayerFree || this.ClearedThisVisit)
                return;
            if (this.PendingVerifyTicks >= 0 || !this.IsRelocationApplied())
                return; // never clear unless the restaurant is confirmed in place

            int day = Game1.Date.TotalDays;
            if (!this.ForceClear && this.Config.ClearOncePerDay && this.LastClearDay == day)
            {
                this.ClearedThisVisit = true;
                return;
            }

            string[] args = this.Config.ClearArguments is { Length: > 0 } ? this.Config.ClearArguments : new[] { "current", "everything" };
            bool found = this.Helper.ConsoleCommands.Trigger("world_clear", args);
            this.ClearedThisVisit = true;
            this.LastClearDay = day;
            this.ForceClear = false;

            if (found)
                this.Monitor.Log($"Ran 'world_clear {string.Join(" ", args)}' in the Bus Stop.", LogLevel.Info);
            else if (!this.WarnedNoCommand)
            {
                this.WarnedNoCommand = true;
                this.Monitor.Log("The 'world_clear' command is not registered (is Console Commands installed?).", LogLevel.Warn);
            }
        }
    }
}
