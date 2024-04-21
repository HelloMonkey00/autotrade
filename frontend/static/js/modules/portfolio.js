export class PortfolioManager {
    constructor() {
        
    }

    init() {
        const socket = io('/portfolio');
        socket.on('update', (data) => {
            this.updatePortfolio(data);
        });
    }

    updatePortfolio(data) {
        const tbody = document.querySelector('#portfolio-table tbody');
        tbody.innerHTML = '';
        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.symbol}</td>
                <td>${item.quantity}</td>
                <td>${item.price}</td>
                <td>${item.value}</td>
            `;
            tbody.appendChild(row);
        });
    }
}