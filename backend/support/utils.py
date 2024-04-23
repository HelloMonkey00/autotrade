
from event.event import LogEvent, OrderSide,OrderType, TrailType
from moomoo import TrdSide, SecurityFirm, TrdMarket
from moomoo import OrderType as TrdType
from moomoo import TrailType as MooMooTrailType
from datetime import datetime


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

convert_from_OrderSide_to_TrailType = {
    None: None,
    TrailType.AMOUNT: MooMooTrailType.AMOUNT,
    TrailType.RATIO: MooMooTrailType.RATIO
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

convert_to_SecurityFirm = {
    'FUTUSECURITIES': SecurityFirm.FUTUSECURITIES,
    'FUTUINC': SecurityFirm.FUTUINC,
    'FUTUSG': SecurityFirm.FUTUSG,
    'FUTUAU': SecurityFirm.FUTUAU
}

convert_to_filter_trdmarket = {
    'HK': TrdMarket.HK,      # 香港市场
    'US': TrdMarket.US,      # 美国市场
    'CN': TrdMarket.CN,      # 大陆市场
    'HKCC': TrdMarket.HKCC,  # 香港A股通市场
    'FUTURES': TrdMarket.FUTURES,  # 期货市场
    'FUTURES_SIMULATE_HK': TrdMarket.FUTURES_SIMULATE_HK,
    'FUTURES_SIMULATE_US': TrdMarket.FUTURES_SIMULATE_US,
    'FUTURES_SIMULATE_SG': TrdMarket.FUTURES_SIMULATE_SG,
    'FUTURES_SIMULATE_JP': TrdMarket.FUTURES_SIMULATE_JP
}

def format_log(event: LogEvent):
    # 将时间格式化为包含毫秒的字符串
    timestamp = event.event_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    # 在日志信息前面加上时间戳
    return f"{timestamp} - {event.message}"

def convert_to_TrailType_and_TrailValue(order_data):
    if 'trail_amount' in order_data and order_data['trail_amount'] is not None:
        return TrailType.AMOUNT, order_data['trail_amount']
    elif 'trail_ratio' in order_data and order_data['trail_ratio'] is not None:
        return TrailType.RATIO, order_data['trail_ratio']
    else:
        return None, None