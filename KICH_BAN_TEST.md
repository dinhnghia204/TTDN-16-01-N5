# KỊCH BẢN TEST HỆ THỐNG - Module Quản lý Tài chính/Kế toán

## 📋 TỔNG QUAN HỆ THỐNG

### Modules đã triển khai:
1. **nhan_su** - Quản lý nhân viên, phòng ban, chức vụ
2. **quan_ly_van_ban** - Quản lý văn bản đi/đến
3. **quan_ly_tai_san** - Quản lý tài sản cố định (TSCĐ)
4. **quan_ly_tai_chinh** - Quản lý tài chính/kế toán ⭐ (Module mới)

### Cấu trúc Module Tài chính:
**15 Models:**
- `tai_khoan_ke_toan` - Hệ thống tài khoản VAS
- `so_cai_ke_toan` - Sổ cái và bút toán
- `chi_tiet_but_toan` - Chi tiết định khoản
- `phieu_luong` + `chi_tiet_luong` - Quản lý lương
- `phieu_thu` - Phiếu thu tiền
- `phieu_chi` - Phiếu chi tiền
- `hoa_don_ban` + `hoa_don_ban_chi_tiet` - Hóa đơn bán hàng
- `hoa_don_mua` + `hoa_don_mua_chi_tiet` - Hóa đơn mua hàng
- `bao_cao_tai_chinh` - Báo cáo tài chính
- 3 Models extend: `tai_san`, `thanh_ly_tai_san`, `lich_su_khau_hao`

---

## 🎯 KỊCH BẢN TEST CHI TIẾT

---

## **KỊCH BẢN 1: QUẢN LÝ DANH MỤC TÀI KHOẢN**

### Mục tiêu:
Kiểm tra hệ thống tài khoản kế toán VAS đã được cài đặt đúng chưa

### Điều kiện tiên quyết:
- Module quan_ly_tai_chinh đã được cài đặt
- Database đã được khởi tạo

### Các bước thực hiện:

#### Bước 1: Kiểm tra tài khoản có sẵn
```
Menu: Tài chính/Kế toán → Danh mục → Tài khoản kế toán
```

**Kết quả mong đợi:**
| Mã TK | Tên tài khoản | Loại | Cấp |
|-------|--------------|------|-----|
| 111 | Tiền mặt | Tài sản | Cấp 2 |
| 112 | Tiền gửi ngân hàng | Tài sản | Cấp 2 |
| 131 | Phải thu của khách hàng | Tài sản | Cấp 2 |
| 156 | Hàng hóa | Tài sản | Cấp 2 |
| 211 | Tài sản cố định hữu hình | Tài sản | Cấp 2 |
| 214 | Hao mòn TSCĐ | Tài sản | Cấp 2 |
| 331 | Phải trả người bán | Nguồn vốn | Cấp 2 |
| 334 | Phải trả CNV | Nguồn vốn | Cấp 2 |
| 411 | Nguồn vốn kinh doanh | Nguồn vốn | Cấp 2 |
| 511 | Doanh thu | Nguồn vốn | Cấp 2 |
| 622 | Chi phí nhân viên | Tài sản | Cấp 2 |
| 627 | Chi phí khấu hao TSCĐ | Tài sản | Cấp 2 |
| 642 | Chi phí quản lý DN | Tài sản | Cấp 2 |
| 711 | Thu nhập khác | Nguồn vốn | Cấp 2 |
| 811 | Chi phí khác | Tài sản | Cấp 2 |

✅ **Pass:** Tất cả 15 tài khoản hiển thị đúng
❌ **Fail:** Thiếu tài khoản hoặc thông tin sai

#### Bước 2: Tạo tài khoản mới (Tùy chọn)
```
Click: Create
Nhập:
- Mã TK: 512
- Tên: Doanh thu bán hàng
- Loại: Nguồn vốn
- Cấp: Cấp 3
- TK cha: 511
```

✅ **Pass:** Tạo thành công, mã TK unique
❌ **Fail:** Trùng mã TK hoặc validation error

---

## **KỊCH BẢN 2: QUẢN LÝ LƯƠNG NHÂN VIÊN (CÓ SẴN)**

### Mục tiêu:
Kiểm tra workflow tính lương tự động và tạo bút toán chi lương

