from app import db
from app.model.user import UserType
from app.Schema.user_schema import user_type_schema
from flask import request
from flask_restful import Resource
from app.common.ResponseGenerator import ResponseGenerator
from flask_api import status


class UserTypeProfile(Resource):

    def post(self):
        """Add a user"""

        userdata = request.get_json()
        result = user_type_schema.validate(userdata)
        if result:
            response = ResponseGenerator(data={}, message="Entered Invalid user data", success=False,
                                         status=status.HTTP_404_NOT_FOUND)

            return response.error_response()

        user = UserType(id=userdata['id'],
                        user_type=userdata['user_type'])
        db.session.add(user)
        db.session.commit()
        output = user_type_schema.dump(user)
        response = ResponseGenerator(data=output, message="User added  successfully", success=True,
                                     status=status.HTTP_201_CREATED)
        return response.success_response()

    def get(self):
        all_users = UserType.query.all()
        output = []
        for user in all_users:
            current_user = {}
            current_user['id'] = user.id
            current_user['user_type'] = user.user_type
            output.append(current_user)
        response = ResponseGenerator(data=output, message="All Users data returned successfully",
                                     success=True, status=status.HTTP_200_OK)
        return response.success_response()


class UserTypedata(Resource):
    def get(self, id):
        user = UserType.query.get(id)
        output = user_type_schema.dump(user)
        if user:
            response = ResponseGenerator(data=output, message="User data returned successfully",
                                         success=True, status=status.HTTP_200_OK)
            return response.success_response()
        else:
            response = ResponseGenerator(data={}, message="User id not found", success=False,
                                         status=status.HTTP_404_NOT_FOUND)
            return response.error_response()

    def put(self, id):

        """Update the user data """

        data = request.get_json()
        result = user_type_schema.validate(data)
        if result:
            #logger.warning('Missing or sending incorrect data to update an activity')
            response = ResponseGenerator(data={}, message="Missing or sending incorrect data to update an activity",
                                         success=False, status=status.HTTP_400_BAD_REQUEST)
            return response.error_response()
        user = UserType.query.filter(UserType.id==id)
        if user:
            user.id = data.get('id', user.id)
            user.user_type = data.get('user_type', user.user_type)
            db.session.commit()
            output = user_type_schema.dump(user)
            #logger.info("User data updated successfully")
            response = ResponseGenerator(data=output, message="User data updated successfully", success=True,
                                         status=status.HTTP_200_OK)
            return response.success_response()

    def delete(self, id):
        user = UserType.query.get(id)
        db.session.delete(user)
        db.session.commit()
        response = ResponseGenerator(data={}, message="User data deleted successfully", success=True,
                                     status=status.HTTP_200_OK)
        return response.success_response()
        # else:
        #     response = ResponseGenerator(data={}, message="User id not found", success=False,
        #                                  status=status.HTTP_404_NOT_FOUND)
        #     return response.error_response()




