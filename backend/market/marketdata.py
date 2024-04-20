import random
from flask_socketio import emit
from flask import Blueprint, jsonify
from event.event import *
from event.eventbus import event_bus

market_bp = Blueprint('market', __name__, url_prefix='/market')

def update_latest_price(price_data):
    emit('update', price_data, namespace='/price')

def update_chart_data(chart_data):
    emit('update', chart_data, namespace='/chart')

def update_news(news_data):
    emit('update', news_data, namespace='/news')

def update_portfolio(portfolio_data):
    emit('update', portfolio_data, namespace='/portfolio')

def on_quote(event: QuoteEvent):
    pass

def on_historical_data(event: HistoricalDataEvent):
    pass

def on_news(event: NewsEvent):
    pass

def on_log(event: LogEvent):
    print(event)

event_bus.subscribe(QuoteEvent, on_quote)
event_bus.subscribe(HistoricalDataEvent, on_historical_data)
event_bus.subscribe(NewsEvent, on_news)
event_bus.subscribe(LogEvent, on_log)