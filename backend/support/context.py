from moomoo import OpenSecTradeContext, SecurityFirm, TrdMarket, OpenFutureTradeContext,OpenQuoteContext
from backend.config import ConfigManager
from .utils import convert_to_SecurityFirm, convert_to_filter_trdmarket

class Context:
    _instance = None
    _trd_ctx = None
    _futures_trd_ctx = None
    _quote_ctx = None
    _handlers = []
    _futures_handlers = []
    _quote_handlers = []

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
    
    def open(self):
        security_firm_str = ConfigManager.get_instance().get('security_firm', '', 'MOOMOO')
        security_firm = convert_to_SecurityFirm[security_firm_str]
        filter_trdmarket_str = ConfigManager.get_instance().get('filter_trdmarket', '', 'MOOMOO')
        filter_trdmarket = convert_to_filter_trdmarket[filter_trdmarket_str]
        trd_ctx = OpenSecTradeContext(filter_trdmarket=filter_trdmarket, host='127.0.0.1', port=11111, security_firm=security_firm)
        return trd_ctx
    
    def open_futures(self):
        security_firm_str = ConfigManager.get_instance().get('security_firm', '', 'MOOMOO')
        security_firm = convert_to_SecurityFirm[security_firm_str]
        filter_trdmarket_str = ConfigManager.get_instance().get('futures_filter_trdmarket', '', 'MOOMOO')
        filter_trdmarket = convert_to_filter_trdmarket[filter_trdmarket_str]
        futures_trd_ctx = OpenFutureTradeContext(filter_trdmarket=filter_trdmarket, host='127.0.0.1', port=11111, security_firm=security_firm)
        return futures_trd_ctx
    
    def open_quote(self):
        quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        return quote_ctx

    def close(self):
        if not self._trd_ctx:
            self._trd_ctx.close()
            
    def close(self, trd_ctx: OpenSecTradeContext):
        if not trd_ctx:
            trd_ctx.close()
    
    def close(self, trd_ctx: OpenFutureTradeContext):
        if not trd_ctx:
            trd_ctx.close()
    
    def close(self, quote_ctx: OpenQuoteContext):
        if not quote_ctx:
            quote_ctx.close()

    def close_futures(self):
        if not self._futures_trd_ctx:
            self._futures_trd_ctx.close()
    
    def close_quote(self):
        if not self._quote_ctx:
            self._quote_ctx.close()
            self._quote_ctx = None
    
    def add_handler(self, handler):
        self._handlers.append(handler)
        if self._trd_ctx:
            self._trd_ctx.set_handler(handler)

    def add_futures_handler(self, futures_handler):
        self._futures_handlers.append(futures_handler)
        if self._futures_trd_ctx:
            self._futures_trd_ctx.set_handler(futures_handler)
    
    def add_quote_handler(self, quote_handler):
        self._quote_handlers.append(quote_handler)
        if self._quote_ctx:
            self._quote_ctx.set_handler(quote_handler)
    