from app import db
from app.Schema.account_transaction_details_schema import transaction_type_schema
from app.model.account_transaction_details import TransactionType
from flask import request
from flask_restful import Resource
from app.common.ResponseGenerator import ResponseGenerator
from app.common.Exception import IdNotFound
from flask_api import status
from app.common.logging import *


class TransactionTypeDetails(Resource):

    def post(self):

        """Add transaction type in the TransactionType table"""

        try:
            transaction_data = request.get_json()
            result = transaction_type_schema.validate(transaction_data)
            if result:
                logger.exception(result)
                response = ResponseGenerator(data={}, message=result, success=False,
                                             status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            account = TransactionType(transaction_type=transaction_data['transaction_type'])
            db.session.add(account)
            db.session.commit()
            output = transaction_type_schema.dump(account)
            logger.info("transaction type details successfully created")
            response = ResponseGenerator(data=output, message="transaction type details successfully created",
                                         success=True, status=status.HTTP_201_CREATED)
            return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message=error,
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()

    def get(self):

        """Provides the details of all the transaction type"""

        try:
            all_transaction_type = TransactionType.query.all()
            output = []
            for transaction in all_transaction_type:
                currenttransaction = {}
                currenttransaction['id'] = transaction.id
                currenttransaction['transaction_type'] = transaction.transaction_type
                output.append(currenttransaction)
            logger.info("All transaction type details returned successfully")
            response = ResponseGenerator(data=output, message="All transaction type details returned successfully",
                                         success=True, status=status.HTTP_200_OK)
            return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message=error, success=False,
                                         status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()


class TransactionTypeData(Resource):

    """ for TransactionTypeData GET(single transaction type detail),
        PUT(update transaction type), DELETE(delete transaction type detail)"""

    def get(self, id):

        """Gives the data of single transaction type  with selected transaction type id """

        try:
            transaction = TransactionType.query.filter(TransactionType.id == id).first()
            output = transaction_type_schema.dump(transaction)
            if transaction:
                logger.info('transaction type returned successfully')
                response = ResponseGenerator(data=output, message="transaction type returned successfully",
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

        """Update the Transaction type """

        try:
            data = request.get_json()
            result = transaction_type_schema.validate(data)
            if result:
                logger.exception(result)
                response = ResponseGenerator(data={}, message=result,
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            transaction = TransactionType.query.filter(TransactionType.id == id).first()
            if transaction:
                transaction.transaction_type = data.get('transaction_type', transaction.transaction_type)
                db.session.commit()
                output = transaction_type_schema.dump(transaction)
                logger.info("transaction_type updated successfully")
                response = ResponseGenerator(data=output, message="transaction_type updated successfully",
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


