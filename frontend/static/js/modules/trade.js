export class TradeManager {
    constructor() {
        this.symbolInput = document.getElementById('symbol-input');
        this.quantityInput = document.getElementById('quantity-input');
        this.orderTypeSelect = document.getElementById('order-type-select');
        this.buyButton = document.getElementById('buy-btn');
        this.sellButton = document.getElementById('sell-btn');
        this.executeOrdersButton = document.getElementById('execute-orders-btn');
        this.ordersTableBody = document.getElementById('orders-table').querySelector('tbody');
        this.priceInput = document.getElementById('price-input');
        this.orders = [];
        this.orderTypeMap = this.getOrderTypeMap();
        this.trailAmountInput = document.getElementById('trail-amount-input');
        this.trailRatioInput = document.getElementById('trail-ratio-input');
    }

    init() {
        this.buyButton.addEventListener('click', () => this.addOrder('BUY'));
        this.sellButton.addEventListener('click', () => this.addOrder('SELL'));
        this.executeOrdersButton.addEventListener('click', () => this.executeOrders());
        this.symbolInput.addEventListener('input', this.doQuote);
    }

    addOrder(side) {
        const symbol = this.symbolInput.value;
        const quantity = parseInt(this.quantityInput.value);
        const orderType = this.orderTypeSelect.value;

        if (!symbol || !quantity || !orderType) {
            return;
        }

        const price = parseFloat(this.priceInput.value);
        if (isNaN(price) || price <= 0) {
            return;
        }

        const order = { symbol, quantity, price, order_side: side, order_type: orderType, id: Date.now() };
        this.orders.push(order);

        // Add the order to the table
        this.addOrderToTable(order);

        // If order_type is "1" or "2", add two additional orders
        if (orderType === "1" || orderType === "2") {
            let trailAmount = parseFloat(this.trailAmountInput.value);
            let trailRatio = parseFloat(this.trailRatioInput.value);

            // If trailAmount or trailRatio is not a number, set them to their default values
            if (isNaN(trailAmount)) {
                trailAmount = 1.0;
            }
            if (isNaN(trailRatio)) {
                trailRatio = 20;
            }

            const extraOrder1 = { symbol, quantity, price: price, order_side: side, order_type: "8", id: Date.now() + 1, trail_amount: trailAmount };
            const extraOrder2 = { symbol, quantity, price: price, order_side: side, order_type: "8", id: Date.now() + 2, trail_ratio: trailRatio };
            this.orders.push(extraOrder1, extraOrder2);

            // Add the extra orders to the table
            this.addOrderToTable(extraOrder1);
            this.addOrderToTable(extraOrder2);
        }
    }


    addOrderToTable(order) {
        const row = document.createElement('tr');
        row.id = `order-${order.id}`;
        let priceDisplay;
        if (order.order_type === "8") {
            if (!isNaN(order.trail_amount)) {
                priceDisplay = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(order.trail_amount);
            } else {
                priceDisplay = `${order.trail_ratio}%`;
            }
        } else {
            priceDisplay = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(order.price);
        }
        row.innerHTML = `
        <td>${order.symbol}</td>
        <td>${order.quantity}</td>
        <td>${priceDisplay}</td>
        <td>${order.order_side}</td>
        <td>${this.orderTypeMap[order.order_type]}</td>
        <td><button data-order-id="${order.id}">Remove</button></td>
    `;
        this.ordersTableBody.appendChild(row);

        // Bind the removeOrderHandler to the Remove button
        const removeButton = row.querySelector('button');
        removeButton.addEventListener('click', () => this.removeOrder(order.id));
    }

    removeOrder(orderId) {
        // Remove the order from the array
        this.orders = this.orders.filter(order => order.id !== orderId);

        // Remove the order from the table
        const row = document.getElementById(`order-${orderId}`);
        this.ordersTableBody.removeChild(row);
    }

    executeOrders() {
        this.orders.forEach(order => {
            // Call the order API for each order
            fetch('/api/trade/order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(order),
            });
        });

        // Clear the orders
        this.orders = [];

        // Clear the table rows
        const rows = this.ordersTableBody.querySelectorAll('tr');
        rows.forEach(row => this.ordersTableBody.removeChild(row));
    }

    getOrderTypeMap() {
        const options = this.orderTypeSelect.options;
        const map = {};
        for (let i = 0; i < options.length; i++) {
            const option = options[i];
            map[option.value] = option.textContent;
        }
        return map;
    }
}