CREATE TABLE latex_references (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ref_type TEXT NOT NULL,
  title TEXT NOT NULL,
  author TEXT,
  year INTEGER
)
