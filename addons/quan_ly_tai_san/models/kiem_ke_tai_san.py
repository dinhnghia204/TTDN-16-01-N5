from odoo import _, api, fields, models

class KiemKeTaiSan(models.Model):
    _name = 'kiem_ke_tai_san'
    _description = 'Bảng chứa thông tin Kiểm kê tài sản'
    _rec_name = 'rec_name'
    _order = 'thoi_gian_tao desc'
    _sql_constraints = [
        ("ma_phieu_kiem_ke_unique", "unique(ma_phieu_kiem_ke)", "Mã phiếu kiểm kê đã tồn tại !"),
    ]

    rec_name = fields.Char(compute='_compute_rec_name', store=True)
    ma_phieu_kiem_ke = fields.Char(
        'Mã phiếu',
        required=False,
        readonly=True,
        copy=False,
        default='/',
    )
    ten_phieu_kiem_ke = fields.Char('Tên phiếu', required=True)
    phong_ban_id = fields.Many2one('phong_ban', string='Bộ phận cần kiểm kê', required=True, ondelete='cascade')
    nhan_vien_kiem_ke_id = fields.Many2one('nhan_vien', string='Nhân viên kiểm kê', ondelete='set null')
    ds_kiem_ke_ids = fields.One2many(comodel_name='kiem_ke_tai_san_line', 
                                     inverse_name='kiem_ke_tai_san_id', 
                                     string ='Danh sách kiểm kê')
    thoi_gian_tao = fields.Datetime('Thời gian tạo phiếu', default=fields.Datetime.now)
    ghi_chu = fields.Char('Ghi chú', default='')
    trang_thai_phieu = fields.Char(compute='_compute_trang_thai_phieu', string='Trạng thái phiếu', store=True)

    @api.depends('ma_phieu_kiem_ke', 'ten_phieu_kiem_ke')
    def _compute_rec_name(self):
        for record in self:
            record.rec_name = record.ma_phieu_kiem_ke + ' - ' + record.ten_phieu_kiem_ke

    @api.depends('ds_kiem_ke_ids.trang_thai')
    def _compute_trang_thai_phieu(self):
        for rec in self:
            if rec.ds_kiem_ke_ids and all(kiem_ke.trang_thai == 'finished' for kiem_ke in rec.ds_kiem_ke_ids):
                rec.trang_thai_phieu = 'Đã kiểm kê'
            else:
                rec.trang_thai_phieu = 'Chưa kiểm kê'

 

    @api.model
    def create(self, vals):
        if not vals.get('ma_phieu_kiem_ke') or vals.get('ma_phieu_kiem_ke') == '/':
            vals['ma_phieu_kiem_ke'] = self.env['ir.sequence'].next_by_code('kiem_ke_tai_san.sequence') or '/'
        return super().create(vals)
    