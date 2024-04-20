from event.event import *
from event.eventbus import event_bus

def on_trade(event):
    update_position(event.order_id)

def update_position(order_id):
    # 根据订单更新持仓,这里省略具体实现
    print(f"Position updated for order: {order_id}")

event_bus.subscribe(TradeEvent, on_trade)