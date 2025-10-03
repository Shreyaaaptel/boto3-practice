import json
import boto3
from boto3.dynamodb.conditions import Attr

dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table('StudentsIND')

def lambda_handler(event, context):

    action = event['action']


    # create a new item in table
    if action == 'create':
        item = { key: value for key, value in event.items() if key != 'action'}

        if 'student_id' not in item:
            return {'message': 'student_id is missing'}
        
        try:
            table.put_item(Item = item, ConditionExpression=Attr('student_id').not_exists())
            return {'message': f'item created {item}'}
        except Exception as e:
            return {'message': f'item already exists {item}'}
    

    # read an item from table
    elif action == 'read':
        student_id = event['student_id']
        response = table.get_item(Key = {'student_id': student_id})

        if 'Item' in response:
            return {'message': response['Item']}
        return {'message': 'item not found'}


    #update an item in table
    elif action == 'update':
        student_id = event['student_id']
        
        attribute_updates = {
            k: {'Value': v, 'Action': 'PUT'} for k, v in event.items() if k not in ['action', 'student_id']
        }
        
        if not attribute_updates:
            return {'message': 'No fields to update'}

        # If the student_id doesn't exist in table, a new item would be created (default)
        response = table.get_item(Key={'student_id': student_id})
        table.update_item(Key={'student_id': student_id}, AttributeUpdates=attribute_updates)        
        return {
            'message': f'item updated: {student_id}'
        }


    # delete an item from table
    elif action == 'delete':
        student_id = event['student_id']
        response = table.delete_item(Key = {'student_id': student_id}, ReturnValues='ALL_OLD')

        if 'Attributes' not in response:
            return {'message': 'item not found'}
        return {'message': f'item deleted {student_id}'}


    else: 
        return {'message': 'invalid action'}
    


