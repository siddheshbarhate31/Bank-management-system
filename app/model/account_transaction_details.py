from app import db


class AccountTransactionDetails(db.Model):

    """Create table AccountTransactionDetails in the database"""

    __tablename__ = 'AccountTransactionDetails'
    id = db.Column(db.Integer, primary_key=True)
    transaction_amount = db.Column(db.Integer)
    transaction_date = db.Column(db.DateTime, server_default=db.func.now())
    bank_account_id = db.Column(db.Integer, db.ForeignKey('BankAccount.id'))
    transaction_type_id = db.Column(db.Integer, db.ForeignKey('TransactionType.id'))
    fund_id = db.Column(db.Integer, db.ForeignKey('FundTransfer.id'))
    transaction_status = db.Column(db.String(120), nullable=False)

    def __init__(self, transaction_amount, bank_account_id, transaction_type_id, fund_id, transaction_status):
        self.transaction_amount = transaction_amount
        self.bank_account_id = bank_account_id
        self.transaction_type_id = transaction_type_id
        self.fund_id = fund_id
        self.transaction_status = transaction_status


class TransactionType(db.Model):

    """Create table TransactionType in the database"""

    __tablename__ = 'TransactionType'
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(120), nullable=False)
    account_transaction_detail = db.relationship('AccountTransactionDetails', backref='TransactionType')

    def __init__(self, transaction_type):
        self.transaction_type = transaction_type


class FundTransfer(db.Model):

    """Create table FundTransfer in the database"""

    __tablename__ = 'FundTransfer'
    id = db.Column(db.Integer, primary_key=True)
    from_account = db.Column(db.String(10), nullable=False)
    to_account = db.Column(db.String(10))
    account_transaction_detail = db.relationship('AccountTransactionDetails', backref='FundTransfer')

    def __init__(self, from_account, to_account):
        self.from_account = from_account
        self.to_account = to_account

