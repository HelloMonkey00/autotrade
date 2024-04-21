from event.event import LogEvent
from event.eventbus import event_bus
from backend import socketio

@socketio.on('connect', namespace='/messages')
def handle_connect():
    socketio.emit('log', {'message':'Connected'}, namespace='/messages')
    print("Connected")
    
    
def on_log(event: LogEvent):
    # 发送日志事件
    socketio.emit('log', event.to_dict(), namespace='/messages')

event_bus.subscribe(LogEvent, on_log)