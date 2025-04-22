CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE sports (
    id INTEGER PRIMARY KEY,
    sport TEXT,
    duration INTEGER,
    distance INTEGER,
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
