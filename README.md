---
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![GitLab](https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)


# 1. Giới thiệu về Hệ thống ERP Quản lý Doanh nghiệp

Hệ thống ERP tích hợp được xây dựng trên nền tảng Odoo 15, bao gồm 4 module chính: **Nhân sự**, **Văn bản**, **Tài sản** và **Tài chính - Kế toán**, cung cấp các chức năng sau:

## Module Quản lý Nhân sự (`nhan_su`)
* Quản lý thông tin nhân viên, phòng ban, chức vụ
* Tự động ghi lịch sử công tác khi thay đổi phòng ban/chức vụ
* Tính toán tuổi tự động với validation nghiệp vụ

## Module Quản lý Văn bản (`quan_ly_van_ban`)
* Văn bản đi: Workflow 4 trạng thái (Nháp → Chờ duyệt → Đã duyệt → Phát hành)
* Văn bản đến: Quản lý xử lý với cảnh báo quá hạn tự động
* Phân loại độ khẩn, độ mật và tích hợp với nhân sự

## Module Quản lý Tài sản (`quan_ly_tai_san`)
* Dashboard tổng quan và tình hình mượn trả
* Quản lý loại tài sản và tài sản cụ thể
* Phân bổ tài sản cho các phòng ban
* Khấu hao tài sản (3 phương pháp: Tuyến tính/Giảm dần/Không)
* Kiểm kê tài sản theo phòng ban
* Luân chuyển tài sản giữa các phòng ban
* Thanh lý tài sản (bán/tiêu hủy)
* Quản lý đơn mượn tài sản & cấp phát tài sản
* Liên kết với văn bản đề xuất mua sắm

## Module Quản lý Tài chính - Kế toán (`quan_ly_tai_chinh`) ⭐ MỚI
* **Hệ thống kế toán**: 12 tài khoản VAS, sổ cái với validation cân bằng Nợ/Có
* **Quản lý lương**: Tự động tính BHXH/BHYT/BHTN, tự động tạo bút toán khi duyệt/chi trả
* **Kế toán tài sản**: Tự động tạo bút toán khi mua/khấu hao/thanh lý tài sản (Automation cấp 2)
* **Thu chi & Hóa đơn**: Phiếu thu/chi, hóa đơn bán/mua với liên kết bút toán
* **Dashboard & Báo cáo**: Biểu đồ real-time, báo cáo tài chính
* **Tích hợp AI**: Telegram Bot + Gemini AI hỗ trợ truy vấn tự nhiên


# 2. Cài đặt công cụ, môi trường và các thư viện cần thiết

## 2.1. Clone project

```bash
git clone https://github.com/dinhnghia204/TTDN-16-01-N5.git
cd TTDN-16-01-N5
```

## 2.2. Cài đặt các thư viện cần thiết

Người sử dụng thực thi các lệnh sau để cài đặt các thư viện cần thiết

```bash
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```

## 2.3. Khởi tạo môi trường ảo

Thay đổi trình thông dịch sang môi trường ảo và chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu

```bash
python3.10 -m venv ./venv
```
```bash
source venv/bin/activate
```
```bash
pip3 install -r requirements.txt
```

# 3. Setup database

Khởi tạo database trên docker bằng việc thực thi file docker-compose.yml

```bash
sudo apt install docker-compose
```
```bash
sudo docker-compose up -d
```

# 4. Setup tham số chạy cho hệ thống

## 4.1. Khởi tạo odoo.conf

Tạo tệp **odoo.conf** có nội dung như sau:

```ini
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5434
xmlrpc_port = 8069
```

# 5. Chạy hệ thống và cài đặt các ứng dụng cần thiết

## 5.1. Thứ tự cài đặt modules

⚠️ **QUAN TRỌNG**: Các modules phải được cài đặt theo thứ tự phụ thuộc:

```
1. nhan_su            → Module nền tảng
2. quan_ly_van_ban    → Phụ thuộc: nhan_su
3. quan_ly_tai_san    → Phụ thuộc: nhan_su, quan_ly_van_ban
4. quan_ly_tai_chinh  → Phụ thuộc: tất cả các module trên
```

## 5.2. Lệnh chạy

**Cách 1: Cài đặt từng module theo thứ tự (Khuyến nghị)**
```bash
python3 odoo-bin.py -c odoo.conf -u nhan_su --stop-after-init
python3 odoo-bin.py -c odoo.conf -u quan_ly_van_ban --stop-after-init
python3 odoo-bin.py -c odoo.conf -u quan_ly_tai_san --stop-after-init
python3 odoo-bin.py -c odoo.conf -u quan_ly_tai_chinh --stop-after-init
```

**Cách 2: Cài đặt tất cả cùng lúc**
```bash
python3 odoo-bin.py -c odoo.conf -u nhan_su,quan_ly_van_ban,quan_ly_tai_san,quan_ly_tai_chinh
```

**Cách 3: Sử dụng script tiện ích**
```bash
chmod +x run.sh
./run.sh
```

Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.

## 5.3. Kiểm tra modules đã cài đặt

Sau khi đăng nhập, vào menu **Settings → Apps** và kiểm tra:
- ✅ `nhan_su` - Quản lý Nhân sự
- ✅ `quan_ly_van_ban` - Quản lý Văn bản  
- ✅ `quan_ly_tai_san` - Quản lý Tài sản
- ✅ `quan_ly_tai_chinh` - Quản lý Tài chính/Kế toán

    
