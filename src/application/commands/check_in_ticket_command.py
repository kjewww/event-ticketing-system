from datetime import datetime
from uuid import UUID


class CheckInTicketCommand:
    def __init__(
        self,
        event_id: UUID,
        ticket_code: str,
        checked_in_at: datetime,
    ):
        self.event_id = event_id
        self.ticket_code = ticket_code
        self.checked_in_at = checked_in_at