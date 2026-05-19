from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.domain.value_objects.ticket_code import TicketCode


class TicketCheckedIn:
    def __init__(
        self,
        booking_id: UUID,
        ticket_id: UUID,
        event_id: UUID,
        ticket_code: TicketCode,
    ):
        self.id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

        self.booking_id = booking_id
        self.ticket_id = ticket_id
        self.event_id = event_id
        self.ticket_code = ticket_code