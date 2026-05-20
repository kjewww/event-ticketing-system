from uuid import UUID


class ViewEventDetailsQuery:
    def __init__(self, event_id: UUID):
        self.event_id = event_id