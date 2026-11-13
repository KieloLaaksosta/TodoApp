CREATE TABLE latex_references (
  bibtex_key TEXT PRIMARY KEY,
  reference_type TEXT NOT NULL,
  title TEXT NOT NULL,
  author TEXT,
  year INTEGER,
  publisher TEXT
)
