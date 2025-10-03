import json
import boto3
import csv
import io

def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    bucket_name = 'practice-s3-boto3' 
    object_key = 'demo.csv'

    try:
        response = s3_client.get_object(Bucket = bucket_name, Key = object_key)
        file_content = response['Body'].read().decode('utf-8')

        csv_reader = csv.reader(io.StringIO(file_content))
        for row in csv_reader:
            print(row)

        return {
            'statusCode': 200,
            'body': json.dumps(f'File read: {object_key}')
        }
    except Exception as e:
        print(f'Error occured while reading file: {e}')

        return{
            'statusCode': 500,
            'body': json.dumps('Couldn\'t read file')
        }