import json

def lambda_handler(event, context):
    
    # for debug
    print('DEBUG INPUT FROM CLIENT:')
    print(event)
    
    headers = event['headers']
    body = json.loads(event['body'])
    
    print('DEBUG HEADER FROM CLIENT:')
    print(headers)
    
        
    print('DEBUG BODY FROM CLIENT:')
    print(body)
    
    firstNum = body['firstNum']
    secondNum = body['secondNum']
    operator = body['operator'] # ADD, MULTIPLE, DEVIDE, SUBSTRACT
    # Process the request
    result = calculate(firstNum, secondNum, operator)
    
    # Create the response body
    response_body = {
        'message': 'Request processed successfully',
        'result': result
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

def calculate(num1, num2, operator):
    if operator == 'ADD':
        return num1 + num2
    elif operator == 'SUBSTRACT':
        return num1 - num2
    elif operator == 'MULTIPLE':
        return num1 * num2
    elif operator == 'DEVIDE':
        return num1 / num2
    else:
        return 0
