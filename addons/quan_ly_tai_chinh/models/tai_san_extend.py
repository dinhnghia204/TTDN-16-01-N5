# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TaiSanExtend(models.Model):
    _inherit = 'tai_san'
    
    # ⭐ Extend model tài sản với thông tin kế toán
    tk_nguyen_gia_id = fields.Many2one('tai_khoan_ke_toan', string='TK Nguyên giá',
                                       help='Tài khoản ghi nhận nguyên giá TSCĐ (thường là TK 211)',
                                       domain="[('ma_tai_khoan', 'like', '21%')]")
    tk_khau_hao_id = fields.Many2one('tai_khoan_ke_toan', string='TK Khấu hao lũy kế',
                                     help='Tài khoản ghi nhận khấu hao lũy kế (thường là TK 214)',
                                     domain="[('ma_tai_khoan', 'like', '214')]")
    
    but_toan_mua_id = fields.Many2one('so_cai_ke_toan', string='Bút toán mua', readonly=True, ondelete='set null')
    da_ghi_nhan_mua = fields.Boolean('Đã ghi nhận mua', default=False, readonly=True)
    
    # ⭐ Tích hợp với Hóa đơn & Phiếu chi
    hoa_don_mua_id = fields.Many2one('hoa_don_mua', string='Hóa đơn mua TSCĐ', readonly=True, ondelete='set null')
    phieu_chi_id = fields.Many2one('phieu_chi', string='Phiếu chi mua TSCĐ', readonly=True, ondelete='set null')
    
    def action_ghi_nhan_mua_tai_san(self):
        """⭐ MỨC 3: Tự động tạo Hóa đơn mua + Phiếu chi + Bút toán khi mua tài sản"""
        for record in self:
            if record.da_ghi_nhan_mua:
                raise ValidationError("Tài sản này đã được ghi nhận mua!")
            
            if not record.tk_nguyen_gia_id:
                raise ValidationError("Chưa chọn tài khoản nguyên giá!")
            
            # 1️⃣ Tạo Hóa đơn mua TSCĐ
            hoa_don = self.env['hoa_don_mua'].create({
                'ngay_hoa_don': record.ngay_mua_ts,
                'ten_nha_cung_cap': 'Nhà cung cấp TSCĐ',
                'loai_mua': 'tai_san',
                'hinh_thuc_thanh_toan': 'tien_mat',
                'phuong_thuc_vat': '0',  # TSCĐ thường không VAT hoặc tách riêng
                'tai_san_id': record.id,
                'ghi_chu': f'Hóa đơn mua tài sản {record.ma_tai_san} - {record.ten_tai_san}',
                'trang_thai': 'da_nhan'
            })
            
            # Thêm chi tiết hóa đơn
            self.env['hoa_don_mua_chi_tiet'].create({
                'hoa_don_id': hoa_don.id,
                'ten_hang_hoa': f'{record.ma_tai_san} - {record.ten_tai_san}',
                'don_vi_tinh': 'Cái',
                'so_luong': 1,
                'don_gia': record.gia_tri_ban_dau,
            })
            
            # 2️⃣ Tạo Phiếu chi thanh toán
            try:
                tk_tien_mat = self.env.ref('quan_ly_tai_chinh.tk_111')
            except:
                raise ValidationError("Chưa cài đặt tài khoản tiền mặt (TK 111)!")
            
            phieu_chi = self.env['phieu_chi'].create({
                'ngay_chi': record.ngay_mua_ts,
                'nguoi_nhan': 'Nhà cung cấp TSCĐ',
                'loai_chi': 'tien_mat',
                'noi_dung': 'chi_khac',
                'tk_no_id': record.tk_nguyen_gia_id.id,
                'tk_co_id': tk_tien_mat.id,
                'so_tien': record.gia_tri_ban_dau,
                'dien_giai': f'Chi tiền mua {record.ten_tai_san}',
                'hoa_don_mua_id': hoa_don.id,
                'tai_san_id': record.id,
                'trang_thai': 'da_chi'
            })
            
            # 3️⃣ Tạo bút toán: Nợ TK 211 (TSCĐ) / Có TK 111 (Tiền mặt)
            but_toan = self.env['so_cai_ke_toan'].create({
                'ngay_hach_toan': fields.Date.today(),
                'ngay_chung_tu': record.ngay_mua_ts,
                'so_chung_tu': hoa_don.ma_hoa_don,
                'loai_chung_tu': 'tai_san',
                'tai_san_id': record.id,
                'dien_giai': f'Mua {record.ten_tai_san}',
                'chi_tiet_but_toan_ids': [
                    (0, 0, {
                        'tk_no_id': record.tk_nguyen_gia_id.id,
                        'tk_co_id': tk_tien_mat.id,
                        'so_tien_no': record.gia_tri_ban_dau,
                        'so_tien_co': record.gia_tri_ban_dau,
                        'dien_giai': f'Mua tài sản {record.ma_tai_san}',
                    })
                ],
                'trang_thai': 'da_ghi_so'
            })
            
            # 4️⃣ Liên kết ngược
            phieu_chi.but_toan_id = but_toan.id
            hoa_don.but_toan_id = but_toan.id
            
            record.write({
                'but_toan_mua_id': but_toan.id,
                'hoa_don_mua_id': hoa_don.id,
                'phieu_chi_id': phieu_chi.id,
                'da_ghi_nhan_mua': True
            })
        
        # Gửi notification
        self.env['bus.bus']._sendone(
            self.env.user.partner_id,
            'simple_notification',
            {
                'title': 'Ghi nhận mua tài sản',
                'message': f'Đã tạo Hóa đơn + Phiếu chi + Bút toán cho tài sản {self.ma_tai_san}',
                'type': 'success',
                'sticky': False
            }
        )
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': f'Đã tích hợp đầy đủ: Hóa đơn {self.hoa_don_mua_id.ma_hoa_don} → Phiếu chi {self.phieu_chi_id.ma_phieu_chi} → Bút toán {self.but_toan_mua_id.id}',
                'type': 'success',
            }
        }
    
    @api.model
    def create(self, vals):
        """Tự động gán tài khoản mặc định khi tạo tài sản"""
        record = super().create(vals)
        
        # Tự động gán TK 211 và TK 214 nếu chưa có
        if not record.tk_nguyen_gia_id:
            try:
                tk_211 = self.env.ref('quan_ly_tai_chinh.tk_211')
                record.tk_nguyen_gia_id = tk_211.id
            except:
                pass
        
        if not record.tk_khau_hao_id:
            try:
                tk_214 = self.env.ref('quan_ly_tai_chinh.tk_214')
                record.tk_khau_hao_id = tk_214.id
            except:
                pass
        
        return record
