using System;

namespace Documents
{
    class Report : Document
    {
        private string author;

        public string Author
        {
            get => author;
            set
            {
                if (string.IsNullOrWhiteSpace(value))
                    throw new ArgumentException("Author не может быть пустым");
                author = value;
            }
        }

        public string Header()
        {
            return $"Report by {Author}";
        }

        public override string Print()
        {
            return Header() + "\n" + base.Print();
        }
    }
}
