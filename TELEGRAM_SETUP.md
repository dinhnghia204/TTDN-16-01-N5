# HƯỚNG DẪN TÍCH HỢP TELEGRAM BOT
# trang debug ds=1&menu_id=4&action=12&model=ir.config_parameter&view_type=list
## 📱 BƯỚC 1: TẠO TELEGRAM BOT

### 1.1. Tạo bot mới với BotFather

1. Mở Telegram, tìm và chat với **@BotFather**
2. Gửi lệnh: `/newbot`
3. Đặt tên bot: `TTDN Accounting Bot` (hoặc tên tùy thích)
4. Đặt username: `ttdn_accounting_bot` (phải kết thúc bằng `_bot`)

**BotFather sẽ trả về:**
```
Done! Congratulations on your new bot. You will find it at t.me/ttdn_accounting_bot. 

Use this token to access the HTTP API:
8573098191:AAH1dVCI5uRqR0_fdPbt5b3abvraJ7Lo3wY

Keep your token secure and store it safely, it can be used by anyone to control your bot.
```

✅ **Lưu lại BOT TOKEN:** `8573098191:AAH1dVCI5uRqR0_fdPbt5b3abvraJ7Lo3wY`

### 1.2. Lấy Chat ID

**Cách 1: Dùng bot @userinfobot**
1. Tìm bot **@userinfobot** trong Telegram
2. Gửi tin nhắn bất kỳ
3. Bot sẽ trả về `Your ID: 123456789`

**Cách 2: Gửi tin nhắn cho bot và dùng API**
1. Tìm bot của bạn trong Telegram (search: `@ttdn_accounting_bot`)
2. Nhấn **Start** và gửi tin nhắn: `Hello`
3. Mở trình duyệt, truy cập:
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
```
Thay `<YOUR_BOT_TOKEN>` bằng token vừa lấy

4. Trong JSON response, tìm:
```json
{
  "message": {
    "chat": {
      "id": 123456789,  ← Đây là Chat ID
      "first_name": "Your Name",
      "type": "private"
    }
  }
}
```

✅ **Lưu lại CHAT ID:** `8082274502`

---

## 🔧 BƯỚC 2: CẤU HÌNH ODOO

### 2.1. Truy cập Settings

```
Menu: Settings → Technical → Parameters → System Parameters
```

**Lưu ý:** Phải bật **Developer Mode** trước:
```
Settings → Activate Developer Mode
```

### 2.2. Thêm 2 tham số mới

**Tham số 1: Telegram Bot Token**
- Click: **Create**
- Key: `telegram_bot_token`
- Value: `8573098191:AAH1dVCI5uRqR0_fdPbt5b3abvraJ7Lo3wY`
- Click: **Save**

**Tham số 2: Telegram Chat ID**
- Click: **Create**
- Key: `telegram_chat_id`
- Value: `8082274502`
- Click: **Save**

![System Parameters Example](https://i.imgur.com/example.png)

---

## 🚀 BƯỚC 3: CÀI ĐẶT PYTHON LIBRARY

Module cần thư viện `requests` để gọi Telegram API.

### 3.1. Cài đặt trong virtual environment

```bash
cd /home/nghiax/TTDN-16-01-N5
source venv/bin/activate
pip install requests
```

### 3.2. Kiểm tra đã cài đặt

```bash
pip show requests
```

**Output mong đợi:**
```
Name: requests
Version: 2.31.0
Summary: Python HTTP for Humans.
```

---

## ✅ BƯỚC 4: UPGRADE MODULE VÀ TEST

### 4.1. Upgrade module

```bash
cd ~/TTDN-16-01-N5
source venv/bin/activate
python3 odoo-bin.py -c odoo.conf -d odoo -u quan_ly_tai_chinh --stop-after-init
```

### 4.2. Restart Odoo server

```bash
# Stop server cũ (Ctrl+C trong terminal đang chạy Odoo)
# Hoặc:
pkill -f odoo-bin

# Start lại
python3 odoo-bin.py -c odoo.conf
```

### 4.3. Test gửi thông báo

**Test 1: Tạo Phiếu thu**
```
Menu: Tài chính/Kế toán → Quỹ tiền → Phiếu thu
Create → Fill form → Click "Xác nhận thu"
```

✅ **Kết quả mong đợi:**
- Odoo hiển thị notification bình thường
- **Telegram nhận tin nhắn:**
  ```
  ✅ 💰 Phiếu thu
  
  Đã xác nhận phiếu thu PT/2026/0001
  Số tiền: 5,000,000 VNĐ
  Người nộp: Nguyễn Văn A
  
  🕐 26/01/2026 20:30:15
  ```

**Test 2: Ghi nhận mua tài sản**
```
Menu: Quản lý tài sản → Tài sản → Open asset
Click: "Ghi nhận mua tài sản"
```

✅ **Kết quả:** Nhận thông báo Telegram với icon ✅

**Test 3: Thanh lý tài sản**
```
Menu: Thanh lý tài sản → Open form
Click: "Ghi nhận thanh lý"
```

✅ **Kết quả:** Nhận thông báo với icon ✅

---

## 🎨 BƯỚC 5: TÙY CHỈNH NÂNG CAO (TÙY CHỌN)

### 5.1. Thêm ảnh vào thông báo

Sửa file `telegram_helper.py`:

```python
def send_photo(self, photo_url, caption):
    """Gửi ảnh với caption"""
    try:
        url = f"{self.api_url}/sendPhoto"
        data = {
            'chat_id': self.chat_id,
            'photo': photo_url,
            'caption': caption,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, json=data, timeout=5)
        response.raise_for_status()
        return True
    except Exception as e:
        _logger.error(f"Failed to send photo: {str(e)}")
        return False
```

### 5.2. Tạo nhóm Telegram để nhận thông báo team

1. Tạo group Telegram: "TTDN Accounting Notifications"
2. Thêm bot vào group: Search `@ttdn_accounting_bot` → Add to group
3. Lấy Group Chat ID:
   - Gửi tin nhắn trong group: `/start`
   - Truy cập: `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Tìm `"chat":{"id":-1001234567890}` (số âm cho group)
   - Update System Parameter `telegram_chat_id` = `-1001234567890`

### 5.3. Tạo inline keyboard (nút bấm)

```python
def send_notification_with_buttons(self, title, message, buttons):
    """
    Gửi notification với nút bấm
    
    Args:
        buttons: List of [{'text': 'Xem chi tiết', 'url': 'http://...'}]
    """
    keyboard = {
        'inline_keyboard': [[btn] for btn in buttons]
    }
    
    url = f"{self.api_url}/sendMessage"
    data = {
        'chat_id': self.chat_id,
        'text': f"<b>{title}</b>\n\n{message}",
        'parse_mode': 'HTML',
        'reply_markup': keyboard
    }
    
    response = requests.post(url, json=data, timeout=5)
    return response.ok
```

**Sử dụng:**
```python
telegram_bot.send_notification_with_buttons(
    title='Phiếu thu mới',
    message='PT/2026/0001 - 5,000,000 VNĐ',
    buttons=[
        {'text': '📄 Xem chi tiết', 'url': 'http://localhost:8069/web#id=1&model=phieu_thu'},
        {'text': '💰 Xem sổ quỹ', 'url': 'http://localhost:8069/web#menu_id=123'}
    ]
)
```

---

## 🔍 TROUBLESHOOTING

### Lỗi 1: "Telegram bot not configured"

**Nguyên nhân:** Thiếu System Parameters

**Giải pháp:**
1. Kiểm tra Settings → Technical → System Parameters
2. Đảm bảo có đúng 2 keys:
   - `telegram_bot_token`
   - `telegram_chat_id`

### Lỗi 2: "Failed to send Telegram message: 401 Unauthorized"

**Nguyên nhân:** Bot token sai

**Giải pháp:**
1. Kiểm tra lại token từ @BotFather
2. Copy chính xác, không có khoảng trắng
3. Update lại System Parameter

### Lỗi 3: "Failed to send Telegram message: 400 Bad Request: chat not found"

**Nguyên nhân:** Chat ID sai hoặc chưa start bot

**Giải pháp:**
1. Mở Telegram, tìm bot
2. Nhấn **Start** và gửi tin nhắn bất kỳ
3. Lấy lại Chat ID theo hướng dẫn ở Bước 1.2

### Lỗi 4: "ModuleNotFoundError: No module named 'requests'"

**Nguyên nhân:** Chưa cài thư viện requests

**Giải pháp:**
```bash
source venv/bin/activate
pip install requests
```

### Lỗi 5: Không nhận được thông báo

**Checklist:**
- [ ] Bot token đúng?
- [ ] Chat ID đúng?
- [ ] Đã /start bot trong Telegram?
- [ ] Thư viện requests đã cài?
- [ ] Module đã upgrade?
- [ ] Odoo server đã restart?

**Debug:**
```bash
# Xem log Odoo
tail -f /var/log/odoo/odoo.log

# Hoặc trong terminal đang chạy Odoo, tìm dòng:
# "Telegram message sent successfully to chat 123456789"
```

---

## 📊 THỐNG KÊ SỬ DỤNG

### Kiểm tra số tin nhắn bot đã gửi

```python
# Trong Odoo shell (python3 odoo-bin.py shell -c odoo.conf -d odoo)
from odoo.addons.quan_ly_tai_chinh.models.telegram_helper import get_telegram_bot

env = api.Environment.manage()
telegram_bot = get_telegram_bot(env)

if telegram_bot:
    # Test gửi tin
    telegram_bot.send_notification(
        title='🧪 Test notification',
        message='Hệ thống đang hoạt động bình thường',
        notification_type='info'
    )
```

---

## 🎯 CÁC THÔNG BÁO ĐÃ TÍCH HỢP

| Chức năng | Icon | Trạng thái |
|-----------|------|-----------|
| Phiếu thu | 💰 | ✅ Đã tích hợp |
| Phiếu chi | 💸 | ⬜ Chưa tích hợp |
| Hóa đơn bán | 🧾 | ⬜ Chưa tích hợp |
| Hóa đơn mua | 📄 | ⬜ Chưa tích hợp |
| Mua tài sản | 🖥️ | ⬜ Chưa tích hợp |
| Thanh lý tài sản | ♻️ | ⬜ Chưa tích hợp |
| Lương nhân viên | 💵 | ⬜ Chưa tích hợp |
| Khấu hao tự động | 📉 | ⬜ Chưa tích hợp |

---

## 📝 GHI CHÚ BẢO MẬT

1. **KHÔNG** commit bot token vào Git
2. **KHÔNG** share bot token công khai
3. Nên dùng group chat thay vì personal chat để toàn team nhận thông báo
4. Có thể tạo nhiều bot cho môi trường khác nhau:
   - Bot production: `@company_accounting_bot`
   - Bot staging: `@company_accounting_test_bot`

---

**Tác giả:** GitHub Copilot  
**Phiên bản:** 1.0  
**Ngày cập nhật:** 26/01/2026
