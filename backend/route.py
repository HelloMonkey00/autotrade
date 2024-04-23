from flask import Blueprint, jsonify, request
from .config import ConfigManager
from event.event import *
from event.eventbus import event_bus
from backend.support.utils import convert_to_OrderType, convert_to_OrderSide, convert_to_TrailType_and_TrailValue
from .config import ConfigManager
from .market.marketdata import *
from .trade.gateway import *


route_bp = Blueprint('route', __name__)

@route_bp.route('/trade/order', methods=['POST'])
def place_order():
    order_data = request.get_json()
    trail_type, trail_value = convert_to_TrailType_and_TrailValue(order_data)
    event = PlaceOrderEvent(datetime.now(), 
                            ticker=order_data['symbol'], 
                            order_quantity=order_data['quantity'], 
                            order_price=order_data['price'], 
                            order_type=convert_to_OrderType[order_data['order_type']], 
                            order_side=convert_to_OrderSide[order_data['order_side']], 
                            order_id=order_data['id'],
                            trail_type=trail_type,
                            trail_value=trail_value)
    event_bus.publish(event)
    return jsonify({"message": "Order placed"})

@route_bp.route('/environment', methods=['GET'])
def get_environment():
    event_bus.publish(GetAccountEvent(datetime.now()))
    return jsonify({"environment": "SIMULATION" if ConfigManager.get_instance().is_simulate() else "REAL"});

@route_bp.route('/trade/close', methods=['POST'])
def close_position_route():
    close_position_data = request.get_json()
    event = ClosePositionEvent(close_position_data)
    event_bus.publish(event)
    return jsonify({"message": "Close position submitted"})

@route_bp.route('/market/quote')
def get_quote_route():
    quote_data = request.get_json()
    event = QuoteEvent(quote_data)
    event_bus.publish(event)
    return jsonify({"message": "Quote request submitted"})

@route_bp.route('/market/history/<symbol>')
def get_historical_data_route(symbol):
    event = HistoricalDataEvent(symbol)
    event_bus.publish(event)
    return jsonify({"message": "Historical data request submitted"})

@route_bp.route('/market/news')
def get_news_route():
    event = NewsEvent()
    event_bus.publish(event)
    return jsonify({"message": "News request submitted"})

@route_bp.route('/auth/login', methods=['POST'])
def login_route():
    event = LoginEvent()
    event_bus.publish(event)
    return jsonify({"message": "Login request submitted"})

@route_bp.route('/auth/verify', methods=['POST'])
def verify_route():
    event = VerifyEvent()
    event_bus.publish(event)
    return jsonify({"message": "Verify request submitted"})

@route_bp.route('/auth/env', methods=['PUT'])
def set_env_route():
    env = request.args.get('env')
    event = SetEnvEvent(env)
    event_bus.publish(event)
    return jsonify({"message": "Set env request submitted"})

@route_bp.route('/auth/status')
def get_status_route():
    event = GetStatusEvent()
    event_bus.publish(event)
    return jsonify({"message": "Get status request submitted"})

if __name__ == '__main__':
    pass