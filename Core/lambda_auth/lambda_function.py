import boto3


def lambda_handler(event, context):

    client = boto3.client("apigateway")

    response = client.get_api_key(
        apiKey="eqphr3i0pj",
    )
