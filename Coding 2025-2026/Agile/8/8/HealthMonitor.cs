using System;

namespace HealthMonitorApp;

public class HealthMonitor
{
    private int _hp = 100;
    private readonly Random _random = new();

    public event HealthEventHandler? HealthChanged;

    private EventHandler<int>? _criticalStateReached;
    private EventHandler<int>? _deathOccurred;

    public event EventHandler<int> CriticalStateReached
    {
        add
        {
            _criticalStateReached += value;
            Console.WriteLine($"// подписчик добавлен на CriticalStateReached");
        }
        remove
        {
            _criticalStateReached -= value;
            Console.WriteLine($"// подписчик удалён из CriticalStateReached");
        }
    }

    public event EventHandler<int> DeathOccurred
    {
        add
        {
            _deathOccurred += value;
            Console.WriteLine($"// подписчик добавлен на DeathOccurred");
        }
        remove
        {
            _deathOccurred -= value;
            Console.WriteLine($"// подписчик удалён из DeathOccurred");
        }
    }

    public void Start()
    {
        _hp = 100;
        Console.WriteLine("COIN INSERTED! HP: FULL");

        for (int i = 1; i <= 12; i++)
        {
            int change = _random.Next(2) == 0
                ? -_random.Next(5, 31)
                : _random.Next(3, 21);

            _hp = Math.Clamp(_hp + change, 0, 100);

            HealthChanged?.Invoke(this, _hp);

            if (_hp == 0)
            {
                _deathOccurred?.Invoke(this, _hp);
                Console.WriteLine("YOU ARE DEAD. Try again?");
                break;
            }

            if (_hp < 20 && _hp > 0)
            {
                _criticalStateReached?.Invoke(this, _hp);
            }

            if (i == 12)
                Console.WriteLine("GAME OVER");
        }
    }
}