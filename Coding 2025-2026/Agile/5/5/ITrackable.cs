public interface ITrackable
{
    string TrackingId { get; set; }
    void AddCheckpoint(string note);
}
