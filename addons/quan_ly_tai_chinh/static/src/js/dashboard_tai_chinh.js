odoo.define('quan_ly_tai_chinh.dashboard_tai_chinh', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var viewRegistry = require('web.view_registry');
    var core = require('web.core');

    var DashboardTaiChinhController = FormController.extend({
        start: function () {
            this._super.apply(this, arguments);
            this.$el.addClass('o_dashboard_view');
        },
        
        willStart: function () {
            return Promise.all([
                this._super.apply(this, arguments),
                this._loadDashboardData()
            ]);
        },
        
        _loadDashboardData: function () {
            const self = this;
            return this._rpc({
                model: 'bao_cao_tai_chinh',
                method: 'get_dashboard_data',
                args: [],
            }).then(function (data) {
                self.dashboardData = data;
            });
        },
        
        renderButtons: function () {
            this.$buttons = $();
            return this.$buttons;
        },
        
        _update: function () {
            const self = this;
            return this._loadDashboardData().then(function () {
                self._updateDashboard();
            });
        },
        
        _updateDashboard: function () {
            if (!this.dashboardData) return;
            const data = this.dashboardData;
            
            // Update counter cards
            this.$('.tong_but_toan').text(data.tong_but_toan);
            this.$('.but_toan_da_ghi_so').text(data.but_toan_da_ghi_so);
            this.$('.tong_phieu_luong').text(data.tong_phieu_luong);
            this.$('.tong_luong_thang').text(this._formatCurrency(data.tong_luong_thang));
            
            // Render charts
            this._renderLoaiChungTuChart(data.loai_chung_tu_stats);
            this._renderButToanTheoThangChart(data.but_toan_theo_thang);
        },
        
        _formatCurrency: function (amount) {
            return amount.toLocaleString('vi-VN') + ' VNĐ';
        },
        
        _renderLoaiChungTuChart: function (loaiChungTuData) {
            if (this.loaiChungTuChart) {
                this.loaiChungTuChart.destroy();
            }
            
            const ctx = this.$('#loaiChungTuChart')[0].getContext('2d');
            const labels = loaiChungTuData.map(d => d.name);
            const data = loaiChungTuData.map(d => d.count);
            
            this.loaiChungTuChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: [
                            '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e',
                            '#e74a3b', '#5a5c69'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                        }
                    }
                }
            });
        },
        
        _renderButToanTheoThangChart: function (butToanTheoThangData) {
            if (this.butToanTheoThangChart) {
                this.butToanTheoThangChart.destroy();
            }
            
            const ctx = this.$('#butToanTheoThangChart')[0].getContext('2d');
            const labels = butToanTheoThangData.map(d => d.thang);
            const data = butToanTheoThangData.map(d => d.count);
            
            this.butToanTheoThangChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Số bút toán',
                        data: data,
                        backgroundColor: '#4e73df'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });
        },
    });

    var DashboardTaiChinhView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: DashboardTaiChinhController,
        }),
    });

    viewRegistry.add('dashboard_tai_chinh', DashboardTaiChinhView);

    return DashboardTaiChinhController;
});
