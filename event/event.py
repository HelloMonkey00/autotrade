from enum import Enum
from dataclasses import dataclass
from typing import Dict

class EventType(Enum):
    TRADE = "TRADE"
    TRADE_ORDER = "TRADE_ORDER"
    QUERY_ORDER = "QUERY_ORDER"
    CANCEL_ORDER = "CANCEL_ORDER"
    QUOTE = "QUOTE"
    HISTORICAL_DATA = "HISTORICAL_DATA"
    NEWS = "NEWS"

@dataclass
class Event:
    type: EventType

@dataclass
class TradeEvent(Event):
    order_id: str

@dataclass
class TradeOrderEvent(Event):
    order_data: Dict

@dataclass
class QueryOrderEvent(Event):
    pass

@dataclass
class CancelOrderEvent(Event):
    pass

@dataclass
class QuoteEvent(Event):
    symbol: str

@dataclass
class HistoricalDataEvent(Event):
    symbol: str

@dataclass
class NewsEvent(Event):
    pass

@dataclass
class LoginEvent(Event):
    pass

@dataclass
class VerifyEvent(Event):
    pass

@dataclass
class SetEnvEvent(Event):
    env: str

@dataclass
class GetStatusEvent(Event):
    pass