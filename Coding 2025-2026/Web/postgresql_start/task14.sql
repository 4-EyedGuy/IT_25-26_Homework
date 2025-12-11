CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    content TEXT NOT NULL,
    published_at TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO articles (title, author, content)
SELECT
    'Title ' || i,
    'Author ' || (1 + (random() * 100)::int),
    md5(random()::text) || ' ' || md5(random()::text) || ' lorem ipsum'
FROM generate_series(1, 1000000) s(i);

SELECT * FROM articles
WHERE author = 'Author 42';

CREATE INDEX idx_articles_author ON articles(author);

SELECT * FROM articles
WHERE author = 'Author 42';

SELECT * FROM articles
WHERE content ILIKE '%lorem%';

CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_articles_content_trgm
    ON articles USING gin (content gin_trgm_ops);

SELECT * FROM articles
WHERE content ILIKE '%lorem%';
