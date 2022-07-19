import json

from encoder import CustomEncoder


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


def get_home():
    '''GET - http://.../home'''

    return build_response(200, "Hello from home page! :D")


def get_customer(table, logger, id):
    '''GET - http://.../customer'''

    try:
        response = table.get_item(
            Key={
                "id": int(id)
            }
        )

    except:
        logger.exception("Do your custom error here. I am just gonna log it out here!")

    if "Item" in response:
        return build_response(200, response["Item"])

    else:
        return build_response(404, {"Message": f"Customer with ({id}) id not found."})


def post_customer(table, logger, request_body):
    '''POST - http://.../customer'''

    try:
        table.put_item(Item=request_body)
        body = {
            "Operation": "SAVE",
            "Message": "SUCCESS",
            "Item": request_body
        }

    except:
        logger.exception("Do your custom error here. I am just gonna log it out here!")

    return build_response(200, body)


def patch_customer(table, logger, id, update_key, update_value):
    '''PATCH - http://.../customer'''

    try:
        response = table.update_item(
            Key={
                "id": int(id)
            },
            UpdateExpression="set %s = :value" % update_key,
            ExpressionAttributeValues={
                ":value": update_value
            },
            ReturnValues="UPDATED_NEW"
        )

        body = {
            "Operation": "UPDATE",
            "Message": "SUCCESS",
            "UpdateAttrebutes": response
        }

    except:
        logger.exception("Do your custom error here. I am just gonna log it out here!")

    return build_response(200, body)


def delete_customer(table, logger, id):
    '''DELETE - http://.../customer'''

    try:
        respone = table.delete_item(
            Key={
                "id": int(id)
            },
            ReturnValues="ALL_OLD"
        )

        body = {
            "Operation": "DELETE",
            "Message": "SUCCESS",
            "deletedItem": respone
        }

    except:
        logger.exception("Do your custom error here. I am just gonna log it out here!")

    if "Attributes" in body["deletedItem"]:
        return build_response(200, body)

    else:
        return build_response(404, {"Message": f"Customer with ({id}) id not found."})


def get_customers(table, logger):
    '''GET - http://.../customers'''

    try:
        response = table.scan()
        result = response["Items"]

        while "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            result.extend(response["Items"])

        body = {
            "customers": result
        }

    except:
        logger.exception("Do your custom error here. I am just gonna log it out here!")

    return build_response(200, body)
