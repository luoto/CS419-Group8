/*
 * This script creates a test database (psql) with some sample data
 */

DROP DATABASE IF EXISTS curses;
CREATE DATABASE curses;

\c curses

CREATE TABLE movies (
  id SERIAL PRIMARY KEY,
  title VARCHAR(25) NOT NULL,
  genre VARCHAR(25)
);

INSERT INTO movies (title, genre) VALUES
('Deadpool', 'Action'),
('Fantastic Four', 'Science Fiction'),
('Dragon Ball Z', 'Fantasy'),
('Intersteller', 'Science Fiction'),
('Boyhood', 'Drama'),
('Gone Girl', 'Thriller'),
('Guardians of the Galaxy', 'Science Fiction');
