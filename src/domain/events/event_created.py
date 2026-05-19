from datetime import datetime, timezone
from uuid import UUID, uuid4


class EventCreated:
    def __init__(self, event_id: UUID):
        self.id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

        self.event_id = event_id