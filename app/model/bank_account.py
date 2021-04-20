from app import db


class BankAccount(db.Model):

    """Create table BankAccount in the database"""

    __tablename__ = 'BankAccount'
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(10), unique=True)
    is_active = db.Column(db.Boolean)
    deleted = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    account_type_id = db.Column(db.Integer, db.ForeignKey('AccountType.id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('BranchDetails.id'))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    balance = db.Column(db.Integer)
    account_transaction_detail = db.relationship('AccountTransactionDetails', backref='BankAccount')

    def __init__(self, account_number, is_active, deleted, balance, user_id, account_type_id, branch_id):
        self.account_number = account_number
        self.is_active = is_active
        self.deleted = deleted
        self.balance = balance
        self.user_id = user_id
        self.account_type_id = account_type_id
        self.branch_id = branch_id


class AccountType(db.Model):

    """Create table AccountType in the database"""

    __tablename__ = 'AccountType'
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(120), nullable=False)
    bank_account = db.relationship('BankAccount', backref='AccountType')

    def __init__(self, account_type):
        self.account_type = account_type


class BranchDetails(db.Model):

    """Create table BranchDetails in the database"""

    __tablename__ = 'BranchDetails'
    id = db.Column(db.Integer, primary_key=True)
    branch_address = db.Column(db.String(200), nullable=False)
    bank_account = db.relationship('BankAccount', backref='BranchDetails')

    def __init__(self, branch_address):
        self.branch_address = branch_address
