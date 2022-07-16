import json

from enums import Var, Method, Path
from custom_encoder import CustomEncoder


def lambda_handler(event, context):
    '''Implemention of CRUD methods.'''

    Var.LOGGER.value.info(event)

    http_method = event["httpMethod"]
    path = event["path"]

    if http_method == Method.GET.value and path == Path.HOME.value:  # GET to /home
        response = get_home()

    elif http_method == Method.GET.value and path == Path.CUSTOMER.value:  # GET to /customer
        response = get_customer(int(event["queryStringParameters"]["id"]))

    elif http_method == Method.POST.value and path == Path.CUSTOMER.value:  # POST to /customer
        response = post_customer(json.loads(event["body"]))

    elif http_method == Method.PATCH.value and path == Path.CUSTOMER.value:  # PATCH to /customer
        request_body = json.loads(event["body"])
        response = patch_customer(request_body["id"], request_body["update_key"], request_body["update_value"])

    elif http_method == Method.DELETE.value and path == Path.CUSTOMER.value:  # DELETE to /customer
        request_body = json.loads(event["body"])
        response = delete_customer(request_body["id"])

    elif http_method == Method.GET.value and path == Path.CUSTOMERS.value:  # GET to /customers
        response = get_customers()

    else:
        response = build_response(404, "Not Found :'(")

    return response


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


def get_customer(id):
    '''GET - http://.../customer'''

    try:
        response = Var.TABLE.value.get_item(
            Key={
                "id": id
            }
        )

        if "Item" in response:
            return build_response(200, response["Item"])
        else:
            return build_response(404, {"Message": f"Customers with ({id}) id not found."})

    except:
        Var.LOGGER.value.exception("Do your custom error here. I am just gonna log it out here!")


def post_customer(request_body):
    '''POST - http://.../customer'''

    try:
        Var.TABLE.value.put_item(Item=request_body)
        body = {
            "Operation": "SAVE",
            "Message": "SUCCESS",
            "Item": request_body
        }
        return build_response(200, body)

    except:
        Var.LOGGER.value.exception("Do your custom error here. I am just gonna log it out here!")


def patch_customer(id, update_key, update_value):
    '''PATCH - http://.../customer'''

    try:
        response = Var.TABLE.value.update_item(
            Key={
                "id": id
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

        return build_response(200, body)

    except:
        Var.LOGGER.value.exception("Do your custom error here. I am just gonna log it out here!")


def delete_customer(id):
    '''DELETE - http://.../customer'''

    try:
        respone = Var.TABLE.value.delete_item(
            Key={
                "id": id
            },
            ReturnValues="ALL_OLD"
        )

        body = {
            "Operation": "DELETE",
            "Message": "SUCCESS",
            "deletedItem": respone
        }

        return build_response(200, body)

    except:
        Var.LOGGER.value.exception("Do your custom error here. I am just gonna log it out here!")


def get_customers():
    '''GET - http://.../customers'''

    try:
        response = Var.TABLE.value.scan()
        result = response["Items"]

        while "LastEvaluatedKey" in response:
            response = Var.TABLE.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            result.extend(response["Items"])

        body = {
            "products": result
        }

        return build_response(200, body)

    except:
        Var.LOGGER.value.exception("Do your custom error here. I am just gonna log it out here!")




# # from set_env import AWS_CREDS, AWS_VARS  # Delete from AWS Lambda
# from custom_encoder import CustomEncoder


# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# table_name = "MallCustomers"
# # dynamodb = boto3.resource("dynamodb", region_name='us-east-1', **AWS_CREDS)  # Delete from AWS Lambda
# dynamodb = boto3.resource("dynamodb")  # Put that code to AWS Lambda
# table = dynamodb.Table(table_name)
