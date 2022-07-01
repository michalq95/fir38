from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_restx import Api


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()
login = LoginManager(app)
api_bp = Blueprint("apis", __name__, url_prefix="/apis/")
api= Api(api_bp)
app.register_blueprint(api_bp)




from app import  models,routes, apis