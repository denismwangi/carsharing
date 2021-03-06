from datetime import datetime
<<<<<<< HEAD
from flask import request,render_template,redirect,session,url_for,current_app
=======
from flask import request,render_template,redirect,session
from flask_restful import fields
>>>>>>> 08556cf25dfdacbc4efb4757f872316c2038d4d6
import timedelta
from flask_restful import fields
from app.models import Borrowed, Transaction, User,Car,Image
from app import db,user_sids
from flask_login import current_user
from ..utils.responses import auth_required, response_with
from ..data import user_data,car_data,borrowed_data
from ..utils import responses as resp
from flask import Blueprint,url_for
from flask_restful import marshal
from ..data import car_data,user_data
from secrets import token_urlsafe
import os
# from flask_socketio import emit

cars=Blueprint("cars",__name__)

def all_cars(count=None,offset=None):
    if not count or not offset:
        count=50
        offset=0
    else:
        count,offset=int(count),int(offset)
        if offset>Car.query.count() or count>Car.query.count():
            count=1
            offset=0
        if offset<0 or count<0:
            count=0
            offset=0

    data=[]
    cars=Car.query.order_by(Car.id).slice(offset,count)
    for entry in  cars:
        car=marshal(entry,car_data)
        car["images"]=[image.path for image in entry.images]
        data.append(car)
    # return response_with(resp.SUCCESS_200,value={"cars":data})
    return data


@cars.route("/",methods=["GET"])
def index():
    count=request.args.get("count")
    offset=request.args.get("offset")
    if not count or not offset:
        count=50
        offset=0
    else:
        count,offset=int(count),int(offset)
        if offset>Car.query.count() or count>Car.query.count():
            count=1
            offset=0
        if offset<0 or count<0:
            count=0
            offset=0

    data=[]
    cars=Car.query.order_by(Car.id).slice(offset,count)
    for entry in  cars:
        car=marshal(entry,car_data)
        car["images"]=[image.path for image in entry.images]
        data.append(car)
    # return response_with(resp.SUCCESS_200,value={"cars":data})
    return render_template('cars/allcars.html', data=cars)


@cars.route("/<int:id>",methods=["GET"])
def car(id):
    car=Car.query.filter_by(id=id).first()
    if not car:
        return response_with(resp.SERVER_ERROR_404,value={})
    response=marshal(car,car_data)
    response["images"]=[image.path for image in car.images]
   
    return response_with(resp.SUCCESS_200,value={"car":response})

<<<<<<< HEAD
@cars.route("/car-single/<int:id>",methods=["GET"])
=======
<<<<<<< HEAD
@cars.route("/<int:id>",methods=["GET"])
>>>>>>> 08556cf25dfdacbc4efb4757f872316c2038d4d6
def car__single(id):
    car=Car.query.filter_by(id=id).first()
    if not car:
        return response_with(resp.SERVER_ERROR_404,value={})
    response=marshal(car,car_data)
    response["images"]=[image.path for image in car.images]
    return response
    # return response_with(resp.SUCCESS_200,value={"car":response})


=======
>>>>>>> 209a401759f5937a8c2499c9c28161e07ed2048c
@cars.route("/<int:id>/owner")
def owner(id):
    car=Car.query.filter_by(id=id).first()
    if not car:
        return response_with(resp.SERVER_ERROR_404,value={})
    owner=User.query.filter_by(id=car.ownerid).first()
    response=marshal(owner,user_data)
    return response_with(resp.SUCCESS_200,value={"car_owner":response})


@cars.route("/<int:id>/available")
def available(id):
    car=Car.query.filter_by(id=id).first()
    if not car:
        return response_with(resp.SERVER_ERROR_404,value={})
    if Borrowed.query.filter_by(carid=car.id).count():
        return response_with(resp.SUCCESS_200,value={"status":{"available":False}})
    else:
        return response_with(resp.SUCCESS_200,value={"status":{"available":True}})


#data about a borrowed car
@cars.route("/<int:id>/borrowed")
def borrowed_info(id):
    car=Borrowed.query.filter_by(carid=id).first()
    if not car:
        return response_with(resp.SERVER_ERROR_404,value={})
    return response_with(resp.SUCCESS_200,value={"borrowed_car":marshal(car,borrowed_data)})


<<<<<<< HEAD

@cars.route("/add_images/<int:id>",methods=["POST","GET"])
@auth_required
def add_images(id):
    if request.method=="POST":
        file=request.files["photo"]
        photo=f"{token_urlsafe(16)}.{file.filename.split('.')[-1]}"
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],photo))
        if not Car.query.filter_by(id=id).first():
            return response_with(resp.SERVER_ERROR_404)
        image=Image(
                carid=id,
                path="uploads/"+photo)
        db.session.add(image)
        db.session.commit()
        return redirect('/api/users/owned')
    return render_template("cars/add_images.html",id=id)


