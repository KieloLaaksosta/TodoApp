CREATE TABLE latex_references (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  bibtex_key TEXT UNIQUE NOT NULL,
  reference_type TEXT NOT NULL,
  title TEXT NOT NULL,
  author TEXT,
  year INTEGER,
  publisher TEXT
)
