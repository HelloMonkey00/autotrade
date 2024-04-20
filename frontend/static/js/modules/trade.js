export class TradeManager {
    constructor() {
        this.symbolInput = document.getElementById('symbol-input');
        this.quantityInput = document.getElementById('quantity-input');
        this.buyButton = document.getElementById('buy-btn');
        this.closePositionButton = document.getElementById('close-position-btn');
        this.strategy1Button = document.getElementById('strategy1-btn');
        this.strategy2Button = document.getElementById('strategy2-btn');
    }

    init() {
        this.buyButton.addEventListener('click', () => this.buyStock());
        this.closePositionButton.addEventListener('click', () => this.closePosition());
        this.strategy1Button.addEventListener('click', () => this.doStrategy(1));
        this.strategy2Button.addEventListener('click', () => this.doStrategy(2));
        this.symbolInput.addEventListener('input', this.doQuote);
    }

    buyStock() {
        const symbol = this.symbolInput.value;
        const quantity = parseInt(this.quantityInput.value);
        if (!symbol || !quantity) {
            return;
        }
        fetch('/api/trade/buy', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbol, quantity })
        });
    }

    closePosition() {
        const symbol = this.symbolInput.value;
        fetch('/api/trade/close', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbol })
        });
    }

    doStrategy(x) {
        fetch('/api/trade/strategy', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ x })
        });
    }

    doQuote() {
        const symbol = this.symbolInput.value;
        if (symbol) {
            // 发送查询请求
            fetch(`/api/market/quote`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ symbol })
            })
        }
    }
}