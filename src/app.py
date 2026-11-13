from flask import redirect, render_template, request, jsonify
from config import app, test_env
from datetime import datetime
from repositories.reference_repository import add_reference, get_references
from db_helper import reset_db

@app.route("/")
def render_home():
    references = get_references()
    return render_template("index.html", references=references)

@app.route("/new_reference")
def new_reference():
    current_year = datetime.now().year
    return render_template("new_reference.html", current_year=current_year)

@app.route("/add_reference", methods=["POST"])
def reference_addition():
    reference_type=request.form["reference_type"]
    bibtex_key=request.form["bibtex_key"]
    title=request.form["title"]
    author=request.form["author"]
    year=request.form["year"]
    publisher=request.form["publisher"]

    add_reference(bibtex_key, reference_type, title, author, year, publisher)
    return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({

            'message': "database reset"

        })
