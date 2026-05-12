from datetime import datetime

class EventPublished:
    def __init__(self, event_id):
        self.event_id = event_id
        self.occured_at = datetime.now()