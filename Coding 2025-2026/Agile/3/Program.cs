using System;

abstract class Instrument
{
    public string InstrumentName { get; set; }
    public string Material { get; set; }

    public Instrument(string instrumentName, string material)
    {
        InstrumentName = instrumentName;
        Material = material;
    }

    public abstract string PlayMusic();
}

class Piano : Instrument
{
    public int KeyCount { get; set; }

    public Piano(string instrumentName, string material, int keyCount)
        : base(instrumentName, material)
    {
        KeyCount = keyCount;
    }

    public override string PlayMusic()
    {
        return $"Играет: {InstrumentName} ({KeyCount} клавиш, {Material}).";
    }
}

class Guitar : Instrument
{
    public int StringCount { get; set; }

    public Guitar(string instrumentName, string material, int stringCount)
        : base(instrumentName, material)
    {
        StringCount = stringCount;
    }

    public override string PlayMusic()
    {
        return $"Играет: {InstrumentName} ({StringCount} струн, {Material}).";
    }
}

class Program
{
    static void Main()
    {
        Instrument piano = new Piano("Пианино", "дерево", 88);
        Instrument guitar = new Guitar("Гитара", "дерево", 12);

        Console.WriteLine(piano.PlayMusic());
        Console.WriteLine(guitar.PlayMusic());
    }
}
