import json
import boto3
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'students')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def get_student_by_id(student_id):
    print(f"Getting student by ID: {student_id}")
    table = dynamodb.Table(TABLE_NAME)
    
    try:
        response = table.get_item(Key={'student_id': student_id})
        item = response.get('Item')
        
        if item:
            return {
                'statusCode': 200,
                'body': json.dumps(item, cls=DecimalEncoder),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': f'Student with ID {student_id} not found'}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
    except Exception as e:
        print(f"Error fetching student: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Internal Server Error: {str(e)}'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

def lambda_handler(event, context):
    """
    Handle API Gateway requests to get student by ID
    URL: <api-gateway-domain>/dev/student/<student-id>
    """
    print(f"Received event: {json.dumps(event)}")
    
    # Check for API Gateway event with pathParameters
    path_params = event.get('pathParameters')
    if path_params:
        # Check for 'student-id' (from URL pattern) or 'student_id'
        student_id = path_params.get('student-id') or path_params.get('student_id')
        if student_id:
            return get_student_by_id(student_id)
    
    return {
        'statusCode': 400,
        'body': json.dumps({'message': 'Missing student_id path parameter'}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
