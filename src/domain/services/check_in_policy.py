from datetime import datetime

from src.domain.aggregates.booking import Booking
from src.domain.aggregates.event import Event
from src.domain.exceptions.domain_exception import TicketCannotBeCheckedInError
from src.domain.value_objects.event_status import EventStatus
from src.domain.value_objects.ticket_code import TicketCode
from src.domain.value_objects.ticket_status import TicketStatus


class CheckInPolicy:
    def ensure_check_in_allowed(
        self,
        event: Event,
        booking: Booking,
        ticket_code: TicketCode,
        checked_in_at: datetime,
    ) -> None:
        if event.status == EventStatus.CANCELLED:
            raise TicketCannotBeCheckedInError("Event has been cancelled.")

        ticket = booking.get_ticket_by_code(ticket_code)

        if ticket is None:
            raise TicketCannotBeCheckedInError("Ticket code is invalid.")

        if ticket.event_id != event.id:
            raise TicketCannotBeCheckedInError("Ticket does not match this event.")

        if not event.date_range.contains(checked_in_at):
            raise TicketCannotBeCheckedInError(
                "Ticket can only be checked in on the event date."
            )

        if ticket.status == TicketStatus.CHECKED_IN:
            raise TicketCannotBeCheckedInError("Ticket has already been used.")

        if ticket.status != TicketStatus.ACTIVE:
            raise TicketCannotBeCheckedInError("Only active tickets can be checked in.")