
### Setup Postman Environment

Create environment variables:
- `APPSYNC_URL`: Your AppSync GraphQL endpoint (e.g., `https://xxxxx.appsync-api.us-east-1.amazonaws.com/graphql`)
- `API_KEY`: Your AppSync API Key

### 1. Get Student by ID
```
POST {{APPSYNC_URL}}
Headers:
    Content-Type: application/json
    x-api-key: {{API_KEY}}

Body (raw JSON):
{
    "query": "query GetStudent($student_id: String!) { getStudent(student_id: $student_id) { student_id first_name last_name email age major enrollment_date created_at } }",
    "variables": {
        "student_id": "STU001"
    }
}
```

### 2. List All Students
```
POST {{APPSYNC_URL}}
Headers:
    Content-Type: application/json
    x-api-key: {{API_KEY}}

Body (raw JSON):
{
    "query": "query ListStudents($limit: Int) { listStudents(limit: $limit) { items { student_id first_name last_name email age major enrollment_date created_at } nextToken } }",
    "variables": {
        "limit": 10
    }
}
```

### 3. Create Student
```
POST {{APPSYNC_URL}}
Headers:
    Content-Type: application/json
    x-api-key: {{API_KEY}}

Body (raw JSON):
{
    "query": "mutation CreateStudent($input: CreateStudentInput!) { createStudent(input: $input) { student_id first_name last_name email age major enrollment_date created_at } }",
    "variables": {
        "input": {
            "student_id": "STU001",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "age": 20,
            "major": "Computer Science",
            "enrollment_date": "2024-01-15"
        }
    }
}
```

### 4. Update Student
```
POST {{APPSYNC_URL}}
Headers:
    Content-Type: application/json
    x-api-key: {{API_KEY}}

Body (raw JSON):
{
    "query": "mutation UpdateStudent($input: UpdateStudentInput!) { updateStudent(input: $input) { student_id first_name last_name email age major enrollment_date created_at } }",
    "variables": {
        "input": {
            "student_id": "STU001",
            "age": 21,
            "email": "john.updated@example.com"
        }
    }
}
```

### 5. Delete Student
```
POST {{APPSYNC_URL}}
Headers:
    Content-Type: application/json
    x-api-key: {{API_KEY}}

Body (raw JSON):
{
    "query": "mutation DeleteStudent($student_id: String!) { deleteStudent(student_id: $student_id) { student_id first_name last_name } }",
    "variables": {
        "student_id": "STU001"
    }
}
```