from app import db


class User(db.Model):

    """ Create table User in the database """

    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=False)
    last_name = db.Column(db.String(120), unique=False)
    address = db.Column(db.String(120), unique=False)
    mobile_number = db.Column(db.String(10), unique=True)
    email_id = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=True)
    is_deleted = db.Column(db.Integer)
    user_type_id = db.Column(db.Integer, db.ForeignKey('UserType.id'))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    bank_account = db.relationship('BankAccount', backref='User', lazy=True)

    def __init__(self, first_name, last_name, address, mobile_number, email_id, password, is_deleted, user_type_id):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.mobile_number = mobile_number
        self.email_id = email_id
        self.password = password
        self.is_deleted = is_deleted
        self.user_type_id = user_type_id


class UserType(db.Model):

    """Create table UserType in the database"""

    __tablename__ = 'UserType'
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(120), nullable=False)
    user = db.relationship('User', backref='UserType')

    def __init__(self, user_type):
        self.user_type = user_type

