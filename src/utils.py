import os
from pathlib import Path
from datetime import datetime;

DATA_DIR = Path(os.environ.get("DATA_DIR", Path(__file__).resolve().parent.parent / "data"))

def current_year(): 
    return datetime.now().year

def bibtex_proof(text: str): return text.replace('"', '{"}')

def create_references_bib_file(bibtex: str):
    """Creates data directory if it diesn't already exist and creates the bib file there"""
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    file_path = DATA_DIR / "references.bib"

    with open(file_path, "w") as file:
        file.write(bibtex)

    return str(file_path)
