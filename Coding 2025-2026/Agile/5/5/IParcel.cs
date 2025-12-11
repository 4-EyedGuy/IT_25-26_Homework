public interface IParcel
{
    string Code { get; set; }
    int Weight { get; set; }
    bool IsDamaged { get; set; }

    void MarkDamaged(int severity)
    {
        if (severity > 0)
            IsDamaged = true;
    }
}