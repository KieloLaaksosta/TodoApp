from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from config import db
from entities.reference import Reference
from utils import bibtex_proof

def get_references():
    result = db.session.execute(text(
        "SELECT reference_type, bibtex_key, author, title, year, publisher FROM latex_references"
    ))
    references = result.fetchall()
    return [Reference(ref[0], ref[1], ref[2], ref[3], ref[4], ref[5]) for ref in references]

def add_reference(reference : Reference):
    sql=text("""
            INSERT INTO latex_references (bibtex_key,reference_type,title,author,year,publisher)
            VALUES (:bibtex_key,:reference_type, :title, :author, :year, :publisher)
            """)
    try:
        db.session.execute(sql, {
            "bibtex_key": reference.key,
            "reference_type": reference.type,
            "title": reference.title,
            "author": reference.author,
            "year": reference.year,
            "publisher": reference.publisher
        })
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Reference with Bibtex key {reference.key} already exists.") from e

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

def delete_reference(bibtex_key : str):
    sql = text(
    """DELETE FROM latex_references WHERE bibtex_key = :bibtex_key""")
    db.session.execute(sql, {"bibtex_key": bibtex_key})
    db.session.commit()

def get_reference(ref_key: str):
    sql = text("""SELECT reference_type, bibtex_key, author, title, year, publisher
               FROM latex_references WHERE bibtex_key = :ref_key""")
    result = db.session.execute(sql, {"ref_key": ref_key})
    if not result:
        return None
    ref = result.fetchall()[0]
    print(ref)
    return Reference(ref[0], ref[1], ref[2], ref[3], ref[4], ref[5])

def update_reference(reference: Reference, ref_id):
    sql=text("""UPDATE latex_references SET bibtex_key=?, reference_type=?,
                title=?, author=?, year=?, publisher=?
                WHERE id=?
            """)
    try:
        db.session.execute(sql, {
            "bibtex_key": reference.key,
            "reference_type": reference.type,
            "title": reference.title,
            "author": reference.author,
            "year": reference.year,
            "publisher": reference.publisher
            "id": ref_id
        })
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Reference with Bibtex key {reference.key} already exists.") from e

