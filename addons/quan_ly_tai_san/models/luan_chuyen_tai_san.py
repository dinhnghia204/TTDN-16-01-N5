from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class LuanChuyenTaiSan(models.Model):
    _name = 'luan_chuyen_tai_san'
    _description = 'Bảng chứa thông tin Luân chuyển tài sản'
    _rec_name = 'ma_phieu_luan_chuyen'
    _order = 'thoi_gian_luan_chuyen desc'
    _sql_constraints = [
        ("ma_phieu_luan_chuyen_unique", "unique(ma_phieu_luan_chuyen)", "Mã phiếu lưu chuyển đã tồn tại !"),
    ]

    ma_phieu_luan_chuyen = fields.Char(
        'Mã phiếu',
        required=False,
        readonly=True,
        copy=False,
        default='/',
    )
    thoi_gian_luan_chuyen = fields.Datetime('Thời gian luân chuyển', required=True, default=fields.Datetime.now)
    trang_thai = fields.Selection([
        ('chua_luan_chuyen', 'Chưa luân chuyển'),
        ('da_hoan_tat', 'Đã hoàn tất')
    ], string='Trạng thái phiếu', default='chua_luan_chuyen', required=True, readonly=True)
    
    # Thông tin luân chuyển
    bo_phan_nguon = fields.Many2one('phong_ban', string='Bộ phận hiện tại', required=True, ondelete='restrict')
    bo_phan_dich = fields.Many2one('phong_ban', string='Bộ phận nhận', required=True, ondelete='restrict')
    nguoi_ban_giao = fields.Many2one('nhan_vien', string='Người bàn giao', required=True, ondelete='restrict', 
                                     help='Ưu tiên chọn nhân viên thuộc bộ phận hiện tại')
    nguoi_nhan = fields.Many2one('nhan_vien', string='Người nhận', required=True, ondelete='restrict',
                                 help='Ưu tiên chọn nhân viên thuộc bộ phận nhận')
    
    # Kiểm tra ngoại lệ (người không thuộc bộ phận)
    la_ngoai_le_ban_giao = fields.Boolean(compute='_compute_la_ngoai_le', store=True, string='Ngoại lệ bàn giao')
    la_ngoai_le_nhan = fields.Boolean(compute='_compute_la_ngoai_le', store=True, string='Ngoại lệ nhận')
    ly_do_ngoai_le = fields.Text('Lý do ngoại lệ', help='Giải thích tại sao chọn người ngoài bộ phận (bắt buộc khi có ngoại lệ)')
    
    ghi_chu = fields.Text('Lý do luân chuyển', required=True, help='Mô tả chi tiết lý do luân chuyển tài sản')
    
    # Liên kết với văn bản
    van_ban_dieu_chuyen_id = fields.Many2one('van_ban_di', string='Văn bản điều chuyển',
                                             help='Văn bản phê duyệt điều chuyển/luân chuyển tài sản')

    luan_chuyen_line_ids = fields.One2many('luan_chuyen_tai_san_line', 'luan_chuyen_id', string='Danh sách tài sản')

    tai_san_da_chon_ids = fields.Many2many(
        'phan_bo_tai_san', compute='_compute_tai_san_da_chon', store=False
    )

    @api.depends('luan_chuyen_line_ids.phan_bo_tai_san_id')
    def _compute_tai_san_da_chon(self):
        for record in self:
            record.tai_san_da_chon_ids = record.luan_chuyen_line_ids.mapped('phan_bo_tai_san_id')

    @api.depends('nguoi_ban_giao', 'nguoi_nhan', 'bo_phan_nguon', 'bo_phan_dich')
    def _compute_la_ngoai_le(self):
        """Kiểm tra xem người bàn giao/nhận có thuộc đúng bộ phận không"""
        for record in self:
            # Kiểm tra người bàn giao
            if record.nguoi_ban_giao and record.bo_phan_nguon:
                record.la_ngoai_le_ban_giao = record.nguoi_ban_giao.phong_ban_id.id != record.bo_phan_nguon.id
            else:
                record.la_ngoai_le_ban_giao = False
            
            # Kiểm tra người nhận
            if record.nguoi_nhan and record.bo_phan_dich:
                record.la_ngoai_le_nhan = record.nguoi_nhan.phong_ban_id.id != record.bo_phan_dich.id
            else:
                record.la_ngoai_le_nhan = False
    
    @api.onchange('bo_phan_nguon')
    def _onchange_bo_phan_nguon(self):
        if self.bo_phan_nguon:
            self.luan_chuyen_line_ids = [(5, 0, 0)]
            # Gợi ý người bàn giao từ bộ phận nguồn
            if not self.nguoi_ban_giao:
                nhan_vien = self.env['nhan_vien'].search([('phong_ban_id', '=', self.bo_phan_nguon.id)], limit=1)
                if nhan_vien:
                    self.nguoi_ban_giao = nhan_vien
    
    @api.onchange('bo_phan_dich')
    def _onchange_bo_phan_dich(self):
        if self.bo_phan_dich:
            # Gợi ý người nhận từ bộ phận đích
            if not self.nguoi_nhan:
                nhan_vien = self.env['nhan_vien'].search([('phong_ban_id', '=', self.bo_phan_dich.id)], limit=1)
                if nhan_vien:
                    self.nguoi_nhan = nhan_vien
    
    @api.constrains('nguoi_ban_giao', 'nguoi_nhan', 'bo_phan_nguon', 'bo_phan_dich', 'ly_do_ngoai_le')
    def _check_ngoai_le(self):
        """Bắt buộc nhập lý do nếu chọn người ngoài bộ phận"""
        for record in self:
            if (record.la_ngoai_le_ban_giao or record.la_ngoai_le_nhan) and not record.ly_do_ngoai_le:
                nguoi_ngoai_le = []
                if record.la_ngoai_le_ban_giao:
                    nguoi_ngoai_le.append(f"'{record.nguoi_ban_giao.name}' không thuộc bộ phận hiện tại")
                if record.la_ngoai_le_nhan:
                    nguoi_ngoai_le.append(f"'{record.nguoi_nhan.name}' không thuộc bộ phận nhận")
                
                raise ValidationError(
                    f"⚠️ Phát hiện ngoại lệ:\n\n"
                    f"{'• ' + chr(10) + '• '.join(nguoi_ngoai_le)}\n\n"
                    f"Vui lòng nhập 'Lý do ngoại lệ' để giải thích tại sao chọn người ngoài bộ phận.\n"
                    f"(Ví dụ: 'IT bàn giao thay', 'Trưởng phòng ủy quyền', v.v.)"
                )  
    
    @api.model_create_multi
    def create(self, vals):
        records = super().create(vals)
        for rec in records:
            if rec.ma_phieu_luan_chuyen in ('/', False):
                rec.ma_phieu_luan_chuyen = rec.env['ir.sequence'].next_by_code('luan_chuyen_tai_san.sequence') or '/'
        for record in records:
            if record.luan_chuyen_line_ids:
                for line in record.luan_chuyen_line_ids:
                    # Lấy phân bổ tài sản hiện tại
                    phan_bo_tai_san = line.phan_bo_tai_san_id
                    if phan_bo_tai_san:
                        # Cập nhật phong_ban_id sang bộ phận đích
                        phan_bo_tai_san.write({
                            'phong_ban_id': record.bo_phan_dich.id,
                            'vi_tri_tai_san_id': record.bo_phan_dich.id,
                            'ngay_phat': fields.Date.today(),
                            'ghi_chu': f"Lưu ý: Phiếu luân chuyển tài sản - {record.ma_phieu_luan_chuyen}"
                        })
                # Cập nhật trạng thái phiếu sau khi luân chuyển thành công
                record.write({'trang_thai': 'da_hoan_tat'})
        return records
