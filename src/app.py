from flask import redirect, render_template, request, flash, session, send_file
from config import app
from repositories.reference_repository import add_reference, get_references, generate_bibtex, REF_TYPES
from utils import current_year, create_references_bib_file

@app.route("/")
def render_home():
    references = get_references()
    return render_template("index.html", references=references)

@app.route("/new_reference")
def new_reference():
    return render_template("new_reference.html", current_year=current_year(), ref_types=REF_TYPES)

@app.route("/add_reference", methods=["POST"])
def reference_addition():
    reference_type=request.form.get("reference_type")
    bibtex_key=request.form.get("bibtex_key")
    title=request.form.get("title")
    author=request.form.get("author")
    year=request.form.get("year")
    publisher=request.form.get("publisher")

    error_msg = add_reference(bibtex_key, reference_type, title, author, year, publisher)
    if error_msg:
        flash(error_msg)
        return redirect("/new_reference")
    
    flash("Reference added succesfully.")
    return redirect("/")

@app.route("/bibtex")
def render_bibtex():
    references = get_references()
    bibtex = generate_bibtex(references)
    return render_template("bibtex.html", bibtex=bibtex)

@app.route("/bibtex/download")
def download_bibtex():
    references = get_references()
    bibtex = generate_bibtex(references)
    path = create_references_bib_file(bibtex)
    return send_file(path, as_attachment=True)