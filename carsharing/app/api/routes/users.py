
from flask import jsonify,g
from app.models import Borrowed, Image, Transaction, User,Car

from flask import Blueprint,render_template,redirect
from flask_login import current_user
from flask_restful import marshal
from app import db
# from flask_socketio import send
# from app import socketio
from app.api.routes.cars import all_cars,car__single
from ..data import user_data,car_data,borrowed_data,income_data,spending_data
from ..utils.responses import response_with,auth_required
from ..utils import responses as resp

users=Blueprint("users",__name__)

@users.route("/admin")
@auth_required
def admin():
    if current_user.role=="admin":
        data=marshal(User.query.all(),user_data)
        return render_template("accounts/admindash.html",data=data)
    else:
        data=marshal(current_user,user_data)
        # return response_with(resp.SUCCESS_200,value={"user":data})
        return render_template("accounts/dashboard.html",data=data)


#########################admin
@users.route("/admin/all_users")
@auth_required
def all_users():
    if current_user.role!="admin":
        return response_with(resp.UNAUTHORIZED_403)
    else:
        data=marshal(User.query.all(),user_data)
        # return response_with(resp.SUCCESS_200,value={"users":data})
        return render_template("accounts/users.html",data=data)
@users.route("/admin/allcars")
def cars():
    data=all_cars(count=None,offset=None)
    return render_template("cars/adcars.html", data=data)

@users.route("/admin/pending_registrations")
def pending_registrations():
    if current_user.role!="admin":
        return response_with(resp.UNAUTHORIZED_403)
    data=marshal(User.query.filter_by(confirmed=False).all(),user_data)
    # return response_with(resp.SUCCESS_200,value={"registrations":data})
    return render_template("accounts/pending_users.html",data=data)    

@users.route("/confirm_registration/<int:id>")
def confirm_registration(id):
    if current_user.role!="admin":
        return response_with(resp.UNAUTHORIZED_403)
    else:
        user=User.query.filter_by(id=id).first()
        user.confirmed=True
        db.session.commit()
        # return response_with(resp.SUCCESS_200)
        return redirect('/api/users/admin/pending_registrations')

@users.route("/admin/pending_approvals")
def pending_approvals():
    if current_user.role!="admin":
        return response_with(resp.UNAUTHORIZED_403)
    else:
        data=marshal(Car.query.filter_by(approved=False).all(),car_data)
        # return response_with(resp.SUCCESS_200,value={"pending_approvals":data})
        return render_template("cars/pending_approval.html",data=data) 


@users.route("/approve_car/<int:id>")
def approve_car(id):
    if current_user.role!="admin":
        return response_with(resp.UNAUTHORIZED_403)
    else:
        car=Car.query.filter_by(id=id).first()
        car.approved=True
        db.session.commit()
        # return response_with(resp.SUCCESS_200)
        return redirect('/api/users/admin/pending_approvals')

@users.route("/delete_car/<int:id>")
def delete_car(id):
    if current_user.role!="admin":
        return response_with(resp.UNAUTHORIZED_403)
    else:
        Image.query.filter_by(carid=id).delete()
        Car.query.filter_by(id=id).delete()
        db.session.commit()
        # return response_with(resp.SUCCESS_200)
        return redirect('/api/users/admin/allcars')

@users.route("/delete_user/<int:id>")
def delete_user(id):
    if current_user.role!="admin":
        return response_with(resp.UNAUTHORIZED_403)
    else:
        for car in User.query.filter_by(id=id).first().cars:
            Image.query.filter_by(carid=car.id).delete()
            Car.query.filter_by(id=car.id).delete()
        User.query.filter_by(id=id).delete()
        db.session.commit()
        # return response_with(resp.SUCCESS_200)
        return redirect('/api/users/admin/all_users')

################################################


@users.route("/profile")
@auth_required
def profile():
    data=marshal(current_user,user_data)
    return render_template('cars/profile.html', data=data)


@users.route("/profile")
@auth_required
def profile():
    data=marshal(current_user,user_data)
    return render_template('cars/profile.html', data=data)



@users.route("/<int:id>")
@auth_required
def user_info(id):
    user=User.query.filter_by(id=id).first()
    if not user:
        return response_with(resp.SERVER_ERROR_404,value={})
    user=marshal(user,user_data)
    #return response_with(resp.SUCCESS_200,value={"user":user})
   



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

def total_owned():
    owned=[]
    for entry in Car.query.filter_by(ownerid=current_user.id).all():
        car=marshal(entry,car_data)
        car["images"]=[image.path for image in entry.images]
        owned.append(car)
    return len(owned)

@users.route("/borrowed")
@auth_required
def borrowed():
    borrowed=[marshal(entry,borrowed_data) for entry in
                 Borrowed.query.filter_by(userid=current_user.id) if entry.status!="pending_return"]
    for entry in borrowed:
        entry["brand"]=Car.query.filter_by(id=entry["carid"]).first().brand
        entry["regno"]=Car.query.filter_by(id=entry["carid"]).first().regno
    # return response_with(resp.SUCCESS_200,value={"borrowed_cars":borrowed})
    return render_template('cars/borrowed.html', data=borrowed)

def total_borrowed():
    borrowed=[marshal(entry,borrowed_data) for entry in
                 Borrowed.query.filter_by(userid=current_user.id)]
    return len(borrowed)


@users.route("/on_lend")
@auth_required
def on_lend():
    on_lend=[marshal(entry,borrowed_data) for entry in
                Borrowed.query.all() if entry.carid in [car.id for car in current_user.cars]]
    for entry in on_lend:
        entry["brand"]=Car.query.filter_by(id=entry["carid"]).first().brand
        entry["regno"]=Car.query.filter_by(id=entry["carid"]).first().regno
    # return response_with(resp.SUCCESS_200,value={"onlend_cars":on_lend})
    return render_template('cars/onlend.html', data=on_lend)

def total_onlend():
    on_lend=[marshal(entry,borrowed_data) for entry in
                Borrowed.query.all() if entry.carid in [car.id for car in current_user.cars]]
    return len(on_lend)
    


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
    # return response_with(resp.SUCCESS_200,value={"transactions":transactions})
    return transactions



# @socketio.on("/message")
# def messages(payload):
#     send(payload,broadcast=True)

users.route("/notifications")
@auth_required
def notifications():
    pass


@users.route("/transactions/spending", methods=['GET', 'POST'])
@auth_required
def user_spending():
    spending=[marshal(entry,spending_data) for entry in
                Transaction.query.filter_by(borrowerid=current_user.id,status="confirmed")]
    return response_with(resp.SUCCESS_200,value={"transactions_spending":spending})

@users.route("/transactions/income", methods=['GET', 'POST'])
@auth_required
def user_income():
    income=[marshal(entry,income_data) for entry in
                Transaction.query.filter_by(ownerid=current_user.id,status="confirmed")]
    return response_with(resp.SUCCESS_200,value={"transactions_income":income})