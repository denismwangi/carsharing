from flask import render_template
from flask import Blueprint


main=Blueprint("main",__name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/allcars")
def cars():
    return render_template("cars/cars.html")


