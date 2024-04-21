# from event.event import *
# from event.eventbus import event_bus
# from backend.support.utils import format_log
# from app import socketio

    
# def update_latest_price(price_data):
#     socketio.emit('update', price_data, namespace='/price')

# def update_chart_data(chart_data):
#     socketio.emit('update', chart_data, namespace='/chart')

# def update_news(news_data):
#     socketio.emit('update', news_data, namespace='/news')

# def update_portfolio(portfolio_data):
#     socketio.emit('update', portfolio_data, namespace='/portfolio')

# def on_quote(event: QuoteEvent):
#     pass

# def on_historical_data(event: HistoricalDataEvent):
#     pass

# def on_news(event: NewsEvent):
#     pass

# def on_log(event: LogEvent):
#     # 发送日志事件
#     socketio.emit('log', {'message':'log'}, namespace='/messages')
#     print(format_log(event))

# event_bus.subscribe(QuoteEvent, on_quote)
# event_bus.subscribe(LogEvent, on_log)