from app import db
from datetime import datetime
from app.model.bank_account import bank_account

class account_transaction_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_amount = db.Column(db.Integer)
    transaction_date = db.Column(db.Date)
    account_number = db.Column(db.Integer, db.Foreignkey('account_number'))
    transaction_type_id = db.Column(db.Integer, db.Foreignkey('transaction_type_id'))
    fund_id = db.Column(db.Integer, db.Foreignkey('fund_id'))

    def __init__(self, transaction_amount, transaction_date, account_number, transaction_type_id, fund_id):
        self.transaction_amount = transaction_amount
        self.transaction_date = datetime.strptime(transaction_date, '%m/%d/%Y').date()
        self.account_number = account_number
        self.transaction_type_id = transaction_type_id
        self.fund_id = fund_id
