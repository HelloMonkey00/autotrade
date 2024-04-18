export class ChartManager {
    constructor() {
        this.chart = null;
    }

    init() {
        const ctx = document.getElementById('chart-container').getContext('2d');
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Price',
                    data: [],
                    borderColor: 'blue',
                    fill: false
                }]
            }
        });

        this.socket = io('/chart');
        this.socket.on('update', (data) => {
            this.updateChart(data);
        });
    }

    updateChart(data) {
        this.chart.data.labels = data.map(item => item.timestamp);
        this.chart.data.datasets[0].data = data.map(item => item.price);
        this.chart.update();
    }
}