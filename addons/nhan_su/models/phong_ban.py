from odoo import models, fields, api


class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ten_phong_ban'

    ma_phong_ban = fields.Char(
        "Mã phòng ban",
        required=False,
        readonly=True,
        copy=False,
        default='/',
    )
    ten_phong_ban = fields.Char("Tên phòng ban", required=True) 
    lich_su_cong_tac_ids = fields.One2many("lich_su_cong_tac",string="Danh sách lịch sử công tác", inverse_name="phong_ban_id")

    _sql_constraints = [
        ("ma_phong_ban_unique", "unique(ma_phong_ban)", "Mã phòng ban đã tồn tại."),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('ma_phong_ban') or vals.get('ma_phong_ban') == '/':
            vals['ma_phong_ban'] = self.env['ir.sequence'].next_by_code('phong_ban.sequence') or '/'
        return super().create(vals)

    # ids_van_ban_di = fields.One2many('van_ban_di', inverse_name='id_co_quan_ban_hanh', string="Văn bản đi")
