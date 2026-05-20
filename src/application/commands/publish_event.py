from uuid import UUID
from src.domain.aggregates.event import Event
from src.domain.repositories.event_repository import EventRepository
from src.application.dto.event_dto import EventResponseDTO

class PublishEventCommand:
    def __init__(self, event_id: UUID):
        self.event_id = event_id
        
class PublishEventCommandHandler:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def handle(self, command: PublishEventCommand) -> EventResponseDTO:
        event = self.event_repository.get_by_id(command.event_id)
        event.publish()
        self.event_repository.save(event)

        return EventResponseDTO(
            event_id=event.id,
            name=event.name,
            status=event.status,
        )