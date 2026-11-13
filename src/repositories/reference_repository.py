from sqlalchemy import text
from config import db
from entities.reference import Reference

MAX_REF_KEY_LEN = 100
MAX_TEXT_LEN = 255

def get_references():
    result = db.session.execute(text(
        "SELECT reference_type, bibtex_key, author, title, year, publisher FROM latex_references"
    ))
    references = result.fetchall()
    return [Reference(ref[0], ref[1], ref[2], ref[3], ref[4], ref[5]) for ref in references]

def add_reference(bibtex_key, reference_type, title, author, year, publisher):
    
    if (
        len(bibtex_key) > MAX_REF_KEY_LEN
        or len(title) > MAX_TEXT_LEN
        or len(author) > MAX_TEXT_LEN
        or len(publisher) > MAX_TEXT_LEN
    ):
        return False
    
    sql=text("""
            INSERT INTO latex_references (bibtex_key,reference_type,title,author,year,publisher)
            VALUES (:bibtex_key,:reference_type, :title, :author, :year, :publisher)
            """)
    db.session.execute(sql,  {
                            "bibtex_key":bibtex_key,
                            "reference_type":reference_type, 
                            "title":title,
                            "author":author, 
                            "year":year, 
                            "publisher":publisher})
    db.session.commit()
    return True
