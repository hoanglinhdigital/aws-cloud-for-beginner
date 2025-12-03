Dưới đây là hướng dẫn **step-by-step đơn giản** để Linh có thể demo dịch vụ **AWS AppSync** bằng **AWS Console** và **Postman**, sử dụng một API GraphQL kết nối với DynamoDB.

---

## 🛠️ Bước 1: Tạo bảng DynamoDB

1. Vào [AWS Console → DynamoDB](https://console.aws.amazon.com/dynamodb).
2. Chọn **Create table**.
3. Đặt tên bảng: `TodoTable`.
4. Primary key: `id` (kiểu String).
5. Giữ các thiết lập mặc định và nhấn **Create table**.

---

## 🧩 Bước 2: Tạo AppSync API

1. Vào [AWS Console → AppSync](https://console.aws.amazon.com/appsync).
2. Chọn **Create API** → **Build from scratch**.
3. Đặt tên: `TodoAPI`.
4. Chọn **Create**.

---

## 🧬 Bước 3: Định nghĩa schema GraphQL

1. Trong tab **Schema**, dán đoạn sau:

```graphql
type Todo {
  id: ID!
  title: String!
  done: Boolean!
}

type Query {
  getTodos: [Todo]
}

type Mutation {
  addTodo(id: ID!, title: String!, done: Boolean!): Todo
}
```

2. Nhấn **Save Schema**.

---

## 🔗 Bước 4: Kết nối với DynamoDB

1. Vào tab **Data Sources** → **Create data source**.
2. Chọn **Amazon DynamoDB table** → chọn `TodoTable`.
3. Đặt tên: `TodoTableDS` → **Create**.

---

## 🧠 Bước 5: Tạo resolvers

1. Vào tab **Resolvers** → chọn `Query.getTodos`.
2. Gắn với `TodoTableDS` → chọn **Invoke DynamoDB Scan** → **Save Resolver**.

3. Tiếp tục với `Mutation.addTodo`:
   - Gắn với `TodoTableDS`.
   - Chọn **PutItem**.
   - Mapping template:

```vtl
{
  "version": "2018-05-29",
  "operation": "PutItem",
  "key": {
    "id": $util.dynamodb.toDynamoDBJson($ctx.args.id)
  },
  "attributeValues": {
    "title": $util.dynamodb.toDynamoDBJson($ctx.args.title),
    "done": $util.dynamodb.toDynamoDBJson($ctx.args.done)
  }
}
```

→ **Save Resolver**.

---

## 🔐 Bước 6: Lấy endpoint và API key

1. Vào tab **Settings** → copy **GraphQL endpoint**.
2. Vào tab **Authorization** → chọn **API key** → copy key.

---

## 📬 Bước 7: Gửi request bằng Postman

1. Mở Postman → tạo request mới:
   - Method: `POST`
   - URL: Dán GraphQL endpoint.
   - Headers:
     - `x-api-key`: Dán API key.
     - `Content-Type`: `application/json`
   - Body → chọn **raw → JSON**:

```json
{
  "query": "mutation { addTodo(id: \"1\", title: \"Learn AppSync\", done: false) { id title done } }"
}
```

→ Nhấn **Send** để thêm dữ liệu.

2. Gửi query để lấy danh sách:

```json
{
  "query": "query { getTodos { id title done } }"
}
```

→ Nhấn **Send** để xem kết quả.

---