=======
>>>>>>> 08556cf25dfdacbc4efb4757f872316c2038d4d6
@cars.route("/<int:id>/bid")
@auth_required
def update(id):
    data=Car.query.filter_by(id=id).first()
    if not data:
        return redirect(url_for('index'))
    else:
        session['update'] = id
        return render_template('cars/borrow.html', data = data)


@cars.route("/<int:id>/borrow",methods=["POST"])
@auth_required
def borrow(id):
    carid=id
<<<<<<< HEAD
    from_date=request.form["from"]
    until_date=request.form["until"]
    duration=request.form["duration"]
    pick_up=request.form["pick_up"]
    drop_off=request.form["drop_off"]

    if Borrowed.query.filter_by(carid=id).first():
        return  {"error":"car is not available for borrowing"}

    borrowed=Borrowed(
        userid=current_user.id,
        carid=carid,
        borrowed_on=from_date,
        expected_on=until_date,
        duration=duration,
        borrowed_loc=pick_up,
        expected_loc=drop_off
    )
    db.session.add(borrowed)
    db.session.commit()
    return redirect('/api/users/borrowed')
=======
    from_date=request.args.get("from")
    until_date=request.args.get("until")
    duration=request.args.get("duration")
    pick_up=request.args.get("pick_up")
    drop_off=request.args.get("drop_off")

    if Borrowed.query.filter_by(carid=id).first():
        return  {"error":"car is not available for borrowing"}

    borrowed=Borrowed(
        userid=current_user.id,
        carid=carid,
        borrowed_on=from_date,
        expected_on=until_date,
        duration=duration,
        borrowed_loc=pick_up,
        expected_loc=drop_off
    )
    db.session.add(borrowed)
    db.session.commit()
    return response_with(resp.SUCCESS_200)

@cars.route("/pending_grants",methods=["GET"])
@auth_required
def pending_grants():
    data=[]
    borrowed=Borrowed.query.filter_by(userid=current_user.id,status="pending")
    for borrow in borrowed:
        if Car.query.filter_by(carid=borrow.carid,ownerid=current_user.id):
            entry=marshal(borrow,borrowed_data)
            data.append(entry)
    return response_with(resp.SUCCESS_200,value={"pending_grants":data})


@cars.route("/<int:id>/grant",methods=["GRANT"])
@auth_required
def grant_car(id):
    borrow=Borrowed.query.filter_by(carid=id).first()
    borrow.status="confirmed"
    db.session.commit()
    return "success",200

>>>>>>> 08556cf25dfdacbc4efb4757f872316c2038d4d6

<<<<<<< HEAD

<<<<<<< HEAD
@cars.route("/pending_grants",methods=["GET"])
@auth_required
def pending_grants():
    data=[]
    borrowed=Borrowed.query.filter_by(status="pending")
    for borrow in borrowed:
        if Car.query.filter_by(id=borrow.carid,ownerid=current_user.id):
            entry=marshal(borrow,borrowed_data)
            data.append(entry)
    # return response_with(resp.SUCCESS_200,value={"pending_grants":data})

    return render_template('cars/borrow_requests.html', data=data)



@cars.route("/<int:id>/grant",methods=["GET"])
@auth_required
def grant_car(id):
=======
@cars.route("/<int:bid>/return")
=======
@cars.route("/<int:id>/return",methods=["GET"])
>>>>>>> 209a401759f5937a8c2499c9c28161e07ed2048c
@auth_required
def return_car(id):
    transaction=Transaction(
        borrowerid=current_user.id,
        ownerid=Car.query.filter_by(id=id).first().ownerid,
        carid=id
    )
    db.session.add(transaction)
    db.session.commit()
    return response_with(resp.SUCCESS_200)

@cars.route("/pending_returns",methods=["GET"])
@auth_required
def pending_returns():
    data=[]
    trans_dat={
        "id":fields.Integer,
        "borrowerid":fields.Integer,
        "carid":fields.Integer,
        "status":fields.String,
        "date":fields.DateTime
    }
    transactions=Transaction(ownerid=current_user.id,status="pending")
    for trans in transactions:
        data.append(marshal(trans,trans_dat))
    return response_with(resp.SUCCESS_200,value={"pending_returns":data})


