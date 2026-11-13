from sqlalchemy import text
from config import db

from entities.reference import Reference

def get_references():
    #TODO (meil ei oo viel kunnon schemaa nii pitää tarkistaa myöhemmin miten ne taulut menee)
    result = db.session.execute(text(
        "SELECT type, key, author, title, year, publisher FROM latex_references"
    ))
    references = result.fetchall()
    return [Reference(ref[0], ref[1], ref[2], ref[3], ref[4], ref[5]) for ref in references]
