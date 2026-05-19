from datetime import datetime, timezone
from uuid import UUID, uuid4


class TicketReserved:
    def __init__(
        self,
        booking_id: UUID,
        event_id: UUID,
        customer_id: str,
        ticket_category_id: UUID,
        quantity: int,
    ):
        self.id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

        self.booking_id = booking_id
        self.event_id = event_id
        self.customer_id = customer_id
        self.ticket_category_id = ticket_category_id
        self.quantity = quantity


class BookingPaid:
    def __init__(self, booking_id: UUID):
        self.id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

        self.booking_id = booking_id


class BookingExpired:
    def __init__(self, booking_id: UUID):
        self.id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

        self.booking_id = booking_id