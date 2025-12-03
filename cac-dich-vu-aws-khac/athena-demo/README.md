Tuyệt vời Linh! Dưới đây là hướng dẫn từng bước để bạn làm quen với **AWS Athena** và sử dụng nó để truy vấn dữ liệu từ các file CSV trong một S3 bucket. Hướng dẫn này tập trung vào thao tác qua **AWS Console**, không cần viết code hay thiết lập hạ tầng.

---

## 🧭 Hướng dẫn từng bước sử dụng Athena để query CSV trên S3

### **Bước 1: Chuẩn bị dữ liệu CSV trên S3**
- Đảm bảo bạn đã có file `.csv` trong một bucket S3.
- File nên có header dòng đầu tiên (tên cột).
- Ví dụ: `s3://my-data-bucket/sales_data.csv`

### **Bước 2: Truy cập Athena**
- Vào [AWS Console](https://console.aws.amazon.com/)
- Tìm dịch vụ **Athena** và mở giao diện Athena Console.

### **Bước 3: Cấu hình query result location**
- Trước khi chạy truy vấn, Athena cần nơi lưu kết quả.
- Trong Athena Console:
  - Chọn **Settings** (góc phải trên cùng).
  - Chọn **Manage** → nhập đường dẫn S3 để lưu kết quả, ví dụ: `s3://my-data-bucket/athena-results/`

### **Bước 4: Tạo database**
- Trong tab **Query Editor**, chạy lệnh SQL sau để tạo database:

```sql
CREATE DATABASE my_data_db;
```

- Chọn database vừa tạo từ dropdown bên trái.

### **Bước 5: Tạo bảng từ file CSV**
- Giả sử file CSV có cấu trúc như sau:

```csv
order_id,customer_name,amount,date
1001,Alice,250.5,2023-10-01
1002,Bob,180.0,2023-10-02
```

- Chạy lệnh SQL để tạo bảng:

```sql
CREATE EXTERNAL TABLE sales_data (
  order_id INT,
  customer_name STRING,
  amount DOUBLE,
  date STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar" = "\""
)
LOCATION 's3://my-data-bucket/sales_data/'
TBLPROPERTIES ('has_encrypted_data'='false');
```

> 📌 Lưu ý: `LOCATION` là thư mục chứa file CSV, không phải file cụ thể.

### **Bước 6: Truy vấn dữ liệu**
- Ví dụ truy vấn toàn bộ dữ liệu:

```sql
SELECT * FROM sales_data;
```

- Truy vấn có điều kiện:

```sql
SELECT customer_name, amount
FROM sales_data
WHERE amount > 200;
```

### **Bước 7: Tối ưu hóa chi phí**
- Dùng định dạng **Parquet** hoặc **ORC** thay vì CSV để giảm chi phí quét dữ liệu.
- Nén dữ liệu (gzip, snappy).
- Partition dữ liệu nếu có nhiều file.

---
