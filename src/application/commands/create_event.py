import datetime
from uuid import UUID

from click import command
from src.domain.aggregates.event import Event
from src.domain.repositories.event_repository import EventRepository
from src.application.dto.event_dto import EventResponseDTO
from src.domain.value_objects.date_range import DateRange

class CreateEventCommand:
    def __init__(
        self,
        organizer_id: UUID,
        name: str,
        description: str,
        start_date: datetime,
        end_date: datetime,
        location: str,
            capacity: int
    ):
        self.organizer_id = organizer_id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.capacity = capacity

class CreateEventCommandHandler:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def handle(self, command: CreateEventCommand) -> EventResponseDTO:
        event = Event(
            organizer_id=command.organizer_id,
            name=command.name,
            description=command.description,
            date_range=DateRange(start_date=command.start_date, end_date=command.end_date),
            location=command.location,
            capacity=command.capacity
            )
        self.event_repository.save(event)
        
        return EventResponseDTO(
            event_id=event.id,
            organizer_id=event.organizer_id,
            name=event.name,
            description=event.description,
            start_date=event.date_range.start_date,
            end_date=event.date_range.end_date,
            location=event.location,
            capacity=event.capacity,
            status=event.status,
        )