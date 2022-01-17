from werkzeug.security import generate_password_hash,check_password_hash
from . import db,login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    phone=db.Column(db.String(20),unique=True)
    username = db.Column(db.String(128),unique=True,index=True)
    password_hash=db.Column(db.String(128))
    about=db.Column(db.String(200))
    joined_on=db.Column(db.DateTime(),default=datetime.utcnow)
    confirmed=db.Column(db.Boolean,default=False)
    photo=db.Column(db.String(64))
    rating=db.Column(db.Integer,default=1)
    role=db.Column(db.String(8),default="user")
    cars=db.relationship("Car",backref="owner",cascade="all,delete-orphan")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self,expiration=3600):
        s=Serializer(current_app.config["SECRET_KEY"],expiration)
        return s.dumps({'confirm':self.id}).decode("utf-8")

    def confirm_token(self,token):
        s=Serializer(current_app.config["SECRET_KEY"])
        try:
            data=s.loads(token.encode("utf-8"))
        except:
            return False
        if data.get("confirm")!=self.id:
            return False
        self.confirmed=True
        db.session.add(self)
        return True

    def __repr__(self):
        return f"User {self.username}"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Car(db.Model):
    __tablename__="cars"
    id = db.Column(db.Integer, primary_key=True)
    regno=db.Column(db.String(64),unique=True)
    brand=db.Column(db.String(64))
    added_on=db.Column(db.DateTime(),default=datetime.utcnow)
    charges=db.Column(db.Integer)
    mileage=db.Column(db.Integer)
    approved=db.Column(db.Boolean,default=False)
    location=db.Column(db.String(64))
    description=db.Column(db.Text())
    borrowed=db.Column(db.Boolean,default=False)
    rating=db.Column(db.Integer,default=1)
    ownerid=db.Column(db.Integer,db.ForeignKey("users.id"))
    photo=db.Column(db.String(64))
    images=db.relationship("Image",backref="pics",cascade="all,delete-orphan")

class Image(db.Model):
    __tablename__="images"
    id=db.Column(db.Integer,primary_key=True)
    carid=db.Column(db.Integer,db.ForeignKey("cars.id"))
    path=db.Column(db.String(64))
    
class Borrowed(db.Model):
    __tablename__="borrowed"
    id = db.Column(db.Integer, primary_key=True)
    userid=db.Column(db.Integer)
    carid=db.Column(db.Integer)
    borrowed_on=db.Column(db.DateTime(), default=datetime.utcnow)
    expected_on=db.Column(db.DateTime())
    duration=db.Column(db.Integer)
    borrowed_loc=db.Column(db.String(64))
    expected_loc=db.Column(db.String(64))

class Transaction(db.Model):
    __tablename__="transactions"
    id = db.Column(db.Integer, primary_key=True)
    borrowerid=db.Column(db.Integer)
    ownerid=db.Column(db.Integer)
    carid=db.Column(db.Integer)
    date=db.Column(db.DateTime(),default=datetime.utcnow)
    amount=db.Column(db.Integer)

