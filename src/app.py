from flask import redirect, render_template, request
from config import app
from repositories.reference_repository import add_reference, get_references

@app.route("/")
def render_home():
    references = get_references()
    return render_template("index.html", references=references)

@app.route("/new_reference")
def new_reference():
    return render_template("new_reference.html")

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
