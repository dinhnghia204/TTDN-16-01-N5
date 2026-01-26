# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SoCaiKeToan(models.Model):
    _name = 'so_cai_ke_toan'
    _description = 'Sổ cái kế toán'
    _rec_name = 'ma_but_toan'
    _order = 'ngay_hach_toan desc, id desc'
    
    _sql_constraints = [
        ("ma_but_toan_unique", "unique(ma_but_toan)", "Mã bút toán đã tồn tại!"),
    ]

    ma_but_toan = fields.Char('Mã bút toán', required=False, readonly=True, copy=False, default='/')
    ngay_hach_toan = fields.Date('Ngày hạch toán', required=True, default=fields.Date.today)
    ngay_chung_tu = fields.Date('Ngày chứng từ', required=True, default=fields.Date.today)
    so_chung_tu = fields.Char('Số chứng từ', required=True)
    
    # Loại chứng từ và liên kết
    loai_chung_tu = fields.Selection([
        ('tai_san', 'Mua/Thanh lý tài sản'),
        ('luong', 'Phiếu lương'),
        ('van_ban', 'Văn bản chi tiêu'),
        ('khau_hao', 'Khấu hao tài sản'),
        ('khac', 'Khác')
    ], string='Loại chứng từ', required=True, default='khac')
    
    # Tích hợp với modules cũ
    tai_san_id = fields.Many2one('tai_san', string='Tài sản', ondelete='set null')
    phieu_luong_id = fields.Many2one('phieu_luong', string='Phiếu lương', ondelete='set null')
    van_ban_chi_id = fields.Many2one('van_ban_di', string='Văn bản chi', ondelete='set null')
    lich_su_khau_hao_id = fields.Many2one('lich_su_khau_hao', string='Phiếu khấu hao', ondelete='set null')
    
    # Chi tiết bút toán
    chi_tiet_but_toan_ids = fields.One2many('chi_tiet_but_toan', 'but_toan_id', string='Chi tiết bút toán')
    
    # Tổng số tiền
    tong_no = fields.Float('Tổng nợ', compute='_compute_tong', store=True, digits=(16, 2))
    tong_co = fields.Float('Tổng có', compute='_compute_tong', store=True, digits=(16, 2))
    chenh_lech = fields.Float('Chênh lệch', compute='_compute_tong', store=True, digits=(16, 2))
    
    dien_giai = fields.Text('Diễn giải', required=True)
    nguoi_lap_id = fields.Many2one('nhan_vien', string='Người lập', default=lambda self: self._get_nhan_vien_hien_tai())
    
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('da_ghi_so', 'Đã ghi sổ')
    ], string='Trạng thái', default='nhap', required=True)
    
    def _get_nhan_vien_hien_tai(self):
        """Lấy nhân viên từ user hiện tại"""
        return self.env['nhan_vien'].search([('email', '=', self.env.user.login)], limit=1).id
    
    @api.depends('chi_tiet_but_toan_ids.so_tien_no', 'chi_tiet_but_toan_ids.so_tien_co')
    def _compute_tong(self):
        for record in self:
            record.tong_no = sum(record.chi_tiet_but_toan_ids.mapped('so_tien_no'))
            record.tong_co = sum(record.chi_tiet_but_toan_ids.mapped('so_tien_co'))
            record.chenh_lech = record.tong_no - record.tong_co
    
    @api.constrains('chi_tiet_but_toan_ids')
    def _check_balance(self):
        for record in self:
            if record.trang_thai == 'da_ghi_so' and abs(record.chenh_lech) > 0.01:
                raise ValidationError(
                    f"Bút toán không cân bằng!\n"
                    f"Tổng Nợ: {record.tong_no:,.2f}\n"
                    f"Tổng Có: {record.tong_co:,.2f}\n"
                    f"Chênh lệch: {record.chenh_lech:,.2f}"
                )
    
    @api.model
    def create(self, vals):
        if not vals.get('ma_but_toan') or vals.get('ma_but_toan') == '/':
            vals['ma_but_toan'] = self.env['ir.sequence'].next_by_code('so_cai_ke_toan.sequence') or '/'
        return super().create(vals)
    
    def action_ghi_so(self):
        """Chuyển trạng thái sang đã ghi sổ"""
        for record in self:
            if not record.chi_tiet_but_toan_ids:
                raise ValidationError("Bút toán phải có ít nhất 1 chi tiết!")
            if abs(record.chenh_lech) > 0.01:
                raise ValidationError(f"Bút toán không cân bằng! Chênh lệch: {record.chenh_lech:,.2f}")
            record.trang_thai = 'da_ghi_so'
        
        # Gửi notification
        self.env['bus.bus']._sendone(
            self.env.user.partner_id,
            'simple_notification',
            {
                'title': 'Ghi sổ thành công',
                'message': f'Đã ghi sổ bút toán {self.ma_but_toan}',
                'sticky': False,
                'type': 'success'
            }
        )
    
    def action_huy_ghi_so(self):
        """Chuyển về trạng thái nháp"""
        for record in self:
            record.trang_thai = 'nhap'
