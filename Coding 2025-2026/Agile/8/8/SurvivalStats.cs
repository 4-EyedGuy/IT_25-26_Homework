using System;

namespace HealthMonitorApp;

public class SurvivalStats
{
    private int _criticalZoneCount = 0;

    public void OnHealthChanged(HealthMonitor sender, int hp)
    {
        if (hp >= 1 && hp <= 19)
            _criticalZoneCount++;
    }

    public void Report()
    {
        Console.WriteLine($"\nСтатистика: критических состояний (1..19 HP): {_criticalZoneCount}");
    }
}