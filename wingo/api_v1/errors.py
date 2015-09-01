from flask import jsonify
from wingo.api_v1 import api 
from wingo.exceptions import CustomError
from mongoengine.errors import ValidationError

@api.app_errorhandler(404)  # this has to be an app-wide handler
def not_found(e):
    response = jsonify({'status': 404, 'error': 'not found', "success": False,
                        'message': 'invalid resource URI'})
    response.status_code = 404
    return response


@api.errorhandler(405)
def method_not_supported(e):
    response = jsonify({'status': 405, 'error': 'method not supported',"success": False,
                        'message': 'the method is not supported'})
    response.status_code = 405
    return response


# @api.app_errorhandler(500)  # this has to be an app-wide handler
# def internal_server_error(e):
#     response = jsonify({'status': 500, 'error': 'internal server error',"success": False,
#                         'message': e.args[0]})
#     response.status_code = 500
#     return response



@api.app_errorhandler(422)  # this has to be an app-wide handler
def internal_server_error(e):

    data = getattr(e, 'data')
    response = jsonify({'status': 422, 'error400': 'internal server error',"success": False,
                        'message': data['message']})
    response.status_code = 422
    return response


# Mongoengine validation error 
@api.app_errorhandler(ValidationError)
def bad_request(e):
    response = jsonify({'status': 400, 'error': 'mongo error',"success": False,
                        'message': ",".join(e.to_dict().values())})
    response.status_code = 400
    return response

# Custom error 
@api.app_errorhandler(CustomError)
def bad_request(e):
    response = jsonify({'status': 400, 'error': 'custom error',"success": False,
                        'message': e.args[0]})
    response.status_code = 400
    return response






