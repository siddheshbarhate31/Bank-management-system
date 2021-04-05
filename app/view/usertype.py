from app import db
from app.model.user import UserType
from app.Schema.user_schema import user_type_schema
from flask import request
from flask_restful import Resource
from app.common.ResponseGenerator import ResponseGenerator
from flask_api import status
from app.common.logging import *


class UserTypeProfile(Resource):

    def post(self):

        """create a user type"""
        try:
            userdata = request.get_json()
            result = user_type_schema.validate(userdata)
            if result:
                logger.exception(result)
                response = ResponseGenerator(data={}, message=result,
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            user = UserType(user_type=userdata['user_type'])
            db.session.add(user)
            db.session.commit()
            output = user_type_schema.dump(user)
            logger.info("User type  successfully created")
            response = ResponseGenerator(data=output, message="User added  successfully", success=True,
                                         status=status.HTTP_201_CREATED)
            return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message="Missing or sending incorrect data to create an activity",
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()


    def get(self):

        """get all the user types"""
        try:
            all_users = UserType.query.all()
            output = []
            for user in all_users:
                current_user = {}
                current_user['id'] = user.id
                current_user['user_type'] = user.user_type
                output.append(current_user)
            logger.info("All User types data returned successfully")
            response = ResponseGenerator(data=output, message="All Users data returned successfully",
                                         success=True, status=status.HTTP_200_OK)
            return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message="Invalid data", success=False,
                                         status=status.HTTP_404_NOT_FOUND)
            return response.error_response()


class UserTypedata(Resource):

    """UserTypeData for GET(single user type), PUT(update user type), DELETE(delete user type)"""

    def get(self, id):

        """Gives the data of single user type with selected usertype id"""
        try:
            user = UserType.query.get(id)
            output = user_type_schema.dump(user)
            logger.info('User type data returned successfully')
            if user:
                response = ResponseGenerator(data=output, message="User data returned successfully",
                                             success=True, status=status.HTTP_200_OK)
                return response.success_response()
            else:
                logger.exception("User type id not found")
                response = ResponseGenerator(data={}, message="User id not found", success=False,
                                             status=status.HTTP_404_NOT_FOUND)
                return response.error_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message="User id not found", success=False,
                                         status=status.HTTP_404_NOT_FOUND)
            return response.error_response()


    def put(self, id):

        """Update the user type data """
        try:
            data = request.get_json()
            result = user_type_schema.validate(data)
            if result:
                logger.exception(result)
                response = ResponseGenerator(data={}, message=result,
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            user = UserType.query.filter(UserType.id == id)
            if user:
                user.user_type = data.get('user_type', user.user_type)
                db.session.commit()
                output = user_type_schema.dump(user)
                logger.info("User data updated successfully")
                response = ResponseGenerator(data=output, message="User data updated successfully", success=True,
                                             status=status.HTTP_200_OK)
                return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message="Missing or sending incorrect data to update an activity",
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()


    def delete(self, id):

        """delete the user type of selected user type id"""
        try:
            user = UserType.query.get(id)
            db.session.delete(user)
            db.session.commit()
            logger.info("User type data deleted successfully")
            return "User type data deleted successfully"
        except:
            logger.exception("User type id not found")
            response = ResponseGenerator(data={}, message="Missing or sending incorrect data to update an activity",
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()

