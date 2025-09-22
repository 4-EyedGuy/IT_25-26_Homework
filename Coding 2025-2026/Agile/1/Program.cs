public class Program
{
    static void Main(string[] args)
    {
        Phone phone = new Phone("IPhone", "353031114750118", 24);
        Console.WriteLine(phone);

        phone.ChargingSoHard(13);
        Console.WriteLine(phone);

        phone.ChargingSoHard(47);
        Console.WriteLine(phone);

        phone.ChargingSoHard(86);
        Console.WriteLine(phone);
    }
}