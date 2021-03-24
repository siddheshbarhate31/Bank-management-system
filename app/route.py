from app import API
from app.view.user import UserProfile
from app.view.user import UserData
from app.view.usertype import UserTypeProfile, UserTypedata


API.add_resource(UserProfile, '/user')
API.add_resource(UserData, '/user/<id>')
API.add_resource(UserTypeProfile, '/usertype')
API.add_resource(UserTypedata, '/usertype/<id>')








