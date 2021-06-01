from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_migrate import Migrate
from app.model import *
from flask_script import Manager
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(environ.get('DATABASE_USERNAME'),
                                                                             environ.get('DATABASE_PASSWORD'),
                                                                             environ.get('DATABASE_HOST'),
                                                                             environ.get('DATABASE'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "SiddeshSecretBankManagementSystemProject1234"
ACCESS_EXPIRES = timedelta(minutes=30)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
app.config['PROPAGATE_EXCEPTIONS'] = True
manager = Manager(app)


jwt = JWTManager(app)
db = SQLAlchemy(app)
API = Api(app)
ma = Marshmallow(app)
migrate = Migrate(app, db, compare_type=True)
