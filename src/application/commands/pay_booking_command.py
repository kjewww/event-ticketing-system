from datetime import datetime
from decimal import Decimal
from uuid import UUID


class PayBookingCommand:
    def __init__(
        self,
        booking_id: UUID,
        customer_id: UUID,
        amount: Decimal,
        paid_at: datetime,
        currency: str = "IDR",
    ):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.amount = amount
        self.currency = currency
        self.paid_at = paid_at