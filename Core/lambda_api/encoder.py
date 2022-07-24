import datetime
import json
from decimal import Decimal

import jwt


def decode_auth_token(jwt_token):
    '''Decodes the auth token.'''
    date_time = datetime.datetime.now()
    key = datetime.datetime.strftime(date_time, "%Y-%m-%d %H:%M")

    try:
        return jwt.decode(jwt_token, key, algorithms=['HS256'])

    except jwt.ExpiredSignatureError:
        'Signature expired. Please log in again.'
        return

    except (jwt.InvalidTokenError, jwt.InvalidSignatureError):
        'Invalid token. Please log in again.'
        return


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)

        return json.JSONDecodeError.default(self, obj)
