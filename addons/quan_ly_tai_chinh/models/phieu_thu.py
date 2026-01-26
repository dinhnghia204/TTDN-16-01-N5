# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PhieuThu(models.Model):
    _name = 'phieu_thu'
    _description = 'Phiếu thu tiền'
    _rec_name = 'ma_phieu_thu'
    _order = 'ngay_thu desc, id desc'
    
    _sql_constraints = [
        ("ma_phieu_thu_unique", "unique(ma_phieu_thu)", "Mã phiếu thu đã tồn tại!"),
    ]

    ma_phieu_thu = fields.Char('Mã phiếu thu', required=False, readonly=True, copy=False, default='/')
    ngay_thu = fields.Date('Ngày thu', required=True, default=fields.Date.today)
    
    # Người nộp tiền
    nguoi_nop = fields.Char('Người nộp tiền', required=True)
    dia_chi = fields.Char('Địa chỉ')
    
    # Loại thu
    loai_thu = fields.Selection([
        ('tien_mat', 'Tiền mặt'),
        ('chuyen_khoan', 'Chuyển khoản')
    ], string='Loại thu', required=True, default='tien_mat')
    
    # Nội dung thu
    noi_dung = fields.Selection([
        ('thu_doanh_thu', 'Thu doanh thu bán hàng'),
        ('thu_cong_no', 'Thu công nợ'),
        ('thu_von', 'Thu vốn góp'),
        ('thu_khac', 'Thu khác')
    ], string='Nội dung thu', required=True, default='thu_doanh_thu')
    
    # Tài khoản
    tk_no_id = fields.Many2one('tai_khoan_ke_toan', string='TK Nợ (Tiền)', required=True,
                               domain=[('ma_tai_khoan', 'in', ['111', '112'])])
    tk_co_id = fields.Many2one('tai_khoan_ke_toan', string='TK Có (Nguồn)', required=True)
    
    # Số tiền
    so_tien = fields.Float('Số tiền', required=True, digits=(16, 2))
    so_tien_chu = fields.Char('Số tiền bằng chữ', compute='_compute_so_tien_chu')
    
    dien_giai = fields.Text('Diễn giải', required=True)
    
    # Liên kết
    but_toan_id = fields.Many2one('so_cai_ke_toan', string='Bút toán', readonly=True, ondelete='set null')
    hoa_don_ban_id = fields.Many2one('hoa_don_ban', string='Hóa đơn bán', ondelete='set null')
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('da_thu', 'Đã thu')
    ], string='Trạng thái', default='nhap', required=True)
    
    nguoi_lap_id = fields.Many2one('nhan_vien', string='Người lập', default=lambda self: self._get_nhan_vien_hien_tai())
    nguoi_duyet_id = fields.Many2one('nhan_vien', string='Người duyệt', readonly=True)
    
    @api.model
    def create(self, vals):
        if vals.get('ma_phieu_thu', '/') == '/':
            vals['ma_phieu_thu'] = self.env['ir.sequence'].next_by_code('phieu_thu.sequence') or '/'
        return super(PhieuThu, self).create(vals)
    
    @api.depends('so_tien')
    def _compute_so_tien_chu(self):
        for record in self:
            if record.so_tien:
                record.so_tien_chu = self._number_to_words(record.so_tien)
            else:
                record.so_tien_chu = ''
    
    def _number_to_words(self, number):
        """Convert số thành chữ (simplified version)"""
        if number == 0:
            return "Không đồng"
        
        millions = int(number / 1000000)
        thousands = int((number % 1000000) / 1000)
        ones = int(number % 1000)
        
        result = []
        if millions > 0:
            result.append(f"{millions} triệu")
        if thousands > 0:
            result.append(f"{thousands} nghìn")
        if ones > 0:
            result.append(f"{ones}")
        
        return " ".join(result) + " đồng"
    
    def _get_nhan_vien_hien_tai(self):
        """Lấy nhân viên đầu tiên trong hệ thống làm mặc định"""
        nhan_vien = self.env['nhan_vien'].search([], limit=1)
        return nhan_vien.id if nhan_vien else False
    
    def action_xac_nhan_thu(self):
        """Xác nhận thu tiền và tạo bút toán"""
        for record in self:
            if record.trang_thai != 'nhap':
                raise ValidationError("Chỉ có thể xác nhận phiếu thu ở trạng thái Nháp!")
            
            if record.so_tien <= 0:
                raise ValidationError("Số tiền phải lớn hơn 0!")
            
            # Tạo bút toán
            but_toan = self.env['so_cai_ke_toan'].create({
                'ngay_hach_toan': record.ngay_thu,
                'ngay_chung_tu': record.ngay_thu,
                'so_chung_tu': record.ma_phieu_thu,
                'loai_chung_tu': 'khac',
                'dien_giai': f"Thu tiền: {record.dien_giai}",
                'nguoi_lap_id': record.nguoi_lap_id.id,
                'chi_tiet_but_toan_ids': [(0, 0, {
                    'tk_no_id': record.tk_no_id.id,
                    'tk_co_id': record.tk_co_id.id,
                    'so_tien': record.so_tien,
                    'dien_giai': record.dien_giai,
                })]
            })
            
            # Auto ghi sổ
            but_toan.action_ghi_so()
            
            # Update trạng thái
            record.write({
                'trang_thai': 'da_thu',
                'but_toan_id': but_toan.id,
                'nguoi_duyet_id': self._get_nhan_vien_hien_tai()
            })
            
            # Gửi notification
            self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                'title': _('Phiếu thu'),
                'message': _('Đã xác nhận phiếu thu %s - Số tiền: %s VNĐ') % (record.ma_phieu_thu, '{:,.0f}'.format(record.so_tien)),
                'sticky': False,
            })
            
            # ⭐ Gửi qua Telegram nếu có cấu hình
            from .telegram_helper import get_telegram_bot
            telegram_bot = get_telegram_bot(self.env)
            if telegram_bot:
                telegram_bot.send_notification(
                    title='💰 Phiếu thu',
                    message=f'Đã xác nhận phiếu thu {record.ma_phieu_thu}\nSố tiền: {record.so_tien:,.0f} VNĐ\nNgười nộp: {record.nguoi_nop}',
                    notification_type='success'
                )
