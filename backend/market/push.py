from event.event import LogEvent, QuoteEvent, OptionsQuoteEvent
from event.eventbus import event_bus
from backend import socketio

def on_quote(event: QuoteEvent):
    # 发送日志事件
    socketio.emit('log', event.to_dict(), namespace='/messages')

def on_query_order(event: QuoteEvent):
    # 发送日志事件
    socketio.emit('log', event.to_dict(), namespace='/messages')
    
def on_log(event: LogEvent):
    # 发送日志事件
    socketio.emit('log', event.to_dict(), namespace='/messages')

def on_options_quote(event: OptionsQuoteEvent):
    # 发送日志事件
    socketio.emit('quote', event.to_dict(), namespace='/semi-trade')

event_bus.subscribe(LogEvent, on_log)
event_bus.subscribe(OptionsQuoteEvent, on_options_quote)