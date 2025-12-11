public class CourierParcel : IParcel, ITrackable
{
    private string code = "";
    private int weight;
    private bool isDamaged;
    private string trackingId = "";
    private int fragility;

    public string Code
    {
        get => code;
        set => code = value;
    }

    public int Weight
    {
        get => weight;
        set => weight = value;
    }

    public bool IsDamaged
    {
        get => isDamaged;
        set => isDamaged = value;
    }

    public string TrackingId
    {
        get => trackingId;
        set => trackingId = value;
    }

    public int Fragility
    {
        get => fragility;
        set
        {
            if (value < 0) fragility = 0;
            else if (value > 10) fragility = 10;
            else fragility = value;
        }
    }

    public void MarkDamaged(int severity)
    {
        int effectiveSeverity = severity + Fragility / 3;
        if (effectiveSeverity > 0)
            IsDamaged = true;
    }

    public void AddCheckpoint(string note)
    {
        Console.WriteLine($"[{TrackingId}] {note}");
    }
}
