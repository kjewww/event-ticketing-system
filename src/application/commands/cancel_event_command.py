from uuid import UUID


class CancelEventCommand:
    def __init__(
        self,
        event_id: UUID,
        organizer_id: str,
    ):
        self.event_id = event_id
        self.organizer_id = organizer_id