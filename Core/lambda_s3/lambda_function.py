import json

import boto3


def lambda_handler(event, context):
    '''Implemention csv parser.'''

    table_name = "MallCustomers"

    s3 = boto3.client("s3")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    csv_file = event["Records"][0]["s3"]["object"]["key"]

    file_object = s3.get_object(Bucket=bucket, Key=csv_file)
    file_reader = file_object["Body"].read().decode("utf-8")
    data_list = []

    for index, line in enumerate(file_reader.split("\n")):

        if line and index >= 1:
            line = line.strip("\r").split(",")

            item = {
                "id": int(line[0]),
                "gender": str(line[1]),
                "age": int(line[2]),
                "annual income": int(line[3]),
                "spending score": int(line[4])
            }

            data_list.append(item)

    with table.batch_writer() as batch:

        for item in data_list:
            batch.put_item(
                Item=item
            )

    return "Success"
