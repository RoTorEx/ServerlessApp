import enum
import logging

import boto3


class Var(enum.Enum):
    TABLE_NAME = "MallCustomers"
    TABLE = boto3.resource("dynamodb").Table(TABLE_NAME)

    LOGGER = logging.getLogger()
    LOGGER.setLevel(logging.INFO)


class Method(enum.Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"


class Path(enum.Enum):
    HOME = "/home"
    CUSTOMER = "/customer"
    CUSTOMERS = "/customers"
