/*
 * This script creates a test database (psql) with some sample data
 */

DROP DATABASE IF EXISTS curses;
CREATE DATABASE curses;

\c curses

CREATE TABLE movies (
  id SERIAL PRIMARY KEY,
  title VARCHAR(25) NOT NULL,
  genre VARCHAR(25),
  studio_id INT references studios(id)
);

CREATE TABLE studios (
  id SERIAL PRIMARY KEY,
  name VARCHAR(25) NOT NULL
);

INSERT INTO studios (name) VALUES
('Comcast'),
('Marvel'),
('Sony');

INSERT INTO movies (title, genre, studio_id) VALUES
('Deadpool', 'Action', 1),
('Fantastic Four', 'Science Fiction', 1),
('Dragon Ball Z', 'Fantasy', 2),
('Intersteller', 'Science Fiction', 3),
('Boyhood', 'Drama', 3),
('Gone Girl', 'Thriller', 2),
('Guardians of the Galaxy', 'Science Fiction', 1);
