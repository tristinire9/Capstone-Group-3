import sqlite3

conn = sqlite3.connect("instance/flaskr.sqlite")

cur = conn.cursor()

cur.execute("""CREATE TABLE relationships (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  componentID INTEGER NOT NULL,
  recipeID INTEGER NOT NULL,

  FOREIGN KEY(componentID) REFERENCES components(id),
  FOREIGN KEY(recipeID) REFERENCES recipes(id)
);""")

