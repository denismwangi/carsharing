import os
from secrets import token_urlsafe
from flask import render_template,redirect,current_app,request,url_for,flash
from flask_login import login_required,login_user,logout_user
from flask import Blueprint,request
from  app.models import User
from  app.utils import send_email
from  app import db,user_sids

accounts=Blueprint("accounts",__name__)

@accounts.route("/dashboard")
@login_required
def dashboard():
    return render_template("accounts/dashboard.html")

@accounts.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        user=User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            login_user(user,remember=True)
            # user_sids[user.id]=request.sid
            return redirect(url_for("accounts.dashboard"))
    flash("Invalid username or password")
    return render_template("accounts/login.html")

@accounts.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are now logged out.")
    return redirect(url_for("main.index"))

@accounts.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password1"]
        email=request.form["email"]
        phone=request.form["phone"]
        about=request.form["about"]
        file=request.files["photo"]
        photo=f"{token_urlsafe(16)}.{file.filename.split('.')[-1]}"
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],photo))
        user=User( username=username,
                    password=password,
                    email=email,
                    phone=phone,
                    about=about,
                    photo="/static/uploads/"+photo)
        db.session.add(user)
        db.session.commit()
        token=user.generate_confirmation_token()
        send_email(user.email,"Confirm Your Registration","auth/email/confirm",user=user,token=token)
        flash('A confirmation link has been sent to you by email.')
        return redirect(url_for('accounts.login'))
    return render_template("accounts/register.html")

@accounts.route("/allcars")
def cars():
    return render_template("cars/cars.html")


@accounts.route('/add-car', methods=['GET', 'POST'])
def addCar():
    if request.method=="POST":
        regno=request.form["regno"]
        brand=request.form["brand"]
        charges=request.form["charges"]
        mileage=request.form["mileage"]
        location=request.form["location"]
        description=request.form["description"]
        file=request.files["photo"]

        photo=f"{token_urlsafe(16)}.{file.filename.split('.')[-1]}"
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],photo))
        car=Car(regno=regno,
                brand=brand,
                charges=charges,
                mileage=mileage,
                location=location,
                description=description,
                photo="/static/uploads/"+photo)
        db.session.add(car)
        db.session.commit()
        return  'Success',200
    return render_template("accounts/addcar.html")

