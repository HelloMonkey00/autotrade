export class TradeManager {
    constructor() {
        this.symbolInput = document.getElementById('symbol-input');
        this.buyButton = document.getElementById('buy-btn');
        this.sellButton = document.getElementById('sell-btn');
        this.queryButton = document.getElementById('query-btn');
        this.cancelButton = document.getElementById('cancel-btn');
    }

    init() {
        this.buyButton.addEventListener('click', () => this.buyStock());
        this.sellButton.addEventListener('click', () => this.sellStock());
        this.queryButton.addEventListener('click', () => this.queryOrder());
        this.cancelButton.addEventListener('click', () => this.cancelOrder());
    }

    buyStock() {
        const symbol = this.symbolInput.value;
        fetch('/api/trade/buy', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbol })
        });
    }

    sellStock() {
        const symbol = this.symbolInput.value;
        fetch('/api/trade/sell', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbol })
        });
    }

    queryOrder() {
        fetch('/api/trade/query')
            .then(response => response.json())
            .then(data => {
                alert(JSON.stringify(data));
            });
    }

    cancelOrder() {
        fetch('/api/trade/cancel', {
            method: 'POST'
        });
    }
}