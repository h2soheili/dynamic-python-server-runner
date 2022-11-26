from app.enums import EventTypes


class Event(object):
    def __int__(self, event_type: EventTypes, parent_order_key: int, order_key: int):
        self.event_type = event_type.value
        self.parent_order_key = event_type
        self.order_key = order_key
