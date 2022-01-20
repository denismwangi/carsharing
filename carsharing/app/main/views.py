import os
from secrets import token_urlsafe
from flask import render_template,request,Blueprint,current_app,redirect,url_for
from flask_login import login_required
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

@main.route("/addcar",methods=["GET","POST"])
@login_required
def add_car():
    if request.method=="POST":
        regno=request.form["regno"]
        brand=request.form["brand"]
        charges=request.form["charges"]
        mileage=request.form["mileage"]
        location=request.form["location"]
        description=request.form["description"]
        transmission=request.form["transmission"]
        seats=request.form["seats"]
        luggage=request.form["luggage"]
        fuel=request.form["fuel"]
        engine=request.form["engine"]
        
        file=request.files["photo"]
        photo=f"{token_urlsafe(16)}.{file.filename.split('.')[-1]}"
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],photo))

        car=Car(regno=regno,
            brand=brand,
            charges=charges,
            mileage=mileage,
            location=location,
            description=description,
            photo="/static/uploads"+photo,
            transmission=transmission,
            seats=seats,
            luggage=luggage,
            fuel=fuel,
            engine=engine,
        )
        return redirect(url_for("accounts.dashboard"))
    return render_template("cars/addcar.html")


    
