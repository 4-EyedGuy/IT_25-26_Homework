public class Hall
{
    public string Name { get; set; }
    public double Size { get; set; }
    public IEnumerable<Exhibit> Exhibits => exhibits;

    public Hall(string name, double size)
    {
        Name = name;
        Size = size;
        exhibits = new List<Exhibit>();
    }

    public void AddExhibit(Exhibit exhibit)
    {
        exhibits.Add(exhibit);
    }

    public override string ToString()
    {
        string exhibitsInfo = exhibits.Count > 0
            ? string.Join(", ", exhibits)
            : "нет экспонатов";
        return $"Зал: {Name}, Площадь: {Size} квадратов, Экспонаты: {exhibitsInfo}";
    }

    private readonly List<Exhibit> exhibits;
}