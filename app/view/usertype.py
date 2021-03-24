from app import db
from app.model.user import UserType
from app.Schema.user_schema import user_type_schema
from flask import request
from flask_restful import Resource
from app.common.ResponseGenerator import ResponseGenerator
from flask_api import status


class UserTypeProfile(Resource):


    def post(self):
        try:
            userdata = request.get_json()
            result = user_type_schema.validate(userdata)
            if result:
                return {
                           "message": "Missing or sending incorrect data to create an activity. {}".format(result)
                       }, 400
            user = UserType(id=userdata['id'],
                            user_type=userdata['user_type'])
            db.session.add(user)
            db.session.commit()
            output = user_type_schema.dump(user)
            response = ResponseGenerator(data=output, message="User added  successfully", success=True,
                                         status=status.HTTP_201_CREATED)
            return response.success_response()
        except:
            response = ResponseGenerator(data={}, message="Entered Invalid user data", success=False,
                                         status=status.HTTP_404_NOT_FOUND)
            return response.error_response(), status.HTTP_404_NOT_FOUND

    def get(self):
        all_users = UserType.query.all()
        output = []
        for user in all_users:
            current_user = {}
            current_user['id'] = user.id
            current_user['user_type'] = user.user_type
            output.append(current_user)
        response = ResponseGenerator(data=output, message="All Users data returned successfully", success=True,
                                     status=status.HTTP_200_OK)
        return response.success_response()


class UserTypedata(Resource):
    def get(self, id):
        user = UserType.query.get(id)
        output = user_type_schema.dump(user)
        if user:
            response = ResponseGenerator(data=output, message="User data returned successfully", success=True,
                                         status=status.HTTP_200_OK)
            return response.success_response()
        else:
            response = ResponseGenerator(data={}, message="User id not found", success=False,
                                         status=status.HTTP_404_NOT_FOUND)
            return response.error_response()

    def delete(self, id):
        user = UserType.query.get(id)
        db.session.delete(user)



