from flask import (
    redirect,
    render_template,
    request,
    flash,
    send_file
)
from config import app
from repositories.reference_repository import (
    add_reference,
    delete_reference,
    get_references,
    get_reference,
    update_reference,
    search_references
)
from entities.reference import (
    REF_TYPES,
    Reference,
    ReferenceValidationError
)
from repositories.bibtex_repository import generate_bibtex, create_references_bib_file
from utils import current_year

@app.route("/", methods=["GET"]) 
def render_home():
    search = request.args.get("search", "")[:255]
    references = search_references(search)

    return render_template("index.html", references=references, search=search)

@app.route("/new_reference")
def new_reference():
    return render_template("new_reference.html", current_year=current_year(), ref_types=REF_TYPES)

@app.route("/search", methods=["POST"])
def reference_search():
    search = request.form.get("search", "")[:255]
    
    references = search_references(search)
    render_template("index.html", references=references, search=search)

    return redirect("/")

@app.route("/add_reference", methods=["POST"])
def reference_addition():
    try:
        reference = Reference.from_form(request.form)
    except ReferenceValidationError as e:
        flash(e.args[0])
        return redirect("/new_reference")
    try:
        add_reference(reference)
    except ValueError as e:
        flash(e.args[0])
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

@app.route("/delete_reference", methods=["POST"])
def reference_deletion():
    bibtex_key = request.form["bibtex_key"]
    delete_reference(bibtex_key)
    flash(f"Reference '{bibtex_key}' was deleted.")
    return redirect("/")

@app.route("/reference/<ref_key>")
def reference_page(ref_key):
    ref = get_reference(ref_key)
    return render_template("reference.html", ref=ref)

@app.route("/edit_reference/<ref_key>")
def edit_reference(ref_key):
    ref= get_reference(ref_key)
    old_key=ref.key
    return render_template("edit_reference.html", ref_types=REF_TYPES, ref=ref, old_key=old_key)

@app.route("/update_reference", methods=["POST"])
def update_reference_route():
    old_key= request.form.get("old_key")
    try:
        reference = Reference.from_form(request.form)
    except ReferenceValidationError as e:
        flash(e.args[0])
        return redirect(f"/edit_reference/{old_key}")
    try:
        update_reference(reference, old_key)
    except ValueError as e:
        flash(e.args[0])
        print("Value")
        return redirect(f"/edit_reference/{old_key}")

    flash("Reference updated succesfully.")
    return redirect("/reference/" + reference.key)
