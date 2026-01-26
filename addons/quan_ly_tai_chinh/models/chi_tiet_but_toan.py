# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ChiTietButToan(models.Model):
    _name = 'chi_tiet_but_toan'
    _description = 'Chi tiết bút toán'

    but_toan_id = fields.Many2one('so_cai_ke_toan', string='Bút toán', required=True, ondelete='cascade')
    
    tk_no_id = fields.Many2one('tai_khoan_ke_toan', string='TK Nợ', required=True, ondelete='restrict',
                               domain="[('kich_hoat', '=', True)]")
    tk_co_id = fields.Many2one('tai_khoan_ke_toan', string='TK Có', required=True, ondelete='restrict',
                               domain="[('kich_hoat', '=', True)]")
    
    so_tien_no = fields.Float('Số tiền nợ', default=0, digits=(16, 2))
    so_tien_co = fields.Float('Số tiền có', default=0, digits=(16, 2))
    so_tien = fields.Float('Số tiền', compute='_compute_so_tien', store=True, digits=(16, 2))
    
    dien_giai = fields.Char('Diễn giải')
    
    # Thông tin phụ
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng ban', ondelete='set null')
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', ondelete='set null')
    
    @api.depends('so_tien_no', 'so_tien_co')
    def _compute_so_tien(self):
        for record in self:
            # Lấy số tiền lớn hơn (thường chỉ 1 trong 2 có giá trị)
            record.so_tien = max(record.so_tien_no, record.so_tien_co)
    
    @api.constrains('tk_no_id', 'tk_co_id')
    def _check_tai_khoan(self):
        for record in self:
            if record.tk_no_id == record.tk_co_id:
                raise ValidationError("Tài khoản Nợ và Có không được trùng nhau!")
    
    @api.constrains('so_tien_no', 'so_tien_co')
    def _check_so_tien(self):
        for record in self:
            if record.so_tien_no < 0 or record.so_tien_co < 0:
                raise ValidationError("Số tiền không được âm!")
            # Đảm bảo chỉ 1 trong 2 có giá trị hoặc cả 2 bằng nhau
            if record.so_tien_no > 0 and record.so_tien_co > 0:
                if abs(record.so_tien_no - record.so_tien_co) > 0.01:
                    raise ValidationError("Nếu cả Nợ và Có đều có giá trị thì phải bằng nhau!")
