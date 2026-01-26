# 🤖 AI ASSISTANT - HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG

## Tổng Quan

**TTDN AI Assistant** là trợ lý ảo thông minh được tích hợp OpenAI GPT-4 vào Telegram Bot, giúp bạn tương tác với hệ thống ERP Odoo bằng ngôn ngữ tự nhiên.

### Tính Năng Chính

✅ **Hiểu ngôn ngữ tự nhiên** - Không cần nhớ lệnh cứng nhắc
✅ **Trả lời thông minh** - AI phân tích và đưa ra câu trả lời chính xác
✅ **Function Calling** - Tự động gọi các hàm Odoo để lấy dữ liệu
✅ **Context-aware** - Nhớ cuộc hội thoại trước đó
✅ **Multi-domain** - Tra cứu tài sản, nhân sự, tài chính, văn bản

---

## 📋 Yêu Cầu Hệ Thống

- Python 3.10+
- Odoo 15
- OpenAI API Key (từ https://platform.openai.com)
- Telegram Bot Token
- Module `quan_ly_tai_chinh` đã cài đặt

---

## 🚀 Cài Đặt

### Bước 1: Cài Dependencies

```bash
cd /home/nghiax/TTDN-16-01-N5

# Kích hoạt virtual environment
source venv/bin/activate

# Cài thư viện OpenAI
pip install openai==1.6.1 tiktoken==0.5.2
```

### Bước 2: Lấy OpenAI API Key

1. Truy cập https://platform.openai.com/api-keys
2. Đăng nhập hoặc tạo tài khoản
3. Click "Create new secret key"
4. Copy API key (dạng: `sk-proj-xxxxxxxxxxxxx`)
5. **Lưu lại** - chỉ hiển thị 1 lần!

**Chi phí sử dụng:**
- GPT-3.5-turbo: ~$0.002/query (rất rẻ, đủ dùng)
- GPT-4-turbo: ~$0.02/query (đắt hơn nhưng thông minh hơn)

### Bước 3: Cấu Hình Odoo

#### 3.1. Update Module

```bash
# Upgrade module với AI features mới
python3 odoo-bin.py -c odoo.conf -u quan_ly_tai_chinh --stop-after-init
```

#### 3.2. Cấu Hình OpenAI trong Odoo

1. **Đăng nhập Odoo** (http://localhost:8069)
2. Vào **Settings** → **Technical** → **Parameters** → **System Parameters**
3. Tìm và cập nhật các tham số:

| Key | Value | Mô tả |
|-----|-------|-------|
| `openai.api_key` | `sk-proj-xxxxxxxx` | API key từ OpenAI |
| `openai.model` | `gpt-3.5-turbo` | Model sử dụng (hoặc `gpt-4-turbo`) |
| `openai.enabled` | `True` | Bật/tắt AI |
| `openai.max_tokens` | `1500` | Giới hạn tokens response |
| `openai.temperature` | `0.7` | Độ sáng tạo (0.0-2.0) |

**Screenshot mẫu:**
```
Name: openai.api_key
Value: sk-proj-abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNO
```

### Bước 4: Khởi Động Telegram Bot

```bash
# Chạy bot trong WSL
wsl -d Ubuntu-22.04 -e bash -lc "cd /home/nghiax/TTDN-16-01-N5 && source venv/bin/activate && bash start_telegram_bot.sh"
```

Hoặc chạy trực tiếp trong WSL:

```bash
cd /home/nghiax/TTDN-16-01-N5
source venv/bin/activate
python3 addons/quan_ly_tai_chinh/telegram_bot_polling.py
```

**Thông báo thành công:**
```
INFO - Starting Telegram bot polling for chat 123456789
INFO - Bot is running. Press Ctrl+C to stop.
```

---

## 💬 Cách Sử Dụng

### Giao Tiếp Tự Nhiên

**Trước đây (Bot cũ):**
```
/stats              ← Phải nhớ lệnh
/taisan             ← Cố định
tra tai san: laptop ← Cú pháp đặc biệt
```

**Bây giờ (AI Assistant):**
```
Hôm nay có bao nhiêu giao dịch?
Tìm laptop phòng IT giá trên 10 triệu
So sánh thu chi tháng này với tháng trước
Tài sản nào sắp hết khấu hao?
Có bao nhiêu nhân viên phòng kế toán?
Số dư quỹ hiện tại là bao nhiêu?
```

### Ví Dụ Hội Thoại

#### 1. Tra Cứu Tài Sản

```
👤 User: Cho tôi xem tài sản phòng IT có giá trên 20 triệu

🤖 Bot: 📊 Tìm thấy 3 tài sản phòng IT có giá trên 20 triệu:

1. 💻 <b>Laptop Dell XPS 15</b> (TS/2024/0123)
   • Giá mua: 25,000,000 VNĐ
   • Giá hiện tại: 20,000,000 VNĐ
   • Ngày mua: 15/03/2024
   • Trạng thái: Đang sử dụng

2. 🖥️ <b>iMac 27"</b> (TS/2024/0087)
   • Giá mua: 45,000,000 VNĐ
   • Giá hiện tại: 38,000,000 VNĐ
   • Ngày mua: 10/02/2024
   • Trạng thái: Đang sử dụng

3. 🖨️ <b>Máy in HP LaserJet</b> (TS/2023/0234)
   • Giá mua: 22,000,000 VNĐ
   • Giá hiện tại: 15,000,000 VNĐ
   • Ngày mua: 05/09/2023
   • Trạng thái: Đang sử dụng

💰 <b>Tổng giá trị:</b>
   • Ban đầu: 92,000,000 VNĐ
   • Hiện tại: 73,000,000 VNĐ

Bạn muốn xem chi tiết tài sản nào không?
```

#### 2. Phân Tích Tài Chính

```
👤 User: Giao dịch tháng này thế nào?

🤖 Bot: 📊 <b>Báo Cáo Tài Chính Tháng 01/2026</b>

💰 <b>Thu nhập:</b>
   • Tổng thu: 150,000,000 VNĐ
   • Số phiếu thu: 15 phiếu
   • Trung bình/phiếu: 10,000,000 VNĐ

💸 <b>Chi phí:</b>
   • Tổng chi: 98,000,000 VNĐ
   • Số phiếu chi: 23 phiếu
   • Trung bình/phiếu: 4,260,870 VNĐ

📈 <b>Kết quả:</b>
   • Chênh lệch: +52,000,000 VNĐ ✅
   • Tỷ lệ lợi nhuận: 34.67%

💡 <b>Nhận xét:</b> Tình hình tài chính tốt! Thu vượt chi 52 triệu đồng.

Bạn muốn xem chi tiết các khoản thu/chi không?
```

#### 3. Context-Aware (Nhớ Hội Thoại)

```
👤 User: Tìm laptop Dell

🤖 Bot: Tìm thấy 2 laptop Dell:
1. Dell XPS 15 - 25 triệu
2. Dell Inspiron - 15 triệu

👤 User: Cái thứ nhất đã khấu hao bao nhiêu?

🤖 Bot: Laptop Dell XPS 15 (TS/2024/0123):
• Giá mua: 25,000,000 VNĐ
• Đã khấu hao: 5,000,000 VNĐ
• Còn lại: 20,000,000 VNĐ
• Phương pháp: Tuyến tính
• Thời gian: 10/48 tháng

👤 User: Nó được mua khi nào?

🤖 Bot: Laptop Dell XPS 15 được mua ngày 15/03/2024
Đã sử dụng được 10 tháng.
```

---

## 🎯 Các Tính Năng AI

### 1. Tra Cứu Tài Sản

**Các câu hỏi AI có thể trả lời:**
- "Tài sản nào có giá trên X triệu?"
- "Tìm laptop/máy tính/thiết bị ở phòng Y"
- "Tài sản nào đã thanh lý?"
- "Cho xem danh sách tài sản mua năm 2024"

### 2. Giao Dịch Thu/Chi

**Ví dụ:**
- "Hôm nay có bao nhiêu giao dịch?"
- "Tổng thu tháng này là bao nhiêu?"
- "Phiếu chi nào trên 10 triệu trong tháng 12?"
- "So sánh thu chi Q1 và Q2"

### 3. Nhân Sự

**Ví dụ:**
- "Có bao nhiêu nhân viên phòng IT?"
- "Tìm nhân viên tên Nguyễn Văn A"
- "Ai là trưởng phòng kế toán?"

### 4. Số Dư Quỹ

**Ví dụ:**
- "Số dư quỹ hiện tại?"
- "Tiền mặt còn bao nhiêu?"
- "Tài khoản ngân hàng có bao nhiêu?"

### 5. Thống Kê Tổng Quan

**Ví dụ:**
- "Thống kê hệ thống"
- "Tổng quan tài sản"
- "Báo cáo tài chính tháng này"

---

## ⚙️ Tùy Chỉnh Nâng Cao

### Thay Đổi Model AI

**GPT-3.5-turbo** (Khuyến nghị - Rẻ & Nhanh):
- Chi phí: ~$0.002/query
- Tốc độ: Nhanh
- Phù hợp: Tra cứu đơn giản

**GPT-4-turbo** (Thông Minh Hơn):
- Chi phí: ~$0.02/query
- Tốc độ: Chậm hơn
- Phù hợp: Phân tích phức tạp

Cập nhật trong Odoo:
```
Settings → Technical → System Parameters
Key: openai.model
Value: gpt-4-turbo  (hoặc gpt-3.5-turbo)
```

### Điều Chỉnh Temperature

Temperature = Độ sáng tạo của AI (0.0 - 2.0)

- **0.0 - 0.3**: Câu trả lời chính xác, ít sáng tạo (dùng cho tra cứu)
- **0.7**: Cân bằng (mặc định)
- **1.0 - 2.0**: Sáng tạo, đa dạng (dùng cho gợi ý, phân tích)

### Xóa Lịch Sử Hội Thoại

Nếu AI nhầm lẫn vì context cũ:

```
/clear
```

hoặc

```
/reset
```

---

## 🐛 Xử Lý Lỗi

### Lỗi 1: "Chưa cấu hình OpenAI API key"

**Nguyên nhân:** Chưa set API key trong Odoo

**Giải pháp:**
1. Vào Odoo → Settings → Technical → System Parameters
2. Tìm `openai.api_key`
3. Nhập API key từ OpenAI

### Lỗi 2: "OpenAI API key không hợp lệ"

**Nguyên nhân:** API key sai hoặc hết hạn

**Giải pháp:**
1. Kiểm tra lại API key
2. Tạo key mới tại https://platform.openai.com/api-keys
3. Cập nhật trong Odoo

### Lỗi 3: "Đã vượt quá giới hạn request"

**Nguyên nhân:** Vượt quota OpenAI (miễn phí có giới hạn)

**Giải pháp:**
1. Chờ 1 phút rồi thử lại
2. Nạp tiền vào tài khoản OpenAI ($5-10 là đủ dùng lâu)

### Lỗi 4: Bot không phản hồi

**Kiểm tra:**

```bash
# Xem log bot
cd /home/nghiax/TTDN-16-01-N5
cat telegram_bot.log
```

**Fallback:** Nếu AI fail, bot tự động chuyển về chế độ rule-based (lệnh cũ vẫn dùng được)

---

## 📊 Monitor Chi Phí OpenAI

### Xem Usage

1. Truy cập https://platform.openai.com/usage
2. Xem chi tiết usage theo ngày/model
3. Set usage limit để tránh vượt ngân sách

### Ước Tính Chi Phí

**GPT-3.5-turbo:**
- 100 câu hỏi/ngày = $0.20/ngày = $6/tháng
- 500 câu hỏi/ngày = $1/ngày = $30/tháng

**Tiết kiệm:**
- Sử dụng GPT-3.5 cho query đơn giản
- Chỉ dùng GPT-4 khi cần phân tích sâu

---

## 🔒 Bảo Mật

### Best Practices

✅ **Không share API key** - Cực kỳ quan trọng!
✅ **Giới hạn chat_id** - Chỉ admin mới dùng được bot
✅ **Monitor usage** - Kiểm tra hàng ngày
✅ **Set usage limit** - Tránh vượt ngân sách
✅ **Không gửi dữ liệu nhạy cảm** - AI không lưu lại nhưng vẫn cẩn thận

### Data Privacy

- OpenAI **không lưu trữ** dữ liệu từ API (theo policy)
- Conversation history được lưu **in-memory** trên server Odoo
- Dữ liệu không được gửi đến bên thứ 3

---

## 🆘 Hỗ Trợ

### Debug Mode

Bật logging chi tiết:

```python
# Trong telegram_bot_polling.py
logging.basicConfig(level=logging.DEBUG)
```

### Test AI Trực Tiếp

Test trong Odoo Shell:

```bash
python3 odoo-bin.py shell -c odoo.conf
```

```python
# Trong shell
env['ai.assistant'].process_message(
    "Có bao nhiêu tài sản?", 
    "test_chat", 
    "Admin"
)
```

### Contact

- File bug: Tạo issue trong project
- Email support: [your-email]
- Telegram: [your-telegram]

---

## 📈 Roadmap

### Đang Phát Triển

- [ ] Voice input (gửi voice note)
- [ ] Tạo báo cáo PDF/Excel tự động
- [ ] Gửi biểu đồ/chart
- [ ] Notifications chủ động
- [ ] Multi-language support

### Đã Hoàn Thành

- [x] OpenAI GPT-4 integration
- [x] Function calling với Odoo
- [x] Context-aware conversation
- [x] Fallback to rule-based
- [x] Error handling

---

## 📝 Changelog

### Version 1.0.0 (27/01/2026)

**Tính năng mới:**
- Tích hợp OpenAI GPT-3.5/GPT-4
- Function calling: get_assets, get_transactions, get_employees, get_cash_balance, get_statistics
- Conversation history management
- Auto fallback to rule-based bot
- Configurable via Odoo System Parameters

**Cải thiện:**
- Telegram bot polling với AI processing
- Better error handling
- Vietnamese language optimization

---

## 🎓 Tips & Tricks

### Hỏi Hiệu Quả

**✅ Tốt:**
- "Tìm laptop phòng IT giá trên 20 triệu"
- "Giao dịch tháng 12 năm 2024"

**❌ Không tốt:**
- "Có gì không?" (quá chung chung)
- "Cho tôi tất cả" (quá rộng)

### Sử Dụng Context

Thay vì hỏi lại từ đầu:

```
❌ Không hiệu quả:
User: Tìm tài sản phòng IT
Bot: [Danh sách 10 tài sản]
User: Tìm tài sản phòng IT giá trên 20 triệu

✅ Hiệu quả:
User: Tìm tài sản phòng IT
Bot: [Danh sách 10 tài sản]
User: Lọc những cái trên 20 triệu  ← AI hiểu context
```

---

**Chúc bạn sử dụng AI Assistant hiệu quả! 🚀**
