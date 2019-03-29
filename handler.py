import json
import decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr


table_name = 'taxiTable'


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


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

def request_ride(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    print(event['queryStringParameters'])

    fe =   Attr('passenger_count').eq(int(event['queryStringParameters']['passenger_count'])) \
         & Attr('PULocationID').eq(int(event['queryStringParameters']['pickup_location'])) \
         & Attr('DOLocationID').eq(int(event['queryStringParameters']['dropoff_location'])) \
         & Attr('tpep_pickup_datetime').eq(event['queryStringParameters']['pickup_datetime'])

    scan_response = table.scan(FilterExpression=fe)

    response = {
        "statusCode": 200,
        "body": json.dumps(scan_response['Items'], cls=DecimalEncoder)
    }

    return response

# def list_availible_vendors(event, context):
#     response = {
#         "statusCode": 200,
#         "body": json.dumps(body)
#     }

#     return response
