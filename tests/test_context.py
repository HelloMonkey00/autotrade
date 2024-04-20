import unittest
from backend.support.context import Context
from moomoo import OpenSecTradeContext

class TestContext(unittest.TestCase):
    def test_open_and_close(self):
        # 创建一个 Context 对象
        context = Context()

        # 调用 open 方法
        trd_ctx = context.open()

        # 验证 trd_ctx 的类型
        self.assertIsInstance(trd_ctx, OpenSecTradeContext)

        # 调用 close 方法
        context.close(trd_ctx)

if __name__ == '__main__':
    unittest.main()