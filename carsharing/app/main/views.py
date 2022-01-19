from flask import render_template,request
from flask import Blueprint
from app.models import Borrowed, Transaction, User,Car
from app.api.routes.cars import all_cars


main=Blueprint("main",__name__)

@main.route("/")
def index():
    data=all_cars(count=None,offset=None)
    return render_template("index.html", data=data)

@main.route("/allcars")
def cars():
    return render_template("cars/cars.html")


