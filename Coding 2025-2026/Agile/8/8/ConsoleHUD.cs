using System;

namespace HealthMonitorApp;

public class ConsoleHUD
{
    public void OnHealthChanged(HealthMonitor sender, int hp)
    {
        Console.WriteLine($"HP: {hp}");
    }

    public void OnCriticalStateReached(object? sender, int hp)
    {
        Console.ForegroundColor = ConsoleColor.Red;
        Console.WriteLine($"HP: {hp}. Look for heals!");
        Console.ResetColor();
    }

    public void OnDeathOccurred(object? sender, int hp)
    {
        Console.ForegroundColor = ConsoleColor.DarkRed;
        Console.WriteLine($"HP: {hp}.....");
        Console.ResetColor();
    }
}