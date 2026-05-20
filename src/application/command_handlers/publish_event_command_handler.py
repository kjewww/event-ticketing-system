from src.application.commands.publish_event_command import PublishEventCommand
from src.application.dto.event_dto import PublishEventResponseDTO
from src.application.interfaces.unit_of_work import UnitOfWork

from src.domain.repositories.event_repository import EventRepository


class PublishEventCommandHandler:
    def __init__(
        self,
        event_repository: EventRepository,
        unit_of_work: UnitOfWork,
    ):
        self.event_repository = event_repository
        self.unit_of_work = unit_of_work

    def handle(self, command: PublishEventCommand) -> PublishEventResponseDTO:
        try:
            event = self.event_repository.get_by_id(command.event_id)

            if event is None:
                raise ValueError("Event not found.")

            if event.organizer_id != command.organizer_id:
                raise PermissionError(
                    "Only the event organizer can publish this event."
                )

            event.publish()

            self.event_repository.save(event)
            self.unit_of_work.commit()

            return PublishEventResponseDTO(
                event_id=event.id,
                name=event.name,
                status=event.status.value,
            )

        except Exception:
            self.unit_of_work.rollback()
            raise