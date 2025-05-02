DROP TABLE IF EXISTS books;

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reader_name TEXT NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL
);

INSERT INTO books (reader_name, title, author) VALUES ('Dani','Spinning Silver', 'Naomi Novik');
INSERT INTO books (reader_name, title, author) VALUES ('Yonah','Hippos Go Berserk', 'Sandra Boynton');
