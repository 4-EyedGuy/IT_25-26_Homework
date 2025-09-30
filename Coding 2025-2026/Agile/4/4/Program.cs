using System;

namespace Documents
{
    class Program
    {
        static void Main()
        {
            Report r = new Report
            {
                Title = "Annual Report",
                Content = "This is the annual report content.",
                Author = "Alice"
            };
            Console.WriteLine(r.Print());
            Console.WriteLine("Word count: " + r.WordCount());

            Note n = new Note
            {
                Title = "Reminder",
                Content = "Buy milk"
            };
            n.Pin();
            Console.WriteLine(n.Print());

            StickyNote sn = new StickyNote
            {
                Title = "Quick Note",
                Content = "Meeting at 5 PM",
                Color = "Yellow"
            };
            Console.WriteLine(sn.Print());
            sn.Recolor("Pink");
            Console.WriteLine(sn.Print());
        }
    }
}
