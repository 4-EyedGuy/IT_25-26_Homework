namespace PayrollSystem;

public class PayrollContext
{
    public int Base { get; set; }
    public int Bonus { get; set; }
    public int Penalty { get; set; }
    public int Final { get; set; }

    public override string ToString()
    {
        return $"Base: {Base}, Bonus: {Bonus}, Penalty: {Penalty}, Final: {Final}";
    }
}