### Điều kiện tiên quyết:
- Có ít nhất 2 nhân viên trong hệ thống
- TK 334 (Phải trả CNV) và TK 622 (Chi phí nhân viên) đã tồn tại

### Các bước thực hiện:

#### Bước 1: Tạo phiếu lương
```
Menu: Tài chính/Kế toán → Quản lý lương → Phiếu lương
Click: Create
```

**Nhập liệu:**
- Tháng lương: 01/2026
- Ghi chú: "Lương tháng 1/2026"

**Chi tiết lương (Add a line):**
| Nhân viên | Lương cơ bản | Phụ cấp | Thưởng | Khấu trừ |
|-----------|--------------|---------|---------|----------|
| Nguyễn Văn A | 10,000,000 | 2,000,000 | 1,000,000 | 500,000 |
| Trần Thị B | 8,000,000 | 1,500,000 | 0 | 300,000 |

**Lương thực nhận tự động:**
- Nguyễn Văn A: 12,500,000 VNĐ
- Trần Thị B: 9,200,000 VNĐ
- **Tổng:** 21,700,000 VNĐ

Click: **Save**

#### Bước 2: Tạo bút toán chi lương
```
Click nút: "Tạo bút toán chi lương" (màu xanh)
```

**Kết quả mong đợi:**
1. Hiển thị notification: "Đã tạo bút toán chi lương PL/2026/0001"
2. Button "Tạo bút toán" biến mất
3. Field "Bút toán" hiển thị link đến bút toán

#### Bước 3: Kiểm tra bút toán
```
Click vào link "Bút toán" hoặc
Menu: Kế toán → Sổ cái kế toán
```

**Định khoản mong đợi:**
```
Nợ TK 622 (Chi phí NV): 21,700,000 VNĐ
    Có TK 334 (Phải trả): 21,700,000 VNĐ
```

✅ **Pass:** Bút toán được tạo đúng, số liệu khớp
❌ **Fail:** Số tiền sai, định khoản sai, hoặc lỗi tạo bút toán

#### Bước 4: Ghi sổ bút toán
```
Trong form Bút toán:
Click: "Ghi sổ" (nếu trạng thái = Nháp)
```

✅ **Pass:** Trạng thái chuyển sang "Đã ghi sổ"
❌ **Fail:** Lỗi khi ghi sổ

---

## **KỊCH BẢN 3: MUA TÀI SẢN CỐ ĐỊNH (TÍCH HỢP ĐẦY ĐỦ)**

### Mục tiêu:
Kiểm tra workflow mua TSCĐ → Tự động tạo Hóa đơn mua + Phiếu chi + Bút toán

### Điều kiện tiên quyết:
- Module quan_ly_tai_san đã cài đặt
- TK 111, 211 đã tồn tại

### Các bước thực hiện:

#### Bước 1: Tạo tài sản mới
```
Menu: Quản lý tài sản → Tài sản → Create
```

**Nhập liệu:**
- Mã tài sản: Tự động (TS/2026/XXXX)
- Tên tài sản: "Laptop Dell XPS 15 - 2026"
- Danh mục: Máy tính (hoặc tạo mới)
- Ngày mua: 26/01/2026
- Giá trị ban đầu: 25,000,000 VNĐ
- Đơn vị tính: Cái
- Phương pháp khấu hao: Tuyến tính
- Thời gian sử dụng (năm): 3

**Fields tự động (từ module Tài chính):**
- TK Nguyên giá: 211 (tự động)
- TK Khấu hao lũy kế: 214 (tự động)

Click: **Save**

#### Bước 2: Ghi nhận mua tài sản
```
Click nút: "Ghi nhận mua tài sản" (màu xanh)
```

**Kết quả mong đợi:**
1. Notification: "Đã tạo Hóa đơn + Phiếu chi + Bút toán cho tài sản TS/2026/XXXX"
2. Button "Ghi nhận mua" biến mất
3. Hiển thị 3 fields mới:
   - Hóa đơn mua: HDM/2026/XXXX
   - Phiếu chi: PC/2026/XXXX
   - Bút toán mua: Link

#### Bước 3: Kiểm tra Hóa đơn mua
```
Click vào link "Hóa đơn mua" hoặc
Menu: Tài chính/Kế toán → Hóa đơn → Hóa đơn mua
```

