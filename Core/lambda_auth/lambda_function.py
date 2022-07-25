from decoder import decode_auth_token


def lambda_handler(event, context):
    '''Check JWT token.'''
    USER_WHITE_LIST = ["admin", "alex", "sergey"]

    jwt_token = event["authorizationToken"]
    decoded_data = decode_auth_token(jwt_token)

    if "name" in decoded_data and decoded_data["name"] in USER_WHITE_LIST:
        auth = 'Allow'

    else:
        auth = 'Deny'

    authResponse = {"principalId": decoded_data["name"], "policyDocument": {
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "execute-api:Invoke",
            "Resource": ["arn:aws:execute-api:us-east-1:384246938732:yvqhf40uva/*/*"],
            "Effect": auth
        }]
    }}

    return authResponse
