import json
import decimal
import boto3
import uuid
from urllib.parse import parse_qs
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

def ride(event, context):
    method = event['httpMethod']
    data = event['queryStringParameters']
    print(method, data)

    if method == 'GET':
        dynamodb = boto3.resource('dynamodb', region_name = 'us-east-1')
        table = dynamodb.Table(table_name)

        fe =  Attr('passenger_count').eq(int(data['passenger_count'])) & \
              Attr('PULocationID').eq(int(data['PULocationID'])) & \
              Attr('DOLocationID').eq(int(data['DOLocationID'])) & \
              Attr('tpep_pickup_datetime').eq(data['tpep_pickup_datetime'])

        scan_response = table.scan(FilterExpression=fe)
        if len(scan_response['Items']) > 0:
            item_to_return = scan_response['Items'][0]
        else:
            item_to_return = []

        response = {
            "statusCode": 200,
            "body": json.dumps(item_to_return, cls=DecimalEncoder)
        }
    
    elif method == 'POST':
        client = boto3.client('dynamodb', region_name = 'us-east-1')
        uuid_key = str(uuid.uuid4())

        client.put_item(
            TableName=table_name,
            Item={
                    'id': {
                        'S': uuid_key,
                    },
                    'VendorID': {
                        'N': data['VendorID'],
                        },
                    'tpep_pickup_datetime': {
                        'S': data['tpep_pickup_datetime'],
                        },
                    'tpep_dropoff_datetime': {
                        'S': data['tpep_dropoff_datetime'],
                        },
                    'passenger_count': {
                        'N': data['passenger_count'],
                        },
                    'trip_distance': {
                        'N': data['trip_distance'],
                        },
                    'PULocationID': {
                        'N': data['PULocationID'],
                        },
                    'DOLocationID': {
                        'N': data['DOLocationID'],
                        },
                    'RatecodeID': {
                        'N': data['RatecodeID'],
                        },
                    'store_and_fwd_flag': {
                        'S': data['store_and_fwd_flag'],
                        },
                    'payment_type': {
                        'N': data['payment_type'],
                        },
                    'fare_amount': {
                        'N': data['fare_amount'],
                        },
                    'extra': {
                        'N': data['extra'],
                        },
                    'mta_tax': {
                        'N': data['mta_tax'],
                        },
                    'improvement_surcharge': {
                        'N': data['improvement_surcharge'],
                        },
                    'tip_amount': {
                        'N': data['tip_amount'],
                        },
                    'tolls_amount': {
                        'N': data['tolls_amount'],
                        },
                    'total_amount': {
                        'N': data['total_amount']
                        },
                }
        )
        response = {
            "statusCode": 200,
            "body": f'Record {uuid_key} inserted successfully.'
        }
    
    else:
        response = {
            "statusCode": 405,
            "body": 'Method Not Allowed'
        }

    return response
