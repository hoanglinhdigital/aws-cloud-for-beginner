import json
import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal
import os
import redis
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

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert DynamoDB Decimal types to int/float"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)


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
        print(f"DEBUG: Socket Check to Redis FAILED - {str(e)}")

    # Check DynamoDB connectivity
    ddb_host = f"dynamodb.{os.environ.get('AWS_REGION', 'ap-southeast-1')}.amazonaws.com"
    print(f"DEBUG: Checking connectivity to DynamoDB at {ddb_host}:443")
    try:
        sock = socket.create_connection((ddb_host, 443), timeout=2)
        print("DEBUG: Socket Check - Successfully connected to DynamoDB port")
        sock.close()
    except Exception as e:
        print(f"DEBUG: Socket Check to DynamoDB FAILED - {str(e)}")

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

def get_from_cache(first_name, last_name, major):
    """
    Retrieve student data from Redis cache
    
    Args:
        first_name: First name to lookup
        last_name: Last name to lookup
        major: Major to lookup
    Returns:
        dict: Student data if found, None otherwise
    """
    try:
        cache = get_redis_client()
        cache_key = f"student:{first_name}:{last_name}:{major}"
        
        cached_data = cache.get(cache_key)
        
        if cached_data:
            print(f"Cache HIT for student_id: {cache_key}")
            return json.loads(cached_data)
        
        print(f"Cache MISS for student_id: {cache_key}")
        return None
        
    except Exception as e:
        print(f"Redis error (will fallback to DynamoDB): {str(e)}")
        return None
def set_in_cache(first_name, last_name, major, student_data):
    """
    Store student data in Redis cache with TTL
    
    Args:
        first_name: First name to lookup
        last_name: Last name to lookup
        major: Major to lookup
        student_data: Student data to cache
    """
    try:
        cache = get_redis_client()
        cache_key = f"student:{first_name}:{last_name}:{major}"
        
        # Serialize data and set with TTL
        cache.setex(
            cache_key,
            CACHE_TTL,
            json.dumps(student_data, cls=DecimalEncoder)
        )
        
        print(f"Cached student_id: {cache_key} with TTL: {CACHE_TTL}s")
        
    except Exception as e:
        print(f"Failed to cache data (non-critical): {str(e)}")       

def search_student_from_dynamodb(first_name, last_name, major):
    """
    Search for students in DynamoDB
    
    Args:
        first_name: First name to search
        last_name: Last name to search
        major: Major to search
    Returns:
        list: List of student data
    """
    try:
        table = dynamodb.Table(TABLE_NAME)
        
        # Build query expression
        filter_expression = None
        if first_name:
            filter_expression = Attr("first_name").eq(first_name)

        if last_name:
            expr = Attr("last_name").eq(last_name)
            filter_expression = expr if filter_expression is None else filter_expression & expr

        if major:
            expr = Attr("major").eq(major)
            filter_expression = expr if filter_expression is None else filter_expression & expr

        # Perform scan
        if filter_expression:
            response = table.scan(FilterExpression=filter_expression)
        else:
            response = table.scan()  # No filters provided

        return response.get("Items", [])
        
    except Exception as e:
        print(f"DynamoDB error: {str(e)}")
        return []   

def lambda_handler(event, context):
    """
    Enhanced search students function with optional features:
    - Case-insensitive search (add ?case_sensitive=false)
    - Partial matching (add ?partial_match=true)
    - Pagination support (add ?limit=20)
    
    Query Parameters:
    - first_name or first-name: First name to search
    - last_name or last-name: Last name to search
    - major: Major to search
    - case_sensitive: true/false (default: true)
    - partial_match: true/false (default: false)
    - limit: Number of results to return (default: all)
    """
    try:
        # Run diagnostics first
        debug_connection()

        # Extract query parameters
        query_params = event.get('queryStringParameters') or {}
        
        # Get search parameters
        first_name = query_params.get('first_name')
        last_name = query_params.get('last_name')
        major = query_params.get('major')
        
        # Get options
        case_sensitive = query_params.get('case_sensitive', 'true').lower() == 'true'
        partial_match = query_params.get('partial_match', 'false').lower() == 'true'
        limit = int(query_params.get('limit', 0))
        
        # Check if at least one search parameter is provided
        if not any([first_name, last_name, major]):
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'At least one search parameter is required',
                    'accepted_parameters': ['first_name', 'last_name', 'major'],
                    'options': ['case_sensitive', 'partial_match', 'limit']
                })
            }
        
        print(f"Search params: first_name={first_name}, last_name={last_name}, major={major}")
        print(f"Options: case_sensitive={case_sensitive}, partial_match={partial_match}, limit={limit}")

        # Check Redis Cache
        try:
            cached_result = get_from_cache(first_name, last_name, major)
            
            if cached_result:
                print(f"Cache HIT for key: {first_name}:{last_name}:{major}")
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps(cached_result)
                }
            print(f"Cache MISS for key: {first_name}:{last_name}:{major}")
        except Exception as e:
            print(f"Redis cache error (continuing to DB): {str(e)}")
        
        # Get DynamoDB table
        print("DEBUG: Starting DynamoDB search...")
        student_data = search_student_from_dynamodb(first_name, last_name, major)
        print(f"DEBUG: Finished DynamoDB search. Found {len(student_data)} records.")
        
        # Serialize result
        json_body = json.dumps(student_data, cls=DecimalEncoder)
        
        # Save to Redis Cache
        try:
            print("DEBUG: Starting Redis write...")
            cache = get_redis_client()
            cache_key = f"search:student:{first_name}:{last_name}:{major}:{case_sensitive}:{partial_match}:{limit}"
            cache.setex(cache_key, CACHE_TTL, json_body)
            print(f"Saved result to cache key: {cache_key}")
            print("DEBUG: Finished Redis write")
        except Exception as e:
            print(f"Error saving to cache: {str(e)}")

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json_body
        }
        
    except Exception as e:
        print(f"Error searching students: {str(e)}")
        import traceback
        traceback.print_exc()
        
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