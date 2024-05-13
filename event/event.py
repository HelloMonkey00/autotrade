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
    
    def __str__(self):
        return self.name
    
class OrderSide(Enum):
    BUY = 1 # 买入
    SELL = 2 # 卖出
    SHORT = 3 # 卖空
    COVER = 4 # 平仓
    
    def __str__(self):
        return self.name

class TrailType(Enum):
    AMOUNT = 1
    RATIO = 2

    def __str__(self):
        return self.name
    
@dataclass
class OrderEvent(Event):
    order_id: str
    ticker: str
    order_quantity: int
    order_type: OrderType = OrderType.LMT
    order_side: OrderSide = OrderSide.BUY
    order_price: Optional[float] = None

@dataclass
class TrailOrderEvent(OrderEvent):
    trail_type: Optional[TrailType] = None
    trail_value: Optional[float] = None
    retry: Optional[int] = 0


@dataclass
class ClosePositionEvent(Event):
    ticker: str

class Command(Enum):
    PLACE_ORDER = 'placeOrder'
    CLOSE_POSITION = 'closePosition'
    MODIFY_POSITION = 'modifyPosition'

    def __str__(self):
        return self.name
@dataclass
class SemiTradeCommandEvent(Event):
    command: Command
    call_quantity: int = 0
    call_level: int = 0
    put_quantity: int = 0
    put_level: int = 0
    order_id: Optional[str] = None

    @classmethod
    def from_request(cls, request_data):
        return cls(
            event_timestamp=datetime.now(),
            command=Command(request_data['command']),
            call_quantity=int(request_data['call']['quantity']),
            call_level=int(request_data['call']['level']),
            put_quantity=int(request_data['put']['quantity']),
            put_level=int(request_data['put']['level'])
        )

@dataclass
class GetAccountEvent(Event):
    pass
@dataclass
class QuoteEvent(Event):
    symbol: str


@dataclass
class HistoricalDataEvent(Event):
    ticker: str

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
    DEBUG = 0
    INFO = 1
    ERROR = 2

    def __str__(self):
        return self.name
    
class LogEvent(Event):
    def __init__(self, message, log_level=LogLevel.INFO, event_timestamp = None):
        self.message = message
        self.log_level = log_level
        if event_timestamp:
            self.event_timestamp = event_timestamp
        else:
            self.event_timestamp = datetime.now()

    def to_dict(self):
        return {'message': self.message, 'level': str(self.log_level), 'timestamp': self.event_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")}

class SemiTradeConnectedEvent(Event):
    pass

class OptionsQuoteEvent(Event):
    code: str
    price: float = None
    higher_code_put: str = None
    lower_code_put: str = None
    higher_code_call: str = None
    lower_code_call: str = None

    def to_dict(self):
        return {'code': self.code, 'price': self.price, 'higher_code_put': self.higher_code_put, 'lower_code_put': self.lower_code_put, 'higher_code_call': self.higher_code_call, 'lower_code_call': self.lower_code_call, 'timestamp': self.event_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")}