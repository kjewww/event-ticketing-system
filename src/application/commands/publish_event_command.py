from uuid import UUID


class PublishEventCommand:
    def __init__(
        self,
        event_id: UUID,
        organizer_id: UUID,
    ):
        self.event_id = event_id
        self.organizer_id = organizer_id