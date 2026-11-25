from sqlalchemy.exc import IntegrityError

from sqlalchemy import text
from config import db
from entities.reference import Reference

SELECT = """
    SELECT reference_type, bibtex_key, author, title, year, publisher
    FROM latex_references
"""

def _row_to_reference(row) -> Reference:
    return Reference(
        row["reference_type"],
        row["bibtex_key"],
        row["author"],
        row["title"],
        row["year"],
        row["publisher"],
    )

def get_references():
    result = db.session.execute(text(SELECT)).mappings().all()
    return [_row_to_reference(row) for row in result]

def add_reference(reference: Reference):
    sql = text("""
        INSERT INTO latex_references (bibtex_key, reference_type, title, author, year, publisher)
        VALUES (:bibtex_key, :reference_type, :title, :author, :year, :publisher)
    """)
    try:
        db.session.execute(
            sql,
            {
                "bibtex_key": reference.key,
                "reference_type": reference.type,
                "title": reference.title,
                "author": reference.author,
                "year": reference.year,
                "publisher": reference.publisher,
            },
        )
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Reference with Bibtex key {reference.key} already exists.") from e

def delete_reference(bibtex_key: str):
    sql = text("DELETE FROM latex_references WHERE bibtex_key = :bibtex_key")
    db.session.execute(sql, {"bibtex_key": bibtex_key})
    db.session.commit()

def search_references(search : str):
    sql = text(f"""
        {SELECT}
        WHERE reference_type LIKE :search
        OR bibtex_key LIKE :search
        OR author LIKE :search
        OR title LIKE :search
        OR publisher LIKE :search
        OR CAST(year AS TEXT) LIKE :search
    """)

    formated_search = search.strip().replace(" ", "%")
    formated_search = f"%{formated_search}%"

    result = db.session.execute(sql, {"search": formated_search}).mappings().all()

    return [_row_to_reference(row) for row in result]

def get_reference(ref_key: str):
    sql = text(f"{SELECT} WHERE bibtex_key = :ref_key")
    row = db.session.execute(sql, {"ref_key": ref_key}).mappings().fetchone()
    if row is None:
        return None
    return _row_to_reference(row)

def update_reference(reference: Reference, old_key):
    sql = text("""
        UPDATE latex_references
        SET bibtex_key = :bibtex_key,
            reference_type = :reference_type,
            title = :title,
            author = :author,
            year = :year,
            publisher = :publisher
        WHERE bibtex_key = :old_key
    """)
    try:
        db.session.execute(
            sql,
            {
                "bibtex_key": reference.key,
                "reference_type": reference.type,
                "title": reference.title,
                "author": reference.author,
                "year": reference.year,
                "publisher": reference.publisher,
                "old_key": old_key,
            },
        )
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Reference with Bibtex key {reference.key} already exists.") from e
