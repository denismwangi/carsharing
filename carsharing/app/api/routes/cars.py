from datetime import datetime
from flask import request,render_template,redirect
import timedelta
from app.models import Borrowed, Transaction, User,Car
from app import db,user_sids
from flask_login import current_user
from ..utils.responses import auth_required, response_with
from ..data import user_data,car_data,borrowed_data
from ..utils import responses as resp
from flask import Blueprint
from flask_restful import marshal
from flask import jsonify
from ..data import car_data,user_data
# from flask_socketio import emit

cars=Blueprint("cars",__name__)

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


@cars.route("/<int:id>/borrowed")
def borrowed_info(id):
    car=Borrowed.query.filter_by(carid=id).first()
    if not car:
        return response_with(resp.SERVER_ERROR_404,value={})
    return response_with(resp.SUCCESS_200,value={"borrowed_car":marshal(car,borrowed_data)})

@cars.route("/<int:id>/borrow",methods=["POST"])
@auth_required
def borrow(id):
    req={"carid":id,
        "from":request.args.get("from"),
        "until":request.args.get("until"),
        "duration":request.args.get("duration"),
        "pick_up":request.args("pick_up"),
        "drop_off":request.args("drop_off")}
    car=Car.query.filter_by(id=id).first()
    if not car:
        return response_with(resp.SERVER_ERROR_404,value={})
    owner=user_sids.get(car.ownerid)
    if not owner:
        return response_with({"error":"owner is not available,try again later"})
    # emit("request_car",req,room=owner)


@cars.route("/<int:id>/grant",methods=["POST"])
@auth_required
def grant_car():
    car=Car.query.filter_by(id=id).first()
    if not car:
        return response_with(resp.SERVER_ERROR_404)
    if car.ownerid!=current_user.id:
        return response_with(resp.UNAUTHORIZED_403)

    borrowed=Borrowed(borrowed_on=request.args.get("from"),
            expected_on=request.args.get("until"),
            duration=request.args.get("duration"),
            borrowed_loc=request.args("borrowed_loc"),
            expected_loc=request.args("expected_loc"))
    db.session.add(borrowed)
    db.session.commit()


@cars.route("/<int:id>/return")
@auth_required
def return_car(id):
    car=Car.query.filter_by(id=id).first()
    if not car:
        return response_with(resp.SERVER_ERROR_404)
    if car.ownerid!=current_user.id:
        return response_with(resp.UNAUTHORIZED_403)
    borrow=Borrowed.query.filter_by(carid=id).first()
    duration=timedelta.Timedelta(datetime.utcnow()-borrow.borrowed_on).total.hours
    transaction=Transaction(
        borrowerid=borrow.userid,
        ownerid=car.ownerid,
        carid=id,
        amount=duration*car.charges
    )
    db.session.add(transaction)
    db.session.commit()
    Borrowed.query.filter_by(carid=id).delete()
    return response_with(resp.SUCCESS_200)


