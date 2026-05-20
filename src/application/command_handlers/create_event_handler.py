from src.application.commands.create_event_command import CreateEventCommand
from src.application.dto.event_dto import CreateEventResponseDTO
from src.application.interfaces.unit_of_work import UnitOfWork

from src.domain.aggregates.event import Event
from src.domain.repositories.event_repository import EventRepository
from src.domain.value_objects.date_range import DateRange


class CreateEventCommandHandler:
    def __init__(
        self,
        event_repository: EventRepository,
        unit_of_work: UnitOfWork,
    ):
        self.event_repository = event_repository
        self.unit_of_work = unit_of_work

    def handle(self, command: CreateEventCommand) -> CreateEventResponseDTO:
        try:
            date_range = DateRange(
                start_date=command.start_date,
                end_date=command.end_date,
            )

            event = Event(
                organizer_id=command.organizer_id,
                name=command.name,
                description=command.description,
                date_range=date_range,
                location=command.location,
                capacity=command.capacity,
            )

            self.event_repository.save(event)
            self.unit_of_work.commit()

            return CreateEventResponseDTO(
                event_id=event.id,
                organizer_id=event.organizer_id,
                name=event.name,
                description=event.description,
                start_date=event.date_range.start_date,
                end_date=event.date_range.end_date,
                location=event.location,
                capacity=event.capacity,
                status=event.status.value,
            )

        except Exception:
            self.unit_of_work.rollback()
            raise