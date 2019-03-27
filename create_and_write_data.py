import csv
import boto3
import uuid
import json

# Get the service resource.
dynamodb_resource = boto3.resource('dynamodb', region_name = 'us-east-1')
dynamodb_client = boto3.client('dynamodb', region_name = 'us-east-1')
table_name = 'taxiTable'

def create_taxi_table(cxn, table_name):
    cxn.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'},
        ],
        BillingMode='PROVISIONED',
        ProvisionedThroughput={
            'ReadCapacityUnits': 123,
            'WriteCapacityUnits': 123
        }
    )
    print('Table Created')

def write_row(row, table_name, client):
    try:
        client.put_item(
            TableName=table_name,
            Item={
                    'id': {
                        'S': str(uuid.uuid4()),
                    },
                    'VendorID': {
                        'N': row['VendorID'],
                        },
                    'tpep_pickup_datetime': {
                        'S': row['tpep_pickup_datetime'],
                        },
                    'tpep_dropoff_datetime': {
                        'S': row['tpep_dropoff_datetime'],
                        },
                    'passenger_count': {
                        'N': row['passenger_count'],
                        },
                    'trip_distance': {
                        'N': row['trip_distance'],
                        },
                    'PULocationID': {
                        'N': row['PULocationID'],
                        },
                    'DOLocationID': {
                        'N': row['DOLocationID'],
                        },
                    'RatecodeID': {
                        'N': row['RatecodeID'],
                        },
                    'store_and_fwd_flag': {
                        'S': row['store_and_fwd_flag'],
                        },
                    'payment_type': {
                        'N': row['payment_type'],
                        },
                    'fare_amount': {
                        'N': row['fare_amount'],
                        },
                    'extra': {
                        'N': row['extra'],
                        },
                    'mta_tax': {
                        'N': row['mta_tax'],
                        },
                    'improvement_surcharge': {
                        'N': row['improvement_surcharge'],
                        },
                    'tip_amount': {
                        'N': row['tip_amount'],
                        },
                    'tolls_amount': {
                        'N': row['tolls_amount'],
                        },
                    'total_amount': {
                        'N': row['total_amount']
                        },
                }
        )
    except Exception as e:
        print('PUT EXCEPTION', e)

try:
    create_taxi_table(dynamodb_resource, table_name)
except dynamodb_client.exceptions.ResourceInUseException:
    print(f'{table_name} table already exists.')

# df = pd.read_csv('yellow_tripdata_2018-12.csv.part')
# for row_id, row_data in df.head().iterrows():
#     if row_id % 10000 == 0:
#         print(f'on row {row_id}')
#     write_row(dict(row_data), table_name, dynamodb)

with open('../yellow_tripdata_2018-12.csv.part', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    count = 0
    for row in reader:
        write_row(row, table_name, dynamodb_client)
        count += 1
        if count % 10 == 0:
            print(f'at row {count}')
            
        if count >= 50:
            break

# print(dynamodb_resource.get_available_subresources())