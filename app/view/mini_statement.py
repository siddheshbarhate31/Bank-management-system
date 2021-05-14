from app.model.account_transaction_details import AccountTransactionDetails
from app.model.bank_account import BankAccount
from flask_restful import Resource
from app.common.ResponseGenerator import ResponseGenerator
from app.common.Exception import IdNotFound
from app.Schema.account_transaction_details_schema import account_transaction_details_schema
from flask_api import status
from app.common.logging import *
from sqlalchemy import desc
from flask_jwt_extended import jwt_required


class MiniStatement(Resource):

    @jwt_required()
    def get(self, id):

        """Gives the detail of first 10 transactions of selected bank account  id """
        try:
            account_transaction = BankAccount.query.filter(BankAccount.id == id).first()
            if account_transaction:
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
