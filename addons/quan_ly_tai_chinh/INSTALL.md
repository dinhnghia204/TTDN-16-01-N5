# HƯỚNG DẪN CÀI ĐẶT MODULE QUẢN LÝ TÀI CHÍNH/KẾ TOÁN

## 📋 Checklist trước khi cài đặt

- [x] Module `nhan_su` đã được cài đặt
- [x] Module `quan_ly_van_ban` đã được cài đặt  
- [x] Module `quan_ly_tai_san` đã được cài đặt
- [x] PostgreSQL đang chạy (port 5434)
- [x] Python 3.10 virtual environment đã kích hoạt

## 🚀 Các bước cài đặt

### Bước 1: Kiểm tra cấu trúc module
```bash
cd /home/nghiax/TTDN-16-01-N5
ls -la addons/quan_ly_tai_chinh/
```

Đảm bảo có các thư mục:
- models/
- data/
- security/
- views/
- static/
- demo/

### Bước 2: Restart Odoo server
```bash
# Stop server hiện tại (Ctrl+C nếu đang chạy)

# Restart với upgrade module
python3 odoo-bin.py -c odoo.conf -u quan_ly_tai_chinh
```

### Bước 3: Kiểm tra logs
Quan sát log để đảm bảo:
- ✅ Module loaded successfully
- ✅ Models registered
- ✅ Data files loaded (12 tài khoản kế toán)
- ✅ Views created

### Bước 4: Truy cập giao diện
1. Mở browser: `http://localhost:8069`
2. Login với user admin
3. Kiểm tra menu mới: **"Tài chính/Kế toán"**

## ✅ Kiểm tra sau cài đặt

### 1. Kiểm tra Tài khoản kế toán
```
Menu: Tài chính/Kế toán → Danh mục → Tài khoản kế toán
```
Phải có 12 tài khoản:
- 111 - Tiền mặt
- 112 - Tiền gửi ngân hàng
- 211 - TSCĐ hữu hình
- 214 - Hao mòn TSCĐ
- 334 - Phải trả NLĐ
- 411 - Nguồn vốn
- 511 - Doanh thu
- 622 - Chi phí nhân công
- 627 - Chi phí khấu hao
- 642 - Chi phí quản lý
- 711 - Thu nhập khác
- 811 - Chi phí khác

### 2. Test Workflow Lương
```
1. Vào menu: Quản lý lương → Phiếu lương
2. Tạo phiếu mới (Tháng 1/2026)
3. Click "Tạo chi tiết từ nhân viên"
4. Click "Duyệt phiếu"
5. Kiểm tra: Phải có thông báo "Duyệt phiếu lương thành công"
6. Vào menu: Kế toán → Sổ cái kế toán
7. Kiểm tra: Có bút toán mới với Mã BT/2026/XXXX
```

### 3. Test Workflow Tài sản
```
1. Vào: Quản lý tài sản → Tài sản → Quản lý tài sản cụ thể
2. Mở 1 tài sản bất kỳ
3. Vào tab "Kế toán"
4. Kiểm tra: Có nút "Ghi nhận mua tài sản"
5. Click nút → Kiểm tra có bút toán mới
```

### 4. Test Dashboard
```
1. Vào: Tài chính/Kế toán → Báo cáo & Dashboard → Dashboard tài chính
2. Kiểm tra hiển thị:
   - 4 cards thống kê
   - 2 biểu đồ (Pie chart + Bar chart)
```

## ⚠️ Xử lý lỗi thường gặp

### Lỗi 1: "Module not found"
```bash
# Kiểm tra odoo.conf
cat odoo.conf | grep addons_path

# Đảm bảo có: addons_path = addons
```

### Lỗi 2: "External ID not found: quan_ly_tai_chinh.tk_xxx"
```bash
# Cài lại data files
python3 odoo-bin.py -c odoo.conf -u quan_ly_tai_chinh --stop-after-init
```

### Lỗi 3: "Access denied for model tai_khoan_ke_toan"
```bash
# Kiểm tra security file
cat addons/quan_ly_tai_chinh/security/ir.model.access.csv
```

### Lỗi 4: Charts không hiển thị
- Kiểm tra internet connection (Chart.js từ CDN)
- Hoặc tải Chart.js về local

## 🔄 Upgrade sau khi sửa code

```bash
# Upgrade chỉ module này
python3 odoo-bin.py -c odoo.conf -u quan_ly_tai_chinh

# Upgrade tất cả modules liên quan
python3 odoo-bin.py -c odoo.conf -u nhan_su,quan_ly_van_ban,quan_ly_tai_san,quan_ly_tai_chinh
```

## 📊 Test kịch bản đầy đủ

### Kịch bản 1: Quản lý lương
1. Tạo phiếu lương tháng 1/2026
2. Tạo chi tiết từ nhân viên
3. Cập nhật lương cho 2-3 nhân viên
4. Duyệt phiếu → Kiểm tra bút toán tự động
5. Chi trả → Kiểm tra bút toán chi tiền

### Kịch bản 2: Mua tài sản
1. Vào module Tài sản, tạo tài sản mới (giá 10 triệu)
2. Vào tab Kế toán
3. Ghi nhận mua tài sản
4. Kiểm tra sổ cái có bút toán: Nợ 211 / Có 111 = 10 triệu

### Kịch bản 3: Khấu hao
1. Vào tài sản vừa mua
2. Chọn phương pháp khấu hao: Tuyến tính
3. Thời gian sử dụng: 5 năm
4. Click "Tính khấu hao"
5. Vào Lịch sử khấu hao → Kiểm tra có bút toán khấu hao

### Kịch bản 4: Thanh lý
1. Vào module Tài sản → Thanh lý tài sản
2. Tạo phiếu thanh lý mới
3. Nhập giá thanh lý
4. Ghi nhận thanh lý
5. Kiểm tra bút toán xóa sổ

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Xem logs: Terminal đang chạy Odoo
2. Kiểm tra file README.md trong module
3. Review file models để hiểu logic

## ✨ Hoàn tất!

Sau khi test thành công tất cả workflows, module đã sẵn sàng sử dụng!
