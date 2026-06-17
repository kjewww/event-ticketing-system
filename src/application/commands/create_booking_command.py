from datetime import datetime
from decimal import Decimal
from uuid import UUID


class CreateBookingCommand:
    def __init__(
        self,
        customer_id: UUID,
        customer_name: str,
        event_id: UUID,
        ticket_category_id: UUID,
        quantity: int,
        requested_at: datetime,
        service_fee_amount: Decimal = Decimal("0"),
        currency: str = "IDR",
    ):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.event_id = event_id
        self.ticket_category_id = ticket_category_id
        self.quantity = quantity
        self.requested_at = requested_at
        self.service_fee_amount = service_fee_amount
        self.currency = currency