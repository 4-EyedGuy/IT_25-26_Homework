public class Phone
{
    public string Brand { get; set; }
    public string SerialNumber { get; set; }
    public int ChargeLevel { get; private set; }

    public Phone(string brand, string serialnumber, int chargelevel)
    {
        Brand = brand;
        SerialNumber = serialnumber;
        ChargeLevel = chargelevel;
    }

    public void ChargingSoHard(int amount)
    {
        ChargeLevel += amount;
        if (ChargeLevel > 100)
        {
            ChargeLevel = 100;
        }
    }

    public override string ToString()
    {
        return $"Бренд: {Brand}, Серийный номер: {SerialNumber}, Уровень заряда батареи: {ChargeLevel}%";
    }
}