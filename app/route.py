from app import API
from app.view.user import UserProfile
from app.view.user import UserData
from app.view.usertype import UserTypeProfile, UserTypedata
from app.view.bank_account import BankAccountDetails


API.add_resource(UserProfile, '/user')
API.add_resource(UserData, '/user/<id>')
API.add_resource(UserTypeProfile, '/usertype')
API.add_resource(UserTypedata, '/usertype/<id>')
API.add_resource(BankAccountDetails, '/bank_account')








