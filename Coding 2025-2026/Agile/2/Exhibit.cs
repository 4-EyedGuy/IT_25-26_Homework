public class Exhibit
{
    public int Id { get; set; }
    public string Title { get; set; }
    public string Author { get; set; }

    public Exhibit(int id, string title, string author)
    {
        Id = id;
        Title = title;
        Author = author;
    }

    public override string ToString()
    {
        return $"{Id}. {Title} (Автор: {Author})";
    }
}