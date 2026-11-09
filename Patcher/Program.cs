using System;
using System.IO;
using System.Linq;
using Mono.Cecil;
using Mono.Cecil.Cil;

// Build-time tool. Adds ONE call at the start of the original Fast Food ModEntry.Entry(IModHelper):
//     BusStopGuardBootstrap.Initialize(helper, this.Monitor);
// Nothing else in the original DLL is changed.
internal static class Program
{
    private const string OriginalEntryType = "BentleyPlayz.FastFoodUsefulStuff.Smapi.ModEntry";
    private const string GuardBootstrapType = "BentleyPlayz.FastFoodUsefulStuff.BusStopGuard.BusStopGuardBootstrap";

    private static int Main(string[] args)
    {
        try
        {
            if (args.Length == 4 && args[0] == "patch")
                return Patch(args[1], args[2], args[3]);
            if (args.Length == 4 && args[0] == "verify")
                return Verify(args[1], args[2], args[3]);
            Console.Error.WriteLine("usage: patch <original.dll> <guard.dll> <out.dll> | verify <patched.dll> <guard.dll> <original.dll>");
            return 2;
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine("FAILED: " + ex);
            return 1;
        }
    }

    private static MethodDefinition FindEntry(ModuleDefinition module)
    {
        TypeDefinition type = module.GetType(OriginalEntryType)
            ?? throw new Exception("Original entry type not found: " + OriginalEntryType);
        return type.Methods.Single(m => m.Name == "Entry" && m.Parameters.Count == 1 && m.HasBody);
    }

    private static int Patch(string originalPath, string guardPath, string outPath)
    {
        using ModuleDefinition guard = ModuleDefinition.ReadModule(guardPath);
        MethodDefinition init = guard.GetType(GuardBootstrapType).Methods
            .Single(m => m.Name == "Initialize" && m.Parameters.Count == 2);

        ModuleDefinition module = ModuleDefinition.ReadModule(originalPath, new ReaderParameters { InMemory = true });
        MethodDefinition entry = FindEntry(module);
        MethodReference initRef = module.ImportReference(init);

        if (entry.Body.Instructions.Any(i => i.Operand is MethodReference r && r.Name == "Initialize" && r.DeclaringType.FullName == GuardBootstrapType))
        {
            Console.WriteLine("Already patched; copying unchanged.");
            File.Copy(originalPath, outPath, true);
            return 0;
        }

        // this.Monitor getter: reuse the reference the original already uses, else build one.
        MethodReference getMonitor = module.GetTypes().Where(t => t.HasMethods).SelectMany(t => t.Methods).Where(m => m.HasBody)
            .SelectMany(m => m.Body.Instructions).Select(i => i.Operand).OfType<MethodReference>()
            .FirstOrDefault(r => r.Name == "get_Monitor" && r.DeclaringType.FullName == "StardewModdingAPI.Mod");
        if (getMonitor == null)
        {
            TypeReference modRef = module.GetTypeReferences().FirstOrDefault(t => t.FullName == "StardewModdingAPI.Mod")
                ?? throw new Exception("StardewModdingAPI.Mod reference not found in the original DLL.");
            TypeReference monitorRef = module.GetTypeReferences().FirstOrDefault(t => t.FullName == "StardewModdingAPI.IMonitor")
                ?? new TypeReference("StardewModdingAPI", "IMonitor", module, modRef.Scope);
            getMonitor = new MethodReference("get_Monitor", monitorRef, modRef) { HasThis = true };
        }

        ILProcessor il = entry.Body.GetILProcessor();
        Instruction first = entry.Body.Instructions[0];
        il.InsertBefore(first, il.Create(OpCodes.Ldarg_1));          // helper
        il.InsertBefore(first, il.Create(OpCodes.Ldarg_0));          // this
        il.InsertBefore(first, il.Create(OpCodes.Call, getMonitor)); // this.Monitor
        il.InsertBefore(first, il.Create(OpCodes.Call, initRef));    // BusStopGuardBootstrap.Initialize(helper, monitor)
        entry.Body.MaxStackSize = Math.Max(entry.Body.MaxStackSize, 4);

        module.Write(outPath);
        Console.WriteLine("Patched " + entry.FullName + " -> " + outPath);
        return 0;
    }

    private static int Verify(string patchedPath, string guardPath, string originalPath)
    {
        using ModuleDefinition patched = ModuleDefinition.ReadModule(patchedPath);
        using ModuleDefinition guard = ModuleDefinition.ReadModule(guardPath);
        using ModuleDefinition original = ModuleDefinition.ReadModule(originalPath);

        Fail(guard.GetTypes().Any(t => t.BaseType != null && t.BaseType.FullName == "StardewModdingAPI.Mod"),
            "BusStopGuard still contains a SMAPI Mod subclass.");
        Fail(guard.GetType(GuardBootstrapType) == null || !guard.GetType(GuardBootstrapType).IsPublic,
            "BusStopGuardBootstrap is missing or not public.");

        string guardName = guard.Assembly.Name.Name;
        Fail(!patched.AssemblyReferences.Any(a => a.Name == guardName), "Patched DLL has no reference to " + guardName);

        MethodDefinition entry = FindEntry(patched);
        var ins = entry.Body.Instructions;
        bool callsInit = ins.Take(6).Any(i => i.Operand is MethodReference r && r.Name == "Initialize" && r.DeclaringType.FullName == GuardBootstrapType);
        Fail(!callsInit, "Entry() does not call BusStopGuardBootstrap.Initialize at its start.");

        int origMethods = original.GetTypes().Sum(t => t.Methods.Count);
        int patchedMethods = patched.GetTypes().Sum(t => t.Methods.Count);
        Fail(origMethods != patchedMethods, $"Method count changed: {origMethods} -> {patchedMethods}");
        Fail(original.GetTypes().Count() != patched.GetTypes().Count(), "Type count changed.");

        Console.WriteLine($"VERIFIED: Entry() calls {GuardBootstrapType}.Initialize; guard is a plain library; original has {origMethods} methods in both versions.");
        return 0;
    }

    private static void Fail(bool condition, string message)
    {
        if (condition)
            throw new Exception("VERIFY FAILED: " + message);
    }
}
