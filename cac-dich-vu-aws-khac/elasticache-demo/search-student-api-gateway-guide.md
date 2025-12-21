# API Gateway Setup Guide - Search Students

## Prerequisites
1. DynamoDB table 'students' created with data
2. Appropriate IAM role for Lambda with DynamoDB scan permissions

## Part 1: Create Lambda Function

### Step 1: Create Lambda Function
1. Go to AWS Lambda Console
2. Click **"Create function"**
3. Select **"Author from scratch"**
4. Configure:
   - **Function name**: `SearchStudents`
   - **Runtime**: Python 3.12 (or latest Python 3.x)
   - **Architecture**: x86_64
   - **Permissions**: 
     - Select "Create a new role with basic Lambda permissions" OR
     - Use existing role with DynamoDB permissions
5. Click **"Create function"**

### Step 2: Add Lambda Code
1. In the Lambda function page, scroll to **"Code source"**
2. Upload `search-student.zip`. *If you modify any code, create Zip file again.
3. Click **"Deploy"** to save changes

### Step 3: Configure Environment Variables
1. Click **"Add environment variable"**
   - **Key**: `DYNAMODB_TABLE`
   - **Value**: `students`
2. Add environment variable for Redis
   - **Key**: `REDIS_HOST`
   - **Value**: YOUR_REDIS_URL
   - **Key**: `REDIS_PORT`
   - **Value**: 6379

### Step 4: Add DynamoDB Permissions to Lambda Role
Add `AmazonDynamoDBReadOnlyAccess` to Lambda role.
Add `AWSLambdaVPCAccessExecutionRole` to Lambda role.

### Step 5: Modify lambda to run inside VPC:
1. Go to **"Configuration"** tab
2. Click **"VPC"** in the left menu
3. Click **Edit**
4. Select your VPC and Subnets
5. Click **Save**

### Step 6: Test Lambda Function
1. In Lambda console, go to **"Test"** tab
2. Click **"Create new event"**
3. **Event name**: `TestSearchStudents`
4. Use this test event:
   ```json
   {
       "queryStringParameters": {
           "first_name": "James",
           "last_name": "Anderson"
       }
   }
   ```
5. Click **"Test"**
6. Verify the response shows matching students with statusCode 200

### Additional Test Cases
**Test with single parameter:**
```json
{
    "queryStringParameters": {
        "major": "Computer Science"
    }
}
```

**Test with all parameters:**
```json
{
    "queryStringParameters": {
        "first_name": "Sarah",
        "last_name": "Martinez",
        "major": "Business Administration"
    }
}
```

**Test with no parameters (should return error):**
```json
{
    "queryStringParameters": {}
}
```

---

## Part 2: Add Search Endpoint to API Gateway

### Option A: Using Existing API (if you already have StudentAPI)

#### Step 1: Navigate to Your API
1. Go to API Gateway Console (https://console.aws.amazon.com/apigateway/)
2. Select your existing **StudentAPI**
3. Find the `/student` resource

#### Step 2: Create Search Resource
1. Select the `/student` resource
2. Click **"Create Resource"**
3. Configure:
   - **Resource Name**: `search`
   - **Resource Path**: `/search`
   - **Enable API Gateway CORS**: ✓ (check this box)
4. Click **"Create Resource"**

Now you should have the path: `/student/search`

#### Step 3: Create GET Method for Search
1. Select the `/student/search` resource
2. Click **"Create Method"**
3. Select **"GET"** from the dropdown
4. Click the checkmark ✓

#### Step 4: Configure GET Method Integration
1. In the method setup page, configure:
   - **Integration type**: Lambda Function
   - **Use Lambda Proxy integration**: ✓ (CHECK THIS - IMPORTANT!)
   - **Lambda Region**: Select your Lambda region
   - **Lambda Function**: Type `SearchStudents`
2. Click **"Save"**
3. Click **"OK"** to grant API Gateway permission

#### Step 5: Configure Query String Parameters (Optional but Recommended)
1. With the GET method selected, click on **"Method Request"**
2. Expand **"URL Query String Parameters"**
3. Click **"Add query string"**
4. Add the following parameters (all optional):
   - `first_name` (or `first-name`)
   - `last_name` (or `last-name`)
   - `major`
5. For each parameter:
   - **Required**: No (leave unchecked)
   - **Caching**: No
6. Click the checkmark to save each parameter

#### Step 6: Enable CORS
1. Select the `/search` resource
2. Click **"Enable CORS"** (or Actions > Enable CORS)
3. Keep default settings:
   - **Access-Control-Allow-Methods**: GET, OPTIONS
   - **Access-Control-Allow-Headers**: Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token
   - **Access-Control-Allow-Origin**: '*'
4. Click **"Enable CORS and replace existing CORS headers"**
5. Click **"Yes, replace existing values"**

#### Step 7: Deploy API
1. Click **"Deploy API"** (or Actions > Deploy API)
2. Configure:
   - **Deployment stage**: Select existing stage (e.g., `dev`)
   - **Deployment description**: Added search endpoint
3. Click **"Deploy"**

#### Step 8: Get API Endpoint URL
Your search endpoint will be:
```
https://{api-id}.execute-api.{region}.amazonaws.com/dev/student/search
```

---
## Part 3: Test the Search API

### Test in Browser
Simply paste these URLs in your browser:

**Search by first name:**
```
https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/student/search?first_name=James
```

**Search by last name:**
```
https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/student/search?last_name=Anderson
```

**Search by major:**
```
https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/student/search?major=Computer%20Science
```

**Search by multiple parameters:**
```
https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/student/search?first_name=Sarah&last_name=Martinez&major=Business%20Administration
```

**Using hyphenated parameter names:**
```
https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/student/search?first-name=James&last-name=Anderson&major=Economics
```

### Test with curl

**Search by first name:**
```bash
curl "https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/student/search?first_name=James"
```

**Search by multiple parameters:**
```bash
curl "https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/student/search?first_name=Sarah&last_name=Martinez&major=Business%20Administration"
```

**With formatted output (using jq):**
```bash
curl -s "https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/student/search?major=Computer%20Science" | jq
```

### Test with Postman

1. Create new GET request
2. URL: `https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/student/search`
3. Go to **"Params"** tab
4. Add query parameters:
   - Key: `first_name`, Value: `James`
   - Key: `last_name`, Value: `Anderson`
   - Key: `major`, Value: `Economics`
5. Click **"Send"**

### Expected Responses

**Success with results (200):**
```json
{
    "count": 2,
    "search_criteria": {
        "first_name": "James",
        "last_name": null,
        "major": null
    },
    "students": [
        {
            "student_id": "STU001",
            "first_name": "James",
            "last_name": "Anderson",
            "email": "james.anderson@email.com",
            "age": 20,
            "major": "Computer Science",
            "enrollment_date": "2024-09-01",
            "created_at": "2024-12-17T10:30:00.123456"
        }
    ]
}
```

**Success with no results (200):**
```json
{
    "count": 0,
    "search_criteria": {
        "first_name": "NonExistent",
        "last_name": null,
        "major": null
    },
    "students": []
}
```

**Missing parameters (400):**
```json
{
    "error": "At least one search parameter is required",
    "accepted_parameters": [
        "first_name",
        "last_name",
        "major"
    ]
}
```

**Server error (500):**
```json
{
    "error": "Internal server error",
    "message": "Table students not found"
}
```

---

## Part 4: API Structure Overview

After setup, your API structure will be:

```
StudentAPI
├── /student
│   ├── /{id}           (GET - Get student by ID)
│   └── /search         (GET - Search students)
│       └── Query Parameters:
│           ├── first_name (optional)
│           ├── last_name (optional)
│           └── major (optional)
```

**Complete URL Examples:**
```
GET /student/STU001
    → Get specific student

GET /student/search?first_name=James
    → Search by first name

GET /student/search?major=Computer%20Science
    → Search by major

GET /student/search?first_name=Sarah&last_name=Martinez
    → Search by first and last name

GET /student/search?first_name=James&last_name=Anderson&major=Economics
    → Search by all parameters
```

---

## Part 5: Performance Considerations

### Important Notes on DynamoDB Scan

⚠️ **Warning**: This implementation uses DynamoDB `Scan` operation, which:
- Reads every item in the table
- Can be slow for large tables (millions of records)
- Consumes read capacity units
- Is acceptable for small-medium datasets (< 100K records)

### Optimization Strategies for Large Tables

**Option 1: Add Global Secondary Index (GSI)**
If you frequently search by major:
1. Create GSI with major as partition key
2. Use Query instead of Scan
3. Much faster and cheaper

**Option 2: Use DynamoDB Streams + Elasticsearch**
For complex search requirements:
1. Stream changes to Elasticsearch/OpenSearch
2. Perform full-text search on Elasticsearch
3. Best for complex queries

**Option 3: Implement Pagination**
For large result sets:
1. Add limit parameter
2. Return LastEvaluatedKey for next page
3. Prevents timeouts on large scans

**Sample Pagination Implementation:**
```python
# In lambda_handler, add:
limit = int(query_params.get('limit', 50))
last_key = query_params.get('last_key')

scan_kwargs = {
    'FilterExpression': filter_expression,
    'ExpressionAttributeNames': expression_attribute_names,
    'ExpressionAttributeValues': expression_attribute_values,
    'Limit': limit
}

if last_key:
    scan_kwargs['ExclusiveStartKey'] = json.loads(last_key)

response = table.scan(**scan_kwargs)

result = {
    'students': response['Items'],
    'count': len(response['Items'])
}

if 'LastEvaluatedKey' in response:
    result['last_key'] = json.dumps(response['LastEvaluatedKey'], cls=DecimalEncoder)
```

---

## Part 6: Monitoring and Troubleshooting

### Enable CloudWatch Logs

**For API Gateway:**
1. Go to API Gateway > Settings
2. Create CloudWatch log role if not exists
3. In your stage (e.g., `dev`):
   - Go to **Logs/Tracing** tab
   - Enable CloudWatch Logs
   - Set log level to **INFO**
   - Enable detailed metrics

**For Lambda:**
Logs are automatically sent to CloudWatch

### View Logs

**API Gateway Logs:**
```bash
aws logs tail /aws/apigateway/StudentAPI --follow
```

**Lambda Logs:**
```bash
aws logs tail /aws/lambda/SearchStudents --follow
```

### Common Issues

**Issue 1: No results returned when data exists**
- Check parameter names (underscore vs hyphen)
- Verify data is in DynamoDB (exact match required)
- Check CloudWatch logs for filter expression

**Issue 2: 400 Bad Request - Missing parameters**
- Ensure at least one parameter is provided
- Check parameter spelling

**Issue 3: Timeout (504)**
- Table is too large for scan operation
- Implement pagination or use GSI
- Increase Lambda timeout (Configuration > General > Timeout)

**Issue 4: High DynamoDB costs**
- Scan operations consume many RCUs
- Consider using On-Demand pricing
- Implement caching at API Gateway level
- Add GSI for frequently used filters

**Issue 5: CORS errors in browser**
- Ensure CORS is enabled on the resource
- Check Lambda returns CORS headers
- Redeploy API after CORS changes

---

## Part 7: Testing with Sample Data

### Load Sample Data First
Use the CSV file we created earlier with `student-process.py` to load data into DynamoDB.

### Test Queries

**1. Find all Computer Science students:**
```bash
curl "https://your-api.execute-api.us-east-1.amazonaws.com/dev/student/search?major=Computer%20Science"
```

**2. Find all students named James:**
```bash
curl "https://your-api.execute-api.us-east-1.amazonaws.com/dev/student/search?first_name=James"
```

**3. Find specific student by full name:**
```bash
curl "https://your-api.execute-api.us-east-1.amazonaws.com/dev/student/search?first_name=Sarah&last_name=Martinez"
```

**4. Complex search:**
```bash
curl "https://your-api.execute-api.us-east-1.amazonaws.com/dev/student/search?first_name=James&last_name=Anderson&major=Economics"
```

---

## Part 8: Security Best Practices

### Add Request Throttling
1. In API Gateway stage settings
2. Configure throttling:
   - **Rate**: 100 requests/second
   - **Burst**: 200 requests

### Add API Key (Optional)
1. API Gateway > API Keys > Create
2. Create Usage Plan
3. Associate with stage
4. Require API key in method request
5. Test with: `curl -H "x-api-key: YOUR_KEY" ...`

### Add Request Validation
1. In Method Request
2. Add request validator
3. Validate query parameters
4. Reject invalid requests early

### Enable AWS WAF (Optional)
1. Protect against SQL injection
2. Rate limiting per IP
3. Geographic restrictions
4. Bot protection

---

## Summary

Your search API endpoint is now ready:

```
GET https://{api-id}.execute-api.{region}.amazonaws.com/dev/student/search?first_name={name}&last_name={name}&major={major}
```

**Supported Query Parameters:**
- `first_name` or `first-name` (optional)
- `last_name` or `last-name` (optional)
- `major` (optional)

**Features:**
✅ Search by any combination of parameters
✅ Case-sensitive exact match
✅ Returns all matching results
✅ CORS enabled for browser access
✅ Proper error handling
✅ CloudWatch logging

**Remember:** At least one search parameter must be provided!