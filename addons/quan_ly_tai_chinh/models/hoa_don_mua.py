# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HoaDonMua(models.Model):
    _name = 'hoa_don_mua'
    _description = 'Hóa đơn mua hàng'
    _rec_name = 'ma_hoa_don'
    _order = 'ngay_hoa_don desc, id desc'
    
    _sql_constraints = [
        ("ma_hoa_don_unique", "unique(ma_hoa_don)", "Mã hóa đơn đã tồn tại!"),
    ]

    ma_hoa_don = fields.Char('Số hóa đơn', required=False, readonly=True, copy=False, default='/')
    ngay_hoa_don = fields.Date('Ngày hóa đơn', required=True, default=fields.Date.today)
    
    # Nhà cung cấp
    ten_nha_cung_cap = fields.Char('Tên nhà cung cấp', required=True)
    ma_so_thue = fields.Char('Mã số thuế')
    dia_chi = fields.Char('Địa chỉ')
    dien_thoai = fields.Char('Điện thoại')
    
    # Chi tiết hóa đơn
    chi_tiet_ids = fields.One2many('hoa_don_mua_chi_tiet', 'hoa_don_id', string='Chi tiết hóa đơn')
    
    # Tính toán
    tong_tien_hang = fields.Float('Tổng tiền hàng', compute='_compute_tong', store=True, digits=(16, 2))
    
    # VAT
    phuong_thuc_vat = fields.Selection([
        ('0', 'Không chịu thuế (0%)'),
        ('5', 'Thuế suất 5%'),
        ('10', 'Thuế suất 10%')
    ], string='VAT', required=True, default='10')
    
    ty_le_vat = fields.Float('Tỷ lệ VAT (%)', compute='_compute_ty_le_vat', store=True)
    tien_vat = fields.Float('Tiền VAT', compute='_compute_tong', store=True, digits=(16, 2))
    tong_thanh_toan = fields.Float('Tổng thanh toán', compute='_compute_tong', store=True, digits=(16, 2))
    
    # Thanh toán
    hinh_thuc_thanh_toan = fields.Selection([
        ('tien_mat', 'Tiền mặt'),
        ('chuyen_khoan', 'Chuyển khoản'),
        ('cong_no', 'Công nợ')
    ], string='Hình thức thanh toán', required=True, default='cong_no')
    
    # Loại mua
    loai_mua = fields.Selection([
        ('hang_hoa', 'Mua hàng hóa'),
        ('vat_tu', 'Mua vật tư'),
        ('tai_san', 'Mua tài sản'),
        ('dich_vu', 'Mua dịch vụ'),
        ('khac', 'Khác')
    ], string='Loại mua', required=True, default='hang_hoa')
    
    # Ghi chú
    ghi_chu = fields.Text('Ghi chú')
    
    # Liên kết
    but_toan_id = fields.Many2one('so_cai_ke_toan', string='Bút toán', readonly=True, ondelete='set null')
    phieu_chi_ids = fields.One2many('phieu_chi', 'hoa_don_mua_id', string='Phiếu chi')
    tai_san_id = fields.Many2one('tai_san', string='Tài sản (nếu mua TSCĐ)', ondelete='set null')
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('da_nhan', 'Đã nhận HĐ'),
        ('da_thanh_toan', 'Đã thanh toán'),
        ('huy', 'Đã hủy')
    ], string='Trạng thái', default='nhap', required=True)
    
    nguoi_lap_id = fields.Many2one('nhan_vien', string='Người lập', default=lambda self: self._get_nhan_vien_hien_tai())
    
    @api.model
    def create(self, vals):
        if vals.get('ma_hoa_don', '/') == '/':
            vals['ma_hoa_don'] = self.env['ir.sequence'].next_by_code('hoa_don_mua.sequence') or '/'
        return super(HoaDonMua, self).create(vals)
    
    @api.depends('phuong_thuc_vat')
    def _compute_ty_le_vat(self):
        for record in self:
            if record.phuong_thuc_vat:
                record.ty_le_vat = float(record.phuong_thuc_vat)
            else:
                record.ty_le_vat = 0
    
    @api.depends('chi_tiet_ids.thanh_tien', 'ty_le_vat')
    def _compute_tong(self):
        for record in self:
            record.tong_tien_hang = sum(record.chi_tiet_ids.mapped('thanh_tien'))
            record.tien_vat = record.tong_tien_hang * record.ty_le_vat / 100
            record.tong_thanh_toan = record.tong_tien_hang + record.tien_vat
    
    def _get_nhan_vien_hien_tai(self):
        # Lấy nhân viên đầu tiên trong hệ thống làm mặc định
        nhan_vien = self.env['nhan_vien'].search([], limit=1)
        return nhan_vien.id if nhan_vien else False
    
    def action_xac_nhan_nhan(self):
        """Xác nhận nhận hóa đơn và tạo bút toán"""
        for record in self:
            if record.trang_thai != 'nhap':
                raise ValidationError("Chỉ có thể xác nhận ở trạng thái Nháp!")
            
            if not record.chi_tiet_ids:
                raise ValidationError("Hóa đơn phải có ít nhất 1 chi tiết!")
            
            # Chọn TK chi phí dựa trên loại mua
            if record.loai_mua == 'hang_hoa':
                tk_chi_phi = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '156')], limit=1)
                if not tk_chi_phi:
                    tk_chi_phi = self.env['tai_khoan_ke_toan'].create({
                        'ma_tai_khoan': '156',
                        'ten_tai_khoan': 'Hàng hóa',
                        'loai_tai_khoan': 'tai_san',
                        'cap_tai_khoan': 'cap_2',
                        'tinh_chat': 'no'
                    })
            elif record.loai_mua == 'tai_san':
                tk_chi_phi = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '211')], limit=1)
            else:
                tk_chi_phi = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '642')], limit=1)
            
            # TK nguồn tiền
            if record.hinh_thuc_thanh_toan == 'tien_mat':
                tk_nguon = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '111')], limit=1)
            elif record.hinh_thuc_thanh_toan == 'chuyen_khoan':
                tk_nguon = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '112')], limit=1)
            else:  # công nợ
                tk_nguon = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '331')], limit=1)
                if not tk_nguon:
                    tk_nguon = self.env['tai_khoan_ke_toan'].create({
                        'ma_tai_khoan': '331',
                        'ten_tai_khoan': 'Phải trả cho người bán',
                        'ten_tieng_anh': 'Trade payables',
                        'loai_tai_khoan': 'nguon_von',
                        'cap_tai_khoan': 'cap_2',
                        'tinh_chat': 'co',
                        'mo_ta': 'Công nợ phải trả nhà cung cấp',
                        'kich_hoat': True
                    })
            
            # Tạo bút toán
            but_toan = self.env['so_cai_ke_toan'].create({
                'ngay_hach_toan': record.ngay_hoa_don,
                'ngay_chung_tu': record.ngay_hoa_don,
                'so_chung_tu': record.ma_hoa_don,
                'loai_chung_tu': 'khac',
                'dien_giai': f"Mua hàng - NCC: {record.ten_nha_cung_cap}",
                'nguoi_lap_id': record.nguoi_lap_id.id,
                'chi_tiet_but_toan_ids': [(0, 0, {
                    'tk_no_id': tk_chi_phi.id,
                    'tk_co_id': tk_nguon.id,
                    'so_tien': record.tong_thanh_toan,
                    'dien_giai': f"Mua {record.loai_mua} - {record.ten_nha_cung_cap}",
                })]
            })
            
            # Auto ghi sổ
            but_toan.action_ghi_so()
            
            # Update trạng thái
            trang_thai_moi = 'da_thanh_toan' if record.hinh_thuc_thanh_toan != 'cong_no' else 'da_nhan'
            record.write({
                'trang_thai': trang_thai_moi,
                'but_toan_id': but_toan.id
            })
            
            # Notification
            self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                'title': _('Hóa đơn mua'),
                'message': _('Đã xác nhận HĐ mua %s - Tổng tiền: %s VNĐ') % (record.ma_hoa_don, '{:,.0f}'.format(record.tong_thanh_toan)),
                'sticky': False,
            })


class HoaDonMuaChiTiet(models.Model):
    _name = 'hoa_don_mua_chi_tiet'
    _description = 'Chi tiết hóa đơn mua'
    
    hoa_don_id = fields.Many2one('hoa_don_mua', string='Hóa đơn', required=True, ondelete='cascade')
    
    ten_hang_hoa = fields.Char('Tên hàng hóa/Dịch vụ', required=True)
    don_vi_tinh = fields.Char('ĐVT', default='Cái')
    so_luong = fields.Float('Số lượng', required=True, default=1, digits=(12, 2))
    don_gia = fields.Float('Đơn giá', required=True, digits=(16, 2))
    thanh_tien = fields.Float('Thành tiền', compute='_compute_thanh_tien', store=True, digits=(16, 2))
    ghi_chu = fields.Char('Ghi chú')
    
    @api.depends('so_luong', 'don_gia')
    def _compute_thanh_tien(self):
        for record in self:
            record.thanh_tien = record.so_luong * record.don_gia
