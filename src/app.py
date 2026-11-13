from flask import Flask, redirect, render_template, request
from repositories.reference_repository import add_reference, get_references

app = Flask(__name__)

@app.route("/")
def render_home():
    return render_template("index.html")

@app.route("/add_reference", methods=["POST"])
def reference_addition():
    reference_type=request.form["reference_type"]
    title=request.form["title"]
    author=request.form["author"]
    year=request.form["year"]
    publisher=request.form["publisher"]

    add_reference(reference_type,title,author,year,publisher)
    return redirect("/new_reference")

