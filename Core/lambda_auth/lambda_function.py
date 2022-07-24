import json

from methods import build_response, get_auth, post_auth


def lambda_handler(event, context):

    GET = "GET"
    POST = "POST"

    AUTH = "/auth"

    http_method = event["httpMethod"]
    path = event["path"]

    if http_method == POST:
        try:
            user_name = json.loads(event["body"])["name"]

        except KeyError:
            return build_response(400, "No 'name' value in body request!")

    if http_method == GET and path == AUTH:  # GET to /auth
        response = get_auth()

    elif http_method == POST and path == AUTH:  # POST to /auth
        response = post_auth(user_name)

    return response
