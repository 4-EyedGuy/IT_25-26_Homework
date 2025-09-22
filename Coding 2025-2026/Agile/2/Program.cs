using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        Museum museum = new Museum("Московский музей современного искусства", 20000);

        Exhibit exhibit1 = new Exhibit(1, "Цветок-Гибрид", "Александр Позин");
        Exhibit exhibit2 = new Exhibit(2, "Между конкретным и беспредельным", "Евгений Гороховский");
        Exhibit exhibit3 = new Exhibit(3, "Жизнь", "Ирина Затуловская");

        museum.AddExhibit(exhibit1);
        museum.AddExhibit(exhibit2);
        museum.AddExhibit(exhibit3);

        Console.WriteLine(museum);
    }
}
