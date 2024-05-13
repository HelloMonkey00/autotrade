export class SemiTradeManager {
    constructor() {
        this.jsonData = document.getElementById('json-data');
        this.levelSelectCall = document.getElementById('level-select-call');
        this.quantityInputCall = document.getElementById('quantity-input-call');
        this.levelSelectPut = document.getElementById('level-select-put');
        this.quantityInputPut = document.getElementById('quantity-input-put');
    }

    init() {
        document.getElementById('place-order').addEventListener('click', () => {
            this.sendCommand('placeOrder');
        });

        document.getElementById('close-position').addEventListener('click', () => {
            this.sendCommand('closePosition');
        });

        document.getElementById('modify-position').addEventListener('click', () => {
            this.sendCommand('modifyPosition');
        });
    }

    sendCommand(command) {
        fetch('/api/semi-trade/command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                command: command,
                call: {
                    level: this.levelSelectCall.value,
                    quantity: this.quantityInputCall.value
                },
                put: {
                    level: this.levelSelectPut.value,
                    quantity: this.quantityInputPut.value
                }
            })
        }).then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        }).then(data => {
            console.log(data);
        }).catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            throw error;
        });
    }

}