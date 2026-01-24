from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class LichSuKhauHao(models.Model):
    _name = 'lich_su_khau_hao'
    _description = 'lich_su_khau_hao'
    _rec_name = "ma_phieu_khau_hao"
    _order = 'ngay_khau_hao desc'
    _sql_constraints = [
        ("ma_phieu_khau_hao_unique", "unique(ma_phieu_khau_hao)", "Mã phiếu khấu hao đã tồn tại !"),
    ]
    
    ma_phieu_khau_hao = fields.Char(
        'Mã phiếu',
        required=False,
        readonly=True,
        copy=False,
        default='/',
    )
    ma_ts = fields.Many2one('tai_san', string='Mã tài sản', required=True, ondelete='cascade')
    ngay_khau_hao = fields.Datetime('Ngày khấu hao',default = fields.Datetime.now(),  required=True)
    gia_tri_hien_tai = fields.Float(string='Giá trị ban đầu', related='ma_ts.gia_tri_hien_tai', store=True)
    so_tien_khau_hao = fields.Float('Số tiền khấu hao', required=True, default=0)
    gia_tri_con_lai = fields.Float(string='Giá trị còn lại', store=True)
    
    @api.onchange('so_tien_khau_hao')
    def _onchange_so_tien_khau_hao(self):
        for record in self:
            if record.ma_ts:
                record.gia_tri_con_lai = max(0, record.ma_ts.gia_tri_hien_tai - record.so_tien_khau_hao)
    
    loai_phieu = fields.Selection([
        ('automatic', 'Tự động'),
        ('manual', 'Thủ công')
    ], string='Phương thức', required=True, default='manual', readonly=True)
    
    # Lấy thông tin từ tài sản (READONLY - không sửa được)
    phuong_phap_khau_hao = fields.Selection(
        related='ma_ts.pp_khau_hao', 
        string='Phương pháp khấu hao', 
        store=True,
        readonly=True,
        help='Lấy từ cấu hình tài sản'
    )
    thoi_gian_toi_da = fields.Integer(
        related='ma_ts.thoi_gian_toi_da', 
        string='Thời gian sử dụng tối đa (năm)', 
        store=True,
        readonly=True,
        help='Lấy từ cấu hình tài sản'
    )
    
    # Field DUY NHẤT người dùng nhập
    so_nam_khau_hao = fields.Integer('Số năm khấu hao', default=1, help='Số năm cần khấu hao (mặc định 1 năm)')
    
    ghi_chu = fields.Char('Ghi chú')
    
    @api.onchange('so_nam_khau_hao', 'ma_ts')
    def _onchange_tinh_khau_hao_tu_dong(self):
        """Tự động tính số tiền khấu hao dựa trên thông tin từ tài sản"""
        for record in self:
            if record.ma_ts and record.phuong_phap_khau_hao and record.phuong_phap_khau_hao != 'none' and record.thoi_gian_toi_da and record.thoi_gian_toi_da > 0:
                gia_tri_ban_dau = record.ma_ts.gia_tri_ban_dau
                gia_tri_hien_tai = record.ma_ts.gia_tri_hien_tai
                so_nam = record.so_nam_khau_hao or 1
                
                if record.phuong_phap_khau_hao == 'straight-line':
                    # Khấu hao tuyến tính
                    so_tien_1_nam = gia_tri_ban_dau / record.thoi_gian_toi_da
                    record.so_tien_khau_hao = so_tien_1_nam * so_nam
                    
                elif record.phuong_phap_khau_hao == 'degressive':
                    # Khấu hao giảm dần (tính cho số năm đầu tiên)
                    r_dt = 1.0 / record.thoi_gian_toi_da
                    
                    # Hệ số điều chỉnh
                    if record.thoi_gian_toi_da <= 4:
                        he_so_h = 1.5
                    elif record.thoi_gian_toi_da <= 6:
                        he_so_h = 2.0
                    else:
                        he_so_h = 2.5
                    
                    r_gd = r_dt * he_so_h
                    
                    # Tính cho 1 năm (có thể mở rộng cho nhiều năm)
                    khau_hao_giam_dan = gia_tri_hien_tai * r_gd
                    so_nam_con_lai = record.thoi_gian_toi_da
                    khau_hao_duong_thang = gia_tri_hien_tai / so_nam_con_lai if so_nam_con_lai > 0 else 0
                    
                    if khau_hao_giam_dan < khau_hao_duong_thang:
                        record.so_tien_khau_hao = khau_hao_duong_thang * so_nam
                    else:
                        record.so_tien_khau_hao = khau_hao_giam_dan * so_nam
                
                # Giới hạn không vượt quá giá trị hiện tại
                if record.so_tien_khau_hao > gia_tri_hien_tai:
                    record.so_tien_khau_hao = gia_tri_hien_tai
    
    @api.model
    def create(self, vals):
        # Tự động tạo mã phiếu nếu chưa có
        if not vals.get('ma_phieu_khau_hao') or vals.get('ma_phieu_khau_hao') == '/':
            vals['ma_phieu_khau_hao'] = self.env['ir.sequence'].next_by_code('lich_su_khau_hao.sequence') or '/'
        
        tai_san = self.env['tai_san'].browse(vals.get('ma_ts'))
        if tai_san:
            so_tien_khau_hao = vals.get('so_tien_khau_hao', 0)
            
            # Validation
            if tai_san.gia_tri_hien_tai == 0:
                raise ValidationError("Tài sản đã hết giá trị, không thể khấu hao !")
            
            if so_tien_khau_hao > tai_san.gia_tri_hien_tai:
                so_tien_khau_hao = tai_san.gia_tri_hien_tai
                vals['so_tien_khau_hao'] = so_tien_khau_hao  # Cập nhật lại giá trị
            
            # Trừ tiền vào tài sản
            tai_san.gia_tri_hien_tai = max(0, tai_san.gia_tri_hien_tai - so_tien_khau_hao)
            
            # Cập nhật giá trị còn lại
            vals['gia_tri_con_lai'] = tai_san.gia_tri_hien_tai  
        
        return super().create(vals)    