**Thông tin mong đợi:**
- Số HĐ: HDM/2026/0001
- Ngày HĐ: 26/01/2026
- Nhà cung cấp: "Nhà cung cấp TSCĐ"
- Loại mua: Mua tài sản
- Trạng thái: Đã nhận HĐ

**Chi tiết hóa đơn:**
| Tên hàng hóa | ĐVT | SL | Đơn giá | Thành tiền |
|--------------|-----|----|---------|-----------| 
| TS/2026/XXXX - Laptop Dell XPS 15 - 2026 | Cái | 1 | 25,000,000 | 25,000,000 |

- VAT: 0%
- Tổng thanh toán: 25,000,000 VNĐ

#### Bước 4: Kiểm tra Phiếu chi
```
Menu: Tài chính/Kế toán → Quỹ tiền → Phiếu chi
```

**Thông tin mong đợi:**
- Mã phiếu: PC/2026/0001
- Ngày chi: 26/01/2026
- Người nhận: "Nhà cung cấp TSCĐ"
- Loại chi: Tiền mặt
- TK Nợ: 211 (TSCĐ)
- TK Có: 111 (Tiền mặt)
- Số tiền: 25,000,000 VNĐ
- Trạng thái: Đã chi
- Hóa đơn mua: Link đến HDM/2026/0001
- Tài sản: Link đến TS/2026/XXXX

#### Bước 5: Kiểm tra Bút toán
```
Menu: Kế toán → Sổ cái kế toán
```

**Định khoản mong đợi:**
```
Chứng từ: HDM/2026/0001
Diễn giải: Mua Laptop Dell XPS 15 - 2026

Nợ TK 211 (TSCĐ): 25,000,000 VNĐ
    Có TK 111 (Tiền mặt): 25,000,000 VNĐ
```

✅ **Pass:** Tất cả 3 chứng từ được tạo và liên kết đúng
❌ **Fail:** Thiếu chứng từ, số liệu sai, hoặc không liên kết

---

## **KỊCH BẢN 4: THANH LÝ TÀI SẢN (TÍCH HỢP PHIẾU THU)**

### Mục tiêu:
Kiểm tra workflow thanh lý TSCĐ → Tự động tạo Phiếu thu + Bút toán thanh lý phức tạp

### Điều kiện tiên quyết:
- Đã có tài sản trong hệ thống (từ Kịch bản 3)
- Tài sản chưa bị thanh lý
- TK 111, 211, 214, 711, 811 đã tồn tại

### Các bước thực hiện:

#### Bước 1: Tạo phiếu thanh lý
```
Menu: Quản lý tài sản → Luân chuyển/Thanh lý → Thanh lý tài sản
Click: Create
```

**Nhập liệu:**
- Mã thanh lý: Tự động (TL/2026/XXXX)
- Hành động: Bán
- Tài sản: Chọn TS/2026/0001 (Laptop Dell XPS 15)
- Người thực hiện: Chọn nhân viên
- Thời gian thanh lý: 26/01/2026 19:00:00
- Lý do: "Hết khấu hao, nâng cấp thiết bị mới"

**Fields tự động:**
- Giá gốc: 25,000,000 VNĐ (từ tài sản)
- Giá bán: 10,000,000 VNĐ (nhập thủ công)

**Fields mới (Module Tài chính):**
- Giá thanh lý: 10,000,000 VNĐ (nhập = Giá bán)

Click: **Save**

#### Bước 2: Ghi nhận thanh lý
```
Click nút: "Ghi nhận thanh lý (Tạo phiếu thu)" (màu xanh)
```

**Kết quả mong đợi:**
1. Notification: "Đã tạo bút toán thanh lý TL/2026/0001 + Phiếu thu PT/2026/0001"
2. Hiển thị 2 fields:
   - Phiếu thu: PT/2026/0001
   - Bút toán thanh lý: Link
3. Trạng thái "Đã ghi nhận KT" = True

#### Bước 3: Kiểm tra Phiếu thu
```
Menu: Tài chính/Kế toán → Quỹ tiền → Phiếu thu
```

