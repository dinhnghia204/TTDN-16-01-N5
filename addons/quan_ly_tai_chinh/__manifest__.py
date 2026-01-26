# -*- coding: utf-8 -*-
{
    'name': "Quản lý Tài chính/Kế toán",

    'summary': """
        Hệ thống kế toán tích hợp với Nhân sự & Tài sản""",

    'description': """
        Module tài chính kế toán bao gồm:
        - Hệ thống tài khoản kế toán (VAS)
        - Sổ cái và định khoản tự động
        - Quản lý lương nhân viên
        - Kế toán tài sản cố định
        - Báo cáo tài chính
    """,

    'author': "Nguyễn Ngọc Đan Trường - 1504",
    'website': "http://www.yourcompany.com",

    'category': 'Accounting/Accounting',
    'version': '1.0',
    'license': 'LGPL-3',
    'application': True,
    'installable': True,

    # Dependencies
    'depends': [
        'base',
        'web',
        'bus',
        'nhan_su',
        'quan_ly_van_ban',
        'quan_ly_tai_san'
    ],

    # Data files
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'data/tai_khoan_ke_toan_data.xml',
        'data/cron_khau_hao_hang_thang.xml',
        
        'views/tai_khoan_ke_toan.xml',
        'views/so_cai_ke_toan.xml',
        'views/phieu_luong.xml',
        'views/phieu_thu.xml',
        'views/phieu_chi.xml',
        'views/hoa_don_ban.xml',
        'views/hoa_don_mua.xml',
        'views/tai_san_extend.xml',
        'views/thanh_ly_tai_san_extend.xml',
        'views/bao_cao_tai_chinh.xml',
        'views/dashboard_tai_chinh.xml',
        'views/menu.xml',
    ],
    
    'assets': {
        'web.assets_backend': [
            'quan_ly_tai_chinh/static/src/js/dashboard_tai_chinh.js',
            'quan_ly_tai_chinh/static/src/css/dashboard_tai_chinh.css',
        ],
    },
    
    'demo': [
        'demo/demo.xml',
    ],
}
