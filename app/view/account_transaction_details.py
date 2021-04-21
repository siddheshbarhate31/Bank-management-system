from app import db
from app.Schema.account_transaction_details_schema import account_transaction_detail_schema, account_transaction_details_schema
from app.model.account_transaction_details import AccountTransactionDetails
from app.model.bank_account import BankAccount
from flask import request
from flask_restful import Resource
from app.common.ResponseGenerator import ResponseGenerator
from app.common.Exception import IdNotFound
from flask_api import status
from app.common.logging import *
from sqlalchemy import desc


class AccountTransactionInfo(Resource):

    def post(self):

        """Add account transaction details in the AccountTransactionDetails table"""
        try:
            account_transaction_data = request.get_json()
            result = account_transaction_detail_schema.validate(account_transaction_data)
            if result:
                logger.exception(result)
                response = ResponseGenerator(data={}, message=result, success=False,
                                             status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()

            account = AccountTransactionDetails(transaction_amount=account_transaction_data['transaction_amount'],
                                                bank_account_id=account_transaction_data['bank_account_id'],
                                                transaction_type_id=account_transaction_data['transaction_type_id'],
                                                fund_id=account_transaction_data['fund_id'],
                                                transaction_status=account_transaction_data['transaction_status'])
            db.session.add(account)
            db.session.commit()
            output = account_transaction_detail_schema.dump(account)
            logger.info("Account transaction details successfully created")
            response = ResponseGenerator(data=output, message="Account transaction details successfully created",
                                         success=True, status=status.HTTP_201_CREATED)
            return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message=error, success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()

    def get(self):

        """Provides the details of all the account transactions"""

        try:
            all_account_transactions = AccountTransactionDetails.query.all()
            output = []
            for account in all_account_transactions:
                account_transaction = {}
                account_transaction['id'] = account.id
                account_transaction['transaction_amount'] = account.transaction_amount
                account_transaction['transaction_date'] = account.transaction_date
                account_transaction['bank_account_id'] = account.bank_account_id
                account_transaction['transaction_type_id'] = account.transaction_type_id
                account_transaction['fund_id'] = account.fund_id
                output.append(account_transaction)
            logger.info("All account transaction details returned successfully")
            response = ResponseGenerator(data=output, message="All account transaction details returned successfully",
                                         success=True, status=status.HTTP_200_OK)
            return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message=error, success=False,
                                         status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()


class AccountTransactionData(Resource):

    """AccountTransactionData for GET(account transaction), PUT(update account transaction),
       DELETE(delete account transaction)"""

    def get(self, id):

        """Gives the detail of account transaction of selected bank account id """
        try:
            account_data = BankAccount.query.filter(BankAccount.id == id).first()
            if account_data:
                mini_statement = AccountTransactionDetails.query.filter(AccountTransactionDetails.bank_account_id == id).order_by(desc(AccountTransactionDetails.id)).limit(10)
                if not mini_statement:
                    raise IdNotFound('id not found:{}'.format(id))
            output = account_transaction_details_schema.dump(mini_statement)
            logger.info('account transaction details returned successfully')
            response = ResponseGenerator(data=output, message="account transaction details returned successfully",
                                         success=True, status=status.HTTP_200_OK)
            return response.success_response()
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

        """Update the account transaction detail """
        try:
            data = request.get_json()
            result = account_transaction_detail_schema.validate(data)
            if result:
                logger.exception(result)
                response = ResponseGenerator(data={}, message=result,
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            account = AccountTransactionDetails.query.filter(AccountTransactionDetails.id == id).first()
            if account:
                account.transaction_amount = data.get('transaction_amount', account.transaction_amount)
                account.bank_account_id = data.get('bank_account_id', account.bank_account_id)
                account.transaction_type_id = data.get('transaction_type_id', account.transaction_type_id)
                account.fund_id = data.get('fund_id', account.fund_id)
                db.session.commit()
                output = account_transaction_detail_schema.dump(account)
                logger.info("account transaction details updated successfully")
                response = ResponseGenerator(data=output, message="account transaction details updated successfully",
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
            response = ResponseGenerator(data={}, message=error,
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()


