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


def aws_dynamodb(client):
    '''Function for DynamoDB.'''

    dynamo_methods = list(filter(lambda meth: not meth.startswith("__"), dir(DynamoDBControls)))

    print(f"\nAvailable methods: {dynamo_methods}.\n")

    try:
        while True:
            user_input = input("Enter preferred work type: ").lower().strip()

            try:
                exec(f"DynamoDBControls.{user_input}(client)")
                sys.exit()

            except AttributeError:
                print("Unsupported method. Сheck out the documentation and try again.")
                continue

            except SyntaxError:
                print("Enter method's name.")
                continue

    except KeyboardInterrupt:
        sys.exit("\nThe program was stopped forcibly in DynamoDB control function.")


def aws_s3(client):
    '''Function for S3 Bucket.'''

    s3_methods = list(filter(lambda meth: not meth.startswith("__"), dir(S3Bucket)))

    print(f"\nAvailable methods: {s3_methods}.\n")

    try:
        while True:
            user_input = input("Enter preferred work type: ").lower().strip()

            try:
                exec(f"S3Bucket.{user_input}(client)")
                sys.exit()

            except AttributeError:
                print("Unsupported method. Сheck out the documentation and try again.")
                continue

            except SyntaxError:
                print("Enter method's name.")
                continue

    except KeyboardInterrupt:
        sys.exit("\nThe program was stopped forcibly in S3 control function.")


def main():
    '''Entry point to AWS DynamoDB & S3 Bucket.'''

    aws = {
        "dynamodb": aws_dynamodb,  # DynamoDB
        "s3": aws_s3,  # S3
    }

    aws_creds = get_credentials()

    try:
        while True:
            user_input = input("Choose preferred AWS: ").lower()

            if user_input in aws:
                client = boto3.client(service_name=user_input, region_name="us-east-1", **aws_creds)  # noqa
                aws[user_input](client)
                break

            else:
                print(f"Such service ({user_input}) does not exist in the current script.")
                continue

    except KeyboardInterrupt:
        sys.exit("\nThe program was stopped forcibly on main function.")


if __name__ == "__main__":
    main()
