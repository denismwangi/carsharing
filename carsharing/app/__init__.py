from flask import Flask
# from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
# import socketio
from config import config
from flask_login import LoginManager
# from flask_socketio import SocketIO,send,emit

login_manager = LoginManager()
login_manager.login_view = "accounts.login"

user_sids={}
# socketio=None
# mail=Mail()
db=SQLAlchemy()

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # global socketio
    # socketio=SocketIO(app,cors_allowed_origins="*")
    # @socketio.on("send_message")
    # def sendMessage(msg):
    #     recipient=msg["userid"]
    #     emit("message",msg["message"],room=recipient)

    #Add the routes over here
    from .main.views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .accounts.views import accounts as accounts_blueprint
    app.register_blueprint(accounts_blueprint, url_prefix='/accounts')

    from .api.routes.cars import cars as car_routes
    app.register_blueprint(car_routes,url_prefix="/api/cars")

    from .api.routes.users import users as user_routes
    app.register_blueprint(user_routes,url_prefix="/api/users")
 
    return app