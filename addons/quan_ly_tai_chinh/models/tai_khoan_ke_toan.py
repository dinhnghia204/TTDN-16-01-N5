# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TaiKhoanKeToan(models.Model):
    _name = 'tai_khoan_ke_toan'
    _description = 'Danh mục tài khoản kế toán'
    _rec_name = 'ma_tai_khoan'
    _order = 'ma_tai_khoan'
    
    _sql_constraints = [
        ("ma_tai_khoan_unique", "unique(ma_tai_khoan)", "Mã tài khoản đã tồn tại!"),
    ]

    ma_tai_khoan = fields.Char('Mã tài khoản', required=True, size=10)
    ten_tai_khoan = fields.Char('Tên tài khoản', required=True)
    ten_tieng_anh = fields.Char('Tên tiếng Anh')
    
    loai_tai_khoan = fields.Selection([
        ('tai_san', 'Tài sản'),
        ('nguon_von', 'Nguồn vốn'),
        ('chi_phi', 'Chi phí'),
        ('doanh_thu', 'Doanh thu'),
        ('thu_nhap_khac', 'Thu nhập khác'),
        ('chi_phi_khac', 'Chi phí khác')
    ], string='Loại tài khoản', required=True)
    
    cap_tai_khoan = fields.Selection([
        ('cap_1', 'Cấp 1'),
        ('cap_2', 'Cấp 2'),
        ('cap_3', 'Cấp 3')
    ], string='Cấp tài khoản', required=True, default='cap_1')
    
    tk_cha_id = fields.Many2one('tai_khoan_ke_toan', string='Tài khoản cha', ondelete='restrict',
                                domain="[('cap_tai_khoan', '!=', 'cap_3')]")
    tk_con_ids = fields.One2many('tai_khoan_ke_toan', 'tk_cha_id', string='Tài khoản con')
    
    tinh_chat = fields.Selection([
        ('no', 'Bên Nợ'),
        ('co', 'Bên Có'),
        ('no_co', 'Lưỡng tính')
    ], string='Tính chất', required=True, default='no_co')
    
    mo_ta = fields.Text('Mô tả')
    kich_hoat = fields.Boolean('Kích hoạt', default=True)
    
    # Computed fields
    ten_day_du = fields.Char('Tên đầy đủ', compute='_compute_ten_day_du', store=True)
    
    @api.depends('ma_tai_khoan', 'ten_tai_khoan')
    def _compute_ten_day_du(self):
        for record in self:
            record.ten_day_du = f"{record.ma_tai_khoan} - {record.ten_tai_khoan}"
    
    @api.constrains('tk_cha_id', 'cap_tai_khoan')
    def _check_cap_tai_khoan(self):
        for record in self:
            if record.tk_cha_id:
                if record.cap_tai_khoan == 'cap_1':
                    raise ValidationError("Tài khoản cấp 1 không thể có tài khoản cha!")
                if record.tk_cha_id.cap_tai_khoan == 'cap_3':
                    raise ValidationError("Tài khoản cha không thể là cấp 3!")
