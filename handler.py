import json
import boto3


def list_resources(event, context):
    dynamodb = boto3.resource('dynamodb')

    body = {
        "message": "List all sub-resources",
        "input": event,
        "resources": dynamodb.get_available_subresources()
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
