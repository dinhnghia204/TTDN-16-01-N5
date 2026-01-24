# -*- coding: utf-8 -*-
from odoo import models, fields, api


class NhanVienExtend(models.Model):
    """Mở rộng model nhan_vien để thêm liên kết với tài sản"""
    _inherit = 'nhan_vien'
    
    # 1. Tài sản đang sử dụng
    tai_san_dang_su_dung_ids = fields.One2many(
        'phan_bo_tai_san', 
        'nhan_vien_su_dung_id', 
        string='Tài sản đang sử dụng',
        domain=[('trang_thai', '=', 'in-use')],
        help='Danh sách tài sản được phân bổ cho nhân viên này'
    )
    so_luong_tai_san = fields.Integer(
        compute='_compute_so_luong_tai_san',
        string='Số lượng tài sản',
        store=True
    )
    
    # 2. Lịch sử mượn tài sản
    don_muon_tai_san_ids = fields.One2many(
        'don_muon_tai_san',
        'nhan_vien_muon_id',
        string='Lịch sử mượn tài sản',
        help='Các đơn mượn tài sản của nhân viên'
    )
    
    # 3. Lịch sử kiểm kê
    kiem_ke_da_thuc_hien_ids = fields.One2many(
        'kiem_ke_tai_san',
        'nhan_vien_kiem_ke_id',
        string='Phiếu kiểm kê đã thực hiện',
        help='Danh sách phiếu kiểm kê do nhân viên này thực hiện'
    )
    
    # 4. Lịch sử luân chuyển
    luan_chuyen_ban_giao_ids = fields.One2many(
        'luan_chuyen_tai_san',
        'nguoi_ban_giao',
        string='Lịch sử bàn giao tài sản',
        help='Các phiếu luân chuyển nhân viên này đã bàn giao'
    )
    luan_chuyen_nhan_ids = fields.One2many(
        'luan_chuyen_tai_san',
        'nguoi_nhan',
        string='Lịch sử nhận tài sản',
        help='Các phiếu luân chuyển nhân viên này đã nhận'
    )
    
    # 5. Lịch sử thanh lý
    thanh_ly_da_thuc_hien_ids = fields.One2many(
        'thanh_ly_tai_san',
        'nguoi_thanh_ly_id',
        string='Lịch sử thanh lý tài sản',
        help='Các tài sản nhân viên này đã thanh lý'
    )
    
    @api.depends('tai_san_dang_su_dung_ids')
    def _compute_so_luong_tai_san(self):
        for record in self:
            record.so_luong_tai_san = len(record.tai_san_dang_su_dung_ids)
