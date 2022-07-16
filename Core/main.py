import sys
from pathlib import Path
import configparser

import boto3

from base import DynamoDBControls


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


def main():
    '''Entry point to DynamoDBControls.'''

    class_methods = list(filter(lambda meth: not meth.startswith("__"), dir(DynamoDBControls)))
    aws_creds = get_credentials()
    client = boto3.client('dynamodb', region_name='us-east-1', **aws_creds)  # noqa

    print(f"\nAvailable methods: {class_methods}.\n")

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
        sys.exit("\nThe program was stopped forcibly.")


if __name__ == "__main__":
    main()
