# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date


class VanBanDen(models.Model):
    _name = 'van_ban_den'
    _description = 'Văn bản đến'
    _rec_name = 'so_ky_hieu'
    _order = 'ngay_den desc, id desc'

    # Thông tin định danh
    so_ky_hieu = fields.Char('Số ký hiệu', required=True, readonly=True, copy=False, default='/')
    ten_van_ban = fields.Char('Tên văn bản/Trích yếu', required=True)
    loai_van_ban_id = fields.Many2one('loai_van_ban', string='Loại văn bản', required=True)
    
    # Nguồn gốc
    co_quan_ban_hanh = fields.Char('Cơ quan ban hành', required=True)
    ngay_ban_hanh = fields.Date('Ngày ban hành', required=True)
    ngay_den = fields.Date('Ngày đến', required=True, default=fields.Date.context_today)
    
    # Độ khẩn, độ mật
    do_khan = fields.Selection([
        ('thuong', 'Thường'),
        ('khan', 'Khẩn'),
        ('hoa_toc', 'Hỏa tốc')
    ], string='Độ khẩn', default='thuong', required=True)
    
    do_mat = fields.Selection([
        ('thuong', 'Thường'),
        ('mat', 'Mật'),
        ('toi_mat', 'Tối mật')
    ], string='Độ mật', default='thuong', required=True)
    
    # Xử lý
    nguoi_nhan_id = fields.Many2one('nhan_vien', string='Người nhận', required=True)
    phong_ban_nhan_id = fields.Many2one('phong_ban', string='Phòng ban xử lý', required=True)
    han_xu_ly = fields.Date('Hạn xử lý')
    noi_dung_xu_ly = fields.Text('Nội dung xử lý')
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('dang_xu_ly', 'Đang xử lý'),
        ('da_xu_ly', 'Đã xử lý')
    ], string='Trạng thái', default='moi', required=True)
    
    # File đính kèm
    file_van_ban = fields.Binary('File văn bản', attachment=True)
    file_name = fields.Char('Tên file')
    
    # Computed fields
    qua_han = fields.Boolean('Quá hạn', compute='_compute_qua_han', store=True)
    so_ngay_con_lai = fields.Integer('Số ngày còn lại', compute='_compute_qua_han')
    
    @api.depends('han_xu_ly', 'trang_thai')
    def _compute_qua_han(self):
        today = date.today()
        for rec in self:
            if rec.han_xu_ly and rec.trang_thai != 'da_xu_ly':
                delta = (rec.han_xu_ly - today).days
                rec.so_ngay_con_lai = delta
                rec.qua_han = delta < 0
            else:
                rec.so_ngay_con_lai = 0
                rec.qua_han = False
    
    @api.onchange('nguoi_nhan_id')
    def _onchange_nguoi_nhan_id(self):
        """Tự động điền phòng ban khi chọn người nhận"""
        if self.nguoi_nhan_id and self.nguoi_nhan_id.phong_ban_id:
            self.phong_ban_nhan_id = self.nguoi_nhan_id.phong_ban_id
    
    def action_bat_dau_xu_ly(self):
        """Chuyển trạng thái sang đang xử lý"""
        self.write({'trang_thai': 'dang_xu_ly'})
    
    def action_hoan_thanh_xu_ly(self):
        """Chuyển trạng thái sang đã xử lý"""
        self.write({'trang_thai': 'da_xu_ly'})
    
    @api.model
    def create(self, vals):
        """Tự động tạo số ký hiệu khi tạo văn bản đến"""
        if vals.get('so_ky_hieu', '/') == '/':
            vals['so_ky_hieu'] = self.env['ir.sequence'].next_by_code('van_ban_den.sequence') or '/'
        return super(VanBanDen, self).create(vals)
    
    _sql_constraints = [
        ('so_ky_hieu_unique', 'UNIQUE(so_ky_hieu)', 'Số ký hiệu văn bản đã tồn tại!')
    ]
