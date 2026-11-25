from utils import DATA_DIR

def bibtex_proof(text: str):
    return text.replace('"', '{"}')

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

def create_references_bib_file(bibtex: str):
    """Creates data directory if it doesn't already exist and creates the bib file there"""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    file_path = DATA_DIR / "references.bib"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(bibtex)

    return str(file_path)
