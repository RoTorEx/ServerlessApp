import json
import logging

import boto3
from methods import (
    build_response,
    delete_customer,
    get_customer,
    get_customers,
    get_home,
    patch_customer,
    post_customer,
)


def lambda_handler(event, context):
    '''Implemention of CRUD methods.'''

    TABLE_NAME = "MallCustomers"

    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"

    HOME = "/home"
    CUSTOMER = "/customer"
    CUSTOMERS = "/customers"

    table = boto3.resource("dynamodb").Table(TABLE_NAME)
    logger = logging.getLogger()

    http_method = event["httpMethod"]
    path = event["path"]

    logger.setLevel(logging.INFO)
    logger.info(event)

    if http_method == GET and path == HOME:  # GET to /home
        response = get_home()

    elif http_method == GET and path == CUSTOMER:  # GET to /customer
        response = get_customer(table, logger, event["queryStringParameters"]["id"])

    elif http_method == POST and path == CUSTOMER:  # POST to /customer
        response = post_customer(table, logger, json.loads(event["body"]))

    elif http_method == PATCH and path == CUSTOMER:  # PATCH to /customer
        request_body = json.loads(event["body"])
        response = patch_customer(table, logger,
                                  request_body["id"], request_body["update_key"], request_body["update_value"])

    elif http_method == DELETE and path == CUSTOMER:  # DELETE to /customer
        request_body = json.loads(event["body"])
        response = delete_customer(table, logger, request_body["id"])

    elif http_method == GET and path == CUSTOMERS:  # GET to /customers
        response = get_customers(table, logger)

    else:
        response = build_response(404, "Not Found :'(")

    return response
