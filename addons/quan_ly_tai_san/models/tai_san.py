from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime

class TaiSan(models.Model):
    _name = 'tai_san'
    _description = 'Bảng chứa thông tin tài sản'
    _rec_name = 'cus_rec_name'
    _order = 'ngay_mua_ts desc'
    _sql_constraints = [
        ("ma_tai_san_unique", "unique(ma_tai_san)", "Mã tài sản đã tồn tại !"),
    ]


    ma_tai_san = fields.Char(
        'Mã tài sản',
        required=False,
        readonly=True,
        copy=False,
        default='/',
    )
    ten_tai_san = fields.Char('Tên tài sản', required=True)
    ngay_mua_ts = fields.Date('Ngày mua tài sản', required=True)
    don_vi_tien_te = fields.Selection([
        ('vnd', 'VNĐ'),
        ('usd', '$'),
    ], string='Đơn vị tiền tệ', default='vnd', required=True)
    gia_tri_ban_dau = fields.Float('Giá trị ban đầu', default = 1, required=True)
    gia_tri_hien_tai = fields.Float('Giá trị hiện tại', default = 1, required=False, readonly=True)
    danh_muc_ts_id = fields.Many2one('danh_muc_tai_san', string='Loại tài sản', required=True, ondelete='restrict')
    giay_to_tai_san = fields.Binary('Giấy tờ liên quan', attachment=True)
    giay_to_tai_san_filename = fields.Char('Tên file')
    hinh_anh = fields.Image('Hình ảnh', max_width=200, max_height=200)

    pp_khau_hao = fields.Selection([
        ('straight-line', 'Tuyến tính'),
        ('degressive', 'Giảm dần'),
        ('none', 'Không')
    ], string='Phương pháp khấu hao', default = 'none', required=True)
    thoi_gian_su_dung = fields.Integer('Thời gian đã sử dụng (năm)', default=0)
    
    # Liên kết với văn bản
    van_ban_mua_sam_id = fields.Many2one('van_ban_di', string='Văn bản đề xuất mua sắm',
                                         help='Văn bản đề xuất/phê duyệt mua sắm tài sản này')

    # Khấu hao tuyến tính
    thoi_gian_toi_da = fields.Integer('Thời gian sử dụng còn lại tối đa (năm)', default=5)

    # Khấu hao giảm dần
    ty_le_khau_hao = fields.Float('Tỷ lệ khấu hao (%)', default=20)

    don_vi_tinh = fields.Char('Đơn vị tính', default = 'Chiếc', required=True)
    ghi_chu = fields.Char('Ghi chú')

    cus_rec_name = fields.Char(compute='_compute_cus_rec_name', store=True)
    @api.depends('ten_tai_san', 'ma_tai_san')
    def _compute_cus_rec_name(self):
        for record in self:
            record.cus_rec_name = record.ma_tai_san + ' - ' + record.ten_tai_san

    phong_ban_su_dung_ids = fields.One2many('phan_bo_tai_san', 'tai_san_id', string='Phòng ban sử dụng')
    lich_su_khau_hao_ids = fields.One2many('lich_su_khau_hao', 'ma_ts', string='Lịch sử khấu hao')
    kiem_ke_history_ids = fields.One2many('kiem_ke_tai_san_line', compute='_compute_kiem_ke_history_ids', string='Lịch sử kiểm kê')
    luan_chuyen_ids = fields.Many2many('luan_chuyen_tai_san', compute='_compute_luan_chuyen_ids', string='Phiếu luân chuyển')
    thanh_ly_ids = fields.One2many('thanh_ly_tai_san', 'tai_san_id', string='Lịch sử thanh lý')
    trang_thai_thanh_ly = fields.Selection([
        ('chua_phan_bo', 'Chưa phân bổ'),
        ('chua_thanh_ly', 'Chưa thanh lý'),
        ('da_phan_bo', 'Đã phân bổ'),
        ('da_thanh_ly', 'Đã thanh lý'),
    ], string='Trạng thái', compute='_compute_trang_thai_thanh_ly', default='chua_phan_bo', store=True)

    lich_su_ky_thuat_ids = fields.One2many(comodel_name='lich_su_ky_thuat', inverse_name='tai_san_id', string='Tình trạng kỹ thuật')
    
    @api.depends('thanh_ly_ids', 'phong_ban_su_dung_ids')
    def _compute_trang_thai_thanh_ly(self):
        for record in self:
            if record.thanh_ly_ids:
                record.trang_thai_thanh_ly = 'da_thanh_ly'
            elif record.phong_ban_su_dung_ids:
                record.trang_thai_thanh_ly = 'da_phan_bo'
            else:
                record.trang_thai_thanh_ly = 'chua_phan_bo'

    
    def _compute_kiem_ke_history_ids(self):
        for record in self:
            phan_bo_ids = self.env['phan_bo_tai_san'].search([('tai_san_id', '=', record.id)]).ids
            record.kiem_ke_history_ids = self.env['kiem_ke_tai_san_line'].search([
                ('phan_bo_tai_san_id', 'in', phan_bo_ids)
            ])
    
    def _compute_luan_chuyen_ids(self):
        for record in self:
            phan_bo_ids = self.env['phan_bo_tai_san'].search([('tai_san_id', '=', record.id)]).ids
            luan_chuyen_lines = self.env['luan_chuyen_tai_san_line'].search([
                ('phan_bo_tai_san_id', 'in', phan_bo_ids)
            ])
            record.luan_chuyen_ids = luan_chuyen_lines.mapped('luan_chuyen_id')

    @api.constrains('gia_tri_ban_dau', 'gia_tri_hien_tai')
    def _check_gia_tri(self):
        for record in self:
            if record.gia_tri_ban_dau < 0 or record.gia_tri_hien_tai < 0:
                raise ValidationError("Giá trị (ban đầu, hiện tại) không thể âm !")
            elif record.gia_tri_hien_tai > record.gia_tri_ban_dau:
                raise ValidationError("Giá trị hiện tại không thể lớn hơn giá trị ban đầu !")

    @api.model
    def create(self, vals):
        if not vals.get('ma_tai_san') or vals.get('ma_tai_san') == '/':
            vals['ma_tai_san'] = self.env['ir.sequence'].next_by_code('tai_san.sequence') or '/'
        
        # Tự động gán giá trị hiện tại = giá trị ban đầu khi tạo mới
        if 'gia_tri_ban_dau' in vals and 'gia_tri_hien_tai' not in vals:
            vals['gia_tri_hien_tai'] = vals['gia_tri_ban_dau']
        
        return super().create(vals)
    
    def action_tinh_khau_hao(self):
        for record in self:
            if record.pp_khau_hao == 'none':
                raise ValidationError("Tài sản này không có phương pháp khấu hao!")
            
            # Kiểm tra thời gian sử dụng hợp lệ
            if record.thoi_gian_su_dung < 0:
                raise ValidationError("Thời gian đã sử dụng không thể âm!")
            
            if record.thoi_gian_su_dung > record.thoi_gian_toi_da:
                raise ValidationError(
                    f"Thời gian đã sử dụng ({record.thoi_gian_su_dung} năm) không thể lớn hơn "
                    f"thời gian tối đa ({record.thoi_gian_toi_da} năm)!"
                )
            
            # Lấy danh sách phiếu khấu hao tự động, sắp xếp theo ngày
            phieu_khau_hao = self.env['lich_su_khau_hao'].search([
                ('ma_ts', '=', record.id),
                ('loai_phieu', '=', 'automatic')
            ], order='ngay_khau_hao asc')
            
            # Kiểm tra nếu phương pháp đã thay đổi
            # Nếu phiếu cũ không có phuong_phap_khau_hao (NULL) hoặc khác với phương pháp hiện tại
            can_xoa_phieu_cu = False
            if phieu_khau_hao:
                phuong_phap_cu = phieu_khau_hao[0].phuong_phap_khau_hao
                # Trường hợp 1: Phiếu cũ không có phương pháp (dữ liệu cũ)
                # Trường hợp 2: Phương pháp đã thay đổi
                if not phuong_phap_cu or phuong_phap_cu != record.pp_khau_hao:
                    can_xoa_phieu_cu = True
            
            if can_xoa_phieu_cu:
                # Hoàn lại giá trị đã khấu hao
                tong_gia_tri_hoan_lai = sum(phieu_khau_hao.mapped('so_tien_khau_hao'))
                record.gia_tri_hien_tai += tong_gia_tri_hoan_lai
                
                # Xóa toàn bộ phiếu cũ
                so_phieu_xoa = len(phieu_khau_hao)
                phuong_phap_cu_text = dict(record._fields['pp_khau_hao'].selection).get(phuong_phap_cu, 'không xác định')
                phuong_phap_moi_text = dict(record._fields['pp_khau_hao'].selection).get(record.pp_khau_hao, '')
                
                phieu_khau_hao.unlink()
                
                self.env['bus.bus']._sendone(
                    self.env.user.partner_id, 
                    'simple_notification', 
                    {
                        'title': 'Đã chuyển phương pháp',
                        'message': f'Đã xóa {so_phieu_xoa} phiếu "{phuong_phap_cu_text}" và hoàn lại {tong_gia_tri_hoan_lai:,.0f} VNĐ. Ấn lại để tính theo "{phuong_phap_moi_text}".',
                        'sticky': False,
                        'type': 'warning'
                    }
                )
                return
            
            so_phieu_da_co = len(phieu_khau_hao)
            so_nam_muc_tieu = record.thoi_gian_su_dung
            
            # TRƯỜNG HỢP 1: Cần xóa phiếu (giảm số năm)
            if so_phieu_da_co > so_nam_muc_tieu:
                so_phieu_can_xoa = so_phieu_da_co - so_nam_muc_tieu
                phieu_can_xoa = phieu_khau_hao[-so_phieu_can_xoa:]  # Lấy n phiếu cuối
                
                # Hoàn lại giá trị đã khấu hao
                tong_gia_tri_hoan_lai = sum(phieu_can_xoa.mapped('so_tien_khau_hao'))
                record.gia_tri_hien_tai += tong_gia_tri_hoan_lai
                
                # Xóa phiếu
                phieu_can_xoa.unlink()
                
                self.env['bus.bus']._sendone(
                    self.env.user.partner_id, 
                    'simple_notification', 
                    {
                        'title': 'Đã hoàn tác',
                        'message': f'Đã xóa {so_phieu_can_xoa} phiếu khấu hao và hoàn lại {tong_gia_tri_hoan_lai:,.0f} VNĐ',
                        'sticky': False,
                        'type': 'info'
                    }
                )
                return
            
            # TRƯỜNG HỢP 2: Đã đủ phiếu
            if so_phieu_da_co == so_nam_muc_tieu:
                raise ValidationError(
                    f"Đã có đủ {so_phieu_da_co} phiếu khấu hao cho {so_nam_muc_tieu} năm!"
                )
            
            # TRƯỜNG HỢP 3: Cần tạo thêm phiếu
            if record.gia_tri_hien_tai <= 0:
                raise ValidationError("Tài sản đã hết giá trị, không thể khấu hao thêm!")
            
            so_nam_can_khau_hao = so_nam_muc_tieu - so_phieu_da_co

            # Lặp qua từng năm cần khấu hao
            for nam in range(so_nam_can_khau_hao):
                if record.gia_tri_hien_tai <= 0:
                    raise ValidationError(
                        f"Tài sản đã hết giá trị sau {nam} năm khấu hao! "
                        f"Không thể tiếp tục khấu hao {so_nam_can_khau_hao - nam} năm còn lại."
                    )
                
                so_tien_khau_hao = 0
                nam_hien_tai = so_phieu_da_co + nam + 1  # Năm thứ mấy đang khấu hao

                if record.pp_khau_hao == 'straight-line':  
                    if record.thoi_gian_toi_da <= 0:
                        raise ValidationError("Thời gian sử dụng tối đa phải lớn hơn 0 (năm) !")
                    so_tien_khau_hao = record.gia_tri_ban_dau / record.thoi_gian_toi_da  

                elif record.pp_khau_hao == 'degressive':  
                    if record.thoi_gian_toi_da <= 0:
                        raise ValidationError("Thời gian sử dụng tối đa phải lớn hơn 0 (năm) !")
                    
                    # 1. Tỷ lệ khấu hao đường thẳng
                    r_dt = 1.0 / record.thoi_gian_toi_da
                    
                    # 2. Hệ số điều chỉnh (H) theo Thông tư 45/2013/TT-BTC
                    if record.thoi_gian_toi_da <= 4:
                        he_so_h = 1.5
                    elif record.thoi_gian_toi_da <= 6:
                        he_so_h = 2.0
                    else:
                        he_so_h = 2.5
                    
                    # 3. Tỷ lệ khấu hao giảm dần
                    r_gd = r_dt * he_so_h
                    
                    # 4. Số năm còn lại
                    so_nam_con_lai = record.thoi_gian_toi_da - nam_hien_tai + 1
                    
                    # 5. Khấu hao giảm dần
                    khau_hao_giam_dan = record.gia_tri_hien_tai * r_gd
                    
                    # 6. Khấu hao đường thẳng (cho số năm còn lại)
                    khau_hao_duong_thang = record.gia_tri_hien_tai / so_nam_con_lai if so_nam_con_lai > 0 else 0
                    
                    # 7. Điều kiện chuyển sang đường thẳng
                    if khau_hao_giam_dan < khau_hao_duong_thang:
                        # Chuyển sang khấu hao đường thẳng
                        so_tien_khau_hao = khau_hao_duong_thang
                    else:
                        # Tiếp tục khấu hao giảm dần
                        so_tien_khau_hao = khau_hao_giam_dan

                so_tien_khau_hao = min(so_tien_khau_hao, record.gia_tri_hien_tai)  
                ma_phieu_khau_hao = 'KH-' + record.ma_tai_san + '-' + datetime.now().strftime('%Y%m%d%H%M%S%f')

                # Tạo phiếu khấu hao - hàm create() sẽ tự động trừ tiền và tính gia_tri_con_lai
                self.env['lich_su_khau_hao'].create({
                    'ma_phieu_khau_hao': ma_phieu_khau_hao,
                    'ma_ts': record.id,
                    'ngay_khau_hao': fields.Datetime.now(),
                    'so_tien_khau_hao': so_tien_khau_hao,
                    'loai_phieu': 'automatic',
                    'phuong_phap_khau_hao': record.pp_khau_hao,
                    'ghi_chu': f'Khấu hao năm {so_phieu_da_co + nam + 1} - {fields.Date.today().strftime("%Y/%m")}'
                })
            
            self.env['bus.bus']._sendone(
                self.env.user.partner_id, 
                'simple_notification', 
                {
                    'title': 'Thành công',
                    'message': f'Đã tạo {so_nam_can_khau_hao} phiếu khấu hao cho tài sản "{record.ten_tai_san}"',
                    'sticky': False,
                    'type': 'success'
                }
            )

