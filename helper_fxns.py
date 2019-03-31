import boto3
import uuid
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# Get the service resource.
dynamodb_resource = boto3.resource('dynamodb', region_name = 'us-east-1')
dynamodb_client = boto3.client('dynamodb', region_name = 'us-east-1')
table_name = 'taxiTable'


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def request_ride(event_dict):
    table = dynamodb_resource.Table(table_name)

    fe = Attr('passenger_count').eq(event_dict['passenger_count']) & \
         Attr('PULocationID').eq(event_dict['pickup_location']) & \
         Attr('DOLocationID').eq(event_dict['dropoff_location'])

    scan_response = table.scan(FilterExpression=fe)

    response = {
        "statusCode": 200,
        "body": json.dumps(scan_response['Items'], cls=DecimalEncoder)
    }

    return response


response = request_ride({
    'passenger_count': 2,
    'pickup_location': 249,
    'dropoff_location': 246
    })
print(response)