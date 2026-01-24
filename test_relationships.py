#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import psycopg2
import sys

try:
    # Kết nối database
    conn = psycopg2.connect(
        host="localhost",
        port="5434",
        database="odoo",
        user="odoo",
        password="odoo"
    )
    cur = conn.cursor()
    
    print("=" * 80)
    print("TEST 1: Kiểm tra fields trong nhan_vien (liên kết văn bản + tài sản)")
    print("=" * 80)
    cur.execute("""
        SELECT name, field_description, ttype, relation 
        FROM ir_model_fields 
        WHERE model='nhan_vien' 
            AND (name LIKE '%van_ban%' OR name LIKE '%tai_san%') 
        ORDER BY name
    """)
    results = cur.fetchall()
    if results:
        for row in results:
            print(f"✓ {row[0]:40} | {row[1]:40} | {row[2]:15} | {row[3]}")
    else:
        print("❌ KHÔNG TÌM THẤY FIELDS!")
    
    print("\n" + "=" * 80)
    print("TEST 2: Kiểm tra fields văn bản trong models tài sản")
    print("=" * 80)
    cur.execute("""
        SELECT model, name, field_description, ttype, relation 
        FROM ir_model_fields 
        WHERE model IN ('thanh_ly_tai_san', 'luan_chuyen_tai_san', 'tai_san') 
            AND name LIKE '%van_ban%' 
        ORDER BY model, name
    """)
    results = cur.fetchall()
    if results:
        for row in results:
            print(f"✓ {row[0]:25} | {row[1]:30} | {row[3]:15} | {row[4]}")
    else:
        print("❌ KHÔNG TÌM THẤY FIELDS!")
    
    print("\n" + "=" * 80)
    print("TEST 3: Kiểm tra module dependencies")
    print("=" * 80)
    cur.execute("""
        SELECT m1.name as module, d.name as depends_on
        FROM ir_module_module m1
        JOIN ir_module_module_dependency d ON d.module_id = m1.id
        WHERE m1.name IN ('nhan_su', 'quan_ly_van_ban', 'quan_ly_tai_san')
        ORDER BY m1.name, d.name
    """)
    results = cur.fetchall()
    print("Module dependencies:")
    current_module = None
    for row in results:
        if row[0] != current_module:
            current_module = row[0]
            print(f"\n{current_module}:")
        print(f"  → {row[1]}")
    
    print("\n" + "=" * 80)
    print("TEST 4: Kiểm tra view extensions")
    print("=" * 80)
    cur.execute("""
        SELECT v.name, v.model, pv.name as parent_view
        FROM ir_ui_view v
        LEFT JOIN ir_ui_view pv ON v.inherit_id = pv.id
        WHERE v.name LIKE '%extend%'
        ORDER BY v.model, v.name
    """)
    results = cur.fetchall()
    if results:
        for row in results:
            print(f"✓ {row[0]:50} | {row[1]:20} | extends: {row[2]}")
    else:
        print("❌ KHÔNG TÌM THẤY VIEW EXTENSIONS!")
    
    print("\n" + "=" * 80)
    print("TEST 5: Kiểm tra sequences (auto-numbering)")
    print("=" * 80)
    cur.execute("""
        SELECT name, code, prefix, padding
        FROM ir_sequence
        WHERE code LIKE '%tai_san%' OR code LIKE '%van_ban%'
        ORDER BY code
    """)
    results = cur.fetchall()
    if results:
        for row in results:
            print(f"✓ {row[1]:40} | Prefix: {row[2]:20} | Padding: {row[3]}")
    else:
        print("⚠ Không tìm thấy sequences")
    
    print("\n" + "=" * 80)
    print("TEST 6: Kiểm tra circular dependency (module load order)")
    print("=" * 80)
    cur.execute("""
        SELECT name, state, latest_version
        FROM ir_module_module
        WHERE name IN ('nhan_su', 'quan_ly_van_ban', 'quan_ly_tai_san')
        ORDER BY name
    """)
    results = cur.fetchall()
    for row in results:
        status = "✓" if row[1] == "installed" else "❌"
        print(f"{status} {row[0]:25} | Status: {row[1]:15} | Version: {row[2]}")
    
    print("\n" + "=" * 80)
    print("SUMMARY: Tổng kết kiểm tra")
    print("=" * 80)
    
    # Count checks
    cur.execute("SELECT COUNT(*) FROM ir_model_fields WHERE model='nhan_vien' AND (name LIKE '%van_ban%' OR name LIKE '%tai_san%')")
    nhan_vien_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM ir_model_fields WHERE model IN ('thanh_ly_tai_san', 'luan_chuyen_tai_san', 'tai_san') AND name LIKE '%van_ban%'")
    tai_san_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM ir_ui_view WHERE name LIKE '%extend%'")
    view_count = cur.fetchone()[0]
    
    print(f"Nhan_vien fields (van_ban + tai_san): {nhan_vien_count}")
    print(f"Tai_san models with van_ban fields: {tai_san_count}")
    print(f"View extensions: {view_count}")
    
    if nhan_vien_count >= 7 and tai_san_count >= 3 and view_count >= 2:
        print("\n✅ TẤT CẢ CÁC LIÊN KẾT HOẠT ĐỘNG BÌNH THƯỜNG!")
    else:
        print("\n⚠ CÓ VẺ CÓ VẤN ĐỀ VỚI MỘT SỐ LIÊN KẾT!")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"❌ LỖI: {e}")
    sys.exit(1)
