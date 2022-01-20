from flask import render_template,request
from flask import Blueprint
from app.models import Borrowed, Transaction, User,Car
from app.api.routes.cars import all_cars,car__single
from flask_restful import marshal

main=Blueprint("main",__name__)

@main.route("/")
def index():
    data=all_cars(count=None,offset=None)
    return render_template("index.html", data=data)

@main.route("/allcars")
def cars():
    data=all_cars(count=None,offset=None)
    return render_template("cars.html", data=data)
   



@main.route("/view-car/<int:id>",methods=["GET"])
def cars_single(id):
    data = car__single(id)
    return render_template("car.html", data=data)

    
