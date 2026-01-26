# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class PhieuLuong(models.Model):
    _name = 'phieu_luong'
    _description = 'Phiếu lương nhân viên'
    _rec_name = 'ma_phieu_luong'
    _order = 'nam desc, thang desc'
    
    _sql_constraints = [
        ("ma_phieu_luong_unique", "unique(ma_phieu_luong)", "Mã phiếu lương đã tồn tại!"),
        ("thang_nam_unique", "unique(thang, nam)", "Phiếu lương tháng này đã tồn tại!"),
    ]

    ma_phieu_luong = fields.Char('Mã phiếu', required=False, readonly=True, copy=False, default='/')
    ten_phieu = fields.Char('Tên phiếu', compute='_compute_ten_phieu', store=True)
    
    thang = fields.Integer('Tháng', required=True, default=lambda self: datetime.now().month)
    nam = fields.Integer('Năm', required=True, default=lambda self: datetime.now().year)
    ngay_cham_cong = fields.Date('Ngày chốt công', required=True, default=fields.Date.today)
    ngay_chi_tra = fields.Date('Ngày dự kiến chi trả')
    
    # Chi tiết lương
    chi_tiet_luong_ids = fields.One2many('chi_tiet_luong', 'phieu_luong_id', string='Chi tiết lương')
    
    # Tổng hợp
    tong_luong_co_ban = fields.Float('Tổng lương cơ bản', compute='_compute_tong_luong', store=True, digits=(16, 2))
    tong_phu_cap = fields.Float('Tổng phụ cấp', compute='_compute_tong_luong', store=True, digits=(16, 2))
    tong_thuong = fields.Float('Tổng thưởng', compute='_compute_tong_luong', store=True, digits=(16, 2))
    tong_khoan_tru = fields.Float('Tổng khoản trừ', compute='_compute_tong_luong', store=True, digits=(16, 2))
    tong_luong = fields.Float('Tổng thực lĩnh', compute='_compute_tong_luong', store=True, digits=(16, 2))
    
    # Link tự động tạo bút toán
    but_toan_id = fields.Many2one('so_cai_ke_toan', string='Bút toán', readonly=True, ondelete='set null')
    
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('da_duyet', 'Đã duyệt'),
        ('da_chi_tra', 'Đã chi trả')
    ], string='Trạng thái', default='nhap', required=True)
    
    nguoi_duyet_id = fields.Many2one('nhan_vien', string='Người duyệt')
    ngay_duyet = fields.Datetime('Ngày duyệt', readonly=True)
    
    ghi_chu = fields.Text('Ghi chú')
    
    @api.depends('thang', 'nam')
    def _compute_ten_phieu(self):
        for record in self:
            record.ten_phieu = f"Phiếu lương tháng {record.thang}/{record.nam}"
    
    @api.depends('chi_tiet_luong_ids.luong_co_ban', 'chi_tiet_luong_ids.phu_cap', 
                 'chi_tiet_luong_ids.thuong', 'chi_tiet_luong_ids.khoan_tru',
                 'chi_tiet_luong_ids.luong_thuc_linh')
    def _compute_tong_luong(self):
        for record in self:
            record.tong_luong_co_ban = sum(record.chi_tiet_luong_ids.mapped('luong_co_ban'))
            record.tong_phu_cap = sum(record.chi_tiet_luong_ids.mapped('phu_cap'))
            record.tong_thuong = sum(record.chi_tiet_luong_ids.mapped('thuong'))
            record.tong_khoan_tru = sum(record.chi_tiet_luong_ids.mapped('khoan_tru'))
            record.tong_luong = sum(record.chi_tiet_luong_ids.mapped('luong_thuc_linh'))
    
    @api.constrains('thang', 'nam')
    def _check_thang_nam(self):
        for record in self:
            if record.thang < 1 or record.thang > 12:
                raise ValidationError("Tháng phải từ 1 đến 12!")
            if record.nam < 2000 or record.nam > 2100:
                raise ValidationError("Năm không hợp lệ!")
    
    @api.model
    def create(self, vals):
        if not vals.get('ma_phieu_luong') or vals.get('ma_phieu_luong') == '/':
            vals['ma_phieu_luong'] = self.env['ir.sequence'].next_by_code('phieu_luong.sequence') or '/'
        return super().create(vals)
    
    def action_tao_chi_tiet_tu_nhan_vien(self):
        """Tự động tạo chi tiết lương từ danh sách nhân viên"""
        for record in self:
            # Xóa chi tiết cũ nếu có
            record.chi_tiet_luong_ids.unlink()
            
            # Lấy tất cả nhân viên đang hoạt động
            nhan_viens = self.env['nhan_vien'].search([])
            
            # Tạo chi tiết cho từng nhân viên
            for nv in nhan_viens:
                self.env['chi_tiet_luong'].create({
                    'phieu_luong_id': record.id,
                    'nhan_vien_id': nv.id,
                    'luong_co_ban': 5000000,  # Mặc định 5 triệu
                    'phu_cap': 0,
                    'thuong': 0,
                    'khoan_tru': 0,
                })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': f'Đã tạo chi tiết lương cho {len(nhan_viens)} nhân viên',
                'type': 'success',
                'sticky': False,
            }
        }
    
    def action_duyet_phieu_luong(self):
        """⭐ MỨC 2: Automation - Tự động tạo bút toán khi duyệt"""
        for record in self:
            if not record.chi_tiet_luong_ids:
                raise ValidationError("Phiếu lương chưa có chi tiết!")
            
            if record.trang_thai != 'nhap':
                raise ValidationError("Chỉ có thể duyệt phiếu ở trạng thái Nháp!")
            
            # Tìm tài khoản kế toán
            try:
                tk_chi_phi_luong = self.env.ref('quan_ly_tai_chinh.tk_622')
                tk_phai_tra_nv = self.env.ref('quan_ly_tai_chinh.tk_334')
            except:
                raise ValidationError(
                    "Chưa cài đặt tài khoản kế toán!\n"
                    "Vui lòng kiểm tra data/tai_khoan_ke_toan_data.xml"
                )
            
            # Tạo bút toán
            but_toan = self.env['so_cai_ke_toan'].create({
                'ngay_hach_toan': fields.Date.today(),
                'ngay_chung_tu': record.ngay_cham_cong,
                'so_chung_tu': record.ma_phieu_luong,
                'loai_chung_tu': 'luong',
                'phieu_luong_id': record.id,
                'dien_giai': f'Chi lương tháng {record.thang}/{record.nam}',
                'chi_tiet_but_toan_ids': [
                    (0, 0, {
                        'tk_no_id': tk_chi_phi_luong.id,
                        'tk_co_id': tk_phai_tra_nv.id,
                        'so_tien_no': record.tong_luong,
                        'so_tien_co': record.tong_luong,
                        'dien_giai': f'Chi lương {len(record.chi_tiet_luong_ids)} nhân viên',
                    })
                ],
                'trang_thai': 'da_ghi_so'
            })
            
            record.write({
                'but_toan_id': but_toan.id,
                'trang_thai': 'da_duyet',
                'ngay_duyet': fields.Datetime.now(),
            })
        
        # Gửi notification
        self.env['bus.bus']._sendone(
            self.env.user.partner_id,
            'simple_notification',
            {
                'title': 'Duyệt phiếu lương thành công',
                'message': f'Đã duyệt phiếu {self.ma_phieu_luong} và tạo bút toán tự động',
                'sticky': False,
                'type': 'success'
            }
        )
    
    def action_chi_tra_luong(self):
        """Chi trả lương - Tạo bút toán chi tiền"""
        for record in self:
            if record.trang_thai != 'da_duyet':
                raise ValidationError("Chỉ có thể chi trả phiếu đã duyệt!")
            
            # Tìm tài khoản
            tk_phai_tra_nv = self.env.ref('quan_ly_tai_chinh.tk_334')
            tk_tien_mat = self.env.ref('quan_ly_tai_chinh.tk_111')
            
            # Tạo bút toán chi tiền
            but_toan_chi = self.env['so_cai_ke_toan'].create({
                'ngay_hach_toan': fields.Date.today(),
                'ngay_chung_tu': fields.Date.today(),
                'so_chung_tu': record.ma_phieu_luong + '/CT',
                'loai_chung_tu': 'luong',
                'phieu_luong_id': record.id,
                'dien_giai': f'Chi trả lương tháng {record.thang}/{record.nam}',
                'chi_tiet_but_toan_ids': [
                    (0, 0, {
                        'tk_no_id': tk_phai_tra_nv.id,
                        'tk_co_id': tk_tien_mat.id,
                        'so_tien_no': record.tong_luong,
                        'so_tien_co': record.tong_luong,
                        'dien_giai': 'Chi tiền mặt',
                    })
                ],
                'trang_thai': 'da_ghi_so'
            })
            
            record.trang_thai = 'da_chi_tra'
        
        self.env['bus.bus']._sendone(
            self.env.user.partner_id,
            'simple_notification',
            {
                'title': 'Chi trả thành công',
                'message': f'Đã chi trả lương {self.ma_phieu_luong}',
                'type': 'success'
            }
        )
