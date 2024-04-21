from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
from backend.route import route_bp
import json

from event.event import *
from event.eventbus import event_bus

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.register_blueprint(route_bp, url_prefix='/api')

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/messages')
def handle_connect():
    socketio.emit('log', {'message':'Connected'}, namespace='/messages')
    print("Connected")

@socketio.on('connect', namespace='/')
def handle_disconnect():
    socketio.emit('log', {'message':'Connected'})
    print("Disconnected")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5005)

def on_log(event: LogEvent):
    # 发送日志事件
    socketio.emit('log', event.to_dict(), namespace='/messages')

event_bus.subscribe(LogEvent, on_log)