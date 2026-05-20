from src.application.commands.disable_ticket_category_command import (
    DisableTicketCategoryCommand,
)
from src.application.dto.ticket_category_dto import (
    DisableTicketCategoryResponseDTO,
)
from src.application.interfaces.unit_of_work import UnitOfWork

from src.domain.repositories.event_repository import EventRepository


class DisableTicketCategoryCommandHandler:
    def __init__(
        self,
        event_repository: EventRepository,
        unit_of_work: UnitOfWork,
    ):
        self.event_repository = event_repository
        self.unit_of_work = unit_of_work

    def handle(
        self,
        command: DisableTicketCategoryCommand,
    ) -> DisableTicketCategoryResponseDTO:
        try:
            event = self.event_repository.get_by_id(command.event_id)

            if event is None:
                raise ValueError("Event not found.")

            if event.organizer_id != command.organizer_id:
                raise PermissionError(
                    "Only the event organizer can disable this ticket category."
                )

            ticket_category = event.get_ticket_category_by_id(
                command.ticket_category_id
            )

            if ticket_category is None:
                raise ValueError("Ticket category not found.")

            event.disable_ticket_category(command.ticket_category_id)

            self.event_repository.save(event)
            self.unit_of_work.commit()

            return DisableTicketCategoryResponseDTO(
                event_id=event.id,
                ticket_category_id=ticket_category.id,
                name=ticket_category.name,
                is_active=ticket_category.is_active,
            )

        except Exception:
            self.unit_of_work.rollback()
            raise