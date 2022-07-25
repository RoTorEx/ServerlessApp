import datetime

import jwt


def decode_auth_token(jwt_token):
    '''Decodes the auth token.'''
    date_time = datetime.datetime.now()
    key = datetime.datetime.strftime(date_time, "%Y-%m-%d %H:%M")

    try:
        decoded_data = jwt.decode(jwt_token, key, algorithms=['HS256'])
        return decoded_data

    except jwt.ExpiredSignatureError as e:
        print("Signature expired. Please log in again.\n", e)
        return

    except (jwt.InvalidTokenError, jwt.InvalidSignatureError) as e:
        print("Invalid token. Please log in again.\n", e)
        return
