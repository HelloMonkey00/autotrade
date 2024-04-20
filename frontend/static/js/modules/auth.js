export class AuthManager {
    constructor() {
    }

    init() {
        this.checkEnvironment();
    }

    checkEnvironment() {
        fetch('/api/environment')
            .then(response => response.json())
            .then(data => {
                const envElement = document.getElementById('login-env');
                envElement.textContent = data.environment;
            });
    }

}