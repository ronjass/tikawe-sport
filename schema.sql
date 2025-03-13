CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE sports (
    id INTEGER PRIMARY KEY,
    sport TEXT,
    duration TEXT,
    distance TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users
);