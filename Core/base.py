from pathlib import Path


class DynamoDBControls:
    '''Interfaces for interaction with dynamoDB.'''

    @staticmethod
    def create_table(client, *args, **kwargs):
        '''Create table in DynamoDB.'''

        table_name = input("Enter the table name: ")

        try:
            response = client.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        "AttributeName": "id",
                        "KeyType": "HASH"
                    },
                ],

                AttributeDefinitions=[
                    {
                        "AttributeName": "id",
                        "AttributeType": "N"
                    },
                ],

                ProvisionedThroughput={
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1
                }
            )
            print("Table created successfully!")

            return response

        except Exception as e:
            print("Error creating table:")
            print(e)

    @staticmethod
    def delete_table(client, *args, **kwargs):
        '''Delete table from DynamoDB.'''

        table_name = input("Enter the table name: ")

        try:
            response = client.delete_table(
                TableName=table_name,
            )
            print("Table deleted successfully!")

            return response

        except Exception as e:
            print("Error deleting table:")
            print(e)

    @staticmethod
    def get_item(client, *args, **kwargs):
        '''Get item from DynamoDB by id.'''

        table_name = input("Enter the table name: ")
        table = client.Table(table_name)

        response = table.get_item(Key={"id": 1})
        print(response)

        print(response['Item'])
        print()


class S3Bucket():
    @staticmethod
    def upload(client, *args, **kwargs):
        '''Upload file to S3 Bucket.'''

        bucket = "csv-dropper"  # S3 Bucket
        file_name = "mall_customers.csv"  # Current name and the name under which the file will be loaded
        folder_name = ""  # Folder where the file will be uploaded
        key = folder_name + file_name

        data_path = str(Path(__file__).resolve().parent.parent) + "/Data"
        data_binary = open(data_path + "/" + file_name, "rb").read()

        try:
            client.put_object(Bucket=bucket, Key=key, Body=data_binary)
            print(f"File '{file_name}' uploaded successfully!")

        except Exception as e:
            print("Error uploading file:")
            print(e)
