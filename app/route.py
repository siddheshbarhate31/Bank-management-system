from app import API
from app.view.user import UserProfile
from app.view.user import UserData
from app.view.usertype import UserTypeProfile, UserTypedata
from app.view.bank_account import BankAccountDetails, BankAccountData
from app.view.account_type import AccountTypeDetails, AccountTypeData
from app.view.branch_details import BranchData, BranchInfo
from app.view.account_transaction_details import AccountTransactionInfo, AccountTransactionData
from app.view.transaction_type import TransactionTypeDetails, TransactionTypeData
from app.view.fund_transfer import FundTransferInfo, FundTransferData
from app.view.mini_statement import MiniStatement
from app.view.login_logout import Login
from app.view.login_logout import Logout

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
API.add_resource(TransactionTypeDetails, '/transaction_type')
API.add_resource(TransactionTypeData, '/transaction_type/<id>')
API.add_resource(AccountTransactionInfo, '/account_transaction_details')
API.add_resource(AccountTransactionData, '/account_transaction_details/<id>')
API.add_resource(FundTransferInfo, '/fund_transfer')
API.add_resource(FundTransferData, '/fund_transfer/<id>')
API.add_resource(MiniStatement, '/mini_statement/<id>')
API.add_resource(Login, '/login')
API.add_resource(Logout, '/logout')





