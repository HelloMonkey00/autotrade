from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from backend.trade.gateway import trade_bp
from backend.market.marketdata import market_bp
from backend.route import route_bp

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.register_blueprint(trade_bp, url_prefix='/api/trade')
app.register_blueprint(market_bp, url_prefix='/api/market')
app.register_blueprint(route_bp, url_prefix='/api')

socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)