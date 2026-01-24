# -*- coding: utf-8 -*-
from odoo import models, fields, api


class VanBanDi(models.Model):
    _name = 'van_ban_di'
    _description = 'Văn bản đi'
    _rec_name = 'so_ky_hieu'
    _order = 'ngay_soan_thao desc, id desc'

    # Thông tin định danh
    so_ky_hieu = fields.Char('Số ký hiệu', required=True, readonly=True, copy=False, default='/')
    ten_van_ban = fields.Char('Tên văn bản/Trích yếu', required=True)
    loai_van_ban_id = fields.Many2one('loai_van_ban', string='Loại văn bản', required=True)
    
    # Người tạo và phát hành
    nguoi_soan_thao_id = fields.Many2one('nhan_vien', string='Người soạn thảo', required=True, 
                                         default=lambda self: self.env.context.get('default_nguoi_soan_thao_id'))
    phong_ban_soan_thao_id = fields.Many2one('phong_ban', string='Phòng ban soạn thảo', required=True)
    nguoi_ky_id = fields.Many2one('nhan_vien', string='Người ký duyệt')
    
    ngay_soan_thao = fields.Date('Ngày soạn thảo', required=True, default=fields.Date.context_today)
    ngay_phat_hanh = fields.Date('Ngày phát hành')
    
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
    
    # Nơi nhận
    noi_nhan = fields.Text('Nơi nhận', help='Liệt kê các cơ quan/đơn vị nhận văn bản')
    
    # Trạng thái workflow
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('da_phat_hanh', 'Đã phát hành')
    ], string='Trạng thái', default='nhap', required=True)
    
    # File đính kèm
    file_van_ban = fields.Binary('File văn bản', attachment=True)
    file_name = fields.Char('Tên file')
    
    # Ghi chú
    ghi_chu = fields.Text('Ghi chú')
    
    @api.model
    def create(self, vals):
        """Tự động tạo số ký hiệu khi tạo văn bản đi"""
        if vals.get('so_ky_hieu', '/') == '/':
            vals['so_ky_hieu'] = self.env['ir.sequence'].next_by_code('van_ban_di') or '/'
        return super(VanBanDi, self).create(vals)
    
    @api.onchange('nguoi_soan_thao_id')
    def _onchange_nguoi_soan_thao_id(self):
        """Tự động điền phòng ban khi chọn người soạn thảo"""
        if self.nguoi_soan_thao_id and self.nguoi_soan_thao_id.phong_ban_id:
            self.phong_ban_soan_thao_id = self.nguoi_soan_thao_id.phong_ban_id
    
    def action_gui_duyet(self):
        """Gửi văn bản đi duyệt"""
        self.write({'trang_thai': 'cho_duyet'})
    
    def action_duyet(self):
        """Duyệt văn bản"""
        self.write({'trang_thai': 'da_duyet'})
    
    def action_phat_hanh(self):
        """Phát hành văn bản"""
        self.write({
            'trang_thai': 'da_phat_hanh',
            'ngay_phat_hanh': fields.Date.context_today(self)
        })
    
    def action_tra_lai(self):
        """Trả lại văn bản về nháp"""
        self.write({'trang_thai': 'nhap'})
    
    _sql_constraints = [
        ('so_ky_hieu_unique', 'UNIQUE(so_ky_hieu)', 'Số ký hiệu văn bản đã tồn tại!')
    ]
