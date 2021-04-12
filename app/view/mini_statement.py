from app.model.account_transaction_details import AccountTransactionDetails
from flask_restful import Resource
from app.common.ResponseGenerator import ResponseGenerator
from flask_api import status
from app.common.logging import *


class MiniStatement(Resource):

    def get(self):

        """Provides the details of all the account transactions"""

        try:
            for i in range(10):
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
                response = ResponseGenerator(data=output,
                                             message="All account transaction details returned successfully",
                                             success=True, status=status.HTTP_200_OK)
                return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message="Sending invalid request", success=False,
                                         status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()
