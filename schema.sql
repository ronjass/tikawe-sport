CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    image BLOB
);

CREATE TABLE sports (
    id INTEGER PRIMARY KEY,
    sport TEXT,
    duration INTEGER,
    distance REAL,
    description TEXT,
    sent_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    user_id INTEGER REFERENCES users
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE sport_classes (
    id INTEGER PRIMARY KEY,
    sport_id INTEGER REFERENCES sports,
    title TEXT,
    value TEXT
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    sport_id INTEGER REFERENCES sports,
    user_id INTEGER REFERENCES users,
    comment TEXT,
    sent_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE likes (
    id INTEGER PRIMARY KEY,
    sport_id INTEGER REFERENCES sports,
    user_id INTEGER REFERENCES users
);

CREATE INDEX idx_sports_user ON sports(user_id);
CREATE INDEX idx_sport_comments ON comments (sport_id);
CREATE INDEX idx_comments_user ON comments (user_id);
CREATE INDEX idx_sport_likes ON likes (sport_id);
CREATE INDEX idx_likes_user on likes (user_id, sport_id);
CREATE INDEX idx_sport_classes_sport ON sport_classes (sport_id);