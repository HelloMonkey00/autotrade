export class AuthManager {
    constructor() {
        this.loginButton = document.getElementById('login-btn');
        this.envSwitch = document.getElementById('env-switch');
        this.loginStatus = document.getElementById('login-status');
    }

    init() {
        this.loginButton.addEventListener('click', () => this.login());
        this.envSwitch.addEventListener('change', () => this.toggleEnv());
    }

    login() {
        // 发送登录请求
        fetch('/api/auth/login', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.updateLoginStatus();
            }
        });
    }

    verify() {
        // 发送验证请求
        fetch('/api/auth/verify', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Verification successful');
            } else {
                alert('Verification failed');
            }
        });
    }

    toggleEnv() {
        // 切换环境
        const env = this.envSwitch.checked ? 'prod' : 'sim';
        fetch(`/api/auth/env?env=${env}`, {
            method: 'PUT',
        })
        .then(() => {
            this.updateLoginStatus();
        });
    }

    updateLoginStatus() {
        fetch('/api/auth/status')
        .then(response => response.json())
        .then(data => {
            this.loginStatus.textContent = data.status;
        });
    }
}