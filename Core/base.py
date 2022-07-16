class DynamoDBControls:
    '''Interfaces for interaction with dynamoDB.'''

    @staticmethod
    def create_table(client, *args, **kwargs):
        '''Create table in DynamoDB.'''

        table_name = input("Enter the name of the table to create: ")

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

        table_name = input("Enter the name of the table to delete: ")

        try:
            response = client.delete_table(
                TableName=table_name,
            )
            print("Table deleted successfully!")

            return response

        except Exception as e:
            print("Error deleting table:")
            print(e)
