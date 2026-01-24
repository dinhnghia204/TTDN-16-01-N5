-- Test 1: Kiểm tra các trường liên kết trong nhan_vien
SELECT 
    name, 
    field_description, 
    ttype, 
    relation 
FROM ir_model_fields 
WHERE model='nhan_vien' 
    AND (name LIKE '%van_ban%' OR name LIKE '%tai_san%') 
ORDER BY name;

-- Test 2: Kiểm tra các trường văn bản trong models tài sản
SELECT 
    model,
    name, 
    field_description, 
    ttype, 
    relation 
FROM ir_model_fields 
WHERE model IN ('thanh_ly_tai_san', 'luan_chuyen_tai_san', 'tai_san') 
    AND name LIKE '%van_ban%' 
ORDER BY model, name;

-- Test 3: Kiểm tra dependencies giữa modules
SELECT 
    m1.name as module,
    d.name as depends_on
FROM ir_module_module m1
JOIN ir_module_module_dependency d ON d.module_id = m1.id
WHERE m1.name IN ('nhan_su', 'quan_ly_van_ban', 'quan_ly_tai_san')
ORDER BY m1.name, d.name;

-- Test 4: Kiểm tra view inheritance
SELECT 
    name,
    model,
    inherit_id
FROM ir_ui_view
WHERE name LIKE '%extend%' OR name LIKE '%van_ban%'
ORDER BY model, name;

-- Test 5: Kiểm tra sequences
SELECT 
    name,
    code,
    prefix,
    padding
FROM ir_sequence
WHERE code LIKE '%tai_san%' OR code LIKE '%van_ban%'
ORDER BY code;
