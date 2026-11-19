from datetime import datetime; 

def current_year(): return datetime.now().year

def bibtex_proof(text: str): return text.replace('"', '{"}')

def create_references_bib_file(bibtex: str):
    with open("files/references.bib", "w") as file:
        file.write(bibtex)
    return "../files/references.bib"
