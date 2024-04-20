from .config import ConfigManager
from moomoo import OpenSecTradeContext, SecurityFirm, TrdMarket

class Context:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
    
    def open(self):
        security_firm_str = ConfigManager.get_instance().get('security_firm', 'FUTUSG', 'MOOMOO')
        security_firm = getattr(SecurityFirm, security_firm_str)
        filter_trdmarket_str = ConfigManager.get_instance().get('filter_trdmarket', 'HK', 'MOOMOO')
        filter_trdmarket = getattr(TrdMarket, filter_trdmarket_str)
        trd_ctx = OpenSecTradeContext(filter_trdmarket=security_firm, host='127.0.0.1', port=11111, security_firm=filter_trdmarket)
        return trd_ctx

    def close(self, trd_ctx: OpenSecTradeContext):
        if trd_ctx:
            trd_ctx.close()