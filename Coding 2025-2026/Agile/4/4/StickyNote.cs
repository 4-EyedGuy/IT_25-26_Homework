using System;

namespace Documents
{
    class StickyNote : Note
    {
        private string color;

        public string Color
        {
            get => color;
            set
            {
                if (string.IsNullOrWhiteSpace(value))
                    throw new ArgumentException("Color не может быть пустым");
                color = value;
            }
        }

        public void Recolor(string c)
        {
            Color = c;
        }

        public override string Print()
        {
            return $"[{Color}] " + base.Print();
        }
    }
}
