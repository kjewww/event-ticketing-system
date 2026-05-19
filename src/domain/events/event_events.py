from datetime import datetime
from uuid import UUID, uuid4

class EventCreated:
    def __init__(self, event_id: UUID):
        self.event_id = event_id
        self.occurred_at = datetime.now()


class EventCancelled:
    def __init__(self, event_id: UUID):
        self.event_id = event_id
        self.occurred_at = datetime.now()

class EventPublished:
    def __init__(self, event_id: UUID):
        self.event_id = event_id
        self.occurred_at = datetime.now()