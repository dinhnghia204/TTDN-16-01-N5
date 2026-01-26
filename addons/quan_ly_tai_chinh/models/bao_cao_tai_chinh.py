# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime, timedelta


class BaoCaoTaiChinh(models.Model):
    _name = 'bao_cao_tai_chinh'
    _description = 'Dashboard và Báo cáo tài chính'
    _auto = False

    @api.model
    def name_get(self):
        return [(record.id, "Báo cáo tài chính") for record in self]
    
    @api.model
    def get_dashboard_data(self):
        """Dashboard tổng quan tài chính"""
        
        # Tổng số bút toán
        tong_but_toan = self.env['so_cai_ke_toan'].search_count([])
        but_toan_da_ghi_so = self.env['so_cai_ke_toan'].search_count([('trang_thai', '=', 'da_ghi_so')])
        but_toan_nhap = self.env['so_cai_ke_toan'].search_count([('trang_thai', '=', 'nhap')])
        
        # Tổng phát sinh trong tháng
        dau_thang = fields.Date.today().replace(day=1)
        but_toan_thang_nay = self.env['so_cai_ke_toan'].search([
            ('ngay_hach_toan', '>=', dau_thang),
            ('trang_thai', '=', 'da_ghi_so')
        ])
        tong_phat_sinh_no = sum(but_toan_thang_nay.mapped('tong_no'))
        tong_phat_sinh_co = sum(but_toan_thang_nay.mapped('tong_co'))
        
        # Thống kê phiếu lương
        tong_phieu_luong = self.env['phieu_luong'].search_count([])
        phieu_luong_da_duyet = self.env['phieu_luong'].search_count([('trang_thai', '=', 'da_duyet')])
        phieu_luong_da_chi_tra = self.env['phieu_luong'].search_count([('trang_thai', '=', 'da_chi_tra')])
        
        # Tổng chi phí lương tháng này
        phieu_luong_thang = self.env['phieu_luong'].search([
            ('thang', '=', datetime.now().month),
            ('nam', '=', datetime.now().year)
        ])
        tong_luong_thang = sum(phieu_luong_thang.mapped('tong_luong'))
        
        # Thống kê theo loại chứng từ
        loai_chung_tu_stats = []
        for loai in ['tai_san', 'luong', 'khau_hao', 'khac']:
            count = self.env['so_cai_ke_toan'].search_count([
                ('loai_chung_tu', '=', loai),
                ('trang_thai', '=', 'da_ghi_so')
            ])
            if count > 0:
                loai_name = dict(self.env['so_cai_ke_toan']._fields['loai_chung_tu'].selection).get(loai)
                loai_chung_tu_stats.append({
                    'name': loai_name,
                    'count': count
                })
        
        # Biểu đồ bút toán theo tháng (6 tháng gần nhất)
        but_toan_theo_thang = []
        for i in range(5, -1, -1):
            thang_hien_tai = datetime.now() - timedelta(days=30*i)
            dau_thang_tmp = thang_hien_tai.replace(day=1).date()
            
            if thang_hien_tai.month == 12:
                cuoi_thang_tmp = thang_hien_tai.replace(day=31).date()
            else:
                cuoi_thang_tmp = (thang_hien_tai.replace(day=1, month=thang_hien_tai.month+1) - timedelta(days=1)).date()
            
            count = self.env['so_cai_ke_toan'].search_count([
                ('ngay_hach_toan', '>=', dau_thang_tmp),
                ('ngay_hach_toan', '<=', cuoi_thang_tmp),
                ('trang_thai', '=', 'da_ghi_so')
            ])
            
            but_toan_theo_thang.append({
                'thang': f"{thang_hien_tai.month}/{thang_hien_tai.year}",
                'count': count
            })
        
        return {
            'tong_but_toan': tong_but_toan,
            'but_toan_da_ghi_so': but_toan_da_ghi_so,
            'but_toan_nhap': but_toan_nhap,
            'tong_phat_sinh_no': tong_phat_sinh_no,
            'tong_phat_sinh_co': tong_phat_sinh_co,
            'tong_phieu_luong': tong_phieu_luong,
            'phieu_luong_da_duyet': phieu_luong_da_duyet,
            'phieu_luong_da_chi_tra': phieu_luong_da_chi_tra,
            'tong_luong_thang': tong_luong_thang,
            'loai_chung_tu_stats': loai_chung_tu_stats,
            'but_toan_theo_thang': but_toan_theo_thang,
        }
    
    @api.model
    def get_bang_can_doi_ke_toan(self, tu_ngay, den_ngay):
        """Báo cáo Bảng cân đối kế toán (đơn giản)"""
        
        # Lấy tất cả bút toán trong kỳ
        but_toans = self.env['so_cai_ke_toan'].search([
            ('ngay_hach_toan', '>=', tu_ngay),
            ('ngay_hach_toan', '<=', den_ngay),
            ('trang_thai', '=', 'da_ghi_so')
        ])
        
        # Tính số dư theo từng loại tài khoản
        tai_khoan_stats = {}
        
        for but_toan in but_toans:
            for chi_tiet in but_toan.chi_tiet_but_toan_ids:
                # Tài khoản Nợ
                if chi_tiet.tk_no_id.id not in tai_khoan_stats:
                    tai_khoan_stats[chi_tiet.tk_no_id.id] = {
                        'ma_tk': chi_tiet.tk_no_id.ma_tai_khoan,
                        'ten_tk': chi_tiet.tk_no_id.ten_tai_khoan,
                        'loai': chi_tiet.tk_no_id.loai_tai_khoan,
                        'phat_sinh_no': 0,
                        'phat_sinh_co': 0
                    }
                tai_khoan_stats[chi_tiet.tk_no_id.id]['phat_sinh_no'] += chi_tiet.so_tien_no
                
                # Tài khoản Có
                if chi_tiet.tk_co_id.id not in tai_khoan_stats:
                    tai_khoan_stats[chi_tiet.tk_co_id.id] = {
                        'ma_tk': chi_tiet.tk_co_id.ma_tai_khoan,
                        'ten_tk': chi_tiet.tk_co_id.ten_tai_khoan,
                        'loai': chi_tiet.tk_co_id.loai_tai_khoan,
                        'phat_sinh_no': 0,
                        'phat_sinh_co': 0
                    }
                tai_khoan_stats[chi_tiet.tk_co_id.id]['phat_sinh_co'] += chi_tiet.so_tien_co
        
        # Tính số dư
        for tk_id, data in tai_khoan_stats.items():
            data['so_du'] = data['phat_sinh_no'] - data['phat_sinh_co']
        
        # Phân loại
        tai_san = {k: v for k, v in tai_khoan_stats.items() if v['loai'] == 'tai_san'}
        nguon_von = {k: v for k, v in tai_khoan_stats.items() if v['loai'] == 'nguon_von'}
        
        return {
            'tu_ngay': tu_ngay,
            'den_ngay': den_ngay,
            'tai_san': list(tai_san.values()),
            'nguon_von': list(nguon_von.values()),
            'tong_tai_san': sum([v['so_du'] for v in tai_san.values()]),
            'tong_nguon_von': sum([v['so_du'] for v in nguon_von.values()]),
        }
    
    @api.model
    def get_bao_cao_ket_qua_kinh_doanh(self, tu_ngay, den_ngay):
        """Báo cáo Kết quả kinh doanh"""
        
        but_toans = self.env['so_cai_ke_toan'].search([
            ('ngay_hach_toan', '>=', tu_ngay),
            ('ngay_hach_toan', '<=', den_ngay),
            ('trang_thai', '=', 'da_ghi_so')
        ])
        
        doanh_thu = 0
        chi_phi = 0
        
        for but_toan in but_toans:
            for chi_tiet in but_toan.chi_tiet_but_toan_ids:
                # Doanh thu (TK 5xx, 7xx)
                if chi_tiet.tk_co_id.ma_tai_khoan and chi_tiet.tk_co_id.ma_tai_khoan[0] in ['5', '7']:
                    doanh_thu += chi_tiet.so_tien_co
                
                # Chi phí (TK 6xx, 8xx)
                if chi_tiet.tk_no_id.ma_tai_khoan and chi_tiet.tk_no_id.ma_tai_khoan[0] in ['6', '8']:
                    chi_phi += chi_tiet.so_tien_no
        
        loi_nhuan = doanh_thu - chi_phi
        
        return {
            'tu_ngay': tu_ngay,
            'den_ngay': den_ngay,
            'doanh_thu': doanh_thu,
            'chi_phi': chi_phi,
            'loi_nhuan': loi_nhuan,
        }
    
    @api.model
    def get_bao_cao_so_quy(self, tu_ngay, den_ngay):
        """Báo cáo Sổ quỹ tiền mặt"""
        
        # Số dư đầu kỳ (TK 111)
        tk_111 = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '111')], limit=1)
        
        # Lấy tất cả giao dịch trong kỳ
        chi_tiets = self.env['chi_tiet_but_toan'].search([
            ('but_toan_id.ngay_hach_toan', '>=', tu_ngay),
            ('but_toan_id.ngay_hach_toan', '<=', den_ngay),
            ('but_toan_id.trang_thai', '=', 'da_ghi_so'),
            '|',
            ('tk_no_id', '=', tk_111.id),
            ('tk_co_id', '=', tk_111.id)
        ], order='but_toan_id.ngay_hach_toan asc')
        
        giao_dichs = []
        tong_thu = 0
        tong_chi = 0
        
        for chi_tiet in chi_tiets:
            if chi_tiet.tk_no_id.id == tk_111.id:
                # Thu tiền
                tong_thu += chi_tiet.so_tien_no
                giao_dichs.append({
                    'ngay': chi_tiet.but_toan_id.ngay_hach_toan,
                    'chung_tu': chi_tiet.but_toan_id.so_chung_tu,
                    'dien_giai': chi_tiet.dien_giai,
                    'thu': chi_tiet.so_tien_no,
                    'chi': 0
                })
            else:
                # Chi tiền
                tong_chi += chi_tiet.so_tien_co
                giao_dichs.append({
                    'ngay': chi_tiet.but_toan_id.ngay_hach_toan,
                    'chung_tu': chi_tiet.but_toan_id.so_chung_tu,
                    'dien_giai': chi_tiet.dien_giai,
                    'thu': 0,
                    'chi': chi_tiet.so_tien_co
                })
        
        return {
            'tu_ngay': tu_ngay,
            'den_ngay': den_ngay,
            'giao_dichs': giao_dichs,
            'tong_thu': tong_thu,
            'tong_chi': tong_chi,
            'ton_cuoi_ky': tong_thu - tong_chi
        }
    
    @api.model
    def get_bao_cao_cong_no(self):
        """Báo cáo Công nợ phải thu/phải trả"""
        
        # Công nợ phải thu (TK 131)
        tk_131 = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '131')], limit=1)
        phieu_thu = 0
        phieu_chi = 0
        
        if tk_131:
            chi_tiets_131 = self.env['chi_tiet_but_toan'].search([
                ('but_toan_id.trang_thai', '=', 'da_ghi_so'),
                '|',
                ('tk_no_id', '=', tk_131.id),
                ('tk_co_id', '=', tk_131.id)
            ])
            
            for ct in chi_tiets_131:
                if ct.tk_no_id.id == tk_131.id:
                    phieu_thu += ct.so_tien_no
                else:
                    phieu_chi += ct.so_tien_co
        
        # Công nợ phải trả (TK 331)
        tk_331 = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '331')], limit=1)
        phai_tra = 0
        da_tra = 0
        
        if tk_331:
            chi_tiets_331 = self.env['chi_tiet_but_toan'].search([
                ('but_toan_id.trang_thai', '=', 'da_ghi_so'),
                '|',
                ('tk_no_id', '=', tk_331.id),
                ('tk_co_id', '=', tk_331.id)
            ])
            
            for ct in chi_tiets_331:
                if ct.tk_co_id.id == tk_331.id:
                    phai_tra += ct.so_tien_co
                else:
                    da_tra += ct.so_tien_no
        
        return {
            'cong_no_phai_thu': phieu_thu - phieu_chi,
            'cong_no_phai_tra': phai_tra - da_tra,
        }
