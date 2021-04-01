from app import db
from app.Schema.bank_account_schema import branch_detail_schema
from app.model.bank_account import BranchDetails
from flask import request
from flask_restful import Resource
from app.common.ResponseGenerator import ResponseGenerator
from flask_api import status
from app.common.logging import *


class BranchData(Resource):

    def post(self):

        """Create branch_details in the BranchDetails table"""

        branch_data = request.get_json()
        result = branch_detail_schema.validate(branch_data)
        if result:
            logger.exception(result)
            response = ResponseGenerator(data={}, message="Missing or sending incorrect data to create an activity",
                                         success=False, status=status.HTTP_404_NOT_FOUND)
            return response.error_response()
        branch = BranchDetails(branch_address=branch_data['branch_address'])
        db.session.add(branch)
        db.session.commit()
        output = branch_detail_schema.dump(branch)
        logger.info("Branch data successfully created")
        response = ResponseGenerator(data=output, message="Branch data successfully created", success=True,
                                     status=status.HTTP_201_CREATED)
        return response.success_response()

    def get(self):

        """Provides the data of all the branch details"""

        all_branch_details = BranchDetails.query.all()
        output = []
        for branch in all_branch_details:
            currentbranch = {}
            currentbranch['branch_id'] = branch.branch_id
            currentbranch['branch_address'] = branch.branch_address
            output.append(currentbranch)
        logger.info("All branch data returned successfully")
        response = ResponseGenerator(data=output, message="All branch data returned successfully",
                                     success=True, status=status.HTTP_200_OK)
        return response.success_response()


class BranchInfo(Resource):

    """BranchInfo for GET(single branch detail), PUT(update branch detail), DELETE(delete branch detail)"""

    def get(self, branch_id):

        """Gives the data of single branch detail with selected branch id """

        branch = BranchDetails.query.filter(BranchDetails.branch_id == branch_id).first()
        output = branch_detail_schema.dump(branch)
        logger.info('Branch data returned successfully')
        if branch:
            response = ResponseGenerator(data=output, message="Branch data returned successfully", success=True,
                                         status=status.HTTP_200_OK)
            return response.success_response()
        else:
            logger.exception("Branch id not found")
            response = ResponseGenerator(data={}, message="Branch id not found", success=False,
                                         status=status.HTTP_404_NOT_FOUND)
            return response.error_response()

    def put(self, branch_id):

        """Update the Branch Data """

        data = request.get_json()
        result = branch_detail_schema.validate(data)
        if result:
            logger.warning(result)
            response = ResponseGenerator(data={}, message="Missing or sending incorrect data to update an activity",
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()
        branch = BranchDetails.query.filter(BranchDetails.branch_id == branch_id).first()
        if branch:
            branch.branch_id = data.get('branch_id', branch.branch_id)
            branch.branch_address = data.get('branch_address', branch.branch_address)
            db.session.commit()
            output = branch_detail_schema.dump(branch)
            logger.info("Branch data updated successfully")
            response = ResponseGenerator(data=output, message="Branch data updated successfully", success=True,
                                         status=status.HTTP_200_OK)
            return response.success_response()

    def delete(self, branch_id):

        """delete the account type of selected account type id"""
        try:
            branch = BranchDetails.query.get(branch_id)
            db.session.delete(branch)
            db.session.commit()
            logger.info("Branch details deleted successfully")
            return "Branch details deleted successfully"
        except:
            logger.exception("branch details id not found")
            response = ResponseGenerator(data={}, message="Missing or sending incorrect data to update an activity",
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()

