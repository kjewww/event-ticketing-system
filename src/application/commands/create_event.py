from uuid import UUID
from src.domain.aggregates.event import Event
from src.domain.repositories.event_repository import EventRepository
from src.application.dto.event_response_dto import EventResponseDTO

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

class CreateEventHandler:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def handle(self, command: CreateEventCommand) -> EventResponseDTO:
        event = Event(
            organizer_id=command.organizer_id,
            name=command.name,
            description=command.description,
            date_range=command.date_range,
            location=command.location,
            capacity=command.capacity
        )
        self.event_repository.save(event)
        
        return EventResponseDTO(
            id=event.id,
            organizer_id=event.organizer_id,
            name=event.name,
            description=event.description,
            date_range=event.date_range,
            location=event.location,
            capacity=event.capacity,
            status=event.status,
            ticket_categories=event.ticket_categories
        )