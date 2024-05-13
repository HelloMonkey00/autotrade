from backend.config import ConfigManager
from backend.support.context import Context
from backend.support.risk import RiskManager
from event.event import *
from event.eventbus import event_bus
from moomoo import RET_OK, ModifyOrderOp, TrdEnv, OptionType
from backend.support.utils import convert_from_OrderSide_to_TrdSide, convert_from_OrderType_to_TrdType, convert_from_TrailType_to_MooMooTrailType
import pytz
import yfinance as yf
        
def get_lastest_option_chain():
    try:
        # Get the option chain for the S&P 500 index
        date_str = datetime.now(pytz.timezone('US/Eastern')).date().strftime('%Y-%m-%d')
        option_chain = yf.Ticker("^SPX").option_chain(date_str) # 有 15 分钟延迟

        # Get the latest price
        sp500 = yf.Ticker("^GSPC")
        latest_price = (sp500.info['bid'] + sp500.info['ask']) / 2
        
        event_bus.publish(LogEvent('SPX latest_price: ' + str(latest_price), LogLevel.INFO))

        return latest_price, option_chain
    except Exception as e:
        event_bus.publish(LogEvent('get_option_chain error: ' + str(e), LogLevel.ERROR))
        raise e

def find_level_strike_code(option_chain_data, last_price, level):
    """
    Find the code in the data where option_type is CALL or PUT and the strike_price is the closest to the level.

    Parameters:
    option_chain_data (pd.DataFrame): The data containing the option information.
    last_price (float): The last price to compare with.
    option_type (str): The type of the option, either "CALL" or "PUT".
    level (float): The level to compare with.

    Returns:
    str: The code of the row with the closest strike price to the level.
    """
    data = option_chain_data

    if level > 0:
        # Find rows where strike_price is greater than last_price
        data = data[data['strike'] > last_price]
        # Sort by the absolute difference between strike_price and last_price
        data = data.iloc[(data['strike'] - last_price).abs().argsort()]
        # Get the row at the position specified by level
        row = data.iloc[level - 1]
    elif level < 0:
        # Find rows where strike_price is less than last_price
        data = data[data['strike'] < last_price]
        # Sort by the absolute difference between strike_price and last_price
        data = data.iloc[(last_price - data['strike']).abs().argsort()]
        # Get the row at the position specified by level
        row = data.iloc[-level - 1]
    else:
        # Find the row with the closest strike price to the last_price
        row = data.iloc[(data['strike_price'] - last_price).abs().argsort()[:1]]

    # SPXW240513C04000000 -> US.SPXW240513C4000000
    return 'US.' + row['contractSymbol'][:11] + row['contractSymbol'][12:]

def get_undo_order_list():
    try:
        simulate = ConfigManager.get_instance().is_simulate()
        trd_env = TrdEnv.SIMULATE if simulate else TrdEnv.REAL
        acc_id = ConfigManager.get_instance().get_int('acc_id', 0, 'MOOMOO')
        trd_ctx = Context.get_instance().open()
        ret, data = trd_ctx.order_list_query(trd_env=trd_env, acc_id=acc_id)
        if ret != RET_OK:
            event_bus.publish(LogEvent('order_list_query error: ' + str(data), LogLevel.ERROR))
            return None
        return data['order_id'].values.tolist()
    finally:
        Context.get_instance().close(trd_ctx)

