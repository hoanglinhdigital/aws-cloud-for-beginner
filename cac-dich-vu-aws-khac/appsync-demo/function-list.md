### Get Student by ID (getStudent)  
Request Mapping Template:  
```
{
    "version": "2017-02-28",
    "operation": "GetItem",
    "key": {
        "student_id": $util.dynamodb.toDynamoDBJson($ctx.args.student_id)
    }
}

```
Response Mapping Template:
```
$util.toJson($ctx.result)
```

### List All Students (listStudents) with Limit
Request Mapping Template:  
```
    {
        "version": "2017-02-28",
        "operation": "Scan",
        #if($ctx.args.limit)
            "limit": $ctx.args.limit,
        #end
        #if($ctx.args.nextToken)
            "nextToken": "$ctx.args.nextToken"
        #end
    }
```
Response Mapping Template:  
```
    {
        "items": $util.toJson($ctx.result.items),
        #if($ctx.result.nextToken)
            "nextToken": "$ctx.result.nextToken"
        #end
    }
```

### Get Student by Major (scan)
Request mapping template:
```
{
    "version": "2017-02-28",
    "operation": "Scan",
    "filter": {
        "expression": "#major = :major",
        "expressionNames": {
            "#major": "major"
        },
        "expressionValues": {
            ":major": $util.dynamodb.toDynamoDBJson($ctx.args.major)
        }
    },
    #if($ctx.args.limit)
        "limit": $ctx.args.limit,
    #end
    #if($ctx.args.nextToken)
        "nextToken": "$ctx.args.nextToken"
    #end
}
```
Response mapping template:
```
{
    "items": $util.toJson($ctx.result.items),
    #if($ctx.result.nextToken)
        "nextToken": "$ctx.result.nextToken"
    #end
}
```
### Create Student (createStudent)
Request Mapping Template:  
```
{
    "version": "2017-02-28",
    "operation": "PutItem",
    "key": {
        "student_id": $util.dynamodb.toDynamoDBJson($ctx.args.input.student_id)
    },
    "attributeValues": {
        "first_name": $util.dynamodb.toDynamoDBJson($ctx.args.input.first_name),
        "last_name": $util.dynamodb.toDynamoDBJson($ctx.args.input.last_name),
        "email": $util.dynamodb.toDynamoDBJson($ctx.args.input.email),
        "age": $util.dynamodb.toDynamoDBJson($ctx.args.input.age),
        "major": $util.dynamodb.toDynamoDBJson($ctx.args.input.major),
        "enrollment_date": $util.dynamodb.toDynamoDBJson($ctx.args.input.enrollment_date),
        "created_at": $util.dynamodb.toDynamoDBJson($util.time.nowISO8601())
    }
}
```
Response Mapping Template:  
```
$util.toJson($ctx.result)
```

### Update Student (updateStudent)
Request Mapping Template:  
```
{
    "version": "2017-02-28",
    "operation": "UpdateItem",
    "key": {
        "student_id": $util.dynamodb.toDynamoDBJson($ctx.args.input.student_id)
    },
    "update": {
        "expression": "SET",
        "expressionNames": {},
        "expressionValues": {}
    }
}

#set($update = "")
#set($count = 0)

#if($ctx.args.input.first_name)
    #set($update = "$update #first_name = :first_name")
    $util.qr($ctx.stash.update.expressionNames.put("#first_name", "first_name"))
    $util.qr($ctx.stash.update.expressionValues.put(":first_name", $util.dynamodb.toDynamoDB($ctx.args.input.first_name)))
    #set($count = $count + 1)
#end

#if($ctx.args.input.last_name)
    #if($count > 0)#set($update = "$update,")#end
    #set($update = "$update #last_name = :last_name")
    $util.qr($ctx.stash.update.expressionNames.put("#last_name", "last_name"))
    $util.qr($ctx.stash.update.expressionValues.put(":last_name", $util.dynamodb.toDynamoDB($ctx.args.input.last_name)))
    #set($count = $count + 1)
#end

#if($ctx.args.input.email)
    #if($count > 0)#set($update = "$update,")#end
    #set($update = "$update #email = :email")
    $util.qr($ctx.stash.update.expressionNames.put("#email", "email"))
    $util.qr($ctx.stash.update.expressionValues.put(":email", $util.dynamodb.toDynamoDB($ctx.args.input.email)))
    #set($count = $count + 1)
#end

#if($ctx.args.input.age)
    #if($count > 0)#set($update = "$update,")#end
    #set($update = "$update #age = :age")
    $util.qr($ctx.stash.update.expressionNames.put("#age", "age"))
    $util.qr($ctx.stash.update.expressionValues.put(":age", $util.dynamodb.toDynamoDB($ctx.args.input.age)))
    #set($count = $count + 1)
#end

#if($ctx.args.input.major)
    #if($count > 0)#set($update = "$update,")#end
    #set($update = "$update #major = :major")
    $util.qr($ctx.stash.update.expressionNames.put("#major", "major"))
    $util.qr($ctx.stash.update.expressionValues.put(":major", $util.dynamodb.toDynamoDB($ctx.args.input.major)))
    #set($count = $count + 1)
#end

#if($ctx.args.input.enrollment_date)
    #if($count > 0)#set($update = "$update,")#end
    #set($update = "$update #enrollment_date = :enrollment_date")
    $util.qr($ctx.stash.update.expressionNames.put("#enrollment_date", "enrollment_date"))
    $util.qr($ctx.stash.update.expressionValues.put(":enrollment_date", $util.dynamodb.toDynamoDB($ctx.args.input.enrollment_date)))
#end

$util.toJson($ctx.stash)
```
Response Mapping Template:  
```
$util.toJson($ctx.result)
```
### Delete Student (deleteStudent)
Request Mapping Template:  
```
{
    "version": "2017-02-28",
    "operation": "DeleteItem",
    "key": {
        "student_id": $util.dynamodb.toDynamoDBJson($ctx.args.student_id)
    }
}
```
Response Mapping Template:  
```
$util.toJson($ctx.result)
```
