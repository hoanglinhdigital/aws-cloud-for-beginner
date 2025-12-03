import json
import csv
import boto3
from datetime import datetime
from io import StringIO
import os

dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')

# Get table name from environment variable
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'students')

def lambda_handler(event, context):
    """
    Process CSV file from S3 and load data into DynamoDB
    """
    try:
        # Extract bucket and key from event
        bucket = event['bucket']
        key = event['key']
        
        print(f"Processing file: s3://{bucket}/{key}")
        
        # Download CSV file from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        csv_content = response['Body'].read().decode('utf-8')
        
        # Parse CSV
        csv_file = StringIO(csv_content)
        csv_reader = csv.DictReader(csv_file)
        
        # Get DynamoDB table
        table = dynamodb.Table(TABLE_NAME)
        
        # Process records
        success_count = 0
        failed_records = []
        
        with table.batch_writer() as batch:
            for row in csv_reader:
                try:
                    # Validate required fields
                    if not row.get('student_id'):
                        failed_records.append({
                            'row': row,
                            'error': 'Missing student_id'
                        })
                        continue
                    
                    # Transform data
                    item = {
                        'student_id': row['student_id'],
                        'first_name': row.get('first_name', ''),
                        'last_name': row.get('last_name', ''),
                        'email': row.get('email', ''),
                        'age': int(row['age']) if row.get('age') else 0,
                        'major': row.get('major', ''),
                        'enrollment_date': row.get('enrollment_date', ''),
                        'created_at': datetime.utcnow().isoformat()
                    }
                    
                    # Write to DynamoDB
                    batch.put_item(Item=item)
                    success_count += 1
                    
                except Exception as e:
                    failed_records.append({
                        'row': row,
                        'error': str(e)
                    })
        
        # Prepare response
        result = {
            'statusCode': 200,
            'message': 'Processing completed',
            'bucket': bucket,
            'key': key,
            'total_records': success_count + len(failed_records),
            'success_count': success_count,
            'failed_count': len(failed_records),
            'failed_records': failed_records[:10]  # Limit to first 10 failures
        }
        
        # If there are failures, mark as partial success
        if failed_records:
            result['statusCode'] = 207  # Multi-Status
            result['message'] = 'Processing completed with errors'
        
        print(f"Processing complete: {success_count} records loaded successfully")
        
        return result
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return {
            'statusCode': 500,
            'message': f'Error processing file: {str(e)}',
            'bucket': event.get('bucket', 'unknown'),
            'key': event.get('key', 'unknown')
        }