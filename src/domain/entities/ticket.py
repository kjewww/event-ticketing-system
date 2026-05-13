from datetime import datetime
from uuid import UUID

from src.domain.value_objects.ticket_code import TicketCode
from src.domain.value_objects.ticket_status import TicketStatus
from src.domain.exceptions.domain_exception import TicketCannotBeCheckedInError


class Ticket:
    def __init__(
        self,
        id: UUID,
        booking_id: UUID,
        event_id: UUID,
        ticket_category_id: UUID,
        ticket_code: TicketCode,
        status: TicketStatus = TicketStatus.ACTIVE,
        checked_in_at: datetime | None = None,
    ):
        self.id = id
        self.booking_id = booking_id
        self.event_id = event_id
        self.ticket_category_id = ticket_category_id
        self.ticket_code = ticket_code
        self.status = status
        self.checked_in_at = checked_in_at

    def check_in(self, checked_in_at: datetime) -> None:
        if self.status != TicketStatus.ACTIVE:
            raise TicketCannotBeCheckedInError(
                "Only active tickets can be checked in."
            )

        self.status = TicketStatus.CHECKED_IN
        self.checked_in_at = checked_in_at

    def cancel(self) -> None:
        self.status = TicketStatus.CANCELLED

    def mark_refund_required(self) -> None:
        self.status = TicketStatus.REFUND_REQUIRED

    def is_checked_in(self) -> bool:
        return self.status == TicketStatus.CHECKED_IN

    def is_active(self) -> bool:
        return self.status == TicketStatus.ACTIVE