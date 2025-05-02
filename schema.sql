DROP TABLE IF EXISTS books;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL
);

INSERT INTO users (name, email) VALUES ('Spinning Silver', 'Naomi Novik');
INSERT INTO users (name, email) VALUES ('Hippos Go Berserk', 'Sandra Boynton');
