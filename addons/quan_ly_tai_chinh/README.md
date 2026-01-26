# Module Quản lý Tài chính/Kế toán

## Mô tả
Module tài chính kế toán tích hợp hoàn chỉnh với các module Nhân sự và Tài sản, cung cấp:
- Hệ thống tài khoản kế toán theo chuẩn VAS
- Sổ cái kế toán và định khoản tự động
- Quản lý lương nhân viên với tính toán BHXH, BHYT, BHTN
- Kế toán tài sản cố định (mua, khấu hao, thanh lý)
- Dashboard và báo cáo tài chính

## Cài đặt

### 1. Dependencies
Module này phụ thuộc vào:
- `nhan_su` - Module quản lý nhân sự
- `quan_ly_van_ban` - Module quản lý văn bản
- `quan_ly_tai_san` - Module quản lý tài sản

### 2. Cài đặt module
```bash
# Nâng cấp module mới
python3 odoo-bin.py -c odoo.conf -u quan_ly_tai_chinh

# Hoặc cài đặt tất cả modules theo thứ tự
python3 odoo-bin.py -c odoo.conf -u nhan_su,quan_ly_van_ban,quan_ly_tai_san,quan_ly_tai_chinh
```

## Tính năng chính

### 1. Hệ thống tài khoản kế toán
- Pre-load 12 tài khoản cơ bản theo VAS
- Phân loại: Tài sản, Nguồn vốn, Chi phí, Doanh thu
- Hỗ trợ 3 cấp tài khoản
- Tính chất: Nợ, Có, Lưỡng tính

### 2. Sổ cái kế toán
- Định khoản Nợ/Có
- Validation cân bằng tự động
- Liên kết với chứng từ gốc (tài sản, lương, văn bản)
- Trạng thái: Nháp / Đã ghi sổ

### 3. Quản lý lương
**Tính năng:**
- Tạo phiếu lương theo tháng/năm
- Tự động tạo chi tiết từ danh sách nhân viên
- Tính toán tự động: BHXH (8%), BHYT (1.5%), BHTN (1%)
- Workflow: Nháp → Duyệt → Chi trả

**⭐ Automation (MỨC 2):**
- Duyệt phiếu → Tự động tạo bút toán: Nợ TK 622 / Có TK 334
- Chi trả → Tự động tạo bút toán: Nợ TK 334 / Có TK 111
- Real-time notifications

### 4. Kế toán tài sản cố định
**Extend model `tai_san`:**
- Thêm field: TK nguyên giá, TK khấu hao
- Action: Ghi nhận mua tài sản

**⭐ Automation (MỨC 2):**
- Mua tài sản → Tự động tạo bút toán: Nợ TK 211 / Có TK 111
- Khấu hao → Tự động tạo bút toán: Nợ TK 627 / Có TK 214 (mỗi khi tính khấu hao)
- Thanh lý → Tự động xóa sổ TSCĐ + ghi nhận lãi/lỗ

### 5. Dashboard & Báo cáo
- Dashboard tổng quan với biểu đồ Chart.js
- Báo cáo Bảng cân đối kế toán
- Báo cáo Kết quả kinh doanh
- Thống kê theo loại chứng từ, theo tháng

## Tích hợp với modules cũ

### Với `nhan_su`:
- `phieu_luong` → `nhan_vien` (chi tiết lương)
- `so_cai_ke_toan.nguoi_lap_id` → `nhan_vien`

### Với `quan_ly_tai_san`:
- Extend `tai_san` với thông tin kế toán
- Extend `lich_su_khau_hao` tự động tạo bút toán
- Extend `thanh_ly_tai_san` với logic xóa sổ

### Với `quan_ly_van_ban`:
- `so_cai_ke_toan.van_ban_chi_id` → `van_ban_di`

## Workflows tự động (MỨC 2)

### 1. Workflow lương
```
Tạo phiếu → Thêm nhân viên → Duyệt
    ↓ (auto)
Tạo bút toán (Nợ 622 / Có 334)
    ↓
Chi trả
    ↓ (auto)
Tạo bút toán chi tiền (Nợ 334 / Có 111)
```

### 2. Workflow mua tài sản
```
Tạo tài sản
    ↓
Ghi nhận mua
    ↓ (auto)
Tạo bút toán (Nợ 211 / Có 111)
```

### 3. Workflow khấu hao
```
Tính khấu hao (action_tinh_khau_hao)
    ↓
Tạo phiếu khấu hao
    ↓ (auto trigger trong create())
Tạo bút toán (Nợ 627 / Có 214)
```

### 4. Workflow thanh lý
```
Thanh lý tài sản
    ↓
Ghi nhận thanh lý
    ↓ (auto)
Tạo bút toán xóa sổ + lãi/lỗ
```

## Cấu trúc Database

### Models chính:
- `tai_khoan_ke_toan` - Danh mục tài khoản
- `so_cai_ke_toan` - Sổ cái (bút toán)
- `chi_tiet_but_toan` - Chi tiết bút toán (Nợ/Có)
- `phieu_luong` - Phiếu lương
- `chi_tiet_luong` - Chi tiết lương nhân viên
- `bao_cao_tai_chinh` - Dashboard (không lưu DB)

### Sequences:
- `BT/YYYY/XXXX` - Bút toán
- `PL/YYYY/XXXX` - Phiếu lương

## Hướng dẫn sử dụng

### 1. Thiết lập ban đầu
- Hệ thống tài khoản đã được pre-load tự động
- Kiểm tra menu: Tài chính/Kế toán → Danh mục → Tài khoản kế toán

### 2. Quản lý lương
1. Vào menu: Tài chính/Kế toán → Quản lý lương → Phiếu lương
2. Tạo phiếu mới, chọn tháng/năm
3. Click "Tạo chi tiết từ nhân viên"
4. Điều chỉnh lương, phụ cấp, thưởng
5. Click "Duyệt phiếu" → Hệ thống tự động tạo bút toán
6. Click "Chi trả lương" → Tự động tạo bút toán chi tiền

### 3. Kế toán tài sản
1. Vào menu: Quản lý tài sản → Tài sản → Quản lý tài sản cụ thể
2. Mở form tài sản, tab "Kế toán"
3. Click "Ghi nhận mua tài sản" → Tự động tạo bút toán
4. Khi tính khấu hao → Tự động tạo bút toán khấu hao

### 4. Xem Dashboard
- Menu: Tài chính/Kế toán → Báo cáo & Dashboard → Dashboard tài chính
- Hiển thị biểu đồ, thống kê real-time

## Lưu ý kỹ thuật

1. **Validation cân bằng**: Bút toán phải có Tổng Nợ = Tổng Có mới ghi sổ được
2. **Real-time notifications**: Sử dụng `bus.bus` module
3. **Chart.js**: Yêu cầu internet để load CDN (hoặc tải offline)
4. **Cron job**: Đã tạo cron khấu hao hàng tháng (mặc định disabled)

## Tác giả
Nguyễn Ngọc Đan Trường - 1504

## License
LGPL-3
