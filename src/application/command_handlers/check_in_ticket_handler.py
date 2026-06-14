from src.application.commands.check_in_ticket_command import CheckInTicketCommand
from src.application.dto.ticket_dto import CheckInTicketResponseDTO
from src.application.interfaces.unit_of_work import UnitOfWork

from src.domain.repositories.booking_repository import BookingRepository
from src.domain.repositories.event_repository import EventRepository
from src.domain.services.check_in_policy import CheckInPolicy
from src.domain.value_objects.ticket_code import TicketCode


class CheckInTicketCommandHandler:
    def __init__(
        self,
        event_repository: EventRepository,
        booking_repository: BookingRepository,
        unit_of_work: UnitOfWork,
        check_in_policy: CheckInPolicy | None = None,
    ):
        self.event_repository = event_repository
        self.booking_repository = booking_repository
        self.unit_of_work = unit_of_work
        self.check_in_policy = check_in_policy or CheckInPolicy()

    def handle(
        self,
        command: CheckInTicketCommand,
    ) -> CheckInTicketResponseDTO:
        try:
            event = self.event_repository.get_by_id(command.event_id)

            if event is None:
                raise ValueError("Event not found.")

            ticket_code = TicketCode(command.ticket_code)

            booking = self.booking_repository.get_by_ticket_code(ticket_code)

            if booking is None:
                raise ValueError("Ticket code is invalid.")

            self.check_in_policy.ensure_check_in_allowed(
                event=event,
                booking=booking,
                ticket_code=ticket_code,
                checked_in_at=command.checked_in_at,
            )

            booking.check_in_ticket(
                ticket_code=ticket_code,
                checked_in_at=command.checked_in_at,
            )

            ticket = booking.get_ticket_by_code(ticket_code)

            self.booking_repository.save(booking)
            self.unit_of_work.commit()

            return CheckInTicketResponseDTO(
                ticket_code=ticket.ticket_code.value,
                event_id=ticket.event_id,
                booking_id=ticket.booking_id,
                status=ticket.status.value,
                checked_in_at=ticket.checked_in_at,
            )

        except Exception:
            self.unit_of_work.rollback()
            raise