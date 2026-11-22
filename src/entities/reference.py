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

    def __str__(self):
        return f"{self.key}: {self.title} by {self.author}"

def generate_bibtex(references: list):
    bibtex = ""
    for ref in references:
        bibtex += f"@{ref.type}"
        bibtex += "{"
        bibtex += f"{ref.key},\n"
        bibtex += f"""    author = "{bibtex_proof(ref.author)}",\n"""
        bibtex += f"""    title = "{bibtex_proof(ref.title)}",\n"""
        bibtex += f"""    year = "{ref.year}",\n"""
        bibtex += f"""    publisher = "{bibtex_proof(ref.publisher)}"\n"""
        bibtex += "}\n"
        bibtex += "\n"
    return bibtex
