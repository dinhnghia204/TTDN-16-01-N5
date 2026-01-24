from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LichSuCongTac(models.Model):
    _name = 'lich_su_cong_tac'
    _description = 'Bảng chứa thông tin lịch sử công tác'
    
    time_start = fields.Date("Thời gian bắt đầu", required=True, default=lambda self: fields.Date.today())
    time_end = fields.Date("Thời gian kết thúc", required=True, default=lambda self: fields.Date.today())
    phong_ban_id = fields.Many2one("phong_ban",string="Phòng ban", required=True)
    chuc_vu_id = fields.Many2one("chuc_vu",string="Chức vụ", required=True)
    nhan_vien_id =fields.Many2one("nhan_vien",string="Nhân viên", required=True)  

    @api.onchange('time_start', 'time_end')
    def _onchange_time_range(self):
        """Bắt lỗi ngay khi chọn ngày trong popup/create nhanh ở tab Nhân viên."""
        today = fields.Date.today()
        for rec in self:
            if rec.time_start and rec.time_end and rec.time_end < rec.time_start:
                raise ValidationError(_("Thời gian kết thúc phải lớn hơn hoặc bằng thời gian bắt đầu."))
            if rec.time_start and rec.time_start > today:
                raise ValidationError(_("Thời gian bắt đầu không được ở tương lai."))

    @api.constrains('time_start', 'time_end')
    def _check_time_range(self):
        today = fields.Date.today()
        for rec in self:
            if rec.time_start and rec.time_end:
                if rec.time_start > rec.time_end:
                    raise ValidationError(_("Thời gian kết thúc phải lớn hơn hoặc bằng thời gian bắt đầu."))
            if rec.time_start and rec.time_start > today:
                raise ValidationError(_("Thời gian bắt đầu không được ở tương lai."))
            # time_end có thể ở hiện tại/tương lai nếu muốn lập kế hoạch; nếu không muốn tương lai, bỏ comment dòng dưới
            # if rec.time_end and rec.time_end > today:
            #     raise ValidationError(_("Thời gian kết thúc không được ở tương lai."))