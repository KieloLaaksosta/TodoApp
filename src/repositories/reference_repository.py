from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from config import db
from entities.reference import Reference
from utils import current_year

MAX_REF_KEY_LEN = 100
MAX_TEXT_LEN = 255
MIN_YEAR = 1

REF_TYPES = ["book"]

def get_references():
    result = db.session.execute(text(
        "SELECT reference_type, bibtex_key, author, title, year, publisher FROM latex_references"
    ))
    references = result.fetchall()
    return [Reference(ref[0], ref[1], ref[2], ref[3], ref[4], ref[5]) for ref in references]

def add_reference(
    bibtex_key : str,
    reference_type : str,
    title : str,
    author : str,
    year_str : str,
    publisher : str
) -> None:
    bibtex_key = bibtex_key.strip()
    reference_type = reference_type.strip()
    title = title.strip()
    author = author.strip()

    if not bibtex_key or not title or not reference_type or not author:
        return False

    if (
        len(bibtex_key) > MAX_REF_KEY_LEN
        or len(title) > MAX_TEXT_LEN
        or (author is not None and len(author)) > MAX_TEXT_LEN
        or len(publisher) > MAX_TEXT_LEN
    ):
        return False

    try:
        year = int(year_str)
    except (TypeError, ValueError):
        return False

    if year > current_year() or year < MIN_YEAR:
        return False

    sql=text("""
            INSERT INTO latex_references (bibtex_key,reference_type,title,author,year,publisher)
            VALUES (:bibtex_key,:reference_type, :title, :author, :year, :publisher)
            """)
    try:
        db.session.execute(sql, {
            "bibtex_key": bibtex_key,
            "reference_type": reference_type,
            "title": title,
            "author": author,
            "year": year,
            "publisher": publisher
        })
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False

def delete_reference(bibtex_key : str):
    sql = text(
    """DELETE FROM latex_references WHERE bibtex_key = :bibtex_key""")
    db.session.execute(sql, {"bibtex_key": bibtex_key})
    db.session.commit()
