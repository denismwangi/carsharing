import  os

basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY=os.environ.get("SECRET_KEY","my secret key")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT",587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    UPLOAD_FOLDER= os.path.join(basedir, 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    @staticmethod
    def init_app(app):
        pass

class  DevelopmentConfig(Config):
    DEBUG=True
    username="root"
    password=""
    server="localhost"
    dbname="csp_database"
    SQLALCHEMY_DATABASE_URI=f"mysql+mysqlconnector://{username}:{password}@{server}/{dbname}"

class  ProductionConfig(Config):
    username=""
    password=""
    server=""
    dbname=""
    SQLALCHEMY_DATABASE_URI=f"mysql+mysqlconnector://{username}:{password}@{server}/{dbname}"
  
config={
    "development":DevelopmentConfig,
    "production":ProductionConfig,
    "default":DevelopmentConfig
}
