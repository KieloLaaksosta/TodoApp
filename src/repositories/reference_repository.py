from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from config import db
from entities.reference import Reference

MAX_REF_KEY_LEN = 100
MAX_TEXT_LEN = 255
MIN_YEAR = 1
MAX_YEAR = 2100

def get_references():
    result = db.session.execute(text(
        "SELECT reference_type, bibtex_key, author, title, year, publisher FROM latex_references"
    ))
    references = result.fetchall()
    return [Reference(ref[0], ref[1], ref[2], ref[3], ref[4], ref[5]) for ref in references]

def none_if_empty(string: str) -> str:
    return string if string else None

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

    author = none_if_empty(author)

    if not bibtex_key or not title or not reference_type:
        return False

    if (
        len(bibtex_key) > MAX_REF_KEY_LEN
        or len(title) > MAX_TEXT_LEN
        or len(author) > MAX_TEXT_LEN
        or len(publisher) > MAX_TEXT_LEN
    ):
        return False

    try:
        year = int(year_str)
    except (TypeError, ValueError):
        return False

    if year > MAX_YEAR or year < MIN_YEAR:
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
