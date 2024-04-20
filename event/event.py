from dataclasses import dataclass, field
from typing import Dict, Optional
from datetime import datetime
from enum import Enum

@dataclass
class Event:
    event_timestamp: datetime

@dataclass
class TradeEvent(Event):
    pass

class OrderType(Enum):
    LMT = 1 # 限价单
    MKT = 2 # 市价单
    STL = 3 # 止损限价单
    STP = 4 # 止损市价单
    LIT = 5 # 限价止盈单
    MIT = 6 # 市价止盈单
    TSL = 7 # 跟踪止损限价单
    TS = 8 # 跟踪止损市价单
    
class OrderSide(Enum):
    BUY = 1 # 买入
    SELL = 2 # 卖出
    SHORT = 3 # 卖空
    COVER = 4 # 平仓
    
@dataclass
class PlaceOrderEvent(Event):
    order_id: str
    ticker: str
    order_quantity: int
    order_type: OrderType = OrderType.LMT
    order_side: OrderSide = OrderSide.BUY
    order_price: Optional[float] = None

@dataclass
class UpdatePositionEvent(Event):
    pass

@dataclass
class ClosePositionEvent(Event):
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

class LogLevel(Enum):
    INFO = 1
    ERROR = 2
    
@dataclass
class LogEvent(Event):
    message: str
    log_level: LogLevel = LogLevel.INFO