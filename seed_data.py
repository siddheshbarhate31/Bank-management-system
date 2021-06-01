from app.model.bank_account import AccountType
from flask_script import Manager
from app import app
from app import db
manager = Manager(app)


@manager.command
def seed_gender_data():
    db.session.add(AccountType(account_type="Saving"))
    db.session.add(AccountType(account_type="Current"))
    db.session.commit()
