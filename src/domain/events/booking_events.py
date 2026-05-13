from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.domain.value_objects.money import Money


class TicketReserved:
    def __init__(
        self,
        booking_id: UUID,
        customer_id: UUID,
        event_id: UUID,
        ticket_category_id: UUID,
        quantity: int,
        total_price: Money,
    ):
        self.event_id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

        self.booking_id = booking_id
        self.customer_id = customer_id
        self.ticketing_event_id = event_id
        self.ticket_category_id = ticket_category_id
        self.quantity = quantity
        self.total_price = total_price


class BookingPaid:
    def __init__(
        self,
        booking_id: UUID,
        customer_id: UUID,
        event_id: UUID,
        total_price: Money,
    ):
        self.event_id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

        self.booking_id = booking_id
        self.customer_id = customer_id
        self.ticketing_event_id = event_id
        self.total_price = total_price


class BookingExpired:
    def __init__(
        self,
        booking_id: UUID,
        customer_id: UUID,
        event_id: UUID,
    ):
        self.event_id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

        self.booking_id = booking_id
        self.customer_id = customer_id
        self.ticketing_event_id = event_id