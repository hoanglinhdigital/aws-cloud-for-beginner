import json

def lambda_handler(event, context):
    
    # for debug
    print('DEBUG INPUT FROM SNS:')
    print(event)

    # Create the response body
    response_body = {
        'message': 'Request processed successfully'
    }
    
    # Create the HTTP response
    response = {
        'statusCode': 200,
        'body': json.dumps(response_body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
    
    return response