**Thông tin mong đợi:**
- Mã phiếu: PT/2026/0001
- Ngày thu: 26/01/2026
- Người nộp: "Thu thanh lý tài sản"
- Loại thu: Tiền mặt
- TK Nợ: 111 (Tiền mặt)
- TK Có: 711 (Thu nhập khác)
- Số tiền: 10,000,000 VNĐ
- Diễn giải: "Thu tiền thanh lý Laptop Dell XPS 15 - 2026"
- Trạng thái: Đã thu

#### Bước 4: Kiểm tra Bút toán thanh lý
```
Click vào link "Bút toán thanh lý"
```

**Định khoản phức tạp (giả sử chưa khấu hao):**
```
Chứng từ: TL/2026/0001
Diễn giải: Thanh lý Laptop Dell XPS 15 - 2026

1. Xóa sổ khấu hao lũy kế (0 VNĐ nếu mới mua):
   Nợ TK 214: 0 VNĐ
       Có TK 211: 0 VNĐ

2. Thu tiền thanh lý:
   Nợ TK 111: 10,000,000 VNĐ
       Có TK 211: 10,000,000 VNĐ (không ghi vào 711)

3. Lỗ thanh lý (25M - 10M = 15M):
   Nợ TK 811 (Chi phí khác): 15,000,000 VNĐ
       Có TK 211: 15,000,000 VNĐ

Tổng Nợ TK 211: 25,000,000 VNĐ (cân bằng)
```

**Lưu ý logic:**
- Nếu Giá thanh lý > Giá trị còn lại → Lãi (Có TK 711)
- Nếu Giá thanh lý < Giá trị còn lại → Lỗ (Nợ TK 811)

✅ **Pass:** Phiếu thu + Bút toán thanh lý đúng, số liệu cân bằng
❌ **Fail:** Định khoản sai hoặc số liệu không khớp

---

## **KỊCH BẢN 5: QUẢN LÝ HOÁ ĐƠN BÁN HÀNG + VAT**

### Mục tiêu:
Kiểm tra tạo hóa đơn bán, tính VAT tự động, và ghi nhận doanh thu

### Điều kiện tiên quyết:
- TK 111, 112, 131, 511 đã tồn tại

### Các bước thực hiện:

#### Bước 1: Tạo hóa đơn bán
```
Menu: Tài chính/Kế toán → Hóa đơn → Hóa đơn bán
Click: Create
```

**Nhập liệu:**
- Số HĐ: Tự động (HDB/2026/0001)
- Ngày HĐ: 26/01/2026
- Khách hàng: "Công ty ABC"
- Mã số thuế: 0123456789
- Địa chỉ: "123 Đường XYZ, TP.HCM"
- Hình thức thanh toán: Tiền mặt
- VAT: 10%

**Chi tiết hóa đơn (Add a line):**
| Tên hàng hóa | ĐVT | SL | Đơn giá | Thành tiền |
|--------------|-----|----|---------|-----------| 
| Laptop HP ProBook 450 | Cái | 2 | 15,000,000 | 30,000,000 |
| Chuột Logitech MX Master | Cái | 5 | 1,500,000 | 7,500,000 |

**Tính toán tự động:**
- Tổng tiền hàng: 37,500,000 VNĐ
- Tiền VAT (10%): 3,750,000 VNĐ
- **Tổng thanh toán: 41,250,000 VNĐ**

Click: **Save**

#### Bước 2: Xuất hóa đơn
```
Click nút: "Xuất hóa đơn" (màu xanh)
```

**Kết quả mong đợi:**
1. Trạng thái: Nháp → Đã xuất
2. Button "Xuất hóa đơn" biến mất
3. Hiển thị field "Bút toán": Link

#### Bước 3: Kiểm tra bút toán doanh thu
```
Click vào link "Bút toán"
```

**Định khoản mong đợi:**
```
Chứng từ: HDB/2026/0001
Diễn giải: Bán hàng cho Công ty ABC

Nợ TK 111 (Tiền mặt): 41,250,000 VNĐ
    Có TK 511 (Doanh thu): 37,500,000 VNĐ
    Có TK 3331 (VAT đầu ra): 3,750,000 VNĐ
```

**Lưu ý:** Nếu TK 3331 không tồn tại, hệ thống tự động tạo

