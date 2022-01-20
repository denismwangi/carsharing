from app.models import Borrowed, Transaction, User,Car
from flask import Blueprint,render_template,redirect
from flask_login import current_user
from flask_restful import marshal
# from flask_socketio import send
# from app import socketio

from ..data import user_data,car_data,borrowed_data,income_data,spending_data
from ..utils.responses import response_with,auth_required
from ..utils import responses as resp

users=Blueprint("users",__name__)

@users.route("/")
@auth_required
def index():
    if current_user.role=="admin":
        data=marshal(User.query.all(),user_data)
        return response_with(resp.SUCCESS_200,value={"users":data})
    else:
        data=marshal(current_user,user_data)
        return response_with(resp.SUCCESS_200,value={"user":data})

@users.route("/<int:id>")
@auth_required
def user_info(id):
    user=User.query.filter_by(id=id).first()
    if not user:
        return response_with(resp.SERVER_ERROR_404,value={})
    user=marshal(user,user_data)
    #return response_with(resp.SUCCESS_200,value={"user":user})
    return render_template('cars/profile.html', data=user)



@users.route("/owned")
@auth_required
def owned():
    owned=[]
    for entry in Car.query.filter_by(ownerid=current_user.id).all():
        car=marshal(entry,car_data)
        car["images"]=[image.path for image in entry.images]
        owned.append(car)

    #return response_with(resp.SUCCESS_200,value={"owned_cars":owned})
    return render_template('cars/cars.html', data=owned)

@users.route("/borrowed")
@auth_required
def borrowed():
    borrowed=[marshal(entry,borrowed_data) for entry in
                 Borrowed.query.filter_by(userid=current_user.id)]
    #return response_with(resp.SUCCESS_200,value={"borrowed_cars":borrowed})

    return render_template('cars/borrowed.html', data=borrowed)

@users.route("/on_lend")
@auth_required
def on_lend():
    on_lend=[marshal(entry,borrowed_data) for entry in
                Borrowed.query.all() if entry.carid in [car.id for car in current_user.cars]]
    # return response_with(resp.SUCCESS_200,value={"onlend_cars":on_lend})
    return render_template('cars/onlend.html', data=on_lend)


@users.route("/transactions")
@auth_required
def user_transactions():
    transactions={}
    spending=[marshal(entry,spending_data) for entry in
                Transaction.query.filter_by(borrowerid=current_user.id)]
    income=[marshal(entry,income_data) for entry in
                Transaction.query.filter_by(ownerid=current_user.id)]
    transactions["spending"]=spending
    transactions["income"]=income
    transactions["total_spent"]=sum([entry["amount"] for entry in spending])
    transactions["total_income"]=sum([entry["amount"] for entry in income])
    return response_with(resp.SUCCESS_200,value={"transactions":transactions})


# @socketio.on("/message")
# def messages(payload):
#     send(payload,broadcast=True)

users.route("/notifications")
@auth_required
def notifications():
    pass