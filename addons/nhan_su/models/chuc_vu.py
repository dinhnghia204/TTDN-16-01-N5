from odoo import models, fields, api


class ChucVu(models.Model):
    _name = 'chuc_vu'
    _description = 'Bảng chứa thông tin chức vụ'
    _rec_name = 'ten_chuc_vu'

    ma_chuc_vu = fields.Char(
        "Mã chức vụ",
        required=False,
        readonly=True,
        copy=False,
        default='/',
    )
    ten_chuc_vu = fields.Char("Tên chức vụ", required=True)  
    lich_su_cong_tac_ids = fields.One2many("lich_su_cong_tac",string="Danh sách lịch sử công tác", inverse_name="chuc_vu_id")

    _sql_constraints = [
        ("ma_chuc_vu_unique", "unique(ma_chuc_vu)", "Mã chức vụ đã tồn tại."),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('ma_chuc_vu') or vals.get('ma_chuc_vu') == '/':
            vals['ma_chuc_vu'] = self.env['ir.sequence'].next_by_code('chuc_vu.sequence') or '/'
        return super().create(vals)
   