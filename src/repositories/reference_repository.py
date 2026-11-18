from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from config import db
from entities.reference import Reference
from utils import current_year
import re

MAX_REF_KEY_LEN = 100
MAX_TEXT_LEN = 255
MIN_YEAR = 1

REF_TYPES = ["book"]
KEY_ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ12346789.:_-"

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
) -> str:
    if None in [bibtex_key, reference_type, title, author, year_str , publisher]:
        return "Missing fields."    
    
    bibtex_key = bibtex_key.strip()
    reference_type = reference_type.strip()
    title = title.strip()
    author = author.strip()
    publisher = publisher.strip()

    if not bibtex_key:
        return "Missing bibtex key."
    if  not title:
        return "Missing title."
    if not reference_type:
        return "Missing reference type key."
    if not author:
        return "Missing author."
    if not publisher:
        return "Missing publisher."
    
    if reference_type not in REF_TYPES:
        return f"Invalid reference type: {reference_type}. Allowed types: {REF_TYPES}"

    if (len(bibtex_key) > MAX_REF_KEY_LEN):
        return f"Bibtex key too long. Maximum: {MAX_REF_KEY_LEN} characters"
    if len(title) > MAX_TEXT_LEN:
        return f"Title too long. Maximum: {MAX_TEXT_LEN} characters"
    if len(author) > MAX_TEXT_LEN:
        return f"Author name too long. Maximum: {MAX_TEXT_LEN} characters"
    if len(publisher) > MAX_TEXT_LEN:
        return f"Publisher name too long. Maximum: {MAX_TEXT_LEN} characters"

    try:
        year = int(year_str)
    except (TypeError, ValueError):
        return f"Invalid year. Must be an integer."

    max_year = current_year()
    if year > max_year or year < MIN_YEAR:
        return f"The year must be at most {max_year} and at least {MIN_YEAR}."

    if not all(c in KEY_ALLOWED_CHARS for c in bibtex_key):
        return "Invalid key. Only numbers, English letters and following specail charachters: _ . : and - are allowed."

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
        return None
    except IntegrityError:
        db.session.rollback()
        return f"Refernce with Bibtex key {bibtex_key} already exists."
