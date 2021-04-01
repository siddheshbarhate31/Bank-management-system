from app import API
from app.view.user import UserProfile
from app.view.user import UserData
from app.view.usertype import UserTypeProfile, UserTypedata
from app.view.bank_account import BankAccountDetails, BankAccountData
from app.view.account_type import AccountTypeDetails, AccountTypeData
from app.view.branch_details import BranchData , BranchInfo


API.add_resource(UserProfile, '/user')
API.add_resource(UserData, '/user/<id>')
API.add_resource(UserTypeProfile, '/usertype')
API.add_resource(UserTypedata, '/usertype/<id>')
API.add_resource(BankAccountDetails, '/bank_account')
API.add_resource(BankAccountData, '/bank_account/<id>')
API.add_resource(AccountTypeData, '/account_type/<id>')
API.add_resource(AccountTypeDetails, '/account_type')
API.add_resource(BranchData, '/branch_details')
API.add_resource(BranchInfo, '/branch_details/<id>')







