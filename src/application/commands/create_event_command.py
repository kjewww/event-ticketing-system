from datetime import date, datetime
from uuid import UUID


class CreateEventCommand:
    def __init__(
        self,
        organizer_id: UUID,
        name: str,
        description: str,
        start_date: date | datetime,
        end_date: date | datetime,
        location: str,
        capacity: int,
    ):
        self.organizer_id = organizer_id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.capacity = capacity