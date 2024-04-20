from asyncio.log import logger
from typing import Type, Callable, Dict, List

class EventBus:
    def __init__(self):
        self.subscribers: Dict[Type, List[Callable]] = {}

    def subscribe(self, event_type: Type, callback: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def publish(self, event):
        event_type = type(event)
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                try:
                    callback(event)
                except Exception as e:
                    logger.error(f"Error in event handler {callback.__name__}: {e}")
                    raise e

event_bus = EventBus()