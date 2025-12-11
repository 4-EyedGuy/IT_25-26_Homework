public class BasicParcel : IParcel
{
    private string code = "";
    private int weight;
    private bool isDamaged;

    public string Code { get => code; set => code = value; }
    public int Weight { get => weight; set => weight = value; }
    public bool IsDamaged { get => isDamaged; set => isDamaged = value; }
}
