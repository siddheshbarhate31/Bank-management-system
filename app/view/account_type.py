from app import db
from app.Schema.bank_account_schema import account_type_schema
from app.model.bank_account import AccountType
from flask import request
from flask_restful import Resource
from app.common.ResponseGenerator import ResponseGenerator
from app.common.Exception import IdNotFound
from flask_api import status
from app.common.logging import *


class AccountTypeDetails(Resource):

    def post(self):

        """Create account_type in the AccountType table"""
        try:
            account_data = request.get_json()
            result = account_type_schema.validate(account_data)
            if result:
                logger.exception(result)
                response = ResponseGenerator(data={}, message=result,
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            account = AccountType(account_type=account_data['account_type'])
            db.session.add(account)
            db.session.commit()
            output = account_type_schema.dump(account)
            logger.info("AccountType data successfully created")
            response = ResponseGenerator(data=output, message="AccountType data successfully created", success=True,
                                         status=status.HTTP_201_CREATED)
            return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message=error, success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()

    def get(self):

        """Provides the data of all the accountTypes"""
        try:
            all_account_types = AccountType.query.all()
            output = []
            for account in all_account_types:
                currentaccount = {}
                currentaccount['id'] = account.id
                currentaccount['account_type'] = account.account_type
                output.append(currentaccount)
            logger.info("All account_type data returned successfully")
            response = ResponseGenerator(data=output, message="All account_type data returned successfully",
                                         success=True, status=status.HTTP_200_OK)
            return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message=error, success=False,
                                         status=status.HTTP_404_NOT_FOUND)
            return response.error_response()


class AccountTypeData(Resource):

    """AccountTypeData for GET(single user), PUT(update user), DELETE(delete user)"""

    def get(self, id):

        """Gives the data of single account_type with selected account_type_id """
        try:
            account = AccountType.query.filter(AccountType.id == id).first()
            output = account_type_schema.dump(account)
            logger.info('AccountType data returned successfully')
            if account:
                response = ResponseGenerator(data=output, message="AccountType data returned successfully",
                                             success=True, status=status.HTTP_200_OK)
                return response.success_response()
            else:
                raise IdNotFound('id not found:{}'.format(id))
        except IdNotFound as error:
            logger.exception(error.message)
            response = ResponseGenerator(data={}, message=error.message, success=False,
                                         status=status.HTTP_404_NOT_FOUND)
            return response.error_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message=error, success=False,
                                         status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()

    def put(self, id):

        """Update the account type data """
        try:
            data = request.get_json()
            result = account_type_schema.validate(data, partial=True)
            if result:
                logger.exception(result)
                response = ResponseGenerator(data={}, message=result,
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            account = AccountType.query.filter(AccountType.id == id).first()
            if account:
                account.account_type = data.get('account_type', account.account_type)
                db.session.commit()
                output = account_type_schema.dump(account)
                logger.info("AccountType data updated successfully")
                response = ResponseGenerator(data=output, message="AccountType data updated successfully", success=True,
                                             status=status.HTTP_200_OK)
                return response.success_response()
            else:
                raise IdNotFound('id not found:{}'.format(id))
        except IdNotFound as error:
            logger.exception(error.message)
            response = ResponseGenerator(data={}, message=error.message, success=False,
                                         status=status.HTTP_404_NOT_FOUND)
            return response.error_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message=error,
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()
