from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class LuanChuyenTaiSanLine(models.Model):
    _name = 'luan_chuyen_tai_san_line'
    _description = 'Chi tiết luân chuyển tài sản'

    luan_chuyen_id = fields.Many2one('luan_chuyen_tai_san', string='Luân chuyển tài sản', required=True, ondelete='cascade')
    phan_bo_tai_san_id = fields.Many2one('phan_bo_tai_san', string='Tài sản', required=True, ondelete='cascade')
    
    # Thông tin tài sản (readonly, tự động lấy từ phan_bo_tai_san)
    ma_tai_san = fields.Char(related='phan_bo_tai_san_id.tai_san_id.ma_tai_san', string='Mã tài sản', readonly=True, store=True)
    ten_tai_san = fields.Char(related='phan_bo_tai_san_id.tai_san_id.ten_tai_san', string='Tên tài sản', readonly=True, store=True)
    bo_phan_so_huu = fields.Many2one(related='phan_bo_tai_san_id.phong_ban_id', string='Bộ phận sở hữu', readonly=True, store=True)
    
    so_luong = fields.Integer('Số lượng luân chuyển', default=1, readonly=True)
    ghi_chu = fields.Char('Ghi chú', default='')
           