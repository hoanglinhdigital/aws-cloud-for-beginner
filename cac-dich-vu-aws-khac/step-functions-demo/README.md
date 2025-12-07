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
    Failed  -> SNS
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
    --billing-mode PAY_PER_REQUEST
```
### Step 2: Create SNS topic
```
aws sns create-topic --name udemy-demo-stepfunctions-topic
```

Using below command to subscribe your email (replace with your email and Topic ARN)
*Or using AWS console
```
aws sns subscribe \
    --topic-arn arn:aws:sns:ap-southeast-1:586098608758:udemy-demo-stepfunctions-topic \
    --protocol email \
    --notification-endpoint hoanglinhdigital@gmail.com

```


### Step 3: Create Lambda function with sample code.
Function name: `student-processing-to-dynamo-db`
Code file: `student-process.py`

### Step 4: Assign more permission for Lambda
*Using `AmazonDynamoDBFullAccess` and `AmazonS3ReadOnlyAccess` for demo purpose.

### Step 5: Create step function with Definition file.
Name: `udemy-demo-student-process`
Definition file: `step_function_definition.json`
*Replace below Placeholder with your information:
    Line #9: `${ProcessStudentsLambdaArn}`
    Line #58, 71: `${SNSTopicArn}`

After import, check below component as your setting and make adjustment if needed:  
- Lambda Function setting
- SNS notification setting for Success and Fail case:
### Step 6: [Optional] Add more policy for StepFunctions role.
Policy file: `stepfunction-role.json`

### Step 7: Create S3 Bucket
*NOTE: Must be unique name and the same region with other resources.
Enable EventBridge Notifications on Your S3 Bucket
• 	Open the Amazon S3 console.
• 	Select your bucket → Properties tab.
• 	Scroll to Event Notifications → Amazon EventBridge.
• 	Turn Send notifications to Amazon EventBridge → On.
• 	Save changes.
⚠️ Note: It may take ~5 minutes for this setting to propagate.

### Step 8: Configure EventBridge rule (for trigger from S3 -> StepFunctions)
Go to EventBridge and create an event to catch s3 Object Created the trigger StepFunctions.
Detail event paternn (replace with your bucket name)
```
{
  "source": ["aws.s3"],
  "detail-type": ["Object Created"],
  "detail": {
    "bucket": {
      "name": ["udemy-demo-students-linh"]
    },
    "object": {
      "key": [{
        "suffix": ".csv"
      }]
    }
  }
}
```
Add Needed Permission for EventBridge's IAM Role (Allow it to trigger Stepfunctions)
    Permission name: `states:StartExecution`
    Resource: `*`

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