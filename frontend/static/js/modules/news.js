export class NewsManager {
    constructor() {
        this.newsContainer = document.getElementById('news-container');
    }

    init() {
        this.socket = io('/news');
        this.socket.on('update', (data) => {
            this.updateNews(data);
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
}