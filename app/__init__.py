from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Siddesh@123@localhost/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
API = Api(app)
ma = Marshmallow(app)




