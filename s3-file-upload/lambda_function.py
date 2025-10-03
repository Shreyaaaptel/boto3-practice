import json
import boto3
import base64
import urllib.parse

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        print("Event:", json.dumps(event, indent=2))
        
        file_content = base64.b64decode(event['file'])
        file_name = urllib.parse.unquote(event['fileName'])
        bucket_name = 'practice-s3-boto3'

        # Upload file to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file_content
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'File {file_name} uploaded successfully to S3'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }