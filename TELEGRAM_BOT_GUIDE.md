# 🤖 HƯỚNG DẪN TẠO TELEGRAM BOT CHI TIẾT (STEP-BY-STEP)

## 📋 MỤC LỤC
1. [Chuẩn bị](#bước-1-chuẩn-bị)
2. [Tạo Bot với BotFather](#bước-2-tạo-bot-với-botfather)
3. [Lấy Chat ID](#bước-3-lấy-chat-id)
4. [Test Bot bằng Browser](#bước-4-test-bot-bằng-browser)
5. [Tạo Group Chat (Tùy chọn)](#bước-5-tạo-group-chat-tùy-chọn)

---

## 📱 BƯỚC 1: CHUẨN BỊ

### Yêu cầu:
- ✅ Có tài khoản Telegram (mobile hoặc desktop)
- ✅ Đã cài đặt Telegram app
- ✅ Có kết nối Internet

### Download Telegram:
- **Mobile:** App Store (iOS) hoặc Google Play (Android)
- **Desktop:** https://desktop.telegram.org/
- **Web:** https://web.telegram.org/

---

## 🤖 BƯỚC 2: TẠO BOT VỚI BOTFATHER

### 2.1. Mở Telegram và tìm BotFather

**Cách 1: Tìm kiếm**
```
1. Mở Telegram
2. Click vào ô Search (🔍) ở góc trên
3. Gõ: @BotFather
4. Click vào bot có dấu tick xanh ✓ (verified)
```

**Cách 2: Dùng link trực tiếp**
```
Click: https://t.me/BotFather
→ Tự động mở trong Telegram app
```

![BotFather Screenshot](https://core.telegram.org/file/811140934/1/zlN4goPTupk/9ff2f2f01c4bd1b013)

### 2.2. Start conversation với BotFather

```
1. Click nút "START" hoặc "/start" ở dưới cùng
2. BotFather sẽ gửi tin nhắn chào mừng kèm danh sách lệnh
```

**Tin nhắn chào mừng từ BotFather:**
```
I can help you create and manage Telegram bots. If you're new to the Bot API, please see the manual (https://core.telegram.org/bots).

You can control me by sending these commands:

/newbot - create a new bot
/mybots - edit your bots
/setname - change a bot's name
/setdescription - change bot description
...
```

### 2.3. Tạo bot mới

**Bước 1: Gửi lệnh tạo bot**
```
Gõ và gửi: /newbot
```

**Phản hồi từ BotFather:**
```
Alright, a new bot. How are we going to call it? Please choose a name for your bot.
```

**Bước 2: Đặt tên hiển thị cho bot**
```
Gõ và gửi: TTDN Accounting Bot
```

📝 **Lưu ý:** 
- Tên này sẽ hiển thị trong Telegram
- Có thể có dấu cách và ký tự đặc biệt
- Ví dụ: "Kế toán TTDN", "Accounting System", "財務通知"

**Phản hồi từ BotFather:**
```
Good. Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.
```

**Bước 3: Đặt username cho bot**
```
Gõ và gửi: ttdn_accounting_bot
```

📝 **Lưu ý quan trọng về username:**
- ❌ Không có dấu cách
- ❌ Không có ký tự đặc biệt (trừ underscore `_`)
- ✅ Chỉ chữ cái (a-z), số (0-9), underscore (_)
- ✅ **BẮT BUỘC** kết thúc bằng `bot` hoặc `_bot`
- ✅ Phải là duy nhất (chưa ai dùng)

**Ví dụ username hợp lệ:**
```
✅ ttdn_accounting_bot
✅ ttdnaccountingbot
✅ ttdn2026_bot
✅ accounting_ttdn_bot
```

**Ví dụ username KHÔNG hợp lệ:**
```
❌ ttdn_accounting (thiếu _bot)
❌ ttdn-accounting-bot (có dấu gạch ngang)
❌ ttdn accounting bot (có dấu cách)
❌ ttdn@accounting_bot (có ký tự @)
```

### 2.4. Nhận Bot Token

**Nếu username hợp lệ, BotFather sẽ trả về:**
```
Done! Congratulations on your new bot. You will find it at t.me/ttdn_accounting_bot. 
You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a nice surprise for it.

Use this token to access the HTTP API:
7891234567:AAH7qQB9Xl6F8rN2tP-3vKuJ5mW0nXyZaBc

Keep your token secure and store it safely, it can be used by anyone to control your bot.

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
```

### 2.5. Lưu Bot Token

✅ **Copy và lưu token này ngay:**
```
7891234567:AAH7qQB9Xl6F8rN2tP-3vKuJ5mW0nXyZaBc
```

📝 **Cấu trúc Bot Token:**
```
<BOT_ID>:<RANDOM_STRING>

Ví dụ:
7891234567:AAH7qQB9Xl6F8rN2tP-3vKuJ5mW0nXyZaBc
│          │
│          └─ Chuỗi random (API key)
└─ Bot ID (số duy nhất)
```

⚠️ **QUAN TRỌNG:**
- **KHÔNG** chia sẻ token này với người khác
- **KHÔNG** commit vào Git/GitHub
- **KHÔNG** post công khai
- Token này = full control bot của bạn
- Nếu lộ token → Regenerate ngay bằng lệnh `/token` với BotFather

### 2.6. Lưu token vào file an toàn

**Trên Windows:**
```
1. Tạo file: C:\Users\<YourName>\telegram_bot_config.txt
2. Ghi nội dung:
   BOT_TOKEN=7891234567:AAH7qQB9Xl6F8rN2tP-3vKuJ5mW0nXyZaBc
   BOT_USERNAME=@ttdn_accounting_bot
   CREATED_DATE=26/01/2026
```

**Trên Linux/WSL:**
```bash
# Tạo file ẩn trong home directory
echo "BOT_TOKEN=7891234567:AAH7qQB9Xl6F8rN2tP-3vKuJ5mW0nXyZaBc" > ~/.telegram_bot_token
chmod 600 ~/.telegram_bot_token  # Chỉ owner đọc được
```

### 2.7. Tùy chỉnh bot (Tùy chọn)

**Thêm mô tả cho bot:**
```
1. Gửi: /setdescription
2. BotFather hỏi: Choose a bot
3. Click vào: @ttdn_accounting_bot
4. Gõ mô tả:
   "Bot thông báo kế toán tài chính cho hệ thống TTDN. Gửi notification về phiếu thu, phiếu chi, hóa đơn và các giao dịch tài chính."
5. Gửi
```

**Thêm About (giới thiệu ngắn):**
```
1. Gửi: /setabouttext
2. Click bot
3. Gõ: "TTDN Accounting Notification Bot"
4. Gửi
```

**Thêm ảnh đại diện:**
```
1. Gửi: /setuserpic
2. Click bot
3. Gửi ảnh (icon/logo công ty)
```

**Thêm danh sách commands (Menu):**
```
1. Gửi: /setcommands
2. Click bot
3. Gõ danh sách commands (mỗi dòng 1 command):
   start - Khởi động bot
   help - Hướng dẫn sử dụng
   status - Kiểm tra trạng thái kết nối
   today - Xem giao dịch hôm nay
   report - Báo cáo tổng hợp
4. Gửi
```

Sau khi setup, khi user chat với bot và gõ `/`, sẽ hiển thị menu commands này.

---

## 🆔 BƯỚC 3: LẤY CHAT ID

### 3.1. Tìm bot của bạn trong Telegram

**Cách 1: Dùng search**
```
1. Click vào ô Search (🔍)
2. Gõ: @ttdn_accounting_bot
3. Click vào bot (tên hiển thị: "TTDN Accounting Bot")
```

**Cách 2: Dùng link**
```
https://t.me/ttdn_accounting_bot
```

### 3.2. Start bot và gửi tin nhắn

```
1. Click nút "START"
2. Gửi bất kỳ tin nhắn nào, ví dụ:
   - "Hello"
   - "Test"
   - "/start"
```

📝 **Lưu ý:** Bot sẽ KHÔNG trả lời (vì chưa có code xử lý), nhưng tin nhắn đã được ghi nhận.

### 3.3. Lấy Chat ID bằng API "8082274502"

**Cách 1: Dùng trình duyệt (Khuyến nghị)**

```
1. Mở trình duyệt (Chrome, Firefox, Edge...)
2. Paste URL sau vào address bar (thay <TOKEN> bằng token thực):

https://api.telegram.org/bot8573098191:AAH1dVCI5uRqR0_fdPbt5b3abvraJ7Lo3wY/getUpdates

3. Nhấn Enter
```

**Kết quả JSON:**
```json
{
  "ok": true,
  "result": [
    {
      "update_id": 123456789,
      "message": {
        "message_id": 1,
        "from": {
          "id": 987654321,          ← Đây là Chat ID của bạn
          "is_bot": false,
          "first_name": "Nguyễn",
          "last_name": "Văn A",
          "username": "nguyenvana",
          "language_code": "vi"
        },
        "chat": {
          "id": 987654321,          ← Đây là Chat ID (trùng với from.id)
          "first_name": "Nguyễn",
          "last_name": "Văn A",
          "username": "nguyenvana",
          "type": "private"
        },
        "date": 1737910800,
        "text": "Hello"
      }
    }
  ]
}
```

✅ **Lưu Chat ID:** `8082274502`

**Giải thích JSON:**
```
- "ok": true           → API call thành công
- "result": [...]      → Mảng các update (tin nhắn)
- "message.chat.id"    → Chat ID cần lấy
- "type": "private"    → Đây là chat 1-1 (không phải group)
```

**Cách 2: Dùng @userinfobot (Đơn giản hơn)**

```
1. Mở Telegram
2. Search: @userinfobot
3. Click vào bot (có dấu tick xanh)
4. Click START
5. Gửi bất kỳ tin nhắn (hoặc không cần gửi gì)
6. Bot tự động trả lời:

Id: 987654321           ← Đây là Chat ID
First: Nguyễn
Last: Văn A
Username: @nguyenvana
Lang: vi
```

✅ **Lưu Chat ID:** `8082274502`

**Cách 3: Dùng @RawDataBot (Xem raw data)**

```
1. Search: @RawDataBot
2. START
3. Gửi tin nhắn bất kỳ
4. Bot trả về JSON đầy đủ, tìm "id" trong phần "from" hoặc "chat"
```

### 3.4. Lưu Chat ID

**Lưu vào file config:**
```
BOT_TOKEN=7891234567:AAH7qQB9Xl6F8rN2tP-3vKuJ5mW0nXyZaBc
CHAT_ID=987654321
BOT_USERNAME=@ttdn_accounting_bot
CREATED_DATE=26/01/2026
```

---

## 🧪 BƯỚC 4: TEST BOT BẰNG BROWSER

### 4.1. Test gửi tin nhắn đơn giản

**URL:**
```
https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=Hello from browser!

Thay giá trị thực:
https://api.telegram.org/bot7891234567:AAH7qQB9Xl6F8rN2tP-3vKuJ5mW0nXyZaBc/sendMessage?chat_id=987654321&text=Hello from browser!
```

**Bước thực hiện:**
```
1. Copy URL trên (thay token và chat_id thật)
2. Paste vào browser
3. Nhấn Enter
```

**Kết quả:**
- Browser hiển thị JSON: `{"ok":true,"result":{...}}`
- Telegram nhận tin nhắn: "Hello from browser!"

✅ **Nếu nhận được tin nhắn → Bot hoạt động!**

### 4.2. Test gửi tin nhắn với emoji

**URL:**
```
https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=✅ Test thành công!
```

### 4.3. Test gửi tin nhắn với HTML formatting

**URL (encode URL):**
```
https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=<b>Bold</b> <i>Italic</i>&parse_mode=HTML
```

**Kết quả:** Nhận tin nhắn có **Bold** và _Italic_

### 4.4. Test bằng cURL (Terminal)

**Trên Linux/WSL/Mac:**
```bash
curl -X POST "https://api.telegram.org/bot7891234567:AAH7qQB9Xl6F8rN2tP-3vKuJ5mW0nXyZaBc/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{"chat_id": 987654321, "text": "Test from cURL"}'
```

**Trên Windows PowerShell:**
```powershell
Invoke-RestMethod -Uri "https://api.telegram.org/bot7891234567:AAH7qQB9Xl6F8rN2tP-3vKuJ5mW0nXyZaBc/sendMessage" `
  -Method Post `
  -Body (@{chat_id=987654321; text="Test from PowerShell"} | ConvertTo-Json) `
  -ContentType "application/json"
```

### 4.5. Test bằng Python (Nhanh)

**Tạo file test_telegram.py:**
```python
import requests

BOT_TOKEN = "7891234567:AAH7qQB9Xl6F8rN2tP-3vKuJ5mW0nXyZaBc"
CHAT_ID = "987654321"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = {
    "chat_id": CHAT_ID,
    "text": "🚀 Test từ Python script!",
    "parse_mode": "HTML"
}

response = requests.post(url, json=data)
print(response.json())
```

**Chạy:**
```bash
python test_telegram.py
```

---

## 👥 BƯỚC 5: TẠO GROUP CHAT (TÙY CHỌN)

### Tại sao cần Group Chat?
- ✅ Toàn team nhận thông báo
- ✅ Có history log tập trung
- ✅ Có thể thêm nhiều bot vào 1 group
- ✅ Phân quyền thành viên (admin, member)

### 5.1. Tạo Group mới

**Trên Telegram:**
```
1. Click vào Menu (☰) → "New Group"
2. Chọn thành viên đầu tiên (ít nhất 1 người, có thể chọn chính mình)
3. Click "Next" (→)
4. Đặt tên group: "TTDN Accounting Notifications"
5. (Tùy chọn) Thêm ảnh đại diện cho group
6. Click "Create"
```

### 5.2. Thêm bot vào Group

**Cách 1: Thêm trực tiếp**
```
1. Mở Group vừa tạo
2. Click vào tên Group ở trên → "Edit"
3. Click "Add Members"
4. Tìm: @ttdn_accounting_bot
5. Click vào bot → "Add"
```

**Cách 2: Dùng link**
```
1. Trong Group, gõ: @ttdn_accounting_bot
2. Click vào suggestion
3. Click "Add to group"
```

### 5.3. Cấp quyền Admin cho bot (Quan trọng!)

```
1. Mở Group
2. Click tên Group → "Edit"
3. Click "Administrators"
4. Click "Add Administrator"
5. Chọn: @ttdn_accounting_bot
6. Bật các quyền (nếu cần):
   ✅ Change Group Info
   ✅ Delete Messages
   ✅ Ban Users (tùy chọn)
   ✅ Invite Users via Link
   ✅ Pin Messages
   ✅ Manage Video Chats
7. Click "Done"
```

📝 **Lưu ý:** Bot cần quyền admin để đọc tin nhắn trong group (nếu privacy mode bật)

### 5.4. Lấy Group Chat ID

**Bước 1: Gửi tin nhắn trong group**
```
1. Mở group
2. Gõ bất kỳ: "Hello bot!"
3. Hoặc: /start
```

**Bước 2: Gọi API getUpdates**
```
https://api.telegram.org/bot7891234567:AAH7qQB9Xl6F8rN2tP-3vKuJ5mW0nXyZaBc/getUpdates
```

**Kết quả JSON (Group Chat):**
```json
{
  "ok": true,
  "result": [
    {
      "update_id": 123456790,
      "message": {
        "message_id": 2,
        "from": {
          "id": 987654321,
          "first_name": "Nguyễn",
          "username": "nguyenvana"
        },
        "chat": {
          "id": -1001234567890,    ← Group Chat ID (số âm!)
          "title": "TTDN Accounting Notifications",
          "type": "supergroup"      ← Type là supergroup
        },
        "date": 1737911000,
        "text": "Hello bot!"
      }
    }
  ]
}
```

✅ **Lưu Group Chat ID:** `-1001234567890`

📝 **Lưu ý quan trọng:**
- Private chat ID: **Số dương** (VD: 987654321)
- Group chat ID: **Số âm** (VD: -1001234567890)
- Supergroup ID: **Số âm 13 chữ số** (VD: -1001234567890)

### 5.5. Test gửi tin nhắn vào Group

**Browser:**
```
https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=-1001234567890&text=✅ Test group notification!
```

**Python:**
```python
import requests

BOT_TOKEN = "7891234567:AAH7qQB9Xl6F8rN2tP-3vKuJ5mW0nXyZaBc"
GROUP_CHAT_ID = "-1001234567890"  # Số âm

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = {
    "chat_id": GROUP_CHAT_ID,
    "text": "📢 Thông báo gửi đến toàn team!",
    "parse_mode": "HTML"
}

response = requests.post(url, json=data)
print(response.json())
```

---

## 🔐 BẢO MẬT & BEST PRACTICES

### DO ✅
- Lưu token vào file riêng, không commit Git
- Dùng biến môi trường (environment variables)
- Regenerate token nếu bị lộ
- Dùng Group Chat cho team, không share token
- Backup token và chat_id ra file an toàn
- Test trên staging bot trước khi deploy production

### DON'T ❌
- ❌ Commit token vào Git/GitHub
- ❌ Post token lên forum/social media
- ❌ Hard-code token trong source code
- ❌ Dùng chung token cho nhiều môi trường
- ❌ Share token qua email/chat không mã hóa

### Cách lưu token an toàn

**1. Dùng .env file (cho development):**
```bash
# .env
TELEGRAM_BOT_TOKEN=7891234567:AAH7qQB9Xl6F8rN2tP-3vKuJ5mW0nXyZaBc
TELEGRAM_CHAT_ID=987654321
```

```python
# Python code
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
```

**2. Dùng Odoo System Parameters (cho production):**
```
Settings → Technical → System Parameters
Key: telegram_bot_token
Value: <token>
```

**3. Dùng secret management (enterprise):**
- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault
- Google Secret Manager

---

## 🔧 TROUBLESHOOTING

### Lỗi 1: "400 Bad Request: chat not found"

**Nguyên nhân:**
- Chat ID sai
- Chưa start bot
- Bot bị block

**Giải pháp:**
```
1. Mở Telegram → Tìm bot
2. Nhấn START
3. Gửi tin nhắn: "Hello"
4. Lấy lại Chat ID từ getUpdates
5. Kiểm tra: Chat ID có đúng không? (số dương cho private, số âm cho group)
```

### Lỗi 2: "401 Unauthorized"

**Nguyên nhân:** Bot token sai

**Giải pháp:**
```
1. Kiểm tra token có đúng không
2. Có dấu cách thừa không?
3. Copy lại token từ BotFather
4. Nếu lộ token → /revoke với BotFather → Lấy token mới
```

### Lỗi 3: "403 Forbidden: bot was blocked by the user"

**Nguyên nhân:** User đã block bot

**Giải pháp:**
```
1. Mở Telegram
2. Tìm bot
3. Click "Unblock" hoặc "Restart"
4. Gửi /start
```

### Lỗi 4: Group không nhận tin nhắn

**Nguyên nhân:** Bot không có quyền

**Giải pháp:**
```
1. Mở Group → Edit → Administrators
2. Thêm bot làm Admin
3. Bật quyền "Post Messages"
4. Test lại
```

### Lỗi 5: getUpdates trả về `{"ok":true,"result":[]}`

**Nguyên nhân:** Chưa có tin nhắn nào

**Giải pháp:**
```
1. Gửi tin nhắn mới cho bot
2. Refresh browser (F5)
3. Hoặc: Xóa offset bằng cách thêm ?offset=-1
```

---

## 📚 TÀI LIỆU THAM KHẢO

### Official Documentation
- Telegram Bot API: https://core.telegram.org/bots/api
- BotFather Commands: https://core.telegram.org/bots#6-botfather
- Telegram Bot Features: https://core.telegram.org/bots/features

### Useful Bots
- @BotFather - Tạo và quản lý bot
- @userinfobot - Lấy user info (ID, username)
- @RawDataBot - Xem raw JSON data
- @LivegramBot - Monitor bot activity
- @Botlistbot - Tìm bot khác

### Python Libraries
- python-telegram-bot: https://github.com/python-telegram-bot/python-telegram-bot
- aiogram: https://github.com/aiogram/aiogram
- pyTelegramBotAPI: https://github.com/eternnoir/pyTelegramBotAPI

### Tools & Utilities
- Telegram Bot API Tester: https://core.telegram.org/bots/api#making-requests
- Webhook Tester: https://webhook.site/
- JSON Formatter: https://jsonformatter.org/

---

## 📝 CHECKLIST HOÀN THÀNH

Đánh dấu ✅ vào các bước đã hoàn thành:

### Tạo Bot
- [ ] Tìm @BotFather trong Telegram
- [ ] Gửi lệnh /newbot
- [ ] Đặt tên bot (display name)
- [ ] Đặt username bot (phải có _bot)
- [ ] Lưu Bot Token
- [ ] Lưu Bot Username

### Lấy Chat ID
- [ ] Start bot (@ttdn_accounting_bot)
- [ ] Gửi tin nhắn: "Hello"
- [ ] Mở browser: getUpdates API
- [ ] Lấy Chat ID từ JSON
- [ ] Lưu Chat ID
- [ ] (Tùy chọn) Test với @userinfobot

### Test Bot
- [ ] Test gửi tin nhắn qua browser
- [ ] Test gửi tin nhắn qua cURL/PowerShell
- [ ] Test gửi tin nhắn qua Python script
- [ ] Nhận được tin nhắn trong Telegram

### Cấu hình Odoo (Bước tiếp theo)
- [ ] Mở Settings → Technical → System Parameters
- [ ] Tạo parameter: telegram_bot_token
- [ ] Tạo parameter: telegram_chat_id
- [ ] Cài thư viện: pip install requests
- [ ] Upgrade module: quan_ly_tai_chinh
- [ ] Test gửi notification từ Odoo

### Group Chat (Tùy chọn)
- [ ] Tạo group mới
- [ ] Thêm bot vào group
- [ ] Cấp quyền admin cho bot
- [ ] Lấy Group Chat ID (số âm)
- [ ] Test gửi tin nhắn vào group

---

## 🎯 BƯỚC TIẾP THEO

Sau khi hoàn thành hướng dẫn này, bạn đã có:
- ✅ Bot Token
- ✅ Chat ID (hoặc Group Chat ID)

**Tiếp theo, làm theo file TELEGRAM_SETUP.md để:**
1. Cài thư viện `requests` trong Odoo
2. Cấu hình System Parameters
3. Upgrade module
4. Test gửi notification từ Odoo

**File liên quan:**
- `TELEGRAM_SETUP.md` - Hướng dẫn tích hợp vào Odoo
- `telegram_helper.py` - Code helper để gửi notification

---

**Tác giả:** GitHub Copilot  
**Phiên bản:** 2.0 (Chi tiết)  
**Ngày cập nhật:** 26/01/2026  
**Thời gian đọc:** ~15 phút  
**Độ khó:** ⭐⭐☆☆☆ (Dễ)
