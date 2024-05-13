from flask import Blueprint, jsonify, request
from .config import ConfigManager
from event.event import *
from event.eventbus import event_bus
from backend.support.utils import convert_to_OrderType, convert_to_OrderSide, convert_to_TrailType_and_TrailValue
from .config import ConfigManager
from .market.push import *
from .market.market import *
from .trade.gateway import *
from .trade.algo import *
from backend import socketio
import uuid


route_bp = Blueprint('route', __name__)

@route_bp.route('/trade/order', methods=['POST'])
def place_order():
    order_data = request.get_json()
    isTrailOrder, trail_type, trail_value = convert_to_TrailType_and_TrailValue(order_data)
    if isTrailOrder:
        event = TrailOrderEvent(datetime.now(),
                                ticker=order_data['symbol'],
                                order_quantity=order_data['quantity'],
                                order_type=convert_to_OrderType[order_data['order_type']],
                                order_side=convert_to_OrderSide[order_data['order_side']],
                                order_id=order_data['id'],
                                trail_type=trail_type,
                                trail_value=trail_value)
    else:
        event = OrderEvent(datetime.now(), 
                                ticker=order_data['symbol'], 
                                order_quantity=order_data['quantity'], 
                                order_price=order_data['price'], 
                                order_type=convert_to_OrderType[order_data['order_type']], 
                                order_side=convert_to_OrderSide[order_data['order_side']], 
                                order_id=order_data['id'])
    event_bus.publish(event)
    return jsonify({"message": "Order placed"})

@route_bp.route('/environment', methods=['GET'])
def get_environment():
    
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

@socketio.on('connect', namespace='/messages')
def handle_connect():
    event_bus.publish(LogEvent('Connected', LogLevel.INFO))
    event_bus.publish(GetAccountEvent(datetime.now()))
    pass

@route_bp.route('/semi-trade/command', methods=['POST'])
def semi_trade_command_route():
    try:
        command_data = request.get_json()
        event = SemiTradeCommandEvent.from_request(command_data)
        event.order_id = str(uuid.uuid4())
        event_bus.publish(event)
        return jsonify({"message": "Semi-trade command submitted"})
    except Exception as e:
        event_bus.publish(LogEvent('Error: ' + str(e), LogLevel.ERROR))
        return jsonify({"message": "Error: " + str(e)})