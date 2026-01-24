# -*- coding: utf-8 -*-
from odoo import models, fields, api


class LoaiVanBan(models.Model):
    _name = 'loai_van_ban'
    _description = 'Loại văn bản'
    _rec_name = 'ten_loai'

    ma_loai = fields.Char('Mã loại', required=True, size=10, readonly=True, copy=False, default='/')
    ten_loai = fields.Char('Tên loại văn bản', required=True)
    mo_ta = fields.Text('Mô tả')
    active = fields.Boolean('Hoạt động', default=True)
    
    @api.model
    def create(self, vals):
        """Tự động tạo mã loại khi tạo loại văn bản"""
        if vals.get('ma_loai', '/') == '/':
            vals['ma_loai'] = self.env['ir.sequence'].next_by_code('loai_van_ban.sequence') or '/'
        return super(LoaiVanBan, self).create(vals)
    
    _sql_constraints = [
        ('ma_loai_unique', 'UNIQUE(ma_loai)', 'Mã loại văn bản đã tồn tại!')
    ]
