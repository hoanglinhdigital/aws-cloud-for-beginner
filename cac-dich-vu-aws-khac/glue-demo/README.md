Tuyệt vời Linh! Dưới đây là hướng dẫn từng bước để bạn làm quen với **AWS Glue** và sử dụng nó để thực hiện ETL dữ liệu từ file CSV trong S3 sang DynamoDB. Hướng dẫn này sử dụng **AWS Console**, không cần viết code thủ công.

---

## 🧭 Hướng dẫn từng bước: ETL từ S3 (CSV) sang DynamoDB bằng AWS Glue

### **Bước 1: Chuẩn bị dữ liệu và tài nguyên**

- ✅ **File CSV**: Đảm bảo file có header dòng đầu tiên, ví dụ:
  ```csv
  id,name,email
  1,Alice,alice@example.com
  2,Bob,bob@example.com
  ```
  Lưu vào S3, ví dụ: `s3://my-etl-bucket/users.csv`

- ✅ **DynamoDB Table**: Tạo bảng DynamoDB trước, ví dụ:
  - Tên bảng: `users`
  - Partition key: `id` (kiểu Number)

---

### **Bước 2: Tạo Glue Database**

1. Vào **AWS Glue Console** → **Databases** → **Add database**
2. Nhập tên: `etl_demo_db`

---

### **Bước 3: Tạo Glue Crawler để khám phá dữ liệu CSV**

1. Vào **Crawlers** → **Add crawler**
2. Đặt tên: `s3_csv_crawler`
3. Chọn nguồn dữ liệu:
   - Data store: S3
   - Path: `s3://my-etl-bucket/users.csv`
4. Chọn IAM role: `AWSGlueServiceRoleDefault` hoặc tạo role mới có quyền truy cập S3 và DynamoDB.
5. Output:
   - Database: `etl_demo_db`
   - Table prefix: `csv_`
6. Chạy crawler → kiểm tra bảng được tạo, ví dụ: `csv_users`

---

### **Bước 4: Tạo Glue Job để ETL sang DynamoDB**

1. Vào **Jobs** → **Add job**
2. Tên: `csv_to_dynamodb_job`
3. IAM Role: chọn role có quyền `glue`, `s3:GetObject`, `dynamodb:PutItem`
4. Type: **Spark**, Language: **Python**
5. Source: chọn bảng `csv_users` từ Glue Catalog
6. Target: chọn **DynamoDB** → bảng `users`
7. Mapping: đảm bảo các cột `id`, `name`, `email` được ánh xạ đúng
8. Script: Glue sẽ tự tạo mã ETL bằng PySpark. Bạn có thể chỉnh sửa nếu cần.

Ví dụ đoạn mã PySpark:

```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Đọc từ Glue Catalog
datasource = glueContext.create_dynamic_frame.from_catalog(database = "etl_demo_db", table_name = "csv_users")

# Ghi vào DynamoDB
glueContext.write_dynamic_frame.from_options(
    frame = datasource,
    connection_type = "dynamodb",
    connection_options = {"dynamodb.output.tableName": "users", "dynamodb.throughput.write.percent": "1.0"}
)

job.commit()
```

---

### **Bước 5: Chạy Job và kiểm tra kết quả**

- Chạy job từ Glue Console.
- Vào DynamoDB → kiểm tra bảng `users` → dữ liệu từ CSV đã được insert.

---

