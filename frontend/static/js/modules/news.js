export class NewsManager {
    constructor() {
        this.newsContainer = document.getElementById('news-container');
        this.logMessages = document.getElementById('log-messages');
        this.messages = [];
    }

    init() {
        const socket = io('/messages');
        socket.on('news', (data) => {
            this.updateNews(data);
        });
        socket.on('log', (data) => {
            this.updateLog(data);
        });
    }

    updateNews(data) {
        this.newsContainer.innerHTML = '';
        data.forEach(item => {
            const newsItem = document.createElement('p');
            newsItem.textContent = item.title;
            this.newsContainer.appendChild(newsItem);
        });
    }

    updateLog(data) {
        // 将新的消息添加到 messages 数组的开始
        this.messages.unshift(data['message']);

        // 创建一个新的 li 元素并添加到 log-messages 元素的开始
        var newLi = document.createElement('li');
        newLi.innerHTML = data['message'];

        // 根据日志级别设置不同的样式
        switch (data['level']) {
            case 'INFO':
                newLi.style.color = 'green';
                break;
            case 'DEBUG':
                newLi.style.color = 'gray';
                break;
            case 'ERROR':
                newLi.style.color = 'red';
                break;
        }

        this.logMessages.insertBefore(newLi, this.logMessages.firstChild);

        // 如果 messages 数组的长度超过 1000，就删除最旧的消息
        if (this.messages.length > 1000) {
            this.messages.pop();

            // 从 log-messages 元素中删除最后一个 li 元素
            this.logMessages.removeChild(this.logMessages.lastChild);
        }
    }
}