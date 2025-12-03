# This demonstration contain two small lambda function that reponsibility for:
## Lambda #1:  
- Load data from CSV file in S3 bucket that contain list of student.
- Transform it then save into DyamoDB table.
## Lambda #2:  
- Send a message to user via AWS SNS for the result.

## Flow to trigger:
S3 bucket -> 
EventBridge -> 
StepFunction ->
    Start
    Lambda -> DyamoDB Table
    Success -> SNS
    Failed -> SNS
    End

## Sample code inside /code folder.

## Steps:
### Step 1: create Dynamodb Table.
```
aws dynamodb create-table \
    --table-name students \
    --attribute-definitions \
        AttributeName=student_id,AttributeType=S \
    --key-schema \
        AttributeName=student_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
```
### Step 2: Create SNS topic
```
aws sns create-topic --name StudentProcessingNotifications
```
Subscribe your email (replace with your email)
```
aws sns subscribe \
    --topic-arn arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:StudentProcessingNotifications \
    --protocol email \
    --notification-endpoint your-email@example.com
```
*Or using AWS console

### Step 3: Create Lambda function with sample code.
Code file: `student-process.py`

### Step 4: Assign more permissino for Lambda
*Using `DynamoDBFullAccess` for demo purpose.

### Step 5: Creat step function with Definition file.
Definition file: `step_function_definition.json`

### Step 6: Add more policy for StepFunctions role.
Policy file: `stepfunction-role.json`

### Step 7: Create S3 Bucket
# Create bucket (use a unique name)
```
aws s3 mb s3://student-data-upload-bucket-YOUR_UNIQUE_ID
```


### Step 8: Configure EventBridge rule (for trigger from S3 -> StepFunctions)
Enable EventBridge notifications
```
aws s3api put-bucket-notification-configuration \
    --bucket student-data-upload-bucket-YOUR_UNIQUE_ID \
    --notification-configuration '{
      "EventBridgeConfiguration": {}
    }'
```

Modify file: `eventbridge-rule-pattern.json`
Create EventBridge rule
```
aws events put-rule \
    --name StudentCSVUploadRule \
    --event-pattern file://eventbridge-rule-pattern.json \
    --state ENABLED
```
Add Step Functions as target
```
aws events put-targets \
    --rule StudentCSVUploadRule \
    --targets "Id"="1","Arn"="arn:aws:states:us-east-1:YOUR_ACCOUNT_ID:stateMachine:StudentProcessingStateMachine","RoleArn"="arn:aws:iam::YOUR_ACCOUNT_ID:role/StudentStepFunctionsRole"
```

### Step 9: Test
Upload `students.csv` file to S3 bucket.
View StepFUnctions execution
View Lambda log on CloudWatch
View Students that been inserted into DynamoDB table.

## Cleanup
Delete S3 bucket.
Delete EventBridge
Delete StepFunctions workflow.
Delete Lambda function
Delete DynamoDB table.
Delete SNS Topic (optional)
Delete IAM role (optional)