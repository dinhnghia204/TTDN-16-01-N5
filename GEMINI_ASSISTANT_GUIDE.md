# 🤖 AI ASSISTANT - HƯỚNG DẪN CÀI ĐẶT VỚI GOOGLE GEMINI

## Tổng Quan

**TTDN AI Assistant** sử dụng **Google Gemini 1.5** - AI thế hệ mới của Google, miễn phí và mạnh mẽ!

### Tại Sao Chọn Gemini?

| Tính năng | Google Gemini | OpenAI GPT |
|-----------|---------------|------------|
| **Chi phí** | **MIỄN PHÍ** (15 req/min) | $0.002/query |
| **Model** | Gemini 1.5 Flash/Pro | GPT-3.5/4 |
| **Context** | **1M tokens** | 16K-128K |
| **Tốc độ** | **Rất nhanh** | Nhanh |
| **Tiếng Việt** | Xuất sắc | Tốt |
| **Function Calling** | ✅ | ✅ |

**Gemini 1.5 Flash = Miễn phí + Cực nhanh + Context cực lớn!**

---

## 📋 Yêu Cầu Hệ Thống

- Python 3.10+
- Odoo 15
- Google Gemini API Key (MIỄN PHÍ từ https://aistudio.google.com)
- Telegram Bot Token
- Module `quan_ly_tai_chinh` đã cài đặt

---

## 🚀 Cài Đặt

### Bước 1: Cài Dependencies

```bash
cd /home/nghiax/TTDN-16-01-N5

# Kích hoạt virtual environment
source venv/bin/activate

# Cài thư viện Google Gemini (version mới nhất)
pip install google-generativeai>=0.8.0
```

### Bước 2: Lấy Gemini API Key (MIỄN PHÍ)

1. Truy cập https://aistudio.google.com/app/apikey
2. Đăng nhập bằng Google Account
3. Click **"Get API Key"** → **"Create API key in new project"**
4. Copy API key (dạng: `AIzaSyXXXXXXXXXXXXXXXX`)
5. **Lưu lại** - có thể xem lại sau!

**Quota miễn phí:**
- 15 requests/phút
- 1,500 requests/ngày
- 1,500,000 requests/tháng
- **HOÀN TOÀN MIỄN PHÍ!**

### Bước 3: Cấu Hình Odoo

#### 3.1. Update Module

```bash
# Upgrade module với Gemini features
python3 odoo-bin.py -c odoo.conf -u quan_ly_tai_chinh --stop-after-init
```

#### 3.2. Cấu Hình Gemini trong Odoo

1. **Đăng nhập Odoo** (http://localhost:8069)
2. Vào **Settings** → **Technical** → **Parameters** → **System Parameters**
3. Tìm và cập nhật các tham số:

| Key | Value | Mô tả |
|-----|-------|-------|
| `gemini.api_key` | `AIzaSyXXXXXXXXXX` | API key từ Google |
| `gemini.model` | `gemini-1.5-flash` | Model sử dụng (hoặc `gemini-1.5-pro`) |
| `gemini.enabled` | `True` | Bật/tắt AI |
| `gemini.temperature` | `0.7` | Độ sáng tạo (0.0-2.0) |

**Screenshot mẫu:**
```
Name: gemini.api_key
Value: AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz1234567
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

### Ví Dụ Hội Thoại Thực Tế

#### 1. Tra Cứu Tài Sản

```
👤 User: Tìm laptop phòng IT giá trên 20 triệu

🤖 Gemini: 📊 Tìm thấy 3 tài sản phòng IT có giá trên 20 triệu:

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

💰 <b>Tổng giá trị:</b> 92 triệu → 73 triệu (hiện tại)

Bạn muốn biết thêm thông tin gì không?
```

#### 2. Phân Tích Tài Chính

```
👤 User: So sánh thu chi tháng này với tháng trước

🤖 Gemini: 📊 <b>So Sánh Thu Chi</b>

<b>Tháng 01/2026:</b>
💰 Thu: 150,000,000 VNĐ
💸 Chi: 98,000,000 VNĐ
📈 Chênh lệch: +52,000,000 VNĐ

<b>Tháng 12/2025:</b>
💰 Thu: 120,000,000 VNĐ
💸 Chi: 110,000,000 VNĐ
📈 Chênh lệch: +10,000,000 VNĐ

<b>So sánh:</b>
✅ Thu tăng: 30 triệu (+25%)
✅ Chi giảm: 12 triệu (-11%)
🎉 Lợi nhuận tăng: 42 triệu (+420%)

<b>Nhận xét:</b> Tình hình kinh doanh cải thiện đáng kể! 
Tháng này hiệu quả hơn rất nhiều so với tháng trước.

Bạn muốn xem chi tiết các khoản thu/chi không?
```

#### 3. Context-Aware (Nhớ Hội Thoại)

```
👤 User: Tìm laptop Dell

🤖 Gemini: Tìm thấy 2 laptop Dell:
1. Dell XPS 15 - 25 triệu
2. Dell Inspiron - 15 triệu

👤 User: Cái đầu đã khấu hao bao nhiêu?

🤖 Gemini: Dell XPS 15 (TS/2024/0123):
• Giá mua: 25,000,000 VNĐ
• Đã khấu hao: 5,000,000 VNĐ (20%)
• Còn lại: 20,000,000 VNĐ
• Phương pháp: Tuyến tính - 48 tháng
• Đã dùng: 10 tháng

👤 User: Nó ở phòng nào?

🤖 Gemini: Laptop Dell XPS 15 hiện đang được sử dụng tại <b>Phòng IT</b>.
```

---

## 🎯 Các Tính Năng AI

### Gemini Có Thể Làm Gì?

✅ **Tra cứu thông minh**
- "Tài sản nào giá trên X triệu?"
- "Laptop ở phòng IT"
- "Tài sản mua năm 2024"

✅ **Phân tích tài chính**
- "Hôm nay có bao nhiêu giao dịch?"
- "So sánh thu chi các tháng"
- "Phiếu chi lớn nhất tháng này"

✅ **Thống kê nhân sự**
- "Có bao nhiêu nhân viên phòng IT?"
- "Tìm nhân viên tên Nguyễn"
- "Ai là trưởng phòng?"

✅ **Báo cáo tự động**
- "Tổng quan hệ thống"
- "Báo cáo tài chính tháng này"
- "Tình hình tài sản"

✅ **Context-aware**
- Nhớ cuộc hội thoại trước
- Hiểu đại từ "nó", "cái đó"
- Trả lời liên tục logic

---

## ⚙️ Tùy Chỉnh

### Chọn Model Gemini

**Gemini 1.5 Flash** (Khuyến nghị - Miễn phí & Nhanh):
- Tốc độ: Cực nhanh
- Chi phí: MIỄN PHÍ
- Phù hợp: Mọi tác vụ

**Gemini 1.5 Pro** (Thông Minh Hơn):
- Tốc độ: Nhanh
- Chi phí: MIỄN PHÍ (quota thấp hơn)
- Phù hợp: Phân tích phức tạp

Cập nhật trong Odoo:
```
Settings → Technical → System Parameters
Key: gemini.model
Value: gemini-1.5-pro  (hoặc gemini-1.5-flash)
```

### Điều Chỉnh Temperature

Temperature = Độ sáng tạo (0.0 - 2.0)

- **0.0 - 0.3**: Chính xác, ít sáng tạo
- **0.7**: Cân bằng (mặc định)
- **1.0 - 2.0**: Sáng tạo, đa dạng

---

## 🐛 Xử Lý Lỗi

### Lỗi 1: "Chưa cấu hình Gemini API key"

**Giải pháp:**
1. Vào Odoo → Settings → Technical → System Parameters
2. Tìm `gemini.api_key`
3. Nhập API key từ Google

### Lỗi 2: "Gemini API key không hợp lệ"

**Giải pháp:**
1. Kiểm tra API key tại https://aistudio.google.com/app/apikey
2. Tạo key mới nếu cần
3. Cập nhật trong Odoo

### Lỗi 3: "Vượt quota" (Resource exhausted)

**Giải pháp:**
- Chờ 1 phút (reset rate limit)
- Giảm số request/phút
- Quota reset mỗi phút/ngày

### Lỗi 4: Bot không phản hồi

**Kiểm tra log:**
```bash
cd /home/nghiax/TTDN-16-01-N5
tail -f telegram_bot.log
```

---

## 💰 Chi Phí (MIỄN PHÍ!)

### Quota Miễn Phí

**Gemini 1.5 Flash:**
- 15 requests/phút
- 1,500 requests/ngày
- 1,500,000 requests/tháng
- **Context**: 1 triệu tokens

**Gemini 1.5 Pro:**
- 2 requests/phút
- 50 requests/ngày
- **Context**: 2 triệu tokens

### So Sánh Chi Phí

| Sử dụng | Gemini | ChatGPT |
|---------|--------|---------|
| 100 câu/ngày | **FREE** | $6/tháng |
| 500 câu/ngày | **FREE** | $30/tháng |
| 1000 câu/ngày | **FREE** | $60/tháng |

**→ Tiết kiệm 100%!** 🎉

---

## 🔒 Bảo Mật

### Best Practices

✅ **Không share API key**
✅ **Giới hạn chat_id** - Chỉ admin
✅ **Monitor usage** - Kiểm tra quota
✅ **Cẩn thận dữ liệu nhạy cảm**

### Data Privacy

- Google **không lưu trữ** dữ liệu từ API
- Conversation history trong server Odoo
- Không gửi đến bên thứ 3

---

## 🆘 Debug & Test

### Test Gemini Trực Tiếp

```bash
python3 odoo-bin.py shell -c odoo.conf
```

```python
# Trong Odoo shell
env['ai.assistant'].process_message(
    "Có bao nhiêu tài sản?", 
    "test_chat", 
    "Admin"
)
```

### Xem Quota Usage

Truy cập: https://aistudio.google.com/app/apikey
→ Xem usage statistics

---

## 📊 So Sánh Gemini vs ChatGPT

### Ưu Điểm Gemini

✅ **MIỄN PHÍ hoàn toàn**
✅ Context window cực lớn (1M tokens)
✅ Tốc độ nhanh hơn GPT-3.5
✅ Tiếng Việt tốt
✅ Không cần credit card
✅ Function calling mạnh mẽ

### Nhược Điểm (Nhỏ)

⚠️ Quota giới hạn (15 req/min)
⚠️ Đôi khi ít "sáng tạo" hơn GPT-4

### Kết Luận

**Gemini 1.5 Flash** là lựa chọn tối ưu cho:
- Doanh nghiệp nhỏ
- Sử dụng nội bộ
- Chi phí $0
- Tốc độ cao

---

## 💡 Tips & Tricks

### Hỏi Hiệu Quả

**✅ Tốt:**
- "Tìm laptop phòng IT giá trên 20 triệu"
- "Giao dịch 30 ngày gần nhất"
- "So sánh thu chi tháng này vs tháng trước"

**❌ Tránh:**
- "Có gì không?" (quá chung chung)
- "Cho tôi tất cả mọi thứ" (quá rộng)

### Tận Dụng Context

Gemini có context 1M tokens - rất lớn!

```
✅ Hỏi liên tục:
User: Tìm laptop Dell
Bot: [Kết quả]
User: Lọc cái trên 20 triệu  ← Gemini hiểu
User: Sắp xếp theo giá      ← Vẫn hiểu
User: Cái đầu tiên là gì?   ← Vẫn nhớ
```

---

## 🎓 Migration từ ChatGPT

### Nếu Bạn Đã Dùng ChatGPT

**Đã làm:**
1. ✅ Code đã chuyển sang Gemini
2. ✅ Config đã cập nhật
3. ✅ Dependencies đã thay đổi

**Bạn cần làm:**
1. Lấy Gemini API key
2. Cài `pip install google-generativeai`
3. Update module Odoo
4. Cấu hình `gemini.api_key`

**Không cần:**
- ❌ Thay đổi code
- ❌ Thay đổi Telegram bot
- ❌ Thay đổi database

---

## 🚀 Roadmap

### Đã Có

- [x] Gemini 1.5 Flash integration
- [x] Function calling tự động
- [x] Context-aware conversation
- [x] Miễn phí 100%
- [x] Tiếng Việt tối ưu

### Sắp Có

- [ ] Voice input
- [ ] Image analysis (Gemini multi-modal)
- [ ] Tạo báo cáo PDF
- [ ] Notifications chủ động

---

## 📞 Support

### Tài Liệu

- Google AI Studio: https://aistudio.google.com
- Gemini API Docs: https://ai.google.dev/docs
- Function Calling Guide: https://ai.google.dev/docs/function_calling

### Community

- GitHub Issues: [your-repo]
- Email: [your-email]
- Telegram: [your-telegram]

---

**Chúc bạn sử dụng Gemini AI Assistant hiệu quả và MIỄN PHÍ! 🚀🎉**
