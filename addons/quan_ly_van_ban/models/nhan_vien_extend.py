# -*- coding: utf-8 -*-
from odoo import models, fields, api


class NhanVienExtend(models.Model):
    """Extend nhân viên model với các trường liên quan đến văn bản"""
    _inherit = 'nhan_vien'

    # Văn bản đến
    van_ban_den_nhan_ids = fields.One2many(
        'van_ban_den', 
        'nguoi_nhan_id',
        string='Văn bản đến đã nhận',
        help='Danh sách văn bản đến mà nhân viên này đã nhận'
    )
    so_luong_van_ban_den = fields.Integer(
        string='Số văn bản đến',
        compute='_compute_so_luong_van_ban',
        store=True
    )

    # Văn bản đi
    van_ban_di_soan_thao_ids = fields.One2many(
        'van_ban_di',
        'nguoi_soan_thao_id',
        string='Văn bản đi đã soạn thảo',
        help='Danh sách văn bản đi mà nhân viên này đã soạn thảo'
    )
    van_ban_di_ky_ids = fields.One2many(
        'van_ban_di',
        'nguoi_ky_id',
        string='Văn bản đi đã ký duyệt',
        help='Danh sách văn bản đi mà nhân viên này đã ký duyệt'
    )
    so_luong_van_ban_di = fields.Integer(
        string='Số văn bản đi',
        compute='_compute_so_luong_van_ban',
        store=True
    )

    @api.depends('van_ban_den_nhan_ids', 'van_ban_di_soan_thao_ids', 'van_ban_di_ky_ids')
    def _compute_so_luong_van_ban(self):
        """Tính tổng số văn bản liên quan"""
        for record in self:
            record.so_luong_van_ban_den = len(record.van_ban_den_nhan_ids)
            record.so_luong_van_ban_di = len(record.van_ban_di_soan_thao_ids) + len(record.van_ban_di_ky_ids)
