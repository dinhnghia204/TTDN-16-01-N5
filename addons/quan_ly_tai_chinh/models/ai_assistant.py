# -*- coding: utf-8 -*-
"""
AI Assistant - Google Gemini Integration
Trợ lý ảo thông minh cho hệ thống ERP Odoo
"""

import json
import logging
from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# Try to import Google Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    _logger.warning("Google Gemini library not installed. AI features will be disabled.")


class AIAssistant(models.TransientModel):
    """Google Gemini-powered AI Assistant for Telegram Bot"""
    _name = 'ai.assistant'
    _description = 'AI Assistant với Google Gemini'
    
    # Conversation history cache (in-memory)
    _conversation_cache = {}
    
    @api.model
    def process_message(self, user_message, chat_id, user_name='User'):
        """
        Main entry point - Xử lý tin nhắn từ user bằng AI
        
        Args:
            user_message (str): Tin nhắn từ user
            chat_id (str): Telegram chat ID
            user_name (str): Tên user
        
        Returns:
            str: Response từ AI
        """
        if not GEMINI_AVAILABLE:
            return self._fallback_to_rule_based(user_message, chat_id, user_name)
        
        try:
            # Kiểm tra API key
            api_key = self._get_gemini_api_key()
            if not api_key:
                return "⚠️ Chưa cấu hình Gemini API key. Vui lòng liên hệ admin."
            
            genai.configure(api_key=api_key)
            
            # Lấy lịch sử hội thoại
            history = self._get_conversation_history(chat_id)
            
            # Xây dựng prompt cho Gemini
            prompt = self._build_gemini_prompt(user_message, history, user_name)
            
            # Gọi Gemini API
            response_text = self._call_gemini_api(prompt)
            
            # Clean HTML để Telegram parse được
            response_text = self._clean_html_for_telegram(response_text)
            
            # Lưu vào history
            self._save_to_history(chat_id, user_message, response_text)
            
            return response_text
                
        except Exception as e:
            _logger.error(f"AI processing error: {str(e)}", exc_info=True)
            return f"❌ Lỗi xử lý AI: {str(e)}\n\nSử dụng /help để xem lệnh cơ bản."
    
    def _get_gemini_api_key(self):
        """Lấy Gemini API key từ config"""
        return self.env['ir.config_parameter'].sudo().get_param('gemini.api_key', default='')
    
    def _clean_html_for_telegram(self, text):
        """
        Clean HTML response để Telegram parse được
        Telegram chỉ hỗ trợ: <b>, <i>, <u>, <s>, <code>, <pre>, <a>
        """
        import re
        
        # Chuyển <ul><li> thành dấu bullet
        text = re.sub(r'<ul>\s*', '', text)
        text = re.sub(r'</ul>\s*', '\n', text)
        text = re.sub(r'<li>\s*', '• ', text)
        text = re.sub(r'</li>\s*', '\n', text)
        
        # Chuyển <ol><li> thành số
        text = re.sub(r'<ol>\s*', '', text)
        text = re.sub(r'</ol>\s*', '\n', text)
        
        # Chuyển <h1-h6> thành bold
        text = re.sub(r'<h[1-6]>(.*?)</h[1-6]>', r'<b>\1</b>\n', text)
        
        # Chuyển <strong> thành <b>
        text = re.sub(r'<strong>(.*?)</strong>', r'<b>\1</b>', text)
        
        # Chuyển <em> thành <i>
        text = re.sub(r'<em>(.*?)</em>', r'<i>\1</i>', text)
        
        # Xóa <p>, <div>, <span> nhưng giữ nội dung
        text = re.sub(r'</?p>', '', text)
        text = re.sub(r'</?div>', '', text)
        text = re.sub(r'</?span[^>]*>', '', text)
        
        # Xóa <br> thành newline
        text = re.sub(r'<br\s*/?>', '\n', text)
        
        # Xóa các HTML tags không hỗ trợ khác
        text = re.sub(r'<table[^>]*>.*?</table>', '[Bảng dữ liệu]', text, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
        
        # Clean multiple newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def _build_gemini_prompt(self, user_message, history, user_name):
        """Xây dựng prompt cho Gemini với function calling"""
        # System prompt
        prompt = self._get_system_prompt(user_name)
        prompt += "\n\n"
        
        # Thêm lịch sử hội thoại (10 gần nhất)
        if history:
            prompt += "--- LỊCH SỬ HỘI THOẠI ---\n"
            for msg in history[-10:]:
                role = "User" if msg['role'] == 'user' else "Assistant"
                prompt += f"{role}: {msg['content']}\n"
            prompt += "\n"
        
        # Thêm câu hỏi hiện tại
        prompt += f"--- CÂU HỎI HIỆN TẠI ---\nUser ({user_name}): {user_message}\n\n"
        
        # Thêm hướng dẫn functions
        prompt += self._get_function_instructions()
        
        return prompt
    
    def _get_system_prompt(self, user_name):
        """System prompt định nghĩa vai trò và khả năng của AI"""
        stats = self._get_system_stats()
        
        return f"""Bạn là trợ lý tài chính thông minh tên là "TTDN Assistant" cho hệ thống ERP Odoo của doanh nghiệp Việt Nam.

THÔNG TIN HỆ THỐNG HIỆN TẠI:
- Tổng tài sản cố định: {stats['total_assets']} tài sản
- Tổng nhân viên: {stats['total_employees']} người
- Tổng phòng ban: {stats['total_departments']} phòng ban
- Ngày hôm nay: {stats['today']}

MODULE HỆ THỐNG:
1. Quản lý Tài sản (TSCĐ) - Theo dõi tài sản, khấu hao, thanh lý
2. Quản lý Nhân sự - Nhân viên, phòng ban, chức vụ
3. Quản lý Tài chính - Thu/chi, sổ cái, báo cáo
4. Quản lý Văn bản - Văn bản đến/đi

KHẢ NĂNG:
✓ Tra cứu thông tin nhanh và chính xác
✓ Phân tích và so sánh dữ liệu
✓ Tạo báo cáo tự động

CÁCH TRẢ LỜI:
- Tiếng Việt tự nhiên, thân thiện
- Ngắn gọn nhưng đầy đủ
- Sử dụng emoji phù hợp (💰 🖥️ 👥 📊)
- Số liệu cụ thể kèm đơn vị
- Chỉ dùng HTML đơn giản: <b>bold</b>, <i>italic</i>
- Không dùng <ul>, <ol>, <li>, <table>
- Dùng dấu bullet (•) thay vì list HTML

NGƯỜI DÙNG: {user_name}
Hãy giúp đỡ {user_name} một cách chuyên nghiệp!"""
    
    def _get_system_stats(self):
        """Lấy thống kê cơ bản về hệ thống"""
        try:
            return {
                'total_assets': self.env['tai_san'].search_count([]),
                'total_employees': self.env['nhan_vien'].search_count([]),
                'total_departments': self.env['phong_ban'].search_count([]),
                'today': fields.Date.today().strftime('%d/%m/%Y')
            }
        except:
            return {
                'total_assets': 0,
                'total_employees': 0,
                'total_departments': 0,
                'today': datetime.now().strftime('%d/%m/%Y')
            }
    
    def _get_function_instructions(self):
        """Hướng dẫn cho AI về các function có thể gọi"""
        return """
--- FUNCTIONS KHẢ DỤNG ---
Bạn có thể gọi các function sau để lấy dữ liệu từ Odoo:

1. get_assets - Lấy danh sách tài sản
   Parameters: department, min_price, max_price, status, keyword
   
2. get_transactions - Lấy giao dịch thu/chi
   Parameters: transaction_type (thu/chi/all), date_from, date_to, min_amount
   
3. get_employees - Lấy thông tin nhân viên
   Parameters: department, position, keyword
   
4. get_cash_balance - Lấy số dư quỹ
   Parameters: (none)
   
5. get_statistics - Thống kê tổng quan
   Parameters: stat_type (overview/assets/finance/hr)

Khi câu hỏi cần dữ liệu, hãy gọi function phù hợp.
Nếu đủ thông tin hoặc câu chung chung, trả lời trực tiếp.
"""
    
    def _call_gemini_api(self, prompt):
        """Gọi Gemini API - pure text mode"""
        try:
            model_name = self._get_model_name()
            temperature = float(self.env['ir.config_parameter'].sudo().get_param('gemini.temperature', '0.7'))
            
            # Tạo model (không dùng tools vì version 0.3.2 chưa hỗ trợ đầy đủ)
            model = genai.GenerativeModel(model_name=model_name)
            
            # Thêm hướng dẫn cho AI về data
            enhanced_prompt = self._enhance_prompt_with_data(prompt)
            
            # Generate response
            response = model.generate_content(
                enhanced_prompt,
                generation_config={
                    'temperature': temperature,
                    'max_output_tokens': 2048,
                }
            )
            
            # Xử lý response đơn giản
            if hasattr(response, 'text') and response.text:
                return response.text
            
            # Nếu không có text, thử lấy từ candidates
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content'):
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        for part in candidate.content.parts:
                            if hasattr(part, 'text') and part.text:
                                return part.text
            
            return "⚠️ Gemini không trả về kết quả. Vui lòng thử lại."
            
        except Exception as e:
            _logger.error(f"Gemini error: {str(e)}", exc_info=True)
            # Fallback: gọi lại không dùng tools
            try:
                _logger.info("Fallback to simple model without tools")
                simple_model = genai.GenerativeModel(model_name=self._get_model_name())
                response = simple_model.generate_content(
                    prompt,
                    generation_config={'temperature': 0.7, 'max_output_tokens': 2048}
                )
                return response.text if hasattr(response, 'text') else str(response)
            except Exception as fallback_error:
                _logger.error(f"Fallback also failed: {str(fallback_error)}")
                raise UserError(f"Lỗi Gemini API: {str(e)}")
    
    def _get_model_name(self):
        """Lấy tên model từ config"""
        return self.env['ir.config_parameter'].sudo().get_param(
            'gemini.model', 
            default='gemini-flash-latest'  # Model stable mới nhất
        )
    
    def _enhance_prompt_with_data(self, prompt):
        """Nhúng data vào prompt thay vì dùng function calling"""
        # Phân tích câu hỏi và lấy data tương ứng
        enhanced = prompt
        
        # Nếu hỏi về sổ cái kế toán / bút toán
        if any(keyword in prompt.lower() for keyword in ['sổ cái', 'bút toán', 'kế toán', 'định khoản', 'giao dịch']):
            try:
                # Lấy 10 bút toán gần nhất
                but_toans = self.env['so_cai_ke_toan'].search([], limit=10, order='ngay_hach_toan desc')
                if but_toans:
                    enhanced += "\n\n--- DỮ LIỆU SỔ CÁI KẾ TOÁN (10 BÚT TOÁN GẦN NHẤT) ---\n"
                    for bt in but_toans:
                        loai = dict(bt._fields['loai_chung_tu'].selection).get(bt.loai_chung_tu, 'Khác')
                        trang_thai = dict(bt._fields['trang_thai'].selection).get(bt.trang_thai, '')
                        enhanced += f"- {bt.ma_but_toan} ({bt.ngay_hach_toan.strftime('%d/%m/%Y')}): {bt.dien_giai}\n"
                        enhanced += f"  Loại: {loai} | Trạng thái: {trang_thai}\n"
                        enhanced += f"  Tổng nợ: {bt.tong_no:,.0f} VNĐ | Tổng có: {bt.tong_co:,.0f} VNĐ\n"
                        if bt.chi_tiet_but_toan_ids:
                            for detail in bt.chi_tiet_but_toan_ids[:3]:  # Chỉ lấy 3 dòng đầu
                                tk_no = detail.tk_no_id.ma_tai_khoan if detail.tk_no_id else ''
                                tk_co = detail.tk_co_id.ma_tai_khoan if detail.tk_co_id else ''
                                enhanced += f"    Nợ TK {tk_no}: {detail.so_tien_no:,.0f} | Có TK {tk_co}: {detail.so_tien_co:,.0f}\n"
            except Exception as e:
                _logger.warning(f"Cannot fetch but_toan data: {e}")
        
        # Nếu hỏi về tài sản
        if any(keyword in prompt.lower() for keyword in ['tài sản', 'tscđ', 'laptop', 'máy tính', 'thiết bị']):
            try:
                assets = self.env['tai_san'].search([], limit=10, order='ngay_mua_ts desc')
                if assets:
                    enhanced += "\n\n--- DỮ LIỆU TÀI SẢN ---\n"
                    for asset in assets:
                        dept = asset.phong_ban_su_dung_ids[0].phong_ban_id.ten_phong_ban if asset.phong_ban_su_dung_ids else 'Chưa phân bổ'
                        enhanced += f"- {asset.ten_tai_san}: {asset.gia_tri_ban_dau:,.0f} VNĐ, phòng {dept}\n"
            except:
                pass
        
        # Nếu hỏi về tiền/quỹ
        if any(keyword in prompt.lower() for keyword in ['tiền', 'số dư', 'quỹ']):
            try:
                balance = self._func_get_cash_balance()
                if balance.get('success'):
                    enhanced += "\n\n--- SỐ DƯ QUỸ ---\n"
                    enhanced += f"Tiền mặt (TK 111): {balance['tien_mat']:,.0f} VNĐ\n"
                    enhanced += f"Ngân hàng (TK 112): {balance['tien_ngan_hang']:,.0f} VNĐ\n"
                    enhanced += f"Tổng quỹ: {balance['tong_quy']:,.0f} VNĐ\n"
            except:
                pass
        
        # Nếu hỏi về thống kê/tổng quan
        if any(keyword in prompt.lower() for keyword in ['thống kê', 'tổng quan', 'bao nhiêu', 'số lượng']):
            try:
                stats = self._func_get_statistics('overview')
                if stats.get('success'):
                    enhanced += "\n\n--- THỐNG KÊ HỆ THỐNG ---\n"
                    enhanced += f"Tổng tài sản: {stats['tong_tai_san']}\n"
                    enhanced += f"Đang sử dụng: {stats['tai_san_dang_dung']}\n"
                    enhanced += f"Nhân viên: {stats['tong_nhan_vien']}\n"
                    enhanced += f"Phòng ban: {stats['tong_phong_ban']}\n"
            except:
                pass
        
        return enhanced
    
    def _execute_function(self, function_name, arguments):
        """Thực thi function được AI yêu cầu"""
        function_map = {
            'get_assets': self._func_get_assets,
            'get_transactions': self._func_get_transactions,
            'get_employees': self._func_get_employees,
            'get_cash_balance': self._func_get_cash_balance,
            'get_statistics': self._func_get_statistics,
        }
        
        func = function_map.get(function_name)
        if func:
            return func(**arguments)
        
        return {"error": f"Function {function_name} not found"}
    
    # ==================== FUNCTION IMPLEMENTATIONS ====================
    
    def _func_get_assets(self, department=None, min_price=None, max_price=None, 
                        status=None, keyword=None):
        """Lấy danh sách tài sản"""
        try:
            domain = []
            
            if department:
                phong_ban = self.env['phong_ban'].search([
                    ('ten_phong_ban', 'ilike', department)
                ], limit=1)
                if phong_ban:
                    domain.append(('phong_ban_su_dung_ids.phong_ban_id', '=', phong_ban.id))
            
            if min_price:
                domain.append(('gia_tri_ban_dau', '>=', min_price))
            
            if max_price:
                domain.append(('gia_tri_ban_dau', '<=', max_price))
            
            if status:
                domain.append(('trang_thai_thanh_ly', '=', status))
            
            if keyword:
                domain.append(('ten_tai_san', 'ilike', keyword))
            
            assets = self.env['tai_san'].search(domain, limit=20, order='ngay_mua_ts desc')
            
            if not assets:
                return {"success": False, "message": "Không tìm thấy tài sản", "count": 0, "data": []}
            
            data = []
            for asset in assets:
                dept_name = "Chưa phân bổ"
                if asset.phong_ban_su_dung_ids:
                    dept_name = asset.phong_ban_su_dung_ids[0].phong_ban_id.ten_phong_ban
                
                data.append({
                    'ma_tai_san': asset.ma_tai_san,
                    'ten_tai_san': asset.ten_tai_san,
                    'gia_tri_ban_dau': asset.gia_tri_ban_dau,
                    'gia_tri_hien_tai': asset.gia_tri_hien_tai,
                    'ngay_mua': asset.ngay_mua_ts.strftime('%d/%m/%Y') if asset.ngay_mua_ts else '',
                    'phong_ban': dept_name,
                    'trang_thai': 'Đang sử dụng' if asset.trang_thai_thanh_ly == 'da_phan_bo' else 'Đã thanh lý',
                })
            
            return {
                "success": True,
                "count": len(data),
                "total_value": sum(a['gia_tri_ban_dau'] for a in data),
                "current_value": sum(a['gia_tri_hien_tai'] for a in data),
                "data": data
            }
            
        except Exception as e:
            _logger.error(f"Error get_assets: {str(e)}")
            return {"error": f"Lỗi: {str(e)}"}
    
    def _func_get_transactions(self, transaction_type='all', date_from=None, 
                               date_to=None, min_amount=None):
        """Lấy giao dịch thu/chi"""
        try:
            result = {"success": True, "transactions": []}
            
            # Parse dates
            date_from_obj = None
            date_to_obj = None
            
            if date_from:
                try:
                    date_from_obj = datetime.strptime(date_from, '%d/%m/%Y').date()
                except:
                    pass
            
            if date_to:
                try:
                    date_to_obj = datetime.strptime(date_to, '%d/%m/%Y').date()
                except:
                    pass
            
            # Mặc định 30 ngày
            if not date_from_obj and not date_to_obj:
                date_to_obj = fields.Date.today()
                date_from_obj = date_to_obj - timedelta(days=30)
            
            # Phiếu thu
            if transaction_type in ['thu', 'all']:
                domain_thu = []
                if date_from_obj:
                    domain_thu.append(('ngay_thu', '>=', date_from_obj))
                if date_to_obj:
                    domain_thu.append(('ngay_thu', '<=', date_to_obj))
                if min_amount:
                    domain_thu.append(('so_tien', '>=', min_amount))
                
                phieu_thu = self.env['phieu_thu'].search(domain_thu, limit=20, order='ngay_thu desc')
                
                for pt in phieu_thu:
                    result['transactions'].append({
                        'loai': 'Thu',
                        'ma_phieu': pt.ma_phieu_thu,
                        'so_tien': pt.so_tien,
                        'ngay': pt.ngay_thu.strftime('%d/%m/%Y'),
                        'nguoi': pt.nguoi_nop,
                        'ly_do': pt.ly_do_thu or '',
                    })
            
            # Phiếu chi
            if transaction_type in ['chi', 'all']:
                domain_chi = []
                if date_from_obj:
                    domain_chi.append(('ngay_chi', '>=', date_from_obj))
                if date_to_obj:
                    domain_chi.append(('ngay_chi', '<=', date_to_obj))
                if min_amount:
                    domain_chi.append(('so_tien', '>=', min_amount))
                
                phieu_chi = self.env['phieu_chi'].search(domain_chi, limit=20, order='ngay_chi desc')
                
                for pc in phieu_chi:
                    result['transactions'].append({
                        'loai': 'Chi',
                        'ma_phieu': pc.ma_phieu_chi,
                        'so_tien': pc.so_tien,
                        'ngay': pc.ngay_chi.strftime('%d/%m/%Y'),
                        'nguoi': pc.nguoi_nhan,
                        'ly_do': pc.ly_do_chi or '',
                    })
            
            # Sort by date
            result['transactions'].sort(key=lambda x: datetime.strptime(x['ngay'], '%d/%m/%Y'), reverse=True)
            
            # Totals
            result['count'] = len(result['transactions'])
            result['tong_thu'] = sum(t['so_tien'] for t in result['transactions'] if t['loai'] == 'Thu')
            result['tong_chi'] = sum(t['so_tien'] for t in result['transactions'] if t['loai'] == 'Chi')
            result['chenh_lech'] = result['tong_thu'] - result['tong_chi']
            
            return result
            
        except Exception as e:
            _logger.error(f"Error get_transactions: {str(e)}")
            return {"error": f"Lỗi: {str(e)}"}
    
    def _func_get_employees(self, department=None, position=None, keyword=None):
        """Lấy thông tin nhân viên"""
        try:
            domain = []
            
            if department:
                phong_ban = self.env['phong_ban'].search([
                    ('ten_phong_ban', 'ilike', department)
                ], limit=1)
                if phong_ban:
                    domain.append(('phong_ban_id', '=', phong_ban.id))
            
            if position:
                chuc_vu = self.env['chuc_vu'].search([
                    ('ten_chuc_vu', 'ilike', position)
                ], limit=1)
                if chuc_vu:
                    domain.append(('chuc_vu_id', '=', chuc_vu.id))
            
            if keyword:
                domain.append(('ho_ten', 'ilike', keyword))
            
            employees = self.env['nhan_vien'].search(domain, limit=50)
            
            if not employees:
                return {"success": False, "message": "Không tìm thấy nhân viên", "count": 0, "data": []}
            
            data = []
            for emp in employees:
                data.append({
                    'ma_nv': emp.ma_nhan_vien,
                    'ho_ten': emp.ho_ten,
                    'phong_ban': emp.phong_ban_id.ten_phong_ban if emp.phong_ban_id else '',
                    'chuc_vu': emp.chuc_vu_id.ten_chuc_vu if emp.chuc_vu_id else '',
                    'email': emp.email or '',
                    'dien_thoai': emp.so_dien_thoai or ''
                })
            
            return {"success": True, "count": len(data), "data": data}
            
        except Exception as e:
            _logger.error(f"Error get_employees: {str(e)}")
            return {"error": f"Lỗi: {str(e)}"}
    
    def _func_get_cash_balance(self):
        """Lấy số dư quỹ"""
        try:
            tk_111 = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '111')], limit=1)
            tk_112 = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '112')], limit=1)
            
            result = {"success": True, "tien_mat": 0, "tien_ngan_hang": 0, "tong_quy": 0}
            
            # TK 111
            if tk_111:
                chi_tiet_no = self.env['chi_tiet_but_toan'].search([
                    ('tk_no_id', '=', tk_111.id),
                    ('but_toan_id.trang_thai', '=', 'da_ghi_so')
                ])
                chi_tiet_co = self.env['chi_tiet_but_toan'].search([
                    ('tk_co_id', '=', tk_111.id),
                    ('but_toan_id.trang_thai', '=', 'da_ghi_so')
                ])
                result['tien_mat'] = sum(chi_tiet_no.mapped('so_tien_no')) - sum(chi_tiet_co.mapped('so_tien_co'))
            
            # TK 112
            if tk_112:
                chi_tiet_no = self.env['chi_tiet_but_toan'].search([
                    ('tk_no_id', '=', tk_112.id),
                    ('but_toan_id.trang_thai', '=', 'da_ghi_so')
                ])
                chi_tiet_co = self.env['chi_tiet_but_toan'].search([
                    ('tk_co_id', '=', tk_112.id),
                    ('but_toan_id.trang_thai', '=', 'da_ghi_so')
                ])
                result['tien_ngan_hang'] = sum(chi_tiet_no.mapped('so_tien_no')) - sum(chi_tiet_co.mapped('so_tien_co'))
            
            result['tong_quy'] = result['tien_mat'] + result['tien_ngan_hang']
            
            return result
            
        except Exception as e:
            _logger.error(f"Error get_cash_balance: {str(e)}")
            return {"error": f"Lỗi: {str(e)}"}
    
    def _func_get_statistics(self, stat_type='overview'):
        """Thống kê tổng quan"""
        try:
            result = {"success": True, "type": stat_type}
            
            if stat_type == 'overview':
                result.update({
                    'tong_tai_san': self.env['tai_san'].search_count([]),
                    'tai_san_dang_dung': self.env['tai_san'].search_count([('trang_thai_thanh_ly', '=', 'da_phan_bo')]),
                    'tong_nhan_vien': self.env['nhan_vien'].search_count([]),
                    'tong_phong_ban': self.env['phong_ban'].search_count([]),
                })
                
                today = fields.Date.today()
                result['phieu_thu_hom_nay'] = self.env['phieu_thu'].search_count([('ngay_thu', '=', today)])
                result['phieu_chi_hom_nay'] = self.env['phieu_chi'].search_count([('ngay_chi', '=', today)])
                
            elif stat_type == 'assets':
                assets = self.env['tai_san'].search([])
                result.update({
                    'tong_so_tai_san': len(assets),
                    'tong_gia_tri_ban_dau': sum(a.gia_tri_ban_dau for a in assets),
                    'tong_gia_tri_hien_tai': sum(a.gia_tri_hien_tai for a in assets),
                    'tong_khau_hao': sum(a.gia_tri_ban_dau - a.gia_tri_hien_tai for a in assets)
                })
                
            elif stat_type == 'finance':
                today = fields.Date.today()
                first_day = today.replace(day=1)
                
                phieu_thu = self.env['phieu_thu'].search([
                    ('ngay_thu', '>=', first_day),
                    ('ngay_thu', '<=', today)
                ])
                result['tong_thu_thang_nay'] = sum(phieu_thu.mapped('so_tien'))
                
                phieu_chi = self.env['phieu_chi'].search([
                    ('ngay_chi', '>=', first_day),
                    ('ngay_chi', '<=', today)
                ])
                result['tong_chi_thang_nay'] = sum(phieu_chi.mapped('so_tien'))
                result['chenh_lech'] = result['tong_thu_thang_nay'] - result['tong_chi_thang_nay']
            
            return result
            
        except Exception as e:
            _logger.error(f"Error get_statistics: {str(e)}")
            return {"error": f"Lỗi: {str(e)}"}
    
    # ==================== CONVERSATION MANAGEMENT ====================
    
    def _get_conversation_history(self, chat_id):
        """Lấy lịch sử hội thoại"""
        return self._conversation_cache.get(chat_id, [])
    
    def _save_to_history(self, chat_id, user_message, bot_response):
        """Lưu hội thoại"""
        if chat_id not in self._conversation_cache:
            self._conversation_cache[chat_id] = []
        
        history = self._conversation_cache[chat_id]
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_response})
        
        # Giới hạn 20 messages
        if len(history) > 20:
            history = history[-20:]
        
        self._conversation_cache[chat_id] = history
    
    def _clear_history(self, chat_id):
        """Xóa lịch sử"""
        if chat_id in self._conversation_cache:
            del self._conversation_cache[chat_id]
    
    # ==================== FALLBACK ====================
    
    def _fallback_to_rule_based(self, user_message, chat_id, user_name):
        """Fallback về rule-based bot"""
        CommandHandler = self.env['telegram.command.handler']
        return CommandHandler.handle_command(user_message, chat_id, user_name)
