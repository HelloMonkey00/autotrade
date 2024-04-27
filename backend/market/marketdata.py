from backend.support.context import Context
from event.event import LogEvent, QuoteEvent, LogLevel
from event.eventbus import event_bus
from backend import socketio
from moomoo import *
import time
from backend.config import ConfigManager

@socketio.on('connect', namespace='/messages')
def handle_connect():
    socketio.emit('log', {'message':'Connected'}, namespace='/messages')
    
def on_quote(event: QuoteEvent):
    # 发送日志事件
    socketio.emit('log', event.to_dict(), namespace='/messages')

def on_query_order(event: QuoteEvent):
    # 发送日志事件
    socketio.emit('log', event.to_dict(), namespace='/messages')
    
def on_log(event: LogEvent):
    # 发送日志事件
    socketio.emit('log', event.to_dict(), namespace='/messages')

@socketio.on('connect', namespace='/spx')
def on_spx_init(event):
    quote_ctx = Context.get_instance().open_quote()
    option_code = ConfigManager.get_instance().get('option_code', None, 'MOOMOO')
    ret, data = quote_ctx.get_option_expiration_date(code=option_code)

    if ret == RET_OK:
        expiration_date_list = data['strike_time'].values.tolist()
        date = expiration_date_list[0] # 取第一个到期日
        ret2, data2 = quote_ctx.get_option_chain(code=option_code, start=date, end=date)
        if ret2 == RET_OK:
            socketio.emit('spx_current_code', {"code":data2['code'][0]}, namespace='/spx')
        else:
            event_bus.publish(LogEvent('error: ' + str(data2), LogLevel.ERROR))
    else:
        event_bus.publish(LogEvent('error: ' + str(data), LogLevel.ERROR))

event_bus.subscribe(LogEvent, on_log)