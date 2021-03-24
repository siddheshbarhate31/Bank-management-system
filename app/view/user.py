from app import db
from app.Schema.user_schema import user_schema
from app.model.user import User
from flask import request
from flask_restful import Resource
from app.common.ResponseGenerator import ResponseGenerator
from flask_api import status
from app.common.logging import *


class UserProfile(Resource):

    """class UserProfile for POST(create user) and GET(all users)"""

    def post(self):

        """Create user in the User table"""

        userdata = request.get_json()
        result = user_schema.validate(userdata)
        if result:
            logger.exception("Missing or sending incorrect data to create an activity")
            response = ResponseGenerator(data={}, message="Missing or sending incorrect data to create an activity",
                                         success=False, status=status.HTTP_404_NOT_FOUND)
            return response.error_response()
        user = User(first_name=userdata['first_name'],
                    last_name=userdata['last_name'],
                    address=userdata['address'],
                    mobile_number=userdata['mobile_number'],
                    email_id=userdata['email_id'],
                    is_deleted=0,
                    password=userdata['password'],
                    user_type_id=userdata['user_type_id'])
        db.session.add(user)
        db.session.commit()
        output = user_schema.dump(user)
        logger.info("User data successfully created")
        response = ResponseGenerator(data=output, message="User data successfully created", success=True,
                                     status=status.HTTP_201_CREATED)
        return response.success_response()



    def get(self):

        """Provides the data of all the users in the user table"""

        all_users = User.query.filter(User.is_deleted == 0)
        output = []
        for user in all_users:
            currentuser = {}
            currentuser['first_name'] = user.first_name
            currentuser['last_name'] = user.last_name
            currentuser['address'] = user.address
            currentuser['mobile_number'] = user.mobile_number
            currentuser['email_id'] = user.email_id
            currentuser['user_type_id'] = user.user_type_id
            output.append(currentuser)
        logger.info("All Users data returned successfully")
        response = ResponseGenerator(data=output, message="All Users data returned successfully", success=True,
                                     status=status.HTTP_200_OK)
        return response.success_response()


class UserData(Resource):

    """UserData for GET(single user), PUT(update user), DELETE(delete user)"""

    def get(self, user_id):

        """Gives the data of single user with selected user_id """

        user = User.query.filter(User.id == user_id, User.is_deleted == 0).first()
        output = user_schema.dump(user)
        logger.info('User data returned successfully')
        if user:
            response = ResponseGenerator(data=output, message="User data returned successfully", success=True,
                                         status=status.HTTP_200_OK)
            return response.success_response()
        else:
            logger.exception("User id not found")
            response = ResponseGenerator(data={}, message="User id not found", success=False,
                                         status=status.HTTP_404_NOT_FOUND)
            return response.error_response()

    def put(self, user_id):

        """Update the user data """

        data = request.get_json()
        result = user_schema.validate(data)
        if result:
            logger.warning('Missing or sending incorrect data to update an activity')
            response = ResponseGenerator(data={}, message="Missing or sending incorrect data to update an activity",
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()
        user = User.query.filter(User.id == user_id, User.is_deleted == 0).first()
        if user:
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.address = data.get('address', user.address)
            user.mobile_number = data.get('mobile_number', user.mobile_number)
            user.email_id = data.get('email_id', user.email_id)
            user.password = data.get('password', user.password)
            user.user_type_id = data.get('user_type_id', user.user_type_id)
            db.session.commit()
            output = user_schema.dump(user)
            logger.info("User data updated successfully")
            response = ResponseGenerator(data=output, message="User data updated successfully", success=True,
                                         status=status.HTTP_200_OK)
            return response.success_response()

    def delete(self, id):

        """Delete the user"""

        user = User.query.get(id)
        if user:
            if user.is_deleted == 1:
                logger.info("User is already deleted")
                return "User is already deleted"
            elif user.is_deleted == 0:
                user.is_deleted = 1
                db.session.commit()
                logger.info("User data deleted successfully")
                response = ResponseGenerator(data=user, message="User data deleted successfully", success=True,
                                             status=status.HTTP_200_OK)
                return response.success_response()
        else:
            logger.warning("User id not found")
            response = ResponseGenerator(data={}, message="User id not found", success=False,
                                         status=status.HTTP_404_NOT_FOUND)
            return response.error_response()

