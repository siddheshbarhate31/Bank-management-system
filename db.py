from app.model.bank_account import AccountType
from flask_script import Manager
from app import app
from app import manager
from app import db
from seed_data import seed_gender_data


@manager.command
def seed():
    seed_gender_data()
    print("Seed Data Loaded.")


if __name__ == '__main__':
    manager.run()
