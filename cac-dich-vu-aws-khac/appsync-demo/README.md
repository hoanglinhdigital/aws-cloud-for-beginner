# Step by step to create AppSync using AWS Console

## Step 1: Create AppSync API using AWS Console
Go to AWS AppSync Console
    Click "Create API"
    Choose "Build from scratch"
    API name: `StudentsAPI`
    Click "Create"

## Step 2: Configure Schema
    In the AppSync console, go to Schema
    Paste the GraphQL schema in `schema.graphql` file.
    Click Save Schema

## Step 3: Create Data Source
    Go to Data Sources in the left menu
    Click Create data source
    Configure:
        Data source name: `StudentsTable`
        Data source type: `Amazon DynamoDB table`
        Region: `Your region`
        Table name: `students`
        Create or use an existing role: Create new role (AppSync will create it automatically)
    Click Create

## Step 4: Create Functions (VTL)
*See function-list.md


## Step3: Configure API Setting
1. Go to **Settings** in AppSync
2. Note your **API URL** and **API Key** (if using API Key authentication)
3. Under **Authorization mode**, add **API Key** for testing

## Step 4: Confiugre Postman Collection (optional)
*See postman.md

## Test with AppSync Console
You can also test directly in the AppSync console:

Go to Queries in the left menu
Use the GraphQL explorer to test queries
### Example query (get student by ID):
```
query MyQuery {
  getStudent(student_id: "STU001") {
    student_id
    first_name
    last_name
    email
    age
    major
    enrollment_date
    created_at
  }
}
```
### Get all and limit:
```
query ListStudents {
  listStudents(limit: 10) {
    items {
      student_id
      first_name
      last_name
      email
      age
      major
      enrollment_date
      created_at
    }
    nextToken
  }
}
```
### Get all student, limit 10:  
```
query ListStudents {
  listStudents(limit: 10) {
    items {
      student_id
      first_name
      last_name
      email
      age
      major
      enrollment_date
      created_at
    }
    nextToken
  }
}
```
### Get student by major (scan):  
```
query GetStudentsByMajor {
  getStudentsByMajor(major: "Computer Science", limit: 10) {
    items {
      student_id
      first_name
      last_name
      email
      age
      major
      enrollment_date
      created_at
    }
    nextToken
  }
}
```

### Create student
```
mutation CreateStudent {
  createStudent(input: {
    student_id: "STU007"
    first_name: "Linh"
    last_name: "Deptrai"
    email: "linhdeptrai@gmail.com"
    age: 33
    major: "SoftwareEngineering"
    enrollment_date: "2024-12-05"
  }) {
    student_id
    first_name
    last_name
    email
    age
    major
    enrollment_date
    created_at
  }
}
```