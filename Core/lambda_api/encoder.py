import datetime
import json
from decimal import Decimal

import jwt


def encode_auth_token(data):
    '''Encodes to auth token.'''
    date_time = datetime.datetime.now()
    key = datetime.datetime.strftime(date_time, "%Y-%m-%d %H:%M")
    encode_data = jwt.encode(data, key, algorithm='HS256')

    response = {
        "token": encode_data
    }

    return response


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)

        return json.JSONDecodeError.default(self, obj)
