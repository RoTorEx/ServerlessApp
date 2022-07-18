from pathlib import Path

import boto3


class DynamoDBControls:
    '''Interfaces for interaction with DynamoDB.'''

    _client = None

    def __init__(self, service_name, aws_creds, table_name):
        self._client = boto3.client(service_name=service_name, region_name="us-east-1", **aws_creds)
        self.table_name = table_name

    def create_table(self):
        '''Create table in DynamoDB.'''

        response = self._client.create_table(
            TableName=self.table_name,
            KeySchema=[
                {
                    "AttributeName": "id",
                    "KeyType": "HASH"
                },
            ],

            AttributeDefinitions=[
                {
                    "AttributeName": "id",
                    "AttributeType": "S"
                },
            ],

            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1
            }
        )
        print(f"Table '{self.table_name}' created successfully!")

        return response

    def delete_table(self):
        '''Delete table from DynamoDB.'''

        response = self._client.delete_table(
            TableName=self.table_name,
        )
        print(f"Table '{self.table_name}' deleted successfully!")

        return response

    def get_item(self):
        '''Get item from DynamoDB by id.'''

        response = self._client.get_item(
            TableName=self.table_name,
            Key={"id": {"S": "0001"}}
        )

        print(f"Item: {response['Item']}")

    def put_item(self):
        '''Put item to DynamoDB.'''

        response = self._client.put_item(
            TableName=self.table_name,
            Item={
                "id": {"S": "0001"},
                "gender": {"S": "Male"},
                "age": {"N": "19"},
                "annual income": {"N": "15"},
                "spending score": {"N": "39"}
            }
        )
        print("Item insert into DynamoDB successfully!")

        return response


class S3Bucket:
    '''Interfaces for interaction with S3.'''

    _client = None

    def __init__(self, service_name, aws_creds):
        self._client = boto3.client(service_name=service_name, region_name="us-east-1", **aws_creds)

    def upload(self):
        '''Upload file to S3 Bucket.'''

        bucket = "csv-dropper"  # S3 Bucket
        file_name = "mall_customers.csv"  # Current name and the name under which the file will be loaded
        folder_name = ""  # Folder where the file will be uploaded
        key = folder_name + file_name

        data_path = str(Path(__file__).resolve().parent.parent) + "/Data"
        data_binary = open(data_path + "/" + file_name, "rb").read()

        self._client.put_object(Bucket=bucket, Key=key, Body=data_binary)
        print(f"File '{file_name}' uploaded successfully!")
