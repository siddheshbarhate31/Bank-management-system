from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Siddesh@123@localhost/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "SiddeshSecretBankManagementSystemProject1234"
ACCESS_EXPIRES = timedelta(minutes=30)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

jwt = JWTManager(app)
db = SQLAlchemy(app)
API = Api(app)
ma = Marshmallow(app)
