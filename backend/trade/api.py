

from backend.support.context import Context
from backend.trade.objects import GetSnapshotsRequest, GetSnapshotsResponse, Snapshot
from moomoo import RET_OK
from event.event import LogEvent, LogLevel
from event.eventbus import event_bus

class API:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(API, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def get_snapshots(self, request: GetSnapshotsRequest) -> GetSnapshotsResponse:
        try:
            quote_ctx = Context.get_instance().open_quote();
            ret, data = quote_ctx.get_market_snapshot(request.code_list)
            if RET_OK == ret:
                snapshots = [Snapshot(code=row['code'], last_price=row['last_price'], implied_volatility = row['option_implied_volatility']) for index, row in data.iterrows()]
                return GetSnapshotsResponse(snapshots=snapshots)
            else:
                event_bus.publish(LogEvent('get_market_snapshot error: ' + str(data), LogLevel.ERROR))
        finally:
            Context.get_instance().close_quote()
            
    def get_option_chain(self, code: str, start: str, end: str):
        try:
            quote_ctx = Context.get_instance().open_quote()
            ret, data = quote_ctx.get_option_chain(code=code, start=start, end=end)
            if RET_OK == ret:
                return data
            else:
                event_bus.publish(LogEvent('get_option_chain error: ' + str(data), LogLevel.ERROR))
                return None
        finally:
            Context.get_instance().close_quote()
    
    def get_option_expiration_date(self, code: str):
        try:
            quote_ctx = Context.get_instance().open_quote()
            ret, data = quote_ctx.get_option_expiration_date(code=code)
            if RET_OK == ret:
                return data
            else:
                event_bus.publish(LogEvent('get_option_expiration_date error: ' + str(data), LogLevel.ERROR))
                return None
        finally:
            Context.get_instance().close_quote()
            