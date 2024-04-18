export class PriceManager {
    constructor() {
        this.socket = null;
    }

    init() {
        this.socket = io('/price');
        this.socket.on('update', (data) => {
            this.updateLatestPrice(data);
        });
    }

    updateLatestPrice(data) {
        document.getElementById('latest-price').textContent = data.price;
    }
}