def cancel_order(order_list):
    try:
        trd_ctx = Context.get_instance().open()
        simulate = ConfigManager.get_instance().is_simulate()
        if not simulate:
            pwd_unlock = ConfigManager.get_instance().get('pwd_unlock', None, 'MOOMOO')
            ret, data = trd_ctx.unlock_trade(pwd_unlock)  # 若使用真实账户下单，需先对账户进行解锁。
            if ret != RET_OK:
                event_bus.publish(LogEvent('unlock_trade failed: ' + data, LogLevel.ERROR))
                return
        trd_env = TrdEnv.SIMULATE if simulate else TrdEnv.REAL
        acc_id = ConfigManager.get_instance().get_int('acc_id', 0, 'MOOMOO')
        for order_id in order_list:
            ret, data = trd_ctx.modify_order(ModifyOrderOp.CANCEL, order_id, qty=0, price=0, trd_env=trd_env, acc_id=acc_id)
            if ret != RET_OK:
                event_bus.publish(LogEvent('order_list_cancel error: ' + str(data), LogLevel.ERROR))
    finally:
        Context.get_instance().close(trd_ctx)

def get_position(code=None):
    try:
        simulate = ConfigManager.get_instance().is_simulate()
        trd_ctx = Context.get_instance().open()
        trd_env = TrdEnv.SIMULATE if simulate else TrdEnv.REAL
        acc_id = ConfigManager.get_instance().get_int('acc_id', 0, 'MOOMOO')
        code = '' if code is None else code
        ret, data = trd_ctx.position_list_query(trd_env = trd_env, acc_id = acc_id, code = code)
        if ret != RET_OK:
            event_bus.publish(LogEvent('position_list_query error: ' + str(data), LogLevel.ERROR))
            return None
        return data
    finally:
        Context.get_instance().close(trd_ctx)
        
# 根据参数下 2 号单
def handle_place_order(event:SemiTradeCommandEvent):
    last_price, option_chain_data = get_lastest_option_chain()
    if event.call_quantity > 0:
        ticker = find_level_strike_code(option_chain_data.calls, last_price, event.call_level)
        order = OrderEvent(datetime.now(), ticker=ticker, order_quantity=event.call_quantity, order_type=OrderType.MKT, order_side=OrderSide.BUY, order_id=event.order_id + "_call", order_price=1.0)
        event_bus.publish(LogEvent('place_order, ticker: ' + order.ticker + ', quantity: ' + str(order.order_quantity) , LogLevel.INFO))
        event_bus.publish(order)
    if event.put_quantity > 0:
        ticker = find_level_strike_code(option_chain_data.puts, last_price, event.put_level)
        order = OrderEvent(datetime.now(), ticker=ticker, order_quantity=event.put_quantity, order_type=OrderType.MKT, order_side=OrderSide.BUY, order_id=event.order_id + "_put", order_price=1.0)
        event_bus.publish(LogEvent('place_order, ticker: ' + order.ticker + ', quantity: ' + str(order.order_quantity) , LogLevel.INFO))
        event_bus.publish(order)

def handle_close_position(event:SemiTradeCommandEvent):
    order_list = get_undo_order_list()
    cancel_order(order_list)
    position_data = get_position()
    sequence = 0
    for index, row in position_data.iterrows():
        ticker = row['code']
        try:
            # Lock the ticker to prevent other threads from modifying the position
            RiskManager.get_instance().lock(ticker)
            ticker_position = get_position(ticker)
            if ticker_position is not None:
                for index, row in ticker_position.iterrows():
                    sequence += 1
                    order = OrderEvent(datetime.now(), ticker=ticker, order_quantity=row['can_sell_qty'], order_type=OrderType.MKT, order_side=OrderSide.SELL, order_id=event.order_id + "_close_" + sequence)
                    event_bus.publish(order)
        finally:
            RiskManager.get_instance().unlock(ticker)

def handle_modify_position(event:SemiTradeCommandEvent):
    handle_close_position(event)
    handle_place_order(event)

def handle_semi_trade_command(event: SemiTradeCommandEvent):
    if event.command == Command.PLACE_ORDER:
        handle_place_order(event)
    elif event.command == Command.CLOSE_POSITION:
        handle_close_position(event)
    elif event.command == Command.MODIFY_POSITION:
        handle_modify_position(event)


event_bus.subscribe(SemiTradeCommandEvent, handle_semi_trade_command)