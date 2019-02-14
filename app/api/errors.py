from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    payload = {
        'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error'),
        'status_code': status_code
    }
    if message:
        payload['message'] = message
    return jsonify(payload)


def bad_request(message):
    return error_response(400, message)