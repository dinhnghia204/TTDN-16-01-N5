#!/bin/bash

echo "================================================"
echo "  KIỂM TRA MODULE QUẢN LÝ TÀI CHÍNH/KẾ TOÁN"
echo "================================================"
echo ""

# Kiểm tra cấu trúc thư mục
echo "1. Kiểm tra cấu trúc module..."
if [ -d "addons/quan_ly_tai_chinh" ]; then
    echo "   ✓ Module directory exists"
else
    echo "   ✗ Module directory NOT found!"
    exit 1
fi

# Kiểm tra files chính
echo ""
echo "2. Kiểm tra files chính..."
files=(
    "addons/quan_ly_tai_chinh/__init__.py"
    "addons/quan_ly_tai_chinh/__manifest__.py"
    "addons/quan_ly_tai_chinh/models/__init__.py"
    "addons/quan_ly_tai_chinh/data/tai_khoan_ke_toan_data.xml"
    "addons/quan_ly_tai_chinh/security/ir.model.access.csv"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file NOT found!"
    fi
done

# Kiểm tra models
echo ""
echo "3. Kiểm tra models..."
models=(
    "tai_khoan_ke_toan.py"
    "so_cai_ke_toan.py"
    "chi_tiet_but_toan.py"
    "phieu_luong.py"
    "chi_tiet_luong.py"
    "tai_san_extend.py"
    "lich_su_khau_hao_extend.py"
    "thanh_ly_tai_san_extend.py"
    "bao_cao_tai_chinh.py"
)

for model in "${models[@]}"; do
    if [ -f "addons/quan_ly_tai_chinh/models/$model" ]; then
        echo "   ✓ models/$model"
    else
        echo "   ✗ models/$model NOT found!"
    fi
done

# Kiểm tra views
echo ""
echo "4. Kiểm tra views..."
views=(
    "menu.xml"
    "tai_khoan_ke_toan.xml"
    "so_cai_ke_toan.xml"
    "phieu_luong.xml"
    "tai_san_extend.xml"
    "dashboard_tai_chinh.xml"
)

for view in "${views[@]}"; do
    if [ -f "addons/quan_ly_tai_chinh/views/$view" ]; then
        echo "   ✓ views/$view"
    else
        echo "   ✗ views/$view NOT found!"
    fi
done

# Test syntax Python
echo ""
echo "5. Test syntax Python..."
python3 -m py_compile addons/quan_ly_tai_chinh/models/*.py 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✓ Python syntax OK"
else
    echo "   ✗ Python syntax errors!"
fi

# Đếm số dòng code
echo ""
echo "6. Thống kê code..."
python_lines=$(find addons/quan_ly_tai_chinh -name "*.py" -exec wc -l {} + | tail -1 | awk '{print $1}')
xml_lines=$(find addons/quan_ly_tai_chinh -name "*.xml" -exec wc -l {} + | tail -1 | awk '{print $1}')
js_lines=$(find addons/quan_ly_tai_chinh -name "*.js" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}')

echo "   Python: $python_lines dòng"
echo "   XML: $xml_lines dòng"
echo "   JavaScript: $js_lines dòng"

echo ""
echo "================================================"
echo "  KIỂM TRA HOÀN TẤT!"
echo "================================================"
echo ""
echo "Sẵn sàng chạy lệnh:"
echo "  python3 odoo-bin.py -c odoo.conf -u quan_ly_tai_chinh"
echo ""
