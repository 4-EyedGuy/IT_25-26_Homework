CREATE SCHEMA music_store;

CREATE TABLE music_store.albums (
    album_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    release_year INT,
    price NUMERIC(10,2)
);

CREATE TABLE music_store.artists (
    artist_id SERIAL PRIMARY KEY,
    stage_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) DEFAULT 'Unknown',
    album_title VARCHAR(100),
    UNIQUE (album_title)
);