from app import db
from app.Schema.bank_account_schema import branch_detail_schema
from app.model.bank_account import BranchDetails
from flask import request
from flask_restful import Resource
from app.common.ResponseGenerator import ResponseGenerator
from app.common.Exception import IdNotFound
from flask_api import status
from app.common.logging import *


class BranchData(Resource):

    def post(self):

        """Add branch_details in the BranchDetails table"""
        try:
            branch_data = request.get_json()
            result = branch_detail_schema.validate(branch_data)
            if result:
                logger.exception(result)
                response = ResponseGenerator(data={}, message=result,
                                             success=False, status=status.HTTP_404_NOT_FOUND)
                return response.error_response()
            branch = BranchDetails(branch_name=branch_data['branch_name'],
                                   branch_address=branch_data['branch_address'])
            db.session.add(branch)
            db.session.commit()
            output = branch_detail_schema.dump(branch)
            logger.info("Branch data successfully created")
            response = ResponseGenerator(data=output, message="Branch data successfully created", success=True,
                                         status=status.HTTP_201_CREATED)
            return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message=error,
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()


    def get(self):

        """Provides the data of all the branch details"""
        try:
            all_branch_details = BranchDetails.query.all()
            output = []
            for branch in all_branch_details:
                currentbranch = {}
                currentbranch['id'] = branch.id
                currentbranch['branch_name'] = branch.branch_name
                currentbranch['branch_address'] = branch.branch_address
                output.append(currentbranch)
            logger.info("All branch data returned successfully")
            response = ResponseGenerator(data=output, message="All branch data returned successfully",
                                         success=True, status=status.HTTP_200_OK)
            return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message=error, success=False,
                                         status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()


class BranchInfo(Resource):

    """BranchInfo for GET(single branch detail), PUT(update branch detail), DELETE(delete branch detail)"""

    def get(self, id):

        """Gives the data of single branch detail with selected branch id """
        try:
            branch = BranchDetails.query.filter(BranchDetails.id == id).first()
            output = branch_detail_schema.dump(branch)
            logger.info('Branch data returned successfully')
            if branch:
                response = ResponseGenerator(data=output, message="Branch data returned successfully", success=True,
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
            response = ResponseGenerator(data={}, message=error, success=False,
                                         status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()

    def put(self, id):

        """Update the Branch Data """
        try:
            data = request.get_json()
            result = branch_detail_schema.validate(data, partial=True)
            if result:
                logger.exception(result)
                response = ResponseGenerator(data={}, message=result,
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            branch = BranchDetails.query.filter(BranchDetails.id == id).first()
            if branch:
                branch.branch_name = data.get('branch_name', branch.branch_name)
                branch.branch_address = data.get('branch_address', branch.branch_address)
                db.session.commit()
                output = branch_detail_schema.dump(branch)
                logger.info("Branch data updated successfully")
                response = ResponseGenerator(data=output, message="Branch data updated successfully", success=True,
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

    def delete(self, id):

        """delete the branch detail of selected branch  id"""
        try:
            branch = BranchDetails.query.get(id)
            if branch:
                db.session.delete(branch)
                db.session.commit()
                logger.info("Branch details deleted successfully")
                return "Branch details deleted successfully"
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
