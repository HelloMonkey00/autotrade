from event.event import TradeOrderEvent, QueryOrderEvent, CancelOrderEvent
from event.eventbus import event_bus

def on_trade_order(event: TradeOrderEvent):
    print("Trade order received")

def on_query_order(event: QueryOrderEvent):
    print("Query order received") 

def on_cancel_order(event: CancelOrderEvent):
    print("Cancel order received")

event_bus.subscribe(TradeOrderEvent, on_trade_order)
event_bus.subscribe(QueryOrderEvent, on_query_order)
event_bus.subscribe(CancelOrderEvent, on_cancel_order)