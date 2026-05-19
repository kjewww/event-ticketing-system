from uuid import UUID

class EventResponseDTO:
    def __init__(
        self,
        id: UUID,
        organizer_id: UUID,
        name: str,
        description: str,
        date_range: dict,
        location: str,
        capacity: int,
        status: str,
        ticket_categories: list[dict]
    ):
        self.id = id
        self.organizer_id = organizer_id
        self.name = name
        self.description = description
        self.date_range = date_range
        self.location = location
        self.capacity = capacity
        self.status = status
        self.ticket_categories = ticket_categories