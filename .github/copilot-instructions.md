# Odoo Asset Management System - Developer Guide

## Project Overview
Vietnamese Odoo 15 ERP system for **Quản lý tài sản** (Asset Management). Features include asset tracking, depreciation calculation, inventory audits, transfers, borrowing/returning, and disposal management.

## Architecture

### Custom Modules Structure
Located in `addons/` with 3 primary custom modules:
- **`nhan_su`** (HR): Employee (`nhan_vien`), department (`phong_ban`), and position (`chuc_vu`) management
- **`quan_ly_van_ban`** (Document Mgmt): Incoming/outgoing document workflows integrated with assets
- **`quan_ly_tai_san`** (Asset Mgmt): Main module depending on both above

### Key Models
**Asset Management** (`addons/quan_ly_tai_san/models/`):
- `tai_san.py`: Core assets with depreciation logic (straight-line/degressive methods)
- `danh_muc_tai_san.py`: Asset categories
- `phan_bo_tai_san.py`: Department allocations
- `don_muon_tai_san.py`/`muon_tra_tai_san.py`: Borrowing requests and tracking
- `kiem_ke_tai_san.py`: Inventory audits with line items
- `luan_chuyen_tai_san.py`: Inter-department transfers
- `thanh_ly_tai_san.py`: Asset disposal records
- `dashboard.py`: Dashboard aggregation via RPC

## Development Workflows

### Running the System
```bash
# Activate virtual environment (Python 3.10)
source venv/bin/activate

# Start PostgreSQL container (port 5434)
sudo docker-compose up -d

# Development mode with auto-reload
./run.sh   # Uses odoo-bin.py with --dev=all

# Standard run (specify modules to upgrade)
python3 odoo-bin.py -c odoo.conf -u nhan_su,quan_ly_van_ban,quan_ly_tai_san

# Stop after init (for testing/CI)
python3 odoo-bin.py -c odoo.conf -u <module_name> --stop-after-init
```

### Module Testing
Use `test_modules.sh` to validate modules independently or together:
```bash
./test_modules.sh  # Tests all 3 custom modules with 30s timeout each
```

### Configuration
- **Main config**: `odoo.conf` (copy from `odoo.conf.template`)
- **Database**: `localhost:5434` (user: `odoo`, pass: `odoo`, db: `odoo`)
- **Webapp**: `http://localhost:8069`
- **Addons path**: Must point to project's `addons/` directory

## Odoo Patterns & Conventions

### Model Definitions
```python
class TaiSan(models.Model):
    _name = 'tai_san'  # Database table prefix
    _rec_name = 'cus_rec_name'  # Display name field
    _order = 'ngay_mua_ts desc'  # Default ordering
    _sql_constraints = [
        ("ma_tai_san_unique", "unique(ma_tai_san)", "Mã tài sản đã tồn tại !")
    ]
```

### Auto-Sequences
Defined in `data/sequences.xml` using year-based prefixes:
- Assets: `TS/2025/0001` (`tai_san.sequence`)
- Borrowing: `DMTS/2025/0001` (`don_muon_tai_san.sequence`)
- Transfers: `LCTS/2025/0001` (`luan_chuyen_tai_san.sequence`)
- Audits: `KKTS/2025/0001` (`kiem_ke_tai_san.sequence`)

Assigned in `@api.model` `create()` override:
```python
@api.model
def create(self, vals):
    if vals.get('ma_tai_san', '/') == '/':
        vals['ma_tai_san'] = self.env['ir.sequence'].next_by_code('tai_san.sequence')
    return super(TaiSan, self).create(vals)
```

### Computed Fields & Dependencies
```python
@api.depends('thanh_ly_ids', 'phong_ban_su_dung_ids')
def _compute_trang_thai_thanh_ly(self):
    for record in self:
        if record.thanh_ly_ids:
            record.trang_thai_thanh_ly = 'da_thanh_ly'
        elif record.phong_ban_su_dung_ids:
            record.trang_thai_thanh_ly = 'da_phan_bo'
```

### Security Access Control
All models grant full CRUD to `base.group_user` in `security/ir.model.access.csv`:
```csv
access_tai_san_all,tai_san.all,model_tai_san,base.group_user,1,1,1,1
```

### Frontend Integration
**Dashboard Controllers** (`models/dashboard.py`):
```python
class AssetDashboard(models.Model):
    _name = 'asset.dashboard'
    
    @api.model
    def get_overview_data(self):
        # Returns JSON for Chart.js visualization
        return {
            'total_assets': len(self.env['tai_san'].search([])),
            'departments_data': [...],  # Pie chart
            'asset_types_data': [...]   # Bar chart
        }
```

**JS Widgets** (`static/src/js/dashboard_overview.js`):
```javascript
odoo.define('quan_ly_tai_san.dashboard_overview', function (require) {
    var FormController = require('web.FormController');
    // RPC call to Python model
    this._rpc({
        model: 'asset.dashboard',
        method: 'get_overview_data',
        args: [],
    }).then(function (data) { /* Render Chart.js */ });
});
```

### View XML Structure
Menu hierarchy in `views/menu.xml`:
```xml
<menuitem id="menu_root" name="Quản lý tài sản" sequence="0" />
<menuitem id="menu_asset_dashboard" parent="menu_root" sequence="1"/>
<menuitem id="menu_dashboard_overview" action="dashboard_tong_quan_action" parent="menu_asset_dashboard"/>
```

## Dependencies & Module Chain
Critical dependency order (affects installation/upgrades):
1. `nhan_su` (base HR module)
2. `quan_ly_van_ban` (depends on `nhan_su`)
3. `quan_ly_tai_san` (depends on `nhan_su`, `quan_ly_van_ban`, `bus`)

Always upgrade in dependency order: `-u nhan_su,quan_ly_van_ban,quan_ly_tai_san`

## Vietnamese Naming Conventions
- **Models/Tables**: Snake_case Vietnamese (`tai_san`, `don_muon_tai_san`)
- **UI Labels**: Full Vietnamese phrases (`'Tên tài sản'`, `'Phương pháp khấu hao'`)
- **Selection Values**: English keys, Vietnamese labels:
  ```python
  pp_khau_hao = fields.Selection([
      ('straight-line', 'Tuyến tính'),
      ('degressive', 'Giảm dần'),
      ('none', 'Không')
  ])
  ```

## Common Pitfalls
- **Missing sequence initialization**: Assets created without `ma_tai_san` will fail uniqueness constraint
- **Circular dependencies**: Avoid bidirectional Many2one references between custom modules
- **Database state**: Use `--stop-after-init` for clean test runs; database persists in Docker volume
- **Port conflicts**: PostgreSQL on non-standard 5434 (check `odoo.conf` vs `docker-compose.yml`)
- **Python version**: Requires Python 3.10 for compatibility with dependencies (`requirements.txt` specifies version-specific packages)
