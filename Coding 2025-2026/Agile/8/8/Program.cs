using HealthMonitorApp;

var monitor = new HealthMonitor();
var hud = new ConsoleHUD();
var stats = new SurvivalStats();

monitor.HealthChanged += hud.OnHealthChanged;
monitor.CriticalStateReached += hud.OnCriticalStateReached;
monitor.DeathOccurred += hud.OnDeathOccurred;

monitor.HealthChanged += stats.OnHealthChanged;

monitor.Start();

Console.WriteLine("\n// HUD отпысывается от критического события");
monitor.CriticalStateReached -= hud.OnCriticalStateReached;

stats.Report();

Console.WriteLine("\nНажмите любую клавишу для выхода...");
Console.ReadKey();