from app import db
from app.Schema.bank_account_schema import bank_account_schema
from app.model.bank_account import BankAccount
from flask import request
from flask_restful import Resource
from app.common.ResponseGenerator import ResponseGenerator
from flask_api import status
from app.common.logging import *


class BankAccountDetails(Resource):

    def post(self):

        """Create user in the User table"""

        account_data = request.get_json()
        result = bank_account_schema.validate(account_data)
        if result:
            logger.exception("Missing or sending incorrect data to create an activity")
            response = ResponseGenerator(data={}, message="Missing or sending incorrect data to create an activity",
                                         success=False, status=status.HTTP_404_NOT_FOUND)
            return response.error_response()
        account = BankAccount(account_number=account_data['account_number'],
                              is_active=account_data['is_active'],
                              deleted=False,
                              user_id=account_data['user_id'],
                              account_type_id=account_data['account_type_id'],
                              branch_id=account_data['branch_id'])
        db.session.add(account)
        db.session.commit()
        output = bank_account_schema.dump(account)
        logger.info("Account data successfully created")
        response = ResponseGenerator(data=output, message="Account data successfully created", success=True,
                                     status=status.HTTP_201_CREATED)
        return response.success_response()

    def get(self):

        """Provides the data of all the accounts"""

        all_accounts = BankAccount.query.all()
        output = []
        for account in all_accounts:
            currentaccount = {}
            currentaccount['account_number'] = account.account_number
            currentaccount['is_active'] = account.is_active
            currentaccount['deleted'] = account.deleted
            currentaccount['user_id'] = account.user_id
            currentaccount['account_type_id'] = account.account_type_id
            currentaccount['branch_id'] = account.branch_id
            output.append(currentaccount)
        logger.info("All account data returned successfully")
        response = ResponseGenerator(data=output, message="All account data returned successfully",
                                     success=True, status=status.HTTP_200_OK)
        return response.success_response()


