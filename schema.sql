DROP TABLE IF EXISTS components;

CREATE TABLE components (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  name TEXT NOT NULL,
  version_num TEXT NOT NULL,
  date TEXT NOT NULL,
  url TEXT NOT NULL,
);

CREATE TABLE recipes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  name TEXT NOT NULL,
  version_num TEXT NOT NULL,
  status TEXT NOT NULL
);


CREATE TABLE relationships (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  componentID INTEGER NOT NULL,
  recipeID INTEGER NOT NULL,

  FOREIGN KEY(componentID) REFERENCES components(id),
  FOREIGN KEY(recipeID) REFERENCES recipes(id)
);

ALTER TABLE relationships ADD COLUMN destination_path text;
