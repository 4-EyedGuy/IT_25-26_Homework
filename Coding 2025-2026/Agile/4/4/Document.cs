using System;

namespace Documents
{
    class Document
    {
        private string title;
        private string content;
        public string Title
        {
            get => title;
            set
            {
                if (string.IsNullOrWhiteSpace(value))
                    throw new ArgumentException("Title не может быть пустым");
                title = value;
            }
        }

        public string Content
        {
            get => content;
            set => content = value ?? "";
        }

        public int WordCount()
        {
            if (string.IsNullOrWhiteSpace(Content)) return 0;
            return Content.Split(new[] { ' ', '\t', '\n' }, StringSplitOptions.RemoveEmptyEntries).Length;
        }

        public string Preview(int chars)
        {
            if (Content.Length <= chars) return Content;
            return Content.Substring(0, chars);
        }

        public virtual string Print()
        {
            return Title + "\n" + Content;
        }
    }
}
