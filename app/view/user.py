from app import db
import bcrypt
from app.Schema.user_schema import user_schema
from app.model.user import User, UserType
from flask_restful import Resource
from app.common.ResponseGenerator import ResponseGenerator
from app.common.Exception import IdNotFound
from flask_api import status
from app.common.logging import *
from app.Schema.user_schema import if_email_id_exist, if_mobile_no_exist
from flask import request
from flask_jwt_extended import jwt_required


class UserProfile(Resource):

    """class UserProfile for POST(create user) and GET(all users)"""

    @jwt_required()
    def post(self):

        """Create user in the User table"""
        try:
            userdata = request.get_json()
            result = user_schema.validate(userdata)
            if result:
                logger.exception(result)
                response = ResponseGenerator(data={}, message=result,
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            if if_email_id_exist(userdata['email_id']):
                logger.warning("Email_id is already taken")
                response = ResponseGenerator(data={}, message="Email_id is already taken",
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            if if_mobile_no_exist(userdata['mobile_number']):
                logger.warning("Mobile number is already taken")
                response = ResponseGenerator(data={}, message="Mobile number is already taken",
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            usertype = UserType.query.filter(UserType.id == userdata['user_type_id']).first()
            if not usertype:
                response = ResponseGenerator(data={}, message="Invalid usertype",
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            hashed = bcrypt.hashpw(userdata['password'].encode('utf-8'), bcrypt.gensalt())
            user = User(first_name=userdata['first_name'],
                        last_name=userdata['last_name'],
                        address=userdata['address'],
                        mobile_number=userdata['mobile_number'],
                        email_id=userdata['email_id'],
                        is_deleted=0,
                        password=hashed,
                        user_type_id=userdata['user_type_id'])
            db.session.add(user)
            db.session.commit()
            output = user_schema.dump(user)
            logger.info("User data successfully created")
            response = ResponseGenerator(data=output, message="User data successfully created", success=True,
                                         status=status.HTTP_201_CREATED)
            return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message=error,
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()

    @jwt_required()
    def get(self):

        """Provides the data of all the users in the user table"""
        try:
            all_users = User.query.filter(User.is_deleted == 0)
            output = []
            for user in all_users:
                currentuser = {}
                currentuser['id'] = user.id
                currentuser['first_name'] = user.first_name
                currentuser['last_name'] = user.last_name
                currentuser['address'] = user.address
                currentuser['mobile_number'] = user.mobile_number
                currentuser['email_id'] = user.email_id
                currentuser['user_type_id'] = user.user_type_id
                currentuser['created_on'] = user.created_on
                output.append(currentuser)
            logger.info("All Users data returned successfully")
            response = ResponseGenerator(data=output, message="All Users data returned successfully", success=True,
                                         status=status.HTTP_200_OK)
            return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message=error, success=False,
                                         status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()


class UserData(Resource):

    """UserData for GET(single user), PUT(update user), DELETE(delete user)"""

    @jwt_required()
    def get(self, id):

        """Gives the data of single user with selected user_id """
        try:
            user = User.query.filter(User.id == id, User.is_deleted == 0).first()
            output = user_schema.dump(user)
            logger.info('User data returned successfully')
            if user:
                response = ResponseGenerator(data=output, message="User data returned successfully",
                                             success=True,
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

    @jwt_required()
    def put(self, id):

        """Update the user data """
        try:
            data = request.get_json()
            result = user_schema.validate(data, partial=True)
            if result:
                logger.exception(result)
                response = ResponseGenerator(data={}, message=result, success=False,
                                             status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            user = User.query.filter(User.id == id, User.is_deleted == 0).first()
            hashed = bcrypt.hashpw(data.get('password', user.password).encode('utf-8'), bcrypt.gensalt())
            if user:
                user.first_name = data.get('first_name', user.first_name)
                user.last_name = data.get('last_name', user.last_name)
                user.address = data.get('address', user.address)
                user.mobile_number = data.get('mobile_number', user.mobile_number)
                user.email_id = data.get('email_id', user.email_id)
                user.password = hashed
                user.user_type_id = data.get('user_type_id', user.user_type_id)
                db.session.commit()
                output = user_schema.dump(user)
                logger.info("User data updated successfully")
                response = ResponseGenerator(data=output, message="User data updated successfully", success=True,
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

    @jwt_required()
    def delete(self, id):

        """Delete the user"""
        try:
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
