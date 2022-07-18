import sys
from pathlib import Path
import configparser

import boto3

from base import DynamoDBControls, S3Bucket


def get_credentials():
    '''Function get credentials for a successful connection with AWS.'''

    core_path = str(Path(__file__).resolve().parent)

    creds = configparser.ConfigParser()
    creds.read(core_path + "/.aws/credentials.ini")

    aws_creds = {
        "aws_access_key_id": creds["CREDENTIALS"]["aws_access_key_id"],
        "aws_secret_access_key": creds["CREDENTIALS"]["aws_secret_access_key"]
    }

    return aws_creds


def aws_dynamodb(service_name, aws_creds):
    '''Function for DynamoDB.'''

    table_name = "MallCustomers"  # noqa
    dynamo_methods = list(filter(lambda meth: not meth.startswith("_"), dir(DynamoDBControls)))

    print(f"\nAvailable methods: {dynamo_methods}.\n")

    session = DynamoDBControls(service_name, aws_creds, table_name)  # noqa

    while True:
        user_input = input("Enter preferred work type or skip to quit: ").lower().strip()

        if user_input in dynamo_methods:
            exec(f"session.{user_input}()")
            print("==< ~ >===")

        elif not user_input:
            break

        else:
            print("Unsupported method. Сheck out the documentation and try again.")


def aws_s3(service_name, aws_creds):
    '''Function for S3 Bucket.'''

    s3_methods = list(filter(lambda meth: not meth.startswith("_"), dir(S3Bucket)))

    print(f"\nAvailable methods: {s3_methods}.\n")

    session = S3Bucket(service_name, aws_creds)  # noqa

    while True:
        user_input = input("Enter preferred work type or skip to quit: ").lower().strip()

        if user_input in s3_methods:
            exec(f"session.{user_input}()")
            print("==< ~ >===\n")

        elif not user_input:
            break

        else:
            print("Unsupported method. Сheck out the documentation and try again.")


def main():
    '''Entry point to AWS DynamoDB & S3 Bucket.'''

    aws = {
        "dynamodb": aws_dynamodb,
        "s3": aws_s3,
    }

    while True:
        print("Available services:", [srvs for srvs in aws])
        user_input = input("Choose preferred AWS  or skip to exit: ").lower()

        if user_input in aws:
            aws[user_input](user_input, get_credentials())

        elif not user_input:
            sys.exit()

        else:
            print(f"Such service ({user_input}) does not exist in the current script.")
            continue


if __name__ == "__main__":
    main()
