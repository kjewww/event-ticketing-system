from uuid import UUID

class CreateEventCommand:
    def __init__(
        self,
        organizer_id: UUID,
        name: str,
        description: str,
        date_range: dict,
        location: str,
        capacity: int
    ):
        self.organizer_id = organizer_id
        self.name = name
        self.description = description
        self.date_range = date_range
        self.location = location
        self.capacity = capacity