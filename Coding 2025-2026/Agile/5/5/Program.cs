using System;

class Program
{
    static void Main()
    {
        IParcel parcel1 = new BasicParcel
        {
            Code = "B001",
            Weight = 200
        };
        parcel1.MarkDamaged(0);
        Console.WriteLine($"BasicParcel damaged: {parcel1.IsDamaged}");
        parcel1.MarkDamaged(1);
        Console.WriteLine($"BasicParcel damaged (after severity 1): {parcel1.IsDamaged}");

        var parcel2 = new CourierParcel
        {
            Code = "C001",
            Weight = 150,
            TrackingId = "TRK123",
            Fragility = 9
        };
        parcel2.MarkDamaged(0);
        Console.WriteLine($"CourierParcel damaged (fragility=9, severity=0): {parcel2.IsDamaged}");
        parcel2.AddCheckpoint("Package received at facility");

        var parcel3 = new CourierParcel
        {
            Code = "C002",
            Weight = 300,
            TrackingId = "TRK456",
            Fragility = 3
        };
        parcel3.MarkDamaged(0);
        Console.WriteLine($"CourierParcel damaged (fragility=3, severity=0): {parcel3.IsDamaged}");
        parcel3.AddCheckpoint("In transit");
    }
}