✅ **Pass:** VAT tính đúng, bút toán cân bằng
❌ **Fail:** VAT sai, định khoản sai

---

## **KỊCH BẢN 6: QUẢN LÝ HOÁ ĐƠN MUA HÀNG**

### Mục tiêu:
Kiểm tra workflow mua hàng hóa, vật tư, dịch vụ (không phải TSCĐ)

### Điều kiện tiên quyết:
- TK 111, 112, 156, 331 đã tồn tại

### Các bước thực hiện:

#### Bước 1: Tạo hóa đơn mua hàng hóa
```
Menu: Tài chính/Kế toán → Hóa đơn → Hóa đơn mua
Click: Create
```

**Nhập liệu:**
- Số HĐ: Tự động (HDM/2026/0002)
- Ngày HĐ: 26/01/2026
- Nhà cung cấp: "Công ty XYZ"
- Loại mua: Mua hàng hóa
- Hình thức thanh toán: Công nợ
- VAT: 5%

**Chi tiết:**
| Tên hàng hóa | ĐVT | SL | Đơn giá | Thành tiền |
|--------------|-----|----|---------|-----------| 
| Bàn làm việc gỗ | Cái | 10 | 2,000,000 | 20,000,000 |

**Tính toán:**
- Tổng tiền hàng: 20,000,000 VNĐ
- Tiền VAT (5%): 1,000,000 VNĐ
- **Tổng thanh toán: 21,000,000 VNĐ**

Click: **Save**

#### Bước 2: Xác nhận nhận hàng
```
Click nút: "Xác nhận nhận HĐ"
```

**Kết quả mong đợi:**
1. Trạng thái: Nháp → Đã nhận HĐ
2. Hiển thị "Bút toán": Link

#### Bước 3: Kiểm tra bút toán
```
Click vào "Bút toán"
```

**Định khoản mong đợi:**
```
Nợ TK 156 (Hàng hóa): 20,000,000 VNĐ
Nợ TK 133 (VAT đầu vào): 1,000,000 VNĐ
    Có TK 331 (Phải trả NCC): 21,000,000 VNĐ
```

✅ **Pass:** Hàng hóa ghi TK 156, VAT ghi TK 133
❌ **Fail:** Định khoản sai TK

---

## **KỊCH BẢN 7: QUẢN LÝ QUỸ TIỀN MẶT - PHIẾU THU/CHI ĐỘC LẬP**

### Mục tiêu:
Kiểm tra tạo phiếu thu/chi không liên quan đến hóa đơn

### Test Case 7A: Phiếu thu khác

#### Các bước:
```
Menu: Tài chính/Kế toán → Quỹ tiền → Phiếu thu
Click: Create
```

**Nhập liệu:**
- Ngày thu: 26/01/2026
- Người nộp: "Nguyễn Văn X"
- Loại thu: Tiền mặt
- Nội dung: Thu khác
- TK Nợ: 111 (Tiền mặt)
- TK Có: 711 (Thu nhập khác)
- Số tiền: 5,000,000 VNĐ
- Diễn giải: "Thu tiền cho thuê văn phòng tháng 1/2026"

Click: **Save** → Click: **"Xác nhận thu"**

**Kết quả:** Tạo bút toán Nợ 111 / Có 711

### Test Case 7B: Phiếu chi văn phòng phẩm

#### Các bước:
```
Menu: Quỹ tiền → Phiếu chi → Create
```

**Nhập liệu:**
- Ngày chi: 26/01/2026
- Người nhận: "Cửa hàng văn phòng phẩm ABC"
- Loại chi: Tiền mặt
- Nội dung: Chi văn phòng phẩm
- TK Nợ: 642 (Chi phí QLDN)
- TK Có: 111 (Tiền mặt)
- Số tiền: 2,500,000 VNĐ
- Diễn giải: "Mua giấy A4, bút, thư mục"

Click: **Save** → Click: **"Xác nhận chi"**

**Kết quả:** Tạo bút toán Nợ 642 / Có 111

✅ **Pass:** Phiếu thu/chi độc lập hoạt động bình thường
❌ **Fail:** Không tạo được bút toán

---

## **KỊCH BẢN 8: BÁO CÁO TÀI CHÍNH (RPC METHOD)**

### Mục tiêu:
Kiểm tra dashboard và báo cáo tài chính (qua RPC hoặc View)

### Test Case 8A: Dashboard tài chính

#### Các bước:
```
Menu: Tài chính/Kế toán → Báo cáo & Dashboard → Dashboard tài chính
```

**Kết quả mong đợi:**
1. Hiển thị biểu đồ tròn: Phân bổ tài sản theo loại
2. Hiển thị biểu đồ cột: Tình hình doanh thu/chi phí theo tháng
3. Các chỉ số KPI:
   - Tổng tài sản
   - Tổng nguồn vốn
   - Doanh thu tháng
   - Chi phí tháng

### Test Case 8B: Báo cáo sổ quỹ

**Gọi qua Developer Console (F12):**
```javascript
// RPC call
odoo.rpc({
    model: 'bao_cao_tai_chinh',
    method: 'get_bao_cao_so_quy',
    args: [[], '2026-01-01', '2026-01-31'],
}).then(function(result) {
    console.log(result);
});
```

**Kết quả mong đợi (JSON):**
```json
{
  "tong_thu": 51250000,
  "tong_chi": 2500000,
  "ton_cuoi_ky": 48750000,
  "chi_tiet_thu": [
    {"ngay": "2026-01-26", "ma_phieu": "PT/2026/0001", "so_tien": 10000000},
    {"ngay": "2026-01-26", "ma_phieu": "HDB/2026/0001", "so_tien": 41250000}
  ],
  "chi_tiet_chi": [
    {"ngay": "2026-01-26", "ma_phieu": "PC/2026/0001", "so_tien": 25000000},
    {"ngay": "2026-01-26", "ma_phieu": "PC/2026/0002", "so_tien": 2500000}
  ]
}
```

✅ **Pass:** Dashboard hiển thị biểu đồ, báo cáo trả về đúng JSON
❌ **Fail:** Lỗi RPC, biểu đồ không hiển thị

---

## **KỊCH BẢN 9: KHẤU HAO TỰ ĐỘNG (CRON JOB)**

### Mục tiêu:
Kiểm tra cronjob tự động tính khấu hao hàng tháng

### Điều kiện tiên quyết:
- Có tài sản với pp_khau_hao = 'straight-line'
- TK 627, 214 đã tồn tại

### Các bước thực hiện:

#### Bước 1: Kiểm tra cấu hình cronjob
```
Menu: Settings → Technical → Automation → Scheduled Actions
Tìm: "Tính khấu hao hàng tháng"
```

**Thông tin:**
- Model: tai_san
- Function: _cron_tinh_khau_hao_hang_thang
- Interval: 1 Month
- Next Execution Date: Ngày đầu tháng sau

#### Bước 2: Test thủ công (Developer mode)
```
Menu: Settings → Technical → Scheduled Actions → "Tính khấu hao hàng tháng"
Click: "Run Manually"
```

**Kết quả mong đợi:**
1. Với tài sản 25,000,000 VNĐ / 3 năm:
   - Khấu hao 1 tháng = 25,000,000 / 36 = 694,444 VNĐ
2. Tạo bút toán:
   ```
   Nợ TK 627: 694,444 VNĐ
       Có TK 214: 694,444 VNĐ
   ```

#### Bước 3: Kiểm tra lịch sử khấu hao
```
Menu: Quản lý tài sản → Tài sản → Mở tài sản
Tab: "Lịch sử khấu hao"
```

**Kết quả:** Hiển thị dòng mới với:
- Tháng: 01/2026
- Số tiền: 694,444 VNĐ
- Giá trị còn lại: 24,305,556 VNĐ

✅ **Pass:** Cronjob chạy đúng, bút toán khấu hao được tạo
❌ **Fail:** Không tạo bút toán hoặc số tiền sai

---

## **KỊCH BẢN 10: KIỂM TRA TÍCH HỢP MODULES**

### Mục tiêu:
Kiểm tra liên kết giữa các modules

### Test Case 10A: Nhân sự → Tài chính

**Kiểm tra:**
1. Tạo phiếu lương → Field "Nhân viên" lấy từ model `nhan_vien`
2. Phiếu thu/chi → Field "Người lập" lấy nhân viên đầu tiên

