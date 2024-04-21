export class PriceManager {
    constructor() {
    }

    init() {
        const socket = io('/price');
        socket.on('update', (data) => {
            this.updateLatestPrice(data);
        });
    }

    updateLatestPrice(data) {
        document.getElementById('latest-price').textContent = data.price;
    }
}