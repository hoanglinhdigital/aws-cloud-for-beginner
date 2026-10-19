# Lab: Làm quen với Docker – Hello Docker

## Mục tiêu

Sau bài lab này, học viên có thể:

- Hiểu các khái niệm cơ bản: **Image**, **Container**, **Registry**.
- Đăng nhập Docker Hub và chạy container đầu tiên (`hello-world`).
- Sử dụng các câu lệnh Docker thường dùng: `pull`, `run`, `ps`, `images`, `logs`, `exec`, `stop`, `start`, `rm`, `rmi`.
- Chạy một web server Nginx, publish port và truy cập từ trình duyệt.
- Dọn dẹp tài nguyên sau khi thực hành.

## Yêu cầu chuẩn bị

- Máy (hoặc EC2 instance) đã cài đặt Docker. Kiểm tra bằng lệnh:

```bash
docker --version
docker info
```

- Tài khoản [Docker Hub](https://hub.docker.com) (miễn phí) – dùng cho bước `docker login`.
- Nếu dùng EC2 Linux và gặp lỗi `permission denied`, thêm user vào group docker rồi đăng nhập lại:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

## Khái niệm nhanh

| Khái niệm | Giải thích |
|-----------|------------|
| Image | "Bản mẫu" chỉ đọc, chứa ứng dụng + thư viện cần thiết để chạy. |
| Container | Một instance đang chạy (hoặc đã dừng) được tạo từ image. |
| Registry | Nơi lưu trữ image: Docker Hub, Amazon ECR... |
| Tag | Phiên bản của image, ví dụ `nginx:1.27`, `nginx:latest`. |

Luồng cơ bản: `Registry --(pull)--> Image --(run)--> Container`

---

## Phần 1 – Đăng nhập Docker Hub

```bash
docker login
```

Nhập **Username** và **Password** (hoặc Access Token) của Docker Hub. Kết quả mong đợi: `Login Succeeded`.

> Việc đăng nhập giúp tránh giới hạn số lần pull image của tài khoản ẩn danh, và là bước cần thiết nếu muốn `push` image sau này.

## Phần 2 – Chạy container đầu tiên

```bash
docker run hello-world
```

Docker sẽ thực hiện:

1. Tìm image `hello-world` trên máy → không có.
2. Tải (pull) image từ Docker Hub.
3. Tạo và chạy container, in ra thông điệp "Hello from Docker!", sau đó container tự thoát.

## Phần 3 – Xem Image và Container

```bash
# Liệt kê các image có trên máy
docker images

# Liệt kê các container đang chạy
docker ps

# Liệt kê tất cả container (kể cả đã dừng)
docker ps -a
```

**Câu hỏi:** Vì sao `docker ps` không thấy container `hello-world`, còn `docker ps -a` thì thấy?
*Đáp án: container `hello-world` chạy xong và thoát ngay, nên ở trạng thái `Exited`; `docker ps` chỉ hiển thị container đang chạy.*

## Phần 4 – Chạy web server Nginx

### 4.1 Tải image

```bash
docker pull nginx:latest
docker images
```

### 4.2 Chạy container ở chế độ nền và publish port

```bash
docker run -d --name my-nginx -p 8080:80 nginx
```

| Tham số | Ý nghĩa |
|---------|---------|
| `-d` | Chạy nền (detached). |
| `--name my-nginx` | Đặt tên cho container. |
| `-p 8080:80` | Map port **8080** của máy host tới port **80** trong container. |

### 4.3 Kiểm tra

```bash
docker ps
curl http://localhost:8080
```

Hoặc mở trình duyệt truy cập `http://localhost:8080` (với EC2: `http://<Public-IP>:8080`, cần mở port 8080 trong Security Group). Trang "Welcome to nginx!" sẽ hiển thị.

### 4.4 Xem log

```bash
docker logs my-nginx          # xem toàn bộ log
docker logs -f my-nginx       # theo dõi log realtime (Ctrl + C để thoát)
```

Hãy refresh trình duyệt vài lần và quan sát các request xuất hiện trong log.

### 4.5 Vào bên trong container

```bash
docker exec -it my-nginx bash
```

Thử một số lệnh trong container:

```bash
ls /usr/share/nginx/html
cat /etc/nginx/conf.d/default.conf
exit
```

### 4.6 Xem thông tin chi tiết và tài nguyên

```bash
docker inspect my-nginx       # thông tin chi tiết (JSON)
docker stats --no-stream      # CPU/RAM đang dùng
```

## Phần 5 – Vòng đời container: stop / start / restart

```bash
docker stop my-nginx
docker ps                     # không còn thấy my-nginx
docker ps -a                  # my-nginx ở trạng thái Exited

docker start my-nginx
docker restart my-nginx
```

## Phần 6 – Thử nghiệm thay đổi nội dung trang web (Bind mount)

Tạo thư mục và file HTML trên máy host(Chạy command sau bằng Gishbash trong thư mục cụ thể vd D:/demo-docker):

```bash
mkdir -p web && echo '<h1>Hello Docker from my machine. by Linh Nguyen</h1>' > web/index.html
```

Chạy container thứ hai, mount thư mục vào Nginx:

```bash
docker run -d --name my-nginx-2 -p 8081:80 -v "D:/demo-docker/web:/usr/share/nginx/html:ro" nginx
curl http://localhost:8081
```

Kết quả hiển thị `Hello Docker from my machine. by Linh Nguyen`. Sửa file `index.html` trên host rồi `curl` lại để thấy nội dung đổi ngay mà không cần build lại image.

## Phần 7 – Dọn dẹp

```bash
# Dừng và xóa container
docker stop my-nginx my-nginx-2
docker rm my-nginx my-nginx-2

# Xóa image không còn dùng
docker rmi nginx hello-world

# (Tuỳ chọn) Dọn toàn bộ container đã dừng, image không dùng, network thừa
docker system prune
```

> Không thể `docker rmi` một image khi vẫn còn container (kể cả đã dừng) dùng nó – hãy `docker rm` container trước.

Cuối cùng, đăng xuất nếu dùng máy dùng chung:

```bash
docker logout
```

---

## Bảng tổng hợp lệnh Docker cơ bản

| Lệnh | Mô tả |
|------|-------|
| `docker login` / `docker logout` | Đăng nhập / đăng xuất registry. |
| `docker pull <image>` | Tải image về máy. |
| `docker images` | Liệt kê image. |
| `docker run <image>` | Tạo và chạy container. |
| `docker run -d -p H:C --name N <image>` | Chạy nền, map port, đặt tên. |
| `docker ps` / `docker ps -a` | Liệt kê container đang chạy / tất cả. |
| `docker logs [-f] <container>` | Xem log. |
| `docker exec -it <container> bash` | Mở shell trong container. |
| `docker stop` / `start` / `restart` | Điều khiển vòng đời container. |
| `docker inspect <container>` | Xem thông tin chi tiết. |
| `docker stats` | Xem mức sử dụng tài nguyên. |
| `docker rm <container>` | Xóa container. |
| `docker rmi <image>` | Xóa image. |
| `docker system prune` | Dọn tài nguyên không dùng. |

## Bước tiếp theo

Sau khi nắm vững các lệnh cơ bản, các bài lab tiếp theo sẽ hướng dẫn build image bằng `Dockerfile`, đẩy image lên **Amazon ECR** và triển khai container bằng **Amazon ECS**.
