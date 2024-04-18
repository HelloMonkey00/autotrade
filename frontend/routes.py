from flask import render_template
from app import app, socketio
from app.producers import CBOEDataProducer, YahooFinanceDataProducer
from app.subscribers import SocketIOSubscriber, LoggingSubscriber
import schedule
import time
from threading import Thread

@app.route('/')
def index():
    print("Index")
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("Connected")
    yahoo_producer.fetch_data()
    cboe_producer.fetch_data()
    schedule.every(10).seconds.do(cboe_producer.fetch_data)
    schedule.every(10).seconds.do(yahoo_producer.fetch_data)
    Thread(target=run_schedule).start()

@socketio.on('disconnect')
def handle_disconnect():
    print("Disconnected")
    schedule.clear()