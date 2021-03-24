from app import db
from app.model.user import User

class bank_account(db.Model):
    account_number = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=True)
    deleted = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.Foreignkey('user_id'))
    account_type_id = db.Column(db.Integer, db.Foreignkey('account_type_id'))
    branch_id = db.Column(db.Integer, db.Foreignkey('branch_id'))
    account_transaction_detail = db.relationship('account_transaction_details', backref='account_number')

    def __init__(self, account_number, is_active, deleted, user_id, account_type_id, branch_id):
        self.account_number = account_number
        self.is_active = is_active
        self.deleted = deleted
        self.user_id = user_id
        self.account_type_id = account_type_id
        self.branch_id = branch_id
