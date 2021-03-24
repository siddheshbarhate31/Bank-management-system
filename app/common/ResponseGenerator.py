from flask_restful import Resource
from flask import jsonify, make_response


class ResponseGenerator(Resource):
    """ResponseGenerator for the success and failure details of the API's"""

    def __init__(self, data, message, success, status):
        self.data = data
        self.message = message
        self.success = success
        self.status = status

    def success_response(self):

        """Gives the success details for the API"""

        response = {'data': self.data,
                    'message': self.message,
                    'success': self.success,
                    'status': self.status}
        return make_response(jsonify(response), self.status)

    def error_response(self):

        """Gives the failure details for the API"""

        response = {'data': self.data,
                    'message': self.message,
                    'success': self.success,
                    'status': self.status}
        return make_response(jsonify(response), self.status)

