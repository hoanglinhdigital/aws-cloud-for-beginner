import json
import boto3
import redis
from datetime import datetime
from decimal import Decimal
import os
import socket

dynamodb = boto3.resource(
    'dynamodb'
    # Add below line if you using VPC endpoint type Interface
    # endpoint_url='https://vpce-0482017ff00e50ef4.dynamodb.ap-southeast-1.vpce.amazonaws.com'
)

# Get configuration from environment variables
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'students')
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
CACHE_TTL = 300  # 5 minutes in seconds
# Initialize Redis connection (reused across Lambda invocations)
redis_client = None

def debug_connection():
    """Diagnostic function to check network connectivity"""
    print(f"DEBUG: Checking connectivity to Redis at {REDIS_HOST}:{REDIS_PORT}")
    try:
        ip_address = socket.gethostbyname(REDIS_HOST)
        print(f"DEBUG: DNS Check - Resolved {REDIS_HOST} to {ip_address}")
    except Exception as e:
        print(f"DEBUG: DNS Check FAILED - {str(e)}")
        return

    try:
        sock = socket.create_connection((REDIS_HOST, REDIS_PORT), timeout=2)
        print("DEBUG: Socket Check - Successfully connected to Redis port")
        sock.close()
    except Exception as e:
        print(f"DEBUG: Socket Check FAILED - {str(e)}")

def get_redis_client():
    """Get or create Redis client (connection pooling)"""
    global redis_client
    if redis_client is None:
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=0,
            decode_responses=True,
            socket_connect_timeout=3,
            socket_timeout=3,
            ssl=True
        )
    return redis_client

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert DynamoDB Decimal types to int/float"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def get_from_cache(student_id):
    """
    Retrieve student data from Redis cache
    
    Args:
        student_id: Student ID to lookup
        
    Returns:
        dict: Student data if found, None otherwise
    """
    try:
        cache = get_redis_client()
        cache_key = f"student:{student_id}"
        
        cached_data = cache.get(cache_key)
        
        if cached_data:
            print(f"Cache HIT for student_id: {student_id}")
            return json.loads(cached_data)
        
        print(f"Cache MISS for student_id: {student_id}")
        return None
        
    except Exception as e:
        print(f"Redis error (will fallback to DynamoDB): {str(e)}")
        return None

def set_in_cache(student_id, student_data):
    """
    Store student data in Redis cache with TTL
    
    Args:
        student_id: Student ID
        student_data: Student data to cache
    """
    try:
        cache = get_redis_client()
        cache_key = f"student:{student_id}"
        
        # Serialize data and set with TTL
        cache.setex(
            cache_key,
            CACHE_TTL,
            json.dumps(student_data, cls=DecimalEncoder)
        )
        
        print(f"Cached student_id: {student_id} with TTL: {CACHE_TTL}s")
        
    except Exception as e:
        print(f"Failed to cache data (non-critical): {str(e)}")

def get_from_dynamodb(student_id):
    """
    Retrieve student data from DynamoDB
    
    Args:
        student_id: Student ID to lookup
        
    Returns:
        dict: Student data if found, None otherwise
    """
    print(f"Cache miss, fetching from DynamoDB for student_id: {student_id}")
    table = dynamodb.Table(TABLE_NAME)
    
    response = table.get_item(
        Key={
            'student_id': student_id
        }
    )
    
    print(response)
    return response.get('Item')

def lambda_handler(event, context):
    """
    Get student by ID from cache or DynamoDB
    
    Flow:
    1. Check Redis cache
    2. If cache hit, return cached data
    3. If cache miss, get from DynamoDB
    4. Store in cache with 5-minute TTL
    5. Return data
    
    Expected API Gateway event structure:
    {
        "pathParameters": {
            "id": "STU001"
        }
    }
    """
    try:
        # Run diagnostics first
        debug_connection()

        # Extract student_id from path parameters
        student_id = event.get('pathParameters', {}).get('id')
        
        if not student_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Missing student_id in path parameters'
                })
            }
        
        print(f"Fetching student with ID: {student_id}")
        
        # Step 1: Try to get from cache
        student = get_from_cache(student_id)
        cache_hit = student is not None
        
        # Step 2: If cache miss, get from DynamoDB
        if not cache_hit:
            student = get_from_dynamodb(student_id)
            
            if not student:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'Student not found',
                        'student_id': student_id
                    })
                }
            
            # Step 3: Store in cache for future requests
            set_in_cache(student_id, student)
        
        # Return student data
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'X-Cache': 'HIT' if cache_hit else 'MISS'
            },
            'body': json.dumps({
                'student': student
            }, cls=DecimalEncoder)
        }
        
    except Exception as e:
        print(f"Error fetching student: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }