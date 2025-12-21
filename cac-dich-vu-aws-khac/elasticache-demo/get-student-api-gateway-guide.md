# API Gateway Setup Guide - Get Student by ID

## Prerequisites
1. Lambda function code: get_student_by_id.py
2. DynamoDB table 'students' created
3. Appropriate IAM role for Lambda with DynamoDB read permissions

## Part 1: Create Lambda Function

### Step 1: Create Lambda Function
1. Create lambda function named: `GetStudentById`
   - Runtime: Python 3.12 (or latest Python 3.x)
   - Architecture: x86_64
   - Permissions: Select "Create a new role with basic Lambda permissions" OR
   - Replace the default code with the content from `get_student_by_id.py` then deploy

### Step 2: Configure Environment Variables

1. Add environment variable for DynamoDB
   - **Key**: `DYNAMODB_TABLE`
   - **Value**: `students`
2. Add environment variable for Redis
   - **Key**: `REDIS_HOST`
   - **Value**: YOUR_REDIS_URL
   - **Key**: `REDIS_PORT`
   - **Value**: 6379

### Step 3: Add DynamoDB Permissions to Lambda Role
Add `AmazonDynamoDBReadOnlyAccess` to Lambda role.
Add `AWSLambdaVPCAccessExecutionRole` to Lambda role.

### Step 4: Modify lambda to run inside VPC:
1. Go to **"Configuration"** tab
2. Click **"VPC"** in the left menu
3. Click **Edit**
4. Select your VPC and Subnets
5. Click **Save**


### Step 6: Test Lambda Function
1. In Lambda console, go to **"Test"** tab
2. Click **"Create new event"**
3. **Event name**: `TestGetStudent`
4. Use this test event:
   ```json
   {
       "pathParameters": {
           "id": "STU001"
       }
   }
   ```
5. Click **"Test"**
6. Verify the response shows student data with statusCode 200

---

## Part 2: Create API Gateway

### Step 1: Create REST API
1. Go to API Gateway Console
2. Click **"Create API"**
3. Under **"REST API"** (not REST API Private), click **"Build"**
4. Configure:
   - **Choose the protocol**: REST
   - **Create new API**: New API
   - **API name**: `StudentAPI`
   - **Description**: API for student management
   - **Endpoint Type**: Regional (or Edge optimized)
5. Click **"Create API"**

### Step 2: Create Resource
1. In the API Gateway console, click **"Create Resource"** (or Actions > Create Resource)
2. Configure:
   - **Resource Name**: `student`
   - **Resource Path**: `/student`
   - **Enable API Gateway CORS**: ✓ (check this box)
3. Click **"Create Resource"**

### Step 3: Create Path Parameter Resource
1. Select the `/student` resource you just created
2. Click **"Create Resource"** again
3. Configure:
   - **Resource Name**: `id`
   - **Resource Path**: `/{id}` (curly braces indicate path parameter)
   - **Enable API Gateway CORS**: ✓ (check this box)
4. Click **"Create Resource"**

### Step 4: Create GET Method
1. Select the `/{id}` resource
2. Click **"Create Method"** (or Actions > Create Method)
3. Select **"GET"** from the dropdown
4. Click the checkmark ✓

### Step 5: Configure GET Method Integration
1. In the method setup page, configure:
   - **Integration type**: Lambda Function
   - **Use Lambda Proxy integration**: ✓ (CHECK THIS - IMPORTANT!)
   - **Lambda Region**: Select your Lambda region (e.g., us-east-1)
   - **Lambda Function**: Type `GetStudentById` (it should auto-complete)
2. Click **"Save"**
3. A popup will appear asking for permission to invoke Lambda
4. Click **"OK"** to grant API Gateway permission to invoke the Lambda function

### Step 6: Enable CORS (if not done automatically)
1. Select the `/{id}` resource
2. Click **"Enable CORS"** (or Actions > Enable CORS)
3. Keep default settings:
   - **Access-Control-Allow-Methods**: Check GET, OPTIONS
   - **Access-Control-Allow-Headers**: Default headers
   - **Access-Control-Allow-Origin**: '*'
4. Click **"Enable CORS and replace existing CORS headers"**
5. Click **"Yes, replace existing values"**

### Step 7: Deploy API
1. Click **"Deploy API"** (or Actions > Deploy API)
2. Configure:
   - **Deployment stage**: [New Stage]
   - **Stage name**: `dev` (or `prod`, `test`, etc.)
   - **Stage description**: Development environment
   - **Deployment description**: Initial deployment
3. Click **"Deploy"**

### Step 8: Get API Endpoint URL
API URL Example:   `https://{api-id}.execute-api.{region}.amazonaws.com/dev/student/{id}`

## Part 3: Test the API

### Test with curl
```bash
# Replace with your actual API Gateway URL and student ID
curl https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/student/STU001
```

### Test with browser
Simply paste the URL in your browser:
```
https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/student/STU001
```

### Test with Postman
1. Create new GET request
2. URL: `https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/student/STU001`
3. Click **"Send"**

### Expected Responses

**Success (200):**
```json
{
    "student": {
        "student_id": "STU001",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@email.com",
        "age": 20,
        "major": "Computer Science",
        "enrollment_date": "2024-09-01",
        "created_at": "2024-12-17T10:30:00.123456"
    }
}
```
