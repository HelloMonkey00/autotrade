import threading

from .context import Context
from event.event import *
from event.eventbus import event_bus
from .utils import convert_from_OrderType_to_TrdType
from .config import ConfigManager
from moomoo import RET_OK, TrdEnv

class RiskManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RiskManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.__init__(*args, **kwargs)  # 初始化 _instance
        return cls._instance
    
    def __init__(self):
        self.locks = {}

    def lock(self, event: PlaceOrderEvent):
        # Get the lock for this ticker
        lock = self.locks.setdefault(event.ticker, threading.Lock())
        lock.acquire()

    def unlock(self, event: PlaceOrderEvent):
        # Get the lock for this ticker
        lock = self.locks.get(event.ticker)
        if lock is not None and lock.locked():
            lock.release()

    def check_risk(self, event: PlaceOrderEvent):
        simulate = ConfigManager.get_instance().is_simulate()
        if simulate:
            return 0, 'Risk check passed'
        else:
            acc_id = ConfigManager.get_instance().get_int('acc_id', None, 'MOOMOO')
            trd_ctx = Context._instance.open()
            trd_type = convert_from_OrderType_to_TrdType[event.order_type]
            self.lock(event)
            ret, data = trd_ctx.acctradinginfo_query(order_type=trd_type, code=event.ticker, acc_id=acc_id,
                                                     price=event.order_price, qty=event.order_quantity, trd_env=TrdEnv.REAL)
            if ret != RET_OK:
                print('acctradinginfo_query error: ', data)
                event_bus.publish(LogEvent('acctradinginfo_query error: ' + str(data), LogLevel.ERROR))
            if data['max_position_sell'][0] < event.order_quantity:
                event_bus.publish(LogEvent('Risk check failed: max_position_sell+' + str(data['max_position_sell'][0]), LogLevel.ERROR))
                return -1, 'Risk check failed: max_position_sell+' + str(data['max_position_sell'][0])
            else:
                event_bus.publish(LogEvent('Risk check passed', LogLevel.INFO))
                return 0, 'Risk check passed'

if __name__ == '__main__':
    risk = RiskManager()
    risk.lock('AAPL')
    risk.unlock('AAPL')