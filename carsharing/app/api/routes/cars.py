from datetime import datetime
from flask import request,render_template,redirect,session
from flask_restful import fields
import timedelta
from app.models import Borrowed, Transaction, User,Car
from app import db,user_sids
from flask_login import current_user
from ..utils.responses import auth_required, response_with
from ..data import user_data,car_data,borrowed_data
from ..utils import responses as resp
from flask import Blueprint,url_for
from flask_restful import marshal
from ..data import car_data,user_data
# from flask_socketio import emit

cars=Blueprint("cars",__name__)

def all_cars(count=None,offset=None):
    if not count or not offset:
        count=5
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
        count=5
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


@cars.route("/<int:id>/return",methods=["GET"])
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
def return_car(id):
    transaction=Transaction.query.filter_by(carid=id).first()
    borrow=Borrowed.query.filter_by(carid=id).first()
    duration=timedelta.Timedelta(datetime.utcnow()-borrow.borrowed_on).total.hours
    amount=Car.query.filter_by(carid=id).first().charges*duration

    transaction.status="confirmed"
    transaction.amount= amount

    db.session.add(transaction)
    db.session.commit()

    Borrowed.query.filter_by(carid=id).delete()
    # return render_template('cars/borrowed.html')
    return response_with(resp.SUCCESS_200)