✅ **Pass:** Dropdown hiển thị danh sách nhân viên
❌ **Fail:** Lỗi "user_id not found"

### Test Case 10B: Tài sản → Tài chính

**Kiểm tra:**
1. Mua tài sản → Tự động tạo hóa đơn + phiếu chi
2. Thanh lý tài sản → Tự động tạo phiếu thu
3. Lịch sử khấu hao → Tạo bút toán vào sổ cái

✅ **Pass:** 3 liên kết hoạt động
❌ **Fail:** Không tạo chứng từ liên kết

### Test Case 10C: Hóa đơn → Phiếu thu/chi

**Kiểm tra:**
1. Hóa đơn mua → Có thể tạo nhiều phiếu chi
2. Hóa đơn bán → Có thể tạo nhiều phiếu thu
3. Xem phiếu → Hiển thị link đến hóa đơn

✅ **Pass:** One2many relationship hoạt động
❌ **Fail:** Không liên kết hoặc lỗi foreign key

---

## 📊 **BẢNG TỔNG HỢP KẾT QUẢ TEST**

| # | Kịch bản | Trạng thái | Ghi chú |
|---|----------|-----------|---------|
| 1 | Quản lý TK kế toán | ⬜ Chưa test | 15 TK VAS |
| 2 | Lương nhân viên | ⬜ Chưa test | Workflow cũ |
| 3 | Mua tài sản | ⬜ Chưa test | **3 chứng từ tự động** |
| 4 | Thanh lý tài sản | ⬜ Chưa test | **Phiếu thu + Bút toán phức tạp** |
| 5 | Hóa đơn bán | ⬜ Chưa test | **VAT tự động** |
| 6 | Hóa đơn mua | ⬜ Chưa test | **Phân loại TK theo loại mua** |
| 7 | Phiếu thu/chi độc lập | ⬜ Chưa test | Không cần hóa đơn |
| 8 | Báo cáo/Dashboard | ⬜ Chưa test | RPC methods |
| 9 | Khấu hao tự động | ⬜ Chưa test | Cronjob |
| 10 | Tích hợp modules | ⬜ Chưa test | Cross-module |

---

## 🔍 **CHECKLIST KIỂM TRA CUỐI CÙNG**

### Kiểm tra cơ sở dữ liệu:
```sql
-- Số lượng tài khoản
SELECT COUNT(*) FROM tai_khoan_ke_toan;  -- Expect: >= 15

-- Tổng số bút toán
SELECT COUNT(*) FROM so_cai_ke_toan;

-- Tổng tiền trong TK 111 (Tiền mặt)
SELECT SUM(so_tien_no) - SUM(so_tien_co) as ton_tien_mat
FROM chi_tiet_but_toan
JOIN tai_khoan_ke_toan ON chi_tiet_but_toan.tk_no_id = tai_khoan_ke_toan.id
WHERE tai_khoan_ke_toan.ma_tai_khoan = '111';
```

### Kiểm tra hiệu năng:
- Thời gian tải Dashboard < 3s
- Thời gian tạo bút toán < 1s
- Thời gian search < 500ms

### Kiểm tra bảo mật:
- Tất cả models có security rules
- Không có SQL injection trong RPC methods
- Field passwords được encrypt

---

## 📝 **GHI CHÚ QUAN TRỌNG**

### Lỗi đã biết:
1. ⚠️ Field `user_id` không tồn tại trong `nhan_vien` → Đã sửa
2. ⚠️ Field `ma_hang` không tồn tại trong `hoa_don_mua_chi_tiet` → Đã sửa
3. ⚠️ Field `ngay_thanh_ly` → Phải dùng `thoi_gian_thanh_ly` → Đã sửa

### Dữ liệu mẫu cần chuẩn bị:
- Ít nhất 3 nhân viên
- Ít nhất 2 phòng ban
- Ít nhất 5 tài sản
- Ít nhất 1 khách hàng (tạo trong Contact)

### Môi trường test:
- Odoo 15 Community
- PostgreSQL 10
- Python 3.10
- Ubuntu 22.04 (WSL)
- Port: 8069

---

**Người thực hiện test:** _______________  
**Ngày test:** _______________  
**Kết quả tổng thể:** ⬜ Pass All | ⬜ Pass with Minor Issues | ⬜ Fail
