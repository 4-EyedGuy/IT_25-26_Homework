namespace Documents
{
    class Note : Document
    {
        public bool Pinned { get; private set; }

        public void Pin()
        {
            Pinned = true;
        }
    }
}