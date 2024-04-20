
from event.event import OrderSide,OrderType
from moomoo import TrdSide
from moomoo import OrderType as TrdType


convert_from_OrderSide_to_TrdSide = {
    OrderSide.BUY: TrdSide.BUY,
    OrderSide.SELL: TrdSide.SELL,
    OrderSide.SHORT: TrdSide.SELL,
    OrderSide.COVER: TrdSide.BUY
}

convert_from_OrderType_to_TrdType= {
    OrderType.LMT: TrdType.NORMAL,
    OrderType.MKT: TrdType.MARKET,
    OrderType.STL: TrdType.STOP_LIMIT,
    OrderType.STP: TrdType.STOP,
    OrderType.LIT: TrdType.LIMIT_IF_TOUCHED,
    OrderType.MIT: TrdType.MARKET_IF_TOUCHED,
    OrderType.TSL: TrdType.TRAILING_STOP_LIMIT,
    OrderType.TS: TrdType.TRAILING_STOP
}

convert_to_OrderType = {
    '1': OrderType.LMT,
    '2': OrderType.MKT,
    '3': OrderType.STL,
    '4': OrderType.STP,
    '5': OrderType.LIT,
    '6': OrderType.MIT,
    '7': OrderType.TSL,
    '8': OrderType.TS
}

convert_to_OrderSide = {
    'BUY': OrderSide.BUY,
    'SELL': OrderSide.SELL,
    # 'SHORT': OrderSide.SHORT,
    'COVER': OrderSide.COVER
}