from app import db
from app.Schema.account_transaction_details_schema import fund_transfer_schema
from app.model.account_transaction_details import FundTransfer
from flask import request
from flask_restful import Resource
from app.common.ResponseGenerator import ResponseGenerator
from flask_api import status
from app.common.logging import *


class FundTransferInfo(Resource):

    def post(self):

        """Add fund transfer in the FundTransfer table"""
        try:
            fund_data = request.get_json()
            result = fund_transfer_schema.validate(fund_data)
            if result:
                logger.exception(result)
                response = ResponseGenerator(data={}, message=result, success=False,
                                             status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            fund = FundTransfer(source=fund_data['source'],
                                destination=fund_data['destination'])
            db.session.add(fund)
            db.session.commit()
            output = fund_transfer_schema.dump(fund)
            logger.info("fund transfer data successfully created")
            response = ResponseGenerator(data=output, message="fund transfer data successfully created",
                                         success=True, status=status.HTTP_201_CREATED)
            return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message="Missing or sending incorrect data to create an activity",
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()

    def get(self):

        """Provides the data of all the fund transfer"""
        try:
            all_fund_transfer = FundTransfer.query.all()
            output = []
            for transfer in all_fund_transfer:
                currentfund = {}
                currentfund['id'] = transfer.id
                currentfund['source'] = transfer.source
                currentfund['destination'] = transfer.destination
                output.append(currentfund)
            logger.info("All fund transfer data returned successfully")
            response = ResponseGenerator(data=output, message="All fund transfer data returned successfully",
                                         success=True, status=status.HTTP_200_OK)
            return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message="Invalid request", success=False,
                                         status=status.HTTP_404_NOT_FOUND)
            return response.error_response()


class FundTransferData(Resource):

    """ for FundTransferData GET(single fund transfer detail),
        PUT(update fund transfer), DELETE(delete fund transfer)"""

    def get(self, id):

        """Gives the data of single fund transfer  with selected fund transfer id """

        try:
            fund = FundTransfer.query.filter(FundTransfer.id == id).first()
            output = fund_transfer_schema.dump(fund)
            if fund:
                logger.info('fund transfer returned successfully')
                response = ResponseGenerator(data=output, message="fund transfer returned successfully",
                                             success=True, status=status.HTTP_200_OK)
                return response.success_response()
            else:
                logger.exception("fund transfer id not found")
                response = ResponseGenerator(data={}, message="fund transfer id not found", success=False,
                                             status=status.HTTP_404_NOT_FOUND)
                return response.error_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message="fund transfer id not found", success=False,
                                         status=status.HTTP_404_NOT_FOUND)
            return response.error_response()

    def put(self, id):

        """Update the fund transfer """

        try:
            data = request.get_json()
            result = fund_transfer_schema.validate(data)
            if result:
                logger.exception(result)
                response = ResponseGenerator(data={}, message=result,
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            fund = FundTransfer.query.filter(FundTransfer.id == id).first()
            if fund:
                fund.source = data.get('source', fund.source)
                fund.destination = data.get('destination', fund.destination)
                db.session.commit()
                output = fund_transfer_schema.dump(fund)
                logger.info("fund transfer updated successfully")
                response = ResponseGenerator(data=output, message="fund transfer updated successfully",
                                             success=True, status=status.HTTP_200_OK)
                return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message="Missing or sending incorrect data to update an activity",
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()

    def delete(self, id):

        """delete the fund transfer of selected fund transfer  id"""

        try:
            fund = FundTransfer.query.get(id)
            db.session.delete(fund)
            db.session.commit()
            logger.info("fund transfer deleted successfully")
            return "fund transfer deleted successfully"
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message="fund transfer id not found",
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()

