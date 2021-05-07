import boto3


def create_users_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',endpoint_url="http://dynamodb-local:8000",
                                    region_name="sa-east-1")

    table = dynamodb.create_table(
        TableName='Users',
        KeySchema=[
            {
                'AttributeName': 'userid',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'username',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'userid',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


if __name__ == '__main__':
    users_table = create_users_table()
    print("Table status:", users_table.table_status)