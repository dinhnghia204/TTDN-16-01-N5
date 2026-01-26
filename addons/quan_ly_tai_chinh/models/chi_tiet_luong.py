# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ChiTietLuong(models.Model):
    _name = 'chi_tiet_luong'
    _description = 'Chi tiết lương nhân viên'
    _rec_name = 'nhan_vien_id'

    phieu_luong_id = fields.Many2one('phieu_luong', string='Phiếu lương', required=True, ondelete='cascade')
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', required=True, ondelete='restrict')
    
    # Thông tin nhân viên (related)
    phong_ban_id = fields.Many2one(related='nhan_vien_id.phong_ban_id', string='Phòng ban', store=True, readonly=True)
    chuc_vu_id = fields.Many2one(related='nhan_vien_id.chuc_vu_id', string='Chức vụ', store=True, readonly=True)
    
    # Các khoản lương
    luong_co_ban = fields.Float('Lương cơ bản', required=True, default=0, digits=(16, 2))
    phu_cap = fields.Float('Phụ cấp', default=0, digits=(16, 2))
    phu_cap_chuc_vu = fields.Float('Phụ cấp chức vụ', default=0, digits=(16, 2))
    phu_cap_khac = fields.Float('Phụ cấp khác', default=0, digits=(16, 2))
    thuong = fields.Float('Thưởng', default=0, digits=(16, 2))
    
    # Các khoản trừ
    khoan_tru = fields.Float('Khoản trừ', default=0, digits=(16, 2))
    bao_hiem_xa_hoi = fields.Float('BHXH (8%)', compute='_compute_bao_hiem', store=True, digits=(16, 2))
    bao_hiem_y_te = fields.Float('BHYT (1.5%)', compute='_compute_bao_hiem', store=True, digits=(16, 2))
    bao_hiem_that_nghiep = fields.Float('BHTN (1%)', compute='_compute_bao_hiem', store=True, digits=(16, 2))
    
    # Tổng
    tong_phu_cap = fields.Float('Tổng phụ cấp', compute='_compute_tong_phu_cap', store=True, digits=(16, 2))
    tong_thu_nhap = fields.Float('Tổng thu nhập', compute='_compute_luong_thuc_linh', store=True, digits=(16, 2))
    tong_bao_hiem = fields.Float('Tổng BH', compute='_compute_luong_thuc_linh', store=True, digits=(16, 2))
    luong_thuc_linh = fields.Float('Thực lĩnh', compute='_compute_luong_thuc_linh', store=True, digits=(16, 2))
    
    # Công
    so_ngay_cong = fields.Float('Số ngày công', default=26)
    ngay_nghi = fields.Float('Ngày nghỉ', default=0)
    ngay_lam_thuc_te = fields.Float('Ngày làm thực tế', compute='_compute_ngay_lam_thuc_te', store=True)
    
    ghi_chu = fields.Text('Ghi chú')
    
    @api.depends('phu_cap', 'phu_cap_chuc_vu', 'phu_cap_khac')
    def _compute_tong_phu_cap(self):
        for record in self:
            record.tong_phu_cap = record.phu_cap + record.phu_cap_chuc_vu + record.phu_cap_khac
    
    @api.depends('so_ngay_cong', 'ngay_nghi')
    def _compute_ngay_lam_thuc_te(self):
        for record in self:
            record.ngay_lam_thuc_te = record.so_ngay_cong - record.ngay_nghi
    
    @api.depends('luong_co_ban')
    def _compute_bao_hiem(self):
        """Tính bảo hiểm theo tỷ lệ"""
        for record in self:
            record.bao_hiem_xa_hoi = record.luong_co_ban * 0.08
            record.bao_hiem_y_te = record.luong_co_ban * 0.015
            record.bao_hiem_that_nghiep = record.luong_co_ban * 0.01
    
    @api.depends('luong_co_ban', 'tong_phu_cap', 'thuong', 'khoan_tru',
                 'bao_hiem_xa_hoi', 'bao_hiem_y_te', 'bao_hiem_that_nghiep')
    def _compute_luong_thuc_linh(self):
        for record in self:
            record.tong_thu_nhap = record.luong_co_ban + record.tong_phu_cap + record.thuong
            record.tong_bao_hiem = record.bao_hiem_xa_hoi + record.bao_hiem_y_te + record.bao_hiem_that_nghiep
            record.luong_thuc_linh = record.tong_thu_nhap - record.tong_bao_hiem - record.khoan_tru
    
    @api.constrains('luong_co_ban', 'phu_cap', 'thuong', 'khoan_tru')
    def _check_so_tien(self):
        for record in self:
            if record.luong_co_ban < 0 or record.phu_cap < 0 or record.thuong < 0 or record.khoan_tru < 0:
                raise ValidationError("Các khoản tiền không được âm!")
    
    @api.constrains('so_ngay_cong', 'ngay_nghi')
    def _check_ngay_cong(self):
        for record in self:
            if record.so_ngay_cong < 0 or record.ngay_nghi < 0:
                raise ValidationError("Số ngày công không được âm!")
            if record.ngay_nghi > record.so_ngay_cong:
                raise ValidationError("Ngày nghỉ không được lớn hơn tổng số ngày công!")
