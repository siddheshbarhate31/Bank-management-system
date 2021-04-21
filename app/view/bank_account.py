from app import db
from app.Schema.bank_account_schema import bank_account_schema, generate_random_number
from app.model.bank_account import BankAccount
from flask import request
from flask_restful import Resource
from app.common.ResponseGenerator import ResponseGenerator
from app.common.Exception import IdNotFound
from flask_api import status
from app.common.logging import *


class BankAccountDetails(Resource):

    def post(self):

        """Create bank account in the BankAccount table"""
        try:
            account_data = request.get_json()
            result = bank_account_schema.validate(account_data)
            if result:
                logger.exception(result)
                response = ResponseGenerator(data={}, message=result, success=False,
                                             status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            branch_id = account_data['branch_id']
            random_number = generate_random_number(7)
            account_number = str(branch_id).zfill(3) + str(random_number)
            logger.debug(account_number)
            account = BankAccount(account_number=account_number,
                                  is_active=1,
                                  deleted=0,
                                  balance=account_data['balance'],
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
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message=error, success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()


    def get(self):

        """Provides the data of all the bank accounts"""

        try:
            all_accounts = BankAccount.query.filter(BankAccount.deleted == 0)
            output = []
            for account in all_accounts:
                currentaccount = {}
                currentaccount['id'] = account.id
                currentaccount['account_number'] = account.account_number
                currentaccount['is_active'] = account.is_active
                currentaccount['balance'] = account.balance
                currentaccount['user_id'] = account.user_id
                currentaccount['account_type_id'] = account.account_type_id
                currentaccount['branch_id'] = account.branch_id
                currentaccount['created_on'] = account.created_on
                output.append(currentaccount)
            logger.info("All account data returned successfully")
            response = ResponseGenerator(data=output, message="All account data returned successfully",
                                         success=True, status=status.HTTP_200_OK)
            return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message=error, success=False,
                                         status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()


class BankAccountData(Resource):

    """BankAccountData for GET(bank account), PUT(update account), DELETE(delete bank account)"""

    def get(self, id):

        """Gives the data of bank account of selected bank account id """
        try:
            account = BankAccount.query.filter(BankAccount.id == id, BankAccount.deleted == 0).first()
            output = bank_account_schema.dump(account)
            if account:
                logger.info('bank account data returned successfully')
                response = ResponseGenerator(data=output, message="bank account data returned successfully",
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

        """Update the bank account data """
        try:
            data = request.get_json()
            result = bank_account_schema.validate(data)
            if result:
                logger.exception(result)
                response = ResponseGenerator(data={}, message=result,
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            account = BankAccount.query.filter(BankAccount.id == id, BankAccount.is_active == True,
                                               BankAccount.deleted == False).first()
            if account:
                account.user_id = data.get('user_id', account.user_id)
                account.account_type_id = data.get('account_type_id', account.account_type_id)
                account.branch_id = data.get('branch_id', account.branch_id)
                db.session.commit()
                output = bank_account_schema.dump(account)
                logger.info("bank account data updated successfully")
                response = ResponseGenerator(data=output, message="bank account data updated successfully",
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
            response = ResponseGenerator(data={}, message=error, success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()

    def delete(self, id):

        """Delete the bank account"""
        try:
            account = BankAccount.query.get(id)
            if account:
                if account.deleted == 1:
                    logger.info("bank account is already deleted")
                    return "bank account is already deleted"
                elif account.deleted == 0:
                    account.deleted = 1
                    db.session.commit()
                    logger.info("bank account deleted successfully")
                    response = ResponseGenerator(data=account, message="bank account deleted successfully",
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
            response = ResponseGenerator(data={}, message=error, success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()


