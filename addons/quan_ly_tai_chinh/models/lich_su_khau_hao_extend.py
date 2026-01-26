# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LichSuKhauHaoExtend(models.Model):
    _inherit = 'lich_su_khau_hao'
    
    but_toan_khau_hao_id = fields.Many2one('so_cai_ke_toan', string='Bút toán khấu hao', 
                                           readonly=True, ondelete='set null')
    da_ghi_nhan_ke_toan = fields.Boolean('Đã ghi nhận kế toán', default=False, readonly=True)
    
    @api.model
    def create(self, vals):
        """⭐ MỨC 2: Tự động tạo bút toán khi ghi nhận khấu hao"""
        record = super().create(vals)
        
        # Chỉ tạo bút toán cho khấu hao tự động
        if record.loai_phieu == 'automatic':
            record._tao_but_toan_khau_hao()
        
        return record
    
    def _tao_but_toan_khau_hao(self):
        """Tạo bút toán khấu hao tự động"""
        for record in self:
            if record.da_ghi_nhan_ke_toan:
                continue
            
            # Kiểm tra tài sản có TK khấu hao không
            if not record.ma_ts.tk_khau_hao_id:
                # Không raise error, chỉ skip
                continue
            
            try:
                # Tìm tài khoản chi phí khấu hao
                tk_chi_phi_khau_hao = self.env.ref('quan_ly_tai_chinh.tk_627')
            except:
                # Nếu chưa có TK 627, không tạo bút toán
                continue
            
            # Tạo bút toán: Nợ TK 627 (Chi phí khấu hao) / Có TK 214 (Khấu hao lũy kế)
            but_toan = self.env['so_cai_ke_toan'].create({
                'ngay_hach_toan': record.ngay_khau_hao,
                'ngay_chung_tu': record.ngay_khau_hao,
                'so_chung_tu': record.ma_phieu_khau_hao,
                'loai_chung_tu': 'khau_hao',
                'lich_su_khau_hao_id': record.id,
                'tai_san_id': record.ma_ts.id,
                'dien_giai': f'Khấu hao {record.ma_ts.ten_tai_san} - {record.phuong_phap_khau_hao_display}',
                'chi_tiet_but_toan_ids': [
                    (0, 0, {
                        'tk_no_id': tk_chi_phi_khau_hao.id,
                        'tk_co_id': record.ma_ts.tk_khau_hao_id.id,
                        'so_tien_no': record.so_tien_khau_hao,
                        'so_tien_co': record.so_tien_khau_hao,
                        'dien_giai': f'Khấu hao năm {record.nam}',
                    })
                ],
                'trang_thai': 'da_ghi_so'
            })
            
            record.write({
                'but_toan_khau_hao_id': but_toan.id,
                'da_ghi_nhan_ke_toan': True
            })
    
    def unlink(self):
        """Khi xóa phiếu khấu hao, xóa luôn bút toán liên quan"""
        for record in self:
            if record.but_toan_khau_hao_id:
                # Chỉ xóa nếu bút toán chưa ghi sổ
                if record.but_toan_khau_hao_id.trang_thai == 'nhap':
                    record.but_toan_khau_hao_id.unlink()
        return super().unlink()
    
    def action_xem_but_toan(self):
        """Mở form bút toán liên quan"""
        self.ensure_one()
        if not self.but_toan_khau_hao_id:
            raise ValidationError("Chưa có bút toán cho phiếu khấu hao này!")
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bút toán khấu hao',
            'res_model': 'so_cai_ke_toan',
            'res_id': self.but_toan_khau_hao_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
