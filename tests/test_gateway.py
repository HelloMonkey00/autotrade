from datetime import datetime
import unittest
from backend.trade.gateway import on_trade_order
from event.event import OrderEvent, OrderSide, OrderType

class TestGateway(unittest.TestCase):
    def test_on_trade_order(self):
        # 创建一个 PlaceOrderEvent 对象
        event = OrderEvent(
            order_side=OrderSide.BUY,
            order_type=OrderType.LMT,
            order_price=100.0,
            order_quantity=1,
            ticker='AAPL',
            event_timestamp=datetime.now(),
            order_id='123456'
        )

        # 调用 on_trade_order 函数
        on_trade_order(event)

        # TODO: 验证 on_trade_order 函数的副作用，例如它是否修改了数据库或发送了网络请求

if __name__ == '__main__':
    unittest.main()