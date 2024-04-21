from moomoo import OpenSecTradeContext, SecurityFirm, TrdMarket
from backend.config import ConfigManager
from .utils import convert_to_SecurityFirm, convert_to_filter_trdmarket

class Context:
    _instance = None

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

    def close(self, trd_ctx: OpenSecTradeContext):
        if trd_ctx:
            trd_ctx.close()
    
    