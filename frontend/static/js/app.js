import { PortfolioManager } from './modules/portfolio.js';
import { SemiTradeManager } from './modules/semi-trade.js';
import { PriceManager } from './modules/price.js';
import { NewsManager } from './modules/news.js';
import { TradeManager } from './modules/trade.js';
import { AuthManager } from './modules/auth.js';

const portfolioManager = new PortfolioManager();
const semiTradeManager = new SemiTradeManager();
const priceManager = new PriceManager();
const newsManager = new NewsManager();
const tradeManager = new TradeManager();
const authManager = new AuthManager();

// 初始化页面
function init() {
    portfolioManager.init();
    semiTradeManager.init();
    priceManager.init();
    newsManager.init();
    tradeManager.init();
    authManager.init();
}

init();