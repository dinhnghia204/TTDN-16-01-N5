#!/bin/bash

echo "==== Testing Odoo Modules ===="
cd /home/ducanh/TTDN-16-01-N5

echo ""
echo "1. Testing nhan_su module upgrade..."
timeout 30 python3 odoo-bin -c odoo.conf -d odoo -u nhan_su --stop-after-init 2>&1 | tail -20
if [ $? -eq 0 ]; then
    echo "✓ nhan_su: OK"
else
    echo "✗ nhan_su: ERROR"
fi

echo ""
echo "2. Testing quan_ly_van_ban module upgrade..."
timeout 30 python3 odoo-bin -c odoo.conf -d odoo -u quan_ly_van_ban --stop-after-init 2>&1 | tail -20
if [ $? -eq 0 ]; then
    echo "✓ quan_ly_van_ban: OK"
else
    echo "✗ quan_ly_van_ban: ERROR"
fi

echo ""
echo "3. Testing quan_ly_tai_san module upgrade..."
timeout 30 python3 odoo-bin -c odoo.conf -d odoo -u quan_ly_tai_san --stop-after-init 2>&1 | tail -20
if [ $? -eq 0 ]; then
    echo "✓ quan_ly_tai_san: OK"
else
    echo "✗ quan_ly_tai_san: ERROR"
fi

echo ""
echo "4. Testing all modules together..."
timeout 30 python3 odoo-bin -c odoo.conf -d odoo -u nhan_su,quan_ly_van_ban,quan_ly_tai_san --stop-after-init 2>&1 | tail -20
if [ $? -eq 0 ]; then
    echo "✓ All modules: OK"
else
    echo "✗ All modules: ERROR"
fi

echo ""
echo "==== Test Complete ===="
