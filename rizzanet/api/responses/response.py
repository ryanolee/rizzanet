from flask import jsonify
from .http_status_codes import http_status

def api_error(error_message,code=500):
    if isinstance( error_message, int):
        code = error_message
        error_message =  http_status.get_error_message(code)

    return jsonify(
        code=code,
        error_message=error_message
    ), code

def api_response(data,code=200):
    response_dict={'code':code,'result':data}
    return jsonify(**response_dict), code
