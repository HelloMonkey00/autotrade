import threading

from .context import Context
from event.event import *
from event.eventbus import event_bus
from .utils import convert_from_OrderType_to_TrdType
from backend.config import ConfigManager
from moomoo import RET_OK, TrdEnv

class RiskManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        self.locks = {}
        self.used_order_ids = set()
    
    def unlock(self, x):
        if isinstance(x, str):
            # Get the lock for this ticker
            lock = self.locks.get(x)
            if lock is not None and lock.locked():
                lock.release()
        elif isinstance(x, OrderEvent):
            # Get the lock for this ticker
            lock = self.locks.get(x.ticker)
            if lock is not None and lock.locked():
                lock.release()
        
    def lock(self, x):
        if isinstance(x, OrderEvent):
            # Get the lock for this ticker
            lock = self.locks.setdefault(x.ticker, threading.Lock())
            if not lock.acquire(timeout=5):  # Check if the lock was acquired
                raise TimeoutError(f"Unable to acquire lock for {x.ticker} within 5 seconds")
        elif isinstance(x, str):
            # Get the lock for this ticker
            lock = self.locks.setdefault(x, threading.Lock())
            if not lock.acquire(timeout=5):  # Check if the lock was acquired
                raise TimeoutError(f"Unable to acquire lock for {x} within 5 seconds")

    def check_duplicate(self, event: OrderEvent):
        # Check if the order is a duplicate
        pass

    def check_risk(self, event: OrderEvent):
        # Check if the order is a duplicate
        if event.order_id in self.used_order_ids:
            event_bus.publish(LogEvent('Risk check failed: duplicate order_id', LogLevel.ERROR))
            return -1, 'Risk check failed: duplicate order_id'
        else:
            self.used_order_ids.add(event.order_id)
        # Check if the order quantity exceeds the maximum position
        acc_id = ConfigManager.get_instance().get_int('acc_id', 0, 'MOOMOO')
        trd_ctx = Context.get_instance().open()
        trd_type = convert_from_OrderType_to_TrdType[event.order_type]
        trd_env = TrdEnv.SIMULATE if ConfigManager.get_instance().is_simulate() else TrdEnv.REAL
        order_price = 0.0 if event.order_type == OrderType.MKT else event.order_price
        ret, data = trd_ctx.acctradinginfo_query(order_type=trd_type, code=event.ticker, acc_id=acc_id,
                                                price=order_price, trd_env=trd_env)
        if ret != RET_OK:
            event_bus.publish(LogEvent('acctradinginfo_query error: ' + str(data), LogLevel.ERROR))
            return -1, 'Risk check failed: acctradinginfo_query error'
        if event.order_side == OrderSide.BUY and data['max_cash_buy'][0] < event.order_quantity:
            event_bus.publish(LogEvent('Risk check failed: max_cash_buy+' + str(data['max_cash_buy'][0]), LogLevel.ERROR))
            return -1, 'Risk check failed: max_cash_buy+' + str(data['max_cash_buy'][0])
        if event.order_side == OrderSide.SELL and data['max_position_sell'][0] < event.order_quantity:
            event_bus.publish(LogEvent('Risk check failed: max_position_sell+' + str(data['max_position_sell'][0]), LogLevel.ERROR))
            return -1, 'Risk check failed: max_position_sell+' + str(data['max_position_sell'][0])
        
        event_bus.publish(LogEvent('Risk check passed', LogLevel.INFO))
        return 0, 'Risk check passed'

if __name__ == '__main__':
    risk = RiskManager()
    risk.lock('AAPL')
    risk.unlock('AAPL')