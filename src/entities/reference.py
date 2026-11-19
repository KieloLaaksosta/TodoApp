from dataclasses import dataclass
from utils import bibtex_proof

@dataclass
class Reference:
    type: str
    key: str
    author: str
    title: str
    year: int
    publisher: str

    def __init__(self, type, key, author, title, year, publisher):
        self.type = type
        self.key = key
        self.author = bibtex_proof(author)
        self.title = bibtex_proof(title)
        self.year = year
        self.publisher = bibtex_proof(publisher)


    def __str__(self):
        return f"{self.key}: {self.title} by {self.author}"
