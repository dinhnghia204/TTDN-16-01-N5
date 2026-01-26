# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ThanhLyTaiSanExtend(models.Model):
    _inherit = 'thanh_ly_tai_san'
    
    but_toan_thanh_ly_id = fields.Many2one('so_cai_ke_toan', string='Bút toán thanh lý', 
                                           readonly=True, ondelete='set null')
    gia_thanh_ly = fields.Float('Giá thanh lý', digits=(16, 2), default=0,
                                help='Số tiền thu được từ thanh lý')
    da_ghi_nhan_ke_toan = fields.Boolean('Đã ghi nhận kế toán', default=False, readonly=True)
    
    # ⭐ Tích hợp với Phiếu thu
    phieu_thu_id = fields.Many2one('phieu_thu', string='Phiếu thu thanh lý', readonly=True, ondelete='set null')
    
    def action_ghi_nhan_thanh_ly(self):
        """⭐ MỨC 2: Tự động tạo bút toán thanh lý"""
        for record in self:
            if record.da_ghi_nhan_ke_toan:
                raise ValidationError("Tài sản này đã được ghi nhận thanh lý!")
            
            tai_san = record.tai_san_id
            
            if not tai_san.tk_nguyen_gia_id or not tai_san.tk_khau_hao_id:
                raise ValidationError("Tài sản chưa có thông tin tài khoản kế toán!")
            
            try:
                tk_tien_mat = self.env.ref('quan_ly_tai_chinh.tk_111')
                tk_thu_nhap_khac = self.env.ref('quan_ly_tai_chinh.tk_711')
                tk_chi_phi_khac = self.env.ref('quan_ly_tai_chinh.tk_811')
            except:
                raise ValidationError("Chưa cài đặt đầy đủ tài khoản kế toán!")
            
            # Tính khấu hao lũy kế
            khau_hao_luy_ke = tai_san.gia_tri_ban_dau - tai_san.gia_tri_hien_tai
            gia_tri_con_lai = tai_san.gia_tri_hien_tai
            
            # Tính lãi/lỗ thanh lý
            lai_lo = record.gia_thanh_ly - gia_tri_con_lai
            
            chi_tiet_lines = []
            
            # 1. Xóa sổ TSCĐ
            # Nợ TK 214 (Khấu hao lũy kế)
            if khau_hao_luy_ke > 0:
                chi_tiet_lines.append((0, 0, {
                    'tk_no_id': tai_san.tk_khau_hao_id.id,
                    'tk_co_id': tai_san.tk_nguyen_gia_id.id,
                    'so_tien_no': khau_hao_luy_ke,
                    'so_tien_co': 0,
                    'dien_giai': 'Xóa sổ khấu hao lũy kế',
                }))
            
            # 2. Thu tiền thanh lý (nếu có)
            if record.gia_thanh_ly > 0:
                chi_tiet_lines.append((0, 0, {
                    'tk_no_id': tk_tien_mat.id,
                    'tk_co_id': tai_san.tk_nguyen_gia_id.id,
                    'so_tien_no': record.gia_thanh_ly,
                    'so_tien_co': 0,
                    'dien_giai': 'Thu tiền thanh lý',
                }))
            
            # 3. Ghi nhận lãi/lỗ
            if lai_lo > 0:
                # Có lãi
                chi_tiet_lines.append((0, 0, {
                    'tk_no_id': tai_san.tk_nguyen_gia_id.id,
                    'tk_co_id': tk_thu_nhap_khac.id,
                    'so_tien_no': 0,
                    'so_tien_co': lai_lo,
                    'dien_giai': f'Lãi thanh lý {abs(lai_lo):,.0f} VNĐ',
                }))
            elif lai_lo < 0:
                # Có lỗ
                chi_tiet_lines.append((0, 0, {
                    'tk_no_id': tk_chi_phi_khac.id,
                    'tk_co_id': tai_san.tk_nguyen_gia_id.id,
                    'so_tien_no': abs(lai_lo),
                    'so_tien_co': 0,
                    'dien_giai': f'Lỗ thanh lý {abs(lai_lo):,.0f} VNĐ',
                }))
            
            # Xóa nguyên giá còn lại (nếu cần cân bằng)
            if gia_tri_con_lai > record.gia_thanh_ly:
                chenh_lech = gia_tri_con_lai - record.gia_thanh_ly
                chi_tiet_lines.append((0, 0, {
                    'tk_no_id': tk_chi_phi_khac.id,
                    'tk_co_id': tai_san.tk_nguyen_gia_id.id,
                    'so_tien_no': chenh_lech,
                    'so_tien_co': 0,
                    'dien_giai': 'Xóa nguyên giá còn lại',
                }))
            
            # Tạo bút toán
            but_toan = self.env['so_cai_ke_toan'].create({
                'ngay_hach_toan': fields.Date.today(),
                'ngay_chung_tu': record.thoi_gian_thanh_ly.date() if record.thoi_gian_thanh_ly else fields.Date.today(),
                'so_chung_tu': record.ma_thanh_ly,
                'loai_chung_tu': 'tai_san',
                'tai_san_id': tai_san.id,
                'dien_giai': f'Thanh lý {tai_san.ten_tai_san}',
                'chi_tiet_but_toan_ids': chi_tiet_lines,
                'trang_thai': 'nhap'  # Để người dùng kiểm tra trước khi ghi sổ
            })
            
            # ⭐ Tạo Phiếu thu (nếu có thu tiền)
            phieu_thu = None
            if record.gia_thanh_ly > 0:
                phieu_thu = self.env['phieu_thu'].create({
                    'ngay_thu': record.thoi_gian_thanh_ly.date() if record.thoi_gian_thanh_ly else fields.Date.today(),
                    'nguoi_nop': 'Thu thanh lý tài sản',
                    'loai_thu': 'tien_mat',
                    'noi_dung': 'thu_khac',
                    'tk_no_id': tk_tien_mat.id,
                    'tk_co_id': tk_thu_nhap_khac.id,
                    'so_tien': record.gia_thanh_ly,
                    'dien_giai': f'Thu tiền thanh lý {tai_san.ten_tai_san}',
                    'but_toan_id': but_toan.id,
                    'trang_thai': 'da_thu'
                })
            
            record.write({
                'but_toan_thanh_ly_id': but_toan.id,
                'phieu_thu_id': phieu_thu.id if phieu_thu else False,
                'da_ghi_nhan_ke_toan': True
            })
        
        # Gửi notification
        phieu_msg = f" + Phiếu thu {self.phieu_thu_id.ma_phieu_thu}" if self.phieu_thu_id else ""
        self.env['bus.bus']._sendone(
            self.env.user.partner_id,
            'simple_notification',
            {
                'title': 'Ghi nhận thanh lý',
                'message': f'Đã tạo bút toán thanh lý {self.ma_thanh_ly}{phieu_msg}. Vui lòng kiểm tra và ghi sổ.',
                'type': 'success',
                'sticky': True
            }
        )
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bút toán thanh lý',
            'res_model': 'so_cai_ke_toan',
            'res_id': self.but_toan_thanh_ly_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
