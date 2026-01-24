from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_ten'

    ma_dinh_danh = fields.Char(
        "Mã định danh",
        required=False,
        readonly=True,
        copy=False,
        default='/',
    )
    ho_ten = fields.Char("Họ tên", required=True, default='')
    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    phong_ban_id = fields.Many2one("phong_ban", string="Phòng ban", ondelete="set null")
    chuc_vu_id = fields.Many2one("chuc_vu", string="Chức vụ", ondelete="set null")
    lich_su_cong_tac_ids = fields.One2many("lich_su_cong_tac",string="Danh sách lịch sử công tác", inverse_name="nhan_vien_id")
    tuoi = fields.Integer("Tuổi", compute="_compute_tuoi", store=True)
    
    _sql_constraints = [
        ("ma_dinh_danh_unique", "unique(ma_dinh_danh)", "Mã định danh đã tồn tại."),
    ]

    @api.depends('ngay_sinh')
    def _compute_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                record.tuoi = (fields.Date.today() - record.ngay_sinh).days // 365
            else:
                record.tuoi = 0

    @api.constrains('ngay_sinh')
    def _check_age_range(self):
        """Đảm bảo ngày sinh không ở tương lai và tuổi trong khoảng hợp lý."""
        today = fields.Date.today()
        for record in self:
            if not record.ngay_sinh:
                continue

            if record.ngay_sinh > today:
                raise ValidationError(_("Ngày sinh không được ở tương lai."))

            age_years = (today - record.ngay_sinh).days // 365
            if age_years < 18 or age_years > 70:
                raise ValidationError(_("Tuổi nhân viên phải nằm trong khoảng 18 đến 70."))

    @api.model
    def create(self, vals):
        if not vals.get('ma_dinh_danh') or vals.get('ma_dinh_danh') == '/':
            vals['ma_dinh_danh'] = self.env['ir.sequence'].next_by_code('nhan_vien.sequence') or '/'
        return super().create(vals)

    def write(self, vals):
        """Khi đổi Phòng ban/Chức vụ hiện tại, tự thêm dòng lịch sử công tác với ngày hôm nay."""
        track_dept = 'phong_ban_id' in vals
        track_pos = 'chuc_vu_id' in vals
        if not (track_dept or track_pos):
            return super().write(vals)

        today = fields.Date.today()
        res = super().write(vals)

        for rec in self:
            if not rec.phong_ban_id and not rec.chuc_vu_id:
                continue
            # đóng bản ghi lịch sử gần nhất nếu chưa đóng
            last_hist = self.env['lich_su_cong_tac'].search([
                ('nhan_vien_id', '=', rec.id)
            ], order='time_start desc', limit=1)

            if last_hist and (not last_hist.time_end or last_hist.time_end < today):
                last_hist.time_end = today

            self.env['lich_su_cong_tac'].create({
                'nhan_vien_id': rec.id,
                'phong_ban_id': rec.phong_ban_id.id,
                'chuc_vu_id': rec.chuc_vu_id.id,
                'time_start': today,
                'time_end': today,
            })

        return res

    @api.constrains('lich_su_cong_tac_ids')
    def _check_lich_su_cong_tac_dates(self):
        """Chặn nhập ngày bắt đầu/kết thúc không hợp lệ ngay trên tab O2M của nhân viên."""
        today = fields.Date.today()
        for rec in self:
            for line in rec.lich_su_cong_tac_ids:
                if line.time_start and line.time_end and line.time_end < line.time_start:
                    raise ValidationError(_("Thời gian kết thúc phải lớn hơn hoặc bằng thời gian bắt đầu."))
                if line.time_start and line.time_start > today:
                    raise ValidationError(_("Thời gian bắt đầu không được ở tương lai."))


