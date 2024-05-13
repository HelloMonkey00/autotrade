from moomoo import *
from time import sleep

from backend.support.context import Context

class TradeDealCallBack(TradeDealHandlerBase):
    """ order update push"""
    def on_recv_rsp(self, rsp_pb):
        ret, content = super(TradeDealCallBack, self).on_recv_rsp(rsp_pb)
        print("TradeDealCallBack", ret, content)
        return ret, content

class FuturesTradeDealCallBack(TradeDealHandlerBase):
    """ order update push"""
    def on_recv_rsp(self, rsp_pb):
        ret, content = super(FuturesTradeDealCallBack, self).on_recv_rsp(rsp_pb)
        print("FuturesTradeDealCallBack", ret, content)
        return ret, content

Context.get_instance().add_handler(TradeDealCallBack())
Context.get_instance().add_futures_handler(FuturesTradeDealCallBack())