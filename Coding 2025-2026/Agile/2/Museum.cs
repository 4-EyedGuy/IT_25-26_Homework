public class Museum
{
    public string Name { get; set; }
    public double Area { get; set; }
    public IEnumerable<Exhibit> Exhibits => exhibits;

    public Museum(string name, double area) 
    {
        Name = name;
        Area = area;
        exhibits = new List<Exhibit>();
    }

    public void AddExhibit(Exhibit exhibit)
    {
        exhibits.Add(exhibit);
    }

    public override string ToString()
    {
        string exhibitsInfo = exhibits.Count > 0
            ? string.Join("\n", exhibits)
            : "всё украли(";
        return $"Музей: {Name}, Площадь: {Area} квадратов\nКоллекция экспозиций:\n{exhibitsInfo}";
    }

    private readonly List<Exhibit> exhibits;
}