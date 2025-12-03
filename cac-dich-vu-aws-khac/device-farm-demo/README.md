Dưới đây là hướng dẫn **step-by-step đơn giản** để Linh có thể kiểm thử một ứng dụng Android (.apk) bằng **AWS Device Farm** thông qua **AWS Console**:

---

## 📱 Bước 1: Chuẩn bị file `.apk`

- Đảm bảo bạn có file `.apk` của ứng dụng Android cần kiểm thử.
- File này nên là bản release hoặc debug đã được ký hợp lệ.

---

## 🧭 Bước 2: Truy cập AWS Device Farm

1. Vào [AWS Console → Device Farm](https://console.aws.amazon.com/devicefarm).
2. Chọn **Create a new project**.
   - Đặt tên: ví dụ `DemoAppTest`.
   - Nhấn **Create project**.

---

## 📦 Bước 3: Tạo một test run

1. Trong project vừa tạo, chọn **Create a new run**.
2. Chọn **Mobile App** → **Android**.
3. Upload file `.apk` của bạn → nhấn **Next**.

---

## 🧪 Bước 4: Chọn loại kiểm thử

Bạn có 2 lựa chọn:

### 🔹 Option 1: **Built-in Explorer (no test script)**

- Chọn **Built-in: Fuzz** hoặc **Explorer** để AWS tự động thao tác ngẫu nhiên trên app.
- Phù hợp với demo nhanh, không cần viết test case.

### 🔹 Option 2: **Custom Test (Appium, Espresso, etc.)**

- Chọn framework bạn dùng (Appium, Calabash, etc.).
- Upload file test script (nếu có).
- Phù hợp với kiểm thử có kịch bản cụ thể.

→ Với demo đơn giản, chọn **Built-in Explorer**.

---

## 📱 Bước 5: Chọn thiết bị kiểm thử

1. Chọn **Device Pool**:
   - Có thể dùng pool mặc định hoặc tạo pool riêng.
   - Chọn 2–3 thiết bị phổ biến như:
     - Samsung Galaxy S10
     - Google Pixel 4
     - Xiaomi Mi 9

2. Nhấn **Next**.

---

## ⚙️ Bước 6: Cấu hình test run

- Đặt tên run: `DemoRun01`.
- Giữ các thiết lập mặc định (timeout, location, etc.).
- Nhấn **Confirm and start run**.

---

## 📊 Bước 7: Xem kết quả

- Sau vài phút, test run sẽ hoàn tất.
- Vào tab **Results** để xem:
  - Video thao tác trên thiết bị.
  - Logs (logcat, performance).
  - Screenshots.
  - Crash reports (nếu có).

---

## ✅ Bước 8: Phân tích & cải tiến

- Dựa vào kết quả, bạn có thể:
  - Phát hiện lỗi UI hoặc crash.
  - Tối ưu hiệu năng.
  - Viết thêm test script cho lần kiểm thử sau.

---