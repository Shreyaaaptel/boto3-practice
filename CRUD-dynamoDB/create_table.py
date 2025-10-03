import boto3

dynamodb_client = boto3.client('dynamodb')

table = dynamodb_client.create_table(
    TableName = 'StudentsIND',
    KeySchema = [{'AttributeName':'student_id', 'KeyType': 'HASH'}],
    AttributeDefinitions = [{'AttributeName':'student_id', 'AttributeType': 'S'}],
    ProvisionedThroughput = {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

dynamodb_client.get_waiter('table_exists').wait(TableName = 'StudentsIND')
print("Table created successfully!")