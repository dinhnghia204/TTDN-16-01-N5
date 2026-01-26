# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class TelegramCommandHandler(models.TransientModel):
    """Xử lý các command từ Telegram bot"""
    _name = 'telegram.command.handler'
    _description = 'Telegram Command Handler'
    
    @api.model
    def handle_command(self, command, chat_id, user_name=''):
        """
        Xử lý command từ user và trả về response
        
        Args:
            command (str): Command từ user (VD: /start, /stats)
            chat_id (str): Chat ID của user
            user_name (str): Tên user
        
        Returns:
            str: Response message
        """
        command = command.strip().lower()
        
        # Command mapping
        handlers = {
            '/start': self._cmd_start,
            '/help': self._cmd_help,
            '/stats': self._cmd_stats,
            '/today': self._cmd_today,
            '/canban': self._cmd_can_ban,
            '/phieuthu': self._cmd_phieu_thu,
            '/phieuchi': self._cmd_phieu_chi,
            '/soquy': self._cmd_so_quy,
            '/taisan': self._cmd_tai_san,
            '/hoadon': self._cmd_hoa_don,
            '/congno': self._cmd_cong_no,
        }
        
        # Tìm handler phù hợp
        handler = handlers.get(command)
        if handler:
            try:
                return handler(user_name)
            except Exception as e:
                _logger.error(f"Error handling command {command}: {str(e)}")
                return f"❌ Lỗi khi xử lý lệnh: {str(e)}"
        
        # Xử lý text search
        if command.startswith('tra tai san'):
            return self._search_tai_san(command.replace('tra tai san:', '').strip())
        elif command.startswith('tra nv'):
            return self._search_nhan_vien(command.replace('tra nv:', '').strip())
        
        # Command không hợp lệ
        return f"❓ Không hiểu lệnh '{command}'\n\nGõ /help để xem danh sách lệnh."
    
    def _cmd_start(self, user_name):
        """Welcome message"""
        return f"""👋 Xin chào {user_name}!

Chào mừng bạn đến với <b>TTDN Accounting Bot</b>

🤖 Tôi có thể giúp bạn:
• Xem thống kê tài chính
• Tra cứu tài sản, nhân viên
• Kiểm tra quỹ tiền, công nợ
• Nhận thông báo realtime

📝 Gõ /help để xem danh sách lệnh"""
    
    def _cmd_help(self, user_name):
        """Danh sách commands"""
        return """📚 DANH SÁCH LỆNH

📊 Thống kê
/stats - Tổng quan hệ thống
/today - Giao dịch hôm nay
/canban - Số dư quỹ

💰 Quỹ tiền
/soquy - Tổng quỹ tiền
/phieuthu - Phiếu thu gần đây
/phieuchi - Phiếu chi gần đây

🖥️ Tài sản
/taisan - Danh sách TSCĐ
tra tai san: [từ khóa] - Tìm tài sản

📄 Hóa đơn
/hoadon - HĐ chưa thanh toán
/congno - Công nợ

👥 Nhân viên
tra nv: [từ khóa] - Tìm nhân viên"""
    
    def _cmd_stats(self, user_name):
        """Thống kê tổng quan"""
        try:
            # Đếm tài sản
            total_assets = self.env['tai_san'].search_count([])
            active_assets = self.env['tai_san'].search_count([('trang_thai_thanh_ly', '=', 'da_phan_bo')])
            
            # Tổng giá trị tài sản
            assets = self.env['tai_san'].search([])
            total_value = sum(asset.gia_tri_ban_dau for asset in assets)
            net_value = sum(asset.gia_tri_hien_tai for asset in assets)
            
            # Nhân viên
            total_employees = self.env['nhan_vien'].search_count([])
            
            # Phiếu thu/chi hôm nay
            today = fields.Date.today()
            phieu_thu_today = self.env['phieu_thu'].search_count([
                ('ngay_thu', '=', today)
            ])
            phieu_chi_today = self.env['phieu_chi'].search_count([
                ('ngay_chi', '=', today)
            ])
            
            return f"""📊 <b>THỐNG KÊ TỔNG QUAN</b>

<b>🖥️ Tài sản cố định</b>
• Tổng số: {total_assets} tài sản
• Đang sử dụng: {active_assets} tài sản
• Giá trị ban đầu: {total_value:,.0f} VNĐ
• Giá trị còn lại: {net_value:,.0f} VNĐ

<b>👥 Nhân sự</b>
• Tổng: {total_employees} nhân viên

<b>💰 Giao dịch hôm nay</b>
• Phiếu thu: {phieu_thu_today}
• Phiếu chi: {phieu_chi_today}

🕐 {fields.Datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"""
        except Exception as e:
            return f"❌ Lỗi: {str(e)}"
    
    def _cmd_today(self, user_name):
        """Giao dịch hôm nay"""
        today = fields.Date.today()
        
        # Phiếu thu
        phieu_thu = self.env['phieu_thu'].search([
            ('ngay_thu', '=', today)
        ], limit=5, order='ngay_thu desc')
        
        # Phiếu chi
        phieu_chi = self.env['phieu_chi'].search([
            ('ngay_chi', '=', today)
        ], limit=5, order='ngay_chi desc')
        
        result = f"📅 <b>GIAO DỊCH HÔM NAY</b>\n<i>{today.strftime('%d/%m/%Y')}</i>\n\n"
        
        if phieu_thu:
            result += "<b>💰 Phiếu thu:</b>\n"
            total_thu = 0
            for pt in phieu_thu:
                result += f"• {pt.ma_phieu_thu}: {pt.so_tien:,.0f} VNĐ - {pt.nguoi_nop}\n"
                total_thu += pt.so_tien
            result += f"  <b>Tổng thu: {total_thu:,.0f} VNĐ</b>\n\n"
        else:
            result += "💰 Phiếu thu: Chưa có\n\n"
        
        if phieu_chi:
            result += "<b>💸 Phiếu chi:</b>\n"
            total_chi = 0
            for pc in phieu_chi:
                result += f"• {pc.ma_phieu_chi}: {pc.so_tien:,.0f} VNĐ - {pc.nguoi_nhan}\n"
                total_chi += pc.so_tien
            result += f"  <b>Tổng chi: {total_chi:,.0f} VNĐ</b>\n\n"
        else:
            result += "💸 Phiếu chi: Chưa có\n\n"
        
        return result
    
    def _cmd_can_ban(self, user_name):
        """Số dư quỹ"""
        # Lấy tài khoản tiền mặt (111) và ngân hàng (112)
        tk_111 = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '111')], limit=1)
        tk_112 = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '112')], limit=1)
        
        result = "<b>💰 SỐ DƯ QUỸ</b>\n\n"
        
        if tk_111:
            # Tính số dư từ chi tiết bút toán (bên Nợ + bên Có)
            chi_tiet_no = self.env['chi_tiet_but_toan'].search([
                ('tk_no_id', '=', tk_111.id),
                ('but_toan_id.trang_thai', '=', 'da_ghi_so')
            ])
            chi_tiet_co = self.env['chi_tiet_but_toan'].search([
                ('tk_co_id', '=', tk_111.id),
                ('but_toan_id.trang_thai', '=', 'da_ghi_so')
            ])
            tong_no = sum(chi_tiet_no.mapped('so_tien_no'))
            tong_co = sum(chi_tiet_co.mapped('so_tien_co'))
            du_111 = tong_no - tong_co
            
            result += f"<b>Tiền mặt (111)</b>\n"
            result += f"• Nợ: {tong_no:,.0f} VNĐ\n"
            result += f"• Có: {tong_co:,.0f} VNĐ\n"
            result += f"• Dư: {du_111:,.0f} VNĐ\n\n"
        else:
            du_111 = 0
        
        if tk_112:
            # Tính số dư từ chi tiết bút toán (bên Nợ + bên Có)
            chi_tiet_no = self.env['chi_tiet_but_toan'].search([
                ('tk_no_id', '=', tk_112.id),
                ('but_toan_id.trang_thai', '=', 'da_ghi_so')
            ])
            chi_tiet_co = self.env['chi_tiet_but_toan'].search([
                ('tk_co_id', '=', tk_112.id),
                ('but_toan_id.trang_thai', '=', 'da_ghi_so')
            ])
            tong_no = sum(chi_tiet_no.mapped('so_tien_no'))
            tong_co = sum(chi_tiet_co.mapped('so_tien_co'))
            du_112 = tong_no - tong_co
            
            result += f"<b>Tiền gửi NH (112)</b>\n"
            result += f"• Nợ: {tong_no:,.0f} VNĐ\n"
            result += f"• Có: {tong_co:,.0f} VNĐ\n"
            result += f"• Dư: {du_112:,.0f} VNĐ\n\n"
        else:
            du_112 = 0
        
        total = du_111 + du_112
        result += f"<b>TỔNG QUỸ: {total:,.0f} VNĐ</b>"
        
        return result
    
    def _cmd_phieu_thu(self, user_name):
        """Phiếu thu gần đây"""
        phieu_thu = self.env['phieu_thu'].search([], limit=10, order='ngay_thu desc')
        
        if not phieu_thu:
            return "💰 Chưa có phiếu thu nào"
        
        result = "<b>💰 PHIẾU THU GẦN ĐÂY</b>\n\n"
        for pt in phieu_thu:
            status = "✅" if pt.trang_thai == 'da_thu' else "⏳"
            result += f"{status} <b>{pt.ma_phieu_thu}</b>\n"
            result += f"   {pt.so_tien:,.0f} VNĐ - {pt.nguoi_nop}\n"
            result += f"   📅 {pt.ngay_thu.strftime('%d/%m/%Y')}\n\n"
        
        return result
    
    def _cmd_phieu_chi(self, user_name):
        """Phiếu chi gần đây"""
        phieu_chi = self.env['phieu_chi'].search([], limit=10, order='ngay_chi desc')
        
        if not phieu_chi:
            return "💸 Chưa có phiếu chi nào"
        
        result = "<b>💸 PHIẾU CHI GẦN ĐÂY</b>\n\n"
        for pc in phieu_chi:
            status = "✅" if pc.trang_thai == 'da_chi' else "⏳"
            result += f"{status} <b>{pc.ma_phieu_chi}</b>\n"
            result += f"   {pc.so_tien:,.0f} VNĐ - {pc.nguoi_nhan}\n"
            result += f"   📅 {pc.ngay_chi.strftime('%d/%m/%Y')}\n\n"
        
        return result
    
    def _cmd_so_quy(self, user_name):
        """Tổng quỹ tiền - hiển thị tổng hợp"""
        tk_111 = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '111')], limit=1)
        tk_112 = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '112')], limit=1)
        
        result = "<b>💰 TỔNG QUỸ TIỀN</b>\n\n"
        
        # Tính tiền mặt
        if tk_111:
            chi_tiet_no = self.env['chi_tiet_but_toan'].search([
                ('tk_no_id', '=', tk_111.id),
                ('but_toan_id.trang_thai', '=', 'da_ghi_so')
            ])
            chi_tiet_co = self.env['chi_tiet_but_toan'].search([
                ('tk_co_id', '=', tk_111.id),
                ('but_toan_id.trang_thai', '=', 'da_ghi_so')
            ])
            du_111 = sum(chi_tiet_no.mapped('so_tien_no')) - sum(chi_tiet_co.mapped('so_tien_co'))
            result += f"💵 Tiền mặt: <b>{du_111:,.0f} VNĐ</b>\n"
        else:
            du_111 = 0
            result += f"💵 Tiền mặt: <b>0 VNĐ</b>\n"
        
        # Tính tiền ngân hàng
        if tk_112:
            chi_tiet_no = self.env['chi_tiet_but_toan'].search([
                ('tk_no_id', '=', tk_112.id),
                ('but_toan_id.trang_thai', '=', 'da_ghi_so')
            ])
            chi_tiet_co = self.env['chi_tiet_but_toan'].search([
                ('tk_co_id', '=', tk_112.id),
                ('but_toan_id.trang_thai', '=', 'da_ghi_so')
            ])
            du_112 = sum(chi_tiet_no.mapped('so_tien_no')) - sum(chi_tiet_co.mapped('so_tien_co'))
            result += f"🏦 Ngân hàng: <b>{du_112:,.0f} VNĐ</b>\n"
        else:
            du_112 = 0
            result += f"🏦 Ngân hàng: <b>0 VNĐ</b>\n"
        
        # Tổng
        total = du_111 + du_112
        result += f"\n━━━━━━━━━━━━━━━━\n"
        result += f"💰 <b>TỔNG CỘNG: {total:,.0f} VNĐ</b>"
        
        return result
    
    def _cmd_tai_san(self, user_name):
        """Danh sách tài sản"""
        assets = self.env['tai_san'].search([
            ('trang_thai_thanh_ly', '=', 'da_phan_bo')
        ], limit=10, order='ngay_mua_ts desc')
        
        if not assets:
            return "🖥️ Chưa có tài sản nào"
        
        result = "<b>🖥️ TÀI SẢN CỐ ĐỊNH</b>\n\n"
        total_value = 0
        for asset in assets:
            # Lấy phòng ban từ phân bổ tài sản
            phong_ban_name = 'Chưa phân bổ'
            if asset.phong_ban_su_dung_ids:
                phong_ban_name = asset.phong_ban_su_dung_ids[0].phong_ban_su_dung_id.ten_phong_ban
            
            result += f"<b>{asset.ma_tai_san}</b> - {asset.ten_tai_san}\n"
            result += f"   💰 {asset.gia_tri_hien_tai:,.0f} VNĐ\n"
            result += f"   📍 {phong_ban_name}\n\n"
            total_value += asset.gia_tri_hien_tai
        
        result += f"<b>TỔNG GIÁ TRỊ: {total_value:,.0f} VNĐ</b>"
        return result
    
    def _cmd_hoa_don(self, user_name):
        """Hóa đơn chưa thanh toán"""
        # Hóa đơn bán
        hd_ban = self.env['hoa_don_ban'].search([
            ('trang_thai', '=', 'chua_thanh_toan')
        ], limit=5)
        
        # Hóa đơn mua
        hd_mua = self.env['hoa_don_mua'].search([
            ('trang_thai', '=', 'chua_thanh_toan')
        ], limit=5)
        
        result = "<b>📄 HÓA ĐƠN CHƯA THANH TOÁN</b>\n\n"
        
        if hd_ban:
            result += "<b>🧾 Hóa đơn bán:</b>\n"
            for hd in hd_ban:
                result += f"• {hd.ma_hoa_don}: {hd.tong_thanh_toan:,.0f} VNĐ\n"
            result += "\n"
        
        if hd_mua:
            result += "<b>📄 Hóa đơn mua:</b>\n"
            for hd in hd_mua:
                result += f"• {hd.ma_hoa_don}: {hd.tong_thanh_toan:,.0f} VNĐ\n"
        
        if not hd_ban and not hd_mua:
            result += "✅ Không có hóa đơn chưa thanh toán"
        
        return result
    
    def _cmd_cong_no(self, user_name):
        """Công nợ phải thu/phải trả"""
        # Phải thu (TK 131)
        tk_131 = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '131')], limit=1)
        # Phải trả (TK 331)
        tk_331 = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '331')], limit=1)
        
        result = "<b>📊 CÔNG NỢ</b>\n\n"
        
        if tk_131:
            chi_tiet_no = self.env['chi_tiet_but_toan'].search([
                ('tk_no_id', '=', tk_131.id),
                ('but_toan_id.trang_thai', '=', 'da_ghi_so')
            ])
            chi_tiet_co = self.env['chi_tiet_but_toan'].search([
                ('tk_co_id', '=', tk_131.id),
                ('but_toan_id.trang_thai', '=', 'da_ghi_so')
            ])
            tong_no = sum(chi_tiet_no.mapped('so_tien_no'))
            tong_co = sum(chi_tiet_co.mapped('so_tien_co'))
            phai_thu = tong_no - tong_co
            result += f"<b>💰 Phải thu (131)</b>\n"
            result += f"   {phai_thu:,.0f} VNĐ\n\n"
        
        if tk_331:
            chi_tiet_no = self.env['chi_tiet_but_toan'].search([
                ('tk_no_id', '=', tk_331.id),
                ('but_toan_id.trang_thai', '=', 'da_ghi_so')
            ])
            chi_tiet_co = self.env['chi_tiet_but_toan'].search([
                ('tk_co_id', '=', tk_331.id),
                ('but_toan_id.trang_thai', '=', 'da_ghi_so')
            ])
            tong_no = sum(chi_tiet_no.mapped('so_tien_no'))
            tong_co = sum(chi_tiet_co.mapped('so_tien_co'))
            phai_tra = tong_co - tong_no
            result += f"<b>💸 Phải trả (331)</b>\n"
            result += f"   {phai_tra:,.0f} VNĐ\n\n"
        
        return result
    
    def _search_tai_san(self, keyword):
        """Tìm tài sản theo tên"""
        if not keyword:
            return "❓ Vui lòng nhập tên tài sản\nVD: tra tai san: Laptop"
        
        assets = self.env['tai_san'].search([
            '|', ('ten_tai_san', 'ilike', keyword),
            ('ma_tai_san', 'ilike', keyword)
        ], limit=5)
        
        if not assets:
            return f"❌ Không tìm thấy tài sản '{keyword}'"
        
        result = f"<b>🔍 KẾT QUẢ TÌM KIẾM: {keyword}</b>\n\n"
        for asset in assets:
            # Lấy phòng ban từ phân bổ
            phong_ban_name = 'Chưa phân bổ'
            if asset.phong_ban_su_dung_ids:
                phong_ban_name = asset.phong_ban_su_dung_ids[0].phong_ban_su_dung_id.ten_phong_ban
            
            result += f"<b>{asset.ma_tai_san}</b> - {asset.ten_tai_san}\n"
            result += f"   💰 Giá trị: {asset.gia_tri_hien_tai:,.0f} VNĐ\n"
            result += f"   📍 {phong_ban_name}\n"
            result += f"   📅 Mua: {asset.ngay_mua_ts.strftime('%d/%m/%Y')}\n\n"
        
        return result
    
    def _search_nhan_vien(self, keyword):
        """Tìm nhân viên theo tên"""
        if not keyword:
            return "❓ Vui lòng nhập tên nhân viên\nVD: tra nv: Nguyễn"
        
        employees = self.env['nhan_vien'].search([
            '|', ('ten_nhan_vien', 'ilike', keyword),
            ('ma_nhan_vien', 'ilike', keyword)
        ], limit=5)
        
        if not employees:
            return f"❌ Không tìm thấy nhân viên '{keyword}'"
        
        result = f"<b>🔍 KẾT QUẢ TÌM KIẾM: {keyword}</b>\n\n"
        for emp in employees:
            result += f"<b>{emp.ma_nhan_vien}</b> - {emp.ten_nhan_vien}\n"
            result += f"   📧 {emp.email or 'N/A'}\n"
            result += f"   📞 {emp.so_dien_thoai or 'N/A'}\n"
            result += f"   🏢 {emp.phong_ban_id.ten_phong_ban if emp.phong_ban_id else 'N/A'}\n"
            result += f"   💼 {emp.chuc_vu_id.ten_chuc_vu if emp.chuc_vu_id else 'N/A'}\n\n"
        
        return result