@cars.route("/<int:id>/confirm_return")
@auth_required
def confirm_return(id):
    transaction=Transaction.query.filter_by(carid=id).first()
    borrow=Borrowed.query.filter_by(carid=id).first()
    duration=timedelta.Timedelta(datetime.utcnow()-borrow.borrowed_on).total.hours
    amount=Car.query.filter_by(carid=id).first().charges*duration

    transaction.status="confirmed"
    transaction.amount= amount

<<<<<<< HEAD
@cars.route("/<int:id>/accept")
@auth_required
def accept_car(id):
    car=Car.query.filter_by(id=id).first()
    if not car:
        return response_with(resp.SERVER_ERROR_404)
    if car.ownerid!=current_user.id:
        return response_with(resp.UNAUTHORIZED_403)
>>>>>>> 08556cf25dfdacbc4efb4757f872316c2038d4d6
    borrow=Borrowed.query.filter_by(carid=id).first()
    borrow.status="confirmed"
    db.session.commit()
    # return "success",200
    return redirect('/api/cars/pending_grants')

@cars.route("/<int:id>/return",methods=["GET"])
@auth_required
def return_car(id):
    transaction=Transaction(
        borrowerid=current_user.id,
        ownerid=Car.query.filter_by(id=id).first().ownerid,
        carid=id
    )
    Borrowed.query.filter_by(carid=id).first().status="pending_return"
    db.session.add(transaction)
    db.session.commit()
    # return response_with(resp.SUCCESS_200)
    return redirect('/api/users/borrowed')

@cars.route("/delete_car/<int:id>")
def delete_car(id):
    Image.query.filter_by(carid=id).delete()
    Car.query.filter_by(id=id).delete()
    db.session.commit()
    # return response_with(resp.SUCCESS_200)
    return redirect('/api/users/owned')

@cars.route("/pending_returns",methods=["GET"])
@auth_required
def pending_returns():
    data=[]
    trans_dat={
        "id":fields.Integer,
        "borrowerid":fields.Integer,
        "carid":fields.Integer,
        "status":fields.String,
        "date":fields.DateTime
    }
    b=[marshal(entry,borrowed_data) for entry in
                Borrowed.query.filter_by(status="pending_return") if entry.carid in [car.id for car in current_user.cars]]
    for trans in b:
        data.append(marshal(trans,trans_dat))
    for entry in data:
        entry["brand"]=Car.query.filter_by(id=entry["carid"]).first().brand
        entry["regno"]=Car.query.filter_by(id=entry["carid"]).first().regno
        # entry["borrower_name"]=User.query.filter_by(id=entry["borrowerid"]).first().username
    # return response_with(resp.SUCCESS_200,value={"pending_returns":data})
    return render_template('cars/returned_cars.html', data=data)

@cars.route("/<int:id>/confirm_return")
@auth_required
def confirm_return(id):
    transaction=Transaction.query.filter_by(carid=id).first()
    borrow=Borrowed.query.filter_by(carid=id).first()
    if not borrow:
        return response_with(resp.SERVER_ERROR_404)
    duration=timedelta.Timedelta(datetime.utcnow()-borrow.borrowed_on).total.hours
    amount=Car.query.filter_by(id=id).first().charges*duration

    transaction.status="confirmed"
    transaction.amount= amount

    db.session.add(transaction)
    Borrowed.query.filter_by(carid=id).delete()
    db.session.commit()

    # return render_template('cars/borrowed.html')
    # return response_with(resp.SUCCESS_200)
    return redirect('/api/cars/pending_returns')

=======
    db.session.add(transaction)
    db.session.commit()

<<<<<<< HEAD
# @cars.route("/<int:id>/accept")
# @auth_required
# def accept_car(id):
#     car=Car.query.filter_by(id=id).first()
#     if not car:
#         return response_with(resp.SERVER_ERROR_404)
#     if car.ownerid!=current_user.id:
#         return response_with(resp.UNAUTHORIZED_403)
#     borrow=Borrowed.query.filter_by(carid=id).first()
#     duration=timedelta.Timedelta(datetime.utcnow()-borrow.borrowed_on).total.hours
#     transaction=Transaction(
#         borrowerid=borrow.userid,
#         ownerid=car.ownerid,
#         carid=id,
#         amount=duration*car.charges
#     )
#     db.session.add(transaction)
#     db.session.commit()
#     Borrowed.query.filter_by(carid=id).delete()
#     return render_template('cars/borrowed.html')
=======
    Borrowed.query.filter_by(carid=id).delete()
    # return render_template('cars/borrowed.html')
    return response_with(resp.SUCCESS_200)
>>>>>>> 209a401759f5937a8c2499c9c28161e07ed2048c
>>>>>>> 08556cf25dfdacbc4efb4757f872316c2038d4d6
