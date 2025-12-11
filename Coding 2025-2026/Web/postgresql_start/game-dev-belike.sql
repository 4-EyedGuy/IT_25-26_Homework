CREATE TABLE developer (
    id         SERIAL PRIMARY KEY,
    name       TEXT      NOT NULL UNIQUE,
    country    TEXT
);

CREATE TABLE game (
    id                  SERIAL PRIMARY KEY,
    title               TEXT    NOT NULL,
    release_year        INT     NOT NULL,
    primary_developer_id INT     NOT NULL,

    CONSTRAINT fk_primary_developer
        FOREIGN KEY (primary_developer_id)
        REFERENCES developer (id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_release_year
        CHECK (release_year >= 1970 AND release_year <= EXTRACT(YEAR FROM CURRENT_DATE))
);

CREATE TABLE game_info (
    game_id         INT  PRIMARY KEY,
    engine          TEXT,
    age_rating      TEXT,
    playtime_hours  INT,

    CONSTRAINT fk_game_info
        FOREIGN KEY (game_id)
        REFERENCES game (id)
        ON DELETE CASCADE,

    CONSTRAINT chk_age_rating
        CHECK (age_rating IN ('E', 'T', 'M', 'AO')),

    CONSTRAINT chk_playtime_positive
        CHECK (playtime_hours > 0)
);

CREATE TABLE game_credit (
    game_id      INT  NOT NULL,
    developer_id INT  NOT NULL,
    role         TEXT NOT NULL,

    PRIMARY KEY (game_id, developer_id, role),

    CONSTRAINT fk_game_credit_game
        FOREIGN KEY (game_id)
        REFERENCES game (id)
        ON DELETE CASCADE,

    CONSTRAINT fk_game_credit_developer
        FOREIGN KEY (developer_id)
        REFERENCES developer (id)
        ON DELETE RESTRICT
);




-- INSERT INTO developer (name, country) VALUES ('Valve', 'USA');
-- INSERT INTO developer (name, country) VALUES ('CD Projekt Red', 'Poland');
-- INSERT INTO developer (name) VALUES ('FromSoftware');

-- INSERT INTO game (title, release_year, primary_developer_id)
-- VALUES ('Portal 2', 2011, 1);

-- INSERT INTO game_info (game_id, engine, age_rating, playtime_hours)
-- VALUES (1, 'Source', 'E', 8);

-- INSERT INTO game_credit (game_id, developer_id, role)
-- VALUES (1, 2, 'co-dev'), (1, 3, 'audio');

-- DELETE FROM game WHERE id = 1;

-- DELETE FROM developer WHERE id = 1;