from uuid import UUID
from src.domain.value_objects.date_range import DateRange
from src.domain.value_objects.event_status import EventStatus
from datetime import datetime

class EventResponseDTO:
    def __init__(
        self,
        event_id: UUID,
        organizer_id: UUID,
        name: str,
        description: str,
        start_date: datetime,
        end_date: datetime,
        location: str,
        capacity: int,
        status: EventStatus,
    ):
        self.event_id = event_id
        self.organizer_id = organizer_id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.capacity = capacity
        self.status = status
