from backend.support.context import Context
from event.event import LogEvent, LogLevel,SemiTradeConnectedEvent,OptionsQuoteEvent
from event.eventbus import event_bus
from moomoo import *
from backend.config import ConfigManager
import pandas as pd
import numpy as np

def on_semi_trade_init(event: SemiTradeConnectedEvent):
    quote_ctx = Context.get_instance().open_quote()
    option_code = ConfigManager.get_instance().get('option_code', None, 'MOOMOO')
    ret_sub, err_message = quote_ctx.subscribe(option_code, [SubType.QUOTE], subscribe_push=False)
    # 先订阅 K 线类型。订阅成功后 OpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本
    if ret_sub == RET_OK:  # 订阅成功
        ret, data = quote_ctx.get_stock_quote(option_code)  # 获取订阅股票报价的实时数据
        if ret == RET_OK:
            last_price = data['last_price'][0]
        else:
            event_bus.publish(LogEvent('get_stock_quote error: ' + str(data), LogLevel.ERROR))
            return
    else:
        event_bus.publish(LogEvent('subscribe error: ' + err_message, LogLevel.ERROR))
        return

    ret, data = quote_ctx.get_option_expiration_date(code=option_code)
    if ret == RET_OK:
        expiration_date_list = data['strike_time'].values.tolist()
        date = expiration_date_list[0] # 取第一个到期日
        ret2, data2 = quote_ctx.get_option_chain(code=option_code, start=date, end=date)
        if ret2 == RET_OK:
            event_bus.publish(build_options_quote_event(data2, last_price))
        else:
            event_bus.publish(LogEvent('get_option_chain error: ' + str(data2), LogLevel.ERROR))
            return
    else:
        event_bus.publish(LogEvent('get_option_expiration_date error: ' + str(data), LogLevel.ERROR))
        return

def build_options_quote_event(data, last_price):
    higher_code_put, lower_code_put = find_closest_strike_codes(data, last_price, 'PUT')
    higher_code_call, lower_code_call = find_closest_strike_codes(data, last_price, 'CALL')
    return OptionsQuoteEvent(data['code'][0], last_price, higher_code_put, lower_code_put, higher_code_call, lower_code_call, event_timestamp=datetime.now())

def find_closest_strike_codes(data: pd.DataFrame, last_price: float, option_type: str):
    """
    Find the codes in the data where option_type is CALL or PUT and the absolute difference between strike_price and last_price is the smallest,
    one for strike_price higher than last_price and one for strike_price lower than last_price.

    Parameters:
    data (pd.DataFrame): The data containing the option information.
    last_price (float): The last price to compare with.
    option_type (str): The type of the option, either "CALL" or "PUT".

    Returns:
    tuple: The codes of the rows with the smallest absolute difference, one for higher and one for lower.
    """
    # Filter the data by option_type
    data = data[data['option_type'] == option_type]

    # Separate the data into higher and lower than last_price
    higher_data = data[data['strike_price'] > last_price]
    lower_data = data[data['strike_price'] <= last_price]

    # Calculate the absolute difference between strike_price and last_price for higher and lower data
    higher_data['diff'] = np.abs(higher_data['strike_price'] - last_price)
    lower_data['diff'] = np.abs(lower_data['strike_price'] - last_price)

    # Find the row with the smallest difference for higher and lower data
    min_diff_row_higher = higher_data[higher_data['diff'] == higher_data['diff'].min()]
    min_diff_row_lower = lower_data[lower_data['diff'] == lower_data['diff'].min()]

    # Return the code of the row with the smallest difference for higher and lower
    return min_diff_row_higher['code'][0], min_diff_row_lower['code'][0]

event_bus.subscribe(SemiTradeConnectedEvent, on_semi_trade_init)