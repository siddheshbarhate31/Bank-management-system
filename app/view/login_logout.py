from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from app.model.user import User
from flask import request
from flask_restful import Resource
from app.common.ResponseGenerator import ResponseGenerator
from flask_api import status
from app.common.logging import *
from app import db
from datetime import timezone
from datetime import datetime
from flask_jwt_extended import get_jwt
from app.model.login_logout import TokenBlocklist
import bcrypt


class Login(Resource):

    def post(self):
        try:
            user_email_id = request.json.get('email_id')
            password = request.json.get('password')
            if not user_email_id:
                logger.warning("Missing user email id")
                response = ResponseGenerator(data={}, message="Email Missing",
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            if not password:
                logger.warning("Missing Password")
                response = ResponseGenerator(data={}, message="Missing Password",
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            user = User.query.filter_by(email_id=user_email_id).first()
            if not user:
                logger.warning("Invalid user email entered")
                response = ResponseGenerator(data={}, message="Invalid user email entered",
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                access_token = create_access_token(identity={'email_id': user_email_id, 'password': password})
                logger.info("Successfully Logged in")
                response = ResponseGenerator(data={"access_token": access_token},
                                             message="You are successfully Logged in!", success=True,
                                             status=status.HTTP_201_CREATED)
                return response.success_response()
            else:
                logger.warning("Invalid password entered")
                response = ResponseGenerator(data={}, message="Invalid password entered",
                                             success=False, status=status.HTTP_400_BAD_REQUEST)
                return response.error_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message=error,
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()


class Logout(Resource):

    @jwt_required()
    def delete(self):
        try:
            jti = get_jwt()["jti"]
            now = datetime.now(timezone.utc)
            db.session.add(TokenBlocklist(jti=jti, created_at=now))
            db.session.commit()
            logger.info("You have been logged out!")
            response = ResponseGenerator(data={}, message="You have been logged out!",
                                         success=True, status=status.HTTP_200_OK)
            return response.success_response()
        except Exception as error:
            logger.exception(error)
            response = ResponseGenerator(data={}, message=error,
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()
