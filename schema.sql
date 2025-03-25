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
    send_at TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
)

CREATE TABLE sport_classes (
    id INTEGER PRIMARY KEY,
    sport_id INTEGER REFERENCES sports,
    title TEXT,
    value TEXT
);