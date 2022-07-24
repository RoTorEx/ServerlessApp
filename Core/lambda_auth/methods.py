import json

from encoder import CustomEncoder, encode_auth_token


def build_response(status_code, body=None):
    '''Create responses function.'''

    response = {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
    }

    if body is not None:
        response["body"] = json.dumps(body, cls=CustomEncoder)

    return response


def get_auth():
    '''GET - http://.../auth'''

    return build_response(200, "Use POST method and enter your name.")


def post_auth(user_name):
    '''GET - http://.../auth'''

    data = {
        "name": user_name.lower()
    }

    return build_response(200, encode_auth_token(data))
