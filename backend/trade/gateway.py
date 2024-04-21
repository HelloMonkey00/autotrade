from backend.support.context import Context
from event.event import *
from event.eventbus import event_bus
from moomoo import RET_OK, TrdEnv, TrdSide
from backend.config import ConfigManager
from backend.support.risk import RiskManager 
from backend.support.utils import convert_from_OrderSide_to_TrdSide, convert_from_OrderType_to_TrdType
import json

def on_trade_order(tradeOrderEvent: PlaceOrderEvent):
    pwd_unlock = ConfigManager.get_instance().get('pwd_unlock', None, 'MOOMOO')
    try:
        trd_ctx = Context.get_instance().open()
        simulate = ConfigManager.get_instance().is_simulate()
        if not simulate:
            ret, data = trd_ctx.unlock_trade(pwd_unlock)  # 若使用真实账户下单，需先对账户进行解锁。
            if ret != RET_OK:
                event_bus.publish(LogEvent('unlock_trade failed: ' + data, LogLevel.ERROR))
                return
        trd_side = convert_from_OrderSide_to_TrdSide[tradeOrderEvent.order_side]
        trd_type = convert_from_OrderType_to_TrdType[tradeOrderEvent.order_type]
        trd_env = TrdEnv.SIMULATE if simulate else TrdEnv.REAL
        acc_id = ConfigManager.get_instance().get_int('acc_id', 0, 'MOOMOO')
        ret, data = RiskManager.get_instance().check_risk(tradeOrderEvent)
        if ret != RET_OK:
            event_bus.publish(LogEvent('Risk check failed: ' + data, LogLevel.ERROR))
            return
        else:
            ret, data = trd_ctx.place_order(tradeOrderEvent.order_price, order_type=trd_type, qty=tradeOrderEvent.order_quantity, 
                                            code=tradeOrderEvent.ticker, trd_side=trd_side, trd_env=trd_env,
                                            acc_id = acc_id)
            RiskManager.get_instance().unlock(tradeOrderEvent)
            if ret == RET_OK:
                event_bus.publish(LogEvent('place_order success: ' + str(data), LogLevel.INFO))
                event_bus.publish(TradeEvent())
            else:
                event_bus.publish(LogEvent('place_order error: ' + str(data), LogLevel.ERROR))
    finally:
        Context.get_instance().close(trd_ctx)

def on_close_position(event: ClosePositionEvent):
    event_bus.publish(LogEvent('close_position', LogLevel.INFO))

def on_get_account(event: GetAccountEvent):
    try:
        trd_ctx = Context.get_instance().open()
        ret, data = trd_ctx.get_acc_list()
        if ret == RET_OK:
            for _, account in data.iterrows():
                if account['trd_env'] == 'SIMULATE':
                    account_data = account.to_dict()
                    event_bus.publish(LogEvent('get_acc_list success:'+str(account_data), LogLevel.INFO))
        else:
            event_bus.publish(LogEvent('get_acc_list error: ' + str(data), LogLevel.ERROR))
    finally:
        Context.get_instance().close(trd_ctx)

event_bus.subscribe(GetAccountEvent, on_get_account)
event_bus.subscribe(PlaceOrderEvent, on_trade_order)
event_bus.subscribe(ClosePositionEvent, on_close_position)